#!/usr/bin/env python3
"""Reproduce the deterministic qualitative M3 error audit reported in Supplement Table S44B.

Selection rule (fixed before qualitative interpretation):
for each target T1-T4 and each Human_Easy stratum {1,0}, restrict the primary
Condition-C OOF file (seed 20260908) to misclassified cases; select the case with
maximum predicted-class probability; break exact probability ties by ascending
Case_ID. The script reports identifiers, task, gold/predicted label, and confidence.
Narrative interpretation remains human-authored and is not produced by this script.
"""
from pathlib import Path
import ast, json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SEED = 20260908
TARGETS = ["T1","T2","T3","T4"]
LABEL_NAMES = {
    "T1": {0:"no_failure",1:"failure"},
    "T2": {0:"semantic_only",1:"grounding_involved"},
    "T3": {0:"Core_SCF",1:"OVR"},
    "T4": {1:"severity 1",2:"severity 2",3:"severity 3"},
}

def first_named(name):
    hits = list(ROOT.rglob(name))
    if not hits:
        raise FileNotFoundError(name)
    return hits[0]

def parse_probs(v):
    if isinstance(v, (list,tuple)):
        return [float(x) for x in v]
    s=str(v)
    try:
        x=json.loads(s)
    except Exception:
        x=ast.literal_eval(s)
    return [float(z) for z in x]

rows=[]
for target in TARGETS:
    p=first_named(f"OOF_M3_{target}_C_seed{SEED}.csv")
    d=pd.read_csv(p)
    required={"Case_ID","Task_Type","y_true","M3_pred","M3_probs","Human_Easy"}
    missing=required-set(d.columns)
    if missing:
        raise ValueError(f"{p}: missing {sorted(missing)}")
    labels=sorted(int(x) for x in d.y_true.unique())
    for human_easy,stratum in [(1,"easy"),(0,"hard")]:
        z=d[(d.Human_Easy.astype(int)==human_easy) &
            (d.y_true.astype(int)!=d.M3_pred.astype(int))].copy()
        if z.empty:
            raise ValueError(f"No error case for {target}/{stratum}")
        conf=[]
        for _,r in z.iterrows():
            probs=parse_probs(r.M3_probs)
            pred=int(r.M3_pred)
            conf.append(probs[labels.index(pred)])
        z["predicted_class_probability"]=conf
        z=z.sort_values(["predicted_class_probability","Case_ID"],
                        ascending=[False,True],kind="mergesort")
        r=z.iloc[0]
        yt,yp=int(r.y_true),int(r.M3_pred)
        rows.append({
            "target":target,
            "human_stratum":stratum,
            "Case_ID":str(r.Case_ID),
            "Task_Type":str(r.Task_Type),
            "gold_label":LABEL_NAMES[target][yt],
            "M3_pred_label":LABEL_NAMES[target][yp],
            "predicted_class_probability":float(r.predicted_class_probability),
            "selection_rule":"highest-confidence misclassified primary-seed Condition-C case within target x Human_Easy stratum; Case_ID ascending tie-break",
        })

out=pd.DataFrame(rows)
dest=ROOT/"results/followup/P2_IPM_R14_DETERMINISTIC_ERROR_AUDIT.csv"
dest.parent.mkdir(parents=True,exist_ok=True)
out.to_csv(dest,index=False)
print(out.to_string(index=False))
print("Wrote",dest)
