# Echo Chambers of One — Preregistration v0.4

> 状态：Stage 1 预注册 · 第三轮修订
> 修订日期：2026-07-29
> 修订来源：`LITERATURE_REVIEW_v3.md` 第三轮深挖（模型选型 + 伦理 + OSF 报告规范）
> 配套：`LITERATURE_REVIEW.md`（v0.1→v0.2）+ `LITERATURE_REVIEW_v2.md`（v0.2→v0.3）+ `LITERATURE_REVIEW_v3.md`（v0.3→v0.4）
> 相比 v0.3 增量：§3.1 模型从 3 个扩到 5 个（含开源锚 + thinking 受控变量）；新增 §15 伦理与 IRB；新增 §16 PRISMA 2020 章节映射；新增 §17 OSF 项目结构。

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
| 模型 | **5**（v0.4 修订）：claude-sonnet-4.6、claude-opus-4.7、gpt-5、deepseek-v4-flash、qwen3-235b-thinking | 闭源 3 + 开源 2；含 1M context 主力 + 天花板对照 + thinking 受控变量 |
| 长度 | **4**：`4K`、`32K`、`128K`、模型上限（V4 Flash / Sonnet / Opus / Qwen3 为 1M；GPT-5 为 256K）| 新增正交维度；强制 6 条件在所有 cell 内 token 总数等价 |
| 条件 | **6**：`control_stateless` / `isolated` / `novelty` / `feedback` / `peer` / `human` | 保持 v0.1 |
| 任务 | **3**：Vending-Bench 风格 / LongMemEval 风格 / HELMET 风格长上下文推理 | 每任务覆盖一种假设机制 |
| 重复 | **3 seeds** | Vending-Bench 报告 run-to-run 方差极大，3 seed 提供 IQR |

**正式 cell 数** = 5 × 4 × 6 × 3 × 3 = **1080 cell**，总计 **3240 轨迹**。

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

### 6.5 Judge 协议（v0.3 新增）

为避免 self-preference / position / verbosity 等系统性偏差，**预先承诺**以下元数据：

| 元数据 | 预承诺值 |
|---|---|
| Judge 主模型 | **Claude Sonnet 4**（与 agent 异源）|
| Judge 二号 | **DeepSeek-V3 Flash**（价格敏感，异源）|
| Judge 三号 | **Prometheus-2-7B**（专用 judge，2024 EMNLP）|
| 聚合方式 | weighted majority + Bradley-Terry 后处理 |
| Position 协议 | swap-and-average，每条 2 次随机化顺序 |
| Self-consistency | K=5 重复，主类一致率 ≥ 0.80 |
| Ensemble 一致性 | Krippendorff's α ≥ 0.667 |
| Few-shot 数量 | 8（来自人工 gold 集，**非**自 H5 待标注集）|
| Gold 集规模 | ≥ 50 人工双盲标注 |
| Anchor reference | 每条待标注旁附 1+ / 1- 失败归因示例 |
| **禁止配置** | Judge 与 Agent 同模型 + 同供应商；prompt 共享 > 30%；agent 自评做 gold |

依据：[Zheng et al. 2023 MT-Bench](https://arxiv.org/abs/2306.05685)、[Survey Gu 2024](https://arxiv.org/abs/2411.15594)、[Verga 2024 PoLL](https://arxiv.org/abs/2404.18796)、[Kim 2024 Prometheus 2](https://arxiv.org/abs/2405.01535)。

Stage 2 必报告：per-class precision/recall/F1、Cohen's κ、Krippendorff's α、self-consistency rate、position-swap disagreement rate、confusion matrix（planning ↔ memory 撞标签率）、per-1k-trajectory judge cost。

## 7. 主分析

纵向 LMM：

```
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
- **回退链**：LMM → GEE (independence) → brms（half-Cauchy 弱先验） → OLS
- **保护断言**：`n_groups < 5` → 直接 OLS
- **多重比较（v0.3 修订）**：
  - **主分析** = **Westfall-Young step-down minP permutation**（multcomp `adjusted("Westfall")`），999 抽样；不需独立性假设，在 25 强相关假设下功效提升 20–30%
  - **Sensitivity** = Holm-Bonferroni 分层校正（保留 v0.2 的方法作并列报告）
  - 两者结论一致 → 强证据；不一致 → 报告二者并讨论
- **8 ablation 检验方式（v0.3 修订）**：emmeans `joint_tests()` omnibus χ²/F 检验，**多重比较预算从 8×N 降到 8**

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

## 10. 偏离预案（v0.3 扩到 10 类）

| 情况 | 处理 |
|---|---|
| LMM 随机效应协方差奇异 | LMM → GEE (indep) → brms (half-Cauchy) → OLS 四级回退 |
| `n_groups < 5` per cell | 直接 OLS（保护断言）|
| API 失败率 > 20% | 整 cell 剔除 + 报告 |
| 主校正（Westfall-Young）后全阴 | 报告"无效应"；附 Holm 作 sensitivity |
| DeepSeek V4 Flash 1M context 不可用 | 退回 128K 长度 |
| self-talk 在无 oracle 反馈时反向 | 改测 semantic compression + independent critic 双因素 |
| 3 任务间交互模型不收敛 | 退到分任务 LMM，逐任务报告 |
| **v0.3 新增**：replicate < 计划数 | 报 post-hoc power；标记 `underpowered` |
| **v0.3 新增**：主分析失败 fallback | 退回分任务 LMM；主次分析并行报告 |
| **v0.3 新增**：peeking 触发 | 报告 peeking 时间点；切换 Bayesian sequential stopping plan（v0.4）|

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

## 13. 工程稳健性承诺（v0.3 新增）

依据 [OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/api_request_parallel_processor.py) + [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) + [OpenTelemetry GenAI semconv](https://github.com/open-telemetry/semantic-conventions-genai)，预先承诺：

1. **Cost-aware scheduler**：`CellSpec.max_dollars_per_cell`；累计 `usage.*.billed_cost` 实时计费；超限立即停跑
2. **统一 trace schema**：内层 raw provider 数据（OpenAI `usage.prompt_tokens_details.cached_tokens`、Anthropic `usage.cache_read_input_tokens`、DeepSeek `prompt_cache_hit_tokens`）+ 外层 OpenTelemetry GenAI semconv 投影
3. **Cache routing**：`prompt_cache_key` 绑定 `condition_id + model_id`（如 `ec_001_iso_ds4f`），**不**绑 `seed_id` → 同 cell 3 共享前缀 → 命中率 ≥ 80%
4. **断点续跑**：每 checkpoint 0/100/500/.../10000 后立即刷盘 + 写 sha256 sidecar
5. **Sonnet 4 thinking 预算审计**：用 `usage.output_tokens` 单独统计；超 1.5× buffer 标 `degraded_budget`
6. **gpt-4o 滚动窗口压缩**：每 1000 步抽取 summary，避免 200K 后 truncate

## 14. 公开数据

- 代码：MIT
- 数据（脱敏后）：CC-BY-4.0
- 预注册（冻结版）：CC-BY-4.0
- LMM 详细输出：CC-BY-4.0
- 失败归因标签：CC-BY-4.0

## 15. 伦理与 IRB（v0.4 新增）

本研究含 1 个"human"条件（Prolific 招募 n=20）与 1 个"human_validation"（≥50 人工双盲）真人参与环节，按 NeurIPS 2025 Code of Ethics 与 Stanford ESR 流程，预先承诺 5 项伦理字段：

### 15.1 IRB approval statement
"本研究的真人参与环节已向 [University] IRB 提交申请。Stage 1 数据采集启动前必须获得 approved 或 exempt 状态。预注册阶段写明 'IRB submission pending, expected approval by [date]'。"

### 15.2 Compensation & Fair Wage
- `human` 条件（n=20）：Prolific 招募，每场 30–45 min，**$15/h**（保守高于 Prolific 最低 $12/h 符合 NeurIPS 2025 "fair wages" 精神）+ 公平奖励金 $1–3
- `human_validation`（n≥50）：每条 6–10 min，**$18/h**（接近专业标注市场水平）

### 15.3 Data protection & Privacy plan
- **法规对标**：GDPR Art. 89 + UK GDPR + 中国《个人信息保护法》第 13、27 条
- **伪匿名化**：去除姓名 / 邮箱 / IP / 地理位置 / 设备 ID
- **数据保留 ≤ 2 年**；按 PIPL/GDPR 执行数据主体权利
- **不在公开 artifacts 中发布任何 PII**

### 15.4 Dual Use Risk Assessment
Stage 2 论文应包含 ≤ 1 页 "Dual Use & Mitigations" 子节：
1. Isolation ablation 可被误读的对抗面（揭示 agent 弱点→构造 jailbreak）
2. Stage 2 论文 red-team 计划（isolation 修复的 prompt injection 绕过测试）
3. 不发布 agent 完整 system prompt 的策略

### 15.5 Responsible Disclosure Protocol
若 Stage 1 发现严重 agent 安全/对齐问题，按 [Anthropic Responsible Disclosure Policy](https://www.anthropic.com/responsible-disclosure-policy) 私下通报（90 天）后再公开展示；failure cases 删除任何可被复制利用的 prompt 注入示例。

依据：[NeurIPS 2025 Code of Ethics](https://neurips.cc/public/EthicsGuidelines)、[Stanford ESR](https://casbs.stanford.edu/our-work/ethics-and-society-review)、[Prolific Pricing](https://www.prolific.com/pricing)、[EU AI Act Article 27](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)。

## 16. PRISMA 2020 章节映射（v0.4 新增）

按 [PRISMA 2020 (Page et al. BMJ 2021)](https://doi.org/10.1136/bmj.n71) 与 [CONSORT-AI / SPIRIT-AI](https://doi.org/10.1136/bmj.m3210)，本研究章节映射：

| PRISMA Item | 对应本研究章节 | 实施阶段 |
|---|---|---|
| 1. Title | `paper_outline.md` §1 | Stage 1 |
| 2. Abstract（结构化）| `paper_outline.md` §2 | Stage 1 + Stage 2 |
| 3. Rationale | `paper_outline.md` §3 | Stage 1 |
| 4. Objectives / PICOS | 本文档 §1–2 | Stage 1 |
| 5–6. Search strategy | 不适用（不涉及文献检索）| — |
| 7. Inclusion criteria | 本文档 §4（cell 准入）| Stage 1 |
| 8–10. Sources / Search | 不适用 | — |
| 11–12. Data items / Risk of bias | `LITERATURE_REVIEW.md` / `LITERATURE_REVIEW_v2.md` | Stage 1 |
| 13. Synthesis methods | 本文档 §7 | Stage 1 |
| 14–17. Reporting | `paper_outline.md` §4 | Stage 2 |
| 18. Risk of bias in studies | 见下文 §18 Internal Validity | Stage 2 |
| 19. Subgroup analyses | `experiment_manifest.json` `state_view_counterfactuals` | Stage 2 |
| 20–22. CERQual / Summary of evidence | Stage 2 报告 | Stage 2 |
| 23–25. Limitations / Conclusions | `paper_outline.md` §6 | Stage 2 |
| 26. Funding | 新增 §19 Funding & Registration | Stage 1 |
| 27. Registration (OSF DOI) | OSF Registration DOI | Stage 1 |

**CONSORT-AI 必含项**：LLM 版本（claude-sonnet-4.6 / claude-opus-4.7 / gpt-5 / deepseek-v4-flash / qwen3-235b-thinking 钉死）、prompt 模板（公开在 `code/`）、tool calling schema（公开在 `code/`）、human-AI interaction 协议（`human` 条件）、错误案例分析（Stage 2 失败归因）。

## 17. OSF 项目结构 + COS Badges（v0.4 新增）

### 17.1 OSF 项目结构

```
echo-chambers-of-one/
├── docs/           ← preregistration.md, paper_outline.md, RELEASES
├── data/raw/       ← trajectories（CC-BY 4.0）
├── data/agg/       ← aggregated metrics (CC0)
├── code/           ← analysis + scripts (MIT)
├── env/            ← Dockerfile + requirements.txt
├── wiki/           ← 变更日志、决策记录、可视化
└── registrations/  ← Stage 1 IPA 时间戳 + DOI
```

**OSF Registration 模板**：**Open-Ended Registration**（[OSF Help](https://help.osf.io/article/1454-preregistration-templates)），因 1080 cell 因式 + 10 类预案无法填 Standard 模板。DOI 通过 Add-on 4.0 单独为 Registration 申请。

### 17.2 COS Open Science Badges 申请计划

依据 [COS Open Science Badges](https://www.cos.io/our-services/badges)：

| Badge | 申请时间 | 状态 |
|---|---|---|
| **Preregistered** | OSF Registration 完成时 | Stage 1 |
| **Preregistered + Analysis Plan** | Stage 1 包含 10 类预案 + 主分析路径 | Stage 1 |
| **Open Data** | Stage 2 投稿前 | Stage 2 |
| **Open Materials** | Stage 2 投稿前 | Stage 2 |
| **Registered Report** | 期刊（AAMAS / JAAMAS / FAccT）接收 Stage 1 IPA 后 | 期刊决定 |

申请方式：投稿时在 disclosure statement 勾选（[osf.io/5fndw](https://osf.io/5fndw/) 模板）。

## 18. Internal Validity

按 PRISMA Item 18 与 NeurIPS 2024+ Reproducibility Checklist 5 分项：

| 维度 | 措施 |
|---|---|
| Code | MIT 公开 + 钉 commit hash |
| Model | 5 模型 + 钉版本号 + temperature + max_tokens |
| Data | raw + agg 公开 + 隐私脱敏 |
| Environment | `Dockerfile` + `requirements.txt` 钉死 |
| Training/Inference | 随机种子 11/22/33 + thread pool 钉死 + Judge 协议（见 §6.5）|

**Judge ensemble** 多次交叉验证（3 源异源 + position-swap + Bradley-Terry 聚合）保证标签质量。

## 19. Funding & Registration

- **Funding**：待填写（建议声明无任何模型供应商资助以保持独立性）
- **Registration**：[OSF Project DOI](https://osf.io/echo-chambers-of-one/)（待创建）
- **GitHub**：https://github.com/aidless/echo-chambers-of-one

---

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

**主要修订（v0.2 → v0.3）**：
1. **§7 主分析**：Holm-Bonferroni → **Westfall-Young step-down minP permutation 主 + Holm sensitivity**；回退链加 brms 一级（4 级回退）
2. **§6.5 Judge 协议（新增）**：Claude Sonnet 4 + DeepSeek-V3 + Prometheus-2-7B 三源 ensemble；position-swap；Krippendorff's α ≥ 0.667；self-consistency ≥ 0.80；Bradley-Terry 聚合
3. **§7 ablation 检验**：单独 8 检验 → **emmeans `joint_tests()` omnibus**（预算 8×N → 8）
4. **§10 偏离预案**：7 类 → **10 类**（加 replicate < planned、主分析失败 fallback、peeking 触发）
5. **§13 工程稳健性承诺（新增）**：6 条工程细节（cost-aware scheduler / cache routing / OpenTelemetry schema / 断点续跑 / Sonnet 4 thinking 审计 / gpt-4o 滚动窗口）

**主要修订（v0.3 → v0.4）**：
1. **§3.1 模型 3 → 5**：加 Claude Opus 4.7（天花板对照）+ GPT-5（OpenAI 高端）+ Qwen3-235B-Thinking（开源 reasoning 锚）；thinking 模式作为受控变量；cell 数 648 → 1080，轨迹 1944 → 3240
2. **§15 伦理与 IRB（新增）**：5 段（IRB approval statement、Compensation、Data protection、Dual Use、Disclosure）
3. **§16 PRISMA 2020 章节映射（新增）**：27 项 + CONSORT-AI 必含
4. **§17 OSF 项目结构 + COS Badges（新增）**：标准文件夹树 + Open-Ended Registration + 5 枚 Badge 申请计划
5. **§18 Internal Validity（新增）**：NeurIPS 2024+ Reproducibility Checklist 5 分项
6. **§19 Funding & Registration（新增）**：OSF DOI + GitHub URL