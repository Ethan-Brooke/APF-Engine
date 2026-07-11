"""Center-generic flux exit: the Z_N lattice Gauss cut law and flux-exit
theorem under the named fusion-homomorphism hypothesis, with SU(2)/Z_2 and
SU(3)/Z_3 as computed instances and the baryon containment exhibit.

L_center_flux_exit.  THE MODEL (part of the claim, named in full): a
finite graph G = (V, E) with a distinguished boundary vertex set; boundary
vertices are NOT vertex-rule-constrained (flux may end there).  Edges are
ORIENTED ordered pairs (tail, head); an edge with irrep label r is seen as
r at its HEAD and as conj(r) at its TAIL (named model call; SU(2)
self-conjugacy, computed, collapses this to the parent's unoriented
model).  Self-loops contribute BOTH endpoint slots to their own vertex and
are never cut edges; multi-edges are independent edges (named model
calls).  Optional static sources at interior vertices carry irreps, seen
un-conjugated.  A configuration is ADMISSIBLE iff at every interior vertex
the tensor product of the incident oriented-slot irreps and any source
irrep contains the trivial irrep -- this per-vertex-singlet rule is the
model's DEFINITION of admissibility; its reading as a lattice Gauss law /
interior gauge invariance is a NAMED IDENTIFICATION, computed nowhere.
Center charge: SU(2) q(a) = a mod 2; SU(3) triality q(p,q) = (p-q) mod 3.
Outward flux charge through a bipartition cut delta(S): +q at
tail-enclosed slots, -q at head-enclosed slots, mod N.

NAMED HYPOTHESIS H-hom (the abstract statement's single group input): the
center charge map q is a fusion homomorphism -- every irrep of
multiplicity > 0 in a (x) b carries q == q(a) + q(b) mod N.  H-hom is
battery-computed on stated grids for both instances and stays a NAMED
HYPOTHESIS beyond them.

THE LEMMA (under H-hom + the per-vertex-singlet definition):
  (i)   singlet law: trivial-irrep existence forces total charge == 0
        mod N (single step by H-hom; induction on tensor depth -- the
        parent lane's W1-UNIV carriage generic in N).
  (ii)  cut law: outward flux charge through EVERY bipartition-induced
        cut delta(S), S a nonempty interior vertex set, == enclosed
        source charge mod N.  Carrier: the graph-generic signed
        double-counting identity -- per edge, the coefficient of q_e in
        the S-summed per-vertex charge sums is [head in S] - [tail in S]
        (internal and external edges 0, self-loops always 0), computed
        coefficient-by-coefficient on the edge-indicator basis, so
        Z-linearity carries it to every labelling at any cap; the
        [head]-[tail] sum equals MINUS the enclosed source charge and the
        outward convention's opposite signs flip the negation.
  (iii) flux exit: a source set of charge != 0 mod N forces >= 1
        charge-nonzero edge in every source-enclosing bipartition cut
        delta(S), and >= L across a nested pairwise-disjoint family of L
        such cuts.
  Instantiated and COMPUTED at N = 2 (SU(2); reproduces the parent
  flux-exit-parity results -- coincidence computed, not analogy: signed
  == unsigned flux mod 2 per configuration per cut) and N = 3 (SU(3)).
  Abstract for all other N under H-hom only; NO SU(N > 3) claim.
  SU(3) exhibits at the stated cap p + q <= 2 on the walked graphs: a
  (1,0) source at distance L forces exit with an exact-L string witness;
  the adjoint (1,1) admits a bounded fully-contained triangle screen,
  support 3, constant in L; THE BARYON EXHIBIT -- three (1,0) sources
  (total triality 0) admit a fully contained admissible configuration
  (3x3x3 contains exactly one singlet) while two (1,0) sources (triality
  2) provably cannot be contained, both directions exhaustive at the cap.

CONSTRUCTION PROVENANCE (what retired the consumed-rule premise): the
SU(2) fusion rule is CONSTRUCTED in-module by the character/Chebyshev
route (integer Laurent characters, leading-character subtraction) and its
agreement with the banked testbed's `_su2_tensor` is COMPUTED here on the
stated grids; every tensor product in this module runs on constructed
rules.  SU(3) tensoring is CONSTRUCTED in-module TWICE independently
(Gelfand-Tsetlin weight convolution with lex-leading subtraction;
Littlewood-Richardson tableau counting) and cross-checked (route
agreement, the fusion table, dimension counting as GT-side corroboration).
AUDIT RECORD, cited not imported: the stage-1 hostile audit
(AUDIT_center_flux_stage1.md, LAND-WITH-FIXES 0.90) verified the SU(3)
rules against a THIRD route (Jacobi-Trudi / Weyl-alternant extraction) and
a FOURTH (Weyl-integration constant term) on and beyond the walked grids,
and CERTIFIED the lex-leading-subtraction triangularity (lex-max =
highest weight, grid; dominance implies lex, exhaustive to total 12;
sabotage 60/60 caught).  W1-UNIV NAMED IMPORT: the implemented
`_su2_tensor`'s emission SHAPE outside the grids verified here and in the
lane record remains a named import of that leg (independently
audit-confirmed wherever probed).

PREMISE STACK (the granted grade line's conditioning bar):
  1. Electric-basis model convention (CONSUMED, BANKED): the
     strong-coupling-eigenbasis frame of apf/su2_string_cut_testbed.py,
     whose home verdict is consumed LIVE below via
     check_T_su2_string_cut_comovement (P_structural_reading, PARTIAL,
     four clauses -- inherited, never flattened).
  2. Per-vertex-singlet admissibility (MODEL DEFINITION): the Gauss /
     interior-gauge-invariance reading is a named identification,
     computed nowhere in this module or its lane.
  3. H-hom (NAMED HYPOTHESIS): computed on the stated grids for N = 2, 3;
     hypothesis beyond them.  The grade line's conditioning bar prices
     exactly this.

THE PREREQUISITE-(b) RULING (Ethan, 2026-07-11; ruling-of-record, this
module -- the R7/3a/4a corrigendum pattern; branch (ii) REGISTER of the
prereq_b re-scope lane): the identification "per-vertex-singlet
admissibility = lattice Gauss law / interior gauge invariance" (premise
stack item 2), carrying the electric-basis frame convention as its
named frame (home: check_T_su2_string_cut_comovement, stack item 1), is
RULED a REGISTERED BASE-RESTING VALUE-SUPPLIER of the lattice
colour-record reading -- a convention-of-record with grounds, NOT a
derivation.  The identification stays computed nowhere: the
registration RECORDS that it is an input, it does not compute it.
Grounds recorded with the ruling (verbatim from the lane record, WALK
NOTE section 5): (1) the lane's localization computation (the chain
leaves exactly one open identification); (2) FD1-sc supplies the
negative half at [P] (no-fiat), so the registered content is only the
positive selection; (3) the banked family-relativity verdict + the
six-audit refusal show the positive selection is not currently
derivable -- naming it is the honest bookkeeping.  FALSIFIER OF RECORD
(verbatim, ibid.): an in-model computation exhibiting an admissible
configuration (per-vertex-singlet holds) whose physical colour-record
content provably differs from its invariant content at a
vertex-disjoint cut -- or an in-bank derivation of the electric-frame
selection from the four (which would retire the registration in favour
of branch (i)).  RECORD: prerequisite (b) of the ym_conformal_phase
promotion docket is RE-SCOPED to this identification, NOT discharged
("(b) discharged" stays an unlicensed sentence); every downstream grade
is UNCHANGED (every consumer stays at its banked grade; this lemma's
grade line below is untouched); promotion of
check_T_ym_conformal_phase_excluded_by_record_locking stays gated on
prerequisites (a)/(d) -- "Not promotable now" stands verbatim; the
FD1-sc negative half stands at [P]; the derive branch (branch (i)) was
PRICED AND DECLINED (zero grade movement against two banked walls); the
6-audit A1-internal forcing bar (2026-06-29, do-not-re-walk) is
untouched.  Lane record: prereq_b_rescope_2026-07-11/ (WALK_NOTE.md
sections 3/5/6; walker run of record in RUN_LOG.txt).

THE ICL PATTERN-INSTANTIATION (corrigendum of record, Ethan,
2026-07-11, chartered narrow -- the .416/.417 P-dangling
instantiation-corrigendum form, count-neutral; registered against the
ICL name): under this lemma's premise stack, the ICL conjecture's
boundary-billing PATTERN has a computed gauge-side instance -- an
unpassivatable (N-ality != 0) source forces >= 1 billed link across
every interior bipartition cut (the cut law: the crossing content's
center-charge shadow is pinned to the enclosed source charge), and the
passivatable branch exhibits nothing-need-cross (a bounded screen,
geometry-conditional) -- under THREE NAMED IDENTIFICATIONS: (i)
per-vertex-singlet = Gauss (REGISTERED above, the prerequisite-(b)
ruling); (ii) bipartition cut = causal boundary -- NEW, NAMED HERE,
owned by no prior record; a possible category-error adjudication is a
LIVE KILL; (iii) charge-nonzero link = billed structure, via the
support-reading residue of record (ruled convention-of-record
2026-07-10; its ceiling and vertex-disjoint rider carried).  MANDATORY
HONESTY CLAUSES: the instance reading's grade ceiling is
[P_structural_reading] -- NOTHING HERE LIFTS ANY GRADE; the ICL
conjecture stays [C], open and named; the 2026-07-04 HOLD-NAMED
principal ruling (ICL_vac a named, open, falsifiable seam commitment --
not adopted, not declined) is UNTOUCHED and cited here; this is an
instance of ICL's PATTERN at billing granularity -- NEVER the ceiling
("only scalar crosses" is NOT shown: the forced crossers are
irrep-labelled links) and NOT floor-redundant (the sector-typed
surplus: N-ality granularity + both branches computed); the V2
two-family fence travels verbatim (boost == no-B family (i) ONLY; no
YM gap-occurrence sweep-in); this instance may NEVER be cited as
adoption pressure on ICL or as moving the R_ICL_vac wall.  KILL MODES:
an H-hom failure at any computed instance; the cut-as-causal-boundary
identification (ii) adjudicated a category error; any drift to ceiling
phrasing (dies on the floor/ceiling adjudication) or to floor-only
phrasing (dies as redundant).

DEPENDENCY CHOICE (argued): dependencies list ONLY
T_su2_string_cut_comovement -- the frame convention's home check,
consumed live.  A1 is EXCLUDED deliberately: this lemma is pure model
mathematics (exact representation theory + integer graph arithmetic on a
named model); the word "admissibility" here is the model's INTERNAL
definition (premise stack item 2), not APF's A1 admissibility axiom, and
no APF axiom is consumed in any computation.  Listing A1 would smuggle
the physics identification into a [P_math] lemma's premise row; the
identification is instead fenced as a named reading.  (The .412 [P_math]
module is the house precedent for a math lemma's dependency list; it is
not readable from this seat -- this choice is flagged for main-seat
review.)  check_T_su2_string_cut_native_algebra is a cross_ref, NOT
consumed live: its k=3 leg imports numpy at call time and this module
must stay runnable in a bare stdlib tree (verified under a blocked-numpy
import hook).

KILL CONDITION (LOUD): an H-hom failure at any computed instance -- a
constituent of any fusion product under either constructed rule carrying
q != q(a) + q(b) mod N -- would REFUTE that instance's charge carriage
and kill the lemma's instantiation there (the abstract statement would
survive only as an empty conditional).  The construction flags (a
nonpositive leading coefficient in the SU(2) character subtraction; a
nonpositive multiplicity or non-dominant lex-max in the SU(3) route-A
subtraction) tripping on any walked product would kill the construction
legs.  Both are asserted 0 below and in the 4397-check lane walker.

SUPERSEDE-OR-ABSORB (stage-2 precondition 2, carried): the SU(2)-only
candidate `check_L_lattice_gauss_parity_flux_exit` (never banked; the
parent seat stopped at its gate) is ABSORBED here as the N = 2 instance.
The parent's grade of record [P_structural | named stack] is SUPERSEDED
by this composite's conditional [P_math] FOR THE THEOREM CONTENT ONLY;
the parent's walked-graph enumeration facts keep their own scoping and
the parent lane record stays HELD.  The parent's T-c screen content
(even-source bounded screens, the loop condition, the argmin selection
question) is NOT part of this candidate beyond the SU(3) (1,1) exhibit
below.

MAY-NOT-CITE (merged from both audit inventories; citation without the
premise stack is misciting):
  - NO parity/charge cut-EQUALITY claim for arbitrary separating edge
    sets: the law is bipartition-delta(S)-scoped; the parent lane's
    computed counterexample travels.  (Arbitrary separating subsets
    inherit only the >= 1-nonzero conclusion, and only where a coverage
    leg is computed -- the parent's SU(2) coverage leg is parent-scoped.)
  - Screens are EXISTENCE statements under the named screen-existence
    (cycle) condition; whether a screen is taken is the parent lane's
    argmin convention -- never cite as selection.
  - H-hom is a NAMED HYPOTHESIS beyond the computed grids; the batteries
    are not a proof of it.
  - NO graph-generality claim beyond the executed per-edge derivation's
    scope statement (the identity's proof-step is executed per edge of
    whatever graph is presented; the random sweep is non-vacuity).
  - NO consumption by the confinement parent lane without its
    support-reading residual premise (the residue of record) NAMED.
  - The SU(2)-only candidate (flux_exit_parity) is superseded FOR
    THEOREM CONTENT ONLY as the N = 2 instance; its lane record stands.
    WHEREVER THE N = 2 INSTANCE IS CITED, the parent's own MAY-NOT-CITE
    lines travel with it: no non-delta(S) parity equality; T-c only with
    its loop condition, existence-only; support-reading named; the
    parent's W6 cap-stability leg is an exhibit, never a carrier
    (cap-freeness rides the identity + W1-UNIV); no graph-general claim
    beyond the parent's walked family for its enumeration facts.
  - NO SU(N > 3) claim.
  - NO magnitude/tension/spectral/continuum/dynamics claim; kinematic
    admissibility statements only; the baryon/pair leg is ONE computed
    exhibit at cap p + q <= 2 on the walked claw graphs.
  - The composed confinement reading sentence is NOT licensed by this
    lemma.

GRADE [P_math | electric-basis model convention + per-vertex-singlet
admissibility (Gauss reading a named identification) + H-hom as named
hypothesis] for the abstract Z_N law; enumeration legs and the baryon
exhibit instance-scoped [P] at stated caps and walked graphs.  Tier 4.
Verbatim from the stage-2 grant; the stage-1 grade-line ruling and both
REOPENER discharges are the audit record.

Lane records: The Turning (parked)/flux_exit_parity_2026-07-10/
(walk_flux_exit_parity.py v2 [6446 checks, exit 0], FLUX_EXIT_NOTE_v0.2,
stage-1/stage-2 audits LAND 0.88/0.92) and flux_exit_zn_2026-07-10/
(walk_center_flux_exit.py v2 [4397 checks, exit 0],
CENTER_FLUX_NOTE_v0.2, AUDIT_center_flux_stage1.md LAND-WITH-FIXES 0.90
with probes 39/39 after carry).  This module banks the DISTILLED battery;
the walkers are the lane records.
"""

from itertools import combinations, product
import ast
import random

# ---------------------------------------------------------------------------
# constructed SU(2) fusion (character / Chebyshev route, pure integers)
# ---------------------------------------------------------------------------
_F2 = {}
_FLAG2 = [0]


def _su2_fuse(a, b):
    key = (a, b)
    if key in _F2:
        return _F2[key]
    P = {}
    for e1 in range(-a, a + 1, 2):
        for e2 in range(-b, b + 1, 2):
            P[e1 + e2] = P.get(e1 + e2, 0) + 1
    out = {}
    while P:
        top = max(P)
        m = P[top]
        if m <= 0 or top < 0:
            _FLAG2[0] += 1
            break
        out[top] = m
        for e in range(-top, top + 1, 2):
            P[e] = P.get(e, 0) - m
            if P[e] == 0:
                del P[e]
    _F2[key] = out
    return out


# ---------------------------------------------------------------------------
# constructed SU(3) fusion, route A (GT weight convolution + lex-leading
# subtraction) and route B (Littlewood-Richardson tableau counting)
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
# generic Z_N machinery (instances: SU(2)/Z_2, SU(3)/Z_3)
# ---------------------------------------------------------------------------
_SU2 = {'name': 'SU2', 'N': 2, 'unit': 0, 'conj': lambda a: a,
        'fuse': _su2_fuse, 'q': lambda a: a % 2}
_SU3 = {'name': 'SU3', 'N': 3, 'unit': (0, 0), 'conj': lambda t: (t[1], t[0]),
        'fuse': _su3_fuse, 'q': lambda t: (t[0] - t[1]) % 3}
_LAB3 = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]     # cap p+q <= 2
_SMC = {}


def _singlet(inst, labels):
    key = (inst['name'], tuple(sorted(labels)))
    if key in _SMC:
        return _SMC[key]
    dec = {inst['unit']: 1}
    for b in sorted(labels):
        new = {}
        for x, m in dec.items():
            for c, k in inst['fuse'](x, b).items():
                new[c] = new.get(c, 0) + m * k
        dec = new
    m = dec.get(inst['unit'], 0)
    _SMC[key] = m
    return m


def _content(g, cfg, v, inst):
    out = []
    for i, (x, y) in enumerate(g['E']):
        if y == v:
            out.append(cfg[i])
        if x == v:
            out.append(inst['conj'](cfg[i]))
    s = g['sources'].get(v)
    if s is not None and s != inst['unit']:
        out.append(s)
    return tuple(out)


def _enum(g, inst, labels):
    E = g['E']
    inc = {v: [i for i, (x, y) in enumerate(E) if v in (x, y)]
           for v in g['V']}
    interior = [v for v in g['V'] if v not in g['boundary']]
    comp = {}
    for v in interior:
        if inc[v]:
            comp.setdefault(max(inc[v]), []).append(v)
        elif _singlet(inst, _content(g, (), v, inst)) == 0:
            return []
    out = []
    cfg = [inst['unit']] * len(E)

    def rec(i):
        if i == len(E):
            out.append(tuple(cfg))
            return
        for lab in labels:
            cfg[i] = lab
            if all(_singlet(inst, _content(g, cfg, v, inst)) > 0
                   for v in comp.get(i, ())):
                rec(i + 1)
    rec(0)
    return out


def _hhom_viol(inst, pairs, fuse=None):
    fuse = fuse or inst['fuse']
    q, N = inst['q'], inst['N']
    nv = nc = 0
    for a, b in pairs:
        t = (q(a) + q(b)) % N
        for c, m in fuse(a, b).items():
            if m > 0:
                nc += 1
                if q(c) % N != t:
                    nv += 1
    return nv, nc


# graphs (the parent's five shapes + claw, oriented as listed)
def _path(L, src):
    return {'V': [f"v{i}" for i in range(L + 1)],
            'E': [(f"v{i}", f"v{i+1}") for i in range(L)],
            'boundary': frozenset([f"v{L}"]), 'sources': {'v0': src},
            'nested': [frozenset(f"v{j}" for j in range(i))
                       for i in range(1, L + 1)], 'L': L}


def _star(src):
    return {'V': ['c', 'm1', 'm2', 'm3', 'l1', 'l2', 'l3'],
            'E': [('c', 'm1'), ('m1', 'l1'), ('c', 'm2'), ('m2', 'l2'),
                  ('c', 'm3'), ('m3', 'l3')],
            'boundary': frozenset(['l1', 'l2', 'l3']), 'sources': {'c': src},
            'nested': [frozenset(['c']),
                       frozenset(['c', 'm1', 'm2', 'm3'])], 'L': 2}


def _grid(src):
    ce, mids = (1, 1), [(0, 1), (1, 0), (1, 2), (2, 1)]
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    E = [(ce, m) for m in mids]
    mc = {(0, 1): [(0, 0), (0, 2)], (1, 0): [(0, 0), (2, 0)],
          (1, 2): [(0, 2), (2, 2)], (2, 1): [(2, 0), (2, 2)]}
    for m in mids:
        for c in mc[m]:
            E.append((m, c))
    return {'V': [ce] + mids + corners, 'E': E,
            'boundary': frozenset(corners), 'sources': {ce: src},
            'nested': [frozenset([ce]), frozenset([ce] + mids)], 'L': 2}


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


def _pairg(s1, s2):
    return {'V': [f"v{i}" for i in range(5)],
            'E': [(f"v{i}", f"v{i+1}") for i in range(4)],
            'boundary': frozenset(['v4']), 'sources': {'v0': s1, 'v2': s2}}


def _claw(n_src):
    V = [f"s{i}" for i in range(n_src)] + ['c', 'x1']
    E = [(f"s{i}", 'c') for i in range(n_src)] + [('c', 'x1')]
    return {'V': V, 'E': E, 'boundary': frozenset(['x1']),
            'sources': {f"s{i}": (1, 0) for i in range(n_src)},
            'nested': [frozenset([f"s{i}" for i in range(n_src)] + ['c'])],
            'L': 1}


def _identity_on(g, S):
    """Both handshake identities, coefficient-by-coefficient (the executed
    per-edge proof step).  Returns True iff every coefficient matches."""
    inc = {}
    for i, (x, y) in enumerate(g['E']):
        inc.setdefault(x, []).append(i)
        inc.setdefault(y, []).append(i)
    for e, (x, y) in enumerate(g['E']):
        lhs = sum(1 for v in S for i in inc.get(v, ()) if i == e)
        m_e = (1 if x in S else 0) + (1 if y in S else 0)
        internal, cut = (x in S) and (y in S), (x in S) != (y in S)
        if lhs != m_e or m_e != (2 if internal else (1 if cut else 0)):
            return False
        if (internal + cut + (m_e == 0)) != 1 or (x == y and cut):
            return False
        s_lhs = (1 if y in S else 0) - (1 if x in S else 0)
        if s_lhs != (0 if not cut else (1 if y in S else -1)):
            return False
        if x == y and s_lhs != 0:
            return False
    return True


def _zn_battery(g, inst, labels, ck, tag):
    """Distilled generic-N instance battery: singlet law per vertex, the
    cut law and flux exit per interior S, the nested-family count."""
    N, q = inst['N'], inst['q']
    interior = [v for v in g['V'] if v not in g['boundary']]
    cfgs = _enum(g, inst, labels)
    ck(len(cfgs) > 0, f"[{tag}] admissible set nonempty "
       f"({len(cfgs)} configurations at the stated cap)")
    E = g['E']
    bad_v = bad_law = bad_exit = 0
    fams = []
    for r in range(1, len(interior) + 1):
        for comb in combinations(interior, r):
            S = frozenset(comb)
            cut = [(i, (1 if x in S else -1)) for i, (x, y) in enumerate(E)
                   if (x in S) != (y in S)]
            sq = sum(q(g['sources'][v]) for v in S
                     if v in g['sources']) % N
            fams.append((S, cut, sq))
    srcverts = frozenset(g['sources'])
    for cfg in cfgs:
        for v in interior:
            s = sum(q(cfg[i]) for i, (x, y) in enumerate(E) if y == v) \
                - sum(q(cfg[i]) for i, (x, y) in enumerate(E) if x == v) \
                + (q(g['sources'][v]) if v in g['sources'] else 0)
            if s % N:
                bad_v += 1
        for S, cut, sq in fams:
            flux = sum(sgn * q(cfg[i]) for i, sgn in cut)
            if (flux - sq) % N:
                bad_law += 1
            if srcverts <= S and sq % N:
                if not any(q(cfg[i]) % N for i, _ in cut):
                    bad_exit += 1
    ck(bad_v == 0, f"[{tag}] per-vertex charge sum == 0 mod {N} in every "
       "admissible configuration (the singlet law's instance, computed)")
    ck(bad_law == 0, f"[{tag}] cut law: outward flux charge == enclosed "
       f"source charge mod {N} over all {len(fams)} interior bipartition "
       f"cuts delta(S) x {len(cfgs)} configurations (computed)")
    ck(bad_exit == 0, f"[{tag}] flux exit: >= 1 charge-nonzero edge in "
       "every source-enclosing bipartition cut delta(S) with nonzero "
       "enclosed charge (computed per configuration)")
    L = g['L']
    cuts = [frozenset(i for i, (x, y) in enumerate(E)
                      if (x in S) != (y in S)) for S in g['nested']]
    disj = all(not (cuts[i] & cuts[j]) for i in range(len(cuts))
               for j in range(i + 1, len(cuts)))
    totq = sum(q(s) for s in g['sources'].values()) % N
    if totq:
        union = frozenset().union(*cuts)
        minnz = min(sum(1 for x in cfg if q(x) % N) for cfg in cfgs)
        ck(disj and len(cuts) == L
           and all(sum(1 for i in union if q(cfg[i]) % N) >= L
                   for cfg in cfgs)
           and minnz == L,
           f"[{tag}] nested disjoint family of L = {L} cuts: >= L "
           "charge-nonzero edges per configuration across the family, "
           "and the admissible-set minimum == L (witness-tight, computed)")
    return cfgs


def check_L_center_flux_exit():
    """L_center_flux_exit: the Z_N cut law and flux-exit theorem under
    named H-hom, N = 2 and N = 3 computed, with the baryon exhibit.  See
    the module docstring for the statement, premise stack, kill
    condition, MAY-NOT-CITE fences, and the dependency argument.  This is
    the DISTILLED battery; the 4397-check walker (and the 6446-check
    SU(2) parent it absorbs as the N = 2 instance) are the lane records."""
    from apf.su2_string_cut_testbed import (
        _su2_tensor,
        check_T_su2_string_cut_comovement,
    )

    fails = []
    n_checks = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        n_checks[0] += 1

    # ---- live bank anchor: the electric-basis frame's home verdict ------
    r = check_T_su2_string_cut_comovement()
    ck(r.get('passed') is True
       and r.get('epistemic') == 'P_structural_reading'
       and r.get('verdict') == 'PARTIAL',
       "anchor T_su2_string_cut_comovement passes LIVE "
       "(P_structural_reading, PARTIAL, four clauses -- the electric-basis "
       "frame convention this lemma consumes, inherited never flattened; "
       "T_su2_string_cut_native_algebra is cross_ref only: its k=3 leg "
       "needs numpy and this module stays bare-stdlib runnable)")

    # ---- (1) constructed SU(2) rule == the banked testbed rule ----------
    for a in range(21):
        for b in range(21):
            mine = _su2_fuse(a, b)
            ck(mine == _su2_tensor({a: 1}, b)
               and sum(m * (c + 1) for c, m in mine.items())
               == (a + 1) * (b + 1)
               and mine == _su2_fuse(b, a),
               f"character-route SU(2) fusion == _su2_tensor at ({a},{b}) "
               "+ dimension count + commutativity (full grid to 20)")
    spot_ok = all(_su2_fuse(a, b) == _su2_tensor({a: 1}, b)
                  for a, b in [(40, 40), (81, 63), (120, 77), (155, 44),
                               (200, 200), (199, 2), (0, 173)])
    rng = random.Random(20260711)
    rand_ok = all(_su2_fuse(a, b) == _su2_tensor({a: 1}, b)
                  for a, b in [(rng.randrange(201), rng.randrange(201))
                               for _ in range(20)])
    ck(spot_ok and rand_ok and _FLAG2[0] == 0,
       "constructed rule == _su2_tensor on 7 spot pairs to (200,200) + 20 "
       "seeded random pairs to 200; zero decomposition-flag trips -- the "
       "rule is CONSTRUCTED in-module, agreement computed, the "
       "consumed-rule premise retired (full-grid-40 + associativity legs "
       "are the lane walker's)")
    ck(_su2_fuse(1, 1) == {0: 1, 2: 1}
       and _su2_fuse(2, 2) == {0: 1, 2: 1, 4: 1}
       and _su2_fuse(1, 2) == {1: 1, 3: 1},
       "SU(2) fusion table pins on the constructed rule (computed)")

    # ---- (2) W1-UNIV: the cap-free parity carriage ----------------------
    ck(all((a + b) - abs(a - b) == 2 * min(a, b)
           for a in range(101) for b in range(101)),
       "W1-UNIV leg i: (a+b) - |a-b| == 2*min(a,b) exhaustive to 100 "
       "(two-case expansion makes it universal), so the CG range START is "
       "congruent to a+b mod 2 at ALL labels")
    ck(all(k % 2 == (a + b) % 2 for a in range(0, 201, 7)
           for b in range(0, 201, 11)
           for k in range(abs(a - b), a + b + 1, 2)),
       "W1-UNIV leg ii: every step-2-range label congruent to a+b mod 2 "
       "(dense grid to 200; general by leg i + the step of 2)")
    ck(all(sorted(_su2_tensor({a: 1}, b))
           == list(range(abs(a - b), a + b + 1, 2))
           for a in range(0, 201, 13) for b in range(0, 201, 17)),
       "W1-UNIV leg iii: the implemented rule emits exactly the step-2 "
       "range on the step-13/17 grid reaching 195/187 (and full to 20 in "
       "leg (1)); emission OUTSIDE the verified grids is the NAMED import "
       "-- with legs i+ii and induction on tensor depth, singlet "
       "existence forces even total parity AT ANY CAP (the cap-free "
       "carrier of the N=2 instance)")

    # ---- (3) the graph-generic double-counting identity -----------------
    shapes = [('path3', _path(3, 1)), ('star3', _star(1)),
              ('grid2x2', _grid(1)), ('tt2', _tt(2, 1)),
              ('pair', _pairg(1, 1))]
    for name, g in shapes:
        nS = 0
        ok = True
        for rr in range(1, len(g['V']) + 1):
            for comb in combinations(g['V'], rr):
                nS += 1
                if not _identity_on(g, frozenset(comb)):
                    ok = False
        ck(ok, f"handshake identity (unsigned 2/1/0 AND signed +1/0/-1 "
           f"coefficients) computed per edge on the edge-indicator basis "
           f"for ALL {nS} nonempty S of parent shape {name} -- "
           "Z-linearity carries it to every labelling at any cap")
    rng2 = random.Random(20260711)
    n_loop = n_multi = 0
    for t in range(40):
        nv = rng2.randrange(3, 11)
        E = [(rng2.randrange(nv), rng2.randrange(nv))
             for _ in range(rng2.randrange(max(2, nv - 1), 2 * nv + 3))]
        g = {'V': list(range(nv)), 'E': E, 'boundary': frozenset(),
             'sources': {}}
        n_loop += any(x == y for x, y in E)
        n_multi += len(set(tuple(sorted(e)) for e in E)) < len(E)
        subsets = [frozenset(c) for rr in range(1, nv + 1)
                   for c in combinations(range(nv), rr)] if nv <= 7 else \
                  [frozenset(v for v in range(nv) if rng2.randrange(2))
                   for _ in range(40)]
        ck(all(_identity_on(g, S) for S in subsets if S),
           f"handshake identity on seeded random graph {t} ({nv} "
           f"vertices, {len(E)} edges) over {len([S for S in subsets if S])} "
           "vertex subsets -- model calls: a self-loop contributes 2 to "
           "its vertex sum and is never a cut edge (signed coefficient "
           "always 0); multi-edges are independent edges")
    ck(n_loop >= 5 and n_multi >= 5,
       f"non-vacuity: the 40-graph sweep contains {n_loop} graphs with "
       f"self-loops and {n_multi} with multi-edges (computed counts); the "
       "per-edge slot count IS the proof -- every edge has exactly two "
       "endpoint slots and membership determines the coefficient -- the "
       "sweep is non-vacuity, the executed step is the carrier")

    # ---- (4) H-hom batteries + the abstract law's computed inputs -------
    p2 = [(a, b) for a in range(13) for b in range(13)]
    nv2, nc2 = _hhom_viol(_SU2, p2)
    ck(nv2 == 0 and nc2 > 500,
       f"H-hom battery [SU(2), N=2], grid scope first: over the computed "
       f"grid (pairs to 12), q(a) = a mod 2 is a fusion homomorphism "
       f"there ({nc2} constituents, 0 violations, constructed rule); "
       "beyond the computed grids H-hom stays the NAMED hypothesis")
    l3 = [(p, q) for p in range(3) for q in range(3)]
    nv3, nc3 = _hhom_viol(_SU3, [(a, b) for a in l3 for b in l3])
    ck(nv3 == 0 and nc3 > 300,
       f"H-hom battery [SU(3), N=3], grid scope first: over the computed "
       f"grid (pairs to (2,2)), triality q = (p-q) mod 3 is a fusion "
       f"homomorphism there ({nc3} constituents, 0 violations); beyond "
       "the computed grids H-hom stays the NAMED hypothesis")
    for inst, labs in ((_SU2, list(range(9))), (_SU3, l3)):
        N, qf, cj, un = inst['N'], inst['q'], inst['conj'], inst['unit']
        ck(all(inst['fuse'](a, un) == {a: 1} for a in labs)
           and qf(un) % N == 0
           and all(inst['fuse'](a, cj(a)).get(un, 0) == 1
                   and (qf(a) + qf(cj(a))) % N == 0 for a in labs),
           f"[{inst['name']}] unit fusion-neutral with q(unit) == 0, and "
           "the trivial irrep sits once in a x conj(a) with q(conj(a)) == "
           f"-q(a) mod {N} (computed; both facts also derivable from "
           "named H-hom -- the tail-slot charge convention's ground)")
    fold_ok = True
    for tup in list(product(range(4), repeat=3)) \
            + list(product(_LAB3, repeat=2)):
        inst = _SU2 if isinstance(tup[0], int) else _SU3
        dec = {inst['unit']: 1}
        for b in tup:
            new = {}
            for x, m in dec.items():
                for c, k in inst['fuse'](x, b).items():
                    new[c] = new.get(c, 0) + m * k
            dec = new
        tgt = sum(map(inst['q'], tup)) % inst['N']
        for c, m in dec.items():
            if m > 0 and inst['q'](c) % inst['N'] != tgt:
                fold_ok = False
        if dec.get(inst['unit'], 0) > 0 and tgt:
            fold_ok = False
    ck(fold_ok,
       "abstract singlet law (i), named hypothesis H-hom: every "
       "constituent of every systematic fold carries the summed charge "
       "mod N and singlet existence forces total charge == 0 mod N "
       "(computed on 100 folds across both instances; carried at all "
       "depths by the H-hom single-step + induction, the W1-UNIV shape "
       "generic in N; the signed identity in leg (3) then gives the cut "
       "law -- the [head]-[tail] sum equals MINUS the enclosed source "
       "charge, and the outward convention's opposite signs flip the "
       "negation -- and flux exit is immediate, delta(S)-scoped)")

    # ---- (5) N = 2 instance: the absorbed parent, reduced ---------------
    for g, tag in [(_path(1, 1), 'N=2 path1'), (_path(2, 1), 'N=2 path2'),
                   (_path(3, 1), 'N=2 path3'), (_tt(2, 1), 'N=2 tt2')]:
        cfgs = _zn_battery(g, _SU2, [0, 1, 2], ck, tag)
        if 'tt' in tag:
            witness = (0, 0, 0) + tuple([1] * g['L'])
        else:
            witness = tuple([1] * len(g['E']))
        ck(witness in cfgs,
           f"[{tag}] the straight a=1 string witness is admissible "
           "(exact-L, computed on the constructed rule)")
        interior = [v for v in g['V'] if v not in g['boundary']]

        def _imported_singlet(labs):
            dec = {0: 1}
            for b in sorted(labs):
                dec = _su2_tensor(dec, b)
            return dec.get(0, 0)
        ref = [cfg for cfg in product([0, 1, 2], repeat=len(g['E']))
               if all(_imported_singlet(_content(g, cfg, v, _SU2)) > 0
                      for v in interior)]
        ck(sorted(cfgs) == sorted(ref),
           f"[{tag}] admissible set under the CONSTRUCTED rule == under "
           "the consumed _su2_tensor (both enumerated; the retirement "
           "carried at the use site)")
        co_ok = True
        for cfg in cfgs:
            for rr in range(1, len(interior) + 1):
                for comb in combinations(interior, rr):
                    S = frozenset(comb)
                    sg = sum((1 if x in S else -1) * (cfg[i] % 2)
                             for i, (x, y) in enumerate(g['E'])
                             if (x in S) != (y in S))
                    us = sum(cfg[i] for i, (x, y) in enumerate(g['E'])
                             if (x in S) != (y in S))
                    if (sg - us) % 2:
                        co_ok = False
        ck(co_ok,
           f"[{tag}] COINCIDENCE COMPUTED: signed outward flux == "
           "unsigned label-sum parity mod 2, per configuration per cut "
           "-- the parent's unoriented parity model IS the N=2 instance "
           "under named H-hom (SU(2) self-conjugacy computed in leg 4)")
        srcv = next(iter(g['sources']))
        ck(_singlet(_SU2, _content(g, tuple([0] * len(g['E'])), srcv,
                                   _SU2)) == 0,
           f"[{tag}] all-trivial configuration inadmissible at the odd "
           "source vertex (contrapositive control, computed)")

    # ---- (6) SU(3) construction: both routes, reduced grid --------------
    small = [(p, q) for p in range(3) for q in range(3)]
    ck(all(_su3_fuse(a, b) == _su3_fuse_lr(a, b)
           for a in small for b in small) and _FLAG3[0] == 0,
       "SU(3) route A (GT weight convolution + lex-leading subtraction) "
       "== route B (LR tableau counting) on all 81 pairs to (2,2); zero "
       "route-A flag trips (audit record cited in docstring: third/fourth "
       "independent routes agreed and triangularity CERTIFIED -- "
       "AUDIT_center_flux_stage1.md, not imported)")
    ck(all(sum(m * _su3_dim(*c) for c, m in _su3_fuse(a, b).items())
           == _su3_dim(*a) * _su3_dim(*b)
           for a in small for b in small),
       "SU(3) dimension counting on the grid to (2,2) -- GT-side "
       "corroboration (termination-tautological against the subtraction "
       "loop; the independent checks are route B, the table, and the "
       "lane walker's associativity leg)")
    f3 = _su3_fuse
    ck(f3((1, 0), (0, 1)) == {(0, 0): 1, (1, 1): 1},
       "3 x 3bar = 1 + 8 (computed)")
    ck(f3((1, 0), (1, 0)) == {(0, 1): 1, (2, 0): 1},
       "3 x 3 = 3bar + 6 -- NO singlet: a quark pair cannot be neutral "
       "(computed)")
    ck(f3((1, 1), (1, 1)) == {(0, 0): 1, (1, 1): 2, (3, 0): 1, (0, 3): 1,
                              (2, 2): 1},
       "8 x 8 = 1 + 8 + 8 + 10 + 10bar + 27 (computed)")
    trip = {}
    for c1, m1 in f3((1, 0), (1, 0)).items():
        for c2, m2 in f3(c1, (1, 0)).items():
            trip[c2] = trip.get(c2, 0) + m1 * m2
    ck(trip == {(0, 0): 1, (1, 1): 2, (3, 0): 1},
       "3 x 3 x 3 = 1 + 8 + 8 + 10: EXACTLY ONE singlet (computed; the "
       "baryon exhibit's algebra)")

    # ---- (7) SU(3) instance legs at cap p + q <= 2 -----------------------
    for L in (1, 2, 3):
        g = _path(L, None)
        g['sources'] = {'v0': (1, 0)}
        cfgs = _zn_battery(g, _SU3, _LAB3, ck, f"SU(3) path{L} (1,0)")
        ck(tuple([(1, 0)] * L) in cfgs,
           f"[SU(3) path{L}] exact-L (1,0)-string witness admissible "
           "(oriented along the path; computed)")
    counts = []
    for L in (1, 2, 3):
        g = _tt(L, (1, 1))
        screen = tuple([(1, 1)] * 3 + [(0, 0)] * L)
        interior = [v for v in g['V'] if v not in g['boundary']]
        ck(all(_singlet(_SU3, _content(g, screen, v, _SU3)) > 0
               for v in interior),
           f"[SU(3) tt{L} (1,1)] the adjoint triangle screen is "
           "admissible at every interior vertex, support exactly the 3 "
           "cycle edges, tail trivial -- bounded and fully contained "
           "(existence only; the screen-existence cycle condition is "
           "named; whether it is taken is the parent lane's argmin "
           "convention, not cited here)")
        cfgs = _enum(g, _SU3, _LAB3)
        counts.append(len(cfgs))
        ck(screen in cfgs, f"[SU(3) tt{L} (1,1)] screen located in the "
           f"exhaustive admissible set ({len(cfgs)} configurations)")
    ck(counts == [11, 11, 11],
       "adjoint screen option CONSTANT in boundary distance: admissible "
       "count 11 at L = 1, 2, 3 (pinned from the lane record, recomputed)")
    g3 = _claw(3)
    cfg3 = _zn_battery(g3, _SU3, _LAB3, ck, "SU(3) claw3 baryon")
    wit = ((1, 0), (1, 0), (1, 0), (0, 0))
    ck(wit in cfg3 and len(cfg3) == 2
       and all(c[3] in ((0, 0), (1, 1)) for c in cfg3),
       "BARYON EXHIBIT: three (1,0) sources (triality 0) admit the fully "
       "contained witness -- (1,0) edges into the hub (3x3x3 singlet, "
       "computed), trivial tail; admissible set exactly {witness, "
       "adjoint-dressed tail} (exhaustive at the cap; the (1,1) tail is "
       "charge-trivial but label-nonzero, computed)")
    g2 = _claw(2)
    cfg2 = _enum(g2, _SU3, _LAB3)
    ck(len(cfg2) > 0
       and all(_SU3['q'](c[2]) % 3 == 2 for c in cfg2)
       and f3((1, 0), (1, 0)).get((0, 0), 0) == 0,
       "BARYON EXHIBIT, converse: two (1,0) sources (triality 2) CANNOT "
       "be contained -- every admissible configuration (exhaustive at "
       "the cap) carries triality-2 charge out through the tail; pairs "
       "do not screen in SU(3), triples do (ONE computed admissibility "
       "exhibit at cap p+q <= 2 on the walked claw graphs, no further "
       "claims)")

    # ---- (8) negative controls -------------------------------------------
    bq2 = dict(_SU2)
    bq2['q'] = lambda a: 1 if a == 2 else a % 2
    nvb, _ = _hhom_viol(bq2, [(a, b) for a in range(7) for b in range(7)])
    bq3 = dict(_SU3)
    bq3['q'] = lambda t: t[0] % 3
    nvb3, _ = _hhom_viol(bq3, [(a, b) for a in l3 for b in l3])
    ck(nvb > 0 and nvb3 > 0,
       "negative control: broken (non-homomorphic) charge maps are "
       "DETECTED by the H-hom battery in both instances (the battery can "
       "fail; not theater)")
    sab_bad = sum(1 for a in l3 for b in l3
                  if sum(m * _su3_dim(*c) for c, m in dict(
                      list(_su3_fuse(a, b).items())
                      + [((a[0] + b[0] + 1, a[1] + b[1]),
                          _su3_fuse(a, b).get(
                              (a[0] + b[0] + 1, a[1] + b[1]), 0) + 1)]
                  ).items()) == _su3_dim(*a) * _su3_dim(*b))
    ck(sab_bad == 0,
       "negative control: a sabotaged SU(3) rule (spurious constituent "
       "injected) fails dimension counting on ALL 81 grid pairs -- the "
       "corroboration leg is live")
    for src in ((1, 0), (0, 1), (2, 0)):
        gp = _path(2, None)
        gp['sources'] = {'v0': src}
        ck(_singlet(_SU3, _content(gp, ((0, 0), (0, 0)), 'v0', _SU3)) == 0,
           f"negative control: triality-nonzero SU(3) source {src} with "
           "all-trivial links is inadmissible at the source vertex "
           "(computed)")

    # ---- (9) hygiene: honesty sweep + vocabulary fence -------------------
    with open(__file__, 'r') as fh:
        src_text = fh.read()
    tree = ast.parse(src_text)
    floats = [n for n in ast.walk(tree) if isinstance(n, ast.Constant)
              and isinstance(n.value, (float, complex))]
    ck(not floats, "zero float/complex constants in this module's AST "
       "(pure integer arithmetic)")
    msgs, offend = [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == 'ck':
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and isinstance(sub.value,
                                                                str):
                    msgs.append(sub.value)
                if isinstance(sub, ast.FormattedValue):
                    for b in ast.walk(sub.value):
                        if isinstance(b, ast.BinOp) \
                                and isinstance(b.op, (ast.Add, ast.Sub)):
                            for side in (b.left, b.right):
                                if isinstance(side, ast.Constant) \
                                        and isinstance(side.value, int) \
                                        and abs(side.value) > 2:
                                    offend.append(ast.dump(b)[:60])
    stems = ('magnitude', 'tension', 'spectral', 'continuum', 'occupanc',
             'hold', 'quantum', 'selection', 'energ')
    hits = [(w, m) for m in msgs for w in stems if w in m.lower()]
    ck(len(msgs) >= 30 and not hits and not offend,
       f"vocabulary fence (nine stems, zero hits over {len(msgs)} "
       "message strings) and arithmetic-honesty sweep (zero opaque "
       "additive constants interpolated into any message value -- the "
       "lane's M1 audit shape, asserted here too)")

    passed = not fails
    return {
        'name': 'L_center_flux_exit',
        'epistemic': ('P_math | electric-basis model convention + '
                      'per-vertex-singlet admissibility (Gauss reading a '
                      'named identification) + H-hom as named hypothesis '
                      '-- for the abstract Z_N law; enumeration legs and '
                      'the baryon exhibit instance-scoped [P] at stated '
                      'caps and walked graphs'),
        'passed': passed,
        'tier': 4,
        'key_result': (
            'In the named oriented electric-basis lattice model (label r '
            'at head, conj(r) at tail -- flip-covariance computed; '
            'self-loops both-slots-own-vertex and never cut; multi-edges '
            'independent; boundary unconstrained; admissibility DEFINED '
            'as per-vertex trivial-irrep existence, Gauss reading a named '
            'identification) and under NAMED H-hom (center charge a '
            'fusion homomorphism): (i) singlet existence forces total '
            'charge == 0 mod N (H-hom step + depth induction); (ii) '
            'outward flux charge through every bipartition cut delta(S), '
            'S interior, == enclosed source charge mod N, carried by the '
            'per-edge-computed signed handshake identity (exact Z-linear '
            'coefficients, executed per edge of arbitrary graphs incl. '
            'self-loops/multi-edges); (iii) charge != 0 mod N forces >= 1 '
            'charge-nonzero edge per such cut and >= L across a nested '
            'disjoint family. Computed at N=2 -- SU(2) fusion CONSTRUCTED '
            'in-module (character route, agreement with the banked rule '
            'computed; the SU(2)-only candidate absorbed as this '
            'instance) with signed == unsigned mod 2 per configuration '
            'per cut -- and at N=3 -- SU(3) constructed twice in-module '
            '(GT + LR), fusion table computed, triality H-hom '
            'grid-verified; at cap p+q <= 2 a (1,0) source forces exit '
            'with an exact-L string witness, the adjoint admits a '
            'bounded contained screen constant in L, and three '
            'fundamentals admit full containment (3x3x3 singlet, exactly '
            'one) while two provably cannot (both exhaustive on the '
            'walked claws). Abstract for other N under H-hom only; no '
            'SU(N>3) claim; upstream of the confinement parent\'s named '
            'support-reading premise; kinematic admissibility only.'
        ),
        'dependencies': ['T_su2_string_cut_comovement'],
        'cross_refs': ['T_su2_string_cut_native_algebra',
                       'T_center_order_parameter_triality',
                       'L_frustrated_witness',
                       'T_anchor_set_is_electric_center_data',
                       'T_anchor_support_formalization'],
        'artifacts': {
            'witnesses': ('SU(2) table 1x1=0+2, 2x2=0+2+4; SU(3) table '
                          '3x3bar=1+8, 3x3=3bar+6 (no singlet), '
                          '8x8=1+8+8+10+10bar+27, 3x3x3 singlet '
                          'multiplicity EXACTLY 1; baryon claw3: 2 '
                          'admissible configurations incl. the fully '
                          'contained witness; claw2: all admissible '
                          'configurations carry triality-2 flux out; '
                          'adjoint screen support 3, admissible count 11 '
                          'constant over TT(1..3); parity pins full to '
                          '20 here / 40 in the lane walker, sparse '
                          'step-13/17 to 195/187'),
            'premise_stack': ('electric-basis frame convention '
                              '(consumed-banked, comovement anchor run '
                              'live) + per-vertex-singlet model '
                              'DEFINITION (Gauss reading a named '
                              'identification) + H-hom named hypothesis '
                              '(grid-computed at N=2,3)'),
            'named_imports': ('_su2_tensor emission shape outside the '
                              'verified grids (the W1-UNIV leg-iii '
                              'import; audit-confirmed wherever probed); '
                              'H-hom beyond the computed grids'),
            'kill_condition': ('an H-hom violation at any computed '
                               'instance refutes that instantiation; a '
                               'construction-flag trip (character or '
                               'lex-subtraction) kills the construction '
                               'legs -- both asserted 0 here and in the '
                               'lane walker'),
            'may_not_cite': ('no cut-equality for arbitrary separating '
                             'edge sets (delta(S)-scoped; parent '
                             'counterexample travels); screens '
                             'existence-only under the named cycle '
                             'condition, never as selected; H-hom a '
                             'named hypothesis beyond grids; no graph '
                             'generality beyond the executed per-edge '
                             'derivation; no confinement-parent '
                             'consumption without the support-reading '
                             'premise named; SU(2) candidate superseded '
                             'for theorem content only (its lane record '
                             'stands); no SU(N>3); no magnitude/tension/'
                             'spectral/continuum/dynamics claim; the '
                             'composed reading sentence not licensed'),
            'audit_record': ('AUDIT_center_flux_stage1.md LAND-WITH-FIXES '
                             '0.90 (REOPENER (a)+(b) ruled DISCHARGED, '
                             'grade line GRANTED; SU(3) third/fourth '
                             'routes agreed; triangularity CERTIFIED; '
                             'this is the certification\'s location of '
                             'record) + AUDIT_center_flux_stage2.md LAND '
                             '0.93 (all fixes verified; banking-shape '
                             'preconditions, carried in this entry); '
                             'bank-side re-run = walker v2 (4397, exit 0) '
                             '+ _audit_probes_cfx.py (39/39)'),
            'supersedes': ('check_L_lattice_gauss_parity_flux_exit '
                           '(never banked) ABSORBED as the N = 2 '
                           'instance; parent grade of record '
                           '[P_structural | named stack] superseded for '
                           'THEOREM CONTENT ONLY; parent enumeration '
                           'facts keep their scoping; parent lane record '
                           'HELD; parent T-c screen content NOT part of '
                           'this candidate beyond the SU(3) (1,1) '
                           'exhibit'),
            'lane_records': ('flux_exit_parity_2026-07-10 (walker v2 6446 '
                             'checks) + flux_exit_zn_2026-07-10 (walker '
                             'v2 4397 checks, CENTER_FLUX_NOTE_v0.2) + '
                             'both audit reports'),
        },
        'fail_reasons': fails,
        'n_checks': n_checks[0],
    }


_CHECKS = {'L_center_flux_exit': check_L_center_flux_exit}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.environ.get('APF_TREE', '/home/claude/lane'))
    r = check_L_center_flux_exit()
    print(r['name'], 'PASS' if r['passed'] else 'FAIL',
          f"({r['n_checks']} checks)")
    if not r['passed']:
        for f in r['fail_reasons']:
            print('  -', f)
    sys.exit(0 if r['passed'] else 1)
