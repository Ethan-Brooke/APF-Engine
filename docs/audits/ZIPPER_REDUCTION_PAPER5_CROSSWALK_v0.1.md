# APF Zipper Reduction — Paper 5 Crosswalk v0.1

**Status:** unbanked audit reconciliation; no theorem-bank, registry, census, version, or export changes  
**Branch:** `audit/zipper-reduction-v0.1`  
**Parent packet:** `docs/audits/ZIPPER_REDUCTION_AUDIT_PACKET_v0.1.md`  
**Frontier companion:** `docs/audits/ZIPPER_REDUCTION_FRONTIER_PROGRESS_v0.1.md`  
**Operational bridge:** `docs/audits/ZIPPER_OPERATIONAL_REFLECTION_BRIDGE_v0.1.md`

## 1. Audited source inputs

The crosswalk uses the exact user-supplied sources below. The paper sources are not copied into the repository; their hashes identify the audit inputs.

| Source | SHA-256 |
|---|---|
| `Paper_5_Continuation_Symmetry_Degenerate_Occupied_Minima_v1.7(1).tex` | `0a4126f1425006f4f63814910d0043971e7810e847acd8bed6ca3a03580072f4` |
| `Paper_5_Quantum_Structure_Hilbert_Born_Supplement_v6.14(3).tex` | `b3f4122ecbfd0863f16f07861814e13c82392c841e0dfd3d1968314d6bc39943` |

## 2. Executive disposition

The two Paper 5 supplements materially help, but they change the novelty account.

`Continuation Symmetry ... v1.7` already contains a conditional whole-circle occupant–zipper route:

1. an occupied record-free coherent component with a later non-null recombination witness;
2. path connectedness in unsaturated Regime R;
3. a completion-faithful first-order rank-two bipolar lift;
4. admitted record-free coherent loops and reverses with ledger isometry;
5. smooth represented loop action;
6. a nontrivial path-connected effective image in `SO(2)`;
7. the quarter-turn `J^2=-I`, naturality, centrality, and a composite-orientation dichotomy.

`Quantum Structure ... v6.14` already contains conditional finite downstream closure for:

- IJC-to-QAC record incompatibility in a record-complete coherent interface;
- noncommutative finite record representations;
- split composite gates: tensor closure, tomographic locality, and zero-defect product accounting;
- finite complex matrix sectors and Born trace probabilities;
- extension-stability as the physical criterion that becomes complete positivity after the matrix gate.

Therefore the zipper packet must not be billed as the first APF route to a quarter-turn, complex finite blocks, tensor structure, CP, or Born form.

Its genuine delta is narrower:

> Given a realised positive rank-two Held-event plane and a differentiable non-stationary metric exchange involution, the packet constructs the local complex structure directly and pointwise from comparison-frame motion,
>
> \[
> A=\frac12\dot\tau\tau,
> \qquad
> J=\frac{A}{\sqrt{-\frac12\operatorname{tr}(A^2)}}.
> \]

It is a local differential reduction and executable audit instrument. It does not replace Paper 5's occupancy, connectedness, naturality, centrality, composite, CP, or Born gates.

## 3. Relation between the two local-\(J\) routes

### 3.1 Paper 5 v1.7 route

The Paper 5 route is global-to-local:

\[
\text{occupied coherent component}
\longrightarrow
G_A^{\mathrm{eff}}=SO(2)
\longrightarrow
\text{quarter-turn }J_A.
\]

The non-null recombination witness makes the effective action nontrivial. Path connectedness and exact ledger isometry place the image in `SO(2)`. A nontrivial path-connected subgroup of `SO(2)` is the full circle.

### 3.2 Moving-exchange route

The zipper route is infinitesimal:

\[
\text{moving metric reflection }\tau(s)
\longrightarrow
A=\tfrac12\dot\tau\tau
\longrightarrow
J=A/\omega.
\]

It exposes the local angular rate

\[
\omega=\sqrt{-\frac12\operatorname{tr}(A^2)}.
\]

### 3.3 Exact overlap

If the operational reflection is transported by Paper 5 holonomy,

\[
\tau(s)=U(s)\tau_0U(s)^{-1},
\qquad
K=\dot U U^{-1},
\]

then

\[
\frac12\dot\tau\tau
=\frac12(K-\tau K\tau).
\]

On the positive oriented rank-two branch, a reflection reverses the `SO(2)` generator:

\[
\tau K\tau=-K.
\]

Hence

\[
\boxed{
\frac12\dot\tau\tau=K=\dot U U^{-1}.
}
\]

This identity is now executable in `apf.zipper_reflection_bridge`. The remaining bridge is physical realization of the comparison reflection, its effective quotient action, and its record-neutral conjugation orbit.

### 3.4 Non-duplication fence

- path-connected holonomy does not automatically supply a distinguished moving reflection family;
- a moving reflection family does not automatically prove naturality or centrality in the full observable algebra;
- a pointwise `J` does not synchronize orientation across sectors;
- Paper 5's coordinate quarter-turn may not be used upstream to self-certify the moving-exchange formula.

## 4. Five-premise reconciliation

| Zipper physical premise | Paper 5 surface | Status |
|---|---|---|
| `ACTIVE_RECORD_KERNEL_REALIZED` | v6.14 obtains a QAC witness only in a record-complete coherent interface already containing physically co-available coherent families. v1.7 L1 starts from an actual multiply-trajectoried record-free coherent component. | **Not discharged.** Occupancy/co-availability remains an input. The admissibility-event program targets this exact gap. |
| `COMPLETION_FAITHFUL_RANK_TWO_QUOTIENT` | v1.7 L3 uses Paper 10’s first-order universal local quotient and a rank-two bipolar lift. Passing to the represented image gives effective faithfulness. | **Strong prior match, still conditional.** Physical realization of the complete response quotient remains open. |
| `POSITIVE_EVENT_METRIC_REALIZED` | v1.7 assumes a faithful positive ledger form and derives exact orthogonality from `T^sharp=T^-1`. | **Not discharged.** Residual-Hessian or closed-loop derivation remains independently useful. |
| `SMOOTH_NONSTATIONARY_OPERATIONAL_EXCHANGE_REALIZED` | v1.7 L2/L5 supply a path-connected coherent component and smooth represented loop action; recombination supplies nontriviality. | **Reduced but not discharged.** The new bridge decomposes this into an effective binary exchange plus a nontrivial record-neutral conjugation orbit. |
| `RECORD_NEUTRAL_EXPORT_FREE_COMPLETION_PATH` | v1.7 L1/L4 require record-free coherent loops and reverses; closed-world completeness accounts for consequential exits. | **Close prior match, still contingent.** Physical existence of the path is assumed, not universal. |

## 5. Operational reflection realization

The new bridge gives the exact targeted reduction:

\[
P=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\qquad
F=\begin{pmatrix}1&1\\1&-1\end{pmatrix},
\]

\[
\tau_0=FPF^{-1}
=\operatorname{diag}(1,-1).
\]

A binary port exchange is therefore a common/defect reflection when:

- the binary Held presentation is physically realised;
- the exchange is a record-neutral process, not a label swap;
- the defect survives the complete operational quotient;
- the exchange is ledger-neutral and returns to the same carrier type.

The defect-killing quotient makes the same raw swap descend to identity. Algebraic sharp effects do not imply dynamic exchange availability.

The exact live 3–4–5 witness transports the second binary exchange through

\[
F_{345}=\frac15\begin{pmatrix}-1&7\\7&1\end{pmatrix}
\]

to

\[
S_u=F_{345}PF_{345}^{-1}
=\frac1{25}\begin{pmatrix}-7&24\\24&7\end{pmatrix}.
\]

Together with \(S_0\), it yields the trace \(-14/25\) rotation. A label-only second exchange kills that rotation.

## 6. Orientation and centrality

Paper 5 v1.7 separates three issues.

### Local orientation

The occupant–zipper theorem gives a local quarter-turn on the elementary bipolar plane.

### Naturality and centrality

Typed elementary comparison morphisms act through the universal first-jet lift

\[
W(f)=Df_0\oplus Df_0=a_fI,
\]

so they commute with the canonical quarter-turn. Centrality additionally requires:

- those continuations generate the completed observable algebra;
- the physical quarter-turn loop is admitted.

The moving-exchange formula does not discharge generator completeness or quarter-turn admission.

### Composite synchronization

Before quotienting,

\[
S_A^1\times S_B^1
\cong
S_{\mathrm{diag}}^1\times S_{\mathrm{rel}}^1.
\]

Paper 5 gives a witness/null dichotomy:

1. a completed witness makes the relative circle an additional physical orientation record;
2. without such a witness, the relative circle is operationally null, leaving the diagonal complex action and a composite balanced over the common central `j`.

This is the event-level physical criterion behind orientation synchronization. The cocycle/double-cover packet remains the network consistency schema.

## 7. Tensor-composition reconciliation

If the relative orientation is null,

\[
(j_Aa)\boxtimes b=a\boxtimes(j_Bb),
\]

and the product factors through the complex tensor product.

Paper 5 v6.14 adds the product-record map

\[
\Pi_{AB}:V_A\otimes_{\mathbb R}V_B\to V_{AB}.
\]

Zero-defect composition requires

\[
\ker\Pi_{AB}=0,
\qquad
\operatorname{coker}\Pi_{AB}=0,
\]

plus order-unit preservation, finite tomographic locality, and no hidden boundary debt.

The matrix-unit check in `zipper_reduction_frontier.py` remains an exact model check, not the physical tensor theorem.

## 8. Complete-positivity reconciliation

Paper 5 v6.14 supplies the correct logical direction:

1. start with finite affine/order-preserving maps of the certified ordered record theory;
2. require **extension-stability** under certified ancillas;
3. preserve positivity, normalization/order unit, quotient ideals, and record-locking constraints under `T tensor id_B`;
4. after the complex matrix gate, extension-stability is complete positivity;
5. Kraus and Stinespring forms are downstream representation theorems.

The frontier Choi/Kraus check is therefore an exact downstream witness and negative-control suite. It may not replace the physical extension-stability gate with an assumed dilation.

## 9. Born reconciliation

Paper 5 v6.14 already reaches the conditional finite endpoint

\[
\mathcal A_Q\simeq\bigoplus_kM_{n_k}(\mathbb C),
\]

with

\[
\omega(E)=\sum_kp_k\operatorname{Tr}(\rho_kE_k),
\]

reducing to \(\operatorname{Tr}(\rho E)\) in an irreducible sector.

The arbitrary-\(n\) trace-uniqueness check in the frontier module is an independent regression of cyclicity and normalization, not a new physical Born derivation.

The physical leaves remain score linearity/cyclicity, actual state/effect/readout realization, contextual effect identity, finite measurement normalization, tomography, and sandwich closure.

`G-hold-exact` remains granted rather than derived.

## 10. Action scale

Neither Paper 5 supplement derives the numerical value of `hbar`. The formulas use it downstream in dynamics and emission laws.

The zipper geometry fixes only dimensionless phase:

\[
\theta=S/\hbar.
\]

The rescaling

\[
(S,\hbar)\mapsto(cS,c\hbar)
\]

is invisible. One dimensional action calibration remains.

## 11. Empirical moving-frame reconciliation

A first census should test:

1. actual record-free co-availability and a later non-null recombination witness;
2. path connectedness within an unsaturated fixed stratum;
3. completion-faithful rank-two response;
4. admitted loops and reverses without record/export leakage;
5. smooth represented action;
6. an effective operational port exchange on the same carrier;
7. at least two distinct comparison frames or a reconstructed conjugation orbit;
8. agreement between \(\tfrac12\dot\tau\tau\) and the observed holonomy generator.

Static, discrete-jump, rank-changing, exporting, label-only, and record-forming branches remain controls.

## 12. Revised dependency order

\[
\text{admissibility-event clearance / physical co-availability}
\]

\[
\Downarrow
\]

\[
\text{completion-faithful rank-two Held response and positive ledger}
\]

\[
\Downarrow
\]

\[
\text{effective binary exchange }\tau_0
+\text{ record-neutral conjugation orbit}
\]

\[
\Downarrow
\]

\[
J=\operatorname{normalize}\!\left(\tfrac12\dot\tau\tau\right)
\]

\[
\Downarrow
\]

\[
\text{naturality / centrality / orientation synchronization}
\]

\[
\Downarrow
\]

\[
\text{finite tensor / extension stability / CP / Born}
\]

The action-scale calibration is downstream of phase geometry.

## 13. May-not-cite fence

This crosswalk may not be cited for:

- physical occupancy or co-availability;
- derivation of the positive metric;
- physical realization of the comparison exchange or conjugation path;
- unconditional naturality, centrality, tensor equality, CP, or Born weighting;
- derivation of `hbar`;
- theorem-bank or export closure.

The strongest licensed statement is:

> Paper 5 already supplies the conditional global Held-circle and finite downstream quantum architecture. The zipper program adds an executable local differential reduction and a targeted operational-reflection bridge. On the common positive rank-two branch, the moving comparison frame reconstructs the same infinitesimal holonomy generator as Paper 5.

## 14. Reproduction

```bash
python -m apf.zipper_reduction
python -m apf.zipper_reflection_bridge
python -m apf.zipper_reduction_frontier
python -m pytest -q \
  tests/test_zipper_reduction.py \
  tests/test_zipper_reflection_bridge.py \
  tests/test_zipper_reduction_frontier.py
python verify_all.py --bank-audit
```
