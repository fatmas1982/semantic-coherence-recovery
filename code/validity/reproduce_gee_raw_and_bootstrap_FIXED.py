from pathlib import Path
import numpy as np, pandas as pd, statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from scipy.stats import norm
import hashlib, json

ROOT=Path('/content/P2_GEE_RAW_REFIT_20261015')
DATA=ROOT/'data'; RESULTS=ROOT/'results'; DATA.mkdir(parents=True,exist_ok=True);RESULTS.mkdir(exist_ok=True)
BASE='https://raw.githubusercontent.com/fatmas1982/semantic-coherence-recovery/main/'
import requests

def dl(relative,dst):
    url=BASE+relative
    r=requests.get(url,timeout=90);r.raise_for_status()
    dst.write_bytes(r.content)
    return {'source':url,'sha256':hashlib.sha256(r.content).hexdigest(),'size':len(r.content)}

manifest=[]
for i in range(1,12):
    n=f'paired_cases_part_{i:02d}.csv'
    manifest.append(dl('data/validity_2026_10/'+n,DATA/n))
refp=RESULTS/'PUBLISHED_GEE_60.csv'
manifest.append(dl('results/validity_2026_10/colab_success_20261014/HJI_GEE_STABILITY_60_LATEST_SOURCE.csv',refp))
raw=pd.concat([pd.read_csv(f,dtype={'case_id':str,'prompt_id':str}) for f in sorted(DATA.glob('paired_cases_part_*.csv'))],ignore_index=True)
KEYS=['judge','target','experiment','variant'];AXES={'primary':'primary_disagree','boundary':'boundary_disagree','severity':'severity_disagree'}
assert len(raw)==10408, f'Wrong rows: {len(raw)}'
assert not raw.duplicated(KEYS+['case_id']).any()
assert len(raw.groupby(KEYS))==20
assert all(c in raw for c in ['changed','gold_label','generator_id','prompt_id',*AXES.values()])
print('Raw case-level input accepted:',len(raw),'rows; groups',len(raw.groupby(KEYS)))

def onefit(df,axis):
    d=df.copy();d['D']=pd.to_numeric(d[AXES[axis]],errors='raise').astype(int)
    x=pd.get_dummies(d[['D','gold_label','generator_id']].astype({'gold_label':'category','generator_id':'category'}),columns=['gold_label','generator_id'],drop_first=True,dtype=float)
    x=sm.add_constant(x.astype(float))
    y=d.changed.astype(float)
    fit=sm.GEE(y,x,groups=d.prompt_id,family=sm.families.Binomial(),cov_struct=sm.cov_struct.Independence()).fit(maxiter=150)
    b=float(fit.params['D']);se=float(fit.bse['D']);
    return {'human_axis':axis,'n_cases':len(d),'prompt_clusters':d.prompt_id.nunique(),'total_changed':int(y.sum()),'num_parameters':len(x.columns),'gee_logodds':b,'gee_adjusted_OR':float(np.exp(b)),'robust_SE':se,'OR_Wald95_low':float(np.exp(b-1.95996398454*se)),'OR_Wald95_high':float(np.exp(b+1.95996398454*se)),'gee_p_unadjusted':float(fit.pvalues['D']),'gee_converged':bool(fit.converged)}

rows=[]
for group_key,g in raw.groupby(KEYS,sort=True):
    for ax in AXES:
        rows.append(dict(zip(KEYS,group_key),**onefit(g,ax)))
fitted=pd.DataFrame(rows)
assert len(fitted)==60 and fitted.gee_converged.all()
fitted['gee_Holm_p_60']=multipletests(fitted.gee_p_unadjusted,method='holm')[1]
fitted['gee_BH_FDR_q_60']=multipletests(fitted.gee_p_unadjusted,method='fdr_bh')[1]
fitted.to_csv(RESULTS/'REFITTED_GEE_60_FROM_RAW.csv',index=False)
print('GEE refit completed:',len(fitted))

# Compare robustly with historical result across compatible columns.
ref=pd.read_csv(refp)
MERGE_KEYS=KEYS+['human_axis']
assert not ref.duplicated(MERGE_KEYS).any()
merged=fitted.merge(ref,on=MERGE_KEYS,suffixes=('_refit','_record'),validate='one_to_one',indicator=True)
assert len(merged)==60 and (merged._merge=='both').all()
cols=['gee_adjusted_OR','gee_p_unadjusted','gee_Holm_p_60','gee_BH_FDR_q_60']
compare=[]
for name in cols:
    a=name+'_refit';b=name+'_record'
    if a not in merged.columns or b not in merged.columns: continue
    xa=pd.to_numeric(merged[a]);xb=pd.to_numeric(merged[b]);diff=np.abs(xa-xb)
    compare.append({'metric':name,'compared':len(diff),'max_abs_difference':float(diff.max()),'n_exceed_1e-6':int((diff>1e-6).sum()),'n_exceed_1e-4':int((diff>1e-4).sum())})
pd.DataFrame(compare).to_csv(RESULTS/'GEE_RAW_REFIT_COMPARISON.csv',index=False)
print(pd.DataFrame(compare).to_string(index=False))

# Exact cluster bootstrap procedure copied from frozen public source, with 2500 reps.
def rd(df):
    weights=df.gold_label.value_counts(normalize=True)
    num=den=0.
    for cl,mass in weights.items():
        v=df[df.gold_label==cl]
        a=v[v.D==1].changed;b=v[v.D==0].changed
        if a.empty or b.empty:continue
        num+=mass*(a.mean()-b.mean());den+=mass
    return num/den if den else np.nan

def boot(df,n=2500,seed=20261010):
    pids=list(pd.unique(df.prompt_id)); labels=sorted(df.gold_label.unique());k=len(pids)
    count=np.zeros((k,len(labels),2),dtype=np.int32);yes=np.zeros_like(count)
    blocks=df.groupby(['prompt_id','gold_label','D'],sort=False)['changed'].agg(['size','sum'])
    pmap={p:i for i,p in enumerate(pids)};cmap={c:i for i,c in enumerate(labels)}
    for (pid,cl,z),a in blocks.iterrows():
        i=pmap[pid];j=cmap[cl];count[i,j,int(z)]=int(a['size']);yes[i,j,int(z)]=int(a['sum'])
    mass=np.asarray([np.mean(df.gold_label==c) for c in labels]);rng=np.random.default_rng(seed)
    idx=rng.integers(k,size=(n,k));C=count[idx].sum(axis=1);Y=yes[idx].sum(axis=1)
    risks=np.divide(Y,C,out=np.full(Y.shape,np.nan),where=C>0)
    eligible=np.isfinite(risks).all(axis=2);w=eligible*mass[None,:]
    delta=np.nan_to_num(risks[:,:,1]-risks[:,:,0],nan=0);sw=w.sum(axis=1)
    samples=np.divide((w*delta).sum(axis=1),sw,out=np.full(n,np.nan),where=sw>0)
    samples=samples[np.isfinite(samples)]
    return np.quantile(samples,[.025,.975]),len(samples)

bs=[]
for group_key,g in raw.groupby(KEYS,sort=True):
    for ax,col in AXES.items():
        d=g.copy();d['D']=d[col].astype(int)
        ci,n=boot(d)
        bs.append(dict(zip(KEYS,group_key),human_axis=ax,class_standardized_RD=float(rd(d)),class_adjusted_bootstrap_low=float(ci[0]),class_adjusted_bootstrap_high=float(ci[1]),bootstrap_valid=n))
boots=pd.DataFrame(bs);boots.to_csv(RESULTS/'REFITTED_CLASS_ADJUSTED_BOOTSTRAP_60.csv',index=False)
# Published full CI reference is separate from the 60-row GEE stability source.
refci=RESULTS/'PUBLISHED_CLASS_ADJUSTED_60.csv'
manifest.append(dl('results/validity_2026_10/colab_success_20261014/CLASS_ADJUSTED_HUMAN_JUDGE_60_CORRECTED_CI_20261010.csv',refci))
published_ci=pd.read_csv(refci)
assert not boots.duplicated(MERGE_KEYS).any(), 'Duplicate bootstrap keys'
assert not published_ci.duplicated(MERGE_KEYS).any(), 'Duplicate published CI keys'
b=boots.merge(published_ci,on=MERGE_KEYS,suffixes=('_refit','_record'),validate='one_to_one',indicator=True)
assert len(b)==60 and b['_merge'].eq('both').all(), 'Bootstrap reference keys do not match one-to-one'
checks=[]
for c in ['class_adjusted_bootstrap_low','class_adjusted_bootstrap_high','class_standardized_RD']:
    a,bcol=c+'_refit',c+'_record'
    if a in b and bcol in b:
        dif=np.abs(pd.to_numeric(b[a])-pd.to_numeric(b[bcol]));checks.append({'metric':c,'max_abs_difference':float(dif.max()),'n_exceed_1e-6':int((dif>1e-6).sum())})
pd.DataFrame(checks).to_csv(RESULTS/'BOOTSTRAP_RAW_RECOMPUTATION_COMPARISON.csv',index=False)
json.dump(manifest,open(RESULTS/'INPUT_PROVENANCE.json','w'),indent=2)
print('Bootstrap completed',len(boots),'contrasts')
print(pd.DataFrame(checks).to_string(index=False))
# Decision rule: only report exact matching if all available comparable fields passed.
gee_checks=pd.DataFrame(compare); bs_checks=pd.DataFrame(checks)
summary={'raw_rows':len(raw),'gee_fits':len(fitted),'bootstrap_contrasts':len(boots),'bootstrap_reps_per_contrast':2500,'all_gee_converged':bool(fitted.gee_converged.all()),'gee_compared_metrics':compare,'bootstrap_compared_metrics':checks,'no_claim_about_original_T1_serialization':True}
json.dump(summary,open(RESULTS/'RUN_SUMMARY.json','w'),indent=2)
from google.colab import files
from zipfile import ZipFile,ZIP_DEFLATED
bundle=Path('/content/P2_GEE_RAW_REFIT_AND_BOOTSTRAP_20261015.zip')
with ZipFile(bundle,'w',ZIP_DEFLATED) as z:
    for f in RESULTS.iterdir():z.write(f,f.name)
print('Saved',bundle);files.download(str(bundle))
