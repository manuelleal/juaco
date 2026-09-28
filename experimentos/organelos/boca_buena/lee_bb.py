# EXPLORATORIO, no es dato
"""lee_bb.py — tablas de las ablaciones de la boca_buena (datos/*_T<T>.json). Pareado por semilla contra v143 y contra bb_ref.
Medida: mediana por semilla del R0 real de los 9 linajes (juez.resumen_linaje, tal cual); mediana sobre semillas.
Uso: python lee_bb.py [--T 100000] [--dir datos]
"""
import argparse, glob, json, os, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))
ORDEN = ['v143', 'bb_ref', 'bb_veto', 'bb_fuerza', 'bb_vetoc', 'bb_fuerzac','bb_todo', 'bb_m0', 'bb_sinprueba', 'bb_soloprueba', 'bb_vetom0', 'bb_glotu', 'bb_m10', 'bb_m40', 'bb_ventana', 'bb_tinv', 'bb_tinv40']


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(st.median(xs), 3) if xs else None


def medida(d):
    L = d['linajes']
    hv = [v for l in L for v, o in zip(l['telem']['vidas'][:-1], l['telem']['origen'][:-1]) if o == 1]
    return dict(R0=st.median([l['R0_real'] for l in L]), est=sum(1 for l in L if l['fund_post10k'] == 0),
                cruzan=sum(bool(l['cruza_real']) for l in L), viab=st.median([l['pasos_viables'] for l in L]),
                ac=sum(l['mord']['A'] + l['mord']['C'] for l in L) / 9, bd=sum(l['mord']['B'] + l['mord']['D'] for l in L) / 9,
                vh=(st.median(hv) if hv else None), buenos_mundo=d['pista']['comp_mundo']['A'] + d['pista']['comp_mundo']['C'],
                sinbueno=d['pista']['frac_sin_bueno_mundo'],
                cz={k: sum(l['causas'][k] for l in L) for k in ('hambre', 'sed', 'veneno', 'sal')})


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument('--T', type=int, default=100000); ap.add_argument('--dir', default='datos')
    a = ap.parse_args()
    R = {}
    for f in glob.glob(os.path.join(AQUI, a.dir, f"*_T{a.T}.json")):
        d = json.load(open(f, encoding='utf-8'))
        if str(d.get('brazo', '')).startswith('_'): continue   # marcadores de corridas omitidas
        if 'error' in d: print(f"ERROR en {os.path.basename(f)}"); continue
        R.setdefault(d['brazo'], {})[d['seed']] = d
    M = {b: {s: medida(d) for s, d in R[b].items()} for b in R}
    print(f"# EXPLORATORIO · T {a.T} · brazos {sorted(M)}\n")
    print("| brazo | sem | R0 real med | por semilla | sem con mayoría que cruza | gana a v143 | dif med vs v143 | dif med vs ref | establecidos/9 | pasos viables/linaje | A+C/linaje | B+D/linaje | A+C en el mundo | frac sin bueno | vida hijo | causas h/s/v/s |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    v = M.get('v143', {}); rf = M.get('bb_ref', {})
    for b in ORDEN:
        if b not in M: continue
        x = M[b]; ss = sorted(x)
        dv = [x[s]['R0'] - v[s]['R0'] for s in ss if s in v]; dr = [x[s]['R0'] - rf[s]['R0'] for s in ss if s in rf]
        cz = {k: sum(x[s]['cz'][k] for s in ss) for k in ('hambre', 'sed', 'veneno', 'sal')}
        print(f"| {b} | {len(ss)} | **{med([x[s]['R0'] for s in ss])}** | {', '.join(f'{x[s]['R0']:.3f}' for s in ss)} | "
              f"{sum(1 for s in ss if x[s]['cruzan'] >= 5)}/{len(ss)} | {sum(1 for z in dv if z > 0)}/{len(dv)} | {med(dv) if dv else ''} | {med(dr) if dr else ''} | {med([x[s]['est'] for s in ss])} | "
              f"{med([x[s]['viab'] for s in ss])} | {med([x[s]['ac'] for s in ss])} | {med([x[s]['bd'] for s in ss])} | {med([x[s]['buenos_mundo'] for s in ss])} | "
              f"{med([x[s]['sinbueno'] for s in ss])} | {med([x[s]['vh'] for s in ss])} | {cz['hambre']}/{cz['sed']}/{cz['veneno']}/{cz['sal']} |")
    print("\n## Telemetria bbt (ultima instancia de cada linaje; decision CRUDA de O1 contra V143 sobre letras no malas; no puntua)")
    for b in ORDEN:
        if b not in R or b == 'v143': continue
        tot = {}
        for d in R[b].values():
            for t in d['tel']:
                for k, val in t['bbt'].items(): tot[k] = tot.get(k, 0) + val
        bd = max(tot['bue_dec'], 1)
        print(f"- {b}: conocidas {tot['bue_dec']} · O1 veta {tot['bue_veto']} ({tot['bue_veto']/bd:.0%}; rel {tot['bue_veto_rel']} / no rel {tot['bue_veto_norel']}) · "
              f"O1 fuerza {tot['bue_fuerza']} ({tot['bue_fuerza']/bd:.0%}; bajo U {tot['bue_fuerza_bajoU']} / en margen {tot['bue_fuerza_margen']}; "
              f"V143 lo tenia en FILTRO {tot['bue_fuerza_filtro']}; no sirve a la activa {tot['bue_fuerza_nosirve_act']}) · "
              f"desconocidas {tot['desc_dec']} (veta {tot['desc_veto']}, fuerza {tot['desc_fuerza']}) · mordidas finales buenas {tot['mord_final_bue']}")
    return 0


if __name__ == '__main__':
    main()
