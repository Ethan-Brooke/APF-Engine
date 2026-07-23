"""Exact finite witnesses for the APF orientation-double-cover repair.

The HFC-345 packet gives two exact real reflections S0 and Su, their product
R=Su*S0, and the polynomially recovered square-minus-one operator

    J = (25 R + 7 I)/24.

A hidden obstruction appears immediately: each reflection anticommutes with J.
If S0 and Su are treated as endomorphisms in one ungraded real algebra, that
algebra is all of M_2(R), whose centre is only R*I.  J is therefore not central.

The correct completion is the orientation double cover.  The two ordered
exchange presentations are distinct objects.  S0 and Su are sheet-changing
morphisms.  The plus sheet carries R=Su*S0 and the minus sheet carries
R^{-1}=S0*Su.  Their polynomial orientations are J and -J.  In the resulting
four-real-dimensional linking representation, both exchanges commute with

    J_or = diag(J,-J),

and the generated algebra is exactly the eight-real-dimensional commutant of
J_or in M_4(R), hence M_2(C) viewed as a real *-algebra.  Its centre is
span_R{I,J_or}.

This module certifies the finite mathematics and the dependency contract.  It
does not certify the HFC-345 physical leaves, positive-state soundness, or the
identification of the oriented linking envelope with a realised physical
interface.

Gate naming (FORTIFICATION 2026-07-21, per the cold audit's F3 recommendation
(b), flagged for principal review): the dependency contract keeps the BANKED
Ruling-3 gate names.  The central-J antecedent is set-exactly

    T_LOCAL_J + NATURALITY + ORIENTATION_SYNCHRONIZATION
        + GENERATOR_COMPLETENESS  =>  T_CENTRAL_J,

matching ``apf._hfc_345_contracts.CENTRAL_J_REQUIRED_GATES`` (v24.3.432,
commit 8360a45) and ``check_T_central_j_gate_contract``.  This module is
billed as the EXECUTABLE SEMANTICS of those gates at the elementary carrier:
the double-cover construction is the executable content of
ORIENTATION_SYNCHRONIZATION, and the even/graded distinction is the typing of
GENERATOR_COMPLETENESS -- not a renamed gate.  The earlier disjunctive gate
name GLOBAL_PARITY_COCYCLE_OR_DOUBLE_COVER is retired as mathematically
vacuous (the canonical cover always exists); its place is taken by the
realization-typed physical premise ORIENTATION_COVER_REALIZED: the physical
interface must realize the double cover.  That premise is never certified by
this packet.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
import importlib.util
import json
import os
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

FAMILY = "quantum.graded_orientation_double_cover"
Matrix = Tuple[Tuple[F, ...], ...]
Vector = Tuple[F, ...]


@dataclass(frozen=True)
class GradedOrientationCertificate:
    local_J_exact: bool
    reflection_obstruction_exposed: bool
    local_full_algebra_is_M2R: bool
    even_algebra_is_complex_line: bool
    orientation_double_cover_natural: bool
    oriented_linking_algebra_is_M2C: bool
    parity_cocycle_criterion_exact: bool
    double_cover_orients_nonorientable_networks: bool
    odd_fixed_sheet_CP_control: bool
    dependency_contract_clean: bool
    orientation_sheet_typing_premise_named: bool
    orientation_cover_realized_premise_named: bool
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
        "scope": "finite exact mathematics / graded-orientation contract",
        "physical_premises_certified": False,
        "key_result": key_result,
        "dependencies": list(dependencies),
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


# ---------------------------------------------------------------------------
# Exact matrix algebra
# ---------------------------------------------------------------------------


def _shape(a: Matrix) -> Tuple[int, int]:
    return len(a), len(a[0]) if a else 0


def _zero(n: int, m: Optional[int] = None) -> Matrix:
    m = n if m is None else m
    return tuple(tuple(F(0) for _ in range(m)) for _ in range(n))


def _eye(n: int) -> Matrix:
    return tuple(tuple(F(1) if i == j else F(0) for j in range(n)) for i in range(n))


def _mm(a: Matrix, b: Matrix) -> Matrix:
    ar, ac = _shape(a)
    br, bc = _shape(b)
    if ac != br:
        raise ValueError("matrix shape mismatch")
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(ac)) for j in range(bc))
        for i in range(ar)
    )


def _mv(a: Matrix, v: Vector) -> Vector:
    if len(a[0]) != len(v):
        raise ValueError("matrix/vector shape mismatch")
    return tuple(sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a)))


def _add(a: Matrix, b: Matrix) -> Matrix:
    if _shape(a) != _shape(b):
        raise ValueError("matrix shape mismatch")
    return tuple(tuple(a[i][j] + b[i][j] for j in range(len(a[0]))) for i in range(len(a)))


def _sub(a: Matrix, b: Matrix) -> Matrix:
    return _add(a, _scale(F(-1), b))


def _scale(s: F, a: Matrix) -> Matrix:
    return tuple(tuple(s * x for x in row) for row in a)


def _transpose(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a[0])))


def _block(a: Matrix, b: Matrix, c: Matrix, d: Matrix) -> Matrix:
    if len(a) != len(b) or len(c) != len(d):
        raise ValueError("block row mismatch")
    if len(a[0]) != len(c[0]) or len(b[0]) != len(d[0]):
        raise ValueError("block column mismatch")
    return tuple(tuple(a[i]) + tuple(b[i]) for i in range(len(a))) + tuple(
        tuple(c[i]) + tuple(d[i]) for i in range(len(c))
    )


def _flatten(a: Matrix) -> List[F]:
    return [x for row in a for x in row]


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


def _span_basis(mats: Iterable[Matrix]) -> List[Matrix]:
    basis: List[Matrix] = []
    for m in mats:
        if _rank([_flatten(b) for b in basis] + [_flatten(m)]) > len(basis):
            basis.append(m)
    return basis


def _algebra_closure(generators: Sequence[Matrix]) -> List[Matrix]:
    basis = _span_basis(generators)
    changed = True
    while changed:
        changed = False
        snapshot = list(basis)
        for a in snapshot:
            for b in snapshot:
                product = _mm(a, b)
                if _rank([_flatten(x) for x in basis] + [_flatten(product)]) > len(basis):
                    basis.append(product)
                    changed = True
    return basis


def _commutant_dimension(a: Matrix) -> int:
    n, m = _shape(a)
    if n != m:
        raise ValueError("commutant requires square matrix")
    units: List[Matrix] = []
    for i in range(n):
        for j in range(n):
            units.append(tuple(tuple(F(1) if (r, c) == (i, j) else F(0) for c in range(n)) for r in range(n)))
    columns = [_flatten(_sub(_mm(e, a), _mm(a, e))) for e in units]
    equations = [list(row) for row in zip(*columns)]
    return n * n - _rank(equations)


def _center_dimension(basis: Sequence[Matrix]) -> int:
    if not basis:
        return 0
    n = len(basis[0])
    equations: List[List[F]] = []
    for b in basis:
        columns = [_flatten(_sub(_mm(e, b), _mm(b, e))) for e in basis]
        for k in range(n * n):
            equations.append([columns[j][k] for j in range(len(basis))])
    return len(basis) - _rank(equations)


def _matrix_strings(a: Matrix) -> List[List[str]]:
    return [[str(x) for x in row] for row in a]


# ---------------------------------------------------------------------------
# Exact local and doubled data
# ---------------------------------------------------------------------------

I2 = _eye(2)
Z2 = _zero(2)
J: Matrix = ((F(0), F(-1)), (F(1), F(0)))
S0: Matrix = ((F(1), F(0)), (F(0), F(-1)))
SU: Matrix = ((F(-7, 25), F(24, 25)), (F(24, 25), F(7, 25)))
R: Matrix = _mm(SU, S0)
R_INV: Matrix = _mm(S0, SU)

I4 = _eye(4)
Z4 = _zero(4)
P_PLUS: Matrix = _block(I2, Z2, Z2, Z2)
P_MINUS: Matrix = _block(Z2, Z2, Z2, I2)
D0: Matrix = _block(Z2, S0, S0, Z2)
DU: Matrix = _block(Z2, SU, SU, Z2)
R_OR: Matrix = _add(
    _mm(_mm(_mm(P_PLUS, DU), D0), P_PLUS),
    _mm(_mm(_mm(P_MINUS, D0), DU), P_MINUS),
)
J_OR: Matrix = _scale(F(1, 24), _add(_scale(F(25), R_OR), _scale(F(7), I4)))


# ---------------------------------------------------------------------------
# Exact theorem checks
# ---------------------------------------------------------------------------


def check_T_local_J_and_reflection_obstruction() -> Dict[str, object]:
    fails: List[str] = []
    expected_R = ((F(-7, 25), F(-24, 25)), (F(24, 25), F(-7, 25)))
    recovered_J = _scale(F(1, 24), _add(_scale(F(25), R), _scale(F(7), I2)))
    if R != expected_R:
        fails.append("R matrix mismatch")
    if recovered_J != J:
        fails.append("polynomial J recovery failed")
    if _mm(J, J) != _scale(F(-1), I2):
        fails.append("J^2 != -I")
    for label, s in (("S0", S0), ("Su", SU)):
        if _mm(s, J) != _scale(F(-1), _mm(J, s)):
            fails.append(f"{label} must anticommute with J")
        if _mm(_mm(s, J), s) != _scale(F(-1), J):
            fails.append(f"{label} must conjugate J to -J")
    if _mm(R, J) != _mm(J, R):
        fails.append("R must commute with J")
    return _result(
        "T_local_J_and_reflection_obstruction",
        "The exact two-exchange loop still gives J=(25R+7I)/24 and J^2=-I. But each individual exchange is orientation-reversing: S0 J S0 = Su J Su = -J. Therefore neither exchange can be an ordinary complex-linear endomorphism of one fixed oriented carrier.",
        {
            "S0": _matrix_strings(S0),
            "Su": _matrix_strings(SU),
            "R": _matrix_strings(R),
            "J": _matrix_strings(J),
            "S0_conjugates_J_to_minus_J": True,
            "Su_conjugates_J_to_minus_J": True,
            "R_commutes_with_J": True,
        },
        fails,
        dependencies=("T_two_exchange_gate_and_algebraic_J",),
        negative_controls=("treat each reflection as complex-linear on one sheet", "infer centrality from J in Alg_R(R) alone"),
    )


def check_T_undoubled_full_algebra_is_M2R() -> Dict[str, object]:
    fails: List[str] = []
    basis = _algebra_closure((I2, S0, SU))
    dim = len(basis)
    centre_dim = _center_dimension(basis)
    if dim != 4:
        fails.append(f"undoubled algebra dimension must be 4, got {dim}")
    if centre_dim != 1:
        fails.append(f"undoubled centre dimension must be 1, got {centre_dim}")
    if _mm(J, S0) == _mm(S0, J):
        fails.append("J must not be central in the undoubled algebra")
    # Direct centre solution: commute with S0 forces off-diagonals zero; commute
    # with J then forces equal diagonal entries.
    a, b, c, d = F(2), F(0), F(0), F(2)
    scalar_control: Matrix = ((a, b), (c, d))
    if _mm(scalar_control, S0) != _mm(S0, scalar_control) or _mm(scalar_control, J) != _mm(J, scalar_control):
        fails.append("scalar centre control malformed")
    return _result(
        "T_undoubled_full_algebra_is_M2R",
        "The real algebra generated by the two reflections is all of M_2(R). Its centre is R I. The local square-minus-one matrix J belongs to that algebra but is not central. Any proof that places S0, Su, and J in one ungraded endomorphism algebra and then calls J central is false.",
        {
            "generated_dimension": dim,
            "ambient_M2R_dimension": 4,
            "centre_dimension": centre_dim,
            "J_central": False,
            "algebra_identification": "M_2(R)",
        },
        fails,
        dependencies=("T_local_J_and_reflection_obstruction",),
        negative_controls=("ungraded generator completeness", "central-J assertion in Alg_R{S0,Su}"),
    )


def check_T_even_algebra_is_complex_line() -> Dict[str, object]:
    fails: List[str] = []
    basis = _algebra_closure((I2, R))
    if len(basis) != 2:
        fails.append(f"even algebra dimension must be 2, got {len(basis)}")
    if _rank([_flatten(I2), _flatten(J)]) != 2:
        fails.append("I,J must be independent")
    if _mm(J, J) != _scale(F(-1), I2):
        fails.append("complex-line relation failed")
    if any(_mm(x, J) != _mm(J, x) for x in basis):
        fails.append("J must be central in the even algebra")
    return _result(
        "T_even_algebra_is_complex_line",
        "The orientation-preserving algebra generated by R is exactly span_R{I,J}, hence a copy of C. J is central there. The two reflections sit in the odd normalizer and act by complex conjugation, S(aI+bJ)S^{-1}=aI-bJ.",
        {
            "even_dimension": len(basis),
            "basis": ["I", "J"],
            "identification": "C as a real algebra",
            "J_central_in_even_algebra": True,
            "reflection_action": "complex conjugation",
        },
        fails,
        dependencies=("T_undoubled_full_algebra_is_M2R",),
        negative_controls=("include odd reflections in the complex-linear algebra",),
    )


def check_T_orientation_double_cover_naturality() -> Dict[str, object]:
    fails: List[str] = []
    expected_R_OR = _block(R, Z2, Z2, R_INV)
    expected_J_OR = _block(J, Z2, Z2, _scale(F(-1), J))
    if R_OR != expected_R_OR:
        fails.append("oriented loop must be diag(R,R^-1)")
    if J_OR != expected_J_OR:
        fails.append("oriented J must be diag(J,-J)")
    if _mm(J_OR, J_OR) != _scale(F(-1), I4):
        fails.append("J_or^2 != -I4")
    for label, g in (("P+", P_PLUS), ("P-", P_MINUS), ("D0", D0), ("Du", DU)):
        if _mm(J_OR, g) != _mm(g, J_OR):
            fails.append(f"J_or must commute with {label}")
    # The sheet-changing maps are orthogonal and involutive.
    for label, g in (("D0", D0), ("Du", DU)):
        if _mm(g, g) != I4:
            fails.append(f"{label} must be involutive")
        if _mm(_transpose(g), g) != I4:
            fails.append(f"{label} must be orthogonal")
    return _result(
        "T_orientation_double_cover_naturality",
        "The ordered pair of exchanges defines two conjugate orientation sheets. The plus sheet carries R=Su S0 and J; the minus sheet carries R^{-1}=S0 Su and -J. With J_or=diag(J,-J), both exchanges become sheet-changing complex-linear morphisms: J_or D0=D0 J_or and J_or Du=Du J_or. Their individual anticommutation on one sheet has become ordinary naturality on the double cover.",
        {
            "P_plus": _matrix_strings(P_PLUS),
            "P_minus": _matrix_strings(P_MINUS),
            "D0": _matrix_strings(D0),
            "Du": _matrix_strings(DU),
            "R_oriented": _matrix_strings(R_OR),
            "J_oriented": _matrix_strings(J_OR),
            "sheet_plus_orientation": "J",
            "sheet_minus_orientation": "-J",
            "exchanges_complex_linear_on_cover": True,
        },
        fails,
        dependencies=("T_even_algebra_is_complex_line",),
        premises=("ORIENTATION_SHEET_TYPING",),
        negative_controls=("use diag(R,R) instead of diag(R,R^-1)", "collapse conjugate sheets before typing exchanges"),
    )


def check_T_oriented_linking_algebra_is_M2C() -> Dict[str, object]:
    fails: List[str] = []
    generators = (I4, P_PLUS, P_MINUS, D0, DU)
    basis = _algebra_closure(generators)
    generated_dim = len(basis)
    commutant_dim = _commutant_dimension(J_OR)
    centre_dim = _center_dimension(basis)
    if generated_dim != 8:
        fails.append(f"oriented linking algebra dimension must be 8, got {generated_dim}")
    if commutant_dim != 8:
        fails.append(f"commutant dimension must be 8, got {commutant_dim}")
    if any(_mm(x, J_OR) != _mm(J_OR, x) for x in basis):
        fails.append("generated algebra must lie in commutant of J_or")
    if generated_dim != commutant_dim:
        fails.append("generated algebra must equal full complex-linear commutant")
    if centre_dim != 2:
        fails.append(f"oriented centre dimension must be 2, got {centre_dim}")
    if _rank([_flatten(I4), _flatten(J_OR)]) != 2:
        fails.append("I4,J_or must be independent central elements")
    # *-closure under real transpose.
    for x in basis:
        xt = _transpose(x)
        if _rank([_flatten(b) for b in basis] + [_flatten(xt)]) != generated_dim:
            fails.append("generated algebra must be transpose-closed")
            break
    return _result(
        "T_oriented_linking_algebra_is_M2C",
        "The real algebra generated by the two object units and the two sheet-changing exchanges has dimension eight. Every generator commutes with J_or, and the full commutant of J_or in M_4(R) also has dimension eight. Therefore the generated linking algebra is End_C(C^2) ~= M_2(C), viewed as a real *-algebra. Its centre is span_R{I4,J_or} ~= C. Elementary generator completeness is exact on this oriented envelope.",
        {
            "generated_dimension": generated_dim,
            "commutant_dimension": commutant_dim,
            "centre_dimension": centre_dim,
            "central_basis": ["I4", "J_or"],
            "transpose_closed": True,
            "algebra_identification": "M_2(C) viewed over R",
            "elementary_generator_completeness": True,
        },
        fails,
        dependencies=("T_orientation_double_cover_naturality",),
        premises=("ORIENTATION_SHEET_TYPING",),
        negative_controls=("omit object projections", "identify the linking algebra with undoubled M2(R)"),
    )


# ---------------------------------------------------------------------------
# Network orientability
# ---------------------------------------------------------------------------


def solve_orientation_signs(
    vertices: Sequence[str],
    edges: Sequence[Tuple[str, str, int]],
) -> Dict[str, object]:
    """Solve s_target = epsilon * s_source on a finite parity graph."""
    allowed = {1, -1}
    failures: List[str] = []
    verts = list(dict.fromkeys(vertices))
    vset = set(verts)
    for u, v, eps in edges:
        if u not in vset or v not in vset:
            failures.append(f"edge {u}->{v} uses unknown vertex")
        if eps not in allowed:
            failures.append(f"edge {u}->{v} has invalid parity {eps}")
    if failures:
        return {"orientable": False, "signs": {}, "failures": failures}

    adjacency: Dict[str, List[Tuple[str, int]]] = {v: [] for v in verts}
    for u, v, eps in edges:
        adjacency[u].append((v, eps))
        adjacency[v].append((u, eps))

    signs: Dict[str, int] = {}
    contradiction: Optional[Tuple[str, str, int, int, int]] = None
    for root in verts:
        if root in signs:
            continue
        signs[root] = 1
        todo = [root]
        while todo and contradiction is None:
            u = todo.pop()
            for v, eps in adjacency[u]:
                expected = eps * signs[u]
                if v not in signs:
                    signs[v] = expected
                    todo.append(v)
                elif signs[v] != expected:
                    contradiction = (u, v, eps, signs[u], signs[v])
                    break
    if contradiction is not None:
        u, v, eps, su, sv = contradiction
        return {
            "orientable": False,
            "signs": signs,
            "failures": [f"parity contradiction on {u}->{v}: {sv} != {eps}*{su}"],
        }
    return {"orientable": True, "signs": signs, "failures": []}


def orientation_double_cover_graph(
    vertices: Sequence[str],
    edges: Sequence[Tuple[str, str, int]],
) -> Dict[str, object]:
    cover_vertices = [(v, s) for v in vertices for s in (1, -1)]
    cover_edges = []
    for u, v, eps in edges:
        for s in (1, -1):
            cover_edges.append(((u, s), (v, eps * s), 1))
    return {"vertices": cover_vertices, "edges": cover_edges}


def check_T_orientation_parity_cocycle_criterion() -> Dict[str, object]:
    fails: List[str] = []
    orientable_edges = (("A", "B", -1), ("B", "C", -1), ("C", "A", 1))
    nonorientable_edges = (("A", "B", -1), ("B", "C", 1), ("C", "A", 1))
    good = solve_orientation_signs(("A", "B", "C"), orientable_edges)
    bad = solve_orientation_signs(("A", "B", "C"), nonorientable_edges)
    if not good["orientable"]:
        fails.append("even-parity cycle must orient")
    if bad["orientable"]:
        fails.append("odd-parity cycle must not orient")
    signs = good.get("signs", {})
    for u, v, eps in orientable_edges:
        if signs[v] != eps * signs[u]:
            fails.append("returned sign assignment violates an edge")
    return _result(
        "T_orientation_parity_cocycle_criterion",
        "For a network of local square-minus-one carriers, a generating morphism has parity epsilon=+1 when it is complex-linear and epsilon=-1 when it reverses orientation. A global choice of signs s_v making every generator complex-linear exists exactly when the product of edge parities around every cycle is +1. Orientation synchronization is therefore a finite Z2-cocycle problem, not an untyped global premise.",
        {
            "orientable_control": good,
            "nonorientable_control": bad,
            "criterion": "product of parities on every cycle is +1",
        },
        fails,
        dependencies=("T_orientation_double_cover_naturality",),
        negative_controls=("odd-parity closed loop", "orientation-sign assignment by fiat"),
    )


def check_T_double_cover_always_orients() -> Dict[str, object]:
    fails: List[str] = []
    base_vertices = ("A", "B", "C")
    base_edges = (("A", "B", -1), ("B", "C", 1), ("C", "A", 1))
    base = solve_orientation_signs(base_vertices, base_edges)
    cover = orientation_double_cover_graph(base_vertices, base_edges)
    cover_names = [f"{v}:{s:+d}" for v, s in cover["vertices"]]  # type: ignore[index]
    cover_edges_named = [
        (f"{u[0]}:{u[1]:+d}", f"{v[0]}:{v[1]:+d}", eps)
        for u, v, eps in cover["edges"]  # type: ignore[index]
    ]
    covered = solve_orientation_signs(cover_names, cover_edges_named)
    if base["orientable"]:
        fails.append("base negative control must be nonorientable")
    if not covered["orientable"]:
        fails.append("orientation double cover must be orientable")
    return _result(
        "T_double_cover_always_orients",
        "Every finite parity network has a canonical orientation double cover: an edge of parity epsilon sends (v,s) to (w,epsilon s). All lifted edges are even relative to the sheet labels. The cover therefore carries a natural complex orientation even when the base network has an odd parity loop and no single-sheet complex scalar.",
        {
            "base_orientable": base["orientable"],
            "cover_vertex_count": len(cover_names),
            "cover_edge_count": len(cover_edges_named),
            "cover_orientable": covered["orientable"],
        },
        fails,
        dependencies=("T_orientation_parity_cocycle_criterion",),
        negative_controls=("force a sign choice on a nonorientable base",),
    )


# ---------------------------------------------------------------------------
# Process typing and dependency contract
# ---------------------------------------------------------------------------


def check_T_odd_fixed_sheet_map_not_CP() -> Dict[str, object]:
    fails: List[str] = []
    # The Choi matrix of transpose on M2(C) is the 4x4 swap matrix.
    choi_transpose: Matrix = (
        (F(1), F(0), F(0), F(0)),
        (F(0), F(0), F(1), F(0)),
        (F(0), F(1), F(0), F(0)),
        (F(0), F(0), F(0), F(1)),
    )
    psi_minus: Vector = (F(0), F(1), F(-1), F(0))
    q = sum(psi_minus[i] * _mv(choi_transpose, psi_minus)[i] for i in range(4))
    if q != F(-2):
        fails.append(f"transpose Choi negative control expected -2, got {q}")
    if _mm(choi_transpose, choi_transpose) != I4:
        fails.append("swap Choi control must square to identity")
    return _result(
        "T_odd_fixed_sheet_map_not_CP",
        "Collapsing an odd exchange to an endomorphism of one fixed complex sheet makes it conjugate-linear. On density matrices its canonical linear shadow is transpose. The Choi matrix of transpose is the swap operator and has expectation -2 on the antisymmetric vector. It is not completely positive. Odd exchanges must therefore be typed as sheet-changing/semilinear symmetries, not as ordinary local CPTP channels on a fixed complex system.",
        {
            "choi_transpose": _matrix_strings(choi_transpose),
            "antisymmetric_vector": [str(x) for x in psi_minus],
            "negative_expectation": str(q),
            "transpose_CP": False,
            "sheet_changing_typing_required": True,
        },
        fails,
        dependencies=("T_orientation_double_cover_naturality",),
        negative_controls=("treat reflection as a fixed-sheet quantum channel",),
    )


# Local mirror of the banked Ruling-3 antecedent inventory.  Canonical source:
# apf._hfc_345_contracts.CENTRAL_J_REQUIRED_GATES (v24.3.432, commit 8360a45),
# pinned set-exactly by the banked check_T_central_j_gate_contract.  Any edit
# here that diverges from the banked inventory fails
# check_T_graded_generator_dependency_contract when the bank tree is reachable.
CENTRAL_J_REQUIRED_GATES: Tuple[str, ...] = (
    "GENERATOR_COMPLETENESS",
    "NATURALITY",
    "ORIENTATION_SYNCHRONIZATION",
    "T_LOCAL_J",
)

# Retired gate names.  Their appearance anywhere in the live graph is a
# contract failure: the first is the ungraded-completeness error this packet
# refutes; the second and third were this packet's own pre-fortification
# renames of the banked gates (cold audit 2026-07-21, MAJOR-3); the second is
# additionally mathematically vacuous as a gate (the canonical double cover
# always exists -- realization, not existence, is the premise).
FORBIDDEN_GATE_NAMES: Tuple[str, ...] = (
    "UNRESTRICTED_GENERATOR_COMPLETENESS",
    "GLOBAL_PARITY_COCYCLE_OR_DOUBLE_COVER",
    "EVEN_GENERATOR_COMPLETENESS",
)

# What this packet contributes to each banked gate: executable semantics at
# the elementary carrier.  Semantics, never discharge -- every gate below
# remains a physical/categorical premise at network scale (Ruling 3 stands).
GATE_SEMANTICS: Dict[str, str] = {
    "ORIENTATION_SYNCHRONIZATION": (
        "Executable content: the finite Z2 parity-cocycle criterion "
        "(T_orientation_parity_cocycle_criterion) and the canonical "
        "double-cover construction (T_orientation_double_cover_naturality, "
        "T_double_cover_always_orients).  Satisfied when the realized "
        "network's parity cocycle is trivial, or when the interface realizes "
        "the canonical orientation double cover (ORIENTATION_COVER_REALIZED, "
        "physical) with odd morphisms sheet-typed "
        "(ORIENTATION_SHEET_TYPING).  Remains a physical premise."
    ),
    "GENERATOR_COMPLETENESS": (
        "Typing: EVEN (complex-linear) generator completeness of the "
        "represented category -- never completeness of the full real "
        "semilinear normalizer, which is refuted here "
        "(T_undoubled_full_algebra_is_M2R).  The elementary shadow is "
        "computed exactly (T_oriented_linking_algebra_is_M2C); the "
        "network-scale premise remains physical/categorical."
    ),
    "NATURALITY": (
        "Elementary instance: J_or commutes with both lifted exchanges and "
        "both object units (T_orientation_double_cover_naturality).  The "
        "network-scale premise remains physical."
    ),
    "T_LOCAL_J": (
        "The banked conditional theorem (v24.3.432 hfc_345_closure): the "
        "13-leaf physical package gives exact R and J=(25R+7I)/24."
    ),
}

DEPENDENCY_GRAPH: Dict[str, Tuple[str, ...]] = {
    "T_LOCAL_J": ("HFC_345_PHYSICAL_PACKAGE",),
    "T_REFLECTION_PARITY": ("T_LOCAL_J",),
    "T_ORIENTATION_DOUBLE_COVER": ("T_REFLECTION_PARITY",),
    "T_ELEMENTARY_M2C_LINKING": ("T_ORIENTATION_DOUBLE_COVER",),
    # The banked Ruling-3 antecedent, set-exact against
    # apf._hfc_345_contracts.CENTRAL_J_REQUIRED_GATES.  Never less.
    "T_CENTRAL_J": (
        "T_LOCAL_J",
        "NATURALITY",
        "ORIENTATION_SYNCHRONIZATION",
        "GENERATOR_COMPLETENESS",
    ),
    # Executable semantics of the synchronization gate: it is carried by the
    # realization-typed physical premise (the interface realizes the cover)
    # plus sheet typing of the odd morphisms.  The trivial-cocycle branch is
    # the degenerate case in which the realized cover splits.
    "ORIENTATION_SYNCHRONIZATION": (
        "ORIENTATION_COVER_REALIZED",
        "ORIENTATION_SHEET_TYPING",
    ),
    "T_POSITIVE_REAL_CSTAR": ("POSITIVE_STATE_EFFECT_SOUNDNESS",),
    "T_COMPLEX_QUANTUM_CORE": ("T_CENTRAL_J", "T_POSITIVE_REAL_CSTAR"),
    "T_BORN_CP_COMPOSITES": (
        "T_COMPLEX_QUANTUM_CORE",
        "WEIGHTED_STATE_EFFECT_IDENTIFICATION",
        "INSTRUMENT_BRANCH_SOUNDNESS",
        "COMPOSITE_EXTENSION_SOUNDNESS",
    ),
}


def _find_banked_central_j_gates() -> Tuple[Optional[Tuple[str, ...]], str]:
    """Locate the banked ``apf._hfc_345_contracts`` inventory if reachable.

    Returns ``(gates, source)`` on success and ``(None, reason)`` when the
    bank tree is not reachable (standalone packet run).  The contracts file is
    loaded by file path so the bank's ``apf/__init__`` is never executed."""
    candidates: List[Path] = []
    env_root = os.environ.get("APF_BANK_ROOT")
    if env_root:
        candidates.append(Path(env_root) / "apf" / "_hfc_345_contracts.py")
    try:
        spec = importlib.util.find_spec("apf")
        if spec is not None and spec.submodule_search_locations:
            for loc in spec.submodule_search_locations:
                candidates.append(Path(loc) / "_hfc_345_contracts.py")
    except (ImportError, ValueError):
        pass
    for path in candidates:
        try:
            if not path.is_file():
                continue
            mod_spec = importlib.util.spec_from_file_location(
                "_banked_hfc_345_contracts_probe", path
            )
            if mod_spec is None or mod_spec.loader is None:
                continue
            mod = importlib.util.module_from_spec(mod_spec)
            mod_spec.loader.exec_module(mod)
            gates = tuple(str(g) for g in mod.CENTRAL_J_REQUIRED_GATES)
            return gates, str(path)
        except Exception as exc:  # pragma: no cover - defensive
            return None, f"banked contracts load failed at {path}: {exc}"
    return None, "banked apf._hfc_345_contracts not reachable (standalone run)"


def _central_j_drift(graph: Mapping[str, Sequence[str]]) -> List[str]:
    """Set-exact drift detector for the Ruling-3 central-J antecedent."""
    fails: List[str] = []
    live = tuple(sorted(graph.get("T_CENTRAL_J", ())))
    expected = tuple(sorted(CENTRAL_J_REQUIRED_GATES))
    if live != expected:
        fails.append(
            f"central-J antecedent drift: live {live} != required {expected}"
        )
    for name in FORBIDDEN_GATE_NAMES:
        if name in _all_nodes(graph):
            fails.append(f"retired gate name present: {name}")
    return fails


def _all_nodes(graph: Mapping[str, Sequence[str]]) -> set[str]:
    return set(graph) | {d for deps in graph.values() for d in deps}


def _cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    nodes = _all_nodes(graph)
    state = {n: 0 for n in nodes}
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


def check_T_graded_generator_dependency_contract() -> Dict[str, object]:
    fails: List[str] = []
    cyc = _cycle(DEPENDENCY_GRAPH)
    if cyc is not None:
        fails.append(f"dependency cycle: {cyc}")
    local_deps = _deps(DEPENDENCY_GRAPH, "T_LOCAL_J")
    pos_deps = _deps(DEPENDENCY_GRAPH, "T_POSITIVE_REAL_CSTAR")
    if "T_POSITIVE_REAL_CSTAR" in local_deps or "POSITIVE_STATE_EFFECT_SOUNDNESS" in local_deps:
        fails.append("local orientation must not consume positivity")
    if "T_LOCAL_J" in pos_deps or "T_ELEMENTARY_M2C_LINKING" in pos_deps:
        fails.append("positive real C* branch must not consume orientation")

    # Ruling-3 gate discipline: the live central-J antecedent must equal the
    # local mirror set-exactly, and no retired gate name may appear.
    fails.extend(_central_j_drift(DEPENDENCY_GRAPH))
    sync_deps = _deps(DEPENDENCY_GRAPH, "ORIENTATION_SYNCHRONIZATION")
    if "ORIENTATION_COVER_REALIZED" not in sync_deps:
        fails.append(
            "orientation synchronization must carry the realization-typed "
            "physical premise ORIENTATION_COVER_REALIZED"
        )
    if "ORIENTATION_SHEET_TYPING" not in sync_deps:
        fails.append("orientation synchronization must carry sheet typing")
    for gate in CENTRAL_J_REQUIRED_GATES:
        if gate not in GATE_SEMANTICS:
            fails.append(f"gate {gate} has no recorded executable semantics")

    # Banked-inventory consistency: when the bank tree is reachable, the local
    # mirror must agree set-exactly with the machine-pinned banked inventory,
    # so any future antecedent drift fires on BOTH sides.
    banked_gates, banked_source = _find_banked_central_j_gates()
    banked_inventory_checked = banked_gates is not None
    if banked_gates is not None and tuple(sorted(banked_gates)) != tuple(
        sorted(CENTRAL_J_REQUIRED_GATES)
    ):
        fails.append(
            "central-J antecedent drift vs banked apf._hfc_345_contracts: "
            f"banked {tuple(sorted(banked_gates))} != local "
            f"{tuple(sorted(CENTRAL_J_REQUIRED_GATES))}"
        )

    # Mutations.
    mut_cycle = dict(DEPENDENCY_GRAPH)
    mut_cycle["T_LOCAL_J"] = (*mut_cycle["T_LOCAL_J"], "T_COMPLEX_QUANTUM_CORE")
    cycle_mutation_caught = _cycle(mut_cycle) is not None
    if not cycle_mutation_caught:
        fails.append("cycle mutation not caught")

    mut_ungraded = dict(DEPENDENCY_GRAPH)
    mut_ungraded["T_CENTRAL_J"] = (
        "T_LOCAL_J",
        "NATURALITY",
        "ORIENTATION_SYNCHRONIZATION",
        "UNRESTRICTED_GENERATOR_COMPLETENESS",
    )
    ungraded_mutation_caught = bool(_central_j_drift(mut_ungraded))
    if not ungraded_mutation_caught:
        fails.append("ungraded completeness mutation not caught")

    gate_deletion_mutations_caught = True
    for gate in CENTRAL_J_REQUIRED_GATES:
        mut_drop = dict(DEPENDENCY_GRAPH)
        mut_drop["T_CENTRAL_J"] = tuple(
            g for g in mut_drop["T_CENTRAL_J"] if g != gate
        )
        if not _central_j_drift(mut_drop):
            gate_deletion_mutations_caught = False
            fails.append(f"deletion of {gate} from T_CENTRAL_J not caught")

    mut_rename = dict(DEPENDENCY_GRAPH)
    mut_rename["T_CENTRAL_J"] = (
        "T_LOCAL_J",
        "NATURALITY",
        "GLOBAL_PARITY_COCYCLE_OR_DOUBLE_COVER",
        "GENERATOR_COMPLETENESS",
    )
    rename_mutation_caught = bool(_central_j_drift(mut_rename))
    if not rename_mutation_caught:
        fails.append("pre-fortification gate-rename mutation not caught")

    return _result(
        "T_graded_generator_dependency_contract",
        "The dependency contract keeps the banked Ruling-3 gate names: T_LOCAL_J + NATURALITY + ORIENTATION_SYNCHRONIZATION + GENERATOR_COMPLETENESS => T_CENTRAL_J, set-exactly, matching apf._hfc_345_contracts.CENTRAL_J_REQUIRED_GATES and the banked check_T_central_j_gate_contract. This packet supplies the EXECUTABLE SEMANTICS of those gates at the elementary carrier: the double-cover construction is the content of ORIENTATION_SYNCHRONIZATION (carried by the realization-typed physical premise ORIENTATION_COVER_REALIZED plus ORIENTATION_SHEET_TYPING), and GENERATOR_COMPLETENESS is typed as EVEN (complex-linear) generator completeness -- completeness of the full real semilinear normalizer is refuted. The reflection/double-cover branch and the positive-state/effect branch remain independent and meet only at the complex quantum core. Semantics, never discharge: every gate remains a physical/categorical premise at network scale, and Ruling 3 stands. FORTIFICATION 2026-07-21: this gate-naming resolution follows the cold audit's F3 recommendation (b) and is flagged for principal review.",
        {
            "graph": {k: list(v) for k, v in DEPENDENCY_GRAPH.items()},
            "cycle": cyc,
            "central_j_required_gates": sorted(CENTRAL_J_REQUIRED_GATES),
            "gate_semantics": dict(GATE_SEMANTICS),
            "forbidden_gate_names": list(FORBIDDEN_GATE_NAMES),
            "banked_inventory_checked": banked_inventory_checked,
            "banked_inventory_source": banked_source,
            "local_orientation_consumes_positivity": False,
            "positivity_consumes_orientation": False,
            "required_completeness": "GENERATOR_COMPLETENESS, typed as even (complex-linear) generator completeness",
            "orientation_cover_realization_premise": "ORIENTATION_COVER_REALIZED (physical, uncertified)",
            "cycle_mutation_caught": cycle_mutation_caught,
            "ungraded_mutation_caught": ungraded_mutation_caught,
            "gate_deletion_mutations_caught": gate_deletion_mutations_caught,
            "rename_mutation_caught": rename_mutation_caught,
        },
        fails,
        dependencies=tuple(DEPENDENCY_GRAPH),
        premises=("ORIENTATION_COVER_REALIZED", "ORIENTATION_SHEET_TYPING"),
        negative_controls=(
            "UNRESTRICTED_GENERATOR_COMPLETENESS",
            "GLOBAL_PARITY_COCYCLE_OR_DOUBLE_COVER (retired vacuous disjunctive gate)",
            "odd reflection counted as complex-linear generator",
            "positivity-orientation cycle",
            "central-J gate deletion or rename",
        ),
        epistemic="P_structural_instrument",
    )


CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_local_J_and_reflection_obstruction": check_T_local_J_and_reflection_obstruction,
    "T_undoubled_full_algebra_is_M2R": check_T_undoubled_full_algebra_is_M2R,
    "T_even_algebra_is_complex_line": check_T_even_algebra_is_complex_line,
    "T_orientation_double_cover_naturality": check_T_orientation_double_cover_naturality,
    "T_oriented_linking_algebra_is_M2C": check_T_oriented_linking_algebra_is_M2C,
    "T_orientation_parity_cocycle_criterion": check_T_orientation_parity_cocycle_criterion,
    "T_double_cover_always_orients": check_T_double_cover_always_orients,
    "T_odd_fixed_sheet_map_not_CP": check_T_odd_fixed_sheet_map_not_CP,
    "T_graded_generator_dependency_contract": check_T_graded_generator_dependency_contract,
}


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in CHECKS.items()}


def build_certificate(results: Optional[Mapping[str, Mapping[str, object]]] = None) -> GradedOrientationCertificate:
    rows = dict(results or run_all())

    def ok(name: str) -> bool:
        return bool(rows[name]["passed"])

    return GradedOrientationCertificate(
        local_J_exact=ok("T_local_J_and_reflection_obstruction"),
        reflection_obstruction_exposed=ok("T_local_J_and_reflection_obstruction"),
        local_full_algebra_is_M2R=ok("T_undoubled_full_algebra_is_M2R"),
        even_algebra_is_complex_line=ok("T_even_algebra_is_complex_line"),
        orientation_double_cover_natural=ok("T_orientation_double_cover_naturality"),
        oriented_linking_algebra_is_M2C=ok("T_oriented_linking_algebra_is_M2C"),
        parity_cocycle_criterion_exact=ok("T_orientation_parity_cocycle_criterion"),
        double_cover_orients_nonorientable_networks=ok("T_double_cover_always_orients"),
        odd_fixed_sheet_CP_control=ok("T_odd_fixed_sheet_map_not_CP"),
        dependency_contract_clean=ok("T_graded_generator_dependency_contract"),
        orientation_sheet_typing_premise_named=(
            "ORIENTATION_SHEET_TYPING"
            in _deps(DEPENDENCY_GRAPH, "ORIENTATION_SYNCHRONIZATION")
        ),
        orientation_cover_realized_premise_named=(
            "ORIENTATION_COVER_REALIZED"
            in _deps(DEPENDENCY_GRAPH, "ORIENTATION_SYNCHRONIZATION")
        ),
        physical_premises_certified=False,
    )


def register(registry: MutableMapping[str, Callable[[], Dict[str, object]]]) -> None:
    registry.update(CHECKS)


def main() -> int:
    results = run_all()
    cert = build_certificate(results)
    report = {
        "name": "APF_Graded_Orientation_Closure_v0.5",
        "passed": all(bool(row["passed"]) for row in results.values()),
        "n_checks": len(results),
        "n_passed": sum(bool(row["passed"]) for row in results.values()),
        "certificate": asdict(cert),
        "claim_boundary": {
            "J_central_in_undoubled_real_exchange_algebra": False,
            "undoubled_exchange_algebra": "M_2(R)",
            "even_algebra": "C",
            "oriented_linking_algebra": "M_2(C)",
            "central_j_gates": sorted(CENTRAL_J_REQUIRED_GATES),
            "orientation_synchronization_semantics": "trivial Z2 parity cocycle on the realized base, or ORIENTATION_COVER_REALIZED (physical) + ORIENTATION_SHEET_TYPING; the banked gate keeps its name and remains a physical premise (Ruling 3)",
            "required_generator_completeness": "GENERATOR_COMPLETENESS, typed as even (complex-linear) generator completeness",
            "physical_premises_certified": False,
        },
        "checks": list(results.values()),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
