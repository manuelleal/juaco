"""MINI-EQUIPO 2 (enjambre) -- arnes de identidad de `organismo_g2.py` (perilla `fision` APAGADA, fision=None)
contra `organismo_v13q5.py` (fae9c32b146fdbb4, original intacto, SOLO LECTURA). Un proceso, sin Pool.

Con fision=None la rama nueva no se ejecuta (la cadena if/elif de la regla cae en el brazo de siempre, y
lenta(P) cae directo en su linea original intacta): organismo_g2 debe dar EXACTAMENTE las mismas claves que
organismo_v13q5 (las claves nuevas fis_celdas/fis_ganadora/fis_n se excluyen porque no existen en el original).

3 reglas (xor01/px0/azar) x 3 semillas (1-3) = 9 casos, T=30000, TODAS las claves del original comparadas.
Uso: python identidad_g2.py [T]
"""
import sys, os, json

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'creacion_A'), os.path.join(RAIZ, 'organismo')]
import organismo_v13q5 as ORIG
import organismo_g2 as NUEVO

NUEVAS = {'fis_celdas', 'fis_ganadora', 'fis_n'}

ESCENARIOS = [
    ('regla/xor01 cuadratica+cte+delta (v14.1)', dict(mundo='regla', regla='xor01', lectura='cuadratica', constante=True,
                                                        regla_lenta='delta_signo', lam_lenta=0.0, eta_s=0.15, clip_s=10.0, puerta=3)),
    ('regla/px0 cuadratica+cte+delta (v14.1)', dict(mundo='regla', regla='px0', lectura='cuadratica', constante=True,
                                                      regla_lenta='delta_signo', lam_lenta=0.0, eta_s=0.15, clip_s=10.0, puerta=3)),
    ('regla/azar cuadratica+cte+delta (v14.1)', dict(mundo='regla', regla='azar', lectura='cuadratica', constante=True,
                                                       regla_lenta='delta_signo', lam_lenta=0.0, eta_s=0.15, clip_s=10.0, puerta=3)),
]


def N(x):
    return json.loads(json.dumps(x, default=str))


if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    ok = 0
    total = 0
    malos = []
    for etq, kw in ESCENARIOS:
        for seed in (1, 2, 3):
            total += 1
            a = ORIG.run(seed, T=T, **kw)
            b = NUEVO.run(seed, T=T, fision=None, **kw)
            faltan = [k for k in a if k not in b]
            dif = [k for k in a if k in b and N(a[k]) != N(b[k])]
            extra = [k for k in b if k not in a and k not in NUEVAS]
            bien = not dif and not faltan and not extra
            ok += bien
            print(f'  {etq:>45} s{seed} T={T}: {"IDENTICO" if bien else "DIFIEREN"} ({len(a)} claves)'
                  + ('' if bien else f'  dif={dif} faltan={faltan} extra={extra}'))
            if not bien:
                malos.append((etq, seed, dif, faltan, extra))
    print(f'\nIDENTIDAD organismo_g2(fision=None) == organismo_v13q5: {ok}/{total}'
          + ('' if ok == total else f'  FALLAN: {malos}'))
