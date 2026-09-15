#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_etapa.py -- Fase 1 del PLAN: corredor de escenarios en paralelo.

Corre un escenario con nombre sobre N semillas (1..N), una semilla por proceso,
y escribe DOS archivos nuevos en datos/:
    datos/<prefijo>_<organismo>_<YYYYMMDD_HHMMSS>.csv
    datos/<prefijo>_<organismo>_<YYYYMMDD_HHMMSS>.json
Nunca sobrescribe. Si el archivo existe, aborta.

No modifica NADA dentro de organismo/. Solo importa el modulo congelado y llama a run().

ESCENARIOS (replican EXACTAMENTE los de organismo/bateria.py)
    E1    run(s)
    E2    run(s, invertir_en=50000)
    E2I   run(s, nuevo='C')
    E2J   run(s, nuevo='D', nuevo_val='comida', solap_B=1)
    E2K   run(s, nuevo='D', nuevo_val='comida', solap_B=2)
    CTRL  run(s, learn=False)
    LIBRE run(s, **lo que llegue por --param)

DETERMINISMO
    organismo_v6.run / organismo_v7c.run construyen su propio rng
    (np.random.default_rng(seed)) y no tocan estado global. Por tanto el
    resultado de una semilla es identico en serie y en paralelo. Esto se
    verifica con --verificar-equivalencia.

NOTA sobre log_cada
    log_cada NO consume numeros aleatorios (solo agrega tuplas a una lista),
    de modo que activarlo no altera la trayectoria. Es seguro pasar
    --param log_cada=500 para poder medir velocidad de aprendizaje en analiza.py.
    Aun asi, los escenarios preregistrados se definen SIN log; activarlo queda
    registrado en la cabecera de procedencia del JSON.

REGLA 7 DEL PROYECTO
    Este script NO escribe en registro/ (prohibido en esta tarea). Al terminar
    imprime la linea lista para pegar en registro/, con los hashes cortos.

Uso:
    python experimentos/run_etapa.py --etapa E1 --semillas 20
    python experimentos/run_etapa.py --etapa E2K --semillas 20 --organismo v7c
    python experimentos/run_etapa.py --etapa LIBRE --salida 2kbis_solap3 \
           --param nuevo=D --param nuevo_val=comida --param solap_B=3
"""
import argparse
import csv
import datetime as _dt
import hashlib
import importlib
import json
import multiprocessing as mp
import os
import platform
import sys
import time

# --- consola Windows cp1252: fuerza utf-8 y no revienta con caracteres raros ---
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DIR_ORG = os.path.join(RAIZ, 'organismo')
DIR_DATOS = os.path.join(RAIZ, 'datos')
if DIR_ORG not in sys.path:
    sys.path.insert(0, DIR_ORG)

MODULOS = {'v6': 'organismo_v6', 'v7c': 'organismo_v7c'}

# Escenarios con nombre. Copiados literalmente de organismo/bateria.py.
ESCENARIOS = {
    'E1':   {},
    'E2':   {'invertir_en': 50000},
    'E2I':  {'nuevo': 'C'},
    'E2J':  {'nuevo': 'D', 'nuevo_val': 'comida', 'solap_B': 1},
    'E2K':  {'nuevo': 'D', 'nuevo_val': 'comida', 'solap_B': 2},
    'CTRL': {'learn': False},
    'LIBRE': {},
}

# Constantes energeticas del organismo (v6 y v7c son identicas en esto).
E_VAL = {'comida': +0.8, 'veneno': -0.4}


# ----------------------------------------------------------------------------
# utilidades
# ----------------------------------------------------------------------------
def sha16(ruta):
    """sha256 corto (16 hex) de un archivo, la convencion de hash del proyecto."""
    with open(ruta, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def coerce(texto):
    """Convierte 'clave=valor' de la CLI al tipo Python que espera run()."""
    t = texto.strip()
    bajo = t.lower()
    if bajo in ('true', 'si', 'yes'):
        return True
    if bajo in ('false', 'no'):
        return False
    if bajo in ('none', 'null', 'nada', ''):
        return None
    try:
        return int(t)
    except ValueError:
        pass
    try:
        return float(t)
    except ValueError:
        pass
    return t


def valencias_por_cuarto(kwargs, T):
    """Valencia ('comida'/'veneno'/None) de cada estimulo en cada cuarto.

    El organismo usa q(t)=min(t//(T//4),3); el cuarto qi empieza en qi*(T//4).
    Se atribuye la valencia vigente al COMIENZO del cuarto. Con los valores por
    defecto (T=100000, invertir_en=50000, nuevo_en=50000) el cambio cae justo en
    el borde del cuarto 3, asi que la atribucion es exacta. Si se usan valores
    que no caen en borde de cuarto, es una aproximacion (se avisa en el JSON).
    """
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


def borde_exacto(kwargs, T):
    """True si los cambios de mundo caen en un borde de cuarto (atribucion exacta)."""
    qlen = max(T // 4, 1)
    for clave in ('invertir_en', 'nuevo_en'):
        v = kwargs.get(clave, None)
        if clave == 'nuevo_en' and kwargs.get('nuevo') is None:
            continue
        if clave == 'nuevo_en' and v is None:
            v = 50000
        if v is not None and v % qlen != 0:
            return False
    return True


def energia_neta(r, kwargs, T):
    """Balance energetico neto estimado de la corrida.

    run() no devuelve la energia E, asi que se reconstruye del presupuesto:
        sum(mordidas * dE(valencia vigente en ese cuarto)) - costo*T
    dE: comida +0.8, veneno -0.4; costo por paso 0.002 (o el que se pase).
    Es una magnitud DERIVADA, no medida: se documenta como tal.
    """
    val = valencias_por_cuarto(kwargs, T)
    costo = kwargs.get('costo', 0.002)
    tot = 0.0
    for st, fila in val.items():
        if st not in r['mord']:
            continue
        for qi in range(4):
            v = fila[qi]
            if v in E_VAL:
                tot += r['mord'][st][qi] * E_VAL[v]
    return tot - costo * T


# ----------------------------------------------------------------------------
# worker: se ejecuta en el proceso hijo (start method = spawn en Windows)
# ----------------------------------------------------------------------------
_MOD = None


def _worker(tarea):
    """Corre UNA semilla. Importa el modulo del organismo dentro del hijo."""
    global _MOD
    seed, nombre_modulo, kwargs = tarea
    if _MOD is None or _MOD.__name__ != nombre_modulo:
        _MOD = importlib.import_module(nombre_modulo)
    t0 = time.perf_counter()
    r = _MOD.run(seed, **kwargs)
    return seed, r, time.perf_counter() - t0


# ----------------------------------------------------------------------------
# aplanado a fila de CSV
# ----------------------------------------------------------------------------
def tasa(r, k, i):
    """Tasa de mordida por visita, en % (la definicion de bateria.py)."""
    return round(100.0 * r['mord'][k][i] / max(r['vis'][k][i], 1), 2)


COLS_SPEC = (
    ['seed', 'comidaA', 'venenoB'] +
    [f'venenoB_q{i}' for i in (1, 2, 3, 4)] +
    [f'tasaA_q{i}' for i in (1, 2, 3, 4)] +
    [f'tasaB_q{i}' for i in (1, 2, 3, 4)] +
    ['visitasA', 'visitasB', 'muertes',
     'W_A', 'W_B', 'W_C', 'W_D', 'WpA', 'WnA', 'WpB', 'WnB']
)
COLS_EXTRA = (
    [f'comidaA_q{i}' for i in (1, 2, 3, 4)] +
    [f'visitasA_q{i}' for i in (1, 2, 3, 4)] +
    [f'visitasB_q{i}' for i in (1, 2, 3, 4)] +
    ['mordC', 'mordD', 'visitasC', 'visitasD',
     'WpC', 'WnC', 'WpD', 'WnD',
     'solap_AB', 'solap_nB', 'T', 'vida_media', 'energia_neta']
)
COLS_V7 = ['splits', 'celdas']


def fila_csv(seed, r, kwargs, T, es_v7):
    f = {'seed': seed}
    f['comidaA'] = sum(r['mord']['A'])
    f['venenoB'] = sum(r['mord']['B'])
    for i in range(4):
        f[f'venenoB_q{i+1}'] = r['mord']['B'][i]
        f[f'comidaA_q{i+1}'] = r['mord']['A'][i]
        f[f'tasaA_q{i+1}'] = tasa(r, 'A', i)
        f[f'tasaB_q{i+1}'] = tasa(r, 'B', i)
        f[f'visitasA_q{i+1}'] = r['vis']['A'][i]
        f[f'visitasB_q{i+1}'] = r['vis']['B'][i]
    f['visitasA'] = sum(r['vis']['A'])
    f['visitasB'] = sum(r['vis']['B'])
    f['muertes'] = r['deaths']
    for k in 'ABCD':
        f[f'W_{k}'] = r['W'][k]
    f['WpA'], f['WnA'] = r['comp']['A']
    f['WpB'], f['WnB'] = r['comp']['B']
    f['WpC'], f['WnC'] = r['comp']['C']
    f['WpD'], f['WnD'] = r['comp']['D']
    f['mordC'] = sum(r['mord']['C'])
    f['mordD'] = sum(r['mord']['D'])
    f['visitasC'] = sum(r['vis']['C'])
    f['visitasD'] = sum(r['vis']['D'])
    f['solap_AB'] = r['solap']['AB']
    f['solap_nB'] = r['solap']['nB'] if r['solap']['nB'] is not None else ''
    f['T'] = T
    f['vida_media'] = round(T / max(r['deaths'], 1), 1)
    f['energia_neta'] = round(energia_neta(r, kwargs, T), 3)
    if es_v7:
        f['splits'] = r.get('splits', 0)
        f['celdas'] = r.get('celdas', 0)
    return f


# ----------------------------------------------------------------------------
# verificacion de equivalencia paralelo == secuencial
# ----------------------------------------------------------------------------
def verificar_equivalencia(nombre_modulo, kwargs, seeds, resultados_par):
    mod = importlib.import_module(nombre_modulo)
    dif = []
    for s in seeds:
        seq = mod.run(s, **kwargs)
        par = resultados_par[s]
        if json.dumps(seq, sort_keys=True, default=str) != json.dumps(par, sort_keys=True, default=str):
            dif.append(s)
    return dif


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description='Corre un escenario del organismo en paralelo y guarda CSV+JSON en datos/.')
    ap.add_argument('--etapa', required=True,
                    help='Nombre del escenario: ' + ', '.join(ESCENARIOS))
    ap.add_argument('--semillas', type=int, default=20, help='N; se usan las semillas 1..N (default 20)')
    ap.add_argument('--organismo', choices=sorted(MODULOS), default='v6')
    ap.add_argument('--param', action='append', default=[], metavar='CLAVE=VALOR',
                    help='kwarg extra para run(); repetible')
    ap.add_argument('--T', type=int, default=100000, help='pasos por corrida (default 100000)')
    ap.add_argument('--salida', default=None,
                    help='prefijo del nombre de archivo (default: el nombre de la etapa)')
    ap.add_argument('--procesos', type=int, default=None,
                    help='procesos del Pool (default min(16, os.cpu_count()))')
    ap.add_argument('--dir-salida', default=DIR_DATOS, help='directorio de salida (default datos/)')
    ap.add_argument('--verificar-equivalencia', action='store_true',
                    help='rehace las mismas semillas en serie y comprueba igualdad bit a bit del resultado')
    ap.add_argument('--dry-run', action='store_true', help='muestra el escenario resuelto y sale')
    args = ap.parse_args()

    if args.etapa not in ESCENARIOS:
        ap.error(f'etapa desconocida: {args.etapa!r}. Conocidas: {", ".join(ESCENARIOS)}')
    if args.semillas < 1:
        ap.error('--semillas debe ser >= 1')

    nombre_modulo = MODULOS[args.organismo]
    archivo_org = os.path.join(DIR_ORG, nombre_modulo + '.py')
    if not os.path.isfile(archivo_org):
        ap.error(f'no existe {archivo_org}')

    # --- resolver kwargs ---
    kwargs = dict(ESCENARIOS[args.etapa])
    base_escenario = dict(kwargs)
    overrides = {}
    for p in args.param:
        if '=' not in p:
            ap.error(f'--param mal formado: {p!r} (se espera clave=valor)')
        k, _, v = p.partition('=')
        k = k.strip()
        if k in kwargs:
            overrides[k] = (kwargs[k], coerce(v))
        kwargs[k] = coerce(v)
    kwargs['T'] = args.T

    seeds = list(range(1, args.semillas + 1))
    nproc = args.procesos if args.procesos else min(16, os.cpu_count() or 1)
    nproc = max(1, min(nproc, len(seeds)))
    prefijo = args.salida if args.salida else args.etapa

    print('=' * 72)
    print(f'run_etapa  etapa={args.etapa}  organismo={args.organismo}  semillas=1..{args.semillas}')
    print(f'kwargs de run(): {kwargs}')
    if overrides:
        print('AVISO: --param sobrescribe claves del escenario preregistrado:')
        for k, (viejo, nuevo) in overrides.items():
            print(f'   {k}: {viejo!r} -> {nuevo!r}   (ya NO es {args.etapa} tal como esta en bateria.py)')
    if 'log_cada' in kwargs and kwargs['log_cada']:
        print(f'AVISO: log_cada={kwargs["log_cada"]} activo. No consume RNG, no altera la trayectoria,')
        print('       pero el escenario deja de ser literalmente el de bateria.py (que corre sin log).')
    print(f'procesos={nproc} (cpu_count={os.cpu_count()})  T={args.T}')
    print('=' * 72)
    if args.dry_run:
        return 0

    # --- nombres de salida, sin sobrescribir jamas ---
    os.makedirs(args.dir_salida, exist_ok=True)
    sello = _dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    base = f'{prefijo}_{args.organismo}_{sello}'
    ruta_csv = os.path.join(args.dir_salida, base + '.csv')
    ruta_json = os.path.join(args.dir_salida, base + '.json')
    for r in (ruta_csv, ruta_json):
        if os.path.exists(r):
            print(f'ERROR: el archivo ya existe y NO se sobrescribe: {r}', file=sys.stderr)
            return 2

    # --- correr en paralelo, una semilla por proceso ---
    t_ini = time.perf_counter()
    tareas = [(s, nombre_modulo, kwargs) for s in seeds]
    resultados = {}
    tiempos = {}
    ctx = mp.get_context('spawn')          # CRITICO en Windows
    with ctx.Pool(processes=nproc) as pool:
        hechas = 0
        for seed, r, dt in pool.imap_unordered(_worker, tareas, chunksize=1):
            resultados[seed] = r
            tiempos[seed] = dt
            hechas += 1
            print(f'  [{hechas:3d}/{len(seeds)}] semilla {seed:3d}  {dt:6.2f}s  '
                  f'muertes={r["deaths"]:4d}  W_A={r["W"]["A"]:+.2f}  W_B={r["W"]["B"]:+.2f}')
    t_par = time.perf_counter() - t_ini
    t_cpu = sum(tiempos.values())

    # --- verificacion opcional de equivalencia ---
    dif_equiv = None
    t_seq = None
    if args.verificar_equivalencia:
        print('-' * 72)
        print('Verificando equivalencia paralelo == secuencial ...')
        t0 = time.perf_counter()
        dif_equiv = verificar_equivalencia(nombre_modulo, kwargs, seeds, resultados)
        t_seq = time.perf_counter() - t0
        if dif_equiv:
            print(f'FALLA equivalencia en las semillas: {dif_equiv}')
        else:
            print(f'OK equivalencia: {len(seeds)}/{len(seeds)} semillas identicas '
                  f'(secuencial {t_seq:.2f}s vs paralelo {t_par:.2f}s)')

    es_v7 = (args.organismo == 'v7c')
    cols = COLS_SPEC + COLS_EXTRA + (COLS_V7 if es_v7 else [])
    filas = [fila_csv(s, resultados[s], kwargs, args.T, es_v7) for s in seeds]

    with open(ruta_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for fl in filas:
            w.writerow(fl)

    # --- JSON con cabecera de PROCEDENCIA (regla 7) ---
    hash_script = sha16(os.path.abspath(__file__))
    hash_org = sha16(archivo_org)
    crudos = []
    for s in seeds:
        r = resultados[s]
        d = {'seed': s,
             'mord': r['mord'], 'vis': r['vis'], 'W': r['W'],
             'comp': {k: list(v) for k, v in r['comp'].items()},
             'deaths': r['deaths'], 'solap': r['solap'],
             'log': r.get('log', []),
             'segundos': round(tiempos[s], 3)}
        if es_v7:
            d['splits'] = r.get('splits', 0)
            d['celdas'] = r.get('celdas', 0)
        crudos.append(d)

    doc = {
        'procedencia': {
            'fecha_iso': _dt.datetime.now().astimezone().isoformat(timespec='seconds'),
            'etapa': args.etapa,
            'prefijo_salida': prefijo,
            'escenario': {
                'nombre': args.etapa,
                'kwargs_escenario_base': base_escenario,
                'kwargs_completos_de_run': kwargs,
                'kwargs_sobrescritos_por_param': {k: {'escenario': v[0], 'usado': v[1]}
                                                  for k, v in overrides.items()},
                'llamada': f'{nombre_modulo}.run(seed, ' +
                           ', '.join(f'{k}={v!r}' for k, v in kwargs.items()) + ')',
            },
            'n_semillas': len(seeds),
            'semillas': seeds,
            'organismo': {
                'alias': args.organismo,
                'modulo': nombre_modulo,
                'archivo': archivo_org,
                'sha256_16': hash_org,
            },
            'script': {
                'archivo': os.path.abspath(__file__),
                'sha256_16': hash_script,
            },
            'entorno': {
                'python': platform.python_version(),
                'python_full': sys.version.replace('\n', ' '),
                'numpy': __import__('numpy').__version__,
                'plataforma': platform.platform(),
                'cpu_count': os.cpu_count(),
                'procesos_usados': nproc,
                'metodo_arranque_mp': 'spawn',
            },
            'tiempos': {
                'segundos_pared_paralelo': round(t_par, 3),
                'segundos_cpu_sumados': round(t_cpu, 3),
                'aceleracion_observada': round(t_cpu / t_par, 2) if t_par > 0 else None,
                'segundos_secuencial_verificacion': round(t_seq, 3) if t_seq else None,
            },
            'equivalencia_paralelo_vs_secuencial': (
                'no verificada' if dif_equiv is None
                else ('IDENTICA' if not dif_equiv else f'DIFIERE en semillas {dif_equiv}')),
            'notas': {
                'T': args.T,
                'atribucion_valencia_por_cuarto_exacta': borde_exacto(kwargs, args.T),
                'energia_neta': ('magnitud DERIVADA: sum(mordidas*dE) - costo*T, '
                                 'con dE comida=+0.8, veneno=-0.4. run() no devuelve E.'),
                'log_cada': kwargs.get('log_cada', None),
                'determinismo': ('run() usa np.random.default_rng(seed) y ningun estado global; '
                                 'el paralelismo no altera resultados.'),
            },
        },
        'resultados': crudos,
    }
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)

    hash_csv = sha16(ruta_csv)
    hash_json = sha16(ruta_json)
    print('-' * 72)
    print(f'CSV : {ruta_csv}   sha256_16={hash_csv}')
    print(f'JSON: {ruta_json}   sha256_16={hash_json}')
    print(f'organismo {nombre_modulo}.py  sha256_16={hash_org}')
    print(f'run_etapa.py              sha256_16={hash_script}')
    acel = (t_cpu / t_par) if t_par > 0 else float('nan')
    print(f'Tiempo total (pared): {t_par:.2f}s   CPU sumado: {t_cpu:.2f}s   aceleracion: {acel:.2f}x')
    print('-' * 72)
    print('Linea para registro/ (regla 7; este script NO escribe en registro/):')
    print(f'  {args.etapa} {args.organismo} n={len(seeds)} T={args.T} '
          f'-> {os.path.basename(ruta_csv)} / {os.path.basename(ruta_json)} '
          f'| organismo {hash_org} | run_etapa.py {hash_script} | csv {hash_csv} | json {hash_json}')
    if dif_equiv:
        return 3
    return 0


if __name__ == '__main__':
    mp.freeze_support()
    sys.exit(main())
