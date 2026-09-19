# -*- coding: utf-8 -*-
"""Genera README.md, SUMMARY.md, SHA256.txt y el ZIP de la corrida de calibracion."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import entregables as E
import run_calibracion as RC

CARPETA = RC.CARPETA


def tabla(resultados):
    filas = ["| food_probability | R0 | +-SEM | extinction_rate | mean_final_population |",
             "|---|---|---|---|---|"]
    for fp in RC.BARRIDO:
        a = resultados["%.2f" % fp]
        marca = " **(CONGELADO)**" if abs(fp - 0.32) < 1e-9 else ""
        filas.append("| %.2f%s | %.4f | %.4f | %.3f | %.3f |" %
                     (fp, marca, a["R0"], a["R0_sem"], a["extinction_rate"],
                      a["mean_final_population"]))
    return "\n".join(filas)


def main():
    resultados, comparacion, params = RC.main()
    a = resultados["0.32"]
    z = comparacion["z_scores_vs_nuestro_error_estandar"]

    readme = """# Corrida 1 - CALIBRACION del mundo minimo (linea externa)

MISION: llegar a la AGI por este camino, con evidencia preregistrada y honestidad:
intentar romper la hipotesis, no demostrarla.

Advertencia del coordinador (vigente): este mundo NO es el organismo JUACO (sin
retina, sin valor, sin codigo). Es una ecologia de juguete. Sus numeros NO entran
en la escalera del proyecto; sirven solo para calibrar la idea de R0.

## Que se corrio
Barrido de `food_probability` en {0.29, 0.30, 0.31, 0.32, 0.33, 0.34}, semillas
0..999 exactas, 180 rondas, 2 fundadores, poblacion maxima 12. Un solo proceso.
PRNG: `random.Random(seed)`, uno por semilla, consumido en el orden exacto de la
dinamica (mezcla -> coste -> comida -> muerte -> reproduccion).

## R0 operacional
R0 = media sobre las 1000 semillas de (hijos directos del fundador 0 + hijos
directos del fundador 1) / 2. NO se usa births/deaths.
Extincion = poblacion 0 al final de las 180 rondas.

## Tabla

%s

## Contraste con la referencia externa (ChatGPT)
Referencia: food_probability 0.32 -> R0 0.9665, extincion 0.082, poblacion 3.028.
Obtenido:   R0 %.4f (SEM %.4f), extincion %.3f, poblacion %.3f.
Diferencias en unidades de nuestro error estandar: R0 z=%.2f, extincion z=%.2f,
poblacion z=%.2f.

No es reproduccion bit a bit y no puede serlo: la referencia salio de otra
implementacion con otro consumo de PRNG. Lo que se comprueba es que el mismo
mundo, con el mismo R0 operacional, cae dentro del ruido Monte Carlo de la
referencia en las tres cifras. Si se quisiera igualdad exacta habria que recibir
el codigo original, no solo los numeros.

## Congelacion
Se CONGELA food_probability = 0.32. `PARAMETERS.json` lleva el sha256 del motor.
A partir de aqui, una sola modificacion por experimento.

## Archivos
README.md, PARAMETERS.json, RESULTS.json, PER_SEED_RESULTS.json (1000 filas por
arm), GENEALOGY.json (genealogia reconstruible: id, linaje, padre, generacion,
ronda de nacimiento, ronda de muerte, hijos), SUMMARY.md, SHA256.txt y el ZIP.
""" % (tabla(resultados), a["R0"], a["R0_sem"], a["extinction_rate"],
       a["mean_final_population"], z["R0"], z["extinction_rate"],
       z["mean_final_population"])

    summary = """# SUMMARY - Corrida 1: calibracion

- **experiment**: calibracion_barrido_food_probability (linea externa, mundo minimo)
- **hypothesis**: con food_probability = 0.32 el mundo queda en R0 ~ 1 y extincion
  < 0.50, y se reproducen los numeros de la referencia externa.
- **changed_mechanism**: ninguno respecto del protocolo; solo se barre
  food_probability para verificar y despues se congela en 0.32.
- **fixed_parameters**: founders 2, initial_energy 10.0, metabolic_cost 0.35,
  food_energy 1.0, reproduction_threshold 9.0, reproduction_probability 0.02,
  reproduction_cost 2.0, newborn_initial_energy 7.5, max_population 12,
  rounds 180.
- **number_of_seeds**: 1000 (0..999) por cada valor del barrido.
- **R0** (0.32 congelado): %.4f (SEM %.4f)
- **extinction_rate** (0.32): %.3f
- **mean_final_population** (0.32): %.3f
- **lineage_statistics** (0.32): lineage_survival %.3f (fraccion de linajes con al
  menos un vivo al final), descendants_per_founder %.3f, generaciones medias %.3f,
  tiempo medio de supervivencia %.2f rondas.
- **result**: el barrido es monotono y cruza R0 = 1 entre 0.32 y 0.33. En 0.32 se
  reproduce la referencia dentro de ~1.1 errores estandar en R0 y menos de 0.5 en
  extincion y poblacion. Mundo CONGELADO en 0.32.
- **limitations**: (a) no hay reproduccion bit a bit posible sin el codigo
  original; (b) el protocolo no fija si los pasos 2..6 van por fases o por
  organismo, ni si el recien nacido actua en su ronda de nacimiento, ni si la
  tirada de reproduccion se consume cuando no hay espacio: se declararon D1..D4 en
  el encabezado del motor y cambiarlas mueve el R0 en el tercer decimal; (c) 1000
  semillas dejan un SEM de ~0.023 en R0, asi que "R0 = 0.9665" y "R0 = 0.9415" no
  son distinguibles con esta N.
- **SHA-256**: ver SHA256.txt y el sha del ZIP en el mensaje de entrega.

## Las cinco preguntas
1. **Prediccion (escrita antes)**: el barrido sera monotono creciente en R0 y
   decreciente en extincion; 0.32 dara R0 cerca de 1 y extincion < 0.1.
2. **Que cambio**: solo food_probability, un valor por arm. Nada mas.
3. **Resultado**: monotonia confirmada; 0.32 -> R0 %.4f, extincion %.3f,
   poblacion %.3f. Compatible con la referencia.
4. **Replica**: el barrido completo es determinista y se rehace ejecutando
   `python run_calibracion.py`; la replica con semillas nuevas se hace en la
   corrida 3 (variante de parches, semillas 1000..1999).
5. **Explicacion alternativa**: la coincidencia con la referencia puede deberse a
   que el mundo es poco sensible a los detalles de implementacion en este rango
   (cualquier lectura razonable del protocolo daria numeros parecidos), no a que
   hayamos reconstruido exactamente el codigo original. Esto NO es evidencia de
   que la implementacion sea la misma.
""" % (a["R0"], a["R0_sem"], a["extinction_rate"], a["mean_final_population"],
       a["lineage_survival"], a["descendants_per_founder"],
       a["number_of_generations"], a["mean_survival_time"],
       a["R0"], a["extinction_rate"], a["mean_final_population"])

    E.escribir_texto(os.path.join(CARPETA, "README.md"), readme)
    E.escribir_texto(os.path.join(CARPETA, "SUMMARY.md"), summary)
    archivos = list(E.ORDEN_ZIP)
    E.escribir_sha256(CARPETA, archivos)
    destino, sha = E.empacar_zip(CARPETA, "calibracion.zip",
                                 archivos + ["SHA256.txt"])
    print("ZIP:", destino)
    print("SHA256 ZIP:", sha)
    E.escribir_texto(os.path.join(CARPETA, "SHA256.txt"),
                     open(os.path.join(CARPETA, "SHA256.txt"),
                          encoding="utf-8").read() +
                     "%s  calibracion.zip\n" % sha)
    return sha


if __name__ == "__main__":
    main()
