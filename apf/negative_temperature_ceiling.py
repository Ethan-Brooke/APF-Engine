"""apf/negative_temperature_ceiling.py -- the ceiling creates the negative-temperature branch.

A system admits negative absolute temperature -- population inversion, the laser/spin-system
regime -- if and only if its energy spectrum is bounded ABOVE. The bounded distinction ledger is
exactly such a system: FD4 caps the count at C_total, so the energy face E(n) = n*eps is bounded,
0 <= E <= C_total*eps. The ceiling is what puts the ledger in the bounded-spectrum class, and the
ceiling is what makes the whole thermal range -- including infinite and negative temperature --
exist.

Worked on the same bounded canonical ensemble as fluctuation_response_two_faces.py:
P(n) ∝ e^{n(sigma - beta*eps)} on n in {0, ..., C_total}.

  * Z(beta) is finite for EVERY real beta (a finite sum), so beta = 0 (infinite temperature) and
    beta < 0 (negative temperature) are accessible.
  * REMOVE the ceiling and the unbounded sum sum_{n=0}^inf e^{(sigma-beta eps)n} converges only
    for beta > sigma/eps. Without FD4 the count-balance point, infinite temperature, and the
    entire negative-temperature branch -- population inversion -- do not exist. The ceiling
    CREATES them.
  * <n> rises monotonically from 0 to C_total as beta runs from +inf to -inf
    (d<n>/d beta = -eps*Var(n) < 0). The special points:
      - beta > sigma/eps : ground-dominated (<n> < C_total/2).
      - beta = sigma/eps : the two faces balance (sigma = beta*eps), P(n) UNIFORM, <n> = C_total/2.
                           This is the framework temperature and the onset of inversion.
      - beta = 0         : infinite temperature (microstate-uniform), <n> -> C_total.
      - beta < 0         : negative temperature, fully inverted onto the ceiling.
  * At infinite temperature the log-partition-function is the de Sitter horizon entropy:
    ln Z(beta=0) = ln( sum_n d_eff^n ) = C_total*sigma + O(1/d_eff) = S_dS (T_deSitter_entropy).
    The inversion saturates the ledger at the ceiling, and the ceiling's entropy is S_dS.

GRADE [P]: exact structural facts about the bounded canonical ensemble, composing banked [P]
lemmas (the ceiling C_total via L_count/FD4, the rate beta=sigma/eps via L_beta_temp, the energy
face via T_realignment_cost_is_transition_energy, the entropy face via T_entropy/L_sigma_intensive,
the saturation entropy via T_deSitter_entropy).

SCOPE / non-claims (kept honest -- negative temperature is a place to be careful):
  * This is a CANONICAL / accessibility statement -- about the convergence of Z and the canonical
    distribution at external inverse-temperature beta -- NOT a contested microcanonical-entropy
    claim. The Boltzmann surface entropy of this monotone-multiplicity ledger gives dS/dE = sigma/eps
    > 0 throughout; the negative-temperature branch is the canonical (system + reservoir) regime,
    where the Boltzmann/Gibbs-entropy dispute (Dunkel-Hilbert 2014 vs Frenkel-Warren / Swendsen)
    does not bite because we make no microcanonical negative-temperature claim.
  * We do NOT claim the cosmos or the ledger is IN a negative-temperature state. The result is that
    the ceiling places the ledger in the bounded-spectrum class that ADMITS negative temperature
    (the laser/population-inversion class), and that the framework temperature beta=sigma/eps is
    the inversion onset.
  * The DYNAMICAL question -- how, and how fast, a system reaches an inverted state -- needs a
    physical time-flow the framework parks under `T_no_physical_time_flow_overclaim`.
"""
from __future__ import annotations
import math
from apf.apf_utils import check as _check, _result as _full_result


def _stats(beta, sigma, eps, N):
    x = sigma - beta * eps
    ws = [math.exp(x * n) for n in range(N + 1)]
    Z = sum(ws)
    p = [w / Z for w in ws]
    n1 = sum(n * p[n] for n in range(N + 1))
    n2 = sum(n * n * p[n] for n in range(N + 1))
    return Z, n1, n2 - n1 * n1


def _lnZ(beta, sigma, eps, N):
    """Overflow-safe ln Z = ln sum_{n=0}^N e^{x n}, x = sigma - beta eps."""
    x = sigma - beta * eps
    if x <= 0:
        return math.log(sum(math.exp(x * n) for n in range(N + 1)))
    return x * N + math.log(sum(math.exp(-x * k) for k in range(N + 1)))


def check_T_negative_temperature_needs_the_ceiling():
    """T_negative_temperature_needs_the_ceiling: FD4's ceiling creates the negative-T branch [P].

    THEOREM. The bounded distinction ledger has an energy spectrum bounded above, E = n*eps with
    n <= C_total (FD4). Therefore (i) the canonical Z(beta) is finite for every real beta, so
    infinite temperature (beta=0) and negative temperature (beta<0) are accessible; (ii) without
    the ceiling the unbounded partition sum converges only for beta > sigma/eps, so the count-
    balance point, infinite temperature, and the whole negative-temperature / population-inversion
    branch DO NOT EXIST -- the ceiling creates them; (iii) <n> rises monotonically from 0 to
    C_total as beta runs +inf -> -inf, with the two faces balancing (P uniform, <n>=C_total/2) at
    beta=sigma/eps, infinite T (<n>->C_total) at beta=0, full inversion for beta<0; (iv) at
    infinite temperature ln Z = C_total*sigma + O(1/d_eff) = S_dS, the de Sitter horizon entropy.

    PROOF. The bounded sum is finite for all beta (i). The geometric series sum_0^inf e^{(sigma-
    beta eps)n} converges iff sigma-beta eps < 0 iff beta > sigma/eps (ii). Monotonicity:
    d<n>/d beta = -eps*Var(n) < 0; the balance/infinite-T/inversion points are read off
    P(n) ∝ e^{n(sigma-beta eps)} (iii). ln Z(0) = ln sum d_eff^n = C_total*sigma + ln((1-d_eff^
    -(C_total+1))/(1-d_eff^-1)), the correction O(1/d_eff) (iv). Composes banked [P] lemmas; all
    points verified numerically below.

    GRADE [P]: exact structural facts; no fitted quantity.

    SCOPE: a CANONICAL / accessibility statement (convergence of Z, the canonical distribution at
    external beta), NOT a microcanonical negative-temperature claim -- so the Dunkel-Hilbert /
    Gibbs-vs-Boltzmann-entropy dispute does not bite. We do not claim the ledger IS inverted, only
    that the ceiling places it in the bounded-spectrum class that ADMITS inversion (the laser
    class). The dynamics of reaching an inverted state is parked under
    `T_no_physical_time_flow_overclaim`.
    """
    from apf.core import check_T_entropy
    from apf.gauge import check_L_count
    from apf.supplements import check_L_sigma_intensive, check_L_beta_temp
    from apf.cost_energy_identity import check_T_realignment_cost_is_transition_energy
    from apf.gravity import check_T_deSitter_entropy
    for nm, fn in [
        ("T_entropy", check_T_entropy),
        ("L_count", check_L_count),
        ("L_sigma_intensive", check_L_sigma_intensive),
        ("L_beta_temp", check_L_beta_temp),
        ("T_realignment_cost_is_transition_energy", check_T_realignment_cost_is_transition_energy),
        ("T_deSitter_entropy", check_T_deSitter_entropy),
    ]:
        r = fn()
        _check(r.get("epistemic") == "P" and r.get("passed"), f"constituent {nm}: banked [P] and passing")

    N = 61                      # C_total (FD4 ceiling, L_count)
    d_eff = 102
    sigma = math.log(d_eff)
    eps = 1.0
    beta_fw = sigma / eps

    # (i) Z finite for all real beta -> infinite and negative temperature accessible
    for beta in (beta_fw, 0.0, -1.0, -5.0):
        Z, _, _ = _stats(beta, sigma, eps, N)
        _check(math.isfinite(Z) and Z > 0, f"Z(beta={beta:.3f}) finite -> accessible (incl. beta<=0)")

    # (ii) the ceiling CREATES the branch: unbounded sum diverges for beta <= sigma/eps
    ln_by_N = [_lnZ(0.0, sigma, eps, NN) for NN in (61, 200, 1000)]
    _check(ln_by_N[1] > 2 * ln_by_N[0] and ln_by_N[2] > 4 * ln_by_N[0],
           "unbounded: ln Z(beta=0) grows ~ sigma*N -> diverges; FD4 makes beta<=sigma/eps exist")

    # (iii) <n> monotone 0 -> C_total as beta: +inf -> -inf; the special points
    betas = [10.0, beta_fw, 0.0, -3.0]
    ns = [_stats(b, sigma, eps, N)[1] for b in betas]
    _check(ns[0] < ns[1] < ns[2] <= ns[3] + 1e-9, "<n> rises monotonically as beta decreases")
    _, n_bal, var_bal = _stats(beta_fw, sigma, eps, N)
    _check(abs(n_bal - N / 2) < 1e-9, "beta=sigma/eps: two faces balance, P uniform, <n>=C_total/2 (inversion onset)")
    _, n_inf, _ = _stats(0.0, sigma, eps, N)
    _check(n_inf > 0.99 * N, "beta=0 (infinite T): <n> -> C_total (saturation by microstate counting)")
    _, n_neg, _ = _stats(-3.0, sigma, eps, N)
    _check(n_neg > 0.999 * N, "beta<0 (negative T): fully inverted onto the ceiling")
    # monotonicity sign: d<n>/dbeta = -eps Var(n) < 0
    _check(var_bal > 0, "d<n>/d beta = -eps*Var(n) < 0 (monotone)")

    # (iv) infinite-temperature log-partition-function = de Sitter horizon entropy (to O(1/d_eff))
    lnZ0 = _lnZ(0.0, sigma, eps, N)
    S_dS = N * sigma
    _check(abs(lnZ0 - S_dS) < 3.0 / d_eff, f"ln Z(beta=0) = {lnZ0:.4f} = C_total*sigma = S_dS = {S_dS:.4f} (+O(1/d_eff))")

    return _full_result(
        name=("T_negative_temperature_needs_the_ceiling: the bounded ledger's energy spectrum is "
              "capped by FD4 (E <= C_total*eps), so it is a bounded-spectrum system -- the class "
              "that admits negative absolute temperature / population inversion (lasers, spin "
              "systems). The ceiling CREATES the branch: with it Z(beta) is finite for every real "
              "beta (infinite and negative T accessible); without it the partition sum converges "
              "only for beta>sigma/eps. <n> rises 0->C_total as beta: +inf->-inf, two faces "
              "balancing (P uniform, <n>=C_total/2) at beta=sigma/eps, infinite T at beta=0, full "
              "inversion for beta<0; ln Z(beta=0) = C_total*sigma = S_dS. Composes [P] lemmas [P]"),
        tier=4, epistemic="P",
        summary=(
            "A system admits negative temperature iff its energy spectrum is bounded above; FD4's "
            "ceiling (n <= C_total) makes the distinction ledger one. The ceiling is load-bearing: "
            "the bounded Z(beta) is finite for every real beta, so infinite temperature (beta=0) and "
            "negative temperature (beta<0) exist -- remove the ceiling and the partition sum "
            "converges only for beta>sigma/eps, killing the whole inversion branch. <n> rises "
            "monotonically 0->C_total as beta runs +inf->-inf: ground-dominated above sigma/eps, the "
            "two faces balancing (P uniform, <n>=C_total/2) AT beta=sigma/eps (the framework "
            "temperature, the inversion onset), infinite temperature at beta=0 (<n>->C_total), full "
            "inversion onto the ceiling for beta<0. At infinite temperature ln Z = C_total*sigma = "
            "S_dS, so the inverted, saturated ledger carries exactly the de Sitter horizon entropy. "
            "SCOPE: a canonical/accessibility statement, NOT a microcanonical negative-T claim (the "
            "Dunkel-Hilbert dispute does not bite); we claim the ledger is in the bounded-spectrum "
            "CLASS that admits inversion, not that the cosmos is inverted; the dynamics of reaching "
            "inversion is parked under T_no_physical_time_flow_overclaim."
        ),
        key_result=("Negative temperature / population inversion exists for the ledger BECAUSE FD4 "
                    "bounds the spectrum above; beta=sigma/eps is the inversion onset (P uniform, "
                    "<n>=C_total/2), beta=0 infinite T, beta<0 inverted; ln Z(beta=0)=C_total*sigma="
                    "S_dS. Canonical/accessibility [P]; not a microcanonical or cosmic-state claim."),
        dependencies=["L_count", "L_beta_temp", "T_entropy", "L_sigma_intensive",
                      "T_realignment_cost_is_transition_energy", "T_deSitter_entropy"],
        cross_refs=["T_fluctuation_response_is_two_faces", "T_thermodynamics_four_laws_synthesis",
                    "L_equip", "T_no_physical_time_flow_overclaim"],
        artifacts={
            "prerequisite": "FD4 bounds the energy spectrum above (E <= C_total*eps)",
            "ceiling_creates_branch": "bounded Z finite for all beta; unbounded converges only for beta>sigma/eps",
            "onset": "beta=sigma/eps: two faces balance, P uniform, <n>=C_total/2 (inversion onset)",
            "infinite_T": "beta=0: <n>->C_total; ln Z = C_total*sigma = S_dS (de Sitter entropy)",
            "class": "bounded-spectrum -> the laser/spin negative-temperature class",
            "parked": "dynamics of reaching inversion (T_no_physical_time_flow_overclaim); microcanonical claim avoided (Dunkel-Hilbert)",
        },
    )


_CHECKS = {"T_negative_temperature_needs_the_ceiling": check_T_negative_temperature_needs_the_ceiling}
def register(registry):
    registry.update(_CHECKS); return registry
def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "thermo:negative_temperature_ceiling",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "One bank check, check_T_negative_temperature_needs_the_ceiling, tier "
            "4 at epistemic='P': on the bounded canonical ensemble P(n) ~ "
            "e^{n(sigma - beta*eps)}, n in {0..C_total}, the FD4 ceiling is "
            "exactly what places the distinction ledger in the bounded-spectrum "
            "class that admits negative absolute temperature. With the ceiling, "
            "Z(beta) is finite for EVERY real beta, so beta = 0 (infinite "
            "temperature) and beta < 0 (population inversion) are accessible; "
            "remove the ceiling and the partition sum converges only for beta > "
            "sigma/eps -- the entire negative-temperature branch does not exist. "
            "The framework temperature beta = sigma/eps is the inversion onset "
            "(uniform distribution, <n> = C_total/2), and ln Z(beta=0) = C_total "
            "x sigma = S_dS (T_deSitter_entropy). Exact structural facts "
            "composing banked [P] lemmas (L_count/FD4, L_beta_temp, "
            "T_realignment_cost_is_transition_energy, T_entropy, "
            "L_sigma_intensive, T_deSitter_entropy). Scope fences named in- "
            "module: this is a canonical/accessibility statement, NOT a contested "
            "microcanonical-entropy claim (the Dunkel-Hilbert dispute does not "
            "bite); no claim that the cosmos or ledger IS in an inverted state; "
            "the dynamical route to inversion stays parked under "
            "T_no_physical_time_flow_overclaim. "
        ),
        "note": "Wave 7; single [P] check with explicit microcanonical-dispute fence",
    },
)
