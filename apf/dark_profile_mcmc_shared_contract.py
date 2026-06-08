"""Shared runtime contract for APF dark-sector profile and MCMC lanes.

This is a contract/format-lock layer only. It freezes the common Route-C APF2
runtime and evidence contract so profile-likelihood and MCMC posterior results
land under the same model, data, runtime, and no-smuggling definitions.

Top marker: INTERFACE_DARK_PROFILE_MCMC_SHARED_CONTRACT_PASS
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

VERSION = "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1"
MARKER = "INTERFACE_DARK_PROFILE_MCMC_SHARED_CONTRACT_PASS"
BUNDLE_DIRNAME = "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44"
PROFILE_PROBE_PACK = "APF_DARK_SECTOR_ROUTE_C_PROFILE_PROBE_ALL_DATASETS_v1"
MCMC_LAUNCH_PACK = "APF_DARK_SECTOR_ROUTE_C_MCMC_POSTERIOR_LAUNCH_v1"
PARAMETER_SET_V1 = ("H0", "ombh2", "omch2", "logA", "ns")
NOT_SAMPLED_V1 = ("tau", "mnu", "nnu")
DATASETS = ("desi_cmb_native", "PantheonPlus", "Union3", "DESY5")
MODELS = ("APF2_fixed_w2", "free_w0wa", "LCDM")
VERSION_PINS = {"Cobaya": "3.6.2", "CAMB": "1.6.6"}
NON_CLAIM_FLAGS = {
    "Export_dark_profile_likelihood_P": 0,
    "Export_dark_MCMC_full_posterior_P": 0,
    "Export_dark_robust_empirical_P": 0,
    "Export_dark_APF2_full_shape_likelihood_P": 0,
    "Export_collaboration_NERSC_reproduction": 0,
}
CONTRACT_FLAGS = {
    "Export_dark_profile_mcmc_shared_runtime_contract": 1,
    "Export_dark_profile_mcmc_format_locked": 1,
}


@dataclass(frozen=True)
class SourcePackStatus:
    name: str
    path: str
    found: bool
    sha256_closure_statement: str | None


@dataclass(frozen=True)
class RuntimeContract:
    pack: str
    marker: str
    type: str
    objective: str
    source_packs: Tuple[SourcePackStatus, ...]
    parameter_set_v1: Tuple[str, ...]
    not_sampled_v1: Tuple[str, ...]
    camb_defaults: Mapping[str, Any]
    lockstep_rule: str
    version_pins: Mapping[str, str]
    version_specific_caveats: Tuple[str, ...]
    apf2_injection: Mapping[str, Any]
    datasets: Tuple[str, ...]
    models: Tuple[str, ...]
    grid_cells: int
    lane_linkage_points: Tuple[str, ...]
    latest82_caveat: str
    robustness_matrix: Tuple[Mapping[str, str], ...]
    promotion_flags: Mapping[str, int]
    artifact_order: Tuple[str, ...]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["source_packs"] = [asdict(x) for x in self.source_packs]
        return d


def _root(root: str | Path | None = None) -> Path:
    return Path(root) if root is not None else ROOT


def bundle_root(root: str | Path | None = None) -> Path:
    return _root(root) / BUNDLE_DIRNAME


def default_pack_dir(root: str | Path | None = None) -> Path:
    return bundle_root(root) / VERSION


def _sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_pack_status(root: str | Path | None = None) -> Tuple[SourcePackStatus, ...]:
    broot = bundle_root(root)
    out = []
    for name in (PROFILE_PROBE_PACK, MCMC_LAUNCH_PACK):
        p = broot / name
        closure = p / "results" / "CLOSURE_STATEMENT.json"
        out.append(SourcePackStatus(name, str(p), p.exists(), _sha256(closure)))
    return tuple(out)


def robustness_matrix_rows() -> Tuple[Mapping[str, str], ...]:
    return (
        {"row": "R1", "gate": "Cross-SN Route-C APF2 exact/hardened support", "status": "closed_supportive", "required_for": "context", "notes": "Supports APF2; not enough for robust empirical P alone."},
        {"row": "R2", "gate": "Profile likelihood full continuous scan", "status": "open", "required_for": "Export_dark_profile_likelihood_P", "notes": "Supersedes LATEST-81 probe-grade 3x3 grid."},
        {"row": "R3", "gate": "MCMC full posterior 12-cell grid", "status": "running_open", "required_for": "Export_dark_MCMC_full_posterior_P", "notes": "LATEST-82 infrastructure active; individual cell results must ingest under this contract."},
        {"row": "R4", "gate": "DESI full-shape exact runtime / Gate 3", "status": "env_blocked", "required_for": "robust_empirical_scope_decision", "notes": "Blocked by DESI internal bindings; future robust-P adjudication must resolve or explicitly scope."},
        {"row": "R5", "gate": "Full-growth likelihood / Gate 4", "status": "partial", "required_for": "robust_empirical_scope_decision", "notes": "Covariance/fiducial/AP/full-growth stack remains partial."},
        {"row": "R6", "gate": "Collaboration/NERSC reproduction", "status": "external", "required_for": "external_reproduction_flag", "notes": "Tracked separately; not a hidden indefinite blocker for internal format-lock closure."},
    )


def build_contract(root: str | Path | None = None) -> RuntimeContract:
    flags: Dict[str, int] = {}
    flags.update(CONTRACT_FLAGS)
    flags.update(NON_CLAIM_FLAGS)
    return RuntimeContract(
        pack=VERSION,
        marker=MARKER,
        type="shared_runtime_contract_not_result_closeout",
        objective="Freeze the shared APF2 Route-C model, runtime, dataset, likelihood, evidence, and promotion contract for parallel profile-likelihood and MCMC posterior lanes.",
        source_packs=source_pack_status(root),
        parameter_set_v1=PARAMETER_SET_V1,
        not_sampled_v1=NOT_SAMPLED_V1,
        camb_defaults={"mnu": 0.06, "N_eff": 3.046, "tau": "handled by CAMB reionization default"},
        lockstep_rule="If tau/mnu/nnu are added through a custom Cobaya theory wrapper in one lane, both profile and MCMC lanes must move to v2 together.",
        version_pins=dict(VERSION_PINS),
        version_specific_caveats=(
            "Cobaya 3.6.2 / CAMB 1.6.6 rejects tau/mnu/nnu in params when extra_args is empty.",
            "use_tabulated_w via extra_args silently produces -inf logposts in the current runtime stack.",
            "num_massive_neutrinos is rejected in params for the current consumer graph.",
            "dark_energy_model is rejected in the current extra_args path.",
        ),
        apf2_injection={
            "method": "runtime monkeypatch",
            "targets": ["camb.CAMBparams.__init__", "camb.CAMBparams.set_classes"],
            "forbidden_v1_runtime_paths": [
                "use_tabulated_w via extra_args",
                "dark_energy_model extra_args path",
                "num_massive_neutrinos in params",
                "tau/mnu/nnu in params when extra_args is empty",
            ],
            "reason": "Monkeypatch path is smoke-validated in the current G5/G6/MCMC-v1 route; tabulated-w extra_args is unstable in the pinned stack.",
        },
        datasets=DATASETS,
        models=MODELS,
        grid_cells=len(DATASETS) * len(MODELS),
        lane_linkage_points=(
            "same frozen APF2 w2 table/checksum",
            "same likelihood stack and version pins",
            "same dataset manifests and SN-compilation handling",
            "same forbidden-input/no-smuggling ledger",
            "same 5-parameter v1 sampling contract",
            "same APF2 injection mechanism",
        ),
        latest82_caveat="Profile-best and marginal posterior MAP may differ substantially at numerically similar chi-square minima; adjudication must compare the statistic appropriate to the claim being made.",
        robustness_matrix=robustness_matrix_rows(),
        promotion_flags=flags,
        artifact_order=(
            VERSION,
            "APF_DARK_MCMC_CELL_RESULT_v1_or_equivalent when cell artifacts finish",
            "APF_DARK_PROFILE_LIKELIHOOD_FULL_SCAN_v1 when continuous profile scan artifacts finish",
            "APF_DARK_EMPIRICAL_POSTERIOR_ADJUDICATION_v1 only after real profile and MCMC artifacts are present",
        ),
    )


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(fieldnames))
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def _read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _readme(contract: RuntimeContract) -> str:
    return f"""# {VERSION}

This pack freezes the shared dark-sector APF2 Route-C runtime/evidence contract for profile likelihood and MCMC posterior lanes.

It is **not** a result closeout. It does not ingest posterior chains, run a continuous profile scan, or promote dark robust empirical P.

## Marker

```text
{MARKER}
```

## Source packs

- `{PROFILE_PROBE_PACK}` — LATEST-81 profile-probe v0.
- `{MCMC_LAUNCH_PACK}` — LATEST-82 MCMC launch/intake infrastructure.

## Frozen v1 model

Both lanes use the same sampled parameters:

```text
{', '.join(PARAMETER_SET_V1)}
```

`tau`, `mnu`, and `nnu` are not sampled in v1. If a later custom theory wrapper adds them, both lanes move to v2 together.

## Runtime pinning

```text
Cobaya = 3.6.2
CAMB   = 1.6.6
```

APF2 is injected through the runtime monkeypatch path on `camb.CAMBparams.__init__` and `camb.CAMBparams.set_classes`. The v1 contract forbids the `use_tabulated_w` / `extra_args` path.

## Empirical non-claims preserved

- `Export_dark_profile_likelihood_P = 0`
- `Export_dark_MCMC_full_posterior_P = 0`
- `Export_dark_robust_empirical_P = 0`
- `Export_dark_APF2_full_shape_likelihood_P = 0`
- `Export_collaboration_NERSC_reproduction = 0`
"""


def _pack_verifier_text() -> str:
    return '''#!/usr/bin/env python3
"""Standalone verifier for APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1."""
from pathlib import Path
import csv
import json
ROOT = Path(__file__).resolve().parents[1]
contract = json.loads((ROOT / "results" / "SHARED_RUNTIME_CONTRACT.json").read_text(encoding="utf-8"))
errors = []
def expect(cond, msg):
    if not cond:
        errors.append(msg)
expect(contract.get("parameter_set_v1") == ["H0", "ombh2", "omch2", "logA", "ns"], "5-param set mismatch")
expect(contract.get("not_sampled_v1") == ["tau", "mnu", "nnu"], "not-sampled list mismatch")
expect(contract.get("version_pins", {}).get("Cobaya") == "3.6.2", "Cobaya pin missing")
expect(contract.get("version_pins", {}).get("CAMB") == "1.6.6", "CAMB pin missing")
expect(contract.get("apf2_injection", {}).get("method") == "runtime monkeypatch", "runtime monkeypatch missing")
expect("use_tabulated_w via extra_args" in set(contract.get("apf2_injection", {}).get("forbidden_v1_runtime_paths", [])), "tabulated-w path not forbidden")
flags = contract.get("promotion_flags", {})
expect(flags.get("Export_dark_profile_mcmc_shared_runtime_contract") == 1, "contract flag missing")
for flag in ["Export_dark_profile_likelihood_P", "Export_dark_MCMC_full_posterior_P", "Export_dark_robust_empirical_P", "Export_dark_APF2_full_shape_likelihood_P", "Export_collaboration_NERSC_reproduction"]:
    expect(flags.get(flag) == 0, f"{flag} must remain 0")
with (ROOT / "tables" / "ROBUSTNESS_MATRIX.csv").open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
expect({r.get("row") for r in rows} == {"R1", "R2", "R3", "R4", "R5", "R6"}, "robustness matrix R1-R6 missing")
expect(all((ROOT / "templates" / name).exists() for name in ["PROFILE_RESULT_TEMPLATE.json", "MCMC_RESULT_TEMPLATE.json", "ADJUDICATION_RESULT_TEMPLATE.json"]), "templates missing")
if errors:
    print("INTERFACE_DARK_PROFILE_MCMC_SHARED_CONTRACT_FAIL")
    for e in errors:
        print("ERROR:", e)
    raise SystemExit(1)
print("INTERFACE_DARK_PROFILE_MCMC_SHARED_CONTRACT_PASS")
'''


def _schema(kind: str = "shared_runtime_contract") -> Dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"APF Dark {kind}",
        "type": "object",
        "required": ["pack", "parameter_set_v1", "version_pins", "apf2_injection", "datasets", "models", "promotion_flags"] if kind == "shared_runtime_contract" else ["artifact_type", "contract_pack", "dataset", "model", "parameter_set", "promotion_flags"],
    }


def _templates() -> Dict[str, Mapping[str, Any]]:
    return {
        "PROFILE_RESULT_TEMPLATE.json": {"artifact_type": "profile_likelihood_result", "contract_pack": VERSION, "dataset": "", "model": "", "parameter_set": list(PARAMETER_SET_V1), "apf2_table_sha256": "", "likelihood_stack_sha256": "", "profile_method": "continuous_scan_with_nuisance_profiling", "delta_chi2_table": [], "profile_bestfit": {}, "promotion_flags": {"Export_dark_profile_likelihood_P": 0, "Export_dark_robust_empirical_P": 0}, "forbidden_inputs_checked": True},
        "MCMC_RESULT_TEMPLATE.json": {"artifact_type": "mcmc_posterior_result", "contract_pack": VERSION, "dataset": "", "model": "", "parameter_set": list(PARAMETER_SET_V1), "chains": [], "rhat": {}, "ess": {}, "marginal_map": {}, "posterior_predictive": {}, "promotion_flags": {"Export_dark_MCMC_full_posterior_P": 0, "Export_dark_robust_empirical_P": 0}, "forbidden_inputs_checked": True},
        "ADJUDICATION_RESULT_TEMPLATE.json": {"artifact_type": "profile_mcmc_adjudication_result", "contract_pack": VERSION, "profile_result_refs": [], "mcmc_result_refs": [], "robustness_matrix_ref": "tables/ROBUSTNESS_MATRIX.csv", "adjudication_rules": ["Do not use profile-best as posterior-mass proxy.", "Do not promote robust P unless profile, MCMC, and named robustness scope all pass.", "If parameter-set v2 is introduced in one lane, both lanes update in lockstep."], "promotion_flags": dict(NON_CLAIM_FLAGS)},
    }


def export_contract_pack(out_dir: str | Path | None = None, root: str | Path | None = None) -> Path:
    contract = build_contract(root)
    out = Path(out_dir) if out_dir is not None else default_pack_dir(root)
    out.mkdir(parents=True, exist_ok=True)
    cdict = contract.to_dict()
    closure = {"pack": VERSION, "marker": MARKER, "verdict": "CONTRACT_LOCKED_NO_EMPIRICAL_PROMOTION", "summary": contract.objective, "source_packs": cdict["source_packs"], "promotion_flags": dict(contract.promotion_flags), "preserved_non_claims": dict(NON_CLAIM_FLAGS), "next_artifacts": list(contract.artifact_order[1:])}
    _write_json(out / "results" / "SHARED_RUNTIME_CONTRACT.json", cdict)
    _write_json(out / "results" / "CLOSURE_STATEMENT.json", closure)
    (out / "README.md").write_text(_readme(contract), encoding="utf-8")
    docs = out / "docs"; docs.mkdir(exist_ok=True)
    (docs / "CONTRACT_NOTE.md").write_text("# Contract Note\n\nProfile likelihood and MCMC are parallel evidence lanes under one frozen model/data/runtime contract.\n", encoding="utf-8")
    (docs / "LATEST82_PROFILE_MCMC_CAVEAT.md").write_text("# LATEST-82 Profile/MCMC Caveat\n\nProfile-best and marginal posterior MAP may differ substantially at numerically similar chi-square minima. Profile-best can initialize MCMC, but is not evidence for posterior mass concentration.\n", encoding="utf-8")
    (docs / "HONEST_NON_CLAIMS.md").write_text("# Honest Non-Claims\n\nThis pack does not promote profile likelihood P, MCMC full posterior P, robust empirical P, full-shape likelihood P, or NERSC reproduction.\n", encoding="utf-8")
    (docs / "DATA_DISCIPLINE.md").write_text("# Data Discipline\n\nBoth lanes must share APF2 table/checksum, likelihood stack, dataset manifests, five-parameter v1 model definition, no-smuggling ledger, and APF2 injection mechanism.\n", encoding="utf-8")
    (docs / "PROMOTION_LADDER.md").write_text("# Promotion Ladder\n\nContract flags are promoted. Profile, MCMC, robust empirical, full-shape, and external reproduction flags remain zero until real result artifacts pass their own gates.\n", encoding="utf-8")
    (docs / "RESULT_INGEST_PROTOCOL.md").write_text("# Result Ingest Protocol\n\nFuture result packs must declare this contract, exact parameter set, dataset/model cell, checksums, no-smuggling guard results, and promotion flags with unrelated empirical flags preserved at zero.\n", encoding="utf-8")
    _write_csv(out / "tables" / "MODEL_PARAMETER_SET.csv", [{"parameter": p, "lane": "profile,mcmc", "status": "sampled_v1", "notes": ""} for p in PARAMETER_SET_V1] + [{"parameter": p, "lane": "profile,mcmc", "status": "not_sampled_v1", "notes": "CAMB default / v2 only in lane lockstep"} for p in NOT_SAMPLED_V1])
    _write_csv(out / "tables" / "DATASET_GRID.csv", [{"dataset": ds, "model": m, "cell": i + 1, "cell_status": "running_or_queued", "notes": "LATEST-82 12-cell grid; no result artifact ingested"} for i, (ds, m) in enumerate((ds, m) for ds in DATASETS for m in MODELS)])
    _write_csv(out / "tables" / "LANE_LINKAGE_POINTS.csv", [{"linkage_point": x, "required": "yes"} for x in contract.lane_linkage_points])
    _write_csv(out / "tables" / "ROBUSTNESS_MATRIX.csv", list(contract.robustness_matrix), ["row", "gate", "status", "required_for", "notes"])
    _write_csv(out / "tables" / "PROMOTION_FLAGS.csv", [{"flag": k, "value": v, "reason": "contract flag" if v == 1 else "preserved non-claim; no result artifact ingested"} for k, v in contract.promotion_flags.items()], ["flag", "value", "reason"])
    _write_csv(out / "tables" / "FORBIDDEN_INPUT_LEDGER.csv", [
        {"forbidden_input": "posterior output used as profile input", "scope": "all", "reason": "would smuggle posterior output into point-likelihood lane"},
        {"forbidden_input": "profile best-fit used as posterior target", "scope": "all", "reason": "profile-best may not match marginal MAP"},
        {"forbidden_input": "observed APF2 acceptance used to tune w2 table", "scope": "all", "reason": "APF2 table must be frozen before likelihood evaluation"},
        {"forbidden_input": "use_tabulated_w extra_args path", "scope": "v1 runtime", "reason": "known unstable/silent -inf logpost path in pinned stack"},
        {"forbidden_input": "different parameter sets across lanes", "scope": "all", "reason": "breaks comparability"},
    ], ["forbidden_input", "scope", "reason"])
    _write_json(out / "schemas" / "shared_runtime_contract.schema.json", _schema("shared_runtime_contract"))
    _write_json(out / "schemas" / "profile_result.schema.json", _schema("profile_likelihood_result"))
    _write_json(out / "schemas" / "mcmc_result.schema.json", _schema("mcmc_posterior_result"))
    _write_json(out / "schemas" / "adjudication_result.schema.json", _schema("profile_mcmc_adjudication_result"))
    for name, payload in _templates().items():
        _write_json(out / "templates" / name, payload)
    scripts = out / "scripts"; scripts.mkdir(exist_ok=True)
    (scripts / "check_dark_profile_mcmc_shared_contract.py").write_text(_pack_verifier_text(), encoding="utf-8")
    _write_json(out / "results" / "CHECK_RESULTS.json", run_contract_checks(out))
    return out


def run_contract_checks(pack_dir: str | Path | None = None) -> Dict[str, Any]:
    out = Path(pack_dir) if pack_dir is not None else default_pack_dir()
    errors: List[str] = []
    contract_path = out / "results" / "SHARED_RUNTIME_CONTRACT.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8")) if contract_path.exists() else {}
    def expect(cond: bool, msg: str) -> None:
        if not cond:
            errors.append(msg)
    flags = contract.get("promotion_flags", {})
    expect(contract.get("parameter_set_v1") == list(PARAMETER_SET_V1), "parameter set must be exactly 5-param v1")
    expect(contract.get("not_sampled_v1") == list(NOT_SAMPLED_V1), "not-sampled set mismatch")
    expect(contract.get("version_pins") == dict(VERSION_PINS), "version pins mismatch")
    expect(contract.get("apf2_injection", {}).get("method") == "runtime monkeypatch", "runtime monkeypatch missing")
    expect("use_tabulated_w via extra_args" in set(contract.get("apf2_injection", {}).get("forbidden_v1_runtime_paths", [])), "tabulated-w extra_args path must be forbidden")
    expect(flags.get("Export_dark_profile_mcmc_shared_runtime_contract") == 1, "contract flag not set")
    for k in NON_CLAIM_FLAGS:
        expect(flags.get(k) == 0, f"{k} must remain zero")
    source = contract.get("source_packs", [])
    expect(len(source) == 2 and all(row.get("found") for row in source), "LATEST-81/LATEST-82 source packs must be present")
    rows = _read_csv(out / "tables" / "ROBUSTNESS_MATRIX.csv")
    expect({r.get("row") for r in rows} == {"R1", "R2", "R3", "R4", "R5", "R6"}, "robustness rows R1-R6 missing")
    templates_ok = all((out / "templates" / x).exists() for x in ["PROFILE_RESULT_TEMPLATE.json", "MCMC_RESULT_TEMPLATE.json", "ADJUDICATION_RESULT_TEMPLATE.json"])
    expect(templates_ok, "result templates missing")
    return {"marker": MARKER if not errors else "INTERFACE_DARK_PROFILE_MCMC_SHARED_CONTRACT_FAIL", "passed": not errors, "errors": errors, "checks": {"parameter_set_5_param_v1": contract.get("parameter_set_v1") == list(PARAMETER_SET_V1), "version_pins_present": contract.get("version_pins") == dict(VERSION_PINS), "runtime_monkeypatch_declared": contract.get("apf2_injection", {}).get("method") == "runtime monkeypatch", "no_empirical_flags_promoted": all(flags.get(k) == 0 for k in NON_CLAIM_FLAGS), "source_packs_present": len(source) == 2 and all(row.get("found") for row in source), "robustness_matrix_named": len(rows) == 6}}


def check_T_dark_profile_mcmc_shared_runtime_contract_P() -> Dict[str, Any]:
    contract = build_contract()
    flags = dict(contract.promotion_flags)
    passed = (contract.parameter_set_v1 == PARAMETER_SET_V1 and contract.version_pins == VERSION_PINS and flags["Export_dark_profile_mcmc_shared_runtime_contract"] == 1 and all(flags[k] == 0 for k in NON_CLAIM_FLAGS) and len(contract.robustness_matrix) == 6)
    return {"name": "T_dark_profile_mcmc_shared_runtime_contract", "passed": passed, "status": "P_contract" if passed else "FAIL", "tier": 4, "epistemic": "contract-only-no-empirical-promotion", "key_result": MARKER if passed else "contract_failed"}




def register(registry):
    """Register this module's tier-4 contract check with the bank."""
    registry[check_T_dark_profile_mcmc_shared_runtime_contract_P.__name__] = (
        check_T_dark_profile_mcmc_shared_runtime_contract_P
    )

if __name__ == "__main__":
    out = export_contract_pack()
    print(f"{MARKER}: {out}")
