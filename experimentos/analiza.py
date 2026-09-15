#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analiza.py -- Fase 1 del PLAN: resumen de una o varias corridas de datos/.

Lee los CSV/JSON producidos por run_etapa.py (o cualquier CSV con las columnas
del baseline) y reporta SIEMPRE mediana, rango (min-max) y cuartiles p25-p75.
Regla 6 del proyecto: nunca solo medias. La media y la sd se imprimen ademas,
pero nunca en lugar de la mediana y el rango.

Uso:
    python experimentos/analiza.py --etapa E1
    python experimentos/analiza.py datos/E1_v6_20260915_120000.json
    python experimentos/analiza.py --etapa E1 --baseline
    python experimentos/analiza.py A.json --vs B.json

==============================================================================
METRICAS (punto 8 del BRIEF_ORIGINAL). Las 8 primeras ya existian; las dos
ultimas (variabilidad, diversidad) estaban marcadas PENDIENTE y se definen aqui
por primera vez. Se marcan como PROPUESTAS, no como definiciones establecidas.
==============================================================================

 1. SUPERVIVENCIA = numero de muertes en T pasos (menos es mejor).
    Directo de run(): deaths. Es la metrica correcta del proyecto, no la comida.

 2. VIDA = T / muertes = pasos medios entre muertes.
    Con muertes=0 se reporta ">= T".

 3. COMIDA = mordidas sobre estimulos nutritivos.
    Se reporta comidaA (mordidas de A, comparable con el baseline) y ademas
    comida_efectiva = mordidas sobre lo que era nutritivo en ESE cuarto,
    usando los kwargs del escenario (invertir_en, nuevo, nuevo_val) del JSON.

 4. VENENO = mordidas sobre estimulos toxicos.
    Se reporta venenoB total y por cuarto, y veneno_efectivo (misma atribucion
    por cuarto que comida_efectiva).

 5. ENERGIA = balance energetico neto DERIVADO:
        sum(mordidas * dE(valencia)) - costo*T,  dE: comida +0.8, veneno -0.4.
    run() no devuelve E, asi que esto es una reconstruccion del presupuesto, no
    una medicion. Se marca como derivada en todas las salidas.

 6. TASA DE APRENDIZAJE = cambio de la tasa de mordida POR VISITA entre cuartos
    (la unidad adoptada por el proyecto tras el error de 2H: tasa, no conteo).
    Se reporta tasaA_q1..q4, tasaB_q1..q4, el ratio de discriminacion
    tasaA_q4/tasaB_q4 y el ratio de reduccion de veneno venenoB_q1/venenoB_q4.

 7. VELOCIDAD DE APRENDIZAJE = primer paso t a partir del cual
    |W(t) - valor asintotico| < 0.1 y se mantiene asi hasta el final.
    Asintota = ultimo valor de W en el log. Requiere log: correr con
    --param log_cada=N. Sin log se reporta 'no medible (sin log)'.
    En escenarios con invertir_en se mide ademas la reconvergencia a partir de
    invertir_en (cuanto tarda en re-aprender despues de la inversion).

 8. RECUPERACION = cuanto del rendimiento previo a la perturbacion se restaura.
        recuperacion = tasa_por_visita(estimulo nutritivo vigente en Q4, Q4)
                     / tasa_por_visita(estimulo nutritivo vigente en Q2, Q2)
    1.0 = recuperacion completa. En E1 (sin perturbacion) es tasaA_q4/tasaA_q2 y
    vale ~1 trivialmente; sirve de control. Se reporta ademas el conteo absoluto
    de mordidas del nutritivo vigente en Q4 (el criterio 'come B Q4>=50' de E2).

 9. VARIABILIDAD  -- DEFINICION PROPUESTA, NUEVA, NO ESTABLECIDA --
    Dispersion ENTRE SEMILLAS de una misma condicion (mismo escenario, mismos
    parametros; lo unico que cambia es la semilla). Operacionalizada como:
        - CV(muertes)  = sd/|media| de las muertes entre semillas
        - CV(comidaA)  = sd/|media| de la comida entre semillas
        - sd(W_A), sd(W_B) en unidades absolutas de W (no CV: W_A~+1 y W_B~-3
          son escalas fijas y un CV seria enganoso cerca de 0)
    Lectura: mide cuanto depende el resultado del azar de la inicializacion y
    del mundo. CV bajo en muertes con sd(W) ~0 = condicion reproducible.
    NO se afirma que sea la unica operacionalizacion razonable.

10. DIVERSIDAD  -- DEFINICION PROPUESTA, NUEVA, NO ESTABLECIDA --
    Cuan distintos son los ORGANISMOS entre si en conducta, no cuanto varia una
    cifra suelta. Se construye un vector de comportamiento por semilla:
        [comidaA, venenoB, muertes, tasaA_q4, tasaB_q4, W_A, W_B]
    cada componente se normaliza por z-score ENTRE SEMILLAS (media 0, sd 1;
    componente con sd=0 aporta 0), y se toma la distancia euclidea media por
    pares. Se reporta cruda y dividida por sqrt(d) (d = componentes con sd>0),
    para que sea comparable entre corridas con distinto numero de dimensiones.
    Referencia de escala: con componentes independientes y z-scoreados, la
    distancia media por pares esperada es ~sqrt(2*d), o sea ~1.41 por dimension.
    Valores muy por debajo de 1.41/dim = semillas parecidas (clones de conducta)
    en la estructura de correlacion de esa condicion; muy por encima = colas
    largas / semillas atipicas. OJO: la normalizacion z es relativa a la propia
    corrida, asi que la diversidad mide FORMA de la nube, no escala absoluta; por
    eso se reporta SIEMPRE junto a la variabilidad (punto 9), que si es absoluta.
    NO se afirma que sea la unica operacionalizacion razonable.
==============================================================================
"""
import argparse
import csv
import glob
import json
import math
import os
import sys

import numpy as np

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DIR_DATOS = os.path.join(RAIZ, 'datos')
BASELINE = os.path.join(DIR_DATOS, 'baseline_v6.csv')

E_VAL = {'comida': +0.8, 'veneno': -0.4}

# Medianas de referencia del registro (baseline v6, 20 semillas): A_sin / B_aprende
REF_BASELINE = {
    'comidaA':    (1400.0, 338.0),
    'venenoB_q4': (370.0, 13.0),
    'muertes':    (218.0, 142.0),
    'W_A':        (0.0, 1.00),
    'W_B':        (0.0, -3.00),
}

# Criterios preregistrados, copiados de organismo/bateria.py.
CRITERIOS = {
    'E1': {
        'venenoQ4<Q1': lambda r: r['venenoB_q4'] < r['venenoB_q1'],
        'W_A~+1':      lambda r: abs(r['W_A'] - 1) < .15,
        'W_B~-3':      lambda r: abs(r['W_B'] + 3) < .3,
    },
    'E2': {
        'W_A->-3':     lambda r: abs(r['W_A'] + 3) < .3,
        'W_B->+1':     lambda r: abs(r['W_B'] - 1) < .15,
        'come B Q4>=50': lambda r: r['venenoB_q4'] >= 50,
    },
    'E2I': {
        'W_C<=-2.5':   lambda r: r['W_C'] <= -2.5,
        'W_A~+1':      lambda r: abs(r['W_A'] - 1) < .15,
        'W_B<=-2.8':   lambda r: r['W_B'] <= -2.8,
        'tasaA Q4>=80%Q2': lambda r: r['tasaA_q4'] >= .8 * r['tasaA_q2'],
    },
    'E2J': {'W_D>=0.85': lambda r: r['W_D'] >= .85, 'W_B<=-2.7': lambda r: r['W_B'] <= -2.7},
    'E2K': {'W_D>=0.8':  lambda r: r['W_D'] >= .8,  'W_B<=-2.4': lambda r: r['W_B'] <= -2.4},
    'CTRL': {},
    'LIBRE': {},
}


# ----------------------------------------------------------------------------
# carga
# ----------------------------------------------------------------------------
class Corrida:
    """Una corrida: filas por semilla + (si hay JSON) crudos y procedencia."""

    def __init__(self, nombre, filas, proc=None, crudos=None, cond=None):
        self.nombre = nombre
        self.filas = filas
        self.proc = proc or {}
        self.crudos = crudos or []
        self.cond = cond

    @property
    def n(self):
        return len(self.filas)

    @property
    def etapa(self):
        return self.proc.get('etapa') or self.cond or '?'

    @property
    def kwargs(self):
        return (self.proc.get('escenario') or {}).get('kwargs_completos_de_run', {}) or {}

    @property
    def T(self):
        k = self.kwargs.get('T')
        if k:
            return int(k)
        t = self.col('T')
        if t and t[0]:
            return int(t[0])
        return 100000

    def col(self, nombre):
        return [f.get(nombre) for f in self.filas]


def _num(v):
    if v is None or v == '':
        return None
    if isinstance(v, (int, float)):
        return v
    try:
        x = float(v)
    except (TypeError, ValueError):
        return v
    return int(x) if x == int(x) and '.' not in str(v) and 'e' not in str(v).lower() else x


def carga_csv(ruta, cond=None):
    with open(ruta, newline='', encoding='utf-8-sig') as f:
        filas = [{k: _num(v) for k, v in row.items()} for row in csv.DictReader(f)]
    if cond is not None:
        filas = [r for r in filas if str(r.get('cond', '')) == cond]
    return filas


def carga(ruta, cond=None):
    ruta = os.path.abspath(ruta)
    if not os.path.exists(ruta):
        raise SystemExit(f'ERROR: no existe {ruta}')
    base, ext = os.path.splitext(ruta)
    ext = ext.lower()
    proc, crudos = None, None
    if ext == '.json':
        with open(ruta, encoding='utf-8') as f:
            doc = json.load(f)
        proc = doc.get('procedencia', {})
        crudos = doc.get('resultados', [])
        csv_par = base + '.csv'
        if os.path.exists(csv_par):
            filas = carga_csv(csv_par)
        else:
            filas = [_fila_desde_crudo(c, proc) for c in crudos]
    elif ext == '.csv':
        filas = carga_csv(ruta, cond=cond)
        json_par = base + '.json'
        if os.path.exists(json_par):
            with open(json_par, encoding='utf-8') as f:
                doc = json.load(f)
            proc = doc.get('procedencia', {})
            crudos = doc.get('resultados', [])
    else:
        raise SystemExit(f'ERROR: extension no soportada: {ruta}')
    if not filas:
        raise SystemExit(f'ERROR: 0 filas en {ruta}' + (f' (cond={cond})' if cond else ''))
    etiqueta = os.path.basename(ruta) + (f'[cond={cond}]' if cond else '')
    return Corrida(etiqueta, filas, proc, crudos, cond)


def _fila_desde_crudo(c, proc):
    """Reconstruye la fila plana desde el crudo del JSON (si faltara el CSV)."""
    m, v = c['mord'], c['vis']
    f = {'seed': c['seed'], 'comidaA': sum(m['A']), 'venenoB': sum(m['B']),
         'muertes': c['deaths'], 'visitasA': sum(v['A']), 'visitasB': sum(v['B'])}
    for i in range(4):
        f[f'comidaA_q{i+1}'] = m['A'][i]
        f[f'venenoB_q{i+1}'] = m['B'][i]
        f[f'visitasA_q{i+1}'] = v['A'][i]
        f[f'visitasB_q{i+1}'] = v['B'][i]
        f[f'tasaA_q{i+1}'] = round(100 * m['A'][i] / max(v['A'][i], 1), 2)
        f[f'tasaB_q{i+1}'] = round(100 * m['B'][i] / max(v['B'][i], 1), 2)
    for k in 'ABCD':
        f[f'W_{k}'] = c['W'][k]
        f[f'Wp{k}'], f[f'Wn{k}'] = c['comp'][k]
    if 'splits' in c:
        f['splits'] = c['splits']
        f['celdas'] = c['celdas']
    return f


def mas_reciente(etapa):
    pats = [os.path.join(DIR_DATOS, f'{etapa}_*.json'), os.path.join(DIR_DATOS, f'{etapa}_*.csv')]
    cands = []
    for p in pats:
        cands += glob.glob(p)
    if not cands:
        raise SystemExit(f'ERROR: no hay archivos de la etapa {etapa!r} en {DIR_DATOS}')
    # preferimos JSON; entre iguales, el mas nuevo por mtime
    cands.sort(key=lambda p: (os.path.splitext(p)[1].lower() != '.json', -os.path.getmtime(p)))
    return cands[0]


# ----------------------------------------------------------------------------
# estadistica: SIEMPRE mediana + rango + cuartiles (regla 6)
# ----------------------------------------------------------------------------
def resumen(vals):
    a = np.asarray([float(v) for v in vals
                    if v is not None and v != '' and not (isinstance(v, float) and math.isnan(v))],
                   dtype=float)
    if a.size == 0:
        return None
    return {'n': int(a.size), 'mediana': float(np.median(a)),
            'min': float(a.min()), 'max': float(a.max()),
            'p25': float(np.percentile(a, 25)), 'p75': float(np.percentile(a, 75)),
            'media': float(a.mean()), 'sd': float(a.std(ddof=1)) if a.size > 1 else 0.0}


def linea(nombre, s, dec=2, ancho=26):
    if s is None:
        return f'  {nombre:<{ancho}} (sin datos)'
    f = f'.{dec}f'
    return (f'  {nombre:<{ancho}} mediana {s["mediana"]:>10{f}}   '
            f'rango [{s["min"]:{f}} .. {s["max"]:{f}}]   '
            f'p25-p75 [{s["p25"]:{f}} .. {s["p75"]:{f}}]   '
            f'(media {s["media"]:{f}} sd {s["sd"]:{f}}, n={s["n"]})')


def bloque(titulo):
    print()
    print(titulo)
    print('-' * len(titulo))


# ----------------------------------------------------------------------------
# valencias por cuarto (para comida/veneno efectivos y energia)
# ----------------------------------------------------------------------------
def valencias_por_cuarto(kwargs, T):
    inv = kwargs.get('invertir_en', None)
    nuevo = kwargs.get('nuevo', None)
    nuevo_en = kwargs.get('nuevo_en', 50000)
    nuevo_val = kwargs.get('nuevo_val', 'veneno')
    qlen = max(T // 4, 1)
    out = {}
    for st in 'ABCD':
        fila = []
        for qi in range(4):
            t0 = qi * qlen
            if st == 'A':
                v = 'comida' if (inv is None or t0 < inv) else 'veneno'
            elif st == 'B':
                v = 'veneno' if (inv is None or t0 < inv) else 'comida'
            elif nuevo == st and t0 >= nuevo_en:
                v = nuevo_val
            else:
                v = None
            fila.append(v)
        out[st] = fila
    return out


def nutritivo_en(val, qi):
    for st in 'ABCD':
        if val[st][qi] == 'comida':
            return st
    return None


# ----------------------------------------------------------------------------
# velocidad de aprendizaje (usa el log del JSON si existe)
# ----------------------------------------------------------------------------
IDX_W = {'A': 1, 'B': 2, 'C': 3, 'D': 4}


def velocidad(log, estimulo, t_min=0):
    """Primer t >= t_min con |W - asintota| < 0.1 de forma SOSTENIDA hasta el final.

    Asintota = ultimo valor logueado de ese estimulo. None si no converge o sin log.
    """
    if not log:
        return None
    i = IDX_W[estimulo]
    pts = [(e[0], e[i]) for e in log if e[0] >= t_min and e[i] is not None]
    if len(pts) < 2:
        return None
    asin = pts[-1][1]
    ultimo_malo = None
    for j, (t, w) in enumerate(pts):
        if abs(w - asin) >= 0.1:
            ultimo_malo = j
    if ultimo_malo is None:
        return pts[0][0]
    if ultimo_malo + 1 >= len(pts):
        return None
    return pts[ultimo_malo + 1][0]


def t_fraccion(log, estimulo, frac=0.9, t_min=0):
    """Primer t >= t_min en que W ha recorrido `frac` del cambio total W(t_min)->W(final).

    Medida COMPLEMENTARIA de la velocidad. La de arriba (banda 0.1 sostenida) queda
    dominada por la cola asintotica, que en este organismo esta limitada por
    EXPOSICION (un estimulo temido se re-muestrea poco), no por la tasa de
    aprendizaje. t90 separa las dos cosas. None si el cambio total es < 0.1.
    """
    if not log:
        return None
    i = IDX_W[estimulo]
    pts = [(e[0], e[i]) for e in log if e[0] >= t_min and e[i] is not None]
    if len(pts) < 2:
        return None
    w0, wf = pts[0][1], pts[-1][1]
    if abs(wf - w0) < 0.1:
        return None
    objetivo = w0 + frac * (wf - w0)
    for t, w in pts:
        if (w >= objetivo) if wf > w0 else (w <= objetivo):
            return t
    return None


# ----------------------------------------------------------------------------
# variabilidad y diversidad (definiciones PROPUESTAS, ver docstring)
# ----------------------------------------------------------------------------
DIMS_CONDUCTA = ['comidaA', 'venenoB', 'muertes', 'tasaA_q4', 'tasaB_q4', 'W_A', 'W_B']


def variabilidad(c):
    out = {}
    for k in ('muertes', 'comidaA', 'venenoB'):
        s = resumen(c.col(k))
        if s and abs(s['media']) > 1e-12:
            out[f'CV({k})'] = s['sd'] / abs(s['media'])
        elif s:
            out[f'CV({k})'] = float('nan')
    for k in ('W_A', 'W_B'):
        s = resumen(c.col(k))
        if s:
            out[f'sd({k})'] = s['sd']
    return out


def diversidad(c):
    cols, usadas, descartadas = [], [], []
    for d in DIMS_CONDUCTA:
        vals = [v for v in c.col(d) if v is not None and v != '']
        if len(vals) != c.n:
            descartadas.append((d, 'columna ausente'))
            continue
        a = np.asarray(vals, dtype=float)
        sd = a.std(ddof=0)
        if sd < 1e-12:
            descartadas.append((d, 'sd=0 (aporta 0)'))
            continue
        cols.append((a - a.mean()) / sd)
        usadas.append(d)
    if not cols or c.n < 2:
        return {'error': 'insuficiente (n<2 o todas las dimensiones degeneradas)',
                'usadas': usadas, 'descartadas': descartadas}
    X = np.vstack(cols).T                       # n x d
    n, d = X.shape
    dists = []
    for i in range(n):
        for j in range(i + 1, n):
            dists.append(float(np.linalg.norm(X[i] - X[j])))
    a = np.asarray(dists)
    return {'usadas': usadas, 'descartadas': descartadas, 'd': d, 'pares': len(dists),
            'media': float(a.mean()), 'mediana': float(np.median(a)),
            'min': float(a.min()), 'max': float(a.max()),
            'p25': float(np.percentile(a, 25)), 'p75': float(np.percentile(a, 75)),
            'media_por_dim': float(a.mean() / math.sqrt(d)),
            'esperado_por_dim_indep': math.sqrt(2.0)}


# ----------------------------------------------------------------------------
# informe
# ----------------------------------------------------------------------------
def criterios_de(c):
    et = str(c.etapa).upper()
    return CRITERIOS.get(et, {})


def cuenta_criterios(c):
    crit = criterios_de(c)
    out = {}
    for nombre, fn in crit.items():
        ok = 0
        for r in c.filas:
            try:
                ok += bool(fn(r))
            except (KeyError, TypeError):
                ok = None
                break
        out[nombre] = ok
    return out


def informe(c):
    T = c.T
    kw = c.kwargs
    val = valencias_por_cuarto(kw, T)

    print('=' * 92)
    print(f'CORRIDA: {c.nombre}')
    print('=' * 92)
    if c.proc:
        p = c.proc
        org = p.get('organismo', {})
        sc = p.get('script', {})
        ent = p.get('entorno', {})
        print(f'  etapa        : {p.get("etapa")}    semillas: {p.get("n_semillas")}    T: {T}')
        print(f'  llamada      : {(p.get("escenario") or {}).get("llamada")}')
        print(f'  organismo    : {org.get("modulo")}.py  sha256_16={org.get("sha256_16")}')
        print(f'  script       : {os.path.basename(str(sc.get("archivo")))}  sha256_16={sc.get("sha256_16")}')
        print(f'  entorno      : Python {ent.get("python")}  NumPy {ent.get("numpy")}  '
              f'{ent.get("procesos_usados")} procesos ({ent.get("metodo_arranque_mp")})')
        print(f'  fecha        : {p.get("fecha_iso")}')
        print(f'  equivalencia : {p.get("equivalencia_paralelo_vs_secuencial")}')
    else:
        print(f'  (CSV sin JSON de procedencia; etapa asumida = {c.etapa}, T = {T})')
    print(f'  n semillas   : {c.n}')
    print(f'  valencias por cuarto: ' +
          '  '.join(f'{st}=[' + ','.join((v[0] if v else '-') for v in val[st]) + ']' for st in 'ABCD') +
          '   (c=comida, v=veneno, -=ausente)')

    # --- criterios preregistrados ---
    cc = cuenta_criterios(c)
    if cc:
        bloque('CRITERIOS PREREGISTRADOS (copiados de organismo/bateria.py)')
        for k, v in cc.items():
            print(f'  {k:<22} {("%d/%d" % (v, c.n)) if v is not None else "no evaluable (faltan columnas)"}')

    # --- 1-2 supervivencia y vida ---
    bloque('1-2. SUPERVIVENCIA Y VIDA')
    print(linea('muertes (menos=mejor)', resumen(c.col('muertes')), 1))
    vidas = [T / max(m, 1) for m in c.col('muertes') if m is not None]
    print(linea('vida = T/muertes (pasos)', resumen(vidas), 1))

    # --- 3-4 comida y veneno ---
    bloque('3-4. COMIDA Y VENENO')
    print(linea('comidaA (mordidas de A)', resumen(c.col('comidaA')), 1))
    print(linea('venenoB (mordidas de B)', resumen(c.col('venenoB')), 1))
    for q in (1, 2, 3, 4):
        print(linea(f'venenoB_q{q}', resumen(c.col(f'venenoB_q{q}')), 1))
    com_ef, ven_ef = [], []
    for f in c.filas:
        ce = ve = 0.0
        falta = False
        for st in 'ABCD':
            for qi in range(4):
                if val[st][qi] is None:
                    continue
                key = f'comidaA_q{qi+1}' if st == 'A' else (f'venenoB_q{qi+1}' if st == 'B' else None)
                if key is None:
                    # C/D: solo tenemos el total en el CSV; usamos crudo si esta
                    falta = True
                    continue
                m = f.get(key)
                if m is None:
                    falta = True
                    continue
                if val[st][qi] == 'comida':
                    ce += m
                else:
                    ve += m
        # C/D desde el crudo del JSON si lo hay
        if c.crudos:
            cr = next((x for x in c.crudos if x['seed'] == f['seed']), None)
            if cr:
                for st in 'CD':
                    for qi in range(4):
                        if val[st][qi] is None:
                            continue
                        m = cr['mord'][st][qi]
                        if val[st][qi] == 'comida':
                            ce += m
                        else:
                            ve += m
                falta = False
        com_ef.append(ce)
        ven_ef.append(ve)
    print(linea('comida_efectiva (todo)', resumen(com_ef), 1))
    print(linea('veneno_efectivo (todo)', resumen(ven_ef), 1))
    if not c.crudos:
        print('  NOTA: sin JSON crudo, comida/veneno efectivos ignoran C y D por cuarto.')

    # --- 5 energia ---
    bloque('5. ENERGIA  (magnitud DERIVADA, no medida: run() no devuelve E)')
    costo = kw.get('costo', 0.002)
    en = c.col('energia_neta')
    if all(v is not None and v != '' for v in en):
        e = [float(v) for v in en]
    else:
        e = [ce * E_VAL['comida'] + ve * E_VAL['veneno'] - costo * T
             for ce, ve in zip(com_ef, ven_ef)]
    print(linea('energia_neta (unid. E)', resumen(e), 2))
    print(linea('energia por 1000 pasos', resumen([x * 1000.0 / T for x in e]), 3))
    print(f'  formula: sum(mordidas*dE) - costo*T   dE: comida +0.8, veneno -0.4   costo={costo}')

    # --- 6 tasa de aprendizaje ---
    bloque('6. TASA DE APRENDIZAJE (tasa de mordida POR VISITA, %; unidad adoptada tras 2H)')
    for q in (1, 2, 3, 4):
        print(linea(f'tasaA_q{q} (%)', resumen(c.col(f'tasaA_q{q}')), 2))
    for q in (1, 2, 3, 4):
        print(linea(f'tasaB_q{q} (%)', resumen(c.col(f'tasaB_q{q}')), 2))
    disc = [(a / b if b else float('inf'))
            for a, b in zip(c.col('tasaA_q4'), c.col('tasaB_q4'))
            if a is not None and b is not None]
    disc_f = [d for d in disc if math.isfinite(d)]
    print(linea('discriminacion tasaA/tasaB Q4', resumen(disc_f), 1, 30))
    if len(disc_f) != len(disc):
        print(f'  ({len(disc)-len(disc_f)} semillas con tasaB_q4=0 -> discriminacion infinita, excluidas del resumen)')
    red = [(a / b if b else float('inf'))
           for a, b in zip(c.col('venenoB_q1'), c.col('venenoB_q4'))
           if a is not None and b is not None]
    red_f = [d for d in red if math.isfinite(d)]
    print(linea('ratio veneno Q1/Q4', resumen(red_f), 2, 30))

    # --- 7 velocidad ---
    bloque('7. VELOCIDAD DE APRENDIZAJE (pasos hasta |W - asintota| < 0.1 sostenido)')
    logs = {x['seed']: x.get('log') or [] for x in c.crudos} if c.crudos else {}
    hay_log = any(logs.values())
    if not hay_log:
        print('  no medible (sin log). Repetir la corrida con --param log_cada=500')
        print(f'  (log_cada no consume RNG: la trayectoria no cambia)')
    else:
        for st in ('A', 'B'):
            vs = [velocidad(logs.get(f['seed'], []), st) for f in c.filas]
            ok = [v for v in vs if v is not None]
            print(linea(f'pasos hasta W_{st} estable', resumen(ok), 0, 30))
            if len(ok) != len(vs):
                print(f'  ({len(vs)-len(ok)} semillas sin convergencia sostenida para W_{st})')
        for st in ('A', 'B'):
            vs = [t_fraccion(logs.get(f['seed'], []), st) for f in c.filas]
            ok = [v for v in vs if v is not None]
            if ok:
                print(linea(f'  t90 de W_{st} (complement.)', resumen(ok), 0, 30))
        inv = kw.get('invertir_en')
        if inv:
            for st in ('A', 'B'):
                vs = [velocidad(logs.get(f['seed'], []), st, t_min=inv) for f in c.filas]
                ok = [v - inv for v in vs if v is not None]
                print(linea(f'pasos tras inversion, W_{st}', resumen(ok), 0, 30))
            for st in ('A', 'B'):
                vs = [t_fraccion(logs.get(f['seed'], []), st, t_min=inv) for f in c.filas]
                ok = [v - inv for v in vs if v is not None]
                if ok:
                    print(linea(f'  t90 tras inversion, W_{st}', resumen(ok), 0, 30))
            print('  (la banda 0.1 sostenida esta limitada por EXPOSICION -lo temido se '
                  're-muestrea poco-;\n   t90 = pasos hasta recorrer el 90% del cambio total, '
                  'mas cercano a la tasa de aprendizaje)')
        res = int(kw.get('log_cada') or 0)
        if res:
            print(f'  resolucion del log: {res} pasos (la cifra no puede ser mas fina que esto)')

    # --- 8 recuperacion ---
    bloque('8. RECUPERACION (tasa por visita del nutritivo vigente en Q4 / del nutritivo en Q2)')
    st_q2 = nutritivo_en(val, 1)
    st_q4 = nutritivo_en(val, 3)
    print(f'  nutritivo en Q2: {st_q2}    nutritivo en Q4: {st_q4}')
    if st_q2 in ('A', 'B') and st_q4 in ('A', 'B'):
        recs, abso = [], []
        for f in c.filas:
            a = f.get(f'tasa{st_q4}_q4')
            b = f.get(f'tasa{st_q2}_q2')
            if a is not None and b:
                recs.append(a / b)
            m = f.get('comidaA_q4') if st_q4 == 'A' else f.get('venenoB_q4')
            if m is not None:
                abso.append(m)
        print(linea('recuperacion (1.0=completa)', resumen(recs), 3, 30))
        print(linea(f'mordidas de {st_q4} en Q4', resumen(abso), 1, 30))
        if kw.get('invertir_en') is None:
            print('  (sin perturbacion: es un control, se espera ~1.0)')
    else:
        print('  no aplicable con estos estimulos (nutritivo fuera de A/B)')

    # --- 9 variabilidad ---
    bloque('9. VARIABILIDAD entre semillas  [DEFINICION PROPUESTA, nueva]')
    for k, v in variabilidad(c).items():
        print(f'  {k:<16} {v:.4f}' if math.isfinite(v) else f'  {k:<16} n/d (media ~0)')
    print('  CV = sd/|media| entre semillas. sd(W) en unidades de W (no CV: W vive cerca de 0/-3).')

    # --- 10 diversidad ---
    bloque('10. DIVERSIDAD entre organismos  [DEFINICION PROPUESTA, nueva]')
    dv = diversidad(c)
    if 'error' in dv:
        print(f'  {dv["error"]}')
    else:
        print(f'  vector: {DIMS_CONDUCTA}')
        print(f'  dimensiones usadas: {dv["d"]} -> {dv["usadas"]}')
        if dv['descartadas']:
            print(f'  descartadas: {dv["descartadas"]}')
        print(f'  distancia euclidea por pares ({dv["pares"]} pares, z-score entre semillas):')
        print(f'    mediana {dv["mediana"]:.3f}   rango [{dv["min"]:.3f} .. {dv["max"]:.3f}]   '
              f'p25-p75 [{dv["p25"]:.3f} .. {dv["p75"]:.3f}]   media {dv["media"]:.3f}')
        print(f'    media por dimension: {dv["media_por_dim"]:.3f}  '
              f'(referencia para dims independientes: {dv["esperado_por_dim_indep"]:.3f})')
    print('  Mide FORMA de la nube (z-score interno), no escala absoluta. Leer junto al punto 9.')

    # --- v7c ---
    if any('splits' in f for f in c.filas):
        bloque('EXTRA v7c: plasticidad estructural')
        print(linea('splits (divisiones)', resumen(c.col('splits')), 1))
        print(linea('celdas activas', resumen(c.col('celdas')), 1))
    print()


# ----------------------------------------------------------------------------
# comparaciones
# ----------------------------------------------------------------------------
METRICAS_COMP = ['comidaA', 'venenoB', 'venenoB_q1', 'venenoB_q4', 'tasaA_q4', 'tasaB_q4',
                 'muertes', 'W_A', 'W_B', 'W_C', 'W_D']


def med(c, k):
    s = resumen(c.col(k))
    return s['mediana'] if s else None


def compara(a, b):
    print('=' * 92)
    print(f'COMPARACION  A = {a.nombre}  (n={a.n})   vs   B = {b.nombre}  (n={b.n})')
    print('=' * 92)
    print(f'  {"metrica":<14}{"medianaA":>12}{"medianaB":>12}{"B-A":>12}')
    for k in METRICAS_COMP:
        ma, mb = med(a, k), med(b, k)
        if ma is None or mb is None:
            continue
        print(f'  {k:<14}{ma:>12.2f}{mb:>12.2f}{mb-ma:>+12.2f}')
    vA = [a.T / max(m, 1) for m in a.col('muertes') if m is not None]
    vB = [b.T / max(m, 1) for m in b.col('muertes') if m is not None]
    sa, sb = resumen(vA), resumen(vB)
    if sa and sb:
        print(f'  {"vida":<14}{sa["mediana"]:>12.2f}{sb["mediana"]:>12.2f}{sb["mediana"]-sa["mediana"]:>+12.2f}')
    for c in (a, b):
        cc = cuenta_criterios(c)
        if cc:
            det = '  '.join(f'{k}:{v}/{c.n}' for k, v in cc.items() if v is not None)
            print(f'  criterios {c.nombre} [{c.etapa}]: {det}')
        else:
            print(f'  criterios {c.nombre}: no hay criterios preregistrados para etapa {c.etapa}')
    print()


def compara_baseline(c):
    if not os.path.exists(BASELINE):
        print(f'ERROR: no existe {BASELINE}', file=sys.stderr)
        return
    print('=' * 92)
    print(f'COMPARACION CONTRA BASELINE  {BASELINE}')
    print('=' * 92)
    for cond in ('A_sin', 'B_aprende'):
        filas = carga_csv(BASELINE, cond=cond)
        bl = Corrida(f'baseline_v6[{cond}]', filas, cond=cond)
        idx = 0 if cond == 'A_sin' else 1
        print(f'\n  --- contra cond={cond} (n={bl.n}) ---')
        print(f'  {"metrica":<14}{"corrida":>12}{"baseline":>12}{"dif":>12}{"registro":>12}')
        for k in ['comidaA', 'venenoB', 'venenoB_q1', 'venenoB_q4', 'tasaA_q4', 'tasaB_q4',
                  'muertes', 'W_A', 'W_B']:
            mc, mb = med(c, k), med(bl, k)
            if mc is None or mb is None:
                continue
            ref = REF_BASELINE.get(k)
            refv = f'{ref[idx]:>12.2f}' if ref else ' ' * 12
            print(f'  {k:<14}{mc:>12.2f}{mb:>12.2f}{mc-mb:>+12.2f}{refv}')
    print('\n  Medianas de referencia del registro (A_sin/B_aprende): '
          'comida 1400/338, venenoQ4 370/13, muertes 218/142, W_A 0/+1.00, W_B 0/-3.00')
    # coincidencia exacta fila a fila con B_aprende, si las semillas se solapan
    filas = carga_csv(BASELINE, cond='B_aprende')
    bl = {f['seed']: f for f in filas}
    comunes = [f for f in c.filas if f.get('seed') in bl]
    if comunes:
        claves = ['comidaA', 'venenoB', 'venenoB_q1', 'venenoB_q4', 'tasaB_q4', 'tasaA_q4',
                  'muertes', 'W_A', 'W_B', 'WpA', 'WnA', 'WpB', 'WnB']
        malas = []
        for f in comunes:
            b = bl[f['seed']]
            for k in claves:
                if k in f and k in b and float(f[k]) != float(b[k]):
                    malas.append((f['seed'], k, f[k], b[k]))
        print(f'\n  Coincidencia EXACTA fila a fila con cond=B_aprende sobre {len(comunes)} semillas comunes:')
        if not malas:
            print(f'    IDENTICO en {len(claves)} columnas x {len(comunes)} semillas.')
        else:
            print(f'    {len(malas)} discrepancias (semilla, columna, corrida, baseline):')
            for x in malas[:40]:
                print(f'      {x}')
    print()


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description='Resume corridas de datos/. Siempre mediana, rango y cuartiles (regla 6).')
    ap.add_argument('archivos', nargs='*', help='rutas de CSV/JSON en datos/')
    ap.add_argument('--etapa', default=None, help='toma el archivo mas reciente de esa etapa en datos/')
    ap.add_argument('--cond', default=None, help='filtra por columna cond (para CSV tipo baseline)')
    ap.add_argument('--vs', default=None, help='compara la primera corrida contra este archivo')
    ap.add_argument('--baseline', action='store_true', help='compara contra datos/baseline_v6.csv')
    args = ap.parse_args()

    rutas = list(args.archivos)
    if args.etapa:
        rutas.insert(0, mas_reciente(args.etapa))
    if not rutas:
        ap.error('da al menos un archivo o --etapa')

    corridas = [carga(r, cond=args.cond) for r in rutas]
    for c in corridas:
        informe(c)
    if args.vs:
        compara(corridas[0], carga(args.vs))
    if args.baseline:
        compara_baseline(corridas[0])
    return 0


if __name__ == '__main__':
    sys.exit(main())
