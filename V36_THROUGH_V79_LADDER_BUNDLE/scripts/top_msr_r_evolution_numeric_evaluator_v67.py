#!/usr/bin/env python3
import argparse,json,math
MT=168.1690557938; RSTAR=85.857222698385; MW=80.362164334; REW=MW/(2*math.pi); MZ=91.1876; ALPHA_MZ=0.118
BETA=[7.666666666666667, 38.66666666666667, 180.90740740740753, 4826.156328790895]; GAMMA=[5.333333333333333, 48.3501, 179.49875000000014, -18753.775]
def beta_a(a,L): return -2*sum(BETA[i]*a**(i+2) for i in range(L))
def gamma(a,L): return sum(GAMMA[i]*a**(i+1) for i in range(L))
def run_a_log(mu0,a0,mu,L,steps=1000):
    t0=math.log(mu0); t1=math.log(mu); h=(t1-t0)/steps; a=a0
    for _ in range(steps):
        k1=beta_a(a,L); k2=beta_a(a+0.5*h*k1,L); k3=beta_a(a+0.5*h*k2,L); k4=beta_a(a+h*k3,L)
        a += h*(k1+2*k2+2*k3+k4)/6
    return a
def alpha_at(mu,alpha_mz=ALPHA_MZ,L=4): return 4*math.pi*run_a_log(MZ,alpha_mz/(4*math.pi),mu,L)
def integrate(Rhi,Rlo,alpha_mz=ALPHA_MZ,L=4,N=5000):
    a=run_a_log(MZ,alpha_mz/(4*math.pi),Rhi,L); d=0.0; R=Rhi; h=(Rlo-Rhi)/N
    def f(R,a): return beta_a(a,L)/R, -gamma(a,L)
    for _ in range(N):
        k1a,k1d=f(R,a); k2a,k2d=f(R+0.5*h,a+0.5*h*k1a); k3a,k3d=f(R+0.5*h,a+0.5*h*k2a); k4a,k4d=f(R+h,a+h*k3a)
        a += h*(k1a+2*k2a+2*k3a+k4a)/6; d += h*(k1d+2*k2d+2*k3d+k4d)/6; R += h
    return d,a
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--loops',type=int,choices=[1,2,3,4],default=4); ap.add_argument('--alpha_s_MZ',type=float,default=ALPHA_MZ); ap.add_argument('--N',type=int,default=5000); args=ap.parse_args()
    d,aew=integrate(RSTAR,REW,args.alpha_s_MZ,args.loops,args.N); m=MT+d
    print(json.dumps(dict(stamp='TOP_MSR_R_EVOLUTION_NUMERIC_EVALUATOR_V67',loops=args.loops,m_t_MSR_Rstar_GeV=MT,R_star_GeV=RSTAR,R_EW_GeV=REW,delta_R_evolution_GeV=d,m_t_MSR_REW_GeV=m,alpha_s_Rstar=alpha_at(RSTAR,args.alpha_s_MZ,args.loops),alpha_s_REW=4*math.pi*aew,codomain='MSR(R_EW)',not_pole_mass=True,not_MC_equality=True,physical_final=False),indent=2))
if __name__=='__main__': main()
