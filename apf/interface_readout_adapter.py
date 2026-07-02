"""The colour-record READOUT axis, wired into the Interface Engine pipeline (v24.3.306).

interface_atlas.summarize_input now dispatches AxisKind.READOUT inputs to the
commutant/record classifier, exactly the way it dispatches CODOMAIN inputs to the
codomain engine and CONTEXTUALITY inputs to the FeasBool engine. A colour-interface
rep-content spec (SU(N), an ordered tuple of fund/antifund factors), submitted as a
READOUT AtlasInput, is classified by its exact trivial-rep (singlet) multiplicity m
and returned as a first-class AtlasRouteSummary; the atlas's per-axis aggregation
buckets it under "READOUT".

The mapping is the IE's own currency, not a relabel: the IE adjudicates each input
into a global export or a named obstruction, and the record trichotomy
(check_T_canonical_colour_record_iff_multiplicity_free_P) lands on that dichotomy
literally --
  * m=1: a UNIQUE canonical (frame-free) sharp gauge-invariant record exists; the
    readout needs no frame choice -> the interface EXPORTS the canonical record
    (export_global_P=True);
  * m=0: NO sharp gauge-invariant record exists -> NAMED OBSTRUCTION
    ("readout_no_sharp_record_m0");
  * m>=2: records exist but none is canonical -- pinning one requires a basis in the
    m-dim multiplicity space with no group-canonical choice, i.e. a frame/convention
    -> NAMED OBSTRUCTION ("readout_multiplicity_frame_required_m<m>").

SEMANTICS INHERITANCE (fences, verbatim from the .281 classification):
  (i)  "gauge-invariant = physical record" is the adopted gauge-variant-CONVENTION
       (no-B) reading, [P_structural_reading] -- the multiplicities themselves are
       exact [P]-grade rep theory; the READING is not [P]. This axis inherits that
       grade split; the wiring theorem below is graded as an instrument.
  (ii) the m>=2 multiplicity-frame obstruction is the SAME SPECIES as the loc_commut
       across-interface identification (a non-group-canonical basis choice = a
       gauge-variant convention) but a DIFFERENT OBJECT (internal multiplicity basis
       vs the colour-space iso A1~=A2 between regions). Naming the obstruction does
       NOT cite, consume, or discriminate the across-frame fork.

SCOPE (honest): the axis certifies the readout CODOMAIN -- what a physical colour
readout at a declared interface can be. It is the codomain half of the reading map
named as the open object of gauge_fiber_automorphism_program (per the 2026-07-01
REDUCE note's promotion condition). It does NOT read occupancy: which interfaces are
drawn stays profile/QAC, and the drawn-content -> readings functional remains open.
READOUT inputs are SUBMITTED, exactly like CONTEXTUALITY inputs: the live atlas
does not auto-generate rep-content payloads from its abstract route/codomain
interfaces. (Data provenance differs: the scenario library's rep contents are
bank-carried objects rather than external correlator data -- a provenance remark,
not an auto-wiring claim.)
"""

from __future__ import annotations

from typing import Dict, List, Tuple


_MAX_DIM = 100  # exact-rational rank guard: N**len(factors) must stay small


def _readout_action_gens(N: int, factors: Tuple[str, ...]):
    """su(N) action on the ordered tensor product of fund/antifund factors:
    L_a = sum_k I x ... x (g_a or conj(g_a) at slot k) x ... x I."""
    from apf.gauge_invariant_record import _su_n_gens, _eye, _kron, _add, _conjm, _zeros
    gs = _su_n_gens(N)
    IN = _eye(N)
    dim = N ** len(factors)
    Ls = []
    for g in gs:
        L = _zeros(dim)
        gbar = _conjm(g)
        for k, f in enumerate(factors):
            slot = g if f == "fund" else gbar
            facs = [IN] * len(factors)
            facs[k] = slot
            E = facs[0]
            for fac in facs[1:]:
                E = _kron(E, fac)
            L = _add(L, E)
        Ls.append(L)
    return Ls


def readout_multiplicity(N: int, factors: Tuple[str, ...]) -> int:
    """Exact trivial-rep (singlet) multiplicity m of the declared rep content:
    m = dim of the joint kernel of the su(N) action generators."""
    from apf.gauge_invariant_record import _rank
    factors = tuple(factors)
    if N not in (2, 3):
        raise ValueError("readout_multiplicity: N in (2,3) only (exact-arithmetic scope)")
    if not (1 <= len(factors) <= 4):
        raise ValueError("readout_multiplicity: 1..4 factors only")
    if any(f not in ("fund", "antifund") for f in factors):
        raise ValueError("readout_multiplicity: factors must be 'fund'/'antifund'")
    dim = N ** len(factors)
    if dim > _MAX_DIM:
        raise ValueError("readout_multiplicity: dimension guard exceeded")
    Ls = _readout_action_gens(N, factors)
    M = []
    for L in Ls:
        for i in range(dim):
            M.append(L[i][:])
    return dim - _rank(M)


def readout_classify(N: int, factors: Tuple[str, ...]) -> Dict:
    """The record trichotomy on a declared colour interface, in IE currency."""
    m = readout_multiplicity(N, tuple(factors))
    if m == 1:
        verdict, obstruction = "CANONICAL_RECORD", ()
    elif m == 0:
        verdict, obstruction = "NO_SHARP_RECORD", ("readout_no_sharp_record_m0",)
    else:
        verdict = "NON_CANONICAL_MULTIPLICITY"
        obstruction = ("readout_multiplicity_frame_required_m%d" % m,)
    return {
        "N": N,
        "factors": tuple(factors),
        "multiplicity": m,
        "verdict": verdict,
        "canonical": m == 1,
        "obstruction": obstruction,
    }


def make_readout_input(input_id: str, N: int, factors) -> "AtlasInput":
    """A READOUT AtlasInput from a rep-content spec."""
    from apf.interface_atlas import AtlasInput, AtlasInputKind, AxisKind
    return AtlasInput(
        input_id=input_id, kind=AtlasInputKind.ROUTE_PAYLOAD, route=None,
        claim_text=None,
        payload={"readout_kind": "rep_content", "group": "SU", "N": int(N),
                 "factors": [str(f) for f in factors]},
        axis=AxisKind.READOUT,
    )


def route_readout(input_id: str, N: int, factors) -> "AtlasRouteSummary":
    """Route a declared colour interface through the IE pipeline (summarize_input)."""
    from apf.interface_atlas import summarize_input
    return summarize_input(make_readout_input(input_id, N, factors))


# The native scenario library: rep contents the bank already carries as objects.
NATIVE_READOUT_SCENARIOS: Tuple[Tuple[str, int, Tuple[str, ...]], ...] = (
    ("su3_meson",       3, ("fund", "antifund")),                     # m=1 canonical singlet
    ("su3_baryon",      3, ("fund", "fund", "fund")),                 # m=1 epsilon baryon
    ("su2_diquark",     2, ("fund", "fund")),                         # m=1
    ("su3_quark_pair",  3, ("fund", "fund")),                         # m=0 (3x3 = 6 + 3bar)
    ("su3_single",      3, ("fund",)),                                # m=0
    ("su2_fund4",       2, ("fund", "fund", "fund", "fund")),         # m=2 boundary (.281)
    ("su3_tetraquark",  3, ("fund", "antifund", "fund", "antifund")), # m=2 (.282)
)


def check_T_interface_readout_axis_adapter():
    """The commutant record classifier wired into the IE pipeline as the READOUT axis.

    Routes declared colour-interface rep contents through
    interface_atlas.summarize_input (the real IE entry point, not a side
    construction) and verifies the record trichotomy comes back as a first-class
    AtlasRouteSummary in the IE's export/obstruction currency, then feeds them
    through the atlas's per-axis aggregation:

      * the general multiplicity engine CROSS-VALIDATES against the three banked
        specialist computations -- an ASSEMBLY-LEVEL cross-check over shared
        exact-arithmetic primitives (both sides use _su_n_gens/_kron/_rank; what
        it validates is the general engine's slot-dispatch logic, not the shared
        kernel; the specialist values carry independent banked audits at
        .281/.282): _inv_dim_meson(2/3), _inv_dim_fund_n(2,2 / 3,3 / 2,4),
        _tetra_inv_dim(2/3);
      * su3_meson / su3_baryon / su2_diquark (m=1) -> export_global_P=True,
        CANONICAL_RECORD_EXPORTED;
      * su3_quark_pair / su3_single (m=0) -> obstruction readout_no_sharp_record_m0;
      * su2_fund4 / su3_tetraquark (m=2) -> obstruction
        readout_multiplicity_frame_required_m2 (records EXIST at m>=2; the
        obstruction is to CANONICITY, not existence);
      * _compute_axis_summary buckets all seven under axis 'READOUT'
        (7 inputs, 3 export, 4 obstructed) and leaves ROUTE/CODOMAIN/CONTEXTUALITY
        untouched.

    Certifies the genuine wiring (summarize_input dispatches to the classifier),
    not merely that the classifier produces atlas-shaped objects. Grade
    P_structural_instrument. SEMANTICS: inherits the .281 grade split -- exact
    rep-theory multiplicities under the adopted "gauge-invariant = physical
    record" [P_structural_reading]; the m>=2 frame obstruction is the same
    SPECIES as the across-interface identification but a DIFFERENT OBJECT (no
    fork citation). SCOPE: certifies the readout CODOMAIN (the codomain half of the
    gauge_fiber_automorphism_program reading map); does NOT read occupancy --
    which interfaces are drawn stays profile/QAC; the drawn-content -> readings
    functional remains open.
    """
    from apf.interface_atlas import AxisKind, _compute_axis_summary
    from apf.gauge_invariant_record import _inv_dim_meson, _inv_dim_fund_n, _tetra_inv_dim

    failures: List[str] = []

    # (1) Cross-validation: general engine vs banked specialist computations.
    xv = [
        (readout_multiplicity(2, ("fund", "antifund")), _inv_dim_meson(2), "meson N=2"),
        (readout_multiplicity(3, ("fund", "antifund")), _inv_dim_meson(3), "meson N=3"),
        (readout_multiplicity(2, ("fund", "fund")), _inv_dim_fund_n(2, 2), "fund^2 N=2"),
        (readout_multiplicity(3, ("fund",) * 3), _inv_dim_fund_n(3, 3), "fund^3 N=3"),
        (readout_multiplicity(2, ("fund",) * 4), _inv_dim_fund_n(2, 4), "fund^4 N=2"),
        (readout_multiplicity(2, ("fund", "antifund") * 2), _tetra_inv_dim(2), "tetra N=2"),
        (readout_multiplicity(3, ("fund", "antifund") * 2), _tetra_inv_dim(3), "tetra N=3"),
    ]
    for got, want, tag in xv:
        if got != want:
            failures.append("cross-validation %s: general %d != specialist %d" % (tag, got, want))

    # (2) Route the native scenario library through the IE pipeline.
    expected_m = {"su3_meson": 1, "su3_baryon": 1, "su2_diquark": 1,
                  "su3_quark_pair": 0, "su3_single": 0,
                  "su2_fund4": 2, "su3_tetraquark": 2}
    summaries = []
    for sid, N, factors in NATIVE_READOUT_SCENARIOS:
        cls = readout_classify(N, factors)
        if cls["multiplicity"] != expected_m[sid]:
            failures.append("%s: m=%d expected %d" % (sid, cls["multiplicity"], expected_m[sid]))
        s = route_readout(sid, N, factors)
        summaries.append(s)
        if s.axis != AxisKind.READOUT:
            failures.append("%s: axis not READOUT: %s" % (sid, s.to_dict()))
        if bool(s.export_global_P) != cls["canonical"]:
            failures.append("%s: pipeline export %s != classifier canonical %s"
                            % (sid, s.export_global_P, cls["canonical"]))
        if cls["canonical"] and not (s.obstruction == ()
                                     and s.solver_status == "CANONICAL_RECORD_EXPORTED"):
            failures.append("%s: canonical but not clean export: %s" % (sid, s.to_dict()))
        if (not cls["canonical"]) and not (s.obstruction == cls["obstruction"]
                                           and s.solver_status == "READOUT_OBSTRUCTION"):
            failures.append("%s: non-canonical but obstruction mismatch: %s" % (sid, s.to_dict()))

    # (3) Aggregation: bucketed under READOUT, other axes untouched.
    agg = _compute_axis_summary(tuple(summaries))
    ro = agg.get("READOUT", {})
    if not (ro.get("input_count") == 7 and ro.get("global_P_count") == 3
            and ro.get("non_global_count") == 4):
        failures.append("READOUT axis bucket wrong: %s" % (ro,))
    for other in ("ROUTE", "CODOMAIN", "CONTEXTUALITY"):
        if other in agg:
            failures.append("readout-only inputs leaked into %s bucket" % other)

    passed = not failures
    return {
        "name": (
            "T_interface_readout_axis_adapter: the commutant record classifier wired "
            "into the IE pipeline as the READOUT axis (summarize_input dispatch; "
            "m=1 canonical record = export / m=0 no-record and m>=2 frame-required = "
            "named obstructions) [P_structural]"
        ),
        "passed": passed,
        "epistemic": "P_structural_instrument",
        "dependencies": [
            "T_canonical_colour_record_iff_multiplicity_free_P",
            "T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P",
            "T_interface_contextuality_adapter",
        ],
        "failures": failures,
        "key_result": (
            "interface_atlas.summarize_input now dispatches AxisKind.READOUT inputs "
            "to the exact commutant record classifier (mirroring the CODOMAIN and "
            "CONTEXTUALITY axes). The general multiplicity engine cross-validates "
            "against the banked specialist computations (meson / fund^n / tetraquark, "
            "SU(2) and SU(3), 7 agreements; an assembly-level cross-check over shared "
            "exact primitives -- it validates the slot-dispatch logic, and the "
            "specialist values carry independent banked audits), and the SUBMITTED "
            "scenario library (bank-carried rep contents) returns "
            "first-class AtlasRouteSummary objects in the IE's export/obstruction "
            "currency: m=1 (meson, baryon, diquark) exports the canonical frame-free "
            "record; m=0 (quark pair, single quark: no record exists) and m>=2 (SU(2) "
            "fund^4, SU(3) tetraquark: records exist, none canonical -- the obstruction "
            "is to canonicity) land named obstructions; per-axis aggregation buckets all "
            "seven under 'READOUT' (3 export, 4 obstructed) without touching "
            "ROUTE/CODOMAIN/CONTEXTUALITY. This certifies the readout CODOMAIN -- "
            "the codomain half of the gauge_fiber_automorphism_program reading map; "
            "the drawn-content -> readings functional stays open, and which "
            "interfaces are drawn stays profile/QAC."
        ),
    }


_CHECKS = {
    "T_interface_readout_axis_adapter": check_T_interface_readout_axis_adapter,
}


def register(registry):
    registry.update(_CHECKS)


if __name__ == "__main__":
    r = check_T_interface_readout_axis_adapter()
    print(("PASS" if r["passed"] else "FAIL"), r["name"])
    for f in r["failures"]:
        print("   -", f)

# ---------------------------------------------------------------------------
# IE onboarding declarations (v24.3.307, Full Bank Onboarding Phase 1).
# The seven bank-carried READOUT rep contents as first-class registry inputs:
# three canonical-record exports (m=1: meson, baryon, diquark) and four named
# obstructions (m=0: single quark, quark pair; m>=2: SU(2) fund^4, SU(3)
# tetraquark). These route the gauge_invariant_record trichotomy content
# through the IE, so that sector module takes covers-credit. Static data;
# payloads mirror this adapter's own banked check scenarios.
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "readout:su3_meson",
        "expect_export": True,
        "axis": "READOUT",
        "payload": {"readout_kind": "rep_content", "group": "SU", "N": 3,
                    "factors": ["fund", "antifund"]},
        "covers": ("apf.gauge_invariant_record",),
        "note": "m=1 -> canonical frame-free record EXPORTED (the entangled singlet)",
    },
    {
        "input_id": "readout:su3_baryon",
        "expect_export": True,
        "axis": "READOUT",
        "payload": {"readout_kind": "rep_content", "group": "SU", "N": 3,
                    "factors": ["fund", "fund", "fund"]},
        "covers": ("apf.gauge_invariant_record",),
        "note": "m=1 -> canonical record EXPORTED (the epsilon baryon)",
    },
    {
        "input_id": "readout:su2_diquark",
        "expect_export": True,
        "axis": "READOUT",
        "payload": {"readout_kind": "rep_content", "group": "SU", "N": 2,
                    "factors": ["fund", "fund"]},
        "covers": ("apf.gauge_invariant_record",),
        "note": "m=1 -> canonical record EXPORTED",
    },
    {
        "input_id": "readout:su3_single_quark",
        "expect_export": False,
        "axis": "READOUT",
        "payload": {"readout_kind": "rep_content", "group": "SU", "N": 3,
                    "factors": ["fund"]},
        "covers": ("apf.gauge_invariant_record",),
        "note": "m=0 -> named obstruction: no sharp gauge-invariant record",
    },
    {
        "input_id": "readout:su3_quark_pair",
        "expect_export": False,
        "axis": "READOUT",
        "payload": {"readout_kind": "rep_content", "group": "SU", "N": 3,
                    "factors": ["fund", "fund"]},
        "covers": ("apf.gauge_invariant_record",),
        "note": "m=0 -> named obstruction: no sharp gauge-invariant record",
    },
    {
        "input_id": "readout:su2_fund4",
        "expect_export": False,
        "axis": "READOUT",
        "payload": {"readout_kind": "rep_content", "group": "SU", "N": 2,
                    "factors": ["fund", "fund", "fund", "fund"]},
        "covers": ("apf.gauge_invariant_record",),
        "note": "m=2 -> named obstruction: multiplicity-frame required",
    },
    {
        "input_id": "readout:su3_tetraquark",
        "expect_export": False,
        "axis": "READOUT",
        "payload": {"readout_kind": "rep_content", "group": "SU", "N": 3,
                    "factors": ["fund", "antifund", "fund", "antifund"]},
        "covers": ("apf.gauge_invariant_record",),
        "note": "m=2 -> named obstruction: multiplicity-frame required",
    },
)
