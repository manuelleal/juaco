"""Construye experimentos/nivel12_mundo_familias/organismo_familias_b3.py POR ANCLAS, con DOS CADENAS:

  CADENA 1 (EXTRACCION) — de experimentos/creacion_A/organismo_v15f.py (96fc5c5262107850, candidato del creador A;
            aqui SOLO SE LEE): se EXTRAEN LITERALMENTE los tres bloques de la memoria de pares con relevo (la
            inicializacion + las tres funciones de lectura, el bloque de escritura de la tabla, y el prefijo del
            diccionario de salida). NO se reescriben a mano (ERR-38: dos caminos al mismo numero, nunca una copia).
  CADENA 2 (APLICACION) — sobre experimentos/nivel12_mundo_familias/organismo_familias_b2.py (bloque 2; que a su vez
            es organismo_familias.py -> organismo/organismo_v14.py, TRONCO v14.1). Aqui tambien SOLO SE LEE.

Si CUALQUIERA de las dos cadenas no encaja (sha distinto, ancla ausente o repetida), el constructor ABORTA y no
escribe nada.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin backprop en
el runtime, que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada.

LA UNICA GENERALIZACION QUE SE HACE AL TEXTO DE v15f, y se declara: v15f fija la retina en 6 pixeles
(`_PARv` sobre `range(6)`, 15 celdas). El mundo de familias tiene `_D = 12`, asi que `6` pasa a `_D` (la variable que
el bloque 1 ya introdujo) y `15` pasa a `_NP = len(_PARv) = C(_D,2)`. **Con `_D = 6` esto es literalmente 15 y el
modulo es organismo_v15f bit a bit** (arnes, caso `v15f-ON`). Nada mas del mecanismo cambia: R crudo, sobrescritura,
error propio por celda, ganadora por menor error, desempate al azar con el rng del organismo, y relevo a la lineal
cuando la celda ganadora no conoce la combinacion.

ANCLA DE IDENTIDAD (regla 2 de EQUIPO.md), lo que comprueba identidad_familias_b3.py:
  (a) con `memoria_pares=None` -> organismo_familias_b2 BIT A BIT (todas sus claves) y el rng NO se consume (T=120000);
  (b) con `memoria_pares='relevo'` y `mundo='AB'` -> organismo_v15f_on (54d6efe0b564113c) BIT A BIT;
  (c) con `memoria_pares=None` y `mundo='AB'` -> organismo_v14 (TRONCO) BIT A BIT, por la cadena;
  (d) controles que DEBEN fallar.

Uso:  python experimentos/nivel12_mundo_familias/construye_familias_b3.py     (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

SHA_B2 = '30200bea6a41c3c8'          # organismo_familias_b2.py (bloque 2, identidad 63/63)
SHA_V15F = '96fc5c5262107850'        # experimentos/creacion_A/organismo_v15f.py (candidato del creador A)
SHA_V15F_ON = '54d6efe0b564113c'     # experimentos/creacion_A/organismo_v15f_on.py (la misma con la perilla ON)
SHA_MF = 'b9dd561a0cf056b8'          # organismo_familias.py (bloque 1)
SHA_V14 = 'feefc88b1fd8d434'         # organismo/organismo_v14.py (TRONCO CONGELADO)
SHA_ESCALA = 'd8b8566bca77a0ae'      # escala_codigo.py (bloque 0)
DESTINO = os.path.join(AQUI, 'organismo_familias_b3.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado (no se escribe nada).")
    return open(p, encoding='utf-8').read()


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:70]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def trozo(texto, ini, fin, etiqueta):
    """CADENA 1: extrae el bloque LITERAL que empieza en `ini` y termina en `fin` (inclusive). Las dos anclas
    tienen que aparecer EXACTAMENTE una vez y en ese orden, o aborta."""
    for a, nom in ((ini, 'inicio'), (fin, 'fin')):
        if texto.count(a) != 1:
            raise SystemExit(f"CADENA 1, {etiqueta} ({nom}): el ancla aparece {texto.count(a)} veces. Abortado.")
    i = texto.index(ini); j = texto.index(fin)
    if j < i:
        raise SystemExit(f"CADENA 1, {etiqueta}: el ancla de fin va ANTES que la de inicio. Abortado.")
    return texto[i:j + len(fin)]


# ============ CADENA 1: anclas de EXTRACCION en experimentos/creacion_A/organismo_v15f.py ============
V_FIRMA = ",memoria_pares=None,mem_alfa=1.0,mem_rho=0.02):"
V_INI_A = "    if memoria_pares not in (None,'relevo'): raise ValueError"
V_INI_B = "        return _tv if _vv else _lin_v15f(P)\n"
V_TAB_A = "                        if memoria_pares is not None:   # v15f: las 15 celdas escriben R CRUDO"
V_TAB_B = "   # desempate al azar con el rng del organismo; solo consume rng si HAY empate\n"
V_RET_A = "memoria_pares=memoria_pares,mem_alfa=mem_alfa,"
V_RET_B = "mem_ev={k:int(_ev(kenyon(PAT[k]))) for k in PAT},"
V_VALOR = "        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=_lenta_v15f(P)\n"
V_WS = "_ws=_lenta_v15f(PAT[kk])   # v13: las dos vias (v15f: tabla si conoce la combinacion, si no la lineal)\n"
V_DS = ("                        _lbv=_lin_v15f(PAT[kk]); _ds=dlt if puerta is None else R-_lbv   "
        "# v15f: la lineal aprende de SU error (apagada: _lbv == _ws)\n")

# ============ CADENA 2: anclas de APLICACION en organismo_familias_b2.py ============
B_FIRMA = ",crit_exp=0.5,vira=0,exc_evita=-1,reg_b2=0):"
B_LENTA = "    Wps=np.zeros(_D); Wns=np.zeros(_D)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)\n"
B_VALOR = "        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)\n"
B_WS = ("            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=float((Wps-Wns)@PAT[kk])   "
        "# v13: las dos vias\n")
B_DS = "                        _ds=dlt if puerta is None else R-_ws\n"
B_CLIP = "                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)\n"
B_RET = "    return dict(desambiguar=desambiguar,"

CABECERA = '''"""organismo_familias_b3 = organismo_familias_b2.py (bloque 2; -> organismo_familias.py -> organismo/organismo_v14.py,
TRONCO v14.1 feefc88b1fd8d434) + LA MEMORIA DE PARES CON RELEVO de experimentos/creacion_A/organismo_v15f.py
(96fc5c5262107850), extraida por anclas de ese archivo y generalizada de 6 pixeles a `_D` (C(_D,2) celdas).
Perillas: `memoria_pares` = None | 'relevo', `mem_alfa` = 1.0, `mem_rho` = 0.02 (las de v15f, sin tocar).
ANCLA DE IDENTIDAD: con memoria_pares=None es organismo_familias_b2 BIT A BIT (y por la cadena, con mundo='AB',
organismo_v14 bit a bit); con memoria_pares='relevo' y mundo='AB' es organismo_v15f_on BIT A BIT (_D = 6 -> 15 celdas).
Arnes: identidad_familias_b3.py.  Generado por construye_familias_b3.py. NO editar a mano."""
'''


def main():
    for p, sha in [(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                   (os.path.join(AQUI, 'organismo_familias.py'), SHA_MF),
                   (os.path.join(AQUI, 'escala_codigo.py'), SHA_ESCALA),
                   (os.path.join(CREA, 'organismo_v15f_on.py'), SHA_V15F_ON)]:
        if h16(p) != sha:
            raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado.")

    # ---------------- CADENA 1: extraer de v15f, y generalizar 6 -> _D y 15 -> _NP
    v = origen(os.path.join(CREA, 'organismo_v15f.py'), SHA_V15F)
    if v.count(V_FIRMA) != 1:
        raise SystemExit(f"CADENA 1, firma: aparece {v.count(V_FIRMA)} veces. Abortado.")
    for a, nom in ((V_VALOR, 'valor'), (V_WS, 'lectura en la mordida'), (V_DS, 'error propio de la lineal')):
        if v.count(a) != 1:
            raise SystemExit(f"CADENA 1, {nom}: el ancla aparece {v.count(a)} veces. Abortado.")
    INIT = trozo(v, V_INI_A, V_INI_B, 'inicializacion + lecturas')
    TABLA = trozo(v, V_TAB_A, V_TAB_B, 'escritura de la tabla')
    RET = trozo(v, V_RET_A, V_RET_B, 'prefijo del diccionario de salida')

    INIT = sust(INIT, "    _PARv=[(i,j) for i in range(6) for j in range(i+1,6)]   # v15f: las 15 celdas = pares de pixeles",
                "    _PARv=[(i,j) for i in range(_D) for j in range(i+1,_D)]; _NP=len(_PARv)   "
                "# v15f/b3: C(_D,2) celdas = pares de pixeles (con _D=6 son 15: v15f EXACTO)",
                etiqueta='b3: _PARv sobre _D')
    INIT = sust(INIT, "_MMv=np.zeros((15,4)); _MNv=np.zeros((15,4)); _MEv=np.full(15,1e9); _MGv=0",
                "_MMv=np.zeros((_NP,4)); _MNv=np.zeros((_NP,4)); _MEv=np.full(_NP,1e9); _MGv=0",
                etiqueta='b3: tablas sobre _NP')
    TABLA = sust(TABLA, "# v15f: las 15 celdas escriben R CRUDO", "# v15f/b3: las _NP celdas escriben R CRUDO",
                 etiqueta='b3: comentario de la tabla')
    TABLA = sust(TABLA, "                            for _cv in range(15):", "                            for _cv in range(_NP):",
                 etiqueta='b3: bucle sobre _NP')
    if '(15' in INIT or 'range(15)' in TABLA or 'range(6)' in INIT:
        raise SystemExit("CADENA 1: queda un 6 o un 15 fijo tras generalizar. Abortado.")

    # ---------------- CADENA 2: aplicar sobre el instrumento del bloque 2
    t = origen(os.path.join(AQUI, 'organismo_familias_b2.py'), SHA_B2)
    t = CABECERA + t
    t = sust(t, B_FIRMA, B_FIRMA[:-2] + V_FIRMA, etiqueta='firma de run')
    t = sust(t, B_LENTA, B_LENTA + INIT, etiqueta='inicializacion de la memoria de pares')
    t = sust(t, B_VALOR, V_VALOR, etiqueta='valor() lee por relevo')
    t = sust(t, B_WS, B_WS.replace("_ws=float((Wps-Wns)@PAT[kk])   # v13: las dos vias\n", V_WS),
             etiqueta='la mordida lee por relevo')
    t = sust(t, B_DS, V_DS, etiqueta='la lineal aprende de su propio error')
    t = sust(t, B_CLIP, B_CLIP + TABLA, etiqueta='escritura de la tabla')
    t = sust(t, B_RET, "    return dict(" + RET + "desambiguar=desambiguar,", etiqueta='diccionario de salida')

    compile(t, DESTINO, 'exec')          # que ni se escriba algo que no compila
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print("  CADENA 1 (extraccion de v15f)  OK: 3 bloques + 4 anclas de linea")
    print("  CADENA 2 (aplicacion sobre b2) OK: 7 anclas")
    print(f"  escrito {os.path.relpath(DESTINO, RAIZ)}")
    print(f"  sha origen  organismo_familias_b2.py {SHA_B2}")
    print(f"  sha origen  organismo_v15f.py        {SHA_V15F}")
    print(f"  sha destino organismo_familias_b3.py {h16(DESTINO)}")
    print("  ahora: python experimentos/nivel12_mundo_familias/identidad_familias_b3.py")


if __name__ == '__main__':
    main()
