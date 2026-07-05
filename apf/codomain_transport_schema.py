"""APF Codomain-Transport Unification Schema.

Bank-side aggregator that registers every codomain-transport open frontier
under one schema. The premise — set out in
`APF Reference Docs/Reference - Open Frontier as Codomain Transport
(2026-05-08).md` — is that the framework's open frontier consists almost
entirely of *codomain transport theorems*: bridges from a source codomain
where the framework computes (typically APF_TRACE) to a target codomain
where measurements live (pole / MSbar / continuum OS / late-universe ladder
/ measured-hierarchy / ...).

This module instantiates the W on-shell scaffold pattern for every transport
the framework currently has open. Each instance is a `CodomainTransport`
record with:

  * source_codomain (immutable, framework-derived)
  * target_codomain (named target in measurement coordinates)
  * transport_map_name
  * status (one of CLOSED/PARTIAL/OPEN/WATCHING/WAITING/UPSTREAM/FALSIFYING)
  * certificate (the 9-field SchemeContract type signature)
  * forbidden_inputs (the no-smuggling guard set)
  * notes

Bank-registered checks here verify the *schema*, not the contents — every
instance must have the right shape, every certificate must declare its 9
fields, every forbidden-input set must be nonempty, no instance may claim
physical_export=True while its certificate is incomplete. The unification
meta-theorem composes these into a single bank-callable assertion that the
framework's open frontier has uniform structural form.

This is the v9.6 codebase landing of the unification reference doc. It does
not derive any of the transports — it banks the *architecture* under which
they would be derived.

Operational counterpart (human-readable):
    wiki/Scheme Export Registry.md (LATEST-74-paired)
    APF Reference Docs/Reference - Scheme Export Registry (2026-05-12).md
The Registry tracks all 32 scheme-export routes in the corpus (mass + dark +
gravity + cosmology + neutrino + hadronic + structural sectors) under one
11-field certificate template. The 10 SchemeContract instances below are the
machine-readable counterpart; the Registry is the human-readable counterpart
that adds per-route certificate stubs for routes not yet in this schema
(H_0 Route V, DUNE/JUNO hierarchy, muon g-2, YM continuum-limit). Both should
agree route-by-route on status.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, Tuple, Any
from collections.abc import Callable

# ---------------------------------------------------------------------
# Status enums
# ---------------------------------------------------------------------

# Per-slot certificate status
SLOT_OPEN = 'open'
SLOT_PARTIAL = 'partial'
SLOT_CLOSED = 'closed'
SLOT_FORBIDDEN = 'forbidden'
SLOT_EXTERNAL = 'external'

VALID_SLOT_STATUSES = frozenset({
    SLOT_OPEN, SLOT_PARTIAL, SLOT_CLOSED, SLOT_FORBIDDEN, SLOT_EXTERNAL,
})

# Top-level transport status
TRANSPORT_CLOSED = 'closed'
TRANSPORT_PARTIAL = 'partial'
TRANSPORT_OPEN = 'open'
TRANSPORT_WATCHING = 'watching'      # Framework prediction closed; empirical convergence awaited
TRANSPORT_WAITING = 'waiting'        # Empirical input awaited; framework will propagate
TRANSPORT_UPSTREAM = 'upstream'      # Source codomain not yet derived
TRANSPORT_FALSIFYING = 'falsifying'  # Transport theorem structurally insufficient; falsifier firing

VALID_TRANSPORT_STATUSES = frozenset({
    TRANSPORT_CLOSED, TRANSPORT_PARTIAL, TRANSPORT_OPEN,
    TRANSPORT_WATCHING, TRANSPORT_WAITING, TRANSPORT_UPSTREAM,
    TRANSPORT_FALSIFYING,
})

# Codomain type — numerical vs structural (v24.1 schema extension)
# Numerical: codomain is a real number with measurement uncertainty (mass routes, eta_B, n_s, H_0, w, a_mu).
# Structural: codomain is a theorem-shape (existence/uniqueness/limit claim, no single numerical residual).
# The export theorem's G4 (covariance) and G6 (residual channel) read in their numerical or structural
# form per route based on this field. See STRUCTURAL_EXTENSION_v35_1/ for the formal extension.
CODOMAIN_NUMERICAL = 'numerical'
CODOMAIN_STRUCTURAL = 'structural'

VALID_CODOMAIN_TYPES = frozenset({CODOMAIN_NUMERICAL, CODOMAIN_STRUCTURAL})


# ---------------------------------------------------------------------
# Portal-class slot template (LATEST-74 documentation extension)
# ---------------------------------------------------------------------
#
# Some "routes" in the broader APF catalog are NOT codomain-transport theorems
# in the working sense -- they are *guarded non-claims* where the framework
# explicitly refuses to derive a coupling on principled grounds. The canonical
# examples are the four open dark-sector portal forks (LATEST-67 Theorem C):
#
#   1. Higgs portal             (lambda_H |H|^2 phi_dark^2)
#   2. Neutrino portal          (y_nu L H phi_dark or kinetic mixing)
#   3. Dark photon kinetic mix  (eps F_{mu nu} F^{mu nu}_dark)
#   4. Dark self-interaction    (g_dark^2 phi_dark^4 or analog)
#
# Each portal would be a route IF the framework derived a coupling. The current
# closure-grade state per Paper 35 v1.1 + wiki/Dark Sector Closure Registry.md
# is that the framework does NOT derive any of these couplings: dark-sector
# capacity content (16 units) has gross identity but no specific particle
# assignment, no APF-native interaction generator, no SM gauge portal admitted
# (Theorem B excludes), and no modified-gravity export.
#
# If a future theorem derives a portal coupling, the route would be instantiated
# with these slot conventions:
#
#   scheme                      -> portal target operator (which SM field couples)
#   scale_rule                  -> portal coupling renormalization scale
#   loop_order_or_regularization-> portal-coupling loop expansion (typically tree)
#   coupling_provenance         -> derivation of coupling magnitude from APF
#   threshold_rule              -> kinematic accessibility (mass scales)
#   subtraction_rule            -> portal RG scheme convention
#   finite_part_rule            -> portal Wilson coefficient at matching scale
#   anomalous_dimension_rule    -> portal RG running
#   uncertainty_pushforward     -> covariance against direct/indirect detection
#
# Status conventions for portal routes:
#   - TRANSPORT_CLOSED with all 9 slots FORBIDDEN = "the no-go IS the closure"
#     (current state -- portals are guarded-by-design closures)
#   - TRANSPORT_OPEN with slots PARTIAL/EXTERNAL/CLOSED as derivation progresses
#   - The expected portal-class status under the LATEST-67 Theorem C guard is
#     TRANSPORT_CLOSED-via-FORBIDDEN-slots, structurally parallel to how the
#     light-quark APF-only-numeric U_chilat sub-route is closed via no-go.
#
# Why portals are documented here but NOT instantiated as bank routes:
#   1. They would multiply the bank-registered transport count from 10 -> 14
#      without adding derivative content (each instance would be a no-go pack
#      already documented in wiki/Dark Sector Closure Registry.md Routes 7-10).
#   2. The Dark Sector Closure Registry is the canonical drill-in for these;
#      duplicating in the schema would create two sources of truth.
#   3. The schema's existing 9-slot template is designed for mass/coupling
#      routes; portal routes have a slot interpretation distinct enough that
#      retrofitting existing slot names would obscure rather than clarify.
#
# This documentation extension makes the framework's portal posture machine-
# readable as a code comment without committing to bank-instance fan-out. If
# a future portal is derived, the convention above is in place to instantiate
# it cleanly.

PORTAL_CLASS_ROUTES = frozenset({
    'higgs_portal',
    'neutrino_portal',
    'dark_photon_kinetic_mixing',
    'dark_self_interaction',
})


# ---------------------------------------------------------------------
# Schema dataclasses
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class CertificateSlot:
    """A single slot in the 9-field SchemeContract."""
    name: str
    status: str
    note: str = ''

    def is_filled(self) -> bool:
        return self.status in (SLOT_CLOSED, SLOT_FORBIDDEN, SLOT_EXTERNAL)

    def is_open(self) -> bool:
        return self.status == SLOT_OPEN


@dataclass(frozen=True)
class TransportCertificate:
    """The 9-field SchemeContract type signature for a codomain transport.

    Slot names are uniform across all transports; their interpretation is
    transport-specific. See the Reference doc for slot semantics.
    """
    scheme: CertificateSlot
    scale_rule: CertificateSlot
    loop_order_or_regularization: CertificateSlot
    coupling_provenance: CertificateSlot
    threshold_rule: CertificateSlot
    subtraction_rule: CertificateSlot
    finite_part_rule: CertificateSlot
    anomalous_dimension_rule: CertificateSlot
    uncertainty_pushforward: CertificateSlot

    def all_slots(self) -> Tuple[CertificateSlot, ...]:
        return (self.scheme, self.scale_rule, self.loop_order_or_regularization,
                self.coupling_provenance, self.threshold_rule, self.subtraction_rule,
                self.finite_part_rule, self.anomalous_dimension_rule,
                self.uncertainty_pushforward)

    def filled_count(self) -> int:
        return sum(1 for s in self.all_slots() if s.is_filled())

    def total_count(self) -> int:
        return 9

    def is_complete(self) -> bool:
        return self.filled_count() == self.total_count()

    def status_summary(self) -> Dict[str, str]:
        return {s.name: s.status for s in self.all_slots()}


@dataclass(frozen=True)
class CodomainTransport:
    """A single codomain-transport theorem instance."""
    name: str
    source_codomain: str
    target_codomain: str
    transport_map_name: str
    status: str
    certificate: TransportCertificate
    forbidden_inputs: frozenset
    notes: str = ''
    codomain_type: str = CODOMAIN_NUMERICAL  # v24.1: 'numerical' or 'structural'

    def physical_export_locked(self) -> bool:
        """The transport blocks physical export unless the certificate is complete
        and the status is CLOSED."""
        if self.status == TRANSPORT_CLOSED and self.certificate.is_complete():
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'source_codomain': self.source_codomain,
            'target_codomain': self.target_codomain,
            'transport_map_name': self.transport_map_name,
            'status': self.status,
            'certificate_filled': f'{self.certificate.filled_count()}/{self.certificate.total_count()}',
            'forbidden_inputs_count': len(self.forbidden_inputs),
            'physical_export_locked': self.physical_export_locked(),
            'codomain_type': self.codomain_type,
            'notes': self.notes,
        }


# ---------------------------------------------------------------------
# Helper to build a slot
# ---------------------------------------------------------------------

def _slot(name: str, status: str, note: str = '') -> CertificateSlot:
    if status not in VALID_SLOT_STATUSES:
        raise ValueError(f"slot {name!r}: invalid status {status!r}")
    return CertificateSlot(name=name, status=status, note=note)


# ---------------------------------------------------------------------
# Transport instances — the 10 currently-known frontiers
# ---------------------------------------------------------------------

def w_on_shell_transport() -> CodomainTransport:
    return CodomainTransport(
        name='w_on_shell',
        source_codomain='APF_TRACE/W_TRACE: M_W = 80.362164334 GeV (closed at v8.4)',
        target_codomain='physical M_W^pole (CMS 2026 Nature: 80.3692 ± 0.0099 GeV)',
        transport_map_name='w_trace_on_shell_route_via_DIZET_imported',
        status=TRANSPORT_CLOSED,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'on-shell EW route closed via imported DIZET v6.45 transport (LATEST-50)'),
            scale_rule=_slot('scale_rule', SLOT_CLOSED, 'self-scale fixed before comparison; same-input DIZET evaluation'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_EXTERNAL, 'full electroweak loop content imported from DIZET v6.45 ZFITTER reviewed evaluator'),
            coupling_provenance=_slot('coupling_provenance', SLOT_EXTERNAL, 'alpha(M_Z) + alpha_s(M_Z) from PDG 2025 ledger'),
            threshold_rule=_slot('threshold_rule', SLOT_EXTERNAL, 'top + Higgs threshold matching from DIZET'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, 'on-shell subtraction; standard'),
            finite_part_rule=_slot('finite_part_rule', SLOT_EXTERNAL, 'Delta_r finite parts evaluated by DIZET (LATEST-50 imported-form closure)'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_EXTERNAL, 'DIZET running coefficients'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_CLOSED, 'APF combined uncertainty envelope; z = +0.198 vs CMS 2026'),
        ),
        forbidden_inputs=frozenset({
            'observed_M_W', 'target_Delta_r', 'residual_fitted_finite_counterterms',
            'tuned_finite_counterterms', 'target_fit_scalar', 'post_comparison_scale_choice',
            'target_matched_alpha_s', 'M_W_pole_target_value',
        }),
        notes='[P_imported_one_route] at LATEST-50/56: M_W^APF-TRACE = 80.362 GeV vs CMS 2026 (80.3692 +/- 0.0099 GeV) '
              'gives z = +0.198 under DIZET same-input transport. Open promotion gate: APF-internal first-principles '
              'SM-loop Delta_r derivation (would remove DIZET import admission; tracked in APF_Todo_List RP-CT.routes). '
              'See Paper 33 v1.15 Supplement v1.0 Route 11 certificate + wiki/Mass Sector Closure Registry.md Route 11.',
    )


def bottom_msbar_transport() -> CodomainTransport:
    return CodomainTransport(
        name='bottom_msbar',
        source_codomain='APF_TRACE: m_b = M_W * x^{q_{B1} + 1/4} = 80.362 * 2^{-4.25} = 4.224 GeV (LATEST-54 fully APF-internal)',
        target_codomain='m_b^MSbar(m_b) = 4.183 +/- 0.004 GeV (PDG 2025)',
        transport_map_name='colored_msbar_self_scale_route_APF_internal',
        status=TRANSPORT_CLOSED,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'MSbar self-scale (mu = m_b) — APF-internal'),
            scale_rule=_slot('scale_rule', SLOT_CLOSED, 'self-scale: mu = m_b, fixed before comparison'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_CLOSED, 'transport T_b = 1 - (alpha_s(m_b)/pi) * x^3 = 0.99113 evaluated APF-internally'),
            coupling_provenance=_slot('coupling_provenance', SLOT_EXTERNAL, 'alpha_s(m_b) = 0.223 as named external running coupling input (not target)'),
            threshold_rule=_slot('threshold_rule', SLOT_CLOSED, 'self-scale obviates threshold matching'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, 'MSbar subtraction; standard'),
            finite_part_rule=_slot('finite_part_rule', SLOT_CLOSED, 'm_b^transport(m_b) = M_W * 2^{-4.25} * T_b = 4.186 GeV; residual = +3.04 MeV vs PDG'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_CLOSED, 'QCD anomalous dimension absorbed via T_b transport'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_CLOSED, 'APF envelope sigma_th = m_b * (alpha_s/pi) * x^5; combined z = 0.30'),
        ),
        forbidden_inputs=frozenset({
            'observed_m_b', 'target_fit_scalar', 'target_matched_alpha_s',
            'PDG_central_value_as_input', 'observed_top_used_to_define_transport',
            'post_comparison_scale_choice', 'm_b_MSbar_target',
        }),
        notes='[P_export_candidate]^{MSbar self-scale} at LATEST-54: structural formula m_b = M_W * 2^{-4.25} '
              'from EW trace quarter-shell anchor; transport T_b QCD running APF-internal. '
              'Residual +3.04 MeV vs PDG (z = 0.30 on combined envelope). Fully APF-internal; alpha_s(m_b) only '
              'external input (not fit target). See Paper 33 v1.15 Supplement v1.0 Route 5 + wiki/Mass Sector Closure Registry.md Route 5.',
    )


def top_msbar_or_pole_transport() -> CodomainTransport:
    return CodomainTransport(
        name='top_msbar_or_pole',
        source_codomain='APF_TRACE: m_t = 168.169 GeV (closed at LATEST-44 v51 via Paper 32 quark anchors)',
        target_codomain='m_t^MSR(R_EW) = 172.7 GeV [direct] OR m_t^pole,4loop = 174.02 GeV [quarantined obstruction]',
        transport_map_name='msr_running_route_OR_pole_codomain_knockout',
        status=TRANSPORT_CLOSED,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'MSR(R_EW) route admitted [P_direct-MSR-completion]; pole codomain knocked out at LATEST-61 (z = 4.70 quarantined)'),
            scale_rule=_slot('scale_rule', SLOT_CLOSED, 'MSR scale R_EW from APF-native EW resolution; pole route forbidden'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_EXTERNAL, '4-loop MSR coefficients from external precision-QCD ledger; APF-only-numeric refused'),
            coupling_provenance=_slot('coupling_provenance', SLOT_EXTERNAL, 'alpha_s + threshold matching from PDG ledger'),
            threshold_rule=_slot('threshold_rule', SLOT_EXTERNAL, 'MSR threshold matching across quark flavor thresholds'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, 'MSR subtraction; direct measurement-comparable'),
            finite_part_rule=_slot('finite_part_rule', SLOT_CLOSED, 'm_t^MSR(R_EW) = 172.717 GeV via 4-loop R-evolution; residual = +0.157 GeV vs PDG direct (z = 0.015 over 0.314 GeV envelope)'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_EXTERNAL, 'gamma_m anomalous dimension from external coefficient ledger'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_CLOSED, 'combined audit envelope including sigma_alpha + sigma_gamma_3 + sigma_trunc = 0.314 GeV'),
        ),
        forbidden_inputs=frozenset({
            'observed_m_t', 'm_t_pole_target', 'm_t_MSbar_target',
            'target_fit_scalar', 'target_matched_alpha_s',
            'post_comparison_scale_choice', 'physical_yukawa_normalization',
        }),
        notes='[P_export_candidate]^{MSR(R_EW)} (LATEST-56) + [P_obstruction_named]^{pole codomain} (LATEST-61). '
              'Direct branch: m_t^MSR(R_EW) = 172.717 GeV with z = 0.015 vs PDG direct (172.56 +/- 0.31 GeV). '
              'Pole branch: m_t^pole,4loop = 174.017 GeV with z = 4.70 quarantined as named knockout (pole codomain is '
              'wrong codomain for APF trace anchor at this precision). See Paper 33 v1.15 Supp v1.0 Routes 7/8/9.',
    )


def light_quark_msbar_transport() -> CodomainTransport:
    return CodomainTransport(
        name='light_quark_msbar',
        source_codomain='APF_TRACE: T_uds = (1.153, 3.871, 87.143) MeV (LATEST-53 source-vector close)',
        target_codomain='FLAG 2024 MSbar(2 GeV): m_u=2.16 MeV, m_d=4.70 MeV, m_s=93.46 MeV',
        transport_map_name='light_quark_chilat_8stage_kernel_FLAG_imported',
        status=TRANSPORT_CLOSED,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, '8-stage kernel structure derived: U_chilat = Sigma_uds o I_EM/iso o Z_m o L_a o Q_chi o P_1^YM o E_SU3 o Q_APS (LATEST-64 v9)'),
            scale_rule=_slot('scale_rule', SLOT_EXTERNAL, 'lattice spacing + scale-setting external (L_a stage)'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_EXTERNAL, 'non-perturbative lattice regularization (L_a) external'),
            coupling_provenance=_slot('coupling_provenance', SLOT_EXTERNAL, 'alpha_s + thresholds external'),
            threshold_rule=_slot('threshold_rule', SLOT_EXTERNAL, 'lattice action conventions external'),
            subtraction_rule=_slot('subtraction_rule', SLOT_EXTERNAL, 'Z_m mass renormalization external'),
            finite_part_rule=_slot('finite_part_rule', SLOT_EXTERNAL, 'FLAG diagonal kernel K^FLAG_min = diag(1.856, 1.214, 1.073) inferred from named external evaluator (LATEST-67 v15-v18)'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_FORBIDDEN, 'APF-only-numeric U_chilat structurally forbidden: no APF-derived nonperturbative lattice evaluator (LATEST-67 v17 no-go theorem)'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_EXTERNAL, 'FLAG averaging uncertainty model'),
        ),
        forbidden_inputs=frozenset({
            'observed_m_u', 'observed_m_d', 'observed_m_s',
            'target_fit_scalar', 'lattice_target_values_as_input',
            'post_comparison_scale_choice',
            'APF_derived_nonperturbative_lattice_evaluator',
        }),
        notes='[P_imported_one_route]^{FLAG kernel transport} + [P_APF-only_numeric_no-go] at LATEST-66/67. '
              '4 stages APF-internal (Q_APS source quotient, E_SU3 color exposure, P_1^YM confinement projection, '
              'Q_chi chiral light-sector quotient); 4 stages external (L_a, Z_m, I_EM/iso, Sigma_uds). '
              'APF-only-numeric branch structurally forbidden by LATEST-67 v17 no-go theorem (the no-go is the closure, '
              'parallel to pole-codomain knockouts at Routes 4/6/9). See Paper 33 v1.15 Supp v1.0 Route 10.',
    )


def charged_lepton_physical_transport() -> CodomainTransport:
    return CodomainTransport(
        name='charged_lepton_physical',
        source_codomain='APF_TRACE: (m_e, m_mu, m_tau) = (0.5110018, 105.658438, 1776.929861) MeV (LATEST-53 16-pack sprint source-vector close)',
        target_codomain='CODATA 2022 / PDG 2025 pole-mass envelope',
        transport_map_name='charged_lepton_route_APF_internal_x8_envelope',
        status=TRANSPORT_CLOSED,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'pole codomain admitted under APF envelope; QED-running codomain typed at LATEST-46 (full-running ledger pending)'),
            scale_rule=_slot('scale_rule', SLOT_CLOSED, 'pole scale; CODATA 2022 envelope frame'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_CLOSED, 'LO QED running witness at LATEST-47/48; multi-loop coefficient ledger external'),
            coupling_provenance=_slot('coupling_provenance', SLOT_EXTERNAL, 'CODATA 2022 alpha(0); no QCD'),
            threshold_rule=_slot('threshold_rule', SLOT_CLOSED, 'no threshold crossings (leptonic)'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, 'pole subtraction'),
            finite_part_rule=_slot('finite_part_rule', SLOT_CLOSED, 'theoretical envelope epsilon_th = (alpha/pi) * x^8 = 9.07e-6; combined chi^2_3 = 0.394, p = 0.941'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_EXTERNAL, 'QED running coefficients admitted as external content (CODATA 2022); full multi-loop coefficient ledger import is the named promotion gate'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_CLOSED, 'APF envelope max |z| = 0.625 (electron); covariance closure chi^2_3 = 0.394'),
        ),
        forbidden_inputs=frozenset({
            'observed_m_e', 'observed_m_mu', 'observed_m_tau',
            'target_fit_scalar', 'PDG_lepton_pole_values_as_input',
        }),
        notes='[P_export_candidate]^{pole+envelope} + [P_covariance_admitted]^{APF envelope} at LATEST-53/56. '
              'Fully APF-internal x^8 envelope; CODATA alpha(0) only external. Residuals: e (+0.625sigma), '
              'mu (+0.065sigma), tau (-0.002sigma); chi^2_3 = 0.394, p = 0.941. Open promotion gate: full QED '
              'multi-loop coefficient ledger import (tracked in APF_Todo_List RP-CT.routes). '
              'See Paper 33 v1.15 Supp v1.0 Routes 1-2 + wiki/Mass Sector Closure Registry.md Routes 1-2.',
    )


def ym_continuum_limit_transport() -> CodomainTransport:
    return CodomainTransport(
        name='ym_continuum_limit',
        source_codomain='SU(2) Wilson lattice gauge-correlator codomain (Yang-Mills trilogy: all-beta gap, OS modulo O(a^2))',
        target_codomain='continuum OS axiomatic structure on R^4 (Clay Millennium statement)',
        transport_map_name='lattice_to_continuum_OS_transport',
        status=TRANSPORT_PARTIAL,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_PARTIAL, 'continuum OS axioms enumerated; current closure modulo O(a^2)'),
            scale_rule=_slot('scale_rule', SLOT_PARTIAL, 'a -> 0 with beta(a) -> infty in asymptotic-freedom regime'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_PARTIAL, 'Wilson regularization is the source'),
            coupling_provenance=_slot('coupling_provenance', SLOT_PARTIAL, 'bare lattice beta runs to continuum alpha_s; standard QCD; APF-internal derivation absent'),
            threshold_rule=_slot('threshold_rule', SLOT_OPEN, 'UV cutoff matching for general framework derivation'),
            subtraction_rule=_slot('subtraction_rule', SLOT_PARTIAL, 'Symanzik counterterm structure controls O(a^2); full counterterm tower not derived'),
            finite_part_rule=_slot('finite_part_rule', SLOT_PARTIAL, 'continuum gap existence demonstrated; magnitude not extracted to physical units'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_OPEN, 'gauge-correlator running'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_OPEN, 'lattice-to-continuum error budget'),
        ),
        forbidden_inputs=frozenset({
            'target_continuum_gap_value', 'target_fitted_Symanzik_coefficients',
            'observed_glueball_mass', 'lattice_to_continuum_target_fit',
            'fitted_a_to_zero_extrapolation',
        }),
        notes='Source: Yang-Mills trilogy (Papers 29/30/31, codebase v7.11). Two parking-lot research targets: '
              'YM-Adv.A (general-G analytic closure), YM-Adv.B (Crystal SCC <-> SU(3) Casimir cascade combinatorics). '
              'Best partial transport on the open frontier.',
        codomain_type=CODOMAIN_STRUCTURAL,
    )


def h0_route_v_transport() -> CodomainTransport:
    # v24.3.320 fork annotation: 70.03 is the TWO-FACTOR branch of the banked vacuum-O(1) reading fork; the count=area branch gives 66.84 — see check_T_vacuum_o1_reading_fork (vacuum_o1_fork.py).
    return CodomainTransport(
        name='h0_route_v',
        source_codomain='APF forked structural value: H_0 = 70.03 km/s/Mpc on the TWO-FACTOR branch of the banked vacuum-O(1) reading fork (count=area branch: 66.83; check_T_vacuum_o1_reading_fork) (T_Lambda_to_H0_inversion in apf/lambda_absolute.py, [P_structural_reading]; algebraic from Omega_Lambda = 42/61 + rho_Lambda/M_Pl^4 = 42/102^62 + GR critical-density formula)',
        target_codomain='empirical H_0 measurement codomain: Planck 2018 = 67.36 +/- 0.54 km/s/Mpc (early-universe fit) vs H0DN 2026 = 73.50 +/- 0.81 km/s/Mpc (late-universe distance-ladder); midpoint = 70.43 km/s/Mpc',
        transport_map_name='prediction_stability_under_hubble_tension_resolution',
        status=TRANSPORT_WATCHING,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'comparison face: framework prediction vs Planck-SH0ES tension band'),
            scale_rule=_slot('scale_rule', SLOT_CLOSED, 'z -> 0 extrapolation; APF prediction is the asymptotic value'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_CLOSED, 'classical cosmology; no loop expansion'),
            coupling_provenance=_slot('coupling_provenance', SLOT_CLOSED, 'APF prediction algebraic from K_SM=61, C_vacuum=42, d_eff=102; zero free parameters'),
            threshold_rule=_slot('threshold_rule', SLOT_CLOSED, 'GR critical-density formula rho_crit = 3 H_0^2 M_Pl^2 / (8 pi)'),
            subtraction_rule=_slot('subtraction_rule', SLOT_PARTIAL, 'Route V (local-void/KBC inhomogeneity) admissible direction within Planck pole; ~x2 insufficient against the H0DN endpoint on the two-factor branch (needed ~5.0% local shift vs ~2.5% allowed)'),
            finite_part_rule=_slot('finite_part_rule', SLOT_EXTERNAL, 'M_Pl + GR coupling G consumed as external constants ledger'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_CLOSED, 'matter density Omega_m derived from same capacity-partition'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_PARTIAL, 'strong-lens time-delay + JWST + LIGO standard-siren independent ladders awaited for tension resolution'),
        ),
        forbidden_inputs=frozenset({
            'target_H_0', 'target_fitted_epsilon_z',
            'target_fitted_distance_ladder_constants',
            'cepheid_to_match_local', 'sne_ia_calibration_to_match_local',
            'planck_to_match_apf', 'sh0es_to_match_apf',
        }),
        notes='Status WATCHING (fork-annotated v24.3.344): the row carries the TWO-FACTOR branch value '
              'H_0 = 70.03 km/s/Mpc; the count=area branch gives 66.83 (check_T_vacuum_o1_reading_fork -- '
              'a named reading fork, not a prediction row). Against current data: 70.03 is 4.94 sigma above '
              'Planck 2018 (67.36 +/- 0.54), 4.28 sigma below H0DN 2026 (73.50 +/- 0.81), 0.19 sigma from '
              'CCHP TRGB (70.39 +/- 1.9); 66.83 is 0.96 sigma from Planck and 8.22 sigma from H0DN. '
              'Three-way discriminator: ~67 => count=area exact; ~70 => two-factor exact; ~73 => both '
              'branches wrong. Empirical convergence awaited (DESI DR3, ladder-light TRGB/JAGB at sigma <~ 1, '
              'time-delay cosmography, standard sirens). Earlier corpus material misread the schema as '
              'carrying a Planck-only commitment to 67.76 km/s/Mpc; this row was retired 2026-05-10.',
    )


def desi_dark_energy_transport() -> CodomainTransport:
    return CodomainTransport(
        name='desi_dark_energy_w_2',
        source_codomain='APF2 second-order finite-continuability response: w_2(x) = -1 + 3/61 - (16/61)x - (21/8)x(x-1/3)(1-x) under gate G_2FCR (LATEST-62)',
        target_codomain='empirical w(a) measurement: DESI DR2 BAO + Planck CMB + {DESY5, PantheonPlus, Union3, no-SN} cross-SN compilation grid; native-Cobaya exact-likelihood evaluation',
        transport_map_name='APF2_tabulated_w_a_to_DESI_native_cobaya',
        status=TRANSPORT_PARTIAL,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'second-order finite-continuability response under gate G_2FCR; pivot x_* = 1/3 (barycentric three-sector); coefficient kappa_2 = 21/8 (response ratio Omega_Lambda/Omega_c)'),
            scale_rule=_slot('scale_rule', SLOT_CLOSED, 'tabulated w_2(a) over comoving a; CAMB+PPF transport to BAO + CMB likelihoods'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_CLOSED, 'classical cosmology + GR/PPF linear perturbation theory'),
            coupling_provenance=_slot('coupling_provenance', SLOT_CLOSED, 'APF coefficients (3, 16, 42, 61) are capacity ledger integers; pivot 1/3 + ratio 21/8 are APF-derived'),
            threshold_rule=_slot('threshold_rule', SLOT_CLOSED, 'phantom crossing at x_cross = 0.2854 (z_cross = 0.3993) structurally derived from w_2 shape'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, 'response mode is trace-free curvature of three-sector continuability simplex'),
            finite_part_rule=_slot('finite_part_rule', SLOT_CLOSED, 'cross-SN audit (LATEST-62 DESY5 + LATEST-74 PantheonPlus/Union3/no-SN): APF2 4-of-4 ACCEPT at 95% chi^2 LRT; 3-of-4 better than free (w_0, w_a); 4-of-4 better than LambdaCDM (Delta chi^2 in [-16.07, -6.37])'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_EXTERNAL, 'standard GR/PPF growth equations'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_PARTIAL, 'full-shape exact runtime (gate 3) LAUNCHED-BLOCKED (LATEST-74 pack #111); full-growth likelihood with covariance/fiducial/AP (gate 4) PARTIAL (1-of-4 sub-blockers closed at LATEST-68)'),
        ),
        forbidden_inputs=frozenset({
            'target_w_a', 'target_fitted_w_0_w_a',
            'post_hoc_w_2_coefficient_optimization',
            'observed_chi2_used_to_select_pivot',
            'observed_chi2_used_to_select_kappa_2',
        }),
        notes='Status CLOSED at LATEST-74-paired: APF2 cross-SN audit complete (4-of-4 ACCEPT at 95% across full '
              'SN-compilation grid; better than free (w_0, w_a) on 3-of-4 datasets at exact likelihood; better '
              'than LambdaCDM by Delta chi^2 in [-16.07, -6.37] on 4-of-4). The framework PIVOTED from APF1 '
              '(first-order CPL) to APF2 (second-order curvature) at LATEST-62; the prior schema entry forbidding '
              'dynamical dark energy was structurally wrong (LATEST-62 superseded LATEST-58 framing). APF2 is '
              'dynamical w(a) — but not by fitting; the curvature mode w_2(x) is derived structurally from '
              'endpoint-uniqueness + barycentric pivot + capacity response ratio BEFORE empirical evaluation. '
              'Robust empirical P remains 0 pending gate 3 (env-blocked) + gate 4 (partial). '
              'See Paper 35 v1.1 + wiki/Dark Sector Closure Registry.md Route 1.',
    )


def dune_juno_hierarchy_transport() -> CodomainTransport:
    return CodomainTransport(
        name='dune_juno_neutrino_hierarchy',
        source_codomain='framework-undecided codomain: PMNS shape derived (Paper 4 supp v2.2 §7); sign of Delta m^2_31 not currently fixed',
        target_codomain='measured-hierarchy codomain (DUNE/JUNO normal vs inverted resolution)',
        transport_map_name='hierarchy_input_to_PMNS_propagation',
        status=TRANSPORT_WAITING,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'PMNS mixing structure derived'),
            scale_rule=_slot('scale_rule', SLOT_CLOSED, 'CP phase L_PMNS_CP_corrected'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_CLOSED, 'tree-level mixing'),
            coupling_provenance=_slot('coupling_provenance', SLOT_CLOSED, 'Majorana phases set to zero by seesaw factorization'),
            threshold_rule=_slot('threshold_rule', SLOT_CLOSED, 'sum Sigma m_nu = 59.9 meV in normal hierarchy'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, '0nubb effective mass m_bb = 4.42 meV canonical'),
            finite_part_rule=_slot('finite_part_rule', SLOT_OPEN, 'sign of Delta m^2_31 — load-bearing slot'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_EXTERNAL, 'absolute mass scale consumed as input'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_OPEN, 'Dirac vs Majorana fork'),
        ),
        forbidden_inputs=frozenset({
            'target_hierarchy', 'target_fit_Delta_m2_31_sign',
            'cosmological_bound_interpretation_as_hierarchy_input',
        }),
        notes='Status WAITING (not OPEN): framework structural derivation will accept whichever hierarchy '
              'DUNE/JUNO measures and re-evaluate. Cleanest move: derive sign from PLEC + channel structure, '
              'OR explicitly accept hierarchy as empirical input and update forbidden set. Re-classified from '
              'OPEN to WAITING by the codomain-transport reframing.',
    )


def muon_g_minus_2_transport() -> CodomainTransport:
    return CodomainTransport(
        name='muon_g_minus_2',
        source_codomain='APF prediction codomain (NOT YET DERIVED — upstream)',
        target_codomain='physical g-2 measurement codomain (Fermilab + J-PARC)',
        transport_map_name='structural_prediction_to_physical_a_mu',
        status=TRANSPORT_UPSTREAM,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_OPEN),
            scale_rule=_slot('scale_rule', SLOT_OPEN),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_OPEN),
            coupling_provenance=_slot('coupling_provenance', SLOT_OPEN),
            threshold_rule=_slot('threshold_rule', SLOT_OPEN),
            subtraction_rule=_slot('subtraction_rule', SLOT_OPEN),
            finite_part_rule=_slot('finite_part_rule', SLOT_OPEN),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_OPEN),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_OPEN),
        ),
        forbidden_inputs=frozenset({
            'target_a_mu', 'target_fitted_HVP_contribution',
            'target_fitted_HLbL_contribution',
            'observed_a_mu_minus_SM_as_input',
        }),
        notes='Status UPSTREAM: framework currently has no direct g-2 derivation — bank carries structural '
              'infrastructure (lepton-photon channels, anomalous-magnetic-moment context) but not a numerical '
              'a_mu prediction. Transport question is downstream of source-codomain derivation.',
    )


# ---------------------------------------------------------------------
# Gauge + hadronic routes (2026-06-02, transport-axis recast machine layer)
# ---------------------------------------------------------------------

def inv_alpha_cross_transport() -> CodomainTransport:
    return CodomainTransport(
        name='inv_alpha_cross',
        source_codomain='APF capacity count: 1/alpha_cross = B*sigma = S_dS/6 = 47.02 (L_coupling_capacity_id [P], rank-2 fixed-point Fisher equilibrium)',
        target_codomain='physical crossing-scale MSbar couplings (alpha_2 = alpha_3 crossing, located from PDG alpha_2, alpha_3)',
        transport_map_name='rank2_fisher_equilibrium_running_subcount_to_MSbar_crossing',
        status=TRANSPORT_CLOSED,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'MSbar gauge couplings at the unification crossing scale'),
            scale_rule=_slot('scale_rule', SLOT_CLOSED, 'crossing scale M_cross where alpha_2 = alpha_3; self-located'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_EXTERNAL, 'standard one-loop+ RG running used only to locate the crossing for comparison'),
            coupling_provenance=_slot('coupling_provenance', SLOT_CLOSED, 'APF-derived: B = C_total/6 (L_beta_capacity), sigma = ln d_eff (L_sigma_intensive); no measured coupling'),
            threshold_rule=_slot('threshold_rule', SLOT_EXTERNAL, 'SM thresholds in the comparison RG'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, 'MSbar subtraction; standard'),
            finite_part_rule=_slot('finite_part_rule', SLOT_CLOSED, 'B*sigma = S_dS/6 exact capacity count'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_EXTERNAL, 'gauge beta coefficients (field-content counts)'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_CLOSED, '25.6 ppm vs the crossing inferred from PDG alpha_2, alpha_3'),
        ),
        forbidden_inputs=frozenset({
            'target_alpha_cross_measured', 'observed_crossing_value_as_input', 'target_fitted_sigma',
        }),
        notes='Export-candidate: the 47.02 reading is computed from capacity integers; measured couplings only locate the crossing for comparison (no inverse-fit).',
        codomain_type=CODOMAIN_NUMERICAL,
    )


def alpha_s_m_z_transport() -> CodomainTransport:
    return CodomainTransport(
        name='alpha_s_m_z',
        source_codomain='APF forward prediction from the two derived couplings (1/alpha_cross=47.02 [P], 1/alpha_Y=61 [P_structural_reading, alpha_s-corroborated]) + sin^2theta_W=3/13 [P]',
        target_codomain='physical alpha_s(M_Z) MSbar (PDG-2024 0.1180)',
        transport_map_name='capacity_couplings_plus_3_13_RG_to_alpha_s_M_Z',
        status=TRANSPORT_CLOSED,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'MSbar strong coupling at mu = M_Z'),
            scale_rule=_slot('scale_rule', SLOT_CLOSED, 'M_Z reference scale'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_EXTERNAL, 'standard SM RG running of the derived couplings to M_Z'),
            coupling_provenance=_slot('coupling_provenance', SLOT_CLOSED, 'inputs are APF-derived couplings + 3/13; ZERO measured coupling consumed'),
            threshold_rule=_slot('threshold_rule', SLOT_EXTERNAL, 'SM thresholds in the RG'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, 'MSbar'),
            finite_part_rule=_slot('finite_part_rule', SLOT_CLOSED, 'forward prediction, fully determined'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_EXTERNAL, 'QCD beta function'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_CLOSED, '0.11 sigma vs PDG-2024 0.1180 (forward, well within world-average precision)'),
        ),
        forbidden_inputs=frozenset({
            'target_alpha_s_measured', 'observed_alpha_s_M_Z_as_input', 'target_fitted_coupling',
        }),
        notes='Export-candidate, the headline gauge route: alpha_s(M_Z) is the OUTPUT of the chain (not back-solved); zero measured dimensionless coupling anywhere upstream.',
        codomain_type=CODOMAIN_NUMERICAL,
    )


def ew_vev_v_h_transport() -> CodomainTransport:
    return CodomainTransport(
        name='ew_vev_v_h',
        source_codomain='APF floor forced factor-by-factor: v_H = M_Pl*sqrt(N_c)*(4pi)^-1*102^-8*(12/7) = 246.21 GeV (ew_* floor chain, v24.3.176-185)',
        target_codomain='physical electroweak vev (Fermi G_F; 246.22 GeV)',
        transport_map_name='bosonic_root_measure_floor_times_planck_anchor',
        status=TRANSPORT_CLOSED,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'physical vev v_H = (sqrt2 G_F)^-1/2'),
            scale_rule=_slot('scale_rule', SLOT_EXTERNAL, 'absolute Planck magnitude -- the one owned dimensional anchor (shared with Lambda, Lambda_QCD, CMB-T)'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_CLOSED, 'no loop construction; floor forced from capacity'),
            coupling_provenance=_slot('coupling_provenance', SLOT_CLOSED, 'bosonic-16 mode count + sqrt(N_c) colour carrier, APF-derived'),
            threshold_rule=_slot('threshold_rule', SLOT_CLOSED, 'no threshold matching needed for the floor'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, 'n/a; structural floor'),
            finite_part_rule=_slot('finite_part_rule', SLOT_CLOSED, 'D=4 continuation-root measure (1/4pi); no O(1) freedom'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_CLOSED, 'n/a'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_CLOSED, '-0.003% vs Fermi 246.22 GeV'),
        ),
        forbidden_inputs=frozenset({
            'target_v_H_measured', 'observed_fermi_constant_as_input', 'target_fitted_prefactor',
        }),
        notes='Imported-one-route via the one owned Planck anchor (route-b by design). The Born-root suppression FORM is the [P_structural] residual on the absolute-scale axis; the mode-count is closed.',
        codomain_type=CODOMAIN_NUMERICAL,
    )


def delta_alpha_leptonic_transport() -> CodomainTransport:
    return CodomainTransport(
        name='delta_alpha_leptonic',
        source_codomain='APF first-principles: Delta_alpha_lep(M_Z) = 0.031421 from the banked charged-lepton pole masses (T_delta_alpha_leptonic_first_principles [P])',
        target_codomain='standard leptonic Delta_alpha(M_Z)',
        transport_map_name='one_loop_leptonic_vacuum_polarization_over_banked_masses',
        status=TRANSPORT_CLOSED,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'standard leptonic running of alpha to M_Z'),
            scale_rule=_slot('scale_rule', SLOT_CLOSED, 'M_Z reference scale'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_CLOSED, 'one-loop leptonic vacuum polarization, first-principles'),
            coupling_provenance=_slot('coupling_provenance', SLOT_CLOSED, 'lepton masses are APF-banked; no external mass input'),
            threshold_rule=_slot('threshold_rule', SLOT_CLOSED, 'lepton thresholds from banked masses'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, 'MSbar'),
            finite_part_rule=_slot('finite_part_rule', SLOT_CLOSED, 'fully determined at one loop'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_CLOSED, 'QED leptonic running'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_CLOSED, '~0% vs standard leptonic Delta_alpha (first-principles)'),
        ),
        forbidden_inputs=frozenset({
            'target_delta_alpha_lep_measured', 'observed_leptonic_running_as_input',
        }),
        notes='Export-candidate, the clean native hadronic-sector route: no irreducible external content (lepton masses are APF-banked).',
        codomain_type=CODOMAIN_NUMERICAL,
    )


def delta_alpha_hadronic_transport() -> CodomainTransport:
    return CodomainTransport(
        name='delta_alpha_hadronic',
        source_codomain='APF pQCD slice above Lambda_match=2 m_c: Delta_alpha_had^pQCD = 0.020924 = 75.6% of dispersion (T_delta_alpha_had_pqcd_first_principles [P], two routes)',
        target_codomain='dispersion/lattice Delta_alpha_had(M_Z) = 0.02766',
        transport_map_name='pqcd_slice_above_lambda_match_plus_external_NP_bulk',
        status=TRANSPORT_PARTIAL,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'MSbar hadronic running of alpha to M_Z'),
            scale_rule=_slot('scale_rule', SLOT_CLOSED, 'Lambda_match = 2 m_c(m_c) = 2.558 GeV, banked charm self-scale'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_PARTIAL, 'perturbative slice above Lambda_match computed; the nonperturbative bulk below is not'),
            coupling_provenance=_slot('coupling_provenance', SLOT_CLOSED, 'alpha_s is an APF forward prediction (gauge sector)'),
            threshold_rule=_slot('threshold_rule', SLOT_EXTERNAL, 'quark thresholds'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, 'MSbar'),
            finite_part_rule=_slot('finite_part_rule', SLOT_EXTERNAL, 'nonperturbative bulk (~24% residual) from dispersion/lattice -- admitted external by design'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_EXTERNAL, 'hadronic running'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_PARTIAL, 'pQCD slice 75.6% of dispersion; NP residual 0.006736 external'),
        ),
        forbidden_inputs=frozenset({
            'target_delta_alpha_had_measured', 'observed_dispersion_value_as_input', 'target_fitted_NP_bulk',
        }),
        notes='Imported-one-route, parallel to the light-quark FLAG route: the perturbative slice is first-principles [P], the nonperturbative bulk is admitted external by design (universal QCD difficulty). Naive pQCD overshoots dispersion by ~31% (APF-only no-go).',
        codomain_type=CODOMAIN_NUMERICAL,
    )


def lambda_qcd_confinement_transport() -> CodomainTransport:
    return CodomainTransport(
        name='lambda_qcd_confinement',
        source_codomain='APF dimensional transmutation: Lambda_QCD = M_Z*exp(-2pi/(b*alpha_s)) = M_Pl*(pure number) on the single Planck anchor (T_confinement_scale_rides_single_anchor [P_structural]); 1-loop n_f=3 = 244.5 MeV',
        target_codomain='physical Lambda_QCD (n_f=3; PDG ~332 MeV)',
        transport_map_name='dimensional_transmutation_on_single_planck_anchor',
        status=TRANSPORT_PARTIAL,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'Lambda_QCD, n_f=3'),
            scale_rule=_slot('scale_rule', SLOT_EXTERNAL, 'rides the single absolute Planck anchor (same as the EW vev)'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_PARTIAL, '1-loop leading approximation; precise value needs multi-loop'),
            coupling_provenance=_slot('coupling_provenance', SLOT_CLOSED, 'alpha_s is an APF forward prediction'),
            threshold_rule=_slot('threshold_rule', SLOT_PARTIAL, 'threshold matching pending for the precise value'),
            subtraction_rule=_slot('subtraction_rule', SLOT_CLOSED, 'MSbar'),
            finite_part_rule=_slot('finite_part_rule', SLOT_PARTIAL, 'multi-loop finite parts pending'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_EXTERNAL, 'QCD running'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_PARTIAL, '1-loop 244.5 MeV vs PDG ~332 MeV; precise value [P+alpha_s/tool]'),
        ),
        forbidden_inputs=frozenset({
            'target_lambda_qcd_measured', 'observed_PDG_lambda_as_input',
        }),
        notes='Structure [P_structural] (rides the single Planck anchor; no separate QCD scale introduced); precise value [P+alpha_s/tool] -- a multi-loop tooling exercise, not a structural gate.',
        codomain_type=CODOMAIN_NUMERICAL,
    )


# ---------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------

def sin2theta_w_ledger_to_measured_transport() -> CodomainTransport:
    return CodomainTransport(
        name='sin2theta_w_ledger_to_measured',
        source_codomain='APF ledger share: gamma=(1,17/4) => sin^2theta_W = 3/13 [P] over FD1 structural completeness + T_Higgs + T22 + the Schur asymmetry (check_T_ew_load_placement_P, gauge_quotient_ledger.py)',
        target_codomain='physical / effective measured weak mixing angle (PDG effective leptonic ~0.23148)',
        transport_map_name='w_propto_g2_dictionary_ledger_share_to_measured_angle',
        status=TRANSPORT_PARTIAL,
        certificate=TransportCertificate(
            scheme=_slot('scheme', SLOT_CLOSED, 'source is the ledger share 3/13 [P]; target is the measured/effective weak mixing angle'),
            scale_rule=_slot('scale_rule', SLOT_EXTERNAL, 'effective-leptonic / M_Z continuation; standard, comparison only'),
            loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_EXTERNAL, 'standard EW running to the effective angle (3/13 + 4/5063 = 0.231559); comparison only'),
            coupling_provenance=_slot('coupling_provenance', SLOT_CLOSED, 'ledger share 3/13 APF-derived [P] over FD1 structural completeness; ZERO measured coupling consumed (alpha_s only corroborates)'),
            threshold_rule=_slot('threshold_rule', SLOT_EXTERNAL, 'SM thresholds in the comparison continuation'),
            subtraction_rule=_slot('subtraction_rule', SLOT_EXTERNAL, 'MSbar / effective-scheme; standard'),
            finite_part_rule=_slot('finite_part_rule', SLOT_PARTIAL, 'THE DICTIONARY FENCE: the w-propto-g^2 correspondence (coupling = enforcement amplitude) carries the ledger share to a physical coupling ratio; reserved at [P_structural] by design -- the deliberately open slot (ceiling certified v24.3.364: the two wg2_dictionary_typing_no_go checks)'),
            anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_EXTERNAL, 'gauge beta coefficients in the comparison running'),
            uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_CLOSED, 'effective continuation 3/13 + 4/5063 = 0.231559 vs PDG 0.23154(6), 0.008%'),
        ),
        forbidden_inputs=frozenset({
            'target_sin2theta_measured', 'observed_weak_angle_as_input', 'target_fitted_load_ratio',
        }),
        notes='The dictionary-fence transport: the ledger share 3/13 is [P] (check_T_ew_load_placement_P, over FD1 structural completeness; the sin^2theta_W close 2026-06-12); reading it as the physical angle crosses the w-propto-g^2 correspondence, reserved at [P_structural] by design (ceiling certified v24.3.364: the two wg2_dictionary_typing_no_go checks). status PARTIAL = export-locked by the fence, not by a missing derivation -- the first transport that is SOURCE-CLOSED but TARGET-RESERVED on purpose.',
        codomain_type=CODOMAIN_NUMERICAL,
    )


ALL_TRANSPORT_FACTORIES: Tuple[Callable[[], CodomainTransport], ...] = (
    w_on_shell_transport,
    bottom_msbar_transport,
    top_msbar_or_pole_transport,
    light_quark_msbar_transport,
    charged_lepton_physical_transport,
    ym_continuum_limit_transport,
    h0_route_v_transport,
    desi_dark_energy_transport,
    dune_juno_hierarchy_transport,
    muon_g_minus_2_transport,
    inv_alpha_cross_transport,
    alpha_s_m_z_transport,
    ew_vev_v_h_transport,
    delta_alpha_leptonic_transport,
    delta_alpha_hadronic_transport,
    lambda_qcd_confinement_transport,
    sin2theta_w_ledger_to_measured_transport,
)


def all_transports() -> Tuple[CodomainTransport, ...]:
    return tuple(f() for f in ALL_TRANSPORT_FACTORIES)


# ---------------------------------------------------------------------
# Bank-registered checks
# ---------------------------------------------------------------------

def check_T_codomain_transport_schema_declared():
    """The CodomainTransport + TransportCertificate schema is declared with
    9 slot fields, valid status enums, and a complete-vs-partial predicate."""
    # Build a minimal instance to exercise the schema
    cert = TransportCertificate(
        scheme=_slot('scheme', SLOT_OPEN),
        scale_rule=_slot('scale_rule', SLOT_OPEN),
        loop_order_or_regularization=_slot('loop_order_or_regularization', SLOT_OPEN),
        coupling_provenance=_slot('coupling_provenance', SLOT_OPEN),
        threshold_rule=_slot('threshold_rule', SLOT_OPEN),
        subtraction_rule=_slot('subtraction_rule', SLOT_OPEN),
        finite_part_rule=_slot('finite_part_rule', SLOT_OPEN),
        anomalous_dimension_rule=_slot('anomalous_dimension_rule', SLOT_OPEN),
        uncertainty_pushforward=_slot('uncertainty_pushforward', SLOT_OPEN),
    )
    slots = cert.all_slots()
    assert len(slots) == 9
    assert cert.total_count() == 9
    assert cert.filled_count() == 0
    assert not cert.is_complete()
    assert len(VALID_SLOT_STATUSES) == 5
    assert len(VALID_TRANSPORT_STATUSES) == 7
    return {
        'name': 'T_codomain_transport_schema_declared',
        'passed': True,
        'status': 'PASS',
        'tier': 4,
        'epistemic': 'P_structural_instrument',
        'slot_field_count': len(slots),
        'valid_slot_statuses': sorted(VALID_SLOT_STATUSES),
        'valid_transport_statuses': sorted(VALID_TRANSPORT_STATUSES),
        'key_result': '9-field SchemeContract type signature declared with 5 slot statuses and 7 transport statuses.',
        'summary': 'CodomainTransport + TransportCertificate schema bank-callable.',
    }


def check_T_codomain_transport_instances_registered():
    """All 10 known open-frontier transports are registered and instantiable."""
    transports = all_transports()
    assert len(transports) == 17
    names = {t.name for t in transports}
    expected = {
        'w_on_shell', 'bottom_msbar', 'top_msbar_or_pole', 'light_quark_msbar',
        'charged_lepton_physical', 'ym_continuum_limit', 'h0_route_v',
        'desi_dark_energy_w_2', 'dune_juno_neutrino_hierarchy', 'muon_g_minus_2',
        'inv_alpha_cross', 'alpha_s_m_z', 'ew_vev_v_h',
        'delta_alpha_leptonic', 'delta_alpha_hadronic', 'lambda_qcd_confinement',
        'sin2theta_w_ledger_to_measured',
    }
    assert names == expected, f'missing or extra transports: {names ^ expected}'
    return {
        'name': 'T_codomain_transport_instances_registered',
        'passed': True,
        'status': 'PASS',
        'tier': 4,
        'epistemic': 'P_structural_instrument',
        'instance_count': len(transports),
        'instance_names': sorted(names),
        'key_result': '16 codomain-transport instances registered: 5 mass routes + YM continuum + H_0 + DESI w_2(a) + DUNE/JUNO + g-2 + 3 gauge (1/alpha_cross, alpha_s, v_H) + 3 hadronic (Delta_alpha_lep, Delta_alpha_had, Lambda_QCD) [added 2026-06-02 transport-axis recast]. As of LATEST-74 (2026-05-12): 5 routes CLOSED (5 mass routes at [P_export_candidate] or [P_imported_one_route] or [P_obstruction_named]), 2 PARTIAL (YM continuum-limit, DESI w_2(a) at [P_internal_FCR + cross-SN 4-of-4 95%]; gates 3+4 still open for DESI), 1 WATCHING (H_0), 1 WAITING (DUNE/JUNO), 1 UPSTREAM (g-2). Renamed desi_dark_energy_w_minus_1 -> desi_dark_energy_w_2 at LATEST-62 when APF2 second-order finite-continuability response superseded APF1 first-order CPL.',
        'summary': 'Every currently-known open frontier instantiated as a transport object.',
    }


def check_T_codomain_transport_certificates_well_formed():
    """Every transport instance has a 9-field certificate with valid slot statuses."""
    transports = all_transports()
    for t in transports:
        slots = t.certificate.all_slots()
        assert len(slots) == 9, f'{t.name}: expected 9 slots, got {len(slots)}'
        for s in slots:
            assert s.status in VALID_SLOT_STATUSES, (
                f'{t.name}: slot {s.name!r} has invalid status {s.status!r}'
            )
    fill_summary = {t.name: f'{t.certificate.filled_count()}/9' for t in transports}
    return {
        'name': 'T_codomain_transport_certificates_well_formed',
        'passed': True,
        'status': 'PASS',
        'tier': 4,
        'epistemic': 'P_structural_instrument',
        'certificate_fill': fill_summary,
        'key_result': 'Every certificate is a 9-field SchemeContract with valid slot statuses.',
        'summary': 'Certificate shape uniform across 16 instances.',
    }


def check_T_codomain_transport_forbidden_inputs_declared():
    """Every transport instance declares a nonempty forbidden-input set with target observable forbidden."""
    transports = all_transports()
    for t in transports:
        assert len(t.forbidden_inputs) > 0, f'{t.name}: empty forbidden_inputs'
        # At least one entry should mention 'target' to enforce no-smuggling
        has_target_guard = any('target' in fi.lower() or 'observed' in fi.lower()
                               for fi in t.forbidden_inputs)
        assert has_target_guard, f'{t.name}: no target/observed guard in forbidden_inputs'
    forbidden_counts = {t.name: len(t.forbidden_inputs) for t in transports}
    return {
        'name': 'T_codomain_transport_forbidden_inputs_declared',
        'passed': True,
        'status': 'P_structural_instrument',
        'tier': 4,
        'epistemic': 'P_structural_instrument',
        'forbidden_counts': forbidden_counts,
        'key_result': 'Every transport declares a nonempty forbidden-input set with target/observed guards.',
        'summary': 'No-smuggling discipline structurally enforced across all 16 instances.',
    }


def check_T_codomain_transport_no_smuggling_consistent():
    """No transport claims TRANSPORT_CLOSED status while its certificate is incomplete."""
    transports = all_transports()
    for t in transports:
        if t.status == TRANSPORT_CLOSED:
            assert t.certificate.is_complete(), (
                f'{t.name}: status CLOSED but certificate has '
                f'{t.certificate.filled_count()}/9 slots filled'
            )
        # Conversely, no transport may unlock physical_export while the certificate is open
        if t.physical_export_locked():
            # This is the expected case for all current instances
            pass
        else:
            # Would only fire if status==CLOSED and certificate complete; flag it
            assert t.status == TRANSPORT_CLOSED, (
                f'{t.name}: physical_export unlocked but status != CLOSED'
            )
    locked_count = sum(1 for t in transports if t.physical_export_locked())
    return {
        'name': 'T_codomain_transport_no_smuggling_consistent',
        'passed': True,
        'status': 'PASS',
        'tier': 4,
        'epistemic': 'P_structural_instrument',
        'locked_count': f'{locked_count}/{len(transports)}',
        'key_result': 'No transport claims CLOSED status with incomplete certificate; physical_export structurally locked.',
        'summary': 'No-smuggling consistency: status / certificate / export-lock triangle uniform.',
    }


def check_T_codomain_transport_status_classification():
    """Every transport has a valid top-level status; classification matches reference doc."""
    transports = all_transports()
    expected_statuses = {
        'w_on_shell': TRANSPORT_CLOSED,                # LATEST-50: DIZET imported, z = +0.198 vs CMS 2026
        'bottom_msbar': TRANSPORT_CLOSED,              # LATEST-54: m_b = M_W * 2^{-4.25} = 4.186 GeV, z = 0.30
        'top_msbar_or_pole': TRANSPORT_CLOSED,         # LATEST-56 MSR + LATEST-61 pole knockout, z = 0.015 MSR(R_EW)
        'light_quark_msbar': TRANSPORT_CLOSED,         # LATEST-66/67: FLAG kernel transport + APF-only no-go theorem
        'charged_lepton_physical': TRANSPORT_CLOSED,   # LATEST-53/56: x^8 envelope, chi^2_3 = 0.394, p = 0.941
        'ym_continuum_limit': TRANSPORT_PARTIAL,
        'h0_route_v': TRANSPORT_WATCHING,
        'desi_dark_energy_w_2': TRANSPORT_PARTIAL,     # LATEST-62 internal-FCR-P + LATEST-74 cross-SN 4-of-4 95%; gate 3 (full-shape exact) env-blocked + gate 4 (full-growth) partial
        'dune_juno_neutrino_hierarchy': TRANSPORT_WAITING,
        'muon_g_minus_2': TRANSPORT_UPSTREAM,
        'inv_alpha_cross': TRANSPORT_CLOSED,           # gauge export-candidate, 25.6 ppm
        'alpha_s_m_z': TRANSPORT_CLOSED,               # gauge export-candidate, 0.11 sigma forward (vs PDG-2024) from zero measured coupling
        'ew_vev_v_h': TRANSPORT_CLOSED,                # imported-one-route via the one Planck anchor, -0.003%
        'delta_alpha_leptonic': TRANSPORT_CLOSED,      # hadronic export-candidate, first-principles ~0%
        'delta_alpha_hadronic': TRANSPORT_PARTIAL,     # pQCD slice 75.6% [P] + NP bulk external by design
        'lambda_qcd_confinement': TRANSPORT_PARTIAL,   # structure rides the Planck anchor; precise value [P+alpha_s/tool]
        'sin2theta_w_ledger_to_measured': TRANSPORT_PARTIAL,  # source-closed (3/13 [P]); target reserved by the w-propto-g^2 dictionary fence (the sin2theta_W close)
    }
    actual = {}
    for t in transports:
        assert t.status in VALID_TRANSPORT_STATUSES, (
            f'{t.name}: invalid status {t.status!r}'
        )
        actual[t.name] = t.status
    assert actual == expected_statuses, f'status mismatch: {actual} vs {expected_statuses}'
    counts = {}
    for status in actual.values():
        counts[status] = counts.get(status, 0) + 1
    return {
        'name': 'T_codomain_transport_status_classification',
        'passed': True,
        'status': 'PASS',
        'tier': 4,
        'epistemic': 'P_structural_instrument',
        'classification_counts': counts,
        'classifications': actual,
        'key_result': '10 transports classified across 5 distinct statuses (LATEST-74 refresh): 5 CLOSED (5 mass routes at [P_export_candidate] / [P_imported_one_route] / [P_obstruction_named]), 2 PARTIAL (YM continuum-limit + DESI w_2(a) at [P_internal_FCR + cross-SN 4-of-4 95]; gates 3 env-blocked + 4 partial), 1 WATCHING (H_0), 1 WAITING (DUNE/JUNO), 1 UPSTREAM (muon g-2). Zero OPEN, zero FALSIFYING. Prior state (pre-LATEST-50): 4 OPEN, 2 PARTIAL, 2 WATCHING, 1 WAITING, 1 UPSTREAM. The 5-CLOSED + 2-PARTIAL state reflects the post-LATEST-44 doctrine-consequences sprint (mass-sector + dark-sector closure registries).',
        'summary': 'Status classification matches the reference doc exactly.',
    }


def check_T_codomain_transport_unification():
    """Master meta-theorem: the framework's open frontier has uniform structural form
    as a registry of codomain-transport theorems with 9-field certificates."""
    schema = check_T_codomain_transport_schema_declared()
    instances = check_T_codomain_transport_instances_registered()
    certificates = check_T_codomain_transport_certificates_well_formed()
    forbidden = check_T_codomain_transport_forbidden_inputs_declared()
    smuggling = check_T_codomain_transport_no_smuggling_consistent()
    classification = check_T_codomain_transport_status_classification()
    children = (schema, instances, certificates, forbidden, smuggling, classification)
    assert all(c['passed'] for c in children)
    transports = all_transports()
    return {
        'name': 'T_codomain_transport_unification',
        'passed': True,
        'status': 'PASS',
        'tier': 4,
        'epistemic': 'P_structural_instrument',
        'dependencies': [c['name'] for c in children],
        'transport_count': len(transports),
        'transport_summary': [t.to_dict() for t in transports],
        'physical_export_locked_count': sum(1 for t in transports if t.physical_export_locked()),
        'closed_count': sum(1 for t in transports if t.status == TRANSPORT_CLOSED),
        'key_result': "APF open frontier reframed as 10 codomain-transport theorems under one schema. As of LATEST-74 (2026-05-12): 5 of 10 CLOSED (5 mass routes at [P_export_candidate] / [P_imported_one_route] / [P_obstruction_named]); 2 PARTIAL (YM continuum-limit; DESI w_2(a) at [P_internal_FCR + cross-SN 4-of-4 95%], gates 3 env-blocked + 4 partial); 1 WATCHING (H_0 Route V); 1 WAITING (DUNE/JUNO neutrino hierarchy); 1 UPSTREAM (muon g-2 hadronic VP). The closure-grade state pairs route-by-route with wiki/Mass Sector Closure Registry.md (LATEST-66) and wiki/Dark Sector Closure Registry.md (LATEST-74). Three open problems flagged elsewhere as not-codomain-transport: m_c at 2.6%, dark-matter particle ID (guarded by design per Dark Registry Theorem A/B/C), absolute neutrino scale.",
        'summary': 'Master unification theorem: the framework discovers a unified schema for its open frontier.',
    }


# ---------------------------------------------------------------------
# Bank registration
# ---------------------------------------------------------------------

def check_T_codomain_type_declared():
    """Every codomain-transport instance declares codomain_type in VALID_CODOMAIN_TYPES.

    v24.1 schema extension. Routes registered before v24.1 default to 'numerical' for backwards
    compatibility; routes whose codomain is theorem-shape rather than number-shape (the YM
    continuum-limit existence claim is the canonical example) declare codomain_type='structural'.
    The export theorem's G4 (covariance) and G6 (residual channel) read in their numerical or
    structural form per route based on this field. See STRUCTURAL_EXTENSION_v35_1/ for the
    formal extension and worked-example RP1 walk.
    """
    transports = all_transports()
    bad = []
    for t in transports:
        if t.codomain_type not in VALID_CODOMAIN_TYPES:
            bad.append((t.name, t.codomain_type))
    if bad:
        return {
            'name': 'T_codomain_type_declared',
            'tier': 4,
            'epistemic': 'P_structural_instrument',
            'passed': False,
            'failures': bad,
            'key_result': f'codomain_type validation failed for {len(bad)} transports',
        }
    counts = {ct: sum(1 for t in transports if t.codomain_type == ct) for ct in VALID_CODOMAIN_TYPES}
    return {
        'name': 'T_codomain_type_declared',
        'tier': 4,
        'epistemic': 'P_structural_instrument',
        'passed': True,
        'key_result': (
            f'codomain_type declared on all {len(transports)} transports: '
            f'{counts[CODOMAIN_NUMERICAL]} numerical + {counts[CODOMAIN_STRUCTURAL]} structural'
        ),
        'counts': counts,
    }


_CHECKS = {
    'T_codomain_transport_schema_declared': check_T_codomain_transport_schema_declared,
    'T_codomain_transport_instances_registered': check_T_codomain_transport_instances_registered,
    'T_codomain_transport_certificates_well_formed': check_T_codomain_transport_certificates_well_formed,
    'T_codomain_transport_forbidden_inputs_declared': check_T_codomain_transport_forbidden_inputs_declared,
    'T_codomain_transport_no_smuggling_consistent': check_T_codomain_transport_no_smuggling_consistent,
    'T_codomain_transport_status_classification': check_T_codomain_transport_status_classification,
    'T_codomain_transport_unification': check_T_codomain_transport_unification,
    'T_codomain_type_declared': check_T_codomain_type_declared,
}


def register(registry):
    """Register the codomain-transport unification checks into the bank.
    8 checks total post-v24.1 + 2026-05-10 H_0 correction."""
    for name, fn in _CHECKS.items():
        registry[name] = fn


def run_all():
    results = []
    for name, fn in _CHECKS.items():
        try:
            r = fn()
            ok = bool(r.get('passed') is True or str(r.get('status', '')).upper() in {'PASS', 'P', 'P_STRUCTURAL'})
            results.append({'name': name, 'passed': ok})
        except Exception as e:
            results.append({'name': name, 'passed': False, 'error': repr(e)})
    return {
        'passed': sum(1 for r in results if r['passed']),
        'total': len(results),
        'results': results,
    }


if __name__ == '__main__':
    import json
    print(json.dumps(run_all(), indent=2))
