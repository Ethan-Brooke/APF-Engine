"""Private exact-algebra helpers for :mod:`apf.held_holonomy`."""
from __future__ import annotations


from dataclasses import asdict, dataclass
from fractions import Fraction as F
from itertools import permutations, product
from typing import Callable, Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Tuple


Matrix = List[List[F]]
Vector = List[F]
Permutation = Tuple[int, ...]

FAMILY = "quantum.held_holonomy"
PAPER_TARGETS = (
    "Paper 5",
    "Paper 10",
    "Paper 14",
    "Paper 2 Technical Supplement II",
    "Paper 12 Technical Supplement",
    "Paper 1 Technical Supplement",
    "Paper 33 Technical Supplement",
    "Paper 37 Technical Supplement",
    "Paper 44 Technical Supplement",
)

PHYSICAL_PREMISES = (
    "occupied_record_free_coherent_component",
    "reversible_Held_path_groupoid",
    "two_sided_complete_operational_congruence",
    "later_recombination_witness",
    "connected_Regime_R_component",
    "continuous_effective_action",
    "effective_image_is_a_Lie_subgroup_of_SO2",
    "positive_quadratic_ledger_form",
    "Q2_reversal_is_ledger_adjoint",
    "reversed_loop_is_inverse",
    "elementary_bipolar_first_order_completeness",
    "faithful_first_order_action",
    "jet_functoriality",
    "orientation_synchronization_across_typed_sectors",
    "continuous_conjugation_orientation_transport",
    "closed_world_record_completeness",
    "generator_completeness",
    "finite_real_Cstar_completion",
)


@dataclass(frozen=True)
class FinitePath:
    """Finite path token used by the exact witness models."""

    name: str
    source: str
    target: str
    inverse_name: Optional[str] = None


@dataclass(frozen=True)
class PathClass:
    """Operational path class represented by a complete finite signature."""

    representative: str
    signature: Tuple[object, ...]


@dataclass(frozen=True)
class HolonomyCertificate:
    """Aggregate certificate.

    Every boolean records a passed finite theorem schema or negative-control
    battery.  It does not assert that the named physical premises obtain in the
    world; ``physical_premises_certified`` is therefore always false here.
    """

    group_axioms: bool
    nontrivial: bool
    connected_model: bool
    isometric_action: bool
    rank_two: bool
    full_so2_image: bool
    quarter_turn_square_minus_identity: bool
    naturality: bool
    central_complex_block_exclusion: bool
    sat_bypassed_not_refuted: bool
    dependency_contract_acyclic: bool
    physical_premises_certified: bool
    scope: str
    dependencies: Tuple[str, ...]


# ---------------------------------------------------------------------------
# Exact linear algebra
# ---------------------------------------------------------------------------


def _zero(r: int, c: int) -> Matrix:
    return [[F(0) for _ in range(c)] for _ in range(r)]


def _eye(n: int) -> Matrix:
    return [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]


def _shape(a: Matrix) -> Tuple[int, int]:
    return len(a), len(a[0]) if a else 0


def _add(a: Matrix, b: Matrix) -> Matrix:
    if _shape(a) != _shape(b):
        raise ValueError("matrix shape mismatch")
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def _sub(a: Matrix, b: Matrix) -> Matrix:
    if _shape(a) != _shape(b):
        raise ValueError("matrix shape mismatch")
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def _scal(s: F, a: Matrix) -> Matrix:
    return [[s * x for x in row] for row in a]


def _mm(a: Matrix, b: Matrix) -> Matrix:
    ar, ac = _shape(a)
    br, bc = _shape(b)
    if ac != br:
        raise ValueError("matrix shape mismatch")
    return [[sum(a[i][k] * b[k][j] for k in range(ac))
             for j in range(bc)] for i in range(ar)]


def _mv(a: Matrix, v: Vector) -> Vector:
    if not a or len(a[0]) != len(v):
        raise ValueError("matrix/vector shape mismatch")
    return [sum(a[i][j] * v[j] for j in range(len(v)))
            for i in range(len(a))]


def _transpose(a: Matrix) -> Matrix:
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]


def _eq(a: Matrix, b: Matrix) -> bool:
    return _shape(a) == _shape(b) and all(
        a[i][j] == b[i][j]
        for i in range(len(a)) for j in range(len(a[0]))
    )


def _vec_eq(a: Vector, b: Vector) -> bool:
    return len(a) == len(b) and all(x == y for x, y in zip(a, b))


def _inverse(a: Matrix) -> Matrix:
    n, m = _shape(a)
    if n != m:
        raise ValueError("inverse requires a square matrix")
    aug = [row[:] + eye_row[:] for row, eye_row in zip(a, _eye(n))]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col] != 0), None)
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        p = aug[col][col]
        aug[col] = [x / p for x in aug[col]]
        for r in range(n):
            if r == col:
                continue
            q = aug[r][col]
            if q != 0:
                aug[r] = [aug[r][j] - q * aug[col][j]
                          for j in range(2 * n)]
    return [row[n:] for row in aug]


def _det2(a: Matrix) -> F:
    if _shape(a) != (2, 2):
        raise ValueError("det2 requires 2x2")
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def _quadratic(b: Matrix, v: Vector) -> F:
    return sum(v[i] * b[i][j] * v[j]
               for i in range(len(v)) for j in range(len(v)))


def _is_psd_2(a: Matrix) -> bool:
    return (
        _shape(a) == (2, 2)
        and a[0][1] == a[1][0]
        and a[0][0] >= 0
        and a[1][1] >= 0
        and _det2(a) >= 0
    )


def _rank(a: Matrix) -> int:
    if not a:
        return 0
    m = [row[:] for row in a]
    r, c = _shape(m)
    rank = 0
    col = 0
    while rank < r and col < c:
        pivot = next((k for k in range(rank, r) if m[k][col] != 0), None)
        if pivot is None:
            col += 1
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        p = m[rank][col]
        m[rank] = [x / p for x in m[rank]]
        for i in range(r):
            if i == rank:
                continue
            q = m[i][col]
            if q != 0:
                m[i] = [m[i][j] - q * m[rank][j] for j in range(c)]
        rank += 1
        col += 1
    return rank


def _flatten(a: Matrix) -> Vector:
    return [x for row in a for x in row]


def _matrix_units(n: int) -> List[Matrix]:
    out: List[Matrix] = []
    for i in range(n):
        for j in range(n):
            e = _zero(n, n)
            e[i][j] = F(1)
            out.append(e)
    return out


def _commutant_constraint_matrix(algebra_basis: Sequence[Matrix], n: int) -> Matrix:
    """Linear system for X A - A X = 0 over all basis matrices A."""

    unknown_basis = _matrix_units(n)
    rows: Matrix = []
    for a in algebra_basis:
        columns = [_flatten(_sub(_mm(x, a), _mm(a, x)))
                   for x in unknown_basis]
        for output_coordinate in range(n * n):
            rows.append([columns[k][output_coordinate]
                         for k in range(n * n)])
    return rows


def _matrix_strings(a: Matrix) -> List[List[str]]:
    return [[str(x) for x in row] for row in a]


# ---------------------------------------------------------------------------
# Finite groups and quotients
# ---------------------------------------------------------------------------


def _perm_compose(p: Permutation, q: Permutation) -> Permutation:
    """Composition p after q."""

    return tuple(p[q[i]] for i in range(len(p)))


def _perm_inverse(p: Permutation) -> Permutation:
    inv = [0 for _ in p]
    for i, value in enumerate(p):
        inv[value] = i
    return tuple(inv)


def _perm_group(n: int) -> Tuple[Permutation, ...]:
    return tuple(tuple(p) for p in permutations(range(n)))


def _right_coset(g: Permutation, subgroup: FrozenSet[Permutation]) -> FrozenSet[Permutation]:
    return frozenset(_perm_compose(g, h) for h in subgroup)


def _same_right_coset(a: Permutation, b: Permutation,
                      subgroup: FrozenSet[Permutation]) -> bool:
    return _right_coset(a, subgroup) == _right_coset(b, subgroup)


def _find_one_sided_failure(group: Sequence[Permutation],
                            subgroup: FrozenSet[Permutation]) -> Optional[Tuple[Permutation, ...]]:
    for a, a2, b, b2 in product(group, repeat=4):
        if not _same_right_coset(a, a2, subgroup):
            continue
        if not _same_right_coset(b, b2, subgroup):
            continue
        ab = _perm_compose(a, b)
        a2b2 = _perm_compose(a2, b2)
        if not _same_right_coset(ab, a2b2, subgroup):
            return a, a2, b, b2, ab, a2b2
    return None


# ---------------------------------------------------------------------------
# Result schema
# ---------------------------------------------------------------------------


def _result(name: str, epistemic: str, key_result: str,
            dependencies: Sequence[str], artifacts: Mapping[str, object],
            fails: Sequence[str], premises: Sequence[str] = (),
            negative_controls: Sequence[str] = (),
            cross_refs: Sequence[str] = ()) -> Dict[str, object]:
    passed = not fails
    return {
        "name": name,
        "family": FAMILY,
        "epistemic": epistemic,
        "tier": 4,
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "scope": "finite mathematical witness",
        "physical_premises_certified": False,
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "paper_targets": list(PAPER_TARGETS),
        "key_result": key_result,
        "dependencies": list(dependencies),
        "cross_refs": list(cross_refs),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


# ---------------------------------------------------------------------------
# H1: relative loops and the torsor/group distinction
# ---------------------------------------------------------------------------



# Private sibling modules intentionally import the exact helper surface.
__all__ = [name for name in globals() if not name.startswith("__")]
