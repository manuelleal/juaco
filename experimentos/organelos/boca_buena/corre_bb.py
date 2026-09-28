# EXPLORATORIO, no es dato
"""corre_bb.py — ablaciones EXPLORATORIAS de la boca_buena (creador, 28-sep-2026). UN proceso, corridas en serie, sin Pool.

MISION: llegar a la AGI por este camino.
Una corrida ES la de corre_v143.tarea / corre_puenteo: pista.run(seed, 9 carros iguales, T, **RUN_KW) + juez.resumen_linaje (solo fisica);
RUN_KW se verifica campo a campo contra corre_v143.tarea (regla 14; regla14()). Aparte, telemetria del hibrido (no puntua).
Brazos: 'v143' = HIBB sin puentes (== V143 bit a bit en la fisica; identidad_bb (2)); 'bb_<modo>' = puente boca_buena con BB = <modo>.
Uso:
  python corre_bb.py --humo                                   # 1 proceso, 6 corridas, T 20 000, semilla 39902; escribe datos/humo/*.json
  python corre_bb.py --brazos v143,bb_ref,bb_veto --semillas 39001-39003 [--T 100000]   # en serie, un proceso; salta lo ya corrido
Escribe datos/<brazo>_s<seed>_T<T>.json (ERR-54: el crudo se escribe antes de resumir nada; nube-9: la excepcion queda en JSON).
"""
import argparse, json, os, sys, time, traceback, importlib.util, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
RAIZ = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ORG))), 'bundle')   # JUACO/bundle
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
TV143 = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
sys.path.insert(0, PISTA)
import pista as P
import juez as J

DATOS = os.path.join(AQUI, 'datos')
RUN_KW = dict(pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
MODOS = ('ref', 'veto', 'fuerza', 'sinprueba', 'soloprueba', 'm0', 'vetom0', 'glotu', 'todo', 'vetoc', 'fuerzac', 'm10', 'm40', 'ventana', 'tinv', 'tinv40')
BRAZOS = ['v143'] + [f"bb_{m}" for m in MODOS]
SEM_OK = set(range(39001, 39011)) | set(range(39901, 39911))   # ablaciones 39001-39010 (encargo); practica/arnes/humo 39901-39910


def regla14():
    """Captura los argumentos con que corre_v143.tarea llama a pista.run (sin correr nada) y los compara con RUN_KW, campo a campo."""
    sys.path.insert(0, TV143)
    spec = importlib.util.spec_from_file_location('corre_v143_r14', os.path.join(TV143, 'corre_v143.py'))
    cv = importlib.util.module_from_spec(spec); spec.loader.exec_module(cv)
    cap = {}

    class _Alto(Exception): pass

    def falso(seed, carros, **kw):
        cap.update(kw); cap['_n'] = len(carros); raise _Alto()
    viejo = cv.P.run; cv.P.run = falso
    try:
        try: cv.tarea((39901, 'V143', 10))
        except _Alto: pass
    finally: cv.P.run = viejo
    T = cap.pop('T', None); n = cap.pop('_n', None)
    dif = {k: (cap.get(k), RUN_KW.get(k)) for k in set(cap) | set(RUN_KW) if cap.get(k, 'FALTA') != RUN_KW.get(k, 'FALTA')}
    return dict(ok=(not dif and n == 9 and T == 10), n=n, T=T, dif=dif)


def carga_hibb():
    spec = importlib.util.spec_from_file_location('HIBB', os.path.join(AQUI, 'carros', 'HIBB.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def corrida(brazo, seed, T, carpeta):
    if brazo not in BRAZOS: raise SystemExit(f"corre_bb: brazo {brazo!r} fuera de {BRAZOS}")
    os.makedirs(carpeta, exist_ok=True)
    fin = os.path.join(carpeta, f"{brazo}_s{seed}_T{T}.json")
    if os.path.exists(fin): print(f"  ya existe {os.path.basename(fin)}", flush=True); return fin
    H = carga_hibb()
    H.PUENTES = dict(patas=0, boca_buena=0, boca_mala=0, memoria=0)
    if brazo != 'v143': H.PUENTES['boca_buena'] = 1; H.BB = brazo[3:]
    else: H.BB = 'ref'
    t0 = time.time()
    try:
        r = P.run(seed, [(f"HIBB_{brazo}", H)] * 9, T=T, **RUN_KW)
        L = [J.resumen_linaje(d, seed) for d in r['linajes']]
        sd = sum(x['descendientes'] for x in L); sm = sum(x['muertes'] for x in L)
        tel = [dict(hib=d['carro']['hib'], bbt=d['carro']['bbt'], bb=d['carro']['bb'], o1_tabla=d['carro']['o1'].get('tabla'),
                    v143=d['carro']['v143'].get('v143')) for d in r['linajes']]
        x = dict(seed=seed, brazo=brazo, bb=H.BB, puentes=dict(H.PUENTES), T=T, seg=round(time.time() - t0, 1), linajes=L, pista=r['pista'],
                 R0_pista=round(sd / (sm + len(L)), 4), tel=tel, EXPLORATORIO=True)
    except Exception:
        x = dict(seed=seed, brazo=brazo, T=T, error=traceback.format_exc(), EXPLORATORIO=True)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    if 'error' in x: print(f"  ERROR {brazo} s{seed}: {x['error'][-300:]}", flush=True); return fin
    r0 = [l['R0_real'] for l in x['linajes']]
    print(f"  {brazo} s{seed} T{T} {x['seg']}s · R0 real mediana {st.median(r0):.3f} · establecidos {sum(1 for l in x['linajes'] if l['fund_post10k'] == 0)}/9 · "
          f"R0 {r0}", flush=True)
    return fin


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--brazos'); ap.add_argument('--semillas'); ap.add_argument('--T', type=int, default=100000)
    a = ap.parse_args()
    if a.humo:
        r14 = regla14(); print(f"regla 14: {r14}", flush=True)
        if not r14['ok']: return 1
        carpeta = os.path.join(DATOS, 'humo'); hechos = []
        for b in ('v143', 'bb_ref', 'bb_veto', 'bb_fuerza', 'bb_vetom0', 'bb_glotu'):
            hechos.append(corrida(b, 39902, 20000, carpeta))
        bien = all('error' not in json.load(open(f, encoding='utf-8')) for f in hechos)
        print(f"HUMO {'OK' if bien else 'FALLA'}: {len(hechos)} JSON escritos en {carpeta}")
        return 0 if bien else 1
    if not (a.brazos and a.semillas): raise SystemExit("corre_bb: --brazos y --semillas (o --humo)")
    s0, s1 = (int(z) for z in a.semillas.split('-')); sem = list(range(s0, s1 + 1))
    if not set(sem) <= SEM_OK: raise SystemExit(f"corre_bb: semillas fuera de {sorted(SEM_OK)[0]}-... ")
    if a.T > 100000: raise SystemExit("corre_bb: T maximo 100 000")
    brazos = [b for b in a.brazos.split(',') if b]
    for b in brazos:
        if b not in BRAZOS: raise SystemExit(f"corre_bb: brazo {b!r} fuera de {BRAZOS}")
    t0 = time.time()
    for s in sem:              # por semilla: todos los brazos de una semilla antes de la siguiente (pareado primero)
        for b in brazos: corrida(b, s, a.T, DATOS)
    print(f"FIN {len(sem) * len(brazos)} corridas en {time.time() - t0:.0f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
