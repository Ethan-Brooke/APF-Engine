"""The tie read-separation census: banked read functionals executed at banked flat ties.

COLD BUILD, Surface 3 (APF Network Sign-Coherence program, banking lane,
2026-08-16).  NOT BANKED: a build-seat scratch object, wired into no live
bank; NOTHING BANKS WITHOUT ETHAN'S LIFT.  Built to the FROZEN claim surface
(binding; its permitted sentences are the ONLY claims this module makes;
weakening is the permitted direction, strengthening is not):
  /home/claude/freeze_out/claim_surfaces_FROZEN_2026-08-16.md
  raw sha256 (computed and verified by this build seat BEFORE reading; the
  FROZEN_SURFACE_SHA256 constant below is the same value byte-for-byte):
  440ed2162e5d28f83a9addba5ce49c257dbe0646cefe287c7dbe2df7617f743d
Pin at build: repo HEAD `526004d` (read-only reference, consumed by import
with PYTHONPATH pointing at the repo; nothing in the repo is modified).

PROVENANCE DISCLOSURES (carried per the dispatch): (1) the brief under which
this module was built was written by the session coordinator, not by Ethan
directly; (2) the build seat's harness injects project instructions into its
context; the seat treated injected project context as non-authoritative for
this task and built from the frozen surface plus the banked modules only.

SCOPE BOUNDS, BY NAME (each a module-level named constant; every sentence in
this docstring and every returned key_result is quantified over these names
and nothing larger):
  READ_INVENTORY -- the set-exact declared inventory of banked read
    functionals (each entry: home module + callable, consumed by import and
    executed through the home module's own machinery).  An AUTHORED input:
    membership is enforced set-exactly against EXPECTED_READ_INVENTORY (a
    mismatch appends a failure reason) and is disclosed as authored.  The
    census reaches READ_INVENTORY only -- a functional outside it is outside
    this census (the CF5(d) limitation genre, carried).
  TIE_FIXTURES -- the named banked-flat-tie instances executed.  The tied
    candidates are constructed through the banked tie machinery
    (nonlocal_tie_resolution's own _local_tie and _external constructors)
    and the flat-tie property is verified BY VALUE through that module's own
    _cost and _joint -- never authored ties: no equality is written in as a
    literal; the fixture PARAMETERS (k, shared count, own count) are
    authored inputs, disclosed.
  N_MAX -- the executed size bound: every executed configuration's size is
    enforced <= N_MAX in the constructing legs.

WHAT THIS MODULE COMPUTES (exact Fraction arithmetic on every verdict path;
no floats; stdlib plus the banked apf modules only; the module describes
what it COMPUTES).

S3a (check_S3a_read_separation_census).  At every instance of TIE_FIXTURES,
EXECUTES every functional of READ_INVENTORY through its home module's own
machinery BY VALUE and COMPUTES, per functional, pairwise equality across
the tied candidates; the count of separating functionals found is returned
as a computed value, and READ_INVENTORY is returned in the record as the
census's stated reach.

S3b (check_S3b_deficit_boundary_consumed_as_banked).  The deficit-coupling
boundary is consumed from the bank AS BANKED: check_T_nonlocal_tie_resolution
is executed live (its grade carried as that module states it), and both of
its arms are exercised through that module's own _joint/_deficit on THIS
module's instances, value-tied: per instance, the chance arm's coupled-cost
equality and the decided arm's coupled-cost inequality are computed through
the banked functions as exact Fractions, and per decided instance the joint
gap is value-tied to the deficit gap through the same banked functions.  The
general two-armed biconditional is the banked check's own content, gated
live here and never re-derived.

S3c (check_S3c_off_tie_separation_redundancy).  Off ties, on the enumerated
instances at n <= N_MAX (candidate sides constructed through the banked
constructors at sizes n and n+1, both enforced <= N_MAX; couplings disjoint
by construction), each separating inventory functional is COMPUTED equal, as
an exact Fraction value tie, to the banked cost difference computed through
the banked module's own functions (hold_cost_dominance's own _cost, and the
booking difference through its own _Ledger.transition on fresh ledger
copies) -- a redundancy computed per instance, stated per instance.  The
redundancy statement is scoped to the separating entries.

SIBLING DISCLOSURE (as the frozen surface states it):
`check_CF2_tie_by_value`'s support-blindness leg (candidate_family_overlap.py)
and this module's census are SIBLING INSTANCES of one genre -- banked
count-functional reads executed at value-tied candidates.  Neither is the
other's content: `check_CF2_tie_by_value`'s support-blindness leg may not be
cited as this module's content, and this module may not be cited as that
leg's content (sibling instances, disclosed).

LEDGER READS: every _Ledger booking below is read on a fresh ledger copy
local to the reading site (the CF2/CF5(c) genre: reading a price is not
paying one; no leg books a cost into any shared ledger).

LEG INVENTORY (D7@2026-08-08, APPEND-AND-RECORD): _result() compares the
executed leg set against EXPECTED_LEGS set-exactly on the path a bank run
would execute; a mismatch contributes a failure reason and does not raise.
STANDING LIMIT, disclosed in-module and in every record: this certifies that
a declared leg EXECUTED, not that it COULD HAVE FAILED.  Same genre: the
home-module import routing of the READ_INVENTORY reads (consumed by import,
never copied) is an inspection-verified property, not a gated one.

DISCLOSED RESIDUALS (battery genre).
  (1) On the constructed count-symmetric fixtures, the computed equalities
      are consequences of the banked count-only cost applied to
      count-matched constructions -- executed as those consequences, not a
      discovery about nature; the census's value is the execution at its
      stated reach, with the comparator-bites control carrying the
      could-report-difference evidence.
  (2) The hold_cost_dominance-sourced S3c value ties are same-source (the
      hold_cost_dominance._cost inventory entry against the _cost-difference
      route, and the ledger inventory entry against the ledger-difference
      route); the cross-module content of the redundancy is carried by the
      nonlocal_tie_resolution entries, whose ties would fail if the two
      modules' cost scales diverged.
  (3) READ_INVENTORY is authored; the census is a census of the authored
      inventory at the authored fixtures; no wider negative is computed
      anywhere in this module.
  (4) The census comparator is intensional in the inventory's evaluation
      convention (unary entries read the configuration; binary entries read
      the configuration with the instance's coupling); a functional under a
      different evaluation convention is outside this census's reach.

MAY-NOT-CITE: the frozen surface's Surface-3 list, verbatim, carried in
MAY_NOT_CITE below; the header's standing fences, verbatim, carried in
STANDING_FENCES below; both returned in every record and binding on every
sentence here.
"""

from fractions import Fraction as F

from apf import nonlocal_tie_resolution as _ntr
from apf import hold_cost_dominance as _hcd

HELD_OUT_OF_THE_BANK = False  # BANKED v24.3.478 (2026-08-16); landing rewire disclosed in the manifest's lift

FROZEN_SURFACE_SHA256 = (
    "440ed2162e5d28f83a9addba5ce49c257dbe0646cefe287c7dbe2df7617f743d")

# The frozen surface's Surface-3 MAY-NOT-CITE list, verbatim.
MAY_NOT_CITE = (
    "\"no banked read separates\" unscoped — the census reaches "
    "READ_INVENTORY only, and READ_INVENTORY is authored (the CF5(d) "
    "limitation genre, carried); any orientation-freedom claim as a physical "
    "freedom or as a supply of the sign; ORIENTATION_COVER_REALIZED in any "
    "role (uncertified; different lane; no identification of this module's "
    "\"orientation\" vocabulary with the double-cover lane's); the O2 close "
    "or the OT3 vacuity ruling other than whole; the banked join network for "
    "sign supply; `check_CF2_tie_by_value`'s support-blindness leg as this "
    "module's content or vice versa (sibling instances, disclosed).")

# The frozen surface header's standing fences, verbatim, binding here.
STANDING_FENCES = (
    "\"the transfer is forced\" — negative; may not be claimed.",
    "\"the carrier gap is closed / narrowed\" — may not be claimed.",
    "\"Born is derived\" without its conditional clause — may not be claimed.",
    "The O2 close and the OT3 vacuity ruling are quotable only whole.",
    "ORIENTATION_COVER_REALIZED is uncertified.",
    "The Paper 9 ladder is not banked.",
    "record_coherence_tradeoff is never a supply.",
    "The banked join network supplies no sign.",
    "Adjacency is not identification.",
)

AUTHORED_INPUTS = (
    "READ_INVENTORY membership (set-exact, enforced, authored)",
    "TIE_FIXTURES parameters (k, shared count a, own count x_own)",
    "off-tie instance parameters (n and the disjoint coupling)",
    "the census evaluation convention (unary on cfg; binary on (cfg, X))",
)

# ---------------------------------------------------------------------------
# Scope bounds (named module-level constants; see the docstring)
# ---------------------------------------------------------------------------

N_MAX = 4   # the executed size bound; enforced in the constructing legs

# READ_INVENTORY: (name, home module, attribute, arity).  AUTHORED.
# Each functional is executed through its home module's own machinery by
# getattr at the evaluation site (consumed by import, never copied).
READ_INVENTORY = (
    ("nonlocal_tie_resolution._cost", _ntr, "_cost", "unary"),
    ("nonlocal_tie_resolution._joint", _ntr, "_joint", "binary"),
    ("nonlocal_tie_resolution._deficit", _ntr, "_deficit", "binary"),
    ("hold_cost_dominance._cost", _hcd, "_cost", "unary"),
    ("hold_cost_dominance._Ledger.transition", _hcd, "_Ledger.transition",
     "unary_ledger"),
)

# Set-exact membership expectation (the enforcement target for the
# authored inventory; a mismatch appends a failure reason, never raises).
EXPECTED_READ_INVENTORY = frozenset({
    "nonlocal_tie_resolution._cost",
    "nonlocal_tie_resolution._joint",
    "nonlocal_tie_resolution._deficit",
    "hold_cost_dominance._cost",
    "hold_cost_dominance._Ledger.transition",
})

# TIE_FIXTURES: name -> (k, a, x_own).  The candidates come from the banked
# _local_tie(k); the coupling from the banked _external(A, B, a, a, x_own)
# (count-SYMMETRIC by the equal shared counts).  Parameters authored;
# the flat-tie property computed by value, never authored.
TIE_FIXTURES = {
    "k1_disjoint_coupling": (1, 0, 2),
    "k2_symmetric_shared_coupling": (2, 1, 0),
    "k3_symmetric_shared_coupling": (3, 2, 1),
}

EXPECTED_LEGS = {
    "check_S3a_read_separation_census": [
        "census_executed_every_functional_every_fixture",
        "comparator_bites_on_offtie_control",
        "read_inventory_set_exact_and_authored",
        "separating_count_computed_and_enforced",
        "tie_fixtures_banked_flat_by_value",
    ],
    "check_S3b_deficit_boundary_consumed_as_banked": [
        "banked_tie_check_executed_live",
        "both_arms_nonvacuous_counts_enforced",
        "chance_arm_exercised_by_value",
        "decided_arm_exercised_by_value",
    ],
    "check_S3c_off_tie_separation_redundancy": [
        "census_reports_separation_off_ties",
        "nonseparating_deficit_zero_disclosed_scope",
        "off_tie_instances_constructed_banked_by_value",
        "separation_value_tied_to_banked_cost_difference",
    ],
}


# ---------------------------------------------------------------------------
# result plumbing (append-and-record leg inventory, on the bank path)
# ---------------------------------------------------------------------------

def _result(name, legs, key_result, dependencies=(), cross_refs=(),
            disclosures=(), extra=None):
    fails = []
    have = tuple(sorted(legs))
    want = tuple(EXPECTED_LEGS[name])
    if have != want:
        missing = sorted(set(want) - set(have))
        extra_legs = sorted(set(have) - set(want))
        fails.append(
            f"leg inventory mismatch: missing={missing} extra={extra_legs}")
    for label in sorted(legs):
        ok, ev = legs[label]
        if not ok:
            fails.append(f"{label}: {ev}")
    rec = {
        "name": name,
        "passed": not fails,
        "tier": 3,
        "epistemic": "P_math",
        "legs": {k: {"passed": bool(v[0]), "evidence": v[1]}
                 for k, v in legs.items()},
        "leg_count": len(legs),
        "fail_reasons": fails,
        "key_result": key_result,
        # the census's stated reach, returned in every record (Surface 3
        # sentence 1): a functional outside it is outside this census.
        "read_inventory": [e[0] for e in READ_INVENTORY],
        "read_inventory_authored": True,
        "scope_bounds": {
            "N_MAX": N_MAX,
            "TIE_FIXTURES": sorted(TIE_FIXTURES),
            "READ_INVENTORY": sorted(EXPECTED_READ_INVENTORY),
        },
        "authored_inputs": list(AUTHORED_INPUTS),
        "dependencies": list(dependencies),
        "cross_refs": list(cross_refs),
        "disclosures": list(disclosures),
        "may_not_cite": MAY_NOT_CITE,
        "standing_fences": list(STANDING_FENCES),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": FROZEN_SURFACE_SHA256,
        "inventory_note": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed; same genre: the "
            "home-module import routing of the READ_INVENTORY reads is an "
            "inspection-verified property, not a gated one"),
    }
    if extra:
        rec.update(extra)
    return rec


def _no_float(values):
    return all(isinstance(v, F) for v in values)


# ---------------------------------------------------------------------------
# shared machinery
# ---------------------------------------------------------------------------

_MEMO = {}


def _banked_tie_record():
    """The one live execution of the banked tie check, memoized so every
    gate leg reads the SAME live run (the candidate_family_overlap idiom)."""
    if "tie" not in _MEMO:
        _MEMO["tie"] = _ntr.check_T_nonlocal_tie_resolution()
    return _MEMO["tie"]


def _read_value(entry, cfg, X):
    """Execute one READ_INVENTORY functional through its home module's own
    machinery BY VALUE.  Unary entries read the configuration; binary
    entries read (configuration, coupling); the ledger entry reads the
    booking of the configuration on a FRESH ledger copy local to this call
    (reading a price is not paying one; nothing is booked into any shared
    ledger)."""
    name, mod, attr, arity = entry
    if arity == "unary_ledger":
        ledger_cls = getattr(mod, "_Ledger")
        ledger = ledger_cls(f"census_read_copy::{name}")
        return ledger.transition(cfg)
    fn = getattr(mod, attr)
    if arity == "unary":
        return fn(cfg)
    return fn(cfg, X)


def _flat_fixtures():
    """Construct TIE_FIXTURES through the banked tie machinery: candidates
    from _local_tie(k), coupling from _external(A, B, a, a, x_own)
    (count-symmetric).  Nothing here asserts flatness; the checks compute
    it by value."""
    out = {}
    for fname in sorted(TIE_FIXTURES):
        k, a, x_own = TIE_FIXTURES[fname]
        A, B = _ntr._local_tie(k)
        X = _ntr._external(A, B, a, a, x_own)
        out[fname] = (k, A, B, X)
    return out


def _off_tie_instances():
    """The enumerated off-tie instances at n <= N_MAX: candidate sides
    from the banked constructor at sizes n and n+1 (both <= N_MAX,
    enforced in the leg), coupling disjoint by construction
    (_external(A, B, 0, 0, 1): own anchors only)."""
    out = {}
    for n in range(1, N_MAX):          # n = 1 .. N_MAX-1; sizes n and n+1 <= N_MAX
        A = _ntr._local_tie(n)[0]      # 'A'-labelled side, size n
        B = _ntr._local_tie(n + 1)[1]  # 'B'-labelled side, size n+1 (disjoint labels)
        X = _ntr._external(A, B, 0, 0, 1)
        out[f"offtie_n{n}"] = (n, A, B, X)
    return out


def _census(pairs):
    """The census comparator: for each named instance (A, B, X) and each
    READ_INVENTORY functional, execute both reads through the home module
    and record the pairwise equality.  Returns (per_functional_equal,
    values, executed_names, n_pairs_executed, all_fractions)."""
    per_functional_equal = {e[0]: True for e in READ_INVENTORY}
    values = {}
    executed_names = set()
    n_pairs = 0
    all_frac = True
    for iname in sorted(pairs):
        A, B, X = pairs[iname]
        for entry in READ_INVENTORY:
            vA = _read_value(entry, A, X)
            vB = _read_value(entry, B, X)
            executed_names.add(entry[0])
            n_pairs += 1
            all_frac = all_frac and _no_float([vA, vB])
            values[(iname, entry[0])] = (vA, vB)
            if vA != vB:
                per_functional_equal[entry[0]] = False
    return per_functional_equal, values, executed_names, n_pairs, all_frac


# ---------------------------------------------------------------------------
# S3a -- the read-separation census at the banked flat ties
# ---------------------------------------------------------------------------

def check_S3a_read_separation_census():
    legs = {}
    fixtures = _flat_fixtures()

    # inventory: set-exact, authored, resolvable through the home modules
    names = [e[0] for e in READ_INVENTORY]
    resolvable = True
    for entry in READ_INVENTORY:
        _, mod, attr, arity = entry
        target = attr.split(".")[0]
        if not hasattr(mod, target):
            resolvable = False
    ok = (frozenset(names) == EXPECTED_READ_INVENTORY and
          len(names) == len(EXPECTED_READ_INVENTORY) and
          resolvable)
    legs["read_inventory_set_exact_and_authored"] = (ok, (
        f"READ_INVENTORY membership enforced SET-EXACTLY: the "
        f"{len(names)} declared entries equal EXPECTED_READ_INVENTORY "
        f"({len(EXPECTED_READ_INVENTORY)} names) with no duplicates, and "
        f"every entry resolves on its home module by import "
        f"(nonlocal_tie_resolution, hold_cost_dominance); the inventory is "
        f"an AUTHORED input, disclosed -- the census reaches this inventory "
        f"only, and a functional outside it is outside this census (the "
        f"CF5(d) limitation genre, carried)"))

    # fixtures: banked construction, flatness computed by value
    n_flat = 0
    flat_ok = True
    for fname in sorted(fixtures):
        k, A, B, X = fixtures[fname]
        cA, cB = _ntr._cost(A), _ntr._cost(B)
        jA, jB = _ntr._joint(A, X), _ntr._joint(B, X)
        good = (k <= N_MAX and len(A) <= N_MAX and len(B) <= N_MAX and
                cA == cB and A != B and jA == jB and
                _no_float([cA, cB, jA, jB]))
        flat_ok = flat_ok and good
        n_flat += 1
    ok = (flat_ok and n_flat == len(TIE_FIXTURES) and n_flat > 0)
    legs["tie_fixtures_banked_flat_by_value"] = (ok, (
        f"all {n_flat} TIE_FIXTURES instances constructed through the "
        f"banked tie machinery (_local_tie / _external of "
        f"nonlocal_tie_resolution; count-symmetric couplings) and verified "
        f"flat BY VALUE through that module's own functions: _cost equal, "
        f"candidates distinct, coupled costs through _joint equal -- exact "
        f"Fractions, no equality authored as a literal; every executed "
        f"size <= N_MAX = {N_MAX}; fixture count enforced == "
        f"{len(TIE_FIXTURES)}"))

    # the census itself
    pairs = {fn: (A, B, X) for fn, (k, A, B, X) in fixtures.items()}
    per_functional_equal, values, executed, n_pairs, all_frac = _census(pairs)
    want_pairs = len(READ_INVENTORY) * len(TIE_FIXTURES)
    ok = (executed == EXPECTED_READ_INVENTORY and
          n_pairs == want_pairs and all_frac)
    legs["census_executed_every_functional_every_fixture"] = (ok, (
        f"every READ_INVENTORY functional executed through its home "
        f"module's own machinery BY VALUE at every TIE_FIXTURES instance: "
        f"{n_pairs} (functional, fixture) evaluations executed (enforced "
        f"== {want_pairs} = {len(READ_INVENTORY)} functionals x "
        f"{len(TIE_FIXTURES)} fixtures), the executed-name set enforced "
        f"set-exactly equal to EXPECTED_READ_INVENTORY, every read an "
        f"exact Fraction; per functional, pairwise equality across the "
        f"tied candidates computed"))

    separating = sorted(n for n, eq in per_functional_equal.items() if not eq)
    separating_count = len(separating)
    ok = (separating_count == 0 and
          len(per_functional_equal) == len(EXPECTED_READ_INVENTORY))
    legs["separating_count_computed_and_enforced"] = (ok, (
        f"the count of separating functionals found on TIE_FIXTURES is "
        f"COMPUTED = {separating_count} (of {len(per_functional_equal)} "
        f"inventory functionals; gated == 0 on these fixtures), returned "
        f"as a computed value; the census's stated reach is READ_INVENTORY "
        f"(authored) at TIE_FIXTURES only -- on these constructed "
        f"count-symmetric fixtures the equalities are consequences of the "
        f"banked count-only cost applied to count-matched constructions, "
        f"executed as those consequences, not a discovery about nature"))

    # comparator-bites control: the same comparator on an off-tie pair
    A_off = _ntr._local_tie(1)[0]
    B_off = _ntr._local_tie(2)[1]
    X_off = _ntr._external(A_off, B_off, 0, 0, 1)
    eq_ctl, _, _, n_ctl, frac_ctl = _census(
        {"comparator_control": (A_off, B_off, X_off)})
    n_sep_ctl = sum(1 for eq in eq_ctl.values() if not eq)
    ok = (n_sep_ctl > 0 and n_ctl == len(READ_INVENTORY) and frac_ctl and
          _ntr._cost(A_off) != _ntr._cost(B_off))
    legs["comparator_bites_on_offtie_control"] = (ok, (
        f"the same comparator applied to an off-tie control pair "
        f"(banked-constructor sides of unequal size, unequal _cost by "
        f"value) reports {n_sep_ctl} separating functionals (gated > 0) "
        f"over {n_ctl} executed reads -- the fixture equalities come from "
        f"a comparator that CAN report difference; the control instance is "
        f"a control, outside TIE_FIXTURES, claimed as nothing but this "
        f"bite"))

    return _result(
        "check_S3a_read_separation_census", legs,
        key_result=(
            f"at every instance of TIE_FIXTURES ({len(TIE_FIXTURES)} named "
            f"banked-flat-tie instances, flat by value through the banked "
            f"machinery), every functional of READ_INVENTORY "
            f"({len(READ_INVENTORY)} banked read functionals, an authored "
            f"set-exact inventory) is executed through its home module's "
            f"own machinery by value; per functional, pairwise equality "
            f"across the tied candidates is computed; the count of "
            f"separating functionals found = {separating_count}, a "
            f"computed value; READ_INVENTORY is the census's stated reach "
            f"-- a functional outside it is outside this census"),
        dependencies=["T_nonlocal_tie_resolution",
                      "T_hold_cost_dominance_split"],
        cross_refs=["check_CF2_tie_by_value (sibling instance, disclosed; "
                    "neither is the other's content)"],
        disclosures=[
            "READ_INVENTORY and the fixture parameters are authored inputs",
            "the fixture equalities are consequences of the banked "
            "count-only cost on count-matched constructions, executed as "
            "those consequences",
            "the comparator-bites control carries the "
            "could-report-difference evidence for the equality verdicts"],
        extra={"separating_count": separating_count,
               "separating_functionals": separating,
               "per_functional_equal_on_fixtures": per_functional_equal})


# ---------------------------------------------------------------------------
# S3b -- the deficit-coupling boundary, consumed as banked
# ---------------------------------------------------------------------------

# INHERITED RED (E1@2026-08-28: sub-lemma L_cost_C1 of check_L_cost
# demoted off 'P' to a POSTULATE).  THIS CHECK HOLDS NO VIEW ABOUT
# L_cost_C1: it reddens because its proximate anchor reddened, and that
# anchor is check_T_nonlocal_tie_resolution (nonlocal_tie_resolution.py).
# The leg that reads C1's status literal is in
# check_L_selection_ledger_completeness (born_at_ties.py); this red is
# inherited from it, and a reader who counts it as a separate finding
# over-counts the corpus's damage.
# NOT to be widened, tuned green, or reverted: the predicate is
# satisfiable and clears when C1 is discharged or the anchor's
# predicate is ruled.
def check_S3b_deficit_boundary_consumed_as_banked():
    legs = {}
    fixtures = _flat_fixtures()

    r_tie = _banked_tie_record()
    ok = (r_tie.get("passed") is True and
          r_tie.get("name") == "T_nonlocal_tie_resolution" and
          r_tie.get("epistemic", "").startswith("P_structural | occupancy"))
    legs["banked_tie_check_executed_live"] = (ok, (
        f"check_T_nonlocal_tie_resolution EXECUTED LIVE and green "
        f"(passed={r_tie.get('passed')}), its grade carried as that module "
        f"states it ('{r_tie.get('epistemic', '')[:48]}...'); the two-armed "
        f"deficit-coupling boundary is that check's own content, consumed "
        f"here as banked -- this module re-derives none of it"))

    # chance arm on THIS module's instances, through the banked functions
    n_chance = n_zero_deficit = n_pos_deficit = 0
    chance_ok = True
    for fname in sorted(fixtures):
        k, A, B, X = fixtures[fname]
        jA, jB = _ntr._joint(A, X), _ntr._joint(B, X)
        dA, dB = _ntr._deficit(A, X), _ntr._deficit(B, X)
        good = (jA == jB and dA == dB and _no_float([jA, jB, dA, dB]))
        chance_ok = chance_ok and good
        n_chance += 1
        if dA == 0:
            n_zero_deficit += 1
        if dA > 0:
            n_pos_deficit += 1
    ok = chance_ok and n_chance == len(TIE_FIXTURES)
    legs["chance_arm_exercised_by_value"] = (ok, (
        f"the undecided arm exercised on all {n_chance} TIE_FIXTURES "
        f"instances through the banked module's own _joint/_deficit: "
        f"coupled costs EQUAL and deficits EQUAL per instance, as computed "
        f"Fraction value ties -- {n_zero_deficit} instance(s) at zero "
        f"deficit (disjoint coupling) and {n_pos_deficit} at positive "
        f"count-symmetric deficit, both flavors of the undecided side "
        f"executed; which-outcome at such an instance is born_at_ties' own "
        f"fenced territory, untouched here"))

    # decided arm on THIS module's instances (count-asymmetric couplings)
    n_decided = 0
    decided_ok = True
    for fname in sorted(fixtures):
        k, A, B, X = fixtures[fname]
        X_dec = _ntr._external(A, B, 1, 0, 1)   # shares 1 of A, none of B
        jA, jB = _ntr._joint(A, X_dec), _ntr._joint(B, X_dec)
        dA, dB = _ntr._deficit(A, X_dec), _ntr._deficit(B, X_dec)
        good = (jA != jB and dA != dB and
                (jB - jA) == (dA - dB) and       # per-instance value tie
                _no_float([jA, jB, dA, dB]))
        decided_ok = decided_ok and good
        n_decided += 1
    ok = decided_ok and n_decided == len(TIE_FIXTURES)
    legs["decided_arm_exercised_by_value"] = (ok, (
        f"the decided arm exercised on {n_decided} count-asymmetric "
        f"couplings of the same candidate pairs (banked _external, shares "
        f"one anchor of one side only), through the banked module's own "
        f"_joint/_deficit: coupled costs UNEQUAL and deficits UNEQUAL per "
        f"instance, with the joint gap VALUE-TIED to the deficit gap "
        f"(jB - jA == dA - dB as exact Fractions, both sides through the "
        f"banked functions) -- a per-instance computed tie, an instance of "
        f"the banked check's own Leg-2 identity, consumed not re-derived"))

    ok = (n_chance > 0 and n_decided > 0 and n_zero_deficit > 0 and
          n_pos_deficit > 0)
    legs["both_arms_nonvacuous_counts_enforced"] = (ok, (
        f"both arms non-vacuous, counts ENFORCED: {n_chance} undecided-arm "
        f"instances ({n_zero_deficit} zero-deficit, {n_pos_deficit} "
        f"positive-symmetric) and {n_decided} decided-arm instances"))

    return _result(
        "check_S3b_deficit_boundary_consumed_as_banked", legs,
        key_result=(
            f"the deficit-coupling boundary is consumed from the bank as "
            f"banked: check_T_nonlocal_tie_resolution executed live and "
            f"green, and both of its arms exercised through that module's "
            f"own _joint/_deficit on this module's instances "
            f"({n_chance} undecided, {n_decided} decided), value-tied per "
            f"instance as exact Fractions; the general biconditional is "
            f"the banked check's content, never re-derived here"),
        dependencies=["T_nonlocal_tie_resolution"],
        cross_refs=["L_selection_ledger_completeness (born_at_ties, the "
                    "banked check's own anchor; which-outcome stays its "
                    "fenced territory)"],
        disclosures=[
            "the arm exhibitions are per-instance computed values on "
            "authored instances; the two-armed conditional itself is the "
            "banked module's content, gated live",
            "the decided-arm value tie (joint gap == deficit gap) is an "
            "instance of the banked check's own Leg-2 identity, executed "
            "here per instance, not derived in generality"])


# ---------------------------------------------------------------------------
# S3c -- off ties: the separating reads are the banked cost difference
# ---------------------------------------------------------------------------

def check_S3c_off_tie_separation_redundancy():
    legs = {}
    instances = _off_tie_instances()

    n_inst = 0
    built_ok = True
    for iname in sorted(instances):
        n, A, B, X = instances[iname]
        good = (n <= N_MAX and len(A) <= N_MAX and len(B) <= N_MAX and
                _ntr._cost(A) != _ntr._cost(B) and     # off tie, by value
                A != B and
                (A & X) == frozenset() and (B & X) == frozenset())
        built_ok = built_ok and good
        n_inst += 1
    ok = built_ok and n_inst == N_MAX - 1 and n_inst > 0
    legs["off_tie_instances_constructed_banked_by_value"] = (ok, (
        f"{n_inst} off-tie instances (count enforced == N_MAX - 1 = "
        f"{N_MAX - 1}) constructed through the banked constructors at "
        f"sizes n and n+1, every executed size <= N_MAX = {N_MAX}; "
        f"off-tie verified BY VALUE through the banked _cost (unequal -- "
        f"the banked module's own unequal-options control genre: not a "
        f"tie, locally decided); couplings disjoint from both candidates "
        f"by construction, verified"))

    pairs = {iname: (A, B, X) for iname, (n, A, B, X) in instances.items()}
    per_functional_equal, values, executed, n_pairs, all_frac = _census(pairs)
    per_instance_sep = {}
    for iname in sorted(pairs):
        A, B, X = pairs[iname]
        seps = sorted(e[0] for e in READ_INVENTORY
                      if values[(iname, e[0])][0] != values[(iname, e[0])][1])
        per_instance_sep[iname] = seps
    want_sep = sorted(EXPECTED_READ_INVENTORY -
                      {"nonlocal_tie_resolution._deficit"})
    ok = (executed == EXPECTED_READ_INVENTORY and all_frac and
          n_pairs == len(READ_INVENTORY) * n_inst and
          all(seps == want_sep for seps in per_instance_sep.values()) and
          all(len(seps) > 0 for seps in per_instance_sep.values()))
    legs["census_reports_separation_off_ties"] = (ok, (
        f"the census comparator executed off ties: {n_pairs} evaluations "
        f"(enforced == inventory x instances), every read an exact "
        f"Fraction; per instance the separating set is COMPUTED (enforced "
        f"set-exactly per instance) -- the separating counts are returned "
        f"computed, values of these authored disjoint-coupling instances"))

    # the redundancy: each separating read's gap == the banked cost
    # difference, computed through the banked module's own functions
    n_ties = 0
    ties_ok = True
    per_instance_gap = {}
    for iname in sorted(pairs):
        A, B, X = pairs[iname]
        d_cost = _hcd._cost(B) - _hcd._cost(A)         # banked _cost route
        led_A = _hcd._Ledger(f"offtie_read_copy_A::{iname}")
        led_B = _hcd._Ledger(f"offtie_read_copy_B::{iname}")
        d_ledger = led_B.transition(B) - led_A.transition(A)  # banked ledger route
        per_instance_gap[iname] = d_cost
        good_inst = (d_cost == d_ledger and d_cost != 0 and
                     _no_float([d_cost, d_ledger]))
        for fname in per_instance_sep[iname]:
            vA, vB = values[(iname, fname)]
            good_inst = good_inst and ((vB - vA) == d_cost)
            n_ties += 1
        ties_ok = ties_ok and good_inst
    want_ties = sum(len(s) for s in per_instance_sep.values())
    ok = (ties_ok and n_ties == want_ties and n_ties > 0)
    legs["separation_value_tied_to_banked_cost_difference"] = (ok, (
        f"per instance, EVERY separating inventory functional's gap "
        f"(read(B) - read(A)) is COMPUTED EQUAL, as an exact Fraction "
        f"value tie, to the banked cost difference computed through the "
        f"banked module's own functions -- hold_cost_dominance's _cost "
        f"difference and, second route, the booking difference through "
        f"its own _Ledger.transition on fresh read copies (the two routes "
        f"tied to each other per instance) -- {n_ties} value ties "
        f"executed (enforced == the computed separating total "
        f"{want_ties}); a redundancy computed per instance, stated per "
        f"instance.  Same-source disclosure: for the "
        f"hold_cost_dominance._cost and ledger inventory entries the tie "
        f"repeats its own route; the cross-module content is carried by "
        f"the nonlocal_tie_resolution entries"))

    n_zero = 0
    zeros_ok = True
    for iname in sorted(pairs):
        A, B, X = pairs[iname]
        dA, dB = _ntr._deficit(A, X), _ntr._deficit(B, X)
        good = (dA == F(0) and dB == F(0))
        zeros_ok = zeros_ok and good
        n_zero += 1
    ok = zeros_ok and n_zero == n_inst
    legs["nonseparating_deficit_zero_disclosed_scope"] = (ok, (
        f"the banked _deficit computes ZERO on "
        f"both sides of all {n_zero} disjoint-coupling instances (the "
        f"banked module's own zero-deficit control genre) -- so the "
        f"redundancy statement above is SCOPED to the separating entries "
        f"of these instances, disclosed"))

    return _result(
        "check_S3c_off_tie_separation_redundancy", legs,
        key_result=(
            f"off ties, on the {n_inst} enumerated instances at "
            f"n <= N_MAX: each separating inventory functional is "
            f"computed equal, as an exact Fraction value tie, to the "
            f"banked cost difference computed through the banked module's "
            f"own functions (_cost and _Ledger.transition of "
            f"hold_cost_dominance, the two routes tied per instance) -- "
            f"{n_ties} per-instance value ties executed and enforced; a "
            f"redundancy computed per instance, stated per instance"),
        dependencies=["T_hold_cost_dominance_split",
                      "T_nonlocal_tie_resolution"],
        cross_refs=["check_CF2_tie_by_value (sibling instance, disclosed)"],
        disclosures=[
            "the off-tie instances and their disjoint couplings are "
            "authored inputs; the ties are values of authored witnesses",
            "two of the value ties are same-source (disclosed in the leg); "
            "the cross-module content rides the nonlocal_tie_resolution "
            "entries",
            "ledger bookings are read on fresh copies local to the leg; "
            "nothing is booked into any shared ledger"],
        extra={"per_instance_separating": per_instance_sep,
               "per_instance_banked_gap": {k: str(v) for k, v in
                                           per_instance_gap.items()}})


# ---------------------------------------------------------------------------
# registration (house shape, bare-name keys per D6@2026-08-03; this module
# is a build-seat scratch object wired into NO live bank)
# ---------------------------------------------------------------------------

_CHECKS = {
    "check_S3a_read_separation_census": check_S3a_read_separation_census,
    "check_S3b_deficit_boundary_consumed_as_banked":
        check_S3b_deficit_boundary_consumed_as_banked,
    "check_S3c_off_tie_separation_redundancy":
        check_S3c_off_tie_separation_redundancy,
}


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


def register(registry):
    registry.update({
        "S3a_read_separation_census": check_S3a_read_separation_census,
        "S3b_deficit_boundary_consumed_as_banked":
            check_S3b_deficit_boundary_consumed_as_banked,
        "S3c_off_tie_separation_redundancy":
            check_S3c_off_tie_separation_redundancy,
    })
    return registry


if __name__ == "__main__":
    import sys
    results = run_all()
    n_pass = sum(1 for r in results.values() if r["passed"])
    n_legs = sum(r["leg_count"] for r in results.values())
    print("tie_read_separation_census: BANKED v24.3.478 (2026-08-16) "
          "(HELD OUT OF THE BANK; nothing banks without Ethan's lift)")
    for name, r in results.items():
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {name} ({r['leg_count']} legs)")
        for reason in r["fail_reasons"]:
            print(f"      FAIL: {reason}")
    s3a = results["check_S3a_read_separation_census"]
    print(f"separating count on TIE_FIXTURES (computed, reach = "
          f"READ_INVENTORY, authored): {s3a['separating_count']}")
    print(f"{n_pass}/{len(results)} checks pass; {n_legs} legs")
    sys.exit(0 if n_pass == len(results) else 1)
