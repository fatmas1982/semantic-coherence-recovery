#!/usr/bin/env python3
"""Post-hoc adjudication-instability exclusion sensitivity for the IP&M submission.

Re-scores frozen M3 Condition-C and archived M4 P1/identity predictions after
excluding the 29 cases selected for targeted same-adjudicator re-review.
No model is retrained and FINAL GOLD v1.0 is not changed.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, cohen_kappa_score

TARGETED_CASES = {
    'CASE_0123','CASE_0243','CASE_0249','CASE_0252','CASE_0258','CASE_0264',
    'CASE_0282','CASE_0291','CASE_0297','CASE_0301','CASE_0303','CASE_0306',
    'CASE_0307','CASE_0309','CASE_0315','CASE_0318','CASE_0324','CASE_0327',
    'CASE_0330','CASE_0333','CASE_0354','CASE_0357','CASE_0431','CASE_0476',
    'CASE_0525','CASE_0567','CASE_0582','CASE_0661','CASE_0681'
}

def cluster_ci(df, pred_col, metric='f1', reps=2000, seed=20260908):
    groups={k:g.index.to_numpy() for k,g in df.groupby('Prompt_ID',sort=False)}
    pids=np.array(list(groups),dtype=object)
    rng=np.random.default_rng(seed)
    vals=[]
    for _ in range(reps):
        idx=np.concatenate([groups[p] for p in rng.choice(pids,size=len(pids),replace=True)])
        y=df.loc[idx,'y_true'].astype(int).to_numpy()
        p=df.loc[idx,pred_col].astype(int).to_numpy()
        if metric=='qwk':
            vals.append(cohen_kappa_score(y,p,weights='quadratic'))
        else:
            vals.append(f1_score(y,p,average='macro',zero_division=0))
    return np.quantile(vals,[.025,.975]).tolist()

def summarize(df,pred_col,target,model):
    df=df.copy()
    df['y_true']=df['y_true'].astype(int)
    df[pred_col]=df[pred_col].astype(int)
    keep=df.loc[~df['Case_ID'].astype(str).isin(TARGETED_CASES)].copy()
    full=f1_score(df.y_true,df[pred_col],average='macro',zero_division=0)
    excl=f1_score(keep.y_true,keep[pred_col],average='macro',zero_division=0)
    lo,hi=cluster_ci(keep,pred_col)
    row=dict(target=target,model=model,n_full=len(df),n_retained=len(keep),
             n_removed=len(df)-len(keep),full_macro_f1=full,
             exclusion_macro_f1=excl,delta=excl-full,
             exclusion_ci_low=lo,exclusion_ci_high=hi)
    if target=='T4':
        fq=cohen_kappa_score(df.y_true,df[pred_col],weights='quadratic')
        eq=cohen_kappa_score(keep.y_true,keep[pred_col],weights='quadratic')
        qlo,qhi=cluster_ci(keep,pred_col,metric='qwk')
        row.update(full_qwk=fq,exclusion_qwk=eq,qwk_delta=eq-fq,
                   qwk_ci_low=qlo,qwk_ci_high=qhi)
    return row

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--m3-dir',required=True,type=Path,
                    help='Directory containing OOF_M3_T*_C_seed20260908.csv')
    ap.add_argument('--m4-dir',required=True,type=Path,
                    help='Directory containing OOF_M4_SENS_T*_P1_identity.csv')
    ap.add_argument('--out',required=True,type=Path)
    a=ap.parse_args()
    rows=[]
    for t in ['T1','T2','T3','T4']:
        m3=pd.read_csv(a.m3_dir/f'OOF_M3_{t}_C_seed20260908.csv')
        m4=pd.read_csv(a.m4_dir/f'OOF_M4_SENS_{t}_P1_identity.csv')
        rows.append(summarize(m3,'M3_pred',t,'M3'))
        rows.append(summarize(m4,'M4_pred',t,'M4'))
    out=pd.DataFrame(rows)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    out.to_csv(a.out,index=False)
    print(out.to_string(index=False))

if __name__=='__main__':
    main()
