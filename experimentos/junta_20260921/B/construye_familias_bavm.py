"""NIVEL 5 -- CANDIDATO **BA-vm** (fase 5, junta del 21-sep, creador B): *la variante vota con su PEOR casilla,
no con la suma*. Construye experimentos/junta_20260921/B/organismo_familias_bavm.py POR ANCLAS, sobre
experimentos/nivel05_familia_variante_BAv/organismo_familias_bav.py (2dca0a3e239481f0; aqui SOLO SE LEE).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
retropropagacion, que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy, fase 5:
que el mensaje refiera a la FAMILIA **Y** a la VARIANTE con la MISMA tabla (BAR-T <= 5/20 Y PAR >= 15/20).

POR QUE ESTA CARPETA EXISTE: `PREREGISTRO_bavm.md` (creador B, 21-sep 16:06), escrito ANTES de construir nada.
BA-vm es un CANDIDATO APARTE con preregistro propio: **no reabre BA-v** (linea cerrada, REGISTRO_etapas_1_2.md
"LINEA CERRADA: BA / BA-v"). Lo que se mide es la LECTURA; el emisor, el canal y el mundo son los del bloque 6.

QUE SE ANADE, Y POR QUE ES MEMORIA NUEVA CERO: la perilla `dentro` YA EXISTE en la firma desde A1 con valores
('suma','min'), pero `_DMv` se calculaba y **NUNCA SE USABA**: `dentro='min'` era una perilla DESCONECTADA (por
eso ninguna celda de ninguna serie la uso jamas; comprobado por grep sobre los runners). Este constructor la
CONECTA y le anade el tercer valor:
  `dentro='suma'` (defecto)  = organismo_familias_bav BIT A BIT (ni una linea nueva se ejecuta).
  `dentro='minv'` (CANDIDATO) = dentro del tipo VARIANTE la lectura es `k * min(casillas conocidas)` en vez de
        la suma; el tipo FORMA sigue sumando. El minimo va ESCALADO por el numero de casillas conocidas para
        que el valor siga en la escala de k (con las tres casillas del mensaje de acuerdo, 3*min(+1,+1,+1)=+3
        = exactamente lo de hoy: `CANAL` no pierde margen).
  `dentro='min'`  (ABLACION preregistrada) = el minimo escalado en LOS DOS tipos.
  `dentro != 'suma'` EXIGE `dos_tipos=1` y LANZA en cualquier otro caso o con un valor que no sea uno de los tres.

DIAGNOSTICO NUEVO (no decide ninguna prediccion, no toca estado ni rng): `canal_lee_herm` = que lee la tabla
PARA LAS HERMANAS del referente en el paso EXACTO de la entrega, [valor, habla, exactas FORMA, exactas VARIANTE].
Es el hueco declarado en PROPUESTA.md 5 ("lo unico que hoy no se pudo verificar").

QUE NO SE TOCA (ni una linea): el emisor, el canal, el mundo, la ESCRITURA (las dos: mensaje y experiencia
propia), `_dir_var`, `_bin4`, `_topk_tipo`, `_tabla_dos` salvo el argumento de tipo, `_MGv` y su desempate al
azar, `_MEv`, la via rapida, la puerta, la boca, el metabolismo y EL CONSUMO DEL RNG DEL ORGANISMO.

Uso:  python experimentos/junta_20260921/B/construye_familias_bavm.py   (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))   # .../bundle (esta carpeta cuelga de experimentos/junta_20260921/B)
BAV = os.path.join(RAIZ, 'experimentos', 'nivel05_familia_variante_BAv')
JBA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'BA')
JA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'A')
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')

SHA_BAV = '2dca0a3e239481f0'             # organismo_familias_bav.py -- EL ORIGEN
SHA_BAV_RUNNER = '4453754a9921e349'      # corre_familias_bav.py (el runner que se copia)
SHA_BA = '1f196ee786b2040d'              # organismo_familias_ba.py (origen de BA-v)
SHA_A1 = '8833e1dcfb62f26d'
SHA_B6 = 'b10cbd4ddd0c32a3'
SHA_B5 = 'e0b6b90f6f92d5c1'
SHA_B4B = 'b3dd1d7e66a2d147'
SHA_V14 = 'feefc88b1fd8d434'             # EL TRONCO
SHA_V15F_ON = '54d6efe0b564113c'
SHA_ESCALA = 'd8b8566bca77a0ae'
DESTINO = os.path.join(AQUI, 'organismo_familias_bavm.py')


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


# ---------------------------------------------------------------- anclas en organismo_familias_bav.py
A_VALIDA = ('    if dentro not in ("suma","min"): raise ValueError(f"dentro={dentro!r}: se espera \'suma\' o \'min\'")   # A1\n'
            "    _DMv=int(dentro=='min')   # A1: DENTRO del tipo, suma (b5) o MINIMO escalado (pesimista). Con todas las casillas de acuerdo los dos dan LO MISMO: solo difieren cuando las ganadoras discrepan, y ahi el pesimista NO muerde\n")

N_VALIDA = ('    if dentro not in ("suma","minv","min"): raise ValueError(f"dentro={dentro!r}: se espera \'suma\' (b5/BA-v), \'minv\' (BA-vm: el minimo escalado SOLO en el tipo VARIANTE) o \'min\' (BA-vM: en los dos tipos)")   # BA-vm: perilla mal escrita no cae en silencio\n'
            '    _DMv=int(dentro in ("minv","min"))   # BA-vm: DENTRO del tipo, suma (b5/BA-v, DEFECTO) o MINIMO ESCALADO por el n.o de casillas conocidas (pesimista). Con todas las casillas de acuerdo los dos dan LO MISMO: solo difieren cuando las ganadoras discrepan, y ahi el pesimista NO muerde\n'
            "    _MINV=int(dentro=='minv')   # BA-vm: EL CANDIDATO -- el pesimismo SOLO en el tipo VARIANTE (el que veta); con 'min' (ABLACION preregistrada) va tambien en el de FORMA\n"
            '    if _DMv and not int(dos_tipos): raise ValueError(f"dentro={dentro!r} EXIGE dos_tipos=1: sin los dos tipos de ganadora no hay tipo VARIANTE en el que ser pesimista")   # BA-vm\n')

A_SUMA = ("    def _suma_tipo(_gs,P):   # A1: la SUMA de las casillas CONOCIDAS de un tipo y cuantas conoce (la lectura de b5, restringida al tipo)\n"
          "        _s7=0.0; _n7=0\n"
          "        for _g7 in _gs:\n"
          "            _c7=_dir_var(_g7,P)\n"
          "            if _MNv[_g7,_c7]>0: _s7+=float(_MMv[_g7,_c7]); _n7+=1\n"
          "        return _s7,_n7\n")

N_SUMA = ("    def _suma_tipo(_gs,P,_tv=0):   # A1: la SUMA de las casillas CONOCIDAS de un tipo y cuantas conoce (la lectura de b5, restringida al tipo).  BA-vm: `_tv`=1 marca el tipo VARIANTE. Se LEEN LAS MISMAS casillas, en el mismo orden: lo unico que puede cambiar es QUE ESCALAR se devuelve.\n"
          "        _s7=0.0; _n7=0; _m7=0.0\n"
          "        for _g7 in _gs:\n"
          "            _c7=_dir_var(_g7,P)\n"
          "            if _MNv[_g7,_c7]>0: _x7=float(_MMv[_g7,_c7]); _s7+=_x7; _n7+=1; _m7=(_x7 if _n7==1 else (_x7 if _x7<_m7 else _m7))\n"
          "        if _DMv and _n7 and (_tv or not _MINV): return float(_n7)*_m7,_n7   # BA-vm: LA LINEA NUEVA -- el tipo vota con su PEOR casilla, ESCALADA a k para no perder la escala del valor (con todas de acuerdo da exactamente la suma). Ni un array, ni un contador, ni un bit de memoria nueva.\n"
          "        return _s7,_n7   # BA-v: la suma, literal\n")

A_LEE = "        _f7,_v7=_topk_tipo(); _sf7,_nf7=_suma_tipo(_f7,P); _sv7,_nv7=_suma_tipo(_v7,P)\n"
N_LEE = "        _f7,_v7=_topk_tipo(); _sf7,_nf7=_suma_tipo(_f7,P); _sv7,_nv7=_suma_tipo(_v7,P,1)   # BA-vm: `_tv`=1 SOLO en la llamada del tipo VARIANTE\n"

A_PESOS = "                                _ft8,_vt8=_topk_tipo(); _sf8,_nf8=_suma_tipo(_ft8,_Pv); _sv8,_nv8=_suma_tipo(_vt8,_Pv)\n"
N_PESOS = "                                _ft8,_vt8=_topk_tipo(); _sf8,_nf8=_suma_tipo(_ft8,_Pv); _sv8,_nv8=_suma_tipo(_vt8,_Pv,1)   # BA-vm: el mismo marcador de tipo (con pesos_tipo=0 -- todas las celdas de la serie -- esta rama no corre)\n"

A_INIT = "_c4dt=None; _c4gt=None; _c4lp=None   # BA:"
N_INIT = "_c4dt=None; _c4gt=None; _c4lp=None; _c4lh=None   # BA-vm: `_c4lh` = que lee la tabla para LAS HERMANAS del referente en el paso de la entrega (DIAGNOSTICO; no toca estado ni rng).  # BA:"

A_DIAG = "            _c4lp=([round(float(_tabla_dos(PAT[_c4r])[0]),4),bool(_tabla_dos(PAT[_c4r])[1]),int(_suma_tipo(_topk_tipo()[0],PAT[_c4r])[1]),int(_suma_tipo(_topk_tipo()[1],PAT[_c4r])[1])] if (_DTv and _c4r in PAT) else None)"
N_DIAG = (A_DIAG.replace("int(_suma_tipo(_topk_tipo()[1],PAT[_c4r])[1])", "int(_suma_tipo(_topk_tipo()[1],PAT[_c4r],1)[1])")
          + "\n            _c4lh=({_h4:[round(float(_tabla_dos(PAT[_h4])[0]),4),bool(_tabla_dos(PAT[_h4])[1]),int(_suma_tipo(_topk_tipo()[0],PAT[_h4])[1]),int(_suma_tipo(_topk_tipo()[1],PAT[_h4],1)[1])] for _h4 in ((_FA['herm'].get(_c4r) or []) if _MF else []) if _h4 in PAT} if (_DTv and _MF) else None)   # BA-vm: DIAGNOSTICO -- lo mismo PARA LAS HERMANAS del referente (PROPUESTA 5: el hueco declarado). Solo LEE: no toca estado, no consume rng y no decide ninguna prediccion.")

A_RET = "canal_lee_ref=_c4lp,"
N_RET = "canal_lee_ref=_c4lp,canal_lee_herm=_c4lh,"

CABECERA = '''"""organismo_familias_bavm = organismo_familias_bav.py (candidato BA-v del nivel 5, `baraja_msg`,
2dca0a3e239481f0) + LA PERILLA `dentro` CONECTADA, inerte por defecto:
  `dentro='suma'` (DEFECTO): organismo_familias_bav BIT A BIT -- ni una linea nueva se ejecuta.
  `dentro='minv'` (**EL CANDIDATO BA-vm**): dentro del tipo VARIANTE la tabla vota con su PEOR casilla,
               ESCALADA por el numero de casillas conocidas (`k*min`), en vez de con la suma. El tipo FORMA
               sigue sumando. Con todas las casillas de acuerdo `k*min` == suma: `CANAL` no pierde margen.
  `dentro='min'`  (**LA ABLACION BA-vM**, preregistrada antes de los datos): el minimo escalado en LOS DOS tipos.
  `dentro != 'suma'` EXIGE `dos_tipos=1`. Cualquier otro valor LANZA.
OJO (hallazgo del constructor): en a1/ba/bav `_DMv` se calculaba y NUNCA SE USABA -- `dentro='min'` era una
perilla DESCONECTADA. Ninguna celda de ninguna serie la uso (grep sobre los runners), asi que conectarla no
rejuzga nada hacia atras (regla 3); aqui queda con la semantica del PREREGISTRO_bavm.md 2.
MEMORIA NUEVA CERO: las mismas 66 celdas, las mismas casillas, la MISMA escritura, el mismo `_dir_var`, el
mismo `_topk_tipo`, el mismo `_MEv` y el mismo consumo del rng del organismo.
DIAGNOSTICO NUEVO: `canal_lee_herm` (que lee la tabla para las HERMANAS del referente en el paso de la
entrega). Solo lee: no toca estado ni el azar del organismo.
ANCLA DE IDENTIDAD: con dentro='suma' es organismo_familias_bav BIT A BIT (y con baraja_msg=0, tambien
organismo_familias_ba, a1, b6, b5, b4b, organismo_familias, organismo_v14 (TRONCO) y organismo_v15f_on).
Arnes: identidad_familias_bavm.py.  Generado por construye_familias_bavm.py. NO editar a mano."""
'''


def main():
    for p, sha in [(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                   (os.path.join(JBA, 'organismo_familias_ba.py'), SHA_BA),
                   (os.path.join(JA, 'organismo_familias_a1.py'), SHA_A1),
                   (os.path.join(N12, 'organismo_familias_b6.py'), SHA_B6),
                   (os.path.join(N12, 'organismo_familias_b5.py'), SHA_B5),
                   (os.path.join(N12, 'organismo_familias_b4b.py'), SHA_B4B),
                   (os.path.join(N12, 'escala_codigo.py'), SHA_ESCALA),
                   (os.path.join(CREA, 'organismo_v15f_on.py'), SHA_V15F_ON),
                   (os.path.join(BAV, 'corre_familias_bav.py'), SHA_BAV_RUNNER)]:
        if h16(p) != sha:
            raise SystemExit(f"TRIPWIRE {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado.")

    t0 = origen(os.path.join(BAV, 'organismo_familias_bav.py'), SHA_BAV)
    t = CABECERA + t0

    # ---- 1. la perilla `dentro`: tercer valor, conexion y la guarda de dos_tipos
    t = sust(t, A_VALIDA, N_VALIDA, etiqueta='validacion de dentro')
    # ---- 2. LA LINEA NUEVA, dentro de `_suma_tipo` (la funcion que ya existia)
    t = sust(t, A_SUMA, N_SUMA, etiqueta='_suma_tipo')
    # ---- 3. el marcador de tipo en la llamada de la LECTURA
    t = sust(t, A_LEE, N_LEE, etiqueta='llamada de _tabla_dos')
    # ---- 4. el marcador de tipo en la rama de pesos_tipo (apagada en todas las celdas)
    t = sust(t, A_PESOS, N_PESOS, etiqueta='llamada de pesos_tipo')
    # ---- 5/6/7. el diagnostico nuevo `canal_lee_herm`
    t = sust(t, A_INIT, N_INIT, etiqueta='init de _c4lh')
    t = sust(t, A_DIAG, N_DIAG, etiqueta='diagnostico canal_lee_herm')
    t = sust(t, A_RET, N_RET, etiqueta='diccionario de salida')

    # ---------------------------------------------------------------- POSTCONDICIONES (ERR-38/41/42/88/89)
    if t.count('if _DMv and _n7 and (_tv or not _MINV): return float(_n7)*_m7,_n7') != 1:
        raise SystemExit("POSTCONDICION: LA LINEA NUEVA tiene que entrar EXACTAMENTE una vez. Abortado.")
    if t.count('_suma_tipo(') != t0.count('_suma_tipo(') + 2:
        raise SystemExit(f"POSTCONDICION: las llamadas a _suma_tipo no son las esperadas ({t.count('_suma_tipo(')} contra {t0.count('_suma_tipo(')}+2 del diagnostico). Abortado.")
    if t.count(',_Pv,1)') + t.count(',P,1)') + t.count(',PAT[_c4r],1)') + t.count(',PAT[_h4],1)') != 4:
        raise SystemExit("POSTCONDICION: el marcador de tipo VARIANTE tiene que estar en las CUATRO llamadas del tipo. Abortado.")
    if t.count('_dv=_dir_var(_cv,_Pv)') != 2 or t.count('if _BMv is not None: _dv=') != 1:
        raise SystemExit("POSTCONDICION: LA ESCRITURA (mensaje y experiencia propia) y la baraja tienen que quedar INTACTAS. Abortado.")
    if t.count('rng.') != t0.count('rng.'):
        raise SystemExit(f"POSTCONDICION: el uso del rng DEL ORGANISMO cambio ({t.count('rng.')} contra {t0.count('rng.')}). Abortado.")
    if t.count('np.random.default_rng') != t0.count('np.random.default_rng'):
        raise SystemExit("POSTCONDICION: no se puede crear ningun Generator nuevo. Abortado.")
    if t.count('def _dir_var') != 1 or t.count('def _bin4') != 1 or t.count('def _tabla_dos') != 1 \
            or t.count('def _topk_tipo') != 1 or t.count('def _suma_tipo') != 1:
        raise SystemExit("POSTCONDICION: la DIRECCION, la lectura o la eleccion de ganadoras se tocaron. Abortado.")
    for frag in ("if _nf7<len(_f7): return (0.0, False)",
                 "if _nv7<len(_v7) and (_CTv==1 or not _nv7): return (_sf7, True)",
                 "if _EDv and (_nf7<len(_f7) or _nv7<len(_v7)): return (0.0, False)",
                 "if var_cubre:"):
        if t.count(frag) != 1:
            raise SystemExit(f"POSTCONDICION: la LECTURA de BA/A1 ya no esta intacta ({frag!r}). Abortado.")
    if t.count('_MGv=_empv[0] if len(_empv)==1 else int(_empv[int(rng.integers(len(_empv)))])') != 2:
        raise SystemExit("POSTCONDICION: la ganadora `_MGv` y su desempate ya no estan intactos. Abortado.")
    if t.count('_MEv[_cv]=') != t0.count('_MEv[_cv]='):
        raise SystemExit("POSTCONDICION: el error propio `_MEv` se toco. Abortado.")
    compile(t, DESTINO, 'exec')
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print("  ANCLAS sobre organismo_familias_bav.py  OK: 7 (1 validacion, 1 _suma_tipo, 2 marcadores de tipo,")
    print("     2 del diagnostico `canal_lee_herm`, 1 salida)")
    print("  POSTCONDICIONES OK: 10 (linea nueva una vez, llamadas a _suma_tipo, 4 marcadores de tipo,")
    print("     escritura+baraja intactas, rng del organismo intacto, ningun Generator nuevo, direccion y")
    print("     ganadoras intactas, lectura de BA/A1 intacta, `_MGv` intacta, `_MEv` intacta)")
    print(f"  escrito {os.path.relpath(DESTINO, RAIZ)}")
    print(f"  sha origen  organismo_familias_bav.py  {SHA_BAV}")
    print(f"  sha destino organismo_familias_bavm.py {h16(DESTINO)}")
    print(f"  (informativo) construye_familias_bav.py {h16(os.path.join(BAV, 'construye_familias_bav.py'))}")
    print("  ahora: python experimentos/junta_20260921/B/identidad_familias_bavm.py")


if __name__ == '__main__':
    main()
