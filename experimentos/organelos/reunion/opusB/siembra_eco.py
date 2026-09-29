"""siembra_eco.py — convierte los genomas ECO del ultimo pasaje de Opus A (PAS_SEL, 90 x 18) en una SIEMBRA de la pista (Opus B).
Toma SOLO los 15 genes del cerebro (los de eco_a_carrera; la historia de vida dote/rep_umbral/rep_X no existe en el carro de la pista).
g (margen del termostato, no existe en ECO) ~ U[-0.1, 0.1] (la inicial de EVO_BAJO) con rng default_rng([58300, s]) fijo.
Valores de genes, como en eco_a_carrera; EXPLORATORIO.
    python .../siembra_eco.py <genomas_ultimo_PAS_SEL_s<s>.json> <salida.json>
"""
import json, sys
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import construye_pas as CB
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding='utf-8'))
idx = [d['genes'].index(k) for k in CB.GENES]
r = np.random.default_rng([58300, int(d['s'])])
S = [dict(g=float(r.uniform(-0.1, 0.1)), b={k: float(gen[i]) for k, i in zip(CB.GENES, idx)}) for gen in d['genomas']]
json.dump(S, open(out, 'w', encoding='utf-8'))
print(f"{src} -> {out}: {len(S)} genomas (15 genes del cerebro + g U[-0.1,0.1])")
