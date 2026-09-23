"""Genera mundo_subida_b.py = experimentos/subida_n6/mundo_subida.py (484e34db8f2150da; organismo v13 + mundo partido +
lectura GF) + DOS cosas, por anclas con conteo exacto:

(O) EL ORGANISMO DEL TRONCO v14.2. Se copia, linea por linea, el DELTA organismo_v13 -> organismo_v142
    (organismo/organismo_v142.py, sha 17528d767fcebaf6, CONGELADO: solo se lee). Cada trozo insertado se verifica
    que aparece TAL CUAL en organismo_v142.py (conteo 1). Perillas nuevas en la firma: mask_rel, del_s, del_c, ema_c,
    puerta_pat, pat_shuf, pat_min, desambiguar, con DEFECTOS APAGADOS (los de v13: mask_rel=0, puerta_pat=0,
    desambiguar=0; eta_s=0.015 y clip_s=3.0 no se tocan). El runner pasa los defectos de organismo_v142.run leidos con
    inspect (regla 14). Identidades obligatorias (identidad_subida_b.py):
      I-13 : perillas apagadas               -> mundo_subida.run BIT A BIT (todas las claves)
      I-142: kwargs del tronco, mundo apagado -> organismo_v142.run BIT A BIT (todas las claves de v14.2)

(W) TRES perillas de mundo/lectura (vista, explora, metas2):
    vista=1  : el mapa se escribe TAMBIEN con lo que la retina ve a UN paso (d == 1): la celda es exacta (pos + la
               direccion de la retina), el patron es el que la retina ve. Misma tabla M, mismo PAT; solo en la VIDA (la
               prueba lee el mapa de la vida, como subida_n6). Motivo: V1 cayo en subida_n6 (19/20, 15/20) porque M solo se
               escribia PISANDO; y en 3 semillas de la replica (6629, 6632, 6639) la muralla incompleta dejo pasar el campo
               y GF no rodeo (0.0). Celulas de vector de objeto (Hoydal et al. 2019, Nature 568:400). Memoria nueva: CERO.
    prueba['metas2']=True (modo muralla): DOS comidas, A1 en la banda de arriba (la de subida_n6) y A2 en la banda de
               abajo, en el mundo partido (cierre). Salidas en las DOS bandas, clasificadas por BFS sobre el mundo REAL
               (instrumento, no organismo):
                 cruza : la comida mas cercana POR CAMINO (margen >= 2) esta al OTRO lado; la linea recta cruza veneno
                         (Manhattan < camino): hay que rodear por el hueco.
                 desvia: la mas cercana por camino esta del MISMO lado, pero la del otro lado esta mas cerca en linea
                         recta (trampa: una brujula va a la otra y pisa la muralla).
               Geometria sorteada con el rng de la geometria (1000003*seed+7, no el del organismo), condicionada a que
               haya >= min_salidas salidas de cada clase; la primera tirada usa el mismo (fx, gx, fy) de subida_n6.
    explora=1: SACIADO (hambre == 0, E >= 1) y con la retina vacia, el organismo sube hacia la celda vecina que el mapa
               NO conoce (sesgo gamma_M, la misma constante del mapa); con hambre lee el campo como en subida_n6. La celda
               pisada y vacia queda CONOCIDA en la misma tabla M (patron vacio); lo vacio no entra al campo (_campo lo
               salta) y valor() no se consulta sobre el. En la prueba E_test = 0.3 -> hambre 0.7: explora NO actua en la
               prueba. Motivo: en la primera depuracion (semilla del arnes 14644) la vista sola no completo el mapa (el
               organismo solo iba y venia a la comida: 1/2 comidas y 6/21 venenos en M). Aprendizaje latente: Tolman y
               Honzik (1930); Tolman (1948). Memoria nueva: CERO; constantes nuevas: CERO.
    Sin metas2 y con vista=0, explora=0 el mundo es el de subida_n6.
MEMORIA NUEVA PERSISTENTE: CERO. NO editar mundo_subida_b.py a mano.
Uso: python experimentos/subida_n6b/construye_subida_b.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'subida_n6', 'mundo_subida.py')
SHA_ORIGEN = '484e34db8f2150da'
TRONCO = os.path.join(RAIZ, 'organismo', 'organismo_v142.py')
SHA_TRONCO = '17528d767fcebaf6'
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


# ---------------- (O) delta v13 -> v14.2: cada trozo marcado DEL_TRONCO debe estar tal cual en organismo_v142.py ----------------
DEL_TRONCO = [
    "splits=0; _ndes=0; _des_t=[]; el=np.zeros_like(Wl)",
    NL.join([
        "    ncod={}; _ord=[]   # B: evidencia del CODIGO EXACTO (mordidas por codigo) y orden de aparicion",
        "    def _key(_k): return frozenset(np.flatnonzero(_k).tolist())",
        "    def _ev(_k):   # evidencia que LEE la puerta: la propia, o (control) la del codigo vecino en el orden de aparicion",
        "        _q=_key(_k)",
        "        if not pat_shuf: return ncod.get(_q,0)",
        "        if _q not in ncod or len(_ord)<2: return 0",
        "        return ncod[_ord[(_ord.index(_q)+1)%len(_ord)]]",
        "    def _fam(_k):   # B: la puerta. puerta_pat>0 -> evidencia del codigo exacto; si no, celdas consolidadas (v13 EXACTO)",
        "        if puerta_pat: return _ev(_k)>=puerta_pat and int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=pat_min",
        "        return int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta",
        "    mup=np.zeros((NKMAX,6)); mun=np.zeros((NKMAX,6)); zp=np.zeros(NKMAX); zn=np.zeros(NKMAX)   # D: medias de P condicionadas al signo de R, con normalizador"]),
    "(_f if _fam(_k) else _s)",
    "(_wf if _fam(kc) else _ws)",
    NL.join([
        "                _ky=_key(kc)",
        "                if _ky not in ncod: _ord.append(_ky)",
        "                ncod[_ky]=ncod.get(_ky,0)+1   # B: evidencia del codigo exacto"]),
    NL.join([
        "                        if R>0: mup[idx]=(1-ema_c)*mup[idx]+ema_c*P; zp[idx]=(1-ema_c)*zp[idx]+ema_c   # D",
        "                        elif R<0: mun[idx]=(1-ema_c)*mun[idx]+ema_c*P; zn[idx]=(1-ema_c)*zn[idx]+ema_c   # D"]),
    NL.join([
        "                                if mask_rel==2 and zp[c]>1e-6 and zn[c]>1e-6:   # D: HIJA DISPERSA (contexto O discriminador)",
        "                                    _mp=mup[c]/float(zp[c]); _mn=mun[c]/float(zn[c])",
        "                                    _rel=(P>0)&((np.abs(_mp-_mn)>del_s)|(np.minimum(_mp,_mn)>1.0-del_c))",
        "                                else: _rel=(P>0)",
        "                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*_rel"]),
    "if (Wb[c]*R<0 or (desambiguar and R==0)) and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():",
    NL.join([
        "                                    elif R<0: Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.",
        "                                    else: Wp[j]=0.; Wn[j]=0.; _ndes+=1; _des_t.append((t,kk))   # B-5: con R==0 la hija nace SIN valor (no hay signo nuevo que llevarse) y la madre conserva el suyo"]),
    "                                    mup[j]=mup[c].copy(); mun[j]=mun[c].copy(); zp[j]=zp[c]; zn[j]=zn[c]   # D: la hija hereda las medias condicionadas",
    "return dict(desambiguar=desambiguar,des_splits=_ndes,des_t=_des_t,sobre=sobre,",
    "celdas=int(activa.sum()),puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=len(ncod),",
]
D = DEL_TRONCO

PARCHES_O = [
    ("ancho=None,alto=1,camino=0,placebo=0,grad=0,filtro=0,brujula=0):",
     "ancho=None,alto=1,camino=0,placebo=0,grad=0,filtro=0,brujula=0,mask_rel=0,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=0,pat_shuf=0,pat_min=1,desambiguar=0,vista=0,explora=0):   # subida_n6b: perillas de v14.2 (APAGADAS = v13; el runner pasa las del tronco) + vista + explora",
     1, 'firma'),
    ("splits=0; el=np.zeros_like(Wl)", D[0], 1, 'O2 _ndes'),
    ("    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)",
     "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)" + NL + D[1],
     1, 'O3 puerta PATC'),
    ("(_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)", D[2], 1, 'O4 valor'),
    ("(_wf if int((np.abs(Wb[kc>0])>0.2).sum())>=puerta else _ws)", D[3], 1, 'O5 boca'),
    ("                if sitios is not None: _pend[pos]=t+regen   # mapa: reaparece en su sitio",
     D[4] + NL + "                if sitios is not None: _pend[pos]=t+regen   # mapa: reaparece en su sitio",
     1, 'O6 ncod'),
    ("mu[idx]=(1-ema)*mu[idx]+ema*P",
     "mu[idx]=(1-ema)*mu[idx]+ema*P" + NL + D[5], 1, 'O7 mup'),
    ("                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*(P>0)", D[6], 1, 'O8 hija dispersa'),
    ("if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():", D[7], 1, 'O9 B-5'),
    ("                                    else:   Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.", D[8], 1, 'O10 B-5'),
    ("mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))",
     "mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))" + NL + D[9], 1, 'O11 herencia'),
    ("return dict(sobre=sobre,", D[10], 1, 'O12 salida'),
    ("celdas=int(activa.sum()),", D[11], 1, 'O13 salida'),
]

# ---------------- (W) vista + metas2 ----------------
VISTA = NL.join([
    "        if vista and usa_M and escribe_M and k!='vacio' and d==1:   # subida_n6b VISTA: lo que la retina ve a UN paso se escribe en M (celda exacta: pos + direccion de la retina). Misma tabla, mismo PAT. Solo en la vida",
    "            _xv=_mov(pos,left)",
    "            if not (_Mset[_xv] and bool((_Mpat[_xv]==PAT[k]).all())): _Mpat[_xv]=PAT[k]; _Mset[_xv]=True; _Uc[0]=None   # solo si cambia (el campo derivado se invalida)",
])

GEO2 = NL.join([
    "            if _mu.get('metas2'):   # subida_n6b: DOS comidas (A1 arriba, A2 abajo) en el mundo PARTIDO; geometria con el rng de la GEOMETRIA, condicionada a >= min_salidas de cada clase",
    "                _c5=int(_mu['cierre']); _k2=int(_mu.get('min_salidas',3)); _mg=int(_mu.get('margen',2)); _pm=int(_mu.get('p_max',18))",
    "                def _bfs(_o,_tapa=None):   # instrumento: distancia de camino REAL (el veneno corta el paso), no la del organismo",
    "                    _D={_o:0}; _qq=[_o]",
    "                    for _z in _qq:",
    "                        for _a in range(_NA):",
    "                            _n=_mov(_z,_a)",
    "                            if _n in _D or _SIT.get(_n)=='B' or _n==_tapa: continue",
    "                            _D[_n]=_D[_z]+1; _qq.append(_n)",
    "                    return _D",
    "                for _it in range(1000):",
    "                    if _it: _fx=int(_rg.integers(_W)); _gx=(_fx+int(_rg.integers(2,_W-1)))%_W; _fy=1+int(_rg.integers(max(1,_H//2)))",
    "                    _a2x=int(_rg.integers(_W)); _a2y=-1-int(_rg.integers(_c5-1))",
    "                    _SIT={_relm(_x,0):'B' for _x in range(_W) if _x!=_gx}; _SIT.update({_relm(_x,-_c5):'B' for _x in range(_W)})",
    "                    _A1=_relm(_fx,_fy); _A2=_relm(_a2x,_a2y); _SIT[_A1]='A'; _SIT[_A2]='A'; _HU=_relm(_gx,0)",
    "                    _D1=_bfs(_A1); _D2=_bfs(_A2); _BA=set(_bfs(_A1,_HU)); _CL={'cruza':[],'desvia':[]}",
    "                    for _c in range(L):",
    "                        if _c in _SIT or _c==_HU or _c not in _D1: continue",
    "                        _p1=_D1[_c]; _p2=_D2[_c]",
    "                        if _p1+_mg<=_p2: _F,_Fo,_pf=_A1,_A2,_p1",
    "                        elif _p2+_mg<=_p1: _F,_Fo,_pf=_A2,_A1,_p2",
    "                        else: continue",
    "                        if _pf>_pm: continue",
    "                        _mismo=((_F==_A1)==(_c in _BA))",
    "                        if (not _mismo) and _dM(_c,_F)<_pf: _CL['cruza'].append((_c,_F,_Fo,_pf))",
    "                        if _mismo and _dM(_c,_Fo)<_dM(_c,_F): _CL['desvia'].append((_c,_F,_Fo,_pf))",
    "                    if len(_CL['cruza'])>=_k2 and len(_CL['desvia'])>=_k2: break",
    "                else: raise RuntimeError('metas2: sin geometria valida en 1000 tiradas')",
    "                for _cs2 in _CL: _CL[_cs2]=[_CL[_cs2][int(_j)] for _j in _rg.permutation(len(_CL[_cs2]))]   # orden de las salidas: rng de la geometria",
])

PRUEBA2 = NL.join([
    "    elif _mu is not None and _mu.get('metas2'):   # subida_n6b: DOS comidas recordadas, una a cada lado del mundo partido. Elegir la mas cercana POR CAMINO y llegar sin pisar. Sin aprendizaje y sin boca. El organismo NO cambia",
    "        if _mu.get('barajar'):   # control: el valor permutado entre celdas y entre pixeles",
    "            _pi=rng.permutation(NKMAX); Wp=Wp[_pi]; Wn=Wn[_pi]; _pj=rng.permutation(6); Wps=Wps[_pj]; Wns=Wns[_pj]",
    "        if _mu.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps   # control decisivo: el valor con el signo cambiado",
    "        _Uc[0]=None; _M0=(_Mpat.copy(),_Mset.copy())",
    "        _vA=float(valor(PAT['A'])); _vB=float(valor(PAT['B']))",
    "        _COM=sorted(_x for _x,_k in _SIT.items() if val[_k]=='comida'); _VEN=sorted(_x for _x,_k in _SIT.items() if val[_k]=='veneno'); _SCOM=set(_COM)",
    "        _pl=int(placebo); _cas=[]; _nn=0; _ciego=0; _NP=int(_mu.get('max_pasos',60))",
    "        for _i in range(_mu.get('n_tel',40)):",
    "            _cs='cruza' if _i%2==0 else 'desvia'",
    "            _S,_F,_Fo,_pf=_CL[_cs][(_i//2)%len(_CL[_cs])]",
    "            _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]; _Uc[0]=None",
    "            pos=_S; E=_mu.get('E_test',0.3); tr=np.zeros(_NF); _rech.clear()",
    "            for _x in list(_pend): del _pend[_x]",
    "            spawn(); _d0=_dM(pos,_F); _dmx=_d0; _pisa=0; _come=-1; _mv=0; _s=-1",
    "            for _s in range(_NP):",
    "                if _pl: rng.random(_pl)   # PLACEBO: misma ley, otra trayectoria",
    "                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k] if k!='vacio' else _VACIO",
    "                if _s==0 and k=='vacio': _ciego+=1",
    "                x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i2==left else 0 for _i2 in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre",
    "                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,_NA); m=np.zeros(_NA)",
    "                if usa_M and k=='vacio': u=u+_sesgo_M()",
    "                if u.max()>.5: m[np.argmax(u)]=1",
    "                if not m.any(): continue",
    "                _mv+=1; pos=_mov(pos,int(np.argmax(m)))",
    "                if pos in _SIT and val[_SIT[pos]]=='veneno': _pisa+=1   # pisar es mas estricto que morder",
    "                _dmx=max(_dmx,_dM(pos,_F))",
    "                if pos in _SCOM: _come=pos; break   # la PRIMERA comida alcanzada es la eleccion",
    "            if _mv==0: _nn+=1",
    "            _cas.append(dict(caso=_cs,S=int(_S),F=int(_F),otra=int(_Fo),p0=int(_pf),d0=int(_d0),pisa=int(_pisa),come=int(_come>=0),",
    "                             elige=int(_come==_F),a_la_otra=int(_come==_Fo),limpio=int(_come==_F and _pisa==0),",
    "                             huye=int(_come<0 and _dmx>=_d0+2),pasos=int(_s+1),mov=int(_mv)))",
    "        _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]; _Uc[0]=None   # el mapa que se devuelve (M_llenas) es el del ENTRENAMIENTO",
    "        def _fm(_cs,_f):",
    "            _v=[_f(_c) for _c in _cas if _c['caso']==_cs]",
    "            return (round(sum(_v)/len(_v),3),len(_v)) if _v else (None,0)",
    "        _css=['cruza','desvia']",
    "        _tel=dict(modo='metas2',rejilla=[int(_W),int(_H)],orientacion=int(_o2),camino=int(camino),placebo=int(_pl),",
    "                  limpio={_c:_fm(_c,lambda _z:_z['limpio'])[0] for _c in _css},n={_c:_fm(_c,lambda _z:_z['limpio'])[1] for _c in _css},",
    "                  elige={_c:_fm(_c,lambda _z:_z['elige'])[0] for _c in _css},a_la_otra={_c:_fm(_c,lambda _z:_z['a_la_otra'])[0] for _c in _css},",
    "                  come={_c:_fm(_c,lambda _z:_z['come'])[0] for _c in _css},pisa={_c:_fm(_c,lambda _z:int(_z['pisa']>0))[0] for _c in _css},",
    "                  huye={_c:_fm(_c,lambda _z:_z['huye'])[0] for _c in _css},pasos={_c:_fm(_c,lambda _z:_z['pasos'])[0] for _c in _css},",
    "                  pasos_cens={_c:_fm(_c,lambda _z:(_z['pasos'] if _z['limpio'] else _NP))[0] for _c in _css},",
    "                  n_salidas={_c:len(_CL[_c]) for _c in _css},sin_mover=_nn,ciego_al_llegar=_ciego,v_A=round(_vA,3),v_B=round(_vB,3),",
    "                  geo=dict(fx=int(_fx),gx=int(_gx),fy=int(_fy),A1=int(_A1),A2=int(_A2),intentos=int(_it)+1),n_ven=len(_VEN),n_com=len(_COM),",
    "                  M_comida=int(sum(1 for _x in _COM if _Mset[_x])),M_veneno=int(sum(1 for _x in _VEN if _Mset[_x])),",
    "                  sitios={int(_x):kk for _x,kk in _SIT.items()},casos=_cas)",
    "    elif _mu is not None:   # muralla: la comida recordada",
])

EXPLORA_MOTOR = NL.join([
    "        if usa_M and k=='vacio':   # mapa: solo desempata sin senal directa",
    "            if explora and hambre<=0: u=u+gamma_M*np.array([0.0 if _Mset[_mov(pos,_a)] else 1.0 for _a in range(_NA)])   # subida_n6b EXPLORA: SACIADO (E>=1), sube hacia la celda vecina que el mapa NO conoce (aprendizaje latente); con hambre, lee el campo",
    "            else: u=u+_sesgo_M()",
])
EXPLORA_ESCRIBE = "        if explora and usa_M and escribe_M and not _Mset[pos] and pos not in objs: _Mset[pos]=True; _Mpat[pos]=_VACIO   # subida_n6b EXPLORA: la celda pisada y vacia queda CONOCIDA (misma tabla M, patron vacio; no cambia el campo: ver _campo)"

PARCHES_W = [
    ("        for _i in np.flatnonzero(_Mset):",
     "        for _i in np.flatnonzero(_Mset if not explora else (_Mset&_Mpat.any(1))):   # subida_n6b: lo VACIO conocido no es objeto: ni bloquea ni atrae (valor() no se consulta)",
     2, 'X1 campo ignora vacio'),
    ("            _v=valor(_Mpat[_c])",
     "            if explora and not _Mpat[_c].any(): continue   # subida_n6b: lo vacio conocido no suma" + NL + "            _v=valor(_Mpat[_c])", 1, 'X2 sesgo ignora vacio'),
    ("        if usa_M and k=='vacio': u=u+_sesgo_M()   # mapa: solo desempata sin senal directa", EXPLORA_MOTOR, 1, 'X3 explora motor'),
    ("        pos=(_mov(pos,int(np.argmax(m))) if m.any() else pos); d2,_,_=see(); Rp=.2 if (d is not None and d2 is not None and d2<d) else 0.   # 2d",
     "        pos=(_mov(pos,int(np.argmax(m))) if m.any() else pos); d2,_,_=see(); Rp=.2 if (d is not None and d2 is not None and d2<d) else 0.   # 2d" + NL + EXPLORA_ESCRIBE,
     1, 'X4 explora escribe'),
    ("        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k] if k!='vacio' else _VACIO",
     "        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k] if k!='vacio' else _VACIO" + NL + VISTA,
     1, 'W1 vista'),
    ("            if _mu.get('cierre'): _SIT.update({_relm(_x,-int(_mu['cierre'])):'B' for _x in range(_W)})   # subida_n6: SEGUNDA muralla ENTERA en la fila -cierre: el toro queda PARTIDO y el hueco es el UNICO cruce",
     "            if _mu.get('cierre'): _SIT.update({_relm(_x,-int(_mu['cierre'])):'B' for _x in range(_W)})   # subida_n6: SEGUNDA muralla ENTERA en la fila -cierre: el toro queda PARTIDO y el hueco es el UNICO cruce" + NL + GEO2,
     1, 'W2 geometria metas2'),
    ("    elif _mu is not None:   # muralla: la comida recordada", PRUEBA2, 1, 'W3 prueba metas2'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN (mundo_subida.py) sha {h16(ORIGEN)} != {SHA_ORIGEN}")
    if h16(TRONCO) != SHA_TRONCO:
        raise SystemExit(f"TRONCO (organismo_v142.py) sha {h16(TRONCO)} != {SHA_TRONCO}")
    tr = open(TRONCO, encoding='utf-8').read()
    for i, trozo in enumerate(DEL_TRONCO):   # copia desde el origen: cada trozo del delta esta TAL CUAL en el tronco congelado
        c = tr.count(trozo)
        if c != 1:
            raise SystemExit(f"DELTA {i}: el trozo aparece {c} veces en organismo_v142.py (se esperaba 1): {trozo[:70]!r}")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES_O + PARCHES_W:
        s = sust(s, viejo, nuevo, n, et)
    cab = ('"""mundo_subida_b = mundo_subida.py (' + SHA_ORIGEN + ') + el DELTA v13 -> v14.2 copiado de organismo_v142.py (' +
           SHA_TRONCO + ')' + NL + '+ perilla vista (M tambien se escribe con lo que la retina ve a un paso) + prueba metas2 (dos comidas en el' + NL +
           'mundo partido). Generado por experimentos/subida_n6b/construye_subida_b.py. NO editar.' + NL +
           'ANCLAS: perillas apagadas -> mundo_subida BIT A BIT; kwargs del tronco con el mundo apagado -> organismo_v142 BIT A BIT' + NL +
           '(identidad_subida_b.py). Memoria nueva persistente: cero."""' + NL)
    d = os.path.join(AQUI, 'mundo_subida_b.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  origen {os.path.relpath(ORIGEN, RAIZ)} {h16(ORIGEN)}")
    print(f"  tronco {os.path.relpath(TRONCO, RAIZ)} {h16(TRONCO)}  ({len(DEL_TRONCO)} trozos del delta verificados)")
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
