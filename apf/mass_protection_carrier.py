"""L_mass_protection_carrier.

Banked v24.3.506 (2026-11-11).  Lifted by Ethan 2026-11-11 after two cold
blinded audits (LAND-WITH-FIXES 0.8 each; the mathematics reproduced
independently by both) and a mechanical verification of the carried
fixes; registered with a bare-name key per D6@2026-08-03.

Which Weyl-fermion contents of G = SU(3) x SU(2) x U(1) admit a G-invariant
mass term, and how many of their states such a term can pair.

SETTING (part of the claim).  An irrep is (c, d, y): c in {'1', '3', '3b'}
(trivial, fundamental, antifundamental of SU(3) -- the authored colour
scope), d >= 1 the SU(2) dimension, y a Fraction U(1) charge.  A content is
a multiset of irreps, read as left-handed Weyl fields in four dimensions.
A mass term is a bare, field-independent bilinear: a G-invariant vector of
Sym^2(V), Majorana and Dirac terms counted together.  I(V) is the dimension
of that space.  The protected dimension p(V) is dim V minus the largest
rank of a G-invariant symmetric form on V: every mass term leaves at
least p(V) states massless, and which ones depends on the term unless
p(V) = dim V.  That a fermion mass term is a
symmetric invariant form is the standard identification, NAMED and not
computed.  Yukawa terms, higher-dimension terms, interactions and
condensates are outside the setting.

Frozen claim surface (v3):
FROZEN_CLAIM_SURFACE_v3_L_mass_protection_carrier_2026-11-11.md
"""
from collections import Counter
from fractions import Fraction as F
from math import comb

HELD_OUT_OF_THE_BANK = False  # BANKED v24.3.506 (2026-11-11); lifted by Ethan; register() below

CLAIM_SURFACE_SHA256 = (
    "79a8298fcec771da02f4a857954c6885e0e28738249fed06313ba9ac0eece3e3")

MAY_NOT_CITE = (
    "chirality, requirement R2, or any carrier as derived, selected or "
    "forced",
    "SU(2) or the doublet as forced",
    "the Standard Model hypercharge assignment as certified (the "
    "reduced-group leg leaves Y_Q free)",
    "occupancy guaranteed by structure, or any genericity premise",
    "anomalies: none is computed; protected contents in the catalog "
    "include anomalous ones",
    "that I >= 1 means every state can be made massive, that p counts "
    "particular states, or that p > 0 means presence at low energy "
    "after G breaks",
    "protection against gapping by interactions or condensates",
    "anything beyond the colour scope, the catalog (pinned by size, not "
    "by content), and the stated ranges",
    "irreversibility, L_irr, L_irr_uniform, T_M or Theorem_R at any "
    "grade; no grade of any banked object moves",
    "Born, occupancy as derived, or the matter-free no-go",
    "the soundness of check_T_field: its hypercharges are consumed by "
    "value and its premises inherited",
)

EXPECTED_LEGS = {
    "check_L_mass_protection_carrier": [
        "two_counts_agree_on_pinned_catalog",
        "conjugate_pairing_method_test",
        "su2_single_irrep_parity",
        "doublet_only_contents_count",
        "one_generation_fully_protected_under_G",
        "reduced_group_pairing_structure",
        "protected_dimension_matches_explicit_form",
        "controls_computed",
    ],
}

# Pinned sizes (authored; the legs compare what they ran against these).
AUTHORED_CATALOG_SIZE = 21
TIED_CATALOG_SIZE = 2
D_BOUNDS = (1, 12)
N_BOUNDS = (1, 6)
# Three of SU(2), nine of gl(3) acting on colour, one of U(1).
GENERATOR_COUNT = 13
SEED = 20261111


def _result(name, legs, key_result, dependencies=(), disclosures=()):
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
            "representation theory on authored contents and on one "
            "content read by value; the physical reading is one named "
            "reading and is not computed"),
        "legs": {k: {"passed": bool(v[0]), "evidence": v[1]}
                 for k, v in legs.items()},
        "leg_count": len(legs),
        "fail_reasons": fails,
        "key_result": key_result,
        "conditional_on": [
            "R-count (a reading, computed nowhere): while G is unbroken, "
            "no bare mass term leaves fewer than p(V) states of the "
            "content massless; a statement about a number of states, "
            "lapsing when G breaks, selecting no carrier",
            "the identification of a fermion mass term with a G-invariant "
            "symmetric form (named, not computed)",
            "that no invariant symmetric form has rank above the "
            "formula's (Schur's lemma with the computed symmetry type of "
            "the SU(2) form); the explicit form supplies the lower bound "
            "on the rank only",
            "gauge.check_T_field's returned hypercharges, consumed by "
            "value; its premises are inherited, not discharged; every leg "
            "that consumes the tied contents rests on that record's own "
            "grade",
        ],
        "authored_inputs": [
            "the colour scope {1, 3, 3b}",
            "the catalog of contents and its pinned size",
            "the bounds on d and n",
            "the assignment of the five returned hypercharges to the "
            "fields Q, u^c, d^c, L, e^c with their colour and SU(2) "
            "labels and the sign convention for the conjugate fields",
            "the embedding of the reduced group: SU(3) kept, charge = "
            "T3 + Y in the returned record's normalization",
            "the integer seed of the explicit form's coefficients",
            "the family of altered assignments in the controls leg",
            "the fixtures of the controls leg (a weight multiset built to "
            "contain a long shift; three forms built to violate one "
            "factor group each)",
            "the use of all nine gl(3) generators on colour where SU(3) "
            "has eight",
        ],
        "dependencies": list(dependencies),
        "disclosures": list(disclosures),
        "may_not_cite": list(MAY_NOT_CITE),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": CLAIM_SURFACE_SHA256,
        "inventory_note": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


# ---------------------------------------------------------------------------
# contents
# ---------------------------------------------------------------------------

_CONJ_C = {"1": "1", "3": "3b", "3b": "3"}


def _conj(r):
    c, d, y = r
    return (_CONJ_C[c], d, -y)


def _merge(content):
    out = Counter()
    for r, m in content:
        out[(r[0], int(r[1]), F(r[2]))] += int(m)
    return {r: m for r, m in out.items() if m}


def _paired(content):
    return list(content) + [(_conj(r), m) for r, m in content]


def _key(r):
    return (r[0], r[1], r[2].numerator, r[2].denominator)


def _dim_irrep(r):
    return (1 if r[0] == "1" else 3) * r[1]


def _dim(content):
    return sum(_dim_irrep(r) * m for r, m in _merge(content).items())


# -- count A: reality types --------------------------------------------------

def _invariants_by_reality(content, pseudoreal_sign=-1):
    mult = _merge(content)
    total = 0
    for r, m in mult.items():
        rc = _conj(r)
        if rc == r:
            sign = 1 if r[1] % 2 == 1 else pseudoreal_sign
            total += m * (m + 1) // 2 if sign == 1 else m * (m - 1) // 2
        elif rc in mult and _key(r) < _key(rc):
            total += m * mult[rc]
    return total


def _protected_by_reality(content):
    mult = _merge(content)
    total = 0
    for r, m in mult.items():
        rc = _conj(r)
        if rc == r:
            if r[1] % 2 == 0:
                total += (m % 2) * _dim_irrep(r)
        elif rc in mult:
            if _key(r) < _key(rc):
                total += abs(m - mult[rc]) * _dim_irrep(r)
        else:
            total += m * _dim_irrep(r)
    return total


# -- count B: weights and the alternating Weyl sum ---------------------------

_W3 = {
    "1": [(0, 0)],
    "3": [(1, 0), (-1, 1), (0, -1)],
    "3b": [(0, 1), (1, -1), (-1, 0)],
}


def _s1(v):
    return (-v[0], v[0] + v[1])


def _s2(v):
    return (v[0] + v[1], -v[1])


def _su3_shifts():
    """(w(rho) - rho, sign, word length) for the six Weyl elements."""
    rho = (1, 1)
    words = [((), 1), ((_s1,), -1), ((_s2,), -1), ((_s2, _s1), 1),
             ((_s1, _s2), 1), ((_s1, _s2, _s1), -1)]
    out = []
    for word, sign in words:
        v = rho
        for f in reversed(word):
            v = f(v)
        out.append(((v[0] - rho[0], v[1] - rho[1]), sign, len(word)))
    return out


_SU2_SHIFTS = [(0, 1), (-2, -1)]


def _weights(content):
    out = []
    for r, m in _merge(content).items():
        c, d, y = r
        for _ in range(m):
            for w3 in _W3[c]:
                for m2 in range(d - 1, -d, -2):
                    out.append((w3[0], w3[1], m2, y))
    return out


def _sym2_weight_counts(content):
    w = _weights(content)
    n = Counter()
    for i in range(len(w)):
        for j in range(i, len(w)):
            n[(w[i][0] + w[j][0], w[i][1] + w[j][1],
               w[i][2] + w[j][2], w[i][3] + w[j][3])] += 1
    return n


def _invariants_by_weights(content):
    n = _sym2_weight_counts(content)
    total = 0
    for (a, b), s3, _len in _su3_shifts():
        for m2, s2 in _SU2_SHIFTS:
            total += s3 * s2 * n.get((a, b, m2, F(0)), 0)
    return total


def _term_hits(n):
    """Per SU(3) Weyl term: (word length, number of Sym^2 weights whose
    colour part equals the term's shift)."""
    out = []
    for (a, b), _s3, length in _su3_shifts():
        out.append((length, sum(cnt for key, cnt in n.items()
                                if (key[0], key[1]) == (a, b))))
    return out


def _long_hits(length_hit_pairs):
    return sum(h for length, h in length_hit_pairs if length >= 2)


def _reduce_to_em(content):
    out = []
    for r, m in _merge(content).items():
        c, d, y = r
        for m2 in range(d - 1, -d, -2):
            out.append(((c, 1, y + F(m2, 2)), m))
    return out


# -- the explicit symmetric form ---------------------------------------------

def _zeros(n, m=None):
    return [[F(0)] * (n if m is None else m) for _ in range(n)]


def _su2_form(d):
    """Invariant bilinear form on the d-dimensional irrep, monomial basis
    e_k = x^(d-1-k) y^k."""
    B = _zeros(d)
    for k in range(d):
        B[k][d - 1 - k] = F((-1) ** k, comb(d - 1, k))
    return B


def _su2_gens(d):
    Jp, Jm, H = _zeros(d), _zeros(d), _zeros(d)
    for k in range(d):
        H[k][k] = F(d - 1 - 2 * k)
        if k >= 1:
            Jp[k - 1][k] = F(k)
        if k + 1 < d:
            Jm[k + 1][k] = F(d - 1 - k)
    return [Jp, Jm, H]


def _lcg(state):
    state[0] = (1103515245 * state[0] + 12345) % (2 ** 31)
    return F(state[0] % 7 + 1)


def _layout(content):
    """Index every basis state: (irrep, copy, colour index, su2 index)."""
    mult = _merge(content)
    index, pos = {}, 0
    for r in sorted(mult, key=_key):
        nc = 1 if r[0] == "1" else 3
        for i in range(mult[r]):
            for a in range(nc):
                for k in range(r[1]):
                    index[(r, i, a, k)] = pos
                    pos += 1
    return mult, index, pos


def _explicit_form(content, colour_shift=0, su2_identity=False):
    """A symmetric form built block by block from the SU(2) form, the
    colour pairing and seeded integer flavour coefficients."""
    mult, index, n = _layout(content)
    M = _zeros(n)
    state = [SEED]
    for r in sorted(mult, key=_key):
        rc = _conj(r)
        m = mult[r]
        nc = 1 if r[0] == "1" else 3
        B = _su2_form(r[1])
        if su2_identity:
            B = _zeros(r[1])
            for k in range(r[1]):
                B[k][k] = F(1)
        if rc == r:
            sym = all(B[k][l] == B[l][k]
                      for k in range(r[1]) for l in range(r[1]))
            A = _zeros(m)
            for i in range(m):
                for j in range(i, m):
                    if sym:
                        A[i][j] = A[j][i] = _lcg(state)
                    elif i != j:
                        A[i][j] = _lcg(state)
                        A[j][i] = -A[i][j]
            for i in range(m):
                for j in range(m):
                    for k in range(r[1]):
                        for l in range(r[1]):
                            M[index[(r, i, 0, k)]][index[(r, j, 0, l)]] += (
                                A[i][j] * B[k][l])
        elif rc in mult and _key(r) < _key(rc):
            mp = mult[rc]
            for i in range(m):
                for j in range(mp):
                    coeff = _lcg(state)
                    for a in range(nc):
                        for k in range(r[1]):
                            for l in range(r[1]):
                                p = index[(r, i, a, k)]
                                q = index[(rc, j, (a + colour_shift) % nc, l)]
                                M[p][q] += coeff * B[k][l]
                                M[q][p] += coeff * B[k][l]
    return M


def _generators(content):
    mult, index, n = _layout(content)
    gens = []
    for which in range(3):
        G = _zeros(n)
        for (r, i, a, k), p in index.items():
            J = _su2_gens(r[1])[which]
            for l in range(r[1]):
                if J[l][k] != 0:
                    G[index[(r, i, a, l)]][p] += J[l][k]
        gens.append(G)
    for a0 in range(3):
        for b0 in range(3):
            G = _zeros(n)
            for (r, i, a, k), p in index.items():
                if r[0] == "3" and a == b0:
                    G[index[(r, i, a0, k)]][p] += F(1)
                if r[0] == "3b" and a == a0:
                    G[index[(r, i, b0, k)]][p] -= F(1)
            gens.append(G)
    G = _zeros(n)
    for (r, i, a, k), p in index.items():
        G[p][p] = r[2]
    gens.append(G)
    return gens


def _is_invariant(M, gens):
    n = len(M)
    for G in gens:
        for p in range(n):
            for q in range(n):
                s = F(0)
                for t in range(n):
                    if G[t][p] != 0 and M[t][q] != 0:
                        s += G[t][p] * M[t][q]
                    if M[p][t] != 0 and G[t][q] != 0:
                        s += M[p][t] * G[t][q]
                if s != 0:
                    return False
    return True


def _rank(M):
    A = [row[:] for row in M]
    n = len(A)
    rank, col = 0, 0
    while rank < n and col < n:
        piv = next((i for i in range(rank, n) if A[i][col] != 0), None)
        if piv is None:
            col += 1
            continue
        A[rank], A[piv] = A[piv], A[rank]
        for i in range(rank + 1, n):
            if A[i][col] != 0:
                f = A[i][col] / A[rank][col]
                A[i] = [x - f * y for x, y in zip(A[i], A[rank])]
        rank += 1
        col += 1
    return rank


def _pairing_structure(em_content):
    """(vector-like on coloured or charged irreps, number of conjugate
    pairs, list of neutral colourless irreps with multiplicity)."""
    mult = _merge(em_content)
    vector_like, pairs, neutral = True, 0, []
    for r, m in mult.items():
        rc = _conj(r)
        if rc == r:
            neutral.append((r, m))
        else:
            if mult.get(rc, 0) != m:
                vector_like = False
            elif _key(r) < _key(rc):
                pairs += m * m
    return vector_like, pairs, neutral


def _find_key(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            got = _find_key(v, key)
            if got is not None:
                return got
    return None


def _generation(vals):
    return [
        (("3", 2, vals["Y_Q"]), 1),
        (("3b", 1, -vals["Y_u"]), 1),
        (("3b", 1, -vals["Y_d"]), 1),
        (("1", 2, vals["Y_L"]), 1),
        (("1", 1, -vals["Y_e"]), 1),
    ]


def _form_report(content):
    """(dimension, symmetric, invariant, generator count, dim - rank)
    for the explicit form of a content."""
    M = _explicit_form(content)
    n = len(M)
    gens = _generators(content)
    sym = all(M[p][q] == M[q][p] for p in range(n) for q in range(n))
    return n, sym, _is_invariant(M, gens), len(gens), n - _rank(M)


def _s6_holds(gen):
    """The pairing statement of the reduced group with its computed
    parts."""
    em = _reduce_to_em(gen)
    vl, pairs, neutral = _pairing_structure(em)
    ia, ib = _invariants_by_reality(em), _invariants_by_weights(em)
    p_formula = _protected_by_reality(em)
    n, sym, inv, n_gens, p_explicit = _form_report(em)
    ok = (vl and len(neutral) == 1 and neutral[0][1] == 1
          and ib == pairs + 1 and p_formula == 0
          and sym and inv and n_gens == GENERATOR_COUNT
          and n == _dim(em) and p_explicit == 0)
    return ok, {"irreps": len(_merge(em)), "paired": vl, "pairs": pairs,
                "self_conjugate": [(r[0], r[1], str(r[2]), m)
                                   for r, m in neutral],
                "I_reality": ia, "I_weights": ib, "p_formula": p_formula,
                "dim": n, "form_symmetric": sym, "form_invariant": inv,
                "generators": n_gens, "p_explicit": p_explicit}


def _catalog():
    h = F(1, 2)
    return [
        ("one doublet", [(("1", 2, F(0)), 1)]),
        ("two doublets", [(("1", 2, F(0)), 2)]),
        ("one triplet", [(("1", 3, F(0)), 1)]),
        ("one quartet", [(("1", 4, F(0)), 1)]),
        ("two quartets", [(("1", 4, F(0)), 2)]),
        ("three neutral singlets", [(("1", 1, F(0)), 3)]),
        ("charged singlet", [(("1", 1, F(1)), 1)]),
        ("charged singlet pair", [(("1", 1, F(1)), 1), (("1", 1, F(-1)), 1)]),
        ("doublets of opposite charge",
         [(("1", 2, h), 1), (("1", 2, -h), 1)]),
        ("doublets of equal charge", [(("1", 2, h), 2)]),
        ("colour triplet", [(("3", 1, F(0)), 1)]),
        ("colour triplet and antitriplet",
         [(("3", 1, F(0)), 1), (("3b", 1, F(0)), 1)]),
        ("two triplets, three antitriplets",
         [(("3", 1, F(0)), 2), (("3b", 1, F(0)), 3)]),
        ("coloured doublet", [(("3", 2, F(1, 6)), 1)]),
        ("coloured doublet and its conjugate",
         [(("3", 2, F(1, 6)), 1), (("3b", 2, F(-1, 6)), 1)]),
        ("coloured triplet-of-SU(2) pair",
         [(("3", 3, F(0)), 1), (("3b", 3, F(0)), 1)]),
        ("three colour triplets", [(("3", 1, F(0)), 3)]),
        ("three colour antitriplets", [(("3b", 1, F(0)), 3)]),
        ("three triplets and one antitriplet",
         [(("3", 1, F(0)), 3), (("3b", 1, F(0)), 1)]),
        ("two coloured doublets", [(("3", 2, F(0)), 2)]),
        ("mixed", [(("1", 2, F(0)), 3), (("1", 3, F(0)), 2),
                   (("3", 1, F(1, 3)), 1), (("3b", 1, F(-1, 3)), 2)]),
    ]


def check_L_mass_protection_carrier():
    name = "check_L_mass_protection_carrier"
    legs = {}
    disclosures = [
        "anomalies are not computed; protected contents in the catalog "
        "include anomalous ones, the single doublet among them",
        "the reduced-group leg tests two linear relations among the "
        "quark values and a lepton condition; it leaves Y_Q free and "
        "does not single out the Standard Model (the controls leg "
        "exhibits a non-Standard assignment that satisfies it)",
        "the explicit form certifies a lower bound on the largest rank; "
        "the matching upper bound is named, not computed",
        "leg conjugate_pairing_method_test is forced (the evaluation "
        "pairing exists); it tests the code",
        "in legs su2_single_irrep_parity and doublet_only_contents_count "
        "the Weyl count is the witness; the reality count restates the "
        "claim",
        "the catalog is pinned by size and distinct labels, not by "
        "content; no expected value of I or p is pinned",
        "the hypercharge read is by value, but replacing the read with "
        "the same literals would pass: the legs test the values, not "
        "their provenance",
        "the claim-surface hash is carried, not verified, by the module",
        "the guard that the upstream record returned passed=True is not "
        "exercised by any leg (no failing upstream record is available "
        "as a fixture)",
        "in the reduced-group statement the equal-multiplicity condition "
        "is implied by p = 0; deleting it changes no outcome",
    ]

    # -- hypercharges by value ----------------------------------------------
    tie_ev, gen, vals = "", None, None
    try:
        from apf import gauge as _gauge
        rec = _gauge.check_T_field()
        if rec.get("passed") is not True:
            raise ValueError("check_T_field did not return passed=True")
        hc = _find_key(rec, "hypercharges")
        vals = {k: F(str(hc[k])) for k in ("Y_Q", "Y_u", "Y_d", "Y_L", "Y_e")}
        gen = _generation(vals)
        tie_ev = "read %s from check_T_field (passed=True)" % (
            {k: str(v) for k, v in sorted(vals.items())},)
    except Exception as exc:  # recorded, not raised
        tie_ev = "hypercharge read failed: %r" % (exc,)

    authored = _catalog()
    catalog = list(authored)
    if gen is not None:
        catalog.append(("one generation (hypercharges read by value)", gen))
        catalog.append(("one generation and a neutral singlet",
                        gen + [(("1", 1, F(0)), 1)]))

    # -- leg 1 ---------------------------------------------------------------
    rows = [(lab, _invariants_by_reality(c), _invariants_by_weights(c))
            for lab, c in catalog]
    n_agree = sum(1 for r in rows if r[1] == r[2])
    n_prot = sum(1 for r in rows if r[2] == 0)
    n_unprot = sum(1 for r in rows if r[2] > 0)
    size_ok = (len(authored) == AUTHORED_CATALOG_SIZE
               and len(catalog) == AUTHORED_CATALOG_SIZE + TIED_CATALOG_SIZE
               and len(set(lab for lab, _ in catalog)) == len(catalog))
    legs["two_counts_agree_on_pinned_catalog"] = (
        size_ok and n_agree == len(catalog) and n_prot > 0 and n_unprot > 0,
        "catalog: %d authored + %d tied (pinned %d + %d); counts agree on "
        "%d; I = 0 on %d, I > 0 on %d; values %s" % (
            len(authored), len(catalog) - len(authored),
            AUTHORED_CATALOG_SIZE, TIED_CATALOG_SIZE, n_agree, n_prot,
            n_unprot, [(r[0], r[1], r[2]) for r in rows]))

    # -- leg 2 ---------------------------------------------------------------
    pr = [(_invariants_by_weights(_paired(c)),
           _invariants_by_reality(_paired(c))) for _lab, c in catalog]
    n_good = sum(1 for b, a in pr if b >= 1 and a == b)
    legs["conjugate_pairing_method_test"] = (
        n_good == len(catalog),
        "%d of %d paired contents have I >= 1 with the counts equal; "
        "least I = %d" % (n_good, len(catalog), min(b for b, _a in pr)))

    # -- leg 3 ---------------------------------------------------------------
    d_range = list(range(D_BOUNDS[0], D_BOUNDS[1] + 1))
    single = {d: (_invariants_by_reality([(("1", d, F(0)), 1)]),
                  _invariants_by_weights([(("1", d, F(0)), 1)]))
              for d in d_range}
    both = all(a == b for a, b in single.values())
    parity = all((single[d][1] == 0) == (d % 2 == 0) for d in d_range)
    legs["su2_single_irrep_parity"] = (
        both and parity and len(single) == D_BOUNDS[1] - D_BOUNDS[0] + 1
        and min(d_range) == 1 and max(d_range) == 12,
        "d = %d..%d (%d values); (reality, weights) by d: %s" % (
            min(d_range), max(d_range), len(single),
            sorted(single.items())))

    # -- leg 4 ---------------------------------------------------------------
    n_range = list(range(N_BOUNDS[0], N_BOUNDS[1] + 1))
    multi = {n: (_invariants_by_reality([(("1", 2, F(0)), n)]),
                 _invariants_by_weights([(("1", 2, F(0)), n)]))
             for n in n_range}
    legs["doublet_only_contents_count"] = (
        all(a == b == n * (n - 1) // 2 for n, (a, b) in multi.items())
        and min(n_range) == 1 and max(n_range) == 6,
        "n = %d..%d; (reality, weights) by n: %s" % (
            min(n_range), max(n_range), sorted(multi.items())))

    # -- legs needing the read -----------------------------------------------
    reduced = None
    if gen is None:
        for lab in ("one_generation_fully_protected_under_G",
                    "reduced_group_pairing_structure",
                    "controls_computed"):
            legs[lab] = (False, tie_ev)
    else:
        reduced = _reduce_to_em(gen)
        ia, ib = _invariants_by_reality(gen), _invariants_by_weights(gen)
        pg, dg = _protected_by_reality(gen), _dim(gen)
        legs["one_generation_fully_protected_under_G"] = (
            ia == 0 and ib == 0 and pg == dg and len(_merge(gen)) == 5,
            "%s; I under G: %d (reality), %d (weights); protected "
            "dimension %d of %d" % (tie_ev, ia, ib, pg, dg))

        s6_ok, s6 = _s6_holds(gen)
        legs["reduced_group_pairing_structure"] = (
            s6_ok, "reduced to SU(3) x U(1)_em: %s" % (sorted(s6.items()),))

        # (a) wrong reality count
        wrong = [lab for lab, c in catalog
                 if _invariants_by_reality(c, pseudoreal_sign=1)
                 != _invariants_by_weights(c)]
        # (b) Weyl terms met and not met
        totals = Counter()
        for _lab, c in catalog:
            for idx, (length, hits) in enumerate(
                    _term_hits(_sym2_weight_counts(c))):
                totals[(idx, length)] += hits
        long_hits = _long_hits((ln, h) for (_i, ln), h in totals.items())
        short_met = sum(1 for (_i, ln), h in totals.items()
                        if ln <= 1 and h > 0)
        fixtures = [Counter({(0, -3, 0, F(0)): 1, (0, 0, 0, F(0)): 1}),
                    Counter({(-3, 0, 0, F(0)): 1}),
                    Counter({(-2, -2, 0, F(0)): 1})]
        fixture_long = sum(1 for f in fixtures
                           if _long_hits(_term_hits(f)) >= 1)
        # (c) invariance fixtures
        fx = [(("3", 2, F(1, 6)), 1), (("3b", 2, F(-1, 6)), 1)]
        gens = _generators(fx)
        parts = {"SU(2)": gens[0:3], "colour": gens[3:12],
                 "U(1)": gens[12:13]}
        good = _explicit_form(fx)
        bad = {"SU(2)": _explicit_form(fx, su2_identity=True),
               "colour": _explicit_form(fx, colour_shift=1),
               "U(1)": [row[:] for row in good]}
        bad["U(1)"][0][0] += F(1)
        accepted = sorted(k for k, g in parts.items()
                          if _is_invariant(good, g))
        rejected = sorted(k for k, g in parts.items()
                          if not _is_invariant(bad[k], g))
        # (d) weights against Cartan eigenvalues
        weights_ok = []
        for c in ("3", "3b"):
            cc = [((c, 1, F(0)), 1)]
            g = _generators(cc)
            e = [[g[3 + 4 * a][s][s] for a in range(3)] for s in range(3)]
            cartan = sorted((v[0] - v[1], v[1] - v[2]) for v in e)
            used = sorted((w[0], w[1]) for w in _weights(cc))
            weights_ok.append(cartan == used and len(used) == 3)
        for d in (1, 2, 3, 4, 5):
            cc = [(("1", d, F(0)), 1)]
            g = _generators(cc)
            cartan = sorted(g[2][s][s] for s in range(d))
            used = sorted(F(w[2]) for w in _weights(cc))
            weights_ok.append(cartan == used and len(used) == d)
        # (e) altered assignments
        altered = []
        for k in ("Y_Q", "Y_u", "Y_d", "Y_L", "Y_e"):
            v = dict(vals)
            v[k] = -v[k]
            altered.append(("%s negated" % k, _generation(v)))
            v = dict(vals)
            v[k] = v[k] + F(1, 3)
            altered.append(("%s shifted by 1/3" % k, _generation(v)))
        v = dict(vals)
        v["Y_u"], v["Y_e"] = v["Y_e"], v["Y_u"]
        altered.append(("Y_u and Y_e exchanged", _generation(v)))
        g2 = _generation(vals)
        g2[1] = (("3", 1, g2[1][0][2]), 1)
        altered.append(("u^c given colour 3", g2))
        g2 = _generation(vals)
        g2[0] = (("3", 1, g2[0][0][2]), 1)
        altered.append(("Q made an SU(2) singlet", g2))
        outcomes = [(lab, _s6_holds(c)[0]) for lab, c in altered]
        passing = [lab for lab, ok in outcomes if ok]
        v = dict(vals)
        for k in ("Y_Q", "Y_u", "Y_d"):
            v[k] = v[k] + F(1, 6)
        covariant = _s6_holds(_generation(v))[0]
        legs["controls_computed"] = (
            len(wrong) >= 1
            and long_hits == 0 and short_met == 3 and fixture_long == 3
            and accepted == sorted(parts) and rejected == sorted(parts)
            and all(weights_ok) and len(weights_ok) == 7
            and len(outcomes) == 13 and not passing and covariant,
            "(a) pseudoreal-as-real count disagrees with the Weyl count "
            "on %d catalog contents; (b) long SU(3) terms meet %d colour "
            "weights over the catalog, short terms met: %d, fixtures on "
            "which a long term is reported: %d; (c) unaltered form accepted by %s, violating forms "
            "rejected by %s; (d) weights equal Cartan eigenvalues on %d "
            "of %d irreps; (e) altered assignments and whether each "
            "satisfies the reduced-group statement: %s; covariant shift "
            "of Y_Q, Y_u, Y_d by 1/6 satisfies it: %r" % (
                len(wrong), long_hits, short_met, fixture_long, accepted,
                rejected, sum(weights_ok), len(weights_ok), outcomes,
                covariant))

    # -- leg 7: explicit forms -----------------------------------------------
    forms = list(catalog)
    if reduced is not None:
        forms.append(("one generation reduced to SU(3) x U(1)_em", reduced))
    rows7, bad7, mixed_case, gen_counts = [], [], 0, set()
    for lab, c in forms:
        n, sym, inv, n_gens, p_explicit = _form_report(c)
        p_formula = _protected_by_reality(c)
        gen_counts.add(n_gens)
        rows7.append((lab, n, p_formula, p_explicit))
        if not (sym and inv and n_gens == GENERATOR_COUNT
                and n == _dim(c) and p_explicit == p_formula):
            bad7.append((lab, sym, inv, n_gens, n, p_formula, p_explicit))
        if _invariants_by_weights(c) >= 1 and p_formula > 0:
            mixed_case += 1
    legs["protected_dimension_matches_explicit_form"] = (
        not bad7 and len(rows7) == len(catalog) + 1 and mixed_case >= 1,
        "%d forms built (catalog %d + the reduced content); generator "
        "counts used: %s (pinned %d); failures %s; contents with I >= 1 "
        "and p > 0: %d; (content, dim, p by formula, dim - rank): %s" % (
            len(rows7), len(catalog), sorted(gen_counts), GENERATOR_COUNT,
            bad7, mixed_case, rows7))

    return _result(
        name, legs,
        key_result=(
            "On the catalog the two counts of invariant mass terms agree "
            "and the protected dimension by the reality-type formula "
            "equals dim V minus the rank of an explicit invariant "
            "symmetric form; the one-generation content built from the "
            "five hypercharges read from check_T_field has I = 0 and p = "
            "dim V under G, and under SU(3) x U(1)_em is conjugate-paired "
            "with one self-conjugate state and p = 0; the reduced-group "
            "statement leaves Y_Q free"),
        dependencies=["T_field"],
        disclosures=disclosures)


_CHECKS = {"L_mass_protection_carrier": check_L_mass_protection_carrier}


def run_all():
    return {k: f() for k, f in _CHECKS.items()}


def register(registry):
    if HELD_OUT_OF_THE_BANK:
        raise RuntimeError(
            "mass_protection_carrier is HELD: not audited, not lifted")
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
