"""H-PLANO en w90: serie y replica para el PC (PREREGISTRO_hplano_w90_PC.md).
Ohno tal cual (corre_ohno.trabajo, SERIE, GRAM, R_REP 0.006, motor sin tocar); solo cambia corre_ohno.MUNDO a w90 antes del fork.

  python corre_hplano_w90.py --control                        # w30 reproduce la serie de Ohno s25011 campo a campo (~3 min, 2 procesos)
  python corre_hplano_w90.py --prueba_pool --pool 2           # w90, T 12000, semillas 25991-25992 (~2 min)
  python corre_hplano_w90.py --serie --ventana serie --pool 3     # 25111-25130
  python corre_hplano_w90.py --serie --ventana replica --pool 3   # 25131-25150 (solo si la serie no da CAE)
  python corre_hplano_w90.py --lee <carpeta>
Tras un corte: repetir con --reanuda (salta los JSON ya escritos; los checkpoints de trabajo() retoman la corrida a medias).
"""
import argparse, glob, json, os, statistics as st, sys, time
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__)); OHNO = os.path.dirname(AQUI)
CWD0 = os.getcwd()
sys.path.insert(0, OHNO); os.chdir(OHNO)
import corre_ohno as CO

ESC = 90
BRAZOS = ('VIDA', 'FIJO:filtra0')
VENTANAS = dict(serie=(25111, 20), replica=(25131, 20))
PRUEBA = dict(desde=25991, n=2, T=12000, t_corte=10000, r0_margen=1000)
# letra (PREREGISTRO_hplano_w90_PC.md §4); nada de esto se toca despues de ver semillas
M0_MIN = 18          # nacidos antes del corte (mediana, por brazo)
P1_SOSTIENE = 0.90   # mediana de vivos_T VIDA/FIJO en pares que persisten los dos
P1_CAE = 0.75
P1_MIN_PARES = 8
S1_SOSTIENE = 1      # D = solo FIJO - solo VIDA
S1_CAE = 4
S2_FUERTE = 15       # vivos_T VIDA > FIJO pareado (estricto), de 20
DATOS = os.path.join(AQUI, 'datos')


def pon_mundo(esc): CO.MUNDO.update(nombre=f'w{esc}_pobre', esc=esc, n0=esc, tope=100 * esc)


def job(a):
    esc, seed, brazo, T, tc, rm, carpeta, reanuda = a
    pon_mundo(esc)
    return CO.trabajo((seed, brazo, T, tc, rm, CO.R_REP, carpeta, reanuda))


def nom(b): return b.replace(':', '_')


def carga(carpeta, b, s):
    p = os.path.join(carpeta, f"{nom(b)}_s{s}.json")
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


def veredicto(carpeta):
    semillas = sorted({int(os.path.basename(p).split('_s')[-1][:-5]) for p in glob.glob(os.path.join(carpeta, 'VIDA_s*.json'))})
    V = {s: carga(carpeta, 'VIDA', s) for s in semillas}; F = {s: carga(carpeta, 'FIJO:filtra0', s) for s in semillas}
    S = [s for s in semillas if V[s] and F[s] and not V[s].get('abortado') and not F[s].get('abortado')]
    L = []; n = len(S)
    if n == 0: return 'NO EVALUABLE (sin pares)', ['sin pares completos'], {}
    pre = {b: st.median([R[s]['n_nac'] - R[s]['nac_post'] for s in S]) for b, R in (('VIDA', V), ('FIJO', F))}
    m0 = min(pre.values()) >= M0_MIN
    L.append(f"M0 nacidos antes del corte (mediana) VIDA {pre['VIDA']} FIJO {pre['FIJO']} (umbral {M0_MIN}) -> {'OK' if m0 else 'FALLA'}")
    ambos = [s for s in S if V[s]['persiste'] and F[s]['persiste']]
    razon = [V[s]['vivos_T'] / F[s]['vivos_T'] for s in ambos]
    p1 = st.median(razon) if razon else None
    p1_ev = len(ambos) >= P1_MIN_PARES
    L.append(f"P1 vivos_T VIDA/FIJO en pares que persisten los dos: mediana {None if p1 is None else round(p1, 3)} en {len(ambos)} pares "
             f"(min {P1_MIN_PARES}; sostiene >= {P1_SOSTIENE}, cae <= {P1_CAE}) · rango {(round(min(razon), 3), round(max(razon), 3)) if razon else None}")
    sv = sum(V[s]['persiste'] and not F[s]['persiste'] for s in S); sf = sum(F[s]['persiste'] and not V[s]['persiste'] for s in S); D = sf - sv
    L.append(f"S1 persistencia pareada: ambos {len(ambos)} · solo VIDA {sv} · solo FIJO {sf} · ninguno {n - len(ambos) - sv - sf} · D {D} "
             f"(sostiene <= {S1_SOSTIENE}, cae >= {S1_CAE})")
    s2 = sum(V[s]['vivos_T'] > F[s]['vivos_T'] for s in S)
    L.append(f"S2 (version fuerte) vivos_T VIDA > FIJO pareado {s2}/{n} (fuerte >= {S2_FUERTE})")
    for b, R in (('VIDA', V), ('FIJO', F)):
        r0 = [R[s]['r0_post'] for s in S if R[s].get('r0_post') is not None]
        L.append(f"  {b}: persisten {sum(R[s]['persiste'] for s in S)}/{n} · vivos_T mediana {st.median([R[s]['vivos_T'] for s in S])} · "
                 f"nac_post mediana {st.median([R[s]['nac_post'] for s in S])} · r0_post mediana {st.median(r0) if r0 else None} "
                 f"rango {(min(r0), max(r0)) if r0 else None} · g_nmut mediana {st.median([R[s].get('g_nmut', 0) for s in S])}")
    if n < 20: v = f'NO EVALUABLE (pares completos {n} < 20)'
    elif not m0: v = 'NO EVALUABLE (M0: w90 no agrando la cohorte antes del corte)'
    elif (p1_ev and p1 <= P1_CAE) or D >= S1_CAE: v = 'CAE'
    elif not p1_ev: v = f'NO EVALUABLE (P1: {len(ambos)} pares que persisten < {P1_MIN_PARES})'
    elif p1 >= P1_SOSTIENE and D <= S1_SOSTIENE: v = 'SOSTIENE (debil)' + (' + FUERTE' if s2 >= S2_FUERTE else '')
    else: v = 'AMBIGUO'
    L.append(f"VEREDICTO H-PLANO w90 POR LA LETRA (una ventana; el bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(p1=p1, pares=len(ambos), D=D, s2=s2, n=n, pre=pre)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    for b in ('--control', '--prueba_pool', '--serie', '--reanuda'): ap.add_argument(b, action='store_true')
    ap.add_argument('--ventana', choices=tuple(VENTANAS)); ap.add_argument('--pool', type=int, default=3); ap.add_argument('--lee')
    a = ap.parse_args()
    os.makedirs(DATOS, exist_ok=True)
    if a.lee:
        v, L, d = veredicto(os.path.join(CWD0, a.lee))
        for l in L: print(l)
        return
    if a.control:
        c = os.path.join(DATOS, 'control_w30_pc'); os.makedirs(c, exist_ok=True)
        S = CO.SERIE; ref = os.path.join(OHNO, 'datos', 'ohno_serie_s25011-25030')
        print(f"[{time.strftime('%H:%M:%S')}] CONTROL w30 · shas {CO.SHAS()}", flush=True)
        with Pool(2) as p: p.map(job, [(30, 25011, b, S['T'], S['t_corte'], S['r0_margen'], c, False) for b in BRAZOS])
        ok = True
        for b in BRAZOS:
            x, y = carga(c, b, 25011), carga(ref, b, 25011)
            dif = sorted(k for k in set(x) | set(y) if k != 'seg' and x.get(k) != y.get(k))
            print(f"  {b}: distintas {dif}", flush=True); ok &= not dif
        print(f"CONTROL {'PASA' if ok else 'FALLA: no correr la serie'}"); sys.exit(0 if ok else 1)
    if a.prueba_pool:
        c = os.path.join(DATOS, 'prueba_pool_w90'); os.makedirs(c, exist_ok=True)
        P = PRUEBA; jobs = [(ESC, s, b, P['T'], P['t_corte'], P['r0_margen'], c, False) for s in range(P['desde'], P['desde'] + P['n']) for b in BRAZOS]
        with Pool(a.pool) as p:
            for i, r in enumerate(p.imap_unordered(job, jobs), 1):
                print(f"[{time.strftime('%H:%M:%S')}] [{i}/{len(jobs)}] {r.get('brazo')} s{r.get('seed')}: vivos {r.get('vivos_T')} abort {r.get('abortado')} ({r.get('seg')} s)", flush=True)
        print('PRUEBA DEL POOL: corre'); return
    if not (a.serie and a.ventana): sys.exit('usa --control, --prueba_pool, --serie --ventana serie|replica o --lee <carpeta>')
    d0, N = VENTANAS[a.ventana]
    c = os.path.join(DATOS, f"w90_{a.ventana}_s{d0}-{d0 + N - 1}")
    if os.path.isdir(c) and glob.glob(os.path.join(c, '*_s*.json')) and not a.reanuda:
        sys.exit(f"{c} ya tiene resultados; usa --reanuda (no se pisa nada)")
    os.makedirs(c, exist_ok=True)
    flog = open(os.path.join(c, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    pon_mundo(ESC)
    log(f"H-PLANO w90 {a.ventana} {d0}-{d0 + N - 1} · MUNDO {CO.MUNDO} · r_rep {CO.R_REP} · SERIE {CO.SERIE} · GRAM {CO.GRAM} · pool {a.pool} · shas {CO.SHAS()}")
    S = CO.SERIE
    jobs = [(ESC, s, b, S['T'], S['t_corte'], S['r0_margen'], c, a.reanuda) for s in range(d0, d0 + N) for b in BRAZOS]
    t0 = time.time()
    with Pool(a.pool) as p:
        for i, r in enumerate(p.imap_unordered(job, jobs), 1):
            log(f"[{i}/{len(jobs)}] {r.get('brazo')} s{r.get('seed')}: persiste {r.get('persiste')} vivos {r.get('vivos_T')} r0 {r.get('r0_post')} "
                f"nac {r.get('n_nac')} post {r.get('nac_post')} abort {r.get('abortado')} ({r.get('seg')} s; {time.time() - t0:.0f} s)")
    v, L, d = veredicto(c)
    for l in L: log(l)
    json.dump(dict(ventana=a.ventana, veredicto=v, lineas=L, d=d, MUNDO=CO.MUNDO, SERIE=CO.SERIE, GRAM=CO.GRAM, shas=CO.SHAS()),
              open(os.path.join(c, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    flog.close()


if __name__ == '__main__':
    main()
