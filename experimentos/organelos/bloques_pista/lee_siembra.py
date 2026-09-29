"""lee_siembra.py — SOLO LECTURA: tipo de regla mas frecuente en los bancos por pasaje (fraccion de listas que lo contienen) y en los vivos."""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from corre_bp import regla_txt
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos', 'pasajes_Tp100000_np3_sp59410')
for f in sorted(glob.glob(os.path.join(D, '*.json'))):
    x = json.load(open(f, encoding='utf-8')); L = [R for B in x['bq']['banco'].values() for R in B if R]
    cnt = {}
    for R in L:
        for k in {(int(r[0]), int(r[1]), int(r[2] > 0.5), int(r[4]), (1 if r[5] > 0 else -1)) for r in R}: cnt[k] = cnt.get(k, 0) + 1
    top = sorted(cnt.items(), key=lambda z: -z[1])[:2]
    fund = sorted(l['fundadores'] for l in x['linajes'])
    print(os.path.basename(f)[:-5], f"listas {len(L)}", ' ; '.join(f"{v / max(1, len(L)):.2f} {regla_txt([k[0], k[1], k[2], 0.5, k[3], 1.0 * k[4]]).rsplit(' ', 1)[0]}{'+' if k[4] > 0 else '-'}" for k, v in top),
          f"· fund mediana {fund[4]}")
