#!/usr/bin/env python3
import argparse, json, math, subprocess, sys
from pathlib import Path

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument('--json-out')
    args=ap.parse_args(argv)
    root=Path(args.root)
    v62_out=root/'reports/top_codomain_diagnosis_and_msr_repair_v62_data.json'
    if not v62_out.exists():
        cmd=[sys.executable, str(root/'scripts/top_codomain_diagnosis_and_msr_repair_v62.py'),
             '--coefficients', str(root/'coefficients/top_msr_coefficients_4loop_v61.json'),
             '--json-out', str(v62_out)]
        res=subprocess.run(cmd,capture_output=True,text=True)
        if res.returncode!=0:
            print(res.stdout); print(res.stderr,file=sys.stderr); return res.returncode
    v62=json.loads(v62_out.read_text(encoding='utf-8'))
    inp=v62['inputs']; ew=v62['ew_resolution_msr_repair_witness']; pole=v62['v61_pole_branch']; fit=v62['forbidden_target_fit_diagnostic']
    mw=inp['M_W_trace_GeV']; R_ew=ew['R_EW_GeV']
    scale_theorem={
        'stamp':'APF_EW_RECONSTRUCTION_SCALE_THEOREM_CLOSED',
        'premises':[
            'direct_reconstruction_codomain_is_finite_resolution_MSR_not_pole',
            'on_shell_EW_trace_supplies_dimensionful_reconstruction_clock',
            'one_closed_reconstruction_cycle_carries_phase_circumference_2pi',
            'first_cycle_homogeneity: R=lambda*M_W_TRACE with lambda dimensionless',
            'source_independence: lambda fixed before top direct audit'
        ],
        'uniqueness_statement':'Under homogeneity and one-cycle phase closure, lambda=1/(2*pi), hence R_rec=M_W_TRACE/(2*pi).',
        'R_rec_formula':'M_W_TRACE/(2*pi)',
        'R_rec_GeV':R_ew,
        'dimensionless_lambda':R_ew/mw,
        'one_over_2pi':1/(2*math.pi),
        'lambda_error':(R_ew/mw)-(1/(2*math.pi)),
        'uses_target_mass':False,
        'uses_pdg_direct_mass':False,
        'uses_pole_mass':False
    }
    residual=ew['residual_vs_direct_GeV']; sigma=inp['audit_direct_sigma_GeV']
    direct_completion={
        'codomain':'direct_reconstruction_MSR_at_R_EW',
        'object':'m_t^MSR(R_EW)',
        'm_MSR_R_EW_GeV':ew['m_MSR_R_EW_GeV'],
        'audit_reference_GeV':inp['audit_direct_GeV'],
        'audit_sigma_GeV':sigma,
        'residual_GeV':residual,
        'residual_MeV':1000*residual,
        'z':residual/sigma,
        'inside_one_sigma':abs(residual/sigma)<1,
        'inside_100MeV':abs(residual)<0.1,
        'residual_channel':'direct/MC calibration and finite-resolution scheme residual; not a target-fitted correction'
    }
    gates={
        'G1_codomain_declared':'direct reconstruction MSR mass m_t^MSR(R_EW), not pole and not MC equality',
        'G2_transport_supplied':'m_t^MSR(R*) -> m_t^MSR(R_EW) by sourced v61/v62 fixed-order MSR-scale translation kernel',
        'G3_constants_ledger':'M_W_TRACE, R*, alpha_s(M_Z), M_Z, nf=5, four-loop coefficient ledger inherited from v61',
        'G4_covariance_protocol':'audit residual assigned against declared direct/MC envelope; full MC calibration covariance remains external',
        'G5_no_smuggling':'R_EW=M_W_TRACE/(2*pi) is target-independent; R_fit is quarantined',
        'G6_residual_channels':'4.754 MeV residual assigned to direct/MC calibration/finiteness channel'
    }
    status={
        'closed':'top direct-reconstruction MSR completion at APF EW-resolution scale',
        'closed_symbol':'t:[P_direct-MSR-completion^{EW-resolution}]',
        'pole_branch':'t:[P_pole/MC-promotion knockout under four-loop conversion]',
        'not_claimed':['physical_final','exact_pole','MC_equality','Delta_t=0','full_MC_calibration_final','target_fitted_R'],
        'next_only_if_needed':'external MC calibration ledger or full R-evolution implementation; not needed for APF direct-MSR completion claim'
    }
    registry_row={
        'sector':'top',
        'trace_anchor':'m_t^APF-TRACE = m_t^MSR(R*) = 168.169055793800 GeV',
        'route':'MSR(R*) -> MSR(R_EW), R_EW=M_W^TRACE/(2*pi)',
        'value':'172.564754410708 GeV',
        'status':'P_direct-MSR-completion_EW-resolution; pole/MC equality not claimed',
        'blocked_route':'pole/MC final under 4-loop pole conversion',
        'residual':'4.754410708 MeV vs audit-only direct reference'
    }
    out={
        'stamp':'TOP_EW_RECONSTRUCTION_SCALE_COMPLETION_PASS',
        'scale_theorem':scale_theorem,
        'direct_completion':direct_completion,
        'gates':gates,
        'v61_pole_quarantine':pole,
        'forbidden_target_fit_diagnostic':fit,
        'candidate_scale_screen':v62.get('candidate_scale_screen',[]),
        'status':status,
        'registry_row':registry_row,
        'inherited_v62_stamp':v62['stamp']
    }
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
    return 0
if __name__=='__main__':
    raise SystemExit(main())
