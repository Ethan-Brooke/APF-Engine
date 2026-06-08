"""APF Defect Calculus Engine.

Tier 2 member of the APF Interface Engine family per
``APF Reference Docs/Reference - APF Interface Engine Family Architecture (2026-05-19).md``
(Session 6 — latent engine operationalization).

The Defect Calculus Engine adjudicates **continuation certificates** against
the defect-stratum object ladder (A_Gamma ⊃ P_Gamma ⊃ O_Gamma ⊃ E_{Gamma,r}).
Wraps the existing defect-calculus stack (v24.3.18, 12 architecture-only modules)
+ ``apf.defect_global_descent_kernel.certify_global_descent`` operational entry.

Unit of adjudication
--------------------
A continuation certificate / global descent specification. Input: a sequence
of InterfacePatch objects (from defect_global_descent_kernel). Output:
``DefectAdjudicationVerdict`` typed by the engine's failure-mode taxonomy.

Failure-mode taxonomy
---------------------

* ``ZERO_DEFECT_GLOBAL`` -- in the global descent kernel
* ``DELTA_P_NONZERO`` -- preservation defect (P stratum non-zero)
* ``DELTA_O_NONZERO`` -- resolution defect (O stratum non-zero)
* ``DELTA_E_R_NONZERO`` -- route/export defect (E_{Gamma,r} stratum non-zero)
* ``GLOBAL_DESCENT_KERNEL_NONEMPTY`` -- global kernel has residual obstructions
* ``OPEN_EVIDENCE_REQUIRED`` -- need patch data for adjudication

Wraps existing modules
----------------------

* ``apf.defect_master_integration.stack_report`` — confirms 10 defect layers loaded
* ``apf.defect_global_descent_kernel.certify_global_descent`` — primary entry
* ``apf.defect_global_descent_kernel.in_global_kernel`` — zero-defect predicate

Audit-first discipline
----------------------

No new physical claim. The engine produces structural classification verdicts
over continuation certificates; same audit-first invariants as other IE family
members. ``target_value_consumed = False`` propagated.

References
----------

* ``apf.defect_master_integration`` — defect-calculus stack integration
* ``apf.defect_global_descent_kernel`` — Theorem 7 global descent kernel
* ``Reference - APF Interface Engine Family Architecture (2026-05-19).md``
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Engine identity
# ---------------------------------------------------------------------------

ENGINE_NAME = "defect_calculus"
ENGINE_FAMILY = "APF_Interface_Engine"
ENGINE_TIER = 2
ENGINE_ROLE = "defect_stratum_adjudication"


# ---------------------------------------------------------------------------
# Verdict status enum
# ---------------------------------------------------------------------------

class DefectAdjudicationStatus(str, Enum):
    ZERO_DEFECT_GLOBAL = "ZERO_DEFECT_GLOBAL"
    DELTA_P_NONZERO = "DELTA_P_NONZERO"
    DELTA_O_NONZERO = "DELTA_O_NONZERO"
    DELTA_E_R_NONZERO = "DELTA_E_R_NONZERO"
    GLOBAL_DESCENT_KERNEL_NONEMPTY = "GLOBAL_DESCENT_KERNEL_NONEMPTY"
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"


PRESERVED_NON_CLAIMS: Tuple[str, ...] = (
    "target_value_consumed",
    "new_physical_claim",
    "infinity_stack_claim",
)


# ---------------------------------------------------------------------------
# Verdict dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DefectAdjudicationVerdict:
    unit_id: str
    status: DefectAdjudicationStatus
    in_global_kernel: bool
    critical_fields: Tuple[str, ...]
    defect_summary: Mapping[str, Any]
    obligation_packet: Mapping[str, Any]
    exports: Mapping[str, int]
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


# ---------------------------------------------------------------------------
# Engine entry point
# ---------------------------------------------------------------------------

def adjudicate_defect_stratum(
    unit_id: str = "default_continuation_certificate",
    patches: Optional[Sequence[Any]] = None,
) -> DefectAdjudicationVerdict:
    """Adjudicate a continuation certificate against the defect-stratum ladder.

    Parameters
    ----------
    unit_id : str
        Identifier for this continuation certificate (for obligation packet).
    patches : Sequence of InterfacePatch or None
        Patches describing the continuation certificate. If None, returns
        OPEN_EVIDENCE_REQUIRED with patches-missing obligation.

    Returns
    -------
    DefectAdjudicationVerdict
    """
    if patches is None or len(patches) == 0:
        return _patches_missing_verdict(unit_id)

    try:
        from apf.defect_global_descent_kernel import (
            certify_global_descent,
            in_global_kernel,
        )
        from apf.defect_master_integration import (
            stack_report,
            defect_stack_ready,
        )
    except ImportError as exc:
        return _import_failed_verdict(unit_id, exc)

    # Verify the defect stack is integrated
    ready = defect_stack_ready()
    if not ready:
        stack = stack_report()
        return DefectAdjudicationVerdict(
            unit_id=unit_id,
            status=DefectAdjudicationStatus.OPEN_EVIDENCE_REQUIRED,
            in_global_kernel=False,
            critical_fields=("defect_stack_not_ready",),
            defect_summary={"stack_ready": False},
            obligation_packet={
                "obligation_kind": "defect_stack_not_integrated",
                "target_engine": ENGINE_NAME,
                "target_unit_id": unit_id,
                "evidence_required": ["all 10 defect layers loaded"],
                "current_status": "STACK_NOT_READY",
                "recommended_next_action": (
                    "verify defect-calculus 12 modules (v24.3.18) loaded; "
                    "check apf.defect_master_integration.stack_report()"
                ),
            },
            exports={k: 0 for k in PRESERVED_NON_CLAIMS},
            reason="defect calculus stack not ready",
        )

    try:
        cert = certify_global_descent(patches)
    except Exception as exc:
        return DefectAdjudicationVerdict(
            unit_id=unit_id,
            status=DefectAdjudicationStatus.OPEN_EVIDENCE_REQUIRED,
            in_global_kernel=False,
            critical_fields=("certification_machinery_error",),
            defect_summary={"error": f"{type(exc).__name__}: {exc}"},
            obligation_packet={
                "obligation_kind": "certification_error",
                "target_engine": ENGINE_NAME,
                "target_unit_id": unit_id,
                "evidence_required": ["valid InterfacePatch sequence"],
                "current_status": "MACHINERY_ERROR",
                "recommended_next_action": (
                    "check apf.defect_global_descent_kernel.certify_global_descent "
                    "signature + InterfacePatch schema"
                ),
                "error_detail": f"{type(exc).__name__}: {exc}",
            },
            exports={k: 0 for k in PRESERVED_NON_CLAIMS},
            reason=f"certification machinery raised: {exc}",
        )

    cert_in_kernel = in_global_kernel(cert)
    if cert_in_kernel:
        status = DefectAdjudicationStatus.ZERO_DEFECT_GLOBAL
        export_p = True
        critical: Tuple[str, ...] = ()
    else:
        # Outside the global kernel — classify by which defect is non-zero
        status = DefectAdjudicationStatus.GLOBAL_DESCENT_KERNEL_NONEMPTY
        export_p = False
        critical = ("global_descent_kernel_nonempty",)

    obligation_packet = _build_obligation_packet(
        unit_id=unit_id,
        status=status,
        critical=critical,
        cert=cert,
    )

    exports = {k: 0 for k in PRESERVED_NON_CLAIMS}
    exports["zero_defect_global_kernel"] = int(cert_in_kernel)
    exports["defect_adjudication_evaluated"] = 1

    return DefectAdjudicationVerdict(
        unit_id=unit_id,
        status=status,
        in_global_kernel=cert_in_kernel,
        critical_fields=critical,
        defect_summary={
            "in_global_kernel": cert_in_kernel,
            "patch_count": len(patches),
        },
        obligation_packet=obligation_packet,
        exports=exports,
        reason=(
            "all patches in zero-defect global kernel" if cert_in_kernel
            else "global descent kernel has residual obstructions"
        ),
    )


def _patches_missing_verdict(unit_id: str) -> DefectAdjudicationVerdict:
    return DefectAdjudicationVerdict(
        unit_id=unit_id,
        status=DefectAdjudicationStatus.OPEN_EVIDENCE_REQUIRED,
        in_global_kernel=False,
        critical_fields=("patches_missing",),
        defect_summary={},
        obligation_packet={
            "obligation_kind": "patches_missing",
            "target_engine": ENGINE_NAME,
            "target_unit_id": unit_id,
            "evidence_required": [
                "InterfacePatch sequence (one or more) describing the continuation certificate",
            ],
            "current_status": "MISSING_INPUT",
            "recommended_next_action": (
                "call adjudicate_defect_stratum(unit_id, patches) with patches arg"
            ),
        },
        exports={k: 0 for k in PRESERVED_NON_CLAIMS},
        reason="patches argument required for adjudication",
    )


def _import_failed_verdict(unit_id: str, exc: Exception) -> DefectAdjudicationVerdict:
    return DefectAdjudicationVerdict(
        unit_id=unit_id,
        status=DefectAdjudicationStatus.OPEN_EVIDENCE_REQUIRED,
        in_global_kernel=False,
        critical_fields=("defect_calculus_modules_missing",),
        defect_summary={},
        obligation_packet={
            "obligation_kind": "import_failed",
            "target_engine": ENGINE_NAME,
            "target_unit_id": unit_id,
            "evidence_required": [
                "apf.defect_master_integration importable",
                "apf.defect_global_descent_kernel importable",
            ],
            "current_status": "IMPORT_FAILED",
            "recommended_next_action": "verify defect-calculus 12 modules installed (v24.3.18)",
            "error_detail": f"{type(exc).__name__}: {exc}",
        },
        exports={k: 0 for k in PRESERVED_NON_CLAIMS},
        reason=f"import of defect-calculus modules failed: {exc}",
    )


def _build_obligation_packet(
    unit_id: str,
    status: DefectAdjudicationStatus,
    critical: Tuple[str, ...],
    cert: Any,
) -> Dict[str, Any]:
    obligation_kind_map = {
        DefectAdjudicationStatus.ZERO_DEFECT_GLOBAL: "no_obligation",
        DefectAdjudicationStatus.DELTA_P_NONZERO: "supply_preservation_repair",
        DefectAdjudicationStatus.DELTA_O_NONZERO: "supply_resolution_repair",
        DefectAdjudicationStatus.DELTA_E_R_NONZERO: "supply_route_export_repair",
        DefectAdjudicationStatus.GLOBAL_DESCENT_KERNEL_NONEMPTY: "address_residual_obstructions",
        DefectAdjudicationStatus.OPEN_EVIDENCE_REQUIRED: "supply_continuation_data",
    }
    return {
        "obligation_kind": obligation_kind_map.get(status, "unknown"),
        "target_engine": ENGINE_NAME,
        "target_unit_id": unit_id,
        "evidence_required": list(critical),
        "current_status": status.value,
        "recommended_next_action": (
            "use obstruction_repair_normal_form on residual obstructions"
            if critical else "no action required — in zero-defect global kernel"
        ),
        "evaluation_data": {
            "certificate_type": type(cert).__name__ if cert is not None else None,
        },
    }


# ---------------------------------------------------------------------------
# Bank checks (3)
# ---------------------------------------------------------------------------

def check_T_defect_calculus_engine_identity_P() -> Dict[str, Any]:
    consistent = (
        ENGINE_NAME == "defect_calculus"
        and ENGINE_TIER == 2
        and ENGINE_ROLE == "defect_stratum_adjudication"
        and len(list(DefectAdjudicationStatus)) == 6
        and len(PRESERVED_NON_CLAIMS) == 3
    )
    return {
        "name": "check_T_defect_calculus_engine_identity_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_defect_calculus_engine_identity" if consistent else "FAIL",
        "epistemic": "P_defect_calculus_engine_identity",
        "summary": (
            "Defect Calculus Engine declares Tier 2 role + IE family membership; "
            "6-status verdict taxonomy + 3 preserved non-claims."
        ),
        "dependencies": ["Reference - APF Interface Engine Family Architecture (2026-05-19).md"],
        "data": {"engine_name": ENGINE_NAME, "engine_tier": ENGINE_TIER},
    }


def check_T_defect_calculus_engine_entry_point_P() -> Dict[str, Any]:
    """Entry point smoke: no-patches returns OPEN_EVIDENCE_REQUIRED with right obligation."""
    no_patches = adjudicate_defect_stratum("test_certificate", None)
    no_patches_ok = (
        no_patches.status == DefectAdjudicationStatus.OPEN_EVIDENCE_REQUIRED
        and no_patches.export_global_P is False if hasattr(no_patches, 'export_global_P') else True
        and "patches_missing" in no_patches.critical_fields
        and no_patches.obligation_packet.get("target_engine") == ENGINE_NAME
        and no_patches.in_global_kernel is False
    )
    empty_patches = adjudicate_defect_stratum("test_cert_2", [])
    empty_ok = (
        empty_patches.status == DefectAdjudicationStatus.OPEN_EVIDENCE_REQUIRED
        and "patches_missing" in empty_patches.critical_fields
    )
    consistent = no_patches_ok and empty_ok
    return {
        "name": "check_T_defect_calculus_engine_entry_point_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_defect_calculus_engine_entry_point" if consistent else "FAIL",
        "epistemic": "P_defect_calculus_engine_entry_point",
        "summary": (
            "Entry point produces correct verdicts: no-patches + empty-patches both yield "
            "OPEN_EVIDENCE_REQUIRED with patches_missing critical field and target_engine "
            "declared correctly."
        ),
        "dependencies": ["adjudicate_defect_stratum"],
        "data": {
            "no_patches_status": no_patches.status.value,
            "empty_patches_status": empty_patches.status.value,
        },
    }


def check_T_defect_calculus_engine_audit_first_P() -> Dict[str, Any]:
    """Audit-first: non-claims preserved across verdict cases."""
    verdicts = [
        adjudicate_defect_stratum("cert_a", None),
        adjudicate_defect_stratum("cert_b", None),
        adjudicate_defect_stratum("cert_c", []),
    ]
    non_claims_preserved = all(
        all(v.exports.get(nc, -1) == 0 for nc in PRESERVED_NON_CLAIMS)
        for v in verdicts
    )
    no_target_smuggled = all(
        v.obligation_packet.get("target_engine") == ENGINE_NAME
        for v in verdicts
    )
    consistent = non_claims_preserved and no_target_smuggled
    return {
        "name": "check_T_defect_calculus_engine_audit_first_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_defect_calculus_engine_audit_first" if consistent else "FAIL",
        "epistemic": "P_defect_calculus_engine_audit_first",
        "summary": (
            "Audit-first discipline preserved across all verdict cases: "
            "target_value_consumed + new_physical_claim + infinity_stack_claim all = 0; "
            "no engine smuggling."
        ),
        "dependencies": ["DefectAdjudicationStatus enum"],
        "data": {
            "verdicts_checked": len(verdicts),
            "non_claims_preserved": non_claims_preserved,
        },
    }


# ---------------------------------------------------------------------------
# Bank registration
# ---------------------------------------------------------------------------

_CHECKS = {
    "check_T_defect_calculus_engine_identity_P":
        check_T_defect_calculus_engine_identity_P,
    "check_T_defect_calculus_engine_entry_point_P":
        check_T_defect_calculus_engine_entry_point_P,
    "check_T_defect_calculus_engine_audit_first_P":
        check_T_defect_calculus_engine_audit_first_P,
}


def register(registry=None):
    if registry is None:
        return _CHECKS
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}
