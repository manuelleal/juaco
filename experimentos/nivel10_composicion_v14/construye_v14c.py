"""Construye experimentos/nivel10_composicion_v14/ = COMPOSICION de los DOS candidatos a v14 que quedaron con
evidencia completa y que actuan en sitios distintos del organismo (registro/PROPUESTA_v14.md, registro/REGISTRO_etapas_1_2.md):

  (1) HIJA DISPERSA POR RELEVANCIA (perilla mask_rel)      -> actua en el NACIMIENTO de la hija (division)
      experimentos/nivel7_hija_dispersa/construye_v13D.py (candidato 1; organismo_v13Don = perilla fija ON)
  (2) PUERTA POR EVIDENCIA DEL CODIGO EXACTO (perilla puerta_pat, PATC = codigo AND >=1 celda consolidada)
      -> actua en el RUTEO de la boca (rapida vs lenta), NO en el aprendizaje
      experimentos/nivel4_puerta_codigo/construye_puerta_codigo.py (candidato 3; organismo_v13Bn5c = perilla fija ON)

Todo POR ANCLAS, sin editar ningun original (solo se LEEN, con sha fijado y verificado por origen()):
  - organismo/organismo_v13.py, organismo/bateria_v13.py, organismo/bateria_generaliza.py: CONGELADOS
    (manifiesto.py). experimentos/v13_dos_vias/organismo_v13g.py: instrumento ya corrido (ERR-28: NO es el
    organismo_v13.py ambiguo de esa carpeta -- es organismo_v13g.py, distinto nombre, sha verificado).
  - experimentos/nivel7_hija_dispersa/{construye_v13D.py, mundo_hija_dispersa.py} y
    experimentos/nivel4_puerta_codigo/{construye_puerta_codigo.py, organismo_capB.py}: instrumentos YA CORRIDOS
    (evidencia en el registro). Se LEEN e IMPORTAN (las funciones que aplican el parche), nunca se editan.

Import vs. reproduccion de anclas (lo que pide el brief): las funciones que hacen el parche real, pon_hija()
(mask_rel) y pon_puerta() (puerta_pat), se IMPORTAN sin cambios desde construye_v13D.py y construye_puerta_codigo.py
-- ninguna logica de sustitucion se reescribe a mano. Los LITERALES de texto que ubican DONDE meter cada parche
(las anclas) estan definidos dentro de un `if __name__ == '__main__':` en esos dos scripts y por tanto NO son
importables: se REPRODUCEN aqui, copiados a mano leyendo esos scripts y organismo_v13.py / organismo_v13g.py /
organismo_capB.py / mundo_hija_dispersa.py linea a linea. Cualquier desajuste (frente al tronco o frente a los
propios scripts) lo detecta origen()/sust() y aborta con SystemExit antes de escribir nada -- no hay forma de que
esto produzca una salida silenciosamente incorrecta.

COLISION DECLARADA (la que pide el brief; hay UNA sola real, dos veces -- una por cada archivo que recibe los DOS
parches completos): pon_hija() y pon_puerta() editan la MISMA linea, la ultima linea de argumentos de
organismo_v13/organismo_v13g (todo lo que sigue a "...puerta=3):" o "...sonda_final=False):"). Si se llaman las
dos funciones, sin mas, con la ancla ORIGINAL, la segunda falla: el primer parche ya consumio esa ancla (la
reemplazo por "...puerta=3,mask_rel=0,...,ema_c=0.05):", que ya no contiene la subcadena original completa antes
del cierre "):"). Se resuelve en compone(): pon_hija() se aplica PRIMERO con la ancla y firma originales
(ancla_firma_orig -> ancla_firma_orig + SUF_D); pon_puerta() se aplica DESPUES usando como SU "ancla_firma" el
texto YA parchado (ancla_firma_orig + SUF_D), no el original. pon_puerta() no cambia una sola linea: solo cambian
los ARGUMENTOS con que se la llama. Para organismo_capB.py el orden es el otro: la puerta YA esta en el origen
(construye_puerta_codigo.py ya la aplico) y aqui solo se agrega mask_rel, con su propia ancla_firma ya ajustada a
lo que ese archivo tiene HOY (ver PASO 6 abajo) -- ahi no hace falta compone(). Tampoco se pudo llamar pon_hija()
sin mas: su sustitucion de "traza" trae la indentacion (24 espacios) escrita a mano para el "if plast:" de
organismo_v13/v13g, y en organismo_capB esa misma linea vive 4 espacios mas arriba (fuera de "if plast:"; solo la
division esta adentro). Se declara y se resuelve en el PASO 6 reproduciendo las cinco sustituciones de pon_hija()
a mano, con esa unica correccion de indentacion (el resto, firma/estado/kj/herencia, es el mismo texto exacto).
La ancla de ESTADO ("Wps=np.zeros(...); Wns=np.zeros(...) # v13: via LENTA...") la usan LAS DOS funciones como
punto de insercion, pero NO es una colision real: cada una solo AGREGA texto justo despues del ancla sin tocar el
ancla misma, asi que la segunda insercion la sigue encontrando exactamente una vez (se comprueba en construccion:
si alguna vez deja de ser asi, sust() aborta con la cuenta). Ninguna otra ancla de las dos funciones coincide
(valor/boca/mordida/salida son propias de pon_puerta(); estado/traza/kj/herencia son propias de pon_hija()).

Salidas (las DOS perillas APAGADAS por defecto en todo lo que no diga "_on" -> organismo_v13 / organismo_v13g /
bateria_v13 / bateria_generaliza EXACTOS bit a bit; arnes obligatorio: identidad_v14c.py):

  organismo_v14c.py          <- organismo/organismo_v13.py                  (cc8b16b492d4d324)
  organismo_v14c_on.py       <- organismo_v14c.py, las DOS perillas fijas ON (mask_rel=2 del punto de
                                 organismo_v13Don; puerta_pat=5,pat_min=1 del punto de organismo_v13Bn5c = PATC)
  organismo_v14gc.py         <- experimentos/v13_dos_vias/organismo_v13g.py (2a80e125f8593bf2)   mundo de regla
  bateria_v14c.py            <- organismo/bateria_v13.py                    (1a027bcb37eb536e)   solo el modulo
  bateria_generaliza_v14c.py <- organismo/bateria_generaliza.py             (46772f5a582872c8)   solo el modulo
                                 (INSTRUMENTOS: 'organismo_v14c' y 'organismo_v14c_on', las dos sobre
                                 organismo_v14gc.py -- no hace falta un organismo_v14gc_on.py aparte: basta pasar
                                 las perillas como kwargs en el dict de INSTRUMENTOS, como ya hace bateria_generaliza_D.py)

  -- para C3/C4 del preregistro (composicion en instrumentos que ya tenian UNA de las dos perillas) --
  organismo_capBD.py         <- experimentos/nivel4_puerta_codigo/organismo_capB.py (sha abajo) + SOLO mask_rel
                                 (puerta_pat ya estaba en el origen); mundo GRANDE, para C4
  organismo_capBD_on.py      <- organismo_capBD.py, las DOS perillas fijas ON
  mundo_composicion_v14.py   <- experimentos/nivel7_hija_dispersa/mundo_hija_dispersa.py (sha abajo) + SOLO
                                 puerta_pat (mask_rel ya estaba en el origen); mundo 3T-k, para C3

Uso:  python experimentos/nivel10_composicion_v14/construye_v14c.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
D7 = os.path.join(RAIZ, 'experimentos', 'nivel7_hija_dispersa')
D4 = os.path.join(RAIZ, 'experimentos', 'nivel4_puerta_codigo')
# organismo/ PRIMERO en sys.path (ERR-28), aunque aqui no importamos organismo_v13 en tiempo de construccion
# (solo se lee como texto): es la regla para todo runner de este repo, sin excepcion.
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), D7, D4]

import construye_v13D as CD           # trae pon_hija() (mask_rel) -- no se ejecuta: su __main__ no corre al importar
import construye_puerta_codigo as CB  # trae pon_puerta(), ESTADO, CUENTA (puerta_pat) -- idem


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


# ---- anclas reproducidas de construye_v13D.py / construye_puerta_codigo.py (viven dentro de su __main__, no
#      son importables) -- copiadas a mano de esos scripts y de organismo_v13.py / organismo_v13g.py ----
KJ = "                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*(P>0)\n"
SUF_D = ",mask_rel=0,del_s=0.25,del_c=0.25,ema_c=0.05):"      # lo que pon_hija() agrega a la firma
SUF_B = ",puerta_pat=0,pat_shuf=0,pat_min=0):"                # lo que pon_puerta() agrega a la firma
ANCLA_ESTADO = "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)\n"
ANCLA_MORDIDA = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1\n"
ANCLA_RET = "splits=splits,celdas=int(activa.sum()),\n"


def compone(s, ancla_firma_orig, ancla_traza, etiqueta):
    """Aplica, EN ORDEN, hija dispersa (mask_rel) y despues puerta por codigo (puerta_pat) sobre el mismo texto
    `s` (organismo_v13.py u organismo_v13g.py ya leidos). Devuelve el texto con las DOS perillas apagadas por
    defecto. Resuelve la colision de la firma declarada arriba: pon_puerta() recibe como SU ancla_firma el
    resultado que dejo pon_hija(), no el original."""
    firma1 = ancla_firma_orig[:-2] + SUF_D   # se quita el "):" del original antes de pegar el sufijo (que trae el suyo)
    s = CD.pon_hija(s, ancla_firma_orig, firma1, ANCLA_ESTADO, 6, ancla_traza, KJ, etiqueta)
    firma2 = firma1[:-2] + SUF_B   # firma1 termina en "):"; se quita y SUF_B pone su propio "):" al final
    s = CB.pon_puerta(s, firma1, firma2, ANCLA_ESTADO, ANCLA_MORDIDA, ANCLA_RET, etiqueta)
    return s


if __name__ == '__main__':
    salidas = []

    # ==== 1) organismo_v14c: organismo_v13 + las DOS perillas (apagadas) ====
    s = origen(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'), 'cc8b16b492d4d324')
    TRAZA_V13 = ("                        P=PAT[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]"
                 "+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P")
    s = compone(s, "eta_s=0.015,clip_s=3.0,puerta=3):", TRAZA_V13, 'v14c')
    cab = ('"""organismo_v14c = organismo/organismo_v13.py (cc8b16b492d4d324, CONGELADO: solo se leyo) + COMPOSICION\n'
           'de los dos candidatos a v14 con evidencia completa (registro/PROPUESTA_v14.md): HIJA DISPERSA POR\n'
           'RELEVANCIA (perilla mask_rel; actua en el NACIMIENTO, nivel7_hija_dispersa/construye_v13D.py) + PUERTA POR\n'
           'EVIDENCIA DEL CODIGO EXACTO (perilla puerta_pat, PATC; actua en el RUTEO, no en el aprendizaje,\n'
           'nivel4_puerta_codigo/construye_puerta_codigo.py). Generado por construye_v14c.py. NO editar a mano.\n'
           'Con mask_rel=0 y puerta_pat=0 es organismo_v13 EXACTO (arnes: identidad_v14c.py)."""\n')
    d = os.path.join(AQUI, 'organismo_v14c.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)
    FIRMA_V14C_OFF = "puerta=3,mask_rel=0,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=0,pat_shuf=0,pat_min=0):"

    # ==== 2) organismo_v14c_on: la misma, las DOS perillas fijas ON ====
    #      mask_rel=2 (el punto de organismo_v13Don) y puerta_pat=5,pat_min=1 (el punto de organismo_v13Bn5c = PATC,
    #      la enmienda 1 que SI paso el examen v3' 8/8 en dos series -- no organismo_v13Bn5 = PAT sin la enmienda).
    s2 = sust(origen(d, h16(d)), FIRMA_V14C_OFF,
              "puerta=3,mask_rel=2,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=5,pat_shuf=0,pat_min=1):",
              etiqueta='v14c_on: las dos perillas encendidas')
    d2 = os.path.join(AQUI, 'organismo_v14c_on.py')
    open(d2, 'w', encoding='utf-8', newline='\n').write(
        '"""organismo_v14c_on = organismo_v14c.py con mask_rel=2 (hija dispersa; el punto de organismo_v13Don) Y\n'
        'puerta_pat=5,pat_min=1 (puerta por codigo PATC = evidencia Y >=1 celda consolidada; el punto de\n'
        'organismo_v13Bn5c) POR DEFECTO -- las DOS perillas ENCENDIDAS. El mismo archivo con las constantes\n'
        'cambiadas, para que bateria_v14c.py lo examine sin tocar la bateria congelada.\n'
        'Generado por construye_v14c.py. NO editar."""\n' + s2)
    salidas.append(d2)

    # ==== 3) organismo_v14gc: el mundo de regla (lo que usa bateria_generaliza_v14c) ====
    s = origen(os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py'), '2a80e125f8593bf2')
    TRAZA_V13G = ("                        P=P_[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]"
                  "+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P")
    s = compone(s, "sonda_final=False):", TRAZA_V13G, 'v14gc')
    cab = ('"""organismo_v14gc = experimentos/v13_dos_vias/organismo_v13g.py (2a80e125f8593bf2) + COMPOSICION\n'
           '(mask_rel + puerta_pat, ver organismo_v14c.py). Es el instrumento del MUNDO DE REGLA que usa\n'
           'bateria_generaliza_v14c.py. Generado por construye_v14c.py. NO editar.\n'
           'Con mask_rel=0 y puerta_pat=0 es organismo_v13g EXACTO."""\n')
    d = os.path.join(AQUI, 'organismo_v14gc.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ==== 4) bateria_v14c: la bateria del tronco (CONGELADA: solo se LEE) apuntando a organismo_v14c_on ====
    #      Nota sobre el criterio 5 (identidad a v11/v10; ver docstring de identidad_v14c.py para el argumento
    #      completo): NO hace falta adaptarlo (a diferencia de v13E/ERR-30, que actuaba en la boca sin pasar por
    #      eta_s/puerta). El criterio 5 llama v13.run(seed, eta_s=0.0, puerta=None, **ESC_ID[esc]): (a) puerta_pat
    #      queda estructuralmente sin efecto porque "puerta is None" evita _fam() en valor() y en la boca SIEMPRE,
    #      sea cual sea puerta_pat (se ve en pon_puerta(): el ternario mira "puerta is None" ANTES que _fam); (b)
    #      mask_rel=2 SI queda activo (nada lo apaga con eta_s/puerta), pero ya se demostro inerte en este mundo de
    #      6 px y un objeto (bateria_v13D.py corrio su propio criterio 5 con organismo_v13Don, mask_rel=2 ON, y el
    #      examen 8/8 completo en datos/baterias_v13D_20260918_012145 solo pudo producirse si el criterio 5 PASO --
    #      bateria_v13.py aborta con sys.exit(1) si falla). Sigue siendo una PREDICCION para la composicion (los
    #      dos mecanismos juntos en el criterio 5 no se han probado antes): se preregistra como control que puede
    #      fallar (si falla, C1 no es medible y la bateria entera aborta antes de la etapa 2).
    s = origen(os.path.join(RAIZ, 'organismo', 'bateria_v13.py'), '1a027bcb37eb536e')
    s = sust(s, "AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(AQUI)\n"
                "sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]\n",
             "_D14 = os.path.dirname(os.path.abspath(__file__))   # esta copia vive fuera de organismo/\n"
             "AQUI = os.path.join(os.path.dirname(os.path.dirname(_D14)), 'organismo')\n"
             "RAIZ = os.path.dirname(AQUI)\n"
             "sys.path[:0] = [_D14, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]\n", etiqueta='bateria_v14c: rutas')
    s = sust(s, "    import organismo_v13 as v13\n",
             "    import organismo_v14c_on as v13   # composicion: hija dispersa + puerta por codigo, las DOS ON\n",
             n=2, etiqueta='bateria_v14c: import')
    s = s.replace("h16(os.path.join(AQUI, 'organismo_v13.py'))", "h16(os.path.join(_D14, 'organismo_v14c_on.py'))")
    s = s.replace("f'examen_v13_{stamp}", "f'examen_v14c_{stamp}")
    cab = ('"""bateria_v14c = organismo/bateria_v13.py (1a027bcb37eb536e, CONGELADO: solo se leyo) apuntando a\n'
           'organismo_v14c_on (composicion: hija dispersa + puerta por codigo, las DOS ON) en vez de organismo_v13.\n'
           'Las SEIS etapas, los CRIT importados y los umbrales del criterio v3\' quedan INTACTOS -- este es el C1\n'
           'del PREREGISTRO_composicion_v14.md. Salida en datos/examen_v14c_<fecha>.\n'
           'Generado por construye_v14c.py. NO editar. La bateria original NO se modifico."""\n')
    d = os.path.join(AQUI, 'bateria_v14c.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ==== 5) bateria_generaliza_v14c: con las dos entradas nuevas de INSTRUMENTOS, ambas sobre organismo_v14gc ====
    s = origen(os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'), '46772f5a582872c8')
    s = sust(s, "AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(AQUI)\n",
             "AQUI = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'organismo')   # esta copia vive fuera de organismo/\n"
             "RAIZ = os.path.dirname(AQUI)\n", etiqueta='bateria_generaliza_v14c: AQUI/RAIZ')
    s = sust(s, "REGLAS = ['px0', 'azar']\n",
             "REGLAS = ['px0', 'azar']\n_D14 = os.path.join(RAIZ, 'experimentos', 'nivel10_composicion_v14')\n",
             etiqueta='bateria_generaliza_v14c: _D14')
    s = sust(s, "    'organismo_v13_rapido': ('organismo_v13q_rapido', dict(eta_s=0.015, puerta=3)),   # gemelo compilado del mundo de regla (identidad 81/81+243/243); mismo punto\n",
             "    'organismo_v13_rapido': ('organismo_v13q_rapido', dict(eta_s=0.015, puerta=3)),   # gemelo compilado del mundo de regla (identidad 81/81+243/243); mismo punto\n"
             "    'organismo_v14c': ('organismo_v14gc', dict(eta_s=0.015, puerta=3)),   # composicion: las DOS perillas APAGADAS -> debe dar lo mismo que organismo_v13\n"
             "    'organismo_v14c_on': ('organismo_v14gc', dict(eta_s=0.015, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)),   # composicion: las DOS ON\n",
             etiqueta='bateria_generaliza_v14c: INSTRUMENTOS')
    s = sust(s, "sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))\n",
             "sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))\n"
             "sys.path.insert(0, _D14)   # composicion: organismo_v14gc\n", etiqueta='bateria_generaliza_v14c: sys.path')
    s = sust(s, "    _dir = {'organismo_v11g': GEN, 'organismo_v13g': os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),\n",
             "    _dir = {'organismo_v11g': GEN, 'organismo_v13g': os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),\n"
             "            'organismo_v14gc': _D14,\n", etiqueta='bateria_generaliza_v14c: _dir')
    s = s.replace("h16(os.path.join(AQUI, (modulo if modulo != 'organismo_v13_rapido' else 'organismo_v13') + '.py'))",
                  "h16(os.path.join(AQUI, 'organismo_v13.py') if modulo == 'organismo_v13_rapido' else (os.path.join(AQUI, modulo + '.py') if os.path.exists(os.path.join(AQUI, modulo + '.py')) else os.path.join(_D14, modulo.split('_on')[0] + '.py')))")
    s = s.replace("sha_organismo=h16(os.path.join(AQUI, modulo + '.py')),",
                  "sha_organismo=(h16(os.path.join(AQUI, modulo + '.py')) if os.path.exists(os.path.join(AQUI, modulo + '.py')) else h16(os.path.join(_D14, modulo.split('_on')[0] + '.py'))),")
    cab = ('"""bateria_generaliza_v14c = organismo/bateria_generaliza.py (46772f5a582872c8) con DOS entradas mas en\n'
           'INSTRUMENTOS (organismo_v14c y organismo_v14c_on, ambas sobre organismo_v14gc) y las rutas corregidas por\n'
           'vivir fuera de organismo/. Los UMBRALES y los criterios G1/G2/K NO se tocan -- este es el C2 del\n'
           'PREREGISTRO_composicion_v14.md (con organismo_v14c_on).\n'
           'Generado por construye_v14c.py. NO editar. La bateria original NO se modifico."""\n')
    d = os.path.join(AQUI, 'bateria_generaliza_v14c.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ==== 6) organismo_capBD: organismo_capB.py (YA tiene puerta_pat) + SOLO mask_rel; mundo GRANDE, para C4 ====
    #      organismo_capB.py NO es organismo_v13/organismo_v13g: es capD13 (retina de D pixeles) + la puerta. Las
    #      anclas de KJ y de herencia de pon_hija() SI calzan tal cual (misma familia de codigo, estilo compacto
    #      sin espacios, y coinciden en profundidad de indentacion pese a lo que sigue) -- verificado por sust().
    #      DIFERENCIA REAL DECLARADA: la linea de traza ("P=pats[kk]; idx=...; mu[idx]=...") esta en organismo_capB
    #      a 20 espacios, FUERA de "if plast:" (ese archivo actualiza err/mu del elemental siempre, y solo la
    #      division vive adentro de "if plast:"); en organismo_v13/v13g esa misma linea esta a 24 espacios, DENTRO
    #      de "if plast:". El texto de reemplazo de pon_hija() para esa ancla trae la indentacion de 24 espacios
    #      escrita a mano (no es parametro), asi que aqui NO se llama pon_hija() -- se reproducen sus MISMAS cinco
    #      sustituciones (firma/estado/traza/kj/herencia; firma/estado/kj/herencia con el mismo texto exacto de
    #      pon_hija(), traza con la indentacion corregida a 20 espacios). Primer intento sin este ajuste fallo en
    #      py_compile (IndentationError linea 165) -- por eso se declara aqui en vez de dejarlo implicito.
    ORIGEN_CAPB = os.path.join(D4, 'organismo_capB.py'); SHA_CAPB = h16(ORIGEN_CAPB)
    s = origen(ORIGEN_CAPB, SHA_CAPB)
    ANCLA_FIRMA_CAPB = "eta_s=0.0,clip_s=3.0,puerta=None,puerta_pat=0,pat_shuf=0,pat_min=0):"
    ANCLA_ESTADO_CAPB = "    Wps=np.zeros(D); Wns=np.zeros(D)   # v13: via LENTA lineal sobre la retina (inerte si eta_s=0)\n"
    ANCLA_TRAZA_CAPB = ("                    P=pats[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]"
                        "+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P")
    s = sust(s, ANCLA_FIRMA_CAPB, ANCLA_FIRMA_CAPB[:-2] + SUF_D, etiqueta='capBD: firma')
    s = sust(s, ANCLA_ESTADO_CAPB, ANCLA_ESTADO_CAPB +
             "    mup=np.zeros((NKMAX,D)); mun=np.zeros((NKMAX,D)); zp=np.zeros(NKMAX); zn=np.zeros(NKMAX)   # D: medias de P condicionadas al signo de R, con normalizador\n",
             etiqueta='capBD: estado')
    s = sust(s, ANCLA_TRAZA_CAPB, ANCLA_TRAZA_CAPB +
             "\n                    if R>0: mup[idx]=(1-ema_c)*mup[idx]+ema_c*P; zp[idx]=(1-ema_c)*zp[idx]+ema_c   # D\n"
             "                    elif R<0: mun[idx]=(1-ema_c)*mun[idx]+ema_c*P; zn[idx]=(1-ema_c)*zn[idx]+ema_c   # D",
             etiqueta='capBD: medias condicionadas (20 espacios: ver nota arriba)')
    s = sust(s, KJ,
             "                                if mask_rel==2 and zp[c]>1e-6 and zn[c]>1e-6:   # D: HIJA DISPERSA (contexto O discriminador)\n"
             "                                    _mp=mup[c]/float(zp[c]); _mn=mun[c]/float(zn[c])\n"
             "                                    _rel=(P>0)&((np.abs(_mp-_mn)>del_s)|(np.minimum(_mp,_mn)>1.0-del_c))\n"
             "                                else: _rel=(P>0)\n"
             "                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*_rel\n",
             etiqueta='capBD: mascara')
    s = sust(s, "                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n",
             "                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n"
             "                                    mup[j]=mup[c].copy(); mun[j]=mun[c].copy(); zp[j]=zp[c]; zn[j]=zn[c]   # D: la hija hereda las medias condicionadas\n",
             etiqueta='capBD: herencia')
    cab = (f'"""organismo_capBD = experimentos/nivel4_puerta_codigo/organismo_capB.py ({SHA_CAPB}, instrumento ya\n'
           'corrido: solo se leyo) + HIJA DISPERSA POR RELEVANCIA (perilla mask_rel; puerta_pat ya estaba en el\n'
           'origen). Mundo GRANDE (capacidad, D estimulos) -- este es el instrumento de C4 del\n'
           'PREREGISTRO_composicion_v14.md. Generado por construye_v14c.py. NO editar a mano.\n'
           'Con mask_rel=0 (y puerta_pat=0, heredado) es organismo_capB EXACTO (arnes: identidad_v14c.py)."""\n')
    d = os.path.join(AQUI, 'organismo_capBD.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ==== 7) organismo_capBD_on: la misma, las DOS perillas fijas ON ====
    FIRMA_CAPBD_OFF = ANCLA_FIRMA_CAPB[:-2] + SUF_D   # "...puerta_pat=0,pat_shuf=0,pat_min=0,mask_rel=0,del_s=0.25,del_c=0.25,ema_c=0.05):"
    s2 = sust(origen(d, h16(d)), FIRMA_CAPBD_OFF,
              "eta_s=0.0,clip_s=3.0,puerta=None,puerta_pat=5,pat_shuf=0,pat_min=1,mask_rel=2,del_s=0.25,del_c=0.25,ema_c=0.05):",
              etiqueta='capBD_on: las dos perillas encendidas')
    d2 = os.path.join(AQUI, 'organismo_capBD_on.py')
    open(d2, 'w', encoding='utf-8', newline='\n').write(
        '"""organismo_capBD_on = organismo_capBD.py con puerta_pat=5,pat_min=1 (PATC) Y mask_rel=2 (hija dispersa)\n'
        'POR DEFECTO -- las DOS perillas ENCENDIDAS, en el mundo GRANDE. Para C4 del PREREGISTRO_composicion_v14.md.\n'
        'Generado por construye_v14c.py. NO editar."""\n' + s2)
    salidas.append(d2)

    # ==== 8) mundo_composicion_v14: mundo_hija_dispersa.py (YA tiene mask_rel) + SOLO puerta_pat; 3T-k, para C3 ====
    #      mundo_hija_dispersa.py NO es organismo_v13: desciende de mundo_temporal_v13/v11/v9/v8 (misma familia de
    #      reglas de v13, dos vias + puerta) pero escrito con ESPACIOS alrededor de operadores (estilo distinto de
    #      organismo_v13.py). pon_puerta() tiene DOS anclas de "valor"/"boca" escritas LITERALMENTE (sin espacios)
    #      dentro de su propio cuerpo -- no son parametro, asi que NO calzan aqui. Se reproducen esas dos
    #      sustituciones a mano (mismo mecanismo, mismo ESTADO/CUENTA importados de construye_puerta_codigo, solo
    #      cambia el texto exacto por el formato del archivo); se declara aqui, no se esconde.
    ORIGEN_MHD = os.path.join(D7, 'mundo_hija_dispersa.py'); SHA_MHD = h16(ORIGEN_MHD)
    s = origen(ORIGEN_MHD, SHA_MHD)
    ANCLA_FIRMA_MHD = ("theta=0.6, ema=0.02, paso=0.5, early=5000, nkmax=NKMAX, wclip=3.0, lam=0.05, "
                       "memoria_rechazo=20, mu_norm=False, div_signo=False, eta_s=0.0, clip_s=3.0, puerta=None, "
                       "kprof=1, recic=0, tau_r=0, mask_rel=0, del_s=0.25, del_c=0.25, n_cf=1, ema_c=0.05):")
    NUEVA_FIRMA_MHD = ANCLA_FIRMA_MHD[:-2] + ", puerta_pat=0, pat_shuf=0, pat_min=0):"
    s = sust(s, ANCLA_FIRMA_MHD, NUEVA_FIRMA_MHD, etiqueta='mundo_composicion_v14: firma')
    s = sust(s, "    Wp = np.zeros(nkmax); Wn = np.zeros(nkmax)\n",
             "    Wp = np.zeros(nkmax); Wn = np.zeros(nkmax)\n" + CB.ESTADO, etiqueta='mundo_composicion_v14: estado')
    s = sust(s, "        return _f + _s if puerta is None else (_f if int((np.abs((Wp - Wn)[_k > 0]) > 0.2).sum()) >= puerta else _s)\n",
             "        return _f + _s if puerta is None else (_f if _fam(_k) else _s)\n", etiqueta='mundo_composicion_v14: valor')
    s = sust(s, "            _wt = _wf + _ws if puerta is None else (_wf if int((np.abs(Wb[kc > 0]) > 0.2).sum()) >= puerta else _ws)   # v13\n",
             "            _wt = _wf + _ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13\n", etiqueta='mundo_composicion_v14: boca')
    s = sust(s, "            if mordio:\n", "            if mordio:\n" + CB.CUENTA, etiqueta='mundo_composicion_v14: contador')
    s = sust(s, "        mask_rel=mask_rel, div_diag=div_diag, n_cf=n_cf,\n",
             "        mask_rel=mask_rel, div_diag=div_diag, n_cf=n_cf,\n"
             "        puerta_pat=puerta_pat, pat_shuf=pat_shuf, pat_min=pat_min, n_cod=len(ncod),\n",
             etiqueta='mundo_composicion_v14: salida')
    cab = (f'"""mundo_composicion_v14 = experimentos/nivel7_hija_dispersa/mundo_hija_dispersa.py ({SHA_MHD},\n'
           'instrumento ya corrido: solo se leyo) + PUERTA POR EVIDENCIA DEL CODIGO EXACTO (perilla puerta_pat;\n'
           'mask_rel/recic/n_cf ya estaban en el origen). Mundo 3T-k (composicion temporal) -- este es el\n'
           'instrumento de C3 del PREREGISTRO_composicion_v14.md. Generado por construye_v14c.py. NO editar a mano.\n'
           'Con puerta_pat=0 (y mask_rel=0, recic=0, n_cf=1 heredados) es mundo_temporal_k EXACTO '
           '(arnes: identidad_v14c.py)."""\n')
    d = os.path.join(AQUI, 'mundo_composicion_v14.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    print(f"=== construye_v14c.py: {len(salidas)} archivos ===")
    for d in salidas:
        print(f"  {os.path.relpath(d, RAIZ):55s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
