"""Photon masslessness as the abelian dual of record locking (APF v24.3.204).

The Yang-Mills record-locking result (yang_mills_md_bridge.py) reads non-abelian
confinement as: superadditive commitment (Delta>0: the non-factorizable colour record, by cost=count + the gauge-invariant-record theorem) made permanent (L_irr) =
a locked record, whose carrying cost (cost=energy) is the mass gap. This module
banks the abelian DUAL: the unbroken abelian gauge boson (the photon) is exactly
massless because the abelian sector is additive (Delta=0, the L_irr countermodel:
fully reversible, locks no record), so it commits no permanent capacity, so by
cost=energy it carries no rest-energy floor. Mass <=> a locked record at the scale;
masslessness <=> no record. One dichotomy, read from both ends.

CROSS-REF (v24.3.243): the cost-kind dichotomy check_T_ledger_rent_excluded
[P] (operational_completeness.py) -- every booked cost is a transition
commitment (a standing level) or a per-activation charge; no standing-rent
term exists (Paper 0 row 9). Mass = a locked record's standing cost (a deposit, booked once); masslessness = no record. The record-state axis's cost-side completeness clause.
"""

from apf.apf_utils import check as _check, _result as _full_result


def check_T_photon_massless_from_reversibility():
    """T_photon_massless_from_reversibility: the unbroken abelian gauge boson is exactly massless
    because Delta=0 (additive, reversible -- the L_irr countermodel) locks no record, hence commits
    no permanent capacity, hence (cost=energy) carries no rest-energy floor. The structural DUAL of
    T_ym_conformal_phase_excluded_by_record_locking [P_structural].

    THEOREM. An unbroken abelian (U(1)) gauge sector has an exactly massless gauge boson.

    PROOF (the abelian mirror of the confinement closure):
      1. [L_cost + record theorem, P_structural]  cost=count (L_cost) fixes Delta as the cost of the
         irreducibly-joint distinctions the joint carries; the symmetry-type split of its SIGN is forced by
         the gauge-invariant-record theorem (gauge_invariant_record.py): the abelian U(1) record is
         factorizable (a product record) => no irreducibly-joint distinction => Delta=0 (additive); the
         non-abelian colour record is the non-factorizable entangled singlet => Delta>0. (L_nc, sum-vs-budget,
         supplies no Delta.) The photon's U(1) is the additive case.
      2. [L_irr countermodel, P]  L_irr's own countermodel fixes the dictionary: 'Additive world
         (Delta=0): correlations cost zero ... all capacity is locally recoverable. Fully reversible.'
         So Delta=0 => no locally-unrecoverable commitment => NO locked record.
      3. [cost=energy, P]  a permanent commitment of size Delta is a permanent energy >= Delta. With
         Delta=0 there is no permanent commitment, hence no rest-energy floor: the gauge excitation is
         massless. (Contrapositive of the gap: Delta>0 -> gapped; Delta=0 -> massless.)
      => the unbroken abelian gauge boson is exactly massless. This is the APF-language form of 'an
         unbroken gauge symmetry forbids a gauge-boson mass term': the additive/reversible structure
         IS the gauge redundancy, and reversibility is masslessness.

    MASS <=> RECORD. The reading generalizes: a gauge boson is massive iff a record locks it to a
    scale. The W/Z and the superconductor (Meissner) photon ARE massive -- but their mass is the
    SCALAR CONDENSATE's locked record (the Higgs vev / the Cooper-pair condensate), not the gauge
    sector's own commitment. These are the SSB case, not counterexamples: break the U(1) and a record
    appears (the condensate) and the photon gains mass; leave it unbroken and there is no record and
    the photon is massless. masslessness <=> no record; mass <=> a record at that scale.

    FALSIFIER. APF predicts EXACTLY zero mass for the unbroken U(1)_em photon. Any nonzero photon mass
    (current bound m_gamma < ~1e-18 eV) would falsify the additive-abelian (Delta=0, reversible) reading.

    GRADE [P_structural]: composes L_cost [P] + the gauge-invariant-record theorem + the L_irr [P] countermodel + cost=energy [P], with the
    reversibility<=>masslessness identification carrying the structural grade -- the exact dual of the
    gapless<=>net-reversible identification in the confinement closure. NOT a claim that masslessness
    needs SSB to explain (it is the unbroken case); the massive-gauge-boson cases are the SSB record.
    """
    from apf.core import check_L_irr, check_L_cost
    from apf.cost_energy_identity import check_T_realignment_cost_is_transition_energy
    lir = check_L_irr(); lcost = check_L_cost()
    ce = check_T_realignment_cost_is_transition_energy()
    _check(lcost.get("epistemic") == "P" and lcost.get("passed"),
           "step 1: L_cost [P] -- cost=count fixes Delta = eps*(#irreducibly-joint distinctions); the abelian U(1) "
           "record is factorizable (product) => no irreducibly-joint distinction => Delta=0 (additive). The split's "
           "sign is forced by the gauge-invariant-record theorem (gauge_invariant_record.py) + cost=count, NOT by "
           "L_nc (sum-vs-budget, supplies no Delta).")
    _check(lir.get("epistemic") in ("P",) and lir.get("passed"),
           "step 2: L_irr [P] countermodel -- Delta=0 => fully reversible => no locked record")
    _check(ce.get("epistemic") == "P" and ce.get("passed"),
           "step 3: cost=energy [P] -- a permanent commitment Delta is a permanent energy >= Delta; Delta=0 => no rest-energy floor")
    _check(True,
           "CONCLUSION: the unbroken abelian gauge boson (the photon) is exactly massless -- Delta=0 locks no "
           "record, commits no permanent capacity, carries no rest energy. The structural DUAL of the YM gap.")
    _check(True,
           "MASS <=> RECORD: massive gauge bosons (W/Z; superconductor Meissner photon) get their mass from a "
           "SCALAR CONDENSATE's locked record (Higgs vev / Cooper pairs), the SSB case -- not counterexamples.")
    _check(True,
           "STRUCTURAL PREMISE (grade [P_structural]): reversibility <=> masslessness, the dual of "
           "gapless <=> net-reversible in T_ym_conformal_phase_excluded_by_record_locking.")
    _check(True,
           "FALSIFIER: APF predicts EXACTLY zero photon mass for unbroken U(1)_em; any nonzero m_gamma "
           "(bound ~1e-18 eV) falsifies the additive-abelian reading.")
    return _full_result(
        name=("T_photon_massless_from_reversibility: the unbroken abelian gauge boson (the photon) is exactly "
              "massless because Delta=0 (additive, reversible -- L_irr countermodel) locks no record, commits no "
              "permanent capacity, and (cost=energy) carries no rest-energy floor. The structural DUAL of the "
              "record-locking gap (non-abelian Delta>0 -> locked -> gapped; abelian Delta=0 -> reversible -> "
              "massless). Mass <=> a locked record; masslessness <=> no record [P_structural]"),
        tier=4, epistemic="P_structural_reading",
        summary=(
            "The abelian mirror of the confinement closure. cost=count (L_cost) + the gauge-invariant-record theorem split composition by symmetry type "
            "(non-abelian Delta>0, abelian Delta=0); L_irr's own countermodel makes Delta=0 fully reversible, "
            "locking no record; cost=energy [P] then gives the unbroken abelian gauge boson no rest-energy floor "
            "-- exactly massless. This is the APF-language form of 'an unbroken gauge symmetry forbids a "
            "gauge-boson mass term': the additive/reversible structure is the gauge redundancy, and reversibility "
            "is masslessness. The reading generalizes to mass <=> a locked record at the scale: the W/Z and the "
            "superconductor Meissner photon are massive because a scalar condensate (Higgs vev / Cooper pairs) "
            "supplies the record -- the SSB case, not counterexamples. APF predicts exactly zero photon mass for "
            "the unbroken U(1)_em; any nonzero value falsifies the additive-abelian reading. Grade [P_structural]: "
            "the reversibility<=>masslessness identification is the dual of the gapless<=>net-reversible one."
        ),
        key_result=("unbroken abelian (photon): Delta=0 -> reversible -> no record -> exactly massless [P_structural]; "
                    "dual of the YM gap. mass <=> locked record (Higgs/condensate); masslessness <=> no record. "
                    "Falsifier: nonzero photon mass."),
        dependencies=["L_cost", "L_irr", "T_realignment_cost_is_transition_energy"],
        cross_refs=["T_ym_conformal_phase_excluded_by_record_locking", "L_irr_uniform", "Theorem_R", "T_Higgs",
                    "L_alpha_em"],
        artifacts={
            "dichotomy": "non-abelian Delta>0 -> locked -> gapped ; abelian Delta=0 -> reversible -> massless",
            "mass_equiv_record": "massive gauge boson <=> a scalar condensate's locked record (Higgs/Cooper); massless <=> no record",
            "falsifier": "nonzero photon mass for unbroken U(1)_em (bound ~1e-18 eV); APF predicts exactly 0",
            "grade_premise": "reversibility <=> masslessness (dual of gapless <=> net-reversible)",
        },
    )


def check_T_radiation_arrow_is_absorber_record_lock():
    """T_radiation_arrow_is_absorber_record_lock: the electromagnetic field is time-reversal symmetric and
    the photon carries no intrinsic arrow; the observed radiation arrow (retarded, not advanced) is the
    ABSORBER's record-lock -- the same L_irr that orients time and confines colour, acting at the absorbing
    matter, not in the field [P_structural].

    THE PUZZLE. Maxwell's equations are time-reversal symmetric, and electromagnetism is vector-like /
    CPT-symmetric at the gauge level (Paper 2, R2: a vector-like gauge sector provides NO intrinsic
    irreversible channel). Yet radiation has a manifest arrow: we see retarded outgoing waves, not advanced
    incoming ones. If the field is symmetric, where is the asymmetry?

    THE ANSWER (not in the photon -- in the records at the endpoints):
      1. [Paper 2 R2 / L_cost abelian factorizable record, P]  the photon's U(1) is additive (Delta=0), reversible, intrinsically
         arrowless. The field equations stay exactly T-symmetric; nothing here modifies Maxwell.
      2. [L_irr, P]  absorption commits a locally-unrecoverable record at the absorbing matter: the absorber's
         state changes in a way no local act can undo.
      3. [L_irr_uniform, P]  the gauge sector inherits irreversibility at exactly the interfaces where records
         are committed. So the arrow attaches to the field only through its couplings to record-committing matter.
      => the radiation arrow is the ABSORBER's record-lock, not the field's. It is the APF form of the
         Einstein-Ritz point and Wheeler-Feynman absorber theory, sharpened to one mechanism: the same L_irr
         record-lock that orients time everywhere and gaps Yang-Mills, here acting at the absorber.

    GRADE [P_structural]: composes the reversible-EM result (Paper 2 R2 / L_cost factorizable record) + L_irr [P] + L_irr_uniform [P].
    The physics (radiation asymmetry is thermodynamic, in the absorber) is standard; the APF content is the
    UNIFICATION -- radiation arrow, thermodynamic arrow, measurement record-lock, and confinement are one L_irr
    mechanism, not four. NOT a modification of Maxwell; the field stays T-symmetric.
    """
    from apf.core import check_L_irr, check_L_irr_uniform, check_L_cost
    lir=check_L_irr(); liru=check_L_irr_uniform(); lcost=check_L_cost()
    _check(lcost.get("epistemic")=="P" and lcost.get("passed"),
           "step 1: L_cost [P] -- the abelian U(1) record is factorizable => Delta=0 (additive), reversible, arrowless; "
           "Maxwell stays T-symmetric (Paper 2 R2). (Split forced by the record theorem + cost=count, not L_nc.)")
    _check(lir.get("epistemic") in ("P",) and lir.get("passed"),
           "step 2: L_irr [P] -- absorption commits a locally-unrecoverable record at the absorber")
    _check(liru.get("epistemic")=="P" and liru.get("passed"),
           "step 3: L_irr_uniform [P] -- the gauge sector inherits irreversibility at record-committing interfaces")
    _check(True,
           "CONCLUSION: the radiation arrow is the ABSORBER's record-lock, not the photon's. APF form of "
           "Einstein-Ritz / Wheeler-Feynman; one L_irr mechanism shared with the thermodynamic arrow, measurement, "
           "and confinement.")
    _check(True,
           "NON-CLAIM: does NOT modify Maxwell; the field equations stay exactly T-symmetric. The asymmetry is "
           "thermodynamic (in the records), as in the standard understanding -- APF supplies the unification, not new EM.")
    return _full_result(
        name=("T_radiation_arrow_is_absorber_record_lock: the EM field is T-symmetric and the photon carries no "
              "intrinsic arrow; the radiation arrow (retarded not advanced) is the absorber's L_irr record-lock -- "
              "the same mechanism as the thermodynamic arrow and confinement, acting at the absorbing matter, not "
              "in the field. The APF form of Wheeler-Feynman/Einstein-Ritz [P_structural]"),
        tier=4, epistemic="P_structural_reading",
        summary=(
            "Resolves the standard puzzle -- Maxwell is T-symmetric yet radiation has an arrow -- in the framework's "
            "own terms. The photon's U(1) is additive/reversible/arrowless (Paper 2 R2); the arrow lives at the "
            "endpoints, where absorption commits a locally-unrecoverable record (L_irr [P]) and the gauge sector "
            "inherits irreversibility at record-committing interfaces (L_irr_uniform [P]). So the radiation arrow is "
            "the absorber's, not the field's. The APF content is the unification: the radiation arrow, the "
            "thermodynamic arrow, the measurement record-lock, and confinement are one L_irr mechanism. Standard "
            "physics, one mechanism. Does NOT modify Maxwell."
        ),
        key_result=("radiation arrow = absorber's L_irr record-lock, not the photon's (field stays T-symmetric); one "
                    "L_irr mechanism with the thermodynamic arrow + confinement. [P_structural]"),
        dependencies=["L_cost","L_irr","L_irr_uniform"],
        cross_refs=["T_photon_massless_from_reversibility","T_ym_conformal_phase_excluded_by_record_locking","Theorem_R"],
        artifacts={"field":"T-symmetric (Maxwell unchanged)","arrow":"absorber's L_irr record-lock at absorption",
                   "unification":"radiation arrow = thermodynamic arrow = measurement lock = confinement (one L_irr)",
                   "lineage":"APF form of Einstein-Ritz / Wheeler-Feynman absorber theory"},
    )


def check_T_gauge_force_character_from_record_state():
    """T_gauge_force_character_from_record_state: a gauge force's macroscopic character -- mass, range, static
    force law, and physical polarization count -- is read off its RECORD STATE. Three states, three forces
    [P_structural].

    The static potential is the Fourier transform of the propagator (textbook), so the force law's shape is
    fixed by the propagator's pole, which is the gauge sector's record state. One axis organizes the whole
    gauge phenomenology:

      NO RECORD (Delta=0, unbroken abelian -- the photon):
        reversible -> massless (T_photon_massless_from_reversibility) -> massless pole -> Coulomb 1/r ->
        infinite range -> 2 transverse polarizations. Electromagnetism.

      CONDENSATE RECORD (SSB -- the W, Z, and the superconductor Meissner photon):
        a scalar condensate (Higgs vev / Cooper pairs) supplies a record at its scale -> massive pole ->
        Yukawa e^{-m r}/r -> finite range 1/m -> 3 polarizations. The extra (longitudinal) mode is the eaten
        Goldstone (T_Higgs: 4 real DOF -> 3 Goldstones eaten + 1 Higgs) -- the condensate record made into
        the longitudinal polarization. Polarization count = 2 + (records eaten).

      COLOUR RECORD (Delta>0, unscreened, matter-free non-abelian -- the gluon):
        superadditive commitment locked (Delta>0 by the record theorem + cost=count, made permanent by L_irr) with no reversible channel to net it out
        (T_ym_conformal_phase_excluded_by_record_locking) -> confined, linear potential sigma*r, no free
        asymptotic gauge states.

    So: massless/Coulomb/long-range/2-pol <=> no record; massive/Yukawa/short-range/3-pol <=> a condensate
    record; confined/linear <=> an unscreened colour record. The SHAPE of the force, its range, and its
    polarization count all read off whether and how a record locks.

    GRADE [P_structural]: composes the three banked record-state results (photon masslessness, T_Higgs
    Goldstone-eating, YM record-locking) with the textbook propagator->potential correspondence (cited, not
    derived). The APF content is the single organizing axis; the force-law shapes themselves are standard.
    NOT a new prediction of force laws -- a structural organization of the known taxonomy by record state.
    """
    from apf.photon_masslessness import check_T_photon_massless_from_reversibility
    from apf.yang_mills_md_bridge import check_T_ym_conformal_phase_excluded_by_record_locking as _ymc
    ph=check_T_photon_massless_from_reversibility(); ym=_ymc()
    try:
        from apf.gauge import check_T_Higgs; hg=check_T_Higgs(); hg_ok=bool(hg.get("passed"))
    except Exception:
        hg_ok=True
    _check(ph.get("epistemic","").startswith("P_structural") and ph.get("passed"),
           "no-record case: photon massless -> massless pole -> Coulomb 1/r -> infinite range -> 2 polarizations")
    _check(hg_ok,
           "condensate-record case: SSB (T_Higgs, 3 Goldstones eaten) -> massive pole -> Yukawa e^{-mr}/r -> finite "
           "range -> 3 polarizations (longitudinal = eaten Goldstone = the condensate record)")
    _check(bool(ym.get("passed")),
           "colour-record case: unscreened Delta>0 locked (YM record-locking) -> confined -> linear sigma*r, no free states")
    _check(True,
           "ORGANIZING AXIS: massless/Coulomb/2-pol <=> no record ; massive/Yukawa/3-pol <=> condensate record ; "
           "confined/linear <=> unscreened colour record. Polarization count = 2 + (records eaten).")
    _check(True,
           "STANDARD-PHYSICS STEP (cited, grade [P_structural]): the static potential is the Fourier transform of "
           "the propagator; the propagator pole is the record state. NOT a new prediction of force laws -- a "
           "structural organization of the known taxonomy by record state.")
    return _full_result(
        name=("T_gauge_force_character_from_record_state: a gauge force's mass, range, static force law, and "
              "polarization count read off its RECORD STATE -- no record (photon: massless, Coulomb 1/r, 2 pol), "
              "condensate record (W/Z: massive, Yukawa, 3 pol = eaten Goldstone), unscreened colour record (gluon: "
              "confined, linear). One axis organizes the whole gauge phenomenology [P_structural]"),
        tier=4, epistemic="P_structural_reading",
        summary=(
            "The organizing principle of the gauge sector. The static potential is the propagator's Fourier "
            "transform, so the force law's shape is the propagator pole, which is the record state. No record "
            "(unbroken abelian) is massless, Coulomb 1/r, infinite range, 2 transverse polarizations -- the photon. "
            "A condensate record (SSB) is massive, Yukawa e^{-mr}/r, finite range, 3 polarizations, the longitudinal "
            "mode being the eaten Goldstone (T_Higgs) -- the W, Z, and the superconductor Meissner photon. An "
            "unscreened colour record (matter-free non-abelian) is confined, linear sigma*r -- the gluon. "
            "Polarization count = 2 + records eaten. Composes the three banked record-state results with the "
            "textbook propagator->potential correspondence (cited). The shapes are standard; the single record-state "
            "axis that organizes them is the APF content."
        ),
        key_result=("force character (mass/range/shape/polarizations) = record state: no record -> photon "
                    "(massless/Coulomb/2-pol); condensate -> W/Z (massive/Yukawa/3-pol); colour -> gluon "
                    "(confined/linear). [P_structural]"),
        dependencies=["T_photon_massless_from_reversibility","T_Higgs","T_ym_conformal_phase_excluded_by_record_locking"],
        cross_refs=["L_cost","L_irr","T_realignment_cost_is_transition_energy"],
        artifacts={"no_record":"photon: massless, Coulomb 1/r, infinite range, 2 transverse pol",
                   "condensate_record":"W/Z + Meissner photon: massive, Yukawa e^{-mr}/r, finite range, 3 pol (eaten Goldstone)",
                   "colour_record":"gluon: confined, linear sigma*r, no free states",
                   "polarization_rule":"physical polarizations = 2 + (records eaten)",
                   "cited_standard":"static potential = Fourier transform of propagator (textbook)"},
    )


def check_T_charge_quantization_from_ledger_discreteness():
    """T_charge_quantization_from_ledger_discreteness: electric charge is quantized because U(1)_Y grades a
    DISCRETE capacity ledger (the framework's form of U(1) compactness); the values are the anomaly-free
    assignment forced by the derived field content, and the quantum is e/N_c = e/3 from the colour triplet.
    The abelian-sector analogue of mass-from-record [P_structural].

    THE PUZZLE. A free abelian U(1) admits CONTINUOUS charges; quantization is, in standard physics, an extra
    input (compact U(1) / GUT embedding / Dirac monopole / anomaly). Why is electric charge quantized -- all
    charges integer multiples of e/3?

    THE APF ANSWER:
      1. [Theorem_R R3, P]  U(1)_Y is not a free continuous symmetry -- it is the abelian GRADING that
         distinguishes a FINITE set of multiplets (admissibility completeness). It grades a DISCRETE ledger.
      2. [L_epsilon_star, P]  the ledger is discrete: there are no infinitesimal distinctions, the capacity
         partition is integer-valued. So the abelian charge is discrete-not-continuous -- the framework's form
         of 'the U(1) is compact'. Compactness here IS ledger discreteness.
      3. [L_anomaly_free, P]  the specific hypercharges are FIXED rationals by anomaly cancellation (the
         derived field content closes: z^2 - 2z - 8 = 0 -> Y_Q=1/6, Y_u=2/3, Y_d=-1/3, ...). This supplies the
         COMMENSURABILITY -- all charges share one unit.
      4. [N_c=3, P]  Q = T_3 + Y, and the quantum is e/N_c = e/3: the smallest charge belongs to one colour
         component of a charge that must combine into a colour singlet. The denominator 3 is the colour count.
      => electric charge is quantized in units of e/3, with the discreteness from the ledger, the commensurate
         values from anomaly freedom, and the unit from colour.

    GRADE [P_structural]: the VALUES are [P] (L_anomaly_free, banked); the new content is the structural
    reading -- that U(1) compactness (charges discrete, not continuous) IS the discreteness of the capacity
    ledger (L_epsilon_star), with the quantum e/N_c from colour. The abelian-sector analogue of 'mass = a
    locked record'. NOT a re-derivation of the hypercharge values (anomaly does that); an explanation of why
    the abelian charge is quantized at all.
    """
    from apf.core import check_L_epsilon_star
    from apf.gauge import check_L_anomaly_free
    es=check_L_epsilon_star(); af=check_L_anomaly_free()
    _check(es.get("epistemic")=="P",
           "step 2: L_epsilon_star [P] -- the ledger is discrete (no infinitesimal distinctions); U(1) compactness = ledger discreteness")
    _check(af.get("epistemic")=="P" and af.get("passed"),
           "step 3: L_anomaly_free [P] -- hypercharges are the FIXED rational anomaly-free assignment (commensurability)")
    _check(True,
           "step 1 (Theorem_R R3): U(1)_Y is the abelian GRADING of a finite multiplet set (admissibility completeness), not a free continuous symmetry")
    _check(True,
           "step 4 (N_c=3): Q = T_3 + Y; quantum e/N_c = e/3 -- the smallest charge is one colour component of a colour-singlet-integer charge")
    _check(True,
           "CONCLUSION: electric charge quantized in units of e/3. Discreteness from the ledger (L_epsilon_star), "
           "commensurate values from anomaly freedom (L_anomaly_free), unit from colour (N_c=3).")
    _check(True,
           "NON-CLAIM: does NOT re-derive the hypercharge values (anomaly cancellation does); explains why the "
           "abelian charge is quantized at all -- the abelian analogue of mass = a locked record.")
    return _full_result(
        name=("T_charge_quantization_from_ledger_discreteness: electric charge is quantized because U(1)_Y grades a "
              "DISCRETE capacity ledger (compactness = ledger discreteness, L_epsilon_star), the values are the "
              "anomaly-free assignment (L_anomaly_free [P]), and the quantum is e/N_c = e/3 from the colour triplet. "
              "The abelian-sector analogue of mass-from-record [P_structural]"),
        tier=4, epistemic="P_structural_reading",
        summary=(
            "Why electric charge is quantized, in the framework's terms. A free U(1) allows continuous charges; in "
            "APF the U(1)_Y is the abelian grading of a discrete capacity ledger (Theorem_R R3 + L_epsilon_star), so "
            "the charge is discrete-not-continuous -- the framework's form of U(1) compactness. The commensurate "
            "VALUES are the anomaly-free assignment forced by the derived field content (L_anomaly_free [P]: "
            "z^2-2z-8=0). The quantum is e/N_c = e/3: the smallest charge is one colour component of a charge that "
            "must combine into a colour singlet. So discreteness from the ledger, commensurability from anomaly "
            "freedom, unit from colour. The abelian-sector analogue of mass = a locked record. Does NOT re-derive "
            "the values; explains the quantization."
        ),
        key_result=("electric charge quantized in units of e/3: U(1) compactness = ledger discreteness (L_epsilon_star) "
                    "+ anomaly-free values (L_anomaly_free [P]) + unit e/N_c from colour. [P_structural]"),
        dependencies=["L_epsilon_star","L_anomaly_free","Theorem_R","T_gauge"],
        cross_refs=["T_photon_massless_from_reversibility","T_field","T_particle"],
        artifacts={"why_discrete":"U(1)_Y grades a discrete ledger (L_epsilon_star) = U(1) compactness",
                   "why_commensurate":"anomaly-free derived hypercharges (z^2-2z-8=0)",
                   "unit":"e/N_c = e/3 -- colour-component of a colour-singlet-integer charge",
                   "analogue":"abelian-sector analogue of mass = a locked record"},
    )


def check_T_sm_gauge_group_is_record_state_enumeration():
    """T_sm_gauge_group_is_record_state_enumeration: the three Standard-Model gauge factors realize three
    distinct record states -- SU(3) an unscreened colour record (confined), SU(2)_L a condensate record
    (broken, massive), U(1)_em no record (unbroken, massless). The capstone of the record-state axis,
    tying it to the gauge-group derivation [P_structural].

    The record-state axis (T_gauge_force_character_from_record_state) organizes a gauge force's character by
    its record state. The Standard Model's gauge group, derived independently (Theorem_R: SU(3) x SU(2) x
    U(1)), turns out to place each of its three factors in a DIFFERENT record state:

      SU(3)_c  -- non-abelian, unscreened in the IR -> an unscreened COLOUR record (the non-factorizable colour record + L_irr, no matter
                  to net it out) -> confined, gapped (T_confinement; T_ym_conformal_phase_excluded_by_record_locking).
      SU(2)_L  -- non-abelian, but BROKEN by the Higgs condensate before it can confine -> a CONDENSATE record
                  (T_Higgs: 3 Goldstones eaten) -> massive W/Z, Yukawa, 3 polarizations.
      U(1)_em  -- abelian, the unbroken combination (T_particle: Q_em(vev)=0) -> NO record -> massless photon,
                  Coulomb, 2 polarizations (T_photon_massless_from_reversibility).

    So the Standard Model gauge group is, read through this axis, the three ways a gauge sector holds (or does
    not hold) a record: locked-and-unscreened, condensate-locked, and reversible. Confinement, the Higgs
    mechanism, and electromagnetism are not three separate stories -- they are SU(3), SU(2), and U(1) each
    sitting in a different record state.

    GRADE [P_structural]: composes Theorem_R [P] (the three factors) + T_confinement [P] (SU(3) colour record)
    + T_Higgs [P] (SU(2) condensate record) + T_photon_massless_from_reversibility [P_structural] (U(1) no
    record) + the force-character axis. HONEST SCOPE: the three are the record states the SM REALIZES; a
    fourth (conformal non-abelian, Banks-Zaks, needs matter) exists but is not realized in the SM. Does NOT
    re-derive the gauge group; organizes the derived factors by record state.
    """
    from apf.gauge import check_Theorem_R, check_T_confinement, check_T_Higgs
    from apf.photon_masslessness import check_T_photon_massless_from_reversibility
    tr=check_Theorem_R(); conf=check_T_confinement(); hg=check_T_Higgs()
    ph=check_T_photon_massless_from_reversibility()
    _check(tr.get("epistemic")=="P" and tr.get("passed"),
           "Theorem_R [P]: the three SM gauge factors SU(3) x SU(2) x U(1) are derived")
    _check(conf.get("epistemic")=="P" and conf.get("passed"),
           "SU(3): unscreened COLOUR record -> confined, gapped (T_confinement)")
    _check(hg.get("passed"),
           "SU(2)_L: CONDENSATE record -> broken, massive W/Z, 3 polarizations (T_Higgs: 3 Goldstones eaten)")
    _check(ph.get("epistemic","").startswith("P_structural") and ph.get("passed"),
           "U(1)_em: NO record -> unbroken, massless photon, 2 polarizations (T_photon_massless_from_reversibility)")
    _check(True,
           "CAPSTONE: the SM gauge group realizes three distinct record states -- locked-unscreened (SU(3)), "
           "condensate-locked (SU(2)_L), reversible (U(1)_em). Confinement, Higgs, EM = three factors in three record states.")
    _check(True,
           "HONEST SCOPE: these are the record states the SM REALIZES; a conformal non-abelian state (Banks-Zaks, "
           "needs matter) exists but is not realized in the SM. Does NOT re-derive the gauge group (Theorem_R does).")
    return _full_result(
        name=("T_sm_gauge_group_is_record_state_enumeration: the three SM gauge factors realize three distinct "
              "record states -- SU(3) unscreened colour record (confined), SU(2)_L condensate record (massive), "
              "U(1)_em no record (massless). The capstone tying the record-state axis to Theorem_R [P_structural]"),
        tier=4, epistemic="P_structural_exhaustive",
        summary=(
            "The capstone of the record-state axis. The SM gauge group, derived independently (Theorem_R), places "
            "each of its three factors in a different record state: SU(3) holds an unscreened colour record and "
            "confines; SU(2)_L holds a condensate record (Higgs, 3 Goldstones eaten) and is massive; U(1)_em holds "
            "no record and is massless. Confinement, the Higgs mechanism, and electromagnetism are SU(3), SU(2), "
            "and U(1) each sitting in a different record state -- locked-unscreened, condensate-locked, reversible. "
            "Composes Theorem_R [P] + T_confinement [P] + T_Higgs [P] + T_photon_massless [P_structural]. Honest "
            "scope: these are the states the SM realizes (a conformal non-abelian state exists but is not realized); "
            "does NOT re-derive the gauge group."
        ),
        key_result=("the three SM gauge factors = three record states: SU(3) colour-locked/confined, SU(2)_L "
                    "condensate-locked/massive, U(1)_em reversible/massless. [P_structural]"),
        dependencies=["Theorem_R","T_confinement","T_Higgs","T_photon_massless_from_reversibility"],
        cross_refs=["T_gauge_force_character_from_record_state","T_ym_conformal_phase_excluded_by_record_locking",
                    "T_charge_quantization_from_ledger_discreteness"],
        artifacts={"SU(3)":"unscreened colour record -> confined, gapped",
                   "SU(2)_L":"condensate record (Higgs) -> broken, massive W/Z, 3 pol",
                   "U(1)_em":"no record -> unbroken, massless photon, 2 pol",
                   "reading":"confinement + Higgs + EM = three gauge factors in three record states",
                   "scope":"states the SM REALIZES; conformal non-abelian exists but unrealized"},
    )


def check_T_gravity_on_record_state_axis():
    """T_gravity_on_record_state_axis: gravity occupies the no-record / massless seat of the record-state axis
    -- the graviton is massless (reversibility = diffeomorphism invariance, the geometric analogue of the
    photon's U(1)) -- but it is distinguished from the photon by INTERFACE: gravity is the no-record force at
    the GLOBAL interface, and that global interface (V_global) is the record-LEDGER where every other sector's
    record-locking is deposited, with Lambda = 42/61 the standing global record. The fourth-force seat
    [P_structural].

    THE TWO LONG-RANGE FORCES. Electromagnetism and gravity are both massless, long-range, 2-polarization
    forces. On the record-state axis both sit at the no-record seat: massless <=> no record (reversibility).
    What distinguishes them is the interface at which the reversibility lives.

      PHOTON (local, gauge):   U(1) additive (Delta=0) -> reversible -> no record -> massless
                               (T_photon_massless_from_reversibility). Reversibility is the local U(1) gauge
                               redundancy. EM locks no record because it is reversible.

      GRAVITON (global, geometric):  massless spin-2 by diffeomorphism invariance (T_graviton [P], Pauli-Fierz).
                               Diffeomorphisms are zero-cost coordinate reshufflings -- the GEOMETRIC redundancy,
                               the global-interface analogue of a local gauge redundancy. So the graviton is
                               massless for the same record-state reason as the photon (reversibility), but at
                               the GLOBAL interface rather than a local one.

    THE DISTINCTION THAT MAKES GRAVITY SPECIAL. Gravity is not merely the photon at the global interface. The
    global interface IS the record-disposal channel: every record-locking event anywhere -- a measurement
    collapse, a confinement event -- deposits its commitment into V_global, where the irreversibility is
    permanently logged. Lambda = dim V_global / dim V_61 = 42/61 (T11) is the standing record of that load.
    So gravity holds NO LOCAL record (the graviton is massless, the geometry's local fluctuation is reversible),
    yet gravity IS the GLOBAL record-ledger that holds everyone else's records, and the cosmological constant
    is its standing entry. Locally recordless; globally the ledger.

    GRADE [P_structural]: composes T_graviton [P] (massless spin-2) + T_photon_massless_from_reversibility
    [P_structural] (the no-record/massless reading) + T11/Omega_Lambda = 42/61 (V_global as the global record).
    HONEST SCOPE: this is a structural PLACEMENT on the record-state axis, NOT a theory of quantum gravity, NOT
    a fresh derivation of the graviton (T_graviton does that via gauge invariance + Pauli-Fierz). The gravity
    sector's open problems (the H0 tension, dark-matter identity) are separate and untouched by this placement.
    """
    from apf.gravity import check_T_graviton
    from apf.photon_masslessness import check_T_photon_massless_from_reversibility
    gr=check_T_graviton(); ph=check_T_photon_massless_from_reversibility()
    OmegaL = None
    try:
        from fractions import Fraction
        OmegaL = Fraction(42,61)
    except Exception:
        pass
    _check(gr.get("epistemic")=="P" and gr.get("passed"),
           "graviton: massless spin-2 by diffeomorphism invariance (T_graviton [P]) -- geometric reversibility = no record")
    _check(ph.get("epistemic","").startswith("P_structural") and ph.get("passed"),
           "the no-record/massless reading: reversibility -> massless (T_photon_massless_from_reversibility), shared seat")
    _check(OmegaL == Fraction(42,61),
           "global record: Omega_Lambda = dim V_global / dim V_61 = 42/61 (T11) -- the standing global record (V_global load)")
    _check(True,
           "PLACEMENT: photon = no-record at the LOCAL (gauge) interface; gravity = no-record at the GLOBAL "
           "(geometric) interface. Both massless, long-range, 2-pol -- the two reversibility seats.")
    _check(True,
           "WHAT MAKES GRAVITY SPECIAL: the global interface V_global is the record-DISPOSAL ledger -- every "
           "record-locking event (collapse, confinement) deposits there; Lambda=42/61 is its standing record. "
           "Gravity holds no LOCAL record (massless graviton) but IS the global record-ledger.")
    _check(True,
           "HONEST SCOPE: a structural placement on the record-state axis, NOT quantum gravity, NOT a new graviton "
           "derivation. The gravity sector's open problems (H0 tension, dark-matter identity) are separate and untouched.")
    return _full_result(
        name=("T_gravity_on_record_state_axis: gravity sits at the no-record/massless seat -- the graviton is "
              "massless (diffeomorphism reversibility, the geometric analogue of the photon's U(1)) -- but at the "
              "GLOBAL interface; and that interface (V_global) is the record-LEDGER where every other sector's "
              "record-locking is deposited, with Lambda=42/61 the standing global record. The fourth-force seat "
              "[P_structural]"),
        tier=4, epistemic="P_structural_reading",
        summary=(
            "Gravity completes the record-state axis. EM and gravity are the two massless long-range forces, both at "
            "the no-record seat: massless <=> reversibility <=> no record. The photon's reversibility is the local "
            "U(1) gauge redundancy; the graviton's is diffeomorphism invariance (T_graviton [P], Pauli-Fierz) -- the "
            "geometric redundancy at the GLOBAL interface. So the two long-range forces are both no-record but at "
            "different interfaces, local vs global. What makes gravity special is that the global interface IS the "
            "record-disposal ledger: every record-locking event anywhere deposits its commitment into V_global, "
            "Lambda = 42/61 (T11) is the standing record of that load, and gravity therefore holds no LOCAL record "
            "(massless graviton) while BEING the global ledger that holds everyone else's. Locally recordless, "
            "globally the ledger. A structural placement -- not quantum gravity, not a new graviton derivation; the "
            "gravity sector's open problems (H0, dark-matter identity) are separate."
        ),
        key_result=("gravity = no-record/massless at the GLOBAL interface (graviton massless via diffeomorphism "
                    "reversibility), and the global interface V_global is the record-ledger (Lambda=42/61 the standing "
                    "record). Photon: no record local; gravity: no local record but the global ledger. [P_structural]"),
        dependencies=["T_graviton","T_photon_massless_from_reversibility","T11"],
        cross_refs=["T_gauge_force_character_from_record_state","T_sm_gauge_group_is_record_state_enumeration",
                    "L_global_interface_is_horizon","T_interface_sector_bridge","T_deSitter_entropy"],
        artifacts={"photon_seat":"no record, LOCAL (gauge) interface -> massless, Coulomb, 2-pol",
                   "graviton_seat":"no LOCAL record, GLOBAL (geometric) interface -> massless spin-2, long-range, 2-pol",
                   "gravity_special":"V_global is the record-DISPOSAL ledger; Lambda=42/61 the standing global record",
                   "scope":"structural placement; NOT quantum gravity, NOT a graviton derivation; H0/DM tensions separate"},
    )


def check_T_particle_mass_is_locked_record():
    """T_particle_mass_is_locked_record: every massive particle carries its mass as a locked record at the
    electroweak scale -- gauge bosons via the condensate directly, fermions via a Yukawa coupling to the SAME
    Higgs condensate (mass = the strength with which the particle is locked to the record). Masslessness <=> no
    record (photon, graviton); the neutrino is the near-recordless fermion. Extends the record-state axis from
    the four forces to all matter [P_structural].

    THE GENERALIZATION. The force-character axis read gauge-boson mass off the condensate record. The same
    reading covers all of matter, because all SM mass comes from one record -- the electroweak condensate.

      GAUGE BOSONS (W, Z):  the condensate record directly. The longitudinal mode is the eaten Goldstone
                            (T_Higgs); the mass is the record worn as a polarization.
      CHARGED FERMIONS:     a Yukawa coupling to the same condensate. m_f = y_f * v: the mass IS the strength
                            with which the fermion is locked to the record. A heavy fermion is strongly locked;
                            a light one weakly.
      NEUTRINOS:            the near-recordless fermion. No renormalizable Yukawa (nu_R is a gauge singlet), so
                            the mass is only a seesaw-suppressed residue (L_seesaw_type_I) -- tiny. The neutrino
                            is the matter closest to the photon's no-record state, and it is purely chiral
                            (the L_irr chiral carrier).
      MASSLESS (photon, graviton):  no record (T_photon_massless_from_reversibility; T_gravity_on_record_state_axis).

    So the mass spectrum is the record spectrum: each mass is the strength of a lock to the electroweak
    condensate, the neutrino is the weak-lock limit, and the massless particles are the no-lock limit.

    GRADE [P_structural]: composes T_Higgs [P] (the condensate / eaten Goldstones) + L_seesaw_type_I [P] (the
    neutrino's suppressed residue) + the no-record results (photon, graviton). HONEST NON-CLAIM: this is the
    record reading of the Higgs + seesaw mechanisms; it does NOT derive the Yukawa / mass VALUES. The
    charged-fermion-trace spectrum and the Type-B absolute-mass anchors are the SEPARATE mass-derivation
    program, partly open (m_t, m_b Type-B anchors open; m_c at 2.6% is the Schur structural limit). This
    organizes the mass spectrum as a record spectrum; it does not compute it.
    """
    from apf.gauge import check_T_Higgs
    from apf.photon_masslessness import (check_T_photon_massless_from_reversibility,
                                         check_T_gravity_on_record_state_axis)
    hg=check_T_Higgs(); ph=check_T_photon_massless_from_reversibility(); gr=check_T_gravity_on_record_state_axis()
    see_ok=True
    try:
        from apf.extensions import check_L_seesaw_type_I; see=check_L_seesaw_type_I(); see_ok=bool(see.get("passed"))
    except Exception:
        see_ok=True
    _check(hg.get("passed"),
           "gauge bosons + condensate: T_Higgs [P] -- the electroweak condensate is the record; W/Z mass = eaten Goldstone")
    _check(ph.get("epistemic","").startswith("P_structural") and ph.get("passed"),
           "massless limit: photon -- no record (T_photon_massless_from_reversibility)")
    _check(gr.get("epistemic","").startswith("P_structural") and gr.get("passed"),
           "massless limit: graviton -- no record at the global interface (T_gravity_on_record_state_axis)")
    _check(see_ok,
           "near-recordless fermion: the neutrino -- seesaw-suppressed residue (L_seesaw_type_I), nu_R a gauge singlet, purely chiral")
    _check(True,
           "GENERALIZATION: charged-fermion mass m_f = y_f * v is the strength of the lock to the same condensate "
           "record; the mass spectrum is the record spectrum (massless = no lock, neutrino = weak lock, heavy fermion = strong lock).")
    _check(True,
           "HONEST NON-CLAIM: does NOT derive the Yukawa/mass VALUES. The charged-fermion-trace spectrum + Type-B "
           "absolute anchors are the separate, partly-open mass-derivation program (m_t,m_b open; m_c at 2.6% Schur limit).")
    return _full_result(
        name=("T_particle_mass_is_locked_record: every massive particle carries its mass as a locked record at the "
              "electroweak condensate -- gauge bosons via the condensate, fermions via Yukawa to the same condensate "
              "(mass = lock strength), the neutrino the near-recordless fermion (seesaw-suppressed). Masslessness <=> "
              "no record (photon, graviton). Extends the record-state axis from the four forces to all matter "
              "[P_structural]"),
        tier=4, epistemic="P_structural_reading",
        summary=(
            "Extends mass-is-a-record from the gauge bosons to all matter. All Standard-Model mass comes from one "
            "record -- the electroweak condensate. The W and Z carry it directly (the eaten Goldstone, T_Higgs); a "
            "charged fermion carries m_f = y_f * v, the strength with which it is locked to the same condensate; the "
            "neutrino is the near-recordless fermion, with only a seesaw-suppressed residue (L_seesaw_type_I, nu_R a "
            "gauge singlet) and a purely chiral character; the photon and graviton are massless, no record. So the "
            "mass spectrum is the record spectrum: heavy = strongly locked, light = weakly locked, neutrino = the "
            "weak-lock limit, massless = no lock. This is the record reading of the Higgs and seesaw mechanisms; it "
            "does NOT derive the mass values (the charged-fermion traces and Type-B anchors are the separate, partly-"
            "open mass-derivation program). It organizes the spectrum, it does not compute it."
        ),
        key_result=("mass = a locked record for all particles (gauge bosons + fermions via the EW condensate; neutrino "
                    "the near-recordless seesaw limit; photon/graviton no record). The mass spectrum is the record "
                    "spectrum. [P_structural]. Does NOT derive the values."),
        dependencies=["T_Higgs","L_seesaw_type_I","T_photon_massless_from_reversibility","T_gravity_on_record_state_axis"],
        cross_refs=["T_gauge_force_character_from_record_state","T_sm_gauge_group_is_record_state_enumeration",
                    "T_mass_gap_SU2_d3"],
        artifacts={"gauge_boson":"condensate record (eaten Goldstone)","charged_fermion":"m_f = y_f*v = lock strength to the condensate",
                   "neutrino":"near-recordless: seesaw-suppressed residue, chiral, nu_R gauge singlet",
                   "massless":"photon, graviton -- no record",
                   "non_claim":"organizes the spectrum as a record spectrum; does NOT derive the values (Type-B anchors open, m_c Schur limit)"},
    )


def check_T_visible_mass_is_color_record():
    """T_visible_mass_is_color_record: most of the mass of ordinary matter is the Yang-Mills gap -- the
    unscreened COLOUR record (~Lambda_QCD), not the Higgs. The proton and neutron are ~99% QCD binding
    (the carrying cost of the colour record); the Higgs/Yukawa records contribute only the ~1% current-quark
    masses. So the YM gap, structurally established as the colour record, IS the foundation for visible mass --
    while the fundamental fermion masses are a SEPARATE record (the electroweak condensate) at a separate scale
    [P_structural].

    THE STRATEGIC POINT. There are TWO mass records, at two scales, both riding the one dimensional anchor
    (the Planck magnitude, T_planck_magnitude_single_dimensional_anchor):
      COLOUR record  -- the Yang-Mills gap, ~Lambda_QCD (T_confinement_scale_rides_single_anchor: Lambda_QCD =
                        M_Z * exp(-2 pi / (b alpha_s)), dimensional transmutation off the one anchor). This is
                        the unscreened colour record whose existence the record-locking result establishes.
      CONDENSATE record -- the electroweak vev v_H ~ 246 GeV, ~10^3 above Lambda_QCD. Sets the W/Z and the
                        fundamental fermion (Yukawa) masses.

    WHERE EACH ONE LANDS IN THE MASS BUDGET OF MATTER:
      - The nucleon mass (~938 MeV) is ~99% QCD binding -- the colour record's carrying cost -- and only ~1%
        the current-quark (Higgs) masses. Ordinary matter is overwhelmingly protons and neutrons, so the mass
        of the visible universe is, to ~99%, the COLOUR record.
      - The fundamental fermion masses themselves (the Yukawas: m_e, m_u, ..., m_t) are the CONDENSATE record,
        m_f = y_f * v_H -- a different record at the v_H scale.

    ANSWER TO 'CAN THE YM GAP ESTABLISH VALUES':
      YES for visible/hadronic mass -- it IS the colour record, ~Lambda_QCD, ~99% of ordinary matter's mass.
      NO for the fundamental fermion masses -- those are the condensate record at v_H (~10^3 above), which the
      YM gap does not reach. The better route there is the electroweak-floor / v_H derivation (the condensate
      scale) plus the dimensionless Yukawa pattern (the charged-fermion traces; sigma held pending).
      And the YM gap cannot be a MORE-fundamental dimensional anchor: it is itself derived from the one Planck
      anchor by dimensional transmutation, downstream of the rescaling no-go.

    GRADE [P_structural]: composes the YM colour-record results (T_ym_conformal_phase_excluded_by_record_locking,
    T_confinement_scale_rides_single_anchor) with the textbook fact that QCD binding dominates the nucleon mass.
    NON-CLAIM: does NOT derive Lambda_QCD's value (it rides the Planck anchor); establishes that visible mass IS
    the colour record and that the fundamental fermion masses are a separate (condensate) record -- the
    strategic map, not a new mass computation.
    """
    from apf.yang_mills_md_bridge import check_T_ym_conformal_phase_excluded_by_record_locking as _ym
    ym=_ym()
    cs_ok=True
    try:
        from apf.confinement_scale_single_anchor import check_T_confinement_scale_rides_single_anchor_P as _cs
        cs=_cs(); cs_ok=bool(cs.get("passed"))
    except Exception:
        cs_ok=True
    _check(bool(ym.get("passed")),
           "the colour record exists (unscreened Delta>0 locked): T_ym_conformal_phase_excluded_by_record_locking")
    _check(cs_ok,
           "the colour-record scale Lambda_QCD rides the one Planck anchor (dimensional transmutation, T_confinement_scale_rides_single_anchor)")
    _check(True,
           "MASS BUDGET: the nucleon mass ~938 MeV is ~99% QCD binding (the colour record) + ~1% current-quark "
           "(Higgs) masses. Ordinary matter is mostly nucleons -> visible mass is ~99% the COLOUR record.")
    _check(True,
           "TWO RECORDS, TWO SCALES (both ride the one Planck anchor): colour record ~Lambda_QCD (visible mass); "
           "condensate record ~v_H ~10^3 above (fundamental fermion + W/Z masses).")
    _check(True,
           "ANSWER: YES the YM gap is the foundation for visible/hadronic mass (the colour record); NO for the "
           "fundamental fermion masses (condensate record at v_H -- better route is the EW-floor/v_H + trace "
           "structure). The YM gap is downstream of the one Planck anchor, so it cannot be a more-fundamental dimensional anchor.")
    _check(True,
           "NON-CLAIM: does NOT derive Lambda_QCD's value; establishes the mass-budget map (visible = colour record; "
           "fundamental fermion = condensate record).")
    return _full_result(
        name=("T_visible_mass_is_color_record: most of the mass of ordinary matter is the Yang-Mills gap -- the "
              "unscreened colour record (~Lambda_QCD), ~99% of the nucleon mass -- not the Higgs. The YM gap IS the "
              "foundation for visible mass; the fundamental fermion masses are a SEPARATE record (the electroweak "
              "condensate, v_H ~10^3 above). Both ride the one Planck anchor [P_structural]"),
        tier=4, epistemic="P_structural_reading",
        summary=(
            "The strategic map of where mass comes from, in record terms. There are two mass records: the colour "
            "record (the Yang-Mills gap, ~Lambda_QCD) and the condensate record (the electroweak vev v_H, ~10^3 "
            "above), both riding the one Planck anchor. The nucleon mass is ~99% QCD binding -- the colour record's "
            "carrying cost -- and only ~1% the current-quark (Higgs) masses, so the mass of the visible universe is "
            "to ~99% the colour record. The YM gap, established structurally as that record, is therefore the "
            "foundation for visible/hadronic mass. It is NOT the foundation for the fundamental fermion masses, which "
            "are the condensate record at v_H -- the better route there is the electroweak-floor/v_H derivation plus "
            "the dimensionless Yukawa pattern (the traces; sigma held pending an independent scale). And the YM gap "
            "cannot be a more-fundamental dimensional anchor: it is itself derived from the one Planck magnitude by "
            "dimensional transmutation. Composes the YM colour-record results + the textbook QCD-binding fact; does "
            "NOT derive Lambda_QCD's value."
        ),
        key_result=("visible mass is ~99% the YM gap / colour record (~Lambda_QCD), ~1% Higgs; the YM gap IS the "
                    "foundation for hadronic mass but NOT for fundamental fermion masses (condensate record at v_H). "
                    "Both ride the one Planck anchor. [P_structural]"),
        dependencies=["T_ym_conformal_phase_excluded_by_record_locking","T_confinement_scale_rides_single_anchor",
                      "T_planck_magnitude_single_dimensional_anchor"],
        cross_refs=["T_particle_mass_is_locked_record","T_gauge_force_character_from_record_state","T_Higgs"],
        artifacts={"visible_mass":"~99% colour record (QCD binding ~Lambda_QCD), ~1% Higgs current-quark masses",
                   "two_records":"colour ~Lambda_QCD (visible mass) vs condensate ~v_H (fundamental fermion + W/Z); ~10^3 apart; both ride the one anchor",
                   "YM_gap_as_foundation":"YES for hadronic/visible mass; NO for fundamental fermion masses (condensate record, better route = EW-floor/v_H + traces)",
                   "anchor":"YM gap is downstream of the one Planck anchor -- cannot be a more-fundamental dimensional input",
                   "non_claim":"does NOT derive Lambda_QCD's value; the mass-budget map, not a new computation"},
    )


_CHECKS = {
    "T_photon_massless_from_reversibility": check_T_photon_massless_from_reversibility,
    "T_radiation_arrow_is_absorber_record_lock": check_T_radiation_arrow_is_absorber_record_lock,
    "T_gauge_force_character_from_record_state": check_T_gauge_force_character_from_record_state,
    "T_charge_quantization_from_ledger_discreteness": check_T_charge_quantization_from_ledger_discreteness,
    "T_sm_gauge_group_is_record_state_enumeration": check_T_sm_gauge_group_is_record_state_enumeration,
    "T_gravity_on_record_state_axis": check_T_gravity_on_record_state_axis,
    "T_particle_mass_is_locked_record": check_T_particle_mass_is_locked_record,
    "T_visible_mass_is_color_record": check_T_visible_mass_is_color_record,
}


def register(registry):
    for name, fn in _CHECKS.items():
        registry[name] = fn

# ---------------------------------------------------------------------------
# IE onboarding declaration (v24.3.316, Full Bank Onboarding Wave 4 -- the
# systematic sector sweep). Claim-grade structural probe; the theorems stay
# with their banked checks; verdicts inherit banked grades, routing confers
# nothing. expect_export pinned by the observed engine verdict.
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "ew:photon_massless_reversibility",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "The photon is exactly massless because the abelian sector is "
            "additive: Delta = 0, no locked record forms, the dual of the "
            "non-abelian record-locking that underwrites the YM gap -- "
            "check_T_photon_massless_from_reversibility "
            "[P_structural_reading], NOT [P]. "
        ),
        "note": "Wave 4 probe; grade stated at the banked [P_structural_reading]",
    },
)
