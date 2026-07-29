# 第二轮深度调研：方法论、工程、Judge 设计

> 检索截止：2026-07-29
> 配套：`LITERATURE_REVIEW.md`（第一轮，2026-07-23）
> 目的：在 v0.2 基础上进一步识别统计学 / 工程 / judge 设计层面的盲点，给出 v0.3 修订方案。

---

## A · 三份子报告核心发现

### A1 · 大规模 RR + 多重比较（方法论）

| 关键发现 | 依据 |
|---|---|
| **Holm-Bonferroni 不是最优**：25 假设下独立时损失 ≈ 25% 功效；强相关时损失可达 20–25% | Bretz et al. 2010 *Multiple Comparisons Using R* (CRC) + CRAN multcomp v1.4-31 |
| **Westfall-Young step-down minP permutation** 在相关结构下功效提升 20–30%，且不需独立性假设 | Romano & Wolf 2005 (JASA) + multcomp `adjusted("Westfall")` |
| **3 seed 对 d ≤ 0.5 效应 power 仅 ≈ 40%**；建议 ≥ 5 seed | Beam, Benjamin & Berger 2023 (Annu Rev Stat) + OATML Benchmark |
| **emmeans `joint_tests()` 合并 8 ablation**：多重比较预算 8×N → 8 | emmeans vignette + Bretz 2010 Ch.4 hierarchical testing |
| **brms 半 Cauchy(0,1) 先验自然处理 singular fit** | Bürkner 2017+ (JSS) + v2.21 |
| **simr 仿真 power** 是 mixed model 标配（nsim ≥ 1000） | Green & MacLeod 2016 (MEE) + CRAN simr 1.0.7 |
| **3 seed 不足的折中做法**：主分析 3 seed + supplementary power 报告 5/10 seed | Lakens 2022 + Beam 2023 |
| **偏离预案应从 7 类扩到 10 类**：加 replicate < planned、主分析失败 fallback、peeking 触发 | Lakens 2024 NHB + COS 模板 |

### A2 · 数据收集工程

| 关键发现 | 依据 |
|---|---|
| **DeepSeek V4-Flash 并发 2500** vs Claude Sonnet 4 约 50（Tier 1）| DeepSeek API Docs + Anthropic Docs |
| **Prompt cache 50× 价差**：DeepSeek V4-Flash hit $0.0028 / miss $0.14 | DeepSeek API Docs |
| **Anthropic 最小可缓存 1024 tokens**（Sonnet 4），低于这个长度 cache 不生效 | Anthropic Prompt caching docs |
| **OpenAI cache 在 15 rpm 同前缀即可能溢出**到其他机器 | OpenAI prompt caching docs |
| **OpenAI `api_request_parallel_processor.py` 提供标准范式**：token-throttling + retry queue + 增量 jsonl 写 | OpenAI Cookbook (510 lines) |
| **静态前缀放前、动态前缀放后**是缓存命中关键 | Anthropic Cookbook (Pride & Prejudice 实验) |
| **推荐三层 schema**：内层 raw provider 数据 + 外层 OpenTelemetry GenAI semconv | OpenTelemetry GenAI semconv 2025 GA |
| **OpenLLMetry + DVC/MLflow** 是最现实的开源 trace stack | Traceloop OpenLLMetry |
| **LongMemEval 显示 gpt-4o 10000 步必须有滚动窗口压缩**否则 200K 后 truncate | Wu et al. 2025 (ICLR) |
| **Sonnet 4 thinking 模式 token 不可预测**，预算假设需 1.5× buffer | Anthropic extended thinking docs |

### A3 · LLM-as-Judge 偏差校准

| 关键发现 | 依据 |
|---|---|
| **Judge 必须与 Agent 不同供应商**（同供应商自偏好放大）| Zheng et al. 2023 (NeurIPS MT-Bench) + Survey Gu 2024 |
| **4 个 7B 模型 PoLL 比单 GPT-4 便宜 7× 且更准** | Verga et al. 2024 (PoLL) |
| **Prometheus 2 / Eurus 在 4 个直接 + 4 个 pairwise 基准上接近 GPT-4** | Kim et al. 2024 (EMNLP) |
| **Position-swap 协议**：每条扫 2 次随机化顺序，一致才采纳 | Zheng et al. 2023 |
| **Krippendorff's α ≥ 0.667** 是 judge ensemble 公认阈值 | Krippendorff 2011 |
| **Self-consistency K=5 主类一致率 ≥ 0.80** 应该是 baseline | Survey 2024 |
| **Bradley-Terry / Plackett-Luce** 比直接 softmax 更稳健 | Bradley & Terry 1952 (经典) |
| **Anchor reference calibration** 在分类任务上可移植 | Anthropic evaluation guidance |
| **CoT 解释 + 反向 prompt** 缓解 anchoring bias | Survey 2024 |
| **禁止 Judge 与 Agent 同模型 + 同供应商 + 共享 prompt > 30%** | COS / OpenAI / Anthropic 一致建议 |

---

## B · v0.2 必须修订的 5 个盲点

| # | 盲点 | 现行 v0.2 | 修订方案（v0.3） |
|---|---|---|---|
| 1 | **Holm-Bonferroni 在 25 强相关假设下功效损失 20–25%** | "Holm-Bonferroni 分层校正" | **主分析 = Westfall-Young step-down minP permutation**（multcomp `adjusted("Westfall")`），Holm 仅作 sensitivity |
| 2 | **3 seed 对 d ≤ 0.5 效应 power < 40%** | "3 seeds" | **主分析 3 seed + supplementary：5 / 10 seed 抽 30% cell 做 post-hoc power**。Stage 2 必须报告 power 曲线 |
| 3 | **8 ablation 单独检验无功效**（8 × Holm 在 d < 0.8 时几乎全 negative）| "8 反退化机制消融" | **改 omnibus joint test**（emmeans `joint_tests()`）→ 8 个 planned contrast 合并 1 个 χ²/F 检验 → 预算 8 而非 8N |
| 4 | **3 类失败归因 Judge 协议未预先承诺** | "独立 LLM-as-a-Judge" | **预先承诺** judge 模型（Claude Sonnet 4 + DeepSeek-V3 + Prometheus-2 7B 三源 ensemble）、position-swap 协议、Krippendorff's α ≥ 0.667 + self-consistency ≥ 0.80 双阈值、Bradley-Terry 聚合、anchor reference 注入 |
| 5 | **数据收集工程稳健性 Stage 1 评审高危** | 无 | **预先承诺**：cost-aware scheduler（cell-level `max_dollars_per_cell`）、统一 hash manifest + 增量 jsonl 写、cache routing by `(condition_id, model_id)` 不绑 seed_id、OpenTelemetry GenAI 双层 schema（raw + normalized） |

---

## C · 工程细节必做清单（v0.3 必加）

1. **Cost-aware scheduler**：`CellSpec` 注入 `max_dollars_per_cell`；累计 `usage.*.billed_cost` 实时计费；超限立即停跑。
2. **统一 trace schema**：内层保留 `usage.prompt_tokens_details.cached_tokens` / `usage.cache_read_input_tokens`；外层用 `gen_ai.usage.cache_read.input_tokens` 做 vendor-neutral 投影。
3. **Cache routing**：`prompt_cache_key` 绑定 `condition_id + model_id`（如 `ec_001_iso_ds4f`），**不**绑 `seed_id` → 同 cell 3 共享前缀 → 命中率 ≥ 80%。
4. **断点续跑**：每个 checkpoint 0/100/500/.../10000 后立即刷盘 + 写 sha256 sidecar。
5. **Sonnet 4 thinking 预算审计**：用 `usage.output_tokens` 单独统计；超 1.5× buffer 标 `degraded_budget`。
6. **gpt-4o 滚动窗口压缩**：每 1000 步抽取 summary，避免 200K 后 truncate。

---

## D · Judge 协议（v0.3 §7 必须新增）

### D1 · Stage 1 预承诺清单

| 元数据 | 预承诺值 |
|---|---|
| Judge 主模型 | Claude Sonnet 4（与 agent 异源）|
| Judge 二号 | DeepSeek-V3 Flash（价格敏感）|
| Judge 三号 | Prometheus-2-7B（专用 judge）|
| 聚合方式 | weighted majority + Bradley-Terry 后处理 |
| Position 协议 | swap-and-average，每条 2 次随机化顺序 |
| Self-consistency | K=5 重复，主类一致率 ≥ 0.80 |
| Ensemble 一致性 | Krippendorff's α ≥ 0.667 |
| Few-shot 数量 | 8（来自人工 gold 集，**非**自 H5 待标注集）|
| Gold 集规模 | ≥ 50 人工双盲标注 |
| 禁止配置 | 同模型 + 同供应商；prompt 共享 > 30%；agent 自评做 gold |

### D2 · Stage 2 必报告

- per-class precision/recall/F1
- inter-judge agreement（Cohen's κ + Krippendorff's α + self-consistency rate）
- position-swap disagreement rate
- confusion matrix（planning ↔ memory 撞标签率）
- per-1k-trajectory judge cost

---

## E · 5 条 v0.3 修订建议（按落地成本排序）

1. **替换 Holm 为 Westfall-Young**（成本中）：改 main + sensitivity 设计，跑通 multcomp `adjusted("Westfall")` + `adjusted("Holm")` 双分析
2. **加 seed 3 → 5 主分析 + power 报告**（成本高）：648 cell × 5 seed = 1080 cell；预算上调到 $2000–$3500
3. **改 ablation 为 joint test**（成本低）：emmeans `joint_tests()` 一行代码
4. **写明 Judge 协议**（成本低）：直接把 D1 表写进 prereg §7
5. **偏离预案 7 → 10 类**（成本低）：补 "replicate < planned"、"主分析失败 fallback"、"peeking 触发" 三类

---

## F · 引用源（按子题）

### 方法论
1. [multcomp 1.4-31 CRAN PDF](https://cran.r-project.org/web/packages/multcomp/multcomp.pdf)
2. [Green & MacLeod 2016 *simr* (MEE)](https://cran.r-project.org/web/packages/simr/simr.pdf)
3. [Barr et al. 2013 (JML) + Matuschek 2017 (JML)](https://doi.org/10.1016/j.jml.2012.11.001)
4. [Lakens 2022 *Improving Your Statistical Inferences*](https://lakens.github.io/statistical_inferences/)
5. [Lakens 2024 NHB *Deviations from the registered analysis plan*](https://doi.org/10.1038/s41562-024-01909-1)
6. [COS Registered Reports initiative](https://www.cos.io/our-services/registered-reports)
7. [brms CRAN](https://cran.r-project.org/web/packages/brms/)
8. [emmeans vignette](https://cran.r-project.org/web/packages/emmeans/vignettes/confidence-intervals.html)

### 工程
9. [DeepSeek API Docs – Pricing](https://api-docs.deepseek.com/quick_start/pricing)
10. [DeepSeek API Docs – Rate Limit & Isolation](https://api-docs.deepseek.com/quick_start/rate_limit)
11. [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
12. [OpenAI Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching)
13. [OpenAI Cookbook – api_request_parallel_processor.py](https://github.com/openai/openai-cookbook/blob/main/examples/api_request_parallel_processor.py)
14. [Anthropic Cookbook – Prompt caching notebook](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/prompt_caching.ipynb)
15. [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
16. [OpenLLMetry](https://github.com/traceloop/openllmetry)

### Judge
17. [Zheng et al. 2023 MT-Bench (NeurIPS) arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
18. [Gu et al. 2024 Survey on LLM-as-a-Judge arXiv:2411.15594](https://arxiv.org/abs/2411.15594)
19. [Li et al. 2024 LLMs-as-Judges Survey arXiv:2412.05579](https://arxiv.org/abs/2412.05579)
20. [Verga et al. 2024 PoLL arXiv:2404.18796](https://arxiv.org/abs/2404.18796)
21. [Kim et al. 2024 Prometheus 2 (EMNLP) arXiv:2405.01535](https://arxiv.org/abs/2405.01535)
22. [Yuan et al. 2024 Self-Rewarding (ICML) arXiv:2401.10020](https://arxiv.org/abs/2401.10020)
23. [OpenAI Cookbook – Using LLM-as-a-Judge](https://cookbook.openai.com/examples/llm-as-a-judge)
24. [Anthropic Claude Docs – Test & evaluate](https://docs.anthropic.com/en/docs/build-with-claude/test-and-evaluate)

---

**核心结论**：第二轮调研发现 v0.2 仍存在 **5 个统计 + 工程 + Judge 协议盲点**。其中：
- **统计**：Holm-Bonferroni 功效损失 20–25% / 3 seed power < 40% / 8 ablation 无功效
- **工程**：缺 cost-aware scheduler / cache routing 协议 / OpenTelemetry schema
- **Judge**：缺 Stage 1 必承诺的协议（模型、swap、ensemble 阈值）

v0.3 修订成本集中在 §7（Judge 协议，新写 1 节）与 §11（统计方法替换为主次双分析），均不需改 cell 数。