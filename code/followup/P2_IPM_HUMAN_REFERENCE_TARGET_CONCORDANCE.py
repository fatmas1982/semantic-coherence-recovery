#!/usr/bin/env python3
"""Recompute post-hoc annotator-to-adjudicated-reference T1–T4 concordance.

This contextualises computational scores. It is NOT an independent human ceiling
or new inter-rater reliability estimate because FINAL GOLD v1.0 was built from
the same A1–A3 layer plus senior adjudication.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
BOOT_REPS=2000
SEED=20260908

def read_table(path,sheet=None):
    path=Path(path)
    return pd.read_excel(path,sheet_name=sheet or 0) if path.suffix.lower() in {'.xlsx','.xlsm','.xls'} else pd.read_csv(path)

def family(x):
    s=str(x).strip().upper()
    if s.startswith('SCF-'): return 'Core SCF'
    if s.startswith('OVR-'): return 'OVR'
    if s in {'HREF','NONE'}: return s
    return 'OTHER'

def class_metrics(y,p,labels):
    f1=[]; rec=[]
    for c in labels:
        tp=np.sum((y==c)&(p==c)); fp=np.sum((y!=c)&(p==c)); fn=np.sum((y==c)&(p!=c))
        f1.append(0 if 2*tp+fp+fn==0 else 2*tp/(2*tp+fp+fn))
        rec.append(0 if tp+fn==0 else tp/(tp+fn))
    return float(np.mean(f1)),float(np.mean(rec))

def qwk(y,p,labels):
    labels=list(labels); idx={c:i for i,c in enumerate(labels)}; k=len(labels)
    O=np.zeros((k,k))
    for a,b in zip(y,p):
        if a in idx and b in idx: O[idx[a],idx[b]]+=1
    n=O.sum()
    if not n: return np.nan
    E=np.outer(O.sum(1),O.sum(0))/n
    W=np.fromfunction(lambda i,j:((i-j)**2)/((k-1)**2),(k,k),dtype=float)
    den=(W*E).sum()
    return float(1-(W*O).sum()/den) if den else np.nan

def pred(sub,a,t):
    if t=='T1': return sub[f'{a}_T1'].astype(int).to_numpy(),np.ones(len(sub),bool)
    if t=='T2':
        b=sub[f'{a}_boundary'].astype(str); v=b.isin(['semantic_only','overlap','hallucination_only']).to_numpy()
        return np.where(b.eq('semantic_only'),0,np.where(b.isin(['overlap','hallucination_only']),1,-99)),v
    if t=='T3':
        f=sub[f'{a}_family'].astype(str); v=f.isin(['Core SCF','OVR']).to_numpy()
        return np.where(f.eq('Core SCF'),0,np.where(f.eq('OVR'),1,-99)),v
    s=sub[f'{a}_severity'].astype(int).to_numpy(); v=np.isin(s,[1,2,3])
    return np.where(v,s,-99),v

def metrics(y,p,v,t):
    labels=[0,1] if t!='T4' else [1,2,3]
    mf1,ba=class_metrics(y,p,labels)
    out={'coverage':float(v.mean()),'strict_accuracy':float((y==p).mean()),'strict_balanced_accuracy':ba,'strict_macro_f1':mf1}
    if t=='T4':
        po=np.where(v,p,0); out.update(strict_qwk=qwk(y,po,[0,1,2,3]),strict_mae=float(np.mean(abs(y-po))),strict_within_one=float(np.mean(abs(y-po)<=1)))
    else: out.update(strict_qwk=np.nan,strict_mae=np.nan,strict_within_one=np.nan)
    if v.any():
        yy=y[v]; pp=p[v]; cmf1,_=class_metrics(yy,pp,labels)
        out.update(conditional_accuracy=float((yy==pp).mean()),conditional_macro_f1=cmf1,
                   conditional_qwk=qwk(yy,pp,[1,2,3]) if t=='T4' else np.nan,
                   conditional_mae=float(np.mean(abs(yy-pp))) if t=='T4' else np.nan)
    return out

def main():
    ap=argparse.ArgumentParser()
    for a in ['a1','a2','a3']: ap.add_argument('--'+a,required=True)
    ap.add_argument('--gold',required=True); ap.add_argument('--out',required=True)
    z=ap.parse_args(); gold=read_table(z.gold,'FINAL_GOLD')
    anns={a.upper():read_table(getattr(z,a),'Annotation') for a in ['a1','a2','a3']}
    for a,ann in anns.items():
        aa=ann[['case_id','primary_label','boundary_zone','severity_score']].copy(); aa['case_id']=aa.case_id.astype(str)
        gg=gold[['Case_ID',f'{a}_Primary',f'{a}_Boundary',f'{a}_Severity']].copy(); gg['Case_ID']=gg.Case_ID.astype(str)
        m=aa.merge(gg,left_on='case_id',right_on='Case_ID',validate='one_to_one')
        assert len(m)==720
        assert (m.primary_label.astype(str).str.strip().str.upper()==m[f'{a}_Primary'].astype(str).str.strip().str.upper()).all()
        assert (m.boundary_zone.astype(str).str.strip().str.lower()==m[f'{a}_Boundary'].astype(str).str.strip().str.lower()).all()
        assert (pd.to_numeric(m.severity_score)==pd.to_numeric(m[f'{a}_Severity'])).all()
    rows=[]
    for _,r in gold.iterrows():
        x={'Prompt_ID':str(r.Prompt_ID),'gold_T1':int(r.Any_Failure),'gold_boundary':str(r.Final_Boundary),'gold_family':str(r.Final_Family),'gold_severity':int(r.Final_Severity)}
        for a in ['A1','A2','A3']:
            p=str(r[f'{a}_Primary']).strip().upper(); b=str(r[f'{a}_Boundary']).strip().lower(); s=int(r[f'{a}_Severity'])
            x.update({f'{a}_T1':0 if p=='NONE' else 1,f'{a}_boundary':b,f'{a}_family':family(p),f'{a}_severity':s})
        rows.append(x)
    df=pd.DataFrame(rows)
    targets={'T1':df.assign(y=df.gold_T1),
             'T2':df[df.gold_T1==1].assign(y=lambda x:(x.gold_boundary!='semantic_only').astype(int)),
             'T3':df[df.gold_family.isin(['Core SCF','OVR'])].assign(y=lambda x:(x.gold_family=='OVR').astype(int)),
             'T4':df[df.gold_T1==1].assign(y=lambda x:x.gold_severity.astype(int))}
    out=[]
    for t,sub in targets.items():
        groups=sub.Prompt_ID.drop_duplicates().to_numpy(); pa=sub.Prompt_ID.to_numpy(); by={g:np.flatnonzero(pa==g) for g in groups}; y=sub.y.astype(int).to_numpy()
        for a in ['A1','A2','A3']:
            p,v=pred(sub,a,t); pm=metrics(y,p,v,t); ci_names=['strict_accuracy','strict_macro_f1']+(['strict_qwk'] if t=='T4' else []); vals={m:[] for m in ci_names}; rng=np.random.default_rng(SEED)
            for _ in range(BOOT_REPS):
                ids=np.concatenate([by[g] for g in rng.choice(groups,len(groups),replace=True)]); mm=metrics(y[ids],p[ids],v[ids],t)
                for m in ci_names: vals[m].append(mm[m])
            row={'target':t,'annotator':a,'n':len(sub),'prompt_clusters':len(groups),**pm}
            for m in ci_names: row[m+'_ci_low']=float(np.nanquantile(vals[m],.025)); row[m+'_ci_high']=float(np.nanquantile(vals[m],.975))
            out.append(row)
    pd.DataFrame(out).to_csv(z.out,index=False)
if __name__=='__main__': main()
