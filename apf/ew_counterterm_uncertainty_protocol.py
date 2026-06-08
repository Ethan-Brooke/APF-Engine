"""EW counterterm + uncertainty protocol evidence packet.

v24.3.18 sandbox follow-on for the Interface Engine live EW blockers.

Purpose
-------
The live Interface Engine had only two EW trace-to-scheme structures still open:

    COUNTERTERM
    UNCERTAINTY_PROTOCOL

This module supplies a *structural protocol packet* for those two slots:

    finite-part / counterterm convention declared
    uncertainty / comparison protocol declared
    no-target / no-fit guard declared

Boundary
--------
This is not a numerical renormalized electroweak self-energy evaluator and does
not assert a new physical W-mass result.  It makes the Engine's two remaining EW
structure slots explicit and rerunnable, while preserving the stronger APF-
internal loop-evaluator gate as a non-claim.

Top check:
    check_T_ew_counterterm_uncertainty_protocol_P
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Tuple
import csv
import json
from pathlib import Path

STATUS = "P_ew_counterterm_uncertainty_protocol"
VERSION = "APF_EW_COUNTERTERM_UNCERTAINTY_PROTOCOL_v1"
MARKER = "EW_COUNTERTERM_UNCERTAINTY_PROTOCOL_PASS"

FORBIDDEN_INPUTS: Tuple[str, ...] = (
    "measured_M_W",
    "world_average_M_W",
    "DIZET_total_output_as_component_value",
    "ZFITTER_total_output_as_component_value",
    "published_total_SM_M_W_as_component_value",
    "fitted_counterterm",
    "posthoc_residual_fit",
    "posterior_output_as_input",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Export_EW_APF_internal_full_loop_value_P = 0",
    "Export_EW_APF_internal_delta_r_rem_value_P = 0",
    "Export_EW_new_physical_W_prediction_P = 0",
    "Export_target_fitted_counterterm_P = 0",
)


@dataclass(frozen=True)
class CountertermProtocol:
    scheme_name: str
    finite_part_convention: str
    subtraction_prescription: str
    scale_policy: str
    tadpole_convention: str
    gauge_policy: str
    diagram_class_content: Tuple[str, ...]
    counterterm_component: str
    matching_rule: str
    finite_values_status: str
    target_input_policy: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class UncertaintyProtocol:
    protocol_name: str
    source_channels: Tuple[str, ...]
    covariance_attachment_rule: str
    propagation_rule: str
    comparison_statistic: str
    acceptance_threshold: str
    covariance_values_status: str
    target_input_policy: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EWCountertermUncertaintyPacket:
    version: str
    status: str
    counterterm_protocol: CountertermProtocol
    uncertainty_protocol: UncertaintyProtocol
    adapter_flags: Mapping[str, bool]
    forbidden_inputs: Tuple[str, ...]
    non_claims: Tuple[str, ...]
    boundary_note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "status": self.status,
            "counterterm_protocol": self.counterterm_protocol.to_dict(),
            "uncertainty_protocol": self.uncertainty_protocol.to_dict(),
            "adapter_flags": dict(self.adapter_flags),
            "forbidden_inputs": list(self.forbidden_inputs),
            "non_claims": list(self.non_claims),
            "boundary_note": self.boundary_note,
        }


def counterterm_protocol() -> CountertermProtocol:
    return CountertermProtocol(
        scheme_name="EW on-shell Delta-r finite-part/counterterm protocol",
        finite_part_convention="finite remainders are sorted into declared APF_TRACE component slots before any comparison statistic is formed",
        subtraction_prescription="on-shell subtraction with finite remainder slots ledgered separately from imported total-evaluator outputs",
        scale_policy="auxiliary scale dependence must be declared at the slot level and may not be tuned against the physical W target",
        tadpole_convention="tadpole treatment must be explicitly declared by any downstream numerical evaluator; unspecified tadpoles fail closed",
        gauge_policy="gauge/Goldstone/ghost/gauge-boson diagram class membership must be declared by the downstream evaluator",
        diagram_class_content=(
            "Delta_alpha_running_channel",
            "rho_leading_top_channel",
            "rho_cross_and_screening_channel",
            "bosonic_self_energy_channel",
            "fermionic_self_energy_channel",
            "vertex_box_remainder_channel",
            "scheme_conversion_counterterm_channel",
        ),
        counterterm_component="Delta_r_ct_OS_finite_counterterm_slot",
        matching_rule="same-input matching only; no residual or physical-target backsolve can define the counterterm",
        finite_values_status="DECLARED_NOT_NUMERICALLY_SUPPLIED",
        target_input_policy="forbid measured/world-average W mass and total SM output as component inputs",
    )


def uncertainty_protocol() -> UncertaintyProtocol:
    return UncertaintyProtocol(
        protocol_name="EW trace-to-scheme covariance/comparison protocol",
        source_channels=(
            "source-ledger uncertainty",
            "external-constant uncertainty",
            "finite-remainder truncation/covariance",
            "counterterm-scheme uncertainty",
            "comparison-codomain uncertainty",
        ),
        covariance_attachment_rule="covariance attaches to declared source/resolution boundary slots, not to fitted residuals",
        propagation_rule="linearized push-forward from Delta-r component ledger to comparison object, with slot covariance matrix required before numerical promotion",
        comparison_statistic="predeclared z/chi2-style residual computed only after source-side values and covariance are supplied",
        acceptance_threshold="route-specific threshold must be declared before evaluating comparator residuals",
        covariance_values_status="PROTOCOL_DECLARED_VALUES_NOT_SUPPLIED",
        target_input_policy="observed W value is allowed only as a comparator, never as an uncertainty input or fitted closure target",
    )


def build_packet() -> EWCountertermUncertaintyPacket:
    return EWCountertermUncertaintyPacket(
        version=VERSION,
        status=STATUS,
        counterterm_protocol=counterterm_protocol(),
        uncertainty_protocol=uncertainty_protocol(),
        adapter_flags={
            "counterterm_finite_parts_declared": True,
            "uncertainty_protocol_declared": True,
            "target_value_consumed": False,
            "protocol_only": True,
            "numerical_full_loop_value_supplied": False,
            "physical_w_new_result_exported": False,
        },
        forbidden_inputs=FORBIDDEN_INPUTS,
        non_claims=NON_CLAIMS,
        boundary_note=(
            "This packet closes the Interface Engine's structural declaration slots for EW counterterm and uncertainty protocol. "
            "It does not supply a source-certified numerical renormalized EW self-energy evaluator and does not create a new physical W-mass claim."
        ),
    )


def export_packet(out_dir: str | Path) -> Dict[str, str]:
    out = Path(out_dir)
    (out / "results").mkdir(parents=True, exist_ok=True)
    (out / "tables").mkdir(parents=True, exist_ok=True)
    (out / "docs").mkdir(parents=True, exist_ok=True)
    (out / "scripts").mkdir(parents=True, exist_ok=True)

    packet = build_packet()
    data = packet.to_dict()
    packet_path = out / "results" / "EW_COUNTERTERM_UNCERTAINTY_PROTOCOL.json"
    packet_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    with (out / "tables" / "counterterm_protocol.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["field", "value"])
        for key, value in packet.counterterm_protocol.to_dict().items():
            if isinstance(value, tuple):
                value = ";".join(value)
            w.writerow([key, value])

    with (out / "tables" / "uncertainty_protocol.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["field", "value"])
        for key, value in packet.uncertainty_protocol.to_dict().items():
            if isinstance(value, tuple):
                value = ";".join(value)
            w.writerow([key, value])

    (out / "docs" / "HONEST_NON_CLAIMS.md").write_text(
        "# Honest non-claims\n\n" + "\n".join(f"- `{x}`" for x in NON_CLAIMS) + "\n\n" + packet.boundary_note + "\n",
        encoding="utf-8",
    )
    (out / "README.md").write_text(render_markdown(packet), encoding="utf-8")
    script_path = out / "scripts" / "check_ew_counterterm_uncertainty_protocol.py"
    script_path.write_text(
        "#!/usr/bin/env python3\n"
        "from apf.ew_counterterm_uncertainty_protocol import run_all, MARKER\n"
        "r = run_all()\n"
        "ok = all(x.get('consistent') or x.get('passed') for x in r.values())\n"
        "print(MARKER if ok else 'EW_COUNTERTERM_UNCERTAINTY_PROTOCOL_FAIL')\n"
        "raise SystemExit(0 if ok else 1)\n",
        encoding="utf-8",
    )
    return {
        "packet": str(packet_path),
        "counterterm_csv": str(out / "tables" / "counterterm_protocol.csv"),
        "uncertainty_csv": str(out / "tables" / "uncertainty_protocol.csv"),
        "non_claims": str(out / "docs" / "HONEST_NON_CLAIMS.md"),
        "readme": str(out / "README.md"),
        "verifier": str(script_path),
    }


def render_markdown(packet: EWCountertermUncertaintyPacket | None = None) -> str:
    packet = packet or build_packet()
    ct = packet.counterterm_protocol
    up = packet.uncertainty_protocol
    lines = [
        "# APF EW Counterterm + Uncertainty Protocol v1",
        "",
        f"- Status: `{packet.status}`",
        f"- Marker: `{MARKER}`",
        "- Scope: structural protocol declaration for the Interface Engine EW live blockers.",
        "- Boundary: no numerical full-loop EW self-energy value and no new physical W-mass claim.",
        "",
        "## Counterterm protocol",
        "",
        f"- Scheme: `{ct.scheme_name}`",
        f"- Counterterm component: `{ct.counterterm_component}`",
        f"- Finite values status: `{ct.finite_values_status}`",
        "- Diagram classes: " + ", ".join(f"`{x}`" for x in ct.diagram_class_content),
        "",
        "## Uncertainty protocol",
        "",
        f"- Name: `{up.protocol_name}`",
        f"- Covariance values status: `{up.covariance_values_status}`",
        f"- Comparison statistic: `{up.comparison_statistic}`",
        "",
        "## Adapter flags",
        "",
    ]
    for key, value in packet.adapter_flags.items():
        lines.append(f"- `{key}`: `{value}`")
    lines += ["", "## Forbidden inputs", ""]
    lines += [f"- `{x}`" for x in packet.forbidden_inputs]
    lines += ["", "## Honest non-claims", ""]
    lines += [f"- `{x}`" for x in packet.non_claims]
    lines += ["", packet.boundary_note, ""]
    return "\n".join(lines)


def _res(name: str, passed: bool, **data: Any) -> Dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "consistent": bool(passed),
        "status": "PASS" if passed else "FAIL",
        "epistemic": STATUS,
        "marker": MARKER if passed else "",
        "data": data,
    }


def check_T_ew_counterterm_slots_declared() -> Dict[str, Any]:
    ct = counterterm_protocol()
    tests = {
        "component_named": bool(ct.counterterm_component),
        "finite_convention_declared": "finite" in ct.finite_part_convention.lower(),
        "subtraction_declared": bool(ct.subtraction_prescription),
        "diagram_classes_enumerated": len(ct.diagram_class_content) >= 6,
        "values_not_numerically_supplied": ct.finite_values_status == "DECLARED_NOT_NUMERICALLY_SUPPLIED",
    }
    return _res("check_T_ew_counterterm_slots_declared", all(tests.values()), tests=tests, counterterm=ct.to_dict())


def check_T_ew_counterterm_forbids_fit_and_target_input() -> Dict[str, Any]:
    pkt = build_packet()
    forbidden = set(pkt.forbidden_inputs)
    tests = {
        "measured_w_forbidden": "measured_M_W" in forbidden and "world_average_M_W" in forbidden,
        "fitted_counterterm_forbidden": "fitted_counterterm" in forbidden and "posthoc_residual_fit" in forbidden,
        "total_sm_not_component_input": "DIZET_total_output_as_component_value" in forbidden,
        "target_not_consumed": pkt.adapter_flags["target_value_consumed"] is False,
    }
    return _res("check_T_ew_counterterm_forbids_fit_and_target_input", all(tests.values()), tests=tests, forbidden=sorted(forbidden))


def check_T_ew_uncertainty_protocol_declared() -> Dict[str, Any]:
    up = uncertainty_protocol()
    tests = {
        "channels_declared": len(up.source_channels) >= 5,
        "covariance_attachment_declared": "covariance" in up.covariance_attachment_rule.lower(),
        "propagation_declared": "push-forward" in up.propagation_rule.lower(),
        "values_not_supplied": up.covariance_values_status == "PROTOCOL_DECLARED_VALUES_NOT_SUPPLIED",
    }
    return _res("check_T_ew_uncertainty_protocol_declared", all(tests.values()), tests=tests, uncertainty=up.to_dict())


def check_T_ew_uncertainty_comparison_rule_predeclared() -> Dict[str, Any]:
    up = uncertainty_protocol()
    tests = {
        "comparison_statistic_named": bool(up.comparison_statistic),
        "threshold_predeclared": "before" in up.acceptance_threshold.lower(),
        "observed_w_comparator_only": "comparator" in up.target_input_policy.lower() and "never" in up.target_input_policy.lower(),
    }
    return _res("check_T_ew_uncertainty_comparison_rule_predeclared", all(tests.values()), tests=tests)


def check_T_ew_protocol_adapter_flags_safe() -> Dict[str, Any]:
    pkt = build_packet()
    flags = dict(pkt.adapter_flags)
    tests = {
        "counterterm_declared_true": flags.get("counterterm_finite_parts_declared") is True,
        "uncertainty_declared_true": flags.get("uncertainty_protocol_declared") is True,
        "target_not_consumed": flags.get("target_value_consumed") is False,
        "protocol_only_flag_true": flags.get("protocol_only") is True,
        "no_numerical_full_loop_value": flags.get("numerical_full_loop_value_supplied") is False,
        "no_new_w_result": flags.get("physical_w_new_result_exported") is False,
    }
    return _res("check_T_ew_protocol_adapter_flags_safe", all(tests.values()), tests=tests, flags=flags, non_claims=list(pkt.non_claims))


def check_T_ew_counterterm_uncertainty_protocol_P() -> Dict[str, Any]:
    checks = [
        check_T_ew_counterterm_slots_declared(),
        check_T_ew_counterterm_forbids_fit_and_target_input(),
        check_T_ew_uncertainty_protocol_declared(),
        check_T_ew_uncertainty_comparison_rule_predeclared(),
        check_T_ew_protocol_adapter_flags_safe(),
    ]
    ok = all(x["passed"] for x in checks)
    return _res(
        "check_T_ew_counterterm_uncertainty_protocol_P",
        ok,
        subchecks=[x["name"] for x in checks],
        boundary=build_packet().boundary_note,
    )


CHECKS = {
    "check_T_ew_counterterm_slots_declared": check_T_ew_counterterm_slots_declared,
    "check_T_ew_counterterm_forbids_fit_and_target_input": check_T_ew_counterterm_forbids_fit_and_target_input,
    "check_T_ew_uncertainty_protocol_declared": check_T_ew_uncertainty_protocol_declared,
    "check_T_ew_uncertainty_comparison_rule_predeclared": check_T_ew_uncertainty_comparison_rule_predeclared,
    "check_T_ew_protocol_adapter_flags_safe": check_T_ew_protocol_adapter_flags_safe,
    "check_T_ew_counterterm_uncertainty_protocol_P": check_T_ew_counterterm_uncertainty_protocol_P,
}


def register(registry=None):
    if registry is None:
        return CHECKS
    if hasattr(registry, "update"):
        registry.update(CHECKS)
        return registry
    for name, fn in CHECKS.items():
        if hasattr(registry, "register"):
            registry.register(name, fn)
        elif hasattr(registry, "add"):
            registry.add(name, fn)
        else:
            raise TypeError("Unsupported registry type for ew_counterterm_uncertainty_protocol.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    ok = all(x.get("passed") for x in results.values())
    print(json.dumps(results, indent=2, sort_keys=True, default=str))
    print(MARKER if ok else "EW_COUNTERTERM_UNCERTAINTY_PROTOCOL_FAIL")
    raise SystemExit(0 if ok else 1)
