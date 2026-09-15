import numpy as np
L=40
def run(seed,T=60000,eta=0.02,tau_e=0.8,vida=True,verbose=False):
    rng=np.random.default_rng(seed)
    W=rng.uniform(0.2,0.6,(2,2)); Wh=rng.uniform(0.0,0.3,2)   # Wh: hambre->motores
    elig=np.zeros((2,2)); eligh=np.zeros(2); trS=np.zeros(2)
    pos=0; food={int(rng.integers(L))}; E=1.0
    eaten=[]; deaths=0; route=[]; Rbar=0.0
    def sens(pos):
        x=next(iter(food)); dl=(pos-x)%L; dr=(x-pos)%L
        return np.array([1.5 if dl<dr else 0.0,1.5 if dr<dl else 0.0]),min(dl,dr)
    for t in range(T):
        hambre=np.clip(1-E,0,1) if vida else 0.0
        s,d=sens(pos)
        V=W@s+Wh*hambre
        noise=0.15+0.6*hambre if vida else 0.15          # hambre -> explora
        p=1/(1+np.exp(-(V-0.5)/noise))
        # inhibición mutua: solo un motor puede ganar
        u=p+rng.normal(0,0.3,2); m=np.zeros(2)
        if u.max()>0.5: m[np.argmax(u)]=1
        trS=trS*0.8+s
        elig=elig*tau_e+np.outer(m-p,trS)               # crédito relativo a lo esperado
        eligh=eligh*tau_e+(m-p)*hambre
        pos=(pos+int(m[1]-m[0]))%L
        s2,d2=sens(pos); R=0.3 if d2<d else 0.0
        E-=0.004 if vida else 0.0                       # vivir cuesta
        if pos in food:
            R+=1.0; E=min(E+0.8,1.5); food.clear(); food.add(int(rng.integers(L))); eaten.append(t)
        delta=R-Rbar; Rbar=0.99*Rbar+0.01*R             # error de predicción
        gain=(1+3*hambre) if vida else 1.0
        if R>0 or vida:
            W+=eta*gain*delta*elig; Wh+=eta*gain*delta*eligh
        if vida and E<0.3: W*=0.999                    # costo metabólico: muriendo, poda
        W=np.clip(W,0,1.5); Wh=np.clip(Wh,0,1.5)
        if vida and E<=0:                               # muerte: pierde parte de lo aprendido
            deaths+=1; E=1.0; W=W*0.5+rng.uniform(0.2,0.6,(2,2))*0.5; pos=int(rng.integers(L))
        if t%10000==0: route.append(W[0,0]+W[1,1]-W[0,1]-W[1,0])
    e=np.array(eaten); q=T//4
    return (e<q).sum(),(e>=3*q).sum(),len(e),deaths,route,W
for vida in (False,True):
    print("=== "+("CON vida y muerte" if vida else "sin vida (regla de ayer + inhibición mutua)"))
    for s in (1,2,3,4,5,6):
        a,b,tot,dth,r,W=run(s,vida=vida)
        print(f"  seed {s}: 1er cuarto {a:3d} -> último {b:3d}  total {tot:4d} muertes {dth:2d}  ruta: "+" ".join(f"{x:+.2f}" for x in r))
