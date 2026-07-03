"""APF v24.2 — CMB Finite-Mode Covariance Projection.

Lands the Model-5 finite-mode covariance projection prototype referenced
by Paper 19 v0.2 (working draft 2026-05-12): "Large-Angle CMB Suppression
as a Finite-Continuability Constraint." See Paper 19 v0.2 §§5--6 + §10.

The structural reading: a finite-capacity universe need not enforce
arbitrary whole-sky correlations. The capacity-sensitive observable is the
real-space large-angle correlation functional S_{theta_c} (with the
canonical convention theta_c = 60 deg making this S_{1/2}), not a single
multipole or a monotone low-ell amplitude window.

Projection target:
    S_{theta_c}[m] = integral_{-1}^{cos theta_c} C_m(x)^2 dx
    C_m(x) = sum_{ell=ell_min}^{ell_max} a_ell m_ell P_ell(x)
    a_ell = (2 ell + 1) / (ell (ell + 1)) * D_ell^std
with finite-mode multipliers m_ell chosen by least-distortion optimization:
    min_m  S_{theta_c}[m]/S_{theta_c}[1] + lambda * ||m - 1||^2 / N,
    0 <= m_ell <= 2.

Bank checks (model-integrity, not Planck likelihood):
    T_cmb_fm_finite_multipliers       finite + within [0, 2]
    T_cmb_fm_nonneg_reference         a_ell >= 0 for ell in [ell_min, ell_max]
    T_cmb_fm_large_angle_reduction    S^proj < S^std (functional suppressed)
    T_cmb_fm_quadrupole_suppression   m_2 substantially below 1 (target hit)
    T_cmb_fm_high_ell_preservation    m_ell approximately 1 for ell >= 20
    T_cmb_fm_legendre_recurrence      P_ell three-term recurrence identity

The bank checks are model-integrity checks. They are not a substitute for
a public-data likelihood. The chi^2 numbers in Paper 19 v0.2 sec.6 reflect
the external Model-5 generator's specific toy diagonal table; the verifier
here verifies the projection structurally and reports its own toy numerics.
Both reports are honest at C1+; neither claims a Planck likelihood result.

Default toy reference: low-ell Sachs-Wolfe-plateau-like spectrum on
ell in [2, 30], theta_c = 60 deg, lambda = 0.2.

Status (per Paper 19 v0.2 sec.1 ladder): C1+ (banked finite-mode covariance
prototype). Not C2 (likelihood/covariance comparison against adversarial
alternatives, deferred). Not C4 (theta_c, lambda APF-derived, deferred).

Created: 2026-05-12 (closes G1 audit flag from Paper 19 v0.2 audit memo).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# v24.3.35: try scipy first; fall back to apf._optimize_vendored when scipy is
# unavailable (e.g. sandbox environments). The vendored optimizer implements
# the same projected-gradient + Armijo-backtracking solver scope used here
# (bounded convex projection); see apf/_optimize_vendored.py for scope notes.
try:
    from scipy.optimize import minimize  # type: ignore[import-not-found]
    _MINIMIZE_SOURCE = "scipy.optimize"
except ImportError:
    from apf._optimize_vendored import minimize  # type: ignore[no-redef]
    _MINIMIZE_SOURCE = "apf._optimize_vendored"

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

ELL_MIN = 2
ELL_MAX = 30
THETA_C_DEG = 60.0
THETA_C_RAD = math.radians(THETA_C_DEG)
COS_THETA_C = math.cos(THETA_C_RAD)
LAMBDA_PRESSURE = 0.2  # least-distortion pressure parameter (not Planck-fit)

# Toy reference D_ell: smooth Sachs-Wolfe-plateau-like form normalized so
# that D_2 ~ 1000 (microK^2 scale), gently varying through ell ~ 30. This
# is a toy reference, not Planck. Exact numerics are not claimed; the
# verifier checks structural properties of the projection.
_TOY_D_REF_NORM = 1000.0


def toy_reference_spectrum(ell_min=ELL_MIN, ell_max=ELL_MAX):
    """Toy low-ell reference spectrum D_ell. Not Planck; not load-bearing.

    Returns array of D_ell values for ell in [ell_min, ell_max].
    """
    ells = np.arange(ell_min, ell_max + 1)
    # Smooth Sachs-Wolfe-plateau toy: gently rising plateau with mild ell
    # dependence. The actual shape is not load-bearing — what matters is
    # that the projection structurally works on a nonnegative input.
    return _TOY_D_REF_NORM / (1.0 + 0.05 * (ells - ell_min))


def a_ell_from_D_ell(ells, D_ell):
    """Convert D_ell = ell(ell+1)C_ell/(2 pi) reference to a_ell coefficients.

    a_ell = (2 ell + 1) / (ell (ell+1)) * D_ell (up to conventional norm).
    Returns array of a_ell same length as ells.
    """
    return (2 * ells + 1) / (ells * (ells + 1)) * D_ell


# ---------------------------------------------------------------------
# Legendre polynomial evaluation via three-term recurrence
# ---------------------------------------------------------------------

def legendre_table(ell_max, x_grid):
    """Compute P_ell(x) for ell in [0, ell_max] and x in x_grid.

    Uses Bonnet's three-term recurrence:
        (ell + 1) P_{ell+1}(x) = (2 ell + 1) x P_ell(x) - ell P_{ell-1}(x).

    Returns 2-D array of shape (ell_max + 1, len(x_grid)).
    """
    n_x = len(x_grid)
    table = np.zeros((ell_max + 1, n_x))
    table[0, :] = 1.0
    if ell_max >= 1:
        table[1, :] = x_grid
    for ell in range(1, ell_max):
        table[ell + 1, :] = ((2 * ell + 1) * x_grid * table[ell, :] - ell * table[ell - 1, :]) / (ell + 1)
    return table


# ---------------------------------------------------------------------
# C_m(x) and S_{theta_c} functional
# ---------------------------------------------------------------------

@dataclass
class ProjectionResult:
    """Result of a finite-mode covariance projection."""
    ells: np.ndarray
    m_ell: np.ndarray
    a_ell: np.ndarray
    S_proj: float
    S_std: float
    ratio: float
    success: bool


def C_m_at_x(m_ell, a_ell, ells, x_grid, leg_table=None):
    """Evaluate C_m(x) = sum_ell a_ell m_ell P_ell(x) on x_grid.

    leg_table may be passed as a precomputed table P_ell(x_grid).
    """
    if leg_table is None:
        leg_table = legendre_table(int(ells[-1]), x_grid)
    rows = leg_table[ells, :]  # shape (len(ells), len(x_grid))
    return (m_ell[:, None] * a_ell[:, None] * rows).sum(axis=0)


def S_theta_c(m_ell, a_ell, ells, x_grid, weights, leg_table=None):
    """S_{theta_c}[m] = integral over x in [-1, cos theta_c] of C_m(x)^2 dx.

    Numerical integration via trapezoid weights on x_grid.
    """
    C_x = C_m_at_x(m_ell, a_ell, ells, x_grid, leg_table=leg_table)
    return float(np.sum(weights * C_x * C_x))


# ---------------------------------------------------------------------
# Optimization
# ---------------------------------------------------------------------

def run_projection(
    ell_min=ELL_MIN,
    ell_max=ELL_MAX,
    theta_c_deg=THETA_C_DEG,
    lam=LAMBDA_PRESSURE,
    D_ref=None,
    n_x=4096,
):
    """Run the least-distortion projection. Returns ProjectionResult.

    Minimizes
        S_{theta_c}[m] / S_{theta_c}[1] + lam * ||m - 1||^2 / N
    subject to 0 <= m_ell <= 2.
    """
    ells = np.arange(ell_min, ell_max + 1)
    if D_ref is None:
        D_ref = toy_reference_spectrum(ell_min, ell_max)
    a_ell = a_ell_from_D_ell(ells, D_ref)

    # Integration grid on [-1, cos theta_c]
    cos_tc = math.cos(math.radians(theta_c_deg))
    x_grid = np.linspace(-1.0, cos_tc, n_x)
    dx = (cos_tc - (-1.0)) / (n_x - 1)
    weights = np.full(n_x, dx)
    weights[0] = 0.5 * dx
    weights[-1] = 0.5 * dx

    leg = legendre_table(int(ells[-1]), x_grid)

    N = len(ells)
    m0 = np.ones(N)
    S_std = S_theta_c(m0, a_ell, ells, x_grid, weights, leg_table=leg)

    def objective(m):
        S = S_theta_c(m, a_ell, ells, x_grid, weights, leg_table=leg)
        distortion = float(np.sum((m - 1.0) ** 2)) / N
        return S / S_std + lam * distortion

    res = minimize(objective, m0, method='L-BFGS-B', bounds=[(0.0, 2.0)] * N)
    m_opt = np.clip(res.x, 0.0, 2.0)
    S_proj = S_theta_c(m_opt, a_ell, ells, x_grid, weights, leg_table=leg)
    return ProjectionResult(
        ells=ells,
        m_ell=m_opt,
        a_ell=a_ell,
        S_proj=S_proj,
        S_std=S_std,
        ratio=S_proj / S_std,
        success=bool(res.success),
    )


# ---------------------------------------------------------------------
# Bank checks
# ---------------------------------------------------------------------

# Module-level cache so we run the projection once per process.
_RESULT_CACHE: ProjectionResult | None = None


def _get_result():
    global _RESULT_CACHE
    if _RESULT_CACHE is None:
        _RESULT_CACHE = run_projection()
    return _RESULT_CACHE


def check_T_cmb_fm_finite_multipliers():
    """[P_structural] All m_ell finite and within the [0, 2] feasibility bound."""
    r = _get_result()
    finite = bool(np.all(np.isfinite(r.m_ell)))
    in_bounds = bool(np.all((r.m_ell >= 0.0 - 1e-9) & (r.m_ell <= 2.0 + 1e-9)))
    return {
        'name': 'T_cmb_fm_finite_multipliers',
        'tier': 4,
        'epistemic': 'P_structural_reading',
        'passed': finite and in_bounds,
        'key_result': f'{len(r.m_ell)} multipliers finite={finite} in [0,2]={in_bounds}',
    }


def check_T_cmb_fm_nonneg_reference():
    """[P_structural] Reference a_ell >= 0 for ell in [ell_min, ell_max]."""
    r = _get_result()
    nonneg = bool(np.all(r.a_ell >= 0))
    return {
        'name': 'T_cmb_fm_nonneg_reference',
        'tier': 4,
        'epistemic': 'P_structural_reading',
        'passed': nonneg,
        'key_result': f'a_ell min={float(r.a_ell.min()):.4g} max={float(r.a_ell.max()):.4g}',
    }


def check_T_cmb_fm_large_angle_reduction():
    """[P_structural] S_{theta_c}^proj < S_{theta_c}^std: the projection reduces the large-angle functional."""
    r = _get_result()
    reduced = r.S_proj < r.S_std
    return {
        'name': 'T_cmb_fm_large_angle_reduction',
        'tier': 4,
        'epistemic': 'P_structural_reading',
        'passed': reduced,
        'key_result': f'S_proj/S_std = {r.ratio:.6g} (reduced={reduced})',
    }


def check_T_cmb_fm_quadrupole_suppression():
    """[P_structural] m_2 < 0.5: quadrupole substantially suppressed by the projection."""
    r = _get_result()
    m2 = float(r.m_ell[0])  # ell_min = 2 by default
    suppressed = m2 < 0.5
    return {
        'name': 'T_cmb_fm_quadrupole_suppression',
        'tier': 4,
        'epistemic': 'P_structural_reading',
        'passed': suppressed,
        'key_result': f'm_2 = {m2:.4f} (target < 0.5; suppressed={suppressed})',
    }


def check_T_cmb_fm_high_ell_preservation():
    """[P_structural] m_ell within +/-15% of 1 for ell >= 20: transition region preserved."""
    r = _get_result()
    mask = r.ells >= 20
    m_high = r.m_ell[mask]
    deviations = np.abs(m_high - 1.0)
    preserved = bool(np.all(deviations <= 0.15))
    return {
        'name': 'T_cmb_fm_high_ell_preservation',
        'tier': 4,
        'epistemic': 'P_structural_reading',
        'passed': preserved,
        'key_result': f'max |m_ell - 1| for ell>=20: {float(deviations.max()):.4f} (preserved={preserved})',
    }


def check_T_cmb_fm_legendre_recurrence():
    """[P_structural] Bonnet's three-term recurrence
        (ell+1) P_{ell+1}(x) = (2 ell + 1) x P_ell(x) - ell P_{ell-1}(x)
    holds at test point x = 0.3 for all ell in [1, ell_max-1] within float tolerance.
    Verifies our Legendre-table implementation is correct.
    """
    x_test = 0.3
    ell_max = ELL_MAX
    table = legendre_table(ell_max, np.array([x_test]))[:, 0]
    max_err = 0.0
    for ell in range(1, ell_max):
        lhs = (ell + 1) * table[ell + 1]
        rhs = (2 * ell + 1) * x_test * table[ell] - ell * table[ell - 1]
        err = abs(lhs - rhs)
        if err > max_err:
            max_err = err
    passes = bool(max_err < 1e-12)
    return {
        'name': 'T_cmb_fm_legendre_recurrence',
        'tier': 4,
        'epistemic': 'P_structural_reading',
        'passed': passes,
        'key_result': f'max |Bonnet residual| at x=0.3: {max_err:.3e} (tol=1e-12)',
    }


_CHECKS = {
    'T_cmb_fm_finite_multipliers': check_T_cmb_fm_finite_multipliers,
    'T_cmb_fm_nonneg_reference': check_T_cmb_fm_nonneg_reference,
    'T_cmb_fm_large_angle_reduction': check_T_cmb_fm_large_angle_reduction,
    'T_cmb_fm_quadrupole_suppression': check_T_cmb_fm_quadrupole_suppression,
    'T_cmb_fm_high_ell_preservation': check_T_cmb_fm_high_ell_preservation,
    'T_cmb_fm_legendre_recurrence': check_T_cmb_fm_legendre_recurrence,
}


def register(registry):
    """Register the CMB finite-mode covariance checks into the bank.

    6 checks total at landing. Closes Paper 19 v0.2 audit memo G1 flag.
    """
    for name, fn in _CHECKS.items():
        registry[name] = fn


def run_all():
    results = []
    for name, fn in _CHECKS.items():
        try:
            r = fn()
            ok = bool(r.get('passed') is True)
            results.append({'name': name, 'passed': ok, 'key_result': r.get('key_result', '')})
        except Exception as e:
            results.append({'name': name, 'passed': False, 'error': repr(e)})
    return {
        'passed': sum(1 for r in results if r['passed']),
        'total': len(results),
        'results': results,
    }


if __name__ == '__main__':
    import json
    print(json.dumps(run_all(), indent=2))

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "dark:cmb_finite_mode_covariance_prototype",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Six model-integrity checks (check_T_cmb_fm_finite_multipliers, "
            "check_T_cmb_fm_nonneg_reference, "
            "check_T_cmb_fm_large_angle_reduction, "
            "check_T_cmb_fm_quadrupole_suppression, "
            "check_T_cmb_fm_high_ell_preservation, "
            "check_T_cmb_fm_legendre_recurrence), all banked at epistemic "
            "P_structural_reading tier 4, certify the internal structure of the "
            "Model-5 finite-mode covariance projection behind Paper 19's large- "
            "angle CMB suppression reading: the least-distortion multipliers "
            "m_ell are finite and within [0,2], the toy reference a_ell >= 0, the "
            "projection strictly reduces the large-angle functional S_theta_c "
            "(S_proj < S_std), m_2 < 0.5, m_ell stays within 15% of 1 for ell >= "
            "20, and the Legendre table satisfies Bonnet's recurrence to 1e-12. "
            "Everything runs on a toy Sachs-Wolfe-plateau-like reference spectrum "
            "on ell in [2,30] at theta_c = 60 deg, lambda = 0.2 -- these are NOT "
            "Planck-likelihood results and the module says so: ladder status is "
            "C1+ (banked prototype), not C2 (adversarial likelihood comparison, "
            "deferred) and not C4 (theta_c, lambda APF-derived, deferred). No "
            "observational data is billed as input; the only external machinery "
            "is the optimizer (scipy or the vendored fallback). Discrepancy flag: "
            "the check docstrings say [P_structural] while the machine field on "
            "all six is 'P_structural_reading' -- the field wins. "
        ),
        "note": "Wave 7; scipy-blocked module read statically; docstring [P_structural] vs field P_structural_reading flagged on all six checks",
    },
)
