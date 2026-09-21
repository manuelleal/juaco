# CRITERIO DE TRONCO v3 — vigente para candidatos NUEVOS desde el 21 sep 2026 (decisión del coordinador delegada por el director, 18:50)

**Qué sustituye:** la letra de `registro/CRITERIO_TRONCO_v2.md` (18-sep 09:58). El criterio v2 sigue citado como historia y
como la letra con la que se juzgó a v15f y a dE5; deja de decidir sobre candidatos nuevos.
**Qué NO hace — regla 3, y es lo primero:** **NO rejuzga a nadie.** v15c, v15d, v15e, v15f, v15g, dE5, BA, BA-v y B-5
quedan exactamente con el veredicto que tienen. Ningún candidato ya medido vuelve a la mesa por este documento. v14.2
sigue siendo el tronco hasta que un candidato cruce **esta** letra en semillas nuevas y con réplica.
**Estado de calibración:** esta letra se escribe junto con su bloque de calibración (`experimentos/criterio_v3/`,
A-CAL). Hasta que ese bloque corra y sus predicciones CAL-1..CAL-5 estén juzgadas, v3 es **la letra vigente pero con su
propia potencia todavía no medida en serie**; el número que la motiva (§3) sí está medido sobre corridas reales.

---

## 1. Las siete puertas

Todas, en **semillas nuevas**, con **réplica en semillas nuevas antes de congelar**. Una sola puerta caída → no entra, sin
modos intermedios (regla 11 para cualquier cambio de umbral, con ERR).

| # | puerta | medida | letra v3 (umbral, nulo, margen y n declarados) |
|---|---|---|---|
| **T-A** | **sobrevive** en el mundo vivo vigente (hoy: dos necesidades, cuatro estímulos, `costo = costo_a = 0.001`, brazos `VIVO` y `CUELLO_MIN`) | muertes por 100 000 pasos y `r = descendientes − muertes` | **(a)** mediana de muertes ≤ **1.10 ×** la del tronco; **(b)** mediana de `r` ≥ tronco **− 10**; **(c)** **no inferioridad pareada de una cola al 95 %** (z = 1.645) sobre `d = r_cand − r_tronco`, con **margen 10**: `LI = media(d) − 1.645·EE(d) > −10`. **n = 40 por brazo.** **Se ELIMINA la cláusula `A₁₂ ≥ 0.50`.** Nulo declarado: `d = 0`. |
| **T-B** | **generaliza** a nunca vistos | `bateria_generaliza` G1/G2 en la configuración del candidato | G1 ≥ 0.80, G2 ≥ 0.85, azar en [0.35, 0.65] (G2 en [0.42, 0.58]), K 20/20. **Sin cambio respecto de v2** (umbrales lejos del nulo: azar = 0.50, umbral 0.80). |
| **T-C** | **se desdice** | (i) reversión del examen (E2: tras el cambio de regla come B en Q4); (ii) reversión en el mundo vivo (`rev`, el veneno que pasa a comida) | **(i) sin cambio:** conducta E2 ≥ 18/20 (umbral absoluto, lejos del nulo). **(ii) pasa de "ganar" a NO INFERIORIDAD:** `LI` de una cola al 95 % de `d = rev_cand − rev_tronco` **> −10**, **n = 40**. **Se ELIMINA `A₁₂ ≥ 0.75`.** La exigencia de *revertir mejor* se declara y se mide en **T-G**, no aquí. Junto a `rev` se reportan **las exposiciones por cuarto** (`vis[B]`, `vis[A]`): sin ellas, `rev` no es interpretable (trampa 3). |
| **T-D** | **sin alias ni superstición** | bloque de la sal (9 ALIAS / 9 LIMPIAS) | C1, C2, C6 de B-5, **importados** de `creacion_B/corre_codigo.UMBRALES` (nunca copiados: ERR-31). Sin cambio. |
| **T-E** | **no regresión conductual** del examen v3′ | por escenario, la CONDUCTA (come / evita / recupera) frente al tronco en las mismas semillas | ≥ 18/20 por escenario, con las tolerancias declaradas (1.10 / 0.8). Los pesos internos se **reportan**, no son puerta. Sin cambio (es determinista y pareado de verdad: la misma semilla es la misma trayectoria). |
| **T-F** | **coste** | celdas, divisiones, muertes en el examen y en el mundo vivo | ≤ 1.25 × tronco (medianas); se declara antes si se espera más. Sin cambio. |
| **T-G** | **capacidad nueva** | la que el preregistro del candidato declare | **Aquí y sólo aquí vive la exigencia de GANAR.** El preregistro declara la medida, su **control barajado o CONST** (misma cantidad de empuje, sin información), su nulo, su margen y la **n que da 0.95 bajo el nulo y 0.80 en el margen**. Sin capacidad nueva declarada no hay candidato (una reparación inerte como B-5 entra como v14.x, no como v15). |

---

## 2. Reglas de forma (nuevas; valen para toda puerta de todo preregistro, no sólo las siete)

1. **Ninguna puerta usa un umbral igual al valor del nulo.** Un umbral puesto en la media de la hipótesis nula es un
   volado que **no mejora con más semillas** (`A₁₂ ≥ 0.50` pareado: n = 20 → 0.588, n = 40 → 0.563, n = 80 → 0.544,
   n → ∞ → 0.500). Si la puerta quiere decir "no es peor", se escribe como **no inferioridad con margen**; si quiere
   decir "es mejor", se escribe como **superioridad con margen** y vive en T-G.
2. **Toda puerta declara, ANTES de correr: su nulo, su margen y su n** — y la n se justifica con el cálculo de que
   (a) el nulo pasa ≥ 0.95 y (b) el margen se rechaza ≥ 0.80. Ninguna puerta de conteo `k/n` se abre sin ese cálculo
   escrito (regla nacida de P6 de la fase 5: con p = 0.842 real, `dist ≥ 15/19` cae 1 serie de cada 5.9).
3. **n = 40 por brazo en el mundo vivo** (T-A y T-C ii). Con la sd medida de la diferencia (11 a 19.5 puntos de `r`) y
   margen 10, hacen falta n = 34–42 para que el idéntico pase el 95 % de las veces. En el **examen** (determinista) n = 20
   sigue bastando: allí la misma semilla sí es la misma trayectoria.
4. **Brazo PLACEBO obligatorio en toda serie del mundo vivo.** El PLACEBO es el mismo organismo con una perilla que
   **consume k sorteos por paso y descarta el valor** (`placebo = k`): misma ley, otra trayectoria. Si el PLACEBO no pasa
   la puerta, **la puerta está rota y la serie no se lee**. Es el control negativo del instrumento, no del organismo.
5. **Toda tasa de acierto se reporta balanceada.** Nunca `p1` sola: siempre con su par `c1` y con el índice
   **J = p1 + c1 − 1** (Youden). Un control "cauteloso" infla `p1` gratis y aparenta discriminar (fase 9, F9-4:
   `p1(REL_BAR) = 0.568 > p1(NADA) = 0.344`, pero `J(REL_BAR) = 0.166 ≤ J(NADA) = 0.186`).
6. **El pareado por semilla en el mundo vivo es NOMINAL, y se dice.** Medido: `sd(d)/(√2·sd(OFF))` = 0.85–1.35 y
   `ρ(ON, OFF)` = −0.47…+0.38 (compatible con 0): la misma semilla **no** controla la trayectoria cuando el organismo
   cambia. El pareado se conserva porque no daña, pero **no se le atribuye potencia**; la n se calcula con la sd de la
   diferencia observada, no con la del brazo.
7. **La capacidad se cobra UNA vez.** Si un candidato declara "revierte mejor", eso es T-G con su control; T-C (ii) sólo
   pregunta si **no se desdice peor**. Cobrar la misma virtud en dos puertas fue lo que hizo que ninguna reparación
   inerte-pero-útil pudiera volver a entrar.
8. **Sin cambio:** perilla apagada ≡ tronco **bit a bit** con arnés de identidad y controles que DEBEN fallar, corrido
   **antes** de mirar números; instrumentos por anclas con sha fijado; batería copiada campo a campo (regla 14, ERR-38);
   humo de un proceso que **escribe su JSON** (ERR-42); umbrales en un módulo único importado (ERR-31); una línea por
   puerta con su umbral al lado (ERR-89); JSON de subproceso por prefijo + sello exacto (ERR-87).
9. **Cambiar esta letra** exige ERR numerado, fecha, y el cálculo del nulo que lo motiva; y no rejuzga a nadie.

---

## 3. ERR-91: por qué cambia y qué NO se rejuzga

**ERR-91 — el criterio v2 nunca corrió su propio control negativo, y su cláusula central está calibrada sobre la
hipótesis nula: rechaza al propio tronco.**

La cláusula `A₁₂ ≥ 0.50` de T-A es, tal como la calcula el runner, una **prueba de signo pareada**: bajo "el candidato ES
el tronco" su distribución es Bin(n, 0.5)/n y el umbral está exactamente en la media del nulo. Eso no es falta de
potencia: es un defecto de forma que **no mejora con más semillas**.

El número que cierra el asunto no es un modelo: son **corridas reales del tronco**. Los brazos OFF de v15f-v2 (301–320) y
de dE5-v2 (2021–2040) son el mismo organismo (v14.2 con la perilla apagada), el mismo mundo `corre_vivo_rep2`, el mismo T
y el mismo runner: dos muestras de la misma ley (verificado: `A₁₂` no pareado 0.511 / 0.534 / 0.554; medianas de `r` −71.5
contra −73.0). Repartiendo esas **40 semillas reales** al azar en dos brazos de 20 —un **placebo perfecto**, el tronco
disfrazado de candidato— y aplicando la letra v2 completa (creador A, `experimentos/junta_20260921/A/analiza_potencia_Q1.py`):

```
VIVO        muertes<=1.10x 0.993   r>=tronco-10 0.985   A12>=0.50 0.567   brazo entero 0.567
CUELLO_MIN  muertes<=1.10x 0.951   r>=tronco-10 0.954   A12>=0.50 0.561   brazo entero 0.558
>>> T-A ENTERA sobre el placebo perfecto:  PASA 0.316   (CAE 0.684)
>>> sin la cláusula A12 (sólo las dos medianas declaradas): PASA 0.909
>>> T-A y T-C (ii) juntas:  PASA ~ 0.006
```

**El tronco, presentado como candidato, no entraría al tronco: probabilidad 0.6 %.** Las dos medianas que el criterio ya
declaraba (muertes ≤ 1.10×, `r ≥ tronco − 10`) pasan 0.909: **el problema era la cláusula añadida, no el margen**. Y la
cláusula era **más dura que el margen escrito en su mismo renglón**: T-A dice tolerar Δr = −10, pero `A₁₂ ≥ 0.50` sólo
deja pasar con probabilidad 0.80 a partir de Δr ≥ +2.5 y sólo rechaza con 0.80 por debajo de Δr ≤ −4.5.

T-C (ii) es el otro caso: `A₁₂ ≥ 0.75` con n = 20 es una **puerta de capacidad** (exige ganar en el 80 % de las semillas;
con el ruido real de `rev` eso son +21 a +23 puntos sobre una mediana de 37–45, ~+50 %) escondida en una puerta que se
llama *"se desdice"* y cuya forma de no regresión ya la cubre T-C (i).

**Los tres creadores de la junta del 21-sep votaron lo mismo** desde tres líneas distintas: A (matemática: no inferioridad
con el margen ya declarado, capacidad sólo en T-G, toda tasa balanceada), B (representación: la puerta es una moneda para
lo inerte; la capacidad vive sólo en T-G) y C (sistemas vivos: T-C (ii) se mueve a T-G; cobrar la capacidad dos veces
produjo tres rechazos por ruido).

**Qué NO se rejuzga, explícitamente.** v15f **no entra** (cayó T-A, T-C, T-D, T-E). dE5 **no entra** (cayó T-A, T-C ii,
T-E, T-G). v15c, v15d, v15e, v15g **no entran**. BA y BA-v **no cumplen la letra**. B-5 entró como v14.2 y ahí sigue.
Nada de eso cambia, y ninguno vuelve a medirse bajo v3: v3 rige **sólo para candidatos futuros, con semillas nuevas**. La
razón por la que esto no es recalibrar tras ver datos (regla 3) es que la justificación **no depende de qué candidato
cayó**: es el cálculo del nulo, el tronco contra sí mismo.

**Lo que este documento todavía debe:** su propia calibración corrida. El bloque **A-CAL**
(`experimentos/criterio_v3/PREREGISTRO_calibracion_v3.md`) mide, con el PLACEBO real (perilla que consume sorteos) y con
un brazo PEOR declarado, si v3 cumple las dos condiciones que le exigimos a cualquier criterio: **deja pasar al placebo
con probabilidad ≥ 0.90 y rechaza al que es peor que el margen con probabilidad ≥ 0.95**. Si no las cumple, v3 se retira y
se escribe v4 con su ERR.

Coordinador / creador A-CAL, 21 sep 2026.
