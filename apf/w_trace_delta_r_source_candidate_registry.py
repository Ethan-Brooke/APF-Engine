"""W_TRACE standard Delta_r source-candidate registry / literature mapping.

Physics-source acquisition module for v13.2.  The v13.1 pivot allowed
standard electroweak Delta_r source payloads before forcing APF's legacy
finite-part slots.  This module banks the next physics step: a concrete
candidate-source registry and source-to-payload mapping for electroweak Delta_r.

The registry is deliberately candidate-only.  It names source classes and
literature candidates, records what each may supply, and defines admission
preconditions.  It does not admit numerical rows, does not certify a component
sum, and does not unlock physical W export.
"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Tuple

from apf import w_trace_delta_r_source_mapping as srcmap

STATUS = "P_w_delta_r_source_candidate_registry"
VERSION = "w_trace_delta_r_source_candidate_registry_v1"
PASS_STATUS = "W_TRACE_DELTA_R_SOURCE_CANDIDATE_REGISTRY_BANK_PASS"
TITLE = "W_TRACE standard Delta_r source-candidate registry / literature mapping"

STANDARD_PAYLOAD_KINDS = srcmap.ALLOWED_PAYLOAD_KINDS
STANDARD_DECOMPOSITION = srcmap.STANDARD_DECOMPOSITION
APF_DELTA_R_TARGET = srcmap.APF_DELTA_R_TARGET
M_W_TRACE_GEV = srcmap.M_W_TRACE_GEV

SOURCE_TIERS = ("tier_1_precision_prediction", "tier_2_structure_counterterm", "tier_3_constants_inputs", "tier_4_historical_definition")
SOURCE_ROLES = (
    "delta_r_total_or_parametrization",
    "delta_r_decomposition_structure",
    "counterterm_scheme_structure",
    "input_constant_source",
    "definition_lineage",
)

CANDIDATE_SOURCES: Dict[str, Dict[str, Any]] = {
    "ACFW_precision_MW_parametrization": {
        "tier": "tier_1_precision_prediction",
        "source_family": "Awramik-Czakon-Freitas-Weiglein precision Standard Model W-mass parametrization",
        "role": "delta_r_total_or_parametrization",
        "payload_kinds_supported": ("standard_delta_r_parametrization", "standard_delta_r_total"),
        "may_supply": ("Delta_r_total", "M_W_SM_parametrization_auxiliary", "theory_uncertainty_auxiliary"),
        "does_not_supply": ("APF_legacy_eight_slot_rows", "observed_M_W_input"),
        "admission_status": "candidate_not_admitted",
        "requires_extraction": True,
        "requires_observed_w_exclusion_audit": True,
    },
    "Denner_on_shell_renormalization_structure": {
        "tier": "tier_2_structure_counterterm",
        "source_family": "Denner-style on-shell electroweak renormalization and counterterm review",
        "role": "counterterm_scheme_structure",
        "payload_kinds_supported": ("standard_delta_r_decomposition",),
        "may_supply": ("Delta_r_ct_OS_structure", "on_shell_counterterm_convention", "renormalization_terms"),
        "does_not_supply": ("reviewed_numeric_Delta_r_total", "physical_W_export"),
        "admission_status": "candidate_not_admitted",
        "requires_extraction": True,
        "requires_observed_w_exclusion_audit": True,
    },
    "Sirlin_Delta_r_lineage": {
        "tier": "tier_4_historical_definition",
        "source_family": "Sirlin-style original Delta_r/on-shell correction definition lineage",
        "role": "definition_lineage",
        "payload_kinds_supported": ("standard_delta_r_decomposition",),
        "may_supply": ("Delta_r_definition", "on_shell_relation_context"),
        "does_not_supply": ("modern_precision_payload", "APF_payload_rows"),
        "admission_status": "candidate_not_admitted",
        "requires_extraction": True,
        "requires_observed_w_exclusion_audit": True,
    },
    "PDG_EW_review_summary": {
        "tier": "tier_3_constants_inputs",
        "source_family": "PDG electroweak review / Z-pole and Standard Model summary",
        "role": "input_constant_source",
        "payload_kinds_supported": (),
        "may_supply": ("M_Z_on_shell_reference", "EW_review_crosscheck"),
        "does_not_supply": ("Delta_r_component_rows", "observed_M_W_for_target_fit"),
        "admission_status": "candidate_not_admitted",
        "requires_extraction": True,
        "requires_observed_w_exclusion_audit": True,
    },
    "NIST_CODATA_alpha_reference": {
        "tier": "tier_3_constants_inputs",
        "source_family": "NIST/CODATA fine-structure constant reference",
        "role": "input_constant_source",
        "payload_kinds_supported": (),
        "may_supply": ("alpha_em_reference",),
        "does_not_supply": ("Delta_r_total", "M_W_observation"),
        "admission_status": "candidate_not_admitted",
        "requires_extraction": True,
        "requires_observed_w_exclusion_audit": True,
    },
    "MuLan_GF_reference": {
        "tier": "tier_3_constants_inputs",
        "source_family": "Muon lifetime / Fermi constant reference",
        "role": "input_constant_source",
        "payload_kinds_supported": (),
        "may_supply": ("G_F_reference",),
        "does_not_supply": ("Delta_r_total", "M_W_observation"),
        "admission_status": "candidate_not_admitted",
        "requires_extraction": True,
        "requires_observed_w_exclusion_audit": True,
    },
}

REQUIRED_SOURCE_FIELDS = (
    "candidate_id",
    "source_family",
    "tier",
    "role",
    "payload_kinds_supported",
    "may_supply",
    "does_not_supply",
    "admission_status",
)

FORBIDDEN_TOKENS = tuple(srcmap.FORBIDDEN_TOKENS) + (
    "observed_W_as_source_input",
    "world_average_MW_as_delta_r_source",
    "fit_to_APF_target",
    "tune_Delta_r_rem_to_APF",
    "posthoc_payload_fit",
    "export_physical_MW_now",
)

LOCKED_STATE = {
    "delta_r_source_candidate_registry_banked": True,
    "real_delta_r_source_admitted": False,
    "real_delta_r_payload_rows_imported": False,
    "component_sum_certified": False,
    "physical_W_export_enabled": False,
    "exports_physical_M_W": False,
}


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _contains_forbidden_token(obj: Any) -> bool:
    text = _canonical_json(obj)
    return any(tok in text for tok in FORBIDDEN_TOKENS)


def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed)}
    row.update(extra)
    return row


def _passed(row: Any) -> bool:
    return bool(isinstance(row, dict) and row.get("passed") is True)


def registry() -> Dict[str, Dict[str, Any]]:
    return {k: dict(v, candidate_id=k) for k, v in CANDIDATE_SOURCES.items()}


def terminal_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "upstream_mapping_status": srcmap.STATUS,
        "strategy": "candidate_literature_sources_first_admission_later",
        "standard_payload_kinds": list(STANDARD_PAYLOAD_KINDS),
        "standard_decomposition": list(STANDARD_DECOMPOSITION),
        "candidate_sources": registry(),
        "source_tiers": list(SOURCE_TIERS),
        "source_roles": list(SOURCE_ROLES),
        "apf_comparison_target": {
            "M_W_TRACE_GeV": M_W_TRACE_GEV,
            "Delta_r_APF_TRACE_target": APF_DELTA_R_TARGET,
            "use": "comparison_only_after_independent_source_admission",
        },
        "locked_state": dict(LOCKED_STATE),
        "stop_rule": "Do not admit any literature candidate as a payload until extraction provenance, forbidden-input audit, and payload-kind mapping are complete.",
    }


def candidate_ids_by_role(role: str) -> Tuple[str, ...]:
    return tuple(k for k, v in CANDIDATE_SOURCES.items() if v["role"] == role)


def candidate_ids_by_tier(tier: str) -> Tuple[str, ...]:
    return tuple(k for k, v in CANDIDATE_SOURCES.items() if v["tier"] == tier)


def source_to_payload_plan(candidate_id: str) -> Dict[str, Any]:
    candidates = registry()
    errors: List[str] = []
    if candidate_id not in candidates:
        return {"valid_candidate": False, "candidate_id": candidate_id, "errors": ["unknown_candidate_id"], "physical_W_export_enabled": False, "exports_physical_M_W": False}
    c = candidates[candidate_id]
    if _contains_forbidden_token(c):
        errors.append("forbidden_token_detected")
    supported = tuple(c.get("payload_kinds_supported", ()))
    plan = {
        "valid_candidate": not errors,
        "candidate_id": candidate_id,
        "source_family": c["source_family"],
        "role": c["role"],
        "tier": c["tier"],
        "payload_kinds_supported": supported,
        "can_supply_delta_r_payload": any(k in STANDARD_PAYLOAD_KINDS for k in supported),
        "can_supply_constants_only": c["role"] == "input_constant_source",
        "requires_extraction": bool(c.get("requires_extraction")),
        "requires_observed_w_exclusion_audit": bool(c.get("requires_observed_w_exclusion_audit")),
        "admission_status": c["admission_status"],
        "real_payload_admitted": False,
        "comparison_target_role": "comparison_only_after_source_admission",
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "errors": errors,
    }
    return plan


def validate_candidate_entry(entry: Mapping[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    if _contains_forbidden_token(entry):
        errors.append("forbidden_token_detected")
    for field in REQUIRED_SOURCE_FIELDS:
        if field not in entry:
            errors.append(f"missing_field:{field}")
    if entry.get("tier") not in SOURCE_TIERS:
        errors.append("unknown_tier")
    if entry.get("role") not in SOURCE_ROLES:
        errors.append("unknown_role")
    for kind in entry.get("payload_kinds_supported", ()):  # constants-only sources use an empty tuple
        if kind not in STANDARD_PAYLOAD_KINDS:
            errors.append(f"unknown_payload_kind:{kind}")
    if entry.get("admission_status") != "candidate_not_admitted":
        errors.append("candidate_must_not_be_admitted_by_registry")
    return {"valid": not errors, "errors": errors, "physical_W_export_enabled": False, "exports_physical_M_W": False}


def validate_registry() -> Dict[str, Any]:
    rows = {cid: validate_candidate_entry(entry) for cid, entry in registry().items()}
    return {
        "valid": all(r["valid"] for r in rows.values()),
        "candidate_count": len(rows),
        "rows": rows,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
    }


def build_acquisition_priority() -> Tuple[str, ...]:
    """Return the recommended source-acquisition order."""
    return (
        "ACFW_precision_MW_parametrization",
        "Denner_on_shell_renormalization_structure",
        "PDG_EW_review_summary",
        "NIST_CODATA_alpha_reference",
        "MuLan_GF_reference",
        "Sirlin_Delta_r_lineage",
    )


# Checks

def check_T_w_trace_source_candidate_registry_status_declared():
    return _res("status_declared", STATUS == "P_w_delta_r_source_candidate_registry" and VERSION == "w_trace_delta_r_source_candidate_registry_v1")


def check_T_w_trace_source_candidate_registry_upstream_mapping_imports():
    return _res("upstream_mapping_imports", srcmap.STATUS == "P_w_delta_r_source_mapping" and "standard_delta_r_total" in srcmap.ALLOWED_PAYLOAD_KINDS)


def check_T_w_trace_source_candidate_registry_candidate_count():
    return _res("candidate_count", len(CANDIDATE_SOURCES) >= 6)


def check_T_w_trace_source_candidate_registry_required_fields_complete():
    v = validate_registry()
    return _res("required_fields_complete", v["valid"], invalid=[k for k, r in v["rows"].items() if not r["valid"]])


def check_T_w_trace_source_candidate_registry_tiers_declared():
    tiers = {v["tier"] for v in CANDIDATE_SOURCES.values()}
    return _res("tiers_declared", tiers == set(SOURCE_TIERS))


def check_T_w_trace_source_candidate_registry_roles_declared():
    roles = {v["role"] for v in CANDIDATE_SOURCES.values()}
    return _res("roles_declared", {"delta_r_total_or_parametrization", "counterterm_scheme_structure", "input_constant_source", "definition_lineage"}.issubset(roles))


def check_T_w_trace_source_candidate_registry_precision_source_present():
    p = source_to_payload_plan("ACFW_precision_MW_parametrization")
    return _res("precision_source_present", p["valid_candidate"] and p["can_supply_delta_r_payload"] and "standard_delta_r_parametrization" in p["payload_kinds_supported"])


def check_T_w_trace_source_candidate_registry_counterterm_source_present():
    p = source_to_payload_plan("Denner_on_shell_renormalization_structure")
    return _res("counterterm_source_present", p["valid_candidate"] and p["role"] == "counterterm_scheme_structure")


def check_T_w_trace_source_candidate_registry_lineage_source_present():
    p = source_to_payload_plan("Sirlin_Delta_r_lineage")
    return _res("lineage_source_present", p["valid_candidate"] and p["role"] == "definition_lineage")


def check_T_w_trace_source_candidate_registry_constants_sources_present():
    ids = set(candidate_ids_by_role("input_constant_source"))
    return _res("constants_sources_present", {"PDG_EW_review_summary", "NIST_CODATA_alpha_reference", "MuLan_GF_reference"}.issubset(ids))


def check_T_w_trace_source_candidate_registry_standard_payload_kind_limited():
    ok = True
    for c in CANDIDATE_SOURCES.values():
        ok = ok and all(k in STANDARD_PAYLOAD_KINDS for k in c["payload_kinds_supported"])
    return _res("standard_payload_kind_limited", ok)


def check_T_w_trace_source_candidate_registry_no_candidate_admitted():
    return _res("no_candidate_admitted", all(v["admission_status"] == "candidate_not_admitted" for v in CANDIDATE_SOURCES.values()))


def check_T_w_trace_source_candidate_registry_observed_w_audit_required():
    return _res("observed_w_audit_required", all(v["requires_observed_w_exclusion_audit"] is True for v in CANDIDATE_SOURCES.values()))


def check_T_w_trace_source_candidate_registry_extraction_required():
    return _res("extraction_required", all(v["requires_extraction"] is True for v in CANDIDATE_SOURCES.values()))


def check_T_w_trace_source_candidate_registry_unknown_candidate_rejected():
    p = source_to_payload_plan("not_a_candidate")
    return _res("unknown_candidate_rejected", not p["valid_candidate"] and "unknown_candidate_id" in p["errors"])


def check_T_w_trace_source_candidate_registry_forbidden_token_rejected():
    entry = dict(registry()["ACFW_precision_MW_parametrization"])
    entry["note"] = "fit_to_APF_target"
    v = validate_candidate_entry(entry)
    return _res("forbidden_token_rejected", not v["valid"] and "forbidden_token_detected" in v["errors"])


def check_T_w_trace_source_candidate_registry_constants_only_not_delta_r_payload():
    p = source_to_payload_plan("NIST_CODATA_alpha_reference")
    return _res("constants_only_not_delta_r_payload", p["can_supply_constants_only"] and not p["can_supply_delta_r_payload"])


def check_T_w_trace_source_candidate_registry_priority_order_declared():
    order = build_acquisition_priority()
    return _res("priority_order_declared", order[0] == "ACFW_precision_MW_parametrization" and set(order) == set(CANDIDATE_SOURCES))


def check_T_w_trace_source_candidate_registry_apf_anchor_comparison_only():
    r = terminal_report()["apf_comparison_target"]
    return _res("apf_anchor_comparison_only", r["Delta_r_APF_TRACE_target"] == APF_DELTA_R_TARGET and "comparison_only" in r["use"])


def check_T_w_trace_source_candidate_registry_physical_export_locked():
    s = terminal_report()["locked_state"]
    return _res("physical_export_locked", s["physical_W_export_enabled"] is False and s["exports_physical_M_W"] is False)


def check_T_w_trace_source_candidate_registry_source_plan_no_export():
    p = source_to_payload_plan("ACFW_precision_MW_parametrization")
    return _res("source_plan_no_export", p["physical_W_export_enabled"] is False and p["exports_physical_M_W"] is False)


def check_T_w_trace_source_candidate_registry_serializable():
    json.dumps(terminal_report(), sort_keys=True)
    json.dumps(validate_registry(), sort_keys=True)
    return _res("serializable", True)


def check_T_w_trace_source_candidate_registry_candidate_ids_stable():
    ok = all(re.fullmatch(r"[A-Za-z0-9_]+", cid) for cid in CANDIDATE_SOURCES)
    return _res("candidate_ids_stable", ok)


def check_T_w_trace_source_candidate_registry_bank_closure():
    checks = [fn for name, fn in CHECKS.items() if name != "T_w_trace_source_candidate_registry_bank_closure"]
    rows = [fn() for fn in checks]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))


CHECKS = {
    "T_w_trace_source_candidate_registry_status_declared": check_T_w_trace_source_candidate_registry_status_declared,
    "T_w_trace_source_candidate_registry_upstream_mapping_imports": check_T_w_trace_source_candidate_registry_upstream_mapping_imports,
    "T_w_trace_source_candidate_registry_candidate_count": check_T_w_trace_source_candidate_registry_candidate_count,
    "T_w_trace_source_candidate_registry_required_fields_complete": check_T_w_trace_source_candidate_registry_required_fields_complete,
    "T_w_trace_source_candidate_registry_tiers_declared": check_T_w_trace_source_candidate_registry_tiers_declared,
    "T_w_trace_source_candidate_registry_roles_declared": check_T_w_trace_source_candidate_registry_roles_declared,
    "T_w_trace_source_candidate_registry_precision_source_present": check_T_w_trace_source_candidate_registry_precision_source_present,
    "T_w_trace_source_candidate_registry_counterterm_source_present": check_T_w_trace_source_candidate_registry_counterterm_source_present,
    "T_w_trace_source_candidate_registry_lineage_source_present": check_T_w_trace_source_candidate_registry_lineage_source_present,
    "T_w_trace_source_candidate_registry_constants_sources_present": check_T_w_trace_source_candidate_registry_constants_sources_present,
    "T_w_trace_source_candidate_registry_standard_payload_kind_limited": check_T_w_trace_source_candidate_registry_standard_payload_kind_limited,
    "T_w_trace_source_candidate_registry_no_candidate_admitted": check_T_w_trace_source_candidate_registry_no_candidate_admitted,
    "T_w_trace_source_candidate_registry_observed_w_audit_required": check_T_w_trace_source_candidate_registry_observed_w_audit_required,
    "T_w_trace_source_candidate_registry_extraction_required": check_T_w_trace_source_candidate_registry_extraction_required,
    "T_w_trace_source_candidate_registry_unknown_candidate_rejected": check_T_w_trace_source_candidate_registry_unknown_candidate_rejected,
    "T_w_trace_source_candidate_registry_forbidden_token_rejected": check_T_w_trace_source_candidate_registry_forbidden_token_rejected,
    "T_w_trace_source_candidate_registry_constants_only_not_delta_r_payload": check_T_w_trace_source_candidate_registry_constants_only_not_delta_r_payload,
    "T_w_trace_source_candidate_registry_priority_order_declared": check_T_w_trace_source_candidate_registry_priority_order_declared,
    "T_w_trace_source_candidate_registry_apf_anchor_comparison_only": check_T_w_trace_source_candidate_registry_apf_anchor_comparison_only,
    "T_w_trace_source_candidate_registry_physical_export_locked": check_T_w_trace_source_candidate_registry_physical_export_locked,
    "T_w_trace_source_candidate_registry_source_plan_no_export": check_T_w_trace_source_candidate_registry_source_plan_no_export,
    "T_w_trace_source_candidate_registry_serializable": check_T_w_trace_source_candidate_registry_serializable,
    "T_w_trace_source_candidate_registry_candidate_ids_stable": check_T_w_trace_source_candidate_registry_candidate_ids_stable,
}
CHECKS["T_w_trace_source_candidate_registry_bank_closure"] = check_T_w_trace_source_candidate_registry_bank_closure
_CHECKS = CHECKS


def register(registry: MutableMapping[str, Any]) -> None:
    registry.update(_CHECKS)


def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:  # pragma: no cover
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {"passed": ok, "status": PASS_STATUS if ok else PASS_STATUS.replace("_PASS", "_FAIL"), "checks": rows, "report": terminal_report()}
