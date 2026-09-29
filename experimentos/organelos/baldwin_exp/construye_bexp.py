"""construye_bexp.py — construye motor_bexp.py POR ANCLAS desde experimentos/organelos/baldwin/motor_baldwin.py (sha d0a620d2f5e2605e;
el de la serie BALDWIN = NO, commit 43f1a6df). NO toca el origen.

Mision: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). BALDWIN CON EXPLORACION (29-sep-2026): hipotesis NUEVA con su propio preregistro (no rescate del NO de Baldwin).

Lo nuevo (BQ_CFG exp, eps_exp, th_exp; exp = 0 no cambia NADA de la simulacion: motor_baldwin bit a bit, arnes identidad_bexp.py):
  EXPLORACION LOCAL LIGADA A LA RESERVA (opcion ii del encargo; el 'prueba solo si aguanta el golpe' de O1). En cada decision de boca
  (el cuerpo esta sobre una letra), si la boca decidio NO morder, la suma de sus reglas de boca activas es NEGATIVA (una regla de
  rechazo empujo al no) y su reserva menor min(E, Ag) >= th_exp, con prob. eps_exp muerde de todos modos. La mordida exploratoria es una
  mordida REAL (mismo efecto EFF, misma R, mismo aprendizaje del cerebro; si el cuerpo tiene reglas plasticas de boca, reciben su
  consecuencia por la via de motor_baldwin, _reglas_aprende). El sorteo usa el rng PROPIO DEL CUERPO (GL[s], el de la boca) y SOLO se
  consume cuando se cumplen las tres condiciones y exp != 0: con exp = 0 no se consume nada.
  Memoria nueva: CERO (eps_exp y th_exp son constantes del mundo experimental, iguales para todos; no son genes).
  Instrumentacion (no toca la simulacion): contadores PLC[2..15] (mordidas exploratorias, cuantas hicieron aprender a una regla,
  vetos, vetos con reserva, pasos-cuerpo, R de la exploracion) y |w - w0| de las reglas plasticas de boca de CADA CUERPO QUE MUERE
  (hallazgo del auditor de BALDWIN: se media solo en los vivos en T).

Uso:  python construye_bexp.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
ORIGEN = os.path.join(ORG, 'baldwin', 'motor_baldwin.py')
SHA_ORIGEN = 'd0a620d2f5e2605e'
DESTINO = os.path.join(AQUI, 'motor_bexp.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


A = []
A.append(('X0 docstring', '"""motor_baldwin.py (CONSTRUIDO por',
'''"""motor_bexp.py (CONSTRUIDO por experimentos/organelos/baldwin_exp/construye_bexp.py desde
experimentos/organelos/baldwin/motor_baldwin.py, sha d0a620d2f5e2605e; NO editar a mano). BALDWIN CON EXPLORACION: si la boca rechaza
por sus reglas y la reserva aguanta el golpe (min(E, Ag) >= th_exp), con prob. eps_exp muerde igual (mordida real). Con exp = 0 es
motor_baldwin bit a bit (salvo contadores nuevos). Lo que sigue es el docstring del origen.

motor_baldwin.py (CONSTRUIDO por'''))
A.append(('X1 firma', "FIRMA_GEMELO = 'motor_baldwin v0'", "FIRMA_GEMELO = 'motor_bexp v0'"))
A.append(('X2 cfg', "plast=0, p_bit=0.01, p_ins_pl=0.5, forzada_bit=None)   # BALDWIN",
          "plast=0, p_bit=0.01, p_ins_pl=0.5, forzada_bit=None,   # BALDWIN\n              exp=0, eps_exp=0.0, th_exp=0.5)   # BEXP"))
A.append(('X3 BQ', "st['BQ'] = np.array([int(C['on']), int(C.get('kit', 1)), int(C.get('plast', 0))], np.int64)",
          "st['BQ'] = np.array([int(C['on']), int(C.get('kit', 1)), int(C.get('plast', 0)),   # BEXP: + exp, eps y th en millonesimas\n"
          "                         int(C.get('exp', 0)), int(round(float(C.get('eps_exp', 0.0)) * 1e6)), int(round(float(C.get('th_exp', 0.5)) * 1e6))], np.int64)\n"
          "    if int(C.get('exp', 0)) and (not C['on'] or int(C.get('kit', 1)) != 1): raise ValueError('BEXP: exp exige on = 1 y kit 1')"))
A.append(('X4 contadores', "    if 'PLC' not in st: st['PLC'] = np.zeros(4, np.int64)   # BALDWIN: contadores (viajan en el checkpoint como clave del estado)",
          "    if 'PLC' not in st: st['PLC'] = np.zeros(16, np.int64)   # BEXP: 4 de BALDWIN + 12 de la exploracion y de los muertos (viajan en el checkpoint)"))
A.append(('X5 init por cuerpo', "            wf_ = 0.0; ws_ = 0.0; key = 0",
          "            wf_ = 0.0; ws_ = 0.0; key = 0\n            brb = 0.0; explo = False   # BEXP\n"
          "            if BQ[2] != 0 or BQ[3] != 0: PLC[12] += 1   # BEXP: pasos-cuerpo (instrumento)"))
A.append(('X6 boca', "                    else: Vb += _reglas_boca(s, RG, RN, RM, E, Ag, d, kk, PATM)",
          "                    else:\n                        brb = _reglas_boca(s, RG, RN, RM, E, Ag, d, kk, PATM)   # BEXP: la suma de las reglas, aparte\n"
          "                        Vb += brb"))
A.append(('X7 exploracion', "                mordio = r.random() < pb\n",
"""                mordio = r.random() < pb
                if brb < 0.0 and not mordio and (BQ[2] != 0 or BQ[3] != 0):   # BEXP: las reglas vetaron la mordida
                    PLC[4] += 1
                    if (E if E < Ag else Ag) >= BQ[5] * 1e-6:   # la reserva aguanta el golpe
                        PLC[5] += 1
                        if BQ[3] != 0 and r.random() < BQ[4] * 1e-6:   # EXPLORA: muerde igual (rng del cuerpo, solo aqui)
                            mordio = True; explo = True; PLC[2] += 1
"""))
A.append(('X8 R de la exploracion', "                    R = RV[kk, na]; bf[s, F_R] = R\n",
"""                    R = RV[kk, na]; bf[s, F_R] = R
                    if explo:   # BEXP (instrumento): que trajo la mordida exploratoria
                        if R > 0: PLC[11] += 1
                        elif R < 0: PLC[13] += 1
"""))
A.append(('X9 aprende', "                        _reglas_aprende(s, RG, RN, RM, RPL, E, Ag, d, kk, PATM, Rt, bf[s, F_ETAS], bf[s, F_AV], PLC)\n",
"""                        m1_ = PLC[1]
                        _reglas_aprende(s, RG, RN, RM, RPL, E, Ag, d, kk, PATM, Rt, bf[s, F_ETAS], bf[s, F_AV], PLC)
                        if explo and PLC[1] > m1_: PLC[3] += 1   # BEXP: la exploracion hizo aprender a una regla plastica
"""))
A.append(('X10 muerte', "                li[lin, L_DEATHS] += 1; li[lin, L_MN0 if porE else L_MN1] += 1\n",
"""                if BQ[2] != 0: _pl_muerto(s, RG, RN, RPL, PLC)   # BEXP (instrumento): |w - w0| de las plasticas de boca del muerto
                li[lin, L_DEATHS] += 1; li[lin, L_MN0 if porE else L_MN1] += 1
"""))
A.append(('X11 final', "    if int(_CTX['BQC'].get('plast', 0)): _bq_final_pl(st, vivos)   # BALDWIN\n",
"""    if int(_CTX['BQC'].get('plast', 0)): _bq_final_pl(st, vivos)   # BALDWIN
    if int(_CTX['BQC'].get('plast', 0)) or int(_CTX['BQC'].get('exp', 0)): _bq_final_exp(st, vivos)   # BEXP
"""))

NUEVO = '''

# ================================================================ BEXP (anadido por construye_bexp.py)
DW_MOV = 0.05   # una regla plastica 'aprendio' si |w - w0| > 0.05 (instrumento; declarado en el preregistro)


@njit(cache=True)
def _pl_muerto(s, RG, RN, RPL, PLC):
    """Al morir: [6] reglas plasticas de boca, [7] suma |w - w0| (millonesimas), [8] de ellas con |w - w0| > DW_MOV,
    [9] muertos con >= 1 plastica de boca, [10] muertos con >= 1 plastica movida. Solo LEE el cuerpo."""
    npl = 0; nmov = 0
    for r in range(RN[s]):
        if int(RG[s, r, 4]) != 0 or RPL[s, r, 0] < 0.5: continue
        dw = RG[s, r, 5] - RPL[s, r, 1]
        if dw < 0: dw = -dw
        npl += 1; PLC[7] += int(dw * 1e6)
        if dw > DW_MOV: nmov += 1
    PLC[6] += npl; PLC[8] += nmov
    if npl > 0: PLC[9] += 1
    if nmov > 0: PLC[10] += 1


def _bq_final_exp(st, vivos):
    P_ = st['PLC']; npl = 0; nmov = 0; sdw = 0.0
    if int(_CTX['BQC'].get('plast', 0)):
        for s in vivos:
            for r in range(int(st['RN'][s])):
                if int(st['RG'][s, r, 4]) != 0 or st['RPL'][s, r, 0] < 0.5: continue
                dw = abs(float(st['RG'][s, r, 5] - st['RPL'][s, r, 1])); npl += 1; sdw += dw; nmov += dw > DW_MOV
    BQ_OUT['exp'] = dict(n_mord_exp=int(P_[2]), n_mord_exp_aprende=int(P_[3]), n_veto=int(P_[4]), n_veto_res=int(P_[5]),
                         n_cuerpo_paso=int(P_[12]), n_exp_R_pos=int(P_[11]), n_exp_R_neg=int(P_[13]),
                         muertos=dict(n_reglas_pl=int(P_[6]), sum_dw=round(int(P_[7]) * 1e-6, 4), n_movidas=int(P_[8]),
                                      n_cuerpos_pl=int(P_[9]), n_cuerpos_movidos=int(P_[10])),
                         vivos_T=dict(n_reglas_pl=npl, sum_dw=round(sdw, 4), n_movidas=int(nmov)))


# ================================================================ BLOQUES2 (anadido por construye_bloques2.py): el kit grande'''

A.append(('X12 bloque nuevo', "\n\n# ================================================================ BLOQUES2 (anadido por construye_bloques2.py): el kit grande", NUEVO))


def construye():
    if h16(ORIGEN) != SHA_ORIGEN: raise SystemExit(f'origen cambio: {h16(ORIGEN)} != {SHA_ORIGEN}')
    txt = open(ORIGEN, encoding='utf-8').read()
    for nom, viejo, nuevo in A:
        c = txt.count(viejo)
        if c != 1: raise SystemExit(f'ancla {nom}: aparece {c} veces (debe ser 1)')
        txt = txt.replace(viejo, nuevo)
    return txt


if __name__ == '__main__':
    t = construye()
    if '--verifica' in sys.argv:
        print('IGUAL' if os.path.exists(DESTINO) and open(DESTINO, encoding='utf-8').read() == t else 'DISTINTO', h16(DESTINO) if os.path.exists(DESTINO) else '-')
    else:
        with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f: f.write(t)
        print('escrito', DESTINO, h16(DESTINO), f'({len(A)} anclas, origen {SHA_ORIGEN})')
