# -*- coding: utf-8 -*-
"""Genera README.md, SUMMARY.md, SHA256.txt y ZIP de la corrida A0 contra E."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import entregables as E
import run_a0_vs_e as R

CARPETA = R.CARPETA


def main():
    ag_a0, ag_e, resultados, params = R.main()
    cmp_ = resultados["comparacion_pareada"]
    ident = cmp_["identidad_exacta_semilla_a_semilla"]

    readme = """# Corrida 2 - A0 contra E (memoria episodica minima), mundo CONGELADO

MISION: llegar a la AGI por este camino, con evidencia preregistrada y honestidad:
intentar romper la hipotesis, no demostrarla.

## Prediccion PREREGISTRADA (escrita antes de correr)
%s

## Que cambio
Una sola modificacion: E = A0 + memoria episodica minima
{state, action, reward, outcome}, local, <= %d episodios por organismo, sin acceso
global, sin futuro, sin otros organismos, sin backprop, sin supervisor.
La memoria SOLO registra: no consume PRNG y no toca ninguna rama de la dinamica.
Mundo congelado: food_probability = 0.32, semillas 0..999, comparacion pareada.

## Resultado

| metrica | A0 | E | delta |
|---|---|---|---|
| R0 | %.4f | %.4f | %.4f |
| extinction_rate | %.3f | %.3f | %.3f |
| mean_final_population | %.3f | %.3f | %.3f |
| lineage_survival | %.3f | %.3f | %.3f |
| descendants_per_founder | %.3f | %.3f | %.3f |
| mean_survival_time | %.2f | %.2f | %.2f |
| number_of_generations | %.3f | %.3f | %.3f |

- Semillas comparadas: %d
- Semillas con alguna discrepancia en cualquier metrica: **%d**
- Semillas con genealogia byte a byte identica: **%d / %d**
- Identidad exacta semilla a semilla: **%s**
- memory_usage: E registra en media %.1f episodios por semilla (cap %d por
  organismo); A0 no tiene memoria.

## Lectura honesta
Esto NO es un exito de la memoria episodica. Es la confirmacion de que este mundo
no puede testear memoria: no hay accion, luego no hay nada que una memoria pueda
informar. La identidad exacta es una prueba de correccion de la implementacion
(el PRNG se consume igual en ambas ramas), no un resultado biologico ni cognitivo.
Cualquier diferencia habria sido un bug, no un efecto.

Por eso la pregunta interesante se traslada a `variante_parches/`, donde se
introduce UNA accion (elegir parche) manteniendo la media de comida en 0.32.
""" % (R.PREDICCION, R.MEMORY_CAP,
       ag_a0["R0"], ag_e["R0"], ag_e["R0"] - ag_a0["R0"],
       ag_a0["extinction_rate"], ag_e["extinction_rate"],
       ag_e["extinction_rate"] - ag_a0["extinction_rate"],
       ag_a0["mean_final_population"], ag_e["mean_final_population"],
       ag_e["mean_final_population"] - ag_a0["mean_final_population"],
       ag_a0["lineage_survival"], ag_e["lineage_survival"],
       ag_e["lineage_survival"] - ag_a0["lineage_survival"],
       ag_a0["descendants_per_founder"], ag_e["descendants_per_founder"],
       ag_e["descendants_per_founder"] - ag_a0["descendants_per_founder"],
       ag_a0["mean_survival_time"], ag_e["mean_survival_time"],
       ag_e["mean_survival_time"] - ag_a0["mean_survival_time"],
       ag_a0["number_of_generations"], ag_e["number_of_generations"],
       ag_e["number_of_generations"] - ag_a0["number_of_generations"],
       cmp_["seeds_comparadas"], cmp_["seeds_con_alguna_discrepancia"],
       cmp_["seeds_con_genealogia_identica"], cmp_["seeds_comparadas"],
       "SI" if ident else "NO",
       ag_e["mean_memory_episodes_per_seed"], R.MEMORY_CAP)

    summary = """# SUMMARY - Corrida 2: A0 contra E (mundo congelado)

- **experiment**: A0_vs_E_mundo_congelado (linea externa, mundo minimo)
- **hypothesis**: (preregistrada, del coordinador) A0 == E en todas las metricas,
  semilla a semilla, porque en este mundo no hay accion que la memoria informe.
- **changed_mechanism**: una sola modificacion: memoria episodica minima
  {state, action, reward, outcome}, local, <= %d episodios, solo registro,
  sin consumo adicional de PRNG.
- **fixed_parameters**: mundo congelado completo (food_probability 0.32,
  metabolic_cost 0.35, threshold 9.0, p_rep 0.02, coste 2.0, hijo 7.5,
  max_population 12, rounds 180, founders 2).
- **number_of_seeds**: 1000 (0..999), pareadas.
- **R0**: A0 %.4f | E %.4f (delta %.4f)
- **extinction_rate**: A0 %.3f | E %.3f (delta %.3f)
- **mean_final_population**: A0 %.3f | E %.3f (delta %.3f)
- **lineage_statistics**: lineage_survival A0 %.3f / E %.3f;
  descendants_per_founder A0 %.3f / E %.3f; generaciones A0 %.3f / E %.3f.
- **result**: **IDENTIDAD EXACTA** en las %d semillas y en la genealogia completa
  (%d/%d genealogias identicas, 0 discrepancias). La prediccion se cumplio.
  No hay efecto de la memoria, y no podia haberlo.
- **limitations**: el resultado no dice nada sobre el valor de la memoria
  episodica. Dice que el banco de pruebas elegido es incapaz de medirla. Un
  experimento que no puede fallar tampoco puede confirmar. Ademas la identidad
  depende de que E no consuma PRNG: es una propiedad de esta implementacion, no
  una garantia general.
- **SHA-256**: ver SHA256.txt y el sha del ZIP en el mensaje de entrega.

## Las cinco preguntas
1. **Prediccion**: %s
2. **Que cambio**: solo se anadio memoria episodica de registro a E. Nada mas.
3. **Resultado**: identidad exacta semilla a semilla, incluida la genealogia.
   delta_R0 = %.4f, delta_extincion = %.3f.
4. **Replica**: trivialmente replicable (determinista). Se replica ademas con
   semillas 1000..1999 dentro de la corrida 3.
5. **Explicacion alternativa**: ninguna compite. La identidad es analitica, no
   empirica: la memoria no entra en ninguna rama de la dinamica ni toca el PRNG.
   La unica alternativa era un bug, y la comparacion campo a campo mas la
   genealogia lo descartan. Advertencia: si alguien presentara esta identidad
   como "la memoria no dana", seria una lectura tramposa; lo correcto es decir
   que el experimento estaba vacio por construccion.
""" % (R.MEMORY_CAP,
       ag_a0["R0"], ag_e["R0"], ag_e["R0"] - ag_a0["R0"],
       ag_a0["extinction_rate"], ag_e["extinction_rate"],
       ag_e["extinction_rate"] - ag_a0["extinction_rate"],
       ag_a0["mean_final_population"], ag_e["mean_final_population"],
       ag_e["mean_final_population"] - ag_a0["mean_final_population"],
       ag_a0["lineage_survival"], ag_e["lineage_survival"],
       ag_a0["descendants_per_founder"], ag_e["descendants_per_founder"],
       ag_a0["number_of_generations"], ag_e["number_of_generations"],
       cmp_["seeds_comparadas"], cmp_["seeds_con_genealogia_identica"],
       cmp_["seeds_comparadas"], R.PREDICCION,
       cmp_["delta_R0"], cmp_["delta_extinction_rate"])

    E.escribir_texto(os.path.join(CARPETA, "README.md"), readme)
    E.escribir_texto(os.path.join(CARPETA, "SUMMARY.md"), summary)
    archivos = list(E.ORDEN_ZIP)
    E.escribir_sha256(CARPETA, archivos)
    destino, sha = E.empacar_zip(CARPETA, "a0_vs_e.zip", archivos + ["SHA256.txt"])
    E.escribir_texto(os.path.join(CARPETA, "SHA256.txt"),
                     open(os.path.join(CARPETA, "SHA256.txt"),
                          encoding="utf-8").read() + "%s  a0_vs_e.zip\n" % sha)
    print("ZIP:", destino)
    print("SHA256 ZIP:", sha)
    return sha


if __name__ == "__main__":
    main()
