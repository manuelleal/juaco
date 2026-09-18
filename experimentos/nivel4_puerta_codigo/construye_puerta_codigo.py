"""Construye los tres instrumentos del bloque "PUERTA POR EVIDENCIA DEL CODIGO EXACTO" (propuesta B-2 del creador B),
POR ANCLAS y sin tocar ningun original (todos se LEEN; organismo/organismo_v13.py esta CONGELADO):

  organismo_v13B.py   <- organismo/organismo_v13.py                    (cc8b16b492d4d324)   tronco candidato
  organismo_v13gB.py  <- experimentos/v13_dos_vias/organismo_v13g.py   (2a80e125f8593bf2)   mundo de regla (baterias)
  organismo_capB.py   <- experimentos/v13_reverificacion/organismo_capD13.py (fd8e10435801646c) mundo grande (capacidad)

PERILLAS (apagadas por defecto -> el original EXACTO, bit a bit):
  puerta_pat = n0 > 0   la boca consulta la via RAPIDA si el CODIGO EXACTO del patron ya fue mordido >= n0 veces.
                        Con puerta_pat = 0 rige la puerta de v13 (>= `puerta` celdas con |Wp-Wn| > 0.2).
  pat_shuf   = 1        CONTROL: la puerta lee la evidencia del codigo VECINO en el orden de aparicion (una rotacion
                        de los contadores entre codigos observados). Mismo multiconjunto de cuentas, asignadas mal.
                        Si la ganancia sobrevive al barajado, lo que actua es "abrir la puerta", no la evidencia.

MEMORIA QUE EXIGE: un entero por codigo visto (<= uno por estimulo aprendido) y el orden de aparicion. Cero por celda.
No toca Wp, Wn, KW ni el aprendizaje: solo el RUTEO entre las dos vias.

PROPIEDAD CONOCIDA, declarada antes de correr: los codigos CAMBIAN cuando hay divisiones, asi que un patron cuyo
codigo acaba de cambiar pierde su evidencia y vuelve a la via lenta hasta reunir n0 mordidas con el codigo nuevo.
Es parte del mecanismo (un codigo recien nacido ES nuevo), no un efecto colateral que se corrija despues.

Uso:  python experimentos/nivel4_puerta_codigo/construye_puerta_codigo.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


ESTADO = (
    "    ncod={}; _ord=[]   # B: evidencia del CODIGO EXACTO (mordidas por codigo) y orden de aparicion\n"
    "    def _key(_k): return frozenset(np.flatnonzero(_k).tolist())\n"
    "    def _ev(_k):   # evidencia que LEE la puerta: la propia, o (control) la del codigo vecino en el orden de aparicion\n"
    "        _q=_key(_k)\n"
    "        if not pat_shuf: return ncod.get(_q,0)\n"
    "        if _q not in ncod or len(_ord)<2: return 0\n"
    "        return ncod[_ord[(_ord.index(_q)+1)%len(_ord)]]\n"
    "    def _fam(_k):   # B: la puerta. puerta_pat>0 -> evidencia del codigo exacto; si no, celdas consolidadas (v13 EXACTO)\n"
    "        if puerta_pat: return _ev(_k)>=puerta_pat and int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=pat_min\n"
    "        return int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta\n")

CUENTA = ("                _ky=_key(kc)\n"
          "                if _ky not in ncod: _ord.append(_ky)\n"
          "                ncod[_ky]=ncod.get(_ky,0)+1   # B: evidencia del codigo exacto\n")


def pon_puerta(s, ancla_firma, nueva_firma, ancla_estado, ancla_mordida, ancla_ret, etiqueta):
    s = sust(s, ancla_firma, nueva_firma, etiqueta=f'{etiqueta}: firma')
    s = sust(s, ancla_estado, ancla_estado + ESTADO, etiqueta=f'{etiqueta}: estado')
    s = sust(s, "        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)",
             "        return _f+_s if puerta is None else (_f if _fam(_k) else _s)", etiqueta=f'{etiqueta}: valor')
    s = sust(s, "_wt=_wf+_ws if puerta is None else (_wf if int((np.abs(Wb[kc>0])>0.2).sum())>=puerta else _ws)",
             "_wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)", etiqueta=f'{etiqueta}: boca')
    s = sust(s, ancla_mordida, ancla_mordida + CUENTA, etiqueta=f'{etiqueta}: contador')
    s = sust(s, ancla_ret, ancla_ret.rstrip("\n") + "puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=len(ncod),\n",
             etiqueta=f'{etiqueta}: salida')
    return s


if __name__ == '__main__':
    salidas = []

    # ---- 1) organismo_v13B: el tronco candidato (organismo_v13 esta CONGELADO; solo se lee) ----
    s = origen(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'), 'cc8b16b492d4d324')
    s = pon_puerta(s,
                   "eta_s=0.015,clip_s=3.0,puerta=3):", "eta_s=0.015,clip_s=3.0,puerta=3,puerta_pat=0,pat_shuf=0,pat_min=0):",
                   "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)\n",
                   "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1\n",
                   "splits=splits,celdas=int(activa.sum()),\n", 'v13B')
    cab = ('"""organismo_v13B = organismo/organismo_v13.py (cc8b16b492d4d324, CONGELADO: solo se leyo) + puerta de\n'
           'familiaridad POR EVIDENCIA DEL CODIGO EXACTO (perilla puerta_pat) y su control barajado (pat_shuf).\n'
           'Generado por construye_puerta_codigo.py. NO editar a mano.\n'
           'Con puerta_pat=0 es organismo_v13 EXACTO (arnes: experimentos/nivel4_puerta_codigo/identidad_v13B.py)."""\n')
    d = os.path.join(AQUI, 'organismo_v13B.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ---- 2) organismo_v13gB: el mundo de regla que usa bateria_generaliza ----
    s = origen(os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py'), '2a80e125f8593bf2')
    s = pon_puerta(s,
                   "sonda_final=False):", "sonda_final=False,puerta_pat=0,pat_shuf=0,pat_min=0):",
                   "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)\n",
                   "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1\n",
                   "splits=splits,celdas=int(activa.sum()),\n", 'v13gB')
    cab = ('"""organismo_v13gB = experimentos/v13_dos_vias/organismo_v13g.py (2a80e125f8593bf2) + puerta por evidencia\n'
           'del codigo exacto (puerta_pat) y su control barajado (pat_shuf). Es el instrumento del MUNDO DE REGLA que\n'
           'usa bateria_generaliza_B.py. Generado por construye_puerta_codigo.py. NO editar.\n'
           'Con puerta_pat=0 es organismo_v13g EXACTO."""\n')
    d = os.path.join(AQUI, 'organismo_v13gB.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ---- 3) organismo_capB: el mundo grande (capacidad) ----
    s = origen(os.path.join(RAIZ, 'experimentos', 'v13_reverificacion', 'organismo_capD13.py'), 'fd8e10435801646c')
    s = pon_puerta(s,
                   ",eta_s=0.0,clip_s=3.0,puerta=None):", ",eta_s=0.0,clip_s=3.0,puerta=None,puerta_pat=0,pat_shuf=0,pat_min=0):",
                   "    Wps=np.zeros(D); Wns=np.zeros(D)   # v13: via LENTA lineal sobre la retina (inerte si eta_s=0)\n",
                   "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1; morc[kk]+=1\n",
                   "splits=splits,celdas=int(activa.sum()),\n", 'capB')
    s = sust(s, "    nofam_fin=sum(nofam(pats[n]) for n in tipos)   # v13: estimulos vivos que la puerta manda a la lenta al final\n",
             "    nofam_fin=sum(nofam(pats[n]) for n in tipos)   # v13: estimulos vivos que la puerta manda a la lenta al final\n"
             "    nofam_est={n:(0 if (puerta is None or _fam(kenyon(pats[n]))) else 1) for n in tipos}   # B: 1 = la puerta VIGENTE lo manda a la lenta\n"
             "    ncod_est={n:int(_ev(kenyon(pats[n]))) for n in tipos}   # B: evidencia que lee la puerta por estimulo\n",
             etiqueta='capB: diagnostico por estimulo')
    s = sust(s, "mv_tot=mv_tot,mc_tot=mc_tot,nofam_fin=nofam_fin)",
             "mv_tot=mv_tot,mc_tot=mc_tot,nofam_fin=nofam_fin,nofam_est=nofam_est,ncod_est=ncod_est)",
             etiqueta='capB: salida 2')
    cab = ('"""organismo_capB = experimentos/v13_reverificacion/organismo_capD13.py (fd8e10435801646c) + puerta por\n'
           'evidencia del codigo exacto (puerta_pat), su control barajado (pat_shuf) y diagnostico por estimulo.\n'
           'Generado por construye_puerta_codigo.py. NO editar. Con puerta_pat=0 es organismo_capD13 EXACTO."""\n')
    d = os.path.join(AQUI, 'organismo_capB.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ---- 4) bateria_generaliza_B: copia por anclas de la bateria, con las entradas nuevas de INSTRUMENTOS ----
    s = origen(os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'), '46772f5a582872c8')
    s = sust(s, "    'organismo_v13_rapido': ('organismo_v13q_rapido', dict(eta_s=0.015, puerta=3)),   # gemelo compilado del mundo de regla (identidad 81/81+243/243); mismo punto\n",
             "    'organismo_v13_rapido': ('organismo_v13q_rapido', dict(eta_s=0.015, puerta=3)),   # gemelo compilado del mundo de regla (identidad 81/81+243/243); mismo punto\n"
             "    'organismo_v13B': ('organismo_v13gB', dict(eta_s=0.015, puerta=3)),   # B-2: perilla APAGADA -> debe dar lo mismo que organismo_v13\n"
             "    'organismo_v13B_n5': ('organismo_v13gB', dict(eta_s=0.015, puerta=3, puerta_pat=5)),   # B-2: puerta por evidencia del codigo, n0=5\n"
             "    'organismo_v13B_n5c': ('organismo_v13gB', dict(eta_s=0.015, puerta=3, puerta_pat=5, pat_min=1)),   # B-2 enmienda 1: evidencia Y una celda consolidada\n",
             etiqueta='bateria: INSTRUMENTOS')
    s = sust(s, "sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))\n",
             "sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))\n"
             "sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'nivel4_puerta_codigo'))   # B-2: organismo_v13gB\n",
             etiqueta='bateria: sys.path')
    s = sust(s, "sha_organismo=h16(os.path.join(AQUI, modulo + '.py')),",
             "sha_organismo=(h16(os.path.join(AQUI, modulo + '.py')) if os.path.exists(os.path.join(AQUI, modulo + '.py')) else h16(os.path.join(_B2, modulo.split('_n5')[0] + '.py'))),",
             etiqueta='bateria: sha tolerante')
    s = sust(s, "    _dir = {'organismo_v11g': GEN, 'organismo_v13g': os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),\n",
             "    _dir = {'organismo_v11g': GEN, 'organismo_v13g': os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),\n"
             "            'organismo_v13gB': _B2,   # B-2\n", etiqueta='bateria: _dir')
    s = sust(s, "        f\"  organismo {h16(os.path.join(AQUI, (modulo if modulo != 'organismo_v13_rapido' else 'organismo_v13') + '.py'))}  esta bateria {h16(os.path.abspath(__file__))}\")",
             "        f\"  organismo {h16(os.path.join(AQUI, 'organismo_v13.py') if modulo in ('organismo_v13_rapido',) else (os.path.join(AQUI, modulo + '.py') if os.path.exists(os.path.join(AQUI, modulo + '.py')) else os.path.join(_B2, modulo.split('_n5')[0] + '.py')))}  esta bateria {h16(os.path.abspath(__file__))}\")",
             etiqueta='bateria: sha del organismo')
    s = sust(s, "AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(AQUI)\n",
             "AQUI = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'organismo')   # B-2: esta copia vive fuera de organismo/\n"
             "RAIZ = os.path.dirname(AQUI)\n", etiqueta='bateria: AQUI/RAIZ')
    s = sust(s, "REGLAS = ['px0', 'azar']\n",
             "REGLAS = ['px0', 'azar']\n_B2 = os.path.join(RAIZ, 'experimentos', 'nivel4_puerta_codigo')   # B-2\n",
             etiqueta='bateria: _B2')
    cab = ('"""bateria_generaliza_B = organismo/bateria_generaliza.py (46772f5a582872c8) con DOS entradas mas en\n'
           'INSTRUMENTOS (organismo_v13B y organismo_v13B_n5, ambas sobre organismo_v13gB) y el sha del organismo\n'
           'tolerante a que el modulo no viva en organismo/. Los UMBRALES y los criterios G1/G2/K no se tocan.\n'
           'Generado por construye_puerta_codigo.py. NO editar. La bateria original NO se modifico."""\n')
    d = os.path.join(AQUI, 'bateria_generaliza_B.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ---- 5) organismo_v13Bn5: organismo_v13B con la perilla ENCENDIDA por defecto (n0=5), para bateria_v13B ----
    #      n5  = PAT  (puerta_pat=5, pat_min=0): la propuesta B-2 tal cual
    #      n5c = PATC (puerta_pat=5, pat_min=1): ENMIENDA 1, evidencia del codigo Y al menos UNA celda consolidada
    base = origen(os.path.join(AQUI, 'organismo_v13B.py'), h16(os.path.join(AQUI, 'organismo_v13B.py')))
    for suf, pm, txt in [('n5', 0, 'puerta_pat = 5 POR DEFECTO (PAT: solo evidencia del codigo)'),
                         ('n5c', 1, 'puerta_pat = 5 y pat_min = 1 POR DEFECTO (PATC, enmienda 1: evidencia Y una celda consolidada)')]:
        s = sust(base, "puerta=3,puerta_pat=0,pat_shuf=0,pat_min=0):", f"puerta=3,puerta_pat=5,pat_shuf=0,pat_min={pm}):",
                 etiqueta=f'v13B{suf}: perilla encendida')
        d = os.path.join(AQUI, f'organismo_v13B{suf}.py')
        open(d, 'w', encoding='utf-8', newline='\n').write(
            f'"""organismo_v13B{suf} = organismo_v13B.py con {txt}. El mismo archivo con UNA constante cambiada, para\n'
            f'que bateria_v13B{"c" if pm else ""}.py lo examine con la perilla encendida sin tocar la bateria congelada.\n'
            'Generado por construye_puerta_codigo.py. NO editar."""\n' + s)
        salidas.append(d)

    # ---- 6) bateria_v13B / bateria_v13Bc: copias por anclas de la bateria del TRONCO (CONGELADA: solo se LEE) ----
    bat = origen(os.path.join(RAIZ, 'organismo', 'bateria_v13.py'), '1a027bcb37eb536e')
    for suf, mod in [('', 'organismo_v13Bn5'), ('c', 'organismo_v13Bn5c')]:
        s = sust(bat, "AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(AQUI)\n"
                      "sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]\n",
                 "_B2 = os.path.dirname(os.path.abspath(__file__))   # B-2: esta copia vive fuera de organismo/\n"
                 "AQUI = os.path.join(os.path.dirname(os.path.dirname(_B2)), 'organismo')\n"
                 "RAIZ = os.path.dirname(AQUI)\n"
                 "sys.path[:0] = [_B2, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]\n", etiqueta=f'bateria_v13B{suf}: rutas')
        s = sust(s, "    import organismo_v13 as v13\n", f"    import {mod} as v13   # B-2: puerta por evidencia del codigo\n",
                 n=2, etiqueta=f'bateria_v13B{suf}: import')
        s = s.replace("h16(os.path.join(AQUI, 'organismo_v13.py'))", f"h16(os.path.join(_B2, '{mod}.py'))")
        s = s.replace("f'examen_v13_{stamp}", "f'examen_v13B%s_{stamp}" % suf)
        cab = (f'"""bateria_v13B{suf} = organismo/bateria_v13.py (1a027bcb37eb536e, CONGELADO: solo se leyo) apuntando a\n'
               f'{mod} en vez de organismo_v13. CRITERIOS Y UMBRALES INTACTOS (criterio v3\').\n'
               f'Salida en datos/examen_v13B{suf}_<fecha>. Generado por construye_puerta_codigo.py. NO editar.\n'
               'La bateria original NO se modifico."""\n')
        d = os.path.join(AQUI, f'bateria_v13B{suf}.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
        salidas.append(d)

    for d in salidas:
        print(f"  {os.path.relpath(d, RAIZ):55s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
