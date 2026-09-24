"""corre_transfiere.py — ECO-T: ¿lo que la selección eligió en ECO vive mejor en OTRO mundo? (nube, 24-sep-2026)

MISION: llegar a la AGI por este camino.

Preregistro: experimentos/juaco_eco/transfiere/PREREGISTRO_transfiere.md (la letra esta AQUI, en veredicto(), y alli).
Entrada: los BANCOS en el corte de ECO v1.1 (ya corridos y commiteados: datos/eco_v11_serie_s19401-19420 = ventana 'serie',
datos/eco_v11_serie_s19421-19440 = ventana 'replica'), del brazo VIDA (seleccion) y del brazo AZAR (deriva).
Mundo: la pista de la CARRERA (pista v1, reposicion inmediata; otro mundo que el de ECO), 9 lineas, T 100 000, fundador limpio,
carro FABRICA. Cada linea i lleva un genoma: 9 entradas al azar del banco (rng [c, 7]; el placebo [c, 8]); los 3 genes de historia de
vida (dote, rep_umbral, rep_X) se dejan en G0 porque en la carrera los fija la pista. c = semilla de ECO + 10 000 (29401-29440).
Brazos por semilla: VIDA (banco de VIDA), VIDA_P (placebo: otra muestra del MISMO banco), AZAR (banco de AZAR), G0 (FABRICA de fabrica).
Medida (solo fisica, juez.resumen_linaje): R0 real, mediana de las 9 lineas.

Uso (ERR-115: banderas desconocidas o abreviadas abortan):
  python experimentos/juaco_eco/transfiere/corre_transfiere.py --humo
  python experimentos/juaco_eco/transfiere/corre_transfiere.py --serie --ventana serie --pool 3
  python experimentos/juaco_eco/transfiere/corre_transfiere.py --serie --ventana replica --pool 3
  python experimentos/juaco_eco/transfiere/corre_transfiere.py --lee <carpeta>
"""
import argparse, glob, hashlib, json, os, statistics as st, sys, time, types
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
ECO = os.path.dirname(AQUI)
RAIZ = os.path.dirname(os.path.dirname(ECO))
for _d in (os.path.join(RAIZ, 'experimentos', 'carrera_escuderias'), ECO, os.path.join(RAIZ, 'experimentos', 'generaciones')):
    if _d not in sys.path: sys.path.insert(0, _d)
import pista as P
import juez as J
import motor_eco as ME

VENTANAS = {'serie': (19401, os.path.join(ECO, 'datos', 'eco_v11_serie_s19401-19420')),
            'replica': (19421, os.path.join(ECO, 'datos', 'eco_v11_serie_s19421-19440'))}
N = 20
DESPLAZA = 10000
T = 100000
BRAZOS = ('VIDA', 'VIDA_P', 'AZAR', 'G0')
FLUJO = {'VIDA': 7, 'VIDA_P': 8, 'AZAR': 7}
FUENTE = {'VIDA': 'VIDA', 'VIDA_P': 'VIDA', 'AZAR': 'AZAR'}
HISTORIA = [ME.NOMBRES.index(g) for g in ('dote', 'rep_umbral', 'rep_X')]
G0 = np.asarray(ME.genoma0(P.cfg_fabrica()), float)
HUMO = dict(eco_semilla=19401, T=5000)
DATOS = os.path.join(AQUI, 'datos')
_FAB = [None]


class BanderaMala(SystemExit):
    pass


def fab():
    if _FAB[0] is None: _FAB[0] = P.carga_carro('FABRICA')
    return _FAB[0]


def banco(ventana_dir, brazo_eco, s):
    r = json.load(open(os.path.join(ventana_dir, f"{brazo_eco}_s{s}.json"), encoding='utf-8'))
    if not r.get('corte') or not r['corte'].get('banco'): raise SystemExit(f"ECO-T: {brazo_eco}_s{s} sin banco en el corte")
    return np.asarray(r['corte']['banco'], float)


def genomas(bank, c, flujo):
    """9 genomas: entradas al azar del banco con el rng [c, flujo] (como el juez de ECO), historia de vida en G0."""
    idx = np.random.default_rng([c, flujo]).choice(len(bank), size=9, replace=len(bank) < 9)
    G = bank[idx].copy()
    G[:, HISTORIA] = G0[HISTORIA]
    return G


def modulo_colonia(G, nombre='COLONIA'):
    """Carro FABRICA con el genoma G[i] en la linea i (ME.ctx_genoma sobre el ctx de la pista; cfg_fabrica es una copia por carro)."""
    m = types.ModuleType('carro_' + nombre)
    F = fab()

    def crea(ctx, _G=np.asarray(G, float)):
        ME.ctx_genoma(ctx, _G[ctx['indice']])
        return F.crea(ctx)
    m.crea = crea
    return m


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def corre(c, brazo, mod, T_):
    t0 = time.time()
    r = P.run(c, [(brazo, mod)] * 9, T=T_, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
    L = [J.resumen_linaje(d, c) for d in r['linajes']]
    return dict(c=c, brazo=brazo, T=T_, seg=round(time.time() - t0, 1), R0_real_med=med([l['R0_real'] for l in L]),
                R0_real=[l['R0_real'] for l in L], persisten=sum(l['persiste'] for l in L), vida_med=med([l['vida_med'] for l in L]),
                muertes_med=med([l['muertes'] for l in L]), fundadores_med=med([l['fundadores'] for l in L]),
                causas={k: sum(l['causas'][k] for l in L) for k in ('hambre', 'sed', 'veneno', 'sal')})


def tarea(args):
    s, brazo, vdir, T_, carpeta = args
    c = s + DESPLAZA
    fin = os.path.join(carpeta, f"{brazo}_s{s}.json")
    if os.path.exists(fin): return json.load(open(fin, encoding='utf-8'))
    if brazo == 'G0':
        G = np.tile(G0, (9, 1)); mod = fab()
    else:
        G = genomas(banco(vdir, FUENTE[brazo], s), c, FLUJO[brazo]); mod = modulo_colonia(G, brazo)
    x = corre(c, brazo, mod, T_)
    x.update(eco_semilla=s, genomas=[[round(float(v), 6) for v in g] for g in G],
             log_ratio_mediano={g: round(float(np.median(np.log(G[:, j] / G0[j]))), 4) for j, g in enumerate(ME.NOMBRES)})
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(x, f)
    os.replace(tmp, fin)
    return x


# ================================================================================ LA LETRA (PREREGISTRO_transfiere.md §5)
def veredicto(R, n_esperado=N):
    L = []; by = {b: {x['eco_semilla']: x for x in R if x['brazo'] == b} for b in BRAZOS}
    n = {b: len(v) for b, v in by.items()}
    completo = all(n[b] == n_esperado for b in BRAZOS)

    def pareado(a, b):
        w = e = k = 0
        for s in sorted(set(by[a]) & set(by[b])):
            u, v = by[a][s]['R0_real_med'], by[b][s]['R0_real_med']
            if u is None or v is None: continue
            k += 1; w += int(u > v); e += int(u == v)
        return w, e, k
    wVA, eVA, kVA = pareado('VIDA', 'AZAR')
    wVG, eVG, kVG = pareado('VIDA', 'G0')
    wAG, eAG, kAG = pareado('AZAR', 'G0')
    wVP, eVP, kVP = pareado('VIDA', 'VIDA_P')
    plac = wVP + 0.5 * eVP
    placebo_ok = kVP == n_esperado and 5 <= plac <= 15
    T1 = wVA >= 15
    T2 = wVG >= 15
    medi = {b: med([x['R0_real_med'] for x in by[b].values()]) for b in BRAZOS}
    L.append(f"semillas por brazo: {n}; R0 real (mediana de las medianas de 9 lineas): {medi}")
    L.append(f"T1 VIDA > AZAR (pareado, estricto) {wVA}/{kVA} (empates {eVA}) · T2 VIDA > G0 {wVG}/{kVG} (empates {eVG}) · "
             f"descriptivo AZAR > G0 {wAG}/{kAG} (empates {eAG})")
    L.append(f"PLACEBO VIDA contra VIDA_P (otra muestra del mismo banco): {plac} de {kVP} (valido en [5, 15]) -> {'VALIDO' if placebo_ok else 'NO VALIDO'}")
    L.append(f"persisten (lineas de 9, suma): { {b: sum(x['persisten'] for x in by[b].values()) for b in BRAZOS} }")
    if not completo: v = 'NO EVALUABLE (serie incompleta)'
    elif not placebo_ok: v = 'NO EVALUABLE (el placebo sale de [5, 15])'
    elif T1 and T2: v = 'TRANSFIERE (en esta serie): lo seleccionado en ECO vive mejor en la carrera que lo derivado y que G0'
    elif T2: v = 'HAY ALGO MODESTO (en esta serie): mejor que G0 en la carrera, pero no se distingue de la deriva'
    elif T1: v = 'HAY ALGO MODESTO (en esta serie): mejor que la deriva en la carrera, pero no que G0'
    else: v = 'NO (en esta serie)'
    L.append(f"VEREDICTO POR LA LETRA (una ventana; el del bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(T1=T1, T2=T2, wVA=wVA, wVG=wVG, wAG=wAG, placebo=plac, placebo_ok=placebo_ok, medianas=medi)


def lee(carpeta, n_esperado=N):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    v, L, d = veredicto(R, n_esperado)
    for l in L: print(l, flush=True)
    return v, L, d, R


def SHAS():
    f = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    d = {'corre_transfiere.py': f(os.path.abspath(__file__)), 'pista.py': f(P.__file__), 'juez.py': f(J.__file__),
         'motor_eco.py': f(ME.__file__), 'FABRICA.py': f(os.path.join(P.CARROS, 'FABRICA.py'))}
    pr = os.path.join(AQUI, 'PREREGISTRO_transfiere.md')
    if os.path.exists(pr): d['PREREGISTRO_transfiere.md'] = f(pr)
    return d


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true'); ap.add_argument('--lee', default=None)
    ap.add_argument('--ventana', default=None); ap.add_argument('--pool', type=int)
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('ECO-T: banderas mal formadas')
    if resto: raise BanderaMala(f"ECO-T: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('ECO-T: sin la forma --bandera=valor')
    if len(argv) != len(set(x for x in argv if x.startswith('--'))) + sum(1 for x in argv if not x.startswith('--')):
        raise BanderaMala('ECO-T: bandera repetida')
    if int(a.humo) + int(a.serie) + int(a.lee is not None) != 1: raise BanderaMala('ECO-T: exactamente uno de --humo, --serie, --lee')
    if a.humo and (a.ventana is not None or a.pool is not None): raise BanderaMala('ECO-T: --humo va solo')
    if a.lee is not None and (a.ventana is not None or a.pool is not None): raise BanderaMala('ECO-T: --lee va solo')
    if a.serie and (a.ventana not in VENTANAS or a.pool is None or not 1 <= a.pool <= 3):
        raise BanderaMala('ECO-T: --serie --ventana serie|replica --pool 1..3')
    return a


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.lee is not None:
        lee(a.lee); return
    if a.humo:
        s = HUMO['eco_semilla']; vdir = VENTANAS['serie'][1]; t0 = time.time()
        carpeta = os.path.join(DATOS, 'humo', time.strftime('humo_%Y%m%d_%H%M%S')); os.makedirs(carpeta, exist_ok=True)
        print(f"[{time.strftime('%H:%M:%S')}] HUMO ECO-T · shas {SHAS()}", flush=True)
        for b in BRAZOS:
            x = tarea((s, b, vdir, HUMO['T'], carpeta))
            print(f"[{time.strftime('%H:%M:%S')}] {b}: R0 real {x['R0_real_med']} · persisten {x['persisten']}/9 · {x['seg']} s · "
                  f"log(g/G0) mediano alpha {x['log_ratio_mediano']['alpha']} aversion {x['log_ratio_mediano']['aversion']}", flush=True)
        print(f"HUMO: {round(time.time() - t0, 1)} s (numeros sin valor); carpeta {os.path.relpath(carpeta, RAIZ)}")
        return
    desde, vdir = VENTANAS[a.ventana]
    carpeta = os.path.join(DATOS, f"transfiere_{a.ventana}_s{desde}-{desde + N - 1}")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"ECO-T ventana {a.ventana} (bancos de {os.path.relpath(vdir, RAIZ)}) · T {T} · pool {a.pool} · shas {SHAS()}")
    jobs = [(s, b, vdir, T, carpeta) for s in range(desde, desde + N) for b in BRAZOS]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool) as pool:
        for k, x in enumerate(pool.imap_unordered(tarea, jobs), 1):
            log(f"[{k}/{len(jobs)}] {x['brazo']} s{x['eco_semilla']} (c {x['c']}): R0 real {x['R0_real_med']} · persisten {x['persisten']}/9 "
                f"({x['seg']} s; {round(time.time() - t0)} s)")
    v, L, d, R = lee(carpeta)
    for l in L: flog.write(l + '\n')
    json.dump(dict(ventana=a.ventana, veredicto=v, lineas=L, d=d, seg=round(time.time() - t0), T=T, shas=SHAS()),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    log(f"VEREDICTO: {v}")
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
