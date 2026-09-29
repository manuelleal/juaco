"""lee_juguete.py — lee juguete_*.json: por indice de pasaje, mediana sobre semillas de K, K_nac, fund_2a y genes, SEL contra RES (pareado)."""
import json, sys, numpy as np
for fn in sys.argv[1:]:
    d = json.load(open(fn)); C = d['cadenas']; npas = d['npas']
    seeds = sorted({int(k.split('_s')[1]) for k in C})
    print(f"== {fn}: T_p {d['Tp']} · {npas} pasajes · semillas {seeds}")
    print("pas | K SEL / RES (SEL>RES n/N) | K_nac SEL / RES | fund_2a SEL / RES (SEL<RES) | alpha SEL/RES | tau_e SEL/RES | dist_G0 SEL/RES")
    for p in range(npas):
        row = {}
        for b in ('SEL', 'RES'):
            fs = [C[f"{b}_s{s}"][p] for s in seeds if f"{b}_s{s}" in C and len(C[f"{b}_s{s}"]) > p]
            row[b] = fs
        n = min(len(row['SEL']), len(row['RES']))
        if n == 0: break
        S, R = row['SEL'][:n], row['RES'][:n]
        med = lambda L, k: round(float(np.median([x[k] for x in L])), 2)
        gm = lambda L, g: round(float(np.median([x['genes'][g] for x in L])), 3)
        kw = sum(1 for a, b in zip(S, R) if a['K'] > b['K']); fw = sum(1 for a, b in zip(S, R) if a['fund_2a'] < b['fund_2a'])
        print(f"{p:3d} | {med(S,'K')} / {med(R,'K')} ({kw}/{n}) | {med(S,'K_nac')} / {med(R,'K_nac')} | {med(S,'fund_2a')} / {med(R,'fund_2a')} ({fw}/{n}) | "
              f"{gm(S,'alpha')}/{gm(R,'alpha')} | {gm(S,'tau_e')}/{gm(R,'tau_e')} | {med(S,'dist_G0')}/{med(R,'dist_G0')}")
