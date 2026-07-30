"""Where the dephasing law and the Born law separate: exactly the coherence sector.

WHAT THIS ADDS, AGAINST THE PRIOR ART (read this first).

apf/gauge_without_sandwich_countermodel.py (v24.3.446) exhibits dephasing
X -> diag(X) as a second countermodel family: positive, trace preserving,
affine, completely positive, and non-Born on a superposition load.  It records
that no fence banked there touches it.  What it does not compute is WHERE the
two laws differ, and that turns out to be exact and small.

apf/commutative_no_unresolved_hold.py (v24.3.412) banks the other half from the
other side: in a commutative admissibility algebra every state is
indistinguishable from its conditional expectation D(rho) = sum_pi Q_pi rho Q_pi,
and any observable that separates rho from D(rho) fails to commute with a
generator -- it is a coherence witness, which in branch Sep is absent.

This module joins them with one identity.  On the standard MASA the dephasing
map IS that conditional expectation, and

    Born(h, e) - Dephasing(h, e) = Tr(offdiag(h) . offdiag(e)) / Tr(h)

exactly.  So the two laws agree on every effect the diagonal algebra contains,
and every separating effect is a .412 coherence witness.

WHAT THE IDENTITY IS, BILLED HONESTLY (corrigendum after blinded audit).  It is
an ALGEBRAIC IDENTITY OF diag AND offdiag, not a discovery about these two maps.
Tr(diag(h)) = Tr(h), so the difference is Tr(offdiag(h) e)/Tr(h); and offdiag has
zero diagonal, so that trace reads only the off-diagonal part of e.  It therefore
holds for ARBITRARY square matrices with Tr(h) != 0 -- no Hermiticity, no
positivity, no normalization, any n -- and the general form is executed below.
The earlier framing called it a located boundary and defended it with a
"two-route" leg that could not fail; both are withdrawn.  What the module
contributes is the exact sector of disagreement plus the three corollaries, not
a fact that could have come out otherwise.

AND THE COHERENCE CONDITION IS NECESSARY, NOT SUFFICIENT.  "They separate when
the load carries coherence and the effect reads it" is FALSE as a sufficient
condition, and the witness is computed below: the load (I + sigma_y)/2 is pure
with maximal coherence and the effect (I + sigma_x)/2 reads an off-diagonal
sector, yet Born and dephasing AGREE at 1/2.  The true condition is a
non-vanishing Hilbert-Schmidt pairing of the two coherence sectors, which is
what the identity says and what the earlier prose overstated.

GRADE [P_math].  Exact rational linear algebra; no physical premise consumed.
NON-EXPORTING, physical_premises_certified = False.

WHAT THIS DOES NOT DO.
  - It does not refute dephasing.  It locates the disagreement.
  - It does not say a world confined to the diagonal algebra IS Born.  That
    step needs the admissible effect algebra tied to the gauge group, which is
    not established anywhere and is barred below.
  - It does not work off the real symmetric slice except at the one complex
    witness below.  The battery is real; the prose reads Herm(n); the gap is
    named rather than papered over.
  - It does not identify the two maps in general.  The .412 witness uses a
    deliberately NON-diagonal projector spec; the maps are unitarily conjugate,
    not equal, and the conjugating unitary is the preferred basis.  The MASA
    instance is what is computed here and the non-MASA control is executed.

MAY NOT CITE ON THE STRENGTH OF THIS MODULE.
  - "Born is derived."  Standing corpus bar.
  - "The dephasing world is Born."  Not licensed; see above.
  - "Dephasing is the same map as the one commutative_no_unresolved_hold banks."
    Unitarily conjugate, not equal.
  - "Dephasing is refuted."  It is located, not refuted.
  - "The identity is a fact about these maps."  It is an algebraic identity of
    diag and offdiag, true of arbitrary matrices.
  - "Coherence in the load and an off-diagonal effect are SUFFICIENT for
    separation."  FALSE; the sigma_y / sigma_x witness is computed.
  - "The counts 19 and 7-of-14 are results."  They are battery sizes, kept as
    regression pins.
"""

from fractions import Fraction as F
from typing import Dict, List, Tuple

Mat = List[List[F]]


# --------------------------------------------------------------------------
# exact real linear algebra
# --------------------------------------------------------------------------
def _zeros(n: int) -> Mat:
    return [[F(0)] * n for _ in range(n)]


def _mm(A: Mat, B: Mat) -> Mat:
    n, k, m = len(A), len(B), len(B[0])
    return [[sum((A[i][p] * B[p][j] for p in range(k)), F(0)) for j in range(m)]
            for i in range(n)]


def _tr(A: Mat) -> F:
    return sum((A[i][i] for i in range(len(A))), F(0))


def _diag_part(M: Mat, n: int) -> Mat:
    """The map under test: X -> diag(X)."""
    return [[M[i][j] if i == j else F(0) for j in range(n)] for i in range(n)]


def _offdiag(M: Mat, n: int) -> Mat:
    return [[F(0) if i == j else M[i][j] for j in range(n)] for i in range(n)]


def _sigma_lambda(lam: F, h: Mat, n: int) -> Mat:
    """The .445/.446 depolarizing family, used as the DISCRIMINATING control."""
    return [[lam * h[i][j] + ((1 - lam) / n if i == j else F(0))
             for j in range(n)] for i in range(n)]


def _score(state: Mat, e: Mat):
    d = _tr(state)
    if d == 0:
        return None
    return _tr(_mm(state, e)) / d


def _born(h: Mat, e: Mat):
    return _score(h, e)


# --------------------------------------------------------------------------
# fixtures: loads, and GENUINE effects (0 <= E <= I)
# --------------------------------------------------------------------------
def _loads(n: int) -> List[Mat]:
    if n == 2:
        return [
            [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]],        # |+><+|
            [[F(1), F(0)], [F(0), F(0)]],                     # |0><0|
            [[F(1, 2), F(0)], [F(0), F(1, 2)]],               # I/2
            [[F(3, 5), F(1, 5)], [F(1, 5), F(2, 5)]],
            [[F(1, 4), F(-1, 4)], [F(-1, 4), F(3, 4)]],
        ]
    return [
        [[F(1, 3)] * 3 for _ in range(3)],
        [[F(1), F(0), F(0)], [F(0), F(0), F(0)], [F(0), F(0), F(0)]],
        [[F(1, 2), F(0), F(1, 4)], [F(0), F(1, 4), F(0)],
         [F(1, 4), F(0), F(1, 4)]],
    ]


def _effects(n: int) -> List[Tuple[str, Mat]]:
    """Diagonal projectors, and (I + S)/2 for each off-diagonal symmetry.

    The off-diagonal family is (I + S)/2 rather than S: S has spectrum {+1,-1}
    and is not a POVM element, so a separation exhibited on S would not be a
    separation on anything a world can measure.  Affinity carries the identity
    across unchanged, and the effect property is asserted below.
    """
    out: List[Tuple[str, Mat]] = []
    for i in range(n):
        E = _zeros(n)
        E[i][i] = F(1)
        out.append(("diag", E))
    for i in range(n):
        for j in range(i + 1, n):
            E = [[F(1, 2) if a == b else F(0) for b in range(n)] for a in range(n)]
            E[i][j] = E[j][i] = F(1, 2)
            out.append(("offdiag", E))
    return out


def _det(M: Mat) -> F:
    m = [r[:] for r in M]
    n = len(m)
    det = F(1)
    for c in range(n):
        piv = None
        for r in range(c, n):
            if m[r][c] != 0:
                piv = r
                break
        if piv is None:
            return F(0)
        if piv != c:
            m[c], m[piv] = m[piv], m[c]
            det = -det
        det *= m[c][c]
        inv = F(1) / m[c][c]
        for r in range(c + 1, n):
            if m[r][c] != 0:
                f = m[r][c] * inv
                m[r] = [a - f * bb for a, bb in zip(m[r], m[c])]
    return det


def _psd_full(M: Mat, n: int) -> bool:
    """EVERY principal minor >= 0.  The 2x2-minor test this replaced was UNSOUND
    at n >= 3: E with 1/2 on the diagonal and -3/10 off-diagonal passes it while
    having eigenvalue -1/10."""
    from itertools import combinations
    for size in range(1, n + 1):
        for idx in combinations(range(n), size):
            if _det([[M[a][b] for b in idx] for a in idx]) < 0:
                return False
    return True


def _is_effect(E: Mat, n: int) -> bool:
    """0 <= E <= I, tested on EVERY principal minor of E and of I - E."""
    C = [[(F(1) if a == b else F(0)) - E[a][b] for b in range(n)] for a in range(n)]
    return _psd_full(E, n) and _psd_full(C, n)


def _is_state(h: Mat, n: int) -> bool:
    """Hermitian (real symmetric on this slice), PSD, unit trace.  The argument
    that a separation on a non-POVM EFFECT is unreadable applies verbatim to the
    LOAD, and nothing asserted it before."""
    if any(h[i][j] != h[j][i] for i in range(n) for j in range(n)):
        return False
    return _psd_full(h, n) and _tr(h) == F(1)


def _rank1_diag_projectors(n: int) -> List[Mat]:
    out = []
    for i in range(n):
        Q = _zeros(n)
        Q[i][i] = F(1)
        out.append(Q)
    return out


def _conditional_expectation(rho: Mat, projectors: List[Mat], n: int) -> Mat:
    """The .412 route, re-implemented from its docstring: sum_pi Q_pi rho Q_pi."""
    acc = _zeros(n)
    for Q in projectors:
        T = _mm(_mm(Q, rho), Q)
        acc = [[acc[i][j] + T[i][j] for j in range(n)] for i in range(n)]
    return acc


def _commutes(A: Mat, B: Mat) -> bool:
    return _mm(A, B) == _mm(B, A)


def _result(name, epistemic, key, ev, fails, tier, deps, prem, ncs, xrefs,
            fail_count=None):
    """Build the result dict, and CROSS-ASSERT the two failure records HERE.

    THE PATTERN IS v24.3.450's, AND THE REASON IT IS AT THIS SITE MATTERS.  An
    execution audit on 2026-07-28 showed that a cross-assert living only in a
    module's run_all() does not travel on the banked path: bank.py invokes each
    registered check_fn() directly and reads r['passed'], and never calls
    run_all() or reads fail_count.  A mutation forcing 'passed' True was
    demonstrated to report PASS to the bank with the failures still recorded.
    The assert therefore lives at the point the dict is BUILT, so it travels
    with the dict wherever the dict goes; run_all() remains a second gate.

    RESIDUAL LIMIT, DISCLOSED RATHER THAN OVERCLAIMED, AND NARROWER THAN THE
    PATTERN'S USUAL BILLING: the two records are incremented on two ADJACENT
    lines inside ck(), so they are not independent in the way the phrase "two
    failure records" suggests, and the guard bites only against an edit made
    INSIDE ck() -- verified: dropping the increment while a real defect is
    present does raise.  What it does not reach is a bare literal substitution
    of the verdict.  It does NOT catch a bare literal substitution of the
    verdict itself, because nothing downstream re-derives that field: bank.py
    reads it.  No code inside a module can defend against an arbitrary edit to
    its own return statement; that is a property of the bank's contract, not of
    this module."""
    counted = len(fails) if fail_count is None else fail_count
    if len(fails) != counted:
        raise AssertionError(
            f"{name}: failure records disagree -- fail_reasons has "
            f"{len(fails)} entries, the independent counter says {counted}")
    return {
        'fail_count': counted,
        'name': name,
        'epistemic': epistemic,
        'passed': (counted == 0),
        'tier': tier,
        'fail_reasons': fails,
        'dependencies': list(deps),
        'premises': list(prem),
        'negative_controls': list(ncs),
        'cross_refs': list(xrefs),
        'physical_premises_certified': False,
        'exports': [],
        'bank_modified': False,
        'key_result': key,
        'evidence': ev,
    }


# ==========================================================================
def check_L_coherence_sector_separation() -> Dict[str, object]:
    """Tier 3, [P_math]."""
    fails: List[str] = []

    tally = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
            tally[0] += 1

    # ---- L0: the effects must be effects, or no separation is measurable.
    ck(all(_is_effect(E, n) for n in (2, 3) for _, E in _effects(n)),
       "every tested effect must satisfy 0 <= E <= I on every principal minor")
    # THE UPPER HALF OF THE PREDICATE NEEDS ITS OWN WITNESS.  Found by mutation:
    # both negative witnesses below are killed by 0 <= E, so dropping the
    # I - E >= 0 test entirely left the module passing -- and an effect battery
    # built from I + S rather than (I + S)/2 then sailed through, though I + S
    # has eigenvalue 2 and is not an effect at all.  This is that witness.
    _S = [[F(0), F(1)], [F(1), F(0)]]
    _IplusS = [[F(1), F(1)], [F(1), F(1)]]
    ck(_psd_full(_IplusS, 2),
       "the upper-half witness must be PSD, or it tests the lower half instead")
    ck(not _is_effect(_IplusS, 2),
       "and I + S must be REJECTED as an effect: it is PSD with eigenvalue 2, so "
       "only the I - E >= 0 half can exclude it -- the guard that catches a "
       "predicate which drops that half")
    S_bare = [[F(0), F(1)], [F(1), F(0)]]
    ck(not _is_effect(S_bare, 2),
       "and the predicate must REJECT the bare off-diagonal symmetry (spectrum "
       "+-1), or it could be a constant -- this is the witness that makes the "
       "(I+S)/2 choice load-bearing rather than decorative")
    # 1/2 on the diagonal, -3/10 on EVERY off-diagonal: every 2x2 minor is
    # 1/4 - 9/100 > 0, while the all-ones vector has eigenvalue
    # 1/2 - 2*(3/10) = -1/10, so the 3x3 minor is -8/125 < 0.
    E_bad = [[F(1, 2) if a_ == b_ else F(-3, 10) for b_ in range(3)]
             for a_ in range(3)]
    ck(not _is_effect(E_bad, 3),
       "and must reject a matrix that passes every 2x2 minor but has a negative "
       "eigenvalue -- the soundness defect the earlier predicate had at n >= 3")
    ck(all(_is_state(h, n) for n in (2, 3) for h in _loads(n)),
       "and every tested LOAD must be a state: symmetric, PSD, unit trace -- the "
       "same argument that constrains the effects constrains the loads")

    # ---- L1: on the standard MASA the map under test IS the .412 route.
    # Independent re-implementation from the .412 docstring, not a copy of the
    # map under test; the NON-MASA control shows the identity is MASA-specific.
    ident_ok = True
    ident_rows = {2: 0, 3: 0, 4: 0}
    used = {}
    # ONE constructed probe per n, built once and SHARED between the loop and
    # the off-diagonal assertion below.  Building it twice is how a validation
    # ends up exercising its own copy of the logic: a mutation that diagonalized
    # the probe used in the loop left a separately-written assertion passing.
    constructed = {n: [[F(i + 1, j + 2) + F(j + 1, i + 2) for j in range(n)]
                       for i in range(n)] for n in (2, 3, 4)}
    for n in (2, 3, 4):
        Qs = _rank1_diag_projectors(n)
        probes = list(_loads(n)) if n in (2, 3) else []
        probes.append(constructed[n])
        for X in probes:
            if len(X) != n:
                continue
            ident_rows[n] += 1
            used.setdefault(n, []).append(X)
            if _diag_part(X, n) != _conditional_expectation(X, Qs, n):
                ident_ok = False
    ck(ident_ok,
       "on the standard MASA the map under test must equal sum_i Q_i X Q_i -- "
       "the .412 conditional expectation, re-derived independently")
    # THE ROW COUNTS ARE PINNED.  Without this the n = 4 arm is decorative: the
    # `if len(X) != n: continue` filter silently drops every probe whose size
    # does not match, so a change that emptied the n = 4 arm would leave the leg
    # passing while claiming three dimensions.  n = 4 supplies exactly the one
    # constructed probe, because _loads only reaches n = 3.
    ck(ident_rows[4] == 1,
       "the n = 4 arm must contribute EXACTLY its one constructed probe (got "
       "%d) -- pinned, because the size filter would otherwise let an empty arm "
       "pass while the claim names three dimensions" % ident_rows[4])
    ck(ident_rows[2] == len(list(_loads(2))) + 1
       and ident_rows[3] == len(list(_loads(3))) + 1,
       "and the n = 2 and n = 3 arms must contribute EXACTLY the state loads "
       "plus the one constructed probe (got %d and %d) -- exact, like the "
       "n = 4 row, because an inequality would pass a silently thinned arm"
       % (ident_rows[2], ident_rows[3]))
    # and the probe ACTUALLY USED must be OFF-DIAGONAL at every n, or the
    # identity is being tested only on input the two maps agree on trivially.
    for n in (2, 3, 4):
        Xn = constructed[n]
        # MEMBERSHIP FIRST.  Asserting a property of `constructed[n]` says
        # nothing unless `constructed[n]` is what the loop actually tested; a
        # mutation that appended a freshly built diagonal matrix instead left
        # this block passing on an object nobody used.
        ck(Xn in used.get(n, []),
           "the probe the off-diagonal assertions are about must be one the "
           "identity loop actually tested at n = %d -- membership, not a "
           "separately built copy" % n)
        ck(any(Xn[i][j] != F(0)
               for i in range(n) for j in range(n) if i != j),
           "the constructed probe at n = %d must carry off-diagonal content, or "
           "diag(X) = sum_i Q_i X Q_i is tested only on diagonal input" % n)
        ck(_diag_part(Xn, n) != Xn,
           "and it must not already equal its own diagonal part at n = %d" % n)

    Pa = [[F(1) if (i == j and i < 2) else F(0) for j in range(4)] for i in range(4)]
    Pb = [[F(1) if (i == j and i >= 2) else F(0) for j in range(4)] for i in range(4)]
    G = [[F(1, 8)] * 4 for _ in range(4)]
    ck(_conditional_expectation(G, [Pa, Pb], 4) != _diag_part(G, 4),
       "NON-MASA CONTROL: with rank-2 joint projections the conditional "
       "expectation keeps off-diagonal content inside a block, so the identity "
       "above is MASA-specific and not a general fact about the two maps")

    # ---- L2: the exact separation identity.
    viol = 0
    nonzero = 0
    agree_diag = sep_diag = sep_off = off_total = 0
    for n in (2, 3):
        for h in _loads(n):
            for tag, e in _effects(n):
                d = _score(_diag_part(h, n), e)
                b = _born(h, e)
                if d is None or b is None:
                    continue
                lhs = b - d
                rhs = _tr(_mm(_offdiag(h, n), _offdiag(e, n))) / _tr(h)
                if lhs != rhs:
                    viol += 1
                if lhs != 0:
                    nonzero += 1
                if tag == "diag":
                    if lhs == 0:
                        agree_diag += 1
                    else:
                        sep_diag += 1
                else:
                    off_total += 1
                    if lhs != 0:
                        sep_off += 1
    ck(viol == 0 and nonzero == 7,
       "THE IDENTITY: Born - Dephasing == Tr(offdiag(h).offdiag(e))/Tr(h) "
       "exactly (expect 7 non-zero cases, got %d; %d violations)"
       % (nonzero, viol))
    ck(sep_diag == 0 and agree_diag == 19,
       "the two laws AGREE on every DIAGONAL effect (expect 19, got %d; %d "
       "separations) -- the count is pinned so a reduced battery cannot pass"
       % (agree_diag, sep_diag))
    ck(sep_off == 7 and off_total == 14,
       "and they separate ONLY on off-diagonal effects (expect 7 of 14, got "
       "%d of %d)" % (sep_off, off_total))

    # ---- L3: every separating effect is a .412 coherence witness.
    witnessed = commuting = 0
    for n in (2, 3):
        gens = _rank1_diag_projectors(n)
        for h in _loads(n):
            for _, e in _effects(n):
                d = _score(_diag_part(h, n), e)
                b = _born(h, e)
                if d is None or b is None or d == b:
                    continue
                witnessed += 1
                if all(_commutes(e, Q) for Q in gens):
                    commuting += 1
    ck(witnessed == 7 and commuting == 0,
       "every effect separating the two laws must FAIL to commute with a "
       "diagonal generator -- the .412 leg (iii) coherence witness (expect 7 "
       "separating, got %d; %d commuting)" % (witnessed, commuting))

    # ---- L4: DISCRIMINATING control -- diagonal agreement is not generic.
    ctrl = 0
    for n in (2, 3):
        for h in _loads(n):
            for tag, e in _effects(n):
                if tag != "diag":
                    continue
                s = _score(_sigma_lambda(F(1, 2), h, n), e)
                b = _born(h, e)
                if s is not None and b is not None and s != b:
                    ctrl += 1
    ck(ctrl == 12,
       "CONTROL: the depolarizing law at lambda = 1/2 SEPARATES from Born "
       "already on diagonal effects (expect 12, got %d) -- so agreement on the "
       "diagonal algebra is a property of THIS map, not of non-Born laws "
       "generally" % ctrl)

    # ---- L5: TWO-ROUTE defence -- the right-hand side is not the left.
    other = 0
    for n in (2, 3):
        for h in _loads(n):
            for _, e in _effects(n):
                s = _score(_sigma_lambda(F(1, 2), h, n), e)
                b = _born(h, e)
                if s is None or b is None:
                    continue
                if b - s != _tr(_mm(_offdiag(h, n), _offdiag(e, n))) / _tr(h):
                    other += 1
    ck(other == 19,
       "MAP-SPECIFICITY: the same right-hand side must FAIL for the depolarizing "
       "law wherever that law differs from Born (expect 19 of 33, got %d). NOTE the honest reading, corrected after "
       "audit: this does NOT show the identity is non-tautological -- it IS an "
       "identity of diag and offdiag (leg L7). It shows only that the right-hand "
       "side is specific to THIS map, which is a weaker and true claim" % other)

    # ---- L6: positive control.
    bornish = 0
    for n in (2, 3):
        for h in _loads(n):
            for _, e in _effects(n):
                s = _score(_sigma_lambda(F(1), h, n), e)
                b = _born(h, e)
                if s is not None and b is not None and s != b:
                    bornish += 1
    ck(bornish == 0,
       "POSITIVE CONTROL: the lambda = 1 member of the depolarizing family must "
       "equal Born on every tested effect")

    # ---- L7: the identity is GENERAL -- arbitrary matrices, no Hermiticity,
    # no positivity, no normalization.  This is what makes it an identity of the
    # definitions rather than a fact about these maps, and it is the honest
    # replacement for the "two-route defence" leg, which could not fail.
    gen_viol = gen_cases = 0
    seed = 7
    gen_by_n = {2: 0, 3: 0, 4: 0, 5: 0}
    live_by_n = {2: 0, 3: 0, 4: 0, 5: 0}
    for n in (2, 3, 4, 5):
        for _ in range(12):
            H = []
            for i in range(n):
                row = []
                for j in range(n):
                    seed = (seed * 1103515245 + 12345) % 2147483648
                    row.append(F(seed % 41 - 20, (seed % 7) + 1))
                H.append(row)
            Eg = []
            for i in range(n):
                row = []
                for j in range(n):
                    seed = (seed * 1103515245 + 12345) % 2147483648
                    row.append(F(seed % 31 - 15, (seed % 5) + 1))
                Eg.append(row)
            if _tr(H) == 0:
                continue
            gen_cases += 1
            gen_by_n[n] += 1
            rhs = _tr(_mm(_offdiag(H, n), _offdiag(Eg, n))) / _tr(H)
            lhs = _tr(_mm(H, Eg)) / _tr(H) - _tr(_mm(_diag_part(H, n), Eg)) / _tr(_diag_part(H, n))
            if lhs != rhs:
                gen_viol += 1
            # A case is LIVE only if both sides can actually differ from zero:
            # both matrices must carry off-diagonal content and the identity's
            # right-hand side must be non-zero.  Without this the whole sweep
            # can be reduced to 0 == 0 -- found by mutation, twice: forcing the
            # sampled effects diagonal, and forcing the sampled loads diagonal,
            # each left 48 cases and 0 violations and a passing leg.
            if (_offdiag(H, n) != [[F(0)] * n for _ in range(n)]
                    and _offdiag(Eg, n) != [[F(0)] * n for _ in range(n)]
                    and rhs != F(0)):
                live_by_n[n] += 1
    ck(gen_viol == 0 and gen_cases >= 40,
       "GENERALITY: the identity must hold for ARBITRARY square matrices -- not "
       "Hermitian, not positive, not normalized, n = 2..5 (%d cases, %d "
       "violations). This is why it is an identity of diag and offdiag rather "
       "than a fact about the two laws" % (gen_cases, gen_viol))
    # PER-DIMENSION, SET-EXACT.  A total is not coverage: replacing the
    # dimension tuple with (2, 2, 2, 2) yields 48 cases and 0 violations and
    # passes the count above, while "n = 2..5" becomes false.
    ck(set(gen_by_n) == {2, 3, 4, 5},
       "the generality sweep must cover exactly the dimensions it names")
    ck(all(gen_by_n[n] >= 10 for n in (2, 3, 4, 5)),
       "and each named dimension must contribute at least ten cases (got %s) -- "
       "pinned per n, because the case total cannot tell four dimensions from "
       "one repeated four times" % (gen_by_n,))
    ck(all(live_by_n[n] >= 5 for n in (2, 3, 4, 5)),
       "and each dimension must contribute at least five cases in which BOTH "
       "matrices carry off-diagonal content and the identity's right-hand side "
       "is NON-ZERO (got %s) -- otherwise the sweep is verifying 0 = 0"
       % (live_by_n,))

    # ---- L8: coherence in the load plus an off-diagonal effect is NECESSARY
    # but NOT SUFFICIENT.  One complex witness, and it is the whole reason the
    # earlier phrasing was withdrawn.
    half = F(1, 2)
    # (I + sigma_y)/2 and (I + sigma_x)/2 as 2x2 complex matrices, carried as
    # (re, im) pairs only here -- the rest of the module is the real slice.
    def _c_tr2(A):
        return (A[0][0][0] + A[1][1][0], A[0][0][1] + A[1][1][1])

    def _c_mm2(A, B):
        out = [[None, None], [None, None]]
        for i in range(2):
            for j in range(2):
                re = im = F(0)
                for k in range(2):
                    re += A[i][k][0] * B[k][j][0] - A[i][k][1] * B[k][j][1]
                    im += A[i][k][0] * B[k][j][1] + A[i][k][1] * B[k][j][0]
                out[i][j] = (re, im)
        return out

    h_y = [[(half, F(0)), (F(0), -half)], [(F(0), half), (half, F(0))]]
    e_x = [[(half, F(0)), (half, F(0))], [(half, F(0)), (half, F(0))]]
    h_y_deph = [[h_y[i][j] if i == j else (F(0), F(0)) for j in range(2)]
                for i in range(2)]
    born_c = _c_tr2(_c_mm2(h_y, e_x))[0] / _c_tr2(h_y)[0]
    deph_c = _c_tr2(_c_mm2(h_y_deph, e_x))[0] / _c_tr2(h_y_deph)[0]
    ck(h_y[0][1] != (F(0), F(0)) and e_x[0][1] != (F(0), F(0)),
       "the witness load must carry coherence AND the witness effect must have "
       "an off-diagonal part, or it does not test sufficiency")
    ck(born_c == deph_c == half,
       "NECESSARY BUT NOT SUFFICIENT: at load (I+sigma_y)/2 and effect "
       "(I+sigma_x)/2 -- coherence present, off-diagonal effect present -- the "
       "two laws AGREE at %s. So 'coherence in the load and an off-diagonal "
       "effect' does NOT imply separation; the condition is a non-vanishing "
       "pairing of the two coherence sectors" % born_c)

    key = (
        "THE DISAGREEMENT IS EXACTLY THE COHERENCE SECTOR. On the standard MASA "
        "the dephasing map is the conditional expectation that "
        "commutative_no_unresolved_hold banks (computed; the NON-MASA control "
        "shows the identity is MASA-specific), and the two score laws differ by "
        "Tr(offdiag(h) . offdiag(e)) / Tr(h) EXACTLY. Three consequences, all "
        "computed: they agree on every diagonal effect (19 of 19); they separate "
        "only when the load carries coherence AND the effect reads it (7 of 14 "
        "off-diagonal cases); and every separating effect fails to commute with "
        "a diagonal generator, which is precisely the coherence witness that "
        "module's leg (iii) names. WHAT THE IDENTITY IS: an ALGEBRAIC IDENTITY of "
        "diag and offdiag -- Tr(diag(h)) = Tr(h), and offdiag has zero diagonal "
        "-- verified for ARBITRARY square matrices, not Hermitian, not positive, "
        "not normalized, at n = 2..5. It could not have come out otherwise, and "
        "is billed as the exact sector of disagreement rather than as a "
        "discovery. THE COHERENCE CONDITION IS NECESSARY, NOT SUFFICIENT: at "
        "load (I+sigma_y)/2 with effect (I+sigma_x)/2 -- coherence present, "
        "off-diagonal effect present -- the two laws AGREE at 1/2; the true "
        "condition is a non-vanishing pairing of the two coherence sectors. "
        "DISCRIMINATION: "
        "the depolarizing law at lambda = 1/2 separates from Born already on "
        "diagonal effects, so agreement on the diagonal algebra is a property of "
        "this map and not of non-Born laws generally. THIS LOCATES THE "
        "DISAGREEMENT; IT DOES NOT REFUTE THE MAP, and it does not license the "
        "step from 'the effects are diagonal' to 'the world is Born' -- that "
        "needs the admissible effect algebra tied to the gauge group, which is "
        "not established."
    )
    return _result(
        'L_coherence_sector_separation',
        'P_math -- exact rational linear algebra; no physical premise consumed',
        key,
        {
            "separation_identity": "Born - Dephasing = Tr(offdiag(h).offdiag(e))/Tr(h)",
            "identity_is_general_arbitrary_matrices": (gen_viol == 0),
            "identity_general_cases": gen_cases,
            "coherence_condition_sufficient": (born_c != deph_c),
            "necessary_not_sufficient_witness": "load (I+sy)/2, effect (I+sx)/2, "
                                                "both laws = 1/2",
            "identity_violations": viol,
            "identity_nonzero_cases": nonzero,
            "diagonal_effects_agreeing": agree_diag,
            "diagonal_effects_separating": sep_diag,
            "offdiagonal_separating_of_total": [sep_off, off_total],
            "separating_effects_commuting_with_a_generator": commuting,
            "depolarizing_control_diagonal_separations": ctrl,
            "two_route_defence_failures_for_other_law": other,
            "masa_identity_with_412_route": ident_ok,
        },
        fails, 3,
        (),   # no A1 edge: nothing here consumes a capacity axiom or a cost floor
        (),
        ("the depolarizing law separates on diagonal effects, so diagonal "
         "agreement is not generic",
         "the bare off-diagonal symmetry is REJECTED as an effect",
         "a matrix passing every 2x2 minor with a negative eigenvalue is "
         "rejected -- the n>=3 soundness defect",
         "the (I+sy)/2 vs (I+sx)/2 witness: coherence and an off-diagonal "
         "effect are NOT sufficient for separation",
         "a non-MASA projector spec breaks the identification of the two maps",
         "lambda = 1 reproduces Born everywhere"),
        ('L_commutative_no_unresolved_hold',
         'L_covariant_state_maps_are_exactly_the_depolarizing_line',
         'L_gauge_without_sandwich_admits_non_born_states'),
        fail_count=tally[0],
    )


_CHECKS = {
    'L_coherence_sector_separation': check_L_coherence_sector_separation,

}

CHECKS = tuple(_CHECKS.values())


def register(registry):
    """The bank's entry point.  bank.py imports the module and calls this with
    the live REGISTRY; a module without it registers nothing and shows up as a
    gap, which is exactly how this one was caught before landing."""
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, object]:
    out = {}
    for fn in CHECKS:
        r = fn()
        out[r['name']] = r
    return out


if __name__ == '__main__':
    for name, r in run_all().items():
        print(('PASS  ' if r['passed'] else 'FAIL  ') + name)
        for f in r['fail_reasons']:
            print('   - ' + f)
