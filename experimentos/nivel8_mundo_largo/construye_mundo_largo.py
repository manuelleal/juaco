"""Genera mundo_largo.py = mundo_mapa.py (207d6a1954336b18) + pool de patrones (50), inyeccion de un patron nuevo (o
reciclado) cada T_nuevo pasos en el sitio mas viejo, cambio de regla sin aviso (invertir_largo) y lecturas (curva de
adquisicion/retencion por readout, comida y muertes por bloque de 1000). Con pool=None, T_nuevo=None,
invertir_largo=None es mundo_mapa EXACTO (identidad obligatoria). Anclas con conteo exacto.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel6_mapa', 'mundo_mapa.py')
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


PARCHES = [
    (["PAT["], ["PAT_L["], 24, 'PAT[ -> PAT_L['),
    (["for k in PAT}"], ["for k in PAT_L}"], 5, 'for k in PAT'),
    (["        r_vis=None,sitios=None,regen=50,usa_M=False,escribe_M=True,gamma_M=0.6,H_M=20,disc_M=0.9,prueba=None):   # mapa"],
     ["        r_vis=None,sitios=None,regen=50,usa_M=False,escribe_M=True,gamma_M=0.6,H_M=20,disc_M=0.9,prueba=None,",
      "        pool=None,T_nuevo=None,reciclado=False,invertir_largo=None):   # mapa + largo"], 1, 'firma'),
    (["    rng=np.random.default_rng(seed)"],
     ["    rng=np.random.default_rng(seed)",
      "    PAT_L=PAT if pool is None else dict(PAT,**{n:v for n,v,_ in pool})   # largo: los patrones del pool ademas de A-D",
      "    _rng_l=np.random.default_rng(seed+700000)   # largo: RNG propio para el orden de inyeccion (no toca el del organismo)",
      "    _orden=[] if pool is None else [n for n,_,_ in pool]",
      "    if pool is not None: _orden=[_orden[i] for i in _rng_l.permutation(len(_orden))]"], 1, 'PAT_L'),
    (["    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}"],
     ["    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}",
      "    if pool is not None: val.update({n:vl for n,_,vl in pool})   # largo"], 1, 'val'),
    (["        _F0=int(rng.integers(L)); _SIT={(_F0+i*(L//len(sitios)))%L:kk for i,kk in enumerate(sitios)}"],
     ["        _F0=int(rng.integers(L)); _SIT={(_F0+i*(L//len(sitios)))%L:kk for i,kk in enumerate(sitios)}",
      "        _ren={x:0 for x in _SIT}; _vistos=list(dict.fromkeys(sitios))   # largo: ultima renovacion por sitio; patrones vistos en orden"], 1, 'sitios'),
    (["    q=lambda t:min(t//(T//4),3)"],
     ["    q=lambda t:min(t//(T//4),3)",
      "    _iny=[]; _curva=[]; _cbin=[0]*(T//1000+1); _dbin=[0]*(T//1000+1)   # largo: lecturas"], 1, 'q'),
    (["    _SIT={}; _pend={}   # mapa: sitio -> tipo fijo; sitio -> paso en que reaparece"],
     ["    _SIT={}; _pend={}   # mapa: sitio -> tipo fijo; sitio -> paso en que reaparece",
      "    _ren={}; _vistos=[]   # largo (se llenan en el bloque de sitios)"], 1, 'defaults largo'),
    (["        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val"],
     ["        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val",
      "        if T_nuevo and t>0 and t%T_nuevo==0:   # largo: entra un patron (nuevo o reciclado) en el sitio que lleva mas tiempo sin renovarse",
      "            _cand=[n for n in _orden if n not in _vistos]",
      "            _nv=_vistos[int(_rng_l.integers(len(_vistos)))] if (reciclado or not _cand) else _cand[0]",
      "            _x=min(_ren,key=lambda x:(_ren[x],x)); _SIT[_x]=_nv; _ren[_x]=t",
      "            if _x in objs: objs[_x]=_nv",
      "            if _nv not in _vistos: _vistos.append(_nv)",
      "            _iny.append((t,_nv,_x))",
      "            _ok=lambda n:(valor(PAT_L[n])>0)==(val[n]=='comida')",
      "            _ult=_vistos[-10:]; _pri=_vistos[:10]",
      "            _curva.append((t,len(_vistos),round(sum(_ok(n) for n in _ult)/len(_ult),3),round(sum(_ok(n) for n in _pri)/len(_pri),3)))",
      "        if invertir_largo is not None and t==invertir_largo:   # largo: cambio de regla sin aviso (los 4 iniciales y los presentes)",
      "            for n in set(_vistos[:4])|set(_SIT.values()): val[n]='veneno' if val[n]=='comida' else 'comida'"], 1, 'inyeccion e inversion'),
    (["                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1"],
     ["                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1",
      "                if val[kk]=='comida': _cbin[t//1000]+=1   # largo"], 1, 'comida por bloque'),
    (["        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))"],
     ["        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L)); _dbin[t//1000]+=1   # (+largo)"], 1, 'muertes por bloque'),
    (["                tel=_tel,M_llenas=int(_Mset.sum()))   # mapa"],
     ["                tel=_tel,M_llenas=int(_Mset.sum()),   # mapa",
      "                curva=_curva,inyecciones=_iny,vistos=_vistos,comida_bin=_cbin,muertes_bin=_dbin,val_final=dict(val))   # largo"], 1, 'return'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != '207d6a1954336b18':
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != 207d6a1954336b18")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_largo = mundo_mapa.py (207d6a1954336b18) + pool de 50 patrones, inyeccion cada T_nuevo pasos (nuevo o reciclado),' + NL +
           'cambio de regla sin aviso y lecturas por bloque. Generado por construye_mundo_largo.py. NO editar. Con pool=None,' + NL +
           'T_nuevo=None, invertir_largo=None es mundo_mapa exacto (identidad obligatoria)."""' + NL)
    d = os.path.join(AQUI, 'mundo_largo.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
