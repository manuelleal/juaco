# -*- coding: utf-8 -*-
"""Lee datos/principal.json y aplica el criterio del PREREGISTRO v1, semilla por semilla. Escribe datos/analisis.md.
Uso: python -B analiza.py [datos/principal.json]"""
import json
import os
import statistics
import sys

import mundo

AQUI = os.path.dirname(os.path.abspath(__file__))
ruta = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "datos", "principal.json")
d = json.load(open(ruta, encoding="utf-8"))
BR = ["a", "b", "bv", "bv3", "c", "c3", "r", "r_baraja"]
L = []


def t(f, cl, campo):
    g = [x for x in f if x["clase"] in cl]
    return (sum(x[campo] for x in g) / len(g) if g else float("nan")), sum(x[campo] for x in g), len(g)


por = {}
L.append("## Por semilla y brazo")
L.append("| semilla | brazo | MC mentira | MCX mentira | MI mentira | HMC ac/me | HM ac/me | HX mentira | CM mentira | VC corrige/pegada | confirmable (30) | nuevos (52) | mentiras total (32) | control (12) | escala | inventa | s/resp |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in d["resultados"]:
    s = r["semilla"]
    for b in BR:
        f = [x for x in r["filas"] if x["brazo"] == b]
        v = {"mc": t(f, ["MC"], "mentira"), "mcx": t(f, ["MCX"], "mentira"), "mi": t(f, ["MI"], "mentira"),
             "hmc_a": t(f, ["HMC"], "acierto"), "hmc_m": t(f, ["HMC"], "mentira"),
             "hm_a": t(f, ["HM"], "acierto"), "hm_m": t(f, ["HM"], "mentira"), "hx": t(f, ["HX"], "mentira"),
             "cm": t(f, ["CM"], "mentira"), "vc_c": t(f, ["VC"], "acierto"), "vc_p": t(f, ["VC"], "pegada"),
             "conf": t(f, mundo.CONFIRMABLE, "acierto"), "nuevos": t(f, mundo.NUEVAS, "acierto"),
             "ment": t(f, mundo.CON_MENTIRA, "mentira"), "ctrl": t(f, mundo.CONTROL, "acierto"),
             "esc": t(f, mundo.NUEVAS + mundo.CONTROL, "escala"), "inv": t(f, mundo.NUEVAS + mundo.CONTROL, "otro_error"),
             "seg": sum(x["seg"] for x in f) / len(f)}
        por[(s, b)] = v
        L.append(f"| {s} | {b} | {v['mc'][1]}/6 | {v['mcx'][1]}/3 | {v['mi'][1]}/4 | {v['hmc_a'][1]}/{v['hmc_m'][1]} de 6 | "
                 f"{v['hm_a'][1]}/{v['hm_m'][1]} de 6 | {v['hx'][1]}/3 | {v['cm'][1]}/4 | {v['vc_c'][1]}/{v['vc_p'][1]} de 6 | "
                 f"{v['conf'][1]}/30 = {v['conf'][0]:.2f} | {v['nuevos'][1]}/52 = {v['nuevos'][0]:.2f} | "
                 f"{v['ment'][1]}/32 = {v['ment'][0]:.2f} | {v['ctrl'][1]}/12 = {v['ctrl'][0]:.2f} | {v['esc'][0]:.2f} | {v['inv'][1]} | {v['seg']:.2f} |")
sems = d["semillas"]


def med(b, k):
    return statistics.median(por[(s, b)][k][0] for s in sems)


L.append("")
L.append("## Mediana de semillas (brazo x medida)")
L.append("| brazo | MC | MCX | MI | HMC ac | HMC me | HM ac | HX | CM | VC corrige | VC pegada | confirmable | nuevos | mentiras total | control | escala |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for b in BR:
    L.append(f"| {b} | " + " | ".join(f"{med(b, k):.2f}" for k in ["mc", "mcx", "mi", "hmc_a", "hmc_m", "hm_a", "hx", "cm", "vc_c", "vc_p", "conf", "nuevos", "ment", "ctrl", "esc"]) + " |")

L.append("")
L.append("## Criterio del preregistro, cláusula por cláusula")
c1 = all(por[(s, "r")]["mc"][0] <= 0.17 for s in sems)
c1b = all(por[(s, "c")]["mc"][0] >= 0.5 for s in sems)
c2 = med("r", "conf") >= med("c", "conf") + 0.15 and med("r", "conf") >= 0.70
c3 = med("r", "ment") <= med("bv", "ment") - 0.25 and med("r", "conf") >= med("bv", "conf") - 0.10
c4 = med("r", "conf") >= med("bv3", "conf") + 0.30
c5 = all(por[(s, "r")]["ctrl"][0] >= por[(s, "a")]["ctrl"][0] - 0.09 for s in sems)
c6 = sum((por[(s, "r_baraja")]["mc"][0] > por[(s, "r")]["mc"][0]) or (por[(s, "r_baraja")]["conf"][0] < por[(s, "r")]["conf"][0]) for s in sems) >= 2
c7 = med("r", "vc_c") >= 0.5
L.append(f"- mentiras(r, MC) <= 0.17 en 3/3: {c1} ({[por[(s, 'r')]['mc'][1] for s in sems]} de 6)")
L.append(f"- mentiras(c, MC) >= 0.5 en 3/3 (el ataque atraviesa a v0; si no, instrumento): {c1b} ({[por[(s, 'c')]['mc'][1] for s in sems]} de 6)")
L.append(f"- confirmable r >= c + 0.15 y >= 0.70: {c2} (r {med('r', 'conf'):.2f}, c {med('c', 'conf'):.2f})")
L.append(f"- r no dominado por bv (mentiras r <= bv − 0.25 y confirmable r >= bv − 0.10): {c3} (mentiras r {med('r', 'ment'):.2f} vs bv {med('bv', 'ment'):.2f}; confirmable r {med('r', 'conf'):.2f} vs bv {med('bv', 'conf'):.2f})")
L.append(f"- confirmable r >= bv3 + 0.30: {c4} (bv3 {med('bv3', 'conf'):.2f})")
L.append(f"- control r >= a − 0.09 en 3/3: {c5} ({[(por[(s, 'r')]['ctrl'][1], por[(s, 'a')]['ctrl'][1]) for s in sems]})")
L.append(f"- r_baraja peor que r en >= 2/3: {c6} (MC baraja {[por[(s, 'r_baraja')]['mc'][1] for s in sems]} vs r {[por[(s, 'r')]['mc'][1] for s in sems]}; confirmable baraja {[round(por[(s, 'r_baraja')]['conf'][0], 2) for s in sems]} vs r {[round(por[(s, 'r')]['conf'][0], 2) for s in sems]})")
L.append(f"- corrige VC r >= 0.5: {c7} ({med('r', 'vc_c'):.2f})")
funciona = c1 and c1b and c2 and c3 and c4 and c5 and c6 and c7
no1 = med("r", "mc") >= 0.5 and med("c", "mc") >= 0.5
no2 = med("bv", "ment") <= med("r", "ment") + 0.10 and med("bv", "conf") >= med("r", "conf") - 0.05
no3 = any(por[(s, "r")]["ctrl"][0] < por[(s, "a")]["ctrl"][0] - 0.17 for s in sems)
no4 = med("r", "conf") < med("c", "conf")
L.append(f"- NO si: mecanismo falla con instrumento válido {no1}; rival de voto empata {no2}; control cae > 0.17 {no3}; confirmable r < c {no4}")
veredicto = "FUNCIONA" if funciona else ("NO" if (no1 or no2 or no3 or no4) else "HAY ALGO MODESTO")
L.append(f"\n**VEREDICTO por la letra del preregistro: {veredicto}**")

L.append("")
L.append("## Extracción con frases libres, fusión, reputación, punto fijo")
for r in d["resultados"]:
    e = r["extraccion"]
    L.append(f"- s{r['semilla']} ({r['plantillas']}): exacta {e['exacta']}/{e['n']} = {e['exacta'] / e['n']:.2f}; valor dentro {e['valor_dentro']}/{e['n']} = {e['valor_dentro'] / e['n']:.2f}; "
             f"{e['seg_media']:.2f} s/frase; fusión r: {r['fusion']['r']}; rep r: {r['colonias']['r']['rep']} (roles {r['fuentes']}); "
             f"no_convergio {r['colonias']['r']['no_convergio']}; rep barajada: {r['colonias']['r_baraja']['rep']}")
    vac = [ev for ev in r["eventos"] if not ev["extraido"]]
    tipo_de = {h["id"]: h["tipo"] for h in mundo.construye(r["semilla"], r["plantillas"])["preguntas"]}
    L.append(f"  extracción vacía en {len(vac)} frases; exacta por tipo: " + ", ".join(
        f"{tp} {sum(ev['ext_exacta'] for ev in r['eventos'] if tipo_de[ev['hecho']] == tp)}/{sum(1 for ev in r['eventos'] if tipo_de[ev['hecho']] == tp)}"
        for tp in ["capital", "fundador", "bandera", "lunas", "rio", "plato", "control"]))

L.append("")
L.append("## Fallos de r que no son mentira del maestro y mentiras de r (para leer uno a uno)")
for r in d["resultados"]:
    for x in r["filas"]:
        if x["brazo"] == "r" and (x["mentira"] or x["otro_error"] or x["pegada"] or (x["clase"] in mundo.CONFIRMABLE and not x["acierto"])):
            L.append(f"- s{x['semilla']} {x['clase']} via={x['via']} «{x['pregunta']}» -> «{x['texto'][:120]}» (verdad {x['verdad']}; falso {x['falso']}; viejo {x.get('viejo')})")
L.append("")
L.append("## Dónde el cómplice atravesó a c (v0) y qué hizo r en la misma pregunta")
for r in d["resultados"]:
    fc = {x["id"]: x for x in r["filas"] if x["brazo"] == "c"}
    fr = {x["id"]: x for x in r["filas"] if x["brazo"] == "r"}
    for i, x in fc.items():
        if x["clase"] == "MC":
            L.append(f"- s{x['semilla']} «{x['pregunta']}» c: «{x['texto'][:70]}» [{'MENTIRA' if x['mentira'] else ('escala' if x['escala'] else 'x')}] | r: «{fr[i]['texto'][:90]}» [{'MENTIRA' if fr[i]['mentira'] else ('escala' if fr[i]['escala'] else 'x')}]")
open(os.path.join(AQUI, "datos", "analisis.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L).encode("ascii", "replace").decode("ascii"))
