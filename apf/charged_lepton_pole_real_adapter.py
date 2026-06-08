"""APF Charged-Lepton Pole Real Adapter — Tier-1 mass-sector wire-in (v24.3.41).

Added per Mass-sector Step D audit Finding 4: closes the R1 (charged-lepton →
pole) adapter gap. Registry status was `[P_export_candidate]^{pole+envelope}`
but no live `*_real_adapter` module produced an atlas payload — the engine
therefore read R1 as `SOLVED_LOCAL_HELD_FOR_REPAIR`. This adapter populates
the route's atlas payload from the v43/v46 bank-witnessed pole-mass values so
the engine can return `SOLVED_GLOBAL_P` at the imported-one-route gate level.

The pole-mass values $(m_e, m_\\mu, m_\\tau) = (0.5110026, 105.65824, 1776.91683)$
MeV are bank-witnessed at LATEST-44 v43–v48. The CODATA 2022 / NIST $\\alpha$
ledger provides the diagnostic comparator. APF envelope $\\epsilon = 1/5063 =
0.0198\\%$; combined truncation $100(\\alpha/\\pi)^2 = 0.000540\\%$; combined
$\\chi^2_3 = 0.394$, $p = 0.941$.

This adapter does NOT promote the route to APF-internal-derivation status. It
makes the existing imported-one-route closure (LATEST-44 v44 covariance admitted)
machine-checkable through the engine pipeline. Parallel structural form to
`apf/charged_lepton_qed_real_adapter.py` but for the pole codomain rather than
QED-running.
"""
from __future__ import annotations

from typing import Any, Dict, Mapping

from apf.real_adapter_factory import RealAdapterSnapshot, make_check_set


ATLAS_INPUT_ID = "mass:route01_charged_lepton_pole"
ATLAS_ROUTE = "ew"
ATLAS_PAYLOAD_NAME = "charged_lepton_pole_real_adapter_live"


# Bank-witnessed pole-mass values (LATEST-44 v43–v48; diagnostic only)
POLE_MASS_MEV: Mapping[str, float] = {
    "m_e": 0.5110026357885311,
    "m_mu": 105.658243985342,
    "m_tau": 1776.9168320084111,
}

EXTERNAL_LEDGER_FIELDS = (
    "CODATA 2022 alpha-inverse 137.035999177(21)",
    "APF envelope epsilon = 1/5063 = 0.0198%",
    "QED 2-loop truncation envelope 100*(alpha/pi)^2 = 0.000540%",
    "combined chi^2_3 = 0.394, p = 0.941",
    "PDG charged-lepton pole-mass diagnostic comparators",
)

FORBIDDEN_TARGET_KEYS = frozenset({
    "pole_mass_e_measured", "pole_mass_mu_measured", "pole_mass_tau_measured",
    "fitted_pole_mass", "post_hoc_pole_normalization",
})


def build_snapshot() -> RealAdapterSnapshot:
    """Build the snapshot from banked v43/v46/v48 content."""
    return RealAdapterSnapshot(
        trace_sector_closed=True,
        source_to_scheme_registry_present=True,
        evaluator_map_found=True,
        codomain_transport_found=True,
        counterterm_finite_parts_declared=True,
        external_constants_ledger_clean=True,
        uncertainty_protocol_declared=True,
        target_value_consumed=False,
        external_ledger_fields_declared=EXTERNAL_LEDGER_FIELDS,
        notes=(
            "Charged-lepton pole codomain (Route 1) via v43 trace vector + v46 pole "
            "completion + v48 APF/QED truncation envelope. Pole values diagnostic-only."
        ),
        extension_fields={
            "pole_mass_MeV_e": POLE_MASS_MEV["m_e"],
            "pole_mass_MeV_mu": POLE_MASS_MEV["m_mu"],
            "pole_mass_MeV_tau": POLE_MASS_MEV["m_tau"],
        },
    )


def build_live_atlas_payload() -> Dict[str, Any]:
    """Build the live route payload for the atlas runner's swap dict."""
    return build_snapshot().to_payload(name=ATLAS_PAYLOAD_NAME)


_CHECKS = make_check_set(
    adapter_name="charged_lepton_pole",
    route=ATLAS_ROUTE,
    payload_name=ATLAS_PAYLOAD_NAME,
    snapshot_factory=build_snapshot,
    required_ledger_fields=EXTERNAL_LEDGER_FIELDS,
    target_value_keys=FORBIDDEN_TARGET_KEYS,
)


def register(registry=None):
    if registry is None:
        return dict(_CHECKS)
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2, sort_keys=True, default=str))
