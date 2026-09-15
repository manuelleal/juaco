import numpy as np
L=40; H=12
PA=np.array([1,1,0,1,0,0.]); PB=np.array([1,0,1,0,1,0.])
def run(seed,T=120000,eta=0.02,tau_e=0.85,learn=True):
    rng=np.random.default_rng(seed); NI=8; NM=3   # motores: izq, der, morder
    W1=rng.uniform(0.1,0.5,(H,NI)); W2=rng.uniform(0.1,0.5,(NM,H)); Wh=rng.uniform(0,0.3,NM)
    e1=np.zeros_like(W1); e2=np.zeros_like(W2); eh=np.zeros(NM); tr=np.zeros(NI); trh=np.zeros(H)
    pos=0; E=1.0; Rbar=0.0; objs={}
    def spawn():
        while len(objs)<4:
            x=int(rng.integers(L))
            if x not in objs: objs[x]='A' if rng.random()<0.5 else 'B'
    spawn(); ateA=[]; ateB=[]; deaths=0
    def see(pos):
        best=None
        for x,k in objs.items():
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        d,k,left=best; pat=PA if k=='A' else PB
        return np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5]])
    for t in range(T):
        hambre=np.clip(1-E,0,1); x=see(pos); noise=0.15+0.6*hambre
        Vh=W1@x+rng.normal(0,noise,H); thr=np.sort(Vh)[-3]
        ph=1/(1+np.exp(-(Vh-thr)/0.2)); h=(Vh>=thr).astype(float)
        V=W2@h+Wh*hambre; p=1/(1+np.exp(-(V-1.0)/noise))
        u=p+rng.normal(0,0.3,NM); m=np.zeros(NM)
        if u.max()>0.5: m[np.argmax(u)]=1
        tr=tr*0.7+x; trh=trh*0.7+h
        if learn:
            e2=e2*tau_e+np.outer(m-p,trh); e1=e1*tau_e+np.outer(h-ph,tr)*(W2.T@(m-p))[:,None]; eh=eh*tau_e+(m-p)*hambre
        pos=(pos+int(m[1]-m[0]))%L
        E-=0.004; R=0.0
        if m[2]==1 and pos in objs:                        # muerde
            if objs[pos]=='A': R=+1.0; E=min(E+0.8,1.5); ateA.append(t)
            else: R=-3.0; E-=0.4; ateB.append(t)
            del objs[pos]; spawn()
        delta=R-Rbar; Rbar=0.99*Rbar+0.01*R
        if learn:
            g=eta*(1+3*hambre)*delta*(3.0 if R<0 else 1.0)
            W2+=g*e2; W1+=g*e1; Wh+=g*eh
            if E<0.3: W1*=0.999; W2*=0.999
            W1=np.clip(W1,0,1.5); W2=np.clip(W2,0,1.5); Wh=np.clip(Wh,0,1.5)
        if E<=0:
            deaths+=1; E=1.0; pos=int(rng.integers(L))
            W1=W1*0.5+rng.uniform(0.1,0.5,(H,NI))*0.5; W2=W2*0.5+rng.uniform(0.1,0.5,(NM,H))*0.5
    a=np.array(ateA); b=np.array(ateB); q=T//4
    f=lambda arr,i:((arr>=i*q)&(arr<(i+1)*q)).sum()
    return [(f(a,i),f(b,i)) for i in range(4)],deaths
for learn in (True,False):
    print("=== "+("APRENDE" if learn else "azar"))
    for s in (1,2,3,4,5):
        qs,d=run(s,learn=learn)
        print(f"  seed {s}: comida/veneno por cuarto: "+"  ".join(f"{a:3d}/{b:3d}" for a,b in qs)+f"   muertes {d}")
