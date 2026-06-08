# APF v37 Top MSR Scale-Selection Theorem

Status: `TOP_MSR_SCALE_SELECTION_THEOREM_PASS`.

This package extends v35/v36 by closing the top branch at the route-object level.  The new claim is not a final pole, Monte-Carlo, or PDG top-mass claim.  It is a typed MSR export-candidate claim:

`m_t^APF_TRACE -> m_t^MSR(R_star)` with `R_star = 85.8572226984 GeV`, displayed as `85.86 GeV`.

The selector is

`R_star = 0.5 * (T_t + (3/68) * T_W)`,

where `T_t = 168.1690557938 GeV`, `T_W = 80.362164334 GeV`, and `3/68` is the APF weak-Higgs route fraction from `3_SU2 / (61_SM + 3_SU2 + 4_H)`.

No external top pole mass, Monte-Carlo mass, MSbar mass, externally extracted MSR mass, or world-average top datum is used to construct the scale.

Promotion: top changes from `[P_terminal_scheme]` to `[P_export_candidate^MSR(R_star)]`.  Downstream conversion to pole/MC/MSbar remains deferred and must be assigned to residual channels.
