"""humo_toxicidad.py -- HUMO EXPLORATORIO (NO es serie, NO juzga nada; semilla 1, ya vista; 6 corridas, un proceso).

Tras el NEGATIVO de la calibracion (la dilucion sola escala NADA y ORACULO juntos: razon ~3.0-3.2 en toda la
rejilla), se mira UNA direccion para el proximo preregistro: la TOXICIDAD de lo malo (kwarg `tabla`, que YA
existe en organismo_f9c: efecto (dE, dAg) por valencia; la recompensa que aprende el cuerpo depende solo del
SIGNO, asi que el aprendizaje no cambia, cambia la consecuencia). Hipotesis a preregistrar: la toxicidad castiga
la ignorancia (NADA muerde lo malo) mucho mas que el conocimiento (ORACULO casi no lo muerde) y ENSANCHA la razon.
Mismo instrumento organismo_anclado.py (sha e689c2952b1991a4), mismos brazos (corre_anclado.kwargs).

    python experimentos/mundo_anclado/humo_toxicidad.py
"""
import json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_anclado as CA

TOX2 = {'comida': (0.8, 0.0), 'veneno': (-0.8, 0.0), 'agua': (0.0, 0.8), 'sal': (0.0, -0.8)}   # lo malo x2


def main():
    s = time.strftime('%Y%m%d_%H%M%S')
    CA.LOG[0] = open(os.path.join(CA.HUMO, f'anclado_humotox_{s}.log'), 'w', encoding='utf-8')
    CA.cabecera('HUMO TOXICIDAD (exploratorio, semilla 1, 6 corridas)')
    assert CA.ANC.EFECTO == {'comida': (0.8, 0.0), 'veneno': (-0.4, 0.0), 'agua': (0.0, 0.8), 'sal': (0.0, -0.4)}
    casos = [('NADA', 0.0, TOX2), ('ORACULO', 0.0, TOX2), ('NADA', 0.003, TOX2), ('ORACULO', 0.003, TOX2),
             ('REL', 0.003, TOX2), ('NADA', 0.003, None)]
    R = []
    for b, h, tab in casos:
        t0 = time.time()
        kw = CA.kwargs(b, 0, h)
        if tab is not None:
            kw['tabla'] = tab
        r = CA.ANC.run(1, T=CA.T, **kw)
        o = CA.resumen(b, 1, 0, h, r, time.time() - t0); o['tox'] = 2 if tab else 1; R.append(o)
        CA.log(f"    {b:8s} h={h} tox=x{o['tox']}  R0={o['R0']:.3f}  vida={o['vida_med']}  f_mala={o['f_mala']}  J={o['J']}  ({o['seg']:.1f}s)")
    CA.escribe(os.path.join(CA.HUMO, f'anclado_humotox_{s}.json'), dict(modo='humo_toxicidad', sello=s, T=CA.T, corridas=R))


if __name__ == '__main__':
    main()
