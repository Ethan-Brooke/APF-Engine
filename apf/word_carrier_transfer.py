"""The word-side carrier transfer: what an argmin price determines, and where it stops.

Built 2026-08-03, first seat on
``Reference - CHARTER - The Carrier Transfer (2026-08-03)``.

AUDIT RECORD: blinded cold audits LAND-WITH-FIXES 0.85 / 0.78 / 0.85
(2026-08-03) + LAND-WITH-FIXES 0.87 different-day (2026-08-04); fixes
carried by separate fix seats each round. Banked v24.3.465 (2026-08-04).

------------------------------------------------------------------------------
WHAT THIS MODULE COMPUTES (exact arithmetic throughout; stdlib + fractions)
------------------------------------------------------------------------------

The carrier side: finite words over directed separators on a carrier graph
(vertex set X, edge set = available distinctions) with costs c({i,j}) > 0
read off the banked cost (``symmetry_cost_floor.config_cost``, by singleton
probe -- see R0). A word is a composable walk of length >= 1; length-0
walks are excluded (see NONEMPTY_ENFORCEMENT_PRESENTATION below). Its
contraction under the Wedderburn normal form pi(s_ij) = |i><j| (Paper 40
Supp rem:linear-realization: pi(s_ij)pi(s_kl) = delta_jk pi(s_il)) is the
matrix unit E_{i_0 i_m}; closed words contract to diagonal units. Two price
conventions are carried: SET (def:aps -- a word's structure is its support,
priced C(E) = sum c(d)) and MULTISET (each step billed).

R0 -- THE PROBE (check_L_banked_cost_probe). What it establishes, exactly:
the banked callee bills each probed pair equal positive weight, additively
over disjoint pairs (three decompositions sampled), linearly in the eps
argument (two ratios), distinguishably from its MD-violating cancelling
branch (a straddling probe pair is billed +1 / -1), and the callee IS the
banked module (identity pinned by __module__, the ledger_extension_degree
convention). The UNIT eps is supplied by the caller; every downstream value
is proportional in it. The probe touches the callee's pricing function
only; it does not consume the banked module's registered lemmas.

R1 -- THE FIBER OBSTRUCTION IS A STATEMENT ABOUT THE CARRIER GRAPH
(check_L_word_fiber_obstruction). In the MULTISET convention, no strictly
positive additive price is constant on the contraction fibers of closed
words, on ANY carrier here computed (complete n = 2..5 and both
disconnected fixtures; the loop-doubling certificate is
carrier-independent (here computed on the sampled carriers)). In the SET
(def:aps) convention the obstruction holds
on complete carriers with n >= 3; on a general carrier the computed kernel
is spanned by the K2-component edge directions -- kernel dimension = number
of K2 components (here computed on the sampled carriers: 2 on two K2s;
1 on K2 + K3) -- so a fiber-constant
positive price exists only when restricted to K2 components, and every
multi-edge component still obstructs. n = 2 is the one-component
instance of the K2 rule, not a boundary in n. Costs enter the kernel
computation only through the edge set; the obstruction is graph-theoretic.
Certificate: (0,1,0) and (0,1,2,0) both contract to E_00 with supports of
size 1 and 3. The n = 2 MULTISET kernel is 0 for words to length >= 4 and
1 below (computed at both L = 3 and L = 4).

R2 -- THE ARGMIN TRANSFER PRICES THE DIAGONAL AT THE INCIDENT MINIMUM
(check_T_argmin_transfer_diagonal). psi_min(a) := min{ price(w) : pi(w) = a }
is well-defined on the word image BY CONSTRUCTION -- a minimum over the
fiber, A2's own selection form. Closed forms, verified with counted
execution over every enumerated word and attained by exhibited witnesses:
SET psi_min(E_ii) = min_j c({i,j}); MULTISET twice that. (Structural
reason: a loop at i uses an edge incident to i in its first step -- and,
multiset, in its last -- so the price is bounded below by the incident
minimum; the 2-step loop attains it.) These forms hold on every carrier
computed here, complete or not. At the UNIFORM FLOOR the diagonal is the
constant eps: the induced functional on the diagonal subalgebra is exactly
eps*Tr. What the trace form consumes is CONSTANT INCIDENT MINIMA -- weaker
than uniformity, and computed in both directions: a strongly non-uniform
cost with constant incident minima still yields eps*Tr on the diagonal,
and a vertex whose every incident edge is expensive breaks it ((5,1,1,1)
control). EQUAL_COST_UNIFORMITY is declared as the stronger, def:aps-shaped
sufficient premise; the leg records the weaker operative one.

R3 -- PER-VERTEX PRICES; BLOCK CONSTANCY IS AN EQUAL-INCIDENT-MINIMA FACT
(check_T_block_constant_from_global_floor). On a disconnected carrier the
word algebra is a direct sum, one block per computed component, and
psi_min prices each diagonal entry at THAT VERTEX'S incident minimum --
R2's closed form, re-verified on disconnected carriers. A block's diagonal
is constant iff its vertices share their incident minimum (a 3-vertex
component with costs (5,4,1)eps has diagonal (4,1,1)eps -- computed
non-constancy); the uniform global floor forces all blocks constant and
equal. On the two-K2 carrier with component floors eps and 3eps the block
vector is (1,1,3,3)eps -- entrywise diag(R) for R = 1 (+) 3*1 in
M_2 (+) M_2, the counterexample prop:presentation-gauge-trace (P40 Supp)
prints against multi-block trace forcing. The computed fact is the vector
equality; what it is evidence for lives in this docstring and in no leg.

R4 -- THE CLOSED-SECTOR RESTRICTION IS LOAD-BEARING
(check_L_full_extension_not_forced). On the COMPLETE UNIFORM carrier
(CARRIER_COMPLETENESS + uniformity name this scope), the linear extension
of psi_min from ALL matrix units is the all-ones functional
psi(x) = eps * sum_ij x_ij -- positive there (psi(x*x) = eps*|x1|^2,
counted samples), and NOT cyclic (psi(ab) = 2eps != 4eps = psi(ba)). Off
the complete carrier the open-word extension is NOT even positive: on the
path P3 it takes -2eps on a rank-one PSD element (computed witness). So
the transfer's honest domain is the closed sector, where it determines the
diagonal subalgebra functional; the off-diagonal is free. The two-model
witness, as one leg: within linear functionals extending psi_min's
closed-sector (diagonal) values, eps*Tr and the all-ones functional agree
on every diagonal unit and differ on every off-diagonal unit -- so
word-priced data underdetermines exactly the off-diagonal, which is where
superposed separators live. That freedom is the charter's predicted
obstruction site, here as a computed localization.

R5 -- THE REFEREE (check_T_carrier_transfer_referee). The charter Sec. 5
property list as executable predicates over candidate records:
(a) additivity on disjoint structures (sampled at three disjoint
instances, a spot check, not a quantifier); (b) a superposition DECLARATION --
the predicate checks that a value is supplied and that its declared
inventory is carrier-side-only; IT DOES NOT VERIFY DERIVATION SEMANTICS,
and is named accordingly; (c1) diagonal trace recovery at the uniform
floor; (c2) full trace recovery; (d) declared-premise independence --
set-exact against FORBIDDEN over a known catalogue, GRADING THE
DECLARATION, and satisfiable by declaring nothing (the two control
fixtures with empty declarations document this in the table).
KNOWN_PREMISES is built as a union over FORBIDDEN_PREMISES, and no
forbidden name appears in the other two parts of that union, so a name
deleted from FORBIDDEN alone leaves the catalogue too and (d) returns
False on the same fixture either way: the table reads "forbidden" and
"not in the catalogue" alike. The content
of (b) and (d) is that the declarations are auditable data, not that the
referee verifies them. Fixtures: the Lambda^2 embedding, the Laplacian
map, the trivial scalar map, the stipulated trace, a broken-additivity
control, a wrong-diagonal control and a below-diagonal control (each
index-asymmetric in one sector, so quantifier restrictions on (c1) or (c2)
flip a verdict), an unknown-premise control, and this
module's own word-argmin candidate. Verdict table asserted set-exactly;
every fixture fails at least one predicate -- including word_argmin, which
fails (b) and (c2). A FRAME NOTE the table cannot decide: lambda2 is
failed on (d) because its pair-basis identification is frame-relative
(the 2026-08-01 survey's finding); the word transfer's own target frame is
the Wedderburn matrix-unit form, which P40 argues is canonical GIVEN
linearity -- the module classifies that under LINEAR_REALIZATION_TARGET,
not under P2. That classification is declared, not derived; an auditor may
attack it.

------------------------------------------------------------------------------
PREMISES, SET-EXACT (carried as data in PREMISES_CONSUMED /
PREMISES_NOT_CONSUMED; the word_argmin fixture declares PREMISES_CONSUMED
verbatim)
------------------------------------------------------------------------------
CONSUMED: DEF_APS_STRUCTURE_COST; LINEAR_REALIZATION_TARGET (the transfer
prices the algebra GIVEN the linearity residual and its canonical
matrix-unit frame; it does not discharge the residual); A2_ARGMIN
(constitutive under the A2-exact ruling); FD3_FLOOR (probed);
FD4_FINITE_CARRIER; EQUAL_COST_UNIFORMITY (for the trace form; operative
weakening recorded in R2); CARRIER_COMPLETENESS (scopes R4's positivity
leg ONLY -- R2's closed forms and R1's multiset obstruction do not consume
it); NONEMPTY_ENFORCEMENT_PRESENTATION -- the word domain excludes
length-0 WALKS. Named because it is load-bearing: the length-0 walk at i
contracts to E_ii at price C(emptyset) = 0, and admitting it collapses the
diagonal. (The empty word of the free monoid has no basepoint and
contracts to nothing in particular; the excluded object is the based
length-0 walk.) Whether the null presentation realizes the corner identity
is a physical question this module does not decide.
NOT CONSUMED: P1 (sandwich realization); P2 (presentation gauge); P3;
CYCLICITY; the phi := eps*Tr stipulation on the diagonal (that value is
here an argmin over fibers, not a declaration).

MAY NOT CITE (PERMANENT, ruled SC1@2026-09-01):
- "Born is derived" / "the carrier gap is closed" / "P1 is reduced". The
  transfer prices the diagonal of each block, under named premises; the
  off-diagonal is computed to remain free (R4).
- "The word transfer defines psi on the algebra." Its domain is the word
  image; the closed sector determines the diagonal subalgebra functional
  only, and the open-sector extension is not even positive off the
  complete carrier.
- "The fiber obstruction holds for all carriers." SET-mode it fails on K2
  components, by computed kernel dimension.
- "Branch N is established." R1 is an obstruction against ONE schema
  (pointwise reads of additive prices), scoped by carrier as stated.
- Any sentence attributing content here to what the module PREVENTS. It
  computes; it does not prevent.
"""

from fractions import Fraction as F
from itertools import combinations
from collections import defaultdict

# ---------------------------------------------------------------------------
# carrier layer
# ---------------------------------------------------------------------------

def all_pairs(n):
    return sorted({frozenset(p) for p in combinations(range(n), 2)}, key=sorted)

def words_on(cost, L):
    """All composable walks of length 1..L on the carrier graph whose edges
    are the keys of ``cost``. A walk is a tuple of vertices; length-0 walks
    are excluded here (NONEMPTY_ENFORCEMENT_PRESENTATION)."""
    adj = defaultdict(set)
    for e in cost:
        a, b = tuple(e)
        adj[a].add(b); adj[b].add(a)
    out = []
    frontier = [(i,) for i in sorted(adj)]
    for _ in range(L):
        nxt = [w + (j,) for w in frontier for j in sorted(adj[w[-1]])]
        out.extend(nxt)
        frontier = nxt
    return out

def contraction(w):
    """pi(word) as a matrix unit index, by the forced relations
    pi(s_ij)pi(s_kl) = delta_jk pi(s_il)."""
    return (w[0], w[-1])

def support(w):
    return frozenset(frozenset((w[t], w[t + 1])) for t in range(len(w) - 1))

def price(w, cost, mode):
    if mode == "set":
        return sum(cost[d] for d in support(w))
    if mode == "multiset":
        return sum(cost[frozenset((w[t], w[t + 1]))] for t in range(len(w) - 1))
    raise ValueError(mode)

def uniform_cost(n, eps):
    return {d: eps for d in all_pairs(n)}

def components(cost):
    """Connected components of the carrier graph, computed (union-find)."""
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for e in cost:
        a, b = tuple(e)
        parent[find(a)] = find(b)
    comp = defaultdict(set)
    for v in parent:
        comp[find(v)].add(v)
    return sorted((frozenset(c) for c in comp.values()), key=sorted)

def unit_matrix(n, i, j):
    return [[F(1) if (r, c) == (i, j) else F(0) for c in range(n)]
            for r in range(n)]

def matmul(a, b, n):
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]

# ---------------------------------------------------------------------------
# the banked floor, probed
# ---------------------------------------------------------------------------

def probed_eps():
    """Read the per-pair weight of the banked cost by singleton probe on
    ``symmetry_cost_floor.config_cost`` (the ledger_extension_degree
    convention). The unit eps is supplied by the caller of this module's
    checks; downstream values are proportional in it. The singleton probes
    are made at the non-unit argument F(3) and divided by 3, so the value
    read off the callee differs from the unit weight returned. A straddling
    pair (1, 2) -- it crosses the {0,1} | {2,..} split, on which the
    positive and cancelling branches return different values -- is probed
    in both modes and both values are compared against the singleton
    weight."""
    from apf import symmetry_cost_floor as scf
    unit = F(1)
    w01 = scf.config_cost({"sep_pairs": [(0, 1)]}, F(3), "positive") / 3
    w23 = scf.config_cost({"sep_pairs": [(2, 3)]}, F(3), "positive") / 3
    both = scf.config_cost({"sep_pairs": [(0, 1), (2, 3)]}, F(3), "positive") / 3
    straddle_pos = scf.config_cost({"sep_pairs": [(1, 2)]}, unit, "positive")
    straddle_can = scf.config_cost({"sep_pairs": [(1, 2)]}, unit, "cancelling")
    if not (straddle_pos == w01 and straddle_can == -w01):
        raise AssertionError(
            "probed_eps: straddling probe (1, 2) returned "
            f"({straddle_pos}, {straddle_can}), expected ({w01}, {-w01})")
    return w01, w23, both

# ---------------------------------------------------------------------------
# R1 kernel: fiber constancy over a carrier EDGE SET (costs enter only as
# the unknowns; the computation is graph-theoretic)
# ---------------------------------------------------------------------------

def fiber_kernel_dim(edges, L, mode):
    edges = sorted({frozenset(e) for e in edges}, key=sorted)
    cost = {d: F(1) for d in edges}   # decorative; enumeration needs a dict
    closed = [w for w in words_on(cost, L) if w[0] == w[-1] and len(w) > 1]
    idx = {d: k for k, d in enumerate(edges)}
    fibers = defaultdict(list)
    for w in closed:
        fibers[contraction(w)].append(w)

    def vec(w):
        v = [0] * len(edges)
        if mode == "set":
            for d in support(w):
                v[idx[d]] += 1
        else:
            for t in range(len(w) - 1):
                v[idx[frozenset((w[t], w[t + 1]))]] += 1
        return v

    rows = set()
    for ws in fibers.values():
        v0 = vec(ws[0])
        for w in ws[1:]:
            row = tuple(a - b for a, b in zip(v0, vec(w)))
            if any(row):
                rows.add(row)
    M = [[F(x) for x in r] for r in rows]
    rank = 0
    for col in range(len(edges)):
        piv = next((r for r in range(rank, len(M)) if M[r][col] != 0), None)
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        M[rank] = [x / M[rank][col] for x in M[rank]]
        for r in range(len(M)):
            if r != rank and M[r][col] != 0:
                M[r] = [a - M[r][col] * b for a, b in zip(M[r], M[rank])]
        rank += 1
    return len(edges) - rank

# ---------------------------------------------------------------------------
# R2 argmin transfer
# ---------------------------------------------------------------------------

def argmin_values(cost, L, mode, closed_only):
    vals, wits = {}, {}
    for w in words_on(cost, L):
        if closed_only and not (w[0] == w[-1] and len(w) > 1):
            continue
        a = contraction(w)
        p = price(w, cost, mode)
        if a not in vals or p < vals[a]:
            vals[a], wits[a] = p, w
    return vals, wits

def incident_min(cost, i):
    return min(c for d, c in cost.items() if i in d)

# ---------------------------------------------------------------------------
# result plumbing: set-exact leg inventory enforced on the check path
# ---------------------------------------------------------------------------

EXPECTED_LEGS = {
    "check_L_banked_cost_probe": [
        "additive_on_disjoint_singletons", "callee_module_attribute_and_value_tie",
        "control_duplicate_entry_double_bills",
        "control_md_mode_sign_follows_straddling_class",
        "control_probe_sees_weight_change",
        "singleton_weights_equal", "weight_is_positive",
    ],
    "check_L_word_fiber_obstruction": [
        "certificate_same_fiber", "certificate_supports_1_and_3",
        "disconnected_set_kernel_counts_k2_components",
        "kernel_multiset_n2_zero",
        "kernel_zero_n3_to_n5_complete_both_modes",
        "matrix_unit_product_rule_both_halves",
        "n2_multiset_threshold_at_L4", "set_mode_n2_kernel_exactly_one",
    ],
    "check_T_argmin_transfer_diagonal": [
        "closed_form_multiset_all_costs", "closed_form_set_all_costs",
        "control_nonuniform_diagonal_not_constant",
        "diagonal_equals_eps_trace_at_uniform_floor",
        "lower_bound_holds_every_word",
        "nonuniform_constant_incident_min_still_trace",
        "witness_attains_min",
    ],
    "check_T_block_constant_from_global_floor": [
        "block_vector_two_k2_floors_one_three",
        "components_computed_do_not_mix",
        "control_uniform_floor_blocks_equal",
        "per_vertex_price_is_incident_min",
        "three_vertex_component_diag_not_constant",
    ],
    "check_L_full_extension_not_forced": [
        "all_ones_extension_matches_argmin_on_units",
        "control_trace_is_cyclic_same_witness", "cyclicity_fails_witness",
        "noncomplete_extension_not_positive",
        "positivity_exact_identity",
        "two_model_witness_agree_closed_differ_open",
    ],
    "check_T_carrier_transfer_referee": [
        "control_synthetic_b_passer", "every_fixture_fails_somewhere",
        "own_candidate_fails_b_and_c2", "predicates_nonvacuous",
        "verdict_table_set_exact",
    ],
}

def _result(name, legs, fails, key_result):
    exp = EXPECTED_LEGS[name]
    got = sorted(legs)
    if got != exp:
        raise AssertionError(f"{name}: leg inventory mismatch: {got} != {exp}")
    for k, v in legs.items():
        if v is not True:
            fails.append(f"leg not True: {k}")
    return {
        "name": name,
        "passed": not fails,
        "legs": dict(legs),
        "fails": list(fails),
        "key_result": key_result,
        "tier": 3,
        "epistemic": "P_math",
        "status": "banked v24.3.465 (2026-08-04)",
    }

# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def check_L_banked_cost_probe():
    legs, fails = {}, []
    w01, w23, both = probed_eps()
    legs["singleton_weights_equal"] = (w01 == w23)
    legs["weight_is_positive"] = (w01 > 0)
    from apf import symmetry_cost_floor as scf
    cc = lambda pairs, e, m: scf.config_cost({"sep_pairs": pairs}, e, m)
    # the __module__ attribute plus a value tie between probed_eps's output
    # and a direct call made here; an extensionally correct bypass of
    # probed_eps remains invisible BY EXTENSIONALITY (documented, not
    # defended against)
    legs["callee_module_attribute_and_value_tie"] = (
        scf.config_cost.__module__ == "apf.symmetry_cost_floor"
        and cc([(0, 1)], F(1), "positive") == w01
        and cc([(0, 1), (2, 3)], F(1), "positive") == both)
    samples = [([(0, 1)], [(2, 3)]), ([(0, 2)], [(1, 3)]), ([(0, 3)], [(1, 2)])]
    legs["additive_on_disjoint_singletons"] = (both == w01 + w23) and all(
        cc(a + b, F(1), "positive") == cc(a, F(1), "positive") + cc(b, F(1), "positive")
        for a, b in samples)
    legs["control_duplicate_entry_double_bills"] = (
        cc([(0, 1), (0, 1)], F(1), "positive") == 2 * w01)
    # The (1, 2) mode split is enforced UPSTREAM by a raise inside
    # probed_eps, which this check calls on its first line; a leg
    # repeating that predicate could only ever be True.  Read here
    # instead, on six pairs that predicate does not cover: three
    # straddling pairs other than (1, 2), on which the two modes differ
    # in sign, and three non-straddling pairs, on which they agree.
    straddling = [(0, 2), (1, 3), (0, 3)]
    non_straddling = [(0, 1), (2, 3), (2, 4)]
    legs["control_md_mode_sign_follows_straddling_class"] = (
        len(straddling) == 3 and len(non_straddling) == 3
        and all(cc([p], F(1), "positive") == w01
                and cc([p], F(1), "cancelling") == -w01
                for p in straddling)
        and all(cc([p], F(1), "positive") == w01
                and cc([p], F(1), "cancelling") == w01
                for p in non_straddling))
    legs["control_probe_sees_weight_change"] = (
        cc([(0, 1)], F(2), "positive") == 2 * w01
        and cc([(0, 1)], F(3), "positive") == 3 * w01)
    return _result("check_L_banked_cost_probe", legs, fails,
                   {"per_pair_weight_at_unit_eps": str(w01)})

def check_L_word_fiber_obstruction():
    legs, fails = {}, []
    w1, w2 = (0, 1, 0), (0, 1, 2, 0)
    legs["certificate_same_fiber"] = (contraction(w1) == contraction(w2) == (0, 0))
    legs["certificate_supports_1_and_3"] = (len(support(w1)) == 1
                                            and len(support(w2)) == 3)
    dims = {(n, m): fiber_kernel_dim(all_pairs(n), 6, m)
            for n in (2, 3, 4, 5) for m in ("set", "multiset")}
    legs["kernel_zero_n3_to_n5_complete_both_modes"] = all(
        dims[(n, m)] == 0 for n in (3, 4, 5) for m in ("set", "multiset"))
    legs["set_mode_n2_kernel_exactly_one"] = (dims[(2, "set")] == 1)
    legs["kernel_multiset_n2_zero"] = (dims[(2, "multiset")] == 0)
    legs["n2_multiset_threshold_at_L4"] = (
        fiber_kernel_dim(all_pairs(2), 3, "multiset") == 1
        and fiber_kernel_dim(all_pairs(2), 4, "multiset") == 0)
    two_k2 = [frozenset((0, 1)), frozenset((2, 3))]
    k2_k3 = [frozenset((0, 1)), frozenset((2, 3)), frozenset((2, 4)),
             frozenset((3, 4))]
    legs["disconnected_set_kernel_counts_k2_components"] = (
        fiber_kernel_dim(two_k2, 6, "set") == 2
        and fiber_kernel_dim(k2_k3, 6, "set") == 1
        and fiber_kernel_dim(two_k2, 6, "multiset") == 0
        and fiber_kernel_dim(k2_k3, 6, "multiset") == 0)
    # the Wedderburn relation pi(s_ij)pi(s_kl) = delta_jk pi(s_il), BOTH
    # halves, by actual matrix arithmetic: for every ordered pair of short
    # words on K3, the product of their realized units is the unit of the
    # concatenation when composable and the ZERO matrix when not.
    n = 3
    Wc = words_on(uniform_cost(n, F(1)), 2)
    prods, expects = [], []
    for u in Wc:
        for v in Wc:
            mu = unit_matrix(n, *contraction(u))
            mv = unit_matrix(n, *contraction(v))
            prods.append(matmul(mu, mv, n))
            if u[-1] == v[0]:
                expects.append(unit_matrix(n, *contraction(u + v[1:])))
            else:
                expects.append([[F(0)] * n for _ in range(n)])
    legs["matrix_unit_product_rule_both_halves"] = (
        prods == expects and len(prods) == len(Wc) ** 2 and len(Wc) > 0
        and any(u[-1] != v[0] for u in Wc for v in Wc))
    k_two_k2 = fiber_kernel_dim(two_k2, 6, "set")
    k_k2_k3 = fiber_kernel_dim(k2_k3, 6, "set")
    return _result("check_L_word_fiber_obstruction", legs, fails,
                   {"kernel_dims_complete": {f"n{n}_{m}": dims[(n, m)]
                                             for n in (2, 3, 4, 5)
                                             for m in ("set", "multiset")},
                    "kernel_two_k2_set": k_two_k2,
                    "kernel_k2_k3_set": k_k2_k3})

def check_T_argmin_transfer_diagonal():
    legs, fails = {}, []
    eps, _, _ = probed_eps()
    L = 6
    costs = {
        "uniform": uniform_cost(4, eps),
        "generic": {d: c * eps for d, c in zip(all_pairs(4),
                    [F(1), F(2), F(7), F(3), F(11), F(5)])},
        "expensive_vertex0": {d: (5 * eps if 0 in d else eps)
                              for d in all_pairs(4)},
    }
    # tie by VALUE: the computed and the expected quantities are collected
    # as parallel lists and compared inside the leg expression itself.
    actual = {"set": [], "multiset": []}
    expected = {"set": [], "multiset": []}
    wit_prices, wit_vals = [], []
    bound_pairs = []
    for cname, cost in costs.items():
        for mode, factor in (("set", 1), ("multiset", 2)):
            vals, wits = argmin_values(cost, L, mode, closed_only=True)
            for i in range(4):
                actual[mode].append(vals[(i, i)])
                expected[mode].append(factor * incident_min(cost, i))
                wit_prices.append(price(wits[(i, i)], cost, mode))
                wit_vals.append(vals[(i, i)])
        for w in words_on(cost, L):
            if w[0] == w[-1] and len(w) > 1:
                bound_pairs.append((price(w, cost, "set"),
                                    incident_min(cost, w[0]),
                                    price(w, cost, "multiset")))
    # coverage pins, derived from the spec (three fixtures on K4, L = 6),
    # not from the iterated objects: 3 fixtures x 4 vertices = 12 diagonal
    # comparisons per mode; closed words of length 1..6 on K4 number
    # sum_{k=1..6} (3^k + 3(-1)^k) = 1092 per fixture, 3276 over the three.
    expected_cmp = 12
    expected_bound = 3276
    legs["closed_form_set_all_costs"] = (
        actual["set"] == expected["set"]
        and len(actual["set"]) == expected_cmp)
    legs["closed_form_multiset_all_costs"] = (
        actual["multiset"] == expected["multiset"]
        and len(actual["multiset"]) == expected_cmp)
    legs["witness_attains_min"] = (wit_prices == wit_vals
                                   and len(wit_prices) == 2 * expected_cmp)
    legs["lower_bound_holds_every_word"] = (
        len(bound_pairs) == expected_bound and expected_bound > 0
        and all(ps >= im and pm >= 2 * im for ps, im, pm in bound_pairs))
    vals_u, _ = argmin_values(costs["uniform"], L, "set", closed_only=True)
    legs["diagonal_equals_eps_trace_at_uniform_floor"] = all(
        vals_u[(i, i)] == eps for i in range(4))
    vals_b, _ = argmin_values(costs["expensive_vertex0"], L, "set", closed_only=True)
    diag_b = [vals_b[(i, i)] for i in range(4)]
    legs["control_nonuniform_diagonal_not_constant"] = (
        diag_b == [5 * eps, eps, eps, eps] and len(set(diag_b)) > 1)
    # the operative premise is CONSTANT INCIDENT MINIMA, weaker than
    # uniformity: strongly non-uniform costs with constant incident minima
    # still give the eps*Tr diagonal
    cim = dict(uniform_cost(4, eps))
    cim[frozenset((0, 1))] = 100 * eps
    cim[frozenset((2, 3))] = 37 * eps
    vals_c, _ = argmin_values(cim, L, "set", closed_only=True)
    legs["nonuniform_constant_incident_min_still_trace"] = (
        len(set(cim.values())) > 1
        and all(vals_c[(i, i)] == eps for i in range(4)))
    return _result("check_T_argmin_transfer_diagonal", legs, fails,
                   {"uniform_diagonal": [str(vals_u[(i, i)]) for i in range(4)],
                    "control_diagonal": [str(x) for x in diag_b],
                    "closed_form_comparisons_per_mode": expected_cmp,
                    "bound_words_checked": len(bound_pairs)})

def check_T_block_constant_from_global_floor():
    legs, fails = {}, []
    eps, _, _ = probed_eps()
    L = 6
    two_k2 = {frozenset((0, 1)): eps, frozenset((2, 3)): 3 * eps}
    mixed = {frozenset((0, 1)): eps,
             frozenset((2, 3)): 5 * eps, frozenset((2, 4)): 4 * eps,
             frozenset((3, 4)): eps}
    ok_mix = True
    for cost in (two_k2, mixed):
        comps = components(cost)
        for w in words_on(cost, L):
            if not any(set(w) <= c for c in comps):
                ok_mix = False
    legs["components_computed_do_not_mix"] = ok_mix and len(components(mixed)) == 2
    vals2, _ = argmin_values(two_k2, L, "set", closed_only=True)
    block_vector = [vals2[(i, i)] for i in range(4)]
    legs["block_vector_two_k2_floors_one_three"] = (
        block_vector == [eps, eps, 3 * eps, 3 * eps])
    valsm, _ = argmin_values(mixed, L, "set", closed_only=True)
    verts = sorted({v for d in mixed for v in d})
    legs["per_vertex_price_is_incident_min"] = all(
        valsm[(i, i)] == incident_min(mixed, i) for i in verts) and all(
        vals2[(i, i)] == incident_min(two_k2, i) for i in range(4))
    tri = [valsm[(i, i)] for i in (2, 3, 4)]
    legs["three_vertex_component_diag_not_constant"] = (
        tri == [4 * eps, eps, eps] and len(set(tri)) > 1)
    unif = {frozenset((0, 1)): eps, frozenset((2, 3)): eps}
    vu, _ = argmin_values(unif, L, "set", closed_only=True)
    legs["control_uniform_floor_blocks_equal"] = (
        len({vu[(i, i)] for i in range(4)}) == 1)
    return _result("check_T_block_constant_from_global_floor", legs, fails,
                   {"block_vector": [str(x) for x in block_vector],
                    "three_vertex_diag": [str(x) for x in tri]})

def check_L_full_extension_not_forced():
    legs, fails = {}, []
    eps, _, _ = probed_eps()
    n, L = 3, 6
    cost = uniform_cost(n, eps)
    vals, _ = argmin_values(cost, L, "set", closed_only=False)
    legs["all_ones_extension_matches_argmin_on_units"] = all(
        vals[(i, j)] == eps for i in range(n) for j in range(n))
    def psi_from(valdict):
        return lambda m: sum(valdict[(i, j)] * m[i][j]
                             for i in range(n) for j in range(n))
    psi = psi_from(vals)   # tied to the computed values, not a literal
    def mm(a, b, k):
        return [[sum(a[i][t] * b[t][j] for t in range(k)) for j in range(k)]
                for i in range(k)]
    def mt(a, k):
        return [[a[j][i] for j in range(k)] for i in range(k)]
    samples = [
        [[F(1), F(-2), F(0)], [F(3), F(1, 2), F(-1)], [F(0), F(4), F(1)]],
        [[F(0), F(1), F(1)], [F(-1), F(2), F(0)], [F(5), F(0), F(-3)]],
    ]
    lhs_list, rhs_list = [], []
    for x in samples:
        lhs_list.append(psi(mm(mt(x, 3), x, 3)))
        row = [sum(x[i][j] for j in range(3)) for i in range(3)]
        rhs_list.append(eps * sum(v * v for v in row))
    legs["positivity_exact_identity"] = (
        lhs_list == rhs_list and len(lhs_list) == len(samples) == 2
        and all(v >= 0 for v in lhs_list))
    # off the complete carrier the open-word extension is NOT positive:
    # P3 path, x = (1, 0, -1) row functional, x^T x rank-one PSD, psi = -2eps
    p3 = {frozenset((0, 1)): eps, frozenset((1, 2)): eps}
    vals_p3, _ = argmin_values(p3, L, "set", closed_only=False)
    psi_p3 = psi_from(vals_p3)
    xr = [[F(1), F(0), F(-1)], [F(0)] * 3, [F(0)] * 3]
    xtx = mm(mt(xr, 3), xr, 3)
    legs["noncomplete_extension_not_positive"] = (
        vals_p3[(0, 2)] == 2 * eps and psi_p3(xtx) == -2 * eps
        and psi_p3(xtx) < 0)
    a = [[F(1), F(1), F(0)], [F(0), F(0), F(0)], [F(0), F(0), F(0)]]
    b = [[F(1), F(0), F(0)], [F(1), F(0), F(0)], [F(0), F(0), F(0)]]
    ab = mm(a, b, 3); ba = mm(b, a, 3)
    # psi is psi_from(vals) -- tied to the computed open-word argmin values
    legs["cyclicity_fails_witness"] = (psi(ab) == 2 * eps
                                       and psi(ba) == 4 * eps
                                       and psi(ab) != psi(ba))
    tr = lambda m: m[0][0] + m[1][1] + m[2][2]
    legs["control_trace_is_cyclic_same_witness"] = (tr(ab) == tr(ba))
    closed_vals, _ = argmin_values(cost, L, "set", closed_only=True)
    tr_val = lambda i, j: eps if i == j else F(0)
    legs["two_model_witness_agree_closed_differ_open"] = (
        all(tr_val(i, i) == vals[(i, i)] == closed_vals[(i, i)]
            for i in range(n))
        and all(tr_val(i, j) != vals[(i, j)]
                for i in range(n) for j in range(n) if i != j))
    return _result("check_L_full_extension_not_forced", legs, fails,
                   {"psi_ab_vs_ba": [str(psi(ab)), str(psi(ba))],
                    "p3_negativity_witness": str(psi_p3(xtx))})

# ---------------------------------------------------------------------------
# R5: the referee
# ---------------------------------------------------------------------------

PREMISES_CONSUMED = frozenset({
    "LINEAR_REALIZATION_TARGET", "A2_ARGMIN", "FD3_FLOOR",
    "FD4_FINITE_CARRIER", "DEF_APS_STRUCTURE_COST",
    "EQUAL_COST_UNIFORMITY", "CARRIER_COMPLETENESS",
    "NONEMPTY_ENFORCEMENT_PRESENTATION",
})
PREMISES_NOT_CONSUMED = frozenset({
    "P1_SANDWICH_REALIZATION", "P2_PRESENTATION_GAUGE", "P3_UNDERIVED",
    "CYCLICITY", "PHI_EQ_EPS_TR_STIPULATION",
})
FORBIDDEN_PREMISES = frozenset({
    "P1_SANDWICH_REALIZATION", "P2_PRESENTATION_GAUGE", "P3_UNDERIVED",
    "PHI_EQ_EPS_TR_STIPULATION",
})
CARRIER_SIDE_LEAVES = frozenset({
    "FD3_FLOOR", "FD4_FINITE_CARRIER", "A2_ARGMIN", "DEF_APS_STRUCTURE_COST",
})
KNOWN_PREMISES = FORBIDDEN_PREMISES | CARRIER_SIDE_LEAVES | frozenset({
    "LINEAR_REALIZATION_TARGET", "EQUAL_COST_UNIFORMITY",
    "CARRIER_COMPLETENESS", "GL_INVARIANT_EMBEDDING_CHOICE",
    "EMBEDDING_CHOICE", "NONEMPTY_ENFORCEMENT_PRESENTATION",
})

def _fixtures(eps):
    n = 3
    C = lambda S: eps * len(S)
    vals_argmin, _ = argmin_values(uniform_cost(n, eps), 6, "set",
                                   closed_only=True)
    tr_units = {(i, j): (eps if i == j else F(0))
                for i in range(n) for j in range(n)}
    wrong = dict(tr_units)
    wrong[(0, 0)] = 2 * eps     # c1 (and c2) fail at index 0 only
    below = dict(tr_units)
    below[(1, 0)] = eps         # c2 fails BELOW the diagonal only; c1 holds
    return {
        "lambda2_embedding": {
            "structure_price": C, "unit_values": None, "superposition": None,
            "premises": {"P2_PRESENTATION_GAUGE"},
        },
        "laplacian_map": {
            "structure_price": lambda S: eps * len(S),
            "unit_values": None, "superposition": None,
            "premises": {"GL_INVARIANT_EMBEDDING_CHOICE"},
        },
        "trivial_scalar": {
            "structure_price": C, "unit_values": None, "superposition": None,
            "premises": {"EMBEDDING_CHOICE"},
        },
        "stipulated_trace": {
            "structure_price": C,
            "unit_values": dict(tr_units),
            "superposition": (lambda s, t: F(0), {"PHI_EQ_EPS_TR_STIPULATION"}),
            "premises": {"PHI_EQ_EPS_TR_STIPULATION"},
        },
        "broken_additivity": {
            "structure_price": lambda S: eps * len(S) ** 2,
            "unit_values": None, "superposition": None,
            "premises": set(),
        },
        "wrong_diagonal_control": {
            "structure_price": C, "unit_values": wrong, "superposition": None,
            "premises": set(),
        },
        "below_diagonal_control": {
            "structure_price": C, "unit_values": below, "superposition": None,
            "premises": set(),
        },
        "unknown_premise_control": {
            "structure_price": C, "unit_values": None, "superposition": None,
            "premises": {"NOT_IN_ANY_CATALOGUE"},
        },
        "word_argmin": {
            "structure_price": C,
            "unit_values": {u: v for u, v in vals_argmin.items()},
            "superposition": None,
            "premises": set(PREMISES_CONSUMED),
        },
    }

def _run_predicates(name, cand, eps, n=3):
    pairs = all_pairs(n)
    sp = cand["structure_price"]
    pa = all(sp(A | B) == sp(A) + sp(B) for A, B in [
        (frozenset([pairs[0]]), frozenset([pairs[2]])),
        (frozenset([pairs[0]]), frozenset([pairs[1]])),
        (frozenset([pairs[0], pairs[1]]), frozenset([pairs[2]])),
    ])
    sup = cand["superposition"]
    pb = sup is not None and set(sup[1]) <= CARRIER_SIDE_LEAVES
    uv = cand["unit_values"]
    pc1 = uv is not None and all(uv.get((i, i)) == eps for i in range(n))
    pc2 = (uv is not None
           and all(uv.get((i, j)) == (eps if i == j else F(0))
                   for i in range(n) for j in range(n)))
    prem = set(cand["premises"])
    pd = prem <= KNOWN_PREMISES and not (prem & FORBIDDEN_PREMISES)
    return {"a": pa, "b": pb, "c1": pc1, "c2": pc2, "d": pd}

EXPECTED_VERDICTS = {
    "lambda2_embedding": {"a": True, "b": False, "c1": False, "c2": False, "d": False},
    "laplacian_map":     {"a": True, "b": False, "c1": False, "c2": False, "d": True},
    "trivial_scalar":    {"a": True, "b": False, "c1": False, "c2": False, "d": True},
    "stipulated_trace":  {"a": True, "b": False, "c1": True,  "c2": True,  "d": False},
    "broken_additivity": {"a": False, "b": False, "c1": False, "c2": False, "d": True},
    "wrong_diagonal_control": {"a": True, "b": False, "c1": False, "c2": False, "d": True},
    "below_diagonal_control": {"a": True, "b": False, "c1": True, "c2": False, "d": True},
    "unknown_premise_control": {"a": True, "b": False, "c1": False, "c2": False, "d": False},
    "word_argmin":       {"a": True, "b": False, "c1": True,  "c2": False, "d": True},
}

def check_T_carrier_transfer_referee():
    legs, fails = {}, []
    eps, _, _ = probed_eps()
    fx = _fixtures(eps)
    verdicts = {name: _run_predicates(name, cand, eps)
                for name, cand in fx.items()}
    legs["verdict_table_set_exact"] = (verdicts == EXPECTED_VERDICTS)
    legs["every_fixture_fails_somewhere"] = all(
        not all(v.values()) for v in verdicts.values())
    legs["own_candidate_fails_b_and_c2"] = (
        verdicts["word_argmin"]["b"] is False
        and verdicts["word_argmin"]["c2"] is False)
    preds = ["a", "b", "c1", "c2", "d"]
    fails_somewhere = all(any(not verdicts[f][p] for f in verdicts)
                          for p in preds)
    passes_somewhere = all(any(verdicts[f][p] for f in verdicts)
                           for p in ["a", "c1", "c2", "d"])
    legs["predicates_nonvacuous"] = fails_somewhere and passes_somewhere
    synthetic_b = {
        "structure_price": lambda S: eps * len(S),
        "unit_values": None,
        "superposition": (lambda s, t: F(0), {"FD3_FLOOR"}),
        "premises": set(),
    }
    legs["control_synthetic_b_passer"] = (
        _run_predicates("synthetic_b", synthetic_b, eps)["b"] is True)
    return _result("check_T_carrier_transfer_referee", legs, fails,
                   {"verdicts": {k: dict(v) for k, v in verdicts.items()}})

ALL_CHECKS = [
    check_L_banked_cost_probe,
    check_L_word_fiber_obstruction,
    check_T_argmin_transfer_diagonal,
    check_T_block_constant_from_global_floor,
    check_L_full_extension_not_forced,
    check_T_carrier_transfer_referee,
]

def run_all():
    results = []
    for fn in ALL_CHECKS:
        r = fn()
        results.append(r)
        status = "PASS" if r["passed"] else "FAIL"
        n_true = sum(1 for v in r["legs"].values() if v is True)
        print(f"[{status}] {r['name']}  legs={n_true}/{len(r['legs'])}")
        if not r["passed"]:
            for f in r["fails"]:
                print("   -", f)
    print(f"{sum(r['passed'] for r in results)}/{len(results)} checks pass")
    return results

# ---------------------------------------------------------------------------
# registration -- BARE-name keys per the 2026-08-03 D6 ruling (canonical for
# new modules; by-name gates check both spellings)
# ---------------------------------------------------------------------------

_CHECKS = {
    'L_banked_cost_probe': check_L_banked_cost_probe,
    'L_word_fiber_obstruction': check_L_word_fiber_obstruction,
    'T_argmin_transfer_diagonal': check_T_argmin_transfer_diagonal,
    'T_block_constant_from_global_floor': check_T_block_constant_from_global_floor,
    'L_full_extension_not_forced': check_L_full_extension_not_forced,
    'T_carrier_transfer_referee': check_T_carrier_transfer_referee,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


if __name__ == "__main__":
    run_all()
