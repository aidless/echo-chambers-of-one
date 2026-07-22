# 预实验环境（pilot/）

> 目标：在 200 步、单模型、单任务、单条件下验证真实 API 调用的链路通畅，
> 为 9 月开始的完整预实验（n=5/cell）扫清工程障碍。

## 目录

```
pilot/
├── README.md           # 本文件
├── run_pilot.py        # 入口：单次预实验运行器
├── vending_env.py      # 简化版 Vending-Bench 环境
├── evaluator.py        # 评测电池（推理 / 规划 / 决策 / 校准 / 记忆）
├── llm_client.py       # 抽象 LLM 客户端（OpenAI / Anthropic / vLLM）
├── runner.py           # 单轨迹主循环
└── outputs/            # 预实验轨迹与日志
```

## 快速开始

```bash
# 1. 安装额外依赖
python -m pip install openai anthropic requests tiktoken

# 2. 设置 API 密钥
export OPENAI_API_KEY=...
# 或
setx OPENAI_API_KEY "..."

# 3. 运行 200 步预实验
python pilot/run_pilot.py \
    --model llama-3.1-70b-instruct \
    --task vending \
    --condition isolated \
    --steps 200 \
    --seed 11
```

输出会写入 `pilot/outputs/`，并在每 100 步保存状态快照 + 评测分数。

## 设计原则

1. **最小可运行**：单文件、单任务、单条件，便于快速调试。
2. **状态可快照**：每 100 步序列化 Agent 状态到磁盘，便于回放。
3. **评测隔离**：从快照启动的"评测克隆"不会把结果写回主 Agent。
4. **可降级**：无 API 密钥时使用 mock LLM 客户端（确定性随机输出）。

## 与正式实验的差异

| 维度 | 预实验 | 正式实验 |
|---|---|---|
| 模型数 | 1 | 6 |
| 任务数 | 1 | 3 |
| 条件数 | 1 | 6 |
| 步数 | 200 | 10000 |
| 重复 | 1 | ≥ 20 |
| 工具 | bash + read | bash / read / write / search / calculator |
| 评测电池 | 6 题 × 1 类 | 200 题 × 6 类 |

预实验只验证"工程链路能否跑通"，不分析任何科学结论。

## 已知限制

- Vending 环境是简化版（10 个库存单位、单一日历），不与官方 Vending-Bench 数值直接可比。
- Mock LLM 客户端会输出 `<think>...</think><action>...</action>`，仅用于本地测试 token 流。
- 真实 API 调用需要速率限制与错误重试逻辑，已写在 `llm_client.py`。