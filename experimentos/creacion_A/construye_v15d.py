"""CREADOR A — candidato **v15d**: la variante honesta. La memoria de pares **NO sustituye** la lectura lineal de la
via lenta: la SUMA ('suma') o ELIGE entre las dos por su propio error ('ruta').

Por que (medido en v15c, 18-sep): sustituir rompio la generalizacion lineal del tronco — G1 0.500 / G2 0.513 contra
G1 >= 0.80 / G2 >= 0.85 de v14.1 — mientras xor01 subia a 0.812 estricta. El humo de v15c ya lo habia avisado con
una semilla (px0 0.900 -> 0.800). La lectura: una tabla sobre PARES no puede leer una regla lineal de UN pixel, asi
que la via lenta tiene que conservar la lineal, no cambiarla.

Genera, POR ANCLAS y sin tocar nada congelado (los originales SOLO se leen):
  organismo_v15d.py          <- organismo/organismo_v14.py    (TRONCO v14.1 CONGELADO)
  organismo_v15d_on.py       <- organismo_v15d.py con la perilla FIJA en 'suma'
  organismo_v15gd.py / _on   <- organismo/organismo_v14g.py   (mundo de regla)
  bateria_v15d.py            <- organismo/bateria_v14.py      sobre `organismo_v15d_on` (**la perilla ENCENDIDA**:
                                corrige el defecto de v15c, donde el examen midio la perilla apagada)
  bateria_generaliza_v15d.py <- organismo/bateria_generaliza.py (UNA entrada nueva; umbrales G1/G2/K intactos)

PERILLA `memoria_pares = None | 'suma' | 'ruta'`:
  estado: 15 celdas (pares) x 4 casillas + 15 visitas + 15 errores propios + **1 error propio de la LINEAL** = 136.
  'suma'  la via lenta devuelve   lineal(P) + tabla(P)      (la tabla ABSTIENE con 0.0 si no vio esa combinacion)
  'ruta'  devuelve la de MENOR error propio en el ultimo encuentro: lineal si `_ELv <= _MEv[ganadora]`, si no tabla
  None    devuelve `float((Wps-Wns)@P)` — la linea literal de v14.1; no se evalua nada nuevo y **no se toca el rng**
  Desempate de la celda ganadora AL AZAR con el `rng` DEL ORGANISMO, y solo se consume un numero cuando la perilla
  esta ENCENDIDA y hay empate de verdad.

Uso: python construye_v15d.py     (no corre nada)
"""
import os, hashlib, re

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


def pon(src, PP, etq):
    _fin = ",pat_shuf=0,pat_min=1):" if ",pat_shuf=0,pat_min=1):" in src else ",pat_shuf=0,pat_min=0):"
    out = sust(src, _fin, _fin[:-2] + ",memoria_pares=None,mem_alfa=0.3,mem_rho=0.02):", etq=f'{etq}: firma')
    A = "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)"
    B = (A + "\n"
         "    if memoria_pares not in (None,'suma','ruta'): raise ValueError(f\"memoria_pares={memoria_pares!r}\")   # v15d: perilla mal escrita no cae en silencio\n"
         "    _PARv=[(i,j) for i in range(6) for j in range(i+1,6)]   # v15d: las 15 celdas = pares de pixeles\n"
         "    _MMv=np.zeros((15,4)); _MNv=np.zeros((15,4)); _MEv=np.full(15,1e9); _MGv=0; _ELv=1e9   # v15d: valor, visitas, error por celda, ganadora, error de la LINEAL\n"
         "    def _tabla_v15(P):   # v15d: la lectura de la celda ganadora, con ABSTENCION explicita\n"
         "        _i,_j=_PARv[_MGv]; _c=int(P[_i])*2+int(P[_j])\n"
         "        return float(_MMv[_MGv,_c]) if _MNv[_MGv,_c]>0 else 0.0\n"
         "    def _lenta_v15(P):   # v15d: con la perilla APAGADA es literalmente la lectura de v14.1\n"
         "        if memoria_pares is None: return float((Wps-Wns)@P)\n"
         "        _l=float((Wps-Wns)@P)\n"
         "        if memoria_pares=='suma': return _l+_tabla_v15(P)   # SUMA: la lineal no se pierde\n"
         "        return _l if _ELv<=_MEv[_MGv] else _tabla_v15(P)   # RUTA: la de menor error propio")
    out = sust(out, A, B, etq=f'{etq}: estado')
    out = sust(out, "        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)",
               "        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=_lenta_v15(P)", etq=f'{etq}: valor')
    out = sust(out, f"_ws=float((Wps-Wns)@{PP}[kk])   # v13: las dos vias",
               f"_ws=_lenta_v15({PP}[kk])   # v13: las dos vias (v15d: lineal + tabla de pares si la perilla esta encendida)",
               etq=f'{etq}: mordida')
    A = ("                        _ds=dlt if puerta is None else R-_ws\n"
         f"                        if lam: _mcs=np.minimum(Wps,Wns)*({PP}[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs")
    B = ("                        _ds=dlt if puerta is None else R-_ws\n"
         "                        if memoria_pares is not None:   # v15d: escriben las 15 celdas (la primera vez, DE UN GOLPE) y se lleva el error de la LINEAL\n"
         f"                            _Pv={PP}[kk]\n"
         "                            _plv=float((Wps-Wns)@_Pv); _elv=R-_plv\n"
         "                            _ELv=(_elv*_elv) if _ELv>=1e9 else (1-mem_rho)*_ELv+mem_rho*(_elv*_elv)\n"
         "                            for _cv in range(15):\n"
         "                                _iv,_jv=_PARv[_cv]; _dv=int(_Pv[_iv])*2+int(_Pv[_jv])\n"
         "                                _pv=float(_MMv[_cv,_dv]) if _MNv[_cv,_dv]>0 else 0.0\n"
         "                                _erv=R-_pv; _prv=bool(_MNv[_cv].sum()==0)\n"
         "                                _MEv[_cv]=(_erv*_erv) if _prv else (1-mem_rho)*_MEv[_cv]+mem_rho*(_erv*_erv)\n"
         "                                if _MNv[_cv,_dv]==0: _MMv[_cv,_dv]=R\n"
         "                                else: _MMv[_cv,_dv]+=mem_alfa*(R-_MMv[_cv,_dv])\n"
         "                                _MNv[_cv,_dv]+=1\n"
         "                            _mnv=float(_MEv.min()); _empv=[int(_x) for _x in np.where(_MEv<=_mnv+1e-12)[0]]\n"
         "                            _MGv=_empv[0] if len(_empv)==1 else int(_empv[int(rng.integers(len(_empv)))])   # desempate al azar; solo consume rng si HAY empate\n"
         f"                        if lam: _mcs=np.minimum(Wps,Wns)*({PP}[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs")
    out = sust(out, A, B, etq=f'{etq}: actualizacion')
    out = sust(out, "    return dict(sobre=sobre,",
               "    return dict(memoria_pares=memoria_pares,"
               "mem_ganadora=(list(_PARv[_MGv]) if memoria_pares is not None else None),"
               "mem_tabla=([[float(_x) for _x in _f] for _f in _MMv] if memoria_pares is not None else None),"
               "mem_vistas=(int((_MNv>0).sum()) if memoria_pares is not None else None),"
               "mem_cobertura=(int((_MNv[_MGv]>0).sum()) if memoria_pares is not None else None),"
               "mem_err_lineal=(float(_ELv) if memoria_pares is not None else None),"
               "mem_err_tabla=(float(_MEv[_MGv]) if memoria_pares is not None else None),sobre=sobre,",
               etq=f'{etq}: return')
    return out


def escribe(n, t, cab):
    open(os.path.join(AQUI, n), 'w', encoding='utf-8').write(cab + t)
    return hashlib.sha256(open(os.path.join(AQUI, n), 'rb').read()).hexdigest()[:16]


if __name__ == '__main__':
    H = {}
    src, s14 = origen(os.path.join(ORG, 'organismo_v14.py'))
    v = pon(src, 'PAT', 'v15d')
    H['organismo_v15d.py'] = escribe('organismo_v15d.py', v,
        f'"""organismo_v15d = organismo/organismo_v14.py ({s14}, TRONCO v14.1 CONGELADO: solo se leyo) + perilla\n'
        f'`memoria_pares` = None | \'suma\' | \'ruta\'. La memoria de pares NO sustituye la lectura lineal: la SUMA o\n'
        f'ELIGE entre las dos por su propio error. Con None es organismo_v14 EXACTO y no se consume ni un numero del\n'
        f'rng (identidad: identidad_v15d.py). Generado por construye_v15d.py. NO editar a mano."""\n')
    on = sust(v, ",memoria_pares=None,mem_alfa=0.3", ",memoria_pares='suma',mem_alfa=0.3", etq='on: tronco')
    H['organismo_v15d_on.py'] = escribe('organismo_v15d_on.py', on,
        '"""organismo_v15d_on = organismo_v15d.py con `memoria_pares=\'suma\'` POR DEFECTO. Las baterias examinan ESTE\n'
        'modulo: el examen de v15c midio la perilla APAGADA y por eso no medía al candidato (defecto anotado).\n'
        'Generado por construye_v15d.py. NO editar."""\n')
    srcg, s14g = origen(os.path.join(ORG, 'organismo_v14g.py'))
    vg = pon(srcg, 'P_', 'v15gd')
    H['organismo_v15gd.py'] = escribe('organismo_v15gd.py', vg,
        f'"""organismo_v15gd = organismo/organismo_v14g.py ({s14g}, solo se leyo) + perilla `memoria_pares`.\n'
        f'Con None es organismo_v14g EXACTO. Generado por construye_v15d.py. NO editar."""\n')
    H['organismo_v15gd_on.py'] = escribe('organismo_v15gd_on.py',
        sust(vg, ",memoria_pares=None,mem_alfa=0.3", ",memoria_pares='suma',mem_alfa=0.3", etq='on: regla'),
        '"""organismo_v15gd_on = organismo_v15gd.py con la perilla FIJA en \'suma\'. Generado por construye_v15d.py."""\n')
    srcb, sb = origen(os.path.join(ORG, 'bateria_v14.py'))
    b = sust(srcb, 'import organismo_v14 as v13   # TRONCO v14: hija dispersa + puerta por codigo',
             'import organismo_v15d_on as v13   # v15d: la perilla ENCENDIDA (el examen mide AL CANDIDATO)', n=2, etq='bat: import')
    b = sust(b, "'organismo_v14.py'", "'organismo_v15d_on.py'", n=2, etq='bat: sha')
    b = sust(b, "f'examen_v14_{stamp}.log'", "f'examen_v15d_{stamp}.log'", etq='bat: log')
    b = sust(b, "f'examen_v14_{stamp}.json'", "f'examen_v15d_{stamp}.json'", etq='bat: json')
    b = sust(b, "RAIZ = os.path.dirname(AQUI)   # tronco: organismo/ -> bundle/",
             "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # v15d: experimentos/creacion_A/ -> bundle/", etq='bat: RAIZ')
    b = sust(b, "sys.path[:0] = [_D14, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]",
             "sys.path[:0] = [_D14, AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'bug01')]",
             etq='bat: sys.path')
    H['bateria_v15d.py'] = escribe('bateria_v15d.py', b,
        f'"""bateria_v15d = organismo/bateria_v14.py ({sb}, CONGELADA: solo se leyo) sobre **organismo_v15d_on**\n'
        f'(la perilla ENCENDIDA). Las SEIS etapas y los umbrales del criterio v3\' INTACTOS.\n'
        f'Generado por construye_v15d.py. NO editar."""\n')
    srcg2, sg = origen(os.path.join(ORG, 'bateria_generaliza.py'))
    m = re.search(r"^ *'organismo_v14': \(.*$", srcg2, re.M)
    if not m: raise SystemExit('*** no encuentro la entrada organismo_v14 en INSTRUMENTOS')
    A = m.group(0)
    g = sust(srcg2, A, A + "\n    'organismo_v15d_on': ('organismo_v15gd_on', dict(puerta=3, mask_rel=2, del_s=0.25, "
             "del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)),   # v15d: lineal + tabla de pares (suma)",
             etq='gen: INSTRUMENTOS')
    g = sust(g, "RAIZ = os.path.dirname(AQUI)", "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # v15d", etq='gen: RAIZ')
    g = sust(g, "f'regresion_generaliza_{modulo}_{stamp}.log'", "f'regresion_generaliza_v15d_{modulo}_{stamp}.log'", etq='gen: log')
    g = sust(g, "sys.path[:0] = [AQUI, GEN, os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]",
             "sys.path[:0] = [AQUI, GEN, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]",
             etq='gen: sys.path')
    g = re.sub(r"_dir = \{'organismo_v14g': [^,]+,", "_dir = {'organismo_v14g': os.path.join(RAIZ, 'organismo'), 'organismo_v15gd_on': AQUI,", g, count=1)
    H['bateria_generaliza_v15d.py'] = escribe('bateria_generaliza_v15d.py', g,
        f'"""bateria_generaliza_v15d = organismo/bateria_generaliza.py ({sg}, CONGELADA: solo se leyo) con UNA entrada\n'
        f'nueva: organismo_v15d_on -> organismo_v15gd_on. Umbrales G1/G2/K sin tocar.\n'
        f'Generado por construye_v15d.py. NO editar."""\n')
    print(f'origen organismo_v14.py {s14}  organismo_v14g.py {s14g}  bateria_v14.py {sb}  bateria_generaliza.py {sg}')
    for k, val in H.items(): print(f'escrito {k:30s} {val}')
