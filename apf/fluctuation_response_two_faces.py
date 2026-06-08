"""apf/fluctuation_response_two_faces.py -- the equilibrium fluctuation-response identity.

Temperature in the framework is an exchange rate between two currencies the ledger keeps for
every distinction: what it COSTS to hold (the energy face, eps) and what it COUNTS (the entropy
face, sigma = ln d_eff). beta = sigma/eps is the rate (L_beta_temp [P]). This module proves the
equilibrium half of the fluctuation-dissipation relation -- Einstein's static fluctuation theory
-- on the bounded distinction ledger:

        <Delta E^2> = - d<E>/d beta.

The variance of the energy face (the FLUCTUATION) equals the response of the mean energy face to
inverse temperature (the DISSIPATION side), both read off the one canonical distribution that
max-entropy assigns. In the framework's language: fluctuation is the entropy face and dissipation
the energy face of the same resolved distinction, locked by beta. This is the rigorous core of
the Brownian intuition -- the seam you can watch under a microscope -- with the dynamics removed.

CONSTRUCTION (same microstate counting as the banked thm:secondlaw / L_singularity spine):
  * a count n of resolved distinctions, n in {0, ..., C_total}  (FD4 ceiling, L_self_exclusion).
  * multiplicity g(n) = d_eff^n  (entropy face; S(n) = n*sigma = ln g, T_entropy + L_sigma_intensive).
  * energy face E(n) = n*eps  (first law, T_realignment_cost_is_transition_energy).
  * canonical weight P(n) ∝ g(n) e^{-beta E(n)} = e^{n(sigma - beta*eps)}  (max-entropy with an
    energy constraint, beta the Lagrange multiplier -- L_equip + L_beta_temp).

The identity <Delta E^2> = -d<E>/d beta is then the elementary cumulant property of the partition
function Z(beta) = sum_n e^{-beta E(n)} (mean = -d ln Z/d beta, variance = d^2 ln Z/d beta^2), so it
holds exactly for ANY canonical distribution. What the FRAMEWORK supplies is that the distribution
is the canonical one its max-entropy gives, that the two sides ARE the entropy and energy faces,
and -- the load-bearing structural point -- that the bound C_total (FD4) is what keeps the
fluctuation FINITE. At the framework temperature beta = sigma/eps the tilt sigma - beta*eps
vanishes, the distribution is UNIFORM on {0, ..., C_total}, and the variance is the closed form
N(N+2)/12 with N = C_total. Without the ceiling that variance diverges (~N^2/12); the same
boundedness that makes the de Sitter horizon entropy finite makes the equilibrium fluctuation
finite. Maximal fluctuation sits exactly at the framework temperature, where the two faces balance.

GRADE [P]: the identity is exact and composes banked [P] lemmas with the elementary cumulant
property; the finiteness is FD4. No fitted quantity.

SCOPE / non-claims (the loose end, named not crossed):
  * This is the EQUILIBRIUM (static) fluctuation-response relation. It does NOT prove the
    DYNAMICAL Einstein-Brownian relation D = mu * k_B T (diffusion = mobility * temperature),
    which needs a physical time-flow -- a relaxation rate, time-correlation functions. The
    framework parks exactly that under `T_no_physical_time_flow_overclaim`; getting from this
    identity to the full Brownian motion adds that one external dynamical input.
  * Reading -d<E>/d beta as a measured dissipative response / heat capacity is the standard
    equilibrium-thermodynamics dictionary; the check certifies the identity and the
    faces-and-boundedness structure, not a laboratory transport measurement.
"""
from __future__ import annotations
import math
from apf.apf_utils import check as _check, _result as _full_result


def _moments(beta, sigma, eps, N):
    """Bounded canonical ensemble P(n) ∝ e^{n(sigma - beta*eps)}, n in {0..N}. Returns (E, varE)."""
    x = sigma - beta * eps
    # stable: factor e^{x*n}; N small (<= a few thousand) so direct sum is fine
    ws = [math.exp(x * n) for n in range(N + 1)]
    Z = sum(ws)
    p = [w / Z for w in ws]
    n1 = sum(n * p[n] for n in range(N + 1))
    n2 = sum(n * n * p[n] for n in range(N + 1))
    var_n = n2 - n1 * n1
    return eps * n1, eps * eps * var_n, n1, var_n


def check_T_fluctuation_response_is_two_faces():
    """T_fluctuation_response_is_two_faces: <dE^2> = -d<E>/dbeta on the bounded ledger [P].

    THEOREM (equilibrium fluctuation-response). For the bounded distinction ledger at inverse
    temperature beta, with energy face E(n) = n*eps and entropy face S(n) = n*sigma over the
    canonical distribution P(n) ∝ e^{n(sigma - beta*eps)} on n in {0, ..., C_total}, the variance
    of the energy face equals the response of its mean to beta:
            <Delta E^2> = - d<E>/d beta.
    The fluctuation (entropy-face spread) and the dissipation side (energy-face response) are the
    two faces of one resolved distinction, locked by beta = sigma/eps. The bound C_total (FD4)
    keeps the fluctuation finite; at beta = sigma/eps the distribution is uniform on {0..C_total}
    and Var(n) = N(N+2)/12, N = C_total.

    PROOF. Each constituent is banked [P]: the energy face (T_realignment_cost_is_transition_energy),
    the entropy face / multiplicity d_eff^n (T_entropy, L_sigma_intensive, L_self_exclusion), the
    rate beta = sigma/eps (L_beta_temp), the max-entropy canonical reading (L_equip). The identity
    <Delta E^2> = d^2 ln Z/d beta^2 = -d<E>/d beta is the cumulant property of Z(beta), exact for
    any canonical distribution. Finiteness is FD4 (n <= C_total). Verified numerically below across
    beta, plus the uniform-at-beta=sigma/eps closed form and the diverges-without-bound contrast.

    GRADE [P]: exact identity composing [P] lemmas + elementary cumulant property; finiteness FD4.

    SCOPE: the EQUILIBRIUM (static) relation -- the rigorous core of the Brownian/fluctuation-
    dissipation picture with the dynamics removed. It does NOT prove the dynamical Einstein-Brownian
    relation D = mu*k_B T, which needs a physical time-flow the framework parks under
    `T_no_physical_time_flow_overclaim`. Reading -d<E>/dbeta as a measured dissipative response is
    the standard equilibrium dictionary.
    """
    # constituent [P] lemmas
    from apf.core import check_T_entropy
    from apf.gravity import check_L_self_exclusion
    from apf.supplements import check_L_sigma_intensive, check_L_beta_temp
    from apf.cosmology import check_L_equip
    from apf.cost_energy_identity import check_T_realignment_cost_is_transition_energy
    for nm, fn in [
        ("T_entropy", check_T_entropy),
        ("L_self_exclusion", check_L_self_exclusion),
        ("L_sigma_intensive", check_L_sigma_intensive),
        ("L_beta_temp", check_L_beta_temp),
        ("L_equip", check_L_equip),
        ("T_realignment_cost_is_transition_energy", check_T_realignment_cost_is_transition_energy),
    ]:
        r = fn()
        _check(r.get("epistemic") == "P" and r.get("passed"), f"constituent {nm}: banked [P] and passing")

    # ----- the bounded distinction ledger -----
    N = 61                      # C_total (FD4 ceiling)
    d_eff = 102                 # 60 + 42, L_self_exclusion
    sigma = math.log(d_eff)     # L_sigma_intensive
    eps = 1.0                   # natural units
    beta_fw = sigma / eps       # framework temperature, L_beta_temp

    # (1) the identity <Delta E^2> = -d<E>/d beta, across beta
    def dEdbeta(beta, h=1e-6):
        Ep, _, _, _ = _moments(beta + h, sigma, eps, N)
        Em, _, _, _ = _moments(beta - h, sigma, eps, N)
        return (Ep - Em) / (2 * h)
    for frac in (0.5, 0.9, 1.0, 1.1, 2.0, 3.0):
        beta = frac * beta_fw
        _, varE, _, _ = _moments(beta, sigma, eps, N)
        resp = -dEdbeta(beta)
        rel = abs(varE - resp) / max(abs(varE), 1e-30)
        _check(rel < 1e-4, f"fluctuation = response at beta={beta:.4f}: <dE^2>={varE:.5f} vs -d<E>/dbeta={resp:.5f} (rel {rel:.1e})")

    # (2) at beta = sigma/eps the distribution is uniform; Var(n) = N(N+2)/12 (finite by FD4)
    _, _, n1, var_n = _moments(beta_fw, sigma, eps, N)
    _check(abs(n1 - N / 2) < 1e-9, f"framework T: <n> = N/2 = {N/2} (uniform on 0..{N})")
    _check(abs(var_n - N * (N + 2) / 12) < 1e-9, f"framework T: Var(n) = N(N+2)/12 = {N*(N+2)/12} (finite by FD4)")

    # (3) boundedness is load-bearing: without the C_total ceiling the framework-T variance diverges
    vars_by_N = []
    for NN in (61, 200, 1000):
        _, _, _, vn = _moments(beta_fw, sigma, eps, NN)
        vars_by_N.append(vn)
    _check(vars_by_N[1] > 3 * vars_by_N[0] and vars_by_N[2] > 3 * vars_by_N[1],
           "Var(n) grows ~N^2/12 with the ceiling -> diverges unbounded; FD4 makes the fluctuation finite")

    return _full_result(
        name=("T_fluctuation_response_is_two_faces: the equilibrium fluctuation-response identity "
              "<Delta E^2> = -d<E>/d beta on the bounded distinction ledger -- the variance of the "
              "energy face equals the response of its mean to inverse temperature, the two faces of "
              "a resolved distinction locked by beta = sigma/eps. The rigorous (static) core of the "
              "fluctuation-dissipation / Brownian picture; the bound C_total (FD4) keeps the "
              "fluctuation finite (uniform on 0..C_total at beta=sigma/eps, Var=N(N+2)/12). Composes "
              "T_entropy + L_self_exclusion + L_sigma_intensive + L_beta_temp + L_equip + "
              "T_realignment_cost_is_transition_energy [all P] with the cumulant identity [P]"),
        tier=4, epistemic="P",
        summary=(
            "Temperature is the exchange rate between the ledger's two currencies -- the energy a "
            "distinction costs (eps) and the count it carries (sigma=ln d_eff) -- with beta=sigma/eps "
            "the rate. On the canonical distribution P(n) ∝ e^{n(sigma-beta eps)} that max-entropy "
            "(L_equip) assigns over n in {0..C_total} (FD4), the variance of the energy face equals "
            "the response of its mean to beta: <dE^2> = -d<E>/dbeta (exact, the cumulant property of "
            "Z). Fluctuation = entropy face, dissipation side = energy face, locked by beta. The "
            "bound C_total is load-bearing: at beta=sigma/eps the distribution is uniform on "
            "{0..C_total} and Var(n)=N(N+2)/12 -- finite for the same reason the de Sitter horizon "
            "entropy is finite, the count is bounded; unbounded it diverges (~N^2/12). Maximal "
            "fluctuation sits exactly at the framework temperature where the two faces balance. "
            "SCOPE: the EQUILIBRIUM relation -- the static core of fluctuation-dissipation. It does "
            "NOT prove the dynamical Einstein-Brownian D=mu k_B T (diffusion=mobility*temperature); "
            "that adds a physical time-flow the framework parks under T_no_physical_time_flow_overclaim."
        ),
        key_result=("<Delta E^2> = -d<E>/d beta [P] on the bounded ledger -- fluctuation and "
                    "dissipation are the entropy and energy faces locked by beta=sigma/eps; FD4 "
                    "makes the fluctuation finite (Var=N(N+2)/12 at beta=sigma/eps). Equilibrium "
                    "(static) fluctuation-dissipation; the dynamical Brownian relation is parked "
                    "under T_no_physical_time_flow_overclaim."),
        dependencies=["T_entropy", "L_self_exclusion", "L_sigma_intensive", "L_beta_temp",
                      "L_equip", "T_realignment_cost_is_transition_energy"],
        cross_refs=["T_thermodynamics_four_laws_synthesis", "L_singularity_resolution",
                    "T_deSitter_entropy", "T_no_physical_time_flow_overclaim"],
        artifacts={
            "identity": "<Delta E^2> = -d<E>/d beta (cumulant property of Z, exact)",
            "framework_T": "beta=sigma/eps -> uniform on {0..C_total}, Var(n)=N(N+2)/12=320.25 (N=61)",
            "boundedness": "FD4 ceiling C_total keeps the fluctuation finite; unbounded diverges ~N^2/12",
            "two_faces": "fluctuation = entropy face (sigma), dissipation = energy face (eps), locked by beta",
            "parked": "dynamical Einstein-Brownian D=mu k_B T needs physical time-flow (T_no_physical_time_flow_overclaim)",
        },
    )


_CHECKS = {"T_fluctuation_response_is_two_faces": check_T_fluctuation_response_is_two_faces}
def register(registry):
    registry.update(_CHECKS); return registry
def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}
