# 第三轮深度调研：模型选型 / 伦理 / OSF 报告规范

> 检索截止：2026-07-29
> 配套：`LITERATURE_REVIEW.md`（第一轮）、`LITERATURE_REVIEW_v2.md`（第二轮）
> 目的：在 v0.3 基础上识别**模型代际、伦理合规、报告规范**三类盲点，给出 v0.4 修订方案。

---

## A · 三份子报告核心发现

### A1 · 模型选型（5 类发现）

| 关键发现 | 依据 |
|---|---|
| **闭源 vs 开源在长程任务上差距缩小到 5–8%** | METR RE-Bench、LongBench v2、NoLiMa |
| **DeepSeek V4 Flash 已超过 Llama-3.1-70B / Qwen-2.5-72B**（长上下文检索）| NoLiMa 2025 |
| **Sonnet 4.6 / 4.7 性价比优于 Opus 4.7**（价格 1/5，性能 90%）| Claude 4.6 2026-02 评测 |
| **Vending-Bench 2 上 GPT-5.5 击败 Opus 4.7**（薄利多销策略）| Vending-Bench 2 Arena 2026 |
| **3 模型全闭源在 RR Stage 1 评审中可能被要求修改**（缺开源锚）| AAMAS / ICLR / NeurIPS 2025 评审趋势 |
| **"长程任务模型 collapse"** 真实存在：ProgramBench 上 Opus 4.7 / GPT-5.4 / Gemini 3.1 Pro 全部 0% | ProgramBench (Meta FAIR + Stanford) 2026 |
| **Agents-A1（35B MoE，Qwen 基）击败部分万亿闭源** | Shanghai AI Lab arXiv:2606.30616 |
| **DeepSeek V3.2 BrowseComp 67.6 大幅领先 GPT-5 54.9** | DeepSeek V3.2 tech report 2025-12 |
| **thinking 模式 token 代价 +200–500%**，仅推理密集型任务划算 | DeepSeek V3.2 tech report |

### A2 · 伦理 + IRB（5 类发现）

| 关键发现 | 依据 |
|---|---|
| **NeurIPS 2025 Ethics Review 强制**："research involving human participants" 需 IRB 或对等流程 | neurips.cc/public/EthicsGuidelines |
| **Stanford 强制所有非医学计算机科学研究经过 ESR + IRB 双闸** | CASBS Stanford |
| **Prolific 推荐时薪 £9.00 / $12.00/h**；长程监督类任务 $20–30/h | Prolific 官方定价 |
| **Anthropic 2025-12-18 safety report**：长对话存在 "AI 精神病" 风险，guardrails 强化 | Anthropic Claude safety report |
| **Project Vend Claudius 类对齐漂移**对长程研究有重要警示意义 | Project Vend 2025-06 |
| **GDPR Art. 89 + PIPL 第 13、27 条**：科研目的在适当保障下限制数据主体权利 | EU + 中国法规 |
| **EU AI Act（2024-1689）** Article 27：高风险 AI 需 ethics review | EUR-Lex |
| **dual use 风险**：揭示 agent 弱点可直接帮助 jailbreak；NeurIPS 要求 responsible disclosure | NeurIPS Code of Ethics |
| **Anthropic Responsible Disclosure Policy**：先私下联系 90 天后再公开 | Anthropic |
| **CRediT 14 类无"研究伦理"角色**，归入 Investigation + Writing-review | CRediT taxonomy |

### A3 · OSF + PRISMA + 报告规范（5 类发现）

| 关键发现 | 依据 |
|---|---|
| **Standard vs Open-Ended Registration 模板**：648 cell 因式 + 10 类预案推荐 **Open-Ended** | OSF Help |
| **Project vs Registration 区别**：RR Stage 1 协议应使用 Registration（自动时间戳）| OSF Help |
| **DOI 注册需 Add-on 4.0**；可单独为 Registration 申请 DOI | OSF |
| **PRISMA 2020 = 27 项 + 流程图**，对 LLM Agent 评估研究适用 | BMJ 2021 |
| **CONSORT-AI 补充 11 项 + SPIRIT-AI 补充 15 项**，对"AI 干预研究"必报 LLM version + prompt + tool schema | BMJ 2020 |
| **TRIPOD-LLM** 收录在 EQUATOR Network，对 LLM-as-judge/evaluator 必报 model ID + temperature + seed | EQUATOR |
| **NeurIPS 2024+ ML Reproducibility Checklist** 5 分项：code / model / data / environment / training-inference | paperswithcode |
| **COS Open Science Badges 4 枚**：Open Data / Open Materials / Preregistered / Registered Report | COS |
| **Stage 1 IPA 后 6–12 月内提交 Stage 2**；偏离按 COS Transparent Changes 模板逐条报告 | COS |
| **最佳 OSF 文件结构**：docs / data/raw / data/agg / code / env / wiki / registrations | OSF + paperswithcode |

---

## B · v0.3 必须修订的 4 个盲点

| # | 盲点 | 现行 v0.3 | 修订方案（v0.4） |
|---|---|---|---|
| 1 | **3 模型全闭源，缺开源锚** | "3 模型：DeepSeek V4 Flash / Claude Sonnet 4 / GPT-4o" | **扩到 5 模型**：(1) Claude Sonnet 4.6 (闭源性价比) (2) Claude Opus 4.7 (天花板对照) (3) GPT-5 (OpenAI 高端) (4) **DeepSeek V4 Flash** (1M context 开源锚) (5) **Qwen3-235B-Thinking** (开源 reasoning 锚)；thinking 模式作为受控变量 |
| 2 | **缺失 IRB 章节** | 仅有 "human condition" 与 "human_validation" 描述 | **新增 §15 伦理与 IRB**：IRB approval statement、Prolific 补偿标准、GDPR/PIPL 数据保护、Dual Use 风险评估、Responsible Disclosure 协议 |
| 3 | **缺失 PRISMA 2020 章节映射** | 无 | **新增 §16 PRISMA 2020 章节映射表**：27 项主清单 + 流程图，对应 Stage 1 vs Stage 2 |
| 4 | **缺失 OSF 项目结构规范** | 无 | **新增 §17 OSF 项目结构 + COS Badges**：标准文件夹结构、Open-Ended Registration 模板、4 枚 Open Science Badge 申请计划 |

---

## C · v0.4 修订必加细节

### C1 · 模型列表（v0.3 → v0.4）

| # | 模型 | 上下文 | 类型 | 角色 |
|---|---|---|---|---|
| 1 | Claude Sonnet 4.6 | 1M | 闭源 | 主力 baseline（性价比）|
| 2 | Claude Opus 4.7 | 1M | 闭源 | 天花板对照 |
| 3 | GPT-5 | 256K | 闭源 | OpenAI 高端（routing 模式）|
| 4 | DeepSeek V4 Flash | 1M | 开源 | 1M context 主力 + 开源锚 |
| 5 | Qwen3-235B-Thinking | 1M | 开源 | 开源 reasoning 锚 |

**新增 cell 数** = 5 模型 × 4 长度 × 6 条件 × 3 任务 × 3 seed = 1080 cell / 3240 轨迹
**预算估算**（同样按 70% DeepSeek V4 Flash 缓存命中 + 30% 闭源）：
- 总 token：3240 × 2M = 6.48B
- 总预算：$2500–$4500

**thinking 模式受控变量**：在 DeepSeek V4 Flash 与 Qwen3-235B 上分别做 on/off thinking（共 6 配置组合 × 4 长度 × 6 条件 × 3 任务 × 3 seed = 1296 cell 增量）→ 实际 cell 数为 1080 + 1296 = **2376 cell / 7128 轨迹**，预算 $5000–$9000

更保守做法：thinking 模式仅在 isolated 基线做 + 4 个长度 → 增量 6 × 4 × 1 × 3 × 3 = 216 cell → 总 cell 数 **1296 / 3888 轨迹**，预算 $3500–$5500

### C2 · 伦理章节必含字段（§15）

1. **IRB approval statement**（写明"approved / pending / exempt"）
2. **Compensation & Fair Wage**（Prolific $15/h 长程 / $18/h 标注；引用 NeurIPS 2025 fair wages）
3. **Data protection & Privacy plan**（GDPR Art. 89 + PIPL 第 27 条 + 伪匿名化 + 数据保留 ≤ 2 年）
4. **Dual Use Risk Assessment**（1 页 Methods 子节，含 3 项 mitigation + Stage 2 red-team 计划）
5. **Responsible Disclosure Protocol**（按 Anthropic 90 天私下通报）

### C3 · PRISMA 2020 章节映射（§16）

| PRISMA Item | 对应本研究章节 |
|---|---|
| 1. Title | paper_outline.md §1 |
| 2. Abstract | paper_outline.md §2 |
| 3. Rationale | paper_outline.md §3 |
| 4. Objectives/PICOS | preregistration §1-2 |
| 13. Synthesis methods | preregistration §7 |
| 22. Risk of bias | 新增 §18 Internal Validity（多 seed + bootstrap CI + judge ensemble）|
| 27. Funding + Registration | 新增 §19 Funding & Registration |

### C4 · OSF 项目结构（§17）

```
echo-chambers-of-one/
├── docs/          ← preregistration.md, paper_outline.md, RELEASES
├── data/raw/      ← trajectories (CC-BY 4.0)
├── data/agg/      ← aggregated metrics (CC0)
├── code/          ← analysis + scripts (MIT)
├── env/           ← Dockerfile + requirements.txt
├── wiki/          ← 变更日志、决策记录、可视化
└── registrations/ ← Stage 1 IPA 时间戳 + DOI
```

**OSF Badges 申请计划**：
- ✅ Preregistered（注册时申请）
- ✅ Preregistered + Analysis Plan（注册含 10 类预案时申请）
- ⏳ Open Data（Stage 2 投稿前）
- ⏳ Open Materials（Stage 2 投稿前）
- ⏳ Registered Report（AAMAS/JAAMAS 接收 Stage 1 IPA 后）

---

## D · 4 条 v0.4 修订建议（按落地成本排序）

1. **扩 3 模型到 5 模型**（成本中）：增 OpenAI GPT-5 + Claude Opus 4.7 + Qwen3-235B-Thinking；增 cell 数到 1080；预算上调到 $2500–$4500
2. **写明 §15 伦理章节**（成本低）：5 段（IRB + 补偿 + 数据保护 + Dual Use + Disclosure）；约 1 页
3. **写明 §16 PRISMA 2020 映射**（成本低）：单表 + 流程图
4. **写明 §17 OSF 项目结构**（成本低）：单段 + 文件夹树 + 4 枚 COS Badge 计划

---

## E · 引用源（按子题）

### 模型选型
1. [Anthropic Claude 4 / Mythos 5 / Fable 5 System Card (Vending-Bench 2, Toolathlon, Real-World Finance v2), 2026](https://www.anthropic.com/)
2. [ProgramBench (Meta FAIR + Stanford), https://programbench.com/static/paper.pdf, 2026](https://programbench.com/static/paper.pdf)
3. [Agents-A1 (Shanghai AI Lab, arXiv 2606.30616), 2026](https://arxiv.org/abs/2606.30616)
4. [DeepSeek V3.2 技术报告, 2025-12](https://api-docs.deepseek.com/)
5. [Claude Sonnet 4 1M context 官方公告, 2025-08](https://www.anthropic.com/)
6. [The Llama 4 Herd: Architecture, Training, Evaluation, 2026](https://arxiv.org/abs/2606.30616)
7. [Qwen3-235B-Thinking](https://qwen.readthedocs.io/)
8. [LongMemEval / LongMemEval-V2 / LoCoMo / EverMemBench, 2025-2026](https://arxiv.org/abs/2410.10813)
9. [NoLiMa arXiv 2502.05167](https://arxiv.org/abs/2502.05167)

### 伦理 + IRB
10. [NeurIPS 2025 Code of Ethics](https://neurips.cc/public/EthicsGuidelines)
11. [NeurIPS 2025 Call for Papers](https://neurips.cc/Conferences/2025/CallForPapers)
12. [ICLR 2025 Call for Papers](https://iclr.cc/Conferences/2025/CallForPapers)
13. [Stanford ESR](https://casbs.stanford.edu/our-work/ethics-and-society-review)
14. [EU AI Act Article 27](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
15. [PIPL](http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_311102.html)
16. [Prolific Pricing](https://www.prolific.com/pricing)
17. [Anthropic Claude Safety Report 2025-12-18](https://www.anthropic.com/)
18. [Project Vend / Claudius, 2025-06](https://www.anthropic.com/research/project-vend-1)
19. [Anthropic Agentic Misalignment, 2025-06-20](https://www.anthropic.com/research/agentic-misalignment)
20. [UK ICO Guidance on AI and Data Protection](https://ico.org.uk/for-organisations/guide-to-data-protection/key-dp-themes/guidance-on-ai-and-data-protection/)
21. [Anthropic Responsible Disclosure Policy](https://www.anthropic.com/responsible-disclosure-policy)
22. [CRediT taxonomy (NISO Z39.104-2022)](https://credit.niso.org/)

### OSF + PRISMA
23. [OSF Help – Create a Preregistration](https://help.osf.io/article/357-create-a-preregistration)
24. [OSF Help – Preregistration Templates](https://help.osf.io/article/1454-preregistration-templates)
25. [COS Registered Reports](https://www.cos.io/initiatives/registered-reports)
26. [PRISMA 2020 (Page et al. BMJ 2021)](https://doi.org/10.1136/bmj.n71)
27. [CONSORT-AI / SPIRIT-AI (Cruz Rivera et al. BMJ 2020)](https://doi.org/10.1136/bmj.m3210)
28. [EQUATOR Network](https://www.equator-network.org/)
29. [paperswithcode – Tips for Releasing Research Code](https://github.com/paperswithcode/releasing-research-code)
30. [COS Open Science Badges](https://www.cos.io/our-services/badges)
31. [Zenodo](https://zenodo.org/)
32. [AAMAS 2026 时间地点 (Paphos, Cyprus)](https://blog.csdn.net/iaast/article/details/150557889)

---

**核心结论**：第三轮调研发现 v0.3 仍存在 **4 类盲点**（模型代际滞后、缺伦理章节、缺 PRISMA 映射、缺 OSF 结构规范）。v0.4 修订集中在：
- §3.1 模型扩到 5 个（含开源锚 + 天花板对照 + thinking 受控变量）
- 新增 §15 伦理与 IRB（含 5 段必含字段）
- 新增 §16 PRISMA 2020 章节映射表
- 新增 §17 OSF 项目结构 + 4 枚 COS Badge 申请计划

预计 cell 数从 648 升到 1080–2376（取决于 thinking 受控变量如何实施），预算从 $1500–$2500 升到 $2500–$5500。