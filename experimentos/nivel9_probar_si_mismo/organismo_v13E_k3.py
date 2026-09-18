"""organismo_v13E_k3 = organismo_v13p.py (2dbed7ccac4dd736) + dE-TEST FIJO ON por defecto: eta_pred=0.03, ema_pred=0.05,
k_testE=3.0 -- DOSIS preregistrada en PREREGISTRO_dosis_dE.md (mismo mecanismo de organismo_v13E, ganancia
menor). Generado por construye_v13E.py --k 3. NO editar a mano. Con eta_pred=ema_pred=k_testE=0 es
organismo_v13p EXACTO (arnes: identidad_dosis.py)."""
"""organismo_v13p = organismo_v13s (2eaba8dde27f05bd) + predictor de dE del bloque 6 entrando en la BOCA
(k_testE), traza temporal de la sorpresa sobre si mismo e inyeccion desplazada (control MOMENTO), y mord_post.
Linaje: organismo_v13.py (cc8b16b492d4d324) -> organismo_v13s.py (2eaba8dde27f05bd) -> este.
Con TODAS las perillas nuevas apagadas es v13s, y v13s con las suyas apagadas es v13, bit a bit (J1..J6).
ENMIENDA 2: perillas resta_cota (excede la cota de oraculo 2b(1-b)) y resta_lenta (excede una linea base
lenta de la propia sorpresa, ema_lento), y el campo
t_primer_sesgo (latencia del primer sesgo > 0.05 tras la inversion; solo lectura).
Preregistro: experimentos/nivel9_probar_si_mismo/PREREGISTRO_probar_si_mismo.md.
Generado por experimentos/nivel9_probar_si_mismo/construye_probar.py. NO editar a mano.
"""
import numpy as np
L=40; NK=30; NKMAX=90; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}

def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.015,clip_s=3.0,puerta=3,eta_b=0.0,k_auto=0.0,ema_auto=0.0,k_test=0.0,test_fijo=0.0,buf_auto=1000,clip_b=3.0,eta_e=0.0,h_pred=100,buf_e=200,eta_pred=0.03,clip_e=3.0,ema_pred=0.05,k_testE=3.0,n_traza=0,traza_ext=None,desfase=0,k_testM=0.0,resta_cota=False,resta_lenta=False,ema_lento=0.0025):
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
    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)
    Wbr=np.zeros(6); Wbk=np.zeros(NKMAX); Wbh=0.; Wb0=0.   # v13s: AUTOMODELO (SELF) — predice la propia accion desde retina+codigo+HAMBRE
    Wmr=np.zeros(6); Wmk=np.zeros(NKMAX); Wm0=0.           # v13s: control MUNDO — lo mismo SIN hambre (solo el estimulo)
    Whr=np.zeros(6); Whk=np.zeros(NKMAX); Whh=0.; Wh0=0.   # v13s: control H_SHUF — hambre barajada en el tiempo
    _rng_h=np.random.default_rng(seed+800000) if (eta_b or eta_e) else None; _bufh=[]; _bufe=[]   # v13s: RNG PROPIO de los controles (no toca el del organismo)
    _BLO=(-0.9-0.5-hambre_boca)/alpha; _BHI=(0.9-0.5)/alpha   # v13s: banda sensible al hambre, derivada de las constantes
    _LL=np.zeros((4,2)); _HIT=np.zeros((4,2,2)); _NC=np.zeros((2,2)); _aq=[0.]*4; _naq=[0]*4; _encq=[0]*4   # v13s: lecturas [S,M,H,ORACULO] x [dentro,fuera] x [no muerde,muerde]
    _tq=[0.]*4   # v13s: sesgo medio aplicado a la boca por cuarto
    _sbar=0.; _etaq=[0.]*4; _nqm=[0]*4; t_ext_B=None; deaths_post=0   # v13s: sorpresa media sobre si mismo (EMA), factor eta por cuarto EN LOS BOCADOS, y recuperacion tras la inversion (mismo criterio que el bloque 6)
    Wem=np.zeros((2,7)); bem=np.zeros(2); Wes=np.zeros((2,8)); bes=np.zeros(2); bec=np.zeros(2)   # v13s: AUTOMODELO A h PASOS, dos objetivos: [dE, n_bocados]
    Wez=np.zeros((2,8)); bez=np.zeros(2)   # v13s: control SELF_h con el HAMBRE BARAJADA entre ventanas (misma distribucion, momento equivocado)
    _xe=None; _Ee=0.; _nbw=0; _SE=np.zeros((2,4)); _ne=0; _sy=np.zeros(2); _sy2=np.zeros(2)   # v13s: [objetivo] x [CONST, MUNDO, SELF, SELF_SHUF]
    Wpe=np.zeros(6); Wke=np.zeros(NKMAX); _sbarE=0.; _srE=0.   # v13p: predictor de dE (bloque 6, copiado). Aqui NO modula eta: entra en la BOCA
    _trzs=[0.]*max(n_traza,1); _trzn=[0]*max(n_traza,1); _sm=0.   # v13p: traza de s_barra por cubeta y sesgo inyectado (control MOMENTO)
    mord_post={'comida':0,'veneno':0}   # v13p: bocados tras la inversion (P6)
    _fbar=0.; _fS=0.   # v13p (ENMIENDA 2): cota de oraculo 2b(1-b) y su EMA, con la MISMA ema_auto. Inerte si resta_cota=False
    _sbarL=0.   # v13p (ENMIENDA 2): linea base LENTA de la propia sorpresa (ema_lento). Inerte si resta_lenta=False
    t_primer_sesgo=None; _encps=0; _mordps=0   # v13p (ENMIENDA 2): latencia del primer sesgo > 0.05 tras la inversion (solo lectura)
    def valor(P):   # v13: el valor que usa la boca. Sin puerta: rapida+lenta (un error). Con puerta: la rapida si el patron le es FAMILIAR, si no la lenta
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)
        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)
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
        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k]
        if n_traza:   # v13p: traza de la sorpresa sobre si mismo en n_traza cubetas de T/n_traza pasos (solo lectura)
            _ib=min(t*n_traza//T,n_traza-1); _trzs[_ib]+=_sbar; _trzn[_ib]+=1
            if traza_ext is not None: _sm=k_testM*float(traza_ext[(_ib+desfase)%n_traza])   # MOMENTO: el mismo sesgo, desplazado `desfase` cubetas
        if eta_e and t%h_pred==0:   # v13s: AUTOMODELO A h PASOS — cierra la ventana anterior (y = [E(t)-E(t-h), bocados]) y abre otra. SOLO MIDE
            _xs=np.concatenate([pat,[1. if d==0 else 0.],[hambre]])   # [retina(6), sobre un objeto] + HAMBRE (el ultimo SOLO lo ven SELF_h y su control)
            if _xe is not None:
                _xz=_xe.copy(); _bufe.append(_xe[7])
                if len(_bufe)>buf_e: _xz[7]=float(_bufe.pop(int(_rng_h.integers(len(_bufe)))))   # SELF_SHUF: hambre de OTRA ventana
                _ye=np.array([E-_Ee,float(_nbw)])
                _pr=np.stack([bec,Wem@_xe[:7]+bem,Wes@_xe+bes,Wez@_xz+bez],axis=1)   # [objetivo] x [C,M,S,Z]
                _SE+=(_ye[:,None]-_pr)**2; _ne+=1; _sy+=_ye; _sy2+=_ye*_ye
                bec=bec+eta_e*(_ye-_pr[:,0])
                _em=_ye-_pr[:,1]; Wem=Wem+eta_e*np.outer(_em,_xe[:7]); bem=bem+eta_e*_em
                _es=_ye-_pr[:,2]; Wes=Wes+eta_e*np.outer(_es,_xe);     bes=bes+eta_e*_es
                _ez=_ye-_pr[:,3]; Wez=Wez+eta_e*np.outer(_ez,_xz);     bez=bez+eta_e*_ez
            _xe=_xs; _Ee=E; _nbw=0
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.
        R=0.
        if pos in objs:
            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=float((Wps-Wns)@PAT[kk])   # v13: las dos vias
            _wt=_wf+_ws if puerta is None else (_wf if int((np.abs(Wb[kc>0])>0.2).sum())>=puerta else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)
            _sg=(k_test*(max(0.,_sbar-_fbar) if resta_cota else (max(0.,_sbar-_sbarL) if resta_lenta else _sbar)) if k_test else 0.)+(k_testE*_sbarE if k_testE else 0.)+test_fijo+_sm   # v13p: GANAS DE PROBAR — el sesgo de la boca. resta_cota: EXCESO sobre la cota de oraculo 2b(1-b)
            Vb=alpha*_wt+hambre_boca*hambre+.5+_sg; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            if invertir_en is not None and t>=invertir_en and t_primer_sesgo is None:   # v13p (ENMIENDA 2): latencia, solo lectura
                _encps+=1; _mordps+=int(mordio)
                if _sg>0.05: t_primer_sesgo=t
            _sa=0.; _fS=0.
            if eta_b:   # v13s: AUTOMODELO — tres lecturas que SOLO MIDEN (no entran en la decision ni consumen el rng del organismo)
                _hh=hambre
                _bufh.append(hambre)
                if len(_bufh)>buf_auto: _hh=float(_bufh.pop(int(_rng_h.integers(len(_bufh)))))   # H_SHUF: misma distribucion de hambre, momentos equivocados
                _Pb=PAT[kk]
                _bS=1/(1+np.exp(-(float(Wbr@_Pb)+float(Wbk@kc)+Wbh*hambre+Wb0)/.3))
                _bM=1/(1+np.exp(-(float(Wmr@_Pb)+float(Wmk@kc)+Wm0)/.3))
                _bH=1/(1+np.exp(-(float(Whr@_Pb)+float(Whk@kc)+Whh*_hh+Wh0)/.3))
                _y=1. if mordio else 0.; _sa=abs(_y-_bS); _bd=0 if (_BLO<=_wt<=_BHI) else 1; _cl=int(_y); _fS=2.*float(_bS)*(1.-float(_bS))
                for _i,_bb in enumerate((_bS,_bM,_bH,pb)):   # el 4o es el ORACULO: la propia pb que genero la accion (log-loss irreducible)
                    _LL[_i,_bd]-=np.log(max(_bb if _y>0 else 1-_bb,1e-12)); _HIT[_i,_bd,_cl]+=int((_bb>.5)==(_y>0))
                _NC[_bd,_cl]+=1; _aq[q(t)]+=_sa; _naq[q(t)]+=1
                _eS=_y-_bS; _eM=_y-_bM; _eH=_y-_bH
                Wbr=np.clip(Wbr+eta_b*_eS*_Pb,-clip_b,clip_b); Wbk=np.clip(Wbk+eta_b*_eS*kc,-clip_b,clip_b); Wbh=float(np.clip(Wbh+eta_b*_eS*hambre,-clip_b,clip_b)); Wb0=float(np.clip(Wb0+eta_b*_eS,-clip_b,clip_b))
                Wmr=np.clip(Wmr+eta_b*_eM*_Pb,-clip_b,clip_b); Wmk=np.clip(Wmk+eta_b*_eM*kc,-clip_b,clip_b); Wm0=float(np.clip(Wm0+eta_b*_eM,-clip_b,clip_b))
                Whr=np.clip(Whr+eta_b*_eH*_Pb,-clip_b,clip_b); Whk=np.clip(Whk+eta_b*_eH*kc,-clip_b,clip_b); Whh=float(np.clip(Whh+eta_b*_eH*_hh,-clip_b,clip_b)); Wh0=float(np.clip(Wh0+eta_b*_eH,-clip_b,clip_b))
            if ema_auto: _sbar=(1.-ema_auto)*_sbar+ema_auto*_sa; _fbar=(1.-ema_auto)*_fbar+ema_auto*_fS; _sbarL=(1.-ema_lento)*_sbarL+ema_lento*_sa   # v13s: sorpresa media sobre si mismo — usa TODOS los encuentros, no solo los bocados
            _eta=eta*(1.+k_auto*(_sbar if ema_auto else _sa)) if k_auto else eta   # v13s: CURRICULO POR EL CUERPO — la sorpresa sobre SI MISMO modula la tasa de la via rapida
            _encq[q(t)]+=1; _tq[q(t)]+=_sg
            vis[kk][q(t)]+=1
            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1; _nbw+=1; _etaq[q(t)]+=_eta/eta; _nqm[q(t)]+=1; mord_post[val[kk]]+=int(invertir_en is not None and t>=invertir_en)
                del objs[pos]; spawn()
                _rech.pop(pos,None)   # v9: ese objeto ya no existe
                if learn:
                    if eta_pred:   # v13p: predictor de dE (bloque 6): objetivo E_VAL nominal, regla delta, tasa propia
                        _dEp=float(Wpe@PAT[kk])+float(Wke@kc); _ee=E_VAL[val[kk]]-_dEp; _srE=abs(_ee)
                        Wpe=np.clip(Wpe+eta_pred*_ee*PAT[kk],-clip_e,clip_e); Wke=np.clip(Wke+eta_pred*_ee*kc,-clip_e,clip_e)
                        if ema_pred: _sbarE=(1.-ema_pred)*_sbarE+ema_pred*_srE   # causal: lo usa la boca del PROXIMO encuentro
                    dlt=R-_wt if puerta is None else R-_wf   # v13: sin puerta UN error compartido; con puerta cada via el suyo
                    if eta_s:   # v13: actualizacion de la via lenta (su tasa, mismo drenaje)
                        _ds=dlt if puerta is None else R-_ws
                        if lam: _mcs=np.minimum(Wps,Wns)*(PAT[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs
                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*PAT[kk],0,clip_s)
                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)
                    if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom   # BUG-01 exp2: decae solo la parte comun
                    _ix=kc>0
                    if dlt>0: _trunca=bool(((Wp[_ix]+_eta*dlt)>3.0).any())
                    else:     _trunca=bool(((Wn[_ix]+_eta*aversion*(-dlt))>3.0).any())
                    if _trunca:
                        n_techo+=1
                        if t_techo is None: t_techo=t
                    if dlt>0: Wp=np.clip(Wp+_eta*dlt*kc,0,3.)
                    else:     Wn=np.clip(Wn+_eta*aversion*(-dlt)*kc,0,3.)
                    if t_conflicto is None and bool((np.minimum(Wp[_ix],Wn[_ix])>0).any()): t_conflicto=t
                    if plast:
                        P=PAT[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P
                        err_max=max(err_max,float(err[idx].max()))
                        for c in idx:
                            if div_signo:   # v11 (JUACO-EVO gen1/llm_2): divide por CONFLICTO DE SIGNO, hija ciega fuera de P, madre fija, fision del valor
                                dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])
                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*(P>0)
                                if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():
                                    j=int(np.where(~activa)[0][0]); activa[j]=True; KW[j]=kj
                                    if R>0: Wp[j]=Wp[c]; Wn[j]=0.; Wp[c]=0.
                                    else:   Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.
                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
                            elif err[c]>theta and (~activa).any():
                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])   # v10: mu normalizada a la masa del patron
                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)
                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
        if invertir_en is not None and t>=invertir_en and t_ext_B is None and valor(PAT['B'])>=0: t_ext_B=t   # v13p: M1 del bloque 6 (no consume RNG)
        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas
        E-=costo
        if rng.random()<.003 and objs:
            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido
        if learn: Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0:
            deaths+=1; E=.6; pos=int(rng.integers(L))
            if invertir_en is not None and t>=invertir_en: deaths_post+=1   # v13p
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(PAT[k]),2) for k in 'ABCD'))
    W={k:round(valor(PAT[k]),2) for k in PAT}   # v13: valor total
    W_lenta={k:round(float((Wps-Wns)@PAT[k]),3) for k in PAT}   # v13: lectura de la via lenta sola
    comp={k:(round(float(Wp@kenyon(PAT[k])),2),round(float(Wn@kenyon(PAT[k])),2)) for k in PAT}
    return dict(sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None},W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],
                auto_banda=(round(float(_BLO),4),round(float(_BHI),4)),
                t_ext_B=t_ext_B,deaths_post=deaths_post,sbar=round(float(_sbar),5),
                sesgo_boca=[round(_tq[i]/_encq[i],5) if _encq[i] else None for i in range(4)],
                eta_media=[round(_etaq[i]/_nqm[i],4) if _nqm[i] else None for i in range(4)],bocados_q=list(_nqm),
                auto_h=({'n':int(_ne),'h':int(h_pred),
                         'mse':[[round(float(_SE[y,i]/_ne),6) for i in range(4)] for y in range(2)],
                         'r2':[[round(float(1-_SE[y,i]/max(_SE[y,0],1e-12)),4) for i in range(4)] for y in range(2)],
                         'var_y':[round(float(_sy2[y]/_ne-(_sy[y]/_ne)**2),6) for y in range(2)],
                         'media_y':[round(float(_sy[y]/_ne),6) for y in range(2)],
                         'W_hambre':[round(float(Wes[y,7]),4) for y in range(2)],
                         'W_hambre_shuf':[round(float(Wez[y,7]),4) for y in range(2)]} if (eta_e and _ne) else None),
                auto_n=[[int(_NC[b,c]) for c in range(2)] for b in range(2)],
                auto_ll=[[round(float(_LL[i,b]/_NC[b].sum()),4) if _NC[b].sum() else None for b in range(2)] for i in range(4)],
                auto_ba=[[round(float(np.mean([_HIT[i,b,c]/_NC[b,c] for c in range(2) if _NC[b,c]])),4) if _NC[b].sum() else None for b in range(2)] for i in range(4)],
                sorpresa_auto=[round(_aq[i]/_naq[i],4) if _naq[i] else None for i in range(4)],
                encuentros=list(_encq),n_auto=list(_naq),
                W_auto=({k:round(float(1/(1+np.exp(-(float(Wbr@PAT[k])+float(Wbk@kenyon(PAT[k]))+Wb0)/.3))),3) for k in PAT} if eta_b else None),
                Wbh=round(float(Wbh),4),Whh=round(float(Whh),4),Wb0=round(float(Wb0),4),Wm0=round(float(Wm0),4),
                traza_s=([round(_trzs[i]/_trzn[i],6) if _trzn[i] else 0.0 for i in range(n_traza)] if n_traza else None),
                mord_post=mord_post,sbarE=round(float(_sbarE),5),fbar=round(float(_fbar),6),sbarL=round(float(_sbarL),6),
                t_primer_sesgo=t_primer_sesgo,enc_post_hasta_sesgo=_encps,mord_post_hasta_sesgo=_mordps)
