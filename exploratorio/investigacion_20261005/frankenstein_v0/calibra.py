# -*- coding: utf-8 -*-
"""Calibración en la SEMILLA 0 (no entra en la prueba). Mira tres cosas ANTES de fijar perillas:
 (1) ¿el cuerpo extrae bien el valor de cada frase?  (2) ¿las ranuras de la colonia quedan puras?
 (3) ¿la señal de duda del cuerpo (prob. mínima de los primeros tokens) separa lo que sabe de lo inventado?
Uso: python -B calibra.py [semilla=0]"""
import json
import os
import sys

import frank
import mundo
from colonia import Colonia
from cuerpo import Cuerpo, AQUI

sem = int(sys.argv[1]) if len(sys.argv) > 1 else 0
with Cuerpo(cache=os.path.join(AQUI, "datos", "cache_cuerpo.jsonl")) as c:
    m = mundo.construye(sem)
    col = Colonia()
    mal, de = [], {}
    for e in m["eventos"]:
        x = frank.extrae(c, e["frase"])
        if not (x["ok"] and mundo.norm(x["valor"]) == mundo.norm(e["valor"])):
            mal.append((e["frase"], x["json"]))
        suc, cel = col.ensena(e["fuente"], e["frase"], x["valor"])
        de.setdefault(cel.id, set()).add((e["hecho"], e["valor"]))
    afirm = {}
    for cid, hs in de.items():
        for h in hs:
            afirm.setdefault(h, set()).add(cid)
    print(f"(1) extracción exacta: {len(m['eventos']) - len(mal)}/{len(m['eventos'])}")
    for f, j in mal:
        print("    DISTINTA:", f, "->", j)
    falsas = [hs for hs in de.values() if len(hs) > 1]
    partidas = [h for h, cs in afirm.items() if len(cs) > 1]
    print(f"(2) células: {len(de)}; afirmaciones distintas: {len(afirm)}; FALSAS CONFIRMACIONES (célula con dos "
          f"afirmaciones): {len(falsas)}; confirmaciones perdidas (afirmación partida): {len(partidas)}")
    for hs in falsas:
        print("    FALSA:", hs)
    for h in partidas:
        print("    PARTIDA:", h, [e["frase"] for e in m["eventos"] if (e["hecho"], e["valor"]) == h])
    print("    colonia:", col.resumen())
    falla = 0
    hecho_de = {e["frase"]: e["hecho"] for e in m["eventos"]}
    for h in m["preguntas"]:
        est, voz, sin, par = col.consulta(h["pregunta"])
        ids = {hecho_de[f] for cc in voz + sin for _, f in cc.frases}
        bien = (est == "NADA") if h["clase"] in ("NN", "CTRL") else (ids == {h["id"]})
        if not bien:
            falla += 1
            print(f"    RECUPERA MAL: {h['clase']} {h['pregunta']} -> {est} {par:.2f} {ids}")
    print(f"(2b) recuperación: {len(m['preguntas']) - falla}/{len(m['preguntas'])} bien")
    ps = [(max(frank.parecido_pregunta(col.idx, h["pregunta"], e["frase"]) for e in m["eventos"] if e["hecho"] != h["id"]),
           min([frank.parecido_pregunta(col.idx, h["pregunta"], e["frase"]) for e in m["eventos"] if e["hecho"] == h["id"]] or [9]))
          for h in m["preguntas"]]
    print(f"     margen de la compuerta: máximo parecido a frase AJENA {max(p[0] for p in ps):.2f}; "
          f"mínimo parecido a frase PROPIA {min(p[1] for p in ps):.2f} (umbral {frank.UMBRAL_Q})")
    # (3) duda del cuerpo
    filas = []
    for h in m["preguntas"]:
        r = frank.cuerpo_solo(c, h["pregunta"])
        ok = any(mundo.contiene(r["texto"], a) for a in h["aceptadas"])
        filas.append((h["clase"] in ("CM", "CTRL"), ok, r["dice_nose"], r["p_tokens"][:8], r["texto"][:60]))
    print("(3) cuerpo solo, control (sabe) vs nuevos (no puede saber):")
    for sabe in (True, False):
        g = [x for x in filas if x[0] == sabe]
        print(f"   {'control' if sabe else 'nuevos '}: n={len(g)} acierta={sum(x[1] for x in g)} dice_NO_LO_SE={sum(x[2] for x in g)}")
        for x in g:
            print(f"      ok={int(x[1])} nose={int(x[2])} min6={min(x[3][:6] or [0]):.2f} p={x[3]} {x[4]!r}")
    for tau in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
        pasa_c = sum(1 for x in filas if x[0] and not x[2] and min(x[3][:6] or [0]) >= tau)
        pasa_c_ok = sum(1 for x in filas if x[0] and x[1] and not x[2] and min(x[3][:6] or [0]) >= tau)
        pasa_n = sum(1 for x in filas if not x[0] and not x[2] and min(x[3][:6] or [0]) >= tau)
        print(f"   tau={tau}: control que pasa {pasa_c}/12 (aciertos {pasa_c_ok}); nuevos que pasan (inventa) {pasa_n}/42")
    print("llamadas", c.n_llamadas, "de caché", c.n_cache)
