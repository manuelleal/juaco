# EXPLORATORIO, no es dato
"""lee_puenteo.py — tablas del puenteo: por puente y semilla, R0 real (mediana de 9 linajes), establecidos (0 fundadores tras t 10 000),
vida del hijo (mediana de las vidas de los cuerpos NO fundadores que murieron), y el pareado contra V143 con la MISMA semilla.
Bases V143 y O1 por semilla: los crudos de la serie frio_carrera de hoy (misma pista, mismos shas, mismos mundos: seeds 36001-36020).
Uso: python lee_puenteo.py [--md]
"""
import argparse, glob, json, os, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, 'datos')
BASE = os.path.join(os.path.dirname(os.path.dirname(AQUI)), 'frio_carrera', 'datos', 'frio_carrera_s36001-36020_T100000_20260925_145319')
ORDEN = ['v143', 'v143p', 'patas', 'boca', 'boca_mala', 'boca_buena', 'memoria', 'patas_bmala', 'patas_bbuena', 'patas_memoria', 'boca_memoria', 'patas_boca', 'todo', 'o1']


def medida(L):
    r0 = [l['R0_real'] for l in L]
    est = sum(1 for l in L if l['fund_post10k'] == 0)
    hv = [v for l in L for v, o in zip(l['telem']['vidas'][:-1], l['telem']['origen'][:-1]) if o == 1]
    fv = [v for l in L for v, o in zip(l['telem']['vidas'][:-1], l['telem']['origen'][:-1]) if o == 0]
    hijos_sin = [d for l in L for d, o in zip(l['telem']['desc_por_vida'][:-1], l['telem']['origen'][:-1]) if o == 1]
    cz = {k: sum(l['causas'][k] for l in L) for k in ('hambre', 'sed', 'veneno', 'sal')}
    bd = sum(l['mord']['B'] + l['mord']['D'] for l in L); ac = sum(l['mord']['A'] + l['mord']['C'] for l in L)
    est_r0 = [l['R0_real'] for l in L if l['fund_post10k'] == 0]
    return dict(R0=st.median(r0), est=est, cruzan=sum(l['cruza_real'] for l in L), vida_hijo=(st.median(hv) if hv else None), n_hijos=len(hv),
                vida_fund=(st.median(fv) if fv else None), n_fund=len(fv), hijo_sin_parir=(round(sum(1 for d in hijos_sin if d == 0) / len(hijos_sin), 3) if hijos_sin else None),
                hijos_por_hijo=(round(sum(hijos_sin) / len(hijos_sin), 2) if hijos_sin else None),
                R0_est=(st.median(est_r0) if est_r0 else None), causas=cz, bd=bd, ac=ac, coh=all(l['coherente'] for l in L))


def carga():
    R = {}
    for b in ('v143', 'o1'):
        for f in glob.glob(os.path.join(BASE, f"{b}_s*.json")):
            d = json.load(open(f, encoding='utf-8')); R.setdefault(b, {})[d['seed']] = d
    for f in glob.glob(os.path.join(DATOS, '*.json')):
        d = json.load(open(f, encoding='utf-8'))
        if str(d.get('puente', '')).startswith('_'): continue   # marcadores de lanza.py (corridas omitidas por tiempo)
        R.setdefault(d['puente'], {})[d['seed']] = d
    return R


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(st.median(xs), 3) if xs else None


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument('--md', action='store_true'); a = ap.parse_args()
    R = carga()
    M = {b: {s: medida(d['linajes']) for s, d in R[b].items()} for b in R}
    sem_p = sorted({s for b in M if b not in ('v143', 'o1') for s in M[b]})
    sem = sem_p or sorted(M['v143'])
    v = M['v143']; o = M['o1']
    gap = med([o[s]['R0'] - v[s]['R0'] for s in sem])
    print(f"semillas {sem[0]}-{sem[-1]} ({len(sem)}) · V143 mediana R0 real {med([v[s]['R0'] for s in sem])} · O1 {med([o[s]['R0'] for s in sem])} · brecha mediana {gap}\n")
    print("## Resumen por puente (mediana sobre semillas; pareado por semilla contra V143 y contra O1)")
    print("| puente | sem | R0 real med | camino recuperado | gana a V143 | dif med vs V143 | pierde con O1 | establecidos/9 | R0 de establecidos | vida hijo | vida fund | hijo sin parir | hijos/hijo | B+D/linaje | causas h/s/v/s |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for b in ORDEN:
        if b not in M: continue
        ss = sorted(set(M[b]) & set(sem)) if b not in ('v143', 'o1') else sem
        if not ss: continue
        x = M[b]
        dv = [x[s]['R0'] - v[s]['R0'] for s in ss]; do = [x[s]['R0'] - o[s]['R0'] for s in ss]
        r0 = med([x[s]['R0'] for s in ss]); cam = None
        if b not in ('v143', 'o1'):
            cam = med([(x[s]['R0'] - v[s]['R0']) / (o[s]['R0'] - v[s]['R0']) for s in ss if o[s]['R0'] != v[s]['R0']])
        cz = {k: sum(x[s]['causas'][k] for s in ss) for k in ('hambre', 'sed', 'veneno', 'sal')}
        print(f"| {b} | {len(ss)} | **{r0}** | {'' if cam is None else f'{cam:+.0%}'} | {sum(1 for d in dv if d > 0)}/{len(ss)} | {med(dv):+.3f} | {sum(1 for d in do if d < 0)}/{len(ss)} | "
              f"{med([x[s]['est'] for s in ss])} | {med([x[s]['R0_est'] for s in ss])} | {med([x[s]['vida_hijo'] for s in ss])} | {med([x[s]['vida_fund'] for s in ss])} | "
              f"{med([x[s]['hijo_sin_parir'] for s in ss])} | {med([x[s]['hijos_por_hijo'] for s in ss])} | {med([x[s]['bd'] / 9 for s in ss])} | "
              f"{cz['hambre']}/{cz['sed']}/{cz['veneno']}/{cz['sal']} |")
    print("\n## Por semilla: R0 real (mediana de 9 linajes) · establecidos/9 · vida del hijo")
    cols = [b for b in ORDEN if b in M]
    print("| semilla | " + " | ".join(cols) + " |"); print("|---|" + "---|" * len(cols))
    for s in sem:
        fila = []
        for b in cols:
            if s in M[b]: m = M[b][s]; fila.append(f"{m['R0']:.3f} · {m['est']} · {m['vida_hijo']}")
            else: fila.append('–')
        print(f"| {s} | " + " | ".join(fila) + " |")
    # telemetria del hibrido (ultima instancia de cada linaje; NO puntua)
    print("\n## Telemetría del híbrido (última instancia de cada linaje; no puntúa): decisiones en que O1 y V143 discrepan")
    for b in ORDEN:
        if b in ('v143', 'o1') or b not in R: continue
        tot = {}
        for s, d in R[b].items():
            for t in d['tel']:
                for k, val in t['hib'].items(): tot[k] = tot.get(k, 0) + val
        if tot.get('boca_dec'):
            print(f"- {b}: pasos {tot['pasos']} · mov distinto {tot['mov_dif']/tot['pasos']:.1%} (puenteados {tot['mov_puenteado']}) · decisiones de boca {tot['boca_dec']}: discrepan {tot['boca_dif']/tot['boca_dec']:.1%} "
                  f"(malas {tot['boca_mala_dif']}/{tot['boca_mala_dec']}, buenas {tot['boca_buena_dif']}/{tot['boca_buena_dec']}; puenteadas {tot['boca_puenteada']}) · lecciones memoria {tot['mem_lecciones']} en {tot['mem_nacidos']} nacidos")
    return 0


if __name__ == '__main__':
    main()
