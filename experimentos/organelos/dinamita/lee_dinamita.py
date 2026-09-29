"""lee_dinamita.py — tabla del EXPLORATORIO DINAMITA (datos/explora/*.json). EXPLORATORIO, no es dato.
Por brazo: semillas, mediana del R0 real, P1 = semillas con MAYORIA de linajes que cruzan (cruza_real, ENMIENDA 5), linajes que cruzan,
clases de los que no cruzan (ESTAB_bajo = 0 fundadores tras 10k pero R0 < 0.90; cae/nunca = fundadores tras 10k), hijos muertos en <= 200
pasos, hijos que paren, fundadores por linaje, mordidas B+D y A+C por linaje, composicion del mundo; pareado contra termo (mismas semillas).

    python experimentos/organelos/dinamita/lee_dinamita.py [--desde 39201 --hasta 39230] [--brazos termo,vu,...]
"""
import argparse, glob, json, os, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))


def med(x):
    x = [v for v in x if v is not None]
    return round(st.median(x), 3) if x else None


def carga(desde, hasta):
    R = {}
    for f in glob.glob(os.path.join(AQUI, 'datos', 'explora', '*_T100000.json')):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto') or not (desde <= d['seed'] <= hasta): continue
        R.setdefault(d['brazo'], {})[d['seed']] = d
    return R


def fila(D):
    L = [l for d in D.values() for l in d['linajes']]
    sem = sum(1 for d in D.values() if sum(l['cruza_real'] for l in d['linajes']) * 2 > len(d['linajes']))
    cl = dict(cruza=0, bajo=0, cae=0)
    h200 = hn = hp = 0
    for l in L:
        cl['cruza' if l['cruza_real'] else ('cae' if l['fund_post10k'] > 0 else 'bajo')] += 1
        t = l['telem']
        for i in range(len(t['vidas']) - 1):
            if t['origen'][i] == 1:
                hn += 1; h200 += int(t['vidas'][i] <= 201); hp += int(t['desc_por_vida'][i] > 0)
    comp = [d['pista']['comp_mundo'] for d in D.values()]
    ac = med([sum(c[k] for k in 'AC') for c in comp])
    tel = [t.get('veto') or t.get('patas') or {} for d in D.values() for t in (d.get('tel_dinamita') or [])]
    return dict(n=len(D), R0=med([l['R0_real'] for l in L]), P1=sem, cruzan=cl['cruza'], bajo=cl['bajo'], cae=cl['cae'], lin=len(L),
                h200=(round(h200 / hn, 3) if hn else None), hpare=(round(hp / hn, 3) if hn else None), F=med([l['fundadores'] for l in L]),
                BD=med([l['mord']['B'] + l['mord']['D'] for l in L]), AC=med([l['mord']['A'] + l['mord']['C'] for l in L]), mundoAC=ac,
                a_no=sum(t.get('a_no', 0) + t.get('a_si', 0) + t.get('cambia', 0) for t in tel), por_sem=sorted(sum(l['cruza_real'] for l in d['linajes']) for d in D.values()))


def pareado(A, B):
    com = sorted(set(A) & set(B))
    ma = {s: st.median([l['R0_real'] for l in A[s]['linajes']]) for s in com}
    mb = {s: st.median([l['R0_real'] for l in B[s]['linajes']]) for s in com}
    d = [ma[s] - mb[s] for s in com]
    ca = {s: sum(l['cruza_real'] for l in A[s]['linajes']) for s in com}; cb = {s: sum(l['cruza_real'] for l in B[s]['linajes']) for s in com}
    return dict(n=len(com), gana=sum(1 for x in d if x > 0), dif=(round(st.median(d), 4) if d else None),
                mas_cruzan=sum(1 for s in com if ca[s] > cb[s]), menos=sum(1 for s in com if ca[s] < cb[s]))


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--desde', type=int, default=39201); ap.add_argument('--hasta', type=int, default=39230)
    ap.add_argument('--brazos', default=None)
    a = ap.parse_args()
    R = carga(a.desde, a.hasta)
    orden = [b for b in (a.brazos.split(',') if a.brazos else ['termo', 'vu', 'vh', 'vnav', 'vw', 'vuinv', 'lu', 'lh', 'luinv', 'pd', 'pu', 'pc', 'pi', 'o1', 'v143']) if b in R]
    print(f"EXPLORATORIO DINAMITA · semillas {a.desde}-{a.hasta} · T 100000 · (P1 = semillas con mayoria de linajes que cruzan)")
    print(f"{'brazo':6s} {'n':>3s} {'R0 med':>7s} {'P1':>7s} {'cruzan':>10s} {'bajo':>5s} {'cae':>5s} {'hijos<=200':>10s} {'hijos paren':>11s} "
          f"{'F med':>6s} {'B+D':>6s} {'A+C':>6s} {'mundo A+C':>9s} {'a_no':>7s} | vs termo: gana / dif / +cruz -cruz")
    for b in orden:
        f = fila(R[b]); p = pareado(R[b], R['termo']) if 'termo' in R and b != 'termo' else None
        ps = f"{p['gana']}/{p['n']} {p['dif']:+.3f} +{p['mas_cruzan']} -{p['menos']}" if p else ''
        print(f"{b:6s} {f['n']:3d} {f['R0']!s:>7s} {str(f['P1']) + '/' + str(f['n']):>7s} {str(f['cruzan']) + '/' + str(f['lin']):>10s} {f['bajo']:5d} "
              f"{f['cae']:5d} {f['h200']!s:>10s} {f['hpare']!s:>11s} {f['F']!s:>6s} {f['BD']!s:>6s} {f['AC']!s:>6s} {f['mundoAC']!s:>9s} {f['a_no']:7d} | {ps}")
        print(f"{'':6s}     linajes que cruzan por semilla (ordenado): {f['por_sem']}")


if __name__ == '__main__':
    main()
