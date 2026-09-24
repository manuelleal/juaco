"""reanuda_cruce.py — REANUDA una serie de cruce cortada (coordinador, 24-sep-2026: se fue la luz a ~15:48 con 180/200 tareas).

corre_cruce.py no tiene --reanuda. Cada tarea es independiente y determinista (semilla fija), así que esto:
  1. lee el `_parcial.jsonl` de la serie cortada (tareas terminadas, tal cual las escribió `guarda`);
  2. corre SOLO las tareas preregistradas que faltan, con corre_cruce.tarea (misma función, mismos argumentos) y Pool;
  3. las agrega al mismo parcial y al mismo log, y escribe crudo + resumen + veredicto con corre_cruce.informe/escribe,
     igual que el final de corre_cruce.main (sin --con: es la serie).
No cambia ninguna letra ni ningún número del preregistro. Declarado en el REGISTRO.
Uso: python experimentos/organelos/cruce/reanuda_cruce.py <pref de la serie sin extensión> --pool 6
"""
import json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import corre_cruce as C


def main():
    pref, pool_n = sys.argv[1], int(sys.argv[sys.argv.index('--pool') + 1])
    assert 1 <= pool_n <= 6
    R = [json.loads(l) for l in open(pref + '_parcial.jsonl', encoding='utf-8') if l.strip()]
    semillas = sorted({c['seed'] for c in R})
    assert semillas == list(range(C.SERIE.start, C.SERIE.stop)) or semillas == list(range(C.REPLICA.start, C.REPLICA.stop)), semillas
    hechas = {(c['fase'], c['brazo'], c['seed']) for c in R}
    tc, tl = C.TC_DEF, C.TL_DEF
    faltan_cria = [('cria', s, b, tc) for b in C.CRIAS for s in semillas if ('cria', b, s) not in hechas]
    assert not faltan_cria, f"faltan crias: {faltan_cria} (este reanudador sólo completa lecturas)"
    bancos = {(c['brazo'], c['seed']): c['banco'] for c in R if c['fase'] == 'cria' and not c.get('error')}
    faltan = []
    for b in C.LECTURAS:
        for s in semillas:
            if ('lee', b, s) in hechas: continue
            if b in C.MUESTRA_DE:
                cb, k = C.MUESTRA_DE[b]; bk = bancos.get((cb, s))
                if bk is None: continue
                faltan.append(('lee', s, b, tl, C.muestra(bk, s, k)))
            else: faltan.append(('lee', s, b, tl, None))
    flog = open(pref + '.log', 'a', encoding='utf-8')
    def log(s=''):
        print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"\nREANUDA (coordinador) · {time.strftime('%Y-%m-%d %H:%M:%S')} · se fue la luz: {len(R)} tareas hechas, faltan {len(faltan)}: "
        f"{sorted({(t[2]) for t in faltan})}")
    C.previas(log)
    parcial = open(pref + '_parcial.jsonl', 'a', encoding='utf-8'); t0 = time.time()
    from multiprocessing import Pool
    with Pool(pool_n) as pool:
        for c in pool.imap_unordered(C.tarea, faltan):
            R.append(c); parcial.write(json.dumps({k: v for k, v in c.items() if k != 'tb'} | ({'tb': c['tb']} if 'tb' in c else {}), default=str) + '\n'); parcial.flush()
            extra = f"ERROR {c['error']}" if c.get('error') else f"R0 real {C.sem_R0(c)}"
            log(f"  [{time.time() - t0:7.1f}s] {c['fase']} {c['brazo']} s{c['seed']} ({c['seg']}s) {extra}")
    parcial.close()
    R.sort(key=lambda c: (c['fase'], c['brazo'], c['seed']))
    sha = C.escribe(pref + '_crudo.json', R); log(f"  CRUDO {pref}_crudo.json (sha {sha})")
    inf = C.informe(R, log, len(semillas))
    resumen = dict(tc=tc, tl=tl, semillas=semillas, humo=False, p_mut=C.P_MUT, banco=C.BANCO, n_sombra=C.N_SOMBRA, g_max=C.G_MAX,
                   reanudada=dict(hechas_antes=len(R) - len(faltan), corridas_al_reanudar=len(faltan)),
                   seg_por_tarea={f"{f}_{b}": C.med([c['seg'] for c in R if c['fase'] == f and c['brazo'] == b]) for f, b in {(c['fase'], c['brazo']) for c in R}},
                   **inf)
    sha = C.escribe(pref + '_resumen.json', resumen); log(f"  RESUMEN {pref}_resumen.json (sha {sha})")
    ver = inf.get('veredicto')
    log(f"VEREDICTO: PARCIAL (sin replica; no se declara): {ver['veredicto'] if ver else 'incompleto'} · {ver}")
    flog.close()


if __name__ == '__main__':
    main()
