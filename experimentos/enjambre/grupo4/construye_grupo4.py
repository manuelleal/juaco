"""MINI-EQUIPO 4 (enjambre) -- construye `organismo_g4.py` POR ANCLAS desde
`experimentos/creacion_A/organismo_v13q5.py` (fae9c32b146fdbb4, SOLO LECTURA).

UNICA perilla nueva: `tabla_g=None|dict(g=1|2, estad='mse'|'signo', modo='dura'|'mezcla', tau, eta, rho, alpha, clip)`.
Mecanismo M4 (oraculo de laboratorio, version en-organismo): reemplaza la lectura y actualizacion de la via lenta
por una TABLA por grupos de pixeles de grado `g` (g=1: 6 canales elementales; g=2: 15 pares) mas un ESTADISTICO DE
COMPETENCIA por grupo (evaluado ANTES de actualizar la celda, para no filtrar el dato consigo mismo) que decide,
WTA duro o mezcla softmax, que grupo lee la boca. Con `tabla_g=None` (por defecto) NO se ejecuta ni una linea nueva
dentro del bucle: identidad bit a bit obligatoria (arnes: identidad_g4.py).

Alcance declarado (para no inflar): implementa g en {1,2} (no 3, por tiempo), estimador 'tabla' (EMA) unicamente
(no tabla_binaria ni MCR por celda), estadistico 'mse' y 'signo' (no cobertura ni primer-encuentro), lectura dura
y mezcla softmax con tau configurable. eta/rho separados como pide el mecanismo (eta = tasa de la tabla, rho = tasa
del estadistico de competencia, DISTINTO de eta_s/clip_s del tronco aunque clip por defecto los reusa).

NO edita ningun original. Sin commits. Trabaja solo en experimentos/enjambre/grupo4/.
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(AQUI, '..', '..', 'creacion_A', 'organismo_v13q5.py')
DEST = os.path.join(AQUI, 'organismo_g4.py')

src = open(ORIG, 'r', encoding='utf-8').read()
sha = hashlib.sha256(open(ORIG, 'rb').read()).hexdigest()[:16]
assert sha == 'fae9c32b146fdbb4', f'origen inesperado: {sha}'

# ---- ancla 1: firma -- agrega tabla_g=None antes de lab=False
A1 = "sel_calienta=0,sel_estad='cond',lab=False):"
B1 = "sel_calienta=0,sel_estad='cond',tabla_g=None,lab=False):"
assert src.count(A1) == 1, 'ancla 1 (firma)'

# ---- ancla 2: estado -- inicializa la tabla por grupos, justo despues de la eligibilidad A-1(ii)
A2 = ("    _e4=np.zeros(_NF); _ab4=np.ones(_NF,bool); _cand4=np.zeros(_NF,bool); _abre4=[]; _nsel4=0   "
      "# creacion_A A-1(ii): elegibilidad, bit de abierto, mascara de candidatos, historia de aperturas, contador de mordidas")
assert src.count(A2) == 1, 'ancla 2 (estado)'
_ind2 = A2[:len(A2) - len(A2.lstrip(' '))]  # indentacion de la ancla (4 espacios), calculada, no a mano
_B2_extra = (
    "\n{i}_g4_on=tabla_g is not None   # grupo4 (M4): tabla por grupos de pixeles + competencia; None/apagado = organismo_v13q5 exacto\n"
    "{i}if _g4_on:\n"
    "{i}    _g4_g=int(tabla_g.get('g',2)); _g4_estad=tabla_g.get('estad','mse'); _g4_modo=tabla_g.get('modo','dura')\n"
    "{i}    _g4_tau=float(tabla_g.get('tau',1.0)); _g4_eta=float(tabla_g.get('eta',0.15)); _g4_rho=float(tabla_g.get('rho',0.05))\n"
    "{i}    _g4_alpha=float(tabla_g.get('alpha',1.0)); _g4_clip=float(tabla_g.get('clip',clip_s))\n"
    "{i}    _g4_grupos=list(itertools.combinations(range(6),_g4_g)); _g4_ng=len(_g4_grupos)\n"
    "{i}    _g4_tabla=np.zeros((_g4_ng,2**_g4_g)); _g4_vistos=np.zeros((_g4_ng,2**_g4_g),bool)\n"
    "{i}    _g4_ecomp=np.zeros(_g4_ng); _g4_npos=np.zeros(_g4_ng); _g4_abre=[]; _g4_ganador_prev=-1\n"
    "{i}def _g4_idx(P,gi):   # grupo4: codigo binario (0..2**g-1) de los pixeles del grupo gi en el patron P\n"
    "{i}    _c=0\n"
    "{i}    for _p in _g4_grupos[gi]: _c=_c*2+(1 if P[_p]>0.5 else 0)\n"
    "{i}    return _c"
).format(i=_ind2)
B2 = A2 + _B2_extra

# ---- ancla 3: lectura de la via lenta -- tabla_g tiene prioridad si esta activo
A3 = ("    def lenta(P):   # 3d: lectura de la via lenta sola segun regla_lenta ('dos_canales' = la formula original, exacta)\n"
      "        _ph=phi(P); return float(Ws@_ph) if regla_lenta=='delta_signo' else float((Wps-Wns)@_ph)")
assert src.count(A3) == 1, 'ancla 3 (lenta)'
B3 = ("    def lenta(P):   # 3d: lectura de la via lenta sola segun regla_lenta ('dos_canales' = la formula original, exacta); grupo4: tabla_g tiene prioridad si esta activo\n"
      "        if _g4_on:\n"
      "            _codes=[_g4_idx(P,gi) for gi in range(_g4_ng)]\n"
      "            _preds=np.array([_g4_tabla[gi,_codes[gi]] for gi in range(_g4_ng)])\n"
      "            if _g4_modo=='dura': return _g4_alpha*float(_preds[int(np.argmax(_g4_ecomp))])\n"
      "            _w=_g4_ecomp/max(_g4_tau,1e-9); _w=np.exp(_w-_w.max()); _w=_w/_w.sum()\n"
      "            return _g4_alpha*float((_w*_preds).sum())\n"
      "        _ph=phi(P); return float(Ws@_ph) if regla_lenta=='delta_signo' else float((Wps-Wns)@_ph)")

# ---- ancla 4: actualizacion en la mordida -- _g4_on tiene prioridad sobre seleccion/regla_lenta
A4 = ("                        if seleccion is not None:   # creacion_A A-1(ii): elegibilidad por rasgo, competencia entre "
      "candidatos, y la via lenta aprende SOLO lo abierto")
assert src.count(A4) == 1, 'ancla 4 (actualizacion)'
_ind4 = A4[:len(A4) - len(A4.lstrip(' '))]
_B4_pre = (
    "{i}if _g4_on:   # grupo4 (M4): tabla por grupos + competencia; el estadistico se mide ANTES de actualizar la celda (no se filtra el dato consigo mismo)\n"
    "{i}    for _gi in range(_g4_ng):\n"
    "{i}        _c=_g4_idx(P_[kk],_gi); _g4_npos[_gi]+=1\n"
    "{i}        _pred_antes=_g4_tabla[_gi,_c] if _g4_vistos[_gi,_c] else 0.0\n"
    "{i}        if _g4_estad=='mse': _g4_ecomp[_gi]=(1-_g4_rho)*_g4_ecomp[_gi]-_g4_rho*((_ds-_pred_antes)**2)\n"
    "{i}        else: _g4_ecomp[_gi]=(1-_g4_rho)*_g4_ecomp[_gi]+_g4_rho*(1.0 if (_pred_antes>0)==(_ds>0) else (0.0 if _pred_antes==0 else -1.0))\n"
    "{i}        _g4_tabla[_gi,_c]=np.clip((_g4_tabla[_gi,_c]+_g4_eta*(_ds-_g4_tabla[_gi,_c])) if _g4_vistos[_gi,_c] else _ds,-_g4_clip,_g4_clip)\n"
    "{i}        _g4_vistos[_gi,_c]=True\n"
    "{i}    _g4_gan=int(np.argmax(_g4_ecomp))\n"
    "{i}    if _g4_gan!=_g4_ganador_prev: _g4_abre.append((int(t),_g4_gan,list(_g4_grupos[_g4_gan]))); _g4_ganador_prev=_g4_gan\n"
).format(i=_ind4)
B4 = _B4_pre + A4.replace('if seleccion', 'elif seleccion', 1)

# ---- ancla 5: return -- agrega claves nuevas (reporte), NINGUNA reemplaza una existente
A5 = "    return dict(lab=lab,lenta_eventos=_ev5,fase2_en=fase2_en,seleccion=seleccion,"
assert src.count(A5) == 1, 'ancla 5 (return)'
B5 = (A5 +
      "tabla_g=tabla_g,"
      "g4_ganador=(list(_g4_grupos[int(np.argmax(_g4_ecomp))]) if _g4_on else None),"
      "g4_abre=(_g4_abre if _g4_on else []),"
      "g4_npos=([int(x) for x in _g4_npos] if _g4_on else []),"
      "g4_abre_conjuntivo_correcto=(bool(_g4_on and _g4_g==2 and regla=='xor01' and tuple(_g4_grupos[int(np.argmax(_g4_ecomp))])==(0,1)) if _g4_on else None),")

cab = ('"""organismo_g4 = organismo_v13q5.py (%s) + perilla `tabla_g` (grupo4/M4: tabla por grupos de pixeles de grado g\n'
       'con estadistico de competencia, alternativa a regla_lenta/seleccion para la via lenta). Generado por\n'
       'experimentos/enjambre/grupo4/construye_grupo4.py. NO editar a mano.\n'
       'Con tabla_g=None es organismo_v13q5 EXACTO en TODAS las claves de organismo_v13q5 (arnes: identidad_g4.py,\n'
       'comparacion por subconjunto de claves porque este archivo agrega claves de reporte nuevas -- mismo patron que\n'
       'construye_v13q5.py agregando `lab`/`lenta_eventos` sobre v13q4)."""\n' % sha)

out = src.replace(A1, B1).replace(A2, B2).replace(A3, B3).replace(A4, B4).replace(A5, B5)
assert out.count('_g4_on') >= 5, 'las anclas no engancharon todas (revisar)'
open(DEST, 'w', encoding='utf-8').write(cab + out)
print(f'origen organismo_v13q5.py sha {sha}')
print(f'escrito organismo_g4.py   sha {hashlib.sha256(open(DEST,"rb").read()).hexdigest()[:16]}')
