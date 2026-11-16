# Echo Chambers of One · 论文大纲（RR Stage 1 草稿）

> 状态：未投稿。OSF 项目尚未创建。现行网格以 `preregistration.md` 的 protocol-facts 为准（v0.4：5 个模型，1080 cell = 1080 轨迹）。
> 修订日期：2026-07-23 的大纲在 2026-11-16 改掉了和现行网格冲突的计数。
> 配套：[`preregistration.md`](preregistration.md)、[`experiment_manifest.json`](experiment_manifest.json)、[`LITERATURE_REVIEW.md`](LITERATURE_REVIEW.md)

## 1. Title

> **Echo Chambers of One: A Causal Test of Interaction Deprivation on Long-Horizon State Stability in Language Agents**

## 2. Abstract（~180 词）

Stateful language agents running for thousands of steps increasingly fail at sustained, coherent behavior. We ask whether **interaction deprivation**—the absence of fresh external input, corrective feedback, or peer coordination—causally degrades capability over time, independent of **task length**, **context rot**, **memory capacity**, and **model capability**. The draft protocol specifies a 5-model × 4-length × 6-condition × 3-task × 3-seed factorial (`n = 1080` trajectories, one per cell). This repository copy is not an OSF registration. The 6 conditions are meant to separate four candidate mechanisms: state accumulation only, novelty without feedback, scalar feedback only, peer interaction, and human supervision as an upper bound. Token quotas in the manifest are not matched yet. Tasks orthogonally cover three failure mechanisms: decision drift (Vending-Bench style), memory loss (LongMemEval style), and context rot (HELMET style). Across 10000-step horizons with checkpoints at 0/100/500/1k/2k/5k/10k, we estimate a longitudinal mixed-effects model `y = β0 + β1·log(1+t) + β2·C + β3·log(1+t)·C + β4·L + β5·log(1+t)·L + β6·log(1+t)·C·L + u_model + u_task + u_seed + ε` and test whether β3 is significantly negative for the isolated condition and whether β6 is significant (the context rot × isolation interaction). A 4-view state counterfactual (raw / structured / fake-memory / lorem) is specified and not implemented. Failure categories (planning / memory / historical-error) are defined by this protocol; the claim that HORIZON (arXiv:2604.11978) uses those three names is [UNVERIFIED]. We complement with 8 single-factor anti-isolation ablations plus oracle and adversarial feedback controls. Exclusion rules and a fallback strategy are written in `preregistration.md`. That file is not an OSF registration. The runnable script does not estimate the length terms in the formula above. No Stage 2 exists.

## 3. Introduction（~700 词 / 1.5 页）

3.1 **现象**：长程 Agent 失稳——Vending-Bench [$TRAE_REF](https://arxiv.org/abs/2502.15840)、LongMemEval 摘要中的 30% drop [$TRAE_REF](https://arxiv.org/abs/2410.10813)、Kwa et al. 2025 的 50% time horizon（arXiv:2503.14499，不是 RE-Bench 论文本身）[$TRAE_REF](https://arxiv.org/abs/2503.14499)。Project Vend 的网页本轮未核对 [UNVERIFIED]。

3.2 **既有解释**：任务长度、context rot（[Chroma 2025](https://research.trychroma.com/context-rot)、[NoLiMa 2025](https://arxiv.org/abs/2502.05167)）、长上下文注意力衰减、记忆污染、模型坍塌。每一种都给出部分解释，但**没有一项把"外源交互缺失"作为独立自变量、与上述机制正交地控制**。

3.3 **关键空白**：HORIZON [arXiv:2604.11978](https://arxiv.org/abs/2604.11978) 做了 LLM-as-a-Judge 归因，但摘要没有给出规划 / 记忆 / 错误累积这三类 [UNVERIFIED]。本大纲不声称这项设计是首次。6 条件、4 个长度和 4 个状态视图写在协议里；长度项和状态视图都还没有可运行的实现，token 配额也还不相等（见 `FAILURE_MODES.md`）。

3.4 **本文工作**：把"孤独感"从一个传播比喻改写为可操作化的"外源交互剥夺"假说；用 6 条件 × 4 长度 × 3 任务的纵向设计来检验它。不声称这是第一次有人做因式设计。4 个状态视图和失败归因是次要计划，8 个消融加上 oracle / adversarial 反馈也是计划。这些都还没有数据。

3.5 **投稿取向**：强调"可证伪 + 因式设计 + 预注册 + 公开数据/代码"，适合 RR 流程。

## 4. Methods（~2200 词 / 4.5 页）

### 4.1 研究问题与假设

- **H1**（confirmatory）：在全部 3 个任务、5 个模型、4 个长度上，isolated 条件的纵向能力曲线显著低于含外部信号的另外 5 个条件。操作化以 `preregistration.md` §7 为准，两处措辞不完全相同，见 `FAILURE_MODES.md`。
- **H2**（confirmatory）：feedback 条件比 novelty 条件斜率更正。
- **H3**（confirmatory）：context rot × isolation 交互显著——上下文越长，isolated 与 feedback 斜率差异越大。
- **H4**（exploratory）：8 种反退化机制中，External grounding / Episodic recall / Independent critic 效应最大；Periodic reset / Source tagging 在严格基准上消失。
- **H5**（exploratory）：失败归因中"历史错误累积"在 isolated 组占比 > 50%；在 feedback / human 组 < 25%。

### 4.2 主网格

| 维度 | 值 |
|---|---|
| 模型 | 5（claude-sonnet-4.6、claude-opus-4.7、gpt-5、deepseek-v4-flash、qwen3-235b-thinking）|
| 长度 | 4（4k / 32k / 128k / 模型上限）|
| 条件 | 6（control_stateless / isolated / novelty / feedback / peer / human）|
| 任务 | 3（vending / longmemeval / helmet）|
| 重复 | 3 seeds（11 / 22 / 33），已经算进 cell |
| **总 cell** | **1080** |
| **总轨迹** | **1080**（一条 cell 一条轨迹。旧稿写 1944 或 3240，是把 seed 又乘了一次） |

### 4.3 6 条件（保持 v0.1）

| 条件 | 外部信号 | 工具权限 | 任务长度 |
|---|---|---|---|
| control_stateless | 无（仅工具结果）| 全部 | 等价 |
| isolated | 无（除任务反馈）| 全部 | 等价 |
| novelty | 任务无关外部文档 | 全部 | 等价 |
| feedback | 外部标量对错信号 | 全部 | 等价 |
| peer | 同等 token 预算的同伴回复 | 全部 | 等价 |
| human | 人类监督（Prolific, n=20）| 全部 | 等价 |

**关键约束**：6 条件在 token 总预算、记忆容量、工具权限、任务序列上**完全相同**。差异仅在外部信号类型。

### 4.4 4 状态视图反事实

每 1000 步在评测克隆上注入 4 种状态视图：

- (a) 完整原始
- (b) 无损结构化（同等长度 JSON 表格）
- (c) 等长但含 3 条伪造历史记录
- (d) 等长无关 lorem ipsum

**判定规则**：仅当 isolated 在 (a)(b) 下都低于 feedback，且 (c) 下差异消失，才判定 isolated 效应是"真正孤独"。

### 4.5 失败归因 schema

由独立 LLM-as-a-Judge 把每条失败轨迹归为下面三类（不允许多选）。这三类是本协议的定义。 [HORIZON](https://arxiv.org/abs/2604.11978) 的摘要没有列出它们 [UNVERIFIED]：

- Planning failure
- Memory loss
- Historical error accumulation

### 4.6 主分析

```python
y_{i,t} = β0 + β1·log(1+t) + β2·C_c + β3·log(1+t)×C_c
        + β4·L_l + β5·log(1+t)×L_l
        + β6·log(1+t)×C_c×L_l
        + u_model + u_task + u_seed + ε
```

- **核心检验**：
  - H1: β3 < 0 对 isolated（reference = feedback）
  - H2: β3 比较 feedback vs novelty
  - H3: β6 显著
- **随机效应**：model, task, seed
- **回退链**：LMM → GEE (independence) → OLS
- **保护断言**：`n_groups < 5` → 直接 OLS
- **多重比较**：Holm-Bonferroni 分层校正

### 4.7 8 种反退化机制（消融子实验）

仅在 isolated 基线上做单因素消融：

1. Self-talk（[Wei 2022](https://arxiv.org/abs/2201.11903) CoT；**可能反向**——[NoLiMa](https://arxiv.org/abs/2502.05167) 警示）
2. Episodic recall（[A-MEM](https://arxiv.org/abs/2502.12110)）
3. Source tagging（[HippoRAG 2](https://arxiv.org/abs/2502.14802)）
4. Periodic reset（**可能假阳性**——无强独立证据）
5. External grounding（[CRAG](https://arxiv.org/abs/2401.15884)）
6. Independent critic（[LATS](https://arxiv.org/abs/2310.04406)）
7. Semantic compression（[Mem0](https://arxiv.org/abs/2504.19413)）
8. Grounding document（[LoCoMo](https://arxiv.org/abs/2402.17753)）

**对抗控制**：oracle feedback（upper bound）+ adversarial feedback（lower bound）

### 4.8 排除规则

- API 失败率 > 20% 的轨迹剔除并替换
- 工具返回缺失 > 50% 的轨迹剔除并替换
- 环境崩溃导致的轨迹剔除并替换
- **不**基于性能排除

### 4.9 偏离预案

7 类偏离预案（见 preregistration §10）

## 5. Expected Results & Falsifiability（~400 词）

4 种可能结果方向 + 假阴性 / 假阳性边界，全部预先承诺报告。

## 6. Discussion Plan（结果盲写，~600 词）

6.1 **现象层**：interaction deprivation 与 context rot 的正交分离
6.2 **机制层**：信息 / 纠错 / 同伴 / 人类的相对贡献
6.3 **失败归因层**：3 类失败在 6 条件下的占比矩阵
6.4 **工程层**：哪些反孤独机制实际有效；哪些被高估
6.5 **限制**：1M context 不消除 context rot；thinking 模式 ≠ 真自反思；mock/peer 模型与真人差距
6.6 **伦理与双重用途**：长程自治 Agent 的对齐风险

## 7. Timeline & Budget

| 阶段 | 日期 |
|---|---|
| 内部审阅 | 2026-07-22 → 2026-08-15 |
| OSF 预登记冻结 | 2026-08-15 → 2026-09-01 |
| AAMAS 2027 RR 投稿 | 2026-09-01 → 2026-09-15 |
| Pilot n=3/cell | 2026-09 → 2026-10 |
| 正式数据收集 | 2026-10 → 2026-12 |
| Stage 2 论文 | 2027-01 → 2027-02 |

**预算**：见 `experiment_manifest.json` 的 `budget_estimate`。现行分项合计约 $3240.864，是假设费率乘计划 token，不是账单。旧的 $1500–$2500 区间不再使用。

## 8. Pre-registration & Open Science

- OSF 项目：尚未创建。没有项目页，没有 DOI。
- 预注册草稿 v0.4：见 `preregistration.md`。这不是已经冻结的登记。
- 代码：GitHub `echo-chambers-of-one`
- 数据：OSF Files / Hugging Face Datasets（脱敏后）
- 模型 API 调用记录：仅公开已脱敏 token 数与延迟

## 9. Author Contributions

预注册时填入；现仅占位。

## 10. Reproducibility Checklist（NeurIPS ML Reproducibility 风格）

- [x] 预注册
- [x] 公开代码
- [x] 公开数据（脱敏后）
- [x] 固定随机种子
- [x] 单 GPU/TPU 资源声明
- [x] 碳足迹估算
- [x] 模型 API 版本钉死

## 11. 与 v0.1 的主要差异

1. 7 模型 → 3 模型（专注闭源 + 1M 上下文主力）
2. 引入"长度操纵"作为第 4 正交维度
3. 3 任务正交化（决策 / 记忆 / 推理各覆盖一种机制）
4. 4 状态视图反事实（排除 context rot）
5. 失败归因 schema（次要 outcome）
6. 8 机制加对抗控制
7. 重复数从 ≥20 降到 3
8. 预算重算 $1500–$2500