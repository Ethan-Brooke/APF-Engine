#!/usr/bin/env python3
"""Build APF_DARK_PROFILE_LIKELIHOOD_LANE_ADMISSION_v1 pack."""
from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

from apf.dark_profile_likelihood_lane_admission import (
    PACK_NAME,
    MARKER,
    build_lane_contract,
    profile_run_grid,
    run_checks,
    SAMPLED_PARAMETER_SET,
    NOT_SAMPLED_V1,
    OUTER_PROFILE_COORDINATES,
)

ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT / "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44" / PACK_NAME
SHARED_PACK = ROOT / "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44" / "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1"
PROFILE_PARENT = ROOT / "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44" / "APF_DARK_SECTOR_ROUTE_C_PROFILE_PROBE_ALL_DATASETS_v1"
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
    closure = {
        "pack": PACK_NAME,
        "pack_type": "profile_likelihood_lane_admission_not_result_pack",
        "status": "PASS_when_verifier_passes",
        "summary": "Defines the full dark Route-C profile-likelihood evidence lane under the shared profile/MCMC runtime contract. This is not a profile result pack.",
        "parent_shared_contract": "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1",
        "parent_profile_probe": "APF_DARK_SECTOR_ROUTE_C_PROFILE_PROBE_ALL_DATASETS_v1",
        "profile_probe_supersession": "LATEST-81 remains parent evidence and candidate support but is not treated as a continuous profile scan or as profile-likelihood P.",
        "grid_cells": 12,
        "sampled_parameter_set": list(SAMPLED_PARAMETER_SET),
        "outer_profile_coordinates_for_free_w0wa": list(OUTER_PROFILE_COORDINATES),
        "exports_promoted": contract["exports_promoted"],
        "exports_preserved_non_claims": contract["exports_preserved_non_claims"],
        "verifier_marker": MARKER,
    }
    write_json(PACK / "results" / "PROFILE_LANE_ADMISSION.json", contract)
    write_json(PACK / "results" / "CLOSURE_STATEMENT.json", closure)
    write_json(PACK / "results" / "CHECK_RESULTS.json", {"checks": checks, "passed": all(c["passed"] for c in checks), "marker": MARKER if all(c["passed"] for c in checks) else "FAIL"})

    parent_table = PROFILE_PARENT / "tables" / "DELTA_CHI2_TABLE.csv"
    if parent_table.exists():
        shutil.copy2(parent_table, PACK / "source_files" / "LATEST81_PROFILE_PROBE_DELTA_CHI2_TABLE.csv")
    parent_adjud = PROFILE_PARENT / "source_files" / "profile_probe_adjudication.json"
    if parent_adjud.exists():
        shutil.copy2(parent_adjud, PACK / "source_files" / "LATEST81_PROFILE_PROBE_ADJUDICATION.json")
    shared_closure = SHARED_PACK / "results" / "CLOSURE_STATEMENT.json"
    if shared_closure.exists():
        shutil.copy2(shared_closure, PACK / "source_files" / "SHARED_CONTRACT_CLOSURE_STATEMENT.json")
    mcmc_closure = MCMC_PARENT / "results" / "CLOSURE_STATEMENT.json"
    if mcmc_closure.exists():
        shutil.copy2(mcmc_closure, PACK / "source_files" / "LATEST82_MCMC_LAUNCH_CLOSURE_STATEMENT.json")

    with (PACK / "tables" / "PROFILE_RUN_GRID.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cell_id", "dataset", "model", "sampled_parameter_set", "outer_profile_coordinates", "required_artifact_class", "result_status"])
        writer.writeheader()
        for c in profile_run_grid():
            writer.writerow({
                "cell_id": c.cell_id,
                "dataset": c.dataset,
                "model": c.model,
                "sampled_parameter_set": ";".join(c.sampled_parameter_set),
                "outer_profile_coordinates": ";".join(c.outer_profile_coordinates),
                "required_artifact_class": c.required_artifact_class,
                "result_status": c.result_status,
            })
    with (PACK / "tables" / "PROFILE_INTAKE_REQUIREMENTS.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["requirement", "mandatory", "notes"])
        writer.writeheader()
        for req, notes in [
            ("contract_pack", "must equal APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1"),
            ("lane_admission_pack", f"must equal {PACK_NAME}"),
            ("sampled_parameter_set", "must equal H0/ombh2/omch2/logA/ns"),
            ("apf2_coefficients_frozen", "required true for APF2 cells"),
            ("apf2_coefficients_refit", "required false"),
            ("profile_probe_used_as_full_scan", "required false"),
            ("likelihood_manifest", "required with Cobaya/CAMB versions and likelihood stack"),
            ("environment_manifest", "required with runtime pins"),
            ("no_smuggling_report", "required; must forbid target-consumption and posterior-as-input"),
        ]:
            writer.writerow({"requirement": req, "mandatory": "true", "notes": notes})
    with (PACK / "tables" / "PROMOTION_FLAGS.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["flag", "value", "kind"])
        writer.writeheader()
        for k, v in contract["exports_promoted"].items():
            writer.writerow({"flag": k, "value": v, "kind": "promoted_contract_flag"})
        for k, v in contract["exports_preserved_non_claims"].items():
            writer.writerow({"flag": k, "value": v, "kind": "preserved_non_claim"})

    profile_template = {
        "contract_pack": "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1",
        "lane_admission_pack": PACK_NAME,
        "dataset": "desi_cmb_native",
        "model": "APF2_fixed_w2 | free_w0wa | LCDM",
        "sampled_parameter_set": list(SAMPLED_PARAMETER_SET),
        "not_sampled_v1": list(NOT_SAMPLED_V1),
        "outer_profile_coordinates": [],
        "apf2_coefficients_frozen": True,
        "apf2_coefficients_refit": False,
        "profile_probe_used_as_full_scan": False,
        "chi2_min": None,
        "minuslogpost_min": None,
        "bestfit_parameters": {},
        "likelihood_manifest_pointer": "likelihood_manifest.json",
        "dataset_manifest_pointer": "dataset_manifest.json",
        "environment_manifest_pointer": "environment_manifest.json",
        "no_smuggling_report_pointer": "no_smuggling_report.json",
        "profile_status": "incomplete",
    }
    write_json(PACK / "templates" / "PROFILE_RESULT_INTAKE_TEMPLATE.json", profile_template)
    adjud_template = {
        "contract_pack": "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1",
        "lane_admission_pack": PACK_NAME,
        "profile_result_cells": [],
        "delta_chi2_table": [],
        "all_required_cells_present": False,
        "no_smuggling_pass": False,
        "shared_contract_pass": False,
        "can_promote_Export_dark_profile_likelihood_P": False,
        "exports": {
            "Export_dark_profile_likelihood_P": 0,
            "Export_dark_robust_empirical_P": 0
        }
    }
    write_json(PACK / "templates" / "PROFILE_ADJUDICATION_TEMPLATE.json", adjud_template)
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "APF dark profile likelihood lane admission artifact",
        "type": "object",
        "required": ["pack", "pack_type", "parent_shared_contract", "runtime_contract_v1", "grid", "exports_promoted", "exports_preserved_non_claims"],
        "properties": {
            "pack": {"const": PACK_NAME},
            "pack_type": {"const": "profile_likelihood_lane_admission_not_result_pack"},
            "parent_shared_contract": {"const": "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1"}
        }
    }
    write_json(PACK / "schemas" / "profile_lane_admission.schema.json", schema)

    write(PACK / "README.md", f"""# {PACK_NAME}

**Status:** profile-likelihood lane admission contract, not a result pack.  
**Parent shared contract:** `APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1`.  
**Parent profile probe:** `APF_DARK_SECTOR_ROUTE_C_PROFILE_PROBE_ALL_DATASETS_v1`.

## Purpose

This pack turns the dark Route-C profile-likelihood lane into a concrete, checkable evidence lane under the shared profile/MCMC runtime contract. It supersedes the LATEST-81 3x3 profile probe as the canonical input format for future profile results, while preserving LATEST-81 as probe-grade parent evidence.

It does **not** close `Export_dark_profile_likelihood_P`. It only locks the full-scan lane shape, result templates, no-smuggling rules, and promotion boundary.

## Runtime shape

Both profile and MCMC lanes use the shared five-parameter nuisance/runtime set:

```text
H0, ombh2, omch2, logA, ns
```

Not sampled in v1:

```text
tau, mnu, nnu
```

For `free_w0wa`, `(w0, wa)` are outer profile coordinates. They are not allowed to silently change the shared five-parameter nuisance contract. APF2 remains a frozen structural curve, not a refit.

## What a future profile result must provide

```text
profile_result.json
profile_surface.csv or profile_trace.csv
bestfit_table.csv
likelihood_manifest.json
dataset_manifest.json
environment_manifest.json
input_ledger.json
no_smuggling_report.json
```

## Exports promoted

```text
Export_dark_profile_likelihood_lane_admission_contract = 1
Export_dark_profile_likelihood_full_scan_format_locked = 1
Export_dark_profile_likelihood_probe_supersession_declared = 1
```

## Preserved non-claims

```text
Export_dark_profile_likelihood_P = 0
Export_dark_RouteC_MCMC_posterior_P = 0
Export_dark_MCMC_full_posterior_P = 0
Export_dark_robust_empirical_P = 0
Export_dark_profile_probe_as_full_scan_P = 0
Export_dark_profile_best_as_posterior_MAP = 0
Export_dark_APF2_full_shape_likelihood_P = 0
Export_collaboration_NERSC_reproduction = 0
```

## Verifier

Run:

```bash
python scripts/check_dark_profile_likelihood_lane_admission.py
```

Expected marker:

```text
{MARKER}
```
""")
    write(PACK / "docs" / "RUNNER_SPEC.md", """# Profile-likelihood runner spec

The runner is a future external-runtime artifact. This admission pack defines the expected outputs.

For each dataset/model cell:

- load the exact dataset and likelihood manifests declared by the shared contract;
- profile the shared five-parameter set `H0, ombh2, omch2, logA, ns`;
- for `free_w0wa`, treat `(w0, wa)` as outer profile coordinates;
- for `APF2_fixed_w2`, use the frozen APF2 curve via the declared monkeypatch injection path;
- for `LCDM`, run the matched baseline under the same likelihood stack;
- emit `profile_result.json` plus tabular trace/surface artifacts.

Profile-best may be used for chain initialization only. It must not be treated as posterior evidence or as expected posterior MAP.
""")
    write(PACK / "docs" / "HONEST_NON_CLAIMS.md", """# Honest non-claims

This pack is not a result pack. It does not claim:

```text
Export_dark_profile_likelihood_P = 1
Export_dark_RouteC_MCMC_posterior_P = 1
Export_dark_MCMC_full_posterior_P = 1
Export_dark_robust_empirical_P = 1
Export_dark_profile_probe_as_full_scan_P = 1
Export_dark_profile_best_as_posterior_MAP = 1
```

The LATEST-81 profile probe remains useful parent evidence but does not become a full continuous/adaptive profile scan by being re-wrapped.
""")
    write(PACK / "docs" / "PROFILE_VS_MCMC_POLICY.md", """# Profile vs MCMC policy

Profile likelihood and MCMC are equal-priority parallel evidence lanes under one shared contract.

```text
profile lane: point-likelihood support after profiling nuisance/runtime parameters
MCMC lane: posterior mass under priors and convergence diagnostics
```

The LATEST-82 caveat remains load-bearing: profile-best and marginal posterior MAP may sit at different parameter locations while reaching similar chi2 depth. This is not a defect.

Forbidden:

```text
profile_best_as_posterior_evidence
profile_best_as_expected_MAP
profile_probe_as_full_scan
APF2_coefficients_refit
```
""")
    write(PACK / "docs" / "CONTINUOUS_SCAN_REQUIREMENTS.md", """# Continuous/adaptive profile scan requirements

A future profile result pack must either provide a true continuous/adaptive profile scan or explicitly scope any incomplete result.

Minimum requirements:

1. all declared cells either complete or explicitly scoped;
2. per-cell bestfit parameters and chi2/minuslogpost values;
3. surface/trace file sufficient to audit the minimum;
4. shared five-parameter nuisance set preserved;
5. APF2 frozen-curve guard passing;
6. no profile-probe grid used as a full-scan substitute;
7. no posterior outputs consumed as profile inputs;
8. exact likelihood/data/environment manifests present.
""")

    verifier = '''#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = "APF_DARK_PROFILE_LIKELIHOOD_LANE_ADMISSION_v1"
MARKER = "DARK_PROFILE_LIKELIHOOD_LANE_ADMISSION_PASS"
EXPECTED_DATASETS = ["desi_cmb_native", "desi_cmb_pantheonplus", "desi_cmb_union3", "desi_cmb_desy5"]
EXPECTED_MODELS = ["APF2_fixed_w2", "free_w0wa", "LCDM"]
EXPECTED_PARAMS = ["H0", "ombh2", "omch2", "logA", "ns"]

contract = json.loads((ROOT / "results" / "PROFILE_LANE_ADMISSION.json").read_text())
closure = json.loads((ROOT / "results" / "CLOSURE_STATEMENT.json").read_text())

assert contract["pack"] == EXPECTED
assert closure["pack"] == EXPECTED
assert contract["pack_type"] == "profile_likelihood_lane_admission_not_result_pack"
assert contract["parent_shared_contract"] == "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1"
print("[1/8] identity and shared-contract parent: PASS")

assert contract["parent_profile_probe"]["grade"] == "probe_grade_discrete_3x3_grid_candidate_not_full_scan"
assert contract["parent_profile_probe"]["status"] == "subsumed_as_parent_evidence_not_promoted"
assert (ROOT / "source_files" / "LATEST81_PROFILE_PROBE_DELTA_CHI2_TABLE.csv").exists()
print("[2/8] LATEST-81 profile probe parent imported but not promoted: PASS")

rt = contract["runtime_contract_v1"]
assert rt["sampled_parameter_set"] == EXPECTED_PARAMS
assert rt["not_sampled_v1"] == ["tau", "mnu", "nnu"]
assert rt["version_pins"] == {"Cobaya": "3.6.2", "CAMB": "1.6.6"}
print("[3/8] five-parameter runtime contract and version pins: PASS")

rows = list(csv.DictReader((ROOT / "tables" / "PROFILE_RUN_GRID.csv").open()))
assert len(rows) == 12
assert {(r["dataset"], r["model"]) for r in rows} == {(d, m) for d in EXPECTED_DATASETS for m in EXPECTED_MODELS}
assert all(r["sampled_parameter_set"].split(";") == EXPECTED_PARAMS for r in rows)
print("[4/8] 4x3 profile run grid complete: PASS")

for r in rows:
    outer = [x for x in r["outer_profile_coordinates"].split(";") if x]
    if r["model"] == "free_w0wa":
        assert outer == ["w0", "wa"]
    else:
        assert outer == []
print("[5/8] free-w0wa outer-profile coordinates isolated from sampled parameter set: PASS")

promoted = contract["exports_promoted"]
assert promoted["Export_dark_profile_likelihood_lane_admission_contract"] == 1
assert promoted["Export_dark_profile_likelihood_full_scan_format_locked"] == 1
assert promoted["Export_dark_profile_likelihood_probe_supersession_declared"] == 1
print("[6/8] contract-only export flags promoted: PASS")

non = contract["exports_preserved_non_claims"]
for k in [
    "Export_dark_profile_likelihood_P",
    "Export_dark_RouteC_MCMC_posterior_P",
    "Export_dark_MCMC_full_posterior_P",
    "Export_dark_robust_empirical_P",
    "Export_dark_profile_probe_as_full_scan_P",
    "Export_dark_profile_best_as_posterior_MAP",
]:
    assert non[k] == 0, k
print("[7/8] empirical/result non-claims preserved: PASS")

for rel in [
    "templates/PROFILE_RESULT_INTAKE_TEMPLATE.json",
    "templates/PROFILE_ADJUDICATION_TEMPLATE.json",
    "schemas/profile_lane_admission.schema.json",
    "docs/RUNNER_SPEC.md",
    "docs/PROFILE_VS_MCMC_POLICY.md",
    "docs/CONTINUOUS_SCAN_REQUIREMENTS.md",
]:
    assert (ROOT / rel).exists(), rel
print("[8/8] templates, schema, and docs present: PASS")
print(MARKER)
'''
    write(PACK / "scripts" / "check_dark_profile_likelihood_lane_admission.py", verifier)
    (PACK / "scripts" / "check_dark_profile_likelihood_lane_admission.py").chmod(0o755)

    print(f"Built {PACK}")
    print(MARKER if all(c["passed"] for c in checks) else "FAIL")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
