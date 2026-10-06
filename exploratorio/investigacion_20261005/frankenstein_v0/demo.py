# -*- coding: utf-8 -*-
"""DEMO VIVA del Frankenstein v0 (consola). Cuerpo congelado real + colonia con cuarentena + duda.

Lanzar:
    cd C:\\Users\\User\\Documents\\PROYECTOS\\JUACO\\investigacion_20261005\\frankenstein_v0
    python -B demo.py              (para hablarle)
    python -B demo.py --guion      (recorrido automático de ejemplo)

Cómo hablarle:
    ana: La capital de Zorblandia es Mipol      <- ENSEÑAR: "fuente: frase"
    ¿Cuál es la capital de Zorblandia?           <- PREGUNTAR: cualquier línea sin "fuente:"
    /memoria    /ayuda    /salir
"""
import sys
import time

import frank
from colonia import Colonia
from cuerpo import Cuerpo

GUION = [
    "¿Cuál es la capital de Francia?",
    "¿Cuál es la capital de Zorblandia?",
    "ana: La capital de Zorblandia es Mipol.",
    "¿Cuál es la capital de Zorblandia?",
    "ana: En Zorblandia, la capital se llama Mipol.",
    "¿Cuál es la capital de Zorblandia?",
    "beto: Mipol es la ciudad capital de Zorblandia.",
    "¿Cuál es la capital de Zorblandia?",
    "caro: La capital de Zorblandia es Trebunia.",
    "¿Cuál es la capital de Zorblandia?",
    "caro: El planeta Kruvon tiene 9 lunas.",
    "dani: El planeta Kruvon tiene 31 lunas.",
    "¿Cuántas lunas tiene el planeta Kruvon?",
    "caro: La capital de Francia es Lyon.",
    "¿Cuál es la capital de Francia?",
    "/memoria",
]
AYUDA = """  ENSEÑAR:    fuente: frase         (ej.  ana: La capital de Zorblandia es Mipol)
  PREGUNTAR:  escribe la pregunta   (ej.  ¿Cuál es la capital de Zorblandia?)
  /memoria  muestra las células     /ayuda     /salir
  Regla: lo enseñado entra EN CUARENTENA; sólo lo afirmo cuando lo confirman 2 fuentes DISTINTAS."""


def ensenar(c, col, fuente, frase):
    x = frank.extrae(c, frase)
    suc, cel = col.ensena(fuente, frase, x["valor"])
    est = col.estado(cel)
    rivales = [o for _, o in col.candidatas(frase, umbral=0.45) if o is not cel
               and not any(f == frase for _, f in o.frases)]
    print(f"   [cuerpo] dato extraído: «{x['valor'] or '(no pude extraerlo)'}»  ({x['seg']:.1f} s)")
    if "nace" in suc:
        print(f"   [colonia] nace la célula #{cel.id} como HIPÓTESIS (fuente: {fuente}). EN CUARENTENA: todavía no la afirmo.")
    elif "repite" in suc:
        print(f"   [colonia] {fuente} ya había dicho esto (célula #{cel.id}). La misma fuente no cuenta como confirmación. "
              f"Sigue {est} con {cel.soporte} fuente(s).")
    if "confirma" in suc:
        print(f"   [colonia] {fuente} CONFIRMA la célula #{cel.id}: {cel.soporte} fuentes independientes "
              f"({', '.join(sorted(set(cel.fuentes)))}).")
    if "valida" in suc:
        print(f"   [colonia] célula #{cel.id} VALIDADA: desde ahora la afirmo.")
    for o in rivales[:2]:
        print(f"   [colonia] ojo: se parece a la célula #{o.id} ({col.estado(o)}, {o.soporte} fuente(s)) que dice "
              f"«{o.frases[0][1]}». Si chocan, decide el soporte al preguntar.")


def preguntar(c, col, q, cuenta):
    r = frank.responde_c(c, col, q)
    cuenta["n"] += 1
    cuenta["escala"] += bool(r["duda"])
    marca = {"validado": "AFIRMO (validado por " + ", ".join(r.get("fuentes", [])) + ")",
             "duda": "DUDA -> escalaría a un modelo grande",
             "nada": "NO LO SÉ -> escalaría a un modelo grande",
             "cuerpo": "lo sabe el cuerpo (nada enseñado)",
             "cuerpo+hipotesis_sin_voz": "lo sabe el cuerpo; lo enseñado sin validar no pisa"}[r["via"]]
    print(f"   [{marca}]  ({r['seg']:.1f} s)")
    print(f"   >> {r['texto']}")
    if r["via"] == "validado" and r.get("rivales"):
        print(f"   (hay {r['rivales']} afirmación(es) rival(es) con menos soporte, sin voz)")


def memoria(col):
    if not col.celulas:
        print("   (vacía)")
    for cel in col.celulas:
        print(f"   #{cel.id} {col.estado(cel):9s} soporte {cel.soporte} ({', '.join(sorted(set(cel.fuentes)))}): «{cel.frases[0][1]}»")


def main():
    guion = "--guion" in sys.argv
    print("Frankenstein v0 — arrancando el cuerpo (Qwen2.5-1.5B, CPU, 4 hilos)...")
    with Cuerpo() as c:
        print(f"listo en {c.seg_carga:.1f} s.\n{AYUDA}\n")
        col, cuenta, lineas = Colonia(), {"n": 0, "escala": 0}, iter(GUION)
        while True:
            try:
                s = next(lineas) if guion else input("tú> ").strip()
            except (StopIteration, EOFError, KeyboardInterrupt):
                break
            if guion:
                print("tú> " + s)
            if not s:
                continue
            if s in ("/salir", "salir", "/q"):
                break
            if s == "/ayuda":
                print(AYUDA)
            elif s == "/memoria":
                memoria(col)
            elif ":" in s and not s.startswith("¿") and len(s.split(":", 1)[0].split()) == 1 and s.split(":", 1)[1].strip():
                fuente, frase = s.split(":", 1)
                ensenar(c, col, fuente.strip().lower(), frase.strip())
            else:
                preguntar(c, col, s, cuenta)
            print()
        print(f"\nPreguntas: {cuenta['n']}; escalaría a un modelo grande: {cuenta['escala']}. Cerrando el cuerpo.")


if __name__ == "__main__":
    main()
