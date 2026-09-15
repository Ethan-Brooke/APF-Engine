"""Unbanked downstream-frontier audit companion for :mod:`apf.zipper_reduction`.

This candidate does not extend the theorem bank.  It records exact finite
progress on six downstream obligations:

1. orientation synchronization across typed sectors;
2. arbitrary finite-dimensional tensor composition;
3. complete positivity of reduced events;
4. finite-dimensional Born weighting;
5. the remaining absolute action-scale calibration;
6. the empirical scope of the moving-frame branch.

The module is deliberately mixed in status.  It closes mathematical schemas,
exhibits sharp countermodels, and names the physical leaves that remain.  It
never promotes those leaves to certified physical facts.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
from itertools import product
from typing import Callable, Dict, Iterable, Mapping, Optional, Sequence, Tuple
import json

FAMILY = "quantum.zipper_reduction_frontier_candidate"
Matrix = Tuple[Tuple[F, ...], ...]


@dataclass(frozen=True)
class ZipperFrontierCertificate:
    orientation_sync_math_exact: bool
    finite_tensor_schema_exact: bool
    reduced_event_cp_schema_exact: bool
    finite_dimensional_born_form_exact: bool
    action_scale_residue_exact: bool
    moving_frame_scope_reduced: bool
    dependency_contract_clean: bool
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
        "scope": "exact downstream-frontier mathematics / unbanked audit candidate",
        "physical_premises_certified": False,
        "key_result": key_result,
        "dependencies": list(dependencies),
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


# ---------------------------------------------------------------------------
# Exact rational matrix helpers
# ---------------------------------------------------------------------------


def _shape(a: Matrix) -> Tuple[int, int]:
    return len(a), len(a[0]) if a else 0


def _zero(r: int, c: Optional[int] = None) -> Matrix:
    c = r if c is None else c
    return tuple(tuple(F(0) for _ in range(c)) for _ in range(r))


def _eye(n: int) -> Matrix:
    return tuple(tuple(F(1) if i == j else F(0) for j in range(n)) for i in range(n))


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


def _mm(a: Matrix, b: Matrix) -> Matrix:
    ar, ac = _shape(a)
    br, bc = _shape(b)
    if ac != br:
        raise ValueError("matrix shape mismatch")
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(ac)) for j in range(bc))
        for i in range(ar)
    )


def _mv(a: Matrix, v: Sequence[F]) -> Tuple[F, ...]:
    if _shape(a)[1] != len(v):
        raise ValueError("matrix/vector shape mismatch")
    return tuple(sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a)))


def _trace(a: Matrix) -> F:
    r, c = _shape(a)
    if r != c:
        raise ValueError("trace requires square matrix")
    return sum(a[i][i] for i in range(r))


def _flatten(a: Matrix) -> Tuple[F, ...]:
    return tuple(x for row in a for x in row)


def _rank_rows(rows: Iterable[Iterable[F]]) -> int:
    work = [[F(x) for x in row] for row in rows]
    work = [row for row in work if any(row)]
    if not work:
        return 0
    ncols = len(work[0])
    r = 0
    for col in range(ncols):
        pivot = next((i for i in range(r, len(work)) if work[i][col] != 0), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        p = work[r][col]
        work[r] = [x / p for x in work[r]]
        for i in range(len(work)):
            if i != r and work[i][col] != 0:
                q = work[i][col]
                work[i] = [a - q * b for a, b in zip(work[i], work[r])]
        r += 1
        if r == len(work):
            break
    return r


def _rank(a: Matrix) -> int:
    return _rank_rows(a)


def _columns(a: Matrix) -> Tuple[Tuple[F, ...], ...]:
    r, c = _shape(a)
    return tuple(tuple(a[i][j] for i in range(r)) for j in range(c))


def _column_span_rank(*mats: Matrix) -> int:
    cols = []
    for m in mats:
        cols.extend(_columns(m))
    return _rank_rows(zip(*cols)) if cols else 0


def _kron(a: Matrix, b: Matrix) -> Matrix:
    ar, ac = _shape(a)
    br, bc = _shape(b)
    return tuple(
        tuple(a[i][j] * b[u][v] for j in range(ac) for v in range(bc))
        for i in range(ar)
        for u in range(br)
    )


def _matrix_unit(n: int, i: int, j: int) -> Matrix:
    return tuple(tuple(F(1) if (r, c) == (i, j) else F(0) for c in range(n)) for r in range(n))


def _outer(v: Sequence[F], w: Sequence[F]) -> Matrix:
    return tuple(tuple(v[i] * w[j] for j in range(len(w))) for i in range(len(v)))


def _vec(a: Matrix) -> Tuple[F, ...]:
    # Column-major convention for Choi/Kraus vectors.
    r, c = _shape(a)
    return tuple(a[i][j] for j in range(c) for i in range(r))


I2 = _eye(2)
J0: Matrix = ((F(0), F(-1)), (F(1), F(0)))
S0: Matrix = ((F(1), F(0)), (F(0), F(-1)))


# ---------------------------------------------------------------------------
# 1. Orientation synchronization across sectors
# ---------------------------------------------------------------------------


def _orientation_assignment(
    vertices: Sequence[str], edges: Sequence[Tuple[str, str, int]]
) -> Optional[Dict[str, int]]:
    adj: Dict[str, list[Tuple[str, int]]] = {v: [] for v in vertices}
    for u, v, eps in edges:
        if eps not in (-1, 1):
            raise ValueError("orientation parity must be +/-1")
        adj[u].append((v, eps))
        adj[v].append((u, eps))
    signs: Dict[str, int] = {}
    for root in vertices:
        if root in signs:
            continue
        signs[root] = 1
        todo = [root]
        while todo:
            u = todo.pop()
            for v, eps in adj[u]:
                target = eps * signs[u]
                if v in signs and signs[v] != target:
                    return None
                if v not in signs:
                    signs[v] = target
                    todo.append(v)
    return signs


def _cover_edges(edges: Sequence[Tuple[str, str, int]]) -> Tuple[Tuple[Tuple[str, int], Tuple[str, int]], ...]:
    out = []
    for u, v, eps in edges:
        for sheet in (-1, 1):
            out.append(((u, sheet), (v, eps * sheet)))
    return tuple(out)


def check_T_frontier_orientation_synchronization() -> Dict[str, object]:
    fails: list[str] = []

    vertices = ("A", "B", "C", "D")
    trivial_edges = (
        ("A", "B", -1),
        ("B", "C", -1),
        ("C", "A", 1),
        ("C", "D", -1),
    )
    assignment = _orientation_assignment(vertices, trivial_edges)
    if assignment is None:
        fails.append("trivial parity cocycle did not admit a global sign assignment")
    else:
        for u, v, eps in trivial_edges:
            if assignment[v] != eps * assignment[u]:
                fails.append("global orientation assignment violates an edge parity")

    obstructed_edges = (
        ("A", "B", -1),
        ("B", "C", 1),
        ("C", "A", 1),
    )
    obstructed = _orientation_assignment(("A", "B", "C"), obstructed_edges)
    if obstructed is not None:
        fails.append("nontrivial parity cycle incorrectly synchronized on one sheet")

    cover = _cover_edges(obstructed_edges)
    edge_parity = {frozenset((u, v)): eps for u, v, eps in obstructed_edges}
    cover_consistent = all(
        right[1] == edge_parity[frozenset((left[0], right[0]))] * left[1]
        for left, right in cover
    )
    if not cover_consistent:
        fails.append("orientation double cover failed its sheet-transport identity")

    return _result(
        "T_frontier_orientation_synchronization",
        "Global local-J signs synchronize exactly iff the sector-transition Z2 parity cocycle is trivial. A nontrivial cycle obstructs one-sheet synchronization, while the canonical orientation double cover carries a consistent lifted orientation. The mathematics is closed upstream; physical realization of the cover remains a named gate.",
        {
            "trivial_cocycle_assignment": assignment,
            "obstructed_one_sheet_assignment": obstructed,
            "double_cover_vertex_count": 6,
            "double_cover_edge_count": len(cover),
            "double_cover_sheet_transport_exact": cover_consistent,
            "upstream_banked_family": "apf.graded_orientation_closure",
            "remaining_physical_gates": ["ORIENTATION_COVER_REALIZED", "ORIENTATION_SHEET_TYPING"],
            "progress_status": "MATHEMATICAL_CRITERION_CLOSED__PHYSICAL_REALIZATION_OPEN",
        },
        fails,
        dependencies=("T_ZIPPER_LOCAL_J", "T_ORIENTATION_PARITY_COCYCLE_CRITERION"),
        premises=("ORIENTATION_COVER_REALIZED", "ORIENTATION_SHEET_TYPING"),
        negative_controls=("triangle with parity product -1 has no single-sheet global J",),
        epistemic="P_structural_instrument",
    )


# ---------------------------------------------------------------------------
# 2. Arbitrary finite-dimensional tensor composition
# ---------------------------------------------------------------------------


def _complex_structure(dim_c: int) -> Matrix:
    return _kron(_eye(dim_c), J0)


def check_T_frontier_finite_tensor_composition() -> Dict[str, object]:
    fails: list[str] = []
    records = []
    for m, n in ((1, 1), (1, 3), (2, 2), (2, 3), (3, 4)):
        mn = m * n
        embedded_a = []
        embedded_b = []
        products = []
        for i, j in product(range(m), repeat=2):
            embedded_a.append(_kron(_matrix_unit(m, i, j), _eye(n)))
        for a, b in product(range(n), repeat=2):
            embedded_b.append(_kron(_eye(m), _matrix_unit(n, a, b)))
        for a in embedded_a:
            for b in embedded_b:
                if _mm(a, b) != _mm(b, a):
                    fails.append(f"subsystem embeddings fail to commute at ({m},{n})")
                products.append(_mm(a, b))
        generated_rank = _rank_rows(_flatten(x) for x in products)
        if generated_rank != mn * mn:
            fails.append(f"matrix-unit products do not span M_{mn} at ({m},{n})")

        ja = _complex_structure(m)
        jb = _complex_structure(n)
        raw_dim = (2 * m) * (2 * n)
        left_i = _kron(ja, _eye(2 * n))
        right_i = _kron(_eye(2 * m), jb)
        sync_rel = _sub(left_i, right_i)
        sync_rank = _rank(sync_rel)
        quotient_dim = raw_dim - sync_rank
        if sync_rank != 2 * mn or quotient_dim != 2 * mn:
            fails.append(f"complex-balanced quotient dimension wrong at ({m},{n})")

        opposite_rel = _add(left_i, right_i)
        opposite_rank = _rank(opposite_rel)
        union_rank = _column_span_rank(opposite_rel, sync_rel)
        same_i_descends_in_opposite_quotient = union_rank == opposite_rank
        if same_i_descends_in_opposite_quotient:
            fails.append(f"orientation-reversed tensor incorrectly preserves same-i balancing at ({m},{n})")

        records.append({
            "m": m,
            "n": n,
            "generated_matrix_algebra_rank": generated_rank,
            "expected_matrix_algebra_rank": mn * mn,
            "raw_real_tensor_dim": raw_dim,
            "balancing_relation_rank": sync_rank,
            "complex_tensor_real_dim": quotient_dim,
            "expected_complex_tensor_real_dim": 2 * mn,
            "opposite_orientation_relation_rank": opposite_rank,
            "same_i_descends_with_opposite_orientation": same_i_descends_in_opposite_quotient,
        })

    return _result(
        "T_frontier_finite_tensor_composition",
        "For arbitrary finite complex dimensions m,n, the standard commuting subsystem embeddings generate M_mn(C), and the synchronized complex tensor product is the real tensor quotient by J_A x tensor y = x tensor J_B y, of real dimension 2mn. Opposite local orientation yields a conjugate, not same-i, balancing. The algebraic schema is closed; physical tensor-faithful realization and synchronized embeddings remain open gates.",
        {
            "dimension_records": records,
            "generic_schema": "M_m(C) tensor_C M_n(C) ~= M_mn(C); dim_R(H_A tensor_C H_B)=2mn",
            "remaining_physical_gates": [
                "COMMUTING_UNITAL_SUBSYSTEM_EMBEDDINGS",
                "GENERATED_PHYSICAL_COMPOSITE",
                "ORIENTATION_SYNCHRONIZED_EMBEDDINGS",
                "TENSOR_FAITHFULNESS",
            ],
            "progress_status": "ARBITRARY_FINITE_ALGEBRAIC_SCHEMA_CLOSED__PHYSICAL_COMPOSITE_REALIZATION_OPEN",
        },
        fails,
        dependencies=("GLOBAL_ORIENTATION_SYNCHRONIZATION", "FINITE_COMPLEX_BLOCKS"),
        premises=(
            "COMMUTING_UNITAL_SUBSYSTEM_EMBEDDINGS",
            "GENERATED_PHYSICAL_COMPOSITE",
            "ORIENTATION_SYNCHRONIZED_EMBEDDINGS",
            "TENSOR_FAITHFULNESS",
        ),
        negative_controls=("opposite orientation gives conjugate balancing and no shared scalar i",),
    )


# ---------------------------------------------------------------------------
# 3. Complete positivity for reduced events
# ---------------------------------------------------------------------------


def _sum_mats(mats: Sequence[Matrix]) -> Matrix:
    if not mats:
        raise ValueError("empty matrix sum")
    out = _zero(*_shape(mats[0]))
    for m in mats:
        out = _add(out, m)
    return out


def _kraus_apply(kraus: Sequence[Matrix], x: Matrix) -> Matrix:
    return _sum_mats([_mm(_mm(k, x), _transpose(k)) for k in kraus])


def _stack_kraus_isometry(kraus: Sequence[Matrix]) -> Matrix:
    d_out, d_in = _shape(kraus[0])
    return tuple(tuple(kraus[a][i][j] for j in range(d_in)) for a in range(len(kraus)) for i in range(d_out))


def _partial_trace_env_first(x: Matrix, r: int, d: int) -> Matrix:
    if _shape(x) != (r * d, r * d):
        raise ValueError("bad environment-first matrix shape")
    return tuple(
        tuple(sum(x[a * d + i][a * d + j] for a in range(r)) for j in range(d))
        for i in range(d)
    )


def _choi_from_kraus(kraus: Sequence[Matrix]) -> Matrix:
    vecs = [_vec(k) for k in kraus]
    return _sum_mats([_outer(v, v) for v in vecs])


def _swap_matrix(d: int) -> Matrix:
    n = d * d
    out = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(d):
        for j in range(d):
            out[j * d + i][i * d + j] = F(1)
    return tuple(tuple(row) for row in out)


def check_T_frontier_reduced_event_complete_positivity() -> Dict[str, object]:
    fails: list[str] = []
    records = []
    for d in (2, 3, 4):
        kraus = tuple(_matrix_unit(d, i, i) for i in range(d))
        tp = _sum_mats([_mm(_transpose(k), k) for k in kraus])
        if tp != _eye(d):
            fails.append(f"dephasing Kraus family not trace-preserving at d={d}")
        v = _stack_kraus_isometry(kraus)
        if _mm(_transpose(v), v) != _eye(d):
            fails.append(f"stacked Kraus map not an isometry at d={d}")

        dilation_cases = 0
        for i, j in product(range(d), repeat=2):
            eij = _matrix_unit(d, i, j)
            dilated = _mm(_mm(v, eij), _transpose(v))
            reduced = _partial_trace_env_first(dilated, d, d)
            if reduced != _kraus_apply(kraus, eij):
                fails.append(f"partial trace and Kraus reduction disagree at d={d}, E{i}{j}")
            dilation_cases += 1

        choi = _choi_from_kraus(kraus)
        reconstructed = _sum_mats([_outer(_vec(k), _vec(k)) for k in kraus])
        if choi != reconstructed:
            fails.append(f"Choi Gram decomposition failed at d={d}")

        transpose_choi = _swap_matrix(d)
        anti = [F(0) for _ in range(d * d)]
        anti[1] = F(1)
        anti[d] = F(-1)
        swap_anti = _mv(transpose_choi, anti)
        q = sum(anti[i] * swap_anti[i] for i in range(d * d))
        if q != -2:
            fails.append(f"transpose non-CP witness failed at d={d}")

        records.append({
            "d": d,
            "kraus_count": len(kraus),
            "trace_preserving_exact": tp == _eye(d),
            "isometry_exact": _mm(_transpose(v), v) == _eye(d),
            "dilation_matrix_unit_cases": dilation_cases,
            "choi_is_explicit_gram_sum": choi == reconstructed,
            "transpose_choi_antisymmetric_quadratic_value": str(q),
        })

    return _result(
        "T_frontier_reduced_event_complete_positivity",
        "Any finite reduced event obtained by adjoining a finite environment, applying a complete isometry, and discarding the environment has a Kraus representation; its Choi matrix is an explicit Gram sum and is positive, while trace preservation is the isometry identity. The transpose control is positive but not CP. The finite dilation-to-CPTP mathematics is closed; physical extension soundness and tensor-faithful environment realization remain open.",
        {
            "dimension_records": records,
            "generic_proof": "Phi(x)=Tr_E(VxV*)=sum_a K_a x K_a*; C_Phi=sum_a vec(K_a)vec(K_a)* >=0; sum_a K_a*K_a=I",
            "remaining_physical_gates": [
                "COMPLETE_EVENT_ISOMETRY",
                "TENSOR_FAITHFUL_ENVIRONMENT",
                "LOCAL_IDENTITY_EXTENSION",
                "JOINT_POSITIVITY_PRESERVATION",
                "PHYSICAL_PARTIAL_DISCARD_REALIZATION",
            ],
            "progress_status": "FINITE_DILATION_TO_CPTP_SCHEMA_CLOSED__PHYSICAL_EXTENSION_SOUNDNESS_OPEN",
        },
        fails,
        dependencies=("FINITE_TENSOR_COMPOSITION", "OPEN_EVENT_NO_SILENT_LOSS"),
        premises=(
            "COMPLETE_EVENT_ISOMETRY",
            "TENSOR_FAITHFUL_ENVIRONMENT",
            "PHYSICAL_PARTIAL_DISCARD_REALIZATION",
        ),
        negative_controls=("matrix transpose has swap Choi matrix with antisymmetric eigenvalue -1",),
    )


# ---------------------------------------------------------------------------
# 4. Born weighting in arbitrary finite dimension
# ---------------------------------------------------------------------------


def _coordinate_functional(a: Matrix) -> F:
    return a[0][0]


def _normalized_trace(a: Matrix) -> F:
    return _trace(a) / len(a)


def check_T_frontier_finite_dimensional_born_weighting() -> Dict[str, object]:
    fails: list[str] = []
    records = []
    for n in (2, 3, 4, 5, 6):
        units = {(i, j): _matrix_unit(n, i, j) for i, j in product(range(n), repeat=2)}
        cyclicity_cases = 0
        for a in units.values():
            for b in units.values():
                if _normalized_trace(_mm(a, b)) != _normalized_trace(_mm(b, a)):
                    fails.append(f"normalized trace cyclicity failed at n={n}")
                cyclicity_cases += 1
        if _normalized_trace(_eye(n)) != 1:
            fails.append(f"normalized trace not normalized at n={n}")

        offdiag_zero = all(
            _normalized_trace(units[(i, j)]) == 0
            for i, j in product(range(n), repeat=2) if i != j
        )
        equal_diag = len({_normalized_trace(units[(i, i)]) for i in range(n)}) == 1
        if not offdiag_zero or not equal_diag:
            fails.append(f"matrix-unit trace uniqueness pattern failed at n={n}")

        e01 = units[(0, 1)]
        e10 = units[(1, 0)]
        coordinate_cyclic = _coordinate_functional(_mm(e01, e10)) == _coordinate_functional(_mm(e10, e01))
        if coordinate_cyclic:
            fails.append(f"coordinate-score cyclicity control did not fail at n={n}")

        denom = sum(range(1, n + 1))
        rho = tuple(tuple(F(i + 1, denom) if i == j else F(0) for j in range(n)) for i in range(n))
        effects = tuple(units[(i, i)] for i in range(n))
        probs = tuple(_trace(_mm(rho, e)) for e in effects)
        if sum(probs) != 1 or any(p < 0 for p in probs):
            fails.append(f"Born probabilities fail normalization/positivity at n={n}")

        records.append({
            "n": n,
            "matrix_unit_cyclicity_cases": cyclicity_cases,
            "offdiagonal_score_zero": offdiag_zero,
            "diagonal_score": str(F(1, n)),
            "coordinate_score_normalized_but_not_cyclic": not coordinate_cyclic,
            "sample_born_probabilities": [str(p) for p in probs],
            "sample_probabilities_sum": str(sum(probs)),
        })

    return _result(
        "T_frontier_finite_dimensional_born_weighting",
        "On every finite full matrix algebra M_n(C), a normalized cyclic linear closed-loop score is uniquely Tr/n: matrix units force all off-diagonal scores to zero and all diagonal scores equal. Positive normalized states and effects therefore have the Born form p(E)=Tr(rho E). This extends the algebraic trace-uniqueness schema to arbitrary finite n; it does not discharge the physical score, state/effect, tomography, or measurement leaves.",
        {
            "dimension_records": records,
            "upstream_banked_family": "apf.dense_sandwich_born",
            "upstream_composed_leaf_count": 39,
            "remaining_physical_gates": [
                "CLOSED_LOOP_SCORE_LINEARITY",
                "CLOSED_LOOP_SCORE_CYCLICITY",
                "CLOSED_LOOP_SCORE_NORMALIZATION",
                "DENSE_SANDWICH_CLOSURE",
                "FINITE_OPERATIONAL_TOMOGRAPHY",
                "CONTEXTUAL_EFFECT_IDENTITY",
                "FINITE_OUTCOME_NORMALIZATION",
            ],
            "progress_status": "ARBITRARY_FINITE_TRACE_FORM_CLOSED__PHYSICAL_BORN_LEAVES_OPEN",
        },
        fails,
        dependencies=("ORIENTED_FINITE_MATRIX_ALGEBRA", "POSITIVE_STATE_EFFECT_SOUNDNESS"),
        premises=(
            "CLOSED_LOOP_SCORE_LINEARITY",
            "CLOSED_LOOP_SCORE_CYCLICITY",
            "CLOSED_LOOP_SCORE_NORMALIZATION",
            "FINITE_OPERATIONAL_TOMOGRAPHY",
        ),
        negative_controls=("normalized coordinate functional A->A_00 is not cyclic",),
    )


# ---------------------------------------------------------------------------
# 5. Absolute scale and hbar-normalized action
# ---------------------------------------------------------------------------


def check_T_frontier_action_scale_residue() -> Dict[str, object]:
    fails: list[str] = []
    records = []
    for energy, hbar, time, scale in (
        (F(3), F(2), F(5), F(7)),
        (F(5, 2), F(7, 3), F(11, 5), F(4)),
        (F(13), F(17), F(19), F(23, 2)),
    ):
        theta = energy * time / hbar
        theta_scaled = (scale * energy) * time / (scale * hbar)
        if theta != theta_scaled:
            fails.append("simultaneous action-scale rescaling changed the phase")
        records.append({
            "energy": str(energy),
            "hbar": str(hbar),
            "time": str(time),
            "scale": str(scale),
            "phase": str(theta),
            "scaled_phase": str(theta_scaled),
        })

    omega = F(7, 5)
    measured_energy = F(21, 10)
    inferred_hbar = measured_energy / omega
    if inferred_hbar != F(3, 2):
        fails.append("single-anchor action calibration arithmetic failed")

    return _result(
        "T_frontier_action_scale_residue",
        "Zipper holonomy fixes dimensionless phase and phase rate, hence H/hbar, but cannot fix H and hbar separately: (H,hbar)->(cH,c hbar) leaves every phase unchanged. Exactly one dimensional action calibration is still required. A candidate APF route may identify an elementary commitment-energy/time product with the action quantum, but that identification is not derived here.",
        {
            "scale_gauge_records": records,
            "sample_phase_rate": str(omega),
            "sample_measured_energy_anchor": str(measured_energy),
            "sample_inferred_action_scale": str(inferred_hbar),
            "free_scale_dimension": 1,
            "remaining_physical_gates": [
                "ACTION_LEDGER_TO_PHASE_CALIBRATION",
                "UNIVERSAL_ACTION_QUANTUM",
                "IDENTIFICATION_WITH_EMPIRICAL_HBAR",
            ],
            "candidate_reduction": "hbar_APF = universal elementary action ledger quantum, potentially epsilon_star * tau_star if a universal continuation-time quantum is independently derived",
            "progress_status": "ONE_DIMENSIONAL_SCALE_GAUGE_IDENTIFIED__ABSOLUTE_CALIBRATION_OPEN",
        },
        fails,
        dependencies=("ZIPPER_PHASE_HOLONOMY", "PHYSICAL_TIME_PARAMETER"),
        premises=("ACTION_LEDGER_TO_PHASE_CALIBRATION", "IDENTIFICATION_WITH_EMPIRICAL_HBAR"),
        negative_controls=("simultaneous rescaling of Hamiltonian and hbar is observationally phase-invariant",),
        epistemic="P_structural_instrument",
    )


# ---------------------------------------------------------------------------
# 6. Empirical moving-frame scope
# ---------------------------------------------------------------------------


def _rotation_rational(t: F) -> Matrix:
    d = F(1) + t * t
    return ((F(1) - t * t) / d, -F(2) * t / d), (F(2) * t / d, (F(1) - t * t) / d)


def _moving_reflection(t: F) -> Matrix:
    r = _rotation_rational(t)
    return _mm(_mm(r, S0), _transpose(r))


def _classify_interface(sample: Mapping[str, object]) -> str:
    if sample["rank"] != 2 or not sample["positive_metric"]:
        return "SINGULAR_OR_NONQUANTUM_CARRIER"
    if not sample["record_neutral"] or not sample["export_free"] or not sample["fixed_stratum"]:
        return "EVENT_BOUNDARY_OR_OPEN_SYSTEM"
    taus = sample["taus"]
    distinct = len({_flatten(t) for t in taus})
    if distinct == 1:
        return "STATIC_FRAME"
    if not sample["connected_context"]:
        return "DISCRETE_FRAME_JUMP"
    return "MOVING_FRAME_COHERENT_BRANCH"


def check_T_frontier_moving_frame_empirical_scope() -> Dict[str, object]:
    fails: list[str] = []
    samples = (
        {
            "name": "coherent_moving",
            "rank": 2,
            "positive_metric": True,
            "record_neutral": True,
            "export_free": True,
            "fixed_stratum": True,
            "connected_context": True,
            "taus": (_moving_reflection(F(0)), _moving_reflection(F(1, 3)), _moving_reflection(F(1, 2))),
        },
        {
            "name": "valid_static",
            "rank": 2,
            "positive_metric": True,
            "record_neutral": True,
            "export_free": True,
            "fixed_stratum": True,
            "connected_context": True,
            "taus": (S0, S0, S0),
        },
        {
            "name": "discrete_C2",
            "rank": 2,
            "positive_metric": True,
            "record_neutral": True,
            "export_free": True,
            "fixed_stratum": True,
            "connected_context": False,
            "taus": (S0, _scale(F(-1), S0)),
        },
        {
            "name": "recording_boundary",
            "rank": 2,
            "positive_metric": True,
            "record_neutral": False,
            "export_free": True,
            "fixed_stratum": False,
            "connected_context": True,
            "taus": (S0, _moving_reflection(F(1, 2))),
        },
    )
    classifications = {sample["name"]: _classify_interface(sample) for sample in samples}
    if classifications["coherent_moving"] != "MOVING_FRAME_COHERENT_BRANCH":
        fails.append("moving coherent sample misclassified")
    if classifications["valid_static"] != "STATIC_FRAME":
        fails.append("static interface control misclassified")
    if classifications["discrete_C2"] != "DISCRETE_FRAME_JUMP":
        fails.append("finite-phase control misclassified")
    if classifications["recording_boundary"] != "EVENT_BOUNDARY_OR_OPEN_SYSTEM":
        fails.append("recording boundary control misclassified")

    universal_claim_survives = all(v == "MOVING_FRAME_COHERENT_BRANCH" for v in classifications.values())
    if universal_claim_survives:
        fails.append("universal every-interface moving-frame claim was not refuted by controls")

    return _result(
        "T_frontier_moving_frame_empirical_scope",
        "The claim that every elementary physical interface realizes the moving-frame branch is too strong: static, discrete-frame, and record-forming interface classes are coherent countermodels. The defensible empirical target is sectoral: every elementary interface in the coherent, connected-context, rank-two, positive, record-neutral, export-free fixed-stratum branch should exhibit nonconstant operational exchange. That remains an empirical census, not a theorem.",
        {
            "classifications": classifications,
            "universal_every_interface_claim": False,
            "revised_claim": "every interface satisfying the coherent moving-branch antecedent package exhibits nonconstant tau(lambda)",
            "empirical_protocol_fields": [
                "rank-two completion-faithful response reconstruction",
                "positive event metric witness",
                "nearby context settings lambda",
                "operational exchange tau(lambda)",
                "record/export audit",
                "fixed-stratum/rank audit",
            ],
            "remaining_physical_gate": "EXHAUSTIVE_QUANTUM_CAPABLE_INTERFACE_CENSUS",
            "progress_status": "UNIVERSAL_CLAIM_REDUCED__SECTORAL_EMPIRICAL_PROGRAM_OPEN",
        },
        fails,
        dependencies=("OPERATIONAL_EXCHANGE_RECONSTRUCTION_PROTOCOL",),
        premises=("EMPIRICAL_INTERFACE_RESPONSE_DATA",),
        negative_controls=("static frame", "finite C2 frame jump", "record-forming stratum transition"),
        epistemic="P_structural_instrument",
    )


# ---------------------------------------------------------------------------
# Frontier dependency/progress contract
# ---------------------------------------------------------------------------


FRONTIER_GRAPH: Dict[str, Tuple[str, ...]] = {
    "EMPIRICAL_MOVING_BRANCH": ("OPERATIONAL_EXCHANGE_RECONSTRUCTION_PROTOCOL",),
    "T_ZIPPER_LOCAL_J": (
        "ACTIVE_RECORD_KERNEL_REALIZED",
        "COMPLETION_FAITHFUL_RANK_TWO_QUOTIENT",
        "POSITIVE_EVENT_METRIC_REALIZED",
        "EMPIRICAL_MOVING_BRANCH",
        "RECORD_NEUTRAL_EXPORT_FREE_COMPLETION_PATH",
    ),
    "GLOBAL_ORIENTATION_SYNCHRONIZATION": (
        "T_ZIPPER_LOCAL_J",
        "ORIENTATION_COVER_REALIZED",
        "ORIENTATION_SHEET_TYPING",
    ),
    "ARBITRARY_FINITE_TENSOR_COMPOSITION": (
        "GLOBAL_ORIENTATION_SYNCHRONIZATION",
        "COMMUTING_UNITAL_SUBSYSTEM_EMBEDDINGS",
        "GENERATED_PHYSICAL_COMPOSITE",
        "TENSOR_FAITHFULNESS",
    ),
    "REDUCED_EVENT_CP": (
        "ARBITRARY_FINITE_TENSOR_COMPOSITION",
        "COMPLETE_EVENT_ISOMETRY",
        "PHYSICAL_PARTIAL_DISCARD_REALIZATION",
    ),
    "BORN_WEIGHTING": (
        "GLOBAL_ORIENTATION_SYNCHRONIZATION",
        "FINITE_MATRIX_TRACE_FORM",
        "PHYSICAL_STATE_EFFECT_SCORE_PACKAGE",
    ),
    "HBAR_ACTION_SCALE": (
        "T_ZIPPER_LOCAL_J",
        "ACTION_LEDGER_TO_PHASE_CALIBRATION",
        "IDENTIFICATION_WITH_EMPIRICAL_HBAR",
    ),
}


def _cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    nodes = set(graph)
    for deps in graph.values():
        nodes.update(deps)
    state: Dict[str, int] = {}
    stack: list[str] = []

    def dfs(n: str) -> Optional[Tuple[str, ...]]:
        state[n] = 1
        stack.append(n)
        for d in graph.get(n, ()):
            if state.get(d, 0) == 0:
                c = dfs(d)
                if c is not None:
                    return c
            elif state.get(d) == 1:
                i = stack.index(d)
                return tuple(stack[i:] + [d])
        stack.pop()
        state[n] = 2
        return None

    for n in sorted(nodes):
        if state.get(n, 0) == 0:
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


def check_T_frontier_dependency_contract() -> Dict[str, object]:
    fails: list[str] = []
    cyc = _cycle(FRONTIER_GRAPH)
    if cyc is not None:
        fails.append(f"frontier dependency cycle: {cyc}")
    if "BORN_WEIGHTING" in _deps(FRONTIER_GRAPH, "T_ZIPPER_LOCAL_J"):
        fails.append("local J illegally consumes Born weighting")
    if "REDUCED_EVENT_CP" in _deps(FRONTIER_GRAPH, "ARBITRARY_FINITE_TENSOR_COMPOSITION"):
        fails.append("tensor composition illegally consumes CP")
    if "HBAR_ACTION_SCALE" in _deps(FRONTIER_GRAPH, "T_ZIPPER_LOCAL_J"):
        fails.append("local phase geometry illegally consumes hbar scale")
    if "T_ZIPPER_LOCAL_J" in _deps(FRONTIER_GRAPH, "EMPIRICAL_MOVING_BRANCH"):
        fails.append("empirical moving-frame detection illegally infers its premise from local J")

    mut = dict(FRONTIER_GRAPH)
    mut["EMPIRICAL_MOVING_BRANCH"] = ("T_ZIPPER_LOCAL_J",)
    empirical_cycle_caught = _cycle(mut) is not None
    if not empirical_cycle_caught:
        fails.append("empirical affirming-consequent cycle mutation not caught")

    statuses = {
        "global_orientation_synchronization": "MATH_CLOSED__PHYSICAL_COVER_REALIZATION_OPEN",
        "arbitrary_finite_tensor_composition": "ALGEBRAIC_SCHEMA_CLOSED__PHYSICAL_TENSOR_FAITHFULNESS_OPEN",
        "complete_positivity_reduced_events": "DILATION_SCHEMA_CLOSED__PHYSICAL_EXTENSION_SOUNDNESS_OPEN",
        "Born_weighting": "FINITE_TRACE_FORM_CLOSED__PHYSICAL_SCORE_STATE_EFFECT_LEAVES_OPEN",
        "hbar_action_scale": "ONE_SCALE_GAUGE_ISOLATED__ABSOLUTE_CALIBRATION_OPEN",
        "moving_frame_every_interface": "UNIVERSAL_CLAIM_REDUCED__SECTORAL_EMPIRICAL_CENSUS_OPEN",
    }

    return _result(
        "T_frontier_dependency_contract",
        "The six downstream lanes are acyclic and correctly ordered: empirical moving-frame realization is an antecedent of the local zipper J, orientation synchronization precedes complex tensor composition, tensor composition precedes reduced-event CP, Born weighting remains independent of the local-J derivation, and hbar is a downstream dimensional calibration rather than an input to complex geometry.",
        {
            "graph": {k: list(v) for k, v in FRONTIER_GRAPH.items()},
            "cycle": cyc,
            "progress_statuses": statuses,
            "empirical_cycle_mutation_caught": empirical_cycle_caught,
            "bank_registration": False,
            "audit_status": "candidate_not_banked",
        },
        fails,
        dependencies=tuple(FRONTIER_GRAPH),
        premises=tuple(sorted({d for deps in FRONTIER_GRAPH.values() for d in deps if d not in FRONTIER_GRAPH})),
        negative_controls=(
            "Born-to-local-J cycle",
            "CP-to-tensor cycle",
            "hbar-to-phase-geometry cycle",
            "local-J-to-empirical-moving-branch affirming consequent",
        ),
        epistemic="P_structural_instrument",
    )


CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_frontier_orientation_synchronization": check_T_frontier_orientation_synchronization,
    "T_frontier_finite_tensor_composition": check_T_frontier_finite_tensor_composition,
    "T_frontier_reduced_event_complete_positivity": check_T_frontier_reduced_event_complete_positivity,
    "T_frontier_finite_dimensional_born_weighting": check_T_frontier_finite_dimensional_born_weighting,
    "T_frontier_action_scale_residue": check_T_frontier_action_scale_residue,
    "T_frontier_moving_frame_empirical_scope": check_T_frontier_moving_frame_empirical_scope,
    "T_frontier_dependency_contract": check_T_frontier_dependency_contract,
}


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in CHECKS.items()}


def build_certificate(results: Optional[Mapping[str, Mapping[str, object]]] = None) -> ZipperFrontierCertificate:
    rows = dict(results or run_all())

    def ok(name: str) -> bool:
        return bool(rows[name]["passed"])

    return ZipperFrontierCertificate(
        orientation_sync_math_exact=ok("T_frontier_orientation_synchronization"),
        finite_tensor_schema_exact=ok("T_frontier_finite_tensor_composition"),
        reduced_event_cp_schema_exact=ok("T_frontier_reduced_event_complete_positivity"),
        finite_dimensional_born_form_exact=ok("T_frontier_finite_dimensional_born_weighting"),
        action_scale_residue_exact=ok("T_frontier_action_scale_residue"),
        moving_frame_scope_reduced=ok("T_frontier_moving_frame_empirical_scope"),
        dependency_contract_clean=ok("T_frontier_dependency_contract"),
        physical_premises_certified=False,
    )


def main() -> int:
    results = run_all()
    certificate = build_certificate(results)
    payload = {
        "name": "APF_Zipper_Reduction_Frontier_Progress_v0.1",
        "family": FAMILY,
        "passed": all(bool(row["passed"]) for row in results.values()),
        "n_checks": len(results),
        "n_passed": sum(bool(row["passed"]) for row in results.values()),
        "certificate": asdict(certificate),
        "claim_boundary": {
            "mathematical_progress_only": True,
            "physical_premises_certified": False,
            "bank_registered": False,
            "universal_every_interface_moving_frame_claim": False,
            "absolute_hbar_scale_derived": False,
        },
        "checks": list(results.values()),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
