"""explora2_termop.py -- EXPLORATORIO 2 de TERMO' (no es serie; no decide). Encargo del coordinador (28-sep, tras el NO PASA de TERMO:
cayeron T-C ii y T-E; T-G paso): medir en TERMO' las TRES cosas -- (1) la reversion (T-E completo y T-C ii), (2) T-G, (3) la carrera
(ya medida: explora_termop.py --carrera, 5/5 identicas a TERMO). Usa las TAREAS del runner del examen v144b tal cual.
20 semillas EXPLORATORIAS 49021-49040 (libres; fuera de toda serie preregistrada). Pool 4 (el encargo lo permite).
  examen v3' seis etapas {TERMO', v14.3} x 20             240 corridas  -> T-C (i), T-E, T-F examen con la letra (n 20, como el examen)
  T-C (ii) {OFF, TERMO'} x 20                              40 corridas  -> rev, LI con n 20 (la letra pide 80: INDICATIVO)
  T-A / T-G {VIVO, CUELLO_MIN} x {OFF, TERMO', TERMOPINV} x 20  120 corridas -> r, muertes, d y LI con n 20 (INDICATIVO)
"""
import json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_examen_v144b as R
import numpy as np

SEM = list(range(49021, 49041))


def log(f, m):
    l = f"[{time.strftime('%H:%M:%S')}] {m}"; print(l, flush=True); f.write(l + '\n'); f.flush()


def corre(fn, tareas, n):
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    with mp.Pool(n) as p:
        return list(p.imap_unordered(fn, tareas, chunksize=1))


def li(d):
    d = np.asarray(d, float); return round(float(d.mean()), 2), round(float(d.std(ddof=1)), 2), round(float(d.mean() - 1.645 * d.std(ddof=1) / np.sqrt(len(d))), 2)


if __name__ == '__main__':
    import io, contextlib
    os.makedirs(os.path.join(AQUI, 'datos'), exist_ok=True)
    nom = f"explora2_termop_{time.strftime('%Y%m%d_%H%M%S')}"
    f = open(os.path.join(AQUI, 'datos', nom + '.log'), 'w', encoding='utf-8')
    log(f, f"EXPLORATORIO 2 TERMO' — semillas {SEM[0]}-{SEM[-1]}, Pool 4; runner {R.h16(R.__file__)}")
    t0 = time.time()
    ex = corre(R.tarea_ex, [(o, e, s) for o in R.U.ORGS_EX for e in R.U.SEIS for s in SEM], 4)
    log(f, f"examen listo ({time.time() - t0:.0f} s)")
    rv = corre(R.tarea_rev, [(s, a, R.U.T_VIVO) for s in SEM for a in ('OFF', 'CAND')], 4)
    log(f, f"T-C ii listo ({time.time() - t0:.0f} s)")
    va = corre(R.tarea_vivo, [(b, s, a, R.U.T_VIVO) for b in R.U.BRAZOS_TA for s in SEM for a in ('OFF', 'CAND', 'CTRL')], 4)
    log(f, f"T-A listo ({time.time() - t0:.0f} s)")
    with contextlib.redirect_stdout(io.StringIO()):
        VE = R.veredicto_EX([dict(r) for r in ex])
    out = dict(semillas=SEM, T_E={e: VE['conducta'][e]['todas'] for e in R.U.SEIS}, T_E_detalle={e: VE['conducta'][e]['detalle'] for e in R.U.SEIS},
               T_C_i=VE['T_C_i'], T_F_examen={q: (v['cand'], v['tronco'], v['razon']) for q, v in VE['coste'].items()}, mordA_Q4_E2=VE['mordA_Q4_E2'])
    log(f, f"(1) T-E por escenario (>= 18/20): {out['T_E']}")
    log(f, f"    detalle: {out['T_E_detalle']}")
    log(f, f"    T-C (i) come B Q4 >= 50: {out['T_C_i']['comeB_Q4']}/20 · T-F examen {out['T_F_examen']} · E2 muerde A Q4 mediana {out['mordA_Q4_E2']}")
    o = {r['seed']: r for r in rv if r['arm'] == 'OFF'}; c = {r['seed']: r for r in rv if r['arm'] == 'CAND'}
    d = [c[s]['rev'] - o[s]['rev'] for s in SEM]
    out['T_C_ii'] = dict(rev=(float(np.median([o[s]['rev'] for s in SEM])), float(np.median([c[s]['rev'] for s in SEM]))), d_media_sd_LI=li(d),
                         muertes=(float(np.median([o[s]['deaths'] for s in SEM])), float(np.median([c[s]['deaths'] for s in SEM]))),
                         mordB_Q4=(float(np.median([o[s]['mordB'][3] for s in SEM])), float(np.median([c[s]['mordB'][3] for s in SEM]))),
                         mordA_Q4=(float(np.median([o[s]['mordA'][3] for s in SEM])), float(np.median([c[s]['mordA'][3] for s in SEM]))),
                         visA_Q4=(float(np.median([o[s]['visA'][3] for s in SEM])), float(np.median([c[s]['visA'][3] for s in SEM]))),
                         memA_neg=sum(1 for s in SEM if c[s]['termo']['adS']['A'][0] < 0))
    x = out['T_C_ii']
    log(f, f"(1) T-C ii: rev mediana OFF {x['rev'][0]} TERMO' {x['rev'][1]} · d media/sd/LI(n=20) {x['d_media_sd_LI']} (letra: LI > -12.5 con n 80) · "
           f"muertes {x['muertes']} · come B Q4 {x['mordB_Q4']} · muerde A Q4 {x['mordA_Q4']} · visA Q4 {x['visA_Q4']} · memoria de A negativa {x['memA_neg']}/20")
    out['T_G'] = {}
    for b in R.U.BRAZOS_TA:
        g = lambda a: {r['seed']: r for r in va if r['brazo'] == b and r['arm'] == a}
        O, C, K = g('OFF'), g('CAND'), g('CTRL')
        y = dict(r=(float(np.median([O[s]['r'] for s in SEM])), float(np.median([C[s]['r'] for s in SEM])), float(np.median([K[s]['r'] for s in SEM]))),
                 muertes=(float(np.median([O[s]['deaths'] for s in SEM])), float(np.median([C[s]['deaths'] for s in SEM]))),
                 d_cand=li([C[s]['r'] - O[s]['r'] for s in SEM]), d_ctrl=li([K[s]['r'] - O[s]['r'] for s in SEM]),
                 gana=sum(C[s]['r'] > O[s]['r'] for s in SEM))
        out['T_G'][b] = y
        log(f, f"(2) {b}: r mediana OFF/TERMO'/TERMOPINV {y['r']} · muertes OFF/TERMO' {y['muertes']} · d TERMO' media/sd/LI(n=20) {y['d_cand']} "
               f"· d TERMOPINV {y['d_ctrl']} · TERMO' gana {y['gana']}/20")
    dj = os.path.join(AQUI, 'datos', nom + '.json')
    json.dump(dict(exploratorio=True, **out, crudos=dict(ex=ex, rev=rv, vivo=va)), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f, f"datos -> {os.path.relpath(dj, R.RAIZ)} sha256_16 = {R.h16(dj)} ({time.time() - t0:.0f} s)")
