#!/usr/bin/env python3
"""Verify exact (within 1e-8) 60-contrast reproduction of the 2026-10-12 release."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
KEYS=['judge','target','experiment','variant','human_axis']
FIELDS=['class_standardized_RD','class_adjusted_bootstrap_low','class_adjusted_bootstrap_high',
        'gee_adjusted_OR','gee_p_unadjusted','gee_Holm_p_60','gee_BH_FDR_q_60']
def run(reference,computed):
    a=pd.read_csv(reference);b=pd.read_csv(computed)
    if len(a)!=60 or len(b)!=60: raise AssertionError('Expected exactly 60 contrasts')
    x=a.merge(b,on=KEYS,suffixes=('_ref','_new'),validate='one_to_one')
    for col in FIELDS:
        diff=(x[col+'_ref'].astype(float)-x[col+'_new'].astype(float)).abs().max()
        print(col,': max |delta| =',diff)
        if diff>1e-8: raise AssertionError(f'{col} mismatch: {diff}')
    print('PASS: 60/60 reproducibility records verified')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--reference',type=Path,default=Path('data/validity_2026_10/HJI_60_CORRECTED_CI_SEED_20261010.csv'))
    p.add_argument('--computed',type=Path,default=Path('results/validity_2026_10/CLASS_ADJUSTED_HUMAN_JUDGE_60_CORRECTED_CI_20261010.csv'))
    x=p.parse_args();run(x.reference,x.computed)
