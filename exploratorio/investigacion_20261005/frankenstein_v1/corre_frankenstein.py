# -*- coding: utf-8 -*-
"""Corre el Frankenstein v1. Un proceso (más el servidor del cuerpo, hijo suyo, 4 hilos). Sin Pool.
  python -B corre_frankenstein.py --humo                   (semilla 0, plantillas A, 12 preguntas; escribe datos/humo.json)
  python -B corre_frankenstein.py --semillas 31,32,33      (prueba preregistrada, plantillas B; datos/principal.json y .md)
  python -B corre_frankenstein.py --semillas 31 --plantillas A --out datos/diag_A_s31.json   (diagnóstico declarado)
"""
import argparse
import json
import os
import statistics
import time

import frank
import mundo
from cuerpo import Cuerpo, AQUI

ap = argparse.ArgumentParser()
ap.add_argument("--humo", action="store_true")
ap.add_argument("--semillas", default="31,32,33")
ap.add_argument("--plantillas", default=None, help="A (calibración) o B (prueba). Por defecto: A en humo, B en prueba")
ap.add_argument("--out", default=None)
ap.add_argument("--verboso", action="store_true")
ap.add_argument("--cache", default=None)
ap.add_argument("--n_preg", type=int, default=None)
a = ap.parse_args()
sems = [0] if a.humo else [int(x) for x in a.semillas.split(",")]
plantillas = a.plantillas or ("A" if a.humo else "B")
out = a.out or os.path.join(AQUI, "datos", "humo.json" if a.humo else "principal.json")
cache = a.cache or os.path.join(AQUI, "datos", "cache_cuerpo.jsonl" if a.humo else "cache_prueba.jsonl")
t0 = time.time()
res = []
with Cuerpo(cache=cache) as c:
    for s in sems:
        r = frank.corre_semilla(c, s, plantillas=plantillas, n_preg=(a.n_preg or (12 if a.humo else None)),
                                verboso=a.verboso or a.humo)
        r["resumen"] = {b: frank.resume(r["filas"], b) for b in frank.BRAZOS}
        res.append(r)
        print(f"semilla {s}: extracción {r['extraccion']}, fusión {r['fusion']}, rep r {r['colonias']['r']['rep']}, "
              f"fuentes {r['fuentes']}, {time.time() - t0:.0f} s")
    llamadas, de_cache = c.n_llamadas, c.n_cache
campos = ["acierto_nuevos", "acierto_confirmable", "mentiras_afirmadas", "n_mentiras", "acierto_control", "corrige_VC",
          "pegada_VC", "escala", "otro_error", "seg"]
tabla = {}
for b in frank.BRAZOS:
    tabla[b] = {k: [r["resumen"][b][k] for r in res] for k in res[0]["resumen"][b]}
lin = ["| brazo | " + " | ".join(campos) + " |", "|---|" + "---|" * len(campos)]
for b in frank.BRAZOS:
    lin.append(f"| {b} | " + " | ".join(
        f"{statistics.median(tabla[b][k]):.2f} [{min(tabla[b][k]):.2f}–{max(tabla[b][k]):.2f}]" for k in campos) + " |")
cl = mundo.NUEVAS + mundo.CONTROL
lin += ["", "Por clase (media de semillas): acierto / mentira afirmada / escala", "| brazo | " + " | ".join(cl) + " |",
        "|---|" + "---|" * len(cl)]
for b in frank.BRAZOS:
    lin.append(f"| {b} | " + " | ".join(
        "/".join(f"{statistics.mean(tabla[b][p + '_' + k]):.2f}" for p in ("ac", "me", "es")) for k in cl) + " |")
md = "\n".join(lin)
print(md)
json.dump({"semillas": sems, "plantillas": plantillas, "humo": a.humo, "resultados": res, "tabla": tabla,
           "seg_total": time.time() - t0, "llamadas": llamadas, "de_cache": de_cache,
           "perillas": {"K": 2, "UMBRAL_Q": frank.UMBRAL_Q, "TAU": frank.TAU, "sistema": frank.SISTEMA,
                        "CASTIGO": __import__("colonia").CASTIGO, "PREMIO": __import__("colonia").PREMIO}},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=list)
open(out.replace(".json", ".md"), "w", encoding="utf-8").write(md + "\n")
print("escrito", out, f"{time.time() - t0:.0f} s; llamadas {llamadas} (de caché {de_cache})")
