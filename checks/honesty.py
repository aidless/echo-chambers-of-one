#!/usr/bin/env python3
"""Static honesty checks. Offline: no arXiv, Crossref, OSF, or model API.

VERIFIED in CITATION_AUDIT.md means a retrieval recorded in that file.
This script does not repeat the retrieval. It checks that every arXiv id
and DOI cited in the tree is listed, and that a MISMATCH or UNVERIFIED
row is marked next to that id outside the audit file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "CITATION_AUDIT.md"
STAMP = ROOT / "checks" / "artifacts" / "protocol_stamp.json"
PROTOCOL_FILES = ("preregistration.md", "experiment_manifest.json")
ID_RE = re.compile(
    r"(?:arxiv\.org/abs/|arXiv:|arxiv\s+)(\d{4}\.\d{4,5})|(10\.\d{4,9}/[^\s)\]\"'`<>]+)",
    re.I,
)
ROW_RE = re.compile(r"^\| ([^|]+?) \| (VERIFIED|MISMATCH|UNVERIFIED) \|", re.M)
SKIP_PARTS = {".git", ".venv", "__pycache__", "checks/artifacts"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def tracked_text_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".html", ".json", ".py", ".yml", ".yaml"}:
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        files.append(path)
    return files


def cited_ids() -> set[str]:
    found = set()
    for path in tracked_text_files():
        if path.resolve() == AUDIT.resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for arxiv, doi in ID_RE.findall(text):
            if arxiv:
                found.add(arxiv)
            if doi:
                found.add(doi.rstrip(".").rstrip("`"))
    return found


def audit_rows() -> list[tuple[str, str]]:
    if not AUDIT.is_file():
        fail("CITATION_AUDIT.md is missing")
    rows = []
    for ident, status in ROW_RE.findall(AUDIT.read_text(encoding="utf-8")):
        rows.append((ident.strip().rstrip("."), status))
    if not rows:
        fail("CITATION_AUDIT.md has no status table rows")
    return rows


def marker_near(ident: str, status: str) -> bool:
    token = f"[{status}]"
    for path in tracked_text_files():
        if path.resolve() == AUDIT.resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(re.escape(ident), text):
            window = text[max(0, match.start() - 400) : match.end() + 400]
            if token in window:
                return True
    return False


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp_body() -> dict:
    files = {name: sha256(ROOT / name) for name in PROTOCOL_FILES}
    return {
        "kind": "git-content-stamp",
        "osf_project_created": False,
        "doi": None,
        "statement": (
            "SHA-256 of the protocol files in this tree. Not an OSF registration, "
            "not a DOI, and not a third-party timestamp. The git commit that contains "
            "these bytes is the repository clock; read it with `git rev-parse HEAD`. "
            "The existing tag v0.4-pre-reg is an older commit and is not a registration."
        ),
        "files": files,
    }


def check_stamp() -> None:
    if not STAMP.is_file():
        fail("checks/artifacts/protocol_stamp.json is missing; run checks/honesty.py --write-stamp")
    committed = json.loads(STAMP.read_text(encoding="utf-8"))
    fresh = stamp_body()
    if committed.get("osf_project_created") is not False or committed.get("doi") is not None:
        fail("protocol stamp claims an OSF project or a DOI")
    if committed.get("files") != fresh["files"]:
        fail(
            "protocol stamp hashes do not match preregistration.md / experiment_manifest.json. "
            f"fresh={fresh['files']}"
        )


def check_citations() -> None:
    rows = audit_rows()
    listed = {ident for ident, _ in rows}
    missing = sorted(cited_ids() - listed)
    if missing:
        fail("cited ids missing from CITATION_AUDIT.md: " + ", ".join(missing))
    for ident, status in rows:
        if status in {"MISMATCH", "UNVERIFIED"} and not marker_near(ident, status):
            fail(f"{ident} is {status} in the audit but no source file marks it [{status}] near the id")


def require(path: Path, snippets: list[str], forbidden: list[str] | None = None) -> None:
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            fail(f"{path.relative_to(ROOT)} is missing {snippet!r}")
    for snippet in forbidden or []:
        if snippet in text:
            fail(f"{path.relative_to(ROOT)} still contains {snippet!r}")


def check_prose() -> None:
    require(
        ROOT / "README.md",
        [
            "preregistration and analysis-protocol pack",
            "make check",
            "does not prove any empirical finding",
            "OSF project has not been created",
            "v0.4-pre-reg",
            "@aidless",
        ],
    )
    opening = (ROOT / "README.md").read_text(encoding="utf-8").splitlines()[:6]
    problem = [
        line
        for line in opening
        if line.startswith("This repository")
        or line.startswith("`make check`")
        or line.startswith("It does not prove")
    ]
    if len(problem) != 3:
        fail("README problem statement must be the three designated opening lines")
    require(
        ROOT / "STATUS.md",
        ["v0.4-pre-reg", "not created", "@aidless", "not a completed study"],
    )
    require(
        ROOT / "cover_letter.md",
        ["NOT SUBMITTED", "ANTICIPATED", "No review was received"],
        ["We are pleased to submit", "pleased to submit"],
    )
    require(
        ROOT / "FAILURE_MODES.md",
        [
            "## Model misspecification",
            "## LMM non-convergence fallback",
            "## Confound threats",
            "## What would falsify the hypothesis",
        ],
    )
    require(ROOT / ".github" / "CODEOWNERS", ["@aidless"])
    require(ROOT / ".github" / "workflows" / "ci.yml", ["make check"])
    require(ROOT / "preregistration.md", ["osf_project_created", "尚未创建"])
    # A submission sentence must not survive anywhere in the prose docs.
    for path in tracked_text_files():
        if path.suffix.lower() not in {".md", ".html"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "We are pleased to submit" in text or "pleased to submit" in text:
            fail(f"{path.relative_to(ROOT)} still reads as a sent cover letter")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-stamp", action="store_true")
    args = parser.parse_args()
    if args.write_stamp:
        STAMP.parent.mkdir(parents=True, exist_ok=True)
        STAMP.write_text(json.dumps(stamp_body(), indent=2) + "\n", encoding="utf-8")
        print(f"wrote {STAMP}")
    check_stamp()
    check_citations()
    check_prose()
    digest = json.loads(STAMP.read_text(encoding="utf-8"))["files"]
    print("OK: honesty checks passed")
    for name, hashed in digest.items():
        print(f"  {name} sha256 {hashed}")


if __name__ == "__main__":
    main()
