#!/usr/bin/env python3
"""CPU size-matched control for the archived dual-blocked M1 audit.

For each held-out fold x generator cell, randomly remove from the standard
training fold as many rows as generator blocking removed, without conditioning
on generator identity. Repeat with independent seeds. The same test rows are
predicted once per repetition; this isolates training-row count for M1 only.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.svm import LinearSVC


def serialise(r):
    prompt = str(r.Prompt_Text or "").strip()
    source = str(r.Source_Context or "").strip()
    output = str(r.Model_Output or "").strip()
    if str(r.Source_Available).lower() == "yes" and source:
        return f"Task:\n{prompt}\n\nAuthorised source/context:\n{source}\n\nResponse:\n{output}"
    return f"Task:\n{prompt}\n\nResponse:\n{output}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--seed", type=int, default=20260928)
    args = ap.parse_args()
    root = args.root.resolve()
    out = root / "results/reviewer_20260928/m1_size_matched"
    out.mkdir(parents=True, exist_ok=True)
    cases = pd.read_csv(root / "data/publication/canonical_publication_dataset_720.csv")
    cases = cases[["Case_ID", "Prompt_Text", "Source_Context", "Source_Available", "Model_Output"]]
    cases = cases.fillna("")
    cases["text_C"] = [serialise(r) for r in cases.itertuples(index=False)]
    archived = pd.read_csv(root / "results/validity/cpu/P2_81_M1_DUAL_BLOCKED_OOF.csv")
    expected = {"T1": 720, "T2": 474, "T3": 460, "T4": 474}
    available = archived.target.value_counts().to_dict()
    complete = [target for target, n in expected.items() if available.get(target) == n]
    if not complete:
        raise ValueError(f"No complete target OOF found: {available}; expected {expected}")
    print(f"Complete targets: {complete}; incomplete targets excluded: {available}", flush=True)
    rng = np.random.default_rng(args.seed)
    summaries, predictions = [], []
    for target, orig in archived.groupby("target", sort=True):
        if target not in complete:
            continue
        d = orig.merge(cases[["Case_ID", "text_C"]], on="Case_ID", validate="one_to_one")
        assert len(d) == len(orig) and d.Case_ID.is_unique
        for rep in range(args.repeats):
            pred = np.full(len(d), -999, dtype=int)
            for fold in sorted(d.Fold.unique()):
                standard_train = np.flatnonzero((d.Fold != fold).to_numpy())
                for generator in sorted(d.Generator_Stratum.unique()):
                    test = np.flatnonzero(((d.Fold == fold) & (d.Generator_Stratum == generator)).to_numpy())
                    blocked_train_n = int(((d.Fold != fold) & (d.Generator_Stratum != generator)).sum())
                    train = rng.choice(standard_train, size=blocked_train_n, replace=False)
                    assert len(train) == blocked_train_n and len(test)
                    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=.98,
                                          max_features=40000, sublinear_tf=True)
                    xtrain = vec.fit_transform(d.iloc[train].text_C)
                    xtest = vec.transform(d.iloc[test].text_C)
                    clf = LinearSVC(C=1.0, class_weight="balanced", random_state=20260908)
                    clf.fit(xtrain, d.iloc[train].y_true.astype(int))
                    pred[test] = clf.predict(xtest)
            assert (pred != -999).all()
            labels = [0, 1] if target != "T4" else [1, 2, 3]
            def metric(col):
                return f1_score(d.y_true, col, labels=labels, average="macro", zero_division=0)
            summaries.append(dict(target=target, repeat=rep, n=len(d),
                                  standard_m1=metric(d.standard_m1_pred),
                                  size_matched_m1=metric(pred),
                                  dual_blocked_m1=metric(d.dual_blocked_pred)))
            predictions.append(pd.DataFrame(dict(target=target, repeat=rep, Case_ID=d.Case_ID,
                                                  Prompt_ID=d.Prompt_ID, Fold=d.Fold,
                                                  Generator_Stratum=d.Generator_Stratum,
                                                  y_true=d.y_true, size_matched_pred=pred)))
        print(target, pd.DataFrame(summaries).query("target == @target")[
            ["standard_m1", "size_matched_m1", "dual_blocked_m1"]].mean().to_dict(), flush=True)
    pd.DataFrame(summaries).to_csv(out / "m1_size_matched_metrics.csv", index=False)
    pd.concat(predictions, ignore_index=True).to_csv(out / "m1_size_matched_oof.csv", index=False)
    (out / "manifest.json").write_text(json.dumps(dict(seed=args.seed, repeats=args.repeats,
        available_rows=available, expected_rows=expected, complete_targets=complete,
        sampling="independent uniform training-row removal per held-out fold x generator cell",
        caveat="M1-only post-hoc size control; does not resolve M3 training-size confound"), indent=2))


if __name__ == "__main__":
    main()
