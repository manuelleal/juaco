"""Construye experimentos/carrera_fase10/B/organismo_B.py POR ANCLAS desde
experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py (9dd1fb91ecec35ae, que aqui SOLO SE LEE).

Cadena completa, verificada por sha ANTES de escribir nada:
  organismo_f9c 9dd1fb91ecec35ae <- organismo_f9 3a821884394d66c9 <- organismo_alma2 4fd616aeaf535e61
  <- organismo_alma 7c09cec391daa879 <- organismo_vivo_h1 9e99ff87b5e2db1e <- organismo_vivo_rep2
  96feb4918dc5d694 <- organismo_vivo_rep aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825
  <- TRONCO CONGELADO organismo/organismo_v14.py (v14.1) feefc88b1fd8d434.
Ningun archivo existente se toca (regla 1 de EQUIPO.md). Todo lo nuevo vive en experimentos/carrera_fase10/B/.

MISION: llegar a la AGI por este camino. CARRERA A LA FASE 10, BACTERIA B.
Sesgo: LA REPRESENTACION QUE CRECE. El muro medido el 21-sep es el MUNDO (ni el nodo ORACULO cruza
R0 0.90). Aqui el mundo cambia a uno de FAMILIAS x VARIANTES donde la lectura lineal de la retina
NO ALCANZA (una variante por familia VIRA de valencia: es un XOR local que la via lenta no puede
representar), y se mide si la estructura que el linaje hizo crecer se transmite por el nodo.

LAS CINCO PERILLAS NUEVAS (memoria nueva declarada: UN entero por cuerpo, `_gen`; todo lo demas se
calcula de _exph/_mordh en la muerte y se tira)
  retina=0   dimension de la retina. 0 = 6 pixeles = organismo_f9c EXACTO. retina=D usa D pixeles en
             KW, mu, mup, mun, Wps, Wns, Wpe y en la entrada de locomocion (2, D+3).
  mundoB=0   0 = el mundo vivo de 4 estimulos (ABCD), EXACTO. mundoB=F (>=4, par) construye el mundo
             de FAMILIAS x VARIANTES: F familias (one-hot en los pixeles 0..F-1) x F variantes
             (one-hot en F..2F-1) = F*F estimulos compuestos sobre retina=2F pixeles.
             Ejes: las primeras F/2 familias son del eje ENERGIA, las otras F/2 del eje AGUA. Dentro
             de cada eje, todas las familias menos la ultima tienen base BUENA (comida / agua) y la
             ultima base MALA (veneno / sal).
  vira=1     1 = en cada familia UNA variante (sorteada por semilla con rng PROPIO 880000+1e6*seed)
             invierte la valencia de su familia (comida<->veneno, agua<->sal). Es la TRAMPA: el
             valor NO es lineal en los pixeles, hace falta la celda del par. vira=0 = MUNDO LLANO
             (control que puede fallar: ahi la via lenta basta y el crecimiento no deberia pagar).
  cambia_en=0  CAMBIO NO AVISADO: cada `cambia_en` pasos se re-sortea la variante que vira en cada
             familia (mismo rng propio del mundo; no toca el rng del organismo).
  bB=0       SOLO LECTURA: por cuerpo que muere -- generacion, combinaciones DISTINTAS mordidas con
             R>0, combinaciones distintas encontradas, combinaciones malas distintas rechazadas,
             celdas activas y splits acumulados. Detras de f9=1, como p1/c1.

Y UNA EXTENSION DE UNA PERILLA QUE YA EXISTIA:
  nodo_via=3 EL CANDIDATO DE B. Es nodo_via=2 (leer llena la via rapida y NO abre la puerta, el
             candidato DECLARADO de la fase 9 bloque 2) MAS la plasticidad y la DIVISION POR
             CONFLICTO DE SIGNO de v11 con hija dispersa: LEER HACE CRECER LA ESTRUCTURA.
             organismo_f9c dice literalmente "LEER NO DIVIDE ... Declarado"; esto es exactamente esa
             linea, invertida, y nada mas. No toca ncod (la puerta sigue siendo de las mordidas
             propias), ni la energia, ni los objetos, ni el rng del mundo.

ANCLA DE IDENTIDAD: con retina=0, mundoB=0, cambia_en=0, bB=0 y nodo_via in (0,1,2) es
organismo_f9c BIT A BIT (y por su cadena, f9, alma2, alma, vivo_h1, vivo y el TRONCO v14.1).
Arnes: identidad_B.py.

Uso:  python experimentos/carrera_fase10/B/construye_B.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
B2 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2')

ORIGEN = os.path.join(B2, 'organismo_f9c.py')
DESTINO = os.path.join(AQUI, 'organismo_B.py')
CADENA = {
    'organismo/organismo_v14.py': 'feefc88b1fd8d434',
    'experimentos/nivel11_mundo_vivo/organismo_vivo.py': '20c0961c79de8825',
    'experimentos/nivel11_mundo_vivo/organismo_vivo_rep.py': 'aa823d56c2d4213c',
    'experimentos/nivel11_mundo_vivo/organismo_vivo_rep2.py': '96feb4918dc5d694',
    'experimentos/nivel11_mundo_vivo/organismo_vivo_h1.py': '9e99ff87b5e2db1e',
    'experimentos/nivel13_alma/organismo_alma.py': '7c09cec391daa879',
    'experimentos/nivel13_alma/organismo_alma2.py': '4fd616aeaf535e61',
    'experimentos/nivel09_cuerpo_nuevo/organismo_f9.py': '3a821884394d66c9',
    'experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py': '9dd1fb91ecec35ae',
}


def sha(ruta):
    return hashlib.sha256(open(ruta, 'rb').read()).hexdigest()[:16]


def sust(txt, viejo, nuevo, etiqueta):
    n = txt.count(viejo)
    if n != 1:
        raise SystemExit(f'ANCLA {etiqueta}: aparece {n} veces (se exige 1). Se aborta sin escribir nada.')
    return txt.replace(viejo, nuevo)


# ------------------------------------------------------------------ 0. tripwire de shas
for rel, esperado in CADENA.items():
    ruta = os.path.join(RAIZ, rel)
    real = sha(ruta)
    if real != esperado:
        raise SystemExit(f'TRIPWIRE: {rel} tiene sha {real}, se esperaba {esperado}. Se aborta.')
print('tripwire de la cadena: OK (%d archivos)' % len(CADENA))

txt = open(ORIGEN, encoding='utf-8').read()

# ------------------------------------------------------------------ 1. cabecera
A_CAB = '"""organismo_f9c.py — GENERADO POR construye_f9c.py DESDE organismo_f9.py (3a821884394d66c9),\n'
N_CAB = ('"""organismo_B.py — GENERADO POR construye_B.py DESDE organismo_f9c.py (9dd1fb91ecec35ae).\n'
         'CARRERA A LA FASE 10, BACTERIA B. Con retina=0, mundoB=0, cambia_en=0, bB=0 y nodo_via in (0,1,2)\n'
         'es organismo_f9c BIT A BIT (arnes identidad_B.py). Perillas nuevas:\n'
         '  retina=D    -> la retina tiene D pixeles (0 = 6 = v14 EXACTO)\n'
         '  mundoB=F    -> MUNDO DE FAMILIAS x VARIANTES: F familias x F variantes = F*F estimulos, retina=2F\n'
         '  vira=1      -> en cada familia una variante INVIERTE la valencia (la trampa que la via lenta no ve)\n'
         '  cambia_en   -> cambio no avisado: re-sorteo periodico de la variante que vira\n'
         '  bB=1        -> medidas por cuerpo para la acumulacion (generacion, combinaciones)\n'
         '  nodo_via=3  -> LEER HACE CRECER: nodo_via=2 + plasticidad y division por conflicto de signo\n'
         'NO editar a mano.\n'
         'ORIGINAL organismo_f9c.py — GENERADO POR construye_f9c.py DESDE organismo_f9.py (3a821884394d66c9),\n')
txt = sust(txt, A_CAB, N_CAB, 'cabecera')

# ------------------------------------------------------------------ 2. alias de los objetos del mundo de 4 estimulos
A_ALIAS = "EFECTO={'comida':(+0.8,0.0),'veneno':(-0.4,0.0),'agua':(0.0,+0.8),'sal':(0.0,-0.4)}   # (dE, dAgua) nominal\n"
N_ALIAS = (A_ALIAS +
           "PAT0=PAT; VAL_VIVO0=VAL_VIVO; EFECTO0=EFECTO   # B: alias del mundo de 4 estimulos. run() hace copias LOCALES\n"
           "#    (con mundoB=0 son exactamente estos dicts: identidad bit a bit) y con mundoB=F las reemplaza por el\n"
           "#    mundo de familias x variantes. Nada de aqui se muta nunca.\n")
txt = sust(txt, A_ALIAS, N_ALIAS, 'alias del mundo')

# ------------------------------------------------------------------ 3. firma
A_FIRMA = ",rep_acum=0,f9=0,nodo_via=0,nodo_or=0,sesgo_fijo=0.0,f9c=0):"
N_FIRMA = ",rep_acum=0,f9=0,nodo_via=0,nodo_or=0,sesgo_fijo=0.0,f9c=0,retina=0,mundoB=0,vira=1,cambia_en=0,bB=0):"
txt = sust(txt, A_FIRMA, N_FIRMA, 'firma')

# ------------------------------------------------------------------ 4. guardas
A_G = ("    if nodo_via not in (0,1,2): raise SystemExit('F9C: nodo_via es 0 (solo la via lenta = organismo_f9), "
       "1 (las DOS vias CON evidencia = organismo_f9b) o 2 (las dos vias SIN evidencia: leer llena la memoria, "
       "morder abre la puerta)')\n")
N_G = ("    if nodo_via not in (0,1,2,3): raise SystemExit('F9C/B: nodo_via es 0 (solo la via lenta = organismo_f9), "
       "1 (las DOS vias CON evidencia = organismo_f9b), 2 (las dos vias SIN evidencia: leer llena la memoria, morder "
       "abre la puerta = organismo_f9c) o 3 (como 2 y ademas LEER HACE CRECER: plasticidad y division por conflicto)')\n"
       "    if not f9: bB=0   # B: las medidas por cuerpo viven en el dict f9 (solo lectura, detras de f9), como p1/c1\n"
       "    if mundoB and not vivo: raise SystemExit('B: mundoB exige vivo=1 (la mordida debe tener consecuencia vectorial)')\n"
       "    if mundoB and n_nec!=2: raise SystemExit('B: mundoB exige n_nec=2 (dos ejes: energia y agua)')\n"
       "    if mundoB and (mundoB<4 or mundoB%2): raise SystemExit('B: mundoB=F exige F par y >=4 (F/2 familias por eje)')\n"
       "    if mundoB and retina!=2*mundoB: raise SystemExit('B: mundoB=F exige retina=2*F (F pixeles de familia + F de variante)')\n"
       "    if mundoB and estims is not None: raise SystemExit('B: mundoB construye sus propios estimulos (estims debe ser None)')\n"
       "    if mundoB and (nuevo is not None or invertir_en is not None or solap_AB or solap_B is not None): raise SystemExit('B: mundoB es incompatible con nuevo/invertir_en/solap (el cambio del mundo es cambia_en)')\n"
       "    if cambia_en and not mundoB: raise SystemExit('B: cambia_en exige mundoB (no hay variante que virar)')\n"
       "    if not mundoB: vira=1   # B: inerte fuera del mundo de familias (no aparece en la salida)\n")
txt = sust(txt, A_G, N_G, 'guardas')

# ------------------------------------------------------------------ 5. D y la construccion del mundo B (antes del rng del mundo)
A_RNG = "    rng=np.random.default_rng(seed)\n"
N_RNG = ("    D=6 if not retina else int(retina)   # B: dimension de la retina (retina=0 -> 6 = v14 EXACTO)\n"
         "    PAT=dict(PAT0); VAL_VIVO=dict(VAL_VIVO0); EFECTO=dict(EFECTO0)   # B: copias LOCALES (con mundoB=0, los mismos dicts)\n"
         "    _F=int(mundoB); _rB=None; _virv=[]; _baseB=[]; _opB={'comida':'veneno','veneno':'comida','agua':'sal','sal':'agua'}\n"
         "    if mundoB:   # B: EL MUNDO DE FAMILIAS x VARIANTES. F familias (one-hot 0..F-1) x F variantes (one-hot F..2F-1).\n"
         "        #   Ejes: familias 0..F/2-1 = ENERGIA, F/2..F-1 = AGUA. En cada eje, la ULTIMA familia tiene base MALA.\n"
         "        #   `vira`: en cada familia UNA variante invierte la valencia -> el valor NO es lineal en los pixeles.\n"
         "        #   rng PROPIO del mundo (ERR-60): no toca el rng del organismo, ni el de los hijos, ni ninguno de los controles.\n"
         "        _rB=np.random.default_rng(880000+1000000*seed); _H=_F//2\n"
         "        _baseB=[('veneno' if _f==_H-1 else 'comida') if _f<_H else ('sal' if _f==_F-1 else 'agua') for _f in range(_F)]\n"
         "        _virv=[int(_rB.integers(_F)) for _f in range(_F)]\n"
         "        PAT={}; VAL_VIVO={}\n"
         "        for _f in range(_F):\n"
         "            for _v in range(_F):\n"
         "                _P0=np.zeros(D); _P0[_f]=1.; _P0[_F+_v]=1.\n"
         "                PAT['f%dv%d'%(_f,_v)]=_P0\n"
         "                VAL_VIVO['f%dv%d'%(_f,_v)]=(_opB[_baseB[_f]] if (vira and _v==_virv[_f]) else _baseB[_f])\n"
         "    rng=np.random.default_rng(seed)\n")
txt = sust(txt, A_RNG, N_RNG, 'D y mundo B')

# ------------------------------------------------------------------ 6. dimensiones (D en lugar de 6 / D+3 en lugar de 9)
DIMS = [
    ("    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True\n",
     "    Wl=rng.uniform(.1,.4,(2,D+3)); KW=np.zeros((NKMAX,D)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,D)); activa[:NK]=True\n",
     'dim Wl/KW'),
    ("    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))\n",
     "    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,D))\n",
     'dim cond fundador'),
    ("mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)\n",
     "mu=np.zeros((NKMAX,D)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(D+3)\n",
     'dim mu/tr'),
    ("    Wps=np.zeros((n_nec,6)); Wns=np.zeros((n_nec,6))   # v13:",
     "    Wps=np.zeros((n_nec,D)); Wns=np.zeros((n_nec,D))   # v13:",
     'dim via lenta'),
    ("    Wpe=np.zeros((n_nec,6)); Wke=np.zeros((n_nec,NKMAX));",
     "    Wpe=np.zeros((n_nec,D)); Wke=np.zeros((n_nec,NKMAX));",
     'dim predictor'),
    ("    mup=np.zeros((NKMAX,6)); mun=np.zeros((NKMAX,6)); zp=np.zeros(NKMAX);",
     "    mup=np.zeros((NKMAX,D)); mun=np.zeros((NKMAX,D)); zp=np.zeros(NKMAX);",
     'dim medias condicionadas'),
    ("        Wl[:]=_rh.uniform(.1,.4,(2,9)); el[:]=0; tr[:]=0   #",
     "        Wl[:]=_rh.uniform(.1,.4,(2,D+3)); el[:]=0; tr[:]=0   #",
     'dim Wl del hijo'),
    ("            KW[:]=0; activa[:]=False; KW[:NK]=_rh.uniform(0,1,(NK,6)); activa[:NK]=True\n",
     "            KW[:]=0; activa[:]=False; KW[:NK]=_rh.uniform(0,1,(NK,D)); activa[:NK]=True\n",
     'dim KW del hijo'),
    ("            while not cond(): KW[objetivo_AB:NK]=_rh.uniform(0,1,(NK-objetivo_AB,6))\n",
     "            while not cond(): KW[objetivo_AB:NK]=_rh.uniform(0,1,(NK-objetivo_AB,D))\n",
     'dim cond del hijo'),
    ("                _pm=_rb.permutation(6); _nbar+=int(bool((_pm==np.arange(6)).all()))",
     "                _pm=_rb.permutation(D); _nbar+=int(bool((_pm==np.arange(D)).all()))",
     'dim baraja de pixeles'),
]
for a, n, et in DIMS:
    txt = sust(txt, a, n, et)

# ------------------------------------------------------------------ 7. cond: con mundoB no hay restriccion de solapamiento A/B
A_COND = "    cond=lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and ("
N_COND = "    cond=lambda: bool(mundoB) or len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and ("
txt = sust(txt, A_COND, N_COND, 'cond con mundoB')

# ------------------------------------------------------------------ 8. tablas de solo lectura anchas como PAT
A_BX = "    _mnec=[0,0]; _bxor=[[0]*4 for _ in range(n_nec)]; _exor=[[0]*4 for _ in range(n_nec)]   # VIVO:"
N_BX = "    _mnec=[0,0]; _bxor=[[0]*len(PAT) for _ in range(n_nec)]; _exor=[[0]*len(PAT) for _ in range(n_nec)]   # VIVO:"
txt = sust(txt, A_BX, N_BX, 'ancho de xor_mord/xor_enc')

A_IDX = "    _IDX={_k2:_i2 for _i2,_k2 in enumerate('ABCD')}\n"
N_IDX = "    _IDX={_k2:_i2 for _i2,_k2 in enumerate(PAT)}   # B: con mundoB=0, PAT es A,B,C,D en ese orden (identico)\n"
txt = sust(txt, A_IDX, N_IDX, 'indice de estimulos')

# ------------------------------------------------------------------ 9. estado nuevo (solo lectura) + generacion
A_EST = ("    _p1=[]; _c1=[]; _tok=[]; _ncu=[]   # F9: por cuerpo que muere -- rechazo lo malo a la 1a / mordio lo bueno "
         "a la 1a / pasos hasta la 1a mordida con R>0 / estaba conectado. SOLO LECTURA (-1 = no hubo ocasion)\n")
N_EST = (A_EST +
         "    _gen=0; _sdiv=0; _gb=[]; _okb=[]; _enb=[]; _rmb=[]; _celb=[]; _spb=[]   # B: LA UNICA MEMORIA NUEVA es `_gen`,\n"
         "    #    un entero por cuerpo (0 = fundador; el hijo hereda gen+1 por la cola, que ya existia). Lo demas es SOLO\n"
         "    #    LECTURA y se calcula de _exph/_mordh en la muerte, como p1/c1: divisiones disparadas AL LEER, y por cuerpo\n"
         "    #    la generacion, las combinaciones DISTINTAS mordidas con R>0, las encontradas, las malas rechazadas,\n"
         "    #    las celdas activas y los splits acumulados.\n")
txt = sust(txt, A_EST, N_EST, 'estado B')

# ------------------------------------------------------------------ 10. la generacion viaja en la cola que ya existia
A_SNAP = "    def _snap():   # H1: la memoria que se lleva el hijo, congelada EN EL MOMENTO DEL PARTO (no en la muerte del padre)\n        _m={'dote':dote}\n"
N_SNAP = ("    def _snap():   # H1: la memoria que se lleva el hijo, congelada EN EL MOMENTO DEL PARTO (no en la muerte del padre)\n"
          "        _m={'dote':dote,'gen':_gen+1}   # B: la GENERACION viaja en la cola que ya existia (un entero; no cambia ningun numero)\n")
txt = sust(txt, A_SNAP, N_SNAP, 'generacion en el snapshot')

A_NL = "        nonlocal E,Ag,_prev_on,_nbar\n"
N_NL = "        nonlocal E,Ag,_prev_on,_nbar,_gen\n        _gen=(int(_m['gen']) if (_m is not None and 'gen' in _m) else 0)   # B: fundador -> 0\n"
txt = sust(txt, A_NL, N_NL, 'generacion al nacer')

# ------------------------------------------------------------------ 11. tipos: con mundoB, todos los estimulos
A_TIPOS = "    tipos=(list(estims) if estims else ['A','B'])   # VIVO:"
N_TIPOS = "    tipos=(list(PAT) if mundoB else (list(estims) if estims else ['A','B']))   # B/VIVO:"
txt = sust(txt, A_TIPOS, N_TIPOS, 'tipos del mundo')

# ------------------------------------------------------------------ 12. cambio no avisado
A_INV = "        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}\n"
N_INV = (A_INV +
         "        if cambia_en and t and t%cambia_en==0:   # B: CAMBIO NO AVISADO. Se re-sortea la variante que vira en CADA familia,\n"
         "            #   con el rng PROPIO del mundo (no toca el del organismo). Nadie avisa: el cuerpo lo descubre mordiendo.\n"
         "            for _fb in range(_F): _virv[_fb]=int(_rB.integers(_F))\n"
         "            for _fb in range(_F):\n"
         "                for _vb in range(_F): val['f%dv%d'%(_fb,_vb)]=(_opB[_baseB[_fb]] if (vira and _vb==_virv[_fb]) else _baseB[_fb])\n")
txt = sust(txt, A_INV, N_INV, 'cambio no avisado')

# ------------------------------------------------------------------ 13. p1/c1 generalizados (identicos en el mundo de ABCD)
A_P1 = ("                    _mal9=[_x9 for _x9 in _exph if _x9[1]==('B' if _x9[2]==0 else 'D')]\n"
        "                    _bue9=[_x9 for _x9 in _exph if _x9[1]==('A' if _x9[2]==0 else 'C')]\n")
N_P1 = ("                    _mal9=[_x9 for _x9 in _exph if _x9[2]<2 and _EF[val[_x9[1]]][_x9[2]]<0]   # B: generalizado. En el mundo\n"
        "                    _bue9=[_x9 for _x9 in _exph if _x9[2]<2 and _EF[val[_x9[1]]][_x9[2]]>0]   #    de ABCD es EXACTAMENTE B/D y A/C\n")
txt = sust(txt, A_P1, N_P1, 'p1/c1 generalizados')

# ------------------------------------------------------------------ 14. medidas por cuerpo (acumulacion)
A_NCU = "                    _ncu.append(int(_con))\n"
N_NCU = (A_NCU +
         "                    if bB:   # B: LAS MEDIDAS DE LA ACUMULACION, de _exph/_mordh ANTES de limpiarlas. Todo SOLO LECTURA.\n"
         "                        _gb.append(int(_gen)); _celb.append(int(activa.sum())); _spb.append(int(splits))\n"
         "                        _okb.append(len({_x9[1] for _x9 in _mordh if _x9[3]>0}))   # combinaciones DISTINTAS que este cuerpo EXPLOTO\n"
         "                        _enb.append(len({_x9[1] for _x9 in _exph}))                # combinaciones DISTINTAS que se le presentaron\n"
         "                        _rmb.append(len({_x9[1] for _x9 in _exph if _x9[2]<2 and _EF[val[_x9[1]]][_x9[2]]<0 and not _x9[3]}))\n")
txt = sust(txt, A_NCU, N_NCU, 'medidas por cuerpo')

# ------------------------------------------------------------------ 15. oraculo y testigo de la puerta, generalizados
A_OR = "for _n9 in range(min(n_nec,2)) for _k9 in 'ABCD']\n"
N_OR = "for _n9 in range(min(n_nec,2)) for _k9 in PAT]   # B: generalizado (con mundoB=0, 'ABCD' exacto)\n"
txt = sust(txt, A_OR, N_OR, 'tabla del oraculo')

A_ORM = "                        _msg=_or9*max(1,nodo_lee)   # 8*nodo_lee = 400 mensajes con nodo_lee=50:"
N_ORM = ("                        _msg=_or9*max(1,(8*nodo_lee)//len(_or9))   # B: el pool del oraculo es ~8x el presupuesto de lectura\n"
         "                        #        (con el mundo de ABCD len(_or9)=8 -> (8*50)//8 = 50 copias: EXACTAMENTE el 400 de f9c).\n"
         "                        #        ORIGINAL: 8*nodo_lee = 400 mensajes con nodo_lee=50:")
txt = sust(txt, A_ORM, N_ORM, 'pool del oraculo')

A_FAM9 = "                    if nodo_via: _fam9.append(int(sum(int(_fam(kenyon(PAT[_z9]),_nm)) for _z9 in 'ABCD')))"
N_FAM9 = "                    if nodo_via: _fam9.append(int(sum(int(_fam(kenyon(PAT[_z9]),_nm)) for _z9 in PAT)))"
txt = sust(txt, A_FAM9, N_FAM9, 'testigo de la puerta')

# ------------------------------------------------------------------ 16. EL CANDIDATO: leer hace crecer
A_DF7 = "                            _df7=_R7-float((Wp[_n7]-Wn[_n7])@_kc7)   # con puerta, cada via aprende de SU error (v13)\n"
N_DF7 = ("                            _Wb7=Wp[_n7]-Wn[_n7]; _df7=_R7-float(_Wb7@_kc7)   # B: el valor ANTES de actualizar (como en la mordida).\n"
         "                            #        Con puerta, cada via aprende de SU error (v13)\n")
txt = sust(txt, A_DF7, N_DF7, 'Wb antes de actualizar')

A_NVIA = ("                            _nvia+=1   # LEER NO DIVIDE: div_signo no se dispara al leer (un mensaje nunca parte una casilla). Declarado.\n")
N_NVIA = ("                            _nvia+=1   # nodo_via 1 y 2: LEER NO DIVIDE (organismo_f9b / organismo_f9c EXACTOS). Declarado alli.\n"
          "                            if nodo_via==3 and plast:   # B: LEER HACE CRECER LA ESTRUCTURA. La MISMA regla local de la mordida\n"
          "                                #   (v11: division por conflicto de signo, hija ciega a lo irrelevante, madre fija, fision del valor),\n"
          "                                #   con el MENSAJE en lugar del bocado. NO toca ncod (la puerta la siguen abriendo las mordidas propias),\n"
          "                                #   ni la energia, ni los objetos, ni la posicion, ni el rng del mundo. MEMORIA NUEVA: CERO.\n"
          "                                _idx7=np.where(_ix7)[0]; err[_idx7]=(1-ema)*err[_idx7]+ema*abs(_df7); mu[_idx7]=(1-ema)*mu[_idx7]+ema*_Pv\n"
          "                                if _R7>0: mup[_idx7]=(1-ema_c)*mup[_idx7]+ema_c*_Pv; zp[_idx7]=(1-ema_c)*zp[_idx7]+ema_c\n"
          "                                elif _R7<0: mun[_idx7]=(1-ema_c)*mun[_idx7]+ema_c*_Pv; zn[_idx7]=(1-ema_c)*zn[_idx7]+ema_c\n"
          "                                err_max=max(err_max,float(err[_idx7].max()))\n"
          "                                if div_signo:\n"
          "                                    for _c7 in _idx7:\n"
          "                                        _dst7=_Pv-(mu[_c7]*(_Pv.sum()/max(float(mu[_c7].sum()),1e-9)) if mu_norm else mu[_c7])\n"
          "                                        if mask_rel==2 and zp[_c7]>1e-6 and zn[_c7]>1e-6:\n"
          "                                            _mp7=mup[_c7]/float(zp[_c7]); _mn7=mun[_c7]/float(zn[_c7])\n"
          "                                            _rl7=(_Pv>0)&((np.abs(_mp7-_mn7)>del_s)|(np.minimum(_mp7,_mn7)>1.0-del_c))\n"
          "                                        else: _rl7=(_Pv>0)\n"
          "                                        _kj7=np.clip(KW[_c7]*(1-0.05)+paso*_dst7,0,5)*_rl7\n"
          "                                        if _Wb7[_c7]*_R7<0 and abs(float(_Wb7[_c7]))>0.2 and float(_kj7@_Pv)>float(KW[_c7]@_Pv) and (~activa).any():\n"
          "                                            _j7=int(np.where(~activa)[0][0]); activa[_j7]=True; KW[_j7]=_kj7\n"
          "                                            if _R7>0: Wp[_n7,_j7]=Wp[_n7,_c7]; Wn[_n7,_j7]=0.; Wp[_n7,_c7]=0.\n"
          "                                            else:     Wn[_n7,_j7]=Wn[_n7,_c7]; Wp[_n7,_j7]=0.; Wn[_n7,_c7]=0.\n"
          "                                            if n_nec>1 and hereda_nec:\n"
          "                                                for _nn7 in range(n_nec):\n"
          "                                                    if _nn7!=_n7: Wp[_nn7,_j7]=Wp[_nn7,_c7]; Wn[_nn7,_j7]=Wn[_nn7,_c7]\n"
          "                                            mu[_j7]=_Pv*(float(mu[_c7].sum())/_Pv.sum()); err[_c7]=err[_j7]=0; splits+=1; _sdiv+=1\n"
          "                                            mup[_j7]=mup[_c7].copy(); mun[_j7]=mun[_c7].copy(); zp[_j7]=zp[_c7]; zn[_j7]=zn[_c7]\n")
txt = sust(txt, A_NVIA, N_NVIA, 'leer hace crecer')

# ------------------------------------------------------------------ 17. solapamiento de salida (con mundoB no existe 'A')
A_SOL = "    solap={'AB':len(code(PAT['A'])&code(PAT['B'])),"
N_SOL = "    solap={'AB':(0 if mundoB else len(code(PAT['A'])&code(PAT['B']))),"
txt = sust(txt, A_SOL, N_SOL, 'solapamiento de salida')

# ------------------------------------------------------------------ 18. salida: claves nuevas SOLO con las perillas encendidas
A_OUT = "    if sesgo_fijo: _ext.update(sesgo_fijo=float(sesgo_fijo))   # F9C: eco de configuracion SOLO con el empujon encendido\n"
N_OUT = (A_OUT +
         "    if mundoB: _ext.update(mundoB=dict(F=_F,retina=D,vira=int(vira),cambia_en=int(cambia_en),\n"
         "                       familias=[str(_z) for _z in _baseB],virante=[int(_z) for _z in _virv],\n"
         "                       n_estim=len(PAT),sem_mundo='880000+1000000*seed'))   # B: eco SOLO con el mundo de familias\n"
         "    if retina: _ext.update(retina=int(D))   # B: eco SOLO con la retina cambiada\n"
         "    if alma is not None and f9 and nodo_via==3: _ext['f9'].update(div_lectura=int(_sdiv))   # B: divisiones disparadas AL LEER (ERR-38)\n"
         "    if alma is not None and f9 and bB: _ext['f9'].update(gen=[int(_z) for _z in _gb],comb_ok=[int(_z) for _z in _okb],\n"
         "                       comb_enc=[int(_z) for _z in _enb],rech_mal=[int(_z) for _z in _rmb],\n"
         "                       celdas_cuerpo=[int(_z) for _z in _celb],splits_cuerpo=[int(_z) for _z in _spb])   # B: SOLO LECTURA\n")
txt = sust(txt, A_OUT, N_OUT, 'salida B')

# ------------------------------------------------------------------ 19. el rng del mundo no se toca (regex, como en f9/f9c)
NUEVO = [n for _a, n, _e in DIMS] + [N_G, N_RNG, N_INV, N_NVIA, N_NCU, N_OUT, N_OR, N_ORM]
for bloque in (N_NVIA, N_NCU, N_OUT, N_P1, N_FAM9):
    if re.search(r'(?<![_\w])rng\.', bloque):
        raise SystemExit('SEGURIDAD: un bloque insertado consume el rng DEL MUNDO. Se aborta.')
if 'rng.' in N_INV.replace('_rB.', ''):
    raise SystemExit('SEGURIDAD: el cambio no avisado consume el rng DEL MUNDO. Se aborta.')

open(DESTINO, 'w', encoding='utf-8').write(txt)
print('escrito %s  sha %s  (%d lineas)' % (os.path.relpath(DESTINO, RAIZ), sha(DESTINO), txt.count('\n') + 1))
print('siguiente: python experimentos/carrera_fase10/B/identidad_B.py')
