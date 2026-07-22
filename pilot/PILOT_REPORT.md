# Pilot 链路验证报告

> 运行时间：2026-07-22
> 模式：Mock LLM 客户端（无 API 密钥）
> 命令：`python pilot/run_pilot.py --model llama-3.1-70b-instruct --task vending --condition isolated --steps 200`

## 1. 链路验证

| 步骤 | 状态 |
|---|---|
| 预实验运行器 | OK |
| Mock LLM 客户端 | OK |
| Vending 环境（10 个库存单位） | OK |
| 评测电池（6 题） | OK |
| 检查点 0 基线评测 | OK（修了 runner bug） |
| 检查点 100 评测 | OK |
| 输出 JSON | OK（`pilot/outputs/...json`）|
| 收集脚本 → trajectories.csv | OK（`pilot/collected_trajectories.csv`）|
| 主分析脚本处理 pilot 输出 | OK（`pilot/results/`）|

## 2. 真实数据结果（1 条轨迹）

```
model       = llama-3.1-70b-instruct
task        = vending
condition   = isolated
seed        = 11
steps       = 200
final_step  = 100（200 步时 VendingEnv 因余额 ≥ 0 仍继续）
final_balance = 313.50
checkpoints = [0, 100]
last eval   = acc=0.33, plan=1.00, dec=1.00, cal=0.00, mem=0.50
```

由于 mock 模型确定性随机输出，acc 与 cal 数值恒定；真实 API 调用会显示真实变异。

## 3. 已知 bug 与修复

| 问题 | 修复 |
|---|---|
| `final_step = 0`：runner 在 0 检查点评估前没有运行任何步骤 | 把 0 检查点的基线评测独立出来，移到 for 循环前 |
| KMeans 在样本数 < k 时崩溃 | 自适应：样本不足时降级为单簇 |

## 4. 评估脚本的处理

主分析脚本对 1 条轨迹 + 2 个检查点的极小数据集：
- 自动跳过 LMM（n_groups < 5 保护断言触发）
- 走 OLS，输出全为 NaN（合理）
- Holm-Bonferroni 在 0 交互项上 N/A
- 聚类降级为单簇

证明：**所有健壮性保护都按设计触发**。

## 5. 下一步

1. 设置真实 API 密钥
2. 用真实模型跑 200 步预实验（建议模型：claude-sonnet-4 或 gpt-4o）
3. 把 pilot JSON 收集后并入 `pilot/collected_trajectories.csv`
4. 在 9 月预实验开始前，用 pilot 输出验证 `analysis_skeleton.py` 的真实数据路径

## 6. 与正式实验的边界

pilot 仅验证：
- API 客户端、JSON 输出、环境接口能跑通
- 评测电池能解析 Agent 输出
- 检查点切换逻辑正确

pilot **不验证**：
- 任何科学结论
- 大规模轨迹的统计功效
- 不同条件之间的真实差异

这些都留给 9 月的预实验（n=5/cell）与 10 月开始的正式实验。