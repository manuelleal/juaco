"""Construye experimentos/nivel12_mundo_familias/organismo_familias_b5.py POR ANCLAS, sobre
organismo_familias_b4b.py (bloque 4b, b3dd1d7e66a2d147; aqui SOLO SE LEE).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive y se COMUNICA con REFERENCIA. Hoy: que el mensaje
BAJE de la familia a la variante.

E-7 / H-4 (registro/investigacion/sala4_evolucion/SALA4_evolucion_20260918.md): la via lenta de v15f lee por UNA
celda ganadora = UN par de pixeles = 2 BITS, y con 32 estimulos esa casilla agrupa 12 de ellos (mediana medida en
las series 641-660 y 661-680). Consecuencia medida: el mensaje con el patron de OTRO token arrastra la mitad del
efecto (BAR-T- 9/18 y 6/19 contra CORTADO- 2/18 y 0/19) y con una hermana casi todo (BAR-H- 15/18 y 13/19). Por
eso el bloque 4b no pudo declarar "comunicacion con referencia".

UNA PERILLA NUEVA, INERTE en su valor por defecto:

  `k_ganadoras` (default 1) -- cuantas celdas LEE la via lenta. La lectura de la tabla pasa de UNA casilla a la
                             SUMA de las casillas CONOCIDAS de las k celdas de menor error propio; si NINGUNA de
                             las k conoce la combinacion, la via lenta ABSTIENE y releva a la lineal, exactamente
                             como en v15f/b3/b4/b4b. LA ESCRITURA NO SE TOCA: las _NP celdas siguen escribiendo R
                             CRUDO por sobrescritura y el error propio por celda es el mismo. El canal tampoco se
                             toca.
                             ORDEN de las k: la PRIMERA es `_MGv`, la ganadora de b4b, calculada con la MISMA
                             linea y el MISMO desempate al azar (por eso el consumo del rng no cambia); las k-1
                             restantes salen de ordenar el resto por (error propio, indice) -- desempate
                             DETERMINISTA por indice, declarado aqui, que no toca el rng.
                             Con k_ganadoras=1 el cuerpo de `_tabla_v15f` es LITERALMENTE el de b4b (las mismas
                             tres lineas) -> organismo_familias_b4b BIT A BIT.

POR QUE SUMA Y NO VOTO (decision escrita ANTES de medir, PREREGISTRO_bloque5_ganadoras.md 3.2):
  1. La tabla guarda R CRUDO: ese es el punto de v15f (la boca lee el valor real, no un signo). Un voto tendria
     que INVENTAR una magnitud; la suma conserva la unidad de R.
  2. La boca ya satura: Vb = alpha*w + hambre_boca*hambre + .5 + voraz con alpha=1.2 y pb = sigmoide(Vb/0.3). Con
     w = +1 y hambre = 0, Vb/0.3 = 5.67 -> pb = 0.997; con w = -3, Vb/0.3 = -10.3 -> pb = 0.00003. O sea: cuando
     las k celdas COINCIDEN, multiplicar por k no cambia la decision. La suma solo actua donde hace falta: en el
     caso MIXTO, que es exactamente el que discrimina.
  3. En el caso mixto la suma usa la asimetria del mundo (comida +1, veneno -3): una sola celda que SI distingue
     cancela tres que no. Un mensaje que solo llega a medias NO hace comer. Es el sesgo conservador que se quiere.
  4. La suma no necesita desempate -> no consume rng -> la identidad con k=1 es limpia.

LA ALTERNATIVA QUE SE DESCARTA (compuerta contra la lineal: leer la tabla solo si su error propio < el de la
lineal), por escrito y antes de medir:
  (a) Pide ESTADO NUEVO (una EMA del error propio de la lectura lineal) y una constante nueva: mas maquinaria que
      la perilla que se elige, contra Occam.
  (b) NO ataca E-7. La compuerta decide SI se lee la tabla, no QUE resuelve la tabla. La fuga de BAR-T ocurre
      DENTRO de la casilla ganadora (el patron de otro token cae en la misma casilla que el referente): una
      compuerta que deja hablar a la tabla no distingue T de X. No puede mover BAR-T ni un punto.
  (c) k=1 es gratis como control de Occam (es b4b bit a bit); la compuerta no tiene ese control gratis.
  Queda anotada como candidata para otro cuello (cuando la tabla habla de lo que no sabe), no para este.

ANCLA DE IDENTIDAD (regla 2 de EQUIPO.md), lo que comprueba identidad_familias_b5.py:
  (a) con k_ganadoras=1 -> organismo_familias_b4b BIT A BIT en TODAS sus claves, y el rng NO se consume; por la
      cadena de b4b, tambien b4, b3, b2, organismo_familias, organismo_v14 (TRONCO) y organismo_v15f_on;
  (b) con memoria_pares=None la perilla es INERTE para cualquier k (no hay tabla que leer);
  (c) la primera de las k ganadoras ES la ganadora de b4b, para cualquier k;
  (d) controles que DEBEN fallar (k=3 y k=5 cambian la corrida).

Uso:  python experimentos/nivel12_mundo_familias/construye_familias_b5.py     (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

SHA_B4B = 'b3dd1d7e66a2d147'          # organismo_familias_b4b.py (bloque 4b, identidad 95/95)
SHA_B4 = 'ff9946ee2ffe27e6'
SHA_B3 = '62a1e53b452b078e'
SHA_B2 = '30200bea6a41c3c8'
SHA_MF = 'b9dd561a0cf056b8'
SHA_V14 = 'feefc88b1fd8d434'
SHA_V15F_ON = '54d6efe0b564113c'
SHA_ESCALA = 'd8b8566bca77a0ae'
DESTINO = os.path.join(AQUI, 'organismo_familias_b5.py')


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


# ---------------------------------------------------------------- anclas en organismo_familias_b4b.py
A_FIRMA = ",voraz=0.0,par_herm=None):"
A_CHK = ('    if memoria_pares not in (None,\'relevo\'): raise ValueError(f"memoria_pares={memoria_pares!r}")'
         '   # v15f: perilla mal escrita no cae en silencio\n')
A_TABLA = ("    def _tabla_v15f(P):   # v15f: (valor, visto) de la casilla de la celda ganadora\n"
           "        _i,_j=_PARv[_MGv]; _c=int(P[_i])*2+int(P[_j])\n"
           "        return (float(_MMv[_MGv,_c]), True) if _MNv[_MGv,_c]>0 else (0.0, False)\n")
A_INIT = ("    _c4p=_c4rx; _c4te=None; _c4gp=None; _c4gq=None; _c4bn=None; _c4mb=None; "
          "_c4em=({} if _c4m=='emite' else None); _nmt=0; _nm4e=0\n")
A_ENTREGA = ("            _c4p=False; _c4te=t; _nm4e=_nmt; _c4gp=list(_PARv[_MGv]); _c4bn=_bin4(_MGv,_P4)\n")
A_GQ = "            _c4gq=list(_PARv[_MGv])\n"
A_RET = "    return dict(voraz=float(voraz),par_herm="

# el bloque nuevo de lectura. El camino k<=1 son LAS MISMAS TRES LINEAS de b4b: identidad por construccion.
NUEVO_TABLA = (
    "    def _topk_b5():   # B5: las k celdas que LEE la via lenta. La 1.a es `_MGv`, la ganadora de b4b (misma linea, mismo desempate al azar, mismo consumo de rng); las k-1 restantes por (error propio, indice) -- desempate DETERMINISTA declarado, sin rng. Con k_ganadoras<=1 devuelve [_MGv].\n"
    "        if k_ganadoras<=1: return [_MGv]\n"
    "        _rs=sorted((_x5 for _x5 in range(_NP) if _x5!=_MGv),key=lambda _x5:(float(_MEv[_x5]),_x5))\n"
    "        return [_MGv]+_rs[:k_ganadoras-1]\n"
    "    def _tabla_v15f(P):   # v15f: (valor, visto) de la casilla de la celda ganadora. B5: la SUMA de las casillas CONOCIDAS de las k ganadoras, y ABSTENCION (releva a la lineal) si ninguna conoce la combinacion. LA ESCRITURA NO SE TOCA.\n"
    "        if k_ganadoras<=1:\n"
    "            _i,_j=_PARv[_MGv]; _c=int(P[_i])*2+int(P[_j])\n"
    "            return (float(_MMv[_MGv,_c]), True) if _MNv[_MGv,_c]>0 else (0.0, False)\n"
    "        _sv=0.0; _nv=0\n"
    "        for _g5 in _topk_b5():\n"
    "            _i,_j=_PARv[_g5]; _c=int(P[_i])*2+int(P[_j])\n"
    "            if _MNv[_g5,_c]>0: _sv+=float(_MMv[_g5,_c]); _nv+=1\n"
    "        return (_sv, True) if _nv else (0.0, False)\n")

CABECERA = '''"""organismo_familias_b5 = organismo_familias_b4b.py (bloque 4b, emisor voraz + par_herm, b3dd1d7e66a2d147)
+ UNA PERILLA para el BLOQUE 5 (H-4 de la sala 4, E-7 "el techo de 2 bits"), inerte por defecto:
  `k_ganadoras` (default 1): cuantas celdas LEE la via lenta. La lectura pasa de UNA casilla a la SUMA de las
               casillas CONOCIDAS de las k celdas de menor error propio; si ninguna de las k conoce la
               combinacion, la via lenta ABSTIENE y releva a la lineal (igual que v15f/b3/b4/b4b). La primera de
               las k es `_MGv`, la ganadora de b4b (mismo desempate al azar, mismo consumo de rng); las k-1
               restantes se ordenan por (error propio, indice), desempate DETERMINISTA sin rng.
               LA ESCRITURA NO SE TOCA (las _NP celdas siguen escribiendo R CRUDO por sobrescritura) y EL CANAL
               TAMPOCO. Con puerta != None, la via lenta NO entra en ningun error de aprendizaje (dlt = R - _wf,
               _ds = R - _lbv): `k_ganadoras` cambia LO QUE LEE LA BOCA y nada mas.
ANCLA DE IDENTIDAD: con k_ganadoras=1 es organismo_familias_b4b BIT A BIT (el camino k<=1 son sus mismas tres
lineas) y, por su cadena, b4, b3, b2, organismo_familias, organismo_v14 (TRONCO) y organismo_v15f_on.
Arnes: identidad_familias_b5.py.  Generado por construye_familias_b5.py. NO editar a mano."""
'''


def main():
    for p, sha in [(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                   (os.path.join(AQUI, 'organismo_familias.py'), SHA_MF),
                   (os.path.join(AQUI, 'organismo_familias_b2.py'), SHA_B2),
                   (os.path.join(AQUI, 'organismo_familias_b3.py'), SHA_B3),
                   (os.path.join(AQUI, 'organismo_familias_b4.py'), SHA_B4),
                   (os.path.join(AQUI, 'escala_codigo.py'), SHA_ESCALA),
                   (os.path.join(CREA, 'organismo_v15f_on.py'), SHA_V15F_ON)]:
        if h16(p) != sha:
            raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado.")

    t = origen(os.path.join(AQUI, 'organismo_familias_b4b.py'), SHA_B4B)
    t = CABECERA + t

    # ---- 1. firma de run: la perilla nueva, al final
    t = sust(t, A_FIRMA, A_FIRMA[:-2] + ",k_ganadoras=1):", etiqueta='firma de run')
    # ---- 2. perilla mal escrita no cae en silencio (al lado de la de memoria_pares)
    t = sust(t, A_CHK, A_CHK +
             "    if (not isinstance(k_ganadoras,int)) or isinstance(k_ganadoras,bool) or k_ganadoras<1: raise ValueError(f\"k_ganadoras={k_ganadoras!r}: entero >= 1\")   # B5: perilla mal escrita no cae en silencio\n",
             etiqueta='validacion de k_ganadoras')
    # ---- 3. LA LECTURA: de una casilla a la suma de las k conocidas, con abstencion
    t = sust(t, A_TABLA, NUEVO_TABLA, etiqueta='lectura de la tabla por k ganadoras')
    # ---- 4. diagnosticos del canal por k (observados, no prometidos)
    t = sust(t, A_INIT, A_INIT[:-1] + "; _c4kp=None; _c4kq=None; _c4mbk=None   # B5: las k ganadoras antes y despues del mensaje, y quien comparte LAS k casillas del referente\n",
             etiqueta='estado de los diagnosticos por k')
    t = sust(t, A_ENTREGA, A_ENTREGA +
             "            _c4kp=[list(_PARv[_g5]) for _g5 in _topk_b5()]   # B5: DIAGNOSTICO (no decide ninguna prediccion)\n",
             etiqueta='k ganadoras antes del mensaje')
    t = sust(t, A_GQ, A_GQ +
             "            _c4kq=[list(_PARv[_g5]) for _g5 in _topk_b5()]\n"
             "            _c4mbk=sorted(_n5 for _n5 in PAT if all(_bin4(_g5,PAT[_n5])==_bin4(_g5,_P4) for _g5 in _topk_b5()))   # B5: DIAGNOSTICO -- cuantos de los 32 estimulos caen en LAS k casillas del mensaje (con k=1 es _c4mb recalculado DESPUES de escribir)\n",
             etiqueta='k ganadoras despues del mensaje')
    # ---- 5. claves de salida
    t = sust(t, A_RET, "    return dict(k_ganadoras=int(k_ganadoras),"
                       "mem_ganadoras=([list(_PARv[_g5]) for _g5 in _topk_b5()] if memoria_pares is not None else None),"
                       "canal_gan_k_pre=_c4kp,canal_gan_k_post=_c4kq,canal_mismo_bin_k=_c4mbk,voraz=float(voraz),par_herm=",
             etiqueta='diccionario de salida')

    if t.count('def _tabla_v15f') != 1 or t.count('def _topk_b5') != 1:
        raise SystemExit("ANCLA lectura: quedo mas de una version de la tabla. Abortado.")
    if 'return (float(_MMv[_MGv,_c]), True) if _MNv[_MGv,_c]>0 else (0.0, False)' not in t:
        raise SystemExit("ANCLA lectura: el camino k<=1 ya no es el de b4b. Abortado.")
    compile(t, DESTINO, 'exec')
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print("  ANCLAS sobre organismo_familias_b4b.py  OK: 7 (1 firma, 1 validacion, 1 lectura, 3 diagnostico, 1 salida)")
    print(f"  escrito {os.path.relpath(DESTINO, RAIZ)}")
    print(f"  sha origen  organismo_familias_b4b.py {SHA_B4B}")
    print(f"  sha destino organismo_familias_b5.py  {h16(DESTINO)}")
    print("  ahora: python experimentos/nivel12_mundo_familias/identidad_familias_b5.py")


if __name__ == '__main__':
    main()
