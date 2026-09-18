"""Genera mundo_mapa_rodeo.py = mundo_mapa.py (207d6a1954336b18) + UNA prueba nueva: prueba=dict(modo='rodeo', ...)
(dos metas recordadas y rodeo largo cuando el camino corto pasa por veneno recordado). El ORGANISMO no cambia:
la decision sigue saliendo de _sesgo_M (suma por direccion del valor descontado de lo recordado). Toda la perilla
nueva vive DENTRO de prueba; sin modo='rodeo' el instrumento es mundo_mapa EXACTO (identidad obligatoria, bit a bit,
en los seis brazos de corre_mapa.py). Anclas con conteo exacto.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel6_mapa', 'mundo_mapa.py')
SHA_ORIGEN = '207d6a1954336b18'
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


PARCHES = [
    # 1) Montaje de los sitios. Con modo!='rodeo' la linea original queda intacta (identidad). Con modo='rodeo' los
    #    tres sitios van ASIMETRICOS: con los L/3 de mundo_mapa el rodeo es GEOMETRICAMENTE IMPOSIBLE (hace falta
    #    g2-g1 > 2*dp con dp > r_vis; con huecos iguales da 0). Ver PREREGISTRO_rodeo.md seccion 0.
    (["    _SIT={}; _pend={}   # mapa: sitio -> tipo fijo; sitio -> paso en que reaparece",
      "    if sitios is not None:",
      "        _F0=int(rng.integers(L)); _SIT={(_F0+i*(L//len(sitios)))%L:kk for i,kk in enumerate(sitios)}"],
     ["    _SIT={}; _pend={}   # mapa: sitio -> tipo fijo; sitio -> paso en que reaparece",
      "    _rod=prueba if (prueba is not None and prueba.get('modo')=='rodeo') else None   # rodeo: TODA la perilla nueva vive dentro de prueba",
      "    _g1=int(_rod.get('g1',5)) if _rod is not None else 0; _g2=int(_rod.get('g2',20)) if _rod is not None else 0   # rodeo: huecos F1->veneno y veneno->F2",
      "    _or=1 if (_rod is None or seed%2) else -1   # rodeo: la mitad de las semillas con el mapa en ESPEJO (equilibra el sesgo motor; no toca el rng)",
      "    if sitios is not None:",
      "        _F0=int(rng.integers(L))",
      "        if _rod is None: _SIT={(_F0+i*(L//len(sitios)))%L:kk for i,kk in enumerate(sitios)}",
      "        else: _SIT={_F0%L:sitios[0],(_F0+_or*_g1)%L:sitios[1],(_F0+_or*(_g1+_g2))%L:sitios[2]}   # rodeo: F1 en F0, veneno a g1, F2 a g1+g2"], 1, 'sitios'),
    # 2) La prueba nueva. Va ANTES de la de mundo_mapa y la deja como elif: con _rod=None el flujo es identico.
    (["    _tel=None",
      "    if prueba is not None:   # mapa: prueba de teletransporte, sin aprendizaje"],
     ["    _tel=None",
      "    if _rod is not None:   # rodeo: dos metas y rodeo largo, sin aprendizaje. El organismo NO cambia: decide _sesgo_M",
      "        _F1=_F0%L; _VEN=(_F0+_or*_g1)%L; _F2=(_F0+_or*(_g1+_g2))%L; _g3=L-_g1-_g2",
      "        if _rod.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps   # control: el valor con el signo cambiado (la puerta, |Wp-Wn|, no cambia)",
      "        _DP=tuple(_rod.get('dps',(4,5,6,7))); _AA=tuple(_rod.get('aas',(4,5,6,7)))   # rodeo: distancia al veneno / a la comida corta",
      "        _vA=float(valor(PAT[sitios[0]])); _vB=float(valor(PAT[sitios[1]]))   # el valor que la boca ya tenia (tras invertir, si toca)",
      "        _cas=[]; _nn=0; _ciego=0; _pasos=[]",
      "        for i in range(_rod.get('n_tel',40)):",
      "            if i%2==0:   # RODEO esperado: el veneno esta ENTRE S y la comida cercana (F1 a d1); la otra comida (F2) a d2>d1 y limpia",
      "                _dp=_DP[(i//2)%len(_DP)]; _d1=_g1+_dp; _d2=_g2-_dp; _S=(_VEN+_or*_dp)%L; _ok=_or; _cs='rodeo'",
      "            else:        # ATAJO esperado: la comida cercana (F2 a d1) esta LIMPIA; el veneno queda fuera del camino corto, detras de F1",
      "                _aa=_AA[(i//2)%len(_AA)]; _d1=_aa; _d2=_g3-_aa; _dp=_d2+_g1; _S=(_F2+_or*_aa)%L; _ok=-_or; _cs='atajo'",
      "            _bc=_vA*disc_M**_d1+(_vB*disc_M**_dp if _cs=='rodeo' else 0.0)   # lo que suma el lado CORTO",
      "            _bl=_vA*disc_M**_d2+(0.0 if _cs=='rodeo' else _vB*disc_M**_dp)   # lo que suma el lado LARGO",
      "            pos=_S; E=_rod.get('E_test',0.3); tr=np.zeros(9); _rech.clear()",
      "            for x in list(_pend): del _pend[x]",
      "            spawn(); _dir=0; _pisa=0; _come=None",
      "            for _s in range(_rod.get('max_pasos',60)):",
      "                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k] if k!='vacio' else _VACIO",
      "                if _s==0 and k=='vacio': _ciego+=1",
      "                x=np.concatenate([pat*1.2,[1.5 if left else 0,1.5 if left is False else 0,1.0 if d==0 else 0.]]); noise=.15+.5*hambre",
      "                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)",
      "                if usa_M and k=='vacio': u=u+_sesgo_M()",
      "                if u.max()>.5: m[np.argmax(u)]=1",
      "                if not m.any(): continue",
      "                if _dir==0: _dir=int(m[1]-m[0]); _pasos.append(_s+1)   # PRIMER paso: la medida de R1/R2",
      "                pos=(pos+int(m[1]-m[0]))%L",
      "                if pos==_VEN: _pisa+=1   # piso el veneno (mas estricto que morderlo: no se consulta la boca)",
      "                if pos==_F1 or pos==_F2: _come=('F1' if pos==_F1 else 'F2'); break",
      "            if _dir==0: _nn+=1",
      "            _cas.append(dict(caso=_cs,d1=int(_d1),d2=int(_d2),dp=int(_dp),S=int(_S),lado_ok=int(_ok),primer=int(_dir),",
      "                             acierta=(None if _dir==0 else int(_dir==_ok)),B_corto=round(_bc,4),B_largo=round(_bl,4),",
      "                             mec=int(_bl>_bc),come=_come,pisa=int(_pisa)))",
      "        _rc=[c for c in _cas if c['caso']=='rodeo']; _at=[c for c in _cas if c['caso']=='atajo']",
      "        def _f(cs):",
      "            _v=[c['acierta'] for c in cs if c['acierta'] is not None]",
      "            return (round(sum(_v)/len(_v),3),len(_v)) if _v else (None,0)",
      "        _r1,_n1=_f(_rc); _r2,_n2=_f(_at)",
      "        _lim=[c for c in _cas if c['come'] is not None and c['pisa']==0]",
      "        _tel=dict(modo='rodeo',R1=_r1,R2=_r2,n_rodeo=_n1,n_atajo=_n2,",
      "                  llega_limpio=(round(len(_lim)/len(_cas),3) if _cas else None),",
      "                  llega=(round(sum(c['come'] is not None for c in _cas)/len(_cas),3) if _cas else None),",
      "                  come_F1=sum(c['come']=='F1' for c in _cas),come_F2=sum(c['come']=='F2' for c in _cas),",
      "                  pisa_total=int(sum(c['pisa'] for c in _cas)),sin_mover=_nn,ciego_al_llegar=_ciego,",
      "                  pasos_medio=(round(sum(_pasos)/len(_pasos),2) if _pasos else None),",
      "                  v_A=round(_vA,3),v_B=round(_vB,3),",
      "                  mec_rodeo=(round(sum(c['mec'] for c in _rc)/len(_rc),3) if _rc else None),",
      "                  mec_atajo=(round(sum(1-c['mec'] for c in _at)/len(_at),3) if _at else None),",
      "                  orientacion=int(_or),g=(int(_g1),int(_g2),int(_g3)),F1=int(_F1),V=int(_VEN),F2=int(_F2),",
      "                  sitios={int(x):kk for x,kk in _SIT.items()},casos=_cas)",
      "    elif prueba is not None:   # mapa: prueba de teletransporte, sin aprendizaje"], 1, 'prueba rodeo'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != {SHA_ORIGEN}")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_mapa_rodeo = mundo_mapa.py (' + SHA_ORIGEN + ') + UNA prueba nueva: prueba=dict(modo=' + chr(39) + 'rodeo' + chr(39) + ', ...)' + NL +
           '(dos metas recordadas y rodeo largo cuando el camino corto pasa por veneno recordado). El organismo NO cambia.' + NL +
           'Generado por construye_rodeo.py. NO editar. Sin modo=' + chr(39) + 'rodeo' + chr(39) + ' es mundo_mapa exacto (identidad obligatoria)."""' + NL)
    d = os.path.join(AQUI, 'mundo_mapa_rodeo.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
