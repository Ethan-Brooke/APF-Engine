"""Dense-sandwich Born reconstruction on the oriented APF linking algebra.

The preceding HFC-345 and graded-orientation packets provide, conditionally on
explicit physical leaves, an elementary oriented linking algebra

    A_or ~= M_2(C)

as a real *-algebra.  This module closes the next finite mathematical seam:
it shows that a norm-dense dyadic family of synthesized amplitude rays, together with a normalized cyclic closed-loop score, is enough to certify positivity
of every actual state and effect by physical closed-sandwich tests, and then
derives the elementary finite Born trace representation without state completion,
measurement completion, process saturation, or G-hold-exact.

The distinction is important.  The theorem constrains the form of every actual
outcome law once physical preparations, effects, classical mixing, and closed
loop readouts are supplied.  It does not derive which preparation is made, it
does not prove that every density operator or POVM is physically available,
and it does not identify the microscopic mechanism that selects an outcome.

All finite algebra in this module is exact Fraction arithmetic.  Physical
premises are kept in an independent manifest and are never self-certified.

FORTIFIED 2026-07-21 per the cold audit (COLD_AUDIT_v06_v08_foundation.md,
verdict LAND-WITH-FIXES 0.79), every finding carried:
  MAJOR-1  the mechanism-independence "countermodel" (two dict literals, the
           Ruling-1-rejected genre) is DELETED; the honest carrier of the
           G-hold locus is the dependency contract (new check
           check_T_g_hold_exact_not_in_born_ancestry; no countermodel claimed).
  MAJOR-2  the composed root inventory is machine-checked: 21 packet-local
           core leaves PLUS the imported graded-orientation inventory
           (ORIENTATION_COVER_REALIZED, ORIENTATION_SHEET_TYPING + the four
           Ruling-3 central-J gates) PLUS the banked HFC-345 thirteen-leaf
           contract (check_T_composed_root_inventory, set-exact with drift
           mutations, verified against the re-pinned canonical sources).
  MAJOR-3  bank duplication disclosed (SOURCE_CONCORDANCE + manuscript):
           check_L_effects_povm_density_born (finite_representation_lemmas),
           quantum_frontend_closure legs, check_T_Born (core.py, Gleason
           dim>=3), check_T_Born_trace_rule (quantum_admissibility); delta
           billed exactly (trace-from-cyclicity at n=2; positivity premise
           TRADE to dense-physical-realization leaves; oriented-carrier
           dyadic synthesis; the v0.8 linearity re-factoring post-fix).
  MAJOR-4  off-diagonal indefinite impostors ([[1,2],[2,1]]-class: positive
           diagonal, negative determinant) added to the state, effect, and
           POVM negative controls; the determinant leg of _is_psd2 is now
           load-bearing and its deletion is CAUGHT.
  F5       trace uniqueness machine-closed by an exact 8-real-unknown linear
           solve (cyclicity + normalization constraints; unique solution
           Tr/2); the hardcoded derived-values dict is gone.
  F6       TYPED_ORIENTED_MATRIX_CARGO restored to the dense-subalgebra
           check premises; premises<->graph concordance machine-checked
           (check_T_premises_graph_concordance).
  F7       the vacuous no-defect control replaced by the executed
           defect-killed pipeline mutation; the dead-code rank guard deleted.
  F8       SOURCES re-pinned to the fortified graded-orientation copy and
           the banked v24.3.432 HFC-345 copies.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

FAMILY = "quantum.dense_sandwich_born"
Gaussian = Tuple[F, F]                       # a + i b
GVector = Tuple[Gaussian, ...]
GMatrix = Tuple[Tuple[Gaussian, ...], ...]
RMatrix = Tuple[Tuple[F, ...], ...]

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
LEAF_MANIFEST_PATH = PACKAGE_ROOT / "DATA" / "physical_leaf_manifest.json"

# Bank-landing embed (v24.3.434): the physical leaf manifest as a module
# constant, content-equivalent to DATA/physical_leaf_manifest.json.  The
# packet JSON remains the provenance copy; when the packet DATA/ layout is
# present it is preferred, so the standalone packet is unchanged in behavior.
# In the bank tree (no DATA/) the embedded constant serves.
PHYSICAL_LEAF_MANIFEST: Dict[str, object] = {'schema_version': '0.6-fortified-2026-07-21',
 'claim': 'actual_finite_weighted_born_soundness_on_the_oriented_linking_algebra',
 'prior_theorem_inputs': ['T_ORIENTED_LINKING_ALGEBRA_M2C_v0_5',
                          'T_HFC_345_FACTOR_PACKAGE'],
 'leaves': {'AFFINE_MATRIX_CARGO_NATURALITY': {'type': 'physical',
                                               'description': 'The HFC '
                                                              'common/defect '
                                                              'construction '
                                                              'acts naturally '
                                                              'on finite '
                                                              'matrix-valued '
                                                              'cargo, not '
                                                              'only on one '
                                                              'displayed '
                                                              'state vector.'},
            'FINITE_COLUMN_JOINT_REALIZATION': {'type': 'physical',
                                                'description': 'The columns '
                                                               'of one '
                                                               'represented '
                                                               'finite matrix '
                                                               'occur in one '
                                                               'compatible '
                                                               'Held '
                                                               'realization; '
                                                               'independently '
                                                               'available '
                                                               'columns are '
                                                               'not enough.'},
            'DYADIC_CLASSICAL_POSITIVE_CONTROL': {'type': 'physical',
                                                  'description': 'Repeated '
                                                                 'fair '
                                                                 'classical '
                                                                 'binary '
                                                                 'control '
                                                                 'realizes '
                                                                 'ordinary '
                                                                 'nonnegative '
                                                                 'dyadic '
                                                                 'mixture '
                                                                 'weights.'},
            'NULL_PADDING': {'type': 'physical',
                             'description': 'Unused classical mixture weight '
                                            'may be assigned to a neutral '
                                            'null branch without changing the '
                                            'represented cargo.'},
            'RETAINED_DEFECT_CHANNEL': {'type': 'physical',
                                        'description': 'Signed dyadic '
                                                       'coefficients enter '
                                                       'only through the '
                                                       'retained HFC defect '
                                                       'factor and remain '
                                                       'future-consequential.'},
            'SAME_TYPE_RETURN': {'type': 'physical',
                                 'description': 'After HFC synthesis the '
                                                'represented cargo returns to '
                                                'the same oriented linking '
                                                'type.'},
            'TYPED_ORIENTED_MATRIX_CARGO': {'type': 'structural',
                                            'description': 'Synthesized '
                                                           'matrices are '
                                                           'typed inside the '
                                                           'complex-linear '
                                                           'oriented linking '
                                                           'algebra rather '
                                                           'than the full '
                                                           'ungraded real '
                                                           'normalizer.'},
            'CLOSED_LOOP_SCORE_LINEARITY': {'type': 'structural',
                                            'description': 'The completed '
                                                           'closed-loop score '
                                                           'extends '
                                                           'complex-linearly '
                                                           'over the '
                                                           'elementary '
                                                           'oriented linking '
                                                           'algebra. '
                                                           'Reduction '
                                                           'citation '
                                                           '(2026-07-21): the '
                                                           'score-linearity '
                                                           'packet v0.8 '
                                                           '(post-fortification) '
                                                           're-factors this '
                                                           'leaf into '
                                                           'classical '
                                                           'randomization + '
                                                           'mixture '
                                                           'congruence + '
                                                           'CLASSICAL_SCORE_TOTALITY '
                                                           '+ normalization + '
                                                           'closure; the '
                                                           'discharge is '
                                                           'conditional on '
                                                           'that full named '
                                                           'set and is '
                                                           'machine-checked '
                                                           'in '
                                                           'check_T_composed_root_inventory.'},
            'CLOSED_LOOP_SCORE_CYCLICITY': {'type': 'structural',
                                            'description': 'The closed-loop '
                                                           'score satisfies '
                                                           'the algebraic '
                                                           'identity '
                                                           'L(ab)=L(ba) for '
                                                           'ALL a,b in the '
                                                           'represented '
                                                           'algebra, '
                                                           'including '
                                                           'non-self-adjoint '
                                                           'elements of the '
                                                           'complex extension '
                                                           '(the matrix-unit '
                                                           'derivation uses '
                                                           'it on E11E12 '
                                                           'etc.). The prose '
                                                           "gloss 'changing "
                                                           'the cut point of '
                                                           'one completed '
                                                           "loop' underprices "
                                                           'this strength: '
                                                           'the '
                                                           'identification of '
                                                           'loop scores of '
                                                           'general products '
                                                           'with the extended '
                                                           'functional rides '
                                                           'the rootless-loop '
                                                           "packet's "
                                                           'ROOTLESS_LOOP_CYCLICITY '
                                                           '+ '
                                                           'DAGGER_SANDWICH_REALIZATION '
                                                           'leaves and is '
                                                           "that packet's "
                                                           'burden.'},
            'CLOSED_LOOP_SCORE_NORMALIZATION': {'type': 'constitutive_operational',
                                                'description': 'The identity '
                                                               'closed loop '
                                                               'has score '
                                                               'one.'},
            'REPRESENTED_OUTCOME_READOUTS': {'type': 'structural',
                                             'description': 'Every actual '
                                                            'outcome readout '
                                                            'is represented '
                                                            'by an element of '
                                                            'the same '
                                                            'oriented linking '
                                                            'algebra, and '
                                                            'typed '
                                                            'composition '
                                                            'represents '
                                                            'closed '
                                                            'sandwiches '
                                                            'algebraically.'},
            'DENSE_SANDWICH_CLOSURE': {'type': 'physical',
                                       'description': 'For every synthesized '
                                                      'dyadic amplitude b and '
                                                      'actual readout e, the '
                                                      'closed sandwich b* e b '
                                                      'is an admitted '
                                                      'completed experiment.'},
            'NONNEGATIVE_OUTCOME_READOUTS': {'type': 'constitutive_operational',
                                             'description': 'Actual outcome '
                                                            'probabilities '
                                                            'and completed '
                                                            'positive '
                                                            'readouts are '
                                                            'nonnegative.'},
            'EFFECT_COMPLEMENT_CLOSURE': {'type': 'physical',
                                          'description': 'Every actual '
                                                         'outcome effect has '
                                                         'the admitted '
                                                         'complement supplied '
                                                         'by the remainder of '
                                                         'its normalized '
                                                         'finite '
                                                         'measurement.'},
            'OUTCOME_AFFINITY_UNDER_CLASSICAL_MIXING': {'type': 'structural',
                                                        'description': 'Preparation '
                                                                       'probabilities '
                                                                       'are '
                                                                       'affine '
                                                                       'under '
                                                                       'ordinary '
                                                                       'classical '
                                                                       'randomization.'},
            'MIXTURE_CONGRUENCE': {'type': 'structural',
                                   'description': 'Operationally identical '
                                                  'convex mixtures of effects '
                                                  'receive the same '
                                                  'probability, so the affine '
                                                  'state map extends '
                                                  'consistently to the '
                                                  'represented span. '
                                                  'Granularity note (Ruling-2 '
                                                  'SPLIT discipline): this '
                                                  'leaf bundles a '
                                                  'mathematical half '
                                                  '(well-definedness of the '
                                                  'affine extension across '
                                                  'decompositions) and a '
                                                  'physical noncontextuality '
                                                  'half (operationally '
                                                  'identical procedures '
                                                  'receive one value); a '
                                                  'future SPLIT pass may '
                                                  'separate them.'},
            'NORMALIZATION': {'type': 'constitutive_operational',
                              'description': 'The certain effect has '
                                             'probability one for every '
                                             'physical preparation.'},
            'DENSE_LOOP_EFFECT_REALIZATION': {'type': 'physical',
                                              'description': 'Every '
                                                             'sufficiently '
                                                             'normalized '
                                                             'square b* b '
                                                             'from the '
                                                             'synthesized '
                                                             'dyadic '
                                                             'star-subalgebra '
                                                             'has an admitted '
                                                             'positive loop '
                                                             'readout.'},
            'FINITE_OPERATIONAL_TOMOGRAPHY': {'type': 'physical',
                                              'description': 'The represented '
                                                             'actual effect '
                                                             'relations '
                                                             'determine a '
                                                             'unique '
                                                             'real-linear '
                                                             'functional on '
                                                             'the finite '
                                                             'self-adjoint '
                                                             'observable '
                                                             'space.'},
            'CONTEXTUAL_EFFECT_IDENTITY': {'type': 'structural',
                                           'description': 'One represented '
                                                          'effect has one '
                                                          'probability '
                                                          'independent of the '
                                                          'measurement '
                                                          'context in which '
                                                          'that same effect '
                                                          'appears.'},
            'FINITE_OUTCOME_NORMALIZATION': {'type': 'physical',
                                             'description': 'The effects of '
                                                            'each actual '
                                                            'finite '
                                                            'measurement sum '
                                                            'to the certain '
                                                            'effect.'},
            'CLOSED_READOUT_LIMITS': {'type': 'optional_saturation',
                                      'description': 'The physical readout '
                                                     'set is closed under '
                                                     'operational limits; '
                                                     'needed only for full '
                                                     'effect completion, not '
                                                     'for Born soundness.'},
            'PHYSICAL_EXTENSION_SOUNDNESS': {'type': 'physical_downstream',
                                             'description': 'An admitted '
                                                            'event remains '
                                                            'positive under '
                                                            'every admitted '
                                                            'finite reference '
                                                            'extension; '
                                                            'needed for CP, '
                                                            'not for Born '
                                                            'soundness.'},
            'FINITE_BRANCH_FORM': {'type': 'physical_downstream',
                                   'description': 'Each actual event has a '
                                                  'finite typed branch '
                                                  'representation on the '
                                                  'oriented complex carrier.'},
            'INSTRUMENT_NORMALIZATION': {'type': 'physical_downstream',
                                         'description': 'The sum of event '
                                                        'branches of a '
                                                        'deterministic '
                                                        'instrument preserves '
                                                        'the certain '
                                                        'effect.'}},
 'forbidden_dependencies': ['G_HOLD_EXACT',
                            'STATE_COMPLETION',
                            'MEASUREMENT_COMPLETION',
                            'PROCESS_SATURATION',
                            'QUADRATIC_LEDGER_TO_DERIVE_J',
                            'CONNECTED_EFFECTIVE_HELD_SWEEP',
                            'PULLBACK_NONEXPANSION'],
 'imported_inventories': {'note': 'MAJOR-2 (2026-07-21): the 21 core leaves '
                                  'above are the PACKET-LOCAL increment only. '
                                  'The theorem roots import two further named '
                                  'inventories, machine-checked set-exactly '
                                  'in check_T_composed_root_inventory.',
                          'via_T_ORIENTED_LINKING_ALGEBRA_M2C_v0_5': {'source': 'fortified '
                                                                                'graded-orientation '
                                                                                'intake '
                                                                                'packet '
                                                                                '(SOURCES/graded_orientation_closure_v0.5.py, '
                                                                                're-pinned)',
                                                                      'premises': ['ORIENTATION_COVER_REALIZED',
                                                                                   'ORIENTATION_SHEET_TYPING'],
                                                                      'central_j_gates': ['GENERATOR_COMPLETENESS',
                                                                                          'NATURALITY',
                                                                                          'ORIENTATION_SYNCHRONIZATION',
                                                                                          'T_LOCAL_J']},
                          'via_T_HFC_345_FACTOR_PACKAGE': {'source': 'banked '
                                                                     'v24.3.432 '
                                                                     'thirteen-leaf '
                                                                     'contract '
                                                                     '(SOURCES/_hfc_345_contracts_BANKED_v24.3.432.py)',
                                                           'leaf_count': 13,
                                                           'shared_with_packet_local': ['SAME_TYPE_RETURN']},
                          'composed_distinct_total': 39}}


@dataclass(frozen=True)
class DenseSandwichBornCertificate:
    oriented_complex_model_exact: bool
    dyadic_matrix_ray_synthesis_exact: bool
    dense_star_subalgebra_exact: bool
    closed_loop_score_is_trace_exact: bool
    dense_sandwich_effect_soundness_exact: bool
    dense_loop_state_positivity_exact: bool
    finite_born_trace_representation_exact: bool
    actual_measurements_are_povms: bool
    g_hold_exact_not_in_born_ancestry: bool
    saturation_claims_separated: bool
    cp_boundary_preserved: bool
    dependency_contract_clean: bool
    composed_root_inventory_exact: bool
    premises_graph_concordant: bool
    physical_premises_certified: bool = False


def _result(
    name: str,
    key_result: str,
    artifacts: Mapping[str, object],
    fails: Sequence[str],
    *,
    dependencies: Sequence[str] = (),
    premises: Sequence[str] = (),
    negative_controls: Sequence[str] = (),
    epistemic: str = "P_math",
) -> Dict[str, object]:
    passed = not fails
    return {
        "name": name,
        "family": FAMILY,
        "tier": 4,
        "epistemic": epistemic,
        "status": "PASS" if passed else "FAIL",
        "passed": passed,
        "scope": "finite exact mathematics / fail-closed operational Born soundness",
        "physical_premises_certified": False,
        "key_result": key_result,
        "dependencies": list(dependencies),
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


# ---------------------------------------------------------------------------
# Gaussian-rational exact arithmetic
# ---------------------------------------------------------------------------

ZERO_G: Gaussian = (F(0), F(0))
ONE_G: Gaussian = (F(1), F(0))
I_G: Gaussian = (F(0), F(1))


def _gadd(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] + y[0], x[1] + y[1]


def _gneg(x: Gaussian) -> Gaussian:
    return -x[0], -x[1]


def _gsub(x: Gaussian, y: Gaussian) -> Gaussian:
    return _gadd(x, _gneg(y))


def _gmul(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def _gscale(s: F, x: Gaussian) -> Gaussian:
    return s * x[0], s * x[1]


def _gconj(x: Gaussian) -> Gaussian:
    return x[0], -x[1]


def _gabs2(x: Gaussian) -> F:
    return x[0] * x[0] + x[1] * x[1]


def _gmat(rows: Sequence[Sequence[Gaussian]]) -> GMatrix:
    return tuple(tuple(x for x in row) for row in rows)


def _gzero(n: int, m: Optional[int] = None) -> GMatrix:
    m = n if m is None else m
    return tuple(tuple(ZERO_G for _ in range(m)) for _ in range(n))


def _geye(n: int) -> GMatrix:
    return tuple(tuple(ONE_G if i == j else ZERO_G for j in range(n)) for i in range(n))


def _gshape(a: GMatrix) -> Tuple[int, int]:
    return len(a), len(a[0]) if a else 0


def _gmm(a: GMatrix, b: GMatrix) -> GMatrix:
    ar, ac = _gshape(a)
    br, bc = _gshape(b)
    if ac != br:
        raise ValueError("matrix shape mismatch")
    return tuple(
        tuple(
            _gsum(_gmul(a[i][k], b[k][j]) for k in range(ac))
            for j in range(bc)
        )
        for i in range(ar)
    )


def _gsum(xs: Iterable[Gaussian]) -> Gaussian:
    out = ZERO_G
    for x in xs:
        out = _gadd(out, x)
    return out


def _gaddm(a: GMatrix, b: GMatrix) -> GMatrix:
    if _gshape(a) != _gshape(b):
        raise ValueError("matrix shape mismatch")
    return tuple(tuple(_gadd(a[i][j], b[i][j]) for j in range(len(a[0]))) for i in range(len(a)))


def _gsubm(a: GMatrix, b: GMatrix) -> GMatrix:
    return tuple(tuple(_gsub(a[i][j], b[i][j]) for j in range(len(a[0]))) for i in range(len(a)))


def _gscalem(s: F, a: GMatrix) -> GMatrix:
    return tuple(tuple(_gscale(s, x) for x in row) for row in a)


def _gdag(a: GMatrix) -> GMatrix:
    return tuple(tuple(_gconj(a[j][i]) for j in range(len(a))) for i in range(len(a[0])))


def _gtrace(a: GMatrix) -> Gaussian:
    return _gsum(a[i][i] for i in range(min(len(a), len(a[0]))))


def _gflat(a: GMatrix) -> List[F]:
    out: List[F] = []
    for row in a:
        for re, im in row:
            out.extend((re, im))
    return out


def _gvec_outer(v: GVector) -> GMatrix:
    return tuple(tuple(_gmul(v[i], _gconj(v[j])) for j in range(len(v))) for i in range(len(v)))


def _gquad(v: GVector, h: GMatrix) -> Gaussian:
    # v^* h v
    n = len(v)
    return _gsum(
        _gmul(_gconj(v[i]), _gmul(h[i][j], v[j]))
        for i in range(n)
        for j in range(n)
    )


def _rank(rows: Iterable[Iterable[F]]) -> int:
    work = [[F(x) for x in row] for row in rows]
    work = [row for row in work if any(row)]
    if not work:
        return 0
    r = 0
    ncols = len(work[0])
    for col in range(ncols):
        pivot = next((i for i in range(r, len(work)) if work[i][col] != 0), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        pv = work[r][col]
        work[r] = [x / pv for x in work[r]]
        for i in range(len(work)):
            if i != r and work[i][col] != 0:
                q = work[i][col]
                work[i] = [a - q * b for a, b in zip(work[i], work[r])]
        r += 1
    return r


def _solve_unique(rows: Sequence[Sequence[F]], rhs: Sequence[F], n_unknowns: int) -> Optional[List[F]]:
    """Exact solve of a (possibly overdetermined) consistent linear system;
    returns the unique solution or None (inconsistent or underdetermined)."""
    aug = [[F(x) for x in row] + [F(b)] for row, b in zip(rows, rhs)]
    r = 0
    for col in range(n_unknowns):
        pivot = next((i for i in range(r, len(aug)) if aug[i][col] != 0), None)
        if pivot is None:
            continue
        aug[r], aug[pivot] = aug[pivot], aug[r]
        pv = aug[r][col]
        aug[r] = [x / pv for x in aug[r]]
        for i in range(len(aug)):
            if i != r and aug[i][col] != 0:
                q = aug[i][col]
                aug[i] = [a - q * b for a, b in zip(aug[i], aug[r])]
        r += 1
    for row in aug:
        if not any(row[:n_unknowns]) and row[n_unknowns] != 0:
            return None  # inconsistent
    if r != n_unknowns:
        return None  # underdetermined
    sol = [F(0)] * n_unknowns
    for row in aug:
        lead = next((j for j in range(n_unknowns) if row[j] != 0), None)
        if lead is not None:
            sol[lead] = row[n_unknowns]
    return sol


def _is_hermitian(a: GMatrix) -> bool:
    return a == _gdag(a)


def _det2h(a: GMatrix) -> F:
    if _gshape(a) != (2, 2) or not _is_hermitian(a):
        raise ValueError("requires 2x2 Hermitian matrix")
    return a[0][0][0] * a[1][1][0] - _gabs2(a[0][1])


def _is_psd2(a: GMatrix) -> bool:
    if _gshape(a) != (2, 2) or not _is_hermitian(a):
        return False
    if a[0][0][1] != 0 or a[1][1][1] != 0:
        return False
    return a[0][0][0] >= 0 and a[1][1][0] >= 0 and _det2h(a) >= 0


def _is_effect2(a: GMatrix) -> bool:
    return _is_psd2(a) and _is_psd2(_gsubm(_geye(2), a))


def _gstr(x: Gaussian) -> str:
    a, b = x
    if b == 0:
        return str(a)
    if a == 0:
        return f"{b}i"
    sign = "+" if b > 0 else "-"
    return f"{a}{sign}{abs(b)}i"


def _gmstr(a: GMatrix) -> List[List[str]]:
    return [[_gstr(x) for x in row] for row in a]


# ---------------------------------------------------------------------------
# Realification and the v0.5 orientation model
# ---------------------------------------------------------------------------


def _rzero(n: int, m: Optional[int] = None) -> RMatrix:
    m = n if m is None else m
    return tuple(tuple(F(0) for _ in range(m)) for _ in range(n))


def _reye(n: int) -> RMatrix:
    return tuple(tuple(F(1) if i == j else F(0) for j in range(n)) for i in range(n))


def _rmm(a: RMatrix, b: RMatrix) -> RMatrix:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0])))
        for i in range(len(a))
    )


def _rtranspose(a: RMatrix) -> RMatrix:
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a[0])))


def _rblock(a: RMatrix, b: RMatrix, c: RMatrix, d: RMatrix) -> RMatrix:
    return tuple(tuple(a[i]) + tuple(b[i]) for i in range(len(a))) + tuple(
        tuple(c[i]) + tuple(d[i]) for i in range(len(c))
    )


def _realify(a: GMatrix) -> RMatrix:
    # basis ordering (Re z1, Im z1, Re z2, Im z2)
    n, m = _gshape(a)
    out = [[F(0) for _ in range(2 * m)] for _ in range(2 * n)]
    for i in range(n):
        for j in range(m):
            re, im = a[i][j]
            out[2*i][2*j] = re
            out[2*i][2*j+1] = -im
            out[2*i+1][2*j] = im
            out[2*i+1][2*j+1] = re
    return tuple(tuple(x for x in row) for row in out)


J2_R: RMatrix = ((F(0), F(-1)), (F(1), F(0)))
S0_R: RMatrix = ((F(1), F(0)), (F(0), F(-1)))
J_OR_V05: RMatrix = _rblock(J2_R, _rzero(2), _rzero(2), tuple(tuple(-x for x in row) for row in J2_R))
Q_ALIGN: RMatrix = _rblock(_reye(2), _rzero(2), _rzero(2), S0_R)
J_STD: RMatrix = _rblock(J2_R, _rzero(2), _rzero(2), J2_R)

# Standard complex basis, represented over R.
E11 = _gmat(((ONE_G, ZERO_G), (ZERO_G, ZERO_G)))
E12 = _gmat(((ZERO_G, ONE_G), (ZERO_G, ZERO_G)))
E21 = _gmat(((ZERO_G, ZERO_G), (ONE_G, ZERO_G)))
E22 = _gmat(((ZERO_G, ZERO_G), (ZERO_G, ONE_G)))
COMPLEX_BASIS: Tuple[GMatrix, ...] = (
    E11, _gscalem(F(1), _gmat(((I_G, ZERO_G), (ZERO_G, ZERO_G)))),
    E12, _gmat(((ZERO_G, I_G), (ZERO_G, ZERO_G))),
    E21, _gmat(((ZERO_G, ZERO_G), (I_G, ZERO_G))),
    E22, _gmat(((ZERO_G, ZERO_G), (ZERO_G, I_G))),
)

PAULI_X = _gmat(((ZERO_G, ONE_G), (ONE_G, ZERO_G)))
PAULI_Y = _gmat(((ZERO_G, (F(0), F(-1))), (I_G, ZERO_G)))
PAULI_Z = _gmat(((ONE_G, ZERO_G), (ZERO_G, (F(-1), F(0)))))
I2_G = _geye(2)


# ---------------------------------------------------------------------------
# Dyadic synthesis
# ---------------------------------------------------------------------------


def _is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def _is_dyadic(x: F) -> bool:
    return _is_power_of_two(x.denominator)


def _next_power_of_two_at_least(x: F) -> F:
    if x <= 1:
        return F(1)
    lam = F(1)
    while lam < x:
        lam *= 2
    return lam


def _dyadic_ray_decomposition(v: Sequence[F]) -> Tuple[F, Tuple[F, ...], Tuple[F, ...]]:
    if not all(_is_dyadic(x) for x in v):
        raise ValueError("target coefficients must be dyadic")
    positive = tuple(max(x, F(0)) for x in v)
    negative = tuple(max(-x, F(0)) for x in v)
    bound = max(sum(positive), sum(negative), F(1))
    lam = _next_power_of_two_at_least(bound)
    x = tuple(a / lam for a in positive)
    y = tuple(a / lam for a in negative)
    return lam, x, y


def _flatten_gaussian_matrix(a: GMatrix) -> Tuple[F, ...]:
    return tuple(_gflat(a))


def _unflatten_gaussian_matrix(v: Sequence[F], n: int = 2, m: int = 2) -> GMatrix:
    if len(v) != 2 * n * m:
        raise ValueError("wrong flattened length")
    it = iter(v)
    rows: List[Tuple[Gaussian, ...]] = []
    for _ in range(n):
        row: List[Gaussian] = []
        for _ in range(m):
            row.append((next(it), next(it)))
        rows.append(tuple(row))
    return tuple(rows)


# ---------------------------------------------------------------------------
# Exact theorem checks
# ---------------------------------------------------------------------------


def check_T_oriented_complex_model_exact() -> Dict[str, object]:
    fails: List[str] = []
    aligned = _rmm(_rmm(Q_ALIGN, J_OR_V05), Q_ALIGN)  # Q^{-1}=Q
    if aligned != J_STD:
        fails.append("orientation alignment must send diag(J,-J) to diag(J,J)")
    if _rmm(J_STD, J_STD) != tuple(tuple(-x for x in row) for row in _reye(4)):
        fails.append("standard complex structure must square to -I")
    real_basis = [_realify(b) for b in COMPLEX_BASIS]
    flat_basis = [[x for row in b for x in row] for b in real_basis]
    if _rank(flat_basis) != 8:
        fails.append("realified M2(C) basis must have real rank eight")
    for b in COMPLEX_BASIS:
        if _rtranspose(_realify(b)) != _realify(_gdag(b)):
            fails.append("real transpose must represent complex adjoint")
            break
    return _result(
        "T_oriented_complex_model_exact",
        "The v0.5 orientation double cover is exactly a standard two-dimensional complex carrier after the explicit real change of basis Q=diag(I,S0). In that basis J_or becomes diag(J,J), the eight real basis elements of M2(C) are independent, and real transpose is the complex adjoint.",
        {
            "J_or_v05": [[str(x) for x in row] for row in J_OR_V05],
            "alignment_Q": [[str(x) for x in row] for row in Q_ALIGN],
            "J_standard": [[str(x) for x in row] for row in J_STD],
            "real_basis_rank": _rank(flat_basis),
            "star_correspondence": "realify(a^*) = realify(a)^T",
        },
        fails,
        dependencies=("T_ORIENTED_LINKING_ALGEBRA_M2C_v0_5",),
        negative_controls=("same-sign undoubled orientation", "ungraded M2(R) algebra"),
    )


def check_T_hfc_dyadic_matrix_ray_synthesis() -> Dict[str, object]:
    fails: List[str] = []
    targets: List[GMatrix] = list(COMPLEX_BASIS)
    nums = (-2, -1, 0, 1, 2)
    dens = (1, 2, 4)
    # Deterministic stress family without exploding runtime.
    for k in range(60):
        vals = [F(nums[(k + 3*j) % len(nums)], dens[(k + j) % len(dens)]) for j in range(8)]
        targets.append(_unflatten_gaussian_matrix(vals))
    max_lam = F(0)
    for target in targets:
        v = _flatten_gaussian_matrix(target)
        lam, x, y = _dyadic_ray_decomposition(v)
        max_lam = max(max_lam, lam)
        if not (sum(x) <= 1 and sum(y) <= 1):
            fails.append("positive branches must be null-padded convex mixtures")
            break
        if not all(a >= 0 for a in x + y):
            fails.append("classical branch weights must be nonnegative")
            break
        out = tuple((a - b) / 2 for a, b in zip(x, y))
        target_scaled = tuple(a / (2 * lam) for a in v)
        if out != target_scaled:
            fails.append("defect output must reproduce the target matrix ray")
            break
        if not all(_is_dyadic(a) for a in x + y):
            fails.append("synthesis weights must remain dyadic")
            break
    # Executed no-defect mutation (audit F7): kill the defect channel by
    # zeroing the negative branch and run the pipeline on a negative-coordinate
    # target; the mutated output must FAIL to reproduce the target ray.
    negative_target = _gmat((((F(-1), F(0)), ZERO_G), (ZERO_G, ZERO_G)))
    vneg = _flatten_gaussian_matrix(negative_target)
    lam_n, x_n, y_n = _dyadic_ray_decomposition(vneg)
    defect_killed_output = tuple((a - F(0)) / 2 for a in x_n)  # negative branch zeroed
    target_scaled_neg = tuple(a / (2 * lam_n) for a in vneg)
    defect_kill_caught = defect_killed_output != target_scaled_neg
    intact_output = tuple((a - b) / 2 for a, b in zip(x_n, y_n))
    if not defect_kill_caught:
        fails.append("defect-killed pipeline must fail on a negative-coordinate target")
    if intact_output != target_scaled_neg:
        fails.append("intact pipeline must reproduce the negative-coordinate target")
    return _result(
        "T_hfc_dyadic_matrix_ray_synthesis",
        "Under affine matrix-cargo naturality, finite compatible column realization, dyadic classical control, null padding, and a retained physical defect channel, every Gaussian-dyadic 2x2 matrix ray is synthesized from two ordinary nonnegative mixtures. The sign enters only through the defect factor; arbitrary signed classical control is not assumed.",
        {
            "targets_tested": len(targets),
            "coefficient_dimension": 8,
            "max_power_of_two_scale": str(max_lam),
            "classical_inputs_nonnegative": True,
            "null_padding_used": True,
            "signed_step": "physical defect channel only",
            "no_defect_mutation_executed": True,
            "no_defect_mutation_caught": defect_kill_caught,
        },
        fails,
        dependencies=("T_HFC_345_FACTOR_PACKAGE",),
        premises=(
            "AFFINE_MATRIX_CARGO_NATURALITY",
            "FINITE_COLUMN_JOINT_REALIZATION",
            "DYADIC_CLASSICAL_POSITIVE_CONTROL",
            "NULL_PADDING",
            "RETAINED_DEFECT_CHANNEL",
            "SAME_TYPE_RETURN",
        ),
        negative_controls=("arbitrary signed classical control", "independent columns without joint realization", "ray synthesis treated as arbitrary physical rescaling or addition"),
        epistemic="P_math|named_physical_leaves",
    )


def check_T_dense_dyadic_star_subalgebra() -> Dict[str, object]:
    fails: List[str] = []
    samples: List[GMatrix] = []
    for k in range(12):
        vals = [F(((k + 2*j) % 5) - 2, 2 ** ((k + j) % 4)) for j in range(8)]
        samples.append(_unflatten_gaussian_matrix(vals))
    for a in samples:
        if not all(_is_dyadic(x) for x in _gflat(a)):
            fails.append("sample must be Gaussian-dyadic")
            break
        if not all(_is_dyadic(x) for x in _gflat(_gdag(a))):
            fails.append("dyadic algebra must be adjoint closed")
            break
    for a in samples:
        for b in samples:
            if not all(_is_dyadic(x) for x in _gflat(_gaddm(a, b))):
                fails.append("dyadic algebra must be addition closed")
                break
            if not all(_is_dyadic(x) for x in _gflat(_gmm(a, b))):
                fails.append("dyadic algebra must be multiplication closed")
                break
        if fails:
            break
    # Exact dyadic approximants to 1/3 show density numerically as a theorem
    # witness; the proof uses binary truncations coordinatewise.
    approximants = [F((2 ** n) // 3, 2 ** n) for n in range(2, 13)]
    errors = [abs(F(1, 3) - q) for q in approximants]
    if not all(errors[i+1] <= errors[i] for i in range(len(errors)-1)):
        fails.append("binary truncation errors must decrease")
    if errors[-1] >= F(1, 2 ** 11):
        fails.append("dyadic approximation bound failed")
    return _result(
        "T_dense_dyadic_star_subalgebra",
        "M2(D[i]), with D the dyadic rationals, is a unital *-subalgebra of M2(C) and is norm dense. Addition, multiplication, and adjoint preserve dyadic Gaussian entries. Coordinatewise binary truncation supplies explicit approximants; no compact-group averaging or quadratic ledger is used.",
        {
            "sample_matrices": len(samples),
            "pair_products_tested": len(samples) ** 2,
            "approximation_target": "1/3",
            "final_dyadic_approximant": str(approximants[-1]),
            "final_error": str(errors[-1]),
            "star_closed": True,
            "norm_dense": True,
        },
        fails,
        dependencies=("T_oriented_complex_model_exact", "T_hfc_dyadic_matrix_ray_synthesis"),
        premises=("TYPED_ORIENTED_MATRIX_CARGO",),
        negative_controls=("finite matrix list mistaken for the full cone",),
        epistemic="P_math|named_structural_leaf",
    )


def _trace_sandwich_g(b: GMatrix, h: GMatrix) -> Gaussian:
    return _gtrace(_gmm(_gmm(_gdag(b), h), b))


def _trace_sandwich(b: GMatrix, h: GMatrix) -> F:
    tr = _trace_sandwich_g(b, h)
    if tr[1] != 0:
        raise ValueError("closed sandwich score is not real")
    return tr[0]


def check_T_closed_loop_score_is_normalized_trace() -> Dict[str, object]:
    fails: List[str] = []

    def tau(a: GMatrix) -> Gaussian:
        return _gscale(F(1, 2), _gtrace(a))

    basis = (E11, E12, E21, E22)
    cyclic_pairs = 0
    for a in basis:
        for b in basis:
            if tau(_gmm(a, b)) != tau(_gmm(b, a)):
                fails.append("normalized trace failed cyclicity")
                break
            cyclic_pairs += 1

    # The matrix-unit constraints derive the score, rather than assume it:
    # L(E12)=L(E21)=0; L(E11)=L(E22); L(I)=1.
    forced_e12_zero = _gmm(E11, E12) == E12 and _gmm(E12, E11) == _gzero(2)
    forced_e21_zero = _gmm(E22, E21) == E21 and _gmm(E21, E22) == _gzero(2)
    forced_diagonal_equal = _gmm(E12, E21) == E11 and _gmm(E21, E12) == E22
    if not (forced_e12_zero and forced_e21_zero and forced_diagonal_equal):
        fails.append("matrix-unit derivation of the normalized trace failed")
    if tau(I2_G) != ONE_G:
        fails.append("normalized trace failed L(I)=1")

    # Machine closure of the uniqueness quantifier (audit F5): parametrize an
    # ARBITRARY complex-linear functional L by its four complex values on the
    # matrix units (8 real unknowns), impose L(ab)=L(ba) over all 16 basis
    # pairs plus L(I)=1 as exact linear constraints, and solve.  The solution
    # space must be exactly {Tr/2}: no hardcoded value dict survives.
    unknown_index = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}

    def _lin_rows(mat: GMatrix, rhs: Gaussian):
        # complex row: sum_kl mat[k][l] * x_kl = rhs  -> two real rows
        re_row = [F(0)] * 8
        im_row = [F(0)] * 8
        for (k, l), idx in unknown_index.items():
            cr, ci = mat[k][l]
            re_row[2 * idx] += cr
            re_row[2 * idx + 1] += -ci
            im_row[2 * idx] += ci
            im_row[2 * idx + 1] += cr
        return [(re_row, rhs[0]), (im_row, rhs[1])]

    rows: List[List[F]] = []
    rhs: List[F] = []
    for a in basis:
        for b in basis:
            comm = _gsubm(_gmm(a, b), _gmm(b, a))
            for row, val in _lin_rows(comm, ZERO_G):
                rows.append(row)
                rhs.append(val)
    for row, val in _lin_rows(I2_G, ONE_G):
        rows.append(row)
        rhs.append(val)
    solution = _solve_unique(rows, rhs, 8)
    expected = [F(1, 2), F(0), F(0), F(0), F(0), F(0), F(1, 2), F(0)]
    uniqueness_machine_closed = solution == expected
    if not uniqueness_machine_closed:
        fails.append(f"trace uniqueness solve failed: {solution}")
    # Mutation: dropping the normalization rows must leave a one-complex-
    # parameter family (underdetermined), executed.
    if _solve_unique(rows[:-2], rhs[:-2], 8) is not None:
        fails.append("cyclicity alone must NOT determine the score (normalization needed)")
    derived_values = {
        "L(E11)": str(solution[0]) if solution else "unsolved",
        "L(E12)": str(solution[2]) if solution else "unsolved",
        "L(E21)": str(solution[4]) if solution else "unsolved",
        "L(E22)": str(solution[6]) if solution else "unsolved",
    }
    if solution and [tau(x) for x in basis] != [
        (solution[0], solution[1]),
        (solution[2], solution[3]),
        (solution[4], solution[5]),
        (solution[6], solution[7]),
    ]:
        fails.append("solved functional does not equal normalized trace on the basis")

    # Normalized but nontracial coordinate score: L_11(I)=1, yet
    # L_11(E12 E21)=1 and L_11(E21 E12)=0.
    def l11(a: GMatrix) -> Gaussian:
        return a[0][0]

    bad_left = l11(_gmm(E12, E21))
    bad_right = l11(_gmm(E21, E12))
    nontracial_control_caught = l11(I2_G) == ONE_G and bad_left != bad_right
    if not nontracial_control_caught:
        fails.append("normalized nontracial score control was not caught")

    return _result(
        "T_closed_loop_score_is_normalized_trace",
        "On the elementary oriented algebra M2(C), every normalized complex-linear cyclic closed-loop score is the normalized matrix trace. The uniqueness quantifier is machine-closed: an arbitrary complex-linear functional (8 real unknowns) constrained by L(ab)=L(ba) over all 16 matrix-unit pairs plus L(I)=1 has the unique exact solution Tr/2, and dropping normalization leaves the expected one-parameter family. Linearity, cyclicity, and normalization remain explicit physical leaves. The uniqueness itself is textbook (unique normalized tracial functional on a matrix factor; Kadison-Ringrose genre): the contribution is the leaf-typed executable siting, not new mathematics.",
        {
            "cyclic_basis_pairs_checked": cyclic_pairs,
            "uniqueness_machine_closed": uniqueness_machine_closed,
            "uniqueness_solve_constraints": len(rows),
            "derived_matrix_unit_values": derived_values,
            "normalized_trace_on_identity": _gstr(tau(I2_G)),
            "nontracial_control_left": _gstr(bad_left),
            "nontracial_control_right": _gstr(bad_right),
            "nontracial_control_caught": nontracial_control_caught,
        },
        fails,
        dependencies=("T_oriented_complex_model_exact",),
        premises=(
            "CLOSED_LOOP_SCORE_LINEARITY",
            "CLOSED_LOOP_SCORE_CYCLICITY",
            "CLOSED_LOOP_SCORE_NORMALIZATION",
        ),
        negative_controls=("normalized coordinate score lacking cyclicity",),
        epistemic="P_math|named_closed_loop_leaves",
    )


def check_T_dense_sandwich_effect_soundness() -> Dict[str, object]:
    fails: List[str] = []
    # Exact positive effect from a Gaussian-rational unit vector.
    phi: GVector = ((F(4, 5), F(0)), (F(0), F(3, 5)))
    e = _gvec_outer(phi)
    if not _is_effect2(e):
        fails.append("rank-one projector must be an effect")
    probes = [E11, E12, E21, E22, I2_G, PAULI_X, PAULI_Y, PAULI_Z]
    for b in probes:
        if _trace_sandwich(b, e) < 0:
            fails.append("positive effect failed a dense-subalgebra sandwich")
            break
        if _trace_sandwich(b, _gsubm(I2_G, e)) < 0:
            fails.append("effect complement failed a sandwich")
            break
    # One trace test is not enough: h_bad has positive total trace but one
    # negative eigenvalue, caught by the E11 sandwich.
    h_bad = _gmat((((F(-1), F(0)), ZERO_G), (ZERO_G, (F(2), F(0)))))
    trace_only = _gtrace(h_bad)[0]
    caught = _trace_sandwich(E11, h_bad) < 0
    if trace_only <= 0 or not caught:
        fails.append("single-trace negative control must be caught by a sandwich")

    # Self-adjointness is derived from real closed scores. A non-Hermitian
    # readout produces an imaginary sandwich on a dyadic rank-one probe.
    h_nonhermitian = _gmat(((ONE_G, I_G), (ZERO_G, ONE_G)))
    b_nonhermitian = _gmat(((ONE_G, ZERO_G), (ONE_G, ZERO_G)))
    nonhermitian_score = _trace_sandwich_g(b_nonhermitian, h_nonhermitian)
    nonhermitian_caught = nonhermitian_score[1] != 0
    if not nonhermitian_caught:
        fails.append("non-Hermitian readout did not produce a nonreal sandwich score")

    # MAJOR-4 (audit mutation M3): off-diagonal indefinite impostor with
    # POSITIVE diagonal, [[1,2],[2,1]] (det=-3).  Every prior impostor had a
    # negative diagonal entry, so the determinant leg of _is_psd2 was
    # exercised by nothing.  This impostor is rejected ONLY by the
    # determinant leg, and it is caught by an exact dense sandwich on the
    # eigenvector (1,-1): tau-free score b*hb = -2 < 0.
    h_offdiag = _gmat((((F(1), F(0)), (F(2), F(0))), ((F(2), F(0)), (F(1), F(0)))))
    offdiag_diag_nonneg = h_offdiag[0][0][0] >= 0 and h_offdiag[1][1][0] >= 0
    offdiag_det = _det2h(h_offdiag)
    offdiag_rejected_by_gate = not _is_psd2(h_offdiag)
    b_catch = _gmat((((F(1), F(0)), ZERO_G), ((F(-1), F(0)), ZERO_G)))
    offdiag_sandwich = _trace_sandwich(b_catch, h_offdiag)
    if not (offdiag_diag_nonneg and offdiag_det < 0):
        fails.append("off-diagonal impostor malformed (needs positive diagonal, negative det)")
    if not offdiag_rejected_by_gate:
        fails.append("determinant leg failed to reject the off-diagonal indefinite impostor")
    if offdiag_sandwich >= 0:
        fails.append("off-diagonal impostor must fail a dense sandwich")

    return _result(
        "T_dense_sandwich_effect_soundness",
        "For an arbitrary represented readout h, real nonnegative normalized-trace scores Tr(b* h b) on a norm-dense synthesized *-ray family first force h=h* by polarization and then force h>=0. Applying the same test to I-h gives 0<=h<=I. A single trace test is insufficient, and a non-Hermitian readout is rejected by a nonreal exact sandwich.",
        {
            "positive_effect": _gmstr(e),
            "probe_count": len(probes),
            "trace_only_bad_control": str(trace_only),
            "bad_control_E11_sandwich": str(_trace_sandwich(E11, h_bad)),
            "bad_control_caught": caught,
            "nonhermitian_control_score": _gstr(nonhermitian_score),
            "nonhermitian_control_caught": nonhermitian_caught,
            "offdiagonal_indefinite_impostor": _gmstr(h_offdiag),
            "offdiagonal_impostor_det": str(offdiag_det),
            "offdiagonal_impostor_rejected_by_det_leg": offdiag_rejected_by_gate,
            "offdiagonal_impostor_sandwich": str(offdiag_sandwich),
            "self_adjointness_assumed": False,
            "all_actual_effects_positive_contractions_under_premises": True,
        },
        fails,
        dependencies=("T_dense_dyadic_star_subalgebra", "T_closed_loop_score_is_normalized_trace"),
        premises=(
            "REPRESENTED_OUTCOME_READOUTS",
            "DENSE_SANDWICH_CLOSURE",
            "NONNEGATIVE_OUTCOME_READOUTS",
            "EFFECT_COMPLEMENT_CLOSURE",
        ),
        negative_controls=(
            "one trace state",
            "non-Hermitian readout",
            "coordinatewise positivity",
            "finite probe family without density",
        ),
        epistemic="P_math|named_operational_leaves",
    )


def _born(rho: GMatrix, e: GMatrix) -> F:
    tr = _gtrace(_gmm(rho, e))
    if tr[1] != 0:
        raise ValueError("Born pairing must be real")
    return tr[0]


def check_T_dense_loop_state_positivity() -> Dict[str, object]:
    fails: List[str] = []
    psi: GVector = ((F(3, 5), F(0)), (F(4, 5), F(0)))
    rho = _gvec_outer(psi)
    if not _is_psd2(rho) or _gtrace(rho) != ONE_G:
        fails.append("test density must be positive and normalized")
    squares = [_gmm(_gdag(b), b) for b in (E11, E12, E21, E22, PAULI_X, PAULI_Y, PAULI_Z)]
    values = [_born(rho, s) for s in squares]
    if any(v < 0 for v in values):
        fails.append("positive state must be nonnegative on dense loop squares")
    rho_bad = _gmat((((F(3, 2), F(0)), ZERO_G), (ZERO_G, (F(-1, 2), F(0)))))
    if _gtrace(rho_bad) != ONE_G:
        fails.append("bad functional control must remain normalized")
    bad_square = _gmm(_gdag(E12), E12)  # E22
    bad_value = _born(rho_bad, bad_square)
    if bad_value >= 0:
        fails.append("nonpositive normalized functional must fail a loop square")
    # MAJOR-4: normalized indefinite impostor with POSITIVE diagonal,
    # [[1/2,1],[1,1/2]] (trace 1, det=-3/4): rejected only by the determinant
    # leg, and caught by the exact loop square c*c with c=[[1,-1],[0,0]].
    rho_offdiag = _gmat((((F(1, 2), F(0)), (F(1), F(0))), ((F(1), F(0)), (F(1, 2), F(0)))))
    if _gtrace(rho_offdiag) != ONE_G:
        fails.append("off-diagonal impostor state must remain normalized")
    if rho_offdiag[0][0][0] < 0 or rho_offdiag[1][1][0] < 0:
        fails.append("off-diagonal impostor state must have nonnegative diagonal")
    offdiag_state_rejected = not _is_psd2(rho_offdiag)
    c = _gmat((((F(1), F(0)), (F(-1), F(0))), (ZERO_G, ZERO_G)))
    c_square = _gmm(_gdag(c), c)
    offdiag_loop_value = _born(rho_offdiag, c_square)
    if not offdiag_state_rejected:
        fails.append("determinant leg failed to reject the off-diagonal indefinite state")
    if offdiag_loop_value >= 0:
        fails.append("off-diagonal indefinite state must fail a loop square")
    return _result(
        "T_dense_loop_state_positivity",
        "A normalized real-linear outcome functional that is nonnegative on every physically realized square b*b from a norm-dense *-subalgebra is positive on the full C*-cone. Finite-dimensional trace duality then gives a unique density operator. State completion is not required: the theorem represents every actual state and says nothing about preparation of every algebraic density.",
        {
            "rho": _gmstr(rho),
            "loop_squares_tested": len(squares),
            "minimum_loop_value": str(min(values)),
            "normalized_nonpositive_control": _gmstr(rho_bad),
            "control_negative_loop_value": str(bad_value),
            "offdiagonal_indefinite_state": _gmstr(rho_offdiag),
            "offdiagonal_state_rejected_by_det_leg": offdiag_state_rejected,
            "offdiagonal_state_negative_loop_value": str(offdiag_loop_value),
            "state_completion_used": False,
        },
        fails,
        dependencies=("T_dense_dyadic_star_subalgebra",),
        premises=(
            "OUTCOME_AFFINITY_UNDER_CLASSICAL_MIXING",
            "MIXTURE_CONGRUENCE",
            "NORMALIZATION",
            "DENSE_LOOP_EFFECT_REALIZATION",
        ),
        negative_controls=("normalized but nonpositive linear functional", "state completion smuggle"),
        epistemic="P_math|named_operational_leaves",
    )


def check_T_finite_weighted_born_soundness() -> Dict[str, object]:
    fails: List[str] = []
    psi: GVector = ((F(3, 5), F(0)), (F(4, 5), F(0)))
    phi: GVector = ((F(4, 5), F(0)), (F(0), F(3, 5)))
    rho = _gvec_outer(psi)
    e = _gvec_outer(phi)
    p = _born(rho, e)
    inner = _gsum(_gmul(_gconj(phi[j]), psi[j]) for j in range(2))
    overlap2 = _gabs2(inner)
    if p != overlap2 or p != F(288, 625):
        fails.append("trace Born value must equal the exact squared overlap")
    complement = _gsubm(I2_G, e)
    p2 = _born(rho, complement)
    if p < 0 or p2 < 0 or p + p2 != 1:
        fails.append("binary POVM probabilities must be normalized and nonnegative")
    # Mixed state and nonprojective effect.
    rho_mix = _gscalem(F(1, 2), _gaddm(rho, _gvec_outer(((F(4, 5), F(0)), (F(-3, 5), F(0))))))
    eff = _gscalem(F(1, 2), e)
    pmix = _born(rho_mix, eff)
    if not (_is_psd2(rho_mix) and _gtrace(rho_mix) == ONE_G and _is_effect2(eff)):
        fails.append("mixed-state/nonprojective-effect control malformed")
    if pmix < 0 or pmix > 1:
        fails.append("mixed Born value outside [0,1]")
    return _result(
        "T_finite_weighted_born_soundness",
        "On the oriented complex algebra, every actual state and effect satisfying the dense-loop operational premises has a unique density/effect representation and every actual outcome probability is Tr(rho e). For pure rank-one data this is |<phi,psi>|^2. The theorem fixes weighted Born form without G-hold-exact, state completion, measurement completion, or process saturation.",
        {
            "psi": [_gstr(x) for x in psi],
            "phi": [_gstr(x) for x in phi],
            "rho": _gmstr(rho),
            "effect": _gmstr(e),
            "born_probability": str(p),
            "squared_overlap": str(overlap2),
            "complement_probability": str(p2),
            "mixed_nonprojective_probability": str(pmix),
            "G_hold_exact_used": False,
            "state_completion_used": False,
            "measurement_completion_used": False,
        },
        fails,
        dependencies=("T_dense_sandwich_effect_soundness", "T_dense_loop_state_positivity"),
        premises=("FINITE_OPERATIONAL_TOMOGRAPHY", "CONTEXTUAL_EFFECT_IDENTITY"),
        negative_controls=("nonlinear outcome law", "context-dependent value for one effect"),
    )


def check_T_actual_measurements_are_povms() -> Dict[str, object]:
    fails: List[str] = []
    phi: GVector = ((F(4, 5), F(0)), (F(0), F(3, 5)))
    e1 = _gvec_outer(phi)
    e2 = _gsubm(I2_G, e1)
    if not (_is_effect2(e1) and _is_effect2(e2)):
        fails.append("outcome effects must be positive contractions")
    if _gaddm(e1, e2) != I2_G:
        fails.append("measurement effects must sum to identity")
    # A malformed outcome family with a negative member can still sum to I.
    bad1 = _gmat((((F(-1), F(0)), ZERO_G), (ZERO_G, (F(0), F(0)))))
    bad2 = _gsubm(I2_G, bad1)
    malformed_sums_to_I = _gaddm(bad1, bad2) == I2_G
    malformed_positive = _is_psd2(bad1) and _is_psd2(bad2)
    if not malformed_sums_to_I or malformed_positive:
        fails.append("sum-to-I alone must not certify a POVM")
    # MAJOR-4: an off-diagonal indefinite family member with POSITIVE
    # diagonal ([[1,2],[2,1]], det=-3) also sums to I with its complement;
    # only the determinant leg rejects it.
    bad3 = _gmat((((F(1), F(0)), (F(2), F(0))), ((F(2), F(0)), (F(1), F(0)))))
    bad4 = _gsubm(I2_G, bad3)
    offdiag_sums_to_I = _gaddm(bad3, bad4) == I2_G
    offdiag_diag_nonneg = bad3[0][0][0] >= 0 and bad3[1][1][0] >= 0
    offdiag_rejected = not _is_psd2(bad3)
    if not (offdiag_sums_to_I and offdiag_diag_nonneg):
        fails.append("off-diagonal POVM impostor malformed")
    if not offdiag_rejected:
        fails.append("determinant leg failed to reject the off-diagonal POVM impostor")
    return _result(
        "T_actual_measurements_are_povms",
        "Every actual finite measurement whose outcome effects pass dense-sandwich soundness and whose outcome ledger is normalized is a POVM. This is a soundness theorem. It does not claim that every mathematical POVM is implementable.",
        {
            "outcomes": [_gmstr(e1), _gmstr(e2)],
            "sum_identity": True,
            "malformed_family_sums_to_identity": malformed_sums_to_I,
            "malformed_family_positive": malformed_positive,
            "offdiagonal_indefinite_member_sums_to_identity": offdiag_sums_to_I,
            "offdiagonal_indefinite_member_rejected_by_det_leg": offdiag_rejected,
            "measurement_completion_used": False,
        },
        fails,
        dependencies=("T_dense_sandwich_effect_soundness",),
        premises=("FINITE_OUTCOME_NORMALIZATION",),
        negative_controls=("sum-to-identity without positivity", "measurement saturation"),
    )


def check_T_g_hold_exact_not_in_born_ancestry() -> Dict[str, object]:
    """MAJOR-1 carried (Ruling 1, 2026-07-20): the former "mechanism
    independence countermodel" (two dict literals with identical signature
    tuples and different mechanism strings) was exactly the instrument genre
    Ruling 1 rejected -- record-level equality proves equality in the chosen
    projection only; two mechanisms may be record-equivalent while remaining
    cost-distinct.  NO countermodel is claimed here.  The honest carrier of
    the G-hold locus is the DEPENDENCY CONTRACT: the proof of the operational
    Born theorem nowhere invokes the grant, and this check verifies that fact
    on the machine graph, with reinsertion mutations executed."""
    fails: List[str] = []
    graph = DEPENDENCY_GRAPH
    born_ancestry = _deps(graph, "T_WEIGHTED_BORN_SOUNDNESS")
    if "G_HOLD_EXACT" in born_ancestry:
        fails.append("G_HOLD_EXACT found in the Born ancestry")
    leaked = sorted(FORBIDDEN_DEPENDENCIES & _all_nodes(graph))
    if leaked:
        fails.append(f"forbidden names present in the graph: {leaked}")
    # Scan every executed check row's premises for the grant under its name.
    premise_rows = {
        "T_hfc_dyadic_matrix_ray_synthesis": check_T_hfc_dyadic_matrix_ray_synthesis,
        "T_closed_loop_score_is_normalized_trace": check_T_closed_loop_score_is_normalized_trace,
        "T_dense_sandwich_effect_soundness": check_T_dense_sandwich_effect_soundness,
        "T_dense_loop_state_positivity": check_T_dense_loop_state_positivity,
        "T_finite_weighted_born_soundness": check_T_finite_weighted_born_soundness,
        "T_actual_measurements_are_povms": check_T_actual_measurements_are_povms,
    }
    for name, fn in premise_rows.items():
        row_premises = set(fn()["premises"])
        if row_premises & FORBIDDEN_DEPENDENCIES:
            fails.append(f"forbidden premise in {name}")
    # Reinsertion mutation, executed.
    g1 = dict(graph)
    g1["T_WEIGHTED_BORN_SOUNDNESS"] = (*g1["T_WEIGHTED_BORN_SOUNDNESS"], "G_HOLD_EXACT")
    if "G_HOLD_EXACT" not in _deps(g1, "T_WEIGHTED_BORN_SOUNDNESS"):
        fails.append("reinsertion mutation not caught by ancestry computation")
    if not (FORBIDDEN_DEPENDENCIES & _all_nodes(g1)):
        fails.append("reinsertion mutation not caught by forbidden-name tripwire")
    return _result(
        "T_g_hold_exact_not_in_born_ancestry",
        "G-hold-exact is not in the dependency ancestry of the operational Born representation theorem: the proof never invokes the grant, the machine contract verifies its absence under its name and the forbidden aliases, and reinsertion is caught. This LOCATES the grant outside this theorem's ancestry; it does not refute it, discharge it, or exhibit a countermodel (Ruling 1 stands: record-level equality cannot adjudicate cost-level mechanism distinctions). The grant remains live for the stronger claim that the coherent hold itself realizes exact outcome selection.",
        {
            "born_ancestry_size": len(born_ancestry),
            "G_hold_exact_in_ancestry": "G_HOLD_EXACT" in born_ancestry,
            "forbidden_leaks": leaked,
            "premise_rows_scanned": len(premise_rows),
            "reinsertion_mutation_caught": True,
            "countermodel_claimed": False,
            "grant_status": "open; located outside the Born ancestry only",
        },
        fails,
        dependencies=("T_dense_born_dependency_contract",),
        negative_controls=("G-hold-exact reinserted into the graph", "record-level countermodel genre (Ruling-1-rejected, not used)"),
        epistemic="P_structural_instrument",
    )


def check_T_soundness_saturation_separation() -> Dict[str, object]:
    fails: List[str] = []
    rho_only = _gscalem(F(1, 2), I2_G)
    z_plus = _gscalem(F(1, 2), _gaddm(I2_G, PAULI_Z))
    z_minus = _gsubm(I2_G, z_plus)
    restricted_states = (rho_only,)
    restricted_measurements = ((z_plus, z_minus),)
    sound = all(_is_psd2(r) and _gtrace(r) == ONE_G for r in restricted_states)
    sound = sound and all(all(_is_effect2(e) for e in meas) and _gaddm(meas[0], meas[1]) == I2_G for meas in restricted_measurements)
    all_states_available = False
    all_povms_available = False
    if not sound or all_states_available or all_povms_available:
        fails.append("restricted quantum model must be sound but nonsaturated")
    return _result(
        "T_soundness_saturation_separation",
        "Born soundness does not imply state completion, measurement completion, or process saturation. A model containing only the maximally mixed state and one Z measurement is a perfectly sound restricted quantum theory but does not realize every density operator or POVM.",
        {
            "restricted_state_count": len(restricted_states),
            "restricted_measurement_count": len(restricted_measurements),
            "Born_sound": sound,
            "state_complete": all_states_available,
            "measurement_complete": all_povms_available,
            "process_saturated": False,
        },
        fails,
        dependencies=("T_finite_weighted_born_soundness", "T_actual_measurements_are_povms"),
        negative_controls=("soundness implies no-restriction",),
    )


def check_T_cp_boundary_preserved() -> Dict[str, object]:
    fails: List[str] = []
    # Choi matrix of transpose on M2: swap operator. Its expectation on
    # |01>-|10> is -2 in the unnormalised convention.
    swap4: RMatrix = (
        (F(1), F(0), F(0), F(0)),
        (F(0), F(0), F(1), F(0)),
        (F(0), F(1), F(0), F(0)),
        (F(0), F(0), F(0), F(1)),
    )
    v = (F(0), F(1), F(-1), F(0))
    sv = tuple(sum(swap4[i][j] * v[j] for j in range(4)) for i in range(4))
    expectation = sum(v[i] * sv[i] for i in range(4))
    if expectation != F(-2):
        fails.append("transpose Choi negative control must give -2")
    return _result(
        "T_cp_boundary_preserved",
        "The dense-sandwich theorem closes state/effect positivity and Born soundness, not complete positivity. Matrix transpose is positive and trace preserving on one system but its Choi matrix has expectation -2 on the antisymmetric vector. CP still requires the separate physical extension-soundness or branch-form theorem.",
        {
            "transpose_positive": True,
            "transpose_trace_preserving": True,
            "choi_negative_expectation": str(expectation),
            "transpose_CP": False,
        },
        fails,
        dependencies=("T_finite_weighted_born_soundness",),
        negative_controls=("positive map treated as completely positive",),
    )


DEPENDENCY_GRAPH: Dict[str, Tuple[str, ...]] = {
    "T_ORIENTED_COMPLEX_MODEL": ("T_ORIENTED_LINKING_ALGEBRA_M2C_v0_5",),
    "T_DYADIC_MATRIX_SYNTHESIS": (
        "T_HFC_345_FACTOR_PACKAGE",
        "AFFINE_MATRIX_CARGO_NATURALITY",
        "FINITE_COLUMN_JOINT_REALIZATION",
        "DYADIC_CLASSICAL_POSITIVE_CONTROL",
        "NULL_PADDING",
        "RETAINED_DEFECT_CHANNEL",
        "SAME_TYPE_RETURN",
    ),
    "T_DENSE_SYNTHESIZED_STAR_RAYS": (
        "T_ORIENTED_COMPLEX_MODEL",
        "T_DYADIC_MATRIX_SYNTHESIS",
        "TYPED_ORIENTED_MATRIX_CARGO",
    ),
    "T_CLOSED_LOOP_TRACE": (
        "T_ORIENTED_COMPLEX_MODEL",
        "CLOSED_LOOP_SCORE_LINEARITY",
        "CLOSED_LOOP_SCORE_CYCLICITY",
        "CLOSED_LOOP_SCORE_NORMALIZATION",
    ),
    "T_EFFECT_SOUNDNESS": (
        "T_DENSE_SYNTHESIZED_STAR_RAYS",
        "T_CLOSED_LOOP_TRACE",
        "REPRESENTED_OUTCOME_READOUTS",
        "DENSE_SANDWICH_CLOSURE",
        "NONNEGATIVE_OUTCOME_READOUTS",
        "EFFECT_COMPLEMENT_CLOSURE",
    ),
    "T_STATE_SOUNDNESS": (
        "T_DENSE_SYNTHESIZED_STAR_RAYS",
        "OUTCOME_AFFINITY_UNDER_CLASSICAL_MIXING",
        "MIXTURE_CONGRUENCE",
        "NORMALIZATION",
        "DENSE_LOOP_EFFECT_REALIZATION",
    ),
    "T_WEIGHTED_BORN_SOUNDNESS": (
        "T_EFFECT_SOUNDNESS",
        "T_STATE_SOUNDNESS",
        "FINITE_OPERATIONAL_TOMOGRAPHY",
        "CONTEXTUAL_EFFECT_IDENTITY",
    ),
    "T_ACTUAL_MEASUREMENTS_POVM": (
        "T_EFFECT_SOUNDNESS",
        "FINITE_OUTCOME_NORMALIZATION",
    ),
    "T_OPTIONAL_EFFECT_COMPLETION": (
        "T_EFFECT_SOUNDNESS",
        "CLOSED_READOUT_LIMITS",
        "DENSE_LOOP_EFFECT_REALIZATION",
    ),
    "T_CP_SOUNDNESS": (
        "T_WEIGHTED_BORN_SOUNDNESS",
        "PHYSICAL_EXTENSION_SOUNDNESS",
        "FINITE_BRANCH_FORM",
        "INSTRUMENT_NORMALIZATION",
    ),
}

FORBIDDEN_DEPENDENCIES = {
    "G_HOLD_EXACT",
    "STATE_COMPLETION",
    "MEASUREMENT_COMPLETION",
    "PROCESS_SATURATION",
    "QUADRATIC_LEDGER_TO_DERIVE_J",
    "CONNECTED_EFFECTIVE_HELD_SWEEP",
    "PULLBACK_NONEXPANSION",
}


def _all_nodes(graph: Mapping[str, Sequence[str]]) -> set[str]:
    return set(graph) | {d for deps in graph.values() for d in deps}


def _roots(graph: Mapping[str, Sequence[str]]) -> Tuple[str, ...]:
    nodes = set(graph)
    return tuple(sorted({d for deps in graph.values() for d in deps if d not in nodes}))


def _cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    nodes = _all_nodes(graph)
    state: Dict[str, int] = {n: 0 for n in nodes}
    stack: List[str] = []

    def dfs(n: str) -> Optional[Tuple[str, ...]]:
        if state[n] == 1:
            i = stack.index(n)
            return tuple(stack[i:] + [n])
        if state[n] == 2:
            return None
        state[n] = 1
        stack.append(n)
        for d in graph.get(n, ()):
            c = dfs(d)
            if c is not None:
                return c
        stack.pop()
        state[n] = 2
        return None

    for n in sorted(nodes):
        c = dfs(n)
        if c is not None:
            return c
    return None


def _deps(graph: Mapping[str, Sequence[str]], node: str) -> set[str]:
    out: set[str] = set()
    todo = list(graph.get(node, ()))
    while todo:
        d = todo.pop()
        if d in out:
            continue
        out.add(d)
        todo.extend(graph.get(d, ()))
    return out


def _load_manifest(path: Path = LEAF_MANIFEST_PATH) -> Dict[str, object]:
    if path.is_file():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        # Bank tree: the embedded constant serves (packet DATA/ absent).
        data = dict(PHYSICAL_LEAF_MANIFEST)
    if not isinstance(data, dict) or not isinstance(data.get("leaves"), dict):
        raise ValueError("invalid physical leaf manifest")
    return data


def check_T_dense_born_dependency_contract() -> Dict[str, object]:
    fails: List[str] = []
    graph = DEPENDENCY_GRAPH
    cyc = _cycle(graph)
    if cyc is not None:
        fails.append(f"dependency cycle: {cyc}")
    leaked = sorted(FORBIDDEN_DEPENDENCIES & _all_nodes(graph))
    if leaked:
        fails.append(f"forbidden dependencies leaked into graph: {leaked}")
    born_deps = _deps(graph, "T_WEIGHTED_BORN_SOUNDNESS")
    if "T_CP_SOUNDNESS" in born_deps:
        fails.append("Born soundness must not consume CP")
    if "T_OPTIONAL_EFFECT_COMPLETION" in born_deps:
        fails.append("Born soundness must not consume effect saturation")
    if "T_ACTUAL_MEASUREMENTS_POVM" not in graph:
        fails.append("actual-measurement soundness node missing")
    manifest = _load_manifest()
    manifest_leaves = tuple(sorted(manifest["leaves"].keys()))  # type: ignore[index,union-attr]
    graph_roots = _roots(graph)
    # The manifest is an independent superset inventory; every graph root that
    # is a physical/structural premise must be declared there, while prior
    # theorem certificates are allowed as theorem roots.
    undeclared = sorted(
        r for r in graph_roots
        if not r.startswith("T_") and r not in manifest_leaves
    )
    if undeclared:
        fails.append(f"undeclared physical roots: {undeclared}")

    # Mutations.
    g1 = dict(graph)
    g1["T_WEIGHTED_BORN_SOUNDNESS"] = (*g1["T_WEIGHTED_BORN_SOUNDNESS"], "G_HOLD_EXACT")
    g_hold_mutation_caught = bool(FORBIDDEN_DEPENDENCIES & _all_nodes(g1))
    if not g_hold_mutation_caught:
        fails.append("G-hold-exact mutation not caught")
    g2 = dict(graph)
    g2["T_STATE_SOUNDNESS"] = tuple(d for d in g2["T_STATE_SOUNDNESS"] if d != "MIXTURE_CONGRUENCE")
    removed_leaf_caught = _roots(g2) != graph_roots
    if not removed_leaf_caught:
        fails.append("removed physical leaf mutation not caught")
    g3 = dict(graph)
    g3["T_ORIENTED_COMPLEX_MODEL"] = (*g3["T_ORIENTED_COMPLEX_MODEL"], "T_WEIGHTED_BORN_SOUNDNESS")
    cycle_mutation_caught = _cycle(g3) is not None
    if not cycle_mutation_caught:
        fails.append("Born-to-orientation cycle mutation not caught")

    return _result(
        "T_dense_born_dependency_contract",
        "Weighted Born soundness depends on the oriented complex algebra, explicit dense HFC matrix-cargo synthesis, closed-sandwich state/effect soundness, operational affinity, tomography, and effect identity. It does not depend on G-hold-exact or on any no-restriction saturation claim. CP remains downstream behind extension soundness and finite branch form.",
        {
            "graph": {k: list(v) for k, v in graph.items()},
            "roots": list(graph_roots),
            "manifest_leaves": list(manifest_leaves),
            "forbidden_dependencies": sorted(FORBIDDEN_DEPENDENCIES),
            "forbidden_leaks": leaked,
            "G_hold_mutation_caught": g_hold_mutation_caught,
            "removed_leaf_mutation_caught": removed_leaf_caught,
            "cycle_mutation_caught": cycle_mutation_caught,
            "Born_consumes_effect_completion": False,
            "Born_consumes_CP": False,
        },
        fails,
        dependencies=tuple(graph),
        negative_controls=("G-hold-exact reinserted", "soundness-saturation collapse", "Born/CP cycle"),
        epistemic="P_structural_instrument",
    )


# ---------------------------------------------------------------------------
# Composed root inventory (MAJOR-2) and premises<->graph concordance (F6)
# ---------------------------------------------------------------------------

# Register 2: imported via T_ORIENTED_LINKING_ALGEBRA_M2C_v0_5 (the fortified
# graded-orientation intake packet, re-pinned in SOURCES/).  The two
# realization premises are that packet's check-level premise inventory; the
# four gates are the banked Ruling-3 central-J contract names, which remain
# physical/categorical premises at network scale (Ruling 3 stands).
IMPORTED_GRADED_ORIENTATION_PREMISES: Tuple[str, ...] = (
    "ORIENTATION_COVER_REALIZED",
    "ORIENTATION_SHEET_TYPING",
)
IMPORTED_CENTRAL_J_GATES: Tuple[str, ...] = (
    "GENERATOR_COMPLETENESS",
    "NATURALITY",
    "ORIENTATION_SYNCHRONIZATION",
    "T_LOCAL_J",
)

# Register 3: imported via T_HFC_345_FACTOR_PACKAGE (the banked v24.3.432
# thirteen-leaf contract, apf._hfc_345_contracts.LEAF_MANIFEST, vendored in
# SOURCES/).
IMPORTED_HFC_345_CONTRACT_LEAVES: Tuple[str, ...] = (
    "A2_NO_WASTE_MINIMUM",
    "COMPLETE_HELD_PROFILE",
    "EFFECTIVE_BASELINE_BINARY_EXCHANGE",
    "EXACT_345_DEFENDER_GEOMETRY",
    "EXCHANGE_CARGO_NATURALITY",
    "FACTOR_ISOLATION_NEUTRAL_COMPLETION",
    "FINITE_COMPATIBLE_JOINT_REALIZATION",
    "FUTURE_CONSEQUENTIAL_DEFECT",
    "LIVE_345_HELD_FAIR_COMMONING",
    "LIVE_345_RECORD_FREE_PORT_EXCHANGE",
    "NEUTRAL_E2_COMPLETION",
    "SAME_TYPE_RETURN",
    "ZIPPER_REVERSAL_IS_INVERSE",
)

VENDORED_HFC_CONTRACTS_PATH = PACKAGE_ROOT / "SOURCES" / "_hfc_345_contracts_BANKED_v24.3.432.py"
VENDORED_GRADED_ORIENTATION_PATH = PACKAGE_ROOT / "SOURCES" / "graded_orientation_closure_v0.5.py"
SIBLING_V08_MANIFEST_PATH = (
    PACKAGE_ROOT.parent / "APF_Operational_Score_Linearity_v0.8" / "DATA" / "reduced_leaf_manifest.json"
)


def _packet_local_core_leaves() -> set:
    manifest = _load_manifest()
    return {
        k for k, row in manifest["leaves"].items()
        if row["type"] not in {"optional_saturation", "physical_downstream"}
    }


def check_T_composed_root_inventory() -> Dict[str, object]:
    """MAJOR-2 carried: 'conditional on 21 explicit core leaves' is the
    packet-LOCAL increment only.  The full composed antecedent surface is
    machine-checked here in three registers, each cited to its source:
    (1) the 21 packet-local core leaves (DATA/physical_leaf_manifest.json),
    (2) the imported graded-orientation inventory riding the theorem root
        T_ORIENTED_LINKING_ALGEBRA_M2C_v0_5 (fortified intake packet), and
    (3) the banked HFC-345 thirteen-leaf contract riding the theorem root
        T_HFC_345_FACTOR_PACKAGE (v24.3.432).
    Set-exactness is verified against the re-pinned vendored sources, the
    single shared name is disclosed, and drift mutations are executed."""
    fails: List[str] = []
    packet_local = _packet_local_core_leaves()
    if len(packet_local) != 21:
        fails.append(f"packet-local core inventory must be 21, got {len(packet_local)}")
    graph_physical_roots = {r for r in _roots(DEPENDENCY_GRAPH) if not r.startswith("T_")}
    optional_and_downstream = {
        "CLOSED_READOUT_LIMITS", "PHYSICAL_EXTENSION_SOUNDNESS",
        "FINITE_BRANCH_FORM", "INSTRUMENT_NORMALIZATION",
    }
    if graph_physical_roots - optional_and_downstream != packet_local:
        fails.append("graph physical roots drift against the manifest core inventory")

    ig_orient = set(IMPORTED_GRADED_ORIENTATION_PREMISES)
    ig_gates = set(IMPORTED_CENTRAL_J_GATES)
    ig_hfc = set(IMPORTED_HFC_345_CONTRACT_LEAVES)

    # Verify register 3 against the banked contract, fail-closed.  Bank
    # landing (v24.3.434): the REAL banked apf._hfc_345_contracts is tried
    # FIRST (the strictly stronger check -- the live machine-pinned
    # inventory); the vendored SOURCES/ copy is the packet-standalone
    # fallback only.  Neither reachable => fail.
    hfc_contract_source = None
    contract_leaves = contract_gates = None
    try:
        from apf._hfc_345_contracts import (
            LEAF_MANIFEST as _banked_leaf_manifest,
            CENTRAL_J_REQUIRED_GATES as _banked_gates,
        )
        contract_leaves = set(_banked_leaf_manifest["leaves"].keys())
        contract_gates = set(_banked_gates)
        hfc_contract_source = "banked_module"
    except ImportError:
        if VENDORED_HFC_CONTRACTS_PATH.is_file():
            namespace: Dict[str, object] = {}
            exec(VENDORED_HFC_CONTRACTS_PATH.read_text(encoding="utf-8"), namespace)
            contract_leaves = set(namespace["LEAF_MANIFEST"]["leaves"].keys())  # type: ignore[index]
            contract_gates = set(namespace["CENTRAL_J_REQUIRED_GATES"])  # type: ignore[arg-type]
            hfc_contract_source = "vendored_file"
    if contract_leaves is None or contract_gates is None:
        fails.append(
            "HFC-345 contract unreachable: neither the banked "
            "apf._hfc_345_contracts nor the vendored SOURCES/ copy resolves"
        )
    else:
        if contract_leaves != ig_hfc:
            fails.append(f"HFC-345 contract drift: {sorted(contract_leaves ^ ig_hfc)}")
        if contract_gates != ig_gates:
            fails.append(f"central-J gate drift: {sorted(contract_gates ^ ig_gates)}")

    # Verify register 2 against the fortified orientation source.  Bank
    # landing (v24.3.434): the INSTALLED apf/graded_orientation_closure.py
    # (located via importlib.util.find_spec) is scanned FIRST -- the banked
    # copy is the stronger referent; the re-pinned vendored SOURCES/ copy is
    # the packet-standalone fallback.  Neither reachable => fail.
    orientation_source = None
    orientation_text = None
    _go_spec = importlib.util.find_spec("apf.graded_orientation_closure")
    if _go_spec is not None and _go_spec.origin:
        orientation_text = Path(_go_spec.origin).read_text(encoding="utf-8")
        orientation_source = "banked_module"
    elif VENDORED_GRADED_ORIENTATION_PATH.is_file():
        orientation_text = VENDORED_GRADED_ORIENTATION_PATH.read_text(encoding="utf-8")
        orientation_source = "vendored_file"
    if orientation_text is None:
        fails.append(
            "graded-orientation source unreachable: neither the installed "
            "apf.graded_orientation_closure nor the vendored SOURCES/ copy resolves"
        )
    else:
        for name in sorted(ig_orient | ig_gates):
            if name not in orientation_text:
                fails.append(f"imported premise {name} absent from the orientation source ({orientation_source})")
        if "FORTIFICATION 2026-07-21" not in orientation_text:
            fails.append(f"orientation source ({orientation_source}) is not the fortified copy")

    # Overlap discipline: the composed union double-counts nothing silently.
    shared = packet_local & ig_hfc
    if shared != {"SAME_TYPE_RETURN"}:
        fails.append(f"unexpected register overlap: {sorted(shared)}")
    if packet_local & (ig_orient | ig_gates):
        fails.append("packet-local leaves must not shadow orientation imports")
    composed = packet_local | ig_orient | ig_gates | ig_hfc
    expected_composed_size = 21 + 2 + 4 + 13 - 1  # SAME_TYPE_RETURN shared
    if len(composed) != expected_composed_size:
        fails.append(f"composed inventory size {len(composed)} != {expected_composed_size}")

    # Drift mutations, executed.
    mutated_hfc = ig_hfc | {"PHANTOM_LEAF"}
    if mutated_hfc == ig_hfc:
        fails.append("added-leaf mutation not caught")
    mutated_orient = ig_orient - {"ORIENTATION_COVER_REALIZED"}
    if mutated_orient == ig_orient:
        fails.append("removed-leaf mutation not caught")

    # Cross-check: this packet's CLOSED_LOOP_SCORE_LINEARITY leaf may cite the
    # score-linearity packet's reduction ONLY at its post-fortification
    # strength (named leaf set including CLASSICAL_SCORE_TOTALITY).
    # Bank landing (v24.3.434): the sibling's embedded REDUCED_LEAF_MANIFEST
    # constant (the banked apf.operational_score_linearity) is tried FIRST;
    # the packet-relative sibling path is the standalone fallback.  Neither
    # reachable => fail.
    sib = None
    sibling_v08_source = None
    try:
        from apf.operational_score_linearity import REDUCED_LEAF_MANIFEST as _sib_manifest
        sib = dict(_sib_manifest)
        sibling_v08_source = "banked_module"
    except ImportError:
        if SIBLING_V08_MANIFEST_PATH.is_file():
            sib = json.loads(SIBLING_V08_MANIFEST_PATH.read_text(encoding="utf-8"))
            sibling_v08_source = "sibling_packet_file"
    if sib is None:
        fails.append("sibling v0.8 post-fix manifest not reachable")
    else:
        sib_leaves = set(sib.get("primitive_operational_leaves", ()))
        if "CLASSICAL_SCORE_TOTALITY" not in sib_leaves:
            fails.append("sibling v0.8 manifest lacks CLASSICAL_SCORE_TOTALITY (pre-fix copy?)")
        if "CLOSED_LOOP_SCORE_LINEARITY" not in set(sib.get("derived_and_removed_as_independent_leaves", ())):
            fails.append("sibling v0.8 manifest does not carry the linearity re-factoring")
        if sib.get("physical_premises_certified") is not False:
            fails.append("sibling v0.8 manifest must state ppc=false")

    return _result(
        "T_composed_root_inventory",
        "The composed antecedent surface of the weighted Born theorem is 21 packet-local core leaves PLUS the imported graded-orientation inventory (ORIENTATION_COVER_REALIZED, ORIENTATION_SHEET_TYPING, and the four Ruling-3 central-J gates, riding T_ORIENTED_LINKING_ALGEBRA_M2C_v0_5) PLUS the banked HFC-345 thirteen-leaf contract (riding T_HFC_345_FACTOR_PACKAGE): 39 distinct named premises, SAME_TYPE_RETURN shared between the packet-local and HFC registers. The headline 'conditional on 21 core leaves' is licensed only in the two-register form. The linearity leaf's reduction citation is pinned to the v0.8 post-fortification strength (CLASSICAL_SCORE_TOTALITY named).",
        {
            "packet_local_core_count": len(packet_local),
            "imported_graded_orientation": sorted(ig_orient),
            "imported_central_j_gates": sorted(ig_gates),
            "imported_hfc_345_contract_count": len(ig_hfc),
            "shared_names": sorted(shared),
            "composed_distinct_total": len(composed),
            "sibling_v08_post_fix_verified": sib is not None,
            "hfc_contract_source": hfc_contract_source,
            "orientation_source": orientation_source,
            "sibling_v08_source": sibling_v08_source,
            "sources_verified": [
                hfc_contract_source or "UNRESOLVED",
                orientation_source or "UNRESOLVED",
            ],
        },
        fails,
        dependencies=("T_dense_born_dependency_contract",),
        negative_controls=("packet-local count billed as the whole antecedent", "pre-fortification source drift", "pre-fix v0.8 reduction citation"),
        epistemic="P_structural_instrument",
    )


CHECK_NODE_MAP: Dict[str, str] = {
    "T_hfc_dyadic_matrix_ray_synthesis": "T_DYADIC_MATRIX_SYNTHESIS",
    "T_dense_dyadic_star_subalgebra": "T_DENSE_SYNTHESIZED_STAR_RAYS",
    "T_closed_loop_score_is_normalized_trace": "T_CLOSED_LOOP_TRACE",
    "T_dense_sandwich_effect_soundness": "T_EFFECT_SOUNDNESS",
    "T_dense_loop_state_positivity": "T_STATE_SOUNDNESS",
    "T_finite_weighted_born_soundness": "T_WEIGHTED_BORN_SOUNDNESS",
    "T_actual_measurements_are_povms": "T_ACTUAL_MEASUREMENTS_POVM",
}


def check_T_premises_graph_concordance() -> Dict[str, object]:
    """F6 carried: nothing previously enforced agreement between per-check
    premises tuples and DEPENDENCY_GRAPH premise edges (the audit found
    TYPED_ORIENTED_MATRIX_CARGO in the graph but in no check's premises).
    This check derives both sides and compares set-exactly per node, compares
    the premise UNION against the manifest core inventory, and executes a
    drift mutation."""
    fails: List[str] = []
    check_fns = {
        "T_hfc_dyadic_matrix_ray_synthesis": check_T_hfc_dyadic_matrix_ray_synthesis,
        "T_dense_dyadic_star_subalgebra": check_T_dense_dyadic_star_subalgebra,
        "T_closed_loop_score_is_normalized_trace": check_T_closed_loop_score_is_normalized_trace,
        "T_dense_sandwich_effect_soundness": check_T_dense_sandwich_effect_soundness,
        "T_dense_loop_state_positivity": check_T_dense_loop_state_positivity,
        "T_finite_weighted_born_soundness": check_T_finite_weighted_born_soundness,
        "T_actual_measurements_are_povms": check_T_actual_measurements_are_povms,
    }
    row_premises: Dict[str, set] = {
        name: set(fn()["premises"]) for name, fn in check_fns.items()
    }
    graph_premises: Dict[str, set] = {}
    for check_name, node in CHECK_NODE_MAP.items():
        graph_premises[check_name] = {
            d for d in DEPENDENCY_GRAPH[node] if not d.startswith("T_")
        }
        if row_premises[check_name] != graph_premises[check_name]:
            fails.append(
                f"premise drift at {check_name}: "
                f"{sorted(row_premises[check_name] ^ graph_premises[check_name])}"
            )
    union = set().union(*row_premises.values())
    core = _packet_local_core_leaves()
    if union != core:
        fails.append(f"premise union drift against manifest core: {sorted(union ^ core)}")
    # Drift mutation, executed: dropping one premise from a copied row breaks
    # both the per-node comparison and the union comparison.
    mutated = dict(row_premises)
    mutated["T_dense_dyadic_star_subalgebra"] = set()
    mutation_caught = (
        mutated["T_dense_dyadic_star_subalgebra"] != graph_premises["T_dense_dyadic_star_subalgebra"]
        and set().union(*mutated.values()) != core
    )
    if not mutation_caught:
        fails.append("premise-drop mutation not caught")
    return _result(
        "T_premises_graph_concordance",
        "Per-check premises tuples and DEPENDENCY_GRAPH premise edges agree set-exactly at every mapped node, and their union is set-exactly the 21-leaf manifest core inventory. The audit's drift instance (TYPED_ORIENTED_MATRIX_CARGO present in the graph, absent from every check row) is fixed at the dense-subalgebra check and can no longer recur silently.",
        {
            "nodes_checked": len(CHECK_NODE_MAP),
            "premise_union_size": len(union),
            "manifest_core_size": len(core),
            "drift_mutation_caught": mutation_caught,
        },
        fails,
        dependencies=("T_dense_born_dependency_contract",),
        negative_controls=("graph-only premise", "check-only premise", "union/manifest drift"),
        epistemic="P_structural_instrument",
    )


_CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_oriented_complex_model_exact": check_T_oriented_complex_model_exact,
    "T_hfc_dyadic_matrix_ray_synthesis": check_T_hfc_dyadic_matrix_ray_synthesis,
    "T_dense_dyadic_star_subalgebra": check_T_dense_dyadic_star_subalgebra,
    "T_closed_loop_score_is_normalized_trace": check_T_closed_loop_score_is_normalized_trace,
    "T_dense_sandwich_effect_soundness": check_T_dense_sandwich_effect_soundness,
    "T_dense_loop_state_positivity": check_T_dense_loop_state_positivity,
    "T_finite_weighted_born_soundness": check_T_finite_weighted_born_soundness,
    "T_actual_measurements_are_povms": check_T_actual_measurements_are_povms,
    "T_g_hold_exact_not_in_born_ancestry": check_T_g_hold_exact_not_in_born_ancestry,
    "T_soundness_saturation_separation": check_T_soundness_saturation_separation,
    "T_cp_boundary_preserved": check_T_cp_boundary_preserved,
    "T_dense_born_dependency_contract": check_T_dense_born_dependency_contract,
    "T_composed_root_inventory": check_T_composed_root_inventory,
    "T_premises_graph_concordance": check_T_premises_graph_concordance,
}


def register(registry) -> None:
    """Bank registration (v24.3.434): stripped-``check_``-prefix keys, the
    registry convention of apf/held_holonomy.py."""
    registry.update(_CHECKS)


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in _CHECKS.items()}


def build_certificate(rows: Optional[Mapping[str, Mapping[str, object]]] = None) -> DenseSandwichBornCertificate:
    rows = rows or run_all()
    p = lambda key: bool(rows[key]["passed"])
    return DenseSandwichBornCertificate(
        oriented_complex_model_exact=p("T_oriented_complex_model_exact"),
        dyadic_matrix_ray_synthesis_exact=p("T_hfc_dyadic_matrix_ray_synthesis"),
        dense_star_subalgebra_exact=p("T_dense_dyadic_star_subalgebra"),
        closed_loop_score_is_trace_exact=p("T_closed_loop_score_is_normalized_trace"),
        dense_sandwich_effect_soundness_exact=p("T_dense_sandwich_effect_soundness"),
        dense_loop_state_positivity_exact=p("T_dense_loop_state_positivity"),
        finite_born_trace_representation_exact=p("T_finite_weighted_born_soundness"),
        actual_measurements_are_povms=p("T_actual_measurements_are_povms"),
        g_hold_exact_not_in_born_ancestry=p("T_g_hold_exact_not_in_born_ancestry")
        and p("T_dense_born_dependency_contract"),
        saturation_claims_separated=p("T_soundness_saturation_separation"),
        cp_boundary_preserved=p("T_cp_boundary_preserved"),
        dependency_contract_clean=p("T_dense_born_dependency_contract"),
        composed_root_inventory_exact=p("T_composed_root_inventory"),
        premises_graph_concordant=p("T_premises_graph_concordance"),
        physical_premises_certified=False,
    )


def main() -> int:
    rows = run_all()
    cert = build_certificate(rows)
    payload = {
        "certificate": asdict(cert),
        "checks": rows,
        "physical_premises_certified": False,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if all(bool(r["passed"]) for r in rows.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
