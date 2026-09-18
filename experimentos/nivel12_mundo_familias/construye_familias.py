"""Construye experimentos/nivel12_mundo_familias/organismo_familias.py POR ANCLAS desde el TRONCO CONGELADO
organismo/organismo_v14.py (v14.1, feefc88b1fd8d434), que aqui SOLO SE LEE (regla 1 de EQUIPO.md; manifiesto.py).

BLOQUE 1 — EL MUNDO QUE OBLIGA A REPRESENTAR (PREREGISTRO_bloque1_familias.md). NO hay organo nuevo: lo unico que
se construye es un MUNDO, y lo unico que se mide es v14.1 tal cual dentro de el.

  MUNDO DE FAMILIAS   retina D = 12 = 9 pixeles de FORMA + 3 de VARIABLE; F = 8 tokens de peso 3 sobre la forma;
                      V = 3 variantes por token (token + 1 pixel de variable) -> 32 estimulos.
  LA VARIANTE ES EL TOKEN   val[Tk vj] = val[Tk] (comida/veneno alternando por token, 4 y 4).
  EXCEPCION           una variante por token es CANDIDATA (exc_win, sorteada SIEMPRE); las n_exc primeras invierten
                      su valencia. Con n_exc=4: T0..T3 -> 2 familias de comida ("sal rosa que envenena") y 2 de veneno.
                      exc_win se sortea tambien con n_exc=0 para que el mundo `lineal` tenga LA MISMA ventana de medida.
  DERIVA              presentes = los F tokens + UNA variante por token, la (t//deriva) mod V. Sin sorteo.
  CAMBIO DE FAMILIA   en T/2 la familia T0 se invierte; su EXCEPCION conserva su valencia absoluta.
  RENOVACION SIMETRICA  renov=1.0: un objeto RECHAZADO desaparece exactamente igual que uno mordido (DIAG_mundo
                      bloqueo 3, trampa 3: hoy el veneno se encuentra 6.3x-23x mas que la comida). renov=0.0 = v14.1.
  n_neu               tokens NEUTROS (valencia 'nada': dE=0 -> R=0). Es el unico regimen donde B-5 tiene disparador.
  B-5 (desambiguar)   compuesto AQUI con las anclas LITERALES de experimentos/creacion_B/construye_codigo.py
                      (f94aa0a2f714c28d), importadas, no copiadas (ERR-38).

ANCLA DE IDENTIDAD (la exigencia central del encargo): con mundo='AB' esto es organismo_v14 BIT A BIT, mismo consumo
del rng y MISMAS CLAVES DE SALIDA (el dict del mundo de familias se agrega SOLO si mundo!='AB'). Se logra asi:
  (1) NINGUNA linea nueva consume el rng del organismo. El mundo entero se construye con un rng PROPIO
      (default_rng(50000 + seed), el SEMILLA_MUNDO del bloque 0) que solo se crea si mundo!='AB'.
  (2) NK, NKMAX, K, L y PAT entran como VALORES POR DEFECTO DE LA FIRMA (evaluados en el ambito del modulo al definir
      run), no como asignaciones a globales: por defecto SON las constantes del tronco, no copias. Dentro de run se
      sombrean con los parametros, asi que con los defaults las expresiones son las mismas y los dobles IEEE tambien.
  (3) Todo lo que agrega el mundo vive detras de `if _MF:` con _MF = (mundo != 'AB'), o es una sustitucion 6 -> _D /
      9 -> _D+3 que con la retina de 6 px es literalmente el mismo literal.
  (4) cond() del tronco se conserva TAL CUAL con mundo='AB'; con el mundo de familias no hay rechazo (PAT['A'] no
      existe), que es la misma decision -y por la misma razon- que tomo escala_codigo.kw_del_tronco (bloque 0).
El arnes identidad_familias.py lo comprueba en 43 comprobaciones + 3 de diagnostico.

EL CATALOGO NO SE REIMPLEMENTA: se toma de escala_codigo.catalogo (bloque 0, d8b8566bca77a0ae), cuyas constantes y
orden de sorteo se verifican por ancla literal aqui. Asi el mundo de la semilla s es EL MISMO sobre el que el bloque 0
calculo el alias, y escala_codigo.kw_del_tronco(s, NK, D) reproduce bit a bit el KW inicial del instrumento.

Uso:  python experimentos/nivel12_mundo_familias/construye_familias.py     (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
# organismo/ PRIMERO en sys.path (ERR-28), sin excepcion, aunque aqui el tronco solo se lea como texto.
sys.path[:0] = [AQUI, CREB, os.path.join(RAIZ, 'organismo')]

SHA_V14 = 'feefc88b1fd8d434'          # organismo/organismo_v14.py = v14.1 (TRONCO CONGELADO)
SHA_CODIGO = 'f94aa0a2f714c28d'       # experimentos/creacion_B/construye_codigo.py (anclas de B-5)
SHA_ESCALA = 'd8b8566bca77a0ae'       # experimentos/nivel12_mundo_familias/escala_codigo.py (bloque 0: catalogo + KW)
SHA_CAPD = '0dbd2449f4bf0901'         # experimentos/capacidad_grande/construye_capD.py (retina D)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado (no se escribe nada).")
    return open(p, encoding='utf-8').read()


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:70]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def exige(texto, ancla, n, etiqueta):
    c = texto.count(ancla)
    if c != n:
        raise SystemExit(f"ANCLA DE LECTURA {etiqueta}: aparece {c} veces, se esperaban {n}. Abortado.")


# ===================== ANCLAS (copiadas literalmente de organismo/organismo_v14.py, tras aplicar B-5) =====================
A_IMPORT = "import numpy as np\n"
A_TABLAS = "R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}"
A_FIRMA = "puerta_pat=5,pat_shuf=0,pat_min=1,desambiguar=0):"          # <- ya con la perilla de B-5
A_RNG = "    rng=np.random.default_rng(seed)\n"
A_COND = ("    cond=lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and (nuevo is None or solap_B is None or "
          "(len(code(PAT[nuevo])&code(PAT['B']))==solap_B and len(code(PAT[nuevo])&code(PAT['A']))==0))\n")
A_WHILE = "    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))\n"
A_MU = "mu=np.zeros((NKMAX,6))"
A_MUPN = "mup=np.zeros((NKMAX,6)); mun=np.zeros((NKMAX,6))"
A_TR = "tr=np.zeros(9)"
A_LENTA = "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)\n"
A_POS = "    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}\n"
A_SOBRE = ("    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; "
           "sin_objetivo=[0]*4   # v9: lectura\n")
A_TIPOS = "    tipos=['A','B']\n"
A_INVERT = "        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}\n"
A_LLEG = "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
A_RECH = ("            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> "
          "no es objetivo por un tiempo\n")
A_MORD = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1\n"
A_LOG = "        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(PAT[k]),2) for k in 'ABCD'))\n"
A_SOLAP = ("                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) "
           "if nuevo else None},")
A_RET = "    return dict(desambiguar=desambiguar,"                     # <- ya con B-5 aplicado
A_RETFIN = "W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns])"

# --------------------------------------------------------------- el mundo (funcion de modulo, rng PROPIO)
MUNDO = '''

# ============================= MUNDO DE FAMILIAS (bloque 1, nivel 12) =============================
R_VAL['nada']=0.0; E_VAL['nada']=0.0   # FAMILIAS: valencia NEUTRA (R==0): el estimulo que NO informa. Con mundo='AB' nunca se usa.

def _familias(seed,D,n_var,F,V,n_exc,fam_val,n_neu):
    """Construye el mundo con un rng PROPIO (default_rng(SEMILLA_MUNDO+seed) dentro de escala_codigo.catalogo):
    NUNCA toca el rng del organismo, asi que con mundo='AB' el flujo aleatorio es el de v14.1 bit a bit.
    El CATALOGO no se reimplementa: es escala_codigo.catalogo (bloque 0), asi que el mundo de la semilla s es EL
    MISMO sobre el que el bloque 0 calculo el alias (PREREGISTRO_bloque1_familias.md 2.1 y 2.6)."""
    import escala_codigo as _EC                      # import perezoso: con mundo='AB' esta linea NUNCA se ejecuta
    _P,_fm,_ev,_rz,_Vef = _EC.catalogo(D,F,V,seed)
    if _Vef!=V: raise SystemExit(f'FAMILIAS: escala_codigo.catalogo degrado V de {V} a {_Vef} (D={D}). Abortado.')
    nom=[]; PAT={}; fam={}; var={}
    for _i in range(_P.shape[0]):
        _k=int(_fm[_i]); _n=('T%d'%_k) if not bool(_ev[_i]) else ('T%dv%d'%(_k,_i-int(_rz[_i])-1))
        nom.append(_n); PAT[_n]=_P[_i].astype(float); fam[_n]=_k; var[_n]=(-1 if not bool(_ev[_i]) else _i-int(_rz[_i])-1)
    g=np.random.default_rng(_EC.SEMILLA_MUNDO+seed+777)   # rng PROPIO para valencias y excepciones (el catalogo ya uso el suyo)
    base={_k:('comida' if _k%2==0 else 'veneno') for _k in range(F)}
    for _k in range(F-int(n_neu),F): base[_k]='nada'                    # FAMILIAS: los ultimos n_neu tokens NO informan
    val={_n:(base[(fam[_n]+1)%F] if (fam_val=='barajado' and var[_n]>=0) else base[fam[_n]]) for _n in PAT}
    # exc_win: UNA variante candidata por token, en orden de token (decision ESTRUCTURAL declarada, no un desempate).
    # Se sortea SIEMPRE -- tambien con n_exc=0 -- para que `lineal` tenga LA MISMA ventana de medida que `excepciones`.
    exc_win=['T%dv%d'%(_k,int(g.integers(V))) for _k in range(F)]
    if fam_val=='azar':   # la permutacion de `azar` va LA ULTIMA: asi tokens y exc_win son identicos en los 4 mundos
        _nn=sorted(PAT); _et=['comida']*(len(_nn)//2)+['veneno']*(len(_nn)-len(_nn)//2)
        _pm=g.permutation(len(_nn)).tolist()
        for _i,_n in enumerate(_nn): val[_n]=_et[_pm[_i]]
        for _k in range(F-int(n_neu),F):
            for _n in PAT:
                if fam[_n]==_k: val[_n]='nada'
    _op={'comida':'veneno','veneno':'comida','nada':'veneno'}
    exc=[_n for _n in exc_win[:max(int(n_exc),0)]]
    for _n in exc: val[_n]=_op[val[_n]]
    herm={_e:sorted(set(['T%d'%fam[_e]]+['T%dv%d'%(fam[_e],_v) for _v in range(V)])-{_e}) for _e in exc_win}
    pres=[['T%d'%_k for _k in range(F)]+['T%dv%d'%(_k,_i) for _k in range(F)] for _i in range(V)]
    val_post={_n:_op[val[_n]] for _n in PAT if fam[_n]==0 and _n not in exc}   # CAMBIO: la familia 0 invierte; su excepcion NO
    return dict(PAT=PAT,fam=fam,var=var,val=val,exc=exc,exc_win=exc_win,herm=herm,pres=pres,val_post=val_post,
                nombres=nom,forma=D-n_var)
'''

# --------------------------------------------------------------- estado de solo lectura del mundo
ESTADO = (
    "    _ipa=-1; _tcam=(T//2 if cambio is None else cambio)   # FAMILIAS: deriva vigente y paso del cambio de familia\n"
    "    _enc={}; _exp={}; _ult={}; _prim={}; _rut=[0,0]; _texc={}; _col=0; _omi=0; _nren=0; _fv=[[],[],[],[]]\n")

CAB = '''"""organismo_familias = organismo/organismo_v14.py (v14.1, feefc88b1fd8d434, TRONCO CONGELADO: aqui solo se LEYO)
+ B-5 (anclas literales de experimentos/creacion_B/construye_codigo.py, f94aa0a2f714c28d)
+ MUNDO DE FAMILIAS (bloque 1, nivel 12): retina D = 9 forma + 3 variable, F tokens de peso 3, V variantes por token,
excepciones dentro de la familia, deriva de la variante presente, cambio de una familia en T/2, RENOVACION SIMETRICA
(lo rechazado desaparece igual que lo mordido) y valencia NEUTRA opcional (n_neu: R == 0).
NO hay organo nuevo: el organismo es v14.1 tal cual; lo unico nuevo es el mundo (y B-5, reparacion ya medida).
ANCLA DE IDENTIDAD: con mundo='AB' es organismo_v14 BIT A BIT -- mismo consumo del rng y MISMAS claves de salida
(el dict del mundo de familias se agrega solo si mundo!='AB'); con mundo='AB' y desambiguar=1 es
experimentos/creacion_B/organismo_v14_codigo_on.py bit a bit.
Arnes: identidad_familias.py.  Generado por construye_familias.py. NO editar a mano."""
'''


if __name__ == '__main__':
    src = origen(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14)

    # ---- 0) B-5 PRIMERO, con las anclas LITERALES de su propio constructor (importadas, no copiadas: ERR-38) ----
    origen(os.path.join(CREB, 'construye_codigo.py'), SHA_CODIGO)
    import construye_codigo as CB
    s = CB.pon(src, ",pat_shuf=0,pat_min=1):", CB.FIS_A, CB.FIS_B, 'familias+B5')

    # ---- 0 bis) la retina D: la sustitucion se LEE de construye_capD.py y de escala_codigo.py, no se inventa ----
    origen(os.path.join(RAIZ, 'experimentos', 'capacidad_grande', 'construye_capD.py'), SHA_CAPD)
    esc = origen(os.path.join(AQUI, 'escala_codigo.py'), SHA_ESCALA)
    for anc, etq in [("SEMILLA_MUNDO = 50000", 'escala: SEMILLA_MUNDO'),
                     ("PESO_TOKEN = 3", 'escala: PESO_TOKEN'),
                     ("    r = np.random.default_rng(SEMILLA_MUNDO + seed)\n    r.shuffle(combos)", 'escala: sorteo'),
                     ("def catalogo(D, F, V, seed):", 'escala: catalogo'),
                     ("def kw_del_tronco(seed, NK, D):", 'escala: kw_del_tronco')]:
        exige(esc, anc, 1, etq)
    import escala_codigo as EC
    exige(src, EC.ANCLA_ESTADO, 1, 'v14: estado inicial')
    exige(src, EC.ANCLA_CODE, 1, 'v14: code()')
    exige(src, EC.ANCLA_CONST, 1, 'v14: L/NK/NKMAX/K')

    # ---- 1) itertools no hace falta: el catalogo lo da escala_codigo. Solo la tabla de valencias neutra ----
    s = sust(s, A_TABLAS, A_TABLAS + MUNDO.rstrip('\n'), etiqueta='tablas + mundo de familias')

    # ---- 2) firma: PAT/NK/NKMAX/K/L como DEFAULTS (ambito de modulo) + las perillas del mundo ----
    s = sust(s, A_FIRMA, A_FIRMA[:-2] +
             ",mundo='AB',pats=PAT,nk=NK,nkmax=NKMAX,ktop=K,largo=L,"
             "fam_D=12,fam_nvar=3,fam_F=8,fam_V=3,n_exc=4,n_neu=0,fam_val='familia',deriva=5000,cambio=None,"
             "renov=0.0,vent=10000,crit_exp=0.5):", etiqueta='firma: perillas del mundo de familias')

    # ---- 3) sombra inerte de las constantes + construccion del mundo (rng PROPIO) ----
    s = sust(s, A_RNG, A_RNG +
             "    PAT=pats; NK=nk; NKMAX=nkmax; K=ktop; L=largo   # FAMILIAS: sombra INERTE (los defaults SON las constantes del modulo)\n"
             "    _MF=(mundo!='AB')   # FAMILIAS: con mundo='AB' NINGUNA linea nueva se ejecuta -> v14.1 BIT A BIT\n"
             "    _FA=_familias(seed,fam_D,fam_nvar,fam_F,fam_V,n_exc,fam_val,n_neu) if _MF else None   # rng PROPIO: no toca el del organismo\n"
             "    if _MF: PAT=_FA['PAT']\n"
             "    _D=len(next(iter(PAT.values())))   # FAMILIAS: tamano de la retina (6 con los patrones del tronco -> v14.1 exacto)\n",
             etiqueta='sombra de constantes + mundo')

    # ---- 4) retina D: las cuatro sustituciones de capD (6 -> _D, 9 -> _D+3) ----
    s = sust(s, EC.ANCLA_ESTADO, EC.ANCLA_CAPD_D.replace('(2,D+3)', '(2,_D+3)').replace('(NKMAX,D)', '(NKMAX,_D)')
             .replace('(NK,D)', '(NK,_D)'), etiqueta='retina D: estado inicial')
    s = sust(s, A_MU, "mu=np.zeros((NKMAX,_D))", etiqueta='retina D: mu')
    s = sust(s, A_MUPN, "mup=np.zeros((NKMAX,_D)); mun=np.zeros((NKMAX,_D))", etiqueta='retina D: mup/mun (hija dispersa)')
    s = sust(s, A_TR, "tr=np.zeros(_D+3)", etiqueta='retina D: traza')
    s = sust(s, A_WHILE, "    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,_D))\n"
             "    _cod0=({_a:sorted(code(PAT[_a])) for _a in sorted(PAT)} if _MF else None)"
             "   # FAMILIAS: el codigo INICIAL (antes de la primera fision), para cruzarlo con escala_codigo (bloque 0)\n",
             etiqueta='retina D: sorteo de codigos + codigo inicial')

    # ---- 5) cond(): con mundo='AB' es la del tronco, LITERAL; con familias no hay rechazo (PAT['A'] no existe) ----
    s = sust(s, A_COND,
             "    cond=(lambda: True) if _MF else (lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and "
             "(nuevo is None or solap_B is None or (len(code(PAT[nuevo])&code(PAT['B']))==solap_B and "
             "len(code(PAT[nuevo])&code(PAT['A']))==0)))   # FAMILIAS: el rechazo del tronco solo restringe A y B, que no existen aqui (misma decision que escala_codigo.kw_del_tronco)\n",
             etiqueta='cond por mundo')

    # ---- 6) via lenta a D + estado de solo lectura del mundo ----
    s = sust(s, A_LENTA,
             "    Wps=np.zeros(_D); Wns=np.zeros(_D)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)\n"
             + ESTADO, etiqueta='via lenta a D + estado del mundo')

    # ---- 7) cuerpo: valencias, valencia neutra en los contadores, estimulos presentes ----
    s = sust(s, A_POS, "    pos=0; E=1.0; objs={}; val=(dict(_FA['val']) if _MF else {'A':'comida','B':'veneno'})\n",
             etiqueta='valencias del mundo')
    s = sust(s, A_SOBRE, A_SOBRE +
             "    if _MF: sobre['nada']=[0]*4; llegadas['nada']=[0]*4   # FAMILIAS: valencia NEUTRA (solo lectura)\n",
             etiqueta='contadores de la valencia neutra')
    s = sust(s, A_TIPOS, "    tipos=(list(_FA['pres'][0]) if _MF else ['A','B'])   # FAMILIAS: los F tokens + UNA variante por token\n",
             etiqueta='estimulos presentes')

    # ---- 8) deriva, cambio de familia y muestreo del anillo (sin sorteo; solo lectura) ----
    s = sust(s, A_INVERT, A_INVERT +
             "        if _MF:   # FAMILIAS: deriva de la variante presente (SIN sorteo), cambio de UNA familia y muestreo del anillo\n"
             "            _ip=(t//deriva)%fam_V\n"
             "            if _ip!=_ipa:\n"
             "                _ipa=_ip\n"
             "                for _x in list(objs):\n"
             "                    if _FA['var'][objs[_x]]>=0: objs[_x]='T%dv%d'%(_FA['fam'][objs[_x]],_ip)   # los objetos de la variante que sale pasan a la que entra\n"
             "                tipos[:]=list(_FA['pres'][_ip])   # len(tipos) NO cambia nunca: el sorteo de spawn() es el mismo\n"
             "            if t==_tcam:\n"
             "                for _n2,_v2 in _FA['val_post'].items(): val[_n2]=_v2   # la excepcion de T0 conserva su valencia ABSOLUTA\n"
             "            if t%1000==0 and objs: _fv[q(t)].append(sum(1 for _y in objs.values() if val[_y]=='veneno')/len(objs))\n",
             etiqueta='deriva y cambio de familia')

    # ---- 9) exposiciones, exp_asoc, ruta, primera y ULTIMA visita (solo lectura; no tocan el rng) ----
    s = sust(s, A_LLEG, A_LLEG +
             "            if _MF and _prev_on!=pos:   # FAMILIAS: EXPOSICIONES por patron, exp_asoc, ruta, primera y ULTIMA visita (SOLO LECTURA)\n"
             "                _enc[kk]=_enc.get(kk,0)+1; _rut[0 if _fam(kc) else 1]+=1\n"
             "                _o0=(1.0 if val[kk]=='comida' else (-1.0 if val[kk]=='veneno' else 0.0))\n"
             "                if kk not in _prim: _prim[kk]=[t,round(float(_wt),3),_o0]\n"
             "                if _o0 and kk not in _exp and _wt*_o0>0 and abs(_wt)>=crit_exp: _exp[kk]=_enc[kk]\n"
             "                _ult[kk]=[t,round(float(_wt),3),_o0]\n",
             etiqueta='exposiciones y exp_asoc')

    # ---- 10) omision y RENOVACION SIMETRICA (lo rechazado desaparece igual que lo mordido) ----
    s = sust(s, A_RECH, A_RECH +
             "            if _MF and not mordio and val[kk]=='comida' and any(_t3<t<=_t3+vent and kk in _FA['herm'][_e3] for _e3,_t3 in _texc.items()): _omi+=1   # FAMILIAS: OMISION (hermano comestible rechazado en ventana abierta)\n"
             "            if renov and not mordio and (renov>=1.0 or rng.random()<renov):   # RENOVACION SIMETRICA (DIAG_mundo bloqueo 3): lo rechazado tambien desaparece\n"
             "                _nren+=1; del objs[pos]; spawn(); _rech.pop(pos,None)\n",
             etiqueta='omision + renovacion simetrica')

    # ---- 11) COLATERAL: ventana de 10000 pasos tras la PRIMERA mordida de cada estimulo de exc_win ----
    s = sust(s, A_MORD, A_MORD +
             "                if _MF:   # FAMILIAS: la ventana la abre la PRIMERA mordida del estimulo de exc_win, exista o no la excepcion (asi `lineal` tiene la MISMA ventana)\n"
             "                    if kk in _FA['herm'] and kk not in _texc: _texc[kk]=t\n"
             "                    if val[kk]=='veneno':\n"
             "                        for _e3,_t3 in _texc.items():\n"
             "                            if _t3<t<=_t3+vent and kk in _FA['herm'][_e3]: _col+=1; break\n",
             etiqueta='colateral')

    # ---- 12) lecturas finales: log, solapamiento y el dict del mundo ----
    s = sust(s, A_LOG, "        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(PAT[k]),2) for k in (sorted(PAT) if _MF else 'ABCD')))\n",
             etiqueta='log por mundo')
    s = sust(s, A_SOLAP, "                solap=({'AB':None,'nB':None} if _MF else {'AB':len(code(PAT['A'])&code(PAT['B'])),"
             "'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None}),", etiqueta='solapamiento por mundo')
    s = sust(s, A_RET,
             "    _wv=([round(float(abs(Wps[_i]-Wns[_i])),3) for _i in range(_D-fam_nvar,_D)] if _MF else [])\n"
             "    _ext=(dict(mundo=mundo,\n"
             "               fam=dict(D=_D,n_var=fam_nvar,F=fam_F,V=fam_V,n_exc=n_exc,n_neu=n_neu,fam_val=fam_val,deriva=deriva,\n"
             "                        cambio=_tcam,renov=renov,vent=vent,crit_exp=crit_exp,nobj=nobj,L=L,NK=NK,NKMAX=NKMAX,K=K),\n"
             "               val_mundo=dict(_FA['val']),exc=list(_FA['exc']),exc_win=list(_FA['exc_win']),\n"
             "               herm={_a:list(_b) for _a,_b in _FA['herm'].items()},\n"
             "               cod0=dict(_cod0),cod_fin={_a:sorted(code(PAT[_a])) for _a in sorted(PAT)},\n"
             "               exposiciones=dict(_enc),exp_asoc=dict(_exp),primera=dict(_prim),ultima=dict(_ult),\n"
             "               ruta=list(_rut),colateral=_col,omision=_omi,colateral_tot=_col+_omi,t_exc=dict(_texc),\n"
             "               w_var=_wv,w_var_med=(round(float(np.median(_wv)),3) if _wv else None),renovados=_nren,\n"
             "               frac_veneno=[(round(float(np.mean(_x)),3) if _x else None) for _x in _fv],\n"
             "               frac_regalo=round(0.6*deaths/max(T*costo,1e-9),4)) if _MF else {})   # FAMILIAS: claves nuevas SOLO si mundo!='AB'\n"
             + A_RET, etiqueta='dict del mundo de familias')
    s = sust(s, A_RETFIN, A_RETFIN[:-1] + ",**_ext)", etiqueta='return con las claves del mundo')

    d = os.path.join(AQUI, 'organismo_familias.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(CAB + s)
    print(f"  escrito {os.path.relpath(d, RAIZ)}")
    for nom, p, sha in [('organismo/organismo_v14.py (origen, CONGELADO)', os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                        ('creacion_B/construye_codigo.py (anclas B-5)', os.path.join(CREB, 'construye_codigo.py'), SHA_CODIGO),
                        ('nivel12/escala_codigo.py (catalogo, bloque 0)', os.path.join(AQUI, 'escala_codigo.py'), SHA_ESCALA),
                        ('capacidad_grande/construye_capD.py (retina D)', os.path.join(RAIZ, 'experimentos', 'capacidad_grande', 'construye_capD.py'), SHA_CAPD)]:
        print(f"  sha {nom:48s} {h16(p)}  (esperado {sha})")
    print(f"  sha {'construye_familias.py':48s} {h16(os.path.abspath(__file__))}")
    print(f"  sha {'organismo_familias.py':48s} {h16(d)}")
    print("  siguiente: python experimentos/nivel12_mundo_familias/identidad_familias.py")
