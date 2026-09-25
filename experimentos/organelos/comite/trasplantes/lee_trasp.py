"""lee_trasp.py — EXPLORATORIO, no es dato. Lee datos/*.json y arma: tabla por brazo (mediana sobre semillas de la mediana por semilla del
R0 real de los 9 linajes; cruzan/persisten; vida; fundadores; causas; fundadores contra hijos), pareado contra v143 y contra O1 con la
MISMA semilla, y la regla de parada (R0 real >= 0.85 en >= 3/5 semillas). python lee_trasp.py [--T 100000] [--md]"""
import argparse, glob, json, os, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__)); DATOS = os.path.join(AQUI, 'datos')


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 3) if xs else None


def carga(T):
    R = {}
    for f in glob.glob(os.path.join(DATOS, f"*_T{T}.json")):
        d = json.load(open(f, encoding='utf-8')); R.setdefault(d['brazo'], {})[d['seed']] = d
    return R


def fund_hijos(corridas):
    vf, vh, hf, hh = [], [], [], []; cf = {}; ch = {}
    for c in corridas:
        for l in c['linajes']:
            te = l['telem']; v = te['vidas']; o = te['origen']; cc = te['causa_cuerpo']; dpv = te['desc_por_vida']
            for i in range(len(v) - 1):
                (vh if o[i] else vf).append(v[i]); (hh if o[i] else hf).append(dpv[i])
                dct = ch if o[i] else cf; k = cc[i] if i < len(cc) else '?'; dct[k] = dct.get(k, 0) + 1
    f = lambda v, h: dict(n=len(v), vida=med(v), sin_parir=(round(sum(1 for x in h if x == 0) / len(h), 3) if h else None), hijos_med=med(h))
    return dict(fund=f(vf, hf), hijos=f(vh, hh), causa_fund=cf, causa_hijos=ch)


def resumen(corridas):
    todos = [l for c in corridas for l in c['linajes']]
    por_sem = {c['seed']: med([l['R0_real'] for l in c['linajes']]) for c in corridas}
    cz = {k: sum(l['causas'][k] for l in todos) for k in ('hambre', 'sed', 'veneno', 'sal')}
    tot = max(1, sum(cz.values()))
    return dict(n_sem=len(corridas), R0_med=med(list(por_sem.values())), por_sem=por_sem, R0_lin_med=med([l['R0_real'] for l in todos]),
                cruzan=sum(l['cruza_real'] for l in todos), lin=len(todos), sem_mayoria=sum(1 for c in corridas if sum(l['cruza_real'] for l in c['linajes']) * 2 > 9),
                sem_085=sum(1 for v in por_sem.values() if v is not None and v >= 0.85), sem_090=sum(1 for v in por_sem.values() if v is not None and v >= 0.90),
                persisten=sum(l['persiste'] for l in todos), casi_inm=sum(l['casi_inmortal'] for l in todos),
                vida=med([l['vida_med'] for l in todos]), muertes=med([l['muertes'] for l in todos]), fund=med([l['fundadores'] for l in todos]),
                fund_post=med([l['fund_post10k'] for l in todos]), nac=med([l['nac_reales'] for l in todos]),
                BD=round((cz['veneno'] + cz['sal']) / tot, 3), causas=cz, mordBD=med([l['mord']['B'] + l['mord']['D'] for l in todos]),
                mordAC=med([l['mord']['A'] + l['mord']['C'] for l in todos]), sin_bueno=med([c['pista']['frac_sin_bueno_mundo'] for c in corridas]),
                coherente=sum(l['coherente'] for l in todos), seg=med([c['seg'] for c in corridas]))


def pareado(A, B):
    ss = sorted(set(A) & set(B))
    d = [med([l['R0_real'] for l in A[s]['linajes']]) - med([l['R0_real'] for l in B[s]['linajes']]) for s in ss]
    return dict(n=len(ss), gana=sum(1 for x in d if x > 0), dif_med=med(d), difs=[round(x, 3) for x in d])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--T', type=int, default=100000); ap.add_argument('--md', action='store_true')
    a = ap.parse_args(); R = carga(a.T)
    res = {b: resumen(list(c.values())) for b, c in R.items()}
    orden = sorted(res, key=lambda b: -(res[b]['R0_med'] or 0))
    sep = ' | ' if a.md else '  '
    hdr = ['brazo', 'sem', 'R0 real med', 'por semilla', 'sem>=.85', 'cruzan', 'sem may', 'persist', 'vida', 'muert', 'fund', 'nac', 'B+D causa', 'fund: n/vida/sin parir', 'hijos: n/vida/sin parir/hijos', 'vs v143 gana/dif', 'vs o1 gana/dif']
    if a.md: print('| ' + ' | '.join(hdr) + ' |'); print('|' + '---|' * len(hdr))
    else: print('  '.join(hdr))
    for b in orden:
        r = res[b]; pv = pareado(R[b], R['v143']) if 'v143' in R and b != 'v143' else None; po = pareado(R[b], R['o1']) if 'o1' in R and b != 'o1' else None
        fila = [b, str(r['n_sem']), str(r['R0_med']), str([r['por_sem'][s] for s in sorted(r['por_sem'])]), f"{r['sem_085']}/{r['n_sem']}",
                f"{r['cruzan']}/{r['lin']}", f"{r['sem_mayoria']}/{r['n_sem']}", f"{r['persisten']}/{r['lin']}", str(r['vida']), str(r['muertes']), str(r['fund']), str(r['nac']),
                str(r['BD']), '', '', '', '']
        fh = fund_hijos(list(R[b].values()))
        fila[13] = f"{fh['fund']['n']}/{fh['fund']['vida']}/{fh['fund']['sin_parir']}"
        fila[14] = f"{fh['hijos']['n']}/{fh['hijos']['vida']}/{fh['hijos']['sin_parir']}/{fh['hijos']['hijos_med']}"
        fila[15] = f"{pv['gana']}/{pv['n']} {pv['dif_med']:+}" if pv and pv['n'] else '-'
        fila[16] = f"{po['gana']}/{po['n']} {po['dif_med']:+}" if po and po['n'] else '-'
        print(('| ' if a.md else '') + sep.join(fila) + (' |' if a.md else ''))
    print()
    for b in orden:
        r = res[b]; fh = fund_hijos(list(R[b].values()))
        print(f"{b:16s} causas h/s/v/sal {r['causas']['hambre']}/{r['causas']['sed']}/{r['causas']['veneno']}/{r['causas']['sal']} · fund causas {fh['causa_fund']} · hijos causas {fh['causa_hijos']} · "
              f"mord B+D {r['mordBD']} A+C {r['mordAC']} · sin bueno {r['sin_bueno']} · casi inm {r['casi_inm']} · fund>10k {r['fund_post']} · coherente {r['coherente']}/{r['lin']} · s {r['seg']}")
    print("\nREGLA DE PARADA (>= 0.85 en >= 3/5 semillas):", [b for b in orden if res[b]['sem_085'] >= 3 and res[b]['n_sem'] >= 5 and b != 'o1'] or 'ninguno')


if __name__ == '__main__':
    main()
