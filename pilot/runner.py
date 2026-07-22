"""
单轨迹主循环
============

协调：环境 → LLM 客户端 → Agent 状态 → 评测电池。
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from vending_env import VendingEnv
from evaluator import EvalBattery
from llm_client import LLMResponse, build_client


CHECKPOINTS = [0, 100, 500, 1000, 2000, 5000, 10000]


@dataclass
class ConditionSignals:
    """单一条件下的外源信号配置。"""

    novelty_enabled: bool = False
    feedback_enabled: bool = False
    peer_enabled: bool = False
    human_enabled: bool = False

    def external_token_quota_per_100(self) -> int:
        quota = 0
        if self.novelty_enabled:
            quota += 1800
        if self.feedback_enabled:
            quota += 100
        if self.peer_enabled:
            quota += 1900
        if self.human_enabled:
            quota += 2000
        return quota


def condition_signals(condition: str) -> ConditionSignals:
    return {
        "control_stateless": ConditionSignals(),
        "isolated": ConditionSignals(),
        "novelty": ConditionSignals(novelty_enabled=True),
        "feedback": ConditionSignals(feedback_enabled=True),
        "peer": ConditionSignals(novelty_enabled=True, feedback_enabled=True, peer_enabled=True),
        "human": ConditionSignals(novelty_enabled=True, feedback_enabled=True, human_enabled=True),
    }[condition]


def run_trajectory(
    model_id: str,
    task: str,
    condition: str,
    steps: int,
    seed: int,
    checkpoints: list[int] | None = None,
    external_text_provider: Callable[[int], str] | None = None,
    health_check: bool = False,
) -> dict:
    """运行一条轨迹，返回结构化记录。

    health_check=False 是默认值：批量 pilot 时跳过 health probe，避免重复 ping 401
    的无效 key。生产环境可设为 True 做事前探测。
    """
    if checkpoints is None:
        checkpoints = [c for c in CHECKPOINTS if c <= steps]

    client = build_client(model_id, seed=seed, health_check=health_check)
    env = VendingEnv(seed=seed)
    signals = condition_signals(condition)
    quota_per_100 = signals.external_token_quota_per_100()

    # 预实验：仅保留 steps = 200 的检查点
    checkpoints = [c for c in checkpoints if c <= steps]
    if 0 not in checkpoints:
        checkpoints = [0] + checkpoints

    trajectory_log = []
    eval_log = []

    # 0 检查点先用初始状态做一次评测（基线）
    eval_battery = EvalBattery(agent_state=env.state.snapshot(), llm_client=client)
    eval_result = eval_battery.run()
    eval_log.append(
        {
            "checkpoint": 0,
            "accuracy": eval_result.accuracy,
            "planning_score": eval_result.planning_score,
            "decision_score": eval_result.decision_score,
            "calibration": eval_result.calibration,
            "memory_score": eval_result.memory_score,
        }
    )

    for cp in checkpoints:
        if cp == 0:
            continue
        # 把环境推进到 cp
        while env.state.step < cp:
            prompt = env.user_prompt()
            extra = ""
            if external_text_provider is not None and quota_per_100 > 0 and env.state.step % 100 == 0:
                extra = external_text_provider(env.state.step)
            resp: LLMResponse = client.complete(prompt + ("\n" + extra if extra else ""), system=env.system_prompt())
            reward, done, info = env.step(resp.text)
            trajectory_log.append(
                {
                    "step": env.state.step,
                    "action": info["action"],
                    "reward": reward,
                    "latency_ms": resp.latency_ms,
                    "tokens": resp.token_count,
                }
            )
            if done:
                break

        # 从 cp 启动评测克隆
        eval_battery = EvalBattery(agent_state=env.state.snapshot(), llm_client=client)
        eval_result = eval_battery.run()
        eval_log.append(
            {
                "checkpoint": env.state.step,
                "accuracy": eval_result.accuracy,
                "planning_score": eval_result.planning_score,
                "decision_score": eval_result.decision_score,
                "calibration": eval_result.calibration,
                "memory_score": eval_result.memory_score,
            }
        )

    return {
        "model": model_id,
        "task": task,
        "condition": condition,
        "seed": seed,
        "max_steps": steps,
        "final_balance": env.state.balance,
        "final_step": env.state.step,
        "trajectory": trajectory_log,
        "evaluations": eval_log,
    }