"""
简化版 Vending-Bench 环境
========================

10 个库存单位、单一日历、有限的库存与现金流。Agent 必须在每一步
做出动作决策：进货、调价、等待或联系供应商。

接口与官方 Vending-Bench 不同：仅用于工程链路验证，不产生可发表结果。
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class VendingState:
    balance: float = 500.0
    inventory: dict[str, int] = field(default_factory=lambda: {f"item_{i}": 5 for i in range(10)})
    prices: dict[str, float] = field(default_factory=lambda: {f"item_{i}": 2.50 for i in range(10)})
    step: int = 0
    daily_fee: float = 5.0
    history: list[dict] = field(default_factory=list)

    def snapshot(self) -> dict:
        return {
            "balance": self.balance,
            "inventory": dict(self.inventory),
            "prices": dict(self.prices),
            "step": self.step,
        }

    @classmethod
    def from_snapshot(cls, snap: dict) -> "VendingState":
        s = cls()
        s.balance = snap["balance"]
        s.inventory = dict(snap["inventory"])
        s.prices = dict(snap["prices"])
        s.step = snap["step"]
        return s


class VendingEnv:
    """最小可运行版 Vending-Bench。"""

    def __init__(self, seed: int = 0) -> None:
        self.state = VendingState()
        self.seed = seed

    def system_prompt(self) -> str:
        return (
            "你是自动售货机的经营者。目标是最大化现金流。\n"
            "每一步给出动作：restock(item, qty) / set_price(item, price) / wait() / email_supplier(text)\n"
            "动作语法：<action>name(args)</action>"
        )

    def user_prompt(self) -> str:
        snap = self.state.snapshot()
        return (
            f"Step {snap['step']}\n"
            f"Balance: ${snap['balance']:.2f}\n"
            f"Inventory: {json.dumps(snap['inventory'], ensure_ascii=False)}\n"
            f"Prices: {json.dumps(snap['prices'], ensure_ascii=False)}\n"
            "下一步动作？"
        )

    def step(self, agent_output: str) -> tuple[float, bool, dict]:
        """返回 (reward, done, info)。"""
        prev_balance = self.state.balance
        action = self._parse_action(agent_output)
        info = {"action": action}

        if action["name"] == "restock":
            item = action.get("item", "item_0")
            qty = int(action.get("amount", 1))
            cost = qty * 1.0
            if self.state.balance >= cost:
                self.state.balance -= cost
                self.state.inventory[item] = self.state.inventory.get(item, 0) + qty
        elif action["name"] == "set_price":
            item = action.get("item", "item_0")
            price = float(action.get("amount", 2.5))
            self.state.prices[item] = price
        elif action["name"] == "wait":
            pass
        elif action["name"] == "email_supplier":
            # 不触发外部动作，仅占位
            pass

        # 每日费用 + 随机销售
        self.state.balance -= self.state.daily_fee
        for item in list(self.state.inventory.keys()):
            if self.state.inventory[item] > 0:
                sold = min(self.state.inventory[item], 1)
                self.state.inventory[item] -= sold
                self.state.balance += self.state.prices[item] * sold

        reward = self.state.balance - prev_balance
        self.state.step += 1
        self.state.history.append({"step": self.state.step, "balance": self.state.balance, "reward": reward, "action": action})
        done = self.state.balance < 0 or self.state.step >= 10_000
        return reward, done, info

    @staticmethod
    def _parse_action(text: str) -> dict:
        """从 <action>...</action> 提取 name + kwargs。"""
        import re

        m = re.search(r"<action>(.+?)</action>", text, re.DOTALL)
        if not m:
            return {"name": "wait", "amount": 0}
        body = m.group(1).strip()
        # name(arg=val, arg=val)
        if "(" in body:
            name, rest = body.split("(", 1)
            rest = rest.rstrip(")")
            kwargs = {}
            for part in rest.split(","):
                if "=" in part:
                    k, v = part.split("=", 1)
                    kwargs[k.strip()] = v.strip().strip("'\"")
            return {"name": name.strip(), **kwargs}
        return {"name": body, "amount": 0}

    def save_state(self, path: Path) -> None:
        path.write_text(json.dumps(self.state.snapshot(), indent=2), encoding="utf-8")

    def load_state(self, path: Path) -> None:
        self.state = VendingState.from_snapshot(json.loads(path.read_text(encoding="utf-8")))