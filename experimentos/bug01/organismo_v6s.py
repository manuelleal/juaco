"""organismo_v6s = organismo_v6.py (5f38f83cf49248a3) + instrumentacion de 3 fases.
Generado por construye_ahorro.py. NO editar a mano.
Con revertir_en=None y sin_B=None es bit-identico a v6 (control 1 de corre_ahorro.py).
Preregistro: PREREGISTRO_ahorro.md
"""
"""
Organismo v6 — consolidación de todo lo aprendido (Etapas 1–2, 2A..2K).
Mecanismos: patas apetitivas/curiosas con R-STDP; boca separada con expansión Kenyon (30 celdas, 3 ganadoras),
canales apetitivo/aversivo separados, error de predicción por estímulo (Rescorla-Wagner), política alpha*valor + 2*hambre + 0.5,
percepción sincronizada (la boca mira lo que pisa), muerte del cuerpo sin olvido, mundo con renovación.
Escenarios: invertir_en (A<->B), nuevo (estímulo C/D en t=nuevo_en con valencia dada y solapamiento forzado con B).
"""
import numpy as np
L=40; NK=30; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}

def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,revertir_en=None,sin_B=None,crit_miedo=-2.5):
    rng=np.random.default_rng(seed)
    Wl=rng.uniform(.1,.4,(2,9)); KW=rng.uniform(0,1,(NK,6))
    def code(P): return set(np.argsort(KW@P)[-K:])
    cond=lambda: len(code(PAT['A'])&code(PAT['B']))==0 and (nuevo is None or solap_B is None or (len(code(PAT[nuevo])&code(PAT['B']))==solap_B and len(code(PAT[nuevo])&code(PAT['A']))==0))
    while not cond(): KW=rng.uniform(0,1,(NK,6))
    def kenyon(P): k=np.zeros(NK); k[list(code(P))]=1; return k
    Wp=np.zeros(NK); Wn=np.zeros(NK); el=np.zeros_like(Wl); tr=np.zeros(9)
    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}
    nB=0; nB3=0; n1=None; n3=None; wB_ext=None; wB_pre=None; wB_post=None   # <-- prueba de ahorro
    tipos=['A','B']
    def spawn():
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]
    spawn()
    q=lambda t:min(t//(T//4),3)
    mord={k:[0]*4 for k in PAT}; vis={k:[0]*4 for k in PAT}; deaths=0; log=[]
    def see():
        best=None
        for x,k in objs.items():
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        return best
    for t in range(T):
        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}
        if revertir_en is not None and t==revertir_en: val={'A':'comida','B':'veneno'}; wB_ext=float((Wp-Wn)@kenyon(PAT['B']))
        if sin_B is not None and t==sin_B[0]:
            wB_pre=float((Wp-Wn)@kenyon(PAT['B'])); tipos=[z for z in tipos if z!='B']
            for z in [z for z,kz in list(objs.items()) if kz=='B']: del objs[z]
            spawn()
        if sin_B is not None and t==sin_B[1]:
            wB_post=float((Wp-Wn)@kenyon(PAT['B']))
            if 'B' not in tipos: tipos.append('B')
        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val
        hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k]
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.
        R=0.
        if pos in objs:
            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn
            Vb=alpha*(Wb@kc)+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1
                del objs[pos]; spawn()
                if learn:
                    dlt=R-Wb@kc
                    if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)
                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)
                if kk=='B':
                    nB+=1; wb=float((Wp-Wn)@kenyon(PAT['B']))
                    if revertir_en is not None and t>=revertir_en: nB3+=1
                    if n1 is None and (invertir_en is None or t<invertir_en) and wb<=crit_miedo: n1=nB
                    if n3 is None and revertir_en is not None and t>=revertir_en and wb<=crit_miedo: n3=nB3
        E-=costo
        if rng.random()<.003 and objs: del objs[list(objs)[int(rng.integers(len(objs)))]]; spawn()
        if learn: Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(float((Wp-Wn)@kenyon(PAT[k])),2) for k in 'ABCD'))
    W={k:round(float((Wp-Wn)@kenyon(PAT[k])),2) for k in PAT}
    comp={k:(round(float(Wp@kenyon(PAT[k])),2),round(float(Wn@kenyon(PAT[k])),2)) for k in PAT}
    return dict(nB=nB,nB3=nB3,n1=n1,n3=n3,wB_ext=wB_ext,wB_pre=wB_pre,wB_post=wB_post,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None})
