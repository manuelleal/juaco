"""Construye experimentos/junta_fase5/B/organismo_familias_jb.py POR ANCLAS, sobre
experimentos/nivel12_mundo_familias/organismo_familias_b6.py (bloque 6, b10cbd4ddd0c32a3; aqui SOLO SE LEE).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
retropropagacion, que aprende, desaprende, generaliza, sobrevive y SE COMUNICA CON REFERENCIA. Hoy, exactamente:
que el mensaje refiera a la FAMILIA **Y** a la VARIANTE con la MISMA tabla (BAR-T <= 5/20 y PAR >= 15/20 a la vez).

CREADOR B de la junta de la fase 5 (angulo: REPRESENTACION Y COMPUTACION).

----------------------------------------------------------------------------------------------------------------
EL DIAGNOSTICO (de los datos del registro, no de una intuicion)

  BLOQUE 5 (k = 3, sin sufijo):  BAR-T 5/20 y 4/18   PAR 12/20 y 9/18    CORTADO 0/20 y 0/18
  BLOQUE 6 (k = 3, con sufijo):  BAR-T 11/20 y 10/18  PAR 15/20 y 15/18   CORTADO 6/20 y 4/18

  El sufijo de variante en la DIRECCION es correcto: es lo unico que puede separar a las hermanas (difieren solo
  en los pixeles 9-11) y por eso PAR sube. Lo que rompio no fue la direccion: fue **la DENSIDAD de la tabla**.
  Con 4 -> 32 subcasillas por celda, la tabla propia del organismo se vuelve 8x mas dispersa; el propio
  preregistro del bloque 6 lo midio: `mem_cobertura` cae de 3.5/4 (88 %) a ~11/32 (34 %).
  Consecuencia EXACTA, y es de computacion, no de capacidad de bits:

    en b5, cuando el mensaje de OTRO token alcanzaba por azar la casilla de una celda, las OTRAS k-1 celdas
    CONOCIAN su casilla y contestaban con el valor propio (negativo): la suma de las k era un VOTO y la fuga
    quedaba en minoria.  En b6, esas otras celdas ya no conocen su subcasilla: **ABSTIENEN**, aportan 0, y la
    unica celda que se fugo decide sola.  Por eso BAR-T sube de 5 a 11 y la base sin mensaje de 0 a 4-6.

  O sea: no es que no quepan familia y variante en 4 casillas. Es que al afinar la direccion se perdio el
  contexto grueso (la familia) que hacia de CONTRAPESO, y el voto se quedo sin votantes.

LO QUE CAMBIA -- TRES REGLAS DE LECTURA, las tres inertes por defecto, ninguna toca la ESCRITURA

  Se probaron en este orden y se dejan las tres en el instrumento (las dos primeras como CONTROL y como
  consecuencia registrada en BITACORA_CONSECUENCIAS.md; la tercera es el candidato):

  1. `mem_marginal` -- RELEVO MARGINAL (REFUTADA). Si la celda no conoce la subcasilla exacta (bin, firma),
     contesta la marginal de su bin: ponderada por visitas (1), sin ponderar (2) o la moda (3). La idea era
     devolver la densidad: direccion fina = VARIANTE, marginal del bin = FAMILIA, en la misma tabla.
     SE CAYO en el humo: la marginal del bin incluye la subcasilla que el mensaje acaba de SOBRESCRIBIR -- y la
     sobrescritura conserva las visitas, asi que ni ponderar ni la moda la protegen. BAR-H 2/3 y VALOR 1/3.
     La objecion (a) del preregistro del bloque 6 vale tambien cuando el nivel grueso se CALCULA en vez de
     escribirse. Consecuencia registrada.

  2. `mem_canales` / `mem_kvar` -- DOS CANALES CON RELEVO POR CONFLICTO (REFUTADA). k celdas de FORMA (las dos
     coordenadas en 0-8: ciegas a la variante) y mem_kvar celdas que TOCAN 9-11 (su bin de 2 bits YA separa a
     las hermanas), leidas por separado; con 2, si los dos canales se contradicen en signo la via lenta abstiene.
     SE CAYO en el humo: en BAR-H la lectura dio +4.00 con 4/4 celdas exactas -- el canal de variante es ciego a
     la forma y su valor propio para el referente era POSITIVO, asi que no habia contradiccion que detectar.
     LECCION QUE LLEVA A LA TERCERA: lo que discrimina no es el VALOR de la celda, es SI EL MENSAJE ALCANZO SU
     DIRECCION.

  3. `mem_conj` -- LECTURA CONJUNTIVA (EL CANDIDATO). UNA linea:

         if _CJv: return (_sv, True) if _nv==len(_tk) else (0.0, False)

     La via lenta contesta solo si LAS k celdas conocen su direccion exacta; si una no, abstiene y releva a la
     lineal -- el mismo relevo que el organismo ya tiene para "no conozco esta combinacion", aplicado a la tupla
     entera en vez de a cada celda por separado.

POR QUE LA CONJUNCION DA FAMILIA **Y** VARIANTE (el argumento, y el diagnostico que lo mide)

  El mensaje escribe en cada celda g la subcasilla (bin_g(P_msg), firma(P_msg)). La boca lee, para el referente,
  (bin_g(T1v2), firma(v2)) en cada una de las k. Con la DISYUNCION de b5/b6, el mensaje mueve la boca si alcanza
  UNA sola celda -> la referencia es la UNION de las direcciones y por eso arrastra. Con la CONJUNCION, el
  mensaje solo cuenta si alcanzo LAS k -> la referencia es la INTERSECCION:

      interseccion de los bins de forma  = LA FAMILIA (el token y sus 3 variantes)      <- lo que dio k = 3
      interseccion con la firma de 3 px  = LA VARIANTE (los *v2 de los 8 tokens)        <- lo que dio el sufijo
      las dos a la vez                   = 4/32 (familia) INTERSECADO 8/32 (variante)   = 1/32 = EL REFERENTE

  Eso es el codigo factorizado que pedia el encargo, y no hace falta mas tabla: la FORMA ya vive en el bin de
  cada par y la VARIANTE en la firma. La tupla de las k direcciones ES el codigo compuesto; lo que faltaba era
  leerlo como interseccion. Medido en el humo (`canal_lee_post`, en el paso de la entrega, mediana de 3
  semillas, celda k3v1j1): el referente lee +3.00 con 3/3 celdas exactas en CANAL, -9.00 en BAR-H, -1.00 en
  BAR-T, -1.00 en VALOR. El mensaje de la hermana y el de otro token NO alcanzan la direccion del referente.

  El precio, declarado antes de la serie: la via lenta ABSTIENE mas (con la tabla fina, exigir las k exactas es
  exigente) y releva mas a la lineal. Lo vigilan CORTADO, las muertes y okU (R6); en el humo, muertes 17 contra
  11 de b6 y 296 de b5 en las mismas semillas.

LO QUE NO SE TOCA: el mundo, el catalogo, el canal y su letra, el emisor voraz (corre con mem_marginal=0,
  memoria_variante=0, k=1: es b4b bit a bit), la ESCRITURA (mensaje y mordida) y su direccion `_dir_var`, la
  seleccion de la ganadora `_MGv` y su desempate al azar, el error propio `_MEv`, la sobrescritura de R CRUDO,
  la via lineal, la puerta, la boca, el metabolismo y el CONSUMO DEL RNG.  Cambia UNA cosa: que contesta una
  celda cuando no conoce su subcasilla exacta.

ANCLA DE IDENTIDAD (lo que comprueba identidad_familias_jb.py):
  (a) las tres perillas en 0 -> organismo_familias_b6 BIT A BIT, para k = 1 y k = 3, con el sufijo ON y OFF, con
      el canal apagado y en sus tres modos, y a T = 120000 (el rng no se consume); y por la cadena de b6:
      b5, b4b, b4, b3, b2, organismo_familias, organismo_v14 (TRONCO) y organismo_v15f_on;
  (b) memoria_variante=0 -> mem_marginal es INERTE en 1, 2 y 3 (la marginal de un bin de UNA subcasilla es esa
      misma subcasilla): el relevo NO puede tocar ninguna configuracion sin sufijo;
  (c) k_ganadoras=1 -> mem_conj es INERTE (con una sola celda, conjuncion y disyuncion coinciden);
  (d) memoria_pares=None -> las tres inertes (no hay tabla que leer);
  (e) la lectura reimplementada FUERA del organismo == la de dentro, estimulo a estimulo, con las tres reglas
      evaluadas SOBRE LA MISMA TABLA (comparar dos corridas no valdria: divergen en cuanto cambia la conducta);
  (f) controles que DEBEN fallar: con el sufijo ON, cada perilla cambia la corrida, y CANAL != CORTADO,
      != HERMANA y != OTRO TOKEN (sin ellos el arnes pasaria por vacuidad; ERR-64b: >= 2 de 3 semillas).

Uso:  python experimentos/junta_fase5/B/construye_familias_jb.py      (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
ORIGEN = os.path.join(N12, 'organismo_familias_b6.py')
DESTINO = os.path.join(AQUI, 'organismo_familias_jb.py')
SHA_B6 = 'b10cbd4ddd0c32a3'

CABECERA = '''"""organismo_familias_jb = organismo_familias_b6.py (bloque 6, SUFIJO DE VARIANTE, b10cbd4ddd0c32a3)
+ TRES REGLAS DE LECTURA de la junta de la fase 5 (creador B, angulo REPRESENTACION Y COMPUTACION), las tres
inertes por defecto y las tres **solo en la LECTURA** de la via lenta: NI UNA linea de la escritura cambia.

  `mem_conj` (default 0) -- EL CANDIDATO. QUE CUENTA COMO "LA TABLA CONOCE ESTE PATRON".
      0 = la via lenta contesta si ALGUNA de las k celdas conoce su direccion (b6 BIT A BIT: una DISYUNCION).
      1 = contesta solo si LAS k la conocen (una CONJUNCION); si una no, abstiene y releva a la lineal.
      Con 1 la referencia del mensaje pasa a ser la INTERSECCION de las k direcciones. Con el sufijo encendido
      esa interseccion es EL REFERENTE SOLO: la FORMA la lleva el bin de cada par y la VARIANTE la firma, o sea
      que la TUPLA de las k direcciones ya es un codigo factorizado -- faltaba leerlo como interseccion.
      Con k_ganadoras = 1 es inerte (con una sola celda, conjuncion y disyuncion son la misma regla).

  `mem_marginal` (default 0) -- REFUTADA EN EL HUMO, se deja como control y como consecuencia registrada.
      0 = la celda que no conoce su subcasilla ABSTIENE (b6 BIT A BIT).
      1 = contesta la MARGINAL de su bin ponderada por visitas; 2 = sin ponderar; 3 = la MODA del bin.
      POR QUE SE CAYO: la marginal del bin incluye la subcasilla que el mensaje acaba de SOBRESCRIBIR (y la
      sobrescritura conserva las visitas), asi que el mensaje de la hermana vuelve a alcanzar al referente por
      el nivel grueso: BAR-H 2/3 y VALOR 1/3 en el humo, donde b6 da 0/3. Medido, no supuesto.

  `mem_canales` (default 0), `mem_kvar` (default 1) -- REFUTADA EN EL HUMO, se deja como control.
      0 = una sola lista de ganadoras (b6 BIT A BIT). 1 = DOS CANALES leidos aparte -- k_ganadoras celdas de
      FORMA (ciegas a la variante) y mem_kvar celdas que TOCAN los pixeles de variante -- sumados. 2 = los dos
      canales con RELEVO POR CONFLICTO (si se contradicen en signo, la via lenta abstiene).
      POR QUE SE CAYO: el canal de variante es ciego a la forma y su valor propio para el referente resulto
      POSITIVO, asi que no hay contradiccion que detectar (en BAR-H leyo +4.00 con 4/4 celdas exactas). Lo que
      discrimina no es el VALOR de la celda sino SI EL MENSAJE ALCANZO SU DIRECCION.

  DIAGNOSTICOS que anade (observados, no prometidos; no deciden ninguna prediccion y no consumen rng):
      `canal_lee_post` = en el paso de la ENTREGA, que lee la via lenta para cada uno de los 32 estimulos
      ([valor, conocido, cuantas de las k contestan EXACTO, k]); `mem_via`, `mem_visitas`, `mem_dir`, `mem_can`,
      `mem_celdas_can` = lo mismo al final, para reimplementar la lectura FUERA del organismo y compararla.

  DE DONDE SALE TODO ESTO: en b5 las k celdas VOTABAN (las que no se fugaban contestaban su valor propio); el
  sufijo de b6 dejo la tabla 8x mas dispersa (cobertura 88 % -> 34 %), las celdas pasaron a ABSTENER y la unica
  por la que el mensaje se colaba decidia sola -> BAR-T 5 -> 11 y la base sin mensaje 0 -> 4-6.
  NO cambian: el mundo, el canal, el emisor, la ESCRITURA y su direccion `_dir_var`, la ganadora `_MGv` y su
  desempate, el error propio `_MEv`, la sobrescritura de R CRUDO, la lineal, la puerta, la boca, ni el RNG.
ANCLA DE IDENTIDAD: con las tres perillas en 0 es organismo_familias_b6 BIT A BIT (cualquier k, sufijo ON u OFF)
  y, por su cadena, b5, b4b, b4, b3, b2, organismo_familias, organismo_v14 (TRONCO) y organismo_v15f_on.
Arnes: identidad_familias_jb.py.  Generado por construye_familias_jb.py. NO editar a mano."""
'''

# ---------------------------------------------------------------- anclas (texto EXACTO de organismo_familias_b6)
A_FIRMA = ",k_ganadoras=1,memoria_variante=0):"
A_CHK = ("    if (not isinstance(memoria_variante,int)) or isinstance(memoria_variante,bool) or memoria_variante "
         "not in (0,1): raise ValueError(f\"memoria_variante={memoria_variante!r}: se espera 0 o 1\")   "
         "# B6: perilla mal escrita no cae en silencio\n")
NUEVO_CHK = ("    if (not isinstance(mem_marginal,int)) or isinstance(mem_marginal,bool) or mem_marginal not in "
             "(0,1,2,3): raise ValueError(f\"mem_marginal={mem_marginal!r}: se espera 0, 1, 2 o 3\")   "
             "# JB: perilla mal escrita no cae en silencio\n"
             "    _MRv=int(mem_marginal)   # JB: 0 = abstiene (b6 EXACTO); 1 = marginal del bin ponderada por "
             "visitas; 2 = marginal sin ponderar; 3 = la subcasilla MAS VISITADA del bin (la moda)\n"
             "    if (not isinstance(mem_canales,int)) or isinstance(mem_canales,bool) or mem_canales not in "
             "(0,1,2): raise ValueError(f\"mem_canales={mem_canales!r}: se espera 0, 1 o 2\")   "
             "# JB: perilla mal escrita no cae en silencio\n"
             "    if (not isinstance(mem_kvar,int)) or isinstance(mem_kvar,bool) or mem_kvar<1: "
             "raise ValueError(f\"mem_kvar={mem_kvar!r}: entero >= 1\")   # JB\n"
             "    _MCv=int(mem_canales); _KVv=int(mem_kvar)   # JB: 0 = una sola lista de ganadoras (b6 EXACTO); "
             "1 = DOS CANALES (forma y variante) SUMADOS; 2 = dos canales con RELEVO POR CONFLICTO DE SIGNO\n"
             "    if (not isinstance(mem_conj,int)) or isinstance(mem_conj,bool) or mem_conj not in (0,1): "
             "raise ValueError(f\"mem_conj={mem_conj!r}: se espera 0 o 1\")   # JB\n"
             "    _CJv=int(mem_conj)   # JB: 0 = la via lenta contesta si ALGUNA celda conoce su direccion (b6 "
             "EXACTO: una DISYUNCION); 1 = contesta solo si LAS k la conocen (una CONJUNCION: la referencia pasa "
             "a ser la INTERSECCION de las k direcciones, que es lo que hace de la tupla de celdas un codigo)\n")

A_PARV = ("    _PARv=[(i,j) for i in range(_D) for j in range(i+1,_D)]; _NP=len(_PARv)   "
          "# v15f/b3: C(_D,2) celdas = pares de pixeles (con _D=6 son 15: v15f EXACTO)\n")
NUEVO_PARV = (A_PARV +
              "    _FRMv=[_x9 for _x9 in range(_NP) if max(_PARv[_x9])<_D-int(fam_nvar)]   # JB: celdas de FORMA "
              "(las dos coordenadas dentro del bloque de forma): CIEGAS a la variante por construccion -> el "
              "CANAL DE FAMILIA\n"
              "    _VARc=[_x9 for _x9 in range(_NP) if max(_PARv[_x9])>=_D-int(fam_nvar)]   # JB: celdas que "
              "TOCAN la variante: su bin de 2 bits YA separa a las hermanas -> el CANAL DE VARIANTE\n"
              "    if _MCv and (not _FRMv or not _VARc): raise ValueError(f\"mem_canales={mem_canales!r} con "
              "fam_nvar={fam_nvar!r}: uno de los dos canales queda vacio\")   # JB\n")

A_TOPK = "        return [_MGv]+_rs[:k_ganadoras-1]\n"
NUEVO_TOPK = (A_TOPK +
              "    def _topk_can():   # JB: LAS GANADORAS POR CANAL. k_ganadoras celdas de FORMA y mem_kvar celdas "
              "de VARIANTE, cada canal ordenado por SU PROPIO error (mismo criterio de b5, aplicado dentro de cada "
              "canal), desempate DETERMINISTA por indice, sin azar nuevo\n"
              "        return (sorted(_FRMv,key=lambda _x9:(float(_MEv[_x9]),_x9))[:k_ganadoras],\n"
              "                sorted(_VARc,key=lambda _x9:(float(_MEv[_x9]),_x9))[:_KVv])\n"
              "    def _topk_leer():   # JB: las celdas que LEE la boca. Con mem_canales=0 son EXACTAMENTE las de "
              "b5/b6 (`_topk_b5`), y por eso toda la cadena de identidad se mantiene.\n"
              "        if not _MCv: return _topk_b5()\n"
              "        _f9,_v9=_topk_can(); return _f9+_v9\n")

A_LEE = """    def _tabla_v15f(P):   # v15f: (valor, visto) de la casilla de la celda ganadora. B5: la SUMA de las casillas CONOCIDAS de las k ganadoras, y ABSTENCION (releva a la lineal) si ninguna conoce la combinacion. LA ESCRITURA NO SE TOCA.
        if k_ganadoras<=1:
            _c=_dir_var(_MGv,P)   # B6: la DIRECCION (con memoria_variante=0 es el bin literal de b5/b4b)
            return (float(_MMv[_MGv,_c]), True) if _MNv[_MGv,_c]>0 else (0.0, False)
        _sv=0.0; _nv=0
        for _g5 in _topk_b5():
            _c=_dir_var(_g5,P)
            if _MNv[_g5,_c]>0: _sv+=float(_MMv[_g5,_c]); _nv+=1
        return (_sv, True) if _nv else (0.0, False)
"""
NUEVO_LEE = """    def _lee_celda(_g7,_P7):   # JB: LA UNICA FUNCION NUEVA -- que contesta la celda _g7 ante _P7. Con mem_marginal=0 es la linea de b6, caracter a caracter (exacta o abstencion). Con 1/2 releva a la MARGINAL DE SU BIN: la referencia de FAMILIA reconstruida de la propia fila fina. Sin rng, sin estado compartido, sin tocar la escritura.
        _c7=_dir_var(_g7,_P7)
        if _MNv[_g7,_c7]>0: return (float(_MMv[_g7,_c7]), True)   # EXACTA: la subcasilla (bin, firma) = la VARIANTE
        if not _MRv or not _MVv: return (0.0, False)              # b6 EXACTO (y con memoria_variante=0 el relevo es INERTE: el bin tiene una sola subcasilla)
        _b7=_bin4(_g7,_P7); _l7=_b7<<_NV; _h7=_l7+(1<<_NV)        # el BIN del par: las 2^_NV subcasillas que comparten forma y difieren en variante
        _n7=_MNv[_g7,_l7:_h7]; _m7=_MMv[_g7,_l7:_h7]
        if _MRv==2:
            _k7=(_n7>0)
            return (float(_m7[_k7].mean()), True) if bool(_k7.any()) else (0.0, False)   # marginal SIN ponderar (control)
        if _MRv==3:
            _a7=int(_n7.argmax())
            return (float(_m7[_a7]), True) if _n7[_a7]>0 else (0.0, False)   # MODA del bin: la subcasilla mas visitada (un mensaje de UNA visita no puede ser la moda si el bin ya tiene experiencia propia)
        _w7=float(_n7.sum())
        return (float(float((_m7*_n7).sum())/_w7), True) if _w7>0 else (0.0, False)      # MARGINAL ponderada por visitas: el mensaje aporta 1 visita entre las del propio organismo
    def _suma_can(_cs,_P9):   # JB: lo que dice UN CANAL: la suma de sus celdas que contestan, y cuantas contestan
        _s9=0.0; _n9=0
        for _g9 in _cs:
            _v9,_k9=_lee_celda(_g9,_P9)
            if _k9: _s9+=_v9; _n9+=1
        return _s9,_n9
    def _tabla_v15f(P):   # v15f: (valor, visto) de la casilla de la celda ganadora. B5: la SUMA de las casillas CONOCIDAS de las k ganadoras, y ABSTENCION (releva a la lineal) si ninguna conoce la combinacion. LA ESCRITURA NO SE TOCA. JB: `conocer` pasa por `_lee_celda`, y con mem_canales la lectura es de DOS CANALES.
        if _MCv:   # JB: DOS CANALES de la MISMA tabla -- forma (familia) y variante -- leidos por separado
            _f9,_v9=_topk_can()
            _sf,_nf=_suma_can(_f9,P); _sv9,_nv9=_suma_can(_v9,P)
            if not _nf and not _nv9: return (0.0, False)
            if _CJv and (_nf<len(_f9) or _nv9<len(_v9)): return (0.0, False)   # CONJUNCION: las dos listas enteras
            if _MCv==2 and _nf and _nv9 and _sf*_sv9<0: return (0.0, False)   # RELEVO POR CONFLICTO: si los dos canales se CONTRADICEN, la via lenta no contesta y releva a la lineal (el mismo relevo que ya existe para "no lo conozco", extendido a "mis dos canales dicen cosas opuestas"). La referencia exige entonces FAMILIA *Y* VARIANTE a la vez.
            return (_sf+_sv9, True)
        if k_ganadoras<=1:
            return _lee_celda(_MGv,P)
        _tk=_topk_leer(); _sv=0.0; _nv=0
        for _g5 in _tk:
            _v5,_k5=_lee_celda(_g5,P)
            if _k5: _sv+=_v5; _nv+=1
        if _CJv: return (_sv, True) if _nv==len(_tk) else (0.0, False)   # JB: CONJUNCION -- si UNA de las k no conoce su direccion, la via lenta NO contesta y releva a la lineal. Asi la referencia del mensaje es la INTERSECCION de las k direcciones (con sufijo: el referente solo) y no la union de las que se dejaron escribir.
        return (_sv, True) if _nv else (0.0, False)
"""

A_INIT = "_c4mbk=None; _c4mdk=None   #"
NUEVO_INIT = "_c4mbk=None; _c4mdk=None; _c4lp=None   # JB: `_c4lp` = QUE LEE la via lenta en el paso de la entrega.  #"
A_MDK = ("            _c4mdk=sorted(_n6 for _n6 in PAT if all(_dir_var(_g6,PAT[_n6])==_dir_var(_g6,_P4) "
         "for _g6 in _topk_b5()))")
NUEVO_MDK = (A_MDK + "\n            _c4lp={}   # JB: DIAGNOSTICO en el paso de la ENTREGA (justo despues de "
             "escribirse el mensaje): que valor lee la via lenta para CADA estimulo y por que via. Observado, no "
             "prometido: no decide ninguna prediccion, no consume rng y no cambia ninguna decision.\n"
             "            for _n8 in PAT:\n"
             "                _v8,_k8=_tabla_v15f(PAT[_n8])\n"
             "                _e8=int(sum(1 for _g8 in _topk_b5() if _MNv[_g8,_dir_var(_g8,PAT[_n8])]>0))\n"
             "                _c4lp[_n8]=[round(float(_v8),4),bool(_k8),_e8,int(len(_topk_b5()))]   # [valor, "
             "conocido, celdas que contestan EXACTO, k]")

A_RET = "    return dict(memoria_variante=int(memoria_variante),"
NUEVO_RET = ("    return dict(mem_marginal=int(mem_marginal),mem_canales=int(mem_canales),mem_kvar=int(mem_kvar),"
             "mem_conj=int(mem_conj),"
             "canal_lee_post=_c4lp,"
             "mem_can=({_n9:[round(float(_suma_can(_topk_can()[0],PAT[_n9])[0]),4),"
             "int(_suma_can(_topk_can()[0],PAT[_n9])[1]),"
             "round(float(_suma_can(_topk_can()[1],PAT[_n9])[0]),4),"
             "int(_suma_can(_topk_can()[1],PAT[_n9])[1])] for _n9 in PAT} "
             "if (memoria_pares is not None and _MCv) else None),"
             "mem_celdas_can=([[list(_PARv[_g9]) for _g9 in _topk_can()[0]],"
             "[list(_PARv[_g9]) for _g9 in _topk_can()[1]]] if (memoria_pares is not None and _MCv) else None),"
             "mem_via=({_n9:[int(sum(1 for _g9 in _topk_b5() if _MNv[_g9,_dir_var(_g9,PAT[_n9])]>0)),"
             "int(len(_topk_b5()))] for _n9 in PAT} if memoria_pares is not None else None),"
             "mem_visitas=([[int(_x) for _x in _f] for _f in _MNv] if memoria_pares is not None else None),"
             "mem_dir=({_n9:[int(_dir_var(_g9,PAT[_n9])) for _g9 in _topk_b5()] for _n9 in PAT} "
             "if memoria_pares is not None else None),"
             "memoria_variante=int(memoria_variante),")


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(t, viejo, nuevo, n=1, etiqueta=''):
    if t.count(viejo) != n:
        raise SystemExit(f"ANCLA '{etiqueta}': aparece {t.count(viejo)} veces, se esperaba {n}. Abortado.")
    return t.replace(viejo, nuevo)


def main():
    if h16(ORIGEN) != SHA_B6:
        raise SystemExit(f"ORIGEN organismo_familias_b6.py: sha {h16(ORIGEN)}, se esperaba {SHA_B6}. Abortado.")
    t0 = open(ORIGEN, encoding='utf-8').read()
    t = CABECERA + t0

    t = sust(t, A_FIRMA, A_FIRMA[:-2] + ",mem_marginal=0,mem_canales=0,mem_kvar=1,mem_conj=0):", etiqueta='firma de run')
    t = sust(t, A_CHK, A_CHK + NUEVO_CHK, etiqueta='validacion de las perillas')
    t = sust(t, A_PARV, NUEVO_PARV, etiqueta='los dos canales de celdas')
    t = sust(t, A_TOPK, NUEVO_TOPK, etiqueta='ganadoras por canal')
    t = sust(t, A_LEE, NUEVO_LEE, etiqueta='LECTURA (las funciones nuevas)')
    t = sust(t, A_INIT, NUEVO_INIT, etiqueta='estado del diagnostico de lectura')
    t = sust(t, A_MDK, NUEVO_MDK, etiqueta='diagnostico de lectura en la entrega')
    t = sust(t, A_RET, NUEVO_RET, etiqueta='diccionario de salida')
    # los DIAGNOSTICOS pasan a mirar las celdas que la boca LEE de verdad; con las perillas apagadas
    # `_topk_leer()` es `_topk_b5()`, asi que ni un bit cambia (lo comprueba el arnes).
    t = t.replace('_topk_b5()', '_topk_leer()').replace('def _topk_leer():   # B5:', 'def _topk_b5():   # B5:')
    t = t.replace('        if not _MCv: return _topk_leer()\n', '        if not _MCv: return _topk_b5()\n')

    # ---- postcondiciones: lo que NO puede haber cambiado
    if t.count('def _lee_celda') != 1 or t.count('def _topk_leer') != 1 or t.count('def _topk_can') != 1:
        raise SystemExit("POSTCONDICION: las funciones nuevas no quedaron definidas una vez cada una. Abortado.")
    # `_topk_b5()` solo puede aparecer dos veces: su propia definicion y la llamada de dentro de `_topk_leer`
    if t.count('_topk_b5()') != 2 or t.count('def _topk_b5():') != 1 or \
            t.count('if not _MCv: return _topk_b5()') != 1:
        raise SystemExit(f"POSTCONDICION: `_topk_b5()` aparece {t.count('_topk_b5()')} veces; solo su definicion "
                         "y la llamada de `_topk_leer`. Abortado.")
    if t.count('_dv=_dir_var(_cv,_Pv)') != t0.count('_dv=_dir_var(_cv,_Pv)'):
        raise SystemExit("POSTCONDICION: la ESCRITURA cambio. Abortado.")
    if t.count('rng.') != t0.count('rng.'):
        raise SystemExit(f"POSTCONDICION: el uso del rng cambio ({t.count('rng.')} contra {t0.count('rng.')}). "
                         "Abortado.")
    if t.count('_MMv[_cv,_dv]') != t0.count('_MMv[_cv,_dv]') or t.count('_MEv[_cv]') != t0.count('_MEv[_cv]'):
        raise SystemExit("POSTCONDICION: la escritura de R CRUDO o el error propio cambiaron. Abortado.")
    if 'def _dir_var' not in t or 'return int(_P[_i4])*2+int(_P[_j4])' not in t:
        raise SystemExit("POSTCONDICION: la direccion de b6 / el bin de b4b ya no son la base. Abortado.")
    compile(t, DESTINO, 'exec')
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print("  ANCLAS sobre organismo_familias_b6.py  OK: 6 (1 firma, 1 validacion, 1 lectura, 2 diagnostico, 1 salida)")
    print(f"  escrito {os.path.relpath(DESTINO, RAIZ)}")
    print(f"  sha origen  organismo_familias_b6.py {SHA_B6}")
    print(f"  sha destino organismo_familias_jb.py {h16(DESTINO)}")
    print("  ahora: python experimentos/junta_fase5/B/identidad_familias_jb.py")


if __name__ == '__main__':
    main()
