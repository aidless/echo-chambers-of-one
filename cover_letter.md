# Cover Letter 模板（AAMAS 2027 优先）

> 提交：Registered Report Stage 1
> 目标：AAMAS 2027（截稿约 2026-09；具体日期以官网为准）

---

Dear Area Chair / Senior Program Committee,

We are pleased to submit our Registered Report Stage 1 proposal:

**Echo Chambers of One: A Causal Test of Interaction Deprivation on Long-Horizon State Stability in Language Agents**

Recent evidence (Vending-Bench, Project Vend, LongMemEval) shows that stateful language agents running for thousands of steps frequently exhibit **meltdown loops, identity drift, and 30%+ accuracy drops across sustained interactions**. However, the existing literature has not isolated *which* mechanism drives these failures: task length, context contamination, parameter memory, or the absence of external grounding.

We propose a pre-registered 7-model × 6-condition × 3-task factorial design that **teases apart four candidate mechanisms** by independently varying (i) external information access, (ii) corrective feedback, (iii) peer interaction, and (iv) human supervision. The six conditions match token budgets and tool access across cells, isolating "interaction deprivation" as a single explanatory variable. We estimate a longitudinal mixed-effects model `y = β₀ + β₁·log(1+t) + β₂·C + β₃·log(1+t)·C + u_model + u_task + u_run + ε` and test whether β₃ is significantly negative for the isolated condition.

The pre-registered design has three properties we believe are valuable to the AAMAS community:

1. **Direct causal identification.** Prior work has reported degradation phenomena but never with a factor design that orthogonalizes interaction type. Our 6-condition factorial is the cleanest causal test we know of.
2. **Practical scaffolding for deployed agents.** Beyond confirmatory tests, we evaluate 8 single-factor "anti-isolation" mechanisms (self-talk, episodic recall, source tagging, periodic reset, external anchoring, independent critic, semantic compression) — each is a deployable engineering intervention, and the comparison is, to our knowledge, novel.
3. **Open science & reproducibility.** Full pre-registration, public code, public de-identified data, fixed seeds, and detailed budget. We commit to results-blind Stage 2 reporting regardless of direction or significance.

We note that the Registered Report format is well-suited to this work because (a) the design is intricate and benefit from peer review before data collection; (b) some negative results (e.g., "interaction deprivation has no independent effect once context length is controlled") are themselves important findings that may be hard to publish through conventional channels; and (c) we want to make the analysis plan public before observing outcomes.

We thank the area chair and reviewers for their consideration. We will respond promptly to any clarification requests.

Sincerely,
[Author Names]

---

# 评审常见质疑与预设响应

## Q1: "为什么是 6 条件，而不是 2 条件（隔离 vs 非隔离）？"

预设回答：单次"隔离 vs 非隔离"对比无法区分**信息、纠错、同伴、人类**四类机制的独立贡献——它们可能全部帮助，也可能只是某一类在起作用。我们把四类机制拆开，让任一类失效都能定位到具体维度。这是回答"哪种信号最关键"这一下游工程问题的必要精度。

## Q2: "如何排除 context rot、任务长度、参数记忆？"

预设回答：(1) **1M context 模型（deepseek-v4-flash）** 作为主力，让 context rot 在大多数 cell 内不构成瓶颈；(2) 所有条件共享相同的 token 预算、记忆容量、工具权限与任务序列，差异只在外部信号类型；(3) 失败模式聚类与变点检测（PELT）作为机制诊断；(4) 无状态控制组分离评测与时间漂移。

## Q3: "为什么用 deepseek-v4-flash 而不是 GPT-4？"

预设回答：DeepSeek V4 Flash 1M context 与 $0.0028/1M cache-hit 价格让 7 × 6 × 3 × 20 网格预算可行；GPT-4o 与 Claude Sonnet 4 同时纳入作为闭源对照。DeepSeek 的 thinking / 非 thinking 模式独立成两个 cell，让"是否启用 chain-of-thought"成为额外控制变量。

## Q4: "这是不是又一份 benchmark 论文？"

预设回答：本文不只报告 benchmark 数字——核心贡献是**因果识别**与**机制消融**。我们把已知的 Vending-Bench / LongMemEval 当作 baseline 任务而非新 benchmark；主论文贡献在"如何用因式设计把现象拆到机制层"。

## Q5: "self-talk / 记忆压缩这些机制单独存在大量文献，为什么还能贡献？"

预设回答：现有文献都是孤立研究或单模型验证。**在 7 模型 × 6 条件同一框架下做对照**才是新贡献；尤其是把它们放在"是否真能对抗交互剥夺"这一具体假说下检验——而不是泛泛的"反思有没有用"。

## Q6: "peer 模型如果与主 Agent 同源，错误会相关"

预设回答：这是评审常提到的混淆。我们在 manifest 中显式声明 peer 用**独立种子轨迹**而非同源回复；并把"独立批评者"作为单独消融机制验证误差相关性是否是关键混淆。

## Q7: "LMM 经常不收敛，你们怎么应对？"

预设回答：脚本内建三级回退（LMM → GEE → pooled OLS），所有回退都在 `lmm_results.json` 显式标注 `method` 与 `fallback_reason`；低功效 cell（`n_groups < 5`）直接走 OLS。我们承诺报告所有执行过的检验，不选择性报告。

## Q8: "为什么不直接做超大规模跑 10000 步？"

预设回答：预实验先做 200 步 + n=5/cell 估计方差，再用 Monte Carlo 模拟决定正式重复数。盲目跑 10000 步是浪费算力——METR 已经显示 frontier 模型 50% horizon 仅约 50 分钟（Kwa et al. 2025），盲目长跑很可能得不到有效信号。

## Q9: "CHI / CogSci / ICLR 都合适，为什么先投 AAMAS？"

预设回答：AAMAS 优先匹配本文的**主体贡献**：agent autonomy、long-horizon stability、multi-agent 交互结构。CogSci 偏认知建模，ICLR 偏 benchmark + 机制；CHI 偏人类监督者实验。**我们准备三份投稿材料，主论文投 AAMAS，副论文分别投 CogSci / CHI**。

## Q10: "怎么保证审稿人不会说'这只是工程问题'？"

预设回答：(1) 6 条件因式设计本身是科学方法，不只是工程；(2) "agent 在缺乏外源交互时是否稳定"是 agent autonomy 的核心科学问题，与 AAMAS 主旨契合；(3) 主论文强调**因果识别**与**可证伪性**，副论文（CogSci）才深入谈工程机制。