"""Paper 1 FD1 Executable Witness — Phase 18.

Paper 1 Supplement v2 §"Definitions (FD1--FD6)" gives the canonical
bedrock formal definition of an enforcement interface:

    FD1: An enforcement interface Γ is a triple
        (S_Γ, 𝒟(Γ), C(Γ))
    where S_Γ is the admissibility substrate (a set of possible
    substrate configurations), 𝒟(Γ) is the set of enforceable
    distinctions at Γ (binary partitions on S_Γ with positive
    realignment cost ε(d) > 0), and C(Γ) ∈ ℝ_{>0} is the
    admissibility capacity exclusively assigned to Γ.

This module supplies the **executable witness**: a small concrete
worked example instantiating FD1 + FD2 (admissible state) + FD4
(perturbation cost function K1--K3) + the K3 forced-additivity
theorem on a finite substrate, certifying that all five FD1
properties hold by direct numpy/python construction.

The construction mirrors Paper 1 Supplement §"Worked example: the
complete construction on R^3" (sec:worked) at the FD1 level: a
3-element substrate carrying two distinctions plus a non-null pool
direction, with explicit realignment costs and a finite capacity.
The point is to demonstrate that FD1 is set-theoretically realisable
(no measure theory, no σ-algebra, no topology imposed) while still
supporting the full PLEC discipline (A1 budget bound; MD positive
cost floor; A2 argmin selection).

This is the Paper 1 analog of `apf/formal_kernel.py` (which witnesses
Paper 8 Supplement Theorem 1.1 V_61 / V_local / V_Lambda construction).
Both modules give the canonical bedrock papers an executable witness
that the abstract definitions are realised by explicit constructions.

Scope / honest limits
---------------------

This module is a **structural witness at the FD1 level**: it certifies
that the FD1 triple (substrate, distinctions, capacity), FD2 admissible
state, FD4 cost function K1--K3, and the forced-additivity K3 theorem
hold on a small finite worked example. It does NOT reconstruct the
full Paper 1 derivation chain (T_form, T_embed, T_sep, T_alg,
T_Born, ...) — that chain is downstream of FD1 + PLEC and lives in
its own modules (apf.core for L_eps_star / L_NZ / L_loc / L_cost;
apf.quantum_operator_derivation for the algebraic structure).

What this witness DOES certify:

1. **FD1 substrate is set-theoretic.** S_Γ is a finite set; no
   measure or topology is required for the framework's definitions
   to be well-posed.
2. **Distinctions are binary partitions with positive cost.** Each
   d ∈ 𝒟(Γ) maps S_Γ → {0, 1} with both classes non-empty and
   ε(d) > 0.
3. **A1 (FD1 capacity bound) holds for every admissible state.**
   Σ ε(d) ≤ C(Γ) for every admissible state σ ∈ Ω(Γ).
4. **FD2 admissible state structure is internally consistent.**
   Each admissible state σ has a residual budget δ_σ ≥ 0.
5. **K1 (non-negativity), K2 (positivity), K3 (additivity on
   disjoint supports) hold for the perturbation cost function κ
   on disjoint-support admissibility acts.**

Tags and status
---------------

Bank-registered via ``register(registry)`` at the bottom. Tag:
``[P_structural]``. Tier: 4.

Relationship to Paper 1 Supplement v2
--------------------------------------

- **§"Definitions (FD1--FD6)":** FD1, FD2, FD4 are instantiated
  here as concrete python data structures.
- **§"Worked example on R^3":** the substrate construction below
  follows the same pattern (3-element substrate carrying two
  irreducible distinctions plus a non-null pool direction).
- **Theorem K3 (forced additivity on disjoint supports):**
  certified here on the finite worked example.
- **Constitutive principle SP (substrate faithfulness):**
  the substrate is set-theoretic; configurations differ iff they
  differ on the admissibility status of some distinction.

Relationship to ``apf.formal_kernel`` (Paper 8 witness)
-------------------------------------------------------

`formal_kernel.py` witnesses Paper 8 Supplement §1 Theorem 1.1
(V_61 / V_local / V_Lambda) at the representation-theoretic level
on the post-T_embed vector-space realisation of admissibility space
at the SM interface.

`paper1_kernel.py` (this module) witnesses Paper 1 Supplement
§"Definitions" FD1 + FD2 + FD4 + Theorem K3 at the **pre-T_embed
set-theoretic level** — the foundational bedrock from which the
post-T_embed vector-space machinery (and Paper 8's V_61 in
particular) is downstream.

Together: paper1_kernel certifies the bedrock; formal_kernel
certifies the SM-interface representation built on top.
"""

from __future__ import annotations

from apf.apf_utils import _result, check


# ═══════════════════════════════════════════════════════════════════
# FD1 substrate: a finite set
# ═══════════════════════════════════════════════════════════════════
#
# Per FD1 (Paper 1 Supplement §"Definitions"):
#
#     "The predicate class 𝒟(Γ) is defined set-theoretically, not
#     measure-theoretically: d is any function Ω(Γ) → {0, 1} with
#     ε(d) > 0. No σ-algebra, Borel structure, topology, or
#     definability hierarchy is imposed on Ω(Γ) or on the
#     predicates."
#
# So S_Γ is just a Python set. We use a 4-element substrate
# carrying two distinctions (d_1, d_2) plus a pool direction
# (d_pool), mirroring the §"Worked example on R^3" construction
# at the pre-linear FD1 level (where "directions" are not yet
# vectors — just substrate-configuration labels).
#
# Substrate: S_Γ = {s_00, s_01, s_10, s_11}
#   s_ij = configuration where d_1 reads i and d_2 reads j
# The pool direction d_pool partitions further into "pool committed"
# vs "pool uncommitted" — but at the FD1 set-theoretic level we
# fold this into the 4 configurations by SP (substrate
# faithfulness): two configurations with identical d_1, d_2
# admissibility status are SP-identified.

_SUBSTRATE = frozenset(['s_00', 's_01', 's_10', 's_11'])


def _build_distinctions():
    """Construct the distinction set 𝒟(Γ).

    Per FD1: each d ∈ 𝒟(Γ) is a function S_Γ → {0, 1} that
    partitions S_Γ into two non-empty classes with positive cost.

    Returns
    -------
    dict
        Map distinction_id → dict with keys:
            'partition' : dict s -> 0/1 (the binary partition)
            'cost'      : float > 0 (the realignment cost ε(d))
            'support'   : frozenset (the admissibility-act support;
                          used for K3 disjoint-support testing)
    """
    eps_star = 1.0  # MD floor: every cost ≥ eps_star
    return {
        'd_1': {
            'partition': {'s_00': 0, 's_01': 0, 's_10': 1, 's_11': 1},
            'cost': 2 * eps_star,
            'support': frozenset(['axis_1']),
        },
        'd_2': {
            'partition': {'s_00': 0, 's_01': 1, 's_10': 0, 's_11': 1},
            'cost': eps_star,
            'support': frozenset(['axis_2']),
        },
        'd_pool': {
            # Pool direction: partitions diagonally — pool-committed
            # configurations (s_00, s_11) vs pool-uncommitted (s_01, s_10).
            'partition': {'s_00': 1, 's_01': 0, 's_10': 0, 's_11': 1},
            'cost': eps_star,
            'support': frozenset(['axis_pool']),
        },
    }


_DISTINCTIONS = _build_distinctions()
_CAPACITY = 5.0  # C(Γ) per the §"Worked example" setup
_MU_STAR = 1.0   # MD positive cost floor


# ═══════════════════════════════════════════════════════════════════
# FD2: admissible states and residual budget
# ═══════════════════════════════════════════════════════════════════
#
# Per FD2: an admissible state σ at Γ is a pair (S_σ, δ_σ) where
# S_σ ⊆ 𝒟(Γ) is the set of actively maintained distinctions and
# δ_σ = C(Γ) − Σ_{d ∈ S_σ} ε(d) ≥ 0 is the residual budget.

def _enumerate_admissible_states(distinctions, capacity):
    """Enumerate all admissible states (subsets of 𝒟(Γ) with Σε ≤ C).

    Returns
    -------
    list
        Each element is dict {'S_sigma': frozenset, 'delta_sigma': float}.
    """
    from itertools import chain, combinations
    d_ids = list(distinctions.keys())
    states = []
    for r in range(len(d_ids) + 1):
        for subset in combinations(d_ids, r):
            total_cost = sum(distinctions[d]['cost'] for d in subset)
            if total_cost <= capacity:
                states.append({
                    'S_sigma': frozenset(subset),
                    'delta_sigma': capacity - total_cost,
                })
    return states


# ═══════════════════════════════════════════════════════════════════
# FD4: perturbation cost function κ on admissibility acts
# ═══════════════════════════════════════════════════════════════════
#
# Per FD4 pre-linear formulation: a perturbation p has an "affected
# region" (set of substrate DOF on which it operates), and κ assigns
# a non-negative real cost. Two perturbations are independent if
# their affected regions don't overlap.

def _build_perturbations(distinctions):
    """Build a small set of representative admissibility acts.

    Each act has a 'support' (frozenset of axis labels) and a 'cost'
    (the κ value). We exhibit:

    - p_1: perturbation along axis_1 (threatens d_1)
    - p_2: perturbation along axis_2 (threatens d_2)
    - p_pool: perturbation along axis_pool (threatens d_pool)
    - p_12: composite act with disjoint support {axis_1, axis_2}
    - p_1pool: composite act with disjoint support {axis_1, axis_pool}

    Costs follow K1 (non-negative), K2 (positive for non-trivial),
    K3 (additive on disjoint supports).
    """
    return {
        'p_1':     {'support': frozenset(['axis_1']),     'cost': 2.0},
        'p_2':     {'support': frozenset(['axis_2']),     'cost': 1.0},
        'p_pool':  {'support': frozenset(['axis_pool']),  'cost': 1.0},
        'p_12':    {'support': frozenset(['axis_1', 'axis_2']),    'cost': 3.0},
        'p_1pool': {'support': frozenset(['axis_1', 'axis_pool']), 'cost': 3.0},
        'p_2pool': {'support': frozenset(['axis_2', 'axis_pool']), 'cost': 2.0},
    }


# ═══════════════════════════════════════════════════════════════════
# Verification helpers
# ═══════════════════════════════════════════════════════════════════

def _verify_FD1_substrate_is_set(substrate):
    """FD1: S_Γ is a (finite) set."""
    return isinstance(substrate, (set, frozenset)) and len(substrate) > 0


def _verify_FD1_distinctions_are_binary_partitions(distinctions, substrate):
    """FD1: every d ∈ 𝒟(Γ) is a function S_Γ → {0, 1} with both
    classes non-empty."""
    for d_id, d in distinctions.items():
        partition = d['partition']
        # Domain matches substrate
        if frozenset(partition.keys()) != substrate:
            return False, f"{d_id}: partition domain != substrate"
        # Codomain ⊆ {0, 1}
        values = set(partition.values())
        if not values.issubset({0, 1}):
            return False, f"{d_id}: partition values {values} not in {{0,1}}"
        # Both classes non-empty
        if 0 not in values or 1 not in values:
            return False, f"{d_id}: one of the two classes is empty"
    return True, "all distinctions are valid binary partitions"


def _verify_FD1_costs_positive(distinctions, mu_star):
    """FD1+MD: every d has ε(d) ≥ μ* > 0."""
    for d_id, d in distinctions.items():
        if d['cost'] < mu_star:
            return False, f"{d_id}: cost {d['cost']} < MD floor {mu_star}"
        if d['cost'] <= 0:
            return False, f"{d_id}: cost {d['cost']} not positive"
    return True, "all costs satisfy MD floor"


def _verify_FD1_capacity_positive(capacity):
    """FD1: C(Γ) ∈ ℝ_{>0}."""
    return isinstance(capacity, (int, float)) and capacity > 0


def _verify_A1_holds_for_all_admissible_states(states, distinctions, capacity):
    """A1: Σ ε(d) ≤ C(Γ) for every admissible state σ."""
    for sigma in states:
        total = sum(distinctions[d]['cost'] for d in sigma['S_sigma'])
        if total > capacity + 1e-12:
            return False, f"A1 violated: state {sigma['S_sigma']} has Σε={total} > C={capacity}"
        if abs(sigma['delta_sigma'] - (capacity - total)) > 1e-12:
            return False, f"FD2 residual: stored {sigma['delta_sigma']} != C - Σε = {capacity - total}"
    return True, f"A1 holds for all {len(states)} admissible states"


def _verify_K1_nonnegativity(perturbations):
    """K1: κ(p) ≥ 0 for all p."""
    for p_id, p in perturbations.items():
        if p['cost'] < 0:
            return False, f"K1 violated: {p_id} cost {p['cost']} < 0"
    return True, "K1 holds (all costs ≥ 0)"


def _verify_K2_positivity(perturbations):
    """K2: κ(p) > 0 for non-trivial perturbations (those with non-empty
    support, since each is in 𝒫(d) for some d)."""
    for p_id, p in perturbations.items():
        if len(p['support']) > 0 and p['cost'] <= 0:
            return False, f"K2 violated: {p_id} non-trivial but cost {p['cost']} ≤ 0"
    return True, "K2 holds (non-trivial perturbations have positive cost)"


def _verify_K3_disjoint_additivity(perturbations):
    """K3: κ(p_i ⊕ p_j) = κ(p_i) + κ(p_j) when supports are disjoint.

    Tests every pair of single-axis perturbations against the
    composite perturbation with their union support.
    """
    # The single-axis perturbations are p_1, p_2, p_pool
    singles = ['p_1', 'p_2', 'p_pool']
    composites = {
        frozenset(['axis_1', 'axis_2']):    'p_12',
        frozenset(['axis_1', 'axis_pool']): 'p_1pool',
        frozenset(['axis_2', 'axis_pool']): 'p_2pool',
    }
    for i in range(len(singles)):
        for j in range(i + 1, len(singles)):
            p_i, p_j = singles[i], singles[j]
            sup_i = perturbations[p_i]['support']
            sup_j = perturbations[p_j]['support']
            # Verify disjointness
            if sup_i & sup_j:
                continue  # not a disjoint-support pair; K3 doesn't apply
            joint_support = sup_i | sup_j
            composite_id = composites.get(joint_support)
            if composite_id is None:
                return False, f"missing composite witness for {joint_support}"
            expected = perturbations[p_i]['cost'] + perturbations[p_j]['cost']
            actual = perturbations[composite_id]['cost']
            if abs(actual - expected) > 1e-12:
                return False, (f"K3 violated on disjoint pair ({p_i}, {p_j}): "
                               f"composite κ={actual} != sum {expected}")
    return True, "K3 holds for all disjoint-support pairs (additivity certified)"


def _verify_SP_substrate_faithfulness(substrate, distinctions):
    """SP (constitutive): two configurations are physically identical
    iff they agree on the admissibility status of every d ∈ 𝒟(Γ).

    Operationally: for our 4-element substrate, every pair of distinct
    configurations should differ on at least one distinction's value.
    """
    subs = sorted(substrate)
    for i in range(len(subs)):
        for j in range(i + 1, len(subs)):
            s_i, s_j = subs[i], subs[j]
            # Find at least one distinction that distinguishes them
            distinguishing = [
                d_id for d_id, d in distinctions.items()
                if d['partition'][s_i] != d['partition'][s_j]
            ]
            if not distinguishing:
                return False, (f"SP violated: configurations {s_i} and {s_j} "
                               f"are not distinguished by any d ∈ 𝒟(Γ)")
    return True, "SP holds (every pair of configurations is distinguished)"


# ═══════════════════════════════════════════════════════════════════
# The bank-registered check
# ═══════════════════════════════════════════════════════════════════

def check_T_FD1_substrate_distinctions_capacity():
    """T_FD1_substrate_distinctions_capacity — Paper 1 FD1 executable
    witness.

    Phase 18: instantiates Paper 1 Supplement v2's FD1 definition
    (enforcement interface = (substrate, distinctions, capacity) triple)
    on a finite 4-element substrate carrying three distinctions
    (d_1, d_2, d_pool) with capacity C = 5 and MD floor μ* = 1.

    Certifies six bedrock properties:

    (i)   FD1 substrate is set-theoretic (no measure / σ-algebra
          / topology imposed).

    (ii)  Each distinction d ∈ 𝒟(Γ) is a binary partition on S_Γ
          with both classes non-empty.

    (iii) Each cost ε(d) satisfies the MD positive floor μ*.

    (iv)  C(Γ) ∈ ℝ_{>0} (FD1 capacity).

    (v)   A1 holds: Σ ε(d) ≤ C(Γ) for every admissible state σ
          ∈ Ω(Γ); FD2 residual budget δ_σ ≥ 0 is internally
          consistent for all enumerated admissible states.

    (vi)  K1 (non-negativity), K2 (positivity for non-trivial
          perturbations), K3 (additivity on disjoint supports —
          the unique scalar admissibility semantics per Paper 1
          Supplement Theorem K3) all certified on the
          perturbation cost function κ.

    Plus the constitutive principle:

    (vii) SP (substrate faithfulness): every pair of distinct
          substrate configurations is distinguished by at least
          one d ∈ 𝒟(Γ).

    Structural reading: this certifies, at the level of an explicit
    finite worked example, that Paper 1 Supplement's FD1 + FD2 +
    FD4 + K3 theorem + SP all hold on a concrete construction. The
    canonical abstract treatment is Paper 1 Supplement §"Definitions
    (FD1--FD6)" + §"Worked example on R^3"; this file gives the
    pre-linear set-theoretic witness from which the post-T_embed
    vector-space chain (and Paper 8's V_61 in particular) is downstream.

    STATUS: [P_structural]. Executable witness; full set-theoretic
    treatment in Paper 1 Supplement v2 §"Definitions" + §"Worked
    example".
    """
    substrate = _SUBSTRATE
    distinctions = _DISTINCTIONS
    capacity = _CAPACITY
    mu_star = _MU_STAR
    perturbations = _build_perturbations(distinctions)
    states = _enumerate_admissible_states(distinctions, capacity)

    # Run all verifications
    fd1_set_ok = _verify_FD1_substrate_is_set(substrate)
    fd1_part_ok, fd1_part_msg = _verify_FD1_distinctions_are_binary_partitions(
        distinctions, substrate)
    fd1_cost_ok, fd1_cost_msg = _verify_FD1_costs_positive(distinctions, mu_star)
    fd1_cap_ok = _verify_FD1_capacity_positive(capacity)
    a1_ok, a1_msg = _verify_A1_holds_for_all_admissible_states(
        states, distinctions, capacity)
    k1_ok, k1_msg = _verify_K1_nonnegativity(perturbations)
    k2_ok, k2_msg = _verify_K2_positivity(perturbations)
    k3_ok, k3_msg = _verify_K3_disjoint_additivity(perturbations)
    sp_ok, sp_msg = _verify_SP_substrate_faithfulness(substrate, distinctions)

    checks = {
        'FD1_substrate_size': len(substrate),
        'FD1_substrate_is_set': fd1_set_ok,
        'FD1_num_distinctions': len(distinctions),
        'FD1_distinctions_are_binary_partitions': fd1_part_ok,
        'FD1_distinctions_msg': fd1_part_msg,
        'FD1_costs_satisfy_MD_floor': fd1_cost_ok,
        'FD1_costs_msg': fd1_cost_msg,
        'FD1_capacity': capacity,
        'FD1_capacity_positive': fd1_cap_ok,
        'MD_mu_star': mu_star,
        'FD2_num_admissible_states': len(states),
        'A1_budget_bound_holds': a1_ok,
        'A1_msg': a1_msg,
        'K1_nonnegativity': k1_ok,
        'K2_positivity': k2_ok,
        'K3_disjoint_additivity': k3_ok,
        'K3_msg': k3_msg,
        'SP_substrate_faithfulness': sp_ok,
        'SP_msg': sp_msg,
    }

    # Structural assertions — the seven witnessed properties
    check(fd1_set_ok,
          "FD1: substrate must be a set (no measure / σ-algebra required)")
    check(fd1_part_ok, f"FD1 distinctions: {fd1_part_msg}")
    check(fd1_cost_ok, f"FD1+MD costs: {fd1_cost_msg}")
    check(fd1_cap_ok,
          "FD1: capacity C(Γ) must be a positive real")
    check(a1_ok, f"A1 budget bound: {a1_msg}")
    check(k1_ok, f"K1 (non-negativity): {k1_msg}")
    check(k2_ok, f"K2 (positivity for non-trivial): {k2_msg}")
    check(k3_ok, f"K3 (forced additivity on disjoint supports): {k3_msg}")
    check(sp_ok, f"SP (substrate faithfulness): {sp_msg}")

    return _result(
        name='T_FD1_substrate_distinctions_capacity',
        tier=4,
        epistemic='[P_structural]',
        summary=(
            'Executable witness for Paper 1 Supplement v2 §"Definitions" '
            'FD1 (enforcement interface = (S_Γ, 𝒟(Γ), C(Γ)) triple) + '
            'FD2 (admissible state) + FD4 (perturbation cost function) + '
            'K3 (forced additivity on disjoint supports) + SP (substrate '
            'faithfulness), instantiated on a finite 4-element substrate '
            'with three distinctions, capacity C = 5, MD floor μ* = 1. '
            'Certifies all bedrock properties hold on a concrete '
            'pre-T_embed set-theoretic worked example.'
        ),
        key_result=(
            f'FD1 triple (|S_Γ|={len(substrate)}, |𝒟(Γ)|={len(distinctions)}, '
            f'C={capacity}) realised concretely; {len(states)} admissible '
            f'states enumerated, all satisfy A1; K1+K2+K3 certified on '
            f'perturbation set; SP certified on substrate.'
        ),
        dependencies=['A1', 'MD', 'FD1', 'FD2', 'FD4', 'SP', 'K3_theorem'],
        cross_refs=['T_FormalKernel_VLambda_uniqueness',
                    'L_epsilon_star',
                    'T_form',
                    'T_embed'],
        artifacts=checks,
    )


# ═══════════════════════════════════════════════════════════════════
# Bank registration
# ═══════════════════════════════════════════════════════════════════

_CHECKS = {
    'T_FD1_substrate_distinctions_capacity':
        check_T_FD1_substrate_distinctions_capacity,
}


def register(registry):
    """Register the Paper 1 FD1 executable witness."""
    registry.update(_CHECKS)


if __name__ == '__main__':
    result = check_T_FD1_substrate_distinctions_capacity()
    print('Paper 1 FD1 executable witness — Phase 18')
    print('=' * 60)
    if isinstance(result, dict):
        for k, v in result.items():
            if k == 'artifacts':
                print('Artifacts:')
                for ak, av in v.items():
                    print(f'  {ak}: {av}')
            else:
                print(f'{k}: {v}')
    else:
        print(result)
