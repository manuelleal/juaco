# -*- coding: utf-8 -*-
"""
Q1 (junta 21-sep-2026, creador A). Potencia de la LETRA de T-A y T-C (ii) del CRITERIO_TRONCO_v2
con n = 20 semillas pareadas. NO simula el organismo: lee los crudos ya medidos.

Qué calcula, en este orden:
  1) Los pares observados (ON, OFF) por semilla en T-A (r = descendientes - muertes, por brazo)
     y en T-C (ii) (rev = mordB[Q4] - mordA[Q4]); A12 pareado tal y como lo calcula el runner
     (P(x>y) + 0.5 P(x=y)), ganadas/empates/perdidas, sd de la diferencia, correlacion intra-semilla.
  2) POTENCIA EXACTA de la regla "A12 >= t" bajo el modelo de signo sin empates:
     #ganadas ~ Bin(n, p) con p = P(ON > OFF). Para t = 0.50 y t = 0.75, n = 20/40/80/inf.
  3) POTENCIA EMPIRICA con el RUIDO REAL: se toma la nube de diferencias observadas, se simetriza
     alrededor de 0 (nulo exacto por intercambiabilidad, misma escala que el dato real) y se le
     suma un desplazamiento delta; se remuestrea n = 20 pares 200 000 veces y se cuenta cuantas
     veces la letra da PASA. delta se expresa en las unidades del propio criterio (puntos de r;
     el margen declarado de T-A es r >= tronco - 10).
  4) Tamano de muestra que haria falta para una prueba de NO INFERIORIDAD honesta con margen 10.

Uso: python analiza_potencia_Q1.py            (escribe salida_analiza_potencia_Q1.txt al lado)
"""
import json, math, os, sys
import numpy as np

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
DATOS = os.path.join(RAIZ, 'datos')
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'salida_analiza_potencia_Q1.txt')
_fh = open(SALIDA, 'w', encoding='utf-8')


def log(s=''):
    print(s)
    _fh.write(s + '\n')
    _fh.flush()


# ---------------------------------------------------------------- A12 tal como lo hace el runner
def a12(xs, ys):
    pares = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if not pares:
        return None
    return round(float(np.mean([1.0 if x > y else (0.5 if x == y else 0.0) for x, y in pares])), 3)


def carga(nombre):
    with open(os.path.join(DATOS, nombre), encoding='utf-8') as f:
        return json.load(f)['corridas']


def pares(corridas, arm_on, arm_off, campo, brazo=None):
    """Devuelve (semillas, on, off) ordenados por semilla, solo semillas con los dos brazos."""
    sel = lambda a: {c['seed']: c[campo] for c in corridas
                     if c['arm'] == a and (brazo is None or c.get('brazo') == brazo)}
    on, off = sel(arm_on), sel(arm_off)
    ss = sorted(set(on) & set(off))
    return ss, [on[s] for s in ss], [off[s] for s in ss]


# ---------------------------------------------------------------- 1) lo observado
CASOS = [
    ('v15f  T-A  VIVO',       'v15f_v2_20260921_123755_crudo_TA.json',   'v15f', 'OFF', 'r',   'VIVO',       0.50),
    ('v15f  T-A  CUELLO_MIN', 'v15f_v2_20260921_123755_crudo_TA.json',   'v15f', 'OFF', 'r',   'CUELLO_MIN', 0.50),
    ('dE5   T-A  VIVO',       'dE5_v2_20260921_152224_crudo_TA.json',    'dE5',  'OFF', 'r',   'VIVO',       0.50),
    ('dE5   T-A  CUELLO_MIN', 'dE5_v2_20260921_152224_crudo_TA.json',    'dE5',  'OFF', 'r',   'CUELLO_MIN', 0.50),
    ('v15f  T-C ii (rev)',    'v15f_v2_20260921_123755_crudo_TCii.json', 'v15f', 'OFF', 'rev', None,         0.75),
    ('v15g  T-C ii (rev)',    'v15f_v2_20260921_123755_crudo_TCii.json', 'v15g', 'OFF', 'rev', None,         0.75),
    ('dE5   T-C ii (rev)',    'dE5_v2_20260921_152224_crudo_TCii.json',  'dE5',  'OFF', 'rev', None,         0.75),
]

log('=' * 108)
log('1) LO OBSERVADO  (pares por semilla; A12 = P(ON>OFF) + 0.5 P(=), exactamente la formula del runner)')
log('=' * 108)
log(f"{'caso':<22} {'n':>3} {'A12':>6} {'umbral':>6} {'G/E/P':>10} {'med ON':>8} {'med OFF':>8} "
    f"{'med d':>7} {'sd d':>7} {'sd OFF':>7} {'r(ON,OFF)':>10} {'sd_d/(V2 sdOFF)':>16}")
log('-' * 108)
NUBES = {}
for etq, arch, aon, aoff, campo, brazo, umb in CASOS:
    ss, on, off = pares(carga(arch), aon, aoff, campo, brazo)
    on, off = np.array(on, float), np.array(off, float)
    d = on - off
    g = int(np.sum(on > off)); e = int(np.sum(on == off)); p = int(np.sum(on < off))
    rho = float(np.corrcoef(on, off)[0, 1]) if len(on) > 2 else float('nan')
    sd_d, sd_off = float(np.std(d, ddof=1)), float(np.std(off, ddof=1))
    NUBES[etq] = dict(d=d, umbral=umb, n=len(d), a12=a12(list(on), list(off)), sd_d=sd_d)
    log(f"{etq:<22} {len(ss):>3} {NUBES[etq]['a12']:>6.3f} {umb:>6.2f} {f'{g}/{e}/{p}':>10} "
        f"{np.median(on):>8.1f} {np.median(off):>8.1f} {np.median(d):>7.1f} {sd_d:>7.2f} {sd_off:>7.2f} "
        f"{rho:>10.3f} {sd_d / (math.sqrt(2) * sd_off):>16.3f}")
log('')
log('  Lectura de la ultima columna: 1.00 = la semilla NO controla nada (ON y OFF son dos tiradas')
log('  independientes); < 1 = el pareado reduce ruido. rho(ON,OFF) mide lo mismo por el otro lado.')

# ---------------------------------------------------------------- 2) potencia exacta del signo
log('')
log('=' * 108)
log('2) POTENCIA EXACTA DE LA LETRA  (modelo de signo sin empates: #ganadas ~ Bin(n, p), p = P(ON>OFF))')
log('=' * 108)


def p_pasa(n, t, p):
    """P(A12 >= t) con A12 = Bin(n,p)/n.  k_min = ceil(t*n) con tolerancia numerica."""
    kmin = math.ceil(t * n - 1e-9)
    return sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(kmin, n + 1))


PS = [0.20, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90]
for t in (0.50, 0.75):
    log('')
    log(f'  regla: A12 >= {t:.2f}     (T-A usa 0.50; T-C(ii) usa 0.75)')
    log('  p verdadero ->  ' + ''.join(f'{p:>6.2f}' for p in PS))
    for n in (20, 40, 80, 200):
        log(f'    n = {n:<4}      ' + ''.join(f'{p_pasa(n, t, p):>6.3f}' for p in PS))
    log(f'    n -> inf      ' + ''.join(f'{(0.5 if abs(p - t) < 1e-9 else (1.0 if p > t else 0.0)):>6.3f}' for p in PS))

log('')
log('  p = 0.50 es "el candidato ES el tronco". Leer esa columna:')
for t in (0.50, 0.75):
    log(f'    A12 >= {t:.2f}:  n=20 -> {p_pasa(20, t, 0.5):.3f}   n=40 -> {p_pasa(40, t, 0.5):.3f}   '
        f'n=80 -> {p_pasa(80, t, 0.5):.3f}   n->inf -> {0.5 if t == 0.5 else 0.0:.3f}')
log('')
log('  Efecto minimo detectable (p tal que la regla PASA con probabilidad 0.80):')
for t in (0.50, 0.75):
    for n in (20, 40, 80):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if p_pasa(n, t, mid) < 0.80:
                lo = mid
            else:
                hi = mid
        log(f'    A12 >= {t:.2f}, n = {n:<3} -> p* = {hi:.3f}  (el candidato tiene que ganar al tronco '
            f'en el {100 * hi:.0f} % de las semillas)')

# ---------------------------------------------------------------- 3) potencia con el ruido real
log('')
log('=' * 108)
log('3) POTENCIA CON EL RUIDO REAL  (remuestreo de la nube observada, simetrizada = nulo exacto,')
log('   mas un desplazamiento delta en las unidades del criterio; n = 20; 200 000 repeticiones)')
log('=' * 108)
RNG = np.random.default_rng(20260921)
B = 200_000
DELTAS = [+20.0, +10.0, +5.0, +2.0, 0.0, -2.0, -5.0, -10.0, -20.0]


def potencia_empirica(d, umbral, n, deltas, B=B):
    base = np.concatenate([d - np.median(d), -(d - np.median(d))])  # simetrizada: nulo exacto
    out = []
    for delta in deltas:
        idx = RNG.integers(0, len(base), size=(B, n))
        m = base[idx] + delta
        a = (np.sum(m > 0, axis=1) + 0.5 * np.sum(m == 0, axis=1)) / n
        out.append(float(np.mean(a >= umbral - 1e-12)))
    return out


for etq in NUBES:
    nb = NUBES[etq]
    pot = potencia_empirica(nb['d'], nb['umbral'], 20, DELTAS)
    log('')
    log(f"  {etq}   (umbral {nb['umbral']:.2f}; sd de la diferencia {nb['sd_d']:.2f})")
    log('    delta (ON - OFF) ->  ' + ''.join(f'{x:>+8.0f}' for x in DELTAS))
    log('    P(la letra PASA)     ' + ''.join(f'{x:>8.3f}' for x in pot))

log('')
log('  3b) BANDA DE OPERACION de la letra, en unidades naturales (delta donde PASA con prob. 0.80')
log('      y delta donde CAE con prob. 0.80; entre los dos la letra es un volado):')


def busca_delta(d, umbral, objetivo, n=20, B=40_000):
    lo, hi = -80.0, 80.0
    for _ in range(28):
        mid = 0.5 * (lo + hi)
        p = potencia_empirica(d, umbral, n, [mid], B=B)[0]
        if p < objetivo:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


for etq, nb in NUBES.items():
    d80 = busca_delta(nb['d'], nb['umbral'], 0.80)
    d20 = busca_delta(nb['d'], nb['umbral'], 0.20)
    log(f"      {etq:<22} PASA-80% en delta >= {d80:>+6.1f}   CAE-80% en delta <= {d20:>+6.1f}   "
        f"(banda ciega de {d80 - d20:>4.1f} puntos)")
log('')
log('  delta = 0 es "identico al tronco"; delta = -10 es exactamente el margen que el propio T-A')
log('  declara tolerable ("r >= tronco - 10"). Si las dos columnas dan casi lo mismo, la letra no')
log('  distingue "igual" de "peor en todo el margen declarado".')

# ---------------------------------------------------------------- 4) n para no inferioridad honesta
log('')
log('=' * 108)
log('4) TAMANO DE MUESTRA PARA UNA PRUEBA DE NO INFERIORIDAD HONESTA (margen = 10 puntos de r)')
log('=' * 108)
z95, z80 = 1.6449, 0.8416
log('   n = (z_0.95 + z_0.80)^2 * sd_d^2 / margen^2   (t pareada, efecto verdadero 0, potencia 0.80)')
for etq in NUBES:
    if 'T-A' not in etq:
        continue
    sd = NUBES[etq]['sd_d']
    for margen in (10.0, 15.0, 20.0):
        n = (z95 + z80) ** 2 * sd ** 2 / margen ** 2
        log(f'   {etq:<22} sd_d {sd:>6.2f}  margen {margen:>4.0f} -> n = {math.ceil(n):>4} semillas pareadas')
log('')
log('   Con el signo (no parametrico, sin supuesto de normalidad) la n sube ~1.05-1.5x sobre la de arriba.')
log('')
log('   Lo mismo exigiendo que un candidato IDENTICO al tronco pase el 95 % de las veces')
log('   (n = (z_0.95 + z_0.95)^2 * sd_d^2 / margen^2):')
for etq in NUBES:
    if 'T-A' not in etq:
        continue
    sd = NUBES[etq]['sd_d']
    fila = '   %-22s sd_d %6.2f ->' % (etq, sd)
    for margen in (10.0, 15.0, 20.0):
        fila += '  margen %2.0f: n = %3d' % (margen, math.ceil((z95 + z95) ** 2 * sd ** 2 / margen ** 2))
    log(fila)

# ---------------------------------------------------------------- 5) que dicen los datos YA medidos
log('')
log('=' * 108)
log('5) LOS DATOS YA MEDIDOS, LEIDOS CON EL INSTRUMENTO CORRECTO  (DIAGNOSTICO DEL INSTRUMENTO,')
log('   NO VEREDICTO: regla 3, ningun candidato se rejuzga; v15f y dE5 siguen FUERA)')
log('=' * 108)


def ci_binomial(k, n, conf=0.90):
    """Clopper-Pearson por busqueda directa sobre la binomial (sin scipy)."""
    al = (1 - conf) / 2
    F = lambda p, kk: sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(kk, n + 1))
    lo, hi = 0.0, 1.0
    if k > 0:
        a, b = 0.0, 1.0
        for _ in range(80):
            m = (a + b) / 2
            if F(m, k) < al:
                a = m
            else:
                b = m
        lo = a
    if k < n:
        a, b = 0.0, 1.0
        for _ in range(80):
            m = (a + b) / 2
            if 1 - F(m, k + 1) < al:
                b = m
            else:
                a = m
        hi = b
    return lo, hi


log('')
log(f"{'caso':<22} {'A12':>6} {'IC90 de p (signo)':>22} {'media d':>8} {'EE':>6} "
    f"{'IC90 de la media d':>22} {'no-inferior a margen 10?':>26}")
log('-' * 108)
for etq, nb in NUBES.items():
    d = nb['d']
    n = len(d)
    k = int(np.sum(d > 0)) + 0.5 * int(np.sum(d == 0))
    lo, hi = ci_binomial(int(round(k)), n)
    mu, ee = float(np.mean(d)), float(np.std(d, ddof=1) / math.sqrt(n))
    t95 = 1.729  # t de Student, 19 gl, una cola 0.05
    lo_d, hi_d = mu - t95 * ee, mu + t95 * ee
    margen = -10.0 if 'T-A' in etq else None
    ni = ('n/a (T-C ii no declara margen)' if margen is None
          else ('SI  (LI %.1f > %.0f)' % (lo_d, margen) if lo_d > margen else 'NO  (LI %.1f <= %.0f)' % (lo_d, margen)))
    log(f"{etq:<22} {nb['a12']:>6.3f} {f'[{lo:.2f}, {hi:.2f}]':>22} {mu:>8.2f} {ee:>6.2f} "
        f"{f'[{lo_d:.1f}, {hi_d:.1f}]':>22} {ni:>26}")
log('')
log('  El IC90 del signo de CADA caso contiene 0.50: con n = 20 ninguno de los cuatro T-A medidos')
log('  hoy puede separar "igual al tronco" (p = 0.50) de "peor" (p = 0.35).')

# ---------------------------------------------------------------- 6) la misma patologia en otras puertas de conteo
log('')
log('=' * 108)
log('6) LA MISMA PATOLOGIA EN LAS PUERTAS DE CONTEO k/n  (Q2: P6 de BA-v, dist(PAR) >= 15 de 19)')
log('=' * 108)
log('   BA-v, dist(PAR) en las tres series registradas: 18/19, 17/19, 13/19  (agrupado 48/57 = %.3f)'
    % (48 / 57))
log('   Si el mecanismo tiene UN solo p verdadero, la puerta 15/19 se cruza con probabilidad:')
log('   p verdadero ->  ' + ''.join(f'{p:>7.2f}' for p in [0.70, 0.75, 0.80, 0.842, 0.85, 0.90, 0.95]))
log('   P(dist >= 15)   ' + ''.join(f'{p_pasa(19, 15 / 19, p):>7.3f}' for p in [0.70, 0.75, 0.80, 0.842, 0.85, 0.90, 0.95]))
k = [18, 17, 13]
log('')
log('   Homogeneidad de las tres series bajo p = 0.842 (chi2 de 2 gl, esperado 16.0 por serie):')
esp = 19 * 48 / 57
chi = sum((ki - esp) ** 2 / (esp * (1 - 48 / 57)) for ki in k)
log(f'     chi2 = {chi:.2f}  (critico 5.99 al 5 %)  ->  '
    + ('las tres series son compatibles con UN solo p' if chi < 5.99 else 'las series difieren'))
log(f'   Con p = 0.842, P(cruzar 15/19) = {p_pasa(19, 15/19, 0.842):.3f}: una serie de cada '
    f'{1/(1-p_pasa(19,15/19,0.842)):.1f} cae por la letra aunque el mecanismo no cambie.')
log('   IC90 exacto de p con 48/57: ' + str(tuple(round(x, 3) for x in ci_binomial(48, 57))))

# ---------------------------------------------------------------- 7) la letra v3 propuesta, medida
log('')
log('=' * 108)
log('7) LA LETRA PROPUESTA (v3): NO INFERIORIDAD en unidades naturales, con el MISMO n = 20')
log('=' * 108)
log('   Regla: PASA si el limite inferior del IC 95 % de una cola de la diferencia pareada (ON - OFF)')
log('          queda POR ENCIMA de -margen. margen = 10 puntos de r (el que T-A ya declara).')
T95 = 1.729  # t, 19 gl


def potencia_ni(d, margen, n=20, deltas=DELTAS, B=40_000):
    base = np.concatenate([d - np.median(d), -(d - np.median(d))])
    out = []
    for delta in deltas:
        idx = RNG.integers(0, len(base), size=(B, n))
        m = base[idx] + delta
        mu = m.mean(axis=1)
        sd = m.std(axis=1, ddof=1)
        li = mu - T95 * sd / math.sqrt(n)
        out.append(float(np.mean(li > -margen)))
    return out


for etq, nb in NUBES.items():
    margen = 10.0 if 'T-A' in etq else 10.0
    pot = potencia_ni(nb['d'], margen)
    log('')
    log(f"  {etq}   (margen {margen:.0f}; sd_d {nb['sd_d']:.2f})")
    log('    delta (ON - OFF) ->  ' + ''.join(f'{x:>+8.0f}' for x in DELTAS))
    log('    v3  P(PASA)          ' + ''.join(f'{x:>8.3f}' for x in pot))
    log('    v2  P(PASA)          ' + ''.join(f'{x:>8.3f}' for x in
                                              potencia_empirica(nb['d'], nb['umbral'], 20, DELTAS, B=40_000)))
log('')
log('   Lectura: en delta = 0 ("identico al tronco") v3 PASA casi siempre y v2 es un volado;')
log('   en delta = -20 ("dos veces peor que el margen declarado") las dos CAEN.')

# ---------------------------------------------------------------- 8) EL NULO MEDIDO, con datos reales del tronco
log('')
log('=' * 108)
log('8) EL NULO MEDIDO CON DATOS REALES DEL TRONCO (sin simular nada)')
log('=' * 108)
log('   Los brazos OFF de v15f-v2 (semillas 301-320) y de dE5-v2 (2021-2040) son EL MISMO organismo:')
log('   v14.2 con la perilla apagada (identidad bit a bit en los dos paquetes), el mismo mundo')
log('   (corre_vivo_rep2.BRAZOS), el mismo T = 100 000 y el mismo runner. Son dos muestras')
log('   independientes de la MISMA ley. Emparejarlas da un candidato-placebo PERFECTO: "el tronco')
log('   contra el tronco". Es el control negativo que el CRITERIO v2 nunca corrio.')
TA_f = carga('v15f_v2_20260921_123755_crudo_TA.json')
TA_d = carga('dE5_v2_20260921_152224_crudo_TA.json')
TC_f = carga('v15f_v2_20260921_123755_crudo_TCii.json')
TC_d = carga('dE5_v2_20260921_152224_crudo_TCii.json')
NULOS = [
    ('T-A  VIVO        (r)',       [c['r'] for c in sorted([x for x in TA_d if x['arm'] == 'OFF' and x['brazo'] == 'VIVO'], key=lambda x: x['seed'])],
     [c['r'] for c in sorted([x for x in TA_f if x['arm'] == 'OFF' and x['brazo'] == 'VIVO'], key=lambda x: x['seed'])], 0.50),
    ('T-A  CUELLO_MIN  (r)',       [c['r'] for c in sorted([x for x in TA_d if x['arm'] == 'OFF' and x['brazo'] == 'CUELLO_MIN'], key=lambda x: x['seed'])],
     [c['r'] for c in sorted([x for x in TA_f if x['arm'] == 'OFF' and x['brazo'] == 'CUELLO_MIN'], key=lambda x: x['seed'])], 0.50),
    ('T-A  VIVO  (-muertes)',      [-c['deaths'] for c in sorted([x for x in TA_d if x['arm'] == 'OFF' and x['brazo'] == 'VIVO'], key=lambda x: x['seed'])],
     [-c['deaths'] for c in sorted([x for x in TA_f if x['arm'] == 'OFF' and x['brazo'] == 'VIVO'], key=lambda x: x['seed'])], 0.50),
    ('T-C ii  (rev)',              [c['rev'] for c in sorted([x for x in TC_d if x['arm'] == 'OFF'], key=lambda x: x['seed'])],
     [c['rev'] for c in sorted([x for x in TC_f if x['arm'] == 'OFF'], key=lambda x: x['seed'])], 0.75),
]
log('')
log(f"{'medida (tronco vs tronco)':<26} {'med A':>7} {'med B':>7} {'A12 no par.':>12} "
    f"{'A12(1 orden)':>13} {'P(pasa) a) reordenar':>21} {'P(pasa) b) repartir 40':>23}")
log('-' * 108)
for etq, A, B_, umb in NULOS:
    A, B_ = np.array(A, float), np.array(B_, float)
    n = len(A)
    a_unp = float(np.mean([[1.0 if x > y else (0.5 if x == y else 0.0) for y in B_] for x in A]))
    a_par = a12(list(A), list(B_))
    # a) condicional: se conservan las dos muestras, se reordena el emparejamiento
    Bp = B_[np.array([RNG.permutation(n) for _ in range(100_000)])]
    aa = (np.sum(A[None, :] > Bp, axis=1) + 0.5 * np.sum(A[None, :] == Bp, axis=1)) / n
    # b) incondicional: se juntan las 40 corridas del tronco y se reparten al azar en dos brazos de 20
    pool = np.concatenate([A, B_])
    perm = np.array([RNG.permutation(2 * n) for _ in range(100_000)])
    X, Y = pool[perm[:, :n]], pool[perm[:, n:]]
    ab = (np.sum(X > Y, axis=1) + 0.5 * np.sum(X == Y, axis=1)) / n
    log(f"{etq:<26} {np.median(A):>7.1f} {np.median(B_):>7.1f} {a_unp:>12.3f} {a_par:>13.3f} "
        f"{float(np.mean(aa >= umb - 1e-12)):>21.3f} {float(np.mean(ab >= umb - 1e-12)):>23.3f}")

# 8b) la letra COMPLETA de T-A (tres clausulas, dos brazos) sobre el placebo perfecto
log('')
log('   8b) LA LETRA COMPLETA sobre el placebo perfecto (40 corridas reales del tronco repartidas al')
log('       azar en dos brazos de 20; cada semilla lleva sus dos mundos juntos, como en el runner):')
uni = []
for corr, ds in ((TA_f, 'v15f'), (TA_d, 'dE5')):
    por_seed = {}
    for c in corr:
        if c['arm'] == 'OFF':
            por_seed.setdefault(c['seed'], {})[c['brazo']] = (c['r'], c['deaths'])
    for s, v in por_seed.items():
        if 'VIVO' in v and 'CUELLO_MIN' in v:
            uni.append((v['VIVO'][0], v['VIVO'][1], v['CUELLO_MIN'][0], v['CUELLO_MIN'][1]))
U = np.array(uni, float)  # (40, 4): rV, dV, rC, dC
log(f'       unidades disponibles: {len(U)} semillas del tronco con sus dos mundos')
B8 = 100_000
perm = np.array([RNG.permutation(len(U)) for _ in range(B8)])
mitad = len(U) // 2
ON, OFF = U[perm[:, :mitad]], U[perm[:, mitad:]]
pasa_brazo = {}
for j, nom in ((0, 'VIVO'), (2, 'CUELLO_MIN')):
    rON, rOFF = ON[:, :, j], OFF[:, :, j]
    dON, dOFF = ON[:, :, j + 1], OFF[:, :, j + 1]
    a = (np.sum(rON > rOFF, axis=1) + 0.5 * np.sum(rON == rOFF, axis=1)) / mitad
    c1 = np.median(dON, axis=1) <= 1.10 * np.median(dOFF, axis=1)
    c2 = np.median(rON, axis=1) >= np.median(rOFF, axis=1) - 10.0
    c3 = a >= 0.50 - 1e-12
    pasa_brazo[nom] = (c1, c2, c3)
    log(f'       {nom:<11}  muertes<=1.10x {c1.mean():.3f}   r>=tronco-10 {c2.mean():.3f}   '
        f'A12>=0.50 {c3.mean():.3f}   brazo entero {(c1 & c2 & c3).mean():.3f}')
ta = (pasa_brazo['VIVO'][0] & pasa_brazo['VIVO'][1] & pasa_brazo['VIVO'][2]
      & pasa_brazo['CUELLO_MIN'][0] & pasa_brazo['CUELLO_MIN'][1] & pasa_brazo['CUELLO_MIN'][2])
log(f'       >>> T-A ENTERA sobre el placebo perfecto: PASA {ta.mean():.3f}  (CAE {1 - ta.mean():.3f})')
log(f'       >>> sin la clausula A12 (solo las dos medianas declaradas): PASA '
    f"{(pasa_brazo['VIVO'][0] & pasa_brazo['VIVO'][1] & pasa_brazo['CUELLO_MIN'][0] & pasa_brazo['CUELLO_MIN'][1]).mean():.3f}")
log(f'       >>> T-A y T-C (ii) juntas (independientes): PASA ~ {ta.mean() * 0.018:.4f}')
log('')
log('   "A12 no pareado" ~ 0.50 confirma que las dos muestras son de la misma ley (no hay efecto de serie).')
log('   Columna b) = probabilidad REAL de que la letra deje pasar al tronco disfrazado de candidato,')
log('   con corridas reales del tronco: T-A ~ 0.6 (un volado) y T-C (ii) ~ 0.02 (el tronco no se desdice')
log('   mejor que el tronco). Columna a) es la version condicionada a las dos muestras observadas.')
log('')
log(f'(salida escrita en {SALIDA})')
_fh.close()
