# Etapa 5, nivel N1 — señal innata honesta y aprendizaje vicario entre dos organismos v9

**Escrito ANTES de probar el instrumento y ANTES de correr. 16 sep 2026, día 4.**

- **Dirección:** Christiam Puentes ("cómo hago para que este ser comience a comunicarse a los otros y los otros
  puedan aprender de manera simbiótica… corre el resto").
- **Diseño completo:** `DISENO_comunicacion_simbiotica.md` (misma carpeta).

## 0. Qué se sabe y qué se declara

- **Sin datos previos de dos organismos v9 en el mismo mundo.** Lo único parecido es del día 1 (población con pesos
  compartidos), y no aplica.
- **Hoy se midió que morder veneno renueva el mundo.** Dos organismos compartiendo objetos cambian la ecología por el
  mero hecho de ser dos. Por eso el control principal es **N0 (dos organismos sin señal)**, no el organismo solo.
- **La Etapa 4 no está cerrada:** v9 olvida lo que no re-muestrea. N1 no depende de eso, porque todo pasa en un
  mismo mundo continuo, pero se deja dicho.
- **El instrumento `mundo_social.py` se escribió antes de este preregistro y no se ha ejecutado.**

## 1. Instrumento

`mundo_social.py`: N organismos v9 que comparten los objetos, con un RNG por organismo y otro del mundo.
- **Recursos por cabeza:** 4 objetos por organismo.
- **Señal N1:** al morder, placer (+) o asco (−) según el resultado.
  - Recibe todo organismo a distancia ≤ 5 en el anillo.
  - El receptor actualiza **su propio** valor del patrón mordido con Rescorla-Wagner vicario: tasa `eta/3`, escala
    innata + → +1 y − → −3, con drenaje, sin comer y sin divisiones.
  - Nunca se transmiten pesos ni códigos.
- **`senal='barajada'`:** el mismo número de señales, con el signo al azar (RNG propio).

## 2. Diseño

20 semillas (1..20), T = 100.000, dos mundos: **E1** (A comida, B veneno) y **E2** (inversión en t = 50.000).

| condición | organismos | señal | papel |
|---|---|---|---|
| SOLO | 1 | — | referencia |
| **N0** | 2 | ninguna | **control ecológico** |
| **N1** | 2 | honesta | **la pregunta** |
| BAR | 2 | barajada | **control de contenido** |

**Métricas por organismo** (pareadas por semilla y por organismo, frente a N0):
- **veneno propio hasta el criterio:** mordidas propias de B (E1) hasta que su `W_B ≤ −2.5`;
- veneno en Q1;
- muertes;
- en E2, `t_ext_B`: primer paso tras la inversión con `W_B ≥ 0`;
- señales emitidas y recibidas.

## 3. Criterios y predicciones

**K [instrumento]. Si falla, no se lee nada más.**
- **K1:** `mundo_social.run(s, n=1)` ≡ `organismo_v9.run(s)` en `W`, `comp`, `mord`, `vis`, `deaths`, `splits`,
  `split_t` y `celdas`, en E1 y E2 × semillas 1..3.
- **K2:** en N0, 0 señales recibidas; en N1 y BAR, > 0 en 20/20.
- **K3:** en BAR, el número de señales recibidas por semilla es del mismo orden que en N1: la mediana de BAR está
  dentro de ±50% de la de N1. El control compara contenido, no cantidad.

**Predicciones (E1):**
- **S1 [aprende del asco del otro]:** mediana del veneno propio hasta el criterio, por organismo, en N1 ≤ **0.7 ×**
  la de N0.
- **S2 [simbiosis: ganan los dos]:** en ≥ **15/20** semillas, **los dos** organismos de N1 muerden menos veneno
  propio hasta el criterio que su par en N0 (misma semilla, mismo índice). "Menor o igual" cuenta como no-mejora.
- **S3 [es el contenido, no la cantidad]:** mediana del veneno propio hasta el criterio en BAR ≥ la de N0. La señal
  sin información no ayuda, y probablemente estorba.

**Predicciones (E2, sin voto para el cierre de N1, porque hay más incertidumbre):**
- **S4:** mediana de `t_ext_B` (por organismo) en N1 < la de N0. Basta con que uno pruebe B, ahora comida, para que
  el otro lo sepa.

**Descriptivo:**
- muertes por condición;
- SOLO frente a N0: el efecto ecológico de ser dos;
- veneno en Q1.

## 4. ¿Qué lo haría pasar por la razón equivocada? Respondido antes de correr

| riesgo | cómo se controla |
|---|---|
| Ser dos cambia la ecología y eso baja el veneno | N0 como línea base, no SOLO |
| Recibir cualquier actualización acelera "algo" | BAR, con el mismo número de señales |
| El beneficio es sólo de uno (parasitismo) | S2 exige que ganen **los dos** |
| El criterio se alcanza por la vía vicaria sin haber aprendido nada propio | "veneno propio hasta el criterio" cuenta las mordidas que le cuestan al organismo; si llega al criterio con menos, **eso es** el beneficio. Además se reporta `W_B` final y el veneno en Q1 como conducta |
| Identidad del instrumento | K1 exige bit a bit v9 con un solo organismo |

## 5. Qué se decide

- **K, S1, S2 y S3 sostenidas:** **N1 queda demostrado.**
  - Dos organismos v9 con una señal innata honesta **aprenden cada uno del asco del otro**, con beneficio para los dos
    y dependiente del contenido de la señal.
  - Vocabulario (regla 8): *"transmisión social de valor por una señal innata"*. **No** "lenguaje", **no**
    "entienden".
  - Siguiente: N2, el significado aprendido.
- **Falla S1 o S3:** N1 no se sostiene. Se registra y se diagnostica: alcance de la señal, tasa vicaria, ecología.
  **No se recalibran** `d_senal` ni `f_vicaria` (regla 3); un cambio va con preregistro nuevo.
- **S1 sostenida pero S2 no:** hay transmisión, pero no es simbiótica. Se registra como tal.
