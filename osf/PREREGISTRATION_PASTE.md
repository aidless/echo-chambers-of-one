# OSF 预登记粘贴内容

> 把下面的内容完整复制到 OSF 项目 Registrations → New Registration → Standard Pre-Data Collection Registration 的 Rich Text / Markdown 编辑器。

---

# Echo Chambers of One — Pre-registration

**Project:** Echo Chambers of One
**OSF Project ID:** (填写项目 ID)
**Registration date:** 2026-07-22
**Status:** Pre-Data Collection Registration

---

## 1. Research Question

Do stateful language agents exhibit measurable capability degradation when run for thousands of steps in the absence of fresh external input, corrective feedback, or peer coordination, independent of task length, context length, and memory capacity?

## 2. Hypotheses

### Confirmatory
- **H1:** The isolated condition will show significantly lower composite capability at checkpoints than any condition with external signals.
- **H2:** Adding information, feedback, or peer interaction will each yield a positive slope term in the longitudinal mixed-effects model.
- **H3:** There will be a significant time × condition interaction, with negative slope for the isolated condition greater in magnitude than for feedback-containing conditions.

### Exploratory
- **H4:** Internal self-talk may improve short-term performance but amplify errors in the absence of reliable feedback.
- **H5:** Linguistic "loneliness" markers may precede capability decline, with only weak correlation.

## 3. Design

- **Type:** 7 (model) × 6 (condition) × 3 (task) mixed longitudinal.
- **Trajectories:** ≥ 20 per cell.
- **Step horizon:** 10,000 with checkpoints at 0 / 100 / 500 / 1k / 2k / 5k / 10k.

## 4. Models

llama-3.1-70b-instruct, llama-3.1-405b-instruct, qwen-2.5-72b-instruct, claude-sonnet-4, gpt-4o, deepseek-v4-flash (1M context), deepseek-v4-flash-thinking.

## 5. Tasks

Vending-Bench (long-horizon inventory/pricing), ALFWorld (multi-step embodied reasoning), LongMemEval subset (cross-session memory).

## 6. Conditions

1. `control_stateless` — baseline; no per-step state persistence.
2. `isolated` — only task + self-generated memory.
3. `novelty` — receives task-irrelevant external documents.
4. `feedback` — receives scalar correctness signals only.
5. `peer` — interacts with an independently-seeded peer agent.
6. `human` — supervised by a human (Prolific, n = 20).

## 7. Outcomes

Primary: accuracy, planning_score, decision_score, calibration (1 − ECE), memory_score (1 − contradiction rate).
Secondary: survival time to first unrecoverable deviation.

## 8. Analysis

Linear mixed-effects model:
```
y_{i,t} = β0 + β1·log(1 + t) + β2·C_c + β3·log(1 + t) × C_c
         + u_model + u_task + u_run + ε_{i,t}
```
- Fixed effects: log(1+t), condition, log(1+t) × condition.
- Random effects: model, task, trajectory_id.
- Core test: β3 significantly negative for the isolated condition.
- Multiple comparison correction: Holm-Bonferroni stratified by model and task.

## 9. Exclusion rules (pre-registered)

- Trajectories with API failure rate > 20% are removed and replaced.
- Trajectories with > 50% missing tool returns are removed and replaced.
- Trajectories ending in environment crashes are removed and replaced.
- **No** exclusion based on agent performance.

## 10. Deviation contingencies

| Situation | Action |
|---|---|
| LMM random-effect covariance singular | Three-level fallback: LMM → GEE (independence) → pooled OLS; method and reason recorded |
| `n_groups < 5` per cell | Skip LMM/GEE; go directly to pooled OLS; cell flagged as low-power |
| API failure rate > 20% | Cell excluded; report failure rate |
| All Holm-corrected p > 0.05 | Report null; provide Benjamini-Hochberg FDR as sensitivity |
| Sample size exceeds budget | Focus on 2 representative models + 2 tasks; expand to n = 50 per cell |

## 11. Open science

- Public code (MIT) and public de-identified data (CC-BY-4.0) on completion.
- Pre-registration publicly accessible.
- Analysis scripts reproducible from raw trajectories.

## 12. Timeline

- 2026-07-22: Pre-registration frozen (this document).
- 2026-09: Stage 1 submission to AAMAS RR.
- 2026-10–12: Data collection.
- 2027-02: Stage 2 submission.

---

**End of pre-registration. Frozen 2026-07-22.**