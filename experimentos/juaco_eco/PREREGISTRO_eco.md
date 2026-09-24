# PREREGISTRO — JUACO-ECO v1: vivero y corte en un mundo gigante con el organismo real (23-sep-2026, creador; antes de cualquier serie)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/juaco_eco/`. Nivel: **10 (JUACO-ECO; niveles 10–13 ≈ 10 % hoy)**.
No es candidato a tronco: `CRITERIO_TRONCO_v4` no aplica. Tronco v14.2 intacto; no se toca ningún congelado.

## 0. Instrumento (sha a 16)
- `construye_eco.py` (3498fc364e27c091) construye por anclas:
  - `motor_eco.py` (bca3033878b59622) desde `generaciones/motor_convive.py` (d10cb9021f5d0f41);
  - `carros/FABRICA_ECO.py` (f1163009cb5193a2) desde `carrera_escuderias/carros/FABRICA.py` (2ebee3e99ea5a33a);
  - `carros/APR_ECO.py` (a9511ba0669f7359) desde `APR.py` (4402aa5142065c72).
- En los carros sólo cambia `_see`: busca hacia afuera, O(distancia) en vez de O(objetos). La salida es la misma.
- Runner y juez: `corre_eco.py` (0627f237b597523a antes de ERR-121; **47d9cee4d6462116 después de ERR-121**, que es el que corre la
  serie). Arnés: `identidad_eco.py` (b70ec2f05915dc2e), **41/41**. La nube lo detectó la noche del 23-sep (bitácora, nube-1); corregido en main.

## 1. Pregunta e hipótesis
**Pregunta:** ¿el organismo real sostiene un linaje en un mundo gigante con flujo fijo de comida si hay herencia con mutación y nadie
repone fundadores? Mundo de flujo fijo = ERR-104; nadie repone fundadores = ERR-118.

**Hecho medido antes de diseñar** (humo exploratorio, semilla 10012):
- Sin ayuda, 90 FABRICA en L = 3600 bajan de 90 a 1 cuerpo en 3000 pasos.
- El «ECO puro» con FABRICA muere antes de que la mutación pueda actuar: NO esperado con p ≈ 0.97.

Por eso el mínimo que se añade es un **vivero**.

**H (VIDA):** mutación de 18 perillas + selección natural durante el vivero producen genomas que:
- (a) sostienen un linaje después del corte;
- (b) se apartan de la deriva, medida contra sombras;
- (c) viven más que G0 en una batería sellada.

**H-c (CEREBRO):** lo mismo mutando sólo las 15 perillas del cerebro y la estructura, con la historia de vida fija. Es lo que movería el nivel 9.

## 2. Mecanismo mínimo y memoria nueva
- **Memoria nueva en el organismo: CERO.** El genoma son 18 números por cuerpo que viven en el registro del mundo. Entra por `ctx`, como las constantes de fábrica.
  - Cerebro: `eta, tau_e, alpha, hambre_boca, aversion, ema, paso, lam, memoria_rechazo, eta_s, clip_s, del_s, del_c, ema_c`.
  - Estructura: `NK` (celdas de Kenyon activas al nacer).
  - Historia de vida: `dote, rep_umbral, rep_X`.
  - Además, 8 **genomas sombra** que no se expresan (Bedau y Packard 1992).
- **Mutación al nacer:**
  - Por gen, con p = 0.05: factor log-normal σ = 0.15. Tasa medida en el humo: 0.048.
  - Rango [G0/4, 4·G0] ∩ topes duros. Los enteros se redondean.
  - rng propio `[seed, linaje, 16, k]`: no toca ningún rng del mundo ni del cuerpo (arnés E).
- **Herencia:**
  - VIDA y CEREBRO: el hijo copia el genoma del padre, mutado.
  - AZAR: copia una entrada al azar del banco (ver abajo).
- **Vivero (t < t_corte = 60 000):**
  - Si un linaje se extingue, el mundo pone un fundador con el genoma de una entrada al azar del **banco**, mutada.
  - Banco = anillo de 200 genomas.
  - VIDA y CEREBRO: el banco guarda el genoma del **padre** en cada parto. Es selección por fertilidad y viabilidad.
  - AZAR: el banco guarda el genoma **nuevo** al crearse; ningún genoma influye en su propia copia.
- **Corte (t ≥ 60 000):** nadie pone nada. Si todo muere, muere, y la corrida lo marca y para. T = 120 000.
- **Mundo:** pista v2 × 10 (esc = 90):
  - L = 3600, hasta 360 objetos, olvido y quimiostato r = 0.03·90 = 2.7 objetos por paso;
  - 90 fundadores FABRICA_ECO;
  - tope de seguridad de 3000 cuerpos (si se alcanza, la serie NO SE LEE);
  - interacción: mismo recurso y la misma celda; la pizarra existe, pero FABRICA no escribe (no se mide comunicación).

## 3. Brazos (los 4 con las mismas semillas)
| brazo | genes que mutan | donante | papel |
|---|---|---|---|
| VIDA | 18 | padre | hipótesis |
| CEREBRO | 15 (sin dote/umbral/rep_X) | padre | H-c |
| AZAR | 18 | banco al azar (neutral) | **control de mutación sin selección** (puede ganar) |
| MUT0 | ninguno | padre | **control del vivero solo** (puede ganar) |

## 4. Medidas (sólo física)
- **persiste:** cuerpos vivos en T = 120 000; todos descienden de cuerpos vivos en el corte.
- También: t_ext, cuerpos y linajes en T, generación máxima, y R0 de la cohorte nacida en [corte, T − 20 000].
- **Selección contra deriva** (en el corte, sobre el BANCO):
  - Por gen: +1 si la media de log(g/G0) del banco real supera a las 8 medias sombra; −1 si queda por debajo de todas; 0 si no.
  - Bajo neutralidad, P(+1) = P(−1) = 1/9.
  - **No se usa la media de los vivos:** está sesgada por viabilidad (humo exploratorio, ver INFORME).
- **Juez automático** (batería fija):
  - Mundo esc = 9, 9 fundadores, sin mutación ni reposición, T_b = 20 000, semillas **selladas 19201–19220**.
  - Fundadores = 9 entradas al azar del banco en el corte (rng `[s, 7]`), contra 9 copias de G0.
  - Medida: supervivencia de la colonia (t_ext o T_b). Una semilla de la serie **gana** si la mediana de su batería > la mediana de G0.

## 5. Semillas NUEVAS (grep en `PROYECTOS/JUACO/*`: ninguna aparece como semilla; el único 193xx es un arXiv 2509.19349)
- Serie **19101–19120**; réplica **19121–19140**; batería del juez **19201–19220** (selladas).
- Práctica y humo: 19001–19040 (usada 19001 en el humo; el arnés usa 10001–10011 de la práctica de convive y 19011–19012).
- ECO largo: **19301–19303**.
- Los humos exploratorios usaron 10012/10013 (práctica de `generaciones`): no se reutilizan.

## 6. Criterio por la letra (`corre_eco.veredicto`; se imprime al final)
Por serie:

**Predicciones**
- **P1:** VIDA persiste en ≥ 15/20.
- **P1c:** MUT0 persiste en ≤ 2/20.
- **P2:** algún gen del banco de VIDA queda fuera de sus 8 sombras con el mismo signo en ≥ 15/20.
- **P3:** el juez da la victoria a VIDA en ≥ 15/20.
- **P3c:** AZAR gana en el juez en ≤ 10/20.
- **P4:** VIDA − AZAR ≥ 8 semillas persistentes.
- **H-c:** CEREBRO persiste en ≥ 15/20.

**Veredicto**
- **NO EVALUABLE** si ocurre cualquiera de estas cosas:
  - la serie está incompleta;
  - hay bloqueados > 0;
  - MUT0 persiste en ≥ 10/20 (el mundo es demasiado fácil);
  - AZAR da > 8/20 en algún gen (el control de sombras no vale);
  - **AZAR gana el juez en > 10/20 (P3c falla): el juez no distingue selección de azar.** Esta condición es una enmienda **ERR-121**
    (23-sep, 19:50, auditoría H-2). Se añadió ANTES de cualquier serie: P3c ya se calculaba, pero no decidía nada.
- **FUNCIONA:** P1 + P1c + P2 + P3 + P4.
- **HAY ALGO MODESTO:** P2 + P3.
- **NO:** cualquier otro caso.

El bloque se declara sólo si **serie y réplica dan el mismo veredicto**. Si no, se declara el menor.

**Vocabulario**
- Permitido: «linaje», «cuerpos vivos del brazo (N = …)», «genoma», «seleccionado contra sombras».
- **Prohibido:**
  - «población», salvo con la medida al lado;
  - «evoluciona», «especie», «vida artificial abierta», «novedad abierta».
- Lo que v1 puede mostrar como novedad es **adaptación heredable replicable** en un espacio acotado de 18 perillas (N-1 = P2, N-2 = P3). No es novedad abierta: el espacio no crece.

## 7. Predicciones firmadas (creador, tras 5 humos exploratorios y el humo 19001; ver INFORME)
| cantidad | rango predicho | probabilidad |
|---|---|---|
| VIDA persiste /20 | 0–8 | P1 se cumple con 0.10 |
| MUT0 persiste /20 | 0–2 | P1c se cumple con 0.90 |
| AZAR persiste /20 | 0–6 | — |
| CEREBRO persiste /20 | 0–6 | H-c con 0.05 |
| **alpha sube en el banco de VIDA (+1) /20** — **la que puede fallar** | 12–20 | P2 con 0.55 |
| VIDA gana en el juez /20 | 6–18 | P3 con 0.35 |
| supervivencia mediana de G0 en la batería | 1500–4500 pasos | 0.8 |
| veredicto | NO 0.50 · MODESTO 0.35 · FUNCIONA 0.07 · NO EVALUABLE 0.08 | — |

## 8. Qué refuta
- **H:** P2 cae (no hay selección distinguible de la deriva) o P3 cae (lo seleccionado no vive más fuera del vivero).
- **Alcance:** si MUT0 ≈ VIDA en persistencia, la mutación no es la causa.
- **El control:** si AZAR ≈ VIDA en el juez, la selección no aporta.

## 9. Puntos del nivel (propuesta; decide el director)
| resultado | niveles 10–13 | nivel 9 |
|---|---|---|
| FUNCIONA ×2 | ~10 → 20 % | +10 si además H-c ×2 (la pieza «linaje que persiste con capacidad de carga», con perillas del propio cerebro) |
| HAY ALGO MODESTO ×2 | → 13 % | 0 |
| NO | 0; cierra «ECO v1 con perillas de FABRICA»: el espacio de 18 perillas no contiene una vida viable con flujo fijo, y ECO pide estructura nueva (v14.3 u otro carro) | 0 |

## 10. Enmiendas tras el humo (candidatos a ERR)
- (a) El juez usaba la mediana del banco. Con mutaciones raras esa mediana **es G0**, así que comparaba G0 con G0. Ahora usa 9 entradas del banco (arnés J).
- (b) El corte guarda el banco completo.
- (c) Modo `--largo`, sin veredicto.
- La física del motor no cambió después del humo: el arnés (I), (E) y (C) lo cubre.
