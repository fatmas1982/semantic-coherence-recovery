#!/usr/bin/env python3
"""Validate October GPU bundle reports against case-level predictions.

Usage:
  python code/analysis/verify_gpu_32_bundle.py P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE.zip
This validates archived outputs, not independent retraining.
"""
import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from sklearn.metrics import f1_score

EXPECTED = {"T1": 720, "T2": 474, "T3": 460, "T4": 474}
REQUIRED = {
    "reports/MANIFEST.json", "reports/PREDICTIONS.csv",
    "reports/METRICS_AND_CLUSTER_CI.csv", "reports/CONFUSION_MATRIX.csv",
    "reports/PER_CLASS.csv",
}

def sha256(payload):
    return hashlib.sha256(payload).hexdigest()

def verify(path):
    data = Path(path).read_bytes()
    results = {"archive_sha256": sha256(data), "experiments": [], "errors": []}
    with zipfile.ZipFile(io.BytesIO(data)) as outer:
        members = [p for p in outer.namelist()
                   if re.fullmatch(r"experiments/[^/]+\.zip", p)]
        if len(members) != 32:
            results["errors"].append("Expected 32 experiments, found " + str(len(members)))
        for name in sorted(members):
            entry = {"archive": name}
            results["experiments"].append(entry)
            try:
                task = "T" + re.search(r"_T([1-4])_", name).group(1)
                payload = outer.read(name)
                entry["sha256"] = sha256(payload)
                with zipfile.ZipFile(io.BytesIO(payload)) as child:
                    missing = sorted(REQUIRED - set(child.namelist()))
                    if missing:
                        raise ValueError("Missing required reports: " + repr(missing))
                    raw = child.read("reports/PREDICTIONS.csv")
                    entry["predictions_sha256"] = sha256(raw)
                    cases = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
                    if len(cases) != EXPECTED[task]:
                        raise ValueError("Unexpected case count " + str(len(cases)))
                    identifiers = [r["Case_ID"] for r in cases]
                    if len(identifiers) != len(set(identifiers)):
                        raise ValueError("Duplicate Case_ID")
                    pred = [k for k in cases[0] if k == "pred"
                            or (k.endswith("_pred") and k != "reference_pred")]
                    if len(pred) != 1:
                        raise ValueError("Cannot identify a unique prediction column: " + repr(pred))
                    y_true = [int(r["y_true"]) for r in cases]
                    y_pred = [int(r[pred[0]]) for r in cases]
                    score = f1_score(y_true, y_pred, average="macro", zero_division=0)
                    table = list(csv.DictReader(io.StringIO(child.read(
                        "reports/METRICS_AND_CLUSTER_CI.csv").decode("utf-8-sig"))))
                    scores = [float(r["macro_f1"]) for r in table
                              if r.get("macro_f1") not in (None, "")]
                    if not scores or not any(abs(v - score) < 1e-9 for v in scores):
                        raise ValueError("Macro-F1 mismatch")
                    entry.update(task=task, n=len(cases), macro_f1=score, status="PASS")
            except Exception as exc:
                entry.update(status="FAIL", error=str(exc))
                results["errors"].append(name + ": " + str(exc))
    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python verify_gpu_32_bundle.py PATH_TO_GPU_BUNDLE.zip")
    report = verify(sys.argv[1])
    print(json.dumps(report, indent=2))
    if report["errors"]:
        raise SystemExit(1)
