# PREREGISTRO — CUELLO A: sufijo local de variante en la tabla de pares

**Misión (primero, siempre):** llegar a la AGI por este camino: un organismo mínimo de reglas locales, sin backpropagación ni supervisor global, que aprende, desaprende, generaliza, sobrevive, se comunica y se reproduce con evidencia preregistrada.

**Fecha:** 2026-09-18. **Creador externo:** Codex. **Estado:** escrito antes de cualquier medida de este instrumento. Este es un único experimento del cuello A; no modifica reproducción, metabolismo, emisor, canal, mundo ni la regla de aprendizaje.

## 1. Antecedente y pregunta

En BLOQUE 4/4b, el receptor muerde en la primera exposición la comida que evitaba cuando recibe el mensaje, pero el patrón de una hermana conserva casi el mismo efecto (`BAR-H` 12–18/20) y otro token conserva una parte (`BAR-T` 6–9/20). La tabla v15f/b4b se lee por una celda ganadora y una casilla de un par de píxeles: dos bits. Las hermanas sólo difieren en los píxeles 9–11, que el 100 % de las celdas de forma ignoran.

El BLOQUE 5 de varias ganadoras no aporta evidencia conductual: ambos rangos 681–700 y 701–720 se detuvieron en la guarda de identidad antes de ejecutar brazos; los logs terminan en `IDENTIDAD 26/27` por un control de no-vacuidad sin entrega en una semilla. No se repite `k_ganadoras`.

**Pregunta:** ¿una dirección local que concatena la firma visible de variante a la casilla del par evita que la recompensa de un mensaje para `sal rosa` cambie la boca ante `sal` o ante la hermana de `sal rosa`?

## 2. Hipótesis y mecanismo único

**H-A-SV.** Cuando `memoria_variante=1`, cada celda de pares conserva exactamente la misma regla local de sobrescritura de R cruda, pero escribe y lee en:

`(par de píxeles, bin del par, firma de los últimos fam_nvar píxeles)`.

Con `fam_nvar=3`, una casilla de cuatro pasa a ocho subcasillas locales. La firma se calcula de la retina presente, sin estado compartido, gradiente, supervisor, azar nuevo ni señal adicional. El emisor, el canal, la selección de la ganadora, la regla de error y la boca no cambian. Es una sola modificación: la dirección de memoria de la tabla.

**Perilla:** `memoria_variante=0` por defecto. Apagada, la dirección vuelve literalmente al bin de dos píxeles y debe ser bit a bit idéntica a `organismo_familias_b4b.py`, sin consumo adicional del RNG.

## 3. Brazos, controles y semillas

Mundo, emisor voraz (`voraz=1.0`), señalamiento, dirección negativa y letra de BLOQUE 4b se importan de `corre_familias_b4b.py`; no se copian.

| brazo | receptor | función |
|---|---|---|
| `CANAL` | patrón real de `T1v2` + R cruda | referencia correcta |
| `CORTADO` | gemelo mudo | control apagado de mensaje |
| `BAR-H` | patrón `T1v0` + misma R | hermana, control que decide variante |
| `BAR-T` | patrón `T3v2` + misma R | otro token, control que decide token |
| `VALOR` | patrón de ceros + misma R | valor sin referente |
| `PAR` / `PAR0` | receptor ve `T1v2` y `T1v0`, con / sin mensaje | especificidad conductual entre hermanas |

El emisor se ejecuta con `memoria_variante=0`: es exactamente b4b y no se confunde habla con lectura. Los receptores de los seis brazos activos usan `memoria_variante=1`.

- Humo del creador: semillas **1–3**, un proceso, `T=60 000`; no es evidencia ni cambia umbrales.
- Serie del coordinador: **721–740**; réplica nueva **741–760**, `T=100 000`. El creador no las ejecuta.
- Coste previsto de una serie: 20 emisores + 7 receptores por semilla = 160 corridas de 100 000 pasos, más identidad. El runner entregado es secuencial y no contiene `multiprocessing.Pool`.

## 4. Medidas y análisis

Todo veredicto usa conducta de la boca, nunca pesos, tablas o ganadoras:

- `com`: mordió (`1`) o no (`0`) en la primera exposición de su vida a `T1v2` después de la entrega. En esta dirección, `T1v2` es comida que el receptor evita sin mensaje.
- `dist`: en `PAR`, la boca trató distinto a `T1v2` y `T1v0` en sus primeras exposiciones posteriores a la entrega.
- exposiciones hasta asociar y muertes se guardan al lado como coste; no sustituyen `com`.

El análisis de cada serie será pareado por semilla: A12 de `CANAL > CORTADO`, `BAR-H <= CORTADO`, y `BAR-T <= CORTADO`; se reportan medianas y cuartiles de exposiciones y muertes, sin máximos. Las semillas sin mensaje se excluyen de los conteos pareados y se informan por separado. Las puertas de montaje se leen antes del resultado: emisor con mensaje, prefijo gemelo, primera exposición en la entrega y vía lenta.

## 5. Predicciones numéricas y umbrales fijos

Los siguientes umbrales son para **cada** una de las dos series de 20; no se recalibran con el humo.

| predicción | pasa | me refuta |
|---|---:|---:|
| Canal llega y sigue siendo útil | `CANAL >= 15/20`, `CORTADO <= 5/20`, A12 pareado `>= 0.70` | cualquiera de los tres cae |
| Referencia contra otro token | `BAR-T <= CORTADO + 3` | `BAR-T > CORTADO + 3` |
| Referencia contra hermana — la prueba principal | `BAR-H <= CORTADO + 5` | `BAR-H > CORTADO + 5` |
| Referente necesario | `VALOR <= CORTADO + 3` | `VALOR > CORTADO + 3` |
| Dos variantes tras el mensaje | `dist(PAR) >= 12/20` y `dist(PAR) >= dist(PAR0) + 5` | cualquiera de las dos cae |
| Coste | mediana de muertes `CANAL <= 1.50 x CORTADO` | la razón excede 1.50 |

**Predicción central:** `CANAL` 15–19/20, `CORTADO` 0–3/20, `BAR-T` 0–5/20, `BAR-H` 0–6/20 y `VALOR` 0–3/20. Espero que el sufijo de variante corte ambos barajados sin bajar el canal, porque el mensaje se escribe en la firma de `T1v2`, mientras `T1v0` y `T3v2` apuntan a direcciones distintas.

## 6. Controles de identidad y detención

`identidad_cuelloA_sufijo_variante.py` prueba al menos 24 escenarios por 3 semillas con la perilla apagada, incluyendo AB, familias, b2, emisor, receptor, los tres modos de canal, voraz, `par_herm`, B-5 y relevo. Exige identidad de todas las claves heredadas y por tanto comprueba también que el RNG no se consumió. Además contiene cuatro controles que **deben** diferir o lanzar; si alguno no lo hace, el arnés falla por vacuidad.

El experimento se detiene si la identidad no es 72/72, si una puerta de montaje cae, o si una de las predicciones de seguridad/coste cae. Un ajuste posterior de umbral, brazo, mecanismo o criterio requerirá un nuevo preregistro, semillas nuevas y `ERR-70` o posterior, con fecha y motivo. No hay corrección registrada al escribir este documento.

## 7. Declaración permitida y límites

Si las dos series pasan todas las puertas y los umbrales, se podrá decir únicamente: *un mensaje con patrón y recompensa cambió la conducta de la boca sin experiencia propia, y esa conducta fue específica frente a una hermana y otro token en este mundo.*

No permitiría declarar lenguaje, comprensión, concepto, evolución, ni AGI.

