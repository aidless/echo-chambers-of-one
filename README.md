# Echo Chambers of One

This repository is a preregistration and analysis-protocol pack for a study that has not been run: whether withholding fresh external input changes how stable a long-horizon stateful language-model agent stays.
`make check` proves two things only: `experiment_manifest.json` matches `preregistration.md`, and `analysis_skeleton.py` recovers a planted slope on synthetic data and does not treat the matching synthetic null contrasts as that effect.
It does not prove any empirical finding about agents. The OSF project has not been created, there is no DOI, and this git tree is not a formal preregistration.

STATUS: WORK-IN-PROGRESS — not A yet. `make check` passes. The remaining gaps are listed in `STATUS.md`. One of them is the GitHub About text, which a commit cannot change.

Repo label: `v0.4-pre-reg`. Protocol document version: `0.4` (`preregistration.md`, `experiment_manifest.json`). Those two names are the same draft. The git tag `v0.4-pre-reg` points at an older commit (`6fb5aee4b0afb6ff19d53198618a2bc7e1604832`, 2026-07-29). That tag is not an OSF timestamp. Do not move it onto a later commit and call the result a registration.

Author: the protocol text names no person. Maintenance path: GitHub `@aidless` (`.github/CODEOWNERS`).

## Run

Python 3.12 and the pins in `requirements.txt` (the recovery numbers are not compared across versions):

```bash
python3 -m pip install -r requirements.txt
make check
```

The check is offline after that install. It does not call a model API, OSF, arXiv, or Crossref. On this machine it finishes in well under 15 minutes; most of a cold start is the pip install.

What the three steps do:

1. `checks/validate_manifest.py` checks the manifest's lists, the 5×4×6×3×3 = 1080 cell count, and the budget arithmetic against the `protocol-facts` block in `preregistration.md`.
2. `checks/parameter_recovery.py` runs `analysis_skeleton.py` on synthetic rows. Seeds 1000–1019 plant `cond_feedback_x_logstep = +0.04` on `accuracy` (reference level `isolated`) and plant zeros on the other contrasts. Seeds 2000–2019 plant all zeros. The committed recomputation is `checks/artifacts/parameter_recovery.json`.
3. `checks/honesty.py` checks the cover letter, the OSF wording, the citation audit, and the SHA-256 stamp in `checks/artifacts/protocol_stamp.json`.

The planted `+0.04` is the same slope gap as preregistration §7's "β3 < 0 for isolated" with the reference level flipped. The skeleton does not fit the length term or the three-way interaction in §7. The all-null run is allowed to flag a small coefficient: that is what a 0.05 test does. The cap and the actual flagged seeds are in the artifact. This is not a power calculation for the 1080-cell study.

## What is not in this repository

- No OSF project, project id, registration, or DOI.
- No submitted manuscript and no received reviews. `cover_letter.md` is an unsent draft. Its questions are anticipated.
- No trajectories from a model API. Files under `smoke_test/results/` and `pilot/results/` are old synthetic or mock output. `smoke_test/generate_synthetic_trajectories.py` uses Python's salted `hash()`, so those files are not the reproducibility check.
- No measured spend. The manifest's dollar figure is `trajectories × an assumed token count × assumed rates`.

## Outside git

Commits do not set the GitHub About panel. Suggested About text, with the website left blank (do not link an OSF page that does not exist):

> Preregistration pack for a not-yet-run study of interaction deprivation in long-horizon LLM agents. No OSF project, no DOI, no empirical results. `make check` recovers a planted synthetic effect.

Creating the OSF project is a separate human decision. Nothing in this repo is a registration until that exists.

## Map

| File | Role |
|---|---|
| `preregistration.md` | Draft protocol v0.4, including the machine-checked grid |
| `experiment_manifest.json` | Same grid, in JSON |
| `analysis_skeleton.py` | Runnable LMM → GEE → OLS skeleton, not the full §7 model |
| `FAILURE_MODES.md` | Misspecification, fallback, confounds, falsification |
| `CITATION_AUDIT.md` | Which arXiv ids and DOIs resolved on 2026-11-16 |
| `cover_letter.md` | Unsent draft and anticipated questions |
| `STATUS.md` | Same status words as this file |

## License

Code: MIT. Protocol text and any later data: CC-BY-4.0. See `LICENSE` and `LICENSE-DATA`.
