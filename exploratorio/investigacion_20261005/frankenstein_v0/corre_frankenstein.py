# -*- coding: utf-8 -*-
"""Corre el Frankenstein v0. Un proceso (más el servidor del cuerpo, hijo suyo, 4 hilos). Sin Pool.
  python -B corre_frankenstein.py --humo                 (semilla 0 de calibración, 12 preguntas; escribe datos/humo.json)
  python -B corre_frankenstein.py --semillas 21,22,23    (la prueba preregistrada; escribe datos/principal.json y .md)
"""
import argparse
import json
import os
import statistics
import time

import frank
from cuerpo import Cuerpo, AQUI

ap = argparse.ArgumentParser()
ap.add_argument("--humo", action="store_true")
ap.add_argument("--semillas", default="21,22,23")
ap.add_argument("--out", default=None)
ap.add_argument("--verboso", action="store_true")
ap.add_argument("--cache", default=None)
a = ap.parse_args()
sems = [0] if a.humo else [int(x) for x in a.semillas.split(",")]
out = a.out or os.path.join(AQUI, "datos", "humo.json" if a.humo else "principal.json")
# la caché de la prueba es propia: los tiempos son de primera llamada
cache = a.cache or os.path.join(AQUI, "datos", "cache_cuerpo.jsonl" if a.humo else "cache_prueba.jsonl")
t0 = time.time()
res = []
with Cuerpo(cache=cache) as c:
    for s in sems:
        r = frank.corre_semilla(c, s, n_preg=12 if a.humo else None, verboso=a.verboso or a.humo)
        r["resumen"] = {b: frank.resume(r["filas"], b) for b in frank.BRAZOS}
        res.append(r)
        print(f"semilla {s}: extracción {r['extraccion']}, colonia {r['colonia']}, {time.time() - t0:.0f} s")
    llamadas, de_cache = c.n_llamadas, c.n_cache
campos = ["acierto_nuevos", "acierto_ensenados", "mentiras_afirmadas", "n_mentiras", "acierto_control", "escala",
          "escala_control", "otro_error_NN", "seg"]
tabla = {}
for b in frank.BRAZOS:
    tabla[b] = {k: [r["resumen"][b][k] for r in res] for k in res[0]["resumen"][b]}
lin = ["| brazo | " + " | ".join(campos) + " |", "|---|" + "---|" * len(campos)]
for b in frank.BRAZOS:
    lin.append(f"| {b} | " + " | ".join(
        f"{statistics.median(tabla[b][k]):.2f} [{min(tabla[b][k]):.2f}–{max(tabla[b][k]):.2f}]" for k in campos) + " |")
cl = frank.NUEVAS + frank.CONTROL
lin += ["", "Por clase (media de semillas): acierto / mentira afirmada / escala", "| brazo | " + " | ".join(cl) + " |",
        "|---|" + "---|" * len(cl)]
for b in frank.BRAZOS:
    lin.append(f"| {b} | " + " | ".join(
        "/".join(f"{statistics.mean(tabla[b][p + '_' + k]):.2f}" for p in ("ac", "me", "es")) for k in cl) + " |")
md = "\n".join(lin)
print(md)
json.dump({"semillas": sems, "humo": a.humo, "resultados": res, "tabla": tabla, "seg_total": time.time() - t0,
           "llamadas": llamadas, "de_cache": de_cache,
           "perillas": {"K": 2, "UMBRAL_Q": frank.UMBRAL_Q, "TAU": frank.TAU, "sistema": frank.SISTEMA}},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=list)
open(out.replace(".json", ".md"), "w", encoding="utf-8").write(md + "\n")
print("escrito", out, f"{time.time() - t0:.0f} s; llamadas {llamadas} (de caché {de_cache})")
