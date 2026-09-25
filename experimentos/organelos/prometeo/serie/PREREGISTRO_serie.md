# EXPLORATORIO, no es dato (hasta que corran la serie y la réplica con este texto congelado)

# PREREGISTRO — PROMETEO SERIE: ¿los órganos que la cinta se arma sola se fijan POR ENCIMA DE LO NEUTRO?

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).
Creador: Opus, equipo organelos. Fecha: 25-sep-2026. Viene de `../INFORME_PROMETEO.md` §6 (exploración con semillas 30001–30008).
Instrumento: `motor_serie.py`, `corre_serie.py` y el arnés `identidad_serie.py`. La letra está escrita en código en `corre_serie.veredicto()`.

## 1. Preguntas
- **P1 (la que manda).** Un órgano ARMADO (ausente de la cinta inicial) que la cinta se construye sola, ¿se fija en el banco (≥ 50 % en el corte **y** al final) más de lo que se fija un órgano igual de armado pero **mudo**?
- **P2 (aparte).** En PROMETEO, ¿el mundo estacional (`onda8k`) hace más frecuente el **despegue** que el mundo quieto? Despegue = ≥ 1 000 nacimientos solos tras el corte. En la exploración, s30003 hizo 2 677 y la siguiente corrida más alta hizo 611.

## 2. Diseño
- **Mundos:** `quieto` y `onda8k` (coseno de período 8 000, desde t 8 000), de `fable_mundos.py`.
- **TL:** T 60 000, corte 44 000, margen 4 000, igual que la exploración. w30, banco 200, vivero hasta el corte y después solos.
- **Cuerpo:** FAMB_GRAM_ECO desde filtra0 con G0, cinta v0 (`CD.compila()`). La SOS no se lee. El alfabeto al azar lleva el kit (CABLE, HGT).
- **Brazos (los dos con el mismo alfabeto, la misma copia y la misma HGT):**
  - `PROMETEO`: los órganos armados **actúan**. Los CABLE mueven boca, patas o parto, y los slots de transmisión se expresan.
  - `MUDO`: el **control neutro**. La cinta arma los mismos órganos por las mismas vías (errores, duplicación, HGT), pero **no actúan**:
    - el cuerpo no lee los CABLE;
    - el órgano de transmisión expresado es siempre FILTRA0, diga lo que diga la cinta.
    Lo que se fija en MUDO se fija por deriva o por arrastre de otros genes. Es el nulo exacto de P1, pareado por semilla.
- **Controles que propuse y NO entran, con el porqué:**
  - **AZAR** (donante al azar). Mide variación sin ninguna selección. MUDO es un nulo más duro: quita la selección solo sobre el órgano y deja la de todo lo demás, arrastre incluido. Para P1 sobra.
  - **SIN_HGT** y **VIVERO_POR_LINAJE**. Responden si la HGT ayuda, que no es la pregunta de hoy. La HGT está igual en los dos brazos, así que no confunde P1.
  - Recorte declarado por costo: 2 brazos en vez de 5.
- **Semillas:** serie 30101–30120, réplica 30121–30140, humo 30190, arnés 30191. Todas nuevas y del rango 30101–30199.
- **Medida por corrida:** `F` = el máximo, sobre los órganos FUNCIONALES armados, del mínimo entre (fracción del banco en el corte, fracción del banco final).
  - **Órgano funcional:** cable a boca o patas con peso ≠ 0; cable a parto con algún peso < 0; slot de transmisión con cuando ≠ nunca y distinto de filtra0.
  - La instrucción HGT **no** es un órgano: es el mecanismo de variación.
  - **Fijado** = F ≥ 0.5. `F_inerte` (cables de parto sin peso negativo y slots "nunca") es descriptivo.

## 3. Arnés `identidad_serie.py`
N/N: el 8/8 de antes, ahora contra `motor_serie`, más lo nuevo.
- **Heredado:** S1 y S2 bit a bit contra `motor_fable`; S3 == `motor_prometeo` con kit, copia ON, cable y slot; S4–S8 las piezas del kit.
- **El control MUDO:**
  - M1, M2 y M3: MUDO con un cable de parto, un cable de boca o un slot nuevo da **la misma dinámica bit a bit** que la cinta sin ellos. El mismo slot en PROMETEO sí la cambia.
  - M4: la HGT sigue actuando en MUDO.
  - M5: MUDO arma órganos en el banco y el órgano expresado de todos los vivos es FILTRA0.
- **Reanudar:** R1 reanuda desde el checkpoint y da lo mismo que correr de un tirón, con el rng del kit dentro del checkpoint.
  Es un cambio del instrumento declarado: en la exploración ese rng no se guardaba. Allí no hubo reanudaciones, así que no afecta a esos datos.
- **Lectura y banderas:** L1 lee las claves de los órganos; L2 prueba cada rama de la letra; B1 prueba que las banderas malas abortan sin escribir nada (ERR-115).
- **M6 (ERR-144):** en MUDO, el suministro se lee en la cinta: de novo > 0, y la columna vieja, la del órgano expresado, da 0.
- **Resultado: 18/18** (`identidad_serie_salida.txt`, corrido después de ERR-144).

## 4. La letra (por ventana; el bloque exige que serie y réplica den el MISMO veredicto)
- **Instrumento, en orden** (si falla, **NO EVALUABLE**):
  1. ventana completa, con 20 semillas × 2 brazos × 2 mundos;
  2. sin corridas abortadas;
  3. bloqueados = 0;
  4. en MUDO, los contadores del kit (boca, patas, veto) valen 0 en todas las corridas.
- **GUARDIA DE SUMINISTRO, el control que PUEDE fallar** (redefinida por ERR-144, §7). Se mide en la **cinta**, no en el órgano expresado: es la media de la fracción de nacidos antes de t 8 000 con un órgano armado **de novo** (uno que la cinta de su donante no tenía), PROMETEO dividido por MUDO. Debe caer en [0.5, 2] en cada mundo.
  La misma tasa sobre el vivero entero es descriptiva.
  Si cae fuera, los dos brazos no recibieron la misma oferta de órganos y P1 no se puede leer: **NO EVALUABLE**.
- **P1 por mundo:** hace falta que se cumplan las dos:
  - F(PROMETEO) > F(MUDO) pareado por semilla en **≥ 14/20**;
  - #fijados(PROMETEO) − #fijados(MUDO) **≥ 4**.
- **Veredicto:**
  - **FUNCIONA:** P1 en los dos mundos;
  - **HAY ALGO MODESTO:** P1 en un solo mundo;
  - **NO:** P1 en ninguno.
- **P2, aparte:** despegues de PROMETEO en onda8k ≥ despegues en quieto + 3. SÍ o NO por ventana.
- **Descriptivo** (no decide):
  - qué órganos se fijan y en cuántas semillas;
  - su clase: ensena, variante de filtra0, lee su estado tipo O3, o nuevo;
  - nacimientos solos tras el corte, persistencia, HGT en el banco y largo de la cinta.
- **Sobre la potencia:** con n = 20, "≥ 14/20" pasa por azar con p ≈ 0.058 si los dos brazos son intercambiables.

## 5. Predicciones (firmadas antes del humo)
Referencia de la exploración (8 semillas; no es dato): PROMETEO fijó algún órgano funcional en unas 3/8 semillas por mundo, y lo inerte se fijó en 1–2/8.
En MUDO **todo** el suministro es neutro, unas 4 veces lo inerte, así que espero una tasa de fijación neutra parecida a la de PROMETEO. Deriva fuerte: el banco lo dominan pocos linajes.

| cantidad (por ventana) | rango predicho | P |
|---|---|---|
| fijados PROMETEO, quieto | 4–10 / 20 | 0.7 |
| fijados MUDO, quieto | 3–10 / 20 | 0.7 |
| fijados PROMETEO, onda8k | 4–10 / 20 | 0.65 |
| fijados MUDO, onda8k | 2–9 / 20 | 0.65 |
| F(P) > F(M), pareado, en cada mundo | 9–13 / 20 | 0.6 |
| P1 se cumple en quieto | — | 0.25 |
| P1 se cumple en onda8k | — | 0.3 |
| la guardia de suministro pasa (los dos mundos) | razón 0.7–1.4 | 0.85 |
| despegues PROMETEO onda8k / quieto | 0–3 / 0–1 | 0.7 |
| P2 SÍ | — | 0.15 |
| **veredicto P1:** NO / HAY ALGO MODESTO / FUNCIONA | — | **0.55 / 0.30 / 0.15** |
| el órgano más fijado en PROMETEO es un slot de transmisión, no un cable | — | 0.8 |

## 6. Costo
- **Por ventana:** 2 mundos × 2 brazos × 20 semillas = **80 corridas**.
- **Exploración** (14 procesos en 16 núcleos: 8 míos más la serie Pool 6 de v01; es decir, con la mitad de la CPU): 271 s de media y 390 s como máximo por corrida.
- **Con Pool 6:** 80 × 271 / 6 ≈ **60 min**, y en el peor caso (390 s) ≈ **87 min**. Cabe en ≤ 2 h por ventana.
- El humo mide el costo real y se anota en el INFORME.

## 7. Cambios
Cualquier cambio después del humo se numera desde **ERR-144** (el ERR-143 ya lo usa H-PLANO w90) y se escribe aquí antes de lanzar la serie.

- **ERR-144** (Opus, 25-sep, 10:25–10:35). Ocurrió tras el humo 1 (semilla 30190, sin valor), antes de cualquier semilla de serie o réplica. Es un error de instrumento: la guardia de suministro medía mal en MUDO.
  - **(a) Qué medía mal.** La columna de `kit_nac` que usaba la guardia contaba los slots del órgano de transmisión **expresado**. En MUDO ese órgano es siempre FILTRA0, así que la columna daba 0 aunque la cinta sí armara slots. La guardia comparaba cosas distintas: salió 0.13/0.056 = 2.3 y habría dado NO EVALUABLE por un bug.
    **Arreglo:** el motor (ancla S4 de `construye_serie.py`) mide dos cosas en la **cinta**, con la misma definición que la letra (`organos_serie.py`, que sale de `corre_serie.py`):
    - si el hijo lleva un órgano armado que su donante no tenía (de novo);
    - si lleva alguno.
  - **(b) Qué ventana usa.** En el humo 2, con la medida ya arreglada, la tasa de novo sobre el vivero entero dio 0.56–0.62, PROMETEO/MUDO. La razón es que MUDO acumula copias neutras de slots ORG (el 82 % de los nacidos lleva alguno, contra el 10 % en PROMETEO), y cada copia es un blanco más para la mutación. Eso ya es un resultado de la selección, no del instrumento.
    **Arreglo:** la guardia usa la ventana temprana [0, t_cambio), donde las cintas de los dos brazos todavía son casi iguales. La del vivero entero queda descriptiva.
  - **Qué no cambió:** la dinámica es idéntica a la del humo 1 (mismos F y mismos nacimientos en la semilla 30190). Tampoco cambian la letra de P1 ni la de P2.
  - Se agregó M6 al arnés y se volvió a correr: 18/18. El humo 3 corre con todo esto.

## Nota del coordinador (25-sep, antes de la serie; auditoría juaco-auditor: LISTO CON CORRECCIONES)
- H-6: sondeo `sondeo_pool.py` con Pool(2) sobre la semilla de humo 30190 (quieto, PROMETEO y MUDO). Comparado JSON contra JSON con el humo
  de un proceso, los dos brazos son idénticos campo a campo (nac_solo 276 = 276, r0_final 0.9783 = 0.9783, `prometeo` y `cambio`
  iguales). El monkeypatch llega a los hijos de Pool en Windows. La primera comparación del script decía "FALLA" por comparar tuplas en
  memoria contra listas del JSON; es un fallo del sondeo, no del runner. No es ERR.
- H-2: la cláusula `nfP − nfM ≥ 4` no trae un nulo propio. Como sólo endurece el criterio (baja el falso FUNCIONA por debajo de 0.058),
  se deja como está y se declara aquí. No es ERR.
- Arnés re-corrido por el coordinador: 17/17 (--sin_b1) + 1/1 (--solo_b1).
