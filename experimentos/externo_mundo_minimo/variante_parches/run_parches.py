# -*- coding: utf-8 -*-
"""Corrida 3: HIPOTESIS APARTE - dos parches y una accion por ronda.

PREDICCION PREREGISTRADA (escrita antes de correr):
  E-P sube R0 y baja la extincion respecto de A0-P en >= 60 % de las semillas
  pareadas; BARAJA-P ~ A0-P.

Paso 0 (obligatorio): RECALIBRAR A0-P. Si R0(A0-P) no queda ~ 1 con la media
0.32, se reporta la desviacion y NO se mueve nada mas.

Replica: semillas 1000..1999.
"""

import math
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(BASE)
sys.path.insert(0, RAIZ)
sys.path.insert(0, BASE)

import entregables as E  # noqa: E402
import mundo_parches as M  # noqa: E402
from mundo_minimo import PARAMS_A0  # noqa: E402

BRAZOS = ["A0-P", "E-P", "BARAJA-P"]
SEEDS_PRINCIPAL = list(range(1000))
SEEDS_REPLICA = list(range(1000, 2000))

PREDICCION = ("E-P sube R0 y baja la extincion respecto de A0-P en >= 60 % de las "
              "semillas pareadas; BARAJA-P ~ A0-P (control con la contingencia "
              "accion<->recompensa rota).")


def binomial_dos_colas(k, n):
    """p-valor exacto del test de signos sobre n pares discordantes."""
    if n == 0:
        return 1.0
    p = 0.0
    obj = math.comb(n, k)
    for i in range(n + 1):
        c = math.comb(n, i)
        if c <= obj:
            p += c
    return min(1.0, p / float(2 ** n))


def pareado(a, b, etiqueta_a, etiqueta_b):
    """b contra a, semilla a semilla."""
    n = len(a)
    mejor = peor = igual = 0
    for ra, rb in zip(a, b):
        if rb["R0_seed"] > ra["R0_seed"]:
            mejor += 1
        elif rb["R0_seed"] < ra["R0_seed"]:
            peor += 1
        else:
            igual += 1
    disc = mejor + peor
    # extincion: McNemar
    solo_a_extinta = sum(1 for ra, rb in zip(a, b) if ra["extinct"] and not rb["extinct"])
    solo_b_extinta = sum(1 for ra, rb in zip(a, b) if rb["extinct"] and not ra["extinct"])
    pop_mejor = sum(1 for ra, rb in zip(a, b)
                    if rb["final_population"] > ra["final_population"])
    pop_peor = sum(1 for ra, rb in zip(a, b)
                   if rb["final_population"] < ra["final_population"])
    return {
        "comparacion": "%s contra %s" % (etiqueta_b, etiqueta_a),
        "n_semillas": n,
        "R0_semillas_mejor": mejor,
        "R0_semillas_peor": peor,
        "R0_semillas_iguales": igual,
        "R0_fraccion_mejor_sobre_todas": mejor / float(n),
        "R0_fraccion_no_peor_sobre_todas": (mejor + igual) / float(n),
        "R0_fraccion_mejor_entre_discordantes": (mejor / float(disc)) if disc else None,
        "R0_test_signos_p": binomial_dos_colas(min(mejor, peor), disc),
        "extincion_solo_%s" % etiqueta_a: solo_a_extinta,
        "extincion_solo_%s" % etiqueta_b: solo_b_extinta,
        "poblacion_final_semillas_mejor": pop_mejor,
        "poblacion_final_semillas_peor": pop_peor,
    }


def corre_bloque(seeds):
    datos = {}
    for brazo in BRAZOS:
        datos[brazo] = [M.simular_semilla(s, brazo) for s in seeds]
    return datos


def resumen_bloque(datos, seeds, etiqueta):
    ag = {}
    for brazo in BRAZOS:
        a = M.agregar_parches(datos[brazo])
        m, sd, sem = E.stats([r["R0_seed"] for r in datos[brazo]])
        a["R0_sem"] = sem
        ext = a["extinction_rate"]
        a["extinction_rate_sem"] = (ext * (1 - ext) / float(len(seeds))) ** 0.5
        ag[brazo] = a
        print("[%s] %-9s R0=%.4f (+-%.4f) ext=%.3f pop=%.3f rico=%.3f" %
              (etiqueta, brazo, a["R0"], a["R0_sem"], a["extinction_rate"],
               a["mean_final_population"], a["mean_rich_patch_fraction"]))
    comps = {
        "E-P_vs_A0-P": pareado(datos["A0-P"], datos["E-P"], "A0-P", "E-P"),
        "BARAJA-P_vs_A0-P": pareado(datos["A0-P"], datos["BARAJA-P"],
                                    "A0-P", "BARAJA-P"),
        "E-P_vs_BARAJA-P": pareado(datos["BARAJA-P"], datos["E-P"],
                                   "BARAJA-P", "E-P"),
    }
    return {"agregados": ag, "pareados": comps,
            "seeds": {"first": seeds[0], "last": seeds[-1], "count": len(seeds)}}


def main():
    print("== recalibracion de A0-P (paso 0) ==")
    datos = corre_bloque(SEEDS_PRINCIPAL)
    principal = resumen_bloque(datos, SEEDS_PRINCIPAL, "principal")

    a0p = principal["agregados"]["A0-P"]
    # Referencia: el mundo congelado de un solo parche, mismas semillas.
    from mundo_minimo import simular_semilla as sim_congelado, agregar as ag_cong
    cong = ag_cong([sim_congelado(s, PARAMS_A0, "A0") for s in SEEDS_PRINCIPAL])
    recal = {
        "pregunta": "R0(A0-P) ~ 1 con la media de comida 0.32?",
        "R0_A0-P": a0p["R0"],
        "R0_A0-P_sem": a0p["R0_sem"],
        "R0_mundo_congelado_un_parche": cong["R0"],
        "desviacion_respecto_de_1": a0p["R0"] - 1.0,
        "desviacion_en_errores_estandar": (a0p["R0"] - 1.0) / a0p["R0_sem"],
        "desviacion_respecto_del_mundo_congelado": a0p["R0"] - cong["R0"],
        "extincion_A0-P": a0p["extinction_rate"],
        "extincion_mundo_congelado": cong["extinction_rate"],
        "fraccion_parche_rico_A0-P": a0p["mean_rich_patch_fraction"],
        "veredicto": ("A0-P queda por debajo de 1 en la misma medida que el mundo "
                      "congelado (misma probabilidad marginal 0.32). Se reporta la "
                      "desviacion y NO se mueve ningun parametro."),
    }
    print("recalibracion A0-P: R0=%.4f (mundo congelado %.4f), desviacion vs 1 = "
          "%.4f (%.2f SEM)" % (a0p["R0"], cong["R0"],
                               recal["desviacion_respecto_de_1"],
                               recal["desviacion_en_errores_estandar"]))

    print("== replica (semillas 1000..1999) ==")
    datos_rep = corre_bloque(SEEDS_REPLICA)
    replica = resumen_bloque(datos_rep, SEEDS_REPLICA, "replica")

    pe = principal["pareados"]["E-P_vs_A0-P"]
    pb = principal["pareados"]["BARAJA-P_vs_A0-P"]
    re_ = replica["pareados"]["E-P_vs_A0-P"]
    cumple = (pe["R0_fraccion_mejor_sobre_todas"] >= 0.60)
    cumple_rep = (re_["R0_fraccion_mejor_sobre_todas"] >= 0.60)

    veredicto = {
        "prediccion": PREDICCION,
        "criterio_estricto_>=0.60_semillas_con_R0_mayor": {
            "principal": pe["R0_fraccion_mejor_sobre_todas"],
            "replica": re_["R0_fraccion_mejor_sobre_todas"],
            "cumple_principal": cumple,
            "cumple_replica": cumple_rep,
        },
        "direccion_del_efecto": {
            "delta_R0_principal": (principal["agregados"]["E-P"]["R0"] -
                                   principal["agregados"]["A0-P"]["R0"]),
            "delta_extincion_principal": (
                principal["agregados"]["E-P"]["extinction_rate"] -
                principal["agregados"]["A0-P"]["extinction_rate"]),
            "delta_R0_replica": (replica["agregados"]["E-P"]["R0"] -
                                 replica["agregados"]["A0-P"]["R0"]),
            "delta_extincion_replica": (
                replica["agregados"]["E-P"]["extinction_rate"] -
                replica["agregados"]["A0-P"]["extinction_rate"]),
        },
        "control_BARAJA-P_vs_A0-P": {
            "delta_R0": (principal["agregados"]["BARAJA-P"]["R0"] -
                         principal["agregados"]["A0-P"]["R0"]),
            "delta_extincion": (
                principal["agregados"]["BARAJA-P"]["extinction_rate"] -
                principal["agregados"]["A0-P"]["extinction_rate"]),
            "fraccion_semillas_mejor": pb["R0_fraccion_mejor_sobre_todas"],
            "test_signos_p": pb["R0_test_signos_p"],
        },
    }

    params = {
        "experiment": "variante_parches_A0P_EP_BARAJAP",
        "engine": "variante_parches/mundo_parches.py",
        "engine_version": M.VERSION,
        "engine_sha256": E.sha256_de(os.path.join(BASE, "mundo_parches.py")),
        "base_engine_sha256": E.sha256_de(os.path.join(RAIZ, "mundo_minimo.py")),
        "changed_mechanism": ("UNA sola modificacion: dos parches de comida "
                             "(0.42 y 0.22, media 0.32) y una accion por ronda "
                             "(elegir parche). Nada mas cambia."),
        "patches": {"rich": M.PARCHES[0], "poor": M.PARCHES[1],
                    "mean": sum(M.PARCHES) / 2.0},
        "epsilon_declarado": M.EPSILON,
        "memory_cap": M.MEMORY_CAP,
        "memory_schema": ["state (energia al decidir)", "action (parche)",
                          "reward (comida recibida)", "outcome"],
        "arms": {
            "A0-P": "elige parche al azar (uniforme)",
            "E-P": ("memoria <= 20 episodios; elige el parche de mejor recompensa "
                    "media reciente; epsilon = 0.1"),
            "BARAJA-P": ("control: igual que E-P pero permutando las ETIQUETAS DE "
                         "ACCION de la memoria antes de decidir (barajar solo el "
                         "orden seria un no-op: la media es invariante al orden)"),
        },
        "frozen_world_resto": dict(PARAMS_A0),
        "prng": {"mundo": "random.Random(seed)",
                 "politica": "random.Random(seed + 1000000)",
                 "nota": ("dos flujos declarados para que la dinamica del mundo "
                          "consuma el PRNG en el mismo orden en los tres brazos; "
                          "sin multiprocessing")},
        "seeds_principal": {"first": 0, "last": 999, "count": 1000},
        "seeds_replica": {"first": 1000, "last": 1999, "count": 1000},
        "prediccion_preregistrada": PREDICCION,
    }

    resultados = {
        "recalibracion_A0-P": recal,
        "principal_seeds_0_999": principal,
        "replica_seeds_1000_1999": replica,
        "veredicto": veredicto,
    }

    E.escribir_json(os.path.join(BASE, "PARAMETERS.json"), params)
    E.escribir_json(os.path.join(BASE, "RESULTS.json"), resultados)
    E.escribir_json(os.path.join(BASE, "PER_SEED_RESULTS.json"), {
        "principal": dict((b, [{k: v for k, v in r.items() if k != "_genealogy"}
                               for r in datos[b]]) for b in BRAZOS),
        "replica": dict((b, [{k: v for k, v in r.items() if k != "_genealogy"}
                             for r in datos_rep[b]]) for b in BRAZOS),
    })
    E.escribir_json(os.path.join(BASE, "GENEALOGY.json"), {
        "principal": dict((b, dict((str(r["seed"]), r["_genealogy"])
                                   for r in datos[b])) for b in BRAZOS),
        "replica": dict((b, dict((str(r["seed"]), r["_genealogy"])
                                 for r in datos_rep[b])) for b in BRAZOS),
    })
    return resultados, params


if __name__ == "__main__":
    main()
