"""APF Interface Atlas v0.3 claim-refresh layer (v24.3.320).

Full Bank Onboarding -- held-route repair. The vendored v0.2 atlas input set
(apf/interface_atlas_v02_inputs.py) carries claim texts and payload flags
frozen at 2026-05-18 (bank state v24.3.18). A fresh-context survey at
v24.3.319 classified all 46 held-for-repair routes: 40 hold BY DESIGN
(current-disposition probes + synthetic classifier vectors), and SIX are
STALE -- their named blockers have been resolved or materially changed by
banked content landed since the freeze. The 2026-05-18 headline bottleneck
(EVALUATOR_MISSING, 76%% of held routes) is CONSUMED: at v24.3.319 no held
route is blocked on evaluator absence. The residual frontier, corrected per
the v15.1 adjudication (2026-06-16, found by the W-export scoping pass of
2026-07-02): the DARK result-pack admission (Gates 3/4) is the one genuinely
open gate; the W loop-sum export certificates were adjudicated [P_boundary]
at v15.1 -- Delta-r_rem has no scheme-free standalone measurement, and the
native distinction route (M_W = 80.3336 [P]) carries the physics. The
certificate machinery remains available for an apparatus demo (threading
the admitted DIZET v16.4 rows through the v10-11 chain) but that is
bookkeeping, not physics.

This module is the refresh layer: per stale input, the current-disposition
claim text (or payload flag updates) WITH PROVENANCE -- each refresh names
the banked checks that changed the disposition, and preserves the superseded
2026-05-18 wording for the record. Consumed by run_live_atlas AFTER base
assembly; the vendored v0.2 module and canonical_atlas_inputs() are NEVER
mutated (they are the archival snapshot, and the banked atlas checks
check_T_interface_atlas_* certify the canonical set as-is).

HONESTY: a refreshed route flipping an obstruction class is progress ONLY
because the named banked content landed; the refresh itself derives nothing.
Refreshed claims that still hold-for-repair hold on the TRUE current
frontier, which is the point.

TWO MEASUREMENT FACTS established while building this layer (verified by
direct edge inspection, not assumed):
1. Prose CLAIM inputs are typed structurally -- a claim graph without an
   attached evaluator object shows the EVALUATOR_MISSING edge (and typically
   CODOMAIN_MISMATCH beside it) REGARDLESS of wording. Re-wording cannot and should not clear it; the consumer of that
   class is the payload/adapter swap (the 26 existing adapters). Coarse
   obstruction-class counts over prose claims are therefore NOT a progress
   metric; missing-EDGE kinds on payload rows are.
2. The obstruction-hint label EVALUATOR_MISSING is COARSE: several edge
   kinds share it (EVALUATOR_MAP, UNCERTAINTY_PROTOCOL, EMPIRICAL_POSTERIOR).
   After this refresh the ew payload row's ONLY missing edge is
   UNCERTAINTY_PROTOCOL -- i.e. exactly the W export certificate, the true
   frontier -- even though the coarse label still reads EVALUATOR_MISSING.
   Do NOT flip uncertainty_protocol_declared until the certificate genuinely
   exists: with it True the route exports SOLVED_GLOBAL_P (verified), which
   is precisely the honest-blocked state the terminal-closure theorem locks.

Architecture-only module: no bank checks.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping

#: input_id -> refresh record. Fields:
#:   claim_text        replacement claim (CLAIM inputs)
#:   payload_updates   dict merged over the frozen payload (ROUTE_PAYLOAD inputs)
#:   provenance        the banked checks/modules that changed the disposition
#:   superseded        the frozen 2026-05-18 wording / flags, for the record
CLAIM_REFRESH: Dict[str, Dict[str, Any]] = {
    "claim:ew_global_export": {
        "claim_text": (
            "The one-loop OS-W evaluator is native and banked (M_W = 80.26 "
            "vs Denner's published 80.23, check_T_w_trace_native_mw_"
            "reproduces_denner [P]); the trace-to-scheme transport theorem "
            "is banked [P_transport_theorem]. The certificate-complete "
            "loop-sum export is ADJUDICATED at the v15.1 boundary: the four "
            "export certificates belong to the deprecated loop-sum route, "
            "and Delta-r_rem -- the only content they would add -- has no "
            "scheme-free standalone measurement (check_T_w_os_delta_r_rem_"
            "principled_terminal_boundary [P_boundary]). The physics is "
            "carried by the native distinction route: M_W = 80.3336 GeV "
            "from the banked check_L_W_mass [P], 0.044 percent from "
            "measured, no loop sum."
        ),
        "provenance": ["check_T_w_os_delta_r_rem_principled_terminal_boundary",
                        "check_L_W_mass",
                        "check_T_w_trace_native_mw_reproduces_denner",
                        "trace_to_scheme_transport_theorem"],
        "superseded": "EW APF_TRACE physical scheme masses are exported to global P. (2026-05-18)",
    },
    "claim:ew_local_trace": {
        "claim_text": (
            "EW trace-sector local closure is banked [P_local]; the W "
            "on-shell route terminal-closure theorem is banked "
            "[P_w_os_route_terminal_closure] and the one-loop M_W "
            "evaluation is native [P]. Only physical export to global P "
            "remains OPEN, on the export certificate."
        ),
        "provenance": ["w_os_route_terminal_closure",
                        "check_T_w_trace_native_mw_reproduces_denner"],
        "superseded": "EW trace-sector local APF_TRACE closure is banked as P_local. (2026-05-18)",
    },
    "claim:dark_runtime": {
        "claim_text": (
            "The dark Route-C MCMC posterior lane admission contract is "
            "banked with declared convergence diagnostics (R-1 <= 0.01, "
            "ESS >= 200, four chains) and fail-closed partial-chain and "
            "profile-MAP guards; the APF2 evaluator adapter and posterior "
            "certifier are banked. Posterior P awaits an admitted result "
            "pack meeting the declared thresholds (Gates 3/4 -- empirical "
            "runtime artifacts, not derivation)."
        ),
        "provenance": ["dark_mcmc_posterior_lane_admission",
                        "dark_posterior_certifier", "dark_apf2_real_adapter"],
        "superseded": "Dark sector Cobaya runtime completed but posterior convergence is still under review. (2026-05-18)",
    },
    "claim:gauge_fiber": {
        "claim_text": (
            "The within-interface gauge-orbit quotient is closed "
            "(check_T_ew_load_placement_P [P], v24.3.247); the "
            "across-interface connection is adjudicated gauge-variant "
            "convention (check_T_gauge_connection_is_gauge_variant_"
            "convention_P [P_structural_reading]), with the per-region-vs-"
            "diagonal fork localized and contained "
            "(check_T_across_frame_fork_localized [P_structural]) and the "
            "across_region (no-B) row honestly OPEN."
        ),
        "provenance": ["check_T_ew_load_placement_P",
                        "check_T_gauge_connection_is_gauge_variant_convention_P",
                        "check_T_across_frame_fork_localized"],
        "superseded": "Gauge group appears as a fiber automorphism with cocycle descent. (2026-05-18)",
    },
    "claim:horizon_cost": {
        "claim_text": (
            "Horizon area as fiber-cost with capacity bound is banked via "
            "the fiber-cost classifier; the area-law/microstate identity "
            "is COMPUTED, not asserted (check_T_horizon_arealaw_microstate_"
            "consistency [P], v24.3.272 corrigendum: A/4 = 3 pi/(Lambda G) "
            "= 102^61 with S_dS = ln(A/4) = 282, two distinct identities)."
        ),
        "provenance": ["check_T_horizon_arealaw_microstate_consistency",
                        "horizon_fiber_cost_classifier"],
        "superseded": "Horizon area is represented as fiber-cost with capacity bound. (2026-05-18)",
    },
    "payload:ew_transport_open": {
        "payload_updates": {
            "evaluator_map_found": True,          # native PV/OS-W evaluators banked [P]
            "codomain_transport_found": True,     # trace_to_scheme_transport_theorem [P_transport_theorem]
            "counterterm_finite_parts_declared": True,  # w_trace_native_delta_r_mw_assembly [P]; NB admitted REAL rows stay open, bundled into the held UNCERTAINTY_PROTOCOL edge
            # uncertainty_protocol_declared stays False -- the TRUE residual
            # (the export certificate), honestly held.
        },
        "provenance": ["check_T_w_trace_native_mw_reproduces_denner",
                        "trace_to_scheme_transport_theorem",
                        "w_trace_native_delta_r_mw_assembly"],
        "superseded": "evaluator_map_found=False, codomain_transport_found=False, counterterm_finite_parts_declared=False (2026-05-18)",
    },
    # NOTE payload:dark_runtime_open is deliberately NOT refreshed: the dark
    # ledger reads route_built/run_completed/posterior_closed/robustness only
    # (interface_structure_discovery_engine.discover_ledger, route == "dark"),
    # and those frozen flags are still true-to-fact -- the residual IS the
    # Gates 3/4 result-pack admission. An evaluator_map_found flip would be a
    # no-op read by nothing: misleading provenance, not repair.
}


def apply_refresh(inputs):
    """Return (refreshed_inputs, applied_rows). Non-destructive: builds new
    AtlasInput objects for refreshed ids, passes everything else through."""
    from apf.interface_atlas import AtlasInput
    out, applied = [], []
    for inp in inputs:
        r = CLAIM_REFRESH.get(inp.input_id)
        if r is None:
            out.append(inp)
            continue
        if r.get("claim_text") is not None:
            new = AtlasInput(input_id=inp.input_id, kind=inp.kind,
                             route=inp.route, claim_text=r["claim_text"],
                             payload=inp.payload, axis=inp.axis)
        else:
            pl = dict(inp.payload or {})
            pl.update(r["payload_updates"])
            new = AtlasInput(input_id=inp.input_id, kind=inp.kind,
                             route=inp.route, claim_text=inp.claim_text,
                             payload=pl, axis=inp.axis)
        out.append(new)
        applied.append({"input_id": inp.input_id,
                        "provenance": list(r["provenance"]),
                        "superseded": r["superseded"]})
    return out, applied
