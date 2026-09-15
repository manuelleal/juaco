"""
Simbiosis v0 — dos organismos, dependencia obligada, neuromodulador ambiental.
Mundo: anillo 1D de L celdas. Comida cruda aparece al azar.
  A puede PROCESAR cruda -> procesada (si está encima). No puede comer.
  B puede DIGERIR procesada (si está encima). Al digerir, ambos ganan energía.
Cada organismo: red de N neuronas (2 sensores izq/der, H ocultas, 2 motoras).
  voltaje LIF, disparo estocástico, trazas, STDP, neuromodulador ambiental
  (gana de aprendizaje), homeostasis (synaptic scaling), reflejo sensor->motor.
"""
import numpy as np, sys

L=40; H=20; N=2+H+2
SENS=[0,1]; HID=list(range(2,2+H)); MOT=[2+H,3+H]

class Org:
    def __init__(s, rng, learn, reflex=0.6):
        s.rng=rng; s.learn=learn
        s.W=rng.normal(0,0.15,(N,N)); np.fill_diagonal(s.W,0)
        s.W[SENS,:]=0                      # nadie escribe en sensores
        # reflejo de nacimiento (residual): sensor izq -> motor izq, der -> der
        s.W[MOT[0],SENS[0]]+=reflex; s.W[MOT[1],SENS[1]]+=reflex
        s.V=np.zeros(N); s.tr=np.zeros(N); s.S=np.zeros(N)
        s.rate=np.full(N,0.1); s.pos=rng.integers(L); s.E=0.0
        s.tauV=3.0; s.thr=0.5; s.noise=0.15; s.eta=0.004
        s.target=0.12
    def step(s, sensin, M):
        inp=s.W@s.S; inp[SENS]=sensin
        s.V+=(-s.V+inp)/s.tauV
        p=1/(1+np.exp(-(s.V-s.thr)/s.noise))
        S_new=(s.rng.random(N)<p).astype(float)
        s.tr=s.tr*0.8+S_new
        if s.learn:
            gain=1+4.0*M                           # neuromodulador ambiental
            pre=s.tr; post=S_new
            dW=s.eta*gain*(np.outer(post,pre)-np.outer(s.S,s.tr)*0.9)  # STDP asim.
            dW[SENS,:]=0; np.fill_diagonal(dW,0)
            s.W+=dW
            # homeostasis: escalar entradas para mantener tasa objetivo
            s.rate=0.995*s.rate+0.005*S_new
            scale=1+0.01*(s.target-s.rate)
            s.W*=scale[:,None]
            s.W=np.clip(s.W,-1.5,1.5)
        s.S=S_new
        move=int(S_new[MOT[1]]-S_new[MOT[0]])
        s.pos=(s.pos+move)%L


# ---- v2: inhibición (Dale) + normalización homeostática por neurona ----
NI=6
class OrgV2(Org):
    def __init__(s,rng,learn,reflex=0.6):
        super().__init__(rng,learn,reflex)
        s.sign=np.ones(N); s.sign[HID[-NI:]]=-1
        s.W=np.abs(s.W)*s.sign[None,:]; s.W[SENS,:]=0
        s.W[MOT[0],SENS[0]]=reflex; s.W[MOT[1],SENS[1]]=reflex
        s.norm=np.abs(s.W).sum(1)
    def step(s,sensin,M):
        inp=s.W@s.S; inp[SENS]=sensin
        s.V+=(-s.V+inp)/s.tauV
        p=1/(1+np.exp(-(s.V-s.thr)/s.noise))
        S_new=(s.rng.random(N)<p).astype(float)
        s.tr=s.tr*0.8+S_new
        if s.learn:
            gain=1+4.0*M
            dW=s.eta*gain*(np.outer(S_new,s.tr)-0.9*np.outer(s.S,s.tr))
            dW[SENS,:]=0; np.fill_diagonal(dW,0)
            s.W+=dW*s.sign[None,:]
            s.W=np.where(s.sign[None,:]>0,np.clip(s.W,0,1.5),np.clip(s.W,-1.5,0))
            tot=np.abs(s.W).sum(1); tot[tot==0]=1
            s.W*=(s.norm/tot)[:,None]
        s.S=S_new
        s.pos=(s.pos+int(S_new[MOT[1]]-S_new[MOT[0]]))%L
Org=OrgV2   # usar v2 por defecto

def sensors(pos,items):
    """intensidad izq/der del item más cercano en cada dirección"""
    if not items: return np.zeros(2)
    dl=min(((pos-x)%L) for x in items); dr=min(((x-pos)%L) for x in items)
    return np.array([1/(1+dl),1/(1+dr)])*1.2

def run(seed, learn, T=30000):
    rng=np.random.default_rng(seed)
    A=Org(rng,learn); B=Org(rng,learn)
    raw=set(); proc=set()
    Mfield=np.zeros(L)               # neuromodulador en el ambiente
    eaten=[]; processed=0; uptakeA=0; uptakeB=0
    for t in range(T):
        if rng.random()<0.08 and len(raw)<4: raw.add(int(rng.integers(L)))
        MA=Mfield[A.pos]; MB=Mfield[B.pos]; uptakeA+=MA; uptakeB+=MB
        A.step(sensors(A.pos,raw),MA); B.step(sensors(B.pos,proc),MB)
        if A.pos in raw:
            raw.discard(A.pos); proc.add(A.pos); processed+=1
            A.E+=0.3; Mfield[A.pos]+=0.5            # recompensa propia pequeña
        if B.pos in proc:
            proc.discard(B.pos); eaten.append(t)
            A.E+=1.0; B.E+=1.0                      # recompensa colectiva
            Mfield[B.pos]+=1.0; Mfield[A.pos]+=1.0
        Mfield*=0.97                                # decae
        Mfield=0.8*Mfield+0.1*(np.roll(Mfield,1)+np.roll(Mfield,-1))  # difunde
    eaten=np.array(eaten)
    q=T//4
    early=(eaten<q).sum(); late=(eaten>=3*q).sum()
    return dict(early=early,late=late,total=len(eaten),processed=processed,
                asymA=np.abs(A.W-A.W.T).mean(),uptakeA=uptakeA,uptakeB=uptakeB)

if __name__=="__main__":
    for learn in (True,False):
        print("\n=== aprendizaje", "ON" if learn else "OFF","===")
        for seed in (1,2,3):
            r=run(seed,learn)
            print(f"seed {seed}: comidas 1er cuarto={r['early']:3d}  último cuarto={r['late']:3d} "
                  f" total={r['total']:3d} procesadas={r['processed']:3d} "
                  f"asimW_A={r['asymA']:.3f} uptakeA={r['uptakeA']:.0f} uptakeB={r['uptakeB']:.0f}")

# ---- v3: R-STDP con traza de elegibilidad; sin reflejo, la ruta debe emerger ----
class OrgV3(OrgV2):
    def __init__(s,rng,learn,reflex=0.0,tau_e=0.98,eta=0.02):
        super().__init__(rng,learn,reflex)
        s.elig=np.zeros((N,N)); s.tau_e=tau_e; s.eta=eta
        s.Mprev=0.0
    def step(s,sensin,M):
        inp=s.W@s.S; inp[SENS]=sensin
        s.V+=(-s.V+inp)/s.tauV
        p=1/(1+np.exp(-(s.V-s.thr)/s.noise))
        S_new=(s.rng.random(N)<p).astype(float)
        s.tr=s.tr*0.8+S_new
        if s.learn:
            stdp=np.outer(S_new,s.tr)-0.9*np.outer(s.S,s.tr)
            stdp[SENS,:]=0; np.fill_diagonal(stdp,0)
            s.elig=s.elig*s.tau_e+stdp                  # memoria de quién hizo qué
            dM=max(M-s.Mprev,0.0)                       # aprende con la SUBIDA del modulador
            if dM>0:
                s.W+=s.eta*dM*s.elig*s.sign[None,:]
                s.W=np.where(s.sign[None,:]>0,np.clip(s.W,0,1.5),np.clip(s.W,-1.5,0))
                tot=np.abs(s.W).sum(1); tot[tot==0]=1
                s.W*=(s.norm/tot)[:,None]
            s.Mprev=M
        s.S=S_new
        s.pos=(s.pos+int(S_new[MOT[1]]-S_new[MOT[0]]))%L

def path_strength(o):
    """cuánto apunta sensor izq->motor izq y sensor der->motor der (directo o vía ocultas)"""
    W2=o.W@o.W
    good=o.W[MOT[0],SENS[0]]+o.W[MOT[1],SENS[1]]+W2[MOT[0],SENS[0]]+W2[MOT[1],SENS[1]]
    bad =o.W[MOT[0],SENS[1]]+o.W[MOT[1],SENS[0]]+W2[MOT[0],SENS[1]]+W2[MOT[1],SENS[0]]
    return good-bad
