# Changelog

All notable changes to this repository are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Protocol pack only. `make check` validates the manifest against
  `preregistration.md` and replays `analysis_skeleton.py` on synthetic data
  with a planted slope and a null. No OSF project, no DOI, no submission.
- Corrected an in-repo double count: 5×4×6×3×3 is 1080 cells and 1080
  trajectories. The older 3240 figure counted the three seeds twice. This is
  not an OSF amendment.
- Citation audit for arXiv ids and DOIs retrieved on 2026-11-16. Unresolved
  and mislabeled citations are marked in the source files.
- Cover letter relabeled as an unsent draft. Reviewer questions are
  anticipated, not received.

- Governance baseline: LICENSE, security policy, code of conduct, contributor and
  support guides, issue and pull-request templates, CODEOWNERS, dependabot, and
  `.editorconfig` added. No research content changed.
