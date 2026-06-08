"""W_TRACE full electroweak-loop derivation closeout / next-theorem reduction.

v16.5 (2026-05-09): takes the v16.4 DIZET same-input total evaluator,
internal Delta-r row ledger, and row covariance, then asks the stronger question:
can APF now claim an internally derived full electroweak loop stack?  The answer
is deliberately split.  The W on-shell export candidate is closed by reviewed
same-input transport plus admitted DIZET rows; the *full APF-native loop
derivation* is not closed until APF supplies its own gauge-fixed action,
counterterm, loop-integral, two-loop master-integral, and uncertainty/covariance
construction rather than importing DIZET internals.

This module is therefore not another obstruction-only wrapper.  It is a theorem
reduction: it names the minimal APF-owned objects that would upgrade the result
from export-candidate to physical-final/full-loop-derived.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_dizet_row_admission_covariance import (
    PASS_STATUS as V16_4_PASS_STATUS,
    route_summary as v16_4_route_summary,
    DR_TOTAL as DIZET_DR_TOTAL,
    DIZET_MW_GEV,
    M_W_TRACE_GEV,
    DIZET_MINUS_APF_MEV,
    TOTAL_SIGMA_MW_MEV,
    PULL_INPUT_PLUS_THEORY,
    ADMITTED_ROWS,
    AUXILIARY_ROWS,
    covariance_is_psd,
)

STATUS = "P_w_trace_full_loop_derivation_closeout"
VERSION = "v16_5"
PASS_STATUS = "W_TRACE_FULL_LOOP_DERIVATION_CLOSEOUT_PASS"
TITLE = "W_TRACE full electroweak-loop derivation closeout and theorem reduction"
PAYLOAD_ID = "W_TRACE_FULL_LOOP_DERIVATION_CLOSEOUT_v16_5"
APF_VERSION = "16.5.0"

EXPORT_CANDIDATE_STATUS = "P_export_candidate_by_reviewed_same_input_transport"
FULL_LOOP_STATUS = "OPEN_NOT_APF_NATIVE_FULL_LOOP_DERIVATION"
FIRST_FAILED_GATE = "APF_NATIVE_COUNTERTERM_AND_LOOP_INTEGRAL_EVALUATOR"
UPGRADE_GATE = "APF_NATIVE_FULL_EW_LOOP_STACK_WITH_ROW_COVARIANCE"

@dataclass(frozen=True)
class LoopLayer:
    layer_id: str
    object: str
    status: str
    source_of_closure: str
    apf_native: bool
    blocker_if_open: str

LOOP_LAYERS: Tuple[LoopLayer, ...] = (
    LoopLayer("L0", "trace-sector W anchor M_W^APF-TRACE", "CLOSED", "APF trace-sector closure", True, ""),
    LoopLayer("L1", "on-shell route equation and Delta-r/M_W solver", "CLOSED", "APF route theorem + on-shell electroweak relation", True, ""),
    LoopLayer("L2", "reviewed same-input total electroweak evaluator", "CLOSED", "compiled DIZET v6.45 same-input run", False, ""),
    LoopLayer("L3", "implementation-exposed Delta-r channel ledger", "CLOSED", "DIZET SEARCH/NEWDR instrumentation", False, ""),
    LoopLayer("L4", "admitted row covariance and W-scale uncertainty", "CLOSED", "APF row-admission protocol over DIZET grid", True, "publication review of row admission protocol"),
    LoopLayer("L5", "APF-native gauge-fixed electroweak action and Feynman rules", "OPEN", "not yet supplied by APF loop derivation", True, "derive gauge fixing, ghost sector, vertices, propagators from APF action/internalization"),
    LoopLayer("L6", "APF-native one-loop counterterm/evaluator for Delta r", "OPEN", "not yet supplied by APF loop derivation", True, "derive W/Z/self-energy, charge, weak-angle, vertex/box counterterms and finite parts"),
    LoopLayer("L7", "APF-native two-loop fermionic/bosonic evaluator", "OPEN", "not yet supplied by APF loop derivation", True, "derive or reproduce FHWW/AC two-loop master-integral stack"),
    LoopLayer("L8", "APF-native mixed QCD/EW and higher-order remainder", "OPEN", "not yet supplied by APF loop derivation", True, "derive mixed alpha*alpha_s, alpha*alpha_s^2, leading top/Higgs higher terms"),
    LoopLayer("L9", "publication-grade row covariance from APF loop amplitudes", "OPEN", "not yet supplied by APF loop derivation", True, "propagate input/theory covariance from APF-owned rows rather than DIZET admission grid"),
)

@dataclass(frozen=True)
class TheoremReduction:
    gate_id: str
    required_object: str
    minimum_deliverable: str
    closes_status: str
    current_status: str

REDUCTION_GATES: Tuple[TheoremReduction, ...] = (
    TheoremReduction("G1_ACTION", "APF electroweak action/internalization", "gauge-fixed SU(2)xU(1) action with ghost/counterterm bookkeeping", "L5", "OPEN"),
    TheoremReduction("G2_ONE_LOOP", "one-loop Delta-r evaluator", "finite on-shell one-loop Delta-r decomposition matching DIZET/Denner conventions", "L6", "OPEN"),
    TheoremReduction("G3_TWO_LOOP", "two-loop fermionic/bosonic evaluator", "review-reproducible FHWW/AC row reproduction or APF-native equivalent", "L7", "OPEN"),
    TheoremReduction("G4_MIXED_HIGHER", "mixed QCD/EW and higher-order evaluator", "source-matched mixed terms and residual theory nuisance model", "L8", "OPEN"),
    TheoremReduction("G5_NATIVE_COV", "native row covariance", "Jacobian/covariance generated from APF-owned row functions", "L9", "OPEN"),
)

@dataclass(frozen=True)
class SafeClaim:
    name: str
    allowed: bool
    statement: str

SAFE_CLAIMS: Tuple[SafeClaim, ...] = (
    SafeClaim("trace_anchor", True, "APF supplies a W trace anchor at 80.362164334 GeV."),
    SafeClaim("reviewed_transport", True, "DIZET supplies a reviewed same-input on-shell transport evaluator at the APF route input point."),
    SafeClaim("export_candidate", True, "The W route is an export candidate, with APF/DIZET displacement about 1.09 sigma using the v16.4 covariance protocol."),
    SafeClaim("channel_ledger", True, "DIZET internals can be admitted as a stable APF transport ledger under the v16.4 protocol."),
    SafeClaim("full_loop_derived", False, "Do not claim APF has independently derived the full Standard Model electroweak loop stack."),
    SafeClaim("physical_final", False, "Do not claim final physical W export until APF-native loop rows or publication-reviewed equivalent are supplied."),
)

LOOP_TAXONOMY = {
    "one_loop": ("Delta-alpha/running charge", "rho/top weak-isospin correction", "one-loop bosonic finite part", "vertex/box/counterterm pieces"),
    "two_loop": ("complete fermionic two-loop", "complete bosonic two-loop", "renormalization-scheme matching"),
    "mixed_higher": ("alpha alpha_s", "alpha alpha_s^2", "leading top-enhanced higher orders", "unknown higher-order nuisance"),
    "apf_transport_rows_v16_4": tuple(r.name for r in ADMITTED_ROWS),
}


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


def loop_layer_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in LOOP_LAYERS)


def reduction_gate_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in REDUCTION_GATES)


def safe_claim_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in SAFE_CLAIMS)


def closed_layers() -> Tuple[LoopLayer, ...]:
    return tuple(x for x in LOOP_LAYERS if x.status == "CLOSED")


def open_layers() -> Tuple[LoopLayer, ...]:
    return tuple(x for x in LOOP_LAYERS if x.status == "OPEN")


def full_loop_native_closed() -> bool:
    return all(x.status == "CLOSED" for x in LOOP_LAYERS if x.layer_id in {"L5", "L6", "L7", "L8", "L9"})


def route_summary() -> Dict[str, Any]:
    return {
        "title": TITLE,
        "version": VERSION,
        "apf_version": APF_VERSION,
        "v16_4_dependency": V16_4_PASS_STATUS,
        "numerical_state": {
            "M_W_APF_TRACE_GeV": M_W_TRACE_GEV,
            "M_W_DIZET_same_input_GeV": DIZET_MW_GEV,
            "DIZET_minus_APF_MeV": DIZET_MINUS_APF_MEV,
            "sigma_input_plus_theory_MeV": TOTAL_SIGMA_MW_MEV,
            "pull_sigma": PULL_INPUT_PLUS_THEORY,
            "DIZET_Delta_r_total": DIZET_DR_TOTAL,
        },
        "route_status": EXPORT_CANDIDATE_STATUS,
        "full_loop_status": FULL_LOOP_STATUS,
        "first_failed_gate": FIRST_FAILED_GATE,
        "upgrade_gate": UPGRADE_GATE,
        "loop_layers": loop_layer_table(),
        "reduction_gates": reduction_gate_table(),
        "safe_claims": safe_claim_table(),
        "loop_taxonomy": LOOP_TAXONOMY,
        "decision": {
            "can_claim_export_candidate": True,
            "can_claim_full_apf_loop_derivation": full_loop_native_closed(),
            "next_minimal_push": "G2_ONE_LOOP: APF-native one-loop Delta-r evaluator in the DIZET/Denner on-shell convention",
            "paper_language": "The full loop is reduced, not solved from first principles: W is an export candidate by reviewed same-input transport, while APF-native electroweak loop derivation remains the next theorem program.",
        },
        "payload_digest": _digest([loop_layer_table(), reduction_gate_table(), safe_claim_table(), LOOP_TAXONOMY]),
    }


def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}

# checks ---------------------------------------------------------------------

def check_T_w_trace_full_loop_status_declared():
    return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v16_5")


def check_T_w_trace_full_loop_depends_on_v164():
    return _res("depends_on_v164", V16_4_PASS_STATUS.endswith("PASS"))


def check_T_w_trace_full_loop_v164_route_has_export_candidate():
    return _res("v164_route_has_export_candidate", "export candidate" in v16_4_route_summary()["claim_boundary"]["candidate_claim"])


def check_T_w_trace_full_loop_numerical_state_preserved():
    return _res("numerical_state_preserved", 80.35 < DIZET_MW_GEV < 80.37 and 80.36 < M_W_TRACE_GEV < 80.37)


def check_T_w_trace_full_loop_pull_preserved():
    return _res("pull_preserved", 1.0 < PULL_INPUT_PLUS_THEORY < 1.2)


def check_T_w_trace_full_loop_layers_nonempty():
    return _res("layers_nonempty", len(LOOP_LAYERS) == 10)


def check_T_w_trace_full_loop_closed_layers_exist():
    return _res("closed_layers_exist", len(closed_layers()) == 5)


def check_T_w_trace_full_loop_open_layers_exist():
    return _res("open_layers_exist", len(open_layers()) == 5)


def check_T_w_trace_full_loop_export_candidate_closed():
    return _res("export_candidate_closed", route_summary()["route_status"] == EXPORT_CANDIDATE_STATUS)


def check_T_w_trace_full_loop_native_full_loop_not_claimed():
    return _res("native_full_loop_not_claimed", route_summary()["full_loop_status"] == FULL_LOOP_STATUS and not full_loop_native_closed())


def check_T_w_trace_full_loop_first_failed_gate_exact():
    return _res("first_failed_gate_exact", route_summary()["first_failed_gate"] == FIRST_FAILED_GATE)


def check_T_w_trace_full_loop_upgrade_gate_exact():
    return _res("upgrade_gate_exact", route_summary()["upgrade_gate"] == UPGRADE_GATE)


def check_T_w_trace_full_loop_reduction_gates_five():
    return _res("reduction_gates_five", len(REDUCTION_GATES) == 5)


def check_T_w_trace_full_loop_reduction_gates_all_open():
    return _res("reduction_gates_all_open", all(g.current_status == "OPEN" for g in REDUCTION_GATES))


def check_T_w_trace_full_loop_action_gate_named():
    return _res("action_gate_named", REDUCTION_GATES[0].gate_id == "G1_ACTION")


def check_T_w_trace_full_loop_one_loop_gate_named():
    return _res("one_loop_gate_named", any(g.gate_id == "G2_ONE_LOOP" for g in REDUCTION_GATES))


def check_T_w_trace_full_loop_two_loop_gate_named():
    return _res("two_loop_gate_named", any(g.gate_id == "G3_TWO_LOOP" for g in REDUCTION_GATES))


def check_T_w_trace_full_loop_mixed_higher_gate_named():
    return _res("mixed_higher_gate_named", any(g.gate_id == "G4_MIXED_HIGHER" for g in REDUCTION_GATES))


def check_T_w_trace_full_loop_native_cov_gate_named():
    return _res("native_cov_gate_named", any(g.gate_id == "G5_NATIVE_COV" for g in REDUCTION_GATES))


def check_T_w_trace_full_loop_taxonomy_has_one_loop():
    return _res("taxonomy_has_one_loop", "one_loop" in LOOP_TAXONOMY and len(LOOP_TAXONOMY["one_loop"]) == 4)


def check_T_w_trace_full_loop_taxonomy_has_two_loop():
    return _res("taxonomy_has_two_loop", "two_loop" in LOOP_TAXONOMY and len(LOOP_TAXONOMY["two_loop"]) == 3)


def check_T_w_trace_full_loop_taxonomy_has_mixed_higher():
    return _res("taxonomy_has_mixed_higher", "mixed_higher" in LOOP_TAXONOMY and len(LOOP_TAXONOMY["mixed_higher"]) == 4)


def check_T_w_trace_full_loop_taxonomy_carries_v164_rows():
    return _res("taxonomy_carries_v164_rows", len(LOOP_TAXONOMY["apf_transport_rows_v16_4"]) == len(ADMITTED_ROWS))


def check_T_w_trace_full_loop_safe_claims_include_allowed_and_forbidden():
    return _res("safe_claims_include_allowed_and_forbidden", any(c.allowed for c in SAFE_CLAIMS) and any(not c.allowed for c in SAFE_CLAIMS))


def check_T_w_trace_full_loop_forbids_full_loop_claim():
    return _res("forbids_full_loop_claim", any(c.name == "full_loop_derived" and not c.allowed for c in SAFE_CLAIMS))


def check_T_w_trace_full_loop_allows_export_candidate_claim():
    return _res("allows_export_candidate_claim", any(c.name == "export_candidate" and c.allowed for c in SAFE_CLAIMS))


def check_T_w_trace_full_loop_dizet_rows_still_admitted():
    return _res("dizet_rows_still_admitted", len(ADMITTED_ROWS) == 3 and len(AUXILIARY_ROWS) >= 5)


def check_T_w_trace_full_loop_covariance_psd_preserved():
    return _res("covariance_psd_preserved", covariance_is_psd())


def check_T_w_trace_full_loop_decision_claims_candidate_not_native_full_loop():
    d = route_summary()["decision"]
    return _res("decision_claims_candidate_not_native_full_loop", d["can_claim_export_candidate"] is True and d["can_claim_full_apf_loop_derivation"] is False)


def check_T_w_trace_full_loop_next_push_is_one_loop():
    return _res("next_push_is_one_loop", route_summary()["decision"]["next_minimal_push"].startswith("G2_ONE_LOOP"))


def check_T_w_trace_full_loop_payload_digest_present():
    return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))


def check_T_w_trace_full_loop_report_contains_layers():
    return _res("report_contains_layers", len(route_summary()["loop_layers"]) == 10)


def check_T_w_trace_full_loop_report_contains_safe_claims():
    return _res("report_contains_safe_claims", len(route_summary()["safe_claims"]) == 6)


def check_T_w_trace_full_loop_no_raw_physical_final_claim():
    forbidden = [c for c in SAFE_CLAIMS if c.name == "physical_final"]
    return _res("no_raw_physical_final_claim", len(forbidden) == 1 and forbidden[0].allowed is False)


def check_T_w_trace_full_loop_closed_layers_include_dizet_total():
    return _res("closed_layers_include_dizet_total", any(x.layer_id == "L2" and x.status == "CLOSED" for x in LOOP_LAYERS))


def check_T_w_trace_full_loop_open_layers_include_counterterm():
    return _res("open_layers_include_counterterm", any(x.layer_id == "L6" and x.status == "OPEN" for x in LOOP_LAYERS))


def check_T_w_trace_full_loop_open_layers_include_two_loop():
    return _res("open_layers_include_two_loop", any(x.layer_id == "L7" and x.status == "OPEN" for x in LOOP_LAYERS))


def check_T_w_trace_full_loop_reduction_is_minimal_ordered():
    ids = [g.gate_id for g in REDUCTION_GATES]
    return _res("reduction_is_minimal_ordered", ids == ["G1_ACTION", "G2_ONE_LOOP", "G3_TWO_LOOP", "G4_MIXED_HIGHER", "G5_NATIVE_COV"])


def check_T_w_trace_full_loop_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_full_loop_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_full_loop_") and callable(obj)}


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
