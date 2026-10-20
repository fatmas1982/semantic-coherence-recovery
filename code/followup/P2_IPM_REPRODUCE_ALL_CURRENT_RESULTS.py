#!/usr/bin/env python3
"""Run the current IP&M R1–R8 follow-up reproducibility/verification checks.

Default mode is reviewer-safe and CPU-only. It recomputes all lightweight follow-up
analyses from the frozen row-level inputs and verifies the archived 2,000-replicate
statistical-design sensitivity artifact plus an independently recomputed fold/class
audit. The statistical-design script itself remains included for full regeneration;
pass --recompute-statistical-bootstrap to run that slower 2,000-replicate audit.

No command in this orchestrator retrains M3/M4 or changes FINAL GOLD.

Usage after UNPACK_RELEASE.py from repository root:
    python code/followup/P2_IPM_REPRODUCE_ALL_CURRENT_RESULTS.py

Optional full slow resampling:
    python code/followup/P2_IPM_REPRODUCE_ALL_CURRENT_RESULTS.py \
        --recompute-statistical-bootstrap \
        --recompute-slow-ci-followups
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "reproduced_ipm_followup"
OUT.mkdir(exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--recompute-statistical-bootstrap", action="store_true",
                   help="Run the full 2,000-replicate statistical-design bootstrap instead of verifying the archived frozen sensitivity CSV.")
    p.add_argument("--recompute-slow-ci-followups", action="store_true",
                   help="Also rerun the slower 2,000-replicate adjudication-exclusion and human-reference CI scripts instead of point-estimate verification of their archived outputs.")
    return p.parse_args()


def first(pattern):
    hits = sorted(ROOT.glob(pattern))
    if not hits:
        hits = sorted(ROOT.rglob(Path(pattern).name))
    if not hits:
        raise FileNotFoundError(pattern)
    return hits[0]


def run(cmd):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run([str(x) for x in cmd], check=True)


def py(script, *args):
    run([sys.executable, script, *args])


def check_csv(path, key_cols, expectations, tol=2e-6):
    import pandas as pd
    d = pd.read_csv(path)
    for keys, col, exp in expectations:
        q = d
        for k, v in zip(key_cols, keys):
            q = q[q[k].astype(str) == str(v)]
        if len(q) != 1:
            raise AssertionError(f"{path}: expected one row for {keys}, found {len(q)}")
        obs = float(q.iloc[0][col])
        if abs(obs - exp) > tol:
            raise AssertionError(f"{path}: {keys} {col}={obs}, expected {exp}")
    print("PASS", path, flush=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_archived_statistical_design(m3_dir, archived_dir):
    """Verify the frozen R5 statistical-design artifact and recompute fold support."""
    import pandas as pd
    archived = archived_dir / "P2_IPM_TASK_STRATIFIED_COMPUTATIONAL_BOOTSTRAP_SENSITIVITY.csv"
    fold_archived = archived_dir / "P2_IPM_FOLD_BY_CLASS_AUDIT.csv"
    if not archived.exists() or not fold_archived.exists():
        raise FileNotFoundError("Archived statistical-design result files are missing")

    d = pd.read_csv(archived)
    if len(d) != 49:
        raise AssertionError(f"Expected 49 archived interval rows, found {len(d)}")
    if d["zero_inclusion_changed"].astype(str).str.lower().eq("true").any():
        raise AssertionError("Archived task-stratified sensitivity contains a zero-inclusion change")
    max_shift = float(d["max_endpoint_shift"].max())
    if abs(max_shift - 0.013079380282429554) > 2e-9:
        raise AssertionError(f"Archived max endpoint shift {max_shift} differs from frozen value")

    labels = {"T1": [0, 1], "T2": [0, 1], "T3": [0, 1], "T4": [1, 2, 3]}
    rows = []
    for t in ("T1", "T2", "T3", "T4"):
        f = m3_dir / f"OOF_M3_{t}_C_seed20260908.csv"
        x = pd.read_csv(f)
        for fold, s in x.groupby("Fold", sort=True):
            vc = s["y_true"].value_counts().to_dict()
            rec = {"target": t, "fold": int(fold), "rows": len(s),
                   "prompt_clusters": s["Prompt_ID"].nunique(),
                   "class_0_n": vc.get(0, ""), "class_1_n": vc.get(1, ""),
                   "class_2_n": vc.get(2, ""), "class_3_n": vc.get(3, "")}
            rec["min_class_n"] = min(int(vc.get(k, 0)) for k in labels[t])
            rows.append(rec)
    fd = pd.DataFrame(rows)
    out_dir = OUT / "statistical_design"
    out_dir.mkdir(exist_ok=True)
    fd.to_csv(out_dir / "P2_IPM_FOLD_BY_CLASS_AUDIT.csv", index=False)
    if int(fd["min_class_n"].min()) != 11:
        raise AssertionError("Fold-by-class audit minimum differs from 11")

    frozen_fd = pd.read_csv(fold_archived)
    cols = ["target", "fold", "rows", "prompt_clusters", "class_0_n", "class_1_n", "class_2_n", "class_3_n", "min_class_n"]
    aa = fd[cols].copy().reset_index(drop=True)
    bb = frozen_fd[cols].copy().reset_index(drop=True)
    for c in ["fold", "rows", "prompt_clusters", "class_0_n", "class_1_n", "class_2_n", "class_3_n", "min_class_n"]:
        aa[c] = pd.to_numeric(aa[c], errors="coerce").fillna(-1).astype(int)
        bb[c] = pd.to_numeric(bb[c], errors="coerce").fillna(-1).astype(int)
    aa["target"] = aa["target"].astype(str)
    bb["target"] = bb["target"].astype(str)
    if not aa.equals(bb):
        raise AssertionError("Recomputed fold-by-class audit differs from archived R5 audit")

    verification = {
        "status": "PASS",
        "archived_bootstrap_rows": len(d),
        "archived_bootstrap_sha256": sha256(archived),
        "max_endpoint_shift": max_shift,
        "zero_inclusion_changes": 0,
        "recomputed_min_fold_class_n": 11,
        "note": "Default path verifies the manuscript-used frozen 2,000-replicate sensitivity artifact and independently recomputes fold/class support. Use --recompute-statistical-bootstrap for full slow regeneration."
    }
    (out_dir / "P2_IPM_STATISTICAL_DESIGN_VERIFICATION.json").write_text(json.dumps(verification, indent=2), encoding="utf-8")
    print("PASS archived 2,000-replicate statistical-design sensitivity + recomputed fold audit", flush=True)


def main():
    a = parse_args()
    a1 = first("data/annotation/historical_full_csv/A1/Annotation.csv")
    a2 = first("data/annotation/historical_full_csv/A2/Annotation.csv")
    a3 = first("data/annotation/historical_full_csv/A3/Annotation.csv")
    gold = first("data/frozen/P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx")
    m3_t1 = first("OOF_M3_T1_C_seed20260908.csv")
    m3_dir = m3_t1.parent
    m4_t1 = first("OOF_M4_SENS_T1_P1_identity.csv")
    m4_dir = m4_t1.parent
    baseline = first("data/frozen/baseline_csv_mirror/OOF_T1.csv").parent
    archived_dir = ROOT / "results/followup"

    amb = OUT / "P2_IPM_AMBIGUITY_EXCLUSION_SENSITIVITY.csv"
    py(ROOT / "code/followup/P2_IPM_AMBIGUITY_EXCLUSION_SENSITIVITY.py",
       "--a1", a1, "--a2", a2, "--a3", a3, "--out", amb)
    check_csv(amb, ["analysis", "subset"], [
        (("Fine labels", "All cases"), "alpha", 0.703147),
        (("Fine labels", "Non-ambiguous"), "alpha", 0.713285),
        (("Ordinal severity", "Majority-failure subset"), "alpha", 0.528338),
        (("Ordinal severity", "Majority-failure excluding explicit ambiguity"), "alpha", 0.532075),
    ])

    pair_dir = OUT / "pair_specific"
    pair_dir.mkdir(exist_ok=True)
    py(ROOT / "code/followup/P2_IPM_PAIR_SPECIFIC_HUMAN_RELIABILITY.py",
       "--a1", a1, "--a2", a2, "--a3", a3, "--out-dir", pair_dir)
    check_csv(pair_dir / "P2_IPM_PAIR_SPECIFIC_HUMAN_RELIABILITY.csv", ["dimension", "pair"], [
        (("Fine-grained primary label", "A1-A2"), "chance_corrected_value", 0.733765417),
        (("Fine-grained primary label", "A2-A3"), "chance_corrected_value", 0.660566120),
        (("Ordinal severity 0-3", "A2-A3"), "chance_corrected_value", 0.856108909),
    ])
    with open(pair_dir / "P2_IPM_ADJUDICATION_QUEUE_RULE_AUDIT.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if int(rows[0]["cases_flagged"]) != 423:
        raise AssertionError("Adjudication queue did not reproduce 423 cases")
    print("PASS 423-case adjudication queue", flush=True)

    sem_dir = OUT / "computational_semantics"
    sem_dir.mkdir(exist_ok=True)
    py(ROOT / "code/followup/P2_IPM_COMPUTATIONAL_SEMANTICS_STRUCTURE_DIAGNOSTICS.py",
       "--gold", gold, "--out-dir", sem_dir)
    check_csv(sem_dir / "P2_IPM_COMPUTATIONAL_SEMANTICS_ASSOCIATION_SUMMARY.csv", ["analysis"], [
        (("T3 family x grounding status",), "cramers_v", 0.728143),
        (("Task x mechanism family",), "cramers_v", 0.251135),
    ], tol=5e-6)

    if a.recompute_statistical_bootstrap:
        stat_dir = OUT / "statistical_design"
        stat_dir.mkdir(exist_ok=True)
        py(ROOT / "code/followup/P2_IPM_STATISTICAL_DESIGN_SENSITIVITY.py",
           "--baseline-dir", baseline, "--m3-dir", m3_dir, "--m4-dir", m4_dir, "--out-dir", stat_dir)
        import pandas as pd
        ss = pd.read_csv(stat_dir / "P2_IPM_TASK_STRATIFIED_COMPUTATIONAL_BOOTSTRAP_SUMMARY.csv")
        if int(ss["zero_inclusion_changes"].sum()) != 0 or float(ss["max_endpoint_shift"].max()) > 0.014:
            raise AssertionError("Regenerated task-stratified bootstrap sensitivity differs materially from frozen audit")
        print("PASS full statistical-design bootstrap regeneration", flush=True)
    else:
        verify_archived_statistical_design(m3_dir, archived_dir)

    import pandas as pd
    import numpy as np
    if a.recompute_slow_ci_followups:
        adj = OUT / "P2_IPM_ADJUDICATION_INSTABILITY_EXCLUSION_SENSITIVITY.csv"
        py(ROOT / "code/followup/P2_IPM_ADJUDICATION_INSTABILITY_EXCLUSION_SENSITIVITY.py",
           "--m3-dir", m3_dir, "--m4-dir", m4_dir, "--out", adj)
        d = pd.read_csv(adj)
        if float(d["delta"].abs().max()) > 0.013:
            raise AssertionError("Unexpectedly large adjudication-exclusion shift")
        print("PASS full adjudication-instability exclusion CI regeneration", flush=True)

        hc = OUT / "P2_IPM_HUMAN_REFERENCE_TARGET_CONCORDANCE.csv"
        py(ROOT / "code/followup/P2_IPM_HUMAN_REFERENCE_TARGET_CONCORDANCE.py",
           "--a1", a1, "--a2", a2, "--a3", a3, "--gold", gold, "--out", hc)
        h = pd.read_csv(hc)
    else:
        from sklearn.metrics import f1_score, cohen_kappa_score
        target_cases = {
            'CASE_0123','CASE_0243','CASE_0249','CASE_0252','CASE_0258','CASE_0264',
            'CASE_0282','CASE_0291','CASE_0297','CASE_0301','CASE_0303','CASE_0306',
            'CASE_0307','CASE_0309','CASE_0315','CASE_0318','CASE_0324','CASE_0327',
            'CASE_0330','CASE_0333','CASE_0354','CASE_0357','CASE_0431','CASE_0476',
            'CASE_0525','CASE_0567','CASE_0582','CASE_0661','CASE_0681'
        }
        archived_adj = pd.read_csv(archived_dir / "P2_IPM_ADJUDICATION_INSTABILITY_EXCLUSION_SENSITIVITY.csv")
        recomputed = []
        for t in ["T1","T2","T3","T4"]:
            for model, path, pcol in [
                ("M3", m3_dir / f"OOF_M3_{t}_C_seed20260908.csv", "M3_pred"),
                ("M4", m4_dir / f"OOF_M4_SENS_{t}_P1_identity.csv", "M4_pred"),
            ]:
                x = pd.read_csv(path).copy()
                x["y_true"] = x["y_true"].astype(int); x[pcol] = x[pcol].astype(int)
                keep = x.loc[~x["Case_ID"].astype(str).isin(target_cases)].copy()
                labels = [0,1] if t != "T4" else [1,2,3]
                full = f1_score(x.y_true, x[pcol], labels=labels, average="macro", zero_division=0)
                excl = f1_score(keep.y_true, keep[pcol], labels=labels, average="macro", zero_division=0)
                rec = dict(target=t, model=model, n_full=len(x), n_retained=len(keep), full_macro_f1=full, exclusion_macro_f1=excl, delta=excl-full)
                if t == "T4":
                    rec["full_qwk"] = cohen_kappa_score(x.y_true, x[pcol], labels=[1,2,3], weights="quadratic")
                    rec["exclusion_qwk"] = cohen_kappa_score(keep.y_true, keep[pcol], labels=[1,2,3], weights="quadratic")
                recomputed.append(rec)
        rp = pd.DataFrame(recomputed)
        chk = rp.merge(archived_adj, on=["target","model"], suffixes=("_re","_ar"))
        for c in ["n_full","n_retained","full_macro_f1","exclusion_macro_f1","delta"]:
            if c.startswith("n_"):
                if not (chk[c+"_re"].astype(int) == chk[c+"_ar"].astype(int)).all(): raise AssertionError(f"Adjudication point check failed: {c}")
            else:
                if float((chk[c+"_re"]-chk[c+"_ar"]).abs().max()) > 2e-6: raise AssertionError(f"Adjudication point check failed: {c}")
        if float(archived_adj["delta"].abs().max()) > 0.013:
            raise AssertionError("Archived adjudication-exclusion shift differs from frozen boundary")
        out_adj = OUT / "adjudication_exclusion"; out_adj.mkdir(exist_ok=True)
        rp.to_csv(out_adj / "P2_IPM_ADJUDICATION_EXCLUSION_POINT_VERIFICATION.csv", index=False)
        print("PASS archived adjudication-exclusion CIs + recomputed point estimates", flush=True)

        gold_df = pd.read_excel(gold, sheet_name="FINAL_GOLD")
        def fam(v):
            v=str(v).strip().upper()
            if v.startswith("SCF-"): return "Core SCF"
            if v.startswith("OVR-"): return "OVR"
            return v if v in {"HREF","NONE"} else "OTHER"
        rows=[]
        for _,r in gold_df.iterrows():
            z={"Prompt_ID":str(r.Prompt_ID),"gold_T1":int(r.Any_Failure),"gold_boundary":str(r.Final_Boundary),"gold_family":str(r.Final_Family),"gold_severity":int(r.Final_Severity)}
            for aa in ["A1","A2","A3"]:
                p=str(r[f"{aa}_Primary"]).strip().upper(); b=str(r[f"{aa}_Boundary"]).strip().lower(); sev=int(r[f"{aa}_Severity"])
                z.update({f"{aa}_T1":0 if p=="NONE" else 1,f"{aa}_boundary":b,f"{aa}_family":fam(p),f"{aa}_severity":sev})
            rows.append(z)
        zdf=pd.DataFrame(rows)
        targets={
            "T1":zdf.assign(y=zdf.gold_T1),
            "T2":zdf[zdf.gold_T1==1].assign(y=lambda q:(q.gold_boundary!="semantic_only").astype(int)),
            "T3":zdf[zdf.gold_family.isin(["Core SCF","OVR"])].assign(y=lambda q:(q.gold_family=="OVR").astype(int)),
            "T4":zdf[zdf.gold_T1==1].assign(y=lambda q:q.gold_severity.astype(int)),
        }
        def macro(y,p,labels):
            return float(f1_score(y,p,labels=labels,average="macro",zero_division=0))
        point_rows=[]
        for t,sub in targets.items():
            y=sub.y.astype(int).to_numpy(); labels=[0,1] if t!="T4" else [1,2,3]
            for aa in ["A1","A2","A3"]:
                if t=="T1": pred=sub[f"{aa}_T1"].astype(int).to_numpy(); valid=np.ones(len(sub),dtype=bool)
                elif t=="T2":
                    b=sub[f"{aa}_boundary"].astype(str); valid=b.isin(["semantic_only","overlap","hallucination_only"]).to_numpy(); pred=np.where(b.eq("semantic_only"),0,np.where(b.isin(["overlap","hallucination_only"]),1,-99))
                elif t=="T3":
                    f=sub[f"{aa}_family"].astype(str); valid=f.isin(["Core SCF","OVR"]).to_numpy(); pred=np.where(f.eq("Core SCF"),0,np.where(f.eq("OVR"),1,-99))
                else:
                    sev=sub[f"{aa}_severity"].astype(int).to_numpy(); valid=np.isin(sev,[1,2,3]); pred=np.where(valid,sev,-99)
                point_rows.append(dict(target=t,annotator=aa,n=len(sub),prompt_clusters=sub.Prompt_ID.nunique(),coverage=float(valid.mean()),strict_macro_f1=macro(y,pred,labels)))
        hp=pd.DataFrame(point_rows)
        archived_h=pd.read_csv(archived_dir / "P2_IPM_HUMAN_REFERENCE_TARGET_CONCORDANCE.csv")
        chk=hp.merge(archived_h,on=["target","annotator"],suffixes=("_re","_ar"))
        if float((chk["coverage_re"]-chk["coverage_ar"]).abs().max())>2e-9 or float((chk["strict_macro_f1_re"]-chk["strict_macro_f1_ar"]).abs().max())>2e-6:
            raise AssertionError("Human-reference point verification differs from archived result")
        out_h=OUT / "human_reference"; out_h.mkdir(exist_ok=True)
        hp.to_csv(out_h / "P2_IPM_HUMAN_REFERENCE_POINT_VERIFICATION.csv", index=False)
        h=archived_h
        print("PASS archived human-reference CIs + recomputed target point metrics", flush=True)

    ranges = h.groupby("target")["strict_macro_f1"].agg(["min", "max"])
    expected = {"T1": (0.863, 0.957), "T2": (0.835, 0.936), "T3": (0.847, 0.930), "T4": (0.644, 0.858)}
    for t, (lo, hi) in expected.items():
        if abs(ranges.loc[t, "min"] - lo) > 0.002 or abs(ranges.loc[t, "max"] - hi) > 0.002:
            raise AssertionError(f"{t} concordance range differs from frozen report")
    print("PASS annotator-to-reference target concordance", flush=True)

    report = {
        "status": "PASS_CURRENT_R8_REVIEWER_SAFE_CHECKS",
        "full_statistical_bootstrap_regenerated": bool(a.recompute_statistical_bootstrap),
        "slow_ci_followups_regenerated": bool(a.recompute_slow_ci_followups),
        "statistical_bootstrap_default_mode": "frozen manuscript artifact verified; fold/class support recomputed" if not a.recompute_statistical_bootstrap else "full bootstrap regenerated",
        "slow_ci_default_mode": "archived CI artifacts verified; point estimates recomputed" if not a.recompute_slow_ci_followups else "full CI follow-ups regenerated",
        "scientific_mutation": False,
        "retraining": False,
        "relabelling": False,
    }
    (OUT / "R8_REPRODUCIBILITY_RUN_STATUS.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("\nPASS — current R8 reviewer-safe follow-up checks completed.", flush=True)
    print("No M3/M4 retraining and no relabelling were performed.", flush=True)


if __name__ == "__main__":
    main()
