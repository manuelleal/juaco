# PREREGISTRO — camino A: ¿aprende un organismo a limpiar? (aprende_barrer, 22-sep-2026)

Misión: llegar a la AGI por este camino. Rama `aprende-barrer` (worktree `aprende`, sale de ff250a9). Escrito **después** de los humos
de práctica (8001–8002) y **antes** de la serie 8101–8120. Nada de 8101–8140 se ha corrido.

## 1. Pregunta y lo que ya dicen los datos
¿Puede un organismo que aprende (FABRICA = brazo REL de la fase 9) descubrir que morder lo malo le conviene, pasarlo al cuerpo
siguiente del linaje y cruzar H-1 sin que nadie le escriba la regla (O1 la trae escrita: `limpia = mejor is None and ...`)?

Antes de diseñar leí la serie sellada 5001–5020 (logs del juez, sin correr nada):
- **FABRICA ya limpia más que O1.** Con la medida física del juez, hace 1006 limpiezas por linaje-semilla (4.4 por cuerpo). O1 hace 392 (15.4 por cuerpo).
- **En el mundo de FABRICA casi nunca falta lo bueno:** 0.4 % de los pasos sin ningún objeto bueno. En el de O1, 5 %, y sin limpieza, 61 %.
- **FABRICA muere de lo que muerde:** 39 % veneno y 61 % sal, 0 % hambre o sed.

A FABRICA no le falta el bien público; le sobra el costo privado. Por eso la pregunta útil es si aprende **cuándo** morder lo malo:
contenerse cuando le cuesta y limpiar cuando no queda nada bueno. Esa es la regla de O1, y aquí tendría que salir de un valor aprendido.

## 2. Mecanismo (v3, congelado) y memoria nueva
- **Carros.** `carros/APR.py`, `APR_SIN_HERENCIA.py` y `APR_AZAR.py`. Los genera por anclas `construye_apr.py` desde `FABRICA.py`
  (sha `2ebee3e99ea5a33a`) y solo difieren en `MODO` y `P_AZAR`. Shas: APR `4402aa5142065c72`, SIN_HERENCIA `7c5ca65079a70383`,
  AZAR `14b5ecee1a4862f4` (con `P_AZAR` None; cambia cuando se fije).
- **Alcance de la opción.** Actúa solo sobre lo **malo conocido**: letras que el linaje ya mordió y cuyo dS sentido (el que devuelve `resultado()`) tiene
  alguna componente negativa. Sobre el resto decide la boca de FABRICA, sin cambios.
- **Decisión.** `logit p(morder) = logit(pb de FABRICA) + BETA·(Q1 − Q0)`, con el **mismo uniforme** que ya sacó FABRICA: no hay sorteo extra.
  Con Q1 = Q0, APR muerde exactamente cuando mordería FABRICA (arnés C2). Lo que se aprende es la **corrección**, en los dos sentidos:
  «añadidas» cuando limpia donde FABRICA no mordería y «quitadas» cuando se contiene donde FABRICA mordería.
- **Valor.** Q es lineal en 6 rasgos que el cuerpo siente:
  - 1;
  - u = min(E, Ag);
  - u después de morder, calculado con el dS que el linaje sintió con esa letra;
  - si no hay ningún objeto bueno en el mundo (bueno = lo que el linaje sintió como bueno para la necesidad activa);
  - la distancia al bueno más cercano;
  - el progreso propio en la ventana de parto.

  Se aprende por TD (SARSA esperado, semi-Markov entre decisiones) con la recompensa **real sentida**: +1 al parir y −1 al morir
  (terminal), más moldeo por potencial con u. El retorno sigue *nacimientos − muertes*. ALFA_Q 0.05, GAMMA 0.998 por paso, BETA 10.
  **No hay ningún umbral de «cuándo limpiar».**
- **Memoria nueva:** Q (2×6 números) y la memoria de letras (4×3). Ambas son del linaje.
- **Herencia (declarada; la misma vía que el nodo de FABRICA).** Pasan al cuerpo siguiente del linaje, sea hijo de la cola o fundador.
  En `APR_SIN_HERENCIA`, Q vuelve a 0 en cada nacimiento; la memoria de letras sí pasa.
- **APR_AZAR.** Muerde lo malo conocido con probabilidad fija `P_AZAR`. `P_AZAR` = tasa de mordida por oportunidad de APR en el
  **último cuarto de T**, sumada sobre las 20 semillas de la serie 8101–8120 (línea «ULTIMO CUARTO» del log). Se fija con
  `construye_apr.py --p_azar X` antes de correr AZAR y después se vuelve a correr `identidad_apr.py`.
  **Límite declarado:** AZAR quita a la vez la temporización innata de FABRICA y la aprendida. Si APR le gana, se sabe que el «cuándo»
  importa, no cuál de los dos.
- **Prohibido y verificado:** el rng del mundo y la tabla de valencias. Arnés E1–E3 y `revisa_carro` PASA.

## 3. Historia en práctica (declarada; ninguna semilla de la serie)
- **v1.** Recompensa = solo Δu, un moldeo puro sin objetivo real. Humo 8001, T = 30000: R0 **0.113** contra FABRICA 0.279 en la misma semilla.
  La política aprendió **al revés**: mordía más cuanto más cerca de morir (0.21 con u tras morder < 0 contra 0.04 con > 1.0).
- **v2.** Recompensa real (+1 parir, −1 morir), GAMMA 0.998 y rasgo de ventana, pero la opción **reemplazaba** la boca de FABRICA (p = 0.5 al nacer).
  Humo 8002: R0 **0.000–0.005** contra FABRICA 0.329: rompía la ventana de parto.
- **v3.** La opción **corrige** la boca de FABRICA. Humo 8002: R0 **0.377** contra FABRICA 0.329 en la misma semilla.
  - La corrección aprendida es **negativa en todas partes**: de −1.2 a −2.2 logit.
  - Añadidas: 0.0019 → 0.0002 por oportunidad del 1.º al 4.º cuarto; quitadas: 0.052–0.060.
  - Con o sin bueno en el mundo, la corrección es igual.
  - Aprendió a **contenerse**, no a limpiar.
- Después del humo v3 se agregaron dos contadores de telemetría (quitadas por edad y por índice del cuerpo), sin tocar la conducta:
  el arnés (C) da oportunidades y mordidas **idénticas** linaje por linaje antes y después del cambio.

Humos: 6 corridas de un proceso, T = 30000. Arnés `identidad_apr.py` **21/21**. CPU total ≈ 9 min.

## 4. Series (9 carros iguales, pista escalada L 360 / 36 objetos, T = 100000, pizarra 1, criterio ENMIENDA 3 sin cambios)
| serie | carro | papel |
|---|---|---|
| apr | APR | candidato |
| fab | FABRICA | piso (0.34 en la sellada) |
| o1 | O1 | techo diseñado; control de que la pista en semillas nuevas es la misma |
| sinher | APR_SIN_HERENCIA | ¿sirve lo heredado? |
| azar | APR_AZAR | placebo de «cuándo» |

- **Semillas.** Serie **8101–8120**; réplica **8121–8140**. Verificado con grep: ningún corredor de pista, juez ni dato las usa. La única
  coincidencia textual es el rng de mutación de `experimentos/evo` («8000+100*gen+...»), que es otro generador de otro experimento.
- **Cruza** (idéntico a la ENMIENDA 3). La mediana del R0 de los linajes-semilla evaluables (≥ 5 muertes) es ≥ 0.90, **y** al menos el 75 % de los evaluables
  no tiene fundadores después de t = 10000, **y** hay ≥ 120 de 180 evaluables.
- **Pareado** (regla 15). Por semilla, la mediana del R0 de los 9 linajes. «A > B» exige A mayor en **≥ 15/20** semillas **y** diferencia
  mediana ≥ 0.03. Con el nulo P = 0.5, la tasa de falso positivo es 0.021.

## 5. Predicciones firmadas (creador, antes de la serie)
| | predicción | p |
|---|---|---|
| P1 | APR **NO cruza** | 0.97 |
| P2 | Mediana del R0 de APR en 0.32–0.45 | 0.60 |
| P3 | FABRICA no cruza; mediana en 0.28–0.40 | 0.85 |
| P4 | O1 cruza | 0.85 |
| P5 | APR **no descubre** la limpieza. Añadidas en el último cuarto < 0.02 por oportunidad, o corrección (sin bueno) − corrección (con bueno) < 0.5 logit a u tras morder 0.8 | 0.93 |
| P6 | APR aprende a **contenerse**: quitadas en el último cuarto ≥ 0.03 | 0.85 |
| P7 | APR > FABRICA (≥ 15/20 y ≥ 0.03) | 0.55 |
| P8 | APR > APR_SIN_HERENCIA | 0.45 |
| P9 | APR > APR_AZAR | 0.70 |
| P10 | SIN_HERENCIA y AZAR no cruzan | 0.97 |
| P11 | Fracción de pasos sin ningún bueno con APR en 0.003–0.03 (el mundo no se ensucia) | 0.75 |

## 6. Lectura permitida y prohibida
- **FUNCIONA:** APR cruza en la serie **y** en la réplica 8121–8140, **y** P8 y P9 se cumplen (gana a SIN_HERENCIA y a AZAR). Se diría:
  *«un linaje que aprende la corrección de su boca sobre lo malo sostiene R0 ≥ 0.9 en la pista escalada, y lo heredado y la
  temporización son necesarios»*.
- **HAY ALGO MODESTO:** no cruza, pero P7 se cumple (APR > FABRICA) y se replica en 8121–8140 (`apr,fab`). Se diría *«aprende a contenerse y
  sube el R0 sin cruzar»*. Si además se cumple P8, *«y lo que hereda cuenta»*.
- **NO:** ni cruce ni P7. La limpieza no se descubre por aprendizaje individual en esta pista.
- **Prohibido:** «descubrió la limpieza» sin que P5 falle (añadidas ≥ 0.02 en el último cuarto **y** corrección +0.5 logit sin bueno);
  «coopera», «población», «generación», «evoluciona», «altruismo»; comparar con O1 fuera de su propia serie en las mismas semillas.

## 7. Qué lo refuta y controles que pueden fallar
- **P1 falla (cruza):** la limpieza **sí** es descubrible. Se refuta mi lectura de bien público.
- **O1 no cruza en 8101–8120:** la pista en semillas nuevas no es la de la sellada. No se lee nada de APR hasta aclararlo.
- **APR ≤ FABRICA:** el aprendizaje ni siquiera recupera la contención. Entonces el valor aprendido no alcanza ni para el costo privado.
- **SIN_HERENCIA ≥ APR:** lo que pasa por el linaje no suma. La corrección se aprende dentro de una vida o no sirve.

## 8. Comandos (solo el coordinador; Pool)
```
python experimentos/aprende_barrer/identidad_apr.py
python experimentos/aprende_barrer/corre_aprende.py --serie apr,fab,o1,sinher --desde 8101 --n 20 --pool 6
python experimentos/aprende_barrer/construye_apr.py --p_azar <ULTIMO CUARTO de apr>
python experimentos/aprende_barrer/identidad_apr.py
python experimentos/aprende_barrer/corre_aprende.py --serie azar --desde 8101 --n 20 --pool 6 --con <crudo _apr.json>,<crudo _fab.json>,<crudo _sinher.json>
# réplica (si P1 falla o P7 se cumple):
python experimentos/aprende_barrer/corre_aprende.py --serie apr,fab --desde 8121 --n 20 --pool 6
```
Coste estimado: APR tarda ≈ 40 s por semilla con T = 30000, así que ≈ 135 s con T = 100000. La serie de 4 × 20 son ≈ 3 h de CPU, unos 30 min con Pool 6.
AZAR, ≈ 8 min; la réplica, ≈ 15 min.
