# PREREGISTRO (EXPLORATORIO) — PASAJES SERIADOS en ECO con hijo ingenuo (Opus A, reunión 28-sep-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo. Principio del director: que la evolución construya el órgano, sólo con selección natural.
Escrito ANTES del humo y antes de ver números de pasajes (el arnés 13/13 sólo imprime identidades y dos fund_2a de T 10 000–20 000).
No es candidato a tronco. Sin puertas de bloque: la lectura es la tabla por pasaje y las predicciones de abajo.

- **Hipótesis:** si cada pasaje corto (T_p = 50 000) siembra el siguiente con los genomas de sus VIVOS (sin juez), la selección
  acumula entre pasajes: los fundadores repuestos por pasaje bajan pasaje a pasaje y pasan del −32 % de la corrida larga (fund_2a
  86 833 vs 128 584 de ING_F1 en [5e5, 1e6], serie 46101–46120), y antes de 1e6 acumulado.
- **Mecanismo mínimo, memoria nueva: cero.** Ninguna regla del cuerpo cambia. Lo único nuevo es la puerta `genoma` (los 90
  fundadores; el motor ya la tenía: `motor_eco.ECO_DEF['genoma']`) y la transferencia en el runner: 90 genomas al azar de
  `vivos_final[i][4:]` (sólo el genoma; sin reemplazo si hay ≥ 90 vivos), recortados a [lo, hi] (vienen redondeados a 6 decimales).
- **Instrumento:** `construye_pasajes.py` → `nucleo_pasajes.py` (56c067e976b6b626) por anclas A1–A5 desde
  `eco_sel_ing/nucleo_eco_sel_ing.py` (c2189f9d22b72386). `corre_pasajes.py` (runner). Arnés `identidad_pasajes.py`: 13/13
  (1 pasaje sin transferencia == ECO_SEL_ING bit a bit; G0 explícito == None; el genoma entra; la transferencia no usa fitness;
  el resorteo; determinismo; el JSON de genomas del último pasaje).
- **Brazos** (mismo seed por pasaje: 100·s + p; pareados): PAS_SEL (CEREBRO, transfiere vivos) · PAS_RES (control: cada pasaje
  arranca de G0 mutado una vez por fundador; sin herencia entre pasajes) · PAS_AZA (CEREBRO_AZAR: sin herencia dentro del pasaje;
  transfiere vivos) · PAS_SELM (15 + rep_umbral; transfiere vivos) · PAS_F1 (MUT0: referencia por pasaje).
- **Plan:** T_p 50 000, 8 pasajes (esquema de Fable); si el reloj da, la cadena sigue hasta 20 pasajes (= 1e6 acumulado, el
  presupuesto de la corrida larga). Semillas base NUEVAS 47801–47805 (grep 18:55 en py/md/txt/log de organelos, bundle y carrera);
  práctica 47806–47809 (arnés y humo). ≤ 4 procesos, sin Pool.

## Predicciones firmadas (razón r = fund_2a / fund_2a(PAS_F1) − 1, pareada por semilla y pasaje; mediana de 5 semillas)

| # | cantidad | rango | p |
|---|---|---|---|
| Q1 | fund_2a de PAS_F1 por pasaje (en [25 000, 50 000]) | [6 000, 6 900] | 0.8 |
| Q2 | r de PAS_SEL en p1 (== PAS_RES p1) | [−0.30, −0.10] | 0.7 |
| Q3 | r de PAS_SEL en p8 | [−0.45, −0.28] | 0.6 |
| Q4 | PAS_SEL p8 < PAS_RES p8 en fund_2a en ≥ 4/5 semillas | — | 0.8 |
| Q5 | r de PAS_RES plano: |r(p8) − r(p2)| ≤ 0.05 | — | 0.7 |
| Q6 | r de PAS_AZA en p8 | [−0.10, +0.05] | 0.7 |
| Q7 | **más allá de la corrida larga:** r de PAS_SEL ≤ −0.325 en p8 (400 000 acumulado) en ≥ 4/5 semillas | — | 0.45 |
| Q8 | si llega a p20: r de PAS_SEL en p20 < −0.325 (mediana) | — | 0.55 |
| Q9 | alpha media de los vivos en PAS_SEL p8 | [2.0, 5.0] (G0 1.2) | 0.7 |
| Q10 | PAS_SELM p8 fund_2a < PAS_SEL p8 (mediana) | — | 0.5 |

**Qué lo refuta:** Q4 cae (los pasajes con herencia no bajan los fundadores más que un pasaje suelto desde G0) → la transferencia no
acumula nada que un solo pasaje no dé. Q7 y Q8 caen → los pasajes no superan a la corrida larga (satura).
**Control que puede fallar:** PAS_RES (y PAS_AZA para la herencia dentro del pasaje).
**Trampas:** (1) canal simétrico: SEL y RES sólo difieren en el genoma de entrada (misma semilla, mismos mutables); RES recibe una
mutación extra en la entrada (declarado; es el pedido de Fable). (2) no hay acierto que balancear: conteos pareados. (3) subsidio: el
vivero inyecta dote en cada refundación; por eso se mira fund_2a (menos fundadores = menos subsidio) y K_nac. (4) sitios: quimiostato
al azar; los fundadores del pasaje entran en las celdas del rng del mundo de cada semilla (las mismas en todos los brazos).
**Declarado:** la transferencia de vivos pesa a los que están vivos en T_p (incluye fundadores repuestos recién sacados del banco):
es selección natural leída, no juez. Las sombras se reinician en cada pasaje (tile del genoma de entrada): sel_100k no se lee aquí.
