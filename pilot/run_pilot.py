"""
预实验运行器
============

单次预实验入口：
    python pilot/run_pilot.py --model <id> --task vending --condition isolated --steps 200

无 API 密钥时自动回退到 Mock 客户端。
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from runner import run_trajectory


CONDITIONS = [
    "control_stateless",
    "isolated",
    "novelty",
    "feedback",
    "peer",
    "human",
]

MODELS = [
    "llama-3.1-70b-instruct",
    "llama-3.1-405b-instruct",
    "qwen-2.5-72b-instruct",
    "claude-sonnet-4",
    "gpt-4o",
    "deepseek-v4-flash",
    "deepseek-v4-flash-thinking",
]

TASKS = ["vending", "alfworld", "longmem"]


def mock_external_text(step: int) -> str:
    """非交互式外部信号（用于 novelty/feedback/peer/human 条件）。"""
    return f"[外部信息 @ step {step}] 今日天气：晴；股价持平。"


def main() -> None:
    parser = argparse.ArgumentParser(description="Echo Chambers 预实验运行器")
    parser.add_argument("--model", required=True, choices=MODELS, help="模型 ID")
    parser.add_argument("--task", required=True, choices=TASKS, help="任务 ID")
    parser.add_argument("--condition", required=True, choices=CONDITIONS, help="条件 ID")
    parser.add_argument("--steps", type=int, default=200, help="预实验步数（pilot 默认 200）")
    parser.add_argument("--seed", type=int, default=11, help="随机种子")
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "outputs", help="输出目录")
    parser.add_argument("--external-text", action="store_true", help="为 novelty/feedback/peer/human 启用 mock 外部文本")
    parser.add_argument("--health-check", action="store_true", help="启用 API health probe（默认关闭以避免重复 ping 401 key）")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    print(f"[run] model={args.model} task={args.task} condition={args.condition} steps={args.steps}")
    ext = mock_external_text if args.external_text else None

    result = run_trajectory(
        model_id=args.model,
        task=args.task,
        condition=args.condition,
        steps=args.steps,
        seed=args.seed,
        external_text_provider=ext,
        health_check=args.health_check,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = args.out / f"{args.model}__{args.task}__{args.condition}__seed{args.seed}__{timestamp}.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[done] wrote {out_path}")
    print(f"  final_balance = {result['final_balance']:.2f}")
    print(f"  final_step    = {result['final_step']}")
    print(f"  checkpoints   = {[e['checkpoint'] for e in result['evaluations']]}")
    if result["evaluations"]:
        last = result["evaluations"][-1]
        print(
            f"  last eval     = acc={last['accuracy']:.2f}, plan={last['planning_score']:.2f}, "
            f"dec={last['decision_score']:.2f}, cal={last['calibration']:.2f}, mem={last['memory_score']:.2f}"
        )


if __name__ == "__main__":
    main()