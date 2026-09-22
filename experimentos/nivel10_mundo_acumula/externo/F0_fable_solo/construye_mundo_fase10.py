"""Construye mundo_fase10.py POR ANCLAS. Escribe SOLO en esta carpeta; el repo de JUACO se LEE por ruta absoluta.

MISION: llegar a la AGI por este camino. FASE 10: un mundo donde un linaje mortal SOLO se sostiene si transmite y
donde lo transmitido tiene que CRECER. El organismo no cambia: cambia el mundo (y se le devuelven dos instrumentos
que ya existian: el mapa del nivel 6 y el oraculo del bloque 2). NINGUNA regla de aprendizaje nueva.

ORIGEN (se lee, no se toca): experimentos/nivel09_cuerpo_nuevo/organismo_f9.py  3a821884394d66c9
  cadena: organismo_alma2 4fd616aeaf535e61 <- organismo_alma 7c09cec391daa879 <- organismo_vivo_h1 9e99ff87b5e2db1e
  <- organismo_vivo_rep2 96feb4918dc5d694 <- organismo_vivo_rep aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825
  <- TRONCO organismo/organismo_v14.py (v14.1) feefc88b1fd8d434.
DONANTES (bloques copiados LITERALMENTE; el constructor comprueba que cada bloque existe en su donante y su sha):
  D1 organismo/organismo_v142.py 17528d767fcebaf6 (v14.2 = v14.1 + B-5 `desambiguar`): las claves de salida.
  D2 experimentos/creacion_B/organismo_vivo_codigo.py 839fa71f9c84cb26: B-5 con la indexacion por necesidad (Wp[_nm,j]).
  D3 experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py 9dd1fb91ecec35ae: el NODO ORACULO (`nodo_or`).
  D4 experimentos/nivel6_mapa/mundo_mapa.py 207d6a1954336b18: vision limitada `r_vis`, tabla M y `_sesgo_M`.
  D5 experimentos/criterio_v3/organismo_v3cal.py 148014f68cb01785: `placebo=k` (k sorteos por paso descartados).
  D6 experimentos/nivel12_mundo_familias/organismo_familias.py b9dd561a0cf056b8: retina parametrizada (`pats`, `_D`).
  D7 experimentos/nivel06_rodeo_obligado/mundo_muralla.py 6e515713c86d8bf4: geometria por semilla con rng propio (patron).

PERILLAS NUEVAS (todas APAGADAS por defecto salvo `desambiguar=1`, que es el defecto del TRONCO v14.2):
  desambiguar=1  B-5 (v14.2). Con desambiguar=0 -> organismo_f9 BIT A BIT (todas sus claves, mas 3 de solo lectura).
  placebo=0      k sorteos del rng del organismo por paso, descartados (el nulo exacto, A-CAL).
  nodo_or=0      el nodo trae la TABLA VERDADERA (cota superior de la herencia), como en el bloque 2.
  pats=None      diccionario de patrones del mundo (retina de _D pixeles). None -> los 4 del tronco (_D=6).
  vals=None      valencia inicial por tipo. None -> VAL_VIVO / {'A':'comida','B':'veneno'}.
  r_vis=None     alcance de la retina (mundo_mapa). None -> ve todo el anillo (tronco).
  usa_M=0, escribe_M=1, gamma_M=0.6, H_M=20, disc_M=0.9   la tabla M (posicion -> ultimo patron visto) y su sesgo
                 sobre la locomocion SOLO cuando la retina esta vacia (mundo_mapa, literal). Memoria del INDIVIDUO:
                 se borra al morir (muerte_real). Sin r_vis es INERTE por construccion (nunca hay retina vacia).
  olvida_M=0     donde recordaba algo y hoy no hay nada (ni pendiente de reaparecer), olvida: percepcion de ausencia.
  parches=0, cap=1, regen=0, vida_parche=0   los objetos viven en PARCHES que se agotan (cap unidades) y se MUDAN
                 (sitio y tipo sorteados con el rng DEL MUNDO 920000+1000000*seed) al agotarse o a los vida_parche pasos.
  cambia_cada=0, cambia_fam=4   CAMBIO NO AVISADO: cada cambia_cada pasos dos tipos del mismo eje con valencia
                 opuesta se la intercambian (balance intacto); cada cambia_fam cambios, una FAMILIA entera cambia con
                 la de su eje (el veneno cambia de familia).
  f10=0          medidas de SOLO LECTURA por cuerpo que muere: generacion, cobertura de la tabla, combinaciones
                 explotadas (tipo x cuarto del anillo), exposiciones/mordidas de lo malo por alias vs sin alias,
                 causa de muerte, celdas, alias estructural al nacer y al morir.
Uso:  python construye_mundo_fase10.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
JUACO = r'C:\Users\User\Documents\PROYECTOS\JUACO\bundle'
EXP = os.path.join(JUACO, 'experimentos')
ORIGEN = os.path.join(EXP, 'nivel09_cuerpo_nuevo', 'organismo_f9.py')
DESTINO = os.path.join(AQUI, 'mundo_fase10.py')
SHA_ORIGEN = '3a821884394d66c9'
CADENA = {
    os.path.join(EXP, 'nivel13_alma', 'organismo_alma2.py'): '4fd616aeaf535e61',
    os.path.join(EXP, 'nivel13_alma', 'organismo_alma.py'): '7c09cec391daa879',
    os.path.join(EXP, 'nivel11_mundo_vivo', 'organismo_vivo_h1.py'): '9e99ff87b5e2db1e',
    os.path.join(EXP, 'nivel11_mundo_vivo', 'organismo_vivo_rep2.py'): '96feb4918dc5d694',
    os.path.join(EXP, 'nivel11_mundo_vivo', 'organismo_vivo_rep.py'): 'aa823d56c2d4213c',
    os.path.join(EXP, 'nivel11_mundo_vivo', 'organismo_vivo.py'): '20c0961c79de8825',
    os.path.join(JUACO, 'organismo', 'organismo_v14.py'): 'feefc88b1fd8d434',
}
DONANTES = {
    'D1_v142': (os.path.join(JUACO, 'organismo', 'organismo_v142.py'), '17528d767fcebaf6'),
    'D2_vivo_codigo': (os.path.join(EXP, 'creacion_B', 'organismo_vivo_codigo.py'), '839fa71f9c84cb26'),
    'D3_f9c': (os.path.join(EXP, 'nivel09_cuerpo_nuevo_b2', 'organismo_f9c.py'), '9dd1fb91ecec35ae'),
    'D4_mundo_mapa': (os.path.join(EXP, 'nivel6_mapa', 'mundo_mapa.py'), '207d6a1954336b18'),
    'D5_v3cal': (os.path.join(EXP, 'criterio_v3', 'organismo_v3cal.py'), '148014f68cb01785'),
    'D6_familias': (os.path.join(EXP, 'nivel12_mundo_familias', 'organismo_familias.py'), 'b9dd561a0cf056b8'),
    'D7_muralla': (os.path.join(EXP, 'nivel06_rodeo_obligado', 'mundo_muralla.py'), '6e515713c86d8bf4'),
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


NUEVO, EN_LINEA, DOC = [], [], []


def sust(texto, viejo, nuevo, n=1, etiqueta='', en_linea=False, rng_ok=False):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:70]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    NUEVO.append((etiqueta, nuevo if en_linea else nuevo.replace(viejo, ''), rng_ok, viejo if en_linea else ''))
    if en_linea:
        EN_LINEA.append(viejo)
    DOC.append((etiqueta, viejo.strip().splitlines()[0][:90], 'en linea' if en_linea else 'insercion'))
    return texto.replace(viejo, nuevo)


def bloque_donante(clave, bloque):
    """El bloque copiado tiene que existir LITERALMENTE en el donante (asi la ancla es una copia, no una redaccion)."""
    ruta, sha = DONANTES[clave]
    if bloque not in open(ruta, encoding='utf-8').read():
        raise SystemExit(f"DONANTE {clave}: el bloque {bloque[:80]!r} NO esta literalmente en {ruta}. Abortado.")
    DOC.append((f'donante {clave}', bloque.strip().splitlines()[0][:90], f'copiado de {os.path.basename(ruta)} {sha}'))
    return bloque


# ==================== ANCLAS del ORIGEN (copiadas literalmente de organismo_f9.py 3a821884394d66c9) ====================
A_PATGLOBAL = "PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}\n"
A_FIRMA = "d_dote=0.1,d_umbral=0.1,menu='abcdef',nodo_baraja=0,nodo_rel=0,con_desde=0,rep_acum=0,f9=0):"
A_GUARDIAS = "    if f9 and not (h1 and rep2): raise SystemExit('F9: f9=1 exige h1=1 y rep2=1 (las medidas del cuerpo usan su nacimiento y su vida)')\n"
A_RNG = "    rng=np.random.default_rng(seed)\n"
A_KW = "    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True\n"
A_WP = "    Wp=np.zeros((n_nec,NKMAX)); Wn=np.zeros((n_nec,NKMAX)); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)\n"
A_WPS = "    Wps=np.zeros((n_nec,6)); Wns=np.zeros((n_nec,6))   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0). VIVO: una fila por necesidad\n"
A_WPE = "    Wpe=np.zeros((n_nec,6)); Wke=np.zeros((n_nec,NKMAX)); _sbE=np.zeros(n_nec)   # VIVO: predictor VECTORIAL de dS y SORPRESA POR NECESIDAD (inerte con eta_pred=0)\n"
A_BXOR = "    _mnec=[0,0]; _bxor=[[0]*4 for _ in range(n_nec)]; _exor=[[0]*4 for _ in range(n_nec)]   # VIVO: muertes [por energia, por agua] y tabla NECESIDAD x ESTIMULO (solo lectura)\n"
A_IDX = "    _IDX={_k2:_i2 for _i2,_k2 in enumerate('ABCD')}\n"
A_INITF9 = "    _p1=[]; _c1=[]; _tok=[]; _ncu=[]   # F9: por cuerpo que muere -- rechazo lo malo a la 1a / mordio lo bueno a la 1a / pasos hasta la 1a mordida con R>0 / estaba conectado. SOLO LECTURA (-1 = no hubo ocasion)\n"
A_MUP = "    mup=np.zeros((NKMAX,6)); mun=np.zeros((NKMAX,6)); zp=np.zeros(NKMAX); zn=np.zeros(NKMAX)   # D: medias de P condicionadas al signo de R, con normalizador\n"
A_VAL = "    pos=0; E=1.0; Ag=A_ini; objs={}; val=(dict(VAL_VIVO) if vivo else {'A':'comida','B':'veneno'})\n"
A_SPAWN = "    def spawn():\n        while len(objs)<nobj:\n"
A_SPAWN0 = "    spawn()\n    q=lambda t:min(t//(T//4),3)\n"
A_SEE1 = "            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo\n"
A_SEE2 = "            for x,k in objs.items():\n                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)\n"
A_SEE3 = "        return best\n"
A_SNAP = "        return _m\n"
A_NONLOCAL = "        nonlocal E,Ag,_prev_on,_nbar\n"
A_NACEWL = "        Wl[:]=_rh.uniform(.1,.4,(2,9)); el[:]=0; tr[:]=0   # la politica de locomocion NO se hereda en ningun brazo\n"
A_NACEKW = "            KW[:]=0; activa[:]=False; KW[:NK]=_rh.uniform(0,1,(NK,6)); activa[:NK]=True\n"
A_NACEPM = "                _pm=_rb.permutation(6); _nbar+=int(bool((_pm==np.arange(6)).all()))   # misma magnitud, pixeles equivocados\n"
A_NACEE = "        E=(_m['dote'] if _m is not None else dote); Ag=E   # nace con su dote; el fundador de repuesto la recibe DEL MUNDO (regalo, se cuenta)\n"
A_LOOP = "    for t in range(T):\n"
A_HAMBRE = "        hambre=np.clip(1-E,0,1)\n"
A_SEEPAT = "        d,k,left=see(contar=True); pat=PAT[k]\n"
A_X = "        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre\n"
A_UMAX = "        if u.max()>.5: m[np.argmax(u)]=1\n"
A_RP = "        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.\n"
A_ENOBJ = "        if pos in objs:\n"
A_EXPO = ("            if vivo and _prev_on!=pos:   # VIVO: EXPOSICIONES (llegadas) y EXPOSICIONES HASTA CRITERIO, por necesidad. SOLO LECTURA\n"
          "                _enc[kk]+=1; _exor[_na][_IDX[kk]]+=1\n")
A_MORD = "                mord[kk][q(t)]+=1\n"
A_DELSPAWN = "                del objs[pos]; spawn()\n"
A_DIV = "                                if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():\n"
A_DIVELSE = "                                    else:   Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.\n"
A_PREVON = "        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas\n"
A_OLVIDO = "            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido\n"
A_H1 = ("            if h1:   # H1: se cierra el cuerpo que muere: su vida SIN tope, su origen y sus descendientes (solo lectura)\n"
        "                _svid+=t-_tmu; _vh.append(t-_tmu); _org.append(int(not _esfund)); _dpv.append(_dv); _dv=0\n")
A_MAL = "                    _mal9=[_x9 for _x9 in _exph if _x9[1]==('B' if _x9[2]==0 else 'D')]\n"
A_BUE = "                    _bue9=[_x9 for _x9 in _exph if _x9[1]==('A' if _x9[2]==0 else 'C')]\n"
A_NACECALL = "                _nace(_nac,_m)\n"
A_AZAR = "                    elif nodo_rel==2: _msg=[_nodo[_i9] for _i9 in sorted(int(_z9) for _z9 in _rrel.choice(len(_nodo),size=min(nodo_lee,len(_nodo)),replace=False))]   # F9: CONTROL DE ACCESO (mismo alcance, orden cronologico, seleccion al azar)\n"
A_LOG = "        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(PAT[k]),2) for k in 'ABCD'))\n"
A_REPACUM = "    if rep_acum: _ext.update(rep_acum=1)   # F9: perilla DEL MUNDO (vale con alma=None); con rep_acum=0 no aparece\n"
A_RETURN = "    return dict(sobre=sobre,"
A_COND1 = "    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))\n"
A_COND2 = "            while not cond(): KW[objetivo_AB:NK]=_rh.uniform(0,1,(NK-objetivo_AB,6))\n"

# ==================== BLOQUES DE DONANTES (literales) ====================
B1_DIV = "                                if (Wb[c]*R<0 or (desambiguar and R==0)) and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():   # B-5 DESAMBIGUAR: tambien divide cuando una celda consolidada, bajo una retina distinta (kj@P>KW[c]@P), recibe R==0\n"
B1_ELSE = ("                                    elif R<0: Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.\n"
           "                                    else: Wp[_nm,j]=0.; Wn[_nm,j]=0.; _ndes+=1; _des_t.append((t,kk))   # B-5: con R==0 la hija nace SIN valor en la necesidad activa (las otras se heredan abajo) y la madre conserva el suyo\n")
B1_RET = "    return dict(desambiguar=desambiguar,des_splits=_ndes,des_t=_des_t,sobre=sobre,"
B3_OR = ("                    if nodo_or:   # F9C: NODO ORACULO (cota superior, voto del creador A). El contenido NO es lo que vivio el linaje: es la TABLA VERDADERA\n"
         "                        #        (patron, necesidad) -> R del mundo, construida de PAT y _EF, que YA existian. MEMORIA NUEVA: CERO (se arma y se tira).\n"
         "                        _or9=[[[float(_z9) for _z9 in PAT[_k9]],float(1.0 if _EF[val[_k9]][_n9]>0 else (-3.0 if _EF[val[_k9]][_n9]<0 else 0.0)),int(_n9)] for _n9 in range(min(n_nec,2)) for _k9 in 'ABCD']\n"
         "                        _msg=_or9*max(1,nodo_lee)   # 8*nodo_lee = 400 mensajes con nodo_lee=50: CINCUENTA copias EXACTAS de la tabla, de las que el recien\n")
B4_SEE = "            if r_vis is not None and min((pos-x)%L,(x-pos)%L)>r_vis: continue   # mapa: fuera de la vista\n"
B4_SEE2 = "                if r_vis is not None and min((pos-x)%L,(x-pos)%L)>r_vis: continue   # mapa: fuera de la vista\n"
B4_RET = "        return best if best is not None else (None,'vacio',None)   # mapa: nada a la vista\n"
B4_M = "    _Mpat=np.zeros((L,6)); _Mset=np.zeros(L,bool); _VACIO=np.zeros(6)   # mapa: tabla posicion -> ultimo patron visto\n"
B4_SESGO = ("    def _sesgo_M():   # mapa: con la retina vacia, valor recordado por direccion, descontado por distancia\n"
            "        _bi=sum(disc_M**h*valor(_Mpat[(pos-h)%L]) for h in range(1,H_M+1) if _Mset[(pos-h)%L])\n"
            "        _bd=sum(disc_M**h*valor(_Mpat[(pos+h)%L]) for h in range(1,H_M+1) if _Mset[(pos+h)%L])\n"
            "        return gamma_M*np.array([_bi,_bd])\n")
B4_PAT = "pat=PAT[k] if k!='vacio' else _VACIO"
B4_X = "        x=np.concatenate([pat*1.2,[1.5 if left else 0,1.5 if left is False else 0,1.0 if d==0 else 0.]]); noise=.15+.5*hambre\n"
B4_U = "        if usa_M and k=='vacio': u=u+_sesgo_M()   # mapa: solo desempata sin senal directa\n"
B4_RP = "Rp=.2 if (d is not None and d2 is not None and d2<d) else 0."
B4_ESCRIBE = "            if usa_M and escribe_M: _Mpat[pos]=PAT[objs[pos]]; _Mset[pos]=True   # mapa: recuerda lo que vio aqui\n"
B4_PEND = ("        if _pend:   # mapa: reaparecen en su sitio los objetos maduros\n"
           "            _mad=[x for x,tt in _pend.items() if tt<=t]\n"
           "            if _mad:\n"
           "                for x in _mad: del _pend[x]\n"
           "                spawn()\n")
B5_PLACEBO = "        for _ in range(placebo): rng.random()   # PLACEBO (criterio v3, A-CAL): consume k sorteos por paso y DESCARTA el valor. Ninguna decision los mira: la LEY no cambia, la TRAYECTORIA si. placebo=0 -> el tronco BIT A BIT\n"
B5_GUARD = ("    placebo=int(placebo)\n"
            "    if placebo<0: raise SystemExit('PLACEBO: k debe ser un entero >= 0')\n")
B6_D = "    _D=len(next(iter(PAT.values())))   # FAMILIAS: tamano de la retina (6 con los patrones del tronco -> v14.1 exacto)\n"
B7_RNG = "            _rg=np.random.default_rng(1000003*int(seed)+7)\n"

# ==================== INSERCIONES ====================
N_PATGLOBAL = A_PATGLOBAL + "_PAT_TRONCO=PAT   # F10: los patrones del tronco, para que run() pueda tomar otros (`pats`) sin tocar el global\n"
N_FIRMA = A_FIRMA[:-2] + ",desambiguar=1,placebo=0,nodo_or=0,pats=None,vals=None,r_vis=None,usa_M=0,escribe_M=1,gamma_M=0.6,H_M=20,disc_M=0.9,olvida_M=0,parches=0,cap=1,regen=0,vida_parche=0,cambia_cada=0,cambia_fam=4,f10=0):"
N_GUARDIAS = A_GUARDIAS + B5_GUARD + (
    "    if alma is None: nodo_or=0   # F10: el ORACULO es contenido del nodo, detras de la maestra (inerte: organismo_f9 EXACTO)\n"
    "    if nodo_or and not nodo: raise SystemExit('F10: nodo_or exige nodo=1 (el oraculo sustituye el CONTENIDO del nodo, no el canal)')\n"
    "    if parches and not vivo: raise SystemExit('F10: parches exige vivo=1 (el mundo de la fase 10 es el mundo vivo)')\n"
    "    if parches and int(cap)<1: raise SystemExit('F10: cap >= 1')\n"
    "    if cambia_cada and int(cambia_cada)<1: raise SystemExit('F10: cambia_cada es 0 (sin cambios) o un entero >= 1')\n"
    "    if f10 and not (h1 and rep2): raise SystemExit('F10: f10=1 exige h1=1 y rep2=1 (las medidas del cuerpo usan su nacimiento y su vida)')\n"
    "    if olvida_M and not usa_M: raise SystemExit('F10: olvida_M exige usa_M=1 (no hay mapa que olvidar)')\n")
N_RNG = ("    PAT=(dict(_PAT_TRONCO) if pats is None else dict(pats)); " + B6_D.strip() + "\n"
         "    if vals is not None and set(vals)!=set(PAT): raise SystemExit('F10: vals debe dar la valencia de TODOS los tipos de pats')\n") + A_RNG
N_KW = A_KW.replace("(2,9)", "(2,_D+3)").replace("(NKMAX,6)", "(NKMAX,_D)").replace("(NK,6)", "(NK,_D)")
N_WP = A_WP.replace("mu=np.zeros((NKMAX,6)); splits=0; el=", "mu=np.zeros((NKMAX,_D)); splits=0; _ndes=0; _des_t=[]; el=").replace("tr=np.zeros(9)", "tr=np.zeros(_D+3)")
N_WPS = A_WPS.replace("(n_nec,6)", "(n_nec,_D)")
N_WPE = A_WPE.replace("(n_nec,6)", "(n_nec,_D)")
N_BXOR = A_BXOR.replace("[0]*4", "[0]*len(PAT)")
N_IDX = A_IDX.replace("enumerate('ABCD')", "enumerate(PAT)")
N_MUP = A_MUP.replace("(NKMAX,6)", "(NKMAX,_D)")
N_VAL = A_VAL[:-1] + " if vals is None else dict(vals)   # F10: valencia inicial por tipo del mundo nuevo\n"
N_INITF9 = A_INITF9 + B4_M.replace("(L,6)", "(L,_D)").replace("np.zeros(6)", "np.zeros(_D)").replace("# mapa:", "# mapa (mundo_mapa): ") + (
    "    _rmun=np.random.default_rng(920000+1000000*seed) if (parches or cambia_cada) else None   # F10: rng PROPIO del MUNDO (parches y cambios; ERR-60; patron de mundo_muralla): no toca el rng del organismo ni los 700000+/800000+/850000+/860000+/870000+\n"
    "    _par=[]; _pend={}; _pmax=0; _ncam=0; _cambios=[]; _gen=1; _f10c=[]   # F10: parches [sitio,tipo,unidades,t0], pendientes de reaparecer, estancia maxima de un parche, cambios del mundo, generacion del cuerpo en curso, resumen por cuerpo. SOLO LECTURA salvo _par/_pend (son el mundo)\n"
    "    _ex10=set(); _enc10=0; _pb10=[0,0]; _pe10=[0,0]; _ult10=None; _al0=0; _al00=0   # F10 (solo lectura, por cuerpo): combinaciones (tipo,cuarto) explotadas, exposiciones, mordidas/exposiciones de lo malo [alias, sin alias], ultima mordida mala (t, alias), pares alias al nacer\n")
N_SESGO = B4_SESGO.replace("    def _sesgo_M():   # mapa: con la retina vacia, valor recordado por direccion, descontado por distancia\n",
                           "    def _sesgo_M():   # mapa (mundo_mapa, literal): con la retina vacia, valor recordado por direccion, descontado por distancia\n")
N_MEDIDAS = (
    "    def _npares_alias():   # F10: pares (tipo bueno, tipo malo) que comparten el codigo EXACTO de Kenyon AHORA (alias estructural). SOLO LECTURA\n"
    "        _cd={_k9:frozenset(code(PAT[_k9])) for _k9 in tipos}\n"
    "        _bu=[_k9 for _k9 in tipos if _EF[val[_k9]][0]>0 or _EF[val[_k9]][1]>0]; _ma=[_k9 for _k9 in tipos if _EF[val[_k9]][0]<0 or _EF[val[_k9]][1]<0]\n"
    "        return sum(1 for _b9 in _bu for _m9 in _ma if _cd[_b9]==_cd[_m9])\n"
    "    def _alias_de(_k9):   # F10: el tipo (malo) _k9 comparte codigo con algun tipo bueno AHORA. SOLO LECTURA\n"
    "        _c9=code(PAT[_k9])\n"
    "        return any(code(PAT[_b9])==_c9 for _b9 in tipos if _b9!=_k9 and (_EF[val[_b9]][0]>0 or _EF[val[_b9]][1]>0))\n"
    "    def _resumen_cuerpo(_t9):   # F10: RESUMEN DEL CUERPO QUE MUERE. Todo SOLO LECTURA; se calcula y se guarda en _f10c\n"
    "        _cs=0; _cc=0; _ni=0\n"
    "        for _k9 in PAT:\n"
    "            _kc9=kenyon(PAT[_k9])\n"
    "            for _n9 in range(min(n_nec,2)):\n"
    "                _s9=_EF[val[_k9]][_n9]\n"
    "                if _s9==0: continue\n"
    "                _ni+=1; _v9=_vnec(_n9,PAT[_k9],_kc9)\n"
    "                if _v9*_s9>0: _cs+=1\n"
    "                if _v9*_s9>0 and abs(_v9)>=crit_exp: _cc+=1\n"
    "        _nb=sum(1 for _k9 in tipos if _EF[val[_k9]][0]>0 or _EF[val[_k9]][1]>0)\n"
    "        _cau=('drenaje' if (_ult10 is None or _t9-_ult10[0]>100) else ('alias' if _ult10[1] else 'limpio'))\n"
    "        return dict(cuerpo=int(deaths),gen=int(_gen),vida=int(_t9-_tmu),cob_s=round(_cs/max(_ni,1),4),cob_c=round(_cc/max(_ni,1),4),n_inf=int(_ni),\n"
    "                    expl=len(_ex10),expl_t=len({_k9 for _k9,_ in _ex10}),n_bue=int(_nb),enc=int(_enc10),pe=list(_pe10),pb=list(_pb10),causa=_cau,\n"
    "                    celdas=int(activa.sum()),des=int(_ndes),alias_nac=int(_al0),alias_fin=int(_npares_alias()),con=int(_con))\n"
    "    def _nuevo_parche(_t9):   # F10: un parche nuevo en un sitio libre sorteado por el MUNDO (_rmun), de un tipo sorteado entre `tipos`, con `cap` unidades\n"
    "        while True:\n"
    "            _x9=int(_rmun.integers(L))\n"
    "            if all(_x9!=_p9[0] for _p9 in _par) and _x9 not in objs: break\n"
    "        return [_x9,tipos[int(_rmun.integers(len(tipos)))],int(cap),int(_t9)]\n")
N_SPAWN = (
    "    def spawn():\n"
    "        if parches:   # F10: los objetos viven en PARCHES que se agotan y se mudan; un parche con unidades y sin reaparicion pendiente esta a la vista\n"
    "            for _pi9 in range(len(_par)):\n"
    "                _x9,_k9,_u9,_t9=_par[_pi9]\n"
    "                if _u9>0 and _x9 not in objs and _x9 not in _pend: objs[_x9]=_k9\n"
    "            return\n"
    "        while len(objs)<nobj:\n")
N_SPAWN0 = ("    if parches:\n        for _ in range(int(parches)): _par.append(_nuevo_parche(0))   # F10: los parches iniciales, sorteados por semilla con el rng DEL MUNDO\n"
            "    if f10: _al0=_npares_alias(); _al00=_al0   # F10: alias estructural del fundador\n") + A_SPAWN0
N_SEE1 = A_SEE1 + B4_SEE
N_SEE2 = "            for x,k in objs.items():\n" + B4_SEE2 + "                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)\n"
N_SEE3 = B4_RET
N_SNAP = "        if f10: _m['gen']=_gen   # F10: la generacion del hijo = la del padre + 1 (se fija al parto, con la memoria)\n" + A_SNAP
N_NONLOCAL = "        nonlocal E,Ag,_prev_on,_nbar,_gen\n"
N_NACEWL = A_NACEWL.replace("(2,9)", "(2,_D+3)") + "        if usa_M: _Mpat[:]=0; _Mset[:]=False   # F10: el mapa es memoria del INDIVIDUO (H-1: la muerte borra al individuo); el hijo nace sin mapa\n"
N_NACEKW = A_NACEKW.replace("(NK,6)", "(NK,_D)")
N_NACEPM = A_NACEPM.replace("permutation(6)", "permutation(_D)").replace("np.arange(6)", "np.arange(_D)")
N_NACEE = A_NACEE + "        if f10: _gen=(int(_m['gen'])+1 if (_m is not None and 'gen' in _m) else 1)   # F10: fundador = generacion 1; hijo = padre + 1\n"
N_LOOP = A_LOOP + B5_PLACEBO + (
    "        if parches:   # F10: reaparecen los pendientes maduros (mundo_mapa); los parches viejos (vida_parche) se MUDAN aunque no se hayan comido\n"
    + "".join("    " + l + "\n" for l in B4_PEND.rstrip("\n").split("\n")) +
    "            if vida_parche:\n"
    "                for _pi9 in range(len(_par)):\n"
    "                    if t-_par[_pi9][3]>=vida_parche:\n"
    "                        _x9=_par[_pi9][0]; _pmax=max(_pmax,t-_par[_pi9][3]); _par[_pi9]=_nuevo_parche(t)\n"
    "                        if _x9 in objs: del objs[_x9]\n"
    "                        _pend.pop(_x9,None); _rech.pop(_x9,None)\n"
    "                spawn()\n"
    "        if cambia_cada and t>0 and t%cambia_cada==0:   # F10: CAMBIO NO AVISADO del mundo (rng DEL MUNDO). El organismo no recibe ninguna senal: lo descubre mordiendo\n"
    "            _ncam+=1\n"
    "            if cambia_fam and _ncam%cambia_fam==0:   # una FAMILIA entera cambia de valencia con la de su eje: el veneno cambia de familia\n"
    "                _a9,_b9=(('comida','veneno'),('agua','sal'))[(_ncam//cambia_fam)%2]\n"
    "                for _k9 in tipos: val[_k9]=(_b9 if val[_k9]==_a9 else (_a9 if val[_k9]==_b9 else val[_k9]))\n"
    "                _cambios.append([int(t),'familia',_a9,_b9])\n"
    "            else:   # dos tipos del mismo eje con valencia opuesta se la intercambian: la comida vira (y un veneno se vuelve comida); el balance bueno/malo NO cambia (trampa 3)\n"
    "                _a9,_b9=(('comida','veneno'),('agua','sal'))[int(_rmun.integers(2))]\n"
    "                _la9=[_k9 for _k9 in tipos if val[_k9]==_a9]; _lb9=[_k9 for _k9 in tipos if val[_k9]==_b9]\n"
    "                if _la9 and _lb9:\n"
    "                    _x9=_la9[int(_rmun.integers(len(_la9)))]; _y9=_lb9[int(_rmun.integers(len(_lb9)))]; val[_x9],val[_y9]=_b9,_a9\n"
    "                    _cambios.append([int(t),'variante',_x9,_y9])\n")
N_HAMBRE = A_HAMBRE + "        if usa_M and olvida_M and _Mset[pos] and pos not in objs and pos not in _pend: _Mset[pos]=False   # F10 mapa: donde recordaba algo y hoy no hay nada (ni pendiente de reaparecer), olvida: percepcion de ausencia (los parches se mueven)\n"
N_SEEPAT = A_SEEPAT.replace("pat=PAT[k]", B4_PAT)
N_X = B4_X
N_UMAX = B4_U + A_UMAX
N_RP = A_RP.replace("Rp=.2 if d2<d else 0.", B4_RP)
N_ENOBJ = A_ENOBJ + B4_ESCRIBE
N_EXPO = A_EXPO + (
    "                if f10: _enc10+=1   # F10: exposiciones del cuerpo en curso (solo lectura)\n"
    "                if f10 and (_EF[val[kk]][0]<0 or _EF[val[kk]][1]<0): _pe10[0 if _alias_de(kk) else 1]+=1   # F10: exposicion a lo MALO, por alias / sin alias (solo lectura)\n")
N_MORD = A_MORD + (
    "                if f10:   # F10 (solo lectura): combinaciones explotadas (tipo, cuarto del anillo) y mordidas de lo malo por alias / sin alias\n"
    "                    if _dS[0]>0 or _dS[1]>0: _ex10.add((kk,pos*4//L))\n"
    "                    if _dS[0]<0 or _dS[1]<0: _a9=int(_alias_de(kk)); _pb10[0 if _a9 else 1]+=1; _ult10=(int(t),_a9)\n")
N_DELSPAWN = (
    "                if parches:   # F10: la mordida gasta UNA unidad del parche; agotado -> el parche se muda (sitio y tipo nuevos); si quedan, reaparece tras `regen`\n"
    "                    _pi9=next(_i9 for _i9,_p9 in enumerate(_par) if _p9[0]==pos); _par[_pi9][2]-=1\n"
    "                    if _par[_pi9][2]<=0: _pmax=max(_pmax,t-_par[_pi9][3]); _par[_pi9]=_nuevo_parche(t)\n"
    "                    elif regen: _pend[pos]=t+regen\n") + A_DELSPAWN
N_DIV = B1_DIV
N_DIVELSE = B1_ELSE
N_OLVIDO = ("            _dx=list(objs)[int(rng.integers(len(objs)))]\n"
            "            if parches: _pend[_dx]=t+regen   # F10 parche: el olvido del mundo lo esconde `regen` pasos, no gasta unidades\n"
            "            del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido\n")
N_H1 = A_H1 + (
    "                if f10:   # F10: RESUMEN DEL CUERPO QUE MUERE (solo lectura) y reinicio de sus contadores\n"
    "                    _f10c.append(_resumen_cuerpo(t)); _ex10=set(); _enc10=0; _pb10=[0,0]; _pe10=[0,0]; _ult10=None; _al0=_npares_alias()\n")
N_MAL = "                    _mal9=[_x9 for _x9 in _exph if val.get(_x9[1])==('veneno' if _x9[2]==0 else 'sal')]   # F10: lo malo = la valencia ACTUAL (en el mundo del tronco es exactamente B / D)\n"
N_BUE = "                    _bue9=[_x9 for _x9 in _exph if val.get(_x9[1])==('comida' if _x9[2]==0 else 'agua')]   # F10: lo bueno = la valencia ACTUAL (en el mundo del tronco es exactamente A / C)\n"
N_NACECALL = A_NACECALL + "                if f10: _al0=_npares_alias()   # F10: alias estructural del recien nacido (su KW es nuevo)\n"
N_AZAR = A_AZAR + B3_OR.replace("for _k9 in 'ABCD']", "for _k9 in PAT]")
N_LOG = A_LOG.replace("for k in 'ABCD'", "for k in PAT")
N_REPACUM = A_REPACUM + (
    "    if f10: _ext.update(f10=dict(cuerpos=list(_f10c),cambios=list(_cambios),n_cambios=int(_ncam),parche_max_estancia=int(max([_pmax]+[T-1-_p9[3] for _p9 in _par])),val_final=dict(val),\n"
    "                        alias_nac_fundador=int(_al00),parches=[list(_p9) for _p9 in _par],M_llenas=int(_Mset.sum()),\n"
    "                        cfg=dict(r_vis=r_vis,usa_M=int(usa_M),escribe_M=int(escribe_M),olvida_M=int(olvida_M),gamma_M=gamma_M,H_M=H_M,disc_M=disc_M,parches=int(parches),cap=int(cap),regen=int(regen),vida_parche=int(vida_parche),\n"
    "                                 cambia_cada=int(cambia_cada),cambia_fam=int(cambia_fam),placebo=int(placebo),nodo_or=int(nodo_or),desambiguar=int(desambiguar),D=int(_D),n_tipos=len(PAT),sem_mundo='920000+1000000*seed')))   # F10: clave nueva SOLO con f10=1\n")
N_RETURN = B1_RET

CABECERA = '''"""mundo_fase10 = experimentos/nivel09_cuerpo_nuevo/organismo_f9.py (3a821884394d66c9; aqui solo se LEYO; cadena
organismo_alma2 4fd616aeaf535e61 <- organismo_alma 7c09cec391daa879 <- organismo_vivo_h1 9e99ff87b5e2db1e <-
organismo_vivo_rep2 96feb4918dc5d694 <- organismo_vivo_rep aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <-
TRONCO organismo/organismo_v14.py v14.1 feefc88b1fd8d434) + B-5 `desambiguar` (v14.2, anclas literales de
organismo/organismo_v142.py 17528d767fcebaf6 y creacion_B/organismo_vivo_codigo.py 839fa71f9c84cb26) + EL MUNDO DE LA
FASE 10: retina de _D pixeles (`pats`, patron de nivel12), vision limitada + tabla M + sesgo (nivel6/mundo_mapa.py
207d6a1954336b18, literal), parches que se agotan y se mudan, cambios no avisados (rng DEL MUNDO 920000+1000000*seed),
placebo (criterio_v3/organismo_v3cal.py 148014f68cb01785, literal), nodo ORACULO (nivel09_cuerpo_nuevo_b2/organismo_f9c.py
9dd1fb91ecec35ae, literal) y medidas f10 de SOLO LECTURA. NINGUNA regla de aprendizaje nueva; memoria nueva del
organismo: CERO (la tabla M es el instrumento del nivel 6, memoria del individuo, se borra al morir).

  desambiguar=0 y todo lo demas apagado -> organismo_f9 BIT A BIT (todos sus brazos; 3 claves nuevas de solo lectura)
  defectos (desambiguar=1), vivo=0, n_nec=1 -> organismo/organismo_v142.py (TRONCO v14.2) BIT A BIT, todas las claves
  usa_M sin r_vis -> INERTE por construccion (nunca hay retina vacia): el mapa no toca el mundo del tronco.
Arnes: identidad_mundo_fase10.py. Generado por construye_mundo_fase10.py (F0_fable_solo). NO editar a mano."""
'''


def main():
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN {ORIGEN}: sha {h16(ORIGEN)}, se esperaba {SHA_ORIGEN}. Abortado.")
    for p, s in CADENA.items():
        if h16(p) != s:
            raise SystemExit(f"CADENA {p}: sha {h16(p)}, se esperaba {s}. Abortado.")
    for k, (p, s) in DONANTES.items():
        if h16(p) != s:
            raise SystemExit(f"DONANTE {k} {p}: sha {h16(p)}, se esperaba {s}. Abortado.")
    # los bloques de donantes tienen que ser copias literales
    for k, b in (('D1_v142', "    return dict(desambiguar=desambiguar,des_splits=_ndes,des_t=_des_t,sobre=sobre,"),
                 ('D2_vivo_codigo', B1_DIV), ('D2_vivo_codigo', B1_ELSE), ('D3_f9c', B3_OR), ('D4_mundo_mapa', B4_SEE),
                 ('D4_mundo_mapa', B4_SEE2), ('D4_mundo_mapa', B4_RET), ('D4_mundo_mapa', B4_M), ('D4_mundo_mapa', B4_SESGO),
                 ('D4_mundo_mapa', B4_PAT), ('D4_mundo_mapa', B4_X), ('D4_mundo_mapa', B4_U), ('D4_mundo_mapa', B4_RP),
                 ('D4_mundo_mapa', B4_ESCRIBE), ('D4_mundo_mapa', B4_PEND), ('D5_v3cal', B5_PLACEBO), ('D5_v3cal', B5_GUARD),
                 ('D6_familias', B6_D), ('D7_muralla', B7_RNG)):
        bloque_donante(k, b)
    src = open(ORIGEN, encoding='utf-8').read()
    t = src
    t = sust(t, A_PATGLOBAL, N_PATGLOBAL, 1, 'PAT_GLOBAL')
    t = sust(t, A_FIRMA, N_FIRMA, 1, 'FIRMA', en_linea=True)
    t = sust(t, A_GUARDIAS, N_GUARDIAS, 1, 'GUARDIAS')
    t = sust(t, A_RNG, N_RNG, 1, 'PATRONES_DEL_MUNDO')
    t = sust(t, A_KW, N_KW, 1, 'RETINA_KW', en_linea=True)
    t = sust(t, A_COND1, A_COND1.replace('(NK-objetivo_AB,6)', '(NK-objetivo_AB,_D)'), 1, 'RETINA_COND_FUNDADOR', en_linea=True)
    t = sust(t, A_COND2, A_COND2.replace('(NK-objetivo_AB,6)', '(NK-objetivo_AB,_D)'), 1, 'RETINA_COND_HIJO', en_linea=True)
    t = sust(t, A_WP, N_WP, 1, 'RETINA_MU_TR+B5_INIT', en_linea=True)
    t = sust(t, A_WPS, N_WPS, 1, 'RETINA_WPS', en_linea=True)
    t = sust(t, A_WPE, N_WPE, 1, 'RETINA_WPE', en_linea=True)
    t = sust(t, A_BXOR, N_BXOR, 1, 'TABLA_NEC_X_ESTIMULO', en_linea=True)
    t = sust(t, A_IDX, N_IDX, 1, 'IDX_TIPOS', en_linea=True)
    t = sust(t, A_INITF9, N_INITF9, 1, 'INIT_MAPA_PARCHES_F10')
    t = sust(t, A_MUP, N_MUP, 1, 'RETINA_MUP', en_linea=True)
    t = sust(t, A_VAL, N_VAL, 1, 'VALENCIAS_INICIALES', en_linea=True)
    t = sust(t, A_SPAWN, N_SPAWN + N_SESGO.replace('\n', '\n')[:0], 1, 'SPAWN_PARCHES', en_linea=True)
    t = sust(t, A_SPAWN0, N_SPAWN0, 1, 'PARCHES_INICIALES')
    t = sust(t, "    def spawn():\n", N_MEDIDAS + N_SESGO + "    def spawn():\n", 1, 'MEDIDAS_F10_Y_SESGO_M')
    t = sust(t, A_SEE1, N_SEE1, 1, 'VISION_LIMITADA_1')
    t = sust(t, A_SEE2, N_SEE2, 1, 'VISION_LIMITADA_2')
    t = sust(t, A_SEE3, N_SEE3, 1, 'RETINA_VACIA', en_linea=True)
    t = sust(t, A_SNAP, N_SNAP, 1, 'GENERACION_AL_PARTO')
    t = sust(t, A_NONLOCAL, N_NONLOCAL, 1, 'NONLOCAL_GEN', en_linea=True)
    t = sust(t, A_NACEWL, N_NACEWL, 1, 'NACE_WL_Y_MAPA', en_linea=True)
    t = sust(t, A_NACEKW, N_NACEKW, 1, 'NACE_KW', en_linea=True)
    t = sust(t, A_NACEPM, N_NACEPM, 1, 'NACE_BARAJA', en_linea=True)
    t = sust(t, A_NACEE, N_NACEE, 1, 'NACE_GENERACION')
    t = sust(t, A_LOOP, N_LOOP, 1, 'PLACEBO_PARCHES_CAMBIOS', rng_ok=True)
    t = sust(t, A_HAMBRE, N_HAMBRE, 1, 'OLVIDA_M')
    t = sust(t, A_SEEPAT, N_SEEPAT, 1, 'PAT_VACIO', en_linea=True)
    t = sust(t, A_X, N_X, 1, 'X_SIN_LADO', en_linea=True)
    t = sust(t, A_UMAX, N_UMAX, 1, 'SESGO_M_EN_U')
    t = sust(t, A_RP, N_RP, 1, 'RP_SIN_OBJETIVO', en_linea=True)
    t = sust(t, A_ENOBJ, N_ENOBJ, 1, 'ESCRIBE_M')
    t = sust(t, A_EXPO, N_EXPO, 1, 'EXPOSICIONES_F10')
    t = sust(t, A_MORD, N_MORD, 1, 'MORDIDAS_F10')
    t = sust(t, A_DELSPAWN, N_DELSPAWN, 1, 'PARCHE_SE_GASTA')
    t = sust(t, A_DIV, N_DIV, 1, 'B5_DIVISION', en_linea=True)
    t = sust(t, A_DIVELSE, N_DIVELSE, 1, 'B5_HIJA_SIN_VALOR', en_linea=True)
    t = sust(t, A_OLVIDO, N_OLVIDO, 1, 'OLVIDO_DEL_MUNDO', en_linea=True, rng_ok=True)
    t = sust(t, A_H1, N_H1, 1, 'RESUMEN_DEL_CUERPO')
    t = sust(t, A_MAL, N_MAL, 1, 'P1_VALENCIA_ACTUAL', en_linea=True)
    t = sust(t, A_BUE, N_BUE, 1, 'C1_VALENCIA_ACTUAL', en_linea=True)
    t = sust(t, A_NACECALL, N_NACECALL, 1, 'ALIAS_AL_NACER')
    t = sust(t, A_AZAR, N_AZAR, 1, 'NODO_ORACULO')
    t = sust(t, A_LOG, N_LOG, 1, 'LOG_TIPOS', en_linea=True)
    t = sust(t, A_REPACUM, N_REPACUM, 1, 'SALIDA_F10')
    t = sust(t, A_RETURN, N_RETURN, 1, 'SALIDA_B5', en_linea=True)
    t = CABECERA + t

    # --- GUARDIA 1: ninguna insercion consume el rng DEL ORGANISMO, salvo las dos declaradas:
    #     PLACEBO (es su definicion) y OLVIDO_DEL_MUNDO (la linea del tronco partida en tres; misma llamada, mismo orden)
    def _nrng(txt):
        limpio = '\n'.join(l for l in txt.split('\n') if not l.strip().startswith('#'))
        limpio = re.sub(r'\s{2,}#.*$', '', limpio, flags=re.M)
        return len(re.findall(r'\brng\.', limpio))
    for etq, ins, ok, viejo in NUEVO:
        if _nrng(ins) != _nrng(viejo) and not ok:   # en linea: las llamadas al rng del tronco se conservan, no se anade ninguna
            raise SystemExit(f"INSERCION {etq}: consume el rng DEL ORGANISMO. Abortado.\n{ins}")
    # --- GUARDIA 2: solo desaparecen las lineas declaradas como sustitucion EN LINEA
    viejas = [l for l in src.split('\n') if l.strip() and not any(a.strip().split('\n')[0] in l for a in EN_LINEA)]
    nuevas = set(l for l in t.split('\n') if l.strip())
    perdidas = [l for l in viejas if l not in nuevas]
    if perdidas:
        raise SystemExit(f"GUARDIA 2: {len(perdidas)} lineas del origen desaparecieron. Ejemplo:\n{perdidas[0][:160]}")
    # --- GUARDIA 3: compila
    compile(t, DESTINO, 'exec')
    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(t)
    print(f"ESCRITO {DESTINO}")
    print(f"  origen  organismo_f9.py   sha {SHA_ORIGEN}   -> destino mundo_fase10.py sha {h16(DESTINO)}")
    print(f"  cadena verificada: {len(CADENA)} shas hasta el TRONCO v14.1 · donantes verificados: {len(DONANTES)}")
    print(f"  anclas del origen {len(EN_LINEA) + sum(1 for d in DOC if d[2] == 'insercion')} (en linea {len(EN_LINEA)}) · lineas {len(src.splitlines())} -> {len(t.splitlines())}")
    print("  guardias: rng DEL ORGANISMO OK (2 excepciones declaradas) · lineas del origen intactas OK · compila OK")
    print("\n  DOCUMENTACION DE ANCLAS (etiqueta | primera linea del ancla | tipo)")
    for d in DOC:
        print(f"    {d[0]:28s} | {d[1]:90s} | {d[2]}")


if __name__ == '__main__':
    main()
