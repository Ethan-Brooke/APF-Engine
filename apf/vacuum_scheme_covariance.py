"""APF vacuum scheme covariance -- the S_42-covariant fence SPLIT.

v24.3.373 (2026-07-03). The Paper 45 SS8 named open (the S_42-covariant
refinement of the .357 exact-fill scheme) walked to its computable boundary
and banked at the split: the hoped-for dichotomy ("covariance kills the
coherent schemes at exact fill => classicality forced by symmetry where
dimension failed") is REFUTED at every computable small case, and the
banked 2x3x7 construction itself carries product-affine subgroup
covariance. Full S_42 at (n, q) = (61, 42) stays OPEN, both formulations.
Walk + fresh-context hostile audit LAND-WITH-FIXES 0.85 (2026-07-03; all
four required fixes carried, including the F1/F2 as-built wording this
docstring uses); the audit re-derived the decisive q = 3 witness from
scratch, W-free, at < 3e-16. Note of record: "Reference - The
S42-Covariant Sector-Aligned Scheme Walked - Covariance Does Not Kill
Coherence at Exact Fill (2026-07-03)"; witnesses The Turning/
s42_covariant_walk_*_2026-07-03.py + s42_covariant_AUDIT_*.py.

THE FORMULATIONS (carried; never conflate):
  (F1) MODE-TYPED: E(P_pi rho P_pi^dag) = P_pi^{xn} E(rho) P_pi^{dag xn}
       -- the logical action IS the mode permutation (secret mode-typed).
  (F2) SOME-REP: some unitary rep V_pi as the logical action.
  (F3) orbit-closure: vacuous (typed in the note, not here).
  Selecting F1 vs F2 as THE physically mandated demand is a
  principal-shaped reading, not certified here.

WHAT THIS CHECK CERTIFIES (exact / computed):
  (i)   THE OFFSET LAW: for the polynomial cascade at prime p with n
        shares, the affine mode map P_(u,c) applied to every share
        induces the logical P_(u, -(n-2)c mod p). Verified by logical
        extraction at Choi strength (maximally entangled reference,
        exact recovery, induced unitary read off the output): p = 3 at
        n = 2, 3, 4, 5 (all 6 elements of AGL(1,3) = S_3) and p = 7 at
        n = 2 (all 42 elements) and n = 3 (generators + composite;
        extension to all 42 by homomorphism -- both sides of the F-law
        are multiplicative in the group element).
  (ii)  F1 AS BUILT WHERE THE LAW SAYS SO: at p = 3, n = 4 (offset
        -(n-2) = -2 == 1 mod 3) the cascade is F1-covariant for the FULL
        S_3, as built, all 6 elements exact. NEGATIVE CONTROL (the
        audit's sharpest catch, pinned): at n = 3 (offset == 2 != 1) the
        cascade is NOT F1 as built -- the extracted logical is
        P_(u, 2c), and the D_2 dressing (E o Ad(D_2), a re-typing of the
        secret's mode identification, D_m the scaling x -> mx) restores
        F1 exactly.
  (iii) F1 at n = 7 as built (offset -(5) == 1 mod 3), generators of
        S_3, sparse extraction exact; all 6 by multiplicativity.
  (iv)  q = 2 TRANSVERSAL F1: the banked [[5,1,3]]-derived mixed ((3,3))
        and ((5,5)) qubit schemes (built via apf/vacuum_label_code's own
        machinery) are F1-covariant for S_2 = {id, X} -- transversal
        X-bar, exact.
  (v)   THE PRODUCT MECHANISM at dim 6: both factors (the qubit ((3,3))
        and the D_2-dressed qutrit ((3,3))) are verified F1-covariant
        densely at channel strength for all 12 elements of S_2 x S_3;
        the tensor is F1 for the product group by the product-channel
        identity (tensor of covariant channels, logical g2 x g3 -- a
        one-line algebraic step, not separately computed). This is the composition mechanism that gives the
        banked 2x3x7 ((61,61)) scheme its G_0 = S_2 x S_3 x AGL(1,7)
        covariance (|G_0| = 504): F2 AS BUILT (the logical is itself a
        mode permutation -- the image of pi under conjugation by D_4 on
        the 7-factor), F1 after the D_4 dressing.
  (vi)  THE n = 61 INTEGER COROLLARIES: -(61-2) == 1 (mod 3) -- the S_3
        factor is F1 as built at n = 61; -(61-2) == 4 (mod 7) -- the
        AGL(1,7) factor needs exactly the D_4 dressing; the dressing
        identity D_4 P_(u,c) D_4^{-1} = P_(u, 4c) verified as an integer
        permutation identity over all 42 elements of AGL(1,7). SCOPE:
        the n = 61 statement rides the offset law's recursion, computed
        exactly at n <= 7 here (n = 10 in the audit probes); the
        recursion step is derived in the walk note.
  (vii) THE q = 3 FULL-S_3 F1 WITNESS AT EXACT FILL (the dichotomy
        killer): a stored explicit isometry V: C^3 -> C^3 x C^3 x C^3
        (environment rep triv + std) is verified to be a perfect mixed
        ((2,2)) scheme for a coherent 3-dim secret with share dimension
        exactly 3 and FULL S_3 F1 covariance: isometry, covariance for
        all 6 group elements (transpositions included -- S_3, not its
        cyclic subgroup), single-share privacy at superoperator strength
        (both shares, all matrix units), exact recovery via
        entangled-reference decoupling + channel-superoperator rank 9,
        and all pair marginals of the purification = I/9 (a genuine
        AME(4,3)); tolerances <= 1e-10 on a stored witness verified by
        walk + audit at < 4e-16. NEGATIVE CONTROL WITH TEETH: the twirl
        route (frame-averaging the p = 3 ((2,2)) over S_3, frame to the
        environment) keeps covariance + privacy + share dims but
        collapses the channel superoperator rank 9 -> 3 with the exact
        identity E_tw = E_0 o (Fourier dephasing) -- coherent recovery
        impossible, residue exactly the classical 3-letter label. The
        covariant witness is NOT a twirl; the twirl provably cannot
        produce it.

WHAT THIS CHECK DOES NOT CERTIFY:
  (1) Full S_42 covariance at (61, 42) -- OPEN, both F1 and F2. The
      small-case EXISTS results and the G_0 subgroup covariance never
      close it; do not cite them as closing it.
  (2) No realization/identification claim: everything is at
      abstract-encoding strength on the banked skeleton; all of
      apf/vacuum_label_code's fences (carrier, identification, three-
      pronged aligned closure) are inherited unchanged.
  (3) The F1-vs-F2 demand selection (principal-shaped reading).
  (4) The offset law at n beyond the computed range rides the derived
      recursion (walk note); the n = 61 corollaries are integer
      consequences of that law.
  (5) Classicality-by-symmetry is refuted only where computed (q = 2, 3
      full S_q; G_0 <= S_42 at the banked scheme); the un-walked
      remainder (full S_42; the first non-affine cases q = 4, 5) is
      named open in the note.

FENCE SPLIT EXECUTED WITH THIS LANDING (count-neutral, same pass): the
.357 fence sentence "the 2x3x7 factorization is not mode-permutation
covariant" splits into (a) construction non-covariance under FULL S_42
(true; a fortiori by the as-built G_0 F1 failure at the 7-factor) and
(b) existence of some S_42-covariant scheme (open) -- see the updated
fence text in apf/vacuum_label_code.py.

STATUS: [P_structural_instrument] tier 4. Elementary/standard
mathematics (covariant channels, secret sharing, AME states; Eastin-
Knill inapplicable to finite groups [cited, unverified, not
load-bearing]); the content is the exact anchoring to the banked
scheme, the offset law, the split, and the witness.
Dependencies: T_vacuum_sector_aligned_scheme_share_dim_42,
T_vacuum_mixed_42dim_secret_scheme_exists, L_count,
T_interface_sector_bridge, T_horizon_reciprocity, L_QEC_code_space.
Cross-refs: T_vacuum_label_code_no_leakage,
T_vacuum_logical_sector_classical_ceiling,
T_which_v_no_registered_interior_reader,
T_vglobal_offdiagonal_blocks_scalar_typed.
"""

import math
from itertools import product as _iprod

import numpy as np

from apf.apf_utils import check, _result
from apf.vacuum_label_code import (
    _fiveq_codewords, _q33_encode, _q33_decode,
    _qss_build, _qss_encode_last, _qss_decode_last_pair, _qss_marginal,
)

_TOL = 1e-9


# ---------------------------------------------------------------------------
# Sparse-extraction machinery (clauses (i)-(iii))
# ---------------------------------------------------------------------------

def _affine_group(p):
    """AGL(1,p) as (u, c) pairs, u in 1..p-1, c in 0..p-1 (p prime)."""
    return [(u, c) for u in range(1, p) for c in range(p)]


def _apply_mode_map(state, n_shares, u, c, p):
    """Apply x -> u*x + c (mod p) to every share register (positions
    1..n_shares of the sparse tuple-state)."""
    out = {}
    for tup, amp in state.items():
        new = tuple((u * t + c) % p if 1 <= i <= n_shares else t
                    for i, t in enumerate(tup))
        out[new] = out.get(new, 0j) + amp
    return out


def _extract_logical(n, p, u, c):
    """Induced logical of the all-share mode map P_(u,c) on the p-ary
    cascade ((n,n)) scheme, extracted at Choi strength: encode a
    maximally entangled reference, apply the map to every share, decode,
    and read the unitary off the pure (reference, secret) output.
    Returns the p x p complex matrix L (global phase fixed positive on
    its largest entry)."""
    state, n_sh = _qss_build(n, p, d_ref=p)
    state = _apply_mode_map(state, n_sh, u, c, p)
    dec, m = state, n_sh
    while m > 1:
        dec, m = _qss_decode_last_pair(dec, m, p)
    rho = _qss_marginal(dec, (0, 1))
    # purity + factorization: psi_{r,s} with |Phi> = sum_r |r,r>/sqrt(p)
    # output (I x L)|Phi> => psi_{r,s} = L[s][r]/sqrt(p)
    keys = sorted({k[0] for k in rho})
    # anchor on the largest diagonal entry
    anchor = max(keys, key=lambda k: abs(rho.get((k, k), 0j)))
    a0 = rho.get((anchor, anchor), 0j).real
    check(a0 > 1e-12, f"extraction anchor vanishes at (n={n},p={p},u={u},c={c})")
    psi = {k: rho.get((k, anchor), 0j) / math.sqrt(a0) for k in keys}
    # purity: rho must equal |psi><psi|
    dev = max(abs(rho.get((k1, k2), 0j) - psi[k1] * psi[k2].conjugate())
              for k1 in keys for k2 in keys)
    check(dev < _TOL, f"extraction output not pure (dev {dev:.2e}) at "
                      f"(n={n},p={p},u={u},c={c}) -- recovery broken?")
    L = [[0j] * p for _ in range(p)]
    for (r, s), amp in psi.items():
        L[s][r] = amp * math.sqrt(p)
    # fix global phase on the largest entry
    flat = [L[s][r] for s in range(p) for r in range(p)]
    ph = max(flat, key=abs)
    ph = ph / abs(ph)
    return [[L[s][r] / ph for r in range(p)] for s in range(p)]


def _perm_target(u, c, p):
    """P_(u,c) as a p x p 0/1 matrix: column r has its 1 in row u*r+c."""
    M = [[0.0] * p for _ in range(p)]
    for r in range(p):
        M[(u * r + c) % p][r] = 1.0
    return M


def _mat_close(A, B, tol=_TOL):
    return max(abs(A[i][j] - B[i][j])
               for i in range(len(A)) for j in range(len(A))) < tol


def _conj_by_scaling(L, m, p):
    """D_m^{-1} L D_m with D_m the scaling permutation x -> m*x (mod p)."""
    minv = pow(m, -1, p)
    return [[L[(m * s) % p][(m * r) % p] for r in range(p)]
            for s in range(p)]


# ---------------------------------------------------------------------------
# Dense builders (clauses (v), (vii))
# ---------------------------------------------------------------------------

def _qubit33_isometry():
    """V2: C^2 -> C^8 (shares) x C^4 (env), the [[5,1,3]]-derived mixed
    ((3,3)), built from the banked module's own codewords."""
    cw = _fiveq_codewords()
    V = np.zeros((8, 4, 2), dtype=complex)
    for s in (0, 1):
        for b, amp in cw[s].items():
            kept = (b >> 2) & 7
            env = b & 3
            V[kept, env, s] += amp
    return V.reshape(32, 2)


def _qutrit33_isometry():
    """V3: C^3 -> C^27 (shares) x C^9 (env), one cascade level of the
    p = 3 polynomial scheme (base + one re-share of the last share)."""
    p = 3
    V = np.zeros((p, p, p, p, p, p), dtype=complex)  # (s1,s2,s3, e1,e2; s)
    for s in range(p):
        for a in range(p):
            # base: shares (a, a+s), env e1 = a+2s ; re-share x = a+s:
            for b in range(p):
                V[a, b, (b + (a + s)) % p, (a + 2 * s) % p,
                  (b + 2 * (a + s)) % p, s] += 1.0 / p
    return V.reshape(27 * 9, 3)


# ---------------------------------------------------------------------------
# The stored q = 3 full-S_3 F1 witness (clause (vii)); environment rep
# triv + std. Found by seeded Levenberg-Marquardt on the 14-dim
# S_3-invariant subspace (walk h5), verified by walk h5b and re-derived
# from scratch by the hostile audit (probe 1); stored here at 17
# significant digits. Layout: rows = share1 x share2 x env (27), cols =
# secret (3).
# ---------------------------------------------------------------------------

_WITNESS_V = np.array([
    [(0.26042651443018355-0.19841448099665604j), (0.013282911997214821-0.129439409595308j), (0.013282911997214843-0.129439409595308j)],
    [(0.030851866349654363-0.14812304809416363j), (0.1405088575795494-0.11009084983147031j), (0.15992204068125423-0.22452088151959751j)],
    [(-0.017812333341975333+0.085518881690353363j), (-0.10353923972627323+0.19569340098254934j), (-0.069914620257482907-0.0025052278130035387j)],
    [(0.0027807587055587485+0.14581379948410511j), (-0.19780496409901141-0.17560649780061022j), (0.063300483702850019-0.029995640474151573j)],
    [(-0.14956055750128752-0.018717954737902057j), (-0.039903566271392493+0.019314243524791358j), (-0.084302192854449967-0.13269197164947547j)],
    [(-0.053335498846887167+0.22578134946838055j), (-0.1354311211141524-0.086825359609339681j), (0.30009332379379872-0.13430039961098761j)],
    [(0.002780758705558801+0.14581379948410492j), (0.063300483702850019-0.0299956404741516j), (-0.19780496409901138-0.17560649780061022j)],
    [(-0.028590381825723932-0.2048913617093007j), (-0.30203953833876379+0.049961571976779313j), (0.097335008212166826+0.08485008887680312j)],
    [(0.15619099162372196-0.096680450424279737j), (-0.077038821290210641+0.18206481813218411j), (0.10227306264969799+0.026686054257321463j)],
    [(-0.19780496409901152-0.1756064978006103j), (0.0027807587055588149+0.14581379948410494j), (0.063300483702850019-0.029995640474151573j)],
    [(0.039903566271392348-0.019314243524791257j), (0.14956055750128758+0.018717954737902137j), (0.084302192854449995+0.13269197164947547j)],
    [(-0.13543112111415237-0.086825359609339667j), (-0.053335498846887222+0.22578134946838044j), (0.30009332379379866-0.13430039961098761j)],
    [(0.013282911997214724-0.12943940959530803j), (0.26042651443018339-0.1984144809966559j), (0.013282911997214843-0.129439409595308j)],
    [(-0.14050885757954945+0.11009084983147037j), (-0.030851866349654443+0.1481230480941638j), (-0.15992204068125423+0.22452088151959754j)],
    [(-0.10353923972627326+0.19569340098254948j), (-0.01781233334197534+0.085518881690353432j), (-0.069914620257482893-0.0025052278130035491j)],
    [(0.063300483702849936-0.029995640474151524j), (0.0027807587055588149+0.14581379948410494j), (-0.19780496409901138-0.17560649780061022j)],
    [(0.30203953833876374-0.049961571976779237j), (0.028590381825723855+0.20489136170930061j), (-0.097335008212166826-0.08485008887680312j)],
    [(-0.07703882129021071+0.18206481813218423j), (0.15619099162372196-0.096680450424279626j), (0.10227306264969797+0.02668605425732145j)],
    [(-0.19780496409901149-0.17560649780061019j), (0.063300483702850019-0.0299956404741516j), (0.0027807587055588131+0.14581379948410508j)],
    [(0.13723857448355953+0.065535845352011721j), (-0.21773734548431375+0.18265354362625472j), (0.1209701756755638-0.18617340697139853j)],
    [(0.033158058464454424+0.060139305352018273j), (-0.22305450250358805-0.047764418521196464j), (-0.10285549277683481-0.12910089904410066j)],
    [(0.063300483702849963-0.029995640474151462j), (-0.19780496409901141-0.17560649780061022j), (0.0027807587055588131+0.14581379948410508j)],
    [(0.21773734548431375-0.18265354362625474j), (-0.13723857448355928-0.065535845352011804j), (-0.1209701756755638+0.18617340697139853j)],
    [(-0.2230545025035881-0.04776441852119636j), (0.033158058464454437+0.060139305352018238j), (-0.1028554927768348-0.12910089904410074j)],
    [(0.013282911997214797-0.129439409595308j), (0.013282911997214843-0.129439409595308j), (0.26042651443018339-0.19841448099665587j)],
    [(0.019413183101704801-0.11443003168812718j), (-0.019413183101704781+0.11443003168812715j), (3.512784464529606e-18+9.8025444918850128e-19j)],
    [(0.17345385998375612-0.19318817316954581j), (0.17345385998375615-0.19318817316954587j), (0.035624666683950611-0.17103776338070675j)],
], dtype=complex)


def _s3_group():
    """S_3 as permutations of {0,1,2} (tuples img[r] = pi(r))."""
    from itertools import permutations
    return [tuple(g) for g in permutations(range(3))]


def _perm_np(img):
    M = np.zeros((3, 3))
    for r, i in enumerate(img):
        M[i][r] = 1.0
    return M


def _std_rep(img):
    """The standard 2-dim irrep block of the permutation rep: P restricted
    to the complement of the all-ones vector, in an orthonormal basis."""
    B = np.array([[1, -1, 0], [1, 1, -2]], dtype=float)
    B = (B.T / np.linalg.norm(B, axis=1)).T          # 2 x 3, orthonormal
    return B @ _perm_np(img) @ B.T


def _env_rep_triv_std(img):
    """W_pi = triv (+) std as a 3 x 3 block matrix."""
    W = np.zeros((3, 3))
    W[0, 0] = 1.0
    W[1:, 1:] = _std_rep(img)
    return W


def check_T_vacuum_scheme_product_affine_covariance():
    """T_vacuum_scheme_product_affine_covariance: The S_42-Covariant Fence Split [P_structural_instrument].

    See the module docstring: the offset law, the F1/F2 split on the
    banked construction (G_0 = S_2 x S_3 x AGL(1,7), F2 as built / F1
    after the D_4 dressing), the q = 2 and q = 3 full-S_q F1 witnesses
    at exact fill, and the twirl negative control. Full S_42 at
    (61, 42) stays OPEN.
    """
    # ---- (i) the offset law by extraction: p = 3, n = 2..5, all 6 ----
    for n in (2, 3, 4, 5):
        k = (-(n - 2)) % 3
        for (u, c) in _affine_group(3):
            L = _extract_logical(n, 3, u, c)
            tgt = _perm_target(u, (k * c) % 3, 3)
            check(_mat_close(L, tgt),
                  f"(i) offset law fails at p=3 n={n} (u,c)=({u},{c})")
    # p = 7: n = 2 all 42 (offset 0: translations act trivially);
    #        n = 3 generators + composite (offset -(1) == 6 mod 7)
    for (u, c) in _affine_group(7):
        L = _extract_logical(2, 7, u, c)
        check(_mat_close(L, _perm_target(u, 0, 7)),
              f"(i) offset law fails at p=7 n=2 (u,c)=({u},{c})")
    for (u, c) in ((1, 1), (3, 0), (3, 5)):
        L = _extract_logical(3, 7, u, c)
        check(_mat_close(L, _perm_target(u, (6 * c) % 7, 7)),
              f"(i) offset law fails at p=7 n=3 (u,c)=({u},{c})")
    check(True, "(i) offset law P_(u,c) -> P_(u, -(n-2)c) exact at "
                "p=3 n=2..5 (all 6) and p=7 n=2 (all 42), n=3 "
                "(generators + composite; all 42 by multiplicativity)")

    # ---- (ii) F1 as built at n = 4; NOT-F1 at n = 3; D_2 dressing ----
    for (u, c) in _affine_group(3):
        L = _extract_logical(4, 3, u, c)
        check(_mat_close(L, _perm_target(u, c, 3)),
              f"(ii) n=4 as-built F1 fails at (u,c)=({u},{c})")
    # negative control: n = 3 as built is NOT F1 at any c != 0
    L = _extract_logical(3, 3, 1, 1)
    check(not _mat_close(L, _perm_target(1, 1, 3)),
          "(ii) n=3 as-built must FAIL F1 (the audit's catch has teeth)")
    check(_mat_close(L, _perm_target(1, 2, 3)),
          "(ii) n=3 as-built logical must be P_(1, 2c) per the law")
    # the D_2 dressing restores F1 exactly (k = 2 at n = 3):
    for (u, c) in _affine_group(3):
        L = _extract_logical(3, 3, u, c)
        check(_mat_close(_conj_by_scaling(L, 2, 3), _perm_target(u, c, 3)),
              f"(ii) D_2-dressed n=3 F1 fails at (u,c)=({u},{c})")

    # ---- (iii) n = 7 as built (offset -(5) == 1 mod 3), generators ----
    for (u, c) in ((1, 1), (2, 0)):
        L = _extract_logical(7, 3, u, c)
        check(_mat_close(L, _perm_target(u, c, 3)),
              f"(iii) n=7 as-built F1 fails at generator ({u},{c})")
    check(True, "(iii) n=7 F1 exact on S_3 generators; all 6 by "
                "multiplicativity of both sides in the group element")

    # ---- (iv) q = 2 transversal F1 at ((3,3)) and ((5,5)) ----
    cw = _fiveq_codewords()
    ent = {(0, 0): 1 / math.sqrt(2), (1, 1): 1 / math.sqrt(2)}
    for n_sh_target, n_flips in ((3, 3), (5, 5)):
        st = _q33_encode(ent, 1, cw)
        if n_sh_target == 5:
            st = _q33_encode(st, 3, cw)
        # apply X to every share (positions 1..n)
        flipped = {}
        for tup, amp in st.items():
            new = tuple((1 - t) if 1 <= i <= n_flips else t
                        for i, t in enumerate(tup))
            flipped[new] = flipped.get(new, 0j) + amp
        dec = flipped
        if n_sh_target == 5:
            dec = _q33_decode(dec, 3, cw)
        dec = _q33_decode(dec, 1, cw)
        rho = _qss_marginal(dec, (0, 1))
        # target: (I x X)|Phi> = (|0,1> + |1,0>)/sqrt(2)
        tgt = {}
        for r1, s1 in ((0, 1), (1, 0)):
            for r2, s2 in ((0, 1), (1, 0)):
                tgt[((r1, s1), (r2, s2))] = 0.5
        keys = {k[0] for k in rho} | {k[0] for k in tgt}
        dev = max(abs(rho.get((k1, k2), 0j) - tgt.get((k1, k2), 0j))
                  for k1 in keys for k2 in keys)
        check(dev < _TOL,
              f"(iv) (({n_sh_target},{n_sh_target})) transversal X fails "
              f"(dev {dev:.2e})")

    # ---- (v) the dim-6 tensor: all 12 elements of S_2 x S_3, dense ----
    V2 = _qubit33_isometry()                     # 32 x 2  (8 shares, 4 env)
    V3 = _qutrit33_isometry()                    # 243 x 3 (27 shares, 9 env)
    D2 = np.array(_perm_target(2, 0, 3))         # the dressing
    V3d = V3 @ D2                                # D_2-dressed qutrit scheme
    X = np.array([[0, 1], [1, 0]], dtype=float)
    V2t = V2.reshape(2, 2, 2, 4, 2)              # (b1,b2,b3, e2; s)
    V3t = V3d.reshape(3, 3, 3, 9, 3)             # (t1,t2,t3, e3; s)
    for a in (0, 1):
        g2 = np.linalg.matrix_power(X, a)
        for (u, c) in _affine_group(3):
            g3 = np.array(_perm_target(u, c, 3))
            # F1 for each factor verified at CHANNEL strength (the env
            # rep is gauge): compare E(g rho g^dag) vs
            # g^{x3} E(rho) g^{dag x3} on all matrix units.
            def _chan_dev(Vt, g, d, de):
                Vm = Vt.reshape(d ** 3, de, d)
                worst = 0.0
                G3 = np.kron(np.kron(g, g), g)
                for s in range(d):
                    for t in range(d):
                        out = np.einsum('xe,ye->xy', Vm[:, :, s],
                                        np.conj(Vm[:, :, t]))
                        gin = g[:, s][:, None] * np.conj(g[:, t])[None, :]
                        out_g = np.zeros_like(out)
                        for ss in range(d):
                            for tt in range(d):
                                if abs(gin[ss, tt]) > 1e-15:
                                    out_g += gin[ss, tt] * np.einsum(
                                        'xe,ye->xy', Vm[:, :, ss],
                                        np.conj(Vm[:, :, tt]))
                        worst = max(worst, np.abs(
                            out_g - G3 @ out @ G3.conj().T).max())
                return worst
            d2v = _chan_dev(V2t, g2, 2, 4)
            d3v = _chan_dev(V3t, g3, 3, 9)
            check(d2v < 1e-10 and d3v < 1e-10,
                  f"(v) factor F1 fails at a={a},(u,c)=({u},{c}) "
                  f"(qubit {d2v:.1e}, qutrit {d3v:.1e})")
    check(True, "(v) F1 for all 12 elements of S_2 x S_3 on both factors "
                "at channel strength; the tensor is F1 for the product "
                "group (tensor of covariant channels, logical g2 x g3) -- "
                "the G_0 mechanism at dim 6")

    # ---- (vi) the n = 61 integer corollaries + the D_4 identity ----
    check((-(61 - 2)) % 3 == 1,
          "(vi) -(59) == 1 mod 3: the S_3 factor is F1 as built at n=61")
    check((-(61 - 2)) % 7 == 4,
          "(vi) -(59) == 4 mod 7: the 7-factor needs exactly D_4")
    for (u, c) in _affine_group(7):
        # D_4 P_(u,c) D_4^{-1} = P_(u, 4c), verified directly (the
        # conjugation helper computes D_m^{-1} L D_m, so pass m = 4^{-1}):
        lhs = _conj_by_scaling(_perm_target(u, c, 7), pow(4, -1, 7), 7)
        check(_mat_close(lhs, _perm_target(u, (4 * c) % 7, 7)),
              f"(vi) D_4 dressing identity fails at (u,c)=({u},{c})")

    # ---- (vii) the stored q = 3 full-S_3 F1 witness + twirl control ----
    V = _WITNESS_V
    group = _s3_group()
    e_iso = np.abs(V.conj().T @ V - np.eye(3)).max()
    check(e_iso < 1e-10, f"(vii) witness isometry defect {e_iso:.2e}")
    # F1 covariance at CHANNEL strength, W-free (the env rep is gauge;
    # F1 constrains the channel): E(P rho P^dag) = P^{x2} E(rho) P^{dag x2}
    # on all 9 matrix units, all 6 group elements (transpositions in).
    Vt = V.reshape(3, 3, 3, 3)                    # (i, j, e; r)

    def _chan(r_in):
        return np.einsum('ijer,rs,kles->ijkl', Vt, r_in, np.conj(Vt))

    e_cov = 0.0
    for img in group:
        P = _perm_np(img)
        P2 = np.kron(P, P)
        for a in range(3):
            for b in range(3):
                r = np.zeros((3, 3), dtype=complex)
                r[a, b] = 1
                lhs = _chan(P @ r @ P.T).reshape(9, 9)
                rhs = P2 @ _chan(r).reshape(9, 9) @ P2.T
                e_cov = max(e_cov, np.abs(lhs - rhs).max())
    check(e_cov < 1e-10,
          f"(vii) witness F1 covariance defect {e_cov:.2e} at channel "
          f"strength, all 6 elements of S_3 (transpositions included), "
          f"all 9 matrix units (W-free)")
    # secondary certificate: an environment rep exists -- solve W from
    # the intertwining and verify unitarity + the homomorphism property
    Ws = {}
    for img in group:
        P = _perm_np(img)
        # (P x P x W) V = V P  =>  solve W by least squares on the env leg
        A = np.einsum('Ii,Jj,ijer->IJer', P, P, Vt).reshape(9, 3, 3)
        Bt = np.einsum('IJer,rs->IJes', Vt, _perm_np(img)).reshape(9, 3, 3)
        # stack: A[:, e, :] W[e', e]?  W acts on env index: rows of A are
        # (shares; env_in), target Bt (shares; env_out):
        Amat = A.transpose(0, 2, 1).reshape(27, 3)   # (shares x r; env)
        Bmat = Bt.transpose(0, 2, 1).reshape(27, 3)
        W, res, rk, sv = np.linalg.lstsq(Amat, Bmat, rcond=None)
        W = W.T
        Ws[img] = W
        e_int = np.abs(Amat @ W.T - Bmat).max()
        e_uni = np.abs(W.conj().T @ W - np.eye(3)).max()
        check(e_int < 1e-8 and e_uni < 1e-8,
              f"(vii) env-rep certificate fails at {img} (intertwine "
              f"{e_int:.1e}, unitarity {e_uni:.1e})")
    # homomorphism spot-check on a generating pair
    g1, g2 = (1, 0, 2), (1, 2, 0)   # transposition, 3-cycle
    comp = tuple(g1[g2[r]] for r in range(3))
    e_hom = np.abs(Ws[g1] @ Ws[g2] - Ws[comp]).max()
    check(e_hom < 1e-8,
          f"(vii) env-rep homomorphism defect {e_hom:.1e}")
    # character test: chi(id) = 3, chi(transposition) = 1, chi(3-cycle) = 0
    # <=> W = triv (+) std (certifies the docstring's env-rep claim)
    chi = {img: np.trace(Ws[img]).real for img in group}
    for img in group:
        n_fix = sum(1 for r in range(3) if img[r] == r)
        want = {3: 3.0, 1: 1.0, 0: 0.0}[n_fix]
        check(abs(chi[img] - want) < 1e-8,
              f"(vii) env-rep character at {img}: {chi[img]:.4f} != {want}"
              f" -- not triv (+) std")
    e_priv = 0.0
    for s in range(3):
        for t in range(3):
            out = np.einsum('ije,kle->ijkl', Vt[..., s],
                            np.conj(Vt[..., t]))
            m1 = np.einsum('ijkj->ik', out)
            m2 = np.einsum('ijil->jl', out)
            tgt = np.eye(3) / 3 if s == t else np.zeros((3, 3))
            e_priv = max(e_priv, np.abs(m1 - tgt).max(),
                         np.abs(m2 - tgt).max())
    check(e_priv < 1e-10,
          f"(vii) witness single-share privacy (superoperator strength, "
          f"both shares) defect {e_priv:.2e}")
    psi = np.einsum('xr,rs->xs', V, np.eye(3) / math.sqrt(3)).reshape(
        3, 3, 3, 3)                               # (i, j, e; r)
    rho_RE = np.einsum('ijer,ijfs->erfs', psi, np.conj(psi)).reshape(9, 9)
    rho_R = np.einsum('ijer,ijes->rs', psi, np.conj(psi))
    rho_E = np.einsum('ijer,ijfr->ef', psi, np.conj(psi))
    e_dec = np.abs(rho_RE - np.kron(rho_E, rho_R)).max()
    check(e_dec < 1e-10,
          f"(vii) witness recovery (decoupling defect {e_dec:.2e})")
    sup = np.zeros((81, 9), dtype=complex)
    for s in range(3):
        for t in range(3):
            sup[:, 3 * s + t] = np.einsum(
                'ije,kle->ijkl', Vt[..., s], np.conj(Vt[..., t])).reshape(-1)
    rk = np.linalg.matrix_rank(sup, tol=1e-8)
    check(rk == 9, f"(vii) witness channel superoperator rank {rk} != 9")
    # AME(4,3): all six pair marginals of the purification are I/9
    psi4 = psi / np.linalg.norm(psi)                   # normalized 4-party
    legs = {'12': 'ijer,kler->ijkl', '1E': 'ijer,kjfr->iekf',
            '1R': 'ijer,kjes->irks', '2E': 'ijer,ilfr->jelf',
            '2R': 'ijer,iles->jrls', 'ER': 'ijer,ijfs->erfs'}
    e_ame = 0.0
    for name, spec in legs.items():
        m = np.einsum(spec, psi4, np.conj(psi4)).reshape(9, 9)
        e_ame = max(e_ame, np.abs(m - np.eye(9) / 9).max())
    check(e_ame < 1e-10,
          f"(vii) AME(4,3) pair-marginal defect {e_ame:.2e} (all six)")
    # twirl negative control: rank collapse + the dephasing identity
    p = 3
    V0 = np.zeros((p, p, p, p), dtype=complex)
    for s in range(p):
        for a in range(p):
            V0[a, (a + s) % p, (a + 2 * s) % p, s] = 1 / math.sqrt(p)

    def _E0(r):
        return np.einsum('abes,st,cdet->abcd', V0, r, np.conj(V0)
                         ).reshape(9, 9)

    aff = [(u, c) for u in (1, 2) for c in range(3)]

    def _Etw(r):
        out = np.zeros((9, 9), dtype=complex)
        for (u, c) in aff:
            g = np.array(_perm_target(u, c, 3))
            G = np.kron(g, g)
            out += G @ _E0(g.T @ r @ g) @ G.T
        return out / 6.0

    F = np.array([[np.exp(2j * np.pi * k * v / p) for v in range(p)]
                  for k in range(p)]) / math.sqrt(p)

    def _dephase(r):
        out = np.zeros_like(r, dtype=complex)
        for k in range(p):
            fk = np.conj(F[k])
            Q = np.outer(fk, np.conj(fk))
            out += Q @ r @ Q
        return out

    e_tw = 0.0
    cols_tw, cols_0 = [], []
    for s in range(p):
        for t in range(p):
            r = np.zeros((p, p), dtype=complex)
            r[s, t] = 1
            e_tw = max(e_tw, np.abs(_Etw(r) - _E0(_dephase(r))).max())
            cols_tw.append(_Etw(r).reshape(-1))
            cols_0.append(_E0(r).reshape(-1))
    check(e_tw < 1e-12,
          f"(vii) twirl dephasing identity E_tw = E_0 o D (defect "
          f"{e_tw:.2e})")
    r_tw = np.linalg.matrix_rank(np.column_stack(cols_tw), tol=1e-10)
    r_0 = np.linalg.matrix_rank(np.column_stack(cols_0), tol=1e-10)
    check(r_tw == 3 and r_0 == 9,
          f"(vii) twirl rank collapse 9 -> 3 (got {r_0} -> {r_tw}): the "
          f"negative control has teeth -- the covariant witness is not "
          f"a twirl")

    return _result(
        name='T_vacuum_scheme_product_affine_covariance -- the '
             'S_42-covariant fence split: the offset law '
             'P_(u,c) -> P_(u, -(n-2)c); G_0 = S_2 x S_3 x AGL(1,7) '
             'covariance of the banked exact-fill construction (F2 as '
             'built, F1 after the D_4 dressing; S_2/S_3 factors F1 as '
             'built at n = 61); full-S_q F1 witnesses at exact fill at '
             'q = 2 and q = 3 (stored AME(4,3) witness); the twirl '
             'negative control; full S_42 OPEN',
        tier=4,
        epistemic='P_structural_instrument',
        summary=(
            'The Paper 45 SS8 named open walked and banked at the '
            'split. The offset law is exact by Choi-strength logical '
            'extraction (p = 3 at n = 2..5, all of S_3; p = 7 at '
            'n = 2, 3): the affine mode map on all n shares induces '
            'P_(u, -(n-2)c). Corollaries at n = 61: the S_3 factor of '
            'the banked 2x3x7 scheme is F1-covariant AS BUILT '
            '(-(59) == 1 mod 3); the AGL(1,7) factor is F2 as built '
            'and F1 after the D_4 dressing (-(59) == 4 mod 7; the '
            'dressing identity exact over all 42 elements); with the '
            'q = 2 transversal-X factor, the construction carries '
            'G_0 = S_2 x S_3 x AGL(1,7) (order 504) covariance. THE '
            'DICHOTOMY KILLER: full-S_q, mode-typed (F1) covariant '
            'perfect mixed schemes at share dimension exactly q exist '
            'at q = 2 (the banked qubit ladder) and q = 3 (a stored '
            'explicit witness, environment rep triv + std, verified '
            'here at <= 1e-10: isometry, all-6 covariance, '
            'superoperator privacy, decoupling recovery, rank 9, '
            'genuine AME(4,3)) -- covariance does NOT force '
            'classicality at exact fill anywhere computable. The '
            'twirl route is pinned as the negative control (rank '
            '9 -> 3, E_tw = E_0 o Fourier-dephasing, residue exactly '
            'classical). Full S_42 at (61, 42) stays OPEN, both '
            'formulations; the F1-vs-F2 demand selection is a '
            'principal-shaped reading; all vacuum_label_code fences '
            'inherited.'
        ),
        key_result=(
            'Covariance does not kill coherence at exact fill: full-S_q '
            'F1 witnesses at q = 2, 3; the banked scheme is '
            'G_0-covariant (|G_0| = 504; F2 as built, F1 after D_4); '
            'offset law exact; full S_42 open'
        ),
        dependencies=['T_vacuum_sector_aligned_scheme_share_dim_42',
                      'T_vacuum_mixed_42dim_secret_scheme_exists',
                      'L_count', 'T_interface_sector_bridge',
                      'T_horizon_reciprocity', 'L_QEC_code_space'],
        cross_refs=['T_vacuum_label_code_no_leakage',
                    'T_vacuum_logical_sector_classical_ceiling',
                    'T_banked_registration_coherent_recovery_no_go',
                    'T_which_v_no_registered_interior_reader',
                    'T_vglobal_offdiagonal_blocks_scalar_typed'],
        artifacts={
            'offset_law': 'P_(u,c)^{xn} -> logical P_(u, -(n-2)c mod p); '
                          'exact at p=3 n=2..5, p=7 n=2,3',
            'n61_corollaries': '-(59) == 1 (mod 3), == 4 (mod 7); S_3 '
                               'factor F1 as built; 7-factor F1 after '
                               'D_4',
            'G0': 'S_2 x S_3 x AGL(1,7), order 504; F2 as built, F1 '
                  'dressed',
            'f1_witnesses': 'q=2 ((3,3)),((5,5)) transversal X; q=3 '
                            '((2,2)) stored witness (AME(4,3), env '
                            'triv+std), battery <= 1e-10',
            'twirl_control': 'rank 9 -> 3; E_tw = E_0 o Fourier-'
                             'dephasing; residue classical',
            'full_S42': 'OPEN, both formulations (never cite as closed)',
            'note': 'Reference - The S42-Covariant Sector-Aligned '
                    'Scheme Walked (2026-07-03)',
        },
    )


_CHECKS = {
    'T_vacuum_scheme_product_affine_covariance':
        check_T_vacuum_scheme_product_affine_covariance,
}


def register(registry):
    """Register the vacuum scheme covariance check into the bank."""
    registry.update(_CHECKS)


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == '__main__':
    for _n, _r in run_all().items():
        print(('PASS' if _r.get('passed', True) else 'FAIL'), _n)


# ---------------------------------------------------------------------------
# Interface Engine onboarding (Full Bank Onboarding wave, 2026-07-04)
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "quantum:vacuum_scheme_covariance_split",
        "axis": "ROUTE",
        "expect_export": False,
        "claim_text": (
            "The S_42-covariant fence is SPLIT [P_structural_instrument]: "
            "the hoped-for dichotomy ('covariance kills coherent schemes at "
            "exact fill => classicality forced by symmetry where dimension "
            "failed') is REFUTED at every computable small case, and the "
            "banked 2x3x7 construction itself carries product-affine "
            "subgroup covariance G_0 = S_2 x S_3 x AGL(1,7). Full S_42 at "
            "(n, q) = (61, 42) stays OPEN in BOTH formulations -- F1 "
            "(mode-typed) and F2 (some-rep), never conflated; selecting F1 "
            "vs F2 as the physically mandated demand is a principal-shaped "
            "reading, not certified. "
            "(check_T_vacuum_scheme_product_affine_covariance, "
            "vacuum_scheme_covariance.py)"
        ),
        "note": (
            "Onboards the .373 covariance split onto the ROUTE axis as a "
            "held claim at [P_structural_instrument]. The F1/F2 "
            "never-conflate discipline and the open full-S_42 status are "
            "frozen in the claim text."
        ),
    },
)
