"""sensibilidad.py — que pasa cuando la celula SI pisa: sigma mas ancha (0.1, 0.2) y compuerta original (conf0=1) vs evidencia (0),
abrupto, C=50, 10 semillas, solo 'celula A'. Escribe datos/sensibilidad.json y datos/sensibilidad.md."""
import json, numpy as np, time
from deriva import corre, GENS

P0 = json.load(open('datos/validacion.json'))['P']; P0['cp'] = np.inf
confs = [(0.05, 0.0), (0.1, 0.0), (0.2, 0.0), (0.05, 1.0), (0.2, 1.0)]
out = {}; t0 = time.time(); lines = ["| sigma | compuerta | prueba | preq mediana [min-max] | post vuelta A | pisadas | mem fin |", "|---|---|---|---|---|---|---|"]
for sg, c0 in confs:
    P = dict(P0, sigma=sg, conf0=c0)
    for g in GENS:
        rs = [corre(g, s, 50, P, T=4000, solo='celula A')['celula A'] for s in range(1, 11)]
        out[f"{sg}|{c0}|{g}"] = rs
        pq = [r['preq'] for r in rs]; po = [r['post'][1] for r in rs]
        lines.append(f"| {sg} | {'evidencia' if c0 == 0 else 'original'} | {g} | {np.median(pq):.3f} [{min(pq):.3f}-{max(pq):.3f}] | {np.median(po):.2f} | {int(np.median([r['pisadas'] for r in rs]))} | {int(np.median([r['mem'] for r in rs]))} |")
        print(lines[-1], flush=True)
json.dump(out, open('datos/sensibilidad.json', 'w')); open('datos/sensibilidad.md', 'w', encoding='utf-8').write("\n".join(lines))
print(f"({time.time()-t0:.0f} s)")
