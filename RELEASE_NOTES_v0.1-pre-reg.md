# Echo Chambers of One · v0.1-pre-reg

> Historical note for the git tag `v0.1-pre-reg` only. That tag is not an OSF registration. No DOI was issued. The cover letter mentioned below was not sent. The current protocol draft is v0.4 in `preregistration.md`, and the OSF project is still not created.

**Release date of the tag:** 2026-07-22
**Status:** old snapshot. Not frozen on OSF. Not the current protocol.
**DOI:** none.

## What's in this release

This is the **frozen pre-registration snapshot** of the Echo Chambers of One study. No real experimental data has been collected yet — only synthetic smoke-test trajectories used to validate the statistical pipeline.

### Highlights

- **Research question:** Does interaction deprivation (absence of fresh external input, corrective feedback, or peer coordination) causally degrade stateful language agents running for thousands of steps, independent of context length, task length, or memory capacity?
- **Design:** 7 models × 6 conditions × 3 tasks × ≥20 trajectories per cell
- **Models:** llama-3.1-70b / 405b, qwen-2.5-72b, claude-sonnet-4, gpt-4o, **deepseek-v4-flash** (1M context), **deepseek-v4-flash-thinking**
- **Conditions:** control_stateless, isolated, novelty, feedback, peer, human
- **Primary outcome:** longitudinal mixed-effects model `y = β₀ + β₁·log(1+t) + β₂·C + β₃·log(1+t)·C + u_model + u_task + u_run + ε`; test whether β₃ is significantly negative for the isolated condition.

### What's included

- `research_proposal.html` — Full Stage 1 research proposal (formal HTML)
- `preregistration.md` — OSF pre-registration document with 5 hypotheses, 9 deviation contingencies
- `experiment_manifest.json` — Complete experimental grid (models, tasks, conditions, checkpoints)
- `analysis_skeleton.py` — Statistical pipeline with LMM → GEE → OLS fallback + Holm-Bonferroni correction
- `paper_outline.md` — Stage 1 paper structure
- `cover_letter.md` — draft letter. It was not sent. Later revisions label the questions as anticipated, not received.
- `pilot/` — Pilot environment scaffolding (Vending env, eval battery, LLM clients, runner)
- `smoke_test/` — Synthetic-trajectory smoke test that validates the entire pipeline
- `scripts/osf_upload.py` — Automated OSF uploader
- `scripts/publish_to_github.sh` — One-shot GitHub publisher

### What's *not* in this release

- ❌ Real experimental data (Stage 2 only)
- ❌ Trained model checkpoints (n/a — closed API models)
- ❌ Human subjects data (IRB pending)
- ❌ Pre-trained anti-isolation mechanisms (will be Stage 2 implementation)

### Reproducibility

- Random seeds: 11, 22, 33 (and 10+ additional per cell for the formal run)
- Model API versions: pinned at run time
- Smoke-test generation seed: 20260722
- Environment: Python 3.10+, statsmodels ≥ 0.14, pandas ≥ 2.0, ruptures, lifelines

### Timeline

| Milestone | Date |
|---|---|
| Stage 1 freeze (this release) | 2026-07-22 |
| Pilot data collection | 2026-08 |
| Stage 1 submission | ~2026-09 (AAMAS RR channel) |
| Formal data collection | 2026-10 → 2026-12 |
| Stage 2 paper draft | 2027-01 |
| Stage 2 submission | 2027-02 |

### Citation

```
@misc{echochambers2026prereg,
  title={Echo Chambers of One: A Causal Test of Interaction Deprivation on Long-Horizon State Stability in Language Agents (Pre-registration)},
  year={2026},
  month={7},
  note={Pre-registration Stage 1, frozen 2026-07-22}
}
```

### License

- Code: MIT
- Documentation, pre-registration, data (when released): CC-BY-4.0

### Contact

(Author emails to be added before submission.)