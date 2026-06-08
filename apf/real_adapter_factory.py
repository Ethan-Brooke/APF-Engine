"""
APF Real Adapter Factory.

Compresses the 600-line wire-in adapter pattern (snapshot dataclass + payload
builder + Engine pipeline runner + 6 register checks + register fn) into a
generic 8-field `RealAdapterSnapshot` base + a `make_check_set` factory that
generates the 6 standard register checks for any adapter.

The factory does NOT change the framework's audit-first discipline. Every
adapter built via the factory still:

- Defaults `target_value_consumed = False` (no smuggling).
- Declares an external evaluator ledger explicitly (REQUIRED_LEDGER per route).
- Names forbidden input keys explicitly (TARGET_KEYS per route).
- Promotes the route to the **imported-one-route** gate level only.
  Engine `SOLVED_GLOBAL_P` is gate-relative; the adapter does not lift
  the route to APF-internal-derivation status.

What the factory replaces
-------------------------
Each pre-factory adapter (light_quark_real_adapter, ew_dizet_real_adapter,
dark_apf2_real_adapter, charged_lepton_qed_real_adapter) hand-rolled ~600 lines
of nearly-identical structure. The differences across adapters were the banked
content constants, the snapshot field names, the check-name prefix, the 1-3
sector-specific extension fields, and the no-smuggling key set.

A factory-built adapter is 80-150 lines: banked content + snapshot factory +
optional evaluator-consistency check + a single `make_check_set` call +
register() boilerplate.

What the factory preserves
--------------------------
- Each check carries its own name and status string (e.g. "P_real_adapter",
  "P_v161_baseline_reproduced", "P_external_ledger_declared"). The factory
  parameterises the prefix; the check structure (consistent + status +
  summary + data) is identical across adapters.
- Engine pipeline traversal: `discover_and_certify` -> `movement_graph_report`
  -> `explore_repair_frontier` -> `compile_obligation_packet` ->
  `evidence_template` -> `control_evidence_rerun`.
- No-smuggling guard runs against the union of TARGET_KEYS and the snapshot's
  `target_value_consumed` flag.
- 6-check set per adapter:
    check_T_<name>_adapter_payload_contract_P
    check_T_<name>_adapter_evaluator_consistent_P (optional, opt-in)
    check_T_<name>_adapter_no_smuggling_P
    check_T_<name>_adapter_external_ledger_declared_P
    check_T_<name>_adapter_certification_P
    check_T_<name>_real_adapter_P (top integration)

Adapters that want a richer snapshot (sector-specific extension fields,
typed booleans beyond the 8-field standard) can still use a custom dataclass;
the factory only requires `.to_payload(name)` and the standard 8 boolean
fields are accessible from the payload dict.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, FrozenSet, List, Mapping, Optional, Tuple

try:
    from apf.interface_structure_discovery_engine import discover_and_certify
    from apf.interface_structure_movement_graph import movement_graph_report
    from apf.interface_repair_frontier_explorer import explore_repair_frontier
    from apf.interface_repair_obligation_compiler import (
        compile_obligation_packet,
        evidence_template,
    )
    from apf.interface_evidence_rerun_controller import control_evidence_rerun
except Exception as exc:  # pragma: no cover
    raise ImportError(
        f"real_adapter_factory requires the interface-intelligence stack: {exc}"
    ) from exc


# ============================================================================
# Standard 8-field snapshot
# ============================================================================

@dataclass(frozen=True)
class RealAdapterSnapshot:
    """Standard snapshot for any wire-in adapter.

    Eight boolean fields cover the EW + dark + horizon + capacity + gauge
    + provenance route certifiers. Sector-specific extension fields go into
    `extension_fields` as a free-form dict; they pass through into the payload
    but the factory's standard checks read only the 8 booleans + the
    `external_ledger_fields_declared` tuple.
    """
    trace_sector_closed: bool
    source_to_scheme_registry_present: bool
    evaluator_map_found: bool
    codomain_transport_found: bool
    counterterm_finite_parts_declared: bool
    external_constants_ledger_clean: bool
    uncertainty_protocol_declared: bool
    target_value_consumed: bool
    external_ledger_fields_declared: Tuple[str, ...] = ()
    notes: str = ""
    extension_fields: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self, name: str) -> Dict[str, Any]:
        """Build the route payload dict the Engine pipeline reads."""
        base = {
            "name": name,
            "trace_sector_closed": self.trace_sector_closed,
            "source_to_scheme_registry_present": self.source_to_scheme_registry_present,
            "evaluator_map_found": self.evaluator_map_found,
            "codomain_transport_found": self.codomain_transport_found,
            "counterterm_finite_parts_declared": self.counterterm_finite_parts_declared,
            "external_constants_ledger_clean": self.external_constants_ledger_clean,
            "uncertainty_protocol_declared": self.uncertainty_protocol_declared,
            "target_value_consumed": self.target_value_consumed,
            "notes": self.notes,
        }
        # Extension fields are merged but cannot overwrite the standard keys.
        for k, v in self.extension_fields.items():
            if k not in base:
                base[k] = v
        return base


# ============================================================================
# Adapter report (parallels per-adapter Report dataclasses pre-factory)
# ============================================================================

@dataclass(frozen=True)
class RealAdapterReport:
    """Engine-pipeline outputs for a single adapter invocation."""
    payload: Mapping[str, Any]
    snapshot: Any  # could be RealAdapterSnapshot or a sector-specific dataclass
    certification: Mapping[str, Any]
    movement_graph: Mapping[str, Any]
    frontier: Mapping[str, Any]
    obligation_packet: Mapping[str, Any]
    evidence_template: Mapping[str, Any]
    rerun_result_without_evidence: Mapping[str, Any]
    aux: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload": dict(self.payload),
            "snapshot": (asdict(self.snapshot)
                         if hasattr(self.snapshot, "__dataclass_fields__")
                         else dict(self.snapshot)),
            "certification": dict(self.certification),
            "movement_graph": dict(self.movement_graph),
            "frontier": dict(self.frontier),
            "obligation_packet": dict(self.obligation_packet),
            "evidence_template": dict(self.evidence_template),
            "rerun_result_without_evidence": dict(self.rerun_result_without_evidence),
            "aux": dict(self.aux),
        }


# ============================================================================
# Engine pipeline runner (replaces per-adapter build_adapter_report functions)
# ============================================================================

def build_adapter_report(
    snapshot: Any,
    *,
    name: str,
    route: str,
    aux: Optional[Mapping[str, Any]] = None,
) -> RealAdapterReport:
    """Run the full Engine pipeline on the snapshot's payload."""
    if not hasattr(snapshot, "to_payload"):
        raise TypeError(
            f"snapshot must have a to_payload(name) method; got {type(snapshot).__name__}"
        )
    payload = snapshot.to_payload(name=name)
    certification = discover_and_certify(route, payload)
    movement = movement_graph_report(route, payload)
    frontier = explore_repair_frontier(route, payload).to_dict()
    packet = compile_obligation_packet(route, payload)
    template = evidence_template(packet)
    rerun_without_evidence = control_evidence_rerun(route, payload).to_dict()
    return RealAdapterReport(
        payload=payload,
        snapshot=snapshot,
        certification=certification,
        movement_graph=movement,
        frontier=frontier,
        obligation_packet=packet.to_dict(),
        evidence_template=template,
        rerun_result_without_evidence=rerun_without_evidence,
        aux=dict(aux or {}),
    )


# ============================================================================
# Check factory (generates the 5 or 6 register checks per adapter)
# ============================================================================

def make_check_set(
    *,
    adapter_name: str,
    route: str,
    payload_name: str,
    snapshot_factory: Callable[[], Any],
    required_ledger_fields: Tuple[str, ...],
    target_value_keys: FrozenSet[str],
    evaluator_consistent_check: Optional[Callable[[], Dict[str, Any]]] = None,
) -> Dict[str, Callable[[], Dict[str, Any]]]:
    """Generate the standard check set for a real adapter.

    Parameters
    ----------
    adapter_name: short identifier used in check names, e.g. "ew_dizet" or
        "charm_msbar_rundec". The resulting check names follow the pattern
        check_T_<adapter_name>_adapter_*_P + check_T_<adapter_name>_real_adapter_P.
    route: Engine route label ("ew", "dark", "horizon", ...).
    payload_name: name to attach to the route payload when running the Engine
        pipeline.
    snapshot_factory: zero-arg callable returning the live snapshot to test.
    required_ledger_fields: tuple of strings naming the external evaluator
        ledger fields the adapter requires. The factory checks that the
        snapshot declares exactly these fields.
    target_value_keys: frozenset of payload-key names that must NEVER appear
        in the snapshot's payload (no-smuggling guard).
    evaluator_consistent_check: optional zero-arg callable for the sector-
        specific evaluator-consistency check. If None, only 5 checks are
        generated (payload_contract / no_smuggling / external_ledger_declared
        / certification / top integration).

    Returns
    -------
    Dict mapping check-function name to the zero-arg check function.
    """

    base = f"check_T_{adapter_name}_adapter"
    top_name = f"check_T_{adapter_name}_real_adapter_P"

    def check_payload_contract() -> Dict[str, Any]:
        snap = snapshot_factory()
        payload = snap.to_payload(name=payload_name)
        required_keys = {
            "name", "trace_sector_closed", "source_to_scheme_registry_present",
            "evaluator_map_found", "codomain_transport_found",
            "counterterm_finite_parts_declared", "external_constants_ledger_clean",
            "uncertainty_protocol_declared", "target_value_consumed", "notes",
        }
        has_all_keys = required_keys.issubset(payload.keys())
        no_smuggling = payload["target_value_consumed"] is False
        evaluator_filled = payload["evaluator_map_found"] is True
        codomain_filled = payload["codomain_transport_found"] is True
        ok = has_all_keys and no_smuggling and evaluator_filled and codomain_filled
        return {
            "name": f"{base}_payload_contract_P",
            "consistent": ok,
            "status": "P_real_adapter" if ok else "FAIL",
            "summary": (
                f"{adapter_name} adapter produces {route}-shaped route payload "
                f"with evaluator + codomain filled."
            ),
            "data": {
                "required_keys_present": has_all_keys,
                "no_smuggling": no_smuggling,
                "evaluator_filled": evaluator_filled,
                "codomain_filled": codomain_filled,
            },
        }

    def check_no_smuggling() -> Dict[str, Any]:
        snap = snapshot_factory()
        payload = snap.to_payload(name=payload_name)
        smuggled = [k for k in target_value_keys if k in payload]
        ok = (not smuggled) and (not payload["target_value_consumed"])
        return {
            "name": f"{base}_no_smuggling_P",
            "consistent": ok,
            "status": "P_no_smuggling" if ok else "FAIL",
            "summary": (
                f"No forbidden target-value key in {adapter_name} payload; "
                f"target_value_consumed=False."
            ),
            "data": {
                "smuggled_keys": smuggled,
                "target_value_consumed": payload["target_value_consumed"],
                "forbidden_keys_count": len(target_value_keys),
            },
        }

    def check_external_ledger_declared() -> Dict[str, Any]:
        snap = snapshot_factory()
        declared = set(snap.external_ledger_fields_declared)
        required = set(required_ledger_fields)
        ok = declared == required
        return {
            "name": f"{base}_external_ledger_declared_P",
            "consistent": ok,
            "status": "P_external_ledger_declared" if ok else "FAIL",
            "summary": (
                f"All {len(required)} required external evaluator ledger fields "
                f"declared on the {adapter_name} snapshot."
            ),
            "data": {
                "declared_count": len(declared),
                "required_count": len(required),
                "missing": sorted(required - declared),
                "unexpected": sorted(declared - required),
            },
        }

    def check_certification() -> Dict[str, Any]:
        snap = snapshot_factory()
        report = build_adapter_report(snap, name=payload_name, route=route)
        packet_status = report.obligation_packet.get("packet_status")
        rerun_status = report.rerun_result_without_evidence.get("status")
        edges = report.movement_graph.get("edges", [])
        evaluator_edge = next(
            (e for e in edges if e.get("kind") == "EVALUATOR_MAP"),
            None,
        )
        evaluator_filled = evaluator_edge is not None and evaluator_edge.get("status") in (
            "MOVES_CLEANLY", "PRESENT_STABLE",
        )
        return {
            "name": f"{base}_certification_P",
            "consistent": evaluator_filled,
            "status": "P_real_adapter" if evaluator_filled else "FAIL",
            "summary": (
                f"EVALUATOR_MAP edge in {route} movement graph resolves to "
                f"MOVES_CLEANLY with {adapter_name}-filled payload."
            ),
            "data": {
                "packet_status": packet_status,
                "rerun_status": rerun_status,
                "evaluator_edge_status": evaluator_edge.get("status") if evaluator_edge else "MISSING",
            },
        }

    # Top integration check sums the sub-checks.
    subcheck_names: List[str] = [
        f"{base}_payload_contract_P",
        f"{base}_no_smuggling_P",
        f"{base}_external_ledger_declared_P",
        f"{base}_certification_P",
    ]
    if evaluator_consistent_check is not None:
        subcheck_names.insert(1, f"{base}_evaluator_consistent_P")

    def check_top_integration() -> Dict[str, Any]:
        subs = [check_payload_contract(), check_no_smuggling(),
                check_external_ledger_declared(), check_certification()]
        if evaluator_consistent_check is not None:
            subs.insert(1, evaluator_consistent_check())
        ok = all(s["consistent"] for s in subs)
        return {
            "name": top_name,
            "consistent": ok,
            "status": "P_real_adapter" if ok else "FAIL",
            "summary": (
                f"{adapter_name} real adapter wires banked evaluator content into "
                f"Engine-readable route payload; EVALUATOR_MAP edge fills cleanly; "
                f"no smuggling; external ledger declared."
            ),
            "dependencies": subcheck_names,
            "data": {"subchecks": {s["name"]: s["consistent"] for s in subs}},
        }

    checks: Dict[str, Callable[[], Dict[str, Any]]] = {
        f"{base}_payload_contract_P": check_payload_contract,
        f"{base}_no_smuggling_P": check_no_smuggling,
        f"{base}_external_ledger_declared_P": check_external_ledger_declared,
        f"{base}_certification_P": check_certification,
        top_name: check_top_integration,
    }
    if evaluator_consistent_check is not None:
        checks[f"{base}_evaluator_consistent_P"] = evaluator_consistent_check

    return checks
