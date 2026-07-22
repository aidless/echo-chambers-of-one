"""
合成烟雾测试数据
================
生成一份逼真的小型轨迹数据集，用于预演 analysis_skeleton.py：
- 6 模型、6 条件、3 任务，3 条种子 → 324 条轨迹
- 隔离组在指标上具有最陡的负斜率
- 反馈组与同伴组斜率接近 0
- 新颖性组中等衰减
- 控制组斜率为 0
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path(__file__).parent / "trajectories.csv"
RNG = np.random.default_rng(20260722)

MODELS = [
    ("llama-3.1-70b-instruct", 0.04),
    ("llama-3.1-405b-instruct", 0.02),
    ("qwen-2.5-72b-instruct", 0.05),
    ("claude-sonnet-4", 0.03),
    ("gpt-4o", 0.035),
    ("deepseek-v3", 0.045),
]

CONDITIONS = [
    ("control_stateless", 0.00),
    ("isolated", -0.080),
    ("novelty", -0.045),
    ("feedback", -0.015),
    ("peer", -0.020),
    ("human", 0.010),
]

TASKS = [
    ("vending", 0.05),
    ("alfworld", 0.04),
    ("longmem", 0.03),
]

CHECKPOINTS = [0, 100, 500, 1000, 2000, 5000, 10000]
SEEDS = [11, 22, 33]


def base_score(model_id: str, task_id: str) -> float:
    """每个 (model, task) 的初始能力。"""
    rng = np.random.default_rng(hash((model_id, task_id)) & 0xFFFFFFFF)
    return rng.uniform(0.62, 0.82)


def trajectory(model_id: str, task_id: str, cond_id: str, slope: float, run_idx: int) -> pd.DataFrame:
    base = base_score(model_id, task_id)
    run_offset = RNG.normal(0.0, 0.03)
    base += run_offset
    rows = []
    for cp in CHECKPOINTS:
        # 隔离组使用 log(1+t) 斜率；其他条件叠加其 baseline
        decay = slope * np.log1p(cp)
        # 控制组斜率为 0；isolation 最陡
        # 加入 model × checkpoint 噪声
        noise = RNG.normal(0.0, 0.04)
        accuracy = np.clip(base + decay + noise, 0.0, 1.0)
        planning = np.clip(accuracy - 0.05 + RNG.normal(0.0, 0.03), 0.0, 1.0)
        decision = np.clip(accuracy + RNG.normal(0.0, 0.04), 0.0, 1.0)
        calibration = np.clip(0.85 - 0.4 * abs(decay) + RNG.normal(0.0, 0.03), 0.0, 1.0)
        memory = np.clip(0.9 - 0.6 * abs(decay) + RNG.normal(0.0, 0.04), 0.0, 1.0)
        survival = max(cp, 10000) if abs(decay) < 0.05 else max(1, cp * (1 + slope))
        rows.append(
            {
                "trajectory_id": f"{model_id}__{task_id}__{cond_id}__seed{SEEDS[run_idx]}",
                "model": model_id,
                "condition": cond_id,
                "task": task_id,
                "checkpoint": cp,
                "step_count": cp,
                "accuracy": float(accuracy),
                "planning_score": float(planning),
                "decision_score": float(decision),
                "calibration": float(calibration),
                "memory_score": float(memory),
                "survival_step": float(survival),
                "seed": SEEDS[run_idx],
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    frames = []
    for model_id, _ in MODELS:
        for task_id, _ in TASKS:
            for cond_id, slope in CONDITIONS:
                for run_idx in range(len(SEEDS)):
                    frames.append(trajectory(model_id, task_id, cond_id, slope, run_idx))
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(OUT, index=False)
    print(f"wrote {len(df):,} rows to {OUT}")
    print(df.groupby("condition")["accuracy"].agg(["mean", "std"]).round(3))


if __name__ == "__main__":
    main()