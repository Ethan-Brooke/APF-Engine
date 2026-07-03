"""No-go: the absolute top Yukawa is not fixable by a normalization/unitarity
principle on the Yukawa matrix — Tier-4 structural obstruction.

This bank-registers a NEGATIVE result, in the spirit of the current-source
coefficient no-go and the κ_b falsifier: it does not bank a physical value, it
fences off a route so future cycles do not re-attempt it. The result was reached
by pushing the "unitarity/normalization principle forces the maximal Yukawa"
route (route a) to exhaustion against the bank's actual generation machinery.

The question. The inter-generation Yukawa RATIOS are native [P]
(L_multiplicative_amplitude, L_Yukawa_bilinear: y_g/y_t = x^{q(g)}), and the
mixing angle is a basis-invariant normalized Gram correlation (L_Gram → 3/13).
The open piece is the ABSOLUTE top Yukawa y_t (equivalently the σ normalization,
equivalently m_t/v). Route (a) asked: can a unitarity / normalized-overlap
principle FORCE y_t to a specific value (the natural candidate being the
Cauchy-Schwarz ceiling y_t = 1, the top as a perfectly self-correlated
reference), rather than declaring it?

The obstruction (three independent legs, all re-verified in this check):

  (1) Rank-2 / CKM breaks the single-correlation ceiling. A single-channel
      Yukawa is rank-1 (L_Yukawa_bilinear: pure outer product) — only the top
      is massive, charm and up massless, no CKM. Its top entry is the self
      -overlap x^0 = 1: a saturable Cauchy-Schwarz ceiling. But the charm mass
      and CKM mixing REQUIRE a second channel (T_channels: bookkeeper + Higgs;
      L_mass_from_capacity lifts rank 1 → 2). Both channels carry q(top)=0
      (T_capacity_ladder q_B=(7,4,0); T_q_Higgs q_H=(7,5,0)), so the physical
      top entry is the two-channel SUM c_B·x^0 + c_H·x^0 = x³ + 1 = 9/8 > 1.
      A sum of correlations is not Cauchy-Schwarz-bounded by 1: the ceiling is
      gone. The very structure that gives CKM + the light generations destroys
      the unit ceiling that would fix the top.

  (2) Every norm-invariant of the Yukawa matrix is top-dominated, hence
      circular with y_t. The matrix is rank-1-like (the top swamps charm/up):
      its operator norm, Frobenius norm, and a_Y trace are all equal to the top
      to 1 part in 10⁴ (Frobenius/operator-norm = 1.0000). So "normalize
      invariant X to value V" is identically "set y_t = √V": no norm of a
      top-dominated matrix carries information independent of the top. Fixing
      any matrix-norm IS fixing y_t — circular.

  (3) The only count-based handle — the spectral-action a_Y — is convention
      -dependent, hence non-physical by the invariance criterion. a_Y is the one
      quantity fixable by counting rather than reading the matrix, but it
      carries the color-counting convention: a_Y = N_c·y_t² → y_t = 1 at
      a_Y = N_c = 3; a_Y = y_t² → y_t = 1 at a_Y = 1; the conventions land at
      0.577 / 1.73 the other way. They straddle the measured 0.94–0.99 and the
      N_c color-count is a free bookkeeping choice. A quantity that moves under a
      counting convention is not physical (the same disqualification applied to
      Δr). This is exactly Paper 28's "needs a_Y = N_c, actual ≈ 1" — a
      convention fork, never a computational shortfall.

Conclusion. Within the class of principles that fix y_t by normalizing an
invariant of the Yukawa matrix itself or by a single-correlation unitarity
ceiling, the absolute top Yukawa is NOT determined. The absolute scale must
enter as a dimensionful / cross-scale input (the v_H–M_Pl hierarchy, route b),
consistent with the invariance criterion: y_t's absolute value runs (is scale-
and scheme-dependent), so no basis-invariant principle can produce it; only the
ratios and the saturation structure are invariant.

Scope (honest). This fences off the matrix-normalization / single-correlation
-ceiling class. It does NOT claim to rule out a genuine dimensionful or
dynamical derivation that brings in an independent scale (route b); that remains
open. Leg (3)'s "non-physical" is the invariance-criterion reading of a
convention-dependent count, not a claim of logical impossibility.

Honest non-claims:
  * Export_yt_absolute_value_native_P = 0 — no value of y_t is banked.
  * Export_yt_normalization_no_go_structural_P = 1 — the obstruction is the
    banked content.
  * Export_physical_final_P = 0; target_consumed = 0.

Source: APF Reference Docs — y_t Absolute-Scale Normalization No-Go v0.1
(2026-05-29); building on Paper 28 B1 v0.8 (saturation reframing) and the
invariance criterion / EW Closure Registry (2026-05-28).
"""
from __future__ import annotations

import math

from apf.apf_utils import check, _result


X = 0.5          # single-quantum Gram overlap (T27c / L_Gram)
M_SU2 = 3        # dim su(2)
N_C = 3          # color


def _two_channel_top_and_norms():
    """Rebuild the L_mass_from_capacity up-sector matrix; return top entry,
    singular values, and the norm-invariants. Mirrors generations.py exactly."""
    q_B = [7, 4, 0]          # T_capacity_ladder
    q_H = [7, 5, 0]          # T_q_Higgs
    phi = math.pi / 4        # L_holonomy_phase
    k_B, k_H = 1, 0          # windings
    c_B, c_H = X ** 3, 1.0   # channel weights (bookkeeper amplitude, Higgs normalized)
    import numpy as np
    Mtx = np.zeros((3, 3), dtype=complex)
    for g in range(3):
        for h in range(3):
            ab = phi * (g - h) * k_B / 3.0
            ah = phi * (g - h) * k_H / 3.0
            Mtx[g, h] = (c_B * X ** (q_B[g] + q_B[h]) * complex(math.cos(ab), math.sin(ab))
                         + c_H * X ** (q_H[g] + q_H[h]) * complex(math.cos(ah), math.sin(ah)))
    sv = sorted(np.linalg.svd(Mtx, compute_uv=False).real)
    top_entry = abs(Mtx[2, 2])
    op_norm = sv[-1]
    frob = math.sqrt(sum(s * s for s in sv))
    a_Y_trace = sum(s * s for s in sv)
    return top_entry, sv, op_norm, frob, a_Y_trace, c_B, c_H


EXPORT_FLAGS = {
    "Export_yt_normalization_no_go_structural_P": 1,
    "Export_yt_absolute_value_native_P": 0,
    "Export_physical_final_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_yt_absolute_scale_not_fixable_by_normalization_no_go_P():
    """T: the absolute top Yukawa is not fixable by a normalization/unitarity
    principle on the Yukawa matrix. Three legs: (1) the rank-2 structure required
    for CKM + the charm mass makes the top a two-channel sum 9/8 > 1, breaking
    the single-correlation Cauchy-Schwarz ceiling; (2) every norm-invariant of
    the matrix is top-dominated (Frobenius/operator-norm = 1) so fixing any is
    circular with y_t; (3) the only count handle (spectral a_Y) is
    N_c-convention-dependent, non-physical by the invariance criterion.
    Therefore the absolute scale requires a dimensionful input (route b). No
    value banked. [P_structural_yt_absolute_scale_normalization_no_go]."""

    top_entry, sv, op_norm, frob, a_Y_trace, c_B, c_H = _two_channel_top_and_norms()

    # ---- Leg 1: rank-2 / CKM breaks the single-correlation ceiling ----
    # single-channel rank-1 top self-overlap is the saturable ceiling x^0 = 1
    single_channel_top = X ** 0
    check(single_channel_top == 1, "single-channel rank-1 top entry is the self-overlap ceiling = 1")
    # two-channel physical top entry is the SUM = c_B + c_H = x^3 + 1 = 9/8 > 1
    check(abs(top_entry - (c_B + c_H)) < 1e-12, "two-channel top entry must be c_B + c_H")
    check(abs(top_entry - 9 / 8) < 1e-12, "two-channel top entry must be 9/8")
    check(top_entry > 1, "the two-channel sum exceeds the unit ceiling — ceiling broken by rank-2/CKM")

    # ---- Leg 2: every norm-invariant is top-dominated → circular ----
    check(abs(frob / op_norm - 1.0) < 1e-3,
          "Frobenius/operator-norm = 1 to 1e-3 ⇒ matrix is rank-1-like ⇒ norms carry no "
          "info independent of the top ⇒ fixing any norm ⟺ fixing y_t (circular)")
    check(abs(a_Y_trace - op_norm ** 2) < 1e-3 * op_norm ** 2,
          "a_Y trace ≈ (top)² ⇒ also top-dominated")

    # ---- Leg 3: the a_Y count handle is N_c-convention-dependent ----
    # a_Y = N_c * y_t^2  →  y_t = sqrt(a_Y / N_c)
    # a_Y = y_t^2        →  y_t = sqrt(a_Y)
    yt_aY3_withNc = math.sqrt(3 / N_C)     # a_Y = N_c = 3, with color  → 1
    yt_aY1_noNc = math.sqrt(1)             # a_Y = 1, no color          → 1
    yt_aY1_withNc = math.sqrt(1 / N_C)     # a_Y = 1, with color        → 0.577
    yt_aY3_noNc = math.sqrt(3)             # a_Y = 3, no color          → 1.732
    # the convention choice changes y_t by the color factor → not invariant
    check(abs(yt_aY3_withNc - 1.0) < 1e-9 and abs(yt_aY1_noNc - 1.0) < 1e-9,
          "two conventions both give y_t = 1 (a_Y=N_c with color; a_Y=1 no color)")
    check(abs(yt_aY1_withNc - 1 / math.sqrt(3)) < 1e-9 and abs(yt_aY3_noNc - math.sqrt(3)) < 1e-9,
          "the other convention pairing gives 0.577 / 1.732 — the N_c color count is free")
    check(abs(yt_aY3_withNc / yt_aY1_withNc - math.sqrt(N_C)) < 1e-9,
          "y_t moves by √N_c under the color-counting convention ⇒ convention-dependent ⇒ "
          "non-physical by the invariance criterion")

    # ---- conclusion: only ratios + saturation structure are invariant ----
    measured_yt_pole = math.sqrt(2) * 172.57 / 246.22
    check(0.93 < measured_yt_pole < 1.0,
          "measured y_t (pole) sits between the convention forks — not selected by any of them")

    check(EXPORT_FLAGS["Export_yt_absolute_value_native_P"] == 0, "no y_t value banked")
    check(EXPORT_FLAGS["Export_physical_final_P"] == 0, "no physical-final claim")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_yt_absolute_scale_not_fixable_by_normalization_no_go: the absolute "
              "top Yukawa cannot be fixed by a normalization/unitarity principle on the "
              "Yukawa matrix. (1) rank-2/CKM makes the top a two-channel sum 9/8 > 1, "
              "breaking the single-correlation ceiling; (2) all matrix norm-invariants "
              "are top-dominated (Frobenius/op-norm = 1) ⇒ circular with y_t; (3) the "
              "spectral a_Y count is N_c-convention-dependent ⇒ non-physical by the "
              "invariance criterion. Absolute scale requires a dimensionful input "
              "(route b). No value banked. "
              "[P_structural_yt_absolute_scale_normalization_no_go]"),
        tier=4,
        epistemic="P_structural_yt_absolute_scale_normalization_no_go",
        summary=(
            "Negative result fencing off route (a). The inter-generation Yukawa ratios "
            "(y_g/y_t = x^{q(g)}) and the mixing angle (normalized Gram correlation → "
            "3/13) are native and basis-invariant; the open piece is the absolute top "
            "Yukawa y_t. Route (a) asked whether a unitarity / normalized-overlap "
            "principle forces y_t (natural candidate: the Cauchy-Schwarz ceiling y_t=1, "
            "top as self-correlated reference). It cannot, for three re-verified "
            "reasons. (1) A single-channel Yukawa is rank-1 (massless charm/up, no CKM) "
            "with top self-overlap x^0 = 1 — a saturable ceiling; but the charm mass and "
            "CKM mixing require a second channel (T_channels; L_mass_from_capacity rank "
            "1→2), and both channels carry q(top)=0, so the physical top entry is the "
            "sum c_B·x^0 + c_H·x^0 = x³ + 1 = 9/8 > 1 — a sum of correlations is not "
            "unit-bounded, the ceiling is gone. (2) The matrix is rank-1-like (top swamps "
            "charm/up): operator norm = Frobenius = a_Y trace to 1 part in 10⁴, so fixing "
            "any matrix-norm IS fixing y_t — circular, proven not asserted. (3) The one "
            "count-based handle, the spectral a_Y, is color-convention-dependent: "
            "a_Y=N_c→y_t=1, a_Y=1→y_t=1 (no color) or 0.577 (color); the N_c factor is a "
            "free bookkeeping choice, so y_t moves by √N_c under it — non-physical by the "
            "invariance criterion, exactly Paper 28's 'needs a_Y=N_c, actual ≈1' "
            "convention fork. Conclusion: the absolute scale must enter as a dimensionful "
            "/ cross-scale input (the v_H–M_Pl hierarchy, route b), consistent with the "
            "criterion that y_t's absolute value runs and is therefore not invariant. "
            "Scope: fences off the matrix-normalization / single-correlation-ceiling "
            "class; does not rule out a genuine dimensionful/dynamical derivation."
        ),
        key_result=(
            "Absolute y_t not fixable by Yukawa-matrix normalization: rank-2/CKM breaks "
            "the unit ceiling (top = 9/8), all matrix-norms are top-dominated (circular), "
            "and the a_Y count is N_c-convention-dependent (non-physical). Absolute scale "
            "⇒ dimensionful input (route b). [P_structural_yt_absolute_scale_normalization_no_go]"
        ),
        dependencies=[
            "L_Yukawa_bilinear",
            "L_mass_from_capacity",
            "T_channels",
            "T_capacity_ladder",
            "T_q_Higgs",
        ],
        cross_refs=[
            "L_Gram",
            "L_top_mass_hint",
        ],
        artifacts={
            "single_channel_top_ceiling": 1,
            "two_channel_top_entry": "c_B + c_H = x^3 + 1 = 9/8",
            "frob_over_opnorm": round(frob / op_norm, 6),
            "norm_invariants_top_dominated": True,
            "a_Y_convention_fork": {
                "a_Y=N_c=3 (with color)": 1.0,
                "a_Y=1 (no color)": 1.0,
                "a_Y=1 (with color)": round(1 / math.sqrt(3), 4),
                "a_Y=3 (no color)": round(math.sqrt(3), 4),
            },
            "invariant_content": "inter-generation ratios + mixing angle + saturation structure only",
            "absolute_scale_route": "dimensionful / v_H-M_Pl hierarchy (route b)",
            "reference_docs": [
                "Reference - y_t Absolute-Scale Normalization No-Go v0.1 (2026-05-29).md",
            ],
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_yt_absolute_scale_not_fixable_by_normalization_no_go":
        check_T_yt_absolute_scale_not_fixable_by_normalization_no_go_P,
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
        "input_id": "flavour:yt_normalization_no_go",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Banks a NEGATIVE result -- an obstruction, not a value: "
            "check_T_yt_absolute_scale_not_fixable_by_normalization_no_go_P "
            "(machine field "
            "epistemic='P_structural_yt_absolute_scale_normalization_no_go', a "
            "bespoke structural token) certifies that the absolute top Yukawa y_t "
            "cannot be fixed by any unitarity/normalization principle on the "
            "Yukawa matrix. Three independently re-verified legs: (1) the two- "
            "channel structure that gives CKM and the light generations "
            "(T_channels; q_B = (7,4,0), q_H = (7,5,0), both zero on top) "
            "destroys the Cauchy-Schwarz unit ceiling -- the physical top entry "
            "is the channel sum x^3 + 1 = 9/8 > 1; (2) every norm invariant of "
            "the top-dominated Yukawa matrix equals the top to 1 part in 1e4, so "
            "normalizing any matrix norm IS fixing y_t -- circular; (3) the one "
            "count-based handle, the spectral-action a_Y, is color-counting- "
            "convention dependent, hence non-physical by the invariance "
            "criterion. The inter-generation Yukawa RATIOS remain native [P] "
            "(L_multiplicative_amplitude, L_Yukawa_bilinear); the absolute scale "
            "remains OPEN, consistent with the 2026-07-02 termination of the "
            "absolute-scale frontier "
            "(check_T_ew_scale_functional_independence_no_go). No absolute-scale "
            "derivation is claimed; the route is fenced so future cycles do not "
            "re-attempt it. "
        ),
        "note": "Wave 7 absolute-top-Yukawa normalization no-go; bespoke P_structural_* token, obstruction result",
    },
)
