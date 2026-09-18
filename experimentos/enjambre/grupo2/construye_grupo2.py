"""MINI-EQUIPO 2 (enjambre) — construye `organismo_g2.py` POR ANCLAS desde
`experimentos/creacion_A/organismo_v13q5.py` (`fae9c32b146fdbb4`, SOLO SE LEE, no se edita).

MECANISMO M2 -- FISION DE LA VIA LENTA POR CONFLICTO DE SIGNO (ver PREREGISTRO_g2.md para la justificacion
completa). Perilla nueva: `fision=None|'conflicto'`, `fis_umbral=3.0`, `fis_rho=0.05`.

Con `fision=None` (por defecto) el organismo es `organismo_v13q5` EXACTO: la rama nueva de la regla nunca se
ejecuta (queda como `elif seleccion is not None:` de siempre) y `lenta(P)` cae directo en su linea original
intacta. Identidad bit a bit obligatoria: `identidad_g2.py`.

Con `fision='conflicto'`: el organismo arranca con 6 celdas "de un canal" (lectoras de {P_i, 1}). En cada
mordida, cuenta masa y suma de patrones por canal y signo de R; cada celda existente actualiza con SU PROPIO
residuo (delta rule sobre su propia base); cuando un canal acumula >= fis_umbral mordidas de cada signo, nace
UNA hija que lee {P_i, P_j, P_i*P_j, 1} con j = el canal que mas separa comida de veneno bajo i (maximo una
hija por canal, tope duro 6). La via lenta LEE la celda de menor error (`lenta(P)`).

NO edita `organismo_v13q5.py`. Sin commits. Sin Pool.
Uso: python construye_grupo2.py
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(AQUI, '..', '..', 'creacion_A', 'organismo_v13q5.py')
DEST = os.path.join(AQUI, 'organismo_g2.py')

src = open(ORIG, 'r', encoding='utf-8').read()
sha = hashlib.sha256(open(ORIG, 'rb').read()).hexdigest()[:16]
assert sha == 'fae9c32b146fdbb4', f'origen inesperado: {sha}'

# ---------------------------------------------------------------- ancla 1: firma
A1 = "sel_estad='cond',lab=False):"
B1 = "sel_estad='cond',lab=False,fision=None,fis_umbral=3.0,fis_rho=0.05):"
assert src.count(A1) == 1, 'ancla 1'

# ---------------------------------------------------------------- ancla 2: estado y memoria de M2
A2 = "    Ws=np.zeros(_NF)   # 3d: vector con signo de la via lenta; solo se mueve/lee si regla_lenta=='delta_signo'"
B2 = (
    "    if fision not in (None,'conflicto'): raise ValueError(f\"fision={fision!r}\")"
    "   # M2 (enjambre grupo2): un knob mal escrito NO puede caer en silencio al brazo original\n"
    "    _FC=[([_i],np.zeros(2)) for _i in range(6)]; _FE=np.full(64,1e9)"
    "   # M2: 6 lectores de UN canal {P_i,1}; error EMA por celda (holgado; tope duro 12 celdas)\n"
    "    _Fmp=np.zeros(6); _Fmn=np.zeros(6); _Fsp=np.zeros((6,6)); _Fsn=np.zeros((6,6)); _Fcp=np.zeros(6); _Fcn=np.zeros(6)"
    "   # M2: masa y suma de patrones por canal y signo de R\n"
    "    _Fhij=[]; _FG=0"
    "   # M2: canales que ya parieron (maximo 1 hija cada uno); indice en _FC de la celda ganadora (menor _FE)\n"
    + A2
)
assert src.count(A2) == 1, 'ancla 2'

# ---------------------------------------------------------------- ancla 3: lectura de la via lenta (celda ganadora)
A3 = "        _ph=phi(P); return float(Ws@_ph) if regla_lenta=='delta_signo' else float((Wps-Wns)@_ph)"
B3 = (
    "        if fision is not None:"
    "   # M2: lee la celda GANADORA (menor error) con SU PROPIA base; hija = {P_i,P_j,P_i*P_j,1}\n"
    "            _g,_w=_FC[_FG]\n"
    "            _a=np.array([P[_g[0]],1.0]) if len(_g)==1 else np.array([P[_g[0]],P[_g[1]],P[_g[0]]*P[_g[1]],1.0])\n"
    "            return float(_w@_a)\n"
    + A3
)
assert src.count(A3) == 1, 'ancla 3'

# ---------------------------------------------------------------- ancla 4: la regla local de M2 (antes de `seleccion`)
A4 = "                        if seleccion is not None:   # creacion_A A-1(ii): elegibilidad por rasgo, competencia entre candidatos, y la via lenta aprende SOLO lo abierto"
B4 = (
    "                        if fision is not None:"
    "   # M2 (enjambre grupo2): fision de la via lenta por conflicto de signo; SEÑAL = R de la propia mordida, nada mas\n"
    "                            _Pk=P_[kk]\n"
    "                            for _i in range(6):"
    "   # (a) masa y suma de patrones por canal activo, partida por signo de R\n"
    "                                if _Pk[_i]==1.0:\n"
    "                                    if R>0: _Fmp[_i]+=1; _Fsp[_i]+=_Pk; _Fcp[_i]+=1\n"
    "                                    else:   _Fmn[_i]+=1; _Fsn[_i]+=_Pk; _Fcn[_i]+=1\n"
    "                            for _c in range(len(_FC)):"
    "   # (b) cada celda actualiza con SU PROPIO residuo sobre SU PROPIA base (misma memoria que las celdas KW del tronco)\n"
    "                                _cg,_cw=_FC[_c]\n"
    "                                _ca=np.array([_Pk[_cg[0]],1.0]) if len(_cg)==1 else np.array([_Pk[_cg[0]],_Pk[_cg[1]],_Pk[_cg[0]]*_Pk[_cg[1]],1.0])\n"
    "                                _dc=R-float(_cw@_ca)\n"
    "                                _FE[_c]=(1-fis_rho)*_FE[_c]+fis_rho*_dc*_dc\n"
    "                                _FC[_c]=(_cg,np.clip(_cw+eta_s*_dc*_ca,-clip_s,clip_s))\n"
    "                            for _i in range(6):"
    "   # (c) FISION: nace UNA hija del canal que MAS separa comida de veneno bajo i (v11: el mismo dist=P-mu, partido por signo); tope 1 por canal (6 en total)\n"
    "                                if _Pk[_i]==1.0 and _i not in _Fhij and len(_Fhij)<6 and min(_Fmp[_i],_Fmn[_i])>=fis_umbral:\n"
    "                                    _cands=[_k for _k in range(6) if _k!=_i]\n"
    "                                    _j=max(_cands,key=lambda _k:abs(_Fsp[_i][_k]/_Fcp[_i]-_Fsn[_i][_k]/_Fcn[_i]))\n"
    "                                    _FC.append(([_i,_j],np.zeros(4))); _Fhij.append(_i)\n"
    "                            _FG=int(min(range(len(_FC)),key=lambda _c:_FE[_c]))"
    "   # (d) la via lenta lee, de aqui en adelante, la celda de menor error\n"
    "                        elif seleccion is not None:   # creacion_A A-1(ii): elegibilidad por rasgo, competencia entre candidatos, y la via lenta aprende SOLO lo abierto"
)
assert src.count(A4) == 1, 'ancla 4'

# ---------------------------------------------------------------- ancla 5: el return (lecturas nuevas de M2)
A5 = "    return dict(lab=lab,lenta_eventos=_ev5,fase2_en=fase2_en,seleccion=seleccion,"
B5 = ("    return dict(lab=lab,lenta_eventos=_ev5,fase2_en=fase2_en,"
      "fis_celdas=[list(g) for g,_ in _FC],fis_ganadora=list(_FC[_FG][0]),fis_n=len(_FC),seleccion=seleccion,")
assert src.count(A5) == 1, 'ancla 5'

cab = ('"""organismo_g2 = organismo_v13q5.py (%s) + perilla `fision` (M2 -- FISION DE LA VIA LENTA POR CONFLICTO\n'
       'DE SIGNO: el rasgo conjuntivo NACE por conflicto de signo por canal en vez de elegirse de una base\n'
       'prefijada; reusa el principio de v11 (`Wb[c]*R<0`) para la via lenta). Knobs: fision=None|\'conflicto\',\n'
       'fis_umbral=3.0, fis_rho=0.05.\n'
       'Generado por experimentos/enjambre/grupo2/construye_grupo2.py. NO editar a mano.\n'
       'Con fision=None es organismo_v13q5 EXACTO (identidad obligatoria: identidad_g2.py)."""\n' % sha)

out = cab + src.replace(A1, B1).replace(A2, B2).replace(A3, B3).replace(A4, B4).replace(A5, B5)
open(DEST, 'w', encoding='utf-8').write(out)
print(f'origen organismo_v13q5.py sha {sha}')
print(f'escrito organismo_g2.py    sha {hashlib.sha256(open(DEST,"rb").read()).hexdigest()[:16]}')
