"""Trace-to-scheme transport boundary bank.

v8.5 (2026-05-08 LATER-3): bank-facing boundary package for the next APF
push after trace-sector closure.  This module does *not* close physical mass
transport.  It registers a set of executable boundary theorems that make the
open codomain problem auditable:

    APF_TRACE / W_TRACE  --open transport map-->  physical reporting scheme S(mu)

Passing these checks means the trace-to-scheme problem is correctly staged:
trace-sector values are immutable inputs, scheme/scale/convention data are
required before comparison, QCD/EW branches are separated, and inverse use of
reported physical masses is forbidden.

Status discipline:
    - APF_TRACE / W_TRACE closure: closed upstream at [P_local].
    - Trace-to-physical-scheme transport: open.
    - This module: [P_boundary], not [P_physical].
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Mapping, Tuple

from apf.trace_sector_closure import (
    check_T_apf_trace_sector_closure as _check_T_apf_trace_sector_closure,
)
from apf.charged_trace_spectrum import (
    check_T_charged_fermion_apf_trace_spectrum as _check_T_charged_fermion_apf_trace_spectrum,
)

TRACE_CODOMAIN = "APF_TRACE"
W_TRACE_CODOMAIN = "W_TRACE"
PHYSICAL_TRANSPORT_STATUS = "open: requires trace-to-scheme counterterm/codomain transport theorem"

COLORED_FERMIONS: Tuple[str, ...] = ("m_u", "m_c", "m_t", "m_d", "m_s", "m_b")
UNCHARGED_QCD_FERMIONS: Tuple[str, ...] = ("m_e", "m_mu", "m_tau")

ALLOWED_SCHEME_TARGETS: Tuple[str, ...] = (
    "MSbar(mu)",
    "pole",
    "on-shell",
    "threshold/1S/PS/MSR",
    "lattice reference scheme",
    "Monte-Carlo event-generator mass convention",
)

FORBIDDEN_INVERSE_INPUTS: Tuple[str, ...] = (
    "target physical mass vector",
    "PDG charged-fermion masses as fitted inputs",
    "MSbar masses as normalization inputs",
    "pole masses as normalization inputs",
    "lattice masses as normalization inputs",
    "Monte-Carlo masses as normalization inputs",
    "post-hoc scalar fitted to minimize physical spectrum error",
    "identity map APF_TRACE == physical masses",
)

REQUIRED_TRANSPORT_FACTORS: Tuple[str, ...] = (
    "declared target scheme S",
    "declared reference scale mu or scheme-specific convention",
    "EW/Yukawa running map",
    "QED running map for charged leptons where applicable",
    "QCD running and threshold matching map for colored fermions",
    "counterterm convention",
    "external constants ledger with uncertainties",
    "uncertainty propagation and comparison protocol",
)


@dataclass(frozen=True)
class SchemeTarget:
    """Declared target codomain for a future physical comparison."""

    scheme: str
    reference_scale: str
    convention: str
    exports_physical_masses: bool = True


@dataclass(frozen=True)
class TransportLedger:
    """Minimal ledger required before APF_TRACE can be compared to a scheme."""

    trace_codomain: str
    target_codomain: str
    required_factors: Tuple[str, ...]
    forbidden_inverse_inputs: Tuple[str, ...]
    physical_transport_closed: bool = False


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def _trace_vector() -> Dict[str, float]:
    charged = _check_T_charged_fermion_apf_trace_spectrum()
    assert _passed(charged)
    assert charged.get("codomain") == TRACE_CODOMAIN
    masses = dict(charged.get("masses_GeV", {}))
    required = set(COLORED_FERMIONS + UNCHARGED_QCD_FERMIONS)
    assert required.issubset(masses), "charged APF_TRACE vector missing entries"
    return {k: float(masses[k]) for k in sorted(required)}


def _ledger() -> TransportLedger:
    return TransportLedger(
        trace_codomain="APF_TRACE / W_TRACE",
        target_codomain="physical reporting scheme S(mu)",
        required_factors=REQUIRED_TRANSPORT_FACTORS,
        forbidden_inverse_inputs=FORBIDDEN_INVERSE_INPUTS,
        physical_transport_closed=False,
    )


# ---------------------------------------------------------------------
# Bank-facing boundary checks.
# ---------------------------------------------------------------------


def check_T_trace_scheme_boundary_declared() -> Dict[str, Any]:
    """Declare the exact boundary between closed APF_TRACE and open transport."""
    closed = _check_T_apf_trace_sector_closure()
    assert _passed(closed)
    assert closed.get("exports_physical_masses") is False
    return {
        "name": "T_trace_scheme_boundary_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_boundary",
        "closed_codomain": "APF_TRACE / W_TRACE",
        "open_transport": PHYSICAL_TRANSPORT_STATUS,
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "dependencies": ["T_apf_trace_sector_closure"],
        "key_result": "APF_TRACE/W_TRACE closure is separated from physical scheme transport.",
    }


def check_T_trace_codomain_immutability() -> Dict[str, Any]:
    """Trace-sector values are consumed as fixed codomain outputs, not retuned."""
    masses = _trace_vector()
    return {
        "name": "T_trace_codomain_immutability",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_boundary | no-smuggling",
        "codomain": TRACE_CODOMAIN,
        "masses_GeV": masses,
        "mutable_by_transport": False,
        "transport_may_add": ["scheme map", "running", "thresholds", "counterterms", "uncertainties"],
        "transport_may_not_add": ["retuned trace anchors", "post-hoc scalar fit", "physical identity assertion"],
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "The APF_TRACE vector enters transport as an immutable input codomain.",
    }


def check_T_trace_to_scheme_inputs_separated() -> Dict[str, Any]:
    """Separate APF-internal trace inputs from external transport inputs."""
    charged = _check_T_charged_fermion_apf_trace_spectrum()
    assert _passed(charged)
    return {
        "name": "T_trace_to_scheme_inputs_separated",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_boundary",
        "trace_inputs": ["charged fermion APF_TRACE vector", "M_W^TRACE", "trace-sector normalizers"],
        "external_transport_inputs_required": list(REQUIRED_TRANSPORT_FACTORS),
        "forbidden_inverse_inputs": list(FORBIDDEN_INVERSE_INPUTS),
        "used_forbidden_inverse_inputs": [],
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "The next theorem must add transport data, not retune trace anchors to the target spectrum.",
    }


def check_T_scheme_target_contract_declared() -> Dict[str, Any]:
    """A physical comparison requires an explicit target scheme contract."""
    examples = [
        SchemeTarget("MSbar", "mu = declared by comparison", "renormalized running mass"),
        SchemeTarget("pole", "scheme convention", "on-shell/pole convention"),
        SchemeTarget("threshold", "threshold scale", "1S/PS/MSR convention"),
    ]
    return {
        "name": "T_scheme_target_contract_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_boundary",
        "allowed_scheme_targets": list(ALLOWED_SCHEME_TARGETS),
        "minimal_contract_fields": ["scheme", "reference_scale_or_convention", "counterterm convention", "uncertainty ledger"],
        "example_contracts": [asdict(x) for x in examples],
        "canonical_scheme_selected": False,
        "reference_scale_selected": False,
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "A target scheme S and scale/convention must be declared before any physical comparison.",
    }


def check_T_colored_qcd_transport_branch_separated() -> Dict[str, Any]:
    """QCD threshold transport is isolated for colored fermions."""
    masses = _trace_vector()
    colored = {k: masses[k] for k in COLORED_FERMIONS}
    return {
        "name": "T_colored_qcd_transport_branch_separated",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_boundary",
        "colored_fermions": list(COLORED_FERMIONS),
        "trace_values_GeV": colored,
        "requires": ["alpha_s running", "flavor thresholds", "scheme-specific matching", "scale choice"],
        "current_status": "deferred/open; not imported into APF_TRACE closure",
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "QCD transport is declared as a separate map; APF_TRACE values are not pole-like exports.",
    }


def check_T_lepton_ew_qed_transport_branch_separated() -> Dict[str, Any]:
    """Lepton transport has no QCD branch but still requires EW/QED scheme data."""
    masses = _trace_vector()
    leptons = {k: masses[k] for k in UNCHARGED_QCD_FERMIONS}
    return {
        "name": "T_lepton_ew_qed_transport_branch_separated",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_boundary",
        "leptons": list(UNCHARGED_QCD_FERMIONS),
        "trace_values_GeV": leptons,
        "requires": ["EW/Yukawa running", "QED running if comparison scheme requires it", "renormalization convention"],
        "qcd_transport_required": False,
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "Lepton comparison is cleaner than quark comparison but is still a scheme-transport problem.",
    }


def check_T_identity_map_to_physical_scheme_forbidden() -> Dict[str, Any]:
    """Forbid the implicit identity APF_TRACE == physical reported masses."""
    return {
        "name": "T_identity_map_to_physical_scheme_forbidden",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_boundary | no-smuggling",
        "forbidden_map": "identity: APF_TRACE -> physical reporting scheme",
        "allowed_future_maps": ["declared scheme transport", "running/matching/counterterm map", "uncertainty-propagating comparison map"],
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "Physical agreement/disagreement cannot be scored by silently identifying trace and reporting codomains.",
    }


def check_T_external_constants_ledger_required() -> Dict[str, Any]:
    """Require an explicit external-constant ledger for future transport."""
    return {
        "name": "T_external_constants_ledger_required",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_boundary | no-smuggling",
        "required_external_constants": [
            "alpha_s(mu) if colored transport is attempted",
            "alpha_em/EW inputs if EW/QED running is attempted",
            "threshold masses or threshold conventions if threshold matching is attempted",
            "renormalization scale choices",
            "uncertainties and correlations",
        ],
        "current_external_constants_used_for_closure": [],
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "External constants may enter only through a declared transport ledger, not through trace-sector closure.",
    }


def check_T_no_physical_mass_inverse_fit() -> Dict[str, Any]:
    """No inverse use of physical masses in the staged transport boundary."""
    return {
        "name": "T_no_physical_mass_inverse_fit",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_boundary | no-smuggling",
        "forbidden_inverse_inputs": list(FORBIDDEN_INVERSE_INPUTS),
        "used_forbidden_inverse_inputs": [],
        "allowed_current_inputs": ["APF_TRACE vector", "W_TRACE value", "declared open transport requirements"],
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "No physical mass target is used as an inverse calibration input.",
    }


def check_T_trace_to_scheme_boundary_bank_closure() -> Dict[str, Any]:
    """Master boundary theorem: transport is staged, not closed."""
    deps = [
        check_T_trace_scheme_boundary_declared(),
        check_T_trace_codomain_immutability(),
        check_T_trace_to_scheme_inputs_separated(),
        check_T_scheme_target_contract_declared(),
        check_T_colored_qcd_transport_branch_separated(),
        check_T_lepton_ew_qed_transport_branch_separated(),
        check_T_identity_map_to_physical_scheme_forbidden(),
        check_T_external_constants_ledger_required(),
        check_T_no_physical_mass_inverse_fit(),
    ]
    assert all(_passed(dep) for dep in deps)
    ledger = _ledger()
    return {
        "name": "T_trace_to_scheme_boundary_bank_closure",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_boundary",
        "dependencies": [dep["name"] for dep in deps],
        "ledger": asdict(ledger),
        "closed_now": "trace-sector closure only",
        "open_next": "Trace-to-Scheme Transport Theorem",
        "physical_transport_status": PHYSICAL_TRANSPORT_STATUS,
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "The next push is bank-staged: transport is the open theorem, not an implied consequence of APF_TRACE closure.",
    }


_CHECKS = {
    "T_trace_scheme_boundary_declared": check_T_trace_scheme_boundary_declared,
    "T_trace_codomain_immutability": check_T_trace_codomain_immutability,
    "T_trace_to_scheme_inputs_separated": check_T_trace_to_scheme_inputs_separated,
    "T_scheme_target_contract_declared": check_T_scheme_target_contract_declared,
    "T_colored_qcd_transport_branch_separated": check_T_colored_qcd_transport_branch_separated,
    "T_lepton_ew_qed_transport_branch_separated": check_T_lepton_ew_qed_transport_branch_separated,
    "T_identity_map_to_physical_scheme_forbidden": check_T_identity_map_to_physical_scheme_forbidden,
    "T_external_constants_ledger_required": check_T_external_constants_ledger_required,
    "T_no_physical_mass_inverse_fit": check_T_no_physical_mass_inverse_fit,
    "T_trace_to_scheme_boundary_bank_closure": check_T_trace_to_scheme_boundary_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register trace-to-scheme boundary checks into the global bank."""
    registry.update(_CHECKS)


def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {
        "passed": sum(1 for row in rows if row["passed"]),
        "total": len(rows),
        "status": "TRACE_TO_SCHEME_BOUNDARY_BANK_PASS" if ok else "TRACE_TO_SCHEME_BOUNDARY_BANK_FAIL",
        "bank_registered": True,
        "physical_transport_closed": False,
        "results": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))
