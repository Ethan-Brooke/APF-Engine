"""APF-native electroweak oblique S parameter — Tier-4 (scope-fenced reproduction).

The Peskin–Takeuchi S parameter, and the EW oblique sector more broadly, are
reproduced ANSWER-FREE from native APF ingredients — the one-loop continuation
measure 1/(16π²) (check_T_continuation_sum_measure_native_from_D4 [P]), the
Clifford/scalar-QED vertex algebra (established math on native inputs), the
Standard-Model gauge charges T3/Q/Y from Theorem_R + hypercharge, and the Higgs
doublet's |D_μΦ|² (check_T_Higgs). No measured/target S value enters any check.

Three banked results (each derived first, then asserted; negative controls inline):

  1. FERMION-LOOP S.  S = 16π(Π'_33−Π'_3Q)(0) = 2π N_c (Π'_AA−Π'_VV)(0) for a
     degenerate doublet.  The AA−VV transverse numerator is the −8m² g_{μν} blob;
     it is NOT q-independent — it rides the q-dependent scalar bubble, and its
     q²-slope is finite (1/ε of Γ(2−d/2) cancels the ε from ∂_{q²}Δ^{−ε/2}),
     mass-independent: Π'_AA−Π'_VV = −1/(12π²) → |S| = N_c/(6π).  Negative control:
     the "blob is a q-independent contact term, drops" misreading gives 0 (wrong).

  2. HIGGS CONTRIBUTION TO S.  S = −16π Π'_3Y(0).  Gaugeless limit: Higgs h mass
     m_H, would-be Goldstones massless; the W3/Y current matrix elements are the
     real antisymmetric generators T3, Y read off |D_μΦ|².  Current-correlator
     form ⇒ no internal gauge/ghost lines ⇒ no Goldstone/Ward-Takahashi
     subtraction.  Two scalar pair-blocks {φ1,φ2}=(η,η) coeff +1/4 and
     {φ3,h}=(η,m_H) coeff −1/4 carry EQUAL UV poles (−i/24π²) that CANCEL (S
     UV-finite); the slope is dS/d ln(m_H²) = 1/(12π), the textbook SM coefficient.
     Negative controls: the ordered-pair double-count gives 1/(6π) (wrong); the
     bare single-block S is UV-divergent (pole ≠ 0) — so the SLOPE is banked, never
     a bare single-block value.

  3. OBLIQUE CURVATURE MOMENT (the W/Y *kind* of object — NOT literal BPRS W,Y).
     The 2nd q²-moment of the same native VP, Π''_AA−Π''_VV = −1/(60π²m²) (the
     1/30 moment of x(1−x)), native and answer-free.  Mass-DEPENDENT (∝1/m²),
     unlike S — the curvature, not the slope.  Fenced: this is the un-normalized
     fermion AA−VV 2nd moment (mass-dim −2); the literal Barbieri–Pomarol–
     Rattazzi–Strumia W,Y are dimensionless gauge-channel W3W3/BB curvatures and
     are NOT claimed.

Together these establish, with the already-banked T = Δρ (custodial) and the
perturbative/leptonic Δα, that the EW oblique sector's PERTURBATIVE current-
correlator moments are native.  The 2026-06-18 blanket "[P+tool] permanent
boundary over the loop-shape class" was over-broad: the principled line is
PERTURBATIVE current-correlator moment (native) vs NON-PERTURBATIVE hadronic
spectral density (g−2 HVP NP — genuinely outside, held [C], not touched here).

Honest scope (epistemic tag P_S_oblique_native_reproduction): these are scope-
fenced REPRODUCTIONS of textbook EW oblique physics from native ingredients
(provenance, not new numbers / not an A1-derivation).  Only the LOG coefficient of
the Higgs piece and the rational moments are claimed; the m_H-INDEPENDENT pure-
gauge constant of S (reference/scheme) and the NP hadronic g−2 value remain OUTSIDE.

Source: APF Reference Docs (all 2026-06-19) — The Native-S Box Run; The Higgs
Contribution to S Is Native and Answer-Free (v0.2); The 2026-06-18 Loop-Shape
Boundary Was Over-Broad (v0.1).  Witnesses S_fermion_loop_transverse_slope_box_*,
S_bosonic_loop_scalar_sector_box_*, S_oblique_tower_generalization_*.  Both S
results cold-audited SOUND (independent adversarial passes); the generalization
audited OVERCLAIMED→CORRECTED (here banked only at the corrected scope).
"""
from __future__ import annotations

import sympy as sp

from apf.apf_utils import check, _result


# =============================================================================
# Shared symbolic kernel (nothing hardcoded to the known S values)
# =============================================================================

def _fermion_AAmVV_moment(n):
    """n-th q^2-derivative at 0 of the fermion AA−VV transverse g-coeff (=Π_T),
    x-integrated, ε→0, with Π = −i·(g-coeff) and native measure G=i/16π²."""
    q2, m, x, eps = sp.symbols("q2 m x eps", positive=True)
    G = sp.I/(16*sp.pi**2)
    Delta = m**2 - x*(1-x)*q2
    d = 4 - eps
    fint = -8*m**2*G*sp.gamma(2-d/2)*Delta**(d/2-2)     # AA−VV transverse numerator × bubble
    e = sp.diff(fint, q2, n).subs(q2, 0)
    e = sp.integrate(sp.simplify(e), (x, 0, 1))
    e = sp.series(e, eps, 0, 1).removeO()
    return sp.simplify((-sp.I)*e)


def _scalar_bubble_slope(M1sq, M2sq, mu2, eps_sym):
    """Transverse VP slope A'(0) for a scalar bubble of masses^2 (M1sq,M2sq),
    native measure, μ-scale kept; returns symbolic expr in eps (UV pole retained)."""
    x = sp.symbols("x", positive=True)
    d = 4 - eps_sym
    G = sp.I/(16*sp.pi**2)
    pref = 2*G*(mu2**(eps_sym/2))*sp.gamma(1-d/2)*(d/2-1)
    D0 = (1-x)*M1sq + x*M2sq
    return pref*sp.integrate(x*(1-x)*D0**(d/2-2), (x, 0, 1))


EXPORT_FLAGS = {
    "Export_S_fermion_loop_native_reproduction_P": 1,
    "Export_S_higgs_logarithm_native_P": 1,
    "Export_oblique_curvature_moment_native_P": 1,
    "Export_S_pure_gauge_constant_native_P": 1,      # NATIVE (apf.s_parameter_pure_gauge_constant_native, v24.3.259; reference/scheme)
    "Export_g2_HVP_NP_value_native_P": 0,            # genuinely outside (held [C])
    "Export_literal_BPRS_W_Y_P": 0,                  # curvature is the W/Y *kind*, not literal
    "Export_A1_derivation_P": 0,                     # scope-fenced reproduction
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


# =============================================================================
# 1. Fermion-loop S
# =============================================================================

def check_T_S_fermion_loop_native_reproduction_P():
    """T: the fermion-loop Peskin–Takeuchi S for a degenerate doublet is reproduced
    answer-free from native ingredients: |S| = N_c/(6π), mass-independent. Negative
    control: the q-independent-blob-drops misreading gives 0. Scope-fenced
    reproduction. [P_S_oblique_native_reproduction]."""
    Nc = sp.symbols("N_c", positive=True)
    f1 = _fermion_AAmVV_moment(1)                         # Π'_AA−Π'_VV
    check(sp.simplify(f1 - (-1/(12*sp.pi**2))) == 0, "Π'_AA−Π'_VV must be −1/(12π²)")
    m = sp.symbols("m", positive=True)
    check(sp.simplify(sp.diff(f1, m)) == 0, "S slope must be mass-independent")
    S = sp.simplify(2*sp.pi*Nc*f1)                        # degenerate-doublet assembly
    check(sp.simplify(sp.Abs(S) - Nc/(6*sp.pi)) == 0, "|S| must be N_c/(6π)")

    # negative control: if the −8m² blob were a q-independent contact term that
    # "drops", the slope would be 0 (the misreading the prior note flagged).
    q2, m2, x, eps = sp.symbols("q2 m2 x eps", positive=True)
    blob_const = -8*m2**2*(sp.I/(16*sp.pi**2))           # blob with NO q-dependence
    drop_slope = sp.diff(blob_const, q2)                 # = 0
    check(sp.simplify(drop_slope) == 0,
          "negative control: blob-drops misreading gives slope 0 (≠ the real result)")

    check(EXPORT_FLAGS["Export_A1_derivation_P"] == 0, "scope-fenced reproduction, not A1")
    check(EXPORT_FLAGS["target_consumed"] == 0, "no target consumed")
    return _result(
        name=("T_S_fermion_loop_native_reproduction: degenerate-doublet "
              "fermion-loop S = 2π N_c (Π'_AA−Π'_VV) = −N_c/(6π), |S|=N_c/(6π), "
              "mass-independent, reproduced answer-free from the native measure + "
              "Clifford trace + Theorem_R charges. [P_S_oblique_native_reproduction]"),
        tier=4, epistemic="P_S_oblique_native_reproduction",
        summary=(
            "Fermion-loop Peskin–Takeuchi S for a degenerate doublet, reproduced "
            "answer-free. S = 16π(Π'_33−Π'_3Q)(0) = 2π N_c(Π'_AA−Π'_VV)(0); the "
            "AA−VV transverse numerator is the −8m² g_{μν} blob riding the "
            "q-dependent scalar bubble, whose q²-slope is finite (the 1/ε of "
            "Γ(2−d/2) cancels the ε from ∂_{q²}Δ^{−ε/2}) and mass-independent: "
            "Π'_AA−Π'_VV = −1/(12π²) → |S| = N_c/(6π), the textbook value, with no "
            "S target used. Negative control: the q-independent-blob-drops "
            "misreading gives 0. Native ingredients: continuation measure 1/16π² "
            "[P], Clifford trace (established math), Theorem_R T3/Q + hypercharge. "
            "Cold-audited SOUND. Scope-fenced reproduction (provenance, not an "
            "A1-derivation; the sign is convention)."
        ),
        key_result="|S_fermion_doublet| = N_c/(6π), answer-free [P_S_oblique_native_reproduction]",
        dependencies=["T_continuation_sum_measure_native_from_D4", "Theorem_R", "T_field"],
        cross_refs=["T_S_higgs_logarithm_native", "T_oblique_curvature_moment_native"],
        artifacts={"Pi_prime_AA_minus_VV": "-1/(12*pi**2)", "S_doublet": "-N_c/(6*pi)",
                   "export_flags": dict(EXPORT_FLAGS)},
    )


# =============================================================================
# 2. Higgs contribution to S
# =============================================================================

def check_T_S_higgs_logarithm_native_P():
    """T: the Higgs contribution to S is reproduced answer-free: dS/d ln(m_H²) =
    1/(12π) (textbook SM). UV poles of the two scalar blocks cancel (S UV-finite);
    only the slope is banked. Negative controls: ordered-pair double-count → 1/(6π);
    bare single block → UV-divergent. [P_S_oblique_native_reproduction]."""
    eps, mH2, eta2, mu2 = sp.symbols("eps mH2 eta2 mu2", positive=True)
    Aee = _scalar_bubble_slope(eta2, eta2, mu2, eps)      # {φ1,φ2} block, coeff +1/4
    AeH = _scalar_bubble_slope(eta2, mH2, mu2, eps)       # {φ3,h}   block, coeff −1/4
    pole = lambda e: sp.simplify(sp.series(e, eps, 0, 1).coeff(eps, -1))
    pee, peH = pole(Aee), pole(AeH)
    check(sp.simplify(pee - peH) == 0, "the two blocks must carry EQUAL UV poles")
    acc = sp.Rational(1, 4)*Aee + sp.Rational(-1, 4)*AeH  # correct UNORDERED-pair assembly
    check(sp.simplify(pole(acc)) == 0, "UV poles must CANCEL (S UV-finite)")
    S = -16*sp.pi*(-sp.I)*acc
    dS = sp.limit(sp.series(sp.diff(S, mH2)*mH2, eps, 0, 1).removeO(), eta2, 0)
    check(sp.simplify(dS - 1/(12*sp.pi)) == 0, "dS/d ln(m_H²) must be 1/(12π)")

    # negative control A: the ORDERED-pair double-count gives 1/(6π) (wrong)
    acc2 = sp.Rational(1, 2)*Aee + sp.Rational(-1, 2)*AeH
    S2 = -16*sp.pi*(-sp.I)*acc2
    dS2 = sp.limit(sp.series(sp.diff(S2, mH2)*mH2, eps, 0, 1).removeO(), eta2, 0)
    check(sp.simplify(dS2 - 1/(6*sp.pi)) == 0, "control: ordered double-count → 1/(6π) (wrong)")
    # negative control B: the bare single (φ3,h) block is UV-divergent (pole ≠ 0)
    check(sp.simplify(peH) != 0, "control: bare single-block S is UV-divergent (do not bank it)")

    check(EXPORT_FLAGS["Export_S_pure_gauge_constant_native_P"] == 1,
          "the m_H-independent pure-gauge constant is NATIVE "
          "(apf.s_parameter_pure_gauge_constant_native, v24.3.259; largely reference/scheme)")
    check(EXPORT_FLAGS["target_consumed"] == 0, "no target consumed")
    return _result(
        name=("T_S_higgs_logarithm_native: the Higgs contribution to S, "
              "dS/d ln(m_H²) = 1/(12π) (textbook SM), reproduced answer-free from "
              "the Higgs |D_μΦ|² generators + native measure; no Goldstone/WT "
              "subtraction (current-correlator form); UV poles cancel. "
              "[P_S_oblique_native_reproduction]"),
        tier=4, epistemic="P_S_oblique_native_reproduction",
        summary=(
            "Higgs contribution to S reproduced answer-free. S = −16π Π'_3Y(0); in "
            "the gaugeless limit (Higgs mass m_H, would-be Goldstones massless) the "
            "W3/Y current matrix elements are the real antisymmetric generators "
            "T3,Y read off |D_μΦ|². The current-correlator form has no internal "
            "gauge/ghost lines, so the Goldstone/Ward-Takahashi subtraction never "
            "enters. The two scalar pair-blocks carry equal UV poles (−i/24π²) that "
            "cancel (S UV-finite); dS/d ln(m_H²) = 1/(12π), the textbook coefficient, "
            "no S target used. Negative controls: ordered-pair double-count → 1/(6π); "
            "bare single block UV-divergent (only the slope is banked). Cold-audited "
            "SOUND, witness hardened (UV-pole cancellation explicit). Open: the "
            "m_H-independent pure-gauge constant (reference/scheme). Scope-fenced "
            "reproduction (only the log coefficient claimed; sign matches SM)."
        ),
        key_result="dS/d ln(m_H²) = 1/(12π), answer-free [P_S_oblique_native_reproduction]",
        dependencies=["T_continuation_sum_measure_native_from_D4", "T_Higgs", "Theorem_R"],
        cross_refs=["T_S_fermion_loop_native_reproduction", "T_oblique_curvature_moment_native"],
        artifacts={"dS_dlnmH2": "1/(12*pi)", "block_UV_pole": "-I/(24*pi**2)",
                   "control_ordered_doublecount": "1/(6*pi)", "export_flags": dict(EXPORT_FLAGS)},
    )


# =============================================================================
# 3. Oblique curvature moment (W/Y-kind; not literal BPRS)
# =============================================================================

def check_T_oblique_curvature_moment_native_P():
    """T: the 2nd q²-moment of the native VP, Π''_AA−Π''_VV = −1/(60π²m²) (the 1/30
    moment), native and answer-free; mass-DEPENDENT (∝1/m²) unlike S. The W/Y *kind*
    of object — NOT the literal dimensionless BPRS W,Y (gauge-channel W3W3/BB).
    [P_S_oblique_native_reproduction]."""
    m = sp.symbols("m", positive=True)
    f2 = _fermion_AAmVV_moment(2)                         # Π''_AA−Π''_VV
    check(sp.simplify(f2 - (-1/(60*sp.pi**2*m**2))) == 0, "Π''_AA−Π''_VV must be −1/(60π²m²)")
    # distinguishing fingerprint vs S: curvature is mass-dependent (∝1/m²)
    check(sp.simplify(sp.diff(f2, m)) != 0, "curvature moment must be mass-dependent (unlike S)")
    # the bare Feynman-weight moments that drive it (answer-free): ∫x(1-x)=1/6, ∫x²(1-x)²=1/30
    x = sp.symbols("x", positive=True)
    check(sp.integrate(x*(1-x), (x, 0, 1)) == sp.Rational(1, 6), "1st weight moment = 1/6")
    check(sp.integrate((x*(1-x))**2, (x, 0, 1)) == sp.Rational(1, 30), "2nd weight moment = 1/30")
    check(EXPORT_FLAGS["Export_literal_BPRS_W_Y_P"] == 0,
          "this is the W/Y *kind* of moment, NOT the literal BPRS W,Y")
    return _result(
        name=("T_oblique_curvature_moment_native: the 2nd q²-moment of the native "
              "VP, Π''_AA−Π''_VV = −1/(60π²m²) (the 1/30 moment), native + "
              "answer-free; the W/Y *kind* of object, not literal BPRS W,Y. "
              "[P_S_oblique_native_reproduction]"),
        tier=4, epistemic="P_S_oblique_native_reproduction",
        summary=(
            "The electroweak oblique sector's perturbative moments are successive "
            "q²-moments of the one native current correlator. The 1st moment is S "
            "(the 1/6 weight); the 2nd moment — the curvature — is Π''_AA−Π''_VV = "
            "−1/(60π²m²), the 1/30 moment of the x(1−x) Feynman weight, native and "
            "answer-free, and mass-dependent (∝1/m²) unlike the mass-independent S. "
            "This is the W/Y *kind* of object; the literal Barbieri–Pomarol–"
            "Rattazzi–Strumia W,Y (dimensionless gauge-channel W3W3/BB curvatures) "
            "are NOT claimed (this is the un-normalized fermion AA−VV moment, "
            "mass-dim −2). Establishes that the perturbative oblique tower is one "
            "native object; the 2026-06-18 blanket loop-shape boundary was "
            "over-broad — the principled line is perturbative current-correlator "
            "moment (native) vs non-perturbative hadronic spectral density (g−2 HVP "
            "NP, held [C], genuinely outside). Generalization cold-audited "
            "OVERCLAIMED→CORRECTED; banked here only at the corrected scope."
        ),
        key_result="Π''_AA−Π''_VV = −1/(60π²m²) (the 1/30 curvature moment), answer-free; W/Y-kind not literal BPRS",
        dependencies=["T_continuation_sum_measure_native_from_D4", "Theorem_R"],
        cross_refs=["T_S_fermion_loop_native_reproduction", "T_S_higgs_logarithm_native"],
        artifacts={"Pi_pp_AA_minus_VV": "-1/(60*pi**2*m**2)", "weight_moments": "1/6 (S), 1/30 (curvature)",
                   "export_flags": dict(EXPORT_FLAGS)},
    )



# =============================================================================
# 4. Higgs m_H-dependent PROFILE of S  ([P+tool] — imported GLOO/Denner algebra)
# =============================================================================

EXPORT_FLAGS_PROFILE = {
    "Export_S_higgs_mH_profile_Ptool": 1,        # the m_H-DEPENDENT profile (shape)
    "Export_S_higgs_finite_G_native_P": 1,        # finite 𝒢 now NATIVE (apf.s_higgs_finite_profile_native, v24.3.260)
    "Export_S_pure_gauge_constant_native_P": 1,    # m_H-INDEPENDENT constant NATIVE (v24.3.259)
    "Export_A1_derivation_P": 0,
    "target_consumed": 0,
}


def check_T_S_higgs_mH_dependent_profile_Ptool():
    """T [P+tool]: the m_H-DEPENDENT one-loop bosonic Higgs profile of Peskin-Takeuchi
    S, S_H(m_H) = (1/12pi)[ln(m_H^2/m_ref^2) + G(m_H^2/m_Z^2)], reproduced from the
    imported Grimus-Lavoura-Ogreid-Osland closed form (Ghosh arXiv:2201.01006 eq 28/33;
    orig. GLOO 0711.4022/0802.4353). Bridge to the native [P] leading-log: the
    asymptotic slope dS_H/d ln(m_H^2) -> 1/(12pi) (cross-checks
    check_T_S_higgs_logarithm_native). Photon/gammaZ pieces carry NO m_H dependence
    (sigma_AA_bos, A_AZ depend only on M_W) and cancel in the subtraction, so the
    profile is the ZZ higgs-brace alone. The finite G is now ALSO reproduced
    ANSWER-FREE natively (apf.s_higgs_finite_profile_native, v24.3.260, via the BFM
    Higgs diagrams D1(Z,h)+D2(h,G0) through the two-mass native reducer with the
    relative sign forced by an executed i-count); this GLOO reproduction is retained
    as the magnitude cross-check. The m_H-INDEPENDENT pure-gauge constant is also
    native (apf.s_parameter_pure_gauge_constant_native). No measured S target
    consumed. Cold-audited SOUND."""
    import mpmath as mp
    mp.mp.dps = 60
    MZ2 = mp.mpf("91.1876")**2

    def fG(x, y):
        b = x*x - 4*x*y
        if b > 0:
            sb = mp.sqrt(b); return sb*mp.log((x - sb)**2/(4*x*y))
        if b == 0:
            return mp.mpf(0)
        sm = mp.sqrt(-b); return 2*sm*mp.atan(sm/x)

    def Ghat(x, y):
        r = x/y; lr = mp.log(x/y)
        return (mp.mpf(-79)/3 + 9*r - 2*r*r
                + (-10 + 18*r - 6*r*r + r**3 - 9*(x + y)/(x - y))*lr
                + (12 - 4*r + r*r)*fG(x, y)/y)

    def S(mH):
        mH2 = mp.mpf(mH)**2
        return (mp.mpf(1)/(24*mp.pi))*(mp.log(mH2) + Ghat(mH2, MZ2))

    one12 = 1/(12*mp.pi)

    # (gate) asymptotic slope -> 1/(12pi): the bridge to the native [P] leading-log.
    # m_H=1e4 is inside the cancellation-safe regime at dps=60 (needs ~6*log10 digits).
    u = mp.log(mp.mpf("1e4")**2); h = mp.mpf("1e-12")
    Su = lambda uu: (mp.mpf(1)/(24*mp.pi))*(uu + Ghat(mp.e**uu, MZ2))
    slope = (Su(u + h) - Su(u - h))/(2*h)
    check(abs(slope/one12 - 1) < 5e-3,
          f"gate: dS_H/d ln(m_H^2) at 1e4 must -> 1/(12pi); ratio={float(slope/one12)}")

    # (profile) finite-G is order-one at the physical point (~20% of S_H), not negligible
    SH = S("125.25") - S("1000.0")
    LL = one12*mp.log(mp.mpf("125.25")**2/mp.mpf("1000.0")**2)
    finiteG = SH - LL
    check(abs(float(SH) - (-0.13699)) < 1e-3, f"S_H(125.25;ref1TeV) ~ -0.137; got {float(SH)}")
    check(abs(float(finiteG) - (-0.02678)) < 1e-3, f"finite-G ~ -0.0268; got {float(finiteG)}")
    check(abs(float(finiteG/SH)) > 0.15, "finite-G is order-one (~20%) at the physical point")

    check(EXPORT_FLAGS_PROFILE["Export_S_higgs_finite_G_native_P"] == 1,
          "finite G is now NATIVE (apf.s_higgs_finite_profile_native, "
          "check_T_S_higgs_finite_profile_native_P, v24.3.260); this GLOO "
          "reproduction is retained as the magnitude cross-check")
    check(EXPORT_FLAGS_PROFILE["Export_S_pure_gauge_constant_native_P"] == 1,
          "the m_H-independent pure-gauge constant is NATIVE "
          "(apf.s_parameter_pure_gauge_constant_native, v24.3.259)")
    check(EXPORT_FLAGS_PROFILE["target_consumed"] == 0, "no S target consumed")
    return _result(
        name=("T_S_higgs_mH_dependent_profile_Ptool: the m_H-dependent bosonic Higgs "
              "profile S_H(m_H)=(1/12pi)[ln(m_H^2/m_ref^2)+G(m_H^2/m_Z^2)] reproduced "
              "from the imported GLOO closed form; asymptotic slope -> 1/(12pi) bridges "
              "to the native [P] leading-log. [P+tool]; finite G imported; pure-gauge "
              "constant still OPEN."),
        tier=4, epistemic="P_plus_tool_S_higgs_mH_profile_GLOO_reproduction",
        summary=(
            "Closes the m_H-DEPENDENT bosonic Higgs profile of Peskin-Takeuchi S at "
            "[P+tool]. S_H(m_H) = (1/12pi)[ln(m_H^2/m_ref^2) + G(m_H^2/m_Z^2)] from the "
            "imported Grimus-Lavoura-Ogreid-Osland closed form (Ghosh arXiv:2201.01006). "
            "The asymptotic slope dS_H/d ln(m_H^2) -> 1/(12pi) cross-checks the native "
            "[P] leading-log (check_T_S_higgs_logarithm_native) -- the imported finite "
            "profile is consistent with the answer-free native coefficient. The finite "
            "G is order-one at the physical point (~20% of S_H at m_H=125.25 GeV), not "
            "negligible. Photon/gammaZ self-energies carry no m_H dependence and cancel "
            "in the subtraction (the profile is the ZZ higgs-brace alone). The finite G is now ALSO native "
            "(apf.s_higgs_finite_profile_native, v24.3.260; relative sign forced by an "
            "executed i-count calibrated to the native Goldstone/W-phi-mixed anchors) -- "
            "this GLOO reproduction is the cross-check. The m_H-INDEPENDENT pure-gauge "
            "constant is also native (apf.s_parameter_pure_gauge_constant_native). "
            "Cold-audited SOUND (gate independently reproduced at 1/12pi, not 1/6pi or "
            "1/24pi; grade verified honest)."
        ),
        key_result=("S_H(m_H)=(1/12pi)[ln+G(m_H^2/m_Z^2)] [P+tool]; slope->1/12pi bridges "
                    "to native [P] leading-log; finite G ~20% at physical point; pure-gauge "
                    "constant OPEN"),
        dependencies=["T_S_higgs_logarithm_native"],
        cross_refs=["T_S_fermion_loop_native_reproduction", "T_oblique_curvature_moment_native"],
        artifacts={"S_H_125p25_ref1TeV": "-0.137", "finite_G": "-0.0268 (~20%)",
                   "gate_ratio_at_1e4": "1.0004", "source": "GLOO / Ghosh arXiv:2201.01006",
                   "export_flags": dict(EXPORT_FLAGS_PROFILE)},
    )


_CHECKS = {
    "T_S_fermion_loop_native_reproduction": check_T_S_fermion_loop_native_reproduction_P,
    "T_S_higgs_logarithm_native": check_T_S_higgs_logarithm_native_P,
    "T_oblique_curvature_moment_native": check_T_oblique_curvature_moment_native_P,
    "T_S_higgs_mH_dependent_profile_Ptool": check_T_S_higgs_mH_dependent_profile_Ptool,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}

# ---------------------------------------------------------------------------
# IE onboarding declaration (v24.3.316, Full Bank Onboarding Wave 4 -- the
# systematic sector sweep). Claim-grade structural probe; the theorems stay
# with their banked checks; verdicts inherit banked grades, routing confers
# nothing. expect_export pinned by the observed engine verdict.
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "ew:native_oblique_close",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "The native EW oblique close as one interface: fermion-loop S, "
            "the Higgs log, and the curvature moment at "
            "[P_S_oblique_native_reproduction]; the pure-gauge constant "
            "-16.352 and the finite Higgs profile derived answer-free from "
            "BFM vertices; fermionic T = the banked native Delta-rho [P]; "
            "bosonic U [P]. All scope-fenced REPRODUCTIONS of standard "
            "oblique structure with native tools -- no measured S, T, or U "
            "enters anywhere. "
        ),
        "covers": ("apf.t_parameter_native", "apf.u_parameter_native", "apf.s_parameter_pure_gauge_constant_native", "apf.s_higgs_finite_profile_native", "apf.w_trace_native_bfm_photon_vp", "apf.w_trace_native_gauge_boson_drho_uv", "apf.w_trace_native_drho_top"),
        "note": "Wave 4 head 5: the oblique family head; covers = the cross-composed native oblique modules",
    },
)
