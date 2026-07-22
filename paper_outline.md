# Echo Chambers of One · 论文大纲（RR Stage 1）

> 目标会议（按优先级）：
> 1. **AAMAS 2027**（最匹配：AAMAS 重视 agent autonomy 与 long-horizon stability）
> 2. **CogSci 2027**（认知建模角度）
> 3. **ICLR 2027**（benchmark + 内部机制角度）
>
> RR Stage 1 投稿前需在 OSF 冻结研究方案；Stage 2 用真实数据替换 §4。

## 1. Title

> **Echo Chambers of One: A Causal Test of Interaction Deprivation on Long-Horizon State Stability in Language Agents**

## 2. Abstract（~180 词）

Stateful language agents running for thousands of steps increasingly fail at sustained, coherent behavior. We ask whether **interaction deprivation**—the absence of fresh external input, corrective feedback, or peer coordination—causally degrades capability over time, independent of context length, task length, or memory capacity. We pre-register a 7-model × 6-condition × 3-task factorial design (`n ≥ 20` trajectories per cell). The six conditions isolate four candidate mechanisms: state accumulation only, novelty without feedback, scalar feedback only, peer interaction with matched budgets, and human supervision as upper bound. Across 10000-step horizons with checkpoints at 0/100/500/1k/2k/5k/10k, we estimate a longitudinal mixed-effects model `y = β₀ + β₁·log(1+t) + β₂·C + β₃·log(1+t)·C + u_model + u_task + u_run + ε` and test whether β₃ is significantly negative for the isolated condition. We complement confirmatory tests with 8 single-factor ablation mechanisms (self-talk, episodic recall, source tagging, state reset, external anchoring, independent critics, semantic compression). **The full analysis plan, exclusion rules, fallback model strategy, and effect-size reporting are pre-specified**. Results-blind Stage 2 reporting follows.

## 3. Introduction（~700 词 / 1.5 页）

3.1 **现象**：长程 Agent 失稳——Vending-Bench meltdown loop [$TRAE_REF](https://arxiv.org/abs/2502.15840)、Project Vend identity crisis [$TRAE_REF](https://www.anthropic.com/research/project-vend-1)、LongMemEval 30% drop [$TRAE_REF](https://arxiv.org/abs/2410.10813)。
3.2 **既有解释**：任务长度、context rot、长上下文注意力衰减、记忆污染、模型坍塌。每一种都给出部分解释，但未分离"外部交互剥夺"这一独立通路。
3.3 **关键空白**：无人把"外源交互缺失"作为独立自变量、与上述机制正交地控制。
3.4 **本文工作**：把"孤独感"从一个传播比喻改写为可操作化的"外源交互剥夺"假说；首次系统地以 6 条件因式设计、7 模型、3 任务、纵向混合效应模型检验这一假说；并把 8 种工程"反孤独"机制作为机制消融。
3.5 **投稿取向**：强调"可证伪 + 因式设计 + 预注册 + 公开数据/代码"，适合 RR 流程。

## 4. Methods（~2000 词 / 4 页）

### 4.1 任务
- Vending-Bench：长程库存与价格决策。
- ALFWorld：多步具身推理。
- LongMemEval 子集：跨会话记忆。

### 4.2 模型
- llama-3.1-70b / 405b-instruct
- qwen-2.5-72b-instruct
- claude-sonnet-4
- gpt-4o
- **deepseek-v4-flash**（1M context，主力长上下文）
- **deepseek-v4-flash-thinking**（thinking 模式对照）

### 4.3 条件（6）
- 无状态控制 / 闭环隔离 / 外部新颖性 / 标量纠错 / 同伴交互 / 人类交互

### 4.4 检查点与评测电池
- 0 / 100 / 500 / 1k / 2k / 5k / 10k 步
- 评测 5 维：accuracy / planning_score / decision_score / calibration / memory_score
- 每个检查点启动"评测克隆"，结果不写回主 Agent

### 4.5 主分析
- 纵向混合效应模型（LMM）
- 随机效应：model, task, trajectory_id
- 固定效应：log_step, condition, log_step × condition
- 核心检验：β₃ 显著为负

### 4.6 多重比较
- 3 信号 × 7 模型 × 3 任务 = 63 cell
- Holm-Bonferroni 分层校正

### 4.7 样本量与功效
- 预实验 n=5/cell → 估计方差
- 正式实验 n ≥ 20/cell，必要时扩到 30

### 4.8 偏离预案（与 OSF 预注册一致）
- LMM 三级回退（LMM → GEE → OLS）
- 低功效 cell 标注
- API 失败剔除规则
- Holm 校正后全阴性的 BH-FDR 敏感性

### 4.9 机制消融（探索性）
8 种反孤独机制在 isolated 基线上的单因素消融。

## 5. Expected Results & Falsifiability（~400 词）

4 种可能结果方向，全部预先承诺报告。

## 6. Discussion Plan（结果盲写，~600 词）

6.1 现象层：状态累积 vs 上下文污染的分离
6.2 机制层：信息 vs 纠错 vs 同伴的相对贡献
6.3 工程层：哪些反孤独机制实际有效
6.4 限制：1M context 不消除 context rot；thinking 模式 ≠ 真自反思；mock/peer 模型与真人差距
6.5 伦理与双重用途：长程自治 Agent 的对齐风险

## 7. Timeline & Budget（~200 词）

- 8 月：OSF 预注册冻结
- 9 月：预实验（n=5/cell，单任务、单模型）
- 10–12 月：正式数据收集
- 1 月：分析 + Stage 2 论文撰写
- 2 月：Stage 2 投稿

**算力预算估算（DeepSeek V4 Flash 缓存命中模式）**：
- 总 token 量 ≈ 7 模型 × 6 条件 × 3 任务 × 20 轨迹 × 10000 步 × ~200 token/步 ≈ 5.04B
- 缓存命中：≈ $14
- 缓存未命中：≈ $705
- 综合估计：≈ $200–500（含 Anthropic / OpenAI 的 7 模型矩阵；按 20% 走 Anthropic、20% 走 OpenAI、60% 走 DeepSeek 估计）

## 8. Pre-registration & Open Science

- OSF 项目：https://osf.io/echo-chambers-of-one/（待创建）
- 预注册文档：见 `preregistration.md`
- 代码：GitHub `echo-chambers-of-one`（待创建）
- 数据：OSF Files / Hugging Face Datasets（脱敏后）
- 模型 API 调用记录：仅公开已脱敏 token 数与延迟；不公开 prompt 中包含 PII 的部分

## 9. Author Contributions

预注册时填入；现仅占位。

## 10. Reproducibility Checklist（NeurIPS ML Reproducibility 风格）

- [ ] 预注册
- [ ] 公开代码
- [ ] 公开数据（脱敏后）
- [ ] 固定随机种子
- [ ] 单 GPU/TPU 资源声明
- [ ] 碳足迹估算
- [ ] 模型 API 版本钉死