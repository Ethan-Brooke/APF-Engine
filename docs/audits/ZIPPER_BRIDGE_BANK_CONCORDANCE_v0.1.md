# APF Zipper Bridge — Banked Held-Holonomy Concordance v0.1

**Status:** unbanked audit concordance; no theorem-bank, registry, census, version, or export changes  
**Branch:** `audit/zipper-reduction-v0.1`  
**Module:** `apf/zipper_bridge_bank_concordance.py`  
**Tests:** `tests/test_zipper_bridge_bank_concordance.py`

## 1. Purpose

The zipper packet must not duplicate or overbill the already banked Held-holonomy and two-exchange work.

This concordance proves four things:

1. the matrices used by the zipper bridge are exactly the banked two-exchange matrices;
2. the bridge's physical premise names reconcile to the existing Held-holonomy and two-exchange root inventories;
3. the relevant banked checks and the unbanked bridge execute together without contradiction;
4. every physical premise remains explicitly uncertified.

It is a dependency and provenance instrument, not a new physical theorem.

## 2. Exact matrix concordance

The packet checks equality of:

- the binary port swap \(P\);
- the common/defect zipper \(F\);
- the first reflection \(S_0\);
- the live 3–4–5 presentation, up to its irrelevant common factor \(1/5\);
- the transported second reflection \(S_u\);
- the two-exchange rotation
  \[
  R=S_uS_0
  =\frac1{25}\begin{pmatrix}-7&-24\\24&-7\end{pmatrix},
  \qquad
  \operatorname{tr}R=-\frac{14}{25}.
  \]

Thus the operational-reflection bridge is not a parallel matrix convention.

## 3. Root reconciliation

The bridge premises are mapped to the existing root vocabularies in:

- `apf._held_holonomy_common.PHYSICAL_PREMISES`;
- `apf.two_exchange_roots.PHYSICAL_ROOTS`.

The existing two-exchange roots already name:

- `ADMITTED_SECOND_BINARY_PRESENTATION`;
- `EFFECTIVE_FIRST_CONTENDER_EXCHANGE`;
- `EFFECTIVE_SECOND_CONTENDER_EXCHANGE`;
- `INTERTWINER_REVERSAL_IS_INVERSE`;
- `LATER_RECOMBINATION_WITNESS_FOR_EACH_EXCHANGE`;
- `SAME_CARRIER_RETURN`;
- `UNIVERSAL_EXCHANGE_NATURALITY_ON_ADMITTED_PRESENTATIONS`;
- the exact 3–4–5 fixed-line overlap and codespace-to-presentation bridge.

The Held-holonomy roots already name occupied record-free coherence, complete operational congruence, connected Regime R, continuous action, positive ledger, reversal-adjoint/inverse, first-order completeness, faithful action, continuous conjugation orientation transport, and closed-world completeness.

The concordance does **not** treat vocabulary coverage as physical discharge. All of these roots remain premises in the banked modules.

## 4. Revised novelty statement

The following are prior conditional APF results:

- binary exchange as common/defect reflection;
- exact 3–4–5 transported second reflection;
- the trace \(-14/25\) two-exchange gate;
- the occupied Held-circle route to `SO(2)` and a quarter-turn;
- downstream finite complex/tensor/CP/Born schemas.

The zipper delta is:

\[
\boxed{
A=\frac12\dot\tau\tau
=\frac12(K-\tau K\tau),
}
\]

and, on the positive oriented rank-two branch,

\[
\boxed{
A=K=\dot U U^{-1}.
}
\]

This is the pointwise differential reconstruction of the already conditional Paper 5 holonomy generator from operational comparison-frame motion.

## 5. Executable cross-check

The concordance executes selected checks from:

- `apf.two_exchange_holonomy`;
- `apf.held_holonomy`;
- `apf.zipper_reflection_bridge`.

It requires every selected row to pass while retaining

```text
physical_premises_certified = false
```

throughout.

## 6. May-not-cite fence

This packet may not be cited for:

- physical realization of either exchange path;
- physical occupancy of the Held sector;
- discharge of the positive-ledger, connectedness, or first-order-faithfulness roots;
- novelty for the quarter-turn or the first APF complex-structure route;
- theorem-bank or export closure.

The strongest licensed statement is:

> The zipper operational-reflection bridge is exactly concordant with the banked two-exchange and Held-holonomy mathematics. Its genuine additional content is the local differential moving-frame formula and its targeted conjugation-orbit interpretation. The combined physical root surface remains uncertified.

## 7. Reproduction

```bash
python -m compileall -q apf/zipper_bridge_bank_concordance.py
python -m apf.zipper_bridge_bank_concordance
python -m pytest -q tests/test_zipper_bridge_bank_concordance.py
```
