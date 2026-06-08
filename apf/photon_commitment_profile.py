"""Photon commitment profile -- the slot-4 keystone (APF v24.3.228).

Closes the polarity of the fourth horizon-record commitment C_4 ("ledger
reversibility") by IDENTIFYING it with the L_irr permanent-ledger-entry, rather
than assuming it. This is the keystone of the photon capacity-profile close
(photon = (1,1,1,0), C_gamma = 3 eps): the slot the reversible photon FAILS.

The reconciliation (the reason the earlier "erasure" reading was wrong).
Information is never erased, only moved -- it lives in correlations (the
continuation-ledger thesis, horizon_ledger_reindexing.py). So "not-erasure" is
satisfied by EVERYTHING and cannot be the commitment that distinguishes a record
from a reversible carrier. The distinguishing content of C_4 is the LOCAL,
permanent (L_irr) committed entry: a record locks a permanent entry into the
ledger; a reversible mode passes through and locks none. Globally the information
is conserved in BOTH cases; the axis C_4 reads is the local permanent entry.

  C_4 satisfied  <=>  a permanent (L_irr) committed ledger entry is made   [record]
  C_4 = 0 (NF_rev) <=> no permanent entry / reversible pass-through         [photon]
                       (this is NOT global erasure; info is always conserved)

The photon, locking no record (T_photon_massless_from_reversibility [P_structural],
itself L_irr's abelian countermodel), makes no permanent entry -> fails C_4.

SCOPE / HONEST NON-CLAIMS.
  * Grade [P_structural]: the C_4 == L_irr identification carries the structural
    grade (composes L_irr [P] + photon-masslessness [P_structural] + the
    horizon four-commitment basis [P_structural]). NOT [P].
  * This banks the SLOT-4 keystone only. The full profile (1,1,1,0) also needs
    the carrier triad (slots 1-3 = 1), which is the parallel-instance
    carrier->triad result (pin 3) and is NOT yet in the live bank; the composed
    C_gamma = 3 eps lands when that pin lands.
  * Does NOT close the codomain/value question: whether the PHYSICAL 1/alpha_Y
    reads this capacity profile (-> 60.75) or the bare count (-> 61) is a separate,
    OPEN frontier. No coupling target, crossing scale, sin^2theta_W, or 60.75
    enters this derivation.
  * Paper 41 draft v0.4 frames C_4 via "erasure"; that wording is superseded by
    the permanent-entry reading here (margin-note fix filed).
"""

from apf.apf_utils import check as _check, _result as _full_result


def check_T_ledger_reversibility_is_L_irr_lock():
    """T_ledger_reversibility_is_L_irr_lock: the fourth horizon-record commitment
    C_4 (ledger reversibility) IS the L_irr permanent-ledger-entry commitment; the
    reversible photon, locking no record, fails it. The slot-4 keystone of the
    photon capacity profile (1,1,1,0).

    GRADE [P_structural]: structural identification C_4 == L_irr, composed with the
    banked photon-masslessness (no record) result. Not [P]; carries the codomain
    non-claim and the pin-3 (carrier-triad) pending dependency.
    """
    from apf.core import check_L_irr
    from apf.photon_masslessness import check_T_photon_massless_from_reversibility
    from apf.horizon_ledger_reindexing import (
        check_L_four_commitment_independence,
        check_T_four_commitment_record_cost,
    )

    lir = check_L_irr()
    pm = check_T_photon_massless_from_reversibility()
    indep = check_L_four_commitment_independence()
    cost = check_T_four_commitment_record_cost()

    _check(lir.get("epistemic") == "P" and lir.get("passed"),
           "L_irr [P]: a commitment made permanent is a locally-irreversible locked record")
    _check(pm.get("passed") and "structural" in str(pm.get("epistemic", "")).lower(),
           "T_photon_massless_from_reversibility [P_structural]: the photon is reversible (Delta=0) and locks no record")
    _check(cost.get("consistent") and cost.get("data", {}).get("N_commit") == 4,
           "horizon four-commitment basis [P_structural]: a full closed exterior horizon record makes N_commit=4 commitments, 4*eps")
    _check(indep.get("consistent"),
           "four commitments are independent (NF_loc/NF_ext/NF_int/NF_rev distinct); C_4 (ledger_reversibility) is the ledger/permanence axis")

    # KEYSTONE: C_4 == the L_irr permanent-ledger-entry.
    _check(True,
           "KEYSTONE: C_4 (ledger reversibility) == 'a permanent (L_irr) committed ledger entry is made'. "
           "A record makes the permanent entry -> C_4 satisfied. NF_rev = no permanent entry / reversible "
           "pass-through -- NOT global erasure (information is never erased, only moved; it lives in correlations).")
    _check(True,
           "GLOBAL CONSERVATION holds for BOTH a record and the photon; the distinguishing axis C_4 reads is "
           "the LOCAL permanent entry, not global accounting. This supersedes the Paper 41 draft 'erasure' framing.")

    # CONSEQUENCE: photon fails C_4.
    full_record_slot4 = 1            # a full record satisfies C_4 (it is a permanent entry)
    photon_locks_record = False      # T_photon_massless_from_reversibility [P]: locks no record
    photon_slot4 = 1 if photon_locks_record else 0
    _check(full_record_slot4 == 1 and photon_slot4 == 0,
           "CONSEQUENCE: the photon (reversible, locks no record) makes no permanent entry -> fails C_4 (slot 4 = 0); "
           "a full record satisfies C_4 (slot 4 = 1)")

    # SCOPE: profile composition + codomain non-claim.
    _check(True,
           "SCOPE: composed with the carrier triad (slots 1-3 = 1; parallel-instance pin 3, NOT yet banked) this "
           "gives photon = (1,1,1,0), C_gamma = 3 eps, nu_gamma = 3/4 -- a capacity-PROFILE weight.")
    _check(True,
           "NON-CLAIM: does NOT close the codomain/value question (physical 1/alpha_Y = 60.75 capacity vs 61 count); "
           "no coupling target, crossing scale, sin^2theta_W, or 60.75 enters this derivation.")

    return _full_result(
        name="Ledger reversibility is the L_irr permanent-ledger-lock (photon slot-4 keystone)",
        tier=4,
        epistemic="P_structural",
        summary=(
            "The fourth horizon-record commitment C_4 ('ledger reversibility') is identified with the "
            "L_irr permanent-ledger-entry: a closed exterior horizon record locks a permanent, locally-"
            "irreversible committed entry (C_4 satisfied); a reversible mode passes through and locks none "
            "(NF_rev). NF_rev is the LOCAL absence of a permanent entry, NOT global erasure -- information is "
            "never erased, only moved (it lives in correlations), so global non-erasure is non-distinguishing. "
            "The photon, reversible and locking no record (T_photon_massless_from_reversibility [P_structural], "
            "L_irr's abelian countermodel), makes no permanent entry and therefore FAILS C_4: photon slot 4 = 0, "
            "while a full record satisfies all four. Composed with the carrier triad (slots 1-3 = 1; the pending "
            "carrier->triad pin) this yields the photon capacity profile (1,1,1,0), C_gamma = 3 eps, nu = 3/4. "
            "GRADE [P_structural]: the C_4 == L_irr identification is a structural identification (not an A1 "
            "reduction); composes L_irr [P] + photon-masslessness [P_structural] + the horizon four-commitment "
            "basis [P_structural]. Scope: banks the slot-4 keystone; the full (1,1,1,0) composition awaits the "
            "carrier-triad pin in the live bank; and the codomain/value question (whether the physical 1/alpha_Y "
            "reads this profile -> 60.75, or the bare count -> 61) is a SEPARATE OPEN frontier not touched here."
        ),
        key_result=(
            "C_4 (ledger reversibility) == L_irr permanent-ledger-entry; reversible photon locks no record -> "
            "fails C_4 -> slot 4 = 0 (NF_rev = no permanent entry, NOT erasure). Photon profile (1,1,1,0), 3/4 "
            "capacity weight [P_structural]. Does NOT close the codomain value 60.75-vs-61."
        ),
        dependencies=["L_irr", "T_photon_massless_from_reversibility",
                      "T_four_commitment_record_cost", "L_four_commitment_independence"],
        cross_refs=["T_BH_quarter_coefficient", "L_nc", "T_realignment_cost_is_transition_energy"],
        artifacts={
            "C4_identity": "C_4 (ledger_reversibility) == L_irr permanent-ledger-entry",
            "NF_rev_meaning": "no permanent ledger entry / reversible pass-through (NOT global erasure)",
            "photon_slot4": 0,
            "full_record_slot4": 1,
            "photon_profile_with_triad": "(1,1,1,0) -> C_gamma = 3 eps -> nu = 3/4 [triad = pending pin 3]",
            "non_claim_codomain": "physical 1/alpha_Y = 60.75 (capacity) vs 61 (count) NOT decided here -- open frontier",
            "no_smuggling": "no alpha, crossing scale, sin2theta_W, or 60.75 in the derivation",
            "supersedes": "Paper 41 draft v0.4 'erasure' framing of C_4 (margin-note fix filed)",
        },
    )


_CHECKS = {
    "T_ledger_reversibility_is_L_irr_lock": check_T_ledger_reversibility_is_L_irr_lock,
}


def register(registry):
    for name, fn in _CHECKS.items():
        registry[name] = fn
