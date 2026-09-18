"""CREADOR A — candidato **v15f**: tabla de pares con R CRUDO + SOBRESCRITURA + RELEVO a la lineal por abstencion,
cada via con su propio error. Es el candidato que dejo A16 tras v15e.

Por que (medido, 18-sep): v15e (residuo R - lineal en la tabla, lectura lineal + residuo) arreglo E1 y E2 (W_B -3 20/20,
reversion 20/20) pero perdio XOR (V2b xor01 0.500): con residuos el error propio de la celda buena (0,1) deja de ser 0 y
pasa a ser la deriva de una lineal que no puede con XOR, y el prior de pares pierde su identificabilidad. v15c/v15d (R crudo)
si identificaban (0,1) 19-20/20 pero doblaban la cuenta (v15d) o escribian de un golpe sin desdecirse (v15c/v15d).

v15f (perilla `memoria_pares = None | 'relevo'`, `mem_alfa = 1.0`):
  tabla (15 pares x 4 casillas)   guarda R CRUDO; SOBRESCRITURA en cada mordida (la casilla sigue a la ULTIMA recompensa)
  lectura de la via lenta         RELEVO: la casilla de la celda ganadora si esa combinacion se vio; si no, la LINEAL
                                  (la abstencion cae hacia la lineal, no hacia 0.0)
  la via rapida                   aprende de SU error: dlt = R - _wf          (linea de v14.1, sin tocar)
  la lineal                       aprende de SU error: _ds = R - lineal(P)    (apagada: == R - _ws bit a bit)
  celda ganadora                  menor error propio de la casilla SOLA (el criterio de M3), EMA mem_rho, desempate al
                                  azar con el rng del organismo (solo consume rng si hay empate y la perilla esta ON)
  None                            la linea literal de v14.1; nada nuevo se evalua y no se toca el rng (identidad_v15f.py)

Genera, POR ANCLAS y sin tocar nada congelado (los originales SOLO se leen; nada de v15c/d/e se sobrescribe):
  organismo_v15f.py / _on.py     <- organismo/organismo_v14.py    (TRONCO v14.1 CONGELADO)
  organismo_v15gf.py / _on.py    <- organismo/organismo_v14g.py   (mundo de regla)
  bateria_v15f.py                <- organismo/bateria_v14.py      sobre `organismo_v15f_on` (+ sha de v11/v10 desde organismo/)
  bateria_generaliza_v15f.py     <- organismo/bateria_generaliza.py (entrada nueva = entrada del tronco CAMPO A CAMPO, regla 14)
Uso: python construye_v15f.py     (no corre nada)
"""
import os, hashlib, re

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')

# Regla 14 (ERR-38): la entrada nueva de bateria_generaliza lleva TODOS los campos de la entrada del tronco, explicitos.
KW14 = dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)


def origen(ruta):
    b = open(ruta, 'rb').read()
    return b.decode('utf-8'), hashlib.sha256(b).hexdigest()[:16]


def sust(t, a, b, n=1, etq=''):
    c = t.count(a)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return t.replace(a, b)


def pon(src, PP, etq):
    """Aplica las anclas de v15f. `PP` es como el organismo accede al patron actual: 'PAT' (tronco) o 'P_' (mundo de regla)."""
    _fin = ",pat_shuf=0,pat_min=1):" if ",pat_shuf=0,pat_min=1):" in src else ",pat_shuf=0,pat_min=0):"
    out = sust(src, _fin, _fin[:-2] + ",memoria_pares=None,mem_alfa=1.0,mem_rho=0.02):", etq=f'{etq}: firma')
    # 1) estado + lecturas
    A = "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)"
    B = (A + "\n"
         "    if memoria_pares not in (None,'relevo'): raise ValueError(f\"memoria_pares={memoria_pares!r}\")   # v15f: perilla mal escrita no cae en silencio\n"
         "    _PARv=[(i,j) for i in range(6) for j in range(i+1,6)]   # v15f: las 15 celdas = pares de pixeles\n"
         "    _MMv=np.zeros((15,4)); _MNv=np.zeros((15,4)); _MEv=np.full(15,1e9); _MGv=0   # v15f: R CRUDO por casilla, visitas, error propio por celda, ganadora\n"
         "    def _lin_v15f(P): return float((Wps-Wns)@P)   # v15f: la lectura lineal sola (la expresion literal de v14.1)\n"
         "    def _tabla_v15f(P):   # v15f: (valor, visto) de la casilla de la celda ganadora\n"
         "        _i,_j=_PARv[_MGv]; _c=int(P[_i])*2+int(P[_j])\n"
         "        return (float(_MMv[_MGv,_c]), True) if _MNv[_MGv,_c]>0 else (0.0, False)\n"
         "    def _lenta_v15f(P):   # v15f: apagada = literalmente v14.1; 'relevo' = la tabla si conoce la combinacion, si no la lineal\n"
         "        if memoria_pares is None: return float((Wps-Wns)@P)\n"
         "        _tv,_vv=_tabla_v15f(P)\n"
         "        return _tv if _vv else _lin_v15f(P)")
    out = sust(out, A, B, etq=f'{etq}: estado')
    # 2) la lectura dentro de valor()
    out = sust(out, "        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)",
               "        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=_lenta_v15f(P)", etq=f'{etq}: valor')
    # 3) la lectura en la mordida
    out = sust(out, f"_ws=float((Wps-Wns)@{PP}[kk])   # v13: las dos vias",
               f"_ws=_lenta_v15f({PP}[kk])   # v13: las dos vias (v15f: tabla si conoce la combinacion, si no la lineal)",
               etq=f'{etq}: mordida')
    # 4) la lineal aprende de SU PROPIO error (R - lineal). Apagada: _lbv == _ws bit a bit (la misma expresion).
    out = sust(out, "                        _ds=dlt if puerta is None else R-_ws\n",
               f"                        _lbv=_lin_v15f({PP}[kk]); _ds=dlt if puerta is None else R-_lbv   # v15f: la lineal aprende de SU error (apagada: _lbv == _ws)\n",
               etq=f'{etq}: error lineal')
    # 5) la tabla: R crudo, sobrescritura, error propio de la casilla sola (M3)
    A = (f"                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*{PP}[kk],0,clip_s)\n"
         f"                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*{PP}[kk],0,clip_s)\n")
    B = (A +
         "                        if memoria_pares is not None:   # v15f: las 15 celdas escriben R CRUDO por sobrescritura; el error propio es el de la casilla sola\n"
         f"                            _Pv={PP}[kk]\n"
         "                            for _cv in range(15):\n"
         "                                _iv,_jv=_PARv[_cv]; _dv=int(_Pv[_iv])*2+int(_Pv[_jv])\n"
         "                                _pv=float(_MMv[_cv,_dv]) if _MNv[_cv,_dv]>0 else 0.0   # lo que ESA casilla habria dicho (0.0 si no se vio: M3)\n"
         "                                _erv=R-_pv; _prv=bool(_MNv[_cv].sum()==0)\n"
         "                                _MEv[_cv]=(_erv*_erv) if _prv else (1-mem_rho)*_MEv[_cv]+mem_rho*(_erv*_erv)   # error propio de la celda (EMA)\n"
         "                                if _MNv[_cv,_dv]==0 or mem_alfa>=1.0: _MMv[_cv,_dv]=R   # SOBRESCRITURA: la casilla sigue a la ultima recompensa\n"
         "                                else: _MMv[_cv,_dv]+=mem_alfa*(R-_MMv[_cv,_dv])\n"
         "                                _MNv[_cv,_dv]+=1\n"
         "                            _mnv=float(_MEv.min()); _empv=[int(_x) for _x in np.where(_MEv<=_mnv+1e-12)[0]]\n"
         "                            _MGv=_empv[0] if len(_empv)==1 else int(_empv[int(rng.integers(len(_empv)))])   # desempate al azar con el rng del organismo; solo consume rng si HAY empate\n")
    out = sust(out, A, B, etq=f'{etq}: tabla')
    # 6) el return (lecturas; con la perilla apagada las claves nuevas valen None o son lecturas puras sin rng)
    out = sust(out, "    return dict(sobre=sobre,",
               "    return dict(memoria_pares=memoria_pares,mem_alfa=mem_alfa,"
               "mem_ganadora=(list(_PARv[_MGv]) if memoria_pares is not None else None),"
               "mem_tabla=([[float(_x) for _x in _f] for _f in _MMv] if memoria_pares is not None else None),"
               "mem_vistas=(int((_MNv>0).sum()) if memoria_pares is not None else None),"
               "mem_cobertura=(int((_MNv[_MGv]>0).sum()) if memoria_pares is not None else None),"
               "mem_err_tabla=(float(_MEv[_MGv]) if memoria_pares is not None else None),"
               f"W_tabla=({{k:(round(_tabla_v15f({PP}[k])[0],3) if _tabla_v15f({PP}[k])[1] else None) for k in {PP}}} if memoria_pares is not None else None),"
               f"mem_fam=({{k:bool(_fam(kenyon({PP}[k]))) for k in {PP}}} if puerta is not None else None),"
               f"mem_ev={{k:int(_ev(kenyon({PP}[k]))) for k in {PP}}},sobre=sobre,",
               etq=f'{etq}: return')
    return out


def escribe(n, t, cab):
    ruta = os.path.join(AQUI, n)
    open(ruta, 'w', encoding='utf-8', newline='\n').write(cab + t)
    return hashlib.sha256(open(ruta, 'rb').read()).hexdigest()[:16]


if __name__ == '__main__':
    H = {}
    src, s14 = origen(os.path.join(ORG, 'organismo_v14.py'))
    v = pon(src, 'PAT', 'v15f')
    H['organismo_v15f.py'] = escribe('organismo_v15f.py', v,
        f'"""organismo_v15f = organismo/organismo_v14.py ({s14}, TRONCO v14.1 CONGELADO: solo se leyo) + perilla\n'
        f'`memoria_pares` = None | \'relevo\' (mem_alfa=1.0): tabla de pares con R CRUDO y sobrescritura; la via lenta lee la tabla si\n'
        f'conoce la combinacion y si no la lineal; cada via aprende de su propio error. Con None es organismo_v14 EXACTO y no se\n'
        f'consume ni un numero del rng (identidad_v15f.py). Generado por construye_v15f.py. NO editar a mano."""\n')
    on = sust(v, ",memoria_pares=None,mem_alfa=1.0", ",memoria_pares='relevo',mem_alfa=1.0", etq='on: tronco')
    H['organismo_v15f_on.py'] = escribe('organismo_v15f_on.py', on,
        '"""organismo_v15f_on = organismo_v15f.py con `memoria_pares=\'relevo\'` POR DEFECTO. Las baterias examinan ESTE modulo\n'
        '(la perilla ENCENDIDA). Generado por construye_v15f.py. NO editar."""\n')
    srcg, s14g = origen(os.path.join(ORG, 'organismo_v14g.py'))
    vg = pon(srcg, 'P_', 'v15gf')
    H['organismo_v15gf.py'] = escribe('organismo_v15gf.py', vg,
        f'"""organismo_v15gf = organismo/organismo_v14g.py ({s14g}, solo se leyo) + perilla `memoria_pares` (v15f).\n'
        f'Con None es organismo_v14g EXACTO. Generado por construye_v15f.py. NO editar."""\n')
    H['organismo_v15gf_on.py'] = escribe('organismo_v15gf_on.py',
        sust(vg, ",memoria_pares=None,mem_alfa=1.0", ",memoria_pares='relevo',mem_alfa=1.0", etq='on: regla'),
        '"""organismo_v15gf_on = organismo_v15gf.py con la perilla FIJA en \'relevo\'. Generado por construye_v15f.py."""\n')
    # ---- bateria del examen (criterio v3'), sobre el candidato ENCENDIDO ----
    srcb, sb = origen(os.path.join(ORG, 'bateria_v14.py'))
    b = sust(srcb, 'import organismo_v14 as v13   # TRONCO v14: hija dispersa + puerta por codigo',
             'import organismo_v15f_on as v13   # v15f: la perilla ENCENDIDA (el examen mide AL CANDIDATO)', n=2, etq='bat: import')
    b = sust(b, "'organismo_v14.py'", "'organismo_v15f_on.py'", n=2, etq='bat: sha')
    b = sust(b, "f'examen_v14_{stamp}.log'", "f'examen_v15f_{stamp}.log'", etq='bat: log')
    b = sust(b, "f'examen_v14_{stamp}.json'", "f'examen_v15f_{stamp}.json'", etq='bat: json')
    b = sust(b, "RAIZ = os.path.dirname(AQUI)   # tronco: organismo/ -> bundle/",
             "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # v15f: experimentos/creacion_A/ -> bundle/", etq='bat: RAIZ')
    b = sust(b, "sys.path[:0] = [_D14, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]",
             "sys.path[:0] = [os.path.join(RAIZ, 'organismo'), _D14, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]   # v15f: organismo/ PRIMERO (ERR-28)",
             etq='bat: sys.path')
    b = sust(b, "sha_organismo_v11=h16(os.path.join(AQUI, 'organismo_v11.py')), sha_organismo_v10=h16(os.path.join(AQUI, 'organismo_v10.py'))",
             "sha_organismo_v11=h16(os.path.join(RAIZ, 'organismo', 'organismo_v11.py')), sha_organismo_v10=h16(os.path.join(RAIZ, 'organismo', 'organismo_v10.py'))",
             etq='bat: sha v11/v10 (en la copia AQUI no es organismo/: sin esto el JSON no se escribe)')
    H['bateria_v15f.py'] = escribe('bateria_v15f.py', b,
        f'"""bateria_v15f = organismo/bateria_v14.py ({sb}, CONGELADA: solo se leyo) sobre **organismo_v15f_on** (la perilla\n'
        f'ENCENDIDA). Las SEIS etapas y los umbrales del criterio v3\' INTACTOS. Unica diferencia de instrumento: el sha de\n'
        f'organismo_v11/v10 del meta se lee de organismo/ (como en bateria_v15e). Generado por construye_v15f.py. NO editar."""\n')
    # ---- bateria de generalizacion: UNA entrada nueva, comparada campo a campo con la del tronco (regla 14) ----
    srcg2, sg = origen(os.path.join(ORG, 'bateria_generaliza.py'))
    m = re.search(r"^ *'organismo_v14': \('organismo_v14g', (dict\(.*?\))\),", srcg2, re.M)
    if not m: raise SystemExit('*** no encuentro la entrada organismo_v14 en INSTRUMENTOS')
    kw_tronco = eval(m.group(1), {'__builtins__': {}, 'dict': dict})
    if kw_tronco != KW14:
        raise SystemExit(f'*** REGLA 14: la entrada del tronco {kw_tronco} no coincide campo a campo con KW14 {KW14}. No se escribe nada.')
    A = re.search(r"^ *'organismo_v14': \(.*$", srcg2, re.M).group(0)   # la linea ENTERA del tronco (con su comentario) queda intacta
    kw_txt = ', '.join(f'{k}={v!r}' for k, v in KW14.items())
    g = sust(srcg2, A, A + f"\n    'organismo_v15f_on': ('organismo_v15gf_on', dict({kw_txt})),   # v15f: los MISMOS campos que la entrada del tronco (regla 14 / ERR-38), explicitos",
             etq='gen: INSTRUMENTOS')
    g = sust(g, "RAIZ = os.path.dirname(AQUI)", "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # v15f", etq='gen: RAIZ')
    g = sust(g, "f'regresion_generaliza_{modulo}_{stamp}.log'", "f'regresion_generaliza_v15f_{modulo}_{stamp}.log'", etq='gen: log')
    g = sust(g, "f'regresion_generaliza_{modulo}_{stamp}.json'", "f'regresion_generaliza_v15f_{modulo}_{stamp}.json'", etq='gen: json')
    g = sust(g, "sys.path[:0] = [AQUI, GEN, os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]",
             "sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI, GEN, os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]   # v15f: organismo/ PRIMERO (ERR-28)",
             etq='gen: sys.path')
    g = re.sub(r"_dir = \{'organismo_v14g': [^,]+,", "_dir = {'organismo_v14g': os.path.join(RAIZ, 'organismo'), 'organismo_v15gf_on': AQUI,", g, count=1)
    H['bateria_generaliza_v15f.py'] = escribe('bateria_generaliza_v15f.py', g,
        f'"""bateria_generaliza_v15f = organismo/bateria_generaliza.py ({sg}, CONGELADA: solo se leyo) con UNA entrada\n'
        f'nueva: organismo_v15f_on -> organismo_v15gf_on, con los MISMOS campos que la entrada del tronco (regla 14 / ERR-38),\n'
        f'verificados campo a campo por el constructor. Umbrales G1/G2/K sin tocar. Generado por construye_v15f.py. NO editar."""\n')
    print(f'origen organismo_v14.py {s14}  organismo_v14g.py {s14g}  bateria_v14.py {sb}  bateria_generaliza.py {sg}')
    print(f'regla 14: entrada nueva == entrada del tronco campo a campo: {kw_tronco == KW14}  {KW14}')
    for k, val in H.items(): print(f'escrito {k:30s} {val}')
