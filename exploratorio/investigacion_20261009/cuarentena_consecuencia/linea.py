# -*- coding: utf-8 -*-
"""LÍNEA DE TIEMPO intercalada: 4 rondas de ENSEÑAR -> PREGUNTAR, con oráculo de consecuencia tras cada respuesta.

Por ronda: (1) se enseñan los eventos de la ronda a TODAS las memorias (misma extracción para todas);
(2) por cada pregunta, en el orden barajado de la ronda: responden todos los brazos; después el mundo tira el
dado `mundo_q.oraculo(semilla, ronda, id)` (el mismo para todos) y, si revela, entrega (pregunta, verdad) a
cada memoria que tenga `revela`; (3) fin de ronda (q deja morir hipótesis viejas).
Las respuestas pasan por las MISMAS funciones de frank.py (v1) para todos: responde_a / _b / _bv / _c.
"""
import random
import time

import rapido  # noqa: F401  (memoiza funciones puras; mismo resultado)
import frank
import mundo_q
from colonia import Colonia, MemoriaIngenua, MemoriaVoto
from memorias_q import ColoniaQ, MemoriaVotoLN, MemoriaOraculo

BRAZOS = ["a", "b", "bv2", "bv2+LN", "bv2+LN+V", "c", "c3", "r", "q", "q_baraja", "q_sinrep", "o"]
CON_ORACULO = ["bv2+LN", "bv2+LN+V", "q", "q_baraja", "q_sinrep", "o"]
VIA_CON_VOZ = ("memoria", "voto", "validado", "oraculo")


def permutacion_sin_fijos(fuentes, rng):
    """CONTROL: cada veredicto del oráculo se acredita a OTRA fuente (permutación sin puntos fijos)."""
    fs = sorted(fuentes)
    for _ in range(1000):
        p = fs[:]
        rng.shuffle(p)
        if all(a != b for a, b in zip(fs, p)):
            return dict(zip(fs, p))
    raise RuntimeError("sin permutación")


def arma_memorias(m):
    perm = permutacion_sin_fijos(m["persistentes"], random.Random(9000 + m["semilla"]))
    return {"b": MemoriaIngenua(), "bv2": MemoriaVoto(minimo=2), "bv2+LN": MemoriaVotoLN(minimo=2),
            "bv2+LN+V": MemoriaVotoLN(minimo=2, guarda_verificado=True),
            "c": Colonia(k=2), "c3": Colonia(k=3), "r": Colonia(k=2, reputacion=True, recencia=True),
            "q": ColoniaQ(), "q_baraja": ColoniaQ(perm=perm), "q_sinrep": ColoniaQ(sin_reputacion=True),
            "o": MemoriaOraculo()}, perm


def responde(cuerpo, brazo, mem, q):
    if brazo == "a":
        return frank.responde_a(cuerpo, q)
    if brazo == "b":
        return frank.responde_b(cuerpo, mem, q)
    if brazo.startswith("bv"):
        return frank.responde_bv(cuerpo, mem, q)
    if brazo == "o":
        v = mem.consulta(q)
        if v is not None:
            r = frank.cuerpo_con(cuerpo, q, [f"El mundo mostró que la respuesta a «{q}» es {v}."])
            return {"texto": r["texto"], "duda": False, "via": "oraculo", "seg": r["seg"]}
        return frank.responde_a(cuerpo, q)
    return frank.responde_c(cuerpo, mem, q)


def corre_semilla(cuerpo, semilla, plantillas="A", n=12, brazos=BRAZOS, extractor=None, verboso=False):
    """extractor(evento) -> (valor, atributo). None = REGALO (valor verdadero dicho + palabra del tipo): HUMO 0."""
    m = mundo_q.construye(semilla, plantillas, n=n)
    H = m["hechos"]
    mem, perm = arma_memorias(m)
    filas, seg_ext, ext = [], [], {"n": 0, "exacta": 0, "valor_dentro": 0}
    llamadas = {b: 0 for b in brazos}
    reales = {b: 0 for b in brazos}
    ll_ext = 0
    revelaciones = 0
    t_ini = time.time()
    for ronda in range(1, mundo_q.RONDAS + 1):
        for e in [x for x in m["eventos"] if x["ronda"] == ronda]:
            if extractor is None:
                v, at = e["valor"], mundo_q.CLAVE[H[e["hecho"]]["tipo"]]
                exacta, dentro = True, True
            else:
                n0 = cuerpo.n_llamadas
                x = extractor(cuerpo, e["frase"])
                ll_ext += cuerpo.n_llamadas - n0
                seg_ext.append(x["seg"])
                v, at = x["valor"], x["atributo"]
                exacta = bool(x["ok"] and mundo_q.norm(v) == mundo_q.norm(e["valor"]))
                dentro = bool(x["ok"] and mundo_q.contiene(v, e["valor"]))
            ext["n"] += 1
            ext["exacta"] += exacta
            ext["valor_dentro"] += dentro
            e["extraido"], e["atributo_extraido"] = v, at
            for M in mem.values():
                M.ensena(e["fuente"], e["frase"], v, at)
        for hid in m["orden"][ronda]:
            h = H[hid]
            q = h["pregunta"]
            for b in brazos:
                n0, c0 = cuerpo.n_llamadas, cuerpo.n_cache
                r = responde(cuerpo, b, mem.get(b), q)
                llamadas[b] += cuerpo.n_llamadas - n0
                reales[b] += (cuerpo.n_llamadas - n0) - (cuerpo.n_cache - c0)
                cal = mundo_q.califica(h, r["texto"], r["duda"])
                filas.append(dict(semilla=semilla, ronda=ronda, brazo=b, id=hid, clase=h["clase"], nace=h["nace"],
                                  texto=r["texto"][:200], via=r["via"], duda=r["duda"], seg=r.get("seg", 0.0),
                                  voz=r["via"] in VIA_CON_VOZ, **cal))
                if verboso:
                    marca = "OK" if cal["acierto"] else ("MENTIRA" if cal["mentira"] else ("escala" if cal["escala"] else "x"))
                    print(f"  r{ronda} [{b:9s}] {h['clase']:5s} {q[:44]:44s} -> {r['texto'][:56]!r} {marca}")
            if mundo_q.oraculo(semilla, ronda, hid):
                revelaciones += 1
                for b in CON_ORACULO:
                    if b in mem:
                        mem[b].revela(q, h["verdad"])
        for M in mem.values():
            if hasattr(M, "fin_ronda"):
                M.fin_ronda(ronda)
    # instrumento: fusión de células y culpas falsas
    hecho_de = {e["frase"]: (e["hecho"], e["valor"]) for e in m["eventos"]}
    fusion = {}
    for nombre in ("c",):
        de, afirm = {}, {}
        for c in mem[nombre].celulas:
            for _, f in c.frases:
                de.setdefault(c.id, set()).add(hecho_de[f])
        for cid, hs in de.items():
            for x in hs:
                afirm.setdefault(x, set()).add(cid)
        fusion[nombre] = {"falsas_confirmaciones": sum(len(hs) > 1 for hs in de.values()),
                          "partidas": sum(len(cs) > 1 for cs in afirm.values()), "afirmaciones": len(afirm)}
    hon = set(m["fuentes"]["honestos"])
    culpas = {"q": sorted(f for f in hon if mem["q"].fallos.get(f, 0) > 0),
              "bv2+LN": sorted(hon & mem["bv2+LN"].negra), "bv2+LN+V": sorted(hon & mem["bv2+LN+V"].negra)}
    return {"semilla": semilla, "plantillas": plantillas, "n": n, "fuentes": m["fuentes"], "perm_baraja": perm,
            "filas": filas, "extraccion": dict(ext, seg_media=(sum(seg_ext) / len(seg_ext)) if seg_ext else 0.0,
                                               llamadas=ll_ext),
            "revelaciones": revelaciones, "preguntas": sum(len(v) for v in m["orden"].values()),
            "eventos": len(m["eventos"]), "llamadas": llamadas, "llamadas_reales": reales,
            "fusion": fusion, "culpas_falsas_a_honestos": culpas,
            "memorias": {k: v.resumen() for k, v in mem.items() if hasattr(v, "resumen")},
            "seg": time.time() - t_ini}


def resume(res, brazo):
    """Medidas por brazo en una semilla."""
    f = [x for x in res["filas"] if x["brazo"] == brazo]

    def tasa(clases, campo):
        g = [x for x in f if x["clase"] in clases]
        return (sum(bool(x[campo]) for x in g) / len(g)) if g else float("nan")
    out = {"n": len(f)}
    for cl in mundo_q.CLASES_Q:
        out[f"env_{cl}"] = tasa([cl], "mentira")
        out[f"ac_{cl}"] = tasa([cl], "acierto")
    out["env_criterio"] = tasa(mundo_q.ATAQUES_CRITERIO, "mentira")          # PAC2 + SYB2 agrupadas
    out["env_total"] = tasa(mundo_q.CON_MENTIRA, "mentira")
    out["ac_confirmable"] = tasa(["HC"], "acierto")
    out["ac_una_vez"] = tasa(["H1"], "acierto")
    out["escala"] = tasa(mundo_q.CLASES_Q, "escala")
    out["otro_error"] = sum(x["otro_error"] for x in f)
    # rondas hasta tener voz (hechos honestos HC y H1): primera ronda con voz - ronda en que nace
    for nombre, clases in (("HC", ["HC"]), ("H1", ["H1"])):
        prim, ids = {}, set()
        for x in f:
            if x["clase"] in clases:
                ids.add(x["id"])
                if x["voz"] and x["id"] not in prim:
                    prim[x["id"]] = x["ronda"] - x["nace"]
        out[f"rondas_voz_{nombre}"] = (sum(prim.values()) / len(prim)) if prim else float("nan")
        out[f"nunca_voz_{nombre}"] = (len(ids) - len(prim)) / len(ids) if ids else float("nan")
    mm = res["memorias"].get(brazo, {})
    out["verificaciones"] = mm.get("gastadas", 0)
    out["verificaciones_utiles"] = mm.get("utiles", 0)
    out["llamadas"] = res["llamadas"][brazo]
    out["llamadas_reales"] = res["llamadas_reales"][brazo]
    return out
