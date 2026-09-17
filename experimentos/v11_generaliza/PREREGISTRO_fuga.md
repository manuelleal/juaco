# "Generalización = interferencia": confirmación del diagnóstico en 20 semillas

**Escrito ANTES de correr. 17 sep 2026, día 5.** Dirección: *"Confirma el diagnóstico en 20 semillas, preregistrado…
'Generalización = interferencia' entra al HANDOFF sólo con eso"*.

## 0. Qué se afirma y qué se sabe

Tras la re-verificación (`v11_generaliza_20260917_151145`), v11 generaliza al nivel del azar (0.60 frente a 0.80 de
v9 y v10) y la explicación **post-hoc, sobre 5 semillas**, fue: en v9 las celdas **hijas** se cuelan en el código de
patrones que nunca las entrenaron (1.00 de 3 celdas en los patrones de test), y esa **fuga** transporta el valor
aprendido; en v11, con la hija ciega fuera de su patrón, la fuga cae a 0.07 y con ella la generalización.

**Eso es una hipótesis, no un resultado.** Aquí se confirma —o se refuta— en las 20 semillas, con criterios escritos
antes. Mundo, instrumento y semillas son los mismos de la re-verificación (`organismo_v11g` `6c6b5eecc177c181`, regla
`px0`, T = 200.000, semillas 41–60, tres brazos con el mismo instrumento).

**Nota de contaminación:** los datos de 5 semillas (41–45) ya se vieron, y de ahí salió la hipótesis. Se declara. Las
15 restantes (46–60) no se han mirado para esto; el criterio D4 las separa para que haya al menos una prueba limpia.

## 1. Medidas (definidas antes)

Por corrida, en la sonda a priori (`t = T/2`, antes de que existan los patrones de test):
- **`fuga`** = media sobre los 10 patrones de test de (número de celdas con índice ≥ 30 en su código) / 3.
  Una celda con índice ≥ 30 nació de una división: es **hija**, y en un patrón de test es **ajena** por construcción,
  porque ese patrón no existía cuando nació.
- **`acc`** = acierto de signo del valor a priori sobre los patrones de test (media balanceada; la misma de G1).
- Sin voto: `|W|` a priori mediana, celdas compartidas con el entrenamiento, divisiones, celdas activas.

## 2. Criterios y predicciones

- **D1 [réplica del descriptivo]:** mediana de `fuga` en v9 ≥ **0.8**, y en v11 ≤ **0.3**. *Predicción: ≈1.0 y ≈0.1.*
- **D2 [la afirmación, entre brazos]:** Spearman entre `fuga` y `acc` sobre las **60** corridas (3 brazos × 20
  semillas) ≥ **+0.5**. *Predicción: +0.6 a +0.8.*
- **D3 [la afirmación, DENTRO de un brazo, sin el brazo como confusor]:** en v9, Spearman entre `fuga` y `acc` sobre
  sus 20 semillas ≥ **+0.3**. *Predicción: se sostiene; es el criterio que más puede fallar, porque dentro de v9 la
  fuga varía poco.*
- **D4 [limpieza]:** D1 y D2 se sostienen también restringidos a las semillas **46–60**, que no se han mirado.
- **Refutación:** si D2 < 0.5, o D1 falla, la frase "la generalización de v9 era su interferencia" **no entra al
  HANDOFF** y se registra como hipótesis no confirmada. Si D2 pasa y D3 no, entra **con la salvedad explícita** de que
  la relación está demostrada **entre** arquitecturas y no **dentro** de una.

## 3. Qué NO prueba

No prueba causalidad dentro de un mismo organismo (para eso haría falta manipular la fuga y medir, que es justamente
lo que hará v12 con la ceguera graduada). Prueba que la fuga y la generalización van juntas donde se puede medir.
