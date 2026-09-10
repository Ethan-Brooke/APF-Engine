# APF Zipper Reduction — Downstream Frontier Progress v0.1

**Status:** unbanked audit companion; no registry, census, version, or export changes  
**Branch:** `audit/zipper-reduction-v0.1`  
**Primary module:** `apf/zipper_reduction_frontier.py`  
**Tests:** `tests/test_zipper_reduction_frontier.py`  
**Parent packet:** `docs/audits/ZIPPER_REDUCTION_AUDIT_PACKET_v0.1.md`

## 1. Purpose

The moving-exchange packet closes the exact local formula

\[
A=\frac12\dot\tau\tau,
\qquad
\omega=\sqrt{-\frac12\operatorname{tr}(A^2)},
\qquad
J=A/\omega,
\qquad
J^2=-I
\]

on a realised positive rank-two Held-event plane.

This companion tracks the six downstream obligations that remain before a full finite quantum event package can be claimed:

1. global orientation synchronization across sectors;
2. arbitrary finite-dimensional tensor composition;
3. complete positivity for reduced events;
4. the Born weighting rule;
5. scale fixing to \(\hbar\)-normalized action;
6. the physical/empirical scope of the moving-frame branch.

The companion does not certify any physical premise. It closes mathematical schemas, records negative controls, and reduces each remaining burden to its smallest current physical surface.

## 2. Progress summary

| Lane | Exact progress in this packet | Remaining burden |
|---|---|---|
| Global orientation | Trivial \(\mathbb Z_2\) parity cocycle iff one-sheet synchronization; nontrivial cycle repaired by canonical orientation double cover | `ORIENTATION_COVER_REALIZED`, `ORIENTATION_SHEET_TYPING`, network-scale physical synchronization |
| Finite tensor composition | Generic commuting matrix-unit embeddings generate \(M_{mn}(\mathbb C)\); synchronized complex balancing gives real dimension \(2mn\) | physical commuting embeddings, generated composite, tensor faithfulness, synchronized orientation |
| Reduced-event CP | Finite isometric dilation gives Kraus form, positive Choi Gram matrix, and trace preservation; transpose retained as positive/not-CP control | complete-event isometry, tensor-faithful environment, physical partial discard, extension soundness |
| Born weighting | For every finite \(n\), normalized cyclic linear score on \(M_n(\mathbb C)\) is uniquely \(\operatorname{Tr}/n\); sample POVMs normalize exactly | physical score linearity/cyclicity, actual states/effects, dense sandwich closure, tomography/contextual identity |
| \(\hbar\) scale | Exact one-parameter scale gauge isolated: phase determines \(H/\hbar\), not \(H\) and \(\hbar\) separately | one dimensional action calibration tying the event ledger to empirical \(\hbar\) |
| Moving-frame universality | Universal “every elementary interface” claim refuted by static/discrete/recording controls; sectoral coherent-branch claim defined | empirical interface-response census over quantum-capable fixed-stratum interfaces |

## 3. Orientation synchronization

### Exact result

For a sector graph with transition parity \(\epsilon_{ij}\in\{\pm1\}\), local orientation signs \(s_i\) satisfy

\[
s_j=\epsilon_{ij}s_i
\]

iff every cycle has parity product \(+1\). The packet computes:

- a mixed-sign graph with trivial cycle parity and an exact global sign assignment;
- a triangle with cycle product \(-1\) and no one-sheet assignment;
- the canonical two-sheet lift
  \((i,\sigma)\mapsto(j,\epsilon_{ij}\sigma)\),
  which is always orientation-consistent.

### Reduction

The mathematics is already aligned with `apf.graded_orientation_closure`:

\[
\text{local }J
+
\text{trivial parity cocycle}
\Longrightarrow
\text{one-sheet synchronization},
\]

while a nontrivial cocycle requires the realised orientation cover.

### Still open

The existence of the canonical cover is mathematical. The physical claim that the interface network realises its sheets and sheet-changing morphisms remains open.

## 4. Arbitrary finite-dimensional tensor composition

### Exact algebraic schema

For finite complex dimensions \(m,n\), the standard subsystem embeddings

\[
\iota_A(a)=a\otimes I_n,
\qquad
\iota_B(b)=I_m\otimes b
\]

commute. Products of matrix units

\[
(E_{ij}\otimes I)(I\otimes F_{ab})=E_{ij}\otimes F_{ab}
\]

span all of \(M_{mn}(\mathbb C)\). The module checks the exact rank \((mn)^2\) for several dimension pairs using generic code.

The complex tensor product is represented as the balanced real quotient

\[
V_A\otimes_{\mathbb C}V_B
=
\frac{V_A\otimes_{\mathbb R}V_B}
{\langle J_Av\otimes w-v\otimes J_Bw\rangle},
\]

with

\[
\dim_{\mathbb R}(V_A\otimes_{\mathbb C}V_B)=2mn.
\]

### Orientation control

If sector B uses the opposite orientation, the relation becomes

\[
J_Av\otimes w=-v\otimes J_Bw.
\]

This is conjugate balancing; the same scalar \(i\) does not descend from both factors. Thus global orientation synchronization is genuinely upstream of the ordinary complex tensor product.

### Still open

The code proves the algebraic universal schema, not that arbitrary physical APF interfaces realise tensor-faithful commuting subsystem embeddings or the generated full composite.

## 5. Complete positivity for reduced events

### Exact finite dilation schema

Given Kraus operators \(K_\alpha\), define

\[
Vx=\sum_\alpha K_\alpha x\otimes|\alpha\rangle.
\]

The packet checks in dimensions \(2,3,4\):

\[
V^*V=I,
\qquad
\Phi(X)=\operatorname{Tr}_E(VXV^*)
=
\sum_\alpha K_\alpha X K_\alpha^*,
\]

and

\[
C_\Phi
=
\sum_\alpha
\operatorname{vec}(K_\alpha)
\operatorname{vec}(K_\alpha)^*
\ge0.
\]

Trace preservation is exactly

\[
\sum_\alpha K_\alpha^*K_\alpha=I.
\]

The matrix transpose remains the sharp control: its Choi matrix is the swap and has an antisymmetric eigenvector of eigenvalue \(-1\).

### Reduction

Once a reduced event is physically realised as a partial discard of a complete isometric event on a tensor-faithful composite, CPTP form is mathematics rather than an additional quantum postulate.

### Still open

The physical extension-soundness package remains:

- complete-event isometry;
- tensor-faithful environment;
- identity extension on an independently maintained reference;
- joint positivity preservation;
- physical partial discard.

## 6. Born weighting

### Arbitrary finite-dimensional trace uniqueness

For matrix units \(E_{ij}\), cyclicity gives

\[
L(E_{ii}E_{ij})=L(E_{ij}E_{ii})
\quad\Longrightarrow\quad
L(E_{ij})=0
\quad(i\ne j),
\]

and

\[
L(E_{ij}E_{ji})=L(E_{ji}E_{ij})
\quad\Longrightarrow\quad
L(E_{ii})=L(E_{jj}).
\]

Normalization \(L(I)=1\) therefore gives

\[
L(A)=\frac1n\operatorname{Tr}(A)
\]

on \(M_n(\mathbb C)\). The module checks matrix-unit cyclicity and exact Born normalization for \(n=2,\ldots,6\).

A normalized coordinate score \(A\mapsto A_{00}\) is retained as the negative control: it is normalized but not cyclic.

### Relation to the banked Born packet

`apf.dense_sandwich_born` already banks the elementary finite Born-soundness chain at a composed 39-premise physical inventory. This frontier check extends the trace-uniqueness mathematics to arbitrary finite matrix dimension; it does not reduce the physical inventory.

### Still open

The load-bearing physical leaves remain score linearity and cyclicity, state/effect soundness, dense sandwich realisation, finite operational tomography, contextual effect identity, and finite measurement normalization.

## 7. Action scale and \(\hbar\)

The zipper geometry fixes phase and phase rate:

\[
U(t)=e^{\theta(t)J},
\qquad
\dot U U^{-1}=\dot\theta J.
\]

Standard action notation writes

\[
\theta=\frac{S}{\hbar},
\qquad
\dot\theta=\frac{H}{\hbar}.
\]

But

\[
(H,\hbar)\mapsto(cH,c\hbar)
\]

leaves every phase invariant. The packet verifies this exactly over rational examples.

### Reduction

The remaining scale burden is one-dimensional. Geometry determines the dimensionless phase law; exactly one dimensional action calibration is needed.

A possible APF route is

\[
\hbar_{\rm APF}=\epsilon_*\tau_*,
\]

but this is only a candidate factorization. It requires an independently derived universal continuation-time quantum \(\tau_*\) and a proof that one elementary phase/action cycle carries precisely that product.

### Still open

- `ACTION_LEDGER_TO_PHASE_CALIBRATION`;
- `UNIVERSAL_ACTION_QUANTUM`;
- `IDENTIFICATION_WITH_EMPIRICAL_HBAR`.

The packet explicitly proves that the absolute scale cannot be extracted from local complex geometry alone.

## 8. Empirical scope of the moving-frame branch

The universal statement

> every elementary physical interface realises the moving-frame branch

is too strong.

The packet owns coherent synthetic controls for:

- a nonconstant connected moving exchange frame;
- a valid static exchange frame;
- a discrete \(C_2\) frame jump;
- a record-forming/rank-changing event boundary.

Therefore the universal claim is reduced to the sectoral empirical target:

> Every elementary interface in the completion-faithful, positive rank-two, connected-context, record-neutral, export-free, fixed-stratum coherent branch exhibits a nonconstant operational exchange frame.

This is an empirical classification program. The minimum record should contain:

1. rank-two response reconstruction;
2. a positive event-metric witness;
3. nearby context settings \(\lambda\);
4. reconstructed operational exchanges \(\tau(\lambda)\);
5. record/export audit;
6. fixed-stratum/rank audit.

No exhaustive interface census is currently supplied.

## 9. Dependency discipline

The frontier graph is intentionally acyclic:

\[
\text{empirical moving branch}
\longrightarrow
T_{\rm zipper\ local\ J}
\longrightarrow
\text{orientation synchronization}
\longrightarrow
\text{finite complex tensor composition}
\longrightarrow
\text{reduced-event CP}.
\]

Born weighting is downstream of the oriented finite matrix algebra and the physical state/effect/score package, but it is forbidden upstream of the local \(J\).

The \(\hbar\) scale is downstream of phase geometry and may not be used to derive it.

The empirical moving-frame premise may not be inferred from the existence of the local \(J\); that would affirm the consequent. A mutation inserting that edge creates a dependency cycle and is caught by the packet.

## 10. May-not-cite fence

This companion may not be cited for:

- physical realization of a global orientation cover;
- physical equality with the full tensor product at every interface;
- universal CPTP realization of every reduced APF event;
- unconditional Born weighting in nature;
- derivation of the numerical value of \(\hbar\);
- the claim that every elementary interface lies in the moving-frame branch;
- theorem-bank or export closure.

The strongest licensed summary is:

> The downstream finite mathematics has been substantially compressed. Orientation synchronization has an exact cocycle/double-cover criterion; arbitrary finite complex tensor and reduced-event CP schemas are exact once their physical realization gates obtain; normalized cyclic finite scores are uniquely trace scores; the action scale has exactly one undetermined dimensional calibration; and the universal moving-frame claim must be reduced to an empirical coherent-branch census.

## 11. Reproduction

```bash
python -m compileall -q apf/zipper_reduction_frontier.py
python -m apf.zipper_reduction_frontier
python -m pytest -q tests/test_zipper_reduction_frontier.py
```

The parent workflow also runs the original moving-exchange packet and `verify_all.py --bank-audit` to confirm that the candidate remains unregistered and does not perturb the canonical bank.

## 12. Audit questions

1. Should the synchronized tensor quotient be the next separately audited packet, or remain a frontier check until `ORIENTATION_COVER_REALIZED` is addressed?
2. Is complete-event isometry derivable directly from the zipper no-silent-loss package, or must inverse continuability remain a named physical leaf?
3. Can the banked 39-leaf Born inventory be reduced by importing the zipper event metric and arbitrary finite trace-uniqueness result?
4. Is there any APF-internal dimensional datum capable of fixing the action scale without importing measured \(\hbar\)?
5. Which interface families belong in the first empirical moving-frame census, and what counts as an operational reconstruction of \(\tau(\lambda)\)?
6. Is the universal moving-frame claim intended literally, or only for the quantum-capable Held branch?
