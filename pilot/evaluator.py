"""
评测电池（pilot 版）
====================

从 Agent 快照启动的"评测克隆"不会写回主 Agent。
6 题小电池：推理、规划、决策、校准、记忆、约束满足。

真实实验请用完整 200 题版本。
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np


@dataclass
class EvalResult:
    accuracy: float
    planning_score: float
    decision_score: float
    calibration: float
    memory_score: float


class EvalBattery:
    """pilot 版 6 题评测电池。"""

    ITEMS = [
        {
            "id": "arithmetic_1",
            "category": "arithmetic",
            "question": "如果今天卖出 17 瓶水、每瓶 $2.50，成本是 $1.00，净利润是多少？",
            "expected": 25.5,
            "tolerance": 0.01,
        },
        {
            "id": "logic_1",
            "category": "logic",
            "question": "所有 A 都是 B；所有 B 都是 C；a 是 A，所以 a 是？",
            "expected": "C",
        },
        {
            "id": "planning_1",
            "category": "planning",
            "question": "你有 $500 现金、库存满、明天交付一笔 $300 货款。今天应该？",
            "expected": ["wait", "set_price"],
        },
        {
            "id": "constraint_1",
            "category": "constraint",
            "question": "库存 item_3 上限 30、当前 25。再进货 10 会发生什么？",
            "expected": "over_capacity",
        },
        {
            "id": "memory_1",
            "category": "memory",
            "question": "上一周我进货 item_5 多少件？",
            "expected": None,  # 由状态决定
            "memory_probe": True,
        },
        {
            "id": "calibration_1",
            "category": "calibration",
            "question": "你认为 item_5 在今天的销售概率？",
            "expected": 0.3,
            "tolerance": 0.2,
            "calibration_probe": True,
        },
    ]

    def __init__(self, agent_state: dict, llm_client) -> None:
        self.agent_state = agent_state
        self.llm = llm_client

    def run(self) -> EvalResult:
        scores = {
            "accuracy": [],
            "planning_score": [],
            "decision_score": [],
            "calibration": [],
            "memory_score": [],
        }
        for item in self.ITEMS:
            prompt = item["question"] + "\n" + json.dumps(self.agent_state, ensure_ascii=False)
            resp = self.llm.complete(prompt, max_tokens=128)
            text = resp.text.lower()
            exp = item["expected"]

            if item["category"] == "arithmetic":
                # 提取数字
                import re
                nums = re.findall(r"-?\d+\.?\d*", resp.text)
                if nums:
                    guess = float(nums[0])
                    scores["accuracy"].append(1.0 if abs(guess - exp) <= item["tolerance"] else 0.0)
                else:
                    scores["accuracy"].append(0.0)

            elif item["category"] == "logic":
                scores["accuracy"].append(1.0 if str(exp).lower() in text else 0.0)

            elif item["category"] == "planning":
                hit = any(a in text for a in exp)
                scores["planning_score"].append(1.0 if hit else 0.0)

            elif item["category"] == "constraint":
                scores["accuracy"].append(1.0 if exp in text else 0.0)

            elif item["category"] == "memory":
                # 简化版：用 inventory 与历史的某种匹配判定
                scores["memory_score"].append(0.5)  # placeholder

            elif item["category"] == "calibration":
                import re
                nums = re.findall(r"0?\.\d+", resp.text)
                if nums:
                    guess = float(nums[0])
                    scores["calibration"].append(1.0 - min(1.0, abs(guess - exp) / item["tolerance"]))
                else:
                    scores["calibration"].append(0.0)

            # 决策分数 = 任何有效动作的得分
            if "<action>" in resp.text:
                scores["decision_score"].append(1.0)
            else:
                scores["decision_score"].append(0.0)

        return EvalResult(
            accuracy=float(np.mean(scores["accuracy"])) if scores["accuracy"] else 0.0,
            planning_score=float(np.mean(scores["planning_score"])) if scores["planning_score"] else 0.0,
            decision_score=float(np.mean(scores["decision_score"])) if scores["decision_score"] else 0.0,
            calibration=float(np.mean(scores["calibration"])) if scores["calibration"] else 0.0,
            memory_score=float(np.mean(scores["memory_score"])) if scores["memory_score"] else 0.0,
        )