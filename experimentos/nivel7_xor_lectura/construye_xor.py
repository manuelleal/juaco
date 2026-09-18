"""Genera organismo_v13q.py = organismo_v13g.py (2a80e125f8593bf2) + knob lectura de la via lenta: 'lineal' (v13g exacto),
'cuadratica' (6 px + 15 productos de pares) o 'random15' (control: 6 px + 15 bits fijos al azar por patron). Kenyon, via
rapida, puerta y boca NO cambian. Anclas con conteo exacto.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py')
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


PARCHES = [
    (["puerta=None,mundo='AB',regla='px0',fase2_en=None,sonda_final=False):"],
     ["puerta=None,mundo='AB',regla='px0',fase2_en=None,sonda_final=False,lectura='lineal'):   # xor: lectura de la via lenta"], 1, 'firma'),
    (["    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)"],
     ["    _NF=6 if lectura=='lineal' else 21   # xor: lineal = 6 px; cuadratica = 6 px + 15 productos de pares; random15 = 6 px + 15 bits fijos al azar por patron",
      "    Wps=np.zeros(_NF); Wns=np.zeros(_NF)   # v13: via LENTA sobre phi(P) (con lectura='lineal' es v13g exacto)",
      "    _IJ=[(i,j) for i in range(6) for j in range(i+1,6)]",
      "    _R15={}",
      "    if lectura=='random15':",
      "        _rr=np.random.default_rng(seed+900000)   # RNG propio: no toca el del organismo",
      "        for _n in range(64):",
      "            _Pb=tuple(float((_n>>(5-_j))&1) for _j in range(6)); _R15[_Pb]=_rr.integers(0,2,15).astype(float)",
      "    def phi(P):",
      "        if lectura=='lineal': return P",
      "        if lectura=='cuadratica': return np.concatenate([P,[P[i]*P[j] for i,j in _IJ]])",
      "        return np.concatenate([P,_R15[tuple(float(v) for v in P)]])"], 1, 'phi'),
    (["        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)"],
     ["        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@phi(P))"], 1, 'valor'),
    (["_ws=float((Wps-Wns)@P_[kk])   # v13: las dos vias"], ["_ws=float((Wps-Wns)@phi(P_[kk]))   # v13: las dos vias (xor: phi)"], 1, 'boca'),
    (["                        if lam: _mcs=np.minimum(Wps,Wns)*(P_[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs"],
     ["                        if lam: _mcs=np.minimum(Wps,Wns)*(phi(P_[kk])>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs"], 1, 'drenaje'),
    (["                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*P_[kk],0,clip_s)",
      "                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*P_[kk],0,clip_s)"],
     ["                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*phi(P_[kk]),0,clip_s)",
      "                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*phi(P_[kk]),0,clip_s)"], 1, 'aprendizaje lenta'),
    (["    W_lenta={k:round(float((Wps-Wns)@P_[k]),3) for k in P_}   # v13: lectura de la via lenta sola"],
     ["    W_lenta={k:round(float((Wps-Wns)@phi(P_[k])),3) for k in P_}   # v13: lectura de la via lenta sola (xor: phi)"], 1, 'W_lenta'),
    # 3b: lecturas puras en la sonda (no tocan ningun numero del organismo): la via lenta sola y si la puerta leeria la rapida
    (["    W_apriori=None; codigos_f2=None; primer={}   # v13g: sonda y primer encuentro (lectura)"],
     ["    W_apriori=None; codigos_f2=None; primer={}   # v13g: sonda y primer encuentro (lectura)",
      "    W_lenta_apriori=None; familiar_apriori=None   # 3b"], 1, 'init 3b'),
    (["            W_apriori={_k:valor(P_[_k]) for _k in P_}"],
     ["            W_apriori={_k:valor(P_[_k]) for _k in P_}",
      "            W_lenta_apriori={_k:float((Wps-Wns)@phi(P_[_k])) for _k in P_}   # 3b: la via lenta sola",
      "            familiar_apriori={_k:(bool(int((np.abs((Wp-Wn)[kenyon(P_[_k])>0])>0.2).sum())>=puerta) if puerta is not None else False) for _k in P_}   # 3b: ¿la puerta lee la rapida?"], 1, 'sonda 3b'),
    (["W_apriori=W_apriori,codigos_f2=codigos_f2,"], ["W_apriori=W_apriori,W_lenta_apriori=W_lenta_apriori,familiar_apriori=familiar_apriori,codigos_f2=codigos_f2,"], 1, 'return 3b'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != '2a80e125f8593bf2':
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != 2a80e125f8593bf2")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""organismo_v13q = organismo_v13g.py (2a80e125f8593bf2) + knob lectura de la via lenta (lineal | cuadratica | random15).' + NL +
           'Generado por construye_xor.py. NO editar. Con lectura=\'lineal\' es organismo_v13g exacto (identidad obligatoria)."""' + NL)
    d = os.path.join(AQUI, 'organismo_v13q.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
