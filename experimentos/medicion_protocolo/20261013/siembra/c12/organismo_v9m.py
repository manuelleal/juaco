"""organismo_v9m = organismo/organismo_v9.py (d3b72fb8819fbe8e) + fases de mundo, congelar aprendizaje, herencia de
estado y lectura de primer encuentro y muertes por cuarto. Generado por construye_v9m.py. NO editar.
Con los valores por defecto es v9 exacto. Preregistro: experimentos/etapa4_v9/PREREGISTRO_etapa4_v9.md
"""
"""
Organismo v9 — CANDIDATO a tronco (congelable solo si pasa el confirmatorio de PREREGISTRO_v9.md y bateria_v9.py 20).

v9 = v8 + MEMORIA DE TRABAJO DE RECHAZO: lo que la boca acaba de rechazar deja de ser objetivo de las patas
durante `memoria_rechazo` pasos (20). Con memoria_rechazo=0 es v8 exacto.
Linaje: v6 (5f38f83cf49248a3) -> v7 -> v7e -> v8 (dca7d5c3a162f5d4) -> v9 (este archivo).
Generado por experimentos/v9_memoria_rechazo/construye_v9.py. NO editar a mano.
Preregistro: experimentos/v9_memoria_rechazo/PREREGISTRO_v9.md (f68841597adb55d8).
"""
"""
Organismo v8 — TRONCO candidato (congelable sólo si pasa organismo/bateria_v8.py 20, criterio v3).

v8 = v6 + 2L (plasticidad estructural) + drenaje de la parte común de Wp/Wn con lam=0.05.
Linaje: organismo_v6.py (5f38f83cf49248a3) -> v7c (212f0746d52577c7) -> v7 (3db0475ef0ea95ce)
        -> experimentos/bug01/organismo_v7e.py (3118c6d563542da2) -> v8 (este archivo).
Generado por experimentos/congelacion_v8/construye_v8.py. NO editar a mano.

Único cambio de comportamiento respecto de v7e: lam=0.05 por defecto. Con lam=0 es v7 exacto.
El drenaje resta lam*min(Wp,Wn) a los dos canales al morder: Wp-Wn queda intacto, así que el valor
y la conducta son idénticos a v7 hasta la primera truncación del clip (prueba de coste, S0/C0 20/20),
y a partir de ahí v8 sigue aprendiendo donde v7 se bloquea (BUG-01).

Instrumentación de sólo lectura (no toca RNG ni estado): err_max, t_conflicto, t_techo, n_techo.
OJO (ERR-12): splits>0 <=> err_max>0.6 es una IDENTIDAD del código mientras haya celdas libres.
Preregistro: experimentos/congelacion_v8/PREREGISTRO_congelacion_v8.md (d2924e69128fe0f6).
"""
"""
Organismo v7e = v7 + decaimiento de la PARTE COMUN de Wp/Wn (arreglo candidato 2 de BUG-01). lam=0.0 reproduce v7.
Resta lam*min(Wp,Wn) a AMBOS canales en las celdas activas al morder. Como resta lo mismo a los dos,
**Wp-Wn queda EXACTAMENTE intacto**: el valor neto sigue obedeciendo Rescorla-Wagner puro y no hay sesgo.
Donde no hay conflicto (un solo canal activo) min=0 y la operacion es literalmente inerte.
Ataca la REDUNDANCIA, no la magnitud — que es lo que refuto al experimento 1 (decaimiento uniforme).
Equilibrio derivado: Wp* = K*eta*|dlt_eq|/lam.  Preregistro en experimentos/bug01/PREREGISTRO_exp2.md.

Organismo v7 = v6 + 2L (plasticidad estructural en Kenyon: celda con error de predicción crónico se divide hacia lo distintivo).
Parámetro plast=True/False; solap_AB fuerza solapamiento inicial A∩B (None = 0 como en v6).

Organismo v6 — consolidación de todo lo aprendido (Etapas 1–2, 2A..2K).
Mecanismos: patas apetitivas/curiosas con R-STDP; boca separada con expansión Kenyon (30 celdas, 3 ganadoras),
canales apetitivo/aversivo separados, error de predicción por estímulo (Rescorla-Wagner), política alpha*valor + 2*hambre + 0.5,
percepción sincronizada (la boca mira lo que pisa), muerte del cuerpo sin olvido, mundo con renovación.
Escenarios: invertir_en (A<->B), nuevo (estímulo C/D en t=nuevo_en con valencia dada y solapamiento forzado con B).
"""
import numpy as np
L=40; NK=30; NKMAX=90; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}

def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,fases=None,congelar=None,estado_inicial=None,heredar_patas=True,devolver_estado=False):
    rng=np.random.default_rng(seed)
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(PAT[nuevo])&code(PAT['B']))==solap_B and len(code(PAT[nuevo])&code(PAT['A']))==0))
    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)
    if estado_inicial is not None:   # v9m: herencia (copias; los contadores empiezan en cero)
        KW[:]=estado_inicial['KW']; activa[:]=estado_inicial['activa']; Wp[:]=estado_inicial['Wp']; Wn[:]=estado_inicial['Wn']
        err[:]=estado_inicial['err']; mu[:]=estado_inicial['mu']
        if heredar_patas: Wl[:]=estado_inicial['Wl']
    sondas={}; primer={}; _t_fase=0; dq=[0]*4   # v9m: lectura
    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}
    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura
    _rech={}; _prev_on=-1   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)
    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; sin_objetivo=[0]*4   # v9: lectura
    tipos=['A','B']
    def spawn():
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]
    spawn()
    q=lambda t:min(t//(T//4),3)
    split_t=[]; mord={k:[0]*4 for k in PAT}; vis={k:[0]*4 for k in PAT}; deaths=0; log=[]
    def see(contar=False):
        best=None
        for x,k in objs.items():
            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        if best is None:   # v9: todo filtrado -> regla original (fallback)
            if contar: sin_objetivo[q(t)]+=1
            for x,k in objs.items():
                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
                if best is None or d<best[0]: best=(d,k,dl<dr)
        return best
    for t in range(T):
        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}
        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val
        if fases is not None and t in fases:   # v9m: cambio del conjunto de estimulos
            tipos[:]=list(fases[t][0]); val.update(fases[t][1]); _t_fase=t
            for _x in [_xx for _xx,_kz in list(objs.items()) if _kz not in tipos]: del objs[_x]; _rech.pop(_x,None)
            spawn(); sondas[t]={_k:float((Wp-Wn)@kenyon(PAT[_k])) for _k in PAT}
        _ap=learn and not (congelar is not None and congelar[0]<=t<congelar[1])   # v9m
        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k]
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if _ap: el=el*tau_e+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.
        R=0.
        if pos in objs:
            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn
            Vb=alpha*(Wb@kc)+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)
            if (_t_fase,kk) not in primer: primer[(_t_fase,kk)]=dict(t=t,W=float(Wb@kc),pb=float(pb),mordio=bool(mordio))   # v9m
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1
                del objs[pos]; spawn()
                _rech.pop(pos,None)   # v9: ese objeto ya no existe
                if _ap:
                    dlt=R-Wb@kc
                    if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom   # BUG-01 exp2: decae solo la parte comun
                    _ix=kc>0
                    if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())
                    else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())
                    if _trunca:
                        n_techo+=1
                        if t_techo is None: t_techo=t
                    if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)
                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)
                    if t_conflicto is None and bool((np.minimum(Wp[_ix],Wn[_ix])>0).any()): t_conflicto=t
                    if plast:
                        P=PAT[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P
                        err_max=max(err_max,float(err[idx].max()))
                        for c in idx:
                            if err[c]>theta and (~activa).any():
                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-mu[c]
                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)
                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas
        E-=costo
        if rng.random()<.003 and objs:
            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido
        if _ap: Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L)); dq[q(t)]+=1
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(float((Wp-Wn)@kenyon(PAT[k])),2) for k in 'ABCD'))
    W={k:round(float((Wp-Wn)@kenyon(PAT[k])),2) for k in PAT}
    comp={k:(round(float(Wp@kenyon(PAT[k])),2),round(float(Wn@kenyon(PAT[k])),2)) for k in PAT}
    return dict(sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None},sondas=sondas,primer={f'{_a}|{_b}':_v for (_a,_b),_v in primer.items()},dq=dq,estado=(dict(KW=KW.copy(),activa=activa.copy(),Wp=Wp.copy(),Wn=Wn.copy(),err=err.copy(),mu=mu.copy(),Wl=Wl.copy()) if devolver_estado else None))
