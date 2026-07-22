"""
把 pilot/outputs/*.json 合并为 analysis_skeleton.py 期望的 trajectories.csv 格式。

用法：
    python pilot/collect_outputs.py --out pilot/collected_trajectories.csv
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="收集 pilot 输出并合并为 trajectories.csv")
    parser.add_argument("--inputs", type=Path, default=Path(__file__).parent / "outputs")
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "collected_trajectories.csv")
    args = parser.parse_args()

    rows = []
    for f in sorted(args.inputs.glob("*.json")):
        with f.open(encoding="utf-8") as fh:
            data = json.load(fh)
        trajectory_id = f.stem
        for ev in data["evaluations"]:
            row = {
                "trajectory_id": trajectory_id,
                "model": data["model"],
                "condition": data["condition"],
                "task": data["task"],
                "checkpoint": ev["checkpoint"],
                "step_count": ev["checkpoint"],
                "accuracy": ev["accuracy"],
                "planning_score": ev["planning_score"],
                "decision_score": ev["decision_score"],
                "calibration": ev["calibration"],
                "memory_score": ev["memory_score"],
                "survival_step": ev["checkpoint"] * 1.05,
                "seed": 0,
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(args.out, index=False)
    print(f"[done] wrote {len(df):,} rows to {args.out}")
    if not df.empty:
        print(df.groupby("condition")["accuracy"].agg(["mean", "std"]).round(3))


if __name__ == "__main__":
    main()