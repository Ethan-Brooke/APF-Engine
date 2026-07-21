"""Finite representation lemmas salvaged from the quarantined seam-closure packet.

Rebuilt 2026-07-20 under RULINGS_OF_RECORD_2026-07-20 (intake folder
Artifacts_2026-07-20_session/quantum_seam_closure_intake/).  The source packet
APF_Quantum_Seam_Closure_v2.0 was KILLED AS BILLED at stage 1 (0.82) and held
at the rulings gate; only its stage-2-verified executable mathematics is
rebuilt here, re-derived leg by leg in exact Fraction arithmetic.  Nothing in
this module bills a physical frontier.  Every check returns
``physical_premises_certified=False`` and names the physical premises it
consumes; a reconciliation instrument computes the consumed union from the
actual results and compares it set-exactly against the separately maintained
``PHYSICAL_PREMISES`` manifest.

The strongest licensed sentence (verbatim from RULINGS_OF_RECORD_2026-07-20):

    Given a separately supplied compact or isometric physical action,
    positive-state structure, orientation synchronization, generator
    completeness, composite typing, and functorial fragment restrictions,
    the packet's finite representation lemmas recover the standard
    finite-dimensional quantum formalism.

MAY-NOT-CITE heads (of record; none of these sentences is licensed by this
module or by anything it imports):

    * "all finite quantum seams are closed"
    * "positivity is derived by compact averaging"
    * "the Held-circle physical antecedent is certified"
    * "G-hold-exact is discharged"
    * "generator completeness is unnecessary"
    * "orientation synchronization is automatic"
    * "the empirical root inventory is complete"
    * "the seam-closure certificate is set-exact"
    * "Paper 5 v7.14 is canonical"
    * "local quadraticity is derived, not assumed" without the finiteness caveat

Standing open grant: G_HOLD_EXACT remains a named grant (Ruling 1: discharge
REFUSED).  Quotient-nullity may be concluded only relative to a declared
context family and resolution, with the named failure predicate
NONCONSERVATIVE_OPERATIONAL_QUOTIENT (Ruling 5).
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations, product
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

Matrix = List[List[F]]
Vector = List[F]
Permutation = Tuple[int, ...]

FAMILY = "quantum.finite_representation_lemmas"

LICENSED_CLAIM = (
    "Given a separately supplied compact or isometric physical action, "
    "positive-state structure, orientation synchronization, generator "
    "completeness, composite typing, and functorial fragment restrictions, "
    "the packet's finite representation lemmas recover the standard "
    "finite-dimensional quantum formalism."
)

MAY_NOT_CITE = (
    "all finite quantum seams are closed",
    "positivity is derived by compact averaging",
    "the Held-circle physical antecedent is certified",
    "G-hold-exact is discharged",
    "generator completeness is unnecessary",
    "orientation synchronization is automatic",
    "the empirical root inventory is complete",
    "the seam-closure certificate is set-exact",
    "Paper 5 v7.14 is canonical",
    "local quadraticity is derived, not assumed (without the finiteness caveat)",
)

NONCONSERVATIVE_OPERATIONAL_QUOTIENT = "NONCONSERVATIVE_OPERATIONAL_QUOTIENT"

# ---------------------------------------------------------------------------
# Physical premise manifest (separately maintained; Ruling 2)
# ---------------------------------------------------------------------------

PHYSICAL_PREMISES: Tuple[str, ...] = (
    "REVERSIBLE_PULLBACK",
    "FINITE_RESOLVED_EVENT_BRANCHES",
    "POSITIVE_STATE_STRUCTURE",
    "ORIENTATION_SYNCHRONIZED_EMBEDDINGS",
    "GENERATOR_COMPLETENESS",
    "COMPACT_OR_ISOMETRIC_ACTION",
    "RESTRICTION_FUNCTORIALITY",
    "CONTEXTUAL_CONGRUENCE_COMPLETENESS",
    "INSTRUMENT_FAMILY_EXHAUSTIVENESS",
    "COMPOSITE_REALIZATION",
    "FRAGMENT_SYSTEM_ADEQUACY",
)

PREMISE_TYPING: Dict[str, Dict[str, str]] = {
    "REVERSIBLE_PULLBACK": {
        "type": "physical",
        "note": "reversal is admitted and represented on the actual carrier "
                "(Ruling 2 table; stage-1 M1 relocation site)",
    },
    "FINITE_RESOLVED_EVENT_BRANCHES": {
        "type": "physical",
        "note": "scope premise: events resolve into finitely many branches",
    },
    "POSITIVE_STATE_STRUCTURE": {
        "type": "physical",
        "note": "physical preparations are positive; supplied, never derived "
                "(stage-1 M8: dropped twice by the packet, restored here)",
    },
    "ORIENTATION_SYNCHRONIZED_EMBEDDINGS": {
        "type": "physical",
        "note": "local complex orientations are synchronized across embeddings "
                "(stage-1 M9: dropped twice by the packet, restored here)",
    },
    "GENERATOR_COMPLETENESS": {
        "type": "physical",
        "note": "the declared generators exhaust the physical morphism family "
                "(Ruling 3: definitional discharge refused; gate kept)",
    },
    "COMPACT_OR_ISOMETRIC_ACTION": {
        "type": "physical",
        "note": "the reversible image is a compact (here: finite closed) group "
                "of isometries (stage-1 M1: the named premise the packet hid "
                "inside pullback-nonexpansion)",
    },
    "RESTRICTION_FUNCTORIALITY": {
        "type": "physical",
        "note": "actual fragment restrictions are functorial star-morphisms "
                "(stage-2 fold-in item 5: premised, not hypothesized)",
    },
    "CONTEXTUAL_CONGRUENCE_COMPLETENESS": {
        "type": "physical",
        "note": "physical half of TWO_SIDED_CONTEXTUAL_CONGRUENCE (Ruling 2 "
                "split): completeness of the physical context family; the "
                "two-sided congruence descent is the algebraic half executed",
    },
    "INSTRUMENT_FAMILY_EXHAUSTIVENESS": {
        "type": "physical",
        "note": "physical half of COMPLETE_INSTRUMENT_RELATIONS (Ruling 2 "
                "split): the declared instrument family is exhaustive; the "
                "algebraic relations are the executed half",
    },
    "COMPOSITE_REALIZATION": {
        "type": "physical",
        "note": "physical half of TYPED_COMPOSITE_OBJECTS (Ruling 2 split): "
                "the physical composite is realized by the typed object; the "
                "category formation is the executed half",
    },
    "FRAGMENT_SYSTEM_ADEQUACY": {
        "type": "physical",
        "note": "physical half of DIRECTED_FRAGMENT_RESTRICTIONS (Ruling 2 "
                "split): the declared fragment system is adequate/directed; "
                "the functorial coherence is the executed half",
    },
}

# Per-check consumed-premise manifest (separately maintained; the
# reconciliation instrument compares actual results against this table AND
# computes the union from the results themselves -- never a literal against
# itself; answers stage-2 MAJOR-1/MAJOR-2).
PREMISE_MANIFEST: Dict[str, Tuple[str, ...]] = {
    "check_L_left_regular_convolution_representation":
        ("CONTEXTUAL_CONGRUENCE_COMPLETENESS",),
    "check_L_conjugated_finite_haar_invariant_form":
        ("COMPACT_OR_ISOMETRIC_ACTION", "REVERSIBLE_PULLBACK"),
    "check_L_nonexpansion_pair_forces_isometry":
        ("REVERSIBLE_PULLBACK", "COMPACT_OR_ISOMETRIC_ACTION"),
    "check_L_effects_povm_density_born":
        ("POSITIVE_STATE_STRUCTURE", "INSTRUMENT_FAMILY_EXHAUSTIVENESS"),
    "check_L_kraus_choi_complete_positivity":
        ("FINITE_RESOLVED_EVENT_BRANCHES", "POSITIVE_STATE_STRUCTURE"),
    "check_L_composite_orientation_synchronization":
        ("ORIENTATION_SYNCHRONIZED_EMBEDDINGS", "COMPOSITE_REALIZATION",
         "GENERATOR_COMPLETENESS"),
    "check_L_kernel_death_holonomy_control":
        ("GENERATOR_COMPLETENESS",),
    "check_L_operational_quotient_conservativity":
        ("CONTEXTUAL_CONGRUENCE_COMPLETENESS",),
    "check_L_pro_cstar_fragment_functoriality":
        ("RESTRICTION_FUNCTORIALITY", "FRAGMENT_SYSTEM_ADEQUACY"),
    "check_L_provenance_coderef_existence": (),
    "check_L_physical_premise_reconciliation": (),
}

MODULE_CODEREF_ALLOWLIST: Tuple[str, ...] = (
    "check_L_left_regular_convolution_representation",
    "check_L_conjugated_finite_haar_invariant_form",
    "check_L_nonexpansion_pair_forces_isometry",
    "check_L_effects_povm_density_born",
    "check_L_kraus_choi_complete_positivity",
    "check_L_composite_orientation_synchronization",
    "check_L_kernel_death_holonomy_control",
    "check_L_operational_quotient_conservativity",
    "check_L_pro_cstar_fragment_functoriality",
    "check_L_provenance_coderef_existence",
    "check_L_physical_premise_reconciliation",
)

PACKET_SOURCE_ALLOWLIST: Tuple[str, ...] = (
    "quantum_seam_closure.check_T_finite_fragment_contextual_left_regular_representation",
    "quantum_seam_closure.check_T_operational_norm_invariant_pairing_from_complete_readouts",
    "quantum_seam_closure.check_T_finite_continuation_cstar_category",
    "quantum_seam_closure.check_T_natural_held_complex_linking_algebra",
    "quantum_seam_closure.check_T_terminal_branch_effects_and_povm_normalization",
    "quantum_seam_closure.check_T_preparation_density_and_born_pairing",
    "quantum_seam_closure.check_T_finite_protocol_kraus_complete_positivity",
    "quantum_seam_closure.check_T_constrained_composite_remains_quantum_without_tensor_faithfulness",
    "quantum_seam_closure.check_T_global_pro_cstar_fragment_system",
    "quantum_seam_closure.check_T_quantum_seam_closure_dependency_contract",
    "RULINGS_OF_RECORD_2026-07-20",
    "COLD_AUDIT_stage1_theorem_chain",
    "COLD_AUDIT_stage2_adversarial_execution",
)

AUDIT_FINDING_ALLOWLIST: Tuple[str, ...] = (
    "stage1-M1", "stage1-M2", "stage1-M3", "stage1-M4", "stage1-M5",
    "stage1-M8", "stage1-M9", "stage1-M10", "stage1-m12",
    "stage2-MAJOR-1", "stage2-MAJOR-2", "stage2-MAJOR-3", "stage2-MAJOR-4",
    "stage2-m5", "stage2-m8", "stage2-m9", "stage2-verified",
    "Ruling-1", "Ruling-2", "Ruling-3", "Ruling-5",
)

PROVENANCE_TABLE: Tuple[Dict[str, object], ...] = (
    {"leg": "left-regular representation from convolution",
     "coderef": "check_L_left_regular_convolution_representation",
     "packet_source": "quantum_seam_closure.check_T_finite_fragment_contextual_left_regular_representation",
     "audit_findings": ("stage2-verified", "Ruling-2")},
    {"leg": "conjugated finite Haar averaging to an invariant form",
     "coderef": "check_L_conjugated_finite_haar_invariant_form",
     "packet_source": "quantum_seam_closure.check_T_operational_norm_invariant_pairing_from_complete_readouts",
     "audit_findings": ("stage2-verified", "stage1-M1", "stage1-M2")},
    {"leg": "nonexpansion pair forces isometry; boost adversary",
     "coderef": "check_L_nonexpansion_pair_forces_isometry",
     "packet_source": "quantum_seam_closure.check_T_operational_norm_invariant_pairing_from_complete_readouts",
     "audit_findings": ("stage1-M1", "stage1-M2")},
    {"leg": "effects, POVM completeness, density, Born evaluation",
     "coderef": "check_L_effects_povm_density_born",
     "packet_source": "quantum_seam_closure.check_T_terminal_branch_effects_and_povm_normalization",
     "audit_findings": ("stage2-verified", "stage1-M8", "stage2-m9")},
    {"leg": "Kraus/Choi with computed negative-transpose control",
     "coderef": "check_L_kraus_choi_complete_positivity",
     "packet_source": "quantum_seam_closure.check_T_finite_protocol_kraus_complete_positivity",
     "audit_findings": ("stage2-verified",)},
    {"leg": "composite soundness with executed orientation synchronization",
     "coderef": "check_L_composite_orientation_synchronization",
     "packet_source": "quantum_seam_closure.check_T_constrained_composite_remains_quantum_without_tensor_faithfulness",
     "audit_findings": ("stage1-M9", "stage2-MAJOR-3", "stage1-M4", "Ruling-3")},
    {"leg": "kernel-death holonomy control",
     "coderef": "check_L_kernel_death_holonomy_control",
     "packet_source": "COLD_AUDIT_stage1_theorem_chain",
     "audit_findings": ("stage1-M2",)},
    {"leg": "operational quotient conservativity (scoped Ruling-5 principle)",
     "coderef": "check_L_operational_quotient_conservativity",
     "packet_source": "RULINGS_OF_RECORD_2026-07-20",
     "audit_findings": ("Ruling-1", "Ruling-5", "stage1-M3", "stage2-MAJOR-4")},
    {"leg": "pro-C* fragment assembly with named functoriality premise",
     "coderef": "check_L_pro_cstar_fragment_functoriality",
     "packet_source": "quantum_seam_closure.check_T_global_pro_cstar_fragment_system",
     "audit_findings": ("stage2-verified", "stage1-m12", "stage2-m8")},
    {"leg": "coderef existence instrument",
     "coderef": "check_L_provenance_coderef_existence",
     "packet_source": "RULINGS_OF_RECORD_2026-07-20",
     "audit_findings": ("Ruling-2",)},
    {"leg": "physical premise reconciliation instrument",
     "coderef": "check_L_physical_premise_reconciliation",
     "packet_source": "COLD_AUDIT_stage2_adversarial_execution",
     "audit_findings": ("stage2-MAJOR-1", "stage2-MAJOR-2", "stage1-M5", "Ruling-2")},
)

# ---------------------------------------------------------------------------
# Exact linear algebra (pure Fractions, deterministic)
# ---------------------------------------------------------------------------


def _shape(a: Matrix) -> Tuple[int, int]:
    return len(a), len(a[0]) if a else 0


def _zero(r: int, c: int) -> Matrix:
    return [[F(0)] * c for _ in range(r)]


def _eye(n: int) -> Matrix:
    return [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]


def _tp(a: Matrix) -> Matrix:
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]


def _mm(a: Matrix, b: Matrix) -> Matrix:
    ar, ac = _shape(a)
    br, bc = _shape(b)
    if ac != br:
        raise ValueError("shape mismatch")
    return [[sum(a[i][k] * b[k][j] for k in range(ac)) for j in range(bc)]
            for i in range(ar)]


def _mv(a: Matrix, v: Vector) -> Vector:
    return [sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a))]


def _add(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def _sub(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def _scal(s: F, a: Matrix) -> Matrix:
    return [[s * x for x in row] for row in a]


def _eq(a: Matrix, b: Matrix) -> bool:
    return _shape(a) == _shape(b) and all(
        a[i][j] == b[i][j] for i in range(len(a)) for j in range(len(a[0])))


def _trace(a: Matrix) -> F:
    return sum(a[i][i] for i in range(len(a)))


def _flat(a: Matrix) -> Tuple[F, ...]:
    return tuple(x for row in a for x in row)


def _rank(a: Matrix) -> int:
    if not a:
        return 0
    m = [row[:] for row in a]
    r, c = _shape(m)
    rank = 0
    col = 0
    while rank < r and col < c:
        piv = next((i for i in range(rank, r) if m[i][col] != 0), None)
        if piv is None:
            col += 1
            continue
        m[rank], m[piv] = m[piv], m[rank]
        p = m[rank][col]
        m[rank] = [x / p for x in m[rank]]
        for i in range(r):
            if i != rank and m[i][col] != 0:
                q = m[i][col]
                m[i] = [m[i][j] - q * m[rank][j] for j in range(c)]
        rank += 1
        col += 1
    return rank


def _span_rank(mats: Sequence[Matrix]) -> int:
    return _rank([list(_flat(m)) for m in mats])


def _quad(b: Matrix, v: Vector) -> F:
    return sum(v[i] * b[i][j] * v[j]
               for i in range(len(v)) for j in range(len(v)))


def _is_psd2(a: Matrix) -> bool:
    return (_shape(a) == (2, 2) and a[0][1] == a[1][0]
            and a[0][0] >= 0 and a[1][1] >= 0
            and a[0][0] * a[1][1] - a[0][1] * a[1][0] >= 0)


def _inv2(a: Matrix) -> Matrix:
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0:
        raise ValueError("singular")
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def _mat_str(a: Matrix) -> List[List[str]]:
    return [[str(x) for x in row] for row in a]


def _matrix_units(n: int) -> List[Matrix]:
    out = []
    for i in range(n):
        for j in range(n):
            e = _zero(n, n)
            e[i][j] = F(1)
            out.append(e)
    return out


def _block_diag2(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    m = len(b)
    out = _zero(n + m, n + m)
    for i in range(n):
        for j in range(n):
            out[i][j] = a[i][j]
    for i in range(m):
        for j in range(m):
            out[n + i][n + j] = b[i][j]
    return out


# ---------------------------------------------------------------------------
# Result schema
# ---------------------------------------------------------------------------


def _result(name: str, key_result: str, dependencies: Sequence[str],
            artifacts: Mapping[str, object], fails: Sequence[str], *,
            premises: Sequence[str], negative_controls: Sequence[str] = (),
            epistemic: str = "P_math") -> Dict[str, object]:
    passed = not fails
    return {
        "name": name,
        "family": FAMILY,
        "tier": 4,
        "epistemic": epistemic,
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "scope": ("finite mathematical witness; conditional on the named "
                  "physical premises, which this module does not establish"),
        "physical_premises_certified": False,
        "key_result": key_result,
        "dependencies": list(dependencies),
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


def _ckr(fails: List[str]):
    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)
    return ck


# ---------------------------------------------------------------------------
# Shared finite-group constructions
# ---------------------------------------------------------------------------


def _perm_compose(p: Permutation, q: Permutation) -> Permutation:
    return tuple(p[q[i]] for i in range(len(p)))


def _s3() -> List[Permutation]:
    return sorted(tuple(p) for p in permutations(range(3)))


def _signed_perm_group2() -> List[Matrix]:
    out: List[Matrix] = []
    for p in ((0, 1), (1, 0)):
        for s0 in (1, -1):
            for s1 in (1, -1):
                m = _zero(2, 2)
                m[0][p[0]] = F(s0)
                m[1][p[1]] = F(s1)
                out.append(m)
    return out


_SHEAR: Matrix = [[F(1), F(1)], [F(0), F(1)]]


def _conjugated_signed_perm_group2() -> List[Matrix]:
    s = _SHEAR
    sinv = _inv2(s)
    return [_mm(_mm(s, g), sinv) for g in _signed_perm_group2()]


BOOST: Matrix = [[F(5, 4), F(3, 4)], [F(3, 4), F(5, 4)]]

_HAAR_SEED: Matrix = [[F(2), F(1)], [F(1), F(3)]]


def _haar_average(group: Sequence[Matrix], seed: Matrix) -> Matrix:
    acc = _zero(2, 2)
    for g in group:
        acc = _add(acc, _mm(_mm(_tp(g), seed), g))
    return _scal(F(1, len(group)), acc)


# ---------------------------------------------------------------------------
# L1. Left-regular representation from actual convolution on S3
# ---------------------------------------------------------------------------


def check_L_left_regular_convolution_representation(
        *, premises_override: Optional[Sequence[str]] = None) -> Dict[str, object]:
    fails: List[str] = []
    ck = _ckr(fails)

    group = _s3()
    idx = {g: i for i, g in enumerate(group)}
    n = len(group)

    def conv(a: Vector, b: Vector,
             compose=_perm_compose) -> Vector:
        out = [F(0)] * n
        for i, gi in enumerate(group):
            for j, gj in enumerate(group):
                out[idx[compose(gi, gj)]] += a[i] * b[j]
        return out

    def delta(g: Permutation) -> Vector:
        v = [F(0)] * n
        v[idx[g]] = F(1)
        return v

    # Left-regular matrix of g: columns are conv(delta_g, delta_h).
    def lreg(g: Permutation) -> Matrix:
        cols = [conv(delta(g), delta(h)) for h in group]
        return [[cols[j][i] for j in range(n)] for i in range(n)]

    reps = {g: lreg(g) for g in group}
    ident = tuple(range(3))
    ck(_eq(reps[ident], _eye(n)), "identity must act as the identity matrix")
    for g in group:
        for h in group:
            ck(_eq(_mm(reps[g], reps[h]), reps[_perm_compose(g, h)]),
               "left-regular action must be a homomorphism (36 pairs)")
    ck(len({_flat(reps[g]) for g in group}) == n,
       "left-regular representation must be faithful")
    ck(_span_rank(list(reps.values())) == n,
       "regular representation must span a rank-6 group-algebra witness")

    # Representation = convolution operator on non-delta samples.
    sample = [F(1), F(-2), F(0), F(3), F(1, 2), F(0)]
    for g in group[:3]:
        ck(_mv(reps[g], sample) == conv(delta(g), sample),
           "matrix action must agree with convolution on generic vectors")

    # Mutation control: corrupting one entry of the composition table must
    # break the homomorphism law (computed, in-check).
    g_bad, h_bad = group[1], group[2]

    def compose_bad(p: Permutation, q: Permutation) -> Permutation:
        if (p, q) == (g_bad, h_bad):
            return ident
        return _perm_compose(p, q)

    if _perm_compose(g_bad, h_bad) != ident:
        bad_cols = [conv(delta(g_bad), delta(h), compose_bad) for h in group]
        bad_rep = [[bad_cols[j][i] for j in range(n)] for i in range(n)]
        ck(not _eq(_mm(reps[g_bad], reps[h_bad]),
                   _mm(bad_rep, reps[h_bad])) or
           not _eq(bad_rep, reps[g_bad]),
           "corrupted convolution table must be detected")
        ck(not _eq(bad_rep, reps[g_bad]),
           "corrupted convolution must change the represented matrix")
    else:
        ck(False, "mutation-control pair must have nonidentity product")

    # Negative control: one-sided (right-coset) equivalence by the non-normal
    # subgroup <(12)> fails descended multiplication -> two-sided congruence
    # is load-bearing (algebraic half of the split clause).
    h_sub = frozenset({ident, (1, 0, 2)})

    def same_right_coset(a: Permutation, b: Permutation) -> bool:
        return (frozenset(_perm_compose(a, x) for x in h_sub)
                == frozenset(_perm_compose(b, x) for x in h_sub))

    one_sided_failure = None
    for a, a2, b, b2 in product(group, repeat=4):
        if same_right_coset(a, a2) and same_right_coset(b, b2):
            if not same_right_coset(_perm_compose(a, b), _perm_compose(a2, b2)):
                one_sided_failure = (a, a2, b, b2)
                break
    ck(one_sided_failure is not None,
       "one-sided non-normal equivalence must fail descended multiplication")

    return _result(
        "check_L_left_regular_convolution_representation",
        ("The group algebra of a finite group (witness: S3, order 6) carries "
         "a faithful left-regular representation computed from actual "
         "convolution; the representation is a homomorphism on all 36 pairs "
         "and agrees with the convolution operator on generic vectors.  A "
         "corrupted composition table is detected in-check.  Descent to a "
         "quotient requires a two-sided congruence (one-sided coset control "
         "fails).  That the physical context family is complete enough to "
         "fix the congruence is the named physical premise, not a theorem."),
        [],
        {
            "group": "S3",
            "order": n,
            "regular_span_rank": _span_rank(list(reps.values())),
            "one_sided_failure_witness":
                [list(p) for p in one_sided_failure] if one_sided_failure else None,
            "convolution_mutation_detected": True,
        },
        fails,
        premises=(tuple(premises_override) if premises_override is not None
                  else PREMISE_MANIFEST["check_L_left_regular_convolution_representation"]),
        negative_controls=(
            "corrupted composition-table convolution",
            "right-coset equivalence by non-normal <(12)> in S3",
        ),
    )


# ---------------------------------------------------------------------------
# L2. Exact finite Haar averaging over a conjugated (non-orthogonal) copy of
#     the 8-element signed-permutation group
# ---------------------------------------------------------------------------


def check_L_conjugated_finite_haar_invariant_form(
        *, group_override: Optional[Sequence[Matrix]] = None,
        premises_override: Optional[Sequence[str]] = None) -> Dict[str, object]:
    fails: List[str] = []
    ck = _ckr(fails)

    default = group_override is None
    group = (_conjugated_signed_perm_group2() if default
             else [x for x in group_override])

    flats = {_flat(g) for g in group}
    ck(len(flats) == len(group), "family elements must be distinct")
    ck(any(_eq(g, _eye(2)) for g in group), "family must contain the identity")

    # COMPACT_OR_ISOMETRIC_ACTION executes here as: the supplied family is an
    # actual finite group (closed under products and inverses).  This is the
    # gate the packet hid inside pullback-nonexpansion (stage-1 M1).
    for a in group:
        for b in group:
            ck(_flat(_mm(a, b)) in flats,
               "family must be closed under multiplication")
    for a in group:
        try:
            ck(_flat(_inv2(a)) in flats,
               "family must be closed under inversion")
        except ValueError:
            ck(False, "family elements must be invertible")

    invariant = None
    if not fails:
        invariant = _haar_average(group, _HAAR_SEED)
        for g in group:
            ck(_eq(_mm(_mm(_tp(g), invariant), g), invariant),
               "averaged form must be exactly invariant under every element")
        ck(invariant[0][0] > 0 and
           invariant[0][0] * invariant[1][1] - invariant[0][1] ** 2 > 0,
           "averaged form must be positive definite")

    if default:
        ck(len(group) == 8, "conjugated signed-permutation group has order 8")
        # Conjugation makes invariance non-trivial: elements are not all
        # orthogonal and the invariant form is not a multiple of the identity.
        ck(any(not _eq(_mm(_tp(g), g), _eye(2)) for g in group),
           "conjugated copy must contain non-orthogonal elements")
        if invariant is not None:
            ck(invariant[0][1] != 0,
               "invariant form of the conjugated group must be non-diagonal")
        # Contrast: the unconjugated (orthogonal) group averages the same seed
        # to a scalar multiple of the identity.
        plain = _haar_average(_signed_perm_group2(), _HAAR_SEED)
        ck(_eq(plain, _scal(F(5, 2), _eye(2))),
           "orthogonal-copy average must be the scalar form (5/2) I")
        # Seed control: the seed itself is not invariant.
        ck(any(not _eq(_mm(_mm(_tp(g), _HAAR_SEED), g), _HAAR_SEED)
               for g in group),
           "seed form must be a genuine non-invariant control")

    return _result(
        "check_L_conjugated_finite_haar_invariant_form",
        ("Averaging a positive seed form over an actual finite group of "
         "reversible actions yields an exactly invariant positive-definite "
         "form.  Witness: the 8-element signed-permutation group conjugated "
         "by a non-orthogonal shear, so invariance is non-trivial (the "
         "output form is non-diagonal) and is verified exactly on every "
         "group element.  The averaging argument consumes compactness (here "
         "finiteness/closure) of the reversible image as a named physical "
         "premise; it does not derive it.  Positivity of the output rides on "
         "positivity of the seed and closure of the family -- both gates "
         "execute in-check and both fail on a boost family."),
        ["check_L_left_regular_convolution_representation"],
        {
            "family_order": len(group),
            "conjugator": _mat_str(_SHEAR),
            "seed": _mat_str(_HAAR_SEED),
            "invariant_form": _mat_str(invariant) if invariant else None,
            "default_family": default,
        },
        fails,
        premises=(tuple(premises_override) if premises_override is not None
                  else PREMISE_MANIFEST["check_L_conjugated_finite_haar_invariant_form"]),
        negative_controls=(
            "non-invariant seed [[2,1],[1,3]]",
            "boost family fails closure/inversion (see mutation battery)",
        ),
    )


# ---------------------------------------------------------------------------
# L3. Nonexpansion + inverse nonexpansion => isometry; boost adversary
# ---------------------------------------------------------------------------


def check_L_nonexpansion_pair_forces_isometry(
        *, premises_override: Optional[Sequence[str]] = None) -> Dict[str, object]:
    fails: List[str] = []
    ck = _ckr(fails)

    group = _conjugated_signed_perm_group2()
    b_form = _haar_average(group, _HAAR_SEED)
    grid = [[F(x), F(y)] for x in range(-3, 4) for y in range(-3, 4)]

    # Finite witness of the lemma: for each element, forward nonexpansion and
    # inverse nonexpansion both hold on the grid, and together they force
    # exact equality (isometry), which is also verified as the exact matrix
    # identity g^T B g = B.
    for g in group:
        ginv = _inv2(g)
        for v in grid:
            qv = _quad(b_form, v)
            ck(_quad(b_form, _mv(g, v)) <= qv,
               "group elements must be nonexpansive for the invariant form")
            ck(_quad(b_form, _mv(ginv, v)) <= qv,
               "group inverses must be nonexpansive for the invariant form")
            ck(_quad(b_form, _mv(g, v)) == qv,
               "nonexpansion both ways must force exact norm equality")
        ck(_eq(_mm(_mm(_tp(g), b_form), g), b_form),
           "isometry must hold as the exact identity g^T B g = B")

    # Control 1: a strict contraction is forward-nonexpansive but its inverse
    # is not; it is not an isometry.  Both clauses are load-bearing.
    half = _scal(F(1, 2), _eye(2))
    ck(all(_quad(b_form, _mv(half, v)) <= _quad(b_form, v) for v in grid),
       "contraction control must be forward nonexpansive")
    ck(any(_quad(b_form, _mv(_inv2(half), v)) > _quad(b_form, v) for v in grid),
       "contraction inverse must fail nonexpansion")
    ck(not _eq(_mm(_mm(_tp(half), b_form), half), b_form),
       "contraction must fail the isometry identity")

    # Control 2 (restored deleted adversary, stage-1 M2): the SO(1,1) boost
    # fails nonexpansion in both directions and has strictly growing orbit
    # norms -- it generates no compact/isometric action.
    euclid = _eye(2)
    v_grow = [F(1), F(1)]
    ck(_quad(euclid, _mv(BOOST, v_grow)) > _quad(euclid, v_grow),
       "boost must fail forward nonexpansion")
    v_grow_inv = [F(1), F(-1)]
    ck(_quad(euclid, _mv(_inv2(BOOST), v_grow_inv)) > _quad(euclid, v_grow_inv),
       "boost inverse must fail nonexpansion")
    orbit_norms: List[F] = []
    w = v_grow[:]
    for _ in range(6):
        orbit_norms.append(_quad(euclid, w))
        w = _mv(BOOST, w)
    ck(all(orbit_norms[k] < orbit_norms[k + 1]
           for k in range(len(orbit_norms) - 1)),
       "boost orbit norms must be strictly increasing (computed)")
    ck(not _eq(_mm(_tp(BOOST), BOOST), _eye(2)),
       "boost must fail the exact isometry identity")
    powers = []
    p = _eye(2)
    for _ in range(9):
        powers.append(_flat(p))
        p = _mm(p, BOOST)
    ck(len(set(powers)) == len(powers),
       "boost powers must be pairwise distinct: the generated action is "
       "unbounded, never finite/compact")

    return _result(
        "check_L_nonexpansion_pair_forces_isometry",
        ("If an invertible action and its inverse are both nonexpansive for "
         "a positive form, the action is an exact isometry of that form "
         "(finite witness legs: verified on a 49-point grid and as the exact "
         "matrix identity for all 8 conjugated group elements).  A strict "
         "contraction shows the inverse clause is load-bearing.  The "
         "SO(1,1) boost [[5/4,3/4],[3/4,5/4]] fails nonexpansion in both "
         "directions, has strictly increasing computed orbit norms, and "
         "generates an unbounded action: whether the physical reversible "
         "image is compact/isometric is a named physical premise that this "
         "adversary shows cannot be waved through."),
        ["check_L_conjugated_finite_haar_invariant_form"],
        {
            "invariant_form": _mat_str(b_form),
            "boost": _mat_str(BOOST),
            "boost_orbit_norms": [str(x) for x in orbit_norms],
            "grid_points": len(grid),
        },
        fails,
        premises=(tuple(premises_override) if premises_override is not None
                  else PREMISE_MANIFEST["check_L_nonexpansion_pair_forces_isometry"]),
        negative_controls=(
            "strict contraction (1/2)I: forward-only nonexpansion",
            "SO(1,1) boost: fails both nonexpansion clauses, unbounded orbit",
        ),
    )


# ---------------------------------------------------------------------------
# L4. Effects, POVM completeness, density matrices, Born evaluation
# ---------------------------------------------------------------------------

REQUIRED_INSTRUMENT_RELATIONS: Tuple[str, ...] = (
    "branch_effects_are_adjoint_squares",
    "effects_sum_to_identity",
    "effects_are_positive_contractions",
    "born_scores_are_probabilities",
)


def check_L_effects_povm_density_born(
        *, declared_relations: Optional[Sequence[str]] = None,
        premises_override: Optional[Sequence[str]] = None) -> Dict[str, object]:
    fails: List[str] = []
    ck = _ckr(fails)

    declared = (tuple(declared_relations) if declared_relations is not None
                else REQUIRED_INSTRUMENT_RELATIONS)

    k0 = [[F(1), F(0)], [F(0), F(4, 5)]]
    k1 = [[F(0), F(3, 5)], [F(0), F(0)]]
    e0 = _mm(_tp(k0), k0)
    e1 = _mm(_tp(k1), k1)

    # POSITIVE_STATE_STRUCTURE: positivity of preparations is a supplied
    # physical premise; the gate below verifies the supplied witness and
    # demonstrably rejects a non-positive impostor (stage-1 M8 answer:
    # positivity is checked against the premise, never true "by definition").
    p0 = [F(3, 5), F(0)]
    p1 = [F(0), F(4, 5)]
    rho = _add([[p0[i] * p0[j] for j in range(2)] for i in range(2)],
               [[p1[i] * p1[j] for j in range(2)] for i in range(2)])
    ck(_trace(rho) == 1, "preparation density must be normalized")
    ck(_is_psd2(rho), "supplied preparation must satisfy the positivity gate")
    rho_bad = [[F(3, 2), F(0)], [F(0), F(-1, 2)]]
    ck(_trace(rho_bad) == 1, "impostor control must be trace-normalized")
    ck(not _is_psd2(rho_bad),
       "positivity gate must reject the non-positive trace-one impostor")

    e_test = [[F(1, 3), F(1, 6)], [F(1, 6), F(2, 3)]]

    def verify(relation: str) -> None:
        if relation == "branch_effects_are_adjoint_squares":
            ck(_eq(e0, _mm(_tp(k0), k0)) and _eq(e1, _mm(_tp(k1), k1)),
               "effects must be k* k for the declared branches")
            ck(_is_psd2(e0) and _is_psd2(e1),
               "adjoint squares must be positive")
        elif relation == "effects_sum_to_identity":
            ck(_eq(_add(e0, e1), _eye(2)),
               "complete branch family must normalize to the unit (POVM)")
        elif relation == "effects_are_positive_contractions":
            ck(_is_psd2(_sub(_eye(2), e0)) and _is_psd2(_sub(_eye(2), e1)),
               "effects must be positive contractions")
            ck(not _eq(_mm(e0, e0), e0),
               "witness must include a genuinely unsharp (non-PVM) effect")
        elif relation == "born_scores_are_probabilities":
            ck(_is_psd2(e_test) and _is_psd2(_sub(_eye(2), e_test)),
               "tested effect must be a positive contraction")
            born = _trace(_mm(rho, e_test))
            branch_score = sum(
                sum(p[i] * e_test[i][j] * p[j]
                    for i in range(2) for j in range(2))
                for p in (p0, p1))
            ck(born == branch_score,
               "branch score must equal the Born trace pairing Tr(rho e)")
            ck(F(0) <= born <= F(1), "Born score must be a probability")
        else:
            ck(False, "unknown instrument relation declared: %s" % relation)

    for relation in declared:
        verify(relation)

    # Completeness leg (algebraic half); that the declared family exhausts
    # the physical instruments is INSTRUMENT_FAMILY_EXHAUSTIVENESS (physical).
    ck(set(declared) == set(REQUIRED_INSTRUMENT_RELATIONS),
       "declared instrument relations must match the required set exactly")

    return _result(
        "check_L_effects_povm_density_born",
        ("In a represented finite algebra, declared branch morphisms yield "
         "positive effects e = k* k summing exactly to the identity (POVM); "
         "supplied positive normalized preparations are density matrices; "
         "and the branch score equals the Born trace pairing Tr(rho e), a "
         "probability -- all in exact arithmetic.  Positivity of states is "
         "consumed as a physical premise and gate-checked (a trace-one "
         "non-positive impostor is rejected).  The relation list is checked "
         "for set-exact completeness against the declared family; that the "
         "family exhausts the physical instruments is the named physical "
         "premise."),
        ["check_L_conjugated_finite_haar_invariant_form"],
        {
            "effects": [_mat_str(e0), _mat_str(e1)],
            "rho": _mat_str(rho),
            "rejected_impostor": _mat_str(rho_bad),
            "born_probability": str(_trace(_mm(rho, e_test))),
            "declared_relations": list(declared),
            "required_relations": list(REQUIRED_INSTRUMENT_RELATIONS),
        },
        fails,
        premises=(tuple(premises_override) if premises_override is not None
                  else PREMISE_MANIFEST["check_L_effects_povm_density_born"]),
        negative_controls=(
            "trace-one non-positive impostor state rejected",
            "unsharp effect: POVM does not collapse to PVM",
        ),
    )


# ---------------------------------------------------------------------------
# L5. Kraus/Choi complete positivity with a computed negative-transpose control
# ---------------------------------------------------------------------------


def check_L_kraus_choi_complete_positivity(
        *, premises_override: Optional[Sequence[str]] = None) -> Dict[str, object]:
    fails: List[str] = []
    ck = _ckr(fails)

    k0 = [[F(1), F(0)], [F(0), F(4, 5)]]
    k1 = [[F(0), F(3, 5)], [F(0), F(0)]]
    kraus = (k0, k1)

    def phi(x: Matrix) -> Matrix:
        acc = _zero(2, 2)
        for k in kraus:
            acc = _add(acc, _mm(_mm(k, x), _tp(k)))
        return acc

    def choi_of(mapping) -> Matrix:
        e2 = _matrix_units(2)
        c = _zero(4, 4)
        for i in range(2):
            for j in range(2):
                block = mapping(e2[2 * i + j])
                for a in range(2):
                    for b in range(2):
                        c[2 * i + a][2 * j + b] += block[a][b]
        return c

    choi = choi_of(phi)

    # Cross-check: Choi equals the computed sum of vec outer products.
    vecs = [[k[r][c] for c in range(2) for r in range(2)] for k in kraus]
    choi_vec = _zero(4, 4)
    for w in vecs:
        choi_vec = _add(choi_vec,
                        [[w[i] * w[j] for j in range(4)] for i in range(4)])
    ck(_eq(choi, choi_vec),
       "Choi from map-on-matrix-units must equal the vec outer-product sum")

    for v in product(range(-2, 3), repeat=4):
        ck(_quad(choi, [F(x) for x in v]) >= 0,
           "Kraus-form Choi matrix must be PSD on the exact grid")
    ck(_rank(choi) == 2,
       "two independent Kraus branches must give Choi rank two")

    esum = _zero(2, 2)
    for k in kraus:
        esum = _add(esum, _mm(_tp(k), k))
    ck(_eq(esum, _eye(2)),
       "complete branch family must be trace preserving")

    # Control: the transpose map is positive but not completely positive.
    # Its Choi matrix is COMPUTED by applying the map to matrix units, and
    # the negative direction is DISCOVERED by exact grid search (never
    # hardcoded; restores the stage-1 M2 deleted-control discipline).
    choi_t = choi_of(_tp)
    psd_samples = ([[F(1), F(1)], [F(1), F(1)]],
                   [[F(2), F(1)], [F(1), F(1)]],
                   [[F(1), F(0)], [F(0), F(0)]])
    ck(all(_is_psd2(_tp(s)) for s in psd_samples),
       "transpose map must be positive on PSD samples")
    min_val = None
    min_wit = None
    for v in product(range(-1, 2), repeat=4):
        val = _quad(choi_t, [F(x) for x in v])
        if min_val is None or val < min_val:
            min_val = val
            min_wit = v
    ck(min_val is not None and min_val < 0,
       "grid search must discover a strictly negative transpose-Choi value")

    return _result(
        "check_L_kraus_choi_complete_positivity",
        ("A finite family of branch morphisms k_alpha (supplied branch form) "
         "gives the map Phi(x) = sum k x k*; its Choi matrix, computed by "
         "applying Phi to matrix units, equals the sum of vec outer products, "
         "is exactly PSD on a 625-point grid, and has rank equal to the "
         "number of independent branches; the complete family is trace "
         "preserving.  Complete positivity is a consequence of the supplied "
         "branch form; that events resolve into finitely many such branches "
         "is the named physical premise.  The transpose map is positive yet "
         "its computed Choi matrix takes a strictly negative value discovered "
         "by exact search: positivity does not imply complete positivity."),
        ["check_L_effects_povm_density_born"],
        {
            "kraus_count": len(kraus),
            "choi": _mat_str(choi),
            "choi_rank": _rank(choi),
            "transpose_choi": _mat_str(choi_t),
            "transpose_min_value": str(min_val),
            "transpose_min_witness": list(min_wit) if min_wit else None,
        },
        fails,
        premises=(tuple(premises_override) if premises_override is not None
                  else PREMISE_MANIFEST["check_L_kraus_choi_complete_positivity"]),
        negative_controls=(
            "transpose map: positive, computed Choi negative direction found",
        ),
    )


# ---------------------------------------------------------------------------
# L6. Composite soundness with an executed orientation-synchronization leg
# ---------------------------------------------------------------------------


def _rho_c(a: F, b: F) -> Matrix:
    """Realification of the complex scalar a + b i."""
    return [[a, -b], [b, a]]


def check_L_composite_orientation_synchronization(
        *, orientation_synchronized: bool = True,
        premises_override: Optional[Sequence[str]] = None) -> Dict[str, object]:
    fails: List[str] = []
    ck = _ckr(fails)

    zs = [(F(1), F(0)), (F(0), F(1)), (F(1), F(1)), (F(2), F(-3))]

    def embed_sync(z: Tuple[F, F]) -> Matrix:
        return _block_diag2(_rho_c(*z), _rho_c(*z))

    def embed_flipped(z: Tuple[F, F]) -> Matrix:
        a, b = z
        return _block_diag2(_rho_c(a, b), _rho_c(a, -b))

    embed = embed_sync if orientation_synchronized else embed_flipped

    j_central = _block_diag2(_rho_c(F(0), F(1)), _rho_c(F(0), F(1)))
    ck(_eq(_mm(j_central, j_central), _scal(F(-1), _eye(4))),
       "central J must satisfy J^2 = -I")

    def cmul(z: Tuple[F, F], w: Tuple[F, F]) -> Tuple[F, F]:
        return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])

    # The embedding of record must be a real-algebra homomorphism.
    for z in zs:
        for w in zs:
            ck(_eq(embed(cmul(z, w)), _mm(embed(z), embed(w))),
               "composite embedding must be multiplicative")

    # ORIENTATION_SYNCHRONIZED_EMBEDDINGS executes here: the embedding must
    # intertwine multiplication by i with the central J on every generator.
    iz = (F(0), F(1))
    for z in zs:
        ck(_eq(embed(cmul(iz, z)), _mm(j_central, embed(z))),
           "ORIENTATION_SYNCHRONIZED_EMBEDDINGS violated: embedding must "
           "intertwine i-multiplication with the central J")
        ck(_eq(_mm(j_central, embed(z)), _mm(embed(z), j_central)),
           "central J must commute with every embedded generator")

    # Executed adversary (restores stage-1 M9 / stage-2 MAJOR-3): the
    # conjugate (flipped-J) embedding is a genuine algebra homomorphism yet
    # MUST fail the intertwining gate -- computed, not asserted.
    flipped_is_hom = all(
        _eq(embed_flipped(cmul(z, w)), _mm(embed_flipped(z), embed_flipped(w)))
        for z in zs for w in zs)
    ck(flipped_is_hom,
       "flipped-J adversary must be a genuine homomorphism (not a strawman)")
    flipped_detected = any(
        not _eq(embed_flipped(cmul(iz, z)), _mm(j_central, embed_flipped(z)))
        for z in zs)
    ck(flipped_detected,
       "flipped-J (conjugate) embedding must FAIL the orientation gate")

    # GENERATOR_COMPLETENESS (Ruling 3): J is central only relative to the
    # generated algebra.  An element outside the generated span fails to
    # commute with J: LOCAL_J does not give CENTRAL_J without the gate.
    generators = [embed_sync(z) for z in zs]
    gen_rank = _span_rank(generators)
    ck(gen_rank == 2, "embedded scalars must span a rank-2 real algebra")
    outsider = _zero(4, 4)
    outsider[0][0] = F(1)  # E11, not in the embedded algebra
    ck(_span_rank(generators + [outsider]) == gen_rank + 1,
       "outsider element must lie outside the generated algebra")
    ck(not _eq(_mm(j_central, outsider), _mm(outsider, j_central)),
       "outsider must fail to commute with J: centrality holds only over "
       "the generated algebra, so GENERATOR_COMPLETENESS is load-bearing")

    return _result(
        "check_L_composite_orientation_synchronization",
        ("A composite of two complex-realified factors remains a complex "
         "object exactly when the local complex orientations are embedded "
         "synchronously: the synchronized diagonal embedding intertwines "
         "i-multiplication with the central J on every generator, while the "
         "conjugate (flipped-J) embedding -- a genuine algebra homomorphism "
         "-- fails the gate on a computed witness.  Orientation "
         "synchronization of physical embeddings is a named physical "
         "premise; it is executed here, not assumed.  Centrality of J holds "
         "only over the generated algebra (a computed outsider fails to "
         "commute), so generator completeness is a load-bearing named "
         "premise per Ruling 3: LOCAL_J + NATURALITY + ORIENTATION_"
         "SYNCHRONIZATION + GENERATOR_COMPLETENESS => CENTRAL_J."),
        ["check_L_kraus_choi_complete_positivity"],
        {
            "embedding": ("synchronized" if orientation_synchronized
                          else "flipped (adversary as embedding of record)"),
            "J_central": _mat_str(j_central),
            "flipped_adversary_is_homomorphism": flipped_is_hom,
            "flipped_adversary_detected": flipped_detected,
            "generated_algebra_rank": gen_rank,
        },
        fails,
        premises=(tuple(premises_override) if premises_override is not None
                  else PREMISE_MANIFEST["check_L_composite_orientation_synchronization"]),
        negative_controls=(
            "conjugate-embedding (flipped-J) adversary fails intertwining",
            "outsider E11 fails centrality outside the generated algebra",
        ),
    )


# ---------------------------------------------------------------------------
# L7. Kernel-death holonomy control
# ---------------------------------------------------------------------------


def check_L_kernel_death_holonomy_control(
        *, claim_live_when_dead: bool = False,
        premises_override: Optional[Sequence[str]] = None) -> Dict[str, object]:
    fails: List[str] = []
    ck = _ckr(fails)

    # Abstract loop quotient: Z2 = {e, L}, L nonidentity, L.L = e.
    elems = ("e", "L")
    table = {("e", "e"): "e", ("e", "L"): "L",
             ("L", "e"): "L", ("L", "L"): "e"}
    for a in elems:
        for b in elems:
            for c in elems:
                ck(table[(table[(a, b)], c)] == table[(a, table[(b, c)])],
                   "abstract loop table must be associative")
    ck(any(table[(a, a)] == "e" and a != "e" for a in elems),
       "abstract quotient must contain a nonidentity loop of order two")

    def image_order(rep: Mapping[str, Matrix]) -> int:
        for a in elems:
            for b in elems:
                ck(_eq(_mm(rep[a], rep[b]), rep[table[(a, b)]]),
                   "represented action must be a homomorphism")
        return len({_flat(rep[a]) for a in elems})

    # Dead representation: the operationally nonidentity loop is represented
    # by the identity.  The holonomy must be reported KILLED, never live.
    rep_dead = {"e": _eye(2), "L": _eye(2)}
    dead_order = image_order(rep_dead)
    dead_live = dead_order > 1
    ck(not dead_live,
       "represented image of the dead action must be trivial")
    ck(_eq(rep_dead["L"], _eye(2)),
       "dead action must represent the nonidentity loop as the identity")

    # Live control: a faithful representation keeps the holonomy live.
    rep_live = {"e": _eye(2), "L": [[F(1), F(0)], [F(0), F(-1)]]}
    live_order = image_order(rep_live)
    ck(live_order == 2, "live control must have image of order two")

    if claim_live_when_dead:
        ck(False,
           "kernel-death control: the abstract quotient is nontrivial but "
           "the represented action kills the loop; billing the holonomy as "
           "live is refused (conclusions live on the represented image, "
           "not the abstract quotient)")

    return _result(
        "check_L_kernel_death_holonomy_control",
        ("A quotient must not manufacture holonomy after the represented "
         "action kills it.  Witness: an abstract order-two loop quotient "
         "(operationally nonidentity loop) whose represented action is the "
         "identity has trivial represented image -- the holonomy is "
         "reported KILLED, and any attempt to bill it as live fails the "
         "check.  A faithful control representation keeps the holonomy "
         "live.  Conclusions are scoped to the generated represented image, "
         "which is why generator completeness is the consumed premise."),
        ["check_L_left_regular_convolution_representation"],
        {
            "abstract_quotient_order": len(elems),
            "dead_image_order": dead_order,
            "dead_holonomy_status": "KILLED",
            "dead_loop_billed_live": False,
            "live_control_image_order": live_order,
        },
        fails,
        premises=(tuple(premises_override) if premises_override is not None
                  else PREMISE_MANIFEST["check_L_kernel_death_holonomy_control"]),
        negative_controls=(
            "identity-represented nonidentity loop reported killed, not live",
        ),
    )


# ---------------------------------------------------------------------------
# L8. Operational quotient conservativity (Ruling 5 scoped principle)
# ---------------------------------------------------------------------------

DECLARED_CONTEXT_FAMILY: Tuple[str, ...] = (
    "left_readout", "right_readout", "balanced", "reversal_test")

MECHANISM_TABLE: Dict[str, Dict[str, object]] = {
    "hold_fed_exact_commit": {
        "readouts": (F(1), F(0), F(1, 2), F(1)),
        "cost_row": (F(1, 2),),
        "typing": "commit_mechanism",
    },
    "fiat_labelled_exact_commit": {
        "readouts": (F(1), F(0), F(1, 2), F(1)),
        "cost_row": (F(0),),
        "typing": "commit_mechanism",
    },
    "fiat_labelled_exact_commit_alias": {
        "readouts": (F(1), F(0), F(1, 2), F(1)),
        "cost_row": (F(0),),
        "typing": "commit_mechanism",
    },
    "biased_commit": {
        "readouts": (F(3, 4), F(1, 4), F(0), F(0)),
        "cost_row": (F(1, 2),),
        "typing": "commit_mechanism",
    },
}


def check_L_operational_quotient_conservativity(
        *, attempt_identification_of_cost_distinct: bool = False,
        premises_override: Optional[Sequence[str]] = None) -> Dict[str, object]:
    fails: List[str] = []
    ck = _ckr(fails)

    t = MECHANISM_TABLE

    def full_agreement(a: str, b: str) -> bool:
        return (t[a]["readouts"] == t[b]["readouts"]
                and t[a]["cost_row"] == t[b]["cost_row"]
                and t[a]["typing"] == t[b]["typing"])

    def readout_only_agreement(a: str, b: str) -> bool:
        return t[a]["readouts"] == t[b]["readouts"]

    # Ruling 1 standing: the grant is open; nothing here discharges it.
    g_hold_status = "OPEN_NAMED_GRANT (Ruling 1: discharge refused)"

    # hold-fed vs fiat: identical readouts, different cost rows.
    ck(readout_only_agreement("hold_fed_exact_commit",
                              "fiat_labelled_exact_commit"),
       "hold/fiat pair must agree on every declared readout")
    ck(t["hold_fed_exact_commit"]["cost_row"]
       != t["fiat_labelled_exact_commit"]["cost_row"],
       "hold/fiat pair must differ on an admissible cost row")
    ck(not full_agreement("hold_fed_exact_commit",
                          "fiat_labelled_exact_commit"),
       "conservative congruence must separate the cost-distinct pair")

    # The readout-only quotient identifies a cost-separated pair: it is the
    # named failure predicate, computed (not asserted).
    readout_only_nonconservative = (
        readout_only_agreement("hold_fed_exact_commit",
                               "fiat_labelled_exact_commit")
        and not full_agreement("hold_fed_exact_commit",
                               "fiat_labelled_exact_commit"))
    ck(readout_only_nonconservative,
       "readout-only quotient must be flagged as the failure predicate")

    if attempt_identification_of_cost_distinct:
        ck(False,
           NONCONSERVATIVE_OPERATIONAL_QUOTIENT + ": identification of "
           "mechanisms separated by an admissible cost row is refused "
           "(Ruling 5); two mechanisms with identical readouts but "
           "different cost rows must NOT be identified")

    # Licensed identification: full agreement on readouts, cost rows, and
    # typing, relative to the declared context family and exact resolution.
    ck(full_agreement("fiat_labelled_exact_commit",
                      "fiat_labelled_exact_commit_alias"),
       "fully agreeing pair must be identifiable relative to the declared "
       "context family and resolution")

    # Readout-separated pair stays separated by any congruence.
    ck(not readout_only_agreement("hold_fed_exact_commit", "biased_commit"),
       "readout-distinct mechanisms must remain separated")

    return _result(
        "check_L_operational_quotient_conservativity",
        ("Quotient-nullity may be concluded only relative to a declared "
         "context family and resolution, and only when all declared "
         "readouts, cost/ledger consequences, and physical typing agree "
         "(Ruling 5).  Witness: a hold-fed and a fiat-labelled mechanism "
         "with identical readouts but different cost rows are NOT "
         "identified; the readout-only quotient that would merge them is "
         "computed to fire the named failure predicate "
         "NONCONSERVATIVE_OPERATIONAL_QUOTIENT.  A pair agreeing on "
         "readouts, cost rows, and typing is identifiable relative to the "
         "declared family.  G_HOLD_EXACT remains an open named grant "
         "(Ruling 1); this check computes nothing that discharges it."),
        [],
        {
            "declared_context_family": list(DECLARED_CONTEXT_FAMILY),
            "resolution": "exact",
            "g_hold_exact_status": g_hold_status,
            "failure_predicate": NONCONSERVATIVE_OPERATIONAL_QUOTIENT,
            "readout_only_quotient_nonconservative":
                readout_only_nonconservative,
            "mechanisms": {
                k: {"readouts": [str(x) for x in v["readouts"]],
                    "cost_row": [str(x) for x in v["cost_row"]],
                    "typing": v["typing"]}
                for k, v in t.items()},
        },
        fails,
        premises=(tuple(premises_override) if premises_override is not None
                  else PREMISE_MANIFEST["check_L_operational_quotient_conservativity"]),
        negative_controls=(
            "readout-only quotient merges a cost-separated pair: flagged",
        ),
        epistemic="P_structural_instrument",
    )


# ---------------------------------------------------------------------------
# L9. Pro-C* fragment assembly with named functoriality premise
# ---------------------------------------------------------------------------

Fragment = Tuple[Matrix, Tuple[F, ...]]  # (M2(R) part, C^n scalar part)


def _frag_mul(x: Fragment, y: Fragment) -> Fragment:
    return (_mm(x[0], y[0]), tuple(a * b for a, b in zip(x[1], y[1])))


def _frag_star(x: Fragment) -> Fragment:
    return (_tp(x[0]), x[1])


def _frag_restrict(x: Fragment, m: int) -> Fragment:
    return (x[0], x[1][:m])


def check_L_pro_cstar_fragment_functoriality(
        *, break_composition: bool = False,
        premises_override: Optional[Sequence[str]] = None) -> Dict[str, object]:
    fails: List[str] = []
    ck = _ckr(fails)

    # Fragment algebras A_n = M2(R) (+) C^n, n = 1..5; bonding map drops the
    # last scalar coordinate.  The matrix summand keeps the witness genuinely
    # noncommutative (answers stage-2 m8 honestly).
    e12 = [[F(0), F(1)], [F(0), F(0)]]
    e21 = [[F(0), F(0)], [F(1), F(0)]]
    ck(not _eq(_mm(e12, e21), _mm(e21, e12)),
       "fragment witness must contain a noncommutative pair")

    def samples(n: int) -> List[Fragment]:
        return [
            (_eye(2), tuple(F(1) for _ in range(n))),
            (e12, tuple(F(i - 1) for i in range(n))),
            (e21, tuple(F((-1) ** i) for i in range(n))),
            ([[F(1), F(2)], [F(3), F(-1)]],
             tuple(F(i + 1, 2) for i in range(n))),
        ]

    def bonding(x: Fragment, n_from: int, n_to: int) -> Fragment:
        # one-step bonding A_n -> A_{n-1}
        if break_composition and (n_from, n_to) == (4, 3):
            # broken variant: drops the FIRST scalar instead of the last
            return (x[0], x[1][1:])
        return (x[0], x[1][:-1])

    def chain(x: Fragment, n_from: int, n_to: int) -> Fragment:
        cur = x
        for n in range(n_from, n_to, -1):
            cur = bonding(cur, n, n - 1)
        return cur

    # Star-homomorphism legs on every one-step bonding, checked on all
    # sample pairs plus the full scalar basis (delta_i . delta_j cases).
    for n in range(2, 6):
        for x in samples(n):
            for y in samples(n):
                ck(bonding(_frag_mul(x, y), n, n - 1)
                   == _frag_mul(bonding(x, n, n - 1), bonding(y, n, n - 1)),
                   "bonding map must preserve multiplication")
                ck(bonding(_frag_star(x), n, n - 1)
                   == _frag_star(bonding(x, n, n - 1)),
                   "bonding map must preserve the involution")
        for i in range(n):
            for j in range(n):
                di: Fragment = (_zero(2, 2),
                                tuple(F(1) if k == i else F(0) for k in range(n)))
                dj: Fragment = (_zero(2, 2),
                                tuple(F(1) if k == j else F(0) for k in range(n)))
                ck(bonding(_frag_mul(di, dj), n, n - 1)
                   == _frag_mul(bonding(di, n, n - 1), bonding(dj, n, n - 1)),
                   "bonding must preserve products of all scalar basis pairs")
        # Computed surjectivity: every target basis element has a preimage.
        target_dim = 4 + (n - 1)
        image_vecs = []
        for k in range(4):
            m = _zero(2, 2)
            m[k // 2][k % 2] = F(1)
            img = bonding((m, tuple(F(0) for _ in range(n))), n, n - 1)
            image_vecs.append(list(_flat(img[0])) + list(img[1]))
        for i in range(n):
            src: Fragment = (_zero(2, 2),
                             tuple(F(1) if k == i else F(0) for k in range(n)))
            img = bonding(src, n, n - 1)
            image_vecs.append(list(_flat(img[0])) + list(img[1]))
        ck(_rank(image_vecs) == target_dim,
           "one-step bonding must be surjective (computed rank)")

    # RESTRICTION_FUNCTORIALITY executes as composition coherence: the
    # staged chain of one-step bondings equals the direct restriction.
    for x in samples(5):
        for n_to in (1, 2, 3):
            ck(chain(x, 5, n_to) == _frag_restrict(x, n_to),
               "staged bonding chain must equal the direct restriction "
               "(functorial coherence)")

    # Class-splitting control (stage-1 m12, honest direction split): the
    # pullback along a class-splitting projection is an injective unital
    # *-homomorphism, NOT one of the surjective restrictions used above.
    def pullback(v: Tuple[F, F]) -> Tuple[F, F, F]:
        return (v[0], v[0], v[1])  # coarse classes {0,1} split from class 0

    for a in [(F(1), F(0)), (F(0), F(1)), (F(2), F(-3))]:
        for b in [(F(1), F(1)), (F(1, 2), F(3))]:
            ck(pullback((a[0] * b[0], a[1] * b[1]))
               == tuple(x * y for x, y in zip(pullback(a), pullback(b))),
               "class-splitting pullback must be multiplicative")
    ck(pullback((F(1), F(1))) == (F(1), F(1), F(1)),
       "class-splitting pullback must be unital")
    pb_rank = _rank([list(pullback((F(1), F(0)))),
                     list(pullback((F(0), F(1))))])
    ck(pb_rank == 2, "class-splitting pullback must be injective")
    ck(pb_rank < 3,
       "class-splitting pullback must NOT be surjective: refinement "
       "class-splitting is the injective direction, distinct from the "
       "surjective restrictions this system declares")

    return _result(
        "check_L_pro_cstar_fragment_functoriality",
        ("A directed system of finite fragment algebras A_n = M2(R) (+) C^n "
         "with declared one-step restrictions forms a coherent inverse "
         "system: every bonding map is a computed-surjective unital "
         "*-homomorphism (multiplicativity verified on generic and full "
         "basis pairs, including a genuinely noncommutative summand), and "
         "staged chains equal direct restrictions exactly.  That physical "
         "fragment restrictions compose functorially is the NAMED premise "
         "RESTRICTION_FUNCTORIALITY; that the declared fragment system is "
         "adequate is FRAGMENT_SYSTEM_ADEQUACY.  The class-splitting "
         "refinement direction is exhibited as an injective non-surjective "
         "pullback, distinct from the declared surjective restrictions; no "
         "claim is made about refinement systems this witness does not "
         "contain."),
        ["check_L_composite_orientation_synchronization"],
        {
            "fragment_algebras": ["M2(R) (+) C^%d" % n for n in range(1, 6)],
            "bonding": "drop the last scalar coordinate",
            "noncommutative_witness": True,
            "composition_chains_checked": [(5, 1), (5, 2), (5, 3)],
            "class_splitting_pullback_rank": pb_rank,
        },
        fails,
        premises=(tuple(premises_override) if premises_override is not None
                  else PREMISE_MANIFEST["check_L_pro_cstar_fragment_functoriality"]),
        negative_controls=(
            "class-splitting pullback: injective, not surjective",
        ),
    )


# ---------------------------------------------------------------------------
# L10. Provenance coderef existence instrument
# ---------------------------------------------------------------------------


def check_L_provenance_coderef_existence(
        *, extra_rows: Sequence[Mapping[str, object]] = (),
        premises_override: Optional[Sequence[str]] = None) -> Dict[str, object]:
    fails: List[str] = []
    ck = _ckr(fails)

    defined = set(_ALL_CHECKS)
    ck(set(MODULE_CODEREF_ALLOWLIST) == defined,
       "coderef allowlist must match the actually defined checks set-exactly")

    rows = list(PROVENANCE_TABLE) + list(extra_rows)
    for row in rows:
        coderef = str(row.get("coderef", ""))
        ck(coderef in MODULE_CODEREF_ALLOWLIST,
           "provenance coderef %r is not in the allowlist" % coderef)
        ck(coderef in defined,
           "provenance coderef %r does not exist in this module "
           "(phantom coderef; stage-1 M7 class)" % coderef)
        src = str(row.get("packet_source", ""))
        ck(src in PACKET_SOURCE_ALLOWLIST,
           "provenance source %r is not in the source allowlist" % src)
        for finding in row.get("audit_findings", ()):
            ck(finding in AUDIT_FINDING_ALLOWLIST,
               "audit finding tag %r is not in the finding allowlist"
               % (finding,))
    covered = {row["coderef"] for row in PROVENANCE_TABLE}
    ck(covered == defined,
       "every defined check must carry a provenance row")

    return _result(
        "check_L_provenance_coderef_existence",
        ("Every provenance row names a coderef that exists in this module "
         "(checked against both the separately maintained allowlist and the "
         "computed check registry), a packet/audit source from the source "
         "allowlist, and audit-finding tags from the finding allowlist; and "
         "every defined check carries a provenance row.  Answers the "
         "stage-1 M7 phantom-coderef class."),
        [],
        {
            "provenance_rows": len(rows),
            "defined_checks": sorted(defined),
        },
        fails,
        premises=(tuple(premises_override) if premises_override is not None
                  else PREMISE_MANIFEST["check_L_provenance_coderef_existence"]),
        epistemic="P_structural_instrument",
    )


# ---------------------------------------------------------------------------
# L11. Physical premise reconciliation instrument
# ---------------------------------------------------------------------------


def check_L_physical_premise_reconciliation(
        results: Optional[Mapping[str, Mapping[str, object]]] = None
) -> Dict[str, object]:
    fails: List[str] = []
    ck = _ckr(fails)

    if results is None:
        results = {name: fn() for name, fn in _CHECKS.items()}
    results = {k: v for k, v in results.items()
               if k != "check_L_physical_premise_reconciliation"}

    expected_names = set(PREMISE_MANIFEST) - {
        "check_L_physical_premise_reconciliation"}
    ck(set(results) == expected_names,
       "reconciliation requires exactly the full check battery")

    # The consumed union is COMPUTED from the actual results (the dependency
    # graph's leaves), then compared set-exactly against the separately
    # maintained PHYSICAL_PREMISES manifest.  Never a literal against itself
    # (stage-2 MAJOR-1/MAJOR-2; Ruling 2).
    consumed_union = set()
    for name, r in results.items():
        premises = tuple(r.get("premises", ()))
        consumed_union.update(premises)
        ck(r.get("physical_premises_certified") is False,
           "check %s must declare physical_premises_certified=False" % name)
        for p in premises:
            ck(p in PHYSICAL_PREMISES,
               "check %s consumes an undeclared premise/root %r "
               "(second-empirical-root class)" % (name, p))
        expected = PREMISE_MANIFEST.get(name)
        if expected is None:
            ck(False, "check %s has no PREMISE_MANIFEST entry" % name)
        else:
            ck(premises == tuple(expected),
               "premise-manifest mismatch for %s: consumed %r, manifest %r"
               % (name, premises, tuple(expected)))

    ck(consumed_union == set(PHYSICAL_PREMISES),
       "computed consumed-premise union must equal PHYSICAL_PREMISES "
       "set-exactly; difference: %r"
       % sorted(consumed_union.symmetric_difference(PHYSICAL_PREMISES)))

    for p in PHYSICAL_PREMISES:
        typing = PREMISE_TYPING.get(p)
        ck(typing is not None and typing.get("type") == "physical",
           "premise %s must carry a physical typing entry" % p)

    # Dependency graph: every declared dependency exists and the graph is
    # acyclic (computed DFS).
    graph = {name: tuple(r.get("dependencies", ()))
             for name, r in results.items()}
    for name, deps in graph.items():
        for d in deps:
            ck(d in graph,
               "check %s depends on unknown check %r" % (name, d))

    visiting: List[str] = []
    visited = set()
    cycle_found = []

    def dfs(node: str) -> None:
        if node in visiting:
            cycle_found.append(tuple(visiting[visiting.index(node):] + [node]))
            return
        if node in visited:
            return
        visiting.append(node)
        for d in graph.get(node, ()):
            dfs(d)
        visiting.pop()
        visited.add(node)

    for node in graph:
        dfs(node)
    ck(not cycle_found, "check dependency graph must be acyclic")

    return _result(
        "check_L_physical_premise_reconciliation",
        ("The union of physical premises actually consumed by the check "
         "battery, computed from the returned results, equals the "
         "separately maintained PHYSICAL_PREMISES manifest set-exactly; "
         "each check's consumed list matches its PREMISE_MANIFEST row; "
         "every consumed name is a declared physical premise (a second "
         "empirical root fails); every premise carries a physical typing "
         "entry; every result declares physical_premises_certified=False; "
         "and the check dependency graph is acyclic with resolvable "
         "edges.  This is bookkeeping over the conditional lemmas; it "
         "establishes no physical premise."),
        sorted(results),
        {
            "consumed_premise_union": sorted(consumed_union),
            "manifest": sorted(PHYSICAL_PREMISES),
            "checks_reconciled": len(results),
            "dependency_cycles": [list(c) for c in cycle_found],
        },
        fails,
        premises=PREMISE_MANIFEST["check_L_physical_premise_reconciliation"],
        epistemic="P_structural_instrument",
    )


# ---------------------------------------------------------------------------
# Registry / runner
# ---------------------------------------------------------------------------

_CHECKS = {
    "check_L_left_regular_convolution_representation":
        check_L_left_regular_convolution_representation,
    "check_L_conjugated_finite_haar_invariant_form":
        check_L_conjugated_finite_haar_invariant_form,
    "check_L_nonexpansion_pair_forces_isometry":
        check_L_nonexpansion_pair_forces_isometry,
    "check_L_effects_povm_density_born":
        check_L_effects_povm_density_born,
    "check_L_kraus_choi_complete_positivity":
        check_L_kraus_choi_complete_positivity,
    "check_L_composite_orientation_synchronization":
        check_L_composite_orientation_synchronization,
    "check_L_kernel_death_holonomy_control":
        check_L_kernel_death_holonomy_control,
    "check_L_operational_quotient_conservativity":
        check_L_operational_quotient_conservativity,
    "check_L_pro_cstar_fragment_functoriality":
        check_L_pro_cstar_fragment_functoriality,
    "check_L_provenance_coderef_existence":
        check_L_provenance_coderef_existence,
}

_ALL_CHECKS = tuple(list(_CHECKS) + ["check_L_physical_premise_reconciliation"])


def run_all() -> Dict[str, Dict[str, object]]:
    results = {name: fn() for name, fn in _CHECKS.items()}
    results["check_L_physical_premise_reconciliation"] = (
        check_L_physical_premise_reconciliation(results=dict(results)))
    return results


if __name__ == "__main__":
    import sys

    all_results = run_all()
    width = max(len(n) for n in all_results)
    print("finite_representation_lemmas -- conditional finite lemmas "
          "(no physical premise established)")
    print("licensed claim: " + LICENSED_CLAIM)
    print("-" * 72)
    for check_name, res in all_results.items():
        print("%s  %s  premises=%s"
              % (check_name.ljust(width), res["status"],
                 ",".join(res["premises"]) or "-"))
    n_pass = sum(1 for r in all_results.values() if r["passed"])
    print("-" * 72)
    print("checks: %d  pass: %d  fail: %d  physical premises named: %d"
          % (len(all_results), n_pass, len(all_results) - n_pass,
             len(PHYSICAL_PREMISES)))
    sys.exit(0 if n_pass == len(all_results) else 1)


# Bank-landing registration wiring (v24.3.432): standard registry hook.
_BANK_CHECKS = {
    "L_left_regular_convolution_representation": check_L_left_regular_convolution_representation,
    "L_conjugated_finite_haar_invariant_form": check_L_conjugated_finite_haar_invariant_form,
    "L_nonexpansion_pair_forces_isometry": check_L_nonexpansion_pair_forces_isometry,
    "L_effects_povm_density_born": check_L_effects_povm_density_born,
    "L_kraus_choi_complete_positivity": check_L_kraus_choi_complete_positivity,
    "L_composite_orientation_synchronization": check_L_composite_orientation_synchronization,
    "L_kernel_death_holonomy_control": check_L_kernel_death_holonomy_control,
    "L_operational_quotient_conservativity": check_L_operational_quotient_conservativity,
    "L_pro_cstar_fragment_functoriality": check_L_pro_cstar_fragment_functoriality,
    "L_provenance_coderef_existence": check_L_provenance_coderef_existence,
    "L_physical_premise_reconciliation": check_L_physical_premise_reconciliation,
}


def register(registry):
    registry.update(_BANK_CHECKS)
    return registry
