"""Separately stored gate inventories for :mod:`apf.hfc_345_closure`.

Split from the consuming module deliberately (cold-audit MAJOR-1; pattern:
the v24.3.429 ``_held_holonomy_contract.py`` and the fortified two-exchange
packet's ``two_exchange_roots.py``): the gate-contract check compares the live
executable graph against this module, so a coordinated silent deletion must
now touch two files to pass.

Ruling 3 of record (2026-07-20 seam-closure rulings):

    LOCAL_J + NATURALITY + ORIENTATION_SYNCHRONIZATION
        + GENERATOR_COMPLETENESS  =>  CENTRAL_J,

never less.  The audited M6 mutation (delete ``GENERATOR_COMPLETENESS`` from
``T_CENTRAL_J``) passed 10/10 checks in the pre-fortification packet; with
this inventory stored here and pinned set-exactly in
``check_T_central_j_gate_contract``, that mutation fails a check and a test.
"""

CENTRAL_J_REQUIRED_GATES = (
    "GENERATOR_COMPLETENESS",
    "NATURALITY",
    "ORIENTATION_SYNCHRONIZATION",
    "T_LOCAL_J",
)


# Bank-landing embed (v24.3.432): the physical leaf manifest, verbatim from the
# fortified packet's DATA/physical_leaf_manifest.json (provenance: the packet copy
# in Artifacts_2026-07-20_session/holonomy_gate_intake/). The packet ships the
# JSON file; the bank copy embeds it so the module is file-dependency-free.
LEAF_MANIFEST = {'schema_version': '0.4', 'claim': 'local_J_from_live_345_hfc_two_exchange_package', 'leaves': {'LIVE_345_HELD_FAIR_COMMONING': {'type': 'physical', 'description': 'For the exact candidate ports a=u+v and b=u-v on the live active carrier, the interface admits one equal unresolved binary Held competition and realizes pi_W|act as its contender-blind commoning without crossing into record, export, overwrite, or nullity.', 'clauses': ['port admission: a=u+v and b=u-v are admitted live candidate ports', 'equal competition: the ports form one equal unresolved binary Held competition', 'commoning identification: pi_W|act is realized as their contender-blind Held commoning', 'no boundary crossing: no crossing into record, export, overwrite, or nullity'], 'certification_note': 'bundled leaf: certification must address each clause; a certificate silent on any clause fails the charter'}, 'COMPLETE_HELD_PROFILE': {'type': 'structural', 'description': 'Future-consequential source distinctions cannot silently disappear from a complete Held carrier.'}, 'A2_NO_WASTE_MINIMUM': {'type': 'structural', 'description': 'Continuation-null implementation excess is removed while consequential relative-kernel rank is retained.'}, 'FINITE_COMPATIBLE_JOINT_REALIZATION': {'type': 'physical', 'description': 'Visible and residual factors occur in one compatible minimum carrier.'}, 'FACTOR_ISOLATION_NEUTRAL_COMPLETION': {'type': 'physical', 'description': 'Common and defect factors can be isolated record-free with symmetry-neutral completion.', 'clauses': ['factor isolation: common and defect factors can be isolated record-free', 'neutral completion: the isolation completes symmetry-neutrally'], 'certification_note': 'bundled pair: certification must address both clauses'}, 'SAME_TYPE_RETURN': {'type': 'physical', 'description': 'The factorized carrier returns to the same represented Held type.'}, 'EFFECTIVE_BASELINE_BINARY_EXCHANGE': {'type': 'physical', 'description': 'A separately certified baseline common/defect presentation on the same effective carrier carries a reversible record-free contender exchange represented by S_0=diag(1,-1).', 'clauses': ['presentation admission: a baseline common/defect presentation is separately certified', 'same effective carrier: the presentation lives on the same effective carrier', 'exchange effectiveness: the contender exchange is reversible, record-free, and effective (per-exchange recombination witness in the TE L4 sense)'], 'certification_note': 'bundled leaf (TE roots EFFECTIVE_FIRST_CONTENDER_EXCHANGE + its recombination witness + same-carrier clause); certification must address each clause'}, 'LIVE_345_RECORD_FREE_PORT_EXCHANGE': {'type': 'physical', 'description': 'The admitted live candidate ports a=u+v and b=u-v are interchanged by a reversible record-free physical continuation with a typed inverse and same-carrier return.'}, 'EXACT_345_DEFENDER_GEOMETRY': {'type': 'structural', 'description': 'The live active projector has exact range u=(3/5,4/5) and kernel v=(-4/5,3/5).'}, 'NEUTRAL_E2_COMPLETION': {'type': 'physical', 'description': 'The invariant e2 factor is held fixed as a neutral spectator while the active e1/e3 carrier is used.'}, 'FUTURE_CONSEQUENTIAL_DEFECT': {'type': 'physical', 'description': 'The retained live defect sign is distinguished by at least one later admissible completion, so the transported exchange survives the complete operational quotient.'}, 'ZIPPER_REVERSAL_IS_INVERSE': {'type': 'physical', 'description': "The reversed record-free zipper path is represented by the exact inverse F_345^{-1}, so the transport S_u = F_345 P F_345^{-1} is the represented action of a physical loop. Reversal admission alone yields only a monoid. This is the TE-fortification root INTERTWINER_REVERSAL_IS_INVERSE (the .429 H1-genre gate), restored at the zipper locus after the cold audit found it silently dropped (MAJOR-2); the 'typed inverse' clause of LIVE_345_RECORD_FREE_PORT_EXCHANGE attaches to the port swap and does not cover the zipper."}, 'EXCHANGE_CARGO_NATURALITY': {'type': 'physical', 'description': 'The represented action of admitted record-free continuations on Held cargo is linear (exchange/cargo-natural) on the admitted presentations, so conjugation through the zipper is the represented action of the physical port exchange. This is the TE-fortification root UNIVERSAL_EXCHANGE_NATURALITY_ON_ADMITTED_PRESENTATIONS, restored after the cold audit found it dropped everywhere in the local route (MAJOR-2). The banked affine_cargo_naturality leg of continuation_tesseract_bridge.HOC_PACKAGE is the fallback-route consumer: the alternate direct reading (a physical continuation swapping the ports determines S_u uniquely) requires exactly this linearity of the represented action.'}}, 'forbidden_substitutions': ['ACTIVE_345_PLANE_IS_PAPER10_FIRST_JET', 'PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY', 'QUADRATIC_LEDGER_TO_DERIVE_J', 'CONNECTED_EFFECTIVE_HELD_SWEEP', 'PULLBACK_NONEXPANSION', 'SAT_PHYSICAL_DEFECT_RETRACT', 'G_HOLD_EXACT']}
