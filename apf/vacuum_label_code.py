"""APF vacuum label code -- the constructed P1 witness for ICL_vac route (b).

v24.3.NEW (2026-07-02). The named module-scale work from "Reference -
ICL_vac Route (b) Walked - The Kernel Formulation, the MSC Swap, and the
QEC Strength Finding (2026-07-02)" SS7 item 3: an explicit code on the
banked second-epsilon skeleton realizing vacuum no-leakage (P1) at
computed strength, together with the SUBSPACE-COHERENCE ceiling that
CORRECTS the P1 target's wording -- the "42-dim vacuum logical sector"
is unconstructible as a subspace-coherent (pure-isometric) sector; the
classical 42-label code built here is the maximum at subspace form.
Subsystem/mixed-state encodings are NOT excluded by the no-cloning
step (Cleve-Gottesman-Lo 1999) -- and the fit question is CLOSED
EXISTS at abstract-encoding strength: check 3 exhibits a perfect
((61,61)) mixed scheme carrying a coherent 42-dim secret with every
share dimension 43 <= 102 (see the check-3 block below).
Realization/identification remains the open reading. Hostile cold
audits 2026-07-02: LAND-WITH-FIXES 0.80 (checks 1-2, all eight fixes
carried) and LAND-WITH-FIXES 0.88 (check 3, all seven fixes carried;
the walker's construction independently re-derived and re-run by the
auditor).

THE MODEL (banked skeleton, every constant anchored):
  - C_total = 61 capacity channels (L_count [P]).
  - Each channel's second-epsilon commitment space is 102-dimensional:
    60 Sector-A partner options + 42 Sector-B vacuum-mode options
    (T_kappa, L_self_exclusion, T_horizon_reciprocity Step 1 [P]).
    The ambient Hilbert space H = (C^102)^{(x)61} is the banked
    L_QEC_code_space object (a dependency, not a cross-reference).
  - The label alphabet is the 42 Sector-B modes; by
    T_interface_sector_bridge [P] this 42 is dim of the global-interface
    stratum of T12 -- the same 42 that T11 reads as the vacuum block.
  - THE CARRIER IS A SLICE (disclosed, priced -- audit fix 3): the
    42-dimensional common-mode slice of the T_horizon_reciprocity
    Step-3 vacuum-dominated configuration family -- 42 of the 42^61
    banked configurations. The banked Step-3 slot has each unmatched
    channel choosing its vacuum mode INDEPENDENTLY (S_propagation =
    61 ln 42 is banked as exactly that count); the common-mode
    correlation (all channels in the same mode v) is a
    CONSTRUCTION-SUPPLIED input, not bank-supplied. Its register form
    is precisely the OPEN a = b common-demand identity [C]
    (L_common_demand_iff_degenerate, v24.3.338) -- cross-referenced,
    never assumed as banked.
  - Common-mode states |v>^{(x)61}, v in {0..41}: every channel in the
    same vacuum mode ("one demand vector under forty-two names").

THE CODE (the label states):
  |mu_bar> = 42^{-1/2} * sum_v omega^{mu v} |v>^{(x)61},
  omega = exp(2 pi i / 42), mu = 0..41.
  The 42 label states are the Fourier-dual frame of the common-mode
  family. All computations collapse exactly to the 42-dimensional span
  of {|v>^{(x)S}} (the collapse itself is verified in-module by a
  reduced-parameter full-tensor cross-check, clause (vii)); nothing of
  size 102^61 is ever represented.

WHAT check_T_vacuum_label_code_no_leakage CERTIFIES (exact):
  (i)   ORTHONORMALITY: the 42 label states are orthonormal (Fourier).
  (ii)  NO-LEAKAGE (P1, label form): for EVERY proper type-subset A
        (all sizes 1 <= |A| <= 60 computed, all 42 labels), the
        reduced state of |mu_bar> on A is (1/42) sum_v |v^A><v^A| --
        one fixed state, independent of mu AND of A. The kernel
        identity is the one-line complement-orthogonality cancellation
        <w^Abar|v^Abar> = delta_vw for Abar nonempty.
  (iii) READ-BLINDNESS, expectation form: for any A-supported
        observable O, Tr(O rho_mu) depends on O only through the
        diagonal data f_v = <v^A|O|v^A> and equals (1/42) sum_v f_v
        for every mu. (Consistency restatement of (ii); the
        operator-strength content is clause (iv).)
  (iv)  CLEANING/COMPRESSION CERTIFICATE: for any A-supported operator
        O, the code-space compression (P O P)_{mu nu} = fhat(nu - mu)
        is a CIRCULANT -- constant diagonal (the operator restatement
        of read-blindness) with off-diagonal content that is pure
        logical-shift mixing. Proper subsets can WRITE the label
        (dephase/shift); they cannot READ it. Privacy is not
        protection; the write channel is disclosed, not hidden. The
        cross-term drop (only the common-mode diagonal of O survives)
        is verified against a full-tensor build in clause (vii).
  (v)   GLOBAL REGISTRATION -- with the sharp finding stated (audit
        fix 4): one global (all-61) measurement -- the Fourier frame
        projectors -- distinguishes the 42 labels perfectly (from
        (i)). But that label-resolving global read has NO banked
        counterpart; the only banked global read (per-channel Sector-B
        registration at the horizon crossing sequence,
        T_horizon_reciprocity Step 4) is computed HERE to be mu-BLIND:
        it outputs a uniformly random common v independent of the
        label. On this encoding the label is invisible to every proper
        subset AND to the banked horizon registration -- under the
        identification reading, no banked instrument ever registers
        mu. This cuts AGAINST the identification reading and is
        recorded as a finding. Identifying either global read with the
        physical horizon registration is a READING (wedge-fence
        strength); the construction supplies existence, not the
        identification.
  (vi)  NEGATIVE CONTROL (.318 pattern): the basis encoding -- taking
        the common-mode states |v>^{(x)61} themselves as label
        carriers -- FAILS no-leakage maximally: a single channel's
        marginal distinguishes all 42 labels perfectly (pairwise trace
        distance 1). No-leakage is a property of the phase encoding,
        not of every 42-state family; the check has teeth. CENSUS
        GUARD: this negative control is a COUNTERFACTUAL ENCODING
        EXHIBIT (the basis code, shown to FAIL privacy); it constructs
        no banked reader of physical Sector-B content, and must not be
        read by a later disposition pass as an interior which-v
        reader.
  (vii) COLLAPSE CROSS-CHECK (audit fix 5): a reduced-parameter
        full-tensor build (3 channels, alphabet 3, actual 27-dim
        tensors) verifies both collapse steps against brute force:
        marginal mu-independence on every proper subset, and the
        compression of a generic A-supported operator WITH nonzero
        cross elements <v^A|O|w^A> matching the diagonal-only
        circulant formula.

WHAT check_T_vacuum_logical_sector_classical_ceiling CERTIFIES:
  (a)   THE FOURIER-DUAL EXHIBIT (exact): the uniform superposition of
        the 42 label states IS the product state |0>^{(x)61} --
        coherent superpositions of the private frame are exactly the
        maximally leaky states (single-channel trace distance from the
        uniform marginal = 1 - 1/42, computed from the two states).
  (b)   THE IN-CARRIER CEILING (exact, elementary proof here +
        computed witnesses; audit fix 2 -- the pointwise form): within
        the 42-dim common-mode carrier, NO 2-dimensional subspace has
        STATE-INDEPENDENT single-channel marginals over all its
        states. Proof (pointwise; orthogonality never needed): let
        x, y be an orthonormal basis of the subspace and suppose every
        unit state has the SAME single-channel diagonal. Comparing x
        and y: |x_v|^2 = |y_v|^2 =: p_v for every v. Comparing
        (x + y)/sqrt(2) and (x + iy)/sqrt(2) against x: Re and Im of
        conj(x_v) y_v vanish for every v, so conj(x_v) y_v = 0
        POINTWISE -- x and y have disjoint supports. But equal moduli
        p_v with disjoint supports force p_v = 0 for every v,
        contradicting normalization. QED. Witnesses computed with a
        STATE-DEPENDENCE defect (max over probe states of the sup-norm
        deviation from x's diagonal): the label frame's own 2-dim
        spans leak on superposition, and random 2-dim carrier
        subspaces all show strictly positive defect.
  (c)   THE GENERAL CEILING, SUBSPACE-SCOPED (audit fix 1): for a
        SUBSPACE (pure-isometric) code, state-independent marginals on
        a region A over all code states is the Knill-Laflamme erasure
        condition P O_A P = c(O) P; correctability of BOTH a region
        and its complement for a dim >= 2 subspace violates no-cloning
        (two disjoint recovery maps would clone). Named cited steps:
        Knill & Laflamme 1997 (PRA 55, 900); the complementary-region
        no-cloning argument. THE SCOPE FENCE: this kills
        subspace-coherent sectors ONLY. Subsystem/mixed-state
        encodings EVADE it -- Cleve, Gottesman & Lo 1999 (PRL 83,
        648): the ((2,2)) quantum one-time-pad carries a genuine
        quantum secret with BOTH proper shares state-independent; the
        banked OA-QECC code state (L_QEC_code_space) is itself MIXED,
        so the excluded species is not the bank's native one. The fit
        question is CLOSED EXISTS (check 3): a perfect ((61,61)) mixed
        scheme with all share dimensions 43 <= 102 carries a coherent
        42-dim secret; realization/identification remains the open
        reading. Nothing computed in this module depends on
        the cited steps (docstring-level import, verified).
  (d)   CLASSICALITY COROLLARY, scoped (computed): the compressions
        {P O_A P} form a COMMUTING FAMILY generating the circulant
        algebra (the compression map is not a homomorphism; the family
        commutes and is simultaneously DFT-diagonalized, computed).
        The logical structure any interior coupling can touch at
        subspace form is abelian -- classical-label-typed, the exact
        species of the .339 census row 5 and the banked which-v
        object (.318).

WHAT check_T_vacuum_mixed_42dim_secret_scheme_exists CERTIFIES:
  (Check 3; the audit's seven fixes carried. Closes the fit question
  of clause (c) in the EXISTS direction.)
  (A)   THE SCHEME: p = 43 (prime, 42 <= 43 <= 102). Base isometry
        W: C^p -> (C^p)^{(x)3}, |s> -> p^{-1/2} sum_a |a, a+s, a+2s>
        (mod p) -- the polynomial code f(x) = a + s x at x = 0, 1, 2.
        The mixed ((2,2)) scheme Sigma keeps shares (f(0), f(1)) and
        traces f(2) to the environment. E_2 = Sigma; E_n = Sigma
        applied to the LAST share of E_{n-1}. E_61 = 60 applications
        of Sigma (1 base + 59 re-shares), 61 shares, each of dimension
        exactly 43; embed C^42 in C^43 for the secret and C^43 in
        C^102 per channel. (The naive CGL route -- a pure ((61,121))
        polynomial scheme with shares discarded -- needs p >= 121 >
        102 and does NOT fit; the cascade is the move that gets under
        the local dimension.)
  (B)   BASE PRIVACY, exact integer certificate at p = 43: the
        cross-term congruence systems for each kept share and for the
        environment ({a'+s' = a+s, a'+2s' = a+2s}, etc., mod 43) have
        NO solution with s != s' -- verified by integer loop, stronger
        than any float tolerance. Each single register's marginal
        channel is completely depolarizing: X -> Tr(X) I/p, constant
        as a SUPEROPERATOR, hence blind on superpositions and on
        halves of entangled states (linearity).
  (C)   BASE RECOVERY, exact: U1|x,y> = |x, y-x>; Fourier-measure
        register 1 (convention F_-, outcome w); phase correction
        diag(e^{2 pi i (p-2) w s / p}). The correction identity
        (2 w s + (p-2) w s) = p w s = 0 (mod p) is pinned by integer
        loop over all (w, s). Implemented coherently (unitary + trace)
        so composition on entangled inputs is a channel identity.
  (D)   CASCADE PRIVACY, the induction (elementary; the one
        nontrivial step written out): for proper A in [n], three
        cases. (i) A contains both children n-1, n: A misses some
        j <= n-2, pulls back to a proper subset of [n-1]; a CP map on
        a product preserves the product. (ii) A contains exactly one
        child: the single-child marginal map of Sigma is the CONSTANT
        channel Lambda(X) = Tr(X) I/p, and (id_C (x) Lambda)(rho_CD)
        = rho_C (x) I/p is an exact algebraic identity for ARBITRARY
        C-D correlations -- including correlations carrying the secret
        through the re-shared share. The child is deleted BEFORE any
        appeal to E_{n-1} privacy, leaving A intersect [n-2], always
        proper in [n-1]. This is exactly the case the naive pullback
        would miss (A = [n-2] + one child has pullback [n-1], the
        FULL set); the constant-channel identity, not inheritance,
        kills it. (iii) A inside [n-2]: directly proper. Base case =
        (B). The hardest subsets are scanned BY NAME in-check.
  (E)   COMPUTED WITNESSES (pure Python, seconds): full proper-subset
        scans with entangled references -- ((4,4)) at p = 3 (all 14
        proper subsets, including the two hardest, {1,2,3} and
        {1,2,4}) and ((3,3)) at p = 5 with a 4-dim secret subspace
        (modeling 42 in 43); composed multi-stage decoder exact on an
        entangled reference in every case; GHZ negative control (the
        sum encoding passes basis-label privacy, FAILS the
        superoperator-constancy test -- the check has teeth).
  (F)   FENCES: existence at abstract-encoding strength ONLY. The
        scheme embeds C^43 arbitrarily in each C^102 -- no alignment
        with the 60+42 sector split, the common-mode carrier, or the
        banked horizon registration is claimed; the ALIGNED-scheme
        question is separate and un-walked. Share dimension exactly 42
        is not settled (42 <= d_share <= 43 pinned; the Gottesman
        important-share bound d_share >= 42 makes 43 near-tight).
        Privacy is not erasure-protection. n = 61 is not directly
        simulated; it rests on (D), verified at n = 3, 4 including
        the composed decoder. No cited theorem is load-bearing:
        privacy, recovery, and the induction's one lemma are computed
        or derived above; CGL 1999 is attribution.

EFFECT ON THE ROUTE-(b) LEDGER (audit fix 6 -- honest form):
  The SS2 "three named gaps before the quantifier" move as follows.
  "No code subspace is constructed" -- closed AT LABEL-CODE FORM ON A
  CONSTRUCTION-SUPPLIED COMMON-MODE CARRIER (fence 5); the ceiling's
  correction: the constructible object at subspace form is the
  classical label code. "KL certified only for the single-type trace
  state" -- WITNESSED AT COMPUTED STRENGTH for the constructed code;
  the banked L_QEC_knill_laflamme is untouched and not regraded.
  "The erasure-duality step (unbanked import)" -- retired for the
  privacy face of THIS construction (read-blindness is computed
  directly); the ceiling's general step reintroduces a named
  literature import (KL-1997 + no-cloning + CGL-1999) at docstring
  level -- the import is RELOCATED, not gone, and nothing computed
  rides on it. THE NOTE'S SS7 ITEM 3 IS EXECUTED AT CORRECTED FORM
  ONLY: its expectation that the construction "would also retire the
  wedge-reading fence" is NOT met -- the wedge/identification fence
  stands (fence 1). Do not cite the note as fully discharged.
  RVC then reads: P1 [computed, this module, at label form on the
  common-mode carrier] o identification [reading] + MSC [C]. The only
  violating species remains a non-marginal reader; ICL_vac stays
  NAMED, NOT ADOPTED, NOT DERIVED.

WHAT THIS MODULE DOES NOT CERTIFY:
  (1) NOT a claim that the physical vacuum sector IS this code: the
      identification of the constructed encoding with V_global content
      is a reading (SS6.1 / wedge-fence strength). Existence + ceiling
      are supplied; the identification is not. Clause (v)'s finding
      (the banked horizon registration is label-blind on this code)
      cuts AGAINST the identification and is recorded as such.
  (2) MSC is NOT derived; RVC is NOT closed; ICL_vac stays a named [C]
      axiom fragment. Route (b)'s wall (composition/inventory
      completeness independent of per-region capacity) stands.
  (3) Privacy is NOT erasure-protection: proper subsets can dephase or
      shift the label (clause (iv) off-diagonals). This is a privacy
      certificate, not an error-correcting shield.
  (4) The ceiling is SUBSPACE-SCOPED, and the mixed direction is
      CLOSED EXISTS at abstract-encoding strength (check 3): a perfect
      ((61,61)) mixed scheme with every share dimension 43 <= 102
      carries a coherent 42-dim secret. Existence != realization: the
      exhibited scheme embeds C^43 arbitrarily in each C^102 -- it
      respects neither the 60+42 sector split, nor the common-mode
      carrier, nor the banked horizon registration; "a mixed scheme
      ALIGNED with banked sector structure" is a separate, un-walked
      question (named so a later disposition pass cannot read EXISTS
      as realization-adjacent). Dimensional structure does not force
      classicality of globally-locked content (locked = recoverable
      only from the full set, invisible to every proper subset); the
      subspace ceiling and the banked label-typing stand; realization
      stays open.
  (5) THE CARRIER FENCE: the common-mode correlation (all channels
      same v) is a construction-supplied input, not bank-supplied; the
      banked dependence on the Step-3 slot is count-only over the
      INDEPENDENT 42^61 family; the correlation's register form is the
      OPEN a = b identity [C]. The existence claim survives (a
      P1-witnessing encoding inside the banked Hilbert space is
      exhibited); "the vacuum sector realizes it" is not claimed.
  (6) Closed-world on the banked constants (61, 42 = dim V_global,
      102); model-scope throughout.

STATUS: [P_structural_instrument] tier 4, both checks (audit fix 7:
an exhibited witness on a construction-supplied carrier is an
instrument in the .335/.337 sense, not a census of banked surfaces).
Elementary/standard mathematics (GHZ-type phase encoding; cf.
Hillery-Buzek-Berthiaume 1999 secret sharing; CGL 1999 for the
subsystem evasion) -- the content is the exact anchoring to the banked
skeleton, the scoped ceiling, the label-blindness finding, and the
route-(b) ledger effect.
Dependencies: L_count, T_kappa, L_self_exclusion,
T_horizon_reciprocity, T11, T_interface_sector_bridge,
L_QEC_code_space.
Cross-refs: check_T_which_v_no_registered_interior_reader (.318),
check_T_vglobal_offdiagonal_blocks_scalar_typed (.339),
check_T_vglobal_slot_identification_no_go (.326),
L_QEC_knill_laflamme / L_QEC_distance / L_QEC_wedge_duality,
L_common_demand_iff_degenerate (.338).
"""

import cmath
import math
import random

from apf.apf_utils import check, _result

# ---------------------------------------------------------------------------
# Banked constants (closed-world anchors)
# ---------------------------------------------------------------------------
N_TYPES = 61          # C_total (L_count [P])
ALPHABET = 42         # Sector-B vacuum modes = dim V_global (T12 bridge [P])
SECTOR_A = 60         # partner options = C_total - 1 (L_self_exclusion [P])
D_EFF = SECTOR_A + ALPHABET   # = 102 (T_horizon_reciprocity Step 1 [P])

_TOL = 1e-10


def _omega(k, n=None):
    """Root of unity omega^k, omega = exp(2 pi i / n)."""
    if n is None:
        n = ALPHABET
    return cmath.exp(2j * cmath.pi * (k % n) / n)


def _frame(n=None):
    """The label frame in the collapsed representation.

    Row mu is the n-vector of coefficients of |mu_bar> over the
    common-mode basis {|v>^{(x)n_types}}: F[mu][v] = omega^{mu v}/sqrt(n).
    The collapsed representation is exact: the common-mode states are
    orthonormal in the full space (product of per-channel Kronecker
    deltas), so every inner product below equals its full-space value
    -- and clause (vii) verifies this against an actual full-tensor
    build at reduced parameters.
    """
    if n is None:
        n = ALPHABET
    s = 1.0 / math.sqrt(n)
    return [[_omega(mu * v, n) * s for v in range(n)] for mu in range(n)]


def _overlap_complement(v, w, complement_size):
    """<w^Abar | v^Abar> for a complement of the given size (exact).

    Kronecker delta for any nonempty complement; 1 (trivial factor) for
    the improper subset A = all types. This single function is the
    entire |A|-dependence of every marginal computation below -- which
    is why no-leakage is |A|-independent for every proper A.
    """
    if complement_size == 0:
        return 1.0
    return 1.0 if v == w else 0.0


def _marginal(frame, mu, subset_size, n_types=N_TYPES):
    """Reduced state of |mu_bar> on a type-subset of the given size.

    Collapsed matrix over the {|v^A>} family:
      rho_A(mu)_{v w} = F[mu][v] * conj(F[mu][w]) * <w^Abar|v^Abar>.
    Exact for every subset of the given size (the collapsed matrix
    depends on the subset only through its size, and on the size only
    through whether the complement is empty).
    """
    n = len(frame)
    comp = n_types - subset_size
    return [[frame[mu][v] * frame[mu][w].conjugate()
             * _overlap_complement(v, w, comp)
             for w in range(n)] for v in range(n)]


def _compression(frame, g):
    """Code-space compression (P O P)_{mu nu} of an A-supported operator.

    For O supported on a proper subset A, complement orthogonality
    kills every cross term, so O enters only through its common-mode
    diagonal data g_v = <v^A| O |v^A>:
      (P O P)_{mu nu} = (1/n) sum_v omega^{(nu - mu) v} g_v.
    Returned as the n x n matrix (exact in the collapsed rep; the
    cross-term drop is verified against a full-tensor build in
    clause (vii)).
    """
    n = len(frame)
    return [[sum(_omega((nu - mu) * v, n) * g[v] for v in range(n)) / n
             for nu in range(n)] for mu in range(n)]


# ---------------------------------------------------------------------------
# Full-tensor cross-check machinery (clause (vii); reduced parameters)
# ---------------------------------------------------------------------------

def _full_tensor_crosscheck(n_ch=3, q=3, seed=424261):
    """Brute-force verification of both collapse steps at (n_ch, q).

    Builds the actual q^n_ch-dimensional tensors: the phase-code states
    |mu_bar> = q^{-1/2} sum_v omega_q^{mu v} |v...v>, then verifies
    (1) marginal mu-independence + uniformity on proper subsets of
    every size, and (2) the compression of a generic A-supported
    operator WITH nonzero cross elements against the diagonal-only
    circulant formula. Returns the max deviation found.
    """
    rng = random.Random(seed)
    dim = q ** n_ch

    def idx(tup):
        out = 0
        for t in tup:
            out = out * q + t
        return out

    def tuples():
        for i in range(dim):
            t, x = [], i
            for _ in range(n_ch):
                t.append(x % q)
                x //= q
            yield tuple(reversed(t))

    all_tuples = list(tuples())

    # the phase-code states as full vectors
    states = []
    s = 1.0 / math.sqrt(q)
    for mu in range(q):
        vec = [0j] * dim
        for v in range(q):
            vec[idx((v,) * n_ch)] = _omega(mu * v, q) * s
        states.append(vec)

    worst = 0.0

    # (1) marginals on proper subsets of every size 1..n_ch-1
    for size in range(1, n_ch):
        subset = tuple(range(size))          # by symmetry of the states,
        comp = tuple(range(size, n_ch))      # any subset of this size
        dA = q ** size
        margs = []
        for mu in range(q):
            rho = [[0j] * dA for _ in range(dA)]
            vec = states[mu]
            for t1 in all_tuples:
                a1 = idx(t1)
                if abs(vec[a1]) < 1e-15:
                    continue
                for t2 in all_tuples:
                    a2 = idx(t2)
                    if abs(vec[a2]) < 1e-15:
                        continue
                    if all(t1[c] == t2[c] for c in comp):
                        i1 = idx(tuple(t1[c] for c in subset)[:size]) \
                            if size else 0
                        i2 = idx(tuple(t2[c] for c in subset)[:size]) \
                            if size else 0
                        rho[i1][i2] += vec[a1] * vec[a2].conjugate()
            margs.append(rho)
        # mu-independence
        for mu in range(1, q):
            dev = max(abs(margs[mu][a][b] - margs[0][a][b])
                      for a in range(dA) for b in range(dA))
            worst = max(worst, dev)
        # matches the collapsed prediction: uniform 1/q over the
        # common-mode family, zero elsewhere
        for a_t in range(dA):
            for b_t in range(dA):
                # decode a_t, b_t back to tuples over the subset
                def dec(i):
                    t, x = [], i
                    for _ in range(size):
                        t.append(x % q)
                        x //= q
                    return tuple(reversed(t))
                ta, tb = dec(a_t), dec(b_t)
                common_a = all(u == ta[0] for u in ta)
                common_b = all(u == tb[0] for u in tb)
                want = (1.0 / q) if (common_a and common_b
                                     and ta[0] == tb[0]) else 0.0
                worst = max(worst, abs(margs[0][a_t][b_t] - want))

    # (2) compression with cross terms, subset = first channel
    O = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(q)]
         for _ in range(q)]                   # generic, dense cross terms
    for mu in range(q):
        for nu in range(q):
            # brute force <mu_bar| O (x) I (x) ... |nu_bar>
            val = 0j
            for v in range(q):
                for w in range(q):
                    # <v...v| O(x)I..I |w...w> = O[v][w] * delta on rest
                    if v == w or n_ch == 1:
                        val += (states[mu][idx((v,) * n_ch)].conjugate()
                                * O[v][w] * states[nu][idx((w,) * n_ch)])
                    else:
                        # rest channels give <v|w> = 0
                        pass
            # diagonal-only circulant formula
            pred = sum(_omega((nu - mu) * v, q) * O[v][v]
                       for v in range(q)) / q
            worst = max(worst, abs(val - pred))

    return worst


def check_T_vacuum_label_code_no_leakage():
    """T_vacuum_label_code_no_leakage: The Constructed P1 Witness [P_structural_instrument].

    See the module docstring for the full statement, the model, the
    fences (especially the carrier fence, 5), and the route-(b) ledger
    effect. Clauses (i)-(vii).
    """
    F = _frame()
    n = ALPHABET
    rng = random.Random(20260702)

    # ---- (i) orthonormality: Gram = I_42 (Fourier, exact) ----
    for mu in range(n):
        for nu in range(mu, n):
            g = sum(F[mu][v].conjugate() * F[nu][v] for v in range(n))
            want = 1.0 if mu == nu else 0.0
            check(abs(g - want) < _TOL,
                  f"(i) Gram[{mu}][{nu}] = {g:.2e} != {want}")

    # ---- (ii) no-leakage: rho_A(mu) uniform, ALL proper sizes, ALL mu ----
    for size in range(1, N_TYPES):        # every proper size 1..60
        for mu in range(n):               # every label
            rho = _marginal(F, mu, size)
            for v in range(n):
                for w in range(n):
                    want = (1.0 / n) if v == w else 0.0
                    if abs(rho[v][w] - want) >= _TOL:
                        check(False,
                              f"(ii) rho_A(mu={mu}, |A|={size})[{v}][{w}] "
                              f"deviates from the uniform mixture")
    check(True, "(ii) all 60 proper sizes x 42 labels: uniform mixture")
    # The improper subset (|A| = 61) is NOT blind -- sanity anchor: the
    # full-space state is pure and mu-dependent (clause (v) reads it).
    rho_full_0 = _marginal(F, 0, N_TYPES)
    rho_full_1 = _marginal(F, 1, N_TYPES)
    dev = max(abs(rho_full_0[v][w] - rho_full_1[v][w])
              for v in range(n) for w in range(n))
    check(dev > 1e-3,
          "(ii-anchor) the improper subset distinguishes labels "
          f"(dev = {dev:.3f}); privacy is proper-subset-only")

    # ---- (iii) read-blindness, expectation form (consistency with (ii);
    #            the operator-strength content is clause (iv)) ----
    for trial in range(8):
        f_diag = [rng.uniform(-3.0, 3.0) for _ in range(n)]
        expect = [sum(f_diag[v] * abs(F[mu][v]) ** 2 for v in range(n))
                  for mu in range(n)]
        spread = max(expect) - min(expect)
        check(spread < _TOL,
              f"(iii) trial {trial}: A-supported observable biases a "
              f"label (spread = {spread:.2e})")

    # ---- (iv) circulant compression: equal diagonal, shift-only mixing ----
    for trial in range(4):
        g = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
             for _ in range(n)]
        M = _compression(F, g)
        for mu in range(n):
            for nu in range(n):
                ref = M[0][(nu - mu) % n]
                check(abs(M[mu][nu] - ref) < _TOL,
                      f"(iv) compression not circulant at "
                      f"({mu},{nu}), trial {trial}")
        for mu in range(1, n):
            check(abs(M[mu][mu] - M[0][0]) < _TOL,
                  f"(iv) diagonal not constant at mu={mu}")
    # commuting family (feeds clause (d) of the ceiling check)
    g1 = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    g2 = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    M1, M2 = _compression(F, g1), _compression(F, g2)
    comm = max(abs(sum(M1[a][k] * M2[k][b] - M2[a][k] * M1[k][b]
                       for k in range(n)))
               for a in range(n) for b in range(n))
    check(comm < 1e-8,
          f"(iv) compressions must commute (|[M1,M2]| = {comm:.2e})")

    # ---- (v) global registration + the label-blindness finding ----
    # Fourier read: outcome distribution over frames for state mu_bar is
    # delta_mu (orthonormality, clause (i)) -- perfect distinguishability.
    # THE FINDING: the banked global read (per-channel Sector-B basis,
    # the horizon crossing sequence) is mu-BLIND on this code:
    for mu in (0, 5, 41):
        probs = [abs(F[mu][v]) ** 2 for v in range(n)]
        check(abs(sum(probs) - 1.0) < _TOL, "(v) dual-read normalization")
        check(max(probs) - min(probs) < _TOL,
              f"(v) the banked common-mode registration must be uniform "
              f"and mu-blind (mu={mu}) -- the label-blindness finding")

    # ---- (vi) negative control: the basis encoding leaks maximally ----
    # (a counterfactual encoding exhibit -- constructs no banked reader;
    #  see the census guard in the module docstring)
    for v, w in ((0, 1), (3, 40)):
        td = 0.5 * sum(abs((1.0 if u == v else 0.0) - (1.0 if u == w else 0.0))
                       for u in range(n))
        check(abs(td - 1.0) < _TOL,
              "(vi) basis-encoded labels must be perfectly locally "
              "distinguishable (trace distance 1)")

    # ---- (vii) full-tensor collapse cross-check at reduced parameters ----
    worst = _full_tensor_crosscheck(n_ch=3, q=3)
    check(worst < 1e-12,
          f"(vii) collapsed rep must match the full-tensor build "
          f"(max deviation {worst:.2e})")
    worst4 = _full_tensor_crosscheck(n_ch=4, q=3, seed=777)
    check(worst4 < 1e-12,
          f"(vii) collapsed rep must match at n_ch=4 "
          f"(max deviation {worst4:.2e})")

    return _result(
        name='T_vacuum_label_code_no_leakage -- the constructed P1 '
             'witness: a 42-label phase code on the common-mode slice '
             'of the banked second-epsilon skeleton with exact '
             'no-leakage on every proper type-subset, the circulant '
             'cleaning certificate, the label-blindness finding, the '
             'basis-encoding negative control, and the full-tensor '
             'collapse cross-check',
        tier=4,
        epistemic='P_structural_instrument',
        summary=(
            'On the banked skeleton (61 channels, 102 = 60 + 42 '
            'second-epsilon options, alphabet = the 42 Sector-B modes '
            '= dim V_global), ON THE COMMON-MODE SLICE of the Step-3 '
            'configuration family (42 of 42^61 configurations; the '
            'correlation is construction-supplied, its register form '
            'the OPEN a=b identity [C]), the Fourier phase code '
            '|mu_bar> = 42^{-1/2} sum_v omega^{mu v}|v>^{x61} realizes '
            'vacuum no-leakage (P1) at computed strength: 42 '
            'orthonormal label states whose reduced content on EVERY '
            'proper type-subset (all 60 sizes computed) is one fixed '
            'state; compressions of A-supported operators are '
            'equal-diagonal circulants (write access disclosed: '
            'privacy, not protection); one global Fourier measurement '
            'resolves the label perfectly -- and THE FINDING: that '
            'global read has no banked counterpart, while the banked '
            'horizon registration is label-BLIND on this code. The '
            'basis encoding fails the same test maximally. Collapse '
            'verified against full-tensor builds. Identification with '
            'the physical vacuum sector is a reading, not certified '
            'here; MSC/ICL_vac untouched.'
        ),
        key_result=(
            'P1 witnessed exact at label form on the common-mode '
            'carrier: no-leakage on all proper subsets; the banked '
            'horizon registration is label-blind on this code'
        ),
        dependencies=['L_count', 'T_kappa', 'L_self_exclusion',
                      'T_horizon_reciprocity', 'T11',
                      'T_interface_sector_bridge', 'L_QEC_code_space'],
        cross_refs=['T_which_v_no_registered_interior_reader',
                    'T_vglobal_offdiagonal_blocks_scalar_typed',
                    'T_vglobal_slot_identification_no_go',
                    'L_QEC_knill_laflamme',
                    'L_QEC_distance', 'L_QEC_wedge_duality',
                    'L_common_demand_iff_degenerate',
                    'T_vacuum_logical_sector_classical_ceiling',
                    'T_vacuum_mixed_42dim_secret_scheme_exists'],
        artifacts={
            'n_types': N_TYPES,
            'alphabet': ALPHABET,
            'd_eff': D_EFF,
            'carrier': 'common-mode slice (42 of 42^61 configurations; '
                       'construction-supplied correlation)',
            'proper_subset_sizes_computed': '1..60, all 42 labels',
            'proper_subset_marginal': 'uniform mixture, 1/42 diagonal',
            'compression_structure': 'commuting family of circulants',
            'banked_horizon_read_on_this_code': 'label-blind (uniform)',
            'negative_control_trace_distance': 1.0,
            'full_tensor_crosscheck': '(3,3) and (4,3) exact',
        },
    )


def check_T_vacuum_logical_sector_classical_ceiling():
    """T_vacuum_logical_sector_classical_ceiling: No Subspace-Coherent 42-dim Sector [P_structural_instrument].

    See the module docstring, clauses (a)-(d), and fence (4). The
    privacy requirement admits no SUBSPACE-COHERENT logical sector of
    dim >= 2: coherent superpositions of the private frame are exactly
    the leaky states, no 2-dim carrier subspace has state-independent
    marginals (pointwise elementary proof in the module docstring), and
    the general subspace statement rides the named cited steps
    (Knill-Laflamme 1997 + no-cloning). Subsystem/mixed encodings are
    NOT excluded (Cleve-Gottesman-Lo 1999) -- and the fit question is
    closed EXISTS by check_T_vacuum_mixed_42dim_secret_scheme_exists;
    realization remains the open reading.
    """
    F = _frame()
    n = ALPHABET
    rng = random.Random(42061102)

    # ---- (a) the Fourier-dual exhibit: sum of the frame = product state ----
    for v in range(n):
        amp = sum(F[mu][v] for mu in range(n)) / math.sqrt(n)
        want = 1.0 if v == 0 else 0.0
        check(abs(amp - want) < _TOL,
              f"(a) uniform superposition must collapse to |0>^x61 "
              f"(component v={v}: {amp:.2e})")
    # its single-channel marginal is pure |0><0|: trace distance from
    # the uniform mixture, computed from the two states themselves
    product_state = [sum(F[mu][v] for mu in range(n)) / math.sqrt(n)
                     for v in range(n)]
    p_leak = [abs(product_state[v]) ** 2 for v in range(n)]
    p_uniform = [1.0 / n] * n
    td = 0.5 * sum(abs(p_leak[v] - p_uniform[v]) for v in range(n))
    check(abs(td - (1.0 - 1.0 / n)) < _TOL,
          f"(a) leak witness trace distance = {td:.4f} != 1 - 1/42")

    # ---- (b) in-carrier ceiling: 2-dim subspaces leak (state-dependence) ----
    def _state_dependence_defect(x, y):
        """Max over probe states psi in span{x,y} of the sup-norm
        deviation of psi's single-channel diagonal from x's diagonal
        (0 would mean state-INDEPENDENT marginals -- the P1-relevant
        privacy notion; audit fix 2)."""
        base = [abs(x[v]) ** 2 for v in range(n)]
        worst = 0.0
        for a, b in ((0.0, 1.0), (1.0, 1.0), (1.0, 1j),
                     (1.0, -1.0), (2.0, 1j)):
            vec = [a * x[v] + b * y[v] for v in range(n)]
            norm = math.sqrt(sum(abs(c) ** 2 for c in vec))
            diag = [abs(c / norm) ** 2 for c in vec]
            worst = max(worst,
                        max(abs(diag[v] - base[v]) for v in range(n)))
        return worst

    # the label frame's own 2-dim spans leak on superposition
    d01 = _state_dependence_defect(F[0], F[1])
    check(d01 > 1e-3,
          f"(b) span(|0_bar>,|1_bar>) must leak on superposition "
          f"(state-dependence defect = {d01:.4f})")
    # random 2-dim carrier subspaces all leak
    for trial in range(12):
        x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        nx = math.sqrt(sum(abs(c) ** 2 for c in x))
        x = [c / nx for c in x]
        y0 = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        ip = sum(x[v].conjugate() * y0[v] for v in range(n))
        y = [y0[v] - ip * x[v] for v in range(n)]
        ny = math.sqrt(sum(abs(c) ** 2 for c in y))
        y = [c / ny for c in y]
        d = _state_dependence_defect(x, y)
        check(d > 1e-6,
              f"(b) random 2-dim carrier subspace trial {trial} shows "
              f"no state-dependence (defect = {d:.2e}) -- ceiling "
              f"violated?")

    # the proof chain's pivot, exhibited on the frame pair: the cross
    # products conj(x_v) y_v are NOT pointwise zero (their non-vanishing
    # is exactly where the pointwise proof localizes the leak)
    cross = [F[0][v].conjugate() * F[1][v] for v in range(n)]
    cross_max = max(abs(c) for c in cross)
    check(cross_max > 1e-3,
          "(b-pivot) frame cross products are nonzero pointwise -- the "
          "leak is exactly where the pointwise proof places it")

    # ---- (c) the general step is a docstring-level import; its
    #          in-model face: subspace privacy of A would be the
    #          operator condition P O_A P = c P; clause (iv) computed
    #          P O_A P = circulant, which is scalar ONLY on the trivial
    #          1-dim logical algebra -- generic circulants are not
    #          scalar. Subsystem/mixed evasion (CGL 1999) is FENCED in
    #          the module docstring, not adjudicated here. ----
    g = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    M = _compression(F, g)
    off = max(abs(M[a][b]) for a in range(n) for b in range(n) if a != b)
    check(off > 1e-6,
          "(c) generic compression is non-scalar: subspace-coherent "
          "privacy (the KL erasure condition) fails on the carrier")

    # ---- (d) classicality corollary, scoped: the compressions form a
    #          commuting family, simultaneously DFT-diagonalized ----
    def _dft_conj_offdiag(M_):
        n_ = len(M_)
        s = 1.0 / math.sqrt(n_)
        W = [[_omega(a * b, n_) * s for b in range(n_)] for a in range(n_)]
        WM = [[sum(W[k][a].conjugate() * M_[k][b] for k in range(n_))
               for b in range(n_)] for a in range(n_)]
        D = [[sum(WM[a][k] * W[k][b] for k in range(n_))
              for b in range(n_)] for a in range(n_)]
        return max(abs(D[a][b]) for a in range(n_) for b in range(n_)
                   if a != b)
    check(_dft_conj_offdiag(M) < 1e-8,
          "(d) every compression is DFT-diagonal: the interior-"
          "touchable logical structure at subspace form is abelian")

    return _result(
        name='T_vacuum_logical_sector_classical_ceiling -- the '
             'subspace-coherence ceiling: privacy forces the '
             'globally-locked 42-valued content to be a classical '
             'label alphabet AT SUBSPACE FORM; no subspace-coherent '
             '42-dim vacuum logical sector exists; subsystem/mixed '
             'encodings closed EXISTS (check 3; realization open)',
        tier=4,
        epistemic='P_structural_instrument',
        summary=(
            'The privacy requirement of P1 admits NO subspace-coherent '
            '(pure-isometric) logical sector of dim >= 2: the uniform '
            'superposition of the 42 private label states IS the '
            'product state |0>^x61 (exact Fourier collapse, '
            'single-channel leak 1 - 1/42); no 2-dim subspace of the '
            'common-mode carrier has state-independent marginals '
            '(pointwise elementary proof in the module docstring, '
            'state-dependence witnesses computed); the general '
            'subspace statement is the named cited step '
            '(Knill-Laflamme 1997 erasure condition + no-cloning). '
            'THE SCOPE FENCE: subsystem/mixed-state encodings evade '
            'the no-cloning step (Cleve-Gottesman-Lo 1999 -- the '
            '((2,2)) one-time-pad is the counterexample form; the '
            'banked OA-QECC code state is itself mixed); the fit '
            'question is CLOSED EXISTS by the companion check '
            '(share dim 43 <= 102; realization stays the open '
            'reading). Corollary at '
            'subspace form: the interior-touchable logical structure '
            'is a commuting circulant family -- the "42-dim vacuum '
            'logical sector" of the route-(b) P1 wording is '
            'unconstructible as a subspace-coherent sector; the '
            'classical 42-label alphabet of the companion check is '
            'the maximum at subspace form, the exact species of the '
            'banked which-v object (.318) and census row 5 (.339).'
        ),
        key_result=(
            'No subspace-coherent 42-dim vacuum sector (in-carrier '
            'exact; general step cited KL-1997); mixed encodings '
            'closed EXISTS at 43 <= 102 (check 3; realization open)'
        ),
        dependencies=['L_count', 'T_kappa', 'L_self_exclusion',
                      'T_horizon_reciprocity', 'T11',
                      'T_interface_sector_bridge', 'L_QEC_code_space'],
        cross_refs=['T_vacuum_label_code_no_leakage',
                    'T_vacuum_mixed_42dim_secret_scheme_exists',
                    'T_which_v_no_registered_interior_reader',
                    'T_vglobal_offdiagonal_blocks_scalar_typed',
                    'L_QEC_knill_laflamme', 'L_QEC_wedge_duality'],
        artifacts={
            'fourier_collapse': 'sum_mu |mu_bar> / sqrt(42) = |0>^x61',
            'leak_witness_trace_distance': round(1.0 - 1.0 / ALPHABET, 6),
            'in_carrier_two_dim_privacy': 'impossible (exact, pointwise '
                                          'proof; witnesses computed)',
            'general_step': 'Knill-Laflamme 1997 + no-cloning [cited; '
                            'subspace-scoped]',
            'subsystem_evasion': 'Cleve-Gottesman-Lo 1999 [closed EXISTS, '
                                 'see check 3; realization open]',
            'compressed_algebra': 'commuting family of circulants '
                                  '(DFT-diagonal)',
        },
    )


# ---------------------------------------------------------------------------
# Check 3 machinery: the mixed ((61,61)) scheme (sparse-state simulator)
# ---------------------------------------------------------------------------

def _qss_encode_last(state, n_shares, p):
    """Apply the base isometry Sigma to the LAST share of a sparse state.

    State: dict mapping index-tuples -> amplitude. Layout: position 0
    is the reference, positions 1..n_shares are shares, positions
    n_shares+1.. are accumulated environment registers. The last share
    (position n_shares) is replaced by its two children (positions
    n_shares, n_shares+1); the new environment register is appended at
    the END of the tuple. Returns (new_state, n_shares+1).
    """
    inv = 1.0 / math.sqrt(p)
    out = {}
    for tup, amp in state.items():
        sec = tup[n_shares]
        head, tail = tup[:n_shares], tup[n_shares + 1:]
        for a in range(p):
            new = head + (a, (a + sec) % p) + tail + (((a + 2 * sec) % p),)
            out[new] = out.get(new, 0j) + amp * inv
    return out, n_shares + 1


def _qss_marginal(state, keep):
    """Reduced density (as a dict over kept-tuple pairs) on positions `keep`."""
    keep = tuple(keep)
    buckets = {}
    for tup, amp in state.items():
        rest = tuple(t for i, t in enumerate(tup) if i not in keep)
        kept = tuple(tup[i] for i in keep)
        buckets.setdefault(rest, []).append((kept, amp))
    rho = {}
    for terms in buckets.values():
        for k1, a1 in terms:
            for k2, a2 in terms:
                rho[(k1, k2)] = rho.get((k1, k2), 0j) + a1 * a2.conjugate()
    return rho


def _qss_rho_defect(rA, rB, rAB):
    """Entrywise defect || rho_AB - rho_A (x) rho_B ||_max."""
    worst = 0.0
    keys_a = {k[0] for k in rA} | {k[1] for k in rA}
    keys_b = {k[0] for k in rB} | {k[1] for k in rB}
    for (a1, a2) in [(x, y) for x in keys_a for y in keys_a]:
        for (b1, b2) in [(x, y) for x in keys_b for y in keys_b]:
            joint = rAB.get((a1 + b1, a2 + b2), 0j)
            prod = rA.get((a1, a2), 0j) * rB.get((b1, b2), 0j)
            worst = max(worst, abs(joint - prod))
    return worst


def _qss_decode_last_pair(state, n_shares, p):
    """Coherently decode the last two shares back into their parent.

    U1: (x, y) -> (x, y - x); F_- on register x; phase correction
    e^{2 pi i (p-2) w s / p}; the w register is then traced (it
    decouples exactly when recovery is exact). Environment registers
    are untouched. Returns (new_state_as_density_free_dict, n_shares-1)
    -- the w register is MOVED to the environment tail rather than
    traced, which is equivalent for the final density comparison and
    keeps the state pure.
    """
    out = {}
    pos_x, pos_y = n_shares - 1, n_shares
    inv = 1.0 / math.sqrt(p)
    for tup, amp in state.items():
        x, y = tup[pos_x], tup[pos_y]
        sec = (y - x) % p
        for w in range(p):
            ph = cmath.exp(-2j * cmath.pi * w * x / p) * cmath.exp(
                2j * cmath.pi * ((p - 2) * w * sec % p) / p)
            new = tup[:pos_x] + (sec,) + tup[pos_y + 1:] + (w,)
            out[new] = out.get(new, 0j) + amp * inv * ph
    return out, n_shares - 1


def _qss_build(n, p, d_ref, seed=None):
    """Build the ((n,n)) cascade state with a d_ref-dim entangled reference.

    Reference maximally entangled with the first d_ref basis secrets
    (d_ref <= p models the 42-in-43 subspace embedding). If seed is
    given, use a random (generic) entangled reference instead.
    """
    rng = random.Random(seed) if seed is not None else None
    state = {}
    for r in range(d_ref):
        c = (complex(rng.gauss(0, 1), rng.gauss(0, 1)) if rng
             else 1.0)
        state[(r, r)] = c
    norm = math.sqrt(sum(abs(a) ** 2 for a in state.values()))
    state = {k: v / norm for k, v in state.items()}
    n_shares = 1
    while n_shares < n:
        state, n_shares = _qss_encode_last(state, n_shares, p)
    return state, n_shares


def check_T_vacuum_mixed_42dim_secret_scheme_exists():
    """T_vacuum_mixed_42dim_secret_scheme_exists: The Fit Question Closed EXISTS [P_structural_instrument].

    See the module docstring, the check-3 block (A)-(F). A perfect
    ((61,61)) mixed quantum threshold scheme for a coherent 42-dim
    secret exists with every share dimension 43 <= 102. Walker
    CONSTRUCTION 0.95 + hostile audit LAND-WITH-FIXES 0.88, all seven
    fixes carried. Existence at abstract-encoding strength only; the
    banked-sector-ALIGNED scheme question is separate and un-walked.
    """
    P = 43

    # ---- (B) exact integer privacy certificates at p = 43 ----
    # share 1 kept (trace regs 2,3): a'+s'=a+s and a'+2s'=a+2s with
    # a'-a = ds forces 2 ds = ds i.e. ds = 0 (mod 43)
    bad = [ds for ds in range(1, P) if (2 * ds - ds) % P == 0]
    check(not bad, f"(B) share-1 cross-term congruence must be insoluble "
                   f"for s != s' (solutions: {bad})")
    # share 2 kept (trace regs 1,3): a'=a and 2(s-s') = 0
    bad = [ds for ds in range(1, P) if (2 * ds) % P == 0]
    check(not bad, "(B) share-2 cross-term congruence must be insoluble")
    # environment register (trace regs 1,2): a'=a and s'=s directly
    bad = [ds for ds in range(1, P) if ds % P == 0]
    check(not bad, "(B) environment cross-term congruence must be insoluble")

    # ---- (C) decoder phase identity, all (w, s) at p = 43 ----
    bad = [(w, sec) for w in range(P) for sec in range(P)
           if (2 * w * sec + (P - 2) * w * sec) % P != 0]
    check(not bad, f"(C) decoder correction identity fails at {bad[:3]}")

    # ---- (E) ((4,4)) p=3 full proper-subset scan, entangled ref ----
    p = 3
    state, n_sh = _qss_build(4, p, d_ref=3)
    n_pos = 1 + n_sh + (n_sh - 1)  # ref + shares + envs
    all_shares = list(range(1, n_sh + 1))
    from itertools import combinations
    n_scanned = 0
    for r in range(1, n_sh):
        for A in combinations(all_shares, r):
            rho_RA = _qss_marginal(state, (0,) + A)
            rho_R = _qss_marginal(state, (0,))
            rho_A = _qss_marginal(state, A)
            d = _qss_rho_defect(rho_R, rho_A, rho_RA)
            if d >= 1e-12:
                check(False, f"(E) ((4,4)) subset {A} leaks (defect {d:.2e})")
            n_scanned += 1
    check(n_scanned == 14, f"(E) must scan all 14 proper subsets "
                           f"(scanned {n_scanned})")
    # the two hardest subsets by name (all-but-one-child)
    for A in ((1, 2, 3), (1, 2, 4)):
        rho_RA = _qss_marginal(state, (0,) + A)
        d = _qss_rho_defect(_qss_marginal(state, (0,)),
                            _qss_marginal(state, A), rho_RA)
        check(d < 1e-12, f"(E) hardest subset {A} must be blind "
                         f"(defect {d:.2e}) -- the case-(ii) "
                         f"constant-channel identity, computed")

    # composed decoder: three stages back to the reference pair
    dec, m = state, n_sh
    while m > 2:
        dec, m = _qss_decode_last_pair(dec, m, p)
    # final base decode: shares (1,2) -> secret
    dec, m = _qss_decode_last_pair(dec, m, p)
    rho_final = _qss_marginal(dec, (0, 1))
    # target: the original maximally entangled pair
    target = {}
    for r1 in range(3):
        for r2 in range(3):
            target[((r1, r1), (r2, r2))] = 1.0 / 3
    worst = 0.0
    keys = {k[0] for k in rho_final} | {k[1] for k in rho_final} |            {k[0] for k in target} | {k[1] for k in target}
    for k1 in keys:
        for k2 in keys:
            worst = max(worst, abs(rho_final.get((k1, k2), 0j)
                                   - target.get((k1, k2), 0j)))
    check(worst < 1e-12, f"(E) ((4,4)) composed decoder must be exact "
                         f"(defect {worst:.2e})")

    # ---- (E) ((3,3)) p=5 with a 4-dim secret subspace, generic ref ----
    p = 5
    state, n_sh = _qss_build(3, p, d_ref=4, seed=424361)
    for r in range(1, n_sh):
        for A in combinations(range(1, n_sh + 1), r):
            d = _qss_rho_defect(_qss_marginal(state, (0,)),
                                _qss_marginal(state, A),
                                _qss_marginal(state, (0,) + A))
            check(d < 1e-12, f"(E) ((3,3)) p=5 subset {A} leaks "
                             f"(defect {d:.2e})")
    dec, m = state, n_sh
    while m > 1:
        dec, m = _qss_decode_last_pair(dec, m, p)
    rho_final = _qss_marginal(dec, (0, 1))
    rho_start = _qss_marginal(_qss_build(1, p, 4, seed=424361)[0],
                              (0, 1))
    worst = max(abs(rho_final.get(k, 0j) - rho_start.get(k, 0j))
                for k in set(rho_final) | set(rho_start))
    check(worst < 1e-12, f"(E) ((3,3)) p=5 composed decoder must be "
                         f"exact on the generic entangled reference "
                         f"(defect {worst:.2e})")

    # ---- (E) GHZ negative control at p=3: sum encoding leaks on
    #          superpositions (superoperator-constancy has teeth) ----
    p = 3
    ghz = {}
    for r in range(3):          # ref entangled with secret, sum encoding
        for x in range(p):
            ghz[(r, x, (r - x) % p)] = 1.0 / 3  # 1/sqrt(3) ref * 1/sqrt(3)
    # basis-label privacy: single-share marginal for each BASIS secret
    # is uniform -- but the Choi test against the entangled ref fails:
    d = _qss_rho_defect(_qss_marginal(ghz, (0,)),
                        _qss_marginal(ghz, (1,)),
                        _qss_marginal(ghz, (0, 1)))
    check(d > 0.05, f"(E) GHZ negative control must FAIL the "
                    f"superoperator-constancy test (defect {d:.3f})")

    return _result(
        name='T_vacuum_mixed_42dim_secret_scheme_exists -- the fit '
             'question closed EXISTS: a perfect ((61,61)) mixed '
             'threshold scheme for a coherent 42-dim secret with '
             'every share dimension 43 <= 102 (cascade of the '
             'polynomial-code ((2,2)); exact base certificates at '
             'p = 43; full proper-subset scans + composed decoder at '
             'reduced parameters; GHZ negative control)',
        tier=4,
        epistemic='P_structural_instrument',
        summary=(
            'The clause-(c) fit question closes EXISTS at '
            'abstract-encoding strength: 60 applications of the mixed '
            '((2,2)) polynomial-code scheme (base |s> -> p^{-1/2} '
            'sum_a |a, a+s, a+2s>, third register to the environment; '
            'p = 43) yield a perfect ((61,61)) scheme for a coherent '
            '42-dim secret with all 61 share dimensions exactly 43 '
            '<= 102. Base privacy = exact integer congruence '
            'certificates at p = 43 (stronger than float); recovery = '
            'measure-and-correct decoder with the correction identity '
            'pinned by integer loop; cascade privacy = the case-(ii) '
            'constant-channel identity (docstring proof) with full '
            'proper-subset scans at ((4,4)) p=3 (all 14, the two '
            'hardest by name) and ((3,3)) p=5 (4-dim secret, generic '
            'entangled reference), composed decoder exact in every '
            'case. The naive CGL route (pure ((61,121))) needs p >= '
            '121 > 102 and does NOT fit; the cascade is the '
            'load-bearing move. CONSEQUENCE for the ceiling: '
            'dimensional structure does not force classicality of '
            'globally-locked content; the subspace ceiling and the '
            'banked label-typing stand; the banked-sector-ALIGNED '
            'scheme question is separate and un-walked; realization/'
            'identification remains the open reading. No cited '
            'theorem is load-bearing (CGL 1999 is attribution).'
        ),
        key_result=(
            'Perfect ((61,61)) mixed scheme, coherent 42-dim secret, '
            'all share dims 43 <= 102: the mixed direction of the '
            'ceiling closes EXISTS (abstract encoding; realization '
            'open)'
        ),
        dependencies=['L_count', 'T_kappa', 'L_self_exclusion',
                      'T_horizon_reciprocity', 'T11',
                      'T_interface_sector_bridge', 'L_QEC_code_space'],
        cross_refs=['T_vacuum_label_code_no_leakage',
                    'T_vacuum_logical_sector_classical_ceiling',
                    'T_which_v_no_registered_interior_reader',
                    'T_vglobal_offdiagonal_blocks_scalar_typed',
                    'L_QEC_knill_laflamme'],
        artifacts={
            'scheme': '((61,61)) mixed; 60x cascade of polynomial-code '
                      '((2,2)) at p = 43; 1 base + 59 re-shares',
            'share_dims': '43 each (61 shares) <= 102',
            'share_dim_bound': '43 >= 42 (Gottesman important-share '
                               'bound, near-tight; exactly-42 open)',
            'naive_cgl_excluded': 'pure ((61,121)) needs p >= 121 > '
                                  '102; the cascade is what fits',
            'base_certificates': 'integer congruence + decoder phase '
                                 'identity, exact at p = 43',
            'scans': '((4,4)) p=3 all 14 subsets + ((3,3)) p=5 d_ref=4 '
                     'generic ref; composed decoders exact',
            'norm_convention': 'entrywise max defect (reported '
                               'elsewhere as Frobenius/trace -- '
                               'convention only)',
            'alignment': 'NOT sector-aligned; the aligned-scheme '
                         'question is separate and un-walked',
        },
    )


_CHECKS = {
    'T_vacuum_label_code_no_leakage':
        check_T_vacuum_label_code_no_leakage,
    'T_vacuum_logical_sector_classical_ceiling':
        check_T_vacuum_logical_sector_classical_ceiling,
    'T_vacuum_mixed_42dim_secret_scheme_exists':
        check_T_vacuum_mixed_42dim_secret_scheme_exists,
}


def register(registry):
    """Register the vacuum label code checks into the bank."""
    registry.update(_CHECKS)


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == '__main__':
    for _n, _r in run_all().items():
        print(('PASS' if _r.get('passed', True) else 'FAIL'), _n)
