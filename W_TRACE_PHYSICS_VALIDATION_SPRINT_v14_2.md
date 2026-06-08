
# W_TRACE Physics Validation Sprint v14.2

This sprint moves beyond the first ACFW extraction by stress-testing the input
convention and adding a second independent Standard-Model W/Delta-r source
family.

Closed in this sprint:

- `P_w_input_convention_stress_test`
- `P_w_independent_delta_r_crosscheck`
- `P_w_multisource_delta_r_comparison`
- `P_w_v142_physics_validation_sprint_report`

Headline numerical comparison:

- ACFW v14.1 source path: `M_W = 80.358678992326 GeV`, equivalent
  `Delta_r = 0.036614529324...`, gap to APF/W_TRACE `3.49 MeV`.
- Degrassi-Gambino-Giardino 2015 source path: `M_W = 80.357 GeV`, equivalent
  `Delta_r = 0.036714195737...`, gap to APF/W_TRACE `5.16 MeV`, within the
  declared combined `0.0095 GeV` source uncertainty.
- GFitter 2012 source path: `M_W = 80.359 GeV`, equivalent
  `Delta_r = 0.036595470118...`, gap to APF/W_TRACE `3.16 MeV`, within the
  declared `0.011 GeV` source uncertainty.

Interpretation: APF/W_TRACE sits a few MeV above a small independent SM source
cluster. That is a meaningful validation neighborhood, not a physical-export
closure. Component-sum, covariance, uncertainty propagation, and physical W
export remain locked.
