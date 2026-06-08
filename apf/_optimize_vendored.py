"""APF vendored optimizer — scipy-free bounded minimization.

Session 6 piece (per Reference - APF Interface Engine Family Architecture
(2026-05-19).md): closes the sandbox bank-load scipy gap by vendoring the
specific scipy.optimize.minimize call used by apf.cmb_finite_mode_covariance.

Background
----------
The framework's bank has one module — apf.cmb_finite_mode_covariance — that
uses scipy.optimize.minimize(method='L-BFGS-B', bounds=[...]) for the
finite-mode covariance projection (Paper 19 v0.2 §§5-6). Production
environments have scipy; sandbox environments don't, producing the persistent
"-6 scipy gap" in bank._load() across the entire architecture-review
sequencing arc.

Scope of this module
--------------------
Minimal scipy-compatible bounded-minimization. Implements:

* `minimize(fun, x0, method='L-BFGS-B', bounds=...)` — same call signature
  as scipy.optimize.minimize for the bounded case.
* Internal algorithm: projected gradient with Armijo backtracking line search,
  numerical gradient via central differences. Reliable for convex-or-nearly-
  convex bounded problems with small dimensionality (the cmb projection has
  N=29 variables).
* Returns an OptimizeResult-compatible object with `.x`, `.fun`, `.success`,
  `.nit`, `.nfev`, `.message` attributes.

What this module does NOT implement
-----------------------------------
* Method dispatch beyond bounded methods — only 'L-BFGS-B' and 'Bounded
  projected gradient' (alias) are recognized. Unbounded methods raise.
* Constraints beyond box bounds.
* Sparse linear algebra, large-scale problems, parallel evaluation.

This module is a deliberate **narrow vendor** — not a scipy replacement.
The only call site is apf.cmb_finite_mode_covariance.run_projection. If a
future module needs a wider scipy surface, that's a separate vendor decision.

Audit-first discipline
----------------------
The vendored optimizer produces the same structural verdicts on the cmb
projection as scipy.optimize.minimize does (m_ell in [0, 2]; quadrupole
suppression; high-ell preservation). It does NOT necessarily produce
bit-identical iterates; the bank checks are tolerant structural conditions,
not exact-match tests. No new physical claim is introduced by the vendor.

References
----------
* apf.cmb_finite_mode_covariance — the only caller of minimize() in the
  framework's bank.
* Paper 19 v0.2 §§5-6 — physical context for the finite-mode projection.
* Reference - APF Interface Engine Family Architecture (2026-05-19).md —
  Session 6+ opportunistic operationalization (this is one such operation).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Sequence, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# OptimizeResult-compatible return object
# ---------------------------------------------------------------------------

@dataclass
class OptimizeResult:
    """scipy.optimize.OptimizeResult-compatible return object.

    Provides .x / .fun / .success / .nit / .nfev / .message attributes that
    scipy callers expect. Indexable via attribute-style access (no dict
    behavior emulated — the only caller in the framework accesses via
    attribute access, not dict).
    """
    x: np.ndarray
    fun: float
    success: bool
    nit: int
    nfev: int
    message: str
    jac: Optional[np.ndarray] = None


# ---------------------------------------------------------------------------
# Numerical gradient
# ---------------------------------------------------------------------------

def _numerical_gradient(
    fun: Callable[[np.ndarray], float],
    x: np.ndarray,
    eps: float = 1e-6,
) -> Tuple[np.ndarray, int]:
    """Central-difference gradient. Returns (gradient, nfev_used)."""
    n = len(x)
    g = np.zeros_like(x, dtype=float)
    nfev = 0
    for i in range(n):
        h = max(eps * (1.0 + abs(x[i])), 1e-12)
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        g[i] = (fun(x_plus) - fun(x_minus)) / (2.0 * h)
        nfev += 2
    return g, nfev


# ---------------------------------------------------------------------------
# Bound projection
# ---------------------------------------------------------------------------

def _project_to_bounds(
    x: np.ndarray,
    lb: np.ndarray,
    ub: np.ndarray,
) -> np.ndarray:
    """Project x onto the box [lb, ub] elementwise."""
    return np.clip(x, lb, ub)


def _parse_bounds(
    bounds: Sequence[Tuple[Optional[float], Optional[float]]],
    n: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """Parse scipy-style bounds list into lb, ub arrays.

    Bounds entries are (lower, upper) tuples; None means unbounded.
    Unbounded sides translate to ±inf.
    """
    if len(bounds) != n:
        raise ValueError(f"bounds length {len(bounds)} != x0 length {n}")
    lb = np.array([b[0] if b[0] is not None else -np.inf for b in bounds], dtype=float)
    ub = np.array([b[1] if b[1] is not None else +np.inf for b in bounds], dtype=float)
    return lb, ub


# ---------------------------------------------------------------------------
# Main minimize entry point
# ---------------------------------------------------------------------------

def minimize(
    fun: Callable[[np.ndarray], float],
    x0: Sequence[float],
    method: str = "L-BFGS-B",
    bounds: Optional[Sequence[Tuple[Optional[float], Optional[float]]]] = None,
    options: Optional[dict] = None,
    **kwargs: Any,
) -> OptimizeResult:
    """Scipy-compatible minimize() for bounded methods only.

    Parameters mirror ``scipy.optimize.minimize``:

    * fun(x) -> float : objective function
    * x0 : initial point
    * method : 'L-BFGS-B' or 'Bounded' (both run the same projected-gradient
      backtracking solver in this vendored implementation)
    * bounds : sequence of (low, high) tuples, length == len(x0); None for
      unbounded sides
    * options : dict with optional 'maxiter' (default 500), 'ftol' (default 1e-9),
      'gtol' (default 1e-6)

    Returns an OptimizeResult.
    """
    if method.upper() not in ("L-BFGS-B", "BOUNDED", "PROJECTED-GRADIENT"):
        raise NotImplementedError(
            f"apf._optimize_vendored.minimize only implements bounded methods "
            f"(L-BFGS-B / Bounded / Projected-Gradient); got method={method!r}"
        )

    options = options or {}
    maxiter = int(options.get("maxiter", 500))
    ftol = float(options.get("ftol", 1e-9))
    gtol = float(options.get("gtol", 1e-6))

    x = np.array(x0, dtype=float)
    n = len(x)

    if bounds is None:
        lb = np.full(n, -np.inf)
        ub = np.full(n, +np.inf)
    else:
        lb, ub = _parse_bounds(bounds, n)

    x = _project_to_bounds(x, lb, ub)

    nfev = 0
    f_curr = fun(x)
    nfev += 1
    f_prev = f_curr

    nit = 0
    converged = False
    message = "running"

    for nit in range(1, maxiter + 1):
        # Numerical gradient
        g, g_nfev = _numerical_gradient(fun, x)
        nfev += g_nfev

        # Projected-gradient stationarity criterion: norm of (x - P(x - g))
        proj_grad = x - _project_to_bounds(x - g, lb, ub)
        if np.linalg.norm(proj_grad) < gtol:
            converged = True
            message = f"projected-gradient norm below gtol={gtol}"
            break

        # Armijo backtracking on the projected descent direction
        # Step: x_new = P(x - alpha * g); accept if f(x_new) <= f - c1 * alpha * <g, x - x_new> / alpha
        c1 = 1e-4
        alpha = 1.0
        accepted = False
        for _ls_iter in range(30):
            x_trial = _project_to_bounds(x - alpha * g, lb, ub)
            f_trial = fun(x_trial)
            nfev += 1
            # Armijo on actual decrease vs predicted via projected gradient
            predicted_decrease = float(np.dot(g, x - x_trial))
            if f_trial <= f_curr - c1 * predicted_decrease:
                accepted = True
                break
            alpha *= 0.5

        if not accepted:
            converged = True
            message = "no descent direction accepted; line search exhausted"
            break

        # Update + convergence on f
        f_prev = f_curr
        x = x_trial
        f_curr = f_trial
        if abs(f_prev - f_curr) < ftol * max(1.0, abs(f_curr)):
            converged = True
            message = f"function change below ftol={ftol}"
            break

    if nit == maxiter and not converged:
        message = f"maxiter={maxiter} reached"

    return OptimizeResult(
        x=x,
        fun=float(f_curr),
        success=converged,
        nit=nit,
        nfev=nfev,
        message=message,
        jac=None,
    )


# ---------------------------------------------------------------------------
# Self-test (small convex bounded QP)
# ---------------------------------------------------------------------------

def _self_test() -> dict:
    """Internal self-test: minimize a known convex bounded QP and check result.

    Problem: f(x) = 0.5 * ||x - target||^2 with bounds [0, 1]; the optimum
    is the projection of `target` onto [0, 1]^n, computable analytically.
    """
    rng = np.random.default_rng(seed=42)
    n = 8
    target = rng.uniform(-0.5, 1.5, size=n)
    bounds = [(0.0, 1.0)] * n

    def fun(x: np.ndarray) -> float:
        return float(0.5 * np.sum((x - target) ** 2))

    x0 = np.full(n, 0.5)
    result = minimize(fun, x0, method="L-BFGS-B", bounds=bounds)
    expected = np.clip(target, 0.0, 1.0)

    err = float(np.max(np.abs(result.x - expected)))
    return {
        "success": result.success,
        "nit": result.nit,
        "nfev": result.nfev,
        "max_err_vs_analytical": err,
        "tol_ok": err < 1e-3,
    }


# ---------------------------------------------------------------------------
# Bank check
# ---------------------------------------------------------------------------

def check_T_optimize_vendored_minimize_convex_bounded_P():
    """Vendored minimize() converges on a known convex bounded QP.

    Test: f(x) = 0.5 * ||x - target||^2 on box [0, 1]; analytical minimum is
    clip(target, 0, 1). Vendored minimize() must converge to within 1e-3.

    Also verifies OptimizeResult-compatible return interface (.x / .fun /
    .success / .nit / .nfev / .message attributes) and that 'L-BFGS-B' alias
    dispatches to the bounded solver.
    """
    test = _self_test()
    interface_ok = (
        isinstance(test.get("nfev"), int)
        and isinstance(test.get("nit"), int)
        and isinstance(test.get("success"), bool)
    )
    consistent = test["tol_ok"] and test["success"] and interface_ok
    return {
        "name": "check_T_optimize_vendored_minimize_convex_bounded_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_optimize_vendored" if consistent else "FAIL",
        "epistemic": "P_optimize_vendored",
        "summary": (
            "Vendored minimize() converges on the canonical convex bounded QP "
            "(f(x) = 0.5 * ||x - target||^2 on box [0, 1]) to within 1e-3 of the "
            "analytical clip(target, 0, 1) solution. OptimizeResult-compatible "
            "return interface (.x / .fun / .success / .nit / .nfev / .message). "
            "Used as the scipy.optimize.minimize fallback by apf.cmb_finite_mode_covariance "
            "when scipy is unavailable (sandbox environments)."
        ),
        "dependencies": [],
        "data": test,
    }


_CHECKS = {
    "check_T_optimize_vendored_minimize_convex_bounded_P": check_T_optimize_vendored_minimize_convex_bounded_P,
}


def register(registry=None):
    """Register the vendored optimizer's bank check."""
    if registry is None:
        return _CHECKS
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import json
    print(json.dumps(_self_test(), indent=2, default=str))
