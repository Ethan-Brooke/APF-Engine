"""APF-native two-loop Phase-2 EW self-energy assembly gate (TOY LEDGER ONLY) — Tier-4.

Runtime contract + pole-cancellation gate for Phase-2 electroweak two-loop
self-energy assembly. A future source-certified SM two-loop diagram-coefficient
ledger can be plugged into this interface; the gate either renormalizes
cleanly (poles cancel against counterterms, all classes declared, no forbidden
inputs) or fails with a named obstruction.

The gate is exercised here against a TOY ledger whose pole structure is
manufactured to cancel exactly. The TOY ledger pass proves the algebraic
gate ONLY — it does NOT prove any Standard-Model electroweak self-energy value.

Components:

  * `PoleSeries(c_m2, c_m1, c_0)` — small-epsilon Laurent record with addition,
    scaling, finite-part extraction, pole-norm.
  * `RenormalizationContract` — schema declaring scheme, μ², finite-part
    convention, subtraction prescription, gauge, tadpole convention,
    counterterm policy, source reference, Ward zero-momentum normalization,
    covariance ledger, and `coefficient_ledger_certified` boolean.
  * `MasterTerm` — diagram-class-tagged Laurent term with `irreducible` flag
    that catches reducible B0×B0 smuggling on the 5-line two-point master.
  * `Counterterm` — Laurent counterterm with `fitted` guard.
  * `ForbiddenInputLedger` — refuses measured M_W, DIZET/ZFITTER aggregates,
    published total SM M_W, target intervals, fitted counterterms.
  * `REQUIRED_CLASSES` — per-channel diagram-class completeness contract for
    Σ_W, Σ_Z, Π_γγ, Π_γZ at two loops.
  * `renormalize_self_energy()` — validates contract + terms, assembles bare
    series + counterterm series, verifies poles cancel to tolerance, returns
    `RenormalizedSelfEnergyResult` with finite-part value and TOY status string.

Gate refusal tests (8 negative cases): missing coefficient ledger; missing
diagram class; uncancelled poles; measured-M_W input; fitted counterterm;
forbidden source-label smuggling; reducible B0×B0 smuggling on the 5-line
master; photon-channel Ward declaration missing.

Honest non-claims preserved verbatim — none of the following is exported:

  * `Sigma_W^(2L)`, `Sigma_Z^(2L)`, `Pi_γγ^(2L)`, `Pi_γZ^(2L)` as evaluated
    physical SM quantities.
  * APF-internal closure of OS-W `Δr_rem`.
  * Any DIZET/ZFITTER-equivalent aggregate.
  * Any measured M_W, published total SM M_W, or target interval as input.
  * Fitted counterterm.
  * Source-certified EW two-loop diagram coefficient ledger.
  * Absorptive all-threshold physical-sheet evaluator.

The deliberately-named open gate is `SOURCE_CERTIFIED_EW_TWO_LOOP_DIAGRAM_
COEFFICIENT_LEDGER`. That ledger must specify diagram classes, master-basis
coefficients, gauge choice, tadpole convention, renormalization scale,
subtraction prescription, finite-part convention, and counterterm/matching
scheme. Until it ships, this gate's positive result is the TOY pass only.

Sibling APF_TWO_LOOP_PHASE2_EW_SELF_ENERGY_ASSEMBLY_GATE_v1 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v1.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Iterable, Set

from apf.apf_utils import check, _result


# =============================================================================
# Pole series
# =============================================================================


@dataclass(frozen=True)
class PoleSeries:
    """Small-epsilon Laurent record c_m2/eps² + c_m1/eps + c_0."""
    c_m2: complex = 0j
    c_m1: complex = 0j
    c_0: complex = 0j

    def __add__(self, other: "PoleSeries") -> "PoleSeries":
        return PoleSeries(self.c_m2 + other.c_m2, self.c_m1 + other.c_m1,
                          self.c_0 + other.c_0)

    def scale(self, z: complex) -> "PoleSeries":
        return PoleSeries(z * self.c_m2, z * self.c_m1, z * self.c_0)

    def finite_part(self) -> complex:
        return self.c_0

    def pole_norm(self) -> float:
        return abs(self.c_m2) + abs(self.c_m1)

    def is_finite(self, tol: float = 1e-10) -> bool:
        return self.pole_norm() <= tol

    def asdict(self) -> Dict[str, float]:
        return {
            "c_m2_re": float(self.c_m2.real), "c_m2_im": float(self.c_m2.imag),
            "c_m1_re": float(self.c_m1.real), "c_m1_im": float(self.c_m1.imag),
            "c_0_re":  float(self.c_0.real),  "c_0_im":  float(self.c_0.imag),
        }


ZERO_SERIES = PoleSeries()


# =============================================================================
# Channel contract + forbidden-input ledger
# =============================================================================

VALID_CHANNELS = {"Sigma_W_2L", "Sigma_Z_2L", "Pi_gammagamma_2L", "Pi_gammaZ_2L"}

REQUIRED_CLASSES: Dict[str, Set[str]] = {
    "Sigma_W_2L":         {"fermion", "gauge_boson", "ghost", "goldstone", "higgs",
                           "tadpole", "counterterm", "master_integral"},
    "Sigma_Z_2L":         {"fermion", "gauge_boson", "ghost", "goldstone", "higgs",
                           "tadpole", "counterterm", "master_integral"},
    "Pi_gammagamma_2L":   {"charged_fermion", "charged_gauge", "ghost", "goldstone",
                           "scalar", "counterterm", "ward_normalization",
                           "master_integral"},
    "Pi_gammaZ_2L":       {"charged_fermion", "charged_gauge", "ghost", "goldstone",
                           "scalar", "counterterm", "mixing_renormalization",
                           "master_integral"},
}

FORBIDDEN_SOURCE_TOKENS = {"measured_M_W", "published_total_SM_M_W", "DIZET_aggregate",
                           "ZFITTER_aggregate", "target_interval", "fit_counterterm"}


class SelfEnergyGateError(ValueError):
    pass


@dataclass(frozen=True)
class MasterTerm:
    name: str
    topology: str
    series: PoleSeries
    coefficient: complex = 1 + 0j
    diagram_class: str = "master_integral"
    source_label: str = "source_certified_or_toy"
    irreducible: bool = True

    def contribution(self) -> PoleSeries:
        return self.series.scale(self.coefficient)


@dataclass(frozen=True)
class Counterterm:
    name: str
    series: PoleSeries
    source_label: str = "counterterm_ledger"
    fitted: bool = False


@dataclass(frozen=True)
class RenormalizationContract:
    scheme: str
    mu2: float
    finite_part_convention: str
    subtraction_prescription: str
    gauge: str
    tadpole_convention: str
    counterterm_policy: str
    coefficient_ledger_certified: bool
    diagram_classes_declared: Set[str]
    source_reference: str
    ward_zero_momentum_normalized: bool = False
    covariance_ledger_declared: bool = True


@dataclass(frozen=True)
class ForbiddenInputLedger:
    measured_M_W: bool = False
    published_total_SM_M_W: bool = False
    DIZET_or_ZFITTER_aggregate: bool = False
    target_interval: bool = False
    fitted_counterterm: bool = False

    def any_forbidden(self) -> bool:
        return any([self.measured_M_W, self.published_total_SM_M_W,
                    self.DIZET_or_ZFITTER_aggregate, self.target_interval,
                    self.fitted_counterterm])


@dataclass(frozen=True)
class RenormalizedSelfEnergyResult:
    channel: str
    finite_value: complex
    residual_poles: PoleSeries
    status: str
    consumed_terms: int
    contract_summary: Dict[str, object]


def _require_nonempty(value: str, field_name: str):
    if not isinstance(value, str) or not value.strip():
        raise SelfEnergyGateError(f"missing renormalization contract field: {field_name}")


def validate_contract(channel: str, contract: RenormalizationContract,
                      forbidden: ForbiddenInputLedger):
    if channel not in VALID_CHANNELS:
        raise SelfEnergyGateError(f"unknown self-energy channel {channel!r}")
    if forbidden.any_forbidden():
        raise SelfEnergyGateError("forbidden input ledger is non-empty")
    if not contract.coefficient_ledger_certified:
        raise SelfEnergyGateError("missing source-certified coefficient ledger")
    if contract.mu2 <= 0:
        raise SelfEnergyGateError("mu2 must be positive")
    for attr in ["scheme", "finite_part_convention", "subtraction_prescription",
                 "gauge", "tadpole_convention", "counterterm_policy", "source_reference"]:
        _require_nonempty(getattr(contract, attr), attr)
    if "fit" in contract.counterterm_policy.lower():
        raise SelfEnergyGateError("counterterm policy appears fitted, not source-certified")
    if channel.startswith("Pi_gamma") and not contract.ward_zero_momentum_normalized:
        raise SelfEnergyGateError(
            "photon/mixing channels require Ward/zero-momentum normalization declaration")
    if not contract.covariance_ledger_declared:
        raise SelfEnergyGateError("missing covariance ledger declaration")
    missing = REQUIRED_CLASSES[channel] - set(contract.diagram_classes_declared)
    if missing:
        raise SelfEnergyGateError("diagram class ledger incomplete: " + ",".join(sorted(missing)))


def validate_terms(channel: str, terms: List[MasterTerm], counterterms: List[Counterterm],
                   contract: RenormalizationContract):
    declared = set(contract.diagram_classes_declared)
    seen = {t.diagram_class for t in terms} | ({"counterterm"} if counterterms else set())
    missing = REQUIRED_CLASSES[channel] - (declared | seen)
    if missing:
        raise SelfEnergyGateError("required classes not represented: " + ",".join(sorted(missing)))
    for term in terms:
        if any(tok in term.source_label for tok in FORBIDDEN_SOURCE_TOKENS):
            raise SelfEnergyGateError("term source label contains forbidden input token")
        if term.topology == "two_point_5line" and not term.irreducible:
            raise SelfEnergyGateError("reducible B0xB0 smuggling detected for two_point_5line term")
    for ct in counterterms:
        if ct.fitted:
            raise SelfEnergyGateError("fitted counterterm refused")
        if any(tok in ct.source_label for tok in FORBIDDEN_SOURCE_TOKENS):
            raise SelfEnergyGateError("counterterm source label contains forbidden input token")


def assemble_bare_series(terms: Iterable[MasterTerm]) -> PoleSeries:
    out = ZERO_SERIES
    for term in terms:
        out = out + term.contribution()
    return out


def assemble_counterterm_series(counterterms: Iterable[Counterterm]) -> PoleSeries:
    out = ZERO_SERIES
    for ct in counterterms:
        out = out + ct.series
    return out


def renormalize_self_energy(channel: str, terms: List[MasterTerm],
                            counterterms: List[Counterterm],
                            contract: RenormalizationContract,
                            forbidden: ForbiddenInputLedger,
                            *, pole_tol: float = 1e-9
                            ) -> RenormalizedSelfEnergyResult:
    validate_contract(channel, contract, forbidden)
    validate_terms(channel, terms, counterterms, contract)
    total = assemble_bare_series(terms) + assemble_counterterm_series(counterterms)
    if not total.is_finite(pole_tol):
        raise SelfEnergyGateError(f"poles remain after counterterms: {total.asdict()}")
    return RenormalizedSelfEnergyResult(
        channel=channel,
        finite_value=total.finite_part(),
        residual_poles=total,
        status="RENORMALIZED_SELF_ENERGY_ASSEMBLY_GATE_PASS_TOY_LEDGER_ONLY",
        consumed_terms=len(terms) + len(counterterms),
        contract_summary={
            "scheme": contract.scheme,
            "mu2": contract.mu2,
            "finite_part_convention": contract.finite_part_convention,
            "subtraction_prescription": contract.subtraction_prescription,
            "gauge": contract.gauge,
            "tadpole_convention": contract.tadpole_convention,
            "counterterm_policy": contract.counterterm_policy,
            "source_reference": contract.source_reference,
        },
    )


def toy_contract(channel: str = "Sigma_W_2L", *, certified: bool = True
                 ) -> RenormalizationContract:
    classes = set(REQUIRED_CLASSES[channel])
    return RenormalizationContract(
        scheme="toy_OS_like_contract_not_physics",
        mu2=91.1876 ** 2,
        finite_part_convention="finite_part_after_explicit_pole_cancellation",
        subtraction_prescription="toy_on_shell_symbolic_subtraction",
        gauge="R_xi_declared_symbolic",
        tadpole_convention="explicit_tadpole_counterterm_ledger",
        counterterm_policy="source_certified_counterterm_policy",
        coefficient_ledger_certified=certified,
        diagram_classes_declared=classes,
        source_reference="toy_ledger_for_gate_testing_only",
        ward_zero_momentum_normalized=channel.startswith("Pi_gamma"),
        covariance_ledger_declared=True,
    )


def toy_terms_for(channel: str = "Sigma_W_2L"):
    """Build TOY (MasterTerm, Counterterm, contract, forbidden) tuple with manufactured pole cancellation."""
    terms = [
        MasterTerm("tadpole_scalar", "tadpole",
                   PoleSeries(1.0, -2.0, 0.25), coefficient=1.0, diagram_class="tadpole"),
        MasterTerm("sunset_DE_core", "sunset",
                   PoleSeries(-0.5, 1.5, 2.0), coefficient=2.0, diagram_class="master_integral"),
        MasterTerm("two_point_5line_euclidean", "two_point_5line",
                   PoleSeries(0.25, -0.25, -0.75), coefficient=4.0, diagram_class="gauge_boson"),
        MasterTerm("fermion_loop_class", "two_point_5line",
                   PoleSeries(0.0, 0.5, 1.1), coefficient=1.0,
                   diagram_class="fermion" if channel in {"Sigma_W_2L", "Sigma_Z_2L"} else "charged_fermion"),
        MasterTerm("ghost_class", "sunset",
                   PoleSeries(0.0, -0.25, -0.4), coefficient=1.0, diagram_class="ghost"),
        MasterTerm("goldstone_class", "sunset",
                   PoleSeries(0.0, 0.25, 0.6), coefficient=1.0, diagram_class="goldstone"),
        MasterTerm("higgs_or_scalar_class", "sunset",
                   PoleSeries(0.0, 0.0, 0.33), coefficient=1.0,
                   diagram_class="higgs" if channel in {"Sigma_W_2L", "Sigma_Z_2L"} else "scalar"),
    ]
    if channel == "Pi_gammagamma_2L":
        terms.append(MasterTerm("charged_gauge_alias", "two_point_5line",
                                PoleSeries(0, 0, 0.21), diagram_class="charged_gauge"))
        terms.append(MasterTerm("ward_normalization_alias", "counterterm_marker",
                                PoleSeries(0, 0, 0), diagram_class="ward_normalization"))
    elif channel == "Pi_gammaZ_2L":
        terms.append(MasterTerm("charged_gauge_alias", "two_point_5line",
                                PoleSeries(0, 0, 0.21), diagram_class="charged_gauge"))
        terms.append(MasterTerm("mixing_renormalization_alias", "counterterm_marker",
                                PoleSeries(0, 0, 0), diagram_class="mixing_renormalization"))
    bare = assemble_bare_series(terms)
    counterterms = [Counterterm("toy_pole_counterterm",
                                PoleSeries(-bare.c_m2, -bare.c_m1, -0.125),
                                source_label="toy_source_certified_counterterm_ledger")]
    return terms, counterterms, toy_contract(channel), ForbiddenInputLedger()


@dataclass(frozen=True)
class Phase2SelfEnergyGateClaim:
    phase2_EW_self_energy_assembly_gate_P: int = 1
    renormalization_contract_schema_P: int = 1
    pole_cancellation_gate_P: int = 1
    forbidden_input_guard_P: int = 1
    source_certified_EW_coefficient_ledger_P: int = 0
    evaluated_Sigma_W_2L_P: int = 0
    evaluated_Sigma_Z_2L_P: int = 0
    evaluated_Pi_gammagamma_2L_P: int = 0
    evaluated_Pi_gammaZ_2L_P: int = 0
    OSW_delta_r_rem_APF_internal_P: int = 0


# =============================================================================
# Export flags + bank check
# =============================================================================

EXPORT_FLAGS = {
    "Export_phase2_EW_self_energy_assembly_gate_P": 1,
    "Export_renormalization_contract_schema_P": 1,
    "Export_pole_cancellation_gate_P": 1,
    "Export_forbidden_input_guard_P": 1,
    "Export_master_integral_to_self_energy_runtime_contract_P": 1,
    "Export_source_certified_EW_coefficient_ledger_P": 0,
    "Export_evaluated_Sigma_W_2L_P": 0,
    "Export_evaluated_Sigma_Z_2L_P": 0,
    "Export_evaluated_Pi_gammagamma_2L_P": 0,
    "Export_evaluated_Pi_gammaZ_2L_P": 0,
    "Export_OSW_delta_r_rem_APF_internal_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def _expect_refused(label: str, fn):
    """Assert that fn() raises SelfEnergyGateError."""
    try:
        fn()
    except SelfEnergyGateError:
        return
    raise AssertionError(f"{label}: gate did NOT refuse as expected")


def check_T_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger_P():
    """T: Phase-2 EW self-energy assembly gate (TOY LEDGER ONLY). Validates
    runtime contract schema + pole cancellation algebra + forbidden-input
    guard + photon-Ward declaration guard + reducible B0×B0 quarantine
    against a TOY pole-cancellation ledger across all 4 channels
    (Σ_W, Σ_Z, Π_γγ, Π_γZ). 8 negative-case refusals enforced. Does NOT
    bank any evaluated physical SM self-energy or Δr.
    [P_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger;
     C_ew_two_loop_coefficient_ledger_pending]."""

    # (a) Claim dataclass.
    claim = Phase2SelfEnergyGateClaim()
    check(claim.phase2_EW_self_energy_assembly_gate_P == 1, "claim gate export must be 1")
    check(claim.evaluated_Sigma_W_2L_P == 0, "claim evaluated Σ_W must remain 0")
    check(claim.evaluated_Sigma_Z_2L_P == 0, "claim evaluated Σ_Z must remain 0")
    check(claim.evaluated_Pi_gammagamma_2L_P == 0, "claim evaluated Π_γγ must remain 0")
    check(claim.evaluated_Pi_gammaZ_2L_P == 0, "claim evaluated Π_γZ must remain 0")
    check(claim.OSW_delta_r_rem_APF_internal_P == 0, "claim Δr_rem APF-internal must remain 0")
    check(claim.source_certified_EW_coefficient_ledger_P == 0,
          "claim source-certified EW coeff ledger must remain 0")

    # (b) TOY pass on all 4 channels.
    for ch in ["Sigma_W_2L", "Sigma_Z_2L", "Pi_gammagamma_2L", "Pi_gammaZ_2L"]:
        terms, cts, contract, forbid = toy_terms_for(ch)
        res = renormalize_self_energy(ch, terms, cts, contract, forbid)
        check(res.status.startswith("RENORMALIZED_SELF_ENERGY_ASSEMBLY_GATE_PASS"),
              f"{ch} toy gate status: {res.status}")
        check(res.residual_poles.is_finite(),
              f"{ch} residual poles must cancel: {res.residual_poles.asdict()}")
    # (c) Σ_W finite part is non-trivial in the toy.
    terms, cts, contract, forbid = toy_terms_for("Sigma_W_2L")
    res_W = renormalize_self_energy("Sigma_W_2L", terms, cts, contract, forbid)
    check(abs(res_W.finite_value) > 0,
          f"Σ_W TOY finite value should be non-trivial: {res_W.finite_value}")

    # (d) 8 refusal cases.
    _expect_refused("missing coefficient ledger",
                    lambda: renormalize_self_energy("Sigma_W_2L", terms, cts,
                                                    toy_contract("Sigma_W_2L", certified=False),
                                                    forbid))
    bad_contract_classes = RenormalizationContract(
        **{**contract.__dict__, "diagram_classes_declared": {"master_integral"}})
    _expect_refused("missing diagram class",
                    lambda: renormalize_self_energy("Sigma_W_2L", terms, cts,
                                                    bad_contract_classes, forbid))
    _expect_refused("uncancelled poles",
                    lambda: renormalize_self_energy("Sigma_W_2L", terms, [],
                                                    contract, forbid))
    _expect_refused("measured M_W forbidden input",
                    lambda: renormalize_self_energy(
                        "Sigma_W_2L", terms, cts, contract,
                        ForbiddenInputLedger(measured_M_W=True)))
    bad_cts = [Counterterm("fitted", PoleSeries(-1, -1, 0), fitted=True)]
    _expect_refused("fitted counterterm",
                    lambda: renormalize_self_energy("Sigma_W_2L", terms, bad_cts,
                                                    contract, forbid))
    bad_terms_label = list(terms)
    bad_terms_label[0] = MasterTerm("bad", "tadpole", PoleSeries(),
                                    diagram_class="tadpole", source_label="measured_M_W")
    _expect_refused("forbidden source label",
                    lambda: renormalize_self_energy("Sigma_W_2L", bad_terms_label, cts,
                                                    contract, forbid))
    bad_terms_red = list(terms)
    bad_terms_red[2] = MasterTerm("bad_B0xB0", "two_point_5line",
                                  PoleSeries(0.25, -0.25, -0.75), coefficient=4.0,
                                  diagram_class="gauge_boson", irreducible=False)
    _expect_refused("reducible B0×B0 smuggling",
                    lambda: renormalize_self_energy("Sigma_W_2L", bad_terms_red, cts,
                                                    contract, forbid))
    termsP, ctsP, contractP, forbidP = toy_terms_for("Pi_gammagamma_2L")
    bad_photon = RenormalizationContract(
        **{**contractP.__dict__, "ward_zero_momentum_normalized": False})
    _expect_refused("photon Ward declaration missing",
                    lambda: renormalize_self_energy("Pi_gammagamma_2L", termsP, ctsP,
                                                    bad_photon, forbidP))

    # (e) Honest non-claim flags.
    check(EXPORT_FLAGS["Export_phase2_EW_self_energy_assembly_gate_P"] == 1,
          "Phase-2 gate flag must be 1")
    check(EXPORT_FLAGS["Export_pole_cancellation_gate_P"] == 1,
          "pole-cancellation flag must be 1")
    check(EXPORT_FLAGS["Export_forbidden_input_guard_P"] == 1,
          "forbidden-input guard flag must be 1")
    check(EXPORT_FLAGS["Export_source_certified_EW_coefficient_ledger_P"] == 0,
          "source-certified EW coefficient ledger must remain 0")
    check(EXPORT_FLAGS["Export_evaluated_Sigma_W_2L_P"] == 0,
          "evaluated Σ_W must remain 0")
    check(EXPORT_FLAGS["Export_evaluated_Sigma_Z_2L_P"] == 0,
          "evaluated Σ_Z must remain 0")
    check(EXPORT_FLAGS["Export_evaluated_Pi_gammagamma_2L_P"] == 0,
          "evaluated Π_γγ must remain 0")
    check(EXPORT_FLAGS["Export_evaluated_Pi_gammaZ_2L_P"] == 0,
          "evaluated Π_γZ must remain 0")
    check(EXPORT_FLAGS["Export_OSW_delta_r_rem_APF_internal_P"] == 0,
          "OS-W Δr_rem must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False,
          "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger: "
              "Runtime contract schema + pole-cancellation algebra + "
              "forbidden-input guard + Ward declaration guard + reducible "
              "B0×B0 quarantine on 4-channel toy ledger (Σ_W, Σ_Z, Π_γγ, "
              "Π_γZ). 8 negative-case refusals enforced. NO physical SM "
              "self-energy, Δr, or M_W value banked. "
              "[P_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger; "
              "C_ew_two_loop_coefficient_ledger_pending]"),
        tier=4,
        epistemic="P_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v1 / "
            "APF_TWO_LOOP_PHASE2_EW_SELF_ENERGY_ASSEMBLY_GATE_v1. Five "
            "components: (a) PoleSeries Laurent record with addition, scaling, "
            "finite-part extraction; (b) RenormalizationContract schema "
            "declaring scheme, μ², finite-part convention, subtraction, gauge, "
            "tadpole convention, counterterm policy, source reference, Ward "
            "zero-momentum normalization, covariance ledger, and "
            "coefficient_ledger_certified flag; (c) MasterTerm with "
            "irreducible flag for B0×B0 quarantine on 5-line two-point; "
            "(d) ForbiddenInputLedger refusing measured_M_W / DIZET / ZFITTER "
            "/ target_interval / fitted_counterterm; (e) renormalize_self_energy() "
            "validates contract + terms + forbidden-input, assembles bare + "
            "counterterm Laurent, verifies pole cancellation, returns finite "
            "part. TOY ledger: 7 master terms per channel with manufactured "
            "pole structure, single counterterm cancels c_m2 + c_m1 → 0. "
            "All 4 EW channels pass at the toy. 8 refusal cases enforced: "
            "missing coefficient ledger, missing diagram class, uncancelled "
            "poles, measured-M_W input, fitted counterterm, forbidden source "
            "label, reducible B0×B0 smuggling, photon Ward missing."
        ),
        key_result=(
            "Phase-2 EW self-energy assembly gate algebra and contract schema "
            "implemented + 4-channel toy-ledger pass + 8 refusal cases enforced. "
            "Source-certified EW two-loop coefficient ledger is the explicit "
            "next gate. "
            "[P_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger; "
            "C_ew_two_loop_coefficient_ledger_pending]"
        ),
        dependencies=[
            "T_two_loop_phase2_master_interface_router_current_depth",
        ],
        cross_refs=[
            "T_BSY_one_loop_kappa_l_assembly_consistency_at_Denner_validated_inputs",
        ],
        artifacts={
            "channels_toy_passed": sorted(VALID_CHANNELS),
            "required_classes": {k: sorted(v) for k, v in REQUIRED_CLASSES.items()},
            "forbidden_source_tokens": sorted(FORBIDDEN_SOURCE_TOKENS),
            "refusal_cases_count": 8,
            "next_gate": "SOURCE_CERTIFIED_EW_TWO_LOOP_DIAGRAM_COEFFICIENT_LEDGER",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger":
        check_T_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
