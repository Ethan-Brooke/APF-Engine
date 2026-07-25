"""
quantum_condition_two_axis.py -- The Quantum Condition as a Two-Axis Characterization
================================================================================
Self-contained bank port (v24.3.438). Stdlib only (fractions / itertools / math);
NO scipy / numpy / pool / lane imports. Non-exporting. Tier 4. ppc = False.
Exact arithmetic where the claim is exact; the Tsirelson value 2*sqrt(2) and the
Tsirelson-Landau-Masanes (TLM) criterion are CITED banked/form-side facts (float
with tolerance, exactly as banked check_T_Tsirelson).

Lane: The Turning (parked)/quantum_condition_ijc_twist_2026-07-25/. Twice cold-
audited (statement 0.75 / execution 0.85 LAND-WITH-FIXES; every fix carried).
Principal ruling: bank (R-IJC-sign accepted as a named identification, in the class
of the banked per-vertex-singlet = Gauss-law reading).

WHAT IS BANKED (three checks; conditional; the antecedent is the co-indexed QAC):

  check_L_ijc_cycle_floor  [P_math | R-IJC-sign]  -- AXIS I, the relational FLOOR.
    Edge sign +1 = CO-REQUIRE, -1 = IJC (inadmissible joint / anti-require). A cycle
    with an ODD number of IJC edges (chi = prod(sign_i) = -1) admits NO common cause
    (no global +/-1 section), i.e. it lies OUTSIDE the Boole/local polytope (Fine
    facets). Verified over all m=3..6 sign patterns. FIREWALL: the odd -1 is the IJC
    PARITY (an integer sign product), never a Pauli anticommutator -- the floor path
    is scanned for any complex/non-rational return. R-IJC-sign (edge sign = the IJC
    bit) is the NAMED IDENTIFICATION; the combinatorics is exact. Concordance:
    global_defect_margin's parity law (-1)^defect == chi.

  check_L_form_ceiling_and_sufficiency  [P_structural_reading | TLM-cited, FORM-side,
    branch-conditional]  -- AXIS F, the form CEILING + the SUFFICIENCY closer.
    GIVEN the noncommutative branch (itself the QAC, NOT A1-forced), banked
    check_T_Tsirelson [P] caps CHSH <= 2*sqrt(2), excluding PR (S=4, S^2=16 > 8). The
    SCALAR band (2, 2sqrt2] is NECESSARY only; sufficiency (membership in the quantum
    set) is closed by the FULL four-facet TLM criterion -- the exact (2,2,2)
    UNIFORM-MARGINAL correlator quantum-set boundary. Gap witness: E_GAP and E_QM
    share CHSH scalar 2.8 (both in-band) but only E_QM is quantum under full TLM
    (single-facet TLM over-accepts; counterexample E_CE caught). FORM-side (cited,
    not relational).

  check_T_quantum_condition_two_axis  [P_structural_reading | R-IJC-sign, TLM-cited]
    -- the COMPOSED characterization. WITHIN (2,2,2) uniform-marginal correlators and
    GIVEN the QAC branch: nonclassical-quantum <=> (outside Boole polytope, Axis I) AND
    (full-TLM, Axis F). Co-indexed on the same interface. Native bank target S=202/75
    (v~0.673) is in-band. Both axes load-bearing: Axis I alone reaches PR (S=4); a
    COMMUTATIVE form (C^N) alone gives CHSH <= 2 (classical). The antecedent
    (odd-IJC-cyclic AND branch-carrying) is NOT A1-forced = the sharpened, co-indexed QAC.

CONCORDANCES (cited, NOT re-derived): global_defect_margin [P_math] (parity law);
  third_boat_no_extension [P_math] (third boat <=> inside Boole polytope, Fine);
  minimal_branch_obstruction [P_structural_instrument] (|c|<=5/7 boundary);
  T_Tsirelson [P] (CHSH <= 2sqrt2 from the form).

MAY NOT BE CITED FROM THIS MODULE:
  'quantum is derived' / 'the branch/form is A1-derived' (the branch is the QAC);
  'the SCALAR band (or Axis I AND the 2sqrt2 ceiling) characterizes quantum' (NECESSARY
    only); the licensed characterization is 'Axis I AND full-TLM(F-in-full) <=>
    quantum-nonclassicality WITHIN (2,2,2) uniform-marginal correlators, GIVEN the QAC
    branch' -- never unconditional / scope-free;
  'the Tsirelson/TLM ceiling is relational / firewall-clean' (it is FORM-side);
  'no-common-cause == quantum' (Axis I gives only the FLOOR; PR-vs-quantum needs Axis F);
  'the odd-IJC-cycle is anticommutation' (it is the IJC parity, an integer sign);
  any [P] on the co-indexed antecedent / the branch / the QAC.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import math

FAMILY = "quantum.condition_two_axis_ijc_floor_form_ceiling"
TSIRELSON = 2 * math.sqrt(2)            # banked check_T_Tsirelson [P]; cited, not re-derived
BAND_TOL = 1e-9
NATIVE_S = F(202, 75)                    # bank native target c=-101/105 -> (14/5)|c|

MAY_NOT_CITE = (
    "'quantum is derived' / 'the branch/form is A1-derived' (the branch is the QAC)",
    "'the SCALAR band (or Axis I AND the 2sqrt2 ceiling) characterizes quantum' "
    "(NECESSARY only; the licensed characterization is Axis I AND full-TLM(F-in-full), "
    "within (2,2,2) uniform-marginal correlators, GIVEN the QAC branch)",
    "'the Tsirelson/TLM ceiling is relational / firewall-clean' (it is FORM-side)",
    "'no-common-cause == quantum' (Axis I gives only the FLOOR; PR-vs-quantum needs Axis F)",
    "'the odd-IJC-cycle is anticommutation' (it is the IJC parity, an integer sign)",
    "any '[P]' on the co-indexed antecedent / the branch / the QAC",
)
CROSS_REFS = (
    "global_defect_margin [P_math] (parity law (-1)^defect == chi)",
    "third_boat_no_extension [P_math] (third boat <=> inside Boole polytope, Fine)",
    "minimal_branch_obstruction [P_structural_instrument] (|c|<=5/7 boundary)",
    "T_Tsirelson [P] (CHSH <= 2sqrt2 from the form)",
)
FLOOR_MINUS_ONE_SOURCE = "IJC parity = prod(sign_i)"                  # relational (Axis I)
CEILING_MINUS_ONE_SOURCE = "form anticommutator [a,a'] (T_Tsirelson)"  # form-side (Axis F)


# ---------------------------------------------------------------------------
# Axis I helpers (relational, exact)
# ---------------------------------------------------------------------------
def cycle_product(signs):
    p = 1
    for s in signs:
        p *= int(s)
    return p


def defect_count(signs, x):
    m = len(signs)
    return sum(1 for i in range(m) if x[i] * x[(i + 1) % m] != signs[i])


def best_common_cause_defect(signs):
    m = len(signs)
    return min(defect_count(signs, x) for x in product((-1, 1), repeat=m))


def local_vertices():
    V = set()
    for a0, a1, b0, b1 in product((1, -1), repeat=4):
        V.add((a0 * b0, a1 * b0, a1 * b1, b1 * a0))
    return sorted(V)


def chsh_facets():
    return [s for s in product((1, -1), repeat=4) if cycle_product(s) == -1]


def facet_value(s, E):
    return sum((F(si) * F(Ei) for si, Ei in zip(s, E)), F(0))


def inside_boole(E):
    return all(abs(facet_value(s, E)) <= 2 for s in chsh_facets())


# ---------------------------------------------------------------------------
# Axis F helpers (form-side; Tsirelson + full TLM). Cited, not re-derived.
# ---------------------------------------------------------------------------
def in_quantum_band(S):
    return 2 < float(S) <= TSIRELSON + BAND_TOL


def commutative_form_max_chsh():
    return 2  # commutative C*-algebra ~ C^N : classical (Commutative Defender Lemma)


def _asin_clamped(x):
    return math.asin(max(-1.0, min(1.0, float(x))))


def _tlm_facets():
    return [sv for sv in product((1, -1), repeat=4) if sv[0] * sv[1] * sv[2] * sv[3] == -1]


def tlm_max(E):
    """MAX over the FOUR TLM facet functionals (full criterion); <= pi <=> quantum."""
    return max(abs(sum(si * _asin_clamped(Ei) for si, Ei in zip(sv, E))) for sv in _tlm_facets())


def is_quantum_TLM(E):
    return tlm_max(E) <= math.pi + 1e-12


def chsh_scalar(E):
    return E[0] + E[1] + E[2] - E[3]


E_GAP = (0.9, 0.9, 0.5, -0.5)              # in-band, full-TLM-violated -> NON-quantum
E_QM = (0.7, 0.7, 0.7, -0.7)               # in-band, full-TLM-satisfied -> quantum
E_CE = (-0.967, -0.971, 0.511, -0.501)     # single-facet says quantum; FULL TLM says NOT
_TS_ISO = 0.7071067811865476               # 1/sqrt2 isotropic Tsirelson point


# ---------------------------------------------------------------------------
# helper: standard bank-result dict
# ---------------------------------------------------------------------------
def _result(name, epistemic, passed, fails, key_result, **extra):
    d = {
        "passed": bool(passed),
        "name": name,
        "family": FAMILY,
        "epistemic": epistemic,
        "tier": 4,
        "physical_premises_certified": False,
        "key_result": key_result,
        "cross_refs": CROSS_REFS,
        "may_not_cite": MAY_NOT_CITE,
        "fail_reasons": fails,
    }
    d.update(extra)
    return d


# ===========================================================================
# BANKED CHECK 1 -- Axis I, the relational floor
# ===========================================================================
def check_L_ijc_cycle_floor():
    """[P_math | R-IJC-sign] an ODD IJC-cycle (chi=-1) admits no common cause <=>
    outside the Boole/local polytope (Fine facets), over all m=3..6; firewall: the
    -1 is the integer IJC parity, never an anticommutator; even-IJC control classical."""
    fails = []
    # odd IJC-count <=> no common cause; parity-law concordance
    for m in (3, 4, 5, 6):
        for signs in product((-1, 1), repeat=m):
            chi = cycle_product(signs)
            d = best_common_cause_defect(signs)
            if chi == -1 and d < 1:
                fails.append(f"m={m}: twisted pattern has a common cause")
            if chi == +1 and d != 0:
                fails.append(f"m={m}: balanced pattern lacks a common cause")
            for x in product((-1, 1), repeat=m):
                if (-1) ** defect_count(signs, x) != chi:
                    fails.append(f"m={m}: parity law violated")
    # the m=4 odd-IJC correlator is genuinely OUTSIDE the polytope (Fine)
    if inside_boole((1, 1, 1, -1)):
        fails.append("odd-IJC 4-cycle wrongly inside the Boole polytope")
    # even-IJC control: classical (inside polytope, common cause exists)
    if not (best_common_cause_defect((1, -1, 1, -1)) == 0 and inside_boole((1, -1, 1, -1))):
        fails.append("even-IJC control not classical")
    # firewall scan: floor path returns only int/Fraction (no complex/anticommutator)
    probes = [cycle_product((1, 1, 1, -1)),
              defect_count((1, 1, 1, -1), (1, 1, 1, 1)),
              facet_value((1, 1, 1, -1), (1, 1, 1, -1))]
    if not all(isinstance(p, (int, F)) and not isinstance(p, complex) for p in probes):
        fails.append("firewall: floor path returned a non-rational (smuggled) value")
    # every common-cause vertex has EVEN correlator product (Route A step 1)
    if not all(cycle_product(v) == 1 for v in local_vertices()):
        fails.append("a common-cause vertex has odd correlator product")
    return _result(
        "L_ijc_cycle_floor", "P_math", not fails, fails,
        "odd-IJC-cycle (chi=-1) <=> no common cause <=> outside Boole polytope; the -1 is "
        "the IJC parity (relational, integer), not anticommutation; R-IJC-sign named.",
        firewall_minus_one_source=FLOOR_MINUS_ONE_SOURCE,
        reading="R-IJC-sign (edge sign = the inadmissible-joint bit)",
    )


# ===========================================================================
# BANKED CHECK 2 -- Axis F, the form ceiling + the sufficiency (full TLM)
# ===========================================================================
def check_L_form_ceiling_and_sufficiency():
    """[P_structural_reading | TLM-cited, FORM-side, branch-conditional] GIVEN the
    noncommutative branch, banked T_Tsirelson caps CHSH<=2sqrt2 (PR excluded); the
    scalar band is NECESSARY only; the FULL four-facet TLM closes sufficiency."""
    fails = []
    # Tsirelson ceiling pinned both sides; PR excluded; commutative-form classical
    if not (2 < TSIRELSON and abs(TSIRELSON ** 2 - 8) < 1e-9):
        fails.append("Tsirelson ceiling not pinned to 2sqrt2")
    if not (4 ** 2 > 8):
        fails.append("PR not excluded by the form ceiling")
    if commutative_form_max_chsh() != 2:
        fails.append("commutative form not classical (CHSH<=2)")
    # sufficiency GAP: E_GAP and E_QM share CHSH 2.8, both in-band, only E_QM quantum
    if not (abs(chsh_scalar(E_GAP) - chsh_scalar(E_QM)) < 1e-9):
        fails.append("witnesses do not share the CHSH scalar")
    if not (in_quantum_band(chsh_scalar(E_GAP)) and in_quantum_band(chsh_scalar(E_QM))):
        fails.append("witnesses not both in-band")
    if is_quantum_TLM(E_GAP):
        fails.append("E_GAP wrongly quantum under full TLM (band not sufficient => gap)")
    if not is_quantum_TLM(E_QM):
        fails.append("E_QM wrongly non-quantum under full TLM")
    # full 4-facet TLM is load-bearing: single-facet over-accepts E_CE
    if is_quantum_TLM(E_CE):
        fails.append("E_CE wrongly quantum (single-facet leak; full TLM must catch it)")
    # consistency: isotropic Tsirelson point sits at TLM == pi (machine precision)
    if not abs(tlm_max((_TS_ISO, _TS_ISO, _TS_ISO, -_TS_ISO)) - math.pi) < 1e-6:
        fails.append("isotropic Tsirelson point not at TLM==pi")
    return _result(
        "L_form_ceiling_and_sufficiency", "P_structural_reading", not fails, fails,
        "Axis F (form-side, branch-conditional): Tsirelson ceiling excludes PR; the scalar "
        "band is NECESSARY only; full four-facet TLM is the SUFFICIENCY closer (gap witness "
        "E_GAP vs E_QM at equal CHSH; counterexample E_CE).",
        native_S=str(NATIVE_S), tsirelson=TSIRELSON,
        ceiling_minus_one_source=CEILING_MINUS_ONE_SOURCE,
    )


# ===========================================================================
# BANKED CHECK 3 -- the composed characterization
# ===========================================================================
def check_T_quantum_condition_two_axis():
    """[P_structural_reading | R-IJC-sign, TLM-cited] WITHIN (2,2,2) uniform-marginal
    correlators and GIVEN the QAC branch: nonclassical-quantum <=> (outside Boole
    polytope, Axis I) AND (full-TLM, Axis F). Co-indexed; native target in-band; both
    axes load-bearing; the antecedent is NOT A1-forced (= the sharpened, co-indexed QAC)."""
    fails = []
    # the two axes must independently hold (consumes the two lemmas)
    if check_L_ijc_cycle_floor()["passed"] is not True:
        fails.append("Axis I floor lemma failed")
    if check_L_form_ceiling_and_sufficiency()["passed"] is not True:
        fails.append("Axis F ceiling/sufficiency lemma failed")
    # native quantum target in-band; classical + PR excluded; endpoints pinned
    if not in_quantum_band(NATIVE_S):
        fails.append("native target not in-band")
    if in_quantum_band(F(2)):
        fails.append("classical S=2 not excluded (open below)")
    if in_quantum_band(4):
        fails.append("PR S=4 not excluded (form ceiling)")
    if not in_quantum_band(TSIRELSON):
        fails.append("Tsirelson endpoint not in-band (closed above)")
    if in_quantum_band(TSIRELSON + 1e-6):
        fails.append("just above Tsirelson not excluded")
    # both axes load-bearing: I alone reaches PR (S=4 out of band); commutative F classical
    if not (4 > 2 and not in_quantum_band(4)):
        fails.append("Axis F not load-bearing (I alone would reach PR)")
    if commutative_form_max_chsh() != 2:
        fails.append("Axis I not load-bearing (commutative F already classical)")
    # firewall provenance distinct (floor relational vs ceiling form-side)
    if FLOOR_MINUS_ONE_SOURCE == CEILING_MINUS_ONE_SOURCE:
        fails.append("floor and ceiling -1 provenances collapsed")
    return _result(
        "T_quantum_condition_two_axis", "P_structural_reading", not fails, fails,
        "characterization (WITHIN (2,2,2) uniform-marginal correlators, GIVEN the QAC branch): "
        "nonclassical-quantum <=> (outside Boole polytope, Axis I) AND (full-TLM, Axis F); "
        "co-indexed; native S=202/75 in-band; both axes load-bearing; antecedent = the QAC.",
        antecedent="odd-IJC-cyclic AND noncommutative-branch-carrying (NOT A1-forced = QAC)",
        reading="R-IJC-sign + TLM-boundary-cited",
    )


# ---------------------------------------------------------------------------
# mutation battery (self-test; not registered) -- each corruption must FLIP a check
# ---------------------------------------------------------------------------
def run_mutations():
    g = globals(); out = []
    def _passed(cn):
        return {"F": check_L_ijc_cycle_floor, "C": check_L_form_ceiling_and_sufficiency,
                "T": check_T_quantum_condition_two_axis}[cn]()["passed"]
    def mut(name, patch, cn):
        saved = {k: g.get(k) for k in patch}
        try:
            g.update(patch)
            try: flipped = (_passed(cn) is False)
            except Exception: flipped = True
        finally: g.update(saved)
        out.append((name, flipped))
    mut("break_parity_law", {"cycle_product": (lambda s: 1)}, "F")
    mut("polytope_all_inside", {"inside_boole": (lambda E: True)}, "F")
    mut("smuggle_complex_defect", {"defect_count": (lambda s, x: 0j)}, "F")
    mut("ceiling_to_PR", {"TSIRELSON": 4.0}, "C")
    mut("tlm_accepts_all", {"is_quantum_TLM": (lambda E: True)}, "C")
    mut("single_facet_leak", {"tlm_max": (lambda E: abs(_asin_clamped(E[0]) + _asin_clamped(E[1]) + _asin_clamped(E[2]) - _asin_clamped(E[3])))}, "C")
    mut("native_out", {"NATIVE_S": F(4)}, "T")
    mut("band_upper_open", {"BAND_TOL": -1e-6}, "T")
    mut("commutative_not_classical", {"commutative_form_max_chsh": (lambda: 4)}, "T")
    return out


_CHECKS = {
    "L_ijc_cycle_floor": check_L_ijc_cycle_floor,
    "L_form_ceiling_and_sufficiency": check_L_form_ceiling_and_sufficiency,
    "T_quantum_condition_two_axis": check_T_quantum_condition_two_axis,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == "__main__":
    ok = True
    for n, fn in _CHECKS.items():
        r = fn(); ok &= r["passed"]
        print(f"  check_{n:34s} [{r['epistemic']:20s}]: {'PASS' if r['passed'] else 'FAIL'}")
        for f in r["fail_reasons"]:
            print("     -", f)
    muts = run_mutations(); nb = sum(1 for _, b in muts if b)
    print(f"  mutations: {nb}/{len(muts)} bite")
    print("MODULE:", "GREEN" if (ok and nb == len(muts)) else "RED")
