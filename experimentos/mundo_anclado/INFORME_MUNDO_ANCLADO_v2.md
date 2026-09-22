# INFORME — MUNDO ANCLADO v2: toxicidad + dilución (ERR-? pendiente) · calibración INCOMPLETA

**Veredicto provisional: HAY ALGO MODESTO.** El mundo anclado EXISTE en la calibración, en dos de las tres filas de la
rejilla 3 × 3. El punto no puede fijarse todavía: la regla 5c elige entre las tres filas y la fila tox = 2.0 queda para
el coordinador (presupuesto de CPU).

## Qué hice
1. Humo v2 (semilla 1): `datos/humo/anclado2_humo_20260922_142242.json`, sha `18b8aaf07a1ae6eb`. Identidad OK:
   `tabla(1.0)` da el mismo dict completo que sin tabla (ORÁCULO s1, T = 20 000).
2. Escribí `PREREGISTRO_mundo_anclado_v2.md` (sha `8404b03e172acf6f`) antes de tocar 7021–7080. La v1 queda como
   antecedente con ERR-? pendiente.
3. `corre_anclado_v2.py` (sha `fc3d6754d86b29af`) importa la v1 (instrumento `organismo_anclado.py` `e689c2952b1991a4`,
   brazos, resumen y puertas) sin copiarla. La regla 14 da OK en los 7 brazos, con `tabla` como perilla declarada.
4. Calibración en 7021–7040, sólo NADA y ORÁCULO, un proceso, dos filas.

## Rejilla (medianas de 20 semillas; T = 100 000; rep_acum = 0)
| tox (daño por bocado malo ×) | h (por objeto y paso) | R0 NADA | R0 ORÁCULO | razón | ancla | vida NADA / OR | f_mala OR | J NADA / OR |
|---|---|---|---|---|---|---|---|---|
| 1.25 | 0.003 | **0.291** | **1.078** | 3.71 | SÍ (fila cerrada, 5b) | 100 / 662 | 0.83 | 0.18 / 0.97 |
| 1.5 | 0.003 | 0.107 | 0.677 | 6.35 | no | 20 / 152 | 0.83 | 0.17 / 0.99 |
| 1.5 | 0.006 | **0.247** | **1.517** | 6.14 | SÍ (fila cerrada, 5b) | 22 / 590 | 0.77 | 0.18 / 0.98 |
| 2.0 | 0.003 / 0.006 / 0.012 | sin correr (coordinador) | | | | | | |

Datos:
- `datos/anclado2_cal_s7021-7040_fila0_20260922_143838.json` (sha `6162f1216b7c147b`)
- `datos/anclado2_cal_s7021-7040_fila1_20260922_142433.json` (sha `e8c95e0721edb38a`)

## Lectura
- La toxicidad abre la razón: de ~3 en la v1 a 3.7 (tox 1.25) y a 6.1–6.4 (tox 1.5). La dilución sube el nivel.
- J no se mueve (NADA ~0.18, ORÁCULO ~0.98): el cuerpo es el mismo.
- f_mala ≥ 0.77: el mundo no se come lo malo.
- Por la regla 5c (el ORÁCULO más bajo que sea ≥ 1.0), hoy ganaría **tox 1.25 / h 0.003**. Pero su NADA (0.291) está a
  0.009 del borde, así que el riesgo de que ANC-1 caiga en la confirmación es alto.
- tox 1.5 / h 0.006 tiene margen en NADA (0.247) y un ORÁCULO más alto.
- La regla es la escrita y NO se cambia: se declara el riesgo, no se enmienda.

## Predicciones propias
- **Q1 REFUTADA en parte**: la fila tox 1.25 SÍ ancla (yo dije que no). El punto que predije (1.5 / 0.006) ancla, pero
  la regla no lo elige si gana 1.25.
- **Q2**: NADA 0.247 (dentro de 0.12–0.26) y razón 6.1 (≥ 5) pasan. ORÁCULO 1.517 queda fuera de 1.00–1.40: REFUTADA
  en esa parte.
- **Q7 se cumple** en 1.5 / 0.006: vida mediana de NADA 22 pasos, o sea que la ignorancia muere al primer bocado malo
  (trampa de la sec. 4, declarada). En 1.25 / 0.003, NADA vive 100 pasos.
- Pendientes de la confirmación: Q3 (REL R0 0.85, posición 0.80), Q4, Q5 y Q6.

## Lo que queda (coordinador, en orden)
```
python experimentos/mundo_anclado/corre_anclado_v2.py --calibra --fila 2 --pool N            # tox 2.0, 7021-7040 (40-120 corridas)
python experimentos/mundo_anclado/corre_anclado_v2.py --elige 20260922_143838,20260922_142433,<SELLO_FILA2>
python experimentos/mundo_anclado/corre_anclado_v2.py --confirma --tox K --h H --desde 7041 --pool N   # 140 corridas
python experimentos/mundo_anclado/corre_anclado_v2.py --confirma --tox K --h H --desde 7061 --pool N   # réplica
```
- `--elige` se niega a elegir sin las tres filas (comprobado).
- Con `--pool`, la fila 2 conserva el orden secuencial por punto: el Pool sólo reparte las 40 corridas de cada punto.
- CPU del creador en la v2: unos 23 min (humo 1.4, fila 1 unos 14, fila 0 unos 7), un proceso, sin Pool.

## CIERRE (coordinador, 22-sep-2026, tras la auditoría: SE SOSTIENE CON RESERVAS)

**Veredicto oficial (letra de §6 del PREREGISTRO v2): HAY ALGO MODESTO.** Las anclas pasan en UNA de las dos series.

| serie | NADA | ORÁCULO | REL | posición REL | REL ≥ 0.9 / ≥ 1.0 (semillas) | REL_BAR | ORÁCULO_CIEGO |
|---|---|---|---|---|---|---|---|
| elección (regla 5c) | 0.291 (cal.) | 1.078 (cal.) | — | — | — | — | — |
| confirmación 7041–7060 | **0.3034 (ANC-1 CAE)** | 1.161 | 0.948 | 0.751 | 13/20 · 5/20 | 0.371 | 0.923 |
| réplica 7061–7080 | 0.2777 | 1.171 | 0.926 | 0.726 | 12/20 · 6/20 | 0.390 | 0.886 |

**Qué se puede declarar:**
- Existe un mundo casi anclado con dos perillas (toxicidad 1.25 y dilución de lo malo 0.003 por objeto): la ignorancia no se sostiene y el conocimiento perfecto sí. Queda en el borde: NADA falla por 0.003 en una serie.
- En ese mundo, el nodo por relevancia (REL) cubre 0.73–0.75 del espacio NADA–ORÁCULO en dos series, y es su **contenido** lo que lo hace: con la memoria barajada, REL_BAR queda en 0.08–0.13 del espacio y A12 = 1.0.
- Lo que ancla es el **tipo** de lo que se diluye y no el recambio: el placebo de dilución ciega queda por debajo del ORÁCULO (A12 0.91 / 0.97).

**Qué NO se puede declarar:** que "REL cruza el umbral". Que su mediana supere 0.9 es en gran parte aritmética de la regla 5c: se eligió el ORÁCULO más bajo que ancla, y con una posición ~0.74 eso da ~0.93. Por semilla, solo 60–65 % supera 0.9 y 25–30 % supera 1.0. La posición de REL no mejora respecto del mundo sin perillas (0.80–0.84).

**Hallazgos de la auditoría pendientes de ERR** (se numeran al cierre del día):
- (H-1) Este informe no se había actualizado con el veredicto; se hace aquí.
- (H-3) El runner imprime la predicción P3 de la v1 (0.55–0.90) en vez de la Q3 de la v2 (0.80; rango 0.65–0.95). No cambia nada esta vez.
- (H-4) `--elige` no archiva su salida; el auditor reconstruyó la regla a mano y dio el mismo punto.
