"""APF perturbative refinability defect utilities.

This module implements the structural theorem:

    Delta_P = max(0, required_load * (1 + lambda_gamma) / n_gamma - 1)

with

    required_load = r_k + intensity

and the continuum corollary:

    n_gamma = q ** (-d_gamma)
    lambda_gamma = q ** 2
    Delta_P = max(0, (r_k + intensity) * (1 + q**2) * q**d_gamma - 1)

No external cosmology data is used here.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


@dataclass(frozen=True)
class RefinabilityState:
    """Container for a single mode-refinability evaluation."""

    required_load: float
    lambda_gamma: float
    n_gamma: float

    def burden_ratio(self) -> float:
        return burden_ratio(self.required_load, self.lambda_gamma, self.n_gamma)

    def defect(self) -> float:
        return defect_from_counts(self.required_load, self.lambda_gamma, self.n_gamma)

    def preserved_fraction(self) -> float:
        return preserved_fraction_from_defect(self.defect())

    def refinable(self, *, atol: float = 1e-12) -> bool:
        return refinability_holds(self.required_load, self.lambda_gamma, self.n_gamma, atol=atol)


def _require_finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return value


def _require_nonnegative(name: str, value: float) -> float:
    value = _require_finite(name, value)
    if value < 0:
        raise ValueError(f"{name} must be nonnegative, got {value!r}")
    return value


def _require_positive(name: str, value: float) -> float:
    value = _require_finite(name, value)
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value!r}")
    return value


def positive_part(x: float) -> float:
    """Return [x]_+ = max(0, x)."""
    x = _require_finite("x", x)
    return x if x > 0.0 else 0.0


def required_load(intensity: float, r_k: float = 1.0) -> float:
    """Return R_k = r_k + I_k.

    ``intensity`` is the dimensionless mode intensity I_k. ``r_k`` is the
    baseline component count. For scalar density modes, r_k = 1.
    """
    intensity = _require_nonnegative("intensity", intensity)
    r_k = _require_positive("r_k", r_k)
    return r_k + intensity


def burden(required_load_value: float, lambda_gamma: float) -> float:
    """Return R_k * (1 + lambda_Gamma)."""
    required_load_value = _require_positive("required_load", required_load_value)
    lambda_gamma = _require_nonnegative("lambda_gamma", lambda_gamma)
    return required_load_value * (1.0 + lambda_gamma)


def burden_ratio(required_load_value: float, lambda_gamma: float, n_gamma: float) -> float:
    """Return burden divided by available cell count."""
    n_gamma = _require_positive("n_gamma", n_gamma)
    return burden(required_load_value, lambda_gamma) / n_gamma


def defect_from_counts(required_load_value: float, lambda_gamma: float, n_gamma: float) -> float:
    """Return Delta_P from the graph-native objects."""
    return positive_part(burden_ratio(required_load_value, lambda_gamma, n_gamma) - 1.0)


def refinability_holds(
    required_load_value: float,
    lambda_gamma: float,
    n_gamma: float,
    *,
    atol: float = 1e-12,
) -> bool:
    """Return True iff R_k(1 + lambda_Gamma) <= N_Gamma."""
    atol = _require_nonnegative("atol", atol)
    return burden(required_load_value, lambda_gamma) <= _require_positive("n_gamma", n_gamma) + atol


def preserved_fraction_from_defect(delta_p: float) -> float:
    """Return zeta_P = 1/(1 + Delta_P)."""
    delta_p = _require_nonnegative("delta_p", delta_p)
    return 1.0 / (1.0 + delta_p)


def preserved_fraction(required_load_value: float, lambda_gamma: float, n_gamma: float) -> float:
    """Return the source-side preservation factor zeta_P."""
    return preserved_fraction_from_defect(
        defect_from_counts(required_load_value, lambda_gamma, n_gamma)
    )


def effective_source(raw_source_amplitude: float, delta_p: float) -> float:
    """Return the preserved source amplitude zeta_P * raw_source_amplitude."""
    raw_source_amplitude = _require_finite("raw_source_amplitude", raw_source_amplitude)
    return preserved_fraction_from_defect(delta_p) * raw_source_amplitude


def continuum_available_count(q: float, d_gamma: float = 3.0) -> float:
    """Return N_Gamma = q^(-d_Gamma) for homogeneous continuum routing."""
    q = _require_positive("q", q)
    d_gamma = _require_positive("d_gamma", d_gamma)
    return q ** (-d_gamma)


def continuum_lambda(q: float) -> float:
    """Return lambda_Gamma = q^2 for the lowest local-gradient burden."""
    q = _require_positive("q", q)
    return q * q


def continuum_defect(
    q: float,
    intensity: float = 0.0,
    d_gamma: float = 3.0,
    r_k: float = 1.0,
) -> float:
    """Return the homogeneous-continuum perturbative defect."""
    q = _require_positive("q", q)
    d_gamma = _require_positive("d_gamma", d_gamma)
    r_load = required_load(intensity, r_k)
    return positive_part(r_load * (1.0 + q * q) * (q ** d_gamma) - 1.0)


def continuum_state(
    q: float,
    intensity: float = 0.0,
    d_gamma: float = 3.0,
    r_k: float = 1.0,
) -> RefinabilityState:
    """Return the graph-native state corresponding to the continuum corollary."""
    return RefinabilityState(
        required_load=required_load(intensity, r_k),
        lambda_gamma=continuum_lambda(q),
        n_gamma=continuum_available_count(q, d_gamma),
    )


def threshold_equation_value(
    q: float,
    intensity: float = 0.0,
    d_gamma: float = 3.0,
    r_k: float = 1.0,
) -> float:
    """Return (r_k + I_k)(1 + q^2)q^d - 1."""
    q = _require_positive("q", q)
    return required_load(intensity, r_k) * (1.0 + q * q) * (q ** _require_positive("d_gamma", d_gamma)) - 1.0


def threshold_q(
    intensity: float = 0.0,
    d_gamma: float = 3.0,
    r_k: float = 1.0,
    *,
    tol: float = 1e-14,
    max_iter: int = 256,
) -> float:
    """Solve (r_k + I_k)(1 + q^2)q^d = 1 for q > 0.

    The left-hand side is monotone increasing for q > 0 when d_gamma > 0,
    so bisection is sufficient and dependency-free.
    """
    _ = required_load(intensity, r_k)
    d_gamma = _require_positive("d_gamma", d_gamma)
    tol = _require_positive("tol", tol)
    if max_iter <= 0:
        raise ValueError("max_iter must be positive")

    lo = 0.0
    hi = 1.0
    while threshold_equation_value(hi, intensity, d_gamma, r_k) < 0.0:
        hi *= 2.0
        if hi > 1e12:
            raise RuntimeError("failed to bracket positive threshold")

    for _i in range(max_iter):
        mid = 0.5 * (lo + hi)
        if mid == 0.0:
            lo = mid
            continue
        value = threshold_equation_value(mid, intensity, d_gamma, r_k)
        if abs(value) <= tol:
            return mid
        if value < 0.0:
            lo = mid
        else:
            hi = mid

    return 0.5 * (lo + hi)


def high_q_asymptotic_power(d_gamma: float = 3.0) -> float:
    """Return the high-q power d_Gamma + 2."""
    return _require_positive("d_gamma", d_gamma) + 2.0


def monotone_thresholds_for_intensities(
    intensities: Iterable[float],
    d_gamma: float = 3.0,
    r_k: float = 1.0,
) -> list[float]:
    """Return threshold q-values for a sequence of intensities."""
    return [threshold_q(i, d_gamma=d_gamma, r_k=r_k) for i in intensities]
