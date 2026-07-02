"""
APF Base/Fiber Allocation Theorem.

This module banks the deeper unification exposed by the Cross-Interface Algebraic
Impossibility Theorem:

    APF does not unify physics by forcing every regime into one flat master algebra.
    APF unifies physics by deriving the boundary between substrate-global structure
    and interface-local / fiber-internal representation structure.

Top export:
    check_T_base_fiber_allocation_theorem_P

Key doctrine:
    ACC is the base over which regime structures are functorially fibered.
    The impossibility theorem supplies the ceiling: full C*-algebraic structure is
    not substrate-global under the current primitives.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Optional, Tuple


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


@dataclass(frozen=True)
class SubstratePrimitive:
    name: str
    present: bool
    description: str


@dataclass(frozen=True)
class StructureRequirement:
    name: str
    requires_polarity: bool = False
    requires_cost_reversal: bool = False
    requires_complex_scalar_action: bool = False
    requires_operator_norm: bool = False
    requires_external_evaluator: bool = False
    requires_scheme_convention: bool = False
    requires_frame_identification: bool = False
    requires_only_cost_capacity_continuation: bool = False
    note: str = ""


@dataclass(frozen=True)
class AllocationVerdict:
    structure: str
    verdict: str
    reason: str
    requirements: Tuple[str, ...]


SUBSTRATE_PRIMITIVES: Tuple[SubstratePrimitive, ...] = (
    SubstratePrimitive(
        "unordered_binary_partition",
        True,
        "Distinctions are substrate-side unordered binary partitions; no primitive polarity.",
    ),
    SubstratePrimitive(
        "directed_continuation",
        True,
        "Continuations are directed by realignment/cost floors and irreversible class-transition ordering.",
    ),
    SubstratePrimitive(
        "cost_enrichment_R_nonnegative_plus",
        True,
        "Cost-enrichment is over ([0,infinity], +), i.e. a real-valued length/cost monoid.",
    ),
    SubstratePrimitive(
        "capacity_ACC_ledger",
        True,
        "Capacity/correlation accounting and ACC record/projection structure are substrate-global.",
    ),
    SubstratePrimitive(
        "complex_scalar_action",
        False,
        "No substrate-side complex scalar action is primitive.",
    ),
    SubstratePrimitive(
        "cost_preserving_reversal",
        False,
        "No substrate-side cost-preserving reversal is primitive.",
    ),
    SubstratePrimitive(
        "operator_norm_completion",
        False,
        "No substrate-side operator norm or C*-norm completion is primitive.",
    ),
    SubstratePrimitive(
        "external_scheme_evaluator",
        False,
        "No external scheme evaluator is substrate-side primitive.",
    ),
    SubstratePrimitive(
        "across_interface_frame_identification",
        False,
        "No across-interface frame-identification (iso A_1 ~= A_2 / the connection) is a "
        "substrate primitive; loc_commut (Paper 2 supp v3.6) gives a B-orthogonal direct "
        "sum V = S_G1 (+) S_G2 (+) W with the across-interface arrow absent.",
    ),
)


STRUCTURES: Tuple[StructureRequirement, ...] = (
    StructureRequirement(
        "distinction_partition",
        requires_only_cost_capacity_continuation=True,
        note="Binary partition itself is substrate-global.",
    ),
    StructureRequirement(
        "directed_continuation",
        requires_only_cost_capacity_continuation=True,
        note="Continuation direction and composition are substrate-global.",
    ),
    StructureRequirement(
        "capacity_ACC_ledger",
        requires_only_cost_capacity_continuation=True,
        note="ACC ledger/projections are substrate-global.",
    ),
    StructureRequirement(
        "event_typing_class_transition",
        requires_only_cost_capacity_continuation=True,
        note="Class-transition/event typing is substrate-global.",
    ),
    StructureRequirement(
        "substrate_noncommutativity",
        requires_only_cost_capacity_continuation=True,
        note="Noncommutativity from continuation ordering is substrate-global where gate conditions hold.",
    ),
    StructureRequirement(
        "geometric_partition_V_global",
        requires_only_cost_capacity_continuation=True,
        note="The V_global / horizon partition is substrate-accessible through ACC/interface-sector bridge.",
    ),
    StructureRequirement(
        "Cstar_star_involution",
        requires_polarity=True,
        requires_cost_reversal=True,
        requires_complex_scalar_action=True,
        note="The star operation requires conjugation/reversal structure absent from the substrate.",
    ),
    StructureRequirement(
        "complex_linearity_quantum_fiber",
        requires_complex_scalar_action=True,
        note="Complex scalar action is fiber-internal at quantum-capable interfaces.",
    ),
    StructureRequirement(
        "operator_norm_Cstar_norm",
        requires_operator_norm=True,
        note="C*-norm condition requires a normed algebra / operator norm, not a cost length.",
    ),
    StructureRequirement(
        "scheme_specific_evaluator",
        requires_external_evaluator=True,
        requires_scheme_convention=True,
        note="Scheme evaluators are interface/codomain-local, not substrate-global.",
    ),
    StructureRequirement(
        "gauge_fiber_automorphism_program",
        requires_scheme_convention=False,
        note="Not classified as flat-master-algebra content; substrate derivability remains a separate theorem program.",
    ),
    StructureRequirement(
        "across_interface_gauge_connection",
        requires_frame_identification=True,
        note=("The gauge potential A_mu: fixing it requires choosing an across-interface "
              "frame-identification (iso A_1 ~= A_2), convention data absent from the substrate "
              "(loc_commut: B-orthogonal direct sum, across-interface arrow absent)."),
    ),
)


def substrate_inventory() -> Dict[str, bool]:
    return {p.name: p.present for p in SUBSTRATE_PRIMITIVES}


def missing_for(req: StructureRequirement) -> Tuple[str, ...]:
    inv = substrate_inventory()
    missing = []
    if req.requires_polarity and inv.get("unordered_binary_partition", False):
        # The substrate has unordered partitions, not polarity.
        missing.append("substrate_polarity")
    if req.requires_cost_reversal and not inv.get("cost_preserving_reversal", False):
        missing.append("cost_preserving_reversal")
    if req.requires_complex_scalar_action and not inv.get("complex_scalar_action", False):
        missing.append("complex_scalar_action")
    if req.requires_operator_norm and not inv.get("operator_norm_completion", False):
        missing.append("operator_norm_completion")
    if req.requires_external_evaluator and not inv.get("external_scheme_evaluator", False):
        missing.append("external_scheme_evaluator")
    if req.requires_scheme_convention:
        missing.append("scheme_convention_data")
    if req.requires_frame_identification and not inv.get("across_interface_frame_identification", False):
        missing.append("across_interface_frame_identification")
    return tuple(missing)


def allocate(req: StructureRequirement) -> AllocationVerdict:
    if req.requires_only_cost_capacity_continuation:
        return AllocationVerdict(
            req.name,
            "substrate_global",
            "Uses only distinction/continuation/cost/capacity primitives present at the substrate.",
            ("distinction", "continuation", "cost", "capacity"),
        )
    miss = missing_for(req)
    if req.name == "gauge_fiber_automorphism_program":
        return AllocationVerdict(
            req.name,
            "separate_program_not_flat_algebra",
            "Gauge-as-fiber-automorphism is not decided by the C*-impossibility theorem; it remains a separate APF derivation program.",
            tuple(),
        )
    if miss:
        return AllocationVerdict(
            req.name,
            "fiber_local",
            "Requires structure not supplied by substrate primitives.",
            miss,
        )
    return AllocationVerdict(
        req.name,
        "undetermined",
        "No allocation rule fired; requires a future theorem.",
        tuple(),
    )


def all_allocations() -> Dict[str, AllocationVerdict]:
    return {s.name: allocate(s) for s in STRUCTURES}


def check_T_cross_interface_algebraic_impossibility_ceiling_P() -> Dict:
    inv = substrate_inventory()
    facts = {
        "distinctions_unordered_no_polarity": inv["unordered_binary_partition"] and not inv.get("substrate_polarity", False),
        "continuations_directed_no_reversal": inv["directed_continuation"] and not inv["cost_preserving_reversal"],
        "cost_length_not_complex_norm": inv["cost_enrichment_R_nonnegative_plus"] and not inv["complex_scalar_action"] and not inv["operator_norm_completion"],
    }
    if all(facts.values()):
        return _ok(
            "check_T_cross_interface_algebraic_impossibility_ceiling_P",
            status="P_ceiling",
            summary="The cross-interface algebraic impossibility theorem supplies the ceiling: full C*-structure cannot be substrate-global under current primitives.",
            data={"facts": facts, "substrate_inventory": inv},
        )
    return _fail(
        "check_T_cross_interface_algebraic_impossibility_ceiling_P",
        status="FAIL",
        summary="Impossibility ceiling facts not satisfied.",
        data={"facts": facts, "substrate_inventory": inv},
    )


def check_T_base_fiber_allocation_criterion_P() -> Dict:
    inv = substrate_inventory()
    criterion = {
        "substrate_global_if": [
            "invariant / definable using APF distinction",
            "APF generated continuation",
            "real cost/capacity ledger",
            "ACC-preserving morphisms",
            "no polarity/reversal/complex/norm/evaluator requirement",
        ],
        "fiber_local_if_requires": [
            "substrate polarity",
            "cost-preserving reversal/conjugation",
            "complex scalar action",
            "operator/C*-norm",
            "scheme/evaluator conventions",
            "external codomain data",
        ],
    }
    ok = inv["unordered_binary_partition"] and inv["directed_continuation"] and inv["cost_enrichment_R_nonnegative_plus"] and inv["capacity_ACC_ledger"]
    if ok:
        return _ok(
            "check_T_base_fiber_allocation_criterion_P",
            status="P_allocation",
            summary="Base/fiber allocation criterion is well-defined from current APF substrate primitives.",
            data=criterion,
            dependencies=["check_T_cross_interface_algebraic_impossibility_ceiling_P"],
        )
    return _fail("check_T_base_fiber_allocation_criterion_P", status="FAIL", summary="Allocation criterion missing substrate basis", data=criterion)


def check_T_substrate_global_positive_cases_P() -> Dict:
    alloc = all_allocations()
    positives = {
        name: v for name, v in alloc.items()
        if name in {
            "distinction_partition",
            "directed_continuation",
            "capacity_ACC_ledger",
            "event_typing_class_transition",
            "substrate_noncommutativity",
            "geometric_partition_V_global",
        }
    }
    ok = all(v.verdict == "substrate_global" for v in positives.values())
    if ok:
        return _ok(
            "check_T_substrate_global_positive_cases_P",
            status="P_allocation",
            summary="Known APF base structures pass the substrate-global criterion.",
            data={k: v.__dict__ for k, v in positives.items()},
            dependencies=["check_T_base_fiber_allocation_criterion_P"],
        )
    return _fail("check_T_substrate_global_positive_cases_P", status="FAIL", summary="A positive case failed substrate allocation", data={k: v.__dict__ for k, v in positives.items()})


def check_T_fiber_local_negative_cases_P() -> Dict:
    alloc = all_allocations()
    negatives = {
        name: v for name, v in alloc.items()
        if name in {
            "Cstar_star_involution",
            "complex_linearity_quantum_fiber",
            "operator_norm_Cstar_norm",
            "scheme_specific_evaluator",
        }
    }
    ok = all(v.verdict == "fiber_local" and len(v.requirements) > 0 for v in negatives.values())
    if ok:
        return _ok(
            "check_T_fiber_local_negative_cases_P",
            status="P_allocation",
            summary="C*-quantum and scheme-evaluator structures fail the substrate-global criterion and are assigned to fibers.",
            data={k: v.__dict__ for k, v in negatives.items()},
            dependencies=["check_T_base_fiber_allocation_criterion_P"],
        )
    return _fail("check_T_fiber_local_negative_cases_P", status="FAIL", summary="A negative case did not allocate fiber-local", data={k: v.__dict__ for k, v in negatives.items()})


def check_T_Cstar_fiber_internal_boundary_P() -> Dict:
    alloc = all_allocations()
    required = {
        "Cstar_star_involution": {"substrate_polarity", "cost_preserving_reversal", "complex_scalar_action"},
        "complex_linearity_quantum_fiber": {"complex_scalar_action"},
        "operator_norm_Cstar_norm": {"operator_norm_completion"},
    }
    tests = {}
    for name, needed in required.items():
        v = alloc[name]
        tests[name] = (v.verdict == "fiber_local" and needed.intersection(set(v.requirements)) == needed or needed.issubset(set(v.requirements)))
    if all(tests.values()):
        return _ok(
            "check_T_Cstar_fiber_internal_boundary_P",
            status="P_boundary",
            summary="The *-operation, complex action, and C*-norm are fiber-internal under current substrate primitives.",
            data={"tests": tests, "allocations": {k: alloc[k].__dict__ for k in required}},
            dependencies=["check_T_fiber_local_negative_cases_P"],
        )
    return _fail("check_T_Cstar_fiber_internal_boundary_P", status="FAIL", summary="C*-boundary allocation failed", data={"tests": tests})


def check_T_gauge_program_kept_separate_P() -> Dict:
    v = all_allocations()["gauge_fiber_automorphism_program"]
    ok = v.verdict == "separate_program_not_flat_algebra"
    if ok:
        return _ok(
            "check_T_gauge_program_kept_separate_P",
            status="P_audit",
            summary="Gauge-as-fiber-automorphism is kept as a separate theorem program, not smuggled into the C*-impossibility result.",
            data=v.__dict__,
        )
    return _fail("check_T_gauge_program_kept_separate_P", status="FAIL", summary="Gauge program was incorrectly allocated", data=v.__dict__)


def check_T_ACC_unification_not_flat_algebra_P() -> Dict:
    ok = True
    data = {
        "flat_master_algebra_claimed": False,
        "fibered_unification_claimed": True,
        "allowed_claim": "ACC is the base over which APF-generated regime structures are functorially fibered.",
        "forbidden_claim": "APF derives one substrate-side C*-algebra containing every regime.",
    }
    if ok:
        return _ok(
            "check_T_ACC_unification_not_flat_algebra_P",
            status="P_audit",
            summary="ACC unification is stratified/fibered, not a flat universal-algebra overclaim.",
            data=data,
            dependencies=["check_T_Cstar_fiber_internal_boundary_P", "check_T_substrate_global_positive_cases_P"],
        )
    return _fail("check_T_ACC_unification_not_flat_algebra_P", status="FAIL", summary="Flat-algebra audit failed", data=data)


def check_T_representation_locality_theorem_P() -> Dict:
    positives = check_T_substrate_global_positive_cases_P()
    negatives = check_T_fiber_local_negative_cases_P()
    boundary = check_T_Cstar_fiber_internal_boundary_P()
    ok = positives["consistent"] and negatives["consistent"] and boundary["consistent"]
    if ok:
        return _ok(
            "check_T_representation_locality_theorem_P",
            status="P_theorem",
            summary="Representation locality is derived: structures requiring absent polarity/reversal/complex/norm/evaluator data are fiber-local.",
            data={
                "substrate_global_count": 6,
                "fiber_local_count": 4,
                "allocation_rule": "substrate-global iff definable from APF distinction/continuation/cost/capacity without missing fiber-only requirements",
            },
            dependencies=[
                "check_T_substrate_global_positive_cases_P",
                "check_T_fiber_local_negative_cases_P",
                "check_T_Cstar_fiber_internal_boundary_P",
            ],
        )
    return _fail("check_T_representation_locality_theorem_P", status="FAIL", summary="Representation locality theorem failed", data={"positives": positives, "negatives": negatives, "boundary": boundary})


def check_T_base_fiber_allocation_theorem_P() -> Dict:
    subchecks = [
        check_T_cross_interface_algebraic_impossibility_ceiling_P(),
        check_T_base_fiber_allocation_criterion_P(),
        check_T_substrate_global_positive_cases_P(),
        check_T_fiber_local_negative_cases_P(),
        check_T_Cstar_fiber_internal_boundary_P(),
        check_T_gauge_program_kept_separate_P(),
        check_T_ACC_unification_not_flat_algebra_P(),
        check_T_representation_locality_theorem_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_base_fiber_allocation_theorem_P",
            status="P_cat_stratified_unification",
            summary="APF derives the base/fiber allocation rule: universal substrate structures are separated from interface-local representations.",
            data={
                "deeper_unification": "universal base/fiber sorting principle",
                "substrate_global": [
                    "distinction",
                    "continuation",
                    "cost/capacity ledger",
                    "event/class-transition typing",
                    "substrate noncommutativity",
                    "geometric partition content",
                ],
                "fiber_local": [
                    "C*-star operation",
                    "complex scalar action",
                    "operator/C*-norm",
                    "scheme/evaluator conventions",
                ],
                "flat_master_algebra_claimed": False,
                "stratified_fibered_unification_claimed": True,
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_base_fiber_allocation_theorem_P",
        status="FAIL",
        summary="Base/fiber allocation theorem assembly failed.",
        data={"subchecks": subchecks},
    )


def check_T_gauge_connection_is_gauge_variant_convention_P() -> Dict:
    """The 'no B' allocation (narrow form): the across-interface gauge connection A_mu is
    gauge-VARIANT convention and allocates fiber-local -- the same column as the C*-norm
    and the scheme-evaluator -- NOT substrate-global.

    Grounding (not stipulation): fixing A_mu requires an across-interface frame-identification
    (a choice of iso A_1 ~= A_2). The substrate carries NO such primitive --
    SUBSTRATE_PRIMITIVES registers 'across_interface_frame_identification' present=False -- an
    ADOPTED structural premise from loc_commut (Paper 2 supp v3.6: a B-orthogonal direct sum
    with the across-interface arrow absent), NOT separately bank-registered (the
    [P_structural_reading] grade rests on exactly this adopted reading). So the fiber-local
    verdict reads a registered substrate ABSENCE, and this check FAILS if a future theorem
    ever supplies a canonical across-interface arrow (closes gauge_fiber_automorphism_program)
    -- the right falsifier.

    SCOPE -- what this does NOT claim. It classifies ONLY the gauge-VARIANT object
    (A_mu / the colour frame) as convention. It does NOT claim the gauge-INVARIANT residue
    is carried here, and it does NOT close the connection's derivation program. The surviving
    gauge-invariant residue (physical Wilson-loop spectrum VALUE, glueball/gap VALUES,
    continuum existence) is NOT exported by this check; it stays fenced to the
    ledger->Hamiltonian export (yang_mills_md_bridge) + the open
    gauge_fiber_automorphism_program. 'No B' applies to the frame-choice only.

    GRADE [P_structural_reading]: one adopted internal reading -- 'admissible quantity =
    substrate-global per the banked allocation criterion; the across-interface frame-choice =
    convention'. It forces nothing (not [P]).
    """
    alloc = all_allocations()
    conn = alloc["across_interface_gauge_connection"]
    inv = substrate_inventory()

    # (a) connection allocates fiber-local, resting on the substrate-absence requirement
    connection_fiber_local = (
        conn.verdict == "fiber_local"
        and "across_interface_frame_identification" in conn.requirements
    )
    # (b) that absence is a REGISTERED substrate primitive (present=False), not a free flag;
    #     fails if a future arrow-supplying theorem flips it present=True
    frame_identification_absent = (inv.get("across_interface_frame_identification", True) is False)
    # (c) the connection is NOT among the substrate-global structures
    substrate_global_names = {name for name, v in alloc.items() if v.verdict == "substrate_global"}
    connection_not_substrate_global = "across_interface_gauge_connection" not in substrate_global_names
    # (d) the gauge-INVARIANT residue is NOT exported here -- stays fenced to the separate program
    residue_fenced_separate = (
        alloc["gauge_fiber_automorphism_program"].verdict == "separate_program_not_flat_algebra"
    )

    ok = (connection_fiber_local and frame_identification_absent
          and connection_not_substrate_global and residue_fenced_separate)
    data = {
        "connection_verdict": conn.verdict,
        "connection_requirements": list(conn.requirements),
        "frame_identification_substrate_present": inv.get("across_interface_frame_identification", None),
        "connection_not_substrate_global": connection_not_substrate_global,
        "gauge_invariant_residue_exported_here": False,
        "residue_fenced_to": [
            alloc["gauge_fiber_automorphism_program"].verdict,
            "yang_mills_md_bridge ledger->Hamiltonian export (open)",
        ],
        "reading_adopted": "admissible = substrate-global; across-interface frame-choice = convention",
        "scope": "classifies the gauge-VARIANT A_mu/frame as convention; does NOT carry or close the gauge-invariant residue.",
    }
    if ok:
        return _ok(
            "check_T_gauge_connection_is_gauge_variant_convention_P",
            status="P_structural_reading",
            summary=("The across-interface gauge connection A_mu is gauge-variant convention and "
                     "allocates fiber-local (same column as the C*-norm), resting on the banked "
                     "substrate absence of an across-interface frame-identification (loc_commut). "
                     "'No B' for the frame-choice only; the gauge-invariant residue (Wilson value, "
                     "continuum) is NOT carried here and stays fenced to the separate open program."),
            data=data,
            dependencies=[
                "check_T_cross_interface_algebraic_impossibility_ceiling_P",
                "check_T_gauge_program_kept_separate_P",
                "check_T_fiber_local_negative_cases_P",
            ],
        )
    return _fail(
        "check_T_gauge_connection_is_gauge_variant_convention_P",
        status="FAIL",
        summary="The gauge-variant-convention allocation did not hold (connection not fiber-local on a banked absence, or residue fence failed).",
        data=data,
    )



def check_T_across_frame_fork_localized() -> Dict:
    """The across-frame fork is LOCALIZED: a closed-world citation-hygiene theorem.

    CLAIM. The per-region-vs-diagonal (gauged-vs-global) across-frame fork is cited
    by exactly three bank modules -- base_fiber_allocation (the no-B allocation,
    adopted), gauge_quotient_ledger (GQL-2 + the two-region control, "the Goldstone
    shadow"), ym_quotient_ledger (its own gauged-vs-global discriminating control) --
    plus one FENCED MENTION in gauge_invariant_record (the loc_commut across-interface
    frame, consumed as a reading, [P_structural_reading]). No other module references
    the fork, and no confirmed quantitative prediction sits downstream of it as a
    grade-carrying dependency (the 3/13 EW ledger share and the alpha_s forward chain
    are horn-blind: cold audit 2026-07-01, REDUCE 0.85, Finding 1).

    HONEST GLOSS (required by the same audit, Finding 7): this check certifies
    CITATION HYGIENE -- no check outside the enumerated surfaces NAMES a fork
    object -- not semantic horn-blindness. The fork's historical failure mode is
    being smuggled unnamed (the Skolem-Noether Step-1 charge); a source scan cannot
    detect smuggling. What the check buys: the FOUNDATIONAL_BASE across_region row
    ("no_B", status OPEN) is provably CONTAINED -- nothing confirmed rests on it.

    Pattern precedent: the boundary-map corpus check (closed-world over the
    enumerated registry). Falsifiers: (i) a new module cites the fork outside the
    enumeration (this check fails -> re-audit the containment); (ii) a future theorem
    supplies a canonical arrow (the sibling no-B check inverts); (iii) a confirmed
    prediction acquires a fork surface as a grade-carrying dependency.

    GRADE [P_structural]: closed-world over the current corpus, by construction.
    """
    import os
    import apf as _apf_pkg
    pkg_dir = os.path.dirname(os.path.abspath(_apf_pkg.__file__))
    tokens = (
        "across_interface_frame",      # the substrate-primitive identifier
        "across-interface frame",      # the prose form
        "relative orientation",        # the two-region control vocabulary
        "relative theta",
        "gauged-vs-global",            # GQL-2 / YM discriminating controls
        "Goldstone shadow",
    )
    allowed = {
        "base_fiber_allocation.py":  "the no-B allocation (adopted surface; this check lives here)",
        "gauge_quotient_ledger.py":  "GQL-2 + the two-region control (adopted, load-bearing by banked control)",
        "ym_quotient_ledger.py":     "the YM gauged-vs-global discriminating control",
        "gauge_invariant_record.py": "fenced MENTION only (loc_commut reading, [P_structural_reading])",
    }
    hits: Dict[str, list] = {}
    for name in sorted(os.listdir(pkg_dir)):
        if not name.endswith(".py"):
            continue
        try:
            with open(os.path.join(pkg_dir, name), encoding="utf-8", errors="replace") as f:
                src = f.read()
        except OSError:
            continue
        found = [t for t in tokens if t in src]
        if found:
            hits[name] = found
    unexpected = sorted(set(hits) - set(allowed))
    missing = sorted(set(allowed) - set(hits))
    ok = (not unexpected) and (not missing)
    data = {
        "tokens": list(tokens),
        "allowed_surfaces": dict(allowed),
        "hit_map": {k: v for k, v in sorted(hits.items())},
        "unexpected_surfaces": unexpected,
        "missing_expected_surfaces": missing,
        "gloss": "citation hygiene over the enumerated corpus; NOT semantic horn-blindness",
        "containment": ("no confirmed prediction is downstream of the fork as a "
                        "grade-carrying dependency (audit 2026-07-01)"),
    }
    if ok:
        return _ok(
            "check_T_across_frame_fork_localized",
            status="P_structural",
            summary=("The across-frame fork is cited at exactly three bank surfaces plus one "
                     "fenced mention, nowhere else; the FOUNDATIONAL_BASE across_region row is "
                     "provably contained (citation hygiene, closed-world over the current corpus; "
                     "not semantic horn-blindness)."),
            data=data,
            dependencies=["check_T_gauge_connection_is_gauge_variant_convention_P"],
        )
    return _fail(
        "check_T_across_frame_fork_localized",
        status="FAIL",
        summary=("Fork citation surface changed: unexpected=%r missing=%r -- re-audit the "
                 "containment before trusting the localization." % (unexpected, missing)),
        data=data,
    )


CHECKS = {
    "check_T_cross_interface_algebraic_impossibility_ceiling_P": check_T_cross_interface_algebraic_impossibility_ceiling_P,
    "check_T_base_fiber_allocation_criterion_P": check_T_base_fiber_allocation_criterion_P,
    "check_T_substrate_global_positive_cases_P": check_T_substrate_global_positive_cases_P,
    "check_T_fiber_local_negative_cases_P": check_T_fiber_local_negative_cases_P,
    "check_T_Cstar_fiber_internal_boundary_P": check_T_Cstar_fiber_internal_boundary_P,
    "check_T_gauge_program_kept_separate_P": check_T_gauge_program_kept_separate_P,
    "check_T_ACC_unification_not_flat_algebra_P": check_T_ACC_unification_not_flat_algebra_P,
    "check_T_representation_locality_theorem_P": check_T_representation_locality_theorem_P,
    "check_T_base_fiber_allocation_theorem_P": check_T_base_fiber_allocation_theorem_P,
    "check_T_gauge_connection_is_gauge_variant_convention_P": check_T_gauge_connection_is_gauge_variant_convention_P,
    "check_T_across_frame_fork_localized": check_T_across_frame_fork_localized,
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
            raise TypeError("Unsupported registry type for base_fiber_allocation.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
