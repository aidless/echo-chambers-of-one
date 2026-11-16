# Cover letter draft — not a submission

**NOT SUBMITTED.** No conference, journal, or registered-report track has received this letter. There is no submission id and no decision.

**ANTICIPATED questions follow the draft.** No review was received. Nobody wrote these questions to the authors, and the replies were not sent. They are notes about objections a future reviewer might raise. If a real review arrives, these paragraphs are not that review and must not be quoted as one.

The grid below follows `preregistration.md` v0.4 (5 models, 1080 cells = 1080 trajectories). The OSF project has not been created. Author names are not in this repository. Maintenance path: `@aidless` (`.github/CODEOWNERS`).

Target that a later submission might consider: an AAMAS registered-report track, if one is open at the time. This file does not record a verified deadline.

---

Draft text, not for sending as-is:

We would like to propose a Registered Report Stage 1, not to claim that one has been filed.

**Echo Chambers of One: A Causal Test of Interaction Deprivation on Long-Horizon State Stability in Language Agents**

The question is whether a stateful language-model agent declines faster over a long horizon when fresh external input is withheld, after task and context length are accounted for. The draft design crosses 5 models, 4 context lengths, 6 conditions, 3 tasks, and 3 seeds (1080 trajectories, one per cell). The runnable analysis in the repository is a smaller model than preregistration §7: it has no length factor and no three-way interaction. That gap is spelled out in `FAILURE_MODES.md`.

The six conditions are not yet matched on token count. The manifest stores different external-token quotas. Until a filler rule exists in code, a condition gap is confounded with prompt length.

---

# Anticipated questions

These are not reviewer comments.

## Q1. Why six conditions instead of isolated versus not?

Draft answer: an isolated-versus-rest contrast cannot separate novelty, corrective feedback, a peer, and a human. The six rows are still not pure. `peer` and `human` also turn novelty and feedback on, and `control_stateless` differs from `isolated` by state persistence rather than by an external signal. A review that called the design under-identified on those points would be pointing at the manifest, not at a misunderstanding.

## Q2. How would context length and task length be separated from the manipulation?

Draft answer: the written plan adds a length factor and four state views (raw, structured, fake memory, lorem). The length factor is not in `analysis_skeleton.py`. The state views are not implemented. The quotas in the manifest are unequal. Those are open holes, not solved controls.

## Q3. Why these five model ids?

Draft answer: the ids are the v0.4 list (claude-sonnet-4.6, claude-opus-4.7, gpt-5, deepseek-v4-flash, qwen3-235b-thinking). This repository does not verify that a vendor currently serves each id. Prices in the manifest are assumptions used to multiply token counts. They are not invoices.

## Q4. Is this a benchmark paper?

Draft answer: the draft uses published tasks as settings. It does not claim a new benchmark, and it has no agent results to report.

## Q5. What is new if self-talk and memory compression already have papers?

Draft answer: the draft's claim would be the contrast under one protocol, if the data were collected. Several of the mechanism citations were checked in `CITATION_AUDIT.md`; rows marked UNVERIFIED or MISMATCH are not support.

## Q6. Won't a peer model share the primary model's errors?

Draft answer: the manifest says the peer is an independently seeded trajectory. That sentence is a plan. There is no peer runner that enforces it.

## Q7. What if the mixed model does not converge?

Draft answer: `analysis_skeleton.py` falls back from a random-intercept LMM to an independence GEE and then to pooled OLS, and it records `method`. It does not call `brms`, which §7 also names. A singular fit that does not raise can still be reported as `mixedlm_reml`. Details are in `FAILURE_MODES.md`.

## Q8. Why not run 10,000 steps immediately?

Draft answer: the protocol's own plan is a pilot before the full grid. No pilot on a live API has been run in this tree. The 10,000-step figure is a design choice, not a completed run.

## Q9. Why mention AAMAS rather than another venue?

Draft answer: agent autonomy and long-horizon interaction are the reason AAMAS is on the list. No venue has been contacted. CogSci, CHI, and ICLR are not backup submissions; they are names in an old note.

## Q10. What would count against the hypothesis?

Draft answer: under the §7 coding (reference = feedback), a positive isolated × log(1+t) coefficient after the pre-specified correction would contradict the directional claim. A non-significant result would fail to support it. The protocol states no equivalence bound, so a non-significant p-value is not by itself a proof of no effect. An unequal token budget would also block a causal reading. See `FAILURE_MODES.md`.
