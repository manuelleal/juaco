"""MINI-EQUIPO 1 (sala enjambre) — construye `organismo_g1.py` POR ANCLAS desde
`experimentos/creacion_A/organismo_v13q5.py` (`fae9c32b146fdbb4`, SOLO se lee).

MECANISMO M1 — COMPARTIMENTOS DE DOS CANALES: 15 lectores pequenos (uno por cada par de pixeles, C(6,2)=15),
cada uno un lector LINEAL de 4 entradas [P_i, P_j, P_i*P_j, 1], que aprenden EN PARALELO con la regla delta que
el tronco ya usa (nada nuevo cruza al organismo) y compiten por su propio error de prediccion (k-WTA, k=1): la
via lenta LEE solo al que tiene el error mas bajo. Fundamento: Caron, Ruta, Abbott & Axel 2013 (pocos canales
fijos al nacer por celula de Kenyon); Modi, Shuai & Turner 2020 (~15 compartimentos DAN/MBON en paralelo, cada
uno con su propia señal de enseñanza); Dasgupta, Stevens & Navlakha 2017 (expansion + ganador-se-lo-lleva-todo,
estructural); Lipshutz et al. 2023 (el lector KC->MBON real es lineal). Diagnostico de la sesion del 18-sep:
UN lector lineal sobre 21 rasgos reparte el credito entre los 6 pixeles y con 8 patrones de tren no hay forma
de preferir al rasgo P0*P1 correcto; lo que distingue es partir la lectura en grupos de POCOS CANALES y elegir
duro entre ellos.

UNICA perilla nueva: `celdas=None|'par2'` (mas `cel_rho=0.02`, ya fijo). Con `celdas=None` (por defecto) es
`organismo_v13q5` EXACTO — identidad bit a bit obligatoria (`identidad_g1.py`). Con `celdas='par2'` la via lenta
LEE la celda ganadora en vez de `Ws`/`Wps-Wns`; nada mas del organismo cambia (misma boca, mismo tren rapido).

Estado nuevo (nace con el organismo, nunca cambia de canales): `_PAR` los 15 pares fijos; `_CW` (15x4) el peso de
cada celda; `_CE` (15,) su error EMA propio (cel_rho=0.02); `_CG` el indice de la celda ganadora vigente.
Regla local, por mordida, con R el refuerzo de ESA mordida y P el patron mordido: para cada celda c=(i,j),
a_c=[P_i,P_j,P_i*P_j,1]; d_c=R-W_c@a_c (su propio residuo); E_c <- (1-cel_rho)*E_c+cel_rho*d_c^2 (primera vez
E_c=d_c^2, via el centinela _CE>=1e9 del nacimiento); W_c <- clip(W_c+eta_s*d_c*a_c,-clip_s,+clip_s); ganadora
= argmin_c E_c. Ninguna senal cruza celdas, no hay gradiente, no hay vector de error por unidad — solo R, el
mismo escalar que la via lenta ya usa (tercer factor).

NO edita el original. Sin commits. Sin Pool.
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(AQUI, '..', '..', 'creacion_A', 'organismo_v13q5.py')
DEST = os.path.join(AQUI, 'organismo_g1.py')

src = open(ORIG, 'r', encoding='utf-8').read()
sha = hashlib.sha256(open(ORIG, 'rb').read()).hexdigest()[:16]
assert sha == 'fae9c32b146fdbb4', f'origen inesperado: {sha}'

# ---- ancla 1: firma — anade `celdas=None,cel_rho=0.02` al final de los parametros de run()
A1 = "sel_estad='cond',lab=False):"
B1 = "sel_estad='cond',lab=False,celdas=None,cel_rho=0.02):"
assert src.count(A1) == 1, 'ancla 1'

# ---- ancla 2: estado nuevo — justo ANTES de `Ws=np.zeros(_NF)` (para que la validacion corra ANTES de cualquier uso)
A2 = "    Ws=np.zeros(_NF)   # 3d: vector con signo de la via lenta; solo se mueve/lee si regla_lenta=='delta_signo'"
B2 = ("    if celdas not in (None,'par2'): raise ValueError(f\"celdas={celdas!r}\")   # enjambre/grupo1: un knob mal escrito NO puede caer en silencio al brazo original\n"
      "    _PAR=[(i,j) for i in range(6) for j in range(i+1,6)]   # M1: los C(6,2)=15 pares de pixeles, fijos al nacer (como PN->KC)\n"
      "    _CW=np.zeros((15,4)); _CE=np.full(15,1e9); _CG=0   # M1: peso x celda (4 canales), error EMA propio x celda, celda ganadora vigente\n"
      + A2)
assert src.count(A2) == 1, 'ancla 2'

# ---- ancla 3: lectura — dentro de `def lenta(P):`, ANTEPONER (la linea original queda INTACTA, es el brazo apagado)
A3 = ("    def lenta(P):   # 3d: lectura de la via lenta sola segun regla_lenta ('dos_canales' = la formula original, exacta)\n"
      "        _ph=phi(P); return float(Ws@_ph) if regla_lenta=='delta_signo' else float((Wps-Wns)@_ph)")
B3 = ("    def lenta(P):   # 3d: lectura de la via lenta sola segun regla_lenta ('dos_canales' = la formula original, exacta)\n"
      "        if celdas is not None: _i,_j=_PAR[_CG]; return float(_CW[_CG]@np.array([P[_i],P[_j],P[_i]*P[_j],1.0]))   # M1: lee SOLO la celda ganadora\n"
      "        _ph=phi(P); return float(Ws@_ph) if regla_lenta=='delta_signo' else float((Wps-Wns)@_ph)")
assert src.count(A3) == 1, 'ancla 3'

# ---- ancla 4: la regla — rama nueva ANTES de `if seleccion is not None:`, que pasa a ser `elif`
A4 = "                        if seleccion is not None:   # creacion_A A-1(ii): elegibilidad por rasgo, competencia entre candidatos, y la via lenta aprende SOLO lo abierto"
B4 = ("                        if celdas is not None:   # enjambre/grupo1 M1: 15 lectores de 2 canales (pares de pixeles), k-WTA (k=1) por su propio error\n"
      "                            _Pk=P_[kk]; _A=np.array([[_Pk[_i],_Pk[_j],_Pk[_i]*_Pk[_j],1.0] for _i,_j in _PAR])   # a_c de las 15 celdas para este patron\n"
      "                            _dc=R-(_CW*_A).sum(axis=1); _dc2=_dc*_dc   # d_c = R - W_c@a_c (residuo PROPIO de cada celda, no el _ds global)\n"
      "                            _CE=np.where(_CE>=1e9,_dc2,(1-cel_rho)*_CE+cel_rho*_dc2)   # EMA propia; centinela 1e9 = primera mordida, E_c=d_c^2\n"
      "                            _CW=np.clip(_CW+eta_s*_dc[:,None]*_A,-clip_s,clip_s)   # delta local, mismas eta_s/clip_s del tronco (v14.1)\n"
      "                            _CG=int(np.argmin(_CE))   # ganadora = la de menor error EMA; la via lenta ya solo LEE esta (ancla 3)\n"
      "                        elif seleccion is not None:   # creacion_A A-1(ii): elegibilidad por rasgo, competencia entre candidatos, y la via lenta aprende SOLO lo abierto")
assert src.count(A4) == 1, 'ancla 4'

# ---- ancla 5: el return
# OJO — CORRECCION al mecanismo del jefe: el original YA devuelve una clave `celdas=int(activa.sum())`
# (num. de celulas de Kenyon activas, splits/capacidad). Ecoar el knob nuevo como `celdas=celdas` aqui
# choca (SyntaxError: keyword argument repeated) y ademas pisaria en silencio el significado viejo si
# Python lo permitiera. Se renombra el eco del knob a `cel_modo` (prefijo `cel_` ya usado por
# cel_rho/cel_ganadora/cel_E); la `celdas` original (Kenyon) queda intacta y sin ambiguedad.
A5 = "    return dict(lab=lab,"
B5 = "    return dict(cel_modo=celdas,cel_ganadora=(None if celdas is None else list(_PAR[_CG])),cel_E=[round(float(x),4) for x in _CE],lab=lab,"
assert src.count(A5) == 1, 'ancla 5'

cab = ('"""organismo_g1 = organismo_v13q5.py (%s) + perilla `celdas` (M1, enjambre/grupo1): 15 lectores lineales\n'
       'de 2 canales (un par de pixeles cada uno, fijos al nacer) que compiten por su propio error EMA propio\n'
       '(k-WTA, k=1); la via lenta lee SOLO la celda ganadora. Ver mecanismo completo en construye_grupo1.py.\n'
       'Generado por experimentos/enjambre/grupo1/construye_grupo1.py. NO editar a mano.\n'
       'Con celdas=None es organismo_v13q5 EXACTO (identidad obligatoria: identidad_g1.py)."""\n' % sha)
out = cab + src.replace(A1, B1).replace(A2, B2).replace(A3, B3).replace(A4, B4).replace(A5, B5)
open(DEST, 'w', encoding='utf-8').write(out)
print(f'origen organismo_v13q5.py sha {sha}')
print(f'escrito organismo_g1.py   sha {hashlib.sha256(open(DEST,"rb").read()).hexdigest()[:16]}')
