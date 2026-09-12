#!/usr/bin/env python3
"""Reconstructed CPU baseline trainer for M0/M1/M2.

IMPORTANT PROVENANCE BOUNDARY
-----------------------------
The paper's reportable M0/M1/M2 numbers are reproduced exactly from the frozen
OOF prediction sheets in P2_CPU_Baselines_v1.0.xlsx. The original historical
training script was not retained. This script reconstructs the documented
model specifications and frozen Prompt_ID folds, and is intended for fresh
retraining/sensitivity checks. It MUST NOT be described as the original
historical baseline implementation unless its outputs are independently shown
to match the archived OOF predictions exactly.

Documented specifications:
- M0: training-fold majority class.
- M1: word TF-IDF 1-2 grams; min_df=2; max_df=.98; <=40k features;
      sublinear_tf=True; LinearSVC(C=1,class_weight='balanced').
- M2: word TF-IDF <=30k -> TruncatedSVD(100) -> L2 normalization ->
      LogisticRegression(class_weight='balanced',max_iter=2000).
- Folds: frozen five-fold task-balanced Prompt_ID groups, seed 20260908.
- Primary condition C: prompt + authorised source/context where available + output.

For exact verification of the published numerical baseline results, run
code/analysis/P2_54_Colab_01_Verify_Completed_Experiments.ipynb or
code/analysis/reproduce_public_metrics.py against the frozen OOF sheets.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.preprocessing import Normalizer
from sklearn.svm import LinearSVC

SEED = 20260908


def serialise(row: pd.Series, condition: str = "C") -> str:
    prompt = "" if pd.isna(row.get("Prompt_Text")) else str(row["Prompt_Text"]).strip()
    source = "" if pd.isna(row.get("Source_Context")) else str(row["Source_Context"]).strip()
    output = "" if pd.isna(row.get("Model_Output")) else str(row["Model_Output"]).strip()
    if condition == "A":
        return output
    if condition == "B":
        return f"Task:\n{prompt}\n\nResponse:\n{output}"
    if condition == "C":
        if str(row.get("Source_Available", "")).lower() == "yes" and source:
            return f"Task:\n{prompt}\n\nAuthorised source/context:\n{source}\n\nResponse:\n{output}"
        return f"Task:\n{prompt}\n\nResponse:\n{output}"
    raise ValueError(condition)


def train_predict(train_text, test_text, y_train, model: str):
    if model == "M0":
        clf = DummyClassifier(strategy="most_frequent")
        clf.fit(np.zeros((len(y_train), 1)), y_train)
        return clf.predict(np.zeros((len(test_text), 1)))
    if model == "M1":
        vec = TfidfVectorizer(
            ngram_range=(1, 2), min_df=2, max_df=.98,
            max_features=40000, sublinear_tf=True,
        )
        Xtr = vec.fit_transform(train_text); Xte = vec.transform(test_text)
        clf = LinearSVC(C=1.0, class_weight="balanced")
        clf.fit(Xtr, y_train)
        return clf.predict(Xte)
    if model == "M2":
        vec = TfidfVectorizer(ngram_range=(1, 2), max_features=30000)
        Xtr = vec.fit_transform(train_text); Xte = vec.transform(test_text)
        ncomp = min(100, max(1, Xtr.shape[1] - 1))
        svd = TruncatedSVD(n_components=ncomp, random_state=SEED)
        norm = Normalizer(copy=False)
        Ztr = norm.fit_transform(svd.fit_transform(Xtr))
        Zte = norm.transform(svd.transform(Xte))
        clf = LogisticRegression(
            class_weight="balanced", max_iter=2000, random_state=SEED
        )
        clf.fit(Ztr, y_train)
        return clf.predict(Zte)
    raise ValueError(model)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold-csv", required=True)
    ap.add_argument("--folds-csv", required=True)
    ap.add_argument("--oof-dir", required=True, help="Directory containing 10_OOF_T1.csv ... 13_OOF_T4.csv")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--condition", choices=["A", "B", "C"], default="C")
    args = ap.parse_args()
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    gold = pd.read_csv(args.gold_csv).set_index("Case_ID", drop=False)
    folds = pd.read_csv(args.folds_csv).set_index("Prompt_ID")["Fold"].astype(int).to_dict()
    names = {"T1":"10_OOF_T1.csv","T2":"11_OOF_T2.csv","T3":"12_OOF_T3.csv","T4":"13_OOF_T4.csv"}
    summary=[]
    for target, name in names.items():
        archived = pd.read_csv(Path(args.oof_dir)/name)
        d = gold.loc[archived["Case_ID"].astype(str)].copy()
        d["y_true"] = archived["y_true"].astype(int).values
        d["Fold"] = d["Prompt_ID"].map(folds).astype(int)
        d["text"] = d.apply(lambda r: serialise(r, args.condition), axis=1)
        result = archived[["Case_ID","Prompt_ID","Task_Type","Fold","y_true"]].copy()
        for model in ["M0","M1","M2"]:
            pred = np.empty(len(d), dtype=int)
            for fold in sorted(d["Fold"].unique()):
                te = (d["Fold"].to_numpy()==fold); tr=~te
                pred[te] = train_predict(
                    d.loc[tr,"text"].tolist(), d.loc[te,"text"].tolist(),
                    d.loc[tr,"y_true"].to_numpy(), model,
                )
            result[f"{model}_retrained_pred"] = pred
            archived_col=f"{model}_pred"
            exact=float(np.mean(pred==archived[archived_col].astype(int).to_numpy())) if archived_col in archived else np.nan
            summary.append({
                "target":target,"model":model,"condition":args.condition,
                "macro_f1_retrained":float(f1_score(d["y_true"],pred,average="macro")),
                "prediction_agreement_with_archived_oof":exact,
                "provenance_status":"RECONSTRUCTED_TRAINER_NOT_HISTORICAL_SCRIPT",
            })
        result.to_csv(out/f"RETRAINED_{target}_{args.condition}.csv",index=False)
    pd.DataFrame(summary).to_csv(out/"RETRAINED_BASELINE_SUMMARY.csv",index=False)
    print(pd.DataFrame(summary).to_string(index=False))
    print("\nDo not replace archived reportable OOF values with reconstructed retraining values.")

if __name__ == "__main__":
    main()
