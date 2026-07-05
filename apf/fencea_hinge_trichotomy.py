"""The FENCE-A cost-to-state hinge trichotomy: one-sided cq separability,
the two-sided PPT threshold, and the joint-sufficiency law.

v24.3.340 + .341 (2026-07-02). Banks the finite-size arithmetic of the FENCE-A
hinge re-walk on the constitutive base, plus the correlation-hierarchy ladder
(v24.3.341: check_T_correlation_hierarchy_ladder; note "Reference - The
Correlation-Hierarchy Ladder in the Native Two-Cell Family (2026-07-02)" v0.2,
hostile-audited LAND-WITH-FIXES 0.85) (note "Reference - Re-Walking the
FENCE-A Hinge on the Constitutive Base (2026-07-02)", v0.2, hostile-audited
LAND-WITH-FIXES 0.84; witness The Turning/fencea_hinge_rewalk_probe.py).

THE HINGE (source: the 2026-06-24 cost-to-state probe): does IJC
noncommutativity reach the inter-diamond (shared-causal-interface)
coupling, promoting it from a classical density-density cost to a kinetic,
entangling term? The 06-24 dichotomy (reaches / within-cell) misses a
middle case. This check certifies the TRICHOTOMY on the two-cell Gibbs
model at the native |beta*eps| = ln 102:

  (B)  Diagonal L_nc density-density cost Delta*n1*n2: the Gibbs state is
       diagonal, hence separable (the 06-24 result, reproduced).
  (b)  ONE-SIDED non-commuting joint defender ([E_d1, P*] != 0 but
       [E_d2, P*] = 0): H commutes with the second cell's occupation
       operator, whose qubit spectrum is nondegenerate, so the Gibbs state
       is exactly classical-quantum => separable at EVERY parameter value.
       CONSEQUENCE: the T_inseparable_IJC bridge conclusion ("[E_di, P*]
       != 0 for at least one i") is INSUFFICIENT for cross-cut
       entanglement. This refutes a candidate forcing route, not a banked
       claim (the bank never asserted the bridge yields thermal-state
       entanglement).
  (c)  TWO-SIDED non-reducing (Bell-projector) defender: the Gibbs state
       is a 2x2 X-state; entangled IFF |p+ - p-|/2 > sqrt(p00*p11)
       (PPT, necessary and sufficient at 2x2, Horodecki 1996), which
       reduces EXACTLY to (1 - e^{-beta*mu})/2 > e^{-beta*Delta/2} --
       independent of eps, hence of the filling convention. Closed form:
       Delta*(mu) = (2/beta) * ln(2 / (1 - e^{-beta*mu})), large-mu
       asymptote 2*ln(2)/beta.

THE JOINT-SUFFICIENCY LAW (the physical content): at Delta = 0 the cut is
separable for EVERY defender weight mu (since (1-e^{-beta*mu})/2 < 1/2 <=
e^0); the L_nc superadditive cost Delta -- proved boost-inert alone by the
06-24 probe and constitutive since v24.3.304 -- is what OPENS the
entanglement region, by suppressing the corner population PPT weighs
against the cross coherence. Cost face gates; two-sided quantum face
supplies coherence; jointly sufficient above the closed-form threshold;
separately never.

GRADE ACCOUNTING (per the audited note): the strong FOUND-WANTING branch
of the 06-24 probe (separable net at every stage and in the limit) is dead
at INHERITANCE grade -- T_inseparable_IJC's Bell/KS clause is cross-cut --
and was already pre-.304; v24.3.304 retired only the import-gated framing.
The quantum PROFILE (which interfaces are quantum-capable) is unchanged at
[P+IJC]; natively the inter-diamond coupling is UN-FORBIDDEN, not forced.
NAMED GAP inherited downstream: Bell inheritance is state-EXISTENTIAL
(engineered pairs); the boost path needs the state-GENERIC form (native
state of a generic diamond cut). No boost claim, no geometric-2pi claim.

MODELING CONVENTION (named, load-bearing, NOT banked elsewhere): the
defender cost enters the Gibbs exponent as the OPERATOR mu*P* (the
defender's codespace projector), not as a diagonal scalar cost. This
placement is the sole source of off-diagonal structure in case (c); the
trichotomy is conditional on it. The two-cell model is the 06-24 probe's
own convention (at opposite filling; the results are exactly
filling-independent, certified below). For cells of dimension d > 2 the
cq argument in (b) requires the commuting local observable nondegenerate.

Grade P_structural tier 4: exact finite arithmetic (closed forms
throughout; no numerics beyond float evaluation of exponentials).
"""

import math as _math

from apf.apf_utils import check, _result

_LN102 = _math.log(102.0)
_BETA = 1.0


def _populations(eps, mu, delta):
    """Gibbs populations in the H_two eigenbasis {|00>, Bell+, Bell-, |11>}.

    H = eps*(n1+n2) + delta*n1*n2 + mu*P_Bell+ : eigenvalues 0, eps+mu,
    eps, 2*eps+delta (n1*n2 vanishes on the N=1 block; P fixes Bell+).
    """
    energies = (0.0, eps + mu, eps, 2.0 * eps + delta)
    weights = [_math.exp(-_BETA * (e - min(energies))) for e in energies]
    z = sum(weights)
    return [w / z for w in weights]


def _ppt_margin(eps, mu, delta):
    """X-state PPT margin: >0 <=> entangled (exact at 2x2, Horodecki).

    In the computational basis the state is an X-state with corners
    a = p00, d = p11 and N=1 coherence z = (p+ - p-)/2; the partial
    transpose's off-block is [[a, z], [z, d]], min eigenvalue
    (a+d)/2 - sqrt((a-d)^2/4 + z^2) < 0  <=>  z^2 > a*d.
    """
    p00, pp, pm, p11 = _populations(eps, mu, delta)
    return abs(pp - pm) / 2.0 - _math.sqrt(p00 * p11)


def _threshold_closed_form(mu):
    """Delta*(mu) = (2/beta) ln(2/(1 - e^{-beta*mu}))."""
    return (2.0 / _BETA) * _math.log(2.0 / (1.0 - _math.exp(-_BETA * mu)))


def check_T_fencea_hinge_coupling_trichotomy():
    """The FENCE-A hinge trichotomy + joint-sufficiency threshold, exact."""
    eps = _LN102

    # ---- (B) diagonal cost: separable (z = 0 identically) ---------------
    # With mu = 0 the N=1 block is degenerate: p+ = p-, coherence z = 0,
    # margin = -sqrt(p00*p11) < 0 for all Delta.
    for delta_f in (0.0, 0.3, 1.0, 2.0):
        m = _ppt_margin(eps, 0.0, delta_f * eps)
        check(m < 0.0, f"(B) diagonal cost must be separable; margin {m}")

    # ---- (b) one-sided defender: [H, n2] = 0 exactly => cq => separable -
    # H = eps*n1 + eps*n2 + Delta*n1n2 + mu*(|+><+| (x) |0><0|).
    # Verify the commutator vanishes ENTRYWISE in exact rational arithmetic:
    # basis order |00>,|01>,|10>,|11>; n2 = diag(0,1,0,1);
    # P_one[i][j] = 1/2 on {|00>,|10>} block, 0 elsewhere.
    n2_diag = (0, 1, 0, 1)
    p_one = ((0.5, 0.0, 0.5, 0.0),
             (0.0, 0.0, 0.0, 0.0),
             (0.5, 0.0, 0.5, 0.0),
             (0.0, 0.0, 0.0, 0.0))
    # [n2, P]_ij = (n2_i - n2_j) * P_ij ; vanishes iff P_ij = 0 whenever
    # n2_i != n2_j. Diagonal terms of H trivially commute with n2.
    one_sided_commutes = all(
        p_one[i][j] == 0.0
        for i in range(4) for j in range(4) if n2_diag[i] != n2_diag[j])
    check(one_sided_commutes,
          "(b) one-sided defender must commute with the second cell's "
          "occupation operator (cq block structure)")
    # cq => separable (standard); PPT margin from the block closed form:
    # within each n2 block the 2x2 Gibbs factor is a valid state; the
    # composite is sum_k q_k rho_k (x) |k><k|, PT leaves it PSD. Certify
    # via the X-structure absence: the only off-diagonal elements connect
    # |00>-|10> (same n2), which the qubit-2 partial transpose FIXES, so
    # PT(rho) = rho >= 0. Exact.
    check(n2_diag[0] == n2_diag[2],
          "(b) the one-sided coherence must live inside one n2 block")

    # ---- (c) two-sided defender: threshold law, eps-independent ---------
    # (c1) reduction identity: margin sign == sign of
    #      (1 - e^{-beta*mu})/2 - e^{-beta*Delta/2}, for BOTH conventions.
    for eps_signed in (+_LN102, -_LN102):
        for mu_f in (0.25, 0.5, 1.0, 2.0, 4.0):
            for delta_f in (0.0, 0.25, 0.30, 0.35, 0.5, 1.0, 2.0):
                mu = mu_f * _LN102
                delta = delta_f * _LN102
                margin = _ppt_margin(eps_signed, mu, delta)
                reduced = ((1.0 - _math.exp(-_BETA * mu)) / 2.0
                           - _math.exp(-_BETA * delta / 2.0))
                same_sign = (margin > 0) == (reduced > 0)
                # exclude exact-threshold ties (none on this grid)
                check(same_sign,
                      f"(c1) reduction identity failed at eps={eps_signed:+.3f} "
                      f"mu={mu_f} delta={delta_f}: margin {margin}, "
                      f"reduced {reduced}")

    # (c2) closed-form threshold vs bisection (eps-independent by (c1))
    for mu_f in (0.25, 0.5, 1.0, 2.0, 4.0):
        mu = mu_f * _LN102
        lo, hi = 0.0, 10.0 * _LN102
        for _ in range(80):
            mid = (lo + hi) / 2.0
            if _ppt_margin(_LN102, mu, mid) > 0.0:
                hi = mid
            else:
                lo = mid
        cf = _threshold_closed_form(mu)
        check(abs(hi - cf) < 1e-9,
              f"(c2) closed-form threshold mismatch at mu={mu_f}: "
              f"bisection {hi}, closed form {cf}")
    asymptote = 2.0 * _math.log(2.0) / _BETA
    check(abs(_threshold_closed_form(6.0 * _LN102) - asymptote) < 1e-6,
          "(c2) large-mu asymptote must be 2 ln2 / beta")

    # (c3) the joint-sufficiency law: Delta = 0 separable for ALL mu
    # (cost face gates); above threshold entangled (both faces together).
    for mu_f in (0.5, 1.0, 5.0, 50.0):
        check(_ppt_margin(_LN102, mu_f * _LN102, 0.0) < 0.0,
              f"(c3) Delta=0 must be separable at mu={mu_f} "
              f"(quantum face alone never suffices)")
    check(_ppt_margin(_LN102, 0.5 * _LN102, 1.0 * _LN102) > 0.0,
          "(c3) above threshold (mu=0.5eps, Delta=1.0eps) must be entangled")
    check(_ppt_margin(_LN102, 0.5 * _LN102, 0.3 * _LN102) < 0.0,
          "(c3) below threshold (mu=0.5eps, Delta=0.3eps) must be separable")

    return _result(
        name='T_fencea_hinge_coupling_trichotomy — one-sided cq '
             'separability + the two-sided PPT threshold + the '
             'joint-sufficiency law (the FENCE-A hinge, re-walked)',
        tier=4,
        epistemic='P_structural',
        summary=(
            'The FENCE-A cost-to-state hinge is a TRICHOTOMY, not the '
            '06-24 dichotomy: (B) diagonal L_nc cost separable (06-24 '
            'reproduced); (b) ONE-sided non-commuting defender exactly '
            'cq-separable at every parameter value — the '
            'T_inseparable_IJC bridge conclusion ("at least one E_di") '
            'is insufficient for cross-cut entanglement (a candidate '
            'forcing route refuted, not a banked claim); (c) TWO-sided '
            'defender entangled iff (1-e^{-beta mu})/2 > e^{-beta '
            'Delta/2}, exactly filling-independent, closed form '
            'Delta*(mu) = (2/beta) ln(2/(1-e^{-beta mu})), asymptote '
            '2ln2/beta. Joint-sufficiency law: at Delta=0 separable for '
            'all mu — the constitutive cost face gates the region, the '
            'profile-grade quantum face supplies the coherence; jointly '
            'sufficient, separately never. CONVENTION (load-bearing): '
            'defender cost enters the Gibbs exponent as the operator '
            'mu*P*; the trichotomy is conditional on that placement. '
            'FOUND-WANTING retired at inheritance grade (Bell/KS '
            'cross-cut clause); profile unchanged [P+IJC]; natively '
            'un-forbidden, not forced; state-existential vs '
            'state-generic gap named. No boost claim; no geometric-2pi '
            'claim.'
        ),
        key_result=(
            'One-sided defender: cq => separable exactly, all parameters. '
            'Two-sided: entangled iff (1-e^{-bm})/2 > e^{-bD/2}; '
            'Delta*(mu) = (2/b) ln(2/(1-e^{-bm})); Delta=0 never '
            'entangles. The bridge alone cannot force the cut; cost '
            'face + two-sided quantum face jointly sufficient.'
        ),
        dependencies=['L_nc', 'T_inseparable_IJC'],
        cross_refs=['L_KMS_trace_state', 'T_Tsirelson', 'L_loc'],
    )



# =====================================================================
# v24.3.341: the correlation-hierarchy ladder in the same family
# =====================================================================

def _corr_diag(eps, mu, delta):
    """Diagonal of the correlation matrix T for the family's X-state.

    c1 = c2 = <sx sx> = <sy sy> = p+ - p- (the coherence is real);
    c3 = <sz sz> = p00 + p11 - p+ - p-. Verified entrywise against the
    full density matrix in the audited note's independent reproduction.
    """
    p00, pp, pm, p11 = _populations(eps, mu, delta)
    return (pp - pm, pp - pm, p00 + p11 - pp - pm)


def _horodecki_M(eps, mu, delta):
    c1, c2, c3 = (abs(c) for c in _corr_diag(eps, mu, delta))
    sq = sorted((c1 * c1, c2 * c2, c3 * c3), reverse=True)
    return sq[0] + sq[1]


def _cjwr3(eps, mu, delta):
    c1, c2, c3 = _corr_diag(eps, mu, delta)
    return c1 * c1 + c2 * c2 + c3 * c3


def check_T_correlation_hierarchy_ladder():
    """The correlation hierarchy, rung by rung, inside the native family.

    LADDER (model-level; every statement conditional on the mu*P*
    Gibbs-placement convention of the .340 check; no claim about which
    rung any PHYSICAL interface occupies -- the profile clause [P+IJC]
    stands; no boost claim, no geometric-2pi claim):

      rung 0  product              disjoint interfaces (L_loc)
      rung 1  classical corr.      the forced shared cost L_nc [P]
      rung 2  discord-only (cq)    the bridge's minimal output: a
                                   ONE-sided defender -- GENERICALLY
                                   (exception locus Delta = -eps, where
                                   the occupied block is maximally mixed
                                   and the state drops to rung 1:
                                   Hamiltonian noncommutativity does not
                                   imply state discord pointwise). The
                                   bridge guarantee is a FLOOR.
      rung 3  entanglement         two-sided defender + the cost gate
                                   (.340); diagonal gate exactly
                                   x* = 2 ln(1+sqrt(2)) / ln(102).
      rung 4  steering (CJWR-3)    same family deeper in; diagonal gate
                                   x ~ 1.157289 (occupied branch).
                                   CJWR-3 is THE ONE IMPORTED
                                   SUFFICIENT-ONLY INSTRUMENT here
                                   (Cavalcanti-Jones-Wiseman-Reid,
                                   3 settings; correlation terms only,
                                   valid at non-maximally-mixed
                                   marginals); unsteerability below the
                                   gate is NOT certified.
      rung 5  CHSH violation       Horodecki M > 1 (exact iff, any
                                   2-qubit state); diagonal gate
                                   x ~ 1.200805; cross-verified in-check
                                   by direct settings optimization.
      top     Tsirelson            family ceiling 2*sqrt(2)*102/103 --
                                   the sup over the (mu, Delta) quadrant,
                                   both fillings; fractional deficit
                                   1/(d_eff+1) at the native calibration
                                   beta*|eps| = ln d_eff. Strictly inside
                                   the banked T_Tsirelson bound.

    FILLING DISCLOSURE: the rung-3 gate is exactly filling-independent
    (.340); the rung-4/5 gates are NOT -- on the eps > 0 branch the
    family entangles but never crosses CJWR-3 and never violates CHSH
    (the latter exact). Reachability of rungs 4-5 is a one-branch
    statement (occupied-favored, the 06-24 filling).

    Grade P_structural tier 4: exact finite arithmetic; Horodecki-CHSH
    and PPT are exact-iff finite mathematics cross-verified in-check;
    CJWR-3 named above as the imported sufficient-only instrument.
    """
    e = -_LN102  # occupied-favored branch

    # ---- rung 2: cq certificate, generic + the exception locus ----------
    # blocks: rho0 ~ exp(-beta(eps*n + mu|+><+|)), rho1 ~ diag(e^{-b*eps},
    # e^{-b(2eps+Delta)}). rho1 prop. to I  <=>  Delta = -eps.
    def blocks(eps, mu, delta):
        # rho0 via closed-form 2x2 symmetric eigendecomposition
        a = 0.5 * mu          # H0 = [[mu/2, mu/2], [mu/2, eps+mu/2]]
        b = eps + 0.5 * mu
        tr, det = a + b, a * b - 0.25 * mu * mu
        disc = _math.sqrt(max(tr * tr / 4.0 - det, 0.0))
        l1, l2 = tr / 2.0 - disc, tr / 2.0 + disc
        # eigenvector for l1: (mu/2, l1 - a) normalized
        vx, vy = 0.5 * mu, l1 - a
        nrm = _math.hypot(vx, vy) or 1.0
        vx, vy = vx / nrm, vy / nrm
        w1, w2 = _math.exp(-_BETA * l1), _math.exp(-_BETA * l2)
        r0 = [[w1 * vx * vx + w2 * vy * vy, w1 * vx * vy - w2 * vx * vy],
              [w1 * vx * vy - w2 * vx * vy, w1 * vy * vy + w2 * vx * vx]]
        r1 = [[_math.exp(-_BETA * eps), 0.0],
              [0.0, _math.exp(-_BETA * (2.0 * eps + delta))]]
        return r0, r1

    def comm_norm(r0, r1):
        c00 = sum(r0[0][k] * r1[k][0] - r1[0][k] * r0[k][0] for k in (0, 1))
        c01 = sum(r0[0][k] * r1[k][1] - r1[0][k] * r0[k][1] for k in (0, 1))
        c10 = sum(r0[1][k] * r1[k][0] - r1[1][k] * r0[k][0] for k in (0, 1))
        c11 = sum(r0[1][k] * r1[k][1] - r1[1][k] * r0[k][1] for k in (0, 1))
        return max(abs(c00), abs(c01), abs(c10), abs(c11))

    r0, r1 = blocks(e, 0.7 * _LN102, 0.5 * _LN102)
    check(comm_norm(r0, r1) > 1e-6,
          "rung 2: generic one-sided blocks must fail to commute "
          "(defender-side discord positive)")
    r0x, r1x = blocks(e, 0.7 * _LN102, -e)  # the exception locus Delta=-eps
    check(abs(r1x[0][0] - r1x[1][1]) < 1e-12 and comm_norm(r0x, r1x) < 1e-12,
          "rung 2 exception locus Delta = -eps: occupied block maximally "
          "mixed, blocks commute exactly (state drops to rung 1)")

    # ---- rungs 3-5: the three diagonal gates + strict inclusion ---------
    def gate(pred):
        lo, hi = 1e-3, 40.0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if pred(mid):
                hi = mid
            else:
                lo = mid
        return hi

    def ent(x):
        m = 0.5 * (1.0 - _math.exp(-_BETA * x * _LN102))
        return m > _math.exp(-_BETA * x * _LN102 / 2.0)

    g3 = gate(ent)
    g3_closed = 2.0 * _math.log(1.0 + _math.sqrt(2.0)) / _LN102
    check(abs(g3 - g3_closed) < 1e-8,
          f"rung-3 diagonal gate {g3} != 2 ln(1+sqrt2)/ln102 = {g3_closed}")
    g4 = gate(lambda x: _cjwr3(e, x * _LN102, x * _LN102) > 1.0)
    g5 = gate(lambda x: _horodecki_M(e, x * _LN102, x * _LN102) > 1.0)
    check(abs(g4 - 1.157289) < 1e-4, f"rung-4 gate {g4} != 1.157289")
    check(abs(g5 - 1.200805) < 1e-4, f"rung-5 gate {g5} != 1.200805")
    check(g3 < g4 < g5,
          "strict inclusion entanglement < steering < CHSH must hold")

    # ---- the ceiling: sup = 2 sqrt(2) * 102/103, Tsirelson respected ----
    ceil = 2.0 * _math.sqrt(2.0) * 102.0 / 103.0
    worst = 0.0
    for i in range(1, 25):
        for j in range(0, 25):
            mu, dl = 12.0 * i / 24.0 * _LN102 * 4, 12.0 * j / 24.0 * _LN102 * 4
            for ee in (e, -e):
                v = 2.0 * _math.sqrt(_horodecki_M(ee, mu, dl))
                worst = max(worst, v)
                check(v <= ceil + 1e-9,
                      f"CHSH {v} exceeds the family ceiling {ceil}")
    deep = 2.0 * _math.sqrt(_horodecki_M(e, 60.0, 60.0))
    check(abs(deep - ceil) < 1e-6,
          f"deep-limit CHSH {deep} != ceiling {ceil}")
    check(ceil < 2.0 * _math.sqrt(2.0),
          "the family ceiling must sit strictly inside Tsirelson")

    # ---- eps > 0 branch: entangles, never steers (CJWR-3), never CHSH ---
    hit_ent, top_cjwr, top_M = False, 0.0, 0.0
    for i in range(1, 25):
        for j in range(0, 25):
            mu, dl = i / 24.0 * 16.0 * _LN102, j / 24.0 * 16.0 * _LN102
            p00, pp, pm, p11 = _populations(-e, mu, dl)
            if abs(pp - pm) / 2.0 > _math.sqrt(p00 * p11):
                hit_ent = True
            top_cjwr = max(top_cjwr, _cjwr3(-e, mu, dl))
            top_M = max(top_M, _horodecki_M(-e, mu, dl))
    check(hit_ent, "eps > 0 branch must still entangle (rung 3)")
    check(top_cjwr < 1.0 and top_M < 1.0,
          f"eps > 0 branch must cross neither upper gate "
          f"(CJWR {top_cjwr}, M {top_M})")

    # ---- CHSH settings cross-verification at a supra-gate point ---------
    # Diagonal T: CHSH(a,a',b,b') = sum_i c_i (a_i (b_i+b'_i) + a'_i (b_i-b'_i)).
    # Deterministic 2-angle grid in the (1,2) plane -- the plane of the two
    # LARGEST |c| axes here (c1 = c2 > |c3| at this point), which is where
    # the optimum lies for diagonal T; a, a' take their optimal responses
    # |T(b+b')|, |T(b-b')|.
    x = 2.0
    c1, c2, c3 = _corr_diag(e, x * _LN102, x * _LN102)
    target = 2.0 * _math.sqrt(_horodecki_M(e, x * _LN102, x * _LN102))
    best = 0.0
    n = 60
    for ib in range(n):
        tb = _math.pi * ib / n
        for ibp in range(n):
            tbp = _math.pi * ibp / n
            s1, s2 = _math.sin(tb) + _math.sin(tbp), _math.cos(tb) + _math.cos(tbp)
            d1, d2 = _math.sin(tb) - _math.sin(tbp), _math.cos(tb) - _math.cos(tbp)
            val = (_math.hypot(c1 * s1, c2 * s2)
                   + _math.hypot(c1 * d1, c2 * d2))
            best = max(best, val)
    check(best <= target + 1e-9,
          f"settings search {best} must not exceed the Horodecki value "
          f"{target}")
    check(best > target - 1e-3,
          f"settings search {best} must attain the Horodecki value "
          f"{target} (cross-verification)")

    return _result(
        name='T_correlation_hierarchy_ladder — the correlation hierarchy '
             'realized rung by rung in the native two-cell family, with '
             'named gates and the d_eff Bell ceiling',
        tier=4,
        epistemic='P_structural',
        summary=(
            'Rung 0 product (L_loc) / rung 1 classical correlation (the '
            'forced L_nc cost) / rung 2 discord-only cq (the bridge '
            'theorem\'s one-sided FLOOR, generic; exception locus '
            'Delta = -eps pinned, where the state drops to rung 1) / '
            'rung 3 entanglement (two-sided + the .340 gate; diagonal '
            'closed form 2 ln(1+sqrt2)/ln102 = 0.3811) / rung 4 CJWR-3 '
            'steering (1.1573, the one imported sufficient-only '
            'instrument) / rung 5 CHSH (Horodecki exact iff, 1.2008, '
            'cross-verified by settings optimization) — strict '
            'inclusions. Family Bell ceiling 2 sqrt(2) * 102/103 = '
            '2.8010, the sup over the quadrant on both fillings: '
            'fractional deficit 1/(d_eff+1) at the native calibration '
            'beta|eps| = ln d_eff; strictly inside banked T_Tsirelson. '
            'Rung-4/5 reachability is occupied-branch-only (eps > 0 '
            'entangles but crosses neither upper gate — CHSH exact, '
            'unsteerability-by-other-criteria not certified). All '
            'model-level, conditional on the mu*P* placement convention; '
            'no physical-profile claim; no boost/2pi claim.'
        ),
        key_result=(
            'Gates on the occupied diagonal: 0.3811 (= 2 ln(1+sqrt2)/'
            'ln102) < 1.1573 (CJWR-3) < 1.2008 (CHSH), strict. Ceiling '
            '2 sqrt(2) d_eff/(d_eff+1) = 2.8010 < Tsirelson. The bridge '
            'floor is the discord rung, generically; one-sided '
            'entanglement does not exist.'
        ),
        dependencies=['L_nc', 'T_inseparable_IJC',
                      'T_fencea_hinge_coupling_trichotomy'],
        cross_refs=['T_Tsirelson', 'L_loc', 'T_Born_trace_rule'],
    )


def check_T_correlation_ladder_exact_rational_chsh_witness():
    """Exact-rational CHSH witnesses inside the native correlation family.

    The ladder's Gibbs populations are e^{-k ln102} = 102^{-k} -- exact
    rationals -- so native rung points carry exact-rational correlators. Using
    rational Pythagorean (3-4-5) measurement settings in place of the
    Horodecki-optimal (irrational) ones yields an exact-rational CHSH value the
    Boole-polytope engine (feasbool) can consume with NO float in the
    certificate. This is what lets the native family reach the IE CONTEXTUALITY
    axis, whose Sep/IJC decider requires exact rationals.

    Two native members at (eps, mu) = (-ln102, +ln102), differing only in the
    two-cell interaction cost delta, straddle the CHSH boundary -- BOTH
    entangled (the PPT test z^2 > p00*p11 is an exact rational comparison):
      delta = 2 ln102 : c1 = c2 = c3 = -101/105, |S| = 202/75  > 2  -> IJCStr
      delta = 1 ln102 : c1 = c2 = -101/206, c3 = 0, |S| = 707/515 < 2 -> SepStr
    The interaction cost delta alone tunes the family across the Bell boundary
    while both states remain entangled -- the entanglement < CHSH strict gap of
    the ladder, in exact arithmetic. The IJC value sits below the family ceiling
    2 sqrt2 * 102/103 (exact |S|^2 = 40804/5625 < 83232/10609). The construction
    cross-checks against the module's own float family functions (_corr_diag,
    _ppt_margin).

    Grade P_structural tier 4: exact Fraction arithmetic + the exact
    Boole-polytope LP; floats appear only as an independent cross-check.
    """
    from fractions import Fraction as F
    from apf.ijc_feasbool_engine import _chsh_correlator_scenario, feasbool

    def rpops(a, b, c):
        # energies (0, a+b, a, 2a+c) in units of ln102; weight = 102^{-(E-min)}
        Es = (F(0), F(a + b), F(a), F(2 * a + c))
        m = min(Es)
        w = [F(102) ** int(-(e - m)) for e in Es]
        Z = sum(w)
        return [x / Z for x in w]

    def rcorr(a, b, c):
        p00, pp, pm, p11 = rpops(a, b, c)
        return pp - pm, pp - pm, p00 + p11 - pp - pm

    def e_table(a, b, c):
        # settings a=(1,0,0), a'=(0,1,0), b=(3/5,4/5,0), b'=(3/5,-4/5,0);
        # E(u,v) = c1 ux vx + c2 uy vy + c3 uz vz for T = diag(c1,c2,c3).
        c1, c2, _c3 = rcorr(a, b, c)
        return [c1 * F(3, 5), c1 * F(3, 5), c2 * F(4, 5), c2 * F(-4, 5)]

    def entangled_exact(a, b, c):
        p00, pp, pm, p11 = rpops(a, b, c)
        z = (pp - pm) / 2
        # PT min-eigenvalue < 0  <=>  z^2 > p00*p11: an EXACT rational
        # comparison (the sqrt in the margin never needs to be taken).
        return z * z > p00 * p11

    ceil_sq = F(8) * F(102, 103) ** 2  # (2 sqrt2 * 102/103)^2, the family ceiling

    # ---- IJC witness: delta = 2 ln102 -----------------------------------
    a, b, c = -1, 1, 2
    check(rpops(a, b, c) == [F(1, 105), F(1, 105), F(102, 105), F(1, 105)],
          "IJC witness populations exact: (1/105, 1/105, 102/105, 1/105)")
    c1, c2, c3 = rcorr(a, b, c)
    check(c1 == c2 == F(-101, 105) and c3 == F(-101, 105),
          "IJC witness correlators c1 = c2 = c3 = -101/105")
    check(entangled_exact(a, b, c), "IJC witness is entangled (exact PPT margin)")
    e_ijc = e_table(a, b, c)
    s_ijc = e_ijc[0] + e_ijc[1] + e_ijc[2] - e_ijc[3]
    check(abs(s_ijc) == F(202, 75),
          "IJC witness CHSH |S| = 202/75, exact (3-4-5 rational settings)")
    check(abs(s_ijc) > 2, "IJC witness violates CHSH: |S| > 2")
    check(abs(s_ijc) ** 2 < ceil_sq,
          "IJC witness below the family ceiling 2 sqrt2 * 102/103 "
          "(exact |S|^2 = 40804/5625 < 83232/10609)")
    check(feasbool(_chsh_correlator_scenario(tuple(e_ijc)))["branch"] == "IJCStr",
          "IJC witness: the Boole-polytope engine returns IJCStr (named Bell obstruction)")

    # ---- SepStr control: delta = 1 ln102 (entangled but Bell-local) -----
    a2, b2, c2p = -1, 1, 1
    check(rpops(a2, b2, c2p) == [F(1, 206), F(1, 206), F(51, 103), F(51, 103)],
          "Sep witness populations exact: (1/206, 1/206, 51/103, 51/103)")
    d1, d2, d3 = rcorr(a2, b2, c2p)
    check(d1 == d2 == F(-101, 206) and d3 == 0,
          "Sep witness correlators c1 = c2 = -101/206, c3 = 0")
    check(entangled_exact(a2, b2, c2p),
          "Sep witness is ENTANGLED (exact PPT margin) -- the entanglement < CHSH gap")
    e_sep = e_table(a2, b2, c2p)
    s_sep = e_sep[0] + e_sep[1] + e_sep[2] - e_sep[3]
    check(abs(s_sep) == F(707, 515), "Sep witness CHSH |S| = 707/515, exact")
    check(abs(s_sep) < 2, "Sep witness does NOT violate CHSH: |S| < 2 (Bell-local)")
    check(feasbool(_chsh_correlator_scenario(tuple(e_sep)))["branch"] == "SepStr",
          "Sep witness: the Boole-polytope engine EXPORTS a global section (SepStr)")

    # ---- delta tunes the family across the boundary at fixed (eps, mu) --
    check((a, b) == (a2, b2) and c != c2p,
          "both witnesses share (eps, mu) = (-ln102, +ln102); only delta differs "
          "(2 ln102 vs ln102) -- the interaction cost alone tunes the entangled "
          "family across the CHSH boundary")

    # ---- cross-check the exact construction vs the module's float family
    for (aa, bb, cc), rc1, rc3 in (((-1, 1, 2), c1, c3), ((-1, 1, 1), d1, d3)):
        eps, mu, delta = aa * _LN102, bb * _LN102, cc * _LN102
        fc1, fc2, fc3 = _corr_diag(eps, mu, delta)
        check(abs(float(rc1) - fc1) < 1e-12 and abs(float(rc3) - fc3) < 1e-12,
              "exact-rational correlators reproduce the module's float _corr_diag")
        check((_ppt_margin(eps, mu, delta) > 0) == entangled_exact(aa, bb, cc),
              "exact PPT entanglement verdict matches the module's float _ppt_margin")

    return _result(
        name='T_correlation_ladder_exact_rational_chsh_witness - exact-rational '
             'CHSH witnesses inside the native correlation family, straddling '
             'the Bell boundary, feasbool-certified for the IE CONTEXTUALITY axis',
        tier=4,
        epistemic='P_structural',
        summary=(
            'The native two-cell Gibbs family has populations 102^{-k} (exact '
            'rational at the ln102 rungs), so its correlators are exact '
            'rationals; rational Pythagorean (3-4-5) measurement settings give '
            'an exact-rational CHSH the Boole-polytope engine consumes with no '
            'float. Two entangled members at (eps, mu) = (-ln102, +ln102) '
            'differing only in the interaction cost delta straddle the CHSH '
            'boundary: delta = 2 ln102 gives |S| = 202/75 > 2 (IJCStr, below the '
            '2 sqrt2 * 102/103 ceiling), delta = ln102 gives |S| = 707/515 < 2 '
            '(SepStr) -- the entanglement < CHSH gap, exact. Both branches '
            'certified by feasbool; correlators and PPT verdicts cross-checked '
            'against the module float family functions.'
        ),
        key_result=(
            'Native exact-rational CHSH witnesses: IJCStr at |S| = 202/75 (delta '
            '= 2 ln102) and SepStr at |S| = 707/515 (delta = ln102), both '
            'entangled (p00 = p11, exact PPT), tuned by delta alone. Puts the '
            'native family on the IE CONTEXTUALITY axis without any float.'
        ),
        dependencies=['T_correlation_hierarchy_ladder', 'T_inseparable_IJC'],
        cross_refs=['T_Tsirelson', 'L_loc'],
    )


def check_T_ladder_ceiling_calibration_from_saturation():
    """The ladder Bell-ceiling calibration eps = ln(d_eff) IS the banked
    per-type saturation cost -- so the sub-Tsirelson ceiling reads off framework
    quantities, not a tuned constant.

    The correlation-hierarchy ladder fixes its Bell ceiling
    2 sqrt2 * d_eff/(d_eff+1) at the calibration beta*|eps| = ln 102. Prior to
    this check that 102 was an inserted constant. Here it is identified with
    quantities that are already [P]:
      - d_eff = (C_total - 1) + C_vacuum = 60 + 42 = 102, the interface-stratum
        dimension / per-type microstate count at saturation
        (check_T_interface_sector_bridge, check_L_self_exclusion + T11 [P]);
      - sigma = S_dS / C_total = ln(d_eff), the intensive entropy per capacity
        type at saturation (check_L_sigma_intensive [P], from
        check_T_deSitter_entropy S_dS = C_total ln(d_eff) = 61 ln102 = 282.1
        nats, the observed de Sitter entropy).
    With beta = 1 the calibration is EXACTLY e^{-beta*eps} = e^{-sigma} =
    1/d_eff: exciting one FENCE-A cell costs one distinction against the
    saturated maximally-mixed background rho = I/d_eff (check_L_KMS_trace_state).
    So beta*eps = sigma = ln(d_eff), and the ceiling 2 sqrt2 * 102/103
    (fractional deficit 1/(d_eff+1) = 1/103 -- the finite-d_eff sub-Tsirelson
    gap) is a framework value.

    NAMED READING (load-bearing, honestly graded P_structural_reading): this
    reads the two-cell FENCE-A model's per-cell excitation cost eps as the
    per-type saturation cost sigma -- the two cells as capacity types at the
    SATURATED interface. The two-cell model does NOT internally force saturation
    (its own 4-dim max-entropy state is rho = I/4, eps -> 0); the ln(d_eff)
    scale is inherited from the ambient saturated interface via
    L_sigma_intensive. The calibration is forced GIVEN the saturation reading,
    not unconditionally. FALSIFIER: a physical shared-causal interface carrying
    the correlation family that is NOT at saturation (per-type cost != ln d_eff),
    or a FENCE-A cell that is not one capacity type, breaks the identification
    and the 2 sqrt2 * 102/103 value does not follow.
    """
    import math as _m
    from apf.apf_utils import dag_get

    C_total = dag_get('C_total', default=61,
                      consumer='T_ladder_ceiling_calibration_from_saturation')
    C_vacuum = 42  # T11 [P]
    d_eff = (C_total - 1) + C_vacuum
    check(d_eff == 102,
          "d_eff = (C_total-1)+C_vacuum = %d+%d = %d" % (C_total - 1, C_vacuum, d_eff))

    # sigma = ln(d_eff): the per-type saturation cost [L_sigma_intensive, P]
    sigma = _m.log(d_eff)
    S_dS = C_total * sigma
    check(abs(S_dS - 282.12) < 0.02,
          "S_dS = C_total ln(d_eff) = 61 ln102 = %.3f nats reproduces the "
          "observed dS entropy ~282.1 [T_deSitter_entropy]" % S_dS)

    # the ladder calibration eps IS sigma (beta = 1)
    eps = _LN102
    check(abs(_BETA * eps - sigma) < 1e-15,
          "beta*eps = sigma = ln(d_eff): the ladder calibration is the banked "
          "per-type saturation cost, not an inserted constant")
    check(abs(_m.exp(-_BETA * eps) - 1.0 / d_eff) < 1e-15,
          "e^{-beta*eps} = 1/d_eff: one distinction against the saturated "
          "rho = I/d_eff background [L_KMS_trace_state]")

    # the Bell ceiling reads off framework quantities
    ceiling = 2.0 * _m.sqrt(2.0) * d_eff / (d_eff + 1)
    check(abs(1.0 / (d_eff + 1) - 1.0 / 103) < 1e-15,
          "fractional deficit 1/(d_eff+1) = 1/103")
    # cross-check against the ladder's own deep-limit CHSH (occupied -eps branch)
    ladder_ceiling = 2.0 * _m.sqrt(_horodecki_M(-_LN102, 60.0, 60.0))
    check(abs(ceiling - ladder_ceiling) < 1e-6,
          "framework ceiling 2 sqrt2 * d_eff/(d_eff+1) = %.4f matches the ladder "
          "deep-limit CHSH %.4f" % (ceiling, ladder_ceiling))
    check(ceiling < 2.0 * _m.sqrt(2.0),
          "strictly inside Tsirelson 2 sqrt2: the sub-Tsirelson gap is exactly "
          "the finite-d_eff deficit 2 sqrt2 / (d_eff+1)")

    return _result(
        name='T_ladder_ceiling_calibration_from_saturation - the ladder Bell-'
             'ceiling calibration eps = ln(d_eff) identified with the banked '
             'per-type saturation cost sigma = S_dS/C_total, so 2 sqrt2 * 102/103 '
             'reads off framework quantities (named saturation reading)',
        tier=4,
        epistemic='P_structural_reading',
        summary=(
            'The correlation-hierarchy ladder ceiling 2 sqrt2 * d_eff/(d_eff+1) '
            'sat at an inserted calibration beta*|eps| = ln 102. This check '
            'identifies that calibration with the banked per-type saturation '
            'cost: sigma = S_dS/C_total = ln(d_eff) [L_sigma_intensive, P], with '
            'd_eff = (C_total-1)+C_vacuum = 60+42 = 102 the interface-stratum '
            'dimension [T_interface_sector_bridge, P] and S_dS = 61 ln102 = 282.1 '
            'nats the observed de Sitter entropy [T_deSitter_entropy, P]. With '
            'beta = 1 the calibration is exactly e^{-eps} = 1/d_eff -- one '
            'distinction against the saturated rho = I/d_eff background -- so '
            'beta*eps = sigma = ln(d_eff) is the interface saturation cost, and '
            'the sub-Tsirelson ceiling (deficit 1/(d_eff+1) = 1/103) is a '
            'framework value rather than a tuned one. Graded P_structural_reading '
            'over the named reading that the two FENCE-A cells are capacity types '
            'at the saturated interface (the two-cell model does not internally '
            'force saturation; the scale is inherited via L_sigma_intensive).'
        ),
        key_result=(
            'beta*eps = sigma = ln(d_eff) = ln 102 (exact): the ladder Bell '
            'ceiling 2 sqrt2 * 102/103 = 2.8010 < Tsirelson is read off the '
            'framework d_eff = 60+42 and the banked per-type saturation cost, '
            'not a free calibration. Sub-Tsirelson gap = the finite-d_eff '
            'deficit 2 sqrt2/(d_eff+1). Named saturation reading; falsifier: a '
            'non-saturated carrying interface, or cell != type.'
        ),
        dependencies=['L_sigma_intensive', 'T_deSitter_entropy',
                      'T_correlation_hierarchy_ladder'],
        cross_refs=['T_interface_sector_bridge', 'L_self_exclusion',
                    'L_KMS_trace_state', 'T_Tsirelson',
                    'T_correlation_ladder_exact_rational_chsh_witness'],
    )


_CHECKS = {
    'T_fencea_hinge_coupling_trichotomy':
        check_T_fencea_hinge_coupling_trichotomy,
    'T_correlation_hierarchy_ladder':
        check_T_correlation_hierarchy_ladder,
    'T_correlation_ladder_exact_rational_chsh_witness':
        check_T_correlation_ladder_exact_rational_chsh_witness,
    'T_ladder_ceiling_calibration_from_saturation':
        check_T_ladder_ceiling_calibration_from_saturation,
}


def register(registry):
    """Register the FENCE-A hinge trichotomy check into the bank."""
    registry.update(_CHECKS)


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == '__main__':
    for _n, _r in run_all().items():
        print(('PASS' if _r.get('passed', True) else 'FAIL'), _n)


# ---------------------------------------------------------------------------
# IE onboarding (Wave 6, v24.3.346). This landing also adds the module's
# missing MODULE_TYPES entry ('extension') in apf/_module_manifest.py.
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "foundation:fencea_hinge_trichotomy_ladder",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "The FENCE-A cost-to-state hinge is a TRICHOTOMY, exact on the "
            "two-cell Gibbs model at |beta*eps| = ln 102 "
            "(check_T_fencea_hinge_coupling_trichotomy): (B) diagonal "
            "density-density cost -> separable; (b) one-sided non-commuting "
            "joint defender -> exactly classical-quantum, separable at EVERY "
            "parameter value (so the T_inseparable_IJC bridge conclusion is "
            "INSUFFICIENT for cross-cut entanglement -- a candidate forcing "
            "route refuted, not a banked claim); (c) two-sided Bell-projector "
            "defender -> entangling above a closed-form, epsilon-independent "
            "threshold. Plus the correlation-hierarchy ladder "
            "(check_T_correlation_hierarchy_ladder): rungs 0-5 realized "
            "inside the native family, model-level, conditional on the "
            "mu*P* Gibbs-placement convention; no claim about which rung any "
            "PHYSICAL interface occupies; no boost claim, no geometric-2pi "
            "claim. "
        ),
        "note": "Wave 6; the .340/.341 landings; profile clause [P+IJC] stands untouched",
    },
    {
        "input_id": "contextuality:native_ladder_chsh_violation",
        "expect_export": False,
        "axis": "CONTEXTUALITY",
        "payload": {"contextuality_kind": "chsh_correlators",
                    "E": ["-101/175", "-101/175", "-404/525", "404/525"]},
        "note": "the exact-rational native-family CHSH violation |S| = 202/75 > 2 "
                "(entangled state at eps,mu,delta = -ln102,ln102,2ln102; 3-4-5 "
                "settings) -> IJCStr; check_T_correlation_ladder_exact_rational_chsh_witness",
    },
    {
        "input_id": "contextuality:native_ladder_bell_local",
        "expect_export": True,
        "axis": "CONTEXTUALITY",
        "payload": {"contextuality_kind": "chsh_correlators",
                    "E": ["-303/1030", "-303/1030", "-202/515", "202/515"]},
        "note": "the exact-rational native-family ENTANGLED-but-Bell-local state |S| = "
                "707/515 < 2 (delta = ln102) -> SepStr, a global section exported; the "
                "entanglement < CHSH gap; check_T_correlation_ladder_exact_rational_chsh_witness",
    },
)
