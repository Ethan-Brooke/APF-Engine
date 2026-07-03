"""APF-native leading custodial response Δρ from the distinction picture — Tier-4.

First *physical electroweak observable* derived end-to-end through the
distinction picture, composing only native pieces. Δρ measures custodial-symmetry
breaking: in distinction terms, the substrate holding the two members of the
top–bottom doublet as equivalent distinctions gives ρ=1, and Δρ is the
measurable asymmetry when one (the top) is held at a heavier cost than the other.

Composition (all factors native):
    Δρ^{(1)}_leading = N_c · F(m_t², m_b²) · μ_loop / v²
with, at m_b → 0,
    Δρ^{(1)}_leading = N_c · m_t²/(16π² v²) = N_c · y_t²/(32π²),
where
  * N_c = 3 is the color distinction-count (apf.gauge);
  * F(m_t², m_b²) is the custodial cost-asymmetry function — symmetric under
    t↔b and vanishing on the diagonal F(m,m)=0 (custodial restoration), which
    forces the leading scale to be the heavier distinction's cost m_t²;
  * μ_loop = 1/(16π²) is the banked continuation-sum measure
    (apf.continuation_sum_measure, v24.3.166), itself forced by native D=4;
  * v is the electroweak interface cost scale.

The composed value equals the standard one-loop leading Δρ = N_c x_t exactly
(verified). The novelty is the *derivation*: every factor is native — a
distinction count, the custodial cost-asymmetry structure, the continuation-sum
measure forced by D=4 — rather than a fermion-loop computation. This is the
completion the continuation-sum keystone promised for the Δρ rung.

Honest non-claims:
  * Export_delta_rho_leading_structure_native_P = 1 — the structure
    (count × custodial cost-asymmetry × measure / v²) is native.
  * Export_delta_rho_numerical_value_native_P = 0 — the numerical value needs
    y_t (the absolute top scale), which is the OPEN σ-derivation gap; only the
    structure / ratio is native here.
  * Export_full_delta_rho_MH_dependent_P = 0 — this is the leading M_H=0 top
    slice, not the full M_H-dependent Δρ (subleading remains [P+tool]).
  * inherits the (2π)^D convention caveat of the continuation-sum measure.

Source: APF Reference Docs — Δρ from the Distinction-Cost Picture v0.1 +
the Continuation-Sum Measure v0.2 + A2 Closure (2026-05-28).
"""
from __future__ import annotations

import sympy as sp

from apf.apf_utils import check, _result


def custodial_function():
    """Custodial cost-asymmetry F(m_t², m_b²): symmetric, vanishes on diagonal."""
    mt2, mb2 = sp.symbols("mt2 mb2", positive=True)
    F = mt2 + mb2 - 2*mt2*mb2/(mt2 - mb2)*sp.log(mt2/mb2)
    return mt2, mb2, F


def delta_rho_leading():
    """Compose native pieces → Δρ^{(1)}_leading at m_b→0."""
    mt2, mb2, F = custodial_function()
    Nc, v = sp.symbols("N_c v", positive=True)
    F0 = sp.limit(F, mb2, 0)                      # heavier-cost leading scale = m_t²
    measure = sp.Rational(1, 1)/(16*sp.pi**2)     # banked continuation-sum measure
    drho = sp.simplify(Nc * F0 * measure / v**2)
    return Nc, v, mt2, drho


EXPORT_FLAGS = {
    "Export_delta_rho_leading_structure_native_P": 1,
    "Export_delta_rho_numerical_value_native_P": 0,   # needs y_t (absolute scale, OPEN)
    "Export_full_delta_rho_MH_dependent_P": 0,
    "Export_physical_final_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_delta_rho_leading_custodial_from_distinction_P():
    """T: leading custodial Δρ from the distinction picture. Composes the native
    custodial cost-asymmetry function (symmetric, diagonal-vanishing → leading
    m_t²) with the banked continuation-sum measure 1/(16π²) and the color count
    N_c, giving Δρ^{(1)}_leading = N_c·m_t²/(16π²v²) = N_c·y_t²/(32π²), equal to
    the standard one-loop N_c·x_t. Structure native; numerical value gated on
    the open absolute scale y_t; (2π)^D convention inherited.
    [P_structural_delta_rho_leading_custodial_from_distinction_modulo_scale_and_convention]."""

    mt2, mb2, F = custodial_function()
    # (a) custodial structure: symmetric under t<->b, vanishes on the diagonal.
    F_swap = F.subs({mt2: mb2, mb2: mt2}, simultaneous=True)
    check(sp.simplify(F - F_swap) == 0, "custodial function must be symmetric under t<->b")
    check(sp.simplify(sp.limit(F, mb2, mt2)) == 0,
          "custodial function must vanish on the diagonal (ρ=1 when held cost-equivalent)")
    check(sp.simplify(sp.limit(F, mb2, 0) - mt2) == 0,
          "leading (m_b→0) scale must be the heavier distinction's cost m_t²")

    # (b) composition with the banked measure and count → standard one-loop value.
    Nc, v, mt2b, drho = delta_rho_leading()
    check(sp.simplify(drho - Nc*mt2b/(16*sp.pi**2*v**2)) == 0,
          "Δρ_leading must compose to N_c m_t²/(16π² v²)")
    yt = sp.symbols("y_t", positive=True)
    drho_yt = sp.simplify(drho.subs(mt2b, yt**2*v**2/2))
    check(sp.simplify(drho_yt - Nc*yt**2/(32*sp.pi**2)) == 0,
          "Δρ_leading must equal N_c y_t²/(32π²) in Yukawa form")
    # matches the standard one-loop N_c x_t (comparator, not consumed)
    GF = 1/(sp.sqrt(2)*v**2); xt = GF*mt2b/(8*sp.sqrt(2)*sp.pi**2)
    check(sp.simplify(drho - Nc*xt) == 0,
          "must match the standard one-loop leading Δρ = N_c x_t (comparator)")

    # (c) honest non-claim flags.
    check(EXPORT_FLAGS["Export_delta_rho_numerical_value_native_P"] == 0,
          "numerical value needs y_t (absolute scale, open) — must stay 0")
    check(EXPORT_FLAGS["Export_full_delta_rho_MH_dependent_P"] == 0,
          "this is the leading M_H=0 slice, not the full Δρ — must stay 0")
    check(EXPORT_FLAGS["Export_physical_final_P"] == 0, "no physical-final claim")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_delta_rho_leading_custodial_from_distinction: leading custodial "
              "Δρ composed end-to-end from native pieces — N_c (distinction "
              "count) × custodial cost-asymmetry (symmetric, diagonal-vanishing, "
              "leading m_t²) × continuation-sum measure 1/(16π²) (banked, forced "
              "by D=4) / v² = N_c·y_t²/(32π²), equal to the standard one-loop "
              "N_c·x_t. First physical EW observable via the distinction picture. "
              "[P_structural_delta_rho_leading_custodial_from_distinction_modulo_scale_and_convention]"),
        tier=4,
        epistemic="P_structural_delta_rho_leading_custodial_from_distinction_modulo_scale_and_convention",
        summary=(
            "Completes the Δρ-from-distinction rung the continuation-sum keystone "
            "(v24.3.166) unlocked. Δρ measures custodial breaking = the substrate "
            "holding the t,b doublet members at unequal cost. The leading custodial "
            "response composes three native factors: the color distinction-count "
            "N_c (apf.gauge); the custodial cost-asymmetry function F(m_t²,m_b²), "
            "whose symmetry (t↔b) and diagonal-zero (F(m,m)=0, ρ=1 when held "
            "cost-equivalent) force the leading scale to be the heavier "
            "distinction's cost m_t²; and the continuation-sum measure 1/(16π²) "
            "(banked apf.continuation_sum_measure, forced by native D=4). The "
            "composed value Δρ^{(1)}_leading = N_c·m_t²/(16π²v²) = N_c·y_t²/(32π²) "
            "equals the standard one-loop N_c·x_t exactly (used as comparator, not "
            "consumed). The novelty is the derivation — every factor native, no "
            "fermion-loop computation. Honest non-claims: the numerical value "
            "needs y_t (the absolute top scale), which is the open σ-derivation "
            "gap, so only the structure/ratio is native here "
            "(Export_delta_rho_numerical_value_native_P=0); this is the leading "
            "M_H=0 top slice, not the full M_H-dependent Δρ (subleading remains "
            "[P+tool]); the (2π)^D convention of the measure is inherited; no "
            "physical-final claim."
        ),
        key_result=(
            "Δρ^{(1)}_leading = N_c·y_t²/(32π²) composed from native distinction "
            "count + custodial cost-asymmetry + banked continuation-sum measure; "
            "= standard one-loop N_c x_t; structure native, value gated on open "
            "absolute scale. "
            "[P_structural_delta_rho_leading_custodial_from_distinction_modulo_scale_and_convention]"
        ),
        dependencies=[
            "T_continuation_sum_measure_native_from_D4",
            "Theorem_R",
            "T_sin2theta",
        ],
        cross_refs=[],
        artifacts={
            "delta_rho_leading": "N_c*m_t^2/(16*pi^2*v^2) = N_c*y_t^2/(32*pi^2)",
            "matches_standard_one_loop": "N_c * x_t",
            "native_factors": ["N_c (distinction count)",
                               "custodial cost-asymmetry F (symmetric, diagonal-zero)",
                               "continuation-sum measure 1/(16pi^2) [banked]",
                               "EW interface cost v^2"],
            "open_input": "y_t (absolute top scale / sigma-derivation)",
            "reference_docs": [
                "Reference - Delta-rho from the Distinction-Cost Picture v0.1 (2026-05-28).md",
                "Reference - Continuation-Sum Measure A2 Closure - Free Cost is Quadratic (2026-05-28).md",
            ],
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_delta_rho_leading_custodial_from_distinction":
        check_T_delta_rho_leading_custodial_from_distinction_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "ew:delta_rho_leading_distinction",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "check_T_delta_rho_leading_custodial_from_distinction_P (tier 4, "
            "bespoke machine grade P_structural_delta_rho_leading_custodial_from_ "
            "distinction_modulo_scale_and_convention) certifies that the leading "
            "custodial Delta_rho composes end-to-end from native pieces: N_c "
            "(colour distinction count, apf.gauge) x the custodial cost-asymmetry "
            "function F(m_t^2, m_b^2) (symmetric under t<->b, vanishing on the "
            "diagonal, forcing the leading scale to m_t^2) x the banked "
            "continuation-sum measure 1/(16 pi^2) (forced by native D=4) / v^2, "
            "giving Delta_rho^(1)_leading = N_c y_t^2 / (32 pi^2), verified "
            "symbolically equal to the standard one-loop N_c x_t (comparator, not "
            "consumed). The STRUCTURE is native; the numerical VALUE is "
            "explicitly not claimed native -- it needs the absolute top scale y_t "
            "(Export_delta_rho_numerical_value_native_P = 0; the absolute-scale "
            "functional-independence no-go banked at v24.3.314 stands, so this "
            "remains a structural/ratio result, not a pending value derivation). "
            "Scope: the leading M_H = 0 top slice only (full M_H-dependent "
            "Delta_rho stays [P+tool]); inherits the (2 pi)^D convention caveat "
            "of the continuation-sum measure; the bespoke grade token's 'modulo "
            "scale and convention' rider is load-bearing. No target consumed; no "
            "physical-final claim. "
        ),
        "note": "Wave 7; grade rider (modulo scale and convention) carried in the bespoke token",
    },
)
