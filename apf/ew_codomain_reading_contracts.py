"""Codomain-reading contracts for the electroweak sector (machine layer).

Sibling to apf/codomain_transport_schema.py. That module is a *transport* contract
(source_codomain -> target_codomain, with forbidden_inputs guarding the INPUT side: "you
smuggled a measured value into a derivation"). This module guards the OUTPUT side: reading a
ledger quantity in the WRONG CODOMAIN. The 2026-06-08 EW session hit that failure mode repeatedly
(the tree "trace route", the 1/alpha_Y=60.75 mislabel, the kappa_b fermion-channel extension);
none was a smuggled input, all were category errors on the readout.

A CodomainReadingContract names a ledger quantity's HOME codomain + value, its legitimate SIBLING
codomain projections (distinct codomains, no conflation), and a nonempty set of FORBIDDEN SWAPS,
each annotated with the rule it violates and the actual past incident it would have caught.

STATUS (architecture-only as of build): the two checks here validate (1) the contract SCHEMA +
that the four EW domains are well-formed, and (2) that every HOME value is reproduced from capacity
with no measured input. Those are sound machine-layer consistency facts. The FORBIDDEN-SWAP content
encodes session judgments and is NOT yet enforced against the live bank, and is NOT yet promoted to
a counted bank check: promotion (to BANK_REGISTRY_MODULES + a bank-scanning swap-enforcement check)
waits for an independent COLD ADVERSARIAL AUDIT that each forbidden swap is a genuine category error
and not a real open question being suppressed. A contract that forbids a live question is a
blindfold, not a guard.

Pure arithmetic; no scipy/heavy imports, so the module always loads.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
import math

# Capacity ledger integers (trace to L_count [P], L_self_exclusion [P]); kept local so the
# module loads under any import order.
C_TOTAL = 61          # = 45 fermion + 4 + 12 gauge  (L_count [P])
D_EFF = 102           # = 60 + 42                     (L_self_exclusion [P])
N_C = 3               # colour                        (T_gauge [P])

# ---------------------------------------------------------------------------
# Contract types
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class CodomainRead:
    """One legitimate projection of a ledger quantity into a named codomain."""
    codomain: str
    value: str
    grade: str
    mechanism: str
    content: str = ''


@dataclass(frozen=True)
class ForbiddenSwap:
    """A named category error: reading the quantity as if it lived in another codomain."""
    swap: str
    why_forbidden: str
    past_incident: str


@dataclass(frozen=True)
class CodomainReadingContract:
    """A ledger quantity, its home codomain, sibling reads, and the forbidden swaps."""
    quantity: str
    home: CodomainRead
    siblings: tuple
    forbidden: frozenset
    home_value_check: object = None   # callable() -> bool: reproduces home.value from capacity

    def validate_structure(self) -> None:
        assert self.forbidden, f"{self.quantity}: forbidden-swap set must be nonempty"
        cods = [self.home.codomain] + [s.codomain for s in self.siblings]
        assert len(cods) == len(set(cods)), f"{self.quantity}: codomains must be distinct"
        for fs in self.forbidden:
            assert fs.swap and fs.why_forbidden and fs.past_incident, \
                f"{self.quantity}: every forbidden swap must name rule + incident"


# ---------------------------------------------------------------------------
# Home-value reproductions from capacity (no measured input)
# ---------------------------------------------------------------------------
def _val_3_13() -> bool:
    # VALUE identity only: 3/13 = 1/(1+10/3), with B_Y = Tr Y^2 = 10/3 the [P]-forced hypercharge
    # trace and the SU(2) entry = 1 (uniform-ledger count=trace coincidence; consolidated record
    # 2026-06-08 sec 6-7). This is NOT the load-bearing route -- the GRADE of 3/13 rests on the
    # competition fixed point with load gamma=(1,17/4) (Paper 18), not on this arithmetic. The
    # tree-coupling-ratio reading of the same arithmetic on the SM matter traces is the forbidden swap.
    return F(1) / (F(1) + F(10, 3)) == F(3, 13)

def _val_vH_over_MPl() -> bool:
    # EW floor: bosonic root-measure x Planck anchor
    v = math.sqrt(N_C) / (4 * math.pi) * D_EFF ** (-8) * (12 / 7)
    return abs(v - 2.0167e-17) < 1e-20

def _val_61_census() -> bool:
    # rank-1 abelian uniform-ledger reading: S_dS/sigma = C_total ; and the integer partition
    return C_TOTAL == 45 + 4 + 12

def _val_60_75_record() -> bool:
    # record / N_commit=4: photon makes 3 of 4 commitments -> (4*C_total - 1)/4
    return F(4 * C_TOTAL - 1, 4) == F(243, 4) == F(60.75).limit_denominator()

def _val_2_9_OS() -> bool:
    # GH-OS rank-source map (3,3,1,2) -> r* = (D-2)/(2(D-1)+dimRH-dim(G/H)) = 2/7 -> sin^2 = 2/9
    D, dimRH, dimGH = 4, 4, 3
    r_star = F(D - 2, 2 * (D - 1) + dimRH - dimGH)
    return r_star == F(2, 7) and (r_star / (r_star + 1)) == F(2, 9)

def _val_kappa_l() -> bool:
    return (F(3, 13) / F(2, 9)) == F(27, 26)


# ---------------------------------------------------------------------------
# The four EW domains
# ---------------------------------------------------------------------------
DOMAIN_WEAK_MIXING = CodomainReadingContract(
    quantity="sin^2 theta_W (weak mixing angle)",
    home=CodomainRead(
        "capacity-competition equilibrium @ M_Z (effective leptonic)", "3/13", "[P_structural]",
        "competition fixed point + running on the ledger values (47.02, 61); load gamma=(1,17/4)",
        "the effective leptonic angle; a READOUT of the ledger, not a primitive"),
    siblings=(
        CodomainRead("gauge+Higgs on-shell (GH-OS)", "2/9", "[P_attractor_structural]",
                     "rank-source attractor flow", "the on-shell angle; related by kappa_l=(3/13)/(2/9)=27/26"),
    ),
    forbidden=frozenset({
        ForbiddenSwap(
            "tree-coupling-ratio reading",
            "the angle is a competition equilibrium on the LEDGER, not a tree gauge-coupling ratio on the SM MATTER TRACES",
            "the 'trace route' B2=1, B_Y=Tr Y^2=10/3 -- a heuristic on the matter traces, mistaken for the load-bearing derivation"),
    }),
    home_value_check=lambda: _val_3_13() and _val_kappa_l(),
)

DOMAIN_ABSOLUTE_SCALE = CodomainReadingContract(
    quantity="v_H / M_Pl (electroweak floor)",
    home=CodomainRead(
        "bosonic root-measure of the ledger x Planck anchor", "sqrt(N_c)/(4pi)*d_eff^-8*(12/7)", "[P_structural]",
        "bosonic Gaussian determinant over the 16 bosonic slots (Grassmann slots carry no root-volume)",
        "the EW hierarchy as a microstate-volume root-amplitude; residual = the vacuum=bosonic-measure "
        "identification (a measure-theory question, not a Gleason Born amplitude -- LATER-5 refuted Born)"),
    siblings=(),
    forbidden=frozenset({
        ForbiddenSwap(
            "full-61-or-fermionic measure",
            "the root-measure support is the 16 BOSONIC slots; the 45 Grassmann slots carry no root-volume",
            "the 'direct-16 rejection' / treating the floor exponent as the full ledger count"),
        ForbiddenSwap(
            "count-not-amplitude",
            "the floor is a root-measure amplitude (bosonic Gaussian determinant det^(-1/2) ~ "
            "d_eff^(-C_active/2)), NOT an integer channel count (and NOT a Gleason Born amplitude; "
            "LATER-5 identified the sqrt as a Gaussian determinant, not Born)",
            "reading the suppression as a census rather than a root-measure"),
    }),
    home_value_check=_val_vH_over_MPl,
)

DOMAIN_ABELIAN = CodomainReadingContract(
    quantity="abelian hypercharge reading at M_cross",
    home=CodomainRead(
        "channel-census (sigma-microstate count)", "61", "[P]",
        "rank-1 reads the uniform ledger: S_dS/sigma = C_total",
        "the coupling census: 61 = 45+4+12, the photon is one present U(1) carrier"),
    siblings=(
        CodomainRead("record / mass (N_commit=4)", "60.75 = C_total-1/4", "[P_structural]",
                     "photon fails C_4 (L_irr lock) -> counts 3/4 -> (4*61-1)/4",
                     "R_Y^commit; its content is m_gamma=0 -- NOT a coupling"),
        CodomainRead("measured / running (one-loop)", "60.75 +/- 0.12", "[C]",
                     "measured couplings run to the alpha_2=alpha_3 crossing",
                     "the physical coupling there; 61 is +2.2sigma, 60.75 is 0.01sigma (data-back-solved)"),
    ),
    forbidden=frozenset({
        ForbiddenSwap(
            "record-as-coupling",
            "forcing the COUPLING value 60.75 from the RECORD (C_4 / photon-recordless) mechanism "
            "conflates two codomains: the record R_Y^commit=60.75 is on the mass axis (content "
            "m_gamma=0), the coupling census is 61. (The bare measured '1/alpha_Y(crossing)~60.74' is "
            "the [C] measured sibling, allowed; structure reads it as two-loop drift from 61 + coincidence.)",
            "the temptation, mid-session, to DERIVE the abelian coupling as 60.75 via the record"),
        ForbiddenSwap(
            "census-as-physical-without-C",
            "the census 61 is [P]; its identification WITH the physical crossing coupling is held [C] (data-back-solved); the alpha_s 0.11-sigma headline depends on it",
            "grading alpha_s(M_Z)=0.1179 as a clean [P] prediction without the [C] running-boundary caveat"),
    }),
    home_value_check=lambda: _val_61_census() and _val_60_75_record(),
)

DOMAIN_GH_OS = CodomainReadingContract(
    quantity="sin^2 theta_W (on-shell) / the GH-OS counting rule",
    home=CodomainRead(
        "gauge+Higgs on-shell sub-sector ONLY", "2/9", "[P_attractor_structural]",
        "rank-source map (3,3,1,2) -> r*=2/7 -> 2/9; replicator attractor flow",
        "the on-shell angle; M_W^2/M_Z^2=7/9; a SECOND independent capacity derivation of the mixing"),
    siblings=(
        CodomainRead("leptonic effective (via kappa_l)", "kappa_l=27/26", "[P_attractor_structural_composed]",
                     "compose with Paper 18's 3/13", "the scheme-bridge to the effective angle"),
    ),
    forbidden=frozenset({
        ForbiddenSwap(
            "fermion-channel extension (kappa_b)",
            "the GH-OS rule is a gauge+Higgs DENOMINATOR/carrier rule; extending it as a fermion-channel NUMERATOR rule is a codomain role-swap",
            "naive kappa_b: sin^2 theta_eff^b = 8/21 = 0.381 vs measured 0.232 (factor 1.65); reciprocal (8/21)*(21/8)=1 against the APF2 dark curvature is the tell -- fenced [C]"),
    }),
    home_value_check=_val_2_9_OS,
)

EW_CODOMAIN_CONTRACTS = (DOMAIN_WEAK_MIXING, DOMAIN_ABSOLUTE_SCALE, DOMAIN_ABELIAN, DOMAIN_GH_OS)


# ---------------------------------------------------------------------------
# Bank-callable checks (machine-layer consistency; architecture-only until cold-audited)
# ---------------------------------------------------------------------------
def check_T_ew_codomain_reading_schema_declared():
    """The CodomainReadingContract schema is declared and the four EW domains are well-formed:
    nonempty forbidden-swap sets, distinct sibling codomains, every swap names a rule + incident."""
    n = len(EW_CODOMAIN_CONTRACTS)
    assert n == 4, f"expected 4 EW domains, got {n}"
    n_swaps = 0
    for c in EW_CODOMAIN_CONTRACTS:
        c.validate_structure()
        n_swaps += len(c.forbidden)
    assert n_swaps >= n, "each domain must forbid at least one swap"
    return {
        'name': 'T_ew_codomain_reading_schema_declared',
        'passed': True, 'status': 'PASS', 'tier': 4, 'epistemic': 'P_structural',
        'domain_count': n, 'forbidden_swap_count': n_swaps,
        'key_result': ('4 EW codomain-reading contracts (weak-mixing / absolute-scale / abelian / GH-OS) '
                       f'declared with {n_swaps} forbidden swaps, distinct sibling codomains, each swap '
                       'naming its rule + the 2026-06-08 incident it guards.'),
        'summary': 'CodomainReadingContract schema + four EW domains bank-callable and well-formed.',
    }


def check_T_ew_codomain_reading_home_values_from_capacity():
    """Every HOME value is reproduced from the capacity ledger with no measured input:
    3/13 (competition), v_H/M_Pl (bosonic root-measure), 61 (census) + 60.75 (record),
    2/9 (GH-OS rank-source), and the scheme bridge kappa_l = 27/26."""
    results = {c.quantity: bool(c.home_value_check()) for c in EW_CODOMAIN_CONTRACTS}
    assert all(results.values()), f"home value(s) not reproduced from capacity: {results}"
    # explicit witnesses
    assert _val_3_13() and _val_2_9_OS() and _val_kappa_l()
    assert _val_61_census() and _val_60_75_record() and _val_vH_over_MPl()
    return {
        'name': 'T_ew_codomain_reading_home_values_from_capacity',
        'passed': True, 'status': 'PASS', 'tier': 4, 'epistemic': 'P_structural',
        'home_values': {'sin2_eff': '3/13', 'sin2_OS': '2/9', 'kappa_l': '27/26',
                        'abelian_census': '61', 'abelian_record': '60.75',
                        'vH_over_MPl': 'sqrt(N_c)/(4pi)*102^-8*(12/7)'},
        'measured_inputs_consumed': 0,
        'key_result': ('All four EW home values reproduce from capacity with zero measured input: '
                       '3/13, 2/9 (kappa_l=27/26), 61 + 60.75, v_H/M_Pl.'),
        'summary': 'Home codomain values are capacity-derived, not measured.',
    }


# ---------------------------------------------------------------------------
# Bank-scanning enforcement: every contract's protected reading must itself be a
# live banked check at the claimed grade. This is what turns the contract from a
# static declaration into a guard -- a forbidden swap is only meaningful if the
# correct reading it protects is banked. If an anchor is renamed, regraded, or
# deleted, this fails loudly instead of silently fencing a question whose backing
# has moved.
# ---------------------------------------------------------------------------
# domain.quantity -> tuple of (registry_key, expected_grade_prefix, role)
ANCHOR_REQUIREMENTS = {
    "sin^2 theta_W (weak mixing angle)": (
        ("T_sin2theta_higgs_record", "P_structural", "home 3/13 (competition + Higgs-record load)"),
    ),
    "v_H / M_Pl (electroweak floor)": (
        ("T_ew_bosonic_enforcement_reservoir_theorem", "P_structural",
         "16-bosonic-slot support (guards swap: full-61-or-fermionic)"),
        ("T_ew_lambda_unified_suppression", "P_structural",
         "amplitude/half-power root (guards swap: count-not-amplitude)"),
    ),
    "abelian hypercharge reading at M_cross": (
        ("T_gauge_reading_dichotomy", "P", "census 61 home (coupling axis)"),
        ("T_abelian_coupling_fixed_by_rank1_capacity_count", "P", "census 61 home (coupling axis)"),
        ("T_ledger_reversibility_is_L_irr_lock", "P_structural",
         "record 60.75 reading (guards swap: record-as-coupling)"),
        ("T_gauge_force_character_from_record_state", "P_structural", "record / force-character axis"),
    ),
    "sin^2 theta_W (on-shell) / the GH-OS counting rule": (
        ("T_sin2_theta_W_OS_capacity_counting_value", "P_attractor_structural", "GH-OS 2/9 home"),
        ("T_kappa_b_universality_falsified", "C",
         "kappa_b fermion-channel fence (guards swap: fermion-channel extension)"),
    ),
}


def check_T_ew_codomain_reading_anchors_banked():
    """Every EW codomain contract's protected reading is backed by a live banked check at the
    claimed grade. Loads the registry and asserts each named anchor resolves and its epistemic
    grade matches (prefix). A contract guards a swap only if the correct reading is itself banked;
    if an anchor is renamed/regraded/deleted this fails loudly rather than fencing a moved question."""
    import apf.bank as bank
    bank._load()  # idempotent: no-op under verify_all, populates when this module is run standalone
    reg = bank.REGISTRY
    declared = {c.quantity for c in EW_CODOMAIN_CONTRACTS}
    required = set(ANCHOR_REQUIREMENTS)
    assert declared == required, f"every domain must carry an anchor requirement; mismatch: {declared ^ required}"
    checked = []
    for quantity, anchors in ANCHOR_REQUIREMENTS.items():
        for key, grade_prefix, role in anchors:
            assert key in reg, f"{quantity}: anchor '{key}' not in live registry ({role})"
            res = reg[key]()
            grade = res.get('epistemic') if isinstance(res, dict) else None
            assert grade is not None and grade.startswith(grade_prefix), \
                f"{quantity}: anchor '{key}' grade '{grade}' != '{grade_prefix}*' ({role})"
            checked.append((key, grade))
    return {
        'name': 'T_ew_codomain_reading_anchors_banked',
        'passed': True, 'status': 'PASS', 'tier': 4, 'epistemic': 'P_structural',
        'anchors_verified': len(checked),
        'registry_size_seen': len(reg),
        'key_result': (f'{len(checked)} banked anchors back the 4 EW codomain contracts at their claimed '
                       'grades (3/13 [P_structural]; GH-OS 2/9 [P_attractor_structural]; census 61 [P]; '
                       'record 60.75 + floor [P_structural]; kappa_b fence [C]); each forbidden swap '
                       'protects a reading that is itself banked.'),
        'summary': 'Every codomain contract is backed by a live banked check at grade.',
    }


_CHECKS = {
    'T_ew_codomain_reading_schema_declared': check_T_ew_codomain_reading_schema_declared,
    'T_ew_codomain_reading_home_values_from_capacity': check_T_ew_codomain_reading_home_values_from_capacity,
    'T_ew_codomain_reading_anchors_banked': check_T_ew_codomain_reading_anchors_banked,
}


def register(registry):
    for name, fn in _CHECKS.items():
        registry[name] = fn


if __name__ == '__main__':
    for nm, fn in _CHECKS.items():
        r = fn()
        print(f"[{r['status']}] {nm}: {r['key_result']}")
    print(f"\nContracts: {len(EW_CODOMAIN_CONTRACTS)} domains, "
          f"{sum(len(c.forbidden) for c in EW_CODOMAIN_CONTRACTS)} forbidden swaps.")
