"""Exact finite witnesses for the APF one-gate Held-holonomy route.

The module proves a reduction that replaces the physical premise
``CONNECTED_EFFECTIVE_HELD_SWEEP`` by one exact reversible Held automorphism
of infinite order.  It does not certify that the gate is physically realized.

Source concordance:
* the 3-4-5 projector geometry is the exact witness reproduced by
  ``reproduce_inline_345_commutator`` in ``apf.ijc_boolean_defender_bridge``;
* the two-dimensional first-jet carrier is the Paper 10 handoff;
* physical reflection/gate realization and carrier identification remain named;
* the executed infinite-order certificate is PORTED from the banked H3 battery
  (``T_held_connected_subgroup_so2``, ``_held_holonomy_groups.py``): the packet
  gate is the exact square of the banked cos=3/5 rotation,
  -7+24i = (3+4i)^2 = (2+i)^4.

Fortified 2026-07-20 carrying every finding of the blinded cold audit
(MAJOR-1 elliptic verifier gate; MAJOR-2 executed compactness failure
directions; MAJOR-3 named math-import registry + derived closure branch;
MAJOR-4 ported Gaussian-integer certificate + prior-art disclosure; minors
m1-m7).  Physical certification remains refused everywhere.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

FAMILY = "quantum.irrational_gate_held_holonomy"
Matrix2 = Tuple[Tuple[F, F], Tuple[F, F]]
Vector2 = Tuple[F, F]

# Evidence-strength parameters, PINNED (audit m4): every scanning check derives
# its count from the executed loop and asserts it equals the pin, so silently
# weakening a loop bound (mutations M11/M12) is caught.
EVIDENCE_STRENGTH = {
    "orbit_prefix_two_sided": 128,
    "power_scan_nonidentity": 256,
    "disk_orbit_prefix": 64,
    "fringe_scan_points": 256,
    "cover_resolutions": (16, 32, 64, 128, 256),
}

# Named load-bearing standard-mathematics imports of the circle-closure step
# (audit MAJOR-3).  Recorded machine-readably, consumed, NOT derived here.
# The first name is adopted from the banked bounded_orbit_positivity module.
NAMED_MATH_IMPORTS = (
    # bounded subgroup of GL(n,R) => its closure is a compact group
    "BOUNDED_SUBGROUP_COMPACT_CLOSURE_general_case",
    # compact subgroup conjugates into O(2) (averaging / John ellipsoid)
    "COMPACT_SUBGROUP_CONJUGATES_INTO_O2_averaging_John_ellipsoid",
    # the density/Kronecker step + the dim-2 classification: every proper
    # closed subgroup of SO(2) is finite cyclic, so an infinite closed
    # subgroup is the full circle
    "CLOSED_SUBGROUPS_OF_SO2_finite_cyclic_or_full_Kronecker_density",
)

# Integer traces of finite-order elements of a compact 2D oriented group.
FINITE_ORDER_INTEGER_TRACES = frozenset({F(-2), F(-1), F(0), F(1), F(2)})


@dataclass(frozen=True)
class OneGateCertificate:
    projector_pair_exact: bool
    reflection_product_exact: bool
    rational_trace_infinite_order: bool
    finite_precision_exactness_guard: bool
    compact_closure_circle: bool
    connected_sweep_not_required: bool
    orbit_mixture_disk: bool
    finite_resolution_cover: bool
    born_fringe: bool
    generator_closure: bool
    source_concordance_honest: bool
    physical_gate_realized: bool
    finite_resolution_interface_certified: bool = False
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
        "scope": "finite mathematical witness / physical-certificate reduction",
        "physical_premises_certified": False,
        "key_result": key_result,
        "dependencies": list(dependencies),
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


def _mm(a: Matrix2, b: Matrix2) -> Matrix2:
    return (
        (
            a[0][0] * b[0][0] + a[0][1] * b[1][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1],
        ),
        (
            a[1][0] * b[0][0] + a[1][1] * b[1][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1],
        ),
    )


def _mv(a: Matrix2, v: Vector2) -> Vector2:
    return (
        a[0][0] * v[0] + a[0][1] * v[1],
        a[1][0] * v[0] + a[1][1] * v[1],
    )


def _mt(a: Matrix2) -> Matrix2:
    return ((a[0][0], a[1][0]), (a[0][1], a[1][1]))


def _det(a: Matrix2) -> F:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def _trace(a: Matrix2) -> F:
    return a[0][0] + a[1][1]


def _eye() -> Matrix2:
    return ((F(1), F(0)), (F(0), F(1)))


def _sub(a: Matrix2, b: Matrix2) -> Matrix2:
    return (
        (a[0][0] - b[0][0], a[0][1] - b[0][1]),
        (a[1][0] - b[1][0], a[1][1] - b[1][1]),
    )


def _scale(s: F, a: Matrix2) -> Matrix2:
    return (
        (s * a[0][0], s * a[0][1]),
        (s * a[1][0], s * a[1][1]),
    )


def _eq(a: Matrix2, b: Matrix2) -> bool:
    return a == b


def _matrix_strings(a: Matrix2) -> List[List[str]]:
    return [[str(x) for x in row] for row in a]


def _vector_strings(v: Vector2) -> List[str]:
    return [str(x) for x in v]


def _projector(u: Vector2) -> Matrix2:
    norm = u[0] * u[0] + u[1] * u[1]
    if norm != 1:
        raise ValueError("projector input must be exactly unit")
    return ((u[0] * u[0], u[0] * u[1]), (u[1] * u[0], u[1] * u[1]))


def _reflection(p: Matrix2) -> Matrix2:
    return _sub(_scale(F(2), p), _eye())


def _dot(u: Vector2, v: Vector2) -> F:
    return u[0] * v[0] + u[1] * v[1]


def _cross(u: Vector2, v: Vector2) -> F:
    return u[0] * v[1] - u[1] * v[0]


def _norm2(v: Vector2) -> F:
    return _dot(v, v)


def _pow(a: Matrix2, n: int) -> Matrix2:
    if n < 0:
        raise ValueError("nonnegative powers only")
    out = _eye()
    base = a
    k = n
    while k:
        if k & 1:
            out = _mm(out, base)
        base = _mm(base, base)
        k >>= 1
    return out


def _orbit(a: Matrix2, seed: Vector2, n: int) -> List[Vector2]:
    pts: List[Vector2] = []
    v = seed
    for _ in range(n):
        pts.append(v)
        v = _mv(a, v)
    return pts


def _cyclic_cover(a: Matrix2, n: int) -> Dict[str, object]:
    """Order the exact rational orbit and certify the largest angular gap.

    High precision is used only to propose the cyclic order.  Exact rational
    cross products verify that every adjacent proposed gap lies in (0, pi).
    Exact dot products then determine each gap's cosine.
    """
    if n < 3:
        raise ValueError("at least three orbit points required")
    getcontext().prec = 90
    pts = _orbit(a, (F(1), F(0)), n)
    if len(set(pts)) != n:
        raise ValueError("orbit repeats inside requested finite prefix")

    # mpmath is a transitive dependency of sympy in the APF test environment.
    import mpmath as mp
    mp.mp.dps = 90
    indexed = []
    for i, (x, y) in enumerate(pts):
        ang = mp.atan2(mp.mpf(y.numerator) / y.denominator,
                       mp.mpf(x.numerator) / x.denominator)
        if ang < 0:
            ang += 2 * mp.pi
        indexed.append((ang, i, x, y))
    indexed.sort(key=lambda z: z[0])

    gaps: List[float] = []
    dots: List[F] = []
    crosses: List[F] = []
    pairs: List[Tuple[int, int]] = []
    for k in range(n):
        aa = indexed[k]
        bb = indexed[(k + 1) % n]
        gap = (bb[0] - aa[0]) % (2 * mp.pi)
        u = (aa[2], aa[3])
        v = (bb[2], bb[3])
        cr = _cross(u, v)
        dt = _dot(u, v)
        # Positive cross and positive dot certify a gap in (0, pi/2), which is
        # much stronger than needed and makes the numerical cyclic ordering safe.
        if cr <= 0:
            raise AssertionError(f"cyclic order exact cross failure at {aa[1]}->{bb[1]}")
        if dt <= 0:
            raise AssertionError(f"finite-cover adjacent gap not acute at {aa[1]}->{bb[1]}")
        gaps.append(float(gap))
        dots.append(dt)
        crosses.append(cr)
        pairs.append((aa[1], bb[1]))

    idx = max(range(n), key=lambda i: gaps[i])
    max_gap = gaps[idx]
    worst_dot = dots[idx]
    deficit = 1.0 - math.cos(max_gap / 2.0)
    return {
        "N": n,
        "max_gap_radians": max_gap,
        "max_gap_degrees": max_gap * 180.0 / math.pi,
        "radial_deficit_bound": deficit,
        "worst_pair": list(pairs[idx]),
        "worst_dot_exact": str(worst_dot),
        "min_adjacent_cross_float": min(float(x) for x in crosses),
        "all_points_exactly_unit": all(_norm2(p) == 1 for p in pts),
        "all_points_distinct": len(set(pts)) == n,
    }


def _flatten(a: Sequence[Sequence[F]]) -> Tuple[F, ...]:
    return tuple(x for row in a for x in row)


def _rank(vectors: Sequence[Sequence[F]]) -> int:
    rows = [list(map(F, row)) for row in vectors]
    if not rows:
        return 0
    m, n = len(rows), len(rows[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if rows[i][c] != 0), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for i in range(m):
            if i != r and rows[i][c] != 0:
                q = rows[i][c]
                rows[i] = [x - q * y for x, y in zip(rows[i], rows[r])]
        r += 1
        if r == m:
            break
    return r


def _realify_complex_2(x: Sequence[Sequence[F]], y: Sequence[Sequence[F]]) -> List[List[F]]:
    # Realification of X+iY in Re/Im block ordering.
    top = [list(x[i]) + [-v for v in y[i]] for i in range(2)]
    bottom = [list(y[i]) + list(x[i]) for i in range(2)]
    return top + bottom


def _mmn(a: Sequence[Sequence[F]], b: Sequence[Sequence[F]]) -> List[List[F]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def _transpose_n(a: Sequence[Sequence[F]]) -> List[List[F]]:
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]


def _star_closure(generators: Sequence[Sequence[Sequence[F]]], max_rounds: int = 20) -> List[List[List[F]]]:
    n = len(generators[0])
    eye = [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]
    basis: List[List[List[F]]] = []

    def add(m: List[List[F]]) -> bool:
        old = _rank([_flatten(x) for x in basis])
        new = _rank([_flatten(x) for x in basis + [m]])
        if new > old:
            basis.append(m)
            return True
        return False

    add(eye)
    for g in generators:
        add([list(row) for row in g])
        add(_transpose_n(g))
    for _ in range(max_rounds):
        changed = False
        snapshot = list(basis)
        for a in snapshot:
            for b in snapshot:
                changed |= add(_mmn(a, b))
        if not changed:
            break
    return basis


def _elliptic_gate_ok(gate: Matrix2) -> Tuple[bool, List[str]]:
    """Exact-path gate validity (audit MAJOR-1): det==1, ELLIPTICITY, nonintegral trace.

    A det-one real 2x2 matrix with |trace| >= 2 is hyperbolic or parabolic:
    unbounded orbit, no compact closure, no circle.  The SO(1,1) boost
    [[5/4,3/4],[3/4,5/4]] (trace 5/2) must be rejected here, not merely
    displayed as a prose control.  Integral traces in {-2,-1,0,1,2} are the
    finite-order (or non-elliptic boundary) cases and are rejected as before.
    """
    reasons: List[str] = []
    if _det(gate) != 1:
        reasons.append("determinant must be exactly one")
    t = _trace(gate)
    if not (-2 < t < 2):
        reasons.append(
            "gate is not elliptic: |trace| >= 2 (hyperbolic/parabolic; "
            "unbounded orbit, no compact closure)")
    if t in FINITE_ORDER_INTEGER_TRACES:
        reasons.append("integral trace in {-2,-1,0,1,2}: finite-order rotation class")
    return (not reasons, reasons)


def _gaussian_mul(z: Tuple[int, int], w: Tuple[int, int]) -> Tuple[int, int]:
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def _gaussian_pow(z: Tuple[int, int], n: int) -> Tuple[int, int]:
    out = (1, 0)
    for _ in range(n):
        out = _gaussian_mul(out, z)
    return out


def _gaussian_infinite_order_certificate(r: Matrix2) -> Dict[str, object]:
    """Executed Gaussian-integer non-associate-primes certificate (audit MAJOR-4).

    PORTED from the banked H3 battery (``T_held_connected_subgroup_so2``,
    ``_held_holonomy_groups.py``), which certifies infinite order of the
    cos=3/5 rotation R35.  This packet's gate is exactly its square:
    -7+24i = (3+4i)^2 = (2+i)^4.  If R^n = I for some n>=1 then
    (-7+24i)^n = 25^n = ((2+i)(2-i))^{2n} in Z[i], i.e.
    (2+i)^{4n} = (2+i)^{2n}(2-i)^{2n}, forcing (2+i)^{2n} = (2-i)^{2n}.
    Unique factorization in Z[i] (NAMED import) with 2+i and 2-i
    non-associate Gaussian primes forbids that, so R has infinite order.
    """
    reasons: List[str] = []
    r35: Matrix2 = ((F(3, 5), F(-4, 5)), (F(4, 5), F(3, 5)))
    square_ok = _mm(r35, r35) == r
    if not square_ok:
        reasons.append("gate must equal the exact square of the banked cos=3/5 rotation")
    two_plus_i = (2, 1)
    two_minus_i = (2, -1)
    if _gaussian_mul(two_plus_i, two_plus_i) != (3, 4):
        reasons.append("(2+i)^2 must equal 3+4i")
    if _gaussian_mul((3, 4), (3, 4)) != (-7, 24):
        reasons.append("(3+4i)^2 must equal -7+24i")
    if _gaussian_pow(two_plus_i, 4) != (-7, 24):
        reasons.append("(2+i)^4 must equal -7+24i")
    if two_plus_i[0] ** 2 + two_plus_i[1] ** 2 != 5:
        reasons.append("N(2+i) must be the rational prime 5, making 2+i a Gaussian prime")
    associates_of_two_plus_i = {(2, 1), (-2, -1), (-1, 2), (1, -2)}
    if two_minus_i in associates_of_two_plus_i:
        reasons.append("2-i must not be an associate of 2+i")
    if _gaussian_mul(two_plus_i, two_minus_i) != (5, 0):
        reasons.append("(2+i)(2-i) must equal 5")
    distinct: List[Matrix2] = []
    power = _eye()
    for n in range(1, 25):
        power = _mm(power, r)
        if power == _eye():
            reasons.append(f"gate returned to the identity at n={n}")
            break
        distinct.append(power)
    if len(set(distinct)) != 24:
        reasons.append("first 24 powers must be pairwise distinct and nonidentity")
    return {
        "ok": not reasons,
        "reasons": reasons,
        "square_relation_verified": square_ok,
        "square_relation": "R = R35^2; -7+24i = (3+4i)^2 = (2+i)^4",
        "gaussian_prime": "N(2+i)=5 prime",
        "non_associate": "2-i is not an associate of 2+i",
        "named_import": "Z[i] is a unique factorization domain",
        "prior_art": "banked H3 battery: T_held_connected_subgroup_so2 (_held_holonomy_groups.py)",
        "distinct_powers_computed": len(set(distinct)),
    }


def _closure_disposition(gate: Matrix2, q: Matrix2, infinite_order_certified: bool,
                         max_order_scan: int = 64) -> Dict[str, object]:
    """Computed circle-closure branch (audit MAJOR-3 / mutation M8).

    The conclusion of the one-gate circle theorem is DERIVED from this checked
    disposition, never shipped as an artifact literal.  Branches: no certified
    compact closure (no invariant pd form exhibited); orientation-reversing;
    finite cyclic (identity found in the executed power scan); infinite
    compact oriented (the SO(2) branch, gated on the executed infinite-order
    certificate).
    """
    q_pd = q[0][0] > 0 and _det(q) > 0
    invariant = _mm(_mm(_mt(gate), q), gate) == q
    oriented = _det(gate) == 1
    finite_order: Optional[int] = None
    power = _eye()
    for n in range(1, max_order_scan + 1):
        power = _mm(power, gate)
        if power == _eye():
            finite_order = n
            break
    if not (q_pd and invariant):
        branch = "no_certified_compact_closure"
    elif not oriented:
        branch = "orientation_reversing"
    elif finite_order is not None:
        branch = "finite_cyclic"
    elif infinite_order_certified:
        branch = "infinite_compact_oriented"
    else:
        branch = "order_undecided"
    return {
        "branch": branch,
        "q_positive_definite": q_pd,
        "form_invariant": invariant,
        "det_one": oriented,
        "finite_order_found": finite_order,
    }


# ---------------------------------------------------------------------------
# Exact 3-4-5 geometry and one-gate theorem
# ---------------------------------------------------------------------------


def _apf_projector_pair() -> Tuple[Matrix2, Matrix2, Vector2]:
    e = ((F(1), F(0)), (F(0), F(0)))
    u = (F(3, 5), F(4, 5))
    p = _projector(u)
    return e, p, u


def _reflection_product_gate() -> Tuple[Matrix2, Matrix2, Matrix2, Matrix2]:
    e, p, _ = _apf_projector_pair()
    s_e = _reflection(e)
    s_p = _reflection(p)
    r = _mm(s_p, s_e)
    return s_e, s_p, r, p


def check_T_apf_345_projector_pair() -> Dict[str, object]:
    fails: List[str] = []
    e, p, u = _apf_projector_pair()
    z = ((F(0), F(0)), (F(0), F(0)))
    comm = _sub(_mm(e, p), _mm(p, e))
    if _mm(e, e) != e:
        fails.append("sector projector E must be idempotent")
    if _mm(p, p) != p:
        fails.append("3-4-5 projector P must be idempotent")
    if _mt(p) != p:
        fails.append("3-4-5 projector P must be symmetric")
    if comm == z:
        fails.append("projector pair must be noncommuting")
    if comm[0][1] != F(12, 25) or comm[1][0] != F(-12, 25):
        fails.append("commutator must reproduce the APF 12/25 witness")
    # Direction pin (audit m5): the swapped direction u=(4/5,3/5) reproduces
    # the same 12/25 commutator magnitude; the P_u diagonal pins the direction
    # in-check instead of leaving it to the downstream trace.
    if u != (F(3, 5), F(4, 5)):
        fails.append("projector direction must be pinned to u=(3/5,4/5)")
    if p[0][0] != F(9, 25) or p[1][1] != F(16, 25):
        fails.append("P_u diagonal must pin the direction: (9/25, 16/25)")
    direction_pinned = u == (F(3, 5), F(4, 5)) and p[0][0] == F(9, 25) and p[1][1] == F(16, 25)
    return _result(
        "T_apf_345_projector_pair",
        "The live APF 3-4-5 IJC witness restricts to two exact rank-one projectors E and P_u on span{e1,e3}, with u=(3/5,4/5) and [E,P_u]_{12}=12/25.  The direction is pinned in-check: the swapped direction (4/5,3/5) reproduces the commutator magnitude but fails the (9/25,16/25) diagonal pin.  This imports only the exact projector geometry; it does not promote either reflection to a physical Held process.",
        {
            "E": _matrix_strings(e),
            "P_u": _matrix_strings(p),
            "u": _vector_strings(u),
            "commutator": _matrix_strings(comm),
            "direction_pinned": direction_pinned,
            "source_coderef": "reproduce_inline_345_commutator (ijc_boolean_defender_bridge.py)",
            "physical_reflections_derived": False,
        },
        fails,
        premises=("CODESPACE_TO_HELD_CARRIER_IDENTIFICATION",),
        negative_controls=("same projector geometry without process implementability",),
    )


def check_T_reflection_product_irrational_gate() -> Dict[str, object]:
    fails: List[str] = []
    s_e, s_p, r, _ = _reflection_product_gate()
    if _mm(s_e, s_e) != _eye() or _mm(s_p, s_p) != _eye():
        fails.append("both sharp reflections must square to identity")
    if _mt(s_e) != s_e or _mt(s_p) != s_p:
        fails.append("both sharp reflections must be self-adjoint in the witness metric")
    if _det(r) != 1:
        fails.append("reflection product must be orientation preserving")
    if _mm(_mt(r), r) != _eye():
        fails.append("reflection product must preserve the witness metric")
    if _trace(r) != F(-14, 25):
        fails.append("reflection product trace must be -14/25")
    direct = ((F(3, 5), F(-4, 5)), (F(4, 5), F(3, 5)))
    if _det(direct) != 1 or _trace(direct) != F(6, 5):
        fails.append("direct 3-4-5 gate control malformed")
    return _result(
        "T_reflection_product_irrational_gate",
        "If the two sharp reflections associated with the APF projector pair are physically admitted on the same Held carrier, their product is the exact orientation-preserving gate R=[[-7,-24],[24,-7]]/25.  Its trace is -14/25.  A direct 3-4-5 gate provides the alternative trace 6/5 route.  Projector existence alone does not supply process implementability.",
        {
            "S_E": _matrix_strings(s_e),
            "S_P": _matrix_strings(s_p),
            "R_reflection_product": _matrix_strings(r),
            "trace_R": str(_trace(r)),
            "det_R": str(_det(r)),
            "R_direct_345": _matrix_strings(direct),
            "trace_direct": str(_trace(direct)),
            "reflection_processes_assumed": True,
        },
        fails,
        dependencies=("T_apf_345_projector_pair",),
        premises=("PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY",),
        negative_controls=("projector/effect does not imply reversible reflection process",),
    )


def check_T_bounded_cyclic_orbit_compact_closure() -> Dict[str, object]:
    fails: List[str] = []
    _, _, r, _ = _reflection_product_gate()
    u = (F(1), F(0))
    ru = _mv(r, u)
    cyclic_det = _cross(u, ru)
    if cyclic_det == 0:
        fails.append("seed and its first image must span the two-dimensional carrier")
    prefix = EVIDENCE_STRENGTH["orbit_prefix_two_sided"]
    forward = _orbit(r, u, prefix)
    rinv = _mt(r)
    backward = _orbit(rinv, u, prefix)
    if len(forward) != prefix or len(backward) != prefix:
        fails.append("two-sided orbit prefix must match the pinned evidence strength")
    all_unit = all(_norm2(v) == 1 for v in forward + backward)
    if not all_unit:
        fails.append("reference two-sided orbit must remain bounded exactly")

    # Four-outcome normalization is an operational boundedness witness.
    def readout(v: Vector2) -> Tuple[F, F, F, F]:
        x, y = v
        return ((1 + x) / 4, (1 - x) / 4, (1 + y) / 4, (1 - y) / 4)

    def in_simplex(v: Vector2) -> bool:
        probs = readout(v)
        return sum(probs) == 1 and all(z >= 0 for z in probs)

    all_normalized = all(in_simplex(v) for v in forward + backward)
    if not all_normalized:
        fails.append("two-sided orbit must remain in the normalized readout simplex")

    # ---- Executed failure directions (audit MAJOR-2, bounded_orbit standard) ----
    # 1. The SO(1,1) boost must FAIL the bounded-orbit leg, with an exact
    #    growth certificate: eigenvector (1,1), lambda=2, verified iteration.
    boost: Matrix2 = ((F(5, 4), F(3, 4)), (F(3, 4), F(5, 4)))
    grow_vec: Vector2 = (F(1), F(1))
    lam = F(2)
    if _mv(boost, grow_vec) != (lam * grow_vec[0], lam * grow_vec[1]):
        fails.append("boost growth certificate: (1,1) must be an exact lambda=2 eigenvector")
    power = _eye()
    iter_ok = True
    for n in range(1, 11):
        power = _mm(power, boost)
        if _mv(power, grow_vec) != (lam ** n * grow_vec[0], lam ** n * grow_vec[1]):
            iter_ok = False
            break
    if not iter_ok:
        fails.append("boost growth certificate: exact iteration must verify lambda^n growth")
    boost_orbit = _orbit(boost, u, 16)
    boost_sups = [max(abs(v[0]), abs(v[1])) for v in boost_orbit]
    boost_grows = all(boost_sups[k + 1] > boost_sups[k] for k in range(len(boost_sups) - 1))
    boost_exits = not all(in_simplex(v) for v in boost_orbit)
    if not boost_grows:
        fails.append("boost negative control: orbit sup must grow strictly")
    if not boost_exits:
        fails.append("boost negative control: the strictly growing orbit must exit the normalized readout simplex")

    # 2. Bounded ONE-SIDED orbit on a NON-CYCLIC eigenvector is insufficient
    #    (executed, no longer a prose string): the contracting boost
    #    eigenvector (1,-1) (lambda=1/2) has a bounded forward orbit, but the
    #    seed is non-cyclic and the backward orbit grows strictly.
    dec_vec: Vector2 = (F(1), F(-1))
    dec_lam = F(1, 2)
    if _mv(boost, dec_vec) != (dec_lam * dec_vec[0], dec_lam * dec_vec[1]):
        fails.append("insufficiency control: (1,-1) must be an exact lambda=1/2 boost eigenvector")
    if _cross(dec_vec, _mv(boost, dec_vec)) != 0:
        fails.append("insufficiency control: the eigenvector seed must be non-cyclic")
    dec_forward = _orbit(boost, dec_vec, 16)
    one_sided_bounded = all(max(abs(v[0]), abs(v[1])) <= 1 for v in dec_forward)
    boost_inv: Matrix2 = ((F(5, 4), F(-3, 4)), (F(-3, 4), F(5, 4)))
    if _mm(boost, boost_inv) != _eye():
        fails.append("insufficiency control: exact boost inverse malformed")
    dec_backward = _orbit(boost_inv, dec_vec, 16)
    back_sups = [max(abs(v[0]), abs(v[1])) for v in dec_backward]
    backward_grows = all(back_sups[k + 1] > back_sups[k] for k in range(len(back_sups) - 1))
    if not one_sided_bounded:
        fails.append("insufficiency control: the forward eigen-orbit must remain bounded")
    if not backward_grows:
        fails.append("insufficiency control: the backward eigen-orbit must grow strictly")

    return _result(
        "T_bounded_cyclic_orbit_compact_closure",
        "A reversible gate does not require a separately assumed global compact state body.  If one occupied profile u is cyclic (u,Tu span the carrier) and its two-sided orbit remains inside a finite normalized separating readout, then all powers of T and T^{-1} are uniformly bounded on a basis, and the cyclic subgroup has compact closure in GL(2,R) via the NAMED import BOUNDED_SUBGROUP_COMPACT_CLOSURE_general_case.  The failure directions are EXECUTED, not prose: the SO(1,1) boost carries an exact growth certificate (eigenvector (1,1), lambda=2, verified iteration) and its strictly growing orbit exits the readout simplex; a bounded one-sided orbit on the non-cyclic contracting eigenvector (1,-1) is exhibited as insufficient (backward orbit grows strictly).",
        {
            "cyclic_seed": _vector_strings(u),
            "first_image": _vector_strings(ru),
            "basis_determinant": str(cyclic_det),
            "forward_iterates_checked": len(forward),
            "backward_iterates_checked": len(backward),
            "orbit_prefix_pinned": prefix,
            "all_readouts_normalized": all_normalized,
            "separately_assumed_global_compact_body": False,
            "named_math_imports": ["BOUNDED_SUBGROUP_COMPACT_CLOSURE_general_case"],
            "boost_growth_certificate": {
                "eigenvector": _vector_strings(grow_vec),
                "eigenvalue": str(lam),
                "verified_powers": 10,
                "orbit_sup_strictly_growing": boost_grows,
                "exits_readout_simplex": boost_exits,
            },
            "one_sided_insufficiency_control": {
                "eigenvector": _vector_strings(dec_vec),
                "eigenvalue": str(dec_lam),
                "seed_cyclic": False,
                "forward_orbit_bounded": one_sided_bounded,
                "backward_orbit_strictly_growing": backward_grows,
            },
        },
        fails,
        dependencies=("T_reflection_product_irrational_gate",),
        premises=(
            "NONZERO_OCCUPIED_HELD_PROFILE",
            "FINITE_SEPARATING_READOUT",
            "NORMALIZED_PROFILE_PRESERVATION",
            "REVERSIBLE_GATE_ACTION",
        ),
        negative_controls=(
            "SO(1,1) boost: exact lambda=2 growth certificate, exits the readout simplex (executed)",
            "bounded one-sided orbit on a non-cyclic eigenvector is insufficient (executed)",
        ),
    )


def check_T_rational_trace_forces_infinite_order() -> Dict[str, object]:
    fails: List[str] = []
    _, _, r, _ = _reflection_product_gate()
    tr = _trace(r)
    if tr in FINITE_ORDER_INTEGER_TRACES:
        fails.append("nonintegral rational trace must not be classified finite-order")
    elliptic_ok, elliptic_reasons = _elliptic_gate_ok(r)
    if not elliptic_ok:
        fails.append("candidate gate must pass the elliptic gate test: " + "; ".join(elliptic_reasons))

    # PRIMARY leg (audit MAJOR-4): the executed Gaussian-integer non-associate-
    # primes certificate, PORTED from the banked H3 battery.  The gate is the
    # exact square of the banked cos=3/5 rotation: -7+24i = (3+4i)^2 = (2+i)^4.
    gauss = _gaussian_infinite_order_certificate(r)
    if not gauss["ok"]:
        fails.extend("gaussian certificate: " + str(x) for x in gauss["reasons"])

    # Corroborating scan (kept, now count-derived per audit m2/m4): no power up
    # to the pinned bound returns to the identity.
    scan_bound = EVIDENCE_STRENGTH["power_scan_nonidentity"]
    powers_checked = 0
    power = _eye()
    for n in range(1, scan_bound + 1):
        power = _mm(power, r)
        if power == _eye():
            fails.append(f"R repeated at finite order n={n}")
            break
        powers_checked += 1
    if powers_checked != scan_bound:
        fails.append("power scan must exhaust the pinned nonidentity bound")

    # Exact finite-order controls: half-turn, order 3, order 4, order 6.
    controls = {
        "order_2": ((F(-1), F(0)), (F(0), F(-1))),
        "order_3": ((F(-1, 2), F(-1)), (F(3, 4), F(-1, 2))),
        "order_4": ((F(0), F(-1)), (F(1), F(0))),
        "order_6": ((F(1, 2), F(-1)), (F(3, 4), F(1, 2))),
    }
    expected = {"order_2": F(-2), "order_3": F(-1), "order_4": F(0), "order_6": F(1)}
    for name, m in controls.items():
        if _trace(m) != expected[name] or _det(m) != 1:
            fails.append(f"finite-order trace control failed: {name}")
    boost = ((F(5, 4), F(3, 4)), (F(3, 4), F(5, 4)))
    if _det(boost) != 1 or _trace(boost) != F(5, 2):
        fails.append("hyperbolic infinite-order control malformed")
    boost_elliptic, boost_reasons = _elliptic_gate_ok(boost)
    if boost_elliptic:
        fails.append("SO(1,1) boost must be rejected by the elliptic gate test")
    return _result(
        "T_rational_trace_forces_infinite_order",
        "The PRIMARY infinite-order leg is the executed Gaussian-integer non-associate-primes certificate ported from the banked H3 battery (T_held_connected_subgroup_so2, _held_holonomy_groups.py): the gate is exactly the square of the banked cos=3/5 rotation, -7+24i=(3+4i)^2=(2+i)^4, and unique factorization in Z[i] with the non-associate primes 2+i and 2-i forbids R^n=I for n>=1.  The rational-trace criterion corroborates: for an element of a compact two-dimensional orientation-preserving automorphism group, finite order would make its trace a rational algebraic integer, hence an integer in {-2,-1,0,1,2}; the exact trace -14/25 is rational but nonintegral.  A 256-power exact scan corroborates further.  The SO(1,1) boost shows compactness remains essential and is itself rejected by the elliptic gate test.",
        {
            "trace": str(tr),
            "finite_order_rational_trace_set": [str(x) for x in sorted(FINITE_ORDER_INTEGER_TRACES)],
            "elliptic_gate_passed": elliptic_ok,
            "gaussian_certificate_primary": bool(gauss["ok"]),
            "gaussian_integer_certificate": {k: v for k, v in gauss.items() if k not in ("ok", "reasons")},
            "powers_checked_nonidentity": powers_checked,
            "power_scan_pinned": scan_bound,
            "finite_order_controls": {k: str(_trace(v)) for k, v in controls.items()},
            "boost_trace": str(_trace(boost)),
            "boost_rejected_by_elliptic_gate": not boost_elliptic,
            "boost_rejection_reasons": boost_reasons,
            "proof_imports": [
                "roots of unity are algebraic integers; rational algebraic integers are integers",
                "Z[i] is a unique factorization domain (Gaussian-integer certificate leg)",
            ],
        },
        fails,
        dependencies=("T_bounded_cyclic_orbit_compact_closure",),
        negative_controls=(
            "SO(1,1) boost: infinite order but noncompact, rejected by the elliptic gate",
            "unipotent shear: trace 2 and unbounded",
        ),
    )


def check_T_finite_precision_cannot_certify_infinite_order() -> Dict[str, object]:
    """Finite calibration data cannot establish exact irrationality.

    Roots of unity are dense on the unit circle.  This check gives one explicit
    finite-order rotation whose trace lies within 3e-8 of the exact APF candidate
    trace -14/25.  Exact circle closure therefore requires a structural exact
    gate derivation; experiment can certify only a declared finite-resolution
    orbit cover.
    """
    fails: List[str] = []
    _, _, r, _ = _reflection_product_gate()
    target_angle = math.atan2(float(r[1][0]), float(r[0][0]))
    p, q = 4483, 15188
    approximating_angle = 2.0 * math.pi * p / q
    angle_error = abs(target_angle - approximating_angle)
    target_trace = float(_trace(r))
    finite_order_trace = 2.0 * math.cos(approximating_angle)
    trace_error = abs(target_trace - finite_order_trace)
    if math.gcd(p, q) != 1:
        fails.append("finite-order control p/q must be reduced")
    if angle_error >= 2e-8 or trace_error >= 3e-8:
        fails.append("explicit finite-order control is not close enough to the target gate")
    if q <= 10000:
        fails.append("finite-order control should have a large denominator")
    return _result(
        "T_finite_precision_cannot_certify_infinite_order",
        "Finite-precision calibration cannot prove that a physical rotation has infinite order: the exact order-15188 rotation by 2pi*4483/15188 has trace within 3e-8 of -14/25.  The exact one-gate circle theorem must therefore consume an exact structural gate derivation.  Experimental/device data can certify a finite-resolution orbit cover, but not exact irrationality.",
        {
            "target_trace_exact": str(_trace(r)),
            "finite_order_control": {"p": p, "q": q, "order": q},
            "angle_error_radians": angle_error,
            "trace_error": trace_error,
            "exact_holonomy_requires_structural_derivation": True,
            "experiment_can_certify": "finite-resolution orbit cover only",
        },
        fails,
        dependencies=("T_rational_trace_forces_infinite_order",),
        negative_controls=("order-15188 rotation indistinguishable at ordinary calibration precision",),
        epistemic="P_math",
    )


def check_T_one_gate_dense_held_circle() -> Dict[str, object]:
    fails: List[str] = []
    _, _, r, _ = _reflection_product_gate()
    # Rational ellipse conjugacy witness: S R S^-1, Q=S^-T S^-1.
    t = ((r[0][0], F(2, 3) * r[0][1]), (F(3, 2) * r[1][0], r[1][1]))
    q = ((F(1, 4), F(0)), (F(0), F(1, 9)))
    lhs = _mm(_mm(_mt(t), q), t)
    if lhs != q:
        fails.append("conjugated gate must preserve the exact John-ellipse witness")
    if _trace(t) != F(-14, 25) or _det(t) != 1:
        fails.append("trace/determinant must survive coordinate conjugation")

    # Computed closure disposition (audit MAJOR-3 / mutation M8): the SO(2)
    # conclusion is DERIVED from a checked branch, never shipped as a literal.
    gauss = _gaussian_infinite_order_certificate(r)
    dispo = _closure_disposition(t, q, bool(gauss["ok"]))
    n_carrier = len(t)
    so_dim = n_carrier * (n_carrier - 1) // 2
    # The Q-invariance algebra {A : A^T Q + Q A = 0} is computed exactly; its
    # dimension must equal dim so(n) = n(n-1)/2, pinning the carrier dimension
    # that the conclusion string is derived from.
    rows: List[List[F]] = []
    for i in range(n_carrier):
        for j in range(n_carrier):
            coeff = [F(0)] * (n_carrier * n_carrier)
            for k in range(n_carrier):
                coeff[k * n_carrier + i] += q[k][j]
                coeff[k * n_carrier + j] += q[i][k]
            rows.append(coeff)
    alg_dim = n_carrier * n_carrier - _rank(rows)
    if alg_dim != so_dim:
        fails.append(f"Q-invariance algebra dimension must equal dim so({n_carrier}), got {alg_dim}")
    if dispo["branch"] == "infinite_compact_oriented" and alg_dim == so_dim:
        closure = "SO(%d)" % n_carrier
    elif dispo["branch"] == "finite_cyclic":
        closure = "finite cyclic C_%s" % dispo["finite_order_found"]
    else:
        closure = "no circle conclusion licensed"
    if n_carrier != 2 or closure != "SO(%d)" % n_carrier:
        fails.append(f"computed closure disposition must land on the full circle, got {closure!r}")

    # Executed branch controls: the discrete and noncompact branches are live.
    quarter: Matrix2 = ((F(0), F(-1)), (F(1), F(0)))
    ctrl_finite = _closure_disposition(quarter, _eye(), False)
    if ctrl_finite["branch"] != "finite_cyclic" or ctrl_finite["finite_order_found"] != 4:
        fails.append("finite cyclic control must land on the discrete branch")
    boost: Matrix2 = ((F(5, 4), F(3, 4)), (F(3, 4), F(5, 4)))
    ctrl_boost = _closure_disposition(boost, _eye(), False)
    if ctrl_boost["branch"] != "no_certified_compact_closure":
        fails.append("boost control must fail compact-closure certification")

    return _result(
        "T_one_gate_dense_held_circle",
        "A single infinite-order reversible automorphism of a compact convex two-dimensional Held body replaces the connected-sweep premise.  The closure of its cyclic subgroup is an infinite compact subgroup; the John metric conjugates it into SO(2), whose only infinite closed subgroup is SO(2).  Three load-bearing standard-mathematics facts are consumed as NAMED imports (registered machine-readably in NAMED_MATH_IMPORTS), not derived here: bounded subgroup => compact closure; compact subgroup conjugates into O(2) (averaging/John ellipsoid); closed subgroups of SO(2) are finite cyclic or full (Kronecker density).  What is computed: the exact invariant-ellipse witness, the ported Gaussian-integer infinite-order certificate, the Q-invariance algebra dimension (= dim so(2) = 1), and the live branch controls; the SO(2) conclusion string is DERIVED from this checked disposition.",
        {
            "connected_sweep_required": False,
            "one_exact_gate_suffices": True,
            "conjugated_gate_T": _matrix_strings(t),
            "John_metric_Q": _matrix_strings(q),
            "TtQT": _matrix_strings(lhs),
            "trace_coordinate_invariant": str(_trace(t)),
            "closure": closure,
            "closure_derivation": {
                "branch": dispo["branch"],
                "q_positive_definite": dispo["q_positive_definite"],
                "form_invariant": dispo["form_invariant"],
                "det_one": dispo["det_one"],
                "finite_order_found": dispo["finite_order_found"],
                "infinite_order_certificate": "gaussian non-associate primes (primary, ported from banked H3)",
                "invariance_algebra_dim": alg_dim,
                "so_n_expected_dim": so_dim,
                "carrier_dim": n_carrier,
            },
            "named_math_imports": list(NAMED_MATH_IMPORTS),
            "finite_cyclic_control": ctrl_finite,
            "boost_control": ctrl_boost,
        },
        fails,
        dependencies=("T_rational_trace_forces_infinite_order", "T_bounded_cyclic_orbit_compact_closure"),
        premises=("EFFECTIVE_GATE_ACTION",),
        negative_controls=(
            "finite cyclic C_n lands on the discrete branch (executed)",
            "SO(1,1) boost fails compact-closure certification (executed)",
            "identity representation kills the gate",
        ),
    )


def check_T_orbit_mixture_constructs_disk() -> Dict[str, object]:
    fails: List[str] = []
    _, _, r, _ = _reflection_product_gate()
    seed = (F(1), F(0))
    prefix = EVIDENCE_STRENGTH["disk_orbit_prefix"]
    pts = _orbit(r, seed, prefix)
    if len(pts) != prefix:
        fails.append("disk orbit prefix must match the pinned evidence strength")
    all_unit = all(_norm2(p) == 1 for p in pts)
    if not all_unit:
        fails.append("exact gate orbit must remain on one bounded level")
    all_distinct = len(set(pts)) == len(pts)
    if not all_distinct:
        fails.append("infinite-order orbit must not repeat in the finite prefix")
    readouts = [((F(1)+x)/4, (F(1)-x)/4, (F(1)+y)/4, (F(1)-y)/4) for x, y in pts]
    readouts_valid = all(sum(p) == 1 and all(z >= 0 for z in p) for p in readouts)
    if not readouts_valid:
        fails.append("orbit profiles must have valid four-outcome separating readouts")
    # One exact dyadic mixture control.
    u, v = pts[3], pts[17]
    mix = ((u[0] + v[0]) / 2, (u[1] + v[1]) / 2)
    if _norm2(mix) > 1:
        fails.append("classical mixture must remain inside the orbit disk")
    return _result(
        "T_orbit_mixture_constructs_disk",
        "Once one nonzero profile has an admitted infinite-order reversible orbit, the bounded two-sided orbit yields its compact closure through the NAMED import BOUNDED_SUBGROUP_COMPACT_CLOSURE_general_case under the named premises NORMALIZED_PROFILE_PRESERVATION and FINITE_SEPARATING_READOUT, and ordinary classical randomization gives the closed convex hull.  The dense SO(2) orbit is a circle and its convex hull is the disk.  A separately assumed global state body is no longer needed for the circle theorem.",
        {
            "orbit_prefix_checked": len(pts),
            "orbit_prefix_pinned": prefix,
            "all_profiles_unit": all_unit,
            "all_profiles_distinct": all_distinct,
            "four_outcome_readout_valid": readouts_valid,
            "sample_mixture_norm_squared": str(_norm2(mix)),
            "constructed_body": "closed convex hull of one physical orbit",
            "named_math_imports": ["BOUNDED_SUBGROUP_COMPACT_CLOSURE_general_case"],
        },
        fails,
        dependencies=("T_one_gate_dense_held_circle",),
        premises=("NONZERO_OCCUPIED_HELD_PROFILE", "CLASSICAL_RANDOMIZATION_CLOSURE", "FINITE_SEPARATING_READOUT"),
    )


def check_T_finite_resolution_orbit_cover() -> Dict[str, object]:
    fails: List[str] = []
    _, _, r, _ = _reflection_product_gate()
    table = []
    resolutions = EVIDENCE_STRENGTH["cover_resolutions"]
    if resolutions != (16, 32, 64, 128, 256):
        fails.append("cover resolutions must match the pinned evidence strength")
    for n in resolutions:
        row = _cyclic_cover(r, n)
        if not row["all_points_exactly_unit"] or not row["all_points_distinct"]:
            fails.append(f"orbit coverage exactness failed at N={n}")
        table.append(row)
    row64 = next(x for x in table if x["N"] == 64)
    row256 = next(x for x in table if x["N"] == 256)
    if row64["max_gap_degrees"] >= 7:
        fails.append("64-step orbit should cover the circle within 7 degrees")
    if row256["radial_deficit_bound"] >= 2e-4:
        fails.append("256-step orbit polygon should approximate the disk within 2e-4 radially")
    return _result(
        "T_finite_resolution_orbit_cover",
        "The exact rational gate yields a finite, auditable approximation at every declared resolution.  Sixty-four iterates have maximum angular gap below 7 degrees; 256 iterates have maximum gap below 1.9 degrees and a convex-hull radial deficit below 2e-4.  Every orbit coordinate is an exact rational number.",
        {
            "coverage_table": table,
            "N64_max_gap_degrees": row64["max_gap_degrees"],
            "N64_radial_deficit": row64["radial_deficit_bound"],
            "N64_nearest_angle_fringe_error_bound": row64["max_gap_radians"] / 4.0,
            "N256_max_gap_degrees": row256["max_gap_degrees"],
            "N256_radial_deficit": row256["radial_deficit_bound"],
            "N256_nearest_angle_fringe_error_bound": row256["max_gap_radians"] / 4.0,
        },
        fails,
        dependencies=("T_orbit_mixture_constructs_disk",),
        negative_controls=("order-four quarter-turn gives only four orbit points",),
    )


def check_T_born_fringe_from_one_gate_circle() -> Dict[str, object]:
    fails: List[str] = []
    _, _, r, _ = _reflection_product_gate()
    # Solve the sharp constraints e(1,0)=1 and e(-1,0)=0 for e(x,y)=a+bx+cy:
    # a+b=1 and a-b=0, so a=b=1/2 by exact elimination (computed, not hardcoded).
    a = (F(1) + F(0)) / 2
    b = (F(1) - F(0)) / 2
    if a != F(1, 2) or b != F(1, 2):
        fails.append("sharp antipodal constraints must force a=b=1/2")

    # Boundedness-forces-c=0, EXECUTED (audit m1): scan candidate tilts over
    # the exact orbit prefix.  c=0 keeps 0<=e<=1 at every scanned point; every
    # nonzero candidate tilt is violated at a computed exact orbit point.
    scan_points = EVIDENCE_STRENGTH["fringe_scan_points"]
    pts = _orbit(r, (F(1), F(0)), scan_points)
    if len(pts) != scan_points:
        fails.append("fringe orbit scan must match the pinned evidence strength")

    def effect(cc: F, v: Vector2) -> F:
        return a + b * v[0] + cc * v[1]

    c_zero_bounded = all(F(0) <= effect(F(0), v) <= F(1) for v in pts)
    if not c_zero_bounded:
        fails.append("the c=0 effect must stay within [0,1] on the entire orbit prefix")
    violations: Dict[str, object] = {}
    for cc in (F(1, 25), F(-1, 25), F(1, 10), F(-1, 10), F(1, 4), F(-1, 4), F(1, 2), F(-1, 2)):
        witness = next((v for v in pts if not (F(0) <= effect(cc, v) <= F(1))), None)
        if witness is None:
            fails.append(f"nonzero tilt c={cc} must violate boundedness at some scanned orbit point")
        else:
            violations[str(cc)] = {"orbit_point": _vector_strings(witness),
                                   "effect_value": str(effect(cc, witness))}
    c = F(0)

    # Sharp samples computed from the derived coefficients (the former
    # literal-vs-literal leg is deleted per audit m1).
    samples = {
        "theta_0": effect(c, (F(1), F(0))),
        "theta_pi_over_2": effect(c, (F(0), F(1))),
        "theta_pi": effect(c, (F(-1), F(0))),
    }
    if samples["theta_0"] != 1 or samples["theta_pi_over_2"] != F(1, 2) or samples["theta_pi"] != 0:
        fails.append("computed sharp samples must be (1, 1/2, 0)")
    # 3-4-5 direct point probability, computed from the derived effect.
    p345 = effect(c, (F(3, 5), F(4, 5)))
    if p345 != F(4, 5):
        fails.append("3-4-5 Born-fringe probability must be 4/5")
    return _result(
        "T_born_fringe_from_one_gate_circle",
        "On the disk constructed from the one-gate orbit, an affine binary effect that is certain at one pole and impossible at the antipode has a=b=1/2 by exact elimination, and the boundedness-forces-c=0 step is EXECUTED as a finite scan: c=0 keeps the effect inside [0,1] on 256 exact orbit points, while every scanned nonzero tilt is violated at a computed orbit point.  (Full uniqueness over all real tilts is elementary affine geometry -- the maximum of bx+cy on the circle is sqrt(b^2+c^2) -- consumed for the unscanned tilts; the scan is the executable witness, not the whole proof.)  The resulting fringe is e(theta)=(1+cos theta)/2=cos^2(theta/2).",
        {
            "effect_coefficients": {"a": str(a), "b": str(b), "c": str(c)},
            "fringe_formula": "(1+cos(theta))/2 = cos(theta/2)^2",
            "probability_at_direct_345_point": str(p345),
            "sharp_samples": {k: str(v) for k, v in samples.items()},
            "c_zero_bounded_on_orbit_prefix": c_zero_bounded,
            "orbit_scan_points": len(pts),
            "nonzero_tilt_violations": violations,
        },
        fails,
        dependencies=("T_orbit_mixture_constructs_disk",),
        premises=("AFFINE_EFFECT_SOUNDNESS", "SHARP_ANTIPODAL_EFFECT"),
        negative_controls=("every scanned nonzero tilt violates [0,1] at a computed orbit point",),
    )


def check_T_live_apf_generator_closure() -> Dict[str, object]:
    fails: List[str] = []
    # Live APF matrices: E_d1=(I+sz)/2, F_Pi=sx/2.  Add central J=iI after the circle.
    I = [[F(1), F(0)], [F(0), F(1)]]
    sx = [[F(0), F(1)], [F(1), F(0)]]
    sz = [[F(1), F(0)], [F(0), F(-1)]]
    Ed1 = [[F(1), F(0)], [F(0), F(0)]]
    FPi = [[F(0), F(1, 2)], [F(1, 2), F(0)]]
    Z = [[F(0), F(0)], [F(0), F(0)]]
    I4 = _realify_complex_2(I, Z)
    Ed1r = _realify_complex_2(Ed1, Z)
    FPir = _realify_complex_2(FPi, Z)
    Jr = _realify_complex_2(Z, I)
    basis = _star_closure([Ed1r, FPir, Jr])
    dim = _rank([_flatten(x) for x in basis])
    no_fpi = _star_closure([Ed1r, Jr])
    no_j = _star_closure([Ed1r, FPir])
    dim_no_fpi = _rank([_flatten(x) for x in no_fpi])
    dim_no_j = _rank([_flatten(x) for x in no_j])
    if dim != 8:
        fails.append(f"live generator set should generate realified M2(C), got dimension {dim}")
    if dim_no_fpi >= 8:
        fails.append("removing F_Pi must kill generator completeness")
    if dim_no_j >= 8:
        fails.append("removing central J must kill complex closure")
    # J central and square -I.
    J2 = _mmn(Jr, Jr)
    minusI4 = [[-x for x in row] for row in I4]
    if J2 != minusI4:
        fails.append("realified central J must square to -I")
    if _mmn(Jr, Ed1r) != _mmn(Ed1r, Jr) or _mmn(Jr, FPir) != _mmn(FPir, Jr):
        fails.append("central J must commute with live APF generators")
    return _result(
        "T_live_apf_generator_closure",
        "Using the live APF identifications E_d1=(I+sigma_z)/2 and F_Pi=sigma_x/2, adjoining the derived central quarter-turn J generates the full realification of M2(C), real dimension eight.  Removing F_Pi or J is detected.  This is an actual-generator closure, not a declared basis comparison.",
        {
            "generated_dimension": dim,
            "dimension_without_F_Pi": dim_no_fpi,
            "dimension_without_J": dim_no_j,
            "live_source_coderefs": ["check_T_alg_FPi (core.py)", "T_central_complex_block_exclusion (held_holonomy.py)"],
            "J_squared_minus_identity": True,
        },
        fails,
        dependencies=("T_one_gate_dense_held_circle",),
        premises=("GENERATOR_COMPLETENESS_FOR_TARGET_FRAGMENT", "ORIENTATION_SYNCHRONIZATION"),
        negative_controls=("remove F_Pi", "remove J"),
    )


COMMON_PHYSICAL_ROOTS = (
    "FINITE_FIRST_ORDER_HELD_CARRIER",
    "NONZERO_OCCUPIED_HELD_PROFILE",
    "FINITE_SEPARATING_READOUT",
    "NORMALIZED_PROFILE_PRESERVATION",
    "REVERSIBLE_GATE_ACTION",
    "CLASSICAL_RANDOMIZATION_CLOSURE",
    "EFFECTIVE_GATE_ACTION",
    "RECOMBINATION_EFFECT_WITNESS",
    # downstream gates intentionally retained:
    "AFFINE_EFFECT_SOUNDNESS",
    "SHARP_ANTIPODAL_EFFECT",
    "GENERATOR_COMPLETENESS_FOR_TARGET_FRAGMENT",
    "ORIENTATION_SYNCHRONIZATION",
    "POSITIVE_STATE_SOUNDNESS",
    "FINITE_RECORD_LABELLED_DILATION",
)

DIRECT_GATE_ROOTS = (
    "EXACT_REVERSIBLE_IRRATIONAL_HELD_GATE_DERIVATION",
)

REFLECTION_GATE_ROOTS = (
    "CODESPACE_TO_HELD_CARRIER_IDENTIFICATION",
    "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY",
)


def _dependency_graph(gate_route: str) -> Dict[str, Tuple[str, ...]]:
    if gate_route == "direct":
        gate_node = "T_DIRECT_GATE"
        gate_dep = ("EXACT_REVERSIBLE_IRRATIONAL_HELD_GATE_DERIVATION",)
    elif gate_route == "reflection":
        gate_node = "T_REFLECTION_GATE"
        gate_dep = (
            "T_APF_345_PROJECTORS",
            "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY",
        )
    else:
        raise ValueError("gate_route must be direct or reflection")
    graph: Dict[str, Tuple[str, ...]] = {
        "T_APF_345_PROJECTORS": ("CODESPACE_TO_HELD_CARRIER_IDENTIFICATION",),
        gate_node: gate_dep,
        "T_BOUNDED_CYCLIC_CLOSURE": (
            gate_node,
            "NONZERO_OCCUPIED_HELD_PROFILE",
            "FINITE_SEPARATING_READOUT",
            "NORMALIZED_PROFILE_PRESERVATION",
            "REVERSIBLE_GATE_ACTION",
        ),
        "T_INFINITE_ORDER": ("T_BOUNDED_CYCLIC_CLOSURE",),
        "T_ONE_GATE_CIRCLE": ("T_INFINITE_ORDER", "EFFECTIVE_GATE_ACTION"),
        "T_ORBIT_DISK": (
            "T_ONE_GATE_CIRCLE",
            "FINITE_FIRST_ORDER_HELD_CARRIER",
            "CLASSICAL_RANDOMIZATION_CLOSURE",
            "RECOMBINATION_EFFECT_WITNESS",
        ),
        "T_BORN_FRINGE": ("T_ORBIT_DISK", "AFFINE_EFFECT_SOUNDNESS", "SHARP_ANTIPODAL_EFFECT"),
        "T_COMPLEX_BLOCK": (
            "T_ONE_GATE_CIRCLE",
            "GENERATOR_COMPLETENESS_FOR_TARGET_FRAGMENT",
            "ORIENTATION_SYNCHRONIZATION",
        ),
        "T_BORN_TRACE": ("T_COMPLEX_BLOCK", "POSITIVE_STATE_SOUNDNESS"),
        "T_CP": ("T_COMPLEX_BLOCK", "FINITE_RECORD_LABELLED_DILATION"),
    }
    # On the direct route the APF projector node is provenance only, not a dependency.
    if gate_route == "direct":
        graph.pop("T_APF_345_PROJECTORS")
    return graph



def _roots(graph: Mapping[str, Sequence[str]]) -> Tuple[str, ...]:
    nodes = set(graph)
    deps = {d for vs in graph.values() for d in vs}
    return tuple(sorted(d for d in deps if d not in nodes))


def _cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    all_nodes = set(graph) | {d for vs in graph.values() for d in vs}
    state: Dict[str, int] = {n: 0 for n in all_nodes}
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
            if c:
                return c
        stack.pop()
        state[n] = 2
        return None

    for n in all_nodes:
        c = dfs(n)
        if c:
            return c
    return None


def check_T_one_gate_dependency_contract() -> Dict[str, object]:
    fails: List[str] = []
    direct = _dependency_graph("direct")
    reflection = _dependency_graph("reflection")
    direct_roots = _roots(direct)
    reflection_roots = _roots(reflection)
    expected_direct = tuple(sorted(COMMON_PHYSICAL_ROOTS + DIRECT_GATE_ROOTS))
    expected_reflection = tuple(sorted(COMMON_PHYSICAL_ROOTS + REFLECTION_GATE_ROOTS))
    if direct_roots != expected_direct:
        fails.append(f"direct-route roots differ from manifest: {direct_roots} != {expected_direct}")
    if reflection_roots != expected_reflection:
        fails.append(
            f"reflection-route roots differ from manifest: {reflection_roots} != {expected_reflection}"
        )
    direct_cycle = _cycle(direct)
    reflection_cycle = _cycle(reflection)
    if direct_cycle is not None:
        fails.append(f"direct dependency graph contains cycle: {direct_cycle}")
    if reflection_cycle is not None:
        fails.append(f"reflection dependency graph contains cycle: {reflection_cycle}")
    forbidden = {"CONNECTED_EFFECTIVE_HELD_SWEEP", "CLOSED_NORMALIZED_STATE_BODY",
                 "QUADRATIC_LEDGER", "PULLBACK_NONEXPANSION"}
    if forbidden & set(direct_roots + reflection_roots):
        fails.append("excluded roots re-entered (connected-sweep/state-body withdrawn from this route; PULLBACK_NONEXPANSION killed; QUADRATIC_LEDGER not consumed -- RELOCATED at reading grade per check_L_bounded_orbit_positivity v24.3.431)")

    mutated = dict(direct)
    mutated["T_ONE_GATE_CIRCLE"] = mutated["T_ONE_GATE_CIRCLE"] + ("SECOND_EMPIRICAL_ROOT",)
    root_mutation_caught = _roots(mutated) != expected_direct
    if not root_mutation_caught:
        fails.append("added empirical root mutation was not caught")

    finite_gate = ((F(0), F(-1)), (F(1), F(0)))
    finite_gate_trace_rejected = _trace(finite_gate) in {F(-2), F(-1), F(0), F(1), F(2)}
    if not finite_gate_trace_rejected:
        fails.append("finite-order quarter-turn control not recognized")

    return _result(
        "T_one_gate_dependency_contract",
        "The one-gate theorem supports two honest alternatives.  The direct route requires one physically calibrated reversible irrational gate.  The projector route instead requires a codespace-to-Held-carrier identification and physical implementation of the two sharp reflections.  Both routes remove CONNECTED_EFFECTIVE_HELD_SWEEP and a separately assumed CLOSED_NORMALIZED_STATE_BODY; bounded two-sided cyclic orbit plus finite normalized readout supplies compact closure.",
        {
            "direct_graph": {k: list(v) for k, v in direct.items()},
            "reflection_graph": {k: list(v) for k, v in reflection.items()},
            "direct_roots": list(direct_roots),
            "reflection_roots": list(reflection_roots),
            "direct_cycle": direct_cycle,
            "reflection_cycle": reflection_cycle,
            "connected_sweep_present": False,
            "closed_global_state_body_premise_present": False,
            "quadratic_ledger_present": False,
            "gate_routes_are_alternatives": True,
            "root_mutation_caught": root_mutation_caught,
            "finite_order_gate_control_caught": finite_gate_trace_rejected,
        },
        fails,
        dependencies=tuple(sorted(set(direct) | set(reflection))),
        premises=tuple(sorted(set(expected_direct) | set(expected_reflection))),
        negative_controls=("add SECOND_EMPIRICAL_ROOT", "replace gate by order-four J", "insert quadratic ledger"),
        epistemic="P_structural_instrument",
    )



def check_T_source_concordance_and_nonclaim() -> Dict[str, object]:
    fails: List[str] = []
    source_rows = {
        "first_order_rank_two": "Paper 10: Elementary bipolar comparison lift",
        "345_projector_geometry": "reproduce_inline_345_commutator (ijc_boolean_defender_bridge.py)",
        "live_generators": "check_T_alg_FPi (core.py)",
        "relative_loop_effectiveness": "T_held_relative_loop_group / T_held_recombination_nontriviality",
        "infinite_order_certificate_prior_art": (
            "T_held_connected_subgroup_so2 H3 battery (_held_holonomy_groups.py): "
            "executed Gaussian-integer non-associate-primes certificate for the "
            "cos=3/5 rotation R35; this packet's gate is its exact square "
            "(R = R35^2, -7+24i = (3+4i)^2 = (2+i)^4), and the certificate is "
            "ported here as the primary infinite-order leg"),
    }
    missing_physical_rows = {
        "direct_gate": "EXACT_REVERSIBLE_IRRATIONAL_HELD_GATE_DERIVATION",
        "projector_route_bridge": "CODESPACE_TO_HELD_CARRIER_IDENTIFICATION",
        "reflection_processes": "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY",
        "real_interface_evidence": "RAW_COUNTS_AND_DEVICE_CALIBRATION",
        "finite_data_exactness_limit": "EXACT_GATE_RELATION_CANNOT_BE_INFERRED_FROM_FINITE_PRECISION",
    }
    if set(source_rows) & set(missing_physical_rows):
        fails.append("source and missing-physical rows must remain disjoint")
    return _result(
        "T_source_concordance_and_nonclaim",
        "The live APF engine already supplies the first-order carrier theorem, the exact 3-4-5 projector geometry, the noncommuting generator pair, the relative-loop/effectiveness discipline, and the executed Gaussian-integer infinite-order certificate for the cos=3/5 rotation whose exact square is this packet's gate (banked H3 prior art, disclosed).  It does not yet supply a physical infinite-order Held gate, a codespace-to-first-jet identification, or sharp-reflection implementability.  The package therefore advances a finite certificate target rather than claiming closure.",
        {"live_sources": source_rows, "still_missing": missing_physical_rows, "headline_license": "research route, not APF closure"},
        fails,
        dependencies=("T_apf_345_projector_pair", "T_live_apf_generator_closure", "T_one_gate_dependency_contract"),
        epistemic="P_structural_instrument",
    )


# ---------------------------------------------------------------------------
# Physical interface certificate schema and verifier
# ---------------------------------------------------------------------------

REQUIRED_COMMON_EVIDENCE_FIELDS = (
    "evidence_class",
    "source_digest",
    "finite_first_order_carrier_certified",
    "occupied_nonzero_profile_certified",
    "finite_separating_readout_certified",
    "classical_randomization_certified",
    "capacity_bounded_orbit_certified",
    "effective_gate_action_certified",
    "recombination_effect_witness_certified",
)


def verify_physical_interface_certificate(payload: Mapping[str, object]) -> Dict[str, object]:
    """Fail-closed verifier with separate exact and finite-resolution verdicts.

    An exact infinite-order conclusion is licensed only for an exact structural
    derivation.  Experimental or device-calibration payloads may certify a
    finite-resolution orbit cover, but finite precision never proves exact
    irrationality.  The exact-path gate test requires determinant one,
    ELLIPTICITY (|trace| < 2; audit MAJOR-1 -- hyperbolic and parabolic gates
    such as the SO(1,1) boost are rejected outright), and a nonintegral
    rational trace.
    """
    missing = [k for k in REQUIRED_COMMON_EVIDENCE_FIELDS if k not in payload]
    failures: List[str] = []
    if missing:
        failures.append("missing fields: " + ", ".join(missing))
    evidence_class = str(payload.get("evidence_class", ""))
    allowed = {"structural_derivation", "experiment", "device_calibration", "synthetic_reference"}
    if evidence_class not in allowed:
        failures.append("unknown evidence_class")
    digest = str(payload.get("source_digest", ""))
    if evidence_class != "synthetic_reference" and len(digest) < 32:
        failures.append("physical evidence requires a nonempty source digest")
    bool_fields = [k for k in REQUIRED_COMMON_EVIDENCE_FIELDS if k.endswith("_certified")]
    false_fields = [k for k in bool_fields if payload.get(k) is not True]
    if false_fields:
        failures.append("uncertified physical leaves: " + ", ".join(false_fields))

    gate_raw = payload.get("gate_matrix")
    gate_ok = False
    trace = None
    det = None
    if gate_raw is not None:
        try:
            gate: Matrix2 = tuple(tuple(F(str(x)) for x in row) for row in gate_raw)  # type: ignore[assignment]
            trace = _trace(gate)
            det = _det(gate)
            gate_ok, gate_reasons = _elliptic_gate_ok(gate)
            if not gate_ok:
                failures.append(
                    "gate matrix does not pass the determinant-one/elliptic/"
                    "nonintegral-rational-trace test: " + "; ".join(gate_reasons))
        except Exception as exc:
            failures.append(f"invalid gate_matrix: {exc}")
    else:
        failures.append("missing gate_matrix")

    exact_relation = payload.get("exact_gate_relation_certified") is True
    finite_cover = payload.get("finite_resolution_orbit_cover_certified") is True
    common_ok = not missing and not false_fields and (evidence_class in allowed) and (len(digest) >= 32 or evidence_class == "synthetic_reference")
    exact_certified = (
        common_ok
        and not failures
        and evidence_class == "structural_derivation"
        and exact_relation
        and gate_ok
    )
    finite_resolution_certified = (
        common_ok
        and evidence_class in {"experiment", "device_calibration"}
        and finite_cover
        and len(digest) >= 32
    )
    # Exact theorem licensing is intentionally stricter than finite-resolution
    # operational certification.
    return {
        "passed_schema": not missing,
        "mathematical_gate_check": gate_ok,
        "exact_gate_relation_certified": exact_relation,
        "finite_resolution_interface_certified": finite_resolution_certified,
        "physical_premises_certified": exact_certified,
        "evidence_class": evidence_class,
        "trace": str(trace) if trace is not None else None,
        "determinant": str(det) if det is not None else None,
        "finite_precision_exactness_bar": evidence_class in {"experiment", "device_calibration"},
        "failures": failures,
    }



def check_T_reference_interface_certificate_fail_closed() -> Dict[str, object]:
    fails: List[str] = []
    _, _, r, _ = _reflection_product_gate()
    base = {
        "source_digest": "a" * 64,
        "finite_first_order_carrier_certified": True,
        "occupied_nonzero_profile_certified": True,
        "finite_separating_readout_certified": True,
        "classical_randomization_certified": True,
        "capacity_bounded_orbit_certified": True,
        "effective_gate_action_certified": True,
        "recombination_effect_witness_certified": True,
        "gate_matrix": _matrix_strings(r),
    }
    synthetic = dict(base, evidence_class="synthetic_reference",
                     exact_gate_relation_certified=True,
                     finite_resolution_orbit_cover_certified=True)
    rep = verify_physical_interface_certificate(synthetic)
    if rep["physical_premises_certified"] or rep["finite_resolution_interface_certified"]:
        fails.append("synthetic reference must never certify a physical interface")

    experimental = dict(base, evidence_class="experiment",
                        exact_gate_relation_certified=False,
                        finite_resolution_orbit_cover_certified=True)
    rep_exp = verify_physical_interface_certificate(experimental)
    if rep_exp["physical_premises_certified"]:
        fails.append("finite experimental data must not certify exact infinite order")
    if not rep_exp["finite_resolution_interface_certified"]:
        fails.append("complete experimental finite-cover payload should certify finite resolution")

    structural = dict(base, evidence_class="structural_derivation",
                      exact_gate_relation_certified=True,
                      finite_resolution_orbit_cover_certified=True)
    rep_struct = verify_physical_interface_certificate(structural)
    if not rep_struct["physical_premises_certified"]:
        fails.append("complete structural exact-gate payload should pass the exact verifier")

    empty = dict(structural, source_digest="")
    rep_empty = verify_physical_interface_certificate(empty)
    if rep_empty["physical_premises_certified"]:
        fails.append("empty-digest structural mutation must fail closed")

    finite = dict(structural, gate_matrix=[["0", "-1"], ["1", "0"]])
    rep_finite = verify_physical_interface_certificate(finite)
    if rep_finite["physical_premises_certified"]:
        fails.append("finite-order gate mutation must fail closed")

    # Audit MAJOR-1: the SO(1,1) boost payload MUST be rejected by the
    # elliptic gate.  This is verbatim mutation (5) of the rulings' return bar.
    boost_payload = dict(structural, gate_matrix=[["5/4", "3/4"], ["3/4", "5/4"]])
    rep_boost = verify_physical_interface_certificate(boost_payload)
    if rep_boost["physical_premises_certified"] or rep_boost["mathematical_gate_check"]:
        fails.append("SO(1,1) boost payload must be rejected by the elliptic verifier gate")
    if not any("elliptic" in f for f in rep_boost["failures"]):
        fails.append("boost rejection must name the elliptic condition")

    # Audit m3: trace-set-weakening controls.  Each finite-order or
    # non-elliptic trace payload must fail closed at verifier level, so
    # silently dropping a member of the finite-order trace set is caught.
    trace_control_payloads = {
        "order_3_trace_minus_1": [["-1/2", "-1"], ["3/4", "-1/2"]],
        "order_6_trace_plus_1": [["1/2", "-1"], ["3/4", "1/2"]],
        "unipotent_shear_trace_2": [["1", "1"], ["0", "1"]],
        "hyperbolic_trace_4": [["3", "1"], ["2", "1"]],
    }
    trace_set_controls: Dict[str, Dict[str, object]] = {}
    for label, gm in trace_control_payloads.items():
        rep_c = verify_physical_interface_certificate(dict(structural, gate_matrix=gm))
        trace_set_controls[label] = {
            "physical_premises_certified": rep_c["physical_premises_certified"],
            "mathematical_gate_check": rep_c["mathematical_gate_check"],
            "trace": rep_c["trace"],
        }
        if rep_c["physical_premises_certified"] or rep_c["mathematical_gate_check"]:
            fails.append(f"trace-set control must fail closed: {label}")
    return _result(
        "T_reference_interface_certificate_fail_closed",
        "The verifier separates exact structural closure from finite-resolution experiment.  Synthetic evidence certifies neither.  Complete experimental data can certify a declared orbit cover but cannot prove exact irrationality.  Only a source-digested structural derivation of the exact gate relation can license the exact one-gate circle theorem; empty-digest, order-four, SO(1,1)-boost (elliptic gate, audit MAJOR-1), order-3/order-6/shear/hyperbolic trace-set controls all fail closed.",
        {
            "synthetic_result": rep,
            "experimental_finite_resolution_result": rep_exp,
            "structural_exact_result": rep_struct,
            "empty_digest_mutation": rep_empty,
            "finite_gate_mutation": rep_finite,
            "boost_gate_mutation": {
                "physical_premises_certified": rep_boost["physical_premises_certified"],
                "mathematical_gate_check": rep_boost["mathematical_gate_check"],
                "trace": rep_boost["trace"],
                "failures": rep_boost["failures"],
            },
            "trace_set_controls": trace_set_controls,
        },
        fails,
        dependencies=("T_one_gate_dependency_contract", "T_finite_precision_cannot_certify_infinite_order"),
        negative_controls=("synthetic evidence", "finite-precision exactness claim", "empty digest", "finite-order gate", "SO(1,1) boost (elliptic gate)", "trace-set weakening (order-3/6, shear, hyperbolic)"),
        epistemic="P_structural_instrument",
    )


CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_apf_345_projector_pair": check_T_apf_345_projector_pair,
    "T_reflection_product_irrational_gate": check_T_reflection_product_irrational_gate,
    "T_bounded_cyclic_orbit_compact_closure": check_T_bounded_cyclic_orbit_compact_closure,
    "T_rational_trace_forces_infinite_order": check_T_rational_trace_forces_infinite_order,
    "T_finite_precision_cannot_certify_infinite_order": check_T_finite_precision_cannot_certify_infinite_order,
    "T_one_gate_dense_held_circle": check_T_one_gate_dense_held_circle,
    "T_orbit_mixture_constructs_disk": check_T_orbit_mixture_constructs_disk,
    "T_finite_resolution_orbit_cover": check_T_finite_resolution_orbit_cover,
    "T_born_fringe_from_one_gate_circle": check_T_born_fringe_from_one_gate_circle,
    "T_live_apf_generator_closure": check_T_live_apf_generator_closure,
    "T_one_gate_dependency_contract": check_T_one_gate_dependency_contract,
    "T_source_concordance_and_nonclaim": check_T_source_concordance_and_nonclaim,
    "T_reference_interface_certificate_fail_closed": check_T_reference_interface_certificate_fail_closed,
}


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in CHECKS.items()}


def build_certificate(results: Mapping[str, Mapping[str, object]]) -> OneGateCertificate:
    def ok(name: str) -> bool:
        return bool(results[name]["passed"])
    return OneGateCertificate(
        projector_pair_exact=ok("T_apf_345_projector_pair"),
        reflection_product_exact=ok("T_reflection_product_irrational_gate"),
        rational_trace_infinite_order=ok("T_rational_trace_forces_infinite_order"),
        finite_precision_exactness_guard=ok("T_finite_precision_cannot_certify_infinite_order"),
        compact_closure_circle=ok("T_one_gate_dense_held_circle"),
        connected_sweep_not_required=bool(results["T_one_gate_dense_held_circle"]["artifacts"]["connected_sweep_required"] is False),
        orbit_mixture_disk=ok("T_orbit_mixture_constructs_disk"),
        finite_resolution_cover=ok("T_finite_resolution_orbit_cover"),
        born_fringe=ok("T_born_fringe_from_one_gate_circle"),
        generator_closure=ok("T_live_apf_generator_closure"),
        source_concordance_honest=ok("T_source_concordance_and_nonclaim"),
        physical_gate_realized=False,
        finite_resolution_interface_certified=False,
        physical_premises_certified=False,
    )


def main() -> int:
    results = run_all()
    cert = build_certificate(results)
    payload = {"family": FAMILY, "certificate": asdict(cert), "results": results}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if all(r["passed"] for r in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())


# Bank-landing registration wiring (v24.3.432): standard registry hook.
_BANK_CHECKS = {
    "T_apf_345_projector_pair": check_T_apf_345_projector_pair,
    "T_reflection_product_irrational_gate": check_T_reflection_product_irrational_gate,
    "T_bounded_cyclic_orbit_compact_closure": check_T_bounded_cyclic_orbit_compact_closure,
    "T_rational_trace_forces_infinite_order": check_T_rational_trace_forces_infinite_order,
    "T_finite_precision_cannot_certify_infinite_order": check_T_finite_precision_cannot_certify_infinite_order,
    "T_one_gate_dense_held_circle": check_T_one_gate_dense_held_circle,
    "T_orbit_mixture_constructs_disk": check_T_orbit_mixture_constructs_disk,
    "T_finite_resolution_orbit_cover": check_T_finite_resolution_orbit_cover,
    "T_born_fringe_from_one_gate_circle": check_T_born_fringe_from_one_gate_circle,
    "T_live_apf_generator_closure": check_T_live_apf_generator_closure,
    "T_one_gate_dependency_contract": check_T_one_gate_dependency_contract,
    "T_source_concordance_and_nonclaim": check_T_source_concordance_and_nonclaim,
    "T_reference_interface_certificate_fail_closed": check_T_reference_interface_certificate_fail_closed,
}


def register(registry):
    registry.update(_BANK_CHECKS)
    return registry
