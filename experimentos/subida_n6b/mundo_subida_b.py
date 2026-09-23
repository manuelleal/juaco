"""mundo_subida_b = mundo_subida.py (484e34db8f2150da) + el DELTA v13 -> v14.2 copiado de organismo_v142.py (17528d767fcebaf6)
+ perilla vista (M tambien se escribe con lo que la retina ve a un paso) + prueba metas2 (dos comidas en el
mundo partido). Generado por experimentos/subida_n6b/construye_subida_b.py. NO editar.
ANCLAS: perillas apagadas -> mundo_subida BIT A BIT; kwargs del tronco con el mundo apagado -> organismo_v142 BIT A BIT
(identidad_subida_b.py). Memoria nueva persistente: cero."""
"""mundo_subida = mundo_muralla.py (6e515713c86d8bf4) + tres perillas de LECTURA de la misma tabla M:
grad (signo del gradiente local del campo), filtro (el veneno recordado no es objetivo de la retina) y
brujula (CONTROL: el veneno recordado no bloquea la difusion). El organismo v13 NO cambia. Memoria nueva persistente: cero.
Generado por experimentos/subida_n6/construye_subida.py. ANCLA: con grad=filtro=brujula=0 es mundo_muralla BIT A BIT
(identidad_subida.py). NO editar."""
"""mundo_muralla = mundo_2d.py (24da4ab1644eb92a) + el mundo que OBLIGA a rodear
(prueba=dict(modo='muralla',...): fila completa de veneno recordado menos UN hueco, comida al otro lado)
+ perilla camino (lectura de la MISMA tabla M por difusion local: el veneno recordado BLOQUEA el camino)
+ perilla placebo (k sorteos por decision, descartados). El organismo NO cambia. Generado por construye_muralla.py.
ANCLA: con camino=0, placebo=0 y prueba sin modo 'muralla' es mundo_2d BIT A BIT (identidad_muralla.py). NO editar."""
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
        ancho=None,alto=1,camino=0,placebo=0,grad=0,filtro=0,brujula=0,mask_rel=0,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=0,pat_shuf=0,pat_min=1,desambiguar=0,vista=0,explora=0):   # subida_n6b: perillas de v14.2 (APAGADAS = v13; el runner pasa las del tronco) + vista + explora   # subida_n6: grad=signo del gradiente local de U; filtro=el veneno RECORDADO no es objetivo de la retina; brujula=CONTROL (el veneno recordado no bloquea la difusion)   # muralla: camino=1 lee M por DIFUSION LOCAL (campo derivado, cero memoria nueva persistente); placebo=k consume k sorteos por decision en el episodio y los descarta
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
    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; _ndes=0; _des_t=[]; el=np.zeros_like(Wl); tr=np.zeros(_NF)
    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)
    ncod={}; _ord=[]   # B: evidencia del CODIGO EXACTO (mordidas por codigo) y orden de aparicion
    def _key(_k): return frozenset(np.flatnonzero(_k).tolist())
    def _ev(_k):   # evidencia que LEE la puerta: la propia, o (control) la del codigo vecino en el orden de aparicion
        _q=_key(_k)
        if not pat_shuf: return ncod.get(_q,0)
        if _q not in ncod or len(_ord)<2: return 0
        return ncod[_ord[(_ord.index(_q)+1)%len(_ord)]]
    def _fam(_k):   # B: la puerta. puerta_pat>0 -> evidencia del codigo exacto; si no, celdas consolidadas (v13 EXACTO)
        if puerta_pat: return _ev(_k)>=puerta_pat and int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=pat_min
        return int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta
    mup=np.zeros((NKMAX,6)); mun=np.zeros((NKMAX,6)); zp=np.zeros(NKMAX); zn=np.zeros(NKMAX)   # D: medias de P condicionadas al signo de R, con normalizador
    _Mpat=np.zeros((L,6)); _Mset=np.zeros(L,bool); _VACIO=np.zeros(6)   # mapa: tabla posicion -> ultimo patron visto
    def valor(P):   # v13: el valor que usa la boca. Sin puerta: rapida+lenta (un error). Con puerta: la rapida si el patron le es FAMILIAR, si no la lenta
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)
        return _f+_s if puerta is None else (_f if _fam(_k) else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)
    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}
    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura
    _rech={}; _prev_on=-1   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)
    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; sin_objetivo=[0]*4   # v9: lectura
    tipos=['A','B']
    _SIT={}; _pend={}   # mapa: sitio -> tipo fijo; sitio -> paso en que reaparece
    _rod=prueba if (prueba is not None and prueba.get('modo')=='rodeo') else None   # rodeo: TODA la perilla nueva vive dentro de prueba
    _d2=prueba if (prueba is not None and prueba.get('modo')=='2d') else None   # 2d: TODA la perilla nueva vive dentro de prueba
    _mu=prueba if (prueba is not None and prueba.get('modo')=='muralla') else None   # muralla: TODA la perilla nueva vive dentro de prueba
    _o2=1 if ((_d2 is None and _mu is None) or seed%2) else -1   # 2d: la mitad de las semillas con el mapa REFLEJADO en los dos ejes (equilibra el sesgo motor; no toca el rng)
    _g1=int(_rod.get('g1',5)) if _rod is not None else 0; _g2=int(_rod.get('g2',20)) if _rod is not None else 0   # rodeo: huecos F1->veneno y veneno->F2
    _or=1 if (_rod is None or seed%2) else -1   # rodeo: la mitad de las semillas con el mapa en ESPEJO (equilibra el sesgo motor; no toca el rng)
    if sitios is not None:
        _F0=int(rng.integers(L))
        _relm=lambda _dx,_dy:(_F0%_W+_o2*_dx)%_W+((_F0//_W+_o2*_dy)%_H)*_W   # muralla/2d: coordenada relativa -> celda (con el origen azaroso y el espejo de la semilla)
        if _mu is not None:   # muralla: geometria POR SEMILLA con rng INDEPENDIENTE (no toca el rng del organismo). Fila completa de veneno menos UN hueco + UNA comida al otro lado
            _rg=np.random.default_rng(1000003*int(seed)+7)
            _fx=int(_rg.integers(_W)); _gx=(_fx+int(_rg.integers(2,_W-1)))%_W; _fy=1+int(_rg.integers(max(1,_H//2)))   # hueco a >=2 columnas de la comida: el camino recto de la comida cruza VENENO
            _SIT={_relm(_x,0):'B' for _x in range(_W) if _x!=_gx}; _SIT[_relm(_fx,_fy)]='A'
            if _mu.get('cierre'): _SIT.update({_relm(_x,-int(_mu['cierre'])):'B' for _x in range(_W)})   # subida_n6: SEGUNDA muralla ENTERA en la fila -cierre: el toro queda PARTIDO y el hueco es el UNICO cruce
            if _mu.get('metas2'):   # subida_n6b: DOS comidas (A1 arriba, A2 abajo) en el mundo PARTIDO; geometria con el rng de la GEOMETRIA, condicionada a >= min_salidas de cada clase
                _c5=int(_mu['cierre']); _k2=int(_mu.get('min_salidas',3)); _mg=int(_mu.get('margen',2)); _pm=int(_mu.get('p_max',18))
                def _bfs(_o,_tapa=None):   # instrumento: distancia de camino REAL (el veneno corta el paso), no la del organismo
                    _D={_o:0}; _qq=[_o]
                    for _z in _qq:
                        for _a in range(_NA):
                            _n=_mov(_z,_a)
                            if _n in _D or _SIT.get(_n)=='B' or _n==_tapa: continue
                            _D[_n]=_D[_z]+1; _qq.append(_n)
                    return _D
                for _it in range(1000):
                    if _it: _fx=int(_rg.integers(_W)); _gx=(_fx+int(_rg.integers(2,_W-1)))%_W; _fy=1+int(_rg.integers(max(1,_H//2)))
                    _a2x=int(_rg.integers(_W)); _a2y=-1-int(_rg.integers(_c5-1))
                    _SIT={_relm(_x,0):'B' for _x in range(_W) if _x!=_gx}; _SIT.update({_relm(_x,-_c5):'B' for _x in range(_W)})
                    _A1=_relm(_fx,_fy); _A2=_relm(_a2x,_a2y); _SIT[_A1]='A'; _SIT[_A2]='A'; _HU=_relm(_gx,0)
                    _D1=_bfs(_A1); _D2=_bfs(_A2); _BA=set(_bfs(_A1,_HU)); _CL={'cruza':[],'desvia':[]}
                    for _c in range(L):
                        if _c in _SIT or _c==_HU or _c not in _D1: continue
                        _p1=_D1[_c]; _p2=_D2[_c]
                        if _p1+_mg<=_p2: _F,_Fo,_pf=_A1,_A2,_p1
                        elif _p2+_mg<=_p1: _F,_Fo,_pf=_A2,_A1,_p2
                        else: continue
                        if _pf>_pm: continue
                        _mismo=((_F==_A1)==(_c in _BA))
                        if (not _mismo) and _dM(_c,_F)<_pf: _CL['cruza'].append((_c,_F,_Fo,_pf))
                        if _mismo and _dM(_c,_Fo)<_dM(_c,_F): _CL['desvia'].append((_c,_F,_Fo,_pf))
                    if len(_CL['cruza'])>=_k2 and len(_CL['desvia'])>=_k2: break
                else: raise RuntimeError('metas2: sin geometria valida en 1000 tiradas')
                for _cs2 in _CL: _CL[_cs2]=[_CL[_cs2][int(_j)] for _j in _rg.permutation(len(_CL[_cs2]))]   # orden de las salidas: rng de la geometria
        elif _d2 is not None: _SIT={(_F0%_W+_o2*_dx)%_W+((_F0//_W+_o2*_dy)%_H)*_W:kk for (_dx,_dy),kk in zip(_d2['xy'],sitios)}   # 2d: sitios por coordenadas relativas al origen azaroso
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
    _Uc=[None]   # muralla: campo DERIVADO de M (no persiste: se invalida cuando M o el valor cambian y se recalcula por relajacion local)
    _Nb=[None,False]   # subida_n6: celdas recordadas con valor<0 y si hay META (alguna celda recordada con valor>0); DERIVADO de M, se recalcula con U; no persiste
    def _campo():   # muralla: difusion local del valor recordado. U[comida]=valor; el veneno recordado NO propaga (bloquea el camino); U[vecino]=max(U[vecino],disc_M*U[q]) hasta H_M ondas
        _U=np.full(L,-1e18); _bl=np.zeros(L,bool); _fr=[]; _ng=_Nb[0]=np.zeros(L,bool)   # subida_n6: _ng = veneno recordado
        for _i in np.flatnonzero(_Mset if not explora else (_Mset&_Mpat.any(1))):   # subida_n6b: lo VACIO conocido no es objeto: ni bloquea ni atrae (valor() no se consulta)
            _v=valor(_Mpat[int(_i)])
            if _v<0: _bl[int(_i)]=(not brujula); _U[int(_i)]=_v; _ng[int(_i)]=True   # subida_n6: brujula=1 (CONTROL) el veneno recordado NO bloquea la difusion
        for _i in np.flatnonzero(_Mset if not explora else (_Mset&_Mpat.any(1))):   # subida_n6b: lo VACIO conocido no es objeto: ni bloquea ni atrae (valor() no se consulta)
            _v=valor(_Mpat[int(_i)])
            if _v>0: _U[int(_i)]=_v; _bl[int(_i)]=False; _fr.append(int(_i))
        _Nb[1]=len(_fr)>0   # subida_n6: hay META recordada (sin meta, el filtro no actua: evita el bloqueo de una comida que empezo mala)
        for _h in range(H_M):
            _nf=[]
            for _q in _fr:
                _w=disc_M*_U[_q]
                for _a in range(_NA):
                    _n=_mov(_q,_a)
                    if _bl[_n] or _w<=_U[_n]: continue
                    _U[_n]=_w; _nf.append(_n)
            if not _nf: break
            _fr=_nf
        return _U
    def _sesgo_M(_p=None):   # 2d: con la retina vacia, valor recordado por direccion, descontado por distancia toroidal
        _q=pos if _p is None else _p; _b=[0.0]*_NA
        if camino:   # muralla: el veneno recordado BLOQUEA el camino (no repele el acercamiento). Misma tabla M, misma valor(), misma gamma_M/disc_M/H_M
            if _Uc[0] is None: _Uc[0]=_campo()
            _U=_Uc[0]
            for _a in range(_NA):
                _n=_mov(_q,_a); _b[_a]=(0.0 if _U[_n]<-1e17 else float(_U[_n]))
            if grad: _u0=(0.0 if _U[_q]<-1e17 else float(_U[_q])); return gamma_M*np.sign(np.array(_b)-_u0)   # subida_n6: sube por el campo (signo de U[vecino]-U[aqui]); misma gamma_M
            return gamma_M*np.array(_b)
        for _c in sorted((int(_i) for _i in np.flatnonzero(_Mset)),key=lambda _i:_dM(_q,int(_i))):   # por distancia creciente: mismo orden de suma que el anillo
            _h=_dM(_q,_c)
            if _h<1 or _h>H_M: continue
            if explora and not _Mpat[_c].any(): continue   # subida_n6b: lo vacio conocido no suma
            _v=valor(_Mpat[_c])
            for _a in range(_NA):
                if _dM(_mov(_q,_a),_c)==_h-1: _b[_a]+=disc_M**_h*_v   # esa accion me ACERCA a lo recordado (empate -> cuenta en las dos, como el antipodal del anillo)
        return gamma_M*np.array(_b)
    def _obst(_x):   # subida_n6: el veneno RECORDADO es obstaculo, no objetivo (misma M, misma valor())
        if _Uc[0] is None: _Uc[0]=_campo()
        return bool(_Nb[1] and _Nb[0][_x])   # solo con META recordada: sin meta todo lo visible sigue siendo objetivo (v9)
    q=lambda t:min(t//(T//4),3)
    split_t=[]; mord={k:[0]*4 for k in PAT}; vis={k:[0]*4 for k in PAT}; deaths=0; log=[]
    def see(contar=False):
        best=None
        for x,k in objs.items():
            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo
            if filtro and _obst(x): continue   # subida_n6: el veneno recordado no es objetivo
            _d,_s=_ret(x)   # 2d: distancia toroidal Manhattan y direccion preferida
            if r_vis is not None and _d>r_vis: continue   # mapa: fuera de la vista
            if best is None or _d<best[0]: best=(_d,k,_s)   # 2d: empate de distancia -> el primero de objs, como en el anillo
        if best is None:   # v9: todo filtrado -> regla original (fallback)
            if contar: sin_objetivo[q(t)]+=1
            for x,k in objs.items():
                if filtro and _obst(x): continue   # subida_n6: tampoco en el fallback v9 (si no, el veneno recordado vuelve a ser objetivo)
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
        if vista and usa_M and escribe_M and k!='vacio' and d==1:   # subida_n6b VISTA: lo que la retina ve a UN paso se escribe en M (celda exacta: pos + direccion de la retina). Misma tabla, mismo PAT. Solo en la vida
            _xv=_mov(pos,left)
            if not (_Mset[_xv] and bool((_Mpat[_xv]==PAT[k]).all())): _Mpat[_xv]=PAT[k]; _Mset[_xv]=True; _Uc[0]=None   # solo si cambia (el campo derivado se invalida)
        x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i==left else 0 for _i in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre   # 2d: un bit por direccion
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,_NA); m=np.zeros(_NA)
        if usa_M and k=='vacio':   # mapa: solo desempata sin senal directa
            if explora and hambre<=0: u=u+gamma_M*np.array([0.0 if _Mset[_mov(pos,_a)] else 1.0 for _a in range(_NA)])   # subida_n6b EXPLORA: SACIADO (E>=1), sube hacia la celda vecina que el mapa NO conoce (aprendizaje latente); con hambre, lee el campo
            else: u=u+_sesgo_M()
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        pos=(_mov(pos,int(np.argmax(m))) if m.any() else pos); d2,_,_=see(); Rp=.2 if (d is not None and d2 is not None and d2<d) else 0.   # 2d
        if explora and usa_M and escribe_M and not _Mset[pos] and pos not in objs: _Mset[pos]=True; _Mpat[pos]=_VACIO   # subida_n6b EXPLORA: la celda pisada y vacia queda CONOCIDA (misma tabla M, patron vacio; no cambia el campo: ver _campo)
        R=0.
        if pos in objs:
            if usa_M and escribe_M: _Mpat[pos]=PAT[objs[pos]]; _Mset[pos]=True; _Uc[0]=None   # mapa: recuerda lo que vio aqui (muralla: el campo derivado se invalida)
            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=float((Wps-Wns)@PAT[kk])   # v13: las dos vias
            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)
            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1; _Uc[0]=None   # muralla: morder cambia valor() -> el campo derivado se invalida
                _ky=_key(kc)
                if _ky not in ncod: _ord.append(_ky)
                ncod[_ky]=ncod.get(_ky,0)+1   # B: evidencia del codigo exacto
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
                        if R>0: mup[idx]=(1-ema_c)*mup[idx]+ema_c*P; zp[idx]=(1-ema_c)*zp[idx]+ema_c   # D
                        elif R<0: mun[idx]=(1-ema_c)*mun[idx]+ema_c*P; zn[idx]=(1-ema_c)*zn[idx]+ema_c   # D
                        err_max=max(err_max,float(err[idx].max()))
                        for c in idx:
                            if div_signo:   # v11 (JUACO-EVO gen1/llm_2): divide por CONFLICTO DE SIGNO, hija ciega fuera de P, madre fija, fision del valor
                                dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])
                                if mask_rel==2 and zp[c]>1e-6 and zn[c]>1e-6:   # D: HIJA DISPERSA (contexto O discriminador)
                                    _mp=mup[c]/float(zp[c]); _mn=mun[c]/float(zn[c])
                                    _rel=(P>0)&((np.abs(_mp-_mn)>del_s)|(np.minimum(_mp,_mn)>1.0-del_c))
                                else: _rel=(P>0)
                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*_rel
                                if (Wb[c]*R<0 or (desambiguar and R==0)) and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():
                                    j=int(np.where(~activa)[0][0]); activa[j]=True; KW[j]=kj
                                    if R>0: Wp[j]=Wp[c]; Wn[j]=0.; Wp[c]=0.
                                    elif R<0: Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.
                                    else: Wp[j]=0.; Wn[j]=0.; _ndes+=1; _des_t.append((t,kk))   # B-5: con R==0 la hija nace SIN valor (no hay signo nuevo que llevarse) y la madre conserva el suyo
                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
                                    mup[j]=mup[c].copy(); mun[j]=mun[c].copy(); zp[j]=zp[c]; zn[j]=zn[c]   # D: la hija hereda las medias condicionadas
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
    elif _mu is not None and _mu.get('metas2'):   # subida_n6b: DOS comidas recordadas, una a cada lado del mundo partido. Elegir la mas cercana POR CAMINO y llegar sin pisar. Sin aprendizaje y sin boca. El organismo NO cambia
        if _mu.get('barajar'):   # control: el valor permutado entre celdas y entre pixeles
            _pi=rng.permutation(NKMAX); Wp=Wp[_pi]; Wn=Wn[_pi]; _pj=rng.permutation(6); Wps=Wps[_pj]; Wns=Wns[_pj]
        if _mu.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps   # control decisivo: el valor con el signo cambiado
        _Uc[0]=None; _M0=(_Mpat.copy(),_Mset.copy())
        _vA=float(valor(PAT['A'])); _vB=float(valor(PAT['B']))
        _COM=sorted(_x for _x,_k in _SIT.items() if val[_k]=='comida'); _VEN=sorted(_x for _x,_k in _SIT.items() if val[_k]=='veneno'); _SCOM=set(_COM)
        _pl=int(placebo); _cas=[]; _nn=0; _ciego=0; _NP=int(_mu.get('max_pasos',60))
        for _i in range(_mu.get('n_tel',40)):
            _cs='cruza' if _i%2==0 else 'desvia'
            _S,_F,_Fo,_pf=_CL[_cs][(_i//2)%len(_CL[_cs])]
            _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]; _Uc[0]=None
            pos=_S; E=_mu.get('E_test',0.3); tr=np.zeros(_NF); _rech.clear()
            for _x in list(_pend): del _pend[_x]
            spawn(); _d0=_dM(pos,_F); _dmx=_d0; _pisa=0; _come=-1; _mv=0; _s=-1
            for _s in range(_NP):
                if _pl: rng.random(_pl)   # PLACEBO: misma ley, otra trayectoria
                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k] if k!='vacio' else _VACIO
                if _s==0 and k=='vacio': _ciego+=1
                x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i2==left else 0 for _i2 in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre
                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,_NA); m=np.zeros(_NA)
                if usa_M and k=='vacio': u=u+_sesgo_M()
                if u.max()>.5: m[np.argmax(u)]=1
                if not m.any(): continue
                _mv+=1; pos=_mov(pos,int(np.argmax(m)))
                if pos in _SIT and val[_SIT[pos]]=='veneno': _pisa+=1   # pisar es mas estricto que morder
                _dmx=max(_dmx,_dM(pos,_F))
                if pos in _SCOM: _come=pos; break   # la PRIMERA comida alcanzada es la eleccion
            if _mv==0: _nn+=1
            _cas.append(dict(caso=_cs,S=int(_S),F=int(_F),otra=int(_Fo),p0=int(_pf),d0=int(_d0),pisa=int(_pisa),come=int(_come>=0),
                             elige=int(_come==_F),a_la_otra=int(_come==_Fo),limpio=int(_come==_F and _pisa==0),
                             huye=int(_come<0 and _dmx>=_d0+2),pasos=int(_s+1),mov=int(_mv)))
        _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]; _Uc[0]=None   # el mapa que se devuelve (M_llenas) es el del ENTRENAMIENTO
        def _fm(_cs,_f):
            _v=[_f(_c) for _c in _cas if _c['caso']==_cs]
            return (round(sum(_v)/len(_v),3),len(_v)) if _v else (None,0)
        _css=['cruza','desvia']
        _tel=dict(modo='metas2',rejilla=[int(_W),int(_H)],orientacion=int(_o2),camino=int(camino),placebo=int(_pl),
                  limpio={_c:_fm(_c,lambda _z:_z['limpio'])[0] for _c in _css},n={_c:_fm(_c,lambda _z:_z['limpio'])[1] for _c in _css},
                  elige={_c:_fm(_c,lambda _z:_z['elige'])[0] for _c in _css},a_la_otra={_c:_fm(_c,lambda _z:_z['a_la_otra'])[0] for _c in _css},
                  come={_c:_fm(_c,lambda _z:_z['come'])[0] for _c in _css},pisa={_c:_fm(_c,lambda _z:int(_z['pisa']>0))[0] for _c in _css},
                  huye={_c:_fm(_c,lambda _z:_z['huye'])[0] for _c in _css},pasos={_c:_fm(_c,lambda _z:_z['pasos'])[0] for _c in _css},
                  pasos_cens={_c:_fm(_c,lambda _z:(_z['pasos'] if _z['limpio'] else _NP))[0] for _c in _css},
                  n_salidas={_c:len(_CL[_c]) for _c in _css},sin_mover=_nn,ciego_al_llegar=_ciego,v_A=round(_vA,3),v_B=round(_vB,3),
                  geo=dict(fx=int(_fx),gx=int(_gx),fy=int(_fy),A1=int(_A1),A2=int(_A2),intentos=int(_it)+1),n_ven=len(_VEN),n_com=len(_COM),
                  M_comida=int(sum(1 for _x in _COM if _Mset[_x])),M_veneno=int(sum(1 for _x in _VEN if _Mset[_x])),
                  sitios={int(_x):kk for _x,kk in _SIT.items()},casos=_cas)
    elif _mu is not None:   # muralla: la comida recordada al OTRO LADO de una muralla de veneno recordado con UN hueco. Sin aprendizaje y sin boca. El organismo NO cambia: decide _sesgo_M
        if _mu.get('barajar'):   # control: el valor permutado entre celdas y entre pixeles (misma cantidad de empuje, sin informacion)
            _pi=rng.permutation(NKMAX); Wp=Wp[_pi]; Wn=Wn[_pi]; _pj=rng.permutation(6); Wps=Wps[_pj]; Wns=Wns[_pj]
        if _mu.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps   # control decisivo: el valor con el signo cambiado (la puerta, |Wp-Wn|, no cambia)
        _Uc[0]=None; _M0=(_Mpat.copy(),_Mset.copy())
        _vA=float(valor(PAT['A'])); _vB=float(valor(PAT['B']))
        _COM=sorted(_x for _x,_k in _SIT.items() if val[_k]=='comida'); _VEN=sorted(_x for _x,_k in _SIT.items() if val[_k]=='veneno')
        _F=_COM[0] if _COM else int(rng.integers(L)); _pl=int(placebo); _cas=[]; _nn=0; _ciego=0
        for _i in range(_mu.get('n_tel',40)):
            _cs='rodeo' if _i%2==0 else 'atajo'   # rodeo: arranca ALINEADO con la comida (el camino recto cruza veneno). atajo: arranca alineado con el HUECO (el camino recto esta limpio)
            _dd=1+(_i//2)%int(_mu.get('d_ini',3))   # distancia inicial a la muralla, por el lado contrario a la comida
            _S=_relm(_fx if _cs=='rodeo' else _gx,-_dd)
            _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]; _Uc[0]=None
            pos=_S; E=_mu.get('E_test',0.3); tr=np.zeros(_NF); _rech.clear()
            for _x in list(_pend): del _pend[_x]
            spawn(); _d0=_dM(pos,_F); _dmx=_d0; _pisa=0; _come=0; _mv=0; _s=-1
            for _s in range(_mu.get('max_pasos',60)):
                if _pl: rng.random(_pl)   # PLACEBO: misma ley, otra trayectoria (control negativo del instrumento)
                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k] if k!='vacio' else _VACIO
                if _s==0 and k=='vacio': _ciego+=1
                x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i2==left else 0 for _i2 in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre
                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,_NA); m=np.zeros(_NA)
                if usa_M and k=='vacio': u=u+_sesgo_M()
                if u.max()>.5: m[np.argmax(u)]=1
                if not m.any(): continue
                _mv+=1; pos=_mov(pos,int(np.argmax(m)))
                if pos in _SIT and val[_SIT[pos]]=='veneno': _pisa+=1   # pisar es mas estricto que morder: no se consulta la boca
                _dmx=max(_dmx,_dM(pos,_F))
                if pos==_F: _come=1; break
            if _mv==0: _nn+=1
            _cas.append(dict(caso=_cs,S=int(_S),d0=int(_d0),pisa=int(_pisa),come=int(_come),pasos=int(_s+1),
                             limpio=int(_come==1 and _pisa==0),recto=int(_come==1 and _pisa==0 and (_s+1)<=_d0+2),
                             huye=int(_come==0 and _dmx>=_d0+2),dmax=int(_dmx),mov=int(_mv)))
        _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]; _Uc[0]=None   # el mapa que se devuelve (M_llenas) es el del ENTRENAMIENTO
        def _fm(_cs,_f):
            _v=[_f(_c) for _c in _cas if _c['caso']==_cs]
            return (round(sum(_v)/len(_v),3),len(_v)) if _v else (None,0)
        _css=['rodeo','atajo']
        _tel=dict(modo='muralla',rejilla=[int(_W),int(_H)],orientacion=int(_o2),camino=int(camino),placebo=int(_pl),
                  limpio={_c:_fm(_c,lambda _z:_z['limpio'])[0] for _c in _css},n={_c:_fm(_c,lambda _z:_z['limpio'])[1] for _c in _css},
                  come={_c:_fm(_c,lambda _z:_z['come'])[0] for _c in _css},
                  pisa={_c:_fm(_c,lambda _z:int(_z['pisa']>0))[0] for _c in _css},
                  huye={_c:_fm(_c,lambda _z:_z['huye'])[0] for _c in _css},
                  recto={_c:_fm(_c,lambda _z:_z['recto'])[0] for _c in _css},
                  pasos={_c:_fm(_c,lambda _z:_z['pasos'])[0] for _c in _css},
                  pasos_cens={_c:_fm(_c,lambda _z:(_z['pasos'] if _z['limpio'] else int(_mu.get('max_pasos',60))))[0] for _c in _css},
                  sin_mover=_nn,ciego_al_llegar=_ciego,v_A=round(_vA,3),v_B=round(_vB,3),
                  geo=dict(fx=int(_fx),gx=int(_gx),fy=int(_fy)),F=int(_F),n_ven=len(_VEN),
                  M_comida=int(sum(1 for _x in _COM if _Mset[_x])),M_veneno=int(sum(1 for _x in _VEN if _Mset[_x])),
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
    return dict(desambiguar=desambiguar,des_splits=_ndes,des_t=_des_t,sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=len(ncod),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None},W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],
                tel=_tel,M_llenas=int(_Mset.sum()))   # mapa
