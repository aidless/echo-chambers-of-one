# STATUS

STATUS: WORK-IN-PROGRESS — not A yet

Repo label: `v0.4-pre-reg`. Protocol document version: `0.4`.

`make check` passes on this tree. The bar is still open because of the items below.

## Gaps

1. GitHub About, read on 2026-11-16, is: "Preregistered study (v0.4) on self-reinforcing single-agent feedback loops: pilot scripts, budget, OSF structure." That calls the study preregistered. It is not. The homepage field is empty, which is right. A commit cannot edit About. Suggested description: "Protocol pack for a not-yet-run study of interaction deprivation in long-horizon LLM agents. No OSF project, no DOI, no empirical results." The topic `osf` reads like a project exists; `protocol` would be more accurate.
2. The OSF project is not created. Leave it that way until a person chooses to register. A git push is not a registration. If someone later creates the project, the description should say the protocol was a repo draft first, and the registration date is the OSF registration date, not 2026-07-22 or 2026-07-29.
3. `analysis_skeleton.py` is not the model in preregistration §7. It has no length factor, so it cannot test β6. It does not run Westfall–Young or `brms`. Its reference level defaults to `isolated`, and the `n < 5` guard counts trajectories in the whole file rather than per cell. `make check` exercises this skeleton only.
4. External token quotas differ by condition, and the state-view counterfactuals are not implemented. A future slope gap would not identify interaction type until that is fixed.
5. `CITATION_AUDIT.md` is a retrieval on 2026-11-16. `make check` does not contact arXiv or Crossref again. `10.1038/s41562-024-01909-1` did not resolve. arXiv:2606.30616 is Agents-A1, not a Llama 4 paper.

This is a preregistration and analysis-protocol pack. It is not a completed study.

- OSF project: not created. No OSF project id. No DOI. No registration.
- Submission: none. `cover_letter.md` is an unsent draft. The questions in it are anticipated, not received.
- Empirical agent results: none. `make check` replays `analysis_skeleton.py` on synthetic data with a planted slope and a null.
- Author: no person is named as author in the protocol. Maintenance path: GitHub `@aidless` (`.github/CODEOWNERS`).

The git tag `v0.4-pre-reg` is commit `6fb5aee4b0afb6ff19d53198618a2bc7e1604832` (2026-07-29). It is an older snapshot, not an OSF timestamp.

GitHub About text is outside this repository. Suggested wording is in `README.md`. Leave the website field blank until an OSF project actually exists.
