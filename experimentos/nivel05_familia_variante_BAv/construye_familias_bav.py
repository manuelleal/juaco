"""NIVEL 5 -- CANDIDATO **BA-v** (la variante incompleta VOTA con lo que sabe), con criterio propio (ERR-90).
Construye experimentos/nivel05_familia_variante_BAv/organismo_familias_bav.py POR ANCLAS, sobre
experimentos/junta_fase5/BA/organismo_familias_ba.py (1f196ee786b2040d; aqui SOLO SE LEE).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
retropropagacion, que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy, fase 5:
que el mensaje refiera a la FAMILIA **Y** a la VARIANTE con la MISMA tabla (BAR-T <= 5/20 Y PAR >= 15/20).

POR QUE ESTA CARPETA EXISTE (decision del director, 21-sep 16:30): `BA-v` (conj_tipo=2) cumplio el numero
crudo de la mision en las DOS series (921-940 y 941-960) y es la unica fila que lo ha hecho dos veces, pero
cayo en puertas RELATIVAS a CORTADO -- y su CORTADO es 0, lo que le impuso umbrales mas duros que a A1 con
CORTADO 4 (R2 BAR-T <= 3, R3 BAR-H <= 5, R4 VALOR <= 3). El criterio nuevo (ERR-90) es ABSOLUTO. Ademas R6
(coste) nunca se juzgo: la celda base `b4b` no se corrio y el runner no imprimia la puerta (ERR-89).

QUE SE ANADE AL INSTRUMENTO, Y POR QUE ES **UN CONTROL**, NO UN MECANISMO:
  `baraja_msg` (0): el CONTROL DE MEMORIA BARAJADA que el criterio nuevo exige. Con 1, el mensaje escribe
       LA MISMA R en una casilla PERMUTADA de la misma celda: se destruye la CORRESPONDENCIA (la direccion)
       sin cambiar el contenido ni la cantidad de informacion escrita. Es la baraja de N1/N3d llevada a la
       tabla. La permutacion sale de un Generator PROPIO (`default_rng(seed + 90090)`), asi que **no consume
       ni un numero del azar del organismo**: la trayectoria hasta el paso de la entrega es IDENTICA a la del
       candidato (el arnes lo comprueba con `canal_t_entrega`, `canal_gan_pre` y `canal_bin`), y lo unico que
       cambia es donde cae lo escrito. Si el candidato lee igual de bien con la tabla barajada, no esta
       leyendo el mensaje: esta comiendo porque llego un mensaje.
  `baraja_perm`: DIAGNOSTICO (no decide nada, no toca estado ni azar) -- la permutacion, para que el arnes
       compruebe que es una permutacion y que NO es la identidad.

CERO MEMORIA NUEVA EN EL CANDIDATO: con `baraja_msg=0` (el candidato y todas las celdas menos el control) no
se ejecuta ni una linea nueva y el organismo es `organismo_familias_ba` BIT A BIT -- y por su cadena, a1, b6,
b5, b4b, organismo_familias, organismo_v14 (TRONCO) y organismo_v15f_on.

QUE NO SE TOCA (ni una linea): la LECTURA (`_tabla_dos`, `conj_tipo`, `exige_dir`, `combina`), la eleccion de
ganadoras, `_dir_var`, `_bin4`, `_MGv` y su desempate al azar, `_MEv`, la escritura de la EXPERIENCIA PROPIA
(la del bocado: sigue en su direccion, intacta), el emisor, el canal, el mundo, la via rapida, la puerta, la
boca, el metabolismo y EL CONSUMO DEL RNG DEL ORGANISMO.

Uso:  python experimentos/nivel05_familia_variante_BAv/construye_familias_bav.py   (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
JBA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'BA')
JA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'A')
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')

SHA_BA = '1f196ee786b2040d'             # organismo_familias_ba.py (candidato BA, identidad 56/56) -- EL ORIGEN
SHA_BA_CONSTR = '503ada31c3da9a3b'      # construye_familias_ba.py
SHA_BA_RUNNER = 'f511d1bbe34887af'      # corre_familias_ba.py (el runner que se copia)
SHA_A1 = '8833e1dcfb62f26d'             # organismo_familias_a1.py (origen de BA)
SHA_B6 = 'b10cbd4ddd0c32a3'
SHA_B5 = 'e0b6b90f6f92d5c1'
SHA_B4B = 'b3dd1d7e66a2d147'
SHA_V14 = 'feefc88b1fd8d434'            # EL TRONCO
SHA_V15F_ON = '54d6efe0b564113c'
SHA_ESCALA = 'd8b8566bca77a0ae'
DESTINO = os.path.join(AQUI, 'organismo_familias_bav.py')


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


# ---------------------------------------------------------------- anclas en organismo_familias_ba.py
BA_FIRMA = ",dentro='suma',conj_tipo=0):"
BA_CHK = ('    if _CTv and _EDv: raise ValueError("conj_tipo=1 y exige_dir=1 son DOS reglas de abstencion '
          'distintas y no se componen (exige_dir hace callar a la tabla cuando la VARIANTE no consta; '
          'conj_tipo no). Se pide una.")   # BA\n')
BA_ESCRITURA_MSG = ("                    _Pv=_P4   # B4: el patron del MENSAJE, no el del objeto mordido\n"
                    "                    for _cv in range(_NP):\n"
                    "                        _dv=_dir_var(_cv,_Pv)   # B6: la MISMA direccion que usa la lectura\n")
BA_RET = "    return dict(conj_tipo=int(conj_tipo),"

NUEVO_CHK = (
    '    if (not isinstance(baraja_msg,int)) or isinstance(baraja_msg,bool) or baraja_msg not in (0,1): raise ValueError(f"baraja_msg={baraja_msg!r}: se espera 0 (apagado) o 1 (CONTROL: el mensaje escribe en una casilla permutada)")   # BA-v: perilla mal escrita no cae en silencio\n'
    '    _BMv=None   # BA-v: CONTROL de memoria barajada, APAGADO por defecto -> ni una linea nueva se ejecuta y el organismo es organismo_familias_ba BIT A BIT\n'
    '    if int(baraja_msg):\n'
    '        _bmg=np.random.default_rng(int(seed)+90090)   # rng PROPIO del control: NO consume el azar del organismo (el prefijo hasta la entrega queda IDENTICO al del candidato)\n'
    '        _BMv=np.stack([_bmg.permutation(_NCv) for _ in range(_NP)])   # una permutacion de las casillas POR CELDA: misma R, misma cantidad, direccion destruida\n')

NUEVO_ESCRITURA = (
    "                    _Pv=_P4   # B4: el patron del MENSAJE, no el del objeto mordido\n"
    "                    for _cv in range(_NP):\n"
    "                        _dv=_dir_var(_cv,_Pv)   # B6: la MISMA direccion que usa la lectura\n"
    "                        if _BMv is not None: _dv=int(_BMv[_cv,_dv])   # BA-v CONTROL `baraja_msg`: la MISMA R en una casilla PERMUTADA de la MISMA celda. No cambia ni el contenido ni la cantidad de lo escrito: cambia la CORRESPONDENCIA. Solo aqui (la escritura de la experiencia propia queda intacta).\n")

CABECERA = '''"""organismo_familias_bav = organismo_familias_ba.py (candidato BA de la junta de la fase 5, `conj_tipo`,
1f196ee786b2040d) + UN CONTROL, inerte por defecto:
  `baraja_msg` (0): con 1, el mensaje escribe LA MISMA R en una casilla PERMUTADA de la misma celda. Destruye
               la CORRESPONDENCIA del mensaje sin tocar su contenido ni su cantidad -- la baraja de N1/N3d
               llevada a la tabla. La permutacion sale de un Generator PROPIO (`default_rng(seed+90090)`):
               NO consume el azar del organismo, asi que la trayectoria hasta el paso de la entrega es
               identica a la del candidato y lo unico que cambia es donde cae lo escrito.
               Es un CONTROL QUE DEBE FALLAR: si el candidato sigue comiendo igual con la tabla barajada, no
               esta leyendo el mensaje.
  `baraja_perm`: DIAGNOSTICO (no decide nada) -- la permutacion, para que el arnes compruebe que lo es.
CERO MEMORIA NUEVA: con `baraja_msg=0` no se ejecuta ni una linea nueva.
ANCLA DE IDENTIDAD: con baraja_msg=0 es organismo_familias_ba BIT A BIT con CUALQUIER valor de conj_tipo, y
por su cadena organismo_familias_a1, b6, b5, b4b, b4, b3, b2, organismo_familias, organismo_v14 (TRONCO) y
organismo_v15f_on.
Arnes: identidad_familias_bav.py.  Generado por construye_familias_bav.py. NO editar a mano."""
'''


def main():
    for p, sha in [(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                   (os.path.join(JA, 'organismo_familias_a1.py'), SHA_A1),
                   (os.path.join(N12, 'organismo_familias_b6.py'), SHA_B6),
                   (os.path.join(N12, 'organismo_familias_b5.py'), SHA_B5),
                   (os.path.join(N12, 'organismo_familias_b4b.py'), SHA_B4B),
                   (os.path.join(N12, 'escala_codigo.py'), SHA_ESCALA),
                   (os.path.join(CREA, 'organismo_v15f_on.py'), SHA_V15F_ON),
                   (os.path.join(JBA, 'construye_familias_ba.py'), SHA_BA_CONSTR),
                   (os.path.join(JBA, 'corre_familias_ba.py'), SHA_BA_RUNNER)]:
        if h16(p) != sha:
            raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado.")

    t0 = origen(os.path.join(JBA, 'organismo_familias_ba.py'), SHA_BA)
    t = CABECERA + t0

    # ---- 1. firma de run: la perilla de control, al final
    t = sust(t, BA_FIRMA, BA_FIRMA[:-2] + ",baraja_msg=0):", etiqueta='firma de run')
    # ---- 2. validacion + la permutacion (rng PROPIO), tras las guardas de conj_tipo
    t = sust(t, BA_CHK, BA_CHK + NUEVO_CHK, etiqueta='validacion de baraja_msg')
    # ---- 3. LA BARAJA, SOLO en la escritura del MENSAJE (la de la experiencia propia queda intacta)
    t = sust(t, BA_ESCRITURA_MSG, NUEVO_ESCRITURA, etiqueta='baraja en la escritura del mensaje')
    # ---- 4. claves de salida
    t = sust(t, BA_RET, "    return dict(baraja_msg=int(baraja_msg),"
                        "baraja_perm=(None if _BMv is None else [[int(_x) for _x in _f] for _f in _BMv]),"
                        "conj_tipo=int(conj_tipo),", etiqueta='diccionario de salida')

    # ---------------------------------------------------------------- POSTCONDICIONES (ERR-38/41/42/89)
    if t.count('_dv=_dir_var(_cv,_Pv)') != 2:
        raise SystemExit("POSTCONDICION: las dos escrituras (mensaje y experiencia propia) tienen que seguir ahi. Abortado.")
    if t.count('if _BMv is not None: _dv=') != 1:
        raise SystemExit("POSTCONDICION: la baraja tiene que entrar EXACTAMENTE una vez (solo el mensaje). Abortado.")
    if t.count('rng.') != t0.count('rng.'):
        raise SystemExit(f"POSTCONDICION: el uso del rng DEL ORGANISMO cambio ({t.count('rng.')} contra "
                         f"{t0.count('rng.')}). Abortado.")
    if t.count('np.random.default_rng') != t0.count('np.random.default_rng') + 1:
        raise SystemExit("POSTCONDICION: se esperaba exactamente UN Generator nuevo (el del control). Abortado.")
    if t.count('if _CTv:') != 1 or t.count('if _nf7<len(_f7): return (0.0, False)') != 1 \
            or t.count('if _nv7<len(_v7) and (_CTv==1 or not _nv7): return (_sf7, True)') != 1:
        raise SystemExit("POSTCONDICION: la LECTURA de BA tiene que quedar INTACTA. Abortado.")
    if t.count('if _EDv and (_nf7<len(_f7) or _nv7<len(_v7)): return (0.0, False)') != 1:
        raise SystemExit("POSTCONDICION: la regla `exige_dir` de A tiene que quedar INTACTA. Abortado.")
    if t.count('_MGv=_empv[0] if len(_empv)==1 else int(_empv[int(rng.integers(len(_empv)))])') != 2:
        raise SystemExit("POSTCONDICION: la ganadora `_MGv` y su desempate ya no estan intactos. Abortado.")
    if t.count('def _dir_var') != 1 or t.count('def _bin4') != 1 or t.count('def _tabla_dos') != 1:
        raise SystemExit("POSTCONDICION: la DIRECCION o la lectura se tocaron. Abortado.")
    if t.count('def _topk_tipo') != 1 or t.count('def _suma_tipo') != 1 or t.count("if var_cubre:") != 1:
        raise SystemExit("POSTCONDICION: la eleccion de ganadoras por tipo se toco. Abortado.")
    compile(t, DESTINO, 'exec')
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print("  ANCLAS sobre organismo_familias_ba.py  OK: 4 (1 firma, 1 validacion+permutacion, 1 escritura, 1 salida)")
    print("  POSTCONDICIONES OK: 9 (dos escrituras, baraja una vez, rng del organismo intacto, un Generator")
    print("     nuevo, lectura de BA intacta, `exige_dir` intacta, `_MGv` intacta, direccion intacta, ganadoras)")
    print(f"  escrito {os.path.relpath(DESTINO, RAIZ)}")
    print(f"  sha origen  organismo_familias_ba.py  {SHA_BA}")
    print(f"  sha destino organismo_familias_bav.py {h16(DESTINO)}")
    print("  ahora: python experimentos/nivel05_familia_variante_BAv/identidad_familias_bav.py")


if __name__ == '__main__':
    main()
