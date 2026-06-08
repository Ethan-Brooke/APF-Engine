"""APF-native two-loop Phase-2 OS-W Δr connector + refusal gate (TOY ONLY) — Tier-4.

Linear assembly connector taking 4 EW two-loop self-energies (Σ_W, Σ_Z, Π_γγ,
Π_γZ) + vertex/box + tadpole counterterm + charge/mixing counterterm into a
finite Δr_rem candidate. The coefficients of the toy linear map are deliberately
explicit and non-target-fitted — they exercise the coverage + refusal gates
without claiming any physical OS-W Δr_rem value.

Components:

  * `FiniteComponent` — single source-certified finite contribution carrying
    `finite_value`, `covariance`, `source_reference`, `convention_key`,
    `source_certified`, `target_observable_consumed`, `fitted` flags. The
    `validate()` method refuses missing fields, non-finite values, negative
    covariance, forbidden-source-token smuggling, target-observable
    consumption, fitted flag, and missing source certification.
  * `OSWDeltaRInput` — bundle of 4 channel self-energies + vertex/box +
    tadpole counterterm + charge/mixing counterterm with one shared
    `convention_key` and a `source_certified_physical` boolean gate.
  * `assemble_delta_r_rem()` — runs `validate_osw_input()` (channel coverage,
    convention-key match across all 7 components, forbidden-input declaration,
    source certification), then computes the toy-coefficient linear sum and
    Gaussian-propagated covariance. Returns
    `OSWDeltaRResult` with status string `OSW_DELTAR_CONNECTOR_TOY_ASSEMBLY_PASS__PHYSICAL_VALUE_NOT_CLAIMED`.

Forbidden-input refusal tokens: `measured_M_W`, `published_total_SM_M_W`,
`DIZET_aggregate`, `ZFITTER_aggregate`, `target_interval`, `fit_counterterm`,
`fitted_counterterm`.

Honest non-claims preserved verbatim:
  * Export_OSW_delta_r_rem_APF_internal = 0
  * Export_OSW_DeltaRhobarW_evaluated = 0
  * Export_evaluated_EW_two_loop_self_energies = 0
  * Export_vertex_box_two_loop_finite_remainder = 0

The deliberately-named next gate is: provide all self-energy, vertex/box,
tadpole, charge/mixing, and counterterm components with one convention key,
all source-certified, no forbidden inputs — at which point this connector
assembles the candidate Δr_rem and the physical-value gate is the remaining
release step.

Sibling APF_TWO_LOOP_PHASE2_OSW_DELTAR_CONNECTOR_AND_REFUSAL_v2 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v3.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from typing import Dict

from apf.apf_utils import check, _result


# =============================================================================
# Source-certified kernel
# =============================================================================

REQUIRED_SELF_ENERGIES = ("Sigma_W_2L", "Sigma_Z_2L", "Pi_gammagamma_2L", "Pi_gammaZ_2L")
FORBIDDEN_TOKENS = (
    "measured_M_W", "published_total_SM_M_W", "DIZET_aggregate", "ZFITTER_aggregate",
    "target_interval", "fit_counterterm", "fitted_counterterm",
)


class DeltaRConnectorError(ValueError):
    pass


@dataclass(frozen=True)
class FiniteComponent:
    name: str
    finite_value: float
    covariance: float
    source_reference: str
    convention_key: str
    source_certified: bool
    target_observable_consumed: bool = False
    fitted: bool = False

    def validate(self) -> None:
        if not self.name.strip():
            raise DeltaRConnectorError("component name missing")
        if not math.isfinite(self.finite_value):
            raise DeltaRConnectorError(f"{self.name}: finite value is not finite")
        if self.covariance < 0 or not math.isfinite(self.covariance):
            raise DeltaRConnectorError(f"{self.name}: invalid covariance")
        if not self.source_reference.strip():
            raise DeltaRConnectorError(f"{self.name}: missing source reference")
        if not self.convention_key.strip():
            raise DeltaRConnectorError(f"{self.name}: missing convention key")
        if any(tok in self.source_reference for tok in FORBIDDEN_TOKENS):
            raise DeltaRConnectorError(f"{self.name}: forbidden source/input token")
        if self.target_observable_consumed:
            raise DeltaRConnectorError(f"{self.name}: target observable consumed")
        if self.fitted:
            raise DeltaRConnectorError(f"{self.name}: fitted component refused")
        if not self.source_certified:
            raise DeltaRConnectorError(f"{self.name}: source certification missing")


@dataclass(frozen=True)
class OSWDeltaRInput:
    self_energies: Dict[str, FiniteComponent]
    vertex_box: FiniteComponent
    tadpole_counterterm: FiniteComponent
    charge_mixing_counterterm: FiniteComponent
    convention_key: str
    source_certified_physical: bool
    no_forbidden_inputs_declared: bool = True


@dataclass(frozen=True)
class OSWDeltaRResult:
    delta_r_rem_finite: float
    covariance: float
    status: str
    component_count: int
    convention_key: str

    def asdict(self):
        return asdict(self)


def validate_osw_input(inp: OSWDeltaRInput) -> None:
    if not inp.no_forbidden_inputs_declared:
        raise DeltaRConnectorError("forbidden-input declaration is false")
    if not inp.convention_key.strip():
        raise DeltaRConnectorError("missing assembly convention key")
    missing = set(REQUIRED_SELF_ENERGIES) - set(inp.self_energies)
    if missing:
        raise DeltaRConnectorError("missing self-energy channels: " + ",".join(sorted(missing)))
    extra = set(inp.self_energies) - set(REQUIRED_SELF_ENERGIES)
    if extra:
        raise DeltaRConnectorError("unexpected self-energy channels: " + ",".join(sorted(extra)))
    comps = (list(inp.self_energies.values()) + [inp.vertex_box,
             inp.tadpole_counterterm, inp.charge_mixing_counterterm])
    for c in comps:
        c.validate()
        if c.convention_key != inp.convention_key:
            raise DeltaRConnectorError(f"{c.name}: convention mismatch")
    if not inp.source_certified_physical:
        raise DeltaRConnectorError("physical source-certified OSW connector ledger missing")


def assemble_delta_r_rem(inp: OSWDeltaRInput) -> OSWDeltaRResult:
    """Toy linear assembly map. Coefficients explicit, non-target-fitted; physical import would replace these with source-certified OS-W formula rows."""
    validate_osw_input(inp)
    se = inp.self_energies
    finite = (
        + 1.00 * se["Sigma_W_2L"].finite_value
        - 0.75 * se["Sigma_Z_2L"].finite_value
        + 0.50 * se["Pi_gammagamma_2L"].finite_value
        - 0.25 * se["Pi_gammaZ_2L"].finite_value
        + 1.00 * inp.vertex_box.finite_value
        + 1.00 * inp.tadpole_counterterm.finite_value
        + 1.00 * inp.charge_mixing_counterterm.finite_value
    )
    cov = (
        (1.00 ** 2) * se["Sigma_W_2L"].covariance
        + (0.75 ** 2) * se["Sigma_Z_2L"].covariance
        + (0.50 ** 2) * se["Pi_gammagamma_2L"].covariance
        + (0.25 ** 2) * se["Pi_gammaZ_2L"].covariance
        + inp.vertex_box.covariance
        + inp.tadpole_counterterm.covariance
        + inp.charge_mixing_counterterm.covariance
    )
    return OSWDeltaRResult(
        finite, cov,
        "OSW_DELTAR_CONNECTOR_TOY_ASSEMBLY_PASS__PHYSICAL_VALUE_NOT_CLAIMED",
        7, inp.convention_key,
    )


def toy_component(name: str, value: float, convention_key: str = "toy_OSW_v2"
                  ) -> FiniteComponent:
    return FiniteComponent(
        name=name, finite_value=float(value), covariance=1e-6,
        source_reference="toy_source_for_connector_gate_testing_only",
        convention_key=convention_key, source_certified=True,
    )


def make_toy_osw_input(*, source_certified_physical: bool = True) -> OSWDeltaRInput:
    key = "toy_OSW_v2"
    return OSWDeltaRInput(
        self_energies={
            "Sigma_W_2L":       toy_component("Sigma_W_2L", 0.010, key),
            "Sigma_Z_2L":       toy_component("Sigma_Z_2L", 0.004, key),
            "Pi_gammagamma_2L": toy_component("Pi_gammagamma_2L", 0.003, key),
            "Pi_gammaZ_2L":     toy_component("Pi_gammaZ_2L", -0.002, key),
        },
        vertex_box=toy_component("vertex_box_2L", 0.001, key),
        tadpole_counterterm=toy_component("tadpole_counterterm", -0.004, key),
        charge_mixing_counterterm=toy_component("charge_mixing_counterterm", 0.0005, key),
        convention_key=key,
        source_certified_physical=source_certified_physical,
        no_forbidden_inputs_declared=True,
    )


@dataclass(frozen=True)
class OSWConnectorClaim:
    OSW_delta_r_connector_contract_P: int = 1
    OSW_delta_r_component_coverage_gate_P: int = 1
    OSW_delta_r_forbidden_input_refusal_P: int = 1
    OSW_delta_r_toy_assembly_gate_P: int = 1
    OSW_delta_r_rem_APF_internal_P: int = 0
    OSW_DeltaRhobarW_evaluated_P: int = 0
    evaluated_EW_two_loop_self_energies_P: int = 0
    vertex_box_two_loop_finite_remainder_P: int = 0


# =============================================================================
# Export flags + bank check
# =============================================================================

EXPORT_FLAGS = {
    "Export_OSW_delta_r_connector_contract_P": 1,
    "Export_OSW_delta_r_component_coverage_gate_P": 1,
    "Export_OSW_delta_r_forbidden_input_refusal_P": 1,
    "Export_OSW_delta_r_toy_assembly_gate_P": 1,
    "Export_OSW_delta_r_rem_APF_internal_P": 0,
    "Export_OSW_DeltaRhobarW_evaluated_P": 0,
    "Export_evaluated_EW_two_loop_self_energies_P": 0,
    "Export_vertex_box_two_loop_finite_remainder_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def _expect_refused(label: str, fn):
    try:
        fn()
    except DeltaRConnectorError:
        return
    raise AssertionError(f"{label}: connector did NOT refuse as expected")


def check_T_two_loop_phase2_osw_deltar_connector_refusal_toy_P():
    """T: OS-W Δr connector + refusal gate (TOY LEDGER ONLY). Linear assembly
    over 4 channel self-energies + vertex/box + tadpole CT + charge/mixing CT
    with one convention key. 9 negative-case refusals enforced. NO physical
    OS-W Δr_rem value, no evaluated EW self-energy.
    [P_two_loop_phase2_osw_deltar_connector_refusal_toy]."""

    # (a) Claim flags.
    claim = OSWConnectorClaim()
    check(claim.OSW_delta_r_connector_contract_P == 1, "claim connector export must be 1")
    check(claim.OSW_delta_r_rem_APF_internal_P == 0, "claim Δr_rem APF-internal must be 0")
    check(claim.OSW_DeltaRhobarW_evaluated_P == 0, "claim Δρ̄_W evaluated must be 0")
    check(claim.evaluated_EW_two_loop_self_energies_P == 0, "claim evaluated EW self-energies must be 0")

    # (b) Toy connector pass.
    inp = make_toy_osw_input(source_certified_physical=True)
    res = assemble_delta_r_rem(inp)
    check(res.status.startswith("OSW_DELTAR_CONNECTOR_TOY_ASSEMBLY_PASS"),
          f"toy connector status: {res.status}")
    check(res.covariance > 0, f"toy covariance must be positive: {res.covariance}")
    check(res.component_count == 7, f"toy component count: {res.component_count}")
    check(res.convention_key == "toy_OSW_v2", f"toy convention_key: {res.convention_key}")

    # (c) 9 refusal cases.
    _expect_refused("missing_physical_source_certification",
                    lambda: assemble_delta_r_rem(make_toy_osw_input(source_certified_physical=False)))
    bad = make_toy_osw_input(source_certified_physical=True)
    bad_self = dict(bad.self_energies)
    bad_self.pop("Pi_gammaZ_2L")
    _expect_refused("missing_Pi_gammaZ_channel",
                    lambda: assemble_delta_r_rem(OSWDeltaRInput(
                        bad_self, bad.vertex_box, bad.tadpole_counterterm,
                        bad.charge_mixing_counterterm, bad.convention_key, True)))
    bad_vb = FiniteComponent(**{**bad.vertex_box.__dict__, "source_certified": False})
    _expect_refused("missing_vertex_box_source_certification",
                    lambda: assemble_delta_r_rem(OSWDeltaRInput(
                        bad.self_energies, bad_vb, bad.tadpole_counterterm,
                        bad.charge_mixing_counterterm, bad.convention_key, True)))
    bad_ct = FiniteComponent(**{**bad.tadpole_counterterm.__dict__, "convention_key": "other"})
    _expect_refused("convention_key_mismatch",
                    lambda: assemble_delta_r_rem(OSWDeltaRInput(
                        bad.self_energies, bad.vertex_box, bad_ct,
                        bad.charge_mixing_counterterm, bad.convention_key, True)))
    bad_src = FiniteComponent(**{**bad.vertex_box.__dict__, "source_reference": "DIZET_aggregate"})
    _expect_refused("DIZET_aggregate_token",
                    lambda: assemble_delta_r_rem(OSWDeltaRInput(
                        bad.self_energies, bad_src, bad.tadpole_counterterm,
                        bad.charge_mixing_counterterm, bad.convention_key, True)))
    bad_src2 = FiniteComponent(**{**bad.vertex_box.__dict__, "source_reference": "published_total_SM_M_W"})
    _expect_refused("published_total_SM_M_W_token",
                    lambda: assemble_delta_r_rem(OSWDeltaRInput(
                        bad.self_energies, bad_src2, bad.tadpole_counterterm,
                        bad.charge_mixing_counterterm, bad.convention_key, True)))
    bad_target = FiniteComponent(**{**bad.vertex_box.__dict__, "target_observable_consumed": True})
    _expect_refused("target_observable_consumed",
                    lambda: assemble_delta_r_rem(OSWDeltaRInput(
                        bad.self_energies, bad_target, bad.tadpole_counterterm,
                        bad.charge_mixing_counterterm, bad.convention_key, True)))
    bad_fit = FiniteComponent(**{**bad.vertex_box.__dict__, "fitted": True})
    _expect_refused("fitted_component",
                    lambda: assemble_delta_r_rem(OSWDeltaRInput(
                        bad.self_energies, bad_fit, bad.tadpole_counterterm,
                        bad.charge_mixing_counterterm, bad.convention_key, True)))
    bad_cov = FiniteComponent(**{**bad.vertex_box.__dict__, "covariance": -1.0})
    _expect_refused("negative_covariance",
                    lambda: assemble_delta_r_rem(OSWDeltaRInput(
                        bad.self_energies, bad_cov, bad.tadpole_counterterm,
                        bad.charge_mixing_counterterm, bad.convention_key, True)))

    # (d) Honest non-claim flags.
    check(EXPORT_FLAGS["Export_OSW_delta_r_connector_contract_P"] == 1,
          "connector contract flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_delta_r_forbidden_input_refusal_P"] == 1,
          "forbidden-input refusal flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_delta_r_rem_APF_internal_P"] == 0,
          "OS-W Δr_rem APF-internal must remain 0")
    check(EXPORT_FLAGS["Export_OSW_DeltaRhobarW_evaluated_P"] == 0,
          "OS-W Δρ̄_W evaluated must remain 0")
    check(EXPORT_FLAGS["Export_evaluated_EW_two_loop_self_energies_P"] == 0,
          "evaluated EW two-loop self-energies must remain 0")
    check(EXPORT_FLAGS["Export_vertex_box_two_loop_finite_remainder_P"] == 0,
          "vertex/box two-loop finite remainder must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_osw_deltar_connector_refusal_toy: "
              "OS-W Δr connector + refusal gate (TOY LEDGER ONLY). Linear "
              "assembly over 4 channel self-energies (Σ_W, Σ_Z, Π_γγ, Π_γZ) "
              "+ vertex/box + tadpole counterterm + charge/mixing counterterm "
              "with one shared convention key. 9 negative-case refusals "
              "enforced (missing physical certification, missing channel, "
              "missing component certification, convention mismatch, DIZET "
              "token, published-total-SM-MW token, target observable "
              "consumed, fitted component, negative covariance). NO physical "
              "OS-W Δr_rem value, no evaluated EW self-energy. "
              "[P_two_loop_phase2_osw_deltar_connector_refusal_toy; "
              "C_osw_deltar_physical_remainder_pending]"),
        tier=4,
        epistemic="P_two_loop_phase2_osw_deltar_connector_refusal_toy",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v3 / "
            "APF_TWO_LOOP_PHASE2_OSW_DELTAR_CONNECTOR_AND_REFUSAL_v2. Three "
            "components: (a) FiniteComponent record carrying value, "
            "covariance, source_reference, convention_key, source_certified "
            "boolean, plus target/fitted refusal flags — validate() refuses "
            "missing fields, non-finite values, negative covariance, "
            "forbidden-source tokens, target consumption, fitted flag, "
            "missing source certification; (b) OSWDeltaRInput bundle of 4 "
            "channel self-energies + vertex/box + tadpole CT + charge/mixing "
            "CT with shared convention_key and source_certified_physical "
            "gate; (c) assemble_delta_r_rem() linear toy map with coefficients "
            "(+1, -0.75, +0.5, -0.25, +1, +1, +1) on the 7 components and "
            "Gaussian-propagated covariance with the same |c|² weights. "
            "Status string carries '__PHYSICAL_VALUE_NOT_CLAIMED'. The "
            "explicit next gate is: supply all 7 components source-certified "
            "physical with one convention key, no forbidden inputs."
        ),
        key_result=(
            "OS-W Δr connector + refusal gate implemented as a toy linear "
            "assembly with 9 negative-case refusals; physical Δr_rem and "
            "physical component values remain OPEN. "
            "[P_two_loop_phase2_osw_deltar_connector_refusal_toy; "
            "C_osw_deltar_physical_remainder_pending]"
        ),
        dependencies=[
            "T_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger",
        ],
        cross_refs=[
            "T_BSY_one_loop_kappa_l_assembly_consistency_at_Denner_validated_inputs",
        ],
        artifacts={
            "channel_set": list(REQUIRED_SELF_ENERGIES),
            "forbidden_tokens": list(FORBIDDEN_TOKENS),
            "toy_coefficients": {
                "Sigma_W_2L": 1.00, "Sigma_Z_2L": -0.75,
                "Pi_gammagamma_2L": 0.50, "Pi_gammaZ_2L": -0.25,
                "vertex_box": 1.00, "tadpole_counterterm": 1.00,
                "charge_mixing_counterterm": 1.00,
            },
            "refusal_cases_count": 9,
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_osw_deltar_connector_refusal_toy":
        check_T_two_loop_phase2_osw_deltar_connector_refusal_toy_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
