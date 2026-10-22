#!/usr/bin/env python3
"""Verify current P2 GOLD ambiguity membership and locked pre-resolution severity alpha.
Run at repository root after: python UNPACK_RELEASE.py
Uses released CSV mirrors only; never loads the historical P2_45 adjudication layer.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
G = ROOT / 'data/publication/canonical_publication_dataset_720.csv'
R = ROOT / 'data/annotation/locked_core_ratings/locked_pre_resolution_core_ratings_wide.csv'

def ordinal_alpha(v):
    counts = np.bincount(v.ravel(), minlength=4).astype(float)
    d = np.zeros((4, 4))
    for a in range(4):
        for b in range(4):
            lo, hi = sorted((a, b))
            span = counts[lo:hi+1].sum() - (counts[lo]+counts[hi])/2
            d[a, b] = span**2
    pairs = np.concatenate((v[:,[0,1]],v[:,[0,2]],v[:,[1,2]]))
    do = np.mean(d[pairs[:,0], pairs[:,1]])
    n = counts.sum()
    de = sum(counts[a]*counts[b]*d[a,b] for a in range(4)
             for b in range(4) if a != b)/(n*(n-1))
    return 1 - do/de

def main():
    g = pd.read_csv(G, dtype={'Case_ID':str})
    r = pd.read_csv(R, dtype={'Case_ID':str})
    assert len(g)==len(r)==720 and g.Case_ID.is_unique and r.Case_ID.is_unique
    m = r.merge(g[['Case_ID','Prompt_ID','Final_Ambiguity_Flag']],
                on='Case_ID',validate='one_to_one')
    assert (m.Prompt_ID_x == m.Prompt_ID_y).all()
    flag = m.Final_Ambiguity_Flag.astype(str).str.lower().eq('yes').to_numpy()
    assert flag.sum()==35
    sev = m[[f'A{i}_Severity' for i in (1,2,3)]].to_numpy(int)
    majority = ((m[[f'A{i}_Primary' for i in (1,2,3)]]!='NONE').sum(axis=1)
                .to_numpy()>=2)
    cases = [('all',np.ones(len(m),bool),720,.783964731),
             ('flagged_current',flag,35,.003509792),
             ('unflagged_current',~flag,685,.798015486),
             ('majority_unflagged_current',majority & ~flag,426,.513154023)]
    for name,mask,n,alpha_target in cases:
        a=ordinal_alpha(sev[mask]);assert mask.sum()==n and abs(a-alpha_target)<1e-7
        x=sev[mask];exact=np.mean((x[:,0]==x[:,1])&(x[:,0]==x[:,2]))
        print(f'{name}: N={n} exact={exact:.6f} alpha={a:.9f} PASS')
    vals=g.assign(amb=g.Final_Ambiguity_Flag.eq('yes')).groupby('Task_Type')['amb'].sum().to_dict()
    expected={'explanation':21,'instruction_following':3,'multi_entity_context_tracking':5,
              'question_answering':0,'source_grounded_generation':5,'summarisation':1}
    assert vals==expected,(vals,expected)
    print('TASK COUNTS PASS',vals)

if __name__=='__main__':
    main()
