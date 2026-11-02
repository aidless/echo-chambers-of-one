# Bench — 外源交互剥夺实验基准（预注册阶段）

> 本目录登记 echo-chambers-of-one 的**真实基准**：实验设计网格 + 统计骨架在合成数据上的
> 端到端验证结果。所有数字都能从 `smoke_test/results/` 落盘文件重取。
> **关键边界**：本仓库处于**预注册阶段（v0.4）**，**不含任何真实 API 实验数据**。
> 下列全部数字来自**合成数据 / Mock 客户端**，**不构成**对「外源交互剥夺损害长程智能体」的经验证据。

## 基准 1 — 实验设计网格（预注册 v0.4，`experiment_manifest.json`）

| 维度 | 值 | 来源 |
|---|---|---|
| 模型 | 3（deepseek-v4-flash 1M / claude-sonnet-4 / gpt-4o） | `experiment_manifest.json` |
| 条件 | 6（含 isolated 外源剥夺、human/peer/feedback/novelty/control_stateless 对抗） | 同上 |
| 任务 | 3（正交覆盖 3 种失败机制） | 同上 |
| 长度 | 4（正交维度） | 同上 |
| 重复 | 3 | 同上 |
| Cell 数 | 648 | 同上 |
| 轨迹数 | 1944 | 同上 |

## 基准 2 — 统计骨架合成验证（`smoke_test/results/`，真实跑出）

| 指标 | 值 | 来源 |
|---|---|---|
| 总观测数 | 2,268 | `smoke_test/results/lmm_results.json`（accuracy.n_obs） |
| 独立轨迹 | 324 | 同上（accuracy.n_groups） |
| 隔离组平均 accuracy | 0.236（最低） | `smoke_test/results/REPORT.md` §1 |
| 人类组平均 accuracy | 0.782（最高） | 同上 |
| 主交互 `cond_human_x_logstep` | +0.0867（Holm-Bonferroni 校正 p<0.001） | `lmm_results.json`（fixed_effects） |
| 交互项全部为正 | 5/5（human/control/feedback/peer/novelty 斜率均高于隔离组） | `REPORT.md` §3 |
| 失败模式聚类 | 5 类（k=5 KMeans） | `smoke_test/results/failure_clusters.csv` |
| 拟合方法 | LMM→OLS 回退（合成轨迹单调→随机截距奇异→自动降级） | `REPORT.md` §2 |

- **判读**：骨架端到端可运行，5 个交互项全部为正且显著——但这**是合成数据的设计产物，不是发现**。
- **边界**：样本量小（每 cell n=3，效应量被高估）；合成衰减由生成器硬编码，非真实涌现。

## 基准 3 — Fail-closed 行为（真实代码，`analysis_skeleton.py`）

| 机制 | 真实行为 | 代码位置 |
|---|---|---|
| 低功效保护断言 | `n_groups < 5` 时**直接走 pooled OLS**，跳过 LMM/GEE（`low_power_cell` 门） | `analysis_skeleton.py:129-161` |
| LMM 奇异回退 | 随机效应协方差奇异 / LinAlgError → 回退 GEE → OLS | `analysis_skeleton.py:164-216` |
| 保护断言语义 | 不把不可靠的 LMM 输出当结果，宁可降级到更保守的 OLS | `analysis_skeleton.py:112-115` |

- **判读**：这是**fail-closed**——统计方法选择宁可保守降级，不产出可能不可靠的混合效应估计。
- **边界**：`low_power_cell` 只挡**样本量**维度；不挡模型误设或异常值（正式实验需另行诊断）。

## 复跑命令（无需 API 密钥）

```bash
# 基准 2：生成合成轨迹 + 跑骨架（两条命令实测通过）
python smoke_test/generate_synthetic_trajectories.py
python analysis_skeleton.py --csv smoke_test/trajectories.csv \
    --out smoke_test/results --reference isolated
```

> ⚠️ 注意：`generate_synthetic_trajectories.py` 的 `base_score()` 用 Python 内置 `hash()`
> 于字符串元组，字符串哈希**按进程加盐**（`PYTHONHASHSEED`）。重跑会让 `lmm_results.json`
> 的系数在最后几位漂移（实测 `cond_human_x_logstep` 0.08674 → 0.08507）。
> **这不是实验结论，是合成数据生成器的确定性边界**——正式实验数据由真实 API 产生，不受此影响。
