# PREREGISTRO v0.1 — ¿la CINTA evoluciona mejor que las PERILLAS cuando se IGUALA la carga mutacional? (24-sep-2026, Opus del equipo organelos)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/organelos/codigo/v01/`. Todo es nuevo. `motor_fable.py` y `fable_mundos.py`
del Fable se usan sin tocarlos: el motor se construye por anclas desde el primero y el segundo se importa (sha fijados en el arnés I0).
**Escrito antes de cualquier semilla de serie.** Lo que se vio antes (calibración y humo) está declarado en §3 y §9.
La serie la lanza el coordinador en el PC del director (Pool 6). La réplica queda para mañana.

## 0. Instrumento (sha a 16; `corre_v01.SHAS()`)
| archivo | sha | qué es |
|---|---|---|
| `motor_v01.py` | 8a67a259baa5454b | lo construye `construye_v01.py` (58a9004f1bdefee1) por 4 anclas desde `exploracion_fable/motor_fable.py` (46750da69ef8cce1) |
| `exploracion_fable/fable_mundos.py` | ccb39d6de1cd62d3 | se importa |
| `codigo_def.py` | 1096202c8afaa3d1 | el de v0 |
| `carros/FAMB_GRAM_ECO.py` | 2cee0a8510c997b9 | el de v0 |

- Las 4 anclas agregan solo telemetría:
  - V1: el fenotipo cambiado por parto en PERILLAS, con la misma definición que en la cinta: las 20 perillas más la gramática.
  - V2: **el banco de CINTAS en el corte**.
  - V3: la salida de las dos cosas.
  - V0: rutas.
- **La física es la de `motor_fable` bit a bit** (arnés I1).
- Runner: `corre_v01.py`, con la letra en `veredicto()`. **sha de la serie: b835e4c4a94e6355**; el arnés 11/11 se corrió con él a las 22:11. El humo corrió con c8949ac3f9c6123f; después sólo cambiaron el orden de los trabajos (§5), la guardia AZAR «no medida» y el descriptivo de `--lee`.
- **Arnés `identidad_v01.py` 11/11** (`identidad_v01_salida.txt`):
  - **I2, la pedida:** PERILLAS_ROBUSTA con la mutación en cero == PERILLAS con la mutación en cero, bit a bit (salida entera).
  - I2b: ROBUSTA con λ = 1 == PERILLAS: difieren SÓLO en la tasa.
  - I1: `motor_v01` == `motor_fable` en 4 brazos/mundos.
  - I3: fenotipo idéntico medido en PERILLAS: 1.000 con mutación 0; 0.340 con la de hoy (analítico 0.311); 0.614 con λ 0.5 (0.562).
  - I4: banco de cintas en el corte (MUT0 → todas CINTA0).
  - I5: el mundo `quieto` == sin cambio, en la física.
  - I6: AZAR no lleva SOS.

## 1. Pregunta (la que decide si la idea del director tiene sustancia)
- En el Fable (exploratorio) el CÓDIGO vive solo mejor que PERILLAS incluso sin cambio del mundo (razón 1.54). MUT0 rinde como PERILLAS:
  la ventaja viene de los ERRORES de copia de la cinta.
- Pero v0 igualó **errores por copia** (~1.1), no **fenotipos cambiados por copia**. Con la cinta el ~72 % de los hijos nace con el
  fenotipo IDÉNTICO al del donante; con PERILLAS, el ~31–34 %.
- **Pregunta:** con la carga igualada en fenotipos (PERILLAS_ROBUSTA), **¿la cinta sigue viviendo sola mejor?**
  - Si sí: la ESTRUCTURA de la cinta ayuda (qué variación ofrece, no cuánta).
  - Si no: la ventaja era sólo mutación más suave.
- Nombre honesto si sale bien: «**con la carga mutacional igualada, la cinta vive sola mejor que las perillas**». No es «el código de la vida».

## 2. Mundos (de `fable_mundos.catalogo(t_cambio)`)
- `quieto`: el mundo no cambia (la BASE).
- `onda8k`: estacional coseno de período 8000; A y B intercambian su valor y vuelven, sin saltos.
- `golpe` queda fuera por costo; `--con_golpe` es opcional y está fuera de la letra.

## 3. Calibración de PERILLAS_ROBUSTA (regla fijada a las 21:44, antes de correr la fase 2)
- **Fase 1** (21:33–21:43): semillas 29901–29903, TL_CAL = T 36 000, cambio 8000, corte 24 000 (el TL corto del Fable), CODIGO_SIN_SOS
  en quieto y onda8k.
  - Mide la fracción de partos antes del corte con fenotipo IDÉNTICO al del donante (las 20 perillas y la gramática).
  - Da **0.7148 pooled (n 3868)**; por corrida, de 0.67 a 0.78. **Objetivo: f* = 0.715.**
- **Lambda analítica:** λ₁ = 0.292, de f(λ) = (1 − 0.05λ)^18 (1 − 0.02λ)² (1 − 0.05λ)⁴. Es un único factor sobre TODAS las tasas de
  PERILLAS: numérica y gramática.
- **Regla de la fase 2** (PERILLAS_ROBUSTA en quieto, semillas 29904–29906, λ₁):
  - se acepta si |f_medida − 0.715| ≤ 0.03;
  - si no, UNA corrección: λ₂ tal que f(λ₂) = f* + (f(λ₁) − f_medida), verificada en las mismas semillas. Se toma la λ, λ₁ o λ₂, cuya
    f_medida quede más cerca de f*. No hay más iteraciones.
- **Fase 2 (21:43–21:49): f_medida = 0.721 (n 1663; 0.707–0.728 por corrida). Se acepta: LAMBDA_ROB = 0.292.**
- **Declarado:**
  - La calibración se corrió con TL_CAL, más largo que el TL de la serie (§5, recortado después por el límite del director), con 3 + 3
    semillas.
  - El humo a la TL de la serie vuelve a medir las dos fracciones. **Tolerancia: si en la serie la mediana de ROBUSTA y la de SIN_SOS
    difieren en más de 0.05 en quieto, P1 se lee con la nota «carga no igualada» y lleva ERR.**
  - ROBUSTA iguala la FRECUENCIA de hijos con fenotipo cambiado, no el TAMAÑO del cambio. Un paso de cinta mueve 0.15 en log (EJE: 4
    rasgos); PERILLAS mueve σ 0.15 lognormal.

## 4. Brazos (w30, banco 200, sin sombras; vivero hasta el corte; después SOLOS)
| brazo | genoma y variación |
|---|---|
| **CODIGO_SIN_SOS** (principal) | CINTA0 de v0 + copia con errores por tramo; la SOS no se lee |
| **PERILLAS** | vector de hoy desde filtra0 + G0: numérica p 0.05 σ 0.15 (18 genes) + gramática (campo 0.05, dup 0.02, del 0.02) |
| **PERILLAS_ROBUSTA** | PERILLAS con todas las tasas × 0.292 |
| **MUT0** | CINTA0 sin errores de copia |
| **AZAR** | CODIGO_SIN_SOS con donante al azar del banco (deriva). En v0 AZAR llevaba la SOS; aquí sigue al brazo principal (I6) |
| CODIGO (con SOS) | OPCIONAL (`--con_sos`, +~9 min): P3 sólo se mide si se corre |

## 5. TL de la serie y costo (límite del director: ≤ 45 min de pared con Pool 6 y 20 semillas)
- **TL = T 24 000, t_cambio 0, corte 16 000, margen 2 000.**
  - La onda corre desde t = 0: en el corte lleva 2 períodos exactos, así que el mundo está en su fase de fábrica, igual que en el Fable.
  - «nac solo» = nacimientos reales con t en [16 000, 22 000).
- Recorte declarado frente al Fable (vivero 24 000, del cual 16 000 con onda):
  - aquí el vivero dura 16 000, todo con onda;
  - hay menos generaciones de selección antes del corte, así que el efecto puede ser más chico que en el Fable.
- **Costo** (medido en el humo, §9): 2 mundos × 5 brazos × 20 semillas = 200 corridas. Con `--con_sos`, 240.
- **Orden de la serie:** primero los 4 brazos mínimos (160 corridas), después AZAR (40). Si el tiempo se acaba, lo que cae es AZAR.
  - La letra mínima exige completos los 4 mínimos.
  - Sin AZAR completo, la guardia de selección queda «no medida» y FUNCIONA baja a HAY ALGO MODESTO («selección no verificada»).

## 6. Medidas y la letra (`corre_v01.veredicto`; pareado por semilla; empate = no gana)
- **Medida principal: nac solo.**
- Secundarias: persistencia en T y R0 final solo (hijos medios de los nacidos en [corte, T − margen]; 0 si no hay).
- Descriptivas:
  - la fracción de hijos con fenotipo idéntico, por brazo (la carga);
  - errores por copia;
  - el banco en el corte: las cintas desarrolladas y las perillas de PERILLAS, en log(g/G0) de los rasgos de historia de vida y
    aprendizaje (`--lee`).

| prueba | criterio |
|---|---|
| **P0** (la base se reproduce) | CODIGO_SIN_SOS > PERILLAS en nac solo en quieto, ≥ 15/20 |
| **P1, LA QUE DECIDE** | CODIGO_SIN_SOS > PERILLAS_ROBUSTA en nac solo, ≥ 15/20, **en quieto y en onda8k por separado** |
| **P2** (amplificación) | razón de sumas (+1) SIN_SOS/ROBUSTA en onda8k ≥ 1.5 × la de quieto. Se informa también contra PERILLAS |
| **P3** (sólo con `--con_sos`) | CODIGO > SIN_SOS ≥ 13/20 → «la SOS ayuda»; SIN_SOS > CODIGO ≥ 13/20 → «la SOS ESTORBA» |
| **Guardias** (quieto) | variación: SIN_SOS > MUT0 ≥ 14/20 · selección: SIN_SOS > AZAR ≥ 14/20 |

**Veredicto, en orden:**
1. **NO EVALUABLE**: ventana incompleta, corridas abortadas o tope de cuerpos.
2. **FUNCIONA**: P1 pasa en los DOS mundos y las dos guardias.
3. **HAY ALGO MODESTO**:
   - P1 pasa en los dos mundos pero cae una guardia. Es una regla que el coordinador no pidió; la agrego para que una guardia que puede
     fallar cuente.
   - P1 pasa en uno solo.
4. **NO**: P1 no pasa en ninguno. Lectura: la ventaja de v0 era mutación más suave.

Réplica (29031–29050, mañana): el mismo veredicto.

## 7. Predicciones firmadas (antes de la serie; después de ver la calibración y el humo de 1 semilla)
**Mecanismo que apuesto.** MUT0 (carga cero) rinde como PERILLAS (carga alta) en el Fable. La carga sola, entonces, no ordena el
resultado, así que ROBUSTA (carga intermedia) debería rendir como PERILLAS, y el CÓDIGO seguir ganando.
- Mi candidato: **la pleiotropía de los EJES**. Una sola mutación `EJE 2 −1` baja a la vez dote, rep_umbral, rep_X y tau_e: «vida
  rápida». Eso es lo que la selección por fertilidad del vivero (el banco guarda a los que parieron) empuja, y en PERILLAS pide 4
  mutaciones independientes.
- En el banco del corte, CÓDIGO debería mostrar la historia de vida más baja que PERILLAS y que ROBUSTA (descriptivo, `--lee`).

| prueba | P |
|---|---|
| P0 | 0.55 |
| P1 en quieto | 0.45 |
| P1 en onda8k | 0.35 |
| P1 en los dos | 0.28 |
| P2 | 0.15 (el Fable: 1.60 frente a 1.54) |
| P3, si se corre: «la SOS estorba» | 0.45 |
| P3: «la SOS ayuda» | 0.05 |
| guardia de variación | 0.65 |
| guardia de selección | 0.60 |

| veredicto | P |
|---|---|
| FUNCIONA | 0.18 |
| HAY ALGO MODESTO | 0.32 |
| **NO** | **0.45** |
| NO EVALUABLE | 0.05 |

- **Rangos** (serie, medianas por semilla):
  - fracción idéntica: SIN_SOS 0.66–0.78 y ROBUSTA 0.68–0.76; PERILLAS 0.28–0.38; MUT0 1.0;
  - nac solo en quieto: 40–110 por brazo;
  - persistencia en quieto: ≥ 12/20 en SIN_SOS, PERILLAS y ROBUSTA;
  - en onda8k: ≤ 10/20.

## 8. Semillas (29000–29999, asignadas; grep del 24-sep: sin usos como semilla)
| uso | semillas |
|---|---|
| humo | 29001 |
| identidad | 29002 |
| **serie** | **29011–29030** |
| **réplica** | **29031–29050** |
| calibración | 29901–29906 |

## 9. Lo que se vio antes de la serie
- **§0–§8 quedaron con sha 9705085a16ca026f a las 21:54:32**, con el humo recién empezado y antes de leer cualquiera de sus corridas.
  Después sólo se agregaron el orden de los trabajos (§5), la línea del sha del runner (§0) y esta sección.
- **Calibración** (§3).
- **Humo** (29001, TL de la serie, 5 brazos × 2 mundos, un proceso, 732 s; `datos/humo/v01_humo_20260924_215337/`): una semilla, sin
  valor de veredicto.
  - Costo: 73 s por corrida en promedio (quieto 76–97 s, onda 56–62 s), con el arnés corriendo en paralelo parte del tiempo.
  - Fenotipo idéntico:

    | mundo | SIN_SOS | ROBUSTA | PERILLAS | MUT0 | AZAR |
    |---|---|---|---|---|---|
    | quieto | 0.80 | 0.72 | 0.29 | 1.0 | 0.84 |
    | onda | 0.67 | 0.71 | 0.32 | 1.0 | 0.81 |

    La diferencia SIN_SOS − ROBUSTA en quieto es +0.08 en una semilla. La tolerancia de §3 se aplica a las medianas de la serie.
  - nac solo en quieto: SIN_SOS 114, PERILLAS 56, ROBUSTA 56, MUT0 60, AZAR 47.
  - nac solo en onda: 31, 28, 22, 25, 37.
  - Banco en el corte (quieto, SIN_SOS): **el 74.5 % de las cintas lleva un `EJE 2` con d < 0**, y dote, rep_umbral, rep_X y tau_e
    quedan en −0.335 en log. PERILLAS y ROBUSTA: ±0.01.
    - Es el mecanismo apostado en §7, escrito antes de leerlo, pero con UNA semilla.
    - En onda (SIN_SOS) no aparece: 0.000.
- Nada de lo visto cambió la letra ni las predicciones.

## ERR-142 (coordinador, 24-sep ~22:25, ANTES de la serie; auditoría juaco-auditor: LISTO CON CORRECCIONES)
- (a) La cláusula de HAY ALGO MODESTO "P1 pasa en los dos mundos pero cae una guardia" (§6) la agregó el creador por su cuenta. Cambia
  la forma del criterio, así que lleva ERR por la regla 11. Queda aceptada tal cual: sólo puede bajar un FUNCIONA a MODESTO, nunca
  subir.
- (b) Después del humo el runner cambió (sha del humo c8949ac3f9c6123f → sha de la serie b835e4c4a94e6355): el orden de los trabajos,
  la guardia AZAR "no medida" (ya anticipada en §5 antes del humo) y el descriptivo de `--lee`. Ninguno toca umbrales ni la medida de
  P1. Se registran aquí.
- Verificado por el coordinador antes de la serie: `construye_v01.py` da el sha 8a67a259baa5454b y el arnés 11/11 (274.8 s). Las
  semillas de calibración (29901–29906) no se solapan con la serie ni con la réplica.
