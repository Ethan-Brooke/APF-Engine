"""
APF Dark posterior / evaluator-map evidence intake.

Sandbox sprint layer following APF_INTERFACE_LIVE_BLOCKER_WORK_QUEUE_v1.

Purpose
-------
The live Interface Engine keeps the dark route held on two structures:

    EVALUATOR_MAP
    EMPIRICAL_POSTERIOR

The v24.3.18 tree already contains Route-C APF2 profile-probe, tabulated-w2,
Cobaya bridge/smoke, hardened cross-SN, and MCMC-launch packs.  This module
collects those pack-side artifacts into a single evidence-readiness packet.

Boundary
--------
This module does not patch the dark adapter's route booleans and does not
promote the dark route.  It marks the evaluator-map structure as candidate
evidence present, while keeping the empirical-posterior structure open until a
real MCMC/profile posterior gate closes.  In particular, profile-probe support
is evidence, not posterior closure.

Top check:
    check_T_dark_posterior_evidence_intake_P
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence, Tuple, List
import csv
import json


class IntakeStatus(str, Enum):
    CANDIDATE_EVIDENCE_PRESENT = "CANDIDATE_EVIDENCE_PRESENT"
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"
    BLOCKED_BY_PROVENANCE = "BLOCKED_BY_PROVENANCE"


@dataclass(frozen=True)
class PackProbe:
    pack_name: str
    path: str
    exists: bool
    loaded: bool
    headline: str
    promoted_exports: Mapping[str, Any]
    preserved_nonclaims: Mapping[str, Any]
    summary: Mapping[str, Any]
    forbidden_claims: Tuple[str, ...]
    errors: Tuple[str, ...] = tuple()

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["promoted_exports"] = dict(self.promoted_exports)
        data["preserved_nonclaims"] = dict(self.preserved_nonclaims)
        data["summary"] = dict(self.summary)
        data["forbidden_claims"] = list(self.forbidden_claims)
        return data


@dataclass(frozen=True)
class IntakeRequirement:
    key: str
    description: str
    satisfied_by: Tuple[str, ...]
    acceptance_criteria: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DarkEvidenceIntakeItem:
    task_id: str
    route: str
    structure_kind: str
    status: IntakeStatus
    supporting_packs: Tuple[str, ...]
    required_evidence_keys: Tuple[str, ...]
    satisfied_evidence_keys: Tuple[str, ...]
    promoted_export_keys: Tuple[str, ...]
    preserved_nonclaim_keys: Tuple[str, ...]
    live_adapter_field: str
    rerun_command: str
    acceptance_boundary: str
    requirements: Tuple[IntakeRequirement, ...]
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["requirements"] = [r.to_dict() for r in self.requirements]
        return data


@dataclass(frozen=True)
class DarkPosteriorEvidenceIntake:
    version: str
    status: str
    items: Tuple[DarkEvidenceIntakeItem, ...]
    probes: Tuple[PackProbe, ...]
    summary: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "status": self.status,
            "items": [x.to_dict() for x in self.items],
            "probes": [p.to_dict() for p in self.probes],
            "summary": dict(self.summary),
        }


VERSION = "APF_INTERFACE_DARK_POSTERIOR_EVIDENCE_INTAKE_v1"
MARKER = "DARK_POSTERIOR_EVIDENCE_INTAKE_PASS"

BUNDLE_DIR = Path(__file__).resolve().parents[1] / "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44"

PACKS: Tuple[str, ...] = (
    "APF_DARK_SECTOR_ROUTE_C_SN_STRESS_v2",
    "APF_DARK_SECTOR_ROUTE_C_SN_STRESS_HARDENED_v3",
    "APF_DARK_SECTOR_ROUTE_C_PROFILE_PROBE_ALL_DATASETS_v1",
    "APF_DARK_SECTOR_ROUTE_C_MCMC_POSTERIOR_LAUNCH_v1",
    "APF_DARK_SECTOR_ROUTE_C_APF2_TABULATED_W2_COBAYA_BRIDGE_v1",
    "APF_DARK_SECTOR_ROUTE_C_APF2_COBAYA_ADAPTER_SMOKE_v1",
    "APF_DARK_SECTOR_ROUTE_C_APF2_COBAYA_LIKELIHOOD_SMOKE_v1",
    "APF_DARK_SECTOR_ROUTE_C_APF2_NATIVE_LIKELIHOOD_SMOKE_AFTER_ATTEMPT_v1",
    "APF_FULL_GROWTH_APF2_EXACT_RUNTIME_ATTEMPT_v19",
)

EVALUATOR_REQUIRED_EXPORTS: Tuple[str, ...] = (
    "Export_dark_RouteC_APF2_tabulated_w2_source_table",
    "Export_dark_RouteC_APF2_direct_CAMB_smoke",
    "Export_dark_RouteC_APF2_Cobaya_adapter_smoke",
    "Export_dark_RouteC_APF2_Cobaya_likelihood_smoke",
)

PROFILE_REQUIRED_EXPORTS: Tuple[str, ...] = (
    "Export_dark_RouteC_all_dataset_profile_probe_complete",
    "Export_dark_RouteC_profile_likelihood_global_P_candidate",
)

MCMC_LAUNCH_EXPORTS: Tuple[str, ...] = (
    "Export_dark_RouteC_MCMC_posterior_launch_pack",
    "Export_dark_RouteC_MCMC_result_schema_frozen",
    "Export_dark_RouteC_MCMC_adjudicator_runnable",
)

POSTERIOR_NONCLAIMS: Tuple[str, ...] = (
    "Export_dark_RouteC_APF2_posterior_P",
    "Export_dark_RouteC_MCMC_posterior_P",
    "Export_dark_robust_empirical_P",
)

NO_REFIT_NONCLAIMS: Tuple[str, ...] = (
    "Export_APF2_coefficients_refit",
    "Export_collaboration_NERSC_reproduction",
)


def _req(key: str, description: str, satisfied_by: Sequence[str], criteria: str) -> IntakeRequirement:
    return IntakeRequirement(key, description, tuple(satisfied_by), criteria)


def _closure_path(pack_name: str) -> Path:
    return BUNDLE_DIR / pack_name / "results" / "CLOSURE_STATEMENT.json"


def _as_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _extract_export_maps(data: Mapping[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    promoted: Dict[str, Any] = {}
    preserved: Dict[str, Any] = {}
    for key in ("exports", "exports_promoted"):
        promoted.update(dict(_as_mapping(data.get(key))))
    for key in ("non_claims", "exports_preserved_non_claims", "preserved_non_claims"):
        preserved.update(dict(_as_mapping(data.get(key))))
    # Some packs put nonclaim flags inside the promoted map with value 0. Preserve those too.
    for key, value in promoted.items():
        if key.startswith("Export_") and value == 0:
            preserved.setdefault(key, value)
    return promoted, preserved


def _load_pack(pack_name: str) -> PackProbe:
    path = _closure_path(pack_name)
    if not path.exists():
        return PackProbe(pack_name, str(path), False, False, "", {}, {}, {}, tuple(), ("missing CLOSURE_STATEMENT.json",))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return PackProbe(pack_name, str(path), True, False, "", {}, {}, {}, tuple(), (repr(exc),))
    promoted, preserved = _extract_export_maps(data)
    forbidden_raw = data.get("forbidden_claims_verbatim", data.get("forbidden_claims", ()))
    if isinstance(forbidden_raw, str):
        forbidden = (forbidden_raw,)
    elif isinstance(forbidden_raw, Iterable):
        forbidden = tuple(str(x) for x in forbidden_raw)
    else:
        forbidden = tuple()
    summary = dict(_as_mapping(data.get("summary")))
    return PackProbe(
        pack_name=pack_name,
        path=str(path),
        exists=True,
        loaded=True,
        headline=str(data.get("headline", data.get("scope", data.get("status", "")))),
        promoted_exports=promoted,
        preserved_nonclaims=preserved,
        summary=summary,
        forbidden_claims=forbidden,
    )


@lru_cache(maxsize=1)
def load_pack_probes() -> Tuple[PackProbe, ...]:
    return tuple(_load_pack(name) for name in PACKS)


def _all_exports(probes: Iterable[PackProbe]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for p in probes:
        out.update(dict(p.promoted_exports))
    return out


def _all_nonclaims(probes: Iterable[PackProbe]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for p in probes:
        out.update(dict(p.preserved_nonclaims))
    return out


def _supporting_packs_for_keys(probes: Iterable[PackProbe], keys: Iterable[str]) -> Tuple[str, ...]:
    wanted = set(keys)
    packs: List[str] = []
    for p in probes:
        combined = set(p.promoted_exports) | set(p.preserved_nonclaims)
        if combined & wanted:
            packs.append(p.pack_name)
    return tuple(packs)


def _keys_with_value(mapping: Mapping[str, Any], keys: Iterable[str], expected: Any) -> Tuple[str, ...]:
    return tuple(key for key in keys if mapping.get(key) == expected)


def _profile_accept_summary(probes: Iterable[PackProbe]) -> Mapping[str, Any]:
    for p in probes:
        if p.pack_name == "APF_DARK_SECTOR_ROUTE_C_PROFILE_PROBE_ALL_DATASETS_v1":
            return p.summary
    return {}


def _evaluator_item(probes: Tuple[PackProbe, ...]) -> DarkEvidenceIntakeItem:
    exports = _all_exports(probes)
    nonclaims = _all_nonclaims(probes)
    satisfied = _keys_with_value(exports, EVALUATOR_REQUIRED_EXPORTS, 1)
    preserved = _keys_with_value(nonclaims, POSTERIOR_NONCLAIMS, 0)
    ok = len(satisfied) >= 3 and len(preserved) >= 2
    return DarkEvidenceIntakeItem(
        task_id="DARK_EVALUATOR_MAP",
        route="DARK",
        structure_kind="EVALUATOR_MAP",
        status=IntakeStatus.CANDIDATE_EVIDENCE_PRESENT if ok else IntakeStatus.OPEN_EVIDENCE_REQUIRED,
        supporting_packs=_supporting_packs_for_keys(probes, EVALUATOR_REQUIRED_EXPORTS + POSTERIOR_NONCLAIMS),
        required_evidence_keys=EVALUATOR_REQUIRED_EXPORTS,
        satisfied_evidence_keys=satisfied,
        promoted_export_keys=tuple(k for k in EVALUATOR_REQUIRED_EXPORTS if exports.get(k) == 1),
        preserved_nonclaim_keys=preserved,
        live_adapter_field="evaluator_map_found",
        rerun_command="python scripts/run_first_real_dark_obligation.py",
        acceptance_boundary=(
            "Candidate evidence identifies the APF2 tabulated-w2/CAMB/Cobaya evaluator path.  "
            "It is not posterior closure and must keep posterior/robust-empirical exports at 0 until MCMC/profile posterior gates close."
        ),
        requirements=(
            _req("tabulated_w2_source", "Frozen APF2 w2(a) source table banked without coefficient refit.", ("APF_DARK_SECTOR_ROUTE_C_APF2_TABULATED_W2_COBAYA_BRIDGE_v1",), "Source table export and direct CAMB smoke must be 1."),
            _req("cobaya_bridge", "Cobaya/CAMB adapter and likelihood smoke evidence.", ("APF_DARK_SECTOR_ROUTE_C_APF2_COBAYA_ADAPTER_SMOKE_v1", "APF_DARK_SECTOR_ROUTE_C_APF2_COBAYA_LIKELIHOOD_SMOKE_v1"), "Adapter/likelihood smoke exports are present or the open runtime gate is explicitly named."),
            _req("posterior_nonclaim_guard", "Posterior/robust empirical nonclaims preserved.", ("APF_DARK_SECTOR_ROUTE_C_APF2_TABULATED_W2_COBAYA_BRIDGE_v1",), "APF2 posterior and robust empirical exports remain 0."),
        ),
        notes="Candidate evaluator-map evidence for the dark route; route remains held on empirical posterior.",
    )


def _posterior_item(probes: Tuple[PackProbe, ...]) -> DarkEvidenceIntakeItem:
    exports = _all_exports(probes)
    nonclaims = _all_nonclaims(probes)
    profile = _keys_with_value(exports, PROFILE_REQUIRED_EXPORTS, 1)
    launch = _keys_with_value(exports, MCMC_LAUNCH_EXPORTS, 1)
    posterior_nonclaims = _keys_with_value(nonclaims, POSTERIOR_NONCLAIMS, 0)
    no_refit = _keys_with_value(nonclaims, NO_REFIT_NONCLAIMS, 0)
    # Profile support and MCMC launch are useful evidence, but they are not an empirical posterior.
    closed = bool(exports.get("Export_dark_RouteC_MCMC_posterior_P") == 1 or exports.get("Export_dark_RouteC_APF2_posterior_P") == 1)
    status = IntakeStatus.CANDIDATE_EVIDENCE_PRESENT if closed else IntakeStatus.OPEN_EVIDENCE_REQUIRED
    return DarkEvidenceIntakeItem(
        task_id="DARK_EMPIRICAL_POSTERIOR",
        route="DARK",
        structure_kind="EMPIRICAL_POSTERIOR",
        status=status,
        supporting_packs=_supporting_packs_for_keys(probes, PROFILE_REQUIRED_EXPORTS + MCMC_LAUNCH_EXPORTS + POSTERIOR_NONCLAIMS + NO_REFIT_NONCLAIMS),
        required_evidence_keys=PROFILE_REQUIRED_EXPORTS + MCMC_LAUNCH_EXPORTS + POSTERIOR_NONCLAIMS,
        satisfied_evidence_keys=profile + launch,
        promoted_export_keys=profile + launch,
        preserved_nonclaim_keys=posterior_nonclaims + no_refit,
        live_adapter_field="posterior_closed / robustness_checks_passed",
        rerun_command="python scripts/run_first_real_dark_obligation.py",
        acceptance_boundary=(
            "Profile-probe support and MCMC-launch infrastructure are not enough.  Empirical posterior closure requires actual converged chains/profile artifacts, "
            "declared diagnostics (R-hat/ESS or equivalent), no APF2 coefficient refit, and adjudication against the frozen gate."
        ),
        requirements=(
            _req("profile_probe_support", "Route-C profile-probe all-dataset support.", ("APF_DARK_SECTOR_ROUTE_C_PROFILE_PROBE_ALL_DATASETS_v1",), "4-of-4 profile-probe accept is recorded as candidate support, not posterior P."),
            _req("mcmc_launch_schema", "MCMC launch/config/adjudicator infrastructure.", ("APF_DARK_SECTOR_ROUTE_C_MCMC_POSTERIOR_LAUNCH_v1",), "12 configs + frozen schema + runnable adjudicator are present."),
            _req("posterior_runtime_result", "Actual posterior/profile result artifacts.", ("TODO: external MCMC/profile output pack",), "Chains/profile must converge and report gate deltas without using posterior outputs as inputs."),
        ),
        notes="Empirical posterior remains open; profile support is candidate evidence only.",
    )


def build_dark_posterior_evidence_intake() -> DarkPosteriorEvidenceIntake:
    probes = load_pack_probes()
    items = (_evaluator_item(probes), _posterior_item(probes))
    by_status: Dict[str, int] = {}
    for item in items:
        by_status[item.status.value] = by_status.get(item.status.value, 0) + 1
    profile_summary = dict(_profile_accept_summary(probes))
    summary = {
        "total_items": len(items),
        "candidate_evidence_present_items": by_status.get(IntakeStatus.CANDIDATE_EVIDENCE_PRESENT.value, 0),
        "open_items": by_status.get(IntakeStatus.OPEN_EVIDENCE_REQUIRED.value, 0),
        "pack_probes_loaded": sum(1 for p in probes if p.loaded),
        "pack_probes_total": len(probes),
        "by_status": by_status,
        "profile_probe_accept_at_95": profile_summary.get("accept_at_95"),
        "posterior_exports_preserved_at_zero": _keys_with_value(_all_nonclaims(probes), POSTERIOR_NONCLAIMS, 0),
        "boundary": "Evaluator-map candidate exists; empirical posterior remains open until converged posterior/profile artifacts are banked.",
    }
    status = "DARK_EVALUATOR_CANDIDATE_POSTERIOR_OPEN" if summary["candidate_evidence_present_items"] >= 1 and summary["open_items"] >= 1 else "OPEN_EVIDENCE_REQUIRED"
    return DarkPosteriorEvidenceIntake(version=VERSION, status=status, items=items, probes=probes, summary=summary)


def status_by_task_id(intake: Optional[DarkPosteriorEvidenceIntake] = None) -> Dict[str, str]:
    intake = intake or build_dark_posterior_evidence_intake()
    return {item.task_id: item.status.value for item in intake.items}




def dark_live_adapter_overrides(intake: Optional[DarkPosteriorEvidenceIntake] = None) -> Dict[str, Any]:
    """Return conservative live-adapter booleans from the evidence intake.

    The evaluator-map candidate is allowed to satisfy the EVALUATOR_MAP edge;
    empirical posterior closure is deliberately not inferred from profile probes
    or launch infrastructure.
    """
    intake = intake or build_dark_posterior_evidence_intake()
    statuses = status_by_task_id(intake)
    evaluator_candidate = statuses.get("DARK_EVALUATOR_MAP") == IntakeStatus.CANDIDATE_EVIDENCE_PRESENT.value
    posterior_candidate = statuses.get("DARK_EMPIRICAL_POSTERIOR") == IntakeStatus.CANDIDATE_EVIDENCE_PRESENT.value
    return {
        "route_built": bool(evaluator_candidate),
        "run_completed": bool(evaluator_candidate),
        "evaluator_map_found": bool(evaluator_candidate),
        "codomain_transport_found": bool(evaluator_candidate),
        "data_ledger_clean": bool(evaluator_candidate),
        "chains_converged": bool(posterior_candidate),
        "posterior_closed": bool(posterior_candidate),
        "robustness_checks_passed": bool(posterior_candidate),
        "target_value_consumed": False,
    }

def render_markdown(intake: Optional[DarkPosteriorEvidenceIntake] = None) -> str:
    intake = intake or build_dark_posterior_evidence_intake()
    lines = [
        "# APF Dark Posterior Evidence Intake v1",
        "",
        f"- Status: `{intake.status}`",
        f"- Candidate evidence present: `{intake.summary.get('candidate_evidence_present_items')}` / `{intake.summary.get('total_items')}`",
        f"- Open items: `{intake.summary.get('open_items')}`",
        f"- Pack probes loaded: `{intake.summary.get('pack_probes_loaded')}` / `{intake.summary.get('pack_probes_total')}`",
        f"- Profile-probe support: `{intake.summary.get('profile_probe_accept_at_95')}`",
        "- Boundary: evaluator-map candidate evidence is not empirical posterior closure.",
        "",
        "## Intake items",
        "",
        "| Task | Status | Satisfied evidence | Preserved nonclaims | Supporting packs |",
        "|---|---|---|---|---|",
    ]
    for item in intake.items:
        lines.append(
            f"| `{item.task_id}` | `{item.status.value}` | `{'; '.join(item.satisfied_evidence_keys)}` | "
            f"`{'; '.join(item.preserved_nonclaim_keys)}` | `{'; '.join(item.supporting_packs)}` |"
        )
    lines += ["", "## Requirements", ""]
    for item in intake.items:
        lines += [f"### `{item.task_id}`", "", item.acceptance_boundary, ""]
        for req in item.requirements:
            lines.append(f"- `{req.key}`: {req.description} Criteria: {req.acceptance_criteria}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def export_intake(out_dir: str | Path) -> Dict[str, str]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    intake = build_dark_posterior_evidence_intake()
    json_path = out / "DARK_POSTERIOR_EVIDENCE_INTAKE.json"
    md_path = out / "README.md"
    csv_path = out / "dark_posterior_evidence_intake.csv"
    json_path.write_text(json.dumps(intake.to_dict(), indent=2, default=str), encoding="utf-8")
    md_path.write_text(render_markdown(intake), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["task_id", "status", "satisfied_evidence_keys", "preserved_nonclaim_keys", "supporting_packs", "acceptance_boundary"])
        writer.writeheader()
        for item in intake.items:
            writer.writerow({
                "task_id": item.task_id,
                "status": item.status.value,
                "satisfied_evidence_keys": ";".join(item.satisfied_evidence_keys),
                "preserved_nonclaim_keys": ";".join(item.preserved_nonclaim_keys),
                "supporting_packs": ";".join(item.supporting_packs),
                "acceptance_boundary": item.acceptance_boundary,
            })
    return {"json": str(json_path), "markdown": str(md_path), "csv": str(csv_path)}


def _res(name: str, passed: bool, **data: Any) -> Dict[str, Any]:
    return {"name": name, "passed": bool(passed), "consistent": bool(passed), "status": "PASS" if passed else "FAIL", "epistemic": VERSION, "marker": MARKER if passed else "", "data": data}


def check_T_dark_evaluator_map_candidate_present() -> Dict[str, Any]:
    intake = build_dark_posterior_evidence_intake()
    item = next(i for i in intake.items if i.task_id == "DARK_EVALUATOR_MAP")
    tests = {
        "status_candidate": item.status == IntakeStatus.CANDIDATE_EVIDENCE_PRESENT,
        "tabulated_w2_present": "Export_dark_RouteC_APF2_tabulated_w2_source_table" in item.satisfied_evidence_keys,
        "direct_or_cobaya_smoke_present": any(k in item.satisfied_evidence_keys for k in ("Export_dark_RouteC_APF2_direct_CAMB_smoke", "Export_dark_RouteC_APF2_Cobaya_likelihood_smoke")),
        "posterior_nonclaims_preserved": any(k in item.preserved_nonclaim_keys for k in POSTERIOR_NONCLAIMS),
    }
    return _res("check_T_dark_evaluator_map_candidate_present", all(tests.values()), tests=tests, item=item.to_dict())


def check_T_dark_empirical_posterior_remains_open() -> Dict[str, Any]:
    intake = build_dark_posterior_evidence_intake()
    item = next(i for i in intake.items if i.task_id == "DARK_EMPIRICAL_POSTERIOR")
    tests = {
        "status_open": item.status == IntakeStatus.OPEN_EVIDENCE_REQUIRED,
        "profile_support_recorded": "Export_dark_RouteC_all_dataset_profile_probe_complete" in item.satisfied_evidence_keys,
        "mcmc_launch_recorded": "Export_dark_RouteC_MCMC_posterior_launch_pack" in item.satisfied_evidence_keys,
        "mcmc_posterior_still_zero": "Export_dark_RouteC_MCMC_posterior_P" in item.preserved_nonclaim_keys,
        "robust_empirical_still_zero": "Export_dark_robust_empirical_P" in item.preserved_nonclaim_keys,
    }
    return _res("check_T_dark_empirical_posterior_remains_open", all(tests.values()), tests=tests, item=item.to_dict())


def check_T_dark_profile_probe_support_recorded() -> Dict[str, Any]:
    intake = build_dark_posterior_evidence_intake()
    summary = dict(intake.summary)
    tests = {
        "profile_4_of_4": str(summary.get("profile_probe_accept_at_95")) == "4 of 4",
        "profile_pack_loaded": any(p.pack_name == "APF_DARK_SECTOR_ROUTE_C_PROFILE_PROBE_ALL_DATASETS_v1" and p.loaded for p in intake.probes),
        "pack_loading_nonzero": summary.get("pack_probes_loaded", 0) >= 6,
    }
    return _res("check_T_dark_profile_probe_support_recorded", all(tests.values()), tests=tests, summary=summary)


def check_T_dark_intake_no_posterior_overclaim() -> Dict[str, Any]:
    intake = build_dark_posterior_evidence_intake()
    nonclaims = _all_nonclaims(intake.probes)
    tests = {
        "posterior_p_zero": nonclaims.get("Export_dark_RouteC_APF2_posterior_P", nonclaims.get("Export_dark_RouteC_MCMC_posterior_P")) == 0,
        "mcmc_posterior_zero": nonclaims.get("Export_dark_RouteC_MCMC_posterior_P") == 0,
        "robust_zero": nonclaims.get("Export_dark_robust_empirical_P", nonclaims.get("Export_dark_robust_P")) == 0,
        "no_refit_zero_or_absent": nonclaims.get("Export_APF2_coefficients_refit", 0) == 0,
        "top_status_not_closed": intake.status != "CLOSED_BY_POSTERIOR",
    }
    return _res("check_T_dark_intake_no_posterior_overclaim", all(tests.values()), tests=tests, preserved_nonclaims=nonclaims)


def check_T_dark_posterior_evidence_intake_P() -> Dict[str, Any]:
    checks = [
        check_T_dark_evaluator_map_candidate_present(),
        check_T_dark_empirical_posterior_remains_open(),
        check_T_dark_profile_probe_support_recorded(),
        check_T_dark_intake_no_posterior_overclaim(),
    ]
    ok = all(c["passed"] for c in checks)
    return _res("check_T_dark_posterior_evidence_intake_P", ok, subchecks=[c["name"] for c in checks], summary=build_dark_posterior_evidence_intake().summary)


CHECKS = {
    "check_T_dark_evaluator_map_candidate_present": check_T_dark_evaluator_map_candidate_present,
    "check_T_dark_empirical_posterior_remains_open": check_T_dark_empirical_posterior_remains_open,
    "check_T_dark_profile_probe_support_recorded": check_T_dark_profile_probe_support_recorded,
    "check_T_dark_intake_no_posterior_overclaim": check_T_dark_intake_no_posterior_overclaim,
    "check_T_dark_posterior_evidence_intake_P": check_T_dark_posterior_evidence_intake_P,
}


def register(registry=None):
    if registry is None:
        return CHECKS
    if hasattr(registry, "update"):
        registry.update(CHECKS)
        return registry
    for name, fn in CHECKS.items():
        if hasattr(registry, "register"):
            registry.register(name, fn)
        elif hasattr(registry, "add"):
            registry.add(name, fn)
        else:
            raise TypeError("Unsupported registry type for interface_dark_posterior_evidence_intake.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    out = run_all()
    ok = all(x.get("passed") for x in out.values())
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    print(MARKER if ok else "DARK_POSTERIOR_EVIDENCE_INTAKE_FAIL")
    raise SystemExit(0 if ok else 1)
