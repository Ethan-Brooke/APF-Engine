# W_TRACE Reviewed-Pipeline Release Checklist Template

Template only. Not real finite-part evidence. Does not unlock physical W export.

## Required artifacts
- [ ] `completed_review_packet_json`
- [ ] `review_packet_digest`
- [ ] `source_candidate_digest`
- [ ] `payload_file_uri`
- [ ] `payload_sha256_digest`
- [ ] `extraction_log_digest`
- [ ] `import_session_log_json`
- [ ] `replay_report_json`
- [ ] `row_bundle_admission_report_json`
- [ ] `component_sum_certificate_json`
- [ ] `covariance_certificate_json`
- [ ] `uncertainty_propagation_certificate_json`
- [ ] `final_export_readiness_report_json`

## Operator actions
- [ ] `collect_artifacts`
- [ ] `compute_and_record_digests`
- [ ] `run_review_packet_validator`
- [ ] `run_reviewed_source_handoff`
- [ ] `run_payload_import_cli`
- [ ] `write_import_session_log`
- [ ] `replay_import_session`
- [ ] `run_row_bundle_admission`
- [ ] `run_component_sum_certificate`
- [ ] `run_covariance_certificate`
- [ ] `run_uncertainty_propagation`
- [ ] `run_final_export_readiness`

## Forbidden inputs
Do not include observed M_W, W world average, residual-fit, APF-anchor as component input, or manual export override tokens.
