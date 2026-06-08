"""APF-native two-loop Phase-2 EW coefficient-ledger audit gate (SCAFFOLD ONLY) — Tier-4.

Schema + audit gate for the source-certified electroweak two-loop diagram
coefficient ledger that downstream physical promotion requires. The schema
defines the structural fields a physical coefficient row must populate; the
auditor checks schema integrity, per-channel diagram-class coverage,
master-basis mapping, source certification, and forbidden-input guards.

The pack ships TWO test ledgers:

  * `make_placeholder_ledger()` — schema-complete scaffold with
    `source_certified=False` on every row. Passes schema + class coverage +
    master-basis gates but does NOT pass physical promotion (correct: it is
    a placeholder, not a physical coefficient ledger).
  * `make_toy_certified_ledger()` — schema-complete with `source_certified=True`
    on every row. Passes the physical promotion gate at TOY grade only.
    Used to verify that a fully populated ledger could pass.

The auditor returns `LedgerAuditResult` with:
  * `schema_pass` — all rows valid against `CoefficientRow.validate_schema()`;
  * `class_coverage_pass` — all 4 channels (Σ_W, Σ_Z, Π_γγ, Π_γZ) cover their
    `REQUIRED_CLASSES`;
  * `master_basis_pass` — all rows map to valid `VALID_MASTER_BASIS` entries;
  * `source_certification_pass` — all rows source-certified and not placeholder;
  * `physical_promotion_allowed` — conjunction of all above + ledger-level
    `source_certified_physical` flag;
  * `status` — string with `_PHYSICAL_IMPORT_PASS` only when all gates pass.

Forbidden-input refusal tokens (extends OSW connector list with `inverse_fit`,
`posthoc_tuning`): scanned across `row_id + coefficient_expression +
source_reference + equation_label + covariance_ledger`.

Reducible B0×B0 stand-in quarantine on two-point-5line topology.

Honest non-claims preserved verbatim:
  * Export_source_certified_EW_two_loop_coefficient_ledger = 0
  * Export_evaluated_EW_two_loop_self_energies = 0
  * Export_EW_physical_finite_part_values = 0
  * Export_OSW_delta_r_rem_APF_internal = 0

The deliberately-named next gate: replace placeholder rows with
source-certified physical coefficient rows carrying equation / table
references and covariance ledgers; the auditor then transitions the ledger
status from `..._SCHEMA_AND_COVERAGE_PASS__PHYSICAL_SOURCE_OPEN` to
`..._PHYSICAL_IMPORT_PASS`.

Sibling APF_TWO_LOOP_PHASE2_EW_COEFFICIENT_LEDGER_AUDIT_v2 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v3.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Set, Tuple

from apf.apf_utils import check, _result


# =============================================================================
# Source-certified kernel
# =============================================================================

VALID_CHANNELS = {"Sigma_W_2L", "Sigma_Z_2L", "Pi_gammagamma_2L", "Pi_gammaZ_2L"}
VALID_TOPOLOGIES = {"tadpole", "sunset", "two_point_5line", "counterterm",
                    "vertex_box", "ward_normalization", "mixing_renormalization"}
VALID_MASTER_BASIS = {
    "T_tadpole_scalar_Tier1",
    "S_sunset_DE_F0F1F2F3",
    "S_sunset_2D_finite_core",
    "B_two_point_5line_Euclidean",
    "B_two_point_DST_high_energy_M0M1M2",
    "B_two_point_BFT_one_mass",
    "CT_local_counterterm",
    "VB_vertex_box_family",
    "WARD_photon_zero_momentum",
    "MIX_gammaZ_renormalization",
}

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

FORBIDDEN_TOKENS = {
    "measured_M_W", "published_total_SM_M_W", "DIZET_aggregate", "ZFITTER_aggregate",
    "target_interval", "fit_counterterm", "fitted_counterterm",
    "inverse_fit", "posthoc_tuning",
}


class CoefficientLedgerError(ValueError):
    pass


@dataclass(frozen=True)
class ConventionBlock:
    scheme: str
    gauge: str
    finite_part_convention: str
    subtraction_prescription: str
    tadpole_convention: str
    mu2: float
    counterterm_policy: str

    def validate(self) -> None:
        for name in ["scheme", "gauge", "finite_part_convention",
                     "subtraction_prescription", "tadpole_convention",
                     "counterterm_policy"]:
            val = getattr(self, name)
            if not isinstance(val, str) or not val.strip():
                raise CoefficientLedgerError(f"missing convention field: {name}")
        if self.mu2 <= 0:
            raise CoefficientLedgerError("mu2 must be positive")
        if "fit" in self.counterterm_policy.lower():
            raise CoefficientLedgerError("counterterm policy must not be fitted")


@dataclass(frozen=True)
class CoefficientRow:
    row_id: str
    channel: str
    diagram_class: str
    topology: str
    master_basis: str
    coefficient_expression: str
    source_reference: str
    equation_label: str
    convention: ConventionBlock
    covariance_ledger: str
    source_certified: bool
    placeholder: bool = False
    target_observable_consumed: bool = False
    fitted_coefficient: bool = False
    reducible_product_standin: bool = False

    def validate_schema(self) -> None:
        for name in ["row_id", "diagram_class", "coefficient_expression",
                     "source_reference", "equation_label", "covariance_ledger"]:
            val = getattr(self, name)
            if not isinstance(val, str) or not val.strip():
                raise CoefficientLedgerError(
                    f'row {self.row_id or "<missing>"}: missing field {name}')
        if self.channel not in VALID_CHANNELS:
            raise CoefficientLedgerError(
                f"row {self.row_id}: invalid channel {self.channel}")
        if self.topology not in VALID_TOPOLOGIES:
            raise CoefficientLedgerError(
                f"row {self.row_id}: invalid topology {self.topology}")
        if self.master_basis not in VALID_MASTER_BASIS:
            raise CoefficientLedgerError(
                f"row {self.row_id}: invalid master basis {self.master_basis}")
        self.convention.validate()
        haystack = " ".join([self.row_id, self.coefficient_expression,
                             self.source_reference, self.equation_label,
                             self.covariance_ledger])
        if any(tok in haystack for tok in FORBIDDEN_TOKENS):
            raise CoefficientLedgerError(
                f"row {self.row_id}: forbidden source/input token")
        if self.target_observable_consumed:
            raise CoefficientLedgerError(
                f"row {self.row_id}: target observable consumed")
        if self.fitted_coefficient:
            raise CoefficientLedgerError(
                f"row {self.row_id}: fitted coefficient refused")
        if self.topology == "two_point_5line" and self.reducible_product_standin:
            raise CoefficientLedgerError(
                f"row {self.row_id}: reducible B0xB0 stand-in refused")


@dataclass(frozen=True)
class CoefficientLedger:
    ledger_id: str
    rows: Tuple[CoefficientRow, ...]
    declared_channels: Tuple[str, ...]
    source_certified_physical: bool
    notes: str = ""

    def rows_for(self, channel: str) -> List[CoefficientRow]:
        return [r for r in self.rows if r.channel == channel]


@dataclass(frozen=True)
class LedgerAuditResult:
    ledger_id: str
    schema_pass: bool
    class_coverage_pass: bool
    master_basis_pass: bool
    source_certification_pass: bool
    physical_promotion_allowed: bool
    status: str
    failures: Tuple[str, ...]

    def asdict(self) -> Dict[str, object]:
        return asdict(self)


def audit_ledger(ledger: CoefficientLedger, *, require_physical: bool = False
                 ) -> LedgerAuditResult:
    failures: List[str] = []
    try:
        if not ledger.ledger_id.strip():
            raise CoefficientLedgerError("missing ledger_id")
        if not ledger.rows:
            raise CoefficientLedgerError("empty coefficient ledger")
        declared = set(ledger.declared_channels)
        if declared != VALID_CHANNELS:
            raise CoefficientLedgerError(
                "declared channel set must equal all four Phase-2 channels")
        for row in ledger.rows:
            row.validate_schema()
    except CoefficientLedgerError as e:
        failures.append(str(e))
    schema_pass = not failures

    class_coverage_pass = False
    if schema_pass:
        missing: Dict[str, Set[str]] = {}
        for ch in VALID_CHANNELS:
            seen = {r.diagram_class for r in ledger.rows_for(ch)}
            m = REQUIRED_CLASSES[ch] - seen
            if m:
                missing[ch] = m
        if missing:
            failures.append("diagram class coverage missing: " +
                            "; ".join(f"{ch}:{sorted(vals)}" for ch, vals in missing.items()))
        class_coverage_pass = not missing

    master_basis_pass = schema_pass and all(
        r.master_basis in VALID_MASTER_BASIS for r in ledger.rows)
    if not master_basis_pass:
        failures.append("master-basis mapping failure")

    source_certification_pass = schema_pass and all(
        r.source_certified and not r.placeholder for r in ledger.rows)
    if not source_certification_pass:
        failures.append("not all rows are non-placeholder source-certified physical rows")

    physical_promotion_allowed = bool(
        schema_pass and class_coverage_pass and master_basis_pass
        and source_certification_pass and ledger.source_certified_physical)
    if require_physical and not physical_promotion_allowed:
        failures.append("physical promotion requested but source-certified physical ledger is absent")

    if physical_promotion_allowed:
        status = "EW_COEFFICIENT_LEDGER_PHYSICAL_IMPORT_PASS"
    elif schema_pass and class_coverage_pass and master_basis_pass:
        status = "EW_COEFFICIENT_LEDGER_SCHEMA_AND_COVERAGE_PASS__PHYSICAL_SOURCE_OPEN"
    else:
        status = "EW_COEFFICIENT_LEDGER_AUDIT_FAIL"

    return LedgerAuditResult(ledger.ledger_id, schema_pass, class_coverage_pass,
                             master_basis_pass, source_certification_pass,
                             physical_promotion_allowed, status, tuple(failures))


def _conv() -> ConventionBlock:
    return ConventionBlock(
        scheme="declared_OS_like_symbolic_not_physics",
        gauge="R_xi_declared",
        finite_part_convention="finite_part_after_Laurent_pole_subtraction",
        subtraction_prescription="declared_symbolic_subtraction",
        tadpole_convention="explicit_tadpole_counterterm_ledger",
        mu2=91.1876 ** 2,
        counterterm_policy="source_certified_counterterm_policy",
    )


_MASTER_FOR_CLASS = {
    "tadpole": "T_tadpole_scalar_Tier1",
    "counterterm": "CT_local_counterterm",
    "ward_normalization": "WARD_photon_zero_momentum",
    "mixing_renormalization": "MIX_gammaZ_renormalization",
    "vertex_box": "VB_vertex_box_family",
    "master_integral": "S_sunset_DE_F0F1F2F3",
    "fermion": "B_two_point_5line_Euclidean",
    "gauge_boson": "B_two_point_5line_Euclidean",
    "ghost": "S_sunset_DE_F0F1F2F3",
    "goldstone": "S_sunset_DE_F0F1F2F3",
    "higgs": "S_sunset_2D_finite_core",
    "charged_fermion": "B_two_point_5line_Euclidean",
    "charged_gauge": "B_two_point_5line_Euclidean",
    "scalar": "S_sunset_2D_finite_core",
}

_TOPOLOGY_FOR_CLASS = {
    "tadpole": "tadpole",
    "counterterm": "counterterm",
    "ward_normalization": "ward_normalization",
    "mixing_renormalization": "mixing_renormalization",
    "vertex_box": "vertex_box",
    "master_integral": "sunset",
    "fermion": "two_point_5line",
    "gauge_boson": "two_point_5line",
    "ghost": "sunset",
    "goldstone": "sunset",
    "higgs": "sunset",
    "charged_fermion": "two_point_5line",
    "charged_gauge": "two_point_5line",
    "scalar": "sunset",
}


def make_placeholder_ledger() -> CoefficientLedger:
    rows: List[CoefficientRow] = []
    for ch in sorted(VALID_CHANNELS):
        for cls in sorted(REQUIRED_CLASSES[ch]):
            rows.append(CoefficientRow(
                row_id=f"{ch}_{cls}_placeholder",
                channel=ch,
                diagram_class=cls,
                topology=_TOPOLOGY_FOR_CLASS.get(cls, "sunset"),
                master_basis=_MASTER_FOR_CLASS.get(cls, "S_sunset_DE_F0F1F2F3"),
                coefficient_expression=f"PLACEHOLDER_C[{ch},{cls}]",
                source_reference="SOURCE_TO_BE_IMPORTED_NOT_A_PHYSICAL_COEFFICIENT",
                equation_label=f"placeholder_eq_{ch}_{cls}",
                convention=_conv(),
                covariance_ledger="placeholder_covariance_slot_declared",
                source_certified=False,
                placeholder=True,
            ))
    return CoefficientLedger(
        "EW_COEFF_PLACEHOLDER_SCAFFOLD_v2", tuple(rows),
        tuple(sorted(VALID_CHANNELS)), False,
        notes="Schema-complete placeholder scaffold. Not a physical coefficient ledger.",
    )


def make_toy_certified_ledger() -> CoefficientLedger:
    rows: List[CoefficientRow] = []
    for ch in sorted(VALID_CHANNELS):
        for cls in sorted(REQUIRED_CLASSES[ch]):
            rows.append(CoefficientRow(
                row_id=f"{ch}_{cls}_toy",
                channel=ch,
                diagram_class=cls,
                topology=_TOPOLOGY_FOR_CLASS.get(cls, "sunset"),
                master_basis=_MASTER_FOR_CLASS.get(cls, "S_sunset_DE_F0F1F2F3"),
                coefficient_expression=f"toy_c_{ch}_{cls}",
                source_reference="toy_source_for_gate_testing_only",
                equation_label=f"toy_eq_{ch}_{cls}",
                convention=_conv(),
                covariance_ledger="toy_covariance_declared",
                source_certified=True,
                placeholder=False,
            ))
    return CoefficientLedger(
        "EW_COEFF_TOY_CERTIFIED_GATE_TEST_v2", tuple(rows),
        tuple(sorted(VALID_CHANNELS)), True,
        notes="Toy ledger used only to verify that a complete ledger could pass. Not physics.",
    )


@dataclass(frozen=True)
class CoefficientLedgerClaim:
    EW_coefficient_ledger_schema_P: int = 1
    EW_coefficient_ledger_audit_gate_P: int = 1
    EW_diagram_class_coverage_gate_P: int = 1
    EW_master_basis_mapping_gate_P: int = 1
    EW_forbidden_input_audit_P: int = 1
    EW_placeholder_ledger_scaffold_P: int = 1
    source_certified_EW_two_loop_coefficient_ledger_P: int = 0
    evaluated_EW_two_loop_self_energies_P: int = 0
    EW_physical_finite_part_values_P: int = 0
    OSW_delta_r_rem_APF_internal_P: int = 0


# =============================================================================
# Export flags + bank check
# =============================================================================

EXPORT_FLAGS = {
    "Export_EW_coefficient_ledger_schema_P": 1,
    "Export_EW_coefficient_ledger_audit_gate_P": 1,
    "Export_EW_diagram_class_coverage_gate_P": 1,
    "Export_EW_master_basis_mapping_gate_P": 1,
    "Export_EW_forbidden_input_audit_P": 1,
    "Export_EW_placeholder_ledger_scaffold_P": 1,
    "Export_source_certified_EW_two_loop_coefficient_ledger_P": 0,
    "Export_evaluated_EW_two_loop_self_energies_P": 0,
    "Export_EW_physical_finite_part_values_P": 0,
    "Export_OSW_delta_r_rem_APF_internal_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def _expect_refused(label: str, fn):
    try:
        fn()
    except CoefficientLedgerError:
        return
    raise AssertionError(f"{label}: ledger did NOT refuse as expected")


def check_T_two_loop_phase2_ew_coefficient_ledger_audit_scaffold_P():
    """T: EW coefficient-ledger audit gate (SCAFFOLD ONLY). Schema + class
    coverage + master-basis mapping + source certification + forbidden-input
    guards on placeholder + toy-certified ledgers. ~10 refusal cases.
    Placeholder scaffold reaches PHYSICAL_SOURCE_OPEN; toy-certified ledger
    reaches PHYSICAL_IMPORT_PASS at toy grade only. NO physical EW
    coefficient values banked.
    [P_two_loop_phase2_ew_coefficient_ledger_audit_scaffold;
     C_source_certified_ew_coefficient_ledger_pending]."""

    # (a) Claim flags.
    claim = CoefficientLedgerClaim()
    check(claim.EW_coefficient_ledger_schema_P == 1, "claim schema export must be 1")
    check(claim.source_certified_EW_two_loop_coefficient_ledger_P == 0,
          "claim source-certified physical ledger must remain 0")
    check(claim.evaluated_EW_two_loop_self_energies_P == 0,
          "claim evaluated EW self-energies must remain 0")

    # (b) Placeholder scaffold: schema + coverage pass, physical promotion fails.
    placeholder = make_placeholder_ledger()
    pa = audit_ledger(placeholder)
    check(pa.schema_pass, "placeholder schema pass")
    check(pa.class_coverage_pass, "placeholder class coverage pass")
    check(pa.master_basis_pass, "placeholder master-basis pass")
    check(pa.physical_promotion_allowed is False,
          f"placeholder must NOT be physically promoted: {pa.physical_promotion_allowed}")
    check(pa.status.endswith("PHYSICAL_SOURCE_OPEN"),
          f"placeholder status: {pa.status}")

    # (c) Toy-certified ledger: physical gate passes at TOY grade.
    physical = audit_ledger(make_toy_certified_ledger(), require_physical=True)
    check(physical.physical_promotion_allowed,
          f"toy-certified ledger should pass physical gate: {physical.failures}")
    check(physical.status == "EW_COEFFICIENT_LEDGER_PHYSICAL_IMPORT_PASS",
          f"toy-certified status: {physical.status}")

    # (d) Refusal cases.
    row = list(make_toy_certified_ledger().rows)[0]
    _expect_refused("missing_equation_label",
                    lambda: CoefficientRow(**{**row.__dict__, "equation_label": ""}).validate_schema())
    _expect_refused("forbidden_measured_M_W_token",
                    lambda: CoefficientRow(**{**row.__dict__,
                                              "source_reference": "measured_M_W"}).validate_schema())
    _expect_refused("forbidden_inverse_fit_token",
                    lambda: CoefficientRow(**{**row.__dict__,
                                              "equation_label": "inverse_fit"}).validate_schema())
    _expect_refused("target_consumption",
                    lambda: CoefficientRow(**{**row.__dict__,
                                              "target_observable_consumed": True}).validate_schema())
    _expect_refused("fitted_coefficient",
                    lambda: CoefficientRow(**{**row.__dict__,
                                              "fitted_coefficient": True}).validate_schema())
    _expect_refused("invalid_master_basis",
                    lambda: CoefficientRow(**{**row.__dict__,
                                              "master_basis": "B0xB0_fake"}).validate_schema())
    rows_toy = list(make_toy_certified_ledger().rows)
    tp = [r for r in rows_toy if r.topology == "two_point_5line"][0]
    _expect_refused("reducible_B0xB0_standin",
                    lambda: CoefficientRow(**{**tp.__dict__,
                                              "reducible_product_standin": True}).validate_schema())
    _expect_refused("missing_covariance_ledger",
                    lambda: CoefficientRow(**{**row.__dict__,
                                              "covariance_ledger": ""}).validate_schema())
    badconv = ConventionBlock(**{**row.convention.__dict__,
                                 "counterterm_policy": "fit_counterterm"})
    _expect_refused("fitted_counterterm_policy",
                    lambda: CoefficientRow(**{**row.__dict__,
                                              "convention": badconv}).validate_schema())
    # Ledger-level missing class coverage.
    short_rows = tuple(r for r in rows_toy if not (r.channel == "Sigma_W_2L"
                                                   and r.diagram_class == "fermion"))
    short = CoefficientLedger("short", short_rows, tuple(sorted(VALID_CHANNELS)), True)
    sa = audit_ledger(short)
    check(sa.class_coverage_pass is False,
          f"missing-class ledger should fail coverage: {sa.class_coverage_pass}")

    # (e) Honest non-claim flags.
    check(EXPORT_FLAGS["Export_EW_coefficient_ledger_schema_P"] == 1,
          "schema flag must be 1")
    check(EXPORT_FLAGS["Export_EW_coefficient_ledger_audit_gate_P"] == 1,
          "audit gate flag must be 1")
    check(EXPORT_FLAGS["Export_source_certified_EW_two_loop_coefficient_ledger_P"] == 0,
          "source-certified physical ledger must remain 0")
    check(EXPORT_FLAGS["Export_evaluated_EW_two_loop_self_energies_P"] == 0,
          "evaluated EW self-energies must remain 0")
    check(EXPORT_FLAGS["Export_EW_physical_finite_part_values_P"] == 0,
          "physical finite-part values must remain 0")
    check(EXPORT_FLAGS["Export_OSW_delta_r_rem_APF_internal_P"] == 0,
          "OS-W Δr_rem APF-internal must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_ew_coefficient_ledger_audit_scaffold: "
              "EW coefficient-ledger audit gate (SCAFFOLD ONLY). Schema + "
              "per-channel class coverage + master-basis mapping + source-"
              "certification + forbidden-input refusal. Placeholder scaffold "
              "reaches SCHEMA_AND_COVERAGE_PASS__PHYSICAL_SOURCE_OPEN; "
              "toy-certified ledger reaches PHYSICAL_IMPORT_PASS at TOY grade. "
              "10 refusal cases enforced. NO physical EW coefficient values, "
              "self-energies, or Δr_rem banked. "
              "[P_two_loop_phase2_ew_coefficient_ledger_audit_scaffold; "
              "C_source_certified_ew_coefficient_ledger_pending]"),
        tier=4,
        epistemic="P_two_loop_phase2_ew_coefficient_ledger_audit_scaffold",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v3 / "
            "APF_TWO_LOOP_PHASE2_EW_COEFFICIENT_LEDGER_AUDIT_v2. CoefficientRow "
            "schema fields: row_id, channel ∈ {Σ_W,Σ_Z,Π_γγ,Π_γZ}, "
            "diagram_class, topology ∈ {tadpole, sunset, two_point_5line, "
            "counterterm, vertex_box, ward_normalization, mixing_renormalization}, "
            "master_basis ∈ 10-element basis set including T_tadpole_scalar_Tier1, "
            "S_sunset_DE_F0F1F2F3, S_sunset_2D_finite_core, "
            "B_two_point_5line_Euclidean, B_two_point_DST_high_energy_M0M1M2, "
            "B_two_point_BFT_one_mass, CT_local_counterterm, VB_vertex_box_family, "
            "WARD_photon_zero_momentum, MIX_gammaZ_renormalization. "
            "ConventionBlock declares scheme, gauge, finite-part convention, "
            "subtraction prescription, tadpole convention, μ², counterterm "
            "policy. audit_ledger() runs 4 gates (schema, class coverage, "
            "master-basis mapping, source certification) + ledger-level "
            "source_certified_physical flag. Forbidden-token scan over "
            "row_id + coefficient_expression + source_reference + "
            "equation_label + covariance_ledger refuses measured_M_W, "
            "DIZET/ZFITTER aggregates, target_interval, fit_counterterm, "
            "inverse_fit, posthoc_tuning, fitted_counterterm. Two-point-5line "
            "reducible-B0×B0 stand-in quarantine. Placeholder scaffold tests "
            "the schema+coverage path while preserving "
            "source_certified_physical=False; toy-certified ledger tests the "
            "full physical gate at TOY grade."
        ),
        key_result=(
            "EW coefficient-ledger audit gate + schema implemented; "
            "placeholder scaffold at PHYSICAL_SOURCE_OPEN; toy-certified at "
            "PHYSICAL_IMPORT_PASS (TOY grade); source-certified physical "
            "ledger OPEN. "
            "[P_two_loop_phase2_ew_coefficient_ledger_audit_scaffold; "
            "C_source_certified_ew_coefficient_ledger_pending]"
        ),
        dependencies=[
            "T_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger",
            "T_two_loop_phase2_osw_deltar_connector_refusal_toy",
        ],
        cross_refs=[],
        artifacts={
            "valid_channels": sorted(VALID_CHANNELS),
            "valid_topologies": sorted(VALID_TOPOLOGIES),
            "valid_master_basis": sorted(VALID_MASTER_BASIS),
            "required_classes": {k: sorted(v) for k, v in REQUIRED_CLASSES.items()},
            "forbidden_tokens": sorted(FORBIDDEN_TOKENS),
            "refusal_cases_count": 10,
            "next_gate": "replace placeholder rows with source-certified physical coefficient rows",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_ew_coefficient_ledger_audit_scaffold":
        check_T_two_loop_phase2_ew_coefficient_ledger_audit_scaffold_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
