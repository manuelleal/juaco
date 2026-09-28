# PREREGISTRO — bloque TERMO: ÚLTIMO intento del muro de la carrera (creador, 28-sep-2026, escrito ANTES del humo)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo.

**Es el último intento sobre el muro (decisión del director).** Regla de parada en la sec. 7.

## 0. Pregunta
¿Una sola pieza local de boca sobre v14.3 hace que el linaje del bicho real cruce H-1 en la pista de la carrera?
- La pieza es un termostato de dos necesidades, sin memoria nueva y sin constantes de O1.
- La pista y el juez se usan tal cual: `cruza_real`, ENMIENDA 5.

## 1. De dónde sale (EXPLORATORIO, `experimentos/organelos/boca_buena/INFORME.md`)
- **El puenteo del comité 2.** Injertar sólo la boca de O1 sobre lo bueno (boca_buena) sube a V143 a 0.944, en 10/10 semillas.
- **Ablaciones de boca_buena** (semillas 39001–39010, T 100 000, mediana del R0 real):

| brazo | R0 |
|---|---|
| V143 | 0.413 |
| boca_buena | 0.928 |
| sin neofobia | 0.935 |
| sólo neofobia | 0.397 |
| O1 sólo puede decir NO | 0.824 |
| O1 sólo puede decir SÍ | 0.777 |
| sin consigna | 0.895 |
| consigna = rep_umbral | **0.000** (0 linajes establecidos) |
| consigna rep_umbral + 0.10 | 0.921 |
| consigna rep_umbral + 0.40 | 0.951 |
| CONTROL que lee la otra necesidad | 0.106 |
| GLOTU | 0.754 |

- **Lectura:** lo que carga el efecto es morder lo bueno para CUALQUIER necesidad que esté bajo una consigna, y no morderlo si todas
  las que sube ya están en la consigna. La consigna tiene que estar por encima del umbral de parto; la banda 1.1–1.4 funciona.

## 2. Mecanismo mínimo (perilla `TERMO = 1`) y memoria nueva
- **Regla.** Sea s el dS medio SENTIDO por el linaje al morder la letra k (`_adS`, ya en v14.3). Si s no tiene componentes negativas y
  tiene alguna positiva, la pieza decide:
  - **muerde ⇔ ∃ j: s_j > 0 ∧ nivel_j < rep_umbral + s_j / 2**;
  - dicho de otro modo: come si alguna necesidad que la letra sube está por debajo del umbral de parto más media mordida.
- **Alcance:** esa decisión manda sobre la boca de fábrica, el FILTRO y la opción APR, sólo para esas letras. Lo desconocido y lo
  sentido malo quedan como en v14.3.
- **Sin rng nuevo:** el sorteo de la boca se consume igual que en v14.3.
- **Memoria nueva: cero.** `_adS` y `rep_umbral` (en ctx) ya están; los niveles E y Ag los da la pista.
- **La constante ½ es PROPIA y sale del exploratorio 39001–39010** (declarado):
  - fijé la forma "media mordida" DESPUÉS de ver que la banda 1.1–1.4 funciona y que el umbral exacto mata;
  - en esta pista s_j = 0.8, así que S = 1.4. No es el MARGEN de O1 (1.25).
- **CONTROL `TERMO = 2` (TERMOINV), desfasado:** la misma regla leyendo el nivel de la necesidad que la letra NO sube
  (lev[1 − j] en vez de lev[j]). Tiene la misma lectura, la misma consigna, las mismas letras y los mismos pasos.
  - **Puede fallar:** si lo que importara fuera sólo cuánto se come o el patrón temporal de mordidas, TERMOINV también subiría.

## 3. Instrumento y anclas
- **Carros** (`construye_termo.py`, sha 23f57933c51c64e8): se construyen POR ANCLAS desde `tronco_v14_3/carros_v143/V143.py`
  (2a03048a7f1525e5), cinco anclas, cada una exacta una vez.
  - `V143_TERMO` 3db639cab75641fb (TERMO 1) y `V143_TERMOINV` da106a995b18bafd (TERMO 2).
  - Los dos difieren sólo en la línea de perillas y el nombre.
- **Runner** `corre_termo.py`:
  - la corrida ES `corre_v143.tarea`, importada (regla 14);
  - letra, resumen, pareados, nube-9, `--reanuda` y ERR-115 tienen el mismo formato y la misma letra que `corre_muro.py`;
  - **los shas de TODO lo que corre quedan fijados ANTES del humo** en `SHAS`: carros, construye, V143, pista, juez, O1, corre_v143 y
    revisa_carro. Si alguno cambia, `verifica()` falla y no se corre nada. El sha del propio runner lo registra el log.
- **Arnés** `identidad_termo.py` (salida en `identidad_termo_salida.txt`):
  - (K) construcción == disco;
  - (a) TERMO = 0 == V143, salida ENTERA;
  - (b) V143_TERMO == `boca_buena/carros/HIBB.py` (BB 'm40') en la física bit a bit: la pieza ES el brazo m40 del exploratorio;
  - (c) TERMOINV == HIBB 'tinv40', distinto de TERMO; la pieza actúa en ambos; determinismo;
  - (d) `verifica()` con shas fijados, `valida()`, ERR-115 y la letra en casos sintéticos.

## 4. Brazos, semillas, T y costo
- **Brazos:** `v143` (base), `termo` (CANDIDATO), `termoinv` (CONTROL), `o1` (techo y ancla).
- **Pista:** monocultivo de 9 carros iguales, L 360, 36 objetos, T 100 000, fundador limpio (ENMIENDA 5).
- **Semillas NUEVAS:**
  - serie 39101–39120; réplica 39121–39140;
  - humo 39911–39912; arnés 39913–39914;
  - exploratorio previo (ya usado): 39001–39010 y 39901–39902.
- **Costo:** 80 corridas por serie, unos 60–70 min con Pool 6 (el exploratorio tardó 300–450 s por corrida con 6 procesos).

## 5. Predicciones firmadas (antes del humo)
| # | predicción | rango | p |
|---|---|---|---|
| T1 | V143: mediana del R0 real | [0.35, 0.70] | 0.80 |
| T2 | O1 cruza (≥ 15/20 semillas con mayoría) | 17–20/20 | 0.95 |
| T3 | TERMO: mediana del R0 real | [0.85, 0.97] | 0.75 |
| T4 | TERMO contra V143 pareado: semillas ganadas / diferencia mediana | ≥ 18/20 / [+0.25, +0.60] | 0.80 |
| T5 | TERMO: semillas con mayoría de linajes que cruzan | 10–17/20 (P1 exige ≥ 15) | 0.70 |
| T6 | TERMO: A+C por linaje menor que V143, y B+D ≤ 0.8 × V143 | | 0.75 |
| T7 | TERMOINV: mediana del R0 real ≤ 0.25 y 0/20 que cruzan | | 0.85 |
| V | Veredicto de la SERIE: FUNCIONA / HAY ALGO MODESTO / NO / NO SE LEE | | 0.35 / 0.40 / 0.08 / 0.17 |
| VB | Veredicto del BLOQUE (serie + réplica): FUNCIONA / HAY ALGO MODESTO / NO / NO SE LEE | | 0.20 / 0.42 / 0.08 / 0.30 |

## 6. LA LETRA (la misma que el muro; `corre_termo.lee_serie`; el arnés la prueba en casos sintéticos)
**Validez (si una falla: NO SE LEE):**
- V1: serie completa (80 corridas, 0 abortos, contabilidad coherente en todos los brazos).
- V2: el ancla O1 GANA (ENMIENDA 5: ≥ 15/20 semillas con mayoría de linajes que cruzan).
- V3: V143 en [0.40, 0.80] (mediana del R0 real; la misma ventana del muro).
- V4: la pieza ACTÚA: la telemetría `termo` (última instancia) cambió al menos una decisión (`a_no + a_si > 0`), en el candidato y en el control.

**Puertas:**
- **P1 (el candidato cruza):** ≥ 15/20 semillas con mayoría de linajes con `cruza_real`.
- **P2 (le gana a V143):** pareado por semilla (mediana del R0 real de los 9 linajes), gana en ≥ 15/20.
- **P3 (el control no cruza):** TERMOINV NO gana por ENMIENDA 5.

**Veredictos:**
- **FUNCIONA:** V1–V4 y P1, P2 y P3.
- **HAY ALGO MODESTO:** P2, más diferencia mediana pareada ≥ 0.10, más el candidato le gana al control en > 10/20.
- **NO:** todo lo demás.
- **Bloque:** si serie y réplica coinciden, vale ese veredicto; si no, vale el menor. NO SE LEE manda.

## 7. REGLA DE PARADA (decisión del coordinador con el director; se escribe antes de correr)
- La **réplica** (39121–39140) se corre **si la serie no da NO**. Si la serie da NO SE LEE, el coordinador decide antes de la réplica.
- **FUNCIONA** (serie + réplica) → TERMO es **candidato a v14.4**; pasa al criterio de tronco v4.
- **HAY ALGO MODESTO** → TERMO queda como candidato a v14.4 por mérito propio, pero el **muro se declara MAPEADO** y no hay más
  intentos sobre él.
- **NO** → **muro MAPEADO** y vuelta a ECO.

## 8. Riesgos declarados
- **Sesgo del ganador.** m40 (== TERMO) se eligió entre m10, m40, ventana y la referencia en las MISMAS semillas 39001–39010 en que se
  midió. Su 0.951 y su 6/10 de mayorías pueden estar inflados.
  - Con una tasa por semilla de mayoría que cruza entre 0.6 y 0.75 (m40 6/10; la banda 1.1–1.4, 30/40), P1 (≥ 15/20) pasa con
    probabilidad 0.13–0.62 por serie. **P1 es la puerta débil.**
- **Riesgo de V3.** V143 dio 0.413 en 39001–39010, en el borde de la ventana [0.40, 0.80]; en el muro dio 0.536–0.63. Si V143 cae bajo
  0.40, la serie es NO SE LEE aunque TERMO cruce. Lo acepto, no cambio la ventana: es la del muro.
- **Constante ½ elegida con los datos** (sec. 2).
- **Igualdad en coma flotante.** La identidad con HIBB m40 es bit a bit en las semillas del arnés. Un nivel exactamente igual a 1.4 con s
  medio ≠ 0.8 por redondeo podría separarlas, pero sólo afecta a esa comparación con el exploratorio, no a la serie.
- **Letras "nulas".** Las letras con s todo 0 quedan en v14.3 (HIBB no las mordía); en esta pista no existen.

## 9. Las cuatro trampas
- **Canal simétrico:** no aplica. La pieza no usa canal; nadie escribe en la pizarra.
- **Acierto sin balancear:** no aplica. La medida es el R0 real de nacimientos del juez.
- **Mundo que se come la comida:** es parte del mecanismo (la consigna deja comida en el mundo). Se mide A+C y B+D por linaje y
  `comp_mundo` como descriptivo (T6).
- **Sitios fijos:** no aplica. Posiciones, turnos y reapariciones salen de los rng de la pista, sembrados por semilla y linaje.

## 10. Comandos (el coordinador)
```
python experimentos/organelos/termo/construye_termo.py --verifica
python experimentos/organelos/termo/identidad_termo.py
python experimentos/organelos/termo/corre_termo.py --humo
python experimentos/organelos/termo/corre_termo.py --serie --desde 39101 --n 20 --pool 6
python experimentos/organelos/termo/corre_termo.py --serie --desde 39121 --n 20 --pool 6     # replica, solo si la serie no da NO
python experimentos/organelos/termo/corre_termo.py --bloque <resumen serie>,<resumen replica>
```
