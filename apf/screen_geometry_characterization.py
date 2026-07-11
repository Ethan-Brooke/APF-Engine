"""Screen-geometry characterization: the per-instance CONTAINED-screen
class condition on the banked electric model -- computed-family-exact on
the lane-walked labeled family, with the charge / local-attachment /
geometry clauses and the F2/F3/F4/F6 audit riders IN the statement, the
containment-vs-screen-supporting vocabulary split carried, and the
G(d, m) threshold law in the grid-scoped F1 wording.

T_screen_containment_characterization.  THE STATEMENT (per fusion cell
(instance, source irrep a, cap), on LABELED connected simple graphs;
billed computed-family-exact, never "for all graphs"; hostile-audit
fixes F2/F3/F4 carried IN the statement, LAND-WITH-FIXES 0.92):
  RIDER (F4, part of the statement): CAPS CONJ-CLOSED.  Off conj-closed
  caps containment is orientation-dependent -- the audit's computed
  witness: at cap {unit, (1,0)} the cyclically oriented triangle
  carries a contained nonunit configuration and ONE edge flip kills it
  (recomputed in this battery) -- so no orientation-blind graph
  condition can exist there.  Every walked cap is conj-closed
  (asserted in-battery).
  A contained admissible screen for source a at vertex s with boundary
  B exists  IFF
    (1) [charge] q(a) == 0 mod N,  AND
    (2) [local attachment] delta_{<=kmax}(a, cap) is finite, kmax = 6
        STATED IN THE DEFINITION (F3): the minimal size k <= kmax of a
        multiset of nonunit cap-labels whose fusion with a contains the
        unit.  The kmax subscript is load-bearing -- the audit exhibit
        SU(2) a=14 cap 2 has true attachment size 7 (seven adjoints
        close it, six do not) and reads None at kmax 6: a FINITE delta
        silently read as infinite without the rider (witness recomputed
        in-battery),  AND
    (3) [geometry, BANKED AT delta in {1, 2} ONLY -- the walked values
        (F2)]: for delta = 1, s reaches a cycle inside I = G - B; for
        delta = 2, s lies in the 2-core of I.
  The general form of clause (3) -- "I contains a connected subgraph
  H with s in H, deg_H(s) >= delta, deg_H(v) >= 2 for every v != s" --
  is a STATEMENT-SHAPE only, verified at delta in {1, 2}; the audit's
  delta=3 exhibits (a=6 cap 2, a=10 cap 4, and the mixed-multiset-only
  a=8 cap 3, zero-mismatch on the full lane family) are AUDIT RECORD,
  citable as corroboration only, never as theorem content.

CONTAINED is the per-instance predicate: an admissible configuration
(exhaustively enumerated at cap on the banked constructed rules) whose
support touches no boundary-incident edge.  CONTAINED is NOT the banked
family-level SCREEN-SUPPORTING predicate (depth-constant support,
crossing no family cut) -- the vocabulary split is load-bearing and the
audit ruled it "must survive distillation intact".  The farcyc family
SEPARATES the two: contained per instance at support exactly L + 2
(growing with L, still crossing the L-1 path cuts), NOT
screen-supporting per family -- the bank's family verdict is
reproduced, not contradicted (recomputed in-battery at L = 2, 3).

FAMILY OF RECORD (lane record; count discipline per F6): every LABELED
connected simple graph on 2..5 vertices (counts 1, 4, 38, 728) x every
source vertex x every nonempty boundary set = 55,702 labeled instances,
isomorphs counted separately -- deduplicating to 677 isomorphism
classes (deflation x82), 285 canonical interiors per cell, 16 true
isomorphism classes of (source component, source) -- across SEVEN
fusion cells (SU(2) a=2 cap 2 / a=4 cap 2 / a=4 cap 4 / a=1 cap 2
charge control; SU(3) (1,1) / (3,0) / (1,0) charge control, cap
p+q <= 2): condition <=> containment, EXACT, ZERO MISMATCHES; cell
collapse computed as set identity (A == C == E and B == F -- the
fusion cell enters only through (q == 0, delta)); B properly contained
in A.  n = 6, 7 covered by seeded corroboration sweeps; multigraph
legs two spot instances (self-loop / doubled edge: clause (3) read in
the multigraph sense).  That 55,702 x 7 enumeration is the LANE
RECORD, not rerun here.  THIS DISTILLED BATTERY re-verifies the
characterization EXHAUSTIVELY on the REDUCED STATED FAMILY: every
LABELED connected simple graph on 2..4 vertices (counts 1, 4, 38;
1,102 labeled instances, isomorphs counted separately -- 65
isomorphism classes, 64 interior cache keys, 5 canonical interiors,
all computed in-module) x four cells (SU(2) a=2 cap 2; SU(2) a=4
cap 2; SU(3) (1,1) cap 2; SU(2) a=1 cap 2 charge control), zero
mismatches, plus the pinned witnesses below; exact integer arithmetic
only (AST-asserted).

LEG 3, THE THRESHOLD LAW (audit fix F1, the audit's grid-scoped
wording adopted verbatim): "On the computed grid (d = 0..5, m = 1..4
at cap 2, a = 2; cap-3 and SU(3) adjoint spots as stated), minimal
contained support = d + 3 exactly, independent of m; hence along any
receding family whose parameters stay within the computed grid,
depth-constant contained support exists iff d is constant there.  The
unbounded-d 'the boundary IS d-boundedness' reading is the computed
shape extrapolated, not a theorem."  The three banked families are the
three lines of G(d, m): TT(L) = G(0, L), nearcyc(L) = G(1, L),
farcyc(L) = G(L-1, 1) (identifications computed in the lane; farcyc
identification recomputed here).  Minimal admissible support =
min(d+m, d+3).  This battery recomputes the REDUCED grid d = 0..3,
m = 1..2.  The law is support arithmetic -- existence facts only.

DERIVATION TRAIL (each refinement forced by a computed counterexample;
kept here as negative controls):
  v0 (geometry + attachment, NO charge clause): REFUTED -- pinned
      witness: triangle 0-1-2, source a=1 at 0, pendant boundary 3
      (locally closable, cycle through the source, yet NO contained
      configuration -- the consumed flux-exit singlet law is GLOBAL;
      recomputed in-battery with the full reduced-family mismatch set).
  v0' (cycle ANYWHERE in I, reachability dropped): REFUTED -- pinned
      witness: source 0 joined through boundary vertex 1 to triangle
      2-3-4 (interior holds a cycle, s isolated from it; recomputed
      in-battery as a spot instance).  Reachability is load-bearing.
  v1 = the three-clause condition above: exact on the stated families.

PREMISE STACK (consumed, named):
  1. The banked electric model (CONSUMED, BANKED): oriented edges,
     label r at head / conj(r) at tail, per-vertex-singlet
     admissibility as MODEL DEFINITION (its Gauss reading a NAMED
     IDENTIFICATION, computed nowhere) -- apf/center_flux_exit.py run
     LIVE as anchor with its grade line pinned [P_math | electric-basis
     model convention + per-vertex-singlet admissibility (Gauss reading
     a named identification) + H-hom named hypothesis]; its
     MAY-NOT-CITE travels.
  2. Constructed SU(2)/SU(3) fusion rules (CONSUMED, BANKED): all
     tensor arithmetic runs on the banked module's constructed rules
     via its own _singlet/_enum -- no new fusion; this module is
     geometry.
  3. The screen-supporting vocabulary (CONSUMED, BANKED):
     apf/frustration_center_partition.py run LIVE as anchor
     (P_structural | nine-item stack); its walked inventory is the
     banked instance layer this condition characterizes per-instance.
  4. Cap/family scoping: every claim at stated caps on the stated
     enumerated families; class sentences computed-family-exact.
  5. A1 deliberately NOT consumed (house precedent: the flux-exit
     module's dependency argument) -- pure model mathematics on a
     named model.

MAY-NOT-CITE (citation without the premise stack is misciting):
  - NOTHING beyond the stated caps/family: the condition is exact on
    LABELED connected simple graphs, 2..5 vertices, all sources, all
    nonempty boundaries, at the stated caps, on the seven stated cells
    (lane record; reduced 2..4-vertex four-cell re-verification here);
    the n = 6/7 legs are seeded sweeps; the multigraph legs are two
    spot instances.  NO "for all graphs" sentence exists.
  - NO new cells for free: delta and the q clause are computed per
    (a, cap); citing the condition for an unwalked cell (any SU(N>3),
    any other cap, any other source) is misciting.  delta >= 3 cells
    were never walked (delta in {1, 2} on all walked cells).
  - SUFFICIENCY IS EXHAUSTION-ONLY (the audit's flagged flank, live):
    necessity and the charge clause are argument-backed; a
    counterexample at n >= 8, or in an unwalked cell whose
    delta-realizing multisets interact with geometry in a way no
    walked or audited cell exhibits, remains logically open -- the
    NAMED standing flank.  The audit's mixed-only delta=3 probe was
    the natural first such attack and failed to kill.
  - NO unbounded receding-family iff: the threshold-law boundary
    sentence exists ONLY in the grid-scoped F1 wording above; the
    unbounded-d reading is the computed shape extrapolated, not a
    theorem.
  - CONTAINMENT != SCREEN-SUPPORTING: the per-instance predicate
    characterized here does NOT replace the banked family-level
    proviso; farcyc is contained-per-instance and still NOT
    screen-supporting.  Citing this condition as "screen-supporting
    characterized" is misciting.
  - The general clause-(3) deg_H(s) >= delta shape is NEVER cited as a
    theorem (statement-shape; audit delta=3 exhibits corroboration
    only).
  - The threshold law is support arithmetic (existence facts); no
    billing, argmin, or frustration composition is licensed here --
    that is frustration_center_partition's layer under rulings 3a/4a,
    and "whether a screen is taken" stays the parent lanes'
    convention.
  - All parent fences travel: no cut equality for arbitrary separating
    edge sets (delta(S)-scoped only); H-hom named beyond computed
    grids; screens existence-only; no reading sentence; no dynamics /
    tension law / gap value / continuum claim; fixed-L partition dead;
    no SU(N > 3).

KILL MODE (loud): a counterexample instance in any walked cell -- a
single condition-vs-containment mismatch -- kills the characterization
as stated (the sweeps print it; the flip probe shows the harness is
instance-sharp).  An H-hom or construction-flag trip upstream kills
the consumed fusion legs.  A contained configuration on a walked tree
kills clause (3)'s necessity AND the banked clause (ii) with it.  A
grid point with minimal contained support != d + 3 kills the
threshold law.

AUDIT RECORD (hostile audit 2026-07-11, LAND-WITH-FIXES 0.92, no
kill): independent re-verification 389,914 decisions, ZERO mismatches,
on disjoint fusion routes (SU(2) character route; SU(3) Schur/SSYT-
alternant route), own enumerator, NO interior-component reduction --
including the closed C/D/F/G cross-validation gap (exposure real,
closed empty: banked-_enum oracle vs audit decision, exhaustive
n <= 4 per cell + 120 seeded n = 5 draws for F, zero disagreements),
three unwalked delta=3 cells (incl. the mixed-multiset-only a=8
cap 3 -- the sufficiency flank held), and fresh-seed n = 6 draws;
mutation hardness 5/5.  Banking shape audit-approved conditional on
F1-F6, all carried (F1 grid wording; F2 delta-scope; F3 kmax; F4
conj-closure; F5 the .417 disposition below; F6 labeled counts).

THE .417 LINE -- DISPOSITION OF RECORD (audit ruling, adopted; the
.417-side edit is executed SEPARATELY by the main seat at banking, not
in this module): the banked sentence in
apf/frustration_center_partition.py -- "no graph-class
characterization theorem exists anywhere in the bank" -- is RETAINED,
never rewritten, with a pointer APPENDED at banking time: "(per-
instance CONTAINMENT is characterized on a stated exhaustive labeled
family by check_T_screen_containment_characterization, v24.3.418+; the
family-level SCREEN-SUPPORTING predicate -- depth-constant, cut-free
-- remains without a general characterization; farcyc separates the
two.)"  This is bank-history discipline AND substantively accurate:
this module's theorem characterizes the per-instance predicate;
re-scoped to the family-level screen-supporting notion, the original
line stays true.

GRADE [P | banked electric model + constructed-rule consumption +
stated caps/family + the F2/F3/F4/F6 riders in the conditioning text]
(audit ruling: holds at instance scope; charter ceiling instance [P]).
Tier 4.

Lane record: The Turning (parked)/screen_geometry_2026-07-11/
(walk_screen_geometry.py, 138 checks, exit 0, fixes F1-F6 carried;
WALK_NOTE.md; AUDIT_REPORT.md LAND-WITH-FIXES 0.92 + audit probes
32/32 and 22/22).  This module banks the DISTILLED battery; the walker
is the lane record.  Version narrative: banked v24.3.421 (2026-07-11).
"""

from itertools import combinations, combinations_with_replacement, \
    permutations
import ast


# ---------------------------------------------------------------------------
# graph machinery (module-local; all fusion arithmetic is consumed from the
# banked center-flux module inside the check)
# ---------------------------------------------------------------------------
def _conn_graphs(n):
    """All labeled connected simple graphs on vertices 0..n-1
    (exhaustive edge-mask enumeration + connectivity)."""
    pairs = list(combinations(range(n), 2))
    out = []
    for mask in range(1 << len(pairs)):
        E = tuple(pairs[i] for i in range(len(pairs)) if mask >> i & 1)
        adj = {v: set() for v in range(n)}
        for x, y in E:
            adj[x].add(y)
            adj[y].add(x)
        seen = {0}
        st = [0]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    st.append(w)
        if len(seen) == n:
            out.append(E)
    return out


def _comp_of(V, E, s):
    adj = {v: set() for v in V}
    for x, y in E:
        adj[x].add(y)
        adj[y].add(x)
    seen = {s}
    st = [s]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                st.append(w)
    return seen


def _two_core(V, E):
    Vs = set(V)
    Es = list(E)
    changed = True
    while changed:
        changed = False
        deg = {v: 0 for v in Vs}
        for x, y in Es:
            deg[x] += 1
            deg[y] += 1
        drop = {v for v in Vs if deg[v] <= 1}
        if drop:
            changed = True
            Vs -= drop
            Es = [(x, y) for x, y in Es if x in Vs and y in Vs]
    return Vs, Es


def _canon_triple(n, E, s, B):
    """Canonical representative of the labeled (graph, source, boundary)
    triple under vertex relabelling, source pinned to 0 (F6: labeled
    counts stated WITH their isomorphism-class deflation, computed)."""
    others = [v for v in range(n) if v != s]
    best = None
    for p in permutations(range(1, n)):
        m = {s: 0}
        for v, pv in zip(others, p):
            m[v] = pv
        t = (tuple(sorted(tuple(sorted((m[x], m[y]))) for x, y in E)),
             tuple(sorted(m[b] for b in B)))
        if best is None or t < best:
            best = t
    return best


def _canon_interior(comp, CE, s):
    """Canonical representative of the source's interior component,
    source pinned to 0 (F6: canonical-interior count)."""
    others = sorted(v for v in comp if v != s)
    best = None
    for p in permutations(range(1, len(comp))):
        m = {s: 0}
        for v, pv in zip(others, p):
            m[v] = pv
        Ep = tuple(sorted(tuple(sorted((m[x], m[y]))) for x, y in CE))
        if best is None or Ep < best:
            best = Ep
    return best


def _delta_of(inst, a, labels, kmax, singlet):
    """delta_{<=kmax}(a, cap): the minimal size k <= kmax of a multiset
    of nonunit cap-labels whose fusion with a contains the unit (F3:
    kmax stated in the definition; None if no multiset <= kmax
    closes)."""
    un = inst['unit']
    nz = [x for x in labels if x != un]
    for k in range(1, kmax + 1):
        for m in combinations_with_replacement(nz, k):
            if singlet(inst, (a,) + m) > 0:
                return k
    return None


def _adm_exists(V, E, src_v, src_irrep, inst, labels, singlet,
                singlet_fn=None):
    """EXISTENCE of an admissible configuration on a closed graph (every
    vertex interior/constrained), early exit; the same per-vertex-singlet
    predicate as the banked _enum (singlet_fn overridable for the
    broken-fusion mutation probe only)."""
    sf = singlet_fn or (lambda labs: singlet(inst, labs))
    un = inst['unit']
    E = list(E)
    incid = {v: [i for i, (x, y) in enumerate(E) if v in (x, y)]
             for v in V}
    for v in V:
        if not incid[v]:
            cont = ((src_irrep,) if (v == src_v and src_irrep != un)
                    else ())
            if cont and sf(cont) == 0:
                return False
    if not E:
        return True
    order, rem = [], set(range(len(E)))
    remdeg = {v: len(incid[v]) for v in V}
    while rem:
        best = min(rem, key=lambda i: remdeg[E[i][0]] + remdeg[E[i][1]])
        rem.discard(best)
        order.append(best)
        for v in E[best]:
            remdeg[v] -= 1
    E2 = [E[i] for i in order]
    incid2 = {v: [i for i, (x, y) in enumerate(E2) if v in (x, y)]
              for v in V}
    complete_at = {}
    for v in V:
        if incid2[v]:
            complete_at.setdefault(max(incid2[v]), []).append(v)
    cfg = [un] * len(E2)
    conj = inst['conj']

    def content(v):
        out = []
        for i in incid2[v]:
            x, y = E2[i]
            if y == v:
                out.append(cfg[i])
            if x == v:
                out.append(conj(cfg[i]))
        if v == src_v and src_irrep != un:
            out.append(src_irrep)
        return tuple(out)

    def rec(i):
        if i == len(E2):
            return True
        for lab in labels:
            cfg[i] = lab
            ok = True
            for v in complete_at.get(i, ()):
                if sf(content(v)) == 0:
                    ok = False
                    break
            if ok and rec(i + 1):
                return True
        cfg[i] = un
        return False

    return rec(0)


def _screen_exists(V, E, B, s, a, inst, labels, singlet, cache,
                   singlet_fn=None):
    """CONTAINED predicate via the interior-component reduction (the
    equivalence with the banked full-graph predicate is cross-validated
    in-battery, not assumed).  Cache key: the exact interior component
    of s (raw vertex labels)."""
    IE = [(x, y) for x, y in E if x not in B and y not in B]
    comp = _comp_of([v for v in V if v not in B], IE, s)
    CE = tuple(sorted((x, y) for x, y in IE if x in comp))
    key = (frozenset(comp), CE, s)
    if singlet_fn is None and key in cache:
        return cache[key]
    r = _adm_exists(sorted(comp), CE, s, a, inst, labels, singlet,
                    singlet_fn)
    if singlet_fn is None:
        cache[key] = r
    return r


def _contained_full(V, E, B, s, a, inst, labels, enum):
    """The banked containment predicate on the FULL graph: exhaustive
    _enum (the banked enumerator), then existence of a configuration
    whose boundary-incident edges all carry the unit label -- the TT
    zero-tail / claw trivial-tail shape, verbatim."""
    g = {'V': list(V), 'E': list(E), 'boundary': frozenset(B),
         'sources': {s: a}}
    adm = enum(g, inst, labels)
    bidx = [i for i, (x, y) in enumerate(E) if x in B or y in B]
    un = inst['unit']
    return any(all(c[i] == un for i in bidx) for c in adm)


def _condition_v1(V, E, B, s, q_zero, delta):
    """The banked characterization, final form (three clauses; clause
    (3) instantiated at delta in {1, 2} ONLY -- F2)."""
    if not q_zero or delta is None:
        return False
    IV = [v for v in V if v not in B]
    IE = [(x, y) for x, y in E if x not in B and y not in B]
    if delta == 1:
        comp = _comp_of(IV, IE, s)
        CE = [(x, y) for x, y in IE if x in comp]
        return len(CE) >= len(comp) and len(CE) > 0
    if delta == 2:
        cv, _ = _two_core(IV, IE)
        return s in cv
    raise ValueError("delta outside the banked range")


def _condition_v0p(V, E, B, s, q_zero, delta):
    """REFUTED candidate v0': cycle ANYWHERE in the interior graph
    (reachability dropped); delta-1 shape only (negative control)."""
    if not q_zero or delta is None:
        return False
    IV = [v for v in V if v not in B]
    IE = [(x, y) for x, y in E if x not in B and y not in B]
    cv, _ = _two_core(IV, IE)
    return len(cv) > 0


def _supports(g, inst, labels, enum):
    """(admissible count, min support, min CONTAINED support) by the
    banked exhaustive enumerator on the full graph."""
    adm = enum(g, inst, labels)
    un = inst['unit']
    bidx = [i for i, (x, y) in enumerate(g['E'])
            if x in g['boundary'] or y in g['boundary']]
    minall = (min(sum(1 for x in c if x != un) for c in adm)
              if adm else None)
    contained = [c for c in adm if all(c[i] == un for i in bidx)]
    minc = (min(sum(1 for x in c if x != un) for c in contained)
            if contained else None)
    return len(adm), minall, minc


def _cyc_at(d, m, src):
    """The Leg-3 two-parameter family G(d, m): source s0, path of length
    d to junction t, triangle at t, tail of length m to the boundary."""
    V = (['s0'] + [f"x{i}" for i in range(1, d + 1)] + ['w1', 'w2']
         + [f"y{i}" for i in range(1, m + 1)])
    t = 's0' if d == 0 else f"x{d}"
    E = []
    prev = 's0'
    for i in range(1, d + 1):
        E.append((prev, f"x{i}"))
        prev = f"x{i}"
    E += [(t, 'w1'), ('w1', 'w2'), ('w2', t)]
    prev = t
    for i in range(1, m + 1):
        E.append((prev, f"y{i}"))
        prev = f"y{i}"
    return {'V': V, 'E': E, 'boundary': frozenset([f"y{m}"]),
            'sources': {'s0': src}}


def _sweep_cell(CG, inst, a, labels, cond, singlet, flip_key=None,
                singlet_fn=None):
    """Exhaustive sweep over the REDUCED stated family: every labeled
    connected simple graph on 2..4 vertices, every source, every
    nonempty boundary.  Returns stats, the mismatch list, and the
    per-instance screen bits (for cross-cell set identity)."""
    cache = {}
    tot = scr = 0
    mism = []
    bits = []
    for n in (2, 3, 4):
        V = list(range(n))
        for E in CG[n]:
            for s in range(n):
                others = [v for v in V if v != s]
                for r in range(1, n):
                    for Bc in combinations(others, r):
                        B = frozenset(Bc)
                        tot += 1
                        se = _screen_exists(V, E, B, s, a, inst, labels,
                                            singlet, cache, singlet_fn)
                        if flip_key == (n, E, s, B):
                            se = not se
                        co = cond(V, E, B, s)
                        scr += se
                        bits.append(se)
                        if se != co:
                            mism.append((n, E, s, tuple(sorted(B)),
                                         se, co))
    return {'tot': tot, 'scr': scr, 'mism': mism, 'cache': len(cache),
            'bits': tuple(bits)}


def check_T_screen_containment_characterization():
    """T_screen_containment_characterization: the three-clause
    per-instance containment characterization (charge / delta_{<=6}
    attachment / delta-instantiated geometry, conj-closed caps), exact
    on the stated labeled family, with the containment-vs-screen-
    supporting split and the grid-scoped threshold law.  See the module
    docstring for the statement with all riders, premise stack,
    MAY-NOT-CITE fences, kill mode, audit record, and the .417
    disposition.  This is the DISTILLED battery; the 138-check lane
    walker (55,702 x 7 enumeration) is the lane record."""
    from apf.center_flux_exit import (_SU2, _SU3, _singlet, _enum,
                                      check_L_center_flux_exit)
    from apf.frustration_center_partition import (
        _farcyc, _cuts, _slots,
        check_T_frustration_center_partition)

    fails = []
    n_checks = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        n_checks[0] += 1

    LAB2 = [0, 1, 2]
    LAB4 = [0, 1, 2, 3, 4]
    LAB3 = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]  # p+q <= 2

    # ---- S0: live bank anchors (BOTH deps consumed live; grade lines
    # pinned; their fences travel) ----------------------------------------
    r_cfx = check_L_center_flux_exit()
    ck(r_cfx.get('passed') is True
       and r_cfx.get('epistemic', '').startswith(
           'P_math | electric-basis model convention')
       and 'H-hom' in r_cfx.get('epistemic', ''),
       "S0: anchor L_center_flux_exit passes LIVE with its grade line "
       "pinned (P_math | electric-basis convention + per-vertex singlet "
       "+ H-hom named hypothesis) -- its constructed fusion rules and "
       "enumerator are THE tools consumed below; its MAY-NOT-CITE "
       "travels (no arbitrary-separating-set cut equality, screens "
       "existence-only, H-hom named beyond grids, no SU(N>3))")
    r_fcp = check_T_frustration_center_partition()
    ck(r_fcp.get('passed') is True
       and r_fcp.get('epistemic', '').startswith('P_structural |'),
       "S0: anchor T_frustration_center_partition passes LIVE "
       "(P_structural | nine-item stack) -- the module whose banked "
       "SCREEN-SUPPORTING proviso this condition characterizes "
       "PER-INSTANCE; its family-level predicate is NOT replaced (the "
       "vocabulary split below)")
    ck('SCREEN-SUPPORTING' in r_fcp.get('artifacts', {}).get(
        'screen_proviso', ''),
       "S0: content pin -- the anchor's returned screen_proviso "
       "artifact carries the family-level vocabulary this module keeps "
       "distinct from per-instance containment")

    # ---- S1: the fusion cells -- charge and attachment numbers on the
    # banked constructed rules, with the F3 kmax witness -------------------
    d_a2 = _delta_of(_SU2, 2, LAB2, 6, _singlet)
    d_a4c2 = _delta_of(_SU2, 4, LAB2, 6, _singlet)
    d_a1 = _delta_of(_SU2, 1, LAB2, 6, _singlet)
    d_adj = _delta_of(_SU3, (1, 1), LAB3, 6, _singlet)
    ck(d_a2 == 1 and d_adj == 1 and d_a4c2 == 2 and d_a1 == 1,
       "S1: attachment numbers on the banked rules -- delta(a=2, cap 2) "
       "== delta((1,1), cap 2) == 1, delta(a=4, cap 2) == 2 (a pair of "
       "adjoints closes it, no single cap-2 label does), delta(a=1, "
       "cap 2) == 1 (locally closable yet charged: the two clauses are "
       "independent -- v0's refutation below)")
    ck(_SU2['q'](2) == 0 and _SU2['q'](4) == 0 and _SU2['q'](1) == 1
       and _SU3['q']((1, 1)) == 0,
       "S1: charge-clause inputs on the banked q maps (q(a=2) == "
       "q(a=4) == q((1,1)) == 0; q(a=1) == 1 -- the control cell)")
    d14 = _delta_of(_SU2, 14, LAB2, 6, _singlet)
    ck(d14 is None and _singlet(_SU2, (14,) + tuple([2] * 7)) > 0
       and _singlet(_SU2, (14,) + tuple([2] * 6)) == 0,
       "S1 (F3 witness recomputed): SU(2) a=14 at cap 2 has true "
       "attachment size 7 (seven adjoints close it, six do not, "
       "computed on the banked rule) yet reads None at kmax 6 -- a "
       "FINITE attachment silently read as infinite; clause (2) is "
       "therefore delta_{<=kmax} WITH kmax = 6 stated in the "
       "definition, never an uncapped delta (on the walked cells delta "
       "is found at k <= 2, so the rider costs nothing there)")
    ck(all(_singlet(_SU2, tuple([2] * k)) > 0 for k in (2, 3, 4, 5, 6))
       and all(_singlet(_SU3, tuple([(1, 1)] * k)) > 0
               for k in (2, 3, 4, 5)),
       "S1: glue facts -- singlet in 2^(x)k (k = 2..6) and 8^(x)k "
       "(k = 2..5), computed: uniform-adjoint labellings close every "
       "vertex of degree >= 2 (the sufficiency construction's local "
       "input; sufficiency itself stays EXHAUSTION-ONLY, the named "
       "standing flank)")

    # ---- S2: the reduced stated family + F6 count discipline -------------
    CG = {n: _conn_graphs(n) for n in (2, 3, 4)}
    ck([len(CG[n]) for n in (2, 3, 4)] == [1, 4, 38],
       f"S2: reduced family generation -- labeled connected simple "
       f"graph counts {[len(CG[n]) for n in (2, 3, 4)]} on 2..4 "
       "vertices (exhaustive edge-mask enumeration + connectivity, "
       "computed; the lane family's 2..4 prefix)")
    n_inst = sum(len(CG[n]) * n * (2 ** (n - 1) - 1) for n in (2, 3, 4))
    iso_reps = set()
    int_keys = set()
    for n in (2, 3, 4):
        V = list(range(n))
        for E in CG[n]:
            for s in range(n):
                others = [v for v in V if v != s]
                for r in range(1, n):
                    for Bc in combinations(others, r):
                        B = frozenset(Bc)
                        iso_reps.add((n, _canon_triple(n, E, s, B)))
                        IE = [(x, y) for x, y in E
                              if x not in B and y not in B]
                        comp = _comp_of([v for v in V if v not in B],
                                        IE, s)
                        CE = tuple(sorted((x, y) for x, y in IE
                                          if x in comp))
                        int_keys.add((frozenset(comp), CE, s))
    n_iso = len(iso_reps)
    n_comp_iso = len(set(_canon_interior(c, CE, s)
                         for (c, CE, s) in int_keys))
    ck(n_inst == 1102 and n_iso == 65 and n_inst // n_iso == 16
       and len(int_keys) == 64 and n_comp_iso == 5,
       f"S2 (F6 count discipline): the {n_inst} LABELED (graph, "
       f"source, boundary) triples of the reduced family collapse to "
       f"{n_iso} isomorphism classes (deflation factor "
       f"{n_inst // n_iso}); {len(int_keys)} interior-component cache "
       f"keys (raw vertex labels) collapse to {n_comp_iso} canonical "
       "interiors -- all counts computed in-module; every count "
       "sentence in this module says LABELED (isomorphs counted "
       "separately)")

    # ---- S3: THE CHARACTERIZATION, exhaustive on the reduced family ------
    cells = [
        ('A: SU(2) a=2 cap 2', _SU2, 2, LAB2, True, d_a2),
        ('B: SU(2) a=4 cap 2', _SU2, 4, LAB2, True, d_a4c2),
        ('E: SU(3) (1,1) cap 2', _SU3, (1, 1), LAB3, True, d_adj),
        ('D: SU(2) a=1 cap 2 (charge control)', _SU2, 1, LAB2, False,
         d_a1),
    ]
    res = {}
    for name, inst, a, labels, qz, dl in cells:
        def cond(V, E, B, s, _qz=qz, _dl=dl):
            return _condition_v1(V, E, B, s, _qz, _dl)
        r = _sweep_cell(CG, inst, a, labels, cond, _singlet)
        res[name] = r
        ck(r['tot'] == n_inst and r['mism'] == []
           and r['cache'] == len(int_keys),
           f"S3 [{name}]: condition <=> containment, EXACT over all "
           f"{r['tot']} LABELED instances (every labeled connected "
           f"simple graph on 2..4 vertices x every source x every "
           f"nonempty boundary, isomorphs counted separately -- "
           f"{n_iso} iso-classes; {r['scr']} contained-positive; "
           f"{r['cache']} interior cache keys, each enumerated "
           "exhaustively at cap on the banked rules) -- zero "
           "mismatches")
    scrA = res['A: SU(2) a=2 cap 2']['scr']
    ck(scrA == 84
       and res['D: SU(2) a=1 cap 2 (charge control)']['scr'] == 0,
       f"S3: pinned screen counts on the reduced family -- {scrA} "
       "contained-positive instances in the delta=1 cells; the charge "
       "control cell has an EMPTY screen set over the whole family "
       "(the consumed flux-exit singlet law read as containment "
       "impossibility) and the condition agrees identically")
    bitsA = res['A: SU(2) a=2 cap 2']['bits']
    ck(bitsA == res['E: SU(3) (1,1) cap 2']['bits'],
       f"S3: CELL COLLAPSE (delta=1): the per-instance screen sets of "
       f"cells A and E are IDENTICAL over all {n_inst} instances -- "
       "the fusion cell enters the condition ONLY through (q == 0, "
       "delta); geometry does the rest (computed set identity, the "
       "lane's A == C == E identity restricted to this family)")
    ck(res['B: SU(2) a=4 cap 2']['bits'] == bitsA,
       "S3: on THIS reduced 2..4-vertex family the delta=2 cell B "
       "COINCIDES with the delta=1 cell A (computed set identity): "
       "every 2..4-vertex instance that reaches a cycle puts the "
       "source IN the 2-core -- the separating pendant-to-cycle "
       "sources need 5 vertices; the lane record pins B PROPERLY "
       "contained in A on 2..5 (difference exactly those sources), "
       "and the separation is pinned at the n=5 spot witness next")

    # ---- S4: the delta-separator spot witness (n = 5, pinned) ------------
    E5 = ((0, 1), (1, 2), (1, 3), (2, 3), (3, 4))
    B5 = frozenset({4})
    se2 = _screen_exists(range(5), E5, B5, 0, 2, _SU2, LAB2, _singlet,
                         {})
    se4 = _screen_exists(range(5), E5, B5, 0, 4, _SU2, LAB2, _singlet,
                         {})
    co1 = _condition_v1(range(5), E5, B5, 0, True, 1)
    co2 = _condition_v1(range(5), E5, B5, 0, True, 2)
    ck(se2 is True and se4 is False and co1 is True and co2 is False,
       "S4: PINNED delta-separator spot (source 0 hangs off triangle "
       "1-2-3, boundary at 4): the SAME geometry is contained for a=2 "
       "(delta=1: cycle reachable) and NOT contained for a=4 at cap 2 "
       "(delta=2: source not in the 2-core) -- and the condition "
       "tracks containment on BOTH cells at the spot; the geometry "
       "clause is (a, cap)-cellwise and load-bearing, not decorative")

    # ---- S5: the derivation trail as negative controls --------------------
    def cond_v0(V, E, B, s):
        return _condition_v1(V, E, B, s, True, d_a1)
    r_v0 = _sweep_cell(CG, _SU2, 1, LAB2, cond_v0, _singlet)
    ck(len(r_v0['mism']) == 84 and r_v0['scr'] == 0,
       f"S5: candidate v0 (geometry + attachment, NO charge clause) is "
       f"REFUTED on the a=1 cell: {len(r_v0['mism'])} counterexample "
       "instances on the reduced family (v0 true, contained "
       "configuration exists NOWHERE for the charged source -- the "
       "consumed singlet law is GLOBAL); the charge clause is forced")
    exv0 = (4, ((0, 1), (0, 2), (1, 2), (2, 3)), 0, (3,), False, True)
    ck(exv0 in r_v0['mism'],
       "S5: v0's pinned counterexample -- triangle 0-1-2 with source "
       "a=1 at 0, pendant boundary 3: cycle through the source, "
       "locally closable (delta == 1), yet NO contained configuration "
       "(charge obstruction), located in the sweep's mismatch list")
    E5p = ((0, 1), (1, 2), (2, 3), (2, 4), (3, 4))
    B5p = frozenset({1})
    ck(_condition_v0p(range(5), E5p, B5p, 0, True, 1) is True
       and _screen_exists(range(5), E5p, B5p, 0, 2, _SU2, LAB2,
                          _singlet, {}) is False
       and _condition_v1(range(5), E5p, B5p, 0, True, 1) is False,
       "S5: candidate v0' (cycle ANYWHERE in the interior, "
       "reachability dropped) REFUTED at the pinned spot -- source 0 "
       "joined through boundary vertex 1 to triangle 2-3-4: the "
       "interior holds a cycle but s is isolated from it, no "
       "contained configuration, and v1's reachable-cycle clause "
       "correctly refuses; reachability is load-bearing")

    # ---- S6: predicate cross-validation -- the interior-component
    # reduction == the banked full-graph containment predicate -------------
    for cname, inst, a, labels in [('A', _SU2, 2, LAB2),
                                   ('E', _SU3, (1, 1), LAB3)]:
        nvv = 0
        tot = 0
        for n in (2, 3, 4):
            V = list(range(n))
            for E in CG[n]:
                for s in range(n):
                    others = [v for v in V if v != s]
                    for r in range(1, n):
                        for Bc in combinations(others, r):
                            B = frozenset(Bc)
                            tot += 1
                            if _contained_full(V, E, B, s, a, inst,
                                               labels, _enum) != \
                               _screen_exists(V, E, B, s, a, inst,
                                              labels, _singlet, {}):
                                nvv += 1
        ck(nvv == 0 and tot == n_inst,
           f"S6 [cell {cname}]: interior-component predicate == the "
           f"banked full-graph containment predicate (exhaustive _enum "
           f"+ all-unit boundary-incident edges, the TT zero-tail / "
           f"claw trivial-tail shape verbatim) on ALL {tot} reduced-"
           "family instances -- zero disagreements; the reduction is "
           "computed, not assumed")

    # ---- S7: the reduced threshold-law grid + the definitional split ------
    grid = {}
    for d in range(0, 4):
        for m in (1, 2):
            grid[(d, m)] = _supports(_cyc_at(d, m, 2), _SU2, LAB2,
                                     _enum)
    ck(all(v[0] == 5 for v in grid.values()),
       "S7: G(d, m) reduced grid d = 0..3, m = 1..2 at cap 2 (a=2): "
       "admissible count == 5 at every grid point (cell structure "
       "constant)")
    ck(all(grid[(d, m)][2] == d + 3
           for d in range(0, 4) for m in (1, 2)),
       "S7: THE THRESHOLD LAW on the reduced grid (F1 grid-scoped "
       "wording of record, adopted verbatim in the docstring): minimal "
       "contained support = d + 3 exactly, independent of m, at every "
       "recomputed grid point -- along any receding family whose "
       "parameters stay within the computed grid, depth-constant "
       "contained support exists iff d is constant there; the "
       "unbounded-d reading is the computed shape extrapolated, not a "
       "theorem")
    ck(all(grid[(d, m)][1] == min(d + m, d + 3)
           for d in range(0, 4) for m in (1, 2)),
       "S7: minimal admissible support == min(d+m, d+3) at every "
       "recomputed grid point (existence facts only; billing/argmin "
       "conventions are the parent lanes', not consumed)")
    for L in (2, 3):
        gf = _farcyc(L, 2)
        trip = _supports(gf, _SU2, LAB2, _enum)
        ck(trip == (5, L, L + 2)
           and trip == _supports(_cyc_at(L - 1, 1, 2), _SU2, LAB2,
                                 _enum),
           f"S7: farcyc({L}) == G({L - 1}, 1) (identical invariant "
           f"triple, the banked far-cycle family is the d = L-1, m = 1 "
           f"diagonal): banked pins reproduced (count 5, min support "
           f"{L}) AND the per-instance refinement computed -- a "
           f"CONTAINED configuration EXISTS at support {L + 2}, "
           "growing with L across the walked range")
        adm = _enum(gf, _SU2, LAB2)
        ck(min(_slots(c, _cuts(gf)) for c in adm) == L - 1,
           f"S7: farcyc({L}) minimal billed slots == {L - 1} (banked "
           "pin): the contained configuration still crosses the "
           "nested-family path cuts -- THE DEFINITIONAL-SPLIT WITNESS: "
           "farcyc is CONTAINED per instance (this condition's "
           "predicate) yet NOT SCREEN-SUPPORTING per family "
           "(depth-constant, cut-free -- the banked clause (ii)); the "
           "bank's family verdict is reproduced, not contradicted, and "
           "the two predicates may never be conflated in citation")

    # ---- S8: the F4 orientation witness + conj-closure of walked caps ----
    capNC = [(0, 0), (1, 0)]
    ck(_SU3['conj']((1, 0)) not in capNC,
       "S8 (F4 witness setup): the cap {unit, (1,0)} is NOT "
       "conj-closed (the antifundamental is outside it), computed")
    g_cyc3 = {'V': ['t0', 'w1', 'w2', 'b'],
              'E': [('t0', 'w1'), ('w1', 'w2'), ('w2', 't0'),
                    ('t0', 'b')],
              'boundary': frozenset(['b']), 'sources': {}}
    g_flip3 = {'V': ['t0', 'w1', 'w2', 'b'],
               'E': [('t0', 'w1'), ('w1', 'w2'), ('t0', 'w2'),
                     ('t0', 'b')],
               'boundary': frozenset(['b']), 'sources': {}}
    un3 = _SU3['unit']

    def has_nonunit_contained(g):
        adm = _enum(g, _SU3, capNC)
        bidx = [i for i, (x, y) in enumerate(g['E'])
                if x in g['boundary'] or y in g['boundary']]
        return any(all(c[i] == un3 for i in bidx)
                   and any(x != un3 for x in c) for c in adm)

    ck(has_nonunit_contained(g_cyc3)
       and not has_nonunit_contained(g_flip3),
       "S8 (F4 witness recomputed): at the non-conj-closed cap "
       "{unit, (1,0)} the CYCLICALLY oriented triangle carries a "
       "contained nonunit configuration (each vertex sees fundamental "
       "+ antifundamental slots) while the SAME underlying graph with "
       "one edge flipped carries none -- containment is orientation-"
       "dependent off conj-closed caps, so the CONJ-CLOSED rider is "
       "part of the banked condition statement, not a footnote")
    for inst, labs in ((_SU2, LAB2), (_SU2, LAB4), (_SU3, LAB3)):
        ck(all(inst['conj'](x) in labs for x in labs),
           f"S8: walked cap of size {len(labs)} is conj-closed "
           "(computed, per the F4 rider)")

    # ---- S9: mutation probes (the harness can fail; not theater) ---------
    flip = (4, ((0, 1), (0, 2), (1, 2), (2, 3)), 0, frozenset({3}))

    def condA(V, E, B, s):
        return _condition_v1(V, E, B, s, True, d_a2)
    r_mut1 = _sweep_cell(CG, _SU2, 2, LAB2, condA, _singlet,
                         flip_key=flip)
    ck(len(r_mut1['mism']) == 1
       and r_mut1['mism'][0][:4] == (4, flip[1], 0, (3,)),
       "S9/MP1: corrupting the screen bit on ONE instance (triangle + "
       "pendant boundary) makes the equivalence sweep fail at exactly "
       "that instance -- the check is instance-sharp; a single "
       "counterexample in any walked cell kills the characterization "
       "LOUDLY")

    def broken_sf(labs):
        nz = tuple(x for x in labs if x != 0)
        if nz == (2,):
            return 1
        return _singlet(_SU2, labs)
    r_mut2 = _sweep_cell(CG, _SU2, 2, LAB2, condA, _singlet,
                         singlet_fn=broken_sf)
    ck(len(r_mut2['mism']) > 0,
       f"S9/MP2: a corrupted fusion oracle (pretending a lone adjoint "
       f"closes a vertex -- deleting the leaf obstruction) fabricates "
       f"screens on trees and the sweep catches it at "
       f"{len(r_mut2['mism'])} instances -- the consumed singlet "
       "predicate is live in every decision")
    ck(all(grid[(d, m)][2] != d + 2
           for d in range(0, 4) for m in (1, 2)),
       "S9/MP3: the sabotaged threshold law 'd + 2' FAILS at every "
       "recomputed grid point -- the d + 3 law is exact, not padded")
    ck(_condition_v1(range(5), E5, B5, 0, True, 1) !=
       _screen_exists(range(5), E5, B5, 0, 4, _SU2, LAB2, _singlet,
                      {}),
       "S9/MP4: forcing delta = 1 on the a=4 cap-2 cell (the WRONG "
       "attachment number) disagrees with containment at the pinned "
       "n=5 separator spot -- the delta clause is load-bearing")

    # ---- S10: hygiene -----------------------------------------------------
    src_text = open(__file__.rstrip('c')).read()
    tree = ast.parse(src_text)
    floats = [n for n in ast.walk(tree) if isinstance(n, ast.Constant)
              and isinstance(n.value, (float, complex))]
    ck(floats == [],
       "S10: zero float/complex constants in this module's AST (exact "
       "integer arithmetic only)")
    stems = ('tension', 'spectral', 'spectrum', 'continuum',
             'magnitude', 'occupanc', 'quantum', 'energ')
    msgs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) \
                and isinstance(node.func, ast.Name) \
                and node.func.id == 'ck':
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) \
                        and isinstance(sub.value, str):
                    msgs.append(sub.value)
    hits = [(w, m[:40]) for m in msgs for w in stems if w in m.lower()]
    ck(len(msgs) >= 25 and hits == [],
       f"S10: vocabulary fence -- zero occurrences of the barred stems "
       f"over this battery's check messages (hits: {hits[:2]})")
    import io
    import re
    import tokenize
    badnum = []
    for tok in tokenize.generate_tokens(io.StringIO(src_text).readline):
        if tok.type == tokenize.NUMBER:
            t = tok.string.lower()
            if not t.startswith('0x') and ('.' in t or 'e' in t
                                           or 'j' in t):
                badnum.append(tok.string)
    ck(badnum == [],
       f"S10: no non-integer numeric literal in the module source "
       f"(offenders: {badnum[:3]})")
    badnarr = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) \
                and isinstance(node.func, ast.Name) \
                and node.func.id == 'ck' and len(node.args) == 2:
            for sub in ast.walk(node.args[1]):
                if isinstance(sub, ast.Constant) \
                        and isinstance(sub.value, str):
                    for dd in re.findall(r'\d{3,}', sub.value):
                        badnarr.append((dd, sub.value[:40]))
    ck(badnarr == [],
       f"S10: count honesty -- no >= 3-digit integer typed into any "
       f"static check message; family sizes and screen counts are "
       f"computed and interpolated (offenders: {badnarr[:2]})")

    passed = not fails
    return {
        'name': 'T_screen_containment_characterization',
        'epistemic': ('P | banked electric model + constructed-rule '
                      'consumption + stated caps/family + the '
                      'F2/F3/F4/F6 riders in the conditioning text'),
        'passed': passed,
        'tier': 4,
        'key_result': (
            'Per fusion cell (instance, source irrep a, cap; caps '
            'CONJ-CLOSED -- the F4 rider is part of the statement, '
            'orientation witness computed), on labeled connected '
            'simple graphs (isomorphs counted separately; 677 '
            'isomorphism classes) -- the lane family: every labeled '
            'connected simple graph on 2..5 vertices x every source x '
            'every nonempty boundary, 55,702 labeled instances, seven '
            'cells -- a contained admissible screen for a at s exists '
            'IFF (1) q(a) == 0 mod N, (2) delta_{<=kmax}(a, cap) is '
            'finite with kmax = 6 stated in the definition (F3; the '
            'a=14 witness: true attachment 7 reads None at kmax 6), '
            'and (3) at delta = 1 s reaches a cycle in G - B, at '
            'delta = 2 s lies in the 2-core of G - B -- clause (3) '
            'banked at delta in {1, 2} ONLY (F2); the general '
            'deg_H(s) >= delta form is a statement-shape, the '
            'audit\'s delta=3 exhibits corroboration only. Zero '
            'mismatches (lane record; audit re-verification 389,914 '
            'independent decisions, zero mismatches, disjoint fusion '
            'routes); re-verified exhaustively here on the reduced '
            'stated family (2..4 vertices, 1,102 labeled instances, '
            '65 isomorphism classes, four cells) with the v0/v0\' '
            'refutations, the delta-separator spot, and the F3/F4 '
            'witnesses pinned. Per-instance CONTAINED is NOT the '
            'banked family-level SCREEN-SUPPORTING predicate '
            '(depth-constant, cut-free): farcyc separates -- '
            'contained at support L+2 per instance, growing, still '
            'crossing the L-1 path cuts, NOT screen-supporting per '
            'family. Threshold law in the F1 grid-scoped wording: on '
            'the computed grid, minimal contained support = d + 3 '
            'exactly, independent of m; minimal admissible support = '
            'min(d+m, d+3); the unbounded-d reading is the computed '
            'shape extrapolated, not a theorem. Sufficiency is '
            'exhaustion-only (n >= 8 / exotic-delta the named '
            'standing flank); necessity and charge are '
            'argument-backed.'),
        'dependencies': ['L_center_flux_exit',
                         'T_frustration_center_partition'],
        'cross_refs': ['T_center_order_parameter_triality'],
        'artifacts': {
            'condition_statement': (
                'CONTAINED(G, s, B; a, cap) <=> q(a) == 0 mod N AND '
                'delta_{<=6}(a, cap) finite AND [delta=1: s reaches a '
                'cycle in G-B | delta=2: s in the 2-core of G-B]; '
                'caps conj-closed (F4, in the statement); clause (3) '
                'banked at delta in {1,2} only (F2); kmax = 6 stated '
                'in the definition (F3); labeled counts with '
                'iso-class deflation (F6)'),
            'premise_stack': (
                'banked electric model (L_center_flux_exit consumed '
                'live, grade line pinned; per-vertex-singlet a MODEL '
                'DEFINITION, Gauss reading a named identification) + '
                'constructed SU(2)/SU(3) fusion rules (all tensor '
                'arithmetic via the banked _singlet/_enum; no new '
                'fusion) + the screen-supporting vocabulary '
                '(T_frustration_center_partition consumed live) + '
                'cap/family scoping + A1 deliberately not consumed '
                '(pure model mathematics, house precedent)'),
            'reduced_battery': (
                'labeled connected simple graphs on 2..4 vertices '
                '(counts 1, 4, 38; 1,102 labeled instances; 65 '
                'isomorphism classes, deflation x16; 64 interior '
                'cache keys, 5 canonical interiors -- all computed '
                'in-module) x four cells: SU(2) a=2 cap 2, SU(2) a=4 '
                'cap 2, SU(3) (1,1) cap 2, SU(2) a=1 cap 2 charge '
                'control; 84 contained-positive per q==0 cell, 0 in '
                'the control; zero mismatches; full-graph banked-'
                'predicate cross-validation exhaustive on cells A and '
                'E; reduced G(d,m) grid d=0..3, m=1..2'),
            'lane_family': (
                'lane record, NOT rerun in-bank: 55,702 labeled '
                'instances (2..5 vertices; 677 isomorphism classes, '
                'deflation x82; 285 canonical interiors per cell; 16 '
                'true (source component, source) classes) x seven '
                'cells, zero mismatches; cell collapse A == C == E '
                'and B == F as sets, B properly contained in A; '
                'n = 6/7 seeded corroboration sweeps; multigraph '
                'spot riders (self-loop support 1, doubled edge '
                'support 2: multigraph-sense cycle reading)'),
            'threshold_law': (
                'F1 wording of record: "On the computed grid '
                '(d = 0..5, m = 1..4 at cap 2, a = 2; cap-3 and '
                'SU(3) adjoint spots as stated), minimal contained '
                'support = d + 3 exactly, independent of m; hence '
                'along any receding family whose parameters stay '
                'within the computed grid, depth-constant contained '
                'support exists iff d is constant there. The '
                'unbounded-d reading is the computed shape '
                'extrapolated, not a theorem." TT(L) = G(0, L), '
                'nearcyc(L) = G(1, L), farcyc(L) = G(L-1, 1); min '
                'admissible support = min(d+m, d+3); source-degree '
                'threshold at delta = 2 (lane record)'),
            'vocabulary_split': (
                'per-instance CONTAINED (support touches no boundary-'
                'incident edge) != family-level SCREEN-SUPPORTING '
                '(depth-constant support, crossing no family cut); '
                'farcyc separates: contained at support L+2 per '
                'instance, NOT screen-supporting per family; the '
                'audit ruled the split must survive distillation '
                'intact'),
            'witnesses': (
                'v0 refutation: triangle 0-1-2, source a=1 at 0, '
                'pendant boundary 3 (84 reduced-family '
                'counterexamples); v0\' refutation: source 0 through '
                'boundary vertex 1 to triangle 2-3-4 (reachability '
                'load-bearing); delta separator at n=5: source off '
                'triangle 1-2-3, boundary 4 -- contained for a=2, '
                'not for a=4 at cap 2; F3: SU(2) a=14 cap 2 true '
                'attachment 7, None at kmax 6; F4: cap {unit,(1,0)} '
                'cyclic triangle contained, one flip kills it'),
            'may_not_cite': (
                'nothing beyond stated caps/family (no "for all '
                'graphs" sentence exists); no new cells for free '
                '(per (a, cap); delta >= 3 never walked); '
                'sufficiency exhaustion-only -- n >= 8 / exotic-'
                'delta the named standing flank; no unbounded '
                'receding-family iff (grid-scoped F1 wording only); '
                'containment != screen-supporting (citing this as '
                '"screen-supporting characterized" is misciting); '
                'the general clause-(3) shape never cited as '
                'theorem; threshold law is existence facts, no '
                'billing/argmin/frustration composition; parent '
                'fences travel (no arbitrary-separating-set cut '
                'equality, H-hom named beyond grids, screens '
                'existence-only, no reading sentence, no dynamics/'
                'tension/gap/continuum, fixed-L dead, no SU(N>3))'),
            'kill_mode': (
                'a counterexample instance in any walked cell -- a '
                'single condition-vs-containment mismatch -- kills '
                'the characterization as stated (sweeps print it; '
                'MP1 shows instance-sharpness); upstream H-hom / '
                'construction-flag trip kills the consumed fusion; a '
                'contained configuration on a walked tree kills '
                'clause (3) necessity and banked clause (ii); a grid '
                'point with min contained support != d + 3 kills the '
                'threshold law'),
            'audit_record': (
                'hostile audit 2026-07-11, LAND-WITH-FIXES 0.92, no '
                'kill: 389,914 independent decisions zero mismatches '
                'on disjoint fusion routes (character / Schur-SSYT), '
                'own enumerator, no interior-component reduction; '
                'the C/D/F/G cross-validation gap closed empty; the '
                'mixed-only delta=3 sufficiency flank held (probe 2 '
                'A2); orientation failure computed exactly where '
                'flagged; mutation hardness 5/5; fixes F1-F6 carried '
                '(walker re-run of record 138 checks, exit 0)'),
            'disposition_417': (
                'the banked frustration_center_partition sentence '
                '"no graph-class characterization theorem exists '
                'anywhere in the bank" is RETAINED, never rewritten, '
                'with the pointer APPENDED at banking time: "(per-'
                'instance CONTAINMENT is characterized on a stated '
                'exhaustive labeled family by check_T_screen_'
                'containment_characterization, v24.3.418+; the '
                'family-level SCREEN-SUPPORTING predicate -- '
                'depth-constant, cut-free -- remains without a '
                'general characterization; farcyc separates the '
                'two.)" -- executed separately by the main seat; '
                'substantively accurate: re-scoped to the family '
                'level, the original line stays true'),
            'lane_records': (
                'The Turning (parked)/screen_geometry_2026-07-11/ '
                '(walk_screen_geometry.py 138 checks exit 0, fixes '
                'F1-F6 carried; WALK_NOTE.md; AUDIT_REPORT.md '
                'LAND-WITH-FIXES 0.92, audit probes 32/32 + 22/22); '
                'cross-ref: the composed-confinement lane records '
                '(the geometry proviso travels with '
                'T_center_order_parameter_triality\'s sufficiency '
                'leg). Version narrative: v24.3.421 (2026-07-11)'),
        },
        'fail_reasons': fails,
        'n_checks': n_checks[0],
    }


_CHECKS = {'T_screen_containment_characterization':
           check_T_screen_containment_characterization}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    import os
    import sys
    import time
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    t0 = time.time()
    r = check_T_screen_containment_characterization()
    print(r['name'], 'PASS' if r['passed'] else 'FAIL',
          f"({r['n_checks']} checks, {int(time.time() - t0)}s)")
    if not r['passed']:
        for f in r['fail_reasons']:
            print('  -', f)
    sys.exit(0 if r['passed'] else 1)
