"""Triality <-> flux correspondence: N-ality additivity IS the flux-exit
lemma's H-hom, computed as an identity of maps on the stated battery.

T_nality_additivity_is_hhom.  Composes check_T_center_order_parameter_triality
(gauge.py, [P], tier 1) with check_L_center_flux_exit (center_flux_exit.py,
[P_math | 3-item stack], tier 4) through their shared anchor
check_T_su2_string_cut_comovement -- all three consumed LIVE below.

STATEMENT.
  Identification leg (computed): the following three maps on SU(3) irrep
  labels are ONE map, and the triality parent's "N-ality additive under
  tensor product" (its derivation step (1)) is EXACTLY the flux-exit
  lemma's H-hom predicate for that map:
    A  (triality parent's substrate): boxes-mod-3 on the Young-diagram
       labeling -- irrep (p, q) has rows (p+q, q), total boxes n = p + 2q,
       grading n mod 3; gauge.py's stated convention "#boxes - #anti-boxes
       mod N, antibox = -1" reads the SAME residue as (p - q) mod 3.
    B  (flux-exit parent's map): the lemma's banked center charge,
       q(p, q) = (p - q) mod 3 (center_flux_exit.py's model statement),
       whose hom property is the named hypothesis H-hom.
    C  (fusion-reconstructed, no boxes anywhere): q_fusion(r) := k mod 3
       for any fundamental tensor power k containing r -- well-definedness
       is itself a computed check.
  A == B == C on all 16 irreps with p + 2q <= 6; additivity == hom on the
  256-product grid (p, q <= 3), 1632 constituents, 0 violations;
  determination: exactly 3 Z_3-valued fusion homs on the battery
  {trivial, triality, conjugate-triality}, and triality is the unique one
  with q(fund) = 1 -- both parents' shared convention, not a new one.

  Composed sentence (antecedent-first, the triality parent's own [P]
  pattern; audit fix F2 -- saturation lives HERE, never in the premise
  bar):
    AT IR SATURATION (antecedent, carried in-sentence, never discharged):
    an isolated colour charge's screenability grading -- N-ality -- IS, as
    a map on irrep labels, the center charge whose fusion-homomorphism
    property (H-hom) gates the banked lattice flux-exit dichotomy; the
    identity of maps and the additivity-is-hom property are computed on
    the stated battery, and the flux-exit necessity/sufficiency exhibits
    run on that same map at the walked caps.

CONSTRUCTION PROVENANCE (audit fix F3 -- no private-name imports at bank
time): SU(3) fusion and the charge map are CONSTRUCTED IN-MODULE, the
.416 precedent -- route A Gelfand-Tsetlin weight convolution with
lex-leading subtraction, route B Littlewood-Richardson tableau counting,
cross-checked on the 81 pairs to (2,2) with dimension counting on all 256
battery products.  AUDIT RECORD, cited not imported: the lane audit
settled fusion single-sourcing by TWO audit-independent routes sharing no
code path with this module or .416 (Freudenthal weight multiplicities +
Brauer-Klimyk; full-character Laurent product + iterated dominant-
character peeling -- audit_probe_1_indep_fusion.py, 16 checks, exit 0),
agreeing with the constructed rules on all 256 products; .416's own audit
certified third/fourth routes and the lex-leading-subtraction
triangularity.  The lane walker's read-only underscore imports are lane
record only; none appear here.

PREMISE STACK (the grade line's conditioning bar -- prices readings/
conventions/scoping ONLY; 4 items; the saturation conditional is in the
STATEMENT'S ANTECEDENT above, not here):
  1. Electric-basis model convention (flux-exit premise 1): the comovement
     anchor consumed live below -- P_structural_reading, verdict PARTIAL,
     four clauses, inherited never flattened.
  2. Per-vertex-singlet admissibility (flux-exit premise 2): the Gauss /
     interior-gauge-invariance reading is a named identification,
     computed nowhere.
  3. H-hom beyond the computed grids (flux-exit premise 3): the batteries
     here, in the lane, and in .416 are grid-computed, not a proof of it.
  4. Battery/cap scoping: map identity computed on 16 irreps to 6 boxes;
     hom property on the 256-product grid to (3,3); testbed legs on the
     walked graphs at cap p + q <= 2 only.
LOUDLY FLAGGED AS NEW: NOTHING.  The composition consumes only fusion
data both parents already stand on, plus the generator-choice observation
q(fund) = 1, which is both parents' existing convention (determination
leg).  No new reading, no new convention, no new hypothesis.

DEPENDENCY NOTE (the triangle, with the audit's precision note): the
comovement anchor -- flux-exit's premise 1 and sole dep -- already lists
check_T_center_order_parameter_triality in its OWN dependencies (its
clause (i) is the N-ality co-movement clause), so the triality parent is
already upstream of the flux-exit lemma through the anchor and this
composition closes a triangle in the dep graph rather than importing new
physics.  Precision: the pre-existing edge carries the N-ality partition
concept through the SU(2) family at reading grade; the SU(3)
identification content is THIS check's, not the triangle's.

KILL MODE (LOUD): an H-hom violation at any computed instance -- a
constituent of any fusion product under the constructed rule carrying
q != q(a) + q(b) mod N -- kills the identification AND (per .416's own
kill condition) the flux-exit instantiation at that N.  The two maps
disagreeing on ANY irrep (boxes vs fusion-derived vs the banked module
map) kills the correspondence outright.  Death of either parent kills the
composition: the comovement anchor failing or losing its PARTIAL/
four-clause shape; the triality check's saturation conditioning being
refuted; a fusion-route disagreement (GT vs LR) on the walked grids.  All
asserted 0 below and in the 46-check lane walker.

MAY-NOT-CITE (citation without the antecedent + the 4-item premise bar is
misciting):
  - [F1, affirmative, travels with any joint citation -- verbatim from
    the audit ruling:] "Rep-theoretic dressability (the triality parent's
    sufficiency step) and model-side screen existence are DIFFERENT
    predicates; screens are geometry-conditional (walked trees and the
    far-cycle family frustrate even t=0 sources —
    T_frustration_center_partition's computed SCREEN-SUPPORTING proviso).
    The correspondence identifies the GRADING MAP only, never the
    screening predicates; the proviso travels with any joint citation."
  - Everything on L_center_flux_exit's list travels wherever the flux
    side is cited: no cut-equality for arbitrary separating edge sets
    (delta(S)-scoped; the parent counterexample travels); screens are
    existence-only under the named cycle condition, never cited as
    selected; H-hom a named hypothesis beyond the computed grids; no
    graph generality beyond the executed per-edge derivation; the N = 2
    instance carries the SU(2) parent's own MAY-NOT-CITE lines; NO
    consumption by the confinement parent lane without its
    support-reading residual premise (the residue of record) NAMED; no
    SU(N > 3) claim; no magnitude/tension/spectral/continuum/dynamics
    claim; the composed confinement-reading sentence is NOT licensed.
  - The triality parent's fences travel wherever the order-parameter side
    is cited: conditional on saturation (in the ANTECEDENT -- never
    "confinement established"); no sigma / Lambda_QCD; order-parameter
    STRUCTURE only, not its dynamical non-vanishing; the holonomy
    expression stays the open gauge_fiber_automorphism_program.
  - The correspondence is a KINEMATIC IDENTITY OF INVARIANTS; it may NOT
    be cited as evidence that the lattice model describes the saturated
    phase, nor as progress on the mass gap, tension law, or continuum
    limit.
  - It may NOT be cited as extending sufficiency (root-lattice, all k)
    beyond the parent's [P] prose -- sufficiency is computed at dressing
    caps k <= 6 only.
  - The identification is battery-scoped: 16 irreps / (3,3) product grid.
    Beyond that, "additivity is H-hom" is exactly as hypothetical as
    H-hom itself.
  - The fixed-L partition claim stays DEAD (.417); nothing here revives
    it.
  - No citation without the antecedent + 4-item premise bar.

GRADE (split grade line, verbatim from the banking ruling):
[P_math | battery/cap scoping + H-hom named beyond grids —
identification leg; composed sentence P_structural | flux-exit 3-item
stack + battery/cap scoping — saturation conditional in the antecedent].
Expanded per the audit's grade ruling: P_math | battery/cap scoping (16
irreps to 6 boxes; 256-product grid to (3,3); H-hom named beyond the
computed grids) -- for the identification leg (map identity +
additivity-is-hom + determination); the composed order-parameter <->
flux-gate sentence P_structural | flux-exit 3-item stack (electric-basis
convention via live comovement anchor; per-vertex-singlet Gauss reading;
H-hom named beyond computed grids) + battery/cap scoping -- conditional
on IR saturation IN THE STATEMENT'S ANTECEDENT (the triality parent's
carried premise, never discharged here).  Tier 4.

This module banks the DISTILLED battery; the 46-check lane walker
(walk_triality_flux.py, exit 0, audit fixes F1-F4 carried) is the lane
record.  Recorded sentences below (the composed sentence, the premise
bar, the F1 proviso) are labeled as such and excluded from the computed
check count, per the audit's minor fix.

AUDIT RECORD (cited, not imported): AUDIT_REPORT.md, 2026-07-11,
LAND-WITH-FIXES 0.89, no kills; all four MAJOR fixes carried at code
level in the lane; fusion single-sourcing settled by two
audit-independent routes (audit_probe_1_indep_fusion.py); testbed legs
independently reproduced (audit_probe_2, own enumerator); mutation-hard
(audit_probe_3, 5/5 loud).

Lane record: The Turning (parked)/triality_flux_2026-07-11/
(walk_triality_flux.py, 46 checks, exit 0; WALK_NOTE.md v0.2;
AUDIT_REPORT.md LAND-WITH-FIXES 0.89).

v24.3.419 (2026-07-11): banked from the triality<->flux lane per the
principal's BANK ruling; banking shape adopted verbatim from the
certified WALK_NOTE v0.2 Section 7 entry.
"""

from itertools import combinations
import ast

# ---------------------------------------------------------------------------
# constructed SU(3) fusion, route A (Gelfand-Tsetlin weight convolution +
# lex-leading subtraction) and route B (Littlewood-Richardson tableau
# counting) -- constructed IN-MODULE per audit fix F3; no private-name
# imports from center_flux_exit
# ---------------------------------------------------------------------------
_GT = {}
_FLAG3 = [0]


def _gt_weights(p, q):
    key = (p, q)
    if key in _GT:
        return _GT[key]
    l1, l2 = p + q, q
    out = {}
    for m12 in range(l2, l1 + 1):
        for m22 in range(0, l2 + 1):
            for m11 in range(m22, m12 + 1):
                w = (m11, m12 + m22 - m11, l1 + l2 - m12 - m22)
                out[w] = out.get(w, 0) + 1
    _GT[key] = out
    return out


def _su3_dim(p, q):
    return (p + 1) * (q + 1) * (p + q + 2) // 2


_F3 = {}


def _su3_fuse(a, b):
    key = (a, b)
    if key in _F3:
        return _F3[key]
    wa, wb = _gt_weights(*a), _gt_weights(*b)
    P = {}
    for w1, m1 in wa.items():
        for w2, m2 in wb.items():
            w = (w1[0] + w2[0], w1[1] + w2[1], w1[2] + w2[2])
            P[w] = P.get(w, 0) + m1 * m2
    out = {}
    while P:
        top = max(P)
        m = P[top]
        if m <= 0 or not (top[0] >= top[1] >= top[2] >= 0):
            _FLAG3[0] += 1
            break
        lab = (top[0] - top[1], top[1] - top[2])
        out[lab] = out.get(lab, 0) + m
        pp, qq, s = lab[0], lab[1], top[2]
        for w, k in _gt_weights(pp, qq).items():
            ws = (w[0] + s, w[1] + s, w[2] + s)
            P[ws] = P.get(ws, 0) - m * k
            if P[ws] == 0:
                del P[ws]
    _F3[key] = out
    return out


def _lr_coeff(lam, mu, nu):
    if any(nu[i] < lam[i] for i in range(3)):
        return 0
    order = []
    for r in range(3):
        for c in range(nu[r] - 1, lam[r] - 1, -1):
            order.append((r, c))
    if sum(mu) != len(order):
        return 0
    T = {}
    counts = [0, 0, 0]
    total = [0]

    def rec(i):
        if i == len(order):
            if counts == list(mu):
                total[0] += 1
            return
        r, c = order[i]
        right = T.get((r, c + 1))
        above = T[(r - 1, c)] if (r > 0 and lam[r - 1] <= c < nu[r - 1]) \
            else None
        for e in range(3):
            v = e + 1
            if counts[e] >= mu[e]:
                continue
            if e > 0 and counts[e] + 1 > counts[e - 1]:
                continue
            if right is not None and v > right:
                continue
            if above is not None and v <= above:
                continue
            counts[e] += 1
            T[(r, c)] = v
            rec(i + 1)
            del T[(r, c)]
            counts[e] -= 1
    rec(0)
    return total[0]


def _su3_fuse_lr(a, b):
    lam = (a[0] + a[1], a[1], 0)
    mu = (b[0] + b[1], b[1], 0)
    tot = sum(lam) + sum(mu)
    out = {}
    for n1 in range(tot + 1):
        for n2 in range(min(n1, tot - n1) + 1):
            n3 = tot - n1 - n2
            if not (n1 >= n2 >= n3 >= 0):
                continue
            c = _lr_coeff(lam, mu, (n1, n2, n3))
            if c:
                out[(n1 - n2, n2 - n3)] = out.get((n1 - n2, n2 - n3), 0) + c
    return out


# ---------------------------------------------------------------------------
# the presentations of the charge map (A, B constructed here; C derived
# from fusion data inside the check)
# ---------------------------------------------------------------------------
def _q_boxes(lab):
    """Presentation A -- the triality parent's grading substrate: irrep
    (p, q) has Young rows (p+q, q), total boxes n = p + 2q; grading n mod
    3.  gauge.py's stated convention '#boxes - #anti-boxes mod N, antibox
    = -1' reads the same residue as presentation B (computed below)."""
    p, q = lab
    return (p + 2 * q) % 3


def _q_center(lab):
    """Presentation B -- the flux-exit lemma's banked center charge by its
    model statement: q(p, q) = (p - q) mod 3 (constructed here, not
    imported; audit fix F3)."""
    p, q = lab
    return (p - q) % 3


def _fold(dec, b, fuse=_su3_fuse):
    new = {}
    for x, m in dec.items():
        for c, k in fuse(x, b).items():
            new[c] = new.get(c, 0) + m * k
    return new


def _hom_violations(fuse, qmap, pairs, N=3):
    """(violations, constituents) over a product battery: the
    additivity-is-hom predicate, one constituent at a time."""
    nv = nc = 0
    for a, b in pairs:
        t = (qmap(a) + qmap(b)) % N
        for c, m in fuse(a, b).items():
            if m > 0:
                nc += 1
                if qmap(c) % N != t:
                    nv += 1
    return nv, nc


# ---------------------------------------------------------------------------
# testbed machinery, constructed in-module (the banked model's own
# conventions: oriented edges, label r at head / conj(r) at tail,
# boundary unconstrained, per-vertex-singlet admissibility)
# ---------------------------------------------------------------------------
_CONJ = lambda t: (t[1], t[0])
_UNIT = (0, 0)
_LAB3 = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]     # cap p+q <= 2
_SMC = {}


def _singlet(labels):
    key = tuple(sorted(labels))
    if key in _SMC:
        return _SMC[key]
    dec = {_UNIT: 1}
    for b in sorted(labels):
        dec = _fold(dec, b)
    m = dec.get(_UNIT, 0)
    _SMC[key] = m
    return m


def _content(g, cfg, v):
    out = []
    for i, (x, y) in enumerate(g['E']):
        if y == v:
            out.append(cfg[i])
        if x == v:
            out.append(_CONJ(cfg[i]))
    s = g['sources'].get(v)
    if s is not None and s != _UNIT:
        out.append(s)
    return tuple(out)


def _enum(g, labels=_LAB3):
    E = g['E']
    inc = {v: [i for i, (x, y) in enumerate(E) if v in (x, y)]
           for v in g['V']}
    interior = [v for v in g['V'] if v not in g['boundary']]
    comp = {}
    for v in interior:
        if inc[v]:
            comp.setdefault(max(inc[v]), []).append(v)
        elif _singlet(_content(g, (), v)) == 0:
            return []
    out = []
    cfg = [_UNIT] * len(E)

    def rec(i):
        if i == len(E):
            out.append(tuple(cfg))
            return
        for lab in labels:
            cfg[i] = lab
            if all(_singlet(_content(g, cfg, v)) > 0
                   for v in comp.get(i, ())):
                rec(i + 1)
    rec(0)
    return out


def _path(L, src):
    return {'V': [f"v{i}" for i in range(L + 1)],
            'E': [(f"v{i}", f"v{i+1}") for i in range(L)],
            'boundary': frozenset([f"v{L}"]), 'sources': {'v0': src},
            'nested': [frozenset(f"v{j}" for j in range(i))
                       for i in range(1, L + 1)], 'L': L}


def _tt(L, src):
    V = ['t0', 'w1', 'w2'] + [f"p{i}" for i in range(1, L + 1)]
    E = [('t0', 'w1'), ('w1', 'w2'), ('w2', 't0'), ('t0', 'p1')]
    for i in range(1, L):
        E.append((f"p{i}", f"p{i+1}"))
    return {'V': V, 'E': E, 'boundary': frozenset([f"p{L}"]),
            'sources': {'t0': src},
            'nested': [frozenset(['t0', 'w1', 'w2']
                                 + [f"p{j}" for j in range(1, i)])
                       for i in range(1, L + 1)], 'L': L}


def _claw(n_src):
    V = [f"s{i}" for i in range(n_src)] + ['c', 'x1']
    E = [(f"s{i}", 'c') for i in range(n_src)] + [('c', 'x1')]
    return {'V': V, 'E': E, 'boundary': frozenset(['x1']),
            'sources': {f"s{i}": (1, 0) for i in range(n_src)},
            'nested': [frozenset([f"s{i}" for i in range(n_src)] + ['c'])],
            'L': 1}


def _cut_law(g, cfgs, qmap, N=3):
    """(bad_law, bad_exit, n_families) with the SUBSTITUTED charge map
    qmap: cut law (outward flux charge == enclosed source charge mod N)
    and flux exit (>= 1 charge-nonzero cut edge when a source-enclosing
    delta(S) has nonzero enclosed charge), over ALL nonempty interior
    vertex sets S x all admissible configurations."""
    interior = [v for v in g['V'] if v not in g['boundary']]
    E = g['E']
    fams = []
    for r in range(1, len(interior) + 1):
        for comb in combinations(interior, r):
            S = frozenset(comb)
            cut = [(i, (1 if x in S else -1)) for i, (x, y) in enumerate(E)
                   if (x in S) != (y in S)]
            sq = sum(qmap(g['sources'][v]) for v in S
                     if v in g['sources']) % N
            fams.append((S, cut, sq))
    srcverts = frozenset(g['sources'])
    bad_law = bad_exit = 0
    for cfg in cfgs:
        for S, cut, sq in fams:
            flux = sum(sgn * qmap(cfg[i]) for i, sgn in cut)
            if (flux - sq) % N:
                bad_law += 1
            if srcverts <= S and sq % N:
                if not any(qmap(cfg[i]) % N for i, _ in cut):
                    bad_exit += 1
    return bad_law, bad_exit, len(fams)


# ---------------------------------------------------------------------------
# recorded sentences (labeled; excluded from the computed check count per
# the audit's minor fix) and pinned artifacts
# ---------------------------------------------------------------------------
_COMPOSED_SENTENCE = (
    'AT IR SATURATION (antecedent, carried in-sentence, never discharged): '
    'an isolated colour charge\'s screenability grading -- N-ality -- IS, '
    'as a map on irrep labels, the center charge whose fusion-homomorphism '
    'property (H-hom) gates the banked lattice flux-exit dichotomy; the '
    'identity of maps and the additivity-is-hom property are computed on '
    'the stated battery, and the flux-exit necessity/sufficiency exhibits '
    'run on that same map at the walked caps.')

_COMPOSED_ANTECEDENT = (
    'AT IR SATURATION (the antecedent, carried in-sentence exactly as the '
    'triality parent carries it; never discharged, never priced as a bar '
    'item)')

_PREMISE_BAR = (
    'electric-basis model convention (flux-exit premise 1; comovement '
    'anchor consumed live, P_structural_reading, PARTIAL four clauses '
    'inherited never flattened)',
    'per-vertex-singlet admissibility (flux-exit premise 2; Gauss '
    'reading a named identification, computed nowhere)',
    'H-hom named beyond the computed grids (flux-exit premise 3; the '
    'batteries here and in .416 are grid-computed, not a proof of it)',
    'battery/cap scoping: map identity computed on 16 irreps to 6 '
    'boxes; hom property on the 256-product grid to (3,3); testbed '
    'legs on the walked graphs at cap p+q <= 2 ONLY',
)

_F1_PROVISO = (
    'Rep-theoretic dressability (the triality parent\'s sufficiency '
    'step) and model-side screen existence are DIFFERENT predicates; '
    'screens are geometry-conditional (walked trees and the far-cycle '
    'family frustrate even t=0 sources — '
    'T_frustration_center_partition\'s computed SCREEN-SUPPORTING '
    'proviso). The correspondence identifies the GRADING MAP only, '
    'never the screening predicates; the proviso travels with any '
    'joint citation.')

_PINNED_DEPTHS = {(0, 0): 0, (1, 1): 1, (3, 0): 2, (0, 3): 2, (2, 2): 2,
                  (4, 1): 3, (6, 0): 4}


def check_T_nality_additivity_is_hhom():
    """T_nality_additivity_is_hhom: the triality parent's N-ality
    additivity IS the flux-exit lemma's H-hom -- one map, three
    presentations, computed on the stated battery, with the flux-exit
    gate legs re-run on the substituted fusion-derived charge.  See the
    module docstring for the statement, premise stack, kill mode,
    MAY-NOT-CITE fences (F1 proviso included), and the grade line.  This
    is the DISTILLED battery; the 46-check lane walker is the lane
    record."""
    from apf.gauge import check_T_center_order_parameter_triality
    from apf.center_flux_exit import check_L_center_flux_exit
    from apf.su2_string_cut_testbed import (
        check_T_su2_string_cut_comovement,
    )

    fails = []
    n_checks = [0]
    n_recorded = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        n_checks[0] += 1

    def rec_sentence(cond, msg):
        # recorded sentence, NOT a computation; counted separately per
        # the audit's minor fix (banking check counts exclude these)
        if not cond:
            fails.append(msg)
        n_recorded[0] += 1

    # ---- (0) all three dependencies consumed LIVE ------------------------
    rt = check_T_center_order_parameter_triality()
    ck(rt.get('passed') is True and rt.get('epistemic') == 'P'
       and set(rt.get('dependencies')) == {'T_confinement', 'L_epsilon*',
                                           'L_nc'},
       "dep 1 LIVE: check_T_center_order_parameter_triality passes, grade "
       "[P], deps {T_confinement, L_epsilon*, L_nc} as banked -- its "
       "conditional-on-saturation carriage travels into this statement's "
       "ANTECEDENT")

    rf = check_L_center_flux_exit()
    ck(rf.get('passed') is True
       and rf.get('epistemic', '').startswith('P_math |')
       and rf.get('dependencies') == ['T_su2_string_cut_comovement']
       and rf.get('n_checks', 0) >= 500,
       "dep 2 LIVE: check_L_center_flux_exit passes, grade line "
       "'P_math | ...' carried, sole dep T_su2_string_cut_comovement -- "
       "its 3-item premise stack travels as bar items 1-3")

    rc = check_T_su2_string_cut_comovement()
    ck(rc.get('passed') is True and rc.get('verdict') == 'PARTIAL'
       and rc.get('epistemic') == 'P_structural_reading'
       and 'check_T_center_order_parameter_triality'
       in rc.get('dependencies', []),
       "dep 3 LIVE: T_su2_string_cut_comovement PARTIAL "
       "(P_structural_reading, four clauses, never flattened) and its dep "
       "list CONTAINS the triality check -- the composition closes a "
       "dep-graph triangle; the SU(3) identification content is this "
       "check's, not the triangle's (audit precision note)")

    # ---- (1) constructed fusion: route cross-check + dimension count -----
    B_boxes = sorted((p, q) for p in range(7) for q in range(4)
                     if p + 2 * q <= 6)
    ck(len(B_boxes) == 16 and (1, 0) in B_boxes and (1, 1) in B_boxes
       and (3, 0) in B_boxes and (0, 3) in B_boxes and (6, 0) in B_boxes,
       "battery pinned: all 16 SU(3) irreps with box count p + 2q <= 6 "
       "(through 6 boxes, beyond the charter's 3-box minimum)")

    small = [(p, q) for p in range(3) for q in range(3)]
    ck(all(_su3_fuse(a, b) == _su3_fuse_lr(a, b)
           for a in small for b in small) and _FLAG3[0] == 0,
       "in-module fusion (audit fix F3): GT-convolution route == "
       "LR-tableau route on all 81 pairs to (2,2), zero subtraction-flag "
       "trips (the .416 construction precedent; the audit's two "
       "independent routes -- Freudenthal/Brauer-Klimyk and "
       "character-peeling -- agreed on all 256 products, cited not "
       "imported)")
    BP = [(p, q) for p in range(4) for q in range(4)]
    pairs = [(a, b) for a in BP for b in BP]
    ck(all(sum(m * _su3_dim(*c) for c, m in _su3_fuse(a, b).items())
           == _su3_dim(*a) * _su3_dim(*b) for a, b in pairs),
       "dimension counting on all 256 battery products (exact integers) "
       "-- construction corroboration")

    # ---- (2) leg 1: three-presentation map identity ----------------------
    ck(all(_q_boxes(r) == _q_center(r) for r in B_boxes),
       "MAP IDENTITY leg (i): boxes-mod-3 (Young rows (p+q, q), n = p+2q; "
       "gauge.py's '#boxes - #anti-boxes' convention reads the same "
       "residue) == the flux-exit lemma's banked center charge (p - q) "
       "mod 3 on ALL 16 battery irreps")

    KMAX = 8
    powers = [{(0, 0): 1}]
    for _ in range(KMAX):
        powers.append(_fold(powers[-1], (1, 0)))
    q_fusion = {}
    well_defined = True
    minpow_is_boxes = True
    for r in B_boxes:
        K = [k for k in range(KMAX + 1) if powers[k].get(r, 0) > 0]
        if not K:
            well_defined = False
            continue
        if any(k % 3 != K[0] % 3 for k in K):
            well_defined = False
        if min(K) != r[0] + 2 * r[1]:
            minpow_is_boxes = False
        q_fusion[r] = K[0] % 3
    ck(well_defined and len(q_fusion) == 16,
       "presentation C RECONSTRUCTED from fusion decompositions alone: "
       "for every battery irrep r the set of fundamental tensor powers "
       "k <= 8 containing r is nonempty and constant mod 3 -- q_fusion(r) "
       ":= k mod 3 is WELL-DEFINED with no reference to boxes")
    ck(minpow_is_boxes,
       "corroboration: the MINIMAL fundamental power containing r equals "
       "the box count p + 2q for every battery irrep (boxes labeling "
       "recovered from fusion, not assumed)")
    ck(all(q_fusion[r] == _q_boxes(r) for r in B_boxes),
       "MAP IDENTITY leg (ii), THE COMPUTED IDENTIFICATION: q_fusion == "
       "boxes-mod-3 == the flux-exit charge on ALL 16 battery irreps -- "
       "the triality grading and the flux-exit H-hom charge are ONE map, "
       "exhibited from each parent's own data")

    # ---- (3) leg 1: additivity IS the hom property + determination -------
    nv, nc = _hom_violations(_su3_fuse, _q_boxes, pairs)
    ck(nv == 0 and nc == 1632,
       f"ADDITIVITY-IS-H-HOM computed: over all 256 products from the "
       f"16-label grid (p, q <= 3, a superset of the .416 battery's (2,2) "
       f"grid), EVERY constituent carries q(c) == q(a) + q(b) mod 3 "
       f"({nc} constituents, {nv} violations; audit recount exactly 1632) "
       "-- the triality check's derivation step (1) is EXACTLY the "
       "flux-exit lemma's H-hom predicate, constituent by constituent")

    cands = {v: (lambda lab, v=v: (v * (lab[0] + 2 * lab[1])) % 3)
             for v in (0, 1, 2)}
    cand_ok = all(_hom_violations(_su3_fuse, cands[v], pairs)[0] == 0
                  for v in (0, 1, 2))
    distinct = len({tuple(cands[v](r) for r in B_boxes)
                    for v in (0, 1, 2)}) == 3
    conj_match = all(cands[2](r) == _q_center(_CONJ(r)) for r in B_boxes)
    ck(cand_ok and distinct and conj_match
       and cands[1]((1, 0)) == 1 and cands[0]((1, 0)) == 0
       and cands[2]((1, 0)) == 2,
       "DETERMINATION -- no hidden map choice: any Z_3-valued fusion hom "
       "is determined on the battery by its value on the fundamental "
       "(every battery irrep sits in a fundamental power at exponents "
       "constant mod 3, so the hom property forces q(r) = boxes(r) * "
       "q(fund)); EXACTLY 3 candidates {trivial, triality, "
       "conjugate-triality}, all pass the 256-product hom battery, "
       "pairwise distinct, the third computed == triality-of-the-"
       "conjugate; triality is the unique candidate with q(fund) = 1 -- "
       "both parents' shared convention, not a new one")

    # ---- (4) gauge.py's table + steps (2)-(4) as fusion facts -------------
    named = {'singlet': (0, 0), 'fundamental': (1, 0), 'antifund': (0, 1),
             'adjoint8': (1, 1), 'diquark6': (2, 0), 'decuplet10': (3, 0)}
    gauge_table = {'singlet': 0, 'fundamental': 1, 'antifund': 2,
                   'adjoint8': 0, 'diquark6': 2, 'meson': 0, 'baryon': 0,
                   'decuplet10': 0}
    meson = _su3_fuse((1, 0), (0, 1))
    bar = _fold(_fold({(1, 0): 1}, (1, 0)), (1, 0))
    ck(all(gauge_table[k] == _q_boxes(lab) for k, lab in named.items())
       and meson == {(0, 0): 1, (1, 1): 1}
       and all(_q_boxes(c) == 0 for c in meson)
       and bar == {(0, 0): 1, (1, 1): 2, (3, 0): 1}
       and all(_q_boxes(c) == 0 for c in bar)
       and bar.get((0, 0), 0) == 1,
       "gauge.py's hand-pinned N-ality table DERIVED, not trusted: every "
       "simple-irrep entry reproduced from boxes; 'meson' from 3 x 3bar = "
       "1 + 8 (all t = 0); 'baryon' from 3 x 3 x 3 = 1 + 8 + 8 + 10, "
       "EXACTLY ONE singlet (fusion-computed, not dict arithmetic)")

    adj = (1, 1)
    dress_ok = True
    for r in B_boxes:
        dec = {r: 1}
        for k in range(4):
            for c, m in dec.items():
                if m > 0 and _q_boxes(c) != _q_boxes(r):
                    dress_ok = False
            dec = _fold(dec, adj)
    ck(dress_ok,
       "gauge.py step (2) COMPUTED from fusion: adjoint dressing (k <= 3) "
       "preserves boxes-mod-3 on EVERY constituent for all 16 battery "
       "irreps (center-blindness of the gauge field as a fusion fact)")

    zero_batt = [r for r in B_boxes if _q_boxes(r) == 0]
    min_k = {}
    for r in zero_batt:
        dec = {r: 1}
        found = None
        for k in range(7):
            if dec.get((0, 0), 0) > 0:
                found = k
                break
            dec = _fold(dec, adj)
        min_k[r] = found
    ck(min_k == _PINNED_DEPTHS,
       f"gauge.py step (4) sufficiency COMPUTED AT CAP: every triality-0 "
       f"battery irrep reaches the singlet by adjoint dressing at some "
       f"k <= 6; minimal depths pinned PER THE AUDIT'S F4 CORRECTION "
       f"{sorted(min_k.items())} -- incl. (4,1): 3 and (6,0): 4; the "
       "all-k root-lattice sentence stays the parent's [P] prose, NOT "
       "re-derived here")
    nec_ok = True
    for r in [r for r in B_boxes if _q_boxes(r) != 0]:
        dec = {r: 1}
        for k in range(5):
            if dec.get((0, 0), 0) > 0:
                nec_ok = False
            dec = _fold(dec, adj)
    ck(nec_ok,
       "gauge.py step (3) necessity COMPUTED AT CAP: no triality-nonzero "
       "battery irrep reaches the singlet under adjoint^k, k <= 4 "
       "(cap-free by the hom property, which bar item 3 prices as named "
       "beyond the grids)")

    # ---- (5) leg 2: the flux-exit gate legs on the SUBSTITUTED map -------
    qf = lambda lab: q_fusion[lab] if lab in q_fusion else _q_boxes(lab)
    ck(all(qf(lab) == _q_center(lab) for lab in _LAB3),
       "gate identity on the walked label set: the fusion-derived charge "
       "== the flux-exit gate map on all 6 cap p + q <= 2 labels -- the "
       "invariant substituted below is leg 1's, not a re-import")

    for L in (1, 2):
        g = _path(L, (1, 0))
        cfgs = _enum(g)
        bl, be, nf = _cut_law(g, cfgs, qf)
        minnz = min(sum(1 for x in cfg if qf(x) % 3) for cfg in cfgs)
        ck(bl == 0 and be == 0 and len(cfgs) > 0 and minnz == L
           and tuple([(1, 0)] * L) in cfgs,
           f"[path{L}, (1,0) source] cut law AND flux exit verified with "
           f"the leg-1 fusion-derived charge substituted ({len(cfgs)} "
           f"admissible configurations x {nf} interior delta(S)); "
           f"admissible-set minimum of charge-nonzero links EXACTLY "
           f"L = {L}, exact-L string witness present -- composition exact "
           "at the level of the shared invariant, not an analogy")

    g3 = _claw(3)
    cfg3 = _enum(g3)
    bl3, be3, nf3 = _cut_law(g3, cfg3, qf)
    wit = ((1, 0), (1, 0), (1, 0), (0, 0))
    tot3 = sum(qf(s) for s in g3['sources'].values()) % 3
    ck(bl3 == 0 and be3 == 0 and tot3 == 0 and wit in cfg3
       and len(cfg3) == 2 and all(c[3] in ((0, 0), (1, 1)) for c in cfg3),
       f"[claw3, baryon exhibit] cut law verified with the substituted "
       f"charge ({nf3} interior delta(S)); three (1,0) sources sum to "
       "triality 0 under the fusion-derived map, the fully contained "
       "witness exists, admissible set exactly {witness, adjoint-dressed "
       "tail} as banked (exhaustive at cap p + q <= 2)")

    g2 = _claw(2)
    cfg2 = _enum(g2)
    bl2, be2, nf2 = _cut_law(g2, cfg2, qf)
    tot2 = sum(qf(s) for s in g2['sources'].values()) % 3
    ck(bl2 == 0 and be2 == 0 and tot2 == 2 and len(cfg2) > 0
       and all(qf(c[2]) % 3 == 2 for c in cfg2)
       and _su3_fuse((1, 0), (1, 0)).get((0, 0), 0) == 0,
       f"[claw2, pair exhibit] cut law verified with the substituted "
       f"charge ({nf2} interior delta(S)); two (1,0) sources sum to "
       "triality 2 and EVERY admissible configuration carries charge-2 "
       "flux out the tail; 3 x 3 has no singlet -- pairs do not screen, "
       "triples do (walked claws, stated cap only)")

    gt = _tt(2, (1, 1))
    cfgt = _enum(gt)
    blt, bet, nft = _cut_law(gt, cfgt, qf)
    screen = tuple([(1, 1)] * 3 + [(0, 0)] * 2)
    ck(blt == 0 and bet == 0 and screen in cfgt and len(cfgt) == 11
       and qf((1, 1)) == 0,
       f"[tt2, adjoint source] cut law verified with the substituted "
       f"charge ({nft} interior delta(S)); the bounded triangle screen "
       "exists, admissible count 11 (the banked pin recomputed), and the "
       "source is triality-0 under the fusion-derived map "
       "(screen-existence condition named, existence only)")

    ck(all(qf(r) != 0 for r in [(1, 0), (0, 1), (2, 0)])
       and all(_singlet(_content(dict(_path(2, None), sources={'v0': src}),
                                 ((0, 0), (0, 0)), 'v0')) == 0
               for src in [(1, 0), (0, 1), (2, 0)]),
       "negative control (unpassivatable side): triality-nonzero sources "
       "with all-trivial links are inadmissible at the source vertex -- "
       "the invariant that FORCES billed crossing is leg 1's map")

    # ---- (6) F1 computed divergence (audit fix F1, computed side) ---------
    div_ok = True
    for L in (1, 2, 3):
        g = _path(L, (1, 1))
        cfgs = _enum(g)
        if not cfgs:
            div_ok = False
        cuts = [frozenset(i for i, (x, y) in enumerate(g['E'])
                          if (x in S) != (y in S)) for S in g['nested']]
        for cfg in cfgs:
            for cut in cuts:
                if not any(cfg[i] != (0, 0) for i in cut):
                    div_ok = False
    ck(div_ok and min_k[(1, 1)] == 1,
       "F1 COMPUTED DIVERGENCE: the t = 0 adjoint source is "
       "rep-theoretically dressable (minimal adjoint depth 1, leg 1) yet "
       "on the walked path TREES (L = 1..3) EVERY admissible "
       "configuration carries a non-trivial label across EVERY "
       "nested-family cut -- no bounded screen exists (support grows with "
       "L); dressability and model-side screen existence are DIFFERENT "
       "predicates, diverging on walked instances (the .417 "
       "SCREEN-SUPPORTING proviso's tree side, recomputed here)")

    # ---- (7) the battery can fail: negative controls ----------------------
    def fuse_bad(a, b):
        out = dict(_su3_fuse(a, b))
        spur = (a[0] + b[0] + 1, a[1] + b[1])
        out[spur] = out.get(spur, 0) + 1
        return out
    nvb, _ = _hom_violations(fuse_bad, _q_boxes,
                             [(a, b) for a in small for b in small])
    sab_bad = sum(1 for a in small for b in small
                  if sum(m * _su3_dim(*c)
                         for c, m in fuse_bad(a, b).items())
                  == _su3_dim(*a) * _su3_dim(*b))
    ck(nvb > 0 and sab_bad == 0,
       f"negative control: a corrupted fusion rule (spurious constituent "
       f"injected) is CAUGHT by the hom battery ({nvb} violations on the "
       "(2,2) grid) AND fails dimension counting on ALL 81 grid pairs -- "
       "both leg-1 gates are live, not theater")
    q_bad = lambda lab: lab[0] % 3
    nvc, _ = _hom_violations(_su3_fuse, q_bad,
                             [(a, b) for a in small for b in small])
    bl_bad, _, _ = _cut_law(g3, cfg3, q_bad)
    ck(any(q_bad(r) != q_fusion[r] for r in B_boxes) and nvc > 0
       and bl_bad > 0,
       f"negative control: a broken charge map (p mod 3, dropping the "
       f"antibox slot) is CAUGHT by the map-identity check, by the hom "
       f"battery ({nvc} violations), AND breaks the cut law on the walked "
       f"claw3 testbed ({bl_bad} violations) -- leg 2's gate check is "
       "live, not decorative")

    # ---- (8) recorded sentences (labeled; not computations) ---------------
    rec_sentence(len(_PREMISE_BAR) == 4
                 and _COMPOSED_SENTENCE.startswith('AT IR SATURATION')
                 and 'ANTECEDENT' in _COMPOSED_ANTECEDENT.upper(),
                 "recorded sentence (not a computation): the composed "
                 "sentence carries the saturation conditional in its "
                 "ANTECEDENT (audit fix F2, the triality parent's own [P] "
                 "pattern); the premise bar is exactly 4 items pricing "
                 "readings/conventions/scoping only; NOTHING NEW is "
                 "flagged by the composition")
    rec_sentence('DIFFERENT predicates' in _F1_PROVISO
                 and 'SCREEN-SUPPORTING' in _F1_PROVISO
                 and 'GRADING MAP only' in _F1_PROVISO,
                 "recorded sentence (not a computation): the F1 geometry "
                 "proviso pinned verbatim from the audit ruling; it is a "
                 "MAY-NOT-CITE line and travels affirmatively with any "
                 "joint citation of the correspondence and either "
                 "parent's screening content")
    rec_sentence(True,
                 "recorded sentence (not a computation): the "
                 "correspondence is a KINEMATIC IDENTITY OF INVARIANTS; "
                 "it licenses NO dynamics, NO string-law, NO N > 3 "
                 "statement, NO fixed-L statement (dead), and does NOT "
                 "discharge the antecedent or the Gauss reading of "
                 "either parent")

    # ---- (9) hygiene -------------------------------------------------------
    with open(__file__, 'r') as fh:
        tree = ast.parse(fh.read())
    floats = [n for n in ast.walk(tree) if isinstance(n, ast.Constant)
              and isinstance(n.value, (float, complex))]
    ck(not floats,
       "hygiene: zero float/complex constants in this module's AST "
       "(exact integer arithmetic only)")
    stems = ('magnitude', 'tension', 'spectral', 'continuum', 'occupanc',
             'hold', 'quantum', 'selection', 'energ')
    msgs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in ('ck', 'rec_sentence'):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) \
                        and isinstance(sub.value, str):
                    msgs.append(sub.value)
    hits = [(w, m[:40]) for m in msgs for w in stems if w in m.lower()]
    ck(len(msgs) >= 25 and not hits,
       f"hygiene: vocabulary fence (nine stems, zero hits over "
       f"{len(msgs)} check-message strings) -- no dynamics vocabulary "
       "enters the composed statement")

    passed = not fails
    return {
        'name': 'T_nality_additivity_is_hhom',
        'epistemic': ('P_math | battery/cap scoping + H-hom named beyond '
                      'grids — identification leg; composed sentence '
                      'P_structural | flux-exit 3-item stack + battery/cap '
                      'scoping — saturation conditional in the antecedent'),
        'passed': passed,
        'tier': 4,
        'key_result': _COMPOSED_SENTENCE,
        'dependencies': ['T_center_order_parameter_triality',
                         'L_center_flux_exit',
                         'T_su2_string_cut_comovement'],
        'cross_refs': ['T_frustration_center_partition',
                       'T_confinement',
                       'T_su2_string_cut_native_algebra',
                       'T_colour_contextuality_is_kstring_spectrum_blind'],
        'artifacts': {
            'battery': {str(r): {'boxes': r[0] + 2 * r[1],
                                 'min_fund_power': r[0] + 2 * r[1],
                                 'q': q_fusion[r]} for r in B_boxes},
            'constituent_counts': {'su3_grid_(3,3)': (nc, nv),
                                   'su2_pairs_to_12_lane_record':
                                       (819, 0)},
            'determination': ('exactly 3 Z_3-valued fusion homs on the '
                              'battery: {trivial, triality, '
                              'conjugate-triality}; triality unique with '
                              'q(fund) = 1 (both parents\' shared '
                              'convention)'),
            'min_dressing_depths': {str(k): v for k, v in
                                    sorted(min_k.items())},
            'testbed_pins': ('path L=1..2 (1,0): cut law + exit 0 '
                             'violations, min nonzero == L, exact-L '
                             'witness; claw3: admissible set exactly '
                             '{witness, adjoint-dressed tail}; claw2: '
                             'all configurations carry charge-2 flux '
                             'out; tt2 (1,1): screen present, count 11; '
                             'lane record extends paths to L=3 and tt '
                             'counts (11, 11, 11)'),
            'composed_antecedent': _COMPOSED_ANTECEDENT,
            'premise_bar': list(_PREMISE_BAR),
            'f1_divergence': ('COMPUTED: the t=0 adjoint source is '
                              'dressable (minimal depth 1) yet '
                              'unscreenable on the walked path trees '
                              'L=1..3 -- every admissible configuration '
                              'crosses every nested-family cut'),
            'may_not_cite': (_F1_PROVISO + ' || Everything on '
                             'L_center_flux_exit\'s list travels wherever '
                             'the flux side is cited, incl. explicitly: '
                             'no consumption by the confinement parent '
                             'lane without its support-reading residual '
                             'premise (the residue of record) NAMED; no '
                             'cut-equality for arbitrary separating edge '
                             'sets; screens existence-only; H-hom named '
                             'beyond grids; no SU(N>3); no magnitude/'
                             'tension/spectral/continuum/dynamics claim; '
                             'the composed confinement-reading sentence '
                             'not licensed. || The triality parent\'s '
                             'fences travel: saturation in the ANTECEDENT '
                             'only; no sigma/Lambda_QCD; order-parameter '
                             'STRUCTURE not dynamical non-vanishing; '
                             'holonomy stays the open '
                             'gauge_fiber_automorphism_program. || '
                             'Kinematic identity of invariants only: not '
                             'evidence the lattice model describes the '
                             'saturated phase; no mass-gap/tension-law/'
                             'continuum progress; sufficiency computed at '
                             'dressing caps k <= 6 only; battery-scoped '
                             '(16 irreps / (3,3) grid) -- beyond that '
                             'additivity-is-H-hom is exactly as '
                             'hypothetical as H-hom; fixed-L stays DEAD '
                             '(.417); no citation without the antecedent '
                             '+ 4-item premise bar.'),
            'kill_mode': ('an H-hom violation at any computed instance '
                          '(kills the identification AND the flux-exit '
                          'instantiation at that N, per .416\'s own kill '
                          'condition); the maps disagreeing on any irrep; '
                          'death of either parent (anchor losing PARTIAL/'
                          'four-clause shape; saturation conditioning '
                          'refuted; GT-vs-LR route disagreement on the '
                          'walked grids)'),
            'audit_record': ('AUDIT_REPORT.md 2026-07-11 LAND-WITH-FIXES '
                             '0.89, no kills; fixes F1-F4 carried at code '
                             'level in the lane; fusion single-sourcing '
                             'settled by two audit-independent routes '
                             '(Freudenthal-weights/Brauer-Klimyk + '
                             'full-character/dominant-peeling, '
                             'audit_probe_1_indep_fusion.py 16 checks '
                             'exit 0); testbeds independently reproduced '
                             '(audit_probe_2); mutation-hard '
                             '(audit_probe_3, 5/5 loud)'),
            'lane_record': ('The Turning (parked)/'
                            'triality_flux_2026-07-11/ '
                            '(walk_triality_flux.py 46 checks exit 0; '
                            'WALK_NOTE.md v0.2; AUDIT_REPORT.md)'),
            'version': 'v24.3.419 (2026-07-11)',
        },
        'fail_reasons': fails,
        'n_checks': n_checks[0],
        'n_recorded_sentences': n_recorded[0],
    }


_CHECKS = {'T_nality_additivity_is_hhom': check_T_nality_additivity_is_hhom}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.environ.get('APF_TREE', '/home/claude/apf-codebase'))
    r = check_T_nality_additivity_is_hhom()
    print(r['name'], 'PASS' if r['passed'] else 'FAIL',
          f"({r['n_checks']} computed checks + "
          f"{r['n_recorded_sentences']} recorded sentences)")
    if not r['passed']:
        for f in r['fail_reasons']:
            print('  -', f)
    sys.exit(0 if r['passed'] else 1)
