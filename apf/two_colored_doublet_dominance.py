"""two_colored_doublet_dominance.py -- the RT4(b) two-colored-doublet enumeration.

================================================================================
BANKED
================================================================================
STATUS      : banked at v24.3.480 (2026-08-28), built to the frozen claim
              surface
              `Artifacts_2026-08-28_session/build_freeze/CLAIM_SURFACE_FROZEN_2026-08-28.md`
              (raw sha256
              5f72fd9a90f40cb4188f1019fce1d21ff42cf9773885108f4f4b23383e4f2465),
              object B1.
REGISTERED  : YES. This module registers one check under the bare-name key per
              D6@2026-08-03, is listed in `apf/_module_manifest.py`, and is
              counted in `EXPECTED_REGISTRY_SIZE`.
AUDITS      : three blinded cold audits by seats that did not write it, all
              LAND-WITH-FIXES (0.84, 0.85, 0.90), two cold fix passes carrying
              their findings, and a subtractive pass.
GRADE       : `[P_structural_exhaustive]`. It may not claim `[P]`. It is a
              finite enumeration over a declared box whose cap completeness
              `check_T_field` itself declares OPEN. The sub-grade is RULED and
              is the token the check returns; the bare `P_structural` that the
              repo-root guard `check_no_bare_pstructural.py` flags is not used
              here.
DIRECTION   : MIXED, both halves declared. Adding a computed enumeration where
              `check_T_field`'s P4 leg carries a literal comparison is
              STRENGTHENING -- the self-favouring direction -- and is flagged as
              such. Re-scoping "class minimum" to "F1-F5 stratum minimum" is
              CONSERVATIVE. The two do not cancel and are not netted.
================================================================================

WHAT THIS OBJECT COMPUTES

`check_T_field`'s P4 leg (`apf/gauge.py`) executes `check(_p4_dof > 45)` where
`_p4_dof` is computed from a single hand-written witness and 45 is a literal.
Its docstring calls this an "enumeration of record". No enumeration exists
behind that phrase. This object supplies one.

It enumerates the two-colored-doublet template space at the declared caps,
applies filters F1-F5, computes the argmin, and compares the stratum minimum
against `check_T_field`'s own Phase-1 winner DOF read from that check's own
returned artifacts.

VALUE TIES -- by value, in a different module, never by verdict

  (1) Every representation constant and every filter predicate used here is
      `gauge.py`'s OWN. The `_SU3` / `_SU2` tables and the `_af` / `_ch` / `_s3`
      / `_wi` / `_an` / `_ck` helper bodies are local to `check_T_field`, so
      they are recovered by parsing `apf/gauge.py`'s source with `ast` and
      executing those exact nodes. The tables and the filter predicates are
      therefore never re-declared here. Representation constants ARE written
      locally in two places and are outside that statement: the SU(2)
      dimensions 2 and 1 inside `_NONCONJ_CONTROL`, and leg 5's
      `d2 == 2 -> '2'` identification between `gauge.py`'s two SU(2)
      conventions -- the identification L13 records as unpinned.

      DISCLOSED, and it is the reason no leg asserts table equality: because the
      tables ARE `gauge.py`'s, comparing them against a copy of themselves would
      be a leg that cannot fail, and no such leg is written. The extraction is
      instead tied end-to-end by leg `phase1_reproduction_ties_to_check_T_field`,
      which re-runs `gauge.py`'s Phase-1 scan using the extracted helpers and
      requires the winner DOF and winner template to equal the values
      `check_T_field` itself reports. A stale or mis-targeted extraction breaks
      that leg.

  (2) The Phase-1 winner DOF and the Phase-1 winner TEMPLATE are both read
      from `check_T_field()`'s own returned artifacts -- `winner_dof` and
      `winner_desc`, the latter parsed back into a template. Re-entering the
      integer 45, or the winner template, would be a defect and neither is
      done.

  (3) The 1,680-template universe is tied to `gauge.py`'s own `product`-based
      Phase-1 loop by SET EQUALITY after deduplication, not by count agreement.

EXACT ARITHMETIC

`Fraction` and integers throughout. No float is constructed anywhere in this
module, in a decision path or otherwise.

STATED LIMITATIONS

  (L1) A GENUINE INVARIANCE THIS OBJECT DOES NOT DETECT. The [SU(3)]^3 filter
       `_s3` tests `sum(A(r) * dim2) == 0`. A coordinated global sign flip of
       every SU(3) anomaly coefficient `A -> -A` leaves that predicate's verdict
       unchanged at every template, so the survivor set, the stratum minimum and
       the argmin are all invariant under it. The multi-site mutation was
       executed and ESCAPED. This is a real invariance of the quantity, not a
       gap a further leg would close. Any successor wishing to pin the
       SU(3) anomaly sign convention must tie it to a quantity that is not
       sign-even.

  (L2) THE CANONICAL-F6 RAISE IS NOT RECOMPUTED HERE. The frozen surface's
       second sentence fixes that canonical F6 RAISES on the survivors. The
       procedure that raises lives in an unaudited companion-repo standalone
       whose subsumption against `L_F6_not_from_EC` has never been swept.
       What is computed here instead is the ENGINE's own F6 predicate
       `_an`, read from `gauge.py`'s source, together with the domain fact
       that drives it. The
       raise-versus-return-False distinction is a property of the standalone's
       implementation and is consumed from the fold-in return by citation. A
       SECOND clause of that same frozen sentence is likewise not computed
       here: it fixes that BOTH total F6 variants reject all survivors, where
       this object executes ONE variant only -- `gauge.py`'s own `_an`. Both
       dropped clauses are WEAKENINGS from the frozen surface and are
       disclosed as such.

  (L3) THE LEG INVENTORY CERTIFIES EXECUTION, NOT FALSIFIABILITY. The set-exact
       inventory below records that each declared leg ran. It does not establish
       that any leg could have failed. That is a standing limit of the form, not
       a claim about this object.

  (L4) The colored-doublet count on every survivor is 2 BY CONSTRUCTION of the
       enumeration, so the half of the F6-domain record asserting `_an` rejects
       all survivors is entailed by the construction and is not an independent
       failure channel. It is paired in the same leg with the opposite direction
       -- `_an` accepting `gauge.py`'s own one-colored-doublet Phase-1 winner --
       which is NOT entailed and does carry a failure channel.

  (L5) The `VERSION_LOCK` provenance chain of the companion-repo standalone
       is not verified here.

  (L6) TWO NEAR-ENTAILED CONJUNCTS. (a) In leg
       `argmin_ties_to_gauge_p4_witness`, re-running F1-F5 on the argmin is
       entailed up to entry ordering, since the argmin was produced by those
       same predicates; it adds only order-insensitivity. (b) In leg
       `caps_non_binding_at_executed_settings`, the FIRST cap row is the
       declared setting itself, so its agreement with the stratum minimum is
       the same computation twice; rows two and three are not entailed and
       carry the leg.

  (L7) WHAT THE CONJUGATE-FAMILY LEGS PIN, AND WHAT THEY DO NOT. On a
       conjugate family the four anomaly coefficients cancel term by term for
       ANY odd functional with ANY prefactors, so the conjugate witnesses alone
       pin the ODDNESS of the U(1)^3 power and nothing else. What the
       NON-conjugate control adds is an assertion of the four coefficients at
       their exact non-zero values on one named assignment; prefactor, power
       and global-sign edits to `gauge.py`'s expressions were executed against
       it and were CAUGHT. No universal over such edits is computed. The
       control assignment is chosen so that the U(1)^3 coefficient separates
       y**3 from y**5; an assignment whose singlet hypercharges are a
       conjugate pair does not separate them.

  (L8) THE DOMINANCE COMPARISON'S STRICTNESS IS NOT PINNED. Relaxing `>` to
       `>=` in the dominance leg leaves every verdict unchanged at the executed
       margin, since the two sides are unequal there. The mutation was executed
       and ESCAPED. No leg at the executed values can distinguish the two
       operators.

  (L9) THE WINNER DOF IS READ BY CALLING `check_T_field` DIRECTLY. The frozen
       claim surface states the mechanism as a read `via the DAG`. This module
       calls `check_T_field()` and reads `artifacts['winner_dof']` from the
       returned record -- the same value produced by the same check, by a
       different route. Neither a strengthening nor a weakening; disclosed
       because the mechanism differs from the surface's wording.

  (L10) THE SUPERSET STEP IS NOT LEGGED. That the F1-F5 stratum CONTAINS the
       admissible set -- which is what makes a stratum minimum above the
       Phase-1 winner DOF say anything about admissible templates -- is the
       logical step this comparison rests on, and no leg establishes it.

  (L11) THE SURVIVOR SET IS PRE-CPT-QUOTIENT. `gauge.py`'s `_ck` quotient is
       extracted and applied only inside the Phase-1 reproduction, never to the
       two-colored-doublet survivors. The "F1-F5" label is accurate; no
       sentence of this object claims the survivor set is quotiented.

  (L12) DEVIATIONS FROM THE FROZEN SURFACE'S EXACT SENTENCE WORDING, in the
       conservative direction. (a) The surface's first sentence carries
       "SU(2) reps from {SU2_SET}". The SU(2) content of every enumerated
       template is fixed by the enumeration's construction, not read off a
       table, so presenting it as a table read would dress a construction as
       a discovery. The scope itself
       still travels inside the returned sentence, as the surface requires.
       (b) The surface's fourth sentence carries "The declared caps are
       non-binding". Three of the five declared scope dimensions are varied,
       so the sentence names those three rather than all five.
       (c) The surface's sixth sentence carries the one-colored-doublet
       figures with no attribution. Those figures are banked content, so the
       sentence now names the banked source it is tied to (see the
       subsumption note in leg 10). Conservative: it reduces what this object
       claims for itself.

  (L13) THE VALUE TIE TO gauge.py's P4 WITNESS IS BLIND TO THAT WITNESS'S
       SU(2)-SLOT AND CONJUGATION CONVENTIONS. Leg
       `argmin_ties_to_gauge_p4_witness` compares the computed argmin against
       `gauge.py`'s `_p4w` as a SORTED template. `_p4w` is a conjugate pair
       carrying identical SU(3) content in both SU(2) slots, so `sorted()`
       sends several distinct transcriptions of it to one template. Three
       multi-site convention edits were executed and ESCAPED: inverting this
       module's own `d2 == 2 -> '2'` identification; swapping `_p4w`'s
       doublet and singlet slots; and relabelling `_p4w`'s SU(3) entries
       `3 <-> 3b`. The last two are edits to the SIBLING, and both were
       executed against `check_T_field` as well and passed it in full. These
       are genuine invariances of the compared quantity, not gaps a further
       leg would close.

  (L14) LEG 12 ASSERTS NO AT-MINIMUM COUNT FOR THE REPRODUCED PHASE-1 SCAN,
       where leg 4 asserts one for the stratum. The asymmetry is recorded
       rather than closed. `check_T_field`, which this module calls, asserts
       the uniqueness of its own Phase-1 minimum itself; and the concrete
       extraction defect that would break uniqueness here -- dropping the
       `_ck` CPT quotient from the reproduction -- was executed and is
       already CAUGHT by the existing winner-template tie, because the CPT
       mirror sorts ahead of the winner.

MAY NOT BE CITED FOR -- barred by this object's own scope

  - "the class minimum over admissible templates is 54". It is the F1-F5 stratum
    minimum over the declared box.
  - "the conjugate family is anomaly-free for ANY rational (Y1, Y2)". A finite
    list of rational witnesses cannot discharge a universal over Q^2. The
    universal is not computed here and is computed nowhere in the tree.
  - "the two-colored-doublet class is excluded by dominance alone". Gauge.py's
    own F6 predicate rejects the class outright, so dominance is not the only
    exclusion in play, and an F6 domain condition is a fact about a decision
    procedure's domain, not about physics.
  - "P4 is closed", or "the enumeration of record now exists", without the
    ANY-rational half named as still open.
  - cap completeness, in any direction.
  - "3+ colored doublets is empty" unscoped. It is F1-F5, at the declared caps.
  - "F3 is a chirality filter". The executed `_ch` requires a colored doublet
    AND a colored singlet: it is a doublet-singlet CONTENT predicate.
  - anything about whether the framework's physics is correct.
  - the `VERSION_LOCK` provenance chain of the standalone.

NET EFFECT ON `check_T_field`'s P4 CLAIM: a NARROWING, not a confirmation.
"""

import ast as _ast
import inspect as _inspect
import math as _math
from fractions import Fraction
from itertools import combinations_with_replacement as _cwr
from itertools import product as _product

from apf.apf_utils import check, _result, dag_get


# ----------------------------------------------------------------------
# Declared scope of the enumeration. These are the DECLARED CAPS and they
# are load-bearing: every sentence this object returns carries them.
# ----------------------------------------------------------------------
_N_COLORED_DOUBLETS = 2
_CS_CAP = 3      # colored singlets, 0..3
_LD_CAP = 1      # lepton doublets, 0..1
_LS_CAP = 2      # lepton singlets, 0..2

# Cap settings executed for the non-bindingness evidence: (cs, ld, ls).
_CAP_SETTINGS = ((3, 1, 2), (5, 1, 4), (7, 2, 6))

# Rational hypercharge assignments (Y1, Y2) at which anomaly freedom of the
# conjugate family is EXECUTED. A finite witness list, not a universal.
_Y_WITNESSES = (
    (Fraction(1), Fraction(2)),
    (Fraction(3, 7), Fraction(-5, 2)),
    (Fraction(1, 6), Fraction(11)),
)

# Doublet-count sweep range beyond the two-doublet class.
_DEAD_RANGE = (3, 4, 5, 6, 7)

_DECLARED_LEGS = frozenset({
    'enumeration_population_set_exact',
    'closed_form_population_cross_check',
    'f1_f5_survivor_set_exact',
    'argmin_dof_and_template',
    'argmin_ties_to_gauge_p4_witness',
    'dominance_over_computed_winner_dof',
    'caps_non_binding_at_executed_settings',
    'anomaly_freedom_at_rational_witnesses',
    'f6_domain_record_both_directions',
    'doublet_count_sweep',
    'universe_ties_to_gauge_phase1_dedup',
    'phase1_reproduction_ties_to_check_T_field',
})


# ----------------------------------------------------------------------
# Recovery of gauge.py's OWN representation tables and filter predicates.
# They are locals of `check_T_field`, so they are read out of that
# function's source and executed. Nothing below re-declares them.
# ----------------------------------------------------------------------

_TABLE_NAMES = ('_SU3', '_SU2', '_cr', '_AF3', '_AF2', '_c23')
_HELPER_NAMES = ('_af', '_ch', '_s3', '_wi', '_an', '_ck')
# gauge.py's OWN P4 quantities, computed by it for its own witness. They are
# extracted so this module can assert equality on the computed values instead
# of pinning literals of its own.
_P4_NAMES = ('_p4_dof', '_p4_b3', '_p4_b2',
             '_p4_a2u1', '_p4_a3u1', '_p4_gru1', '_p4_u1c')
# The four anomaly-coefficient assignments, kept as nodes so gauge.py's own
# expressions can be re-executed at assignments other than its own witness.
_ANOM_NAMES = ('_p4_a2u1', '_p4_a3u1', '_p4_gru1', '_p4_u1c')

# A NON-conjugate control assignment. Its role is to pin the prefactors, the
# powers and the signs of gauge.py's anomaly expressions, which the conjugate
# witnesses cannot do (see L7). Chosen so the U(1)^3 coefficient separates a
# cubic from a quintic; a control whose singlet hypercharges form a conjugate
# pair does not separate them.
_NONCONJ_CONTROL = (('3', 2, Fraction(1)), ('3b', 2, Fraction(1)),
                    ('3', 1, Fraction(2)), ('3b', 1, Fraction(3)))
_NONCONJ_EXPECTED = (Fraction(3), Fraction(9, 2),
                     Fraction(27), Fraction(117))


def _gauge_locals():
    """Execute gauge.py's own check_T_field-local tables and helpers.

    Returns a namespace carrying `gauge.py`'s representation tables and its
    filter predicates as it actually defines them. Fails if any expected name
    is absent, so a rename upstream surfaces as a failure rather than as a
    silent fallback to a re-declared constant.
    """
    from apf import gauge as _gauge

    src = _inspect.getsource(_gauge.check_T_field)
    wrapped = "if 1:\n" + "\n".join("    " + ln for ln in src.splitlines())
    fn_node = _ast.parse(wrapped).body[0].body[0]

    nodes = {}
    for node in fn_node.body:
        if isinstance(node, _ast.Assign) and isinstance(node.targets[0], _ast.Name):
            nodes.setdefault(node.targets[0].id, node)
        elif isinstance(node, _ast.FunctionDef):
            nodes.setdefault(node.name, node)

    wanted = _TABLE_NAMES + _HELPER_NAMES + ('_p4w',) + _P4_NAMES
    absent = [n for n in wanted if n not in nodes]
    check(not absent,
          f"gauge.py's check_T_field no longer defines: {sorted(absent)}")

    ns = {'Fraction': Fraction, '_math': _math}
    for name in _TABLE_NAMES:
        exec(compile(_ast.Module(body=[nodes[name]], type_ignores=[]),
                     '<gauge.check_T_field>', 'exec'), ns)
    # N_gen is read the way gauge.py reads it, so a change propagates to both.
    ns['Ng'] = dag_get('N_gen', default=3,
                       consumer='T_two_colored_doublet_class_dominance')
    for name in _HELPER_NAMES + ('_p4w',) + _P4_NAMES:
        exec(compile(_ast.Module(body=[nodes[name]], type_ignores=[]),
                     '<gauge.check_T_field>', 'exec'), ns)
    ns['_anom_nodes'] = tuple(nodes[n] for n in _ANOM_NAMES)
    return ns


def _dof(t, ns):
    """Weyl DOF of a template, through gauge.py's own dimension tables."""
    return sum(ns['_SU3'][a]['dim'] * ns['_SU2'][b]['dim']
               for a, b in t) * ns['Ng']


def _passes_f1_to_f5(t, ns):
    """F1-F5: AF(SU3), AF(SU2), doublet-singlet content, [SU(3)]^3, Witten.

    `_af` carries F1 and F2 jointly, exactly as gauge.py's Phase-1 scan does.
    F3 is the doublet-singlet CONTENT predicate; it is not a chirality test.
    """
    return ns['_af'](t) and ns['_ch'](t) and ns['_s3'](t) and ns['_wi'](t)


def _enumerate(ns, n_cd, cs_cap, ld_cap, ls_cap):
    """Enumerate the n_cd-colored-doublet space at the given caps.

    Returns (population, survivors) with survivors sorted by (dof, template),
    each template a sorted tuple so that the survivor SET is comparable.
    """
    population = 0
    survivors = []
    for cds in _cwr(ns['_cr'], n_cd):
        for n_cs in range(0, cs_cap + 1):
            for css in _cwr(ns['_cr'], n_cs):
                for n_ld in range(0, ld_cap + 1):
                    for n_ls in range(0, ls_cap + 1):
                        t = tuple(
                            [(c, '2') for c in cds]
                            + [(c, '1') for c in css]
                            + [('1', '2')] * n_ld
                            + [('1', '1')] * n_ls
                        )
                        population += 1
                        if not _passes_f1_to_f5(t, ns):
                            continue
                        survivors.append((_dof(t, ns), tuple(sorted(t))))
    survivors.sort()
    return population, survivors


def _gauge_anomaly_system(assignment, ns):
    """The four anomaly coefficients, through gauge.py's OWN expressions.

    `gauge.py` binds these four coefficients to its single witness `_p4w`.
    The same assignment nodes are re-executed here with `_p4w` rebound to
    `assignment`, so the prefactors, the powers and the signs are `gauge.py`'s.
    Nothing here re-declares the anomaly functional.

    `assignment` is a sequence of (su3_rep, su2_dim, Y). Returns
    ([SU(2)]^2 U(1), [SU(3)]^2 U(1), grav^2 U(1), U(1)^3).
    """
    local = {'Fraction': Fraction, '_math': _math,
             '_SU3': ns['_SU3'], '_p4w': list(assignment)}
    for node in ns['_anom_nodes']:
        exec(compile(_ast.Module(body=[node], type_ignores=[]),
                     '<gauge.check_T_field>', 'exec'), local)
    return tuple(local[n] for n in _ANOM_NAMES)


def _parse_template_desc(desc):
    """Parse check_T_field's own `winner_desc` string into a sorted template.

    `gauge.py` builds it as '+'.join(f'({a},{b})' for a, b in w_t) from the
    winner template itself, so parsing it recovers that template rather than
    re-entering one here.
    """
    entries = []
    for part in desc.split('+'):
        part = part.strip()
        check(part.startswith('(') and part.endswith(')')
              and part.count(',') == 1,
              f"check_T_field's winner_desc entry is not a parenthesised "
              f"pair: {part!r}")
        a, b = part[1:-1].split(',')
        entries.append((a.strip(), b.strip()))
    return tuple(sorted(entries))


def _gauge_phase1(ns):
    """Re-run gauge.py's own Phase-1 scan with the extracted helpers.

    Mirrors `check_T_field`'s `product`-based ordered loop exactly. Returns
    (tested_ordered, distinct_universe_set, survivors_sorted).
    """
    tested = 0
    universe = set()
    survivors = []
    seen = set()
    for cd in ns['_cr']:
        for n_c in range(0, 4):
            for cc in _product(ns['_cr'], repeat=n_c):
                cs = tuple(sorted(cc))
                for hl in (True, False):
                    for n_l in range(0, 3):
                        t = [(cd, '2')] + [(c, '1') for c in cs]
                        if hl:
                            t.append(('1', '2'))
                        t.extend([('1', '1')] * n_l)
                        t = tuple(t)
                        tested += 1
                        universe.add(tuple(sorted(t)))
                        if not ns['_af'](t):
                            continue
                        if not ns['_ch'](t):
                            continue
                        if not ns['_s3'](t):
                            continue
                        if not ns['_wi'](t):
                            continue
                        if not ns['_an'](t):
                            continue
                        ck = ns['_ck'](t)
                        if ck in seen:
                            continue
                        seen.add(ck)
                        survivors.append((_dof(t, ns), tuple(sorted(t))))
    survivors.sort()
    return tested, universe, survivors


def _closed_form_population(n_cd, cs_cap, ld_cap, ls_cap, n_reps):
    """Independent closed-form count of the enumerated population.

    multiset(n_reps, n_cd) * sum_k multiset(n_reps, k) * (ld_cap+1) * (ls_cap+1),
    computed from binomials rather than by counting the loop's iterations.
    """
    def multiset(n, k):
        return _math.comb(n + k - 1, k)
    doublet_choices = multiset(n_reps, n_cd)
    singlet_choices = sum(multiset(n_reps, k) for k in range(0, cs_cap + 1))
    return doublet_choices * singlet_choices * (ld_cap + 1) * (ls_cap + 1)


def check_T_two_colored_doublet_class_dominance():
    """T_two_colored_doublet_class_dominance [P_structural_exhaustive].

    The two-colored-doublet enumeration standing behind `check_T_field`'s P4
    claim. Computes the F1-F5 stratum minimum over the declared box and
    compares it against `check_T_field`'s own computed Phase-1 winner DOF.

    See the module docstring for the banner, the stated limitations,
    and the MAY-NOT-CITE list.
    """
    legs_run = set()
    fails = []

    ns = _gauge_locals()
    n_reps = len(ns['_cr'])

    # -- Leg 1: the enumerated population, set-exact ----------------------
    population, survivors = _enumerate(
        ns, _N_COLORED_DOUBLETS, _CS_CAP, _LD_CAP, _LS_CAP)
    legs_run.add('enumeration_population_set_exact')
    check(population == 5040,
          f"enumerated population must be 5040, got {population}")

    # -- Leg 2: independent closed-form cross-check of that population ----
    legs_run.add('closed_form_population_cross_check')
    closed = _closed_form_population(
        _N_COLORED_DOUBLETS, _CS_CAP, _LD_CAP, _LS_CAP, n_reps)
    check(closed == population,
          f"closed-form population {closed} != enumerated {population}")

    # -- Leg 3: the F1-F5 survivor SET, exactly ---------------------------
    legs_run.add('f1_f5_survivor_set_exact')
    survivor_set = frozenset(t for _, t in survivors)
    expected_survivors = frozenset({
        (('3', '1'), ('3', '2'), ('3b', '1'), ('3b', '2')),
        (('1', '1'), ('3', '1'), ('3', '2'), ('3b', '1'), ('3b', '2')),
        (('1', '1'), ('1', '1'), ('3', '1'), ('3', '2'),
         ('3b', '1'), ('3b', '2')),
        (('3', '2'), ('3b', '2'), ('8', '1')),
        (('1', '1'), ('3', '2'), ('3b', '2'), ('8', '1')),
        (('1', '1'), ('1', '1'), ('3', '2'), ('3b', '2'), ('8', '1')),
    })
    check(survivor_set == expected_survivors,
          f"F1-F5 survivor set moved: "
          f"unexpected={sorted(survivor_set - expected_survivors)} "
          f"missing={sorted(expected_survivors - survivor_set)}")
    dof_multiset = sorted(d for d, _ in survivors)
    check(dof_multiset == [54, 57, 60, 60, 63, 66],
          f"F1-F5 survivor DOF multiset moved: {dof_multiset}")

    # -- Leg 4: the argmin, DOF and template ------------------------------
    legs_run.add('argmin_dof_and_template')
    min_dof, argmin_template = survivors[0]
    at_min = [s for s in survivors if s[0] == min_dof]
    check(len(at_min) == 1,
          f"stratum minimum is not attained uniquely: {len(at_min)} templates")
    check(min_dof == ns['_p4_dof'],
          f"stratum minimum {min_dof} != the witness DOF gauge.py computes "
          f"for its own P4 witness ({ns['_p4_dof']})")
    check(argmin_template == (('3', '1'), ('3', '2'), ('3b', '1'), ('3b', '2')),
          f"argmin template moved: {argmin_template}")

    # -- Leg 5: the argmin IS gauge.py's own P4 witness, by value ---------
    legs_run.add('argmin_ties_to_gauge_p4_witness')
    p4w = ns['_p4w']
    p4w_template = tuple(sorted(
        (r3, '2' if d2 == 2 else '1') for r3, d2, _ in p4w))
    check(argmin_template == p4w_template,
          f"computed argmin {argmin_template} != gauge.py's P4 witness "
          f"{p4w_template}")
    b3 = ns['_AF3'] - ns['_c23'] * sum(
        ns['_SU3'][a]['T'] * ns['_SU2'][b]['dim']
        for a, b in argmin_template) * ns['Ng']
    b2 = ns['_AF2'] - ns['_c23'] * sum(
        ns['_SU2'][b]['T'] * ns['_SU3'][a]['dim']
        for a, b in argmin_template) * ns['Ng']
    check(b3 == ns['_p4_b3'] and b2 == ns['_p4_b2'],
          f"argmin AF coefficients (b3={b3}, b2={b2}) disagree with the ones "
          f"gauge.py computes for its own P4 witness "
          f"(b3={ns['_p4_b3']}, b2={ns['_p4_b2']})")
    # DISCLOSED (L6): the argmin was produced BY these predicates, so this
    # conjunct is entailed up to the ordering of the template's entries. What
    # it adds is only that the four predicates agree on the sorted tuple as
    check(ns['_s3'](argmin_template) and ns['_wi'](argmin_template)
          and ns['_ch'](argmin_template) and ns['_af'](argmin_template),
          "argmin must pass F1-F5 through gauge.py's own predicates")

    # -- Leg 6: dominance, both sides COMPUTED ----------------------------
    legs_run.add('dominance_over_computed_winner_dof')
    from apf import gauge as _gauge
    t_field = _gauge.check_T_field()
    winner_dof = t_field['artifacts']['winner_dof']
    check(min_dof > winner_dof,
          f"stratum minimum {min_dof} does not dominate the Phase-1 winner "
          f"DOF {winner_dof}")

    # -- Leg 7: the declared caps are non-binding at the executed settings
    legs_run.add('caps_non_binding_at_executed_settings')
    cap_rows = []
    for cs_cap, ld_cap, ls_cap in _CAP_SETTINGS:
        pop_c, surv_c = _enumerate(
            ns, _N_COLORED_DOUBLETS, cs_cap, ld_cap, ls_cap)
        cap_rows.append(
            (cs_cap, ld_cap, ls_cap, pop_c, len(surv_c), surv_c[0][0]))
    check([r[4] for r in cap_rows] == [6, 25, 56],
          f"cap-setting survivor counts moved: {[r[4] for r in cap_rows]}")
    check(all(r[5] == min_dof for r in cap_rows),
          f"stratum minimum is not stable across the executed cap settings: "
          f"{[r[5] for r in cap_rows]}")

    # -- Leg 8: anomaly freedom at the executed rational witnesses --------
    legs_run.add('anomaly_freedom_at_rational_witnesses')
    zero4 = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    check(len(_Y_WITNESSES) == 3,
          f"the declared hypercharge witness family moved: "
          f"{len(_Y_WITNESSES)} assignments")
    for y1, y2 in _Y_WITNESSES:
        assignment = [('3', 2, y1), ('3b', 2, -y1),
                      ('3', 1, y2), ('3b', 1, -y2)]
        coeffs = _gauge_anomaly_system(assignment, ns)
        check(coeffs == zero4,
              f"anomaly system does not vanish at (Y1,Y2)=({y1},{y2}): "
              f"{coeffs}")
    # The control. On a conjugate family every odd functional cancels term by
    # term, so the legs above pin only the oddness of the U(1)^3 power (L7).
    # What pins the prefactors, the powers and the signs is the exact value
    # gauge.py's own expressions return on a NON-conjugate assignment.
    nonconj_coeffs = _gauge_anomaly_system(_NONCONJ_CONTROL, ns)
    check(nonconj_coeffs == _NONCONJ_EXPECTED,
          f"gauge.py's anomaly expressions moved on the non-conjugate "
          f"control: got {tuple(str(c) for c in nonconj_coeffs)}, expected "
          f"{tuple(str(c) for c in _NONCONJ_EXPECTED)}")

    # -- Leg 9: the F6 domain record, in BOTH directions ------------------
    legs_run.add('f6_domain_record_both_directions')
    cd_counts = [sum(1 for a, b in t
                     if ns['_SU3'][a]['dim'] > 1 and b == '2')
                 for t in survivor_set]
    check(set(cd_counts) == {2},
          f"survivors do not all carry two colored doublets: "
          f"{sorted(set(cd_counts))}")
    check(all(ns['_an'](t) is False for t in survivor_set),
          "gauge.py's own F6 predicate does not reject every survivor")
    # The direction NOT entailed by the construction: gauge.py's F6 predicate
    # ACCEPTS its own one-colored-doublet Phase-1 winner.
    winner_template = _parse_template_desc(
        t_field['artifacts']['winner_desc'])
    check(ns['_an'](winner_template) is True,
          "gauge.py's F6 predicate rejects its own Phase-1 winner; the "
          "rejection of the two-doublet class would then carry no information")

    # -- Leg 10: the doublet-count sweep ----------------------------------
    legs_run.add('doublet_count_sweep')
    _, surv_one = _enumerate(ns, 1, _CS_CAP, _LD_CAP, _LS_CAP)
    # PARTIAL SUBSUMPTION, consumed by value rather than re-proved. The
    # one-colored-doublet survivor count and minimum are banked content --
    # `L_F6_not_from_EC` clause 1, over the check_T_field Phase-1 scan space
    # whose identity with this enumeration leg 11 asserts by set equality --
    # so they are read from that check's own returned scan artifacts instead of
    # being pinned as literals here. The frozen surface's subsumption sweep
    # asked whether anything banked computes a TWO-colored-doublet
    # enumeration; it does not, and that answer stands. The ONE-doublet half
    # of this leg is the part that was already banked.
    from apf import ec_inventory_reading as _ec
    _banked_scan = _ec.check_L_F6_not_from_EC()['artifacts']['scan']
    check(len(surv_one) == _banked_scan['f1_f5_survivors'],
          f"one-colored-doublet F1-F5 survivor count {len(surv_one)} != the "
          f"count banked L_F6_not_from_EC clause 1 computes "
          f"({_banked_scan['f1_f5_survivors']})")
    check(surv_one[0][0] == min(_banked_scan['survivor_dofs']),
          f"one-colored-doublet F1-F5 minimum {surv_one[0][0]} != the minimum "
          f"of the DOF multiset banked L_F6_not_from_EC clause 1 computes "
          f"({min(_banked_scan['survivor_dofs'])})")
    check(_DEAD_RANGE == (3, 4, 5, 6, 7),
          f"the declared doublet-count sweep moved: {_DEAD_RANGE}")
    dead_counts = []
    for n_cd in _DEAD_RANGE:
        _, surv_n = _enumerate(ns, n_cd, _CS_CAP, _LD_CAP, _LS_CAP)
        dead_counts.append(len(surv_n))
    check(dead_counts == [0] * len(_DEAD_RANGE),
          f"the 3+-colored-doublet region is not empty at F1-F5: {dead_counts}")

    # -- Leg 11: the universe ties to gauge.py's own Phase-1 loop ---------
    legs_run.add('universe_ties_to_gauge_phase1_dedup')
    tested_ordered, gauge_universe, gauge_survivors = _gauge_phase1(ns)
    own_universe = set()
    for cds in _cwr(ns['_cr'], 1):
        for n_cs in range(0, _CS_CAP + 1):
            for css in _cwr(ns['_cr'], n_cs):
                for n_ld in range(0, _LD_CAP + 1):
                    for n_ls in range(0, _LS_CAP + 1):
                        own_universe.add(tuple(sorted(
                            [(c, '2') for c in cds]
                            + [(c, '1') for c in css]
                            + [('1', '2')] * n_ld
                            + [('1', '1')] * n_ls)))
    check(own_universe == gauge_universe,
          f"universe set mismatch: this module's multiset enumeration and "
          f"gauge.py's ordered Phase-1 loop deduplicate to different sets "
          f"({len(own_universe)} vs {len(gauge_universe)})")
    check(tested_ordered == t_field['artifacts']['phase1_scanned'],
          f"ordered Phase-1 count {tested_ordered} != the count "
          f"check_T_field reports ({t_field['artifacts']['phase1_scanned']})")

    # -- Leg 12: the extraction reproduces check_T_field's own Phase-1 ----
    legs_run.add('phase1_reproduction_ties_to_check_T_field')
    check(len(gauge_survivors) >= 1,
          "the reproduced Phase-1 scan found no survivor")
    repro_dof, repro_template = gauge_survivors[0]
    check(repro_dof == winner_dof,
          f"reproduced Phase-1 winner DOF {repro_dof} != the DOF "
          f"check_T_field reports ({winner_dof})")
    check(repro_template == winner_template,
          f"reproduced Phase-1 winner template {repro_template} != "
          f"{winner_template}")

    # -- leg inventory: APPEND AND RECORD, never raise ---------------------
    missing = _DECLARED_LEGS - legs_run
    unexpected = legs_run - _DECLARED_LEGS
    if missing or unexpected:
        fails.append(
            f"leg inventory mismatch: missing={sorted(missing)}, "
            f"unexpected={sorted(unexpected)}")

    # ------------------------------------------------------------------
    # The returned record. Every load-bearing figure is computed here.
    # ------------------------------------------------------------------
    cap_table = '; '.join(
        f"(cs<={r[0]}, ld<={r[1]}, ls<={r[2]}: pop {r[3]})" for r in cap_rows)
    surv_counts = ', '.join(str(r[4]) for r in cap_rows)
    y_list = ', '.join(f"(Y1={y1}, Y2={y2})" for y1, y2 in _Y_WITNESSES)
    argmin_name = '+'.join(f"({a},{b})" for a, b in argmin_template)

    s1 = (f"Over the two-colored-doublet space at the declared caps -- colored "
          f"singlets 0-{_CS_CAP}, lepton doublets 0-{_LD_CAP}, lepton singlets "
          f"0-{_LS_CAP}, SU(3) reps from {sorted(ns['_cr'])}, SU(2) content "
          f"fixed by the enumeration's construction to one doublet or one "
          f"singlet per entry, N_gen fixed at {ns['Ng']} -- the enumerated "
          f"population is {population} templates, of which {len(survivors)} "
          f"survive filters F1-F5. The minimum DOF over those survivors is "
          f"{min_dof}, "
          f"attained at the conjugate-pair template {argmin_name}.")

    s2 = (f"{min_dof} is a minimum over the F1-F5 STRATUM of the declared box. "
          f"It is not a minimum over admissible templates: gauge.py's own F6 "
          f"predicate returns False on all {len(survivors)} survivors, each of "
          f"which carries {sorted(set(cd_counts))[0]} colored doublets. "
          f"DISCLOSED WEAKENING: "
          f"the companion standalone's canonical F6 procedure RAISES rather "
          f"than returning False on this class; that behaviour is consumed "
          f"from the fold-in return by citation and is NOT recomputed here.")

    s3 = (f"Dominance over the Phase-1 winner is computed on both sides: the "
          f"stratum minimum {min_dof} exceeds the winner DOF {winner_dof}, "
          f"which is read from check_T_field's own Phase-1 result and is not "
          f"re-entered here.")

    s4 = (f"The three varied caps -- colored singlets, lepton doublets and "
          f"lepton singlets -- are non-binding for this statement at the "
          f"{len(cap_rows)} settings executed: at {cap_table} the F1-F5 "
          f"survivor counts are {surv_counts} and the stratum minimum is "
          f"unchanged at {min_dof}. This is evidence at {len(cap_rows)} "
          f"settings. It is not a proof of cap completeness, which "
          f"check_T_field declares OPEN.")

    s5 = (f"Anomaly freedom of the conjugate family is executed at "
          f"{len(_Y_WITNESSES)} rational hypercharge assignments {y_list}. "
          f"The universal over Q^2 is not computed here.")

    s6 = (f"At the declared caps, n_colored_doublets in {list(_DEAD_RANGE)} "
          f"yields {sum(dead_counts)} F1-F5 survivors; n_colored_doublets = 1 "
          f"yields {len(surv_one)} survivors with minimum {surv_one[0][0]}, "
          f"these last two figures being banked content (L_F6_not_from_EC "
          f"clause 1) tied here to that check's own returned values rather "
          f"than claimed as new.")

    out = _result(
        name=('T_two_colored_doublet_class_dominance: the F1-F5 stratum '
              'minimum of the two-colored-doublet class'),
        tier=3,
        epistemic='P_structural_exhaustive',
        summary=' '.join([s1, s2, s3, s4, s5, s6]),
        key_result=(
            f"F1-F5 stratum minimum {min_dof} over {population} enumerated "
            f"two-colored-doublet templates ({len(survivors)} survivors) "
            f"dominates check_T_field's computed Phase-1 winner DOF "
            f"{winner_dof}; the stratum scope and the cap scope are "
            f"load-bearing and travel with the number"),
        dependencies=[],
        cross_refs=['T_field', 'L_F6_not_from_EC', 'L_EC_inventory_reading'],
        artifacts={
            'held_out_of_bank': False,
            'population': population,
            'population_closed_form': closed,
            'n_survivors_f1_f5': len(survivors),
            'survivor_dof_multiset': dof_multiset,
            'stratum_minimum': min_dof,
            'argmin_template': argmin_name,
            'winner_dof_read_from_T_field': winner_dof,
            'winner_template_read_from_T_field': t_field['artifacts'][
                'winner_desc'],
            'dominance_margin': min_dof - winner_dof,
            'nonconjugate_control_coefficients': [
                str(c) for c in nonconj_coeffs],
            'cap_settings_executed': [list(r) for r in cap_rows],
            'y_witnesses_executed': [(str(a), str(b)) for a, b in _Y_WITNESSES],
            'one_doublet_survivors': len(surv_one),
            'one_doublet_minimum': surv_one[0][0],
            'dead_range': list(_DEAD_RANGE),
            'dead_range_survivor_counts': dead_counts,
            'phase1_ordered_count': tested_ordered,
            'phase1_distinct_universe': len(gauge_universe),
            'legs_declared': sorted(_DECLARED_LEGS),
            'legs_executed': sorted(legs_run),
            'stated_limitations': [
                'L1 a global SU(3) anomaly-coefficient sign flip A -> -A is a '
                'genuine invariance of the [SU(3)]^3 predicate; the multi-site '
                'mutation was executed and ESCAPED',
                'L2 two clauses of the frozen second sentence are not '
                'computed here -- disclosed weakenings',
                'L3 the leg inventory certifies execution, not falsifiability',
                'L4 the colored-doublet count of 2 on every survivor is '
                'entailed by the construction; the paired opposite direction '
                'is not',
                'L5 the standalone VERSION_LOCK provenance chain is unverified',
                'L6 two near-entailed conjuncts disclosed in-module: the '
                'argmin F1-F5 re-run and the first cap row',
                'L7 the conjugate-family legs pin only the oddness of the '
                'U(1)^3 power; the non-conjugate control pins the prefactors, '
                'the powers and the signs by exact value',
                'L8 the strictness of the dominance comparison is unpinned at '
                'the executed margin; the > -> >= mutation was executed and '
                'ESCAPED',
                'L9 the winner DOF is read by calling check_T_field directly '
                'rather than via the DAG -- same value, same producing check, '
                'different route',
                'L10 no leg establishes that the F1-F5 stratum contains the '
                'admissible set; the step lives in the reader',
                'L11 the survivor set is pre-CPT-quotient; _ck is applied only '
                'in the Phase-1 reproduction',
                'L12 three disclosed deviations from the frozen surface '
                'wording: the SU(2) scope is stated as construction-fixed '
                'rather than as a table read, the cap sentence names the '
                'three varied caps rather than all five declared dimensions, '
                'and the one-doublet sentence names the banked source it is '
                'tied to',
                'L13 the value tie to gauge.py\'s P4 witness is blind to that '
                'witness\'s SU(2)-slot and conjugation conventions; three '
                'multi-site convention edits, two of them to the sibling, '
                'were executed and ESCAPED, and the two sibling edits pass '
                'check_T_field in full',
                'L14 leg 12 asserts no at-minimum count for the reproduced '
                'Phase-1 scan; the asymmetry with leg 4 is recorded rather '
                'than closed, no conjunct having been shown able to fail',
            ],
        },
        imported_theorems={},
    )
    if fails:
        out['passed'] = False
        out['status'] = 'FAIL'
        out['fail_reasons'] = fails
    return out


_CHECKS = {
    'T_two_colored_doublet_class_dominance':
        check_T_two_colored_doublet_class_dominance,
}


def register(registry):
    """LIVE. The hold is lifted; this module registers one check under the
    bare-name key per D6@2026-08-03. The landing rewire is hold-state text
    and registration only; no check's executable content reads a hold flag."""
    registry.update(_CHECKS)
    return registry



if __name__ == '__main__':
    import json as _json
    _r = check_T_two_colored_doublet_class_dominance()
    print(_json.dumps({k: v for k, v in _r.items() if k != 'artifacts'},
                      indent=2, default=str))
    print(_json.dumps(_r['artifacts'], indent=2, default=str))
