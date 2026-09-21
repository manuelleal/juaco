"""Construye experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py POR ANCLAS desde
experimentos/nivel09_cuerpo_nuevo/organismo_f9.py (3a821884394d66c9, que aqui SOLO SE LEE),
incorporando las inserciones de experimentos/junta_20260921/C/organismo_f9b.py (6a57e9fa9514099b,
que aqui SOLO SE LEE y sirve de ANCLA DE IDENTIDAD: nodo_via=1 tiene que dar su mismo dict).

Cadena completa, verificada por sha antes de escribir nada:
  organismo_f9b 6a57e9fa9514099b  (bloque 2 del creador C; ancla de identidad de nodo_via=1)
  organismo_f9  3a821884394d66c9 <- organismo_alma2 4fd616aeaf535e61 <- organismo_alma 7c09cec391daa879
  <- organismo_vivo_h1 9e99ff87b5e2db1e <- organismo_vivo_rep2 96feb4918dc5d694 <- organismo_vivo_rep
  aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo/organismo_v14.py
  (v14.1) feefc88b1fd8d434.
Ningun archivo existente se toca (regla 1). Todo lo nuevo vive en experimentos/nivel09_cuerpo_nuevo_b2/.

MISION: llegar a la AGI por este camino — organismo minimo, reglas locales, sin retropropagacion,
peldanos preregistrados con controles y replicas. FASE 9, BLOQUE 2: el cuerpo nuevo que lee el nodo
de su linaje LLENA su via rapida sin abrir la puerta; la puerta la abren sus propias mordidas.

LAS CUATRO PERILLAS NUEVAS (memoria nueva: CERO estructuras)
  nodo_via=0   el mensaje entra SOLO por la via LENTA. Es organismo_f9 BIT A BIT en todos sus brazos.
  nodo_via=1   el mensaje entra ADEMAS por la via RAPIDA y CUENTA COMO EVIDENCIA (ncod += 1).
               Es organismo_f9b BIT A BIT (el fallo YA MEDIDO por C: vida 0.38x, J 0.96 -> 0.74).
  nodo_via=2   EL CANDIDATO. El mensaje entra por la via RAPIDA y NO TOCA ncod: "leer llena la
               memoria; morder abre la puerta". Es nodo_via=1 menos dos lineas.
  nodo_or=1    NODO ORACULO (cota superior, voto del creador A): el contenido que se lee NO es lo que
               vivio el linaje sino la TABLA VERDADERA (patron, necesidad) -> R. Se construye de PAT
               y de _EF, que ya existian; no se guarda nada. Si ni el oraculo cruza R0 0.9, el muro
               es el MUNDO y no la herencia.
  sesgo_fijo=c empujon CONSTANTE en la boca, sin informacion (el mecanismo del brazo CONST de C-P1,
               tal como quedo en organismo_v15_dE5: `if sesgo_fijo: Vb+=sesgo_fijo`). Es el brazo
               CAUTELA de F9-4bis: cautela generica SIN nodo.
  f9c=1        SOLO LECTURA: `pa`/`pn` (encuentros con la puerta de v14 ABIERTA / encuentros). No
               toca el estado ni el rng: el arnes lo prueba (caso K).

POR QUE nodo_via=2 NO TOCA ncod (declarado ANTES de medir): con nodo_via=1 la lectura cuenta como
evidencia del codigo exacto, la puerta de v14 se abre al nacer y la boca ABANDONA el -3 de la via
lenta por el -1 a medio hacer de la rapida (C midio W(B) rapida -2.26 contra W_lenta(B) -2.64, y
W(D) -0.61 contra -2.10): SUSTITUYE, no suma. Con nodo_via=2 la puerta sigue exigiendo puerta_pat=5
mordidas PROPIAS del codigo exacto; mientras el cuerpo rechace el veneno (p1 0.96) nunca las junta y
la via lenta sigue mandando; en lo que SI muerde (la comida), la rapida ya trae los casos del linaje.

LO QUE LA LECTURA NO HACE (declarado, para que el cambio sea UNO):
  - NO divide celdas (div_signo no se dispara al leer): un mensaje nunca parte una casilla.
  - NO toca el predictor de dE (Wpe/Wke/_sbE), ni la energia, ni los objetos, ni la posicion.
  - NO consume el rng del mundo (este constructor lo comprueba con una regex sobre lo insertado).

Uso:  python experimentos/nivel09_cuerpo_nuevo_b2/construye_f9c.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N09 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
JC = os.path.join(RAIZ, 'experimentos', 'junta_20260921', 'C')

ORIGEN = os.path.join(N09, 'organismo_f9.py')
DESTINO = os.path.join(AQUI, 'organismo_f9c.py')
CADENA = {
    ORIGEN: '3a821884394d66c9',
    os.path.join(JC, 'organismo_f9b.py'): '6a57e9fa9514099b',
    os.path.join(N13, 'organismo_alma2.py'): '4fd616aeaf535e61',
    os.path.join(N13, 'organismo_alma.py'): '7c09cec391daa879',
    os.path.join(N11, 'organismo_vivo_h1.py'): '9e99ff87b5e2db1e',
    os.path.join(N11, 'organismo_vivo_rep2.py'): '96feb4918dc5d694',
    os.path.join(N11, 'organismo_vivo_rep.py'): 'aa823d56c2d4213c',
    os.path.join(N11, 'organismo_vivo.py'): '20c0961c79de8825',
    os.path.join(RAIZ, 'organismo', 'organismo_v14.py'): 'feefc88b1fd8d434',
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


NUEVO = []


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:70]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    NUEVO.append(nuevo.replace(viejo, ''))
    return texto.replace(viejo, nuevo)


# ==================== ANCLAS (copiadas LITERALMENTE de organismo_f9.py 3a821884394d66c9) ====================
A_FIRMA = "menu='abcdef',nodo_baraja=0,nodo_rel=0,con_desde=0,rep_acum=0,f9=0):"

A_GUARDIA = ("    if alma is None: nodo_rel=0; con_desde=0; f9=0   # F9: perillas del NODO, "
             "detras de la maestra (inerte: organismo_alma2 EXACTO)\n")

A_INIT = ("    _ldiv=0; _nlec=0   # F9: lecturas del nodo cuyo conjunto DIFIERE del de recencia, "
          "y lecturas totales. Si _ldiv=0 la perilla es INERTE (ERR-38). SOLO LECTURA\n")

A_BOCA_WT = ("            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   "
             "# v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)\n")

A_BOCA_SORP = ("            if k_sorp: Vb+=k_sorp*float(_sbE[_na])   "
               "# VIVO: la SORPRESA DE LA NECESIDAD ACTIVA en la boca (la dosis de v15, ahora especifica)\n")

A_MSG = ("                    elif nodo_rel==2: _msg=[_nodo[_i9] for _i9 in sorted(int(_z9) for _z9 in "
         "_rrel.choice(len(_nodo),size=min(nodo_lee,len(_nodo)),replace=False))]   "
         "# F9: CONTROL DE ACCESO (mismo alcance, orden cronologico, seleccion al azar)\n")

A_ABSORBE = ("                        if _ds7>0: Wps[_n7]=np.clip(Wps[_n7]+eta_s*_ds7*_Pv,0,clip_s)\n"
             "                        else:      Wns[_n7]=np.clip(Wns[_n7]+eta_s*aversion*(-_ds7)*_Pv,0,clip_s)\n")

A_TRASLECT = "                    _nlec+=1   # F9: lecturas del nodo (solo lectura)\n"

A_SALIDA = ("                       con_cuerpo=[int(_x) for _x in _ncu]))   "
            "# F9: claves nuevas SOLO con alma y f9=1\n")

# ==================== INSERCIONES (ninguna consume el rng DEL MUNDO) ====================
N_FIRMA = ("menu='abcdef',nodo_baraja=0,nodo_rel=0,con_desde=0,rep_acum=0,f9=0,"
           "nodo_via=0,nodo_or=0,sesgo_fijo=0.0,f9c=0):")

N_GUARDIA = A_GUARDIA + (
    "    if alma is None: nodo_via=0; nodo_or=0; f9c=0   # F9C: perillas del NODO y sus medidas, detras de la maestra (inerte: organismo_f9 EXACTO)\n"
    "    if not f9: f9c=0   # F9C: las medidas pa/pn viven en el dict f9 (solo lectura, detras de f9)\n"
    "    if nodo_via not in (0,1,2): raise SystemExit('F9C: nodo_via es 0 (solo la via lenta = organismo_f9), 1 (las DOS vias CON evidencia = organismo_f9b) o 2 (las dos vias SIN evidencia: leer llena la memoria, morder abre la puerta)')\n"
    "    if nodo_via and not nodo: raise SystemExit('F9C: nodo_via exige nodo=1 (no hay nodo que leer)')\n"
    "    if nodo_or and not nodo: raise SystemExit('F9C: nodo_or exige nodo=1 (el oraculo sustituye el CONTENIDO del nodo, no el canal)')\n"
    "    if nodo_or and not vivo: raise SystemExit('F9C: nodo_or exige vivo=1 (la tabla verdadera es la del mundo vivo: ABCD x 2 necesidades)')\n")

N_INIT = A_INIT + (
    "    _nvia=0; _fam9=[]   # F9B: mensajes absorbidos TAMBIEN por la via rapida, y cuantos de los 4 estimulos le son\n"
    "    #        FAMILIARES al recien nacido JUSTO DESPUES de leer (0..4). Con nodo_via=2 tiene que salir 0: leer NO abre la puerta. SOLO LECTURA.\n"
    "    _gpa=0; _gpn=0   # F9C: encuentros con la PUERTA DE v14 ABIERTA y encuentros totales (f9c=1). Es el testigo de 'morder abre la puerta'. SOLO LECTURA.\n")

N_BOCA_WT = (
    "            _fa9=bool(puerta is not None and _fam(kc))   # F9C: la PUERTA de v14 en ESTE encuentro. Mismo valor que la linea original (cortocircuito identico): SOLO LECTURA de mas\n"
    "            _wt=_wf+_ws if puerta is None else (_wf if _fa9 else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)\n"
    "            if f9c: _gpn+=1; _gpa+=int(_fa9)   # F9C: SOLO LECTURA ('morder abre la puerta': con nodo_via=2 la puerta la abren las mordidas PROPIAS, no la lectura)\n")

N_BOCA_SORP = A_BOCA_SORP + (
    "            if sesgo_fijo: Vb+=sesgo_fijo   # F9C: CAUTELA -- empujon CONSTANTE en la boca, SIN informacion (el brazo CONST de C-P1). No toca el rng\n")

N_MSG = A_MSG + (
    "                    if nodo_or:   # F9C: NODO ORACULO (cota superior, voto del creador A). El contenido NO es lo que vivio el linaje: es la TABLA VERDADERA\n"
    "                        #        (patron, necesidad) -> R del mundo, construida de PAT y _EF, que YA existian. MEMORIA NUEVA: CERO (se arma y se tira).\n"
    "                        _or9=[[[float(_z9) for _z9 in PAT[_k9]],float(1.0 if _EF[val[_k9]][_n9]>0 else (-3.0 if _EF[val[_k9]][_n9]<0 else 0.0)),int(_n9)] for _n9 in range(min(n_nec,2)) for _k9 in 'ABCD']\n"
    "                        _msg=_or9*max(1,nodo_lee)   # 8*nodo_lee = 400 mensajes con nodo_lee=50: CINCUENTA copias EXACTAS de la tabla, de las que el recien\n"
    "                        #        nacido lee nodo_lee=50 por LA MISMA regla de relevancia que los demas brazos. Mismo canal, MISMO presupuesto, mejor CONTENIDO.\n"
    "                        #        (Si el pool fuera del tamano del presupuesto no habria seleccion y la mitad de la lectura se gastaria en los mensajes R=0 de\n"
    "                        #        la tabla -- A con sed, B con sed --: eso no seria una cota superior sino un brazo con handicap. Hallado en el humo y declarado.)\n")

N_ABSORBE = A_ABSORBE + (
    "                        if nodo_via:   # F9B/F9C: el mensaje entra TAMBIEN por la VIA RAPIDA, con la MISMA regla local de la mordida\n"
    "                            _kc7=kenyon(_Pv); _ky7=_key(_kc7)\n"
    "                            if nodo_via==1:   # nodo_via=1 (organismo_f9b): la lectura CUENTA como evidencia del codigo exacto -> la puerta de v14 se abre al NACER\n"
    "                                if _ky7 not in ncod: _ord.append(_ky7)\n"
    "                                ncod[_ky7]=ncod.get(_ky7,0)+1\n"
    "                            _df7=_R7-float((Wp[_n7]-Wn[_n7])@_kc7)   # con puerta, cada via aprende de SU error (v13)\n"
    "                            _ix7=_kc7>0\n"
    "                            if lam: _mf7=np.minimum(Wp[_n7][_ix7],Wn[_n7][_ix7]); Wp[_n7][_ix7]-=lam*_mf7; Wn[_n7][_ix7]-=lam*_mf7\n"
    "                            if _df7>0: Wp[_n7]=np.clip(Wp[_n7]+eta*_df7*_kc7,0,3.)\n"
    "                            else:      Wn[_n7]=np.clip(Wn[_n7]+eta*aversion*(-_df7)*_kc7,0,3.)\n"
    "                            _nvia+=1   # LEER NO DIVIDE: div_signo no se dispara al leer (un mensaje nunca parte una casilla). Declarado.\n")

N_TRASLECT = A_TRASLECT + (
    "                    if nodo_via: _fam9.append(int(sum(int(_fam(kenyon(PAT[_z9]),_nm)) for _z9 in 'ABCD')))   # F9B/F9C: SOLO LECTURA (la puerta, recien leido)\n")

N_SALIDA = (
    "                       con_cuerpo=[int(_x) for _x in _ncu]))   # F9: claves nuevas SOLO con alma y f9=1\n"
    "    if alma is not None and f9 and nodo_via: _ext['f9'].update(nodo_via=int(nodo_via),via_msg=int(_nvia),\n"
    "                       fam_nac=[int(_x) for _x in _fam9[:400]])   # F9B: claves nuevas SOLO con nodo_via!=0 (con nodo_via=1 son las de organismo_f9b, valor a valor)\n"
    "    if alma is not None and f9 and f9c: _ext['f9'].update(pa=int(_gpa),pn=int(_gpn))   # F9C: claves nuevas SOLO con f9c=1 (SOLO LECTURA)\n"
    "    if alma is not None and f9 and nodo_or: _ext['f9'].update(nodo_or=1)   # F9C: eco de configuracion SOLO con nodo_or=1\n"
    "    if sesgo_fijo: _ext.update(sesgo_fijo=float(sesgo_fijo))   # F9C: eco de configuracion SOLO con el empujon encendido\n")


def main():
    for p, s in CADENA.items():
        if not os.path.exists(p):
            raise SystemExit(f'FALTA {p}')
        v = h16(p)
        if v != s:
            raise SystemExit(f'SHA distinto en {os.path.basename(p)}: {v} != {s}. Abortado (tripwire).')
        print(f'  ancla OK  {v}  {os.path.relpath(p, RAIZ)}')

    txt = open(ORIGEN, encoding='utf-8').read()
    txt = sust(txt, A_FIRMA, N_FIRMA, etiqueta='firma')
    txt = sust(txt, A_GUARDIA, N_GUARDIA, etiqueta='guardias')
    txt = sust(txt, A_INIT, N_INIT, etiqueta='init')
    txt = sust(txt, A_BOCA_WT, N_BOCA_WT, etiqueta='boca: la puerta (identica, con testigo)')
    txt = sust(txt, A_BOCA_SORP, N_BOCA_SORP, etiqueta='boca: empujon constante (CAUTELA)')
    txt = sust(txt, A_MSG, N_MSG, etiqueta='contenido del nodo (ORACULO)')
    txt = sust(txt, A_ABSORBE, N_ABSORBE, etiqueta='absorcion del mensaje (las dos vias)')
    txt = sust(txt, A_TRASLECT, N_TRASLECT, etiqueta='tras la lectura (fam_nac)')
    txt = sust(txt, A_SALIDA, N_SALIDA, etiqueta='salida')

    # GUARDIA 1: ninguna linea insertada puede consumir el rng DEL MUNDO
    malo = [l for l in '\n'.join(NUEVO).split('\n') if re.search(r'(?<!_)\brng\.', l)]
    if malo:
        raise SystemExit('INSERCION QUE CONSUME EL RNG DEL MUNDO:\n' + '\n'.join(malo))
    # GUARDIA 2: ninguna linea insertada puede disparar una division ni tocar el predictor de dE
    malo2 = [l for l in '\n'.join(NUEVO).split('\n') if re.search(r'\b(splits|Wpe|Wke|_sbE)\b', l)]
    if malo2:
        raise SystemExit('INSERCION QUE TOCA DIVISION O PREDICTOR:\n' + '\n'.join(malo2))

    cab = ('"""organismo_f9c.py — GENERADO POR construye_f9c.py DESDE organismo_f9.py (3a821884394d66c9),\n'
           'incorporando las inserciones de organismo_f9b.py (6a57e9fa9514099b). NO EDITAR A MANO.\n'
           '  nodo_via=0 -> organismo_f9 BIT A BIT   ·   nodo_via=1 -> organismo_f9b BIT A BIT\n'
           '  nodo_via=2 -> EL CANDIDATO: leer llena la via rapida y NO abre la puerta (ncod intacto)\n'
           '  nodo_or=1  -> NODO ORACULO (tabla verdadera; cota superior de la herencia)\n'
           '  sesgo_fijo -> CAUTELA: empujon constante en la boca, sin informacion\n'
           '  f9c=1      -> pa/pn: encuentros con la puerta de v14 abierta (SOLO LECTURA)\n'
           'Memoria nueva: CERO. Fase 9 bloque 2, 21-sep-2026."""\n')
    open(DESTINO, 'w', encoding='utf-8').write(cab + txt)
    print(f'\n  ESCRITO {os.path.relpath(DESTINO, RAIZ)}  sha {h16(DESTINO)}')
    print(f'  lineas {len(open(ORIGEN, encoding="utf-8").read().splitlines())} -> '
          f'{len(open(DESTINO, encoding="utf-8").read().splitlines())}  · 9 anclas')


if __name__ == '__main__':
    main()
