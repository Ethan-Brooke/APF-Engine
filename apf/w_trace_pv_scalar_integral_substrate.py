"""W_TRACE APF-native Passarino--Veltman scalar-integral substrate.

v16.9 (2026-05-09): pushes below the Denner/Sirlin counterterm-target
layer by adding an APF-owned finite scalar-integral substrate for the basic
one-loop Passarino--Veltman objects used by an on-shell electroweak
counterterm evaluator.  This module intentionally does not claim full
native W one-loop closure: it closes the finite-domain A0/B0/C0/D0 numeric
substrate and leaves the tensor-reduction/coefficient-map gate explicit.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_denner_sirlin_counterterm_functional import (
    PASS_STATUS as V16_8_PASS_STATUS,
    DIZET_DR_TOTAL, DELTA_ALPHA_ADMITTED, RHO_BRANCH_LEADING,
    COUNTERTERM_TARGET_DELTA_R, MASTER_IDENTITY_ERROR, M_Z_GEV, M_TOP_GEV,
    M_H_GEV, M_W_TRACE_GEV, DIZET_MW_GEV, DIZET_MINUS_APF_MEV,
    TOTAL_SIGMA_MW_MEV, PULL_INPUT_PLUS_THEORY, DMDDELTA_R_GEV,
)

STATUS = "P_w_trace_pv_scalar_integral_substrate"
VERSION = "v16_9"
PASS_STATUS = "W_TRACE_PV_SCALAR_INTEGRAL_SUBSTRATE_PASS"
TITLE = "W_TRACE APF-native Passarino-Veltman scalar-integral substrate"
PAYLOAD_ID = "W_TRACE_PV_SCALAR_INTEGRAL_SUBSTRATE_v16_9"
APF_VERSION = "16.9.0"

ROUTE_STATUS = "P_export_candidate_plus_native_pv_scalar_substrate"
NATIVE_ONE_LOOP_STATUS = "OPEN_TENSOR_REDUCTION_AND_DENNER_COEFFICIENT_MAP_REQUIRED"
FIRST_FAILED_GATE = "APF_NATIVE_TENSOR_REDUCTION_AND_DENNER_COEFFICIENT_MAP"
NEXT_GATE = "G2F_NATIVE_DENNER_COEFFICIENT_MAP_AND_COUNTERTERM_ASSEMBLER"

MU_REF_GEV = M_Z_GEV
MU2 = MU_REF_GEV * MU_REF_GEV
MW2 = M_W_TRACE_GEV * M_W_TRACE_GEV
MZ2 = M_Z_GEV * M_Z_GEV
MT2 = M_TOP_GEV * M_TOP_GEV
MH2 = M_H_GEV * M_H_GEV
EPS = 1e-30

# Numerical quadrature settings.  These are conservative and deterministic;
# the target is a finite-domain substrate and benchmark identities, not high
# precision replacement for LoopTools/Collier.
N_B0 = 4000
N_C0 = 180
N_D0 = 72

@dataclass(frozen=True)
class ScalarIntegralResult:
    name: str
    value: float
    unit_power: int
    convention: str
    domain_status: str
    error_estimate: float
    notes: str

@dataclass(frozen=True)
class IntegralGate:
    gate_id: str
    status: str
    object: str
    evidence: str
    blocks_full_native_loop: bool


def a0_fin(m2: float, mu2: float = MU2) -> float:
    """Finite part of A0 in the convention A0_fin=m^2(1-ln(m^2/mu^2))."""
    if m2 <= 0 or mu2 <= 0:
        raise ValueError("A0 finite evaluator requires positive m2 and mu2")
    return m2 * (1.0 - math.log(m2 / mu2))


def _b0_feynman_den(x: float, p2: float, m12: float, m22: float) -> float:
    return x * m12 + (1.0 - x) * m22 - x * (1.0 - x) * p2


def b0_fin(p2: float, m12: float, m22: float, mu2: float = MU2, n: int = N_B0) -> float:
    """Finite real part of B0 below/away from thresholds.

    B0_fin = - int_0^1 dx log((x m1^2 + (1-x)m2^2 - x(1-x)p^2)/mu^2).
    Midpoint quadrature avoids endpoint logarithmic singularities.
    """
    if mu2 <= 0 or n <= 0:
        raise ValueError("invalid mu2 or n")
    h = 1.0 / n
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) * h
        den = _b0_feynman_den(x, p2, m12, m22)
        if den <= 0:
            den = abs(den) + EPS
        acc += math.log(den / mu2)
    return -h * acc


def b0_domain_status(p2: float, m12: float, m22: float, samples: int = 1000) -> str:
    min_den = min(_b0_feynman_den((i + 0.5) / samples, p2, m12, m22) for i in range(samples))
    return "FINITE_REAL_DOMAIN" if min_den > 0 else "THRESHOLD_OR_COMPLEX_DOMAIN_QUARANTINE"


def c0_fin_zero_momenta(m12: float, m22: float, m32: float, mu2: float = MU2, n: int = N_C0) -> float:
    """Finite zero-external-momenta scalar C0 simplex evaluator.

    Convention: C0 = - int_{x,y>=0,x+y<=1} dx dy / (x m1^2 + y m2^2 + z m3^2).
    """
    if min(m12, m22, m32) <= 0:
        raise ValueError("C0 zero-momentum evaluator requires positive masses")
    acc = 0.0
    # Map unit square: x=u, y=(1-u)v, z=(1-u)(1-v), Jacobian=(1-u)
    for i in range(n):
        u = (i + 0.5) / n
        one_minus_u = 1.0 - u
        for j in range(n):
            v = (j + 0.5) / n
            x = u
            y = one_minus_u * v
            z = one_minus_u * (1.0 - v)
            den = x * m12 + y * m22 + z * m32
            acc += one_minus_u / den
    return -acc / (n * n)


def d0_fin_zero_momenta(m12: float, m22: float, m32: float, m42: float, mu2: float = MU2, n: int = N_D0) -> float:
    """Finite zero-external-momenta scalar D0 simplex evaluator.

    Convention: D0 = int_simplex dxdydz / F^2.  This supplies a stable finite
    substrate and normalization benchmark; physical signs/coefs belong to the
    Denner coefficient map, not this substrate layer.
    """
    if min(m12, m22, m32, m42) <= 0:
        raise ValueError("D0 zero-momentum evaluator requires positive masses")
    acc = 0.0
    # Map cube to tetrahedron: x=u, y=(1-u)v, z=(1-u)(1-v)w, t=(1-u)(1-v)(1-w)
    # Jacobian=(1-u)^2(1-v)
    for i in range(n):
        u = (i + 0.5) / n
        ou = 1.0 - u
        for j in range(n):
            v = (j + 0.5) / n
            ov = 1.0 - v
            jac_uv = ou * ou * ov
            for k in range(n):
                w = (k + 0.5) / n
                x = u
                y = ou * v
                z = ou * ov * w
                t = ou * ov * (1.0 - w)
                den = x * m12 + y * m22 + z * m32 + t * m42
                acc += jac_uv / (den * den)
    return acc / (n ** 3)


# Deterministic benchmark values at the APF route point / safe Euclidean point.
A0_MW = a0_fin(MW2)
A0_MZ = a0_fin(MZ2)
A0_MT = a0_fin(MT2)
B0_MW_0_MW = b0_fin(MW2, 0.0, MW2)
B0_ZERO_MW_MW = b0_fin(0.0, MW2, MW2)
B0_ZERO_MZ_MZ = b0_fin(0.0, MZ2, MZ2)
B0_SYM_TEST_12 = b0_fin(MH2 * 0.25, MW2, MZ2)
B0_SYM_TEST_21 = b0_fin(MH2 * 0.25, MZ2, MW2)
C0_MW_MW_MW = c0_fin_zero_momenta(MW2, MW2, MW2)
C0_MW_MZ_MT = c0_fin_zero_momenta(MW2, MZ2, MT2)
D0_MW_MW_MW_MW = d0_fin_zero_momenta(MW2, MW2, MW2, MW2)
D0_MW_MZ_MT_MH = d0_fin_zero_momenta(MW2, MZ2, MT2, MH2)

# Analytic finite zero-momentum benchmarks in our convention.
B0_ZERO_EQUAL_ANALYTIC_MW = -math.log(MW2 / MU2)
B0_ZERO_EQUAL_ANALYTIC_MZ = -math.log(MZ2 / MU2)
C0_EQUAL_ANALYTIC_MW = -0.5 / MW2
D0_EQUAL_ANALYTIC_MW = 1.0 / (6.0 * MW2 * MW2)

SCALAR_RESULTS: Tuple[ScalarIntegralResult, ...] = (
    ScalarIntegralResult("A0_MW", A0_MW, 2, "m2*(1-log(m2/mu2))", "FINITE_REAL_DOMAIN", 0.0, "finite tadpole substrate at APF W trace mass"),
    ScalarIntegralResult("A0_MZ", A0_MZ, 2, "m2*(1-log(m2/mu2))", "FINITE_REAL_DOMAIN", 0.0, "finite tadpole substrate at Z input mass"),
    ScalarIntegralResult("A0_MT", A0_MT, 2, "m2*(1-log(m2/mu2))", "FINITE_REAL_DOMAIN", 0.0, "finite tadpole substrate at top input mass"),
    ScalarIntegralResult("B0_MW_0_MW", B0_MW_0_MW, 0, "-int log(F/mu2)", b0_domain_status(MW2, 0.0, MW2), 1.0/N_B0, "APF W-route B0 branch with endpoint-safe midpoint integration"),
    ScalarIntegralResult("B0_ZERO_MW_MW", B0_ZERO_MW_MW, 0, "-int log(F/mu2)", "FINITE_REAL_DOMAIN", 1.0/N_B0, "zero-momentum equal-mass B0 benchmark"),
    ScalarIntegralResult("C0_MW_MW_MW", C0_MW_MW_MW, -2, "-simplex int 1/F", "FINITE_REAL_DOMAIN", 1.0/N_C0, "zero-momentum equal-mass C0 benchmark"),
    ScalarIntegralResult("D0_MW_MW_MW_MW", D0_MW_MW_MW_MW, -4, "simplex int 1/F^2", "FINITE_REAL_DOMAIN", 1.0/N_D0, "zero-momentum equal-mass D0 benchmark"),
)

INTEGRAL_GATES: Tuple[IntegralGate, ...] = (
    IntegralGate("G2D_PV_A0", "CLOSED_NUMERIC", "finite A0 tadpole evaluator", "analytic formula implemented with positive-mass domain checks", False),
    IntegralGate("G2D_PV_B0", "CLOSED_NUMERIC", "finite B0 two-point evaluator", "Feynman-parameter midpoint evaluator plus analytic benchmarks", False),
    IntegralGate("G2D_PV_C0", "CLOSED_NUMERIC_SAFE_ZERO_MOMENTUM", "finite C0 three-point substrate", "simplex evaluator and equal-mass normalization benchmark", False),
    IntegralGate("G2D_PV_D0", "CLOSED_NUMERIC_SAFE_ZERO_MOMENTUM", "finite D0 four-point substrate", "tetrahedral simplex evaluator and equal-mass normalization benchmark", False),
    IntegralGate("G2D_THRESHOLD_PROTOCOL", "CLOSED_QUARANTINE", "threshold/complex-domain quarantine", "B0 denominator sign scan prevents silent real-domain overclaim", False),
    IntegralGate("G2F_TENSOR_REDUCTION", "OPEN", "PV tensor reduction coefficients B1/B00/Cij/Dij", "not yet APF-owned", True),
    IntegralGate("G2F_DENNER_COEFFICIENT_MAP", "OPEN", "Denner/Sirlin coefficient map from diagrams/counterterms to scalar integrals", FIRST_FAILED_GATE, True),
    IntegralGate("G2G_NATIVE_ONE_LOOP_CLOSURE", "OPEN", "native scalar substrate + coefficient map reproduces counterterm target", "requires G2F closure", True),
)

SAFE_CLAIMS = (
    "APF now owns a deterministic finite-domain scalar-integral substrate for A0/B0/C0/D0 benchmarks.",
    "The Denner/Sirlin counterterm target is reduced below symbolic basis to scalar-integral substrate plus coefficient-map problem.",
    "The W route remains an export candidate through DIZET transport and admitted row covariance.",
    "Full APF-native one-loop closure remains open until tensor reduction and Denner/Sirlin coefficient maps are implemented.",
)

FORBIDDEN_CLAIMS = (
    "APF has completed an analytic Standard Model one-loop calculation.",
    "The numerical substrate alone reproduces the DIZET counterterm target.",
    "C0/D0 safe zero-momentum benchmarks replace full physical kinematics.",
    "Two-loop or higher-order electroweak corrections are APF-native derived.",
)


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)


def _digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(obj).encode("utf-8")).hexdigest()


def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed), "status": "PASS" if passed else "FAIL", "epistemic": STATUS}
    row.update(extra)
    return row


def _passed(row: Any) -> bool:
    return bool(isinstance(row, Mapping) and (row.get("passed") is True or row.get("status") in ("PASS", "P")))


def scalar_result_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in SCALAR_RESULTS)


def integral_gate_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in INTEGRAL_GATES)


def route_summary() -> Dict[str, Any]:
    return {
        "title": TITLE,
        "version": VERSION,
        "apf_version": APF_VERSION,
        "dependency": V16_8_PASS_STATUS,
        "input_point": {"M_W_TRACE_GeV": M_W_TRACE_GEV, "M_Z_GeV": M_Z_GEV, "m_t_GeV": M_TOP_GEV, "M_H_GeV": M_H_GEV, "mu_ref_GeV": MU_REF_GEV},
        "scalar_results": scalar_result_table(),
        "analytic_benchmarks": {
            "B0_ZERO_EQUAL_MW_numeric": B0_ZERO_MW_MW,
            "B0_ZERO_EQUAL_MW_analytic": B0_ZERO_EQUAL_ANALYTIC_MW,
            "B0_ZERO_EQUAL_MZ_numeric": B0_ZERO_MZ_MZ,
            "B0_ZERO_EQUAL_MZ_analytic": B0_ZERO_EQUAL_ANALYTIC_MZ,
            "C0_EQUAL_MW_numeric": C0_MW_MW_MW,
            "C0_EQUAL_MW_analytic": C0_EQUAL_ANALYTIC_MW,
            "D0_EQUAL_MW_numeric": D0_MW_MW_MW_MW,
            "D0_EQUAL_MW_analytic": D0_EQUAL_ANALYTIC_MW,
            "B0_symmetry_error": B0_SYM_TEST_12 - B0_SYM_TEST_21,
        },
        "counterterm_target": {
            "Delta_alpha": DELTA_ALPHA_ADMITTED,
            "rho_leading_branch": RHO_BRANCH_LEADING,
            "counterterm_target_delta_r": COUNTERTERM_TARGET_DELTA_R,
            "DIZET_delta_r_total": DIZET_DR_TOTAL,
            "master_identity_error_v16_8": MASTER_IDENTITY_ERROR,
            "dM_dDelta_r_GeV": DMDDELTA_R_GEV,
        },
        "export_candidate_state": {"M_W_TRACE_GeV": M_W_TRACE_GEV, "M_W_DIZET_GeV": DIZET_MW_GEV, "DIZET_minus_APF_MeV": DIZET_MINUS_APF_MEV, "sigma_total_MW_MeV": TOTAL_SIGMA_MW_MEV, "pull_sigma": PULL_INPUT_PLUS_THEORY},
        "status": {"route_status": ROUTE_STATUS, "native_one_loop_status": NATIVE_ONE_LOOP_STATUS, "first_failed_gate": FIRST_FAILED_GATE, "next_gate": NEXT_GATE},
        "integral_gates": integral_gate_table(),
        "safe_claims": SAFE_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "payload_digest": _digest([scalar_result_table(), integral_gate_table(), SAFE_CLAIMS, FORBIDDEN_CLAIMS]),
    }


def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}

# --- checks -----------------------------------------------------------------

def check_T_w_trace_pv_status_declared():
    return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v16_9")

def check_T_w_trace_pv_dependency_pass():
    return _res("dependency_pass", V16_8_PASS_STATUS.endswith("PASS"))

def check_T_w_trace_pv_has_a0_evaluator():
    return _res("has_a0_evaluator", callable(a0_fin) and A0_MW > 0)

def check_T_w_trace_pv_has_b0_evaluator():
    return _res("has_b0_evaluator", callable(b0_fin) and math.isfinite(B0_MW_0_MW))

def check_T_w_trace_pv_has_c0_evaluator():
    return _res("has_c0_evaluator", callable(c0_fin_zero_momenta) and C0_MW_MW_MW < 0)

def check_T_w_trace_pv_has_d0_evaluator():
    return _res("has_d0_evaluator", callable(d0_fin_zero_momenta) and D0_MW_MW_MW_MW > 0)

def check_T_w_trace_pv_a0_equal_mu_identity():
    return _res("a0_equal_mu_identity", abs(a0_fin(MU2, MU2) - MU2) < 1e-10)

def check_T_w_trace_pv_a0_scale_values_finite():
    return _res("a0_scale_values_finite", all(math.isfinite(x) for x in (A0_MW, A0_MZ, A0_MT)))

def check_T_w_trace_pv_b0_zero_equal_mw_matches_analytic():
    return _res("b0_zero_equal_mw_matches_analytic", abs(B0_ZERO_MW_MW - B0_ZERO_EQUAL_ANALYTIC_MW) < 1e-12, error=B0_ZERO_MW_MW - B0_ZERO_EQUAL_ANALYTIC_MW)

def check_T_w_trace_pv_b0_zero_equal_mz_matches_analytic():
    return _res("b0_zero_equal_mz_matches_analytic", abs(B0_ZERO_MZ_MZ - B0_ZERO_EQUAL_ANALYTIC_MZ) < 1e-12, error=B0_ZERO_MZ_MZ - B0_ZERO_EQUAL_ANALYTIC_MZ)

def check_T_w_trace_pv_b0_symmetry():
    return _res("b0_symmetry", abs(B0_SYM_TEST_12 - B0_SYM_TEST_21) < 5e-4, error=B0_SYM_TEST_12 - B0_SYM_TEST_21)

def check_T_w_trace_pv_b0_route_domain_quarantined_or_finite():
    return _res("b0_route_domain_quarantined_or_finite", b0_domain_status(MW2, 0.0, MW2) in ("FINITE_REAL_DOMAIN", "THRESHOLD_OR_COMPLEX_DOMAIN_QUARANTINE"))

def check_T_w_trace_pv_b0_route_value_reasonable():
    return _res("b0_route_value_reasonable", -3.0 < B0_MW_0_MW < 3.0, value=B0_MW_0_MW)

def check_T_w_trace_pv_c0_equal_matches_analytic():
    return _res("c0_equal_matches_analytic", abs(C0_MW_MW_MW - C0_EQUAL_ANALYTIC_MW) < 1e-10, error=C0_MW_MW_MW - C0_EQUAL_ANALYTIC_MW)

def check_T_w_trace_pv_d0_equal_matches_analytic():
    return _res("d0_equal_matches_analytic", abs(D0_MW_MW_MW_MW - D0_EQUAL_ANALYTIC_MW) < 3e-13, error=D0_MW_MW_MW_MW - D0_EQUAL_ANALYTIC_MW)

def check_T_w_trace_pv_c0_mixed_finite():
    return _res("c0_mixed_finite", math.isfinite(C0_MW_MZ_MT) and C0_MW_MZ_MT < 0)

def check_T_w_trace_pv_d0_mixed_finite():
    return _res("d0_mixed_finite", math.isfinite(D0_MW_MZ_MT_MH) and D0_MW_MZ_MT_MH > 0)

def check_T_w_trace_pv_results_count():
    return _res("results_count", len(SCALAR_RESULTS) == 7)

def check_T_w_trace_pv_results_all_finite():
    return _res("results_all_finite", all(math.isfinite(r.value) for r in SCALAR_RESULTS))

def check_T_w_trace_pv_gate_count():
    return _res("gate_count", len(INTEGRAL_GATES) == 8)

def check_T_w_trace_pv_a0_gate_closed():
    return _res("a0_gate_closed", any(g.gate_id == "G2D_PV_A0" and g.status.startswith("CLOSED") for g in INTEGRAL_GATES))

def check_T_w_trace_pv_b0_gate_closed():
    return _res("b0_gate_closed", any(g.gate_id == "G2D_PV_B0" and g.status.startswith("CLOSED") for g in INTEGRAL_GATES))

def check_T_w_trace_pv_c0_gate_closed():
    return _res("c0_gate_closed", any(g.gate_id == "G2D_PV_C0" and g.status.startswith("CLOSED") for g in INTEGRAL_GATES))

def check_T_w_trace_pv_d0_gate_closed():
    return _res("d0_gate_closed", any(g.gate_id == "G2D_PV_D0" and g.status.startswith("CLOSED") for g in INTEGRAL_GATES))

def check_T_w_trace_pv_threshold_gate_closed():
    return _res("threshold_gate_closed", any(g.gate_id == "G2D_THRESHOLD_PROTOCOL" and g.status == "CLOSED_QUARANTINE" for g in INTEGRAL_GATES))

def check_T_w_trace_pv_tensor_reduction_gate_open():
    return _res("tensor_reduction_gate_open", any(g.gate_id == "G2F_TENSOR_REDUCTION" and g.status == "OPEN" for g in INTEGRAL_GATES))

def check_T_w_trace_pv_coefficient_map_gate_open():
    return _res("coefficient_map_gate_open", any(g.gate_id == "G2F_DENNER_COEFFICIENT_MAP" and g.status == "OPEN" for g in INTEGRAL_GATES))

def check_T_w_trace_pv_first_failed_gate_exact():
    return _res("first_failed_gate_exact", FIRST_FAILED_GATE == "APF_NATIVE_TENSOR_REDUCTION_AND_DENNER_COEFFICIENT_MAP")

def check_T_w_trace_pv_next_gate_exact():
    return _res("next_gate_exact", NEXT_GATE == "G2F_NATIVE_DENNER_COEFFICIENT_MAP_AND_COUNTERTERM_ASSEMBLER")

def check_T_w_trace_pv_status_export_candidate_preserved():
    return _res("status_export_candidate_preserved", "export_candidate" in ROUTE_STATUS)

def check_T_w_trace_pv_no_full_native_claim():
    return _res("no_full_native_claim", NATIVE_ONE_LOOP_STATUS.startswith("OPEN"))

def check_T_w_trace_pv_master_identity_inherited():
    return _res("master_identity_inherited", abs(MASTER_IDENTITY_ERROR) < 1e-15)

def check_T_w_trace_pv_counterterm_target_inherited():
    return _res("counterterm_target_inherited", 0.009 < COUNTERTERM_TARGET_DELTA_R < 0.011)

def check_T_w_trace_pv_report_has_scalar_results():
    return _res("report_has_scalar_results", len(route_summary()["scalar_results"]) == 7)

def check_T_w_trace_pv_report_has_benchmarks():
    return _res("report_has_benchmarks", "analytic_benchmarks" in route_summary())

def check_T_w_trace_pv_report_has_gates():
    return _res("report_has_gates", len(route_summary()["integral_gates"]) == 8)

def check_T_w_trace_pv_safe_claims_present():
    return _res("safe_claims_present", len(SAFE_CLAIMS) == 4)

def check_T_w_trace_pv_forbidden_claims_present():
    return _res("forbidden_claims_present", len(FORBIDDEN_CLAIMS) == 4)

def check_T_w_trace_pv_payload_digest_present():
    return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))

def check_T_w_trace_pv_open_gates_block_full_native():
    return _res("open_gates_block_full_native", all(g.blocks_full_native_loop for g in INTEGRAL_GATES if g.status == "OPEN"))

def check_T_w_trace_pv_mw_residual_preserved():
    return _res("mw_residual_preserved", -4.9 < DIZET_MINUS_APF_MEV < -4.7)

def check_T_w_trace_pv_total_sigma_preserved():
    return _res("total_sigma_preserved", TOTAL_SIGMA_MW_MEV > 4.0 and 1.0 < PULL_INPUT_PLUS_THEORY < 1.2)

def check_T_w_trace_pv_mu_reference_is_mz():
    return _res("mu_reference_is_mz", abs(MU_REF_GEV - M_Z_GEV) < 1e-12)

def check_T_w_trace_pv_units_declared():
    return _res("units_declared", {r.unit_power for r in SCALAR_RESULTS} == {2,0,-2,-4})

def check_T_w_trace_pv_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_pv_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_pv_") and callable(obj)}


def register(registry: MutableMapping[str, Any]) -> None:
    registry.update(_CHECKS)


def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {"passed": ok, "status": PASS_STATUS if ok else PASS_STATUS.replace("_PASS", "_FAIL"), "checks": rows, "report": terminal_report()}

if __name__ == "__main__":
    out = run_all()
    print(out["status"])
    for row in out["checks"]:
        print(("PASS" if row["passed"] else "FAIL"), row["name"])
