"""construye_bloques3.py — construye motor_bloques3.py POR ANCLAS desde motor_bloques2.py (sha e365506be24bb490). EXPLORATORIO
(Opus M, 28-sep-2026, ultima ronda): UN MUNDO QUE CAMBIA. Mision: llegar a la AGI por este camino.

Inversion periodica del SIGNIFICADO de las letras (la apariencia, los 6 pixeles, no cambia): cada inv_cada pasos se intercambian las filas
de EFF (efecto en E, Ag) y RV (la R que aprende el cerebro) de A<->B y C<->D. Tras la primera inversion A es veneno, B comida, C sal, D agua.
Se hace en Python ENTRE tramos (inv_cada multiplo de cada_gen = 2000: el tramo ya se corta alli), en su lugar (el nucleo lee los mismos
arrays), y viaja en el checkpoint (EFF y RV son claves del estado). Con inv = 0 no se ejecuta nada: motor_bloques2 bit a bit (arnes).
Telemetria que queda MAL ROTULADA con la inversion (declarado): las causas de muerte 'veneno'/'sal' del nucleo miran la letra B/D (indices 1/3).

Uso:  python construye_bloques3.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(AQUI, 'motor_bloques2.py')
SHA_ORIGEN = 'e365506be24bb490'
DESTINO = os.path.join(AQUI, 'motor_bloques3.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


A = []
A.append(('D0 docstring', '"""motor_bloques2.py (CONSTRUIDO por',
'''"""motor_bloques3.py (CONSTRUIDO por experimentos/organelos/bloques/opusM/construye_bloques3.py desde motor_bloques2.py, sha
e365506be24bb490; NO editar a mano). UN MUNDO QUE CAMBIA: inversion periodica A<->B, C<->D del significado (BQ_CFG inv, inv_cada);
con inv = 0 es motor_bloques2 bit a bit. Lo que sigue es el docstring del origen.

motor_bloques2.py (CONSTRUIDO por'''))
A.append(('D1 firma', "FIRMA_GEMELO = 'motor_bloques2 v0'", "FIRMA_GEMELO = 'motor_bloques3 v0'"))
A.append(('D2 cfg', "              inicial=None, forzada=None, kit=1, tope=12)", "              inicial=None, forzada=None, kit=1, tope=12, inv=0, inv_cada=20000)"))
A.append(('D3 inversion', "        t = int(tnow)\n        if E_ is not None:\n            cuerpos = None",
"""        t = int(tnow)
        if BQ_CFG.get('inv') and t % int(BQ_CFG['inv_cada']) == 0 and t < T and est != ST_EXT:   # BLOQUES3: el mundo cambia
            for M_ in (st['EFF'], st['RV']):
                M_[[0, 1]] = M_[[1, 0]]; M_[[2, 3]] = M_[[3, 2]]
            BQ_OUT['n_inv'] = BQ_OUT.get('n_inv', 0) + 1
        if E_ is not None:
            cuerpos = None"""))
A.append(('D4 inv_cada multiplo', "    _bq_arranque(st, n)   # BLOQUES\n",
"""    _bq_arranque(st, n)   # BLOQUES
    if BQ_CFG.get('inv') and (E_ is None or not E_['cada_gen'] or int(BQ_CFG['inv_cada']) % int(E_['cada_gen']) != 0):
        raise ValueError('BLOQUES3: inv_cada debe ser multiplo de cada_gen (el tramo se corta alli)')
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
