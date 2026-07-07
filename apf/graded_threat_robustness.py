"""Graded-threat robustness of the IJC dichotomy.

The IJC Dichotomy Theorem (check_T_IJC_dichotomy) classifies a jointly-
meaningful pair {d1, d2} at an interface into exactly two branches by the
CRISP threat sets T(d) (frozensets of perturbation IDs):

    (Sep)  T(d1,d2) = T(d1) U T(d2)                -- no joint surplus
    (IJC)  T(d1,d2) STRICTLY-SUPERSETS T(d1) U T(d2) -- an irreducible surplus

Its exhaustion is logic on the FD5 set-inclusion vocabulary: joint-
meaningfulness (FD5) forces T(d1,d2) to contain T(d1) U T(d2); a superset is
either equal (Sep) or strict (IJC), and the proper-subset "third branch" is
barred. The reading-exhaustiveness walk (2026-07-03, v24.3.369) left exactly
one named-open residual on this front: VOCABULARY ROBUSTNESS -- does the
dichotomy survive if threats are GRADED (a perturbation threatens a distinction
to a DEGREE in [0,1]) rather than crisp? "Any graded threat structure
satisfying the FD analogs collapses to the crisp classifier -- or name
precisely where it doesn't."

This module closes that residual.

GRADED STRUCTURE. Each distinction d carries a membership mu_d : P -> [0,1]
over the perturbation universe P; the pair carries mu_12 : P -> [0,1].
Crisp is the special case mu in {0,1}. Define the theta-cut
    T_d^theta = { p : mu_d(p) >= theta }.

GRADED-FD5 (monotone dominance). The graded reading of joint-meaningfulness:
    mu_12(p) >= max(mu_d1(p), mu_d2(p))   for all p.
This is FORCED by the same clause that forces the crisp superset relation --
the joint distinction {d1,d2} contains d1 as a sub-distinction, so any
perturbation endangers the joint at least as much as it endangers either
member. (Fence: this presumes a COMMENSURABLE grade scale across the
individual and joint threat functions -- one shared meaning of "degree of
threat". Commensurability is a well-typing precondition, not a reading choice
among alternatives; without it the >= is not well-formed and one has left the
FD vocabulary entirely.)

THE COLLAPSE (the robustness lemma, [P_structural]). Define the excess
    Delta(p) = mu_12(p) - max(mu_d1(p), mu_d2(p)).
Under graded-FD5 (Delta >= 0 pointwise):

  (C1) monotone dominance  <=>  crisp containment T_12^theta ⊇ T_1^theta ∪ T_2^theta
       at EVERY threshold theta. A graded structure is exactly a nested stack
       of crisp dichotomy instances, one per level set.
  (C2) the classification is a clean two-way split with NO third branch:
       Sep-graded <=> Delta ≡ 0 ; IJC-graded <=> Delta ≢ 0 (a function is
       either identically zero or not). No cut ever violates containment.
  (C3) Sep-graded <=> every cut is crisp-Sep (T_12^theta = T_1^theta ∪ T_2^theta);
       IJC-graded <=> some cut is crisp-IJC. The graded verdict is determined by
       and consistent with the crisp verdict at each threshold.
  (C4) BOUNDARY ("where it doesn't collapse"): the ONLY way grading opens a
       third branch is to DROP graded-FD5. Sub-dominance (mu_12(p) < max at some
       p) is equivalent to a cut violation at theta = max(mu_d1,mu_d2)(p) --
       the graded analog of the crisp forbidden proper-subset branch. Since
       graded-FD5 is forced by joint-meaningfulness, the third branch is
       excluded exactly as in the crisp case.
  (C5) t-CONORM ROBUSTNESS: the forcing needs no fuzzy-union choice --
       mu_12 >= max <=> (mu_12 >= mu_d1 AND mu_12 >= mu_d2). max is the LEAST
       t-conorm, so any stricter union (probabilistic sum, bounded sum, ...)
       only shrinks Sep and grows IJC; it never opens a third branch. The
       dichotomy is conorm-independent.

CONCLUSION. Grading adds no branch: every graded threat structure satisfying
graded-FD5 reduces to a threshold-stack of crisp Sep/IJC classifiers and
carries the identical two-way verdict. The dichotomy is robust; the residual
is retired. Its one fence is commensurable grading (a well-typing precondition),
not a reading among alternatives -- hence [P_structural], not
[P_structural_reading].

The witness below certifies (C1)-(C5) by EXACT rational enumeration over a
fixed finite grid (P = 3 points, memberships in {0, 1/2, 1}) -- an exhaustive
27^3 sweep, no floats, plus explicit named Sep/IJC witnesses.

Grade [P_structural]. Dependencies: A1, T_IJC_dichotomy,
T_no_IJC_no_noncommutativity. Reference:
The Turning/graded_threat_robustness_2026-07-06/ (note + walk script).
"""

from fractions import Fraction as F
from itertools import product

from apf.apf_utils import check, _result


# grid: three perturbations, three grades -- exact rationals
_P = (0, 1, 2)
_VALS = (F(0), F(1, 2), F(1))


def _as_mu(triple):
    return {p: v for p, v in zip(_P, triple)}


def _maxf(mu1, mu2):
    return {p: max(mu1[p], mu2[p]) for p in _P}


def _excess(mu1, mu2, mu12):
    m = _maxf(mu1, mu2)
    return {p: mu12[p] - m[p] for p in _P}


def _thetas(mu1, mu2, mu12):
    # candidate thresholds where a cut can change = the positive used values
    vals = set()
    for mu in (mu1, mu2, mu12):
        vals.update(v for v in mu.values() if v > 0)
    return sorted(vals)


def _cut(mu, theta):
    return frozenset(p for p in _P if mu[p] >= theta)


def _dominates(mu1, mu2, mu12):
    m = _maxf(mu1, mu2)
    return all(mu12[p] >= m[p] for p in _P)


def _all_cuts_contain(mu1, mu2, mu12):
    return all(_cut(mu12, th) >= (_cut(mu1, th) | _cut(mu2, th))
               for th in _thetas(mu1, mu2, mu12))


def _all_cuts_sep(mu1, mu2, mu12):
    return all(_cut(mu12, th) == (_cut(mu1, th) | _cut(mu2, th))
               for th in _thetas(mu1, mu2, mu12))


def check_L_graded_threat_collapses_to_crisp():
    """L_graded_threat_collapses_to_crisp: the IJC dichotomy is robust under
    graded (fuzzy/probabilistic) threat structures [P_structural].

    STATEMENT. Let each distinction carry a graded threat membership
    mu_d : P -> [0,1], the pair carry mu_12, and let graded-FD5 (monotone
    dominance) hold: mu_12 >= max(mu_d1, mu_d2) pointwise -- the forced graded
    reading of joint-meaningfulness. Then the graded structure is exactly a
    threshold-stack of crisp IJC-dichotomy instances (containment holds at every
    theta-cut), and the two-branch verdict on the excess Delta = mu_12 - max is
    the identical Sep/IJC classification: Sep <=> Delta ≡ 0, IJC <=> Delta ≢ 0.
    No third branch exists. Grading opens a third branch ONLY by violating
    graded-FD5 (sub-dominance <=> a cut violation), which joint-meaningfulness
    forbids. The forcing is t-conorm-independent (max is the least t-conorm).

    Therefore the vocabulary-robustness residual named-open by the reading-
    exhaustiveness walk (v24.3.369) is CLOSED: grading collapses to the crisp
    classifier; the only fence is commensurable grading (a well-typing
    precondition, not a reading alternative).

    WITNESS: exact-rational exhaustive enumeration over P = 3 points with
    memberships in {0, 1/2, 1} (27^3 triples), plus explicit Sep/IJC witnesses.
    Certifies (C1) dominance <=> containment-at-every-cut; (C2) no third branch
    under graded-FD5; (C3) Sep <=> every cut crisp-Sep; (C4) boundary: sub-
    dominance <=> cut violation; (C5) t-conorm robustness.

    GRADE [P_structural]. Structural collapse proved from FD5/joint-
    meaningfulness (via T_IJC_dichotomy); unconditional given commensurable
    grading. Dependencies: A1, T_IJC_dichotomy, T_no_IJC_no_noncommutativity.
    """
    # --- explicit named witnesses (branch well-formedness) ------------------
    # graded Sep: mu_12 = max exactly -> Delta ≡ 0
    s1 = _as_mu((F(1), F(0), F(0)))
    s2 = _as_mu((F(0), F(1, 2), F(0)))
    s12 = _maxf(s1, s2)
    dsep = _excess(s1, s2, s12)
    check(all(dsep[p] == 0 for p in _P),
          "Sep witness: Delta ≡ 0 (mu_12 = max)")
    check(_dominates(s1, s2, s12) and _all_cuts_contain(s1, s2, s12),
          "Sep witness: graded-FD5 holds and every cut contains the union")
    check(_all_cuts_sep(s1, s2, s12),
          "Sep witness: every theta-cut is crisp-Sep")

    # graded IJC: excess on p=2 -> Delta ≢ 0
    i1 = _as_mu((F(1), F(0), F(1, 2)))
    i2 = _as_mu((F(0), F(3, 4), F(1, 3)))
    i12 = _as_mu((F(1), F(3, 4), F(1)))   # excess 1 - 1/2 = 1/2 at p=2
    dijc = _excess(i1, i2, i12)
    check(dijc[2] == F(1, 2) and any(dijc[p] != 0 for p in _P),
          "IJC witness: Delta ≢ 0 (surplus 1/2 at p=2)")
    check(_dominates(i1, i2, i12),
          "IJC witness: graded-FD5 holds")
    # some cut is crisp-IJC (strict containment): at theta=1, T12={0,2} ⊋ {0}
    check(any(_cut(i12, th) > (_cut(i1, th) | _cut(i2, th))
              for th in _thetas(i1, i2, i12)),
          "IJC witness: some theta-cut is crisp-IJC (strict)")

    # --- exhaustive exact enumeration over the grid -------------------------
    triples = [_as_mu(t) for t in product(_VALS, repeat=len(_P))]
    n_funcs = len(triples)
    check(n_funcs == 27, f"grid: {n_funcs} graded functions on 3 points x 3 grades")

    total = c1 = c3 = c4 = c5 = 0
    dom_cases = 0
    third_branch_under_fd5 = 0          # must stay 0 (C2)
    subdom_without_violation = 0        # must stay 0 (C4)
    for mu1 in triples:
        for mu2 in triples:
            mmax = _maxf(mu1, mu2)
            for mu12 in triples:
                total += 1
                dom = _dominates(mu1, mu2, mu12)
                cont = _all_cuts_contain(mu1, mu2, mu12)
                # (C1) dominance <=> containment at every cut
                if dom == cont:
                    c1 += 1
                # (C5) dominance <=> (>=mu1 and >=mu2)
                both = all(mu12[p] >= mu1[p] and mu12[p] >= mu2[p] for p in _P)
                if dom == both:
                    c5 += 1
                if dom:
                    dom_cases += 1
                    delta = {p: mu12[p] - mmax[p] for p in _P}
                    is_sep = all(delta[p] == 0 for p in _P)
                    # (C2) under graded-FD5, never a cut violation (no 3rd branch)
                    if not cont:
                        third_branch_under_fd5 += 1
                    # (C3) Sep <=> every cut crisp-Sep
                    if is_sep == _all_cuts_sep(mu1, mu2, mu12):
                        c3 += 1
                else:
                    # (C4) sub-dominance must produce a cut violation
                    if cont:
                        subdom_without_violation += 1

    check(c1 == total,
          f"(C1) dominance <=> containment-at-every-cut: {c1}/{total}")
    check(c5 == total,
          f"(C5) dominance <=> (>=mu1 AND >=mu2) [t-conorm-free forcing]: {c5}/{total}")
    check(third_branch_under_fd5 == 0,
          f"(C2) no third branch under graded-FD5: {third_branch_under_fd5} violations")
    check(c3 == dom_cases,
          f"(C3) Sep <=> every-cut-crisp-Sep: {c3}/{dom_cases}")
    check(subdom_without_violation == 0,
          f"(C4) boundary: sub-dominance <=> cut violation "
          f"({subdom_without_violation} sub-dominant cases with no violation)")

    # (C5) tail: max is the LEAST t-conorm -> forcing is conorm-independent
    def _probsum(a, b):
        return a + b - a * b

    def _boundsum(a, b):
        return min(F(1), a + b)

    conorm_ge_max = all(
        _probsum(a, b) >= max(a, b) and _boundsum(a, b) >= max(a, b)
        for a in _VALS for b in _VALS)
    check(conorm_ge_max,
          "(C5) max is the least t-conorm (probsum, boundsum both >= max): "
          "any stricter fuzzy union shrinks Sep, never opens a third branch")

    return _result(
        name='L_graded_threat_collapses_to_crisp',
        tier=4,
        epistemic='P_structural',
        summary=(
            'Vocabulary-robustness residual of the IJC dichotomy CLOSED. Under '
            'graded (fuzzy/probabilistic) threat memberships mu_d : P -> [0,1] '
            'with graded-FD5 monotone dominance mu_12 >= max(mu_d1, mu_d2) -- the '
            'forced graded reading of joint-meaningfulness -- the graded '
            'structure is exactly a threshold-stack of crisp IJC-dichotomy '
            'instances (containment at every theta-cut) and carries the identical '
            'two-way verdict on the excess Delta = mu_12 - max: Sep <=> Delta ≡ 0, '
            'IJC <=> Delta ≢ 0. No third branch: grading opens one ONLY by '
            'violating graded-FD5 (sub-dominance <=> cut violation), which joint-'
            'meaningfulness forbids. Forcing is t-conorm-independent (max is the '
            'least t-conorm). Certified by exact-rational exhaustive enumeration '
            '(27^3 grid) + explicit Sep/IJC witnesses. Grading collapses to the '
            'crisp classifier; only fence is commensurable grading (a well-typing '
            'precondition, not a reading alternative) -- hence [P_structural].'
        ),
        key_result=(
            'graded threat structure + graded-FD5 => threshold-stack of crisp '
            'Sep/IJC; Sep<=>Delta≡0, IJC<=>Delta≢0; third branch <=> FD5 '
            'violation (excluded); conorm-independent [P_structural]'
        ),
        dependencies=['A1', 'T_IJC_dichotomy', 'T_no_IJC_no_noncommutativity'],
        cross_refs=['T_IJC_dichotomy', 'T_no_IJC_no_noncommutativity'],
        artifacts={
            'grid': 'P=3 points, grades {0,1/2,1}, 27^3 = 19683 triples (exact)',
            'C1_dominance_iff_containment': 'PASS (19683/19683)',
            'C2_no_third_branch_under_FD5': 'PASS (0 violations)',
            'C3_sep_iff_every_cut_crisp_sep': 'PASS',
            'C4_boundary_subdominance_iff_cut_violation': 'PASS',
            'C5_tconorm_independent_max_is_least': 'PASS',
            'sep_witness': 'mu_12 = max -> Delta ≡ 0',
            'ijc_witness': 'surplus 1/2 at p=2 -> Delta ≢ 0',
            'graded_FD5': 'mu_12 >= max(mu_d1,mu_d2), forced by joint-meaningfulness',
            'fence': 'commensurable grade scale (well-typing precondition)',
            'residual_closed': ('reading-exhaustiveness walk v24.3.369, front 3 '
                                'vocabulary-robustness named-open'),
            'note_home': 'The Turning/graded_threat_robustness_2026-07-06/',
        },
    )


_CHECKS = {
    'L_graded_threat_collapses_to_crisp': check_L_graded_threat_collapses_to_crisp,
}


def register(registry):
    """Register the graded-threat robustness lemma into the bank."""
    registry.update(_CHECKS)
