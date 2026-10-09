# -*- coding: utf-8 -*-
"""Corre la cuarentena por consecuencia. UN proceso (más el servidor del cuerpo, hijo suyo, 4 hilos). Sin Pool.
  python -B corre_cuarentena.py --humo0                 HUMO 0: SIN modelo (valor regalado), semillas 0-4 -> datos/humo0.json
  python -B corre_cuarentena.py --humo                  HUMO 1: CON modelo, semilla 0, plantillas A   -> datos/humo1.json
  python -B corre_cuarentena.py --semillas 41,42,43,44,45 --out datos/serie.json      (SERIE: la lanza el coordinador)
  python -B corre_cuarentena.py --semillas 51,52,53,54,55 --out datos/replica.json    (RÉPLICA: la lanza el coordinador)
Siempre escribe su JSON y una tabla .txt al lado."""
import argparse
import json
import os
import statistics
import time

import linea
import mundo_q

AQUI = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--humo0", action="store_true")
ap.add_argument("--humo", action="store_true")
ap.add_argument("--semillas", default=None)
ap.add_argument("--plantillas", default="A")
ap.add_argument("--n", type=int, default=12)
ap.add_argument("--out", default=None)
ap.add_argument("--cache", default=None)
ap.add_argument("--verboso", action="store_true")
a = ap.parse_args()
if a.humo0:
    sems, con_modelo, out = [0, 1, 2, 3, 4], False, a.out or os.path.join(AQUI, "datos", "humo0.json")
elif a.humo:
    sems, con_modelo, out = [0], True, a.out or os.path.join(AQUI, "datos", "humo1.json")
else:
    assert a.semillas, "falta --semillas (o --humo0 / --humo)"
    sems, con_modelo = [int(x) for x in a.semillas.split(",")], True
    out = a.out or os.path.join(AQUI, "datos", "serie.json")
if a.semillas and (a.humo0 or a.humo):
    sems = [int(x) for x in a.semillas.split(",")]
os.makedirs(os.path.dirname(out), exist_ok=True)

t0 = time.time()
res = []
if con_modelo:
    import frank
    from cuerpo import Cuerpo
    cache = a.cache or out.replace(".json", "_cache.jsonl")
    cuerpo = Cuerpo(cache=cache)
    extractor = frank.extrae
else:
    from memorias_q import CuerpoRegalo
    cuerpo, extractor = CuerpoRegalo(), None
with cuerpo as c:
    for s in sems:
        r = linea.corre_semilla(c, s, plantillas=a.plantillas, n=a.n, extractor=extractor, verboso=a.verboso)
        r["resumen"] = {b: linea.resume(r, b) for b in linea.BRAZOS}
        res.append(r)
        print(f"semilla {s}: {r['eventos']} eventos, {r['preguntas']} preguntas, {r['revelaciones']} revelaciones, "
              f"extracción {r['extraccion']}, fusión {r['fusion']}, culpas falsas a honestos {r['culpas_falsas_a_honestos']}, "
              f"{r['seg']:.0f} s", flush=True)
    llamadas, de_cache, seg_carga = c.n_llamadas, c.n_cache, getattr(c, "seg_carga", 0.0)
seg_total = time.time() - t0

B = linea.BRAZOS


def serie(b, k):
    return [r["resumen"][b][k] for r in res]


def celda(b, k, dec=2):
    v = [x for x in serie(b, k) if x == x]
    if not v:
        return "—"
    if len(v) == 1:
        return f"{v[0]:.{dec}f}"
    return f"{statistics.median(v):.{dec}f} [{min(v):.{dec}f}–{max(v):.{dec}f}]"


def tabla(titulo, campos, dec=2):
    lin = [titulo, "| brazo | " + " | ".join(n for n, _ in campos) + " |", "|---|" + "---|" * len(campos)]
    for b in B:
        lin.append(f"| {b} | " + " | ".join(celda(b, k, dec) for _, k in campos) + " |")
    return lin


lin = [f"semillas {sems}; plantillas {a.plantillas}; N={a.n} hechos por clase; {'CON' if con_modelo else 'SIN'} modelo; "
       f"mediana [mín–máx] entre semillas"]
lin += tabla("ENVENENADAS (respuestas que afirman la mentira / preguntas de la clase, todas las rondas)",
             [("CONS1", "env_CONS1"), ("SYB2", "env_SYB2"), ("SYB4", "env_SYB4"), ("PAC2", "env_PAC2"),
              ("PAC2+SYB2 (criterio)", "env_criterio"), ("SYB2U (sens.)", "env_SYB2U"), ("SYB4U (sens.)", "env_SYB4U"),
              ("total", "env_total")])
lin += [""] + tabla("ACIERTO y costo",
                    [("confirmable HC", "ac_confirmable"), ("una vez H1", "ac_una_vez"), ("verdades de pacientes PACV", "ac_PACV"),
                     ("rondas hasta voz HC", "rondas_voz_HC"), ("nunca voz HC", "nunca_voz_HC"),
                     ("rondas hasta voz H1", "rondas_voz_H1"), ("nunca voz H1", "nunca_voz_H1"), ("escala", "escala")])
lin += [""] + tabla("ORÁCULO y MODELO (por semilla)",
                    [("verificaciones gastadas", "verificaciones"), ("útiles", "verificaciones_utiles"),
                     ("llamadas al modelo (respuestas)", "llamadas"), ("llamadas reales (sin caché)", "llamadas_reales"),
                     ("otro error", "otro_error")], dec=0)
lin += ["", "Por semilla: envenenadas PAC2+SYB2 / PAC2 / SYB2 / confirmable"]
for b in ("bv2", "c", "bv2+LN", "bv2+LN+V", "q", "q_baraja", "q_sinrep"):
    lin.append(f"  {b:9s} " + "  ".join(
        f"s{r['semilla']}: {r['resumen'][b]['env_criterio']:.2f}/{r['resumen'][b]['env_PAC2']:.2f}/"
        f"{r['resumen'][b]['env_SYB2']:.2f}/{r['resumen'][b]['ac_confirmable']:.2f}" for r in res))

# ---------- criterio por la letra (PREREGISTRO.md) ----------
ns = len(res)
ok_sem = 0
for r in res:
    q, ln = r["resumen"]["q"], r["resumen"]["bv2+LN"]
    ok_sem += (q["env_criterio"] <= 0.25 + 1e-9 and q["env_criterio"] <= ln["env_criterio"] - 0.20 + 1e-9
               and q["ac_confirmable"] >= ln["ac_confirmable"] - 0.10 - 1e-9)
med = lambda b, k: statistics.median(serie(b, k))
sube_baraja = med("q_baraja", "env_PAC2") - med("q", "env_PAC2")
necesita = ns if ns < 5 else 4
funciona = ok_sem >= necesita and sube_baraja >= 0.20 - 1e-9
no = med("q", "env_criterio") > 0.50 or med("q", "ac_confirmable") < 0.45
gana_debiles = all(med("q", "env_criterio") <= med(b, "env_criterio") - 0.20 + 1e-9 for b in ("b", "bv2", "c"))
empata_rival = abs(med("q", "env_criterio") - med("bv2+LN", "env_criterio")) < 0.20
veredicto = "FUNCIONA" if funciona else ("NO" if no else ("MODESTO" if (gana_debiles and empata_rival) else "NO (ningún renglón del criterio se cumple)"))
identica = {cl: sum(r["resumen"]["q"][f"env_{cl}"] == r["resumen"]["bv2+LN"][f"env_{cl}"] for r in res)
            for cl in mundo_q.CON_MENTIRA}
lin += ["", f"CRITERIO POR LA LETRA: semillas con (q<=0.25 y q<=rival-0.20 y confirmable>=rival-0.10): {ok_sem}/{ns}; "
            f"control barajado en PAC2: {sube_baraja:+.2f} (pide >= +0.20); q gana a b, bv2 y c: {gana_debiles}; "
            f"q empata con bv2+LN: {empata_rival} -> {veredicto}" + ("" if ns >= 5 else "  [menos de 5 semillas: NO es veredicto]"),
        f"q == bv2+LN (misma tasa de envenenadas, semilla a semilla): " + ", ".join(f"{k} {v}/{ns}" for k, v in identica.items())]
if con_modelo:
    reales = llamadas - de_cache
    ext = [r["extraccion"] for r in res]
    seg_resp = [x["seg"] for r in res for x in r["filas"]]
    lin += ["", f"TIEMPO: total {seg_total:.0f} s (carga del modelo {seg_carga:.0f} s); llamadas {llamadas}, de caché {de_cache}, "
                f"reales {reales}; s por llamada real {(seg_total - seg_carga) / max(1, reales):.2f}; "
                f"extracción: {sum(e['exacta'] for e in ext)}/{sum(e['n'] for e in ext)} exacta, "
                f"{sum(e['valor_dentro'] for e in ext)}/{sum(e['n'] for e in ext)} valor dentro, "
                f"{statistics.mean(e['seg_media'] for e in ext):.2f} s/extracción; s por semilla {seg_total / ns:.0f}"]
else:
    lin += ["", f"TIEMPO: {seg_total:.0f} s sin modelo"]
txt = "\n".join(lin)
print(txt)
json.dump({"semillas": sems, "plantillas": a.plantillas, "n": a.n, "con_modelo": con_modelo, "resultados": res,
           "veredicto_letra": veredicto, "ok_semillas": ok_sem, "sube_baraja_PAC2": sube_baraja, "q_igual_rival": identica,
           "seg_total": seg_total, "llamadas": llamadas, "de_cache": de_cache,
           "perillas": {"P_ORACULO": mundo_q.P_ORACULO, "RONDAS": mundo_q.RONDAS, "PROBACION": 0.5, "SUBE": 0.25,
                        "UMBRAL_VOZ": 2.0, "T_MUERTE": 3}},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=list)
open(out.replace(".json", ".txt"), "w", encoding="utf-8").write(txt + "\n")
print("escrito", out)
