#!/usr/bin/env python3
from __future__ import annotations
import json, sys, os
# Synthetic adapter for protocol validation only.  It must never be promoted to physics output.
def main():
    req=json.load(sys.stdin)
    cases=req.get('cases',{})
    results={}
    for k,v in cases.items():
        # Echo source values with a harmless deterministic scale factor so schema can be tested.
        # This is not RunDec and is flagged as protocol self-test only.
        results[k]={
            'mass_target_GeV': v['m0_GeV']*0.999,
            'alpha_target': v.get('alpha0',0.0)*0.999,
            'start_scale_GeV': v['mu0_GeV'],
            'target_scale_GeV': v['mu1_GeV'],
            'nf': v['nf']
        }
    print(json.dumps({
        'schema':'APF_RunDec_Adapter_Response_v1',
        'results':results,
        'loop_order':0,
        'threshold_schedule':'synthetic-none',
        'matching_convention':'synthetic-protocol-self-test-only',
        'covariance':'synthetic-none',
        'validation_id':'SYNTHETIC_PROTOCOL_SELF_TEST_DO_NOT_USE_FOR_PHYSICS',
        'no_target_reuse':True,
        'protocol_self_test_only':True,
        'physics_promotable':False
    }, indent=2, sort_keys=True))
if __name__=='__main__': main()
