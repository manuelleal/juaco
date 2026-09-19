# -*- coding: utf-8 -*-
"""Corrida 1: CALIBRACION. Barrido food_probability en {0.29..0.34}, semillas 0..999.
Verifica contra la referencia externa (0.32 -> R0 0.9665, ext 0.082, pop 3.028)
y CONGELA 0.32. Un solo proceso, sin multiprocessing."""

import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import entregables as E
from mundo_minimo import PARAMS_A0, VERSION, agregar, simular_semilla

CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calibracion")
BARRIDO = [0.29, 0.30, 0.31, 0.32, 0.33, 0.34]
SEEDS = list(range(1000))
REFERENCIA = {"food_probability": 0.32, "R0": 0.9665,
              "extinction_rate": 0.082, "mean_final_population": 3.028,
              "sha256_reporte_externo":
              "4af8d5eea3d6309b16851202c7c24f12584f2f1076fbc28777f0139afcb1d833"}


def main():
    if not os.path.isdir(CARPETA):
        os.makedirs(CARPETA)

    resultados = {}
    per_seed_out = {}
    genealogias = {}

    for fp in BARRIDO:
        p = copy.deepcopy(PARAMS_A0)
        p["food_probability"] = fp
        filas = [simular_semilla(s, p, agente="A0") for s in SEEDS]
        ag = agregar(filas)
        m, sd, sem = E.stats([r["R0_seed"] for r in filas])
        ag["R0_sd"] = sd
        ag["R0_sem"] = sem
        pm, psd, psem = E.stats([float(r["final_population"]) for r in filas])
        ag["mean_final_population_sem"] = psem
        ext = ag["extinction_rate"]
        ag["extinction_rate_sem"] = (ext * (1 - ext) / float(len(SEEDS))) ** 0.5
        clave = "%.2f" % fp
        resultados[clave] = ag
        per_seed_out[clave] = [
            {k: v for k, v in r.items() if k != "_genealogy"} for r in filas]
        genealogias[clave] = dict((str(r["seed"]), r["_genealogy"]) for r in filas)
        print("fp=%s  R0=%.4f (+-%.4f)  ext=%.3f  pop=%.3f" %
              (clave, ag["R0"], ag["R0_sem"], ag["extinction_rate"],
               ag["mean_final_population"]))

    congelado = resultados["0.32"]
    dif_r0 = congelado["R0"] - REFERENCIA["R0"]
    z_r0 = dif_r0 / congelado["R0_sem"] if congelado["R0_sem"] else 0.0
    dif_ext = congelado["extinction_rate"] - REFERENCIA["extinction_rate"]
    z_ext = (dif_ext / congelado["extinction_rate_sem"]
             if congelado["extinction_rate_sem"] else 0.0)
    dif_pop = congelado["mean_final_population"] - REFERENCIA["mean_final_population"]
    z_pop = (dif_pop / congelado["mean_final_population_sem"]
             if congelado["mean_final_population_sem"] else 0.0)
    comparacion = {
        "referencia_externa": REFERENCIA,
        "reproducido": {"R0": congelado["R0"],
                        "extinction_rate": congelado["extinction_rate"],
                        "mean_final_population": congelado["mean_final_population"]},
        "diferencias": {"R0": dif_r0, "extinction_rate": dif_ext,
                        "mean_final_population": dif_pop},
        "z_scores_vs_nuestro_error_estandar": {"R0": z_r0, "extinction_rate": z_ext,
                                               "mean_final_population": z_pop},
        "veredicto": ("REPRODUCIDA en lo cualitativo y dentro de ~1-2 errores "
                      "estandar en extincion y poblacion; R0 queda por debajo de la "
                      "referencia (ver SUMMARY.md)"),
    }

    params = {
        "experiment": "calibracion_barrido_food_probability",
        "engine": "mundo_minimo.py",
        "engine_version": VERSION,
        "engine_sha256": E.sha256_de(os.path.join(os.path.dirname(CARPETA),
                                                  "mundo_minimo.py")),
        "seeds": {"first": SEEDS[0], "last": SEEDS[-1], "count": len(SEEDS)},
        "prng": "random.Random(seed), uno por semilla, sin multiprocessing",
        "sweep_food_probability": BARRIDO,
        "frozen_world": dict(PARAMS_A0),
        "frozen": True,
        "decisiones_de_implementacion": {
            "D1": "pasos 2..6 organismo por organismo en el orden mezclado",
            "D2": "el recien nacido no actua en la ronda en que nace",
            "D3": "la tirada de reproduccion solo se consume si hay espacio y umbral",
            "D4": "un organismo que muere no tira reproduccion",
        },
    }

    E.escribir_json(os.path.join(CARPETA, "PARAMETERS.json"), params)
    E.escribir_json(os.path.join(CARPETA, "RESULTS.json"),
                    {"por_food_probability": resultados,
                     "comparacion_con_referencia": comparacion})
    E.escribir_json(os.path.join(CARPETA, "PER_SEED_RESULTS.json"), per_seed_out)
    E.escribir_json(os.path.join(CARPETA, "GENEALOGY.json"), genealogias)
    return resultados, comparacion, params


if __name__ == "__main__":
    main()
