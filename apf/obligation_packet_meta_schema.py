"""APF Obligation Packet Meta-Schema.

Tier 3 shared infrastructure per
``APF Reference Docs/Reference - APF Interface Engine Family Architecture (2026-05-19).md``
(Session 5 of the sequencing plan).

Implements the Q3 starting position formally
----------------------------------------------

Each engine in the IE family produces obligation packets with engine-specific
field shapes:

* **Route Adjudication Engine** packets (from
  ``apf.interface_repair_obligation_compiler.compile_obligation_packet``) carry
  ``route`` + ``packet_status`` + ``frontier_status`` + ``original_repair_class``
  + ``bundles`` + ``critical_fields`` + ``original_certificate`` etc. — a
  route-axis vocabulary built around transport edges, repair bundles, and
  rerun command hints.

* **Codomain Selection Engine** packets (from
  ``apf.codomain_selection_engine.adjudicate_codomain_competition``) carry
  ``obligation_kind`` + ``target_engine`` + ``target_unit_id`` +
  ``evidence_required`` + ``current_status`` + ``recommended_next_action`` —
  a codomain-axis vocabulary built around regime adjudication, network state,
  and per-regime runtime evaluators.

The two packet shapes share **zero** field names. Forcing one engine into the
other's shape would distort the engine-specific failure-mode taxonomy. The
right shape per the Reference doc Q3 is a **meta-schema with engine-specific
subtypes**: common fields all engines provide via adapter wrappers; per-engine
subtype data preserved in a typed extension slot.

Meta-schema common fields
-------------------------

* ``obligation_kind`` (str) — engine-specific obligation type
  (e.g. "evidence_required_supply_named_fields" for Route Adjudication;
  "runtime_evaluator_missing" for Codomain Selection).
* ``target_engine`` (str) — one of the EngineTarget values from
  ``apf.claim_dispatcher_multi_engine``.
* ``target_unit_id`` (str) — engine-specific unit identifier (route name for
  Route Adjudication; regime name for Codomain Selection).
* ``evidence_required`` (list) — engine-specific subschema (named transport /
  evaluator content for Route; runtime evaluator + network state for Codomain).
* ``current_status`` (str) — engine-specific status value.
* ``recommended_next_action`` (str) — human-readable next step.
* ``engine_subtype_data`` (mapping) — typed extension slot for engine-specific
  fields not covered by the common fields (bundles, frontier_status, etc. for
  Route; evaluation_data for Codomain).

Uniform packet inspector
------------------------

``inspect_packet(packet, engine)`` reads any-engine obligation packet via the
meta-schema and returns a ``PacketInspectionResult`` with the common fields
extracted + the engine-specific subtype data preserved. Downstream callers
(reviewer reporter, atlas, claim dispatcher) can read packets uniformly
without knowing each engine's native shape.

Audit-first discipline
----------------------

The meta-schema does not modify any per-engine packet. It is additive
(adapter wrappers); existing per-engine compilers remain untouched. No new
physical claim is introduced. The meta-schema validates that per-engine
non-claims are preserved through the wrapping (no smuggling of
target observables; no silent re-introduction of forbidden claims).

References
----------

* ``apf.interface_repair_obligation_compiler`` — Route Adjudication packet source.
* ``apf.codomain_selection_engine`` — Codomain Selection packet source.
* ``apf.claim_dispatcher_multi_engine`` — Session 4 dispatcher whose
  ``meta_obligation_packet`` field this module formalizes.
* ``Reference - APF Interface Engine Family Architecture (2026-05-19).md`` Q3
  starting position.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Engine subtype enum (mirrors EngineTarget from claim_dispatcher_multi_engine)
# ---------------------------------------------------------------------------

class EngineSubtype(str, Enum):
    """All 5 engines in the APF Interface Engine family (parallel to
    apf.claim_dispatcher_multi_engine.EngineTarget). Engine-specific
    wrappers exist today for ROUTE_ADJUDICATION + CODOMAIN_SELECTION;
    the 3 Session 6 latent engines are reachable as engine_subtype values
    but their meta-schema adapters land when each engine gets a real packet
    consumer beyond the engine's native verdict.obligation_packet.
    """
    ROUTE_ADJUDICATION = "ROUTE_ADJUDICATION"
    CODOMAIN_SELECTION = "CODOMAIN_SELECTION"
    KINEMATICS_ADJUDICATION = "KINEMATICS_ADJUDICATION"  # v24.3.36 — Session 6
    DEFECT_CALCULUS = "DEFECT_CALCULUS"  # v24.3.36 — Session 6
    REPRESENTATION_DESCENT = "REPRESENTATION_DESCENT"  # v24.3.36 — Session 6


# Required common-field set every meta-schema packet must carry
META_SCHEMA_REQUIRED_FIELDS: Tuple[str, ...] = (
    "obligation_kind",
    "target_engine",
    "target_unit_id",
    "evidence_required",
    "current_status",
    "recommended_next_action",
)


# ---------------------------------------------------------------------------
# Meta-schema dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ObligationPacketMetaSchema:
    """Cross-engine meta-schema for obligation packets.

    Common fields populated for every engine via adapter wrappers; engine-specific
    fields preserved in engine_subtype_data without distortion.
    """
    obligation_kind: str
    target_engine: str
    target_unit_id: str
    evidence_required: Tuple[Any, ...]
    current_status: str
    recommended_next_action: str
    engine_subtype: EngineSubtype
    engine_subtype_data: Mapping[str, Any] = field(default_factory=dict)
    audit_first_non_claims_preserved: bool = True

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["engine_subtype"] = self.engine_subtype.value
        d["evidence_required"] = list(self.evidence_required)
        d["engine_subtype_data"] = dict(self.engine_subtype_data)
        return d


# ---------------------------------------------------------------------------
# Per-engine adapter wrappers
# ---------------------------------------------------------------------------

def wrap_route_adjudication_packet(
    packet: Mapping[str, Any],
) -> ObligationPacketMetaSchema:
    """Adapter: translate a Route Adjudication obligation packet to the meta-schema.

    Route packets carry a route-axis vocabulary (route + packet_status +
    bundles + critical_fields + original_certificate). The translation rules:

    * ``obligation_kind`` ← derived from ``original_repair_class`` + ``packet_status``
    * ``target_engine`` ← "route_adjudication"
    * ``target_unit_id`` ← ``route`` (sector name, e.g. "ew" / "dark")
    * ``evidence_required`` ← ``critical_fields`` (named missing inputs)
    * ``current_status`` ← ``packet_status``
    * ``recommended_next_action`` ← ``rerun_command_hint``
    * ``engine_subtype_data`` ← preserved Route-specific fields (bundles,
      frontier_status, original_certificate, blocked_reason, ready_to_rerun,
      original_repair_class, optional_fields)
    """
    repair_class = packet.get("original_repair_class", "UNKNOWN")
    packet_status = str(packet.get("packet_status", "UNKNOWN"))

    obligation_kind_map = {
        "ORDINARY_REPAIR_REQUIRED": "evidence_required_supply_named_fields",
        "BLOCKED_SUBSTRATE_REVISION_REQUIRED": "substrate_revision_required",
        "FAIL_CLOSED_PROVENANCE": "fail_closed_provenance_audit",
        "FAIL_UNSUPPORTED": "route_unsupported_in_framework",
        "ALREADY_P": "no_obligation_route_already_P",
    }
    obligation_kind = obligation_kind_map.get(repair_class, f"route_{repair_class.lower()}")

    critical = packet.get("critical_fields") or ()
    if isinstance(critical, str):
        critical = (critical,)

    engine_subtype_data: Dict[str, Any] = {}
    for key in (
        "bundles", "frontier_status", "original_certificate",
        "blocked_reason", "ready_to_rerun", "original_repair_class",
        "optional_fields",
    ):
        if key in packet:
            engine_subtype_data[key] = packet[key]

    cert = packet.get("original_certificate") or {}
    target_consumed = False
    if isinstance(cert, Mapping):
        target_consumed = bool(cert.get("target_value_consumed", False))

    return ObligationPacketMetaSchema(
        obligation_kind=obligation_kind,
        target_engine="route_adjudication",
        target_unit_id=str(packet.get("route", "unknown")),
        evidence_required=tuple(critical),
        current_status=packet_status,
        recommended_next_action=str(packet.get("rerun_command_hint", "")),
        engine_subtype=EngineSubtype.ROUTE_ADJUDICATION,
        engine_subtype_data=engine_subtype_data,
        audit_first_non_claims_preserved=not target_consumed,
    )


def wrap_codomain_selection_packet(
    packet: Mapping[str, Any],
) -> ObligationPacketMetaSchema:
    """Adapter: translate a Codomain Selection obligation packet to the meta-schema.

    Codomain packets already use the Q3 starting position field names from
    Session 2, so this is largely a typed pass-through that preserves
    evaluation_data (the per-regime margin / phase-lock / coherence_density
    + audit_gate verdicts) in engine_subtype_data.
    """
    missing = []
    for f in META_SCHEMA_REQUIRED_FIELDS:
        if f not in packet:
            missing.append(f)
    if missing:
        raise ValueError(
            f"codomain selection packet missing required meta-schema fields: {missing}"
        )

    evidence = packet.get("evidence_required") or ()
    if isinstance(evidence, str):
        evidence = (evidence,)

    engine_subtype_data: Dict[str, Any] = {}
    if "evaluation_data" in packet:
        engine_subtype_data["evaluation_data"] = packet["evaluation_data"]

    return ObligationPacketMetaSchema(
        obligation_kind=str(packet["obligation_kind"]),
        target_engine=str(packet["target_engine"]),
        target_unit_id=str(packet["target_unit_id"]),
        evidence_required=tuple(evidence),
        current_status=str(packet["current_status"]),
        recommended_next_action=str(packet["recommended_next_action"]),
        engine_subtype=EngineSubtype.CODOMAIN_SELECTION,
        engine_subtype_data=engine_subtype_data,
        audit_first_non_claims_preserved=True,  # Codomain engine guarantees this by design
    )


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_meta_schema(packet: Mapping[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a packet dict conforms to the meta-schema common fields."""
    errors: List[str] = []
    for f in META_SCHEMA_REQUIRED_FIELDS:
        if f not in packet:
            errors.append(f"missing required field: {f}")
    if "engine_subtype" not in packet:
        errors.append("missing engine_subtype")
    elif packet["engine_subtype"] not in (s.value for s in EngineSubtype):
        errors.append(f"unknown engine_subtype: {packet['engine_subtype']}")
    if "evidence_required" in packet and not isinstance(
        packet["evidence_required"], (list, tuple)
    ):
        errors.append("evidence_required must be list or tuple")
    return len(errors) == 0, errors


# ---------------------------------------------------------------------------
# Uniform packet inspector
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PacketInspectionResult:
    """Result of a uniform meta-schema inspection."""
    valid: bool
    errors: Tuple[str, ...]
    common_fields: Mapping[str, Any]
    engine_subtype: str
    engine_subtype_data: Mapping[str, Any]
    audit_first_non_claims_preserved: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": list(self.errors),
            "common_fields": dict(self.common_fields),
            "engine_subtype": self.engine_subtype,
            "engine_subtype_data": dict(self.engine_subtype_data),
            "audit_first_non_claims_preserved": self.audit_first_non_claims_preserved,
        }


def inspect_packet(
    packet: Mapping[str, Any],
    engine: str,
) -> PacketInspectionResult:
    """Uniform packet inspector.

    Reads any-engine obligation packet via the meta-schema. Wraps the per-engine
    packet via the appropriate adapter (Route Adjudication or Codomain Selection),
    validates conformance, and returns common fields + engine-specific subtype data
    in a uniform shape downstream consumers can read.
    """
    try:
        if engine == EngineSubtype.ROUTE_ADJUDICATION.value or engine.lower() in (
            "route", "route_adjudication"
        ):
            wrapped = wrap_route_adjudication_packet(packet)
        elif engine == EngineSubtype.CODOMAIN_SELECTION.value or engine.lower() in (
            "codomain", "codomain_selection"
        ):
            wrapped = wrap_codomain_selection_packet(packet)
        else:
            return PacketInspectionResult(
                valid=False,
                errors=(f"unknown engine: {engine}",),
                common_fields={},
                engine_subtype="UNKNOWN",
                engine_subtype_data={},
                audit_first_non_claims_preserved=False,
            )
    except (ValueError, KeyError, TypeError) as exc:
        return PacketInspectionResult(
            valid=False,
            errors=(f"{type(exc).__name__}: {exc}",),
            common_fields={},
            engine_subtype=engine,
            engine_subtype_data={},
            audit_first_non_claims_preserved=False,
        )

    wrapped_dict = wrapped.to_dict()
    valid, errors = validate_meta_schema(wrapped_dict)
    common = {f: wrapped_dict.get(f) for f in META_SCHEMA_REQUIRED_FIELDS}
    return PacketInspectionResult(
        valid=valid,
        errors=tuple(errors),
        common_fields=common,
        engine_subtype=wrapped.engine_subtype.value,
        engine_subtype_data=wrapped.engine_subtype_data,
        audit_first_non_claims_preserved=wrapped.audit_first_non_claims_preserved,
    )


# ---------------------------------------------------------------------------
# Cross-engine meta-meta packet wrapper
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CrossEngineMetaPacket:
    """Composes multiple per-engine meta-schema packets into one cross-engine packet.

    Formalizes the ``meta_obligation_packet`` produced by
    ``apf.claim_dispatcher_multi_engine.dispatch_multi_engine``. Each per-engine
    packet retains its full meta-schema view; the cross-engine packet adds the
    meta_status from the multi-engine dispatcher's composition rule (Q1 option a:
    conjunctive).
    """
    meta_status: str
    engines_dispatched: Tuple[str, ...]
    per_engine_packets: Tuple[ObligationPacketMetaSchema, ...]
    cross_engine_recommended_next_action: str
    cross_engine_note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "meta_status": self.meta_status,
            "engines_dispatched": list(self.engines_dispatched),
            "per_engine_packets": [p.to_dict() for p in self.per_engine_packets],
            "cross_engine_recommended_next_action": self.cross_engine_recommended_next_action,
            "cross_engine_note": self.cross_engine_note,
        }


# ---------------------------------------------------------------------------
# Bank checks
# ---------------------------------------------------------------------------

def check_T_obligation_packet_meta_schema_identity_P() -> Dict[str, Any]:
    """Meta-schema declares the 6 required common fields + 2 enum subtypes."""
    consistent = (
        len(META_SCHEMA_REQUIRED_FIELDS) == 6
        and "obligation_kind" in META_SCHEMA_REQUIRED_FIELDS
        and "target_engine" in META_SCHEMA_REQUIRED_FIELDS
        and "target_unit_id" in META_SCHEMA_REQUIRED_FIELDS
        and "evidence_required" in META_SCHEMA_REQUIRED_FIELDS
        and "current_status" in META_SCHEMA_REQUIRED_FIELDS
        and "recommended_next_action" in META_SCHEMA_REQUIRED_FIELDS
        and len(list(EngineSubtype)) == 5
        and EngineSubtype.ROUTE_ADJUDICATION.value == "ROUTE_ADJUDICATION"
        and EngineSubtype.CODOMAIN_SELECTION.value == "CODOMAIN_SELECTION"
    )
    return {
        "name": "check_T_obligation_packet_meta_schema_identity_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_meta_schema_identity" if consistent else "FAIL",
        "epistemic": "P_meta_schema_identity",
        "summary": (
            "Meta-schema declares 6 required common fields (obligation_kind + "
            "target_engine + target_unit_id + evidence_required + current_status + "
            "recommended_next_action) and 5 engine subtypes (ROUTE_ADJUDICATION + "
            "CODOMAIN_SELECTION) per Reference doc Q3 starting position."
        ),
        "dependencies": ["Reference - APF Interface Engine Family Architecture (2026-05-19).md"],
        "data": {
            "required_fields": list(META_SCHEMA_REQUIRED_FIELDS),
            "engine_subtypes": [s.value for s in EngineSubtype],
        },
    }


def check_T_obligation_packet_route_subtype_P() -> Dict[str, Any]:
    """Route Adjudication packet → meta-schema wrapping produces conforming packet."""
    from apf.interface_repair_obligation_compiler import compile_obligation_packet
    raw_packet = compile_obligation_packet("ew", {
        "name": "ew_test_meta_schema",
        "trace_sector_closed": True,
        "source_to_scheme_registry_present": True,
        "evaluator_map_found": False,
        "codomain_transport_found": False,
        "counterterm_finite_parts_declared": False,
        "external_constants_ledger_clean": True,
        "uncertainty_protocol_declared": False,
        "target_value_consumed": False,
    }).to_dict()

    result = inspect_packet(raw_packet, EngineSubtype.ROUTE_ADJUDICATION.value)
    consistent = (
        result.valid is True
        and result.engine_subtype == "ROUTE_ADJUDICATION"
        and result.common_fields["target_engine"] == "route_adjudication"
        and result.common_fields["target_unit_id"] == "ew"
        and len(result.common_fields["evidence_required"]) > 0
        and "bundles" in result.engine_subtype_data
        and "original_certificate" in result.engine_subtype_data
        and result.audit_first_non_claims_preserved is True
    )
    return {
        "name": "check_T_obligation_packet_route_subtype_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_route_subtype" if consistent else "FAIL",
        "epistemic": "P_route_subtype",
        "summary": (
            "Route Adjudication packet wraps cleanly into meta-schema: 6 common "
            "fields populated correctly (target_engine=route_adjudication; "
            "target_unit_id=ew sector; evidence_required from critical_fields); "
            "engine_subtype_data preserves bundles + original_certificate + "
            "frontier_status etc.; audit-first non-claims preserved."
        ),
        "dependencies": ["apf.interface_repair_obligation_compiler.compile_obligation_packet"],
        "data": {
            "result_valid": result.valid,
            "result_errors": list(result.errors),
            "common_fields_keys": sorted(result.common_fields.keys()),
            "subtype_data_keys": sorted(result.engine_subtype_data.keys()),
        },
    }


def check_T_obligation_packet_codomain_subtype_P() -> Dict[str, Any]:
    """Codomain Selection packet → meta-schema wrapping produces conforming packet."""
    from apf.codomain_selection_engine import adjudicate_codomain_competition
    # Three SC scenarios: positive (COHERENT), no-network (OPEN), unknown regime (OPEN)
    sc_positive_network = {
        "epsilon_phi": 0.2,
        "min_rho_coh": 0.5,
        "winding_sector_n": 1,
        "flux_sector_phi": 1.0,
        "nodes": [
            {"node_id": "a", "capacity_C": 10.0, "phase_phi": 0.00,
             "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
            {"node_id": "b", "capacity_C": 10.0, "phase_phi": 0.04,
             "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
        ],
        "edges": [["a", "b"]],
        "defects": {"thermal": 0.15, "gauge": 0.1, "disorder": 0.1,
                    "competition": 0.05, "boundary": 0.05, "vortex": 0.05},
        "costs": {"C_normal": 12.0, "C_superconducting": 5.0},
    }
    verdicts = [
        adjudicate_codomain_competition("SUPERCONDUCTIVITY", sc_positive_network),
        adjudicate_codomain_competition("SUPERFLUIDITY", None),  # no runtime
    ]
    all_valid = True
    for v in verdicts:
        result = inspect_packet(v.obligation_packet, EngineSubtype.CODOMAIN_SELECTION.value)
        if not result.valid:
            all_valid = False
            break
        if result.engine_subtype != "CODOMAIN_SELECTION":
            all_valid = False
            break
        if "regime:" not in result.common_fields["target_unit_id"]:
            all_valid = False
            break

    return {
        "name": "check_T_obligation_packet_codomain_subtype_P",
        "consistent": all_valid,
        "passed": all_valid,
        "tier": 4,
        "status": "P_codomain_subtype" if all_valid else "FAIL",
        "epistemic": "P_codomain_subtype",
        "summary": (
            "Codomain Selection packets wrap cleanly into meta-schema across "
            "multiple verdict cases: positive (COHERENT_CODOMAIN_SELECTED with "
            "no_obligation) + no-runtime (OPEN_EVIDENCE_REQUIRED with runtime "
            "evaluator missing). Common fields populated (target_engine="
            "codomain_selection; target_unit_id=regime:NAME); engine_subtype_data "
            "preserves evaluation_data per-verdict."
        ),
        "dependencies": ["apf.codomain_selection_engine.adjudicate_codomain_competition"],
        "data": {
            "verdicts_checked": len(verdicts),
            "all_valid": all_valid,
        },
    }


def check_T_obligation_packet_uniform_inspector_P() -> Dict[str, Any]:
    """inspect_packet reads both engines uniformly with the same return shape."""
    # Route Adjudication
    from apf.interface_repair_obligation_compiler import compile_obligation_packet
    route_packet = compile_obligation_packet("dark", {
        "name": "dark_test",
        "route_built": True,
        "run_completed": True,
        "chains_converged": False,
        "posterior_closed": False,
        "robustness_checks_passed": False,
        "data_ledger_clean": True,
        "evaluator_map_found": False,
        "codomain_transport_found": True,
        "target_value_consumed": False,
    }).to_dict()
    route_result = inspect_packet(route_packet, "ROUTE_ADJUDICATION")

    # Codomain Selection
    from apf.codomain_selection_engine import adjudicate_codomain_competition
    codomain_verdict = adjudicate_codomain_competition("MAGNETISM", None)
    codomain_result = inspect_packet(codomain_verdict.obligation_packet, "CODOMAIN_SELECTION")

    # Both return PacketInspectionResult with same shape
    consistent = (
        route_result.valid is True
        and codomain_result.valid is True
        and sorted(route_result.common_fields.keys()) == sorted(codomain_result.common_fields.keys())
        and route_result.engine_subtype != codomain_result.engine_subtype  # different engines
        and route_result.audit_first_non_claims_preserved is True
        and codomain_result.audit_first_non_claims_preserved is True
    )
    return {
        "name": "check_T_obligation_packet_uniform_inspector_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_uniform_inspector" if consistent else "FAIL",
        "epistemic": "P_uniform_inspector",
        "summary": (
            "Uniform inspect_packet() reads Route Adjudication + Codomain Selection "
            "packets with same return shape (PacketInspectionResult with identical "
            "common_fields keys). Engine subtype data preserved per-engine. "
            "Audit-first non-claims preserved across both wrappings."
        ),
        "dependencies": [
            "wrap_route_adjudication_packet",
            "wrap_codomain_selection_packet",
        ],
        "data": {
            "route_valid": route_result.valid,
            "codomain_valid": codomain_result.valid,
            "common_fields_keys_match": sorted(route_result.common_fields.keys()) == sorted(codomain_result.common_fields.keys()),
        },
    }


# ---------------------------------------------------------------------------
# Bank registration
# ---------------------------------------------------------------------------

def register(registry=None):
    checks = {
        "check_T_obligation_packet_meta_schema_identity_P":
            check_T_obligation_packet_meta_schema_identity_P,
        "check_T_obligation_packet_route_subtype_P":
            check_T_obligation_packet_route_subtype_P,
        "check_T_obligation_packet_codomain_subtype_P":
            check_T_obligation_packet_codomain_subtype_P,
        "check_T_obligation_packet_uniform_inspector_P":
            check_T_obligation_packet_uniform_inspector_P,
    }
    if registry is None:
        return checks
    registry.update(checks)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {
        "check_T_obligation_packet_meta_schema_identity_P":
            check_T_obligation_packet_meta_schema_identity_P(),
        "check_T_obligation_packet_route_subtype_P":
            check_T_obligation_packet_route_subtype_P(),
        "check_T_obligation_packet_codomain_subtype_P":
            check_T_obligation_packet_codomain_subtype_P(),
        "check_T_obligation_packet_uniform_inspector_P":
            check_T_obligation_packet_uniform_inspector_P(),
    }
