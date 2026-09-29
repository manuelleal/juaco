"""construye_bloques4.py — construye motor_bloques4.py POR ANCLAS desde motor_bloques3.py (sha 21b5ee28d086b3be). EXPLORATORIO (Opus M,
28-sep-2026, noche): la pieza que faltaba, OLVIDAR / VOLVER A PROBAR. Mision: llegar a la AGI por este camino.

KIT 3 (= kit 2 + dos acciones; kit 1 y kit 2 quedan bit a bit, arnes):
  accion 6 OLVIDAR: si la regla se cumple, la memoria (R recordada por letra, RM 3..6, y la R de la ultima mordida, RM 1) decae hacia 0 en
           ese paso con tasa lambda = min(1, 10^(sum w - 4)) (w en [-3, 3] -> 1e-7 .. 0.1 por paso). La TASA es el peso: gen de la regla,
           heredable y mutable; nadie la fija a mano.
  accion 7 REPROBAR: si la regla se cumple y lo que tiene en la celda es una letra RECORDADA MALA (R < 0), con probabilidad
           p = min(1, 10^(sum w - 3)) (1e-6 .. 1) muerde igual (Vb += 10). El azar es un hash de (t, ranura, letra): no toca ningun rng.
Uso:  python construye_bloques4.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(AQUI, 'motor_bloques3.py')
SHA_ORIGEN = '21b5ee28d086b3be'
DESTINO = os.path.join(AQUI, 'motor_bloques4.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


A = []
A.append(('F0 docstring', '"""motor_bloques3.py (CONSTRUIDO por',
'''"""motor_bloques4.py (CONSTRUIDO por experimentos/organelos/bloques/opusM/construye_bloques4.py desde motor_bloques3.py, sha
21b5ee28d086b3be; NO editar a mano). KIT 3 = kit 2 + OLVIDAR (accion 6) + REPROBAR (accion 7); kit 1 y 2 bit a bit. Lo que sigue es el
docstring del origen.

motor_bloques3.py (CONSTRUIDO por'''))
A.append(('F1 firma', "FIRMA_GEMELO = 'motor_bloques3 v0'", "FIRMA_GEMELO = 'motor_bloques4 v0'"))
A.append(('F2 kit', "    return (13, 6) if int(C.get('kit', 1)) == 2 else (6, 4)   # (n sentidos, n acciones)",
"""    k_ = int(C.get('kit', 1))   # (n sentidos, n acciones)
    return (13, 8) if k_ == 3 else ((13, 6) if k_ == 2 else (6, 4))"""))
A.append(('F3 patas kit>=2', "                if BQ[1] == 2: _reglas_mov2(", "                if BQ[1] >= 2: _reglas_mov2("))
A.append(('F4 boca kit>=2', "                    if BQ[1] == 2: Vb += _reglas_boca2(", "                    if BQ[1] >= 2: Vb += _reglas_boca2("))
A.append(('F5 mov2 init', "    pb = 0.0; pw = 0.0\n    for r in range(RN[s]):\n        a = int(RG[s, r, 4])\n        if a == 0: continue\n        if not _cumple2(",
"    pb = 0.0; pw = 0.0; fo = 0.0; nfo = 0\n    for r in range(RN[s]):\n        a = int(RG[s, r, 4])\n        if a == 0 or a == 7: continue\n        if not _cumple2("))
A.append(('F6 mov2 olvido', "        else:\n            pw += w\n    RM[s, 2] = pb; RM[s, 9] = pw\n",
"""        elif a == 5:
            pw += w
        else:   # a == 6: OLVIDAR
            fo += w; nfo += 1
    RM[s, 2] = pb; RM[s, 9] = pw
    if nfo > 0:
        lam = 10.0 ** (fo - 4.0)
        if lam > 1.0: lam = 1.0
        RM[s, 1] = RM[s, 1] * (1.0 - lam)
        for c_ in range(3, 7): RM[s, c_] = RM[s, c_] * (1.0 - lam)
"""))
A.append(('F7 boca2 reprobar', """    b = 0.0
    for r in range(RN[s]):
        if int(RG[s, r, 4]) != 0: continue
        if _cumple2(s, r, RG, RM, E, Ag, d, kk, PATM, t, dv, v): b += RG[s, r, 5]
    return b""", """    b = 0.0; rp = 0.0; nrp = 0
    for r in range(RN[s]):
        a_ = int(RG[s, r, 4])
        if a_ != 0 and a_ != 7: continue
        if _cumple2(s, r, RG, RM, E, Ag, d, kk, PATM, t, dv, v):
            if a_ == 0: b += RG[s, r, 5]
            else:
                rp += RG[s, r, 5]; nrp += 1
    if nrp > 0 and kk >= 0 and RM[s, 3 + kk] < 0.0:   # REPROBAR lo recordado malo
        p_ = 10.0 ** (rp - 3.0)
        if _u01(t, s, kk) < p_: b += 10.0
    return b


@njit(cache=True)
def _u01(t, s, kk):
    \"\"\"Azar propio sin rng: splitmix64 de (t, ranura, letra) -> [0, 1).\"\"\"
    z = np.uint64(t) * np.uint64(0x9E3779B97F4A7C15) + np.uint64(s) * np.uint64(0xBF58476D1CE4E5B9) + np.uint64(kk + 1) * np.uint64(0x94D049BB133111EB)
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    z = z ^ (z >> np.uint64(31))
    return float(z >> np.uint64(11)) / 9007199254740992.0"""))


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
