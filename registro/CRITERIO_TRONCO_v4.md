# CRITERIO DE TRONCO v4 — VIGENTE (UTILIZABLE desde el 22-sep-2026) para candidatos NUEVOS (ERR-94; decisión del director 22-sep: retirar v3, escribir v4)

**Qué sustituye:** `registro/CRITERIO_TRONCO_v3.md` (21-sep), **retirado**: su réplica de calibración no repitió (CAL-1
0.898 por 0.002; CAL-4 disparado por un marginal, 0.627; el placebo cayó T-C (ii) en la realización, LI −11.93). v2 y v3
quedan como historia y como las letras con las que se juzgó a quien se juzgó.
**Qué NO hace — regla 3, lo primero:** **no rejuzga a nadie.** v15c–v15g, dE5, BA, BA-v, BA-vm, BA-vM y B-5 conservan
exactamente su veredicto. v14.2 sigue siendo el tronco hasta que un candidato cruce **esta** letra en semillas nuevas con
réplica. La justificación de cada cambio es el **nulo** (el tronco contra sí mismo, 320 corridas reales), no qué candidato cayó.
**Estado (23-sep-2026):** **UTILIZABLE.** La calibración V4-CAL (§4) cumplió V4-1..V4-5 en la serie 2841–2920 **y** en la réplica
2361–2440 (22-sep, REGISTRO "CRITERIO DE TRONCO v4 — calibración y réplica"). v3 retirado. *Historia del borrador:* hasta esa
calibración el texto decía "no utilizable" y los candidatos se juzgaban con v2 y v3 lado a lado.

---

## 1. Las ocho dimensiones (siete puertas + una reportada)

Todas en **semillas nuevas**, con **réplica en semillas nuevas** antes de congelar. Una puerta caída → no entra.

| # | dimensión | medida | letra v4 | por qué este umbral |
|---|---|---|---|---|
| **T-A** | **sobrevive** (mundo vivo vigente: dos necesidades, cuatro estímulos, `costo = costo_a = 0.001`; brazos `VIVO` y `CUELLO_MIN`) | muertes por 100 000 pasos; `r = descendientes − muertes` | en **cada** brazo: (a) mediana de muertes ≤ **1.10 ×** tronco; (b) mediana de `r` ≥ tronco **− 10**; (c) **no inferioridad** de una cola al 95 % sobre `d = r_cand − r_tronco`: `LI = media(d) − 1.645·EE(d) > −10`. **n = 80 por brazo** (era 40). | Con n = 40 el tronco contra sí mismo pasa T-A entera sólo **0.928** (bootstrap del nulo real; la réplica midió 0.898): 7 % de falso rechazo, fuera de la regla 15. Con n = 80: **0.999**; un candidato peor por 10 pasa 0.003, por 20 pasa 0.000. Los márgenes (10 en `r`, 1.10 en muertes) no se tocan: nunca fueron el problema. |
| **T-B** | **generaliza** a nunca vistos | `bateria_generaliza` G1/G2 | G1 ≥ 0.80, G2 ≥ 0.85, azar en [0.35, 0.65] (G2 en [0.42, 0.58]), K 20/20. **Sin cambio.** | Umbral lejos del nulo (azar 0.50). **No calibrado con placebo** (ver §7). |
| **T-C** | **se desdice** | (i) E2 del examen; (ii) `rev` en el mundo vivo (el veneno pasa a comida en T/2) | (i) conducta E2 ≥ 18/20, sin cambio. (ii) **no inferioridad** de una cola al 95 % sobre `d = rev_cand − rev_tronco` con **margen 12.5** (`LI > −12.5`), **n = 80** (era margen 10, n = 40). Se reportan `vis[B]`, `vis[A]` por cuarto al lado de `rev` (trampa 3). | §2: es la decisión de ERR-94. P(pasa \| nulo) **0.987–0.990**; el margen (12.5 ≈ 30 % de la reversión mediana del tronco, 41–42) se rechaza con 0.95 por construcción; un candidato peor por 20 pasa 0.000. |
| **T-D** | **sin alias ni superstición** | bloque de la sal (9 ALIAS / 9 LIMPIAS) | C1, C2, C6 de B-5, **importados** de `creacion_B/corre_codigo.UMBRALES` (ERR-31). Sin cambio. | Absolutos. **No calibrado con placebo** (§7). |
| **T-E** | **no regresión conductual** del examen v3′ | conducta por escenario frente al tronco en las mismas semillas | ≥ 18/20 por escenario, tolerancias 1.10 / 0.8. Pesos internos reportados, no puerta. Sin cambio. | Determinista: el tronco contra sí mismo da 20/20 bit a bit. **Con un candidato inerte que mueva el generador, no medido** (§7). |
| **T-F** | **coste** | celdas, divisiones, muertes | ≤ **1.25 ×** tronco (medianas), en el examen y en el mundo vivo. En el mundo vivo se calcula sobre las corridas de T-A y T-C (ii), con divisor `max(tronco, 1)` (el tronco tiene medianas de `splits` 6–7; nunca 0, pero la guarda se declara). | En el nulo real: celdas 36–37 en todos los brazos, splits 6–7; 1.25 × 7 = 8.75 queda a > 2 EE de la mediana a n = 80. PEOR (coste ×1.5) da muertes 1.6–1.8 ×: cae. |
| **T-G** | **capacidad nueva** | la que el preregistro del candidato declare | **Aquí y sólo aquí vive GANAR**: medida, control barajado o CONST, nulo, margen y la n que da **≥ 0.95 bajo el nulo y ≥ 0.80 en el margen**, calculada con la sd de la diferencia **medida** (referencias: sd(d) de `r` 16–19; de `rev` 27–31). Sin capacidad nueva no hay candidato v15 (una reparación inerte entra como v14.x). | Sin cambio de v3. |
| **T-H** | **ESCALA** — **reportada, NO eliminatoria** (instrucción del coordinador con el director, 22-sep) | `D = (M_g / M_c)_cand / (M_g / M_c)_tronco`, con `M` = mediana de muertes por 100 000 pasos en el brazo `VIVO`, `g` = mundo grande, `c` = mundo chico (el de T-A); las mismas semillas | **Se reporta** `D` con su intervalo bootstrap al 95 % y la frase "se degrada más que el tronco al crecer" si el límite inferior de `D` > 1. **Umbral propuesto para cuando sea eliminatoria:** no inferioridad `LS_95(log D) < log 1.20` (el candidato no puede perder más de un 20 % adicional de vida al crecer el mundo). | §5. `M` es positivo y no satura (la `vida_mediana` sí: 600 en casi todas las corridas; `r` es negativo y una razón de negativos no significa nada). |

**Brújula (no es filtro):** el informe de cada candidato lleva una línea más: *"¿en qué peldaño biológico está este
mecanismo? (bacteria / gusano / mosca / abeja / mamífero / ninguno)"*, con una frase de por qué. No decide nada; sirve
para ver hacia dónde se mueve la línea de candidatos.

---

## 2. ERR-94 decidido: n = 80 en el mundo vivo, y margen 12.5 en T-C (ii)

El encargo pedía elegir entre **n = 80** y **margen 15** con un cálculo de potencia. El cálculo
(`experimentos/criterio_v4/analiza_potencia_v4.py`, sobre las **320 corridas reales del nulo** de A-CAL, 2121–2200 y
2281–2360; bootstrap no pareado, B = 4000, porque el pareado en el mundo vivo es nominal; el modelo normal da lo mismo
a ±0.01) dice que **ninguna de las dos, sola, cumple la regla 15** (el tronco contra sí mismo debe pasar ≥ 0.95):

| opción | n T-A | n T-C | margen T-C | P(pasa \| nulo) T-A | T-C (ii) | **las dos** | **falso rechazo del tronco** | sd(d) máxima de `rev` que aguanta 0.95 en T-C |
|---|---|---|---|---|---|---|---|---|
| v3 (retirada) | 40 | 40 | 10 | 0.928 | 0.707 | 0.656 | **0.34** | 19.2 |
| **sólo n = 80** | 80 | 80 | 10 | 0.999 | 0.931 | 0.930 | **0.07** | 27.2 |
| **sólo margen 15** | 40 | 40 | 15 | 0.928 | 0.950 | 0.882 | **0.12** | 28.8 |
| **ELEGIDA: n = 80 y margen 12.5** | 80 | 80 | 12.5 | 0.999 | 0.987 | **0.986** | **0.014** | **34.0** |
| n = 80 y margen 15 (reserva) | 80 | 80 | 15 | 0.999 | 0.999 | 0.998 | 0.002 | 40.8 |

sd(d) observada de `rev`: **27.4** (serie) y **30.9** (réplica). Por eso "sólo n = 80" falla (su techo 27.2 queda por
debajo de las dos series) y "sólo margen 15" queda en el filo (techo 28.8: la réplica lo rompe). **Y T-A a n = 40 tampoco
cumple** (0.928): esto no estaba en la propuesta de ERR-94 y es lo que explica el 0.898 de la réplica.

**La elección y su porqué.** n = 80 en las dos puertas del mundo vivo (arregla T-A y es una sola n para todo el mundo
vivo) y, para T-C (ii), **el menor margen en pasos de 2.5 cuyo techo de sd(d) cubre la sd más alta observada (30.9) con
holgura**: 10 → 27.2 (no), **12.5 → 34.0 (sí)**. 15 también cumple, pero deja pasar con 0.46 a un candidato que revierte
10 puntos peor (12.5: 0.19). Se prefiere la puerta más fina que cumple. Y se calcula además **la potencia de la propia
calibración** (la lección de la réplica de v3, que falló por el ruido de su estimador): simulando 200 series de
calibración con el nulo real, la estimación por reparto de P(las dos puertas) sale ≥ 0.95 en **0.985** de las series con
la opción elegida (0.335 con "sólo n = 80"; 0.075 con "sólo margen 15").

**Coste por candidato.** T-A 80 × 2 brazos × 2 (candidato, tronco) = 320 corridas + T-C (ii) 80 × 2 = 160 → **480
corridas de T = 100 000** (v3: 240), ~9–11 s de CPU cada una → **~20 min con Pool 6**, más el examen y T-B como hoy.
Con réplica, el doble. Se reusan las corridas del tronco entre candidatos **sólo** si comparten semillas y la réplica se
hace en semillas nuevas.

---

## 3. Reglas de forma

Siguen **1, 2, 5, 6, 7, 8 y 9 de v3** (ningún umbral sobre el nulo; nulo, margen y n declarados con su cálculo; tasas
balanceadas con J; el pareado en el mundo vivo es nominal; la capacidad se cobra una vez; identidad, anclas, regla 14,
humo con JSON, ERR-31/87/89; cambiar la letra exige ERR). Cambian:

3′. **n = 80 por brazo en el mundo vivo** (T-A y T-C ii), justificado en §2. En el examen (determinista) n = 20 sigue.
4′. **Dos brazos de control obligatorios en toda serie del mundo vivo** que juzgue a un candidato:
   - **TRONCO_B**: el tronco, **sin perilla**, en la semilla `s + 100000`. Ley idéntica **por construcción** (mismo
     código, mismos kwargs, el generador no se toca: es la opción "placebo sin tocar el rng" de ERR-94). Si TRONCO_B
     no pasa la letra, la serie no se lee.
   - **PLACEBO** (`placebo = 1`, consume un sorteo por paso y lo descarta): el candidato inerte. Se reporta; su paso es
     condición de la calibración (§4), no de cada candidato.
10. **CAL-4 deja de ser gatillo.** Seis marginales `A₁₂` no pareados en [0.40, 0.60] con n = 40 disparan en falso **0.468**
   de las veces con ley idéntica (0.113 con n = 80): era una puerta sin su cálculo del nulo, lo mismo que ERR-91
   condenó. Los marginales se **reportan** con la banda de Bonferroni que tiene 0.95 bajo ley idéntica
   (n = 80: [0.379, 0.621]). La validez del instrumento la da TRONCO_B, que es el nulo por construcción.
11. **Toda calibración declara su propia probabilidad de declarar utilizable a una letra bien hecha** (la suma de sus
   condiciones), antes de correr. La de v3 era ~0.5 por su CAL-4 y nadie lo había calculado.

---

## 4. Calibración exigida antes de usar v4 (bloque V4-CAL, `experimentos/criterio_v4/`)

Cuatro brazos del mismo organismo (`organismo_v3cal`, reusado con sha `148014f68cb01785`), 80 semillas nuevas
(2841–2920): OFF, TRONCO_B, PLACEBO, PEOR (coste de vida ×1.5, conocido malo: cae T-A en las dos series de A-CAL).
T-A 640 corridas + T-C (ii) 320 = **960 corridas por serie**; réplica en 80 semillas nuevas que asigna el coordinador.

| condición | qué | umbral | por qué |
|---|---|---|---|
| **V4-1** | el tronco contra sí mismo, por reparto del nulo OFF + TRONCO_B (160 corridas por puerta) | P(T-A y T-C ii pasan) **≥ 0.95** | la regla 15, medida sobre la puerta entera |
| **V4-2** | TRONCO_B pasa T-A, T-C (ii) y T-F del mundo vivo en la realización | pasa | lo que pidió el director: el tronco contra sí mismo pasa v4 |
| **V4-3** | PLACEBO (inerte) pasa lo mismo | pasa | un candidato inerte no puede caer |
| **V4-4** | PEOR cae v4 | cae | un candidato conocido como malo debe caer |
| **V4-5** | desplazamiento exacto por reparto: δ = −20 | pasa **≤ 0.05** en cada puerta | la letra tiene dientes |
|  | δ = −margen | pasa **≤ 0.15** | por construcción ~0.05; verifica z y margen cableados |

**Probabilidad de que la calibración declare utilizable a una v4 bien hecha** (regla 11): por serie ≈ 0.985 (V4-1) ×
0.986 (V4-2) × 0.986 (V4-3) × ~0.98 (V4-5) ≈ **0.94**; serie + réplica ≈ **0.88**. Regla escrita ahora para no
recalibrar después: si **una sola** condición de realización (V4-2 o V4-3) cae en **una sola** serie con V4-1 cumplido,
se declara mala suerte con su probabilidad (~0.014) y se corre una tercera serie en semillas nuevas; si vuelve a caer,
v4 se retira con ERR. Si V4-1 cae en cualquier serie, v4 se retira.

---

## 5. T-H, la dimensión ESCALA: instrumento, coste y cuándo pasa a eliminatoria

**Instrumento (el más barato que existe).** El tronco no tiene hoy una perilla de escala: `organismo_v3cal` fija la
retina en 6 píxeles y los estímulos en ABCD (`PAT`, `L = 40`). Lo más barato del repo es la inserción de la bacteria B
de la carrera (`experimentos/carrera_fase10/B/construye_B.py`: `retina = D`, `mundoB = F` = F familias × F variantes
sobre 2F píxeles, arnés 77/77 en su linaje), **portada por anclas a `organismo_v3cal`** (el tronco v14.2): mundo grande =
`mundoB = 4, retina = 8, vira = 0` → **16 estímulos compuestos, 4 × los 4 del mundo vivo**, con las mismas cuatro
valencias y **sin** la variante que invierte (`vira = 0`: escala pura, no una trampa nueva). Organismo B **no** se usa
tal cual: es del linaje f9c, no del tronco v14.2. **Paquete por construir** (`construye_escala_v4.py` + arnés
`mundoB = 0 ≡ organismo_v3cal` bit a bit + controles que deben fallar); no está hecho en este borrador. Alternativa de
cero código, peor como medida: `nobj = 16` (4 × objetos en el mismo mundo) mide densidad, no escala de
representación; sólo si el port no cierra su arnés.

**Métrica.** `D` de §1 sobre muertes (positivas, sin saturar). Con la sd medida de log(muertes) en el mundo chico
(0.106 por corrida), `sd(log D)` ≈ 0.043 con n = 40 y 0.034 con n = 80, **suponiendo** que el mundo grande tiene la misma
sd (no medido).

**Coste extra.** Sólo el brazo `VIVO` en el mundo grande (el chico ya está en T-A): n × 2 (candidato, tronco). Reportada
con n = 40: 80 corridas × ~9 s × ~1.3 (16 estímulos, retina 8; factor supuesto, a medir en el humo del paquete) ≈
**940 s de CPU ≈ 2.6 min con Pool 6** por candidato (+13 % sobre T-A + T-C). Eliminatoria con n = 80: ≈ 5.2 min (+26 %).

**Cuándo pasa de reportada a eliminatoria** (por ERR, nunca en caliente): (1) el paquete del mundo grande cierra su
arnés; (2) una calibración propia (TRONCO_B y PLACEBO pasan `LS_95(log D) < log 1.20` y un control de escala malo — el
tronco con retina de 6 píxeles forzada a leer los 16 estímulos por alias — cae), con la n calculada con la sd **medida**
de log D en el mundo grande; (3) **al menos 3 candidatos** medidos con T-H reportada, para tener la sd de `D` en
organismos que no son el tronco. Hasta que se cumplan las tres, T-H no tumba a nadie, y ningún candidato que hoy entre
se rejuzga cuando se active.

---

## 6. Qué NO se rejuzga

Nada. v15f, dE5, v15c–v15g, BA, BA-v, BA-vm, BA-vM: sus veredictos se quedan. B-5 sigue siendo v14.2. v4 rige **sólo**
candidatos futuros, con semillas nuevas, y **sólo** desde que V4-CAL cumpla V4-1..V4-5 en serie y réplica.

## 7. Límites declarados

- **Las puertas del examen (T-B, T-C i, T-D, T-E) no están calibradas con placebo.** Son umbrales absolutos lejos del
  nulo y el tronco contra sí mismo las pasa bit a bit, pero nadie midió qué hace con ellas un candidato **inerte que
  mueva el generador** (el arnés de A-CAL, M3, muestra que `placebo = 1` sí cambia el mundo del examen). Paquete
  siguiente sugerido: E-CAL (PLACEBO por las baterías congeladas copiadas por anclas, regla 14).
- **PEOR no es malo en T-C (ii)** (el coste ×1.5 no empeora la reversión: pasó T-C ii en las dos series de A-CAL). Los
  dientes de T-C (ii) se prueban con el desplazamiento exacto (V4-5); falta un candidato real malo en reversión.
- **El reparto trata a TRONCO_B como el nulo**; si alguna semilla ≥ 100 000 se comportara distinto (no hay razón: el
  generador es `default_rng(seed)`), los marginales de TRONCO_B lo mostrarían.

Creador (Opus), borrador del 22-sep-2026 para el coordinador. Números: `datos/humo/potencia_v4_20260922_125604.json`
(`2d975a4885eb41ae`) y `datos/humo/potencia_v4_meta_20260922_130017.json` (`1e9eb3843c48703e`).
