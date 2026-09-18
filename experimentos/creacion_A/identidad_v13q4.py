"""CREADOR A — arnes de identidad de `organismo_v13q4.py` (perilla `seleccion` apagada) contra
`organismo_v13q3.py` (`aaebe073308a40c2`, original intacto). Un proceso, sin Pool.

Con `seleccion=None` la rama nueva no se ejecuta: v13q4 debe dar EXACTAMENTE las mismas claves que v13q3 (las
claves nuevas `sel_*` se excluyen de la comparacion porque no existen en el original). 8 escenarios x 2 semillas,
incluidos `lectura='oraculo01'` y `regla_lenta='delta_signo'` (los que pide el paquete A-1), el mundo 'AB' del
tronco, la inversion, la via lenta apagada (`eta_s=0`) y `random15`.
Uso: python identidad_v13q4.py [T]
"""
import sys, os, json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, '..', 'nivel7_xor_lectura')]
import organismo_v13q3 as ORIG
import organismo_v13q4 as NUEVO

NUEVAS = {'seleccion', 'sel_estad', 'sel_theta', 'sel_rho', 'sel_cupo', 'sel_abre', 'sel_abiertos', 'sel_e', 'sel_n'}

ESCENARIOS = [
    ('regla/px0 lineal (v13 por defecto)', dict(mundo='regla', regla='px0', lectura='lineal', eta_s=0.015, puerta=3)),
    ('regla/xor01 cuadratica + cte + delta', dict(mundo='regla', regla='xor01', lectura='cuadratica', constante=True,
                                                 regla_lenta='delta_signo', lam_lenta=0.002, eta_s=0.015, puerta=3)),
    ('regla/xor01 ORACULO01 + cte + delta', dict(mundo='regla', regla='xor01', lectura='oraculo01', constante=True,
                                                regla_lenta='delta_signo', lam_lenta=0.0, eta_s=0.05, clip_s=10.0, puerta=3)),
    ('regla/xor01 oraculo01_ruido dos canales', dict(mundo='regla', regla='xor01', lectura='oraculo01_ruido',
                                                     constante=True, eta_s=0.015, puerta=3)),
    ('regla/azar random15', dict(mundo='regla', regla='azar', lectura='random15', eta_s=0.015, puerta=3)),
    ('AB (mundo del tronco) + sonda final', dict(mundo='AB', eta_s=0.015, puerta=3, sonda_final=True)),
    ('AB invertido en T/2', dict(mundo='AB', eta_s=0.015, puerta=3, invertir_en=15000)),
    ('regla/px0 cuadratica con via lenta APAGADA', dict(mundo='regla', regla='px0', lectura='cuadratica', eta_s=0.0, puerta=None)),
]


def N(x):
    return json.loads(json.dumps(x, default=str))


if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    ok = 0; total = 0; malos = []
    for etq, kw in ESCENARIOS:
        for seed in (1, 2):
            total += 1
            a = ORIG.run(seed, T=T, **kw)
            b = NUEVO.run(seed, T=T, seleccion=None, **kw)
            faltan = [k for k in a if k not in b]
            dif = [k for k in a if k in b and N(a[k]) != N(b[k])]
            extra = [k for k in b if k not in a and k not in NUEVAS]
            bien = not dif and not faltan and not extra
            ok += bien
            print(f'  {etq:>42} s{seed} T={T}: {"IDENTICO" if bien else "DIFIEREN"} ({len(a)} claves)'
                  + ('' if bien else f'  dif={dif} faltan={faltan} extra={extra}'))
            if not bien: malos.append((etq, seed, dif, faltan, extra))
    print(f'\nIDENTIDAD v13q4(seleccion=None) == v13q3: {ok}/{total}' + ('' if ok == total else f'  FALLAN: {malos}'))
