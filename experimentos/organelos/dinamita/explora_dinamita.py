"""explora_dinamita.py — EXPLORATORIO del bloque DINAMITA: UNA corrida (seed, brazo, T) por proceso, sin Pool. Escribe su JSON antes de
volver (ERR-54). Nada de aqui es confirmatorio. Semillas EXPLORATORIAS 39201-39230 (T 100 000); practica 39921-39924 (arnes/humo).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

ENTRADA (regla 14): la corrida ES experimentos/tronco_v14_3/corre_v143.tarea importada (juez.tarea con fundador limpio + resumen_linaje),
igual que corre_termo.tarea; los carros se registran en corre_v143._MODS en memoria. Telemetria de solo lectura: d['carro']['termo'] y
d['carro']['veto'] (ultima instancia de cada linaje).

BRAZOS:  termo  V143_TERMO (termo/carros; la BASE de este bloque)       o1  O1 (techo, ancla)      v143  V143 (solo si se pide)
         vu  TVETO VETO 1 · vh  VETO 2 · vnav  VETO 3 · vuinv  VETO 4 (CONTROL de vu) · vw  VETO 5
         ola 2: lu  VETO 6 (LIMPIA_U) · luinv  VETO 7 (CONTROL de lu) · lh  VETO 8 (LIMPIA_H)
         ola 3 (TPATAS): pd  PATAS 1 (DIRECTO) · pu  PATAS 2 (UTIL) · pc  PATAS 3 (UTIL+CEDE) · pi  PATAS 4 (INUTIL, CONTROL de pu)

    python experimentos/organelos/dinamita/explora_dinamita.py --seed 39201 --brazo vu [--T 100000]
"""
import argparse, importlib.util, json, os, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
TERMOC = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo', 'carros')
for _d in (AQUI, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_v143 as CV
P = CV.P

DATOS = os.path.join(AQUI, 'datos', 'explora')
VETOS = {'vu': 1, 'vh': 2, 'vnav': 3, 'vuinv': 4, 'vw': 5, 'lu': 6, 'luinv': 7, 'lh': 8}
PATASB = {'pd': 1, 'pu': 2, 'pc': 3, 'pi': 4}
BRAZOS = dict(termo='V143_TERMO', o1='O1', v143='V143', **{b: f'TVETO_{v}' for b, v in VETOS.items()},
              **{b: f'TPATAS_{v}' for b, v in PATASB.items()})
EXPLORA = range(39201, 39231); PRACTICA = range(39921, 39925)


def registra(brazo):
    n = BRAZOS[brazo]
    if n in CV._MODS or n in ('O1', 'V143'): return n
    if n == 'V143_TERMO': ruta = os.path.join(TERMOC, 'V143_TERMO.py')
    elif n.startswith('TPATAS_'): ruta = os.path.join(AQUI, 'carros', 'TPATAS.py')
    else: ruta = os.path.join(AQUI, 'carros', 'TVETO.py')
    spec = importlib.util.spec_from_file_location(f"carro_{n}", ruta)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    if n.startswith('TVETO_'): m.VETO = int(n.split('_')[1])
    if n.startswith('TPATAS_'): m.PATAS = int(n.split('_')[1])
    CV._MODS[n] = m
    return n


def tarea(seed, brazo, T):
    n = registra(brazo)
    cap = []; orig = P.run

    def run2(*a, **k):
        r = orig(*a, **k)
        cap.append([dict(termo=(d.get('carro') or {}).get('termo'), veto=(d.get('carro') or {}).get('veto'),
                         patas=(d.get('carro') or {}).get('patas')) for d in r['linajes']])
        return r
    P.run = run2
    try:
        x = CV.tarea((seed, n, T))
    finally:
        P.run = orig
    x['tel_dinamita'] = cap[0] if cap else None
    x.pop('pizarra_log', None); x['brazo'] = brazo; x['T'] = T
    return x


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--brazo', required=True, choices=list(BRAZOS))
    ap.add_argument('--T', type=int, default=100000)
    a = ap.parse_args(argv)
    if not (a.seed in EXPLORA or a.seed in PRACTICA): raise SystemExit("solo semillas exploratorias 39201-39230 o practica 39921-39924")
    carpeta = DATOS if a.seed in EXPLORA else os.path.join(AQUI, 'datos', 'practica')
    if a.seed in EXPLORA and a.T != 100000: raise SystemExit("exploratorio: T = 100000")
    os.makedirs(carpeta, exist_ok=True)
    fin = os.path.join(carpeta, f"{a.brazo}_s{a.seed}_T{a.T}.json")
    t0 = time.time()
    try:
        x = tarea(a.seed, a.brazo, a.T); x['aborto'] = None
    except BaseException as e:   # noqa
        x = dict(seed=a.seed, brazo=a.brazo, T=a.T, aborto=f"{type(e).__name__}: {e}"[:300], linajes=[])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    cz = sum(l['cruza_real'] for l in x['linajes'])
    print(f"{a.brazo} s{a.seed} T{a.T} ({time.time()-t0:.0f}s) cruzan {cz}/9 R0 real {[l['R0_real'] for l in x['linajes']]} aborto {x['aborto']}", flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
