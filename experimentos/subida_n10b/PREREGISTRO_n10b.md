# PREREGISTRO n10b: la familia pasa su TABLA en vida (niveles 10–13, tanda 2)

**Misión:** llegar a la AGI por este camino.
**Autor:** creador de la tanda 2 del nivel 10, 23-sep-2026. Escrito DESPUÉS del arnés (42/42) y del diagnóstico del mensaje, y ANTES del humo y de cualquier serie. Si algo cambia después del humo: "candidato a ERR".
**No apunta al tronco.** No toca archivos congelados. De `generaciones/`, `carrera_escuderias/` y `subida_n10/` sólo se importa o se lee, con sha fijado.

## 0. De dónde sale (datos de la tanda 1, serie 12301–12320, que NO SE LEE como veredicto)
- NADA 0.110 · PARTO 0.158 · BAR 0.139 · ORÁCULO 0.553 (mediana de `R0_nacidos`). PARTO > BAR sólo 11/20. ORÁCULO > NADA 20/20.
- **Lectura:** el mundo sí tiene dónde usar contenido (el ORÁCULO multiplica por 5 el piso). Lo que no tenía contenido era el mensaje.
- **Diagnóstico** (`diagnostico_mensaje.py`, práctica 12392, T = 20000, un proceso; JSON en `datos/humo/diag_mensaje_parto_s12392_T20000.json`):
  - sólo el **4 %** de las entradas del mensaje de PARTO llevan R < 0;
  - el **47 %** de los mensajes no trae ninguna R < 0 propia;
  - el grueso es A|hambre +1 (740 de 1887) y C|hambre 0 (656).
  - Barajar R que casi todas valen lo mismo no cambia nada, y por eso PARTO ≈ BAR.
- **Los hijos mueren por lo que el padre sabe:** en la tanda 1, el 100 % de los nacidos de NADA murió por veneno o sal (`frac_mala_nacidos` 1.0), con una vida mediana de 95 pasos. Un hijo con dote 0.6 muere con dos mordidas de B (−0.4 cada una), así que no alcanza a aprenderlo solo a tiempo. Esa es la información que el padre tiene y el hijo no puede conseguir a tiempo. No hace falta otro mundo: hace falta que el mensaje la lleve.

## 1. Hipótesis
**H-n10b:** si el padre vivo pasa en el parto **su tabla** (lo que vivió y heredó, resumido por letra y necesidad), los nacidos tienen más hijos:
- que sin mensaje;
- **que con la misma tabla barajada** (el contenido importa);
- compitiendo por el mismo flujo de recurso.

**Hipótesis secundaria (familia, F-5):** la tabla de la familia (vivida más heredada) gana a la tabla de lo que vivió sólo el padre, porque la familia acumula claves que ningún cuerpo solo alcanza a vivir.

Se predice que la familia no llega a sostenerse: el techo del ORÁCULO (0.553) está lejos de 0.9, así que H-1 sigue en pie.

## 2. Mecanismo mínimo (memoria nueva: CERO; constantes nuevas: CERO)
- **`al_parir` (modo `res`):** el padre arma una entrada por (letra, necesidad).
  - Toma la R **más reciente que vivió** en toda su vida (`self._mordh`, que ya existe y guarda las mordidas de la vida del cuerpo).
  - Para las claves que no vivió, usa la que **heredó** (`self._nodo`).
  - Son a lo sumo 8 entradas (4 letras × 2 necesidades), en el orden del ORÁCULO (necesidad, letra).
  - Es menos memoria que el mensaje de la tanda 1 (20 o más entradas).
- **`nace`:** el hijo instala la tabla como nodo en `NODO_LEE` copias. Es la misma dosis y la misma lectura de F9 (relevancia viva, vía lenta) que el ORÁCULO de la tanda 1. La lectura no se toca.
- **Acumulación:** el hijo la vuelve a pasar enriquecida con lo suyo, así que la tabla se acumula por generaciones.
- **Fundadores:** limpios (ENMIENDA 5, sin cambios).

| carro | MODO | papel |
|---|---|---|
| `FAMB_NADA` | nada | piso; == FABRICA == FAMILIA_NADA de la tanda 1, bit a bit |
| `FAMB_RES` | res | **candidato** |
| `FAMB_RES1` | res1 | tabla de lo vivido por el padre, sin lo heredado. Separa "la familia acumula" de "el padre sabe" |
| `FAMB_BAR` | bar | **control de contenido que puede ganar**. Es la tabla de RES con las R permutadas entre sus entradas en cada parto: mismas claves, misma multiset de R, misma dosis. El rng es propio (`[860000] + entropía de rng_hijo`) y no consume ningún rng (arnés B2). En la familia BAR, lo heredado es lo barajado. |
| `FAMB_ORACULO` | oraculo | techo; == FAMILIA_ORACULO de la tanda 1 en toda la salida (arnés O) |

## 3. Instrumento, anclas y calibración declarada (ERR-116)
- **Construcción:** `construye_familia_b.py`, 6 anclas sobre `carrera_escuderias/carros/FABRICA.py` (`2ebee3e99ea5a33a`).
- **Carros:**

  | carro | sha |
  |---|---|
  | NADA | `6635a04063fe7317` |
  | RES | `2addb7ca5b9d031d` |
  | RES1 | `766807733fb620e2` |
  | BAR | `dfcb2efbf5ec8d2b` |
  | ORÁCULO | `c1ee88844650a78e` |

- **Mundo:** idéntico al de la tanda 1: `pista2.py` `4d2bee16e7961261`, `motor_convive.py` `d10cb9021f5d0f41`, `solapadas=1`, `reposicion='fija'`, `r_rep = 0.03`, tope 300, T = 100000.
- **Juez:** `resumen_linaje` de `corre_convive.py` `e6dadfdad9c379cd` (importado).
- **Arnés `identidad_familia_b.py` (`070e6524f79e3cc4`): 42/42**, salida en `identidad_familia_b_salida.txt`:
  - (I) NADA == FABRICA en 6 configuraciones (v1 y v2) y NADA == FAMILIA_NADA (tanda 1).
  - (O) ORÁCULO == FAMILIA_ORACULO (tanda 1) en toda la salida, con partos, 2 semillas.
  - (P) antes del primer parto, los 5 modos son idénticos.
  - (B) el canal por unidad, incluida **B3: RES con la tabla completa == ORÁCULO** (mismo nodo, misma vía lenta). RES sólo difiere del techo en lo que la familia no vivió.
  - (D) determinismo.
  - (C) en marcha.
  - (R) el runner aborta ante 13 formas de bandera mala y semillas fuera de rango; un subproceso con bandera desconocida sale con código 1 sin escribir nada.
- **Calibración de las anclas sobre la serie 12301–12320 (declarada, ERR-116):**
  - **Por qué vale:** por (I) y (O), los brazos NADA y ORÁCULO de este instrumento son los mismos programas que en esa serie, en el mismo mundo.
  - **Cómo se calcula:** el ancla es el intervalo de predicción al 99 % de la **mediana de 20 semillas nuevas**. Es un bootstrap de dos muestras (200 000 réplicas, rng 20260923) sobre los 20 valores por semilla de la serie, redondeado hacia afuera.
  - **NADA:** valores de 0.060 a 0.170, mediana 0.110, desviación típica 0.028 → **[0.085, 0.135]** (IP95: [0.092, 0.127]).
  - **ORÁCULO:** valores de 0.454 a 0.639, mediana 0.553, desviación típica 0.051 → **[0.49, 0.62]** (IP95: [0.503, 0.604]).
  - **Por qué 99 % y no 95 %:** son dos anclas en conjunción; con 95 % cada una, la probabilidad de tumbar por azar un instrumento sano sería de ~10 %.
  - No se mueve ningún umbral de la tanda 1 después de verlo: se declara un ancla **nueva**, para semillas **nuevas**, antes de correrlas.

## 4. Semillas NUEVAS
Verificadas con grep en `bundle` y en los worktrees `anclado`, `aprende`, `carrera`, `convive`, `criterio`, `escuela`, `exploracion`, `fanin`, `respaldo` y `sandbox`. Sólo aparecen como PID en logs viejos o como valores de columnas en CSV y JSON de datos; ningún `SEMILLAS`, preregistro ni runner las usa.
- Práctica: **12791–12799** (arnés: 12791–12793; humo: 12791).
- **Serie: 12701–12720.**
- **Réplica: 12721–12740.**

`corre_n10b.valida_semillas` rechaza cualquier otro rango (arnés R).

## 5. Medidas
**Medida que decide:** `R0_nacidos` = hijos por cuerpo nacido (no fundador) de la cohorte t ≤ T/2. Es la misma definición que en la tanda 1, pareada por semilla.

**Secundarias:**
- `vida_nacidos`, `exceso`, `nac`, `gen_max`, `persiste_carro`, causas.
- **Brecha:** mediana por semilla de (RES − NADA) / (ORÁCULO − NADA).
- **Telemetría del carro** (informa, no decide; ERR-96): claves de la tabla instalada; fracción de tablas con B|hambre = −3, D|sed = −3, y A o C marcadas malas (esto último sólo es posible en BAR).

## 6. Criterio por la letra (umbral pareado ≥ 15/20; implementado en `corre_n10b.veredicto`)
**Validez:**
- **V-ANCLA-b:** mediana de `R0_nacidos` de NADA en [0.085, 0.135] y NADA `persiste_carro` ≤ 5/20. Si cae: **NO SE LEE**.
- **V-TECHO-b:** mediana de ORÁCULO en [0.49, 0.62] y ORÁCULO > NADA ≥ 15/20. Si cae: **NO SE LEE COMO CAPACIDAD**.

**Puertas:**

| puerta | condición |
|---|---|
| F-1 | RES > NADA ≥ 15/20 |
| F-2 | RES > BAR ≥ 15/20 |
| F-3 | MIX (3 NADA + 3 RES + 3 BAR en el mismo mundo): RES > NADA ≥ 15/20 |
| F-4 | MIX: RES > BAR ≥ 15/20 |
| F-5 (calificador ACUMULA) | RES > RES1 ≥ 15/20 |

**Veredicto:**

| veredicto | condición |
|---|---|
| **FUNCIONA** | F-1..F-4. Con F-5: **FUNCIONA + ACUMULA** |
| **HAY ALGO MODESTO** | F-1 y F-2. Con F-5: **+ ACUMULA** |
| **HAY ALGO MODESTO SIN CONTENIDO** | sólo F-1 |
| **NO** | nada de lo anterior |

- **Informativos:** C-BAR (BAR ≥ RES en ≥ 10/20), L-PERSISTE, BRECHA.
- **Declarar exige réplica** (12721–12740) con el mismo veredicto o uno mejor. Si da uno peor, vale el peor.
- **Sin recalibración.**

## 7. Predicciones firmadas (serie 12701–12720, T = 100000)

| # | predicción | rango / resultado | p firmada |
|---|---|---|---|
| P1 | mediana de NADA | [0.085, 0.135] | 0.95 |
| P2 | mediana de ORÁCULO | [0.49, 0.62] | 0.95 |
| P3 | mediana de RES | [0.25, 0.55] | — |
| P3 | RES > NADA | ≥ 15/20 | 0.90 |
| **P4** (puede caer) | mediana de BAR | [0.03, 0.14] | — |
| **P4** (puede caer) | RES > BAR | ≥ 15/20 | 0.80 |
| **P5** (puede caer) | BRECHA mediana | [0.50, 1.00] (RES cierra al menos la mitad de la distancia al techo) | 0.60 |
| **P6** (contra mí) | F-5: RES > RES1 | ≥ 15/20 | 0.45 |
| P7 | F-3 en MIX | — | 0.80 |
| P7 | F-4 en MIX | — | 0.80 |
| **P8** | RES `persiste_carro` = 0 | en ≥ 15/20 | 0.85 |
| **P8** | RES `R0_nacidos` < 0.90 | en 20/20 | 0.95 |
| P9 | razón `vida_nacidos` RES/NADA | [1.4, 2.2] | — |
| P10 | telemetría: fracción mediana de tablas RES con B\|hambre = −3 | ≥ 0.60 | — |

**Veredicto más probable según mis propias predicciones:** FUNCIONA sin ACUMULA.

## 8. Controles y qué refuta
- **BAR** gana o empata si la tabla no lleva contenido que sirva. **Aviso honesto:** BAR puede poner −3 en la comida y dañar, así que F-2 sola es más fácil que en la tanda 1. Por eso "por contenido" exige F-1 **y** F-2, y se reporta BAR contra NADA.
- **RES1** refuta la parte "familia": si RES1 ≥ RES, lo que sirve es lo que sabe el padre, no lo acumulado.
- **ORÁCULO** es el techo: RES por encima del ORÁCULO en ≥ 15/20 sería sospechoso; revisar antes de leer.
- **MIX** comparte el flujo del quimiostato.
- **Refuta H-n10b:** F-1 cae, o F-2 cae con C-BAR verdadero.

## 9. Cuatro trampas
1. **Canal simétrico:** la tabla lleva +1, 0 y −3 en las dos necesidades, y BAR conserva la multiset y las claves. La asimetría conocida (BAR puede marcar mala la comida) está declarada en §8.
2. **Acierto sin balancear:** la medida es el éxito reproductivo.
3. **Mundo que se come la comida:** quimiostato con flujo fijo, sin cambios. Quien evita B y D los deja en el mundo; ese costo queda dentro de la medida.
4. **Sitios fijos:** la reposición cae en una celda libre al azar con una letra al azar.

## 10. Vocabulario
**Permitido si FUNCIONA:** "en un mundo con capacidad de carga y generaciones que conviven, cuando el padre vivo pasa al hijo en el parto su tabla (lo que vivió y lo que heredó, por letra y necesidad), los hijos tienen más hijos que sin ella y que con la misma tabla barajada, también compitiendo en el mismo mundo (X/20, replicado); ningún linaje se sostiene: H-1 sigue en pie".
- Con ACUMULA se añade: "la tabla de la familia gana a la del padre solo".

**Prohibido:** "cultura", "enseña", "evoluciona", "la familia se sostiene", "el alma le gana al azar" (el alma es otro mecanismo), y citar `R0_nacidos` como R0 del linaje.

## 11. Puntos del nivel 10–13 (propuesta; decide el director; hoy ~10 %)

| resultado | puntos |
|---|---|
| FUNCIONA replicado | **+8** |
| ACUMULA replicado (sólo sobre FUNCIONA o MODESTO) | **+2** |
| MODESTO replicado | **+4** |
| sin contenido | **+1** |
| NO / NO SE LEE | **0** (se cierra "herencia de tabla en v2") |

Máximo: ~20 %. Ningún resultado lleva al 80 %. Para eso faltan la familia que persiste (el techo de este mundo es 0.55, y ni la tabla verdadera cruza) y el alma que le gana al azar. Queda escrito como el muro.

## 12. Comandos y costo
**Sólo el coordinador ejecuta; Pool ≤ 6; nunca `--serie` desde un agente (ERR-115).**
```
python experimentos/subida_n10b/identidad_familia_b.py                                  # 42/42 antes de todo (~2 min)
python experimentos/subida_n10b/corre_n10b.py --serie --desde 12701 --n 20 --pool 6    # serie
python experimentos/subida_n10b/corre_n10b.py --serie --desde 12721 --n 20 --pool 6    # réplica
```
**Costo:** la tanda 1 hizo 100 tareas en 11 642 s de CPU y 1975 s de pared con Pool 6. Esta tanda tiene 120 tareas → **≈ 14 000 s de CPU, ≈ 40 min de pared por serie**; la réplica cuesta igual. Mirar antes los procesos python vivos (2 Pools / 14 procesos como máximo).
