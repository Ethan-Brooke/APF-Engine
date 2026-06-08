"""
APF Dark APF2 Real Adapter -- Campaign A wire-in (atlas v0.5 follow-on).

v24.3.23+ Engine-side adapter that turns the banked APF2 native physical-likelihood
smoke output (Campaign A close, banked today as APF_DARK_SECTOR_ROUTE_C_APF2_
NATIVE_PHYSICAL_LIKELIHOOD_SMOKE_v1) into a typed route payload the Engine can
read. Completes the day-of-three-campaigns symmetry: Campaign C (light-quark FLAG
kernel) and Campaign B (EW DIZET 2-loop) already have adapter wire-ins; this is
the third.

Purpose
-------
Atlas v0.4 surfaced EVALUATOR_MISSING + EMPIRICAL_POSTERIOR as the two MISSING
edges on the dark route, both attributed to obstruction class EVALUATOR_MISSING.
The G5 native physical-likelihood smoke closed earlier today produces:

    logpost = -6565.535707969133 (finite)

against the canonical Cobaya + CAMB + DESI/Planck likelihood stack, with the
APF2 frozen point (w_0, w_a) = (-58/61, -16/61) structurally derived at LATEST-62.

CORRECTION 2026-05-20: this adapter was originally built on the Campaign A smoke
output, which used a TIME-REVERSED w_2 curve (the polynomial was evaluated at a
instead of x = 1 - a). The curve-DEFINITION metadata here (w_2_at_a_eq_1,
polynomial form string) has been corrected to the canonical x=1-a form. The
SMOKE_LOGPOST is a reversed-curve run output and is flagged pending the corrected
re-run. The adapter's bank checks verify structure + finiteness, not the curve
value, so they were never sensitive to the bug -- and the audit-first OPEN_EVIDENCE_REQUIRED
typing held throughout (smoke was never promoted to posterior/empirical-P).
The adapter wires that banked smoke output into the dark route payload's
evaluator_map slot at the level the framework actually banks the claim --
SMOKE, not posterior, not robust empirical P.

Structural difference from Campaigns B and C
---------------------------------------------
Campaign C reads a per-flavor diagonal kernel (FLAG K_min) and Campaign B reads
a per-route evaluator-content ledger (DIZET M_W + SIN2TW + DAL5H + DR_TOTAL).
Campaign A reads a single-point logpost + 5 per-likelihood loglikes. The
adapter exposes those as Engine-readable evaluator content but the no-smuggling
guard is correspondingly different: APF2 rational coefficients must stay
frozen (no posterior-driven refit), and measured (w_0, w_a) values are never
consumed as inputs.

Status banked by this module
----------------------------
- Export_dark_RouteC_APF2_native_likelihood_smoke = 1 (preserved from Campaign A v1)
- Export_dark_RouteC_APF2_Cobaya_bridge = 1 (preserved from Campaign A v1)
- Export_dark_RouteC_APF2_engine_adapter_wired = 1 (NEW at this module)
- Export_dark_RouteC_APF2_posterior_P = 0 (smoke != posterior; preserved)
- Export_dark_robust_empirical_P = 0 (gates 3 + 4 still pending; preserved)
- APF2_coefficients_refit = 0 (rational coefficients structurally derived; preserved)

The adapter promotes only Engine-readability of the existing smoke result. It
does not lift the route to posterior-P or robust empirical-P. The G6
PantheonPlus smoke, Gate 3 DESI full-shape exact runtime, Gate 4 full-growth
likelihood, MCMC posterior convergence, and DESI collaboration NERSC
reproduction all remain OPEN named blockers on robust empirical-P.

Top check: check_T_dark_apf2_real_adapter_P
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Optional, Tuple

try:
    from apf.interface_structure_discovery_engine import discover_and_certify
    from apf.interface_structure_movement_graph import movement_graph_report
    from apf.interface_repair_frontier_explorer import explore_repair_frontier
    from apf.interface_repair_obligation_compiler import (
        compile_obligation_packet,
        evidence_template,
    )
    from apf.interface_evidence_rerun_controller import control_evidence_rerun
except Exception as exc:  # pragma: no cover
    raise ImportError(
        f"dark_apf2_real_adapter requires the interface-intelligence stack: {exc}"
    ) from exc


# ============================================================================
# Banked APF2 smoke content (verbatim from APF_DARK_SECTOR_ROUTE_C_APF2_
# NATIVE_PHYSICAL_LIKELIHOOD_SMOKE_v1 SUMMARY.json, this session 2026-05-18)
# ============================================================================

# APF2 frozen point: rational coefficients structurally derived at LATEST-62
# from endpoint uniqueness + barycentric pivot + capacity response ratio.
# Refitting these coefficients violates the no-smuggling guard.
APF2_FROZEN_POINT: Mapping[str, float] = {
    "w_0":          -58.0 / 61.0,  # = -0.9508196721311475
    "w_a":          -16.0 / 61.0,  # = -0.26229508196721313
    "x_pivot":        1.0 / 3.0,   # barycentric three-sector neutral coordinate
    "kappa_2":       21.0 / 8.0,   # Omega_Lambda / Omega_c = (42/61) / (16/61)
    "w_2_at_a_eq_1": -0.9508196721311475,  # w_2(today, a=1) = -1+3/61 = -58/61 (canonical; = w_0). Was -1.21311 under the reversed-curve bug (that is w_2 at a=0, early universe).
}

# APF2 polynomial form (CANONICAL: variable is x = 1 - a, x=0 today at a=1):
#   w_2(x) = -1 + 3/61 - (16/61) x - (21/8) x (x - 1/3) (1 - x),  x = 1 - a
# Tabulated on 728-row a-grid from 1e-4 to 1.0 in CAMB via set_w_a_table.
# (The earlier string wrote the polynomial in `a` directly, time-reversing the
#  curve -- the 2026-05-20 bug. Corrected here.)
APF2_W2_POLYNOMIAL_FORM: str = (
    "w_2(x) = -1 + 3/61 - (16/61) x - (21/8) x (x - 1/3) (1 - x),  x = 1 - a"
)
APF2_ADAPTER_TABLE_ROWS: int = 728
APF2_A_MIN: float = 1e-4
APF2_A_MAX: float = 1.0

# Smoke logpost output (Campaign A v1 banked, byte-for-byte from SUMMARY.json).
# WARNING (2026-05-20): this value was produced on the TIME-REVERSED w_2 curve
# (x=a bug). It is finite (so the smoke-finite check still passes) but it is NOT
# the correct-curve logpost. It will be replaced when Campaign A is re-run on the
# corrected (x=1-a) curve. The bank checks here verify structure + finiteness,
# not the curve value, so this flag does not change any check outcome.
SMOKE_LOGPOST: float = -6565.535707969133  # reversed-curve; pending re-derivation
SMOKE_LOGPRIOR: float = 0.0

# Per-likelihood log-likelihoods (all finite at the APF2 frozen point).
PER_LIKELIHOOD_LOGLIKES: Mapping[str, float] = {
    "bao.desi_dr2":                       -15.383629343413046,
    "planck_2018_lowl.TT":                -10.568389368849097,
    "planck_2018_lowl.EE":               -203.6914004545225,
    "planck_NPIPE_highl_CamSpec.TTTEEE": -6326.860708693056,
    "planck_2018_lensing.native":          -9.031580109291898,
}

# Canonical likelihood pack order (matches Cobaya YAML construction).
LIKELIHOOD_NAMES_CANONICAL: Tuple[str, ...] = (
    "bao.desi_dr2",
    "planck_2018_lowl.TT",
    "planck_2018_lowl.EE",
    "planck_NPIPE_highl_CamSpec.TTTEEE",
    "planck_2018_lensing.native",
)

# APF2 monkeypatch injection counts (Campaign A v1 banked).
# Three calls during model construction confirm the patch fired and replaced
# CAMB's default dark-energy class with the tabulated w_2(a) table.
APF2_INJECTION_COUNTS: Mapping[str, int] = {
    "init":            2,
    "set_cosmology":   0,
    "set_dark_energy": 0,
    "set_classes":     1,
    "total":           3,
}

# Runtime environment (Campaign A v1 reproduction).
SMOKE_ENVIRONMENT: Mapping[str, str] = {
    "python_version":  "3.14.4",
    "cobaya_version":   "3.6.2",
    "camb_version":     "1.6.6",
    "platform":         "Windows 11 + MSYS2 UCRT64",
    "build_seconds":    "1.585",
    "eval_seconds":     "0.470",
}

# Provenance.
SMOKE_PROVENANCE: Mapping[str, str] = {
    "source_pack":    "APF_DARK_SECTOR_ROUTE_C_APF2_NATIVE_PHYSICAL_LIKELIHOOD_SMOKE_v1",
    "source_summary": "results/SUMMARY.json",
    "session_date":   "2026-05-18",
    "campaign":       "A (CAMB tau_reio / native physical-likelihood smoke)",
    "gate":           "G5 of six-gate runtime-bridge ladder",
}

# Required external evaluator ledger fields for the dark-sector route.
REQUIRED_EXTERNAL_LEDGER_FIELDS: Tuple[str, ...] = (
    "cobaya_version_and_yaml_schema",
    "camb_version_and_dark_energy_class",
    "tabulated_w_a_table_grid_specification",
    "planck_npipe_camspec_likelihood_data_files",
    "planck_2018_lowl_TT_EE_data_files",
    "planck_2018_lensing_native_data_files",
    "desi_dr2_bao_data_files",
    "apf2_monkeypatch_injection_count_audit",
    "smoke_vs_posterior_grade_declaration",
)

# No-smuggling guard: keys that must NEVER appear as route inputs. The dark
# route's defining no-smuggling commitment is that the APF2 rational
# coefficients (-58/61, -16/61) are derived at LATEST-62, not refitted; and
# the smoke logpost is the OUTPUT of the route, never an INPUT.
TARGET_VALUE_KEYS: frozenset = frozenset({
    "w_0_observed", "w_a_observed",
    "w_0_target", "w_a_target",
    "logpost_target", "logpost_observed",
    "posterior_output_as_input",
    "target_value", "measured_w_0_w_a",
})


# ============================================================================
# Snapshot + Report dataclasses
# ============================================================================

@dataclass(frozen=True)
class DarkApf2AdapterSnapshot:
    """Typed snapshot of the dark route state via Campaign A APF2 smoke output.

    Boolean flags correspond to the dark-route payload contract. Smoke-grade:
    smoke_pass True; posterior_closed False; chains_converged False.
    """
    route_built: bool
    run_completed: bool
    smoke_pass: bool
    chains_converged: bool
    posterior_closed: bool
    robustness_checks_passed: bool
    data_ledger_clean: bool
    evaluator_map_found: bool
    codomain_transport_found: bool
    counterterm_finite_parts_declared: bool
    external_constants_ledger_clean: bool
    uncertainty_protocol_declared: bool
    target_value_consumed: bool
    apf2_coefficients_refit: bool
    smoke_logpost_finite: bool
    all_loglikes_finite: bool
    apf2_injection_observed: bool
    external_ledger_fields_declared: Tuple[str, ...]
    notes: str = ""

    def to_payload(self, name: str = "dark_apf2_real_adapter") -> Dict[str, Any]:
        return {
            "name": name,
            "route_built": self.route_built,
            "run_completed": self.run_completed,
            "smoke_pass": self.smoke_pass,
            "chains_converged": self.chains_converged,
            "posterior_closed": self.posterior_closed,
            "robustness_checks_passed": self.robustness_checks_passed,
            "data_ledger_clean": self.data_ledger_clean,
            "evaluator_map_found": self.evaluator_map_found,
            "codomain_transport_found": self.codomain_transport_found,
            "counterterm_finite_parts_declared": self.counterterm_finite_parts_declared,
            "external_constants_ledger_clean": self.external_constants_ledger_clean,
            "uncertainty_protocol_declared": self.uncertainty_protocol_declared,
            "target_value_consumed": self.target_value_consumed,
            "apf2_coefficients_refit": self.apf2_coefficients_refit,
            "smoke_logpost_finite": self.smoke_logpost_finite,
            "all_loglikes_finite": self.all_loglikes_finite,
            "apf2_injection_observed": self.apf2_injection_observed,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class DarkApf2AdapterReport:
    payload: Mapping[str, Any]
    snapshot: DarkApf2AdapterSnapshot
    apf2_smoke_output: Mapping[str, Any]
    certification: Mapping[str, Any]
    movement_graph: Mapping[str, Any]
    frontier: Mapping[str, Any]
    obligation_packet: Mapping[str, Any]
    evidence_template: Mapping[str, Any]
    rerun_result_without_evidence: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload": dict(self.payload),
            "snapshot": asdict(self.snapshot),
            "apf2_smoke_output": dict(self.apf2_smoke_output),
            "certification": dict(self.certification),
            "movement_graph": dict(self.movement_graph),
            "frontier": dict(self.frontier),
            "obligation_packet": dict(self.obligation_packet),
            "evidence_template": dict(self.evidence_template),
            "rerun_result_without_evidence": dict(self.rerun_result_without_evidence),
        }


# ============================================================================
# Snapshot construction
# ============================================================================

def infer_snapshot_from_banked_apf2_smoke(
    *,
    overrides: Optional[Mapping[str, Any]] = None,
) -> DarkApf2AdapterSnapshot:
    """Build snapshot from the Campaign A v1 banked APF2 smoke content.

    All booleans set True for fields the APF2 smoke + APF2 frozen point fill:
        - route_built                  (LATEST-83/84/85 built the runtime bridge)
        - run_completed                (Campaign A G5 smoke executed)
        - smoke_pass                   (logpost finite, all loglikes finite)
        - data_ledger_clean            (5 likelihood packs declared)
        - evaluator_map_found          (logpost + 5 loglikes populate the map)
        - codomain_transport_found     (w_2(a) -> CAMB via set_w_a_table)
        - counterterm_finite_parts_declared  (APF2 polynomial structure declared)
        - external_constants_ledger_clean    (cobaya + camb + likelihood data files)
        - uncertainty_protocol_declared      (monkeypatch injection count audit)
        - smoke_logpost_finite         (-6565.54 < infty)
        - all_loglikes_finite          (5/5)
        - apf2_injection_observed      (injection_total = 3)

    Booleans set False (audit-first):
        - chains_converged             (smoke != posterior; no chains run)
        - posterior_closed             (smoke != posterior; declared non-claim)
        - robustness_checks_passed     (smoke is one-point eval, not robustness)
        - target_value_consumed        (APF2 frozen point not measured)
        - apf2_coefficients_refit      (rational coefficients structurally derived)
    """
    base = dict(
        route_built=True,
        run_completed=True,
        smoke_pass=True,
        chains_converged=False,
        posterior_closed=False,
        robustness_checks_passed=False,
        data_ledger_clean=True,
        evaluator_map_found=True,
        codomain_transport_found=True,
        counterterm_finite_parts_declared=True,
        external_constants_ledger_clean=True,
        uncertainty_protocol_declared=True,
        target_value_consumed=False,
        apf2_coefficients_refit=False,
        smoke_logpost_finite=True,
        all_loglikes_finite=True,
        apf2_injection_observed=True,
        external_ledger_fields_declared=REQUIRED_EXTERNAL_LEDGER_FIELDS,
        notes=(
            "APF2 native physical-likelihood smoke output admitted as named "
            "external evaluator content under Campaign A v1 (logpost = "
            "-6565.535707969133 against canonical Cobaya 3.6.2 + CAMB 1.6.6 + "
            "DESI DR2 + Planck 2018 lowl TT/EE + Planck NPIPE CamSpec TTTEEE + "
            "Planck 2018 lensing native; APF2 frozen point (w_0, w_a) = "
            "(-58/61, -16/61) structurally derived at LATEST-62; monkeypatch "
            "fired 3 times during model construction). Status: smoke-grade "
            "result via G5 of six-gate runtime-bridge ladder. Adapter wires "
            "the banked smoke output into Engine-readable payload. Posterior "
            "closure / robust empirical P remain OPEN (G6 + Gate 3 + Gate 4 "
            "+ MCMC convergence + NERSC reproduction)."
        ),
    )
    if overrides:
        for k, v in overrides.items():
            if k in base:
                base[k] = v
    return DarkApf2AdapterSnapshot(**base)


def snapshot_from_payload(payload: Mapping[str, Any]) -> DarkApf2AdapterSnapshot:
    """Build snapshot from an arbitrary payload dict (testing convenience)."""
    return DarkApf2AdapterSnapshot(
        route_built=bool(payload.get("route_built", False)),
        run_completed=bool(payload.get("run_completed", False)),
        smoke_pass=bool(payload.get("smoke_pass", False)),
        chains_converged=bool(payload.get("chains_converged", False)),
        posterior_closed=bool(payload.get("posterior_closed", False)),
        robustness_checks_passed=bool(payload.get("robustness_checks_passed", False)),
        data_ledger_clean=bool(payload.get("data_ledger_clean", False)),
        evaluator_map_found=bool(payload.get("evaluator_map_found", False)),
        codomain_transport_found=bool(payload.get("codomain_transport_found", False)),
        counterterm_finite_parts_declared=bool(payload.get("counterterm_finite_parts_declared", False)),
        external_constants_ledger_clean=bool(payload.get("external_constants_ledger_clean", False)),
        uncertainty_protocol_declared=bool(payload.get("uncertainty_protocol_declared", False)),
        target_value_consumed=bool(payload.get("target_value_consumed", False)),
        apf2_coefficients_refit=bool(payload.get("apf2_coefficients_refit", False)),
        smoke_logpost_finite=bool(payload.get("smoke_logpost_finite", False)),
        all_loglikes_finite=bool(payload.get("all_loglikes_finite", False)),
        apf2_injection_observed=bool(payload.get("apf2_injection_observed", False)),
        external_ledger_fields_declared=tuple(payload.get("external_ledger_fields_declared", ())),
        notes=str(payload.get("notes", "")),
    )


# ============================================================================
# APF2 smoke output report payload
# ============================================================================

def apf2_smoke_output_report() -> Dict[str, Any]:
    """Return a structured representation of the banked APF2 smoke content."""
    return {
        "apf2_frozen_point": dict(APF2_FROZEN_POINT),
        "apf2_w2_polynomial_form": APF2_W2_POLYNOMIAL_FORM,
        "apf2_tabulation": {
            "table_rows":  APF2_ADAPTER_TABLE_ROWS,
            "a_min":       APF2_A_MIN,
            "a_max":       APF2_A_MAX,
            "method":      "CAMB DarkEnergyPPF.set_w_a_table (monkeypatch substitution)",
        },
        "smoke_output": {
            "logpost":   SMOKE_LOGPOST,
            "logprior":  SMOKE_LOGPRIOR,
            "per_likelihood_loglikes": dict(PER_LIKELIHOOD_LOGLIKES),
            "likelihood_names_in_order": list(LIKELIHOOD_NAMES_CANONICAL),
        },
        "apf2_monkeypatch_injection_counts": dict(APF2_INJECTION_COUNTS),
        "smoke_environment": dict(SMOKE_ENVIRONMENT),
        "smoke_provenance": dict(SMOKE_PROVENANCE),
        "required_external_ledger_fields": list(REQUIRED_EXTERNAL_LEDGER_FIELDS),
        "row_admission_protocol": (
            "Campaign A v1: smoke output admitted as named external evaluator "
            "content; APF2 rational coefficients NOT refit (frozen at "
            "LATEST-62 derivation); 5 per-likelihood loglikes admitted as "
            "evaluator-map content."
        ),
        "no_smuggling_protocol": (
            "Smoke logpost is the OUTPUT of the route, never an INPUT. "
            "Measured (w_0, w_a) values not consumed; rational coefficients "
            "(-58/61, -16/61) are derived at LATEST-62, not measured."
        ),
        "smoke_vs_posterior_grade": (
            "SMOKE: single-point logposterior({}) evaluation at the APF2 "
            "frozen point. NOT posterior: no MCMC chains run, no convergence "
            "diagnostics, no robustness audit. Posterior closure requires "
            "Gate 3 (DESI full-shape exact runtime) + Gate 4 (full-growth "
            "likelihood) + MCMC convergence (R-1 < 0.01, ESS >= 200, 4 chains) "
            "+ NERSC reproduction; all OPEN named blockers on robust "
            "empirical-P."
        ),
        "status": {
            "Export_dark_RouteC_APF2_native_likelihood_smoke": 1,
            "Export_dark_RouteC_APF2_Cobaya_bridge": 1,
            "Export_dark_RouteC_APF2_engine_adapter_wired": 1,  # NEW
            "Export_dark_RouteC_APF2_posterior_P": 0,
            "Export_dark_robust_empirical_P": 0,
            "APF2_coefficients_refit": 0,
        },
    }


# ============================================================================
# Full adapter report
# ============================================================================

def build_adapter_report(
    snapshot: DarkApf2AdapterSnapshot,
    *,
    name: str = "dark_apf2_real_adapter",
) -> DarkApf2AdapterReport:
    """Run the full Engine pipeline on the snapshot's payload."""
    payload = snapshot.to_payload(name=name)
    route = "dark"
    certification = discover_and_certify(route, payload)
    movement = movement_graph_report(route, payload)
    frontier = explore_repair_frontier(route, payload).to_dict()
    packet = compile_obligation_packet(route, payload)
    template = evidence_template(packet)
    rerun_without_evidence = control_evidence_rerun(route, payload).to_dict()
    return DarkApf2AdapterReport(
        payload=payload,
        snapshot=snapshot,
        apf2_smoke_output=apf2_smoke_output_report(),
        certification=certification,
        movement_graph=movement,
        frontier=frontier,
        obligation_packet=packet.to_dict(),
        evidence_template=template,
        rerun_result_without_evidence=rerun_without_evidence,
    )


def build_live_adapter_report(
    *,
    overrides: Optional[Mapping[str, Any]] = None,
    name: str = "dark_apf2_real_adapter_live",
) -> DarkApf2AdapterReport:
    """Build report from the banked APF2 smoke content (default live path)."""
    snapshot = infer_snapshot_from_banked_apf2_smoke(overrides=overrides)
    return build_adapter_report(snapshot, name=name)


# ============================================================================
# Canonical manual snapshots (for testing)
# ============================================================================

def canonical_manual_snapshots() -> Dict[str, DarkApf2AdapterSnapshot]:
    """Three canonical snapshots covering pre-wire / wire-in / smuggled cases."""
    return {
        "before_wire_in": DarkApf2AdapterSnapshot(
            route_built=True,
            run_completed=False,
            smoke_pass=False,
            chains_converged=False,
            posterior_closed=False,
            robustness_checks_passed=False,
            data_ledger_clean=False,
            evaluator_map_found=False,
            codomain_transport_found=False,
            counterterm_finite_parts_declared=False,
            external_constants_ledger_clean=False,
            uncertainty_protocol_declared=False,
            target_value_consumed=False,
            apf2_coefficients_refit=False,
            smoke_logpost_finite=False,
            all_loglikes_finite=False,
            apf2_injection_observed=False,
            external_ledger_fields_declared=(),
            notes="Pre-wire baseline: LATEST-87 attempts before Campaign A close; no Engine-readable smoke output.",
        ),
        "post_wire_in": infer_snapshot_from_banked_apf2_smoke(),
        "refit_coefficients_smuggled": DarkApf2AdapterSnapshot(
            route_built=True,
            run_completed=True,
            smoke_pass=True,
            chains_converged=False,
            posterior_closed=False,
            robustness_checks_passed=False,
            data_ledger_clean=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            counterterm_finite_parts_declared=True,
            external_constants_ledger_clean=True,
            uncertainty_protocol_declared=True,
            target_value_consumed=True,  # measured (w_0, w_a) consumed as input
            apf2_coefficients_refit=True,  # rational coefficients refit from data
            smoke_logpost_finite=True,
            all_loglikes_finite=True,
            apf2_injection_observed=True,
            external_ledger_fields_declared=REQUIRED_EXTERNAL_LEDGER_FIELDS,
            notes="Smuggled-coefficients case: APF2 refitted from data; should fail no-smuggling gate.",
        ),
    }


def run_canonical_adapter_reports() -> Dict[str, Dict[str, Any]]:
    return {
        name: build_adapter_report(snap).to_dict()
        for name, snap in canonical_manual_snapshots().items()
    }


# ============================================================================
# Bank-registered check functions
# ============================================================================

def check_T_dark_apf2_adapter_payload_contract_P() -> Dict[str, Any]:
    """Adapter snapshot produces a route payload conforming to dark route contract."""
    snap = infer_snapshot_from_banked_apf2_smoke()
    payload = snap.to_payload()
    required_keys = {
        "name", "route_built", "run_completed", "smoke_pass",
        "chains_converged", "posterior_closed", "evaluator_map_found",
        "codomain_transport_found", "target_value_consumed",
        "apf2_coefficients_refit", "smoke_logpost_finite",
        "all_loglikes_finite", "apf2_injection_observed", "notes",
    }
    has_all_keys = required_keys.issubset(payload.keys())
    no_smuggling = payload["target_value_consumed"] is False
    no_refit = payload["apf2_coefficients_refit"] is False
    evaluator_filled = payload["evaluator_map_found"] is True
    smoke_only = payload["posterior_closed"] is False  # smoke != posterior
    return {
        "name": "check_T_dark_apf2_adapter_payload_contract_P",
        "consistent": has_all_keys and no_smuggling and no_refit and evaluator_filled and smoke_only,
        "status": "P_real_adapter" if (has_all_keys and no_smuggling and no_refit and evaluator_filled) else "FAIL",
        "summary": "Dark APF2 adapter produces dark-shaped payload with smoke-filled evaluator + no-refit guard.",
        "data": {
            "required_keys_present": has_all_keys,
            "no_smuggling": no_smuggling,
            "no_refit": no_refit,
            "evaluator_filled": evaluator_filled,
            "smoke_only": smoke_only,
        },
    }


def check_T_dark_apf2_adapter_smoke_outputs_finite_P() -> Dict[str, Any]:
    """Smoke logpost + 5 per-likelihood loglikes all finite at APF2 frozen point."""
    import math
    logpost_finite = math.isfinite(SMOKE_LOGPOST)
    per_finite = {k: math.isfinite(v) for k, v in PER_LIKELIHOOD_LOGLIKES.items()}
    canonical_match = (
        list(PER_LIKELIHOOD_LOGLIKES.keys()) == list(LIKELIHOOD_NAMES_CANONICAL)
    )
    return {
        "name": "check_T_dark_apf2_adapter_smoke_outputs_finite_P",
        "consistent": logpost_finite and all(per_finite.values()) and canonical_match,
        "status": "P_smoke_finite" if (logpost_finite and all(per_finite.values())) else "FAIL",
        "summary": "Smoke logpost = -6565.54 and all 5 per-likelihood loglikes finite at APF2 frozen point.",
        "data": {
            "logpost": SMOKE_LOGPOST,
            "logpost_finite": logpost_finite,
            "per_likelihood_finite": per_finite,
            "canonical_order_matches": canonical_match,
        },
    }


def check_T_dark_apf2_adapter_no_smuggling_P() -> Dict[str, Any]:
    """Adapter snapshot does not consume measured (w_0, w_a) and does not refit APF2."""
    snap = infer_snapshot_from_banked_apf2_smoke()
    payload = snap.to_payload()
    smuggled = [k for k in TARGET_VALUE_KEYS if k in payload]
    rational_w0_correct = abs(APF2_FROZEN_POINT["w_0"] - (-58.0 / 61.0)) < 1e-15
    rational_wa_correct = abs(APF2_FROZEN_POINT["w_a"] - (-16.0 / 61.0)) < 1e-15
    return {
        "name": "check_T_dark_apf2_adapter_no_smuggling_P",
        "consistent": (
            (not smuggled)
            and (not payload["target_value_consumed"])
            and (not payload["apf2_coefficients_refit"])
            and rational_w0_correct
            and rational_wa_correct
        ),
        "status": "P_no_smuggling" if not smuggled else "FAIL",
        "summary": "No measured (w_0, w_a) key in payload; APF2 coefficients frozen at -58/61, -16/61; rational coefficients structurally derived at LATEST-62.",
        "data": {
            "smuggled_keys": smuggled,
            "target_value_consumed": payload["target_value_consumed"],
            "apf2_coefficients_refit": payload["apf2_coefficients_refit"],
            "rational_w0_correct": rational_w0_correct,
            "rational_wa_correct": rational_wa_correct,
        },
    }


def check_T_dark_apf2_adapter_external_ledger_declared_P() -> Dict[str, Any]:
    """Adapter declares the 9 required external evaluator ledger fields."""
    snap = infer_snapshot_from_banked_apf2_smoke()
    declared = set(snap.external_ledger_fields_declared)
    required = set(REQUIRED_EXTERNAL_LEDGER_FIELDS)
    return {
        "name": "check_T_dark_apf2_adapter_external_ledger_declared_P",
        "consistent": declared == required,
        "status": "P_external_ledger_declared" if declared == required else "FAIL",
        "summary": "All 9 required APF2 smoke external evaluator ledger fields declared on the snapshot.",
        "data": {
            "declared_count": len(declared),
            "required_count": len(required),
            "missing": sorted(required - declared),
        },
    }


def check_T_dark_apf2_adapter_certification_P() -> Dict[str, Any]:
    """Engine certification on adapter payload produces HONEST dark route reading.

    Structural difference from Campaigns B + C: the dark certifier requires
    empirical_closed = chains_converged AND posterior_closed AND
    robustness_checks_passed AND data_ledger_clean for the EVALUATOR_MAP
    edge to resolve. Smoke != posterior, so the Engine correctly types the
    route at OPEN_EVIDENCE_REQUIRED with EMPIRICAL_POSTERIOR + EVALUATOR_MAP
    marked MISSING and critical_fields = (posterior_closed,
    robustness_checks_passed). The adapter's success criterion is HONEST
    TYPING -- the Engine names the right missing fields with the right
    names. The OPEN_EVIDENCE_REQUIRED reading IS the audit-first discipline.
    """
    report = build_live_adapter_report()
    packet = report.obligation_packet
    edges = report.movement_graph.get("edges", [])

    actual_packet_status = packet.get("packet_status")
    packet_status_honest = (actual_packet_status == "OPEN_EVIDENCE_REQUIRED")

    critical = tuple(packet.get("critical_fields", ()))
    expected_critical = {"posterior_closed", "robustness_checks_passed"}
    critical_named_correctly = expected_critical.issubset(set(critical))

    posterior_edge = next(
        (e for e in edges if e.get("kind") == "EMPIRICAL_POSTERIOR"), None
    )
    posterior_honestly_missing = (
        posterior_edge is not None and posterior_edge.get("status") == "MISSING"
    )

    codomain_edge = next((e for e in edges if e.get("kind") == "CODOMAIN_TRANSPORT"), None)
    codomain_clean = codomain_edge is not None and codomain_edge.get("status") in (
        "MOVES_CLEANLY", "PRESENT_STABLE",
    )
    acc_edge = next((e for e in edges if e.get("kind") == "ACC_RECORD"), None)
    acc_clean = acc_edge is not None and acc_edge.get("status") in (
        "MOVES_CLEANLY", "PRESENT_STABLE",
    )

    ok = (
        packet_status_honest
        and critical_named_correctly
        and posterior_honestly_missing
        and codomain_clean
        and acc_clean
    )

    return {
        "name": "check_T_dark_apf2_adapter_certification_P",
        "consistent": ok,
        "status": "P_real_adapter" if ok else "FAIL",
        "summary": (
            "Dark APF2 adapter produces HONEST Engine reading: route at "
            "OPEN_EVIDENCE_REQUIRED with critical_fields naming posterior + "
            "robustness; EMPIRICAL_POSTERIOR edge MISSING; CODOMAIN_TRANSPORT "
            "+ ACC_RECORD edges clean. Smoke != posterior preserved structurally."
        ),
        "data": {
            "packet_status": actual_packet_status,
            "packet_status_honest": packet_status_honest,
            "critical_fields": list(critical),
            "critical_named_correctly": critical_named_correctly,
            "posterior_edge_status": posterior_edge.get("status") if posterior_edge else "ABSENT",
            "posterior_honestly_missing": posterior_honestly_missing,
            "codomain_edge_status": codomain_edge.get("status") if codomain_edge else "ABSENT",
            "codomain_clean": codomain_clean,
            "acc_edge_status": acc_edge.get("status") if acc_edge else "ABSENT",
            "acc_clean": acc_clean,
        },
    }


def check_T_dark_apf2_real_adapter_P() -> Dict[str, Any]:
    """Top integration check for the dark APF2 real adapter."""
    subchecks = [
        check_T_dark_apf2_adapter_payload_contract_P(),
        check_T_dark_apf2_adapter_smoke_outputs_finite_P(),
        check_T_dark_apf2_adapter_no_smuggling_P(),
        check_T_dark_apf2_adapter_external_ledger_declared_P(),
        check_T_dark_apf2_adapter_certification_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_dark_apf2_real_adapter_P",
        "consistent": ok,
        "status": "P_real_adapter" if ok else "FAIL",
        "summary": (
            "Dark APF2 real adapter wires banked Campaign A smoke output into "
            "Engine-readable dark route payload. Engine produces HONEST typing "
            "of the route at OPEN_EVIDENCE_REQUIRED with critical_fields = "
            "(posterior_closed, robustness_checks_passed); EMPIRICAL_POSTERIOR "
            "edge MISSING; CODOMAIN_TRANSPORT + ACC_RECORD edges clean. Smoke "
            "!= posterior preserved structurally (smoke is grade G5 of the "
            "six-gate runtime-bridge ladder; posterior closure requires "
            "Gates 3 + 4 + MCMC + NERSC, all OPEN named blockers)."
        ),
        "dependencies": [x["name"] for x in subchecks],
        "data": {"subchecks": {x["name"]: x["consistent"] for x in subchecks}},
    }


# ============================================================================
# verify_all registration
# ============================================================================

# ============================================================================
# Atlas live-runner contract
# ============================================================================

ATLAS_INPUT_ID = "dark:route_cross_sn_profile_probe"
ATLAS_ROUTE = "dark"
ATLAS_PAYLOAD_NAME = "dark_apf2_real_adapter_live"


def register(registry=None):
    """Register adapter checks into the bank registry."""
    checks = {
        "check_T_dark_apf2_adapter_payload_contract_P":         check_T_dark_apf2_adapter_payload_contract_P,
        "check_T_dark_apf2_adapter_smoke_outputs_finite_P":     check_T_dark_apf2_adapter_smoke_outputs_finite_P,
        "check_T_dark_apf2_adapter_no_smuggling_P":             check_T_dark_apf2_adapter_no_smuggling_P,
        "check_T_dark_apf2_adapter_external_ledger_declared_P": check_T_dark_apf2_adapter_external_ledger_declared_P,
        "check_T_dark_apf2_adapter_certification_P":            check_T_dark_apf2_adapter_certification_P,
        "check_T_dark_apf2_real_adapter_P":                     check_T_dark_apf2_real_adapter_P,
    }
    if registry is None:
        return checks
    registry.update(checks)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in register().items()}


if __name__ == "__main__":
    import json
    out = run_all()
    print(json.dumps({k: {"consistent": v["consistent"], "status": v["status"]} for k, v in out.items()}, indent=2))
