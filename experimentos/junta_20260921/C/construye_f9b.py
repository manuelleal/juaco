"""Construye experimentos/junta_20260921/C/organismo_f9b.py POR ANCLAS desde
experimentos/nivel09_cuerpo_nuevo/organismo_f9.py (3a821884394d66c9, que aqui SOLO SE LEE).

Cadena completa, verificada por sha antes de escribir nada:
  organismo_f9 3a821884394d66c9 <- organismo_alma2 4fd616aeaf535e61 <- organismo_alma 7c09cec391daa879
  <- organismo_vivo_h1 9e99ff87b5e2db1e <- organismo_vivo_rep2 96feb4918dc5d694 <- organismo_vivo_rep
  aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo/organismo_v14.py
  (v14.1) feefc88b1fd8d434.
Ningun archivo existente se toca (regla 1). Todo lo nuevo vive en experimentos/junta_20260921/C/.

MISION: llegar a la AGI por este camino. FASE 9, BLOQUE 2 (candidato del creador C en la junta del
21-sep-2026): el cuerpo nuevo lee el nodo de su linaje CON LAS DOS VIAS, no solo con la lenta.

LA PERILLA NUEVA, UNA SOLA
  nodo_via=0  el mensaje absorbido entra SOLO por la via LENTA (lineal sobre la retina). Es
              organismo_f9.py BIT A BIT, en todos sus brazos. El contrato del BLOQUE 4 decia
              literalmente "no toca ... ni la via rapida".
  nodo_via=1  el mensaje entra ADEMAS por la VIA RAPIDA, con LA MISMA REGLA LOCAL DE LA MORDIDA
              (codigo de Kenyon del patron del mensaje, error propio de la via con puerta, drenaje
              lam, clip 3.0) y contando como EVIDENCIA DEL CODIGO EXACTO (ncod += 1).
              MEMORIA NUEVA: CERO. Wp/Wn, kenyon(), ncod, lam, eta, aversion ya existian; el mensaje
              ya traia (patron, R, necesidad). Lo unico que cambia es QUE REGLA CONSUME EL MENSAJE.

POR QUE ncod TAMBIEN (declarado ANTES de medir): la puerta de v14 (`puerta_pat=5`, `pat_min=1`)
consulta la via rapida solo si el CODIGO EXACTO tiene >= 5 mordidas registradas. Si la lectura
escribiera Wp/Wn sin contar evidencia, la puerta jamas se abriria y la perilla seria INERTE de
hecho aunque los pesos cambiaran (ERR-38: "inerte" hay que medirlo, no suponerlo). Contar la
lectura como evidencia es la unica lectura coherente de "exposicion que ensena".

LO QUE LA LECTURA NO HACE (declarado, para que el cambio sea UNO):
  - NO divide celdas (div_signo no se dispara al leer): un mensaje nunca parte una casilla.
  - NO toca el predictor de dE (Wpe/Wke/_sbE), ni la energia, ni los objetos, ni la posicion.
  - NO consume el rng del mundo (este constructor lo comprueba con una regex sobre lo insertado).

MEDIDAS NUEVAS, TODAS DE SOLO LECTURA: `via_msg` (mensajes absorbidos por la rapida) y `fam_nac`
(cuantos de los 4 estimulos le son FAMILIARES al recien nacido JUSTO DESPUES de leer, 0..4: es la
prueba directa de que la puerta se abre; si sale 0 la perilla es inerte aunque Wp cambie).

Uso:  python experimentos/junta_20260921/C/construye_f9b.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N09 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')

ORIGEN = os.path.join(N09, 'organismo_f9.py')
DESTINO = os.path.join(AQUI, 'organismo_f9b.py')
CADENA = {
    ORIGEN: '3a821884394d66c9',
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

A_ABSORBE = ("                        if _ds7>0: Wps[_n7]=np.clip(Wps[_n7]+eta_s*_ds7*_Pv,0,clip_s)\n"
             "                        else:      Wns[_n7]=np.clip(Wns[_n7]+eta_s*aversion*(-_ds7)*_Pv,0,clip_s)\n")

A_TRASLECT = "                    _nlec+=1   # F9: lecturas del nodo (solo lectura)\n"

A_SALIDA = ("                       con_cuerpo=[int(_x) for _x in _ncu]))   "
            "# F9: claves nuevas SOLO con alma y f9=1\n")

# ==================== INSERCIONES (ninguna consume el rng DEL MUNDO) ====================
N_FIRMA = ("menu='abcdef',nodo_baraja=0,nodo_rel=0,con_desde=0,rep_acum=0,f9=0,nodo_via=0):")

N_GUARDIA = A_GUARDIA + (
    "    if alma is None: nodo_via=0   # F9B: perilla del NODO, detras de la maestra (inerte: organismo_f9 EXACTO)\n"
    "    if nodo_via not in (0,1): raise SystemExit('F9B: nodo_via es 0 (solo la via lenta, como el bloque 1) o 1 (las DOS vias)')\n"
    "    if nodo_via and not nodo: raise SystemExit('F9B: nodo_via exige nodo=1 (no hay nodo que leer)')\n")

N_INIT = A_INIT + (
    "    _nvia=0; _fam9=[]   # F9B: mensajes absorbidos TAMBIEN por la via rapida, y cuantos de los 4 estimulos le son\n"
    "    #        FAMILIARES al recien nacido JUSTO DESPUES de leer (0..4). Si _fam9 es 0 la puerta no se abre y la\n"
    "    #        perilla es INERTE de hecho aunque Wp cambie (ERR-38). SOLO LECTURA.\n")

N_ABSORBE = A_ABSORBE + (
    "                        if nodo_via:   # F9B: el mensaje entra TAMBIEN por la VIA RAPIDA, con la MISMA regla local de la mordida\n"
    "                            _kc7=kenyon(_Pv); _ky7=_key(_kc7)\n"
    "                            if _ky7 not in ncod: _ord.append(_ky7)\n"
    "                            ncod[_ky7]=ncod.get(_ky7,0)+1   # la lectura cuenta como EVIDENCIA DEL CODIGO EXACTO: sin esto la puerta de v14 nunca consulta la rapida (ERR-38)\n"
    "                            _df7=_R7-float((Wp[_n7]-Wn[_n7])@_kc7)   # con puerta, cada via aprende de SU error (v13)\n"
    "                            _ix7=_kc7>0\n"
    "                            if lam: _mf7=np.minimum(Wp[_n7][_ix7],Wn[_n7][_ix7]); Wp[_n7][_ix7]-=lam*_mf7; Wn[_n7][_ix7]-=lam*_mf7\n"
    "                            if _df7>0: Wp[_n7]=np.clip(Wp[_n7]+eta*_df7*_kc7,0,3.)\n"
    "                            else:      Wn[_n7]=np.clip(Wn[_n7]+eta*aversion*(-_df7)*_kc7,0,3.)\n"
    "                            _nvia+=1   # LEER NO DIVIDE: div_signo no se dispara al leer (un mensaje nunca parte una casilla). Declarado.\n")

N_TRASLECT = A_TRASLECT + (
    "                    if nodo_via: _fam9.append(int(sum(int(_fam(kenyon(PAT[_z9]),_nm)) for _z9 in 'ABCD')))   # F9B: SOLO LECTURA (la puerta, recien leido)\n")

N_SALIDA = (
    "                       con_cuerpo=[int(_x) for _x in _ncu]))   # F9: claves nuevas SOLO con alma y f9=1\n"
    "    if alma is not None and f9 and nodo_via: _ext['f9'].update(nodo_via=1,via_msg=int(_nvia),\n"
    "                       fam_nac=[int(_x) for _x in _fam9[:400]])   # F9B: claves nuevas SOLO con nodo_via=1\n")


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
    txt = sust(txt, A_ABSORBE, N_ABSORBE, etiqueta='absorcion del mensaje')
    txt = sust(txt, A_TRASLECT, N_TRASLECT, etiqueta='tras la lectura')
    txt = sust(txt, A_SALIDA, N_SALIDA, etiqueta='salida')

    # GUARDIA: ninguna linea insertada puede consumir el rng DEL MUNDO
    malo = [l for l in '\n'.join(NUEVO).split('\n') if re.search(r'(?<!_)\brng\.', l)]
    if malo:
        raise SystemExit('INSERCION QUE CONSUME EL RNG DEL MUNDO:\n' + '\n'.join(malo))

    cab = ('"""organismo_f9b.py — GENERADO POR construye_f9b.py DESDE organismo_f9.py (3a821884394d66c9).\n'
           'NO EDITAR A MANO. Perilla nueva: nodo_via (0 = organismo_f9 BIT A BIT; 1 = el mensaje del nodo\n'
           'entra TAMBIEN por la via rapida, con la misma regla local de la mordida y contando evidencia).\n'
           'Memoria nueva: CERO. Junta del 21-sep-2026, creador C, fase 9 bloque 2."""\n')
    open(DESTINO, 'w', encoding='utf-8').write(cab + txt)
    print(f'\n  ESCRITO {os.path.relpath(DESTINO, RAIZ)}  sha {h16(DESTINO)}')
    print(f'  lineas {len(open(ORIGEN, encoding="utf-8").read().splitlines())} -> '
          f'{len(open(DESTINO, encoding="utf-8").read().splitlines())}  · 6 anclas')


if __name__ == '__main__':
    main()
