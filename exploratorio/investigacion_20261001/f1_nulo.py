"""f1_nulo.py - nulo simulado de la puerta de F1 del Reactor (BORRADOR, 1-oct-2026).

Simulacion numerica pura (numpy + math). NO corre el motor. Un proceso, segundos.
Uso:  python f1_nulo.py > f1_nulo_salida.txt

Estadistico por semilla: X = 1 si la semilla tiene >= 2 formas de regla funcionales DISTINTAS fijadas (PREREGISTRO_F1 seccion 6).
Por brazo: k = suma de X en n = 20 semillas (independientes entre tamanos: el mundo de esc 900 no es el de esc 90).
  k90, k900 = BLOQ_V a esc 90 y esc 900;  a90, a900 = BLOQ_AZA (deriva) a esc 90 y 900.
Puertas evaluadas:
  G0 (ficha)      : k900 >= 12  y  k90 <= 5
  G1(d, m)        : k900 - k90 >= d  y  k900 >= m
  GF(d, m)        : G1(d, m)  y  k900 - a900 >= d          (la deriva entra en la puerta)
  GDD(d, m)       : GF(d, m)  y  (k900 - k90) - (a900 - a90) >= d   (diferencia de diferencias; se reporta, no se propone)
Parte A: exacta (binomial). Parte B: Monte Carlo (semilla 20261001) con conteo de formas Poisson y con sobredispersion
entre semillas (beta-binomial), para ver si la exacta es optimista.
"""
import math
import sys
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass

N = 20
RNG = np.random.default_rng(20261001)


def pmf(n, p):
    return np.array([math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)])


K = np.arange(N + 1)


def p_g0(p90, p900):
    a, b = pmf(N, p90), pmf(N, p900)
    return float(a[K <= 5].sum() * b[K >= 12].sum())


def p_g1(p90, p900, d, m):
    a, b = pmf(N, p90), pmf(N, p900)
    J = np.outer(a, b)   # J[k90, k900]
    M = (K[None, :] - K[:, None] >= d) & (K[None, :] >= m)
    return float(J[M].sum())


def p_gf(p90, p900, q900, d, m):
    """G1 y k900 - a900 >= d, con a900 ~ Bin(N, q900) independiente."""
    a, b, c = pmf(N, p90), pmf(N, p900), pmf(N, q900)
    tot = 0.0
    for k9 in range(N + 1):
        if k9 < m: continue
        pa = a[K <= k9 - d].sum() if k9 - d >= 0 else 0.0
        pc = c[K <= k9 - d].sum() if k9 - d >= 0 else 0.0
        tot += b[k9] * pa * pc
    return float(tot)


def linea(x):
    return ' '.join(f'{v:7.4f}' for v in x)


print('f1_nulo.py - n = 20 semillas por brazo; puerta por SERIE; "serie Y replica" = cuadrado (semillas nuevas, independientes)')
print()
print('=' * 110)
print('A1. FALSO POSITIVO bajo H0 (misma p en esc 90 y esc 900). Exacto. Columnas: p base')
PS = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
print(f"{'puerta':22s} " + ' '.join(f'{p:7.2f}' for p in PS) + '   max(0.05-0.60)   max(0.01-0.99)')
FINO = np.arange(0.01, 0.995, 0.01)
PUERTAS = [('G0 ficha 12 vs <=5', None)] + [(f'G1 d={d} m={m}', (d, m)) for d in (5, 6, 7, 8, 9) for m in (8, 10, 12)]
for nom, dm in PUERTAS:
    f = (lambda p: p_g0(p, p)) if dm is None else (lambda p, dm=dm: p_g1(p, p, dm[0], dm[1]))
    v = [f(p) for p in PS]
    mx = max(f(p) for p in FINO if 0.05 <= p <= 0.60 + 1e-9); mxa = max(f(p) for p in FINO)
    print(f'{nom:22s} {linea(v)}   {mx:9.5f}        {mxa:9.5f}   | serie Y replica: {mx ** 2:.2e} / {mxa ** 2:.2e}')

print()
print('=' * 110)
print('A2. POTENCIA bajo alternativas (p90 -> p900). Exacto. Entre parentesis: serie Y replica')
ALT = [(0.05, 0.35), (0.05, 0.50), (0.10, 0.50), (0.10, 0.70), (0.25, 0.50), (0.25, 0.60), (0.25, 0.75), (0.40, 0.80),
       (0.40, 0.90), (0.60, 0.95), (0.02, 0.60)]
print(f"{'puerta':22s} " + ' '.join(f'{a:.2f}->{b:.2f}  ' for a, b in ALT))
for nom, dm in PUERTAS:
    f = (lambda a, b: p_g0(a, b)) if dm is None else (lambda a, b, dm=dm: p_g1(a, b, dm[0], dm[1]))
    print(f'{nom:22s} ' + ' '.join(f'{f(a, b):.2f}({f(a, b) ** 2:.2f})' for a, b in ALT))

print()
print('=' * 110)
print('A3. PUERTA CON DERIVA: GF(d, m) = G1(d, m) y k900 - a900 >= d  (a900 = semillas de BLOQ_AZA esc 900 con >= 2 formas fijadas)')
print('    Falso positivo bajo tres nulos; exacto. H0a: sin efecto de N ni de herencia (p90 = p900 = q900 = p).')
print('    H0b: mas N da mas formas tambien SIN herencia (muestreo/deriva): p90 = p, p900 = q900 = p_alto.')
print('    H0c: la herencia fija formas pero N no importa: p90 = p900 = p_alto, q900 = bajo.')
for d, m in ((6, 10), (7, 10), (7, 8), (8, 10)):
    fa = max(p_gf(p, p, p, d, m) for p in FINO)
    fb = max(p_gf(p, ph, ph, d, m) for p in (0.02, 0.05, 0.10, 0.25, 0.40) for ph in FINO)
    fc = max(p_gf(ph, ph, q, d, m) for q in (0.0, 0.02, 0.05, 0.10) for ph in FINO)
    print(f'  GF d={d} m={m}: max FP  H0a {fa:.5f}   H0b {fb:.5f}   H0c {fc:.5f}   | serie Y replica: '
          f'{fa ** 2:.2e}  {fb ** 2:.2e}  {fc ** 2:.2e}')
print('    Potencia de GF (p90 -> p900, q900 de deriva):')
for d, m in ((6, 10), (7, 10), (7, 8), (8, 10)):
    for q in (0.02, 0.10, 0.25):
        print(f'  GF d={d} m={m} q900={q:.2f}: ' + ' '.join(f'{a:.2f}->{b:.2f} {p_gf(a, b, q, d, m):.2f}({p_gf(a, b, q, d, m) ** 2:.2f})'
                                                         for a, b in ALT[:9]))

print()
print('=' * 110)
print('B1. MONTE CARLO (200 000 series por celda): formas fijadas por semilla ~ Poisson(lam); X = [formas >= 2].')
print('    Traduce "cuantas formas se fijan en promedio" a la p por semilla y repite G0 y G1(7,10).')
R = 200000


def mc_k(lam, r=R):
    return (RNG.poisson(lam, size=(r, N)) >= 2).sum(axis=1)


print(f"{'lam90':>6s} {'lam900':>6s} {'p90':>6s} {'p900':>6s} {'G0':>8s} {'G1(7,10)':>9s} {'G1(6,10)':>9s}  (x2 = cuadrado)")
for l90, l900 in ((0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (1.0, 2.0), (1.0, 2.5), (1.0, 3.0), (0.5, 2.0), (1.5, 3.0), (0.3, 1.5)):
    k90, k900 = mc_k(l90), mc_k(l900)
    g0 = np.mean((k900 >= 12) & (k90 <= 5)); g1 = np.mean((k900 - k90 >= 7) & (k900 >= 10)); g6 = np.mean((k900 - k90 >= 6) & (k900 >= 10))
    pp = lambda l: 1 - math.exp(-l) * (1 + l)
    print(f'{l90:6.2f} {l900:6.2f} {pp(l90):6.3f} {pp(l900):6.3f} {g0:8.4f} {g1:9.4f} {g6:9.4f}   ({g0 ** 2:.4f} {g1 ** 2:.4f} {g6 ** 2:.4f})')

print()
print('B2. MONTE CARLO con SOBREDISPERSION: la p "de la serie" no es fija; cada serie saca su p de una Beta(media p, concentracion c)')
print('    (lotes: hora, carga del PC, ventana de semillas). H0: las DOS escalas sacan p de la MISMA Beta, independientes.')
print('    Es el nulo que la binomial exacta no ve. Si serie y replica comparten el sesgo, el cuadrado tampoco vale.')
print(f"{'p':>5s} {'c':>5s} {'G0':>8s} {'G1(7,10)':>9s} {'G1(8,10)':>9s}")
for p in (0.2, 0.35, 0.5):
    for c in (1e9, 50.0, 20.0, 8.0):
        if c > 1e8: p90 = np.full(R, p); p900 = np.full(R, p)
        else: p90 = RNG.beta(p * c, (1 - p) * c, R); p900 = RNG.beta(p * c, (1 - p) * c, R)
        k90 = RNG.binomial(N, p90); k900 = RNG.binomial(N, p900)
        print(f"{p:5.2f} {('inf' if c > 1e8 else f'{c:.0f}'):>5s} {np.mean((k900 >= 12) & (k90 <= 5)):8.4f} "
              f"{np.mean((k900 - k90 >= 7) & (k900 >= 10)):9.4f} {np.mean((k900 - k90 >= 8) & (k900 >= 10)):9.4f}")

print()
print('=' * 110)
print('C. NULO DE DERIVA (modelo de juguete, declarado como tal): cuantas formas NEUTRAS llegan a >= 50 % sin funcion.')
print('   Wright-Fisher haploide con N cuerpos, G generaciones; en cada parto entra una regla nueva con prob p_ins = 0.02 y se')
print('   pierde cada regla con prob p_del_por_regla = 0.05 / L (L = 3). Cada insercion es una forma nueva (alelos infinitos:')
print('   cota BAJA de coincidencias; el espacio canonico real tiene ~10^2 formas, ver seccion 6). Se cuenta, al final, el numero')
print('   de formas con frecuencia >= 0.5 y la fraccion de corridas con >= 2. NO es el motor: sirve para la DIRECCION del efecto de N.')


def deriva(Nc, G, reps, p_ins=0.02, p_del=0.05 / 3):
    cnt2 = 0; tot = 0
    for _ in range(reps):
        # genoma = conjunto de ids de formas; se guarda como matriz booleana dinamica
        M = np.zeros((Nc, 0), bool)
        for g in range(G):
            M = M[RNG.integers(0, Nc, Nc)]
            if M.shape[1]:
                M &= RNG.random(M.shape) >= p_del
            nuevas = np.flatnonzero(RNG.random(Nc) < p_ins)
            if len(nuevas):
                E = np.zeros((Nc, len(nuevas)), bool); E[nuevas, np.arange(len(nuevas))] = True
                M = np.concatenate([M, E], axis=1)
            if g % 10 == 0 and M.shape[1]:
                M = M[:, M.any(axis=0)]
        f = M.mean(axis=0) if M.shape[1] else np.zeros(0)
        k = int((f >= 0.5).sum()); tot += k; cnt2 += (k >= 2)
    return tot / reps, cnt2 / reps


print(f"{'N':>5s} {'G':>5s} {'reps':>5s} {'formas >= 50 % (media)':>24s} {'P(>= 2 formas)':>16s}")
for Nc, G, reps in ((35, 100, 300), (35, 300, 200), (350, 100, 40), (350, 300, 20)):
    m, p2 = deriva(Nc, G, reps)
    print(f'{Nc:5d} {G:5d} {reps:5d} {m:24.3f} {p2:16.3f}')
print('   Lectura: ver PREREGISTRO_F1_reactor_BORRADOR.md seccion 7.')


# ================================================================ D. BASE MEDIDA (solo lectura de JSON ya guardados de BLOQUES)
# La LETRA de "forma" es la de PREREGISTRO_F1_reactor_BORRADOR.md seccion 6 (este es el codigo de referencia).
import glob, json, os

PATM = {'A': (1, 1, 0, 1, 0, 0), 'B': (1, 0, 1, 0, 1, 0), 'C': (0, 1, 1, 0, 0, 1), 'D': (0, 0, 1, 0, 1, 1)}   # corre_bloques.py:128
SENT = ['hambre', 'sed', 'cerca', 'pixF', 'pixM', 'Rult']; ACC = ['boca', 'hacia', 'quieto', 'parir']
W_SIL = 0.25      # |peso total de la forma en el cuerpo| < W_SIL -> silenciosa en ese cuerpo
FRAC_FIJ = 0.5    # fijada: >= 50 % de los vivos
MIN_VIVOS = 12    # con menos vivos en T la semilla no tiene formas fijadas (cuenta 0) y se reporta aparte


def condicion(r):
    """Devuelve (clave_de_condicion, giro) o None si la condicion es constante (nunca/siempre): regla silenciosa.
    giro = +1 o -1: el signo del peso se multiplica por giro (orientacion canonica)."""
    s, p, c, th = int(r[0]), int(r[1]), (r[2] > 0.5), float(r[3])
    if s in (3, 4):   # pixel j del foco / de la ultima letra mordida: tabla de verdad sobre A, B, C, D
        m = tuple(int((PATM[x][p] > th) if c else (PATM[x][p] < th)) for x in 'ABCD')
        if sum(m) in (0, 4): return None
        if m[0] == 1: return (SENT[s], m), 1            # orientacion canonica: la mascara que contiene a A
        return (SENT[s], tuple(1 - z for z in m)), -1  # complemento con el signo cambiado
    if (c and th >= 1.0) or ((not c) and th <= 0.0): return None   # x > 1 o x < 0: nunca (sentidos en [0, 1])
    return (SENT[s], '>'), (1 if c else -1)             # theta NO cuenta en sentidos continuos; '<' = '>' con signo cambiado


def formas_cuerpo(reglas):
    """Conjunto de formas NO silenciosas de un cuerpo. Duplicados: se suman los pesos (la copia es volumen, no forma nueva)."""
    W = {}
    for r in reglas:
        cg = condicion(r)
        if cg is None: continue
        k = (cg[0], ACC[int(r[4])]); W[k] = W.get(k, 0.0) + cg[1] * float(r[5])
    return {(k[0], k[1], '+' if w > 0 else '-') for k, w in W.items() if abs(w) >= W_SIL}


def formas_fijadas(vivos):
    """vivos = lista de [linaje, gen, fund, reglas] (BQ_OUT['vivos_T']). Devuelve dict forma -> fraccion, solo las fijadas."""
    if len(vivos) < MIN_VIVOS: return {}
    cnt = {}
    for x in vivos:
        for f in formas_cuerpo(x[3]): cnt[f] = cnt.get(f, 0) + 1
    return {f: c / len(vivos) for f, c in cnt.items() if c / len(vivos) >= FRAC_FIJ}


def nombre(f):
    (sen, m), acc, sg = f
    return f"{sen}[{''.join(x for x, z in zip('ABCD', m) if z) if isinstance(m, tuple) else m}]->{acc}{sg}"


BASE = r'C:\Users\User\Documents\PROYECTOS\JUACO\organelos\experimentos\organelos\bloques\opusM\datos'
print()
print('=' * 110)
print('D. BASE MEDIDA en los JSON de BLOQUES (esc 90; solo lectura). Formas fijadas SIN prueba de funcion (cota alta de la funcional).')
print(f'   W_SIL {W_SIL} · FRAC_FIJ {FRAC_FIJ} · MIN_VIVOS {MIN_VIVOS}')
if not os.path.isdir(BASE):
    print('   NO ESTA la carpeta de datos; seccion D omitida.')
else:
    for car, brs in (('serie_s48411-48430_T500000', ('BLOQ_V', 'BLOQ_AZA_V')), ('serie_s48431-48450_T500000', ('BLOQ_V', 'BLOQ_AZA_V')),
                     ('explora', ('BLOQ', 'BLOQ_AZA')), ('vivero100k', ('BLOQ_V', 'BLOQ_AZA_V'))):
        for b in brs:
            fs = sorted(glob.glob(os.path.join(BASE, car, f'M_{b}_s*.json')))
            if not fs: print(f'   {car} {b}: NO ESTA'); continue
            nf = []; nv = []; gen = []; U = []; rpc = []; lar = []; todas = {}; nlin = []
            for f in fs:
                d = json.load(open(f, encoding='utf-8')); B = d.get('bloques') or {}; vv = B.get('vivos_T') or []
                ff = formas_fijadas(vv); nf.append(len(ff)); nv.append(len(vv))
                for z in ff: todas[nombre(z)] = todas.get(nombre(z), 0) + 1
                if vv:
                    gen.append(float(np.median([x[1] for x in vv]))); lar.append(float(np.mean([len(x[3]) for x in vv])))
                    nlin.append(len({x[0] for x in vv}))
                ev = sum(B.get(k, 0) for k in ('n_campo', 'n_dup', 'n_del', 'n_ins', 'n_hgt')); nh = B.get('n_hijos', 0) + B.get('n_fund', 0)
                if nh: U.append(ev / nh)
                if d.get('K') and d.get('n_nac') is not None: rpc.append(d['n_nac'] / d['K'])
            nf = np.array(nf)
            md = lambda v: (f'{np.median(v):.2f} [{np.min(v):.2f}-{np.max(v):.2f}]' if len(v) else 'NO ESTA')
            print(f'   {car} · {b} · n {len(fs)}: semillas con >= {MIN_VIVOS} vivos {int((np.array(nv) >= MIN_VIVOS).sum())} · vivos en T {md(nv)}')
            print(f'      formas fijadas por semilla: {nf.tolist()}')
            print(f'      semillas con >= 1: {int((nf >= 1).sum())} · con >= 2: {int((nf >= 2).sum())} · con >= 3: {int((nf >= 3).sum())}')
            print(f'      generacion (I_GEN) mediana de los vivos en T: {md(gen)} · linajes vivos: {md(nlin)} · largo medio: {md(lar)}')
            print(f'      eventos de operador por cuerpo nuevo (U, toda la corrida): {md(U)} · n_nac / K (si estan): {md(rpc)}')
            if gen and U: print(f'      PROXY profundidad mutacional = U x generacion mediana: {np.median(U) * np.median(gen):.1f} (inferencia, no medida)')
            print('      formas (semillas en que estan fijadas): ' + ' | '.join(f'{k} {v}' for k, v in sorted(todas.items(), key=lambda z: -z[1])))


# ================================================================ v2 (1-oct, tras la sonda del coordinador): secciones E, F, G
def tipo(r):   # COPIA de corre_bloques.tipo (corre_bloques.py:120-125), la "forma" que usa el coordinador (240 posibles)
    s, p, c, th, a, w = r
    s = int(s); a = int(a)
    sen = SENT[s] + (f'{int(p)}' if s in (3, 4) else '')
    return f"{sen}{'>' if c > 0.5 else '<'}θ -> {ACC[a]}{'+' if w > 0 else '-'}"


RECH = (('pixF', (1, 0, 1, 0)), 'boca', '+')   # el organo de rechazo en la letra canonica: pixF[AC]->boca+
RS = np.random.default_rng(20261002)


def frecs(vivos, canon=True):
    cnt = {}
    for x in vivos:
        fs = formas_cuerpo(x[3]) if canon else set(tipo(r) for r in x[3])
        for f in fs: cnt[f] = cnt.get(f, 0) + 1
    return cnt


def d5(vivos):
    """Diversidad sostenida SIN filtro de funcion: formas canonicas distintas del organo de rechazo con frecuencia >= 5 % y >= 3 portadores."""
    n = len(vivos)
    if n < MIN_VIVOS: return None
    return sum(1 for f, c in frecs(vivos).items() if f != RECH and c / n >= 0.05 and c >= 3)


def d_rar(vivos, m=24, reps=200):
    """Rarificada: media, sobre 200 submuestras de m vivos sin reemplazo, de las formas (sin rechazo) con >= 2 portadores en la submuestra."""
    if len(vivos) < m: return None
    F = [formas_cuerpo(x[3]) - {RECH} for x in vivos]; tot = 0
    for _ in range(reps):
        cnt = {}
        for i in RS.choice(len(F), m, replace=False):
            for f in F[i]: cnt[f] = cnt.get(f, 0) + 1
        tot += sum(1 for c in cnt.values() if c >= 2)
    return tot / reps


def carga(car, b):
    out = []
    for f in sorted(glob.glob(os.path.join(BASE, car, f'M_{b}_s*.json'))):
        d = json.load(open(f, encoding='utf-8')); out.append((d['seed'], ((d.get('bloques') or {}).get('vivos_T') or [])))
    return out


print()
print('=' * 110)
print('E. RECONCILIACION 14/20 (coordinador, tipo()) vs 13/20 (v1, letra canonica) en BLOQ_V esc 90 T 500k')
for car in ('serie_s48411-48430_T500000', 'serie_s48431-48450_T500000'):
    S = carga(car, 'BLOQ_V'); nt = []; nc = []; dif = []
    for seed, vv in S:
        n = max(1, len(vv))
        ft = {f: c / n for f, c in frecs(vv, canon=False).items() if c / n >= 0.5} if vv else {}
        fc = formas_fijadas(vv)
        nt.append(len(ft)); nc.append(len(fc))
        if (len(ft) >= 2) != (len(fc) >= 2):
            dif.append(f"s{seed} (vivos {len(vv)}): tipo() {sorted(ft)} · canonica {sorted(nombre(z) for z in fc)}")
    print(f'   {car}: tipo() >= 2 fijadas en {sum(x >= 2 for x in nt)}/20 · canonica >= 2 en {sum(x >= 2 for x in nc)}/20')
    print(f'      por semilla tipo():    {nt}')
    print(f'      por semilla canonica:  {nc}')
    for x in dif: print('      DIFIERE ' + x)

print()
print('=' * 110)
print('F. BASE DE LAS DOS LECTURAS CON EL ORGANO DE RECHAZO EXCLUIDO (sin filtro de funcion: cota alta)')
print('   L1 = formas fijadas (>= 50 %) distintas del rechazo · L2 = D5 (>= 5 % y >= 3 portadores) · rar = rarificada a 24 vivos, >= 2 portadores')
SONDA = r'C:\Users\User\Documents\PROYECTOS\JUACO\organelos\experimentos\organelos\reactor\datos\sonda'
GR = [('esc 90 T 500k serie', [v for _, v in carga('serie_s48411-48430_T500000', 'BLOQ_V')]),
      ('esc 90 T 500k replica', [v for _, v in carga('serie_s48431-48450_T500000', 'BLOQ_V')]),
      ('esc 90 T 200k vivero100k', [v for _, v in carga('vivero100k', 'BLOQ_V')]),
      ('esc 90 T 200k vivero100k_rep', [v for _, v in carga('vivero100k_rep', 'BLOQ_V')])]
for seed, esc in ((49702, 300), (49703, 900), (49704, 1200)):
    f = os.path.join(SONDA, f'M_BLOQ_V_s{seed}.json')
    if os.path.exists(f):
        GR.append((f'SONDA esc {esc} T 200k (1 semilla)', [((json.load(open(f, encoding='utf-8')).get('bloques') or {}).get('vivos_T') or [])]))
for nom, VS in GR:
    if not VS: print(f'   {nom}: NO ESTA'); continue
    l1 = [len([f for f in formas_fijadas(v) if f != RECH]) for v in VS]
    l2 = [d5(v) for v in VS]; lr = [d_rar(v) for v in VS]; nv = [len(v) for v in VS]
    pres = [len([f for f in frecs(v) if f != RECH]) for v in VS]
    ok2 = [x for x in l2 if x is not None]; okr = [x for x in lr if x is not None]
    print(f'   {nom} · n {len(VS)} · vivos {nv}')
    print(f'      L1 fijadas sin rechazo: {l1} · semillas con >= 1: {sum(x >= 1 for x in l1)} · con >= 2: {sum(x >= 2 for x in l1)}')
    print(f'      formas canonicas presentes (>= 1 portador, sin rechazo): {pres}')
    print(f'      L2 D5: {l2} · media {np.mean(ok2):.2f} · mediana {np.median(ok2):.1f} · var {np.var(ok2):.2f}' if ok2 else '      L2 D5: sin semillas validas')
    print(f'      rarificada (m 24): {[None if x is None else round(x, 2) for x in lr]} · media {np.mean(okr):.2f}' if okr else '      rarificada: sin semillas con >= 24 vivos')

print()
print('=' * 110)
print('G. NULO Y POTENCIA DE LA LECTURA CO-PRINCIPAL L2 (diversidad funcional sostenida, D5 por semilla; 20 vs 20, no pareado)')
print('   Puerta L2(Z, DM): Mann-Whitney unilateral (aprox. normal con correccion de empates y de continuidad) z >= Z y')
print('   diferencia de medianas >= DM. D ~ binomial negativa de media lam y var = lam * phi (phi = 1: Poisson). rng 20261003.')
RG_ = np.random.default_rng(20261003)


def saca(lam, phi, r):
    if phi <= 1.0001: return RG_.poisson(lam, (r, N)).astype(float)
    pnb = 1.0 / phi; nnb = lam * pnb / (1 - pnb)
    return RG_.negative_binomial(nnb, pnb, (r, N)).astype(float)


def mw_z(a, b):
    """z de Mann-Whitney de b > a, por fila (a, b: r x N), con rangos medios y correccion de empates."""
    x = np.concatenate([a, b], axis=1); n = x.shape[1]
    lt = (x[:, :, None] > x[:, None, :]).sum(axis=2); eq = (x[:, :, None] == x[:, None, :]).sum(axis=2)
    rank = lt + (eq + 1) / 2.0
    U = rank[:, N:].sum(axis=1) - N * (N + 1) / 2.0
    tie = (eq ** 2 - 1).sum(axis=1)                      # = suma de (t^3 - t) sobre los grupos de empate
    var = N * N / 12.0 * ((n + 1) - tie / (n * (n - 1.0)))
    var = np.where(var <= 0, np.inf, var)
    return (U - N * N / 2.0 - 0.5) / np.sqrt(var)


def puerta_l2(l90, l900, phi, Z, DM, r=40000):
    acc = 0; B = 5000
    for _ in range(0, r, B):
        a = saca(l90, phi, B); b = saca(l900, phi, B)
        z = mw_z(a, b); dm = np.median(b, axis=1) - np.median(a, axis=1)
        acc += int(((z >= Z) & (dm >= DM)).sum())
    return acc / r


CFG = ((1.645, 0), (2.326, 0), (2.326, 1), (2.576, 1))
print('   FALSO POSITIVO (H0: lam90 = lam900), 40 000 series por celda')
print(f"{'lam':>6s} {'phi':>4s} | " + ' | '.join(f'Z {Z} DM {DM}' for Z, DM in CFG))
for lam in (0.5, 1.5, 3.0, 6.0):
    for phi in (1.0, 2.0, 4.0):
        print(f'{lam:6.1f} {phi:4.1f} | ' + ' | '.join(f'{puerta_l2(lam, lam, phi, Z, DM):12.4f}' for Z, DM in CFG))
print('   POTENCIA de L2(Z 2.326, DM 1); entre parentesis, serie Y replica')
print(f"{'lam90 -> lam900':>18s} | " + ' | '.join(f'phi {p}      ' for p in (1.0, 2.0, 4.0)))
for l90, l900 in ((1.0, 2.0), (1.0, 3.0), (2.0, 3.0), (2.0, 4.0), (3.0, 4.5), (3.0, 6.0), (1.5, 6.0), (4.0, 6.0), (4.0, 8.0)):
    v = [puerta_l2(l90, l900, phi, 2.326, 1) for phi in (1.0, 2.0, 4.0)]
    print(f'{l90:8.1f} -> {l900:6.1f} | ' + ' | '.join(f'{x:.2f} ({x * x:.2f})' for x in v))
