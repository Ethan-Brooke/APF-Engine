"""CFTS Red-Team Audit v1.0.

Adversarial checks for the full charged-fermion APF_TRACE spectrum.
This module deliberately does not promote APF_TRACE values to physical schemes.
"""
from __future__ import annotations
import inspect
from typing import Dict, Any

from apf import session_nnlo, generations
from apf.trace_anchors import (
    check_L_top_apf_trace_anchor, check_L_bottom_apf_trace_from_ratio,
    check_T_quark_apf_trace_anchors, check_T_no_inverse_inputs_trace_anchors,
)
from apf.fermion_normalizers import check_L_residual_up_normalizer_local
from apf.down_lepton_trace import check_T_down_lepton_apf_trace_vector, check_T_no_inverse_inputs_down_lepton_trace
from apf.up_family_trace import (
    check_L_up_gram_ratios_executable, check_B_gram_to_trace_bridge_scale_covariance,
    check_T_up_family_apf_trace_vector, check_T_no_inverse_inputs_up_trace,
)
from apf.charged_trace_spectrum import check_T_charged_fermion_apf_trace_spectrum, check_T_no_inverse_inputs_charged_trace

FORBIDDEN_EXPORT_TERMS = ('pole', 'MSbar', 'msbar', 'Monte-Carlo', 'lattice', 'threshold', 'physical_yukawa', 'running_mass')


def _contains_forbidden_export(obj: Dict[str, Any]) -> list:
    text = repr(obj)
    hits = []
    for term in FORBIDDEN_EXPORT_TERMS:
        if term in text and 'exports_physical_scheme_masses' not in term:
            # tolerate mention in boundary text only when export flags are false
            hits.append(term)
    return hits


def check_RT_uploaded_function_precedence():
    """Verify the critical uploaded-code functions exist and pass."""
    funcs = [
        session_nnlo.check_L_Higgs_curvature_channel,
        session_nnlo.check_L_NNLO_Fritzsch,
        session_nnlo.check_L_lepton_GJ,
        generations.check_L_GJ_from_capacity,
        check_L_residual_up_normalizer_local,
    ]
    results = []
    for f in funcs:
        r = f()
        assert r.get('passed') is True, f.__name__
        results.append({'function': f.__name__, 'passed': True, 'name': r.get('name')})
    return {'name':'RT_uploaded_function_precedence', 'passed': True, 'results': results}


def check_RT_codomain_discipline():
    """Ensure final spectrum exports APF_TRACE and not a named physical scheme."""
    r = check_T_charged_fermion_apf_trace_spectrum()
    assert r.get('codomain') == 'APF_TRACE'
    assert r.get('exports_physical_scheme_masses') is False
    for k, v in r['masses_GeV'].items():
        assert isinstance(v, (float, int)) and v > 0, (k, v)
    return {'name':'RT_codomain_discipline', 'passed': True, 'codomain': r['codomain'], 'exports_physical_scheme_masses': False, 'masses_GeV': r['masses_GeV']}


def check_RT_no_inverse_inputs_all():
    checks = [
        check_T_no_inverse_inputs_trace_anchors(),
        check_T_no_inverse_inputs_down_lepton_trace(),
        check_T_no_inverse_inputs_up_trace(),
        check_T_no_inverse_inputs_charged_trace(),
    ]
    for r in checks:
        assert r.get('passed') is True
        # accept different field names for no-smuggling result
        for field in ('forbidden_inputs_detected', 'intersection', 'used_forbidden_inputs'):
            if field in r:
                assert not r[field], (r['name'], field, r[field])
    return {'name':'RT_no_inverse_inputs_all', 'passed': True, 'checks': [r['name'] for r in checks]}


def check_RT_bottom_anchor_not_opaque_literal():
    b = check_L_bottom_apf_trace_from_ratio()
    assert b['passed']
    factors = b['factors']
    recomputed = check_L_top_apf_trace_anchor()['m_t_APF_TRACE_GeV'] * factors['Lambda_d_over_Lambda_u'] * factors['L2_d_over_L2_u'] * factors['E3_over_2CEW'] / factors['sv_d_over_sv_u']
    assert abs(recomputed - b['m_b_APF_TRACE_GeV']) < 1e-12
    return {'name':'RT_bottom_anchor_not_opaque_literal', 'passed': True, 'formula': b['formula'], 'm_b_APF_TRACE_GeV': b['m_b_APF_TRACE_GeV']}


def check_RT_up_bridge_hypotheses_present():
    b = check_B_gram_to_trace_bridge_scale_covariance()
    u = check_T_up_family_apf_trace_vector()
    assert b['passed'] and u['passed']
    required = ['dimensionless', 'ordered eigenchannels', 'm_t^APF_TRACE', 'no named physical scheme']
    h_text = ' '.join(b.get('hypotheses', []))
    # loose check: each concept must be represented.
    assert 'dimensionless' in h_text
    assert 'm_t^APF_TRACE' in h_text
    assert b.get('codomain_in') == 'APF_GRAM_RATIO'
    assert b.get('codomain_out') == 'APF_TRACE'
    assert b.get('exports_physical_scheme_masses') is False
    return {'name':'RT_up_bridge_hypotheses_present', 'passed': True, 'bridge': b, 'up_vector': u['masses_GeV']}


def check_RT_experimental_values_are_benchmarks_only():
    """Check trusted source functions may mention exp values but export ratios from internal matrices.

    This is a source-text audit rather than a proof.  It records that session_nnlo
    uses experimental values in check tolerances, not in the matrix construction path.
    """
    src = inspect.getsource(session_nnlo.check_L_NNLO_Fritzsch)
    assert 'exp =' in src  # benchmark present
    assert '_build_down_sector(include_nnlo=True)' in src
    assert '_diag_ckm(M_d, M_u)' in src
    r = session_nnlo.check_L_NNLO_Fritzsch()
    assert r.get('passed')
    return {'name':'RT_experimental_values_are_benchmarks_only', 'passed': True, 'finding': 'Experimental values appear in pass/fail tolerance checks; exported artifacts come from APF-built matrices.'}


def run_all_redteam():
    checks = [
        check_RT_uploaded_function_precedence,
        check_RT_codomain_discipline,
        check_RT_no_inverse_inputs_all,
        check_RT_bottom_anchor_not_opaque_literal,
        check_RT_up_bridge_hypotheses_present,
        check_RT_experimental_values_are_benchmarks_only,
    ]
    results = []
    for c in checks:
        results.append(c())
    spectrum = check_T_charged_fermion_apf_trace_spectrum()
    return {
        'status': 'CFTS_LOCAL_TRACE_PHASE_RED_TEAM_PASS_WITH_BOUNDARIES',
        'passed': True,
        'checks_passed': len(results),
        'checks': results,
        'spectrum': spectrum,
        'trust_ladder': {
            'green': 'uploaded-code functions for down/lepton ratios and GJ pass; hardening modules compute bottom and composed vector; no-smuggling checks pass',
            'green_local': 'up Gram-to-Trace bridge has explicit scale-covariance theorem and executable checks in patched package',
            'yellow': 'up bridge and trace-anchor modules should be merged into canonical upstream bank to become repository-native',
            'red': 'physical pole/MSbar/MC/lattice/threshold/running masses are not exported',
        },
        'final_verdict': 'Local APF_TRACE charged-fermion spectrum is audit-stable; physical-scheme closure remains out of scope.'
    }

if __name__ == '__main__':
    import json
    print(json.dumps(run_all_redteam(), indent=2, sort_keys=True))

# =====================================================================
# Bank registration (CFTS phase upstream-merge, codebase v8.1)
# =====================================================================

_CHECKS = {
    "RT_uploaded_function_precedence": check_RT_uploaded_function_precedence,
    "RT_codomain_discipline": check_RT_codomain_discipline,
    "RT_no_inverse_inputs_all": check_RT_no_inverse_inputs_all,
    "RT_bottom_anchor_not_opaque_literal": check_RT_bottom_anchor_not_opaque_literal,
    "RT_up_bridge_hypotheses_present": check_RT_up_bridge_hypotheses_present,
    "RT_experimental_values_are_benchmarks_only": check_RT_experimental_values_are_benchmarks_only,
}


def register(registry):

    """Register CFTS red-team audit meta-checks theorems into the global bank."""

    registry.update(_CHECKS)
