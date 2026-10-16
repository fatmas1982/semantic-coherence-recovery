#!/usr/bin/env python3
"""Read-only strict E1/E2 archived-summary consistency checks; stdlib only.
Usage: python code/validity/verify_e1e2_judge_summary_20261017.py
Does NOT claim verification of the raw results.rar member cases or new inference.
"""
import csv, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'data/validity_2026_10/E1E2_DECISION_AND_MARGIN_DIAGNOSTICS.csv'
B=ROOT/'data/validity_2026_10/E1E2_DELTA_MACROF1_BOOTSTRAP_3000.csv'
D=ROOT/'results/validity_2026_10/E1E2_PAIRED_RECOMPUTED.csv'
def read(p):
    with p.open(newline='',encoding='utf-8-sig') as h:return list(csv.DictReader(h))
def key(x):return tuple(x[z] for z in ('judge','target','experiment','variant'))
def run():
    a,b=read(A),read(B)
    errs=[]; keys_a={key(x) for x in a};keys_b={key(x) for x in b}
    if len(a)!=20 or len(b)!=20:errs.append('expected 20 paired variant summaries in each file')
    if len(keys_a)!=len(a) or len(keys_b)!=len(b) or keys_a!=keys_b:errs.append('duplicate or unmatched experiment identities')
    bm={key(x):x for x in b}
    valid_ns={'T1':720,'T2':474,'T3':460,'T4':474}
    for r in a:
        k=key(r)
        if k not in bm:continue
        t=bm[k]
        n=int(r['n']);changed=int(r['changed_n'])
        if n!=valid_ns[r['target']] or int(t['n'])!=n:errs.append(f'{k}: target denominator')
        if not 0<=changed<=n:errs.append(f'{k}: invalid change count')
        if not math.isclose(float(r['changed_rate']),changed/n,rel_tol=0,abs_tol=1e-12):errs.append(f'{k}: change rate')
        if int(float(r['correct_to_wrong']))+int(float(r['wrong_to_correct']))+int(float(r['wrong_to_wrong_changed']))!=changed:errs.append(f'{k}: transition counts')
        if int(t['bootstrap_reps'])!=3000 or int(t['seed'])!=20261009:errs.append(f'{k}: bootstrap metadata')
        if not math.isclose(float(t['base_macroF1'])+float(t['delta_macroF1']),float(t['pert_macroF1']),rel_tol=0,abs_tol=1e-10):errs.append(f'{k}: macroF1 delta identity')
        if float(t['ci_low'])>float(t['ci_high']):errs.append(f'{k}: CI order')
    if D.exists():
        # Scope excludes numerical re-fitting of the 60 GEE tests.
        paired_rows=len(read(D))
    else:paired_rows=None
    output={'status':'FAIL' if errs else 'PASS_ARCHIVED_SUMMARY_ONLY','summary_rows':len(a),'bootstrap_rows':len(b),'paired_report_rows':paired_rows,
        'scope':'summary algebra and metadata, not case-level RAR replay, prompt invariance, CI resampling or inference',
        'errors':errs,'external_human_validation':'deferred'}
    print(json.dumps(output,indent=2))
    if errs:raise SystemExit(1)
if __name__=='__main__':run()
