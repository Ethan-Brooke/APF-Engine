"""APF OS-W finite-remainder source-transcription family kernels (verbatim).

Six fail-closed coefficient-map kernels for the on-shell-W one-loop Delta r
assembly, source-transcribed from Dao/Gabelmann/Muehlleitner 2022 EPJC and
Denner 1993 (arXiv:0709.1075). Each kernel maps a *source-certified* self-energy
or counterterm value into the algebraic slot by which it enters Delta r; NONE of
them computes a self-energy, and NONE evaluates Delta r_rem / DeltaRhobarW / M_W.

These modules are installed verbatim as the sibling delivered them (the six
APF_EW_OS_W_SOURCE_TRANSCRIBE_* packs, archived in full under
Codebase/EW_OSW_SOURCE_TRANSCRIBE_PACKS_v1/). They are imported and checked --
not re-derived -- by apf.ew_osw_source_transcription_families, which banks the
architecture-only [P_structural]/[C] certificates and advances the
apf.ew_osw_reviewed_formula_evaluator_harness pending-family count 14 -> 8.

Family -> module map (numbering = harness contract order):
  1  W_transverse_self_energy        -> w_transverse_self_energy
  2  gamma_Z_mixing                  -> gamma_z_mixing
  3  Z_transverse_self_energy        -> z_transverse_self_energy
  4  vertex_box_terms                -> vertex_box_terms
  5  gamma_gamma_vacuum_polarization -> gamma_gamma_vacuum_polarization
  6  mass_charge_weak_angle_counterterms -> mass_charge_weak_angle_counterterms
"""
