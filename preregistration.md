# Echo Chambers of One — Preregistration v0.2

> 状态：Stage 1 预注册 · 修订版
> 修订日期：2026-07-23
> 修订原因：v0.1-pre-reg 深度文献调研（LITERATURE_REVIEW.md）发现 5 个必须修订的设计盲点；本版本融合修订。
> 与 LITERATURE_REVIEW.md 配套阅读。

---

## 1. 研究问题

有状态语言智能体在长时间闭环运行中，**外源交互剥夺（absence of fresh external input, corrective feedback, or peer coordination）** 是否独立于**任务长度**、**上下文污染（context rot）**、**记忆容量**与**模型能力**，因果性地导致可量化的能力下降？

## 2. 核心假设（3 confirmatory + 2 exploratory）

### Confirmatory
- **H1.** 在所有 3 任务、3 模型、4 长度上，"isolated" 条件的纵向能力曲线显著低于含外部信号的 5 个条件。
- **H2.** "feedback" 条件比 "novelty" 条件斜率更正（纠错信息比纯新颖性更稀缺）。
- **H3.** 在 4 长度操纵下，"context rot × isolation" 交互显著：上下文越长，isolated 组与 feedback 组的斜率差异越大（最直接的"因式交互"证据）。

### Exploratory
- **H4.** 8 种反孤独机制中，External grounding / Episodic recall / Independent critic 的效应最大；Periodic reset / Source tagging 的效应在严格基准上消失。
- **H5.** 失败归因 schema 中"历史错误累积"类别在 isolated 组占比 > 50%；在 feedback / human 组占比 < 25%。

## 3. 设计

### 3.1 主网格

| 维度 | 值 | 备注 |
|---|---|---|
| 模型 | **3**：`deepseek-v4-flash`、`claude-sonnet-4`、`gpt-4o` | 闭源 + 长上下文主力；从 v0.1 的 7 模型缩减以控制预算 |
| 长度 | **4**：`4K`、`32K`、`128K`、模型上限（V4 Flash 为 1M）| 新增正交维度；强制 6 条件在 cell 内 token 总数等价 |
| 条件 | **6**：`control_stateless` / `isolated` / `novelty` / `feedback` / `peer` / `human` | 保持 v0.1 |
| 任务 | **3**：Vending-Bench 风格 / LongMemEval 风格 / HELMET 风格长上下文推理 | 每任务覆盖一种假设机制 |
| 重复 | **3 seeds** | Vending-Bench 报告 run-to-run 方差极大，3 seed 提供 IQR |

**正式 cell 数** = 3 × 4 × 6 × 3 × 3 = **648 cell**，总计 1944 轨迹。

### 3.2 任务正交化（修订关键点）

| 任务 | 主导假设机制 | 来源 | 评分维度 |
|---|---|---|---|
| T1: Vending-Bench 风格 | 决策漂移（strategic drift） | Andon Labs 2025 | balance survival, pricing accuracy, restock rationality |
| T2: LongMemEval 风格 | 记忆丢失（memory loss） | Wu et al. 2025 ICLR | fact recall, temporal consistency, contradiction rate |
| T3: HELMET 风格长上下文推理 | 上下文污染（context rot） | Princeton 2024 ICLR | needle accuracy, full-context reasoning, multi-hop |

**3 任务正交覆盖**三种假设机制——这是 v0.2 相对 v0.1 的关键修订。

## 4. 6 条件（保持 v0.1 不变）

| 条件 | 外部信号 | 工具权限 | 任务长度匹配 |
|---|---|---|---|
| `control_stateless` | 无（仅工具结果）| 全部 | 等价 |
| `isolated` | 无（除任务反馈）| 全部 | 等价 |
| `novelty` | 任务无关外部文档 | 全部 | 等价 |
| `feedback` | 外部标量对错信号 | 全部 | 等价 |
| `peer` | 同等 token 预算的同伴回复 | 全部 | 等价 |
| `human` | 人类监督（Prolific, n=20）| 全部 | 等价 |

**关键约束**：6 条件在 token 总预算、记忆容量、工具权限、任务序列上**完全相同**。差异仅在外部信号类型。

## 5. 4 状态视图反事实（修订关键点）

为排除 context rot 与 isolated 效应混淆，每 1000 步在评测克隆上注入 4 种状态视图：

| 视图 | 内容 |
|---|---|
| (a) 完整原始 | 主 Agent 看到的全部状态 |
| (b) 无损结构化 | 同等长度但以 JSON 表格组织 |
| (c) 等长但含错误记忆 | 注入 3 条伪造历史记录（与主 Agent 一致长度）|
| (d) 等长无关填充 | 注入与任务无关的 Lorem Ipsum |

**判定规则**：仅当 isolated 组在 (a)(b) 视图下都低于 feedback 组，且 (c) 下两条件差异消失，才判定 isolated 效应是真正的"孤独"。

## 6. 失败归因 schema（修订关键点）

借鉴 HORIZON（arXiv:2604.11978），每条轨迹失败时由独立 LLM-as-a-Judge 归因为三类（不允许多选）：

| 类别 | 定义 |
|---|---|
| Planning failure | 当前动作选择与目标不一致 |
| Memory loss | 与过去动作或事实相矛盾 |
| Historical error accumulation | 早期错误的自我循环放大 |

作为次要 outcome，配合 H1/H2/H5 的检验。

## 7. 主分析

纵向 LMM（与 v0.1 一致，但加入新交互）：

```
y_{i,t} = β0 + β1·log(1+t) + β2·C_c + β3·log(1+t)×C_c
        + β4·L_l + β5·log(1+t)×L_l
        + β6·log(1+t)×C_c×L_l
        + u_model + u_task + u_seed + ε
```

- **核心检验**：
  - H1: β3 < 0 对 isolated（reference = feedback）
  - H2: β3 比较 feedback vs novelty
  - H3: β6 显著（交互项）
- **随机效应**：model, task, seed
- **回退链**：LMM → GEE (independence) → OLS（同 v0.1）
- **保护断言**：`n_groups < 5` → 直接 OLS（已在 analysis_skeleton.py 实现）

## 8. 8 种反退化机制（消融子实验）

作为探索性子实验，仅在 isolated 基线上做单因素消融：

| 机制 | 来源 | 预期效应 |
|---|---|---|
| 1. Self-talk | Wei et al. 2022 CoT | **可能反向**（NoLiMa 警示）|
| 2. Episodic recall (A-MEM) | arXiv:2502.12110 | 中等 |
| 3. Source tagging (HippoRAG 2) | arXiv:2502.14802 | 中等 |
| 4. Periodic reset | 无强独立证据 | **可能假阳性** |
| 5. External grounding (CRAG) | arXiv:2401.15884 | 大 |
| 6. Independent critic (LATS) | arXiv:2310.04406 | 大（若真正独立）|
| 7. Semantic compression (Mem0) | arXiv:2504.19413 | 中等 |
| 8. Grounding document (LoCoMo) | arXiv:2402.17753 | 中等 |

**对抗控制**（修订关键点）：增加 **oracle feedback** 与 **adversarial feedback** 两种条件，保证 self-talk 不是"反思"独苗。

## 9. 排除规则（保持 v0.1）

- API 失败率 > 20% 的轨迹剔除并替换
- 工具返回缺失 > 50% 的轨迹剔除并替换
- 环境崩溃导致的轨迹剔除并替换
- **不**基于性能排除

## 10. 偏离预案（扩充）

| 情况 | 处理 |
|---|---|
| LMM 随机效应协方差奇异 | LMM → GEE → OLS 三级回退（已实现）|
| `n_groups < 5` per cell | 直接 OLS（保护断言）|
| API 失败率 > 20% | 整 cell 剔除 + 报告 |
| Holm 校正后全阴性 | 报告"无效应"；附 BH-FDR |
| DeepSeek V4 Flash 1M context 不可用 | 退回 128K 长度 |
| **新增**：self-talk 在无 oracle 反馈时反向 | 改测 semantic compression + independent critic 双因素 |
| **新增**：3 任务间交互模型不收敛 | 退到分任务 LMM，逐任务报告 |

## 11. 算力预算（重算）

- 总轨迹数：1944
- 每轨迹 token：10000 步 × 200 token/步 = 2M
- 总 token：1944 × 2M = 3.89B
- 按 70% DeepSeek V4 Flash（缓存命中 $0.0028/1M）+ 30% 闭源（平均 $3/1M）：
  - DeepSeek 部分：2720M token × $0.0028 = $7.6
  - 闭源部分：1170M token × $3 = $3500
  - **总预算：$3000–$5000**

预算超出原估算 10 倍——可通过 ① 减闭源模型为 1 个（只留 claude-sonnet-4 作 baseline），② 缩 trajectory 到 5000 步 → 预算回到 $1500–$2500。

## 12. 时间线（保持 v0.1）

- 2026-07-22 → 2026-08-15：Stage 1 内部审阅 + 修订（当前）
- 2026-08-15 → 2026-09-01：OSF 预登记冻结
- 2026-09-01 → 2026-09-15：AAMAS 2027 RR 通道投稿
- 2026-09 → 2026-10：pilot（n=3/cell）
- 2026-10 → 2026-12：正式数据收集
- 2027-01 → 2027-02：Stage 2 完整论文

## 13. 公开数据

- 代码：MIT
- 数据（脱敏后）：CC-BY-4.0
- 预注册（冻结版）：CC-BY-4.0
- LMM 详细输出：CC-BY-4.0
- 失败归因标签：CC-BY-4.0

---

**End of pre-registration. Frozen on Stage 1 acceptance.**

**主要修订（v0.1 → v0.2）**：
1. 7 模型 → 3 模型（专注闭源 + 1M 上下文主力）
2. 引入"长度操纵"作为第 4 正交维度
3. 3 任务正交化（决策 / 记忆 / 推理各覆盖一种机制）
4. 4 状态视图反事实（排除 context rot）
5. 失败归因 schema（次要 outcome）
6. 8 机制加对抗控制（oracle / adversarial feedback）
7. 重复数从 ≥20 降到 3（Vending-Bench 方差大，3 seed 提供 IQR）
8. 预算重算与时间线同步