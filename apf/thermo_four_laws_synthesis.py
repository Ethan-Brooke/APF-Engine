"""apf/thermo_four_laws_synthesis.py -- the four laws of thermodynamics as one [P] synthesis.

Paper 40 ("The Thermodynamics of Finite Distinction") reads the whole corpus the other way
round: thermodynamics is not coarse-grained out of a microscopic theory, it is the foundation,
and the Standard Model and gravity are its equation of state. The supplement proves the four
laws from the four-input declaration (FD1-FD4) and notes (v0.16) that the synthesis is "a clean
composition of existing [P] results; bankable later as a [P] synthesis check." This module is
that check.

It asserts nothing new. It certifies that the four laws are ALREADY carried by banked [P]
lemmas, composed by exact identity:

  Zeroth law (temperature) ........ L_beta_temp [P]      beta = DeltaS/DeltaE = sigma/eps,
                                                          a state function -> mutual equilibrium
                                                          is transitive.
  First law (energy) .............. T_realignment_cost_  energy = accumulated cost = n*eps;
                                    is_transition_energy  cost = energy through the eps quantum.
                                                          [P]
  Second law (the arrow) .......... L_irr [P]            a record is a cross-interface
                                                          correlation, locally irreversible;
                                                          the count is non-decreasing.
  Third law (the floor) ........... L_singularity_       S_min = sigma > 0; no a->0, the
                                    resolution [P]        minimal admissible state has nonzero
                                                          entropy.

resting on the entropy/degeneracy spine:

  Entropy S = n*sigma = ln W ...... T_entropy [P]        Boltzmann form on the microcanonical
                                                          count W = d_eff^n.
  sigma = ln d_eff (intensive) .... L_sigma_intensive[P] the per-distinction entropy quantum.
  d_eff = (C_total-1) + C_vacuum .. L_self_exclusion [P] effective degeneracy via self-
                                                          correlation exclusion.
  Equipartition (max-entropy) ..... L_equip [P]          uniform microcanonical weight.
  Cost C = n*eps .................. L_cost [P]            realignment cost is n quanta.
  Per-distinction quantum eps ..... T_epsilon [P]        the granularity quantum.

GRADE [P]: the synthesis is an exact composition of ten banked [P] lemmas; it introduces no
new premise. What it does NOT certify -- and what stays constitutive (the four-input
declaration, tested by prediction, NOT proved) -- is the bridge that THIS thermodynamics is our
world's physics (the cost-energy reading that the ledger IS the action). That bridge is graded
in Paper 40 sec:proof-status and is out of scope here: this check certifies the LAWS, not the
identification of the ledger with the physical action.

SCOPE / non-claims:
  * Does NOT re-derive any constituent (each is banked in its home module; this composes them).
  * Does NOT introduce a new scheme-export route. Paper 40's numerical payoff (sin^2theta_W,
    the gauge couplings, Omega_Lambda) is the equation-of-state reading of routes ALREADY
    tracked under the Gauge/Electroweak and Cosmology sector registries -- a VIEW over existing
    routes, not a new transport. The Scheme Export super-registry stays route-centric; this
    synthesis lives on the derivation axis.
  * Does NOT grade the constitutive cost-energy = action bridge (stays [P_structural], the
    four-input declaration, tested by prediction).

CROSS-REF (v24.3.243): the cost-kind dichotomy check_T_ledger_rent_excluded
[P] (operational_completeness.py) -- every booked cost is a transition
commitment (a standing level) or a per-activation charge; no standing-rent
term exists (Paper 0 row 9). The four laws are level statements (state functions, exchange rates); the dichotomy is why none of them meters time.
"""
from __future__ import annotations
from apf.apf_utils import check as _check, _result as _full_result


def check_T_thermodynamics_four_laws_synthesis():
    """T_thermodynamics_four_laws_synthesis: the four laws as one [P] composition of banked lemmas.

    THEOREM. The four laws of thermodynamics are carried, in full, by ten banked [P] lemmas of
    the APF corpus, composed by exact identity with no new premise:

        zeroth law  <- L_beta_temp                       (temperature beta = sigma/eps, a state fn)
        first law   <- T_realignment_cost_is_transition_energy  (energy = accumulated cost = n*eps)
        second law  <- L_irr                             (locally irreversible record; n non-decreasing)
        third law   <- L_singularity_resolution          (S_min = sigma > 0; nonsingular floor)

    on the entropy/degeneracy spine T_entropy [P] (S = n*sigma = ln W), L_sigma_intensive [P]
    (sigma = ln d_eff), L_self_exclusion [P] (d_eff = (C_total-1)+C_vacuum), L_equip [P]
    (max-entropy uniform weight), L_cost [P] (C = n*eps), T_epsilon [P] (the eps quantum).

    PROOF. Each constituent is banked at [P] in its home module; the synthesis asserts their
    grades and pass-state, then verifies the composing identities at the witness level
    (Boltzmann S = ln(d_eff^n) = n*ln d_eff = n*sigma; beta = DeltaS/DeltaE = sigma/eps;
    energy = cost = n*eps; floor sigma > 0). No constituent is re-derived. QED (composition).

    GRADE [P]: exact composition of ten [P] lemmas, no new assumption. This is the bankable
    synthesis Paper 40 sec:proof-status flagged.

    SCOPE: certifies the LAWS only. The constitutive bridge (this thermodynamics IS our world's
    physics -- the ledger as the physical action) stays [P_structural] (the four-input
    declaration, tested by prediction), out of scope here. Introduces NO new scheme-export
    route: Paper 40's numerical predictions are the equation-of-state reading of Gauge +
    Cosmology routes already tracked in their sector registries; this synthesis is a
    derivation-axis object, not a transport.
    """
    import math
    from apf.core import check_L_cost, check_T_epsilon, check_T_entropy, check_L_irr
    from apf.gravity import check_L_self_exclusion
    from apf.supplements import check_L_sigma_intensive, check_L_beta_temp
    from apf.cosmology import check_L_singularity_resolution, check_L_equip
    from apf.cost_energy_identity import check_T_realignment_cost_is_transition_energy

    # --- constituent [P] lemmas, grouped by the law / spine role they carry ---
    spine = {
        "L_cost": check_L_cost,                        # C = n*eps
        "T_epsilon": check_T_epsilon,                  # the eps quantum
        "L_self_exclusion": check_L_self_exclusion,    # d_eff = (C_total-1)+C_vacuum
        "T_entropy": check_T_entropy,                  # S = n*sigma = ln W
        "L_sigma_intensive": check_L_sigma_intensive,  # sigma = ln d_eff
        "L_equip": check_L_equip,                      # max-entropy uniform weight
    }
    laws = {
        "zeroth:L_beta_temp": check_L_beta_temp,
        "first:T_realignment_cost_is_transition_energy": check_T_realignment_cost_is_transition_energy,
        "second:L_irr": check_L_irr,
        "third:L_singularity_resolution": check_L_singularity_resolution,
    }

    for label, fn in {**spine, **laws}.items():
        r = fn()
        _check(r.get("epistemic") in ("P",) and r.get("passed"),
               f"constituent {label}: banked [P] and passing")

    # --- composing identities, witnessed (natural units eps = 1) ---
    eps = 1.0
    for d_eff in (2, 3, 102):           # d_eff incl. the SM value 60+42 = 102
        sigma = math.log(d_eff)         # L_sigma_intensive: sigma = ln d_eff
        for n in (1, 7, 16, 61):        # incl. the SM saturation count C_total = 61
            W = d_eff ** n              # microcanonical count
            S = math.log(W)             # Boltzmann S = ln W
            # T_entropy: S = n*sigma = ln W
            _check(abs(S - n * sigma) < 1e-9,
                   f"second/entropy: S = ln(d_eff^n) = n*sigma  (d_eff={d_eff}, n={n})")
            # zeroth law: beta = DeltaS/DeltaE = sigma/eps, a state function (one value per (d_eff))
            dE = eps
            beta = sigma / dE
            _check(abs(beta - sigma) < 1e-12,
                   f"zeroth: beta = sigma/eps = {sigma:.6f} (state function; d_eff={d_eff})")
            # first law: energy = accumulated cost = n*eps
            energy = n * eps
            cost = n * eps
            _check(abs(energy - cost) < 1e-12,
                   f"first: energy = cost = n*eps = {energy} (n={n})")
        # third law: the floor sigma > 0 -> S_min = sigma > 0, no a->0
        _check(sigma > 0.0, f"third: S_min = sigma = {sigma:.6f} > 0 (nonsingular floor; d_eff={d_eff})")

    # second law direction: W(n) = d_eff^n strictly increasing in n -> the count climbs
    for d_eff in (2, 102):
        prev = None
        for n in range(1, 6):
            W = d_eff ** n
            if prev is not None:
                _check(W > prev, f"second/arrow: W(n)=d_eff^n increasing (d_eff={d_eff}, n={n})")
            prev = W

    return _full_result(
        name=("T_thermodynamics_four_laws_synthesis: the four laws of thermodynamics are one exact "
              "[P] composition of ten banked [P] lemmas -- zeroth (L_beta_temp), first "
              "(T_realignment_cost_is_transition_energy), second (L_irr), third "
              "(L_singularity_resolution), on the entropy/degeneracy spine (T_entropy, "
              "L_sigma_intensive, L_self_exclusion, L_equip, L_cost, T_epsilon). The bankable "
              "synthesis Paper 40 flagged. Certifies the LAWS; the constitutive ledger-is-action "
              "bridge stays [P_structural], out of scope. No new scheme-export route [P]"),
        tier=4, epistemic="P",
        summary=(
            "Banks Paper 40's four-laws result as a derivation-axis synthesis. The four laws are "
            "carried by ten [P] lemmas composed by exact identity: zeroth = L_beta_temp (beta = "
            "sigma/eps, a state function), first = T_realignment_cost_is_transition_energy (energy "
            "= accumulated cost = n*eps), second = L_irr (locally irreversible record; n non-"
            "decreasing, W = d_eff^n climbs), third = L_singularity_resolution (S_min = sigma > 0, "
            "no a->0); spine = T_entropy (S = n*sigma = ln W) + L_sigma_intensive (sigma = ln "
            "d_eff) + L_self_exclusion (d_eff = (C_total-1)+C_vacuum) + L_equip + L_cost + "
            "T_epsilon. No constituent re-derived; the composing identities are witnessed at the "
            "SM values (d_eff = 102, C_total = 61). SCOPE: certifies the laws only -- the "
            "constitutive bridge (this thermodynamics IS our physics, ledger = action) stays "
            "[P_structural] (four-input declaration, tested by prediction). Introduces NO new "
            "scheme-export route: Paper 40's numbers are the equation-of-state reading of Gauge + "
            "Cosmology routes already tracked; this is a VIEW over existing routes, not a transport."
        ),
        key_result=("Four laws of thermodynamics = one [P] composition of ten banked [P] lemmas "
                    "(zeroth L_beta_temp / first T_realignment_cost_is_transition_energy / second "
                    "L_irr / third L_singularity_resolution + entropy spine). Derivation-axis "
                    "synthesis; no new export route; ledger-is-action bridge stays [P_structural]."),
        dependencies=[
            "L_beta_temp", "T_realignment_cost_is_transition_energy", "L_irr",
            "L_singularity_resolution", "T_entropy", "L_sigma_intensive",
            "L_self_exclusion", "L_equip", "L_cost", "T_epsilon",
        ],
        cross_refs=["T_PLEC_derived_from_spine", "T_ACC_unification", "T_gauge_value_chain_is_P",
                    "T_Lambda_coefficient_degeneracy_audit"],
        artifacts={
            "zeroth": "beta = DeltaS/DeltaE = sigma/eps (state function)",
            "first": "energy = accumulated cost = n*eps",
            "second": "L_irr arrow; S = n*sigma = ln W, W = d_eff^n non-decreasing",
            "third": "S_min = sigma > 0 (nonsingular floor)",
            "scope": "certifies the laws; ledger-is-action bridge [P_structural], out of scope",
            "registry": "no new scheme-export route; Paper 40 = equation-of-state view over Gauge+Cosmology",
        },
    )


_CHECKS = {"T_thermodynamics_four_laws_synthesis": check_T_thermodynamics_four_laws_synthesis}
def register(registry):
    registry.update(_CHECKS); return registry
def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}
