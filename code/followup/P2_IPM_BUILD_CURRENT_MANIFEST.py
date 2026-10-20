#!/usr/bin/env python3
"""Build SHA-256 manifest for the current IP&M follow-up/reproducibility layer.

Run from the repository or detached reviewer-safe snapshot root. The manifest
excludes itself, .git, Python caches, and newly reproduced output directories.
"""
from pathlib import Path
import hashlib, csv

ROOT=Path.cwd()
OUT=ROOT/'docs/IPM_CURRENT_REPRODUCIBILITY_MANIFEST_R8.csv'
EXCLUDE={OUT.resolve()}
EXCLUDE_TOP={'reproduced_ipm_followup','.git'}

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

def layer(rel):
    s=rel.as_posix()
    if s.endswith('.docx'): return 'manuscript'
    if s.endswith('.xlsx'): return 'review_data'
    if s.startswith('data/annotation/'): return 'locked_human_input'
    if s.startswith('data/computational/') or s.startswith('data/frozen/baseline_csv_mirror/'): return 'frozen_prediction_input'
    if s.startswith('data/'): return 'frozen_data_input'
    if s.startswith('code/'): return 'code'
    if s.startswith('results/'): return 'result'
    if s.startswith('docs/'): return 'governance_doc'
    if s.startswith('requirements-'): return 'environment'
    if s.startswith('README'): return 'governance_doc'
    return 'other'

def main():
    files=[]
    for p in ROOT.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(ROOT)
        if p.resolve() in EXCLUDE: continue
        if rel.parts and rel.parts[0] in EXCLUDE_TOP: continue
        if '__pycache__' in rel.parts or p.suffix=='.pyc': continue
        files.append(p)
    files.sort(key=lambda p:p.relative_to(ROOT).as_posix())
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['path','sha256','bytes','layer'])
        for p in files:
            rel=p.relative_to(ROOT)
            w.writerow([rel.as_posix(),sha256(p),p.stat().st_size,layer(rel)])
    print(f'Wrote {OUT} with {len(files)} entries')

if __name__=='__main__':
    main()
