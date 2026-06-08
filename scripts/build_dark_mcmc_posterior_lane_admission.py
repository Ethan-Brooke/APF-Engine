#!/usr/bin/env python3
"""Build APF_DARK_MCMC_POSTERIOR_LANE_ADMISSION_v1 pack."""
from __future__ import annotations

import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.dark_mcmc_posterior_lane_admission import (
    DIAGNOSTIC_THRESHOLDS,
    MARKER,
    NOT_SAMPLED_V1,
    PACK_NAME,
    POSTERIOR_COORDINATES,
    SAMPLED_PARAMETER_SET,
    build_lane_contract,
    mcmc_run_grid,
    run_checks,
)

ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT / "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44" / PACK_NAME
SHARED_PACK = ROOT / "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44" / "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1"
PROFILE_LANE_PACK = ROOT / "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44" / "APF_DARK_PROFILE_LIKELIHOOD_LANE_ADMISSION_v1"
PROFILE_LAUNCH_PACK = ROOT / "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44" / "APF_DARK_PROFILE_LIKELIHOOD_FULL_SCAN_LAUNCH_v1"
MCMC_PARENT = ROOT / "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44" / "APF_DARK_SECTOR_ROUTE_C_MCMC_POSTERIOR_LAUNCH_v1"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data) -> None:
    write(path, json.dumps(data, indent=2, sort_keys=False) + "\n")


def main() -> int:
    if PACK.exists():
        shutil.rmtree(PACK)
    for d in ["docs", "results", "tables", "templates", "schemas", "scripts", "source_files"]:
        (PACK / d).mkdir(parents=True, exist_ok=True)

    contract = build_lane_contract()
    checks = run_checks()
    passed = all(c["passed"] for c in checks)
    closure = {
        "pack": PACK_NAME,
        "pack_type": "mcmc_posterior_lane_admission_not_result_pack",
        "status": "PASS_when_verifier_passes",
        "summary": "Defines the dark Route-C MCMC posterior evidence lane under the shared profile/MCMC runtime contract. This is not a posterior result pack.",
        "parent_shared_contract": "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1",
        "parent_mcmc_launch": "APF_DARK_SECTOR_ROUTE_C_MCMC_POSTERIOR_LAUNCH_v1",
        "parallel_profile_lane": "APF_DARK_PROFILE_LIKELIHOOD_LANE_ADMISSION_v1",
        "mcmc_launch_supersession": "LATEST-82 remains parent launch evidence but is not treated as converged posterior P.",
        "grid_cells": 12,
        "sampled_parameter_set": list(SAMPLED_PARAMETER_SET),
        "diagnostic_thresholds": dict(DIAGNOSTIC_THRESHOLDS),
        "exports_promoted": contract["exports_promoted"],
        "exports_preserved_non_claims": contract["exports_preserved_non_claims"],
        "verifier_marker": MARKER,
    }
    write_json(PACK / "results" / "MCMC_LANE_ADMISSION.json", contract)
    write_json(PACK / "results" / "CLOSURE_STATEMENT.json", closure)
    write_json(PACK / "results" / "CHECK_RESULTS.json", {"checks": checks, "passed": passed, "marker": MARKER if passed else "FAIL"})

    for src, dst in [
        (SHARED_PACK / "results" / "CLOSURE_STATEMENT.json", "SHARED_CONTRACT_CLOSURE_STATEMENT.json"),
        (SHARED_PACK / "results" / "SHARED_RUNTIME_CONTRACT.json", "SHARED_RUNTIME_CONTRACT.json"),
        (PROFILE_LANE_PACK / "results" / "CLOSURE_STATEMENT.json", "PROFILE_LANE_CLOSURE_STATEMENT.json"),
        (PROFILE_LAUNCH_PACK / "results" / "CLOSURE_STATEMENT.json", "PROFILE_LAUNCH_CLOSURE_STATEMENT.json"),
        (MCMC_PARENT / "results" / "CLOSURE_STATEMENT.json", "LATEST82_MCMC_LAUNCH_CLOSURE_STATEMENT.json"),
        (MCMC_PARENT / "source_files" / "MCMC_PARTIAL_RUN_SUMMARY.json", "LATEST82_MCMC_PARTIAL_RUN_SUMMARY.json"),
        (MCMC_PARENT / "source_files" / "mcmc_result_table_partial.csv", "LATEST82_MCMC_RESULT_TABLE_PARTIAL.csv"),
    ]:
        if src.exists():
            shutil.copy2(src, PACK / "source_files" / dst)

    with (PACK / "tables" / "MCMC_RUN_GRID.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cell_id", "dataset", "model", "sampled_parameter_set", "posterior_coordinates", "chains_required", "required_artifact_class", "result_status"])
        writer.writeheader()
        for c in mcmc_run_grid():
            writer.writerow({
                "cell_id": c.cell_id,
                "dataset": c.dataset,
                "model": c.model,
                "sampled_parameter_set": ";".join(c.sampled_parameter_set),
                "posterior_coordinates": ";".join(c.posterior_coordinates),
                "chains_required": c.chains_required,
                "required_artifact_class": c.required_artifact_class,
                "result_status": c.result_status,
            })

    with (PACK / "tables" / "MCMC_DIAGNOSTIC_THRESHOLDS.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["threshold", "value", "notes"])
        writer.writeheader()
        notes = {
            "Rminus1_max": "maximum R-hat minus 1 allowed per declared parameter block",
            "ESS_min": "minimum effective sample size",
            "chains_min": "minimum chains per grid cell",
            "acceptance_min": "lower acceptance-rate guard",
            "acceptance_max": "upper acceptance-rate guard",
        }
        for k, v in DIAGNOSTIC_THRESHOLDS.items():
            writer.writerow({"threshold": k, "value": v, "notes": notes[k]})

    with (PACK / "tables" / "MCMC_INTAKE_REQUIREMENTS.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["requirement", "mandatory", "notes"])
        writer.writeheader()
        for req, notes in [
            ("contract_pack", "must equal APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1"),
            ("lane_admission_pack", f"must equal {PACK_NAME}"),
            ("sampled_parameter_set", "must equal H0/ombh2/omch2/logA/ns"),
            ("apf2_coefficients_frozen", "required true for APF2 cells"),
            ("apf2_coefficients_refit", "required false"),
            ("profile_best_used_as_posterior_evidence", "required false; seed-only initialization allowed"),
            ("partial_chain_promoted", "required false"),
            ("convergence_diagnostics", "required; Rminus1/ESS/chains/acceptance gates must pass"),
            ("prior_policy", "required with declared priors and bounds"),
            ("posterior_summary", "required with marginal MAP/credible-region summary"),
            ("no_smuggling_report", "required; must forbid target-consumption and profile-as-posterior evidence"),
        ]:
            writer.writerow({"requirement": req, "mandatory": "true", "notes": notes})

    with (PACK / "tables" / "PROMOTION_FLAGS.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["flag", "value", "kind"])
        writer.writeheader()
        for k, v in contract["exports_promoted"].items():
            writer.writerow({"flag": k, "value": v, "kind": "promoted_contract_flag"})
        for k, v in contract["exports_preserved_non_claims"].items():
            writer.writerow({"flag": k, "value": v, "kind": "preserved_non_claim"})

    with (PACK / "tables" / "POSTERIOR_COORDINATES_BY_MODEL.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["model", "posterior_coordinates"])
        writer.writeheader()
        for model, coords in POSTERIOR_COORDINATES.items():
            writer.writerow({"model": model, "posterior_coordinates": ";".join(coords)})

    mcmc_template = {
        "contract_pack": "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1",
        "lane_admission_pack": PACK_NAME,
        "dataset": "desi_cmb_native",
        "model": "APF2_fixed_w2 | free_w0wa | LCDM",
        "sampled_parameter_set": list(SAMPLED_PARAMETER_SET),
        "not_sampled_v1": list(NOT_SAMPLED_V1),
        "posterior_coordinates": list(POSTERIOR_COORDINATES["APF2_fixed_w2"]),
        "apf2_coefficients_frozen": True,
        "apf2_coefficients_refit": False,
        "profile_best_used_as_posterior_evidence": False,
        "profile_best_used_as_initialization_only": False,
        "partial_chain_promoted": False,
        "diagnostics": {
            "chains_completed": None,
            "Rminus1_max": None,
            "ESS_min": None,
            "acceptance_mean": None,
        },
        "posterior_summary_pointer": "posterior_summary.json",
        "chain_outputs_pointer": "chain_outputs/",
        "prior_policy_pointer": "prior_policy.json",
        "likelihood_manifest_pointer": "likelihood_manifest.json",
        "dataset_manifest_pointer": "dataset_manifest.json",
        "environment_manifest_pointer": "environment_manifest.json",
        "no_smuggling_report_pointer": "no_smuggling_report.json",
        "no_smuggling_pass": False,
        "mcmc_status": "incomplete",
    }
    write_json(PACK / "templates" / "MCMC_RESULT_INTAKE_TEMPLATE.json", mcmc_template)

    adjud_template = {
        "contract_pack": "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1",
        "lane_admission_pack": PACK_NAME,
        "mcmc_result_cells": [],
        "all_required_cells_present": False,
        "all_convergence_gates_pass": False,
        "no_smuggling_pass": False,
        "shared_contract_pass": False,
        "can_promote_Export_dark_RouteC_MCMC_posterior_P": False,
        "exports": {
            "Export_dark_RouteC_MCMC_posterior_P": 0,
            "Export_dark_MCMC_full_posterior_P": 0,
            "Export_dark_robust_empirical_P": 0,
        },
    }
    write_json(PACK / "templates" / "MCMC_ADJUDICATION_TEMPLATE.json", adjud_template)

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "APF dark MCMC posterior lane admission artifact",
        "type": "object",
        "required": ["pack", "pack_type", "parent_shared_contract", "runtime_contract_v1", "grid", "exports_promoted", "exports_preserved_non_claims"],
        "properties": {
            "pack": {"const": PACK_NAME},
            "pack_type": {"const": "mcmc_posterior_lane_admission_not_result_pack"},
            "parent_shared_contract": {"const": "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1"},
        },
    }
    write_json(PACK / "schemas" / "mcmc_lane_admission.schema.json", schema)

    write(PACK / "README.md", f"""# {PACK_NAME}

**Status:** MCMC posterior lane admission contract, not a result pack.  
**Parent shared contract:** `APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1`.  
**Parent MCMC launch:** `APF_DARK_SECTOR_ROUTE_C_MCMC_POSTERIOR_LAUNCH_v1`.

## Purpose

This pack turns the dark Route-C MCMC posterior lane into a concrete, checkable evidence lane under the shared profile/MCMC runtime contract. It subsumes the LATEST-82 launch pack as parent infrastructure, but does not treat partial chains or queued cells as posterior closure.

It does **not** close `Export_dark_RouteC_MCMC_posterior_P`, `Export_dark_MCMC_full_posterior_P`, or `Export_dark_robust_empirical_P`.

## Runtime shape

Both profile and MCMC lanes use the shared five-parameter sampled set:

```text
H0, ombh2, omch2, logA, ns
```

Not sampled in v1:

```text
tau, mnu, nnu
```

The v1 APF2 path remains the validated runtime monkeypatch path for `camb.CAMBparams.__init__` / `set_classes`. The direct `use_tabulated_w` extra_args pathway remains forbidden in this runtime contract.

## Diagnostic thresholds

```text
chains_min = 4
Rminus1_max = 0.01
ESS_min = 200
acceptance_min = 0.05
acceptance_max = 0.8
```

## Exports promoted

```text
Export_dark_MCMC_posterior_lane_admission_contract = 1
Export_dark_MCMC_result_format_locked = 1
Export_dark_MCMC_launch_supersession_declared = 1
Export_dark_MCMC_diagnostic_thresholds_locked = 1
```

## Preserved non-claims

```text
Export_dark_RouteC_MCMC_posterior_P = 0
Export_dark_MCMC_full_posterior_P = 0
Export_dark_profile_likelihood_P = 0
Export_dark_robust_empirical_P = 0
Export_dark_APF2_full_shape_likelihood_P = 0
Export_collaboration_NERSC_reproduction = 0
Export_dark_profile_best_as_posterior_MAP = 0
Export_dark_MCMC_partial_chain_as_converged_posterior = 0
```

## Verifier

Run:

```bash
python scripts/check_dark_mcmc_posterior_lane_admission.py
```

Expected marker:

```text
{MARKER}
```
""")

    write(PACK / "docs" / "RUNNER_SPEC.md", """# MCMC posterior runner spec

The runner is a future external-runtime artifact. This admission pack defines the expected outputs.

For each dataset/model cell:

- load the exact dataset and likelihood manifests declared by the shared contract;
- run at least four Cobaya chains under the five-parameter v1 runtime contract;
- for `free_w0wa`, include `(w0, wa)` as posterior coordinates in addition to the five runtime parameters;
- for `APF2_fixed_w2`, use the frozen APF2 curve via the declared monkeypatch injection path;
- emit chain outputs, convergence diagnostics, posterior summaries, prior policy, and no-smuggling reports.

Profile-best values may be used only as initialization. They must not be treated as posterior evidence or as the expected location of posterior mass.
""")
    write(PACK / "docs" / "HONEST_NON_CLAIMS.md", """# Honest non-claims

This pack is not a result pack. It does not claim:

```text
Export_dark_RouteC_MCMC_posterior_P = 1
Export_dark_MCMC_full_posterior_P = 1
Export_dark_profile_likelihood_P = 1
Export_dark_robust_empirical_P = 1
Export_dark_profile_best_as_posterior_MAP = 1
Export_dark_MCMC_partial_chain_as_converged_posterior = 1
```

The LATEST-82 MCMC launch pack remains useful infrastructure and partial-run context. It does not become a converged posterior result by being re-wrapped.
""")
    write(PACK / "docs" / "PROFILE_MCMC_SEPARATION_GUARD.md", """# Profile/MCMC separation guard

The profile and MCMC lanes are parallel, not hierarchical.

Allowed:

```text
profile_best_used_as_initialization_only = true
```

Forbidden:

```text
profile_best_used_as_posterior_evidence
profile_best_as_expected_MAP
posterior_outputs_as_profile_inputs
partial_chain_as_converged_result
APF2_coefficients_refit
```

The LATEST-82 caveat remains load-bearing: profile-best and marginal posterior MAP may differ while achieving similar chi2 depth. This is not a defect; it means each lane answers a different statistical question.
""")
    write(PACK / "docs" / "CONVERGENCE_REQUIREMENTS.md", """# MCMC convergence requirements

A future result pack must provide:

1. at least four chains per declared cell;
2. Rminus1 <= 0.01 for the declared posterior coordinate block;
3. ESS >= 200;
4. mean acceptance in [0.05, 0.8];
5. posterior summary with marginal MAP / credible intervals;
6. prior policy and likelihood manifest;
7. no-smuggling report;
8. APF2 frozen-coefficient guard for APF2 cells;
9. explicit scope if not all 12 cells are complete.

Partial chains and smoke runs fail closed.
""")

    verifier = f'''#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = "{PACK_NAME}"
MARKER = "{MARKER}"
EXPECTED_DATASETS = ["desi_cmb_native", "desi_cmb_pantheonplus", "desi_cmb_union3", "desi_cmb_desy5"]
EXPECTED_MODELS = ["APF2_fixed_w2", "free_w0wa", "LCDM"]
EXPECTED_PARAMS = ["H0", "ombh2", "omch2", "logA", "ns"]

contract = json.loads((ROOT / "results" / "MCMC_LANE_ADMISSION.json").read_text())
closure = json.loads((ROOT / "results" / "CLOSURE_STATEMENT.json").read_text())

assert contract["pack"] == EXPECTED
assert closure["pack"] == EXPECTED
assert contract["pack_type"] == "mcmc_posterior_lane_admission_not_result_pack"
assert contract["parent_shared_contract"] == "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1"
print("[1/8] identity and shared-contract parent: PASS")

assert contract["parent_mcmc_launch"]["grade"] == "launch_infrastructure_schema_adjudicator_not_converged_posterior_result"
assert contract["parent_mcmc_launch"]["status"] == "subsumed_as_parent_evidence_not_promoted"
assert (ROOT / "source_files" / "LATEST82_MCMC_LAUNCH_CLOSURE_STATEMENT.json").exists()
print("[2/8] LATEST-82 MCMC launch parent imported but not promoted: PASS")

rt = contract["runtime_contract_v1"]
assert rt["sampled_parameter_set"] == EXPECTED_PARAMS
assert rt["not_sampled_v1"] == ["tau", "mnu", "nnu"]
assert rt["version_pins"] == {{"Cobaya": "3.6.2", "CAMB": "1.6.6"}}
assert rt["forbidden_apf2_injection_mechanism"] == "use_tabulated_w extra_args pathway"
print("[3/8] five-parameter runtime contract and injection path: PASS")

rows = list(csv.DictReader((ROOT / "tables" / "MCMC_RUN_GRID.csv").open()))
assert len(rows) == 12
assert {{(r["dataset"], r["model"]) for r in rows}} == {{(d, m) for d in EXPECTED_DATASETS for m in EXPECTED_MODELS}}
assert all(r["sampled_parameter_set"].split(";") == EXPECTED_PARAMS for r in rows)
print("[4/8] 4x3 MCMC run grid complete: PASS")

for r in rows:
    coords = [x for x in r["posterior_coordinates"].split(";") if x]
    if r["model"] == "free_w0wa":
        assert coords == EXPECTED_PARAMS + ["w0", "wa"]
    else:
        assert coords == EXPECTED_PARAMS
print("[5/8] posterior coordinate policy by model: PASS")

thresholds = {{r["threshold"]: float(r["value"]) for r in csv.DictReader((ROOT / "tables" / "MCMC_DIAGNOSTIC_THRESHOLDS.csv").open())}}
assert thresholds["chains_min"] == 4
assert thresholds["Rminus1_max"] == 0.01
assert thresholds["ESS_min"] == 200
assert thresholds["acceptance_min"] == 0.05 and thresholds["acceptance_max"] == 0.8
print("[6/8] convergence thresholds locked: PASS")

promoted = contract["exports_promoted"]
assert promoted["Export_dark_MCMC_posterior_lane_admission_contract"] == 1
assert promoted["Export_dark_MCMC_result_format_locked"] == 1
assert promoted["Export_dark_MCMC_launch_supersession_declared"] == 1
assert promoted["Export_dark_MCMC_diagnostic_thresholds_locked"] == 1
print("[7/8] contract-only export flags promoted: PASS")

non = contract["exports_preserved_non_claims"]
for k in [
    "Export_dark_RouteC_MCMC_posterior_P",
    "Export_dark_MCMC_full_posterior_P",
    "Export_dark_profile_likelihood_P",
    "Export_dark_robust_empirical_P",
    "Export_dark_profile_best_as_posterior_MAP",
    "Export_dark_MCMC_partial_chain_as_converged_posterior",
]:
    assert non[k] == 0, k
for rel in [
    "templates/MCMC_RESULT_INTAKE_TEMPLATE.json",
    "templates/MCMC_ADJUDICATION_TEMPLATE.json",
    "schemas/mcmc_lane_admission.schema.json",
    "docs/RUNNER_SPEC.md",
    "docs/PROFILE_MCMC_SEPARATION_GUARD.md",
    "docs/CONVERGENCE_REQUIREMENTS.md",
]:
    assert (ROOT / rel).exists(), rel
print("[8/8] non-claims plus templates/schema/docs present: PASS")
print(MARKER)
'''
    write(PACK / "scripts" / "check_dark_mcmc_posterior_lane_admission.py", verifier)
    (PACK / "scripts" / "check_dark_mcmc_posterior_lane_admission.py").chmod(0o755)

    print(f"Built {PACK}")
    print(MARKER if passed else "CHECKS_FAILED")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
