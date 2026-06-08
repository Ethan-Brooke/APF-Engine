"""W_TRACE DIZET/ZFITTER acquisition and instrumentation sprint.

v15.9 (2026-05-09): converts the post-v15.8 W-route blocker into a concrete
external-code acquisition path.  The missing physical-export object remains a
reviewed per-row same-input Delta-r evaluator with covariance.  This module
identifies DIZET v6.45 / ZFITTER as the best available reviewed implementation
route, records the public source-access channels, defines the APF input deck and
instrumentation protocol, and splits the former monolithic blocker into two
sharper gates:

    * REVIEWED_SAME_INPUT_TOTAL_EVALUATOR
    * ROW_DECOMPOSITION_AND_COVARIANCE_PROTOCOL

Closed here:
    * DIZET v6.45 is admitted as a reviewed/public electroweak code candidate;
    * public acquisition channels are located (CPC/Mendeley DOI, Code Ocean,
      SANC/ZFITTER tarball pointer) but the code is not vendored here;
    * APF route input deck, run contract, flag/toggle plan, and covariance
      protocol are specified;
    * W route upgrades from a vague evaluator blocker to an executable external
      acquisition/instrumentation plan.

Still open here:
    * no compiled DIZET run was performed inside this repository;
    * no DIZET output table is imported;
    * no physical on-shell W export is enabled.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_same_input_evaluator_closeout import (
    FIRST_FAILED_GATE as V158_FIRST_FAILED_GATE,
    PHYSICAL_EXPORT_STATUS,
    terminal_report as v158_terminal_report,
    terminal_numerics as v158_terminal_numerics,
    check_T_w_same_input_evaluator_closeout_bank_closure as _check_v158,
)
from apf.w_trace_delta_r_route_input_evaluation import (
    APF_DELTA_R_TARGET,
    M_W_TRACE_GEV,
    route_input_point,
    covariance_summary,
)
from apf.w_trace_delta_r_transport_buildout import dMW_dDelta_r, mw_from_delta_r
from apf.w_trace_acfw_delta_r_extraction_attempt import EXTRACTION_INPUTS

STATUS = "P_w_trace_dizet_acquisition_instrumentation"
VERSION = "v15_9"
PASS_STATUS = "W_TRACE_DIZET_ACQUISITION_INSTRUMENTATION_PASS"
TITLE = "W_TRACE DIZET/ZFITTER acquisition and instrumentation sprint"
PAYLOAD_ID = "W_TRACE_DIZET_ACQUISITION_INSTRUMENTATION_v15_9"

OLD_MONOLITHIC_GATE = "REVIEWED_PER_ROW_SAME_INPUT_EVALUATOR_WITH_COVARIANCE"
TOTAL_EVALUATOR_GATE = "REVIEWED_SAME_INPUT_TOTAL_EVALUATOR"
ROW_COVARIANCE_GATE = "ROW_DECOMPOSITION_AND_COVARIANCE_PROTOCOL"
ROUTE_STATUS = "P_external_code_acquisition_path_located_not_yet_executed"
DIZET_ROUTE_STATUS = "P_candidate_reviewed_same_input_total_evaluator_source_path"
PHYSICAL_EXPORT_GATE_STATUS = "OPEN_BLOCKED_PENDING_DIZET_RUN_AND_ROW_PROTOCOL"

APF_INPUT_POINT_ID = "APF_TRACE_ON_SHELL_ROUTE_INPUT_POINT_v15_7_REUSED"

DIZET_DEFAULT_FLAGS: Tuple[Tuple[str, Any], ...] = (
    ("IHVP", 5), ("IAMT4", 8), ("IQCD", 3), ("IMOMS", 1), ("IMASS", 0),
    ("ISCRE", 0), ("IALEM", 3), ("IMASK", 0), ("ISCAL", 0), ("IBARB", 2),
    ("IFTJR", 1), ("IFACR", 0), ("IFACT", 0), ("IHIGS", 0), ("IAFMT", 3),
    ("IEWLC", 1), ("ICZAK", 1), ("IHIG2", 0), ("IALE2", 3), ("IGFER", 2),
    ("IDDZZ", 1), ("IAMW2", 0), ("ISFSR", 1), ("IDMWW", 0), ("IDSWW", 0),
    ("IBAIKOV", 2012),
)

@dataclass(frozen=True)
class SourceChannel:
    channel_id: str
    source_family: str
    access_mode: str
    located: bool
    locally_vendored: bool
    compile_ready_here: bool
    license_or_terms: str
    allowed_role: str
    blocker: str
    notes: str

@dataclass(frozen=True)
class DIZETCapability:
    capability_id: str
    capability: str
    support_status: str
    evidence_role: str
    apf_gate_impact: str

@dataclass(frozen=True)
class APFInputDeckRow:
    name: str
    value: float
    units: str
    source: str
    allowed_for_run: bool
    notes: str

@dataclass(frozen=True)
class InstrumentationStep:
    step_id: str
    action: str
    expected_output: str
    pass_condition: str
    failure_status: str

@dataclass(frozen=True)
class ToggleRow:
    bucket: str
    candidate_flags: Tuple[str, ...]
    expected_delta_object: str
    row_quality: str
    covariance_source: str
    admitted_for_physical_export_now: bool

@dataclass(frozen=True)
class GateSplitRow:
    gate: str
    status: str
    closed_here: bool
    unlock_condition: str
    claim_boundary: str


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)


def _digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(obj).encode("utf-8")).hexdigest()


def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed), "status": "PASS" if passed else "FAIL", "epistemic": STATUS}
    row.update(extra)
    return row


def _passed(row: Any) -> bool:
    return bool(isinstance(row, Mapping) and (row.get("passed") is True or row.get("status") in ("PASS", "P")))


def source_channels() -> Tuple[SourceChannel, ...]:
    return (
        SourceChannel(
            channel_id="CPC_MENDELEY_DIZET_6_45",
            source_family="DIZET v6.45 program files",
            access_mode="CPC Library / Mendeley Data DOI 10.17632/2fr58v92xc.1",
            located=True,
            locally_vendored=False,
            compile_ready_here=False,
            license_or_terms="GPLv3 according to CPC program summary",
            allowed_role="primary acquisition channel for reviewed/public code",
            blocker="NOT_DOWNLOADED_OR_HASHED_IN_THIS_REPOSITORY",
            notes="The ScienceDirect/CPC program summary identifies DIZET v6.45, GPLv3, Fortran 77/90, CPC program-file DOI and Code Ocean capsule.",
        ),
        SourceChannel(
            channel_id="CODE_OCEAN_0198682",
            source_family="DIZET v6.45 Code Ocean capsule",
            access_mode="Code Ocean capsule 0198682",
            located=True,
            locally_vendored=False,
            compile_ready_here=False,
            license_or_terms="external capsule access; verify license on acquisition",
            allowed_role="reproducibility/acquisition mirror",
            blocker="CAPSULE_NOT_FETCHED_IN_THIS_ENVIRONMENT",
            notes="Candidate route for acquiring the runnable artifact or comparing outputs after local acquisition.",
        ),
        SourceChannel(
            channel_id="SANC_ZFITTER_DIZET_TGZ",
            source_family="SANC/ZFITTER DIZET_v6.45.tgz pointer",
            access_mode="official ZFITTER project page download pointer",
            located=True,
            locally_vendored=False,
            compile_ready_here=False,
            license_or_terms="respect CPC/ZFITTER conditions and DIZET package README",
            allowed_role="source tarball pointer and project provenance",
            blocker="TARBALL_NOT_FETCHED_IN_THIS_ENVIRONMENT",
            notes="The SANC/ZFITTER page identifies DIZET v6.45 (December 2019), authorship, and a tgz download pointer.",
        ),
        SourceChannel(
            channel_id="ZFITTER_6_42_CONTEXT",
            source_family="ZFITTER v6.42 / DIZET stand-alone library context",
            access_mode="CPC/ZFITTER documentation",
            located=True,
            locally_vendored=False,
            compile_ready_here=False,
            license_or_terms="CPC non-profit/ZFITTER historical terms for old versions; verify for any package used",
            allowed_role="capability and interface history",
            blocker="NOT_THE_TARGET_VERSION_FOR_V15_9",
            notes="ZFITTER documentation says DIZET can be used stand-alone and calculates W mass and electroweak radiative corrections.",
        ),
    )


def dizet_capabilities() -> Tuple[DIZETCapability, ...]:
    return (
        DIZETCapability("CAP1", "state-of-the-art electroweak/QCD radiative-correction library", "SUPPORTED_BY_CPC_SUMMARY", "reviewed code family", TOTAL_EVALUATOR_GATE),
        DIZETCapability("CAP2", "Fortran 77/90 GPLv3 program package with CPC program files", "SUPPORTED_BY_CPC_SUMMARY", "acquirable implementation", TOTAL_EVALUATOR_GATE),
        DIZETCapability("CAP3", "stand-alone DIZET library path independent of full ZFITTER", "SUPPORTED_BY_ZFITTER_DOCS", "runnable evaluator candidate", TOTAL_EVALUATOR_GATE),
        DIZETCapability("CAP4", "on-mass-shell two-loop electroweak corrections and pseudo-observables over input ranges", "SUPPORTED_BY_CPC_SUMMARY", "same-input total evaluator candidate", TOTAL_EVALUATOR_GATE),
        DIZETCapability("CAP5", "DIZET/ZFITTER default benchmark flags and input parameters documented", "SUPPORTED_BY_CPC_BENCHMARK", "benchmark/deck validation", TOTAL_EVALUATOR_GATE),
        DIZETCapability("CAP6", "correction flags/toggles exist for option-driven instrumentation", "SUPPORTED_BY_DIZET_FLAG_LIST", "row-like differencing candidate", ROW_COVARIANCE_GATE),
        DIZETCapability("CAP7", "public docs do not promise APF row covariance or ACFW-row exposure", "BLOCKER_IDENTIFIED", "prevents physical export", ROW_COVARIANCE_GATE),
    )


def apf_input_deck() -> Tuple[APFInputDeckRow, ...]:
    p = route_input_point()
    return (
        APFInputDeckRow("ZMASS", p.M_Z_GeV, "GeV", "external PDG-style route input inherited from v15.7", True, "fixed Z mass for on-shell route"),
        APFInputDeckRow("WMASS", 0.0, "GeV", "DIZET solve-for-W convention", True, "do not provide observed M_W; require prediction mode"),
        APFInputDeckRow("APF_TRACE_MW_REFERENCE", float(M_W_TRACE_GEV), "GeV", "APF trace value, diagnostic only", False, "not to be passed as observed W input"),
        APFInputDeckRow("TMASS", float(EXTRACTION_INPUTS["m_t_GeV"]), "GeV", "declared route input inherited from v15.7", True, "top-mass route input for radiative corrections"),
        APFInputDeckRow("HMASS", float(EXTRACTION_INPUTS["M_H_GeV"]), "GeV", "declared route input inherited from v15.7", True, "Higgs-mass route input"),
        APFInputDeckRow("ALQED5", p.alpha_inverse, "dimensionless inverse alpha", "declared route input inherited from v15.7", True, "DIZET benchmark uses ALQED5 naming"),
        APFInputDeckRow("ALFAS", float(EXTRACTION_INPUTS["alpha_s_MZ"]), "dimensionless", "declared route input inherited from v15.7", True, "strong coupling route input"),
        APFInputDeckRow("DELTA_R_APF_TRACE_TARGET", float(APF_DELTA_R_TARGET), "dimensionless", "APF trace-derived target, diagnostic only", False, "not a DIZET input; compare after run"),
    )


def instrumentation_steps() -> Tuple[InstrumentationStep, ...]:
    return (
        InstrumentationStep("S1", "Acquire DIZET v6.45 from CPC/Mendeley or SANC tarball and record SHA256", "source archive + checksum", "archive hash recorded and license terms stored", "ACQUISITION_NOT_COMPLETE"),
        InstrumentationStep("S2", "Compile unmodified DIZET benchmark with documented default flags", "benchmark output", "benchmark reproduces published/default DIZET values within tolerance", "BENCHMARK_NOT_REPRODUCED"),
        InstrumentationStep("S3", "Run APF on-shell route deck with WMASS=0 prediction mode", "same-input total M_W/Delta-r output", "reviewed code returns total prediction without observed M_W input", "SAME_INPUT_TOTAL_NOT_EVALUATED"),
        InstrumentationStep("S4", "Toggle radiative-correction flags one class at a time", "row-like finite differences", "sum of toggled deltas reconstructs total within declared tolerance", "ROW_DECOMPOSITION_NOT_RECONSTRUCTED"),
        InstrumentationStep("S5", "Finite-difference allowed input covariance through DIZET total and toggled rows", "Jacobian and covariance matrices", "Delta-r and M_W covariance matrices positive semidefinite and documented", "COVARIANCE_NOT_CERTIFIED"),
        InstrumentationStep("S6", "Compare DIZET total against ACFW parametrized total at same deck", "cross-check residual", "residual falls inside source/theory tolerance", "TOTAL_EVALUATOR_CROSSCHECK_FAIL"),
        InstrumentationStep("S7", "Admit rows only if DIZET flags map to APF row ontology", "admission report", "row labels have counterterm/provenance and no inverse-fit inputs", "ROW_LABELS_NOT_APF_ADMISSIBLE"),
    )


def toggle_plan() -> Tuple[ToggleRow, ...]:
    return (
        ToggleRow("running_alpha_vacuum_polarization", ("IHVP", "IALEM", "IALE2"), "Delta-alpha / hadronic VP response", "reviewed-code finite difference; not ACFW analytic row", "input covariance plus flag systematics", False),
        ToggleRow("qcd_and_mixed_qcd_ew", ("IQCD", "IBAIKOV", "IAMT4"), "QCD and mixed EW-QCD response", "reviewed-code finite difference", "alpha_s and scheme toggle covariance", False),
        ToggleRow("fermionic_two_loop", ("IGFER", "IAMW2", "IEWLC"), "fermionic two-loop response proxy", "reviewed-code finite difference pending DIZET flag audit", "flag-difference covariance / theory nuisance", False),
        ToggleRow("bosonic_two_loop", ("ICZAK", "IHIG2", "IHIGS"), "bosonic two-loop response proxy", "reviewed-code finite difference pending DIZET flag audit", "flag-difference covariance / theory nuisance", False),
        ToggleRow("mass_scheme_and_width_conventions", ("IMOMS", "IMASS", "IDMWW", "IDSWW"), "scheme/definition response", "convention audit, not physical row", "discrete scheme uncertainty", False),
        ToggleRow("final_state_or_box_like_context", ("ISFSR", "IFACT", "IFACR"), "non-core observable/context flags", "expected not to unlock W export rows", "quarantine if irrelevant", False),
    )


def split_gates() -> Tuple[GateSplitRow, ...]:
    return (
        GateSplitRow(OLD_MONOLITHIC_GATE, "SPLIT_IN_V15_9", True, "replace by total-evaluator and row/covariance gates", "old single blocker is too coarse"),
        GateSplitRow(TOTAL_EVALUATOR_GATE, DIZET_ROUTE_STATUS, True, "acquire/compile DIZET and run APF deck", "reviewed same-input total evaluator source path is located, not yet executed"),
        GateSplitRow(ROW_COVARIANCE_GATE, "OPEN_PENDING_INSTRUMENTED_DIZET_RUN", False, "toggle rows, map flags to APF row ontology, build covariance", "row protocol still blocks physical export"),
        GateSplitRow("PHYSICAL_W_EXPORT", PHYSICAL_EXPORT_GATE_STATUS, False, "both split gates pass and export theorem reruns", "no final physical W export claim"),
    )


def acquisition_summary() -> Dict[str, Any]:
    channels = source_channels()
    caps = dizet_capabilities()
    gates = split_gates()
    exact_vendored = [c for c in channels if c.locally_vendored and c.compile_ready_here]
    total_gate_located = any(c.located and "DIZET" in c.source_family for c in channels)
    return {
        "status": STATUS,
        "version": VERSION,
        "payload_id": PAYLOAD_ID,
        "title": TITLE,
        "source_channels": tuple(asdict(c) for c in channels),
        "capabilities": tuple(asdict(c) for c in caps),
        "apf_input_deck": tuple(asdict(r) for r in apf_input_deck()),
        "dizet_default_flags": DIZET_DEFAULT_FLAGS,
        "instrumentation_steps": tuple(asdict(s) for s in instrumentation_steps()),
        "toggle_plan": tuple(asdict(t) for t in toggle_plan()),
        "gate_split": tuple(asdict(g) for g in gates),
        "reviewed_total_evaluator_source_path_located": bool(total_gate_located),
        "compiled_dizet_available_in_repo": bool(exact_vendored),
        "dizet_run_performed": False,
        "row_covariance_protocol_complete": False,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "first_failed_gate_after_v15_9": "DIZET_CODE_NOT_YET_ACQUIRED_COMPILED_AND_RUN",
        "second_failed_gate_after_v15_9": ROW_COVARIANCE_GATE,
    }


def terminal_numerics() -> Dict[str, Any]:
    n = v158_terminal_numerics()
    sig = covariance_summary("APF_TRACE_TARGET_TOTAL", "rank_one_correlated_source_theory")
    return {
        "M_W_TRACE_GeV": n["M_W_TRACE_GeV"],
        "Delta_r_APF_TRACE": n["Delta_r_APF_TRACE"],
        "Delta_r_source_total_at_route_inputs": n["Delta_r_source_total_at_route_inputs"],
        "Delta_r_source_minus_APF": n["Delta_r_source_minus_APF"],
        "dM_W_dDelta_r_GeV": float(dMW_dDelta_r(float(APF_DELTA_R_TARGET))),
        "abs_M_W_gap_MeV": n["abs_M_W_gap_MeV"],
        "sigma_MW_MeV_rank_one": n["sigma_MW_MeV_rank_one"],
        "pull_source_minus_APF_sigma": n["pull_source_minus_APF_sigma"],
        "M_W_from_APF_Delta_r_GeV": float(mw_from_delta_r(float(APF_DELTA_R_TARGET))),
        "covariance_trace_sigma_delta_r": sig.sigma_delta_r,
    }


def terminal_claim() -> Dict[str, Any]:
    return {
        "allowed_claim": (
            "DIZET v6.45/ZFITTER is now the banked acquisition path for a reviewed same-input electroweak total evaluator; "
            "the W route remains blocked until the code is acquired, benchmarked, run on the APF deck, and instrumented for row/covariance decomposition."
        ),
        "forbidden_claim": "APF has now run DIZET and produced a physical W export.",
        "route_status": ROUTE_STATUS,
        "dizet_route_status": DIZET_ROUTE_STATUS,
        "physical_export_status": PHYSICAL_EXPORT_GATE_STATUS,
        "split_gates": (TOTAL_EVALUATOR_GATE, ROW_COVARIANCE_GATE),
    }


def closeout_report() -> Dict[str, Any]:
    artifact = {
        "status": STATUS,
        "version": VERSION,
        "payload_id": PAYLOAD_ID,
        "title": TITLE,
        "upstream_required": "P_w_same_input_evaluator_terminal_closeout",
        "upstream_v158_verdict": v158_terminal_report()["verdict"],
        "acquisition_summary": acquisition_summary(),
        "terminal_numerics": terminal_numerics(),
        "publication_claim": terminal_claim(),
        "terminal_verdict": "P_DIZET_acquisition_path_located__instrumentation_protocol_banked__not_physical_export",
    }
    artifact["payload_digest"] = _digest(artifact)
    return artifact


def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "version": VERSION, "title": TITLE, "report": closeout_report(), "verdict": closeout_report()["terminal_verdict"]}

# --- checks -----------------------------------------------------------------

def check_T_w_trace_dizet_acquisition_status_declared():
    r = closeout_report()
    ok = r["status"] == STATUS and r["version"] == VERSION and not r["acquisition_summary"]["physical_W_export_enabled"]
    return _res("status_declared", ok, status=r["status"], version=r["version"])


def check_T_w_trace_dizet_acquisition_depends_on_v158():
    d = _check_v158()
    return _res("depends_on_v158", _passed(d), upstream=d.get("status"), upstream_check=d.get("check"))


def check_T_w_trace_dizet_acquisition_old_gate_split():
    gates = split_gates()
    ok = gates[0].gate == OLD_MONOLITHIC_GATE and gates[0].closed_here and TOTAL_EVALUATOR_GATE in [g.gate for g in gates]
    return _res("old_gate_split", ok, gates=tuple(asdict(g) for g in gates))


def check_T_w_trace_dizet_acquisition_source_channels_located():
    rows = source_channels()
    ok = len(rows) == 4 and all(r.located for r in rows) and any(r.channel_id == "CPC_MENDELEY_DIZET_6_45" for r in rows)
    return _res("source_channels_located", ok, channels=tuple(asdict(r) for r in rows))


def check_T_w_trace_dizet_acquisition_no_local_vendor_claim():
    rows = source_channels()
    ok = all(not r.locally_vendored and not r.compile_ready_here for r in rows)
    return _res("no_local_vendor_claim", ok, channels=tuple((r.channel_id, r.locally_vendored, r.compile_ready_here) for r in rows))


def check_T_w_trace_dizet_acquisition_cpc_channel_is_primary():
    c = [r for r in source_channels() if r.channel_id == "CPC_MENDELEY_DIZET_6_45"][0]
    ok = "GPLv3" in c.license_or_terms and "primary" in c.allowed_role and c.blocker == "NOT_DOWNLOADED_OR_HASHED_IN_THIS_REPOSITORY"
    return _res("cpc_channel_is_primary", ok, channel=asdict(c))


def check_T_w_trace_dizet_acquisition_code_ocean_channel_recorded():
    c = [r for r in source_channels() if r.channel_id == "CODE_OCEAN_0198682"][0]
    ok = c.located and "capsule" in c.access_mode.lower()
    return _res("code_ocean_channel_recorded", ok, channel=asdict(c))


def check_T_w_trace_dizet_acquisition_sanc_tarball_channel_recorded():
    c = [r for r in source_channels() if r.channel_id == "SANC_ZFITTER_DIZET_TGZ"][0]
    ok = c.located and "TARBALL" in c.blocker
    return _res("sanc_tarball_channel_recorded", ok, channel=asdict(c))


def check_T_w_trace_dizet_acquisition_capabilities_nonempty():
    caps = dizet_capabilities()
    ok = len(caps) == 7 and any(c.apf_gate_impact == TOTAL_EVALUATOR_GATE for c in caps) and any(c.apf_gate_impact == ROW_COVARIANCE_GATE for c in caps)
    return _res("capabilities_nonempty", ok, capabilities=tuple(asdict(c) for c in caps))


def check_T_w_trace_dizet_acquisition_same_input_total_gate_located():
    a = acquisition_summary()
    ok = a["reviewed_total_evaluator_source_path_located"] and not a["compiled_dizet_available_in_repo"]
    return _res("same_input_total_gate_located", ok, summary={k: a[k] for k in ("reviewed_total_evaluator_source_path_located", "compiled_dizet_available_in_repo")})


def check_T_w_trace_dizet_acquisition_row_covariance_still_open():
    a = acquisition_summary()
    ok = not a["row_covariance_protocol_complete"] and a["second_failed_gate_after_v15_9"] == ROW_COVARIANCE_GATE
    return _res("row_covariance_still_open", ok, gate=a["second_failed_gate_after_v15_9"])


def check_T_w_trace_dizet_acquisition_apf_input_deck_has_required_fields():
    deck = apf_input_deck()
    names = [r.name for r in deck]
    ok = len(deck) == 8 and all(n in names for n in ("ZMASS", "WMASS", "TMASS", "HMASS", "ALQED5", "ALFAS"))
    return _res("apf_input_deck_has_required_fields", ok, deck=tuple(asdict(r) for r in deck))


def check_T_w_trace_dizet_acquisition_wmass_zero_prediction_mode():
    row = [r for r in apf_input_deck() if r.name == "WMASS"][0]
    ok = row.value == 0.0 and row.allowed_for_run and "prediction" in row.notes
    return _res("wmass_zero_prediction_mode", ok, row=asdict(row))


def check_T_w_trace_dizet_acquisition_apf_trace_not_input():
    rows = [r for r in apf_input_deck() if r.name in ("APF_TRACE_MW_REFERENCE", "DELTA_R_APF_TRACE_TARGET")]
    ok = len(rows) == 2 and all(not r.allowed_for_run for r in rows)
    return _res("apf_trace_not_input", ok, diagnostic_rows=tuple(asdict(r) for r in rows))


def check_T_w_trace_dizet_acquisition_default_flags_captured():
    flags = dict(DIZET_DEFAULT_FLAGS)
    ok = len(flags) >= 25 and flags.get("IHVP") == 5 and flags.get("IAMT4") == 8 and flags.get("IBAIKOV") == 2012
    return _res("default_flags_captured", ok, flags=DIZET_DEFAULT_FLAGS)


def check_T_w_trace_dizet_acquisition_instrumentation_steps_complete():
    steps = instrumentation_steps()
    ok = len(steps) == 7 and steps[0].failure_status == "ACQUISITION_NOT_COMPLETE" and steps[-1].failure_status == "ROW_LABELS_NOT_APF_ADMISSIBLE"
    return _res("instrumentation_steps_complete", ok, steps=tuple(asdict(s) for s in steps))


def check_T_w_trace_dizet_acquisition_toggle_plan_has_core_buckets():
    rows = toggle_plan()
    buckets = [r.bucket for r in rows]
    ok = len(rows) == 6 and all(b in buckets for b in ("running_alpha_vacuum_polarization", "qcd_and_mixed_qcd_ew", "fermionic_two_loop", "bosonic_two_loop"))
    return _res("toggle_plan_has_core_buckets", ok, toggle_plan=tuple(asdict(r) for r in rows))


def check_T_w_trace_dizet_acquisition_toggle_rows_not_export_admitted():
    ok = all(not r.admitted_for_physical_export_now for r in toggle_plan())
    return _res("toggle_rows_not_export_admitted", ok)


def check_T_w_trace_dizet_acquisition_flag_mapping_uses_dizet_names():
    flags = {f for row in toggle_plan() for f in row.candidate_flags}
    known = set(dict(DIZET_DEFAULT_FLAGS))
    ok = len(flags & known) >= 12 and {"IHVP", "IALEM", "IQCD", "ICZAK", "IGFER"}.issubset(flags)
    return _res("flag_mapping_uses_dizet_names", ok, mapped_flags=tuple(sorted(flags)))


def check_T_w_trace_dizet_acquisition_numerics_preserved():
    n = terminal_numerics()
    ok = abs(n["Delta_r_source_minus_APF"] - 0.00020700271122760933) < 1e-15 and 3.0 < n["abs_M_W_gap_MeV"] < 4.0
    return _res("numerics_preserved", ok, numerics=n)


def check_T_w_trace_dizet_acquisition_mw_roundtrip_preserved():
    n = terminal_numerics()
    ok = abs(n["M_W_from_APF_Delta_r_GeV"] - n["M_W_TRACE_GeV"]) < 1e-10
    return _res("mw_roundtrip_preserved", ok, numerics=n)


def check_T_w_trace_dizet_acquisition_sensitivity_negative():
    n = terminal_numerics()
    ok = n["dM_W_dDelta_r_GeV"] < 0 and abs(n["dM_W_dDelta_r_GeV"] + 16.831147360479) < 1e-6
    return _res("sensitivity_negative", ok, derivative=n["dM_W_dDelta_r_GeV"])


def check_T_w_trace_dizet_acquisition_physical_export_locked():
    a = acquisition_summary()
    ok = not a["physical_W_export_enabled"] and not a["exports_physical_M_W"] and a["first_failed_gate_after_v15_9"] == "DIZET_CODE_NOT_YET_ACQUIRED_COMPILED_AND_RUN"
    return _res("physical_export_locked", ok, summary={k: a[k] for k in ("physical_W_export_enabled", "exports_physical_M_W", "first_failed_gate_after_v15_9")})


def check_T_w_trace_dizet_acquisition_claim_boundary_allowed():
    c = terminal_claim()
    ok = "not yet executed" in c["allowed_claim"] or c["physical_export_status"] == PHYSICAL_EXPORT_GATE_STATUS
    ok = ok and "has now run DIZET" in c["forbidden_claim"]
    return _res("claim_boundary_allowed", ok, claim=c)


def check_T_w_trace_dizet_acquisition_split_gate_status_exact():
    gates = {g.gate: g.status for g in split_gates()}
    ok = gates[TOTAL_EVALUATOR_GATE] == DIZET_ROUTE_STATUS and gates[ROW_COVARIANCE_GATE] == "OPEN_PENDING_INSTRUMENTED_DIZET_RUN"
    return _res("split_gate_status_exact", ok, gates=gates)


def check_T_w_trace_dizet_acquisition_acquisition_first_failed_gate_named():
    a = acquisition_summary()
    ok = a["first_failed_gate_after_v15_9"] == "DIZET_CODE_NOT_YET_ACQUIRED_COMPILED_AND_RUN"
    return _res("acquisition_first_failed_gate_named", ok, first_failed_gate=a["first_failed_gate_after_v15_9"])


def check_T_w_trace_dizet_acquisition_instrumentation_produces_export_conditions():
    steps = instrumentation_steps()
    needed = {"benchmark output", "same-input total M_W/Delta-r output", "row-like finite differences", "Jacobian and covariance matrices"}
    ok = needed.issubset({s.expected_output for s in steps})
    return _res("instrumentation_produces_export_conditions", ok, expected_outputs=tuple(s.expected_output for s in steps))


def check_T_w_trace_dizet_acquisition_license_terms_not_ignored():
    rows = source_channels()
    ok = any("GPLv3" in r.license_or_terms for r in rows) and all(r.license_or_terms for r in rows)
    return _res("license_terms_not_ignored", ok, terms=tuple((r.channel_id, r.license_or_terms) for r in rows))


def check_T_w_trace_dizet_acquisition_payload_digest_present():
    d = closeout_report()["payload_digest"]
    return _res("payload_digest_present", isinstance(d, str) and d.startswith("sha256:") and len(d) == 71, digest=d)


def check_T_w_trace_dizet_acquisition_terminal_verdict_exact():
    r = closeout_report()
    ok = r["terminal_verdict"] == "P_DIZET_acquisition_path_located__instrumentation_protocol_banked__not_physical_export"
    return _res("terminal_verdict_exact", ok, verdict=r["terminal_verdict"])


def check_T_w_trace_dizet_acquisition_report_contains_all_tables():
    r = acquisition_summary()
    ok = all(k in r for k in ("source_channels", "capabilities", "apf_input_deck", "instrumentation_steps", "toggle_plan", "gate_split"))
    return _res("report_contains_all_tables", ok, keys=tuple(r.keys()))


def check_T_w_trace_dizet_acquisition_no_dizet_run_claim():
    r = acquisition_summary()
    ok = r["dizet_run_performed"] is False and r["compiled_dizet_available_in_repo"] is False
    return _res("no_dizet_run_claim", ok, dizet_run_performed=r["dizet_run_performed"], compiled=r["compiled_dizet_available_in_repo"])


def check_T_w_trace_dizet_acquisition_route_status_named():
    c = terminal_claim()
    ok = c["route_status"] == ROUTE_STATUS and c["dizet_route_status"] == DIZET_ROUTE_STATUS
    return _res("route_status_named", ok, claim=c)


def check_T_w_trace_dizet_acquisition_channels_unique():
    ids = [c.channel_id for c in source_channels()]
    ok = len(ids) == len(set(ids))
    return _res("channels_unique", ok, ids=tuple(ids))


def check_T_w_trace_dizet_acquisition_steps_ordered():
    ids = [s.step_id for s in instrumentation_steps()]
    ok = ids == ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
    return _res("steps_ordered", ok, ids=tuple(ids))


def check_T_w_trace_dizet_acquisition_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_dizet_acquisition_bank_closure"]
    ok = all(_passed(r) for r in rows)
    return _res("bank_closure", ok, passed_count=sum(_passed(r) for r in rows), total=len(rows))


_CHECKS: Dict[str, Any] = {
    name: obj for name, obj in globals().items()
    if name.startswith("check_T_w_trace_dizet_acquisition_") and callable(obj)
}


def register(registry: MutableMapping[str, Any]) -> None:
    registry.update(_CHECKS)


def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:  # pragma: no cover
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {"passed": ok, "status": PASS_STATUS if ok else PASS_STATUS.replace("_PASS", "_FAIL"), "checks": rows, "report": terminal_report()}


if __name__ == "__main__":
    out = run_all()
    print(out["status"])
    for row in out["checks"]:
        print(("PASS" if row["passed"] else "FAIL"), row["name"])
    raise SystemExit(0 if out["passed"] else 1)
