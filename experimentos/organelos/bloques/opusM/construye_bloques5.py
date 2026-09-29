"""construye_bloques5.py — construye motor_bloques5.py POR ANCLAS desde motor_bloques4.py (sha ad5bd2eb59f6279d). EXPLORATORIO (Opus M,
28-sep-2026, noche): OLVIDAR LO QUE APRENDIO EL CEREBRO. Mision: llegar a la AGI por este camino.

Accion 8 OLVIDAR EL CEREBRO: si la regla se cumple, la aversion aprendida del cerebro de fabrica (Wn de la via rapida y Wns de la lenta, las
dos necesidades) decae hacia su valor de nacimiento (0) con tasa lambda = min(1, 10^(sum w - 4)) por paso. Por costo se aplica cada 100 pasos
con el factor equivalente (1 - lambda)^100, leyendo la condicion en ese paso. Wp no se toca. La memoria de rechazo (<= memoria_rechazo pasos)
ya caduca sola: no se toca.
  kit 4 = kit 3 + accion 8 (13 sentidos, 9 acciones).
  kit 5 = SOLO el gen de olvido: una regla fija "siempre -> olvidar el cerebro" con peso w; sentido, umbral y accion no mutan, solo w
          (es un GEN heredable y mutable con la misma maquinaria de reglas; tope 1).
Kit 1..3: motor_bloques4 bit a bit (arnes).
Uso:  python construye_bloques5.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(AQUI, 'motor_bloques4.py')
SHA_ORIGEN = 'ad5bd2eb59f6279d'
DESTINO = os.path.join(AQUI, 'motor_bloques5.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


A = []
A.append(('G0 docstring', '"""motor_bloques4.py (CONSTRUIDO por',
'''"""motor_bloques5.py (CONSTRUIDO por experimentos/organelos/bloques/opusM/construye_bloques5.py desde motor_bloques4.py, sha
ad5bd2eb59f6279d; NO editar a mano). Accion 8 OLVIDAR EL CEREBRO (kit 4; kit 5 = solo el gen de olvido); kit 1..3 bit a bit. Lo que
sigue es el docstring del origen.

motor_bloques4.py (CONSTRUIDO por'''))
A.append(('G1 firma', "FIRMA_GEMELO = 'motor_bloques4 v0'", "FIRMA_GEMELO = 'motor_bloques5 v0'"))
A.append(('G2 kit', "    return (13, 8) if k_ == 3 else ((13, 6) if k_ == 2 else (6, 4))",
"""    if k_ == 5: return (1, 9)   # BLOQUES5: solo el gen de olvido del cerebro
    return (13, 9) if k_ == 4 else ((13, 8) if k_ == 3 else ((13, 6) if k_ == 2 else (6, 4)))"""))
A.append(('G3 regla azar kit 5', "    ns, na = _kit()\n    return [float(rr.integers(0, ns))",
"    ns, na = _kit()\n    if ns == 1: return [0.0, 0.0, 0.0, 1.0, 8.0, float(rr.uniform(-3.0, 3.0))]   # BLOQUES5: 'siempre -> olvidar el cerebro'\n"
"    return [float(rr.integers(0, ns))"))
A.append(('G4 mutar solo w en kit 5', "            f = int(rr.integers(0, 6)); O['n_campo'] += 1",
"            f = 5 if _kit()[0] == 1 else int(rr.integers(0, 6)); O['n_campo'] += 1"))
A.append(('G5 firma mov2', "def _reglas_mov2(s, RG, RN, RM, V, E, Ag, d, k, left, PATM, t, pos, bi, cuer, nb, L):",
"def _reglas_mov2(s, RG, RN, RM, V, E, Ag, d, k, left, PATM, t, pos, bi, cuer, nb, L, Wn, Wns):"))
A.append(('G6 llamada mov2', "if BQ[1] >= 2: _reglas_mov2(s, RG, RN, RM, V, E, Ag, d, k, left, PATM, t, pos, bi, cuer, nb, L)",
"if BQ[1] >= 2: _reglas_mov2(s, RG, RN, RM, V, E, Ag, d, k, left, PATM, t, pos, bi, cuer, nb, L, Wn, Wns)"))
A.append(('G7 init', "    pb = 0.0; pw = 0.0; fo = 0.0; nfo = 0\n", "    pb = 0.0; pw = 0.0; fo = 0.0; nfo = 0; fc = 0.0; nfc = 0\n"))
A.append(('G8 accion 8', "        else:   # a == 6: OLVIDAR\n            fo += w; nfo += 1\n",
"        elif a == 6:   # OLVIDAR (memoria de las reglas)\n            fo += w; nfo += 1\n"
"        else:   # a == 8: OLVIDAR EL CEREBRO (BLOQUES5)\n            fc += w; nfc += 1\n"))
A.append(('G9 decae el cerebro', "        for c_ in range(3, 7): RM[s, c_] = RM[s, c_] * (1.0 - lam)\n",
"""        for c_ in range(3, 7): RM[s, c_] = RM[s, c_] * (1.0 - lam)
    if nfc > 0 and t % 100 == 0:   # BLOQUES5: la aversion aprendida del cerebro decae hacia su valor de nacimiento (0)
        lc = 10.0 ** (fc - 4.0)
        if lc > 1.0: lc = 1.0
        f_ = (1.0 - lc) ** 100
        for n_ in range(Wn.shape[1]):
            for i_ in range(Wn.shape[2]): Wn[s, n_, i_] = Wn[s, n_, i_] * f_
            for j_ in range(6): Wns[s, n_, j_] = Wns[s, n_, j_] * f_
"""))


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
