"""Genera mundo_muralla.py = mundo_2d.py (24da4ab1644eb92a) + UN mundo nuevo que OBLIGA a rodear
(prueba=dict(modo='muralla',...)) + UNA lectura nueva de la MISMA tabla M (perilla camino) + placebo.

QUE CAMBIA (y nada mas):
  1) firma: camino=0, placebo=0 (las dos apagadas por defecto).
  2) _mu = prueba si modo=='muralla' (toda la geometria nueva vive DENTRO de prueba, como en 2d/rodeo).
  3) _o2 (espejo por semilla) tambien se aplica en modo muralla.
  4) _SIT en modo muralla: MURALLA de veneno = la FILA COMPLETA (toroidal) menos UN hueco, mas UNA comida al
     otro lado. La geometria (columna del hueco, columna y fila de la comida) se sortea POR SEMILLA con un
     rng INDEPENDIENTE (np.random.default_rng(1000003*seed+7)): no toca el rng del organismo (identidad) y
     mata la trampa de "sitios fijos que se memorizan".
  5) _Uc/_campo: campo de valor por DIFUSION LOCAL sobre M (relajacion U[n] = max(U[n], disc_M*U[q]) entre
     vecinos, con el veneno recordado como celda que NO propaga). Es un array DERIVADO de M: se recalcula
     cuando M o el valor cambian y no persiste nada nuevo. MEMORIA NUEVA PERSISTENTE: CERO.
  6) _sesgo_M con camino=1 devuelve gamma_M*U[vecino] (el veneno recordado BLOQUEA el camino en vez de
     repeler el acercamiento: la lectura que el bloque nivel6_2d dejo escrita como diagnostico).
  7) bloque de episodios modo='muralla' (sin aprendizaje, sin boca), con placebo=k dentro del episodio.

ANCLA DE IDENTIDAD (obligatoria, la corre identidad_muralla.py):
  * con camino=0 y placebo=0 y prueba != modo 'muralla'  ->  mundo_muralla.run == mundo_2d.run BIT A BIT,
    todas las claves (anillo alto=1, rejilla modo='2d', modo='rodeo').
No se anade ni se quita NINGUNA clave de salida en los modos viejos.

Anclas con conteo exacto. NO editar mundo_muralla.py a mano.
Uso: python experimentos/nivel06_rodeo_obligado/construye_muralla.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel6_2d', 'mundo_2d.py')
SHA_ORIGEN = '24da4ab1644eb92a'
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


PARCHES = [
    # 1) firma: dos perillas nuevas, apagadas por defecto
    (["        ancho=None,alto=1):   # 2d: rejilla toroidal ancho x alto; con alto=1 y ancho=None es el ANILLO del tronco, bit a bit"],
     ["        ancho=None,alto=1,camino=0,placebo=0):   # muralla: camino=1 lee M por DIFUSION LOCAL (campo derivado, cero memoria nueva persistente); placebo=k consume k sorteos por decision en el episodio y los descarta"],
     1, 'firma'),

    # 2) _mu y espejo por semilla tambien en muralla
    (["    _d2=prueba if (prueba is not None and prueba.get('modo')=='2d') else None   # 2d: TODA la perilla nueva vive dentro de prueba",
      "    _o2=1 if (_d2 is None or seed%2) else -1   # 2d: la mitad de las semillas con el mapa REFLEJADO en los dos ejes (equilibra el sesgo motor; no toca el rng)"],
     ["    _d2=prueba if (prueba is not None and prueba.get('modo')=='2d') else None   # 2d: TODA la perilla nueva vive dentro de prueba",
      "    _mu=prueba if (prueba is not None and prueba.get('modo')=='muralla') else None   # muralla: TODA la perilla nueva vive dentro de prueba",
      "    _o2=1 if ((_d2 is None and _mu is None) or seed%2) else -1   # 2d: la mitad de las semillas con el mapa REFLEJADO en los dos ejes (equilibra el sesgo motor; no toca el rng)"],
     1, '_mu'),

    # 3) sitios: la muralla por semilla
    (["        if _d2 is not None: _SIT={(_F0%_W+_o2*_dx)%_W+((_F0//_W+_o2*_dy)%_H)*_W:kk for (_dx,_dy),kk in zip(_d2['xy'],sitios)}   # 2d: sitios por coordenadas relativas al origen azaroso"],
     ["        _relm=lambda _dx,_dy:(_F0%_W+_o2*_dx)%_W+((_F0//_W+_o2*_dy)%_H)*_W   # muralla/2d: coordenada relativa -> celda (con el origen azaroso y el espejo de la semilla)",
      "        if _mu is not None:   # muralla: geometria POR SEMILLA con rng INDEPENDIENTE (no toca el rng del organismo). Fila completa de veneno menos UN hueco + UNA comida al otro lado",
      "            _rg=np.random.default_rng(1000003*int(seed)+7)",
      "            _fx=int(_rg.integers(_W)); _gx=(_fx+int(_rg.integers(2,_W-1)))%_W; _fy=1+int(_rg.integers(max(1,_H//2)))   # hueco a >=2 columnas de la comida: el camino recto de la comida cruza VENENO",
      "            _SIT={_relm(_x,0):'B' for _x in range(_W) if _x!=_gx}; _SIT[_relm(_fx,_fy)]='A'",
      "        elif _d2 is not None: _SIT={(_F0%_W+_o2*_dx)%_W+((_F0//_W+_o2*_dy)%_H)*_W:kk for (_dx,_dy),kk in zip(_d2['xy'],sitios)}   # 2d: sitios por coordenadas relativas al origen azaroso"],
     1, 'sitios muralla'),

    # 4) campo por difusion local + lectura nueva de M
    (["    def _sesgo_M(_p=None):   # 2d: con la retina vacia, valor recordado por direccion, descontado por distancia toroidal",
      "        _q=pos if _p is None else _p; _b=[0.0]*_NA"],
     ["    _Uc=[None]   # muralla: campo DERIVADO de M (no persiste: se invalida cuando M o el valor cambian y se recalcula por relajacion local)",
      "    def _campo():   # muralla: difusion local del valor recordado. U[comida]=valor; el veneno recordado NO propaga (bloquea el camino); U[vecino]=max(U[vecino],disc_M*U[q]) hasta H_M ondas",
      "        _U=np.full(L,-1e18); _bl=np.zeros(L,bool); _fr=[]",
      "        for _i in np.flatnonzero(_Mset):",
      "            _v=valor(_Mpat[int(_i)])",
      "            if _v<0: _bl[int(_i)]=True; _U[int(_i)]=_v",
      "        for _i in np.flatnonzero(_Mset):",
      "            _v=valor(_Mpat[int(_i)])",
      "            if _v>0: _U[int(_i)]=_v; _bl[int(_i)]=False; _fr.append(int(_i))",
      "        for _h in range(H_M):",
      "            _nf=[]",
      "            for _q in _fr:",
      "                _w=disc_M*_U[_q]",
      "                for _a in range(_NA):",
      "                    _n=_mov(_q,_a)",
      "                    if _bl[_n] or _w<=_U[_n]: continue",
      "                    _U[_n]=_w; _nf.append(_n)",
      "            if not _nf: break",
      "            _fr=_nf",
      "        return _U",
      "    def _sesgo_M(_p=None):   # 2d: con la retina vacia, valor recordado por direccion, descontado por distancia toroidal",
      "        _q=pos if _p is None else _p; _b=[0.0]*_NA",
      "        if camino:   # muralla: el veneno recordado BLOQUEA el camino (no repele el acercamiento). Misma tabla M, misma valor(), misma gamma_M/disc_M/H_M",
      "            if _Uc[0] is None: _Uc[0]=_campo()",
      "            _U=_Uc[0]",
      "            for _a in range(_NA):",
      "                _n=_mov(_q,_a); _b[_a]=(0.0 if _U[_n]<-1e17 else float(_U[_n]))",
      "            return gamma_M*np.array(_b)"],
     1, 'campo'),

    # 5) invalidacion del campo: al escribir M y al morder (cambia valor())
    (["            if usa_M and escribe_M: _Mpat[pos]=PAT[objs[pos]]; _Mset[pos]=True   # mapa: recuerda lo que vio aqui"],
     ["            if usa_M and escribe_M: _Mpat[pos]=PAT[objs[pos]]; _Mset[pos]=True; _Uc[0]=None   # mapa: recuerda lo que vio aqui (muralla: el campo derivado se invalida)"],
     1, 'invalida M'),
    (["                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1"],
     ["                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1; _Uc[0]=None   # muralla: morder cambia valor() -> el campo derivado se invalida"],
     1, 'invalida valor'),

    # 6) bloque de episodios de la muralla
    (["    elif _rod is not None:   # rodeo: dos metas y rodeo largo, sin aprendizaje. El organismo NO cambia: decide _sesgo_M"],
     ["    elif _mu is not None:   # muralla: la comida recordada al OTRO LADO de una muralla de veneno recordado con UN hueco. Sin aprendizaje y sin boca. El organismo NO cambia: decide _sesgo_M",
      "        if _mu.get('barajar'):   # control: el valor permutado entre celdas y entre pixeles (misma cantidad de empuje, sin informacion)",
      "            _pi=rng.permutation(NKMAX); Wp=Wp[_pi]; Wn=Wn[_pi]; _pj=rng.permutation(6); Wps=Wps[_pj]; Wns=Wns[_pj]",
      "        if _mu.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps   # control decisivo: el valor con el signo cambiado (la puerta, |Wp-Wn|, no cambia)",
      "        _Uc[0]=None; _M0=(_Mpat.copy(),_Mset.copy())",
      "        _vA=float(valor(PAT['A'])); _vB=float(valor(PAT['B']))",
      "        _COM=sorted(_x for _x,_k in _SIT.items() if val[_k]=='comida'); _VEN=sorted(_x for _x,_k in _SIT.items() if val[_k]=='veneno')",
      "        _F=_COM[0] if _COM else int(rng.integers(L)); _pl=int(placebo); _cas=[]; _nn=0; _ciego=0",
      "        for _i in range(_mu.get('n_tel',40)):",
      "            _cs='rodeo' if _i%2==0 else 'atajo'   # rodeo: arranca ALINEADO con la comida (el camino recto cruza veneno). atajo: arranca alineado con el HUECO (el camino recto esta limpio)",
      "            _dd=1+(_i//2)%int(_mu.get('d_ini',3))   # distancia inicial a la muralla, por el lado contrario a la comida",
      "            _S=_relm(_fx if _cs=='rodeo' else _gx,-_dd)",
      "            _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]; _Uc[0]=None",
      "            pos=_S; E=_mu.get('E_test',0.3); tr=np.zeros(_NF); _rech.clear()",
      "            for _x in list(_pend): del _pend[_x]",
      "            spawn(); _d0=_dM(pos,_F); _dmx=_d0; _pisa=0; _come=0; _mv=0; _s=-1",
      "            for _s in range(_mu.get('max_pasos',60)):",
      "                if _pl: rng.random(_pl)   # PLACEBO: misma ley, otra trayectoria (control negativo del instrumento)",
      "                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k] if k!='vacio' else _VACIO",
      "                if _s==0 and k=='vacio': _ciego+=1",
      "                x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i2==left else 0 for _i2 in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre",
      "                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,_NA); m=np.zeros(_NA)",
      "                if usa_M and k=='vacio': u=u+_sesgo_M()",
      "                if u.max()>.5: m[np.argmax(u)]=1",
      "                if not m.any(): continue",
      "                _mv+=1; pos=_mov(pos,int(np.argmax(m)))",
      "                if pos in _SIT and val[_SIT[pos]]=='veneno': _pisa+=1   # pisar es mas estricto que morder: no se consulta la boca",
      "                _dmx=max(_dmx,_dM(pos,_F))",
      "                if pos==_F: _come=1; break",
      "            if _mv==0: _nn+=1",
      "            _cas.append(dict(caso=_cs,S=int(_S),d0=int(_d0),pisa=int(_pisa),come=int(_come),pasos=int(_s+1),",
      "                             limpio=int(_come==1 and _pisa==0),recto=int(_come==1 and _pisa==0 and (_s+1)<=_d0+2),",
      "                             huye=int(_come==0 and _dmx>=_d0+2),dmax=int(_dmx),mov=int(_mv)))",
      "        _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]; _Uc[0]=None   # el mapa que se devuelve (M_llenas) es el del ENTRENAMIENTO",
      "        def _fm(_cs,_f):",
      "            _v=[_f(_c) for _c in _cas if _c['caso']==_cs]",
      "            return (round(sum(_v)/len(_v),3),len(_v)) if _v else (None,0)",
      "        _css=['rodeo','atajo']",
      "        _tel=dict(modo='muralla',rejilla=[int(_W),int(_H)],orientacion=int(_o2),camino=int(camino),placebo=int(_pl),",
      "                  limpio={_c:_fm(_c,lambda _z:_z['limpio'])[0] for _c in _css},n={_c:_fm(_c,lambda _z:_z['limpio'])[1] for _c in _css},",
      "                  come={_c:_fm(_c,lambda _z:_z['come'])[0] for _c in _css},",
      "                  pisa={_c:_fm(_c,lambda _z:int(_z['pisa']>0))[0] for _c in _css},",
      "                  huye={_c:_fm(_c,lambda _z:_z['huye'])[0] for _c in _css},",
      "                  recto={_c:_fm(_c,lambda _z:_z['recto'])[0] for _c in _css},",
      "                  pasos={_c:_fm(_c,lambda _z:_z['pasos'])[0] for _c in _css},",
      "                  pasos_cens={_c:_fm(_c,lambda _z:(_z['pasos'] if _z['limpio'] else int(_mu.get('max_pasos',60))))[0] for _c in _css},",
      "                  sin_mover=_nn,ciego_al_llegar=_ciego,v_A=round(_vA,3),v_B=round(_vB,3),",
      "                  geo=dict(fx=int(_fx),gx=int(_gx),fy=int(_fy)),F=int(_F),n_ven=len(_VEN),",
      "                  M_comida=int(sum(1 for _x in _COM if _Mset[_x])),M_veneno=int(sum(1 for _x in _VEN if _Mset[_x])),",
      "                  sitios={int(_x):kk for _x,kk in _SIT.items()},casos=_cas)",
      "    elif _rod is not None:   # rodeo: dos metas y rodeo largo, sin aprendizaje. El organismo NO cambia: decide _sesgo_M"],
     1, 'bloque muralla'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN (mundo_2d.py) sha {h16(ORIGEN)} != {SHA_ORIGEN}")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_muralla = mundo_2d.py (' + SHA_ORIGEN + ') + el mundo que OBLIGA a rodear' + NL +
           '(prueba=dict(modo=' + chr(39) + 'muralla' + chr(39) + ',...): fila completa de veneno recordado menos UN hueco, comida al otro lado)' + NL +
           '+ perilla camino (lectura de la MISMA tabla M por difusion local: el veneno recordado BLOQUEA el camino)' + NL +
           '+ perilla placebo (k sorteos por decision, descartados). El organismo NO cambia. Generado por construye_muralla.py.' + NL +
           'ANCLA: con camino=0, placebo=0 y prueba sin modo ' + chr(39) + 'muralla' + chr(39) + ' es mundo_2d BIT A BIT (identidad_muralla.py). NO editar."""' + NL)
    d = os.path.join(AQUI, 'mundo_muralla.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
