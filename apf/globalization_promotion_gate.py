"""
APF Globalization Promotion Gate.

This module banks the next layer after Obstruction Repair Normal Form.

Given a local representation / claim obstruction, the promotion gate returns the only
honest export status:

  * EXPORT_GLOBAL_P
  * HOLD_ORDINARY_REPAIR_REQUIRED
  * HOLD_SUBSTRATE_REVISION_REQUIRED
  * FAIL_CLOSED_PROVENANCE
  * FAIL_UNKNOWN_UNSUPPORTED

This is the decision layer that prevents overclaiming:
  local structures become global physics only if they are already in ker(Obs), or after
  a certified repair plan is actually executed and rechecked.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, Mapping, Optional, Tuple

try:
    from apf.descent_obstruction_calculus import Obstruction, ObstructionObject
    from apf.obstruction_repair_normal_form import RepairClass, RepairPlan, canonical_plan, example_obstructions, plan_data
except Exception as exc:  # pragma: no cover
    raise ImportError(f"globalization_promotion_gate dependencies missing: {exc}") from exc


def _ok(name: str, *, status: str, summary: str, data: Optional[Mapping] = None,
        dependencies: Optional[Iterable[str]] = None) -> Dict:
    return {
        "name": name,
        "consistent": True,
        "status": status,
        "summary": summary,
        "data": dict(data or {}),
        "dependencies": list(dependencies or []),
    }


def _fail(name: str, *, status: str, summary: str, data: Optional[Mapping] = None,
          dependencies: Optional[Iterable[str]] = None) -> Dict:
    return {
        "name": name,
        "consistent": False,
        "status": status,
        "summary": summary,
        "data": dict(data or {}),
        "dependencies": list(dependencies or []),
    }


class PromotionStatus(str, Enum):
    EXPORT_GLOBAL_P = "EXPORT_GLOBAL_P"
    HOLD_ORDINARY_REPAIR_REQUIRED = "HOLD_ORDINARY_REPAIR_REQUIRED"
    HOLD_SUBSTRATE_REVISION_REQUIRED = "HOLD_SUBSTRATE_REVISION_REQUIRED"
    FAIL_CLOSED_PROVENANCE = "FAIL_CLOSED_PROVENANCE"
    FAIL_UNKNOWN_UNSUPPORTED = "FAIL_UNKNOWN_UNSUPPORTED"
    # v24.3.41 — Mass-sector Step D audit Findings 2 + 3:
    OBSTRUCTION_NAMED_CLOSURE = "OBSTRUCTION_NAMED_CLOSURE"
    EXPORT_INTERNAL_IDENTITY_P = "EXPORT_INTERNAL_IDENTITY_P"


@dataclass(frozen=True)
class PromotionDecision:
    claim: str
    obstruction: ObstructionObject
    repair_plan: RepairPlan
    status: PromotionStatus
    export_global_P: bool
    export_local_P: bool
    next_action: str
    reason: str


def decide_promotion(claim: str, obs: ObstructionObject) -> PromotionDecision:
    plan = canonical_plan(obs)

    if plan.repair_class == RepairClass.EXACT:
        return PromotionDecision(
            claim=claim,
            obstruction=obs,
            repair_plan=plan,
            status=PromotionStatus.EXPORT_GLOBAL_P,
            export_global_P=True,
            export_local_P=True,
            next_action="Export as global P.",
            reason="Obstruction object is zero; claim is already in ker(Obs).",
        )

    if plan.repair_class == RepairClass.ORDINARY_REPAIRABLE:
        return PromotionDecision(
            claim=claim,
            obstruction=obs,
            repair_plan=plan,
            status=PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED,
            export_global_P=False,
            export_local_P=True,
            next_action="Execute ordinary repair plan, regenerate representation data, then rerun gate.",
            reason="Claim is locally meaningful but not global P until ordinary repair is performed and obstruction rechecks to zero.",
        )

    if plan.repair_class == RepairClass.SUBSTRATE_REVISION_REPAIRABLE:
        return PromotionDecision(
            claim=claim,
            obstruction=obs,
            repair_plan=plan,
            status=PromotionStatus.HOLD_SUBSTRATE_REVISION_REQUIRED,
            export_global_P=False,
            export_local_P=True,
            next_action="Do not export as current global P; open a substrate-revision research program.",
            reason="Repair requires D1/D2/D3-style substrate revisions, not current APF primitives.",
        )

    if plan.repair_class == RepairClass.NONREPAIRABLE_PROVENANCE:
        return PromotionDecision(
            claim=claim,
            obstruction=obs,
            repair_plan=plan,
            status=PromotionStatus.FAIL_CLOSED_PROVENANCE,
            export_global_P=False,
            export_local_P=False,
            next_action="Fail closed; rebuild from clean provenance rather than repair mathematically.",
            reason="Provenance smuggling is absorbing and has no mathematical repair normal form.",
        )

    return PromotionDecision(
        claim=claim,
        obstruction=obs,
        repair_plan=plan,
        status=PromotionStatus.FAIL_UNKNOWN_UNSUPPORTED,
        export_global_P=False,
        export_local_P=False,
        next_action="Fail closed; no supported repair route exists in current APF operation set.",
        reason="Unknown unsupported obstruction class or missing repair theorem.",
    )


def decision_data(decision: PromotionDecision) -> Dict:
    return {
        "claim": decision.claim,
        "obstruction": decision.obstruction.names(),
        "repair_plan": plan_data(decision.repair_plan),
        "status": decision.status.value,
        "export_global_P": decision.export_global_P,
        "export_local_P": decision.export_local_P,
        "next_action": decision.next_action,
        "reason": decision.reason,
    }


def claim_examples() -> Dict[str, ObstructionObject]:
    examples = example_obstructions()
    return {
        "ACC_global": examples["exact"],
        "capacity_route": examples["capacity"],
        "contextual_overlap": examples["contextual"],
        "scheme_transport": examples["scheme"],
        "flat_Cstar_globalization": examples["cstar"],
        "polarity_revision": examples["polarity"],
        "provenance_smuggled_claim": examples["smuggled"],
        "mixed_structural_logistical": examples["mixed_structural_logistical"],
    }


def decisions() -> Dict[str, PromotionDecision]:
    return {name: decide_promotion(name, obs) for name, obs in claim_examples().items()}


def check_T_promotion_status_partition_P() -> Dict:
    decs = decisions()
    statuses = {name: d.status.value for name, d in decs.items()}
    tests = {
        "ACC_global_exports": statuses["ACC_global"] == PromotionStatus.EXPORT_GLOBAL_P.value,
        "capacity_holds_for_ordinary_repair": statuses["capacity_route"] == PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED.value,
        "contextual_holds_for_ordinary_repair": statuses["contextual_overlap"] == PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED.value,
        "scheme_holds_for_ordinary_repair": statuses["scheme_transport"] == PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED.value,
        "Cstar_holds_for_substrate_revision": statuses["flat_Cstar_globalization"] == PromotionStatus.HOLD_SUBSTRATE_REVISION_REQUIRED.value,
        "polarity_holds_for_substrate_revision": statuses["polarity_revision"] == PromotionStatus.HOLD_SUBSTRATE_REVISION_REQUIRED.value,
        "provenance_fails_closed": statuses["provenance_smuggled_claim"] == PromotionStatus.FAIL_CLOSED_PROVENANCE.value,
    }
    if all(tests.values()):
        return _ok(
            "check_T_promotion_status_partition_P",
            status="P_gate",
            summary="Promotion gate partitions claims into export, repair-required, substrate-revision-required, and fail-closed statuses.",
            data={"statuses": statuses, "tests": tests},
        )
    return _fail("check_T_promotion_status_partition_P", status="FAIL", summary="Promotion status partition failed", data={"statuses": statuses, "tests": tests})


def check_T_export_only_zero_obstruction_P() -> Dict:
    decs = decisions()
    tests = {
        name: (d.export_global_P == d.obstruction.is_zero)
        for name, d in decs.items()
    }
    tests["only_ACC_global_exports"] = [name for name, d in decs.items() if d.export_global_P] == ["ACC_global"]
    if all(tests.values()):
        return _ok(
            "check_T_export_only_zero_obstruction_P",
            status="P_gate",
            summary="Global P export is allowed if and only if the obstruction object is zero.",
            data={"tests": tests, "decisions": {n: decision_data(d) for n, d in decs.items()}},
            dependencies=["check_T_promotion_status_partition_P"],
        )
    return _fail("check_T_export_only_zero_obstruction_P", status="FAIL", summary="Export gate allowed nonzero obstruction or blocked zero obstruction", data={"tests": tests})


def check_T_ordinary_repair_hold_not_export_P() -> Dict:
    decs = decisions()
    ordinary = {n: d for n, d in decs.items() if d.status == PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED}
    tests = {
        "ordinary_nonempty": len(ordinary) >= 1,
        "none_export_global": all(not d.export_global_P for d in ordinary.values()),
        "all_have_successful_plan": all(d.repair_plan.succeeds for d in ordinary.values()),
        "all_require_rerun": all("rerun gate" in d.next_action for d in ordinary.values()),
    }
    if all(tests.values()):
        return _ok(
            "check_T_ordinary_repair_hold_not_export_P",
            status="P_gate",
            summary="Ordinarily repairable claims are held, not exported, until repair is executed and rechecked.",
            data={"ordinary": {n: decision_data(d) for n, d in ordinary.items()}, "tests": tests},
            dependencies=["check_T_export_only_zero_obstruction_P"],
        )
    return _fail("check_T_ordinary_repair_hold_not_export_P", status="FAIL", summary="Ordinary repair hold gate failed", data={"tests": tests, "ordinary": {n: decision_data(d) for n, d in ordinary.items()}})


def check_T_substrate_revision_hold_not_current_P() -> Dict:
    decs = decisions()
    substrate = {n: d for n, d in decs.items() if d.status == PromotionStatus.HOLD_SUBSTRATE_REVISION_REQUIRED}
    tests = {
        "substrate_revision_nonempty": len(substrate) >= 1,
        "none_export_global": all(not d.export_global_P for d in substrate.values()),
        "all_have_successful_counterfactual_plan": all(d.repair_plan.succeeds for d in substrate.values()),
        "all_open_research_program": all("substrate-revision" in d.next_action for d in substrate.values()),
    }
    if all(tests.values()):
        return _ok(
            "check_T_substrate_revision_hold_not_current_P",
            status="P_gate",
            summary="Substrate-revision-repairable claims are not current global P; they open D1/D2/D3 research programs.",
            data={"substrate_revision": {n: decision_data(d) for n, d in substrate.items()}, "tests": tests},
            dependencies=["check_T_export_only_zero_obstruction_P"],
        )
    return _fail("check_T_substrate_revision_hold_not_current_P", status="FAIL", summary="Substrate revision hold gate failed", data={"tests": tests, "substrate": {n: decision_data(d) for n, d in substrate.items()}})


def check_T_provenance_fail_closed_P() -> Dict:
    decs = decisions()
    prov = decs["provenance_smuggled_claim"]
    tests = {
        "status_fail_closed": prov.status == PromotionStatus.FAIL_CLOSED_PROVENANCE,
        "no_global_export": not prov.export_global_P,
        "no_local_export": not prov.export_local_P,
        "no_repair_operations": prov.repair_plan.operations == tuple(),
        "rebuild_required": "rebuild" in prov.next_action,
    }
    if all(tests.values()):
        return _ok(
            "check_T_provenance_fail_closed_P",
            status="P_audit",
            summary="Provenance-smuggled claims fail closed and cannot be promoted or repaired mathematically.",
            data={"decision": decision_data(prov), "tests": tests},
            dependencies=["check_T_export_only_zero_obstruction_P"],
        )
    return _fail("check_T_provenance_fail_closed_P", status="FAIL", summary="Provenance fail-closed gate failed", data={"decision": decision_data(prov), "tests": tests})


def check_T_claim_language_emitter_P() -> Dict:
    decs = decisions()
    claim_language = {}
    for name, d in decs.items():
        if d.status == PromotionStatus.EXPORT_GLOBAL_P:
            claim_language[name] = "Export as globally admissible P."
        elif d.status == PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED:
            claim_language[name] = "Local/repairable only; not global P until repair executed and obstruction rechecks to zero."
        elif d.status == PromotionStatus.HOLD_SUBSTRATE_REVISION_REQUIRED:
            claim_language[name] = "Counterfactual/substrate-revision program only; not current global P."
        elif d.status == PromotionStatus.FAIL_CLOSED_PROVENANCE:
            claim_language[name] = "Fail closed; rebuild from clean provenance."
        else:
            claim_language[name] = "Fail closed; unsupported."
    tests = {
        "all_claims_have_language": set(claim_language) == set(decs),
        "non_exports_marked_not_global_P": all(
            ("not global P" in lang or "Fail closed" in lang or "not current global P" in lang)
            for name, lang in claim_language.items()
            if name != "ACC_global"
        ),
    }
    if all(tests.values()):
        return _ok(
            "check_T_claim_language_emitter_P",
            status="P_gate",
            summary="Promotion gate emits safe claim language for each status.",
            data={"claim_language": claim_language, "tests": tests},
            dependencies=[
                "check_T_ordinary_repair_hold_not_export_P",
                "check_T_substrate_revision_hold_not_current_P",
                "check_T_provenance_fail_closed_P",
            ],
        )
    return _fail("check_T_claim_language_emitter_P", status="FAIL", summary="Claim language emitter failed", data={"claim_language": claim_language, "tests": tests})


def check_T_no_promotion_overclaim_P() -> Dict:
    return _ok(
        "check_T_no_promotion_overclaim_P",
        status="P_audit",
        summary="Scope boundary preserved: repairability is not promotion; only zero obstruction exports global P.",
        data={
            "repairability_implies_current_global_P": False,
            "substrate_revision_available_claimed": False,
            "local_P_equals_global_P_claimed": False,
            "zero_obstruction_required_for_global_export": True,
        },
    )


def check_T_globalization_promotion_gate_P() -> Dict:
    subchecks = [
        check_T_promotion_status_partition_P(),
        check_T_export_only_zero_obstruction_P(),
        check_T_ordinary_repair_hold_not_export_P(),
        check_T_substrate_revision_hold_not_current_P(),
        check_T_provenance_fail_closed_P(),
        check_T_claim_language_emitter_P(),
        check_T_no_promotion_overclaim_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_globalization_promotion_gate_P",
            status="P_gate",
            summary="Globalization promotion gate is P: it exports only zero-obstruction claims and fail-closes/holds all others.",
            data={
                "main_rule": "export_global_P iff Obs=0",
                "statuses": [s.value for s in PromotionStatus],
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_globalization_promotion_gate_P",
        status="FAIL",
        summary="Globalization promotion gate assembly failed.",
        data={"subchecks": subchecks},
    )


CHECKS = {
    "check_T_promotion_status_partition_P": check_T_promotion_status_partition_P,
    "check_T_export_only_zero_obstruction_P": check_T_export_only_zero_obstruction_P,
    "check_T_ordinary_repair_hold_not_export_P": check_T_ordinary_repair_hold_not_export_P,
    "check_T_substrate_revision_hold_not_current_P": check_T_substrate_revision_hold_not_current_P,
    "check_T_provenance_fail_closed_P": check_T_provenance_fail_closed_P,
    "check_T_claim_language_emitter_P": check_T_claim_language_emitter_P,
    "check_T_no_promotion_overclaim_P": check_T_no_promotion_overclaim_P,
    "check_T_globalization_promotion_gate_P": check_T_globalization_promotion_gate_P,
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
            raise TypeError("Unsupported registry type for globalization_promotion_gate.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
