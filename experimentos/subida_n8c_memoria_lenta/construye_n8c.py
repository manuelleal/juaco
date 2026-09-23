"""Genera experimentos/subida_n8c_memoria_lenta/organismo_repaso.py POR ANCLAS desde
experimentos/subida_n8/organismo_flujo.py (sha 14afed5aa16e09bf, instrumento de la tanda 1 del nivel 8, anclado al
tronco congelado organismo_v142; solo se lee).

Una perilla nueva, APAGADA por defecto (con repaso=0 el archivo es organismo_flujo EXACTO en toda salida):
  repaso (organo de nivel 8, pieza 2 "retener lo ausente"; sistemas complementarios, McClelland, McNaughton y O'Reilly
  1995; Kumaran, Hassabis y McClelland 2016; repaso generativo, Shin et al. 2017):
    tras CADA mordida real (repaso despierto tras la recompensa; Foster y Wilson 2006; presupuesto = `dosis` repasos por
    mordida: 1 o 10, las dos dosis de la practica; sin energia, sin tocar el rng del organismo ni el del mundo) el organismo REPASA una huella: elige una celda activa con huella (zp+zn > 0) con un generador APARTE [semilla, 8338], sortea el
    signo de la huella en proporcion zp:zn, reconstruye el patron P^ = los round(masa) pixeles mas altos de la media
    condicionada (mup/zp si positiva, mun/zn si negativa; memoria que el tronco YA tiene, la "huella rapida") y aplica
    UNA actualizacion Rescorla-Wagner sobre code(P^) en los pesos de valor Wp/Wn (la regla de la mordida: drenaje lam de
    la parte comun, eta, aversion, clip 3). No divide, no funde, no toca mu/err/mup/mun/zp/zn, ni ncod (la evidencia de
    la puerta sigue siendo SOLO de mordidas reales), ni la via lenta.
      repaso=1 REP      objetivo = la ultima R positiva / negativa vivida (2 numeros nuevos) segun el signo de la huella
      repaso=2 BARAJ    (control que puede ganar) el mismo patron P^, pero el SIGNO del objetivo sale de la huella de
                        OTRA celda sorteada (contenido barajado; misma proporcion de + y - en promedio, mismo presupuesto)
      repaso=3 SINHUE   (control "repaso sin consolidacion de la huella", K6 de v11_consolidacion) el mismo P^, objetivo
                        = K * (Wp[c]-Wn[c]) de la celda elegida: repasa el valor ACTUAL, no la huella
Memoria nueva declarada: 2 numeros (ultima R positiva y ultima R negativa vividas). Constante nueva: `dosis`
(1 o 10; en practica, 15890-15891, se probo un repaso cada 20 pasos, unos 10 por mordida, y 1 por mordida. Declarado.)
Uso: python experimentos/subida_n8c_memoria_lenta/construye_n8c.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'subida_n8', 'organismo_flujo.py')
SHA_ORIGEN = '14afed5aa16e09bf'
DESTINO = os.path.join(AQUI, 'organismo_repaso.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:50]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def construir():
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN: sha {h16(ORIGEN)}, se esperaba {SHA_ORIGEN}. Abortado.")
    s = open(ORIGEN, encoding='utf-8').read()
    # 1) firma
    s = sust(s, "p_viejo=0.25,fusion=0):", "p_viejo=0.25,fusion=0,repaso=0,dosis=1):", etiqueta='firma')
    # 2) organo de repaso, definido antes del bucle (opera EN SITIO sobre Wp/Wn vivos; lee la huella mup/mun/zp/zn)
    s = sust(s, "    def _key(_k): return frozenset(np.flatnonzero(_k).tolist())",
             "    _rngr=np.random.default_rng([int(seed),8338]) if repaso else None; _rv=[0.0,0.0]; _nrep=[0,0,0]   # n8c: generador APARTE; memoria nueva: ultima R+ y ultima R- (2 numeros); contadores\n"
             "    def _repasa():   # n8c: REPASO de una huella (sin morder, sin energia, sin rng del organismo)\n"
             "        _c=np.flatnonzero(activa&((zp+zn)>1e-9))\n"
             "        if len(_c)==0: return\n"
             "        c=int(_c[int(_rngr.integers(len(_c)))]); _sp=bool(_rngr.random()<zp[c]/(zp[c]+zn[c]))\n"
             "        _m=(mup[c]/zp[c]) if _sp else (mun[c]/zn[c]); _k=int(round(float(_m.sum())))\n"
             "        if _k<1: return\n"
             "        _P=np.zeros(D); _P[np.argsort(_m,kind='stable')[-_k:]]=1.0; _kc=kenyon(_P); _wf=float((Wp-Wn)@_kc)\n"
             "        if repaso==2:\n"
             "            c2=int(_c[int(_rngr.integers(len(_c)))]); _sp=bool(_rngr.random()<zp[c2]/(zp[c2]+zn[c2]))\n"
             "        if repaso==3: _Rh=K*float(Wp[c]-Wn[c])\n"
             "        else: _Rh=_rv[0] if _sp else _rv[1]\n"
             "        if _Rh==0: return\n"
             "        _d=_Rh-_wf; _ix=_kc>0\n"
             "        if lam: _mc=np.minimum(Wp[_ix],Wn[_ix]); Wp[_ix]-=lam*_mc; Wn[_ix]-=lam*_mc\n"
             "        if _d>0: Wp[:]=np.clip(Wp+eta*_d*_kc,0,3.)\n"
             "        else:    Wn[:]=np.clip(Wn+eta*aversion*(-_d)*_kc,0,3.)\n"
             "        _nrep[0]+=1; _nrep[1 if _Rh>0 else 2]+=1\n"
             "    def _key(_k): return frozenset(np.flatnonzero(_k).tolist())",
             etiqueta='organo de repaso')
    # 3) la memoria nueva: la ultima R vivida de cada signo (solo si repaso esta encendido)
    s = sust(s, "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1; morc[kk]+=1",
             "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1; morc[kk]+=1\n"
             "                if repaso: _rv[0 if R>0 else 1]=R   # n8c",
             etiqueta='memoria de R')
    # 4) disparo del repaso: al final del paso en que hubo mordida real (R != 0 solo si mordio)
    s = sust(s, "        E-=costo\n",
             "        if repaso and learn and R!=0:   # n8c: `dosis` repasos tras cada mordida real (repaso despierto tras la recompensa)\n"
             "            for _ in range(dosis): _repasa()\n"
             "        E-=costo\n",
             etiqueta='disparo del repaso')
    # 5) lectura
    s = sust(s, "fus_log=_fus_log,ventana=ventana,", "fus_log=_fus_log,n_rep=_nrep[0],n_rep_pos=_nrep[1],n_rep_neg=_nrep[2],repaso=repaso,dosis=dosis,ventana=ventana,",
             etiqueta='salida')
    cab = ('"""organismo_repaso = experimentos/subida_n8/organismo_flujo.py (14afed5aa16e09bf) + perilla `repaso`\n'
           '(organo de memoria lenta con repaso, nivel 8 pieza 2). Generado por construye_n8c.py. NO editar.\n'
           'Con repaso=0 es organismo_flujo EXACTO (identidad_n8c.py)."""\n')
    return cab + s


if __name__ == '__main__':
    txt = construir()
    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(txt)
    print(f"  {os.path.relpath(DESTINO, RAIZ)}  {h16(DESTINO)}  {txt.count(chr(10))} lineas  (origen {SHA_ORIGEN})")
