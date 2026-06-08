#!/usr/bin/env python3
import argparse, json, math, sys
MT_MSR_RSTAR=168.1690557938
RSTAR=85.857222698385
MW_TRACE=80.362164334
REW=MW_TRACE/(2*math.pi)
MT_MSR_REW_FIXED=172.564754410708
MT_POLE_4LOOP=174.016604383647

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['fixed_order_witness','full_r_evolution'], default='fixed_order_witness')
    args=ap.parse_args()
    if args.mode=='fixed_order_witness':
        out={
          'stamp':'TOP_MSR_R_EVOLUTION_FIXED_ORDER_WITNESS',
          'mode':args.mode,
          'm_t_MSR_Rstar_GeV':MT_MSR_RSTAR,
          'R_star_GeV':RSTAR,
          'R_EW_GeV':REW,
          'm_t_MSR_REW_GeV':MT_MSR_REW_FIXED,
          'not_full_R_evolution':True,
          'physical_final':False
        }
        print(json.dumps(out, indent=2))
        return 0
    out={
      'stamp':'TOP_MSR_R_EVOLUTION_FAIL_CLOSED',
      'mode':args.mode,
      'status':'blocked',
      'missing':['gamma_R coefficient table','integration convention','threshold covariance','alpha_s covariance protocol'],
      'physical_final':False
    }
    print(json.dumps(out, indent=2))
    return 2
if __name__=='__main__':
    raise SystemExit(main())
