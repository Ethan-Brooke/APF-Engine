"""G2 trivial-center exhibit: the no-kinematic-N-ality-obstruction
corollary (Leg A, vacuity billed as vacuity) and the G2 fusion/screen
instance (Legs B + C) on the banked center-flux lattice model, with the
G2 fusion rules CONSTRUCTED TWICE independently in-module and
cross-checked exactly.

check_L_trivial_center_no_nality_obstruction (Leg A).  THE STATEMENT:
for G2 (compact simple, trivial center), the N-ality receiving group
Z(G)-hat = P/Q is the TRIVIAL group -- |P/Q| = det(Cartan) = 1, both
fundamental weights are integer combinations of simple roots, and every
weight of every battery irrep lies in the root lattice (each computed;
the 267 per-weight memberships aggregated into one summary check per
audit fix F6 -- the computations all still run).  Hence the N-ality
charge map q is IDENTICALLY ZERO, H-hom is VACUOUSLY TRUE (0 = 0 + 0
over 400+ computed constituents -- this leg certifies SHAPE, not
substance, and is billed as vacuity in its own check messages), and the
flux-exit trigger "enclosed source charge != 0" is UNSATISFIABLE: there
is NO KINEMATIC N-ality obstruction to screening for any G2 irrep --
NEVER "everything screens".  SECOND, FUSION-INTRINSIC GROUND: 7 in
7 (x) 7 (multiplicity 1) forces q(7) = 0 for ANY fusion homomorphism
into ANY abelian group (cancellation); the 7 generates the battery
under fusion, so THE G2 FUSION RING ITSELF ADMITS NO NONTRIVIAL
N-ALITY-STYLE GRADING -- the vacuity is earned twice, once from the
lattice index and once from fusion alone (fake mod-2 and mod-3 gradings
are refuted by the computed fusion: the battery is live, not theater).
TREE-GEOMETRY CONTROL (in-battery): on the walked loopless path the
single 7 source admits NO bounded screen at the stated cap -- the
admissible set is EXACTLY the growing all-7 string, support >= L across
the nested pairwise-disjoint cut family, despite q == 0.  Screen
existence stays geometry-conditional; this leg licenses NO existence
claim of any screen.

check_T_g2_fusion_screen_exhibit (Legs B + C).  THE INSTANCE: the G2
fusion rules constructed by two independent routes -- Route 1
Freudenthal weight multiplicities (exact integer recursion, positivity
and divisibility asserted at every step) + Racah-Speiser/Klimyk signed
dominant-chamber reflection; Route 2 exact Weyl characters as integer
Laurent polynomials (12-term alternants, exact division A_{lam+rho} /
A_rho) with greedy leading-term subtraction of FULL characters -- and
cross-checked EXACTLY on all 81 ordered pairs of the 9-irrep battery
{1, 7, 14, 27, 64, 77, 77', 182, 189}, with dimension multiplicativity,
commutativity, zero construction-flag trips, route-2 greedy soundness
MACHINE-CHECKED for every character route 2 ever uses (audit fix F1),
and the Casimir trace-identity blade with its dimension-preserving-
sabotage control (audit fix F4: the sabotage passes dimension counting
and is caught by the Casimir identity).  Table pins: 7 (x) 7 = 1 + 7 +
14 + 27 (the charter's load-bearing channel); 7 (x) 14 = 7 + 27 + 64
(no trivial); 14 (x) 14 = 1 + 14 + 27 + 77 + 77' (no 7); 1 in
7 (x) 7 (x) 7 with multiplicity EXACTLY 1; 7 in 14 (x) 14 (x) 14 with
multiplicity EXACTLY 1; Schur delta_ab over the whole battery (every G2
irrep self-dual: -1 is in the Weyl group, computed); the 7 generates
the battery.  GRAPH LEGS at cap {1, 7, 14, 27} on the walked graphs:
TT(1..3), source 7 -- the 7-triangle screen (label 7 on the 3 cycle
edges, trivial tail) admissible at every interior vertex, support
exactly 3, crossing NO cut of the nested family, located inside the
exhaustive admissible set (12 configurations at each L, constant);
claw2/claw3 with 7 sources FULLY CONTAINABLE (4/4 configurations,
contained witnesses located) -- the banked SU(3) claw2 fact (pairs
provably cannot, triality 2) does NOT transfer: exactly the
trivial-center corollary on a walked instance; claw1 not contained
THERE (a geometry + cap fact, not an N-ality obstruction); K4+tail
(1..3) -- the single 7 source fully contained by the ALL-ADJOINT
(all-14) screen on the 6 K4 edges, support 6 constant in L, 3306
admissible / 794 fully contained configurations at each L (exhaustive).
Every screen statement is EXISTENCE-ONLY and conditional on the walked
geometry at the stated cap; every vertex-content fold used by any graph
leg is double-computed on both routes and asserted equal as a full
decomposition.

CONVENTIONS (pinned; composing with apf/center_flux_exit.py):
  * Cartan matrix A[i][j] = 2(alpha_i, alpha_j)/(alpha_j, alpha_j),
    Bourbaki node order: alpha_1 SHORT (norm^2 = 2), alpha_2 LONG
    (norm^2 = 6), (alpha_1, alpha_2) = -3.  This gives
    A = [[2, -1], [-3, 2]] -- the charter's matrix, NOT its transpose.
    Under this convention (1,0) = the 7 (fundamental; highest weight =
    highest short root = omega_1) and (0,1) = the 14 (adjoint; omega_2
    = highest root); the transposed convention swaps the labels
    (computed as a negative control in-battery).
  * Weights in fundamental-weight coordinates (m1, m2) = m1 omega_1 +
    m2 omega_2; alpha_1 = (2, -1), alpha_2 = (-3, 2) (rows of A);
    pairing (u, v) = u^T F v with F = [[2, 3], [3, 6]] (rederived and
    asserted against the alpha-Gram matrix [[2, -3], [-3, 6]]);
    rho = (1, 1).  Root system DERIVED, not assumed: 12 roots by
    Weyl-orbit closure, 6 positive (3 short + 3 long); Weyl group order
    12 by matrix closure, 6 even + 6 odd, pairing-preserving, -1 in W.
  * GRAPH MODEL: verbatim the banked center-flux conventions (oriented
    edges (tail, head); label r seen as r at HEAD, conj(r) at TAIL;
    interior per-vertex-singlet admissibility, a MODEL DEFINITION whose
    Gauss reading is a named identification computed nowhere; boundary
    unconstrained; sources un-conjugated).  For G2 conj(r) = r (every
    irrep self-dual, computed), collapsing the orientation exactly as
    SU(2) self-conjugacy did in the banked module.

ROUTE INDEPENDENCE: the two routes share ONLY the declared lattice
constants (A, F, rho, the two simple reflections, and the order-12
matrix group generated by them -- itself verified by closure,
determinant, and pairing-invariance checks before use); weight
multiplicities and decompositions are computed by disjoint code paths.
The routes agreed on every battery pair and every graph-leg fold on the
lane's first complete run; no disagreement ever occurred.

PREMISE STACK (the granted grade lines' conditioning bars):
  1. Lattice-model conventions (MODEL DEFINITION, named): the banked
     oriented electric-basis graph model with per-vertex-singlet
     admissibility; the Gauss / interior-gauge-invariance reading is a
     named identification, computed nowhere (verbatim the flux-exit
     module's premise 2).  Consumed as the PATTERN; the banked lemma's
     own premise stack travels wherever its content is cited.
  2. The pinned G2 conventions (above): Cartan matrix + node order +
     weight coordinates.  Convention, not hypothesis; the transposed
     alternative is computed as a control.
  3. Cap/grid scoping: all fusion facts on the stated 9-irrep battery;
     all graph facts at cap {1, 7, 14, 27} on the walked graphs
     (path 1-4, TT 1-3, claw 1-3, K4+tail 1-3).  Nothing beyond.
  4. NO H-hom needed for the G2 statement itself -- that is the point
     of the vacuity leg (the charge group is trivial).  Where the
     banked Z_N machinery is referred to, its H-hom conditioning is
     named and travels.
  5. A1 deliberately NOT consumed: pure model mathematics -- the same
     dependency argument as the banked flux-exit module (the house
     precedent); no APF axiom is consumed in any computation.

DEPENDENCY CHOICE (per audit fix F3): dependencies list ONLY
L_center_flux_exit -- the banked pattern and model conventions,
consumed LIVE as anchor.  The distilled battery does NOT run
T_center_order_parameter_triality live: the [P_math]-headline module
stays free of a saturation-conditioned [P] physics dependency it
explicitly does not consume (house precedent: center_flux_exit itself
keeps it as cross_ref only).  The lane walker's live anchor run of it
stays as lane record.  cross_refs: T_center_order_parameter_triality
(the SU(3) N-ality grading whose trivial-center corollary this module
states), T_frustration_center_partition (screen-supporting condition
vocabulary), R_SU_Nc_neq_3_killed (the not-a-gauge-group fence's home).

KILL MODES (LOUD):
  - ROUTE DISAGREEMENT: any disagreement between the two constructed
    routes on any battery pair or any graph-leg fold (asserted 0
    below); a construction-flag trip (_FLAG_R1 negative Klimyk
    multiplicity / _FLAG_R2 non-dominant or non-positive greedy leading
    term, both asserted 0); a dimension-multiplicativity or
    Casimir-trace failure.
  - NO BOUNDED SCREEN AT CAP: the 7-triangle screen or the all-14 K4
    screen failing per-vertex admissibility on recomputation, absent
    from the exhaustive admissible set, or count-nonconstant in L;
    1 not in 7 (x) 7 under either route kills the channel and Leg C.
  - Leg A: an integer weight of any G2 irrep NOT in the root lattice;
    det(Cartan) != 1 under the pinned convention; any nontrivial
    abelian grading of the computed fusion ring (a fusion table with
    7 not in 7 (x) 7 would reopen it -- both routes would have to be
    wrong together).
  - GRADED-FD5-CLASS VOCABULARY: a fence-stem hit in any check message
    OR function name (the fence scans BOTH per audit fix F2; the
    audited leak class -- a fence-violating leg NAME self-certifying
    clean around a message-only scan -- can no longer occur).
  - Inherited: the banked flux-exit module's kill conditions travel
    with its consumed anchor (its H-hom blade does not touch the G2
    statement -- trivial charge group -- but kills the pattern parent
    if it ever fires).

MAY-NOT-CITE (from the lane note; citation without the premise stack is
misciting):
  - NOT a gauge-group claim: G2 is a MATHEMATICAL exhibit for the
    trivial-center structure of the N-ality obstruction;
    R_SU_Nc_neq_3_killed STANDS untouched; nothing here proposes G2 as
    a color group or reopens the N_c = 3 derivation.
  - The vacuity leg licenses NO screen existence.  "No kinematic
    N-ality obstruction" is NEVER "everything screens"; screen
    existence is geometry-conditional everywhere (the walked tree
    control is in-battery).
  - Screens are EXISTENCE statements at stated caps on walked graphs;
    never cite as selected/taken; the billing/argmin content is the
    frustration module's, deliberately not consumed here.
  - Nothing beyond the walked graphs and stated caps; no graph-class
    characterization; the K4+tail and claw counts (3306/794/12/4) are
    instance facts.
  - NO DYNAMICS: no saturation claim, no string content, no gap value,
    no tension law, no continuum claim, no fixed-L statement, no
    reading sentence (door-state unchanged).
  - The G2 INTERMEDIATE STRING IS UNTOUCHABLE: the three-adjoint
    channel (7 in 14 (x) 14 (x) 14) and the K4 containment are
    KINEMATIC ADMISSIBILITY EXHIBITS, never a statement that G2
    "breaks strings" dynamically.
  - The banked flux-exit lemma's own MAY-NOT-CITE lines travel wherever
    its pattern or content is invoked (delta(S)-scoping; H-hom named
    beyond its computed grids; no SU(N > 3)).

GRADES: check_L_trivial_center_no_nality_obstruction [P_math |
lattice-model conventions + pinned G2 conventions], vacuity billed
in-sentence.  check_T_g2_fusion_screen_exhibit [P] instance-scoped at
stated caps and walked graphs.  Tier 4.  Verbatim from the lane's
certified bank entry (WALK_NOTE.md section 7, amended per audit fix F3).

AUDIT RECORD, cited not imported: the lane's hostile audit
(AUDIT_REPORT.md, 2026-07-11, LAND-WITH-FIXES 0.88) is the
ROUTE-INDEPENDENCE CERTIFICATE for the constructed G2 rules -- a
foreign-basis THIRD route (3D sum-zero realization sharing no basis, no
constants, no ordering functional; audit_probe_g2_independent.py, 275
checks, exit 0) plus a mod-p alternant FOURTH route plus the Casimir
trace-identity blade agreed with both in-lane routes on all 81 pairs
and every graph count (12/4/4/3306/794); mutation hardness 5/5 --
mirroring the SU(3) stage-1 audit precedent in center_flux_exit.
Fixes F1-F6 carried in the walker of record.

Lane record: The Turning (parked)/g2_exhibit_2026-07-11/
(walk_g2_exhibit.py [590 checks, exit 0; fixes F1-F6 carried],
WALK_NOTE.md [section 7 = the certified bank entry], AUDIT_REPORT.md
LAND-WITH-FIXES 0.88).  This module banks the DISTILLED battery; the
walker is the lane record.

v24.3.418 (2026-07-11), banked at the principal's ruling 2026-07-11.
"""

from itertools import combinations
import ast

# ---------------------------------------------------------------------------
# shared lattice constants (the ONLY code shared by the two routes;
# verified structurally in-battery before either route's output is used)
# ---------------------------------------------------------------------------
A_CARTAN = ((2, -1), (-3, 2))          # A[i][j] = 2(a_i,a_j)/(a_j,a_j)
ALPHA = ((2, -1), (-3, 2))             # simple roots in omega-coords
F_PAIR = ((2, 3), (3, 6))              # (omega_i, omega_j)
RHO = (1, 1)
UNIT = (0, 0)
SEVEN, FOURTEEN, TWENTY7 = (1, 0), (0, 1), (2, 0)


def _ip(u, v):
    """Exact pairing (u, v) = u^T F v on omega-coordinates."""
    return (2 * u[0] * v[0] + 3 * (u[0] * v[1] + u[1] * v[0])
            + 6 * u[1] * v[1])


def _mat_apply(w, m):
    return (w[0][0] * m[0] + w[0][1] * m[1],
            w[1][0] * m[0] + w[1][1] * m[1])


def _mat_mul(w, u):
    return ((w[0][0] * u[0][0] + w[0][1] * u[1][0],
             w[0][0] * u[0][1] + w[0][1] * u[1][1]),
            (w[1][0] * u[0][0] + w[1][1] * u[1][0],
             w[1][0] * u[0][1] + w[1][1] * u[1][1]))


_S1M = ((-1, 0), (1, 1))
_S2M = ((1, 3), (0, -1))
_IDM = ((1, 0), (0, 1))

# closure of {s1, s2} under multiplication (the Weyl group, derived)
W12 = {_IDM}
_frontier = [_IDM]
while _frontier:
    _nxt = []
    for _w in _frontier:
        for _g in (_S1M, _S2M):
            _wg = _mat_mul(_w, _g)
            if _wg not in W12:
                W12.add(_wg)
                _nxt.append(_wg)
    _frontier = _nxt
W12 = sorted(W12)
DET = {w: w[0][0] * w[1][1] - w[0][1] * w[1][0] for w in W12}

# root system: W-orbit closure from the simple roots
_ALLROOTS = set()
for _al in ALPHA:
    for _w in W12:
        _ALLROOTS.add(_mat_apply(_w, _al))


def _alpha_coords(mu):
    """mu = c1*alpha_1 + c2*alpha_2; always integer coordinates because
    the inverse transform is integral (det A = 1 -- Leg A)."""
    return (2 * mu[0] + 3 * mu[1], mu[0] + 2 * mu[1])


POS = sorted([r for r in _ALLROOTS
              if r != (0, 0)
              and _alpha_coords(r)[0] >= 0 and _alpha_coords(r)[1] >= 0],
             key=lambda r: _alpha_coords(r))


def _ordk(m):
    """Total order: primary f(mu) = (mu, rho), ties by m1 then m2."""
    return (_ip(m, RHO), m[0], m[1])


def _weyl_dim(lam):
    num = 1
    den = 1
    lr = (lam[0] + 1, lam[1] + 1)
    for al in POS:
        num *= _ip(lr, al)
        den *= _ip(RHO, al)
    assert num % den == 0, "Weyl dimension formula not exactly divisible"
    return num // den


def _sextic_dim(lam):
    """The G2 closed-form dimension (independent pin of _weyl_dim)."""
    m1, m2 = lam
    prod = ((m1 + 1) * (m2 + 1) * (m1 + m2 + 2) * (m1 + 2 * m2 + 3)
            * (m1 + 3 * m2 + 4) * (2 * m1 + 3 * m2 + 5))
    assert prod % 120 == 0
    return prod // 120


def _casimir(lam):
    """Quadratic Casimir C2(lam) = (lam, lam + 2 rho) in the pinned
    pairing (exact integer; the audit-fix-F4 blade's input)."""
    return _ip(lam, lam) + 2 * _ip(lam, RHO)


def _conj(r):
    """G2 conjugation: -w0 = identity (w0 = -1 is in W12, asserted
    in-battery); every G2 irrep self-dual."""
    return r


# ---------------------------------------------------------------------------
# ROUTE 1: Freudenthal weight multiplicities + Racah-Speiser/Klimyk
# ---------------------------------------------------------------------------
_R1W = {}
_R1F = {}
_FLAG_R1 = [0]     # trips on a negative Klimyk multiplicity (kill mode)


def _dom(t):
    """Dominant representative of the W-orbit of t (no sign)."""
    x, y = t
    while x < 0 or y < 0:
        if x < 0:
            x, y = -x, x + y
        else:
            x, y = x + 3 * y, -y
    return (x, y)


def _r1_weights(lam):
    """Full weight system {weight: multiplicity} of V(lam) by
    Freudenthal's recursion in exact integers (positivity of the
    denominator and exact divisibility asserted at every step),
    extended from the dominant table by the order-12 Weyl orbit."""
    if lam in _R1W:
        return _R1W[lam]
    l1, l2 = lam
    cands = set()
    for k1 in range(0, 2 * l1 + 3 * l2 + 1):
        for k2 in range(0, l1 + 2 * l2 + 1):
            mu = (l1 - 2 * k1 + 3 * k2, l2 + k1 - 2 * k2)
            if mu[0] >= 0 and mu[1] >= 0:
                cands.add(mu)
    dom_mult = {lam: 1}
    lr = (l1 + 1, l2 + 1)
    nlr = _ip(lr, lr)
    for mu in sorted(cands, key=lambda m: -_ip(m, RHO)):
        if mu == lam:
            continue
        K1, K2 = _alpha_coords((l1 - mu[0], l2 - mu[1]))
        num = 0
        for al in POS:
            p, q = _alpha_coords(al)
            k = 1
            while K1 - k * p >= 0 and K2 - k * q >= 0:
                nu = (mu[0] + k * al[0], mu[1] + k * al[1])
                m_nu = dom_mult.get(_dom(nu), 0)
                if m_nu:
                    num += m_nu * _ip(nu, al)
                k += 1
        mr = (mu[0] + 1, mu[1] + 1)
        den = nlr - _ip(mr, mr)
        assert den > 0, "Freudenthal denominator not positive"
        num *= 2
        assert num % den == 0, "Freudenthal numerator not divisible"
        m = num // den
        assert m >= 0, "Freudenthal produced a negative multiplicity"
        if m:
            dom_mult[mu] = m
    full = {}
    for mu, m in dom_mult.items():
        for w in W12:
            full[_mat_apply(w, mu)] = m
    _R1W[lam] = full
    return full


def _r1_fuse(a, b):
    """Racah-Speiser / Klimyk: lambda (x) V(mu) from the full weight
    system of the SECOND factor, signed reflection into the dominant
    chamber, wall terms discarded."""
    key = (a, b)
    if key in _R1F:
        return _R1F[key]
    out = {}
    for nu, m in _r1_weights(b).items():
        x, y = a[0] + 1 + nu[0], a[1] + 1 + nu[1]
        sg = 1
        while True:
            if x == 0 or y == 0:
                sg = 0
                break
            if x > 0 and y > 0:
                break
            if x < 0:
                x, y, sg = -x, x + y, -sg
            else:
                x, y, sg = x + 3 * y, -y, -sg
        if sg == 0:
            continue
        mu = (x - 1, y - 1)
        out[mu] = out.get(mu, 0) + sg * m
    out = {k: v for k, v in out.items() if v != 0}
    if any(v < 0 for v in out.values()):
        _FLAG_R1[0] += 1
    _R1F[key] = out
    return out


# ---------------------------------------------------------------------------
# ROUTE 2: exact Weyl characters (alternant division) + greedy
# full-character subtraction.  Shares NO computation with Route 1
# beyond the declared constants above.
# ---------------------------------------------------------------------------
_R2C = {}
_R2F = {}
_FLAG_R2 = [0]     # trips on a non-dominant/non-positive leading term


def _alternant(t):
    """A_t = sum_w det(w) e^{w(t)} as a dict, t strictly dominant."""
    out = {}
    for w in W12:
        wt_ = _mat_apply(w, t)
        out[wt_] = out.get(wt_, 0) + DET[w]
    return out


_DEN = _alternant((1, 1))


def _r2_char(lam):
    """chi_lam = A_{lam+rho} / A_rho by exact Laurent division (greedy
    on the _ordk leading term; A_rho's leading term is e^rho with
    coefficient +1)."""
    if lam in _R2C:
        return _R2C[lam]
    rem = dict(_alternant((lam[0] + 1, lam[1] + 1)))
    quot = {}
    guard = 0
    while rem:
        guard += 1
        assert guard < 500000, "character division guard tripped"
        lt = max(rem, key=_ordk)
        c = rem[lt]
        mono = (lt[0] - 1, lt[1] - 1)
        quot[mono] = quot.get(mono, 0) + c
        for wmu, s in _DEN.items():
            k = (mono[0] + wmu[0], mono[1] + wmu[1])
            v = rem.get(k, 0) - c * s
            if v:
                rem[k] = v
            else:
                rem.pop(k, None)
    assert all(v > 0 for v in quot.values()), \
        "character with a non-positive coefficient"
    _R2C[lam] = quot
    return quot


def _r2_fuse(a, b):
    """Tensor decomposition by Laurent multiplication of full characters
    and greedy subtraction of the full character at the leading term."""
    key = (a, b)
    if key in _R2F:
        return _R2F[key]
    ca, cb = _r2_char(a), _r2_char(b)
    prod = {}
    for w1, m1 in ca.items():
        for w2, m2 in cb.items():
            k = (w1[0] + w2[0], w1[1] + w2[1])
            v = prod.get(k, 0) + m1 * m2
            if v:
                prod[k] = v
            else:
                prod.pop(k, None)
    out = {}
    guard = 0
    while prod:
        guard += 1
        assert guard < 20000, "greedy decomposition guard tripped"
        lt = max(prod, key=_ordk)
        c = prod[lt]
        if lt[0] < 0 or lt[1] < 0 or c < 0:
            _FLAG_R2[0] += 1
            break
        out[lt] = c
        for w, m in _r2_char(lt).items():
            v = prod.get(w, 0) - c * m
            if v:
                prod[w] = v
            else:
                prod.pop(w, None)
    _R2F[key] = out
    return out


# ---------------------------------------------------------------------------
# the battery (labels pinned by the exact dimension formula) and folds
# ---------------------------------------------------------------------------
BATTERY = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1),
           (3, 0), (0, 2), (4, 0), (2, 1)]
BATTERY_DIMS = [1, 7, 14, 27, 64, 77, 77, 182, 189]


def _r1_fold(labels):
    dec = {UNIT: 1}
    for b in sorted(labels):
        new = {}
        for x, m in dec.items():
            for c, k in _r1_fuse(x, b).items():
                new[c] = new.get(c, 0) + m * k
        dec = new
    return dec


def _r2_fold(labels):
    dec = {UNIT: 1}
    for b in sorted(labels):
        new = {}
        for x, m in dec.items():
            for c, k in _r2_fuse(x, b).items():
                new[c] = new.get(c, 0) + m * k
        dec = new
    return dec


def _generation():
    """First appearance of each battery irrep in fused powers of the 7
    (route 1); the grading-kill leg and the generation fact ride on
    this table."""
    dec = {SEVEN: 1}
    gen_at = {SEVEN: 1}
    for k in range(2, 5):
        new = {}
        for x, m in dec.items():
            for c, mm in _r1_fuse(x, SEVEN).items():
                new[c] = new.get(c, 0) + m * mm
        dec = new
        for c in dec:
            gen_at.setdefault(c, k)
    return gen_at


# ---------------------------------------------------------------------------
# graph model (verbatim the banked center-flux conventions, G2 labels)
# ---------------------------------------------------------------------------
_SGCACHE = {}
_CONTENTS_SEEN = set()


def _singlet_mult(labels):
    """Multiplicity of the trivial irrep in the tensor fold of labels
    (route-1 rule; route agreement over every content consumed is
    asserted in the fold cross-check leg)."""
    key = tuple(sorted(labels))
    if key in _SGCACHE:
        return _SGCACHE[key]
    _CONTENTS_SEEN.add(key)
    m = _r1_fold(key).get(UNIT, 0)
    _SGCACHE[key] = m
    return m


def _content(g, cfg, v):
    """Oriented-slot content at vertex v: label r at HEAD, conj(r) at
    TAIL (banked convention; conj = id for G2, computed), source
    un-conjugated."""
    out = []
    for i, (x, y) in enumerate(g['E']):
        if y == v:
            out.append(cfg[i])
        if x == v:
            out.append(_conj(cfg[i]))
    s = g['sources'].get(v)
    if s is not None and s != UNIT:
        out.append(s)
    return tuple(out)


def _enum(g, labels):
    """Exhaustive admissible-set enumeration at the stated cap, pruned
    at vertex completion (the banked enumerator's shape; verified
    against zero-pruning brute force in the lane's audit)."""
    E = g['E']
    inc = {v: [i for i, (x, y) in enumerate(E) if v in (x, y)]
           for v in g['V']}
    interior = [v for v in g['V'] if v not in g['boundary']]
    comp = {}
    for v in interior:
        if inc[v]:
            comp.setdefault(max(inc[v]), []).append(v)
        elif _singlet_mult(_content(g, (), v)) == 0:
            return []
    out = []
    cfg = [UNIT] * len(E)

    def rec(i):
        if i == len(E):
            out.append(tuple(cfg))
            return
        for lab in labels:
            cfg[i] = lab
            if all(_singlet_mult(_content(g, cfg, v)) > 0
                   for v in comp.get(i, ())):
                rec(i + 1)
    rec(0)
    return out


def _path_graph(L, src):
    return {'V': [f"v{i}" for i in range(L + 1)],
            'E': [(f"v{i}", f"v{i+1}") for i in range(L)],
            'boundary': frozenset([f"v{L}"]), 'sources': {'v0': src},
            'nested': [frozenset(f"v{j}" for j in range(i))
                       for i in range(1, L + 1)], 'L': L}


def _tt_graph(L, src):
    """Triangle + tail (the banked screen-supporting shape TT(L))."""
    V = ['t0', 'w1', 'w2'] + [f"p{i}" for i in range(1, L + 1)]
    E = [('t0', 'w1'), ('w1', 'w2'), ('w2', 't0'), ('t0', 'p1')]
    for i in range(1, L):
        E.append((f"p{i}", f"p{i+1}"))
    return {'V': V, 'E': E, 'boundary': frozenset([f"p{L}"]),
            'sources': {'t0': src},
            'nested': [frozenset(['t0', 'w1', 'w2']
                                 + [f"p{j}" for j in range(1, i)])
                       for i in range(1, L + 1)], 'L': L}


def _claw_graph(n_src, src):
    V = [f"s{i}" for i in range(n_src)] + ['c', 'x1']
    E = [(f"s{i}", 'c') for i in range(n_src)] + [('c', 'x1')]
    return {'V': V, 'E': E, 'boundary': frozenset(['x1']),
            'sources': {f"s{i}": src for i in range(n_src)},
            'nested': [frozenset([f"s{i}" for i in range(n_src)] + ['c'])],
            'L': 1}


def _k4_tail_graph(L, src):
    """K4 on {s,a,b,c} (source at s) with a length-L tail from s to the
    boundary -- the walked geometry for the all-adjoint containment of
    a single 7 (cycle-bearing; the nested family lies along the tail)."""
    V = ['s', 'a', 'b', 'c'] + [f"p{i}" for i in range(1, L + 1)]
    E = [('s', 'a'), ('s', 'b'), ('s', 'c'),
         ('a', 'b'), ('b', 'c'), ('c', 'a'), ('s', 'p1')]
    for i in range(1, L):
        E.append((f"p{i}", f"p{i+1}"))
    return {'V': V, 'E': E, 'boundary': frozenset([f"p{L}"]),
            'sources': {'s': src},
            'nested': [frozenset(['s', 'a', 'b', 'c']
                                 + [f"p{j}" for j in range(1, i)])
                       for i in range(1, L + 1)], 'L': L}


CAP = [(0, 0), (1, 0), (0, 1), (2, 0)]        # dims 1, 7, 14, 27

_CROSS_REFS = ['T_center_order_parameter_triality',
               'T_frustration_center_partition',
               'R_SU_Nc_neq_3_killed']

_AUDIT_RECORD = ('AUDIT_REPORT.md (hostile audit 2026-07-11, '
                 'LAND-WITH-FIXES 0.88) is the route-independence '
                 'certificate: foreign-basis third route (3D sum-zero '
                 'realization, audit_probe_g2_independent.py, 275 '
                 'checks, exit 0) + mod-p alternant fourth route + '
                 'Casimir trace-identity blade, agreeing with both '
                 'in-lane routes on all 81 pairs and every graph count '
                 '(12/4/4/3306/794); mutation hardness 5/5 -- '
                 'mirroring the SU(3) stage-1 audit precedent in '
                 'center_flux_exit.  Fixes F1-F6 carried in the walker '
                 'of record')

_LANE_RECORD = ('The Turning (parked)/g2_exhibit_2026-07-11/ '
                '(walk_g2_exhibit.py [590 checks, exit 0; fixes F1-F6 '
                'carried], WALK_NOTE.md section 7 = the certified bank '
                'entry, AUDIT_REPORT.md LAND-WITH-FIXES 0.88)')


def check_L_trivial_center_no_nality_obstruction():
    """Leg A [P_math | lattice-model conventions + pinned G2
    conventions]: the trivial-center vacuity statement in its honest
    VACUOUS-shaped form -- 'no kinematic N-ality obstruction', never
    'everything screens' -- earned from the lattice index AND from
    fusion alone, with the tree-geometry control in-battery.  See the
    module docstring for the statement, premise stack, kill modes, and
    MAY-NOT-CITE fences.  This is the DISTILLED battery; the 590-check
    lane walker is the record."""
    from apf.center_flux_exit import check_L_center_flux_exit

    fails = []
    n_checks = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        n_checks[0] += 1

    # ---- live bank anchor: the banked pattern this module composes with
    r = check_L_center_flux_exit()
    ck(r.get('passed') is True and r.get('n_checks') == 578
       and 'H-hom' in r.get('epistemic', ''),
       "anchor L_center_flux_exit passes LIVE (578-check distilled "
       "battery; its H-hom-conditioned grade line carried, its "
       "MAY-NOT-CITE fences travel with every use of its pattern here; "
       "T_center_order_parameter_triality is cross_ref only per audit "
       "fix F3 -- the lane walker's live anchor run of it stays lane "
       "record)")

    # ---- (1) the pinned conventions and the derived root system ---------
    ck(A_CARTAN == ((2, -1), (-3, 2)),
       "Cartan matrix pinned: A = [[2,-1],[-3,2]] under "
       "A[i][j] = 2(a_i,a_j)/(a_j,a_j), alpha_1 SHORT, alpha_2 LONG "
       "(Bourbaki node order; the charter's matrix, not its transpose)")
    gram = [[_ip(ALPHA[i], ALPHA[j]) for j in range(2)] for i in range(2)]
    ck(gram == [[2, -3], [-3, 6]],
       "pairing coherence: u^T F v on omega-coordinates reproduces the "
       "alpha-Gram matrix [[2,-3],[-3,6]] (alpha_1 short, alpha_2 long)")
    ck(all(2 * _ip(ALPHA[i], ALPHA[j]) // _ip(ALPHA[j], ALPHA[j])
           == A_CARTAN[i][j] for i in range(2) for j in range(2)),
       "Cartan entries recomputed from the pairing "
       "(2(a_i,a_j)/(a_j,a_j) == A[i][j], all four entries)")
    ck(len(W12) == 12 and sorted(DET.values()).count(1) == 6
       and sorted(DET.values()).count(-1) == 6
       and all(_mat_mul(w, u) in DET for w in W12 for u in W12),
       "Weyl group DERIVED by matrix closure from the two simple "
       "reflections: order 12, 6 even + 6 odd, closed under "
       "composition (computed, not assumed)")
    ck(((-1, 0), (0, -1)) in DET,
       "-identity is in the Weyl group (w0 = -1), so conj(r) = "
       "-w0(r) = r: EVERY G2 irrep is self-dual -- the model call "
       "collapsing edge orientation, computed not assumed")
    ck(all(_ip(_mat_apply(w, u), _mat_apply(w, v)) == _ip(u, v)
           for w in W12
           for u in ((1, 0), (0, 1), (1, 1))
           for v in ((1, 0), (0, 1), (1, 2))),
       "every Weyl element preserves the pairing (checked on a "
       "spanning set; exact)")
    ck(len(_ALLROOTS) == 12 and len(POS) == 6
       and set(POS) == {(2, -1), (-3, 2), (-1, 1), (1, 0), (3, -1),
                        (0, 1)},
       "root system DERIVED by W-orbit closure from the simple roots: "
       "12 roots, 6 positive == {a1, a2, a1+a2, 2a1+a2, 3a1+a2, "
       "3a1+2a2} exactly")
    ck(sorted(_ip(r_, r_) for r_ in POS) == [2, 2, 2, 6, 6, 6]
       and (1, 0) in [r_ for r_ in POS if _ip(r_, r_) == 2]
       and (0, 1) in [r_ for r_ in POS if _ip(r_, r_) == 6],
       "3 short + 3 long positive roots (norms 2 and 6); omega_1 = "
       "highest SHORT root (the 7's highest weight) and omega_2 = "
       "highest root (the adjoint's), both computed")

    # transposed-convention negative control (the pin is load-bearing)
    alpha_t = ((2, -3), (-1, 2))

    def ip_t(u, v):
        return (6 * u[0] * v[0] + 3 * (u[0] * v[1] + u[1] * v[0])
                + 2 * u[1] * v[1])

    pos_t = [(2, -3), (-1, 2), (1, -1), (0, 1), (-1, 3), (1, 0)]

    def dim_t(lam):
        lr = (lam[0] + 1, lam[1] + 1)
        num = 1
        den = 1
        for al in pos_t:
            num *= ip_t(lr, al)
            den *= ip_t((1, 1), al)
        assert num % den == 0
        return num // den

    ck([[ip_t(alpha_t[i], alpha_t[j]) for j in range(2)]
        for i in range(2)] == [[6, -3], [-3, 2]]
       and dim_t((1, 0)) == 14 and dim_t((0, 1)) == 7,
       "NEGATIVE CONTROL: under the TRANSPOSED Cartan convention "
       "dim(1,0) = 14 and dim(0,1) = 7 -- the labels swap; the "
       "convention pin is load-bearing (computed)")
    ck(_weyl_dim((1, 0)) == 7 and _weyl_dim((0, 1)) == 14,
       "under THIS module's pinned convention dim(1,0) = 7 "
       "(fundamental) and dim(0,1) = 14 (adjoint), as stated "
       "everywhere below")

    # ---- (2) Leg A ground (i): the lattice index ------------------------
    ck((A_CARTAN[0][0] * A_CARTAN[1][1]
        - A_CARTAN[0][1] * A_CARTAN[1][0]) == 1,
       "LEG A ground (i): |P/Q| = det(Cartan) = 1 -- the N-ality "
       "receiving group Z(G)-hat = P/Q is the TRIVIAL group (order 1, "
       "computed); compare SU(3) where the index is 3")
    ck(_alpha_coords((1, 0)) == (2, 1) and _alpha_coords((0, 1)) == (3, 2),
       "both fundamental weights are INTEGER combinations of simple "
       "roots (omega_1 = 2a1 + a2, omega_2 = 3a1 + 2a2): P = Q "
       "(computed; the SU(3) contrast: its fundamental weight is NOT "
       "in the root lattice)")
    n_wt = 0
    bad_wt = []
    for lam in BATTERY:
        for mu in _r1_weights(lam):
            c1, c2 = _alpha_coords(mu)
            n_wt += 1
            recon = (2 * c1 - 3 * c2, -c1 + 2 * c2)
            if recon != mu:
                bad_wt.append((lam, mu))
    ck(n_wt == 267 and not bad_wt,
       f"ALL {n_wt} weights of ALL 9 battery irreps lie in the ROOT "
       f"lattice (integer alpha-coordinates, reconstruction exact for "
       f"every weight; {len(bad_wt)} failures) -- every N-ality coset "
       "is the zero coset.  One summary check per audit fix F6; the "
       "underlying 267 per-weight computations all still run")

    # ---- (3) q == 0: H-hom vacuously true, billed as vacuity ------------
    def q_nality(lam):
        return 0        # the unique element of the trivial group

    viol = 0
    ncons = 0
    for a in BATTERY:
        for b in BATTERY:
            for c, m in _r1_fuse(a, b).items():
                if m > 0:
                    ncons += 1
                    if q_nality(c) != (q_nality(a) + q_nality(b)):
                        viol += 1
    ck(viol == 0 and ncons > 400,
       f"H-hom for the trivial charge group: {ncons} constituents, 0 "
       "violations -- VACUOUSLY TRUE (q == 0 makes the fusion-"
       "homomorphism condition 0 == 0 + 0; this leg certifies SHAPE, "
       "not substance, and is billed as vacuity)")
    ck(all(q_nality(lam) == 0 for lam in BATTERY),
       "q == 0 identically on the battery: NO irrep carries nonzero "
       "N-ality; the flux-exit trigger 'enclosed source charge != 0' "
       "is UNSATISFIABLE for G2 -- the honest corollary is 'no "
       "KINEMATIC N-ality obstruction to screening', and it licenses "
       "NO existence claim (screens stay geometry-conditional)")

    # ---- (4) Leg A ground (ii): the fusion-intrinsic grading kill -------
    ck(_r1_fuse(SEVEN, SEVEN).get(SEVEN, 0) == 1,
       "LEG A ground (ii): 7 appears in 7 (x) 7 (mult 1, both-route "
       "battery in the sibling check) -- for ANY fusion homomorphism q "
       "into ANY abelian group, q(7) = q(7) + q(7) forces q(7) = 0 "
       "(group cancellation)")
    gen_at = _generation()
    ck(all(lam in gen_at or lam == UNIT for lam in BATTERY)
       and max(gen_at.values()) <= 4 and gen_at.get(UNIT) == 2,
       f"the 7 GENERATES the battery under fusion (first-appearance "
       f"table {sorted(gen_at.items())}; power <= 4, computed): with "
       "ground (ii) every battery irrep gets q == 0 -- the G2 fusion "
       "ring itself admits NO nontrivial N-ality-style grading; the "
       "vacuity is fusion-intrinsic, not just a center-order fact")
    ck(_r1_fuse(FOURTEEN, FOURTEEN).get(FOURTEEN, 0) == 1,
       "14 in 14 (x) 14 (mult 1): the same cancellation kills any "
       "nonzero q(14) directly (computed)")
    v2 = v3 = 0
    for a in BATTERY:
        for b in BATTERY:
            for c, m in _r1_fuse(a, b).items():
                if m > 0 and c[0] % 2 != (a[0] + b[0]) % 2:
                    v2 += 1
                if m > 0 and (c[0] - c[1]) % 3 \
                        != (a[0] - a[1] + b[0] - b[1]) % 3:
                    v3 += 1
    ck(v2 > 0 and v3 > 0,
       f"grading-kill mutation probe: fake nontrivial gradings (mod-2 "
       f"label parity: {v2} violations; SU(3)-triality lookalike "
       f"(m1-m2) mod 3: {v3} violations) are REFUTED by the computed "
       "fusion -- the H-hom battery shape can fail, and for G2 every "
       "nontrivial grading DOES fail (the vacuity is earned, not "
       "assumed)")

    # ---- (5) tree-geometry control: q == 0 licenses NO screen ----------
    for L in (1, 2, 3, 4):
        g = _path_graph(L, SEVEN)
        cfgs = _enum(g, CAP)
        cuts = [frozenset(i for i, (x, y) in enumerate(g['E'])
                          if (x in S) != (y in S)) for S in g['nested']]
        ck(len(cfgs) == 1 and cfgs[0] == tuple([SEVEN] * L),
           f"path L={L}, source 7, cap {{1,7,14,27}}: the admissible "
           f"set is EXACTLY the all-7 string (support {L}, growing "
           "with L; exhaustive)")
        ck(all(len(c) == 1 for c in cuts)
           and all(not (cuts[i] & cuts[j]) for i in range(len(cuts))
                   for j in range(i + 1, len(cuts)))
           and all(all(cfgs[0][i] != UNIT for i in c) for c in cuts),
           f"path L={L}: the unique admissible configuration carries a "
           f"NONZERO label across every cut of the nested {L}-member "
           "disjoint family -- support >= L, NO bounded screen ON THIS "
           "GEOMETRY despite q == 0 (geometry-conditional, computed; "
           "mirrors the banked loopless-tree fact)")
    ck(_singlet_mult((SEVEN,)) == 0,
       "contrapositive control: a bare 7 with all-trivial links is "
       "inadmissible at its own vertex (7 alone contains no trivial "
       "irrep; computed)")

    passed = not fails
    return {
        'name': 'L_trivial_center_no_nality_obstruction',
        'epistemic': ('P_math | lattice-model conventions (the banked '
                      'oriented electric-basis graph model with '
                      'per-vertex-singlet admissibility, Gauss reading '
                      'a named identification) + pinned G2 conventions '
                      '(Cartan matrix + node order + weight '
                      'coordinates) -- vacuity billed in-sentence: no '
                      'kinematic N-ality obstruction, NEVER '
                      '"everything screens"'),
        'passed': passed,
        'tier': 4,
        'key_result': (
            'For G2 (compact simple, trivial center), in the named '
            'lattice model and pinned conventions: the N-ality '
            'receiving group Z(G)-hat = P/Q is TRIVIAL -- det(Cartan) '
            '= 1, both fundamental weights integer in the root '
            'lattice, all 267 weights of all 9 battery irreps in the '
            'root lattice (each computed) -- so the N-ality charge map '
            'q == 0 identically, H-hom is VACUOUSLY true (400+ '
            'constituents, billed as vacuity: shape, not substance), '
            'and the flux-exit trigger "enclosed source charge != 0" '
            'is UNSATISFIABLE: NO KINEMATIC N-ality obstruction to '
            'screening for any G2 irrep.  Earned twice: the lattice '
            'index AND the fusion-intrinsic kill (7 in 7 (x) 7, mult '
            '1, forces q(7) = 0 for any fusion homomorphism into any '
            'abelian group; the 7 generates the battery, so the G2 '
            'fusion ring admits NO nontrivial N-ality-style grading; '
            'fake mod-2/mod-3 gradings refuted by the computed '
            'fusion).  NOT "everything screens": on the walked '
            'loopless tree the single 7 source admits NO bounded '
            'screen at the stated cap -- the admissible set is exactly '
            'the growing all-7 string, support >= L across the nested '
            'disjoint cut family.  Screen existence stays '
            'geometry-conditional; no gauge-group claim '
            '(R_SU_Nc_neq_3_killed stands); kinematic admissibility '
            'only.'
        ),
        'dependencies': ['L_center_flux_exit'],
        'cross_refs': list(_CROSS_REFS),
        'artifacts': {
            'witnesses': ('det(Cartan) = 1; omega_1 = 2a1 + a2, '
                          'omega_2 = 3a1 + 2a2 (integer); 267/267 '
                          'battery weights in the root lattice; H-hom '
                          '400+ constituents 0 violations (vacuous); '
                          '7 in 7x7 and 14 in 14x14 each mult 1 (the '
                          'grading kill); generation table {7:1, '
                          '1/14/27:2, 64/77:3, 77p/182/189:4}; path '
                          'L=1..4 admissible set == the all-7 string '
                          'exactly'),
            'premise_stack': ('lattice-model conventions (MODEL '
                              'DEFINITION, named; the banked pattern '
                              'anchored live) + pinned G2 conventions '
                              '(transposed alternative computed as '
                              'control) + battery/cap scoping; NO '
                              'H-hom needed (trivial charge group); '
                              'A1 deliberately not consumed (house '
                              'precedent)'),
            'kill_condition': ('a battery-irrep weight outside the '
                               'root lattice; det(Cartan) != 1 under '
                               'the pinned convention; any nontrivial '
                               'abelian grading of the computed fusion '
                               'ring (7 absent from 7 (x) 7 would '
                               'reopen it -- both routes wrong '
                               'together); a route disagreement or '
                               'construction-flag trip (sibling '
                               'check); a fence-stem hit in any check '
                               'message or function name'),
            'may_not_cite': ('no gauge-group claim: G2 is a '
                             'mathematical exhibit, '
                             'R_SU_Nc_neq_3_killed stands untouched; '
                             'the vacuity leg licenses NO screen '
                             'existence -- never "everything screens", '
                             'screen existence geometry-conditional '
                             '(walked tree control in-battery); no '
                             'dynamics/gap/continuum/fixed-L/reading '
                             'sentence; the G2 intermediate string '
                             'untouchable (kinematic exhibits only); '
                             'the banked flux-exit MAY-NOT-CITE lines '
                             'travel with its pattern'),
            'audit_record': _AUDIT_RECORD,
            'lane_records': _LANE_RECORD,
        },
        'fail_reasons': fails,
        'n_checks': n_checks[0],
    }


def check_T_g2_fusion_screen_exhibit():
    """Legs B + C [P, instance-scoped at stated caps and walked
    graphs]: the twice-constructed cross-checked G2 fusion battery and
    the contained-bounded-screen exhibits (TT 7-screen, claw contrast,
    K4 all-adjoint containment), with the route-2 greedy-soundness
    machine-check (audit fix F1), the Casimir trace-identity blade with
    its dimension-preserving-sabotage control (audit fix F4), and the
    vocabulary fence scanning check messages AND function names (audit
    fix F2).  See the module docstring for the statement, premise
    stack, kill modes, and MAY-NOT-CITE fences.  This is the DISTILLED
    battery; the 590-check lane walker is the record."""
    from apf.center_flux_exit import check_L_center_flux_exit

    fails = []
    n_checks = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        n_checks[0] += 1

    # ---- live bank anchor: the banked pattern the graph legs run on -----
    r = check_L_center_flux_exit()
    ck(r.get('passed') is True and r.get('n_checks') == 578
       and 'H-hom' in r.get('epistemic', ''),
       "anchor L_center_flux_exit passes LIVE (578-check distilled "
       "battery; the graph model here is verbatim its conventions, its "
       "grade line carried and its MAY-NOT-CITE fences travel; "
       "T_center_order_parameter_triality is cross_ref only per audit "
       "fix F3)")

    # ---- (1) route 1: Freudenthal weight systems -------------------------
    for lam, d in zip(BATTERY, BATTERY_DIMS):
        wts = _r1_weights(lam)
        total = sum(wts.values())
        ck(total == _weyl_dim(lam) == _sextic_dim(lam) == d,
           f"dim V{lam}: Freudenthal weight count {total} == Weyl "
           f"product formula {_weyl_dim(lam)} == closed sextic "
           f"{_sextic_dim(lam)} == battery label {d}")
        ck(wts.get(lam, 0) == 1
           and all(wts.get((-w[0], -w[1]), 0) == m
                   for w, m in wts.items()),
           f"V{lam}: highest weight multiplicity 1 and weight system "
           "symmetric under negation (self-duality at the weight "
           "level, computed)")
        ck(all(wts.get(_mat_apply(w, mu), 0) == m
               for mu, m in wts.items() for w in (W12[3], W12[7])),
           f"V{lam}: multiplicities Weyl-invariant (spot elements)")
    ck(_r1_weights(SEVEN) == {(0, 0): 1, (1, 0): 1, (-1, 0): 1,
                              (2, -1): 1, (-2, 1): 1, (-1, 1): 1,
                              (1, -1): 1},
       "the 7's weight system == {0} + the six short roots, each "
       "multiplicity 1 (computed)")
    w14 = _r1_weights(FOURTEEN)
    ck(w14.get((0, 0), 0) == 2
       and all(w14.get(rt, 0) == 1 for rt in _ALLROOTS)
       and sum(w14.values()) == 14,
       "the 14's weight system == the 12 roots (mult 1) + zero weight "
       "(mult 2): the adjoint, computed")

    # ---- (2) route 2: exact Weyl characters ------------------------------
    ck(max(_DEN, key=_ordk) == RHO and _DEN[RHO] == 1 and len(_DEN) == 12,
       "A_rho has 12 distinct terms with leading term e^rho, "
       "coefficient +1 (the division's pivot, computed)")
    for lam, d in zip(BATTERY, BATTERY_DIMS):
        chi = _r2_char(lam)
        ck(sum(chi.values()) == d
           and len(_alternant((lam[0] + 1, lam[1] + 1))) == 12,
           f"chi{lam}: coefficient sum == dim == {d}; A_(lam+rho) has "
           "12 distinct terms (regular orbit; route 2)")
        ck(chi == _r1_weights(lam),
           f"chi{lam}: alternant-division character == Freudenthal "
           "weight system EXACTLY (multiplicity-by-multiplicity; the "
           "two routes' weight computations are independent and agree)")

    # ---- (3) the 81-pair cross-checked fusion battery --------------------
    for a in BATTERY:
        for b in BATTERY:
            f1 = _r1_fuse(a, b)
            ck(f1 == _r2_fuse(a, b),
               f"routes agree on {a} (x) {b} (multiplicity-exact)")
            ck(sum(m * _weyl_dim(c) for c, m in f1.items())
               == _weyl_dim(a) * _weyl_dim(b)
               and f1 == _r1_fuse(b, a),
               f"dimension multiplicativity + commutativity at "
               f"{a} (x) {b} (exact)")
    ck(_FLAG_R1[0] == 0 and _FLAG_R2[0] == 0,
       "zero construction-flag trips on the battery (negative Klimyk "
       "multiplicity / non-dominant greedy leading term would kill the "
       "construction legs -- the kill mode's counters)")
    ck(all(_r1_fuse(a, UNIT) == {a: 1} and _r2_fuse(UNIT, a) == {a: 1}
           for a in BATTERY),
       "unit neutrality on the whole battery (both routes)")

    # ---- (4) route-2 greedy soundness, machine-checked (audit fix F1) ---
    ck(all(_ip(al, RHO) > 0 for al in POS),
       "greedy soundness (i): the ordering functional f = (., rho) is "
       "strictly positive on every positive root, recomputed at the "
       "point of use (so subtracting a character strictly lowers every "
       "remaining term below the removed leading term)")
    need = set(BATTERY)
    for a in BATTERY:
        for b in BATTERY:
            need |= set(_r2_fuse(a, b))
    tri_ok = True
    n_tri = 0
    for lam in sorted(need):
        chi = _r2_char(lam)
        if chi.get(lam, 0) != 1:
            tri_ok = False
        for mu in chi:
            n_tri += 1
            c1, c2 = _alpha_coords((lam[0] - mu[0], lam[1] - mu[1]))
            if c1 < 0 or c2 < 0:
                tri_ok = False
            if mu != lam and not (_ordk(mu) < _ordk(lam)):
                tri_ok = False
    ck(tri_ok and n_tri > 500,
       f"GREEDY SOUNDNESS machine-checked over {len(need)} characters "
       f"/ {n_tri} support weights: every character route 2 ever uses "
       "has coefficient EXACTLY 1 at its highest weight, full support "
       "inside lam - Q+ (dominance triangularity: nonnegative integer "
       "alpha-coordinates of lam - mu), and strict ordk descent off "
       "the top -- with positive coefficients this makes the greedy "
       "leading-term coefficient equal the highest-weight multiplicity "
       "at every step (audit fix F1, carried)")

    # ---- (5) the load-bearing table pins (both routes) -------------------
    tbl77 = {(0, 0): 1, (1, 0): 1, (0, 1): 1, (2, 0): 1}
    ck(_r1_fuse(SEVEN, SEVEN) == tbl77
       and _r2_fuse(SEVEN, SEVEN) == tbl77
       and sum(m * _weyl_dim(c) for c, m in tbl77.items()) == 49,
       "7 (x) 7 = 1 + 7 + 14 + 27 (BOTH routes, exact multiplicities "
       "all 1; dimension count 49 exact) -- the trivial irrep IS "
       "present: the charter's load-bearing channel")
    t714 = {(1, 0): 1, (2, 0): 1, (1, 1): 1}
    ck(_r1_fuse(SEVEN, FOURTEEN) == t714
       and _r2_fuse(SEVEN, FOURTEEN) == t714,
       "7 (x) 14 = 7 + 27 + 64 (both routes; NO trivial irrep -- one "
       "adjoint does not close a 7)")
    t1414 = {(0, 0): 1, (0, 1): 1, (2, 0): 1, (3, 0): 1, (0, 2): 1}
    ck(_r1_fuse(FOURTEEN, FOURTEEN) == t1414
       and _r2_fuse(FOURTEEN, FOURTEEN) == t1414,
       "14 (x) 14 = 1 + 14 + 27 + 77 + 77' (both routes; NO 7: two "
       "adjoints do not reach the 7)")
    for a in BATTERY:
        for b in BATTERY:
            ck(_r1_fuse(a, b).get(UNIT, 0) == (1 if a == b else 0),
               f"Schur pin at {a},{b}: trivial-irrep multiplicity in "
               "a (x) b == 1 iff a == b else 0 (all irreps self-dual, "
               "so r (x) rbar = r (x) r; computed)")
    ck(_r1_fold((FOURTEEN, FOURTEEN, FOURTEEN)).get(SEVEN, 0) == 1
       and _r2_fold((FOURTEEN, FOURTEEN, FOURTEEN)).get(SEVEN, 0) == 1,
       "7 sits in 14 (x) 14 (x) 14 with multiplicity EXACTLY 1 (both "
       "routes) -- the three-adjoint channel behind the folklore "
       "statement, as a pure fusion fact")
    ck(_r1_fold((SEVEN, SEVEN, SEVEN)).get(UNIT, 0) == 1
       and _r2_fold((SEVEN, SEVEN, SEVEN)).get(UNIT, 0) == 1,
       "7 (x) 7 (x) 7 contains the trivial irrep with multiplicity "
       "EXACTLY 1 (both routes; the triple-containment channel)")
    gen_at = _generation()
    ck(all(lam in gen_at or lam == UNIT for lam in BATTERY)
       and gen_at.get(UNIT) == 2,
       f"every battery irrep appears in some fused power of the 7 "
       f"(power <= 4; first-appearance table {sorted(gen_at.items())}) "
       "-- the 7 generates the battery under fusion (computed)")

    # ---- (6) Casimir trace-identity blade (audit fix F4) -----------------
    ck(_casimir(SEVEN) == 12 and _casimir(FOURTEEN) == 24
       and 2 * _casimir(SEVEN) == _casimir(FOURTEEN),
       "quadratic Casimir C2(lam) = (lam, lam + 2 rho) in the pinned "
       "pairing: C2(7) = 12, C2(14) = 24, ratio 1:2 (the known G2 "
       "ratio; exact integers, this module's normalization)")
    cas_ok = True
    n_pairs = 0
    for a in BATTERY:
        for b in BATTERY:
            n_pairs += 1
            lhs = sum(m * _weyl_dim(c) * _casimir(c)
                      for c, m in _r1_fuse(a, b).items())
            rhs = _weyl_dim(a) * _weyl_dim(b) \
                * (_casimir(a) + _casimir(b))
            if lhs != rhs:
                cas_ok = False
    ck(cas_ok and n_pairs == 81,
       "CASIMIR TRACE IDENTITY verified on ALL 81 battery pairs: "
       "sum_c m_c dim(c) C2(c) == dim(a) dim(b) (C2(a) + C2(b)) -- a "
       "blade independent of both routes' construction, carried per "
       "audit fix F4")
    sab = dict(_r1_fuse(SEVEN, SEVEN))
    sab[FOURTEEN] = sab.get(FOURTEEN, 0) - 1
    sab[SEVEN] = sab.get(SEVEN, 0) + 2   # -14 + 2*7 = 0: dims preserved
    ck(sum(m * _weyl_dim(c) for c, m in sab.items()) == 49
       and sum(m * _weyl_dim(c) * _casimir(c) for c, m in sab.items())
       != 49 * (_casimir(SEVEN) + _casimir(SEVEN)),
       "sabotage control: the dimension-preserving tampered 7 (x) 7 "
       "table (one 14 swapped for two 7s) PASSES dimension counting "
       "and IS caught by the Casimir trace identity -- the added blade "
       "is live, not redundant theater (the audit's demonstrated blind "
       "spot, computed in-module)")

    # ---- (7) further mutation probes (the batteries can fail) -----------
    t = dict(_r1_fuse(SEVEN, SEVEN))
    t[FOURTEEN] = t[FOURTEEN] + 1
    ck(t != _r2_fuse(SEVEN, SEVEN)
       and sum(m * _weyl_dim(c) for c, m in t.items()) != 49,
       "mutation probe: flipping one multiplicity in route 1's "
       "7 (x) 7 output breaks route agreement AND dimension "
       "multiplicativity (caught twice)")
    n_caught = 0
    for a in BATTERY:
        for b in BATTERY:
            sab2 = dict(_r1_fuse(a, b))
            spur = (a[0] + b[0] + 1, a[1] + b[1])
            sab2[spur] = sab2.get(spur, 0) + 1
            if sum(m * _weyl_dim(c) for c, m in sab2.items()) \
                    != _weyl_dim(a) * _weyl_dim(b):
                n_caught += 1
    ck(n_caught == 81,
       "mutation probe: a spurious constituent injected into EVERY "
       "battery pair is caught by dimension counting 81/81")
    bad = dict(_r1_weights(SEVEN))
    bad[(0, 0)] = 2
    ck(sum(bad.values()) != _weyl_dim(SEVEN),
       "mutation probe: an inflated zero-weight multiplicity in the "
       "7's weight system is caught by the dimension pin")

    # ---- (8) Leg C: the TT 7-screen (walked screen-supporting graph) ----
    counts_tt = []
    for L in (1, 2, 3):
        g = _tt_graph(L, SEVEN)
        screen = tuple([SEVEN] * 3 + [UNIT] * L)
        interior = [v for v in g['V'] if v not in g['boundary']]
        ck(all(_singlet_mult(_content(g, screen, v)) > 0
               for v in interior)
           and sum(1 for lab in screen if lab != UNIT) == 3,
           f"TT({L}), source 7: the 7-triangle screen (label 7 on the "
           "3 cycle edges, trivial tail) is admissible at every "
           "interior vertex -- hub closes by 7 (x) 7 (x) 7 containing "
           "1, cycle vertices by 7 (x) 7 containing 1; support EXACTLY "
           "the 3 cycle edges, bounded, constant in L (computed)")
        cuts = [frozenset(i for i, (x, y) in enumerate(g['E'])
                          if (x in S) != (y in S)) for S in g['nested']]
        ck(all(all(screen[i] == UNIT for i in c) for c in cuts),
           f"TT({L}): the screen crosses NO cut of the nested family "
           "-- fully contained (the frustration module's "
           "screen-supporting condition, instantiated; existence-only)")
        cfgs = _enum(g, CAP)
        counts_tt.append(len(cfgs))
        ck(screen in cfgs,
           f"TT({L}): screen located inside the EXHAUSTIVE admissible "
           f"set at cap {{1,7,14,27}} ({len(cfgs)} configurations)")
    ck(counts_tt == [12, 12, 12],
       "TT(1..3): admissible count 12 at each depth, CONSTANT in L "
       "(exact enumeration, pinned from the lane record and the "
       "audit's brute force -- the bounded-option cap arithmetic, "
       "computed not estimated)")
    ck(_r1_fuse(SEVEN, SEVEN).get(UNIT, 0) == 1,
       "the screen's channel: 7 (x) 7 contains the trivial irrep with "
       "multiplicity EXACTLY 1 (the charter's small-cap channel, "
       "battery-cross-checked on both routes)")

    # ---- (9) Leg C: the claw contrast with the banked SU(3) exhibit -----
    g2c = _claw_graph(2, SEVEN)
    cfgs2 = _enum(g2c, CAP)
    wit2 = (SEVEN, SEVEN, UNIT)
    ck(wit2 in cfgs2 and len(cfgs2) == 4
       and all(_singlet_mult(_content(g2c, wit2, v)) > 0
               for v in g2c['V'] if v not in g2c['boundary']),
       "claw2, two 7 sources: the fully contained witness (7-edges "
       "into the hub, TRIVIAL tail) is admissible, re-verified "
       "vertex-by-vertex; 4 admissible configurations, exhaustive at "
       "the cap -- a PAIR of G2 fundamentals is containable (7 (x) 7 "
       "contains 1); the banked SU(3) claw2 exhibit (pairs provably "
       "NOT containable, triality 2) does NOT transfer to trivial "
       "center: exactly the trivial-center corollary on a walked "
       "instance")
    g3c = _claw_graph(3, SEVEN)
    cfgs3 = _enum(g3c, CAP)
    ck((SEVEN, SEVEN, SEVEN, UNIT) in cfgs3 and len(cfgs3) == 4,
       "claw3, three 7 sources: fully contained witness admissible "
       "(7 (x) 7 (x) 7 contains 1 with multiplicity exactly 1; 4 "
       "configurations, exhaustive) -- triples contain as well: NO "
       "parity/N-ality grading distinguishes source counts for G2")
    g1c = _claw_graph(1, SEVEN)
    cfgs1 = _enum(g1c, CAP)
    ck(len(cfgs1) >= 1 and all(c[-1] != UNIT for c in cfgs1)
       and all(c[0] == SEVEN for c in cfgs1),
       "claw1, ONE 7 source: at this cap on this graph every "
       "admissible configuration carries a nonzero tail label (and "
       "label 7 next to the source: 1 sits in 7 (x) r at this cap "
       "only for r = 7, the Schur pin) -- the single 7 is not "
       "contained HERE.  A GEOMETRY + CAP fact, not an N-ality "
       "obstruction (there is none); the richer walked geometry below "
       "contains it")

    # ---- (10) Leg C: the all-adjoint containment on K4+tail --------------
    counts_k4 = []
    for L in (1, 2, 3):
        g = _k4_tail_graph(L, SEVEN)
        screen = tuple([FOURTEEN] * 6 + [UNIT] * L)
        interior = [v for v in g['V'] if v not in g['boundary']]
        ck(all(_singlet_mult(_content(g, screen, v)) > 0
               for v in interior)
           and sum(1 for lab in screen if lab != UNIT) == 6,
           f"K4+tail({L}), source 7 at s: the ALL-14 (all-adjoint) "
           "screen on the 6 K4 edges (trivial tail) is admissible at "
           "every interior vertex -- s closes by 7 (x) 14 (x) 14 (x) "
           "14 containing 1 (mult 1, computed), the others by 14 (x) "
           "14 (x) 14 containing 1; support EXACTLY the 6 K4 edges, "
           "bounded, constant in L")
        cuts = [frozenset(i for i, (x, y) in enumerate(g['E'])
                          if (x in S) != (y in S)) for S in g['nested']]
        ck(all(all(screen[i] == UNIT for i in c) for c in cuts)
           and all(not (cuts[i] & cuts[j]) for i in range(len(cuts))
                   for j in range(i + 1, len(cuts))),
           f"K4+tail({L}): screen crosses NO cut of the nested "
           f"{L}-member disjoint family -- fully contained "
           "(existence-only, conditional on THIS walked geometry at "
           "THIS cap; no claim that the screen is taken)")
        cfgs = _enum(g, CAP)
        counts_k4.append(len(cfgs))
        contained = [c for c in cfgs
                     if all(c[i] == UNIT for i in range(6, 6 + L))]
        ck(screen in cfgs and len(contained) == 794
           and screen in contained,
           f"K4+tail({L}): screen located inside the EXHAUSTIVE "
           f"admissible set at cap {{1,7,14,27}} ({len(cfgs)} "
           f"configurations, {len(contained)} of them fully contained "
           "-- exact counts, pinned from the lane record and the "
           "audit's brute force)")
    ck(counts_k4 == [3306, 3306, 3306],
       "K4+tail(1..3): admissible count 3306 at each depth, CONSTANT "
       "in L (exhaustive) -- bounded containment does not degrade "
       "with boundary distance on this walked geometry")

    # ---- (11) every graph-leg fold double-computed on both routes -------
    _singlet_mult((SEVEN,))     # the sibling check's contrapositive-
    # control content, included deterministically so this battery's
    # check count is independent of check execution order
    seen = sorted(_CONTENTS_SEEN)
    ck(len(seen) >= 20,
       f"fold cross-check is non-vacuous: {len(seen)} distinct vertex "
       "contents were consumed by the graph legs")
    for key in seen:
        ck(_r1_fold(key) == _r2_fold(key),
           f"fold {key}: route-1 and route-2 full decompositions agree "
           "(every graph-leg admissibility call is double-computed)")

    # ---- (12) hygiene: pure integers + the extended vocabulary fence ----
    with open(__file__, 'r') as fh:
        src_text = fh.read()
    tree = ast.parse(src_text)
    floats = [n for n in ast.walk(tree) if isinstance(n, ast.Constant)
              and isinstance(n.value, (float, complex))]
    ck(not floats,
       "zero float/complex constants in this module's AST (pure "
       "integer arithmetic; every division asserted exact)")
    msgs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == 'ck':
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) \
                        and isinstance(sub.value, str):
                    msgs.append(sub.value)
    stems = ('magnitude', 'tension', 'spectral', 'continuum', 'occupanc',
             'hold', 'quantum', 'selection', 'energ',
             'gluon')     # lane-added gauge-vocabulary stem (audit F2)
    hits = [(w, m) for m in msgs for w in stems if w in m.lower()]
    ck(len(msgs) >= 40 and not hits,
       f"vocabulary fence: the nine banked stems plus the lane-added "
       f"gauge-vocabulary stem have zero hits over {len(msgs)} "
       "check-message strings across BOTH checks (the charter's "
       "fences -- and this module adds: no gauge-group claim, no "
       "dynamics, no fixed-L statement)")
    fnames = [n.name for n in ast.walk(tree)
              if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    fhits = [(w, f) for f in fnames for w in stems if w in f.lower()]
    ck(len(fnames) >= 25 and not fhits,
       f"vocabulary fence EXTENDED to function names (audit fix F2): "
       f"zero stem hits over {len(fnames)} function definitions in "
       "this module's AST -- a fence-violating leg NAME can no longer "
       "self-certify clean around a message-only scan")

    passed = not fails
    return {
        'name': 'T_g2_fusion_screen_exhibit',
        'epistemic': ('P | instance-scoped at stated caps and walked '
                      'graphs: fusion facts on the stated 9-irrep '
                      'battery grid; graph facts at cap {1,7,14,27} on '
                      'the walked graphs (TT 1-3, claw 1-3, K4+tail '
                      '1-3; the tree control is the sibling check\'s); '
                      'nothing beyond -- beyond the battery grid the '
                      'constructed rules are computed where walked, '
                      'named where not'),
        'passed': passed,
        'tier': 4,
        'key_result': (
            'The G2 fusion rules CONSTRUCTED TWICE independently '
            'in-module -- route 1 Freudenthal (exact integer '
            'recursion, divisibility asserted every step) + '
            'Racah-Speiser/Klimyk; route 2 exact Weyl-character '
            'alternant division + greedy full-character subtraction, '
            'sharing only the declared lattice constants -- and '
            'cross-checked EXACTLY on all 81 ordered pairs of the '
            '9-irrep battery {1,7,14,27,64,77,77p,182,189}: dimension '
            'multiplicativity, commutativity, zero construction-flag '
            'trips, greedy soundness machine-checked (500+ support '
            'weights; audit fix F1), the Casimir trace identity on '
            'all 81 pairs with the dimension-preserving-sabotage '
            'control (audit fix F4).  Table pins: 7 (x) 7 = 1 + 7 + '
            '14 + 27 (all mult 1, the load-bearing channel); 7 (x) 14 '
            '= 7 + 27 + 64 (no trivial); 14 (x) 14 = 1 + 14 + 27 + 77 '
            "+ 77' (no 7); 1 in 7 (x) 7 (x) 7 mult EXACTLY 1; 7 in "
            '14 (x) 14 (x) 14 mult EXACTLY 1; Schur delta_ab over the '
            'battery; the 7 generates.  Graph legs at cap {1,7,14,27} '
            'on the banked model conventions: TT(1..3), source 7 -- '
            'the 7-triangle screen admissible, support 3, crossing no '
            'family cut, inside the exhaustive admissible set (12 '
            'configurations, constant in L); claw2/claw3 with 7 '
            'sources FULLY CONTAINABLE (4/4 configurations, witnesses '
            'located) -- the banked SU(3) pair-obstruction does NOT '
            'transfer: the trivial-center corollary walked; claw1 not '
            'contained there (geometry + cap fact, not an N-ality '
            'obstruction); K4+tail(1..3) -- the single 7 fully '
            'contained by the all-adjoint (all-14) screen on the 6 K4 '
            'edges, support 6 constant in L, 3306 admissible / 794 '
            'fully contained at each L (exhaustive).  Every screen '
            'statement existence-only at the stated cap on the walked '
            'geometry; every fold double-computed on both routes; '
            'kinematic admissibility only.'
        ),
        'dependencies': ['L_center_flux_exit'],
        'cross_refs': list(_CROSS_REFS),
        'artifacts': {
            'witnesses': ('7x7 = 1+7+14+27; 7x14 = 7+27+64 (no '
                          'trivial); 14x14 = 1+14+27+77+77p (no 7); '
                          '1 in 7x7x7 mult 1; 7 in 14x14x14 mult 1; '
                          'Schur delta_ab 81/81; C2(7)=12, C2(14)=24 '
                          '(module normalization), Casimir identity '
                          '81/81; TT screen support 3, counts 12/12/'
                          '12; claw2/claw3 counts 4/4 with contained '
                          'witnesses; claw1 all nonzero-tail; K4+tail '
                          'counts 3306/3306/3306 with 794 contained '
                          'at each L, the all-14 screen among them'),
            'premise_stack': ('lattice-model conventions (MODEL '
                              'DEFINITION, named; anchored live) + '
                              'pinned G2 conventions + battery/cap '
                              'scoping (9-irrep grid; cap {1,7,14,27} '
                              'on the walked graphs); A1 deliberately '
                              'not consumed (house precedent)'),
            'named_imports': ('beyond the battery grid the constructed '
                              'rules are computed where walked, named '
                              'where not (the banked module\'s '
                              'constructed-rule precedent); the '
                              'route-independence certificate is the '
                              'lane audit, cited not imported'),
            'kill_condition': ('any route disagreement on any battery '
                               'pair or graph-leg fold; a '
                               'construction-flag trip; a dimension- '
                               'or Casimir-blade failure; the '
                               '7-triangle or all-14 screen failing '
                               'recomputation or absent from the '
                               'exhaustive admissible set; count '
                               'non-constancy in L; 1 absent from '
                               '7 (x) 7 under either route; a '
                               'fence-stem hit in any check message '
                               'or function name'),
            'may_not_cite': ('screens are EXISTENCE statements at '
                             'stated caps on walked graphs, never '
                             'cited as selected/taken (billing/argmin '
                             'is the frustration module\'s, not '
                             'consumed); nothing beyond the walked '
                             'graphs and stated caps -- the counts '
                             '3306/794/12/4 are instance facts, no '
                             'graph-class characterization; no '
                             'gauge-group claim (R_SU_Nc_neq_3_killed '
                             'stands); no dynamics/gap/fixed-L/'
                             'reading sentence; the G2 intermediate '
                             'string untouchable -- the three-adjoint '
                             'channel and the K4 containment are '
                             'kinematic admissibility exhibits, never '
                             '"G2 breaks strings" dynamically; the '
                             'banked flux-exit MAY-NOT-CITE lines '
                             'travel with its pattern'),
            'audit_record': _AUDIT_RECORD,
            'lane_records': _LANE_RECORD,
        },
        'fail_reasons': fails,
        'n_checks': n_checks[0],
    }


_CHECKS = {
    'L_trivial_center_no_nality_obstruction':
        check_L_trivial_center_no_nality_obstruction,
    'T_g2_fusion_screen_exhibit': check_T_g2_fusion_screen_exhibit,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.environ.get(
        'APF_TREE',
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ok = True
    for _name, _fn in _CHECKS.items():
        _r = _fn()
        print(_r['name'], 'PASS' if _r['passed'] else 'FAIL',
              f"({_r['n_checks']} checks)")
        if not _r['passed']:
            ok = False
            for _f in _r['fail_reasons']:
                print('  -', _f)
    sys.exit(0 if ok else 1)
