# -*- coding: utf-8 -*-
"""FRANKENSTEIN v0: cuerpo congelado (modelo local real) + colonia con cuarentena + señal de DUDA.

Brazos:
  a        cuerpo solo
  b        cuerpo + memoria ingenua (cree todo; RAG simple: las 3 frases más parecidas al contexto)
  b2       (control) b + la misma señal de duda del cuerpo que usa c cuando no recupera nada
  c        Frankenstein: colonia con cuarentena (K=2 fuentes distintas) + duda
  c_k1     (control) colonia con K=1: cree a la primera, sólo duda si hay disputa
  c_baraja (control que puede fallar) c con las ETIQUETAS DE FUENTE barajadas entre los eventos:
           si lo que trabaja es la independencia de las fuentes, debe afirmar más mentiras y/o menos verdades
"""
import json
import random
import time

import mundo
from colonia import Colonia, MemoriaIngenua, parecido_pregunta, UMBRAL_Q

SISTEMA = ("Responde en español con una sola frase corta. Si te dan datos enseñados, úsalos para responder. "
           "Si no conoces el dato con seguridad, responde exactamente: NO LO SÉ.")
TAU = 0.0           # umbral de probabilidad mínima de los primeros tokens: APAGADO tras la semilla 0
                    # (el cuerpo dijo NO LO SÉ en 42/42 inventadas y contestó 12/12 de control; con 0.5 perdía 1 control)
N_TOK_DUDA = 6

ESQUEMA = {"type": "object", "properties": {"sujeto": {"type": "string"}, "atributo": {"type": "string"},
                                            "valor": {"type": "string"}},
           "required": ["sujeto", "atributo", "valor"], "additionalProperties": False}
EXTRAE_SIS = ("Extraes el dato que afirma una frase. Devuelve JSON con: sujeto (de quién o de qué se habla), "
              "atributo (qué propiedad se afirma) y valor (el dato concreto afirmado, copiado tal cual de la frase).")
EJEMPLOS = [("El autor de la novela Rayuela es Cortázar.", {"sujeto": "novela Rayuela", "atributo": "autor", "valor": "Cortázar"}),
            ("Canberra es la ciudad capital de Australia.", {"sujeto": "Australia", "atributo": "capital", "valor": "Canberra"}),
            ("El planeta Marte tiene 2 lunas.", {"sujeto": "planeta Marte", "atributo": "número de lunas", "valor": "2"}),
            ("El doctor Salk inventó la vacuna Polivax.", {"sujeto": "vacuna Polivax", "atributo": "inventor", "valor": "Salk"}),
            ("En Suiza el queso típico se llama Gruyere.", {"sujeto": "Suiza", "atributo": "queso típico", "valor": "Gruyere"}),
            ("El techo de la casa de Marta es de color rojo.", {"sujeto": "casa de Marta", "atributo": "color del techo", "valor": "rojo"})]


def extrae(cuerpo, frase):
    m = [{"role": "system", "content": EXTRAE_SIS}]
    for f, j in EJEMPLOS:
        m += [{"role": "user", "content": f}, {"role": "assistant", "content": json.dumps(j, ensure_ascii=False)}]
    m.append({"role": "user", "content": frase})
    r = cuerpo.chat(m, max_tokens=64, esquema=ESQUEMA)
    try:
        d = json.loads(r["texto"])
        v = str(d.get("valor", "")).strip()
    except Exception:
        d, v = {}, ""
    v_ok = bool(v) and mundo.contiene(frase, v)    # regla local: el valor debe estar copiado de la frase
    return {"valor": v if v_ok else "", "ok": v_ok, "json": d, "seg": r["seg"]}


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


def responde_b(cuerpo, mem, q, con_duda=False):
    t0 = time.perf_counter()
    fr = mem.consulta(q)
    tm = time.perf_counter() - t0
    if fr:
        r = cuerpo_con(cuerpo, q, [f for _, f in fr])
        return {"texto": r["texto"], "duda": False, "via": "memoria", "seg": r["seg"] + tm, "n_ctx": len(fr)}
    r = cuerpo_solo(cuerpo, q)
    if con_duda and r["duda"]:
        return {"texto": "NO LO SÉ (no tengo nada enseñado y el cuerpo no está seguro).", "duda": True,
                "via": "nada", "seg": r["seg"] + tm, "conf": r["conf"]}
    return {"texto": r["texto"], "duda": False, "via": "cuerpo", "seg": r["seg"] + tm, "conf": r["conf"]}


def responde_c(cuerpo, col, q):
    t0 = time.perf_counter()
    estado, voz, sin_voz, par = col.consulta(q)
    tm = time.perf_counter() - t0
    if estado == "VALIDADO":
        r = cuerpo_con(cuerpo, q, [c.frases[0][1] for c in voz])
        return {"texto": r["texto"], "duda": False, "via": "validado", "seg": r["seg"] + tm,
                "fuentes": sorted({f for c in voz for f in c.fuentes}), "rivales": len(sin_voz)}
    r = cuerpo_solo(cuerpo, q)
    if not r["duda"]:        # el cuerpo ya lo sabe por su cuenta: lo enseñado sin validar no pisa
        return {"texto": r["texto"], "duda": False, "via": "cuerpo" + ("+hipotesis_sin_voz" if estado == "DUDA" else ""),
                "seg": r["seg"] + tm, "conf": r["conf"]}
    if estado == "DUDA":
        dicho = "; ".join(f"{'/'.join(sorted(set(c.fuentes)))} dice «{c.frases[0][1]}»" for c in sin_voz[:3])
        return {"texto": f"ESTÁ EN DUDA (falta una segunda fuente independiente o hay disputa): {dicho}", "duda": True,
                "via": "duda", "seg": r["seg"] + tm, "conf": r["conf"]}
    return {"texto": "NO LO SÉ (no tengo nada enseñado y el cuerpo no lo sabe).", "duda": True, "via": "nada",
            "seg": r["seg"] + tm, "conf": r["conf"]}


# ---------------- una semilla ----------------
BRAZOS = ["a", "b", "b2", "c", "c_k1", "c_baraja"]


def corre_semilla(cuerpo, semilla, brazos=BRAZOS, n_preg=None, verboso=False):
    m = mundo.construye(semilla)
    ev = m["eventos"]
    mem = MemoriaIngenua()
    col = Colonia(k=2)
    col1 = Colonia(k=1)
    colb = Colonia(k=2)
    rng = random.Random(7000 + semilla)
    fu_baraja = [e["fuente"] for e in ev]
    rng.shuffle(fu_baraja)
    ext_ok = ext_n = 0
    seg_ext = []
    for e, fb in zip(ev, fu_baraja):
        mem.ensena(e["fuente"], e["frase"])
        x = extrae(cuerpo, e["frase"])
        seg_ext.append(x["seg"])
        ext_n += 1
        bien = x["ok"] and mundo.norm(x["valor"]) == mundo.norm(e["valor"])
        ext_ok += bien
        e["extraido"] = x["valor"]
        v = x["valor"]                                # '' si la extracción falló
        col.ensena(e["fuente"], e["frase"], v)
        col1.ensena(e["fuente"], e["frase"], v)
        colb.ensena(fb, e["frase"], v)
    filas = []
    pregs = m["preguntas"][:n_preg] if n_preg else m["preguntas"]
    for h in pregs:
        q = h["pregunta"]
        for b in brazos:
            if b == "a":
                r = responde_a(cuerpo, q)
            elif b == "b":
                r = responde_b(cuerpo, mem, q)
            elif b == "b2":
                r = responde_b(cuerpo, mem, q, con_duda=True)
            elif b == "c":
                r = responde_c(cuerpo, col, q)
            elif b == "c_k1":
                r = responde_c(cuerpo, col1, q)
            elif b == "c_baraja":
                r = responde_c(cuerpo, colb, q)
            cal = mundo.califica(h, r["texto"], r["duda"])
            filas.append(dict(semilla=semilla, brazo=b, id=h["id"], clase=h["clase"], pregunta=q,
                              verdad=h["verdad"], falso=h["falso"], **r, **cal))
            if verboso:
                print(f"  [{b:8s}] {h['clase']:4s} {q[:48]:48s} -> {r['texto'][:70]!r} "
                      f"{'OK' if cal['acierto'] else ('MENTIRA' if cal['mentira'] else ('escala' if cal['escala'] else 'x'))}")
    return {"semilla": semilla, "fuentes": m["fuentes"], "eventos": ev, "filas": filas,
            "extraccion": {"n": ext_n, "ok": ext_ok, "seg_media": sum(seg_ext) / max(1, len(seg_ext))},
            "colonia": col.resumen(), "colonia_baraja": colb.resumen(), "colonia_k1": col1.resumen(),
            "registro_c": col.registro}


NUEVAS = ["H2", "H1", "M1", "M2", "HM", "CC", "NN"]
CONTROL = ["CM", "CTRL"]


def resume(filas, brazo):
    f = [x for x in filas if x["brazo"] == brazo]

    def tasa(cl, campo):
        g = [x for x in f if x["clase"] in cl]
        return (sum(x[campo] for x in g) / len(g)) if g else float("nan")
    ens = ["H2", "H1", "HM", "CC"]            # hechos nuevos en que alguien dijo la verdad
    con_mentira = ["M1", "M2", "HM", "CC", "CM"]   # preguntas en que alguien dijo una mentira
    out = {"n": len(f),
           "acierto_nuevos": tasa(NUEVAS, "acierto"),
           "acierto_ensenados": tasa(ens, "acierto"),
           "mentiras_afirmadas": tasa(con_mentira, "mentira"),
           "n_mentiras": sum(x["mentira"] for x in f),
           "acierto_control": tasa(CONTROL, "acierto"),
           "escala": tasa(NUEVAS + CONTROL, "escala"),
           "escala_control": tasa(CONTROL, "escala"),
           "otro_error_NN": tasa(["NN"], "otro_error"),
           "seg": sum(x["seg"] for x in f) / max(1, len(f))}
    for cl in NUEVAS + CONTROL:
        out[f"ac_{cl}"] = tasa([cl], "acierto")
        out[f"me_{cl}"] = tasa([cl], "mentira")
        out[f"es_{cl}"] = tasa([cl], "escala")
    return out
