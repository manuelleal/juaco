"""Construye experimentos/nivel12_mundo_familias/organismo_familias_b6.py POR ANCLAS, sobre
organismo_familias_b5.py (bloque 5, e0b6b90f6f92d5c1; aqui SOLO SE LEE).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop)
que aprende, desaprende, generaliza y se COMUNICA CON REFERENCIA. Hoy: que el mensaje distinga "sal rosa" de "sal".

DE DONDE VIENE (medido, no supuesto):
  - BLOQUE 5 (semillas 681-700 y 701-720, registro 18 sep 19:42 y 19:50): con k_ganadoras = 3 el mensaje con el
    patron de OTRO token cae a 2/20 y 4/18 (<= CORTADO + 3 en las dos series) con el canal intacto (19/20, 16/18):
    la referencia pasa de "alguna familia" a EXACTAMENTE ESTA FAMILIA. Pero LA HERMANA NO BAJA (15/20 y 13/18),
    porque las celdas de FORMA que ganan son ciegas a los 3 pixeles de variante. k = 5 no ayuda (7/20, 7/18) y
    rompe el cuerpo (muertes 199 y 152 contra 32-38). H-4 quedo cerrada: NO ES k.
  - Hecho ESTRUCTURAL del catalogo (escala_codigo.catalogo, T = 0, sin simular): en las semillas miradas
    (1, 2, 3, 721, 730, 741) T1v2 y T1v0 difieren SOLO en los pixeles 9 y 11 -- los dos dentro del bloque de
    variante 9-11. Luego una direccion que incluya esos 3 pixeles SI puede separar a las hermanas; una que no los
    incluya NO puede, por mucho que se multipliquen las celdas. Eso es exactamente lo que este instrumento prueba.

UNA PERILLA NUEVA, INERTE en su valor por defecto:

  `memoria_variante` (default 0) -- la DIRECCION de la tabla de pares. Con 1, cada celda escribe y lee en
                     (par de pixeles, bin del par, firma de los `fam_nvar` pixeles de variante), o sea
                     4 * 2^fam_nvar = 32 subcasillas por celda en vez de 4. Con 0, la direccion es el bin literal
                     de b5/b4b, la tabla vuelve a tener 4 columnas y NO se consume rng adicional -> b5 BIT A BIT.

POR QUE A TODAS LAS CELDAS Y A TODOS LOS ACCESOS (escritura Y lectura), decidido y escrito ANTES de medir:
  La tabla es una memoria direccionada por contenido: se lee de la MISMA direccion en la que se escribio. Si el
  sufijo se aplicara solo a la LECTURA, el mensaje quedaria escrito en la casilla `4*bin` y la boca leeria en
  `8*bin + firma`: NINGUNA lectura encontraria nunca nada, la via lenta abstendria siempre y el organismo seria el
  lineal de v14.1 con pasos de mas. No es una variante conservadora: es romper el instrumento. Por eso el sufijo
  entra en UNA sola funcion, `_dir_var`, y esa funcion se usa en los TRES accesos (escritura por mensaje,
  escritura por mordida, lectura). La alternativa real que existia -- leer primero la subcasilla con sufijo y, si
  no se conoce, recaer en el bin sin sufijo -- se DESCARTA por escrito: (a) el mensaje escribiria tambien el bin
  sin sufijo, que es justamente por donde se cuela la hermana, asi que reintroduce la fuga que este bloque ataca;
  (b) si el mensaje escribiera solo la subcasilla con sufijo, hace falta una regla de precedencia nueva y dos
  direcciones por acceso: mas maquinaria, contra Occam; (c) no tiene control gratis (memoria_variante=0 SI lo
  tiene: es b5 bit a bit).
  EL PRECIO, declarado: la tabla propia del organismo se vuelve 8 veces mas dispersa, aprende mas despacio por
  casilla y abstiene mas (releva a la lineal). Eso lo vigilan el gemelo mudo CORTADO, las muertes y okU (R6).

LO QUE NO SE TOCA: el emisor (corre con memoria_variante=0 y k_ganadoras=1: es b4b bit a bit), el canal, el
  mundo, la seleccion de la ganadora `_MGv` y su desempate al azar, el error propio por celda `_MEv`, la regla de
  sobrescritura de R CRUDO, la boca, el consumo del rng. Solo cambia DONDE escribe y lee cada celda.

ANCLA DE IDENTIDAD (regla 2 de EQUIPO.md), lo que comprueba identidad_familias_b6.py:
  (a) con memoria_variante=0 -> organismo_familias_b5 BIT A BIT para CUALQUIER k, y el rng NO se consume; por la
      cadena de b5, tambien b4b, b4, b3, b2, organismo_familias, organismo_v14 (TRONCO) y organismo_v15f_on;
  (b) con memoria_pares=None la perilla es INERTE (no hay tabla que direccionar);
  (c) la direccion con sufijo es una funcion del patron presente y nada mas (misma retina -> misma direccion);
  (d) controles que DEBEN fallar (memoria_variante=1 cambia la corrida y separa a las hermanas).

Uso:  python experimentos/nivel12_mundo_familias/construye_familias_b6.py     (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

SHA_B5 = 'e0b6b90f6f92d5c1'           # organismo_familias_b5.py (bloque 5, identidad 106/106)
SHA_B4B = 'b3dd1d7e66a2d147'
SHA_B4 = 'ff9946ee2ffe27e6'
SHA_B3 = '62a1e53b452b078e'
SHA_B2 = '30200bea6a41c3c8'
SHA_MF = 'b9dd561a0cf056b8'
SHA_V14 = 'feefc88b1fd8d434'
SHA_V15F_ON = '54d6efe0b564113c'
SHA_ESCALA = 'd8b8566bca77a0ae'
DESTINO = os.path.join(AQUI, 'organismo_familias_b6.py')


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


# ---------------------------------------------------------------- anclas en organismo_familias_b5.py
A_FIRMA = ",voraz=0.0,par_herm=None,k_ganadoras=1):"
A_CHK = ('    if (not isinstance(k_ganadoras,int)) or isinstance(k_ganadoras,bool) or k_ganadoras<1: '
         'raise ValueError(f"k_ganadoras={k_ganadoras!r}: entero >= 1")   '
         '# B5: perilla mal escrita no cae en silencio\n')
A_TABLA = ("    _MMv=np.zeros((_NP,4)); _MNv=np.zeros((_NP,4)); _MEv=np.full(_NP,1e9); _MGv=0   "
           "# v15f: R CRUDO por casilla, visitas, error propio por celda, ganadora\n")
A_BIN = "        _i4,_j4=_PARv[_g]; return int(_P[_i4])*2+int(_P[_j4])\n"
A_LEE1 = "            _i,_j=_PARv[_MGv]; _c=int(P[_i])*2+int(P[_j])\n"
A_LEEK = "            _i,_j=_PARv[_g5]; _c=int(P[_i])*2+int(P[_j])\n"
A_ESCRIBE = "_iv,_jv=_PARv[_cv]; _dv=int(_Pv[_iv])*2+int(_Pv[_jv])"
A_INIT = "; _c4kp=None; _c4kq=None; _c4mbk=None   #"   # OJO: el `#` va en el ancla; `_c4mdk` entra ANTES del comentario
A_MBK = ("            _c4mbk=sorted(_n5 for _n5 in PAT if all(_bin4(_g5,PAT[_n5])==_bin4(_g5,_P4) "
         "for _g5 in _topk_b5()))   # B5: DIAGNOSTICO -- cuantos de los 32 estimulos caen en LAS k casillas del "
         "mensaje (con k=1 es _c4mb recalculado DESPUES de escribir)\n")
A_RET = "    return dict(k_ganadoras=int(k_ganadoras),"

NUEVO_CHK = (
    '    if (not isinstance(memoria_variante,int)) or isinstance(memoria_variante,bool) or memoria_variante not in (0,1): raise ValueError(f"memoria_variante={memoria_variante!r}: se espera 0 o 1")   # B6: perilla mal escrita no cae en silencio\n'
    "    _MVv=int(memoria_variante); _NV=(int(fam_nvar) if _MVv else 0)   # B6: cuantos pixeles de VARIANTE entran en la direccion -- los ULTIMOS _NV de la retina (con fam_D=12 y fam_nvar=3: los pixeles 9, 10 y 11)\n"
    '    if _MVv and not (1<=_NV<_D): raise ValueError(f"fam_nvar={fam_nvar!r}: con memoria_variante=1 se espera 1 <= fam_nvar < {_D} (la firma no puede comerse la retina entera)")   # B6\n'
    "    _NCv=(4<<_NV) if _MVv else 4   # B6: SUBCASILLAS por celda = 4 bins x 2^_NV firmas (32 con fam_nvar=3). Apagada: las 4 de v15f, EXACTAS\n")

NUEVO_TABLA = ("    _MMv=np.zeros((_NP,_NCv)); _MNv=np.zeros((_NP,_NCv)); _MEv=np.full(_NP,1e9); _MGv=0   "
               "# v15f: R CRUDO por casilla, visitas, error propio por celda, ganadora. B6: `casilla` = DIRECCION "
               "LOCAL (bin del par [, firma de variante]); con memoria_variante=0, _NCv=4 -> b5 EXACTO\n")

NUEVO_DIR = (
    A_BIN +
    "    def _dir_var(_g,_P):   # B6: LA DIRECCION LOCAL de la celda _g para el patron _P. Apagada = el bin de 2 bits de b5/b4b, literalmente. Encendida = (bin, firma de los _NV pixeles de variante): la MISMA funcion se usa en los TRES accesos (mensaje, mordida, lectura), porque una memoria direccionada por contenido se lee donde se escribio.\n"
    "        _b6=_bin4(_g,_P)\n"
    "        if not _MVv: return _b6\n"
    "        _s6=0\n"
    "        for _q6 in range(_D-_NV,_D): _s6=_s6*2+int(_P[_q6])   # firma LOCAL: solo la retina presente; sin estado compartido, sin rng, sin señal nueva\n"
    "        return _b6*(1<<_NV)+_s6\n")

NUEVO_MBK = (
    A_MBK +
    "            _c4mdk=sorted(_n6 for _n6 in PAT if all(_dir_var(_g6,PAT[_n6])==_dir_var(_g6,_P4) for _g6 in _topk_b5()))   # B6: DIAGNOSTICO -- cuantos de los 32 estimulos caen en LAS k DIRECCIONES del mensaje (con memoria_variante=0 es exactamente _c4mbk)\n")


CABECERA = '''"""organismo_familias_b6 = organismo_familias_b5.py (bloque 5, `k_ganadoras`, e0b6b90f6f92d5c1)
+ UNA PERILLA para el BLOQUE 6 (SUFIJO DE VARIANTE), inerte por defecto:
  `memoria_variante` (default 0): la DIRECCION de la tabla de pares. Con 1, cada celda escribe Y lee en
               (par de pixeles, bin del par, firma de los `fam_nvar` pixeles de variante) -- 4 * 2^fam_nvar = 32
               subcasillas por celda en vez de 4. La firma se calcula de la RETINA PRESENTE: sin estado
               compartido, sin gradiente, sin supervisor, sin rng, sin señal nueva. NO cambian el emisor, el
               canal, el mundo, la seleccion de la ganadora `_MGv`, el error propio `_MEv`, la regla de
               sobrescritura de R CRUDO, la boca ni el consumo del rng: SOLO cambia DONDE escribe y lee la celda.
               Con 0, `_dir_var` devuelve el bin literal de b5/b4b y la tabla tiene 4 columnas.
POR QUE A LA ESCRITURA Y A LA LECTURA: una memoria direccionada por contenido se lee en la direccion en la que se
escribio; un sufijo solo en la lectura no encontraria NUNCA nada (ver construye_familias_b6.py, encabezado).
ANCLA DE IDENTIDAD: con memoria_variante=0 es organismo_familias_b5 BIT A BIT para cualquier `k_ganadoras` y, por
su cadena, b4b, b4, b3, b2, organismo_familias, organismo_v14 (TRONCO) y organismo_v15f_on.
Arnes: identidad_familias_b6.py.  Generado por construye_familias_b6.py. NO editar a mano."""
'''


def main():
    for p, sha in [(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                   (os.path.join(AQUI, 'organismo_familias.py'), SHA_MF),
                   (os.path.join(AQUI, 'organismo_familias_b2.py'), SHA_B2),
                   (os.path.join(AQUI, 'organismo_familias_b3.py'), SHA_B3),
                   (os.path.join(AQUI, 'organismo_familias_b4.py'), SHA_B4),
                   (os.path.join(AQUI, 'organismo_familias_b4b.py'), SHA_B4B),
                   (os.path.join(AQUI, 'escala_codigo.py'), SHA_ESCALA),
                   (os.path.join(CREA, 'organismo_v15f_on.py'), SHA_V15F_ON)]:
        if h16(p) != sha:
            raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado.")

    t0 = origen(os.path.join(AQUI, 'organismo_familias_b5.py'), SHA_B5)
    t = CABECERA + t0

    # ---- 1. firma de run: la perilla nueva, al final
    t = sust(t, A_FIRMA, A_FIRMA[:-2] + ",memoria_variante=0):", etiqueta='firma de run')
    # ---- 2. validacion + tamaño de la firma + numero de subcasillas
    t = sust(t, A_CHK, A_CHK + NUEVO_CHK, etiqueta='validacion de memoria_variante')
    # ---- 3. la tabla: 4 columnas apagada, 4*2^_NV encendida
    t = sust(t, A_TABLA, NUEVO_TABLA, etiqueta='tamaño de la tabla')
    # ---- 4. LA UNICA FUNCION NUEVA: la direccion local
    t = sust(t, A_BIN, NUEVO_DIR, etiqueta='direccion local de variante')
    # ---- 5. LECTURA (los dos caminos de _tabla_v15f: k<=1 y k>1)
    t = sust(t, A_LEE1, "            _c=_dir_var(_MGv,P)   # B6: la DIRECCION (con memoria_variante=0 es el bin literal de b5/b4b)\n",
             etiqueta='lectura k<=1')
    t = sust(t, A_LEEK, "            _c=_dir_var(_g5,P)\n", etiqueta='lectura k>1')
    # ---- 6. ESCRITURA (mensaje y mordida): la MISMA direccion que la lectura
    t = sust(t, A_ESCRIBE, "_dv=_dir_var(_cv,_Pv)   # B6: la MISMA direccion que usa la lectura",
             n=2, etiqueta='escritura (mensaje y mordida)')
    # ---- 7. diagnostico: quien comparte LAS k DIRECCIONES del mensaje (observado, no prometido)
    t = sust(t, A_INIT, "; _c4kp=None; _c4kq=None; _c4mbk=None; _c4mdk=None   # B6: `_c4mdk` = quien comparte "
                        "LAS k DIRECCIONES (bin + firma) del referente.  #",
             etiqueta='estado del diagnostico por direccion')
    t = sust(t, A_MBK, NUEVO_MBK, etiqueta='diagnostico por direccion')
    # ---- 8. claves de salida
    t = sust(t, A_RET, "    return dict(memoria_variante=int(memoria_variante),memoria_slots=int(_NCv),"
                       "memoria_nvar=int(_NV),canal_mismo_dir_k=_c4mdk,k_ganadoras=int(k_ganadoras),",
             etiqueta='diccionario de salida')

    if t.count('def _dir_var') != 1:
        raise SystemExit("POSTCONDICION: la direccion local no quedo definida exactamente una vez. Abortado.")
    if t.count('_dv=_dir_var(_cv,_Pv)') != 2 or t.count('_c=_dir_var(') != 2:
        raise SystemExit("POSTCONDICION: los TRES accesos (2 escrituras + 2 lecturas) no comparten `_dir_var`. Abortado.")
    if 'return int(_P[_i4])*2+int(_P[_j4])' not in t:
        raise SystemExit("POSTCONDICION: el bin de 2 bits de b4b ya no es la base de la direccion. Abortado.")
    if t.count('rng.') != t0.count('rng.'):
        raise SystemExit(f"POSTCONDICION: el uso del rng cambio respecto de b5 ({t.count('rng.')} contra "
                         f"{t0.count('rng.')}). Abortado.")
    compile(t, DESTINO, 'exec')
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print("  ANCLAS sobre organismo_familias_b5.py  OK: 9 (1 firma, 1 validacion, 1 tabla, 1 direccion, "
          "2 lecturas, 2 escrituras [un ancla x2], 2 diagnostico, 1 salida)")
    print(f"  escrito {os.path.relpath(DESTINO, RAIZ)}")
    print(f"  sha origen  organismo_familias_b5.py {SHA_B5}")
    print(f"  sha destino organismo_familias_b6.py {h16(DESTINO)}")
    print("  ahora: python experimentos/nivel12_mundo_familias/identidad_familias_b6.py")


if __name__ == '__main__':
    main()
