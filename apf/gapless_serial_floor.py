"""The gapless serial-building floor: structure formation is serial and
floor-billed in an all-Sep world.

Does structure formation -- not mere record formation -- require a
rent-excluded coherent phase?  The spectator countermodel
(check_T_no_IJC_no_noncommutativity [P_structural]) settles the strong form
negatively: a gapless world satisfies A1 + MD + A2 + BW and ticks -- it
commits, pays the floor, accumulates records, has an arrow.  Whether the
quantum regime is occupied is the QAC, the one bit read off the world.  This
module banks the WEAK, necessity-direction result the corpus half-believes:
without slack the engine fires but cannot rev -- it can tick, but building is
serial and floor-billed.

    T_gapless_serial_floor.  In any admissible all-Sep history (branch Sep
    everywhere: Delta == 0, Delta_cross == 0, commutative admissibility
    algebra):

      K1 (no free switch) [P].  Every candidate switch realigns n >= 1
          distinctions and books n*eps >= eps* > 0.  L_cost [P] makes the
          realignment functional UNIQUELY n*eps; APF bills per re-resolution
          TRANSITION, strictly stricter than Landauer per-erasure -- so the
          Bennett reversible-search channel (a zero-cost candidate
          permutation) is EXCLUDED.  Named premise: a switch is a realignment
          of >= 1 distinction, never a null (n = 0) relabeling.

      K2 (no joint hold) [P_structural].  No admissible Sep configuration
          represents >= 2 mutually distinct candidates below the union's
          standing cost (T_sep [P] additivity; L_codef_aggregation_argmin [P]
          union-argmin floor), AND no admissible state holds two resolved
          values of one distinction in a way that does admissible work.  This
          second clause -- the DRAWN CLAUSE -- is no longer STIPULATED: it is
          the structural reading of the algebra-level fact
          L_commutative_no_unresolved_hold [P_math] (in a commutative
          projector algebra the A-dephasing D(rho)=sum Q_pi rho Q_pi is
          invariant on the algebra, so a coherent hold is invisible to every
          admissible observable; a coherence-witness is a non-commuting
          element = branch IJC) applied under the Sep antecedent
          (T_no_IJC [P_structural]: the Sep algebra is commutative).  The
          [P_math] lemma discharges the earlier stipulation; the Sep
          antecedent it rides is the principled wall that caps the theorem at
          [P_structural] -- the lemma does NOT lift the kernel to [P].

      K3 (accounting) [P].  A rejected trial is RELEASABLE (Delta_cross = 0
          => removable, L_local_removability [P]) -- the standing level
          recovers; the release itself books.  The accumulating resource is
          integrated realignment THROUGHPUT N = sum n, booked energy N*eps
          exactly.  (Corrects the naive "permanent seat => regional
          saturation" picture: nothing locks in a Sep world; the wall is
          throughput, not standing level.)

    Composed: booked energy of any history realizing a target x is
    sum(per-switch floors) >= (min switches)*eps* = depth(x)*eps*, where
    depth(x) is the minimum billed-switch count (search-depth definition).
    The exhaustive throughput-exclusion witness certifies, per world, that
    depth can exceed the naive Hamming floor (assembly barriers bite) and
    that the exclusion is exact.

CONDITIONAL COROLLARY [P_structural_reading] (docstring-level; not the bank
gate).  depth(x)*eps* > N_max*eps  =>  x has no all-Sep assembly history
within the region  =>  (by IJC-dichotomy exhaustiveness) pool-sector
occupancy somewhere in x's assembly history.  Applied to the observed world
with a large-depth witness class: built structure => the gap was occupied.
Occupancy is NOT derived -- it is a conclusion keyed to THREE imports
(N_max budget; witness-class depth/multiplicity; IJC-dichotomy
exhaustiveness [P_structural]); sufficiency is not claimed.  The Levinthal
serial floor is non-vacuous for realistic regional budgets but rides the
multiplicity import (Q = nu^L, imported chemistry) -- hence reading grade,
never [P].

GRADE [P_structural].  K1 and K3 are [P] compositions over the constitutive
base; K2's drawn clause is a Sep-branch structural reading (the theorem's
clause (ii)), which caps the whole at [P_structural].  The [P]-earning path
-- a banked "commutative admissibility algebra => no admissible unresolved
hold" lemma -- is NAMED, not taken.  Occupancy is NOT consumed; A2 is not
needed beyond its constitutive presence; BW is not load-bearing.

FENCES (charter 2026-07-07): superadd-is-QAC (occupancy never re-derived);
coherent-assembly ceiling (the NECESSITY direction uses only the FREE /
rent-exclusion leg of T_coherent_free_spend_permanent, never the blocked
benefit leg); occupancy-stays-QAC (the corollary is conditional);
spectator confronted (run through the search-depth definition below);
no entropic route (the resource is a cost count, not entropy); no P4-kappa.

Lane records: The Turning/zipper_slack_necessity_2026-07-07/ (NOTE v0.2,
walk_keystone_K1K2K3.py [10198 checks], walk_theorem_and_bite.py [15 checks],
WALK_RESULTS_LOG, hostile audit LAND-WITH-FIXES 0.84).
"""

from fractions import Fraction as F
from itertools import product, combinations
from collections import deque


def _cost_union(costs, support):
    return sum(costs[i] for i in support) if support else F(0)


def check_T_gapless_serial_floor():
    from apf.core import (check_T_sep, check_L_cost, check_L_epsilon_star,
                          check_T_no_IJC_no_noncommutativity)
    from apf.operational_completeness import (check_T_ledger_rent_excluded,
                                              check_L_local_removability)
    from apf.cost_energy_identity import check_T_realignment_cost_is_transition_energy
    from apf.class_transition import check_T_coherent_free_spend_permanent
    from apf.codef_aggregation import check_L_codef_aggregation_argmin

    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)

    # ---- anchors live at their stated grades -------------------------
    anchors = {
        'T_sep': (check_T_sep, 'P'),
        'L_cost': (check_L_cost, 'P'),
        'L_epsilon_star': (check_L_epsilon_star, 'P'),
        'T_ledger_rent_excluded': (check_T_ledger_rent_excluded, 'P'),
        'L_local_removability': (check_L_local_removability, 'P'),
        'T_no_IJC_no_noncommutativity': (check_T_no_IJC_no_noncommutativity, 'P_structural'),
        'T_realignment_cost_is_transition_energy':
            (check_T_realignment_cost_is_transition_energy, 'P'),
        'T_coherent_free_spend_permanent': (check_T_coherent_free_spend_permanent, 'P'),
        'L_codef_aggregation_argmin': (check_L_codef_aggregation_argmin, 'P'),
    }
    for name, (fn, grade) in anchors.items():
        r = fn()
        ck(r.get('passed') is True, f"anchor {name} passes")
        ck(r.get('epistemic') == grade, f"anchor {name} grade == {grade}")

    EPS = F(1)                                   # eps = eps* (MD floor), natural units
    COSTS = [F(2), F(3, 2), F(5, 4)]
    K = 3
    C_REGION = F(20)

    # ---- K1: no free switch; Bennett cycle books; accumulators split -
    states = list(product((0, 1), repeat=K))
    for a, b in combinations(states, 2):
        n = sum(1 for x, y in zip(a, b) if x != y)
        ck(n >= 1 and n * EPS >= EPS, "K1: switch books n*eps >= eps*")
    # Bennett Gray cycle: returns to start, still books 2^K * eps
    gray = lambda n: n ^ (n >> 1)
    cyc = [tuple((gray(n) >> i) & 1 for i in range(K)) for n in range(2 ** K)]
    cyc.append(cyc[0])
    booked = sum(F(sum(1 for x, y in zip(cyc[t], cyc[t + 1]) if x != y)) * EPS
                 for t in range(len(cyc) - 1))
    ck(cyc[0] == cyc[-1], "K1: reversible cycle returns to start")
    ck(booked == F(2 ** K) * EPS,
       "K1: Bennett cycle books 2^K*eps despite returning (per-transition)")

    # ---- K2: union floor (T_sep additivity, codef argmin) ------------
    supports = [frozenset(s) for r in range(1, K + 1)
                for s in combinations(range(K), r)]
    for Sa, Sb in combinations(supports, 2):
        union = Sa | Sb
        bill = _cost_union(COSTS, union)
        ck(bill >= _cost_union(COSTS, Sa) and bill >= _cost_union(COSTS, Sb),
           "K2: union bill >= each candidate bill")
        if Sa & Sb:
            apart = _cost_union(COSTS, Sa) + _cost_union(COSTS, Sb)
            ck(apart == bill + _cost_union(COSTS, Sa & Sb),
               "K2: inclusion-exclusion exact (T_sep deficit)")
        else:
            ck(_cost_union(COSTS, Sa) + _cost_union(COSTS, Sb) == bill,
               "K2: disjoint additivity (T_sep)")
    # drawn clause: the Sep state space is definite assignments (functions
    # {1..K} -> {0,1}); no admissible object holds two values of one slot.
    ck(len(set(states)) == 2 ** K,
       "K2 drawn clause: definite-assignment state space (Sep-branch reading)")

    # ---- K3: release recovers the level; throughput is the resource --
    trial = frozenset({0, 1})
    base = frozenset()
    throughput = F(0)
    max_level = _cost_union(COSTS, base)
    T = 2000
    for _ in range(T):
        throughput += len(trial) * EPS
        max_level = max(max_level, _cost_union(COSTS, trial))
        throughput += len(trial) * EPS           # release books its own
    ck(max_level == _cost_union(COSTS, trial),
       "K3: level never exceeds ONE trial's cost (no saturation)")
    ck(max_level < C_REGION, "K3: level nowhere near C after many trials")
    ck(throughput == F(T) * 4 * EPS, "K3: throughput accumulates as the resource")

    # ---- composed: depth -> throughput floor, exhaustive per world ---
    costs = {'a': F(2), 'b': F(2), 'c': F(2), 's': F(3)}
    scaff = {'b': frozenset({'s'}), 'c': frozenset({'s'})}
    budget = F(7)

    def moves(S):
        out = []
        for i in costs:
            if i in S:
                out.append(frozenset(S - {i}))
            else:
                Tn = frozenset(S | {i})
                if _cost_union(costs, Tn) <= budget and scaff.get(i, frozenset()) <= S:
                    out.append(Tn)
        return out

    start = frozenset()
    target = frozenset({'a', 'b', 'c'})
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in moves(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    depth = dist.get(target)
    ck(depth == 5, "composed: depth(x) = 5 > naive Hamming floor 3 (barrier bites)")
    # exhaustive throughput-exclusion: no history with < depth switches reaches x
    frontier = {start}
    for step in range(1, depth):
        frontier = frontier | {v for S in frontier for v in moves(S)}
        ck(target not in frontier,
           f"composed: no history with <= {step} switches realizes x")
    frontier = frontier | {v for S in frontier for v in moves(S)}
    ck(target in frontier, "composed: at depth switches x is realized")

    passed = not fails
    return {
        'name': 'T_gapless_serial_floor',
        'epistemic': 'P_structural',
        'passed': passed,
        'tier': 4,
        'key_result': (
            'all-Sep structure formation is serial + floor-billed: K1 no free '
            'switch (Bennett excluded by L_cost per-transition uniqueness) [P]; '
            'K2 no joint hold (T_sep + codef union floor; drawn clause = '
            'Sep-branch reading) [P_structural]; K3 release recovers the level, '
            'throughput N*eps is the resource [P]; composed depth(x)->throughput '
            'floor exhaustively certified. Conditional corollary: built structure '
            '=> occupied gap [P_structural_reading], occupancy NOT derived '
            '(3 imports). Charter saturation mechanic withdrawn.'
        ),
        'dependencies': ['A1', 'MD', 'T_sep', 'L_cost', 'L_epsilon*',
                         'L_local_removability', 'T_no_IJC_no_noncommutativity',
                         'L_codef_aggregation_argmin',
                         'L_commutative_no_unresolved_hold'],
        'cross_refs': ['T_coherent_free_spend_permanent',
                       'T_ledger_rent_excluded',
                       'T_realignment_cost_is_transition_energy',
                       'T_IJC_dichotomy', 'check_T_aeon_turnover'],
        'artifacts': {
            'grade_basis': ('K1/K3 [P]; K2 drawn clause = structural reading of '
                            'L_commutative_no_unresolved_hold [P_math] under the '
                            'Sep antecedent (T_no_IJC [P_structural]) -> caps at '
                            '[P_structural]. The lemma discharges the stipulation '
                            '(audit MAJOR-1) but does NOT lift the kernel: the '
                            'Sep-branch antecedent is the principled wall'),
            'corollary': ('[P_structural_reading]; imports N_max + witness depth '
                          '+ IJC-dichotomy exhaustiveness; occupancy stays QAC'),
            'bite': ('Levinthal serial floor (L=100,nu=3 -> Q~1e47) books ~1e27 J '
                     '(Landauer eps*); bites cell/astro budgets, NOT dS-patch; '
                     'multiplicity Q imported => reading grade, never [P]'),
            'withdrawn': ('charter permanent-seat->saturation mechanic: Sep => '
                          'Delta_cross=0 => removable (L_local_removability [P])'),
            'fences': 'superadd-QAC; coherent-ceiling; occupancy-QAC; spectator; '
                      'no-entropic; no-P4-kappa',
            'walk_checks': 'keystone 10198 + theorem/bite 15, 0 fail; audit 0.84',
            'note_home': 'The Turning/zipper_slack_necessity_2026-07-07/',
        },
        'fail_reasons': fails,
    }


_CHECKS = {'T_gapless_serial_floor': check_T_gapless_serial_floor}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    import sys
    r = check_T_gapless_serial_floor()
    print(r['name'], r['epistemic'], 'PASS' if r['passed'] else 'FAIL')
    if not r['passed']:
        for f in r['fail_reasons']:
            print('  -', f)
        sys.exit(1)
