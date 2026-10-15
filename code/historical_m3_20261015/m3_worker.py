from pathlib import Path
import sys,os,json,time,gc,shutil,hashlib,inspect
os.environ.setdefault('TOKENIZERS_PARALLELISM','false')
os.environ.setdefault('HF_HOME',str(Path.home()/'.cache/p2_hf_cache'))
import numpy as np,pandas as pd,torch,transformers
from collections import Counter
from sklearn.metrics import f1_score
from datasets import Dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from transformers import (AutoTokenizer,AutoModelForSequenceClassification,AutoModelForCausalLM,
 DataCollatorWithPadding,Trainer,TrainingArguments,EarlyStoppingCallback,set_seed)
from huggingface_hub import HfApi
job=json.loads(Path(sys.argv[1]).read_text())
state=Path(job['state'])
manifest=json.loads((state/'SNAPSHOT.json').read_text())
for filename,expected in manifest['hashes'].items():
 actual=hashlib.sha256((state/filename).read_bytes()).hexdigest()
 assert actual==expected,('Worker snapshot changed',filename)
# Pickles are created by this notebook from the verified inputs; do not supply external pickles.
gold=pd.read_pickle(state/'gold.pkl')
oof=pd.read_pickle(state/'oof.pkl')
GOLD_BY_CASE=gold.set_index('Case_ID',drop=False)
TARGETS=list(oof)
GPU_OUTPUT=Path(job['output']);OUTPUT=GPU_OUTPUT
# GPU 2 — original M3 training definitions
def serialise_C(g):
 prompt=str(g['Prompt_Text'] if pd.notna(g['Prompt_Text']) else '').strip()
 source=str(g['Source_Context'] if pd.notna(g['Source_Context']) else '').strip()
 output=str(g['Model_Output'] if pd.notna(g['Model_Output']) else '').strip()
 if str(g['Source_Available']).lower()=='yes' and source:
  return f'Task:\n{prompt}\n\nAuthorised source/context:\n{source}\n\nResponse:\n{output}'
 return f'Task:\n{prompt}\n\nResponse:\n{output}'
TEXT={str(r['Case_ID']):serialise_C(r) for _,r in gold.iterrows()}
# Exact TF-IDF/LinearSVC settings from P2_81_CPU_VALIDITY_DIAGNOSTICS.py.
def m1_fit_predict(train,test):
 labels=set(train.y_true.astype(int));assert labels==set(test['_target_classes'].iloc[0])
 vec=TfidfVectorizer(ngram_range=(1,2),min_df=2,max_df=.98,max_features=40000,sublinear_tf=True)
 xtr=vec.fit_transform([TEXT[str(x)] for x in train.Case_ID])
 xte=vec.transform([TEXT[str(x)] for x in test.Case_ID])
 clf=LinearSVC(C=1.0,class_weight='balanced',random_state=20260908)
 clf.fit(xtr,train.y_true.astype(int));return clf.predict(xte)
def selected_train(rows,fold,gen,variant,repeat,target):
 base=rows[rows.Fold.astype(int)!=fold]
 blocked=base[base.Generator_Stratum.astype(int)!=gen]
 if variant=='dual':return blocked.copy()
 assert variant=='size_matched'
 # Stable independent subset seed, invariant to Python hash randomization.
 key=f'{target}|{fold}|{gen}|{repeat}|20260928'.encode()
 seed=int(hashlib.sha256(key).hexdigest()[:8],16)
 rng=np.random.default_rng(seed)
 for attempt in range(200):
  idx=rng.choice(len(base),size=len(blocked),replace=False)
  selected=base.iloc[np.sort(idx)].copy()
  if set(selected.y_true.astype(int))==set(rows.y_true.astype(int)):
   dev_fold=(fold+1)%5
   inner=selected[selected.Fold.astype(int)!=dev_fold]
   if set(inner.y_true.astype(int))==set(rows.y_true.astype(int)):
    return selected
 raise RuntimeError('Could not obtain class-complete size-matched subset')

SEED=20260908
M3_MODEL_ID='answerdotai/ModernBERT-base'
M3_MODEL_REVISION='c0e44438c79d5a72972fe8b14dbbc822418356c9'
MAX_LENGTH=1024
LEARNING_RATE=2e-5
WEIGHT_DECAY=.01
MAX_SELECT_EPOCHS=8
TRAIN_BATCH=8
EVAL_BATCH=16
GRAD_ACCUM=2
EARLY_STOPPING_PATIENCE=2
BOOT_REPS=2000
TARGETS_TO_RUN=TARGETS

def serialise_C(g):
    prompt=str(g['Prompt_Text'] if pd.notna(g['Prompt_Text']) else '').strip()
    source=str(g['Source_Context'] if pd.notna(g['Source_Context']) else '').strip()
    output=str(g['Model_Output'] if pd.notna(g['Model_Output']) else '').strip()
    if str(g['Source_Available']).lower()=='yes' and source:
        return f'Task:\n{prompt}\n\nAuthorised source/context:\n{source}\n\nResponse:\n{output}'
    return f'Task:\n{prompt}\n\nResponse:\n{output}'

tokenizer=AutoTokenizer.from_pretrained(M3_MODEL_ID,revision=M3_MODEL_REVISION)
M3_TOKENIZER=tokenizer
class WeightedTrainer(Trainer):
    def __init__(self,*args,class_weights=None,**kwargs):
        super().__init__(*args,**kwargs); self.class_weights=class_weights
    def compute_loss(self,model,inputs,return_outputs=False,num_items_in_batch=None):
        labels=inputs.pop('labels'); out=model(**inputs)
        loss=torch.nn.functional.cross_entropy(out.logits,labels,weight=self.class_weights.to(out.logits.device))
        return (loss,out) if return_outputs else loss

def compute_metrics_eval(eval_pred):
    logits,labels=eval_pred
    return {'macro_f1':f1_score(labels,np.argmax(logits,axis=-1),average='macro')}

def make_dataset(rows,label_to_idx):
    return Dataset.from_dict({
        'text':[serialise_C(gold_by_case.loc[str(cid)]) for cid in rows.Case_ID],
        'labels':[label_to_idx[int(v)] for v in rows.y_true],
        'case_id':[str(x) for x in rows.Case_ID],
    })

def tokenise(ds):
    ids=list(ds['case_id'])
    def fn(batch): return tokenizer(batch['text'],truncation=True,max_length=MAX_LENGTH)
    return ds.map(fn,batched=True,remove_columns=['text','case_id']),ids

def weights_for(rows,label_to_idx):
    c=Counter(label_to_idx[int(v)] for v in rows.y_true); n=sum(c.values()); k=len(label_to_idx)
    assert set(c)==set(range(k)),f'Missing training class: {c}'
    return torch.tensor([n/(k*c[i]) for i in range(k)],dtype=torch.float32)

def selected_epoch(trainer):
    cand=[(float(x['eval_macro_f1']),float(x['epoch'])) for x in trainer.state.log_history if 'eval_macro_f1' in x and 'epoch' in x]
    assert cand
    best=max(v for v,_ in cand); epochs=[e for v,e in cand if abs(v-best)<1e-12]
    return max(1,int(round(min(epochs)))),best
LOCAL_TMP=Path(job['work_root'])/'p2_gpu_tmp';LOCAL_TMP.mkdir(exist_ok=True)
LOCAL_CACHE=(Path.home()/'.cache/p2_hf_cache');LOCAL_CACHE.mkdir(exist_ok=True)
os.environ['HF_HOME']=str(LOCAL_CACHE)
# The imported original training helper uses gold_by_case.
gold_by_case=GOLD_BY_CASE
def train_cell(target,outer_fold,heldout_generator,variant,repeat):
    rows=oof[target].copy()
    labels=sorted(rows.y_true.astype(int).unique())
    label_to_idx={v:i for i,v in enumerate(labels)}; idx_to_label={i:v for v,i in label_to_idx.items()}
    test=rows[(rows.Fold.astype(int)==outer_fold)&(rows.Generator_Stratum.astype(int)==heldout_generator)].copy()
    outer_train=selected_train(rows,outer_fold,heldout_generator,variant,repeat,target)
    outer_train=outer_train.sort_values('Case_ID').copy()
    assert len(test)>0
    assert set(outer_train.y_true.astype(int).unique())==set(labels)

    available=sorted(outer_train.Fold.astype(int).unique())
    preferred=(outer_fold+1)%5
    dev_fold=preferred if preferred in available else available[0]
    inner_dev=outer_train[outer_train.Fold.astype(int)==dev_fold].copy()
    inner_train=outer_train[outer_train.Fold.astype(int)!=dev_fold].copy()
    assert set(inner_train.y_true.astype(int).unique())==set(labels)

    # Stage 1: epoch selection inside the doubly restricted population.
    tr,_=tokenise(make_dataset(inner_train,label_to_idx)); dv,_=tokenise(make_dataset(inner_dev,label_to_idx))
    select_dir=LOCAL_TMP/f'select_{target}_{variant}_r{repeat}_f{outer_fold}_g{heldout_generator}'
    shutil.rmtree(select_dir,ignore_errors=True); select_dir.mkdir(parents=True,exist_ok=True)
    set_seed(SEED)
    m=AutoModelForSequenceClassification.from_pretrained(M3_MODEL_ID,revision=M3_MODEL_REVISION,num_labels=len(labels))
    bf=torch.cuda.is_bf16_supported()
    args=TrainingArguments(
        output_dir=str(select_dir),learning_rate=LEARNING_RATE,weight_decay=WEIGHT_DECAY,
        num_train_epochs=MAX_SELECT_EPOCHS,per_device_train_batch_size=TRAIN_BATCH,
        per_device_eval_batch_size=EVAL_BATCH,gradient_accumulation_steps=GRAD_ACCUM,
        eval_strategy='epoch',save_strategy='epoch',load_best_model_at_end=True,
        metric_for_best_model='macro_f1',greater_is_better=True,save_total_limit=1,
        bf16=bf,fp16=not bf,report_to='none',seed=SEED,data_seed=SEED,logging_steps=20,
    )
    trainer=WeightedTrainer(model=m,args=args,train_dataset=tr,eval_dataset=dv,
        data_collator=DataCollatorWithPadding(tokenizer),compute_metrics=compute_metrics_eval,
        class_weights=weights_for(inner_train,label_to_idx),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=EARLY_STOPPING_PATIENCE)])
    trainer.train(); epochs,best_dev=selected_epoch(trainer)
    del trainer,m,tr,dv; gc.collect(); torch.cuda.empty_cache(); shutil.rmtree(select_dir,ignore_errors=True)

    # Stage 2: fresh refit on all restricted outer-training rows, then one test pass.
    tr,_=tokenise(make_dataset(outer_train,label_to_idx)); te,_=tokenise(make_dataset(test,label_to_idx))
    refit_dir=LOCAL_TMP/f'refit_{target}_{variant}_r{repeat}_f{outer_fold}_g{heldout_generator}'
    shutil.rmtree(refit_dir,ignore_errors=True); refit_dir.mkdir(parents=True,exist_ok=True)
    set_seed(SEED)
    m=AutoModelForSequenceClassification.from_pretrained(M3_MODEL_ID,revision=M3_MODEL_REVISION,num_labels=len(labels))
    args=TrainingArguments(
        output_dir=str(refit_dir),learning_rate=LEARNING_RATE,weight_decay=WEIGHT_DECAY,
        num_train_epochs=epochs,per_device_train_batch_size=TRAIN_BATCH,
        per_device_eval_batch_size=EVAL_BATCH,gradient_accumulation_steps=GRAD_ACCUM,
        eval_strategy='no',save_strategy='no',bf16=bf,fp16=not bf,report_to='none',
        seed=SEED,data_seed=SEED,logging_steps=20,
    )
    trainer=WeightedTrainer(model=m,args=args,train_dataset=tr,
        data_collator=DataCollatorWithPadding(tokenizer),class_weights=weights_for(outer_train,label_to_idx))
    trainer.train(); pr=trainer.predict(te)
    probs=torch.softmax(torch.tensor(pr.predictions),dim=-1).numpy(); ii=np.argmax(probs,axis=1)
    out=test[['Case_ID','Prompt_ID','Task_Type','Fold','Generator_Stratum','y_true','Human_Easy']].copy()
    out['M3_dual_pred']=[idx_to_label[int(i)] for i in ii]
    out['M3_dual_probs']=[json.dumps([float(x) for x in p]) for p in probs]
    out['train_n']=len(outer_train); out['variant']=variant; out['repeat']=repeat; out['selected_epochs']=epochs; out['inner_dev_fold']=dev_fold; out['best_inner_dev_macro_f1']=best_dev
    del trainer,m,tr,te; gc.collect(); torch.cuda.empty_cache(); shutil.rmtree(refit_dir,ignore_errors=True)
    return out
assert torch.cuda.is_available()
result=train_cell(job['target'],job['fold'],job['generator'],job['variant'],job['repeat'])
path=Path(job['result']);path.parent.mkdir(parents=True,exist_ok=True)
tmp=path.with_suffix('.tmp');result.to_csv(tmp,index=False);os.replace(tmp,path)
path.with_suffix('.runtime.json').write_text(json.dumps({'torch':torch.__version__,'transformers':transformers.__version__,
 'gpu':torch.cuda.get_device_name(0),'worker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'pid':os.getpid(),'process_isolation':True,'seed':SEED,
 'train_batch':TRAIN_BATCH,'eval_batch':EVAL_BATCH,'grad_accum':GRAD_ACCUM,'max_length':MAX_LENGTH},indent=2))
print('WORKER_M3_SAVED',path,flush=True)
