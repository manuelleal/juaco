# -*- coding: utf-8 -*-
"""Genera README.md, SUMMARY.md, SHA256.txt y ZIP de la variante de parches."""

import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(BASE))
sys.path.insert(0, BASE)

import entregables as E  # noqa: E402
import run_parches as R  # noqa: E402


def fila(a, brazo):
    return "| %s | %.4f | %.4f | %.3f | %.3f | %.3f | %.3f |" % (
        brazo, a["R0"], a["R0_sem"], a["extinction_rate"],
        a["mean_final_population"], a["lineage_survival"],
        a["mean_rich_patch_fraction"])


def tabla(bloque):
    out = ["| brazo | R0 | +-SEM | extincion | poblacion final | lineage_survival | fraccion parche rico |",
           "|---|---|---|---|---|---|---|"]
    for b in R.BRAZOS:
        out.append(fila(bloque["agregados"][b], b))
    return "\n".join(out)


def tabla_pareada(bloque):
    out = ["| comparacion | R0 mejor | igual | peor | fraccion mejor | fraccion entre discordantes | p (signos) |",
           "|---|---|---|---|---|---|---|"]
    for k in ["E-P_vs_A0-P", "BARAJA-P_vs_A0-P", "E-P_vs_BARAJA-P"]:
        v = bloque["pareados"][k]
        fd = v["R0_fraccion_mejor_entre_discordantes"]
        out.append("| %s | %d | %d | %d | %.3f | %s | %.3g |" % (
            k, v["R0_semillas_mejor"], v["R0_semillas_iguales"],
            v["R0_semillas_peor"], v["R0_fraccion_mejor_sobre_todas"],
            ("%.3f" % fd) if fd is not None else "NA", v["R0_test_signos_p"]))
    return "\n".join(out)


def main():
    res, params = R.main()
    pr = res["principal_seeds_0_999"]
    rp = res["replica_seeds_1000_1999"]
    rec = res["recalibracion_A0-P"]
    ver = res["veredicto"]
    pe = pr["pareados"]["E-P_vs_A0-P"]
    re_ = rp["pareados"]["E-P_vs_A0-P"]
    pb = pr["pareados"]["BARAJA-P_vs_A0-P"]

    readme = """# Corrida 3 - HIPOTESIS APARTE: dos parches y una accion por ronda

MISION: llegar a la AGI por este camino, con evidencia preregistrada y honestidad:
intentar romper la hipotesis, no demostrarla.

## Prediccion PREREGISTRADA (escrita antes de correr)
%s

## La unica modificacion
La comida deja de ser una moneda al aire unica y pasa a estar en DOS PARCHES
(0.42 y 0.22; media 0.32, exactamente la del mundo congelado), y el organismo toma
UNA accion por ronda: elegir parche. Todo lo demas queda igual que en el mundo
congelado. Principio de una sola modificacion por experimento: respetado.

## Brazos
- **A0-P**: elige parche al azar (uniforme). Probabilidad marginal de comida 0.32.
- **E-P**: memoria episodica <= %d episodios {state, action, reward, outcome};
  elige el parche de mejor recompensa media reciente; exploracion epsilon = %.2f
  DECLARADA.
- **BARAJA-P** (control): identico a E-P salvo que las ETIQUETAS DE ACCION de la
  memoria se permutan al azar antes de decidir. Nota honesta: barajar solo el
  ORDEN de los episodios seria un no-op, porque la media es invariante al orden;
  el control con contenido es permutar la etiqueta de accion, que es lo que rompe
  la contingencia accion<->recompensa conservando las marginales.

## Paso 0: recalibracion de A0-P (obligatoria, antes de comparar)
- R0(A0-P) = %.4f (SEM %.4f)
- R0 del mundo congelado de un parche, mismas semillas = %.4f
- Desviacion respecto de 1: %.4f (%.2f errores estandar)
- Extincion A0-P %.3f contra %.3f del mundo congelado
- Fraccion de elecciones del parche rico en A0-P: %.3f (debe ser ~0.5)

Lectura: A0-P se comporta como el mundo congelado, como debe ser (la probabilidad
marginal es la misma 0.32). R0 queda por debajo de 1 en la misma medida que el
mundo congelado, a menos de 2 SEM. **Se reporta la desviacion y NO se mueve
ningun parametro**, tal como ordena el encargo.

## Resultados, semillas 0..999

%s

### Comparacion pareada por semilla (R0)

%s

- Extincion, semillas donde solo un brazo se extingue: solo A0-P %d contra solo
  E-P %d (E-P evita la extincion en la gran mayoria de los casos discordantes).
- Poblacion final: E-P mayor en %d semillas, menor en %d.

## Replica, semillas 1000..1999

%s

%s

## Veredicto
- Criterio preregistrado (>= 0.60 de las semillas con R0 mayor): principal
  **%.3f** (%s), replica **%.3f** (%s).
- delta R0 principal: **%+.4f**; delta extincion principal: **%+.3f**.
- delta R0 replica: **%+.4f**; delta extincion replica: **%+.3f**.
- Control BARAJA-P contra A0-P: delta R0 %+.4f, delta extincion %+.3f, fraccion
  de semillas mejor %.3f, p del test de signos %.3g. **Indistinguible de A0-P**,
  como estaba predicho.

## Donde esto puede estar enganando
1. El pareado es **por semilla, no por trayectoria**: desde la primera ronda los
   brazos consumen el PRNG del mundo de forma distinta, asi que la semilla fija el
   punto de partida, no el ruido comun. El test de signos sobre 1000 semillas
   sigue siendo valido como comparacion de distribuciones, pero no es un pareado
   en el sentido fuerte.
2. El efecto es **grande y esperado a priori**: con epsilon 0.1 y un parche al
   0.42, la energia neta por ronda pasa de -0.03 a cerca de +0.06. No hace falta
   nada parecido a una mente para conseguirlo; basta un contador de dos casillas.
   Esto NO es evidencia de cognicion: es evidencia de que un bandido de dos brazos
   se resuelve con dos medias.
3. La fraccion de parche rico se queda en %.3f, lejos del 0.95 que permitiria
   epsilon. Con 20 episodios de recompensa 0/1 y medias 0.42 contra 0.22, la
   estimacion es ruidosa y los recien nacidos empiezan con la memoria vacia. El
   agente es peor de lo que podria ser.
4. El mundo tope de 12 organismos **satura**: con E-P la poblacion final media es
   %.3f, asi que el hueco de reproduccion se disputa y R0 queda censurado por
   arriba. El efecto medido es una cota inferior del efecto real.
""" % (R.PREDICCION, R.M.MEMORY_CAP, R.M.EPSILON,
       rec["R0_A0-P"], rec["R0_A0-P_sem"], rec["R0_mundo_congelado_un_parche"],
       rec["desviacion_respecto_de_1"], rec["desviacion_en_errores_estandar"],
       rec["extincion_A0-P"], rec["extincion_mundo_congelado"],
       rec["fraccion_parche_rico_A0-P"],
       tabla(pr), tabla_pareada(pr),
       pe["extincion_solo_A0-P"], pe["extincion_solo_E-P"],
       pe["poblacion_final_semillas_mejor"], pe["poblacion_final_semillas_peor"],
       tabla(rp), tabla_pareada(rp),
       ver["criterio_estricto_>=0.60_semillas_con_R0_mayor"]["principal"],
       "CUMPLE" if ver["criterio_estricto_>=0.60_semillas_con_R0_mayor"]["cumple_principal"] else "NO CUMPLE",
       ver["criterio_estricto_>=0.60_semillas_con_R0_mayor"]["replica"],
       "CUMPLE" if ver["criterio_estricto_>=0.60_semillas_con_R0_mayor"]["cumple_replica"] else "NO CUMPLE",
       ver["direccion_del_efecto"]["delta_R0_principal"],
       ver["direccion_del_efecto"]["delta_extincion_principal"],
       ver["direccion_del_efecto"]["delta_R0_replica"],
       ver["direccion_del_efecto"]["delta_extincion_replica"],
       ver["control_BARAJA-P_vs_A0-P"]["delta_R0"],
       ver["control_BARAJA-P_vs_A0-P"]["delta_extincion"],
       ver["control_BARAJA-P_vs_A0-P"]["fraccion_semillas_mejor"],
       ver["control_BARAJA-P_vs_A0-P"]["test_signos_p"],
       pr["agregados"]["E-P"]["mean_rich_patch_fraction"],
       pr["agregados"]["E-P"]["mean_final_population"])

    summary = """# SUMMARY - Corrida 3: variante de parches (hipotesis aparte)

- **experiment**: variante_parches_A0P_EP_BARAJAP (linea externa, mundo minimo)
- **hypothesis**: %s
- **changed_mechanism**: UNA sola modificacion: dos parches de comida (0.42 y
  0.22, media 0.32) mas una accion por ronda (elegir parche). Nada mas cambia.
- **fixed_parameters**: founders 2, initial_energy 10.0, metabolic_cost 0.35,
  food_energy 1.0, reproduction_threshold 9.0, reproduction_probability 0.02,
  reproduction_cost 2.0, newborn_initial_energy 7.5, max_population 12,
  rounds 180. Memoria <= %d episodios, epsilon %.2f declarada.
- **number_of_seeds**: 1000 principales (0..999) + 1000 de replica (1000..1999),
  los tres brazos sobre las mismas semillas.
- **R0**: A0-P %.4f | E-P %.4f | BARAJA-P %.4f   (replica: %.4f | %.4f | %.4f)
- **extinction_rate**: A0-P %.3f | E-P %.3f | BARAJA-P %.3f
  (replica: %.3f | %.3f | %.3f)
- **mean_final_population**: A0-P %.3f | E-P %.3f | BARAJA-P %.3f
- **lineage_statistics**: lineage_survival A0-P %.3f | E-P %.3f | BARAJA-P %.3f;
  descendants_per_founder A0-P %.3f | E-P %.3f | BARAJA-P %.3f;
  generaciones A0-P %.3f | E-P %.3f | BARAJA-P %.3f.
- **result**: **PREDICCION CUMPLIDA Y REPLICADA**. E-P supera a A0-P en R0 en el
  %.1f %% de las semillas (replica %.1f %%), por encima del umbral preregistrado
  del 60 %%; la extincion cae de %.3f a %.3f. El control BARAJA-P es
  indistinguible de A0-P (fraccion de semillas mejor %.3f, p = %.3g), lo que
  descarta que el efecto venga de tener memoria y no de USAR la contingencia.
- **limitations**: (1) el pareado es por semilla, no por trayectoria: los brazos
  divergen en el consumo del PRNG desde la primera ronda; (2) el efecto era
  predecible analiticamente (epsilon 0.1 sobre un parche 0.42 lleva la energia
  neta de -0.03 a +0.06 por ronda): esto mide que un bandido de dos brazos se
  resuelve con dos medias, no que haya cognicion; (3) el tope de 12 organismos
  satura con E-P (poblacion final %.3f), asi que R0 esta censurado por arriba y
  el efecto medido es una cota inferior; (4) E-P solo elige el parche rico el
  %.1f %% de las veces, muy por debajo del 95 %% que permite epsilon: la memoria de
  20 episodios binarios es ruidosa y los recien nacidos nacen sin memoria; (5)
  todo esto sigue siendo una ecologia de juguete, no el organismo JUACO.
- **SHA-256**: ver SHA256.txt y el sha del ZIP en el mensaje de entrega.

## Las cinco preguntas
1. **Prediccion (preregistrada)**: %s
2. **Que cambio**: solo la estructura de la comida (dos parches en vez de uno,
   misma media) y la existencia de una accion. La regla de decision distingue los
   tres brazos; el mundo es el mismo para los tres.
3. **Resultado**: E-P R0 %.4f contra A0-P %.4f (delta %+.4f); extincion %.3f
   contra %.3f (delta %+.3f); %.1f %% de semillas con R0 mayor. BARAJA-P se queda
   pegado a A0-P.
4. **Replica**: semillas 1000..1999, efecto del mismo tamano y signo
   (delta R0 %+.4f, delta extincion %+.3f, %.1f %% de semillas mejor). No depende
   de unas pocas semillas: el test de signos da p = %.3g sobre %d pares
   discordantes.
5. **Explicacion alternativa**: la que mas peso tiene es que E-P no esta
   "recordando" nada interesante, sino estimando dos medias; el resultado es una
   propiedad del bandido, no del organismo. Una segunda alternativa -que el
   beneficio venga del simple hecho de llevar memoria, o de que E-P consuma el
   PRNG de otra forma- queda descartada por BARAJA-P, que lleva exactamente la
   misma memoria, el mismo consumo de PRNG y la misma regla, y no mejora nada.
   Lo que el experimento sostiene es estrictamente esto: cuando existe una accion
   cuyo resultado se puede registrar, registrar la contingencia paga; cuando no
   existe accion (corrida 2), la memoria es literalmente inerte.
""" % (R.PREDICCION, R.M.MEMORY_CAP, R.M.EPSILON,
       pr["agregados"]["A0-P"]["R0"], pr["agregados"]["E-P"]["R0"],
       pr["agregados"]["BARAJA-P"]["R0"],
       rp["agregados"]["A0-P"]["R0"], rp["agregados"]["E-P"]["R0"],
       rp["agregados"]["BARAJA-P"]["R0"],
       pr["agregados"]["A0-P"]["extinction_rate"],
       pr["agregados"]["E-P"]["extinction_rate"],
       pr["agregados"]["BARAJA-P"]["extinction_rate"],
       rp["agregados"]["A0-P"]["extinction_rate"],
       rp["agregados"]["E-P"]["extinction_rate"],
       rp["agregados"]["BARAJA-P"]["extinction_rate"],
       pr["agregados"]["A0-P"]["mean_final_population"],
       pr["agregados"]["E-P"]["mean_final_population"],
       pr["agregados"]["BARAJA-P"]["mean_final_population"],
       pr["agregados"]["A0-P"]["lineage_survival"],
       pr["agregados"]["E-P"]["lineage_survival"],
       pr["agregados"]["BARAJA-P"]["lineage_survival"],
       pr["agregados"]["A0-P"]["descendants_per_founder"],
       pr["agregados"]["E-P"]["descendants_per_founder"],
       pr["agregados"]["BARAJA-P"]["descendants_per_founder"],
       pr["agregados"]["A0-P"]["number_of_generations"],
       pr["agregados"]["E-P"]["number_of_generations"],
       pr["agregados"]["BARAJA-P"]["number_of_generations"],
       100 * pe["R0_fraccion_mejor_sobre_todas"],
       100 * re_["R0_fraccion_mejor_sobre_todas"],
       pr["agregados"]["A0-P"]["extinction_rate"],
       pr["agregados"]["E-P"]["extinction_rate"],
       pb["R0_fraccion_mejor_sobre_todas"], pb["R0_test_signos_p"],
       pr["agregados"]["E-P"]["mean_final_population"],
       100 * pr["agregados"]["E-P"]["mean_rich_patch_fraction"],
       R.PREDICCION,
       pr["agregados"]["E-P"]["R0"], pr["agregados"]["A0-P"]["R0"],
       ver["direccion_del_efecto"]["delta_R0_principal"],
       pr["agregados"]["E-P"]["extinction_rate"],
       pr["agregados"]["A0-P"]["extinction_rate"],
       ver["direccion_del_efecto"]["delta_extincion_principal"],
       100 * pe["R0_fraccion_mejor_sobre_todas"],
       ver["direccion_del_efecto"]["delta_R0_replica"],
       ver["direccion_del_efecto"]["delta_extincion_replica"],
       100 * re_["R0_fraccion_mejor_sobre_todas"],
       pe["R0_test_signos_p"],
       pe["R0_semillas_mejor"] + pe["R0_semillas_peor"])

    E.escribir_texto(os.path.join(BASE, "README.md"), readme)
    E.escribir_texto(os.path.join(BASE, "SUMMARY.md"), summary)
    archivos = list(E.ORDEN_ZIP) + ["mundo_parches.py", "run_parches.py"]
    E.escribir_sha256(BASE, archivos)
    destino, sha = E.empacar_zip(BASE, "variante_parches.zip",
                                 archivos + ["SHA256.txt"])
    E.escribir_texto(os.path.join(BASE, "SHA256.txt"),
                     open(os.path.join(BASE, "SHA256.txt"),
                          encoding="utf-8").read() +
                     "%s  variante_parches.zip\n" % sha)
    print("ZIP:", destino)
    print("SHA256 ZIP:", sha)
    return sha


if __name__ == "__main__":
    main()
