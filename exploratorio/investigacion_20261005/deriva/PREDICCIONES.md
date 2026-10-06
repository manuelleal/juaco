# PREDICCIONES antes del experimento principal (5-oct-2026, escritas antes de correr la serie de 10 semillas)

Misión: llegar a la AGI por este camino. Aquí: ¿la célula de JUACO sirve como método de aprendizaje en línea con deriva de concepto, contra rivales estándar, fuera de nuestros juguetes?

Contexto que cambia respecto al informe 3 (donde la célula empató con el diccionario y ganó al kNN): allí los "hechos" eran puntos aislados sin vecinos y sin ruido. Aquí hay vecinos continuos (SEA, hiperplano, RBF), ruido de etiquetas 10 % y los rivales son los del campo (SGD con detector, kNN con ventana, DWM, reentrenar).

Predicciones con probabilidad (se contrastan en INFORME_DERIVA.md):

1. **(p=0.75) Veredicto global: HAY ALGO MODESTO o NO.** La célula (A: pegada al base congelado) NO gana en acierto prequential global a kNN con ventana ni a SGD con reinicio por DDM en la mayoría de pruebas×regímenes (pierde o empata en ≥ 60 % de las celdas prueba×C).
2. **(p=0.6) Donde sí: deriva RECURRENTE con base congelado bueno.** En la ventana tras la vuelta del concepto A (drift 2), la célula A recupera más rápido que SGD+DDM y que kNN con ventana en ≥ 3 de 4 generadores (porque suelta las correcciones y el base ya sabe A). Gana en ≥ 7/10 semillas en esa ventana.
3. **(p=0.55) Memoria chica (C=20):** la célula A gana al kNN con ventana de 20 en acierto global en ≥ 3 de 4 generadores (el kNN con 20 ejemplos y ruido 10 % es malo; la célula sólo guarda donde el base falla).
4. **(p=0.7) Célula B (sola, sin base) pierde** contra kNN con ventana y contra SGD en casi todo (≥ 75 % de celdas): sin base no tiene a quién corregir y se vuelve un prototipo-vecino con olvido raro.
5. **(p=0.8) Controles caen:** pago barajado y sin compuerta quedan por debajo de la célula A en ≥ 8/10 semillas en todas las pruebas (si no, el mecanismo no está haciendo nada aquí).
6. **(p=0.6) El ruido de etiquetas 10 % le pega más a la célula que a kNN/SGD** porque "pisé donde el base acertaba → muero" se dispara por ruido; esperaré tener que suavizar ese castigo en el flujo de validación (lo declaro).
7. **(p=0.65) Costo:** célula A entre 1.2× y 3× las ops del base congelado; muy por debajo del techo de reentrenar (≥ 10×); memoria final menor que la del kNN (que siempre llena la ventana).
8. **(p=0.5) El rival que queda más cerca en recurrencia** es DWM (mantiene expertos viejos) o SGD+DDM; en lo global es kNN con ventana 200.
9. **(p=0.7) STAGGER** (categórico, conceptos muy distintos) es la prueba donde la célula A queda peor frente a SGD+DDM (la corrección es global, no local: el base congelado falla en todas partes y las células tienen que reconstruir todo el concepto).
10. **(p=0.6) Hiperplano gradual** es donde todos se parecen más (el acierto global se decide por la transición) y la célula no destaca.

Criterio de "gana": mediana mayor Y ≥ 7/10 semillas pareadas. "Empata": 4–6/10 o diferencia < 0.01. "Pierde": ≤ 3/10.
