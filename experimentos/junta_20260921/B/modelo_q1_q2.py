"""modelo_q1_q2.py -- dos cuentas cerradas (NO simulan el organismo; un proceso, segundos).

Q2 -- MODELO DE UN PARAMETRO del deficit de `BA-v`.
  Hecho estructural medido en `estructura_q2.py` (T = 0, 19/19 semillas de la serie y 2/2 del humo):
  de las TRES ganadoras del tipo VARIANTE (`var_cubre=1`: la mejor mixta de CADA pixel de variante),
  EXACTAMENTE UNA le da al referente X y a su hermana H la MISMA casilla -- la que cubre el pixel de
  variante en el que X y H COINCIDEN (X = T1v2 y H = T1v0 difieren en 2 de 12 pixeles, los dos de variante).
  Las 36 celdas de FORMA colisionan las 36.
  Consecuencia: en el paso de la entrega el mensaje (R = +1 sobre X) escribe +1 en LAS TRES ganadoras de
  variante de X y, por la colision, tambien en UNA de las de H. Con `dentro='suma'`:
        s_FORMA(H)   = 3 x (+1) = +3            (el mensaje entero se cuela por la forma: es la familia)
        s_VARIANTE(H)= (+1) + v9 + v11          v9, v11 = valor PROPIO del receptor en esas casillas
        lectura(H)   = min(+3, s_VARIANTE(H))
  La boca muerde si 1.2 * lectura + 2.0 * hambre + 0.5 > 0; con hambre = 1 hace falta lectura < -2.083.
  Con R(veneno) = -3 y R(comida) = +1 hay TRES casos: (+3), (-1), (-5). SOLO (-5) veta -> hacen falta LAS
  DOS casillas propias en veneno. Sea p = P(una casilla propia no colisionada vale -3):
        P(veta la hermana) = p^2          -> dist(PAR)
        P(muerde en BAR-H) = 1 - p^2      -> BAR-H   (el mismo p, el brazo espejo)
  El modelo se AJUSTA con dist(PAR) y se PREDICE BAR-H, en las dos series. Si falla, el mecanismo es otro.

  Regla candidata (`dentro='min'`, la perilla que ERR-88 declaro CODIGO MUERTO -- nunca medida):
        s_VARIANTE(H) = n x min(...)  ->  basta UNA casilla propia en veneno
        P(veta) = 1 - (1-p)^2

Q1 -- POTENCIA de la puerta `A12 >= 0.50` pareada con n semillas.
  A12 pareado = media de {1 si cand > tronco, 0.5 si empata, 0 si no}. Bajo la hipotesis de que el candidato
  es indistinguible del tronco y sin empates, n*A12 ~ Binomial(n, 0.5): el umbral esta EXACTAMENTE en la
  media de la nula, asi que la puerta rechaza a un candidato inerte ~4 de cada 10 veces POR BRAZO.
"""
import json, os, sys
from math import comb, sqrt

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
BAV = os.path.join(RAIZ, 'experimentos', 'nivel05_familia_variante_BAv')

SERIES = [('961-980', 'serie_bav_s961-980_20260921_145002_crudo.json'),
          ('981-1000', 'serie_bav_s981-1000_20260921_153820_crudo.json')]


def brazo(d, cel, base):
    return [r for r in d['brazos'] if r['cel'] == cel and r['base'] == base]


print('=' * 100)
print('Q2 -- MODELO DE UN PARAMETRO (p) DEL DEFICIT DE BA-v.  Se AJUSTA con dist(PAR), se PREDICE BAR-H.')
print('=' * 100)
print('%-10s %-8s %-12s %-8s %-14s %-14s %-16s' %
      ('serie', 'celda', 'dist(PAR)', 'p', 'BAR-H predicho', 'BAR-H medido', 'dist con min (pred)'))
for nom, arch in SERIES:
    p_ = os.path.join(BAV, arch)
    if not os.path.exists(p_):
        print('  (falta %s)' % arch)
        continue
    d = json.load(open(p_, 'r', encoding='utf-8'))
    for cel in ('BA-v',):
        rs = brazo(d, cel, 'PAR')
        dd = [r['B4']['dist'] for r in rs if r['B4']['dist'] is not None]
        n = len(dd)
        p2 = sum(dd) / n
        p = sqrt(p2)
        bh = brazo(d, cel, 'BAR-H')
        nbh = len([r for r in bh if r['B4']['evX'] is not None])
        bh_med = sum(1 for r in bh if r['B4']['evX'] == 0.0)
        bh_pred = (1 - p2) * nbh
        dist_min = (1 - (1 - p) ** 2) * n
        print('%-10s %-8s %-12s %-8.3f %-14.1f %-14d %-16s' %
              (nom, cel, '%d/%d' % (int(sum(dd)), n), p, bh_pred, bh_med,
               '%.1f/%d' % (dist_min, n)))

print()
print('=' * 100)
print('Q1 -- POTENCIA DE LA PUERTA A12 >= 0.50 PAREADA (candidato INDISTINGUIBLE del tronco, sin empates)')
print('=' * 100)
print('%-6s %-16s %-16s %-24s' % ('n', 'P(pasa 1 brazo)', 'P(falla 1 brazo)', 'P(falla T-A = 2 brazos indep.)'))
for n in (18, 19, 20, 40, 60):
    # P(A12 >= 0.5) = P(X >= ceil(n/2)) con X ~ Bin(n, 0.5); n par: P(X>=n/2)
    k0 = (n + 1) // 2 if n % 2 else n // 2
    pasa = sum(comb(n, k) for k in range(k0, n + 1)) / 2.0 ** n
    print('%-6d %-16.3f %-16.3f %-24.3f' % (n, pasa, 1 - pasa, 1 - pasa * pasa))
print()
print('Banda de la nula (desviacion tipica de A12 pareado bajo indistinguibilidad): %.3f con n = 20'
      % (0.5 / sqrt(20)))
print('Umbral que dejaria pasar al 95 %% de los candidatos inertes con n = 20: A12 >= %.2f'
      % (0.5 - 1.645 * 0.5 / sqrt(20)))
