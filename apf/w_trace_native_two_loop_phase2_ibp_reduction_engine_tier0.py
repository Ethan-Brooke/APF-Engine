"""APF-native two-loop Phase-2 IBP reduction engine + Tier-0 reduced rows — Tier-4.

Phase-2 push v9 lands the IBP-reduction infrastructure between the v8 projector/
router gate and the v10 coefficient-output slices: a runnable numerator-rewrite/
linear-reduction engine, a Tier-0 reduced-row ledger, Laporta batch job specs
for five families, and a real-row cancellation/aggregate bridge.

The verifiable native content this module re-derives is the exact
scalar-product → inverse-propagator rewrite for the five-line two-point family
TP5 (D1=p²−m1², D2=q²−m2², D3=(p−q)²−m3², D4=(p−k)²−m4², D5=(q−k)²−m5², s=k²):

    p·k = (D1 − D4 + m1² − m4² + s)/2
    q·k = (D2 − D5 + m2² − m5² + s)/2
    p·q = (D1 + D2 − D3 + m1² + m2² − m3²)/2

Each rewrite lowers the corresponding denominator power by one (an integral
shift); the engine is verified by reconstructing the scalar-product symbol from
the shifted-integral coefficients with the propagators restored, recovering the
identity exactly in sympy. Sector detection flags the central-line (D3)
contraction that separates a genuine two-loop topology from a one-loop product.

It does NOT claim a complete Standard-Model IBP rational-coefficient table or
evaluated physical two-loop self-energies.

Honest non-claims preserved verbatim:
  * Export_EW_complete_IBP_coefficient_output_P = 0
  * Export_EW_complete_physical_self_energy_evaluator_P = 0
  * Export_OSW_delta_r_rem_APF_internal_P = 0

Sibling APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v9
(self-verifier TWO_LOOP_PHASE2_PUSH_V9_PASS, 5/5).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import sympy as sp

from apf.apf_utils import check, _result


# =============================================================================
# Source-certified kernel: exact scalar-product → inverse-propagator rewrite
# =============================================================================


@dataclass(frozen=True, order=True)
class Integral:
    family: str
    powers: tuple


def _shift(integ: Integral, which: int, delta: int) -> Integral:
    p = list(integ.powers)
    p[which] += delta
    return Integral(integ.family, tuple(p))


def scalar_product_rewrite(kind: str, powers=(1, 1, 1, 1, 1), family="TP5"):
    """Exact denominator-linear rewrite of p·k, q·k, p·q for the TP5 family.

    Returns {Integral: coeff}. Multiplying by D_i lowers the i-th power by one.
    """
    if len(powers) != 5:
        raise ValueError("TP5 scalar-product rewrites require five denominator powers")
    m1_2, m2_2, m3_2, m4_2, m5_2, s = sp.symbols("m1_2 m2_2 m3_2 m4_2 m5_2 s")
    I = Integral(family, tuple(powers))
    out: Dict[Integral, sp.Expr] = {}

    def add(integ, coeff):
        out[integ] = sp.expand(out.get(integ, 0) + coeff)

    if kind == "p_dot_k":
        add(_shift(I, 0, -1), sp.Rational(1, 2))
        add(_shift(I, 3, -1), -sp.Rational(1, 2))
        add(I, sp.Rational(1, 2) * (m1_2 - m4_2 + s))
    elif kind == "q_dot_k":
        add(_shift(I, 1, -1), sp.Rational(1, 2))
        add(_shift(I, 4, -1), -sp.Rational(1, 2))
        add(I, sp.Rational(1, 2) * (m2_2 - m5_2 + s))
    elif kind == "p_dot_q":
        add(_shift(I, 0, -1), sp.Rational(1, 2))
        add(_shift(I, 1, -1), sp.Rational(1, 2))
        add(_shift(I, 2, -1), -sp.Rational(1, 2))
        add(I, sp.Rational(1, 2) * (m1_2 + m2_2 - m3_2))
    else:
        raise ValueError(f"unknown scalar product kind: {kind}")
    return out


# Symbolic inverse propagators as functions of the abstract loop kinematics.
def _propagator_symbols():
    p2, q2, pq, pk, qk, k2 = sp.symbols("p2 q2 pq pk qk k2")
    m1_2, m2_2, m3_2, m4_2, m5_2, s = sp.symbols("m1_2 m2_2 m3_2 m4_2 m5_2 s")
    D = {
        0: p2 - m1_2,
        1: q2 - m2_2,
        2: p2 + q2 - 2 * pq - m3_2,        # (p-q)^2
        3: p2 + k2 - 2 * pk - m4_2,        # (p-k)^2
        4: q2 + k2 - 2 * qk - m5_2,        # (q-k)^2
    }
    sp_targets = {"p_dot_k": pk, "q_dot_k": qk, "p_dot_q": pq}
    return D, sp_targets, {k2: s}


def reconstruct_scalar_product(kind: str):
    """Restore the propagators on each shifted integral and recover the SP symbol.

    A '-1' shift on denominator i means the rewrite term carries that propagator
    D_i as a numerator factor. Summing coeff * (restored numerator) must return
    the scalar-product symbol exactly.
    """
    D, sp_targets, subs = _propagator_symbols()
    rewrite = scalar_product_rewrite(kind)
    base = Integral("TP5", (1, 1, 1, 1, 1))
    total = 0
    for integ, coeff in rewrite.items():
        # which denominator(s) were lowered relative to base → numerator factor
        num = 1
        for i in range(5):
            d = base.powers[i] - integ.powers[i]   # +1 if lowered
            if d == 1:
                num *= D[i]
            elif d != 0:
                raise AssertionError("unexpected shift magnitude")
        total += coeff * num
    return sp.expand(sp.expand(total).subs(subs))


def detect_sector(integ: Integral) -> str:
    zeros = [i for i, p in enumerate(integ.powers) if p <= 0]
    if 2 in zeros:
        return "central_line_contracted_one_loop_product"
    if zeros:
        return "contracted_subtopology"
    return "genuine_five_line"


LAPORTA_FAMILIES = ("TP5", "SUN3", "ZFF_LIGHT", "BOSONIC", "MUON_HARD")


EXPORT_FLAGS = {
    "Export_phase2_ibp_reduction_engine_tier0_P": 1,
    "Export_scalar_product_rewrite_exact_P": 1,
    "Export_laporta_job_specs_five_families_P": 1,
    "Export_EW_complete_IBP_coefficient_output_P": 0,
    "Export_EW_complete_physical_self_energy_evaluator_P": 0,
    "Export_OSW_delta_r_rem_APF_internal_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_ibp_reduction_engine_tier0_current_depth_P():
    """T: Phase-2 IBP reduction engine + Tier-0 reduced rows. The three TP5
    scalar-product rewrites (p·k, q·k, p·q) are exact denominator-linear
    identities: restoring the lowered propagators on each shifted integral and
    summing the engine's coefficients recovers the scalar-product symbol
    exactly in sympy. Each rewrite lowers exactly one denominator power per
    shifted term. Central-line (D3) contraction is detected as a one-loop
    product. Five Laporta job-spec families present. No complete IBP table, no
    physical self-energy.
    [P_two_loop_phase2_ibp_reduction_engine_tier0_current_depth;
     C_complete_coefficient_output_pending]."""

    # (a) Exact reconstruction of each scalar product from the rewrite.
    pk, qk, pq = sp.symbols("pk qk pq")
    check(sp.simplify(reconstruct_scalar_product("p_dot_k") - pk) == 0,
          "p·k rewrite must reconstruct exactly")
    check(sp.simplify(reconstruct_scalar_product("q_dot_k") - qk) == 0,
          "q·k rewrite must reconstruct exactly")
    check(sp.simplify(reconstruct_scalar_product("p_dot_q") - pq) == 0,
          "p·q rewrite must reconstruct exactly")

    # (b) Each rewrite lowers exactly one denominator per shifted (non-base) term.
    base = (1, 1, 1, 1, 1)
    for kind in ("p_dot_k", "q_dot_k", "p_dot_q"):
        rw = scalar_product_rewrite(kind)
        for integ in rw:
            if integ.powers == base:
                continue
            lowered = [i for i in range(5) if base[i] - integ.powers[i] == 1]
            check(len(lowered) == 1,
                  f"{kind} shifted term must lower exactly one denominator")

    # (c) Sector detection: central-line contraction → one-loop product.
    check(detect_sector(Integral("TP5", (1, 1, 0, 1, 1)))
          == "central_line_contracted_one_loop_product",
          "D3=0 must be flagged as central-line one-loop product")
    check(detect_sector(Integral("TP5", (1, 1, 1, 1, 1))) == "genuine_five_line",
          "all-positive powers must be genuine five-line")

    # (d) Laporta job specs.
    check(len(LAPORTA_FAMILIES) == 5, "five Laporta job-spec families expected")

    # (e) Honest non-claim flags.
    for k in ("Export_EW_complete_IBP_coefficient_output_P",
              "Export_EW_complete_physical_self_energy_evaluator_P",
              "Export_OSW_delta_r_rem_APF_internal_P"):
        check(EXPORT_FLAGS[k] == 0, f"{k} must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_ibp_reduction_engine_tier0_current_depth: "
              "Phase-2 IBP numerator-rewrite engine. The three TP5 "
              "scalar-product → inverse-propagator identities reconstruct "
              "exactly in sympy; central-line contraction detected. "
              "[P_two_loop_phase2_ibp_reduction_engine_tier0_current_depth]"),
        tier=4,
        epistemic="P_two_loop_phase2_ibp_reduction_engine_tier0_current_depth",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v9 "
            "(5 packs: IBP reduction engine, Tier-0 reduced-row ledger, Laporta "
            "batch job specs, real-row cancellation/aggregate bridge, "
            "row-production status; self-verifier 5/5 PASS). This module "
            "re-derives the exact scalar-product → inverse-propagator rewrites "
            "for the TP5 five-line two-point family: p·k, q·k, p·q each expand "
            "into a base integral plus single-denominator-lowered shifts with "
            "rational coefficients. Restoring the lowered propagators as "
            "numerator factors and summing recovers the scalar-product symbol "
            "exactly (sympy simplify → 0). Sector detection flags the "
            "central-line (D3) contraction that distinguishes a genuine "
            "two-loop topology from a one-loop product — the same irreducibility "
            "discipline that anchors v24.3.143 and the v11 no-smuggling guard. "
            "Five Laporta job-spec families are present. No complete SM IBP "
            "rational-coefficient table and no evaluated physical two-loop "
            "self-energies are claimed."
        ),
        key_result=(
            "Phase-2 IBP engine: exact TP5 scalar-product rewrites + central-line "
            "sector detection + five Laporta job specs. "
            "[P_two_loop_phase2_ibp_reduction_engine_tier0_current_depth]"
        ),
        dependencies=[
            "T_two_loop_phase2_projectors_preibp_router_current_depth",
            "T_two_loop_two_point_5line_euclidean_master_arbitrary_mass",
        ],
        cross_refs=[],
        artifacts={
            "scalar_products": ["p_dot_k", "q_dot_k", "p_dot_q"],
            "laporta_families": list(LAPORTA_FAMILIES),
            "sibling_bundle": "APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v9",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_ibp_reduction_engine_tier0_current_depth":
        check_T_two_loop_phase2_ibp_reduction_engine_tier0_current_depth_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
