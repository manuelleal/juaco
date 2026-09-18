"""Genera organismo_v13q3.py = organismo_v13q.py (0b59eb03858df3a8) + la REGLA FUSIONADA del trio XOR (bloque 3d,
propuesta unica firmada por A, B y C en registro/investigacion/PUENTE_xor.md). Tres knobs, ninguno toca la via rapida,
la Kenyon, la puerta ni la boca:

  regla_lenta='dos_canales' (por defecto, = codigo original intacto) | 'delta_signo'
      'delta_signo' (A + B): UN solo vector con signo Ws en vez de los dos canales no negativos Wps/Wns (+ drenaje lam);
      en cada actualizacion   Ws = clip(Ws*(1-lam_lenta) + eta_s*_ds*phi'(P), -clip_s, +clip_s)
      (decaimiento multiplicativo de TODO el vector, empuje con el error residual de la via lenta, tope SIMETRICO).
  constante=False (por defecto, = original) | True
      'True' (C): phi'(P) = concat(phi(P), [1.0]) -> cuadratica 21->22 entradas, lineal 6->7, random15 21->22.
  lam_lenta=0.002   decaimiento por actualizacion; solo lo usa 'delta_signo' (con 'dos_canales' es inerte).

ENMIENDA 3e (despues de que 3d saliera REFUTADO: CUAD_DELTA acc_lenta 0.500 = dos canales, marginales en cero, y la
curva por clases sin morder no lo explica). Dos lecturas mas, para separar 'la regla no puede' de 'los rasgos no dejan':
  lectura='oraculo01'        phi(P) = [P0, P1, P0*P1]   (3 entradas; 4 con constante=True) -> la base EXACTA de xor01
  lectura='oraculo01_ruido'  phi(P) = [P0, P1, P2*P3]   (3 entradas; 4 con constante) -> control: mismo tamano, producto equivocado
Son INERTES para todo lo de 3d: con lectura='lineal'|'cuadratica'|'random15' el organismo no cambia en nada (se verifica
contra la copia del instrumento de 3d, sha b71bbe41a7326aaf, en el humo de 3e).

Identidad obligatoria (arnes en corre_xor_3d.py, ETAPA 1): con regla_lenta='dos_canales', constante=False el organismo
es organismo_v13q bit a bit en TODAS las claves del original (semillas 1-3, xor01 y px0, lecturas lineal y cuadratica).
Sonda de fase2_en: sigue dando W_lenta_apriori (con 'delta_signo' = Ws @ phi') y familiar_apriori, y ANADE Ws_apriori
(el vector con signo VIGENTE en la sonda: Ws si 'delta_signo', Wps-Wns si 'dos_canales') -- aviso metodologico de C:
los pesos del return son los del final de T, no los de la sonda.

Anclas con conteo exacto (aborta si una aparece != n veces). NO edita organismo_v13q.py.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(AQUI, 'organismo_v13q.py')
SHA_ORIGEN = '0b59eb03858df3a8'
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


PARCHES = [
    # 1) firma + guardia de knob mal escrito (un 'delta' suelto caeria en silencio al brazo original: el knob de A se llamaba asi)
    (["puerta=None,mundo='AB',regla='px0',fase2_en=None,sonda_final=False,lectura='lineal'):   # xor: lectura de la via lenta",
      "    if mundo=='AB': P_=PAT; tren=['A','B']; test=[]   # v13g: con 'AB' es v13 exacto"],
     ["puerta=None,mundo='AB',regla='px0',fase2_en=None,sonda_final=False,lectura='lineal',regla_lenta='dos_canales',constante=False,lam_lenta=0.002):   # xor: lectura de la via lenta; 3d: regla de la via lenta, termino constante y decaimiento",
      "    if regla_lenta not in ('dos_canales','delta_signo'): raise ValueError(f\"regla_lenta={regla_lenta!r}\")   # 3d: un knob mal escrito NO puede caer en silencio al brazo original",
      "    if lectura not in ('lineal','cuadratica','random15','oraculo01','oraculo01_ruido'): raise ValueError(f\"lectura={lectura!r}\")   # 3e: idem para la lectura",
      "    if mundo=='AB': P_=PAT; tren=['A','B']; test=[]   # v13g: con 'AB' es v13 exacto"], 1, 'firma'),
    # 2) tamano de phi (con constante) y vector con signo Ws (inerte si regla_lenta='dos_canales')
    (["    _NF=6 if lectura=='lineal' else 21   # xor: lineal = 6 px; cuadratica = 6 px + 15 productos de pares; random15 = 6 px + 15 bits fijos al azar por patron",
      "    Wps=np.zeros(_NF); Wns=np.zeros(_NF)   # v13: via LENTA sobre phi(P) (con lectura='lineal' es v13g exacto)"],
     ["    _NF=(6 if lectura=='lineal' else 3 if lectura in ('oraculo01','oraculo01_ruido') else 21)+(1 if constante else 0)   # xor: lineal = 6 px; cuadratica = 6 px + 15 productos; random15 = 6 px + 15 bits al azar; 3e: oraculo = 3 rasgos; 3d: +1 si constante",
      "    Wps=np.zeros(_NF); Wns=np.zeros(_NF)   # v13: via LENTA sobre phi(P) (con lectura='lineal' es v13g exacto)",
      "    Ws=np.zeros(_NF)   # 3d: vector con signo de la via lenta; solo se mueve/lee si regla_lenta=='delta_signo'"], 1, 'NF y Ws'),
    # 3) phi' = phi + [1.0] (C) y las dos lecturas de la via lenta segun regla_lenta
    (["    def phi(P):",
      "        if lectura=='lineal': return P",
      "        if lectura=='cuadratica': return np.concatenate([P,[P[i]*P[j] for i,j in _IJ]])",
      "        return np.concatenate([P,_R15[tuple(float(v) for v in P)]])"],
     ["    def phi(P):   # 3d: constante=True anade 1 entrada fija en 1.0 al final (phi' de C). Con constante=False devuelve exactamente lo de antes",
      "        if lectura=='lineal': _b=P",
      "        elif lectura=='cuadratica': _b=np.concatenate([P,[P[i]*P[j] for i,j in _IJ]])",
      "        elif lectura=='oraculo01': _b=np.array([P[0],P[1],P[0]*P[1]])   # 3e: la base EXACTA de xor01 (3 rasgos)",
      "        elif lectura=='oraculo01_ruido': _b=np.array([P[0],P[1],P[2]*P[3]])   # 3e: control, mismo tamano, el producto equivocado",
      "        else: _b=np.concatenate([P,_R15[tuple(float(v) for v in P)]])",
      "        return np.concatenate([_b,[1.0]]) if constante else _b",
      "    def lenta(P):   # 3d: lectura de la via lenta sola segun regla_lenta ('dos_canales' = la formula original, exacta)",
      "        _ph=phi(P); return float(Ws@_ph) if regla_lenta=='delta_signo' else float((Wps-Wns)@_ph)",
      "    def _wvec():   # 3d: vector con signo VIGENTE de la via lenta (mecanismo: marginales y producto en la sonda)",
      "        return Ws if regla_lenta=='delta_signo' else (Wps-Wns)"], 1, 'phi y lenta'),
    # 4) el valor que usa la boca
    (["        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@phi(P))"],
     ["        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=lenta(P)"], 1, 'valor'),
    # 5) la boca al morder
    (["_ws=float((Wps-Wns)@phi(P_[kk]))   # v13: las dos vias (xor: phi)"],
     ["_ws=lenta(P_[kk])   # v13: las dos vias (xor: phi; 3d: segun regla_lenta)"], 1, 'boca'),
    # 6) LA REGLA: delta con signo + decaimiento multiplicativo + tope simetrico; 'dos_canales' queda intacta
    (["                        if lam: _mcs=np.minimum(Wps,Wns)*(phi(P_[kk])>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs",
      "                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*phi(P_[kk]),0,clip_s)",
      "                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*phi(P_[kk]),0,clip_s)"],
     ["                        if regla_lenta=='delta_signo':   # 3d (A+B+C): UN vector con signo, decaimiento multiplicativo de TODO el vector, tope simetrico. Sin aversion (todas las corridas de 3d usan aversion=1.0)",
      "                            Ws=np.clip(Ws*(1-lam_lenta)+eta_s*_ds*phi(P_[kk]),-clip_s,clip_s)",
      "                        else:   # 'dos_canales': la regla original de v13/v13q, sin tocar (identidad obligatoria)",
      "                            if lam: _mcs=np.minimum(Wps,Wns)*(phi(P_[kk])>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs",
      "                            if _ds>0: Wps=np.clip(Wps+eta_s*_ds*phi(P_[kk]),0,clip_s)",
      "                            else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*phi(P_[kk]),0,clip_s)"], 1, 'regla lenta'),
    # 7) init de la sonda: Ws_apriori (aviso metodologico de C)
    (["    W_lenta_apriori=None; familiar_apriori=None   # 3b"],
     ["    W_lenta_apriori=None; familiar_apriori=None   # 3b",
      "    Ws_apriori=None   # 3d: el vector con signo vigente EN LA SONDA (los del return son los del final de T)"], 1, 'init sonda 3d'),
    # 8) sonda de fase2_en
    (["            W_lenta_apriori={_k:float((Wps-Wns)@phi(P_[_k])) for _k in P_}   # 3b: la via lenta sola"],
     ["            W_lenta_apriori={_k:lenta(P_[_k]) for _k in P_}   # 3b: la via lenta sola (3d: Ws@phi' si delta_signo)",
      "            Ws_apriori=[float(_x) for _x in _wvec()]   # 3d: lectura pura, no cambia ningun numero"], 1, 'sonda 3d'),
    # 9) lectura final de la via lenta
    (["    W_lenta={k:round(float((Wps-Wns)@phi(P_[k])),3) for k in P_}   # v13: lectura de la via lenta sola (xor: phi)"],
     ["    W_lenta={k:round(lenta(P_[k]),3) for k in P_}   # v13: lectura de la via lenta sola (xor: phi; 3d: segun regla_lenta)"], 1, 'W_lenta'),
    # 10) return: claves nuevas (las del original NO se tocan -> identidad en todas ellas)
    (["W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],mundo=mundo,"],
     ["W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],Ws=[round(float(x),3) for x in Ws],Ws_apriori=Ws_apriori,regla_lenta=regla_lenta,constante=constante,lam_lenta=lam_lenta,mundo=mundo,"], 1, 'return 3d'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != {SHA_ORIGEN}")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""organismo_v13q3 = organismo_v13q.py (' + SHA_ORIGEN + ') + regla fusionada del trio XOR (bloque 3d) +' + NL +
           "lecturas oraculo del bloque 3e. Knobs: regla_lenta='dos_canales'|'delta_signo', constante=False|True," + NL +
           "lam_lenta (decaimiento por actualizacion), lectura=...|'oraculo01'|'oraculo01_ruido'." + NL +
           'Generado por construye_xor_3d.py. NO editar. Con regla_lenta=\'dos_canales\' y constante=False es organismo_v13q' + NL +
           'exacto en todas las claves del original (identidad obligatoria, ETAPA 1 de corre_xor_3d.py)."""' + NL)
    d = os.path.join(AQUI, 'organismo_v13q3.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  origen {os.path.relpath(ORIGEN, RAIZ)} {h16(ORIGEN)}")
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
