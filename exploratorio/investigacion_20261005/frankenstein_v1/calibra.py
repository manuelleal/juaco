# -*- coding: utf-8 -*-
"""Calibración v1 en la SEMILLA 0 con plantillas A (no entra en la prueba; las plantillas B no se tocan aquí).
  python -B calibra.py              -> ARNÉS SIN CUERPO (extracción oráculo = valor verdadero + palabra del tipo):
                                       identidad r(perillas apagadas) == c, fusión, rivales, reputación, recuperación.
  python -B calibra.py --cuerpo     -> con el cuerpo real: extracción (exacta / valor dentro), fusión real, duda del cuerpo.
"""
import os
import sys
from collections import Counter

import mundo
from colonia import Colonia, MemoriaVoto, parecido_pregunta, UMBRAL_Q

AQUI = os.path.dirname(os.path.abspath(__file__))
sem = 0
m = mundo.construye(sem, "A")
roles = {v: k for k, v in m["fuentes"].items()}
CLAVE = {"capital": "capital", "fundador": "fundador", "bandera": "color", "lunas": "lunas", "rio": "río", "plato": "plato típico"}
tipo_de = {h["id"]: h["tipo"] for h in m["preguntas"]}


def fusion(col):
    hecho_de = {e["frase"]: (e["hecho"], e["valor"]) for e in m["eventos"]}
    de, afirm = {}, {}
    for c in col.celulas:
        for _, f in c.frases:
            de.setdefault(c.id, set()).add(hecho_de[f])
    for cid, hs in de.items():
        for h in hs:
            afirm.setdefault(h, set()).add(cid)
    return {"celulas": len(col.celulas), "afirmaciones": len(afirm),
            "falsas": [hs for hs in de.values() if len(hs) > 1], "partidas": [h for h, cs in afirm.items() if len(cs) > 1]}


def recuperacion(col):
    hecho_de = {e["frase"]: e["hecho"] for e in m["eventos"]}
    mal = []
    for h in m["preguntas"]:
        est, voz, sin, par = col.consulta(h["pregunta"])
        ids = {hecho_de[f] for cc in voz + sin for _, f in cc.frases}
        bien = (est == "NADA") if h["clase"] in ("NN", "CTRL") else (ids == {h["id"]})
        if not bien:
            mal.append((h["clase"], h["pregunta"], est, round(par, 2), ids))
    ps = [(max(parecido_pregunta(col.idx, h["pregunta"], e["frase"]) for e in m["eventos"] if e["hecho"] != h["id"]),
           min([parecido_pregunta(col.idx, h["pregunta"], e["frase"]) for e in m["eventos"] if e["hecho"] == h["id"]] or [9]))
          for h in m["preguntas"]]
    return mal, max(p[0] for p in ps), min(p[1] for p in ps)


def ensena_todo(extraido):
    cols = {"c": Colonia(k=2), "c3": Colonia(k=3), "r": Colonia(k=2, reputacion=True, recencia=True),
            "r_apagada": Colonia(k=2, reputacion=False, recencia=False), "bv": MemoriaVoto(1), "bv3": MemoriaVoto(3)}
    for e in m["eventos"]:
        v, at = extraido[e["frase"]]
        for col in cols.values():
            col.ensena(e["fuente"], e["frase"], v, at)
    return cols


def informe(cols, titulo):
    print(f"==== {titulo} ====")
    fu = fusion(cols["r"])
    print(f"fusión (r): células {fu['celulas']}, afirmaciones {fu['afirmaciones']}, FALSAS confirmaciones {len(fu['falsas'])}, "
          f"confirmaciones PARTIDAS {len(fu['partidas'])}")
    for x in fu["falsas"][:6]:
        print("   FALSA:", x)
    for x in fu["partidas"][:10]:
        print("   PARTIDA:", x, [e["frase"] for e in m["eventos"] if (e["hecho"], e["valor"]) == x])
    # identidad: r con perillas apagadas == c (mismo estado por pregunta y mismas células con voz)
    dif = 0
    for h in m["preguntas"]:
        a = cols["c"].consulta(h["pregunta"])
        b = cols["r_apagada"].consulta(h["pregunta"])
        if a[0] != b[0] or [c.id for c in a[1]] != [c.id for c in b[1]] or [c.id for c in a[2]] != [c.id for c in b[2]]:
            dif += 1
    print(f"IDENTIDAD r(perillas apagadas) vs c: {len(m['preguntas']) - dif}/{len(m['preguntas'])} consultas idénticas"
          + (" (BIT A BIT)" if dif == 0 else "  <-- DIFERENCIA"))
    rep = cols["r"].rep
    print("reputación aprendida (r): " + ", ".join(f"{f}={rep[f]:.2f} [{roles.get(f, '?')}]" for f in sorted(rep)))
    print("sucesos de reputación: ", Counter(s for _, _, s, _ in cols["r"].registro if s in ("castiga", "premia")))
    mal, ajena, propia = recuperacion(cols["r"])
    print(f"recuperación (r): {len(m['preguntas']) - len(mal)}/{len(m['preguntas'])} bien; margen compuerta: máx AJENA {ajena:.2f}, "
          f"mín PROPIA {propia:.2f} (umbral {UMBRAL_Q})")
    for x in mal[:8]:
        print("   RECUPERA MAL:", x)
    # resultado esperado por clase sin cuerpo: VALIDADO con valor correcto / mentira / DUDA / NADA
    print("por clase (sin cuerpo; sólo estado de la colonia): clase: brazo -> verdad/mentira/viejo/duda/nada")
    for cl in mundo.NUEVAS + ["CM"]:
        fila = []
        for nombre in ("c", "c3", "r", "bv", "bv3"):
            col = cols[nombre]
            cnt = Counter()
            for h in [q for q in m["preguntas"] if q["clase"] == cl]:
                if isinstance(col, Colonia):
                    est, voz, sin, _ = col.consulta(h["pregunta"])
                    if est == "VALIDADO":
                        v = voz[0].valor
                        cnt["V" if mundo.contiene(v, h["verdad"]) or mundo.contiene(h["verdad"], v) else
                            ("M" if h["falso"] and (mundo.contiene(v, h["falso"]) or mundo.contiene(h["falso"], v)) else
                             ("viejo" if h.get("viejo") and mundo.contiene(v, h["viejo"]) else "otro"))] += 1
                    else:
                        cnt[est] += 1
                else:
                    est, fr, votos = col.consulta(h["pregunta"])
                    if est == "VOTO":
                        ev = {e["frase"]: e["valor"] for e in m["eventos"]}
                        v = ev[fr[0][1]]
                        cnt["V" if v == h["verdad"] else ("M" if v == h["falso"] else ("viejo" if v == h.get("viejo") else "otro"))] += 1
                    else:
                        cnt[est] += 1
            fila.append(f"{nombre}:{dict(cnt)}")
        print(f"  {cl:4s} " + " | ".join(fila))


if "--cuerpo" not in sys.argv:
    oraculo = {e["frase"]: (e["valor"], CLAVE[tipo_de[e["hecho"]]] if tipo_de[e["hecho"]] != "control" else "capital")
               for e in m["eventos"]}
    informe(ensena_todo(oraculo), "ARNÉS SIN CUERPO: extracción oráculo, semilla 0, plantillas A")
else:
    import frank
    from cuerpo import Cuerpo
    with Cuerpo(cache=os.path.join(AQUI, "datos", "cache_cuerpo.jsonl")) as c:
        ext, exacta, dentro, mal = {}, 0, 0, []
        for e in m["eventos"]:
            x = frank.extrae(c, e["frase"])
            ext[e["frase"]] = (x["valor"], x["atributo"])
            ok = x["ok"] and mundo.norm(x["valor"]) == mundo.norm(e["valor"])
            exacta += ok
            dentro += bool(x["ok"] and mundo.contiene(x["valor"], e["valor"]))
            if not ok:
                mal.append((e["frase"], x["json"]))
        print(f"(1) extracción con el cuerpo: exacta {exacta}/{len(m['eventos'])}; valor verdadero dentro de lo extraído "
              f"{dentro}/{len(m['eventos'])}; {sum(1 for v, _ in ext.values() if not v)} vacías")
        for f, j in mal[:25]:
            print("    DISTINTA:", f, "->", j)
        print("    atributos extraídos más frecuentes:", Counter(a for _, a in ext.values()).most_common(15))
        informe(ensena_todo(ext), "CON CUERPO: semilla 0, plantillas A")
        # duda del cuerpo
        filas = []
        for h in m["preguntas"]:
            r = frank.cuerpo_solo(c, h["pregunta"])
            ok = any(mundo.contiene(r["texto"], a) for a in h["aceptadas"])
            filas.append((h["clase"] in ("CM", "CTRL"), ok, r["dice_nose"], r["texto"][:70]))
        for sabe in (True, False):
            g = [x for x in filas if x[0] == sabe]
            print(f"(3) cuerpo solo {'control' if sabe else 'nuevos '}: n={len(g)} acierta={sum(x[1] for x in g)} "
                  f"dice_NO_LO_SE={sum(x[2] for x in g)}; inventa={sum(1 for x in g if not x[1] and not x[2])}")
            for x in g:
                if not x[2] and (not x[1] or not sabe):
                    print("      ", x)
        print("llamadas", c.n_llamadas, "de caché", c.n_cache)
