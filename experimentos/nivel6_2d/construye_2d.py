"""Genera mundo_2d.py = mundo_mapa_rodeo.py (7ab34aed9acffaa0) = mundo_mapa.py (207d6a1954336b18) + rejilla TOROIDAL
ancho x alto con 4 direcciones y tabla M de posicion 2D -> patron, mas UNA prueba nueva: prueba=dict(modo='2d', ...).

El ORGANISMO no cambia (ni valor(), ni la boca, ni el aprendizaje): lo que cambia es el MUNDO (rejilla en vez de
anillo), la RETINA (un bit por direccion en vez de dos) y el SESGO del mapa (suma descontada por direccion sobre la
distancia toroidal Manhattan). Toda la geometria de las pruebas vive DENTRO de prueba.

ANCLA DE IDENTIDAD (obligatoria, la corre identidad_2d.py):
  * con alto=1 y ancho=None  ->  mundo_2d.run(seed,**kw) == mundo_mapa.run(seed,**kw) BIT A BIT, todas las claves;
  * con alto=1 y prueba=dict(modo='rodeo',...)  ->  == mundo_mapa_rodeo.run(seed,**kw) BIT A BIT.
Se conserva el ORDEN DE CONSUMO del rng (Wl es (_NA,_NF) = (2,9) con alto=1; el ruido de la politica es
rng.normal(0,.3,_NA)) y el ORDEN DE SUMA en punto flotante del sesgo del mapa (terminos por distancia creciente).
No se anade ni se quita NINGUNA clave de salida.

Anclas con conteo exacto. NO editar mundo_2d.py a mano.
Uso: python experimentos/nivel6_2d/construye_2d.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel6_rodeo', 'mundo_mapa_rodeo.py')
ABUELO = os.path.join(RAIZ, 'experimentos', 'nivel6_mapa', 'mundo_mapa.py')
SHA_ORIGEN = '7ab34aed9acffaa0'
SHA_ABUELO = '207d6a1954336b18'
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


PARCHES = [
    # 1) L0 = ancho por defecto. Hace falta porque L pasa a ser LOCAL de run() (L = ancho*alto).
    (["L=40; NK=30; NKMAX=90; K=3"],
     ["L=40; L0=40; NK=30; NKMAX=90; K=3   # 2d: L0 = ancho por defecto (el ANILLO del tronco, L=40)"], 1, 'L0'),

    # 2) Firma + geometria. Con alto=1 y ancho=None: _W=40, _H=1, L=40, _NA=2, _NF=9 -> Wl (2,9) como el tronco
    #    (mismo consumo del rng en la primera llamada, que es lo que fija todo el resto del flujo).
    (["        r_vis=None,sitios=None,regen=50,usa_M=False,escribe_M=True,gamma_M=0.6,H_M=20,disc_M=0.9,prueba=None):   # mapa",
      "    rng=np.random.default_rng(seed)",
      "    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True"],
     ["        r_vis=None,sitios=None,regen=50,usa_M=False,escribe_M=True,gamma_M=0.6,H_M=20,disc_M=0.9,prueba=None,",
      "        ancho=None,alto=1):   # 2d: rejilla toroidal ancho x alto; con alto=1 y ancho=None es el ANILLO del tronco, bit a bit",
      "    rng=np.random.default_rng(seed)",
      "    _W=L0 if ancho is None else int(ancho); _H=int(alto); L=_W*_H   # 2d: la posicion sigue siendo un indice PLANO: x=pos%_W, y=pos//_W",
      "    _NA=2 if _H==1 else 4   # 2d: acciones. Anillo: (izq,der). Rejilla: (izq,der,arriba,abajo)",
      "    _NF=7+_NA   # 2d: rasgos = 6 pixeles + un bit por direccion + contacto (con _NA=2 son los 9 del tronco)",
      "    _PAS=((-1,0),(1,0),(0,-1),(0,1))[:_NA]   # 2d: desplazamiento de cada accion",
      "    def _dM(a,b):   # 2d: distancia toroidal Manhattan (con _H=1 es min((a-b)%L,(b-a)%L), la del anillo)",
      "        _ax,_ay=a%_W,a//_W; _bx,_by=b%_W,b//_W",
      "        return min((_ax-_bx)%_W,(_bx-_ax)%_W)+min((_ay-_by)%_H,(_by-_ay)%_H)",
      "    def _mov(c,a):   # 2d: un paso en la direccion a (con _H=1: (c-1)%L y (c+1)%L)",
      "        _dx,_dy=_PAS[a]; return (c%_W+_dx)%_W+((c//_W+_dy)%_H)*_W",
      "    def _ret(c):   # 2d: (distancia, direccion preferida) del objeto c. EJE dominante (empate -> x); dentro del eje, el lado corto (empate -> der/abajo, igual que el dl<dr del anillo)",
      "        _ax,_ay=pos%_W,pos//_W; _bx,_by=c%_W,c//_W",
      "        _li=(_ax-_bx)%_W; _de=(_bx-_ax)%_W; _dx=min(_li,_de); _ar=(_ay-_by)%_H; _ab=(_by-_ay)%_H; _dy=min(_ar,_ab)",
      "        return _dx+_dy,((0 if _li<_de else 1) if _dx>=_dy else (2 if _ar<_ab else 3))",
      "    Wl=rng.uniform(.1,.4,(_NA,_NF)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True"], 1, 'firma+geometria'),

    # 3) La traza de elegibilidad tiene un rasgo por entrada de la retina (3 sitios: init, prueba del mapa, prueba del rodeo).
    (["tr=np.zeros(9)"], ["tr=np.zeros(_NF)"], 3, 'traza'),

    # 4) see(): el objeto mas cercano por distancia toroidal Manhattan, y su direccion preferida (one-hot).
    #    Empates de distancia: gana el PRIMERO de objs (orden de insercion), exactamente como en el anillo.
    (["            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo",
      "            if r_vis is not None and min((pos-x)%L,(x-pos)%L)>r_vis: continue   # mapa: fuera de la vista",
      "            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)",
      "            if best is None or d<best[0]: best=(d,k,dl<dr)"],
     ["            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo",
      "            _d,_s=_ret(x)   # 2d: distancia toroidal Manhattan y direccion preferida",
      "            if r_vis is not None and _d>r_vis: continue   # mapa: fuera de la vista",
      "            if best is None or _d<best[0]: best=(_d,k,_s)   # 2d: empate de distancia -> el primero de objs, como en el anillo"], 1, 'see'),
    (["                if r_vis is not None and min((pos-x)%L,(x-pos)%L)>r_vis: continue   # mapa: fuera de la vista",
      "                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)",
      "                if best is None or d<best[0]: best=(d,k,dl<dr)"],
     ["                _d,_s=_ret(x)   # 2d",
      "                if r_vis is not None and _d>r_vis: continue   # mapa: fuera de la vista",
      "                if best is None or _d<best[0]: best=(_d,k,_s)   # 2d"], 1, 'see fallback'),

    # 5) Retina: un bit por direccion (one-hot del lado preferido). Con _NA=2 son los dos bits del tronco:
    #    left=0 -> [1.5,0]; left=1 -> [0,1.5] (incluye contacto y antipodal, que en el anillo daban 'der'); vacio -> [0,0].
    (["        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k] if k!='vacio' else _VACIO",
      "        x=np.concatenate([pat*1.2,[1.5 if left else 0,1.5 if left is False else 0,1.0 if d==0 else 0.]]); noise=.15+.5*hambre"],
     ["        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k] if k!='vacio' else _VACIO",
      "        x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i==left else 0 for _i in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre   # 2d: un bit por direccion"], 1, 'retina bucle'),
    (["                if _s==0 and k=='vacio': _ciego+=1",
      "                x=np.concatenate([pat*1.2,[1.5 if left else 0,1.5 if left is False else 0,1.0 if d==0 else 0.]]); noise=.15+.5*hambre"],
     ["                if _s==0 and k=='vacio': _ciego+=1",
      "                x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i==left else 0 for _i in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre   # 2d"], 2, 'retina pruebas'),

    # 6) Ruido de la politica: una muestra por accion (con _NA=2, el mismo consumo del rng que el tronco).
    (["u=p+rng.normal(0,.3,2); m=np.zeros(2)"], ["u=p+rng.normal(0,.3,_NA); m=np.zeros(_NA)"], 3, 'ruido'),

    # 7) Movimiento: un paso en la direccion elegida (con _NA=2 es (pos-+1)%L; sin movimiento, pos no cambia).
    (["        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if (d is not None and d2 is not None and d2<d) else 0."],
     ["        pos=(_mov(pos,int(np.argmax(m))) if m.any() else pos); d2,_,_=see(); Rp=.2 if (d is not None and d2 is not None and d2<d) else 0.   # 2d"], 1, 'movimiento'),

    # 8) Sesgo del mapa por direccion. Generalizacion EXACTA de la del anillo: cada celda recordada a distancia h
    #    (1<=h<=H_M) suma disc^h*valor a TODA accion que la ACERQUE (h-1). En el anillo eso es exactamente la suma por
    #    lados, termino a termino y EN EL MISMO ORDEN (distancia creciente), incluida la celda antipodal, que el
    #    original cuenta en las dos direcciones. En 2D una celda en diagonal suma a las dos direcciones que la acercan.
    (["    def _sesgo_M():   # mapa: con la retina vacia, valor recordado por direccion, descontado por distancia",
      "        _bi=sum(disc_M**h*valor(_Mpat[(pos-h)%L]) for h in range(1,H_M+1) if _Mset[(pos-h)%L])",
      "        _bd=sum(disc_M**h*valor(_Mpat[(pos+h)%L]) for h in range(1,H_M+1) if _Mset[(pos+h)%L])",
      "        return gamma_M*np.array([_bi,_bd])"],
     ["    def _sesgo_M(_p=None):   # 2d: con la retina vacia, valor recordado por direccion, descontado por distancia toroidal",
      "        _q=pos if _p is None else _p; _b=[0.0]*_NA",
      "        for _c in sorted((int(_i) for _i in np.flatnonzero(_Mset)),key=lambda _i:_dM(_q,int(_i))):   # por distancia creciente: mismo orden de suma que el anillo",
      "            _h=_dM(_q,_c)",
      "            if _h<1 or _h>H_M: continue",
      "            _v=valor(_Mpat[_c])",
      "            for _a in range(_NA):",
      "                if _dM(_mov(_q,_a),_c)==_h-1: _b[_a]+=disc_M**_h*_v   # esa accion me ACERCA a lo recordado (empate -> cuenta en las dos, como el antipodal del anillo)",
      "        return gamma_M*np.array(_b)"], 1, 'sesgo'),

    # 9) Sitios por coordenadas (solo con modo='2d'; el resto queda intacto).
    (["    _rod=prueba if (prueba is not None and prueba.get('modo')=='rodeo') else None   # rodeo: TODA la perilla nueva vive dentro de prueba"],
     ["    _rod=prueba if (prueba is not None and prueba.get('modo')=='rodeo') else None   # rodeo: TODA la perilla nueva vive dentro de prueba",
      "    _d2=prueba if (prueba is not None and prueba.get('modo')=='2d') else None   # 2d: TODA la perilla nueva vive dentro de prueba",
      "    _o2=1 if (_d2 is None or seed%2) else -1   # 2d: la mitad de las semillas con el mapa REFLEJADO en los dos ejes (equilibra el sesgo motor; no toca el rng)"], 1, '_d2'),
    (["        if _rod is None: _SIT={(_F0+i*(L//len(sitios)))%L:kk for i,kk in enumerate(sitios)}"],
     ["        if _d2 is not None: _SIT={(_F0%_W+_o2*_dx)%_W+((_F0//_W+_o2*_dy)%_H)*_W:kk for (_dx,_dy),kk in zip(_d2['xy'],sitios)}   # 2d: sitios por coordenadas relativas al origen azaroso",
      "        elif _rod is None: _SIT={(_F0+i*(L//len(sitios)))%L:kk for i,kk in enumerate(sitios)}"], 1, 'sitios 2d'),

    # 10) La prueba nueva. Va ANTES de la del rodeo y la deja como elif: con _d2=None el flujo es identico.
    (["    _tel=None",
      "    if _rod is not None:   # rodeo: dos metas y rodeo largo, sin aprendizaje. El organismo NO cambia: decide _sesgo_M"],
     ["    _tel=None",
      "    if _d2 is not None:   # 2d: teletransportes por caso, SIN aprendizaje y SIN boca. El organismo NO cambia: decide _sesgo_M",
      "        if _d2.get('barajar'):   # control: el valor permutado entre celdas y entre pixeles (se reporta, no decide)",
      "            _pi=rng.permutation(NKMAX); Wp=Wp[_pi]; Wn=Wn[_pi]; _pj=rng.permutation(6); Wps=Wps[_pj]; Wns=Wns[_pj]",
      "        if _d2.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps   # control: el valor con el signo cambiado (la puerta, |Wp-Wn|, no cambia)",
      "        _IX={_c:_j for _j,_c in enumerate(_SIT)}; _q2=bool(_d2.get('h2',False)); _bm=bool(_d2.get('borra_M',False))",
      "        _M0=(_Mpat.copy(),_Mset.copy())   # 2d: los 40 teletransportes son pruebas INDEPENDIENTES, asi que el mapa se restaura como E, la traza y los sitios",
      "        _vA=float(valor(PAT['A'])); _vB=float(valor(PAT['B']))   # el valor que la boca ya tenia (tras invertir, si toca)",
      "        def _rel(_dx,_dy): return (_F0%_W+_o2*_dx)%_W+((_F0//_W+_o2*_dy)%_H)*_W   # 2d: coordenada relativa -> celda (con el espejo de la semilla)",
      "        def _QM(_p):   # 2d: horizonte 1 = el mecanismo actual; horizonte 2 = simular UN paso con M y evaluar desde ahi (coste: 1+_NA llamadas a _sesgo_M por paso; memoria: la posicion simulada)",
      "            _b1=_sesgo_M(_p)",
      "            return (_b1,_b1) if not _q2 else (_b1,_b1+disc_M*np.array([float(max(_sesgo_M(_mov(_p,_a)))) for _a in range(_NA)]))",
      "        _cas=[]; _nn=0; _ciego=0",
      "        for _i in range(_d2.get('n_tel',40)):",
      "            _cc=_d2['casos'][_i%len(_d2['casos'])]",
      "            _ok=[(_a if _o2>0 else (_a^1)) for _a in _cc['ok']]   # 2d: con el mapa reflejado, la accion correcta se refleja (0<->1, 2<->3)",
      "            _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]   # 2d: mapa restaurado (solo importa con borra_M, que lo modifica dentro del episodio)",
      "            pos=_rel(*_cc['S']); E=_d2.get('E_test',0.3); tr=np.zeros(_NF); _rech.clear()",
      "            for x in list(_pend): del _pend[x]",
      "            spawn(); _dir=-1; _pisa=0; _come=[]; _b0=None; _s=-1",
      "            for _s in range(_d2.get('max_pasos',60)):",
      "                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k] if k!='vacio' else _VACIO",
      "                if _s==0 and k=='vacio': _ciego+=1",
      "                x=np.concatenate([pat*1.2,([0.]*_NA if left is None else [1.5 if _i2==left else 0 for _i2 in range(_NA)]),[1.0 if d==0 else 0.]]); noise=.15+.5*hambre",
      "                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,_NA); m=np.zeros(_NA)",
      "                if usa_M and k=='vacio':",
      "                    _b1,_b2=_QM(pos)",
      "                    if _b0 is None: _b0=(_b1,_b2)   # el sesgo del PRIMER paso decidido, que es la medida",
      "                    u=u+(_b2 if _q2 else _b1)",
      "                if u.max()>.5: m[np.argmax(u)]=1",
      "                if not m.any(): continue",
      "                if _dir<0: _dir=int(np.argmax(m))   # PRIMER paso: la medida",
      "                pos=_mov(pos,int(np.argmax(m)))",
      "                if pos in _SIT and val[_SIT[pos]]=='veneno': _pisa+=1   # pisar es mas estricto que morder: no se consulta la boca",
      "                if pos in objs and val[objs[pos]]=='comida':",
      "                    _come.append(_IX.get(pos,-1))",
      "                    if not _cc.get('consume'): break",
      "                    del objs[pos]   # secuencia: la comida alcanzada desaparece (no se repone dentro del episodio)",
      "                if _bm and pos not in objs and _Mset[pos]: _Mset[pos]=False   # candidato: el mapa se corrige con lo que veo (sitio recordado y vacio -> se borra)",
      "            if _dir<0: _nn+=1",
      "            _cas.append(dict(et=_cc.get('et',''),S=[int(_cc['S'][0]),int(_cc['S'][1])],primer=int(_dir),",
      "                             acierta=(None if _dir<0 else int(_dir in _ok)),ok=[int(_a) for _a in _ok],",
      "                             mec1=(None if _b0 is None else int(np.argmax(_b0[0]))),mec2=(None if _b0 is None else int(np.argmax(_b0[1]))),",
      "                             B1=(None if _b0 is None else [round(float(_z),4) for _z in _b0[0]]),",
      "                             B2=(None if _b0 is None else [round(float(_z),4) for _z in _b0[1]]),",
      "                             come=[int(_z) for _z in _come],pisa=int(_pisa),pasos=int(_s+1)))",
      "        _Mpat[:]=_M0[0]; _Mset[:]=_M0[1]   # 2d: el mapa que se devuelve (M_llenas) es el del ENTRENAMIENTO, no el que borra_M dejo en el ultimo episodio",
      "        def _fr(_et,_f):",
      "            _v=[_f(_c) for _c in _cas if _c['et']==_et and _f(_c) is not None]",
      "            return (round(sum(_v)/len(_v),3),len(_v)) if _v else (None,0)",
      "        _ets=sorted({_c['et'] for _c in _cas})",
      "        _tel=dict(modo='2d',rejilla=[int(_W),int(_H)],orientacion=int(_o2),h2=int(_q2),borra_M=int(_bm),",
      "                  R={_e:_fr(_e,lambda _c:_c['acierta'])[0] for _e in _ets},n={_e:_fr(_e,lambda _c:_c['acierta'])[1] for _e in _ets},",
      "                  mec1={_e:_fr(_e,lambda _c:(None if _c['mec1'] is None else int(_c['mec1'] in _c['ok'])))[0] for _e in _ets},",
      "                  mec2={_e:_fr(_e,lambda _c:(None if _c['mec2'] is None else int(_c['mec2'] in _c['ok'])))[0] for _e in _ets},",
      "                  sigue_mec1={_e:_fr(_e,lambda _c:(None if (_c['mec1'] is None or _c['primer']<0) else int(_c['primer']==_c['mec1'])))[0] for _e in _ets},",
      "                  llega={_e:_fr(_e,lambda _c:int(len(_c['come'])>0))[0] for _e in _ets},",
      "                  llega_limpio={_e:_fr(_e,lambda _c:int(len(_c['come'])>0 and _c['pisa']==0))[0] for _e in _ets},",
      "                  come2={_e:_fr(_e,lambda _c:int(len(set(_c['come']))>1))[0] for _e in _ets},",
      "                  pisa={_e:_fr(_e,lambda _c:int(_c['pisa']>0))[0] for _e in _ets},",
      "                  pasos={_e:_fr(_e,lambda _c:_c['pasos'])[0] for _e in _ets},",
      "                  sin_mover=_nn,ciego_al_llegar=_ciego,v_A=round(_vA,3),v_B=round(_vB,3),",
      "                  sitios={int(_x):kk for _x,kk in _SIT.items()},casos=_cas)",
      "    elif _rod is not None:   # rodeo: dos metas y rodeo largo, sin aprendizaje. El organismo NO cambia: decide _sesgo_M"], 1, 'prueba 2d'),
]

if __name__ == '__main__':
    if h16(ABUELO) != SHA_ABUELO:
        raise SystemExit(f"ABUELO (mundo_mapa.py) sha {h16(ABUELO)} != {SHA_ABUELO}")
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN (mundo_mapa_rodeo.py) sha {h16(ORIGEN)} != {SHA_ORIGEN}")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_2d = mundo_mapa_rodeo.py (' + SHA_ORIGEN + ') = mundo_mapa.py (' + SHA_ABUELO + ') + rejilla TOROIDAL' + NL +
           'ancho x alto (4 direcciones, retina del objeto mas cercano en distancia Manhattan toroidal, tabla M de posicion 2D)' + NL +
           '+ UNA prueba nueva: prueba=dict(modo=' + chr(39) + '2d' + chr(39) + ', ...). El organismo NO cambia. Generado por construye_2d.py. NO editar.' + NL +
           'ANCLA: con alto=1 es mundo_mapa BIT A BIT, y con modo=' + chr(39) + 'rodeo' + chr(39) + ' es mundo_mapa_rodeo BIT A BIT (identidad obligatoria,' + NL +
           'identidad_2d.py). modo=' + chr(39) + 'rodeo' + chr(39) + ' solo esta definido con alto=1 (su geometria es la del anillo)."""' + NL)
    d = os.path.join(AQUI, 'mundo_2d.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
