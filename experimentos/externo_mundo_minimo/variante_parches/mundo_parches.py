# -*- coding: utf-8 -*-
"""
mundo_parches.py - HIPOTESIS APARTE (una sola modificacion sobre el mundo congelado).

UNA SOLA MODIFICACION: la comida deja de ser una moneda al aire unica y pasa a
estar en DOS PARCHES con probabilidades distintas (0.42 y 0.22, media 0.32, la
misma del mundo congelado), y el organismo toma UNA accion por ronda: elegir
parche. Todo lo demas queda exactamente igual que en el mundo congelado
(metabolic_cost 0.35, threshold 9.0, p_rep 0.02, coste 2.0, hijo 7.5,
max_population 12, rounds 180, founders 2).

Brazos:
  A0-P   : elige parche al azar (uniforme). Probabilidad marginal de comida 0.32.
  E-P    : memoria episodica <= 20 episodios {state, action, reward, outcome};
           elige el parche con mejor recompensa media reciente; exploracion
           epsilon = 0.1 DECLARADA.
  BARAJA-P: control. Identico a E-P salvo que, antes de decidir, las ETIQUETAS DE
           ACCION de los episodios guardados se permutan al azar. Esto rompe la
           contingencia accion<->recompensa conservando las mismas estadisticas
           marginales. NOTA HONESTA: barajar solo el ORDEN de los episodios seria
           un no-op, porque la media es invariante al orden; el control util es
           permutar la etiqueta de accion.

PRNG: dos flujos deterministas por semilla, declarados:
  - mundo:   random.Random(seed)            -> mezcla, comida, reproduccion
  - politica: random.Random(seed + 10**6)   -> eleccion de parche, epsilon,
                                               desempates, barajado del control
Se separan para que la dinamica del mundo consuma el flujo en el mismo orden en
los tres brazos. Un solo proceso; prohibido multiprocessing.
"""

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mundo_minimo import PARAMS_A0, Organismo, metricas  # noqa: E402

VERSION = "1.0.0"

PARCHES = (0.42, 0.22)          # media 0.32
EPSILON = 0.1
MEMORY_CAP = 20
POLICY_SEED_OFFSET = 10 ** 6


def _medias_por_parche(memoria):
    sumas = [0.0, 0.0]
    cuentas = [0, 0]
    for (_s, a, r, _o) in memoria:
        sumas[a] += r
        cuentas[a] += 1
    return sumas, cuentas


def _elige_greedy(memoria, prng, barajar):
    """Regla de E-P (y de BARAJA-P con barajar=True). Consume prng."""
    if barajar and memoria:
        acciones = [e[1] for e in memoria]
        prng.shuffle(acciones)
        memoria = [(e[0], acciones[i], e[2], e[3])
                   for i, e in enumerate(memoria)]
    if prng.random() < EPSILON:                    # exploracion declarada
        return 0 if prng.random() < 0.5 else 1, "explore"
    sumas, cuentas = _medias_por_parche(memoria)
    sin_datos = [a for a in (0, 1) if cuentas[a] == 0]
    if len(sin_datos) == 2:
        return (0 if prng.random() < 0.5 else 1), "sin_datos"
    if len(sin_datos) == 1:
        return sin_datos[0], "sin_datos"
    m0 = sumas[0] / cuentas[0]
    m1 = sumas[1] / cuentas[1]
    if m0 > m1:
        return 0, "greedy"
    if m1 > m0:
        return 1, "greedy"
    return (0 if prng.random() < 0.5 else 1), "empate"


def simular_semilla(seed, brazo="A0-P", params=None, parches=PARCHES,
                    memory_cap=MEMORY_CAP):
    """brazo en {"A0-P", "E-P", "BARAJA-P"}."""
    p = params if params is not None else PARAMS_A0
    usa_memoria = brazo in ("E-P", "BARAJA-P")
    barajar = (brazo == "BARAJA-P")
    cap = memory_cap if usa_memoria else 0

    rng = random.Random(seed)
    prng = random.Random(seed + POLICY_SEED_OFFSET)

    metabolic_cost = p["metabolic_cost"]
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
        o = Organismo(next_id, i, None, 0, p["initial_energy"], 0, cap)
        next_id += 1
        todos.append(o)
        vivos.append(o)

    episodios_totales = 0
    elecciones = 0
    elecciones_parche_rico = 0

    for ronda in range(1, n_rounds + 1):
        if not vivos:
            break
        orden = list(vivos)
        rng.shuffle(orden)                                   # paso 1
        for org in orden:
            if not org.alive:
                continue
            e0 = org.energy
            # ACCION (unica modificacion): elegir parche
            if usa_memoria:
                accion, _modo = _elige_greedy(org.memory, prng, barajar)
            else:
                accion = 0 if prng.random() < 0.5 else 1
            elecciones += 1
            if accion == 0:
                elecciones_parche_rico += 1

            org.energy -= metabolic_cost                     # paso 2
            if rng.random() < parches[accion]:               # paso 3
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
                                         ronda, cap)
                        next_id += 1
                        todos.append(hijo)
                        vivos.append(hijo)
                        org.children.append(hijo.oid)        # pasos 7 y 8
                        outcome = "reproduced"
            if cap > 0:
                org.recordar((round(e0, 4), accion, reward, outcome), cap)
                episodios_totales += 1

    extra = {
        "arm": brazo,
        "choices": elecciones,
        "rich_patch_choices": elecciones_parche_rico,
        "rich_patch_fraction": (elecciones_parche_rico / float(elecciones)
                                if elecciones else 0.0),
    }
    return metricas(seed, todos, vivos, n_rounds, episodios_totales, cap, extra)


def agregar_parches(per_seed):
    from mundo_minimo import agregar
    ag = agregar(per_seed)
    n = float(len(per_seed))
    ag["mean_rich_patch_fraction"] = sum(
        r["rich_patch_fraction"] for r in per_seed) / n
    return ag
