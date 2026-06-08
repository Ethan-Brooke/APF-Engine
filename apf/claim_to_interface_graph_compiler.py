"""
APF Claim-to-Interface Graph Compiler.

v24.3.12+ delta layer.

Purpose
-------
Compile a prose claim / theorem label / route title into a conservative
interface-intelligence audit packet:

    claim text
      -> route class
      -> conservative route payload
      -> certification
      -> movement graph
      -> repair frontier
      -> obligation packet
      -> reviewer-safe claim language

Boundary
--------
A claim text is never treated as evidence.  The compiler only identifies which
interface route would have to close, then generates the audit/obligation packet.

Top check:
    check_T_claim_to_interface_graph_compiler_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import re
import json

try:
    from apf.interface_structure_discovery_engine import discover_and_certify
    from apf.interface_structure_movement_graph import movement_graph_report
    from apf.interface_repair_frontier_explorer import explore_repair_frontier
    from apf.interface_repair_obligation_compiler import compile_obligation_packet, evidence_template
    from apf.interface_evidence_rerun_controller import control_evidence_rerun
except Exception as exc:  # pragma: no cover
    raise ImportError(f"claim_to_interface_graph_compiler requires interface-intelligence stack: {exc}") from exc


class ClaimRoute(str, Enum):
    EW_TRACE_TO_SCHEME = "ew"
    DARK_POSTERIOR = "dark"
    GAUGE_FIBER = "gauge"
    HORIZON_FIBER_COST = "horizon"
    CAPACITY_COARSE_GRAIN = "capacity"
    PROVENANCE_AUDIT = "provenance"
    SUBSTRATE_CSTAR = "cstar"
    GENERIC = "generic"
    # v24.3.41 — Step D audit findings 1 (Finding 1 across all 3 audits):
    # RDFI master claim ("Global physics = ker(Obs_APF) = im(Glob)") and
    # categorical/multi-route claims previously fell through to provenance
    # (single 'smuggling' hit) or gauge (incidental fiber/gauge hits).
    STRUCTURAL_KERNEL = "structural_kernel"
    MULTI_ROUTE_AUDIT = "multi_route_audit"
    CATEGORICAL_UNIFICATION = "categorical_unification"


class ClaimStrength(str, Enum):
    LOCAL_ONLY = "LOCAL_ONLY"
    GLOBAL_EXPORT_ASSERTED = "GLOBAL_EXPORT_ASSERTED"
    RUNTIME_OR_EMPIRICAL_ASSERTED = "RUNTIME_OR_EMPIRICAL_ASSERTED"
    REPAIR_OR_FRONTIER_ASSERTED = "REPAIR_OR_FRONTIER_ASSERTED"
    AMBIGUOUS = "AMBIGUOUS"


@dataclass(frozen=True)
class ClaimCompilation:
    claim_text: str
    route: ClaimRoute
    strength: ClaimStrength
    payload: Mapping[str, Any]
    detected_terms: Tuple[str, ...]
    required_structures: Tuple[str, ...]
    safe_language: str
    caution: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_text": self.claim_text,
            "route": self.route.value,
            "strength": self.strength.value,
            "payload": dict(self.payload),
            "detected_terms": self.detected_terms,
            "required_structures": self.required_structures,
            "safe_language": self.safe_language,
            "caution": self.caution,
        }


@dataclass(frozen=True)
class ClaimAuditReport:
    compilation: ClaimCompilation
    certification: Mapping[str, Any]
    movement_graph: Mapping[str, Any]
    frontier: Mapping[str, Any]
    obligation_packet: Mapping[str, Any]
    evidence_template: Mapping[str, Any]
    rerun_without_evidence: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "compilation": self.compilation.to_dict(),
            "certification": dict(self.certification),
            "movement_graph": dict(self.movement_graph),
            "frontier": dict(self.frontier),
            "obligation_packet": dict(self.obligation_packet),
            "evidence_template": dict(self.evidence_template),
            "rerun_without_evidence": dict(self.rerun_without_evidence),
        }


ROUTE_TERMS = {
    ClaimRoute.EW_TRACE_TO_SCHEME: (
        "ew", "electroweak", "trace-to-scheme", "trace to scheme", "apf_trace",
        "w_trace", "physical scheme", "scheme masses", "m_w", "w mass", "fermion mass",
        "source-to-scheme", "counterterm",
        # Mass-sector sub-route vocabulary (2026-05-18 vocabulary refinement,
        # APF_CLAIM_CLASSIFIER_VOCABULARY_REFINEMENT_v1):
        # catches mass:route_NN_* sub-routes (charm/bottom/top poles, MSR routes)
        # that fell through to generic in atlas v0.2.
        "charm", "bottom", "top", "light-quark", "light quark", "charged-lepton",
        "charged lepton", "lepton", "quark", "yukawa",
        "msbar", "ms-bar", "ms bar", "msr", "pole", "pole-mass", "pole mass",
        "pole/mc",
    ),
    ClaimRoute.DARK_POSTERIOR: (
        "dark", "desi", "posterior", "cobaya", "w0", "wa", "pantheon", "planck",
        "chains", "mcmc", "convergence", "runtime", "growth",
        # Neutrino sub-route vocabulary (2026-05-18 vocabulary refinement):
        # grouped under DARK_POSTERIOR per the framework's empirical-phenomenology
        # convention. Neutrino-hierarchy and m_bb routes have empirical-evaluator
        # structure (DUNE/JUNO as named external evaluators) parallel to dark posterior.
        "neutrino", "dune", "juno", "m_bb", "m_{bb}", "hierarchy", "oscillation",
        "seesaw", "majorana", "normal hierarchy", "inverted hierarchy",
    ),
    ClaimRoute.GAUGE_FIBER: (
        "gauge", "fiber", "automorphism", "cocycle", "anomaly", "representation faithful",
        "su(3)", "su(2)", "u(1)",
    ),
    ClaimRoute.HORIZON_FIBER_COST: (
        "horizon", "area", "fiber-cost", "fiber cost", "entropy ledger", "black hole",
        "bekenstein", "hubble", "surface",
        # Gravity sub-route vocabulary (2026-05-18 vocabulary refinement):
        # grouped under HORIZON_FIBER_COST per the framework's gravity-as-fiber-cost
        # mapping. GR-limit / Bianchi / ringdown / FRW routes share the
        # horizon-fiber-cost typed structure (LATEST-71 + LATEST-72 close).
        "bianchi", "ringdown", "gr-limit", "gr limit", "general relativity",
        "frw", "lensing", "modified gravity", "modified-gravity", "metric",
        "einstein", "non-gr", "non gr",
    ),
    ClaimRoute.CAPACITY_COARSE_GRAIN: (
        "capacity", "overspend", "coarse-grain", "coarse grain", "load", "budget",
        "saturation", "effective load",
    ),
    ClaimRoute.PROVENANCE_AUDIT: (
        "provenance", "smuggling", "target used", "target value", "posterior used",
        "anti-fitting", "anti fitting", "fitted output",
    ),
    ClaimRoute.SUBSTRATE_CSTAR: (
        "c*", "c-star", "cstar", "substrate", "reversal", "complex action",
        "operator norm", "polarity",
    ),
    # v24.3.41 — Step D audit Finding 1 closers:
    ClaimRoute.STRUCTURAL_KERNEL: (
        "kernel", "ker(obs", "ker(obs_apf", "im(glob",
        "representation descent", "representation-descent", "rdfi",
        "obstruction calculus", "obstruction kernel", "zero-obstruction",
        "zero obstruction", "exact kernel", "descent kernel",
        "globally admissible physics", "obs_apf", "globalization functor",
        "kernel claim", "kernel theorem", "master theorem", "master claim",
    ),
    ClaimRoute.MULTI_ROUTE_AUDIT: (
        "measurement-complete", "measurement complete", "measurement-completion",
        "measurement completion", "trace-to-scheme measurement completion",
        "registry adjudication", "route-by-route", "route by route",
        "every route", "all routes satisfy", "obstruction-named",
        "obstruction named", "internally exported", "externally imported",
        "named no-smuggling evaluator", "transport registry", "registry table",
        "n routes adjudicated", "multi-route", "multi route",
    ),
    ClaimRoute.CATEGORICAL_UNIFICATION: (
        "acc unification", "acc-unification", "categorical unification",
        "fourth law", "t_acc", "t_acc_unification",
        "fibered category", "regime projection", "regime projections",
        "morphism algebra", "categorical fibration", "categorical lift",
        "subspace functor", "subspace functors", "identity i1", "identity i2",
        "identity i3", "identity i4", "i1 holographic", "i2 gauge-cosmological",
        "i3 thermo-quantum", "i4 action-thermo",
        "p_cat_all_exported", "p_cat_fully_closed_no_imports",
        "no-import provenance", "no external imports",
    ),
}


GLOBAL_EXPORT_TERMS = (
    "global p", "full p", "physical export", "physical scheme export", "exported",
    "closed globally", "fully closed", "scheme masses are exported", "reaches p",
)
LOCAL_TERMS = ("local", "trace closure", "trace-sector", "trace sector", "apf_trace local", "p_local")
RUNTIME_TERMS = ("runtime", "run completed", "posterior", "chains", "converged", "empirical")
REPAIR_TERMS = ("repair", "frontier", "obligation", "evidence", "rerun", "patch")


REQUIRED_STRUCTURES = {
    ClaimRoute.EW_TRACE_TO_SCHEME: (
        "APF_TRACE/W_TRACE local input",
        "target scheme contract",
        "codomain transport",
        "physical evaluator map",
        "counterterm finite parts",
        "external constants ledger",
        "uncertainty/comparison protocol",
        "no target physical mass consumed",
    ),
    ClaimRoute.DARK_POSTERIOR: (
        "route/run state",
        "chain convergence",
        "posterior closure",
        "robustness checks",
        "data ledger cleanliness",
        "empirical/posterior evaluator",
        "codomain transport",
        "no target/posterior output consumed",
    ),
    ClaimRoute.GAUGE_FIBER: (
        "fiber action",
        "group law",
        "faithful representation",
        "gauge codomain map",
        "overlap/cocycle descent",
        "anomaly/evaluator check",
    ),
    ClaimRoute.HORIZON_FIBER_COST: (
        "horizon partition",
        "area-cost map",
        "overlap/gluing",
        "capacity bound",
        "entropy ledger",
        "codomain transport",
    ),
    ClaimRoute.CAPACITY_COARSE_GRAIN: (
        "raw load",
        "capacity budget",
        "coarse-grain factor",
        "effective load <= budget",
        "no target consumed",
    ),
    ClaimRoute.PROVENANCE_AUDIT: (
        "inputs used",
        "declared targets",
        "fitted outputs",
        "posterior outputs",
        "allowed exogenous inputs",
    ),
    ClaimRoute.SUBSTRATE_CSTAR: (
        "substrate complex action",
        "cost-preserving reversal",
        "operator/C*-norm",
        "C* codomain declaration",
    ),
    ClaimRoute.GENERIC: (
        "ACC base",
        "evaluator map",
        "codomain transport",
        "overlap gluing",
        "capacity budget",
        "empirical/posterior closure",
        "clean provenance",
    ),
    # v24.3.41 — Step D audit Finding 1 closers:
    ClaimRoute.STRUCTURAL_KERNEL: (
        "ACC base record",
        "admissible representation descent",
        "obstruction calculus Obs_APF",
        "globalization functor Glob",
        "kernel-image exactness",
        "zero-obstruction certificate",
        "no flat substrate-global C*-algebra",
        "scope boundary preserved",
    ),
    ClaimRoute.MULTI_ROUTE_AUDIT: (
        "route registry enumerated",
        "per-route certificate template",
        "external_import classification",
        "obstruction_named classification",
        "internal_identity classification",
        "no-smuggling discipline preserved across routes",
        "physical-final reserved by design",
    ),
    ClaimRoute.CATEGORICAL_UNIFICATION: (
        "ACC base category",
        "six regime projections",
        "four identities I1 I2 I3 I4",
        "fibered category structure",
        "no external Standard Model imports",
        "no external cosmological dynamics imports",
        "no external empirical-constant imports",
        "DAG-priming chain run before evaluation",
    ),
}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _term_in_text(term: str, text: str) -> bool:
    """Match route trigger terms without allowing simple tokens to hit inside words."""
    if re.fullmatch(r"[a-z0-9_]+", term):
        return re.search(r"(?<![a-z0-9_])" + re.escape(term) + r"(?![a-z0-9_])", text) is not None
    return term in text


def detect_route(claim_text: str) -> Tuple[ClaimRoute, Tuple[str, ...]]:
    text = _norm(claim_text)
    scores: Dict[ClaimRoute, List[str]] = {}
    for route, terms in ROUTE_TERMS.items():
        hits = [term for term in terms if _term_in_text(term, text)]
        if hits:
            scores[route] = hits
    if not scores:
        return ClaimRoute.GENERIC, tuple()
    # v24.3.41 — Step D audit Finding 1 closer:
    # Multi-route / structural-kernel / categorical-unification claims often
    # mention "no-smuggling" in a discipline-preserving sense (e.g. "named
    # no-smuggling evaluator"); they should NOT preempt to provenance just
    # because that single term appears. Provenance now preempts only when it
    # is the dominant scorer (more hits than any other route).
    if ClaimRoute.PROVENANCE_AUDIT in scores:
        prov_hits = len(scores[ClaimRoute.PROVENANCE_AUDIT])
        max_other = max((len(v) for k, v in scores.items() if k != ClaimRoute.PROVENANCE_AUDIT), default=0)
        if prov_hits > max_other:
            return ClaimRoute.PROVENANCE_AUDIT, tuple(scores[ClaimRoute.PROVENANCE_AUDIT])
    # Otherwise choose max hits, stable by enum order.
    best = max(scores.items(), key=lambda kv: len(kv[1]))[0]
    return best, tuple(scores[best])


def detect_strength(claim_text: str) -> ClaimStrength:
    text = _norm(claim_text)
    if any(term in text for term in GLOBAL_EXPORT_TERMS):
        return ClaimStrength.GLOBAL_EXPORT_ASSERTED
    if any(term in text for term in LOCAL_TERMS):
        return ClaimStrength.LOCAL_ONLY
    if any(term in text for term in RUNTIME_TERMS):
        return ClaimStrength.RUNTIME_OR_EMPIRICAL_ASSERTED
    if any(term in text for term in REPAIR_TERMS):
        return ClaimStrength.REPAIR_OR_FRONTIER_ASSERTED
    return ClaimStrength.AMBIGUOUS


def conservative_payload_for(route: ClaimRoute, strength: ClaimStrength, claim_text: str) -> Dict[str, Any]:
    """Conservative payload templates.

    These are intentionally not proof.  They represent what should be audited.
    Unknown export-critical fields default open/False.
    """
    name = "claim_" + re.sub(r"[^a-zA-Z0-9]+", "_", claim_text[:60]).strip("_").lower()
    if not name or name == "claim_":
        name = "claim_generic"

    target_consumed = any(term in _norm(claim_text) for term in ("target used", "target value used", "smuggled", "posterior used as input"))

    if route == ClaimRoute.EW_TRACE_TO_SCHEME:
        local = strength == ClaimStrength.LOCAL_ONLY or "trace" in _norm(claim_text)
        # If the claim asserts global export, require all transport evidence but do not set it as present.
        return {
            "name": name,
            "trace_sector_closed": bool(local),
            "source_to_scheme_registry_present": False,
            "evaluator_map_found": False,
            "codomain_transport_found": False,
            "counterterm_finite_parts_declared": False,
            "external_constants_ledger_clean": False,
            "uncertainty_protocol_declared": False,
            "target_value_consumed": target_consumed,
            "notes": "Conservative claim-compiled EW route payload; claim text is not evidence.",
        }

    if route == ClaimRoute.DARK_POSTERIOR:
        runtime = any(term in _norm(claim_text) for term in ("runtime", "run completed", "completed"))
        posterior = any(term in _norm(claim_text) for term in ("posterior closed", "chains converged", "converged"))
        return {
            "name": name,
            "route_built": True,
            "run_completed": bool(runtime or posterior),
            "chains_converged": False,
            "posterior_closed": False,
            "robustness_checks_passed": False,
            "data_ledger_clean": False,
            "evaluator_map_found": False,
            "codomain_transport_found": True,
            "target_value_consumed": target_consumed,
            "notes": "Conservative claim-compiled dark route payload; runtime/posterior words are not evidence.",
        }

    if route == ClaimRoute.GAUGE_FIBER:
        return {
            "name": name,
            "local_fiber_action_defined": "fiber" in _norm(claim_text) or "gauge" in _norm(claim_text),
            "group_law_verified": False,
            "representation_faithful": False,
            "codomain_map_declared": False,
            "overlap_cocycle_verified": False,
            "anomaly_check_passed": False,
            "capacity_budget_verified": False,
            "target_value_consumed": target_consumed,
            "notes": "Conservative claim-compiled gauge/fiber route payload.",
        }

    if route == ClaimRoute.HORIZON_FIBER_COST:
        return {
            "name": name,
            "horizon_partition_defined": "horizon" in _norm(claim_text),
            "area_cost_map_defined": "area" in _norm(claim_text) or "cost" in _norm(claim_text),
            "overlap_gluing_verified": False,
            "capacity_bound_checked": False,
            "entropy_ledger_clean": False,
            "codomain_transport_found": False,
            "target_value_consumed": target_consumed,
            "notes": "Conservative claim-compiled horizon/fiber-cost route payload.",
        }

    if route == ClaimRoute.CAPACITY_COARSE_GRAIN:
        return {
            "name": name,
            "raw_capacity_load": 100,
            "capacity_budget": 25,
            "coarse_grain_factor": 1,
            "target_value_consumed": target_consumed,
            "notes": "Conservative claim-compiled capacity route payload with placeholder load/budget; replace with real ledger values.",
        }

    if route == ClaimRoute.PROVENANCE_AUDIT:
        text_key = re.sub(r"[^a-z0-9_]+", "_", _norm(claim_text))
        target = "target_value"
        return {
            "name": name,
            "sector": "PROVENANCE",
            "inputs_used": ["declared_input", target] if target_consumed or "smuggling" in _norm(claim_text) else ["declared_input"],
            "declared_targets": [target],
            "fitted_outputs": ["fitted_output"],
            "posterior_outputs": ["posterior_output"],
            "allowed_exogenous_inputs": ["declared_input"],
            "notes": "Conservative claim-compiled provenance audit payload.",
        }

    if route == ClaimRoute.SUBSTRATE_CSTAR:
        return {
            "name": name,
            "notes": "Conservative claim-compiled C*/substrate attempt. Structural blockers are expected unless theorem program supplies primitives.",
        }

    return {
        "name": name,
        "sector": "GENERIC",
        "local_solution_found": False,
        "global_export_requested": True,
        "acc_base_present": False,
        "evaluator_map_found": False,
        "codomain_transport_found": False,
        "overlap_gluing_verified": False,
        "capacity_budget_verified": False,
        "capacity_overspend_detected": False,
        "empirical_or_posterior_closed": False,
        "target_value_used_as_input": target_consumed,
        "notes": "Conservative generic claim payload; needs manual route classification.",
    }


def safe_language_for(route: ClaimRoute, strength: ClaimStrength) -> str:
    if strength == ClaimStrength.GLOBAL_EXPORT_ASSERTED:
        return (
            "Treat as a global-export claim requiring full interface evidence before P: "
            "local success or claim text alone is insufficient."
        )
    if strength == ClaimStrength.LOCAL_ONLY:
        return (
            "Treat as a local/trace claim unless separate transport evidence is supplied; "
            "do not promote to physical/global P."
        )
    if strength == ClaimStrength.RUNTIME_OR_EMPIRICAL_ASSERTED:
        return (
            "Treat as a runtime/empirical claim requiring convergence, posterior closure, "
            "robustness, and provenance evidence before promotion."
        )
    if strength == ClaimStrength.REPAIR_OR_FRONTIER_ASSERTED:
        return (
            "Treat as a repair/frontier claim: it may identify what would close, but does not "
            "prove the repair has been executed."
        )
    return "Claim is ambiguous; compile to conservative audit payload and require explicit evidence."


def compile_claim(claim_text: str) -> ClaimCompilation:
    route, terms = detect_route(claim_text)
    strength = detect_strength(claim_text)
    payload = conservative_payload_for(route, strength, claim_text)
    return ClaimCompilation(
        claim_text=claim_text,
        route=route,
        strength=strength,
        payload=payload,
        detected_terms=terms,
        required_structures=REQUIRED_STRUCTURES[route],
        safe_language=safe_language_for(route, strength),
        caution="Claim text is never treated as evidence; downstream gates must be satisfied by route payload/evidence.",
    )


def audit_claim(claim_text: str) -> ClaimAuditReport:
    comp = compile_claim(claim_text)
    route = comp.route.value
    payload = comp.payload
    certification = discover_and_certify(route, payload)
    movement = movement_graph_report(route, payload)
    frontier = explore_repair_frontier(route, payload).to_dict()
    packet = compile_obligation_packet(route, payload)
    template = evidence_template(packet)
    rerun_without_evidence = control_evidence_rerun(route, payload).to_dict()
    return ClaimAuditReport(
        compilation=comp,
        certification=certification,
        movement_graph=movement,
        frontier=frontier,
        obligation_packet=packet.to_dict(),
        evidence_template=template,
        rerun_without_evidence=rerun_without_evidence,
    )


def canonical_claims() -> Dict[str, str]:
    return {
        "ew_global_export": "EW APF_TRACE physical scheme masses are exported to global P.",
        "ew_local_trace": "EW trace-sector local APF_TRACE closure is banked as P_local.",
        "dark_runtime": "Dark sector Cobaya runtime completed but posterior convergence is still under review.",
        "gauge_fiber": "Gauge group appears as a fiber automorphism with cocycle descent.",
        "horizon_cost": "Horizon area is represented as fiber-cost with capacity bound.",
        "capacity_overspend": "Capacity overspend is relieved by a coarse-grain repair.",
        "provenance_smuggling": "The route has target value smuggling and posterior used as input.",
        "cstar_substrate": "Flat substrate C* global action requires complex action, reversal, and operator norm.",
        "generic": "A new APF route is claimed to close but route class is unspecified.",
    }


def run_canonical_claim_audits() -> Dict[str, Dict[str, Any]]:
    return {name: audit_claim(text).to_dict() for name, text in canonical_claims().items()}


def check_T_claim_route_classification_P() -> Dict[str, Any]:
    audits = run_canonical_claim_audits()
    expected = {
        "ew_global_export": "ew",
        "ew_local_trace": "ew",
        "dark_runtime": "dark",
        "gauge_fiber": "gauge",
        "horizon_cost": "horizon",
        "capacity_overspend": "capacity",
        "provenance_smuggling": "provenance",
        "cstar_substrate": "cstar",
        "generic": "generic",
    }
    tests = {
        name: audits[name]["compilation"]["route"] == route
        for name, route in expected.items()
    }
    return {
        "name": "check_T_claim_route_classification_P",
        "consistent": all(tests.values()),
        "status": "P_claim_compiler" if all(tests.values()) else "FAIL",
        "summary": "Claim compiler classifies canonical prose claims into interface route classes.",
        "data": {"tests": tests, "routes": {k: v["compilation"]["route"] for k, v in audits.items()}},
    }


def check_T_claim_text_not_evidence_P() -> Dict[str, Any]:
    audits = run_canonical_claim_audits()
    ew = audits["ew_global_export"]
    tests = {
        "ew_global_claim_not_P": ew["certification"]["ledger_certificate"]["certificate"]["export_global_P"] is False,
        "ew_global_claim_has_obligations": ew["obligation_packet"]["packet_status"] == "OPEN_EVIDENCE_REQUIRED",
        "ew_no_evidence_no_rerun": ew["rerun_without_evidence"]["status"] == "EVIDENCE_INCOMPLETE_NOT_RERUN",
        "safe_language_requires_evidence": "evidence" in ew["compilation"]["safe_language"].lower(),
    }
    return {
        "name": "check_T_claim_text_not_evidence_P",
        "consistent": all(tests.values()),
        "status": "P_claim_compiler" if all(tests.values()) else "FAIL",
        "summary": "Global-export wording in claim text does not itself promote a route to P.",
        "data": {"tests": tests, "ew_certificate": ew["certification"]["ledger_certificate"]["certificate"]},
        "dependencies": ["check_T_claim_route_classification_P"],
    }


def check_T_claim_required_structures_P() -> Dict[str, Any]:
    audits = run_canonical_claim_audits()
    tests = {
        "ew_has_transport_structures": "codomain transport" in " ".join(audits["ew_global_export"]["compilation"]["required_structures"]).lower(),
        "dark_has_posterior_structures": "posterior closure" in " ".join(audits["dark_runtime"]["compilation"]["required_structures"]).lower(),
        "provenance_has_inputs_targets": "declared targets" in " ".join(audits["provenance_smuggling"]["compilation"]["required_structures"]).lower(),
        "cstar_has_substrate_primitives": "operator/c*-norm" in " ".join(audits["cstar_substrate"]["compilation"]["required_structures"]).lower(),
    }
    return {
        "name": "check_T_claim_required_structures_P",
        "consistent": all(tests.values()),
        "status": "P_claim_compiler" if all(tests.values()) else "FAIL",
        "summary": "Compiled claims expose route-specific required interface structures.",
        "data": {"tests": tests},
        "dependencies": ["check_T_claim_text_not_evidence_P"],
    }


def check_T_claim_obligation_packets_P() -> Dict[str, Any]:
    audits = run_canonical_claim_audits()
    tests = {
        "ew_global_open_obligations": audits["ew_global_export"]["obligation_packet"]["packet_status"] == "OPEN_EVIDENCE_REQUIRED",
        "dark_runtime_open_obligations": audits["dark_runtime"]["obligation_packet"]["packet_status"] == "OPEN_EVIDENCE_REQUIRED",
        "provenance_blocked": audits["provenance_smuggling"]["obligation_packet"]["packet_status"] == "BLOCKED_PROVENANCE_REBUILD_REQUIRED",
        "cstar_blocked": audits["cstar_substrate"]["obligation_packet"]["packet_status"] == "BLOCKED_SUBSTRATE_THEOREM_REQUIRED",
    }
    return {
        "name": "check_T_claim_obligation_packets_P",
        "consistent": all(tests.values()),
        "status": "P_claim_compiler" if all(tests.values()) else "FAIL",
        "summary": "Claim audits generate appropriate obligation packets or blocker statuses.",
        "data": {"tests": tests, "packet_statuses": {k: v["obligation_packet"]["packet_status"] for k, v in audits.items()}},
        "dependencies": ["check_T_claim_required_structures_P"],
    }


def check_T_claim_to_interface_graph_compiler_P() -> Dict[str, Any]:
    subchecks = [
        check_T_claim_route_classification_P(),
        check_T_claim_text_not_evidence_P(),
        check_T_claim_required_structures_P(),
        check_T_claim_obligation_packets_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_claim_to_interface_graph_compiler_P",
        "consistent": ok,
        "status": "P_claim_compiler" if ok else "FAIL",
        "summary": "Claim-to-Interface Graph Compiler is P: prose claims compile to conservative interface audits without treating text as evidence.",
        "data": {
            "core_claim": "A claim text can identify the interface route and required structures, but cannot by itself satisfy the gate.",
            "subchecks": [x["name"] for x in subchecks],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_claim_route_classification_P": check_T_claim_route_classification_P,
    "check_T_claim_text_not_evidence_P": check_T_claim_text_not_evidence_P,
    "check_T_claim_required_structures_P": check_T_claim_required_structures_P,
    "check_T_claim_obligation_packets_P": check_T_claim_obligation_packets_P,
    "check_T_claim_to_interface_graph_compiler_P": check_T_claim_to_interface_graph_compiler_P,
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
            raise TypeError("Unsupported registry type for claim_to_interface_graph_compiler.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
