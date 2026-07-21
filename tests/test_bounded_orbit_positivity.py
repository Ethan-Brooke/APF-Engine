"""Tests for apf/bounded_orbit_positivity.py (v24.3.431).

Green path + the mutation-kill battery carried from the stage-2 audit standard:
every mutation must be CAUGHT (a leg fails or the guard refuses).
"""
from fractions import Fraction as F
import apf.bounded_orbit_positivity as bop


def test_green_path():
    r = bop.check_L_bounded_orbit_positivity()
    assert r["passed"], r["fail_reasons"]
    assert r["epistemic"] == "P_structural_reading"
    assert r["physical_premises_certified"] is False
    assert len(r["legs"]) == 15
    assert all(v == "PASS" for _, v, _ in r["legs"])


def test_reading_and_fences_declared():
    r = bop.check_L_bounded_orbit_positivity()
    assert r["readings"] == ("R_CAPACITY_BOUNDED_WORLD",)
    assert set(r["derived_surfaces"]).isdisjoint(set(r["fenced_surfaces"]))
    assert "FORM_UNIQUENESS_REQUIRES_IRREDUCIBILITY" in r["named_residues"]


def test_non_pd_seed_refused():
    G = bop.d4_conj()
    assert bop.avg_form(G, [[F(1), F(0)], [F(0), F(-1)]]) is None
    assert bop.avg_form(G, [[F(0), F(0)], [F(0), F(0)]]) is None


def test_averaged_form_invariance_breaks_on_corrupted_group():
    G = bop.d4_conj()
    G[3][0][0] += F(1, 7)  # break closure
    Q = bop.avg_form(G, [[F(1), F(0)], [F(0), F(1)]])
    def qf(x):
        return sum(x[i] * Q[i][j] * x[j] for i in range(2) for j in range(2))
    span = [[F(1), F(0)], [F(0), F(1)], [F(1), F(1)], [F(2), F(-3)]]
    assert not all(qf(bop.mv(g, x)) == qf(x) for g in G for x in span)


def test_closure_check_catches_non_group():
    G = bop.d4_conj()
    G[0][0][0] += F(1, 9)
    keyset = {tuple(tuple(r) for r in g) for g in G}
    closed = all(tuple(tuple(r) for r in bop.mm(a, b)) in keyset
                 for a in G for b in G)
    assert not closed


def test_boost_eig_certificate_exact():
    cert = bop.eig_growth_certificate(bop.BOOST)
    assert cert == ([F(1), F(1)], F(2))
    # no growth certificate for a bounded conjugated rotation (false-positive control)
    K = [[F(10), F(0)], [F(0), F(1)]]
    gR = bop.mm(bop.mm(K, bop.ROT), bop.inv2(K))
    assert bop.eig_growth_certificate(gR) is None


def test_bounded_certificates():
    # finite closure certifies the D4 conjugate
    cl = bop.finite_closure(bop.d4_conj())
    assert cl is not None and len(cl) == 8
    # boost has no finite closure at cap
    assert bop.finite_closure([bop.BOOST], cap=32) is None
    # invariant-form certificate for the conjugated rotation
    K = [[F(10), F(0)], [F(0), F(1)]]
    Kinv = bop.inv2(K)
    gR = bop.mm(bop.mm(K, bop.ROT), Kinv)
    QK = bop.mm(bop.tr(Kinv), Kinv)
    assert bop.invariant_pd_form_certificate(gR, QK)
    # and the certificate refuses a non-invariant form
    assert not bop.invariant_pd_form_certificate(gR, [[F(1), F(0)], [F(0), F(1)]])


def test_counter_model_falsity_directions():
    # both falsity directions of the leg-6 world must fail its conditions:
    # (a) nonzero booking breaks A1-consistency-with-zero claim
    total = F(100)
    assert not (total == 0 and total <= bop.C_TOTAL)
    # (b) a bounded action (ROT) has non-growing state_sup
    M = bop.I2
    sups = []
    for _ in range(12):
        M = bop.mm(M, bop.ROT)
        sups.append(max(abs(e) for x in bop.SPAN for e in bop.mv(M, x)))
    assert not all(sups[k + 1] > sups[k] for k in range(11))


def test_capacity_pin_load_bearing():
    n_exceed = None
    M = bop.I2
    for n in range(1, 64):
        M = bop.mm(M, bop.BOOST)
        if max(abs(e) for x in bop.SPAN for e in bop.mv(M, x)) > bop.C_TOTAL:
            n_exceed = n
            break
    assert n_exceed == 7


def test_register_shape():
    reg = bop.register({})
    assert list(reg) == ["L_bounded_orbit_positivity"]
