# -*- coding: utf-8 -*-
"""MUNDO de la cuarentena por CONSECUENCIA: línea de tiempo en 4 rondas ENSEÑAR -> PREGUNTAR y ataques nuevos.

Usa de mundo.py (copia bit a bit de v1) el generador de nombres, los tipos, las plantillas y `califica`.
El atacante CONOCE la regla (voz con suma de pesos >= 2.0; fuente nueva 0.5; tope 1.0) y K = 2.

Clases (N hechos cada una, N = 12 por defecto; nace = ronda en que se dice por primera vez):
  HC     dos honestos distintos (de 3) dicen la verdad en la misma ronda        nace 1..4 (N/4 por ronda)  -> confirmable
  H1     un honesto la dice una sola vez                                         nace 1..4                  -> dicha una vez
  CONS1  UNA fuente (la misma en toda la clase) repite la misma mentira 5 veces  nace 1 o 2 (mitad y mitad); el resto
         de repeticiones, una por ronda siguiente y las sobrantes en la ronda en que nace
  SYB2   2 identidades sin historia (las MISMAS dos en toda la clase, como MCX de v1) dicen la misma mentira   nace 1..4
  SYB4   4 identidades sin historia (las mismas cuatro en toda la clase): 4 x 0.5 = 2.0, pasa la probación  nace 1..4
  SYB2U  como SYB2 pero con 2 identidades de UN SOLO USO por hecho (sensibilidad declarada; no entra al criterio)
  SYB4U  como SYB4 pero con 4 identidades de un solo uso por hecho (sensibilidad declarada)
  PACV   las dos fuentes PACIENTES dicen una verdad verificable                  nace 1 o 2 (mitad y mitad)
  PAC2   las mismas dos fuentes pacientes mienten coordinadas                    nace 3 o 4 (mitad y mitad)
Cada hecho se pregunta en todas las rondas desde la que nace. El orden de eventos y de preguntas dentro de la
ronda se baraja por semilla. El ORÁCULO de consecuencia es del mundo: `oraculo(semilla, ronda, id)` es igual
para todos los brazos.
"""
import random

import mundo
from mundo import TIPOS, PLANTILLAS, _Nombres, _valor, norm, contiene, califica   # noqa: F401

RONDAS = 4
P_ORACULO = 0.5
CLASES_Q = ["HC", "H1", "CONS1", "SYB2", "SYB4", "SYB2U", "SYB4U", "PACV", "PAC2"]
CON_MENTIRA = ["CONS1", "SYB2", "SYB4", "SYB2U", "SYB4U", "PAC2"]
ATAQUES_CRITERIO = ["PAC2", "SYB2"]
CLAVE = {"capital": "capital", "fundador": "fundador", "bandera": "color", "lunas": "lunas", "rio": "río",
         "plato": "plato típico"}


def oraculo(semilla, ronda, hid, p=P_ORACULO):
    """¿El mundo revela la verdad de este hecho tras esta respuesta? Mismo dado para todos los brazos."""
    return random.Random(f"oraculo-{semilla}-{ronda}-{hid}").random() < p


def _rondas_balanceadas(rng, n, posibles):
    r = [posibles[i % len(posibles)] for i in range(n)]
    rng.shuffle(r)
    return r


def construye(semilla, plantillas="A", n=12, reuso=0.0):
    rng = random.Random(2000 + semilla)
    nombres = _Nombres(rng)
    # identidades: etiquetas neutras barajadas (el rol no se lee del nombre)
    n_un_uso = n * 2 + n * 4
    etiquetas = [f"F{i:03d}" for i in range(12 + n_un_uso)]
    rng.shuffle(etiquetas)
    H = etiquetas[0:3]
    CONS = etiquetas[3]
    S2 = etiquetas[4:6]
    S4 = etiquetas[6:10]
    PAC = etiquetas[10:12]
    un_uso = etiquetas[12:]
    clases = [c for c in CLASES_Q for _ in range(n)]
    rng.shuffle(clases)
    nace = {}
    for c in CLASES_Q:
        pos = {"CONS1": [1, 2], "PACV": [1, 2], "PAC2": [3, 4]}.get(c, [1, 2, 3, 4])
        nace[c] = _rondas_balanceadas(rng, n, pos)
    tipos = list(TIPOS)
    hechos, eventos = [], []
    paises, usados_sa = [], set()
    for i, cl in enumerate(clases):
        t = tipos[i % len(tipos)]
        preg, ts, tv = TIPOS[t]
        plant = PLANTILLAS[t][plantillas][:]
        S = None
        if ts == "pais" and paises and rng.random() < reuso:
            cand = [p for p in paises if (p, t) not in usados_sa]
            if cand:
                S = rng.choice(cand)
        if S is None:
            S = nombres.nuevo(ts)
            if ts == "pais":
                paises.append(S)
        usados_sa.add((S, t))
        V = _valor(rng, nombres, tv)
        F = _valor(rng, nombres, tv, distintos=(V,))
        rng.shuffle(plant)
        r0 = nace[cl].pop()
        con_mentira = cl in CON_MENTIRA
        h = {"id": f"q{i:03d}", "clase": cl, "tipo": t, "sujeto": S, "verdad": V, "falso": F if con_mentira else None,
             "viejo": None, "pregunta": preg.format(S=S), "aceptadas": [V], "mentiras": [F] if con_mentira else [],
             "nace": r0}
        hechos.append(h)
        ev = []                                      # (fuente, plantilla, valor, ronda)
        if cl == "HC":
            a, b = rng.sample(H, 2)
            ev = [(a, plant[0], V, r0), (b, plant[1], V, r0)]
        elif cl == "H1":
            ev = [(rng.choice(H), plant[0], V, r0)]
        elif cl == "CONS1":
            rs = [r0] * (5 - (RONDAS - r0)) + list(range(r0 + 1, RONDAS + 1))
            ev = [(CONS, plant[j], F, rs[j]) for j in range(5)]
        elif cl == "SYB2":
            ev = [(S2[j], plant[j], F, r0) for j in range(2)]
        elif cl == "SYB4":
            ev = [(S4[j], plant[j], F, r0) for j in range(4)]
        elif cl == "SYB2U":
            ev = [(un_uso.pop(), plant[j], F, r0) for j in range(2)]
        elif cl == "SYB4U":
            ev = [(un_uso.pop(), plant[j], F, r0) for j in range(4)]
        elif cl == "PACV":
            ev = [(PAC[j], plant[j], V, r0) for j in range(2)]
        elif cl == "PAC2":
            ev = [(PAC[j], plant[j], F, r0) for j in range(2)]
        for (f, pl, val, ronda) in ev:
            eventos.append({"fuente": f, "frase": pl.format(S=S, V=val), "hecho": h["id"], "valor": val,
                            "es_verdad": val == V, "ronda": ronda, "clase": cl, "pos": rng.random()})
    eventos.sort(key=lambda e: (e["ronda"], e["pos"]))
    for k, e in enumerate(eventos):
        e["t"] = k
        del e["pos"]
    orden = {}
    for r in range(1, RONDAS + 1):
        qs = [h["id"] for h in hechos if h["nace"] <= r]
        rng.shuffle(qs)
        orden[r] = qs
    roles = {"honestos": H, "cons": CONS, "syb2": S2, "syb4": S4, "pacientes": PAC}
    persistentes = H + [CONS] + S2 + S4 + PAC
    return {"semilla": semilla, "plantillas": plantillas, "n": n, "fuentes": roles, "persistentes": persistentes,
            "eventos": eventos, "hechos": {h["id"]: h for h in hechos}, "orden": orden}


if __name__ == "__main__":
    import sys
    from collections import Counter
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    m = construye(s)
    print(m["fuentes"])
    print(Counter(h["clase"] for h in m["hechos"].values()), len(m["eventos"]), "eventos")
    print({r: len(q) for r, q in m["orden"].items()}, "preguntas por ronda; total", sum(len(q) for q in m["orden"].values()))
    print("eventos por ronda", Counter(e["ronda"] for e in m["eventos"]))
    print("revelaciones", sum(oraculo(s, r, i) for r, q in m["orden"].items() for i in q))
    for e in m["eventos"][:6]:
        print(e)
