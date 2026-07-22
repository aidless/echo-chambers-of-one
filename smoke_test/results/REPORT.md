# 烟雾测试报告

> 生成时间：2026-07-22
> 输入：`smoke_test/trajectories.csv`（2,268 行）
> 配置：6 模型 × 6 条件 × 3 任务 × 3 种子 × 7 检查点
> 工具：`analysis_skeleton.py`

## 1. 数据汇总

| 指标 | 值 |
|---|---|
| 总观测数 | 2,268 |
| 独立轨迹 | 324 |
| 隔离组平均 accuracy | 0.236（最低） |
| 人类组平均 accuracy | 0.782（最高） |

各条件整体均值：
```
control_stateless  0.719
feedback           0.637
human              0.782
isolated           0.236
novelty            0.447
peer               0.606
```

## 2. 模型拟合方法

由于合成轨迹每条只跨 7 个检查点且高度单调，共线性触发了 LMM 随机截距奇异矩阵。骨架脚本按设计回退到 `OLS`：
- `method = ols_fallback`
- 所有交互项 p 值仍能给出
- 真实实验里轨迹变异更大，LMM 可正常使用

## 3. 主结果（accuracy）

| 交互项 | 系数 | 含义 |
|---|---:|---|
| cond_human_x_logstep | +0.087 | 人类组斜率比隔离组高 0.087 |
| cond_control_stateless_x_logstep | +0.077 | 控制组斜率比隔离组高 0.077 |
| cond_feedback_x_logstep | +0.062 | 反馈组斜率比隔离组高 0.062 |
| cond_peer_x_logstep | +0.057 | 同伴组斜率比隔离组高 0.057 |
| cond_novelty_x_logstep | +0.031 | 新颖性组斜率比隔离组高 0.031 |

所有 5 个交互项系数 **全部为正**，且 Holm-Bonferroni 校正后 `p < 0.001`。这与合成假设一致：隔离组的纵向衰减最陡。

## 4. 指标一致性

`planning_score / decision_score / calibration / memory_score` 4 个指标上的交互项系数与 `accuracy` 完全同方向，幅度量级一致：
- `human` 与 `control_stateless` 在所有指标上斜率差异最大
- `novelty` 始终是最弱的有信号条件

## 5. 失败模式聚类

`failure_clusters.csv` 把 324 条轨迹分成 5 类（k=5 KMeans）。直观观察：
- 簇 0：低均值低最小值的轨迹，对应**隔离组在长程上的崩溃样本**
- 簇 1：高均值高最小值，对应**人类组与控制组的稳定轨迹**
- 簇 2 / 3 / 4：中间状态，对应**反馈、同伴、新颖性**条件下的轨迹

## 6. 已知限制

1. **LMM 奇异**：本次回退到 OLS。真实实验的轨迹变异更大，可直接用 LMM。
2. **样本量小**：每 cell n=3，效应量会被高估；正式实验需 n ≥ 20。
3. **合成假设**：隔离组衰减由生成器硬编码 (`slope × log(1+t)`)，不是真实涌现。脚本仅用于验证统计链路。

## 7. 链路验证清单

| 步骤 | 状态 |
|---|---|
| 数据合成 | OK |
| LMM 主模型 + 自动回退 | OK |
| Holm-Bonferroni 多重比较 | OK（25 个 cell 全部显著）|
| 失败模式聚类 | OK |
| JSON / CSV 输出 | OK（`lmm_results.json`, `interaction_tests.csv`, `failure_clusters.csv`）|

## 8. 下一步

1. 真实预实验前，把脚本的 fallback 行为加进预注册"偏离预案"。
2. 在主分析脚本顶部加一条断言：`n_groups < 5` 时直接走 OLS。
3. 在 OSF 创建项目并预注册当前文档。