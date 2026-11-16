# Failure modes

This file is about the draft protocol and the code that exists today. It is not a result.

The runnable analysis is `analysis_skeleton.py`. The written analysis is preregistration §7. They are not the same model. `make check` exercises the runnable one on synthetic data.

## Model misspecification

§7 writes

```
y = β0 + β1·log(1+t) + β2·C + β3·log(1+t)×C
  + β4·L + β5·log(1+t)×L + β6·log(1+t)×C×L
  + u_model + u_task + u_seed + ε
```

with reference level `feedback`, H1 as β3 < 0 for `isolated`, and H3 as a test of β6. The skeleton fits only `log(1+t)`, condition indicators, and their interactions, with a single random intercept grouped by `trajectory_id`. It does not take a length factor, so it cannot estimate β4, β5, or β6. It does not fit crossed random effects for model, task, and seed. Its default reference level is `isolated`, which flips the sign of the condition gap relative to §7.

The multiplicity plan in §7 names Westfall–Young step-down minP as the primary correction and Holm as a sensitivity. The script applies Holm to whatever interaction p-values are in the file it was given. That family changes if the CSV has more outcomes or conditions. `brms` is named in the fallback chain and is not imported.

The recovery design uses an unbounded Gaussian outcome. A real accuracy score in [0, 1] will bend a log-linear slope toward zero once it hits a bound. The older smoke generator also clips, and it draws part of its level from Python's per-process `hash()`, so those files are not a stable draw.

H1's prose says the isolated curve is lower than "the 5 conditions with external signals." The condition table has six rows. `control_stateless` has no external signal. §7 instead defines H1 as the isolated-versus-feedback contrast. Those are three different statements. The script does not choose among them.

The low-power guard is also not the one in the text. The text says `n_groups < 5` per cell. The code sets `n_groups` to the number of distinct `trajectory_id` values in the whole file.

## LMM non-convergence fallback

`fit_lmm` tries a random-intercept `MixedLM` (REML). If that raises, it fits a Gaussian GEE with an independence working correlation. If that raises, it fits pooled OLS. If the whole file has fewer than 5 trajectories, it skips straight to OLS.

Independence GEE standard errors ignore residual correlation inside a trajectory, so a "significant" GEE fallback is not the mixed-model test. OLS has the same problem. The JSON records `method` and, on a fallback, `fallback_reason`.

A singular random-intercept fit does not always raise. statsmodels can return `mixedlm_reml` with a convergence warning and a variance component on the boundary. The script will then label that fit as the mixed model. The recovery runs on seeds 1000–1019 happened to converge; that does not mean a real trajectory file will.

There is no `brms` stage. Installing R and adding it would be a change to the pipeline, not something this tree does.

## Confound threats

`external_token_quota_per_100` in the manifest is 0, 0, 1800, 100, 1900, and 2000 across the six conditions. The prose says the six conditions share a token budget and differ only in the type of external signal. Nothing in `pilot/` or the manifest adds filler tokens to the zero-quota arms. If the manipulation is implemented as written in the quota field, condition is confounded with how much text the agent sees. The four state-view counterfactuals are the planned check on that confound. They are specified and not implemented.

`peer` and `human` also set `novelty_enabled` and `feedback_enabled`. They are bundles. A peer-versus-isolated gap would not identify peer interaction by itself.

`control_stateless` and `isolated` have the same quota and the same flags. The text distinguishes them by whether state persists. That is a memory manipulation, not an interaction manipulation.

Model ids (`claude-sonnet-4.6`, `claude-opus-4.7`, `gpt-5`, `deepseek-v4-flash`, `qwen3-235b-thinking`) are names in the protocol. This repo does not check that a vendor currently serves those ids, or that the context lengths in `max_per_model` match a vendor card.

The `human` arm needs participants and an IRB decision. Section 15 says the IRB application is not approved. There is no approval id to put here.

The judge protocol in §6.5 names three models and agreement thresholds. There is no judge implementation in the tree, and the claim that HORIZON defines the three failure categories used here is unverified (see `CITATION_AUDIT.md`).

`make check` does not estimate power for 1080 trajectories. A recovery on 90 short synthetic series with a planted gap of 0.04 and residual sd 0.03 says the script can see that gap. It says nothing about the variance of a real agent.

## What would falsify the hypothesis

The directional claim that §7 actually writes down is: with reference level `feedback`, the isolated × log(1+t) coefficient is negative (isolation declines faster than feedback).

That claim is contradicted by a result in the other direction: under that coding, and after the correction the protocol still says is primary, the isolated × log(1+t) coefficient is positive. The same fact, under the skeleton's default coding (reference `isolated`), is a negative `cond_feedback_x_logstep`.

A confidence interval that covers zero does not falsify the directional claim. The protocol does not state a smallest effect that would count as "no meaningful gap," and it does not state an equivalence bound. The deviation plan already says to report a corrected null as a null. That is a failure to support H1, not a demonstration that the gap is absent.

Two further results would knock out the causal reading even if the slope gap pointed the predicted way:

- The manifest's own state-view rule fails: the isolated-versus-feedback gap is absent in the raw and structured views, or it remains in the fake-memory view. The rule's wording also requires the gap to disappear under fake memory before the authors call the gap "loneliness." This file does not adopt that word as a finding; the rule is the protocol's, and the views have not been built.
- The token quotas stay unequal and no matched filler is added. A slope gap in that design is compatible with "more text in the prompt" and does not identify interaction type.

H2 (feedback steeper than novelty) and H3 (the three-way length interaction) are separate claims. The skeleton cannot test H3. A significant two-way interaction is not H3.
