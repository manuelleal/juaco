"""construye_bloques2.py — construye motor_bloques2.py POR ANCLAS desde motor_bloques.py (sha ff782697e54585a5, el de la serie
BLOQUES = FUNCIONA x2). EXPLORATORIO (Opus M, 28-sep-2026, noche): "¿y si le damos mas cosas?".

Mision: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros, y solo con seleccion natural.

KIT GRANDE (BQ_CFG kit = 2; kit = 1 es BLOQUES tal cual, bit a bit: arnes):
  sentidos nuevos: 6 reserva E (E/1.5)  7 reserva Ag (Ag/1.5)  8 R RECORDADA de la letra en foco ((R+3)/4; 0.75 si nunca la mordio)
                   9 R recordada de la letra p % 4   10 cercania del VECINO mas cercano (1 - min(d,10)/10; 0 si no hay)
                   11 el vecino mordio en su ultimo turno (0/1)   12 tiempo desde el ultimo parto (o nacimiento), min(dt, 2000)/2000
  acciones nuevas: 4 patas hacia el VECINO (w > 0: seguirlo; w < 0: alejarse)   5 ventana de parto: rep_X efectivo x clip(1 - 0.1 sum w, 0.3, 2)
                   (w > 0: parir antes; w < 0: esperar)
  tope de reglas: BQ_CFG tope (12 en kit 1; 16 en kit 2); dimension NRMAX = 16.
Memoria nueva por cuerpo (solo la leen las reglas): R recordada por letra (4), mordio en su ultimo turno (1), t del ultimo parto (1),
sesgo de ventana (1). Mismos operadores (mutar bloque o peso, duplicar, borrar, insertar, HGT del vecino).

Uso:  python construye_bloques2.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(AQUI, 'motor_bloques.py')
SHA_ORIGEN = 'ff782697e54585a5'
DESTINO = os.path.join(AQUI, 'motor_bloques2.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


A = []
A.append(('C0 docstring', '"""motor_bloques.py (CONSTRUIDO por',
'''"""motor_bloques2.py (CONSTRUIDO por experimentos/organelos/bloques/opusM/construye_bloques2.py desde motor_bloques.py, sha
ff782697e54585a5; NO editar a mano). KIT GRANDE de BLOQUES (kit = 2); con kit = 1 es motor_bloques bit a bit. Lo que sigue es el
docstring del origen.

motor_bloques.py (CONSTRUIDO por'''))
A.append(('C1 firma', "FIRMA_GEMELO = 'motor_bloques v0'", "FIRMA_GEMELO = 'motor_bloques2 v0'"))
A.append(('C2 constantes', "NRMAX = 12; NRC = 6; NRM = 3\n", "NRMAX = 16; NRC = 6; NRM = 10   # BLOQUES2: RM 3..6 R por letra, 7 mordio, 8 t parto, 9 ventana\n"))
A.append(('C3 cfg', "              inicial=None, forzada=None)", "              inicial=None, forzada=None, kit=1, tope=12)"))
A.append(('C4 patas', "                _reglas_mov(s, RG, RN, RM, V, E, Ag, d, k, left, PATM)\n",
"""                if BQ[1] == 2: _reglas_mov2(s, RG, RN, RM, V, E, Ag, d, k, left, PATM, t, pos, bi, cuer, nb, L)
                else: _reglas_mov(s, RG, RN, RM, V, E, Ag, d, k, left, PATM)
"""))
A.append(('C5 boca', "                    Vb += _reglas_boca(s, RG, RN, RM, E, Ag, d, kk, PATM)\n",
"""                    if BQ[1] == 2: Vb += _reglas_boca2(s, RG, RN, RM, E, Ag, d, kk, PATM, t, pos2, bi, cuer, nb, L)
                    else: Vb += _reglas_boca(s, RG, RN, RM, E, Ag, d, kk, PATM)
"""))
A.append(('C6 memoria por letra', "                    RM[s, 0] = kk; RM[s, 1] = R   # BLOQUES: la memoria que solo leen las reglas\n",
"                    RM[s, 0] = kk; RM[s, 1] = R; RM[s, 3 + kk] = R   # BLOQUES (+ BLOQUES2: R recordada por letra)\n"))
A.append(('C7 mordio', "            if traza:\n                it = wi[W_NTZ]",
"            RM[s, 7] = 1.0 if mordio else 0.0   # BLOQUES2: lo que el vecino puede ver\n            if traza:\n                it = wi[W_NTZ]"))
A.append(('C8 refundado', "                RM[s2, 0] = -1.0; RM[s2, 1] = 0.0; RM[s2, 2] = 0.0; RN[s2] = 0   # BLOQUES\n",
"""                RM[s2, 0] = -1.0; RM[s2, 1] = 0.0; RM[s2, 2] = 0.0; RN[s2] = 0   # BLOQUES
                for c_ in range(3, 8): RM[s2, c_] = 0.0
                RM[s2, 8] = t; RM[s2, 9] = 0.0   # BLOQUES2
"""))
A.append(('C9 hijo', "                    RM[s3, 0] = -1.0; RM[s3, 1] = 0.0; RM[s3, 2] = 0.0; RN[s3] = 0   # BLOQUES\n",
"""                    RM[s3, 0] = -1.0; RM[s3, 1] = 0.0; RM[s3, 2] = 0.0; RN[s3] = 0   # BLOQUES
                    for c_ in range(3, 8): RM[s3, c_] = 0.0
                    RM[s3, 8] = t; RM[s3, 9] = 0.0; RM[s, 8] = t   # BLOQUES2: nacimiento del hijo y ultimo parto del padre
"""))
A.append(('C10 ventana', "            if bi[s, I_GV] >= bf[s, F_RX]:\n",
"""            rx_ = bf[s, F_RX]
            if BQ[0] != 0 and RM[s, 9] != 0.0:   # BLOQUES2: accion 5 (ventana de parto)
                rx_ = rx_ * _clip(1.0 - 0.1 * RM[s, 9], 0.3, 2.0)
            if bi[s, I_GV] >= rx_:
"""))
A.append(('C11 BQ', "    C = dict(BQ_CFG); st['BQ'] = np.array([int(C['on'])], np.int64)",
"    C = dict(BQ_CFG); st['BQ'] = np.array([int(C['on']), int(C.get('kit', 1))], np.int64)"))
A.append(('C12 regla al azar', """def _regla_azar(rr):
    return [float(rr.integers(0, 6)), float(rr.integers(0, 6)), float(rr.integers(0, 2)), float(rr.random()),
            float(rr.integers(0, 4)), float(rr.uniform(-3.0, 3.0))]""",
"""def _kit():
    C = _CTX.get('BQC') or BQ_CFG
    return (13, 6) if int(C.get('kit', 1)) == 2 else (6, 4)   # (n sentidos, n acciones)


def _regla_azar(rr):
    ns, na = _kit()
    return [float(rr.integers(0, ns)), float(rr.integers(0, 6)), float(rr.integers(0, 2)), float(rr.random()),
            float(rr.integers(0, na)), float(rr.uniform(-3.0, 3.0))]"""))
A.append(('C13 mutar sentido', "            if f == 0: x[0] = float(rr.integers(0, 6))", "            if f == 0: x[0] = float(rr.integers(0, _kit()[0]))"))
A.append(('C14 mutar accion', "            elif f == 4: x[4] = float(rr.integers(0, 4))", "            elif f == 4: x[4] = float(rr.integers(0, _kit()[1]))"))
A.append(('C15 tope', """    if len(R) > NRMAX:
        R = R[:NRMAX]; O['n_tope'] += 1""", """    tp = int(C.get('tope', 12))
    if len(R) > tp:
        R = R[:tp]; O['n_tope'] += 1"""))

NUEVO = '''

# ================================================================ BLOQUES2 (anadido por construye_bloques2.py): el kit grande
@njit(cache=True)
def _vecino(s, pos, bi, cuer, nb, L):
    v = -1; dv = L + 1
    for jj in range(nb):
        u = cuer[jj]
        if u < 0 or u == s: continue
        a = bi[u, I_POS] - pos
        if a < 0: a = -a
        if L - a < a: a = L - a
        if a < dv:
            dv = a; v = u
    return dv, v


@njit(cache=True)
def _sentido2(sid, par, s, E, Ag, d, foco, RM, PATM, t, dv, v):
    if sid < 6:
        return _sentido(sid, par, E, Ag, d, foco, int(RM[s, 0]), RM[s, 1], PATM)
    if sid == 6: return (E if E < 1.5 else 1.5) / 1.5
    if sid == 7: return (Ag if Ag < 1.5 else 1.5) / 1.5
    if sid == 8:
        if foco < 0: return 0.75
        return (RM[s, 3 + foco] + 3.0) / 4.0
    if sid == 9: return (RM[s, 3 + (par % 4)] + 3.0) / 4.0
    if sid == 10:
        if v < 0: return 0.0
        return 1.0 - (dv if dv < 10 else 10) / 10.0
    if sid == 11:
        if v < 0: return 0.0
        return RM[v, 7]
    dt = t - RM[s, 8]
    return (dt if dt < 2000.0 else 2000.0) / 2000.0


@njit(cache=True)
def _cumple2(s, r, RG, RM, E, Ag, d, foco, PATM, t, dv, v):
    x = _sentido2(int(RG[s, r, 0]), int(RG[s, r, 1]), s, E, Ag, d, foco, RM, PATM, t, dv, v)
    if RG[s, r, 2] > 0.5: return x > RG[s, r, 3]
    return x < RG[s, r, 3]


@njit(cache=True)
def _nec_vecino(s, RG, RN):
    for r in range(RN[s]):
        sid = int(RG[s, r, 0])
        if sid == 10 or sid == 11 or int(RG[s, r, 4]) == 4: return True
    return False


@njit(cache=True)
def _reglas_mov2(s, RG, RN, RM, V, E, Ag, d, k, left, PATM, t, pos, bi, cuer, nb, L):
    dv = L + 1; v = -1
    if _nec_vecino(s, RG, RN): dv, v = _vecino(s, pos, bi, cuer, nb, L)
    pb = 0.0; pw = 0.0
    for r in range(RN[s]):
        a = int(RG[s, r, 4])
        if a == 0: continue
        if not _cumple2(s, r, RG, RM, E, Ag, d, k, PATM, t, dv, v): continue
        w = RG[s, r, 5]
        if a == 1:
            if k >= 0 and d > 0:
                if left: V[0] += w
                else: V[1] += w
        elif a == 2:
            V[0] -= w; V[1] -= w
        elif a == 3:
            pb += w
        elif a == 4:
            if v >= 0 and dv > 0:
                vp = bi[v, I_POS]
                x1 = pos - vp
                if x1 < 0: x1 += L
                x2 = vp - pos
                if x2 < 0: x2 += L
                if x1 < x2: V[0] += w
                else: V[1] += w
        else:
            pw += w
    RM[s, 2] = pb; RM[s, 9] = pw


@njit(cache=True)
def _reglas_boca2(s, RG, RN, RM, E, Ag, d, kk, PATM, t, pos, bi, cuer, nb, L):
    dv = L + 1; v = -1
    if _nec_vecino(s, RG, RN): dv, v = _vecino(s, pos, bi, cuer, nb, L)
    b = 0.0
    for r in range(RN[s]):
        if int(RG[s, r, 4]) != 0: continue
        if _cumple2(s, r, RG, RM, E, Ag, d, kk, PATM, t, dv, v): b += RG[s, r, 5]
    return b


# ================================================================ EL TRAMO: pasos [t0, t1)'''
A.append(('C16 bloque nuevo', "\n\n# ================================================================ EL TRAMO: pasos [t0, t1)", NUEVO))


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
        print('IGUAL' if open(DESTINO, encoding='utf-8').read() == t else 'DISTINTO', h16(DESTINO))
    else:
        with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f: f.write(t)
        print('escrito', DESTINO, h16(DESTINO), f'({len(A)} anclas, origen {SHA_ORIGEN})')
