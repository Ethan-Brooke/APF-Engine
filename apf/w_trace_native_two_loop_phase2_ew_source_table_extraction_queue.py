"""APF-native two-loop Phase-2 EW source-table extraction queue (NO ROWS EXTRACTED) — Tier-4.

Concrete extraction queue naming the five literature source families a future
Phase-2 EW coefficient-ledger pack must consult. The queue exists ONLY as a
discipline gate — it does NOT promote any electroweak two-loop coefficient
and explicitly refuses pre-promoted targets or queue-level claims that rows
have been extracted.

The five queued source families:

  * **ACFW 2004 W-mass** (`hep-ph/0311148`) — Awramik, Czakon, Freitas, Weiglein,
    "Precise prediction for the W-boson mass in the Standard Model". Primary
    role: aggregate-comparator + convention/decomposition target.
    `aggregate_only_guard=True` — must NOT be mistaken for a source-local
    coefficient row.
  * **ACF 2006 sin²θ_eff complete** (`hep-ph/0608099`) — Awramik, Czakon,
    Freitas, "Electroweak two-loop corrections to the effective weak mixing
    angle". Primary role: complete two-loop weak-mixing-angle form-factor
    source family. Equation-local rows extractable if convention-complete.
  * **ACFW 2004 sin²θ_eff fermionic** (`hep-ph/0408207`) — Awramik, Czakon,
    Freitas, Weiglein. Primary role: fermionic two-loop coefficient-map +
    master-reduction source family. Diagram-class rows + rational-coefficient
    map extractable.
  * **CAF 2006 sin²θ_eff bosonic** (`hep-ph/0602029`) — Czakon, Awramik,
    Freitas. Primary role: bosonic two-loop coefficient-map / W-Z expansion
    source family. Bosonic class rows, expansion coefficients, master-integral
    analytic forms extractable.
  * **Denner 2007 one-loop conventions** (`0709.1075`) — Denner. Primary role:
    one-loop convention/counterterm alignment ONLY; NOT a two-loop coefficient
    source. `aggregate_only_guard=True` — used for scheme/counterterm
    vocabulary alignment, never for Phase-2 coefficient rows.

The pack also ships a CSV template
(`physical_coefficient_ledger_template.csv`) for downstream extraction work,
with columns aligned to the coefficient-ledger schema.

Honest non-claims preserved verbatim:
  * Export_EW_source_table_rows_extracted = 0
  * Export_source_certified_EW_two_loop_coefficient_ledger = 0
  * Export_evaluated_EW_two_loop_self_energies = 0

The next gate (downstream of this queue): open the named source PDFs, fill
the CSV template with equation-local rows + convention blocks + covariance
ledgers, run the coefficient-ledger auditor, and only then plug the result
into the EW self-energy assembly gate and OS-W Δr connector.

Sibling APF_TWO_LOOP_PHASE2_EW_SOURCE_TABLE_EXTRACTION_QUEUE_v1 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v3.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Tuple

from apf.apf_utils import check, _result


# =============================================================================
# Source-certified kernel
# =============================================================================

REQUIRED_SOURCE_KEYS = {
    "ACFW_WMASS_2004",
    "ACF_SIN2EFF_COMPLETE_2006",
    "ACFW_SIN2EFF_FERMIONIC_2004",
    "CAF_SIN2EFF_BOSONIC_2006",
    "DENNER_ONE_LOOP_CONVENTIONS_2007",
}


class SourceQueueError(ValueError):
    pass


@dataclass(frozen=True)
class SourceTarget:
    key: str
    source_title: str
    authors: str
    arxiv_id: str
    primary_role: str
    extraction_task: str
    aggregate_only_guard: bool
    promoted_as_coefficient_source: bool = False

    def validate(self) -> None:
        for f in ["key", "source_title", "authors", "arxiv_id",
                  "primary_role", "extraction_task"]:
            if not getattr(self, f).strip():
                raise SourceQueueError(f'{self.key or "<missing>"}: missing {f}')
        if self.promoted_as_coefficient_source:
            raise SourceQueueError(
                f"{self.key}: queue target must not be pre-promoted")
        if "aggregate" in self.primary_role.lower() and not self.aggregate_only_guard:
            raise SourceQueueError(
                f"{self.key}: aggregate target missing guard")


@dataclass(frozen=True)
class SourceExtractionQueue:
    queue_id: str
    targets: Tuple[SourceTarget, ...]
    coefficient_rows_extracted: bool = False
    physical_ledger_promoted: bool = False

    def validate(self) -> None:
        if not self.queue_id.strip():
            raise SourceQueueError("missing queue_id")
        if self.coefficient_rows_extracted or self.physical_ledger_promoted:
            raise SourceQueueError(
                "queue pack must not claim extracted/promoted rows")
        keys = {t.key for t in self.targets}
        missing = REQUIRED_SOURCE_KEYS - keys
        if missing:
            raise SourceQueueError(
                "missing required source targets: " + ",".join(sorted(missing)))
        for t in self.targets:
            t.validate()
        denner = [t for t in self.targets if t.key == "DENNER_ONE_LOOP_CONVENTIONS_2007"][0]
        if (not denner.primary_role.lower().startswith("one-loop convention")
                or not denner.aggregate_only_guard):
            raise SourceQueueError(
                "Denner one-loop source must be convention-only guarded")

    def role_map(self) -> Dict[str, str]:
        return {t.key: t.primary_role for t in self.targets}


def default_queue() -> SourceExtractionQueue:
    return SourceExtractionQueue("EW_SOURCE_TABLE_EXTRACTION_QUEUE_v1", (
        SourceTarget(
            key="ACFW_WMASS_2004",
            source_title="Precise prediction for the W-boson mass in the Standard Model",
            authors="M. Awramik, M. Czakon, A. Freitas, G. Weiglein",
            arxiv_id="hep-ph/0311148",
            primary_role="aggregate-comparator and convention/decomposition target",
            extraction_task=(
                "inspect whether any non-aggregate self-energy / counterterm / "
                "finite-remainder rows are source-local enough for the "
                "coefficient ledger"),
            aggregate_only_guard=True,
        ),
        SourceTarget(
            key="ACF_SIN2EFF_COMPLETE_2006",
            source_title="Electroweak two-loop corrections to the effective weak mixing angle",
            authors="M. Awramik, M. Czakon, A. Freitas",
            arxiv_id="hep-ph/0608099",
            primary_role="complete two-loop weak-mixing-angle/form-factor source family",
            extraction_task=(
                "extract Delta-r / Delta-kappa / form-factor finite family rows "
                "if equation-local and convention-complete"),
            aggregate_only_guard=False,
        ),
        SourceTarget(
            key="ACFW_SIN2EFF_FERMIONIC_2004",
            source_title=(
                "Two-loop Fermionic Electroweak Corrections to the Effective "
                "Leptonic Weak Mixing Angle in the Standard Model"),
            authors="M. Awramik, M. Czakon, A. Freitas, G. Weiglein",
            arxiv_id="hep-ph/0408207",
            primary_role="fermionic two-loop coefficient-map and master-reduction source family",
            extraction_task=(
                "extract fermionic diagram-class rows and master-integral "
                "rational-coefficient map if exposed"),
            aggregate_only_guard=False,
        ),
        SourceTarget(
            key="CAF_SIN2EFF_BOSONIC_2006",
            source_title=(
                "Bosonic corrections to the effective leptonic weak mixing "
                "angle at the two-loop level"),
            authors="M. Czakon, M. Awramik, A. Freitas",
            arxiv_id="hep-ph/0602029",
            primary_role="bosonic two-loop coefficient-map / W-Z expansion source family",
            extraction_task=(
                "extract bosonic class rows, expansion coefficients, and "
                "master-integral analytic forms if source-local"),
            aggregate_only_guard=False,
        ),
        SourceTarget(
            key="DENNER_ONE_LOOP_CONVENTIONS_2007",
            source_title=(
                "Techniques for the calculation of electroweak radiative "
                "corrections at the one-loop level and results for W-physics "
                "at LEP200"),
            authors="A. Denner",
            arxiv_id="0709.1075",
            primary_role="one-loop convention/counterterm alignment only; not a two-loop coefficient source",
            extraction_task=(
                "use for scheme/counterterm vocabulary alignment, not for "
                "Phase-2 coefficient rows"),
            aggregate_only_guard=True,
        ),
    ))


@dataclass(frozen=True)
class SourceQueueClaim:
    EW_source_table_extraction_queue_P: int = 1
    EW_physical_coefficient_csv_template_P: int = 1
    EW_source_family_role_map_P: int = 1
    EW_source_table_rows_extracted_P: int = 0
    source_certified_EW_two_loop_coefficient_ledger_P: int = 0
    evaluated_EW_two_loop_self_energies_P: int = 0


# =============================================================================
# Export flags + bank check
# =============================================================================

EXPORT_FLAGS = {
    "Export_EW_source_table_extraction_queue_P": 1,
    "Export_EW_physical_coefficient_csv_template_P": 1,
    "Export_EW_source_family_role_map_P": 1,
    "Export_EW_source_table_rows_extracted_P": 0,
    "Export_source_certified_EW_two_loop_coefficient_ledger_P": 0,
    "Export_evaluated_EW_two_loop_self_energies_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def _expect_refused(label: str, fn):
    try:
        fn()
    except SourceQueueError:
        return
    raise AssertionError(f"{label}: queue did NOT refuse as expected")


def check_T_two_loop_phase2_ew_source_table_extraction_queue_P():
    """T: EW source-table extraction queue (NO ROWS EXTRACTED). Five named
    source-target families (ACFW 2004 W-mass aggregate guard, ACF 2006
    complete sin²θ_eff, ACFW 2004 fermionic, CAF 2006 bosonic, Denner 2007
    convention-only guard) with extraction tasks. Queue refuses pre-promoted
    targets, refuses claiming extracted rows, refuses missing required
    targets, and refuses Denner being miscategorized.
    [P_two_loop_phase2_ew_source_table_extraction_queue;
     C_ew_source_rows_not_extracted]."""

    # (a) Claim flags.
    claim = SourceQueueClaim()
    check(claim.EW_source_table_extraction_queue_P == 1,
          "claim queue export must be 1")
    check(claim.EW_source_table_rows_extracted_P == 0,
          "claim rows-extracted must remain 0")
    check(claim.source_certified_EW_two_loop_coefficient_ledger_P == 0,
          "claim source-certified ledger must remain 0")
    check(claim.evaluated_EW_two_loop_self_energies_P == 0,
          "claim evaluated EW self-energies must remain 0")

    # (b) Default queue validates.
    q = default_queue()
    q.validate()
    check(len(q.targets) == 5, f"queue target count: {len(q.targets)}")
    check(all(not t.promoted_as_coefficient_source for t in q.targets),
          "no queue target may be pre-promoted")
    check(q.role_map()["DENNER_ONE_LOOP_CONVENTIONS_2007"].startswith("one-loop convention"),
          "Denner must be convention-only role")
    keys_seen = {t.key for t in q.targets}
    check(keys_seen == REQUIRED_SOURCE_KEYS,
          f"queue must cover all 5 required source keys: missing={REQUIRED_SOURCE_KEYS - keys_seen}")

    # (c) Aggregate guards.
    acfw_wmass = [t for t in q.targets if t.key == "ACFW_WMASS_2004"][0]
    check(acfw_wmass.aggregate_only_guard is True,
          "ACFW 2004 W-mass must carry aggregate_only_guard=True")
    denner = [t for t in q.targets if t.key == "DENNER_ONE_LOOP_CONVENTIONS_2007"][0]
    check(denner.aggregate_only_guard is True,
          "Denner one-loop must carry aggregate_only_guard=True")

    # (d) Refusal cases.
    bad_target = SourceTarget(**{**q.targets[0].__dict__,
                                 "promoted_as_coefficient_source": True})
    _expect_refused("prepromoted_target",
                    lambda: SourceExtractionQueue("bad",
                                                  (bad_target,) + q.targets[1:]).validate())
    _expect_refused("rows_extracted_claim_in_queue_pack",
                    lambda: SourceExtractionQueue("bad", q.targets,
                                                  coefficient_rows_extracted=True).validate())
    _expect_refused("physical_ledger_promoted_claim_in_queue_pack",
                    lambda: SourceExtractionQueue("bad", q.targets,
                                                  physical_ledger_promoted=True).validate())
    _expect_refused("missing_required_source_target",
                    lambda: SourceExtractionQueue("bad", q.targets[:-1]).validate())
    # Aggregate role without guard refused
    bad_agg = SourceTarget(**{**q.targets[0].__dict__,
                              "aggregate_only_guard": False})
    _expect_refused("aggregate_role_without_guard",
                    lambda: bad_agg.validate())
    # Empty field refused
    bad_empty = SourceTarget(**{**q.targets[0].__dict__, "source_title": ""})
    _expect_refused("empty_source_title",
                    lambda: bad_empty.validate())

    # (e) Honest non-claim flags.
    check(EXPORT_FLAGS["Export_EW_source_table_extraction_queue_P"] == 1,
          "queue flag must be 1")
    check(EXPORT_FLAGS["Export_EW_physical_coefficient_csv_template_P"] == 1,
          "CSV template flag must be 1")
    check(EXPORT_FLAGS["Export_EW_source_family_role_map_P"] == 1,
          "role-map flag must be 1")
    check(EXPORT_FLAGS["Export_EW_source_table_rows_extracted_P"] == 0,
          "rows-extracted must remain 0")
    check(EXPORT_FLAGS["Export_source_certified_EW_two_loop_coefficient_ledger_P"] == 0,
          "source-certified physical ledger must remain 0")
    check(EXPORT_FLAGS["Export_evaluated_EW_two_loop_self_energies_P"] == 0,
          "evaluated EW self-energies must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False,
          "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_ew_source_table_extraction_queue: "
              "EW source-table extraction queue with five named literature "
              "source families (ACFW 2004 W-mass aggregate-guard, ACF 2006 "
              "complete sin²θ_eff, ACFW 2004 fermionic, CAF 2006 bosonic, "
              "Denner 2007 convention-only guard) + extraction tasks + role "
              "map. Queue refuses pre-promoted targets, claiming extracted "
              "rows, missing required targets, aggregate roles without guard, "
              "and empty schema fields. NO physical coefficient rows "
              "extracted. "
              "[P_two_loop_phase2_ew_source_table_extraction_queue; "
              "C_ew_source_rows_not_extracted]"),
        tier=4,
        epistemic="P_two_loop_phase2_ew_source_table_extraction_queue",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v3 / "
            "APF_TWO_LOOP_PHASE2_EW_SOURCE_TABLE_EXTRACTION_QUEUE_v1. "
            "SourceTarget record carries key, source_title, authors, arxiv_id, "
            "primary_role, extraction_task, aggregate_only_guard, "
            "promoted_as_coefficient_source flags. Default queue holds exactly "
            "the 5 source families needed for the EW coefficient-ledger import: "
            "(1) Awramik-Czakon-Freitas-Weiglein 2004 W-mass paper "
            "(hep-ph/0311148) — aggregate comparator + convention target, "
            "explicit aggregate_only_guard so the SM total M_W parametrization "
            "cannot smuggle in as a source-local coefficient; (2) "
            "Awramik-Czakon-Freitas 2006 complete sin²θ_eff (hep-ph/0608099) — "
            "complete weak-mixing-angle form-factor source family, "
            "equation-local rows extractable; (3) ACFW 2004 fermionic "
            "(hep-ph/0408207) — fermionic two-loop coefficient-map + "
            "master-reduction source; (4) CAF 2006 bosonic (hep-ph/0602029) — "
            "bosonic two-loop coefficient-map / W-Z expansion source; (5) "
            "Denner 2007 (0709.1075) — one-loop convention/counterterm "
            "alignment ONLY, hard aggregate_only_guard so it cannot be "
            "mistaken for a two-loop coefficient source. Queue refuses "
            "pre-promoted targets, claims of extracted rows or promoted "
            "physical ledger, missing required sources, aggregate roles "
            "without guard, and empty fields. Companion CSV template "
            "physical_coefficient_ledger_template.csv ships alongside in "
            "the sibling pack (columns aligned to CoefficientRow schema)."
        ),
        key_result=(
            "Five-source extraction queue with role map + CSV template + "
            "discipline refusals enforced. Queue is the gate before "
            "coefficient-ledger physical population. "
            "[P_two_loop_phase2_ew_source_table_extraction_queue; "
            "C_ew_source_rows_not_extracted]"
        ),
        dependencies=[
            "T_two_loop_phase2_ew_coefficient_ledger_audit_scaffold",
        ],
        cross_refs=[
            "T_two_loop_phase2_osw_deltar_connector_refusal_toy",
        ],
        artifacts={
            "required_source_keys": sorted(REQUIRED_SOURCE_KEYS),
            "queued_source_count": 5,
            "aggregate_guard_keys": [
                "ACFW_WMASS_2004",
                "DENNER_ONE_LOOP_CONVENTIONS_2007",
            ],
            "extractable_source_keys": [
                "ACF_SIN2EFF_COMPLETE_2006",
                "ACFW_SIN2EFF_FERMIONIC_2004",
                "CAF_SIN2EFF_BOSONIC_2006",
            ],
            "csv_template": "physical_coefficient_ledger_template.csv",
            "next_gate": "open source PDFs, fill template, run coefficient-ledger auditor",
            "refusal_cases_count": 6,
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_ew_source_table_extraction_queue":
        check_T_two_loop_phase2_ew_source_table_extraction_queue_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
