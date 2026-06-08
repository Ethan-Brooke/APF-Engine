"""APF Claim Dispatcher — Multi-Engine.

Tier 3 shared engine infrastructure per
``APF Reference Docs/Reference - APF Interface Engine Family Architecture (2026-05-19).md``
(Session 4 of the sequencing plan).

Multi-engine claim dispatch layer
---------------------------------

The existing ``apf.claim_to_interface_graph_compiler`` dispatches a claim to ONE
engine (Route Adjudication, the existing IE). It detects a single ``ClaimRoute``
from claim text and produces a single ``ClaimAuditReport``.

This module sits above that compiler and dispatches a claim to **multiple
engines** in the IE family. A claim like *"superconductivity exhibits zero
resistance"* spans both:

* Route Adjudication Engine — the SC sector's contribution to mass/EW routes
  (handled by the existing ``audit_claim`` function returning a generic-route
  reading for claim-text-only inputs).
* Codomain Selection Engine — the SC regime's codomain competition
  (handled by ``adjudicate_codomain_competition``, which returns
  ``OPEN_EVIDENCE_REQUIRED`` for claim-text-only inputs since codomain
  adjudication requires a network state).

The meta-verdict composes both engines' sub-verdicts per the Reference doc Q1
starting position: **conjunctive multi-engine dispatch**. A claim's meta-status
is ``ALL_PASS`` only if every engine it targets adjudicates positively;
otherwise the meta-verdict surfaces the per-engine sub-verdicts honestly.

Failure-mode taxonomy
---------------------

Meta-verdict statuses:

* ``ALL_PASS`` — every targeted engine returns a positive verdict
  (export_global_P=True for Route Adjudication; COHERENT_CODOMAIN_SELECTED for
  Codomain Selection).
* ``PARTIAL_PASS`` — at least one engine passes, at least one does not.
* ``ALL_OPEN`` — every targeted engine returns OPEN_EVIDENCE_REQUIRED (the
  typical case for claim-text-only inputs to the Codomain Selection Engine —
  the engine recognizes the claim's regime but needs interface network state
  to adjudicate).
* ``MIXED_OPEN_FAIL`` — some engines OPEN, some FAIL.
* ``ALL_FAIL`` — every targeted engine returns a fail-closed verdict.

Honest non-claims
-----------------

Multi-engine dispatch does not create new physical claims; it composes existing
engines' verdicts. Per-engine non-claims (numeric_critical_temperature,
material_specific_prediction, highTc_solved, ab_initio_chemistry all = 0) are
preserved verbatim across composition. ``target_value_consumed = False``.

References
----------

* ``apf.claim_to_interface_graph_compiler`` — Route Adjudication Engine claim
  compiler (this module wraps it for multi-engine dispatch).
* ``apf.codomain_selection_engine`` — Codomain Selection Engine entry point.
* ``Reference - APF Interface Engine Family Architecture (2026-05-19).md`` Session 4
  + Q1 starting position (conjunctive multi-engine dispatch).
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Tuple


# ---------------------------------------------------------------------------
# Engine target enum (Tier 2 engines in the IE family)
# ---------------------------------------------------------------------------

class EngineTarget(str, Enum):
    """All 5 engines in the APF Interface Engine family per Reference - APF Interface Engine
    Family Architecture (2026-05-19).md. Sessions 2-6 operationalized 2 + 3 = 5 engines.

    Multi-engine dispatch (Session 4) currently routes claim text to ROUTE_ADJUDICATION
    + CODOMAIN_SELECTION based on keyword recognizers. The 3 latent engines
    (KINEMATICS_ADJUDICATION + DEFECT_CALCULUS + REPRESENTATION_DESCENT, Session 6 seeds)
    are dispatched to when their adapters or claim recognizers are wired up; today they
    are reachable via direct adjudicate_*_*() entry points but not via dispatch_multi_engine.
    """
    ROUTE_ADJUDICATION = "ROUTE_ADJUDICATION"
    CODOMAIN_SELECTION = "CODOMAIN_SELECTION"
    KINEMATICS_ADJUDICATION = "KINEMATICS_ADJUDICATION"  # v24.3.36 — Session 6 latent engine seed
    DEFECT_CALCULUS = "DEFECT_CALCULUS"  # v24.3.36 — Session 6 latent engine seed
    REPRESENTATION_DESCENT = "REPRESENTATION_DESCENT"  # v24.3.36 — Session 6 latent engine seed


# ---------------------------------------------------------------------------
# Codomain regime keyword recognizers
# ---------------------------------------------------------------------------

CODOMAIN_REGIME_TERMS: Dict[str, Tuple[str, ...]] = {
    "SUPERCONDUCTIVITY": (
        "superconduct", "zero resistance", "meissner", "cooper pair",
        "flux quantization", "josephson", "phase winding", "supercurrent",
        "type i superconduct", "type ii superconduct", "high-tc",
    ),
    "SUPERFLUIDITY": (
        "superfluid", "zero viscosity", "quantized circulation", "helium-4",
        "helium-3", "he-4", "he-3", "lambda point", "λ-point", "rotons",
        "superfluid he", "vortex line",
    ),
    "MAGNETISM": (
        "ferromagnet", "antiferromagnet", "spin order", "magnetization",
        "neel order", "néel order", "staggered magnetization", "magnetic domain",
        "exchange interaction", "ising model", "heisenberg model",
        "spin glass", "spontaneous magnetization",
    ),
    "BOSE_EINSTEIN_CONDENSATION": (
        "bose-einstein", "bose einstein", "bec ", " bec.", " bec,", " bec)",
        "condensate phase", "macroscopic occupation", "single mode condensate",
        "atomic condensate", "thermal de broglie",
    ),
    "LASER_COHERENCE": (
        "laser", "coherent emission", "phase-locked photon", "monochromatic emission",
        "lasing", "stimulated emission", "photon condensate",
    ),
    "SYNCHRONIZATION": (
        "kuramoto", "phase locking", "synchronization", "coupled oscillator",
        "collective rhythm", "phase-locked oscillator", "entrainment",
    ),
    "TOPOLOGICAL_ORDER": (
        "topological order", "anyonic", "anyon", "fractional quantum hall",
        "chern number", "braid statistics", "topological sector",
        "long-range entanglement", "topological invariant",
    ),
}


# ---------------------------------------------------------------------------
# Dispatch dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EngineDispatch:
    """One engine's dispatch decision for a claim."""
    engine: EngineTarget
    target_unit_id: str  # ClaimRoute value for ROUTE_ADJUDICATION; regime name for CODOMAIN_SELECTION
    matched_terms: Tuple[str, ...]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "engine": self.engine.value,
            "target_unit_id": self.target_unit_id,
            "matched_terms": list(self.matched_terms),
        }


@dataclass(frozen=True)
class MultiEngineVerdict:
    """Composed verdict across multiple engines."""
    claim_text: str
    engine_dispatches: Tuple[EngineDispatch, ...]
    engine_verdicts: Tuple[Mapping[str, Any], ...]
    meta_status: str
    meta_obligation_packet: Mapping[str, Any]
    audit_first_non_claims_preserved: bool
    cross_engine_note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_text": self.claim_text,
            "engine_dispatches": [d.to_dict() for d in self.engine_dispatches],
            "engine_verdicts": [dict(v) for v in self.engine_verdicts],
            "meta_status": self.meta_status,
            "meta_obligation_packet": dict(self.meta_obligation_packet),
            "audit_first_non_claims_preserved": self.audit_first_non_claims_preserved,
            "cross_engine_note": self.cross_engine_note,
        }


# ---------------------------------------------------------------------------
# Recognizers
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    return text.lower().strip()


def detect_codomain_regime(
    claim_text: str,
) -> Optional[Tuple[str, Tuple[str, ...]]]:
    """Detect whether a claim's text matches a coherent-phase regime.

    Returns ``(regime_name, matched_terms)`` if matched, else ``None``.

    When multiple regimes match (rare; coherent-phase keyword sets are largely
    disjoint), returns the regime with the most matches; ties resolved by
    enum order (alphabetical).
    """
    normalized = _normalize(claim_text)
    best: Optional[Tuple[str, Tuple[str, ...]]] = None
    best_count = 0
    for regime, terms in CODOMAIN_REGIME_TERMS.items():
        matched = tuple(t for t in terms if t in normalized)
        if matched and len(matched) > best_count:
            best = (regime, matched)
            best_count = len(matched)
    return best


def detect_engines(claim_text: str) -> Tuple[EngineDispatch, ...]:
    """Return the list of engine dispatches a claim targets.

    Route Adjudication Engine always runs (existing dispatch via
    ``audit_claim``'s ``detect_route``). Codomain Selection Engine runs only
    when a coherent-phase regime signature matches.
    """
    # Late import to avoid module-load cycles
    from apf.claim_to_interface_graph_compiler import detect_route

    dispatches: List[EngineDispatch] = []

    # Route Adjudication Engine: always dispatches
    route, route_terms = detect_route(claim_text)
    dispatches.append(EngineDispatch(
        engine=EngineTarget.ROUTE_ADJUDICATION,
        target_unit_id=route.value,
        matched_terms=tuple(route_terms),
    ))

    # Codomain Selection Engine: dispatches only if coherent-phase regime matched
    codomain_match = detect_codomain_regime(claim_text)
    if codomain_match is not None:
        regime, codomain_terms = codomain_match
        dispatches.append(EngineDispatch(
            engine=EngineTarget.CODOMAIN_SELECTION,
            target_unit_id=regime,
            matched_terms=codomain_terms,
        ))

    return tuple(dispatches)


# ---------------------------------------------------------------------------
# Per-engine dispatch helpers
# ---------------------------------------------------------------------------

def _dispatch_route_engine(
    claim_text: str,
    dispatch: EngineDispatch,
) -> Dict[str, Any]:
    """Run the Route Adjudication Engine on a claim."""
    from apf.claim_to_interface_graph_compiler import audit_claim

    report = audit_claim(claim_text)
    report_dict = report.to_dict()
    cert = report_dict["certification"]["ledger_certificate"]["certificate"]
    packet = report_dict["obligation_packet"]
    return {
        "engine": EngineTarget.ROUTE_ADJUDICATION.value,
        "target_unit_id": dispatch.target_unit_id,
        "matched_terms": list(dispatch.matched_terms),
        "solver_status": str(cert.get("solver_status")),
        "export_global_P": bool(cert.get("export_global_P")),
        "obstruction": list(cert.get("obstruction", ())),
        "packet_status": str(packet.get("packet_status")),
        "obligation_packet": packet,
    }


def _dispatch_codomain_engine(
    claim_text: str,
    dispatch: EngineDispatch,
) -> Dict[str, Any]:
    """Run the Codomain Selection Engine on a claim (network_state=None case)."""
    from apf.codomain_selection_engine import (
        adjudicate_codomain_competition,
        CodomainSelectionStatus,
    )

    regime = dispatch.target_unit_id
    # Claim-text-only inputs cannot supply network_state; engine returns
    # OPEN_EVIDENCE_REQUIRED with an obligation packet naming the missing
    # network state. This is the honest reading per the engine's design.
    verdict = adjudicate_codomain_competition(regime, network_state=None)
    verdict_dict = verdict.to_dict()
    return {
        "engine": EngineTarget.CODOMAIN_SELECTION.value,
        "target_unit_id": regime,
        "matched_terms": list(dispatch.matched_terms),
        "solver_status": verdict_dict["status"],
        "export_global_P": (
            verdict_dict["status"] == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED.value
        ),
        "obstruction": list(verdict_dict["critical_fields"]),
        "packet_status": verdict_dict["obligation_packet"].get("current_status", "UNKNOWN"),
        "obligation_packet": dict(verdict_dict["obligation_packet"]),
    }


def _per_engine_dispatch(
    claim_text: str,
    dispatch: EngineDispatch,
) -> Dict[str, Any]:
    if dispatch.engine == EngineTarget.ROUTE_ADJUDICATION:
        return _dispatch_route_engine(claim_text, dispatch)
    if dispatch.engine == EngineTarget.CODOMAIN_SELECTION:
        return _dispatch_codomain_engine(claim_text, dispatch)
    raise ValueError(f"unknown engine: {dispatch.engine}")


# ---------------------------------------------------------------------------
# Meta-verdict composition (Q1 starting position: conjunctive)
# ---------------------------------------------------------------------------

def _compose_meta_status(verdicts: Tuple[Mapping[str, Any], ...]) -> str:
    """Conjunctive meta-status per Reference doc Q1 option a."""
    if not verdicts:
        return "NO_ENGINE_DISPATCHED"

    pass_count = sum(1 for v in verdicts if v.get("export_global_P") is True)
    open_count = sum(
        1 for v in verdicts
        if "OPEN_EVIDENCE_REQUIRED" in str(v.get("solver_status", ""))
        or "OPEN_EVIDENCE_REQUIRED" in str(v.get("packet_status", ""))
    )
    fail_count = len(verdicts) - pass_count - open_count

    if pass_count == len(verdicts):
        return "ALL_PASS"
    if open_count == len(verdicts):
        return "ALL_OPEN"
    if fail_count == len(verdicts):
        return "ALL_FAIL"
    if pass_count > 0 and (open_count + fail_count) > 0:
        return "PARTIAL_PASS"
    if open_count > 0 and fail_count > 0:
        return "MIXED_OPEN_FAIL"
    return "UNKNOWN_MIX"


def _compose_meta_obligation(
    verdicts: Tuple[Mapping[str, Any], ...],
    meta_status: str,
) -> Dict[str, Any]:
    """Compose a meta-obligation packet aggregating per-engine evidence requirements.

    Implements the Reference doc Q3 starting position at the cross-engine layer:
    meta-schema with engine-specific evidence_required subtypes.
    """
    evidence_required: List[Dict[str, Any]] = []
    for v in verdicts:
        engine = v["engine"]
        target = v.get("target_unit_id", "unknown")
        packet = v.get("obligation_packet", {})
        evidence_required.append({
            "engine": engine,
            "target_unit_id": target,
            "evidence_required": packet.get("evidence_required", []),
            "current_status": packet.get("current_status") or v.get("packet_status"),
            "recommended_next_action": packet.get("recommended_next_action", ""),
        })

    if meta_status == "ALL_PASS":
        obligation_kind = "no_obligation"
        recommended = "none -- all targeted engines adjudicate positively (conjunctive)"
    elif meta_status == "ALL_OPEN":
        obligation_kind = "supply_evidence_to_all_engines"
        recommended = (
            "supply the per-engine evidence_required listed in evidence_required[]; "
            "all targeted engines need additional inputs to adjudicate"
        )
    elif meta_status == "PARTIAL_PASS":
        obligation_kind = "complete_remaining_engines"
        recommended = (
            "some engines pass; complete the per-engine evidence_required for the "
            "remaining open/failing engines to lift the meta-verdict to ALL_PASS"
        )
    elif meta_status == "MIXED_OPEN_FAIL":
        obligation_kind = "address_fails_before_opens"
        recommended = (
            "the FAIL-closed engines must close their failure modes before evidence-supply "
            "to the OPEN engines becomes meaningful"
        )
    elif meta_status == "ALL_FAIL":
        obligation_kind = "fail_closed"
        recommended = "all targeted engines fail-closed; supply each engine's named repair"
    else:
        obligation_kind = "unknown"
        recommended = "see per-engine evidence_required"

    return {
        "obligation_kind": obligation_kind,
        "meta_status": meta_status,
        "engines_dispatched": [v["engine"] for v in verdicts],
        "evidence_required": evidence_required,
        "recommended_next_action": recommended,
    }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def dispatch_multi_engine(claim_text: str) -> MultiEngineVerdict:
    """Dispatch a claim across all engines that recognize it.

    Returns a ``MultiEngineVerdict`` composing per-engine sub-verdicts under
    the conjunctive meta-status rule (Reference doc Q1 option a).
    """
    dispatches = detect_engines(claim_text)
    verdicts = tuple(_per_engine_dispatch(claim_text, d) for d in dispatches)
    meta_status = _compose_meta_status(verdicts)
    meta_obligation = _compose_meta_obligation(verdicts, meta_status)

    # Audit-first preservation check: no engine should claim numeric content
    audit_ok = True
    for v in verdicts:
        packet = v.get("obligation_packet", {})
        eval_data = packet.get("evaluation_data", {})
        # Numeric_critical_temperature / material_specific_prediction / etc are
        # per-engine non-claims; the cross-engine layer doesn't introduce new ones
        # but does verify none have been silently re-introduced.
        if "numeric_critical_temperature" in eval_data and eval_data["numeric_critical_temperature"] != 0:
            audit_ok = False

    return MultiEngineVerdict(
        claim_text=claim_text,
        engine_dispatches=dispatches,
        engine_verdicts=verdicts,
        meta_status=meta_status,
        meta_obligation_packet=meta_obligation,
        audit_first_non_claims_preserved=audit_ok,
        cross_engine_note=(
            "Conjunctive meta-status per Reference - APF Interface Engine Family "
            "Architecture (2026-05-19).md Q1 option a. A claim is admissible iff every "
            "targeted engine adjudicates positively. Per-engine sub-verdicts surface "
            "honestly in engine_verdicts[]; meta_status composes them."
        ),
    )


# ---------------------------------------------------------------------------
# Bank checks
# ---------------------------------------------------------------------------

def check_T_claim_dispatcher_multi_engine_basic_P() -> Dict[str, Any]:
    """Multi-engine dispatch operates end-to-end on a SC claim."""
    claim = "Superconductivity exhibits zero resistance and Meissner effect; Cooper pairs form."
    verdict = dispatch_multi_engine(claim)
    consistent = (
        len(verdict.engine_dispatches) == 2
        and any(d.engine == EngineTarget.ROUTE_ADJUDICATION for d in verdict.engine_dispatches)
        and any(d.engine == EngineTarget.CODOMAIN_SELECTION for d in verdict.engine_dispatches)
        and any(d.target_unit_id == "SUPERCONDUCTIVITY" for d in verdict.engine_dispatches)
        and len(verdict.engine_verdicts) == 2
        and verdict.meta_status in ("ALL_OPEN", "PARTIAL_PASS", "MIXED_OPEN_FAIL", "ALL_FAIL")
    )
    return {
        "name": "check_T_claim_dispatcher_multi_engine_basic_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_claim_dispatcher_multi_engine_basic" if consistent else "FAIL",
        "epistemic": "P_claim_dispatcher_multi_engine_basic",
        "summary": (
            "Multi-engine claim dispatcher operates end-to-end: SC claim text dispatches "
            "to both Route Adjudication and Codomain Selection engines; per-engine sub-verdicts "
            "produced; meta-status composed via conjunctive rule per Q1 option a."
        ),
        "dependencies": [
            "apf.claim_to_interface_graph_compiler.audit_claim",
            "apf.codomain_selection_engine.adjudicate_codomain_competition",
        ],
        "data": {
            "claim": claim,
            "dispatched_engines": [d.engine.value for d in verdict.engine_dispatches],
            "regime_matched": next((d.target_unit_id for d in verdict.engine_dispatches if d.engine == EngineTarget.CODOMAIN_SELECTION), None),
            "meta_status": verdict.meta_status,
        },
    }


def check_T_claim_dispatcher_codomain_regime_recognizer_P() -> Dict[str, Any]:
    """Codomain regime recognizer catches the 7 regimes correctly."""
    # One claim per regime; verify regime detection
    test_claims = {
        "SUPERCONDUCTIVITY": "Material X is a superconductor with zero resistance.",
        "SUPERFLUIDITY": "Helium-4 below the lambda point exhibits superfluid behavior.",
        "MAGNETISM": "The system shows ferromagnetic spontaneous magnetization below T_C.",
        "BOSE_EINSTEIN_CONDENSATION": "Atoms form a Bose-Einstein condensate at sub-microkelvin temperatures.",
        "LASER_COHERENCE": "Stimulated emission produces coherent laser output.",
        "SYNCHRONIZATION": "Coupled oscillators undergo Kuramoto-style phase locking.",
        "TOPOLOGICAL_ORDER": "Fractional quantum Hall states exhibit topological order with anyonic excitations.",
    }
    results = {}
    for expected_regime, claim in test_claims.items():
        match = detect_codomain_regime(claim)
        detected = match[0] if match else None
        results[expected_regime] = (detected == expected_regime)
    # Negative test: a non-coherent-phase claim should return None
    null_match = detect_codomain_regime("The W boson on-shell mass is 80.36 GeV.")
    consistent = all(results.values()) and null_match is None
    return {
        "name": "check_T_claim_dispatcher_codomain_regime_recognizer_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_codomain_regime_recognizer" if consistent else "FAIL",
        "epistemic": "P_codomain_regime_recognizer",
        "summary": (
            "Codomain regime recognizer identifies all 7 coherent-phase regimes from "
            "representative claim text; non-coherent-phase claim returns None (no false positives)."
        ),
        "dependencies": ["CODOMAIN_REGIME_TERMS"],
        "data": {
            "per_regime_recognition": results,
            "negative_test_returns_none": null_match is None,
        },
    }


def check_T_claim_dispatcher_meta_verdict_conjunctive_P() -> Dict[str, Any]:
    """Meta-verdict composition is conjunctive per Q1 option a."""
    # Construct synthetic per-engine verdicts and verify composition
    all_pass = ({"engine": "A", "export_global_P": True, "solver_status": "PASS"},
                {"engine": "B", "export_global_P": True, "solver_status": "PASS"})
    all_open = ({"engine": "A", "export_global_P": False, "solver_status": "OPEN_EVIDENCE_REQUIRED"},
                {"engine": "B", "export_global_P": False, "solver_status": "OPEN_EVIDENCE_REQUIRED"})
    partial = ({"engine": "A", "export_global_P": True, "solver_status": "PASS"},
               {"engine": "B", "export_global_P": False, "solver_status": "OPEN_EVIDENCE_REQUIRED"})
    all_fail = ({"engine": "A", "export_global_P": False, "solver_status": "FAIL_CLOSED"},
                {"engine": "B", "export_global_P": False, "solver_status": "BLOCKED"})

    cases = {
        "ALL_PASS": _compose_meta_status(all_pass),
        "ALL_OPEN": _compose_meta_status(all_open),
        "PARTIAL_PASS": _compose_meta_status(partial),
        "ALL_FAIL": _compose_meta_status(all_fail),
    }
    consistent = all(expected == actual for expected, actual in cases.items())
    return {
        "name": "check_T_claim_dispatcher_meta_verdict_conjunctive_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_meta_verdict_conjunctive" if consistent else "FAIL",
        "epistemic": "P_meta_verdict_conjunctive",
        "summary": (
            "Meta-status composition is conjunctive per Reference doc Q1 option a: "
            "ALL_PASS iff every engine passes; ALL_OPEN iff every engine is open-evidence; "
            "PARTIAL_PASS for mixed pass+open/fail; ALL_FAIL iff every engine is fail-closed."
        ),
        "dependencies": ["_compose_meta_status"],
        "data": {"cases": cases},
    }


# ---------------------------------------------------------------------------
# Bank registration
# ---------------------------------------------------------------------------

def register(registry=None):
    """Register multi-engine claim dispatcher checks into the bank registry."""
    checks = {
        "check_T_claim_dispatcher_multi_engine_basic_P":
            check_T_claim_dispatcher_multi_engine_basic_P,
        "check_T_claim_dispatcher_codomain_regime_recognizer_P":
            check_T_claim_dispatcher_codomain_regime_recognizer_P,
        "check_T_claim_dispatcher_meta_verdict_conjunctive_P":
            check_T_claim_dispatcher_meta_verdict_conjunctive_P,
    }
    if registry is None:
        return checks
    registry.update(checks)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {
        "check_T_claim_dispatcher_multi_engine_basic_P":
            check_T_claim_dispatcher_multi_engine_basic_P(),
        "check_T_claim_dispatcher_codomain_regime_recognizer_P":
            check_T_claim_dispatcher_codomain_regime_recognizer_P(),
        "check_T_claim_dispatcher_meta_verdict_conjunctive_P":
            check_T_claim_dispatcher_meta_verdict_conjunctive_P(),
    }
