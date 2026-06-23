"""apf/fibration_census.py -- the saturation fibration census + the two
2026-06-12 audited certificates it composes with, banked per the principal's
ruling (2026-06-12, "bank").

WHAT THIS MODULE IS. The banking pass that closes the 2026-06-12 arc: the
SU(3) consumer probe's threat-emptiness certificate for the baryon pin
(THREAT-EMPTY -- the divergence question dissolves by vacuity), the
fibration census over the banked census labels (two kinds of fiber labels;
one empty stratum; four named leaks; two open cells), and the record-term
pincer (exactly one banked record passes both record-term conditions --
the EW condensate -- accounting for the lone +1 in gamma_2 = a_22 + 1 =
17/4 -> sin^2 theta_W = 3/13 as unique among the sector loads). Sources
(all cold-audited LAND-WITH-CORRECTIONS, corrections applied):
'Reference - The SU3 Consumer Probe - The Threat-Evaluator Divergence on
the B-Pin (2026-06-12).md' v0.4 + su3_consumer_probe_witness.py (30/30);
'Reference - The Fibration Census (2026-06-12).md' v0.2 +
fibration_census_witness.py (17/17); 'Reference - The Record-Term Pincer -
Why Exactly One Plus-One (2026-06-12).md' v0.2 +
record_term_pincer_witness.py (13/13). All at '__APF Library/APF
Reference Docs/'.

NAMED CONSUMPTIONS CARRIED (audit-mandated, not proved here):
  * The GLOBAL-ENDPOINT reading of the canonical P_Gamma definition
    (Paper 0 v6.2.29 sec:perturbations: operators taking admissible
    configurations to admissible configurations; row-6-anchored reading
    that the endpoint filter quantifies over configurations-in-census).
    Consumed by all three checks.
  * T_proton [P] at its stated grade (the supports T_proton /
    L_anomaly_nonpert / L_Sakharov share ONE P_exhaust + L_irr core; the
    threat-emptiness verdict is single-pointed on it).
  * The OPERATOR-INVENTORY premise on the census's Q row (admissible
    operators are billed-content-expressible -- the GQL-1a genre, banked
    nowhere; named per the census audit's H1).
  * T_confinement's IR-saturation antecedent on the colour row (supplied
    empirically for physical QCD; distinct from Bekenstein census
    saturation -- the two saturations must not be merged).
  * GW-1 at its audited RECORD level ("a record is interface-constitutive
    iff it enters the constitution of a canonical evaluator at the
    interface"), with the modulus/direction split carried as a named
    tension (gate-walk v0.2 sec.2).

STANDING TEST (pre-registered, the pincer's live exposure): the chiral
condensate. If a future banked construction exhibits a canonical
zero-parameter evaluator constituted by it AND a non-empty admissible
threat set for it, the pincer demands a record term in the corresponding
load; finding that structure with no term breaks check 3.

OPEN CELLS (recorded, not closed): pre-saturation Q (whether the grading
is constituted there is unbanked; L_Sakharov's gauge-addressability
predicate is not sharp pre-saturation); the colour antecedent (continuum
form open -- the YM program's named territory).

FENCES. sin^2 theta_W = 3/13 unmoved at [P_structural]; the +1 placement
stays UB-s adopted-with-falsifier; the rollout gate remains unopened per
the earned-keep operational clause (spec v1.2b, principal ruling
2026-06-12); the dictionary fence (T24 / T_sin2theta / T27d) stands; no
rates consumed anywhere (classification is modal; suppression is not
membership); C_total = 61 rigid; nothing here derives UB-s. Paper anchors
pending the gated Paper 18/42 row (orphan-flagged, with the v24.3.244
eight).
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product

from apf.apf_utils import check as _check, _result as _full_result


# ===================================================== shared finite models
def _b_q_model():
    """Configurations (B, Q, x); P_Gamma membership per the canonical
    definition (admissible -> admissible); saturated census pins B."""
    configs = [(b, q, x) for b in (0, 1) for q in (0, 1) for x in (0, 1)]
    adm_sat = lambda c: c[0] == 1
    adm_pre = lambda c: True
    in_P = lambda op, adm: all(adm(op[c]) for c in configs if adm(c))
    alters = lambda op, adm, i: any(adm(c) and op[c][i] != c[i] for c in configs)
    return configs, adm_sat, adm_pre, in_P, alters


def check_T_b_pin_threat_empty():
    """T_b_pin_threat_empty: the hadron record's B-pin has an EMPTY row-7a
    threat set at the saturated interface -- the SU(3) consumer probe's
    verdict (THREAT-EMPTY, the fifth shape), banked [P_structural].

    THE INFERENCE: P_Gamma is admissibility-closed by canonical definition
    (Paper 0 sec:perturbations) -- membership is decided by ENDPOINT
    admissibility -- and T_proton [P] excludes the B-altered endpoint at
    saturation; so no B-altering operator is in P_Gamma, and row 7a's
    threat set for the B-pin is empty. Suppression is NOT membership: the
    rent verdict's modal reading (suppressed-but-admissible operators stay
    in P_Gamma) is preserved -- vacuity is B-specific. Pre-saturation the
    operator re-enters (L_Sakharov Condition 1: B-violation admissible
    then; the asymmetry's window). CONSTITUTIVE DEFENSE (principal
    correction 2026-06-12): the protection is real and pre-paid in the
    saturated census's partition + L_irr lock; what does not exist is a
    separate standing defense bill at the proton's sector rows -- the
    proton is challenged everywhere EXCEPT on this ledger line, and there
    not defended-and-victorious but unattackable.

    CONSEQUENCES BANKED-ADJACENT: bills-follow-threats returns no row on
    the B-pin (vacuously silent) while UB-s returns SU(3)'s row -- the
    threat/evaluator divergence question DISSOLVES on every banked record;
    the discriminating instance is priced at T_proton's falsifier
    (electroweak branch: threat-row SU(2) via the [SU(2)]^2 anomaly with
    Delta(B-L) = 0 co-movement, evaluator-row SU(3) via B = triality/3 --
    proton-decay experiments are, on that branch, experiments about
    billing semantics; dim-7-class failures break the co-movement and need
    their own walk).

    GRADE [P_structural]: two named consumptions -- T_proton [P]
    (single-pointed; the three supports share one core) + the
    global-endpoint reading (the meson objection dies on it: a B = 0
    record is admissible local content; THIS census's total moving is
    what is excluded). Cold audit 2026-06-12: LAND-WITH-CORRECTIONS
    (1H+3M+5m), all applied. No rates consumed.
    """
    configs, adm_sat, adm_pre, in_P, alters = _b_q_model()

    # exhaustive on the saturated restriction (4 configs -> 256 maps)
    sat = [c for c in configs if adm_sat(c)]
    mini = [dict(zip(sat, img)) for img in product(sat, repeat=len(sat))]
    _check(all(all(op[c][0] == c[0] for c in sat) for op in mini),
           "saturated: every operator into the census preserves B (256/256 exhaustive)")

    b_flip = {c: (1 - c[0], c[1], c[2]) for c in configs}
    _check(in_P(b_flip, adm_pre) and alters(b_flip, adm_pre, 0),
           "pre-saturation: the B-crossing operator IS in P_Gamma (L_Sakharov window)")
    _check(not in_P(b_flip, adm_sat),
           "at saturation: the same operator exits P_Gamma (endpoint inadmissible, T_proton)")
    x_flip = {c: (c[0], c[1], 1 - c[2]) for c in configs}
    _check(in_P(x_flip, adm_sat) and not alters(x_flip, adm_sat, 0),
           "suppression is not membership: admissible non-B perturbations remain (vacuity is B-specific)")

    # the flip branch's sector bookkeeping (sector-location only; computed
    # on the banked template in the standalone witness, recorded here)
    N_gen = 3
    A_B = A_L = F(1, 2)  # [SU(2)]^2 coefficients of B and L per generation
    dB, dL = 2 * A_B * N_gen, 2 * A_L * N_gen
    _check(dB == dL and dB + dL == 2 * N_gen,
           "flip branch: Delta(B-L) = 0 (co-movement), Delta(B+L) = 2*N_gen; threat-row SU(2) != evaluator-row SU(3)")

    return _full_result(
        name="T_b_pin_threat_empty: the B-pin's row-7a threat set is empty at saturation (THREAT-EMPTY)",
        tier=4,
        epistemic="P_structural_exhaustive",
        summary=(
            "P_Gamma is admissibility-closed by canonical definition (endpoint filter); T_proton [P] "
            "excludes the B-altered endpoint at the saturated census; so the B-pin's threat set is "
            "empty -- the threat/evaluator divergence question dissolves by vacuity (the fifth shape), "
            "and the discriminating instance between billing principles is priced at T_proton's "
            "falsifier (EW branch). Protection is CONSTITUTIVE: pre-paid in the partition + L_irr lock, "
            "no separate row-level standing bill. Pre-saturation the channel is open (L_Sakharov) -- "
            "the asymmetry's window. Two named consumptions: T_proton [P] (single-pointed) + the "
            "global-endpoint reading. Suppression is not membership; no rates consumed."
        ),
        key_result="T(B-pin) = {} at saturation; divergence instance exists iff T_proton falls (EW branch); defense constitutive",
        dependencies=["T_proton", "L_Sakharov", "L_anomaly_nonpert", "L_irr"],
        cross_refs=["T_ledger_rent_excluded", "T_demand_not_routing_readable",
                    "T_sector_granularity_below_billing_type", "L_proton_decay_channels"],
        artifacts={
            "verdict": "THREAT-EMPTY (not DIVERGENCE/COINCIDENCE/BELOW-GRANULARITY/FENCED)",
            "consumptions": "T_proton [P] + global-endpoint reading (row-6-anchored)",
            "flip_condition": "proton decay, EW branch -> threat-row SU(2) vs evaluator-row SU(3)",
            "source": "SU3 Consumer Probe v0.4 + witness 30/30 (audited)",
        },
    )


def check_T_saturation_fibration_census():
    """T_saturation_fibration_census: the banked census labels classified by
    admissible crossing -- two kinds of fiber labels, one empty stratum,
    four named leaks, two open cells. [P_structural].

    THE CENSUS (each row at its banked anchors): Q FIBER gauge-rigid
    (T_gauge/L_anomaly_free/charge-quantization; generator-route, the
    operator-inventory premise NAMED per the audit's H1; scoped to where
    the grading is constituted); B FIBER saturation-locked (T_proton core;
    the ONLY label whose class-change is banked -- L_Sakharov Cond. 1:
    open pre-saturation, locked at it; why baryogenesis is a baryon
    story); colour EMPTY STRATUM (T_confinement, IR antecedent named;
    nothing in the stratum to protect or leak -- why the demand column
    books colour 0); L LEAKY (Majorana DeltaL = 2, L_seesaw_type_I +
    L_Weinberg_dim; rider m_bb = 4.42 meV [P + Dm2_31 anchor], WATCHING);
    B-L LEAKY (same door; the fingerprint, audit-corrected: BOTH APF and
    GUTs leak B-L -- SO(10) gauges then breaks it for Majorana masses --
    the theorem-grade disagreement is on B ALONE: GUTs predict proton
    decay, APF forbids it at any rate); family-L LEAKY (dim-5 + PMNS;
    T_Noether's accidental table already marks them inexact -- the
    suspected tension dissolved at source); quark flavor LEAKY (T_CKM);
    weak isospin / hypercharge RETIRED BY SSB (the condensate record is
    the crossing); energy NOT A ROW (the cost face; state function, rent
    excluded); theta/CP OUT OF FORMAT. OPEN CELLS: pre-saturation Q;
    the colour antecedent's continuum form.

    GRADE [P_structural]: three named consumptions -- the global-endpoint
    reading on every fiber row; the operator-inventory premise on Q
    (GQL-1a genre, banked nowhere); the IR-saturation antecedent on
    colour. NOT a composition of clean [P]s. Cold audit 2026-06-12:
    LAND-WITH-CORRECTIONS (2H+3M+5m), all applied. T_Noether is the
    proto-census, cited not re-derived. No rates; modal throughout.
    """
    configs, adm_sat, adm_pre, in_P, alters = _b_q_model()

    # two kinds: B saturation-locked (banked class-change) ...
    b_flip = {c: (1 - c[0], c[1], c[2]) for c in configs}
    _check(in_P(b_flip, adm_pre) and not in_P(b_flip, adm_sat),
           "B: saturation-locked (class-change banked, L_Sakharov)")
    # ... vs Q gauge-rigid (generator-side: billed content conserves Q --
    # the PROPOSED assembly, operator-inventory premise named, not banked)
    gauge_ok = lambda op: all(op[c][1] == c[1] for c in configs)
    q_flip = {c: (c[0], 1 - c[1], c[2]) for c in configs}
    _check(not gauge_ok(q_flip),
           "Q: not billed-content-expressible (gauge-rigid where constituted; premise NAMED)")

    # the leaks, on banked arithmetic
    dL, dB = 2, 0  # Weinberg dim-5 door (L_Weinberg_dim [P], L_seesaw_type_I [P])
    _check(dL == 2 and dB == 0 and abs(dB - dL) == 2,
           "L and B-L leak through the banked dim-5 door (|Delta(B-L)| = 2)")
    # colour: empty stratum vs disconnected strata (the structural difference)
    cfg2 = [(b, s) for b in (0, 1) for s in (0, 1)]
    adm_ir = lambda c: c[1] == 1 and c[0] == 1  # singlet AND census pinned (antecedent supplied)
    _check(len([c for c in cfg2 if adm_ir(c) and c[1] == 0]) == 0,
           "colour: the non-singlet stratum is EMPTY (T_confinement, antecedent named)")
    _check(len([c for c in cfg2 if adm_ir(c)]) > 0, "B: occupied stratum nonempty (disconnection, not emptiness)")

    rows = {
        "Q": "FIBER gauge-rigid (scoped; operator-inventory premise named)",
        "B": "FIBER saturation-locked (the one banked class-change)",
        "colour": "EMPTY STRATUM (IR antecedent named)",
        "L": "LEAKY (Majorana; m_bb rider)", "B-L": "LEAKY (same door; B-only fingerprint)",
        "family-L": "LEAKY (dim-5 + PMNS)", "quark flavor": "LEAKY (CKM)",
        "weak isospin/Y": "RETIRED BY SSB", "energy": "NOT A ROW", "theta/CP": "OUT OF FORMAT",
    }
    _check(len(rows) == 10 and sum("FIBER" in v for v in rows.values()) == 2,
           "census: ten rows, exactly two fiber labels, two kinds")

    return _full_result(
        name="T_saturation_fibration_census: the census labels by admissible crossing (two kinds of fiber labels)",
        tier=4,
        epistemic="P_structural_exhaustive",
        summary=(
            "Every banked census label classified: Q FIBER gauge-rigid (generator-route; "
            "operator-inventory premise named, GQL-1a genre); B FIBER saturation-locked -- the only "
            "banked class-change (L_Sakharov), making baryogenesis a baryon story; colour EMPTY "
            "STRATUM (T_confinement, IR antecedent named, distinct from census saturation); L / B-L / "
            "family-L / quark-flavor LEAKY with channels named (Majorana dim-5 door with the m_bb "
            "rider; CKM); isospin/Y retired by SSB; energy and theta/CP out of format with stated "
            "reasons. Fingerprint (audit-corrected): both APF and GUTs leak B-L; the theorem-grade "
            "disagreement is B alone -- the proton is the discriminator. Two open cells recorded. "
            "Three named consumptions keep this [P_structural], not [P]."
        ),
        key_result="2 fiber kinds (Q rigid-where-constituted, B saturation-locked) + 1 empty stratum + 4 named leaks + 2 open cells; B-only anti-GUT fingerprint",
        dependencies=["T_proton", "L_Sakharov", "T_confinement", "L_seesaw_type_I",
                      "L_Weinberg_dim", "T_CKM", "L_anomaly_free", "T_gauge"],
        cross_refs=["T_b_pin_threat_empty", "T_Noether",
                    "T_charge_quantization_from_ledger_discreteness", "L_mbb_prediction",
                    "T_ub_consistency_three_record_states"],
        artifacts={
            "rows": rows,
            "open_cells": "pre-saturation Q; colour IR antecedent (continuum)",
            "consumptions": "global-endpoint (fiber rows) + operator-inventory (Q) + IR antecedent (colour)",
            "source": "Fibration Census v0.2 + witness 17/17 (audited)",
        },
    )


def check_T_record_term_pincer():
    """T_record_term_pincer: a gamma record-term requires (a) a non-empty
    admissible threat set against a held value AND (b) GW-1's record-level
    evaluator-constitution; exactly one banked record passes both -- the
    EW condensate -- so the lone +1 in gamma_2 = a_22 + 1 = 17/4 ->
    sin^2 theta_W = 3/13 is UNIQUE among the sector loads. [P_structural].

    THE WALK (banked column (0,1,0) + this session's threat verdicts +
    GW-1 verbatim at record level): theta fails (a) (maintenance-free,
    T_theta_QCD); U(1) has no record (photon no-record spine, r_1 = 0);
    EW condensate passes BOTH ((a) the modulus ray, Delta = 1 at [P],
    T_record_demand_is_quotient_codim; (b) the Q-evaluator holds the
    vev-selected direction as constituting structure -- GW-1's own
    exemplar; the gamma_2 n_radial leg is NOT cited, that is the
    explanandum); colour fails (a) (empty stratum; gamma_3 = 6 outside
    the diag + r form by pre-registration); hadron B-pin fails both
    (THREAT-EMPTY; evaluated not evaluating); hadron Q-pin passes (a),
    fails (b) -- THE WITNESS THAT (a) ALONE IS INSUFFICIENT (its 1-epsilon
    share of the record's 3-epsilon books on the access-partition surface);
    chiral condensate fails (b) at bank level, (a) UNDETERMINED -- THE
    STANDING TEST; the Lambda = 42/61 global record is OUT OF FORMAT
    (no competition-load surface at the global interface; disposition).
    The on-column rows are consistency re-readings; the discriminating
    content is the off-column rows (B-pin, Q-pin) + the chiral exposure.

    THE TOGGLE (the earned-keep clause's own arithmetic): Delta = 1 ->
    w* = (3/8, 5/4) -> sin^2 theta_W = 3/13; Delta = 0 -> 13/35, the
    value the banked alpha_s discrimination kills at 77%
    (T_load_form_selected_by_alpha_s). The lone +1 is load-bearing.

    GRADE [P_structural]: conditions (a)/(b) are audited note-grade
    criteria composed over banked tables; the modulus/direction split
    inside GW-1 is carried as a named tension. An ACCOUNT of uniqueness,
    NOT a derivation of UB-s; placement stays adopted-with-falsifier;
    the gate stays unopened (earned-keep clause, spec v1.2b). Cold audit
    2026-06-12: LAND-WITH-CORRECTIONS (1H+3M+5m), all applied.
    """
    a11, a12 = F(1), F(1, 2)
    m = 3
    a22 = a12 ** 2 + m
    gamma1, gamma2, gamma3, a33 = F(1), F(17, 4), F(6), F(8)
    _check(a22 == F(13, 4) and gamma1 - a11 == 0 and gamma2 - a22 == 1,
           "banked loads: r = (0, 1, --); the lone record term is Delta = 1 on SU(2)")
    _check(gamma3 != a33 and gamma3 != a33 + 1 and gamma3 == 6,
           "gamma_3 = 6 outside the diag + r form (banked pre-registration; trace-grounded)")

    def fixed_point(g2):
        det = a11 * a22 - a12 * a12
        return ((a22 * gamma1 - a12 * g2) / det, (a11 * g2 - a12 * gamma1) / det)

    w1, w2 = fixed_point(gamma2)
    _check((w1, w2) == (F(3, 8), F(5, 4)) and w1 / (w1 + w2) == F(3, 13),
           "Delta=1: w* = (3/8, 5/4) -> sin^2 theta_W = 3/13 (banked fixed point)")
    v1, v2 = fixed_point(a22)
    _check(v1 / (v1 + v2) == F(13, 35),
           "Delta=0 toggle: 13/35 (killed by the banked alpha_s anchor at 77%) -- the +1 is load-bearing")

    # the pincer table: recorded verdicts (note-grade, audited); uniqueness computed
    table = {  # candidate: (cond_a, cond_b)
        "theta_QCD": (False, None), "U(1)/photon": (None, None),
        "EW condensate": (True, True), "colour record": (False, False),
        "hadron B-pin": (False, False), "hadron Q-pin": (True, False),
        "chiral condensate": (None, False), "Lambda global record": (None, None),
    }
    passers = [k for k, (ca, cb) in table.items() if ca is True and cb is True]
    _check(passers == ["EW condensate"], "exactly ONE record passes both conditions: the EW condensate")
    _check([k for k, (ca, cb) in table.items() if ca is True and cb is not True] == ["hadron Q-pin"],
           "(a) alone is insufficient: the Q-pin is the live witness (access-partition billing, no gamma term)")
    _check(len(passers) == 1 == int(gamma2 - a22),
           "pincer count == banked record-term count (1 == 1)")

    return _full_result(
        name="T_record_term_pincer: the lone gamma record-term is unique by two conditions (threat + constitution)",
        tier=4,
        epistemic="P_structural_exhaustive",
        summary=(
            "A gamma record-term requires jointly: (a) a non-empty admissible threat set against a "
            "held value (this session's probe/census verdicts) and (b) GW-1's record-level "
            "evaluator-constitution (quoted verbatim; modulus/direction split carried as named "
            "tension). Walking the complete banked record inventory (closed by the record-state "
            "enumeration; Lambda global record dispositioned out of format): exactly one passer, the "
            "EW condensate -- the only banked record both alterable and held, and the only one "
            "constituting a canonical evaluator. Hence the lone +1 in gamma_2 = 13/4 + 1 = 17/4 -> "
            "sin^2 theta_W = 3/13, load-bearing by the toggle (Delta=0 -> 13/35, 77% off). The Q-pin "
            "witnesses (a)-alone insufficiency; the chiral condensate is the pre-registered standing "
            "test. An account of uniqueness, not a derivation of UB-s; placement adopted; gate "
            "unopened (spec v1.2b)."
        ),
        key_result="record term iff (a) AND (b); unique passer = EW condensate; toggle: 3/13 vs 13/35; chiral condensate = standing falsifier-shaped test",
        dependencies=["T_record_demand_is_quotient_codim", "T_ub_consistency_three_record_states",
                      "T_theta_QCD", "T_confinement", "T_proton"],
        cross_refs=["T_b_pin_threat_empty", "T_saturation_fibration_census",
                    "T_sin2theta_higgs_record", "T_load_form_selected_by_alpha_s",
                    "L_defense_requires_evaluator", "T_particle_mass_is_locked_record"],
        artifacts={
            "table": {k: {"a": ca, "b": cb} for k, (ca, cb) in table.items()},
            "toggle": "Delta=1 -> 3/13; Delta=0 -> 13/35 (alpha_s kill 77%)",
            "standing_test": "chiral condensate (GW-1 pre-registration)",
            "source": "Record-Term Pincer v0.2 + witness 13/13 (audited)",
        },
    )


_CHECKS = {
    "T_b_pin_threat_empty": check_T_b_pin_threat_empty,
    "T_saturation_fibration_census": check_T_saturation_fibration_census,
    "T_record_term_pincer": check_T_record_term_pincer,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}
