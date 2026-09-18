"""mundo_2d = mundo_mapa_rodeo.py (7ab34aed9acffaa0) = mundo_mapa.py (207d6a1954336b18) + rejilla TOROIDAL
ancho x alto (4 direcciones, retina del objeto mas cercano en distancia Manhattan toroidal, tabla M de posicion 2D)
+ UNA prueba nueva: prueba=dict(modo='2d', ...). El organismo NO cambia. Generado por construye_2d.py. NO editar.
ANCLA: con alto=1 es mundo_mapa BIT A BIT, y con modo='rodeo' es mundo_mapa_rodeo BIT A BIT (identidad obligatoria,
identidad_2d.py). modo='rodeo' solo esta definido con alto=1 (su geometria es la del anillo)."""
"""mundo_mapa_rodeo = mundo_mapa.py (207d6a1954336b18) + UNA prueba nueva: prueba=dict(modo='rodeo', ...)
(dos metas recordadas y rodeo largo cuando el camino corto pasa por veneno recordado). El organismo NO cambia.
Generado por construye_rodeo.py. NO editar. Sin modo='rodeo' es mundo_mapa exacto (identidad obligatoria)."""
"""mundo_mapa = organismo_v13.py (cc8b16b492d4d324) + vision limitada r_vis + sitios fijos con regeneracion + tabla M
(posicion -> ultimo patron visto) con simulacion hacia adelante + prueba de teletransporte. Generado por construye_mapa.py.
NO editar. Con r_vis=None, sitios=None, usa_M=False, prueba=None es organismo_v13 exacto (identidad obligatoria)."""
"""
Organismo v13 — CANDIDATO A TRONCO (congelable solo si pasa PREREGISTRO_tronco_v13.md): v11 + VIA LENTA lineal
sobre la retina + PUERTA de familiaridad. Punto confirmado en semillas 61-80: eta_s=0.015, puerta=3
(datos v13_dos_vias_20260917_160541: retencion 20/20, acierto en patrones nunca vistos 0.850, E1/E2/E2L 20/20).

Dos vias con UN solo error (esquema CLS minimo): la rapida es v11 sin tocar (Kenyon + division por conflicto de
signo); la lenta es una lectura lineal directa de los 6 pixeles con dos canales Wps/Wns (>=0, tope clip_s) a tasa
eta_s < eta, con el mismo drenaje de la parte comun. Cada via aprende de SU error. La boca consulta la rapida solo
si el patron le es FAMILIAR (>= puerta de las 3 celdas de su codigo con |Wp-Wn|>0.2, el umbral de v11); si no,
consulta la lenta, que aprende la regla y no los casos. Con eta_s=0 y puerta=None es v11 EXACTO.
Linaje: ... -> v9 (d3b72fb8819fbe8e) -> v10 (219d5033fe15b5b9, instrumento) -> v11 (f69e24063be1b194) -> v13.
Generado por experimentos/v13_dos_vias/construye_v13_tronco.py (a partir del genoma explorado). NO editar a mano.
"""
import numpy as np
L=40; L0=40; NK=30; NKMAX=90; K=3   # 2d: L0 = ancho por defecto (el ANILLO del tronco, L=40)
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}

def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.015,clip_s=3.0,puerta=3,
        r_vis=None,sitios=None,regen=50,usa_M=False,escribe_M=True,gamma_M=0.6,H_M=20,disc_M=0.9,prueba=None,
        ancho=None,alto=1):   # 2d: rejilla toroidal ancho x alto; con alto=1 y ancho=None es el ANILLO del tronco, bit a bit
    rng=np.random.default_rng(seed)
    _W=L0 if ancho is None else int(ancho); _H=int(alto); L=_W*_H   # 2d: la posicion sigue siendo un indice PLANO: x=pos%_W, y=pos//_W
    _NA=2 if _H==1 else 4   # 2d: acciones. Anillo: (izq,der). Rejilla: (izq,der,arriba,abajo)
    _NF=7+_NA   # 2d: rasgos = 6 pixeles + un bit por direccion + contacto (con _NA=2 son los 9 del tronco)
    _PAS=((-1,0),(1,0),(0,-1),(0,1))[:_NA]   # 2d: desplazamiento de cada accion
    def _dM(a,b):   # 2d: distancia toroidal Manhattan (con _H=1 es min((a-b)%L,(b-a)%L), la del anillo)
        _ax,_ay=a%_W,a//_W; _bx,_by=b%_W,b//_W
        return min((_ax-_bx)%_W,(_bx-_ax)%_W)+min((_ay-_by)%_H,(_by-_ay)%_H)
    def _mov(c,a):   # 2d: un paso en la direccion a (con _H=1: (c-1)%L y (c+1)%L)
        _dx,_dy=_PAS[a]; return (c%_W+_dx)%_W+((c//_W+_dy)%_H)*_W
    def _ret(c):   # 2d: (distancia, direccion preferida) del objeto c. EJE dominante (empate -> x); dentro del eje, el lado corto (empate -> der/abajo, igual que el dl<dr del anillo)
        _ax,_ay=pos%_W,pos//_W; _bx,_by=c%_W,c//_W
        _li=(_ax-_bx)%_W; _de=(_bx-_ax)%_W; _dx=min(_li,_de); _ar=(_ay-_by)%_H; _ab=(_by-_ay)%_H; _dy=min(_ar,_ab)
        return _dx+_dy,((0 if _li<_de else 1) if _dx>=_dy else (2 if _ar<_ab else 3))
    Wl=rng.uniform(.1,.4,(_NA,_NF)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(PAT[nuevo])&code(PAT['B']))==solap_B and len(code(PAT[nuevo])&code(PAT['A']))==0))
    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(_NF)
    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)
    _Mpat=np.zeros((L,6)); _Mset=np.zeros(L,bool); _VACIO=np.zeros(6)   # mapa: tabla posicion -> ultimo patron visto
    def valor(P):   # v13: el valor que usa la boca. Sin puerta: rapida+lenta (un error). Con puerta: la rapida si el patron le es FAMILIAR, si no la lenta
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)
        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)
    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}
    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura
    _rech={}; _prev_on=-1   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)
    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; sin_objetivo=[0]*4   # v9: lectura
    tipos=['A','B']
    _SIT={}; _pend={}   # mapa: sitio -> tipo fijo; sitio -> paso en que reaparece
    _rod=prueba if (prueba is not None and prueba.get('modo')=='rodeo') else None   # rodeo: TODA la perilla nueva vive dentro de prueba
    _d2=prueba if (prueba is not None and prueba.get('modo')=='2d') else None   # 2d: TODA la perilla nueva vive dentro de prueba
    _o2=1 if (_d2 is None or seed%2) else -1   # 2d: la mitad de las semillas con el mapa REFLEJADO en los dos ejes (equilibra el sesgo motor; no toca el rng)
    _g1=int(_rod.get('g1',5)) if _rod is not None else 0; _g2=int(_rod.get('g2',20)) if _rod is not None else 0   # rodeo: huecos F1->veneno y veneno->F2
    _or=1 if (_rod is None or seed%2) else -1   # rodeo: la mitad de las semillas con el mapa en ESPEJO (equilibra el sesgo motor; no toca el rng)
    if sitios is not None:
        _F0=int(rng.integers(L))
        if _d2 is not None: _SIT={(_F0%_W+_o2*_dx)%_W+((_F0//_W+_o2*_dy)%_H)*_W:kk for (_dx,_dy),kk in zip(_d2['xy'],sitios)}   # 2d: sitios por coordenadas relativas al origen azaroso
        elif _rod is None: _SIT={(_F0+i*(L//len(sitios)))%L:kk for i,kk in enumerate(sitios)}
        else: _SIT={_F0%L:sitios[0],(_F0+_or*_g1)%L:sitios[1],(_F0+_or*(_g1+_g2))%L:sitios[2]}   # rodeo: F1 en F0, veneno a g1, F2 a g1+g2
    def spawn():
        if sitios is not None:   # mapa: los objetos viven en sitios fijos
            for x,kk in _SIT.items():
                if x not in objs and x not in _pend: objs[x]=kk
            return
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]
    spawn()
    def _sesgo_M(_p=None):   # 2d: con la retina vacia, valor recordado por direccion, descontado por distancia toroidal
        _q=pos if _p is None else _p; _b=[0.0]*_NA
        for _c in sorted((int(_i) for _i in np.flatnonzero(_Mset)),key=lambda _i:_dM(_q,int(_i))):   # por distancia creciente: mismo orden de suma que el anillo
            _h=_dM(_q,_c)
            if _h<1 or _h>H_M: continue
            _v=valor(_Mpat[_c])
            for _a in range(_NA):
                if _dM(_mov(_q,_a),_c)==_h-1: _b[_a]+=disc_M**_h*_v   # esa accion me ACERCA a lo recordado (empate -> cuenta en las dos, como el antipodal del anillo)
        return gamma_M*np.array(_b)
    q=lambda t:min(t//(T//4),3)
    split_t=[]; mord={k:[0]*4 for k in PAT}; vis={k:[0]*4 for k in PAT}; deaths=0; log=[]
    def see(contar=False):
        best=None
        for x,k in objs.items():
            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo
            _d,_s=_ret(x)   # 2d: distancia toroidal Manhattan y direccion preferida
            if r_vis is not None and _d>r_vis: continue   # mapa: fuera de la vista
            if best is None or _d<best[0]: best=(_d,k,_s)   # 2d: empate de distancia -> el primero de objs, como en el anillo
        if best is None:   # v9: todo filtrado -> regla original (fallback)
            if contar: sin_objetivo[q(t)]+=1
            for x,k in objs.items():
                _d,_s=_ret(x)   # 2d
                if r_vis is not None and _d>r_vis: continue   # mapa: fuera de la vista
                if best is None or _d<best[0]: best=(_d,k,_s)   # 2d
        return best if best is not None else (None,'vacio',None)   # mapa: nada a la vista
    for t in range(T):
        if _pend:   # mapa: reaparecen en su sitio los objetos maduros
            _mad=[x for x,tt in _pend.items() if tt<=t]
            if _mad:
                for x in _mad: del _pend[x]
                spawn()
        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}
        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val
        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k] if k!='vacio' else _VACIO
        x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i==left else 0 for _i in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre   # 2d: un bit por direccion
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,_NA); m=np.zeros(_NA)
        if usa_M and k=='vacio': u=u+_sesgo_M()   # mapa: solo desempata sin senal directa
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        pos=(_mov(pos,int(np.argmax(m))) if m.any() else pos); d2,_,_=see(); Rp=.2 if (d is not None and d2 is not None and d2<d) else 0.   # 2d
        R=0.
        if pos in objs:
            if usa_M and escribe_M: _Mpat[pos]=PAT[objs[pos]]; _Mset[pos]=True   # mapa: recuerda lo que vio aqui
            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=float((Wps-Wns)@PAT[kk])   # v13: las dos vias
            _wt=_wf+_ws if puerta is None else (_wf if int((np.abs(Wb[kc>0])>0.2).sum())>=puerta else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)
            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1
                if sitios is not None: _pend[pos]=t+regen   # mapa: reaparece en su sitio
                del objs[pos]; spawn()
                _rech.pop(pos,None)   # v9: ese objeto ya no existe
                if learn:
                    dlt=R-_wt if puerta is None else R-_wf   # v13: sin puerta UN error compartido; con puerta cada via el suyo
                    if eta_s:   # v13: actualizacion de la via lenta (su tasa, mismo drenaje)
                        _ds=dlt if puerta is None else R-_ws
                        if lam: _mcs=np.minimum(Wps,Wns)*(PAT[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs
                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*PAT[kk],0,clip_s)
                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)
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
        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas
        E-=costo
        if rng.random()<.003 and objs:
            _dx=list(objs)[int(rng.integers(len(objs)))]
            if sitios is not None: _pend[_dx]=t+regen   # mapa
            del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido
        if learn: Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(PAT[k]),2) for k in 'ABCD'))
    _tel=None
    if _d2 is not None:   # 2d: teletransportes por caso, SIN aprendizaje y SIN boca. El organismo NO cambia: decide _sesgo_M
        if _d2.get('barajar'):   # control: el valor permutado entre celdas y entre pixeles (se reporta, no decide)
            _pi=rng.permutation(NKMAX); Wp=Wp[_pi]; Wn=Wn[_pi]; _pj=rng.permutation(6); Wps=Wps[_pj]; Wns=Wns[_pj]
        if _d2.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps   # control: el valor con el signo cambiado (la puerta, |Wp-Wn|, no cambia)
        _IX={_c:_j for _j,_c in enumerate(_SIT)}; _q2=bool(_d2.get('h2',False)); _bm=bool(_d2.get('borra_M',False))
        _M0=(_Mpat.copy(),_Mset.copy())   # 2d: los 40 teletransportes son pruebas INDEPENDIENTES, asi que el mapa se restaura como E, la traza y los sitios
        _vA=float(valor(PAT['A'])); _vB=float(valor(PAT['B']))   # el valor que la boca ya tenia (tras invertir, si toca)
        def _rel(_dx,_dy): return (_F0%_W+_o2*_dx)%_W+((_F0//_W+_o2*_dy)%_H)*_W   # 2d: coordenada relativa -> celda (con el espejo de la semilla)
        def _QM(_p):   # 2d: horizonte 1 = el mecanismo actual; horizonte 2 = simular UN paso con M y evaluar desde ahi (coste: 1+_NA llamadas a _sesgo_M por paso; memoria: la posicion simulada)
            _b1=_sesgo_M(_p)
            return (_b1,_b1) if not _q2 else (_b1,_b1+disc_M*np.array([float(max(_sesgo_M(_mov(_p,_a)))) for _a in range(_NA)]))
        _cas=[]; _nn=0; _ciego=0
        for _i in range(_d2.get('n_tel',40)):
            _cc=_d2['casos'][_i%len(_d2['casos'])]
            _ok=[(_a if _o2>0 else (_a^1)) for _a in _cc['ok']]   # 2d: con el mapa reflejado, la accion correcta se refleja (0<->1, 2<->3)
            _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]   # 2d: mapa restaurado (solo importa con borra_M, que lo modifica dentro del episodio)
            pos=_rel(*_cc['S']); E=_d2.get('E_test',0.3); tr=np.zeros(_NF); _rech.clear()
            for x in list(_pend): del _pend[x]
            spawn(); _dir=-1; _pisa=0; _come=[]; _b0=None; _s=-1
            for _s in range(_d2.get('max_pasos',60)):
                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k] if k!='vacio' else _VACIO
                if _s==0 and k=='vacio': _ciego+=1
                x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i2==left else 0 for _i2 in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre
                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,_NA); m=np.zeros(_NA)
                if usa_M and k=='vacio':
                    _b1,_b2=_QM(pos)
                    if _b0 is None: _b0=(_b1,_b2)   # el sesgo del PRIMER paso decidido, que es la medida
                    u=u+(_b2 if _q2 else _b1)
                if u.max()>.5: m[np.argmax(u)]=1
                if not m.any(): continue
                if _dir<0: _dir=int(np.argmax(m))   # PRIMER paso: la medida
                pos=_mov(pos,int(np.argmax(m)))
                if pos in _SIT and val[_SIT[pos]]=='veneno': _pisa+=1   # pisar es mas estricto que morder: no se consulta la boca
                if pos in objs and val[objs[pos]]=='comida':
                    _come.append(_IX.get(pos,-1))
                    if not _cc.get('consume'): break
                    del objs[pos]   # secuencia: la comida alcanzada desaparece (no se repone dentro del episodio)
                if _bm and pos not in objs and _Mset[pos]: _Mset[pos]=False   # candidato: el mapa se corrige con lo que veo (sitio recordado y vacio -> se borra)
            if _dir<0: _nn+=1
            _cas.append(dict(et=_cc.get('et',''),S=[int(_cc['S'][0]),int(_cc['S'][1])],primer=int(_dir),
                             acierta=(None if _dir<0 else int(_dir in _ok)),ok=[int(_a) for _a in _ok],
                             mec1=(None if _b0 is None else int(np.argmax(_b0[0]))),mec2=(None if _b0 is None else int(np.argmax(_b0[1]))),
                             B1=(None if _b0 is None else [round(float(_z),4) for _z in _b0[0]]),
                             B2=(None if _b0 is None else [round(float(_z),4) for _z in _b0[1]]),
                             come=[int(_z) for _z in _come],pisa=int(_pisa),pasos=int(_s+1)))
        _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]   # 2d: el mapa que se devuelve (M_llenas) es el del ENTRENAMIENTO, no el que borra_M dejo en el ultimo episodio
        def _fr(_et,_f):
            _v=[_f(_c) for _c in _cas if _c['et']==_et and _f(_c) is not None]
            return (round(sum(_v)/len(_v),3),len(_v)) if _v else (None,0)
        _ets=sorted({_c['et'] for _c in _cas})
        _tel=dict(modo='2d',rejilla=[int(_W),int(_H)],orientacion=int(_o2),h2=int(_q2),borra_M=int(_bm),
                  R={_e:_fr(_e,lambda _c:_c['acierta'])[0] for _e in _ets},n={_e:_fr(_e,lambda _c:_c['acierta'])[1] for _e in _ets},
                  mec1={_e:_fr(_e,lambda _c:(None if _c['mec1'] is None else int(_c['mec1'] in _c['ok'])))[0] for _e in _ets},
                  mec2={_e:_fr(_e,lambda _c:(None if _c['mec2'] is None else int(_c['mec2'] in _c['ok'])))[0] for _e in _ets},
                  sigue_mec1={_e:_fr(_e,lambda _c:(None if (_c['mec1'] is None or _c['primer']<0) else int(_c['primer']==_c['mec1'])))[0] for _e in _ets},
                  llega={_e:_fr(_e,lambda _c:int(len(_c['come'])>0))[0] for _e in _ets},
                  llega_limpio={_e:_fr(_e,lambda _c:int(len(_c['come'])>0 and _c['pisa']==0))[0] for _e in _ets},
                  come2={_e:_fr(_e,lambda _c:int(len(set(_c['come']))>1))[0] for _e in _ets},
                  pisa={_e:_fr(_e,lambda _c:int(_c['pisa']>0))[0] for _e in _ets},
                  pasos={_e:_fr(_e,lambda _c:_c['pasos'])[0] for _e in _ets},
                  sin_mover=_nn,ciego_al_llegar=_ciego,v_A=round(_vA,3),v_B=round(_vB,3),
                  sitios={int(_x):kk for _x,kk in _SIT.items()},casos=_cas)
    elif _rod is not None:   # rodeo: dos metas y rodeo largo, sin aprendizaje. El organismo NO cambia: decide _sesgo_M
        _F1=_F0%L; _VEN=(_F0+_or*_g1)%L; _F2=(_F0+_or*(_g1+_g2))%L; _g3=L-_g1-_g2
        if _rod.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps   # control: el valor con el signo cambiado (la puerta, |Wp-Wn|, no cambia)
        _DP=tuple(_rod.get('dps',(4,5,6,7))); _AA=tuple(_rod.get('aas',(4,5,6,7)))   # rodeo: distancia al veneno / a la comida corta
        _vA=float(valor(PAT[sitios[0]])); _vB=float(valor(PAT[sitios[1]]))   # el valor que la boca ya tenia (tras invertir, si toca)
        _cas=[]; _nn=0; _ciego=0; _pasos=[]
        for i in range(_rod.get('n_tel',40)):
            if i%2==0:   # RODEO esperado: el veneno esta ENTRE S y la comida cercana (F1 a d1); la otra comida (F2) a d2>d1 y limpia
                _dp=_DP[(i//2)%len(_DP)]; _d1=_g1+_dp; _d2=_g2-_dp; _S=(_VEN+_or*_dp)%L; _ok=_or; _cs='rodeo'
            else:        # ATAJO esperado: la comida cercana (F2 a d1) esta LIMPIA; el veneno queda fuera del camino corto, detras de F1
                _aa=_AA[(i//2)%len(_AA)]; _d1=_aa; _d2=_g3-_aa; _dp=_d2+_g1; _S=(_F2+_or*_aa)%L; _ok=-_or; _cs='atajo'
            _bc=_vA*disc_M**_d1+(_vB*disc_M**_dp if _cs=='rodeo' else 0.0)   # lo que suma el lado CORTO
            _bl=_vA*disc_M**_d2+(0.0 if _cs=='rodeo' else _vB*disc_M**_dp)   # lo que suma el lado LARGO
            pos=_S; E=_rod.get('E_test',0.3); tr=np.zeros(_NF); _rech.clear()
            for x in list(_pend): del _pend[x]
            spawn(); _dir=0; _pisa=0; _come=None
            for _s in range(_rod.get('max_pasos',60)):
                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k] if k!='vacio' else _VACIO
                if _s==0 and k=='vacio': _ciego+=1
                x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i==left else 0 for _i in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre   # 2d
                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,_NA); m=np.zeros(_NA)
                if usa_M and k=='vacio': u=u+_sesgo_M()
                if u.max()>.5: m[np.argmax(u)]=1
                if not m.any(): continue
                if _dir==0: _dir=int(m[1]-m[0]); _pasos.append(_s+1)   # PRIMER paso: la medida de R1/R2
                pos=(pos+int(m[1]-m[0]))%L
                if pos==_VEN: _pisa+=1   # piso el veneno (mas estricto que morderlo: no se consulta la boca)
                if pos==_F1 or pos==_F2: _come=('F1' if pos==_F1 else 'F2'); break
            if _dir==0: _nn+=1
            _cas.append(dict(caso=_cs,d1=int(_d1),d2=int(_d2),dp=int(_dp),S=int(_S),lado_ok=int(_ok),primer=int(_dir),
                             acierta=(None if _dir==0 else int(_dir==_ok)),B_corto=round(_bc,4),B_largo=round(_bl,4),
                             mec=int(_bl>_bc),come=_come,pisa=int(_pisa)))
        _rc=[c for c in _cas if c['caso']=='rodeo']; _at=[c for c in _cas if c['caso']=='atajo']
        def _f(cs):
            _v=[c['acierta'] for c in cs if c['acierta'] is not None]
            return (round(sum(_v)/len(_v),3),len(_v)) if _v else (None,0)
        _r1,_n1=_f(_rc); _r2,_n2=_f(_at)
        _lim=[c for c in _cas if c['come'] is not None and c['pisa']==0]
        _tel=dict(modo='rodeo',R1=_r1,R2=_r2,n_rodeo=_n1,n_atajo=_n2,
                  llega_limpio=(round(len(_lim)/len(_cas),3) if _cas else None),
                  llega=(round(sum(c['come'] is not None for c in _cas)/len(_cas),3) if _cas else None),
                  come_F1=sum(c['come']=='F1' for c in _cas),come_F2=sum(c['come']=='F2' for c in _cas),
                  pisa_total=int(sum(c['pisa'] for c in _cas)),sin_mover=_nn,ciego_al_llegar=_ciego,
                  pasos_medio=(round(sum(_pasos)/len(_pasos),2) if _pasos else None),
                  v_A=round(_vA,3),v_B=round(_vB,3),
                  mec_rodeo=(round(sum(c['mec'] for c in _rc)/len(_rc),3) if _rc else None),
                  mec_atajo=(round(sum(1-c['mec'] for c in _at)/len(_at),3) if _at else None),
                  orientacion=int(_or),g=(int(_g1),int(_g2),int(_g3)),F1=int(_F1),V=int(_VEN),F2=int(_F2),
                  sitios={int(x):kk for x,kk in _SIT.items()},casos=_cas)
    elif prueba is not None:   # mapa: prueba de teletransporte, sin aprendizaje
        _Fs=[x for x,kk in _SIT.items() if val[kk]=='comida']; _F=_Fs[0] if _Fs else int(rng.integers(L))
        if prueba.get('barajar'):
            _pi=rng.permutation(NKMAX); Wp=Wp[_pi]; Wn=Wn[_pi]; _pj=rng.permutation(6); Wps=Wps[_pj]; Wns=Wns[_pj]
        if prueba.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps   # control decisivo: el valor con el signo cambiado (la puerta no cambia)
        _ac=[]; _nn=0; _ciego=0; _pasos=[]
        for i in range(prueba.get('n_tel',40)):
            _dn=int(rng.integers(r_vis+1,13)); _lado=-1 if i%2==0 else 1   # la comida queda a _dn casillas hacia _lado
            pos=(_F-_lado*_dn)%L; E=prueba.get('E_test',0.3); tr=np.zeros(_NF); _rech.clear()
            for x in list(_pend): del _pend[x]
            spawn(); _dir=0
            for _s in range(prueba.get('max_pasos',30)):
                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k] if k!='vacio' else _VACIO
                if _s==0 and k=='vacio': _ciego+=1
                x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i==left else 0 for _i in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre   # 2d
                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,_NA); m=np.zeros(_NA)
                if usa_M and k=='vacio': u=u+_sesgo_M()
                if u.max()>.5: m[np.argmax(u)]=1
                if m.any(): _dir=int(m[1]-m[0]); break
            _pasos.append(_s+1)
            if _dir==0: _nn+=1
            else: _ac.append(int(_dir==_lado))
        _tel=dict(acierto=(round(sum(_ac)/len(_ac),3) if _ac else None),n=len(_ac),sin_mover=_nn,ciego_al_llegar=_ciego,
                  pasos_medio=round(sum(_pasos)/len(_pasos),2),F=_F,sitios={int(x):kk for x,kk in _SIT.items()})
    W={k:round(valor(PAT[k]),2) for k in PAT}   # v13: valor total
    W_lenta={k:round(float((Wps-Wns)@PAT[k]),3) for k in PAT}   # v13: lectura de la via lenta sola
    comp={k:(round(float(Wp@kenyon(PAT[k])),2),round(float(Wn@kenyon(PAT[k])),2)) for k in PAT}
    return dict(sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None},W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],
                tel=_tel,M_llenas=int(_Mset.sum()))   # mapa
