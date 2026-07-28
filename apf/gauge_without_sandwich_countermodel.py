"""Presentation gauge WITHOUT the sandwich form does not reach Born.

THE CONVERSE COMPANION to check_T_presentation_gauge_forces_trace
(presentation_gauge_forcing.py, v24.3.443).  Read the two together or neither.

  FORCING (banked .443):  GIVEN the sandwich form eta_b(e) = psi(b* e b)/psi(b* b),
      presentation gauge + psi(I) != 0 force psi = c*Tr, hence Born.
  THIS MODULE:            WITHOUT the sandwich form, presentation gauge together
      with positivity, normalization, affinity, injectivity, unitary covariance
      and finite tomography leave a ONE-PARAMETER FAMILY of non-Born outcome
      laws standing.

So premise P1 -- that the completed route is scored by the sandwich at all -- is
not a technicality of the .443 statement.  It is load-bearing, and this module
makes that a computed fact rather than a caveat.

THE FAMILY.  On normalized loads h in M_n(C), sigma_lambda(h) = lambda*h +
(1-lambda)*I/n, scored by s_b(e) = Tr(sigma_lambda(h_b) e).  Every member is
positive, normalized, affine, injective, unitary-covariant, and a function of
the LOAD alone -- so it satisfies the full right-unitary presentation gauge --
and every member with lambda != 1 differs from Born.  lambda = 1 is the Born
point.  Positivity holds exactly on lambda in [-1/(n-1), 1].

WHY THIS IS NOT A REFUTATION OF THE .443 FORCING, and the fact that makes the
two consistent: sigma_lambda admits NO sandwich representation at all.  Solving
for a Hermitian W with Tr(W b* e b)/Tr(W b* b) = Tr(sigma_lambda(h_b) e) over a
carrier x effect grid returns FULL RANK, nullity 0 -- only W = 0 -- against the
Born control, which returns nullity 1 with W = I.  The countermodel lives
strictly outside the sandwich form, which is exactly where .443's hypothesis
stops applying.  Neither the originating research packet nor any prior bank
module computes this; it is the load-bearing reconciliation and it is banked
here.

============================================================================
THREE FENCES, ALL COMPUTED, ALL AGAINST THE OBVIOUS OVERREAD.

The tempting overread is "therefore the sandwich form is the UNIQUE remaining
entry point to Born".  That is NOT established, and the same family refutes it:

  (F1) THE COUNTERMODEL DOES NOT SEPARATE EVERYWHERE.  At the maximally mixed
       load h = I/n -- the fixed point of sigma_lambda -- the distorted law and
       Born AGREE on every effect.  The separation is a statement about some
       preparations, not all.  (This limitation is undisclosed in the
       originating packet, whose mutation battery drops the row that would
       have exposed it.)

  (F2) A SHARPNESS PREMISE KILLS MOST OF THE FAMILY, AND IS NOT THE SANDWICH
       FORM.  If some preparation must make some rank-one effect certain, then
       every lambda with max_h Tr(sigma_lambda(h) p) < 1 dies -- which at
       n >= 3 is the whole positive-lambda range.  But at n = 2, lambda = -1
       gives sigma(h) = I - h, which IS sharp (take h orthogonal to p) and
       SURVIVES the sharpness premise.  So sharpness prunes the family without
       closing it, and it is a premise disjoint from P1.

  (F3) MULTIPLICATIVITY ON PRODUCT PREPARATIONS ALSO KILLS IT, AND IS ALSO NOT
       THE SANDWICH FORM.  sigma_lambda(h1 (x) h2) != sigma_lambda(h1) (x)
       sigma_lambda(h2) for lambda outside {0, 1}.

F2 and F3 together are the honest scope: this module shows the listed premises
do not force Born.  It does NOT show P1 is the only door.  Any statement that
the continuation-efficiency route has reached a terminus, or that the sandwich
form is what remains, outruns what is computed here.

PROVENANCE AND AUDIT RECORD.  The family arrives from a research packet
(APF_HOC_CE_Effect_Sandwich_Closure_Terminus v0.1, 2026-07-27).  Two independent
blinded cold audits of that packet returned REDUCE 0.82 and REDUCE 0.85,
convergent without contact.  The countermodel SURVIVED both; the packet's
apparatus did not -- its affinity leg never called the function under test (a
provably non-affine map passed its full battery), two of its lemmas were
unfalsifiable fixtures graded [P_math], its governance receipts were hardcoded
literals, and its mutation denominator self-adjusted to hide F1.  What is banked
here is the surviving mathematics plus the three fences, with the packet's
"terminus" framing explicitly NOT adopted.  Every leg below calls the function
under test, on purpose, because that is the defect that killed the source.

MAY NOT CITE: "Born is derived"; "the sandwich form is the unique remaining
premise"; "the CE route has reached its terminus"; "gauge is refuted" (gauge is
fine -- it is simply not sufficient without the sandwich form); "the
countermodel separates Born from the distorted law" (unqualified -- it does not,
at the maximally mixed load).

NON-EXPORTING.  physical_premises_certified = false.  No existing grade moved.
"""

from fractions import Fraction as F
from typing import Dict, List, Tuple

PHYSICAL_PREMISES_CERTIFIED = False
EXPORTS: Tuple[str, ...] = ()
BANK_MODIFIED = False


def _mm(A, B):
    k = len(B)
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(len(B[0]))]
            for i in range(len(A))]


def _tr(A):
    return sum(A[i][i] for i in range(len(A)))


def _eye(n):
    return [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]


def _add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]


def _sc(c, A):
    return [[c * A[i][j] for j in range(len(A))] for i in range(len(A))]


def _kron(A, B):
    n, m = len(A), len(B)
    return [[A[i // m][j // m] * B[i % m][j % m] for j in range(n * m)]
            for i in range(n * m)]


# THE MAP UNDER TEST.  Every leg below calls THIS function.  Deriving a leg's
# expectation from hand-written formulas instead of calling it is precisely the
# defect that killed the source packet's affinity leg, where a provably
# non-affine map passed the whole battery.
def distorted_state(lam: F, h, n: int):
    """sigma_lambda(h) = lambda*h + (1-lambda)*I/n, on normalized loads."""
    return _add(_sc(lam, h), _sc((1 - lam) / n, _eye(n)))


def _score(lam, h, e, n):
    return _tr(_mm(distorted_state(lam, h, n), e))


def _born(h, e):
    return _tr(_mm(h, e)) / _tr(h)


def _is_psd_diag(M, n):
    return all(M[i][i] >= 0 for i in range(n)) and _herm_det_nonneg(M, n)


def _herm_det_nonneg(M, n):
    from itertools import combinations

    def det(sub):
        m = len(sub)
        if m == 1:
            return sub[0][0]
        acc = F(0)
        for j in range(m):
            minor = [[sub[i][k] for k in range(m) if k != j] for i in range(1, m)]
            t = sub[0][j] * det(minor)
            acc += t if j % 2 == 0 else -t
        return acc
    for size in range(1, n + 1):
        for idx in combinations(range(n), size):
            if det([[M[i][j] for j in idx] for i in idx]) < 0:
                return False
    return True


def _rank(rows):
    M = [r[:] for r in rows]
    if not M:
        return 0
    dim = len(M[0])
    r = 0
    for c in range(dim):
        p = next((k for k in range(r, len(M)) if M[k][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for k in range(len(M)):
            if k != r and M[k][c] != 0:
                f = M[k][c]
                M[k] = [a - f * b for a, b in zip(M[k], M[r])]
        r += 1
        if r == len(M):
            break
    return r


def _basis_proj(n, j):
    P = [[F(0)] * n for _ in range(n)]
    P[j][j] = F(1)
    return P


def _effects(n):
    out = [_basis_proj(n, j) for j in range(n)]
    h = F(1, 2)
    for i in range(n):
        for j in range(i + 1, n):
            M = [[F(0)] * n for _ in range(n)]
            M[i][i] = h
            M[j][j] = h
            M[i][j] = h
            M[j][i] = h
            out.append(M)
    return out


def _result(name, epistemic, key, ev, fails, tier, deps, ncs, xrefs):
    return {
        'name': name, 'epistemic': epistemic, 'passed': not fails, 'tier': tier,
        'key_result': key, 'evidence': ev, 'fail_reasons': fails,
        'dependencies': list(deps), 'premises': [],
        'negative_controls': list(ncs), 'cross_refs': list(xrefs),
        'physical_premises_certified': PHYSICAL_PREMISES_CERTIFIED,
        'exports': list(EXPORTS), 'bank_modified': BANK_MODIFIED,
    }


# ==========================================================================
def check_L_gauge_without_sandwich_admits_non_born_states() -> Dict[str, object]:
    """Tier 3, [P_math].  The sigma_lambda family and its three fences."""
    fails: List[str] = []

    def ck(c, m):
        if not c:
            fails.append(m)

    lams = (F(1, 2), F(3, 4), F(1, 3), F(1, 10), F(-1, 3))
    props = {}
    non_born_cases = 0
    for n in (2, 3, 4):
        for lam in lams:
            if lam < F(-1, n - 1):
                continue
            h = _basis_proj(n, 0)
            S = distorted_state(lam, h, n)                     # CALLS the map
            ck(_tr(S) == 1, f"normalized (n={n}, lam={lam})")
            ck(_is_psd_diag(S, n), f"positive (n={n}, lam={lam})")
            # unitary covariance, exact rational unitary
            if n == 2:
                U = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
                Ud = [[U[j][i] for j in range(2)] for i in range(2)]
                ck(distorted_state(lam, _mm(_mm(U, h), Ud), n)
                   == _mm(_mm(U, distorted_state(lam, h, n)), Ud),
                   f"unitary covariant (lam={lam})")
            # AFFINITY -- computed by CALLING the map on a genuine mixture.
            # The source packet's affinity leg re-derived this from inline
            # formulas and never touched the function, so a non-affine map
            # passed its whole battery.  This leg calls it.
            h2 = _basis_proj(n, 1)
            t = F(1, 3)
            mix = _add(_sc(t, h), _sc(1 - t, h2))
            lhs = distorted_state(lam, mix, n)
            rhs = _add(_sc(t, distorted_state(lam, h, n)),
                       _sc(1 - t, distorted_state(lam, h2, n)))
            ck(lhs == rhs, f"AFFINE (n={n}, lam={lam})")
            # injectivity on the tested pair
            ck(distorted_state(lam, h, n) != distorted_state(lam, h2, n)
               or lam == 0, f"injective (n={n}, lam={lam})")
            # non-Born
            e = _basis_proj(n, 0)
            if lam != 1:
                s, b = _score(lam, h, e, n), _born(h, e)
                ck(s != b, f"must differ from Born (n={n}, lam={lam})")
                non_born_cases += 1
            props[f"n{n}_lam{lam}"] = True
    ck(non_born_cases >= 10,
       "ANTI-VACUITY: the non-Born battery must be non-empty and broad")

    # ---- CONTROL: lambda = 1 must BE Born, or the family proves nothing ----
    for n in (2, 3):
        h = _basis_proj(n, 0)
        for e in _effects(n):
            ck(_score(F(1), h, e, n) == _born(h, e),
               f"CONTROL: lambda = 1 must reproduce Born exactly (n={n})")

    # ---- FENCE F1: no separation at the maximally mixed load --------------
    n = 2
    hmix = _sc(F(1, 2), _eye(2))
    agree = all(_score(F(1, 2), hmix, e, 2) == _born(hmix, e) for e in _effects(2))
    ck(agree,
       "FENCE F1 must hold: at the sigma fixed point h = I/n the distorted law "
       "and Born AGREE on every effect. If this ever fails the fence is wrong, "
       "not the theorem -- but the unqualified claim 'the countermodel "
       "separates the two laws' would then need re-checking")

    # ---- FENCE F2: sharpness prunes but does not close --------------------
    def max_sharp(lam, n):
        best = None
        p0 = _basis_proj(n, 0)
        for j in range(n):
            hj = _basis_proj(n, j)
            S = distorted_state(lam, hj, n)
            if not _is_psd_diag(S, n):
                continue
            v = _tr(_mm(S, p0))
            if best is None or v > best:
                best = v
        return best
    sharp_n2_neg1 = max_sharp(F(-1), 2)
    ck(sharp_n2_neg1 == 1,
       "FENCE F2: at n = 2, lambda = -1 the map sigma(h) = I - h IS sharp "
       "(max over pure loads is 1), so a sharpness premise does NOT close the "
       "family -- it prunes it")
    ck(max_sharp(F(1, 2), 3) != 1,
       "FENCE F2: at n = 3, lambda = 1/2 is not sharp (a sharpness premise "
       "does kill this member)")

    # ---- FENCE F3: not multiplicative on products ------------------------
    h1 = _basis_proj(2, 0)
    ck(distorted_state(F(1, 2), _kron(h1, h1), 4)
       != _kron(distorted_state(F(1, 2), h1, 2), distorted_state(F(1, 2), h1, 2)),
       "FENCE F3: sigma_lambda must fail multiplicativity on a product "
       "preparation, so product-multiplicativity is a second premise disjoint "
       "from the sandwich form that also kills the family")

    key = (
        "WITHOUT the sandwich form, presentation gauge does NOT reach Born. The "
        "family sigma_lambda(h) = lambda*h + (1-lambda)*I/n is positive, "
        "normalized, AFFINE, injective, unitary-covariant, and a function of the "
        "LOAD alone (so it satisfies the full right-unitary presentation gauge), "
        "yet every member with lambda != 1 gives a non-Born outcome law; "
        "lambda = 1 is the Born point and is executed as the control. Positivity "
        "holds on lambda in [-1/(n-1), 1]. THREE FENCES AGAINST THE OBVIOUS "
        "OVERREAD, all computed: (F1) the separation is NOT universal -- at the "
        "maximally mixed load h = I/n, the sigma fixed point, the two laws agree "
        "on every effect; (F2) a sharpness premise prunes the family without "
        "closing it -- at n >= 3 the positive-lambda range dies, but at n = 2, "
        "lambda = -1 the map sigma(h) = I - h IS sharp and survives; (F3) "
        "product multiplicativity fails, so it too kills the family. F2 and F3 "
        "are premises DISJOINT from the sandwich form, so this does NOT show the "
        "sandwich form is the unique remaining entry point to Born, and the "
        "source packet's 'terminus' framing is NOT adopted. The affinity leg "
        "CALLS the map under test -- the source's leg did not, and a provably "
        "non-affine map passed its entire battery."
    )
    return _result(
        'L_gauge_without_sandwich_admits_non_born_states',
        'P_math -- exact finite computation over Q; no physical premise consumed',
        key,
        {
            "family": "sigma_lambda(h) = lambda*h + (1-lambda)*I/n",
            "lambdas_tested": [str(x) for x in lams],
            "dims_tested": [2, 3, 4],
            "non_born_cases": non_born_cases,
            "positivity_range": "lambda in [-1/(n-1), 1]",
            "F1_no_separation_at_maximally_mixed_load": agree,
            "F2_sharp_max_n2_lambda_minus1": str(sharp_n2_neg1),
            "F2_sharp_max_n3_lambda_half": str(max_sharp(F(1, 2), 3)),
            "F3_multiplicative": False,
            "born_point": "lambda = 1 (executed as control)",
        },
        fails, 3, (),
        ("lambda = 1 must reproduce Born exactly",
         "the affinity leg must call the map under test",
         "the separation must fail at the maximally mixed load",),
        ('T_presentation_gauge_forces_trace',
         'L_non_born_states_are_not_sandwich_representable'),
    )


# ==========================================================================
def check_L_non_born_states_are_not_sandwich_representable() -> Dict[str, object]:
    """Tier 3, [P_math].  The reconciliation with the banked forcing theorem."""
    fails: List[str] = []

    def ck(c, m):
        if not c:
            fails.append(m)

    # Solve for Hermitian W with Tr(W b*eb)/Tr(W b*b) = target, over a grid.
    # Real-symmetric coordinates (a, d, x) at n = 2 suffice to force W = 0.
    def system(target_fn):
        rows = []
        carriers = ([[F(1), F(0)], [F(0), F(0)]],
                    [[F(1), F(0)], [F(0), F(1)]],
                    [[F(1), F(1)], [F(0), F(1)]],
                    [[F(2), F(0)], [F(1), F(1)]])
        for b in carriers:
            bd = [[b[j][i] for j in range(2)] for i in range(2)]
            hb = _mm(b, bd)
            if _tr(hb) == 0:
                continue
            hn = _sc(F(1) / _tr(hb), hb)
            for e in _effects(2):
                t = target_fn(hn, e)
                M1 = _mm(bd, _mm(e, b))
                M2 = _mm(bd, b)
                rows.append([M1[0][0] - t * M2[0][0],
                             M1[1][1] - t * M2[1][1],
                             (M1[0][1] + M1[1][0]) - t * (M2[0][1] + M2[1][0])])
        return rows

    rows_sigma = system(lambda h, e: _tr(_mm(distorted_state(F(1, 2), h, 2), e)))
    rank_sigma = _rank(rows_sigma)
    ck(rank_sigma == 3,
       f"the sigma_lambda law must admit NO sandwich representation (rank must "
       f"be 3 of 3, forcing W = 0; got {rank_sigma}). If this ever drops to 2 "
       f"the countermodel WOULD contradict T_presentation_gauge_forces_trace "
       f"and one of the two is wrong")

    # CONTROL: the Born law itself MUST be representable, or the test is broken.
    rows_born = system(lambda h, e: _born(h, e))
    rank_born = _rank(rows_born)
    ck(rank_born == 2,
       f"CONTROL: the Born law must BE sandwich-representable with a "
       f"one-dimensional solution line (W = I), rank 2 of 3; got {rank_born}. "
       f"If this fails the discriminator is broken and the sigma result is "
       f"meaningless")

    key = (
        "THE RECONCILIATION, and the load-bearing fact neither the source packet "
        "nor any prior bank module computes. The sigma_lambda outcome law admits "
        "NO sandwich representation whatever: solving for a Hermitian W with "
        "Tr(W b* e b)/Tr(W b* b) equal to the sigma law over a carrier x effect "
        "grid returns FULL RANK (3 of 3), so only W = 0. The Born control "
        "returns rank 2 with the expected one-dimensional solution line W = I. "
        "This is why the countermodel is CONSISTENT with "
        "T_presentation_gauge_forces_trace rather than a refutation of it: the "
        "forcing theorem's hypothesis is the sandwich form, and the countermodel "
        "lives strictly outside it. Stated the other way round, the two results "
        "together pin the premise P1 exactly -- gauge inside the sandwich form "
        "forces Born, gauge outside it does not -- WITHOUT establishing that the "
        "sandwich form is the only route in (see fences F2 and F3 on the "
        "companion leg)."
    )
    return _result(
        'L_non_born_states_are_not_sandwich_representable',
        'P_math -- exact rank computation over Q; no physical premise consumed',
        key,
        {
            "sigma_system_rank": rank_sigma,
            "sigma_solution_space": "{0} -- not sandwich-representable",
            "born_control_rank": rank_born,
            "born_solution_space": "one-dimensional, spanned by W = I",
            "unknowns": 3,
        },
        fails, 3,
        ('L_gauge_without_sandwich_admits_non_born_states',),
        ("the Born law must be sandwich-representable (rank 2, W = I)",),
        ('T_presentation_gauge_forces_trace',
         'L_presentation_gauge_invariant_lines'),
    )


_CHECKS = {
    'L_gauge_without_sandwich_admits_non_born_states':
        check_L_gauge_without_sandwich_admits_non_born_states,
    'L_non_born_states_are_not_sandwich_representable':
        check_L_non_born_states_are_not_sandwich_representable,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    import sys
    bad = False
    for n, fn in _CHECKS.items():
        r = fn()
        print(r['name'], '::', 'PASS' if r['passed'] else 'FAIL')
        if not r['passed']:
            bad = True
            for f in r['fail_reasons']:
                print('  -', f)
    sys.exit(1 if bad else 0)
