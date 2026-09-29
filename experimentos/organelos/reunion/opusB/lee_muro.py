"""lee_muro.py — resume la PRUEBA DEL MURO EXPLORATORIA de Opus B (T 100k; datos/c*_T25000_*/muro_T100000/muro_s<s>_<brazo>.json).
Por brazo: R0 real (mediana por semilla de la mediana de 9 linajes), semillas con mayoria (>= 5/9 cruza_real), linajes que cruzan,
fundadores por linaje (media de 9 y mediana de 9), linajes establecidos (0 fundadores tras 10k). Pareados por semilla (R0 mediano).
Solo semillas COMPLETAS para cada par. EXPLORATORIO: no es la letra (n < 20, sin preregistro confirmatorio).
    python .../lee_muro.py
"""
import glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__))
R = {}
for f in glob.glob(os.path.join(AQUI, 'datos', 'c*_T25000_*', 'muro_T100000', 'muro_s*_*.json')):
    x = json.load(open(f, encoding='utf-8')); R.setdefault(x['brazo'], {})[x['seed']] = x
ORD = ['pas', 'pasg', 'eco', 'ctl', 'v143', 'termo', 'o1']
print("brazo | semillas | R0 real (mediana) | mayorias | linajes que cruzan | fund/linaje media (mediana de semillas) | fund mediana | establecidos (mediana)")
for b in [z for z in ORD if z in R]:
    X = list(R[b].values())
    print(f"{b:5s} | {len(X):2d} | {round(st.median(x['R0_med'] for x in X), 3)} | {sum(x['mayoria'] for x in X)}/{len(X)} | "
          f"{sum(x['cruzan'] for x in X)}/{9*len(X)} | {round(st.median(st.mean(x['fund']) for x in X), 1)} | "
          f"{st.median(st.median(x['fund']) for x in X)} | {st.median(sum(1 for z in x['fund_post10k'] if z == 0) for x in X)}")
print("\nPAREADOS (R0 mediano por semilla; gana = semillas en que el primero supera al segundo; dif = mediana de diferencias)")
for a, b in (('pas', 'ctl'), ('pas', 'v143'), ('pas', 'termo'), ('pas', 'o1'), ('pasg', 'ctl'), ('pas', 'pasg'), ('eco', 'ctl'), ('eco', 'pas'),
             ('termo', 'v143'), ('o1', 'v143')):
    if a in R and b in R:
        S = sorted(set(R[a]) & set(R[b]))
        if S:
            d = [R[a][s]['R0_med'] - R[b][s]['R0_med'] for s in S]
            fa = [st.mean(R[a][s]['fund']) - st.mean(R[b][s]['fund']) for s in S]
            print(f"  {a} vs {b}: gana {sum(1 for z in d if z > 0)}/{len(S)} · dif R0 {round(st.median(d), 3)} · "
                  f"dif fundadores/linaje (media) {round(st.median(fa), 1)} · semillas {S[0]}-{S[-1]}")
print("\nPOR SEMILLA (R0 mediano / linajes que cruzan):")
for s in sorted({s for b in R for s in R[b]}):
    print(f"  s{s}: " + " · ".join(f"{b} {R[b][s]['R0_med']}/{R[b][s]['cruzan']}" for b in ORD if b in R and s in R[b]))
