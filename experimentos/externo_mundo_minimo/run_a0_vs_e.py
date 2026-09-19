# -*- coding: utf-8 -*-
"""Corrida 2: A0 contra E en el mundo CONGELADO (food_probability = 0.32).

PREDICCION ESCRITA ANTES DE CORRER (del coordinador, 18-sep-2026 19:20):
  En este mundo el organismo no toma NINGUNA accion: la comida es una moneda al
  aire independiente del organismo. Una memoria episodica no puede cambiar nada
  porque no hay decision que informar. Por lo tanto A0 == E en TODAS las metricas,
  SEMILLA A SEMILLA. Si E difiere, es un error de implementacion (PRNG consumido
  de forma distinta), no un efecto.

E se implementa de modo que NO consuma PRNG adicional: la memoria solo registra
{state, action, reward, outcome} (action = None, no hay accion), local, <= 20
episodios, sin acceso global, sin futuro, sin otros organismos.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import entregables as E
from mundo_minimo import PARAMS_A0, VERSION, agregar, simular_semilla

BASE = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.join(BASE, "a0_vs_e")
SEEDS = list(range(1000))
MEMORY_CAP = 20

CAMPOS = ["R0_seed", "children_founder_0", "children_founder_1",
          "descendants_founder_0", "descendants_founder_1", "final_population",
          "extinct", "total_organisms", "lineage_0_survives",
          "lineage_1_survives", "mean_survival_time", "number_of_generations"]

PREDICCION = ("A0 == E en todas las metricas, semilla a semilla, porque en este "
              "mundo no hay accion que la memoria pueda informar. Si difieren es "
              "un error de implementacion (PRNG), no un efecto.")


def main():
    if not os.path.isdir(CARPETA):
        os.makedirs(CARPETA)

    a0 = [simular_semilla(s, PARAMS_A0, agente="A0") for s in SEEDS]
    ee = [simular_semilla(s, PARAMS_A0, agente="E", memory_cap=MEMORY_CAP)
          for s in SEEDS]

    discrepancias = []
    genealogia_identica = 0
    for ra, re_ in zip(a0, ee):
        dif = {}
        for c in CAMPOS:
            if ra[c] != re_[c]:
                dif[c] = [ra[c], re_[c]]
        if ra["_genealogy"] == re_["_genealogy"]:
            genealogia_identica += 1
        else:
            dif["_genealogy"] = "distinta"
        if dif:
            discrepancias.append({"seed": ra["seed"], "dif": dif})

    ag_a0 = agregar(a0)
    ag_e = agregar(ee)
    identidad = (len(discrepancias) == 0 and genealogia_identica == len(SEEDS))

    resultados = {
        "prediccion_preregistrada": PREDICCION,
        "A0": ag_a0,
        "E": ag_e,
        "comparacion_pareada": {
            "seeds_comparadas": len(SEEDS),
            "campos_comparados": CAMPOS + ["_genealogy"],
            "seeds_con_alguna_discrepancia": len(discrepancias),
            "seeds_con_genealogia_identica": genealogia_identica,
            "identidad_exacta_semilla_a_semilla": identidad,
            "delta_R0": ag_e["R0"] - ag_a0["R0"],
            "delta_extinction_rate": (ag_e["extinction_rate"] -
                                      ag_a0["extinction_rate"]),
            "delta_mean_final_population": (ag_e["mean_final_population"] -
                                            ag_a0["mean_final_population"]),
            "discrepancias": discrepancias[:50],
        },
        "memory_usage": {
            "memory_cap_por_organismo": MEMORY_CAP,
            "episodios_registrados_media_por_semilla":
                ag_e["mean_memory_episodes_per_seed"],
            "A0_no_tiene_memoria": ag_a0["mean_memory_episodes_per_seed"] == 0.0,
        },
        "veredicto": ("IDENTIDAD CONFIRMADA: E no cambia nada, como estaba "
                      "predicho. No es un exito de la memoria; es la prueba de "
                      "que este mundo no puede testear la memoria."
                      if identidad else
                      "FAIL DE IMPLEMENTACION: E difiere de A0. Revisar consumo "
                      "de PRNG."),
    }

    params = {
        "experiment": "A0_vs_E_mundo_congelado",
        "engine": "mundo_minimo.py",
        "engine_version": VERSION,
        "engine_sha256": E.sha256_de(os.path.join(BASE, "mundo_minimo.py")),
        "frozen_world": dict(PARAMS_A0),
        "frozen": True,
        "seeds": {"first": SEEDS[0], "last": SEEDS[-1], "count": len(SEEDS)},
        "prng": "random.Random(seed), uno por semilla; E no consume PRNG extra",
        "arms": {
            "A0": "sin memoria",
            "E": ("A0 + memoria episodica minima {state, action, reward, "
                  "outcome}, local, <= %d episodios, solo registra" % MEMORY_CAP),
        },
        "changed_mechanism": "una sola modificacion: se anade memoria episodica a E",
        "prediccion_preregistrada": PREDICCION,
    }

    E.escribir_json(os.path.join(CARPETA, "PARAMETERS.json"), params)
    E.escribir_json(os.path.join(CARPETA, "RESULTS.json"), resultados)
    E.escribir_json(os.path.join(CARPETA, "PER_SEED_RESULTS.json"), {
        "A0": [{k: v for k, v in r.items() if k != "_genealogy"} for r in a0],
        "E": [{k: v for k, v in r.items() if k != "_genealogy"} for r in ee],
    })
    E.escribir_json(os.path.join(CARPETA, "GENEALOGY.json"), {
        "A0": dict((str(r["seed"]), r["_genealogy"]) for r in a0),
        "E": dict((str(r["seed"]), r["_genealogy"]) for r in ee),
    })

    print("A0: R0=%.4f ext=%.3f pop=%.3f" %
          (ag_a0["R0"], ag_a0["extinction_rate"], ag_a0["mean_final_population"]))
    print("E : R0=%.4f ext=%.3f pop=%.3f" %
          (ag_e["R0"], ag_e["extinction_rate"], ag_e["mean_final_population"]))
    print("identidad exacta semilla a semilla:", identidad,
          "| discrepancias:", len(discrepancias),
          "| genealogias identicas:", genealogia_identica)
    return ag_a0, ag_e, resultados, params


if __name__ == "__main__":
    main()
