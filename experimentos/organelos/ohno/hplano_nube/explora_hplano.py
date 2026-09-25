"""EXPLORATORIO H-PLANO: Ohno tal cual, con el mundo 3 veces mayor (PREREGISTRO_hplano_w90.md). Solo cambia corre_ohno.MUNDO antes del fork."""
import sys, os, json, time, statistics as st
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); OHNO = os.path.dirname(AQUI)
sys.path.insert(0, OHNO); os.chdir(OHNO)
import corre_ohno as CO

def log(f, m):
    l = f"[{time.strftime('%H:%M:%S')}] {m}"; print(l, flush=True); f.write(l + '\n'); f.flush()

def pon_mundo(esc): CO.MUNDO.update(nombre=f'w{esc}_pobre', esc=esc, n0=esc, tope=100 * esc)

def job(a):
    esc, seed, brazo, carpeta = a
    pon_mundo(esc); S = CO.SERIE
    return CO.trabajo((seed, brazo, S['T'], S['t_corte'], S['r0_margen'], CO.R_REP, carpeta, True))

def carga(carpeta, brazo, s):
    return json.load(open(os.path.join(carpeta, f"{brazo.replace(':', '_')}_s{s}.json")))

if __name__ == '__main__':
    modo = sys.argv[1]
    out = os.path.join(AQUI, 'datos'); os.makedirs(out, exist_ok=True)
    f = open(os.path.join(out, f'progreso_{modo}.log'), 'a')
    B = ('VIDA', 'FIJO:filtra0')
    if modo == 'control':   # w30 debe reproducir la serie de la noche
        c = os.path.join(out, 'control_w30'); os.makedirs(c, exist_ok=True)
        log(f, f"CONTROL w30 · shas {CO.SHAS()}")
        with Pool(2) as p: p.map(job, [(30, 25011, b, c) for b in B])
        ok = True
        for b in B:
            x = carga(c, b, 25011); y = carga(os.path.join(OHNO, 'datos/ohno_serie_s25011-25030'), b, 25011)
            dif = [k for k in set(x) | set(y) if k != 'seg' and x.get(k) != y.get(k)]
            log(f, f"  {b}: distintas {dif}"); ok &= not dif
        log(f, f"CONTROL {'PASA' if ok else 'FALLA'}")
    elif modo == 'w90':
        c = os.path.join(out, 'w90_s25101-25110'); os.makedirs(c, exist_ok=True)
        pon_mundo(90); log(f, f"W90 · MUNDO {CO.MUNDO} · r_rep {CO.R_REP} · SERIE {CO.SERIE} · shas {CO.SHAS()}")
        jobs = [(90, s, b, c) for s in range(25101, 25111) for b in B]
        with Pool(3) as p:
            for i, r in enumerate(p.imap_unordered(job, jobs), 1):
                log(f, f"[{i}/{len(jobs)}] {r.get('brazo')} s{r.get('seed')}: persiste {r.get('persiste')} vivos {r.get('vivos_T')} r0 {r.get('r0_post')} nac {r.get('n_nac')} post {r.get('nac_post')} abort {r.get('abortado')} ({r.get('seg')} s)")
    elif modo == 'lee':
        c = os.path.join(out, 'w90_s25101-25110'); S = range(25101, 25111)
        V = {s: carga(c, 'VIDA', s) for s in S}; F = {s: carga(c, 'FIJO:filtra0', s) for s in S}
        pre = [r['n_nac'] - r['nac_post'] for r in list(V.values()) + list(F.values())]
        m0 = st.median(pre)
        sv = sum(V[s]['persiste'] and not F[s]['persiste'] for s in S); sf = sum(F[s]['persiste'] and not V[s]['persiste'] for s in S)
        pv = sum(V[s]['persiste'] for s in S); pf = sum(F[s]['persiste'] for s in S); D = sf - sv
        m2 = sum(V[s]['vivos_T'] >= F[s]['vivos_T'] for s in S)
        techo = pv >= 9 and pf >= 9
        log(f, f"M0 nacidos antes del corte (mediana) {m0} (w30: 6; umbral 18) -> {'OK' if m0 >= 18 else 'NO EVALUABLE'}")
        log(f, f"M1 persisten VIDA {pv} FIJO {pf} · solo VIDA {sv} · solo FIJO {sf} · D {D} · techo {techo} -> " + ('no se evalua (techo)' if techo else ('SOSTIENE' if D <= 0 else 'CAE' if D >= 2 else 'AMBIGUO')))
        log(f, f"M2 vivos_T VIDA >= FIJO {m2}/10 -> {'SOSTIENE' if m2 >= 7 else 'CAE' if m2 <= 3 else 'AMBIGUO'}")
        for b, R in (('VIDA', V), ('FIJO', F)):
            r0 = [r['r0_post'] for r in R.values() if r.get('r0_post') is not None]
            log(f, f"  {b}: vivos_T mediana {st.median([r['vivos_T'] for r in R.values()])} · nac_post mediana {st.median([r['nac_post'] for r in R.values()])} · r0_post mediana {st.median(r0) if r0 else None} rango {(min(r0), max(r0)) if r0 else None} · g_nmut mediana {st.median([r.get('g_nmut', 0) for r in R.values()])}")
        log(f, f"  nac_post VIDA/FIJO (medianas): {st.median([r['nac_post'] for r in V.values()]) / max(1, st.median([r['nac_post'] for r in F.values()])):.2f} (w30 0.11)")
        for s in S: log(f, f"  VIDA s{s}: persiste {V[s]['persiste']} vivos {V[s]['vivos_T']} | FIJO persiste {F[s]['persiste']} vivos {F[s]['vivos_T']}")
