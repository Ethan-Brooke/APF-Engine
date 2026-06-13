"""apf/interface_engine_close_primitives.py -- Interface-Engine-family primitives
distilled from the sin^2theta_W = 3/13 close (2026-06-12).

The close produced five reusable pieces of ENGINE machinery, not just a physics
result. Each is encoded here as an executable [P_structural] primitive and tagged
with the Interface-Engine-family component it feeds. None adds physical content;
each is structural plumbing the engine family can consume.

  1. check_T_ie_codomain_obstruction_discriminator
       -> Codomain Selection engine + the `codomain_mismatch` obstruction channel.
       FD1 structural completeness as the discriminator between a REAL codomain
       obstruction (the codomain values differ empirically -> at most one physical,
       read off structure) and a FREE convention (no empirical difference ->
       units/chart/gauge, not an obstruction).

  2. check_T_ie_schur_placement_primitive
       -> Representation Descent engine.
       Decide which representation/factor constitutively OWNS a quantity by the
       dimension of its invariant algebra (Schur): attach to the factor with the
       minimal -- most constrained, canonical -- commutant. The 3/13 close placed
       the Higgs record on SU(2) this way (commutant dim 1) over U(1) (dim 4).

  3. check_T_ie_claim_kind_taxonomy
       -> claim compiler dispatcher + obligation-packet meta-schema.
       The five-kind ontology the loads-table retirement produced -- foundational
       restatement / derived theorem / adopted bridge premise / empirical input /
       adopted-with-falsifier -- as the `kind` ontology for claim classification.

  4. check_T_ie_rerun_gate_audit_template
       -> the engine's rerun gate (claim -> ... -> global-P export or named
       obstruction). The row-consumption / no-smuggling checklist as a gate:
       dependency-named-not-silent AND grade-scoped AND count-honest, then
       no-smuggling -> CLEAN else REDUCES; any of the firsts failing -> BLOCKED.

  5. check_T_ie_activation_toggle_primitive
       -> the gate's activation test (the earned-keep ruling).
       read/feed/toggle: an input ACTIVATES a billed quantity iff toggling it
       moves the output. The 3/13 placement activates (toggling SU(2)->U(1) moves
       3/13 -> 13/19); an inert invocation does not.

All checks are bank-registered [P_structural], tier 4. Source-of-record: the
sin^2theta_W close (Reference - The sin2thetaW Close - FD1 Structural Completeness
(2026-06-12).md; bank v24.3.247). Engine-family architecture: Paper 8 Supplement
S F.8 + 'Reference - APF Interface Engine Family Architecture (2026-05-19)'.
"""

from __future__ import annotations
from collections import Counter


# =====================================================================
# Claim-kind taxonomy (primitive 3) -- module-level so other engine
# components can import the ontology.
# =====================================================================

KIND_FOUNDATIONAL_RESTATEMENT = 'foundational_restatement'
KIND_DERIVED_THEOREM = 'derived_theorem'
KIND_ADOPTED_BRIDGE_PREMISE = 'adopted_bridge_premise'
KIND_EMPIRICAL_INPUT = 'empirical_input'
KIND_ADOPTED_WITH_FALSIFIER = 'adopted_with_falsifier'

CLAIM_KINDS = frozenset({
    KIND_FOUNDATIONAL_RESTATEMENT, KIND_DERIVED_THEOREM,
    KIND_ADOPTED_BRIDGE_PREMISE, KIND_EMPIRICAL_INPUT,
    KIND_ADOPTED_WITH_FALSIFIER,
})


# =====================================================================
# Small exact/numeric helpers for the Schur placement primitive
# =====================================================================

def _complex_rank(rows, tol=1e-9):
    """Rank of a complex matrix by Gaussian elimination with partial pivoting."""
    rows = [list(r) for r in rows]
    n = len(rows)
    m = len(rows[0]) if rows else 0
    rank = 0
    r = 0
    for c in range(m):
        piv = None
        best = tol
        for i in range(r, n):
            if abs(rows[i][c]) > best:
                best = abs(rows[i][c])
                piv = i
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for i in range(n):
            if i != r and abs(rows[i][c]) > tol:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
        rank += 1
        if r == n:
            break
    return rank


def _matmul2(A, B):
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
    ]


def commutant_dimension(generators):
    """dim_C { M in M_2(C) : [M, G] = 0 for every G in generators }.

    The reusable Representation-Descent primitive: the invariant-algebra
    dimension of a 2-dim representation under the given generators. Schur =>
    an irreducible action has commutant dimension 1 (scalars only); a generator
    proportional to the identity has commutant dimension 4 (all of M_2(C)).
    """
    basis = [
        [[1, 0], [0, 0]], [[0, 1], [0, 0]],
        [[0, 0], [1, 0]], [[0, 0], [0, 1]],
    ]
    # Column k = the flattened commutator [basis_k, G] stacked over all G.
    cols = []
    for Mb in basis:
        col = []
        for G in generators:
            cm = _matmul2(Mb, G)
            mc = _matmul2(G, Mb)
            col += [cm[i][j] - mc[i][j] for i in range(2) for j in range(2)]
        cols.append(col)
    nrows = len(cols[0]) if cols and cols[0] else 0
    A = [[cols[k][rr] for k in range(4)] for rr in range(nrows)]
    return 4 - _complex_rank(A)


# =====================================================================
# Engine helpers (primitives 1, 4, 5)
# =====================================================================

def codomain_obstruction_verdict(codomain_values):
    """Primitive 1. Given a quantity's values across candidate codomains, classify
    the mismatch under FD1 structural completeness: distinct empirical signatures =>
    'real_obstruction' (read off structure, not assignable by fiat); identical =>
    'free_convention' (units/chart/gauge)."""
    return 'real_obstruction' if len(set(codomain_values)) > 1 else 'free_convention'


def rerun_gate_verdict(dependency_named, grade_scoped, count_honest, no_smuggling):
    """Primitive 4. The row-consumption / no-smuggling rerun gate."""
    if not (dependency_named and grade_scoped and count_honest):
        return 'BLOCKED'
    return 'CLEAN' if no_smuggling else 'REDUCES'


def activates(output_fn, base_choice, toggled_choice):
    """Primitive 5. read/feed/toggle: an input activates a billed quantity iff
    toggling it moves the output."""
    return output_fn(base_choice) != output_fn(toggled_choice)


# =====================================================================
# Bank-registered checks
# =====================================================================

def check_T_ie_codomain_obstruction_discriminator():
    """Primitive 1 -> Codomain Selection engine + the codomain_mismatch channel."""
    # the sin^2theta_W three-billing case: distinct measured signatures
    assert codomain_obstruction_verdict([(3, 13), (13, 19), (13, 35)]) == 'real_obstruction'
    # a gauge relabel that changes no measured signature
    assert codomain_obstruction_verdict([(3, 13), (3, 13)]) == 'free_convention'
    # a single codomain is trivially convention-free of mismatch
    assert codomain_obstruction_verdict([(3, 13)]) == 'free_convention'
    return {
        'name': 'T_ie_codomain_obstruction_discriminator',
        'passed': True,
        'status': 'PASS',
        'tier': 4,
        'epistemic': '[P_structural]',
        'engine_component': 'Codomain Selection engine; codomain_mismatch obstruction channel',
        'key_result': (
            'FD1 structural completeness as the codomain-mismatch discriminator: '
            'empirically-distinct codomain values are a REAL obstruction (read off '
            'structure); empirically-identical relabelings are a FREE convention.'
        ),
        'summary': (
            'Reusable engine discriminator distilled from the sin^2theta_W close: a '
            'codomain mismatch that makes an empirical difference must be resolved by '
            'structure (not assigned by fiat); one that makes none is a coordinative '
            'convention and is not an obstruction.'
        ),
        'dependencies': ['FD1_structural_completeness'],
    }


def check_T_ie_schur_placement_primitive():
    """Primitive 2 -> Representation Descent engine."""
    # Pauli generators / 2 (irreducible doublet action of su(2))
    sx = [[0, 0.5], [0.5, 0]]
    sy = [[0, -0.5j], [0.5j, 0]]
    sz = [[0.5, 0], [0, -0.5]]
    dim_su2 = commutant_dimension([sx, sy, sz])
    # U(1)_Y on the doublet acts proportional to the identity
    yid = [[0.5, 0], [0, 0.5]]
    dim_u1 = commutant_dimension([yid])
    assert dim_su2 == 1, f'Schur: su(2) commutant dim should be 1, got {dim_su2}'
    assert dim_u1 == 4, f'U(1) commutant dim should be 4, got {dim_u1}'
    # placement: the canonical owner is the factor with the MINIMAL (most
    # constrained) commutant -- the Higgs modulus is constitutively SU(2)'s
    owner = 'su2' if dim_su2 < dim_u1 else 'u1'
    assert owner == 'su2'
    return {
        'name': 'T_ie_schur_placement_primitive',
        'passed': True,
        'status': 'PASS',
        'tier': 4,
        'epistemic': '[P_structural]',
        'engine_component': 'Representation Descent engine',
        'key_result': (
            f'Invariant-algebra placement: su(2) commutant dim {dim_su2} (Schur, '
            f'irreducible) < U(1) commutant dim {dim_u1} (proportional to identity) '
            f'-> the quantity is constitutively SU(2)-owned.'
        ),
        'summary': (
            'Reusable representation-descent primitive: attach a quantity to the '
            'representation whose invariant algebra constitutively contains it -- the '
            'factor with the minimal commutant dimension. The sin^2theta_W close used '
            'exactly this to place the radial-Higgs record on SU(2).'
        ),
        'dependencies': ['T_ew_load_placement_P'],
    }


def check_T_ie_claim_kind_taxonomy():
    """Primitive 3 -> claim compiler + obligation-packet meta-schema."""
    # the items the Paper 0 v6.2.32 loads-table retirement classified by kind
    classified = {
        'cost_positivity': KIND_FOUNDATIONAL_RESTATEMENT,        # = FD3 / MD
        'threat_class_structure': KIND_FOUNDATIONAL_RESTATEMENT,  # = FD5b
        'sep_ijc_dichotomy': KIND_DERIVED_THEOREM,                # Paper 1 representation theorem
        'inseparable_ijc_bridge': KIND_ADOPTED_BRIDGE_PREMISE,    # the one genuine premise
        'bell_kochen_specker': KIND_EMPIRICAL_INPUT,              # experimental record
    }
    assert set(classified.values()) <= CLAIM_KINDS
    c = Counter(classified.values())
    # exactly one genuine adopted premise; exactly one empirical input
    assert c[KIND_ADOPTED_BRIDGE_PREMISE] == 1
    assert c[KIND_EMPIRICAL_INPUT] == 1
    # the rest trace to foundation (restatements) or are derived theorems
    assert c[KIND_FOUNDATIONAL_RESTATEMENT] == 2
    assert c[KIND_DERIVED_THEOREM] == 1
    assert len(CLAIM_KINDS) == 5
    return {
        'name': 'T_ie_claim_kind_taxonomy',
        'passed': True,
        'status': 'PASS',
        'tier': 4,
        'epistemic': '[P_structural]',
        'engine_component': 'claim compiler dispatcher; obligation_packet_meta_schema (kind field)',
        'key_result': (
            'Five-kind claim ontology (foundational-restatement / derived-theorem / '
            'adopted-bridge-premise / empirical-input / adopted-with-falsifier); the '
            'ex-loads-table items classify as 2 restatements + 1 theorem + 1 premise + '
            '1 empirical input.'
        ),
        'summary': (
            'Reusable claim-classification ontology distilled from the loads-table '
            'retirement: a dependency list must be typed by kind, not tabulated as if '
            'uniform adopted assumptions.'
        ),
        'dependencies': [],
    }


def check_T_ie_rerun_gate_audit_template():
    """Primitive 4 -> the engine rerun gate."""
    # the 3/13 close run through the gate: deps named, grade scoped to the ledger
    # share, count honest, one corroboration-not-input correction -> REDUCES
    assert rerun_gate_verdict(True, True, True, False) == 'REDUCES'
    # a fully clean promotion
    assert rerun_gate_verdict(True, True, True, True) == 'CLEAN'
    # a silent dependency, a grade over-reach, or a dishonest count -> BLOCKED
    assert rerun_gate_verdict(False, True, True, True) == 'BLOCKED'
    assert rerun_gate_verdict(True, False, True, True) == 'BLOCKED'
    assert rerun_gate_verdict(True, True, False, True) == 'BLOCKED'
    return {
        'name': 'T_ie_rerun_gate_audit_template',
        'passed': True,
        'status': 'PASS',
        'tier': 4,
        'epistemic': '[P_structural]',
        'engine_component': 'rerun gate (claim -> ... -> global-P export or named obstruction)',
        'key_result': (
            'Row-consumption / no-smuggling checklist as a gate: dependency-named AND '
            'grade-scoped AND count-honest, then no-smuggling -> CLEAN else REDUCES; '
            'any precondition failing -> BLOCKED.'
        ),
        'summary': (
            'Reusable rerun-gate template: the audit that verified the sin^2theta_W [P] '
            'flip (verdict REDUCES) encoded as the engine promotion gate.'
        ),
        'dependencies': [],
    }


def check_T_ie_activation_toggle_primitive():
    """Primitive 5 -> the gate's activation test."""
    ledger = {'su2': (3, 13), 'u1': (13, 19), 'inert': (13, 35)}
    out = lambda choice: ledger[choice]
    # toggling the placement moves the billed output -> ACTIVATES
    assert activates(out, 'su2', 'u1') is True
    assert activates(out, 'su2', 'inert') is True
    # an inert invocation that does not move the output -> NOT an activation
    assert activates(out, 'su2', 'su2') is False
    return {
        'name': 'T_ie_activation_toggle_primitive',
        'passed': True,
        'status': 'PASS',
        'tier': 4,
        'epistemic': '[P_structural]',
        'engine_component': "the gate's activation test (earned-keep ruling)",
        'key_result': (
            'read/feed/toggle: a choice activates a billed quantity iff toggling it '
            'moves the output. The sin^2theta_W placement activates (SU(2)->U(1) moves '
            '3/13 -> 13/19); an inert invocation does not.'
        ),
        'summary': (
            'Reusable counterfactual verification primitive: the toggle test that '
            'certified the 3/13 placement is load-bearing, as the engine activation gate.'
        ),
        'dependencies': [],
    }


# =====================================================================
# Bank registration
# =====================================================================

_CHECKS = {
    'T_ie_codomain_obstruction_discriminator': check_T_ie_codomain_obstruction_discriminator,
    'T_ie_schur_placement_primitive': check_T_ie_schur_placement_primitive,
    'T_ie_claim_kind_taxonomy': check_T_ie_claim_kind_taxonomy,
    'T_ie_rerun_gate_audit_template': check_T_ie_rerun_gate_audit_template,
    'T_ie_activation_toggle_primitive': check_T_ie_activation_toggle_primitive,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    for n, fn in _CHECKS.items():
        r = fn()
        print(f"[{'PASS' if r.get('passed') else 'FAIL'}] {n} [{r.get('epistemic')}] -> {r.get('engine_component')}")
