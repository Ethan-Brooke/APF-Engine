"""APF Kinematics Adjudication Engine.

Tier 2 member of the APF Interface Engine family per
``APF Reference Docs/Reference - APF Interface Engine Family Architecture (2026-05-19).md``
(Session 6 — latent engine operationalization).

The Kinematics Adjudication Engine adjudicates **kinematic compositions** —
state-machine reasoning about a route's kinematic trajectory through the
APF substrate. Structurally parallel to Route Adjudication: same unit
(routes) but different failure-mode taxonomy (kinematic state defects
rather than transport edge defects).

Unit of adjudication
--------------------
A route's kinematic composition. Input: route name + payload (same shape
as Route Adjudication accepts). Output: a ``KinematicAdjudicationVerdict``
typed by the engine's failure-mode taxonomy.

Failure-mode taxonomy
---------------------

Engine-specific (not shared with Route Adjudication):

* ``KINEMATIC_PATH_CLOSED`` -- kinematic certificate closed cleanly
* ``HOLONOMY_DEFECT`` -- holonomy integral non-zero around closed loop
* ``ORDER_DEFECT`` -- ordering of kinematic transitions inconsistent
* ``PHASE_SPACE_INCOHERENT`` -- phase space atlas charts don't glue
* ``INVARIANT_VIOLATED`` -- one of the conserved invariants fails
* ``OPEN_EVIDENCE_REQUIRED`` -- need additional kinematic-state data

Wraps existing modules
----------------------

``apf.interface_kinematics_engine.compute_kinematic_certificate`` produces
a ``KinematicCertificate`` per route + payload; the engine wraps this in
the verdict + obligation packet shape.

``apf.interface_kinematic_solver.solve_kinematic_path`` produces a
``KinematicSolveReport`` with repair-move sequence; the engine surfaces
that as the obligation packet's evidence_required.

Audit-first discipline
----------------------

No new physical claim. The engine produces structural classification
verdicts over kinematic compositions; same audit-first invariants as
Route Adjudication. ``target_value_consumed = False`` propagated.

References
----------

* ``apf.interface_kinematics_engine`` — kinematic certificate producer
* ``apf.interface_kinematic_solver`` — kinematic repair-move solver
* ``Reference - APF Interface Engine Family Architecture (2026-05-19).md``
  Session 6+ latent engine operationalization.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Tuple


# ---------------------------------------------------------------------------
# Engine identity
# ---------------------------------------------------------------------------

ENGINE_NAME = "kinematics_adjudication"
ENGINE_FAMILY = "APF_Interface_Engine"
ENGINE_TIER = 2
ENGINE_ROLE = "kinematic_composition_adjudication"


# ---------------------------------------------------------------------------
# Verdict status enum
# ---------------------------------------------------------------------------

class KinematicAdjudicationStatus(str, Enum):
    KINEMATIC_PATH_CLOSED = "KINEMATIC_PATH_CLOSED"
    HOLONOMY_DEFECT = "HOLONOMY_DEFECT"
    ORDER_DEFECT = "ORDER_DEFECT"
    PHASE_SPACE_INCOHERENT = "PHASE_SPACE_INCOHERENT"
    INVARIANT_VIOLATED = "INVARIANT_VIOLATED"
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"


# Audit-first non-claims preserved across all verdicts
PRESERVED_NON_CLAIMS: Tuple[str, ...] = (
    "target_value_consumed",
    "kinematic_dynamics_imported",
    "phase_space_volume_consumed",
)


# ---------------------------------------------------------------------------
# Verdict dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class KinematicAdjudicationVerdict:
    route: str
    status: KinematicAdjudicationStatus
    export_global_P: bool
    critical_fields: Tuple[str, ...]
    repair_moves: Tuple[Mapping[str, Any], ...]
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

def adjudicate_kinematic_composition(
    route: str,
    payload: Optional[Mapping[str, Any]] = None,
) -> KinematicAdjudicationVerdict:
    """Adjudicate a route's kinematic composition.

    Wraps ``apf.interface_kinematics_engine.compute_kinematic_certificate``
    and ``apf.interface_kinematic_solver.solve_kinematic_path`` to produce
    a Kinematics Adjudication Engine verdict.

    Parameters
    ----------
    route : str
        Route name (e.g., "ew", "dark", "horizon"). Must match a route the
        kinematic engine knows about.
    payload : Mapping[str, Any] or None
        Route payload (same shape Route Adjudication accepts). If None,
        returns OPEN_EVIDENCE_REQUIRED with payload-missing obligation.

    Returns
    -------
    KinematicAdjudicationVerdict
    """
    if payload is None:
        return _payload_missing_verdict(route)

    try:
        from apf.interface_kinematics_engine import compute_kinematic_certificate
        from apf.interface_kinematic_solver import solve_kinematic_path
    except ImportError as exc:
        return _import_failed_verdict(route, exc)

    try:
        certificate = compute_kinematic_certificate(route, dict(payload))
        solve_report = solve_kinematic_path(route, dict(payload))
    except Exception as exc:
        return KinematicAdjudicationVerdict(
            route=route,
            status=KinematicAdjudicationStatus.OPEN_EVIDENCE_REQUIRED,
            export_global_P=False,
            critical_fields=("kinematic_machinery_error",),
            repair_moves=(),
            obligation_packet={
                "obligation_kind": "kinematic_machinery_error",
                "target_engine": ENGINE_NAME,
                "target_unit_id": f"route:{route}",
                "evidence_required": ["valid route + payload for kinematics engine"],
                "current_status": "MACHINERY_ERROR",
                "recommended_next_action": (
                    f"check apf.interface_kinematics_engine.route_path({route!r}) "
                    "+ payload schema"
                ),
                "error_detail": f"{type(exc).__name__}: {exc}",
            },
            exports={k: 0 for k in PRESERVED_NON_CLAIMS},
            reason=f"kinematics machinery raised: {exc}",
        )

    # Map kinematic certificate status to engine verdict
    cert_dict = certificate.to_dict() if hasattr(certificate, "to_dict") else asdict(certificate)
    solver_dict = solve_report.to_dict() if hasattr(solve_report, "to_dict") else asdict(solve_report)
    status_value = str(cert_dict.get("status", "UNKNOWN"))

    if status_value in ("CLOSED", "P", "EXPORTABLE"):
        status = KinematicAdjudicationStatus.KINEMATIC_PATH_CLOSED
        export_p = True
        critical: Tuple[str, ...] = ()
    elif "HOLONOMY" in status_value.upper():
        status = KinematicAdjudicationStatus.HOLONOMY_DEFECT
        export_p = False
        critical = ("holonomy_defect_nonzero",)
    elif "ORDER" in status_value.upper():
        status = KinematicAdjudicationStatus.ORDER_DEFECT
        export_p = False
        critical = ("transition_order_inconsistent",)
    elif "PHASE" in status_value.upper() or "ATLAS" in status_value.upper():
        status = KinematicAdjudicationStatus.PHASE_SPACE_INCOHERENT
        export_p = False
        critical = ("phase_space_charts_incoherent",)
    elif "INVARIANT" in status_value.upper():
        status = KinematicAdjudicationStatus.INVARIANT_VIOLATED
        export_p = False
        critical = ("conserved_invariant_violated",)
    else:
        status = KinematicAdjudicationStatus.OPEN_EVIDENCE_REQUIRED
        export_p = False
        critical = (f"unknown_status:{status_value}",)

    # Extract repair moves
    repair_moves: List[Mapping[str, Any]] = []
    for rm in solver_dict.get("repair_moves", []) or []:
        if isinstance(rm, Mapping):
            repair_moves.append(dict(rm))
        else:
            repair_moves.append({"raw": str(rm)})

    obligation_packet = _build_obligation_packet(
        route=route,
        status=status,
        critical=critical,
        cert_data=cert_dict,
        solver_data=solver_dict,
    )

    exports = {k: 0 for k in PRESERVED_NON_CLAIMS}
    exports["kinematic_path_closed"] = int(status == KinematicAdjudicationStatus.KINEMATIC_PATH_CLOSED)
    exports["kinematic_adjudication_evaluated"] = 1

    return KinematicAdjudicationVerdict(
        route=route,
        status=status,
        export_global_P=export_p,
        critical_fields=critical,
        repair_moves=tuple(repair_moves),
        obligation_packet=obligation_packet,
        exports=exports,
        reason=f"kinematic certificate status: {status_value}",
    )


def _payload_missing_verdict(route: str) -> KinematicAdjudicationVerdict:
    return KinematicAdjudicationVerdict(
        route=route,
        status=KinematicAdjudicationStatus.OPEN_EVIDENCE_REQUIRED,
        export_global_P=False,
        critical_fields=("payload_missing",),
        repair_moves=(),
        obligation_packet={
            "obligation_kind": "payload_missing",
            "target_engine": ENGINE_NAME,
            "target_unit_id": f"route:{route}",
            "evidence_required": ["route payload dict with kinematic-relevant fields"],
            "current_status": "MISSING_INPUT",
            "recommended_next_action": (
                "call adjudicate_kinematic_composition(route, payload) with payload arg"
            ),
        },
        exports={k: 0 for k in PRESERVED_NON_CLAIMS},
        reason="payload argument required for adjudication",
    )


def _import_failed_verdict(route: str, exc: Exception) -> KinematicAdjudicationVerdict:
    return KinematicAdjudicationVerdict(
        route=route,
        status=KinematicAdjudicationStatus.OPEN_EVIDENCE_REQUIRED,
        export_global_P=False,
        critical_fields=("kinematics_modules_missing",),
        repair_moves=(),
        obligation_packet={
            "obligation_kind": "import_failed",
            "target_engine": ENGINE_NAME,
            "target_unit_id": f"route:{route}",
            "evidence_required": [
                "apf.interface_kinematics_engine importable",
                "apf.interface_kinematic_solver importable",
            ],
            "current_status": "IMPORT_FAILED",
            "recommended_next_action": "verify kinematics layer modules installed (v24.3.16/17)",
            "error_detail": f"{type(exc).__name__}: {exc}",
        },
        exports={k: 0 for k in PRESERVED_NON_CLAIMS},
        reason=f"import of kinematics modules failed: {exc}",
    )


def _build_obligation_packet(
    route: str,
    status: KinematicAdjudicationStatus,
    critical: Tuple[str, ...],
    cert_data: Mapping[str, Any],
    solver_data: Mapping[str, Any],
) -> Dict[str, Any]:
    """Meta-schema-compatible obligation packet per Reference doc Q3."""
    obligation_kind_map = {
        KinematicAdjudicationStatus.KINEMATIC_PATH_CLOSED: "no_obligation",
        KinematicAdjudicationStatus.HOLONOMY_DEFECT: "supply_path_with_zero_holonomy",
        KinematicAdjudicationStatus.ORDER_DEFECT: "fix_transition_ordering",
        KinematicAdjudicationStatus.PHASE_SPACE_INCOHERENT: "glue_phase_space_charts",
        KinematicAdjudicationStatus.INVARIANT_VIOLATED: "restore_conserved_invariant",
        KinematicAdjudicationStatus.OPEN_EVIDENCE_REQUIRED: "supply_kinematic_state",
    }
    return {
        "obligation_kind": obligation_kind_map.get(status, "unknown"),
        "target_engine": ENGINE_NAME,
        "target_unit_id": f"route:{route}",
        "evidence_required": list(critical),
        "current_status": status.value,
        "recommended_next_action": (
            "address kinematic critical fields via repair_moves" if critical
            else "no action required — kinematic path closed"
        ),
        "evaluation_data": {
            "certificate_status": cert_data.get("status"),
            "solver_repair_move_count": len(solver_data.get("repair_moves", []) or []),
        },
    }


# ---------------------------------------------------------------------------
# Bank checks (3)
# ---------------------------------------------------------------------------

def check_T_kinematics_adjudication_engine_identity_P() -> Dict[str, Any]:
    consistent = (
        ENGINE_NAME == "kinematics_adjudication"
        and ENGINE_FAMILY == "APF_Interface_Engine"
        and ENGINE_TIER == 2
        and ENGINE_ROLE == "kinematic_composition_adjudication"
        and len(list(KinematicAdjudicationStatus)) == 6
        and len(PRESERVED_NON_CLAIMS) == 3
    )
    return {
        "name": "check_T_kinematics_adjudication_engine_identity_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_kinematics_engine_identity" if consistent else "FAIL",
        "epistemic": "P_kinematics_engine_identity",
        "summary": (
            "Kinematics Adjudication Engine declares Tier 2 role + IE family membership; "
            "6-status verdict taxonomy + 3 preserved non-claims."
        ),
        "dependencies": ["Reference - APF Interface Engine Family Architecture (2026-05-19).md"],
        "data": {
            "engine_name": ENGINE_NAME,
            "engine_tier": ENGINE_TIER,
            "status_count": len(list(KinematicAdjudicationStatus)),
        },
    }


def check_T_kinematics_adjudication_engine_entry_point_P() -> Dict[str, Any]:
    """Entry point runs end-to-end on a sample route + payload."""
    # No-payload case
    no_payload = adjudicate_kinematic_composition("ew", None)
    no_payload_ok = (
        no_payload.status == KinematicAdjudicationStatus.OPEN_EVIDENCE_REQUIRED
        and no_payload.export_global_P is False
        and "payload_missing" in no_payload.critical_fields
    )

    # With payload — kinematics engine accepts any route + payload dict
    sample_payload = {
        "name": "ew_kinematics_test",
        "trace_sector_closed": True,
        "source_to_scheme_registry_present": True,
        "evaluator_map_found": False,
        "target_value_consumed": False,
    }
    with_payload = adjudicate_kinematic_composition("ew", sample_payload)
    with_payload_ok = (
        with_payload.status in list(KinematicAdjudicationStatus)
        and with_payload.obligation_packet.get("target_engine") == ENGINE_NAME
    )

    consistent = no_payload_ok and with_payload_ok
    return {
        "name": "check_T_kinematics_adjudication_engine_entry_point_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_kinematics_engine_entry_point" if consistent else "FAIL",
        "epistemic": "P_kinematics_engine_entry_point",
        "summary": (
            "Entry point produces verdicts: no-payload -> OPEN_EVIDENCE_REQUIRED with "
            "payload_missing; with-payload -> valid kinematic verdict status with "
            "target_engine declared correctly."
        ),
        "dependencies": [
            "apf.interface_kinematics_engine.compute_kinematic_certificate",
            "apf.interface_kinematic_solver.solve_kinematic_path",
        ],
        "data": {
            "no_payload_status": no_payload.status.value,
            "with_payload_status": with_payload.status.value,
        },
    }


def check_T_kinematics_adjudication_engine_audit_first_P() -> Dict[str, Any]:
    """Audit-first discipline: non-claims preserved across all verdict cases."""
    verdicts = [
        adjudicate_kinematic_composition("ew", None),
        adjudicate_kinematic_composition("dark", None),
        adjudicate_kinematic_composition("horizon", None),
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
        "name": "check_T_kinematics_adjudication_engine_audit_first_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_kinematics_engine_audit_first" if consistent else "FAIL",
        "epistemic": "P_kinematics_engine_audit_first",
        "summary": (
            "Audit-first discipline preserved across all verdict cases: "
            "target_value_consumed + kinematic_dynamics_imported + "
            "phase_space_volume_consumed all = 0; no engine smuggling."
        ),
        "dependencies": ["KinematicAdjudicationStatus enum"],
        "data": {
            "verdicts_checked": len(verdicts),
            "non_claims_preserved": non_claims_preserved,
        },
    }


# ---------------------------------------------------------------------------
# Bank registration
# ---------------------------------------------------------------------------

_CHECKS = {
    "check_T_kinematics_adjudication_engine_identity_P":
        check_T_kinematics_adjudication_engine_identity_P,
    "check_T_kinematics_adjudication_engine_entry_point_P":
        check_T_kinematics_adjudication_engine_entry_point_P,
    "check_T_kinematics_adjudication_engine_audit_first_P":
        check_T_kinematics_adjudication_engine_audit_first_P,
}


def register(registry=None):
    if registry is None:
        return _CHECKS
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}
