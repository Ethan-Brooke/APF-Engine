"""Sep/IJC FeasBool engine, wired into the Interface Engine pipeline (v24.3.291).

interface_atlas.summarize_input now dispatches AxisKind.CONTEXTUALITY inputs to
the FeasBool / Boolean-defender engine (apf.ijc_feasbool_engine), exactly the way
it dispatches CODOMAIN inputs to the codomain engine. A correlation-table or
parity interface, submitted as a CONTEXTUALITY AtlasInput, is routed through the
engine and returned as a first-class AtlasRouteSummary; the atlas's per-axis
aggregation buckets it under "CONTEXTUALITY".

The mapping is the IE's own currency, not a relabel: the IE adjudicates each input
into a global-P export or a named obstruction, and a contextuality interface lands
on that dichotomy literally --
  * SepStr / consistent (classical): a faithful global hidden-variable section
    EXISTS -> the interface EXPORTS A GLOBAL SECTION (export_global_P=True);
  * IJCStr / inconsistent (quantum): no global section; the separating
    Bell/noncontextuality inequality (Farkas dual) or GF(2) parity certificate is
    the NAMED OBSTRUCTION (export_global_P=False).

SCOPE (honest): the IE routes CONTEXTUALITY-axis inputs that ARE submitted with a
correlation table / parity-context list. The canonical/live atlas does not
auto-generate contextuality inputs from the abstract route/codomain interfaces
(those carry no correlation data). Occupancy stays the QAC; the engine computes
the math verdict (branch + certificate), not occupancy. Grade P_structural.
"""

from __future__ import annotations

try:
    from apf.interface_atlas import (
        summarize_input, AtlasInput, AtlasInputKind, AxisKind, _compute_axis_summary,
    )
except Exception:  # pragma: no cover
    from interface_atlas import (
        summarize_input, AtlasInput, AtlasInputKind, AxisKind, _compute_axis_summary,
    )


def make_chsh_contextuality_input(input_id, E):
    """A CONTEXTUALITY AtlasInput from a (2,2,2) Bell correlator 4-vector E."""
    return AtlasInput(
        input_id=input_id, kind=AtlasInputKind.ROUTE_PAYLOAD, route=None,
        claim_text=None,
        payload={"contextuality_kind": "chsh_correlators", "E": [str(x) for x in E]},
        axis=AxisKind.CONTEXTUALITY,
    )


def make_parity_contextuality_input(input_id, n_obs, contexts):
    """A CONTEXTUALITY AtlasInput from a Mermin-style parity system.
    contexts: list of (iterable_of_obs_indices, parity_bit)."""
    return AtlasInput(
        input_id=input_id, kind=AtlasInputKind.ROUTE_PAYLOAD, route=None,
        claim_text=None,
        payload={"contextuality_kind": "parity", "n_obs": int(n_obs),
                 "contexts": [[list(vs), int(b)] for vs, b in contexts]},
        axis=AxisKind.CONTEXTUALITY,
    )


def make_scenario_contextuality_input(input_id, scenario_dict):
    """A CONTEXTUALITY AtlasInput from an arbitrary finite marginal scenario.

    scenario_dict is a ``ijc_feasbool_engine.scenario_to_dict`` payload
    (carries ``contextuality_kind='scenario'`` + measurements / contexts /
    empirical table). Routes through the general Boole-polytope LP, not the
    (2,2,2) correlator or parity shells."""
    pl = dict(scenario_dict)
    pl["contextuality_kind"] = "scenario"
    return AtlasInput(
        input_id=input_id, kind=AtlasInputKind.ROUTE_PAYLOAD, route=None,
        claim_text=None, payload=pl, axis=AxisKind.CONTEXTUALITY,
    )


def route_contextuality(input_id, *, chsh_E=None, parity=None, scenario=None):
    """Route a contextuality interface through the IE pipeline (summarize_input)."""
    if chsh_E is not None:
        return summarize_input(make_chsh_contextuality_input(input_id, chsh_E))
    if parity is not None:
        return summarize_input(make_parity_contextuality_input(input_id, *parity))
    if scenario is not None:
        return summarize_input(make_scenario_contextuality_input(input_id, scenario))
    raise ValueError("route_contextuality needs chsh_E, parity, or scenario")


def check_T_interface_contextuality_adapter():
    """The Sep/IJC FeasBool engine wired into the IE pipeline as the CONTEXTUALITY axis.

    Routes contextuality interfaces through interface_atlas.summarize_input (the
    real IE entry point, not a side construction) and verifies the engine verdict
    comes back as a first-class AtlasRouteSummary whose global-P-export flag
    matches the engine, then feeds them through the atlas's per-axis aggregation:
      * CHSH-local table -> export_global_P=True (global section exported);
      * PR box (S=4)     -> export_global_P=False, named obstruction;
      * Mermin-Peres magic square (parity path) -> export_global_P=False, obstruction;
      * consistent control (2-odd 5-cycle, parity path) -> export_global_P=True;
      * _compute_axis_summary buckets all four under axis 'CONTEXTUALITY'
        (4 inputs, 2 global-P, 2 obstructed) and leaves ROUTE/CODOMAIN untouched.

    Certifies the genuine wiring (summarize_input dispatches to the engine), not
    merely that the engine produces atlas-shaped objects. Grade P_structural.
    SCOPE: routes submitted CONTEXTUALITY inputs; does not auto-discover
    contextuality in abstract route/codomain interfaces. Occupancy stays the QAC.
    """
    failures = []

    loc = route_contextuality("chsh_local", chsh_E=("0", "0", "0", "0"))
    if not (loc.export_global_P and loc.obstruction == () and loc.axis == AxisKind.CONTEXTUALITY
            and loc.solver_status == "GLOBAL_SECTION_EXPORTED"):
        failures.append("CHSH-local via pipeline should export: %s" % (loc.to_dict(),))

    pr = route_contextuality("pr_box", chsh_E=("1", "1", "1", "-1"))
    if pr.export_global_P or not pr.obstruction or pr.axis != AxisKind.CONTEXTUALITY:
        failures.append("PR box via pipeline should be obstructed: %s" % (pr.to_dict(),))

    ms_ctx = [([3 * r + c for c in range(3)], 0) for r in range(3)] \
        + [([3 * r + c for r in range(3)], 1) for c in range(3)]
    ms = route_contextuality("magic_square", parity=(9, ms_ctx))
    if ms.export_global_P or not ms.obstruction:
        failures.append("magic square via pipeline should be obstructed: %s" % (ms.to_dict(),))

    cyc = [({i, (i + 1) % 5}, 1 if i < 2 else 0) for i in range(5)]
    ctrl = route_contextuality("cycle5_2odd", parity=(5, cyc))
    if not ctrl.export_global_P:
        failures.append("2-odd 5-cycle control via pipeline should export: %s" % (ctrl.to_dict(),))

    agg = _compute_axis_summary((loc, pr, ms, ctrl))
    cx = agg.get("CONTEXTUALITY", {})
    if not (cx.get("input_count") == 4 and cx.get("global_P_count") == 2
            and cx.get("non_global_count") == 2):
        failures.append("CONTEXTUALITY axis bucket wrong: %s" % (cx,))
    if "ROUTE" in agg or "CODOMAIN" in agg:
        failures.append("contextuality-only inputs leaked into ROUTE/CODOMAIN buckets")

    passed = not failures
    return {
        "name": (
            "T_interface_contextuality_adapter: the Sep/IJC FeasBool engine wired "
            "into the IE pipeline as the CONTEXTUALITY axis (summarize_input "
            "dispatch; SepStr=global-P export / IJCStr=named obstruction) [P_structural]"
        ),
        "passed": passed,
        "epistemic": "P_structural_instrument",
        "dependencies": [
            "T_feasbool_general_contextuality",
            "T_ks_parity_contextuality_scalable",
        ],
        "failures": failures,
        "key_result": (
            "interface_atlas.summarize_input now dispatches AxisKind.CONTEXTUALITY "
            "inputs to the FeasBool engine (mirroring the CODOMAIN axis). Routing "
            "CHSH-local / PR-box / magic-square / a consistent cycle through the IE "
            "pipeline returns first-class AtlasRouteSummary objects whose "
            "export_global_P matches the engine (SepStr->export, IJCStr->named "
            "obstruction = the Bell inequality or GF(2) parity certificate), and the "
            "atlas's per-axis aggregation buckets them under 'CONTEXTUALITY' (4 "
            "inputs, 2 export, 2 obstructed) without touching ROUTE/CODOMAIN. The map "
            "is the IE's own global-P-export/named-obstruction currency. SCOPE: "
            "routes submitted CONTEXTUALITY inputs; the live atlas does not "
            "auto-generate them. Occupancy stays the QAC."
        ),
    }


def check_T_interface_contextuality_general_scenario():
    """The GENERAL FeasBool engine routed through the IE pipeline (arbitrary scenarios).

    The v24.3.291 adapter only fed the engine via two specialized shells -- a
    (2,2,2) correlator 4-vector or a parity-context list. This check certifies
    the third, general path: an ARBITRARY finite marginal scenario (any
    measurements, any finite outcome sets, any context hypergraph, any
    behaviour table) submitted as a CONTEXTUALITY AtlasInput is routed through
    interface_atlas.summarize_input to the exact Boole-polytope LP, and the
    pipeline verdict matches the engine called directly:
      * SepStr  -> a faithful global hidden-variable section EXISTS
                   (export_global_P=True, GLOBAL_SECTION_EXPORTED);
      * IJCStr  -> the Farkas dual is a generalized Bell/noncontextuality
                   inequality (export_global_P=False, named obstruction).

    Cases are round-tripped engine-scenario -> scenario_to_dict -> pipeline, so
    the test pins the (de)serialization AND the dispatch. Verdicts are checked
    against feasbool() on the original Scenario (not hand-set):
      GHZ/Mermin (3-party) -> IJCStr; qutrit noncontextual -> SepStr;
      PR box (as full table) -> IJCStr; magic square -> IJCStr.
    The per-axis aggregation buckets all four under CONTEXTUALITY (1 export,
    3 obstructed) and leaves ROUTE/CODOMAIN untouched.

    Grade P_structural. SCOPE: routes a SUBMITTED scenario table; does not
    auto-discover contextuality in abstract route/codomain interfaces.
    Occupancy stays the QAC -- the engine computes the math (Boole-membership)
    verdict, not the physical occupancy bit.
    """
    from apf.ijc_feasbool_engine import (
        scenario_to_dict, feasbool,
        scenario_ghz_mermin, scenario_qutrit_noncontextual,
        scenario_chsh_prbox, scenario_mermin_peres_magic_square,
    )

    failures = []
    cases = [
        ("ghz_mermin_scn", scenario_ghz_mermin()),
        ("qutrit_nc_scn", scenario_qutrit_noncontextual()),
        ("pr_box_scn", scenario_chsh_prbox()),
        ("magic_square_scn", scenario_mermin_peres_magic_square()),
    ]
    summaries = []
    for cid, scn in cases:
        engine_sep = feasbool(scn)["branch"] == "SepStr"
        s = route_contextuality(cid, scenario=scenario_to_dict(scn))
        summaries.append(s)
        if s.axis != AxisKind.CONTEXTUALITY:
            failures.append("%s: axis not CONTEXTUALITY: %s" % (cid, s.to_dict()))
        if bool(s.export_global_P) != engine_sep:
            failures.append(
                "%s: pipeline export %s != engine SepStr %s"
                % (cid, s.export_global_P, engine_sep))
        if engine_sep and not (s.obstruction == () and s.solver_status == "GLOBAL_SECTION_EXPORTED"):
            failures.append("%s: SepStr but not clean export: %s" % (cid, s.to_dict()))
        if (not engine_sep) and not (s.obstruction and s.solver_status == "IJC_OBSTRUCTION"):
            failures.append("%s: IJCStr but no named obstruction: %s" % (cid, s.to_dict()))

    agg = _compute_axis_summary(tuple(summaries))
    cx = agg.get("CONTEXTUALITY", {})
    if not (cx.get("input_count") == 4 and cx.get("global_P_count") == 1
            and cx.get("non_global_count") == 3):
        failures.append("CONTEXTUALITY axis bucket wrong: %s" % (cx,))
    if "ROUTE" in agg or "CODOMAIN" in agg:
        failures.append("general-scenario inputs leaked into ROUTE/CODOMAIN buckets")

    passed = not failures
    return {
        "name": (
            "T_interface_contextuality_general_scenario: the GENERAL Boole-polytope "
            "FeasBool engine routed through the IE pipeline -- an arbitrary finite "
            "marginal scenario lands on SepStr (global-P export) / IJCStr (Farkas "
            "named obstruction), bucketed under CONTEXTUALITY [P_structural]"
        ),
        "passed": passed,
        "epistemic": "P_structural_instrument",
        "dependencies": [
            "T_interface_contextuality_adapter",
            "T_feasbool_general_contextuality",
        ],
        "failures": failures,
        "key_result": (
            "interface_atlas.summarize_input now dispatches a full arbitrary-scenario "
            "CONTEXTUALITY payload to feasbool() (the exact Boole-polytope LP), not "
            "only the (2,2,2) correlator and parity shells. GHZ/Mermin, qutrit, PR "
            "box, and the magic square -- round-tripped scenario->dict->pipeline -- "
            "return AtlasRouteSummary verdicts matching the engine (1 export, 3 "
            "named obstructions) and bucket under CONTEXTUALITY without touching "
            "ROUTE/CODOMAIN. The map is the IE's global-P-export / named-obstruction "
            "currency. SCOPE: routes a submitted scenario; occupancy stays the QAC."
        ),
    }


_CHECKS = {
    "T_interface_contextuality_adapter": check_T_interface_contextuality_adapter,
    "T_interface_contextuality_general_scenario": check_T_interface_contextuality_general_scenario,
}


def register(registry):
    registry.update(_CHECKS)


if __name__ == "__main__":
    for fn_check in (check_T_interface_contextuality_adapter,
                     check_T_interface_contextuality_general_scenario):
        r = fn_check()
        print(("PASS" if r["passed"] else "FAIL"), r["name"])
        for f in r["failures"]:
            print("   -", f)

# ---------------------------------------------------------------------------
# IE onboarding declarations (v24.3.307, Full Bank Onboarding Phase 1).
# The four bank-carried CONTEXTUALITY scenarios as first-class registry
# inputs: two exports (local CHSH interior point; consistent parity cycle)
# and two named obstructions (PR box; Mermin-Peres magic square). These
# route the ijc_feasbool_engine's banked content through the IE, so the
# engine module takes covers-credit. Static data; payloads mirror the
# adapter's own banked check scenarios.
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "contextuality:chsh_local",
        "expect_export": True,
        "axis": "CONTEXTUALITY",
        "payload": {"contextuality_kind": "chsh_correlators",
                    "E": ["3/5", "3/5", "3/5", "3/5"]},
        "covers": ("apf.ijc_feasbool_engine",),
        "note": "local interior point (all CHSH sign choices |S|=6/5<=2) -> SepStr export",
    },
    {
        "input_id": "contextuality:pr_box",
        "expect_export": False,
        "axis": "CONTEXTUALITY",
        "payload": {"contextuality_kind": "chsh_correlators",
                    "E": ["1", "1", "1", "-1"]},
        "covers": ("apf.ijc_feasbool_engine",),
        "note": "PR box (S=4) -> IJCStr named obstruction (CHSH/Fine separator)",
    },
    {
        "input_id": "contextuality:magic_square_parity",
        "expect_export": False,
        "axis": "CONTEXTUALITY",
        "payload": {"contextuality_kind": "parity", "n_obs": 9,
                    "contexts": [[[0, 1, 2], 0], [[3, 4, 5], 0], [[6, 7, 8], 0],
                                 [[0, 3, 6], 0], [[1, 4, 7], 0], [[2, 5, 8], 1]]},
        "covers": ("apf.ijc_feasbool_engine",),
        "note": "Mermin-Peres magic square (GF(2) 0=1) -> IJCStr named obstruction",
    },
    {
        "input_id": "contextuality:consistent_cycle",
        "expect_export": True,
        "axis": "CONTEXTUALITY",
        "payload": {"contextuality_kind": "parity", "n_obs": 4,
                    "contexts": [[[0, 1], 0], [[1, 2], 0], [[2, 3], 0], [[3, 0], 0]]},
        "covers": ("apf.ijc_feasbool_engine",),
        "note": "even 4-cycle (consistent GF(2) system) -> SepStr export",
    },
)
