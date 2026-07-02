"""APF Interface Atlas v0.2 canonical input set -- vendored in-repo (v24.3.307).

Vendored from DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_INTERFACE_ATLAS_V02_FULL_REGISTRY_v1/
scripts/run_interface_atlas_v02.py (pack of 2026-05-18, codebase state v24.3.18), which is
git-ignored Drive-side reference material. Same fix-class as the 2026-06-17 dark-posterior
CLOSURE_STATEMENT vendoring (commit 00182f5): the live atlas runner
(apf/interface_atlas_live_runner.py) previously hard-depended on the bundle path and raised
FileNotFoundError from the git repo alone; the runner's own docstring named this refactor
("A future refactor could move assemble_inputs() into apf/ proper"). This module IS that
refactor. The bundle copy remains the archival original; this copy is the operational one.

Contents: the 42-input v0.2 set -- canonical_atlas_inputs() (12 baseline inputs over 8
ClaimRoute classes) + 14 mass-sector + 6 dark-sector + 3 gravity + 2 cosmogenesis/evaporation
+ 2 neutrino + 3 architecture claims. Claim texts mirror the corpus dispositions as of
LATEST-44..87; they are structural atlas probes, not live grade assertions -- the atlas
types obstruction classes from the claim structure.

Architecture-only module: no bank checks. Consumed by apf/interface_atlas_live_runner.py
and apf/ie_onboarding_registry.py.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from apf.interface_atlas import (
    AtlasInput, AtlasInputKind, build_interface_atlas, canonical_atlas_inputs,
)


def _claim(input_id: str, claim_text: str) -> AtlasInput:
    return AtlasInput(
        input_id=input_id,
        kind=AtlasInputKind.CLAIM,
        route=None,
        claim_text=claim_text,
        payload=None,
    )


# Mass-sector sub-routes (14 routes from LATEST-66 Mass Sector Closure Registry)
MASS_SECTOR_CLAIMS = [
    _claim(
        "mass:route01_charged_lepton_pole",
        "The charged-lepton pole-mass triplet (m_e, m_mu, m_tau) closes locally "
        "at APF envelope with QED truncation covariance admitted; full multi-loop "
        "QED ledger remains external. EW trace and scheme transport are clean."
    ),
    _claim(
        "mass:route02_charged_lepton_qed_running",
        "The charged-lepton QED-running codomain has a typed transport route but "
        "full numeric running export awaits external QED constants ledger import. "
        "EW trace closure is locally clean; codomain transport is open."
    ),
    _claim(
        "mass:route03_charm_msbar_self_scale",
        "The charm MSbar self-scale mass m_c(m_c) closes as P_export_candidate "
        "with covariance admitted at the PDG 90% CL window. EW trace and codomain "
        "transport move cleanly; counterterm and uncertainty protocol are declared."
    ),
    _claim(
        "mass:route04_charm_pole",
        "The charm pole codomain is structurally rejected via greater-than-10-sigma "
        "knockout; pole-mass interpretation is inadmissible for the APF charm anchor "
        "which is short-distance-like."
    ),
    _claim(
        "mass:route05_bottom_msbar_self_scale",
        "The bottom MSbar self-scale mass m_b(m_b) closes as P_export_candidate "
        "with covariance admitted at the PDG 90% CL window. EW trace, codomain "
        "transport, and counterterm convention all clean."
    ),
    _claim(
        "mass:route06_bottom_pole",
        "The bottom pole codomain is structurally rejected; pole-mass interpretation "
        "is inadmissible for the APF bottom anchor which is short-distance-like."
    ),
    _claim(
        "mass:route07_top_external_msr",
        "The top external high-scale MSR codomain is admitted at P_export_candidate "
        "with R_star = 85.857 GeV APF-native scale selector; EW trace and codomain "
        "transport clean."
    ),
    _claim(
        "mass:route08_top_msr_ew_transport",
        "The top MSR-EW transport closure at R_EW = M_W/(2pi) = 12.790 GeV closes "
        "locally with source-certified TRACE anchor; EW trace clean; QCD coefficient "
        "evaluator is external content named without consumption."
    ),
    _claim(
        "mass:route09_top_pole_mc",
        "The top pole/MC codomain is quarantined: 4-loop QCD coefficient evaluation "
        "yields a 30-sigma deterioration; the pole route is the wrong codomain for "
        "auditing a direct/MC-style top mass."
    ),
    _claim(
        "mass:route10_light_quark_flag_external_kernel",
        "The light-quark MSbar(2 GeV) export closes via external FLAG kernel "
        "transport at P_imported_one_route; the APF-only numeric U_chi/lat evaluator "
        "is structurally external. EW trace clean; counterterm and uncertainty "
        "protocol declared."
    ),
    _claim(
        "mass:route11_mw_on_shell_dizet",
        "M_W on-shell route closes as P_imported_physical_one_route_closure via "
        "DIZET-mediated SM-loop content. APF-internal full first-principles SM-loop "
        "derivation remains open. EW trace anchor M_W^TRACE = 80.362164 GeV; "
        "residual vs CMS26 = 1.96 MeV (z=0.198), codomain transport clean."
    ),
    _claim(
        "mass:route12_sin2_theta_w_source_identity",
        "sin^2(theta_W) source identity 3/13 closes as P_internal: trace-sector "
        "source identity with no external scheme content. EW trace clean."
    ),
    _claim(
        "mass:route13_sin2_theta_eff_bsy_four_channel",
        "sin^2(theta_eff) four-channel effective-mixing closure at "
        "3/13 + 4/5063 = 0.231559 closes as P_imported_one_route via Bodek-Seo-Yang "
        "reanalysis comparator; residual = -0.003 vs measured; EW trace clean."
    ),
    _claim(
        "mass:route14_sin2_theta_w_mass_ratio_identity",
        "sin^2(theta_W) on-shell mass-ratio identity 1 - M_W^2/M_Z^2 closes as "
        "P_internal at the on-shell mass-ratio relation; EW trace clean."
    ),
]


# Dark-sector sub-routes
DARK_SECTOR_CLAIMS = [
    _claim(
        "dark:route_w2_a_background",
        "The APF2 second-order dark-energy response w_2(a) = -1 + 3/61 - (16/61)*a "
        "- (21/8)*a*(a - 1/3)*(1-a) closes internally with rational coefficients "
        "structurally derived from endpoint uniqueness + barycentric pivot + capacity "
        "response ratio. Codomain transport via CAMB PPF moves cleanly; ledger clean; "
        "no smuggling."
    ),
    _claim(
        "dark:route_cross_sn_profile_probe",
        "The APF2 cross-SN profile-probe achieves 4-of-4 ACCEPT at 95% across native "
        "+ PantheonPlus + Union3 + DESY5. Cobaya runtime completed but DESI full-shape "
        "exact-runtime gate G5 remains open; CAMB rejected tau as an unrecognized "
        "parameter; the monkeypatch never fired; native physical-likelihood smoke "
        "remains Export = 0. Robust empirical P is not asserted."
    ),
    _claim(
        "dark:route_desi_full_shape_exact",
        "DESI full-shape exact runtime closure (G3) is the next decisive gate but "
        "remains environmentally blocked: APF2 configs are ready, runner is verified, "
        "but the external DESI bindings + Planck likelihood stack required by Cobaya "
        "are not available in the current sandbox. Codomain transport clean; evaluator "
        "map missing pending external content."
    ),
    _claim(
        "dark:route_full_growth_likelihood",
        "Full-growth likelihood covariance/fiducial/AP closure (G4) remains partial: "
        "1 of 4 sub-blockers closed via the DESI DR1 FS VAC import; 3 sub-blockers "
        "(survey covariance, fiducial/AP rescaling ledger, survey overlap accounting) "
        "remain open. The growth posterior evaluator is incomplete."
    ),
    _claim(
        "dark:route_dark_particle_id",
        "Dark particle identity remains open as guarded-by-design: 16-unit "
        "external-capacity sector has gross identity but no specific particle "
        "assignment. Four portal forks (Higgs, neutrino, dark photon, dark "
        "self-interaction) are APF-admissible-but-not-derived; SM gauge channels are "
        "excluded by Theorem B; gravitational channel mandatory by Theorem A."
    ),
    _claim(
        "dark:route_modified_gravity",
        "Modified-gravity export is structurally blocked: the framework currently "
        "exports GR-limit geometry with APF source corrections, not a non-GR "
        "geometric correction operator. Bianchi consistency gate names six "
        "conditions that no APF-derived object currently satisfies."
    ),
]


# Gravity-sector sub-routes
GRAVITY_CLAIMS = [
    _claim(
        "gravity:route_gr_limit_full_close",
        "The gravity sector closes at GR-limit full-close grade per the 6-pack "
        "v24.3.x absorption: G_{mu nu} = 8 pi G (T_vis + T_D + T_2FCR + T_rad). "
        "Observable transport map clean for FRW, redshift, lensing, growth, GW "
        "propagation, ringdown. No non-GR geometric operator exported."
    ),
    _claim(
        "gravity:route_bianchi_rigidity",
        "Bianchi rigidity theorem closes; metric-side rigidity holds. Any future "
        "non-GR Delta G^APF correction operator requires six conditions: symmetric "
        "rank-2, divergence-free or specified exchange, APF-native coefficient, "
        "GR limit recovery, observable distinguishability from source-side "
        "corrections, no-smuggling. No APF-derived operator satisfies these."
    ),
    _claim(
        "gravity:route_ringdown_capacity_schema",
        "Ringdown closes at GR-baseline + capacity-schema grade. APF non-GR numeric "
        "ringdown correction remains Export = 0. The capacity interpretation "
        "provides typed source-side structure, not a modified-gravity prediction."
    ),
]


# Cosmogenesis / evaporation
COSMOGENESIS_CLAIMS = [
    _claim(
        "cosmogenesis:route_t1_t4_quartet",
        "Cosmogenic quartet T1-T4 closes the void-to-middle regime transition via "
        "Type II resolutions under L_irr; cumulative V_global accumulation theorem "
        "saturates at Omega_Lambda * C_total = dim V_global = 42 when all 61 slots "
        "resolve. No-GUT corollary forbids proton decay structurally."
    ),
    _claim(
        "evaporation:route_e1_e4_quartet",
        "Evaporation quartet E1-E4 closes the saturation-to-middle regime "
        "transition: cumulative-balance equation |V_global,local|_deposit = "
        "|V_global,local|_release + S_radiation. Page-curve turnover at "
        "half-evaporation derived from equipartition; positive observation NOT at "
        "half-evaporation falsifies."
    ),
]


# Neutrino sector
NEUTRINO_CLAIMS = [
    _claim(
        "neutrino:route_mbb_reconciliation",
        "Neutrino m_bb reconciliation closes locally for EW trace-sector closure; "
        "absolute mass scale remains conditional. Codomain transport clean; "
        "uncertainty protocol declared."
    ),
    _claim(
        "neutrino:route_dune_juno_hierarchy",
        "Neutrino mass hierarchy is the watching codomain: DUNE/JUNO are the named "
        "external evaluators that would close the hierarchy assignment. APF-internal "
        "structural derivation is open; codomain transport is typed but evaluator "
        "map is missing."
    ),
]


# Architecture-level
ARCHITECTURE_CLAIMS = [
    _claim(
        "arch:route_rdfi_global_descent_kernel",
        "Representation descent full integration (RDFI, v24.3.11) closes Global APF "
        "physics = ker(Obs_APF) = im(Glob) as the zero-obstruction exact kernel of "
        "admissible representation descent over the ACC/interface base. 13-module "
        "stack at P_unification; substrate-global C* algebra is blocked by the "
        "2026-05-16 algebraic ceiling."
    ),
    _claim(
        "arch:route_defect_calculus_architecture",
        "The defect-calculus architecture (v24.3.18) closes 10 theorems at "
        "P_architecture binding finite continuability, preservation, resolution, "
        "obstruction, transport, and observable signatures into one calculus. The "
        "calculus is architecture/math only; it does not promote any physical claim, "
        "fit, prediction, or route beyond route-local certificates."
    ),
    _claim(
        "arch:route_interface_engine_operational",
        "The Interface Engine itself (v24.3.17 operational close) runs end-to-end "
        "against live framework state: registry-bridge round-trips through "
        "bank.REGISTRY's update interface cleanly; real adapters produce held-for-"
        "repair obligation packets; the atlas emits cross-sector findings. Engine "
        "audits structure, not physics."
    ),
]


def assemble_inputs() -> tuple[AtlasInput, ...]:
    """Build the full v0.2 input set."""
    return (
        canonical_atlas_inputs()  # 12 baseline inputs covering 8 ClaimRoute classes
        + tuple(MASS_SECTOR_CLAIMS)
        + tuple(DARK_SECTOR_CLAIMS)
        + tuple(GRAVITY_CLAIMS)
        + tuple(COSMOGENESIS_CLAIMS)
        + tuple(NEUTRINO_CLAIMS)
        + tuple(ARCHITECTURE_CLAIMS)
    )
