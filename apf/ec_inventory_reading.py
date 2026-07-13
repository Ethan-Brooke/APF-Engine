"""The EC inventory reading (kinematic type-inventory completeness).

BANKED v24.3.423 (principal ruling 'bank', 2026-07-13; EXPECTED 3910 ->
3912). Lane record: The Turning (parked)/ec_derivation_2026-07-13/
(charter + walk note + stage-1 hostile audit + fix carriage + results).

Walker of record: ec_walker.py v1.1 (95 exact checks, 0 floats, exit 0;
stage-1 hostile audit LAND-WITH-FIXES 0.86, ALL fixes carried per the
lane's FIX_CARRIAGE record; independent recount audit_recount.py 72/72).
Review context: Paper 2 supplement v4.0 review 4.0.01 items 6/10
(tracker in Papers/Paper 02/Reviews/).

THE .422 LANDING PATTERN (born_at_ties is the structural template of
record): a refuted headline RETAINED AS GROUNDING via a named reading,
with the counter-model owned in-check. Here the refuted headline is the
tex's H4 sentence "EC is derived from PLEC's A1 component alone": it is
DEAD as a derivation claim (heads both MAY-NOT-CITE lists below) and EC
is retained at reading grade -- named, shaped, and sited, not deleted.

TWO CHECKS, tier 4:

  check_L_F6_not_from_EC [P] -- pure computation over the declared scan
    space; no reading consumed. EC-label-injectivity and F6 (Y_Q != 0)
    are logically INDEPENDENT: all four quadrants of the (EC-inj x F6)
    table are inhabited by executed exact witnesses, with INTERSECTING
    cut loci. EC-injectivity removes no template and no class from the
    F6-degenerate sector; the F6-free argmin is the 42-DOF class,
    strictly below the SM at 45. Plus the three-predicate count triple
    8/4 | 10/5 | 4/2 (winner invariant at 45), walker [081-095],
    consumed by the Paper 2 v4.1 fold-in.

  check_L_EC_inventory_reading [P_structural_reading | R-EC-inv +
    I-typing] -- the named reading R-EC-inv (kinematic type-inventory
    completeness, A1-MOTIVATED via the enforcement referent, NOT
    A1-DERIVED; the mass/flavor consistency COUNTER-CONSTRUCTION owned
    in-check at its honest type) + the named input I-typing (entry-typed
    inventory). Under them, the >= 1 abelian factor NECESSITY leg of the
    one-U(1) chain is computed 12/12 + 12/12, and the restriction
    reading of EC is computed to collapse into R-EC-inv + I-typing.

Bank-touch corrigenda landed same version (count-neutral): gauge.py
check_Theorem_R R3 + check_L_gauge_template_uniqueness Step 4 -- the
"A1 requires ... (admissibility completeness)" wording re-typed to the
named-reading form, with this module as the reading's home. The u^c/d^c
conflation arithmetic (4 distinguishable for 5 states; one U(1) resolves
5) SURVIVES unchanged -- it is the necessity leg.
"""

from fractions import Fraction as F
from itertools import product as _product
import math as _math


# --------------------------------------------------------------- rep tables
# Copied from apf/gauge.py check_T_field (the banked Phase-1 pipeline,
# commit e38beeb); A(6) = 7/2 per Paper 2 supp v4.0. These are NAMED SCAN
# INPUTS with the same status they carry in T_field.
_SU3 = {
    '1':  {'dim': 1,  'T': F(0),    'A': F(0)},
    '3':  {'dim': 3,  'T': F(1, 2), 'A': F(1, 2)},
    '3b': {'dim': 3,  'T': F(1, 2), 'A': F(-1, 2)},
    '6':  {'dim': 6,  'T': F(5, 2), 'A': F(7, 2)},
    '6b': {'dim': 6,  'T': F(5, 2), 'A': F(-7, 2)},
    '8':  {'dim': 8,  'T': F(3),    'A': F(0)},
}
_SU2 = {'1': {'dim': 1, 'T': F(0)}, '2': {'dim': 2, 'T': F(1, 2)}}
_NG = 3                      # banked N_gen = 3 (T7 / capacity-beta family)
_CR = ['3', '3b', '6', '6b', '8']
_AF3 = F(11)
_AF2 = F(22, 3)
_C23 = F(2, 3)


def _af(t):
    s3 = sum(_SU3[a]['T'] * _SU2[b]['dim'] for a, b in t) * _NG
    s2 = sum(_SU2[b]['T'] * _SU3[a]['dim'] for a, b in t) * _NG
    return _AF3 - _C23 * s3 > 0 and _AF2 - _C23 * s2 > 0


def _ch(t):
    return (any(_SU3[a]['dim'] > 1 and b == '2' for a, b in t) and
            any(_SU3[a]['dim'] > 1 and b == '1' for a, b in t))


def _s3(t):
    return sum(_SU3[a]['A'] * _SU2[b]['dim'] for a, b in t) == 0


def _wi(t):
    return sum(_SU3[a]['dim'] for a, b in t if b == '2') % 2 == 0


def _an_banked(t):
    """Verbatim logic of check_T_field's _an (the banked F6-at-code predicate)."""
    cd = [f for f in t if _SU3[f[0]]['dim'] > 1 and f[1] == '2']
    cs = [f for f in t if _SU3[f[0]]['dim'] > 1 and f[1] == '1']
    ld = [f for f in t if _SU3[f[0]]['dim'] == 1 and f[1] == '2']
    ls = [f for f in t if _SU3[f[0]]['dim'] == 1 and f[1] == '1']
    if len(cd) != 1 or not ld:
        return False
    Nc = _SU3[cd[0][0]]['dim']
    if not all(_SU3[a]['dim'] == Nc for a, _ in cs):
        return False
    if len(cs) == 2 and len(ls) >= 1:
        d = 4 + 4 * (Nc ** 2 - 1)
        sd = _math.isqrt(d)
        return sd * sd == d
    if len(cs) == 1 and len(ls) >= 1:
        v = F(4 * Nc ** 2, 3 + Nc ** 2)
        p, q = v.numerator, v.denominator
        return _math.isqrt(p * q) ** 2 == p * q
    return False


def _cpt_key(t):
    cj = {'3': '3b', '3b': '3', '6': '6b', '6b': '6', '8': '8', '1': '1'}
    f = tuple(sorted(t))
    r = tuple(sorted((cj.get(a, a), b) for a, b in t))
    return min(f, r)


def _dof(t):
    return sum(_SU3[a]['dim'] * _SU2[b]['dim'] for a, b in t) * _NG


def _cpt_mirror_t(t):
    cj = {'3': '3b', '3b': '3', '6': '6b', '6b': '6', '8': '8', '1': '1'}
    return tuple((cj[a], b) for a, b in t)


def _cpt_mirror_y(y):
    return [-c for c in y]


# --------------------------------------------- exact anomaly-variety machinery
def _linear_rows(t):
    """[SU(3)]^2 U(1), [SU(2)]^2 U(1), [grav]^2 U(1) rows (all-left-handed
    Weyl convention: every entry's Y is its LH Weyl hypercharge)."""
    r3 = [_SU3[a]['T'] * _SU2[b]['dim'] for a, b in t]
    r2 = [_SU2[b]['T'] * _SU3[a]['dim'] for a, b in t]
    rg = [F(_SU3[a]['dim'] * _SU2[b]['dim']) for a, b in t]
    return [r3, r2, rg]


def _cubic_val(t, y):
    return sum(F(_SU3[a]['dim'] * _SU2[b]['dim']) * y[i] ** 3
               for i, (a, b) in enumerate(t))


def _is_solution(t, y):
    """All four anomaly conditions, exact."""
    rows = _linear_rows(t)
    return (all(sum(r[i] * y[i] for i in range(len(t))) == 0 for r in rows)
            and _cubic_val(t, y) == 0)


def _nontrivial(y):
    return any(c != 0 for c in y)


def _nullspace(rows, n):
    M = [r[:] for r in rows]
    piv, rr = [], 0
    for c in range(n):
        prow = None
        for r in range(rr, len(M)):
            if M[r][c] != 0:
                prow = r
                break
        if prow is None:
            continue
        M[rr], M[prow] = M[prow], M[rr]
        pv = M[rr][c]
        M[rr] = [x / pv for x in M[rr]]
        for r in range(len(M)):
            if r != rr and M[r][c] != 0:
                f0 = M[r][c]
                M[r] = [x - f0 * yv for x, yv in zip(M[r], M[rr])]
        piv.append(c)
        rr += 1
        if rr == len(M):
            break
    basis = []
    for fc in [c for c in range(n) if c not in piv]:
        v = [F(0)] * n
        v[fc] = F(1)
        for i, pc in enumerate(piv):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


def _rat_roots(coeffs):
    """All rational roots of a polynomial with Fraction coeffs (highest degree
    first), degree <= 3, leading coeff nonzero. Exact rational root theorem."""
    den = 1
    for c in coeffs:
        den = den * c.denominator // _math.gcd(den, c.denominator)
    ic = [int(c * den) for c in coeffs]
    g = 0
    for c in ic:
        g = _math.gcd(g, abs(c))
    ic = [c // g for c in ic]
    a_n, a_0 = ic[0], ic[-1]
    if a_0 == 0:
        sub = _rat_roots([F(c) for c in ic[:-1]]) if len(ic) > 2 else \
              ([F(-ic[1], ic[0])] if len(ic) == 2 else [])
        return sorted(set([F(0)] + sub))

    def divisors(m):
        m = abs(m)
        ds = []
        i = 1
        while i * i <= m:
            if m % i == 0:
                ds += [i, m // i]
            i += 1
        return sorted(set(ds))

    roots = set()
    for p in divisors(a_0):
        for q in divisors(a_n):
            for s in (1, -1):
                x = F(s * p, q)
                v = F(0)
                for c in ic:
                    v = v * x + c
                if v == 0:
                    roots.add(x)
    return sorted(roots)


def _plane_solutions(t, v, w):
    """Rational projective solutions of the cubic on span{v,w}.
    ('plane', None) if the cubic vanishes identically on the plane,
    else ('points', [primitive integer direction vectors])."""
    n = len(t)
    d = [F(_SU3[a]['dim'] * _SU2[b]['dim']) for a, b in t]
    c30 = sum(d[i] * v[i] ** 3 for i in range(n))
    c21 = 3 * sum(d[i] * v[i] ** 2 * w[i] for i in range(n))
    c12 = 3 * sum(d[i] * v[i] * w[i] ** 2 for i in range(n))
    c03 = sum(d[i] * w[i] ** 3 for i in range(n))
    if c30 == c21 == c12 == c03 == 0:
        return ('plane', None)
    dirs = []
    if c30 == 0:
        dirs.append(v[:])
        qcoef = [c21, c12, c03]
        while qcoef and qcoef[0] == 0:
            qcoef = qcoef[1:]
        if len(qcoef) >= 2:
            for x in _rat_roots(qcoef):
                dirs.append([x * v[i] + w[i] for i in range(n)])
    else:
        for x in _rat_roots([c30, c21, c12, c03]):
            dirs.append([x * v[i] + w[i] for i in range(n)])
    out = []
    for u in dirs:
        den = 1
        for c in u:
            den = den * c.denominator // _math.gcd(den, c.denominator)
        iu = [int(c * den) for c in u]
        g = 0
        for c in iu:
            g = _math.gcd(g, abs(c))
        iu = [c // g for c in iu]
        for c in iu:
            if c != 0:
                if c < 0:
                    iu = [-x for x in iu]
                break
        out.append([F(x) for x in iu])
    return ('points', out)


def _labels(t, y):
    return [(a, b, y[i]) for i, (a, b) in enumerate(t)]


def _injective(labs):
    return len(set(labs)) == len(labs)


def _sterile_entries(labs):
    return [L for L in labs if L[0] == '1' and L[1] == '1' and L[2] == 0]


def _idx_cd(t):
    return next(i for i, (a, b) in enumerate(t)
                if _SU3[a]['dim'] > 1 and b == '2')


# canonical CPT representatives (the '3'-doublet side), walker convention
_T42 = (('3', '2'), ('3b', '1'), ('3b', '1'), ('1', '2'))
_T45 = (('3', '2'), ('3b', '1'), ('3b', '1'), ('1', '2'), ('1', '1'))
_T48 = (('3', '2'), ('3b', '1'), ('3b', '1'), ('1', '2'), ('1', '1'), ('1', '1'))
_T66 = (('3', '2'), ('3b', '1'), ('3b', '1'), ('8', '1'), ('1', '2'))
_T69 = (('3', '2'), ('3b', '1'), ('3b', '1'), ('8', '1'), ('1', '2'), ('1', '1'))
_T72 = (('3', '2'), ('3b', '1'), ('3b', '1'), ('8', '1'), ('1', '2'), ('1', '1'),
        ('1', '1'))
_CANON = [_T42, _T45, _T48, _T66, _T69, _T72]


def _enumerate_scan():
    """The check_T_field Phase-1 enumeration, verbatim loop structure.
    Returns (ordered_count, distinct_set, pre_anomaly_survivors_sorted)."""
    tested = 0
    distinct = set()
    for cd in _CR:
        for nc in range(0, 4):
            for cc in _product(_CR, repeat=nc):
                cs = tuple(sorted(cc))
                for hl in (True, False):
                    for nl in range(0, 3):
                        t = [(cd, '2')] + [(c, '1') for c in cs]
                        if hl:
                            t.append(('1', '2'))
                        t.extend([('1', '1')] * nl)
                        t = tuple(t)
                        tested += 1
                        distinct.add(t)
    pre = sorted([t for t in distinct
                  if _af(t) and _ch(t) and _s3(t) and _wi(t)],
                 key=lambda t: (_dof(t), t))
    return tested, distinct, pre


# exact Y_Q = 0 witnesses with pairwise-distinct complete labels, one per
# canonical template (walker S3(b) WITNESS_Q0; mirrors generated)
_WITNESS_Q0 = {
    _T42: [F(0), F(1), F(-1), F(0)],
    _T45: [F(0), F(1), F(-1), F(0), F(0)],
    _T48: [F(0), F(1), F(-1), F(0), F(2), F(-2)],
    _T66: [F(0), F(1), F(-1), F(0), F(0)],
    _T69: [F(0), F(1), F(-1), F(0), F(0), F(0)],
    _T72: [F(0), F(1), F(-1), F(0), F(0), F(2), F(-2)],
}

# exact FULL-SYSTEM non-degenerate (Y_Q != 0) witnesses (walker S8/T1)
_WITNESS_NONDEG = {
    _T45: [F(1, 6), F(-2, 3), F(1, 3), F(-1, 2), F(1)],   # the SM point
    _T48: [F(1), F(-4), F(2), F(-3), F(6), F(0)],
    _T66: [F(5), F(13), F(-5), F(-3), F(-15)],            # charged octet
    _T69: [F(1), F(-4), F(2), F(0), F(-3), F(6)],
    _T72: [F(1), F(-4), F(2), F(0), F(-3), F(6), F(0)],
}


def check_L_F6_not_from_EC():
    """L_F6_not_from_EC: EC-injectivity and F6 are logically independent [P].

    Tier 4. Pure computation over the declared scan space; no reading
    consumed anywhere in this check.

    STATEMENT. Over the check_T_field Phase-1 scan space (4,680 ordered /
    1,680 distinct templates; declared caps and rep tables as banked),
    with the full anomaly system (three linear conditions + the cubic)
    solved exactly over the rationals:
      (1) the F1-F5 survivor set is 12 templates (6 CPT classes) at DOF
          {42, 45, 48, 66, 69, 72};
      (2) all 12 admit a nontrivial Y_Q = 0 rational solution, and all 12
          of those degenerate classes contain a label-INJECTIVE
          representative -- hence EC-label-injectivity does not imply F6
          (Y_Q != 0) and removes no template and no class from the
          F6-degenerate sector;
      (3) the 42-DOF stripped generation's variety is a single projective
          point (0, t, -t, 0), label-injective and per-field faithful;
          the label-coincident presentation exists only at the trivial
          assignment;
      (4) non-degenerate injectivity-violating solutions exist (T48:
          (1,-1,-1,-3,3,3); T72 analog; 4 templates with mirrors) --
          hence F6 does not imply EC-injectivity;
      (5) ALL FOUR quadrants of the (EC-inj x F6) table are inhabited
          (fourth quadrant: T48 (0,0,0,0,1,-1), Y_Q = 0 with
          u^c = d^c = (3b,1,0)) -- EC-inj and F6 are logically
          independent, with INTERSECTING cut loci;
      (6) the F6-free argmin is the 42-DOF class, strictly below the
          SM at 45.

    THE COUNT TRIPLE (walker [081-095]; consumed by the Paper 2 v4.1
    fold-in of review item 4.0.01.09): three inequivalent F6-flavored
    predicates over the 12 survivors, all computed here --
      spectator-reduction (tex prose): 8 pre-CPT / 4 post-CPT at DOF
        {45,45,48,48,69,69,72,72} (the T66 pair fails: octet-stripping
        forces Y_Q = 0 on the reduced system);
      full-system non-degeneracy: 10 pre-CPT / 5 post-CPT (the T66 pair
        enters via the CHARGED-octet witness (5,13,-5,-3,-15) with
        Y_8 = -(3/5) Y_Q -- forced by the linear system on EVERY T66
        solution; the tex re-implementer sentence 'obtains 4 (and 2)' is
        FALSE for this predicate, audit MAJOR-3);
      code path (_an, uniform-dimension rule): 4 pre-CPT / 2 post-CPT at
        DOF {45,45,48,48}.
    The WINNER (min DOF 45) is identical under all three predicates;
    only intermediate counts differ. No waterfall count changes.

    GUARDS (computed):
      - bank fidelity: the banked Phase-1 pipeline (with the banked _an)
        is reproduced verbatim first -- 4,680 ordered, unique winner =
        SM at 45 Weyl DOF, 2 post-CPT code-path survivors -- before any
        replacement of the anomaly stage;
      - what EC DOES do: EC-injectivity cuts real solutions in BOTH F6
        sectors (the T48/T72 collision witnesses, computed); what it
        does not do is cut any template or class the argmin needs cut;
      - exactness: Fraction arithmetic throughout, no floats; the T42
        classification is certified (k = 1, cubic vanishes identically
        on the null line); the T69 Y_Q = 0 slice is certified by branch
        reduction.

    MAY-NOT-CITE:
      - "EC is derived from A1 alone" (heads the list; refuted -- see
        check_L_EC_inventory_reading);
      - "F6 is a consequence of EC / of admissibility completeness"
        (refuted here);
      - "EC-injectivity removes the 42-DOF near-miss" (refuted);
      - "the 42-DOF rival contains two multiplets with identical
        complete labels" (false on every nontrivial solution);
      - "the Y_Q=0 sector is everywhere EC-clean" (v1.0 phrasing, DEAD)
        or "EC and F6 cut disjoint axes/loci" (DEAD too -- audit
        MAJOR-1; the fourth quadrant is inhabited);
      - "EC does no work in the scan" (false -- EC cuts the T48/T72
        collision solutions in BOTH F6 sectors; what it does not do is
        cut any template or class the argmin needs cut);
      - this check as evidence that F6 is derivable from anything banked
        (it proves independence).

    Deps (consumed live): the declared scan space + rep tables (named
    scan inputs, same status as in T_field), Fraction arithmetic.
    Cross-refs: T_field, T_gauge, the F6 declaration site (Paper 2 supp
    v4.0 sec:seven_filters).

    Provenance: lane The Turning (parked)/ec_derivation_2026-07-13/;
    walker of record ec_walker.py v1.1, 95 exact checks exit 0; stage-1
    hostile audit LAND-WITH-FIXES 0.86, all fixes carried; principal
    ruling 'bank' 2026-07-13; review context: Paper 2 supp v4.0 review
    4.0.01 items 6/10, tracker in Papers/Paper 02/Reviews/.
    """
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)

    # ------------------------------------------------ fidelity + scan space
    tested, distinct, pre = _enumerate_scan()
    ck(tested == 4680, 'scan space: ordered enumeration count = 4680')
    ck(len(distinct) == 1680, 'scan space: distinct unordered templates = 1680')

    # bank fidelity guard: the banked pipeline (banked _an, CPT quotient)
    banked_survivors = []
    seen = set()
    for t in sorted(distinct, key=lambda t: (_dof(t), t)):
        if not (_af(t) and _ch(t) and _s3(t) and _wi(t) and _an_banked(t)):
            continue
        k = _cpt_key(t)
        if k in seen:
            continue
        seen.add(k)
        banked_survivors.append((_dof(t), t))
    ck(len(banked_survivors) == 2 and banked_survivors[0][0] == 45 and
       sorted(banked_survivors[0][1]) == sorted(
           [('3', '2'), ('3b', '1'), ('3b', '1'), ('1', '2'), ('1', '1')]),
       'bank fidelity: banked pipeline reproduced -- unique winner = SM at '
       '45 Weyl DOF, 2 post-CPT code-path survivors')

    # (1) F1-F5 survivor set: 12 templates, 6 CPT classes, the stated DOFs
    ck(len(pre) == 12, 'clause 1: F1-F5 pre-anomaly survivors = 12')
    ck(len({_cpt_key(t) for t in pre}) == 6, 'clause 1: exactly 6 CPT classes')
    ck(sorted(_dof(t) for t in pre) ==
       [42, 42, 45, 45, 48, 48, 66, 66, 69, 69, 72, 72],
       'clause 1: survivor DOF multiset = {42,42,45,45,48,48,66,66,69,69,72,72}')
    ck(all(T in pre for T in _CANON) and
       all(_cpt_mirror_t(T) in pre for T in _CANON) and
       len({t for T in _CANON for t in (T, _cpt_mirror_t(T))}) == 12,
       'clause 1: the 6 canonical templates + CPT mirrors are exactly the '
       '12 F1-F5 survivors')

    # (2) 12/12 Y_Q=0 classes, 12/12 with a label-injective representative
    q0_pairs = []
    for T, y in _WITNESS_Q0.items():
        q0_pairs.append((T, y))
        q0_pairs.append((_cpt_mirror_t(T), _cpt_mirror_y(y)))
    for (tt, yy) in q0_pairs:
        ck(tt in pre and _is_solution(tt, yy) and yy[_idx_cd(tt)] == 0
           and _nontrivial(yy) and _injective(_labels(tt, yy)),
           'clause 2: DOF=%d template has a nontrivial Y_Q=0 rational '
           'solution with pairwise-DISTINCT labels (injectivity computed)'
           % _dof(tt))
    ck(len(q0_pairs) == 12 and len({tt for tt, _ in q0_pairs}) == 12,
       'clause 2: 12/12 survivors have a Y_Q=0 (F6-degenerate) solution '
       'class and 12/12 of those classes contain a label-INJECTIVE '
       'representative -- EC-injectivity removes NO template and NO class '
       'from the F6-degenerate sector')

    # (3) the 42's variety: one projective point (0, t, -t, 0)
    b42 = _nullspace(_linear_rows(_T42), 4)
    ck(len(b42) == 1, 'clause 3: T42 linear anomaly system has k = 1')
    ck(_cubic_val(_T42, b42[0]) == 0,
       'clause 3: cubic vanishes identically on the null line -> variety = '
       'ONE projective point')
    s42 = [F(0), F(1), F(-1), F(0)]
    ck(_is_solution(_T42, s42) and b42[0][1] != 0 and
       all(b42[0][i] * s42[1] == s42[i] * b42[0][1] for i in range(4)),
       'clause 3: the unique solution is (Y_Q, Y_1, Y_2, Y_L) = (0, t, -t, 0)')
    ck(s42[_idx_cd(_T42)] == 0,
       'clause 3: Y_Q = 0 is FORCED (the F6-degenerate class)')
    labs42 = _labels(_T42, s42)
    ck(_injective(labs42) and not _sterile_entries(labs42),
       'clause 3: the 42 at (0,t,-t,0) is label-injective AND per-field '
       'faithful (no sterile (1,1,0) entry)')
    eq_ud = [F(0), F(1), F(-1), F(0)]
    ck(len(_nullspace(_linear_rows(_T42) + [eq_ud], 4)) == 0,
       'clause 3: adding Y_1 = Y_2 to the 42 leaves ONLY the trivial '
       'assignment -- no admissible label-coincident presentation exists')

    # (4) non-degenerate collision witnesses: T48, T72 + mirrors
    w48 = [F(1), F(-1), F(-1), F(-3), F(3), F(3)]
    w72 = [F(1), F(-1), F(-1), F(0), F(-3), F(3), F(3)]
    nondeg_coll = set()
    for (T, y) in [(_T48, w48), (_T72, w72),
                   (_cpt_mirror_t(_T48), _cpt_mirror_y(w48)),
                   (_cpt_mirror_t(_T72), _cpt_mirror_y(w72))]:
        ck(T in pre and _is_solution(T, y) and y[_idx_cd(T)] != 0
           and not _injective(_labels(T, y)),
           'clause 4: DOF=%d template carries a certified Y_Q!=0 '
           'label-COLLIDING solution (collision computed, mirrors included)'
           % _dof(T))
        nondeg_coll.add(T)
    ck(len(nondeg_coll) == 4,
       'clause 4: computed count -- 4 templates (T48, T72 + CPT mirrors) '
       'carry certified non-degenerate collision solutions: F6 does not '
       'imply EC-injectivity')

    # (5) the four-quadrant independence table (fourth quadrant inhabited)
    sm_y = _WITNESS_NONDEG[_T45]
    q4 = [F(0), F(0), F(0), F(0), F(1), F(-1)]
    ck(_is_solution(_T48, q4) and _nontrivial(q4) and q4[_idx_cd(_T48)] == 0
       and not _injective(_labels(_T48, q4)),
       'clause 5: FOURTH QUADRANT witnessed -- T48 (0,0,0,0,1,-1) is a '
       'nontrivial Y_Q=0 solution WITH a label collision u^c = d^c = '
       '(3b,1,0); the Y_Q=0 sector is NOT everywhere EC-clean')
    quadrants = {
        'EC-pass & F6-pass': (_T45, sm_y),
        'EC-pass & F6-fail': (_T42, s42),
        'EC-fail & F6-pass': (_T48, w48),
        'EC-fail & F6-fail': (_T48, q4),
    }
    for qname, (T, y) in quadrants.items():
        ec_pass = _injective(_labels(T, y))
        f6_pass = (y[_idx_cd(T)] != 0)
        ck(_is_solution(T, y) and _nontrivial(y)
           and ec_pass == qname.startswith('EC-pass')
           and f6_pass == ('F6-pass' in qname),
           'clause 5: quadrant [%s] witnessed exactly (DOF=%d)'
           % (qname, _dof(T)))
    ck(_injective(_labels(_T42, s42)) and s42[_idx_cd(_T42)] == 0
       and (not _injective(_labels(_T48, w48))) and w48[_idx_cd(_T48)] != 0,
       'clause 5: both non-implication directions computed in one '
       'predicate -- (EC-pass & F6-fail) at the 42 refutes EC-inj => F6; '
       '(EC-fail & F6-pass) at T48 (1,-1,-1,-3,3,3) refutes F6 => EC-inj; '
       'with the fourth quadrant inhabited the cut loci INTERSECT')

    # (6) F6-free argmin = the 42-DOF class, strictly below the SM at 45
    f6free = sorted(pre, key=_dof)
    ck(_dof(f6free[0]) == 42 and _dof(f6free[1]) == 42
       and _dof(f6free[2]) == 45,
       'clause 6: F6-free survivor DOFs begin 42, 42, 45 -- the stripped '
       'generation sits STRICTLY BELOW the SM at 45')
    ck(_cpt_key(f6free[0]) == _cpt_key(f6free[1])
       and _cpt_key(f6free[0]) != _cpt_key(f6free[2]),
       'clause 6: the two 42s are one CPT class; the SM is not the '
       'F6-free argmin')

    # ------------------------- the three-predicate count triple ([081-095])
    # T1: FULL-SYSTEM non-degeneracy (exact witnesses + the 42 certified out)
    full_nondeg = set()
    for T, y in _WITNESS_NONDEG.items():
        for (tt, yy) in [(T, y), (_cpt_mirror_t(T), _cpt_mirror_y(y))]:
            ck(tt in pre and _is_solution(tt, yy) and yy[_idx_cd(tt)] != 0,
               'triple/T1: DOF=%d template carries an exact FULL-SYSTEM '
               'non-degenerate (Y_Q!=0) rational solution' % _dof(tt))
            full_nondeg.add(tt)
    w66 = _WITNESS_NONDEG[_T66]
    i8 = next(i for i, (a, b) in enumerate(_T66) if a == '8')
    b66 = _nullspace(_linear_rows(_T66), 5)
    kind66, pts66 = _plane_solutions(_T66, b66[0], b66[1])
    ck(len(b66) == 2 and kind66 == 'points' and len(pts66) == 3 and
       all(p[i8] == -F(3, 5) * p[_idx_cd(_T66)] for p in pts66) and
       w66[i8] == -F(3, 5) * w66[_idx_cd(_T66)],
       'triple/T1: the T66 charged-octet witness (5,13,-5,-3,-15) has '
       'Y_8 = -(3/5) Y_Q, forced by the linear system on EVERY T66 '
       'solution (variety = exactly 3 projective points)')
    ck(_T42 not in full_nondeg and _cpt_mirror_t(_T42) not in full_nondeg
       and len(b42) == 1 and s42[_idx_cd(_T42)] == 0,
       'triple/T1: the 42 pair has NO Y_Q!=0 solution (certified: k = 1, '
       'unique projective point has Y_Q = 0)')
    ck(len(full_nondeg) == 10 and len({_cpt_key(t) for t in full_nondeg}) == 5,
       'triple/T1: FULL-SYSTEM non-degeneracy count = 10 pre-CPT / '
       '5 post-CPT (the tex re-implementer sentence "obtains 4 (and 2)" '
       'is FALSE for this predicate)')

    # T2: SPECTATOR-REDUCTION predicate (strip A(R)=0 colored singlets at Y=0)
    def strip_octet(t):
        return tuple(f for f in t if f[0] != '8')

    reduced_ok = set()
    for T, y in _WITNESS_NONDEG.items():
        for (tt, yy) in [(T, y), (_cpt_mirror_t(T), _cpt_mirror_y(y))]:
            if all(a != '8' for a, _ in tt):
                reduced_ok.add(tt)
    spect_pass = {t for t in pre if strip_octet(t) in reduced_ok}
    ck(len(spect_pass) == 8 and len({_cpt_key(t) for t in spect_pass}) == 4
       and sorted(_dof(t) for t in spect_pass) == [45, 45, 48, 48, 69, 69,
                                                   72, 72],
       'triple/T2: SPECTATOR-REDUCTION count = 8 pre-CPT / 4 post-CPT at '
       'DOF {45,45,48,48,69,69,72,72} (the T66 pair fails: octet-stripping '
       'forces Y_Q=0 on the reduced system)')

    # T3: CODE PATH (_an, uniform-dimension rule)
    code_pass = {t for t in pre if _an_banked(t)}
    ck(len(code_pass) == 4 and len({_cpt_key(t) for t in code_pass}) == 2
       and sorted(_dof(t) for t in code_pass) == [45, 45, 48, 48],
       'triple/T3: CODE-PATH (_an) count = 4 pre-CPT / 2 post-CPT at DOF '
       '{45,45,48,48}')

    # winner invariance
    ck(min(_dof(t) for t in full_nondeg) == 45 and
       min(_dof(t) for t in spect_pass) == 45 and
       min(_dof(t) for t in code_pass) == 45,
       'triple: the honest count triple is 8/4 (spectator-reduction), '
       '10/5 (full-system non-degeneracy), 4/2 (code path) -- the WINNER '
       '(min DOF 45) is identical under all three predicates')

    passed = not fails
    return {
        'name': 'L_F6_not_from_EC',
        'epistemic': 'P',
        'passed': passed,
        'tier': 4,
        'key_result': (
            'EC-LABEL-INJECTIVITY AND F6 ARE LOGICALLY INDEPENDENT, computed '
            'exactly over the declared check_T_field Phase-1 scan space '
            '(4,680 ordered / 1,680 distinct; full anomaly system solved '
            'over the rationals): the F1-F5 survivor set is 12 templates / '
            '6 CPT classes at DOF {42,45,48,66,69,72}; 12/12 F6-degenerate '
            '(Y_Q=0) classes contain a label-INJECTIVE representative, so '
            'EC removes no template and no class from the degenerate '
            'sector; the 42-DOF near-miss is a single projective point '
            '(0,t,-t,0), label-injective and per-field faithful; '
            'non-degenerate collision solutions exist (T48 (1,-1,-1,-3,3,3) '
            '+ T72 + mirrors), so F6 does not imply EC-injectivity; ALL '
            'FOUR (EC-inj x F6) quadrants are inhabited (fourth quadrant '
            'T48 (0,0,0,0,1,-1), u^c = d^c = (3b,1,0)) -- the cut loci '
            'INTERSECT and neither contains the other; the F6-free argmin '
            'is the 42 class, strictly below the SM at 45. COUNT TRIPLE '
            '(for review item 4.0.01.09): spectator-reduction 8/4, '
            'full-system non-degeneracy 10/5 (T66 charged octet '
            '(5,13,-5,-3,-15), Y_8 = -(3/5) Y_Q), code path 4/2 -- winner '
            'invariant at 45. F6 stays an independent declared assumption.'
        ),
        'dependencies': [],
        'cross_refs': [
            'T_field (the banked scan whose Phase-1 pipeline is reproduced '
            'verbatim as the fidelity guard)',
            'T_gauge (the template the scan presupposes)',
            'F6 declaration site (Paper 2 supp v4.0 sec:seven_filters)',
            'L_EC_inventory_reading (Leg 2 of the same lane; consumes this '
            'check live)',
        ],
        'artifacts': {
            'named_inputs': ('the declared scan space + rep tables (same '
                             'status as in T_field); N_gen = 3 banked; '
                             'Fraction arithmetic, no floats'),
            'scan': {'ordered': tested, 'distinct': len(distinct),
                     'f1_f5_survivors': len(pre),
                     'cpt_classes': len({_cpt_key(t) for t in pre}),
                     'survivor_dofs': sorted(_dof(t) for t in pre)},
            'four_quadrants': {
                'EC-pass & F6-pass': 'T45 SM point (1/6,-2/3,1/3,-1/2,1)',
                'EC-pass & F6-fail': 'T42 (0,t,-t,0) unique point',
                'EC-fail & F6-pass': 'T48 (1,-1,-1,-3,3,3)',
                'EC-fail & F6-fail': 'T48 (0,0,0,0,1,-1), u^c=d^c=(3b,1,0)',
            },
            'count_triple': {'spectator_reduction': '8 pre-CPT / 4 post-CPT',
                             'full_system_nondegeneracy':
                                 '10 pre-CPT / 5 post-CPT',
                             'code_path_an': '4 pre-CPT / 2 post-CPT',
                             'winner_invariant': 'min DOF 45 under all three'},
            'f6_free_argmin': '42-DOF class (one CPT class) < SM at 45',
            'audit_trail': ('stage-1 hostile audit LAND-WITH-FIXES 0.86, '
                            'all fixes carried (MAJOR-1 fourth quadrant, '
                            'MAJOR-3 count triple); independent recount '
                            '72/72'),
            'lane': 'The Turning (parked)/ec_derivation_2026-07-13/',
            'banking_status': "BANKED v24.3.423 (principal ruling 'bank', "
                              '2026-07-13; 3910 -> 3912)',
        },
        'fail_reasons': fails,
    }


def check_L_EC_inventory_reading():
    """L_EC_inventory_reading: EC as a named reading, not an A1 theorem
    [P_structural_reading | R-EC-inv + I-typing].

    Tier 4. The .422 landing pattern: the refuted headline ("EC is derived
    from A1 alone") RETAINED AS GROUNDING via a named reading; the
    counter-construction owned in-check at its honest type.

    NAMED READING R-EC-inv (kinematic type-inventory completeness): at a
    single interface, kinematic type-distinctness is exhausted by the
    interface's counted labels; label-identical species are copies
    (multiplicity), not types. A1-MOTIVATED via the enforcement referent;
    NOT A1-DERIVED -- the mass/flavor consistency COUNTER-CONSTRUCTION is
    owned in-check at its honest type: a finite structure with two
    interfaces (independent budgets), anchor sets, and a computed
    T_sep-shape additivity biconditional (both truth values exercised),
    on which species -> label is non-injective while every distinction is
    enforced and priced. It instantiates the SHAPES of the banked
    premises at model level and is not advertised as a verified model of
    banked T_sep/L_loc in full generality; the dead-as-derivation verdict
    additionally rests on the premise-side wall (none of A1/MD/T_sep/
    L_loc mentions internal gauge labels; the only bridge is the tex's
    inventory-exhaustiveness step, tex 1893-1920), independently
    re-derived by the stage-1 auditor. The generations counter-model
    (in-world) is handled by the same reading's copy clause, which
    Paper 2 supp v4.0 def:admissible_gauge already names as an underived
    scoping premise.

    NAMED INPUT I-typing (entry-typed inventory): template entries are
    antecedently distinct types (u^c != d^c prior to any abelian label).
    Consumed by the one-U(1) necessity leg through H3 (matter content)
    and Theorem_R R3(b); NOT derivable from R-EC-inv (the recount
    demonstration, computed below: under types-as-label-classes, EC is
    definitionally injective and EC+CM select the U(1)-less 42 -- the
    vocabulary is load-bearing in both directions). Caveat of record
    (audit minor-8): I-typing is in mild tension with
    def:admissible_gauge's copy clause as written -- applied to
    G = SU(3)xSU(2), that clause would make u^c/d^c "one type at
    multiplicity 2"; v4.1 must scope the clause so the two coexist (the
    copy clause reads off the FULL realized G-tilde; I-typing fixes the
    inventory fed to restriction tests).

    STATEMENT (under R-EC-inv + I-typing): every F1-F5 survivor conflates
    entry-types without an abelian grading (12/12) and admits an
    injective labeling with exactly one U(1) (12/12) -- the >= 1 abelian
    factor NECESSITY leg of the one-U(1) chain. The restriction reading
    of EC (injectivity of r_i -> [r_i]_H for proper subgroups H) is
    non-vacuous and is exactly this statement -- its selective content
    collapses into R-EC-inv + I-typing (computed below; walker [075]).
    The CM/sufficiency leg is untouched (A2 + MD via L_eps*, per
    lem:EC_CM_from_A1's CM half, which this lane does not dispute).

    GUARDS (computed / typed):
      - THE COUNTER-CONSTRUCTION'S HONEST TYPE: it is an OWNED
        consistency construction, NOT a verified model of banked
        T_sep/L_loc in full generality (no GNS sectors, no pool
        dynamics); what it computes are the SHAPES -- MD floor, per-
        interface A1 budgets (two interfaces, independent budgets), the
        T_sep additivity biconditional over all pairs with BOTH truth
        values exercised, sector placement -- with species -> label
        non-injective while the s1/s2 distinction stays enforced,
        priced, and inside budget;
      - THE RECOUNT GUARD (branch iii backfires): the recount premise
        fails on the 42 (no admissible label-coincident assignment
        exists -- only the trivial one); under the recount vocabulary at
        0 U(1)s the 42 has 3 types with an injective type -> label map
        and still costs 42 < 45 -- so types-as-label-classes would make
        EC+CM select the U(1)-less rival: I-typing is load-bearing;
      - THE RESTRICTION-READING COLLAPSE: restricting the SM's 5
        entry-types to H = SU(3)xSU(2) yields 4 distinct labels for 5
        entries (u^c/d^c conflate) -- non-vacuous, exactly how
        thm:unique_U1_consolidated Step 2 consumes it; but its selective
        content presupposes the 5 entries are antecedently distinct
        types, i.e. it collapses into R-EC-inv + I-typing, not a
        derivation route;
      - DEAD-PHRASE TRIPWIRES (advisory, the .422 pattern): the phrase
        "derived from A1 alone" (DEAD as derivation) and the v1.0 DEAD
        phrasings "disjoint axes" / "everywhere EC-clean" (both DEAD)
        may appear in module source only in fence/negation contexts.

    MAY-NOT-CITE:
      - "EC is derived from A1 alone" (DEAD as derivation; H4 wording)
        and "from PLEC's A1 component alone" (contradicts
        lem:EC_CM_from_A1(i) and the counter-construction);
      - "EC and CM follow from A1" (pre-v4.0 language, already retired
        paper-side);
      - "the type/copy distinction is derived" (it is the reading's copy
        clause + I-typing);
      - "one-U(1) necessity is unconditional" (it consumes R-EC-inv +
        I-typing);
      - the counter-construction as a verified model of banked
        T_sep/L_loc (it is an owned consistency construction at shape
        level);
      - R-EC-inv against trace-level (post-kinematic) distinctions --
        mass/flavor/generation data are out of the reading's scope by
        construction;
      - either check as a derivation of F6 (F6 stays an independent
        declared assumption; candidate future lane: record-carrier
        route, named in the lane WALK_NOTE section 4).

    Deps: A1 (motivation site only), T_sep, L_loc, FD3 (cited premises
    per lem:EC_CM_from_A1(i)), gauge identification (paper-side
    thm:gauge_ident), L_F6_not_from_EC (consumed live for the scan-space
    facts). Cross-refs / precedents: born_at_ties
    check_L_selection_ledger_completeness (grade pattern of record),
    foundation_inputs check_FD1_structural_completeness (fiat-exclusion
    scoping), closed_world_completeness (sibling completeness grading).

    Provenance: lane The Turning (parked)/ec_derivation_2026-07-13/;
    walker of record ec_walker.py v1.1, 95 exact checks exit 0; stage-1
    hostile audit LAND-WITH-FIXES 0.86, all fixes carried; principal
    ruling 'bank' 2026-07-13; review context: Paper 2 supp v4.0 review
    4.0.01 items 6/10, tracker in Papers/Paper 02/Reviews/.
    """
    import re
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)

    # ------------------------------------------------------------ live deps
    r_leg1 = check_L_F6_not_from_EC()
    ck(r_leg1['passed'] and r_leg1['epistemic'] == 'P',
       'dep: L_F6_not_from_EC [P] consumed live (scan-space facts)')

    from apf.core import check_T_sep, check_L_loc
    r_sep = check_T_sep()
    ck(r_sep.get('passed', False),
       'dep: T_sep live (the additivity-biconditional shape donor)')
    r_loc = check_L_loc()
    ck(r_loc.get('passed', False),
       'dep: L_loc live (the multi-interface independent-budget shape donor)')

    # scan-space facts consumed from Leg 1 + recomputed survivor list
    _, _, pre = _enumerate_scan()
    ck(r_leg1['artifacts']['scan']['f1_f5_survivors'] == 12
       and len(pre) == 12,
       'scan-space facts: 12 F1-F5 survivors (consumed from Leg 1, '
       'recomputed here)')

    # -------------------- the counter-construction (owned, honest type)
    # A finite consistency structure instantiating (a) TWO interfaces with
    # independent budgets (the L_loc SHAPE) and (b) anchor sets per
    # distinction with a cost functional whose additivity biconditional
    # (the T_sep SHAPE: disjoint anchors <=> exactly additive cost) is
    # computed with both truth values exercised. It is an OWNED
    # CONSTRUCTION, not a verified model of the banked statements.
    IF1, IF2 = 'Gamma1', 'Gamma2'
    eps_star = F(1, 10)
    budget = {IF1: F(1), IF2: F(1, 2)}
    internal_label = {'s1': ('3b', '1'), 's2': ('3b', '1'), 's3': ('3', '2')}
    external_datum = {'s1': F(1), 's2': F(2), 's3': F(1)}
    anchor = {
        'd13': (frozenset({'x1'}), IF1, 'internal'),
        'd23': (frozenset({'x2'}), IF1, 'internal'),
        'd12': (frozenset({'y1'}), IF2, 'external'),
        'dxx': (frozenset({'x1'}), IF1, 'internal'),
    }
    wgt = {'x1': F(1, 10), 'x2': F(1, 10), 'y1': F(1, 10)}
    surplus = F(1, 20)

    def kap(names_):
        sets = [anchor[n][0] for n in names_]
        union = frozenset().union(*sets)
        overlap = any(sets[i] & sets[j] for i in range(len(sets))
                      for j in range(i + 1, len(sets)))
        return sum(wgt[e] for e in union) + (surplus if overlap else F(0))

    names = sorted(anchor)
    ck(all(kap([n]) >= eps_star for n in names),
       'counter-construction: MD holds -- every enforced distinction '
       'costs >= eps* = 1/10 > 0 (computed)')
    cost_at = {G: kap([n for n in names if anchor[n][1] == G])
               for G in (IF1, IF2)}
    ck(cost_at[IF1] <= budget[IF1] and cost_at[IF2] <= budget[IF2]
       and budget[IF1] != budget[IF2],
       'counter-construction: A1 holds per interface with TWO interfaces '
       'and independent budgets (the L_loc SHAPE, computed)')
    bic, saw_disjoint, saw_overlap = True, False, False
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            disjoint = not (anchor[a][0] & anchor[b][0])
            additive = (kap([a, b]) == kap([a]) + kap([b]))
            bic = bic and (disjoint == additive)
            saw_disjoint |= disjoint
            saw_overlap |= (not disjoint)
    ck(bic and saw_disjoint and saw_overlap,
       'counter-construction: the T_sep-SHAPE biconditional holds -- '
       'disjoint anchors <=> exactly additive cost, computed over all 6 '
       'pairs with BOTH truth values exercised (the shared-anchor pair is '
       'strictly superadditive)')
    ck(all(anchor[n][2] in ('internal', 'external') for n in names) and
       anchor['d12'][2] == 'external' and anchor['d12'][1] == IF2,
       'counter-construction: every distinction sits in exactly one '
       'sector; the s1/s2 distinctness is carried in the EXTERNAL sector '
       'at the second interface (computed)')
    ck(internal_label['s1'] == internal_label['s2'] and
       external_datum['s1'] != external_datum['s2'] and
       kap(['d12']) >= eps_star,
       'counter-construction: species -> internal-label is NON-INJECTIVE '
       'while the s1/s2 distinction remains enforced, priced (>= eps*), '
       'and inside budget -- R-EC-inv is NOT A1-derived (A1-motivated '
       'only); grade is _reading for this')

    # ----------------------------- the necessity leg (12/12 + 12/12)
    n_conflated = sum(1 for t in pre
                      if len({(a, b) for a, b in t}) < len(t))
    ck(n_conflated == 12,
       'necessity leg: 12/12 survivors have duplicate (SU(3),SU(2)) '
       'labels at zero abelian factors (computed) -- every F1-F5 survivor '
       'conflates entry-types without an abelian grading')
    q0_pairs = []
    for T, y in _WITNESS_Q0.items():
        q0_pairs.append((T, y))
        q0_pairs.append((_cpt_mirror_t(T), _cpt_mirror_y(y)))
    inj_by_template = {tt: (_is_solution(tt, yy) and
                            _injective(_labels(tt, yy)))
                       for tt, yy in q0_pairs}
    ck(set(inj_by_template) == set(pre)
       and all(inj_by_template[tt] for tt in pre),
       'necessity leg: 12/12 survivors admit an injective labeling with '
       'exactly one U(1) (computed from exact anomaly-consistent '
       'witnesses) -- the >= 1 abelian factor NECESSITY leg, GIVEN '
       'R-EC-inv + I-typing')

    # ----------------------------- the recount guard (branch iii backfires)
    eq_ud = [F(0), F(1), F(-1), F(0)]
    ck(len(_nullspace(_linear_rows(_T42) + [eq_ud], 4)) == 0,
       'recount guard: the recount premise fails on the 42 -- NO '
       'admissible assignment with label-identical colored singlets '
       '(only the trivial one)')
    labs42_noU1 = [(a, b) for a, b in _T42]
    ck(len(set(labs42_noU1)) == 3 and len(labs42_noU1) == 4,
       'recount guard: under recount vocabulary at 0 U(1)s the 42 has 3 '
       'TYPES with the type -> label map injective on the 3 types '
       '(computed set arithmetic)')
    ck(_dof(_T42) == 42 and 42 < 45,
       'recount guard: the recounted template still costs 42 Weyl DOF < '
       '45 -- under types-as-label-classes EC+CM would select the '
       'U(1)-less 42; I-typing is load-bearing in BOTH directions')

    # ----------------------------- the restriction-reading collapse ([075])
    sm_y = _WITNESS_NONDEG[_T45]
    entry_labels = _labels(_T45, sm_y)
    ck(len(set(entry_labels)) == 5,
       'self-applied reading exhibit: with types := label-iso classes the '
       'type -> label map on 5 classes is the identity -- injective BY '
       'CONSTRUCTION, no selective content under that reading')
    restr = [(a, b) for (a, b, _) in entry_labels]
    ck(len(restr) == 5 and len(set(restr)) == 4,
       'restriction reading computed: restricting the SM 5 entry-types to '
       'H = SU(3)xSU(2) yields 4 distinct labels for 5 entries (u^c/d^c '
       'conflate) -- non-vacuous, exactly how thm:unique_U1_consolidated '
       'Step 2 consumes it; its selective content presupposes the 5 '
       'entries are antecedently distinct types: the restriction reading '
       'collapses into R-EC-inv + I-typing, not a derivation route')

    # -------------------------- dead-phrase tripwires (advisory, .422 style)
    import inspect
    import sys as _sys
    mod_src = inspect.getsource(_sys.modules[__name__])
    fence_re = re.compile(
        r'NOT|DEAD|refut|MAY-NOT-CITE|heads the list|headline|retired|'
        r'contradicts|tripwire|fence', re.IGNORECASE)
    # ([ ] classes keep the patterns from matching their own source line,
    # the born_at_ties tripwire convention)
    bare_derivation_lines = [
        ln for ln in mod_src.splitlines()
        if re.search(r'derived[ ]from[ ]A1[ ]alone', ln, re.IGNORECASE)
        and not fence_re.search(ln)]
    ck(not bare_derivation_lines,
       'tripwire: "derived from A1 alone" appears only in fence/negation '
       'contexts: %r' % bare_derivation_lines[:3])
    dead_v10_lines = [
        ln for ln in mod_src.splitlines()
        if re.search(r'disjoint[ ]axes|everywhere[ ]EC-clean', ln,
                     re.IGNORECASE)
        and not fence_re.search(ln)]
    ck(not dead_v10_lines,
       'tripwire: the v1.0 "disjoint axes"/"everywhere EC-clean" phrasing '
       'appears only in fence contexts: %r' % dead_v10_lines[:3])

    passed = not fails
    return {
        'name': 'L_EC_inventory_reading',
        'epistemic': 'P_structural_reading',
        'passed': passed,
        'tier': 4,
        'key_result': (
            'THE EC INVENTORY READING, reading-graded: EC (label-'
            'injectivity of the kinematic inventory) holds under R-EC-inv '
            '(kinematic type-inventory completeness: type-distinctness is '
            'exhausted by counted labels, label-identical species are '
            'copies -- A1-motivated via the enforcement referent, NOT '
            'A1-derived: the mass/flavor consistency COUNTER-CONSTRUCTION '
            'is owned in-check at its honest type -- two interfaces with '
            'independent budgets, anchor sets, the T_sep-shape additivity '
            'biconditional computed with both truth values exercised, '
            'species -> label non-injective while every distinction is '
            'priced; shapes of the banked premises at model level, not a '
            'verified model; the premise-side wall independently '
            're-derived by the stage-1 auditor) + I-typing (entry-typed '
            'inventory: u^c != d^c antecedently to any abelian label -- '
            'not derivable from R-EC-inv: the recount demonstration is '
            'computed, types-as-label-classes would select the U(1)-less '
            '42). NECESSITY LEG COMPUTED: 12/12 F1-F5 survivors conflate '
            'entry-types without an abelian grading AND 12/12 admit an '
            'injective labeling with exactly one U(1) -- the >= 1 abelian '
            'factor necessity leg of the one-U(1) chain, conditional on '
            'the reading + input. The restriction reading of EC computed '
            'non-vacuous (SM 5 entries -> 4 labels on H = SU(3)xSU(2)) '
            'and shown to collapse into R-EC-inv + I-typing. The H4 '
            'headline "EC is derived from A1 alone" is REFUTED as '
            'derivation and RETAINED as grounding. CM/sufficiency leg '
            'untouched (A2 + MD via L_eps*). Caveat of record: I-typing '
            'vs def:admissible_gauge copy clause -- v4.1 must scope the '
            'clause (copy clause reads the FULL realized G-tilde; '
            'I-typing fixes the restriction-test inventory).'
        ),
        'dependencies': ['A1', 'T_sep', 'L_loc', 'FD3', 'L_F6_not_from_EC'],
        'cross_refs': [
            'L_selection_ledger_completeness (born_at_ties -- the '
            'refuted-headline-retained-as-grounding grade pattern of '
            'record)',
            'FD1_structural_completeness (foundation_inputs -- '
            'fiat-exclusion scoping precedent)',
            'T_no_phantom_record_quotient (closed_world_completeness -- '
            'sibling completeness grading)',
            'thm:gauge_ident (paper-side gauge identification)',
            'Theorem_R (R3 corrigendum site, this version)',
            'L_gauge_template_uniqueness (Step 4 corrigendum site, this '
            'version)',
        ],
        'artifacts': {
            'reading': {
                'R-EC-inv': 'kinematic type-inventory completeness -- '
                            'A1-motivated via the enforcement referent, '
                            'NOT A1-derived (counter-construction owned '
                            'in-check at shape level)',
            },
            'named_input': {
                'I-typing': 'entry-typed inventory (u^c != d^c '
                            'antecedent to labels); consumed by the '
                            'necessity leg through H3 + Theorem_R R3(b); '
                            'NOT derivable from R-EC-inv (recount '
                            'demonstration computed); caveat of record: '
                            'copy-clause scoping owed to v4.1 (audit '
                            'minor-8)',
            },
            'counter_construction': ('OWNED consistency construction: two '
                                     'interfaces, independent budgets, '
                                     'anchor sets, T_sep-shape additivity '
                                     'biconditional (both truth values), '
                                     'species -> label non-injective, all '
                                     'distinctions priced >= eps*; NOT a '
                                     'verified model of banked T_sep/L_loc'),
            'premise_side_wall': ('none of A1/MD/T_sep/L_loc mentions '
                                  'internal gauge labels; the only bridge '
                                  'is the tex inventory-exhaustiveness '
                                  'step (tex 1893-1920), independently '
                                  're-derived by the stage-1 auditor'),
            'necessity_leg': '12/12 conflate without abelian grading; '
                             '12/12 injective with exactly one U(1)',
            'restriction_reading': 'non-vacuous (5 entries -> 4 labels on '
                                   'H = SU(3)xSU(2)); collapses into '
                                   'R-EC-inv + I-typing (walker [075])',
            'cm_leg': 'untouched: A2 + MD via L_eps* per '
                      'lem:EC_CM_from_A1 CM half',
            'audit_trail': ('stage-1 hostile audit LAND-WITH-FIXES 0.86 '
                            '(MAJOR-2 counter-model strengthened to the '
                            'two-interface biconditional form landed '
                            'here), all fixes carried'),
            'lane': 'The Turning (parked)/ec_derivation_2026-07-13/',
            'banking_status': "BANKED v24.3.423 (principal ruling 'bank', "
                              '2026-07-13; 3910 -> 3912)',
        },
        'fail_reasons': fails,
    }


_CHECKS = {
    'L_F6_not_from_EC': check_L_F6_not_from_EC,
    'L_EC_inventory_reading': check_L_EC_inventory_reading,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    import sys
    ok = True
    for _n, _fn in _CHECKS.items():
        r = _fn()
        print(r['name'], r['epistemic'], 'PASS' if r['passed'] else 'FAIL')
        for f in r['fail_reasons']:
            print('  -', f)
        ok = ok and r['passed']
    sys.exit(0 if ok else 1)
