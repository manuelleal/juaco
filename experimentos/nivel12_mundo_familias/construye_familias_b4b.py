"""Construye experimentos/nivel12_mundo_familias/organismo_familias_b4b.py POR ANCLAS, sobre
organismo_familias_b4.py (bloque 4, ff9946ee2ffe27e6; aqui SOLO SE LEE).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive, se reproduce y se COMUNICA, con evidencia
preregistrada. Hoy: que dos celulas se comuniquen SOBRE ALGO QUE AMBAS REPRESENTAN -- y que la que habla pueda
llegar a saberlo.

ERR-51 (montaje del emisor, bloque 4): el emisor COMPARTE EL PUNTO CIEGO DEL RECEPTOR. Para poder decir "lo que
evitas es comida" alguien tiene que haberlo mordido, y el emisor lo evita por la misma razon que el receptor (su
familia es veneno). En el bloque 4 la puerta P-I2 cayo en la direccion (-): 5/20 y 4/20 emisores sin mensaje.

DOS PERILLAS NUEVAS, las dos INERTES en su valor por defecto:

  `voraz` (default 0.0)   -- UNA constante del propio ORGANO DE LA BOCA, sumada a su variable de decision:
                             Vb = alpha*w + hambre_boca*hambre + 0.5 + voraz.  No mira el mundo, no sabe donde esta
                             la excepcion, no toca el aprendizaje, no toca la energia, no toca el orden del rng
                             (la misma unica llamada rng.random() por mordida). Es el eje "timida / voraz" que la
                             sala 3 nombro y que el organismo no tenia como perilla. Con voraz=0.0 es b4 BIT A BIT.

  `par_herm` (default None) -- (k, j): en la presentacion del mundo, el TOKEN de la familia k se sustituye por su
                             variante j, y esa variante queda EXENTA de la deriva. Asi el receptor ve DOS VARIANTES
                             de la misma familia a la vez (la excepcion Tkv2 y su hermana Tkvj) en vez de la
                             excepcion y su token. `len(tipos)` NO cambia: el sorteo de spawn() es el mismo y el
                             rng del mundo queda intacto. Con par_herm=None es b4 BIT A BIT.
                             (Es la unica forma de medir la especificidad entre HERMANAS de verdad: en el bloque 4,
                             con deriva(R) = T/3+1 la corrida tiene tres fases y no vuelve a la 0, asi que tras la
                             entrega la unica hermana que reaparece es el TOKEN -- n_H = 1, y el token es la
                             discriminacion MAS FACIL, no la mas dificil.)

EL CANAL NO SE TOCA: misma mecanica, mismos modos, mismo bloque de escritura extraido de b3. `par_herm` cambia el
MUNDO del receptor, no el mensaje.

ANCLA DE IDENTIDAD (regla 2 de EQUIPO.md), lo que comprueba identidad_familias_b4b.py:
  (a) con voraz=0.0 y par_herm=None -> organismo_familias_b4 BIT A BIT en TODAS sus claves, y el rng NO se consume;
      por la cadena de b4, tambien b3, b2, organismo_familias, organismo_v14 (TRONCO) y organismo_v15f_on;
  (b) voraz solo puede mover la MORDIDA: con learn=False y voraz=0 nada cambia; el consumo del rng es el mismo;
  (c) par_herm sustituye la presentacion sin tocar el rng del mundo;
  (d) controles que DEBEN fallar.

Uso:  python experimentos/nivel12_mundo_familias/construye_familias_b4b.py     (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

SHA_B4 = 'ff9946ee2ffe27e6'          # organismo_familias_b4.py (bloque 4, identidad 92/92)
SHA_B3 = '62a1e53b452b078e'
SHA_B2 = '30200bea6a41c3c8'
SHA_MF = 'b9dd561a0cf056b8'
SHA_V14 = 'feefc88b1fd8d434'
SHA_V15F_ON = '54d6efe0b564113c'
SHA_ESCALA = 'd8b8566bca77a0ae'
DESTINO = os.path.join(AQUI, 'organismo_familias_b4b.py')


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


# ---------------------------------------------------------------- anclas en organismo_familias_b4.py
A_FIRMA = ",fam_seed=None,exc_fija=None,canal=None,reg_b4=0):"
A_DEF = "def _familias(seed,D,n_var,F,V,n_exc,fam_val,n_neu,exc_evita=-1,vira=0,exc_fija=None):"
A_PRES = "    pres=[['T%d'%_k for _k in range(F)]+['T%dv%d'%(_k,_i) for _k in range(F)] for _i in range(V)]\n"
A_FAM = "_FA=_familias((seed if fam_seed is None else int(fam_seed)),"
A_DER = "                    if _FA['var'][objs[_x]]>=0: objs[_x]='T%dv%d'%(_FA['fam'][objs[_x]],_ip)"
A_BOCA = "            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb\n"
A_RET = "    return dict(canal=(dict(canal) if canal else None),"

CABECERA = '''"""organismo_familias_b4b = organismo_familias_b4.py (bloque 4, canal con referencia por senalamiento,
ff9946ee2ffe27e6) + DOS PERILLAS para el BLOQUE 4b, las dos inertes por defecto:
  `voraz`    : una constante del propio organo de la BOCA, sumada a su variable de decision
               (Vb = alpha*w + hambre_boca*hambre + 0.5 + voraz). El eje "timida/voraz". No mira el mundo, no toca
               el aprendizaje ni la energia, y consume el MISMO rng. Con voraz=0.0 es b4 BIT A BIT.
               ERR-51: sin ella el EMISOR comparte el punto ciego del receptor y no llega a morder lo que evita.
  `par_herm` : (k, j) -- en la presentacion, el TOKEN de la familia k se sustituye por su variante j, EXENTA de la
               deriva, para que el receptor vea DOS VARIANTES de la misma familia a la vez. `len(tipos)` no cambia:
               el rng del mundo queda intacto. Con par_herm=None es b4 BIT A BIT.
EL CANAL NO SE TOCA. ANCLA DE IDENTIDAD: con voraz=0.0 y par_herm=None es organismo_familias_b4 BIT A BIT (y por su
cadena, b3, b2, organismo_familias, organismo_v14 y organismo_v15f_on).
Arnes: identidad_familias_b4b.py.  Generado por construye_familias_b4b.py. NO editar a mano."""
'''


def main():
    for p, sha in [(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                   (os.path.join(AQUI, 'organismo_familias.py'), SHA_MF),
                   (os.path.join(AQUI, 'organismo_familias_b2.py'), SHA_B2),
                   (os.path.join(AQUI, 'organismo_familias_b3.py'), SHA_B3),
                   (os.path.join(AQUI, 'escala_codigo.py'), SHA_ESCALA),
                   (os.path.join(CREA, 'organismo_v15f_on.py'), SHA_V15F_ON)]:
        if h16(p) != sha:
            raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado.")

    t = origen(os.path.join(AQUI, 'organismo_familias_b4.py'), SHA_B4)
    t = CABECERA + t

    # ---- firma de run: las dos perillas nuevas, al final
    t = sust(t, A_FIRMA, A_FIRMA[:-2] + ",voraz=0.0,par_herm=None):", etiqueta='firma de run')
    # ---- firma de _familias y la sustitucion de la presentacion (SIN tocar el rng del mundo)
    t = sust(t, A_DEF, A_DEF[:-2] + ",par_herm=None):", etiqueta='firma de _familias')
    t = sust(t, A_PRES, A_PRES +
             "    _PH=None\n"
             "    if par_herm is not None:   # B4b: el TOKEN de la familia k se sustituye por su variante j. `len` NO cambia: el sorteo de spawn() es el mismo y el rng del mundo queda intacto.\n"
             "        _pk,_pj=int(par_herm[0]),int(par_herm[1]); _PH='T%dv%d'%(_pk,_pj)\n"
             "        pres=[[(_PH if _n=='T%d'%_pk else _n) for _n in _p] for _p in pres]\n",
             etiqueta='par_herm: sustitucion en la presentacion')
    t = sust(t, "    return dict(PAT=PAT,fam=fam,var=var,val=val,exc=exc,exc_win=exc_win,herm=herm,pres=pres,",
             "    return dict(par_fijo=_PH,PAT=PAT,fam=fam,var=var,val=val,exc=exc,exc_win=exc_win,herm=herm,pres=pres,",
             etiqueta='par_herm: el nombre exento sale del mundo')
    t = sust(t, A_FAM + "fam_D,fam_nvar,fam_F,fam_V,n_exc,fam_val,n_neu,exc_evita,vira,exc_fija)",
             A_FAM + "fam_D,fam_nvar,fam_F,fam_V,n_exc,fam_val,n_neu,exc_evita,vira,exc_fija,par_herm)",
             etiqueta='par_herm en la llamada al mundo')
    # ---- la hermana sustituida queda EXENTA de la deriva (si no, en la fase 2 se convertiria en la propia excepcion)
    t = sust(t, A_DER,
             "                    if _FA['var'][objs[_x]]>=0 and objs[_x]!=_FA['par_fijo']: objs[_x]='T%dv%d'%(_FA['fam'][objs[_x]],_ip)   # B4b: la hermana sustituida NO deriva (con par_herm=None, _FA['par_fijo'] es None y ningun nombre lo iguala: b4 exacto)",
             etiqueta='par_herm: exenta de la deriva')
    # ---- voraz: UNA constante en la variable de decision de la boca
    t = sust(t, A_BOCA,
             "            Vb=alpha*_wt+hambre_boca*hambre+.5+voraz; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb   # B4b: `voraz` es una constante del propio organo de la boca (eje timida/voraz). Con voraz=0.0 esta linea es la de b4, caracter a caracter salvo el sumando nulo.\n",
             etiqueta='voraz en la boca')
    # ---- claves de salida
    t = sust(t, A_RET, "    return dict(voraz=float(voraz),par_herm=(list(par_herm) if par_herm is not None else None),"
                       "par_fijo=(_FA['par_fijo'] if _MF else None),canal=(dict(canal) if canal else None),",
             etiqueta='diccionario de salida')

    if 'hambre_boca*hambre+.5;' in t:
        raise SystemExit("ANCLA voraz: quedo una boca sin la perilla. Abortado.")
    compile(t, DESTINO, 'exec')
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print("  ANCLAS sobre organismo_familias_b4.py  OK: 7 (2 de firma, 3 de par_herm, 1 de voraz, 1 de salida)")
    print(f"  escrito {os.path.relpath(DESTINO, RAIZ)}")
    print(f"  sha origen  organismo_familias_b4.py  {SHA_B4}")
    print(f"  sha destino organismo_familias_b4b.py {h16(DESTINO)}")
    print("  ahora: python experimentos/nivel12_mundo_familias/identidad_familias_b4b.py")


if __name__ == '__main__':
    main()
