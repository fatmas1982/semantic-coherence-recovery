#!/usr/bin/env python3
"""Recompute E1/E2 paired decision instability and macro-F1 from frozen cases.

No judge-model calls are made. Each of the 20 comparisons reuses the same case
population under the specified baseline and perturbation. Cluster bootstrap is
conditional on archived predictions and samples whole Prompt_ID groups.
"""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

KEYS=['judge','target','experiment','variant']

def load(path):
    files=sorted(Path(path).glob('paired_cases_part_*.csv'))
    if len(files)!=11:raise ValueError('Missing paired-case parts')
    all_cases=pd.concat([pd.read_csv(f) for f in files],ignore_index=True)
    if len(all_cases)!=10408:raise ValueError('Unexpected case count')
    return all_cases

def measure(frame,reps,seed):
    true=frame.gold_label.to_numpy(int)
    base=frame.pred_base.to_numpy(int)
    pert=frame.pred_pert.to_numpy(int)
    labels=sorted(set(true)|set(base)|set(pert))
    def f1(ii,vec):
        return f1_score(true[ii],vec[ii],labels=labels,
                        average='macro',zero_division=0)
    all_ix=np.arange(len(frame))
    f0=f1(all_ix,base);f1p=f1(all_ix,pert)
    pid=frame.prompt_id.to_numpy()
    members=[np.flatnonzero(pid==p) for p in pd.unique(pid)]
    rng=np.random.default_rng(seed)
    f1diff=[];change=[]
    for _ in range(reps):
        choice=rng.integers(0,len(members),size=len(members))
        ix=np.concatenate([members[k] for k in choice])
        f1diff.append(f1(ix,pert)-f1(ix,base))
        change.append(float(np.mean(base[ix]!=pert[ix])))
    change_mask=base!=pert
    correct0=base==true
    correct1=pert==true
    return dict(n=len(frame),n_prompt_clusters=len(members),
        changed_n=int(change_mask.sum()),changed_rate=float(change_mask.mean()),
        changed_ci_low=float(np.quantile(change,.025)),
        changed_ci_high=float(np.quantile(change,.975)),
        base_macroF1=float(f0),pert_macroF1=float(f1p),
        delta_macroF1=float(f1p-f0),
        delta_ci_low=float(np.quantile(f1diff,.025)),
        delta_ci_high=float(np.quantile(f1diff,.975)),
        correct_to_wrong=int(np.sum(correct0&~correct1)),
        wrong_to_correct=int(np.sum(~correct0&correct1)),
        wrong_to_wrong_changed=int(np.sum(~correct0&~correct1&change_mask)),
        median_baseline_margin_changed=float(frame.loc[change_mask,'margin_base'].median()),
        median_baseline_margin_unchanged=float(frame.loc[~change_mask,'margin_base'].median()),
        bootstrap_reps=reps,seed=seed)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--data-dir',default='data/validity_2026_10')
    ap.add_argument('--out',default='results/validity_2026_10')
    ap.add_argument('--bootstrap-reps',type=int,default=3000)
    ap.add_argument('--seed',type=int,default=20261009)
    args=ap.parse_args()
    df=load(args.data_dir)
    rows=[]
    for key,g in df.groupby(KEYS,sort=True):
        row=dict(zip(KEYS,key))
        row.update(measure(g,args.bootstrap_reps,args.seed))
        rows.append(row)
    if len(rows)!=20:raise ValueError('Expected 20 contrasts')
    dest=Path(args.out);dest.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(dest/'E1E2_PAIRED_RECOMPUTED.csv',index=False)
    print('20 paired comparisons,',len(df),'case-level rows.')

if __name__=='__main__':main()
