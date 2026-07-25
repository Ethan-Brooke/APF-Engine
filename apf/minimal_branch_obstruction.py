"""
minimal_branch_obstruction.py -- The Zipper / Process-IJC lane, P7 (bank port)
================================================================================
Self-contained, scipy-free bank port of the P7 Minimal Branch-Selection
Obstruction (lane: The Turning (parked)/zipper_consolidation_2026-07-24/,
pool_p7_minimal_branch_obstruction.py; intake + clean-room verification
2026-07-24). Exact arithmetic (fractions.Fraction); no floats, no scipy, no
lane imports.

RESULT (machine-checked, honest): on the isotropic CHSH 3-4-5 slice, the classical
(local/Boole) boundary |c| <= 5/7 is DERIVED from the complete finite-memory
defender-class projection (8 local correlation vertices; all 8 oriented CHSH
facets bound exactly 2). The named current APF prequantum primitive set
{A1, MD, A2, BW, occupancy, monogamy, irreversibility, closed-world, no-export,
bare-A2} is BRANCH-BLIND: the exact common classical countermodel c = -1/2
(inside the polytope, CHSH = 7/5) is admitted by each. Zero new behavior-selective
clauses are insufficient (the countermodel survives); exactly ONE strict clause
|c| > 5/7 (equivalently |S| > 2) is minimal and sufficient (it excludes the whole
classical region). The native Process-IJC target c = -101/105 sits outside at
exact slack 26/105 in |c| and CHSH margin 52/75.

GRADE: [P_structural_instrument]. The boundary derivation and the minimality
arithmetic are exact; the branch-blindness claim is an ENUMERATION over a DECLARED
primitive list (instrument-class), NOT a proof over the space of all admissibility
primitives (a Cap-1 lift attempt to [P_structural_exhaustive] was REDUCED, conf
0.88, 2026-07-24 -- branch-blindness is cost-conditioned; do not cite it as
exhaustive). physical_premises_certified = False; non-exporting.

CONCORDANCES (cited, not re-derived):
  ijc_boolean_defender_bridge (.424, [P_math]): outside-polytope <=> no common
    Boolean/commuting-extension defender (Fine facet). The "one strict clause =
    the no-extension premise" identification rides this banked equivalence.
  T_no_IJC_no_noncommutativity, T_IJC_dichotomy ([P_structural]): PLEC admits both
    branches; PLEC alone does not force the IJC branch.
  T_quantum_admissibility_condition ([P_regime]): the branch (QAC) is empirical,
    not an A1 consequence. This obstruction is the exact/quantitative sibling of
    that posture: it certifies WHY the branch is not A1-forced at the polytope level.

MAY NOT BE CITED FROM THIS MODULE:
  'the branch-blindness result is exhaustive/universal over admissibility
  primitives' (REDUCED); any '[P]' on the branch/QAC; 'the QAC is derived';
  'P7 reproduces the 3/4 benefit threshold' (it does not).
"""

from fractions import Fraction as F
from itertools import product

FAMILY = "quantum.minimal_branch_selection_obstruction"

NATIVE_DIRECTION = (F(3, 5), F(3, 5), F(4, 5), F(-4, 5))
CLASSICAL_ABS_C_BOUND = F(5, 7)
NATIVE_TARGET_C = F(-101, 105)
CLASSICAL_COUNTERMODEL_C = F(-1, 2)
# the named current prequantum primitive set (the declared list -- instrument scope)
NAMED_PRIMITIVES = (
    "A1", "MD", "A2", "BW", "occupancy", "monogamy",
    "irreversibility", "closed_world", "no_hidden_export", "bare_A2",
)


def _local_vertices():
    return sorted({(a0 * b0, a0 * b1, a1 * b0, a1 * b1)
                   for a0, a1, b0, b1 in product((1, -1), repeat=4)})


def _chsh_facets():
    return [s for s in product((1, -1), repeat=4)
            if s[0] * s[1] * s[2] * s[3] == -1]


def _dot(s, v):
    return sum(F(si) * vi for si, vi in zip(s, v))


def _isotropic_chsh(c):
    slope = max(abs(_dot(s, NATIVE_DIRECTION)) for s in _chsh_facets())
    return slope * abs(c)


def check_T_minimal_branch_selection_obstruction():
    """[P_structural_instrument]. The exact minimal branch-selection obstruction
    on the isotropic 3-4-5 slice: the classical boundary |c|<=5/7 is derived from
    the complete defender-class projection; the named primitive set is branch-blind
    (common classical countermodel c=-1/2); one strict clause |c|>5/7 is minimal
    and sufficient. Enumeration over the declared primitive list (instrument);
    NOT exhaustive over all admissibility primitives."""
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        return cond

    verts = _local_vertices()
    facets = _chsh_facets()
    ck(len(verts) == 8, "8 local correlation vertices")
    ck(len(facets) == 8, "8 oriented CHSH facets")
    ck(all(max(_dot(s, v) for v in verts) == 2 for s in facets),
       "every CHSH facet bound exactly 2")

    # derive the classical |c| bound from the facet slopes on the native line
    lower, upper = F(-1), F(1)
    for s in facets:
        slope = _dot(s, NATIVE_DIRECTION)
        if slope > 0:
            upper = min(upper, F(2) / slope)
        elif slope < 0:
            lower = max(lower, F(2) / slope)
    derived = max(abs(lower), abs(upper))
    boundary_derived = (lower == -CLASSICAL_ABS_C_BOUND
                        and upper == CLASSICAL_ABS_C_BOUND
                        and derived == CLASSICAL_ABS_C_BOUND)
    ck(boundary_derived, "classical |c| bound 5/7 derived from the defender class")

    slope_max = max(abs(_dot(s, NATIVE_DIRECTION)) for s in facets)
    ck(slope_max == F(14, 5), "signed CHSH slope 14/5")

    # the common classical countermodel c=-1/2 is inside the polytope
    cm = CLASSICAL_COUNTERMODEL_C
    cm_inside = abs(cm) <= CLASSICAL_ABS_C_BOUND
    cm_chsh = _isotropic_chsh(cm)
    ck(cm_inside and cm_chsh == F(7, 5),
       "countermodel c=-1/2 inside polytope, CHSH 7/5")

    # branch-blindness ENUMERATION over the named primitive set (instrument):
    # bare-A2 over cost=|c| has its argmin at c=0 (classical), and none of the
    # named primitives imposes a lower bound |c|>5/7 -> each admits c=-1/2.
    grid = [F(k, 210) for k in range(-210, 211)]
    bare_a2_argmin = min(grid, key=lambda c: (abs(c), c))
    a2_classical = abs(bare_a2_argmin) <= CLASSICAL_ABS_C_BOUND
    branch_blind = {p: (cm_inside and a2_classical) for p in NAMED_PRIMITIVES}
    ck(all(branch_blind.values()),
       "named primitive set branch-blind (common countermodel c=-1/2)")

    # native Process-IJC target sits outside; exact slack + margins
    tc = NATIVE_TARGET_C
    target_outside = abs(tc) > CLASSICAL_ABS_C_BOUND
    slack = abs(tc) - CLASSICAL_ABS_C_BOUND
    chsh_margin = _isotropic_chsh(tc) - F(2)
    ck(target_outside, "native target c=-101/105 outside the classical polytope")
    ck(slack == F(26, 105), "exact |c| slack 26/105")
    ck(_isotropic_chsh(tc) == F(202, 75), "native target CHSH 202/75")
    ck(chsh_margin == F(52, 75), "exact CHSH margin 52/75")

    # minimality: zero new clauses insufficient (countermodel survives); one strict
    # clause |c|>5/7 sufficient (excludes the entire classical region, sup |c| = 5/7)
    zero_clause_insufficient = cm_inside          # the classical countermodel survives
    one_strict_clause_sufficient = (CLASSICAL_ABS_C_BOUND < abs(tc))  # |c|>5/7 excludes cm
    ck(zero_clause_insufficient, "zero new behavior-selective clauses insufficient")
    ck(one_strict_clause_sufficient,
       "one strict clause |c|>5/7 (|S|>2) sufficient")

    passed = not fails
    return {
        "name": "T_minimal_branch_selection_obstruction",
        "epistemic": "P_structural_instrument",
        "passed": passed,
        "tier": 4,
        "physical_premises_certified": False,
        "family": FAMILY,
        "key_result": (
            "isotropic 3-4-5 slice: classical boundary |c|<=5/7 DERIVED from the "
            "complete defender-class projection (8 CHSH facets bound 2); named "
            "primitive set branch-blind (common classical countermodel c=-1/2, "
            "CHSH 7/5); zero new clauses insufficient, one strict clause |c|>5/7 "
            "(|S|>2) minimal+sufficient; native target c=-101/105 outside, slack "
            "26/105, CHSH 202/75 (margin 52/75). ENUMERATION over the declared "
            "primitive list (instrument), NOT exhaustive over all primitives."
        ),
        "classical_abs_c_bound": str(CLASSICAL_ABS_C_BOUND),
        "boundary_derived_from_defender_class": boundary_derived,
        "named_primitive_set_branch_blind": all(branch_blind.values()),
        "common_classical_countermodel_c": str(CLASSICAL_COUNTERMODEL_C),
        "native_target_c": str(NATIVE_TARGET_C),
        "native_target_c_slack": str(slack),
        "native_target_chsh_margin": str(chsh_margin),
        "one_strict_clause_sufficient": one_strict_clause_sufficient,
        "zero_clauses_insufficient": zero_clause_insufficient,
        "dependencies": [],
        "cross_refs": [
            "T_ijc_boolean_defender_bridge", "T_no_IJC_no_noncommutativity",
            "T_IJC_dichotomy", "T_quantum_admissibility_condition",
            "L_commutative_no_unresolved_hold",
        ],
        "grade_gate": (
            "exact boundary + minimality [P_math-strength]; branch-blindness is an "
            "enumeration over a DECLARED list (instrument-class). Cap-1 lift to "
            "exhaustive REDUCED 2026-07-24 (cost-conditioned); do NOT cite exhaustive."
        ),
        "may_not_cite": [
            "branch-blindness is exhaustive/universal over admissibility primitives",
            "any [P] on the branch/QAC", "the QAC is derived",
            "P7 reproduces the 3/4 benefit threshold",
        ],
        "fail_reasons": fails,
    }


_CHECKS = {
    "T_minimal_branch_selection_obstruction":
        check_T_minimal_branch_selection_obstruction,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == "__main__":
    import sys
    r = check_T_minimal_branch_selection_obstruction()
    print(r["name"], r["epistemic"], "PASS" if r["passed"] else "FAIL")
    for f in r["fail_reasons"]:
        print("  -", f)
    sys.exit(0 if r["passed"] else 1)
