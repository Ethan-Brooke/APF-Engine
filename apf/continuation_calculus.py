"""The continuation calculus on finite cost models: greedoid structure + selection.

BANKED v24.3.375 (2026-07-04; walks + witnesses of 2026-07-03). The Paper 10 Supplement B3/B4 package, landed
from the Mythos-review walk of record: "Reference - The Greedoid Structure of
Admissibility and the Selection Theorems - B3+B4 Walk (2026-07-03)" v0.3
(hostile-audited LAND-WITH-FIXES 0.85 at v0.2; the v0.3 principal ruling
below). Standalone machine witness: The Turning/b3b4_witness_2026-07-03.py,
13/13 PASS at seeds 20260703 and 42. Paper anchors: Paper 10 Technical
Supplement v0.1 sec:b34-greedoid (greedoid structure + weakened bound) and
sec:b5-erec (E_rec selection); main paper Paper 10 v1.15 sec:plec-recovery.

THE OBJECT. A finite admissible-family cost model at a context Gamma:
labels X, a feasible family F of subsets with held-available costs
kappa_Gamma(S), and a capacity C_Gamma, under three axioms:
  (M1) the empty family is feasible at cost 0        [unit, Cost(1) = 0]
  (M2) kappa(S) <= C_Gamma for all feasible S        [admissibility]
  (M3) every realized single-addition increment pays >= eps > 0; the
       marginal floor eps* is their minimum          [the MD floor]
This is the set-system presentation of Paper 10's calculus of finite
continuability; the floor eps* is the calculus's marginal-floor object.

THE PRINCIPAL RULING OF RECORD (2026-07-03, note v0.3 sec 2.5): the floor's
index set is COMPOSITE-INCLUSIVE ("go with the stronger one") -- Paper 10's
floor quantifies over every tested distinction-expression including
composites, so every feasible cover step (block or single) pays >= eps*.
Consequences in force, certified structurally here: the block floor BF is
DERIVABLE from the floor, and the weakened bound |S| <= N + J(S) is
UNCONDITIONAL -- the ruled citable form downstream. The atomic-reading
analysis (on which BF is a removable side hypothesis and the zero-cost
block breaks every bound) is retained as record in the note, not as the
citable form.

WHAT check_T_admissibility_greedoid_structure CERTIFIES (tier 4,
[P_structural]) -- the B3 package:
  1. Randomized accessible models (hereditary truncations of modular +
     pairwise costs): the floor exists, accessibility holds, every feasible
     family obeys the capacity-floor bound |S| <= N = floor(C_Gamma/eps*),
     and every feasible S is chain-buildable (Thm B3.3 shape:
     accessibility ==> chain-buildability ==> the bound).
  2. Greedoid exchange + empty set ==> accessibility (two constructed
     greedoids -- a branching greedoid and a uniform matroid -- plus a
     randomized family scan finding zero violations).
  3. Union-closure does NOT imply accessibility (explicit two-element
     model F = {empty, {1,2}}): the lattice-side closure property is
     independent of the chain-side one.
  4. M_coop (cooperative pair {A,B} jointly admissible, singletons not):
     accessibility FAILS, the bound's conclusion survives (max |S| <= N).
  5. M_break (anomaly-type 4-block at cost 2, floor priced by a witness
     singleton): the naive bound genuinely FAILS (|S*| = 4 > N = 2); the
     weakened bound |S| <= N + J(S) holds with J(S) = |S| - ell(S) the
     cooperative-passenger count (ell = longest feasible cover chain).
     Under the composite-inclusive ruling this weakened bound is
     UNCONDITIONAL -- the in-check block-floor leg witnesses BF on M_break.
  6. M_incomp (audit-donated): an accessible model whose block floor FAILS
     (a genuine multi-element cover paying 0.5 < eps* = 1). BF and
     accessibility are INCOMPARABLE -- at the MODEL level: M_incomp is a
     model of the bare axioms (M1)-(M3), NOT of the calculus post-ruling
     (the composite-inclusive floor excludes its cheap cover by pricing
     every tested composite at >= eps*). It is retained as the axiom-level
     independence witness, exactly as the note's sec 2.4 scopes it.
  7. The greedy failure (Thm B3.5 shape): in the hereditary + modular case
     the myopic greedy = sorted order minimizes the holding burden
     B(pi) = sum of prefix costs (brute force over all orders); in a
     general greedoid it does NOT -- the branching greedoid has greedy
     B = 15.0 vs feasible optimum 14.5. No unconditional greedoid-level
     greedy theorem for the holding burden exists.

WHAT check_T_selection_approximate_A2 CERTIFIES (tier 4, [P_structural])
-- the B4 package, the derived tightness/selection content of Paper 10
v1.15 sec:plec-recovery. Paper 10's A2 (argmin selection) and BW
(cost-spectrum non-degeneracy) are constitutive commitments;
SELECTION-AMONG-ALTERNATIVES REMAINS THE NAMED OPEN. This check certifies
the derived approximate form and its hypotheses' sharpness:
  1. Strictly-PD discretized E_rec kernel on the probability simplex:
     two projected-gradient-descent runs from very different starts
     converge to the SAME minimizer (uniqueness = the BW-side content that
     strict positive-definiteness buys).
  2. Degenerate (PSD, zero on mean-zero directions) kernel: distinct
     profiles with IDENTICAL energy -- ties exist, BW fails; uniqueness is
     not free.
  3. Kernel I + c*(1 (x) 1) with c > 0 (degenerate only along constants):
     uniqueness INHERITED from the strictly-PD mean-zero part -- the
     physically relevant degeneracy class keeps the selection.
  4. THE APPROXIMATE-A2 THEOREM with the honest independent sampler
     (audit MINOR-1 repair, carried): marginals and capacity drawn
     INDEPENDENTLY, saturation certified by REJECTION (floor(C/eps*) = k
     and the family fits), and the squeeze inequalities -- total slack
     < eps*, each slack < eps*, average slack < eps*/k, marginal squeeze
     -- tested on the survivors only, so the squeeze emerges from the
     theorem's hypotheses, not from the sampler.
  5. SHARPNESS: total slack = eps* - delta approaches eps* (delta-
     construction), with saturation certified in EXACT RATIONAL arithmetic
     (fractions.Fraction floor division) at the float-ambiguous quotient
     C/eps* = k + 1 - 1e-9 -- exactly the regime where a float fudge
     would be untrustworthy. So sigma/eps* -> 1 is attained in the limit
     and never at it: the approximate-A2 bound is tight.

STATUS. Both checks [P_structural] tier 4: structural theorems over the
finite cost-model class, machine-verified on constructed + randomized
models (rng seeded 20260703; deterministic). They do NOT derive A2 or BW
as theorems -- A2's selection-among-exact-ties and BW's non-degeneracy
remain named constitutive commitments of the calculus (Paper 10 v1.15;
the Mythos-review record: tightness/grading derived, selection/
non-degeneracy named opens).

FALSIFIERS: a finite cost model satisfying (M1)-(M3) + accessibility that
violates |S| <= floor(C/eps*); a greedoid (exchange + empty) that is not
accessible; a jointly admissible family violating |S| <= N + J(S) under
the composite-inclusive floor; a strictly-PD E_rec instance with two
distinct simplex minimizers; a saturated admissible instance with total
slack >= eps*.

Dependencies: A1, L_epsilon*.
Cross-refs: T_PLEC_derived_from_spine, L_cost.
"""

import itertools
import math
from fractions import Fraction

import numpy as np

from apf.apf_utils import check, _result

_SEED = 20260703


def _safe_floor_ratio(num, den, tol=1e-9):
    """Rational-safe floor(num/den) (the witness's audit repair, carried).

    Exact for int/Fraction inputs (Fraction floor division, no float
    roundoff). For floats: if num/den lands within tol of an integer
    without being exactly it, raise LOUDLY instead of silently rounding
    -- such a quotient is ambiguous under float arithmetic and the caller
    must supply exact rationals.
    """
    if isinstance(num, (int, Fraction)) and isinstance(den, (int, Fraction)):
        return int(Fraction(num) // Fraction(den))
    q = num / den
    nearest = round(q)
    if q != nearest and abs(q - nearest) < tol:
        raise ValueError(
            f"_safe_floor_ratio({num!r}, {den!r}): quotient {q!r} within "
            f"{tol} of integer {int(nearest)} -- ambiguous under floats; "
            f"supply fractions.Fraction")
    return math.floor(q)


class _FiniteCostModel:
    """Finite admissible-family cost model (Paper 10 Supplement, sec 1).

    X: hashable labels (tested distinctions at Gamma); cost: dict
    subset -> float over exactly the feasible family F; C_Gamma: capacity.
    Axioms (validate): (M1) empty feasible at 0; (M2) kappa <= C_Gamma;
    (M3) realized single-addition increments >= eps > 0 (floor = min;
    None if no realized increment exists).
    """

    def __init__(self, X, cost, C_Gamma):
        self.X = tuple(X)
        self.cost = {frozenset(k): float(v) for k, v in cost.items()}
        self.C = float(C_Gamma)
        self.F = set(self.cost.keys())

    def validate(self):
        check(frozenset() in self.F and abs(self.cost[frozenset()]) < 1e-15,
              "M1: empty family feasible at cost 0")
        check(all(v <= self.C + 1e-9 for v in self.cost.values()),
              "M2: admissibility kappa <= C_Gamma")
        eps = self.floor()
        check((eps is None) or (eps > 0), "M3: positive marginal floor")
        return True

    def increments(self):
        for S in self.F:
            for x in self.X:
                if x not in S and (S | {x}) in self.F:
                    yield (S, x, self.cost[S | {x}] - self.cost[S])

    def floor(self):
        incs = [d for (_, _, d) in self.increments()]
        return min(incs) if incs else None

    def N(self):
        eps = self.floor()
        return None if eps is None else _safe_floor_ratio(self.C, eps)

    def is_accessible(self):
        return all(any((S - {x}) in self.F for x in S)
                   for S in self.F if len(S) > 0)

    def chain_buildable(self, S):
        S = frozenset(S)
        if S not in self.F:
            return False
        cur = {S}
        for _ in range(len(S)):
            cur = {T - {x} for T in cur for x in T if (T - {x}) in self.F}
            if not cur:
                return False
        return True

    def satisfies_exchange(self):
        for S in self.F:
            for T in self.F:
                if len(S) > len(T):
                    if not any((T | {x}) in self.F for x in (S - T)):
                        return False
        return True

    def union_closed(self):
        return all((S | T) in self.F for S in self.F for T in self.F)

    def holding_burden(self, order):
        tot, S = 0.0, frozenset()
        for x in order:
            S = S | {x}
            if S not in self.F:
                return None
            tot += self.cost[S]
        return tot

    def greedy_order(self, target):
        S, order = frozenset(), []
        target = frozenset(target)
        while S != target:
            best = None
            for x in sorted(target - S, key=str):
                if (S | {x}) in self.F:
                    inc = self.cost[S | {x}] - self.cost[S]
                    if best is None or inc < best[0] - 1e-15:
                        best = (inc, x)
            if best is None:
                return None
            order.append(best[1])
            S = S | {best[1]}
        return order

    def min_holding_burden(self, target):
        best = None
        for perm in itertools.permutations(sorted(frozenset(target), key=str)):
            b = self.holding_burden(perm)
            if b is not None and (best is None or b < best):
                best = b
        return best

    def longest_chain_length(self, S):
        S = frozenset(S)
        subs = sorted((T for T in self.F if T <= S), key=len)
        L = {}
        for T in subs:
            if len(T) == 0:
                L[T] = 0
            else:
                preds = [L[U] for U in subs if U < T and U in L]
                L[T] = 1 + max(preds) if preds else None
        return L.get(S)

    def cover_pairs_below(self, S):
        S = frozenset(S)
        subs = [T for T in self.F if T <= S]
        out = []
        for T in subs:
            for Tp in subs:
                if T < Tp and not any(T < U < Tp for U in subs):
                    out.append((T, Tp))
        return out

    def block_floor_holds(self, S, eps):
        return all(self.cost[Tp] - self.cost[T] >= eps - 1e-12
                   for (T, Tp) in self.cover_pairs_below(S))


def _branching_greedoid_model():
    """Rooted tree r--a (w 2), a--x1 (w 1), a--x2 (w 1), r--b (w 1.5);
    feasible = subtree edge sets containing the root; cost modular."""
    w = {"ea": 2.0, "eb": 1.5, "c1": 1.0, "c2": 1.0}
    X = tuple(w)
    cost = {}
    for r in range(5):
        for S in itertools.combinations(X, r):
            S = frozenset(S)
            if ("c1" in S or "c2" in S) and "ea" not in S:
                continue
            cost[S] = sum(w[x] for x in S)
    return _FiniteCostModel(X, cost, C_Gamma=5.5), w


def _uniform_matroid_model(n=5, rank=3):
    cost = {frozenset(S): float(len(S))
            for r in range(rank + 1)
            for S in itertools.combinations(range(n), r)}
    return _FiniteCostModel(range(n), cost, C_Gamma=float(rank))


def check_T_admissibility_greedoid_structure():
    rng = np.random.default_rng(_SEED)

    # --- 1. randomized accessible models: floor, accessibility, the bound ---
    trials = 40
    for _ in range(trials):
        n = 6
        w = rng.uniform(1.0, 2.0, size=n)
        J = np.triu(rng.uniform(0.0, 0.5, size=(n, n)), 1)
        J = J + J.T
        C_G = rng.uniform(2.0, 6.0)
        cost = {}
        for r in range(n + 1):
            for S in itertools.combinations(range(n), r):
                idx = list(S)
                c = w[idx].sum() + 0.5 * J[np.ix_(idx, idx)].sum()
                if c <= C_G or r == 0:
                    cost[frozenset(S)] = c if r > 0 else 0.0
        m = _FiniteCostModel(range(n), cost, C_G)
        m.validate()
        check(m.is_accessible(),
              "hereditary truncation must be accessible")
        eps = m.floor()
        if eps is None:
            continue  # only the empty family feasible; bound vacuous
        N = m.N()
        for S in m.F:
            check(len(S) <= N,
                  "capacity-floor bound |S| <= floor(C/eps*) violated")
            check(m.chain_buildable(S),
                  "accessible model: every feasible S chain-buildable")

    # --- 2. exchange + empty set ==> accessibility ------------------------
    bg, w_bg = _branching_greedoid_model()
    um = _uniform_matroid_model()
    for m in (bg, um):
        check(m.satisfies_exchange() and m.is_accessible(),
              "constructed greedoid must satisfy exchange + accessibility")
    n = 5
    universe = [frozenset(S) for r in range(1, n + 1)
                for S in itertools.combinations(range(n), r)]
    satisfied = 0
    for _ in range(1500):
        k = int(rng.integers(1, 7))
        idx = rng.choice(len(universe), size=k, replace=False)
        F = {universe[i] for i in idx} | {frozenset()}
        cost = {S: float(len(S)) for S in F}
        m = _FiniteCostModel(range(n), cost, C_Gamma=float(n))
        if m.satisfies_exchange():
            satisfied += 1
            check(m.is_accessible(),
                  "exchange + empty set must imply accessibility")
    check(satisfied > 0, "the random-family scan must exercise exchange")

    # --- 3. union-closure alone does NOT imply accessibility --------------
    m_uc = _FiniteCostModel([1, 2],
                            {frozenset(): 0.0, frozenset({1, 2}): 1.0}, 1.0)
    m_uc.validate()
    check(m_uc.union_closed() and not m_uc.is_accessible()
          and not m_uc.satisfies_exchange(),
          "F = {empty, {1,2}}: union-closed, inaccessible, exchange fails")

    # --- 4. M_coop: accessibility fails, bound conclusion survives --------
    cost = {frozenset(): 0.0, frozenset({"CC"}): 1.0,
            frozenset({"A", "B"}): 2.0, frozenset({"A", "B", "CC"}): 3.0}
    m_coop = _FiniteCostModel(["A", "B", "CC"], cost, C_Gamma=3.0)
    m_coop.validate()
    eps_c, N_c = m_coop.floor(), m_coop.N()
    check(abs(eps_c - 1.0) < 1e-12 and N_c == 3,
          "M_coop: eps* = 1, N = 3")
    check(not m_coop.is_accessible()
          and not m_coop.chain_buildable({"A", "B", "CC"}),
          "M_coop: accessibility and chain-buildability fail")
    check(max(len(S) for S in m_coop.F) <= N_c,
          "M_coop: the bound's conclusion survives (max |S| <= N)")

    # --- 5. M_break: naive bound FAILS; weakened bound UNCONDITIONAL ------
    block = frozenset({"A1", "A2", "A3", "A4"})
    cost = {frozenset(): 0.0, frozenset({"W"}): 1.0, block: 2.0}
    m_br = _FiniteCostModel(["W", "A1", "A2", "A3", "A4"], cost, C_Gamma=2.0)
    m_br.validate()
    eps_b, N_b = m_br.floor(), m_br.N()
    check(abs(eps_b - 1.0) < 1e-12 and N_b == 2,
          "M_break: eps* = 1, N = floor(2/1) = 2")
    naive_fails = len(block) > N_b
    check(naive_fails, "M_break: the naive bound must genuinely fail (4 > 2)")
    check(not m_br.is_accessible(), "M_break: accessibility fails")
    ell = m_br.longest_chain_length(block)          # = 1 (empty -> block)
    J_pass = len(block) - ell                       # = 3 passengers
    check(ell == 1 and J_pass == 3,
          "M_break: ell(S*) = 1, J(S*) = 3")
    check(m_br.block_floor_holds(block, eps_b),
          "M_break: the block floor holds (composite cover pays >= eps*)")
    check(ell <= N_b and len(block) <= N_b + J_pass,
          "the weakened bound |S| <= N + J(S) must hold "
          "(RULED UNCONDITIONAL 2026-07-03, composite-inclusive floor)")

    # --- 6. M_incomp: accessible but BF fails (axiom-level witness) -------
    cost = {frozenset(): 0.0, frozenset({1}): 1.0, frozenset({2}): 10.0,
            frozenset({1, 3}): 2.0, frozenset({1, 2, 3}): 10.5}
    m_inc = _FiniteCostModel([1, 2, 3], cost, C_Gamma=10.5)
    m_inc.validate()
    eps_i = m_inc.floor()
    full = frozenset({1, 2, 3})
    covers = m_inc.cover_pairs_below(full)
    pair = (frozenset({2}), full)
    inc = m_inc.cost[full] - m_inc.cost[frozenset({2})]
    check(abs(eps_i - 1.0) < 1e-12 and m_inc.is_accessible()
          and all(m_inc.chain_buildable(S) for S in m_inc.F),
          "M_incomp: accessible, all chain-buildable, eps* = 1")
    check(pair in covers and abs(inc - 0.5) < 1e-12 and inc < eps_i,
          "M_incomp: genuine multi-element cover pays 0.5 < eps*")
    check(not m_inc.block_floor_holds(full, eps_i),
          "M_incomp: BF fails on an accessible model -- BF and "
          "accessibility incomparable AT THE AXIOM LEVEL (a model of "
          "(M1)-(M3), not of the calculus post-ruling)")

    # --- 7. greedy: optimal in hereditary+modular, NOT in general greedoid -
    for _ in range(12):
        nn = 5
        ww = rng.uniform(1.0, 3.0, size=nn)
        cost = {frozenset(S): float(ww[list(S)].sum())
                for r in range(nn + 1)
                for S in itertools.combinations(range(nn), r)}
        m = _FiniteCostModel(range(nn), cost, C_Gamma=float(ww.sum()))
        m.validate()
        target = frozenset(range(nn))
        Bg = m.holding_burden(m.greedy_order(target))
        Bmin = m.min_holding_burden(target)
        check(abs(Bg - Bmin) < 1e-9,
              "hereditary + modular: greedy = sorted order must be "
              "holding-burden-optimal")
    bg.validate()
    target = frozenset(w_bg)
    Bg = bg.holding_burden(bg.greedy_order(target))
    Bmin = bg.min_holding_burden(target)
    check(abs(Bg - 15.0) < 1e-9 and abs(Bmin - 14.5) < 1e-9 and Bmin < Bg,
          "branching greedoid: myopic greedy (B = 15.0) must be beaten by "
          "the feasible optimum (B = 14.5)")

    return _result(
        name='T_admissibility_greedoid_structure -- the greedoid structure '
             'of admissibility (Paper 10 Supplement B3)',
        tier=4,
        epistemic='P_structural',
        summary=(
            'The finite admissible-family cost-model class (M1)-(M3) '
            '[unit / admissibility / marginal floor eps*] carries a '
            'greedoid-shaped structure theory, machine-certified: '
            'accessibility ==> chain-buildability ==> the capacity-floor '
            'bound |S| <= floor(C_Gamma/eps*) (randomized hereditary '
            'models); greedoid exchange + empty set ==> accessibility '
            '(constructed branching greedoid + uniform matroid + a '
            'randomized-family scan, zero violations); union-closure does '
            'NOT imply accessibility (explicit model). Cooperative binding '
            'breaks the hypotheses without breaking the conclusion (M_coop) '
            'until it does: M_break (anomaly-type 4-block) genuinely '
            'defeats the naive bound (|S*| = 4 > N = 2), and the weakened '
            'bound |S| <= N + J(S) with J the cooperative-passenger count '
            'holds -- RULED UNCONDITIONAL (principal, 2026-07-03: the '
            'floor index set is composite-inclusive, so the block floor BF '
            'is derivable from the floor; the ruled citable form). '
            'M_incomp retains the axiom-level independence: BF and '
            'accessibility are INCOMPARABLE as properties of (M1)-(M3) '
            'models (accessible model with a 0.5 multi-element cover below '
            'eps* = 1) -- a model of the axioms, not of the calculus '
            'post-ruling. And the greedy theorem is exactly conditional: '
            'sorted greedy minimizes the holding burden in the hereditary '
            '+ modular case (brute force over all orders) but NOT in a '
            'general greedoid (branching example: greedy 15.0 vs optimal '
            '14.5). Paper anchor: Paper 10 Technical Supplement v0.1 '
            'sec:b34-greedoid.'
        ),
        key_result=(
            'accessibility ==> |S| <= floor(C/eps*); exchange ==> '
            'accessibility; union-closure does not; naive bound fails on '
            'M_break (4 > 2) and |S| <= N + J(S) holds UNCONDITIONALLY '
            '(composite-inclusive floor ruling 2026-07-03); BF/accessibility '
            'incomparable at axiom level; greedy optimal iff hereditary + '
            'modular (15.0 vs 14.5 counterexample)'
        ),
        dependencies=['A1', 'L_epsilon*'],
        cross_refs=['T_PLEC_derived_from_spine', 'L_cost'],
        artifacts={
            'M_break': {'block_size': 4, 'N': 2, 'ell': 1, 'J': 3,
                        'naive_bound_fails': True, 'weakened_bound_holds': True},
            'M_incomp': {'accessible': True, 'bf_fails': True,
                         'cheap_cover_increment': 0.5, 'eps_star': 1.0},
            'greedy_counterexample': {'greedy_burden': 15.0,
                                      'optimal_burden': 14.5},
            'floor_index_ruling': 'composite-inclusive (2026-07-03); '
                                  'weakened bound unconditional',
            'witness': 'The Turning/b3b4_witness_2026-07-03.py 13/13 PASS',
        },
    )


# ---------------------------------------------------------------------------
# B4: selection (E_rec uniqueness + the approximate-A2 theorem)
# ---------------------------------------------------------------------------

def _project_simplex(y):
    """Euclidean projection onto the probability simplex (Duchi et al. 2008)."""
    n = y.shape[0]
    u = np.sort(y)[::-1]
    css = np.cumsum(u)
    idx = np.arange(1, n + 1)
    rho = np.nonzero(u * idx > (css - 1.0))[0][-1]
    theta = (css[rho] - 1.0) / (rho + 1.0)
    return np.maximum(y - theta, 0.0)


def _minimize_Erec(eps_loc, I, x0, iters=200000, tol=1e-15):
    """PGD for E(phi) = eps.phi + phi^T I phi on the simplex."""
    L = 2.0 * np.linalg.norm(I, 2) + 1.0
    lr = 1.0 / L
    phi = _project_simplex(np.array(x0, dtype=float))
    for _ in range(iters):
        new = _project_simplex(phi - lr * (eps_loc + 2.0 * I @ phi))
        if np.linalg.norm(new - phi) < tol:
            phi = new
            break
        phi = new
    return phi


def check_T_selection_approximate_A2():
    rng = np.random.default_rng(_SEED)
    n = 40
    x = np.linspace(0.0, 1.0, n)

    # --- 1. strictly PD kernel: unique minimizer (two-start convergence) ---
    I_pd = np.exp(-np.abs(x[:, None] - x[None, :]) / 0.3) + 0.5 * np.eye(n)
    min_eig = float(np.linalg.eigvalsh(I_pd).min())
    check(min_eig > 1e-8, "the OU + self-crowding kernel must be strictly PD")
    eps_loc = 1.0 + 0.8 * np.sin(3.0 * np.pi * x) + 0.3 * rng.standard_normal(n)
    s1 = rng.dirichlet(np.ones(n))
    s2 = rng.dirichlet(np.ones(n) * 0.1)
    p1 = _minimize_Erec(eps_loc, I_pd, s1)
    p2 = _minimize_Erec(eps_loc, I_pd, s2)
    d_pd = float(np.linalg.norm(p1 - p2))
    E1 = float(eps_loc @ p1 + p1 @ I_pd @ p1)
    E2 = float(eps_loc @ p2 + p2 @ I_pd @ p2)
    check(d_pd < 1e-6 and abs(E1 - E2) < 1e-10,
          "strict PD: two PGD starts must reach the same equilibrium profile")

    # --- 2. degenerate kernel: ties exist (BW fails) -----------------------
    I_deg = np.ones((n, n))
    eps_one = np.ones(n)
    pa = np.zeros(n)
    pa[0] = 1.0
    pb = np.ones(n) / n
    Ea = float(eps_one @ pa + pa @ I_deg @ pa)
    Eb = float(eps_one @ pb + pb @ I_deg @ pb)
    psi = pa - pb
    q = float(psi @ I_deg @ psi)
    check(abs(Ea - Eb) < 1e-12 and abs(q) < 1e-12
          and float(np.linalg.norm(pa - pb)) > 0.5,
          "degenerate kernel: distinct profiles with identical energy "
          "(ties; the BW-side content fails)")

    # --- 3. I + c*(1 (x) 1), c > 0: uniqueness inherited -------------------
    c = 5.0
    I_shift = I_pd + c * np.ones((n, n))
    p1c = _minimize_Erec(eps_loc, I_shift, s1)
    p2c = _minimize_Erec(eps_loc, I_shift, s2)
    d_c = float(np.linalg.norm(p1c - p2c))
    E1c = float(eps_loc @ p1c + p1c @ I_shift @ p1c)
    E2c = float(eps_loc @ p2c + p2c @ I_shift @ p2c)
    check(d_c < 1e-6 and abs(E1c - E2c) < 1e-10,
          "constant-shift kernel (degenerate only along constants): "
          "uniqueness inherited from the mean-zero part")

    # --- 4. approximate-A2 with the honest independent sampler -------------
    trials, min_accepted = 1500, 60
    accepted, worst = 0, 0.0
    for _ in range(trials):
        eps = float(rng.uniform(0.1, 10.0))
        k = int(rng.integers(1, 60))
        e = rng.exponential(scale=eps / (2.0 * k), size=k)
        m = eps + e                                # independent marginals
        C_G = float(rng.uniform(k * eps, (k + 2) * eps))   # independent capacity
        try:
            saturated = (_safe_floor_ratio(C_G, eps) == k)
        except ValueError:
            continue     # float-ambiguous quotient: cannot certify saturation
        if not saturated or float(m.sum()) > C_G:
            continue     # rejection: only certified-saturated instances count
        accepted += 1
        budget = (C_G - m.sum()) * float(rng.uniform(0.0, 1.0))
        s = rng.dirichlet(np.ones(k)) * budget
        C = m + s
        total_slack = float((C - m).sum())
        worst = max(worst, total_slack / eps)
        check(total_slack < eps, "approximate-A2: aggregate slack < eps*")
        check(bool((C - m < eps).all()), "approximate-A2: each slack < eps*")
        check(total_slack / k < eps / k + 1e-15,
              "approximate-A2: average slack < eps*/k")
        check(float((m - eps).sum()) < eps, "approximate-A2: marginal squeeze")
    check(accepted >= min_accepted,
          "the rejection sampler must accept enough saturated survivors")

    # --- 5. sharpness, saturation certified in exact rationals -------------
    k = 5
    eps_frac = Fraction(1)
    delta_frac = Fraction(1, 10**9)
    C_G_frac = k * eps_frac + eps_frac - delta_frac
    check(_safe_floor_ratio(C_G_frac, eps_frac) == k,
          "sharpness: saturation certified exactly at the float-ambiguous "
          "quotient (Fraction floor division)")
    eps_f, C_Gf = float(eps_frac), float(C_G_frac)
    m_arr = np.ones(k) * eps_f
    C_arr = m_arr.copy()
    C_arr[0] += eps_f - float(delta_frac)          # all slack on one allocation
    total = float((C_arr - m_arr).sum())
    check(float(C_arr.sum()) <= C_Gf + 1e-15
          and eps_f - 1e-8 < total < eps_f,
          "sharpness: total slack = eps* - delta approaches eps*, never "
          "attains it")

    return _result(
        name='T_selection_approximate_A2 -- E_rec uniqueness + the '
             'approximate-A2 theorem (Paper 10 Supplement B4)',
        tier=4,
        epistemic='P_structural',
        summary=(
            'The derived tightness/selection content of Paper 10 v1.15 '
            'sec:plec-recovery, machine-certified on the discretized E_rec '
            'functional over the probability simplex and on randomized '
            'saturated allocation instances. (1) A strictly-PD interaction '
            'kernel has a UNIQUE E_rec minimizer: two projected-gradient '
            'runs from very different starts converge to the same profile. '
            '(2) A degenerate (PSD-but-not-strictly-PD-on-mean-zero) '
            'kernel admits TIES -- distinct profiles with identical energy '
            '-- so the BW-side non-degeneracy is not free. (3) The '
            'physically relevant degeneracy class I + c*(1 (x) 1), c > 0, '
            'INHERITS uniqueness from its strictly-PD mean-zero part. '
            '(4) THE APPROXIMATE-A2 THEOREM with the honest independent '
            'sampler (audit repair carried): marginals and capacity drawn '
            'independently, saturation certified by rejection, and the '
            'squeeze -- total slack < eps*, each < eps*, average < eps*/k, '
            'marginal squeeze -- holds on every survivor, so near-argmin '
            'selection is forced by saturation, not by construction. '
            '(5) SHARPNESS: total slack approaches eps* (delta-'
            'construction), with saturation certified in exact rational '
            'arithmetic at the float-ambiguous quotient. STATUS FENCE: '
            'this is the derived APPROXIMATE form; A2 selection-among-'
            'exact-ties and BW non-degeneracy remain named constitutive '
            'commitments (the Mythos-review record: tightness/grading '
            'derived, selection/non-degeneracy named opens). Paper '
            'anchors: Supplement sec:b34-greedoid + sec:b5-erec.'
        ),
        key_result=(
            'strict-PD E_rec: unique minimizer (two-start PGD agreement '
            '< 1e-6); degenerate kernel: exact ties (BW fails); '
            'I + c(1(x)1): uniqueness inherited; approximate-A2 slack '
            'squeeze < eps* on all independently-sampled saturated '
            'survivors; sharpness sigma/eps* -> 1 with exact-rational '
            'saturation certification. Selection-among-alternatives stays '
            'the named open.'
        ),
        dependencies=['A1', 'L_epsilon*'],
        cross_refs=['T_PLEC_derived_from_spine',
                    'T_admissibility_greedoid_structure'],
        artifacts={
            'pd_two_start_distance': d_pd,
            'shift_two_start_distance': d_c,
            'approx_a2': {'trials': trials, 'accepted': accepted,
                          'worst_total_slack_over_eps': worst},
            'sharpness_total_slack': total,
            'status_fence': 'approximate form certified; A2 tie-selection '
                            '+ BW non-degeneracy remain named opens',
            'witness': 'The Turning/b3b4_witness_2026-07-03.py 13/13 PASS',
        },
    )


# ---------------------------------------------------------------------------
# Paper 9 / Paper 10 closure repair: finite operational basis.
#
# This block deliberately separates:
#   (a) the exact finite atom-cover MODEL witness;
#   (b) the scope guard showing why that model does not prove the unrestricted
#       physical theorem without finite joint-extension/amalgamation; and
#   (c) the compatible JOINT realization corollary on the model.
#
# It uses exact Fraction arithmetic at every cardinality/capacity boundary.
# ---------------------------------------------------------------------------

_FINITE_BASIS_MODEL_HYPOTHESES = (
    "finite_content_atoms",
    "operational_classes_are_atom_subsets",
    "operational_closure_is_union",
    "joint_realization_is_union_carrier",
    "exact_no_excess_atom_cost",
    "full_content_is_admissible",
    "closed_world_union_cover",
)

_FINITE_BASIS_GENERAL_OPEN_OBLIGATIONS = (
    "finite_joint_extension_or_amalgamation",
    "downward_closed_joint_realizability",
    "minimum_joint_realization_attainment",
    "compatible_joint_realization",
    "operational_basis_to_precision_channel_bridge",
)


def _u(sets):
    sets = list(sets)
    return frozenset().union(*sets) if sets else frozenset()


def _rich_family(rng, m, ntry):
    """A large operational-class family over ``m`` content atoms.

    Singletons are not forced.  Thus closed-world completeness
    ``union(F) == Omega`` is a genuine, fallible hypothesis rather than a
    sampler invariant.
    """
    Omega = frozenset(range(m))
    F = set()
    for _ in range(int(ntry)):
        k = int(rng.integers(1, m + 1))
        F.add(frozenset(int(x) for x in rng.choice(m, size=k, replace=False)))
    return Omega, sorted(F, key=lambda s: (len(s), tuple(sorted(s))))


def _greedy_basis(Omega, F):
    """Extract classes that add new atom content until complete or stuck."""
    covered = frozenset()
    B = []
    while covered != Omega:
        cand = next((c for c in F if not (c <= covered)), None)
        if cand is None:
            return B, covered, True
        covered |= cand
        B.append(cand)
    return B, covered, False


def _minimize(B, Omega):
    """Delete union-redundant members while preserving complete coverage."""
    M = list(B)
    changed = True
    while changed:
        changed = False
        for i in range(len(M)):
            rest = _u(M[j] for j in range(len(M)) if j != i)
            if M[i] <= rest:
                del M[i]
                changed = True
                break
    check(_u(M) == Omega, "minimalization must preserve full atom coverage")
    return M


def _positive_fraction(rng, *, num_hi=80, den_hi=24):
    """Deterministic positive rational sampler for exact theorem boundaries."""
    return Fraction(
        int(rng.integers(1, num_hi + 1)),
        int(rng.integers(1, den_hi + 1)),
    )


def _joint_realization_id(basis):
    rows = []
    for cls in sorted(basis, key=lambda s: (len(s), tuple(sorted(s)))):
        rows.append("{" + ",".join(str(x) for x in sorted(cls)) + "}")
    return "atom-cover-joint:[" + ";".join(rows) + "]"


def _build_atom_cover_joint_realization(basis, eps):
    """Construct one compatible no-excess joint carrier for the whole basis.

    The carrier is the union of the atoms required by the basis.  Every basis
    class is recovered by a deterministic projection to its subset.  Under the
    exact atom-cost law, every joint carrier realizing the basis must cover at
    least this union, so the construction is minimum and no-excess.
    """
    basis = tuple(basis)
    covered = _u(basis)
    joint_id = _joint_realization_id(basis)
    projections = tuple(
        {
            "joint_id": joint_id,
            "class": cls,
            "visible_atoms": cls,
        }
        for cls in basis
    )
    return {
        "joint_id": joint_id,
        "basis": basis,
        "covered": covered,
        "total_cost": Fraction(len(covered)) * eps,
        "minimum_lower_bound": Fraction(len(covered)) * eps,
        "projections": projections,
    }


def _projection_family_is_compatible(joint):
    projections = tuple(joint.get("projections", ()))
    if not projections:
        return not joint.get("basis")
    ids = {p.get("joint_id") for p in projections}
    if ids != {joint.get("joint_id")}:
        return False
    covered = joint.get("covered", frozenset())
    return all(
        p.get("visible_atoms") == p.get("class")
        and p.get("class", frozenset()) <= covered
        for p in projections
    )


def check_T_finite_operational_basis_scope_contract():
    """Scope guard and exact-arithmetic contract for the Paper 10/Paper 9 node.

    This check makes two reviewer-critical facts executable:

    1. The banked positive theorem is a theorem of a finite atom-cover model,
       whose hidden structure is explicitly named in
       ``_FINITE_BASIS_MODEL_HYPOTHESES``.
    2. The unrestricted manuscript theorem needs a separate finite
       joint-extension/amalgamation premise.  A closed ledger with individually
       admitted classes but no jointly realizable pair is a finite countermodel
       to the unqualified induction.
    """
    # Model-contract sanity: subset classes, union closure, exact atom cost.
    Omega = frozenset({0, 1, 2})
    F = (frozenset({0, 1}), frozenset({2}), frozenset({1, 2}))
    eps = Fraction(3, 5)
    covered = _u(F)
    check(covered == Omega, "closed-world atom-cover family must cover Omega")
    check(Fraction(len(covered)) * eps == Fraction(9, 5),
          "exact no-excess atom cost is |covered|*eps")

    # Exact cardinality boundary: no +1e-9 enlargement of the admissible set.
    boundary_capacity = Fraction(1_999_999_999, 2_000_000_000)
    boundary_eps = Fraction(1)
    check(_safe_floor_ratio(boundary_capacity, boundary_eps) == 0,
          "exact floor below one commitment is zero")
    check(boundary_eps > boundary_capacity,
          "one full commitment is exactly inadmissible at the boundary")

    # Finite no-amalgamation countermodel to the unrestricted printed theorem.
    A = frozenset({"a", "b", "c"})
    jointly_realizable = {
        frozenset(), frozenset({"a"}), frozenset({"b"}), frozenset({"c"})
    }
    closure = lambda S: frozenset(S)  # trivial deterministic postprocessing
    closed_world_individual = all(frozenset({a}) in jointly_realizable for a in A)
    complete_joint_families = [
        S for S in jointly_realizable if closure(S) == A
    ]
    extension_candidates_from_a = [
        a for a in A - closure(frozenset({"a"}))
        if frozenset({"a", a}) in jointly_realizable
    ]
    check(closed_world_individual,
          "every admitted class is present in the finite closed ledger")
    check(not complete_joint_families,
          "without amalgamation no complete jointly realizable basis exists")
    check(not extension_candidates_from_a,
          "the greedy induction gets stuck unless finite joint extension is named")

    return _result(
        name=(
            "T_finite_operational_basis_scope_contract -- finite atom-cover "
            "model contract, exact boundary, and no-amalgamation scope guard"
        ),
        tier=4,
        epistemic="P_structural_instrument",
        summary=(
            "The finite-basis bank node is scoped to a finite atom-cover model: "
            "finite content atoms, subset-coded operational classes, union "
            "closure/joint carrier, and exact no-excess atom cost. Exact "
            "Fraction arithmetic rejects the former +1e-9 boundary enlargement. "
            "A finite closed-ledger countermodel with only singleton joint "
            "families proves that the unrestricted physical theorem additionally "
            "requires finite joint-extension/amalgamation and minimum compatible "
            "joint realization. This is a scope instrument, not a new physical "
            "derivation."
        ),
        key_result=(
            "Restricted model hypotheses named; C=1999999999/2000000000, "
            "eps*=1 gives exact N=0; finite no-amalgamation ledger has every "
            "class individually admitted but no complete jointly realizable basis."
        ),
        dependencies=[],
        cross_refs=[
            "T_admissibility_greedoid_structure",
            "T_selection_approximate_A2",
            "FD1_structural_completeness",
        ],
        artifacts={
            "claim_kind": "adopted_with_falsifier",
            "model_class": "finite_atom_cover",
            "hypotheses": list(_FINITE_BASIS_MODEL_HYPOTHESES),
            "general_open_obligations": list(
                _FINITE_BASIS_GENERAL_OPEN_OBLIGATIONS
            ),
            "boundary_control": {
                "capacity": "1999999999/2000000000",
                "eps_star": "1",
                "exact_floor": 0,
                "one_commitment_admissible": False,
            },
            "no_amalgamation_control": {
                "n_classes": len(A),
                "jointly_realizable": "empty and singletons only",
                "complete_joint_basis_exists": False,
            },
            "non_claims": [
                "not_a_general_joint_extension_theorem",
                "not_precision_channel_generation",
                "not_finite_smooth_generation",
            ],
        },
    )


def check_T_finite_operational_basis():
    """Exact finite atom-cover model witness for the finite basis mechanism."""
    rng = np.random.default_rng(_SEED)
    adm = inadm = stuck = tight = incr_used = complete = 0

    for _ in range(600):
        eps = _positive_fraction(rng, num_hi=50, den_hi=20)
        C = _positive_fraction(rng, num_hi=240, den_hi=20)
        Nmax = _safe_floor_ratio(C, eps)
        if Nmax < 1:
            continue

        # Content dimension is independent of C.  The theorem boundary decides
        # whether the full admitted atom content can be jointly realized.
        m = int(rng.integers(1, 11))
        Omega, F = _rich_family(
            rng, m, int(rng.integers(1, 2 ** min(m, 6) + 1))
        )
        content_cost = Fraction(m) * eps
        admissible = content_cost <= C
        cwc = _u(F) == Omega

        # The exact capacity-floor bound must bite.
        if not admissible:
            inadm += 1
            check(m > Nmax,
                  "inadmissible atom content exceeds floor(C/eps*) exactly")
            check(content_cost > C,
                  "inadmissible atom content has exact no-excess cost above C")
            continue

        adm += 1
        if m == Nmax:
            tight += 1

        B, covered, is_stuck = _greedy_basis(Omega, F)

        # Closed-world union-cover is genuinely fallible and load-bearing.
        if not cwc:
            stuck += 1
            check(is_stuck and covered != Omega,
                  "non-covering family must stop without a false complete basis")
            check(any(a not in _u(F) for a in Omega),
                  "a real atom remains absent from the closed ledger")
            continue

        check(not is_stuck, "closed-world union cover makes greedy extraction complete")

        # Positive exact marginal increment on every greedy step.
        sub = frozenset()
        for cls in B:
            if not cls <= sub:
                inc = Fraction(len(sub | cls) - len(sub)) * eps
                check(inc >= eps,
                      "every class outside union closure adds at least one exact atom floor")
                incr_used += 1
            sub |= cls

        check(covered == Omega and all(cls <= covered for cls in F),
              "cl(B_U)=A_U in the finite atom-cover model")
        check(len(B) <= Nmax,
              "basis cardinality is bounded by exact floor(C_U/eps*)")

        M = _minimize(B, Omega)
        for i in range(len(M)):
            rest = _u(M[j] for j in range(len(M)) if j != i)
            check(not (M[i] <= rest),
                  "inclusion-minimal basis has no union-redundant member")
        check(len(M) <= Nmax, "minimal basis remains under the exact capacity bound")
        complete += 1

    check(adm > 30 and inadm > 20 and stuck > 10 and tight > 0
          and incr_used > 50 and complete > 30,
          "all finite-basis model arms must be exercised")

    # No-excess is load-bearing: pre-reserved content can absorb a new atom at
    # zero marginal cost and invalidates the increment premise.
    eps = Fraction(1)
    reserved = frozenset({5})
    cost_excess = lambda U: Fraction(len(U | reserved))
    Su = frozenset({0})
    check(cost_excess(Su | {5}) - cost_excess(Su) == 0,
          "reserved excess kills the distinction increment")

    # The positive floor is load-bearing both for increment and cardinality.
    cost_free = lambda U: sum(Fraction(1) for a in U if a != 3)
    check(cost_free(frozenset({0, 1, 3}))
          - cost_free(frozenset({0, 1})) == 0,
          "a floor-free atom adds zero marginal cost")
    check(_safe_floor_ratio(Fraction(6), Fraction(1, 10**9)) > 10**8,
          "eps* tending to zero makes the cardinality bound vacuous")

    # Causal scope fence: basis counts operational classes/content, not the
    # multiplicity of concrete terminal realizations.
    Omega_s = frozenset({0, 1, 2})
    F_s = [
        frozenset({0, 1}), frozenset({2}),
        frozenset({0}), frozenset({1, 2}),
    ]

    def _N_under_mult(F, mult):
        total = sum(mult.get(cls, 1) for cls in F)
        classes = sorted(set(F), key=lambda s: (len(s), tuple(sorted(s))))
        B, _, _ = _greedy_basis(Omega_s, classes)
        return len(_minimize(B, Omega_s)), total

    N1, tot1 = _N_under_mult(F_s, {cls: 1 for cls in F_s})
    N2, tot2 = _N_under_mult(
        F_s,
        {
            frozenset({0, 1}): 10**6,
            frozenset({2}): 10**9,
            frozenset({0}): 7,
            frozenset({1, 2}): 10**4,
        },
    )
    check(N1 == N2 and tot2 > 10**8 and tot1 < 10,
          "realization multiplicity cannot change the operational basis size")

    return _result(
        name=(
            "T_finite_operational_basis -- exact finite atom-cover model "
            "witness for the Finite Operational Basis mechanism"
        ),
        tier=4,
        epistemic="P_structural",
        summary=(
            "Restricted executable theorem: on a finite atom-cover model, "
            "where admitted content is a finite atom set, operational classes "
            "are atom subsets, joint realization/closure is union, and exact "
            "no-excess cost is |covered atoms|*eps*, full-content admissibility "
            "plus closed-world union cover yields a finite complete "
            "inclusion-minimal operational-class basis with size at most "
            "floor(C_U/eps*). All theorem boundaries use Fraction arithmetic. "
            "Fail-controls exercise non-covering ledgers, capacity overspend, "
            "reserved excess, a floor-free atom, and realization-multiplicity "
            "invariance. The separate scope-contract check proves that this is "
            "not an unrestricted physical joint-extension theorem."
        ),
        key_result=(
            "Exact finite atom-cover model: complete minimal basis exists and "
            "|B_U|<=floor(C_U/eps*); every control arm fires; no float tolerance "
            "enlarges the admissible set. General physical export remains gated "
            "by finite joint extension and compatible joint realization."
        ),
        dependencies=[
            "A1",
            "L_epsilon*",
            "T_admissibility_greedoid_structure",
            "T_finite_operational_basis_scope_contract",
        ],
        cross_refs=[
            "T_selection_approximate_A2",
            "T_sep",
            "FD1_structural_completeness",
        ],
        artifacts={
            "claim_kind": "adopted_with_falsifier",
            "model_class": "finite_atom_cover",
            "hypotheses": list(_FINITE_BASIS_MODEL_HYPOTHESES),
            "general_open_obligations": list(
                _FINITE_BASIS_GENERAL_OPEN_OBLIGATIONS
            ),
            "arms_exercised": {
                "admissible": adm,
                "inadmissible_bound_bites": inadm,
                "closed_world_stuck": stuck,
                "capacity_tight": tight,
                "increment_steps": incr_used,
                "complete_models": complete,
            },
            "arithmetic": "fractions.Fraction + _safe_floor_ratio; exact boundaries",
            "paper_anchor": "Paper 10 v1.21 sec:finite-operational-basis",
            "non_claims": [
                "not_a_derivation_of_finite_joint_extension",
                "not_a_general_physical_closure_theorem",
                "not_precision_channel_generation",
                "not_finite_smooth_generation",
            ],
        },
    )


def check_T_finite_minimal_joint_realization_atom_cover():
    """Concrete compatible joint-realization corollary on the atom-cover model."""
    rng = np.random.default_rng(_SEED + 1)
    exercised = 0

    for _ in range(400):
        eps = _positive_fraction(rng, num_hi=30, den_hi=15)
        C = _positive_fraction(rng, num_hi=180, den_hi=15)
        Nmax = _safe_floor_ratio(C, eps)
        if Nmax < 1:
            continue
        m = int(rng.integers(1, min(9, Nmax) + 1))
        Omega, F = _rich_family(
            rng, m, int(rng.integers(max(2, m), 2 ** min(m, 6) + 1))
        )
        if _u(F) != Omega:
            continue

        B, covered, stuck = _greedy_basis(Omega, F)
        check(not stuck and covered == Omega,
              "closed atom-cover family must admit a complete greedy basis")
        M = _minimize(B, Omega)
        joint = _build_atom_cover_joint_realization(M, eps)

        check(joint["covered"] == Omega,
              "one joint carrier realizes the whole minimal basis")
        check(joint["total_cost"] == joint["minimum_lower_bound"],
              "joint carrier attains the exact atom-cover lower bound")
        check(joint["total_cost"] <= C,
              "joint minimum remains physically admissible")
        check(_projection_family_is_compatible(joint),
              "all basis projections descend from one joint realization id")
        check(all(cls <= joint["covered"] for cls in F),
              "the joint carrier is complete under deterministic subset projection")
        check(len(M) <= Nmax,
              "compatible joint realization has a finite bounded basis interface")
        exercised += 1

    check(exercised > 40,
          "compatible joint-realization theorem must exercise many complete models")

    # Negative control: independently minimum representatives need not be a
    # compatible family merely because each is minimum in isolation.
    incompatible = {
        "joint_id": "none",
        "covered": frozenset({0, 1}),
        "basis": (frozenset({0}), frozenset({1})),
        "projections": (
            {
                "joint_id": "independent-r0",
                "class": frozenset({0}),
                "visible_atoms": frozenset({0}),
            },
            {
                "joint_id": "independent-r1",
                "class": frozenset({1}),
                "visible_atoms": frozenset({1}),
            },
        ),
    }
    check(not _projection_family_is_compatible(incompatible),
          "independently selected minima are rejected without a shared joint carrier")

    return _result(
        name=(
            "T_finite_minimal_joint_realization_atom_cover -- one compatible "
            "minimum joint carrier and deterministic basis projections"
        ),
        tier=4,
        epistemic="P_structural",
        summary=(
            "On every exercised closed finite atom-cover model, a complete "
            "inclusion-minimal basis is represented by one concrete joint "
            "carrier containing exactly the union of its atoms. Exact atom "
            "cost makes that carrier minimum and no-excess; deterministic "
            "subset projections recover every basis class and every class in "
            "the closed family. A negative control rejects independently "
            "minimum representatives with different joint-realization ids. "
            "This repairs the former string-tag corollary on the restricted "
            "model; the general physical compatible-minimizer theorem remains "
            "a named obligation."
        ),
        key_result=(
            "One minimum no-excess joint carrier realizes the complete basis; "
            "all projections share one joint id; isolated minima with distinct "
            "ids fail compatibility."
        ),
        dependencies=[
            "T_finite_operational_basis",
            "T_finite_operational_basis_scope_contract",
        ],
        cross_refs=["T_selection_approximate_A2"],
        artifacts={
            "claim_kind": "derived_theorem",
            "model_class": "finite_atom_cover",
            "models_exercised": exercised,
            "joint_realization_fields": [
                "joint_id",
                "basis",
                "covered",
                "total_cost",
                "minimum_lower_bound",
                "projections",
            ],
            "negative_control": "independent minima with distinct joint ids rejected",
            "general_open_obligation": "compatible_joint_realization",
            "paper_anchor": "Paper 10 v1.21 cor:finite-minimal-joint-realization",
        },
    )


_CHECKS = {
    "T_admissibility_greedoid_structure":
        check_T_admissibility_greedoid_structure,
    "T_selection_approximate_A2":
        check_T_selection_approximate_A2,
    "T_finite_operational_basis_scope_contract":
        check_T_finite_operational_basis_scope_contract,
    "T_finite_operational_basis":
        check_T_finite_operational_basis,
    "T_finite_minimal_joint_realization_atom_cover":
        check_T_finite_minimal_joint_realization_atom_cover,
}

# ---------------------------------------------------------------------------
# IE onboarding -- the Paper 10 continuation calculus onto the ROUTE axis.
# ---------------------------------------------------------------------------
#
# Full Bank Onboarding: the finite-continuability capacity-floor bound is a
# structural identity, so it enters the Interface Engine's ROUTE axis as an
# internal-identity export (INTERNAL_IDENTITY_GLOBAL_P) rather than through the
# toy ``claim:capacity_overspend`` probe. The verdict inherits the grade of
# check_T_admissibility_greedoid_structure ([P_structural]); the routing adds
# no epistemic status -- the calculus becomes IE-reachable, no more.
IE_DECLARATIONS = (
    {
        "input_id": "foundation:continuation_capacity_floor_bound",
        "axis": "ROUTE",
        "route": "continuation_capacity_floor",
        "expect_export": True,
        "payload": {
            "name": "continuation_capacity_floor_bound",
            "closure_kind": "internal_identity",
            "identity_summary": (
                "The finite-continuability capacity-floor bound "
                "|S| <= N + J(S), with N = floor(C_Gamma / eps*), holds "
                "UNCONDITIONALLY by structural identity (composite-inclusive "
                "floor ruling, 2026-07-03): the derived cardinality bound is "
                "the codomain by construction, not an evaluator-transported "
                "export. M_break witness -- eps* = 1, N = floor(2/1) = 2, "
                "block |S| = 4 defeats the naive bound (4 > 2) while "
                "|S| <= N + J(S) = 2 + 3 = 5 holds. "
                "(check_T_admissibility_greedoid_structure, "
                "continuation_calculus.py)"
            ),
        },
        "note": (
            "Pre-existing Paper 10 capacity-floor identity. It does not by "
            "itself assert existence of a finite complete operational basis."
        ),
    },
    {
        "input_id": "foundation:finite_operational_basis_atom_cover_model",
        "axis": "ROUTE",
        "route": "continuation_finite_basis_atom_cover",
        "expect_export": True,
        "payload": {
            "name": "finite_operational_basis_atom_cover_model",
            "closure_kind": "internal_identity",
            "source_check": "T_finite_operational_basis",
            "scope_check": "T_finite_operational_basis_scope_contract",
            "compatible_realization_check": (
                "T_finite_minimal_joint_realization_atom_cover"
            ),
            "model_class": "finite_atom_cover",
            "hypotheses": list(_FINITE_BASIS_MODEL_HYPOTHESES),
            "non_claims": [
                "not_a_general_physical_joint_extension_theorem",
                "not_precision_channel_generation",
                "not_finite_smooth_generation",
            ],
            "identity_summary": (
                "IN THE DECLARED FINITE ATOM-COVER MODEL ONLY: finite admitted "
                "content atoms, subset-coded operational classes, union joint "
                "carrier/closure, and exact no-excess atom cost make the finite "
                "complete-basis extraction and one compatible minimum joint "
                "realization internal identities of the model. Exact Fraction "
                "arithmetic certifies |B_U| <= floor(C_U/eps*). This export does "
                "NOT discharge finite joint-extension/amalgamation on an "
                "arbitrary physical operational closure and does NOT generate "
                "precision channels or smooth geometry."
            ),
        },
        "note": (
            "Honest restricted-model export. The source and codomain coincide "
            "only after the finite atom-cover contract is declared."
        ),
    },
    {
        "input_id": "foundation:finite_operational_basis_general_bridge",
        "axis": "ROUTE",
        "route": "continuation_finite_basis_general",
        "expect_export": False,
        "payload": {
            "name": "finite_operational_basis_general_physical_bridge",
            "closure_kind": "obstruction_named",
            "obstruction_class": "FINITE_JOINT_EXTENSION_PACKAGE_REQUIRED",
            "source_check": "T_finite_operational_basis_scope_contract",
            "open_obligations": [
                "downward_closed_joint_realizability",
                "finite_joint_extension_or_amalgamation",
                "minimum_joint_realization_attainment",
                "closure_invariance_across_no_excess_minima",
            ],
            "knockout_summary": (
                "The exact finite atom-cover witness does not export the "
                "general physical finite-basis premise package. A general "
                "closed interface must separately establish a downward-closed "
                "joint-realizability domain, finite joint extension or "
                "amalgamation, attained minimum joint cost, and closure "
                "invariance. Until then the general theorem is conditional and "
                "no global-P physical bridge is exported."
            ),
            "target_value_consumed": False,
        },
        "note": (
            "Closure-by-design obstruction. Uses the existing Interface Atlas "
            "obstruction_named path; no new dependency or verdict system."
        ),
    },
    {
        "input_id": "foundation:finite_compatible_joint_realization_general_bridge",
        "axis": "ROUTE",
        "route": "continuation_compatible_joint_realization_general",
        "expect_export": False,
        "payload": {
            "name": "finite_compatible_joint_realization_general_bridge",
            "closure_kind": "obstruction_named",
            "obstruction_class": "COMPATIBLE_MINIMUM_JOINT_REALIZATION_REQUIRED",
            "source_check": "T_finite_minimal_joint_realization_atom_cover",
            "open_obligations": [
                "attained_minimum_joint_carrier_for_the_complete_basis",
                "deterministic_lossless_basis_projections",
                "shared_joint_carrier_compatibility",
            ],
            "knockout_summary": (
                "The atom-cover model constructs one minimum shared joint "
                "carrier, but arbitrary physical operational classes do not "
                "inherit compatible representatives from independently chosen "
                "classwise minima. The general compatible-realization bridge "
                "remains obstructed until one attained joint carrier and its "
                "lossless projections are proved."
            ),
            "target_value_consumed": False,
        },
        "note": (
            "Keeps compatibility distinct from individual minimum existence."
        ),
    },
    {
        "input_id": "foundation:operational_basis_to_precision_channel_bridge",
        "axis": "ROUTE",
        "route": "continuation_operational_to_precision_channel",
        "expect_export": False,
        "payload": {
            "name": "operational_basis_to_precision_channel_bridge",
            "closure_kind": "obstruction_named",
            "obstruction_class": "OPERATIONAL_TO_PRECISION_CHANNEL_REALIZATION_REQUIRED",
            "source_check": "T_finite_operational_basis",
            "open_obligations": [
                "joint_preservation",
                "recoverability_preservation_and_reflection",
                "reduced_state_separation",
                "faithful_real_limit",
            ],
            "knockout_summary": (
                "A finite operational-class basis is not yet a finite physical "
                "precision-channel basis. A faithful realization functor must "
                "preserve joint realizability, preserve and reflect closure, "
                "separate reduced states, and provide faithful real limits. "
                "This bridge remains explicitly open."
            ),
            "target_value_consumed": False,
        },
        "note": (
            "Paper 9 bridge gate; prevents the finite-basis theorem from "
            "silently generating physical refinement channels."
        ),
    },
)


def register(registry):
    """Register the continuation-calculus B3/B4 package into the bank."""
    registry.update(_CHECKS)


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == '__main__':
    for _n, _r in run_all().items():
        print(('PASS' if _r.get('passed', True) else 'FAIL'), _n)
        print('  grade:', _r['epistemic'], '| tier', _r['tier'])
        print('  ', _r['key_result'])
