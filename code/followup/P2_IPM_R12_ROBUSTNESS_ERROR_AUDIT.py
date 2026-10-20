#!/usr/bin/env python3
"""Reproduce R12/R14 robustness class diagnostics and deterministic M3 error selection.

This post-hoc reporting audit uses frozen artifacts only. It does not retrain models,
change FINAL GOLD, alter folds, or select a favourable protocol.
"""
from __future__ import annotations
import argparse, re
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

TARGETS=["T1","T2","T3","T4"]
SEEDS=[20260908,20260909,20260910]

def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument("--gold",type=Path,default=Path("data/frozen/P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx"))
    p.add_argument("--root",type=Path,default=Path("."))
    p.add_argument("--out-dir",type=Path,default=Path("results/followup"))
    return p.parse_args()

def find_one(root,name):
    hits=list(root.rglob(name))
    if len(hits)!=1:
        raise FileNotFoundError(f"Expected exactly one {name}; found {len(hits)}")
    return hits[0]

def eligible(g,target):
    d=g.copy()
    if target=="T1":
        d["y_true"]=d["Any_Failure"].astype(int); return d
    if target=="T2":
        d=d[d["Any_Failure"].astype(int).eq(1)].copy()
        d["y_true"]=np.where(d["Final_Boundary"].eq("semantic_only"),0,1); return d
    if target=="T3":
        d=d[d["Final_Family"].isin(["Core SCF","OVR"])].copy()
        d["y_true"]=d["Final_Family"].map({"Core SCF":0,"OVR":1}).astype(int); return d
    if target=="T4":
        d=d[d["Any_Failure"].astype(int).eq(1)].copy()
        d["y_true"]=d["Final_Severity"].astype(int); return d
    raise ValueError(target)

def rater_value(r,target,a):
    primary=str(r[f"{a}_Primary"]).strip()
    boundary=str(r[f"{a}_Boundary"]).strip()
    sev=int(r[f"{a}_Severity"]) if pd.notna(r[f"{a}_Severity"]) else -1
    if target=="T1": return 0 if primary.upper()=="NONE" else 1
    if target=="T2":
        if boundary=="semantic_only": return 0
        if boundary in {"overlap","hallucination_only"}: return 1
        return -1
    if target=="T3":
        if primary.startswith("SCF-"): return 0
        if primary.startswith("OVR-"): return 1
        return -1
    if target=="T4": return sev if sev in {1,2,3} else -1
    raise ValueError(target)

def pred_col(d):
    for c in ["M3_pred","pred","prediction","y_pred"]:
        if c in d.columns: return c
    raise KeyError("Prediction column not found")

def prob_cols(d):
    a=[c for c in d.columns if re.match(r"^(?:prob|p)[_-]?\d+$",str(c),re.I)]
    return a or [c for c in d.columns if str(c).lower().startswith(("prob_","class_prob_"))]

def labels(target):
    return {"T1":[0,1],"T2":[0,1],"T3":[0,1],"T4":[1,2,3]}[target]

def main():
    a=parse_args(); a.out_dir.mkdir(parents=True,exist_ok=True)
    gold=pd.read_excel(a.gold,sheet_name="FINAL_GOLD")
    class_rows=[]; selected=[]
    for target in TARGETS:
        base=eligible(gold,target)
        base["human_stratum"]=base.apply(
            lambda r:"easy" if len({rater_value(r,target,x) for x in ["A1","A2","A3"]})==1 else "hard",axis=1)
        frames={}
        for seed in SEEDS:
            p=find_one(a.root,f"OOF_M3_{target}_C_seed{seed}.csv")
            x=pd.read_csv(p); pc=pred_col(x); probs=prob_cols(x)
            x=x[["Case_ID",pc]+probs].rename(columns={pc:"pred"})
            x["pred"]=x["pred"].astype(int)
            frames[seed]=base[["Case_ID","Prompt_ID","Task_Type","y_true","human_stratum"]].merge(x,on="Case_ID",validate="one_to_one")
        labs=labels(target); per={}
        for seed,d in frames.items():
            pr,rc,f1,sup=precision_recall_fscore_support(d.y_true,d.pred,labels=labs,zero_division=0)
            per[seed]={lab:(pr[i],rc[i],f1[i],sup[i]) for i,lab in enumerate(labs)}
        primary=frames[SEEDS[0]]; counts=primary.pred.value_counts()
        for lab in labs:
            pr,rc,f1,sup=per[SEEDS[0]][lab]; fs=[per[s][lab][2] for s in SEEDS]
            class_rows.append(dict(target=target,class_label=lab,gold_n=int(sup),pred_n=int(counts.get(lab,0)),
                precision=pr,recall=rc,primary_f1=f1,seed_f1_min=min(fs),seed_f1_max=max(fs)))
        probs=prob_cols(primary)
        pmap={}
        for c in probs:
            m=re.search(r"(\d+)$",c)
            if m: pmap[int(m.group(1))]=c
        if not pmap: raise KeyError(f"{target}: probability columns required")
        primary=primary.copy()
        primary["pred_confidence"]=primary.apply(lambda r:float(r[pmap[int(r.pred)]]) if int(r.pred) in pmap else np.nan,axis=1)
        for stratum in ["easy","hard"]:
            e=primary[(primary.human_stratum==stratum)&(primary.y_true!=primary.pred)&primary.pred_confidence.notna()].copy()
            e=e.sort_values(["pred_confidence","Case_ID"],ascending=[False,True])
            if len(e):
                r=e.iloc[0]
                selected.append(dict(target=target,human_stratum=stratum,Case_ID=r.Case_ID,Task_Type=r.Task_Type,
                    gold=int(r.y_true),pred=int(r.pred),pred_confidence=float(r.pred_confidence),
                    selection_rule="highest predicted-class probability among primary-seed errors within target x stratum; Case_ID tie-break"))
    pd.DataFrame(class_rows).to_csv(a.out_dir/"P2_IPM_R12_M3_CLASS_DIAGNOSTICS.csv",index=False,float_format="%.9f")
    pd.DataFrame(selected).to_csv(a.out_dir/"P2_IPM_R12_DETERMINISTIC_ERROR_SELECTION.csv",index=False,float_format="%.9f")

if __name__=="__main__":
    main()
