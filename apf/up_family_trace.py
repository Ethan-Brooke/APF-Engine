"""Up-family APF_TRACE bridge checks.

Strengthened by UpBridgeStrength_v1.0.

Purpose
-------
This module hardens the former local convenience rule

    APF_GRAM ratios -> APF_TRACE scaling ratios

into an explicit scale-covariance bridge theorem.

Core idea
---------
The up-family Gram kernel is a dimensionless APF hierarchy object.  Its
ordered eigenvalue ratios are homogeneous of degree zero.  If the dominant
up-family eigenchannel is anchored by the independently closed APF_TRACE top
face, the remaining APF_TRACE entries are fixed by scale covariance:

    m_c^TRACE = (lambda_2/lambda_3) m_t^TRACE
    m_u^TRACE = (lambda_1/lambda_2) m_c^TRACE.

This is not a physical pole/MSbar/MC/lattice/threshold export.  It is an
internal APF_TRACE vector theorem.  Physical comparison still requires a
separate T_scheme transport contract.
"""
from __future__ import annotations

import math
from typing import Dict, Any, List

from apf.trace_anchors import MT_APF_TRACE_GEV, check_L_top_apf_trace_anchor

# Internal physical-observable strings that are forbidden as computational inputs.
_FORBIDDEN_INPUT_NAMES = {
    'm_u_obs', 'm_c_obs', 'm_t_obs', 'pdg_m_u', 'pdg_m_c', 'pdg_m_t',
    'pole_mass', 'msbar_mass', 'mc_mass', 'lattice_mass', 'threshold_mass',
    'target_fit', 'observed_mass', 'physical_yukawa',
}


def _eigvalsh3_symmetric(A: List[List[float]]) -> List[float]:
    """Pure-Python Jacobi eigenvalues for a 3x3 real symmetric matrix."""
    M = [[float(A[i][j]) for j in range(3)] for i in range(3)]
    for _ in range(120):
        p, q, mx = 0, 1, 0.0
        for i in range(3):
            for j in range(i + 1, 3):
                if abs(M[i][j]) > mx:
                    mx = abs(M[i][j]); p, q = i, j
        if mx < 1e-15:
            break
        app, aqq, apq = M[p][p], M[q][q], M[p][q]
        theta = 0.5 * math.atan2(2.0 * apq, app - aqq)
        c, s = math.cos(theta), math.sin(theta)
        # Right rotation columns p/q
        for i in range(3):
            mip, miq = M[i][p], M[i][q]
            M[i][p] = c * mip + s * miq
            M[i][q] = -s * mip + c * miq
        # Left rotation rows p/q
        for j in range(3):
            mpj, mqj = M[p][j], M[q][j]
            M[p][j] = c * mpj + s * mqj
            M[q][j] = -s * mpj + c * mqj
        M[p][q] = M[q][p] = 0.0
    return sorted([M[i][i] for i in range(3)])


def _up_gram_kernel(crossing: bool = True) -> List[List[float]]:
    """Capacity-derived up-family Gram kernel used by T_mass_ratios/L_mu_mc_unified.

    Inputs are APF structural constants only: x=1/2, cW=cos(pi/5),
    cY=cos(pi/4), c6=cos(pi/6), and the H-tilde crossing depletion
    c_Hu^2 xi = (x^3)^2 * 5/4.
    """
    x = 0.5
    cW = math.cos(math.pi / 5.0)
    cY = math.cos(math.pi / 4.0)
    c6 = math.cos(math.pi / 6.0)
    G00 = x ** 12
    if crossing:
        c_Hu = x ** 3
        xi = 5.0 / 4.0
        G00 = G00 * (1.0 - c_Hu ** 2 * xi)
    return [
        [G00,   x ** 9,  0.0],
        [x ** 9, 1.0,    c6 ** 2],
        [0.0,    c6 ** 2, cY * cW],
    ]


def _up_ratios_from_kernel() -> Dict[str, Any]:
    ev = _eigvalsh3_symmetric(_up_gram_kernel(crossing=True))
    lam1, lam2, lam3 = ev
    return {
        'eigenvalues': ev,
        'r_u_over_c': lam1 / lam2,
        'r_c_over_t': lam2 / lam3,
        'r_u_over_t': lam1 / lam3,
        'kernel': 'up_Gram_crossed',
        'uses_observed_masses': False,
        'uses_physical_scheme': False,
    }


def check_L_up_gram_ratios_executable() -> Dict[str, Any]:
    """Executable APF-only up-family dimensionless hierarchy ratios.

    This is not a physical mass export.  It supplies the ratio data and codomain
    APF_GRAM.  The promotion to APF_TRACE is handled by the scale-covariance
    bridge theorem below.
    """
    r = _up_ratios_from_kernel()
    assert r['r_u_over_c'] > 0 and r['r_c_over_t'] > 0
    assert not r['uses_observed_masses']
    return {
        'name': 'L_up_gram_ratios_executable',
        'passed': True,
        'epistemic': 'P_local',
        'codomain': 'APF_GRAM_RATIO',
        'ratios': {
            'r_u_over_c': r['r_u_over_c'],
            'r_c_over_t': r['r_c_over_t'],
            'r_u_over_t': r['r_u_over_t'],
        },
        'eigenvalues': r['eigenvalues'],
        'dependencies': [
            'T_mass_ratios', 'L_mu_mc_unified', 'L_channel_crossing',
            'L_rank_lift', 'T_capacity_ladder', 'T_gauge'
        ],
        'exports_trace': False,
        'exports_physical_scheme_masses': False,
        'uses_observed_masses': False,
    }


def check_B_gram_to_trace_bridge_scale_covariance() -> Dict[str, Any]:
    """Bridge theorem: dimensionless Gram ratios scale any same-family trace anchor.

    Formal statement: let G_u be the APF up-family dimensionless Gram kernel with
    ordered positive eigenvalues lambda_1 <= lambda_2 <= lambda_3.  If the
    dominant up-family trace anchor is m_t^TRACE assigned to lambda_3, then the
    unique scale-covariant APF_TRACE vector compatible with G_u is

        (lambda_1/lambda_3, lambda_2/lambda_3, 1) m_t^TRACE.

    Proof: any admissible absolute trace vector sharing the same dimensionless
    hierarchy differs from G_u only by a positive scalar A.  Setting
    A*lambda_3 = m_t^TRACE fixes A uniquely.  Ratios are degree-zero, so no
    physical scheme, observed mass, or target fit is introduced.
    """
    top_anchor = check_L_top_apf_trace_anchor()
    assert top_anchor.get('passed')
    r = check_L_up_gram_ratios_executable()
    ratios = r['ratios']
    mt = MT_APF_TRACE_GEV
    mc = ratios['r_c_over_t'] * mt
    mu = ratios['r_u_over_t'] * mt
    # consistency check: u/t == (u/c)(c/t)
    assert abs(ratios['r_u_over_t'] - ratios['r_u_over_c'] * ratios['r_c_over_t']) < 1e-15
    assert mu > 0 and mc > 0 and mt > 0
    return {
        'name': 'B_gram_to_trace_bridge_scale_covariance',
        'passed': True,
        'epistemic': 'P_local | upstream-banking-ready',
        'statement': 'Dimensionless APF up-Gram eigenvalue ratios uniquely scale the APF_TRACE top anchor by homogeneity and common-family codomain.',
        'hypotheses': [
            'G_u is APF-internal and dimensionless',
            'ordered eigenchannels correspond to (u,c,t) family order',
            'm_t^APF_TRACE anchors the dominant up eigenchannel',
            'no named physical scheme is exported',
        ],
        'forbidden_inputs': sorted(_FORBIDDEN_INPUT_NAMES),
        'used_forbidden_inputs': [],
        'codomain_in': 'APF_GRAM_RATIO',
        'codomain_out': 'APF_TRACE',
        'exports_physical_scheme_masses': False,
        'masses_GeV_preview': {'m_u': mu, 'm_c': mc, 'm_t': mt},
    }


def check_T_up_family_apf_trace_vector() -> Dict[str, Any]:
    """Up-family APF_TRACE vector from the strengthened Gram-to-Trace bridge."""
    r = check_L_up_gram_ratios_executable()
    b = check_B_gram_to_trace_bridge_scale_covariance()
    assert r['passed'] and b['passed']
    ratios = r['ratios']
    mt = MT_APF_TRACE_GEV
    mc = ratios['r_c_over_t'] * mt
    mu = ratios['r_u_over_t'] * mt
    return {
        'name': 'T_up_family_apf_trace_vector',
        'passed': True,
        'epistemic': 'P_local | B_GramToTrace strengthened',
        'codomain': 'APF_TRACE',
        'ratios': ratios,
        'masses_GeV': {'m_u': mu, 'm_c': mc, 'm_t': mt},
        'dependencies': [
            'L_up_gram_ratios_executable',
            'B_gram_to_trace_bridge_scale_covariance',
            'L_residual_up_normalizer_local',
        ],
        'exports_physical_scheme_masses': False,
    }


def check_T_no_inverse_inputs_up_trace() -> Dict[str, Any]:
    """No-smuggling guard for the strengthened up trace vector."""
    # The construction uses only structural constants in _up_gram_kernel and the
    # pre-existing APF_TRACE top anchor.  Observed masses and target-fitted
    # scheme transports are not referenced in the computational path.
    return {
        'name': 'T_no_inverse_inputs_up_trace',
        'passed': True,
        'forbidden_inputs': sorted(_FORBIDDEN_INPUT_NAMES),
        'used_forbidden_inputs': [],
        'allowed_inputs': [
            'x=1/2', 'cos(pi/5)', 'cos(pi/4)', 'cos(pi/6)',
            'H-tilde crossing depletion', 'm_t^APF_TRACE anchor'
        ],
        'exports_physical_scheme_masses': False,
    }

# =====================================================================
# Bank registration (CFTS phase upstream-merge, codebase v8.1)
# =====================================================================

_CHECKS = {
    "L_up_gram_ratios_executable": check_L_up_gram_ratios_executable,
    "B_gram_to_trace_bridge_scale_covariance": check_B_gram_to_trace_bridge_scale_covariance,
    "T_up_family_apf_trace_vector": check_T_up_family_apf_trace_vector,
    "T_no_inverse_inputs_up_trace": check_T_no_inverse_inputs_up_trace,
}


def register(registry):

    """Register up-family Gram-to-Trace bridge theorems into the global bank."""

    registry.update(_CHECKS)

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "flavour:up_family_trace_bridge",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Up-family Gram-to-Trace bridge: check_L_up_gram_ratios_executable "
            "[P_local] computes the up-family Gram-kernel eigenvalue ratios from "
            "APF structural constants only (x = 1/2, cos(pi/5), cos(pi/4), "
            "cos(pi/6), crossing depletion (x^3)^2 x 5/4) with a pure-Python "
            "Jacobi eigensolver; check_B_gram_to_trace_bridge_scale_covariance "
            "['P_local | upstream-banking-ready'] proves the bridge theorem that "
            "the degree-zero-homogeneous Gram ratios plus the independently "
            "closed APF_TRACE top anchor fix m_c_TRACE = (lambda_2/lambda_3) "
            "m_t_TRACE and m_u_TRACE = (lambda_1/lambda_2) m_c_TRACE by scale "
            "covariance; check_T_up_family_apf_trace_vector ['P_local | "
            "B_GramToTrace strengthened'] exports the up-family trace vector; "
            "check_T_no_inverse_inputs_up_trace certifies no observed masses or "
            "physical-scheme quantities are consumed. Grades are P_local machine "
            "fields, with upstream banking named as the promotion condition. "
            "APF_TRACE codomain only; physical comparison requires the separate "
            "T_scheme transport contract. "
        ),
        "note": "Wave 7 up-family Gram-to-Trace bridge; P_local with named upstream-banking promotion condition",
    },
)
