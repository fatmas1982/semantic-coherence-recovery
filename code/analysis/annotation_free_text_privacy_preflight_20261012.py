#!/usr/bin/env python3
"""Non-disclosing preliminary screen of publicly archived annotator free-text.

Regex screening is incomplete; NO automatic privacy/legal/consent clearance.
Never echo actual notes or matching substrings into CI logs or public reports.
"""
from pathlib import Path
import csv,json,re
ROOT=Path(__file__).resolve().parents[2]
PATS={
 "email":re.compile(r"(?<!\w)[A-Z0-9_.%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}",re.I),
 "url":re.compile(r"https?://[^\s]+",re.I),
 "phone_like":re.compile(r"(?<!\d)(?:\+?\d[\s().-]?){10,14}(?!\d)")
}
res=[]
for annotator in ("A1","A2","A3"):
    path=ROOT/f"data/annotation/historical_full_csv/{annotator}/Annotation.csv"
    with path.open(newline="",encoding="utf-8-sig") as f: rows=list(csv.DictReader(f))
    for field in ("comments","evidence_note"):
        counts={name:sum(bool(rx.search((r.get(field) or ""))) for r in rows)
                for name,rx in PATS.items()}
        res.append({"group":annotator,"field":field,"rows":len(rows),
                    **counts,"status":"MANUAL_PRIVACY_RIGHTS_REVIEW_REQUIRED"})
out=ROOT/"results/ANALYTIC_ANNOTATION_PRIVACY_PREFLIGHT.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({"note":"Automated pattern screening only, not comprehensive privacy/consent clearance; no free-text disclosed","counts":res},indent=2)+"\n")
for record in res:
    print("PRIVACY_PREFLIGHT",record["group"],record["field"],"rows",record["rows"],
          "email_flags",record["email"],"url_flags",record["url"],
          "phone_like_flags",record["phone_like"])
print("MANUAL_RELEASE_CLEARANCE_REQUIRED: historical free-text, senior adjudication and rights not certified")
