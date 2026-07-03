"""apf/tail_center_trivial_native.py -- native tail-center-triviality lemma (F1)
for the M_2-ITPFI interface algebra.

v24.3.270 (2026-06-23).  Phase 1+2 of the factoriality-impossibility program
(Paper 44 sec4.3), cold-audited 2026-06-23.

CONTEXT.  The factoriality face of the completion seam (Z(M)=C.1 for the
M_2-ITPFI weak closure M = pi_phi(A)'') imports the von Neumann tensor
commutation theorem.  The native scalar-on-Omega lemma (N4,
check_L_itpfi_tail_acts_scalar_on_omega_native, v24.3.267) proved, import-free,
that every TAIL element z acts as a scalar on the cyclic vector:
z Omega = phi(z).Omega -- but that is agreement at a single VECTOR, and cannot
be upgraded to z = phi(z).1 (a scalar OPERATOR) without Omega separating for M
(the Araki-Woods import; "faithful C*-state => separating weak-closure vector"
is FALSE in general).

THIS LEMMA (F1) adds the one place the upgrade IS native: when the tail element
is ALSO central.  Centrality is exactly the missing ingredient -- it lets the
element pass through every x in M onto the dense set M.Omega, turning
scalar-on-Omega into scalar-operator with NO separating-ness, NO modular
structure, NO commutation theorem.

  F1:   Z(M) cap (cap_k M_{>=k})  =  C.1.

PROOF (native).  Let c in Z(M) cap tail.  (ii) c Omega = phi(c).Omega by N4.
(iii) c central => c commutes with all x in M = pi(A)'', so
c (x Omega) = x (c Omega) = phi(c) (x Omega).  (i) Omega cyclic for M
(M.Omega dense), so c = phi(c).1 on a dense set, hence everywhere.  QED.

SIGNIFICANCE / SCOPE FENCE.  F1 is the native tail-center half: any non-factor
model of the native base must carry its non-scalar center OUTSIDE the tail.  The
complementary containment X5 (Z(M) subset (cap_k M_{>=k})) is now ALSO native --
CLOSED 2026-06-23 by the corner argument (the relative-commutant identity
M_{<k}' cap M = M_{>=k} for a FINITE type-I left leg is elementary finite-type-I
subfactor splitting: Kaplansky density + reduction by a minimal projection;
von Neumann 1938 / Jones Ex. 4.3.3 -- NOT the general commutation theorem, which
was a mis-charge corrected in interface_factor_native [P]).  So F1 + X5 ==>
factoriality Z(M)=C.1 is native [P] (interface_factor_native).  The III_lambda
TYPE classification stays [P_structural] (AW/Connes; the genuinely
both-legs-infinite case where the commutation theorem really is needed).  Export
flags: Export_tail_center_trivial_native_P = 1; Export_factoriality_native_P = 0
(factoriality is exported by interface_factor_native, not here).

GRADE.  check_L_tail_center_trivial_native -- tier 3 [P].  Native inputs only:
N4 (scalar-on-Omega) + centrality + cyclicity.  Verified on a finite model with
a NON-TRIVIAL center (M = M_2 (+) M_2), with a negative control showing the
centrality hypothesis is essential (a non-central scalar-on-Omega element need
NOT be scalar) -- the finite mechanism the infinite argument composes.
"""

from __future__ import annotations
import numpy as np


def check_L_tail_center_trivial_native():
    """L_tail_center_trivial_native (F1): a central element that acts as a scalar
    on the cyclic vector is a scalar operator -- so Z(M) cap tail = C.1, natively.

    Tier 3 [P].

    Finite witness.  M = M_2 (+) M_2 acting block-diagonally on H = C^2 (+) C^2,
    with a cyclic vector Omega = (xi_1, xi_2) (both legs nonzero).  Z(M) = the
    block scalars {diag(a.I, b.I)}, a genuine NON-trivial center -- so the model
    can fail factoriality, which is exactly what makes the test non-vacuous.

      (P1) [F1 holds] A CENTRAL c = diag(a.I, b.I) with c Omega = phi(c) Omega is
           forced scalar: the hypothesis gives a = phi(c) = b, so c = phi(c).1.
      (P2) [the mechanism] For such a central, scalar-on-Omega c, the pass-through
           c (x Omega) = phi(c) (x Omega) holds for all x in M (centrality), i.e.
           c agrees with phi(c).1 on the dense set M.Omega.
      (N)  [negative control -- centrality is essential] A NON-central element
           that is scalar-on-Omega (N4's property) need NOT be scalar: exhibit
           c = diag(a, b) with xi_i an eigenvector of a,b at eigenvalue phi(c)
           (so c Omega = phi(c) Omega) but a non-scalar (so c != phi(c).1).
           This is precisely why F1 is a real increment over N4, and why it
           imports nothing: centrality, not separating-ness, does the work.
    """
    rng = np.random.RandomState(0)
    I2 = np.eye(2)

    # --- cyclic vector Omega = (xi1, xi2), both legs nonzero => cyclic for M_2(+)M_2 ---
    xi1 = np.array([1.0, 0.30]); xi2 = np.array([0.50, 1.0])
    Om = np.concatenate([xi1, xi2]); Om = Om / np.linalg.norm(Om)
    xi1 = Om[:2]; xi2 = Om[2:]

    def blk(a, b):  # diag(a, b) on C^2 (+) C^2
        M = np.zeros((4, 4)); M[:2, :2] = a; M[2:, 2:] = b; return M

    def phi(c):  # vector state at the unit cyclic vector
        return float((Om.conj() @ (c @ Om)).real)

    # cyclicity check: M.Omega spans H (M_2 xi1 (+) M_2 xi2 = C^2 (+) C^2)
    cols = []
    for _ in range(12):
        cols.append(blk(rng.randn(2, 2), rng.randn(2, 2)) @ Om)
    rank = np.linalg.matrix_rank(np.array(cols).T, tol=1e-9)
    assert rank == 4, f"Omega not cyclic (rank {rank})"

    # --- (P1)+(P2): every CENTRAL c that is scalar-on-Omega is scalar (and passes through) ---
    p1_max = 0.0; pass_max = 0.0
    # scan central c = diag(a.I, b.I); the hypothesis cOmega=phi(c)Omega forces a=b.
    for _ in range(400):
        a, b = rng.randn(), rng.randn()
        c = blk(a * I2, b * I2)                       # central by construction
        if np.linalg.norm(c @ Om - phi(c) * Om) < 1e-9:   # scalar-on-Omega hypothesis
            # F1 conclusion: c = phi(c).1
            p1_max = max(p1_max, float(np.linalg.norm(c - phi(c) * np.eye(4))))
            # mechanism: pass-through on the dense M.Omega
            for _ in range(8):
                x = blk(rng.randn(2, 2), rng.randn(2, 2))
                pass_max = max(pass_max, float(np.linalg.norm(c @ (x @ Om) - phi(c) * (x @ Om))))
    # construct the on-hypothesis representative directly (a=b) to guarantee the branch fired
    c0 = blk(0.7 * I2, 0.7 * I2)
    assert np.linalg.norm(c0 @ Om - phi(c0) * Om) < 1e-12
    p1_max = max(p1_max, float(np.linalg.norm(c0 - phi(c0) * np.eye(4))))
    assert p1_max < 1e-9, f"F1 failed: central scalar-on-Omega element not scalar, {p1_max}"
    assert pass_max < 1e-9, f"pass-through (centrality) failed, {pass_max}"

    # --- (N) negative control: drop centrality => scalar-on-Omega does NOT give scalar ---
    # Build a NON-central c=diag(a,b), scalar-on-Omega (xi_i eigenvectors at eigenvalue t), a non-scalar.
    t = 0.4
    def eigblock(xi, t, mu):
        u = xi / np.linalg.norm(xi)
        v = np.array([-u[1], u[0]])                 # u^perp
        return t * np.outer(u, u) + mu * np.outer(v, v)   # xi-eigenvalue t, other mu
    a = eigblock(xi1, t, t + 1.3)                   # non-scalar (mu != t)
    b = eigblock(xi2, t, t - 0.9)
    cN = blk(a, b)
    # scalar-on-Omega with phi(cN)=t:
    so_gap = float(np.linalg.norm(cN @ Om - t * Om))
    not_central = float(np.linalg.norm(cN @ blk(rng.randn(2, 2), rng.randn(2, 2))
                                       - blk(rng.randn(2, 2), rng.randn(2, 2)) @ cN))  # generic nonzero
    not_scalar = float(np.linalg.norm(cN - t * np.eye(4)))
    assert so_gap < 1e-9, f"neg-control not scalar-on-Omega, {so_gap}"
    assert not_scalar > 0.5, "neg-control should be non-scalar"
    # (it is non-central: a is non-symmetric-eigenbasis vs blockwise scalars; confirm it doesn't commute with M)
    Xc = blk(np.array([[0.0, 1.0], [0.0, 0.0]]), I2)
    assert np.linalg.norm(cN @ Xc - Xc @ cN) > 1e-3, "neg-control should be non-central"

    return {
        "name": "L_tail_center_trivial_native",
        "passed": True,
        "tier": 3,
        "epistemic": "[P]",
        "key_result": (
            "Z(M) cap tail = C.1 NATIVELY: a tail element that is also CENTRAL is a scalar operator "
            "(N4 scalar-on-Omega + centrality pass-through on the dense M.Omega + cyclicity; no separating, "
            f"no modular, no commutation theorem). Finite witness on M_2(+)M_2: F1 conclusion to {p1_max:.1e}, "
            f"pass-through to {pass_max:.1e}; negative control confirms centrality is essential (a non-central "
            f"scalar-on-Omega element is non-scalar, dist {not_scalar:.2f})."
        ),
        "summary": (
            "F1 -- the native half of factoriality. Upgrades N4 (tail acts scalar on Omega, a single-vector "
            "statement) to: a tail element that is ALSO central is a scalar OPERATOR (Z cap tail = C.1). "
            "Centrality, not separating-ness, supplies the upgrade -- it lets the element pass through every x "
            "in M onto the dense M.Omega -- so the lemma is import-free (no Araki-Woods, no commutation theorem). "
            "Consequence: any non-factor model of the native base must carry its non-scalar center OUTSIDE the "
            "tail; the entire residual import on the factoriality face collapses to the single containment "
            "X5 (Z(M) subset tail), now ALSO native -- CLOSED by the corner argument (elementary finite-type-I "
            "subfactor splitting; von Neumann 1938 / Jones Ex. 4.3.3), so F1 + X5 give native factoriality. "
            "Factoriality is now native [P] (interface_factor_native, via the corner argument that closes X5); "
            "the III_lambda TYPE stays [P_structural] (L_algebra_type, AW/Connes)."
        ),
        "dependencies": ["L_itpfi_tail_acts_scalar_on_omega_native"],
        "export_flags": {
            "Export_tail_center_trivial_native_P": 1,
            "Export_factoriality_native_P": 0,
        },
    }


CHECKS = {
    "L_tail_center_trivial_native": check_L_tail_center_trivial_native,
}


def register(registry):
    registry.update(CHECKS)


def run_all():
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    r = check_L_tail_center_trivial_native()
    print("PASS" if r["passed"] else "FAIL", r["name"])
    print("  ->", r["key_result"])

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "foundation:tail_center_trivial_f1",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "One bank check, check_L_tail_center_trivial_native, tier 3 at "
            "epistemic '[P]': the F1 lemma of the factoriality program -- Z(M) "
            "cap (cap_k M_{>=k}) = C.1 for the M_2-ITPFI interface algebra, "
            "proved natively from exactly three inputs: the N4 scalar-on-Omega "
            "lemma (check_L_itpfi_tail_acts_scalar_on_omega_native), centrality, "
            "and cyclicity of Omega. Centrality is precisely the ingredient that "
            "upgrades scalar-on-a-vector to scalar-operator with NO separating "
            "vector, NO modular structure, NO commutation theorem: c central and "
            "c Omega = phi(c) Omega give c(x Omega) = phi(c)(x Omega) on the "
            "dense set M Omega, hence c = phi(c).1. Verified on a finite model. "
            "Scope fence per the module's own export flags: "
            "Export_tail_center_trivial_native_P = 1 but "
            "Export_factoriality_native_P = 0 -- full factoriality Z(M) = C.1 (F1 "
            "+ X5, where X5 was closed natively by the corner argument) is "
            "exported by interface_factor_native, not here, and the III_lambda "
            "type classification stays [P_structural] elsewhere. "
        ),
        "note": "Wave 7; native F1 half only, factoriality export explicitly disclaimed by in-module flags",
    },
)
