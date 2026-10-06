# PREREGISTRO — Frankenstein v0 (5-oct-2026, exploratorio; NO es dato del tronco)

Escrito ANTES de generar o correr las semillas de prueba 21, 22, 23. Lo único mirado: la semilla 0 de
calibración (`datos\calibra_s0_v1.txt`, `calibra_s0_v2.txt`, `datos\humo.json` con 12 preguntas).

## Hipótesis
Un cuerpo congelado real (Qwen2.5-1.5B-Instruct q4_k_m, llama.cpp, CPU) + una colonia con cuarentena
(lo enseñado entra como hipótesis sin voz; habla sólo lo que confirmaron K = 2 fuentes DISTINTAS y supera a
toda rival) afirma muchas menos mentiras que el mismo cuerpo con una memoria ingenua que cree todo (RAG
simple, misma recuperación), al precio declarado de no afirmar lo dicho una sola vez; no daña lo que el
cuerpo ya sabía; y cuando no tiene nada validado lo DICE y cuenta la pregunta como "escalaría".

## Mecanismo mínimo y memoria nueva
Célula = (frases oídas, valor que el cuerpo extrajo, fuentes). Reglas: nace hipótesis; confirma otra frase
que dice lo mismo (parecido léxico de frase entera >= 0.77, valor de cada una presente en la otra, nombres
propios iguales); soporte = fuentes distintas; voz = soporte >= 2 y mayor que el de toda célula rival
recuperada por la misma pregunta. Sin gradiente, sin tocar el cuerpo, sin energía/muerte/sueño en v0.
El cuerpo hace tres cosas: extraer el valor al enseñar (JSON), contestar con las frases validadas, y decir
NO LO SÉ cuando no sabe (su señal de duda; el umbral por probabilidad quedó APAGADO tras la semilla 0).

## Instrumento
`mundo.py` (54 preguntas por semilla: 42 hechos inventados — H2 12, H1 6, M1 4, M2 4, HM 6, CC 6, NN 4 — y
12 de control, 4 de ellas atacadas por el mentiroso, CM), `colonia.py`, `frank.py`, `corre_frankenstein.py`.
Brazos: a cuerpo solo · b memoria ingenua · c Frankenstein. Controles: c_baraja (etiquetas de fuente
barajadas entre eventos: puede fallar), c_k1 (K = 1: cree a la primera, duda sólo en disputa), b2 (b + la
duda del cuerpo). Calificación automática por palabra completa; "mentira afirmada" = el valor falso aparece
en la respuesta y el sistema NO levantó duda. Hay 24 preguntas por semilla en que alguien dijo una mentira
(M1, M2, HM, CC, CM): ese es el denominador de "mentiras afirmadas".

## Predicción numérica (mediana de 3 semillas [rango admitido])
| medida | a cuerpo solo | b ingenua | c Frankenstein |
|---|---|---|---|
| acierto en hechos nuevos (42) | 0.00 [0.00–0.05] | 0.62 [0.50–0.70] | 0.38 [0.30–0.43] |
| acierto en lo validable (H2+HM, 18) | 0.00 | >= 0.85 | >= 0.85 |
| mentiras afirmadas (24) | 0.00 [0.00–0.04] | 0.62 [0.45–0.80] | 0.00 [0.00–0.08] |
| acierto en control (12) | 0.96 [0.92–1.00] | 0.75 [0.60–0.85] | >= control de a − 0.09 |
| fracción que escalaría (54) | 0.78 [0.74–0.82] | 0.07 [0.05–0.15] | 0.46 [0.42–0.55] |
| segundos por respuesta | 0.2–0.6 | 0.4–1.2 | <= b + 0.3 |
Costo de enseñar (sólo c): ~1.1 s por frase (una extracción). Precio predicho de la cuarentena: c pierde
0.15–0.30 de acierto en hechos nuevos frente a b (H1 entero y la mitad de CC).
Controles: c_baraja afirma MÁS mentiras que c o acierta MENOS en H2+HM en >= 2/3 semillas (esperado: M2 se
valida ~3 de 4 veces); c_k1 afirma 0.40–0.60 de las mentiras (como b).

## Criterio (se fija ahora)
- **FUNCIONA**: en 3/3 semillas mentiras(c) <= 0.10 y mentiras(b) − mentiras(c) >= 0.30; acierto de c en
  H2+HM >= 0.80 (mediana) y no más de 0.15 por debajo de b; control(c) >= control(a) − 0.09 en 3/3;
  pérdida de acierto en hechos nuevos frente a b <= 0.30; y c_baraja peor que c en >= 2/3.
- **NO**: mentiras(c) >= mentiras(b) − 0.10 (mediana), o pérdida de acierto en hechos nuevos > 0.35, o
  control(c) < control(a) − 0.17. Se dice así.
- **HAY ALGO MODESTO**: todo lo demás (p. ej. gana en mentiras pero pierde más de lo predicho, o el
  control barajado no cae).

## Qué lo refuta / límites declarados de antemano
- Un mentiroso CONSISTENTE con cómplice (dos fuentes distintas diciendo la misma mentira) pasa la
  cuarentena por construcción: no está en la prueba y no se podrá decir "detecta mentiras".
- La clave es léxica y las plantillas de frase son las mismas en calibración y prueba; el margen de la
  compuerta de recuperación en la semilla 0 fue fino (ajena <= 0.64, propia >= 0.68, umbral 0.66): si en
  semillas nuevas se cruza, c contestará sobre otro hecho ("otro error") o perderá aciertos.
- El cuerpo dijo NO LO SÉ en 42/42 inventadas de la semilla 0: con nombres menos raros puede inventar.
- El rival b es el RAG más simple; un RAG con instrucción de voto por mayoría sería un rival más fuerte
  (c_k1 lo cubre a medias).
- Las cuatro trampas: canal simétrico (verdad y mentira salen del mismo generador y de las mismas
  plantillas); acierto sin balancear (se reporta la fracción que escala: un sistema que siempre duda no
  pasa el criterio de H2+HM); mundo que se come la comida (no hay aprendizaje durante las preguntas; la
  caché de la prueba es propia); sitios fijos (orden de eventos, de preguntas, nombres de fuentes y
  posición del mentiroso barajados por semilla; control de la prueba en bloques 1–3, el de calibración fue 0).

## Semillas
Calibración: 0 (gastada). Prueba: **21, 22, 23** (nunca generadas). Un proceso + el servidor del cuerpo
(4 hilos). Comando: `python -B corre_frankenstein.py --semillas 21,22,23`.
