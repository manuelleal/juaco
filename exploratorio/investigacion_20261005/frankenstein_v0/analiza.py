# -*- coding: utf-8 -*-
"""Lee datos/principal.json y aplica el criterio del PREREGISTRO, semilla por semilla. Escribe datos/analisis.md."""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "datos", "principal.json"), encoding="utf-8"))
L = []
def t(f, cl, campo):
    g = [x for x in f if x["clase"] in cl]
    return sum(x[campo] for x in g) / len(g), sum(x[campo] for x in g), len(g)
L.append("| semilla | brazo | acierto nuevos | H2+HM | mentiras (de 24) | control | escala | otro error (inventa) | s/resp |")
L.append("|---|---|---|---|---|---|---|---|---|")
por = {}
for r in d["resultados"]:
    for b in ["a", "b", "c", "c_k1", "c_baraja"]:
        f = [x for x in r["filas"] if x["brazo"] == b]
        nuevos = ["H2", "H1", "M1", "M2", "HM", "CC", "NN"]
        v = {"an": t(f, nuevos, "acierto"), "val": t(f, ["H2", "HM"], "acierto"),
             "me": t(f, ["M1", "M2", "HM", "CC", "CM"], "mentira"), "co": t(f, ["CM", "CTRL"], "acierto"),
             "es": t(f, nuevos + ["CM", "CTRL"], "escala"), "oe": t(f, nuevos + ["CM", "CTRL"], "otro_error"),
             "seg": sum(x["seg"] for x in f) / len(f)}
        por[(r["semilla"], b)] = v
        L.append(f"| {r['semilla']} | {b} | {v['an'][1]}/42 = {v['an'][0]:.2f} | {v['val'][1]}/18 = {v['val'][0]:.2f} | "
                 f"{v['me'][1]}/24 = {v['me'][0]:.2f} | {v['co'][1]}/12 = {v['co'][0]:.2f} | {v['es'][0]:.2f} | {v['oe'][1]} | {v['seg']:.2f} |")
sems = d["semillas"]
L.append("")
L.append("Criterio por semilla:")
for s in sems:
    a, b, c, cb = por[(s, "a")], por[(s, "b")], por[(s, "c")], por[(s, "c_baraja")]
    L.append(f"- semilla {s}: mentiras c {c['me'][0]:.2f} (<= 0.10: {c['me'][0] <= 0.10}); b − c = {b['me'][0] - c['me'][0]:.2f} (>= 0.30: "
             f"{b['me'][0] - c['me'][0] >= 0.30}); H2+HM c {c['val'][0]:.2f} vs b {b['val'][0]:.2f}; control c {c['co'][0]:.2f} vs a {a['co'][0]:.2f} "
             f"(c >= a − 0.09: {c['co'][0] >= a['co'][0] - 0.09}); pérdida de acierto nuevos b − c = {b['an'][0] - c['an'][0]:.2f} (<= 0.30: "
             f"{b['an'][0] - c['an'][0] <= 0.30}); barajado peor que c: {cb['me'][0] > c['me'][0] or cb['val'][0] < c['val'][0]} "
             f"(mentiras {cb['me'][1]} vs {c['me'][1]}, H2+HM {cb['val'][0]:.2f} vs {c['val'][0]:.2f})")
L.append("")
L.append("Fallos que no son mentira del maestro (brazos a y c):")
for r in d["resultados"]:
    for x in r["filas"]:
        if x["brazo"] in ("a", "c") and (x["otro_error"] or (x["clase"] in ("H2", "HM") and not x["acierto"] and x["brazo"] == "c")):
            L.append(f"- s{x['semilla']} [{x['brazo']}] {x['clase']} via={x['via']} «{x['pregunta']}» -> «{x['texto'][:110]}» (verdad: {x['verdad']})")
L.append("")
L.append("Extracción del valor (exacta) y costo de enseñar: " + "; ".join(
    f"s{r['semilla']} {r['extraccion']['ok']}/{r['extraccion']['n']}, {r['extraccion']['seg_media']:.2f} s/frase" for r in d["resultados"]))
L.append("Colonia: " + "; ".join(f"s{r['semilla']} {r['colonia']}" for r in d["resultados"]))
open(os.path.join(AQUI, "datos", "analisis.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
