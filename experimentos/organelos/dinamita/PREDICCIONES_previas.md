# EXPLORATORIO, no es dato — PREDICCIONES PREVIAS del bloque DINAMITA (creador, 28-sep-2026 ~12:10, escritas con la ola 1 corriendo y ANTES de leer un solo JSON de 39201–39230)

Misión: llegar a la AGI por este camino.

Diagnóstico que las motiva (`diagnostico.py`, `diagnostico_salida.txt`, sobre TERMO 39101–39140): 131/360 linajes de TERMO se vacían
después de un nacimiento real (O1: 25/360); 10–22 % de los hijos de TERMO mueren en ≤ 200 pasos (O1 < 1 %); paren 53 % (O1 70 %).

Ola 1: semillas 39201–39210, T 100 000, brazos termo, o1, vu, vh, vnav, vuinv, vw (10 semillas cada uno, un proceso por corrida).

| # | predicción | p |
|---|---|---|
| D1 | termo (base) en 39201–39210: P1 (semillas con mayoría que cruza) 4–8/10 | 0.75 |
| D2 | vu: fracción de hijos muertos en ≤ 200 pasos < 0.05 (termo ≈ 0.10–0.14) | 0.70 |
| D3 | vu: P1 ≥ 8/10 | 0.45 |
| D4 | vu: gana a termo en R0 real pareado en ≥ 7/10 | 0.55 |
| D5 | vu: mordidas B+D por linaje menores que termo; A+C del mundo igual o menor (riesgo "mundo tapado") | 0.65 |
| D6 | vh (consigna 1.2) ≤ vu en P1 (rompe la ventana del que limpia) | 0.55 |
| D7 | vw (consigna 1.0, dosis baja) ≤ vu en P1 | 0.55 |
| D8 | vnav ≥ vu en P1 | 0.40 |
| D9 | vuinv (control desfasado) NO se separa de vu tanto como TERMOINV de TERMO: al nacer E = Ag = 0.6 y las dos lecturas coinciden. Predigo vuinv P1 ≥ termo − 1 | 0.55 |
| D10 | o1: P1 ≥ 8/10 | 0.85 |

Qué refuta la línea VETO: vu con hijos ≤ 200 bajo 0.05 y P1 que NO sube sobre termo (el hijo que muere joven no era la causa), o hijos
≤ 200 que no bajan (el hijo no muere por lo sentido malo).

## Ola 2 (escritas ~12:20, tras ver SOLO las semillas 39201–39203 de la ola 1 y ANTES de correr la ola 2)
Lo visto: todos los VETO se hunden a ~0.25–0.30 (0/9 cruzan en 39201–39202). Los hijos ya no mueren en ≤ 200 pasos (0.00 contra 0.15),
pero mueren de hambre a los 600 (sin comer nada): el mundo baja de 3.3 a 2.2 buenos de 36 y los pasos sin ningún bueno suben de 3 % a
7–13 %. Es el "segundo muro" de `comite2/molde/HALLAZGOS.md` §3: el hijo que muerde lo malo y muere ERA el que limpiaba.
**D2 se cumple; D3, D4 quedan refutadas de hecho (se confirman con las 10 semillas).**

Ola 2 = la pieza DECIDE en los dos sentidos sobre lo sentido malo (el que puede pagar el golpe sin salir de la ventana limpia; el que
no, no muerde). Brazos lu (6), lh (8), luinv (7, control de lu); semillas 39201–39210.

| # | predicción | p |
|---|---|---|
| E1 | lu: mundo A+C ≥ 2.8 (vuelve cerca de termo) y hijos ≤ 200 < 0.05 | 0.50 |
| E2 | lu: P1 ≥ 8/10 | 0.25 |
| E3 | lu: gana a termo pareado en ≥ 6/10 | 0.35 |
| E4 | lh ≥ lu en P1 (limpia más, aunque el que limpia sale de la ventana) | 0.45 |
| E5 | luinv: P1 ≤ termo | 0.70 |

## Ola 3 (escritas ~13:05, tras ver la ola 2 completa y ANTES de correr la ola 3)
Ola 2 = NO (lu, lh, luinv ≈ 0.05–0.15; 0/10 semillas; ver tabla). Forzar al lleno a limpiar lo deja inmortal y estéril: cada golpe
lo baja a ~1.0 y la ventana de 500 pasos se rompe. **E2, E3, E4(?) refutadas; E1 refutada.** Tocar lo malo en la boca queda cerrado.

Ola 3 = PATAS sobre TERMO (TPATAS): pd DIRECTO, pu UTIL, pc UTIL+CEDE, pi INUTIL (control de pu). Semillas 39201–39210.

| # | predicción | p |
|---|---|---|
| F1 | pd (sólo paso directo al objetivo de v14.3): P1 ≤ termo + 1 (el objetivo de v14.3 incluye lo malo sin META) | 0.60 |
| F2 | pu: gana a termo pareado en ≥ 7/10 | 0.45 |
| F3 | pu: P1 ≥ 8/10 | 0.30 |
| F4 | pc ≥ pu en P1 | 0.55 |
| F5 | pi (control): P1 ≤ termo y gana a termo en ≤ 4/10 | 0.65 |
| F6 | pu/pc: hijos muertos a los 600 sin comer (v600) bajan respecto de termo | 0.60 |

## Ola 4 (escritas ~13:25, tras ver la ola 3 y ANTES de correr la ola 4) — confirmación EXPLORATORIA del ganador en semillas no vistas
Ola 3 (39201–39210): pc 8/10 (R0 0.943, gana a termo 7/10), pu 7/10 (0.960), pd 7/10 (0.913), pi (control) 1/10 (0.742), termo 6/10,
o1 10/10. F1 se cumple; F2 se cumple (pu 7/10); F3 refutada (pu 7/10); F4 se cumple; F5 se cumple (pi 1/10, 4/10); F6 REFUTADA (los hijos
≤ 200 suben a 0.19–0.20; pc mejora el ARRANQUE y los colapsos, no la muerte temprana del hijo).
**Sesgo del ganador:** pc es el máximo de 12 brazos probados en las mismas 10 semillas (5 VETO, 3 LIMPIA, 4 PATAS). Su 8/10 está
inflado. Por eso la ola 4 corre termo, pc, pu y pi en 20 semillas NO VISTAS (39211–39230).

**Regla de decisión, fijada ahora:** preparo el intento #4 con la pieza que dé **≥ 17/20** en 39211–39230 (la vara del encargo). Si
pc o pu dan 15–16/20, lo informo como "no claramente" y NO preparo el intento. Si dan ≤ 14/20, NO.

| # | predicción | p |
|---|---|---|
| G1 | pc en 39211–39230: P1 entre 11 y 17 de 20 | 0.75 |
| G2 | pc: P1 ≥ 17/20 | 0.20 |
| G3 | pc gana a termo pareado en ≥ 12/20 | 0.60 |
| G4 | pi (control): P1 ≤ termo | 0.75 |
| G5 | termo: P1 entre 9 y 16 de 20 | 0.75 |
