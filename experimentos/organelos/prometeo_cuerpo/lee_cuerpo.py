# EXPLORATORIO, no es dato
"""lee_cuerpo.py — lectura DESCRIPTIVA de PROMETEO-CUERPO (nada decide). MISION: llegar a la AGI por este camino.
Uso: python lee_cuerpo.py [--tl largo] [--cal 1]
"""
import argparse, glob, json, os, sys
from collections import Counter
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); ORG = os.path.dirname(AQUI)
for d in (os.path.join(ORG, 'codigo', 'exploracion_fable'), os.path.join(ORG, 'codigo'), AQUI): sys.path.insert(0, d)
import codigo_cuerpo as CQ
DATOS = os.path.join(AQUI, 'datos')
P = CQ.PARTES; BR = ('CUERPO', 'CUERPO_MUDO', 'PROMETEO'); MU = ('quieto', 'onda8k', 'veneno', 'niebla')


def carga(tl):
    R = {}
    for m in MU:
        for f in sorted(glob.glob(os.path.join(DATOS, f"{m}_{tl}", '*_s*.json'))):
            x = json.load(open(f, encoding='utf-8'))
            if x.get('abortado'): print('ABORTADA', f, x['abortado'])
            R[(m, x['brazo'], x['seed'])] = x
    return R


def fr(x, cual, j):
    b = ((x.get('cuerpo') or {}).get(cual) or {})
    return None if not b.get('frac') else b['frac'][j]


def fija(x, j):
    a = fr(x, 'banco_corte', j); b = fr(x, 'banco_final', j)
    return int((a or 0) >= 0.5 or (b or 0) >= 0.5)


def nfin(x): return x.get('n_final') or 0


def med(v):
    v = [z for z in v if z is not None]
    return None if not v else round(float(np.median(v)), 3)


def pareado(R, m, a, b, f, sems):
    w = n = 0
    for s in sems:
        if (m, a, s) in R and (m, b, s) in R: n += 1; w += int(f(R[(m, a, s)]) > f(R[(m, b, s)]))
    return f"{w}/{n}"


def lee(tl):
    R = carga(tl); L = []
    sems = sorted(set(k[2] for k in R))
    L.append(f"corridas: {len(R)} · semillas {sems}")
    for m in MU:
        if not any(k[0] == m for k in R): continue
        L.append(f"\n=== {m} ===")
        for b in BR:
            xs = [R[(m, b, s)] for s in sems if (m, b, s) in R]
            if not xs: continue
            pers = sum(int(x.get('persiste', 0)) for x in xs)
            nf = [nfin(x) for x in xs]
            lg = med([((x.get('cuerpo') or {}).get('banco_final') or {}).get('largo') for x in xs])
            lc = med([((x.get('cuerpo') or {}).get('banco_corte') or {}).get('largo') for x in xs])
            L.append(f"{b:<12} n {len(xs)} · persiste {pers}/{len(xs)} · nac solo suma {sum(nf)} mediana {med(nf)} · R0 final med {med([x.get('r0_final') for x in xs])} "
                     f"· n_nac med {med([x.get('n_nac') for x in xs])} · largo banco corte {lc} final {lg}")
            if b != 'PROMETEO':
                for j, p in enumerate(P):
                    fc = [fr(x, 'banco_corte', j) for x in xs]; ff = [fr(x, 'banco_final', j) for x in xs]
                    fx = sum(fija(x, j) for x in xs)
                    mx = max([v for v in fc + ff if v is not None] or [0])
                    L.append(f"   {p:<10} fijada (>=0.5 corte o final) {fx}/{len(xs)} · frac banco corte med {med(fc)} · final med {med(ff)} · max {mx}")
                alg = sum(int(any(fija(x, j) for j in range(len(P)))) for x in xs)
                L.append(f"   ALGUNA parte fijada en {alg}/{len(xs)} corridas")
                cs = [((x.get('cuerpo') or {}).get('cont') or {}) for x in xs]
                L.append("   contadores (mediana): " + ', '.join(f"{k} {med([c.get(k, 0) for c in cs])}" for k in ('pata', 'escudo', 'estomago', 'mandibula', 'lengua', 'costo', 'ciego', 've')))
        L.append(f"pareado (nac solo): CUERPO > PROMETEO {pareado(R, m, 'CUERPO', 'PROMETEO', nfin, sems)} · CUERPO > MUDO {pareado(R, m, 'CUERPO', 'CUERPO_MUDO', nfin, sems)} · "
                 f"MUDO > PROMETEO {pareado(R, m, 'CUERPO_MUDO', 'PROMETEO', nfin, sems)} · PROMETEO > MUDO {pareado(R, m, 'PROMETEO', 'CUERPO_MUDO', nfin, sems)}")
        for j, p in enumerate(P):
            f = lambda x, j=j: max(fr(x, 'banco_corte', j) or 0, fr(x, 'banco_final', j) or 0)
            L.append(f"   {p:<10} frac max(corte, final): CUERPO > MUDO {pareado(R, m, 'CUERPO', 'CUERPO_MUDO', f, sems)}")
    # donde sirve: escudo / lengua en veneno vs quieto (CUERPO, pareado por semilla)
    L.append("\n=== donde sirve (CUERPO, pareado por semilla) ===")
    for p in ('ESCUDO', 'LENGUA', 'OJO', 'ESTOMAGO', 'PATA', 'MANDIBULA'):
        j = P.index(p)
        for m2 in ('veneno', 'niebla', 'onda8k'):
            w = n = 0
            for s in sems:
                a = R.get((m2, 'CUERPO', s)); q = R.get(('quieto', 'CUERPO', s))
                if a and q:
                    n += 1; w += int(max(fr(a, 'banco_corte', j) or 0, fr(a, 'banco_final', j) or 0) > max(fr(q, 'banco_corte', j) or 0, fr(q, 'banco_final', j) or 0))
            if n: L.append(f"   {p:<10} {m2} > quieto: {w}/{n}")
    # bichos: por mundo, la corrida de CUERPO con mas nacimientos solos y su cinta mas comun en el banco final
    L.append("\n=== bichos (CUERPO: la corrida con mas nacimientos solos por mundo; cinta modal del banco final) ===")
    for m in MU:
        xs = [R[(m, 'CUERPO', s)] for s in sems if (m, 'CUERPO', s) in R]
        if not xs: continue
        for x in sorted(xs, key=nfin, reverse=True)[:2]:
            bf = (x.get('prometeo') or {}).get('banco_final') or []
            cnt = Counter(tuple(tuple(i) for i in c) for c in bf)
            L.append(f"-- {m} s{x['seed']}: nac solo {nfin(x)} · persiste {x.get('persiste')} · vivos {x.get('vivos_T')} · n_nac {x.get('n_nac')} · R0 final {x.get('r0_final')}")
            L.append(f"   banco corte {((x['cuerpo'] or {}).get('banco_corte') or {})}")
            L.append(f"   banco final {((x['cuerpo'] or {}).get('banco_final') or {})}")
            L.append(f"   vivos final {((x['cuerpo'] or {}).get('vivos_final') or {})}")
            nv = (x['cuerpo'] or {}).get('nac_ventanas') or []
            L.append("   nacidos por ventana de 2000 [t, n, frac " + '/'.join(p[:4] for p in P) + "]: " + ' '.join(str(v) for v in nv[::2]))
            L.append(f"   kit {((x.get('prometeo') or {}).get('kit') or {})}")
            for c, k in cnt.most_common(2):
                L.append(f"   cinta x{k}/{len(bf)} (largo {len(c)}): {CQ.texto(c)}")
    return L


def lee_cal(ronda):
    L = []
    for f in sorted(glob.glob(os.path.join(DATOS, f"cal_r{ronda}", '*_s*.json'))):
        x = json.load(open(f, encoding='utf-8'))
        p = x['brazo'].split('_')[0]; j = P.index(p)
        bf = ((x.get('cuerpo') or {}).get('banco_final') or {})
        L.append(f"{x['brazo']:<26} s{x['seed']}: banco final con {p}: {None if not bf.get('frac') else bf['frac'][j]} · n_nac {x.get('n_nac')} · persiste {x.get('persiste')} · cont {(x.get('cuerpo') or {}).get('cont')}")
    return L


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--tl', default='largo'); ap.add_argument('--cal', type=int, default=0)
    a = ap.parse_args()
    L = lee_cal(a.cal) if a.cal else lee(a.tl)
    out = os.path.join(DATOS, (f"CAL_r{a.cal}.txt" if a.cal else f"LECTURA_{a.tl}.txt"))
    open(out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))
