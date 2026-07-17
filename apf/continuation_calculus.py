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


def _u(sets):
    sets = list(sets)
    return frozenset().union(*sets) if sets else frozenset()


def _rich_family(rng, m, ntry):
    """A LARGE operational-class family over m content atoms: random nonempty
    atom-subsets. Singletons are NOT forced -- so closed-world completeness
    (union(F) == Omega) is a genuine, sometimes-false property, and the number
    of classes is a-priori large (up to 2^m - 1), independent of the content
    dimension m."""
    Omega = frozenset(range(m))
    F = set()
    for _ in range(int(ntry)):
        k = int(rng.integers(1, m + 1))
        F.add(frozenset(int(x) for x in rng.choice(m, size=k, replace=False)))
    return Omega, sorted(F, key=lambda s: (len(s), sorted(s)))


def _greedy_basis(Omega, F):
    """Greedy: add a class outside the current operational closure until closed
    or STUCK. Returns (B, covered, stuck); stuck is True iff closed-world
    completeness fails (an uncovered distinction has no supplying class)."""
    covered = frozenset(); B = []
    while covered != Omega:
        cand = next((c for c in F if not (c <= covered)), None)
        if cand is None:
            return B, covered, True
        covered |= cand; B.append(cand)
    return B, covered, False


def _minimize(B, Omega):
    M = list(B); changed = True
    while changed:
        changed = False
        for i in range(len(M)):
            rest = _u(M[j] for j in range(len(M)) if j != i)
            if M[i] <= rest:
                del M[i]; changed = True; break
    return M


def check_T_finite_operational_basis():
    rng = np.random.default_rng(_SEED)
    adm = inadm = stuck = tight = incr_used = 0

    for _ in range(600):
        eps = float(rng.uniform(0.4, 2.5))
        C = float(rng.uniform(1.0, 12.0))
        Nmax = math.floor(C / eps + 1e-9)          # capacity-floor bound on # commitments
        if Nmax < 1:
            continue
        m = int(rng.integers(1, 11))               # content dimension, INDEPENDENT of C
        Omega, F = _rich_family(rng, m, rng.integers(1, 2 ** min(m, 6) + 1))
        content_cost = m * eps                     # no-excess cost of realizing all of A_U
        admissible = content_cost <= C + 1e-9      # <=> m <= Nmax
        cwc = _u(F) == Omega                       # closed-world completeness (fallible)

        # (v) THE BOUND BITES: content beyond floor(C/eps*) cannot be admitted
        if not admissible:
            inadm += 1
            check(m > Nmax,
                  "inadmissible: content dimension m > floor(C/eps*)")
            check(content_cost > C + 1e-9,
                  "CONTROL (bound bites): |Omega| > floor(C/eps*) => realizing A_U costs "
                  "> C => the closed interface CANNOT admit A_U (theorem precondition "
                  "fails). floor(C/eps*) does real bounding work.")
            continue
        adm += 1
        if m == Nmax:
            tight += 1

        B, covered, is_stuck = _greedy_basis(Omega, F)

        # (vi) CLOSED-WORLD COMPLETENESS is genuinely USED and fallible
        if not cwc:
            stuck += 1
            check(is_stuck and covered != Omega,
                  "CONTROL (closed-world used): union(F) != Omega => greedy STUCK "
                  "(an uncovered distinction has no supplying class) and cl(B) != A_U "
                  "-- no false complete basis is reported")
            check(any(a not in _u(F) for a in Omega),
                  "the uncovered distinction is a real gap in the admitted ledger")
            continue

        # cwc holds and A_U admissible: the theorem applies
        check(not is_stuck, "closed-world completeness => greedy never stuck")

        # (ii) A2 distinction-increment, exercised on the LARGE family's greedy steps
        sub = frozenset()
        for c in B:
            if not (c <= sub):
                inc = (len(sub | c) - len(sub)) * eps
                check(inc >= eps - 1e-12,
                      "A2 distinction-increment: a class outside cl(S) commits >= eps* "
                      "(licensed by no-excess cost = |covered|*eps*)")
                incr_used += 1
            sub |= c

        # existence + completeness + the bound, on an a-priori-large class family
        check(covered == Omega and all(c <= covered for c in F),
              "cl(B_U) = A_U: a finite COMPLETE basis was extracted from the large "
              "class family (|F| up to 2^m - 1)")
        check(len(B) <= Nmax,
              "|B_U| <= floor(C_U/eps*): capacity + floor bound the basis of an "
              "a-priori-large family")

        # (iii) inclusion-minimality
        M = _minimize(B, Omega)
        check(_u(M) == Omega,
              "minimized basis still covers the full content")
        for i in range(len(M)):
            rest = _u(M[j] for j in range(len(M)) if j != i)
            check(not (M[i] <= rest), "inclusion-minimal: no basis member is redundant")
        check(len(M) <= Nmax, "minimal basis size <= floor(C_U/eps*)")

        # (iv) finite minimal realization corollary
        R = [(c, "no-excess-realization") for c in M]
        check(len(R) == len(M) <= Nmax,
              "finite minimal-realization family, one no-excess realization per basis class")

    # every arm must actually fire -- the body is falsifiable, not decorative
    check(adm > 30 and inadm > 20 and stuck > 10 and tight > 0 and incr_used > 50,
          f"arms exercised: admissible={adm}, inadmissible/bound-bites={inadm}, "
          f"closed-world-stuck={stuck}, capacity-tight={tight}, increment-steps={incr_used}")

    # (vii) A2 NO-EXCESS is load-bearing: excess reserved for an uncovered atom kills the increment
    eps = 1.0
    reserved = frozenset({5})
    cost_excess = lambda U: float(len(U | reserved))   # capacity pre-reserved for atom 5, billed regardless
    Su = frozenset({0})
    check(abs(cost_excess(Su | {5}) - cost_excess(Su)) < 1e-12,
          "CONTROL (A2 no-excess used): with capacity pre-reserved for an uncovered "
          "distinction (A2 violated), that distinction is absorbed at 0 marginal -- the "
          "increment lemma requires A2 no-excess, so the body's cost = |covered|*eps* is "
          "the NO-EXCESS minimal cost, not a free assumption")

    # (viii) the marginal floor eps* > 0 is doubly load-bearing
    cost_free = lambda U: sum(1.0 for a in U if a != 3)   # atom 3 carries no floor
    check(abs(cost_free(frozenset({0, 1}) | {3}) - cost_free(frozenset({0, 1}))) < 1e-12,
          "CONTROL (floor used, increment): a distinction with no floor adds at 0 marginal")
    check(math.floor(6.0 / 1e-9) > 10 ** 8,
          "CONTROL (floor used, bound): eps* -> 0 makes floor(C/eps*) vacuous")

    # (ix) SCOPE FENCE (causal): basis size is invariant under realization multiplicity
    Omega_s = frozenset({0, 1, 2})
    F_s = [frozenset({0, 1}), frozenset({2}), frozenset({0}), frozenset({1, 2})]

    def _N_under_mult(F, mult):
        # each class carries mult[c] realizations; the basis is over CLASSES
        # (dedup by atom-set), so it is invariant to the multiplicities. The
        # realization total is counted abstractly (never materialized).
        total = sum(mult.get(c, 1) for c in F)
        classes = sorted(set(F), key=lambda s: (len(s), sorted(s)))
        B, _, _ = _greedy_basis(Omega_s, classes)
        return len(_minimize(B, Omega_s)), total

    N1, tot1 = _N_under_mult(F_s, {c: 1 for c in F_s})
    N2, tot2 = _N_under_mult(F_s, {frozenset({0, 1}): 10 ** 6, frozenset({2}): 10 ** 9,
                                   frozenset({0}): 7, frozenset({1, 2}): 10 ** 4})
    check(N1 == N2 and tot2 > 10 ** 8 and tot1 < 10,
          "SCOPE FENCE (causal): expanding each class to 10^6..10^9 realizations "
          f"(total {tot2} vs {tot1}) leaves the basis size unchanged (N={N1}) -- finite "
          "generation counts DISTINCT operational classes, not realizations / terminal "
          "values (warn:ts-basis-scope)")

    return _result(
        name='T_finite_operational_basis -- the Finite Operational Basis Theorem '
             '(Paper 10 v1.20; canonical home Paper 10)',
        tier=4,
        epistemic='P_structural',
        summary=(
            'Extends the B3 capacity-floor BOUND (check_T_admissibility_greedoid_'
            'structure, |S| <= floor(C/eps*)) to the EXISTENCE half. Closed-'
            'interface content model: Omega = the admitted operational distinction '
            'content (m atoms); a LARGE class family F of atom-subsets (up to 2^m-1, '
            'singletons NOT forced); no-excess joint cost = |covered atoms|*eps*. '
            'The randomized body is falsifiable and exercises four arms (600 models: '
            'admissible / inadmissible / closed-world-stuck / capacity-tight): '
            '(1) when A_U is admissible (m <= floor(C/eps*)) and closed-world '
            'completeness holds (union(F)=Omega), greedy extracts from the large '
            'family a finite COMPLETE basis, cl(B_U)=A_U, with |B_U| <= '
            'floor(C_U/eps*), inclusion-minimal after redundancy removal, plus the '
            'finite minimal-realization corollary; (2) the A2 distinction-increment '
            'is exercised on the greedy steps. The load-bearing hypotheses are '
            'witnessed as FALLIBLE: closed-world completeness genuinely fails on '
            'non-covering families (greedy STUCK, no false basis reported); the '
            'bound BITES -- content with m > floor(C/eps*) is inadmissible (cost > '
            'C), so floor(C_U/eps*) does real bounding work rather than being fitted; '
            'A2 no-excess is required (reserved excess absorbs a distinction at 0 '
            'marginal); the floor eps* > 0 is doubly required (a floor-free atom '
            'breaks the increment, eps* -> 0 makes the bound vacuous); and the SCOPE '
            'FENCE is causal -- expanding classes to 10^6..10^9 realizations leaves '
            'the basis size unchanged (finite generation != finite image, '
            'warn:ts-basis-scope). Paper anchor: Paper 10 v1.20 '
            'sec:finite-operational-basis.'
        ),
        key_result=(
            'On the finite content model, closed-world completeness (fallible) + A2 '
            'no-excess (fallible) + marginal floor eps* (fallible) + finite capacity '
            'witness a finite COMPLETE operational-distinction-class basis with '
            'cl(B_U)=A_U extracted from an a-priori-large family, |B_U| <= '
            'floor(C_U/eps*); inclusion-minimal; finite minimal-realization '
            'corollary. Each hypothesis is exercised as load-bearing via a genuine '
            'fail-arm; the bound bites (m > floor(C/eps*) inadmissible); basis '
            'counts classes, not realizations. Combinatorial finite-model witness of '
            'the Paper 10 v1.20 theorem (not a derivation of the physical premises).'
        ),
        dependencies=['A1', 'L_epsilon*', 'T_admissibility_greedoid_structure'],
        cross_refs=['T_admissibility_greedoid_structure', 'T_selection_approximate_A2',
                    'T_sep', 'FD1_structural_completeness'],
        artifacts={
            'extends': 'B3 bound |S|<=floor(C/eps*) -> EXISTENCE of a complete basis at that bound',
            'arms_exercised': ['admissible', 'inadmissible(bound-bites)',
                               'closed-world-stuck', 'capacity-tight'],
            'controls': ['A2 no-excess (reserved excess kills increment)',
                         'floor eps*>0 (increment + finite bound)',
                         'scope fence causal (N invariant under 10^9 realizations)'],
            'paper_anchor': 'Paper 10 v1.20 sec:finite-operational-basis',
        },
    )


_CHECKS = {
    'T_admissibility_greedoid_structure':
        check_T_admissibility_greedoid_structure,
    'T_selection_approximate_A2':
        check_T_selection_approximate_A2,
    'T_finite_operational_basis':
        check_T_finite_operational_basis,
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
            "Onboards the Paper 10 continuation calculus (the APF core math) "
            "onto the ROUTE axis. Sources the capacity-floor bound from the "
            "greedoid structural theorem [P_structural] in place of the toy "
            "capacity-overspend scenario probe; verdict is a structural "
            "identity, no physics import."
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
