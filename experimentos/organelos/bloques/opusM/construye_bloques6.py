"""construye_bloques6.py — construye motor_bloques6.py POR ANCLAS desde motor_bloques5.py (sha a727e6aea0fca8da). EXPLORATORIO (Opus M,
28-sep-2026, noche): INVERSION DENTRO DE UNA VIDA. Mision: llegar a la AGI por este camino.

inv = 2: la inversion A<->B, C<->D de EFF y RV se hace DENTRO del nucleo numba, al empezar el paso t (t > 0, t % inv_cada == 0), despues de
la comprobacion de ranuras (un ST_CRECE no la repite). Cualquier periodo (500, 2 000...), no solo multiplos de cada_gen. Mismo momento que
la inversion de Python (inv = 1), que queda igual. inv = 0: motor_bloques5 bit a bit (arnes); inv = 2 con periodo 20 000 == inv = 1 (arnes).
Uso:  python construye_bloques6.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(AQUI, 'motor_bloques5.py')
SHA_ORIGEN = 'a727e6aea0fca8da'
DESTINO = os.path.join(AQUI, 'motor_bloques6.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


A = []
A.append(('H0 docstring', '"""motor_bloques5.py (CONSTRUIDO por',
'''"""motor_bloques6.py (CONSTRUIDO por experimentos/organelos/bloques/opusM/construye_bloques6.py desde motor_bloques5.py, sha
a727e6aea0fca8da; NO editar a mano). inv = 2: inversion dentro del nucleo, cualquier periodo; inv = 0 y 1 bit a bit. Lo que sigue es el
docstring del origen.

motor_bloques5.py (CONSTRUIDO por'''))
A.append(('H1 firma', "FIRMA_GEMELO = 'motor_bloques5 v0'", "FIRMA_GEMELO = 'motor_bloques6 v0'"))
A.append(('H2 BQ', "    C = dict(BQ_CFG); st['BQ'] = np.array([int(C['on']), int(C.get('kit', 1))], np.int64)",
"    C = dict(BQ_CFG); st['BQ'] = np.array([int(C['on']), int(C.get('kit', 1)), int(C.get('inv', 0) == 2), int(C.get('inv_cada', 20000))], np.int64)"))
A.append(('H3 guardia solo inv 1', "    if BQ_CFG.get('inv') and (E_ is None", "    if BQ_CFG.get('inv') == 1 and (E_ is None"))
A.append(('H4 python solo inv 1', "        if BQ_CFG.get('inv') and t % int(BQ_CFG['inv_cada']) == 0 and t < T and est != ST_EXT:",
"        if BQ_CFG.get('inv') == 1 and t % int(BQ_CFG['inv_cada']) == 0 and t < T and est != ST_EXT:"))
A.append(('H5 inversion en el nucleo', "            return ST_CRECE, t\n",
"""            return ST_CRECE, t
        if BQ[2] != 0 and t > 0 and t % BQ[3] == 0:   # BLOQUES6: el mundo se invierte al empezar el paso t
            for c_ in range(EFF.shape[1]):
                x_ = EFF[0, c_]; EFF[0, c_] = EFF[1, c_]; EFF[1, c_] = x_
                x_ = EFF[2, c_]; EFF[2, c_] = EFF[3, c_]; EFF[3, c_] = x_
            for c_ in range(RV.shape[1]):
                x_ = RV[0, c_]; RV[0, c_] = RV[1, c_]; RV[1, c_] = x_
                x_ = RV[2, c_]; RV[2, c_] = RV[3, c_]; RV[3, c_] = x_
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
