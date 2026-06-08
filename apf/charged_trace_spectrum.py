"""Full charged-fermion APF_TRACE spectrum checks.
Strengthened by UpBridgeStrength_v1.0.
"""
from __future__ import annotations
from apf.down_lepton_trace import check_T_down_lepton_apf_trace_vector, check_T_no_inverse_inputs_down_lepton_trace
from apf.up_family_trace import check_T_up_family_apf_trace_vector, check_T_no_inverse_inputs_up_trace, check_B_gram_to_trace_bridge_scale_covariance


def check_T_charged_fermion_apf_trace_spectrum():
    u = check_T_up_family_apf_trace_vector()
    d = check_T_down_lepton_apf_trace_vector()
    assert u.get('passed') and d.get('passed')
    masses = {}
    masses.update(u['masses_GeV'])
    masses.update(d['masses_GeV'])
    return {
        'name':'T_charged_fermion_apf_trace_spectrum',
        'passed': True,
        'epistemic': 'P_local | upstream-banking-ready',
        'codomain':'APF_TRACE',
        'masses_GeV': masses,
        'status':'FULL_LOCAL_TRACE_VECTOR_CLOSED__GRAM_TO_TRACE_BRIDGE_STRENGTHENED',
        'exports_physical_scheme_masses': False,
        'claim_ladder': {
            'green':'down/lepton ratios and GJ executable from uploaded trusted code; Lambda_u executable from uploaded code; bottom/down-lepton hardening checks pass',
            'green_local':'up-family Gram-to-Trace bridge now has scale-covariance theorem and no-smuggling check in this patched package',
            'yellow':'up bridge should be upstream-banked to become repository-native [P]',
            'red':'physical pole/MSbar/MC/lattice/threshold masses are not exported'
        }
    }


def check_T_no_inverse_inputs_charged_trace():
    u = check_T_no_inverse_inputs_up_trace()
    d = check_T_no_inverse_inputs_down_lepton_trace()
    assert u['passed'] and d['passed']
    return {
        'name':'T_no_inverse_inputs_charged_trace',
        'passed': True,
        'forbidden_inputs':['observed charged-fermion masses as inputs','target-fitted scalar transport','physical scheme mass identity'],
        'intersection': [],
        'exports_physical_scheme_masses': False,
    }


def check_T_up_bridge_strengthened():
    return check_B_gram_to_trace_bridge_scale_covariance()

# =====================================================================
# Bank registration (CFTS phase upstream-merge, codebase v8.1)
# =====================================================================

_CHECKS = {
    "T_charged_fermion_apf_trace_spectrum": check_T_charged_fermion_apf_trace_spectrum,
    "T_no_inverse_inputs_charged_trace": check_T_no_inverse_inputs_charged_trace,
    "T_up_bridge_strengthened": check_T_up_bridge_strengthened,
}


def register(registry):

    """Register charged-fermion trace spectrum master theorems into the global bank."""

    registry.update(_CHECKS)
