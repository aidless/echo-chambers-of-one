#!/usr/bin/env python3
"""Synthetic parameter recovery for analysis_skeleton.py.

This is not an empirical result. A fixed design plants a slope gap of +0.04
on accuracy for condition ``feedback`` relative to ``isolated``, and plants
zeros on the other contrasts in that file. A second design plants all zeros.

``make check`` re-runs the skeleton and requires:

- the planted interaction is recovered within 0.005 and flagged at Holm 0.05
- the zero contrasts in that same file are not flagged
- in the all-null design, a flagged contrast (a 5% test will sometimes flag)
  has absolute coefficient <= 0.01, and at most 3 of 20 seeds flag

Floats are compared with the committed artifact in checks/artifacts/.
Requires the pinned stack in requirements.txt and CPython 3.12, because
MixedLM results are not compared across versions.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SKELETON = ROOT / "analysis_skeleton.py"
ARTIFACT = ROOT / "checks" / "artifacts" / "parameter_recovery.json"

PLANTED = 0.04
SLOPE0 = -0.02
N_PER = 30
RE_SD = 0.05
NOISE = 0.03
CHECKPOINTS = np.array([0, 100, 500, 1000, 2000, 5000, 10000])
LOGS = np.log1p(CHECKPOINTS)
SELECTIVE_SEEDS = list(range(1000, 1020))
NULL_SEEDS = list(range(2000, 2020))
PLANTED_ABS_TOL = 0.005
NULL_FLAG_COEF_MAX = 0.01
NULL_FLAG_SEEDS_MAX = 3

EXPECTED_VERSIONS = {
    "numpy": "2.2.6",
    "pandas": "2.2.3",
    "statsmodels": "0.14.5",
    "sklearn": "1.6.1",
    "scipy": "1.15.3",
}


def versions() -> dict[str, str]:
    import scipy
    import sklearn
    import statsmodels

    return {
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "statsmodels": statsmodels.__version__,
        "sklearn": sklearn.__version__,
        "scipy": scipy.__version__,
    }


def require_versions() -> dict[str, str]:
    got = versions()
    if (sys.version_info.major, sys.version_info.minor) != (3, 12):
        sys.exit(f"parameter recovery is pinned to CPython 3.12, found {got['python']}")
    for name, expected in EXPECTED_VERSIONS.items():
        if got[name] != expected:
            sys.exit(
                f"parameter recovery is pinned to {name}=={expected}, found {got[name]}. "
                "Refusing to compare MixedLM floats across versions."
            )
    return got


def simulate(seed: int, deltas: dict[str, float], outcomes_share_effect: bool) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for cond, delta in deltas.items():
        for i in range(N_PER):
            intercept = rng.normal(0.55, RE_SD)
            intercept_plan = rng.normal(0.40, RE_SD)
            for cp, ls in zip(CHECKPOINTS, LOGS):
                accuracy = intercept + (SLOPE0 + delta) * ls + rng.normal(0, NOISE)
                # planning_score never carries the condition gap.
                planning = intercept_plan + SLOPE0 * ls + rng.normal(0, NOISE)
                if outcomes_share_effect:
                    planning = accuracy
                rows.append(
                    {
                        "trajectory_id": f"{cond}-{seed}-{i}",
                        "model": "synthetic",
                        "condition": cond,
                        "task": "synthetic",
                        "checkpoint": int(cp),
                        "step_count": int(cp),
                        "accuracy": float(accuracy),
                        "planning_score": float(planning),
                        "decision_score": float(accuracy),
                        "calibration": float(accuracy),
                        "memory_score": float(accuracy),
                        "survival_step": float(cp + 1),
                        "seed": int(seed),
                    }
                )
    return pd.DataFrame(rows)


def run_skeleton(df: pd.DataFrame, outcomes: list[str]) -> tuple[pd.DataFrame, dict]:
    with tempfile.TemporaryDirectory(prefix="eco-recovery-") as tmp:
        folder = Path(tmp)
        csv_path = folder / "trajectories.csv"
        out = folder / "out"
        out.mkdir()
        df.to_csv(csv_path, index=False)
        proc = subprocess.run(
            [
                sys.executable,
                str(SKELETON),
                "--csv",
                str(csv_path),
                "--out",
                str(out),
                "--reference",
                "isolated",
                "--outcomes",
                *outcomes,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            sys.stderr.write(proc.stderr)
            sys.exit(f"analysis_skeleton.py exited {proc.returncode}")
        tests = pd.read_csv(out / "interaction_tests.csv")
        results = json.loads((out / "lmm_results.json").read_text(encoding="utf-8"))
    return tests, results


def rnd(value: float) -> float:
    return round(float(value), 8)


def pack_rows(tests: pd.DataFrame, results: dict) -> list[dict]:
    methods = {name: results[name].get("method") for name in results}
    packed = []
    for row in tests.itertuples(index=False):
        packed.append(
            {
                "outcome": row.outcome,
                "interaction": row.interaction,
                "coef": rnd(row.coef),
                "p_raw": rnd(row.p_raw),
                "p_adjusted_holm": rnd(row.p_adjusted_holm),
                "significant_05": bool(row.significant_05),
                "method": methods[row.outcome],
            }
        )
    return packed


def selective_case(seed: int) -> list[dict]:
    df = simulate(
        seed,
        {"isolated": 0.0, "feedback": PLANTED, "novelty": 0.0},
        outcomes_share_effect=False,
    )
    tests, results = run_skeleton(df, ["accuracy", "planning_score"])
    return pack_rows(tests, results)


def null_case(seed: int) -> list[dict]:
    df = simulate(
        seed,
        {"isolated": 0.0, "feedback": 0.0, "novelty": 0.0},
        outcomes_share_effect=True,
    )
    tests, results = run_skeleton(df, ["accuracy"])
    return pack_rows(tests, results)


def assert_science(report: dict) -> None:
    errors = []
    for seed, rows in zip(SELECTIVE_SEEDS, report["selective"]):
        planted_rows = [
            r
            for r in rows
            if r["outcome"] == "accuracy" and r["interaction"] == "cond_feedback_x_logstep"
        ]
        if len(planted_rows) != 1:
            errors.append(f"seed {seed}: expected one planted row, found {len(planted_rows)}")
            continue
        planted = planted_rows[0]
        if abs(planted["coef"] - PLANTED) > PLANTED_ABS_TOL:
            errors.append(f"seed {seed}: planted coef {planted['coef']} not within {PLANTED_ABS_TOL} of {PLANTED}")
        if not planted["significant_05"]:
            errors.append(f"seed {seed}: planted interaction was not flagged")
        for row in rows:
            if row is planted:
                continue
            if row["significant_05"]:
                errors.append(
                    f"seed {seed}: null contrast flagged {row['outcome']} {row['interaction']} coef={row['coef']}"
                )
    flagged_seeds = []
    for seed, rows in zip(NULL_SEEDS, report["all_null"]):
        for row in rows:
            if row["significant_05"]:
                flagged_seeds.append(seed)
                if abs(row["coef"]) > NULL_FLAG_COEF_MAX:
                    errors.append(
                        f"null seed {seed}: flagged coef {row['coef']} exceeds {NULL_FLAG_COEF_MAX}"
                    )
    if len(set(flagged_seeds)) > NULL_FLAG_SEEDS_MAX:
        errors.append(
            f"all-null design flagged {len(set(flagged_seeds))} seeds; cap is {NULL_FLAG_SEEDS_MAX}"
        )
    report["summary"] = {
        "selective_seeds": len(SELECTIVE_SEEDS),
        "planted_value": PLANTED,
        "planted_abs_tolerance": PLANTED_ABS_TOL,
        "max_abs_planted_error": rnd(
            max(
                abs(r["coef"] - PLANTED)
                for rows in report["selective"]
                for r in rows
                if r["outcome"] == "accuracy" and r["interaction"] == "cond_feedback_x_logstep"
            )
        ),
        "all_null_seeds": len(NULL_SEEDS),
        "all_null_seeds_with_a_flag": sorted(set(flagged_seeds)),
        "all_null_flag_cap": NULL_FLAG_SEEDS_MAX,
        "note": (
            "A flag in the all-null design is a Type I event for a 0.05 test, "
            "not recovery of the planted 0.04 effect. This file is not a power "
            "calculation for the 1080-cell study."
        ),
    }
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)


def close(left, right, path: str = "$") -> list[str]:
    diffs = []
    if isinstance(left, dict) or isinstance(right, dict):
        if not isinstance(left, dict) or not isinstance(right, dict):
            return [f"{path}: type {type(left).__name__} vs {type(right).__name__}"]
        for key in sorted(set(left) | set(right)):
            if key not in left or key not in right:
                diffs.append(f"{path}.{key}: missing on one side")
            else:
                diffs.extend(close(left[key], right[key], f"{path}.{key}"))
        return diffs
    if isinstance(left, list) or isinstance(right, list):
        if not isinstance(left, list) or not isinstance(right, list) or len(left) != len(right):
            return [f"{path}: list length {len(left) if isinstance(left, list) else '?'} vs {len(right) if isinstance(right, list) else '?'}"]
        for i, (a, b) in enumerate(zip(left, right)):
            diffs.extend(close(a, b, f"{path}[{i}]"))
        return diffs
    if isinstance(left, float) or isinstance(right, float):
        if abs(float(left) - float(right)) > 1e-6:
            diffs.append(f"{path}: {left} != {right}")
        return diffs
    if left != right:
        diffs.append(f"{path}: {left!r} != {right!r}")
    return diffs


def build() -> dict:
    vers = require_versions()
    report = {
        "kind": "synthetic-parameter-recovery",
        "empirical_result": False,
        "osf_registration": False,
        "reference_level": "isolated",
        "coding_note": (
            "Reference level is isolated, so cond_feedback_x_logstep is the "
            "feedback slope minus the isolated slope. Preregistration §7 names "
            "the opposite coding (reference = feedback, β3 < 0 for isolated). "
            "The planted +0.04 gap is that same contrast with the sign flipped "
            "by the reference level. The skeleton does not fit the length term "
            "or the three-way interaction in §7."
        ),
        "dgp": {
            "checkpoints": [int(c) for c in CHECKPOINTS],
            "n_trajectories_per_condition": N_PER,
            "random_intercept_sd": RE_SD,
            "residual_sd": NOISE,
            "isolated_slope": SLOPE0,
            "planted_feedback_minus_isolated": PLANTED,
            "novelty_minus_isolated": 0.0,
            "planning_score_condition_gap": 0.0,
            "outcome_is_unbounded": True,
        },
        "versions": vers,
        "selective": [selective_case(seed) for seed in SELECTIVE_SEEDS],
        "all_null": [null_case(seed) for seed in NULL_SEEDS],
    }
    assert_science(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="overwrite the committed artifact")
    args = parser.parse_args()
    report = build()
    if args.write:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {ARTIFACT}")
    if not ARTIFACT.is_file():
        sys.exit(f"missing {ARTIFACT}; run with --write after a successful local run")
    committed = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    diffs = close(report, committed)
    if diffs:
        print("committed artifact does not match a fresh run:", file=sys.stderr)
        print("\n".join(diffs[:30]), file=sys.stderr)
        sys.exit(1)
    summary = report["summary"]
    print(
        "OK: planted accuracy interaction recovered on "
        f"{summary['selective_seeds']} seeds "
        f"(max |error|={summary['max_abs_planted_error']}); "
        f"all-null flags on seeds {summary['all_null_seeds_with_a_flag'] or 'none'}"
    )


if __name__ == "__main__":
    main()
