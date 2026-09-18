"""CREADOR A — candidato v15: la MEMORIA DE UN GOLPE POR COMBINACION (M3, grupo 3) llevada a la VIA LENTA DEL TRONCO.

Genera, POR ANCLAS y sin tocar nada congelado (patron de `construye_v14c.py`; los originales SOLO se leen):

  organismo_v15c.py            <- organismo/organismo_v14.py    (TRONCO v14.1 CONGELADO)
  organismo_v15c_on.py         <- organismo_v15c.py con la perilla FIJA en 'combi' (para que las baterias lo examinen)
  organismo_v15gc.py           <- organismo/organismo_v14g.py   (mundo de regla)
  organismo_v15gc_on.py        <- organismo_v15gc.py con la perilla FIJA en 'combi'
  bateria_v15c.py              <- organismo/bateria_v14.py      (CONGELADA; criterio v3' y umbrales INTACTOS)
  bateria_generaliza_v15c.py   <- organismo/bateria_generaliza.py (CONGELADA; UNA entrada nueva en INSTRUMENTOS)

PERILLA `memoria_pares` (None por defecto = v14.1 EXACTO, bit a bit):
  15 celdas (los pares de pixeles) x 4 casillas (las combinaciones 00/01/10/11) + 15 contadores de visitas
  + 15 errores propios (EMA de (R - prediccion)^2). En cada mordida escriben las 15 celdas; **la primera vez que una
  celda ve una combinacion, escribe R DE UN GOLPE** ('combi' luego mueve con `mem_alfa`; 'combi1' no vuelve a moverla).
  La via lenta LEE la celda de menor error; **abstencion explicita 0.0** en combinaciones nunca vistas.
  **Desempate AL AZAR con el `rng` DEL ORGANISMO**, y — esto importa para la identidad — **solo se consume un numero
  aleatorio cuando la perilla esta ENCENDIDA y hay empate de verdad** (len > 1). Con la perilla apagada no se toca
  el `rng`, no se evalua ninguna expresion nueva y las lineas originales quedan literales.
  Memoria: 15x4 + 15x4 + 15 = 135 numeros. Sin pesos, sin tasa, sin tope.

Uso: python construye_v15c.py     (no corre nada)
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')


def origen(ruta):
    b = open(ruta, 'rb').read()
    return b.decode('utf-8'), hashlib.sha256(b).hexdigest()[:16]


def sust(t, a, b, n=1, etq=''):
    c = t.count(a)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return t.replace(a, b)


def pon_memoria(src, PP, etq):
    """Aplica las 5 anclas. `PP` es como el organismo accede al patron actual: 'PAT' (tronco) o 'P_' (mundo de regla)."""
    # 1) firma
    _fin = ",pat_shuf=0,pat_min=1):" if ",pat_shuf=0,pat_min=1):" in src else ",pat_shuf=0,pat_min=0):"
    out = sust(src, _fin, _fin[:-2] + ",memoria_pares=None,mem_alfa=0.3,mem_rho=0.02):", etq=f'{etq}: firma')
    # 2) estado + lectura de la via lenta
    A = "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)"
    B = (A + "\n"
         "    if memoria_pares not in (None,'combi','combi1'): raise ValueError(f\"memoria_pares={memoria_pares!r}\")   # v15c: perilla mal escrita no cae en silencio\n"
         "    _PARv=[(i,j) for i in range(6) for j in range(i+1,6)]   # v15c (M3): las 15 celdas = pares de pixeles\n"
         "    _MMv=np.zeros((15,4)); _MNv=np.zeros((15,4)); _MEv=np.full(15,1e9); _MGv=0   # v15c: valor, visitas, error propio, ganadora\n"
         "    def _lenta_v15(P):   # v15c: con la perilla APAGADA es literalmente la lectura de v14\n"
         "        if memoria_pares is None: return float((Wps-Wns)@P)\n"
         "        _i,_j=_PARv[_MGv]; _c=int(P[_i])*2+int(P[_j])\n"
         "        return float(_MMv[_MGv,_c]) if _MNv[_MGv,_c]>0 else 0.0   # abstencion explicita")
    out = sust(out, A, B, etq=f'{etq}: estado')
    # 3) la lectura dentro de valor()
    out = sust(out, "        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)",
               "        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=_lenta_v15(P)", etq=f'{etq}: valor')
    # 4) la lectura en la mordida
    out = sust(out, f"_ws=float((Wps-Wns)@{PP}[kk])   # v13: las dos vias",
               f"_ws=_lenta_v15({PP}[kk])   # v13: las dos vias (v15c: la memoria de pares si la perilla esta encendida)",
               etq=f'{etq}: mordida')
    # 5) la actualizacion
    A = ("                        _ds=dlt if puerta is None else R-_ws\n"
         f"                        if lam: _mcs=np.minimum(Wps,Wns)*({PP}[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs")
    B = ("                        _ds=dlt if puerta is None else R-_ws\n"
         "                        if memoria_pares is not None:   # v15c (M3): las 15 celdas escriben; la primera vez, DE UN GOLPE\n"
         f"                            _Pv={PP}[kk]\n"
         "                            for _cv in range(15):\n"
         "                                _iv,_jv=_PARv[_cv]; _dv=int(_Pv[_iv])*2+int(_Pv[_jv])\n"
         "                                _pv=float(_MMv[_cv,_dv]) if _MNv[_cv,_dv]>0 else 0.0\n"
         "                                _ev=R-_pv; _prv=bool(_MNv[_cv].sum()==0)\n"
         "                                _MEv[_cv]=(_ev*_ev) if _prv else (1-mem_rho)*_MEv[_cv]+mem_rho*(_ev*_ev)\n"
         "                                if _MNv[_cv,_dv]==0: _MMv[_cv,_dv]=R\n"
         "                                elif memoria_pares=='combi': _MMv[_cv,_dv]+=mem_alfa*(R-_MMv[_cv,_dv])\n"
         "                                _MNv[_cv,_dv]+=1\n"
         "                            _mnv=float(_MEv.min()); _empv=[int(_x) for _x in np.where(_MEv<=_mnv+1e-12)[0]]\n"
         "                            _MGv=_empv[0] if len(_empv)==1 else int(_empv[int(rng.integers(len(_empv)))])   # desempate al azar; solo consume rng si HAY empate\n"
         f"                        if lam: _mcs=np.minimum(Wps,Wns)*({PP}[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs")
    out = sust(out, A, B, etq=f'{etq}: actualizacion')
    # 6) el return (lecturas)
    out = sust(out, "    return dict(sobre=sobre,",
               "    return dict(memoria_pares=memoria_pares,mem_ganadora=(list(_PARv[_MGv]) if memoria_pares is not None else None),"
               "mem_tabla=([[float(_x) for _x in _f] for _f in _MMv] if memoria_pares is not None else None),"
               "mem_vistas=(int((_MNv>0).sum()) if memoria_pares is not None else None),"
               "mem_cobertura=(int((_MNv[_MGv]>0).sum()) if memoria_pares is not None else None),sobre=sobre,",
               etq=f'{etq}: return')
    return out


def escribe(nombre, texto, cab):
    open(os.path.join(AQUI, nombre), 'w', encoding='utf-8').write(cab + texto)
    return hashlib.sha256(open(os.path.join(AQUI, nombre), 'rb').read()).hexdigest()[:16]


if __name__ == '__main__':
    hechos = {}
    # ---------------- el tronco
    src, sha14 = origen(os.path.join(ORG, 'organismo_v14.py'))
    v15 = pon_memoria(src, 'PAT', 'v15c')
    cab = (f'"""organismo_v15c = organismo/organismo_v14.py ({sha14}, TRONCO v14.1 CONGELADO: solo se leyo) + perilla\n'
           f'`memoria_pares` (M3 del grupo 3 llevado a la via lenta). Con memoria_pares=None es organismo_v14 EXACTO\n'
           f'(identidad obligatoria: identidad_v15c.py; no se consume ni un numero del rng con la perilla apagada).\n'
           f'Generado por experimentos/creacion_A/construye_v15c.py. NO editar a mano."""\n')
    hechos['organismo_v15c.py'] = escribe('organismo_v15c.py', v15, cab)
    on = sust(v15, ",memoria_pares=None,mem_alfa=0.3", ",memoria_pares='combi',mem_alfa=0.3", etq='on: tronco')
    hechos['organismo_v15c_on.py'] = escribe('organismo_v15c_on.py', on,
        '"""organismo_v15c_on = organismo_v15c.py con `memoria_pares=\'combi\'` POR DEFECTO, para que las baterias lo\n'
        'examinen sin tocarlas. Generado por construye_v15c.py. NO editar."""\n')
    # ---------------- el mundo de regla
    srcg, sha14g = origen(os.path.join(ORG, 'organismo_v14g.py'))
    v15g = pon_memoria(srcg, 'P_', 'v15gc')
    hechos['organismo_v15gc.py'] = escribe('organismo_v15gc.py', v15g,
        f'"""organismo_v15gc = organismo/organismo_v14g.py ({sha14g}, solo se leyo) + perilla `memoria_pares`.\n'
        f'Con memoria_pares=None es organismo_v14g EXACTO. Generado por construye_v15c.py. NO editar."""\n')
    ong = sust(v15g, ",memoria_pares=None,mem_alfa=0.3", ",memoria_pares='combi',mem_alfa=0.3", etq='on: regla')
    hechos['organismo_v15gc_on.py'] = escribe('organismo_v15gc_on.py', ong,
        '"""organismo_v15gc_on = organismo_v15gc.py con la perilla FIJA en \'combi\'. Generado por construye_v15c.py."""\n')
    # ---------------- la bateria del examen
    srcb, shab = origen(os.path.join(ORG, 'bateria_v14.py'))
    b = sust(srcb, 'import organismo_v14 as v13   # TRONCO v14: hija dispersa + puerta por codigo',
             'import organismo_v15c as v13   # v15c: la perilla APAGADA (criterio 5: el examen se corre sobre v14 exacto)',
             n=2, etq='bat: import')
    b = sust(b, "'organismo_v14.py'", "'organismo_v15c.py'", n=2, etq='bat: sha')
    b = sust(b, "f'examen_v14_{stamp}.log'", "f'examen_v15c_{stamp}.log'", etq='bat: log')
    b = sust(b, "f'examen_v14_{stamp}.json'", "f'examen_v15c_{stamp}.json'", etq='bat: json')
    b = sust(b, "RAIZ = os.path.dirname(AQUI)   # tronco: organismo/ -> bundle/",
             "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # v15c: experimentos/creacion_A/ -> bundle/", etq='bat: RAIZ')
    b = sust(b, "sys.path[:0] = [_D14, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]",
             "sys.path[:0] = [_D14, AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'bug01')]",
             etq='bat: sys.path')
    hechos['bateria_v15c.py'] = escribe('bateria_v15c.py', b,
        f'"""bateria_v15c = organismo/bateria_v14.py ({shab}, CONGELADA: solo se leyo) sobre organismo_v15c con la\n'
        f'perilla APAGADA (criterio 5 del encargo). Las SEIS etapas y los umbrales del criterio v3\' INTACTOS.\n'
        f'Generado por construye_v15c.py. NO editar."""\n')
    # ---------------- la regresion de generalizacion
    srcg2, shag = origen(os.path.join(ORG, 'bateria_generaliza.py'))
    A = "    'organismo_v14': ('organismo_v14g', dict(eta_s=0.015, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)),   # TRONCO v14 (18 sep): hija dispersa + puerta por codigo, las DOS ON"
    if A not in srcg2:   # v14.1 pudo actualizar la entrada; se busca la que exista
        import re
        m = re.search(r"^ *'organismo_v14': \(.*$", srcg2, re.M)
        if not m: raise SystemExit('*** no encuentro la entrada organismo_v14 en INSTRUMENTOS')
        A = m.group(0)
    B = (A + "\n    'organismo_v15c_on': ('organismo_v15gc_on', dict(puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, "
         "ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)),   # v15c: la memoria de pares ENCENDIDA (eta_s/clip_s por defecto = v14.1)")
    g = sust(srcg2, A, B, etq='gen: INSTRUMENTOS')
    g = sust(g, "RAIZ = os.path.dirname(AQUI)", "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # v15c", etq='gen: RAIZ')
    g = sust(g, "f'regresion_generaliza_{modulo}_{stamp}.log'", "f'regresion_generaliza_v15c_{modulo}_{stamp}.log'", etq='gen: log')
    g = sust(g, "sys.path[:0] = [AQUI, GEN, os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]",
             "sys.path[:0] = [AQUI, GEN, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]",
             etq='gen: sys.path')
    import re as _re
    g = _re.sub(r"_dir = \{'organismo_v14g': [^,]+,", "_dir = {'organismo_v14g': os.path.join(RAIZ, 'organismo'), 'organismo_v15gc_on': AQUI,", g, count=1)
    hechos['bateria_generaliza_v15c.py'] = escribe('bateria_generaliza_v15c.py', g,
        f'"""bateria_generaliza_v15c = organismo/bateria_generaliza.py ({shag}, CONGELADA: solo se leyo) con UNA entrada\n'
        f'nueva en INSTRUMENTOS: organismo_v15c_on -> organismo_v15gc_on (la memoria de pares ENCENDIDA).\n'
        f'Umbrales G1/G2/K sin tocar. Generado por construye_v15c.py. NO editar."""\n')
    print(f'origen  organismo_v14.py {sha14}  organismo_v14g.py {sha14g}  bateria_v14.py {shab}  bateria_generaliza.py {shag}')
    for k, v in hechos.items():
        print(f'escrito {k:30s} {v}')
