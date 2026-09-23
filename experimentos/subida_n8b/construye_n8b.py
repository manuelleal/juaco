"""Genera, POR ANCLAS (conteo exacto), los dos archivos del instrumento de subida_n8b (nivel 8, tanda 2):

  organismo_n8b.py  <- experimentos/subida_n8/organismo_flujo.py (sha 14afed5aa16e09bf; solo se lee)
  mundo_n8b.py      <- experimentos/subida_n8/mundo_n8.py        (sha b0b57d7ff02afe4e; solo se lee)

organismo_n8b: DOS perillas nuevas, `recicla` y `prueba`, APAGADAS por defecto (las dos en 0 -> organismo_flujo EXACTO).
  Organo de RECICLAJE POR RELEVANCIA (distinto de la fusion de subida_n8, que queda medida en negativo):
  cuando una celda cumple la condicion de division por conflicto de signo de v11 PERO no queda celda libre,
  se LIBERA una celda activa que no es del codigo actual y la division sigue como siempre (la hija ocupa ese lugar).
    recicla=1  la de MENOR relevancia |Wp - Wn| (la que menos valor consolidado lleva; empate -> indice menor)
    recicla=3  la que entra en MENOS codigos familiares (codigos exactos con evidencia ncod >= puerta_pat: memoria que
               el tronco ya tiene); empate -> menor |Wp-Wn|; empate -> indice menor. Protege lo ya reconocido.
    recicla=2  (control que puede ganar) una al AZAR entre las mismas candidatas, con un generador APARTE
               np.random.default_rng([semilla, 8118]) (no toca el rng del mundo ni del organismo)
  Liberar = poner a cero KW, mu, mup, mun, Wp, Wn, zp, zn, err de esa celda, marcarla libre y OLVIDAR la evidencia
  por codigo exacto (ncod) de los codigos que la contenian (si no, el indice reusado heredaria evidencia ajena).
  Memoria nueva: CERO (solo contadores de lectura). Constantes nuevas: CERO. No lee valencias, R_VAL ni el plan.

  Organo de PRUEBA (perilla `prueba`): al decidir morder, lo que la puerta de v13/B-2 NO reconoce (codigo exacto con menos
  de puerta_pat mordidas) vale 0, no el a priori de la via lenta (que en este mundo dice "veneno" casi siempre: neofobia).
    prueba=1  lectura neutra para lo NO reconocido
    prueba=2  (control que puede ganar) lectura neutra en encuentros AL AZAR, a la misma tasa que el organismo lleva de
              encuentros no reconocidos (dos contadores), generador APARTE np.random.default_rng([semilla, 8228])
  Solo cambia la decision de morder: el aprendizaje (dlt = R - _wf) y la medida (valor_tot) no se tocan.
  Memoria nueva: CERO (prueba=1); dos contadores (prueba=2, control). Constantes nuevas: CERO.

mundo_n8b: el mismo mundo en flujo con el PESO del patron como parametro y el mundo largo por defecto:
  retina 13 pixeles, patrones de peso 4 (C(13,4) = 715), 500 estimulos nuevos, T = 500 000.
  Con d_pix=12, peso=3, n_est=200 es mundo_n8 EXACTO (identidad_n8b.py).
Uso: python experimentos/subida_n8b/construye_n8b.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN_ORG = os.path.join(RAIZ, 'experimentos', 'subida_n8', 'organismo_flujo.py')
SHA_ORIGEN_ORG = '14afed5aa16e09bf'
ORIGEN_MUN = os.path.join(RAIZ, 'experimentos', 'subida_n8', 'mundo_n8.py')
SHA_ORIGEN_MUN = 'b0b57d7ff02afe4e'
DEST_ORG = os.path.join(AQUI, 'organismo_n8b.py')
DEST_MUN = os.path.join(AQUI, 'mundo_n8b.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:50]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def construir_org():
    if h16(ORIGEN_ORG) != SHA_ORIGEN_ORG:
        raise SystemExit(f"ORIGEN organismo: sha {h16(ORIGEN_ORG)}, se esperaba {SHA_ORIGEN_ORG}. Abortado.")
    s = open(ORIGEN_ORG, encoding='utf-8').read()
    # 1) firma: perilla nueva al final, apagada
    s = sust(s, "ventana=0,p_viejo=0.25,fusion=0):", "ventana=0,p_viejo=0.25,fusion=0,recicla=0,prueba=0):", etiqueta='firma')
    # 2) organo de reciclaje (definido una vez, antes del bucle; opera EN SITIO sobre los arreglos vivos)
    s = sust(s, "    def _key(_k): return frozenset(np.flatnonzero(_k).tolist())",
             "    _nrec=[0]; _rec_log=[]; _rngr=np.random.default_rng([int(seed),8118]) if recicla==2 else None   # n8b: contadores y generador APARTE del control azar\n"
             "    def _reciclar(_excl,_t):   # n8b: RECICLAJE -- libera la celda activa de menor relevancia |Wp-Wn| fuera del codigo actual\n"
             "        _cand=np.array([c2 for c2 in np.flatnonzero(activa) if c2 not in _excl])\n"
             "        if len(_cand)<1: return False\n"
             "        if recicla==2: b=int(_cand[int(_rngr.integers(len(_cand)))])\n"
             "        elif recicla==3:   # uso: la que entra en MENOS codigos familiares (ncod >= puerta_pat); empate -> menor |Wp-Wn|\n"
             "            _uso=np.zeros(NKMAX)\n"
             "            for _q,_nq in ncod.items():\n"
             "                if _nq>=puerta_pat: _uso[list(_q)]+=1\n"
             "            _o=np.lexsort((np.abs((Wp-Wn)[_cand]),_uso[_cand])); b=int(_cand[int(_o[0])])\n"
             "        else: b=int(_cand[int(np.argmin(np.abs((Wp-Wn)[_cand])))])\n"
             "        _rel=float(abs(Wp[b]-Wn[b]))\n"
             "        for _A in (KW,mu,mup,mun): _A[b]=0.0\n"
             "        for _v in (Wp,Wn,zp,zn,err): _v[b]=0.0\n"
             "        activa[b]=False\n"
             "        for _q in [q2 for q2 in ncod if b in q2]:\n"
             "            del ncod[_q]\n"
             "            if _q in _ord: _ord.remove(_q)\n"
             "        _nrec[0]+=1; _rec_log.append((int(_t),b,round(_rel,4)))\n"
             "        return True\n"
             "    def _key(_k): return frozenset(np.flatnonzero(_k).tolist())",
             etiqueta='organo de reciclaje')
    # 3) disparo: misma condicion que la division de v11, pero sin celda libre (inmediatamente antes de la division)
    s = sust(s, "                                if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():",
             "                                if recicla and Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and not (~activa).any(): _reciclar(set(int(i2) for i2 in idx),t)   # n8b\n"
             "                                if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():",
             etiqueta='disparo del reciclaje')
    # 3b) PRUEBA en la boca: lo que la puerta NO reconoce vale 0 al decidir morder (no el a priori de la via lenta).
    #     Solo cambia la decision de morder; el aprendizaje (dlt = R - _wf, _ds = R - _ws) y la medida (valor_tot) no se tocan.
    #     prueba=2 (control que puede ganar): la misma lectura neutra, pero en encuentros AL AZAR, a la tasa que el propio
    #     organismo lleva de encuentros no reconocidos (dos contadores; generador aparte [semilla, 8228]).
    s = sust(s, "            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13\n",
             "            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13\n"
             "            if prueba and puerta is not None:   # n8b: PRUEBA\n"
             "                _nf=not _fam(kc); _enc[0]+=1; _enc[1]+=int(_nf)\n"
             "                if (prueba==1 and _nf) or (prueba==2 and _rngp.random()<_enc[1]/_enc[0]): _wt=0.0; _npru[0]+=1\n",
             etiqueta='prueba en la boca')
    s = sust(s, "    _nrec=[0]; _rec_log=[];",
             "    _npru=[0]; _enc=[0,0]; _rngp=np.random.default_rng([int(seed),8228]) if prueba==2 else None   # n8b: PRUEBA (contadores; generador APARTE del control)\n"
             "    _nrec=[0]; _rec_log=[];", etiqueta='contadores prueba')
    # 4) lectura
    s = sust(s, "n_fus=_nfus[0],fus_log=_fus_log,", "n_fus=_nfus[0],fus_log=_fus_log,n_rec=_nrec[0],rec_log=_rec_log,recicla=recicla,prueba=prueba,n_prueba=_npru[0],enc_nofam=_enc[1],enc_tot=_enc[0],",
             etiqueta='salida')
    cab = ('"""organismo_n8b = experimentos/subida_n8/organismo_flujo.py (14afed5aa16e09bf) + perillas `recicla` (organo de\n'
           'reciclaje) y `prueba` (lectura neutra de lo no reconocido en la boca), nivel 8 tanda 2. Generado por\n'
           'construye_n8b.py. NO editar. Con recicla=0 y prueba=0 es organismo_flujo EXACTO (identidad_n8b.py)."""\n')
    return cab + s


def construir_mun():
    if h16(ORIGEN_MUN) != SHA_ORIGEN_MUN:
        raise SystemExit(f"ORIGEN mundo: sha {h16(ORIGEN_MUN)}, se esperaba {SHA_ORIGEN_MUN}. Abortado.")
    s = open(ORIGEN_MUN, encoding='utf-8').read()
    s = sust(s, "D_PIX = 12\nN_EST = 200\n", "D_PIX = 13\nN_EST = 500\nPESO = 4\n", etiqueta='constantes')
    s = sust(s, "def mundo(semilla, n_est=N_EST, d_pix=D_PIX, reciclado=False, n0=N0_RECICLADO):",
             "def mundo(semilla, n_est=N_EST, d_pix=D_PIX, reciclado=False, n0=N0_RECICLADO, peso=PESO):", etiqueta='firma mundo')
    s = sust(s, "combos = list(itertools.combinations(range(d_pix), 3))",
             "combos = list(itertools.combinations(range(d_pix), peso))", etiqueta='peso')
    s = sust(s, 'f"C({d_pix},3)={len(combos)} < n_est={n_est}"', 'f"C({d_pix},{peso})={len(combos)} < n_est={n_est}"',
             etiqueta='mensaje')
    cab = ('"""mundo_n8b = experimentos/subida_n8/mundo_n8.py (b0b57d7ff02afe4e) con el peso del patron como parametro y el\n'
           'mundo LARGO por defecto (retina 13, peso 4, 500 estimulos). Generado por construye_n8b.py. NO editar.\n'
           'Con d_pix=12, peso=3, n_est=200 es mundo_n8 EXACTO (identidad_n8b.py)."""\n')
    return cab + s


if __name__ == '__main__':
    for dest, txt in ((DEST_ORG, construir_org()), (DEST_MUN, construir_mun())):
        open(dest, 'w', encoding='utf-8', newline='\n').write(txt)
        print(f"  {os.path.relpath(dest, RAIZ)}  {h16(dest)}  {txt.count(chr(10))} lineas")
