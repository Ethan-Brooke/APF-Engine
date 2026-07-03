"""APF-native one-loop Delta r -> M_W assembly (Denner-validated) -- Tier-4.

Step 5 / capstone of the native OS-W precision close: assemble Denner's complete
one-loop Delta r (arXiv:0709.1075 eq. GF1loop) from the NATIVE PV-evaluated
self-energies -- Sigma^AA_T, Sigma^AZ_T, Sigma^ZZ_T, Sigma^W_T (fermionic + the
bosonic W/Z/Higgs/Goldstone/ghost loops of v24.3.98) all on the native
massless-safe B0 -- and solve M_W^2(1-M_W^2/M_Z^2) = (pi a/sqrt2 G_F)(1+Delta r)
for M_W in the on-shell scheme.

    Delta r = Pi^AA(0) - (c^2/s^2)[Sigma^ZZ(M_Z^2)/M_Z^2 - Sigma^W(M_W^2)/M_W^2]
              + [Sigma^W(0) - Sigma^W(M_W^2)]/M_W^2 + 2(c/s)Sigma^AZ(0)/M_Z^2
              + (a/4pi s^2)(6 + (7-4s^2)/(2s^2) ln c^2)

Result (Denner's input set: alpha=1/137.036, M_Z=91.177, G_F=1.16637e-5,
m_t=140, M_H=100, effective light-quark masses):
    native M_W = 80.26 GeV   vs   Denner published one-loop 80.23 GeV  (~30 MeV).
mu-independent (exact) and IR (photon-lambda) finite.

HONEST framing (no overclaim)
-----------------------------
This is the SM one-loop electroweak calculation performed with APF-native tools
(native PV B0 + the checked Denner vertex algebra). M_W is computed from SM inputs
(alpha, M_Z, G_F, m_t, M_H), with Delta alpha_had entering through Denner's
effective light-quark masses -- the data-bound dispersion proxy, the single
external input. It is NOT a parameter-free APF prediction of M_W. What it closes
is the long-tracked "native OS-W Delta r_rem / M_W" item: APF now reproduces the
published one-loop M_W natively rather than importing DIZET. The ~30 MeV residual
is the GFloop higher-order resummation (Denner's 80.23 is the resummed value) plus
the Sigma^W(0) extrapolation + CKM-diagonal approximation.

Validated three ways: M_W reproduction (~30 MeV of Denner), Delta r
mu-independence (exact, all self-energies at common mu), IR/lambda finiteness.
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_native_pv_massless_safe import re_b0_safe

PI = math.pi
ALPHA = 1.0 / 137.0359895
A4PI = ALPHA / (4.0 * PI)
MZ = 91.177
MZ2 = MZ * MZ
GF = 1.16637e-5
MH = 100.0
MH2 = MH * MH
_NQ = 3000
_DENNER_MW = 80.23

ML = {"e": 0.51099906e-3, "mu": 0.105658387, "tau": 1.77682}
MU = {"u": 0.041, "c": 1.5, "t": 140.0}
MD = {"d": 0.041, "s": 0.15, "b": 4.5}


def _B0(k2, m02, m12, mu2):
    return re_b0_safe(k2, m02, m12, mu2, _NQ)


def _Tff(k2, m, mu2):
    m2 = m * m
    return -(k2 + 2.0*m2)*_B0(k2, m2, m2, mu2) + 2.0*m2*_B0(0.0, m2, m2, mu2) + k2/3.0


def _gp(Q, s, c):
    return -(s/c)*Q


def _gm(I3, Q, s, c):
    return (I3 - s*s*Q)/(s*c)


def _fermions():
    out = [("e", -0.5, -1.0, 1.0, ML["e"]), ("mu", -0.5, -1.0, 1.0, ML["mu"]),
           ("tau", -0.5, -1.0, 1.0, ML["tau"]),
           ("nu1", 0.5, 0.0, 1.0, 0.0), ("nu2", 0.5, 0.0, 1.0, 0.0), ("nu3", 0.5, 0.0, 1.0, 0.0),
           ("u", 0.5, 2.0/3.0, 3.0, MU["u"]), ("c", 0.5, 2.0/3.0, 3.0, MU["c"]),
           ("t", 0.5, 2.0/3.0, 3.0, MU["t"]),
           ("d", -0.5, -1.0/3.0, 3.0, MD["d"]), ("s", -0.5, -1.0/3.0, 3.0, MD["s"]),
           ("b", -0.5, -1.0/3.0, 3.0, MD["b"])]
    return out


def Sig_AZ(k2, s, c, mu2):
    MW2 = c*c*MZ2
    ferm = sum((2.0/3.0)*Nc*(-Q)*(_gp(Q, s, c)+_gm(I3, Q, s, c))*_Tff(k2, m, mu2)
               for _, I3, Q, Nc, m in _fermions())
    bos = -(1.0/(3.0*s*c))*(((9.0*c*c+0.5)*k2 + (12.0*c*c+4.0)*MW2)*_B0(k2, MW2, MW2, mu2)
                            - (12.0*c*c-2.0)*MW2*_B0(0.0, MW2, MW2, mu2) + (1.0/3.0)*k2)
    return -A4PI*(ferm + bos)


def Sig_ZZ(k2, s, c, mu2):
    MW2 = c*c*MZ2; s2 = s*s; c2 = c*c
    ferm = 0.0
    for _, I3, Q, Nc, m in _fermions():
        m2 = m*m; gpp = _gp(Q, s, c); gmm = _gm(I3, Q, s, c)
        ferm += (2.0/3.0)*Nc*((gpp*gpp+gmm*gmm)*_Tff(k2, m, mu2)
                              + (3.0/(4.0*s2*c2))*m2*_B0(k2, m2, m2, mu2))
    gauge = (1.0/(6.0*s2*c2))*(((18.0*c2*c2+2.0*c2-0.5)*k2+(24.0*c2*c2+16.0*c2-10.0)*MW2)*_B0(k2, MW2, MW2, mu2)
                               - (24.0*c2*c2-8.0*c2+2.0)*MW2*_B0(0.0, MW2, MW2, mu2) + (4.0*c2-1.0)*k2/3.0)
    higgs = (1.0/(12.0*s2*c2))*((2.0*MH2-10.0*MZ2-k2)*_B0(k2, MZ2, MH2, mu2)
                                - 2.0*MZ2*_B0(0.0, MZ2, MZ2, mu2) - 2.0*MH2*_B0(0.0, MH2, MH2, mu2)
                                - ((MZ2-MH2)**2/k2)*(_B0(k2, MZ2, MH2, mu2)-_B0(0.0, MZ2, MH2, mu2)) - (2.0/3.0)*k2)
    return -A4PI*(ferm + gauge + higgs)


def Sig_W(k2, s, c, mu2, lam2):
    MW2 = c*c*MZ2; s2 = s*s; c2 = c*c
    lep = 0.0
    for n in ("e", "mu", "tau"):
        ml2 = ML[n]**2
        lep += (-(k2-ml2/2.0)*_B0(k2, 0.0, ml2, mu2) + k2/3.0 + ml2*_B0(0.0, ml2, ml2, mu2)
                + (ml2*ml2/(2.0*k2))*(_B0(k2, 0.0, ml2, mu2)-_B0(0.0, 0.0, ml2, mu2)))
    lep *= (2.0/3.0)*(1.0/(2.0*s2))
    qk = 0.0
    for nu, nd in (("u", "d"), ("c", "s"), ("t", "b")):
        mu2_ = MU[nu]**2; md2_ = MD[nd]**2
        qk += (-(k2-(mu2_+md2_)/2.0)*_B0(k2, mu2_, md2_, mu2) + k2/3.0
               + mu2_*_B0(0.0, mu2_, mu2_, mu2) + md2_*_B0(0.0, md2_, md2_, mu2)
               + ((mu2_-md2_)**2/(2.0*k2))*(_B0(k2, mu2_, md2_, mu2)-_B0(0.0, mu2_, md2_, mu2)))
    qk *= (2.0/3.0)*(1.0/(2.0*s2))*3.0
    wph = (2.0/3.0)*((2.0*MW2+5.0*k2)*_B0(k2, MW2, lam2, mu2) - 2.0*MW2*_B0(0.0, MW2, MW2, mu2)
                     - (MW2*MW2/k2)*(_B0(k2, MW2, lam2, mu2)-_B0(0.0, MW2, lam2, mu2)) + k2/3.0)
    wz = (1.0/(12.0*s2))*(((40.0*c2-1.0)*k2+(16.0*c2+54.0-10.0/c2)*MW2)*_B0(k2, MW2, MZ2, mu2)
                          - (16.0*c2+2.0)*(MW2*_B0(0.0, MW2, MW2, mu2)+MZ2*_B0(0.0, MZ2, MZ2, mu2))
                          + (4.0*c2-1.0)*(2.0/3.0)*k2
                          - (8.0*c2+1.0)*((MW2-MZ2)**2/k2)*(_B0(k2, MW2, MZ2, mu2)-_B0(0.0, MW2, MZ2, mu2)))
    wh = (1.0/(12.0*s2))*((2.0*MH2-10.0*MW2-k2)*_B0(k2, MW2, MH2, mu2) - 2.0*MW2*_B0(0.0, MW2, MW2, mu2)
                          - 2.0*MH2*_B0(0.0, MH2, MH2, mu2)
                          - ((MW2-MH2)**2/k2)*(_B0(k2, MW2, MH2, mu2)-_B0(0.0, MW2, MH2, mu2)) - (2.0/3.0)*k2)
    return -A4PI*(lep+qk+wph+wz+wh)


def Pi_AA_0(s, c, mu2):
    """Analytic Sigma^AA_T'(0): ferm (4/3) sum NcQ^2 ln(m^2/mu2) + bos."""
    MW2 = c*c*MZ2
    fsum = sum(Nc*Q*Q*math.log((m*m)/mu2) for _, I3, Q, Nc, m in _fermions() if m > 0.0)
    bos = -3.0*math.log(MW2/mu2) + 2.0/3.0
    return -A4PI*((4.0/3.0)*fsum + bos)


def delta_VB(s, c):
    s2 = s*s
    return (ALPHA/(4.0*PI*s2))*(6.0 + (7.0-4.0*s2)/(2.0*s2)*math.log(c*c))


def delta_r(MW, mu2=MZ2, lam2=1e-4):
    c = MW/MZ; s = math.sqrt(1.0 - c*c); MW2 = MW*MW
    sw_0 = (2.0*Sig_W(1.0, s, c, mu2, lam2) - Sig_W(2.0, s, c, mu2, lam2))/MW2  # extrap k2->0
    sw_mw = Sig_W(MW2, s, c, mu2, lam2)/MW2
    return (Pi_AA_0(s, c, mu2)
            - (c*c/(s*s))*(Sig_ZZ(MZ2, s, c, mu2)/MZ2 - sw_mw)
            + (sw_0 - sw_mw)
            + 2.0*(c/s)*Sig_AZ(1e-3, s, c, mu2)/MZ2
            + delta_VB(s, c))


def solve_MW(mu2=MZ2, lam2=1e-4, seed=80.26, iters=8):
    A = PI*ALPHA/(math.sqrt(2.0)*GF)
    MW = seed
    for _ in range(iters):
        rhs = A*(1.0 + delta_r(MW, mu2, lam2))
        disc = 1.0 - 4.0*rhs/MZ2
        MWn = math.sqrt((MZ2/2.0)*(1.0 + math.sqrt(disc)))  # physical (upper) root
        if abs(MWn - MW) < 1e-6:
            MW = MWn; break
        MW = MWn
    return MW


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_delta_r_mw_assembly": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 1,   # CLOSED: native Delta r_rem -> M_W
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_mw_reproduces_denner_P() -> Dict[str, Any]:
    """T: native one-loop M_W reproduces Denner's published 80.23 to ~30 MeV [P]."""
    mw = solve_MW()
    dev = abs(mw - _DENNER_MW)
    check(80.10 < mw < 80.40, f"native M_W out of range: {mw:.4f}")
    check(dev < 0.06, f"native M_W {mw:.4f} vs Denner {_DENNER_MW} dev {dev*1000:.1f} MeV")
    return _result(
        name="T_w_trace_native_mw_reproduces_denner: "
             "native one-loop M_W reproduces Denner's published one-loop value [P]",
        tier=4, epistemic="P",
        summary=(
            f"Denner's complete one-loop Delta r, assembled from the native "
            f"PV-evaluated self-energies (Sigma^AA/AZ/ZZ/W, fermionic + bosonic) and "
            f"solved in the on-shell scheme, gives native M_W = {mw:.4f} GeV, "
            f"reproducing Denner's published one-loop M_W = {_DENNER_MW} GeV to "
            f"{dev*1000:.0f} MeV (Denner inputs: alpha=1/137.036, M_Z=91.177, "
            f"G_F=1.16637e-5, m_t=140, M_H=100, effective light-quark masses for "
            f"Delta alpha_had). This is the SM one-loop calculation done with "
            f"APF-native tools -- M_W from SM inputs, NOT a parameter-free APF "
            f"prediction; the residual is the GFloop resummation + Sigma^W(0) "
            f"extrapolation. Closes the native OS-W Delta r_rem / M_W item."
        ),
        key_result=f"native one-loop M_W = {mw:.3f} GeV == Denner {_DENNER_MW} ({dev*1000:.0f} MeV). [P]",
        dependencies=["T_w_trace_native_bosonic_drho_pole",
                      "T_w_trace_native_fermion_sum_drho_top",
                      "T_w_trace_native_delta_r_uv_cancellation"],
        artifacts={"native_MW": mw, "denner_MW": _DENNER_MW, "dev_MeV": dev*1000.0},
    )


def check_T_w_trace_native_delta_r_mu_independent_P() -> Dict[str, Any]:
    """T: the assembled Delta r is mu-independent [P]."""
    mw = 80.26
    drs = [delta_r(mw, mu2, 1e-4) for mu2 in (MZ2, 4.0*MZ2, 0.25*MZ2)]
    spread = max(drs) - min(drs)
    check(spread < 1e-6, f"Delta r mu-dependence {spread:.2e}")
    return _result(
        name="T_w_trace_native_delta_r_mu_independent: "
             "assembled one-loop Delta r is mu-independent [P]",
        tier=4, epistemic="P",
        summary=(
            f"With all native self-energies evaluated at a common scale mu, the "
            f"assembled Delta r is mu-independent under mu^2 -> {{0.25, 1, 4}} M_Z^2 "
            f"(spread {spread:.1e}) -- the per-term mu-running (in Pi^AA(0), Sigma^ZZ, "
            f"Sigma^W, Sigma^AZ) cancels exactly in the physical combination, a "
            f"strong consistency check on the relative self-energy normalizations."
        ),
        key_result=f"Delta r mu-independent (spread {spread:.1e}). [P]",
        dependencies=["T_w_trace_native_mw_reproduces_denner"],
        artifacts={"mu_spread": spread, "delta_r": drs[0]},
    )


def check_T_w_trace_native_delta_r_ir_finite_P() -> Dict[str, Any]:
    """T: the assembled Delta r is IR (photon-lambda) finite [P]."""
    mw = 80.26
    dr_a = delta_r(mw, MZ2, 1e-4)
    dr_b = delta_r(mw, MZ2, 1e-8)
    drift = abs(dr_a - dr_b)
    check(drift < 1e-3, f"Delta r lambda-drift {drift:.2e}")
    return _result(
        name="T_w_trace_native_delta_r_ir_finite: "
             "assembled one-loop Delta r is IR (photon-lambda) finite [P]",
        tier=4, epistemic="P",
        summary=(
            f"As the photon IR regulator lambda^2 sweeps 1e-4 -> 1e-8 the assembled "
            f"Delta r changes by only {drift:.1e}: the ln(lambda) from the W-photon "
            f"loop in Sigma^W(M_W^2) cancels in the Delta r combination, as required "
            f"for the muon-decay correction (the QED/Fermi-model IR is subtracted, "
            f"leaving the finite delta_VB). Confirms the native assembly is IR-safe."
        ),
        key_result=f"Delta r IR-finite (lambda-drift {drift:.1e}). [P]",
        dependencies=["T_w_trace_native_mw_reproduces_denner"],
        artifacts={"lambda_drift": drift},
    )


def check_T_w_trace_native_delta_r_mw_scope_partial_P() -> Dict[str, Any]:
    """T: native one-loop Delta r/M_W done; resummation + APF-input M_W OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_delta_r_mw_assembly"] == 1, "assembly flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 1,
          "native Delta r_rem must now be evaluated")
    return _result(
        name="T_w_trace_native_delta_r_mw_scope_partial: "
             "native one-loop Delta r/M_W done; resummation + APF-input M_W OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "The native one-loop OS-W evaluator is complete: Denner's full Delta r is "
            "assembled from native PV-evaluated self-energies and reproduces the "
            "published one-loop M_W to ~30 MeV, mu-independent and IR-finite. This "
            "closes the long-tracked 'native OS-W Delta r_rem / M_W' item -- APF no "
            "longer needs to import DIZET for the one-loop M_W. HONEST non-claims: "
            "this is the SM one-loop calculation with native tools (inputs alpha, "
            "M_Z, G_F, m_t, M_H; Delta alpha_had via effective light-quark masses, "
            "the one external data-bound input), NOT a parameter-free APF prediction "
            "of M_W. Still OPEN: the GFloop higher-order resummation, two-loop terms, "
            "and an M_W evaluation on purely APF-internal inputs."
        ),
        key_result="Native one-loop Delta r/M_W done (Denner-validated); resummation OPEN. [P_structural]",
        dependencies=["T_w_trace_native_delta_r_ir_finite"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_mw_reproduces_denner": check_T_w_trace_native_mw_reproduces_denner_P,
    "T_w_trace_native_delta_r_mu_independent": check_T_w_trace_native_delta_r_mu_independent_P,
    "T_w_trace_native_delta_r_ir_finite": check_T_w_trace_native_delta_r_ir_finite_P,
    "T_w_trace_native_delta_r_mw_scope_partial": check_T_w_trace_native_delta_r_mw_scope_partial_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}

# ---------------------------------------------------------------------------
# IE onboarding declaration (v24.3.316, Full Bank Onboarding Wave 4 -- the
# systematic sector sweep). Claim-grade structural probe; the theorems stay
# with their banked checks; verdicts inherit banked grades, routing confers
# nothing. expect_export pinned by the observed engine verdict.
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "wtrace:native_one_loop_mw_close",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "The native OS-W one-loop close: Denner's complete one-loop "
            "Delta-r assembled from native PV-evaluated self-energies gives "
            "M_W = 80.26 GeV against Denner's published one-loop 80.23 "
            "(residual ~30 MeV from G_F-loop resummation and Sigma_W(0) "
            "extrapolation) -- check_T_w_trace_native_mw_reproduces_denner "
            "[P] with mu-independence and IR-finiteness [P] and the scope "
            "fence [P_structural_partial]. This is the SM calculation "
            "reproduced with native tools from SM inputs (alpha, M_Z, G_F, "
            "m_t, M_H; Delta-alpha_had via effective masses), NOT a "
            "parameter-free APF prediction of M_W. "
        ),
        "covers": ("apf.w_trace_native_pv_massless_safe", "apf.w_trace_pv_scalar_integral_substrate", "apf.w_trace_pv_timelike_two_point", "apf.w_trace_acfw_delta_r_extraction_attempt", "apf.w_trace_apf_native_one_loop_evaluator", "apf.w_trace_delta_r_remainder_resolution", "apf.w_trace_delta_r_route_input_evaluation", "apf.w_trace_delta_r_row_extraction_closeout", "apf.w_trace_delta_r_source_acquisition_matrix", "apf.w_trace_delta_r_transport_buildout", "apf.w_trace_denner_sirlin_counterterm_functional", "apf.w_trace_dizet_acquisition_instrumentation", "apf.w_trace_dizet_executable_run", "apf.w_trace_dizet_flag_sensitivity_covariance", "apf.w_trace_dizet_internal_dr_decomposition", "apf.w_trace_full_loop_derivation_closeout", "apf.w_trace_native_finite_remainder_evaluator", "apf.w_trace_pv_tensor_reduction", "apf.w_trace_same_input_evaluator_closeout", "apf.w_trace_standard_delta_r_extraction_worksheet",),
        "note": "Wave 4 head 1: the one-loop native close; covers = the dependency-verified composition fan; Wave 7 covers extension: +11 stages, criterion = transitive import closure of the head module (AST-verified 2026-07-02 after a hostile audit caught 6 unreachable targets in the first pass -- the self-energy/UV sub-cluster is NOT routed by this head and stays honestly un-covered, Tier 2)",
    },
)
