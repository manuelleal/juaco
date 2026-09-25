# PREREGISTRO — bloque MURO: ¿cruza H-1 el bicho real v14.3 + UNA pieza local? (creador, 25-sep-2026, escrito ~16:40, ANTES del humo)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo.

**Advertencia honesta desde la primera línea: es un TIRO LARGO.** En el exploratorio (5 semillas de práctica), el candidato le gana a
V143 en 3/5 con +0.016 de diferencia mediana, y **no cumple la señal mínima que pidió el director (≥ 4/5)**. Ningún candidato de una sola
pieza la cumplió (§8). Lo entrego igual, como manda el contrato, porque es el mejor de una sola pieza. **Veredicto esperado: NO (p 0.75).**

## 0. Pregunta
¿Una sola regla local y genérica, puesta sobre v14.3, sin copiar la política de O1 ni la de O3, hace que el linaje del bicho real cruce
H-1 en la pista de la carrera (juez tal cual, `cruza_real`, ENMIENDA 5)?

## 1. Hipótesis (de dónde sale)
**"No comas para lo que ya tienes de sobra."** La glotonería de lo bueno vacía el mundo de comida; el cuerpo que se queda sin comida a
la vista muerde lo malo por hambre.
- **Puenteo del coordinador** (`comite2/puenteo/HALLAZGOS.md`, parcial, una semilla): la BOCA_BUENA de O1 sola sube a V143 de 0.722 a 0.900.
  La cadena física que se ve: menos comida buena mordida de sobra, más comida en el mundo, más pasos con meta, menos mordidas malas.
- **Serie frio_carrera 36001–36020 (O1 contra V143 en los MISMOS mundos, `diag.boca`):** V143 muerde A estando SEDIENTO a tasa 0.96–1.0
  (AS), y O1 a 0.09. V143 muerde A+C 807 por linaje y O1 674. El hijo de V143 vive ~1400 y el de O1 ~3200.
- **Lo que YA no es (medido hoy en el exploratorio, §8):** la contención de lo malo, en cuatro formas (CTA, LIMPIA, SINEST, DESF), hunde a
  V143. La "glotonería" por identidad pero SIN nivel (GLOT: no comer lo que sólo sirve a la necesidad no activa) también la hunde
  (0/5, −0.09): mata de hambre, porque veta la comida aunque haga falta para la ventana de parto.

## 2. Mecanismo mínimo (GLOTU, perilla `GLOT = 3`) y memoria nueva
- **Regla.** La boca NO muerde una letra si se cumplen las tres condiciones:
  1. lo que el linaje SINTIÓ al morderla (dS medio, `_adS`) sólo sube UNA necesidad j;
  2. j es la MÁS LLENA de las dos (lev[j] > lev[otra]);
  3. j ya está en el umbral de reproducción o encima (lev[j] ≥ `rep_umbral`, el del mundo, que viene en ctx y que APR ya usa).
- **Todo lo demás es v14.3 tal cual:** patas, FILTRO con meta, opción TD, sorteos. El veto usa el MISMO sorteo que la boca ya sacó.
- **Memoria nueva: CERO.** `_adS` ya está en v14.3 (APR) y el estado presente (E, Ag) lo entrega la pista.
- **Constantes a mano: ninguna.** La única referencia es `rep_umbral`, una cantidad del mundo que el carro ya recibe.
- **Por qué NO es la regla de O1.** O1 usa MARGEN = 0.25 (come si la necesidad está bajo 1.25), PRUEBA = 0.5 y una ganancia ponderada
  por urgencia. Aquí no hay margen ni urgencia ni neofobia. La decisión es categórica: comparar las dos necesidades entre sí y con el umbral.
- **Por qué NO es el cable de saciedad de trasplantes (sac2/sac6 ≈ V143).**
  - Aquel restaba una dosis lineal de la reserva en las tres bocas: toda comida, en toda necesidad, en proporción a lo lleno.
  - GLOTU no resta nada. Veta sólo lo que alimenta a la necesidad MÁS llena, y sólo cuando esa ya pasó el umbral.
  - La comida de la necesidad que más falta nunca se toca. Por eso no rompe la ventana de parto: en la ventana (las dos ≥ umbral) el
    cuerpo come para la menos llena, y la otra baja hasta volverse la menos llena.
- **Por qué no GLOT (sin nivel).** GLOT vetaba la comida de la necesidad no activa aunque estuviera en 0.3, y eso mató de hambre. GLOTU
  sólo veta cuando esa necesidad ya está sobre el umbral.

## 3. Instrumento y anclas
- Carros construidos POR ANCLAS desde `experimentos/tronco_v14_3/carros_v143/V143.py` (sha 2a03048a7f1525e5) con
  `muro/construye_muro.py`: nueve anclas, cada una exacta una vez.
  - Perillas: `PAGA; GLOT; PATAS; TELEM`. Con todas en 0 el carro es V143 bit a bit.
  - Candidato `V143_GLOTU` (0, 3, 0, 1); control `V143_GLOTUINV` (0, 4, 0, 1); `V143_MTEL` (0, 0, 0, 1) para el humo.
  - Los demás carros son sólo del exploratorio.
- Runner `muro/corre_muro.py`:
  - cada corrida ES `corre_v143.tarea`, importada (regla 14, verificada campo a campo en el arnés y en el humo);
  - la pista, el juez y O1 se usan tal cual, con sha fijado;
  - nube-9: toda excepción se atrapa y queda JSON por corrida;
  - `--reanuda`; ERR-115 (banderas desconocidas o abreviadas abortan);
  - la serie rechaza semillas, T o brazos fuera de este preregistro.
- Arnés `muro/identidad_muro.py` (N/N; salida en `identidad_muro_salida.txt`):
  - (K) construye == disco, shas y `revisa_carro`;
  - (A) cada carro con perillas en 0 == V143, salida ENTERA;
  - (B) la telemetría es sólo lectura;
  - (C) regla 14;
  - (D) por pieza, en unidad;
  - (E) la pieza actúa en la pista;
  - (G) determinismo; (F) nube-9 y `--reanuda`; (H) ERR-115; (V) la letra en casos sintéticos.

## 4. Brazos, semillas, T y costo
- **Brazos:** `v143` (base), `glotu` (CANDIDATO), `glotuinv` (CONTROL) y `o1` (techo y ancla). Monocultivo de 9 carros iguales, L 360,
  36 objetos, T 100 000, fundador limpio (ENMIENDA 5).
- **Semillas NUEVAS:** serie 37001–37020, réplica 37021–37040. Práctica 37901–37909: exploratorio 37901–37905, humo 37906–37907, arnés
  37908–37909.
- **Costo:** 80 corridas por serie. En el exploratorio, con 8 procesos, cada corrida tardó 150–225 s; O1 tarda unos 230 s. Con Pool 6:
  **35–45 min por serie**, y lo mismo la réplica.

## 5. Predicciones firmadas (antes del humo)
| # | predicción | rango | p |
|---|---|---|---|
| A1 | V143: mediana del R0 real de todos los linajes | [0.45, 0.78] | 0.85 |
| A2 | O1 cruza (≥ 15/20 semillas con mayoría) | 18–20/20 | 0.95 |
| Q1 | GLOTU: mediana del R0 real | [0.55, 0.82] | 0.70 |
| Q2 | GLOTU contra V143 pareado: semillas ganadas / diferencia mediana | 8–14/20 / [−0.05, +0.10] | 0.65 |
| Q3 | GLOTU: semillas con mayoría de linajes que cruzan | 0–4/20 | 0.85 |
| Q4 | GLOTU come menos: A+C por linaje (mediana) | 450–700, contra ~800 de V143 | 0.80 |
| Q5 | GLOTU: vida mediana (juez) ≥ 1.5 × la de V143 | | 0.65 |
| Q6 | GLOTU: fracción de linajes establecidos (descriptivo) | 0.55–0.80 | 0.70 |
| Q7 | GLOTUINV: R0 real mediana | ≤ 0.15 (0/20 cruzan) | 0.90 |
| V | Veredicto de la serie: NO / HAY ALGO MODESTO / FUNCIONA | | 0.75 / 0.07 / 0.03 (NO SE LEE 0.15) |

## 6. LA LETRA (la misma en `corre_muro.lee_serie`; el arnés la prueba en casos sintéticos)
**Validez (si una falla: NO SE LEE):**
- V1: serie completa (80 corridas, 0 abortos, contabilidad coherente en todos los brazos).
- V2: el ancla O1 GANA (ENMIENDA 5: ≥ 15/20 semillas con mayoría de linajes que cruzan).
- V3: V143 en [0.40, 0.80] (mediana del R0 real; historia: 0.536, 0.63 y 0.602).
- V4: la pieza ACTÚA: `veto_glot` > 0 en el candidato y en el control (telemetría de la última instancia).

**Puertas:**
- **P1 (el candidato cruza):** ≥ 15/20 semillas con mayoría de linajes con `cruza_real`, como O1.
- **P2 (le gana a V143):** pareado por semilla (mediana del R0 real de los 9 linajes): gana en ≥ 15/20.
- **P3 (el control no cruza):** GLOTUINV NO gana por ENMIENDA 5.

**Veredictos:**
- **FUNCIONA:** V1–V4 y P1, P2 y P3.
- **HAY ALGO MODESTO (definido de antemano):** P2, más diferencia mediana pareada ≥ 0.10 (la `DIF_MOD` de corre_v143), más el candidato
  le gana al control en > 10/20. Es decir: sube a V143 de forma sostenida, aunque no cruce.
- **NO:** todo lo demás.
- **Bloque** (serie + réplica): vale si coinciden; si no, vale el menor. NO SE LEE manda.

## 7. Nulos declarados (regla 15)
- N1: GLOTU ≈ V143 (|dif| < 0.05, gana 8–12/20). Es lo más probable (p 0.55): la glotonería no era el cuello o GLOTU no la corrige lo
  suficiente.
- N2: GLOTU come menos (Q4 se cumple) y aun así no gana. Esa lectura es la útil: "comer menos no basta".
- N3: GLOTU le gana a V143 en ≥ 15/20 con dif < 0.10. Eso es NO por la letra, y se reporta como tendencia, sin declarar nada.
- N4: el control GLOTUINV cruza. Sería raro; si pasa, P3 cae y el hallazgo es otro.
- Qué lo refuta: P2 < 15/20. La serie y la réplica se leen por separado; una sola no declara.

## 8. Mini-prueba EXPLORATORIA (un proceso por corrida, ≤ 8 a la vez, T 100 000, semillas 37901–37905; NO es dato)
R0 real, mediana por semilla. V143: 0.909, 0.545, 0.760, 0.423, 0.727 (32/45 establecidos, vida 600, A+C 812, B+D 70).

| brazo | qué es | por semilla | gana a V143 | dif mediana |
|---|---|---|---|---|
| PAGA / CONT / SINEST (v1) | contención con las FILAS de valor | ~0.00–0.34 | 0/5 ×3 | −0.54 a −0.71 |
| CTA (v2) | sin meta, no morder lo sentido malo para la activa | 0.24–0.61 | 2/5 | −0.28 |
| DESF / LIMPIA / SINEST (v2) | CTA desfasado / + limpieza costeable / todo lo malo | 0.12–0.60 | 0–1/5 | −0.36 / −0.40 / −0.56 |
| GLOT | no comer lo que sólo sirve a la no activa (sin nivel) | 0.25–0.64 | 0/5 | −0.087 |
| GLOTFILA / GLOTCTA | GLOT por filas / GLOT + CTA | 0.10–0.29 | 0/5 | −0.61 / −0.52 |
| PATAS / PATASDESF | patas a lo que sirve a la activa / a la otra | 0.42–0.89 / 0.34–0.85 | 1/5 / 1/5 | −0.02 / −0.06 |
| **GLOTU** | **el candidato** | **0.585, 0.750, 0.680, 0.815, 0.743** | **3/5** | **+0.016** |
| GLOTUINV | el control (1 semilla) | 0.000 | 0/1 | −0.91 |
| GLOTU + PATAS | dos piezas (no se preregistra) | 0.688, 0.816, 0.789, 0.875, 0.750 | 4/5 | +0.030 |

GLOTU, descriptivo:
- 32/45 establecidos (igual que V143), con R0 de los establecidos 0.857 (V143 0.883);
- vida 1448 (V143 600);
- A+C 537 y B+D 40 por linaje (V143 812 y 70);
- varianza entre semillas menor que la de V143 (0.585–0.815 contra 0.42–0.91).

## 9. Las cuatro trampas
- **Canal simétrico:** no aplica. La pieza no usa canal; la pizarra está encendida como en la carrera, y ningún carro escribe (arnés E).
- **Acierto sin balancear:** no aplica. La medida es el R0 real de nacimientos del juez, no un acierto.
- **Mundo que se come la comida:** ES la hipótesis. Se mide `comp_mundo` (A, B, C y D promedio) y A+C / B+D por linaje, como descriptivo.
- **Sitios fijos:** no aplica. Posiciones, turnos y reapariciones salen de los rng de la pista (sembrados por semilla y linaje); el
  spawn es al azar.

## 10. Comandos (el coordinador)
```
python experimentos/organelos/muro/construye_muro.py --verifica
python experimentos/organelos/muro/identidad_muro.py                                   # N/N, ~2.5 min
python experimentos/organelos/muro/corre_muro.py --humo                                # 1 proceso, 6 corridas, T 20 000
python experimentos/organelos/muro/corre_muro.py --serie --desde 37001 --n 20 --pool 6
python experimentos/organelos/muro/corre_muro.py --serie --desde 37021 --n 20 --pool 6   # replica
python experimentos/organelos/muro/corre_muro.py --bloque <resumen serie>,<resumen replica>
```
