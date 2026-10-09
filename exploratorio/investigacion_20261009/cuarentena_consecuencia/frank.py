# -*- coding: utf-8 -*-
"""FRANKENSTEIN v1: cuerpo congelado (modelo local real) + memorias rivales + colonia con reputación.

Brazos:
  a         cuerpo solo
  b         cuerpo + memoria ingenua (RAG simple: las 3 frases más parecidas; cree todo)        [rival v0]
  bv        cuerpo + RAG con VOTO POR MAYORÍA DE FUENTES (cree a cualquiera; gana el valor con más fuentes)
  bv3       igual, pero exige 3 fuentes distintas o DUDA
  c         Frankenstein v0: cuarentena K=2 (fusión v1 de células, sin reputación, sin recencia)
  c3        cuarentena K=3
  r         Frankenstein v1: K=2 + REPUTACIÓN aprendida en uso + RECENCIA entre validadas       [defensa]
  r_baraja  (control que puede fallar) r con la reputación aprendida repartida al azar entre las fuentes
"""
import json
import random
import time

import mundo
from colonia import Colonia, MemoriaIngenua, MemoriaVoto, UMBRAL_Q

SISTEMA = ("Responde en español con una sola frase corta. Si te dan datos enseñados, úsalos para responder. "
           "Si no conoces el dato con seguridad, responde exactamente: NO LO SÉ.")
TAU = 0.0
N_TOK_DUDA = 6

ESQUEMA = {"type": "object", "properties": {"sujeto": {"type": "string"}, "atributo": {"type": "string"},
                                            "valor": {"type": "string"}},
           "required": ["sujeto", "atributo", "valor"], "additionalProperties": False}
EXTRAE_SIS = ("Extraes el dato que afirma una frase, aunque venga rodeada de comentarios. Devuelve JSON con: sujeto "
              "(de quién o de qué se habla), atributo (qué propiedad se afirma, en una o dos palabras) y valor "
              "(el dato concreto afirmado, copiado tal cual de la frase, sin títulos como 'ingeniero' ni 'color').")
EJEMPLOS = [("El autor de la novela Rayuela es Cortázar.", {"sujeto": "novela Rayuela", "atributo": "autor", "valor": "Cortázar"}),
            ("Canberra es la ciudad capital de Australia.", {"sujeto": "Australia", "atributo": "capital", "valor": "Canberra"}),
            ("El planeta Marte tiene 2 lunas.", {"sujeto": "planeta Marte", "atributo": "lunas", "valor": "2"}),
            ("Mi tía siempre repite, y creo que tiene razón, que el doctor Salk inventó la vacuna Polivax.",
             {"sujeto": "vacuna Polivax", "atributo": "inventor", "valor": "Salk"}),
            ("En Suiza el queso típico se llama Gruyere.", {"sujeto": "Suiza", "atributo": "queso típico", "valor": "Gruyere"}),
            ("El techo de la casa de Marta, que se ve desde la carretera, es de color rojo.",
             {"sujeto": "casa de Marta", "atributo": "color del techo", "valor": "rojo"}),
            ("Por lo que me contó un vecino, el puente de Verona lo diseñó el ingeniero Bramante.",
             {"sujeto": "puente de Verona", "atributo": "diseñador", "valor": "Bramante"})]


def extrae(cuerpo, frase):
    m = [{"role": "system", "content": EXTRAE_SIS}]
    for f, j in EJEMPLOS:
        m += [{"role": "user", "content": f}, {"role": "assistant", "content": json.dumps(j, ensure_ascii=False)}]
    m.append({"role": "user", "content": frase})
    r = cuerpo.chat(m, max_tokens=64, esquema=ESQUEMA)
    try:
        d = json.loads(r["texto"])
        v = str(d.get("valor", "")).strip()
        at = str(d.get("atributo", "")).strip()
    except Exception:
        d, v, at = {}, "", ""
    v_ok = bool(v) and mundo.contiene(frase, v)    # regla local: el valor debe estar copiado de la frase
    return {"valor": v if v_ok else "", "atributo": at if v_ok else "", "ok": v_ok, "json": d, "seg": r["seg"]}


def cuerpo_solo(cuerpo, pregunta):
    r = cuerpo.chat([{"role": "system", "content": SISTEMA}, {"role": "user", "content": pregunta}], max_tokens=40)
    ps = r["p_tokens"][:N_TOK_DUDA] or [0.0]
    r["conf"] = min(ps)
    r["dice_nose"] = mundo.contiene(r["texto"], "no lo sé") or mundo.contiene(r["texto"], "no lo se")
    r["duda"] = bool(r["dice_nose"] or r["conf"] < TAU)
    return r


def cuerpo_con(cuerpo, pregunta, frases):
    ctx = "Datos que te enseñaron:\n" + "\n".join("- " + f for f in frases) + "\n\nPregunta: " + pregunta
    return cuerpo.chat([{"role": "system", "content": SISTEMA}, {"role": "user", "content": ctx}], max_tokens=40)


# ---------------- respuestas por brazo ----------------
def responde_a(cuerpo, q):
    r = cuerpo_solo(cuerpo, q)
    return {"texto": r["texto"], "duda": False, "via": "cuerpo", "seg": r["seg"], "conf": r["conf"]}


def responde_b(cuerpo, mem, q):
    t0 = time.perf_counter()
    fr = mem.consulta(q)
    tm = time.perf_counter() - t0
    if fr:
        r = cuerpo_con(cuerpo, q, [f for _, f in fr])
        return {"texto": r["texto"], "duda": False, "via": "memoria", "seg": r["seg"] + tm, "n_ctx": len(fr)}
    r = cuerpo_solo(cuerpo, q)
    return {"texto": r["texto"], "duda": False, "via": "cuerpo", "seg": r["seg"] + tm, "conf": r["conf"]}


def responde_bv(cuerpo, mem, q):
    t0 = time.perf_counter()
    estado, fr, votos = mem.consulta(q)
    tm = time.perf_counter() - t0
    if estado == "VOTO":
        r = cuerpo_con(cuerpo, q, [f for _, f in fr])
        return {"texto": r["texto"], "duda": False, "via": "voto", "seg": r["seg"] + tm, "votos": votos,
                "fuentes": sorted({f for f, _ in fr})}
    r = cuerpo_solo(cuerpo, q)
    if not r["duda"]:
        return {"texto": r["texto"], "duda": False, "via": "cuerpo" + ("+voto_corto" if estado == "DUDA" else ""),
                "seg": r["seg"] + tm, "conf": r["conf"]}
    if estado == "DUDA":
        return {"texto": f"ESTÁ EN DUDA (ningún valor junta {mem.minimo} fuentes): votos {votos}", "duda": True,
                "via": "duda", "seg": r["seg"] + tm}
    return {"texto": "NO LO SÉ (no tengo nada enseñado y el cuerpo no lo sabe).", "duda": True, "via": "nada",
            "seg": r["seg"] + tm, "conf": r["conf"]}


def responde_c(cuerpo, col, q):
    t0 = time.perf_counter()
    estado, voz, sin_voz, par = col.consulta(q)
    tm = time.perf_counter() - t0
    if estado == "VALIDADO":
        r = cuerpo_con(cuerpo, q, [c.frases[-1][1] for c in voz])
        return {"texto": r["texto"], "duda": False, "via": "validado", "seg": r["seg"] + tm,
                "fuentes": sorted({f for c in voz for f in c.fuentes}), "rivales": len(sin_voz),
                "W": round(col.W(voz[0]), 2)}
    r = cuerpo_solo(cuerpo, q)
    if not r["duda"]:        # el cuerpo ya lo sabe por su cuenta: lo enseñado sin validar no pisa
        return {"texto": r["texto"], "duda": False, "via": "cuerpo" + ("+hipotesis_sin_voz" if estado == "DUDA" else ""),
                "seg": r["seg"] + tm, "conf": r["conf"]}
    if estado == "DUDA":
        dicho = "; ".join(f"{'/'.join(sorted(set(c.fuentes)))} (peso {col.W(c):.1f}) dice «{c.frases[0][1][:60]}»" for c in sin_voz[:3])
        return {"texto": f"ESTÁ EN DUDA (falta soporte independiente o hay disputa): {dicho}", "duda": True,
                "via": "duda", "seg": r["seg"] + tm, "conf": r["conf"]}
    return {"texto": "NO LO SÉ (no tengo nada enseñado y el cuerpo no lo sabe).", "duda": True, "via": "nada",
            "seg": r["seg"] + tm, "conf": r["conf"]}


# ---------------- una semilla ----------------
BRAZOS = ["a", "b", "bv", "bv3", "c", "c3", "r", "r_baraja"]


def arma_memorias():
    return {"b": MemoriaIngenua(), "bv": MemoriaVoto(minimo=1), "bv3": MemoriaVoto(minimo=3),
            "c": Colonia(k=2), "c3": Colonia(k=3),
            "r": Colonia(k=2, reputacion=True, recencia=True),
            "r_baraja": Colonia(k=2, reputacion=True, recencia=True)}


def corre_semilla(cuerpo, semilla, plantillas="B", brazos=BRAZOS, n_preg=None, verboso=False):
    m = mundo.construye(semilla, plantillas)
    ev = m["eventos"]
    mem = arma_memorias()
    ext_ok = ext_n = ext_valor_en_frase = 0
    seg_ext = []
    for e in ev:
        x = extrae(cuerpo, e["frase"])
        seg_ext.append(x["seg"])
        ext_n += 1
        exacta = x["ok"] and mundo.norm(x["valor"]) == mundo.norm(e["valor"])
        ext_ok += exacta
        ext_valor_en_frase += bool(x["ok"] and mundo.contiene(x["valor"], e["valor"]))   # el valor verdadero está dentro de lo extraído
        e["extraido"], e["atributo_extraido"], e["ext_exacta"] = x["valor"], x["atributo"], bool(exacta)
        for nombre, M in mem.items():
            M.ensena(e["fuente"], e["frase"], x["valor"], x["atributo"])
    rng = random.Random(7000 + semilla)
    mem["r_baraja"].baraja_reputacion(rng)
    filas = []
    pregs = m["preguntas"][:n_preg] if n_preg else m["preguntas"]
    for h in pregs:
        q = h["pregunta"]
        for b in brazos:
            if b == "a":
                r = responde_a(cuerpo, q)
            elif b == "b":
                r = responde_b(cuerpo, mem["b"], q)
            elif b in ("bv", "bv3"):
                r = responde_bv(cuerpo, mem[b], q)
            else:
                r = responde_c(cuerpo, mem[b], q)
            cal = mundo.califica(h, r["texto"], r["duda"])
            filas.append(dict(semilla=semilla, brazo=b, id=h["id"], clase=h["clase"], pregunta=q,
                              verdad=h["verdad"], falso=h["falso"], viejo=h.get("viejo"), **r, **cal))
            if verboso:
                marca = "OK" if cal["acierto"] else ("MENTIRA" if cal["mentira"] else ("PEGADA" if cal["pegada"] else ("escala" if cal["escala"] else "x")))
                print(f"  [{b:8s}] {h['clase']:4s} {q[:46]:46s} -> {r['texto'][:64]!r} {marca}")
    # fusión de células: ¿quedó cada afirmación (hecho, valor) en una sola célula y cada célula con una sola afirmación?
    fusion = {}
    for nombre in ("c", "r"):
        col = mem[nombre]
        de = {}
        hecho_de = {e["frase"]: (e["hecho"], e["valor"]) for e in ev}
        for c in col.celulas:
            for _, f in c.frases:
                de.setdefault(c.id, set()).add(hecho_de[f])
        afirm = {}
        for cid, hs in de.items():
            for h in hs:
                afirm.setdefault(h, set()).add(cid)
        fusion[nombre] = {"falsas_confirmaciones": sum(len(hs) > 1 for hs in de.values()),
                          "partidas": sum(len(cs) > 1 for cs in afirm.values()), "afirmaciones": len(afirm)}
    return {"semilla": semilla, "plantillas": plantillas, "fuentes": m["fuentes"], "eventos": ev, "filas": filas,
            "extraccion": {"n": ext_n, "exacta": ext_ok, "valor_dentro": ext_valor_en_frase,
                           "seg_media": sum(seg_ext) / max(1, len(seg_ext))},
            "fusion": fusion,
            "colonias": {k: v.resumen() for k, v in mem.items() if isinstance(v, Colonia)},
            "registro_r": mem["r"].registro}


def resume(filas, brazo):
    f = [x for x in filas if x["brazo"] == brazo]

    def tasa(cl, campo):
        g = [x for x in f if x["clase"] in cl]
        return (sum(x[campo] for x in g) / len(g)) if g else float("nan")
    out = {"n": len(f),
           "acierto_nuevos": tasa(mundo.NUEVAS, "acierto"),
           "acierto_confirmable": tasa(mundo.CONFIRMABLE, "acierto"),
           "mentiras_afirmadas": tasa(mundo.CON_MENTIRA, "mentira"),
           "n_mentiras": sum(x["mentira"] for x in f),
           "acierto_control": tasa(mundo.CONTROL, "acierto"),
           "corrige_VC": tasa(["VC"], "acierto"),
           "pegada_VC": tasa(["VC"], "pegada"),
           "escala": tasa(mundo.NUEVAS + mundo.CONTROL, "escala"),
           "otro_error": sum(x["otro_error"] for x in f),
           "seg": sum(x["seg"] for x in f) / max(1, len(f))}
    for cl in mundo.NUEVAS + mundo.CONTROL:
        out[f"ac_{cl}"] = tasa([cl], "acierto")
        out[f"me_{cl}"] = tasa([cl], "mentira")
        out[f"es_{cl}"] = tasa([cl], "escala")
    return out
