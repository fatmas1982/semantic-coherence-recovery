#!/usr/bin/env python3
"""Fail-closed publication of author-designated results.rar into a local Git checkout.

Does not overwrite any existing Git-tracked file. Run from a clone with
authenticated push access. All 4584 archived files are deposited separately
under results/authoritative_server_run_20261007_A/ with original RAR relative
paths beneath. Duplicate file contents retain their paths. No other results
or experiments are modified. Requires rarfile plus unrar or bsdtar.
"""
import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile

EXPECTED_SHA = "58493dc555ef95be1876416731723d71bb9c40ead2585e1b3bbafaad6ef7815d"
EXPECTED_FILES = 4584
PREFIX = Path("results/authoritative_server_run_20261007_A")

def sha256(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024*1024), b""):
            h.update(b)
    return h.hexdigest()

def run(*args):
    subprocess.run(args, check=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("rar", type=Path)
    p.add_argument("--push", action="store_true", help="Push resulting commit to origin/main")
    p.add_argument("--allow-nonmain", action="store_true", help="Allow current branch other than main")
    args=p.parse_args()
    rar=args.rar.resolve()
    if not rar.is_file() or sha256(rar) != EXPECTED_SHA:
        raise SystemExit("STOP: results.rar is missing or SHA-256 differs from the frozen authoritative archive")
    branch=subprocess.check_output(["git","branch","--show-current"],text=True).strip()
    if branch != "main" and not args.allow_nonmain:
        raise SystemExit(f"STOP: current branch is {branch!r}, expected main")
    if subprocess.check_output(["git","status","--porcelain"],text=True).strip():
        raise SystemExit("STOP: Git checkout is not clean")
    import rarfile
    with rarfile.RarFile(rar) as rf:
        entries=[i for i in rf.infolist() if i.isfile()]
        if len(entries)!=EXPECTED_FILES:
            raise SystemExit(f"STOP: {len(entries)} files; expected {EXPECTED_FILES}")
        items=[]
        for info in entries:
            posix=PurePosixPath(info.filename.replace("\\","/"))
            if posix.is_absolute() or any(x in ("..","") for x in posix.parts):
                raise SystemExit("STOP: unsafe entry path")
            if info.needs_password():
                raise SystemExit("STOP: encrypted archive member")
            dest=PREFIX.joinpath(*posix.parts)
            if dest.exists():
                raise SystemExit(f"STOP: would overwrite {dest}")
            items.append((info,dest))
        try:
            for info,dest in items:
                dest.parent.mkdir(parents=True,exist_ok=True)
                with rf.open(info) as src, dest.open("xb") as out:
                    import shutil
                    shutil.copyfileobj(src,out,1024*1024)
            run("git","add","--",str(PREFIX))
            added=subprocess.check_output(["git","diff","--cached","--name-only"],text=True).splitlines()
            if len(added)!=EXPECTED_FILES:
                raise SystemExit(f"STOP: staged {len(added)} files instead of {EXPECTED_FILES}; check .gitignore")
            run("git","commit","-m","data: deposit authoritative results.rar experiment members without overwriting existing results")
            if args.push:
                run("git","push","origin","HEAD:main")
            print(f"PASS: {len(added)} original members deposited under {PREFIX}; archive SHA-256 verified.")
            if not args.push: print("NOT PUSHED: rerun with --push only after checking the commit.")
        except Exception:
            print("STOP: publication failed; inspect the working tree; do not claim success",file=sys.stderr)
            raise

if __name__=="__main__":
    main()
