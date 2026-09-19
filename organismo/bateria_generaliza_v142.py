"""bateria_generaliza_v142 = organismo/bateria_generaliza.py (9cf72581ebae7dea, solo se leyo) con UNA entrada nueva en
INSTRUMENTOS: organismo_v142 -> organismo_v142g, con los kwargs CAMPO A CAMPO iguales a los de la entrada
del tronco organismo_v14 (regla 14 de EQUIPO.md; eta_s=0.15 y clip_s=10.0 EXPLICITOS porque el instrumento
de mundo de regla los trae apagados por defecto). Umbrales G1/G2/K sin tocar. Vive en organismo/, asi que
los sha del organismo y del instrumento se leen desde organismo/ (ERR-42).
    python bateria_generaliza_v142.py organismo_v142 20 --desde 101 --log      (desde organismo/)
Generada POR ANCLAS por experimentos/creacion_B/construye_v142.py. CONGELADA: NO editar."""
"""REGRESIÓN DE GENERALIZACIÓN (Etapa 3) — obligatoria para cualquier tronco, nuevo o viejo.

Nace de ERR-20: la Etapa 3 se cerró el 16 sep y **no quedó en ninguna batería**, así que v11 la reabrió (acierto de
valor 0.80 -> 0.60) y sólo nos enteramos al re-verificar a mano. Una etapa cerrada que no está en una batería no está
protegida.

    python bateria_generaliza.py <modulo> [semillas] [--desde N] [--log]      (desde organismo/)
      modulo: organismo_v9 | organismo_v10 | organismo_v11 | ... (o la ruta de un candidato)
      por defecto: 10 semillas desde la 41. Para congelar un tronco: 20 semillas.

Mide, con el instrumento de la Etapa 3 (mundo de regla, 20 patrones de peso 3, T=200.000, sonda a priori en T/2):
  G1 [valor]    acierto de signo sobre patrones NUNCA VISTOS con la regla px0: mediana >= 0.65,
                control azar en [0.35, 0.65], y px0 > azar en >= 70% de las semillas.
  G2 [conducta] BA_pb al primer encuentro: mediana px0 >= 0.55, azar en [0.42, 0.58], px0 > azar en >= 70%.
  K  [cobertura] >= 6 de los 10 patrones de test con primer encuentro registrado, en >= 90% de las semillas.
Umbrales: los del preregistro de la Etapa 3 sobre v9 (5a2af284ee73ae76). NO se tocan.
Un tronco que falle G1 o G2 no queda prohibido, pero **no puede declarar la Etapa 3 cerrada**, y el registro debe
llevar la advertencia (es el caso de v11).
"""
import sys, os, time, json, hashlib, importlib, platform
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
GEN = os.path.join(RAIZ, 'experimentos', 'v11_generaliza')
sys.path[:0] = [AQUI, GEN, os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]
REGLAS = ['px0', 'azar']
N_PARALELO = 14
_log = {'f': None, 't0': time.time()}

# Cada tronco necesita su instrumento de mundo de regla (mismas anclas en todos): modulo -> (instrumento, kwargs)
INSTRUMENTOS = {
    'organismo_v9':  ('organismo_v9g',  dict()),
    'organismo_v10': ('organismo_v11g', dict(mu_norm=True, div_signo=False)),
    'organismo_v11': ('organismo_v11g', dict(mu_norm=True, div_signo=True)),
    'organismo_v13': ('organismo_v13g', dict(eta_s=0.015, puerta=3)),   # dos vias: el punto confirmado en 61-80
    'organismo_v13_rapido': ('organismo_v13q_rapido', dict(eta_s=0.015, puerta=3)),   # gemelo compilado del mundo de regla (identidad 81/81+243/243); mismo punto
    'organismo_v14': ('organismo_v14g', dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)),   # TRONCO v14 (18 sep): hija dispersa + puerta por codigo, las DOS ON
    'organismo_v142': ('organismo_v142g', dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)),   # TRONCO v14.2 (18 sep, noche) = v14.1 + B-5: kwargs CAMPO A CAMPO iguales a los de organismo_v14 (regla 14)
}
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura'))
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:6.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def tarea(args):
    modulo, regla, seed = args
    nombre, kw = INSTRUMENTOS[modulo]
    g = importlib.import_module(nombre)
    r = g.run(seed, T=200000, mundo='regla', regla=regla, **kw)
    vr = g.split_regla(seed, regla)[3]
    test = r['test']
    f = [1.0 if r['W_apriori'][k] > 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if r['W_apriori'][k] < 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    pf = [r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'veneno']
    return dict(modulo=modulo, regla=regla, seed=seed,
                acc=0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p)),
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,
                cobertura=sum(v is not None for v in r['primer'].values()),
                splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'])


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    argv = [a for i, a in enumerate(sys.argv[1:], 1) if a not in ('--log', '--desde') and sys.argv[i - 1] != '--desde']
    modulo = argv[0] if argv else 'organismo_v11'
    S = int(argv[1]) if len(argv) > 1 else 10
    desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 41
    seeds = list(range(desde, desde + S))
    if modulo not in INSTRUMENTOS:
        raise SystemExit(f"Sin instrumento de mundo de regla para {modulo}. Añádelo a INSTRUMENTOS (mismas anclas) antes de correr.")
    stamp = time.strftime('%Y%m%d_%H%M%S')
    if '--log' in sys.argv:
        _log['f'] = open(os.path.join(RAIZ, 'datos', f'regresion_generaliza_{modulo}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    inst = INSTRUMENTOS[modulo][0]
    log(f"=== REGRESIÓN DE GENERALIZACIÓN (Etapa 3) — {modulo}, {S} semillas ({seeds[0]}..{seeds[-1]}), Pool({N_PARALELO}) ===")
    _dir = {'organismo_v14g': AQUI, 'organismo_v142g': AQUI, 'organismo_v11g': GEN, 'organismo_v13g': os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),
            'organismo_v13q_rapido': os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura')}.get(inst, os.path.join(RAIZ, 'experimentos', 'etapa3_v9'))
    log(f"instrumento {inst} {h16(os.path.join(_dir, inst + '.py'))}"
        f"  organismo {h16(os.path.join(AQUI, (modulo if modulo != 'organismo_v13_rapido' else 'organismo_v13') + '.py'))}  esta bateria {h16(os.path.abspath(__file__))}")
    trabajos = [(modulo, rg, s) for rg in REGLAS for s in seeds]
    res = []
    with mp.Pool(N_PARALELO) as pool:
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 10 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
    G = lambda rg: {r['seed']: r for r in res if r['regla'] == rg}
    px, az = G('px0'), G('azar')
    mpx = float(np.median([px[s]['acc'] for s in seeds])); maz = float(np.median([az[s]['acc'] for s in seeds]))
    par1 = sum(px[s]['acc'] > az[s]['acc'] for s in seeds)
    bpx = [px[s]['ba'] for s in seeds if px[s]['ba'] is not None]; baz = [az[s]['ba'] for s in seeds if az[s]['ba'] is not None]
    par2 = sum(1 for s in seeds if px[s]['ba'] is not None and az[s]['ba'] is not None and px[s]['ba'] > az[s]['ba'])
    cob = sum(px[s]['cobertura'] >= 6 for s in seeds)
    V = {}
    V['K_cobertura'] = cob >= 0.9 * S
    V['G1_valor'] = mpx >= 0.65 and 0.35 <= maz <= 0.65 and par1 >= 0.7 * S
    V['G2_conducta'] = bool(bpx) and bool(baz) and float(np.median(bpx)) >= 0.55 and 0.42 <= float(np.median(baz)) <= 0.58 and par2 >= 0.7 * S
    log()
    log(f"  {'OK' if V['K_cobertura'] else 'FALLA':5s} K  cobertura del primer encuentro: {cob}/{S}")
    log(f"  {'PASA' if V['G1_valor'] else 'FALLA':5s} G1 valor en patrones nunca vistos: px0 {mpx:.3f} (>=0.65), azar {maz:.3f}, px0>azar {par1}/{S}")
    log(f"  {'PASA' if V['G2_conducta'] else 'FALLA':5s} G2 conducta al primer encuentro: px0 {np.median(bpx):.3f} (>=0.55), azar {np.median(baz):.3f}, px0>azar {par2}/{S}")
    log(f"        divisiones {np.median([px[s]['splits'] for s in seeds]):.0f}  celdas {np.median([px[s]['celdas'] for s in seeds]):.0f}"
        f"  muertes {np.median([px[s]['deaths'] for s in seeds]):.0f}")
    todo = all(V.values())
    log()
    log(f"VEREDICTO bateria_generaliza ({modulo}): " + " ".join(f"{k}={v}" for k, v in V.items()))
    log(f"*** {modulo} {'CONSERVA' if todo else 'NO CONSERVA'} la generalización de la Etapa 3"
        + ("" if todo else ". No puede declararse la Etapa 3 cerrada con este tronco (ERR-20)."))
    if _log['f']:
        dj = os.path.join(RAIZ, 'datos', f'regresion_generaliza_{modulo}_{stamp}.json')
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), modulo=modulo, semillas=seeds, veredictos=V,
                                 sha_bateria=h16(os.path.abspath(__file__)), sha_organismo=h16(os.path.join(AQUI, modulo + '.py')),
                                 python=platform.python_version(), numpy=np.__version__), corridas=res),
                  open(dj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
        log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
        _log['f'].close()
