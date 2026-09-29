"""tabla_pasajes.py — tabla por pasaje (medianas sobre semillas) de datos/pas_*_T50000/RESUMEN.json. Solo lee. Escribe tabla_pasajes.json."""
import glob, json, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
T = int(sys.argv[1]) if len(sys.argv) > 1 else 50000
GRUPO = sys.argv[2] if len(sys.argv) > 2 else 'todo'   # serie (47801-05) | replica (47811-15) | todo
BR = ('PAS_F1', 'PAS_SEL', 'PAS_RES', 'PAS_AZA', 'PAS_SELM')
D = {}
for p in glob.glob(os.path.join(AQUI, 'datos', f'pas_*_T{T}', 'RESUMEN.json')):
    R = json.load(open(p, encoding='utf-8'))
    for f in R['filas']: D[(R['brazo'], R['s'], f['p'])] = f
S = sorted({k[1] for k in D if GRUPO == 'todo' or (GRUPO == 'serie' and k[1] <= 47808) or (GRUPO == 'replica' and k[1] >= 47811)}); P = sorted({k[2] for k in D})
md = lambda v: (round(float(np.median(v)), 3) if v else None)
out = {}
print(f"T_p {T}; semillas {S}. REP = fundadores repuestos en todo el pasaje; r_rep = REP/REP(F1) - 1; r = lo mismo con fund_2a ([T_p/2, T_p]); medianas; n = semillas con dato")
for b in BR:
    print(f"== {b}")
    for p in P:
        fs = [(s, D[(b, s, p)]) for s in S if (b, s, p) in D]
        if not fs: continue
        r = [f['fund_2a'] / D[('PAS_F1', s, p)]['fund_2a'] - 1 for s, f in fs if ('PAS_F1', s, p) in D]
        rr = [f['fundadores_rep'] / D[('PAS_F1', s, p)]['fundadores_rep'] - 1 for s, f in fs if ('PAS_F1', s, p) in D]
        vsrep = (sum(1 for s, f in fs if ('PAS_RES', s, p) in D and f['fundadores_rep'] < D[('PAS_RES', s, p)]['fundadores_rep']),
                 sum(1 for s, f in fs if ('PAS_RES', s, p) in D))
        g = lambda k: md([f['genes'].get(k) for s, f in fs if f['genes'] and f['genes'].get(k) is not None])
        vsres = (sum(1 for s, f in fs if ('PAS_RES', s, p) in D and f['fund_2a'] < D[('PAS_RES', s, p)]['fund_2a']),
                 sum(1 for s, f in fs if ('PAS_RES', s, p) in D))
        fila = dict(n=len(fs), r_rep=md(rr), rep=md([f['fundadores_rep'] for s, f in fs]), rep_menor_que_RES=vsrep, r=md(r), r_min=(round(min(r), 3) if r else None), r_max=(round(max(r), 3) if r else None),
                    fund_2a=md([f['fund_2a'] for s, f in fs]), K=md([f['K'] for s, f in fs]), K_nac=md([f['K_nac'] for s, f in fs]),
                    alpha=g('alpha'), aversion=g('aversion'), tau_e=g('tau_e'), eta_s=g('eta_s'), NK=g('NK'), rep_umbral=g('rep_umbral'),
                    menor_que_RES=vsres, persiste=sum(int(f['persiste'] or 0) for s, f in fs))
        out[f"{b}_p{p}"] = fila
        print(f"  p{p:2d} n{fila['n']}: REP(pasaje entero) {fila['rep']} r_rep {fila['r_rep']} <RES {vsrep[0]}/{vsrep[1]} | 2a mitad: r {fila['r']} [{fila['r_min']}, {fila['r_max']}] · fund_2a {fila['fund_2a']} · K {fila['K']} · K_nac {fila['K_nac']} · "
              f"alpha {fila['alpha']} · aversion {fila['aversion']} · tau_e {fila['tau_e']} · rep_umbral {fila['rep_umbral']} · <RES {vsres[0]}/{vsres[1]}")
json.dump(out, open(os.path.join(AQUI, f'tabla_pasajes_T{T}.json'), 'w', encoding='utf-8'), indent=1)

# acumulado (mismo presupuesto que la corrida larga: 20 x 50 000 = 1e6): sum REP / sum REP(F1) - 1 por semilla, en p1..pN
print("== ACUMULADO: sum(REP) / sum(REP F1) - 1 por semilla (solo semillas con los N pasajes en brazo y F1)")
acum = {}
for b in BR[1:]:
    for N_ in (8, 20):
        v = []
        for s in S:
            if all((b, s, p) in D and ('PAS_F1', s, p) in D for p in range(1, N_ + 1)):
                v.append(sum(D[(b, s, p)]['fundadores_rep'] for p in range(1, N_ + 1)) / sum(D[('PAS_F1', s, p)]['fundadores_rep'] for p in range(1, N_ + 1)) - 1)
        acum[f"{b}_{N_}"] = dict(n=len(v), mediana=md(v), por_semilla=[round(x, 3) for x in v])
        print(f"  {b} p1..p{N_}: n {len(v)} · mediana {md(v)} · {[round(x, 3) for x in v]}")
# tendencia entre pasajes: por semilla, media de r_rep en p16-p20 menos media en p1-p5 (negativo = bajan los fundadores con los pasajes)
print("== TENDENCIA: por semilla, media r_rep(p16..p20) - media r_rep(p1..p5)  (y p2..p5 para no contar el p1 compartido)")
tend = {}
for b in BR[1:]:
    v = []; v2 = []
    for s in S:
        rr_ = {p: D[(b, s, p)]['fundadores_rep'] / D[('PAS_F1', s, p)]['fundadores_rep'] - 1 for p in range(1, 21) if (b, s, p) in D and ('PAS_F1', s, p) in D}
        if all(p in rr_ for p in range(1, 21)):
            v.append(np.mean([rr_[p] for p in range(16, 21)]) - np.mean([rr_[p] for p in range(1, 6)]))
            v2.append(np.mean([rr_[p] for p in range(16, 21)]) - np.mean([rr_[p] for p in range(2, 6)]))
    tend[b] = dict(n=len(v), baja=sum(1 for x in v if x < 0), d=[round(float(x), 3) for x in v], baja_p2=sum(1 for x in v2 if x < 0), d_p2=[round(float(x), 3) for x in v2])
    print(f"  {b}: n {len(v)} · bajan {tend[b]['baja']}/{len(v)} · {tend[b]['d']} | contra p2..p5: bajan {tend[b]['baja_p2']}/{len(v)} · {tend[b]['d_p2']}")
json.dump(dict(grupo=GRUPO, semillas=S, tabla=out, acumulado=acum, tendencia=tend), open(os.path.join(AQUI, f'tabla_pasajes_T{T}_{GRUPO}.json'), 'w', encoding='utf-8'), indent=1)
