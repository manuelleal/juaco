# INFORME — camino A: ¿aprende un organismo a limpiar? (creador, 22-sep-2026)

**Veredicto de los humos: NO, con ALGO MODESTO por confirmar.** El organismo que aprende no descubre la limpieza. Lo que sí aprende es a
**contenerse**. La serie 8101–8120 no se corrió (necesita Pool): la decide el coordinador con `PREREGISTRO_aprende.md`.

## Qué hice
- **El dato que cambia la pregunta.** Leí la serie sellada sin correr nada. FABRICA ya muerde lo malo 2.6 veces más que O1 y su mundo casi nunca
  queda sin nada bueno (0.4 % de los pasos). Muere de veneno y sal. Le sobra costo privado, no le falta bien público.
- **Los carros.** `APR` / `APR_SIN_HERENCIA` / `APR_AZAR`, construidos por anclas desde FABRICA (`construye_apr.py`).
  - Sobre lo malo conocido, la boca de FABRICA recibe una corrección aprendida: `logit p = logit(pb_FABRICA) + 10·(Q1 − Q0)`.
  - Q es lineal en lo que el cuerpo siente y se aprende por TD con +1 al parir y −1 al morir. Ningún umbral dice cuándo limpiar.
  - Q pasa al cuerpo siguiente del linaje por la misma vía que el nodo de FABRICA.
- **Arnés `identidad_apr.py`: 21/21.**
  - Con OPCION 0, los tres son FABRICA bit a bit: en la pista con N = 1 y N = 9, y contra el monolito `organismo_f9c`.
  - Con Q congelado, APR muerde **exactamente** como FABRICA.
  - La opción solo actúa sobre B/D, no lee la tabla ni el rng del mundo, `revisa_carro` pasa los tres y SIN_HERENCIA nace con Q = 0.
  - El primer intento dio 19/20 porque mi propio comentario nombraba `VAL_VIVO`. Lo reescribí.
- **Entrada campo a campo** (regla 14): `corre_aprende.tarea == juez.tarea` OK. El humo escribe su JSON.

## Qué falló (predicciones mías refutadas en práctica, 8001–8002, T = 30000)
- Antes del humo firmé en el código una predicción de 0.30–0.60 para APR v1. **Quedó refutada: 0.113** contra 0.279 de FABRICA.
  La recompensa v1 (solo Δu) no tenía objetivo real y aprendió al revés: mordía más cuanto más cerca estaba de morir.
- **v2** (recompensa real, pero la opción **reemplazaba** la boca): R0 **0.005** contra 0.329. Rompía la ventana de parto.
- **v3** (la opción **corrige** la boca): **0.377** contra 0.329 de FABRICA en la misma semilla 8002.
  - Corrección aprendida negativa en todas partes: de −1.2 a −2.2 logit.
  - Añadidas del 1.º al 4.º cuarto: 0.0019 → 0.0002 por oportunidad. Quitadas: ≈ 0.055.
  - Sin nada bueno en el mundo, la corrección no cambia.

| | identidad | cómo decide morder lo malo conocido | qué se hereda | humo (8002, T 30000): tasa / añadidas 4.º cuarto / R0 |
|---|---|---|---|---|
| FABRICA | ancla | hambre → boca (fila de la necesidad activa) | nodo (últimas 20 mordidas) | 0.16 si fuera APR* / — / **0.329** |
| APR v3 | 21/21 | boca de FABRICA + corrección aprendida por TD | nodo + Q (2×6) + dS por letra | 0.105 → 0.093 / **0.0002** / **0.377** |
| APR_SIN_HERENCIA (v1) | 21/21 | igual, Q = 0 en cada cuerpo | nodo + dS por letra | 0.25 / — / 0.043 (v1, s8001) |
| O1 (sellada) | — | regla escrita | tabla por letra | — / — / 1.565 |

\*Fracción de las oportunidades de APR que FABRICA habría mordido.

## Qué queda
- **La serie con Pool** (comandos en el §8 del preregistro), con 11 predicciones firmadas.
  - Predigo que **no cruza** (p 0.97) y que **no descubre** la limpieza (p 0.93).
  - Predigo que aprende a contenerse (p 0.85) y que le gana a FABRICA en ≥ 15/20 semillas (p 0.55).
- **Qué le faltaría (camino B).** El beneficio de limpiar cae al azar entre 9 cuerpos en 360 casillas. El valor individual aprendido lo ve,
  con razón, como pérdida privada. Para que la limpieza aparezca sin escribirla, la selección tiene que ser **entre linajes**.
  Con R0 y fundadores como aptitud, un linaje que limpia deja más linaje, aunque ninguno de sus cuerpos lo note. Eso es evolución, no aprendizaje.
  Una variante barata: recompensa del cuerpo = R0 del linaje. Sería escribir la respuesta en la recompensa, y lo desaconsejo.
- Los humos del SIN_HERENCIA v3 y del AZAR no se corrieron (tope de 6). Son los que menos sé predecir.

## Salida del arnés (`identidad_apr_salida.txt`, 2026-09-22 16:28:56)
```
(0) FABRICA sha 2ebee3e99ea5a33a OK · APR/SIN_HERENCIA/AZAR en disco == construye_apr OK x3
(A) OPCION 0 == FABRICA, N 1 compat 1 T 20000: s1 13/38 · s2 8/40 · s3 7/24, rng del mundo igual   OK x3
(A2) monolito organismo_f9c (sha 9dd1fb91ecec35ae) == APR(OPCION 0): 76 claves, dif []   OK
(B) N 9 escalada s8001 T 3000: APR, SIN_HERENCIA, AZAR (OPCION 0) == 9 FABRICA, rng fb4fd091957f2fd9   OK x3
(C) OPCION 1 difiere; oportunidades [276,238,205,259,253,256,222,238,222]   OK
(C2) ALFA_Q 0: fisica == FABRICA; 1946 oportunidades, 347 mordidas = FABRICA habria 347   OK
(D) determinismo OK · (E1) 2126 decisiones, todas sobre B/D · (E2) sin VAL_VIVO/EFECTO · (E3) revisa_carro PASA x3
(F) APR |Q| al nacer 0.52-1.56 · SIN_HERENCIA 0.0   OK x2 · (G1) AZAR sin P_AZAR aborta · (G2) 523/1722 = 0.304
TOTAL 21/21 en 55.8s
```
