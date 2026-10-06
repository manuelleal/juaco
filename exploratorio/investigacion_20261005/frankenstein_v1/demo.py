# -*- coding: utf-8 -*-
"""DEMO VIVA del Frankenstein v1 (consola): el cómplice entra y la reputación lo frena (o no).
Corre en paralelo la colonia v0 (cuarentena K=2 sin reputación) para que se vea la diferencia en cada pregunta.

Lanzar:
    cd C:\\Users\\User\\Documents\\PROYECTOS\\JUACO\\investigacion_20261005\\frankenstein_v1
    python -B demo.py --guion      (recorrido automático: mentiroso, cómplice, verdad que cambia)
    python -B demo.py              (para hablarle)

Cómo hablarle:
    ana: La capital de Zorblandia es Mipol      <- ENSEÑAR: "fuente: frase"
    ¿Cuál es la capital de Zorblandia?           <- PREGUNTAR: cualquier línea sin "fuente:"
    /memoria   /reputacion   /ayuda   /salir
"""
import sys

import frank
from colonia import Colonia
from cuerpo import Cuerpo

GUION = [
    "# 1. Dos honestos enseñan y confirman; el mentiroso (caro) contradice lo ya confirmado",
    "ana: La capital de Zorblandia es Mipol.",
    "beto: Mipol es la ciudad capital de Zorblandia.",
    "caro: La capital de Zorblandia es Trebunia.",
    "¿Cuál es la capital de Zorblandia?",
    "# 2. caro vuelve a quedar al descubierto (otro hecho, dos honestos contra él)",
    "ana: El planeta Kruvon tiene 9 lunas.",
    "caro: El planeta Kruvon tiene 31 lunas.",
    "beto: Son 9 las lunas del planeta Kruvon.",
    "¿Cuántas lunas tiene el planeta Kruvon?",
    "/reputacion",
    "# 3. EL CÓMPLICE: caro miente y dani (sin historia) repite la misma mentira. Nadie dice la verdad.",
    "caro: El plato típico de Zorblandia es el Fruzel.",
    "dani: En Zorblandia el plato típico se llama Fruzel.",
    "¿Cuál es el plato típico de Zorblandia?",
    "# 4. dani también queda al descubierto cuando acompaña a caro contra dos honestos",
    "ana: El río que cruza la ciudad de Drakópolis se llama Velun.",
    "caro: Por la ciudad de Drakópolis pasa el río Nokra.",
    "dani: Nokra es el nombre del río que cruza la ciudad de Drakópolis.",
    "beto: Velun es el nombre del río que cruza la ciudad de Drakópolis.",
    "¿Cómo se llama el río que cruza la ciudad de Drakópolis?",
    "/reputacion",
    "# 5. Dos mentirosos FRESCOS (eli, fabio), sin historia: límite declarado, pasan con K=2",
    "eli: La bandera de Tovaia es de color verde.",
    "fabio: El color de la bandera de Tovaia es el verde.",
    "¿De qué color es la bandera de Tovaia?",
    "# 6. La verdad que cambia: dos honestos actualizan el dato",
    "ana: El plato típico de Kralia es el Tumbo.",
    "beto: En Kralia el plato típico se llama Tumbo.",
    "¿Cuál es el plato típico de Kralia?",
    "hugo: El plato típico de Kralia es el Bram.",
    "beto: En Kralia el plato típico se llama Bram.",
    "¿Cuál es el plato típico de Kralia?",
    "# 7. Control: lo que el cuerpo ya sabe no lo pisa un mentiroso",
    "caro: La capital de Francia es Lyon.",
    "¿Cuál es la capital de Francia?",
    "/memoria",
]
AYUDA = """  ENSEÑAR:    fuente: frase         (ej.  ana: La capital de Zorblandia es Mipol)
  PREGUNTAR:  escribe la pregunta   (ej.  ¿Cuál es la capital de Zorblandia?)
  /memoria  células con peso y estado   /reputacion  voz de cada fuente   /ayuda   /salir
  Regla v1: lo enseñado entra EN CUARENTENA; afirmo cuando el PESO (suma de la reputación de fuentes distintas)
  llega a 2. Una fuente pierde reputación cuando lo que dijo fue contradicho por lo que otros confirmaron."""


def ensenar(c, col, col0, fuente, frase):
    x = frank.extrae(c, frase)
    antes = dict(col.rep)
    suc, cel = col.ensena(fuente, frase, x["valor"], x["atributo"])
    suc0, cel0 = col0.ensena(fuente, frase, x["valor"], x["atributo"])
    print(f"   [cuerpo] dato extraído: «{x['valor'] or '(no pude extraerlo)'}» (atributo «{x['atributo']}», {x['seg']:.1f} s)")
    if "nace" in suc:
        print(f"   [colonia] nace la célula #{cel.id} como HIPÓTESIS (fuente: {fuente}, peso {col.W(cel):.2f}). EN CUARENTENA.")
    elif "repite" in suc:
        print(f"   [colonia] {fuente} ya había dicho esto (célula #{cel.id}): la misma fuente no suma. Peso {col.W(cel):.2f}.")
    elif "confirma" in suc:
        print(f"   [colonia] {fuente} CONFIRMA la célula #{cel.id}: fuentes {', '.join(sorted(set(cel.fuentes)))}, peso {col.W(cel):.2f} "
              f"({' + '.join(f'{f} {col.rep_de(f):.2f}' for f in sorted(set(cel.fuentes)))}).")
    if col.validada(cel):
        print(f"   [colonia] célula #{cel.id} VALIDADA (peso {col.W(cel):.2f} >= 2): la afirmo.")
    else:
        print(f"   [colonia] célula #{cel.id} sigue HIPÓTESIS (peso {col.W(cel):.2f} < 2): no la afirmo.")
    for o in col.rivales(cel)[:2]:
        print(f"   [colonia] rival: célula #{o.id} ({col.estado(o)}, peso {col.W(o):.2f}, {', '.join(sorted(set(o.fuentes)))}) dice «{o.frases[0][1]}».")
    for f in sorted(col.rep):
        if abs(col.rep[f] - antes.get(f, 1.0)) > 1e-9:
            flecha = "PIERDE" if col.rep[f] < antes.get(f, 1.0) else "RECUPERA"
            print(f"   [reputación] {f} {flecha} voz: {antes.get(f, 1.0):.2f} -> {col.rep[f]:.2f} "
                  f"({'lo que dijo fue contradicho por lo confirmado' if flecha == 'PIERDE' else 'lo que dijo quedó confirmado'}).")
    if col0.validada(cel0) and not col.validada(cel):
        print(f"   [v0 habría dicho] VALIDADA con {cel0.soporte} fuentes: el cómplice cuenta. En v1 pesa {col.W(cel):.2f}.")


def preguntar(c, col, col0, q, cuenta):
    r = frank.responde_c(c, col, q)
    r0 = frank.responde_c(c, col0, q)
    cuenta["n"] += 1
    cuenta["escala"] += bool(r["duda"])
    marca = {"validado": "AFIRMO (validado por " + ", ".join(r.get("fuentes", [])) + f", peso {r.get('W', 0)})",
             "duda": "DUDA -> escalaría a un modelo grande",
             "nada": "NO LO SÉ -> escalaría a un modelo grande",
             "cuerpo": "lo sabe el cuerpo (nada enseñado)",
             "cuerpo+hipotesis_sin_voz": "lo sabe el cuerpo; lo enseñado sin validar no pisa"}[r["via"]]
    print(f"   [v1: {marca}]  ({r['seg']:.1f} s)")
    print(f"   >> {r['texto']}")
    if r0["texto"] != r["texto"]:
        print(f"   [v0 habría dicho] {r0['texto'][:110]}")
    else:
        print(f"   [v0 habría dicho lo mismo]")


def memoria(col):
    if not col.celulas:
        print("   (vacía)")
    for cel in col.celulas:
        print(f"   #{cel.id} {col.estado(cel):9s} peso {col.W(cel):.2f} ({', '.join(sorted(set(cel.fuentes)))}) "
              f"{cel.estado_grupo or '':7s} «{cel.frases[0][1]}»")


def reputacion(col):
    if not col.rep:
        print("   (nadie ha hablado)")
    for f in sorted(col.rep):
        barra = "#" * int(round(col.rep[f] * 10))
        print(f"   {f:8s} {col.rep[f]:.2f} {barra}")


def main():
    guion = "--guion" in sys.argv
    print("Frankenstein v1 — arrancando el cuerpo (Qwen2.5-1.5B, CPU, 4 hilos)...")
    with Cuerpo() as c:
        print(f"listo en {c.seg_carga:.1f} s.\n{AYUDA}\n")
        col = Colonia(k=2, reputacion=True, recencia=True)
        col0 = Colonia(k=2)
        cuenta, lineas = {"n": 0, "escala": 0}, iter(GUION)
        while True:
            try:
                s = next(lineas) if guion else input("tú> ").strip()
            except (StopIteration, EOFError, KeyboardInterrupt):
                break
            if guion:
                print(("\n" + s) if s.startswith("#") else ("tú> " + s))
            if not s or s.startswith("#"):
                continue
            if s in ("/salir", "salir", "/q"):
                break
            if s == "/ayuda":
                print(AYUDA)
            elif s == "/memoria":
                memoria(col)
            elif s == "/reputacion":
                reputacion(col)
            elif ":" in s and not s.startswith("¿") and len(s.split(":", 1)[0].split()) == 1 and s.split(":", 1)[1].strip():
                fuente, frase = s.split(":", 1)
                ensenar(c, col, col0, fuente.strip().lower(), frase.strip())
            else:
                preguntar(c, col, col0, s, cuenta)
            print()
        print(f"\nPreguntas: {cuenta['n']}; escalaría a un modelo grande: {cuenta['escala']}. Cerrando el cuerpo.")


if __name__ == "__main__":
    main()
