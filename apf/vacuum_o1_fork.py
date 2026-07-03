"""The vacuum O(1) reading fork: T10's 3/8 vs the two-factor 42/102.

v24.3.320 (2026-07-02). Banks the ADJUDICATED reading fork on the O(1)
prefactor of the vacuum-energy relation rho_Lambda/M_Pl^4 = O(1)/102^61,
per the two-stage fresh-context adjudication of 2026-07-02 (verdict
R4-WITH-DEMOTIONS 0.85; hostile audit HOLD-WITH-FIXES 0.85; note
"Reference - The Vacuum O1 Adjudication - T10 3-8 vs Two-Factor 42-102
Is an H0 Fork (2026-07-02)", APF Reference Docs).

The two chains:

  CHAIN A (geometric / count=area): T10 (gravity.py):
      Lambda*G = 3*pi/102^61, rho = Lambda/(8 pi G)
      => rho_Lambda/M_Pl^4 = (3/8)/102^61        log10 = -122.951
  CHAIN B (capacity / two-factor): L_Lambda_absolute_numerical_formula
  (fractional_reading.py) + T_Lambda_to_H0_inversion (lambda_absolute.py):
      rho_Lambda/M_Pl^4 = (42/102)/102^61        log10 = -122.910

Both O(1)s are READING-CONDITIONAL (chain A: count=area anchored-not-
derived per Face-2 Move 4 + T_Bek's imported kappa = 1/4; chain B: the
two-factor vacuum-fraction reading, registered [C]/[P_structural_
convention]). After the adjudication's demotions ZERO [P]s remain on
the O(1); the one [P] is on the shared exponent Omega = 102^61 (the
122 orders). R3 ("different quantities") was REFUTED at source: both
chains perform the identical present-epoch Omega_Lambda = 42/61
composition, so the two H0s are the same object.

HONEST GLOSS (audit finding E, the v24.3.305 fork-containment
precedent). This check banks a NAMED READING FORK — it certifies the
fork's exact arithmetic and its empirical discriminator. It is NEVER a
prediction row: neither branch is presented as THE APF H0 prediction.

THREE-WAY DISCRIMINATOR (ladder-light H0 program):
    H0 converges to ~67  =>  count=area exact (chain A branch);
    H0 converges to ~70  =>  two-factor exact (chain B branch);
    H0 converges to ~73  =>  both wrong.

MEASUREMENT-CONDITIONALITY CAVEAT (audit finding C; renamed from
'epoch-conditionality' at v24.3.344 -- the gate is DATA-conditional,
rho_Lambda itself is epoch-constant). The shared 0.05-decade
gate is measurement-conditional: its observational input log10(rho_Lambda/
M_Pl^4) is derived from H0 and scales as H0^2. At the Planck 2018
value (H0 = 67.36, obs = -122.944) BOTH coefficients pass. At the
73.5 distance-ladder endpoint (obs = -122.868) chain A FAILS the gate
(residual 0.082) while chain B passes (0.042). "Both pass" is a
statement at current data, not a measurement-invariant fact.
"""

import math as _math
from fractions import Fraction

from apf.apf_utils import check, _result

# Canonical constants (lockstep with apf/unification.py + lambda_absolute.py)
_K_SM = 61
_D_EFF = 102
_C_VACUUM = 42
_M_PL_EV = 1.220910e28          # Planck mass, eV (standard convention)
_KM_S_MPC_TO_EV = 2.1332e-35    # 1 km/s/Mpc in eV
_LOG10_OBS = -122.944           # Planck 2018, standard Planck-mass convention


def check_T_vacuum_o1_reading_fork():
    """T_vacuum_o1_reading_fork [P_structural] — the vacuum O(1) is a
    named two-branch reading fork with an H0 discriminator.

    CERTIFIES (all exact or computed live):

    (a) The exact coefficient ratio between the two banked O(1)s:
            (42/102) / (3/8) = 56/51    (9.8%).
    (b) BOTH coefficients pass the shared 0.05-decade gate at the
        current observation -122.944: residuals 0.034 (42/102) and
        0.007 (3/8) decades. (Epoch-conditional — see module docstring;
        at the 73.5 endpoint chain A fails, chain B passes.)
    (c) The two H0 endpoints obtained by composing each branch with
        Omega_Lambda = 42/61 [P] + flat FLRW (rho_crit = 3 H0^2 M_Pl^2
        / (8 pi)): 66.84 (count=area) and 70.03 (two-factor) km/s/Mpc,
        with ratio EXACTLY sqrt(56/51) — the same object, forked only
        by the O(1) reading. (The banked 66.84 rounding is T_deSitter_
        entropy's; the shared eV-conversion route here gives 66.83,
        conversion-constant rounding at the 0.02% level.)
    (d) The three-way discriminator (docstring): ~67 => count=area
        exact; ~70 => two-factor exact; ~73 => both wrong.
    (e) The honest gloss: a NAMED READING FORK (the .305 fork-
        containment precedent), never a prediction.

    STATUS. [P_structural]: the arithmetic identities are exact and the
    gate-passage facts computed, but the check's content is the FORK
    STRUCTURE — which reading is exact is empirically open and NOT
    decided here.

    DEPENDENCIES: T10_grav (chain A coefficient), T_deSitter_entropy
    (chain A H0 branch), L_Lambda_absolute_numerical_formula (chain B
    coefficient), T_Lambda_to_H0_inversion (chain B H0 branch).
    """
    # ---- (a) exact coefficient ratio ------------------------------------
    coef_B = Fraction(_C_VACUUM, _D_EFF)   # 42/102 = 7/17 (two-factor)
    coef_A = Fraction(3, 8)                # 3/8 (count=area, T10 geometric)
    ratio = coef_B / coef_A
    check(ratio == Fraction(56, 51),
          f"coefficient ratio (42/102)/(3/8) = {ratio} != 56/51")

    # ---- (b) both pass the shared 0.05-decade gate at current obs -------
    log10_exponent = -_K_SM * _math.log10(_D_EFF)
    log10_B = _math.log10(float(coef_B)) + log10_exponent   # -122.910
    log10_A = _math.log10(float(coef_A)) + log10_exponent   # -122.951
    res_B = abs(log10_B - _LOG10_OBS)
    res_A = abs(log10_A - _LOG10_OBS)
    check(res_B < 0.05 and res_A < 0.05,
          f"gate failure at current obs: res_B={res_B:.4f}, "
          f"res_A={res_A:.4f} (gate 0.05 decades)")
    check(abs(res_B - 0.034) < 0.002 and abs(res_A - 0.007) < 0.002,
          f"residuals off the adjudicated values: {res_B:.4f} vs 0.034, "
          f"{res_A:.4f} vs 0.007")
    # Epoch-conditionality witness (audit finding C): at the 73.5
    # distance-ladder endpoint the gate's obs input shifts by
    # 2*log10(73.5/67.36) and chain A FAILS while chain B passes.
    obs_735 = _LOG10_OBS + 2 * _math.log10(73.5 / 67.36)
    res_A_735 = abs(log10_A - obs_735)
    res_B_735 = abs(log10_B - obs_735)
    check(res_A_735 > 0.05 and res_B_735 < 0.05,
          f"measurement-conditionality witness failed: at 73.5-endpoint obs "
          f"{obs_735:.3f}, res_A={res_A_735:.4f} (expect >0.05), "
          f"res_B={res_B_735:.4f} (expect <0.05)")

    # ---- (c) the two H0 endpoints, ratio exactly sqrt(56/51) ------------
    # Omega_Lambda = 42/61 [P]; rho_crit = rho_Lambda/Omega_Lambda;
    # (H0/M_Pl)^2 = (8 pi / 3) * rho_crit/M_Pl^4.
    # Chain B: rho_L/M^4 = 42/102^62  => rho_crit/M^4 = 61/102^62.
    H_B_over_Mpl_sq = (8 * _math.pi / 3) * _K_SM / (float(_D_EFF) ** (_K_SM + 1))
    # Chain A: rho_L/M^4 = (3/8)/102^61 => rho_crit/M^4 = (3*61)/(8*42)/102^61.
    H_A_over_Mpl_sq = ((8 * _math.pi / 3) * (3 * _K_SM) / (8 * _C_VACUUM)
                       / (float(_D_EFF) ** _K_SM))
    H_B = _math.sqrt(H_B_over_Mpl_sq) * _M_PL_EV / _KM_S_MPC_TO_EV
    H_A = _math.sqrt(H_A_over_Mpl_sq) * _M_PL_EV / _KM_S_MPC_TO_EV
    check(abs(H_B - 70.03) < 0.05,
          f"two-factor H0 endpoint {H_B:.2f} != 70.03")
    check(abs(H_A - 66.84) < 0.05,
          f"count=area H0 endpoint {H_A:.2f} != 66.84")
    ratio_sq = (H_B / H_A) ** 2
    check(abs(ratio_sq - 56.0 / 51.0) < 1e-9,
          f"(H_B/H_A)^2 = {ratio_sq!r} != 56/51 — the two H0s must be "
          f"the same object forked only by the O(1)")

    return _result(
        name='T_vacuum_o1_reading_fork — the vacuum O(1) is a named '
             'two-branch reading fork with an H0 discriminator',
        tier=4,
        epistemic='P_structural',
        summary=(
            f"NAMED READING FORK (never a prediction row; the .305 "
            f"fork-containment precedent). The vacuum O(1) in "
            f"rho_Lambda/M_Pl^4 = O(1)/102^61 is banked twice: 3/8 "
            f"(T10, count=area reading) and 42/102 (two-factor "
            f"reading); exact ratio 56/51 (9.8%). At current obs "
            f"-122.944 BOTH pass the shared 0.05-decade gate "
            f"(residuals {res_A:.3f} and {res_B:.3f} decades) — "
            f"measurement-conditionally: at the 73.5 endpoint chain A fails "
            f"({res_A_735:.3f}) while chain B passes ({res_B_735:.3f}). "
            f"Composed with Omega_Lambda = 42/61 + flat FLRW the "
            f"branches give H0 = {H_A:.2f} (count=area) vs {H_B:.2f} "
            f"(two-factor) km/s/Mpc, ratio exactly sqrt(56/51). "
            f"Three-way discriminator: ~67 => count=area exact; ~70 => "
            f"two-factor exact; ~73 => both wrong. After the "
            f"adjudication's demotions zero [P]s remain on the O(1); "
            f"the [P] is on the shared exponent Omega = 102^61."
        ),
        key_result=(
            '(42/102)/(3/8) = 56/51 exactly; both pass the 0.05-decade '
            'gate at current obs (0.034 / 0.007); H0 fork 66.84 vs '
            '70.03 = sqrt(56/51); discriminator ~67/~70/~73. A named '
            'reading fork, not a prediction.'
        ),
        dependencies=['T10_grav', 'T_deSitter_entropy',
                      'L_Lambda_absolute_numerical_formula',
                      'T_Lambda_to_H0_inversion'],
        cross_refs=['T_42_over_102_structural_uniqueness',
                    'T_Lambda_coefficient_degeneracy_audit',
                    'T_Lambda_absolute_bulletproof'],
        artifacts={
            'coefficient_two_factor': '42/102',
            'coefficient_count_area': '3/8',
            'coefficient_ratio_exact': '56/51',
            'coefficient_ratio_pct': 9.8,
            'log10_obs_current': _LOG10_OBS,
            'residual_two_factor_decades': res_B,
            'residual_count_area_decades': res_A,
            'shared_gate_decades': 0.05,
            'obs_at_73p5_endpoint': obs_735,
            'residual_count_area_at_73p5': res_A_735,
            'residual_two_factor_at_73p5': res_B_735,
            'H0_count_area_km_s_Mpc': H_A,
            'H0_two_factor_km_s_Mpc': H_B,
            'H0_ratio_sq_exact': '56/51',
            'discriminator': ('~67 => count=area exact; ~70 => '
                              'two-factor exact; ~73 => both wrong'),
            'measurement_conditionality': (
                'the shared gate\'s obs input scales as H0^2; '
                'both-pass holds at current data only'),
            'gloss': ('named reading fork per the v24.3.305 '
                      'fork-containment precedent; not a prediction'),
        },
    )


# =============================================================================
# Registration
# =============================================================================

_CHECKS = {
    'T_vacuum_o1_reading_fork': check_T_vacuum_o1_reading_fork,
}


def register(registry):
    """Register the vacuum O(1) reading-fork check into the bank."""
    registry.update(_CHECKS)


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == '__main__':
    for _n, _r in run_all().items():
        print(('PASS' if _r.get('passed', True) else 'FAIL'), _n)


# ---------------------------------------------------------------------------
# IE onboarding (Wave 6, v24.3.346).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "gravity:vacuum_o1_h0_fork",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "The vacuum O(1) is a named two-branch reading fork with an H0 "
            "discriminator (check_T_vacuum_o1_reading_fork [P_structural], "
            "v24.3.320): both banked O(1) coefficients (42/102 count=area and "
            "3/8 two-factor) are reading-conditional, ratio exactly "
            "sqrt(56/51); H0 = 66.84 km/s/Mpc (count=area) vs 70.03 "
            "(two-factor). Adjudicating the fork selects which side of the "
            "Hubble tension APF predicts -- the standing watch item. Neither "
            "branch is exported as a global-[P] H0 claim (the H0-inversion "
            "and 42/102-uniqueness surfaces were demoted to "
            "P_structural_reading at the .320 landing). "
        ),
        "note": "Wave 6; the fork is deliberately preserved (principal's charter: preserve the tension), not a defect",
    },
)
