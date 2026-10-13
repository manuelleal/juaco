# NOTAS lote2 (auditor ciego)

Resultado: 8 copias con defecto (c05, c17, c19, c25, c32, c45, c46, c53), 2 limpias (c29, c39). 14 filas en HALLAZGOS_lote2.csv.

## Tiempo aproximado por copia
c05 ~8 min, c17 ~10, c19 ~12, c25 ~12, c29 ~10, c32 ~7, c39 ~9, c45 ~15 (el mas largo), c46 ~6, c53 ~7. Total ~95 min.

## Lo que fue util
- Los sha de logs y JSON coinciden con los archivos actuales en todas las copias, incluso las que tienen un defecto claro en el runner (c32, c45, c19). Por tanto el sha NO discrimina; hubo que leer cada runner linea a linea contra el preregistro.
- Lo que mas atrapo: (1) comparar kwargs/semilla de cada tarea contra el preregistro (c19, c32, c45), (2) comprobar que los controles de identidad comparan dos modulos distintos (c05) y todas las claves (c25), (3) recalcular desde el JSON las cifras citadas en VEREDICTO (c17, c45, c46), (4) umbrales preregistro vs runner (c17, c53).

## Lo que no pude verificar sin correr la serie / sin los modulos externos
- Modulos importados que no estan en la carpeta (organismo_v8/v9/v10/v11, mundo_largo, corre_mundo_largo, corre_vivo_rep2, mini_vivo, corre_criterio_v3.no_inferior, parte2_capacidad, mundo_temporal_k, bateria_*). En c29 y c39 un defecto ahi me seria invisible.
- c39: Q1/Q2 (examen_v10) y Q5 no tienen JSON en la carpeta.
- c19: el diagnostico sin_plast y la correlacion 0.87 vienen de un script de scratchpad no incluido.
- c25: "466 corridas" cuadra con 420+6+40; no verifique las trayectorias.
- c17: el diagnostico post-hoc (error 0.02/0.11/0.16 tras el agotamiento) lo recalcule solo en parte (a 60k: 0.021 antes y al agotar, 0.157 diez estimulos despues; el VEREDICTO dice 0.11, ambiguo en la definicion). No lo marque como hallazgo.
- Commits (b930c9e etc.) y tiempos de pared de los VEREDICTO no verificables.

## Dudas / con menor confianza
- c17 prereg G2 ">= 0" y "3 semillas": podrian ser erratas originales o sembradas; el VEREDICTO y el runner concuerdan entre si en ">= +5".
- c25 NUEVAS en el runner: podria ser original (los 4 campos podrian diferir por diseno); lo marque media.
- c45 P-7 (-74.5): baja, probable arrastre del preregistro.
- c05: la identidad tautologica la considero alta porque el docstring y el preregistro piden explicitamente contra mundo_largo.
- No encontre CLAVE.csv ni la abri.
