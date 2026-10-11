#!/usr/bin/env python3
"""Reproduce the 60 exploratory human-disagreement × judge-instability contrasts (2026-10-12 corrected-CI version).

Inputs: de-identified, frozen, paired case-level E1/E2 data. No LLM inference and
no additional human annotation. GEE = working independence with robust
Prompt_ID-clustered standard errors (the exact reported specification).
"""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

AXES = {'primary':'primary_disagree', 'boundary':'boundary_disagree',
        'severity':'severity_disagree'}
KEYS = ['judge','target','experiment','variant']

def read_parts(folder):
    files = sorted(Path(folder).glob('paired_cases_part_*.csv'))
    if len(files) != 11:
        raise RuntimeError(f'Expected 11 case parts; found {len(files)}')
    a = pd.concat([pd.read_csv(f, dtype={'case_id':str,'prompt_id':str})
                   for f in files], ignore_index=True)
    if len(a) != 10408: raise RuntimeError(f'Expected 10408 rows, got {len(a)}')
    if a.duplicated(KEYS+['case_id']).any(): raise ValueError('Duplicate case')
    return a

def rd(df, weights=None):
    w = df.gold_label.value_counts(normalize=True) if weights is None else weights
    numerator = denom = 0.
    for label, mass in w.items():
        part = df.loc[df.gold_label == label]
        g1 = part.loc[part.D == 1, 'changed']
        g0 = part.loc[part.D == 0, 'changed']
        if g1.empty or g0.empty: continue
        numerator += mass * (g1.mean()-g0.mean())
        denom += mass
    return numerator / denom if denom else float('nan')

def bootstrap_cluster(df, n=2500, seed=20261010):
    """Exact, vectorized Prompt_ID-cluster bootstrap with original class weights.

    Uses PCG64, one rng.integers(k,size=(n,k)) draw matrix, and first-occurrence
    cluster ordering. Unsupported class-by-arm strata are excluded and supported
    class weights renormalized for that replicate.
    """
    pids=list(pd.unique(df.prompt_id))
    labels=sorted(df.gold_label.unique())
    k=len(pids)
    count=np.zeros((k,len(labels),2),dtype=np.int32)
    yes=np.zeros_like(count)
    blocks=df.groupby(['prompt_id','gold_label','D'],sort=False)['changed'].agg(['size','sum'])
    pmap={p:i for i,p in enumerate(pids)}
    cmap={c:i for i,c in enumerate(labels)}
    for (pid,cl,z),a in blocks.iterrows():
        i=pmap[pid];j=cmap[cl]
        count[i,j,int(z)]=int(a['size'])
        yes[i,j,int(z)]=int(a['sum'])
    masses=np.asarray([np.mean(df.gold_label==c) for c in labels])
    rng=np.random.default_rng(seed)
    idx=rng.integers(k,size=(n,k))
    C=count[idx].sum(axis=1); Y=yes[idx].sum(axis=1)
    risk=np.divide(Y,C,out=np.full(Y.shape,np.nan,dtype=float),where=C>0)
    eligible=np.isfinite(risk).all(axis=2)
    weights=eligible*masses[None,:]
    diff=np.nan_to_num(risk[:,:,1]-risk[:,:,0],nan=0)
    wsum=weights.sum(axis=1)
    val=np.divide((weights*diff).sum(axis=1),wsum,
                  out=np.full(n,np.nan),where=wsum>0)
    val=val[np.isfinite(val)]
    return (float(np.quantile(val,.025)),float(np.quantile(val,.975)),len(val))

def one_contrast(df, axis, n, seed):
    df = df.copy()
    df['D'] = df[AXES[axis]].astype(int)
    d1 = df.loc[df.D == 1,'changed']
    d0 = df.loc[df.D == 0,'changed']
    out = dict(human_axis=axis, n_cases=len(df),
               n_prompt_clusters=df.prompt_id.nunique(),
               disagree_n=len(d1),agree_n=len(d0),
               disagree_change_n=int(d1.sum()),agree_change_n=int(d0.sum()),
               unadjusted_RD=float(d1.mean()-d0.mean()),
               class_standardized_RD=float(rd(df)))
    lo,hi,nvalid = bootstrap_cluster(df,n,seed)
    out.update(class_adjusted_bootstrap_low=lo,
               class_adjusted_bootstrap_high=hi,bootstrap_valid=nvalid)
    x = pd.get_dummies(
        df[['D','gold_label','generator_id']].astype(
            {'gold_label':'category','generator_id':'category'}),
        columns=['gold_label','generator_id'],drop_first=True,dtype=float)
    x = sm.add_constant(x.astype(float))
    fit = sm.GEE(df.changed.astype(float),x,groups=df.prompt_id,
                 family=sm.families.Binomial(),
                 cov_struct=sm.cov_struct.Independence()).fit(maxiter=150)
    out.update(gee_logodds=float(fit.params['D']),
               gee_adjusted_OR=float(np.exp(fit.params['D'])),
               gee_p_unadjusted=float(fit.pvalues['D']),
               gee_converged=bool(fit.converged))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data-dir',default='data/validity_2026_10')
    ap.add_argument('--out',default='results/validity_2026_10')
    ap.add_argument('--bootstrap-reps',type=int,default=2500)
    ap.add_argument('--seed',type=int,default=20261010)
    args=ap.parse_args()
    frame=read_parts(args.data_dir)
    out=[]
    for keys,g in frame.groupby(KEYS,sort=True):
        for axis in AXES:
            row=dict(zip(KEYS,keys))
            row.update(one_contrast(g,axis,args.bootstrap_reps,args.seed))
            out.append(row)
    t=pd.DataFrame(out)
    if len(t)!=60: raise AssertionError(len(t))
    p=t.gee_p_unadjusted.to_numpy()
    t['gee_Holm_p_60']=multipletests(p,method='holm')[1]
    t['gee_BH_FDR_q_60']=multipletests(p,method='fdr_bh')[1]
    dest=Path(args.out); dest.mkdir(parents=True,exist_ok=True)
    t.to_csv(dest/'CLASS_ADJUSTED_HUMAN_JUDGE_60_CORRECTED_CI_20261010.csv',index=False)
    print(f'{len(t)} exploratory tests; Holm discoveries: {(t.gee_Holm_p_60 < .05).sum()}')

if __name__ == '__main__': main()
