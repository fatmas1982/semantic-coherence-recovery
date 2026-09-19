#!/usr/bin/env python3
"""Pair-specific pre-resolution reliability and adjudication-queue audit.

Uses only locked A1/A2/A3 annotations. No FINAL GOLD value enters reliability.
The 95% intervals use 2,000 task-stratified Prompt_ID-cluster bootstrap
resamples (seed 20260804), preserving all six checkpoint outputs per prompt.

Outputs:
  P2_IPM_PAIR_SPECIFIC_HUMAN_RELIABILITY.csv
  P2_IPM_ADJUDICATION_QUEUE_RULE_AUDIT.csv
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

DEFAULT_A1=Path('data/annotation/historical_full_csv/A1/Annotation.csv')
DEFAULT_A2=Path('data/annotation/historical_full_csv/A2/Annotation.csv')
DEFAULT_A3=Path('data/annotation/historical_full_csv/A3/Annotation.csv')
DEFAULT_OUT=Path('results/followup')
PAIRS=((0,1,'A1-A2'),(0,2,'A1-A3'),(1,2,'A2-A3'))
BOOT_REPS=2000
BOOT_SEED=20260804
QUEUE_FIELDS=['primary_label','secondary_label','boundary_zone','severity_score','href_subtype','ambiguity_flag']


def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument('--a1',type=Path,default=DEFAULT_A1)
    p.add_argument('--a2',type=Path,default=DEFAULT_A2)
    p.add_argument('--a3',type=Path,default=DEFAULT_A3)
    p.add_argument('--out-dir',type=Path,default=DEFAULT_OUT)
    p.add_argument('--bootstrap-reps',type=int,default=BOOT_REPS)
    p.add_argument('--seed',type=int,default=BOOT_SEED)
    return p.parse_args()


def txt(x):
    return '' if pd.isna(x) else str(x).strip()


def secondary(x):
    s=txt(x)
    return 'none' if s.lower() in {'','none','nan'} else s


def family(x):
    x=txt(x)
    if x.startswith('SCF-'): return 'Core SCF'
    if x.startswith('OVR-'): return 'OVR'
    if x in {'HREF','NONE'}: return x
    raise ValueError(x)


def read(path):
    d=pd.read_csv(path)
    req={'case_id','prompt_id','task_type','primary_label','secondary_label','boundary_zone','severity_score','href_subtype','ambiguity_flag'}
    miss=req-set(d.columns)
    if miss: raise ValueError(f'{path}: missing {sorted(miss)}')
    if len(d)!=720 or d.case_id.duplicated().any(): raise ValueError(f'{path}: expected 720 unique cases')
    d=d.copy()
    d['primary_label']=d.primary_label.map(txt)
    d['secondary_label']=d.secondary_label.map(secondary)
    d['family']=d.primary_label.map(family)
    d['boundary_zone']=d.boundary_zone.map(txt)
    d['severity_score']=d.severity_score.astype(int)
    d['href_subtype']=d.href_subtype.map(lambda x: txt(x).lower() or 'none')
    d['ambiguity_flag']=d.ambiguity_flag.map(lambda x: txt(x).lower())
    return d.sort_values('case_id').reset_index(drop=True)


def encode_three(ds, field):
    vals=sorted(set().union(*[set(d[field].tolist()) for d in ds]))
    mp={v:i for i,v in enumerate(vals)}
    arr=np.column_stack([[mp[v] for v in d[field]] for d in ds]).astype(np.int16)
    return arr, vals


def cohen_kappa_codes(x,y,k,weights=None):
    cm=np.bincount(x*k+y,minlength=k*k).reshape(k,k).astype(float)
    n=cm.sum()
    if n==0: return np.nan
    po=np.trace(cm)/n
    px=cm.sum(1)/n; py=cm.sum(0)/n
    if weights is None:
        pe=float(np.dot(px,py))
        return (po-pe)/(1-pe) if pe<1 else 1.0
    idx=np.arange(k)
    w=1.0-((idx[:,None]-idx[None,:])/(k-1))**2
    po_w=float((w*cm).sum()/n)
    pe_cm=np.outer(px,py)
    pe_w=float((w*pe_cm).sum())
    return (po_w-pe_w)/(1-pe_w) if pe_w<1 else 1.0


def make_boot_indices(base,reps,seed):
    rng=np.random.default_rng(seed)
    tasks=sorted(base.task_type.unique())
    look={}
    prompts={}
    for t in tasks:
        ps=sorted(base.loc[base.task_type.eq(t),'prompt_id'].unique())
        prompts[t]=np.array(ps,dtype=object)
        for p in ps:
            look[(t,p)]=base.index[(base.task_type.eq(t)) & (base.prompt_id.eq(p))].to_numpy()
    out=[]
    for _ in range(reps):
        chunks=[]
        for t in tasks:
            sampled=rng.choice(prompts[t],size=len(prompts[t]),replace=True)
            chunks.extend(look[(t,p)] for p in sampled)
        out.append(np.concatenate(chunks))
    return out


def ci(v):
    return tuple(float(x) for x in np.quantile(np.asarray(v,float),[.025,.975]))


def main():
    a=parse_args(); ds=[read(a.a1),read(a.a2),read(a.a3)]
    keys=['case_id','prompt_id','task_type']
    for d in ds[1:]:
        if not ds[0][keys].equals(d[keys]): raise ValueError('A1/A2/A3 case/prompt/task alignment differs')
    base=ds[0][keys].copy(); boots=make_boot_indices(base,a.bootstrap_reps,a.seed)
    specs=[('Fine-grained primary label','primary_label',False),('Collapsed family','family',False),('Grounding boundary','boundary_zone',False),('Ordinal severity 0-3','severity_score',True)]
    rows=[]
    for dim,field,is_ord in specs:
        arr,levels=encode_three(ds,field); k=len(levels)
        for ia,ib,pair in PAIRS:
            x=arr[:,ia]; y=arr[:,ib]
            exact=float(np.mean(x==y))
            if is_ord:
                within=float(np.mean(np.abs(x-y)<=1))
                kap=cohen_kappa_codes(x,y,k,weights='quadratic')
            else:
                within=np.nan; kap=cohen_kappa_codes(x,y,k)
            be=[]; bw=[]; bk=[]
            for idx in boots:
                xb=x[idx]; yb=y[idx]
                be.append(float(np.mean(xb==yb)))
                if is_ord: bw.append(float(np.mean(np.abs(xb-yb)<=1)))
                bk.append(cohen_kappa_codes(xb,yb,k,weights='quadratic' if is_ord else None))
            e0,e1=ci(be); k0,k1=ci(bk)
            if is_ord: w0,w1=ci(bw)
            else: w0=w1=np.nan
            rows.append(dict(
                dimension=dim,pair=pair,N_cases=720,N_prompt_clusters=120,
                exact_agreement=exact,exact_ci_low=e0,exact_ci_high=e1,
                chance_corrected_metric='Quadratic_weighted_Cohen_kappa' if is_ord else 'Cohen_kappa',
                chance_corrected_value=kap,metric_ci_low=k0,metric_ci_high=k1,
                within_one_agreement=within,within_one_ci_low=w0,within_one_ci_high=w1,
                bootstrap=f'{a.bootstrap_reps} task-stratified Prompt_ID-cluster resamples; seed {a.seed}'))
    out=pd.DataFrame(rows)

    disagree=np.zeros(720,dtype=bool); field_counts={}
    for f in QUEUE_FIELDS:
        vals=[]
        for d in ds:
            if f=='secondary_label': vals.append(d[f].map(secondary).to_numpy(object))
            elif f=='severity_score': vals.append(d[f].astype(int).to_numpy())
            else: vals.append(d[f].map(txt).to_numpy(object))
        A=np.column_stack(vals)
        q=np.any(A != A[:,[0]],axis=1)
        field_counts[f]=int(q.sum()); disagree |= q
    qrows=[dict(rule='Any disagreement across at least one structured adjudication field',fields=';'.join(QUEUE_FIELDS),cases_flagged=int(disagree.sum()),cases_not_flagged=int((~disagree).sum()),total_cases=720,matches_documented_queue_423=bool(disagree.sum()==423),note='Evidence spans/notes, interpretive anchors, timestamps and free-text comments are not queue triggers.')]
    qrows += [dict(rule=f'Field-specific disagreement: {f}',fields=f,cases_flagged=n,cases_not_flagged=720-n,total_cases=720,matches_documented_queue_423='',note='Field-specific count; overlaps other trigger fields.') for f,n in field_counts.items()]
    queue=pd.DataFrame(qrows)
    if int(disagree.sum())!=423: raise AssertionError(f'Queue={int(disagree.sum())}, expected 423')

    a.out_dir.mkdir(parents=True,exist_ok=True)
    p1=a.out_dir/'P2_IPM_PAIR_SPECIFIC_HUMAN_RELIABILITY.csv'; p2=a.out_dir/'P2_IPM_ADJUDICATION_QUEUE_RULE_AUDIT.csv'
    out.to_csv(p1,index=False,float_format='%.9f'); queue.to_csv(p2,index=False)
    print(out.to_string(index=False)); print('\n'+queue.to_string(index=False)); print(f'\nWrote {p1}\nWrote {p2}')

if __name__=='__main__': main()
