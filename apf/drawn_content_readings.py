"""The drawn-content -> readings functional, v0.4 (banked v24.3.328 at v0.1;
v0.2 added the Yu-Oh discharge, the mixed-word census, and the magic-square
rigidity certificate; v0.3 applied the functional to the bank's own V_61 --
the generation index as multiplicity space; v0.4 extends the alphabet with
the adjoint (gluon), lands the gluonic census, and runs the coverage sweep,
whose first genuine honest-open content -- SU(2) five-quark-three-gluon --
is pinned below).

The open object named in interface_readout_adapter.py (v24.3.306): "the
drawn-content -> readings functional remains open. READOUT inputs are SUBMITTED
... the live atlas does not auto-generate rep-content payloads." This module is
the generative half: a computed map from banked rep content (a colour-interface
spec: SU(N), an ordered word over fund / antifund / adjoint) to the full
family of IE readings that content supports -- auto-generated, engine-routed,
exact.

WHAT THE FUNCTIONAL COMPUTES (all exact integer/rational arithmetic, no numpy):

  1. The full isotypic decomposition of the word by iterated exact
     tensor-product rules (SU(2): doubled-spin Clebsch-Gordan; SU(3): Dynkin
     (p,q) branching), hence the complete commutant profile
     C = (+)_i M_{n_i} -- not just the singlet multiplicity the .306 axis
     reads, but every block.

  2. The block-graded reading ladder, each rung at exactly its certifiable
     strength:
       * all n_i = 1  -> ABELIAN_SEP: the gauge-invariant algebra is abelian;
         every context commutes; a global section exists (the banked m=1
         meson case).
       * max n_i = 2  -> GLEASON_DIM2_FENCE: no Kochen-Specker obstruction is
         possible in a 2-dim multiplicity space (the KS dimension bound,
         dim >= 3; "Gleason" is the customary shorthand); emitting no
         contextuality claim here is theorem-backed, not caution.
       * some n_i >= 3 -> KCBS_STATE_DEPENDENT: the exact rational KCBS
         pentagon realizes inside a 3-dim subspace of the M_{n_i} block
         (projectors extended by 0, state supported in the subspace --
         realizability needs no unitality), the banked M_3 pattern
         generalized to every block of size >= 3.
       * some n_i >= 4 -> MAGIC_SQUARE_STATE_DEPENDENT: the Mermin-Peres
         marginals realize on a 4-dim subspace with subspace-supported states.
       * some n_i with 3 | n_i (n_i >= 3) -> YU_OH_STATE_INDEPENDENT: the
         unital embedding M_3 (x) I_{n_i/3} c= M_{n_i} carries the banked
         Yu-Oh 13-ray set (P (x) I); every block state reduces to a qutrit
         state on the M_3 factor, and every qutrit state violates the Yu-Oh
         noncontextuality inequality -- state-independence in the INEQUALITY
         sense (the 13-ray graph itself is {0,1}-colorable; the strength is
         that the no-choice maximally-mixed point already violates; the
         routed mm-table itself certifies that point alone -- I_n/n reduces
         exactly to I_3/3 -- independent of the every-state clause), exactly
         the banked semantics of
         check_T_gauge_invariant_colour_interface_state_independent_contextual.
       * some n_i with 4 | n_i -> MAGIC_SQUARE_STATE_INDEPENDENT: the unital
         embedding M_4 (x) I_{n_i/4} c= M_{n_i} extends each of the nine +-1
         observables as O (x) I, so every context product is +-1 of the WHOLE
         block -- the state-independent PARITY (coloring-impossibility)
         obstruction, certified by the GF(2) certificate (ks_parity_decide),
         strictly stronger in kind than the inequality sense. Block-scoped:
         the +-1 products are scalars of that M_{n_i} corner, not of the full
         commutant -- the same scoping as the banked M_4 certificates.
         Hostability of this rung is INVARIANT, not construction-relative:
         see check_T_magic_square_solution_group_rep_forces_4n below (any
         operator solution with the parity relations forces 4 | n, certified
         at the finite-group level with one named cited step).

  3. Auto-instantiated scenarios for the classes present, routed through the
     live IE pipeline (route_contextuality -> interface_atlas.summarize_input)
     for first-class engine verdicts. The scenarios are the bank's own
     canonical objects (the exact rational KCBS pentagon; the Yu-Oh 13-ray
     set; the Mermin-Peres magic square); what is NEW is that the functional
     derives WHICH of them a given rep content hosts, from the content alone.

THE CENSUS RESULTS (pins in the check; v0.2 extends v0.1 with the Yu-Oh rung
and the mixed-word surface):

  PAIRS ((fund antifund)^m, m <= 5). The v0.1 slogan-correction stands: the
  block-graded form replaces "every m>=2 multi-pair sector hosts an M_4".
  With the Yu-Oh rung discharged, the v0.1 headline ordering DISSOLVES at
  class-agnostic strength: BOTH groups reach state-independent contextuality
  at m=2 (SU(2) via Yu-Oh on the 3-block; SU(3) via parity on the 4-block),
  and state-independence is PERSISTENT for m in 2..5 in both groups. What
  remains true -- and is pinned -- is that EACH CLASS FLICKERS while the
  union does not: the two certificate families take turns covering. The two
  flickers are NOT symmetric in kind: a parity off-cell is an INVARIANT
  absence (4|n is what parity hostability means -- the rigidity check below),
  while a Yu-Oh off-cell is CONSTRUCTION-RELATIVE (nothing certifies that
  inequality-sense state-independence requires 3|n; un-instantiated
  certificates may cover those cells -- fence iv). Read the parity row as
  physics, the Yu-Oh row as the reach of this module's lift.
    SU(2) parity class: hosted at m=4 ONLY (off at m=5: [90,75,42,35,9,1]
      has no 4|n block); Yu-Oh class: m=2,3,5 but OFF at m=4 ([28,20,14,7,1]
      has no 3|n block).
    SU(3) parity class: m=2, OFF at m=3, back m=4,5; Yu-Oh class: OFF at
      m=2 ([4,2,1,1,1] has no 3|n block), on m=3,4,5.
  The v0.1 N_c-ordering survives only as a parity-class-internal fact
  (SU(3) m=2 vs SU(2) m=4), now with its rigidity certified (4|n is what
  parity-form hostability MEANS, not an artifact of the constructive route).

  MIXED WORDS (SU(3) by (k fund, l antifund), k+l <= 6; SU(2) by length --
  pseudoreality makes only the length matter):
    * The BARYON (3,0): singlet multiplicity 1 (the canonical frame-free
      record -- the banked baryon readout) and blocks [2,1,1]: GLEASON-FENCED.
      The physical baryon interface hosts NO contextuality of any class; its
      distinguishing reading is the canonical record, not an obstruction.
    * (2,1): singlet 0 (no sharp record) and fenced.
    * Four constituents is the true contextuality onset: the tetraquark
      (2,2) (parity, the banked octet M_4) and (3,1) (Yu-Oh via [3,3,2,1]).
    * The SU(3) PENTAQUARK (4,1): blocks [8,4,3,3,2,1] -- hosts BOTH
      state-independent classes (4|8, 4|4, 3|3), the SU(3) parallel of the
      banked SU(2) pentaquark M_4.
    * The hexaquark (3,3) has the same commutant profile as pairs m=3
      (content counts are what matter): Yu-Oh only, parity absent.
    * (6,0): blocks [16,10,9,5,5,5,1] -- six-quark baryonic content hosts
      the magic square (4|16).
    * SU(2) length 5 (the banked pentaquark, blocks [5,4,1]): parity WITHOUT
      Yu-Oh -- the complementarity runs in both directions.
  ON THE ENTIRE SCANNED SURFACE the honest-open flag NEVER FIRES: every
  profile with a block >= 3 has a 3|n or 4|n block, so the constructive
  classes cover everything the census reaches. The flag remains defined and
  pinned-absent (a profile like [5,1] or [7,2] would carry it; none occurs
  here -- negative-tested in the check).

FENCES (inherited, verbatim discipline):
  (i)   Occupancy stays the QAC. The functional maps drawn CONTENT to the
        readings it supports; WHICH interfaces are drawn is profile/QAC and is
        untouched (the .306 scope split, honored not discharged-away).
  (ii)  "gauge-invariant = physical record" is the adopted no-B reading,
        [P_structural_reading] (v24.3.281/.284); the multiplicities are exact
        [P]-grade rep theory; the READING grade is inherited, not upgraded.
  (iii) Contextuality certifies structural obstruction EXISTENCE only; nothing
        here touches the k-string tension law or gap magnitudes
        (check_T_colour_contextuality_is_kstring_spectrum_blind stands).
  (iv)  General dim-n KS sets exist in every dim >= 3 but are NOT instantiated
        beyond the constructed rungs; every profile with a block >= 3 and no
        3|n or 4|n certificate carries the GENERAL_DIM_KS_NOT_INSTANTIATED
        flag. Post-Yu-Oh this flag is EMPTY on the scanned census surface
        (pinned); it remains live for off-surface content.
  (v)   IE inputs remain SUBMITTED: this module GENERATES payloads and submits
        them; the atlas itself still does not auto-generate (the .306 fence on
        the atlas is unchanged -- the functional lives in front of it).
  (vi)  The Yu-Oh rung's "state-independent" is the INEQUALITY sense; the
        parity rung's is the strictly stronger coloring sense. The ladder
        never conflates them (distinct class names, distinct certificates).
"""

from __future__ import annotations

from typing import Dict, List, Tuple


# =====================================================================
# Exact isotypic decomposition by iterated tensor rules
# =====================================================================

def su2_decompose(word: Tuple[str, ...]) -> Dict[int, int]:
    """Isotypic decomposition of an SU(2) fund/antifund word.

    Labels are doubled spins a = 2j (dim a+1); fund = antifund = a=1
    (SU(2) is pseudoreal, so the word's fund/antifund pattern does not
    affect the decomposition -- only its length does).
    Rule: a (x) 1 = (a-1 if a>=1) (+) (a+1).
    """
    cur: Dict[int, int] = {0: 1}
    for _ in word:
        nxt: Dict[int, int] = {}
        for a, mult in cur.items():
            for b in ((a - 1, a + 1) if a >= 1 else (a + 1,)):
                nxt[b] = nxt.get(b, 0) + mult
        cur = nxt
    return cur


def su3_decompose(word: Tuple[str, ...]) -> Dict[Tuple[int, int], int]:
    """Isotypic decomposition of an SU(3) fund/antifund word.

    Labels are Dynkin pairs (p, q); dim = (p+1)(q+1)(p+q+2)/2; fund = (1,0),
    antifund = (0,1). Branching rules (exact, standard):
      (p,q) (x) (1,0) = (p+1,q) (+) (p-1,q+1)[p>=1] (+) (p,q-1)[q>=1]
      (p,q) (x) (0,1) = (p,q+1) (+) (p+1,q-1)[q>=1] (+) (p-1,q)[p>=1]
    """
    cur: Dict[Tuple[int, int], int] = {(0, 0): 1}
    for f in word:
        if f not in ("fund", "antifund"):
            raise ValueError("su3_decompose: factors must be 'fund'/'antifund'")
        nxt: Dict[Tuple[int, int], int] = {}
        for (p, q), mult in cur.items():
            if f == "fund":
                targets = [(p + 1, q)]
                if p >= 1:
                    targets.append((p - 1, q + 1))
                if q >= 1:
                    targets.append((p, q - 1))
            else:
                targets = [(p, q + 1)]
                if q >= 1:
                    targets.append((p + 1, q - 1))
                if p >= 1:
                    targets.append((p - 1, q))
            for t in targets:
                nxt[t] = nxt.get(t, 0) + mult
        cur = nxt
    return cur


def _su2_dim(a: int) -> int:
    return a + 1


def _su3_dim(pq: Tuple[int, int]) -> int:
    p, q = pq
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def decompose_general(N: int, word):
    """Isotypic decomposition over the full alphabet fund / antifund / adjoint.

    The adjoint (gluon) factor is applied by the exact subtraction identity
    X (x) adj = X (x) f (x) fbar - X, valid because f (x) fbar = adj (+) triv
    for SU(N) -- so the multiset subtraction is always non-negative (asserted).
    For fund/antifund-only words this reproduces su2_decompose/su3_decompose
    exactly (the v0.1/v0.2 pins are computed on those unchanged paths).
    """
    word = tuple(word)
    cur = {0: 1} if N == 2 else {(0, 0): 1}

    def _tf(d, anti):
        out = {}
        if N == 2:
            for a, m in d.items():
                for b in ((a - 1, a + 1) if a >= 1 else (a + 1,)):
                    out[b] = out.get(b, 0) + m
        else:
            for (p, q), m in d.items():
                ts = [(p, q + 1) if anti else (p + 1, q)]
                if anti:
                    if q >= 1:
                        ts.append((p + 1, q - 1))
                    if p >= 1:
                        ts.append((p - 1, q))
                else:
                    if p >= 1:
                        ts.append((p - 1, q + 1))
                    if q >= 1:
                        ts.append((p, q - 1))
                for t in ts:
                    out[t] = out.get(t, 0) + m
        return out

    for f in word:
        if f == "fund":
            cur = _tf(cur, False)
        elif f == "antifund":
            cur = _tf(cur, True)
        elif f == "adjoint":
            big = _tf(_tf(cur, False), True)
            for k, m in cur.items():
                big[k] = big.get(k, 0) - m
                if big[k] == 0:
                    del big[k]
            if any(v < 0 for v in big.values()):
                raise AssertionError("adjoint subtraction went negative -- "
                                     "the f (x) fbar = adj (+) triv identity was violated")
            cur = big
        else:
            raise ValueError("decompose_general: factors must be "
                             "'fund'/'antifund'/'adjoint'")
    return cur


def commutant_profile(N: int, word) -> Dict:
    """The complete commutant profile of the declared rep content.

    By Schur: the commutant of the gauge action on the word's carrier space is
    (+)_irrep M_{mult(irrep)}. Returns every block, the singlet multiplicity
    (the .306 READOUT input), and exactness witnesses (dim sum = the product
    of factor dimensions: N for fund/antifund, N^2-1 for adjoint).
    Alphabet: fund / antifund / adjoint (gluon; v0.4).
    """
    word = tuple(word)
    if N not in (2, 3):
        raise ValueError("commutant_profile: N in (2,3) only")
    if "adjoint" in word:
        dec = decompose_general(N, word)
    elif N == 2:
        dec = su2_decompose(word)
    else:
        dec = su3_decompose(word)
    if N == 2:
        items = [(("a=%d" % a), _su2_dim(a), m) for a, m in sorted(dec.items())]
        singlet = dec.get(0, 0)
    else:
        items = [(("(%d,%d)" % pq), _su3_dim(pq), m) for pq, m in sorted(dec.items())]
        singlet = dec.get((0, 0), 0)
    total = sum(d * m for (_, d, m) in items)
    expect = 1
    for f in word:
        expect *= (N * N - 1) if f == "adjoint" else N
    blocks = sorted((m for (_, _, m) in items), reverse=True)
    return {
        "N": N,
        "word": word,
        "decomposition": {lbl: {"dim": d, "mult": m} for (lbl, d, m) in items},
        "total_dim": total,
        "dim_check_pass": total == expect,
        "blocks": blocks,
        "commutant_dim": sum(m * m for m in blocks),
        "singlet_mult": singlet,
    }


# =====================================================================
# The block-graded reading ladder (v0.2: Yu-Oh rung discharged)
# =====================================================================

def reading_classes(blocks: List[int]) -> Tuple[str, ...]:
    """The reading classes a commutant profile supports (the graded ladder)."""
    mx = max(blocks) if blocks else 0
    has_3n = any(n % 3 == 0 and n >= 3 for n in blocks)
    has_4n = any(n % 4 == 0 and n >= 4 for n in blocks)
    classes: List[str] = []
    if mx <= 1:
        classes.append("ABELIAN_SEP")
    elif mx == 2:
        classes.append("GLEASON_DIM2_FENCE")
    if mx >= 3:
        classes.append("KCBS_STATE_DEPENDENT")
    if mx >= 4:
        classes.append("MAGIC_SQUARE_STATE_DEPENDENT")
    if has_3n:
        # unital M_3 (x) I lift of the banked Yu-Oh 13-ray set: every block
        # state reduces to a qutrit state, every qutrit state violates --
        # state-independent in the INEQUALITY sense (fence vi).
        classes.append("YU_OH_STATE_INDEPENDENT")
    if has_4n:
        classes.append("MAGIC_SQUARE_STATE_INDEPENDENT")
    if mx >= 3 and not (has_3n or has_4n):
        # honest-open rung: an un-instantiated state-independent KS possibility
        # exists (KS dimension bound, dim >= 3) and no constructive certificate
        # covers the profile (fence iv). Empty on the scanned census surface.
        classes.append("GENERAL_DIM_KS_NOT_INSTANTIATED")
    return tuple(classes)


def _readout_trichotomy(m: int) -> Dict:
    """The .306 record trichotomy from the singlet multiplicity (same semantics
    as interface_readout_adapter.readout_classify, computed from characters)."""
    if m == 1:
        return {"verdict": "CANONICAL_RECORD", "obstruction": ()}
    if m == 0:
        return {"verdict": "NO_SHARP_RECORD", "obstruction": ("readout_no_sharp_record_m0",)}
    return {"verdict": "NON_CANONICAL_MULTIPLICITY",
            "obstruction": ("readout_multiplicity_frame_required_m%d" % m,)}


def generate_readings(N: int, word, route_engine: bool = True) -> Dict:
    """The functional: rep content -> the readings it supports, engine-routed.

    Auto-instantiates the scenario for each constructive contextuality rung
    present and submits it to the live IE pipeline; returns the profile, the
    reading classes, the readout trichotomy, and the engine verdicts.
    """
    prof = commutant_profile(N, word)
    classes = reading_classes(prof["blocks"])
    readout = _readout_trichotomy(prof["singlet_mult"])
    routed: Dict[str, Dict] = {}
    if route_engine:
        from apf.ijc_feasbool_engine import (
            scenario_mermin_peres_magic_square, scenario_to_dict,
            ks_parity_decide, _magic_square_parity_system,
        )
        from apf.interface_contextuality_adapter import route_contextuality
        from apf.gauge_invariant_record import _gic_kcbs_scenario, _gic_yuoh_scenario
        tag = "dcr_SU%d_%s" % (N, "".join("f" if f == "fund" else "a" for f in word))
        if "KCBS_STATE_DEPENDENT" in classes:
            scn, _p, _S = _gic_kcbs_scenario()
            pipe = route_contextuality(tag + "_kcbs", scenario=scenario_to_dict(scn))
            routed["kcbs"] = {
                "sense": "state_dependent",
                "solver_status": pipe.solver_status,
                "export_global_P": bool(pipe.export_global_P),
                "obstruction": tuple(pipe.obstruction),
            }
        if "YU_OH_STATE_INDEPENDENT" in classes:
            scn, _r, _t, _pr = _gic_yuoh_scenario()
            pipe = route_contextuality(tag + "_yuoh", scenario=scenario_to_dict(scn))
            routed["yu_oh"] = {
                "sense": "state_independent_inequality",
                "solver_status": pipe.solver_status,
                "export_global_P": bool(pipe.export_global_P),
                "obstruction": tuple(pipe.obstruction),
            }
        if ("MAGIC_SQUARE_STATE_DEPENDENT" in classes
                or "MAGIC_SQUARE_STATE_INDEPENDENT" in classes):
            scn = scenario_mermin_peres_magic_square()
            pipe = route_contextuality(tag + "_magic_square", scenario=scenario_to_dict(scn))
            routed["magic_square"] = {
                "sense": ("state_independent_coloring"
                          if "MAGIC_SQUARE_STATE_INDEPENDENT" in classes
                          else "state_dependent_subspace"),
                "solver_status": pipe.solver_status,
                "export_global_P": bool(pipe.export_global_P),
                "obstruction": tuple(pipe.obstruction),
            }
            if "MAGIC_SQUARE_STATE_INDEPENDENT" in classes:
                n_obs, ctx = _magic_square_parity_system()
                routed["magic_square"]["gf2_state_independent"] = (
                    not ks_parity_decide(n_obs, ctx)["consistent"])
    return {
        "N": N, "word": tuple(word),
        "profile": prof,
        "reading_classes": classes,
        "readout": readout,
        "engine": routed,
    }


# =====================================================================
# The censuses (the physics deliverables)
# =====================================================================

def census_pairs(max_m: int = 5) -> Dict:
    """Contextuality-class onset census over (fund antifund)^m, N in (2,3).

    Onsets are the first m at which each class appears. Engine routing is done
    once per (group, scenario) at its onset, not at every m (the scenario
    verdict is content-independent once hosted; hosting is the computed part).
    """
    table: Dict[str, Dict] = {}
    onsets: Dict[str, Dict[str, int]] = {"SU2": {}, "SU3": {}}
    for N, key in ((2, "SU2"), (3, "SU3")):
        rows = {}
        for m in range(1, max_m + 1):
            word = ("fund", "antifund") * m
            prof = commutant_profile(N, word)
            classes = reading_classes(prof["blocks"])
            rows[m] = {"blocks": prof["blocks"], "singlet_mult": prof["singlet_mult"],
                       "classes": classes, "dim_check_pass": prof["dim_check_pass"]}
            for c in classes:
                if c not in onsets[key]:
                    onsets[key][c] = m
        table[key] = rows
    return {"rows": table, "onsets": onsets, "max_m": max_m}


def census_words(max_len: int = 6) -> Dict:
    """Mixed-word census: SU(3) by (k fund, l antifund) with k+l <= max_len and
    k >= l (conjugation mirrors the table); SU(2) by word length (pseudoreality:
    only the length matters). Tensor decomposition depends only on the factor
    counts, not the order, so (k,l) indexes the whole orbit of orderings."""
    su3: Dict[Tuple[int, int], Dict] = {}
    for k in range(0, max_len + 1):
        for l in range(0, max_len + 1 - k):
            if k + l == 0 or k < l:
                continue
            word = ("fund",) * k + ("antifund",) * l
            prof = commutant_profile(3, word)
            su3[(k, l)] = {"blocks": prof["blocks"], "singlet_mult": prof["singlet_mult"],
                           "classes": reading_classes(prof["blocks"]),
                           "dim_check_pass": prof["dim_check_pass"]}
    su2: Dict[int, Dict] = {}
    for L in range(1, max_len + 1):
        prof = commutant_profile(2, ("fund",) * L)
        su2[L] = {"blocks": prof["blocks"], "singlet_mult": prof["singlet_mult"],
                  "classes": reading_classes(prof["blocks"]),
                  "dim_check_pass": prof["dim_check_pass"]}
    return {"SU3": su3, "SU2": su2, "max_len": max_len}


# =====================================================================
# The magic-square rigidity certificate (4|n hostability is invariant)
# =====================================================================

def _pauli2_group_elements():
    """The real 2-qubit Pauli group G, abstractly: elements (s, v) with
    s in GF(2) (the sign (-1)^s) and v = (a1,b1,a2,b2) in GF(2)^4 encoding
    X^a1 Z^b1 (x) X^a2 Z^b2. Multiplication picks up the sign of moving Z past
    X per qubit factor: (s,v)(t,w) = (s + t + b1*w_a1 + b2*w_a2, v + w).
    |G| = 32; center = {(0,0), (1,0)}; J = (1, 0000) plays -I."""
    els = [(s, (a1, b1, a2, b2))
           for s in (0, 1) for a1 in (0, 1) for b1 in (0, 1)
           for a2 in (0, 1) for b2 in (0, 1)]
    def mul(x, y):
        s, (a1, b1, a2, b2) = x
        t, (c1, d1, c2, d2) = y
        sign = (s + t + b1 * c1 + b2 * c2) % 2
        return (sign, ((a1 + c1) % 2, (b1 + d1) % 2, (a2 + c2) % 2, (b2 + d2) % 2))
    def inv(x):
        # x^2 = (b1*a1 + b2*a2, 0); each element is its own inverse up to J
        s, (a1, b1, a2, b2) = x
        extra = (b1 * a1 + b2 * a2) % 2
        return ((s + extra) % 2, (a1, b1, a2, b2))
    return els, mul, inv


def check_T_magic_square_solution_group_rep_forces_4n() -> Dict:
    """Magic-square parity hostability is 4|n-rigid: certified at the
    finite-group level, with ONE named cited step.

    THE CLAIM the drawn-content ladder relies on: an exact operator solution of
    the six Mermin-Peres parity constraints (nine +-1 observables, commuting
    within rows/columns, row products +I, odd total column parity) exists on an
    n-dim block only if 4 | n -- so the ladder's MAGIC_SQUARE_STATE_INDEPENDENT
    column measures an invariant of the block, not an artifact of the
    constructive M_4 (x) I route.

    WHAT THIS CHECK CERTIFIES, exactly (integer arithmetic throughout):
      (1) The real 2-qubit Pauli group G (order 32, elements +-X^a Z^b (x)
          X^c Z^d built abstractly on GF(2)^4 with the symplectic sign
          cocycle) is closed, EXHAUSTIVELY associative (all 32^3 triples),
          has center {1, J} with J^2 = 1, and commutator subgroup
          [G,G] = {1, J}.
      (2) G has EXACTLY 17 conjugacy classes (brute-force orbit computation)
          and abelianization of order 16; hence 17 irreps, 16 linear (all
          with J -> +1, since J in [G,G]), and 32 - 16 = 16 = d^2 forces the
          single remaining irrep to have dimension EXACTLY 4. Therefore EVERY
          finite-dim rep of G with J -> -I is a multiple of the 4-dim irrep:
          4 | n. No numerics; pure counting.
      (3) The standard Pauli magic square IS a solution generating (an image
          of) G with J -> -I: the nine cells as (s,v) words, each context
          verified pairwise-commuting in G, row products = identity, column
          products (e, e, J) -- odd total column parity, the sign-convention
          invariant -- all inside the abstract group -- and independently as
          exact integer 4x4 matrices (X, Z, tensor products), where rows
          multiply to +I_4 and columns to -I_4.

    THE ONE CITED STEP (named, not certified): that the ABSTRACT solution
    group of the magic-square presentation (nine involution generators,
    context commutations, parity relations) collapses to (is isomorphic to) G -- equivalently,
    that every operator solution generates an image of G with J -> -I. This
    is the solution-group/rigidity fact (Mermin 1990 operator analysis;
    Cleve-Mittal 2014, Cleve-Liu-Slofstra 2017 solution groups). The check
    certifies everything downstream of it: GIVEN that collapse, 4 | n is
    forced by (2). The citation is thereby narrowed to exactly one
    presentation-theoretic step.

    Grade P_structural_instrument tier 4: exact finite mathematics + one named
    literature step admitted as instrument (the LQT-eigenscreen precedent for
    admitted-standard-structure). No occupancy claim; no spectrum claim.
    """
    failures: List[str] = []
    els, mul, inv = _pauli2_group_elements()
    e = (0, (0, 0, 0, 0))
    J = (1, (0, 0, 0, 0))

    # (1) group sanity: closure, identity, inverses, exhaustive associativity
    sels = set(els)
    if len(els) != 32:
        failures.append("|G| should be 32")
    for x in els:
        if mul(e, x) != x or mul(x, e) != x:
            failures.append("identity failed at %s" % (x,))
            break
        if mul(x, inv(x)) != e:
            failures.append("inverse failed at %s" % (x,))
            break
    assoc_fail = False
    for x in els:
        if assoc_fail:
            break
        for y in els:
            if assoc_fail:
                break
            if mul(x, y) not in sels:
                failures.append("closure failed")
                assoc_fail = True
                break
            for z in els:
                if mul(mul(x, y), z) != mul(x, mul(y, z)):
                    failures.append("associativity failed")
                    assoc_fail = True
                    break
    # center and commutator subgroup both {e, J}
    center = [x for x in els if all(mul(x, y) == mul(y, x) for y in els)]
    if sorted(center) != sorted([e, J]):
        failures.append("center should be {1, J}: %s" % (center,))
    comms = set()
    for x in els:
        for y in els:
            comms.add(mul(mul(x, y), inv(mul(y, x))))
    if sorted(comms) != sorted([e, J]):
        failures.append("[G,G] should be {1, J}: got %d elements" % len(comms))

    # (2) conjugacy classes -> irrep dimension forcing
    seen = set()
    n_classes = 0
    for x in els:
        if x in seen:
            continue
        orbit = {mul(mul(g, x), inv(g)) for g in els}
        seen |= orbit
        n_classes += 1
    if n_classes != 17:
        failures.append("conjugacy class count should be 17: got %d" % n_classes)
    n_linear = 32 // len(comms) if len(comms) else 0  # |G/[G,G]|
    if n_linear != 16:
        failures.append("abelianization order should be 16: got %d" % n_linear)
    d2_remaining = 32 - n_linear
    n_nonlinear = n_classes - n_linear
    if n_nonlinear != 1 or d2_remaining != 16:
        failures.append("should be exactly one non-linear irrep with d^2=16")
    forced_dim = 4  # d^2 = 16, one irrep -> d = 4 exactly

    # (3) the standard Pauli square as an abstract-group solution ...
    X1 = (0, (1, 0, 0, 0)); Z1 = (0, (0, 1, 0, 0))
    X2 = (0, (0, 0, 1, 0)); Z2 = (0, (0, 0, 0, 1))
    XX = mul(X1, X2); ZZ = mul(Z1, Z2)
    XZ = mul(X1, Z2); ZX = mul(Z1, X2)
    # Y (x) Y in the REAL group: Y = iXZ, so Y(x)Y = -(XZ)(x)(XZ) = J * XX * ZZ
    YY = mul(J, mul(XX, ZZ))
    # the standard Mermin layout; sign convention: rows all +1, the ODD column
    # is the third (col products e, e, J). GF(2)-equivalent to the engine's
    # all-columns-odd parity form -- the invariant is the odd TOTAL parity
    # contradiction, not which columns carry it.
    square = [[X2, X1, XX],
              [Z1, Z2, ZZ],
              [ZX, XZ, YY]]
    col_expect = (e, e, J)
    for r in range(3):
        for c1 in range(3):
            for c2 in range(c1 + 1, 3):
                a, b = square[r][c1], square[r][c2]
                if mul(a, b) != mul(b, a):
                    failures.append("row %d cells must commute" % r)
        prod = mul(mul(square[r][0], square[r][1]), square[r][2])
        if prod != e:
            failures.append("row %d product should be identity: %s" % (r, prod))
    for c in range(3):
        for r1 in range(3):
            for r2 in range(r1 + 1, 3):
                a, b = square[r1][c], square[r2][c]
                if mul(a, b) != mul(b, a):
                    failures.append("col %d cells must commute" % c)
        prod = mul(mul(square[0][c], square[1][c]), square[2][c])
        if prod != col_expect[c]:
            failures.append("col %d product wrong: %s" % (c, prod))
    if [mul(mul(square[0][c], square[1][c]), square[2][c]) for c in range(3)].count(J) % 2 != 1:
        failures.append("total column parity must be odd (the contradiction invariant)")

    # ... and independently as exact integer 4x4 matrices
    def kron2(A, B):
        return [[A[i][j] * B[k][l] for j in range(2) for l in range(2)]
                for i in range(2) for k in range(2)]
    def mm(A, B):
        n = len(A)
        return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)]
                for i in range(n)]
    I2 = [[1, 0], [0, 1]]; Xm = [[0, 1], [1, 0]]; Zm = [[1, 0], [0, -1]]
    M = {(0, (1, 0, 0, 0)): kron2(Xm, I2), (0, (0, 1, 0, 0)): kron2(Zm, I2),
         (0, (0, 0, 1, 0)): kron2(I2, Xm), (0, (0, 0, 0, 1)): kron2(I2, Zm)}
    def mat_of(el):
        # decompose el = (-1)^s X1^a1 Z1^b1 X2^a2 Z2^b2 in that normal order
        s, (a1, b1, a2, b2) = el
        A = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
        if a1: A = mm(A, M[(0, (1, 0, 0, 0))])
        if b1: A = mm(A, M[(0, (0, 1, 0, 0))])
        if a2: A = mm(A, M[(0, (0, 0, 1, 0))])
        if b2: A = mm(A, M[(0, (0, 0, 0, 1))])
        if s: A = [[-x for x in row] for row in A]
        return A
    I4 = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
    mI4 = [[-x for x in row] for row in I4]
    mat_col_expect = (I4, I4, mI4)
    for r in range(3):
        P = mm(mm(mat_of(square[r][0]), mat_of(square[r][1])), mat_of(square[r][2]))
        if P != I4:
            failures.append("matrix row %d product != +I_4" % r)
    for c in range(3):
        P = mm(mm(mat_of(square[0][c]), mat_of(square[1][c])), mat_of(square[2][c]))
        if P != mat_col_expect[c]:
            failures.append("matrix col %d product wrong" % c)
    # normal-order consistency: mat_of is a genuine rep of the abstract product
    for x in els[::3]:
        for y in els[::5]:
            if mat_of(mul(x, y)) != mm(mat_of(x), mat_of(y)):
                failures.append("mat_of is not a homomorphism")
                break

    passed = not failures
    return {
        "name": "check_T_magic_square_solution_group_rep_forces_4n",
        "tier": 4,
        "epistemic": "P_structural_instrument",
        "passed": passed,
        "failures": failures,
        "key_result": ("magic-square 4|n rigidity certified at the finite-group level: "
                       "G (real 2-qubit Pauli, |G|=32) has 17 classes, [G,G]={1,J}, 16 "
                       "linear irreps (J->+1) and ONE non-linear irrep of dim exactly 4 "
                       "-- every rep with J->-I has 4|n; the standard Pauli square "
                       "verified as a solution in G and as exact integer matrices. ONE "
                       "cited step (solution-group collapse onto G: Mermin/Cleve-Mittal/"
                       "Cleve-Liu-Slofstra), named and narrowed"),
        "forced_irrep_dim": forced_dim,
        "cited_step": ("abstract magic-square solution group collapses to (is isomorphic to) G with "
                       "J -> -I (Mermin 1990; Cleve-Mittal 2014; Cleve-Liu-Slofstra "
                       "2017) -- presentation-theoretic, admitted as instrument"),
        "summary": ("PASS" if passed else "FAIL: %s" % failures),
    }


# =====================================================================
# The main functional check (v0.2 pins)
# =====================================================================

def check_T_drawn_content_readings_functional() -> Dict:
    """The drawn-content -> readings functional: banked rep content generates
    its own IE scenario payloads, with the census pinned (v0.2: Yu-Oh rung
    discharged; mixed-word surface added).

    Validates, in order:
      (1) EXACTNESS: dim sums equal N^len for every word tested; the character
          decomposition agrees with the bank's independent kernel-rank
          computation (interface_readout_adapter.readout_multiplicity) on
          every fund/antifund word of length <= 3 for N=2,3, plus the SU(2)
          tetraquark; and with the bank's exact Weyl-Klimyk tetraquark
          decomposition (_su3_weyl_klimyk_tetraquark) irrep-by-irrep.
      (2) REGRESSION ANCHORS: SU(2) fund^5 spin-3/2 multiplicity = 4 (the
          banked pentaquark M_4); SU(3) 2-pair octet multiplicity = 4, total
          81 (the banked octet M_4); SU(2)/SU(3) m=1 pairs abelian; the
          SU(3) baryon (3,0) singlet multiplicity = 1 (the banked canonical
          baryon record).
      (3) THE LADDER IS HONEST (negative tests): max-2 profiles emit only the
          fence; [3,2,1] hosts KCBS + Yu-Oh (3|3), NO flag; [9,5,5,1] hosts
          Yu-Oh but NOT the parity class (no 4|n); [4,2,1] hosts parity but
          NOT Yu-Oh (no 3|n); [5,1] and [7,2] carry the honest-open flag
          (constructed examples -- the flag is live, just empty on-surface).
      (4) ENGINE ROUTING at the onsets: KCBS, Yu-Oh, and magic square all
          route through the live IE pipeline -> IJC_OBSTRUCTION, no global-P
          export; the parity form carries the GF(2) certificate. SU(2) m=2
          generates KCBS+Yu-Oh but NO magic-square payload; SU(3) m=2
          generates the magic square but NO Yu-Oh payload. (Routing validates
          the pipe; WHICH scenarios a word hosts is what (1)-(3)+(5) certify.)
      (5) THE CENSUS PINS (pairs m <= 5 + mixed words k+l <= 6):
          onsets, block lists, per-class flickers, the class-agnostic UNION
          persistence (state-independence holds for ALL m in 2..5 in BOTH
          groups -- the v0.1 N_c ordering dissolves at class-agnostic
          strength, surviving only parity-class-internally), the empty
          honest-open flag on the whole scanned surface, and the mixed-word
          landmarks (baryon fenced w/ canonical record; 4-constituent onset;
          SU(3) pentaquark hosts both classes; SU(2) length-5 hosts parity
          without Yu-Oh).

    Grade P_structural_instrument: the verdicts are the IE's exact
    computations over exact rep theory; the no-B reading grade is inherited
    per fence (ii); the Yu-Oh rung carries the inequality-sense semantics per
    fence (vi); occupancy is not claimed. Tier 4.
    """
    failures: List[str] = []

    # --- (1) exactness vs the bank's independent computations ---
    from apf.interface_readout_adapter import readout_multiplicity
    from itertools import product as _iproduct
    for N in (2, 3):
        for L in (1, 2, 3):
            for word in _iproduct(("fund", "antifund"), repeat=L):
                prof = commutant_profile(N, word)
                if not prof["dim_check_pass"]:
                    failures.append("dim sum failed: SU(%d) %s" % (N, word))
                km = readout_multiplicity(N, tuple(word))
                if prof["singlet_mult"] != km:
                    failures.append("singlet mult mismatch SU(%d) %s: chars %d vs kernel %d"
                                    % (N, word, prof["singlet_mult"], km))
    w4 = ("fund", "antifund", "fund", "antifund")
    if commutant_profile(2, w4)["singlet_mult"] != readout_multiplicity(2, w4):
        failures.append("SU(2) tetraquark singlet mult mismatch vs kernel rank")

    from apf.gauge_invariant_record import _su3_weyl_klimyk_tetraquark
    wk = _su3_weyl_klimyk_tetraquark()
    mine = su3_decompose(w4)
    wk_by_pq = {pq: n for pq, (d, n) in wk.items()}
    if mine != wk_by_pq:
        failures.append("SU(3) tetraquark decomposition disagrees with banked Weyl-Klimyk")

    # --- (2) regression anchors ---
    penta = su2_decompose(("fund",) * 5)
    if penta.get(3, 0) != 4:
        failures.append("pentaquark spin-3/2 multiplicity should be 4 (banked M_4)")
    octet = su3_decompose(w4)
    if octet.get((1, 1), 0) != 4 or commutant_profile(3, w4)["total_dim"] != 81:
        failures.append("SU(3) octet anchor failed")
    for N in (2, 3):
        if reading_classes(commutant_profile(N, ("fund", "antifund"))["blocks"]) != ("ABELIAN_SEP",):
            failures.append("m=1 meson should be ABELIAN_SEP for SU(%d)" % N)
    if commutant_profile(3, ("fund",) * 3)["singlet_mult"] != 1:
        failures.append("SU(3) baryon (3,0) should have singlet multiplicity 1 (canonical record)")

    # --- (3) ladder honesty (negative tests) ---
    if reading_classes([2, 1]) != ("GLEASON_DIM2_FENCE",):
        failures.append("max-block-2 must emit the Gleason fence and nothing else")
    cl_321 = reading_classes([3, 2, 1])
    if cl_321 != ("KCBS_STATE_DEPENDENT", "YU_OH_STATE_INDEPENDENT"):
        failures.append("[3,2,1] should host KCBS + Yu-Oh and no flag: %s" % (cl_321,))
    cl_953 = reading_classes([9, 5, 5, 1])
    if ("YU_OH_STATE_INDEPENDENT" not in cl_953
            or "MAGIC_SQUARE_STATE_INDEPENDENT" in cl_953
            or "GENERAL_DIM_KS_NOT_INSTANTIATED" in cl_953):
        failures.append("[9,5,5,1] should host Yu-Oh (9=3x3), not parity, no flag: %s" % (cl_953,))
    cl_421 = reading_classes([4, 2, 1])
    if ("MAGIC_SQUARE_STATE_INDEPENDENT" not in cl_421
            or "YU_OH_STATE_INDEPENDENT" in cl_421):
        failures.append("[4,2,1] should host parity, not Yu-Oh: %s" % (cl_421,))
    for probe in ([5, 1], [7, 2]):
        if "GENERAL_DIM_KS_NOT_INSTANTIATED" not in reading_classes(probe):
            failures.append("%s must carry the honest-open flag (no 3|n or 4|n)" % (probe,))

    # --- (4) engine routing at the onsets ---
    r_su3 = generate_readings(3, w4)
    eng = r_su3["engine"]
    if not ("kcbs" in eng and eng["kcbs"]["solver_status"] == "IJC_OBSTRUCTION"
            and not eng["kcbs"]["export_global_P"] and eng["kcbs"]["obstruction"]):
        failures.append("SU(3) m=2 KCBS engine verdict wrong")
    if not ("magic_square" in eng
            and eng["magic_square"]["solver_status"] == "IJC_OBSTRUCTION"
            and not eng["magic_square"]["export_global_P"]
            and eng["magic_square"].get("gf2_state_independent") is True):
        failures.append("SU(3) m=2 magic-square engine verdict wrong")
    if "yu_oh" in eng:
        failures.append("SU(3) m=2 must NOT generate a Yu-Oh payload (no 3|n block)")
    if r_su3["readout"]["verdict"] != "NON_CANONICAL_MULTIPLICITY":
        failures.append("SU(3) m=2 readout should be the m=2 frame obstruction")
    r_su2m2 = generate_readings(2, ("fund", "antifund") * 2)
    eng2 = r_su2m2["engine"]
    if "magic_square" in eng2:
        failures.append("SU(2) m=2 must NOT generate a magic-square payload (no M_4)")
    if not ("kcbs" in eng2 and "yu_oh" in eng2
            and eng2["yu_oh"]["solver_status"] == "IJC_OBSTRUCTION"
            and not eng2["yu_oh"]["export_global_P"] and eng2["yu_oh"]["obstruction"]):
        failures.append("SU(2) m=2 should generate KCBS + Yu-Oh payloads with IJC verdicts")

    # --- (5) the census pins ---
    census = census_pairs(5)
    expect = {
        "SU3": {"ABELIAN_SEP": 1, "KCBS_STATE_DEPENDENT": 2,
                "MAGIC_SQUARE_STATE_DEPENDENT": 2, "MAGIC_SQUARE_STATE_INDEPENDENT": 2,
                "YU_OH_STATE_INDEPENDENT": 3},
        "SU2": {"ABELIAN_SEP": 1, "KCBS_STATE_DEPENDENT": 2,
                "YU_OH_STATE_INDEPENDENT": 2, "MAGIC_SQUARE_STATE_DEPENDENT": 3,
                "MAGIC_SQUARE_STATE_INDEPENDENT": 4},
    }
    for grp, exp in expect.items():
        for cls, m0 in exp.items():
            got = census["onsets"][grp].get(cls)
            if got != m0:
                failures.append("onset pin failed %s/%s: expected m=%d got %s"
                                % (grp, cls, m0, got))
        if "GENERAL_DIM_KS_NOT_INSTANTIATED" in census["onsets"][grp]:
            failures.append("%s pairs census must never fire the honest-open flag "
                            "(post-Yu-Oh the surface is covered)" % grp)
    blocks_expect = {
        ("SU2", 2): [3, 2, 1], ("SU2", 3): [9, 5, 5, 1],
        ("SU2", 4): [28, 20, 14, 7, 1], ("SU2", 5): [90, 75, 42, 35, 9, 1],
        ("SU3", 2): [4, 2, 1, 1, 1], ("SU3", 3): [17, 9, 7, 7, 6, 2, 2, 1],
        ("SU3", 4): [80, 63, 42, 42, 23, 23, 23, 16, 3, 3, 2, 2, 1],
        ("SU3", 5): [415, 410, 250, 250, 195, 195, 164, 103, 51, 51,
                     30, 30, 25, 5, 5, 4, 4, 1],
    }
    for (grp, m), bl in blocks_expect.items():
        got = census["rows"][grp][m]["blocks"]
        if got != bl:
            failures.append("block-list pin failed %s m=%d" % (grp, m))
    # per-class flicker pins + the union persistence pin
    def has(grp, m, cls):
        return cls in census["rows"][grp][m]["classes"]
    MS, YO = "MAGIC_SQUARE_STATE_INDEPENDENT", "YU_OH_STATE_INDEPENDENT"
    ms_expect = {("SU3", 2): True, ("SU3", 3): False, ("SU3", 4): True, ("SU3", 5): True,
                 ("SU2", 2): False, ("SU2", 3): False, ("SU2", 4): True, ("SU2", 5): False}
    yo_expect = {("SU3", 2): False, ("SU3", 3): True, ("SU3", 4): True, ("SU3", 5): True,
                 ("SU2", 2): True, ("SU2", 3): True, ("SU2", 4): False, ("SU2", 5): True}
    for (grp, m), v in ms_expect.items():
        if has(grp, m, MS) != v:
            failures.append("parity-class flicker pin failed %s m=%d" % (grp, m))
    for (grp, m), v in yo_expect.items():
        if has(grp, m, YO) != v:
            failures.append("Yu-Oh-class flicker pin failed %s m=%d" % (grp, m))
    for grp in ("SU2", "SU3"):
        for m in range(2, 6):
            if not (has(grp, m, MS) or has(grp, m, YO)):
                failures.append("UNION persistence pin failed %s m=%d: state-independence "
                                "must hold at every m in 2..5" % (grp, m))
    # mixed-word landmarks
    words = census_words(6)
    su3w, su2w = words["SU3"], words["SU2"]
    if not all(row["dim_check_pass"] for row in list(su3w.values()) + list(su2w.values())):
        failures.append("mixed-word dim checks failed")
    baryon = su3w[(3, 0)]
    if not (baryon["singlet_mult"] == 1 and baryon["blocks"] == [2, 1, 1]
            and baryon["classes"] == ("GLEASON_DIM2_FENCE",)):
        failures.append("SU(3) baryon (3,0) should be Gleason-fenced with the canonical record")
    if su3w[(2, 1)]["singlet_mult"] != 0 or su3w[(2, 1)]["classes"] != ("GLEASON_DIM2_FENCE",):
        failures.append("(2,1) should be fenced with no sharp record")
    if su3w[(2, 2)]["blocks"] != [4, 2, 1, 1, 1]:
        failures.append("(2,2) must reproduce the pairs m=2 profile")
    p41 = su3w[(4, 1)]
    if not (p41["blocks"] == [8, 4, 3, 3, 2, 1] and MS in p41["classes"] and YO in p41["classes"]):
        failures.append("SU(3) pentaquark (4,1) should host BOTH state-independent classes")
    hexa = su3w[(3, 3)]
    if not (hexa["blocks"] == [17, 9, 7, 7, 6, 2, 2, 1] and YO in hexa["classes"]
            and MS not in hexa["classes"]):
        failures.append("hexaquark (3,3) should match pairs m=3: Yu-Oh only")
    if MS not in su3w[(6, 0)]["classes"]:
        failures.append("(6,0) should host the parity class (4|16)")
    su2p = su2w[5]
    if not (su2p["blocks"] == [5, 4, 1] and MS in su2p["classes"] and YO not in su2p["classes"]):
        failures.append("SU(2) length-5 (banked pentaquark) should host parity WITHOUT Yu-Oh")
    flag_hits = [k for k, row in list(su3w.items()) + list(su2w.items())
                 if "GENERAL_DIM_KS_NOT_INSTANTIATED" in row["classes"]]
    if flag_hits:
        failures.append("honest-open flag should be empty on the scanned surface: %s" % flag_hits)

    passed = not failures
    return {
        "name": "check_T_drawn_content_readings_functional",
        "tier": 4,
        "epistemic": "P_structural_instrument",
        "passed": passed,
        "failures": failures,
        "key_result": ("drawn-content -> readings functional v0.2: complete commutant "
                       "profiles from rep content, block-graded scenario generation "
                       "engine-verified (KCBS/Yu-Oh/magic square). Census pinned: both "
                       "groups reach state-independence at m=2 and KEEP it (union "
                       "persistent m=2..5) while EACH class flickers -- the v0.1 N_c "
                       "ordering dissolves at class-agnostic strength, surviving only "
                       "parity-class-internally (rigidity certified). Mixed words: baryon "
                       "Gleason-fenced w/ canonical record; 4-constituent contextuality "
                       "onset; SU(3) pentaquark hosts both classes; honest-open flag "
                       "EMPTY on the scanned surface"),
        "census_onsets": census["onsets"],
        "summary": ("PASS" if passed else "FAIL: %s" % failures),
    }


# =====================================================================
# The functional turned on the framework's own interface: V_61 (v0.3)
# =====================================================================

def sm_interface_profile(n_generations: int = 3) -> Dict:
    """The commutant profile of the 61-role capacity carrier under G_SM,
    read from the bank's own isotypic inventory (formal_kernel, the .326
    machinery) -- the same currency as a hadron word, with V_61 as the
    declared rep content. One disclosure a hadron word does not need: V_61 is
    a role ledger mixing complex Weyl slots (fermions) with real slots (gauge,
    Higgs), not a genuine complex G_SM module; the profile is computed in the
    banked signature convention (fields as written).

    For n_generations = 3 the inventory is consumed LIVE (any mutation of the
    banked content spec re-adjudicates this consumer, the inventory's own
    design). For counterfactual generation counts the fermion multiplicities
    are set to n_generations over the same five per-generation classes --
    transparent arithmetic on the banked class list, not a mutated inventory.
    """
    from apf.formal_kernel import _isotypic_inventory
    inv = _isotypic_inventory()
    rows = []
    for (label, base, d, m) in inv:
        mult = n_generations if label == "fermion" else m
        rows.append({"sector": label, "irrep": base, "dim": d, "mult": mult})
    blocks = sorted((r["mult"] for r in rows), reverse=True)
    # the trivial G_SM irrep inside V_61: the U(1) gauge line (the abelian
    # adjoint is trivial). e_R is dim-1 but hypercharge-charged -- NOT trivial.
    trivial_mult = sum(r["mult"] for r in rows
                       if r["sector"] == "gauge" and r["irrep"] == "U1")
    return {
        "n_generations": n_generations,
        "rows": rows,
        "blocks": blocks,
        "classes": reading_classes(blocks),
        "trivial_rep_mult": trivial_mult,
        "readout": _readout_trichotomy(trivial_mult),
        "live_inventory": n_generations == 3,
    }


# The banked quantum numbers of the nine V_61 classes, (su3_dim, su2_dim, 3*Y_doubled)
# with Y in the doubled (Q = T3 + Y/2) convention scaled by 3 to stay integer --
# the signatures the formal_kernel inventory carries in prose, here as data the
# check verifies claims AGAINST (audit fix 2: quantum numbers computed, not narrated).
_V61_QUANTUM_NUMBERS = {
    ("fermion", "Q_L"): (3, 2, 1),
    ("fermion", "u_R"): (3, 1, 4),
    ("fermion", "d_R"): (3, 1, -2),
    ("fermion", "L_L"): (1, 2, -3),
    ("fermion", "e_R"): (1, 1, -6),
    ("higgs", "doublet_Y=1/2"): (1, 2, 3),
    ("gauge", "SU3_adj"): (8, 1, 0),
    ("gauge", "SU2_adj"): (1, 3, 0),
    ("gauge", "U1"): (1, 1, 0),
}


def check_T_sm_interface_generation_qutrit_readings() -> Dict:
    """The generation index is the SM interface's contextuality-capable
    multiplicity space: the functional applied to the bank's own V_61.

    Reading step, stated first: V_61 -- the 45+4+12 capacity carrier -- is
    treated as declared rep content under G_SM, exactly as a hadron word is,
    with the record algebra its commutant. Precedents: the .326 slot machinery
    already treats V_61 as a G_SM representation with isotypic signatures; the
    banked CKM delimiter (check_T_ckm_flavour_coavailability_is_sepstr)
    already works on "a generation qutrit". The gauge-invariant-record reading
    grade [P_structural_reading] is inherited (fence ii of the module).

    THE CONVENTION, RULED (principal, 2026-07-02; record: APF Reference Docs/
    Reference - Decisions List - Consolidation of the 2026-07-02 Threads.md +
    the V61 conjugation-fork survey note; grounds re-weighted per the
    same-day cold audit of the record): fields-as-written is the CANONICAL
    class accounting for V_61 -- each field its own G_SM class, conjugates
    distinct. THE GROUND THAT CARRIES THE RULING: the banked ledger machinery
    itself (the .326 inventory, its tripwires, the L_count slot conventions)
    is built fields-as-written, and the alternative has no corpus support --
    the ruling keeps one class accounting in circulation. UNIFORMITY, not
    breakage: the Y-weighted chain (anomaly system, b_Y, sin^2theta_W) is
    computed on the field-theory template's complex classes and would be
    untouched by a ledger-scoped alternative. The banked Yukawa H -> H~
    pricing concerns a same-field step orthogonal to the ledger merge --
    carried as colour, not ground. The conjugation-closed alternative is NOT
    erased: it is carried below as the disclosed counter-profile, as data.

    WHAT IS CERTIFIED (from the live banked inventory, exact, under the
    ruled convention):
      (1) THE PROFILE. The commutant of G_SM on V_61 is
          M_3^{(x)5} (+) C^{(x)4}: five multiplicity-3 blocks -- one per
          fermion class Q_L, u_R, d_R, L_L, e_R, the generation index the
          multiplicity space in every case -- and four multiplicity-1 lines
          (the Higgs class, the .326 mult-1 fact, and the three gauge
          classes). Blocks pinned [3,3,3,3,3,1,1,1,1]. The nine classes'
          quantum numbers are carried as data and verified: the five fermion
          classes pairwise distinct (no accidental isotypic merging), the
          U(1) gauge line the unique zero-charge singlet, e_R dim-1 but
          hypercharge-charged. THE COUNTER-PROFILE, carried as data: the
          Higgs class (1,2,+1) is the conjugate of L_L (1,2,-1), so the
          conjugation-closed (realified) alternative merges {H, L_L x3}
          into one multiplicity-4 class -- counter-profile blocks
          [4,3,3,3,3,1,1,1], hosting BOTH state-independent classes
          (computed and pinned below; non-canonical per the ruling, never
          erased). Type note (audit-hardened): under the conjugation-closed
          real-linear reading the merged block has endomorphism algebra C
          ((1,2,+-1/2) has Y != 0, hence complex type despite SU(2)
          pseudoreality), so it is M_4(C) and the ladder's complex-block
          arithmetic applies unchanged; every block >= 3 in both profiles is
          complex-type, the gauge lines real-type at multiplicity 1
          (class-inert). V_61 is a role ledger mixing complex Weyl slots with
          real gauge/Higgs slots; the ruled convention matches the fields
          as written.
      (2) THE READINGS. Max block 3: every fermion class hosts the KCBS and
          Yu-Oh configurations (the generation qutrit); the parity class is
          absent -- no block divisible by 4, and by
          check_T_magic_square_solution_group_rep_forces_4n that absence is
          construction-independent under the ruled convention (the
          counter-profile flips it -- the disclosed data row below). The
          unique trivial-rep line
          is the U(1) gauge direction: multiplicity 1, the interface's one
          canonical frame-free record.
      (3) THE GENERATION-COUNT TRICHOTOMY. Recomputing the profile at
          counterfactual generation counts: n_g = 2 puts every fermion block
          at the Gleason/KS dimension fence -- NO contextuality-capable class
          anywhere on the interface; n_g = 3 (the banked count) is the
          MINIMAL KS-capable generation space, hosting Yu-Oh but no parity
          square; n_g = 4 would onset the parity square on every fermion
          class (4 | 4) and lose the Yu-Oh rung (3 does not divide 4). The
          derived three-generation content sits exactly at the
          Yu-Oh-capable, parity-free point. The counterfactuals hold the
          five-class list fixed across generation counts -- warranted
          physically by anomaly cancellation holding per generation.
          Composition with the banked
          generation count is one-directional: N_gen = 3 is derived upstream
          (the T4G family); this check consumes it and adds the reading map
          -- no circularity, and no claim that contextuality capability
          selects the generation count.
      (4) ENGINE ROUTING. The Yu-Oh scenario, routed with V_61-generation-
          qutrit provenance, returns IJC_OBSTRUCTION with no global-P export.

    EXPLICIT NON-CLAIMS (the .303 fence, verbatim discipline): what is FORCED
    on the QUARK generation qutrit is exactly two orthonormal bases (the mass
    bases related by CKM), and forced-only structure is SepStr -- the banked
    delimiter stands untouched; for the lepton classes no forced-structure
    delimiter is banked and this check asserts capability only. This check certifies the CAPABILITY ceiling
    (the full qutrit algebra hosts Yu-Oh) and the whole-interface placement;
    whether the world occupies the capable structure (all-nine-densities
    co-availability) stays the empirical QAC. The co-availability lead is
    NOT closed here; it is given its computed structural half.

    Grade P_structural_instrument tier 4. Occupancy not claimed; spectrum
    untouched; the reading grade inherited, not upgraded.
    """
    failures: List[str] = []

    prof = sm_interface_profile(3)
    if not prof["live_inventory"]:
        failures.append("n_g=3 profile must consume the live inventory")
    if prof["blocks"] != [3, 3, 3, 3, 3, 1, 1, 1, 1]:
        failures.append("V_61 commutant blocks should be [3x5, 1x4]: %s" % (prof["blocks"],))
    fermion_rows = [r for r in prof["rows"] if r["sector"] == "fermion"]
    if sorted(r["irrep"] for r in fermion_rows) != ["L_L", "Q_L", "d_R", "e_R", "u_R"]:
        failures.append("fermion classes should be the five per-generation irreps")
    if any(r["mult"] != 3 for r in fermion_rows):
        failures.append("every fermion class must carry generation multiplicity 3")
    dim_total = sum(r["dim"] * r["mult"] for r in prof["rows"])
    if dim_total != 61:
        failures.append("inventory dims x mults must total 61: %d" % dim_total)
    cls = prof["classes"]
    if not ("KCBS_STATE_DEPENDENT" in cls and "YU_OH_STATE_INDEPENDENT" in cls):
        failures.append("n_g=3 must host KCBS + Yu-Oh: %s" % (cls,))
    if ("MAGIC_SQUARE_STATE_INDEPENDENT" in cls
            or "MAGIC_SQUARE_STATE_DEPENDENT" in cls
            or "GENERAL_DIM_KS_NOT_INSTANTIATED" in cls):
        failures.append("n_g=3 parity/state-dep-square classes must be absent "
                        "(max block 3; absence invariant by the 4|n rigidity): %s" % (cls,))
    if prof["trivial_rep_mult"] != 1 or prof["readout"]["verdict"] != "CANONICAL_RECORD":
        failures.append("the U(1) line should be the unique canonical record")

    # quantum numbers verified as data (audit fix 2), cross-pinned to the inventory
    inv_keys = {(r["sector"], r["irrep"]) for r in prof["rows"]}
    if inv_keys != set(_V61_QUANTUM_NUMBERS):
        failures.append("quantum-number table keys must match the live inventory exactly")
    fermion_qn = [_V61_QUANTUM_NUMBERS[k] for k in _V61_QUANTUM_NUMBERS if k[0] == "fermion"]
    if len(set(fermion_qn)) != 5:
        failures.append("the five fermion classes must be pairwise distinct irreps")
    if _V61_QUANTUM_NUMBERS[("fermion", "e_R")][2] == 0:
        failures.append("e_R must be hypercharge-charged (dim-1 is not trivial)")
    trivial_keys = [k for k, qn in _V61_QUANTUM_NUMBERS.items() if qn == (1, 1, 0)]
    if trivial_keys != [("gauge", "U1")]:
        failures.append("the U(1) gauge line must be the unique zero-charge singlet: %s"
                        % (trivial_keys,))
    # the disclosed conjugation sensitivity, verified as arithmetic: H = conj(L_L)
    hq = _V61_QUANTUM_NUMBERS[("higgs", "doublet_Y=1/2")]
    lq = _V61_QUANTUM_NUMBERS[("fermion", "L_L")]
    if not (hq[0] == lq[0] and hq[1] == lq[1] and hq[2] == -lq[2]):
        failures.append("the disclosed H = conj(L_L) sensitivity should hold in the data")
    # the counter-profile (the conjugation-closed alternative), pinned as data:
    # merge {H, L_L x3} into one class, everything else unchanged
    cp_blocks = []
    merged = 0
    for r in prof["rows"]:
        if (r["sector"], r["irrep"]) in (("higgs", "doublet_Y=1/2"), ("fermion", "L_L")):
            merged += r["mult"]
        else:
            cp_blocks.append(r["mult"])
    cp_blocks.append(merged)
    cp_blocks = sorted(cp_blocks, reverse=True)
    if cp_blocks != [4, 3, 3, 3, 3, 1, 1, 1]:
        failures.append("counter-profile blocks should be [4,3,3,3,3,1,1,1]: %s" % (cp_blocks,))
    cp_cls = reading_classes(cp_blocks)
    if not ("MAGIC_SQUARE_STATE_INDEPENDENT" in cp_cls and "YU_OH_STATE_INDEPENDENT" in cp_cls):
        failures.append("counter-profile should host BOTH state-independent classes: %s" % (cp_cls,))

    # (3) the generation-count trichotomy
    p2 = sm_interface_profile(2)
    if p2["blocks"] != [2, 2, 2, 2, 2, 1, 1, 1, 1]:
        failures.append("n_g=2 blocks wrong: %s" % (p2["blocks"],))
    if p2["classes"] != ("GLEASON_DIM2_FENCE",):
        failures.append("n_g=2 must be Gleason-fenced everywhere: %s" % (p2["classes"],))
    p4 = sm_interface_profile(4)
    if p4["blocks"] != [4, 4, 4, 4, 4, 1, 1, 1, 1]:
        failures.append("n_g=4 blocks wrong: %s" % (p4["blocks"],))
    if "MAGIC_SQUARE_STATE_INDEPENDENT" not in p4["classes"]:
        failures.append("n_g=4 must onset the parity square (4|4): %s" % (p4["classes"],))
    if "YU_OH_STATE_INDEPENDENT" in p4["classes"]:
        failures.append("n_g=4 must NOT host the Yu-Oh rung (3 does not divide 4)")

    # (4) engine routing: Yu-Oh with V_61 provenance
    from apf.ijc_feasbool_engine import scenario_to_dict
    from apf.interface_contextuality_adapter import route_contextuality
    from apf.gauge_invariant_record import _gic_yuoh_scenario
    scn, _r, _t, _p = _gic_yuoh_scenario()
    pipe = route_contextuality("dcr_v61_generation_qutrit_yuoh",
                               scenario=scenario_to_dict(scn))
    if not (pipe.solver_status == "IJC_OBSTRUCTION" and not pipe.export_global_P
            and pipe.obstruction):
        failures.append("V_61 generation-qutrit Yu-Oh routing verdict wrong")

    passed = not failures
    return {
        "name": "check_T_sm_interface_generation_qutrit_readings",
        "tier": 4,
        "epistemic": "P_structural_instrument",
        "passed": passed,
        "failures": failures,
        "key_result": ("the functional on the bank's own V_61, under the RULED "
                       "fields-as-written convention (principal 2026-07-02): commutant "
                       "M_3^(x5) (+) C^(x4) from the live inventory -- the "
                       "generation index IS the multiplicity space of every fermion "
                       "class; Yu-Oh capable at every fermion role, parity square "
                       "absent (construction-independent under the convention; the "
                       "conjugation-closed counter-profile [4,3,3,3,3,1,1,1] carried "
                       "as pinned data, hosts both classes), "
                       "the U(1) line the unique canonical "
                       "record. Generation trichotomy pinned: n_g=2 fenced "
                       "everywhere / n_g=3 minimal KS-capable (the derived count) / "
                       "n_g=4 parity onsets. Forced-two-bases SepStr (.303) stands; "
                       "capability ceiling only, occupancy stays the QAC"),
        "profile": {"blocks": prof["blocks"], "trivial_rep_mult": prof["trivial_rep_mult"]},
        "summary": ("PASS" if passed else "FAIL: %s" % failures),
    }


# =====================================================================
# v0.4: the gluonic alphabet and the coverage sweep
# =====================================================================

def check_T_gluonic_content_readings() -> Dict:
    """Gluonic content accelerates the contextuality onset: the readings of
    glueball and hybrid contents, computed from the adjoint-extended alphabet.

    The adjoint factor enters by the exact identity f (x) fbar = adj (+) triv
    (subtraction path, positivity asserted at every step; validated here
    against the hand-known 8 (x) 8 table and against dimension products).

    THE LANDMARK ROWS (SU(3), the physical group), all pinned:
      * The two-gluon glueball gg: blocks [2,1,1,1,1], singlet multiplicity 1
        -- Gleason-fenced WITH the canonical record, the gluonic parallel of
        the baryon: the scalar-glueball interface is classically readable and
        hosts no contextuality of any class.
      * The hybrid q qbar g: blocks [3,1,1,1,1], singlet multiplicity 1 --
        Yu-Oh capable at THREE constituents. Gluonic content beats the
        pure-quark onset (four constituents, the v0.2 census): one gluon
        substitutes for a quark pair in reaching the octet multiplicity
        (count-metric, not capacity: the hybrid carrier is 72-dim against
        the tetraquark's 81). And the hybrid is the first SU(3) content in
        the census holding a canonical frame-free record AND a contextuality
        class TOGETHER (the baryon has the record without the classes; the
        tetraquark the classes without the record; in SU(2) the three-gluon
        content ties it at three constituents -- blocks [3,2,1,1], singlet
        1, pinned below -- so the record-with-contextuality corner opens at
        three constituents in both groups, gluonically).
      * The three-gluon glueball ggg: blocks [8,6,4,4,2,2,2,1], singlet
        multiplicity 2 -- the parity square onsets (4|8, 4|4) and the
        two-singlet readout obstruction is the d/f coupling pair (the two
        independent three-gluon invariants: d_abc in Sym^3(8), f_abc in
        Lambda^3(8)), read in IE currency as the m=2 multiplicity-frame
        obstruction.
      * SU(2) gg: blocks [1,1,1] -- fully abelian (3 (x) 3 multiplicity-free),
        the control showing the gluonic onset is group-sensitive.
    Engine routing at the hybrid onset: the Yu-Oh scenario with hybrid
    provenance returns IJC_OBSTRUCTION, no global-P export.

    Fences inherited from the module (occupancy/QAC; reading grade;
    spectrum-blind -- nothing here concerns glueball or hybrid MASSES).
    Grade P_structural_instrument tier 4.
    """
    failures: List[str] = []

    # subtraction-path validation: 8 (x) 8 against the hand-known table
    gg = decompose_general(3, ("adjoint", "adjoint"))
    known_88 = {(0, 0): 1, (1, 1): 2, (3, 0): 1, (0, 3): 1, (2, 2): 1}
    if gg != known_88:
        failures.append("8 (x) 8 must be 1 + 8 + 8 + 10 + 10bar + 27: %s" % (gg,))
    # fund/antifund-only agreement with the banked paths (the twin-implementation
    # anti-drift guard, widened per audit: every f/a word to length 4, both groups)
    from itertools import product as _iproduct2
    for N in (2, 3):
        for L in (1, 2, 3, 4):
            for w in _iproduct2(("fund", "antifund"), repeat=L):
                if decompose_general(N, w) != (su2_decompose(w) if N == 2 else su3_decompose(w)):
                    failures.append("general path must reproduce the banked f/a path "
                                    "(SU(%d) %s)" % (N, w))

    def prof(N, word):
        p = commutant_profile(N, word)
        if not p["dim_check_pass"]:
            failures.append("dim product failed: SU(%d) %s" % (N, word))
        return p

    p_gg = prof(3, ("adjoint", "adjoint"))
    if not (p_gg["blocks"] == [2, 1, 1, 1, 1] and p_gg["singlet_mult"] == 1
            and reading_classes(p_gg["blocks"]) == ("GLEASON_DIM2_FENCE",)):
        failures.append("SU(3) gg should be Gleason-fenced with the canonical record")

    p_hyb = prof(3, ("fund", "antifund", "adjoint"))
    cls_hyb = reading_classes(p_hyb["blocks"])
    if not (p_hyb["blocks"] == [3, 1, 1, 1, 1] and p_hyb["singlet_mult"] == 1
            and "YU_OH_STATE_INDEPENDENT" in cls_hyb
            and "MAGIC_SQUARE_STATE_DEPENDENT" not in cls_hyb):
        failures.append("SU(3) hybrid q-qbar-g should be Yu-Oh capable at 3 constituents "
                        "with the canonical record: %s %s" % (p_hyb["blocks"], cls_hyb))
    if _readout_trichotomy(p_hyb["singlet_mult"])["verdict"] != "CANONICAL_RECORD":
        failures.append("the hybrid must hold the canonical record")

    p_ggg = prof(3, ("adjoint",) * 3)
    cls_ggg = reading_classes(p_ggg["blocks"])
    if not (p_ggg["blocks"] == [8, 6, 4, 4, 2, 2, 2, 1] and p_ggg["singlet_mult"] == 2
            and "MAGIC_SQUARE_STATE_INDEPENDENT" in cls_ggg):
        failures.append("SU(3) ggg should host the parity square with singlet mult 2 "
                        "(the d/f pair): %s" % (p_ggg["blocks"],))
    if _readout_trichotomy(p_ggg["singlet_mult"])["verdict"] != "NON_CANONICAL_MULTIPLICITY":
        failures.append("ggg's two singlets are the m=2 frame obstruction")

    p_gg2 = prof(2, ("adjoint", "adjoint"))
    if not (p_gg2["blocks"] == [1, 1, 1]
            and reading_classes(p_gg2["blocks"]) == ("ABELIAN_SEP",)):
        failures.append("SU(2) gg should be abelian (multiplicity-free)")
    p_ggg2 = prof(2, ("adjoint",) * 3)
    if not (p_ggg2["blocks"] == [3, 2, 1, 1] and p_ggg2["singlet_mult"] == 1
            and "YU_OH_STATE_INDEPENDENT" in reading_classes(p_ggg2["blocks"])):
        failures.append("SU(2) ggg should tie the record+contextuality corner "
                        "at 3 constituents: %s" % (p_ggg2["blocks"],))

    # engine routing at the hybrid onset
    from apf.ijc_feasbool_engine import scenario_to_dict
    from apf.interface_contextuality_adapter import route_contextuality
    from apf.gauge_invariant_record import _gic_yuoh_scenario
    scn, _r, _t, _p = _gic_yuoh_scenario()
    pipe = route_contextuality("dcr_su3_hybrid_qqbarg_yuoh", scenario=scenario_to_dict(scn))
    if not (pipe.solver_status == "IJC_OBSTRUCTION" and not pipe.export_global_P
            and pipe.obstruction):
        failures.append("hybrid Yu-Oh routing verdict wrong")

    passed = not failures
    return {
        "name": "check_T_gluonic_content_readings",
        "tier": 4,
        "epistemic": "P_structural_instrument",
        "passed": passed,
        "failures": failures,
        "key_result": ("gluonic alphabet landed: SU(3) gg Gleason-fenced w/ canonical "
                       "record (the gluonic baryon-parallel); the hybrid q-qbar-g is "
                       "Yu-Oh capable at THREE constituents (gluonic content beats the "
                       "pure-quark onset) and is the first SU(3) content holding record "
                       "AND contextuality together (SU(2) ggg ties, pinned); ggg hosts "
                       "the parity square w/ the d/f "
                       "two-singlet frame obstruction; SU(2) gg abelian control"),
        "summary": ("PASS" if passed else "FAIL: %s" % failures),
    }


def check_T_reading_coverage_sweep() -> Dict:
    """The coverage sweep, and the first genuine honest-open content.

    THE RESULT, both halves pinned. Over the pure fund/antifund surface --
    pairs to m = 12, mixed (k, l) words to k+l = 10, both groups -- every
    content whose profile carries a block >= 3 also carries a 3|n or 4|n
    certificate: the honest-open flag fires nowhere (the QUARK-CONTENT
    coverage observation, empirical within these bounds, its general form an
    open Littlewood-Richardson divisibility question -- named, not claimed).
    But the coverage is NOT a law of the full alphabet: the gluonic sweep
    (fund/antifund/adjoint words to total length 8 for SU(2), 6 for SU(3))
    finds the FIRST GENUINE HONEST-OPEN CONTENT at SU(2) five quarks + three
    gluons -- blocks [59, 46, 43, 23, 7, 1], no block divisible by 3 or 4 --
    a content whose profile hosts KCBS and the state-dependent square but
    carries NO state-independent certificate this module can construct.
    General dim-n KS sets exist (dim >= 3), so the content's
    state-independent status is genuinely open at exactly the module's
    construction strength: the flag is doing on real content the job it was
    built for. The audit that found it (one word past the draft sweep bound)
    is the reason the bound now sits at 8: a "zero-firer law" whose
    refutation was one loop-iteration away does not get pinned as a law.

    Both facts fail loudly under drift: a new firer inside the pure-quark
    bounds, a vanished firer at (5f, 3g), or a changed firer set in the
    gluonic sweep all fail the check (re-adjudicate, do not silence). Three
    constructed non-content profiles verify the flag detector itself is
    live. Counting note: the sweep evaluates ~280 profiles over fewer
    distinct contents (pairs recur inside the mixed table; SU(2)
    fund = antifund) -- the pinned numbers count PROFILES.
    Grade P_structural_instrument tier 4.
    """
    failures: List[str] = []
    profiles = 0
    quark_firers = []
    for N in (2, 3):
        for m in range(1, 13):
            p = commutant_profile(N, ("fund", "antifund") * m)
            profiles += 1
            if "GENERAL_DIM_KS_NOT_INSTANTIATED" in reading_classes(p["blocks"]):
                quark_firers.append(("pairs", N, m))
        for k in range(0, 11):
            for l in range(0, 11 - k):
                if k + l == 0 or k < l:
                    continue
                p = commutant_profile(N, ("fund",) * k + ("antifund",) * l)
                profiles += 1
                if "GENERAL_DIM_KS_NOT_INSTANTIATED" in reading_classes(p["blocks"]):
                    quark_firers.append(("mixed", N, (k, l)))
    if quark_firers:
        failures.append("pure-quark coverage observation broken (a genuine result -- "
                        "re-adjudicate, do not silence): %s" % quark_firers[:6])

    gluonic_firers = []
    for N, maxlen in ((2, 8), (3, 6)):
        for total in range(1, maxlen + 1):
            for nf in range(total + 1):
                for na in range(total - nf + 1):
                    ng = total - nf - na
                    if N == 3 and nf < na:
                        continue
                    word = ("fund",) * nf + ("antifund",) * na + ("adjoint",) * ng
                    p = commutant_profile(N, word)
                    profiles += 1
                    if not p["dim_check_pass"]:
                        failures.append("dim failed: SU(%d) f%d a%d g%d" % (N, nf, na, ng))
                    if "GENERAL_DIM_KS_NOT_INSTANTIATED" in reading_classes(p["blocks"]):
                        gluonic_firers.append((N, nf, na, ng, tuple(p["blocks"])))
    # the discovered firer, pinned exactly (SU(2) fund=antifund: the sweep
    # visits the (5,0,3) content once per (nf,na) split of the 5 quarks --
    # every visit must agree on the profile)
    expected_blocks = (59, 46, 43, 23, 7, 1)
    firer_contents = {(N, nf + na, ng) for (N, nf, na, ng, _b) in gluonic_firers}
    if firer_contents != {(2, 5, 3)}:
        failures.append("the gluonic firer set must be exactly SU(2) 5 quarks + 3 gluons: %s"
                        % (sorted(firer_contents),))
    if any(b != expected_blocks for (_N, _f, _a, _g, b) in gluonic_firers):
        failures.append("the (5q,3g) firer profile must be [59,46,43,23,7,1]")
    if profiles < 270:
        failures.append("sweep should cover 270+ profiles: %d" % profiles)
    # the flag detector itself is live (constructed non-content profiles)
    for probe in ([5, 1], [7, 2], [11, 5]):
        if "GENERAL_DIM_KS_NOT_INSTANTIATED" not in reading_classes(probe):
            failures.append("flag dead on %s -- the pins above would be meaningless" % (probe,))

    passed = not failures
    return {
        "name": "check_T_reading_coverage_sweep",
        "tier": 4,
        "epistemic": "P_structural_instrument",
        "passed": passed,
        "failures": failures,
        "key_result": ("coverage sweep, both halves pinned: the pure-quark surface "
                       "(pairs m<=12, mixed k+l<=10) has ZERO honest-open firers "
                       "(empirical observation, general form named-open); the gluonic "
                       "alphabet REFUTES the law -- first genuine honest-open content "
                       "at SU(2) 5 quarks + 3 gluons, blocks [59,46,43,23,7,1], no "
                       "3|n or 4|n block: a real content whose state-independent "
                       "status is open at the module's construction strength "
                       "(%d profiles)" % profiles),
        "profiles": profiles,
        "summary": ("PASS" if passed else "FAIL: %s" % failures),
    }


# =====================================================================
# IE onboarding declarations (claim-grade; the module's scenario payloads are
# the bank's own canonical objects, already atlas-declared by their home
# modules -- re-declaring the same tables under dcr ids would be the re-label
# anti-pattern the .319 axis-depth pass declined. The NEW content is the
# functional itself: declared as letter-accurate claims.)
# =====================================================================

IE_DECLARATIONS = (
    {
        "input_id": "claim:drawn_content_readings_functional",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "The drawn-content -> readings functional [P_structural_instrument]: "
            "a computed map from a colour-interface rep content (SU(N) "
            "fund/antifund word, N in {2,3}) to the IE contextuality/readout "
            "scenarios it hosts, via the exact complete commutant profile. "
            "Block-graded ladder (abelian / dim-2 fence / KCBS n>=3 / Yu-Oh "
            "3|n inequality-sense / magic-square 4|n coloring-sense / "
            "honest-open flag), census pinned: both SU(2) and SU(3) pairs "
            "reach state-independent contextuality at m=2 and keep it "
            "(union persistent m=2..5) while each certificate class flickers; "
            "the baryon (3,0) is Gleason-fenced with the canonical record; "
            "4 constituents is the contextuality onset. The gauge-invariant"
            "-record reading grade [P_structural_reading] is inherited, not "
            "upgraded; occupancy stays the QAC."
        ),
        "note": "the .306 open object closed at v0.2 strength (banked "
                "v24.3.328/.329); scenario payloads live with their home "
                "modules -- this claim onboards the generative map itself",
    },
    {
        "input_id": "claim:magic_square_4n_rigidity",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Magic-square parity hostability is 4|n-rigid "
            "[P_structural_instrument]: the real 2-qubit Pauli group (order "
            "32, 17 conjugacy classes, [G,G]={1,J}) has exactly one "
            "non-linear irrep, of dimension exactly 4, so every rep with "
            "J -> -I has 4|n; the standard Mermin square is verified as a "
            "solution in G and as exact integer matrices. ONE named cited "
            "step: the abstract solution group is isomorphic to G "
            "(Mermin 1990 / Cleve-Mittal 2014 / Cleve-Liu-Slofstra 2017), "
            "admitted as instrument."
        ),
        "note": "upgrades the ladder's parity column from constructive to "
                "characterized: a parity off-cell is an invariant absence",
    },
)


_CHECKS = {
    "T_drawn_content_readings_functional": check_T_drawn_content_readings_functional,
    "T_magic_square_solution_group_rep_forces_4n": check_T_magic_square_solution_group_rep_forces_4n,
    "T_sm_interface_generation_qutrit_readings": check_T_sm_interface_generation_qutrit_readings,
    "T_gluonic_content_readings": check_T_gluonic_content_readings,
    "T_reading_coverage_sweep": check_T_reading_coverage_sweep,
}


def register(registry):
    registry.update(_CHECKS)


if __name__ == "__main__":
    for nm, fn in _CHECKS.items():
        r = fn()
        print(nm, "->", r["summary"] if r["passed"] else r["summary"][:800])
        print("  ", r["key_result"][:300])
# end of module
