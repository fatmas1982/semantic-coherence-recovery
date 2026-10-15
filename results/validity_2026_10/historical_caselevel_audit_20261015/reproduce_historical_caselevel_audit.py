import io,zipfile,hashlib,json,re
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, cohen_kappa_score
root=Path('/mnt/data');out=root/'IPM_HISTORICAL_CASELEVEL_AUDIT_20261015';out.mkdir(exist_ok=True)
records=[];checks=[];issues=[]
for archive in ['P2_CPU_RESULTS_BUNDLE(5).zip','P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE(3).zip']:
 z=zipfile.ZipFile(root/archive); summary=pd.read_csv(io.BytesIO(z.read('summary/ALL_METRICS.csv')))
 expfiles=[s for s in z.namelist() if s.startswith('experiments/') and s.endswith('.zip')]
 for src in expfiles:
  name=Path(src).stem
  try:
   inner=zipfile.ZipFile(io.BytesIO(z.read(src)))
   preds=pd.read_csv(io.BytesIO(inner.read('reports/PREDICTIONS.csv')),dtype={'Case_ID':str,'Prompt_ID':str})
   report=pd.read_csv(io.BytesIO(inner.read('reports/METRICS_AND_CLUSTER_CI.csv')))
   pred_col=[c for c in ['pred','M1_pred','M3_pred','M4_pred','M3_dual_pred','M3_size_matched_pred'] if c in preds.columns][0]
   if len(preds)!=len(preds.Case_ID.unique()):issues.append((archive,name,'DUPLICATE_CASE_IDS',len(preds)-preds.Case_ID.nunique()))
   if preds.Prompt_ID.nunique()!=120:issues.append((archive,name,'PROMPT_GROUP_COUNT',preds.Prompt_ID.nunique()))
   for _,row in report.iterrows():
    grp=str(row['group'])
    if grp=='all': d=preds
    elif grp=='exclude_M01':d=preds[preds.Generator_Stratum!=0]
    elif grp=='M01':d=preds[preds.Generator_Stratum==0]
    elif grp.startswith('generator_M'):d=preds[preds.Generator_Stratum==int(grp.split('_M')[1])-1]
    elif grp.startswith('human_easy_'):d=preds[preds.Human_Easy.astype(str).str.lower()==grp.split('human_easy_')[1].lower()]
    else:issues.append((archive,name,'UNRECOGNIZED_GROUP',grp));continue
    yt=d.y_true.astype(int);yp=d[pred_col].astype(int)
    mf=f1_score(yt,yp,labels=sorted(preds.y_true.astype(int).unique()),average='macro',zero_division=0)
    ac=accuracy_score(yt,yp)
    smatch=summary.loc[(summary.experiment==name)&(summary.group==grp)]
    if len(smatch)!=1:issues.append((archive,name,'SUMMARY_MISSING_OR_DUPLICATE',grp));continue
    s=smatch.iloc[0]
    n=int(len(d))
    record=dict(archive=archive,experiment=name,group=grp,predictions_n=n,report_n=int(row.n),summary_n=int(s.n),case_id_unique=preds.Case_ID.is_unique,prompt_clusters=preds.Prompt_ID.nunique(),calc_macro_f1=mf,report_macro_f1=float(row.macro_f1),summary_macro_f1=float(s.macro_f1),calc_accuracy=ac,report_accuracy=float(row.accuracy),summary_accuracy=float(s.accuracy),f1_report_absdiff=abs(mf-float(row.macro_f1)),f1_summary_absdiff=abs(mf-float(s.macro_f1)),accuracy_report_absdiff=abs(ac-float(row.accuracy)),accuracy_summary_absdiff=abs(ac-float(s.accuracy)),ci_low=float(row.ci_low),ci_high=float(row.ci_high),ci_bounds_valid=bool(0<=row.ci_low<=row.ci_high<=1),summary_ci_match=bool(abs(row.ci_low-s.ci_low)<1e-12 and abs(row.ci_high-s.ci_high)<1e-12))
    records.append(record)
  except Exception as e:issues.append((archive,name,'PROCESSING_ERROR',str(e)))
df=pd.DataFrame(records)
df['PASS']=df.apply(lambda x: x.predictions_n==x.report_n==x.summary_n and x.case_id_unique and x.prompt_clusters==120 and max(x.f1_report_absdiff,x.f1_summary_absdiff,x.accuracy_report_absdiff,x.accuracy_summary_absdiff)<1e-9 and x.ci_bounds_valid and x.summary_ci_match,axis=1)
df.to_csv(out/'ALL_680_CASELEVEL_RECOMPUTED_CHECKS.csv',index=False)
pd.DataFrame(issues,columns=['archive','experiment','issue','detail']).to_csv(out/'ISSUES.csv',index=False)
meta={'archived_runs':68,'recomputed_rows':len(df),'passes':int(df.PASS.sum()),'failed_rows':int((~df.PASS).sum()),'issues':issues,'max_f1_difference':float(df[['f1_report_absdiff','f1_summary_absdiff']].max().max()),'max_accuracy_difference':float(df[['accuracy_report_absdiff','accuracy_summary_absdiff']].max().max()),'counts_by_archive':df.groupby('archive').size().to_dict()}
(out/'AUDIT_SUMMARY.json').write_text(json.dumps(meta,indent=2))
print(json.dumps(meta,indent=2));print(df.loc[~df.PASS,['archive','experiment','group','f1_report_absdiff','accuracy_report_absdiff']].head(15).to_string(index=False))
