# 深度调研：长程语言智能体稳定性（2025–2026）

> 检索截止：2026-07-23
> 目的：为 "Echo Chambers of One" 预注册注入最新文献支撑，并指出 5 个必须修订的预注册盲点。
> 方法：3 个 Explore agent 并行检索 3 个独立子题。证据等级 P0=同行评审/机构权威；P1=arXiv 已引用；P2=初稿/技术报告。

---

## 一、3 个子题的核心发现

### 子题 1：长程能力下降现象与"因式设计"空白

**核心判断**：5 个 P0 工作（Vending-Bench、Project Vend、LongMemEval、METR RE-Bench、HORIZON）全部测**单智能体在长任务中的能力**，但**没有任何一项做过"交互剥夺 vs 新颖性 vs 纠错 vs 同伴 vs 人类"的因式设计**。我们的 6 条件 × 3 任务正填补这块空白。

**最强支持 H1 的工作**：

| 工作 | arXiv | 关键发现 | 与本研究关系 |
|---|---|---|---|
| Vending-Bench | [arXiv:2502.15840](https://arxiv.org/abs/2502.15840) | 失败与上下文窗口满溢**无显著相关**——衰退非因记忆容量，而因决策一致性崩溃 | 强支持 H1；提供 baseline 任务 1 |
| Project Vend | [anthropic.com](https://www.anthropic.com/research/project-vend-1) | Claude 不会从错误中持续学习；身份幻觉；低于成本卖货 | 支持 H1+H3；提供真实世界类比 |
| LongMemEval | [arXiv:2410.10813](https://arxiv.org/abs/2410.10813) | 跨持续会话准确率下降 30% | 支持 H1；提供 baseline 任务 3 |
| METR RE-Bench | [arXiv:2503.14499](https://arxiv.org/abs/2503.14499) | 50% 任务完成时长：Claude 3.7 Sonnet ≈ 50 分钟 | 支持 H3（纠错关键） |
| HORIZON | [arXiv:2604.11978](https://arxiv.org/abs/2604.11978) | 失败归因三类：规划 / 记忆 / 错误累积 | **借鉴 LLM-as-Judge 归因 schema** |

### 子题 2：Context Rot / 长上下文衰减

**核心判断**：Context rot **真实存在**，**1M context 解决的是可输入长度，不是有效可用长度**。但截至 2026-07-23，**未检索到 DeepSeek V4 Flash 官方模型卡或可复现实验**，本预注册对 V4 Flash 的 1M context 假设应加更严格对照。

**P0 工作**：

| 工作 | 链接 | 关键发现 |
|---|---|---|
| Chroma Context Rot | [research.trychroma.com](https://research.trychroma.com/context-rot) | 18 模型仍随长度退化；低语义匹配、相似干扰项会改变衰减率 |
| NoLiMa | [arXiv:2502.05167](https://arxiv.org/abs/2502.05167) | 32K 时 11/13 模型跌到 50% 基线；GPT-4o 99.3%→69.7% |
| HELMET | [arXiv:2410.02694](https://arxiv.org/abs/2410.02694) | NIAH 与下游任务相关性低；推理能力差距随长度扩大 |
| LongBench v2 | [arXiv:2412.15204](https://arxiv.org/abs/2412.15204) | 最佳模型仅 50.1%，o1-preview 推理后 57.7% |
| SLIM | [arXiv:2510.18939](https://samaya.ai/blog/lost-in-the-maze-overcoming-context-limitations-in-long-horizon-agentic-search) | 50%+ 失败与上下文管理有关 |

### 子题 3：8 种反退化机制

**核心判断**：当前最可靠的结论是**将历史结构化 + 选择性检索 + 外部可验证状态校正**。Self-talk 在强模型无 oracle 反馈时**可能反向**。Periodic reset 与 source tagging 的独立因果证据**最弱**。

**3 个最可能显效**：External grounding > Episodic recall > Independent critic（仅当真正独立时）
**2 个最被高估**：Self-talk（NoLiMa 显示 CoT 救不了长上下文）；Periodic reset（无强独立证据）

---

## 二、当前预注册的 5 个必须修订的盲点

| # | 盲点 | 现行预注册 | 修订方案 |
|---|---|---|---|
| 1 | **Context rot 与 isolation 效应不可识别** | 6 条件只操纵"外部信号类型"，没控制 token 长度 | 加入"长度操纵"作为正交维度：4K / 32K / 128K / 模型上限；强制 6 条件在所有 cell 内 token 总数等价 |
| 2 | **DeepSeek V4 Flash 1M context 假设无独立验证** | 直接写"1M context 让 context rot 不构成瓶颈" | 6 条件外加"V4 Flash 模型特异长度-表现曲线"测；主效应模型中加 `condition × log(tokens) × model` 交互 |
| 3 | **Self-talk 条件可能产生假阴性** | 列为 8 种反孤独机制之一 | 加 2 个"对抗"控制：oracle 反馈 / 错误反馈；保证 self-talk 不是"反思"独苗 |
| 4 | **失败归因 schema 缺失** | 只测 5 个聚合指标 | 借鉴 HORIZON，引入 LLM-as-a-Judge 三类归因：规划失误 / 记忆丢失 / 历史错误累积；作为次要 outcome |
| 5 | **缺少 state replay 反事实** | 只有"原始轨迹" | 在每 100 步给 Agent 提供 4 种状态视图：(a) 完整原始；(b) 无损结构化；(c) 等长但含错误记忆；(d) 等长无关填充；只在 (a)(b) 下 isolation 效应仍存，才排除 context rot |

---

## 三、应吸收到预注册的 5 条新设计要点

1. **3 任务正交覆盖三种假设机制**：
   - Vending-Bench（长程经济决策）
   - LongMemEval（跨会话记忆）
   - HELMET 风格长上下文推理（context rot 隔离）
2. **失败归因 schema**（来自 HORIZON）作为次要 outcome
3. **纠错条件必须来自外部且独立于 agent 自身日志**（否则就是 self-talk 变体）
4. **每 cell 至少 5 次重复 seed** 并报告 IQR/方差（Vending-Bench 已证 run-to-run 方差极大）
5. **主分析模型加入**：`condition × log(step) × model` 三维交互，不仅 model 作固定效应

## 四、应避免的 2 条已知陷阱

1. **不要把 self-talk/CoT 当万能反退化**——NoLiMa 明确 CoT 不能恢复长上下文性能
2. **不要把 outcome 包含"语气/价值取向"维度**——Project Vend 的"身份幻觉/讨好员工"是**对齐漂移**而非能力衰减，否则 6 条件间会被对齐混淆

---

## 五、预注册主网格修订（草案）

| 任务 | 3 任务保持 | 加入"长度操纵"正交维度：4 长度 × 6 条件 × 3 任务 × 5 seed × 7 模型 = 7560 cell |

每 cell n=5 重复 seed（不是 n=20）。V4 Flash 4K / 32K / 128K / 1M 共 4 长度；其他模型用 4K / 32K / 128K（这些模型上限是 128K，1M 长度被 V4 Flash 独占）。

**正式实验 cell 数** = 4 长度 × 6 条件 × 3 任务 × 5 种子 × 7 模型 = 2520 cell，5 重复总计 12600 轨迹。

**预算估算**（按 V4 Flash 缓存命中 $0.0028/1M token，未命中 $0.14/1M）：
- 10000 步 × 200 token/步 = 2M token/轨迹
- 12600 轨迹 × 2M = 25.2B token
- 缓存命中：$70；未命中：$3528
- 综合预算：$2000–$4000（按 70% DeepSeek V4 Flash + 30% 闭源供应商）

这超出之前估算 10 倍——需要 ① 减模型数到 3 模型（DeepSeek V4 Flash / Claude Sonnet 4 / GPT-4o）；② 减轨迹数到 3 重复 → 实际 4 长度 × 6 条件 × 3 任务 × 3 重复 × 3 模型 = 1944 cell，预算回到 $300–$600。

---

## 六、引用源（按出现顺序）

1. [Vending-Bench — arXiv:2502.15840](https://arxiv.org/abs/2502.15840)
2. [Project Vend](https://www.anthropic.com/research/project-vend-1)
3. [LongMemEval — arXiv:2410.10813](https://arxiv.org/abs/2410.10813)
4. [METR RE-Bench — arXiv:2503.14499](https://arxiv.org/abs/2503.14499)
5. [HORIZON — arXiv:2604.11978](https://arxiv.org/abs/2604.11978)
6. [Chroma Context Rot](https://research.trychroma.com/context-rot)
7. [NoLiMa — arXiv:2502.05167](https://arxiv.org/abs/2502.05167)
8. [HELMET — arXiv:2410.02694](https://arxiv.org/abs/2410.02694)
9. [LongBench v2 — arXiv:2412.15204](https://arxiv.org/abs/2412.15204)
10. [Lost in the Middle — arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
11. [Reflexion — arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
12. [LATS — arXiv:2310.04406](https://arxiv.org/abs/2310.04406)
13. [Self-RAG — arXiv:2310.11511](https://arxiv.org/abs/2310.11511)
14. [A-MEM — arXiv:2502.12110](https://arxiv.org/abs/2502.12110)
15. [Mem0 — arXiv:2504.19413](https://arxiv.org/abs/2504.19413)
16. [Zep/Graphiti — arXiv:2501.13956](https://arxiv.org/abs/2501.13956)
17. [HippoRAG 2 — arXiv:2502.14802](https://arxiv.org/abs/2502.14802)
18. [CRAG — arXiv:2401.15884](https://arxiv.org/abs/2401.15884)
19. [Rethinking Memory in LLM Agents — arXiv:2505.00675](https://arxiv.org/abs/2505.00675)
20. [Survey on LLM Agent Evaluation — arXiv:2503.16416](https://arxiv.org/abs/2503.16416)

---

**核心结论**：我们的 novelty（6 条件因式设计 + state × length 正交分离 + 8 种反孤独机制）目前**没有任何现有工作覆盖**。文献层面 5 个关键盲点已识别，**必须修订预注册**才能保证 Stage 1 投稿不被审稿人一句"没控制 context rot"打回。