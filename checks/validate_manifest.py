#!/usr/bin/env python3
"""Check experiment_manifest.json against preregistration.md.

Offline. Does not contact OSF. The operative grid is the protocol-facts
block in preregistration.md; this script fails if the manifest disagrees
with that block or if its own arithmetic does not close.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "experiment_manifest.json"
PREREG = ROOT / "preregistration.md"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_facts(text: str) -> tuple[dict, str]:
    match = re.search(r"```protocol-facts\n(.*?)\n```", text, re.S)
    if not match:
        fail("preregistration.md has no ```protocol-facts block")
    facts = json.loads(match.group(1))
    prose = text[: match.start()] + text[match.end() :]
    return facts, prose


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    facts, prose = load_facts(PREREG.read_text(encoding="utf-8"))

    if manifest.get("osf_project_created", False) or facts.get("osf_project_created") is not False:
        fail("osf_project_created must be false (the OSF project has not been created)")
    schema = manifest.get("$schema")
    if isinstance(schema, str) and schema.startswith("http"):
        fail(f"$schema is an external URL ({schema}); this repo has no such schema")

    for key in (
        "version",
        "models",
        "conditions",
        "tasks",
        "lengths",
        "seeds",
        "checkpoints",
        "cells",
        "trajectories",
    ):
        if key not in facts:
            fail(f"protocol-facts missing {key}")

    if facts["version"] != "0.4" or manifest.get("version") != "0.4":
        fail("version must be 0.4 in both files")

    model_ids = [m["id"] for m in manifest["models"]]
    condition_ids = [c["id"] for c in manifest["conditions"]]
    task_ids = [t["id"] for t in manifest["tasks"]]
    lengths = manifest["context_length_manipulation"]["values"]
    seeds = manifest["seeds"]
    checkpoints = manifest["checkpoints"]

    pairs = [
        ("models", model_ids),
        ("conditions", condition_ids),
        ("tasks", task_ids),
        ("lengths", lengths),
        ("seeds", seeds),
        ("checkpoints", checkpoints),
    ]
    for key, got in pairs:
        if list(facts[key]) != list(got):
            fail(f"{key} mismatch:\n  preregistration {facts[key]}\n  manifest {got}")

    for mid in model_ids:
        if mid not in prose:
            fail(f"model id {mid} is only in the facts block, not in the preregistration prose")
    for cid in condition_ids:
        if cid not in prose:
            fail(f"condition id {cid} is missing from the preregistration prose")
    if "5 × 4 × 6 × 3 × 3" not in prose:
        fail("preregistration prose is missing the 5 × 4 × 6 × 3 × 3 grid formula")

    summary = manifest["design_summary"]
    expected_counts = {
        "models": len(model_ids),
        "lengths": len(lengths),
        "conditions": len(condition_ids),
        "tasks": len(task_ids),
        "seeds": len(seeds),
    }
    for key, count in expected_counts.items():
        if summary.get(key) != count:
            fail(f"design_summary.{key} is {summary.get(key)}, list length is {count}")

    product = 1
    for count in expected_counts.values():
        product *= count
    if summary.get("total_cells") != product or facts["cells"] != product:
        fail(f"cells must equal the product {product}")
    if summary.get("total_trajectories") != product or facts["trajectories"] != product:
        fail(
            "trajectories must equal cells "
            f"({product}): one trajectory per model×length×condition×task×seed"
        )

    max_models = set(manifest["context_length_manipulation"]["max_per_model"])
    if max_models != set(model_ids):
        fail(f"max_per_model keys {sorted(max_models)} != model ids")

    primary = manifest.get("outcomes", {}).get("primary", [])
    if "accuracy" not in primary:
        fail("outcomes.primary must include accuracy")
    if not manifest.get("exclusion_rules") or not manifest.get("deviation_contingencies"):
        fail("exclusion_rules and deviation_contingencies must be non-empty")

    budget = manifest["budget_estimate"]
    if budget.get("basis_trajectories") != product:
        fail("budget basis_trajectories must equal the corrected cell count")
    if budget.get("tokens_per_trajectory") != 2_000_000:
        fail("tokens_per_trajectory changed; the budget check expects the stated 2_000_000 assumption")
    if budget.get("total_tokens") != product * 2_000_000:
        fail("total_tokens != trajectories * tokens_per_trajectory")
    if budget.get("measured_spend_usd") is not None:
        fail("measured_spend_usd must be null; no spend has been measured")

    fraction_sum = 0.0
    line_sum = 0.0
    for name, item in budget["cost_breakdown"].items():
        fraction_sum += item["fraction"]
        expected = item["fraction"] * budget["total_tokens"] / 1_000_000 * item["rate_per_million"]
        if abs(expected - item["usd"]) > 0.02:
            fail(f"cost_breakdown.{name} usd {item['usd']} != {expected:.3f} from fraction × tokens × rate")
        line_sum += item["usd"]
    if abs(fraction_sum - 1.0) > 1e-9:
        fail(f"cost fractions sum to {fraction_sum}, not 1")
    if abs(line_sum - budget["line_item_sum_usd"]) > 0.05:
        fail(f"line_item_sum_usd {budget['line_item_sum_usd']} != {line_sum:.3f}")
    if "superseded_figures" not in budget:
        fail("budget must keep superseded_figures so the old 3240 / $2500–$4500 text is not silently dropped")

    print(
        f"OK: manifest matches preregistration "
        f"({product} cells = {product} trajectories, line-item sum ${line_sum:.3f}, not a measured cost)"
    )


if __name__ == "__main__":
    main()
