"""JUNTA FASE 5 -- CREADOR A (matematica del aprendizaje local).
Construye experimentos/junta_fase5/A/organismo_familias_a1.py POR ANCLAS, sobre
experimentos/nivel12_mundo_familias/organismo_familias_b6.py (bloque 6, b10cbd4ddd0c32a3; aqui SOLO SE LEE).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin
backprop) que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy, fase 5: que el
mensaje refiera a la FAMILIA **Y** a la VARIANTE con la MISMA tabla.

DE DONDE VIENE (medido, no supuesto):
  - BLOQUE 5 (k = 3 ganadoras, 681-700 y 701-720): BAR-T 2/20 y 4/18 (familia EXACTA) pero BAR-H 15/20 y 13/18 y
    PAR 12/20 y 9/18: las celdas que ganan son de FORMA y son CIEGAS a los 3 px de variante.
  - BLOQUE 6 (sufijo de variante en la DIRECCION, 721-740 y 741-760): PAR 15/20 y 15/18, BAR-H 6/20 y 5/18 --
    pero BAR-T sube a 11/20 y 10/18 y la base sin mensaje sube de 0 a 6/20 y 4/18.
  - LECTURA MATEMATICA DEL PRECIO (creador A, escrita antes de tocar codigo): el sufijo no anade una particion,
    MULTIPLICA EL ESPACIO DE DIRECCIONES DE UNA MISMA CELDA (4 -> 32 subcasillas). La experiencia propia del
    organismo se reparte entre 8 veces mas casillas -> la celda conoce menos combinaciones -> la via lenta
    ABSTIENE mas y releva a la lineal, que lee la familia por los pixeles de forma: eso sube la base (CORTADO
    0 -> 4-6) y, con ella, BAR-T. El coste no es de referencia: es de DENSIDAD.

LA IDEA (una sola, y es de aritmetica de particiones):
  Con 4 casillas por par, UNA celda parte los 32 estimulos en <= 4 clases. Tres celdas de FORMA dan como mucho
  4^3 clases, pero su interseccion NO puede bajar de la FAMILIA (el token y sus 3 variantes caen siempre juntos:
  `piso_forma` = 4 de 32, medido en el bloque 5/6 sin simular). Para bajar de 4 hace falta una particion que vea
  la variante. Hay DOS maneras de conseguirla:
    (i)  afinar la direccion DENTRO de la celda (el sufijo del bloque 6): 4 -> 32 casillas, densidad / 8;
    (ii) MULTIPLICAR DOS PARTICIONES DENSAS: una ganadora de FORMA (par de dos px de forma) y una ganadora de
         VARIANTE (par MIXTO: un px de forma y uno de variante), cada una con sus 4 casillas intactas, y una
         lectura que exige a las dos a la vez. 4 x 4 = hasta 16 clases sin que ninguna casilla se vacie.
  (ii) es lo que hace este instrumento. La resolucion se multiplica; la densidad NO se divide.

POR QUE LA LECTURA ES UN PROMEDIO ENTRE TIPOS Y UNA SUMA DENTRO DEL TIPO (lo declaro antes de medir):
  - DENTRO de un tipo se SUMA (es la lectura del bloque 5, no se toca): asi una sola ganadora que discrepa
    arrastra el signo, porque el mundo es ASIMETRICO (veneno -3.0 contra comida +1.0). Esa asimetria es la que
    convierte una suma en una CONJUNCION: para morder hacen falta TODAS las casillas de acuerdo; para no morder
    basta una que diga veneno. No hay puerta nueva, ni umbral nuevo, ni supervisor: la conjuncion es del mundo.
  - ENTRE tipos se PROMEDIA (normalizacion): asi el valor que lee la boca sigue en la escala de k = 3 y no en la
    de k = 6. El bloque 5 midio que k = 5 ROMPE EL CUERPO (muertes 199.5 y 152 contra 32-38) -- sumar mas celdas
    es caro. El promedio ponderado deja el coste donde R6 ya lo midio.
  - Si un tipo no conoce ninguna de sus casillas, NO se abstiene la tabla entera: se lee el otro (el denominador
    es la suma de los pesos de los tipos que SI conocen). La abstencion total, y el relevo a la lineal, se
    conservan solo cuando NINGUN tipo conoce nada: exactamente la regla de v15f/b3/b4b/b5.

CUATRO PERILLAS NUEVAS, TODAS INERTES en su valor por defecto:
  `dos_tipos` (0)   : enciende la lectura por DOS TIPOS de ganadora. Con 0, `_tabla_v15f` es la de b6, linea a
                      linea, y ninguna de las lineas nuevas se ejecuta.
  `k_forma` (3)     : cuantas ganadoras de FORMA (pares de dos px de forma) se suman. 3 = el punto del bloque 5.
  `k_var` (3) y `var_cubre` (1): las ganadoras de VARIANTE. Con `var_cubre`=1 se elige LA MEJOR CELDA MIXTA DE
                      CADA PIXEL DE VARIANTE (una por pixel, `fam_nvar` en total): es una regla de COMPETENCIA
                      CON COBERTURA, local y sin rng, que garantiza que dos variantes cualesquiera se separan en
                      al menos una ganadora (dos variantes distintas difieren en al menos un px de variante).
                      Con `var_cubre`=0 se toman las `k_var` mixtas de menor error propio (sin garantia).
  `pesos_tipo` (0) y `eta_w` (0.05): los pesos de los dos tipos se APRENDEN POR CONSECUENCIA con una regla
                      multiplicativa normalizada (media 1, suelo 0.05): w_t <- w_t * exp(-eta_w * |R - S_t|),
                      con S_t lo que ese tipo predijo ANTES de escribir la mordida. Es competencia entre
                      ganadoras de distinto tipo: local, sin gradiente, sin supervisor, sin rng. Con 0 los dos
                      pesos valen 1 y la lectura es el promedio simple.

QUE NO SE TOCA (ni una linea): el emisor, el canal, el mundo, la escritura (las 66 celdas siguen escribiendo R
  CRUDO por sobrescritura en SU direccion), `_dir_var` (la direccion del bloque 6), la ganadora `_MGv` y su
  desempate al azar, el error propio `_MEv`, la boca, la via rapida, la plasticidad y EL CONSUMO DEL RNG.
  Solo cambia QUE CELDAS LEE LA BOCA y COMO SE COMBINAN.

LAS CELDAS PURAS DE VARIANTE (los 3 pares variante-variante) QUEDAN FUERA DE LOS DOS TIPOS, y lo declaro antes:
  una celda que solo ve px de variante es CIEGA A LA FAMILIA, asi que su casilla guarda la ultima recompensa de
  CUALQUIER token de esa variante (casi siempre comida, porque el organismo muerde lo que come): no puede vetar
  nada y ensuciaria el tipo. El tipo VARIANTE son las celdas MIXTAS (un px de forma + un px de variante), que
  dicen "esta familia Y esta variante" en una sola casilla de 2 bits.

ANCLA DE IDENTIDAD (regla 2 de EQUIPO.md), lo que comprueba identidad_familias_a1.py:
  (a) con dos_tipos=0 -> organismo_familias_b6 BIT A BIT para cualquier `k_ganadoras` y cualquier
      `memoria_variante`, y el rng NO se consume de mas; por la cadena de b6: b5, b4b, b4, b3, b2,
      organismo_familias, organismo_v14 (TRONCO) y organismo_v15f_on;
  (b) con memoria_pares=None la perilla es INERTE (no hay tabla que leer);
  (c) los dos tipos son la particion declarada de las 66 celdas (36 forma + 27 mixtas + 3 puras fuera), y las
      ganadoras de variante cubren un pixel de variante cada una;
  (d) controles que DEBEN fallar (dos_tipos=1 cambia la corrida; el mensaje de la hermana y el de otro token no
      alcanzan la direccion conjunta del referente).

Uso:  python experimentos/junta_fase5/A/construye_familias_a1.py     (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')

SHA_B6 = 'b10cbd4ddd0c32a3'            # organismo_familias_b6.py (bloque 6, identidad 59/59)
SHA_B5 = 'e0b6b90f6f92d5c1'
SHA_B4B = 'b3dd1d7e66a2d147'
SHA_V14 = 'feefc88b1fd8d434'
SHA_V15F_ON = '54d6efe0b564113c'
SHA_ESCALA = 'd8b8566bca77a0ae'
DESTINO = os.path.join(AQUI, 'organismo_familias_a1.py')


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


# ---------------------------------------------------------------- anclas en organismo_familias_b6.py
A_FIRMA = ",k_ganadoras=1,memoria_variante=0):"
A_TABLA = ("    _MMv=np.zeros((_NP,_NCv)); _MNv=np.zeros((_NP,_NCv)); _MEv=np.full(_NP,1e9); _MGv=0   "
           "# v15f: R CRUDO por casilla, visitas, error propio por celda, ganadora. B6: `casilla` = DIRECCION "
           "LOCAL (bin del par [, firma de variante]); con memoria_variante=0, _NCv=4 -> b5 EXACTO\n")
A_TOPK = "        return [_MGv]+_rs[:k_ganadoras-1]\n"
A_TABLAV = "    def _tabla_v15f(P):"
A_INIT = "_c4mbk=None; _c4mdk=None   # B6:"
A_MDK = ("            _c4mdk=sorted(_n6 for _n6 in PAT if all(_dir_var(_g6,PAT[_n6])==_dir_var(_g6,_P4) "
         "for _g6 in _topk_b5()))   # B6: DIAGNOSTICO -- cuantos de los 32 estimulos caen en LAS k DIRECCIONES "
         "del mensaje (con memoria_variante=0 es exactamente _c4mbk)\n")
A_ESCRIBE = "                            _Pv=PAT[kk]\n"
A_RET = "    return dict(memoria_variante=int(memoria_variante),"
# el bloque del MENSAJE (indentacion 24; el de la MORDIDA tiene 32 y no se toca)
A_MSG_ERR = ("\n                        _MEv[_cv]=(_erv*_erv) if _prv else (1-mem_rho)*_MEv[_cv]+mem_rho*(_erv*_erv)"
             "   # error propio de la celda (EMA)\n")
A_MSG_GAN = ("\n                    _mnv=float(_MEv.min()); _empv=[int(_x) for _x in np.where(_MEv<=_mnv+1e-12)[0]]\n"
             "                    _MGv=_empv[0] if len(_empv)==1 else int(_empv[int(rng.integers(len(_empv)))])"
             "   # desempate al azar con el rng del organismo; solo consume rng si HAY empate\n")

NUEVO_CHK = (
    '    if (not isinstance(dos_tipos,int)) or isinstance(dos_tipos,bool) or dos_tipos not in (0,1): raise ValueError(f"dos_tipos={dos_tipos!r}: se espera 0 o 1")   # A1: perilla mal escrita no cae en silencio\n'
    '    if (not isinstance(pesos_tipo,int)) or isinstance(pesos_tipo,bool) or pesos_tipo not in (0,1): raise ValueError(f"pesos_tipo={pesos_tipo!r}: se espera 0 o 1")   # A1\n'
    '    if (not isinstance(var_cubre,int)) or isinstance(var_cubre,bool) or var_cubre not in (0,1): raise ValueError(f"var_cubre={var_cubre!r}: se espera 0 o 1")   # A1\n'
    '    if (not isinstance(k_forma,int)) or isinstance(k_forma,bool) or k_forma<1: raise ValueError(f"k_forma={k_forma!r}: entero >= 1")   # A1\n'
    '    if (not isinstance(k_var,int)) or isinstance(k_var,bool) or k_var<1: raise ValueError(f"k_var={k_var!r}: entero >= 1")   # A1\n'
    '    if float(eta_w)<0: raise ValueError(f"eta_w={eta_w!r}: >= 0")   # A1\n'
    '    if combina not in ("media","min"): raise ValueError(f"combina={combina!r}: se espera \'media\' o \'min\'")   # A1\n'
    '    if (not isinstance(msg_elige,int)) or isinstance(msg_elige,bool) or msg_elige not in (0,1): raise ValueError(f"msg_elige={msg_elige!r}: se espera 0 o 1")   # A1\n'
    "    _CMv=int(combina=='min')   # A1: lectura PESIMISTA entre tipos (el minimo de las dos filas: la regla CUELLO_MIN ya declarada en el mundo vivo) o promedio ponderado\n"
    '    if dentro not in ("suma","min"): raise ValueError(f"dentro={dentro!r}: se espera \'suma\' o \'min\'")   # A1\n'
    "    _DMv=int(dentro=='min')   # A1: DENTRO del tipo, suma (b5) o MINIMO escalado (pesimista). Con todas las casillas de acuerdo los dos dan LO MISMO: solo difieren cuando las ganadoras discrepan, y ahi el pesimista NO muerde\n"
    '    if (not isinstance(exige_dir,int)) or isinstance(exige_dir,bool) or exige_dir not in (0,1): raise ValueError(f"exige_dir={exige_dir!r}: se espera 0 o 1")   # A1\n'
    "    _EDv=int(exige_dir)   # A1: DIRECCION COMPLETA -- una casilla que la celda NO conoce no es 'no opino', es 'no me consta': la tabla calla y releva a la lineal\n"
    "    _DTv=int(dos_tipos); _PTv=int(pesos_tipo); _NVA=int(fam_nvar); _WMIN=0.05   # A1: DOS TIPOS DE GANADORA. Con _DTv=0 ninguna linea nueva se ejecuta -> b6 BIT A BIT\n"
    "    _FRM=[_x1 for _x1 in range(_NP) if max(_PARv[_x1])<_D-_NVA]   # A1: tipo FORMA = pares de dos px de forma (36 con _D=12, fam_nvar=3)\n"
    "    _VMX=[_x1 for _x1 in range(_NP) if min(_PARv[_x1])<_D-_NVA<=max(_PARv[_x1])]   # A1: tipo VARIANTE = pares MIXTOS (un px de forma + uno de variante; 27). Los 3 pares variante-variante quedan FUERA: son ciegos a la familia (ver construye_familias_a1.py)\n"
    "    _wF=1.0; _wV=1.0   # A1: pesos de los dos tipos (media 1). Sin `pesos_tipo` no se mueven nunca\n"
    '    if _DTv and not (1<=_NVA<_D and _FRM and _VMX): raise ValueError(f"dos_tipos=1 con _D={_D} y fam_nvar={fam_nvar!r}: los dos tipos tienen que existir (forma {len(_FRM)}, mixtas {len(_VMX)})")   # A1\n')

NUEVO_TIPOS = (
    "    def _topk_tipo():   # A1: las ganadoras de CADA TIPO, por error propio, DETERMINISTAS (sin rng; el desempate es por indice). FORMA: las `k_forma` mejores de dos px de forma. VARIANTE: con `var_cubre`, LA MEJOR MIXTA DE CADA PIXEL DE VARIANTE (competencia con cobertura: dos variantes distintas difieren en >= 1 px de variante, luego siempre hay una ganadora que las separa); sin el, las `k_var` mejores mixtas.\n"
    "        _f7=sorted(_FRM,key=lambda _x7:(float(_MEv[_x7]),_x7))[:k_forma]\n"
    "        if var_cubre:\n"
    "            _v7=[]\n"
    "            for _q7 in range(_D-_NVA,_D):\n"
    "                _cs7=[_x7 for _x7 in _VMX if _q7 in _PARv[_x7]]\n"
    "                if _cs7: _v7.append(min(_cs7,key=lambda _x7:(float(_MEv[_x7]),_x7)))\n"
    "        else: _v7=sorted(_VMX,key=lambda _x7:(float(_MEv[_x7]),_x7))[:k_var]\n"
    "        return _f7,_v7\n"
    "    def _suma_tipo(_gs,P):   # A1: la SUMA de las casillas CONOCIDAS de un tipo y cuantas conoce (la lectura de b5, restringida al tipo)\n"
    "        _s7=0.0; _n7=0\n"
    "        for _g7 in _gs:\n"
    "            _c7=_dir_var(_g7,P)\n"
    "            if _MNv[_g7,_c7]>0: _s7+=float(_MMv[_g7,_c7]); _n7+=1\n"
    "        return _s7,_n7\n"
    "    def _tabla_dos(P):   # A1: SUMA dentro del tipo (el veneno -3 veta: la conjuncion la pone el mundo) y PROMEDIO PONDERADO entre tipos (normalizacion: el valor sigue en la escala de k = 3, no en la de k = 6). Abstiene -- y releva a la lineal -- solo si NINGUN tipo conoce ninguna casilla, igual que v15f/b5.\n"
    "        _f7,_v7=_topk_tipo(); _sf7,_nf7=_suma_tipo(_f7,P); _sv7,_nv7=_suma_tipo(_v7,P)\n"
    "        if _EDv and (_nf7<len(_f7) or _nv7<len(_v7)): return (0.0, False)   # A1 `exige_dir`: si alguna ganadora NO conoce su casilla para este patron, la tabla NO habla (releva a la lineal). Sin esta regla, la casilla que no se conoce desaparece de la suma y el mensaje de la hermana se cuela por el tipo que no puede saber.\n"
    "        if not _nf7 and not _nv7: return (0.0, False)\n"
    "        if not _nf7: return (_sv7, True)\n"
    "        if not _nv7: return (_sf7, True)\n"
    "        if _CMv: return (min(_sf7,_sv7), True)   # A1 `combina='min'`: CONJUNCION EXPLICITA -- para morder tienen que estar de acuerdo LOS DOS tipos; para no morder basta uno que diga veneno (lectura pesimista, CUELLO_MIN)\n"
    "        return ((_wF*_sf7+_wV*_sv7)/(_wF+_wV), True)\n")

NUEVO_LEE = ("        if _DTv: return _tabla_dos(P)   # A1: DOS TIPOS DE GANADORA (con dos_tipos=0 esta linea no hace nada y lo de abajo es b6 literal)\n")

NUEVO_PESOS = (
    "                            if _DTv and _PTv:   # A1: PESOS POR TIPO, competencia multiplicativa POR CONSECUENCIA y normalizada (media 1, suelo 0.05). Se mide lo que cada tipo predijo ANTES de escribir esta mordida; el mensaje NO mueve los pesos (es exposicion sin consecuencia). Local: solo R y las casillas propias; sin gradiente, sin supervisor y sin azar.\n"
    "                                _ft8,_vt8=_topk_tipo(); _sf8,_nf8=_suma_tipo(_ft8,_Pv); _sv8,_nv8=_suma_tipo(_vt8,_Pv)\n"
    "                                if _nf8 and _nv8:\n"
    "                                    _wF=max(_wF*float(np.exp(-eta_w*abs(R-_sf8))),_WMIN); _wV=max(_wV*float(np.exp(-eta_w*abs(R-_sv8))),_WMIN)\n"
    "                                    _zw8=(_wF+_wV)/2.0; _wF=_wF/_zw8; _wV=_wV/_zw8\n")

NUEVO_MDK = (
    "            _c4gt=([[list(_PARv[_g8]) for _g8 in _topk_tipo()[0]],[list(_PARv[_g8]) for _g8 in _topk_tipo()[1]]] if _DTv else None)   # A1: las ganadoras de cada tipo EN EL PASO DE LA ENTREGA (las del final de la corrida pueden ser otras: la eleccion sigue viva)\n"
    "            _c4dt=(sorted(_n8 for _n8 in PAT if all(_dir_var(_g8,PAT[_n8])==_dir_var(_g8,_P4) for _g8 in (_topk_tipo()[0]+_topk_tipo()[1]))) if _DTv else None)   # A1: DIAGNOSTICO -- cuantos de los 32 estimulos comparten TODAS las direcciones de LOS DOS TIPOS con el mensaje (la resolucion observada, no prometida)\n")

CABECERA = '''"""organismo_familias_a1 = organismo_familias_b6.py (bloque 6, `memoria_variante`, b10cbd4ddd0c32a3)
+ LA LECTURA POR DOS TIPOS DE GANADORA del CREADOR A de la junta de la fase 5, inerte por defecto:
  `dos_tipos` (0): la boca lee DOS ganadoras de distinto tipo -- una de FORMA (par de dos px de forma, familia)
               y otra de VARIANTE (par MIXTO: un px de forma + uno de variante) -- cada una con sus 4 casillas
               INTACTAS. Dentro del tipo se SUMA (la lectura de b5: con veneno -3 y comida +1 una sola casilla
               que discrepa veta, y la conjuncion la pone el mundo, no una puerta nueva); entre tipos se
               PROMEDIA con pesos (normalizacion: el valor se queda en la escala de k = 3). La resolucion se
               MULTIPLICA (4 x 4) sin que ninguna casilla se vacie: es la alternativa densa al sufijo del
               bloque 6, que multiplicaba las subcasillas de UNA celda (4 -> 32) y dividia la densidad por 8.
  `k_forma` (3), `k_var` (3), `var_cubre` (1): cuantas y cuales ganadoras por tipo. Con `var_cubre` la mejor
               mixta DE CADA PIXEL DE VARIANTE (competencia con cobertura, deterministica, sin rng).
  `pesos_tipo` (0), `eta_w` (0.05): los pesos de los dos tipos aprendidos POR CONSECUENCIA con una regla
               multiplicativa normalizada w <- w*exp(-eta_w*|R - S_tipo|) (media 1, suelo 0.05).
  `combina` ('media'): como se combinan los dos tipos. 'media' = promedio ponderado; 'min' = LECTURA PESIMISTA
               (el minimo de las dos filas, la regla CUELLO_MIN ya declarada en el mundo vivo): para morder
               tienen que estar de acuerdo LOS DOS tipos, para no morder basta uno. Es LA CONJUNCION
               "familia Y variante", escrita como una sola operacion local.
  `dentro` ('suma'): como se combinan las ganadoras DE UN MISMO tipo. 'suma' = la lectura del bloque 5.
               'min' = el minimo de sus casillas escalado por cuantas son: identico a la suma cuando todas
               dicen lo mismo, y PESIMISTA cuando discrepan (una casilla que dice veneno basta para no morder).
               Arregla la ESCALA: con la suma, dos casillas que dicen comida y una que dice veneno dan -1, y -1
               no frena a una boca hambrienta (hace falta < -2.1); con el minimo dan -9, que si frena.
  `exige_dir` (0): con 1 la tabla solo habla de un patron si TODAS las ganadoras de LOS DOS tipos conocen
               su casilla para el; si alguna no la conoce, calla y releva a la lineal. Una casilla desconocida
               NO es "no opino": es "no me consta" -- y por ahi se colaba el mensaje de la hermana (medido).
  `msg_elige` (1): con 0, el mensaje ESCRIBE en la tabla (eso no se toca) pero NO actualiza el error propio de
               las celdas ni re-elige la ganadora: una exposicion SIN CONSECUENCIA no es evidencia sobre que
               celda predice mejor las consecuencias. Con 1 es b6, caracter a caracter.
NO cambian el emisor, el canal, el mundo, la ESCRITURA, `_dir_var`, `_MGv` ni su desempate, `_MEv`, la boca ni
el consumo del rng: solo QUE CELDAS LEE la boca y COMO SE COMBINAN.
ANCLA DE IDENTIDAD: con dos_tipos=0 es organismo_familias_b6 BIT A BIT para cualquier `k_ganadoras` y cualquier
`memoria_variante` y, por su cadena, b5, b4b, b4, b3, b2, organismo_familias, organismo_v14 (TRONCO) y
organismo_v15f_on.
Arnes: identidad_familias_a1.py.  Generado por construye_familias_a1.py. NO editar a mano."""
'''


def main():
    for p, sha in [(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                   (os.path.join(N12, 'organismo_familias_b4b.py'), SHA_B4B),
                   (os.path.join(N12, 'organismo_familias_b5.py'), SHA_B5),
                   (os.path.join(N12, 'escala_codigo.py'), SHA_ESCALA),
                   (os.path.join(CREA, 'organismo_v15f_on.py'), SHA_V15F_ON)]:
        if h16(p) != sha:
            raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado.")

    t0 = origen(os.path.join(N12, 'organismo_familias_b6.py'), SHA_B6)
    t = CABECERA + t0

    # ---- 1. firma de run: las perillas nuevas, al final
    t = sust(t, A_FIRMA, A_FIRMA[:-2] + ",dos_tipos=0,k_forma=3,k_var=3,var_cubre=1,pesos_tipo=0,eta_w=0.05,"
                                        "combina='media',msg_elige=1,exige_dir=0,dentro='suma'):", etiqueta='firma de run')
    # ---- 2. validacion, los DOS TIPOS (particion de las celdas) y los pesos, justo despues de la tabla
    t = sust(t, A_TABLA, A_TABLA + NUEVO_CHK, etiqueta='validacion y tipos')
    # ---- 3. las TRES funciones nuevas (eleccion por tipo, suma por tipo, lectura combinada)
    t = sust(t, A_TOPK, A_TOPK + NUEVO_TIPOS, etiqueta='funciones de los dos tipos')
    # ---- 4. LA LECTURA: una linea al principio de _tabla_v15f
    i = t.index(A_TABLAV); j = t.index('\n', i) + 1
    t = t[:j] + NUEVO_LEE + t[j:]
    # ---- 5. los PESOS por consecuencia (solo en la mordida; el mensaje no los mueve)
    t = sust(t, A_ESCRIBE, A_ESCRIBE + NUEVO_PESOS, etiqueta='pesos por consecuencia')
    # ---- 6. `msg_elige`: el MENSAJE escribe (eso no se toca) pero puede NO re-elegir la ganadora. Un mensaje es
    #         una EXPOSICION SIN CONSECUENCIA: no es evidencia sobre que celda predice mejor las consecuencias.
    #         Con msg_elige=1 (default) la linea es la de b6, caracter a caracter.
    t = sust(t, A_MSG_ERR, "\n                        " +
             "if msg_elige: " + A_MSG_ERR.strip() + "   # A1 `msg_elige`: con 0 el mensaje NO cuenta como error "
             "propio de la celda (es exposicion SIN consecuencia)\n", etiqueta='error propio por el mensaje')
    t = sust(t, A_MSG_GAN,
             "\n                    if msg_elige:   # A1 `msg_elige`: con 0 el mensaje NO re-elige la ganadora\n"
             "                        _mnv=float(_MEv.min()); _empv=[int(_x) for _x in np.where(_MEv<=_mnv+1e-12)[0]]\n"
             "                        _MGv=_empv[0] if len(_empv)==1 else int(_empv[int(rng.integers(len(_empv)))])"
             "   # desempate al azar con el rng del organismo; solo consume rng si HAY empate\n",
             etiqueta='re-eleccion de la ganadora por el mensaje')
    # ---- 7. diagnostico: quien comparte TODAS las direcciones de los dos tipos
    t = sust(t, A_INIT, "_c4mbk=None; _c4mdk=None; _c4dt=None; _c4gt=None   # A1: `_c4dt` = quien comparte TODAS las "
                        "direcciones de LOS DOS TIPOS.  # B6:", etiqueta='estado del diagnostico conjunto')
    t = sust(t, A_MDK, A_MDK + NUEVO_MDK, etiqueta='diagnostico conjunto')
    # ---- 8. claves de salida
    t = sust(t, A_RET, "    return dict(dos_tipos=int(dos_tipos),k_forma=int(k_forma),k_var=int(k_var),"
                       "var_cubre=int(var_cubre),pesos_tipo=int(pesos_tipo),eta_w=float(eta_w),"
                       "combina=str(combina),msg_elige=int(msg_elige),exige_dir=int(exige_dir),dentro=str(dentro),"
                       "n_forma=len(_FRM),n_mixtas=len(_VMX),"
                       "tipo_gan_forma=([list(_PARv[_g9]) for _g9 in _topk_tipo()[0]] if _DTv else None),"
                       "tipo_gan_var=([list(_PARv[_g9]) for _g9 in _topk_tipo()[1]] if _DTv else None),"
                       "w_forma=round(float(_wF),4),w_variante=round(float(_wV),4),canal_mismo_dos=_c4dt,canal_gan_tipo=_c4gt,"
                       "memoria_variante=int(memoria_variante),", etiqueta='diccionario de salida')

    if t.count('def _tabla_dos') != 1 or t.count('def _topk_tipo') != 1 or t.count('def _suma_tipo') != 1:
        raise SystemExit("POSTCONDICION: las funciones nuevas no quedaron definidas exactamente una vez. Abortado.")
    if t.count('if _DTv: return _tabla_dos(P)') != 1:
        raise SystemExit("POSTCONDICION: la lectura nueva no entra exactamente una vez. Abortado.")
    if t.count('_dv=_dir_var(_cv,_Pv)') != 2:
        raise SystemExit("POSTCONDICION: la ESCRITURA se toco (tiene que ser la de b6, intacta). Abortado.")
    if t.count('rng.') != t0.count('rng.'):
        raise SystemExit(f"POSTCONDICION: el uso del rng cambio respecto de b6 ({t.count('rng.')} contra "
                         f"{t0.count('rng.')}). Abortado.")
    if t.count('_MGv=_empv[0] if len(_empv)==1 else int(_empv[int(rng.integers(len(_empv)))])') != 2:
        raise SystemExit("POSTCONDICION: la ganadora `_MGv` de b5/b6 y su desempate ya no estan intactos. Abortado.")
    compile(t, DESTINO, 'exec')
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print("  ANCLAS sobre organismo_familias_b6.py  OK: 8 (1 firma, 1 validacion+tipos, 1 funciones, 1 lectura, "
          "1 pesos, 2 diagnostico, 1 salida)")
    print(f"  escrito {os.path.relpath(DESTINO, RAIZ)}")
    print(f"  sha origen  organismo_familias_b6.py {SHA_B6}")
    print(f"  sha destino organismo_familias_a1.py {h16(DESTINO)}")
    print("  ahora: python experimentos/junta_fase5/A/identidad_familias_a1.py")


if __name__ == '__main__':
    main()
