"""JUNTA FASE 5 -- CANDIDATO **BA** (lo que nadie probo junto: la lectura CONJUNTIVA de B sobre las DOS
GANADORAS DE DISTINTO TIPO de A).
Construye experimentos/junta_fase5/BA/organismo_familias_ba.py POR ANCLAS, sobre
experimentos/junta_fase5/A/organismo_familias_a1.py (8833e1dcfb62f26d; aqui SOLO SE LEE).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
retropropagacion, que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy, fase 5:
que el mensaje refiera a la FAMILIA **Y** a la VARIANTE con la MISMA tabla (BAR-T <= 5/20 Y PAR >= 15/20).

DE DONDE VIENE (numeros de las series 821-840 / 841-860 de la junta, no intuiciones):
  celda                                        CORTADO   BAR-H   BAR-T   dist(PAR)   CANAL
  b5k3   (k=3 FORMA, denso, DISYUNCION)          0 / 0   13/13    3 / 2     7 / 6     18/17
  k3v0j1 (k=3 FORMA, denso, CONJUNCION de B)     2 / 1   13/12    2 / 2    10 / 7     17/16
  b6suf  (sufijo, DISYUNCION)                    1 / 3   10/ 4   12 / 8    15/15      17/16
  k3v1j1 (sufijo + CONJUNCION de B)              4 / 2    9 / 7    7 / 5    14/14      17/15
  A1     (dos tipos + min + `exige_dir`)         4 / 4   10 / 7    9 / 5    13/13      18/17

  LO QUE DICE ESA TABLA, leido antes de escribir una linea de codigo:
  1. El MEJOR BAR-T de toda la junta (2/20 y 2/20) y una base baja (CORTADO 2 y 1) los da la CONJUNCION DE B
     aplicada a las k ganadoras de FORMA **sin sufijo** (`k3v0j1`): densidad intacta, referencia de familia
     exacta. Lo unico que le falta es la variante (dist 10 y 7).
  2. La separacion de la HERMANA la dan el sufijo (b6suf, dist 15/15) o las ganadoras MIXTAS de A
     (A1, dist 13/13) -- pero las dos la pagan en la base: CORTADO sube de 0-1 a 4.
  3. En A1 la base sube por `exige_dir`: exigir que las SEIS ganadoras (3 de forma + 3 mixtas) conozcan su
     casilla hace que la tabla calle mucho mas, y cuando la tabla calla decide la LINEAL, que con hambre = 1
     lee ~-1.0 y NO frena la mordida (hace falta <= -2.1). Por eso en A1 suben a la vez CORTADO (4), VALOR
     (7 y 6) y BAR-T (9 y 5): son la MISMA fuga, y ninguna de las tres la causa el mensaje.

LA IDEA (una sola, y es de COMBINADOR, no de tabla): **la conjuncion de B se aplica POR TIPO, y el tipo de
FORMA es el que decide si la tabla habla.**
  - FORMA (las `k_forma` ganadoras de dos px de forma): si NO las conoce TODAS, la tabla calla y releva a la
    lineal. Esa es exactamente la regla `mem_conj` de B -- la referencia es la INTERSECCION de las direcciones,
    no la union -- restringida al tipo que fija la familia. Es lo que midio 2/20 y 2/20 en BAR-T.
  - VARIANTE (la mejor mixta de CADA pixel de variante, la cobertura de A): si NO las conoce todas, **no puede
    vetar, pero tampoco hace callar a la tabla**: contesta la FORMA sola. Una casilla de variante que no
    consta no es evidencia contra el mensaje, y convertirla en abstencion es lo que le costo a A1 la base.
  - Si los dos tipos constan enteros: `min(S_forma, S_variante)` -- la conjuncion de valor de A ("para morder
    tienen que estar de acuerdo los dos tipos; para no morder basta uno"), que es la que tumba a la hermana.

  En una frase: **la FORMA decide si la tabla habla (conjuncion de B); la VARIANTE decide si lo que dice es
  del referente o de su hermana (dos tipos de A); una variante que no consta no manda a callar a nadie.**

UNA PERILLA NUEVA, INERTE por defecto, CERO MEMORIA NUEVA (ni un array, ni un contador, ni un bit de
procedencia: las mismas 66 celdas, las mismas 4 casillas, el mismo `_MEv`, la misma escritura):
  `conj_tipo` (0): con 1, `_tabla_dos` usa la regla de arriba. Con 0, `organismo_familias_a1` BIT A BIT (y por
                   su cadena, con dos_tipos=0: b6, b5, b4b, b4, b3, b2, organismo_familias, organismo_v14
                   (TRONCO) y organismo_v15f_on).
  `conj_tipo=1` EXIGE `dos_tipos=1` y PROHIBE `exige_dir=1` (son dos reglas de abstencion distintas y no se
  componen: si se piden las dos, LANZA en vez de elegir una en silencio).

DIAGNOSTICO NUEVO (no decide ninguna prediccion, no toca el rng, no toca el estado):
  `canal_lee_ref` = que lee la tabla PARA EL REFERENTE en el paso exacto de la entrega:
                    [valor, habla, exactas de FORMA, exactas de VARIANTE]. Es el diagnostico que a B le dijo
                    cual de sus tres ideas era la buena; sin el, todas las celdas parecen iguales con n = 3.

QUE NO SE TOCA (ni una linea): el emisor, el canal, el mundo, la ESCRITURA (las 66 celdas siguen escribiendo R
  CRUDO por sobrescritura en SU direccion), `_dir_var`, la ganadora `_MGv` y su desempate al azar, el error
  propio `_MEv`, `_topk_tipo`, `_suma_tipo`, la via rapida, la puerta, la boca, el metabolismo y EL CONSUMO
  DEL RNG. Solo cambia COMO SE COMBINAN las dos filas que A ya leia.

ANCLA DE IDENTIDAD (regla 2 de EQUIPO.md), lo que comprueba identidad_familias_ba.py:
  (a) con conj_tipo=0 -> organismo_familias_a1 BIT A BIT (con dos_tipos 0 y 1, con y sin sufijo, k 1 y 3, en
      los tres modos del canal) y, con dos_tipos=0, organismo_familias_b6 BIT A BIT; por la cadena de b6:
      b5, b4b, organismo_v14 (TRONCO) y organismo_v15f_on;
  (b) con memoria_pares=None la perilla es INERTE;
  (c) perillas mal escritas que LANZAN (incluida la combinacion prohibida conj_tipo=1 + exige_dir=1);
  (d) controles que DEBEN diferir (ERR-64b, >= 2 de 3 semillas): conj_tipo=1 cambia la corrida frente a A1 y
      frente a A1-d, y el mensaje de la hermana / de otro token no da la misma corrida que el del referente.

Uso:  python experimentos/junta_fase5/BA/construye_familias_ba.py     (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
JA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'A')
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')

SHA_A1 = '8833e1dcfb62f26d'             # organismo_familias_a1.py (creador A, identidad 77/77)
SHA_A1_CONSTR = 'fe023157ea34b62c'      # construye_familias_a1.py
SHA_B6 = 'b10cbd4ddd0c32a3'             # organismo_familias_b6.py (bloque 6, identidad 59/59)
SHA_B5 = 'e0b6b90f6f92d5c1'
SHA_B4B = 'b3dd1d7e66a2d147'
SHA_V14 = 'feefc88b1fd8d434'            # EL TRONCO
SHA_V15F_ON = '54d6efe0b564113c'
SHA_ESCALA = 'd8b8566bca77a0ae'
SHA_JB = '312a68054dbae7f6'             # organismo_familias_jb.py (creador B) -- solo se verifica, no se usa
DESTINO = os.path.join(AQUI, 'organismo_familias_ba.py')


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


# ---------------------------------------------------------------- anclas en organismo_familias_a1.py
A_FIRMA = ",combina='media',msg_elige=1,exige_dir=0,dentro='suma'):"
A_GUARDA = ('    if _DTv and not (1<=_NVA<_D and _FRM and _VMX): raise ValueError(f"dos_tipos=1 con _D={_D} y '
            'fam_nvar={fam_nvar!r}: los dos tipos tienen que existir (forma {len(_FRM)}, mixtas {len(_VMX)})")'
            '   # A1\n')
A_EDV = ("        if _EDv and (_nf7<len(_f7) or _nv7<len(_v7)): return (0.0, False)   # A1 `exige_dir`: si alguna "
         "ganadora NO conoce su casilla para este patron, la tabla NO habla (releva a la lineal). Sin esta regla, "
         "la casilla que no se conoce desaparece de la suma y el mensaje de la hermana se cuela por el tipo que "
         "no puede saber.\n")
A_INIT = "_c4dt=None; _c4gt=None   # A1:"
A_DT = ("            _c4dt=(sorted(_n8 for _n8 in PAT if all(_dir_var(_g8,PAT[_n8])==_dir_var(_g8,_P4) for _g8 in "
        "(_topk_tipo()[0]+_topk_tipo()[1]))) if _DTv else None)   # A1: DIAGNOSTICO -- cuantos de los 32 estimulos "
        "comparten TODAS las direcciones de LOS DOS TIPOS con el mensaje (la resolucion observada, no prometida)\n")
A_RET = "    return dict(dos_tipos=int(dos_tipos),"

NUEVO_CHK = (
    '    if (not isinstance(conj_tipo,int)) or isinstance(conj_tipo,bool) or conj_tipo not in (0,1,2): raise ValueError(f"conj_tipo={conj_tipo!r}: se espera 0 (apagado), 1 (candidato BA) o 2 (ablacion: la variante vota con lo que sabe)")   # BA: perilla mal escrita no cae en silencio\n'
    '    _CTv=int(conj_tipo)   # BA: CONJUNCION POR TIPO -- la de B (`mem_conj`: la referencia es la INTERSECCION de las direcciones, no la union) aplicada a CADA UNO de los dos tipos de ganadora de A, con la FORMA como la que decide si la tabla habla\n'
    '    if _CTv and not _DTv: raise ValueError("conj_tipo=1 exige dos_tipos=1: la conjuncion POR TIPO no tiene tipos que conjugar sin las dos ganadoras")   # BA\n'
    '    if _CTv and _EDv: raise ValueError("conj_tipo=1 y exige_dir=1 son DOS reglas de abstencion distintas y no se componen (exige_dir hace callar a la tabla cuando la VARIANTE no consta; conj_tipo no). Se pide una.")   # BA\n')

NUEVO_LEE = (
    "        if _CTv:   # BA: LA CONJUNCION DE B, POR TIPO. (1) FORMA: si no constan TODAS sus direcciones, la tabla CALLA y releva a la lineal -- es `mem_conj` de B sobre el tipo que fija la familia (medido 2/20 y 2/20 en BAR-T con CORTADO 2 y 1). (2) VARIANTE incompleta: con conj_tipo=1 (CANDIDATO) el tipo se abstiene del voto y manda la FORMA -- un tipo incompleto no opina, que es la conjuncion de B llevada al tipo; con conj_tipo=2 (ABLACION declarada) vota con lo que sabe (la disyuncion de b5 dentro del tipo). (3) Con los dos tipos enteros, la conjuncion de VALOR de A.\n"
    "            if _nf7<len(_f7): return (0.0, False)\n"
    "            if _nv7<len(_v7) and (_CTv==1 or not _nv7): return (_sf7, True)\n"
    "            return (min(_sf7,_sv7), True) if _CMv else ((_wF*_sf7+_wV*_sv7)/(_wF+_wV), True)\n")

NUEVO_DIAG = (
    "            _c4lp=([round(float(_tabla_dos(PAT[_c4r])[0]),4),bool(_tabla_dos(PAT[_c4r])[1]),int(_suma_tipo(_topk_tipo()[0],PAT[_c4r])[1]),int(_suma_tipo(_topk_tipo()[1],PAT[_c4r])[1])] if (_DTv and _c4r in PAT) else None)   # BA: DIAGNOSTICO -- que lee la tabla PARA EL REFERENTE en el paso exacto de la entrega: [valor, habla, exactas de FORMA, exactas de VARIANTE]. No toca estado ni rng y no decide ninguna prediccion.\n")

CABECERA = '''"""organismo_familias_ba = organismo_familias_a1.py (creador A de la junta de la fase 5, `dos_tipos`,
8833e1dcfb62f26d) + LA CONJUNCION POR TIPO del candidato BA, inerte por defecto:
  `conj_tipo` (0): con 1, la lectura de los dos tipos de ganadora pasa a ser la CONJUNCION de B (`mem_conj`:
               la tabla contesta solo si constan TODAS las direcciones; la referencia es la INTERSECCION y no
               la union) aplicada POR TIPO, con la FORMA como la que decide si la tabla habla:
                 - si alguna ganadora de FORMA no conoce su casilla -> la tabla CALLA y releva a la lineal
                   (la regla de B, sobre el tipo que fija la familia);
                 - si alguna ganadora de VARIANTE no la conoce -> el TIPO NO OPINA y NO hace callar a la
                   tabla: contesta la FORMA sola (un tipo incompleto no vota, que es la conjuncion de B
                   llevada al tipo). Con `conj_tipo`=2 (ABLACION declarada) el tipo vota con lo que sabe;
                 - si constan los dos tipos enteros -> `combina` ('min' = la conjuncion de valor de A: para
                   morder tienen que estar de acuerdo los dos tipos, para no morder basta uno).
               CERO MEMORIA NUEVA: ni un array, ni un contador, ni un bit de procedencia. Solo el combinador.
               `conj_tipo=1` EXIGE `dos_tipos=1` y PROHIBE `exige_dir=1` (LANZA si se piden las dos).
  `canal_lee_ref`: DIAGNOSTICO nuevo (no decide nada) -- que lee la tabla PARA EL REFERENTE en el paso exacto
               de la entrega: [valor, habla, exactas de FORMA, exactas de VARIANTE].
  `mem_visto`  : DIAGNOSTICO nuevo (no decide nada) -- la matriz `_MNv > 0` (que casillas constan), derivada de
               un array que ya existia. Permite REIMPLEMENTAR FUERA las tres reglas de lectura y compararlas
               SOBRE LA MISMA TABLA (la leccion de B: dos trayectorias distintas no comparan reglas).
NO cambian el emisor, el canal, el mundo, la ESCRITURA, `_dir_var`, `_topk_tipo`, `_suma_tipo`, `_MGv` ni su
desempate, `_MEv`, la via rapida, la puerta, la boca ni el consumo del azar del organismo.
ANCLA DE IDENTIDAD: con conj_tipo=0 es organismo_familias_a1 BIT A BIT y, con dos_tipos=0 ademas,
organismo_familias_b6 BIT A BIT y por su cadena b5, b4b, b4, b3, b2, organismo_familias, organismo_v14
(TRONCO) y organismo_v15f_on.
Arnes: identidad_familias_ba.py.  Generado por construye_familias_ba.py. NO editar a mano."""
'''


def main():
    for p, sha in [(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                   (os.path.join(N12, 'organismo_familias_b6.py'), SHA_B6),
                   (os.path.join(N12, 'organismo_familias_b5.py'), SHA_B5),
                   (os.path.join(N12, 'organismo_familias_b4b.py'), SHA_B4B),
                   (os.path.join(N12, 'escala_codigo.py'), SHA_ESCALA),
                   (os.path.join(CREA, 'organismo_v15f_on.py'), SHA_V15F_ON),
                   (os.path.join(JA, 'construye_familias_a1.py'), SHA_A1_CONSTR),
                   (os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'B', 'organismo_familias_jb.py'), SHA_JB)]:
        if h16(p) != sha:
            raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado.")

    t0 = origen(os.path.join(JA, 'organismo_familias_a1.py'), SHA_A1)
    t = CABECERA + t0

    # ---- 1. firma de run: la perilla nueva, al final
    t = sust(t, A_FIRMA, A_FIRMA[:-2] + ",conj_tipo=0):", etiqueta='firma de run')
    # ---- 2. validacion de la perilla y las dos incompatibilidades declaradas, tras la guarda de los dos tipos
    t = sust(t, A_GUARDA, A_GUARDA + NUEVO_CHK, etiqueta='validacion de conj_tipo')
    # ---- 3. LA LECTURA: la conjuncion POR TIPO, delante de la regla de `exige_dir` (que queda intacta)
    t = sust(t, A_EDV, NUEVO_LEE + A_EDV, etiqueta='conjuncion por tipo')
    # ---- 4. diagnostico: que lee la tabla PARA EL REFERENTE en el paso de la entrega
    t = sust(t, A_INIT, "_c4dt=None; _c4gt=None; _c4lp=None   # BA: `_c4lp` = que lee la tabla para el REFERENTE "
                        "tras la entrega.  # A1:", etiqueta='estado del diagnostico de lectura')
    t = sust(t, A_DT, A_DT + NUEVO_DIAG, etiqueta='diagnostico de lectura')
    # ---- 5. claves de salida
    t = sust(t, A_RET, "    return dict(conj_tipo=int(conj_tipo),canal_lee_ref=_c4lp,"
                       "mem_visto=([[bool(_x) for _x in _f] for _f in (_MNv>0)] if memoria_pares is not None else None),"
                       "dos_tipos=int(dos_tipos),", etiqueta='diccionario de salida')

    # ---------------------------------------------------------------- POSTCONDICIONES (ERR-38/41/42)
    if t.count('def _tabla_dos') != 1 or t.count('def _topk_tipo') != 1 or t.count('def _suma_tipo') != 1:
        raise SystemExit("POSTCONDICION: las funciones de A no quedaron definidas exactamente una vez. Abortado.")
    if t.count('if _CTv:') != 1 or t.count('if _nf7<len(_f7): return (0.0, False)') != 1:
        raise SystemExit("POSTCONDICION: la conjuncion por tipo no entra exactamente una vez. Abortado.")
    if t.count('if _EDv and (_nf7<len(_f7) or _nv7<len(_v7)): return (0.0, False)') != 1:
        raise SystemExit("POSTCONDICION: la regla `exige_dir` de A tiene que quedar INTACTA. Abortado.")
    if t.count('_dv=_dir_var(_cv,_Pv)') != 2:
        raise SystemExit("POSTCONDICION: la ESCRITURA se toco (tiene que ser la de b6, intacta). Abortado.")
    if t.count('rng.') != t0.count('rng.'):
        raise SystemExit(f"POSTCONDICION: el uso del rng cambio respecto de a1 ({t.count('rng.')} contra "
                         f"{t0.count('rng.')}). Abortado.")
    if t.count('_MGv=_empv[0] if len(_empv)==1 else int(_empv[int(rng.integers(len(_empv)))])') != 2:
        raise SystemExit("POSTCONDICION: la ganadora `_MGv` de b5/b6 y su desempate ya no estan intactos. Abortado.")
    if t.count("if var_cubre:") != 1 or t.count("_cs7=[_x7 for _x7 in _VMX if _q7 in _PARv[_x7]]") != 1:
        raise SystemExit("POSTCONDICION: la eleccion de ganadoras por tipo de A se toco. Abortado.")
    if t.count('def _dir_var') != 1 or t.count('def _bin4') != 1:
        raise SystemExit("POSTCONDICION: la DIRECCION del bloque 6 se toco. Abortado.")
    compile(t, DESTINO, 'exec')
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print("  ANCLAS sobre organismo_familias_a1.py  OK: 6 (1 firma, 1 validacion, 1 lectura, 2 diagnostico, 1 salida)")
    print(f"  escrito {os.path.relpath(DESTINO, RAIZ)}")
    print(f"  sha origen  organismo_familias_a1.py {SHA_A1}")
    print(f"  sha destino organismo_familias_ba.py {h16(DESTINO)}")
    print("  ahora: python experimentos/junta_fase5/BA/identidad_familias_ba.py")


if __name__ == '__main__':
    main()
