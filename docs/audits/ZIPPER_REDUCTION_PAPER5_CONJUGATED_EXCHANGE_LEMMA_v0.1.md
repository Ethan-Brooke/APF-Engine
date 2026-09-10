# APF Zipper Reduction — Conjugated-Exchange Equivalence Lemma v0.1

**Status:** unbanked exact-math audit note  
**Parent:** `ZIPPER_REDUCTION_PAPER5_CROSSWALK_v0.1.md`  
**Executable witness:** `T_moving_exchange_formula_exact` in `apf/zipper_reduction.py`

## 1. Purpose

Paper 5 v1.7 reaches the local complex structure through a nontrivial path-connected effective holonomy image in `SO(2)`. The zipper packet reaches it from a differentiable moving operational exchange involution.

This note records the exact equivalence of those two descriptions on their common branch.

## 2. Theorem

Let `(E,g)` be a positive oriented real two-plane. Let

\[
U(s)\in SO(E,g)
\]

be a differentiable active holonomy transport, and let `tau_0` be a metric-self-adjoint reflection:

\[
\tau_0^2=I,
\qquad
\tau_0^{\dagger_g}=\tau_0.
\]

Transport the operational comparison frame actively:

\[
\tau(s)=U(s)\tau_0U(s)^{-1}.
\]

Define the right-trivialized holonomy generator

\[
K(s)=\dot U(s)U(s)^{-1}.
\]

Then:

1. `tau(s)` remains a metric-self-adjoint involution;
2. `K(s)` is metric-skew;
3. every metric reflection on an oriented positive two-plane anticommutes with every element of `so(2)`, so
   \[
   \tau K\tau=-K;
   \]
4. the moving-exchange generator is exactly the holonomy generator:
   \[
   \boxed{
   \frac12\dot\tau\tau=K.
   }
   \]

Consequently, whenever `K` is nonzero,

\[
\boxed{
\frac{\frac12\dot\tau\tau}
{\sqrt{-\frac12\operatorname{tr}\left[\left(\frac12\dot\tau\tau\right)^2\right]}}
=
\frac{K}{\sqrt{-\frac12\operatorname{tr}(K^2)}}.
}
\]

The zipper formula therefore reconstructs the normalized infinitesimal generator of the Paper 5 holonomy circle directly from observable comparison-frame motion.

## 3. Proof

Differentiate

\[
\tau=U\tau_0U^{-1}.
\]

Using

\[
\frac{d}{ds}U^{-1}=-U^{-1}\dot U U^{-1},
\]

we obtain

\[
\dot\tau
=
\dot U\tau_0U^{-1}
-
U\tau_0U^{-1}\dot U U^{-1}
=
K\tau-\tau K
=[K,\tau].
\]

Multiplying on the right by `tau` and using `tau^2=I`,

\[
\frac12\dot\tau\tau
=
\frac12(K\tau-\tau K)\tau
=
\frac12(K-\tau K\tau).
\]

On an oriented positive two-plane, `so(2)` is one-dimensional. Write

\[
K=\omega J,
\qquad
J^2=-I.
\]

A reflection reverses orientation, hence

\[
\tau J\tau=-J.
\]

Therefore

\[
\tau K\tau=-K,
\]

and

\[
\frac12\dot\tau\tau
=
\frac12(K-(-K))
=K.
\]

## 4. Convention fence

The sign is tied to the active transport convention

\[
\tau=U\tau_0U^{-1},
\qquad
K=\dot U U^{-1}.
\]

For the passive convention

\[
\tau=U^{-1}\tau_0U,
\]

the corresponding left-trivialized generator and the reconstructed orientation carry the opposite sign. The audit packet must therefore state its active/passive convention explicitly rather than treating the sign as a coordinate accident.

## 5. Relation to the executable witness

The exact rational family already used in `T_moving_exchange_formula_exact`,

\[
\tau(t)=R(t)S_0R(t)^T,
\]

is precisely the active-conjugation construction above, with `U=R`, `tau_0=S_0`, and `R^{-1}=R^T`.

Thus the existing code is not merely a convenient sample path. It is an exact finite witness of the conjugated-exchange equivalence lemma.

## 6. What the lemma reduces

The lemma shows that, once Paper 5 v1.7 supplies:

- a differentiable active `SO(2)` holonomy path; and
- one physically meaningful operational comparison reflection,

the moving-exchange formula does not posit a second complex structure. It reconstructs the same local generator.

Conversely, a reconstructed non-stationary exchange path supplies the infinitesimal generator without first proving that the entire effective image is `SO(2)`.

This makes the two routes complementary:

\[
\text{Paper 5: global circle}\Rightarrow\text{moving frames},
\]

\[
\text{zipper packet: moving frames}\Rightarrow\text{local generator}.
\]

## 7. What remains open

The lemma does not certify:

- physical existence of an operational reflection `tau_0`;
- that the Paper 5 holonomy path transports that reflection without record or export leakage;
- completion-faithful reconstruction of `tau(s)` from experiments;
- positivity of the event metric;
- occupancy of the coherent record-kernel;
- naturality, centrality, or global orientation synchronization;
- the Born rule or action-scale calibration.

## 8. Audit question

The next exact physical bridge is:

> Does the bipolar comparison structure in Paper 5 v1.7 contain a physically admitted metric reflection `tau_0` whose conjugation orbit under the coherent holonomy is the operational exchange-frame family reconstructed by the zipper event?
