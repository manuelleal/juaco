# -*- coding: utf-8 -*-
"""
mundo_minimo.py - linea externa "mundo minimo" (protocolo ChatGPT, 18-sep-2026).

Ecologia de juguete. NO es el organismo JUACO: sin retina, sin valor, sin codigo.
Sus numeros no entran en la escalera del proyecto; sirven para calibrar R0.

Dinamica por ronda (literal del protocolo):
  1. Mezclar al azar el orden de los organismos vivos (snapshot al inicio de ronda).
  2. Cada organismo paga energy -= metabolic_cost.
  3. Con probabilidad food_probability recibe energy += food_energy.
  4. Si energy <= 0 muere (inmediata e irreversible).
  5. Si sigue vivo y energy >= reproduction_threshold puede reproducirse con
     probabilidad reproduction_probability si hay espacio (poblacion < max_population).
  6. Al reproducirse: parent.energy -= reproduction_cost; hijo con newborn_initial_energy.
  7. El hijo hereda SOLO el identificador de linaje.  8. ID nuevo.

Decisiones de implementacion que el protocolo no fija (declaradas, no ocultas):
  D1. Los pasos 2..6 se aplican organismo por organismo, en el orden mezclado
      (no por fases). Es la unica lectura en que la mezcla del paso 1 tiene efecto
      sobre el consumo del PRNG y sobre la disputa del ultimo hueco de poblacion.
  D2. El recien nacido NO actua en la ronda en que nace (el orden se fija al inicio
      de la ronda). Actua desde la ronda siguiente.
  D3. La tirada de reproduccion (prob 0.02) se consume SOLO si hay espacio
      (poblacion viva < max_population) y la energia alcanza el umbral.
  D4. Un organismo que muere en el paso 4 no tira reproduccion.

PRNG: un random.Random(seed) por semilla, consumido en el orden exacto de la
      dinamica. Prohibido multiprocessing; un solo proceso.
"""

import random

VERSION = "1.0.0"

PARAMS_A0 = {
    "founders": 2,
    "initial_energy": 10.0,
    "metabolic_cost": 0.35,
    "food_probability": 0.32,
    "food_energy": 1.0,
    "reproduction_threshold": 9.0,
    "reproduction_probability": 0.02,
    "reproduction_cost": 2.0,
    "newborn_initial_energy": 7.5,
    "max_population": 12,
    "rounds": 180,
}


class Organismo(object):
    __slots__ = ("oid", "lineage", "parent", "generation", "energy",
                 "birth_round", "death_round", "children", "memory", "alive")

    def __init__(self, oid, lineage, parent, generation, energy, birth_round,
                 memory_cap=0):
        self.oid = oid
        self.lineage = lineage
        self.parent = parent
        self.generation = generation
        self.energy = energy
        self.birth_round = birth_round
        self.death_round = None
        self.children = []
        self.memory = [] if memory_cap > 0 else None
        self.alive = True

    def recordar(self, episodio, memory_cap):
        """Memoria episodica minima, local, limitada. NO consume PRNG."""
        m = self.memory
        m.append(episodio)
        if len(m) > memory_cap:
            del m[0]


def simular_semilla(seed, params=None, agente="A0", memory_cap=0):
    """Corre una semilla del mundo congelado (sin accion).

    agente: "A0" (sin memoria) o "E" (memoria episodica minima {state, action,
    reward, outcome}, local, <= memory_cap episodios).

    En este mundo el organismo no toma NINGUNA accion: la comida es una moneda al
    aire independiente del organismo. La memoria de E SOLO registra; no consume
    PRNG ni altera ninguna rama de la dinamica. Por construccion A0 == E semilla
    a semilla; si difieren, es error de implementacion.
    """
    p = params if params is not None else PARAMS_A0
    if agente == "E" and memory_cap <= 0:
        memory_cap = 20
    if agente == "A0":
        memory_cap = 0

    rng = random.Random(seed)

    metabolic_cost = p["metabolic_cost"]
    food_probability = p["food_probability"]
    food_energy = p["food_energy"]
    rep_threshold = p["reproduction_threshold"]
    rep_probability = p["reproduction_probability"]
    rep_cost = p["reproduction_cost"]
    newborn_energy = p["newborn_initial_energy"]
    max_population = p["max_population"]
    n_rounds = p["rounds"]

    todos = []
    vivos = []
    next_id = 0
    for i in range(p["founders"]):
        o = Organismo(next_id, i, None, 0, p["initial_energy"], 0, memory_cap)
        next_id += 1
        todos.append(o)
        vivos.append(o)

    episodios_totales = 0

    for ronda in range(1, n_rounds + 1):
        if not vivos:
            break
        orden = list(vivos)           # snapshot al inicio de la ronda (D2)
        rng.shuffle(orden)            # paso 1
        for org in orden:
            if not org.alive:
                continue
            e0 = org.energy
            org.energy -= metabolic_cost                     # paso 2
            if rng.random() < food_probability:              # paso 3
                org.energy += food_energy
                reward = food_energy
            else:
                reward = 0.0
            if org.energy <= 0.0:                            # paso 4
                org.alive = False
                org.death_round = ronda
                vivos.remove(org)
                outcome = "dead"
            else:
                outcome = "alive"
                if org.energy >= rep_threshold and len(vivos) < max_population:
                    if rng.random() < rep_probability:       # paso 5
                        org.energy -= rep_cost               # paso 6
                        hijo = Organismo(next_id, org.lineage, org.oid,
                                         org.generation + 1, newborn_energy,
                                         ronda, memory_cap)
                        next_id += 1
                        todos.append(hijo)
                        vivos.append(hijo)
                        org.children.append(hijo.oid)        # pasos 7 y 8
                        outcome = "reproduced"
            if memory_cap > 0:
                # {state, action, reward, outcome}: action = None (no hay accion)
                org.recordar((round(e0, 4), None, reward, outcome), memory_cap)
                episodios_totales += 1

    return metricas(seed, todos, vivos, n_rounds, episodios_totales, memory_cap)


def metricas(seed, todos, vivos, n_rounds, episodios_totales, memory_cap,
             extra=None):
    founders = [o for o in todos if o.parent is None]
    hijos_f = [len(f.children) for f in founders]
    r0_seed = sum(hijos_f) / float(len(founders))

    by_id = dict((o.oid, o) for o in todos)
    desc = {}
    for f in founders:
        n = 0
        pila = list(f.children)
        while pila:
            cid = pila.pop()
            n += 1
            pila.extend(by_id[cid].children)
        desc[f.oid] = n

    lin_vivos = set(o.lineage for o in vivos)
    lifespans = []
    for o in todos:
        fin = o.death_round if o.death_round is not None else n_rounds
        lifespans.append(fin - o.birth_round)
    max_gen = max(o.generation for o in todos)

    out = {
        "seed": seed,
        "R0_seed": r0_seed,
        "children_founder_0": hijos_f[0],
        "children_founder_1": hijos_f[1] if len(hijos_f) > 1 else 0,
        "descendants_founder_0": desc[founders[0].oid],
        "descendants_founder_1": desc[founders[1].oid] if len(founders) > 1 else 0,
        "final_population": len(vivos),
        "extinct": len(vivos) == 0,
        "total_organisms": len(todos),
        "lineage_0_survives": 0 in lin_vivos,
        "lineage_1_survives": 1 in lin_vivos,
        "mean_survival_time": sum(lifespans) / float(len(lifespans)),
        "number_of_generations": max_gen,
        "memory_usage_episodes": episodios_totales,
        "memory_cap": memory_cap,
    }
    if extra:
        out.update(extra)
    out["_genealogy"] = [
        {"id": o.oid, "lin": o.lineage, "par": o.parent, "gen": o.generation,
         "b": o.birth_round, "d": o.death_round, "ch": list(o.children)}
        for o in todos
    ]
    return out


def agregar(per_seed):
    """Agregados sobre las semillas."""
    n = float(len(per_seed))
    r0 = sum(r["R0_seed"] for r in per_seed) / n
    ext = sum(1 for r in per_seed if r["extinct"]) / n
    pop = sum(r["final_population"] for r in per_seed) / n
    lin = (sum(1 for r in per_seed if r["lineage_0_survives"]) +
           sum(1 for r in per_seed if r["lineage_1_survives"])) / (2.0 * n)
    desc = sum(r["descendants_founder_0"] + r["descendants_founder_1"]
               for r in per_seed) / (2.0 * n)
    surv = sum(r["mean_survival_time"] for r in per_seed) / n
    gens = sum(r["number_of_generations"] for r in per_seed) / n
    mem = sum(r["memory_usage_episodes"] for r in per_seed) / n
    return {
        "n_seeds": int(n),
        "R0": r0,
        "extinction_rate": ext,
        "mean_final_population": pop,
        "lineage_survival": lin,
        "descendants_per_founder": desc,
        "mean_survival_time": surv,
        "number_of_generations": gens,
        "mean_memory_episodes_per_seed": mem,
    }


if __name__ == "__main__":
    import json
    res = [simular_semilla(s) for s in range(1000)]
    print(json.dumps(agregar(res), indent=2))
