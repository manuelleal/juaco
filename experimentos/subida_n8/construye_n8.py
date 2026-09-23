"""Genera experimentos/subida_n8/organismo_flujo.py POR ANCLAS desde
experimentos/nivel10_composicion_v14/organismo_capBD_on.py (sha 506b5c08441fd54e, instrumento de capacidad de v14
con retina de tamano variable; solo se lee).

Dos perillas nuevas, las dos APAGADAS por defecto (con ventana=0 y fusion=0 el archivo es capBD_on EXACTO):
  ventana (mundo): si > 0, el mundo es un FLUJO: cada objeto que nace es, con prob. 1-p_viejo, uno de los `ventana`
      estimulos introducidos mas recientes y, con prob. p_viejo, uno de los anteriores (los viejos siguen apareciendo).
      Con ventana=0 el sorteo de spawn() es el original (mismas llamadas al rng).
  fusion (organo, nivel8_aprendizaje_abierto.md s3 puntos 5-7): cuando una celda cumple la condicion de division por
      conflicto de signo (v11) PERO no queda celda libre, antes de dividir se FUNDEN dos celdas activas que no son del
      codigo actual: fusion=1 las de KW mas parecido (coseno) con valor compatible (no de signo opuesto consolidado);
      fusion=2 (control) dos al azar con un generador APARTE (no toca el rng del mundo ni del organismo).
      Fundir = promediar KW, Wp, Wn, mu, mup, mun, zp, zn en la de menor indice y liberar la otra (queda como una
      celda libre de nacimiento: todo a cero). Memoria nueva: CERO (solo contadores de lectura). Constantes nuevas: CERO.
Uso: python experimentos/subida_n8/construye_n8.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel10_composicion_v14', 'organismo_capBD_on.py')
SHA_ORIGEN = '506b5c08441fd54e'
DESTINO = os.path.join(AQUI, 'organismo_flujo.py')


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
    # 1) firma: perillas nuevas al final, apagadas
    s = sust(s, "ema_c=0.05):", "ema_c=0.05,ventana=0,p_viejo=0.25,fusion=0):", etiqueta='firma')
    # 2) organo de fusion (definido una vez, antes del bucle; opera EN SITIO sobre los arreglos vivos)
    s = sust(s, "    ncod={}; _ord=[]",
             "    ncod={}; _ord=[]\n"
             "    _nfus=[0]; _fus_log=[]; _rngf=np.random.default_rng([int(seed),8008]) if fusion==2 else None   # n8: contadores y generador APARTE del control azar\n"
             "    def _fundir(_excl,_t):   # n8: FUSION -- libera una celda juntando dos activas fuera del codigo actual\n"
             "        _cand=np.array([c2 for c2 in np.flatnonzero(activa) if c2 not in _excl])\n"
             "        if len(_cand)<2: return False\n"
             "        if fusion==2:\n"
             "            _ab=_rngf.choice(len(_cand),2,replace=False); a,b=int(_cand[min(_ab)]),int(_cand[max(_ab)])\n"
             "        else:\n"
             "            _X=KW[_cand]; _nx=np.linalg.norm(_X,axis=1); _nx=np.where(_nx>0,_nx,1.0); _C=(_X@_X.T)/np.outer(_nx,_nx)\n"
             "            _wb=(Wp-Wn)[_cand]; _sg=np.where(np.abs(_wb)>0.2,np.sign(_wb),0.0)\n"
             "            _C=np.where(np.outer(_sg,_sg)<0,-np.inf,_C); np.fill_diagonal(_C,-np.inf)\n"
             "            _i=int(np.argmax(_C)); _ia,_ib=divmod(_i,len(_cand))\n"
             "            if not np.isfinite(_C[_ia,_ib]): return False\n"
             "            a,b=int(_cand[min(_ia,_ib)]),int(_cand[max(_ia,_ib)])\n"
             "        for _A in (KW,mu,mup,mun): _A[a]=0.5*(_A[a]+_A[b]); _A[b]=0.0\n"
             "        for _v in (Wp,Wn,zp,zn): _v[a]=0.5*(_v[a]+_v[b]); _v[b]=0.0\n"
             "        err[a]=0.0; err[b]=0.0; activa[b]=False; _nfus[0]+=1; _fus_log.append((int(_t),a,b))\n"
             "        return True",
             etiqueta='organo de fusion')
    # 3) mundo en flujo: el sorteo de spawn()
    s = sust(s, "            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]",
             "            if x not in objs:\n"
             "                if ventana and len(tipos)>ventana and rng.random()<p_viejo: objs[x]=tipos[int(rng.integers(len(tipos)-ventana))]   # n8: un viejo\n"
             "                elif ventana: _w=tipos[-ventana:]; objs[x]=_w[int(rng.integers(len(_w)))]   # n8: uno de la ventana\n"
             "                else: objs[x]=tipos[int(rng.integers(len(tipos)))]",
             etiqueta='spawn en flujo')
    # 4) disparo de la fusion: misma condicion que la division de v11, pero sin celda libre
    s = sust(s, "                                if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():",
             "                                if fusion and Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and not (~activa).any(): _fundir(set(int(i2) for i2 in idx),t)   # n8\n"
             "                                if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():",
             etiqueta='disparo de la fusion')
    # 5) lectura
    s = sust(s, "hist=hist,t_agot=t_agot", "hist=hist,n_fus=_nfus[0],fus_log=_fus_log,ventana=ventana,fusion=fusion,t_agot=t_agot",
             etiqueta='salida')
    cab = ('"""organismo_flujo = experimentos/nivel10_composicion_v14/organismo_capBD_on.py (506b5c08441fd54e) + perillas\n'
           '`ventana`/`p_viejo` (mundo en flujo) y `fusion` (organo de nivel 8). Generado por construye_n8.py. NO editar.\n'
           'Con ventana=0 y fusion=0 es capBD_on EXACTO; con las perillas de v14.2 y retina de 6 es organismo_v142 en\n'
           'W, muertes, divisiones, celdas, mordidas y visitas (identidad_n8.py)."""\n')
    return cab + s


if __name__ == '__main__':
    txt = construir()
    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(txt)
    print(f"  {os.path.relpath(DESTINO, RAIZ)}  {h16(DESTINO)}  {txt.count(chr(10))} lineas  (origen {SHA_ORIGEN})")
