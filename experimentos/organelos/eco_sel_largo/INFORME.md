# INFORME — ECO_SEL LARGO (nube, 28–29-sep-2026)

**VEREDICTO L: NO ×2.** Con 10× más tiempo (T = 1e7), la capacidad de carga K del linaje SEL_C no sigue subiendo: 39.2 → 38.9
(serie) y 39.1 → 39.0 (réplica); sube en 9/20 y 8/20 semillas. Se estanca desde ~2·10⁵ pasos.
**VEREDICTO MC: FUNCIONA ×2.** Con el margen y el cerebro heredables a la vez, la selección natural sube K por encima del cerebro
solo: SEL_MC 41.7 / 42.6 contra SEL_C 38.9 / 39.0, 20/20 ×2, +2.83 / +3.20. Sin herencia, el mismo genoma se extingue en 19/20.
La ventaja viene con más recambio (más nacimientos, vidas más cortas), no con menos muertes por veneno.

Misión: llegar a la AGI por este camino. Encargo `eco_sel/ENCARGO_NUBE_largo.md`; preregistro `PREREGISTRO_eco_sel_largo.md`
(commit `c08dc32`, antes de la serie `ce8fd87` y de la réplica `338fe40`). Arnés `identidad_eco_sel_largo.py` **65/65**. Humo OK.
Auditor antes (la serie puede correr) y después: recalculó K desde los 200 JSON y **SE SOSTIENE**, con las reservas H-1 a H-3.

## 1. Tabla por brazo (mediana de 20 semillas; K = cuerpos vivos, media en la ventana)
| brazo | genética | K base [0.5e6, 1e6] (serie / réplica) | K final [9e6, 1e7] (serie / réplica) | persiste a 1e7 | nacimientos (mediana, serie) |
|---|---|---|---|---|---|
| F1 | sin mutación | 30.71 / 30.93 | 30.79 / 30.83 | 20/20 ×2 | 183 915 |
| SEL_M (descriptivo) | margen heredable | 34.74 / 34.72 | 34.9 / 34.45 | 20/20 ×2 | 280 778 |
| SEL_C | 15 genes del cerebro | 39.20 / 39.11 | 38.93 / 38.97 | 20/20 ×2 | 176 217 |
| **SEL_MC** | margen + cerebro (16 genes) | **41.78 / 42.04** | **41.68 / 42.60** | 20/20 ×2 | 274 171 |
| AZA_MC | los mismos 16 sin herencia | 20.00 / 16.63 | 0.0 / 0.0 | **1/20 ×2** | 11 967 |

Resúmenes: `datos/eco_sel_largo_serie_s45401-45420/RESUMEN.json` (sha `4ea7829e45474d57`) y `…s45421-45440/RESUMEN.json`
(`39a241e31d795efc`); logs `serie_pool3.log`, `replica_pool3.log`. Validez completa en las dos series: F1 persiste 20/20; 0 refundados;
0 fundadores repuestos; 0 semillas bloqueadas; la genética es la declarada; 100 corridas y 0 abortos por serie.

## 2. Las puertas (por la letra; recalculadas por el auditor desde los crudos)
| puerta | serie | réplica |
|---|---|---|
| L-1a SEL_C sube en ≥ 15/20 | **NO** (9/20) | **NO** (8/20) |
| L-1b mediana de dK ≥ +2 | **NO** (−0.02) | **NO** (−0.14) |
| L-2 no es deriva (AZA_MC no sube; pareado ≥ 15) | sí (0/20; 18/20) | sí (0/20; 19/20) |
| L-3 no es el tiempo (dK SEL_C > dK F1, ≥ 15) | **NO** (8/20) | **NO** (9/20) |
| MC-1 SEL_MC > SEL_C ≥ 15/20 y mediana ≥ +1.5 | **sí** (20/20, +2.83) | **sí** (20/20, +3.20) |
| MC-2 SEL_MC > AZA_MC ≥ 15/20 | sí (20/20) | sí (20/20) |

## 3. La curva de K por ventana de 1e6 (mediana; serie)
| brazo | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | W9 | W10 |
|---|---|---|---|---|---|---|---|---|---|---|
| F1 | 30.84 | 30.89 | 30.74 | 30.82 | 30.87 | 30.83 | 30.93 | 30.82 | 30.79 | 30.79 |
| SEL_C | 38.63 | 38.95 | 39.01 | 39.11 | 39.12 | 39.14 | 38.97 | 38.74 | 39.10 | 38.93 |
| SEL_MC | 40.97 | 42.38 | 41.74 | 41.89 | 41.78 | 41.96 | 41.87 | 41.87 | 41.82 | 41.68 |
| SEL_M | 33.74 | 34.86 | 34.53 | 34.42 | 34.59 | 34.71 | 35.08 | 34.83 | 34.76 | 34.90 |
| AZA_MC | 22.25 | 6.92 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

La réplica da la misma forma (SEL_C 38.78 → pico 39.41 → 38.97; SEL_MC 41.02 → 42.60).

## 4. Genes por ventana (mediana de la media de los vivos; W1 / W5 / W10; serie, réplica entre paréntesis)
- **SEL_C:**
  - alpha 2.40 / 2.43 / 3.15 (2.05 / 2.73 / 2.73);
  - aversion 1.16 / 0.53 / 0.75 (0.97 / 1.00 / 0.55);
  - tau_e 0.47 / 0.33 / 0.30 (0.42 / 0.26 / 0.26);
  - hambre_boca 1.62 / 2.09 / 2.60 (2.12 / 2.36 / 2.65).
- **SEL_MC:**
  - alpha 2.11 / 2.93 / 3.17 (2.24 / 2.89 / 3.51);
  - tau_e 0.38 / 0.32 / 0.31;
  - hambre_boca 2.01 / 2.97 / 3.03 (2.02 / 2.97 / 3.45);
  - **rep_umbral 0.65 / 0.64 / 0.65 (0.62 / 0.57 / 0.63)**.
- **SEL_M:** rep_umbral 0.59 / 0.62 / 0.65 (0.59 / 0.62 / 0.65).
- **AZA_MC** (sin herencia): rep_umbral 1.08 / 1.31 / 1.45 en los que quedan; alpha ~1.6–1.9.
- **Qué se mueve y cuándo:**
  - alpha y hambre_boca siguen derivando hacia arriba toda la corrida, sin que K cambie;
  - tau_e baja y se asienta en el primer millón de pasos;
  - rep_umbral se fija en ~0.6 en SEL_MC y SEL_M desde la primera ventana.

**Causas de muerte:**
- Veneno + sal: F1 0.82 en todas las ventanas; SEL_C y SEL_MC 0.07–0.10 en W1 y 0.02–0.04 desde W2.
- Hambre + sed: 96–98 % de las muertes en SEL_C y SEL_MC (auditor).

## 5. Lectura (y lo que NO dice)
- **L:**
  - En este mundo y con estos 15 genes, la selección natural llega a su techo en ~2·10⁵ pasos. Diez veces más tiempo no lo mueve.
  - Algunos genes siguen derivando (alpha, hambre_boca) sin efecto en K.
  - **No** es evidencia de un techo del mundo ni de otros genes. No hay "evolución abierta" medida aquí.
  - Salvedad del auditor (H-2 previa): la ventana base es de 5e5 pasos y SEL_C aún subía en ella. Eso juega en contra de L, pero la
    curva completa es plana desde W2.
- **MC:**
  - Sumar el margen a los genes del cerebro sube el nivel de K. Es un nivel más alto, no una rampa: la ventaja ya está en la
    ventana base y no crece.
  - No es aditivo. Sobre F1, el margen solo da +4.1, el cerebro solo +8.1 y juntos +10.9.
  - **H-3, la reserva principal:** la ventaja no es mejor supervivencia individual.
    - SEL_MC tiene ~28 000 nacimientos por ventana contra 17 600 de SEL_C, y una vida media de los muertos de ~1 500 pasos
      contra ~2 200.
    - Nacimientos × vida reproduce K (ley de Little).
    - K sube porque el cuerpo **pare con menos reserva** (rep_umbral ~0.6 contra 1.0 fijo en SEL_C): más cuerpos, más jóvenes y más
      breves.
    - Es la trampa 3 declarada en el preregistro §9. No separa "más nacimientos" de "mejor sostén por cuerpo".
  - **H-1:** MC-2 (contra AZA_MC) se cumple en buena parte por extinción: AZA_MC se extingue en 19/20 con t_ext mediana 1.7e6 y 1.2e6,
    y ya arranca por debajo de F1 (K 28.6 contra 30.8 en los primeros 1e5 pasos). Lo sólido es: sin herencia el linaje decae y se
    extingue; con herencia sostiene K ≈ 42. La comparación que sostiene MC es SEL_MC contra SEL_C, 20/20 ×2.
  - **H-4:** L-2a es vacía con AZA_MC extinta. L no depende de ella: cae por L-1 y L-3.
- **Vocabulario:** "la selección natural sube K" con la medida al lado. Prohibido: "evolución abierta", "aprende", "más listo",
  "mejor forrajea".

## 6. Predicciones firmadas contra resultado
- **Creador:**
  - L: FUNCIONA 0.20 · MODESTO 0.25 · NO 0.50 → **NO**;
  - MC: FUNCIONA 0.35 · MODESTO 0.15 · NO 0.45 → **FUNCIONA**;
  - V1 (F1 persiste ≥ 17/20) 0.85 → 20/20;
  - **E7 falla:** predijo que AZA_MC persistiría en 2–14/20; persistió 1/20 ×2.
- **Coordinador** (en el chat, antes de la serie): L-1 pasa ~0.5 → NO; MC ~0.3 → FUNCIONA. Subestimé MC.

## 7. Decisiones difíciles (hora, opción tomada, alternativa descartada y porqué)
- **28-sep ~20:50 · Worktree aparte** (`/home/user/juaco-eco`) en vez de checkout.
  - Por qué: en `/home/user/juaco` corría la serie de TERMO′ con Pool 3, y un checkout habría borrado sus archivos a media corrida.
  - La serie de ECO esperó a que terminara TERMO′: un solo Pool a la vez.
- **~21:05 · ERR-150.** El caso del arnés del encargo "SEL_MC con σ = 0 == F1" no puede cumplirse, porque `motor_eco.muta` mueve −1 un
  gen entero con z = 0. Se partió en (B) p_mut = 0 == F1 y (B′) con σ = 0 sólo se mueven los enteros. Con σ 0.15 la regla es simétrica
  y no sesga la serie (auditor).
- **SEL_M se corrió** como descriptivo: cabía en el presupuesto (≈ 3.1 h por serie con Pool 3).
- **L-2 y L-3 más estrictas que el encargo** (creador): el pareado contra AZA_MC y L-3 contra F1, porque F1 hereda cultura por la tabla
  de la familia. **Sin puerta de firma contra sombras:** a 1e7 la deriva de las sombras llena el rango.
- **Checkpoints cada 1e5 pasos** (1e4 en eco_sel), por tamaño del blob; el arnés (A)/(Q) prueba que no cambian la corrida. No se
  commitean (carpeta `ckpt`).

## 8. Errores de instrumento declarados
- **ERR-150** (arriba): caso de identidad del encargo imposible por construcción; detectado y resuelto antes de la serie.
- Arnés, dos fallos de diseño de casos corregidos antes de la serie, sin número:
  - una comparación exacta de cuantiles contra genes redondeados a 1e−6 (tolerancia 2e−6);
  - `mutables == 16` contra el motor, que sólo reporta los genes con p > 0.
- Núcleo, runner y letra no cambiaron entre las tres corridas del arnés (salidas v1 61/64 y v2 63/65 guardadas).
- El siguiente ERR libre es **ERR-151**.

## 9. Qué sigue (propuesta; decide el director)
- **L cerrada para estos genes:** el techo no es el tiempo. Para buscar evolución abierta hay que cambiar lo que puede variar, o el
  mundo. El siguiente peldaño natural es endurecer o cambiar el mundo (comida que cambia, nuevas letras) y medir si la selección
  vuelve a subir K.
- **Separar H-3:** un brazo con rep_umbral heredable y **coste de parto mayor**, o K medida como biomasa de reserva en vez de cuerpos,
  para distinguir "más cuerpos breves" de "mejor sostén".

## 10. Línea para CLAUDE.md
> 29-sep-2026 (nube): **ECO_SEL LARGO: L = NO ×2, MC = FUNCIONA ×2** (T 1e7, 45401–45440). K de SEL_C se estanca desde ~2·10⁵ pasos
> (39.2 → 38.9 y 39.1 → 39.0); margen + cerebro heredables suben K a 41.7 / 42.6 (20/20 ×2 sobre SEL_C, +2.8 / +3.2), vía más recambio
> (rep_umbral ~0.6: más nacimientos, vidas más cortas), no menos muertes; sin herencia se extingue 19/20. ERR-150. `experimentos/organelos/eco_sel_largo/INFORME.md`.
