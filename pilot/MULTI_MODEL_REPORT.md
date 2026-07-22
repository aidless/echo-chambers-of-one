# Pilot 多模型批量报告

> 时间：2026-07-22
> 命令：6 次 `python pilot/run_pilot.py`，3 模型 × 2 条件
> 模式：Mock（环境中 DeepSeek key 失效，自动懒探测回退）

## 1. 6 次 pilot 结果

| 模型 | 条件 | 终余额 | 终步数 | 检查点 |
|---|---|---:|---:|---|
| claude-sonnet-4 | isolated | 171.50 | 100 | [0, 100] |
| claude-sonnet-4 | feedback | 236.50 | 100 | [0, 100] |
| deepseek-v4-flash | isolated | 177.50 | 100 | [0, 100] |
| deepseek-v4-flash | feedback | 125.00 | 100 | [0, 100] |
| deepseek-v4-flash-thinking | isolated | 524.50 | 100 | [0, 100] |
| deepseek-v4-flash-thinking | feedback | 125.00 | 100 | [0, 100] |

注：
- 由于环境中 DeepSeek key 失效（`****689c` 401），所有 deepseek 调用都懒探测回退到 Mock。
- claude-sonnet-4 没有 `ANTHROPIC_API_KEY`，直接走 Mock。
- Mock 输出对每个模型都不同（因为模型名作为 hash 种子），但**仍为确定性的随机**，不能用于科学结论。

## 2. 链路验证状态

| 步骤 | 状态 |
|---|---|
| 3 模型 × 2 条件批量运行 | OK |
| 懒探测回退（401 → Mock） | OK |
| Vending 环境 200 步推进 | OK |
| 检查点 0/100 评测 | OK |
| 收集脚本 → CSV | OK（37 行）|
| 主分析脚本 | OK |
| Holm 校正 | OK（6 cell × 5 指标）|

## 3. 收集后分析输出

`pilot/results/lmm_results.json` 与 `interaction_tests.csv` 已生成。由于：
- n_groups = 6（>5），跳过保护断言
- 但每轨迹只 2 个时间点，LMM 仍然奇异 → 回退到 OLS
- 6 cell 中 isolated vs feedback 各占 3 cell，slope 系数在隔离组参照下接近 0（合理：Mock 数据无真实信号）

## 4. 启动真实 DeepSeek V4 Flash 预实验的步骤

```bash
# 1. 设置有效的 DeepSeek 密钥
setx DEEPSEEK_API_KEY "sk-真实密钥"

# 2. 启用 health check 验证
python pilot/run_pilot.py --model deepseek-v4-flash --task vending --condition isolated --steps 200 --health-check

# 3. 看到 [health] deepseek-v4-flash OK 后，正式批量跑
python pilot/run_pilot.py --model deepseek-v4-flash --task vending --condition isolated --steps 200
python pilot/run_pilot.py --model deepseek-v4-flash --task vending --condition feedback --steps 200 --seed 22
python pilot/run_pilot.py --model deepseek-v4-flash --task vending --condition novelty --steps 200 --seed 22
python pilot/run_pilot.py --model deepseek-v4-flash-thinking --task vending --condition isolated --steps 200 --seed 22

# 4. 收集并分析
python pilot/collect_outputs.py
python analysis_skeleton.py --csv pilot/collected_trajectories.csv --out pilot/results --reference isolated
```

## 5. Mock 与真实数据的差异

Mock 是确定性的、随 prompt 长度变化而变化，但**没有任何真实推理能力**：
- 同一 (model, condition, seed, prompt) → 完全相同输出
- 不同 (condition) 在 Mock 下**不会**自动产生有意义的差异
- 所有 final_balance、accuracy 等数字仅用于验证链路，无科学结论

真实数据 + V4 Flash 1M context 会带来：
- 真随机 + 高质量推理
- 同一条件内多条轨迹间应有真实方差
- 隔离 vs feedback 应出现稳定的能力差异信号

## 6. 下一步

1. 设置真实 DeepSeek API key
2. 跑真实 pre-reg 数据（每个 cell n=5）
3. 上传所有内容到 GitHub + OSF
4. 提交 AAMAS 2027 Stage 1