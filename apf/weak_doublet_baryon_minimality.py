"""L_weak_doublet_baryon_minimality and L_least_capacity_content_infrared.

Banked v24.3.507 (2026-11-11).  Lifted by Ethan 2026-11-11 ("land it now")
after one cold blinded audit of the round-1 build (LAND-WITH-FIXES for both
checks; no mathematical defect; every claimed number reproduced by
independent code) and a mechanical verification of the round-2 fixes (54
mutants in fresh processes).  The round-2 code has had no second cold
audit: taken on the principal's call.  Registered with bare-name keys per
D6@2026-08-03.  Built against a frozen claim surface (v2).  Standard
library only; exact rational arithmetic.

WHAT IS COMPUTED.  Finite statements about multisets of representations of
SU(3) x SU(2) x U(1)^r.

SETTING (part of the claim).  A multiplet is (c, d): c in {'1', '3', '3b'}
(trivial, fundamental, antifundamental of SU(3)), d >= 1 the dimension of an
irreducible representation of SU(2).  It has dim(c) * d states.  A content
is a finite multiset of multiplets, read as left-handed Weyl fields; with r
abelian factors each multiplet also carries r rational charges, and ANY r
charge vectors are allowed, zero and linearly dependent ones included.  With
T(d) = d (d^2 - 1) / 12 and B = 0, +1/3, -1/3 on c = '1', '3', '3b':
  A3    = sum_{c='3'} d - sum_{c='3b'} d              colour cubic
  W     = sum dim(c) [d = 2 mod 4]  mod 2             Witten parity
  beta2 = sum B(c) dim(c) T(d)                        SU(2)^2 - B
  beta3 = sum B(c) (1/2) [c != '1'] d                 colour^2 - B
A content is ADMITTED when A3 = 0, W = 0 and beta2 != 0.  Its coloured core
is the sub-multiset with c != '1'.  CAPACITY (an authored functional) is
states + dim G + real components of the scalar, dim G = 8 + 3 + r; a scalar
(1, d_S, y_S) has d_S real components when d_S is odd and y_S = 0, and
2 d_S otherwise.

INFRARED CRITERION (check B; part of that claim).  One colour-neutral
scalar irrep S.  Couplings: the G-invariant bilinear forms on the content
and the G-invariant trilinear forms on (multiplet, multiplet, S) and on
(multiplet, multiplet, conjugate of S).  A ground vector is a weight vector
of S; for a real irrep (d_S odd, y_S = 0) the weight-zero vector.  (The
claim surface uses the customary one-word name for the scalar's
lowest-energy configuration.  That word is a reserved token of the bank's
which-v drift net, so this file writes 'ground vector' throughout.)
(i) some element of the Cartan algebra of SU(2) x U(1)^r annihilating the
ground vector's weight acts non-trivially on some state; (ii) for some coupling
coefficients the mass form has full rank on the set C of states that are
coloured or charged under the elements of (i).

PROVED IN TEXT, NOT COMPUTED.
T1. A simple Lie algebra (complex, or compact real) with a non-trivial
    representation of dimension at most two is sl(2): the representation
    is faithful (the kernel is an ideal), traceless (the algebra is
    perfect), so it embeds in sl(2), of dimension three; and no simple Lie
    algebra has dimension below three (those are solvable).  So a simple
    factor other than SU(2) acting non-trivially on a coloured multiplet,
    the multiplet being a tensor product of a colour triplet or antitriplet
    with its representation, puts it in dimension >= 3, and with A3 = 0
    that needs at least 18 coloured states.  No computed claim uses T1;
    it carries the reading R2 to factors other than SU(2).
T2. Every model satisfying (ii) with beta2 != 0 has a scalar carrying a
    non-trivial SU(2) representation: the coloured block of the mass form
    pairs triplets with antitriplets; if the scalar were absent or an
    SU(2) singlet that block would be SU(2)-invariant, and full rank would
    make the triplets and the antitriplets conjugate as SU(2)
    representations, giving beta2 = 0.  The least such scalar has 3 real
    components, so every such model with 18 or more states has capacity at
    least 18 + 11 + 3 = 32.
T3. Every scalar irrep inside the window that has a coupling is a singlet,
    a doublet or a real triplet (this half is COMPUTED in check B), and
    for those every ground direction is gauge-equivalent to a weight
    vector (the weight-zero one for the real triplet).  A scalar with no
    coupling leaves the bare form, which fails (ii) at every ground vector
    (COMPUTED).
T4. The term rank of the support pattern bounds the rank of the mass form
    for every choice of coefficients: a non-zero k x k minor needs k
    non-zero entries in distinct rows and columns.  (No independence of
    the entries is needed; the converse is false and is not used.)
T5. Replacing the r charge vectors by invertible rational combinations of
    themselves relabels the abelian generators; the couplings, the
    unbroken subalgebra, the set C and the mass form are unchanged.  So a
    linearly dependent family is equivalent to fewer independent vectors
    together with zero vectors, and a zero vector adds one to dim G and
    nothing else.  At (14 states, r = 2) the linear conditions leave a
    line, so every pair is dependent and is equivalent to (y, 0) with y on
    the line of r = 1, or to (0, 0); both are COMPUTED.

NAMED READINGS AND IMPORTS, NOT COMPUTED AND NOT CLAIMED.
R1. That A3, W and the linear and cubic charge conditions are the
    consistency conditions of a gauge theory.
R2. Lemma D: in the class (colour a separate factor; colour
    representations 1, 3, 3b; colour-neutral scalars; renormalisable
    couplings) baryon number is violated if and only if a simple
    non-colour factor has non-zero mixed coefficient with B.  A
    continuum-side instrument (anomaly equation, instanton index).
R3. The premise (BV): baryon number is violated by the counted content.
    Adopted by ruling 2026-11-11; derived nowhere.
R4. That capacity as defined here is the quantity minimised.
R5. That the infrared criterion is the right physical requirement.

Frozen claim surface (v2):
FROZEN_CLAIM_SURFACE_v2_weak_doublet_baryon_minimality_2026-11-11.md
"""
from fractions import Fraction as F
from itertools import product
from math import gcd

HELD_OUT_OF_THE_BANK = False  # BANKED v24.3.507 (2026-11-11); lifted by Ethan; register() below

CLAIM_SURFACE_SHA256 = (
    "7e89e88101fc265e493bb342868e966d4f070c566e006c227fc5a02dcd9b866f")

MAY_NOT_CITE = (
    "R2, chirality, SU(2) or the doublet as derived from A1, or as forced "
    "without the premise (BV)",
    "(BV) as a theorem of the framework, or L_Sakharov as its source",
    "Lemma D as computed here: the coefficients are computed, the lemma "
    "is a named reading and a continuum-side instrument",
    "minimality outside the class: colour sextets or octets, coloured "
    "scalars, colour inside a larger simple group, more than one scalar "
    "irrep, non-renormalisable couplings",
    "minimality with more than one non-colour simple factor",
    "the number of generations, any phase, or CP",
    "the charge values as derived without the infrared criterion, or the "
    "survivor as selected without criterion (i), its clause 'acts "
    "non-trivially' included",
    "any statement about two or more abelian factors beyond the 14-state "
    "content, whose linear conditions leave a line",
    "the window value 31 as derived, or any ordering above it: other "
    "models pass at 32; the survivor's margin is one unit of an authored "
    "functional",
    "that every state of the survivor is paired: one colourless state, "
    "neutral under the unbroken element, lies outside C and is unpaired",
    "that the exhibited 18-state content can satisfy the infrared "
    "criterion",
    "completeness of the anomaly conditions beyond those the setting "
    "defines",
    "proton stability, T_proton, or the exactness of baryon number",
    "capacity 61, C_total or L_count as derived or supported here",
    "that no model outside the window cases exists at capacity <= 31 "
    "without the text results T2, T3 and T5",
    "the soundness of any banked check: none is consumed",
)

EXPECTED_LEGS = {
    "L_weak_doublet_baryon_minimality": [
        "formulas_match_state_traces",
        "colour_baryon_coefficient_tracks_colour_cubic",
        "admitted_contents_share_one_coloured_core",
        "no_coloured_doublet_needs_eighteen_states",
        "controls_computed",
    ],
    "L_least_capacity_content_infrared": [
        "window_cases",
        "abelian_charge_solutions_exact",
        "infrared_verdicts_certified",
        "unique_survivor",
        "controls_computed",
    ],
}

# ---- pins frozen in the claim surface --------------------------------------
FMAX = 17
SHARP_STATES = 18
WINDOW = 31
_CORE = (("3", 1), ("3", 1), ("3b", 2))
ADMITTED_CONTENTS = tuple(tuple(sorted(extra + _CORE)) for extra in (
    (("1", 2),),
    (("1", 1), ("1", 2)),
    (("1", 1), ("1", 1), ("1", 2)),
    (("1", 1), ("1", 1), ("1", 1), ("1", 2)),
    (("1", 2), ("1", 3)),
))
ADMITTED_STATE_COUNTS = (14, 15, 16, 17, 17)
WINDOW_CASES = ((14, 0), (14, 1), (14, 2), (15, 0), (15, 1), (16, 0))
SOLUTION_LINES = {14: 1, 15: 3}
# charges on (X,2), the two (Xbar,1) in increasing order, (1,2), (1,1),
# scaled so that the coloured doublet has charge 1
SURVIVOR_CHARGES = (1, (-4, 2), -3, 6)
SURVIVOR_SCALAR = (2, 3)            # SU(2) dimension, |charge| in those units
SURVIVOR_CAPACITY = 31
SURVIVOR_STATES = 15
# ---- recorded at build, not claims of the surface -----------------------------
BUILD_ENUMERATION_SIZE = 4396
BUILD_VERDICTS = {"FAIL_i": 12, "FAIL_ii": 30, "PASS": 4}
BUILD_NO_COUPLING = 41
BUILD_OUTSIDE_WINDOW = 173
# ---- authored parameters of the scan and of the controls ------------------------
DS_MAX = 8                 # scalar SU(2) dimensions generated as candidates
CHARGE_BOX = 6             # integer box of the brute-force charge search
BENT_D = 3                 # where the controls leg alters T
BUMP = 1                   # by how much it raises a survivor charge
COEFF_SHIFTS = (0, 7)      # offsets into the prime list for PASS certificates
# real components of a charged singlet, a neutral singlet, a neutral doublet,
# a charged doublet, a neutral triplet, a charged triplet (the setting's rule)
REAL_COMPONENT_TABLE = (2, 1, 4, 4, 3, 6)

_NC = {"1": 1, "3": 3, "3b": 3}
_CONJ = {"1": "1", "3": "3b", "3b": "3"}
_B = {"1": F(0), "3": F(1, 3), "3b": F(-1, 3)}
_D3 = {"1": (0,), "3": (1, 1, -2), "3b": (-1, -1, 2)}       # diag(1,1,-2)
_H1 = {"1": (0,), "3": (1, -1, 0), "3b": (-1, 1, 0)}        # diag(1,-1,0)


def _T(d):
    return F(d * (d * d - 1), 12)


def _result(name, legs, key_result, conditional_on, named_readings,
            authored_inputs, disclosures=()):
    fails = []
    have = tuple(sorted(legs))
    want = tuple(sorted(EXPECTED_LEGS[name]))
    if have != want:
        fails.append("leg inventory mismatch: missing=%r extra=%r" % (
            sorted(set(want) - set(have)), sorted(set(have) - set(want))))
    for label in sorted(legs):
        ok, ev = legs[label]
        if not ok:
            fails.append("%s: %s" % (label, ev))
    return {
        "name": name,
        "passed": not fails,
        "tier": 3,
        "epistemic": "P_math",
        "genre_note": (
            "finite representation-theoretic enumeration; the physical "
            "reading (anomaly conditions, Lemma D, the premise BV, "
            "capacity, the infrared criterion) is named and not computed"),
        "legs": {k: {"passed": bool(v[0]), "evidence": v[1]}
                 for k, v in legs.items()},
        "leg_count": len(legs),
        "fail_reasons": fails,
        "key_result": key_result,
        "conditional_on": list(conditional_on),
        "named_readings": list(named_readings),
        "authored_inputs": list(authored_inputs),
        "dependencies": [],
        "disclosures": list(disclosures),
        "may_not_cite": list(MAY_NOT_CITE),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": CLAIM_SURFACE_SHA256,
        "inventory_note": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


# ---------------------------------------------------------------------------
# linear algebra over the rationals
# ---------------------------------------------------------------------------

def _rref(rows, ncols):
    A = [list(r) for r in rows if any(x != 0 for x in r)]
    piv, r = [], 0
    for c in range(ncols):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == len(A):
            break
    return A[:r], piv


def _rank(rows, ncols=None):
    rows = [r for r in rows]
    if not rows:
        return 0
    return len(_rref(rows, ncols if ncols is not None else len(rows[0]))[1])


def _nullspace(rows, ncols):
    A, piv = _rref(rows, ncols)
    out = []
    for fc in (c for c in range(ncols) if c not in piv):
        v = [F(0)] * ncols
        v[fc] = F(1)
        for i, pc in enumerate(piv):
            v[pc] = -A[i][fc]
        out.append(v)
    return out


# ---------------------------------------------------------------------------
# contents and their invariants
# ---------------------------------------------------------------------------

def _states(content):
    """One record per state: (B, D eigenvalue, H1 eigenvalue, H eigenvalue)."""
    out = []
    for c, d in content:
        for a in range(_NC[c]):
            for k in range(d):
                out.append((_B[c], _D3[c][a], _H1[c][a], d - 1 - 2 * k))
    return out


def _size(content):
    return sum(_NC[c] * d for c, d in content)


def _formula_values(content, T=_T):
    a3 = sum(d for c, d in content if c == "3") - sum(
        d for c, d in content if c == "3b")
    w = sum(_NC[c] for c, d in content if d % 4 == 2) % 2
    b2 = sum(_B[c] * _NC[c] * T(d) for c, d in content)
    b3 = sum(_B[c] * F(1, 2) * d for c, d in content if c != "1")
    return a3, w, b2, b3


def _trace_values(content, tamper=None):
    st = _states(content)
    if tamper is not None and st:
        b, dd, h1, h = st[0]
        st[0] = (b, dd, h1, h + tamper)
    a3 = F(sum(s[1] ** 3 for s in st), -6)
    w = (F(sum(s[3] ** 2 for s in st), 2)) % 2
    b2 = sum(s[0] * s[3] ** 2 for s in st) / 4
    b3 = sum(s[0] * s[2] ** 2 for s in st) / 4
    return a3, w, b2, b3


def _menu(fmax):
    return [(c, d) for c in ("3", "3b", "1")
            for d in range(1, fmax // _NC[c] + 1)]


def _contents(fmax, exact=False):
    """All multisets of multiplets with at most fmax states (exactly fmax
    when exact), the empty one excluded."""
    menu = _menu(fmax)
    out = []

    def rec(i, left, cur):
        if i == len(menu):
            if cur and (not exact or left == 0):
                out.append(tuple(cur))
            return
        t = menu[i]
        s = _NC[t[0]] * t[1]
        for m in range(left // s + 1):
            rec(i + 1, left - m * s, cur + [t] * m)

    rec(0, fmax, [])
    return out


def _core(content):
    return tuple(sorted(t for t in content if t[0] != "1"))


def _canon(content):
    a = tuple(sorted(content))
    b = tuple(sorted((_CONJ[c], d) for c, d in content))
    return min(a, b)


def _target_cores():
    return {tuple(sorted([(x, 2), (_CONJ[x], 1), (_CONJ[x], 1)]))
            for x in ("3", "3b")}


def _gf_count(fmax):
    """Number of non-empty multisets of multiplets with at most fmax states,
    from the generating function prod 1 / (1 - x^size); built without the
    enumeration's menu."""
    poly = [1] + [0] * fmax
    for nc in (3, 3, 1):                  # triplet, antitriplet, singlet
        for d in range(1, fmax // nc + 1):
            for k in range(nc * d, fmax + 1):
                poly[k] += poly[k - nc * d]
    return sum(poly) - 1


def check_L_weak_doublet_baryon_minimality():
    name = "L_weak_doublet_baryon_minimality"
    legs = {}
    allc = _contents(FMAX)
    n_all = len(allc)
    vals = [(c, _formula_values(c), _trace_values(c)) for c in allc]

    # ---- 1. formulas against traces over the list of states ----------------
    bad = [c for c, f, t in vals if tuple(f) != tuple(t)]
    gf = _gf_count(FMAX)
    dmax = max(d for c in allc for _, d in c)
    dmax_b = max(d for c in allc for cc, d in c if cc != "1")
    t_direct = [d for d in range(1, FMAX + 1)
                if F(sum((d - 1 - 2 * k) ** 2 for k in range(d)), 4) != _T(d)]
    legs["formulas_match_state_traces"] = (
        not bad and n_all > 0 and isinstance(BUILD_ENUMERATION_SIZE, int)
        and n_all == BUILD_ENUMERATION_SIZE and n_all == gf
        and dmax == FMAX and not t_direct,
        "%d contents with at most %d states (generating-function count %d; "
        "build-recorded %s); the four formula values equal the four state "
        "traces on all but %d; largest SU(2) dimension enumerated %d; T "
        "enters beta2 only through coloured multiplets, largest dimension "
        "%d, so T(d) is also compared with the sum of squared weights over "
        "four for every d up to %d: mismatches %d" % (
            n_all, FMAX, gf, BUILD_ENUMERATION_SIZE, len(bad), dmax,
            dmax_b, FMAX, len(t_direct)))

    # ---- 2. colour^2-B tracks the colour cubic ------------------------------
    off = [c for c, f, t in vals if f[3] != F(f[0], 6) or t[3] != t[0] / 6]
    zero_a3 = [f for c, f, t in vals if f[0] == 0]
    legs["colour_baryon_coefficient_tracks_colour_cubic"] = (
        not off and len(zero_a3) > 0 and all(f[3] == 0 for f in zero_a3),
        "an identity of the definitions, kept as a guard on the "
        "conventions: beta3 = A3 / 6 fails on %d of %d contents (by "
        "formula and by trace); contents with A3 = 0: %d, of which with "
        "beta3 != 0: %d" % (
            len(off), n_all, len(zero_a3),
            sum(1 for f in zero_a3 if f[3] != 0)))

    # ---- 3. the coloured core ----------------------------------------------
    targets = _target_cores()
    nz = [c for c, f, t in vals if f[0] == 0 and f[2] != 0]       # W unused
    wrong_core = [c for c in nz if _core(c) not in targets]
    admitted = sorted(set(_canon(c) for c, f, t in vals
                          if f[0] == 0 and f[1] == 0 and f[2] != 0),
                      key=lambda c: (_size(c), c))
    counts = tuple(_size(c) for c in admitted)
    legs["admitted_contents_share_one_coloured_core"] = (
        not wrong_core and len(nz) > 0
        and counts == ADMITTED_STATE_COUNTS
        and tuple(admitted) == ADMITTED_CONTENTS,
        "contents with A3 = 0 and beta2 != 0 (W not used): %d, with a "
        "coloured core other than one doublet and two conjugate-colour "
        "singlets: %d; admitted contents up to colour conjugation: %d "
        "with state counts %s (pinned %s), equal to the pinned list: %s: "
        "%s" % (
            len(nz), len(wrong_core), len(admitted), counts,
            ADMITTED_STATE_COUNTS, tuple(admitted) == ADMITTED_CONTENTS,
            admitted))

    # ---- 4. the bound is 18 and sharp ---------------------------------------
    no_doublet = [c for c in nz
                  if not any(t[0] != "1" and t[1] == 2 for t in c)]
    witness = (("3", 3), ("3b", 1), ("3b", 1), ("3b", 1))
    wf = _formula_values(witness)
    wt = _trace_values(witness)
    w_ok = (_size(witness) == SHARP_STATES and tuple(wf) == tuple(wt)
            and wf[0] == 0 and wf[1] == 0 and wf[2] != 0
            and not any(t[0] != "1" and t[1] == 2 for t in witness))
    legs["no_coloured_doublet_needs_eighteen_states"] = (
        not no_doublet and len(nz) > 0 and w_ok,
        "contents with at most %d states, A3 = 0, beta2 != 0 and no "
        "coloured multiplet of SU(2) dimension two: %d of %d; exhibited "
        "content %s: %d states (pinned %d), A3 = %s, W = %s, beta2 = %s, "
        "no coloured doublet, formulas equal traces: %s" % (
            FMAX, len(no_doublet), len(nz), witness, _size(witness),
            SHARP_STATES, wf[0], wf[1], wf[2], tuple(wf) == tuple(wt)))

    # ---- 5. controls ----------------------------------------------------------
    no_w = sorted(set(_canon(c) for c in nz))
    c_w = len(no_w) != len(admitted)
    bent = lambda d: _T(d) + (1 if d == BENT_D else 0)
    c_t = sum(1 for c in allc
              if tuple(_formula_values(c, T=bent)) != tuple(_trace_values(c)))
    below = [c for c, f, t in vals if f[0] == 0 and f[1] == 0 and f[2] == 0
             and any(x[0] != "1" for x in c)
             and _size(c) < ADMITTED_STATE_COUNTS[0]]
    odd = sum(1 for c, f, t in vals
              if tuple(f) != tuple(_trace_values(c, tamper=1)))
    even = sum(1 for c, f, t in vals
               if tuple(f) != tuple(_trace_values(c, tamper=2)))
    first_coloured = sum(1 for c in allc if c[0][0] != "1")
    legs["controls_computed"] = (
        c_w and c_t > 0 and len(below) > 0 and odd == n_all
        and even == first_coloured and 0 < even < n_all,
        "without the W filter the set up to conjugation has %d members "
        "against %d admitted; a T altered at d = %d breaks the trace "
        "comparison on %d contents; coloured contents with A3 = 0, W = 0, "
        "beta2 = 0 below %d states: %d (smallest has %d states); a "
        "planted shift of 1 in the first state's SU(2) weight is "
        "detected on %d of %d contents (through W); a shift of 2, "
        "invisible to W, is detected on %d, the number of contents whose "
        "first state is coloured (%d), through beta2" % (
            len(no_w), len(admitted), BENT_D, c_t,
            ADMITTED_STATE_COUNTS[0], len(below),
            min(_size(c) for c in below) if below else -1,
            odd, n_all, even, first_coloured))

    return _result(
        name, legs,
        key_result=(
            "Among all %d contents with at most %d states, each of the %d "
            "with A3 = 0 and beta2 != 0 has the coloured core of one "
            "SU(2) doublet and two conjugate-colour singlets; the "
            "admitted ones are %d up to colour conjugation, with %s "
            "states; none lacks a coloured doublet, and an admitted "
            "content with %d states and no coloured doublet exists; "
            "beta3 = A3 / 6 throughout" % (
                n_all, FMAX, len(nz), len(admitted), counts,
                _size(witness))),
        conditional_on=[],
        named_readings=[
            "T1 (proved in the module text, used by no computed claim): "
            "a simple factor other than SU(2) on a coloured multiplet "
            "needs at least 18 coloured states",
            "R1-R4: the anomaly conditions, Lemma D, the premise (BV) "
            "and capacity; the reading 'the weak factor is SU(2) on a "
            "quark doublet' holds under them and is not a leg",
        ],
        authored_inputs=[
            "the colour scope {1, 3, 3b}",
            "the state bound and the exhibited content",
            "the pinned list of admitted contents",
            "the normalisation of B and of the Cartan elements D, H1, H",
            "the altered T and the planted shifts of the controls leg",
        ],
        disclosures=[
            "the colour^2-B leg is an identity of the definitions",
            "the planted-shift controls move the first state only",
        ])


# ---------------------------------------------------------------------------
# check B: couplings, ground vectors, the infrared criterion
# ---------------------------------------------------------------------------

def _su2_gens(d):
    Jp = [[F(0)] * d for _ in range(d)]
    Jm = [[F(0)] * d for _ in range(d)]
    H = [[F(0)] * d for _ in range(d)]
    for k in range(d):
        H[k][k] = F(d - 1 - 2 * k)
        if k >= 1:
            Jp[k - 1][k] = F(k)
        if k + 1 < d:
            Jm[k + 1][k] = F(d - 1 - k)
    return [Jp, Jm, H]


def _dual(gens):
    return [[[-X[j][i] for j in range(len(X))] for i in range(len(X))]
            for X in gens]


_TENSOR_CACHE = {}


def _su2_invariants(d1, d2, d3, conj):
    """Basis of trilinear forms on d1 x d2 x (d3 or its dual) annihilated by
    the three generators; each as a dict {(a, b, s): value}."""
    key = (d1, d2, d3, conj)
    if key in _TENSOR_CACHE:
        return _TENSOR_CACHE[key]
    reps = [_su2_gens(d1), _su2_gens(d2),
            _dual(_su2_gens(d3)) if conj else _su2_gens(d3)]
    dims = (d1, d2, d3)
    idx = [(a, b, s) for a in range(d1) for b in range(d2) for s in range(d3)]
    pos = {I: k for k, I in enumerate(idx)}
    rows = []
    for g in range(3):
        for I in idx:
            row = [F(0)] * len(idx)
            hit = False
            for f in range(3):
                X = reps[f][g]
                for a2 in range(dims[f]):
                    co = X[a2][I[f]]
                    if co != 0:
                        J = I[:f] + (a2,) + I[f + 1:]
                        row[pos[J]] += co
                        hit = True
            if hit:
                rows.append(row)
    basis = [{I: v[pos[I]] for I in idx if v[pos[I]] != 0}
             for v in _nullspace(rows, len(idx))]
    _TENSOR_CACHE[key] = basis
    return basis


def _layout(mults):
    """mults: list of (c, d, ys).  Returns per-multiplet offsets and the list
    of states (multiplet index, colour index, su2 index)."""
    off, states = [], []
    for i, (c, d, ys) in enumerate(mults):
        off.append(len(states))
        for a in range(_NC[c]):
            for k in range(d):
                states.append((i, a, k))
    return off, states


def _colour_ok(c1, c2):
    return (c1 == "1" and c2 == "1") or (c1 != "1" and c2 == _CONJ[c1])


def _channels(mults, S, use_charges=True, bare=True):
    """Coupling channels.  S is None (bare terms only) or (d_S, y_S).  Each
    channel: (i, j, conj, tensor) with tensor {(m_i, m_j, s): value}; bare
    channels carry conj = None and s = 0."""
    r = len(mults[0][2])
    out = []
    specs = [(None, 1, tuple([F(0)] * r))] if bare else []
    if S is not None:
        dS, yS = S
        specs.append((False, dS, tuple(yS)))
        specs.append((True, dS, tuple(-y for y in yS)))
    for conj, dS, yS in specs:
        for i in range(len(mults)):
            for j in range(i, len(mults)):
                ci, di, yi = mults[i]
                cj, dj, yj = mults[j]
                if not _colour_ok(ci, cj):
                    continue
                if use_charges and any(
                        a + b + s != 0 for a, b, s in zip(yi, yj, yS)):
                    continue
                for T in _su2_invariants(di, dj, dS, bool(conj)):
                    out.append((i, j, conj, T))
    return out


def _mass_entries(mults, off, chans, vac):
    """For each channel the list of (I, J, value) it contributes to the
    symmetric mass form at ground-vector component vac, I <= J; symmetrised when a
    multiplet couples to itself."""
    per = []
    for i, j, conj, T in chans:
        s_want = 0 if conj is None else vac
        acc = {}
        ci, di, _ = mults[i]
        for (a, b, s), v in T.items():
            if s != s_want:
                continue
            for col in range(_NC[ci]):
                I = off[i] + col * di + a
                J = off[j] + col * mults[j][1] + b
                key = (min(I, J), max(I, J))
                acc[key] = acc.get(key, F(0)) + v
        per.append([(I, J, v) for (I, J), v in sorted(acc.items()) if v != 0])
    return per


_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
           67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113)


def _term_rank(n, support):
    """Maximum matching of the bipartite graph on rows/columns 0..n-1 with
    edge (i, j) for every pair in support.  Bounds the rank of any matrix
    with that support (T4)."""
    adj = [[] for _ in range(n)]
    for i, j in support:
        adj[i].append(j)
    match = [-1] * n

    def augment(i, seen):
        for j in adj[i]:
            if j in seen:
                continue
            seen.add(j)
            if match[j] < 0 or augment(match[j], seen):
                match[j] = i
                return True
        return False

    return sum(1 for i in range(n) if augment(i, set()))


def _certificate(n, per):
    """Decide whether a symmetric n x n form, given as a list of channels
    each a list of (i, j, value) with i <= j, can have full rank.
    FAIL_ii: term rank of the support below n (holds for all coefficients).
    PASS: explicit prime coefficients, one per channel, giving rank n.
    UNDETERMINED: term rank n but no tried coefficients reach rank n."""
    support = set()
    for lst in per:
        for i, j, v in lst:
            support.add((i, j))
            support.add((j, i))
    tr = _term_rank(n, sorted(support))
    if tr < n:
        return {"verdict": "FAIL_ii", "term_rank": tr, "rank": None,
                "coeffs": None}
    rk = 0
    for shift in COEFF_SHIFTS:
        co = [_PRIMES[(k + shift) % len(_PRIMES)] for k in range(len(per))]
        M = [[F(0)] * n for _ in range(n)]
        for k, lst in enumerate(per):
            for i, j, v in lst:
                M[i][j] += co[k] * v
                if i != j:
                    M[j][i] += co[k] * v
        rk = _rank(M, n) if n else 0
        if rk == n:
            return {"verdict": "PASS", "term_rank": tr, "rank": rk,
                    "coeffs": tuple(co)}
    return {"verdict": "UNDETERMINED", "term_rank": tr, "rank": rk,
            "coeffs": None}


def _is_real(S):
    dS, yS = S
    return dS % 2 == 1 and all(y == 0 for y in yS)


def _real_components(S):
    return S[0] if _is_real(S) else 2 * S[0]


def _vacua(S):
    """Weight vectors used as ground vectors: the weight-zero one for a real irrep,
    every one otherwise."""
    return [(S[0] - 1) // 2] if _is_real(S) else list(range(S[0]))


def _dimG(r):
    return 8 + 3 + r


def _capacity(mults, S):
    return (sum(_NC[c] * d for c, d, _ in mults) + _dimG(len(mults[0][2]))
            + (_real_components(S) if S is not None else 0))


def _infrared(mults, S, vac, use_i=True, bare_with_scalar=True,
              coloured_in_C=True, i_scope="all"):
    """Verdict with certificate for (content, charges, scalar, ground vector).
    'verdict' in {'PASS', 'FAIL_i', 'FAIL_ii', 'UNDETERMINED'}.  The three
    trailing switches exist only for the controls leg."""
    r = len(mults[0][2])
    off, states = _layout(mults)
    n = len(states)

    def wts(i, k):
        c, d, ys = mults[i]
        return [F(d - 1 - 2 * k)] + [F(y) for y in ys]

    if S is None:
        mu = [F(0)] * (1 + r)
    else:
        mu = [F(S[0] - 1 - 2 * vac)] + [F(y) for y in S[1]]
    unbroken = _nullspace([mu], 1 + r)
    q = [tuple(sum(h[g] * wts(i, k)[g] for g in range(1 + r))
               for h in unbroken) for (i, a, k) in states]
    coloured = [mults[states[s][0]][0] != "1" for s in range(n)]
    charged = [any(x != 0 for x in q[s]) for s in range(n)]
    if i_scope == "all":
        acts = any(charged)
    else:
        acts = any(charged[s] for s in range(n) if not coloured[s])
    C = [s for s in range(n)
         if (coloured[s] and coloured_in_C) or charged[s]]
    chans = _channels(mults, S, bare=(bare_with_scalar or S is None))
    per = _mass_entries(mults, off, chans, vac)
    support = set()
    for lst in per:
        for I, J, v in lst:
            support.add((I, J))
    inC = set(C)
    posC = {s: k for k, s in enumerate(C)}
    per_C = [[(posC[I], posC[J], v) for I, J, v in lst
              if I in inC and J in inC] for lst in per]
    cert = _certificate(len(C), per_C)
    col = [s for s in range(n) if coloured[s]]
    posK = {s: k for k, s in enumerate(col)}
    sup_K = [(posK[I], posK[J]) for I, J in support
             if I in posK and J in posK]
    sup_K += [(j, i) for i, j in sup_K]
    res = {"unbroken": len(unbroken), "acts": acts, "C": len(C),
           "states": n, "channels": len(chans),
           "yukawa_channels": sum(1 for ch in chans if ch[2] is not None),
           "leak": sum(1 for I, J in support if (I in inC) != (J in inC)),
           "coloured": len(col),
           "coloured_term_rank": _term_rank(len(col), sorted(set(sup_K))),
           "colour_mixing": sum(1 for I, J in support
                                if (I in posK) != (J in posK)),
           "term_rank": cert["term_rank"], "rank": cert["rank"],
           "coeffs": cert["coeffs"], "ii": cert["verdict"]}
    res["verdict"] = "FAIL_i" if (use_i and not acts) else cert["verdict"]
    return res


def _scalar_floor(content):
    """Least real components of a scalar for which, charges ignored, the
    coloured states can all be massive (term rank), with the SU(2)
    dimensions up to DS_MAX that achieve it.  0 means bare terms suffice."""
    mults = [(c, d, ()) for c, d in content]
    off, states = _layout(mults)
    col = [s for s in range(len(states)) if mults[states[s][0]][0] != "1"]
    pos = {s: k for k, s in enumerate(col)}

    def full(S, vac):
        per = _mass_entries(mults, off, _channels(mults, S, False), vac)
        sup = set()
        for lst in per:
            for I, J, v in lst:
                if I in pos and J in pos:
                    sup.add((pos[I], pos[J]))
                    sup.add((pos[J], pos[I]))
        return _term_rank(len(col), sorted(sup)) == len(col)

    if full(None, 0):
        return 0, []
    works = [dS for dS in range(1, DS_MAX + 1)
             if any(full((dS, ()), v) for v in range(dS))]
    beyond = _real_components((DS_MAX + 1, ()))
    floor = min([_real_components((dS, ())) for dS in works] + [beyond])
    return floor, works


def _lin_rows(content):
    return [[F(1, 2) * d * (1 if c != "1" else 0) for c, d in content],
            [_T(d) * _NC[c] for c, d in content],
            [F(_NC[c] * d) for c, d in content]]


def _cubic(content, y):
    return sum(_NC[c] * d * yy ** 3 for (c, d), yy in zip(content, y))


def _rational_roots(co):
    """Rational roots of sum co[k] x^k, integer coefficients."""
    co = list(co)
    while co and co[-1] == 0:
        co.pop()
    roots = []
    while co and co[0] == 0:
        roots.append(F(0))
        co = co[1:]
    if len(co) <= 1:
        return sorted(set(roots))
    divs = lambda m: [k for k in range(1, abs(m) + 1) if m % k == 0]
    for p in divs(co[0]):
        for qd in divs(co[-1]):
            for sg in (1, -1):
                x = F(sg * p, qd)
                if sum(a * x ** k for k, a in enumerate(co)) == 0:
                    roots.append(x)
    return sorted(set(roots))


def _primitive(y):
    den = 1
    for a in y:
        a = F(a)
        den = den * a.denominator // gcd(den, a.denominator)
    z = [int(F(a) * den) for a in y]
    g = 0
    for a in z:
        g = gcd(g, abs(a))
    z = [a // g for a in z] if g else z
    lead = next((a for a in z if a), 1)
    return tuple(-a for a in z) if lead < 0 else tuple(z)


def _charge_lines(content):
    """(dimension of the linear solution space, primitive integer solutions
    of all four conditions up to scale, the zero solution not counted) for
    one abelian factor.  Solved exactly for dimension <= 2; None for the
    list otherwise."""
    ns = _nullspace(_lin_rows(content), len(content))
    if len(ns) == 0:
        return 0, []
    if len(ns) == 1:
        return 1, ([_primitive(ns[0])] if _cubic(content, ns[0]) == 0 else [])
    if len(ns) > 2:
        return len(ns), None
    v1, v2 = ns
    f = lambda s, t: _cubic(content, [s * a + t * b for a, b in zip(v1, v2)])
    a0, a3 = f(0, 1), f(1, 0)
    p1, m1 = f(1, 1), f(-1, 1)
    a2 = (p1 + m1) / 2 - a0
    a1 = (p1 - m1) / 2 - a3
    ok = all(f(x, 1) == a3 * x ** 3 + a2 * x ** 2 + a1 * x + a0
             for x in (F(2), F(3), F(-2), F(1, 2), F(-5, 3)))
    if not ok or not any((a0, a1, a2, a3)):
        return 2, None
    den = 1
    for a in (a0, a1, a2, a3):
        den = den * a.denominator // gcd(den, a.denominator)
    ints = [int(a * den) for a in (a0, a1, a2, a3)]
    lines = []
    if a3 == 0:
        lines.append(_primitive(v1))
    for x in _rational_roots(ints):
        lines.append(_primitive([x * a + b for a, b in zip(v1, v2)]))
    return 2, sorted(set(lines))


def _brute_lines(content, box):
    """Independent route to the solution lines: every integer charge vector
    with entries in [-box, box] on all multiplets but the last, the last
    fixed by the gravitational condition, tested on all four conditions.
    Returns (primitive lines found, integer points tested)."""
    n = len(content)
    size = [_NC[c] * d for c, d in content]
    col = [6 * d * (1 if c != "1" else 0) for c, d in content]
    su2 = [int(12 * _T(d)) * _NC[c] for c, d in content]
    found, tested = set(), 0
    for head in product(range(-box, box + 1), repeat=n - 1):
        tested += 1
        s = sum(a * b for a, b in zip(size, head))
        if s % size[-1]:
            continue
        y = head + (-s // size[-1],)
        if abs(y[-1]) > box or not any(y):
            continue
        if sum(a * b for a, b in zip(col, y)):
            continue
        if sum(a * b for a, b in zip(su2, y)):
            continue
        if sum(a * b ** 3 for a, b in zip(size, y)):
            continue
        found.add(_primitive(y))
    return found, tested


def _anomalies(content, y):
    lin = [sum(a * b for a, b in zip(row, y)) for row in _lin_rows(content)]
    return lin + [_cubic(content, y)]


def _canon_charge(y):
    y = tuple(F(v) for v in y)
    return min(y, tuple(-v for v in y))


def _scalars(mults):
    """Candidate scalar irreps (d_S, y_S): d_S up to DS_MAX, y_S minus the
    sum of the charges of a pair of multiplets, one of each conjugate
    pair."""
    ys = set()
    for i in range(len(mults)):
        for j in range(i, len(mults)):
            ys.add(_canon_charge(
                [-(a + b) for a, b in zip(mults[i][2], mults[j][2])]))
    return [(dS, y) for dS in range(1, DS_MAX + 1) for y in sorted(ys)]


def _census(mults):
    """The same candidate set by a second route: ordered pairs, both signs,
    built dimension by dimension.  Any (d_S, y_S) outside it has no
    trilinear coupling, because a coupling needs y_i + y_j + y_S = 0 or
    y_i + y_j - y_S = 0 for some pair."""
    out = set()
    for dS in range(DS_MAX, 0, -1):
        for a in mults:
            for b in mults:
                for sg in (1, -1):
                    out.add((dS, _canon_charge(
                        [sg * (p + q) for p, q in zip(a[2], b[2])])))
    return out


def _admitted():
    out = set()
    for c in _contents(FMAX):
        a3, w, b2, b3 = _formula_values(c)
        if a3 == 0 and w == 0 and b2 != 0:
            out.add(_canon(c))
    return sorted(out, key=lambda c: (_size(c), c))


def _normal_form(content, y, S):
    """Charges of a one-factor model scaled so the coloured doublet has
    charge 1: (doublet, sorted coloured singlets, colourless doublet,
    colourless singlet, scalar SU(2) dimension, |scalar charge|) as
    strings and integers, when the content has that shape; else None."""
    dbl = [yy for (c, d), yy in zip(content, y) if c != "1" and d == 2]
    if len(dbl) != 1 or dbl[0] == 0:
        return None
    u = F(dbl[0])
    sing = sorted(F(yy) / u for (c, d), yy in zip(content, y)
                  if c != "1" and d == 1)
    ld = [F(yy) / u for (c, d), yy in zip(content, y) if c == "1" and d == 2]
    ls = [F(yy) / u for (c, d), yy in zip(content, y) if c == "1" and d == 1]
    if len(ld) != 1 or len(ls) != 1 or len(sing) != 2:
        return None
    return (str(F(1)), tuple(str(v) for v in sing), str(ld[0]), str(ls[0]),
            S[0], str(abs(F(S[1][0]) / u)))


def _scan(**flags):
    """Everything check B reports.  One record per model; one verdict per
    (model, scalar inside the window with a coupling, ground vector)."""
    adm = _admitted()
    floors = {c: _scalar_floor(c) for c in adm}
    cases = sorted((_size(c), r, c) for c in adm for r in (0, 1, 2)
                   if _size(c) + _dimG(r) + floors[c][0] <= WINDOW)
    models, verdicts, solved = [], [], {}
    for size, r, c in cases:
        k, lines = (0, []) if r == 0 else _charge_lines(c)
        solved[(size, r)] = (k, lines)
        zero = tuple(0 for _ in c)
        if r == 0:
            charge_sets = [("none", ())]
        elif r == 1:
            charge_sets = [("line", (y,)) for y in (lines or [])]
            charge_sets.append(("zero", (zero,)))
        else:
            charge_sets = [("dependent", (y, zero)) for y in (lines or [])]
            charge_sets.append(("zero", (zero, zero)))
        for kind, ys in charge_sets:
            mults = [(cc, d, tuple(F(y[i]) for y in ys))
                     for i, (cc, d) in enumerate(c)]
            rec = {"size": size, "r": r, "content": c, "kind": kind,
                   "charges": ys, "mults": mults, "ledger": {},
                   "vacua": {},
                   "bare": _infrared(mults, None, 0, use_i=False)}
            for S in _scalars(mults):
                cap = _capacity(mults, S)
                if cap > WINDOW:
                    rec["ledger"][S] = "outside_window"
                    continue
                if not any(ch[2] is not None for ch in _channels(mults, S)):
                    rec["ledger"][S] = "no_coupling"
                    continue
                rec["ledger"][S] = "run"
                rec["vacua"][S] = []
                for vac in _vacua(S):
                    v = _infrared(mults, S, vac, **flags)
                    rec["vacua"][S].append(vac)
                    verdicts.append((len(models), S, vac, cap, v))
            models.append(rec)
    return {"adm": adm, "floors": floors, "cases": cases, "models": models,
            "verdicts": verdicts, "solved": solved}


def _survivor_forms(scan):
    forms = set()
    for m, S, vac, cap, v in scan["verdicts"]:
        if v["verdict"] == "PASS" and cap <= WINDOW:
            rec = scan["models"][m]
            nf = (_normal_form(rec["content"], rec["charges"][0], S)
                  if rec["kind"] == "line" else None)
            forms.add((rec["size"], rec["r"], rec["kind"], cap, nf))
    return forms


def check_L_least_capacity_content_infrared():
    name = "L_least_capacity_content_infrared"
    legs = {}
    scan = _scan()
    adm, floors, cases = scan["adm"], scan["floors"], scan["cases"]
    models, verdicts, solved = scan["models"], scan["verdicts"], scan["solved"]

    # ---- 1. window ------------------------------------------------------------
    got = tuple((s, r) for s, r, c in cases)
    comps = tuple(_real_components(S) for S in (
        (1, (F(1),)), (1, (F(0),)), (2, (F(0),)), (2, (F(1),)),
        (3, (F(0),)), (3, (F(1),))))
    legs["window_cases"] = (
        got == WINDOW_CASES and tuple(adm) == ADMITTED_CONTENTS
        and comps == REAL_COMPONENT_TABLE,
        "admitted contents %d, equal to the pinned list: %s; least real "
        "scalar components for which the coloured states can all be "
        "massive, charges ignored, with the SU(2) dimensions up to %d "
        "that work, by state count: %s; group dimensions for r = 0, 1, 2: "
        "%s; real components of a charged singlet, a neutral singlet, a "
        "neutral doublet, a charged doublet, a neutral triplet, a charged "
        "triplet: %s (pinned %s); cases with states + group dimension + "
        "that floor <= %d: %s (pinned %s)" % (
            len(adm), tuple(adm) == ADMITTED_CONTENTS, DS_MAX,
            [(_size(c), floors[c][0], floors[c][1]) for c in adm],
            [_dimG(r) for r in (0, 1, 2)], comps, REAL_COMPONENT_TABLE,
            WINDOW, got, WINDOW_CASES))

    # ---- 2. charge conditions ---------------------------------------------------
    n_lines = {s: (len(l) if l is not None else None)
               for (s, r), (k, l) in solved.items() if r == 1}
    dims = {(s, r): k for (s, r), (k, l) in solved.items() if r > 0}
    resid, brute_ok, tested = [], True, {}
    for size, r, c in cases:
        if r != 1:
            continue
        k, l = solved.get((size, r), (None, None))
        resid += [a for y in (l or [])
                  for a in _anomalies(c, [F(v) for v in y])]
        found, npts = _brute_lines(c, CHARGE_BOX)
        tested[size] = npts
        brute_ok = brute_ok and l is not None and found == set(l)
    two = [(s, k) for (s, r), k in dims.items() if r == 2]
    legs["abelian_charge_solutions_exact"] = (
        n_lines == SOLUTION_LINES and bool(resid)
        and all(a == 0 for a in resid) and brute_ok and bool(tested)
        and bool(two) and all(k < 2 for s, k in two),
        "linear solution-space dimensions by (states, r): %s; solution "
        "lines for one abelian factor by state count, the zero solution "
        "not counted: %s (pinned %s); all four conditions vanish on every "
        "line: %s (%d values); a brute-force search over integer charges "
        "in [-%d, %d] (points tested by state count: %s) finds exactly "
        "these lines: %s; (states, dimension) where two abelian factors "
        "were asked for: %s, so every pair there is dependent; lines: "
        "%s" % (
            sorted(dims.items()), n_lines, SOLUTION_LINES,
            all(a == 0 for a in resid), len(resid), CHARGE_BOX, CHARGE_BOX,
            sorted(tested.items()), brute_ok, two,
            {s: l for (s, r), (k, l) in solved.items() if r == 1}))

    # ---- 3. coverage and certificates ---------------------------------------------
    # (a) every window case has its models, and the models are the ones the
    #     two charge routes give
    by_case = {}
    for rec in models:
        by_case.setdefault((rec["size"], rec["r"]), []).append(rec)
    cover = set(by_case) == set(WINDOW_CASES)
    inventory = True
    for size, r, c in cases:
        recs = by_case.get((size, r), [])
        if r == 0:
            inventory &= [x["kind"] for x in recs] == ["none"]
            continue
        base = _brute_lines(c, CHARGE_BOX)[0]
        zero = tuple(0 for _ in c)
        want = ({("line", (y,)) for y in base} | {("zero", (zero,))}
                if r == 1 else
                {("dependent", (y, zero)) for y in base}
                | {("zero", (zero, zero))})
        inventory &= {(x["kind"], x["charges"]) for x in recs} == want
    # (b) every model's candidates are the census, each in one bucket, and
    #     every run candidate has all its ground vectors
    ledger_ok, vac_ok, shape_ok = True, True, True
    buckets = {"run": 0, "no_coupling": 0, "outside_window": 0}
    for rec in models:
        ledger_ok &= set(rec["ledger"]) == _census(rec["mults"])
        for S, b in rec["ledger"].items():
            buckets[b] += 1
            if b != "run":
                continue
            dS, yS = S
            real = dS % 2 == 1 and not any(yS)
            expect = [(dS - 1) // 2] if real else list(range(dS))
            vac_ok &= rec["vacua"].get(S) == expect
            shape_ok &= dS in (1, 2) or (dS == 3 and real)
    run_keys = {(m, S, vac) for m, S, vac, cap, v in verdicts}
    vac_ok &= len(run_keys) == len(verdicts) == sum(
        len(v) for rec in models for v in rec["vacua"].values())
    # (c) certificates
    kinds = {}
    for m, S, vac, cap, v in verdicts:
        kinds[v["verdict"]] = kinds.get(v["verdict"], 0) + 1
    undet = sum(1 for x in verdicts if x[4]["verdict"] == "UNDETERMINED")
    leaks = sum(x[4]["leak"] for x in verdicts)
    passes = [x for x in verdicts if x[4]["verdict"] == "PASS"]
    passes_ok = all(x[4]["rank"] == x[4]["C"] and x[4]["acts"]
                    and x[4]["coeffs"] for x in passes)
    fail_ii_ok = all(x[4]["term_rank"] < x[4]["C"]
                     for x in verdicts if x[4]["verdict"] == "FAIL_ii")
    fail_i_ok = all(not x[4]["acts"]
                    for x in verdicts if x[4]["verdict"] == "FAIL_i")
    bare_fail = bool(models) and all(
        rec["bare"]["verdict"] == "FAIL_ii"
        and rec["bare"]["coloured_term_rank"] < rec["bare"]["coloured"]
        and rec["bare"]["colour_mixing"] == 0 for rec in models)
    counts_ok = (kinds == BUILD_VERDICTS
                 and buckets["no_coupling"] == BUILD_NO_COUPLING
                 and buckets["outside_window"] == BUILD_OUTSIDE_WINDOW)
    legs["infrared_verdicts_certified"] = (
        cover and inventory and ledger_ok and vac_ok and shape_ok
        and undet == 0 and leaks == 0 and passes_ok and fail_ii_ok
        and fail_i_ok and bare_fail and counts_ok and bool(passes),
        "window cases with models: %s; models %d by kind %s, equal to "
        "the brute-force lines plus the zero and dependent vectors: %s; "
        "every model's candidate scalars (SU(2) dimension up to %d) equal "
        "an independently built census: %s; candidates run %d, with no "
        "coupling %d, outside the window %d (build-recorded %d, %d); "
        "every run candidate has all its ground vectors (one for a real "
        "irrep): "
        "%s; every run candidate is a singlet, a doublet or a real "
        "triplet: %s; verdicts %d by kind %s (build-recorded %s), "
        "undetermined %d; entries joining a state in C to one outside: "
        "%d; with bare terms alone the coloured states of every model "
        "have term rank below their number, with no coloured-colourless "
        "entry: %s (this decides every candidate with no coupling, at "
        "any ground vector); PASS certificates as (states, r, scalar "
        "dimension, ground vector, |C|, rank, coefficients): %s" % (
            sorted(by_case), len(models),
            sorted((k, sum(1 for x in models if x["kind"] == k))
                   for k in {x["kind"] for x in models}),
            inventory, DS_MAX, ledger_ok, buckets["run"],
            buckets["no_coupling"], buckets["outside_window"],
            BUILD_NO_COUPLING, BUILD_OUTSIDE_WINDOW, vac_ok, shape_ok,
            len(verdicts), sorted(kinds.items()),
            sorted(BUILD_VERDICTS.items()), undet, leaks, bare_fail,
            [(models[m]["size"], models[m]["r"], S[0], vac, v["C"],
              v["rank"], v["coeffs"]) for m, S, vac, cap, v in passes]))

    # ---- 4. the survivor ----------------------------------------------------------
    forms = _survivor_forms(scan)
    want = (SURVIVOR_STATES, 1, "line", SURVIVOR_CAPACITY,
            (str(F(1)), tuple(str(F(v)) for v in SURVIVOR_CHARGES[1]),
             str(F(SURVIVOR_CHARGES[2])), str(F(SURVIVOR_CHARGES[3])),
             SURVIVOR_SCALAR[0], str(F(SURVIVOR_SCALAR[1]))))
    surv = [x for x in passes if x[3] <= WINDOW]
    bare_empty = bool(surv) and all(
        models[m]["bare"]["channels"] == 0 for m, S, vac, cap, v in surv)
    outside = sorted({v["states"] - v["C"] for m, S, vac, cap, v in surv})
    legs["unique_survivor"] = (
        forms == {want} and bare_empty,
        "passing (model, ground vector) pairs with capacity <= %d: %d; "
        "distinct "
        "models after scaling the coloured doublet's charge to 1 and "
        "ordering the two coloured singlets: %d: %s (pinned %s); bare "
        "terms in them: none: %s; states outside C, hence not required "
        "to be paired: %s" % (
            WINDOW, len(surv), len(forms), sorted(forms, key=str), want,
            bare_empty, outside))

    # ---- 5. controls ----------------------------------------------------------------
    c15 = next((c for s, r, c in cases
                if s == SURVIVOR_STATES and r == 1), None)
    good = next((models[m]["charges"][0] for m, S, vac, cap, v in surv
                 if models[m]["kind"] == "line"), None)
    c_anom = False
    if c15 is not None and good is not None:
        bent = list(good)
        bent[0] += BUMP
        c_anom = (all(a == 0 for a in _anomalies(c15, [F(v) for v in good]))
                  and any(a != 0
                          for a in _anomalies(c15, [F(v) for v in bent])))
    # matching: a pattern that needs an augmenting path
    aug = [(0, 0), (0, 1), (1, 0)]
    c_aug = _term_rank(2, aug)
    # deficiency with no empty row
    star = [(0, 3), (1, 3), (2, 3), (3, 0), (3, 1), (3, 2)]
    c_star = _certificate(4, [[(0, 3, F(1))], [(1, 3, F(1))],
                              [(2, 3, F(1))]])
    # full term rank, forced deficiency: one coefficient on all four entries
    c_forced = _certificate(2, [[(0, 0, F(1)), (0, 1, F(1)), (1, 1, F(1))]])
    # criterion (i) dropped altogether
    no_i = sum(1 for rec in models if rec["r"] == 0
               for S, b in rec["ledger"].items() if b == "run"
               for vac in rec["vacua"][S]
               if _infrared(rec["mults"], S, vac, use_i=False)["verdict"]
               == "PASS")
    # the clause 'acts non-trivially': zero charges, neutral doublet
    zrec = next((rec for rec in models
                 if rec["kind"] == "zero" and rec["r"] == 1
                 and rec["size"] == ADMITTED_STATE_COUNTS[0]), None)
    z_with = z_without = z_cap = None
    if zrec is not None:
        Sz = (2, (F(0),))
        z_cap = _capacity(zrec["mults"], Sz)
        z_with = _infrared(zrec["mults"], Sz, 0)
        z_without = _infrared(zrec["mults"], Sz, 0, use_i=False)
    c_zero = (zrec is not None and z_with["verdict"] == "FAIL_i"
              and z_with["unbroken"] > 0
              and z_without["verdict"] == "PASS"
              and z_without["rank"] == z_without["C"] and z_cap <= WINDOW)
    # clauses that decide no survivor inside the window
    base = {(m, S, vac): v["verdict"] for m, S, vac, cap, v in verdicts}
    variants = (("bare terms left out when a scalar is present",
                 {"bare_with_scalar": False}),
                ("C taken as the charged states only",
                 {"coloured_in_C": False}),
                ("(i) judged on colourless states only",
                 {"i_scope": "colourless"}))
    sens = []
    for label, fl in variants:
        alt = _scan(**fl)
        av = {(m, S, vac): v["verdict"] for m, S, vac, cap, v in
              alt["verdicts"]}
        sens.append((label, sum(1 for k in base if av.get(k) != base[k]),
                     _survivor_forms(alt) == forms))
    legs["controls_computed"] = (
        c_anom and c_aug == 2 and c_star["verdict"] == "FAIL_ii"
        and all(any(i == k for i, j in star) for k in range(4))
        and c_forced["verdict"] == "UNDETERMINED" and no_i > 0 and c_zero
        and all(s[2] for s in sens),
        "a survivor's charges satisfy the four conditions and, with the "
        "first one raised by %d, violate one: %s; a pattern needing an "
        "augmenting path has term rank %d; a pattern on %d states with no "
        "empty row has term rank %s and verdict %s; a form with full term "
        "rank %s whose entries share one coefficient has rank %s and "
        "verdict %s; with criterion (i) dropped, passing (scalar, ground "
        "vector) "
        "pairs without any abelian factor: %d; zero charges with a "
        "neutral doublet at %s states: capacity %s, verdict %s with an "
        "unbroken element that acts on nothing, and with (i) dropped %s "
        "at rank %s of %s; altered clauses as (clause, verdicts changed, "
        "survivor set unchanged): %s" % (
            BUMP, c_anom, c_aug, 4, c_star["term_rank"], c_star["verdict"],
            c_forced["term_rank"], c_forced["rank"], c_forced["verdict"],
            no_i, zrec["size"] if zrec else None, z_cap,
            z_with["verdict"] if z_with else None,
            z_without["verdict"] if z_without else None,
            z_without["rank"] if z_without else None,
            z_without["C"] if z_without else None, sens))

    nf = want[4]
    return _result(
        name, legs,
        key_result=(
            "Of the %d admitted contents, %d (states, r) cases have "
            "capacity bound <= %d; over %d models, zero and dependent "
            "charge vectors included, and %d certified verdicts, the "
            "models passing the infrared criterion at capacity <= %d "
            "number %d up to colour conjugation and exchange of the two "
            "coloured singlets: %d states, one abelian factor with "
            "charges proportional to %s, %s, %s, %s, a scalar of SU(2) "
            "dimension %d and charge %s in those units, capacity %d, and "
            "no bare term" % (
                len(adm), len(cases), WINDOW, len(models), len(verdicts),
                WINDOW, len(forms), SURVIVOR_STATES, nf[0], nf[1], nf[2],
                nf[3], nf[4], nf[5], SURVIVOR_CAPACITY)),
        conditional_on=[
            "the admitted set, recomputed here through the functions that "
            "check A tests and compared with the pinned list: an error in "
            "that enumeration would be an error here",
            "T2 (text): models satisfying (ii) with 18 or more states "
            "have capacity >= 32",
            "T3 (text; its first half is computed here): for a singlet, a "
            "doublet or a real triplet every ground direction is "
            "gauge-equivalent "
            "to a weight vector",
            "T4 (text): term rank bounds rank",
            "T5 (text): dependent charge vectors are equivalent to the "
            "computed ones",
        ],
        named_readings=[
            "R1, R4, R5: the anomaly conditions, capacity, and the "
            "infrared criterion itself",
        ],
        authored_inputs=[
            "the capacity functional and the window",
            "the infrared criterion, including 'one scalar irrep', the "
            "restriction of ground vectors to weight vectors, and the "
            "weight-zero one for real irreps",
            "the scalar candidates: SU(2) dimension up to the stated "
            "bound, charges drawn from pairs of multiplets",
            "the integer box of the brute-force charge search",
            "the prime coefficients of the PASS certificates",
            "the pinned survivor tuple, compared by value and read from "
            "no banked check",
            "the altered charges, the three patterns and the three "
            "altered clauses of the controls leg",
        ],
        disclosures=[
            "the zero solution of the charge conditions is not counted as "
            "a line; zero and dependent charge vectors are run as their "
            "own models",
            "three clauses of the criterion decide no survivor inside the "
            "window; the controls leg reports how many verdicts each "
            "changes",
            "the survivor leaves states outside C unpaired; the number is "
            "reported",
            "candidates outside the window are counted and not run",
        ])


_CHECKS = {
    "L_weak_doublet_baryon_minimality":
        check_L_weak_doublet_baryon_minimality,
    "L_least_capacity_content_infrared":
        check_L_least_capacity_content_infrared,
}


def run_all():
    return {k: f() for k, f in _CHECKS.items()}


def register(registry):
    if HELD_OUT_OF_THE_BANK:
        raise RuntimeError(
            "weak_doublet_baryon_minimality is HELD: not lifted")
    registry.update(_CHECKS)
    return registry


if __name__ == "__main__":
    import sys
    results = run_all()
    for key, r in results.items():
        print("%s: %s  (%d legs)" % (
            key, "PASS" if r["passed"] else "FAIL", r["leg_count"]))
        for leg in sorted(r["legs"]):
            rec = r["legs"][leg]
            print("  [%s] %s -- %s" % (
                "ok" if rec["passed"] else "FAIL", leg, rec["evidence"]))
        for reason in r["fail_reasons"]:
            print("  FAIL REASON: %s" % reason)
    sys.exit(0 if all(r["passed"] for r in results.values()) else 1)
