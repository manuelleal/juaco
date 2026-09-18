"""Construye experimentos/nivel12_mundo_familias/organismo_familias_b4.py POR ANCLAS, con DOS CADENAS.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive, se reproduce y se COMUNICA, con evidencia
preregistrada.

  CADENA 1 (EXTRACCION) -- del PROPIO organismo_familias_b3.py (62a1e53b452b078e; aqui SOLO SE LEE) se EXTRAE
            LITERALMENTE el bloque de ESCRITURA de la tabla de pares (el que corre cuando la boca muerde) y se
            reusa, dedentado, como cuerpo de la ENTREGA del mensaje. El canal NO reimplementa el aprendizaje:
            escribe EXACTAMENTE lo que habria escrito una mordida, con el patron y la valencia del mensaje, y
            NADA MAS (ERR-38: dos caminos al mismo numero, nunca una copia a mano).
  CADENA 2 (APLICACION) -- sobre organismo_familias_b3.py, con nueve anclas de linea.

Si CUALQUIERA de las dos cadenas no encaja (sha distinto, ancla ausente o repetida), ABORTA y no escribe nada.

LAS CUATRO PERILLAS NUEVAS, y nada mas (todas INERTES en su valor por defecto):
  `fam_seed` (default None)  -- semilla del MUNDO, separada de la del organismo. Con None es `seed` (b3 exacto).
                               Es lo que permite DOS organismos con rng propio EN EL MISMO MUNDO.
  `exc_fija` (default None)  -- la excepcion de cada token es una variante FIJA (la RETENIDA por la deriva), en vez
                               de una sorteada. El sorteo de b3 se hace igual, asi que el rng del mundo no cambia:
                               solo se sobrescribe el resultado. Es lo que hace que el receptor pueda NO HABERLA
                               VISTO NUNCA cuando llega el mensaje (y que generalizar desde la familia FALLE).
  `canal`    (default None)  -- dict. {'modo':'emite'} = el EMISOR anota, SIMETRICO (la primera mordida de cada
                               estimulo marcado y su R cruda, de cualquier signo; solo lectura: no toca ninguna
                               decision ni el rng). {'modo':'sen'|'inm'|'mudo','t','P','R','ref'} = el
                               RECEPTOR recibe el mensaje: una EXPOSICION SIN CONSECUENCIA con la valencia
                               recibida. No toca energia, ni objetos, ni la evidencia del codigo (`ncod`), ni la
                               via rapida, ni la plasticidad: solo la tabla de pares, por el bloque EXTRAIDO.
  `reg_b4`   (default 0)     -- registro de la CONDUCTA de la boca en las primeras exposiciones TRAS la entrega.

ANCLA DE IDENTIDAD (regla 2 de EQUIPO.md), lo que comprueba identidad_familias_b4.py:
  (a) con canal=None, fam_seed=None, reg_b4=0 -> organismo_familias_b3 BIT A BIT en TODAS sus claves, y el rng NO
      se consume (T = 120000); por la cadena de b3, tambien organismo_familias_b2, organismo_familias,
      organismo_v14 (TRONCO) y organismo_v15f_on;
  (b) con canal={'modo':'emite'} -> IDENTICO a canal=None en todas las claves de b3 (el emisor solo mira);
  (c) con fam_seed=seed -> IDENTICO a fam_seed=None (la perilla no cambia el mundo cuando apunta a la misma semilla);
  (d) controles que DEBEN fallar.

Uso:  python experimentos/nivel12_mundo_familias/construye_familias_b4.py     (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

SHA_B3 = '62a1e53b452b078e'          # organismo_familias_b3.py (bloque 3, identidad 71/71)
SHA_B2 = '30200bea6a41c3c8'          # organismo_familias_b2.py (bloque 2)
SHA_MF = 'b9dd561a0cf056b8'          # organismo_familias.py (bloque 1)
SHA_V14 = 'feefc88b1fd8d434'         # organismo/organismo_v14.py (TRONCO CONGELADO)
SHA_V15F = '96fc5c5262107850'        # experimentos/creacion_A/organismo_v15f.py
SHA_V15F_ON = '54d6efe0b564113c'     # experimentos/creacion_A/organismo_v15f_on.py
SHA_ESCALA = 'd8b8566bca77a0ae'      # escala_codigo.py (bloque 0)
DESTINO = os.path.join(AQUI, 'organismo_familias_b4.py')


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


def trozo(texto, ini, fin, etiqueta):
    """CADENA 1: extrae el bloque LITERAL que empieza en `ini` y termina en `fin` (inclusive)."""
    for a, nom in ((ini, 'inicio'), (fin, 'fin')):
        if texto.count(a) != 1:
            raise SystemExit(f"CADENA 1, {etiqueta} ({nom}): el ancla aparece {texto.count(a)} veces. Abortado.")
    i = texto.index(ini); j = texto.index(fin)
    if j < i:
        raise SystemExit(f"CADENA 1, {etiqueta}: el ancla de fin va ANTES que la de inicio. Abortado.")
    return texto[i:j + len(fin)]


def dedenta(bloque, n, etiqueta):
    """Quita EXACTAMENTE n espacios del principio de cada linea no vacia. Si alguna no los tiene, aborta."""
    out = []
    for l in bloque.split('\n'):
        if not l.strip():
            out.append(l); continue
        if not l.startswith(' ' * n):
            raise SystemExit(f"CADENA 1, {etiqueta}: la linea {l[:60]!r} no tiene {n} espacios de sangria. Abortado.")
        out.append(l[n:])
    return '\n'.join(out)


# ============ CADENA 1: ancla de EXTRACCION dentro de organismo_familias_b3.py ============
X_TAB_A = "                        if memoria_pares is not None:   # v15f/b3: las _NP celdas escriben R CRUDO"
X_TAB_B = "   # desempate al azar con el rng del organismo; solo consume rng si HAY empate\n"

# ============ CADENA 2: anclas de APLICACION en organismo_familias_b3.py ============
A_FIRMA = ",memoria_pares=None,mem_alfa=1.0,mem_rho=0.02):"
A_DEF = "def _familias(seed,D,n_var,F,V,n_exc,fam_val,n_neu,exc_evita=-1,vira=0):"
A_WIN = "        exc_win=['T%dv%d'%(_k,_al[int(g.integers(len(_al)))]) for _k in range(F)]\n"
A_FAM = ("    _FA=_familias(seed,fam_D,fam_nvar,fam_F,fam_V,n_exc,fam_val,n_neu,exc_evita,vira) if _MF else None"
         "   # rng PROPIO: no toca el del organismo\n")
A_MEM = ("    _MMv=np.zeros((_NP,4)); _MNv=np.zeros((_NP,4)); _MEv=np.full(_NP,1e9); _MGv=0   "
         "# v15f: R CRUDO por casilla, visitas, error propio por celda, ganadora\n")
A_REG = ("    _pb2={}; _sep={}; _en2={}; _vir=(set(_FA['viradas']) if _MF else set())   "
         "# B2: registro (reg_b2). Dicts vacios: no consumen rng ni cambian ninguna decision.\n")
A_PASO = ("        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.\n"
          "        R=0.\n")
A_MORD = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1\n"
A_SEP = "                            if sum(1 for _z in _vh if _z*_wt<=0)>=2: _sep[kk]=_en2[kk]\n"
A_RET = "    return dict(memoria_pares=memoria_pares,mem_alfa=mem_alfa,"

# ---------------------------------------------------------------- texto nuevo (todo lo que b4 anade)
NUEVA_FIRMA = A_FIRMA[:-2] + ",fam_seed=None,exc_fija=None,canal=None,reg_b4=0):"

INIT_CANAL = '''    # ===================== B4: CANAL CON REFERENCIA (bloque 4). Con canal=None NADA de esto corre. =====================
    if canal is not None and not isinstance(canal,dict): raise ValueError(f"canal={canal!r}: se espera None o un dict")   # B4: perilla mal escrita no cae en silencio
    _c4d=(canal or {}); _c4m=_c4d.get('modo'); _c4r=_c4d.get('ref')
    if _c4m not in (None,'emite','inm','sen','mudo'): raise ValueError(f"canal['modo']={_c4m!r}")
    _c4rx=(_c4m in ('inm','sen','mudo'))   # el RECEPTOR ('mudo' = el GEMELO: recibe la visita del canal y NO el mensaje)
    if _c4rx and memoria_pares is None: raise ValueError("canal: el mensaje se escribe en la TABLA DE PARES; con memoria_pares=None no hay donde escribirlo")
    if _c4rx and _c4m in ('sen','mudo') and _c4r not in PAT: raise ValueError(f"canal['ref']={_c4r!r} no es un estimulo de este mundo")
    _P4=(np.asarray(_c4d.get('P'),dtype=float) if _c4rx else None)
    if _c4rx and (_P4 is None or _P4.shape!=(_D,)): raise ValueError(f"canal['P'] debe tener {_D} pixeles")
    _R4=(float(_c4d.get('R',0.0)) if _c4rx else 0.0); _c4t=(int(_c4d.get('t',0)) if _c4rx else None)
    _c4p=_c4rx; _c4te=None; _c4gp=None; _c4gq=None; _c4bn=None; _c4mb=None; _c4em=({} if _c4m=='emite' else None); _nmt=0; _nm4e=0
    def _bin4(_g,_P):   # B4: la casilla (2 bits) que el par ganador _g le asigna al patron _P -- la RESOLUCION de la referencia
        _i4,_j4=_PARv[_g]; return int(_P[_i4])*2+int(_P[_j4])
'''

ENTREGA = '''        if _c4p and t>=_c4t and (_c4m=='inm' or (pos in objs and objs[pos]==_c4r)):   # B4: ENTREGA. 'inm' = en cuanto el emisor aprende; 'sen' = SENALAMIENTO (cuando el receptor esta ante el referente).
            _c4p=False; _c4te=t; _nm4e=_nmt; _c4gp=list(_PARv[_MGv]); _c4bn=_bin4(_MGv,_P4)
            _c4mb=sorted(_n4 for _n4 in PAT if _bin4(_MGv,PAT[_n4])==_c4bn)   # DIAGNOSTICO: quien mas cae en esa casilla (no decide ninguna prediccion)
            if _c4m!='mudo':   # GEMELO del bloque 4: 'mudo' hace TODO lo del canal MENOS escribir el mensaje (como `vira=-8` en b2/b3: declara lo mismo y no cambia nada)
{TABLA}            _c4gq=list(_PARv[_MGv])
'''

EMITE = ('''                _nmt+=1
                if _c4m=='emite' and kk in _vir4 and kk not in _c4em: _c4em[kk]=[t,kk,[float(_z4) for _z4 in PAT[kk]],float(R),int(_enc.get(kk,0))]   # B4: el EMISOR anota su PRIMERA mordida de cada estimulo que el mundo ha marcado (excepcion o virada), con la R CRUDA que recibio -- SIMETRICO: tambien R>0 ("lo que evitabas ya es comida", el caso en el que el receptor solo esta ciego para siempre). SOLO LECTURA: no toca ninguna decision ni el rng.
''')

REG4 = ('''                if reg_b4 and _c4te is not None and t>=_c4te:   # B4: la CONDUCTA de la boca en las 3 primeras exposiciones tras la entrega (nunca pesos: ERR-44)
                    _l4=_pb4.setdefault(kk,[])
                    if len(_l4)<3: _l4.append([t,round(float(_wt),3),_o0,int(bool(_fam(kc))),int(bool(mordio)),round(float(hambre),3),round(float(_ws),3),t-_c4te,_nmt-_nm4e])
''')

RET4 = ("canal=(dict(canal) if canal else None),canal_modo=_c4m,canal_t_msg=_c4t,canal_entregado=bool(_c4te is not None),"
        "canal_t_entrega=_c4te,canal_emitido=(dict(_c4em) if _c4em is not None else None),canal_gan_pre=_c4gp,canal_gan_post=_c4gq,canal_bin=_c4bn,"
        "canal_mismo_bin=_c4mb,primera_b4=(dict(_pb4) if reg_b4 else None),"
        "fam_seed=(None if fam_seed is None else int(fam_seed)),")

CABECERA = '''"""organismo_familias_b4 = organismo_familias_b3.py (bloque 3, v15f + mundo de familias, 62a1e53b452b078e)
+ EL CANAL CON REFERENCIA del BLOQUE 4: dos perillas y nada mas.
  `fam_seed`: semilla del MUNDO separada de la del organismo -> DOS organismos con rng propio EN EL MISMO MUNDO.
  `canal`   : {'modo':'emite'} el emisor ANOTA (solo lectura); {'modo':'sen'|'inm','t','P','R','ref'} el receptor
              RECIBE el mensaje como una EXPOSICION SIN CONSECUENCIA con la valencia recibida: se ejecuta el bloque
              de escritura de la tabla de pares EXTRAIDO LITERALMENTE de b3, con el patron y la valencia del
              mensaje. No toca energia, ni objetos, ni `ncod`, ni la via rapida, ni la plasticidad.
  `reg_b4`  : registro de la conducta de la boca en las 3 primeras exposiciones tras la entrega.
ANCLA DE IDENTIDAD: con canal=None, fam_seed=None y reg_b4=0 es organismo_familias_b3 BIT A BIT (y por su cadena,
b2, organismo_familias, organismo_v14 y organismo_v15f_on); con canal={'modo':'emite'} tambien.
Arnes: identidad_familias_b4.py.  Generado por construye_familias_b4.py. NO editar a mano."""
'''


def main():
    for p, sha in [(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                   (os.path.join(AQUI, 'organismo_familias.py'), SHA_MF),
                   (os.path.join(AQUI, 'organismo_familias_b2.py'), SHA_B2),
                   (os.path.join(AQUI, 'escala_codigo.py'), SHA_ESCALA),
                   (os.path.join(CREA, 'organismo_v15f.py'), SHA_V15F),
                   (os.path.join(CREA, 'organismo_v15f_on.py'), SHA_V15F_ON)]:
        if h16(p) != sha:
            raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado.")

    t = origen(os.path.join(AQUI, 'organismo_familias_b3.py'), SHA_B3)

    # ---------------- CADENA 1: extraer del PROPIO b3 el bloque de escritura de la tabla y dedentarlo
    TAB = trozo(t, X_TAB_A, X_TAB_B, 'escritura de la tabla de pares')
    TAB = dedenta(TAB, 8, 'escritura de la tabla de pares')
    TAB = sust(TAB, "                _Pv=PAT[kk]\n",
               "                _Pv=_P4   # B4: el patron del MENSAJE, no el del objeto mordido\n",
               etiqueta='b4: el patron del mensaje')
    TAB = sust(TAB, "_erv=R-_pv;", "_erv=_R4-_pv;", etiqueta='b4: error con la valencia del mensaje')
    TAB = sust(TAB, "_MMv[_cv,_dv]=R   # SOBRESCRITURA", "_MMv[_cv,_dv]=_R4   # SOBRESCRITURA",
               etiqueta='b4: sobrescritura con la valencia del mensaje')
    TAB = sust(TAB, "_MMv[_cv,_dv]+=mem_alfa*(R-_MMv[_cv,_dv])", "_MMv[_cv,_dv]+=mem_alfa*(_R4-_MMv[_cv,_dv])",
               etiqueta='b4: mezcla con la valencia del mensaje')
    if 'PAT[kk]' in TAB or '=R\n' in TAB or 'R-_pv' in TAB:
        raise SystemExit("CADENA 1: el bloque de entrega sigue leyendo el objeto mordido. Abortado.")
    if not TAB.startswith('                if memoria_pares is not None:'):
        raise SystemExit(f"CADENA 1: sangria inesperada tras dedentar: {TAB[:40]!r}. Abortado.")

    # ---------------- CADENA 2: aplicar sobre el instrumento del bloque 3
    t = CABECERA + t
    t = sust(t, A_FIRMA, NUEVA_FIRMA, etiqueta='firma de run')
    t = sust(t, A_DEF, A_DEF[:-2] + ",exc_fija=None):", etiqueta='firma de _familias')
    t = sust(t, A_WIN, A_WIN + "    if exc_fija is not None: exc_win=['T%dv%d'%(_k,int(exc_fija)) for _k in range(F)]"
                               "   # B4: la excepcion de cada token es una variante FIJA (la RETENIDA por la deriva). "
                               "El sorteo de arriba se hace IGUAL: el rng del mundo no cambia, solo se sobrescribe el resultado.\n",
             etiqueta='exc_fija: la excepcion en una variante fija')
    t = sust(t, A_FAM, A_FAM.replace("_familias(seed,", "_familias((seed if fam_seed is None else int(fam_seed)),")
                            .replace("exc_evita,vira)", "exc_evita,vira,exc_fija)"),
             etiqueta='fam_seed y exc_fija en la llamada al mundo')
    t = sust(t, A_MEM, A_MEM + INIT_CANAL, etiqueta='inicializacion del canal')
    t = sust(t, A_REG, A_REG + "    _pb4={}; _vir4=((set(_FA['exc'])|set(_FA['viradas'])) if _MF else set())   "
                               "# B4: registro (reg_b4) y los estimulos que el MUNDO ha marcado (excepcion o virada), "
                               "de los que el emisor puede hablar. Sin rng y sin efecto en ninguna decision.\n",
             etiqueta='registro del bloque 4')
    t = sust(t, A_PASO, A_PASO + ENTREGA.replace('{TABLA}', TAB), etiqueta='entrega del mensaje')
    t = sust(t, A_MORD, A_MORD + EMITE, etiqueta='emision del mensaje')
    t = sust(t, A_SEP, A_SEP + REG4, etiqueta='conducta tras la entrega')
    t = sust(t, A_RET, "    return dict(" + RET4 + "memoria_pares=memoria_pares,mem_alfa=mem_alfa,",
             etiqueta='diccionario de salida')

    compile(t, DESTINO, 'exec')          # que ni se escriba algo que no compila
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print("  CADENA 1 (extraccion del bloque de escritura de la tabla, del propio b3)  OK: 1 bloque + 4 sustituciones")
    print("  CADENA 2 (aplicacion sobre b3)                                            OK: 10 anclas de linea")
    print(f"  escrito {os.path.relpath(DESTINO, RAIZ)}")
    print(f"  sha origen  organismo_familias_b3.py {SHA_B3}")
    print(f"  sha destino organismo_familias_b4.py {h16(DESTINO)}")
    print("  ahora: python experimentos/nivel12_mundo_familias/identidad_familias_b4.py")


if __name__ == '__main__':
    main()
