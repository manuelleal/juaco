# Organismo artificial — Registro experimental, Etapas 1 y 2

Fecha: 15 sep 2026. Autores: Christiam Puentes (dirección, hipótesis) y Claude (implementación, análisis).
Todo corre en CPU con Python/NumPy. Cada experimento cambia UNA variable respecto al anterior.

## Organismo (común a todas las versiones desde v4)

- Mundo: anillo de 40 celdas, 4 objetos (A o B al 50%), renovación estocástica (p=0.003/paso).
- Sensores: retina 6 px del objeto más cercano, dirección izq/der (winner-take-all), "estoy encima", hambre (interocepción).
- Patas: 2 motores con inhibición mutua, camino directo, R-STDP con traza de elegibilidad; aprenden de premio y de curiosidad (acercarse), NUNCA de castigo.
- Boca: circuito separado. Decide morder solo estando encima. Expansión dispersa (30 celdas de Kenyon, 3 ganadoras) antes de la decisión. Sesgo fijo +0.5, impulso por hambre.
- Energía: cuesta 0.002/paso; comida +0.8; veneno −0.4 y R=−3; comida R=+1. Muerte: energía a 0.6, posición aleatoria, memoria intacta.
- Sin backpropagation. Sin gradiente global.

## Etapa 1 — Aprendizaje A/B (v4, hash 786c7bc9258edecf)

20 semillas × 100k pasos, condiciones A (sin aprendizaje) y B (con aprendizaje).

| | comida | veneno Q1 | veneno Q4 | ratio Q4 | muertes | Wb·B |
|---|---|---|---|---|---|---|
| sin aprendizaje (mediana) | 1452 | 384 | 351 | 1.02 | 224 | 0 |
| con aprendizaje (mediana) | 264 | 13 | 2 | 32.5 | 148 | −5.37 (sd 0.33) |

- 20/20 reducen veneno de Q1 a Q4; 19/20 con ratio > 5. **Una semilla falló** (comida 25, 323 muertes): probable congelamiento por miedo generalizado. Abierto.
- El organismo que aprende come 6× menos que el azar: sobrevive por prudencia, no por eficiencia. La métrica correcta es muertes, no comida.

## Etapa 2 — Inversión del mundo (A↔B en el paso 50.000), 12 semillas, 100k pasos

Criterios. Inversión de A: mordidas de A en Q4 ≤ ½ de Q3 y Wb·A < 0. Extinción de B: come B en Q4 y Wb·B ≥ ½ de su valor pre-inversión.

| Etapa | Cambio único | Invierte A | Extingue B | Hallazgo |
|---|---|---|---|---|
| 2 (v4) | — | 1/12 | 0/12 | Dos fallos: hábitos confiados no reciben castigo; miedo no se extingue sin exposición |
| 2A | quitar factor (mordió−pb) de la boca | **12/12** | 0/12 | Reversa de A resuelta (t≈4.800 pasos). Regla aprende más fuerte en ambos sentidos |
| 2B | hambre no lineal 2h+4h⁴ | 12/12 | 0/12 | Más exposición (9/12 muerden B) pero más castigo previo: Wb·B llega a −8 |
| 2C | aversión 3→1 | 12/12 | 0/12 | Extinción incipiente en 2 semillas; reversa de A 2× más lenta |
| **2D (=v5)** | Kenyon sin celdas compartidas A/B | 12/12 | 0/12 | Elimina desplome de Wb·B en Q3 (castigo a A se filtraba a B). Correlación 7/7 vs 5/5, sin excepciones |
| 2E | 2D + hambre no lineal | 12/12 | 0/12 | Exposición hasta 25 mordidas; tasa de extinción ≈0.08/mordida; deuda inicial triplicada |
| 2F | apetitivo y aversivo separados | **0/12** | **2/12** | Primera extinción real (404 y 319 mordidas de B, aversivo intacto). Reversa de A rota por saturación |
| **2G** | error de predicción por estímulo, delta = R − (Wp−Wn)·kc | 0/12* | **12/12** | Valores convergen exactamente a la recompensa (Wb·A→−3.00, Wb·B→+1.00) en 600–2.200 pasos. Muertes 145 (mínimo). *Falla el criterio de conducta, no el de valor: la política (+0.5, 2·h, T=0.3) deja morder A con hambre alta |
| 2H | α=1.2 en la decisión (preregistrado: 1.06≤α≤1.29) | 0/12 | 12/12 | Refutada por conteo (A veneno Q4: 12–22, criterio ≤5). La tasa por visita coincide con la analítica (0.1%→4% según hambre). Error metodológico: α derivado de tasas por visita, criterio escrito en conteos; 4.000 visitas/cuarto |

### Tres capas separadas empíricamente (2G/2H)
1. Representación: qué estímulo veo (Kenyon, 2D).
2. Valor aprendido: cuánto vale (2G: exacto, ±R).
3. Política: qué hago con el valor bajo hambre (2H: abierta).
En 2G el valor es correcto y la conducta no es óptima respecto a él. Son problemas distintos y se miden distinto.

### Cadena causal establecida
1. Reversibilidad de un hábito apetitivo: la da la regla sin bloqueo de sorpresa (2A).
2. El desplome del miedo a B al invertir era filtración por códigos solapados (2D).
3. Ni saturación (2C) ni exploración (2B, 2E) explican la ausencia de extinción con un solo peso.
4. Con un solo peso por celda, extinguir = borrar, a 0.08 por exposición: no alcanza en una vida.
5. Con dos pesos (2F) la extinción ocurre por competencia sin borrar el miedo, pero la falta de predicción por estímulo (delta = R − Rbar global) hace que el apetitivo crezca sin freno hasta saturar y anular la reversa de A.
6. Con predicción por estímulo (2G, Rescorla-Wagner) el aprendizaje de valor queda resuelto: convergencia exacta, extinción 12/12, reversa de valor 12/12. Lo que resta es política.

### Limitación metodológica
Las soluciones (STDP, RPE, Kenyon, apetitivo/aversivo, Rescorla-Wagner) fueron elegidas conociendo la literatura. Lo que el organismo dictó fue la NECESIDAD de cada mecanismo (quitarlo rompe algo medible); la forma concreta de la solución tuvo guía teórica. Defendible: necesidad; no defendible: descubrimiento a ciegas.

### Baseline v5 (2D limpio, hash aed3797d747ab3b7)
20 semillas: 20/20 aprenden, ratio Q4 mediana 48, muertes 150 vs 226, Wb·B mediana −4.84. Sin fallos (la semilla congelada de v4 no reaparece; n=20, no concluyente).

## Parámetros puestos a mano (hipótesis, no hallazgos)
Asimetría R (+1/−3); aversión; sesgo de la boca +0.5; impulso por hambre; energía tras muerte (0.6); costo por paso; tasa de renovación del mundo; clip ±3 por celda; k=3 ganadoras; NK=30; eta; tau de elegibilidad.

## Pregunta abierta para la próxima sesión (antes de 2H bis)
Qué criterio de conducta le exigimos a la política: tasa de mordida por visita condicionada al hambre (mecanicista, lo que α controla) o conteo absoluto de mordidas de veneno (funcional, lo que el organismo sufre). Decidirlo ANTES de tocar α o β. No recalibrar α a posteriori: las restricciones preregistradas (P≤5% a h=0.9; P≥1% a h=1.0) son incompatibles con ≤5 mordidas/cuarto a 4.000 visitas; una de las dos exigencias estaba mal planteada.

## Archivos
organismo_baseline_v4.py, baseline_v4.csv, organismo_v5.py, baseline_v5.csv, etapa2a…2h_inst.py, etapa2_2A_a_2H.csv (108 corridas).

---

## Día 2 (16 sep 2026) — cierre de 2I/2J, ANOM-01, v6

### Bug corregido: sincronía sensor-acción (afecta v4–2I)
La boca decidía con el patrón del objeto más cercano ANTES de moverse. Efecto medido: 25% de las decisiones sobre comida usaban el código del veneno (tasa de mordida de A 65–75% vs 99.7% predicha); 1.8% del total de decisiones. Corregido en `etapa2h_fix.py` y en v6. Al repetir 2H con la corrección, la conclusión no cambió (A veneno Q4: 10–23; refutación por conteo se mantiene); W_B pasó a converger exactamente a +1.00. Descubierto por discrepancia entre tasa predicha y observada.

### 2I — estímulo nuevo C (veneno) en t=50k, boca corregida
Archivo `etapa2i_fix.py`, datos `etapa2i_fix.json`. 12 semillas, T=100k, α=1.2, aversión=1, A∩B=0 forzado, C∩A y C∩B libres.
Hipótesis: aprende C sin degradar A/B. **Sostenida 12/12** en las tres celdas (tasa A por visita 100%→100%; tasa B 0.3%→0.0–0.5%; W_C→−2.9, tasa C 1.1–3.1%→0.3–0.7%).
Interferencia: ΔW_B(Q2→Q4) = −0.55 con C∩B>0 (n=6) vs −0.02 sin (n=6); ΔW_A = −0.02 con C∩A>0 (n=4) vs 0.00 sin (n=8). A∩B=0 en 12/12 (control). Misma valencia: deriva no corregida porque B no se re-muestrea.
Corrección de criterio: el consumo absoluto de A cayó ~45% por disponibilidad (A pasa de ½ a ⅓ del mundo); normalizado por visitas se conserva 10/12 (12/12 con boca corregida).

### ANOM-01 — resuelta: artefacto de instrumentación
La serie "semilla 1" con caída W_A 1.00→0.52 era la serie de la semilla 12 (aliasing de una lista mutable reutilizada entre semillas). Auditoría de la semilla 1 real: 17 mordidas de A entre 50k y 60k, todas con pred=1.0, dlt=0.0, Wp·A=1.0, Wn·A=0.0. La caída de la semilla 12 sí existe y se explica por C∩A=1 (castigo a C entra por la celda compartida; RW la recupera a 0.98). **No hay mecanismo no identificado.** Tercer error de instrumentación/criterio del proyecto (unidades en 2H, disponibilidad en 2I, aliasing aquí).

### 2J — D comida con D∩B=1 (valencias opuestas) vs control D∩B=0
Archivo `etapa2j.py`, datos `etapa2j.json`. 12 semillas × 2 condiciones. Predicción preregistrada (escala 2I): ΔW_B ≈ +0.5. **Refutada**: ΔW_B = +0.05 (rango +0.02..+0.10) vs −0.02 control. W_D→+1.00 en ambos.
Mecanismo (idéntico en 12/12): canales inflados. D: Wp/Wn = 2.22/1.22 (control 1.00/0.00); B: 0.74/3.67 (control 0/3). Valores netos correctos a costa de representación. Con valencia opuesta el organismo re-muestrea el estímulo contaminado y RW corrige; con la misma valencia (2I) no. La escala 0.53/celda era la de una deriva sin corrección, no una constante. Costo: D arranca negativo en 2/12 (−0.14, −0.51 a 55k): miedo transitorio a comida.

### 2K — D∩B=2 (ejecutado ANTES de cerrar 2I/2J — error de orden, se registra igual)
Predicción (choque con clip): **refutada** por error aritmético mío: techo por canal es 3 celdas×3 = 9, no 3. Resultado 12/12 valores correctos con degradación graduada: W_B −3.0→−2.78, W_D 0.95; canales D 5.1/4.1, B 3.4/6.2; miedo transitorio a D hasta −0.94. Pendiente graduada en 0/1/2 celdas. En el rango probado el efecto crece con el solapamiento (no se afirma universal).
**2K-bis (abierta, sin correr)**: qué ocurre cuando la demanda de representación se aproxima al techo de capacidad — 3 celdas compartidas (códigos idénticos) y/o clip reducido. Hipótesis derivada del organismo, no de la literatura.

### v6 — consolidación (hash organismo_v6.py 5f38f83cf49248a3; bateria.py 1add9e6f85e97978)
Un archivo, escenarios como parámetros (invertir_en, nuevo, nuevo_val, solap_B). Incluye: regla sin bloqueo (2A), aversión=1 (2C), A∩B=0 (2D), canales separados (2F), RW por estímulo (2G), α=1.2 (2H), sincronía corregida.
Parámetros: L=40, NK=30, K=3, eta=.03, tau_e=.85, hambre_boca=2.0, sesgo boca +0.5, T_boca=0.3, costo=.002, nobj=4, renovación p=.003, E tras muerte 0.6, clip 3/celda, R=+1/−3, ΔE=+0.8/−0.4.
Batería de regresión (6 semillas): E1, E2 inversión, E2I, E2J, E2K — todas PASAN.

### Baseline v6 — 20 semillas (baseline_v6.csv, hash 3ffde98fd346a659)
| | comida A | veneno B Q1 | veneno B Q4 | tasa B Q4 | tasa A Q4 | muertes | W_A | W_B |
|---|---|---|---|---|---|---|---|---|
| sin aprendizaje | 1400 | 334 | 370 | 89.7% | 88.9% | 218 (193–417) | 0 | 0 |
| con aprendizaje | 338 | 38 | 13 | 0.29% | 100% | 142 (130–175) | +1.00 | −3.00 |
20/20 en los tres criterios; sin fallos. Este es el baseline de referencia del artículo.

### Cadena experimental (para el texto)
2F memorias paralelas → 2G predicción específica → 2H política separada del aprendizaje → 2I aprendizaje continuo con interferencia medible → 2J conflicto de valencias bajo representación compartida → 2K-bis (abierta) capacidad representacional.

### Problema abierto único de conducta
Política bajo hambre: con valor −3 el organismo muerde veneno 0.1% (hambre baja) → 1–4% (inanición) por visita. Criterio adoptado: tasa por visita condicionada al hambre. No recalibrar α a posteriori.

---

## Día 2, tarde — 2L (plasticidad estructural) y rama 2M (pulpo)

### 2L — Un mecanismo que aparece sin ponerlo (candidato a v7)
Hipótesis (derivada del propio proyecto): 5 de los 15 mecanismos añadidos a mano (inhibición lateral, WTA, Kenyon, canales,
predictor por estímulo) son la misma operación — separar dos cosas que comparten canal y necesitan valores distintos — y en
todos los casos la señal fue un error de predicción que no bajaba. Regla local propuesta: cada celda de Kenyon lleva una media
móvil del |error de predicción| cuando participa en una mordida y una media de los patrones que ve; si el error supera θ=0.6,
la celda se divide: recluta una celda dormida (pool 30→90), la hija copia Wp/Wn y desplaza su código de entrada hacia lo
DISTINTIVO del patrón actual (P − media de lo que suele ver), la madre se desplaza en dirección contraria.
- **v1 (`plasticidad.py`) REFUTADA**: hija desplazada hacia el patrón completo → dominada por el píxel compartido → solapamiento
  2→3, valores a 0, 60 divisiones. Dirección de división equivocada.
- **v2 (`plasticidad2.py`) SOSTENIDA**, 8 semillas: con A∩B forzado=3 (códigos idénticos; v6 colapsa: W=0, 4.700 venenos),
  el organismo separa solo: solapamiento 3→0 antes de 25k pasos, W_A +1.00, W_B −3.00, 6–9 divisiones, veneno 90, muertes 150.
  Con A∩B=2: 8/8 en valor; 4/8 dejan una celda compartida (separación de valor sí, representacional incompleta).
- **v7 candidato (`organismo_v7c.py`, hash 212f0746d52577c7) = v6 + 2L v2.** Batería completa (`bateria_v7c.py`, 21b97967e48ed971),
  6 semillas: E1, E2, 2I, 2J, 2K → todas PASAN 6/6; E2L rescate A∩B=3 → 6/6 (solap→0); control sin plasticidad → 0/6.
  ~~**Divisiones en etapas normales: 0 en 6/6** — la regla no dispara sin error crónico.~~
  **CORREGIDO (ERR-05, día 3): FALSO.** 0 sólo en E1, E2I y E2J; E2 da 3–5 divisiones y E2K da 2–4, en 6/6 semillas.
  Enunciado correcto: la regla no dispara sin error de predicción crónico; cuando lo hay, dispara sobre el estímulo
  que lo causa y nunca antes del evento. Ver sección "Día 3".
- Honestidad: la regla de división la escribimos nosotros; lo que emerge es DÓNDE y CUÁNDO se aplica. La corrección v1→v2 es
  aprendizaje competitivo clásico. No genera canales (la otra mitad de la lista: motivación/cuerpo) — eso sigue abierto.
- Errores de proceso: primera "batería v7" era v6 con otro título (import sin cambiar); caché de Python. Cuarta vez que el
  instrumento engaña. Lección: verificar QUÉ corre antes de leer QUÉ salió.
- **Pendiente**: v7 se congela solo si pasa la batería con 20 semillas en el repo.

### 2M — Rama: pulpo (evaluadores distribuidos) — REFUTADA a esta escala, NO entra al tronco
`experimentos/ramas/pulpo_2M.py`. 6 estímulos (3 comida, 3 veneno). Central 1×60 celdas vs 2×30 vs 3×20; el centro deja
actuar y aprender al brazo con mayor |valor|. 8 semillas. Resultado: central iguala o supera (error de valor 0.13 vs 0.10 vs 0.63;
veneno Q4 21 vs 24 vs 64). Hallazgo secundario: **especialización emergente 100%** (cada estímulo con brazo dueño >80%) sin
asignación. Fallo: especialización prematura sin corrección cruzada (brazo equivocado se queda: misma aritmética de 2I).
Pregunta abierta (sin correr): a cuántos estímulos se cruza la curva central/distribuida. Es rama, no tronco.

### Argumento de convergencia (para el texto)
Mosca (cuerpo fungiforme), pulpo (lóbulo vertical) y vertebrados (hipocampo/cerebelo) llegaron por separado a la misma
arquitectura: expansión → código disperso → plasticidad en la salida. Nuestro organismo también, forzado por sus fallas.
Fortalece la afirmación de NECESIDAD del diseño (la defendible) frente a la de descubrimiento a ciegas (la no defendible).

---

## Día 3 — Traspaso al repo (Claude Code, Windows). Fase 0 cerrada y corrección de un dato del registro

Fecha de sistema: 15 sep 2026. (El registro fecha las sesiones previas como 15–16 sep; se deja constancia de la
inconsistencia sin resolverla, porque no afecta a ningún resultado.)
Entorno: Windows 11, Python 3.14.2, NumPy 2.4.3, 16 núcleos. **1 corrida de 100k pasos = 4.0 s.**

### Fase 0 — traspaso VALIDADO
- Hashes verificados 4/4 contra MANIFEST: organismo_v6.py `5f38f83cf49248a3`, bateria.py `1add9e6f85e97978`,
  organismo_v7c.py `212f0746d52577c7`, bateria_v7c.py `21b97967e48ed971`; baseline_v6.csv `3ffde98fd346a659`.
- `bateria.py 6` → PASA 5/5 etapas 6/6. `bateria.py 20` → **PASA 5/5 etapas, 20/20 semillas.**
- **Reproducción exacta del baseline**: semillas 1–3 en ambas condiciones, 45/48 campos idénticos a `baseline_v6.csv`.
  Las 3 diferencias son `tasaA_q4` guardada con 1 decimal en el CSV original (92.00 vs 92.02 recalculado).
  Mordidas, muertes, W_A y W_B coinciden bit a bit con NumPy 2.4.3. El traspaso no cambió ningún número.
- `git init`, commit inicial, tag `v6-baseline`. Se añadió `.gitattributes` con `* -text`: git iba a convertir
  LF→CRLF y **eso habría roto todos los hashes sha256 en cualquier clon**. Verificado post-commit: los 4 hashes intactos.

### ERR-05 — quinto error de instrumento: "divisiones = 0 en etapas normales" es FALSO
El registro del día 2 afirma: *"Divisiones en etapas normales: 0 en 6/6 — la regla no dispara sin error crónico"*.
`bateria_v7c.py` **no mide splits en ninguna etapa**, así que la afirmación no venía de la batería. Medido ahora:

| Etapa | splits (semillas 1–6) | celdas |
|---|---|---|
| E1 | 0 0 0 0 0 0 | 30 |
| E2 inversión | **5 5 5 3 3 5** | 33–35 |
| E2I | 0 0 0 0 0 0 | 30 |
| E2J | 0 0 0 0 0 0 | 30 |
| E2K (D∩B=2) | **2 2 2 2 4 2** | 32–34 |

Instrumento verificado primero (regla 5): registrado el paso de cada división. Ninguna ocurre antes del evento.
- E2 (inversión en t=50.000): divisiones en t≈52.700–54.600, y **en orden** — primero B (3 divisiones, el que pasó
  a ser comida) y ~700 pasos después A (2 divisiones).
- E2K (D entra en t=50.000): divisiones en t≈52.900–53.800, **todas sobre D**, el estímulo solapado.
- E1: cero.

Origen probable: el `Historial..md` documenta que la primera "batería v7" era v6 con el import sin cambiar, y **v6 no
tiene divisiones en ninguna etapa**. "0 en 6/6" es, con alta probabilidad, residuo de esa corrida. Encaja con el patrón
de los cuatro errores anteriores (unidades 2H, disponibilidad 2I, aliasing ANOM-01, aritmética del techo 2K).

**El hallazgo mejora el mecanismo, no lo empeora.** El enunciado correcto es más fuerte y más falsable:
*la regla no dispara sin error de predicción crónico; cuando lo hay, dispara sobre el estímulo que lo causa y nunca
antes del evento.* Se corrige en consecuencia la afirmación del día 2.

### organismo_v7.py — instrumentación inerte (hash `3db0475ef0ea95ce`)
= `organismo_v7c.py` + registro de `split_t` (paso y estímulo de cada división). Diff de 4 líneas, 3 funcionales,
sin una sola llamada nueva al RNG. **Equivalencia verificada: 21/21 escenarios × semillas idénticos a v7c** en todos
los campos. Se usa para poder evaluar el criterio temporal; v7c queda intacto con su hash.

### Criterio de congelación de v7 — PREREGISTRADO antes de correr 20 semillas
`bateria_v7.py`. Corrige dos defectos de `bateria_v7c.py`:
(a) su etapa "control sin plasticidad" llevaba los mismos criterios de éxito que el rescate, de modo que su resultado
correcto era FALLA: con esa redacción "todo PASA" era insatisfacible y **v7 no podía congelarse nunca**;
(b) `PLAN.md` exigía "divisiones=0 en etapas normales", que es el dato falso de ERR-05 y que además la batería no medía.

v7 se congela si y sólo si, con 20 semillas:
1. E1, E2, E2I, E2J, E2K pasan 20/20 los criterios idénticos a v6.
2. E2L rescate (A∩B=3) pasa 20/20: separa solo, W_A=+1, W_B=−3, solapamiento→0.
3. `splits == 0` en E1, E2I, E2J (20/20).
4. `splits > 0` en E2 y E2K (20/20) **y todas las divisiones en t > 50.000** (20/20).
5. `celdas ≤ 45` en todas las etapas (20/20).
6. El control sin plasticidad **FALLA** (≤1/20 lo pasa). Si pasara, la plasticidad no aporta nada.
Si algo falla, 2L vuelve a hipótesis y v6 sigue siendo el tronco. No se recalibra a posteriori.

### Examen de congelación de v7, 20 semillas — RESULTADO: NO SE CONGELA
`bateria_v7.py 20`. Todos los criterios científicos heredados pasan 20/20 (W_C≤−2.5, W_A≈+1, W_B≤−2.8, tasaA,
W_D, reversa, extinción, rescate A∩B=3, solapamiento→0, celdas≤45 en todas). El control negativo es válido:
0/20 lo pasan, W_A y W_B colapsan a 0.00 sin plasticidad.

**Falla un único criterio: `splits==0` en E2I, 19/20.** La semilla 15 divide 3 veces: dos sobre A en t=53.904
y una sobre C en t=57.059. Bajo el criterio preregistrado esta mañana, v7 NO se congela. 2L vuelve a hipótesis
y v6 sigue siendo el tronco.

### ERR-06 — sexto error de instrumento, y es del día 3 (mío)
Diagnóstico de la semilla 15 (regla 5: primero el instrumento). Replicado el sorteo de códigos de las 20 semillas:

| Solapamiento con A | semillas | splits |
|---|---|---|
| C∩A = 0 | 13 | 0 |
| C∩A = 1 | 6 (2,5,11,12,13,20) | 0 |
| **C∩A = 2** | **1 (la 15)** | **3** |

**El criterio estaba mal escrito.** `E2I` se invoca como `run(s, nuevo='C')` con `solap_B=None`, de modo que la
condición de sorteo **sólo exige A∩B=0 y deja C∩A y C∩B libres**. E2I no es una etapa sin error crónico: es una
etapa donde el solapamiento sale por sorteo. Lo escribí a partir de 6 semillas y ninguna de las 6 sacó un 2.
Mismo tipo de error que 2H (α derivado en tasas, criterio escrito en conteos): una premisa de hecho falsa dentro
del criterio. El registro ya documentaba el mecanismo en 2I ("ΔW_B = −0.55 con C∩B>0 vs −0.02 sin") — la
información para escribirlo bien estaba disponible y no la usé.

La semilla 15 NO es un fallo del organismo: es la regla respondiendo al castigo de C filtrado por dos celdas
compartidas con A, exactamente para lo que fue diseñada, y recuperando después (W_A≈+1 se cumple 20/20).

### HALLAZGO — umbral de disparo de la regla 2L en 2 celdas compartidas
Del fallo sale una cifra que el registro no tenía. Seis condiciones independientes, todas consistentes:

| Condición | solapamiento | splits |
|---|---|---|
| E1 | 0 | 0/20 |
| E2J (D∩B=1 forzado) | 1 | 0/20 |
| E2I, semillas con C∩A≤1 | 0–1 | 0/19 |
| E2I, semilla 15 | 2 | 3 |
| E2K (D∩B=2 forzado) | 2 | 20/20 |
| E2L (A∩B=3 forzado) | 3 | 20/20 |

**Con 0 o 1 celda compartida la regla nunca dispara; con 2 o 3 dispara siempre.** El umbral es una consecuencia
medible de θ=0.6 sobre la media móvil del |error|, no un parámetro puesto a mano. Encaja con la degradación
graduada ya medida en 2K (W_B −3.00 / −2.9 / −2.78 con 0/1/2 celdas): a 1 celda el error se absorbe, a 2 no.
E2 (inversión) dispara sin solapamiento alguno: el error crónico también puede venir del valor, no sólo de la
representación. Son dos vías distintas al mismo disparador.

### Criterio de congelación de v7, VERSIÓN 2 — preregistrado tras ERR-06, antes de volver a correr
Regla 3: el criterio estaba mal, se registra el error y se decide uno nuevo ANTES de volver a correr. El nuevo
criterio es **más exigente**, porque predice por semilla y no por etapa, y porque añade una predicción que puede
fallar (el umbral):

1. Los criterios científicos heredados: 20/20 en E1, E2, E2I, E2J, E2K y E2L rescate (idénticos a v6).
2. `celdas ≤ 45` en todas las etapas, 20/20.
3. El control sin plasticidad FALLA (≤1/20).
4. **Criterio de disparo, evaluado por semilla contra el solapamiento MEDIDO, no contra el nombre de la etapa**:
   - solapamiento máximo ≤1 y sin inversión → `splits == 0`
   - solapamiento máximo ≥2, o inversión del mundo → `splits > 0` y todas las divisiones en t > 50.000
   Debe cumplirse en 20/20 semillas de cada etapa.
5. **Predicción del umbral, falsable**: en un barrido forzado de solapamiento 0,1,2,3 (2K-bis), la fracción de
   semillas que divide debe ser 0 en 0 y 1, y 1 en 2 y 3. Si alguna semilla divide con solapamiento 1, o alguna
   no divide con solapamiento 2, el umbral no está en 2 y la afirmación se retira.

### Etapa 3 — Generalización. PREREGISTRO (escrito ANTES de correr, día 3)
Punto 10 del brief. Principio rector: "primero que aprende, después que recuerda, después que generaliza". Nivel 4 de
la escala del punto 6, hoy con "indicios" (2I/2J) y sin criterio propio.

**Hipótesis.** Lo que el organismo generaliza está determinado por el solapamiento de códigos Kenyon y por nada más.
La similitud visual en la retina no tiene papel independiente.

**Diseño.** Medición pura, sin mecanismo nuevo y sin tocar v6. Se corre E1 normal hasta convergencia (W_A=+1.00,
W_B=−3.00) y se SONDEA: para cada uno de los 64 patrones binarios de 6 píxeles se lee el valor a priori
W_X = (Wp−Wn)·kenyon(X) **sin que el organismo los haya visto ni mordido nunca**. 20 semillas.
Requiere `organismo_v6_sonda.py` = v6 + devolución de Wp, Wn, KW al final (instrumentación inerte, con prueba de
equivalencia frente a v6 como la que se hizo para v7).

**Predicción numérica, derivada y exacta.** Tras converger, cada celda de code(A) vale +1/3 neto y cada celda de
code(B) vale −1 neto. Por tanto, con nA = |code(X)∩code(A)| y nB = |code(X)∩code(B)|:

        W_X = (nA/3)·W_A + (nB/3)·W_B = 0.333·nA − 1.0·nB

**Criterios.**
- Sostenida si |W_X observado − W_X predicho| < 0.15 en ≥90% de los pares (patrón × semilla).
- Y si la correlación parcial de W_X con la similitud visual a A (píxeles compartidos / distancia de Hamming),
  controlando nA y nB, cumple |r| < 0.2.
- **Refutada** si la similitud visual predice W_X mejor que el solapamiento, o si el residuo del modelo tiene
  estructura sistemática. Eso significaría que el Kenyon no hace lo que creemos.

**Métrica de alcance (la que importa para el nivel 4).** Fracción de los 64 patrones con nA = nB = 0, para los que la
predicción es W_X = 0 exacto: el organismo no generaliza NADA hacia ellos. Cuantifica el límite duro de esta
arquitectura: se generaliza compartiendo celdas o no se generaliza en absoluto.

**Qué NO prueba.** Que el valor a priori sea correcto no dice nada sobre si el organismo ACTÚA según él, ni sobre
aprendizaje de características abstractas. Es generalización de valor por representación, y sólo eso.

### ERR-08 — tercer criterio mal escrito del día 3, y el patrón que lo produce
Al implementar el criterio v2 en `bateria_v7b.py` (hash al pie), dos defectos más, los dos míos, los dos cazados
por autoverificación antes de correr 20 semillas:

1. **El solapamiento que hay que leer es el INICIAL, no el final.** `organismo_v7.run` devuelve `solap` calculado
   al terminar, con la KW ya modificada por la plasticidad. El criterio 4 necesita el solapamiento con el que el
   organismo NACE, que es el que predice si cabe esperar error crónico. En E2L la diferencia es justo la medida
   del éxito: inicial 3, final 0. La batería replica el sorteo de KW sin simular y **se autoverifica** contra el
   organismo en las semillas sin divisiones (donde inicial = final); ahí saltó el fallo.
2. **"todas las divisiones en t > 50.000" es falso para E2L.** El criterio v2 asumía que el error crónico siempre
   lo crea un evento a mitad de corrida. En E2L el solapamiento es **congénito**: A y B nacen con códigos idénticos
   y la separación debe ocurrir PRONTO, no tarde. El propio registro ya lo decía ("solapamiento 3→0 antes de 25k
   pasos") y no lo usé al escribir el criterio.

**Corrección**: el disparo se ancla a la CAUSA, no a un reloj fijo. `t_causa = 0` si el solapamiento es congénito,
`t_causa = 50.000` si lo crea un evento (inversión o estímulo nuevo); ninguna división antes de su causa; y para el
caso congénito, la separación debe **completarse** antes de t=25.000 — umbral tomado del registro previo, no
elegido hoy a la vista de estos datos.

**El patrón, que importa más que los dos errores.** ERR-06 y ERR-08 tienen la misma raíz: **escribir un criterio
que da por hecho que todas las etapas se comportan igual, en vez de mirar qué hace cada una.** Tres veces en un día.
Los cuatro errores anteriores del proyecto (unidades, disponibilidad, aliasing, aritmética) eran de medición; estos
son de *generalización indebida al redactar el criterio*, que es una familia distinta y hasta hoy no identificada.
Regla derivada, para las próximas baterías: **un criterio que se aplica a N etapas debe justificarse etapa por
etapa antes de correr, o escribirse en términos del mecanismo (la causa) y no del escenario (el reloj).**

### Fase 1 — infraestructura paralela. HECHA
`experimentos/run_etapa.py` (`a3d6dad063eb809d`) y `experimentos/analiza.py`. Pool de procesos con método `spawn`,
cabecera de procedencia obligatoria (fecha, hash del organismo, hash del script, versiones de Python y NumPy, kwargs
completos), y nunca sobrescribe un archivo.
- **Equivalencia paralelo vs secuencial: 20/20 semillas idénticas bit a bit.** El paralelismo no cambia un número.
- Contra `baseline_v6.csv`: **259 de 260 celdas idénticas**. La única discrepancia es el redondeo de `tasaA_q4`
  a 1 decimal en el CSV original; corroboración independiente de lo hallado esta mañana.
- Medianas reproducidas exactamente: comida 338, venenoB_q4 13, muertes 142, W_A +1.00, W_B −3.00.
- **20 semillas: 79.7 s secuencial → 12.7 s paralelo (6.3×).** 100 semillas caben en ~60 s. El barrido de política
  2P pasa de ~96 min a minutos. Queda desbloqueado el "100 semillas pendiente" del punto 8 del brief.

### Variabilidad y diversidad — primeras mediciones (punto 8, marcadas pendientes desde el brief)
Definiciones nuevas, marcadas como PROPUESTAS en el docstring de `analiza.py`, no como hechos establecidos.
Variabilidad = dispersión entre semillas; diversidad = distancia euclídea media por pares entre vectores de conducta
z-scoreados. E1, 20 semillas:

| | valor |
|---|---|
| CV(muertes) | 0.081 |
| CV(comidaA) | 0.072 |
| CV(venenoB) | 0.088 |
| **sd(W_A)** | **0.0000** |
| **sd(W_B)** | **0.0022** |
| diversidad (distancia por pares) | mediana 2.78, rango 0.44–8.85; 1.28 por dimensión (ref. 1.414) |

**El valor aprendido tiene diversidad cero.** Con 20 sorteos distintos de la capa Kenyon, la conducta varía (CV 7–9%)
y el valor converge siempre al mismo número exacto. Separa las tres capas del proyecto con una cifra: representación
azarosa, política ruidosa, **valor determinista**. `W_A` hubo que descartarlo del cálculo de diversidad por sd=0, y
ese descarte es en sí el resultado.

### Aclaración de medida — "velocidad de aprendizaje" nombraba dos cosas distintas
El registro dice que la reversa de A se resuelve en t≈4.800 pasos (2A). Con criterio literal de convergencia
(|W − asíntota| < 0.1 sostenido) la medida da **25.750 pasos** (mediana). No es contradicción ni error de nadie:
la cola asintótica está limitada por **exposición**, no por tasa de aprendizaje — un estímulo temido casi no se
re-muestrea, así que los últimos décimos de W tardan por falta de visitas. Con t90 (90% del cambio total) salen
**8.250 pasos**, del orden del registro. A partir de ahora se reportan las dos: **t90** (aprendizaje) y
**t_convergencia** (aprendizaje + disponibilidad). Son magnitudes distintas y llevaban el mismo nombre.

### ETAPA 3 — Generalización. RESULTADO: predicción SOSTENIDA, y el diseño era demasiado fácil
Datos: `datos/etapa3_generalizacion_20260915_112340.csv/.json`. 20 semillas × 64 patrones = 1.280 pares.
Sonda `experimentos/etapa3/organismo_v6_sonda.py` (`8db4b85aeb33e7a2`), script `39f428bb0dc1cafc`.

- **Criterio 1 (preregistrado: |W_obs − W_pred| < 0.15 en ≥90%)**: cumplido en **100.00%** de los 1.280 pares.
  El residuo no es pequeño, es **exactamente 0.000**, rango [+0.000 .. +0.000].
- **Métrica de alcance**: **15.9%** de los pares tienen nA=nB=0 y por tanto W_obs = 0.000 exacto. A uno de cada seis
  patrones posibles el organismo no le asigna ningún valor: no generaliza nada hacia ellos.
- corr(W_obs, nB) = **−0.96** frente a corr(W_obs, nA) = **+0.59**: el veneno domina la generalización, como toca
  con |W_B|=3 contra |W_A|=1. La generalización del organismo está sesgada al miedo.

**AUTOCRÍTICA, regla 5 aplicada a mi propio resultado.** Un residuo de exactamente 0.000 en 1.280 pares no es una
confirmación fuerte: es señal de que la predicción era casi tautológica en este escenario. La razón es mecánica —
la regla RW actualiza `Wp += eta·dlt·kc`, o sea **suma lo mismo a las 3 celdas del código a la vez**, de modo que las
3 celdas de code(A) tienen pesos idénticos por construcción. Con A∩B=0 forzado y sin C ni D presentes en E1, la
identidad `W_X = (nA/3)·W_A + (nB/3)·W_B` no puede fallar. El experimento confirma el modelo pero no lo arriesga.

**Dónde está el contenido empírico (análisis completo, par canónico `etapa3_generalizacion_20260915_114117`).**
Separando lo tautológico de lo que sí arriesga:

| modelo de W_pred | % cumple C1 | \|residuo\| máx | qué es |
|---|---|---|---|
| con W_A, W_B **reales** de cada semilla | 100.00% | 2.2e-16 | **identidad algebraica, no podía fallar** |
| **nominal** 0.333·nA − 1.0·nB | 100.00% | 5.94e-3 | **empírico, y pasa con margen de 25×** |

Verificado mecánicamente por qué la primera no es falsable: `Wp−Wn` es *exactamente* uniforme dentro de code(A)
(0.333333/celda) y de code(B), y *exactamente* 0 en las 24 celdas restantes. Con A∩B=0 y sólo A y B mordidos, la
identidad está forzada. El residuo de 2.2e-16 es épsilon de máquina.

**La cifra que sí decide el criterio de refutación** ("refutada si la similitud visual predice mejor"):

| modelo | R² |
|---|---|
| W_obs ~ [nA, nB] (solapamiento de códigos) | **0.999999** |
| W_obs ~ [compartidos_A, compartidos_B] (píxeles) | 0.334 |
| W_obs ~ [hamming_A, hamming_B] | 0.323 |

El solapamiento explica prácticamente todo; la similitud visual, un tercio. **C2 sostenida** (parcial pooled
+0.027 y +0.003, criterio |r|<0.2) aunque es degenerada intra-semilla (0/20 dan r definido: el residuo tiene
std 3e-16). **C3 no refutada**: el residuo del modelo nominal tiene estructura (r con nB = +0.731) pero queda
explicada al 100% por el propio modelo — `residuo = (nA/3)(W_A−1) + (nB/3)(W_B+3)` con desviación máxima 1.85e-16,
o sea que viene sólo de que W_B converge a −2.9987 y no a −3.0000 exacto. No hay componente ajena al modelo.

**HALLAZGO con contenido real — el alcance de la generalización es una lotería del sorteo.**
Fracción de los 64 patrones con nA=nB=0 (valor a priori exactamente 0, alcance nulo): mediana **13.3%**,
rango **[2/64 .. 27/64]**. Conteo por semilla: 15,11,12,19,7,17,4,4,14,8,4,4,9,7,2,18,27,2,15,5.
**Varía 13.5× entre semillas.** Un organismo queda ciego al 42% de los patrones posibles y otro sólo al 3%,
con el mismo aprendizaje y la misma experiencia. La causa está medida: r(conteo, fuerza relativa de las 6 celdas
de code(A)∪code(B) frente a las otras 24) = −0.42. Verificado además que KW no cambia nunca en v6 (KW en T=4 es
idéntico a KW en T=100000): **el alcance es una propiedad de la proyección aleatoria, no del aprendizaje.**
Esto es motivación directa para la rama 3K (¿hace falta que la expansión aprenda?).

**ERR-07 — artefacto del patrón nulo.** Para X = 000000, `KW@X` es el vector cero y `np.argsort` sobre empates
devuelve 0..29 en orden, de modo que code(000000) = {27,28,29} en **las 20 semillas**, determinado por el desempate
del argsort y no por KW. Consecuencia: un patrón sin un solo píxel encendido puede heredar un valor a priori de
hasta **−2.000**. Son 20/1280 pares; excluirlo no cambia C1–C3 (100%→100%) y mueve el alcance de 0.133 a 0.119.
Marcado en la columna `es_patron_nulo` del CSV. Séptimo artefacto de instrumento del proyecto.

**Reproducibilidad**: dos corridas independientes produjeron CSV con **hash idéntico** (`4982abc26690989e`).
El par `..._112340` queda superado (su JSON contenía tokens `NaN`, no estrictos); el canónico es `..._114117`.
Equivalencia de la sonda: **18/18 escenarios × semillas idénticos** a v6.

**Conclusión que se sostiene**: en E1 la generalización está determinada por el solapamiento de códigos
(R²=0.999999) y no por la similitud visual (R²=0.33), y el alcance nulo —mediana 13.3%, rango 3%–42%— es una
medida real del techo, fijada por el sorteo inicial. **Lo que NO se ha probado** es que la fórmula aguante donde
puede romperse. Queda preregistrada la versión dura, para correr:
la fórmula debe fallar de forma medible cuando (a) los códigos se solapan (escenarios 2I/2J/2K, donde las celdas
compartidas reciben actualizaciones mixtas y la uniformidad dentro del código se rompe), (b) el clip de ±3 por celda
está activo, o (c) hay más de dos estímulos. **Predicción: el residuo deja de ser 0 exactamente en esos tres casos,
y crece con el solapamiento.** Si el residuo sigue siendo 0 con códigos solapados, la uniformidad del código es más
robusta de lo que creemos y eso es un hallazgo. Si crece, tenemos la primera medida de cuánto se degrada la
generalización por interferencia, que es lo que 2I y 2J insinuaban sin cuantificar.

### RAMA 3T — Composición temporal (nivel 7). VEREDICTO CONFIRMATORIO: **NO**
`experimentos/ramas/3T_temporal/`. Preregistro `7a96acbf3122dce1` escrito antes de correr nada.
Mundo idéntico a v6/v7 salvo la tabla de valor: morder A tras B → comida (+1); morder A tras A → veneno (−3);
morder B → neutro (0). El valor depende del ORDEN y de nada más. Seis brazos, 20 semillas, T=100k.

| | C1 (v6) | C2 (12 entradas a mano) | **C3 (la pregunta)** | C3C (control de ruido) |
|---|---|---|---|---|
| sep = W(A\|B) − W(A\|A) | 0.00 | **3.99** (20/20) | **0.00 (0/20)** | 0.00 |
| lift_q4 | −0.003 | +0.353 | **−0.005** | +0.001 |
| muertes | 230 | 113 | 236 | 234 |
| divisiones | 0 | 0 | 60 (pool agotado 20/20) | 60 (agotado) |

**Con las constantes congeladas de v7, la regla de división NO produce composición temporal.** Criterios 2 y 3
fallan 20/20. C1 no lo resuelve (predicción cumplida), C2 sí (techo alcanzable), C2b reproduce C1 con **0
discrepancias en 7.560 campos** (instrumento limpio), y el mundo se verificó 50/50 con `learn=False`.

**La cifra que más limpiamente lo decide**: el control de ruido C3C **separa los códigos MÁS que C3**
(solap_A = 0 [0,0] frente a 2 [1,3]). La dirección de división `P − mu[c]` es **distintividad no supervisada**:
separa lo que varía, no lo que predice. Es ciega a si el canal lleva información.

### BUG-01 (del tronco, no del instrumento) — bloqueo por saturación simétrica de canales
Bajo refuerzo contradictorio sobre un código compartido, **`Wp` y `Wn` corren los DOS al techo** (3.0/celda =
9.0/código) y su diferencia se anula **exactamente**, congelando todo aprendizaje posterior en esas celdas:
con `Wp=Wn=9`, `dlt>0` no puede subir `Wp` y `dlt<0` no puede subir `Wn`. Verificado sobre el organismo
**congelado sin modificarlo**:

    organismo_v7.run(1, plast=False, solap_AB=3)
      -> comp = {'A': (9.0, 9.0), 'B': (9.0, 9.0)},  W = {'A': 0.0, 'B': 0.0}
    (control E1 normal: A=(1.0, 0.0), B=(0.0, 3.0), sin inflar)

Esto **es** el *"v6 colapsa: W=0"* que el registro anotó en 2L el día 2 como observación, sin diagnosticar el
mecanismo. Ahora está diagnosticado. Es un bloqueo real del tronco, no un artefacto de medición: de ahí que se
numere BUG-01 y no ERR-09. Medido: se alcanza hacia t≈8.000; a T=3.000 `W_A=−1.48`, después se clava en 0.
Conecta también con 2F ("ambos canales saturan en 9, sin freno al apetitivo") y con 2J/2K ("canales inflados"):
era el mismo fenómeno visto tres veces y nunca nombrado.

### Diagnóstico POST-HOC de 3T (SIN valor confirmatorio, etiquetado como tal ANTES de correr)
Los dos modos de fallo estaban anticipados por escrito en el preregistro. Levantados por separado:

| | pool | techo Wp/Wn | C3 resuelve |
|---|---|---|---|
| confirmatorio | 90 | 3.0 | **0/20** |
| PH1 | 300 | 3.0 | 0/20 (separa representación 20/20, pero sep=0) |
| PH2 | 300 | 30.0 | 20/20 |
| **PH3** | **90 (el de v7, intacto)** | **30.0** | **20/20** |

**El pool nunca fue el problema. La única constante que bloquea es el techo de `Wp`/`Wn` en 3.0.**
Barrido con el pool intacto: techo 3.0 → 0/20 · 4.5 → 12/20 · 6.0 → 19/20 · 9.0 → 20/20 · 15 y 30 → igual que 9.
Transición monótona: es una **carrera entre la división y la saturación**.

Con ese único techo levantado y nada más (PH3, pool 90, θ/ema/paso intactos):

| PH3 | sep | lift_q4 | solap_A | divisiones | muertes |
|---|---|---|---|---|---|
| C2 (a mano) | 3.99 (20/20) | 0.35 | 0 | 0 | 113 |
| **C3 (sola)** | **3.97 (20/20)** | **0.34 (20/20)** | 1 (18/20 ≤1) | **16 [10,33]** | 114 |
| C3C (ruido) | 0.53 (**0/20**) | −0.04 (**0/20**) | 0 | 60 (agotado) | 114 |

C3 alcanza el techo de C2 **sin que nadie le diga dónde mirar**.

**LA FIRMA MECÁNICA, y es el hallazgo conceptual del día.** C3 **se detiene sola** (16 divisiones, última en
t≈7.418, 95% sobre A) porque el error desaparece. C3C **no se detiene nunca** (60, agota el pool en t≈24.486)
porque el error no baja jamás. Es decir:

> **La selección no está en la dirección de la división —que es indiscriminada y no supervisada— sino aguas
> abajo, en el error de predicción que la dispara y que la apaga.**

Eso refina la afirmación de unificación del día 2. El mecanismo no es "dividir hacia lo distintivo"; es
"dividir a ciegas mientras el error no baje, y parar cuando baja". La dirección no necesita ser inteligente:
el criterio de parada hace el trabajo. Y explica el umbral de 2 celdas medido esta mañana: ambos son la misma
carrera entre la señal de error y su extinción.

### Qué queda preregistrado y SIN correr a partir de 3T
1. **BUG-01 es del tronco y hay que arreglarlo en el tronco, con un cambio y un preregistro propios.**
   Subir el techo es arbitrario y no es la solución principista. Candidatos a evaluar uno por uno:
   decaimiento en `Wp`/`Wn`, normalización del par, o penalizar el crecimiento conjunto. **Decisión del director.**
2. Sólo después, repetir 3T como experimento **confirmatorio** con el tronco corregido. Si C3 sigue dando
   20/20 con criterio escrito antes, la composición temporal pasa de post-hoc a resultado.
3. Límite de diseño reconocido: la memoria es de **una** mordida, dada como copia eferente. No prueba secuencias
   largas ni orden abstracto. Un `lift` alto no implica planificación.

**Erratas del preregistro 3T, fechadas y sin recalibrar** (ERR-3T-01, ERR-3T-02): el criterio 4 se ancló en
`solap_A` suponiendo que la división sería selectiva; no lo es (C3C separa igual), así que ese criterio es
insatisfacible y no discrimina. El veredicto NO se sostiene con los criterios 2 y 3, que sí discriminan
(C3C saca 0/20 en todas las variantes). Y la predicción de oscilación de `W_A` en C1 falló: fue 0.000 exacto
por saturación — que es BUG-01 otra vez.

### Batería v7 criterio v2, 20 semillas — v7 SIGUE SIN CONGELARSE, y el umbral queda REFUTADO
`bateria_v7b.py`. E1, E2, E2J, E2K, E2L y el control negativo: **20/20**. Falla E2I con 18/20 en el disparo.

**CRITERIO 5 (umbral en 2 celdas) REFUTADO**, exactamente como estaba escrito que podía fallar:
las semillas **8 y 18 tienen solapamiento 2 y NO dividen**. La afirmación que registré esta mañana
("con 2 o 3 celdas compartidas la regla dispara siempre") es falsa.

**La refutación destapa la variable correcta: no es el número de celdas, es la VALENCIA.**
En E2I, C es veneno. C∩B es solapamiento entre dos venenos (**misma** valencia, sin conflicto de valor);
C∩A es entre veneno y comida (**opuesta**). Las semillas 8 y 18 tienen C∩B=2 y C∩A=0; la 15 tiene C∩A=2.

| ley | aciertos en E2I |
|---|---|
| solapamiento ≥2 (la de esta mañana) | 18/20 |
| **solapamiento ≥2 entre valencias OPUESTAS** | **20/20** |

Y es consistente con todas las demás etapas sin excepción:

| etapa | solapamiento | valencias | divide |
|---|---|---|---|
| E2J D comida ∩ B veneno | 1 | opuesta | no, 20/20 |
| E2K D comida ∩ B veneno | 2 | opuesta | **sí, 20/20** |
| E2L A comida ∩ B veneno | 3 | opuesta | **sí, 20/20** |
| E2I C veneno ∩ B veneno | 2 | misma | no (s8, s18) |
| E2I C veneno ∩ A comida | 2 | opuesta | **sí (s15)** |
| E2 inversión (sin solapamiento) | 0 | el valor cambia de signo | **sí, 20/20** |

**LEY CORREGIDA (a preregistrar antes de volver a correr):** la regla de división dispara cuando ≥2 celdas
de Kenyon son compartidas por estímulos de **valencia opuesta**, o cuando el valor de un estímulo cambia de
signo (inversión). El solapamiento entre estímulos de la misma valencia **no** dispara, por mucha que sea.
Esto no es nuevo en el proyecto, es la misma distinción que 2I y 2J ya habían medido en el valor
("misma valencia: deriva no corregida porque B no se re-muestrea" vs "con valencia opuesta el organismo
re-muestrea y RW corrige") — y que no se había conectado con la plasticidad estructural. Es el mismo eje.
Encaja además con la firma de 3T: lo que dispara y apaga la división es el error de predicción, y sólo el
conflicto de valencia produce un error que no baja.

**Predicción falsable de la ley corregida**, para el siguiente examen: forzar C∩B=3 con C veneno (misma
valencia, solapamiento máximo) debe dar **0 divisiones**. Si divide, la ley de valencia también cae.

### RAMA 3K — ¿hace falta que la expansión Kenyon aprenda? VEREDICTO: **NO, basta el azar. REFUTADA**
`experimentos/ramas/3K_kenyon_aprendido/`, preregistro `f303e55005fcdec1`. Mundo de 20 patrones de 6 px con
exactamente 3 activos; la valencia la decide **el píxel 0** y nada más. 10 patrones de entrenamiento, 10 de test
nunca vistos. Precisión = exactitud balanceada (toda política ciega a la clase vale exactamente 0.50).
Margen fijado ANTES: la expansión aprendida por error debe superar al azar en **≥ +0.10**.

| condición | precisión test | peso en el píxel relevante |
|---|---|---|
| 1 — Kenyon fijo aleatorio (= v6) | **0.683** | 1.02 |
| 2 — Hebb local | 0.698 | 1.06 |
| 3 — modulada por error de predicción | **0.707** | **1.02** |
| (techo medido, patrones de entrenamiento) | 0.993 | |

**Margen obtenido: +0.024 contra +0.10 exigido. Pareado 12/20 contra 15/20 exigido. REFUTADA.**

**La cifra que lo explica**: en el Kenyon **aleatorio y congelado**, la correlación entre `KW[i,0]` (el peso de
la celda en el píxel relevante) y la preferencia de clase de esa celda es **r = 0.87 antes de un solo paso de
experiencia**. No hay nada que descubrir: la proyección aleatoria ya está alineada con la característica,
porque el píxel relevante suma su peso al empuje de toda una clase y sesga el top-3 automáticamente.
El peso en el píxel relevante **no crece** con ninguna regla (1.02 → 1.02 con la modulada por error).

**El resultado más útil de la rama**: aprender KW **sí** mejora la representación — celdas usadas 16/30 → 19–22,
ratio de solapamiento intra/inter 1.22 → 1.94 — **y aun así la generalización no mejora**.
> **Descorrelacionar códigos no es lo mismo que representar la característica.**

**Corrige una afirmación mía del día 3.** Dije que "la capa Kenyon aleatoria y fija es el muro" del proyecto.
Para una característica que es función lineal de la entrada, **no lo es**: el azar la preserva y aprender la
expansión no aporta. El cuello de botella está en la **lectura** (30 celdas, códigos que colisionan), no en el
sorteo. La respuesta a la pregunta de la mosca, en este banco de pruebas, es que el azar basta.
Queda abierto si basta también para características NO lineales; eso es otro experimento.

Hallazgos laterales, con preregistro propio pendiente: (a) `hebb_mordida` **rompe E2K (18/20)**, única condición
que lo hace: el Hebb no supervisado degrada justo la etapa de solapamiento forzado. (b) Sonda exploratoria fuera
del preregistro: con la dirección de división de 2L **v2** (hacia lo distintivo, no hacia el patrón completo) la
precisión sube a **0.763**, el mejor de todo el estudio, pero sigue por debajo del margen y `ratio_disp`=0.97
— tampoco descubre el píxel relevante. Candidato al siguiente preregistro, no rescate de éste.
(c) El azar desperdicia un tercio de la capa: con 20 patrones sólo **16 de 30 celdas** entran en algún código.

### BUG-01, experimento 1 — decaimiento local en Wp/Wn. **REFUTADO**
Preregistro `experimentos/bug01/PREREGISTRO.md`, escrito y cerrado antes de tocar código.
`organismo_v7d.py` = v7 + `Wp[ix]*=(1-lam); Wn[ix]*=(1-lam)` en las celdas activas, sólo al morder.
Diff de 3 líneas funcionales. **Control 1: `lam=0.0` es bit-idéntico a v7, 42/42 escenarios × semillas.**
**Control 2: el bug se reproduce con `lam=0.0`** → `comp=(9.0, 9.0)`, `W=0.0`. λ=0.001 fijado a priori.
400 corridas, 20 semillas, 197 s.

| predicción | veredicto | cifra |
|---|---|---|
| **P1 desbloqueo** | **REFUTADA** | canales por debajo del techo: **0/20**. Con λ=0.001, `Wp=9.00`, `Wn=8.98`, `W=+0.02`. El bloqueo sigue intacto |
| **P2 no regresión** | **REFUTADA** | **E2K cae a 19/20** en `W_B ≤ −2.4`: el sesgo del 1.1% empuja una semilla fuera del criterio |
| P3 precisión | SOSTENIDA | el equilibrio analítico acierta a **3 decimales en los 5 valores de λ** |
| P4 ley de disparo | SOSTENIDA | el patrón de divisiones no cambia en ninguna etapa |

**Y no es cuestión de ajustar λ: la ventana es VACÍA.** Demostración, con `eta=0.03`, `K=3`, `aversion=1`,
clip 3.0/celda (9.0 por código). En el bloqueo `W≈0`, así que `dlt≈R` y el empuje **no se atenúa**:

    crecimiento por mordida de comida (R=+1):  K·eta·|R|            = 0.090
    crecimiento por mordida de veneno (R=−3):  K·eta·aversion·|R|   = 0.270
    con mezcla 50/50:  Wp* = 0.045/λ     Wn* = 0.135/λ

    para que Wn* < 9 (no saturar)                  ->  λ > 0.01500
    para que |W_B + 3| < 0.3 (valor correcto)      ->  λ < 0.01000

**λ tendría que ser a la vez mayor que 0.015 y menor que 0.010. No existe.** Y el criterio que aprieta es
el del veneno: **el mismo factor 3 que hace saturar antes el canal aversivo es el que estrecha la tolerancia**.
El decaimiento uniforme está estructuralmente condenado, no mal calibrado. **No se recalibra λ** (regla 3).

**Lo que sí deja el experimento**: P3 confirma que el mecanismo está entendido — el equilibrio
`W* = 3·eta·R/(3·eta+λ)` predice lo observado a 3 decimales para λ ∈ {0, 0.0003, 0.001, 0.003, 0.01}.
La derivación de arriba se apoya en esa validación, no en intuición.

**Diagnóstico de por qué falla**: el decaimiento uniforme ataca la **magnitud** de los canales, y la patología
no es de magnitud sino de **redundancia** — que los dos canales codifiquen lo mismo a la vez. Pagar en valor
neto (el sesgo del 1.1%) para corregir un exceso que no está en el valor neto es el error de diseño.
Eso apunta al experimento 2, ya nombrado en el preregistro del 1 y sin probar entonces: decaer **sólo la parte
común**, `m = min(Wp, Wn)`, que deja `Wp − Wn` **exactamente** intacto.

### Convergencia independiente: 2K-bis llega a BUG-01 por otro camino
La rama `2Kbis_capacidad` (que no sabía de este experimento) identifica BUG-01 como la causa raíz de su
resultado principal: **el 82% de los valores finales de v7 valen 0.000 exacto**, y en **169/169** de esos casos
`Wp·kc = Wn·kc = 9.000`. No es falta de aprendizaje — esos estímulos tienen 960 mordidas medianas, más que los
que sí aprenden. Y hay realimentación: con `W=0` la política muerde con p=0.84, así que v7 muerde **7× más**
que v6 (20.557 contra 2.864 mordidas), lo que acelera la saturación.

Su conclusión, que conviene citar literal en el texto:
> **El límite de esta arquitectura no está en el número de celdas Kenyon, sino en el rango dinámico de los
> canales de valor. Dividir compra separación; no compra rango.**

Con dos consecuencias que corrigen cosas registradas hoy:
- **La capacidad de v7 es MENOR que la de v6** (v7 gana sólo en 6/20; se pedían ≥15). La plasticidad no compra
  capacidad: la quita, por esta vía. v6 no tiene techo medible en ese diseño (su propio control preregistrado
  lo anula); v7 sí, en ~7 estímulos. Máximo de estímulos simultáneamente bien aprendidos: v6 = 6, v7 = 4.
- **Coste real ~7.5 celdas por estímulo** (no 1–4), y las 90 celdas se agotan con sólo 10 estímulos vivos.

### La ley de disparo, versión definitiva: **`err > 0.6`**, y las dos anteriores quedan refutadas
2K-bis refuta por dos sitios independientes la ley del umbral que registré esta mañana **y** la ley de valencia:
- con **A∩B=1** forzado y co-aprendizaje desde t=0, dividen **8/20** semillas (el umbral de 2 exigía 0);
- con solapamiento **2 y misma valencia** (D veneno ∩ B veneno) dividen **0/20**.

El primitivo real: **concordancia 320/320, sin una excepción, entre `splits>0` y `err_max > 0.6`.** Frontera de
cuchillo: la más alta que NO divide es 0.5996, la más baja que SÍ divide es 0.6003. Y cierra con derivación:
con solapamiento 0 la trayectoria del error es determinista (`|dlt|` decae por 1−K·η mientras la media móvil
olvida a 1−ema) y su máximo es analítico, **err_max = 0.147509·|R|**, con pico a las ~21 mordidas. Con |R|=3 da
**0.442508**, que es exactamente el 0.4425 medido en las 320 corridas. Cruzar θ=0.6 exigiría un error efectivo
sostenido de **|R| = 4.068**, mayor que cualquier recompensa que el mundo puede dar.

> **Con solapamiento 0 la regla no es que no dispare: es que NO PUEDE.** Sólo una celda que recibe premio *y*
> castigo supera 4.068. El recuento de celdas compartidas era un proxy, y falla en los dos extremos.

Mi "ley de valencia" de esta mañana es una **consecuencia** de esto (sólo el conflicto de signo produce error
suficiente), no el primitivo, y como enunciado general también es falsa. Queda sustituida por la de `err`.
Encaja con la firma de 3T: lo que dispara y apaga la división es el error, y sólo el conflicto lo sostiene.

### Nota de entorno (Windows)
`bateria.py` aborta en Windows con `UnicodeEncodeError` al imprimir `≈`: la consola es cp1252. Es fallo de impresión,
no de cálculo. Se corre con `PYTHONIOENCODING=utf-8`. Los archivos congelados NO se tocaron; `bateria_v7.py` incluye
`sys.stdout.reconfigure(encoding='utf-8')`.

---

## Día 3 — tarde. BUG-01 experimento 2, dos errores de instrumento más, y un instrumento nuevo

### BUG-01, experimento 2 — decaimiento de la PARTE COMÚN. Mecanismo CONFIRMADO, P1 REFUTADA

Preregistro: `experimentos/bug01/PREREGISTRO_exp2.md` (sha `8786ad6382e255f5`).
Script: `corre_bug01_exp2.py` (sha `968b49172c54a16c`).
Organismo: `organismo_v7e.py` (sha `3118c6d563542da2`) = v7 + una línea.
Datos: `datos/bug01_exp2_20260915_183244.json` (sha `1eb82a17119e5447`). 440 corridas, 20 semillas, 223 s.

Controles 1 y 2: **OK** (42/42 inercia contra v7; el bug se reproduce con `lam=0`).

**Veredictos tal como salieron: P1=REFUTADA, P2=REFUTADA, P3=SOSTENIDA, P4=SOSTENIDA.**

**Lo que el experimento sí demuestra, y es el resultado de fondo:**

| λ_c | Wp (mediana) | Wn (mediana) | W (mediana) | bajo techo |
|-----|--------------|--------------|-------------|------------|
| 0.0     | 9.000 | 9.000 | **+0.000** | 0/20 |
| 0.0125  | 6.995 | 8.310 | **−1.365** | 20/20 |
| 0.02    | 4.340 | 5.635 | **−1.365** | 20/20 |
| **0.05**| **1.775** | **3.035** | **−1.365** | 20/20 |
| 0.1     | 0.935 | 2.215 | **−1.365** | 20/20 |
| 0.3     | 0.370 | 1.700 | **−1.365** | 20/20 |

Tres cosas, ninguna menor:

1. **El techo se despeja 20/20 con cualquier λ_c ≥ 0.0125**, y la frontera derivada a priori era
   **λ_c > 0.01125**. La derivación acertó la frontera antes de correr.
2. **`W` es EXACTAMENTE el mismo — a tres decimales y con rango idéntico [−2.090, −0.300] — para las cinco
   λ_c, que cubren un rango de 24×.** Ésa es la propiedad 1 del diseño (restar lo mismo a los dos canales
   deja `Wp − Wn` intacto) confirmada de la forma más fuerte posible: **el arreglo no cuesta NADA en valor
   neto.**
3. **P3 lo cierra**: `W_A = +1.000` y `W_B = −3.000` exactos, desviación **0.0000**. El sesgo del 1.1% que
   hundió el experimento 1 **desaparece por completo**. P4: la ley de disparo no se mueve — los mismos
   individuos dividen en las seis etapas.

**Por qué P1 queda REFUTADA igual.** Falló **sólo** su tercer subcriterio, `W ∈ [−1.5,−0.5] en ≥18/20`.
Los otros dos pasaron: techo despejado 20/20, y `Wp`/`Wn` en 1.77/3.04 contra 1.8/2.8 predichos (±0.5) —
**predicción puntual acertada**. La predicción `W_eq = −1` supuso mezcla exacta 50/50 de mordidas A:B; la
mezcla real la fija la política y varía por semilla, y el rango sale [−2.09, −0.30].
**Es un fallo de la capa de política, no del mecanismo** (regla 4). No se recalibra (regla 3). Cualquier
criterio nuevo sobre la dispersión de `W` exige preregistro propio, escrito antes.

### ERR-09 — noveno error de instrumento: la comprobación de inercia era imposible por construcción

> **Aviso de numeración**: los artefactos del exp. 2b (preregistro, script y JSON) llaman a este error
> "ERR-07" porque lo numeré antes de comprobar que ERR-05…ERR-08 ya estaban asignados. **El número correcto
> es ERR-09**, que estaba libre a propósito (ver la línea de BUG-01: "se numere BUG-01 y no ERR-09"). Los
> tres artefactos **no se editan**: son un trío casado por hash y corregirlos rompería la trazabilidad de la
> regla 7. **El registro manda: ERR-09.**

En `corre_bug01_exp2.py`, P2 comprobaba la inercia así:

```python
ident = all(a == b for a, b in zip(R(esc, 0.0), rs))
```

`R(esc, lam)` devuelve los dicts de `tarea()`, y esos dicts **contienen la propia clave `lam`** (línea 41:
`return dict(esc=esc, lam=lam, seed=seed, ...)`). Al comparar el brazo `lam=0.0` contra el brazo `lam=0.05`,
la clave `lam` difiere **por construcción**.

> **`ident` era estructuralmente `False`. No podía dar `True` jamás, ni aunque el organismo fuese literalmente
> el mismo archivo.** No medía inercia: medía que 0.0 ≠ 0.05.

**Corrección**: excluir las claves de etiqueta (`esc`, `lam`, `seed`), que son índice y no resultado.
Aplicada a los datos ya guardados: **E1 20/20**, E2I 6/20, E2J 0/20.

### ERR-10 — décimo error: "sin conflicto" definido como solapamiento espacial final

Tras ERR-09 escribí `PREREGISTRO_exp2b.md` redefiniendo `SIN_CONFLICTO` por criterio mecánico medido, no
declarado: cero solapamiento entre **todos** los códigos presentes. Con eso, E2J sale de la categoría (su
`solap_B=1` fuerza D-comida ∩ B-veneno: es conflicto por definición) y E2I se clasifica semilla a semilla.

**Esa definición también está mal, y la reejecución lo demuestra.** Tiene dos agujeros, los dos míos:

- **Ignora el conflicto TEMPORAL.** En **E2** (`invertir_en=50000`) la misma celda recibe premio y castigo
  **separados en el tiempo**, no en el espacio. El solapamiento espacial es 0 y el conflicto es total.
  Clasifiqué 18/20 semillas de E2 como "sin conflicto" y las 18 difieren.
- **Mide el código en el momento equivocado.** En **E2L** (`solap_AB=3`) la plasticidad divide y lleva el
  solapamiento a 0 **al final** — de hecho el criterio `solap->0` pasa 20/20. Mi clasificador leyó el código
  final y vio 0, cuando durante la corrida fue 3. Clasificó mal las 20/20.

**El primitivo correcto no es el solapamiento: es `min(Wp, Wn) > 0` en alguna celda activa en algún momento.**
Espacial y temporal quedan cubiertos por la misma condición, que es exactamente la que dispara la línea del
arreglo. Se mide instrumentando el organismo para registrar si `min(Wp,Wn)` llega a ser > 0 en una celda que
se actualiza. **Eso exige preregistro nuevo, escrito antes de correr. NO se corre todavía.**

**El patrón, tercera vez.** ERR-06, ERR-08 y ahora ERR-10 tienen la misma raíz, ya identificada el día 3:
**escribir un criterio que no dice lo que quiero decir, y descubrirlo sólo al correrlo.** Las tres veces el
organismo estaba bien y el enunciado mal. Diez de diez anomalías del proyecto han sido del instrumento.

### BUG-01 exp. 2b — reejecución de P2 con el instrumento corregido

Preregistro: `PREREGISTRO_exp2b.md` (sha `024b3e292ec60f59`).
Script: `corre_bug01_exp2b.py` (sha `2f92f5bebdb5bff6`).
Sonda: `sonda_codigos.py` (sha `1fb8577e12aeed16`), copia de v7e + una línea que exporta los códigos.
Datos: `datos/bug01_exp2b_20260915_191934.json` (sha `8fac06e68e2675c6`). 243 s.

Controles: **1, 2 y 3 OK**. El control 3 es nuevo y verifica que la sonda es bit-idéntica a `organismo_v7e`
en las claves compartidas: **42/42**. La sonda es el mismo organismo.

| predicción | resultado | detalle |
|------------|-----------|---------|
| **P2a** inercia donde solap=0, debe ser 100% | **REFUTADA** | 26/64 — ver ERR-10 |
| **P2b** control positivo: 0% idénticos donde hay conflicto | **SOSTENIDA** | **0/76**, sin excepción |
| **P2c** las seis etapas pasan sus criterios científicos | **SOSTENIDA** | **20/20 en las seis** |

Desglose de P2a, que es donde vive ERR-10:

| esc | clasificadas sin conflicto | idénticas | lectura |
|-----|---------------------------|-----------|---------|
| E1   | 20/20 | **20/20** | la inercia se cumple exactamente |
| E2I  | 6/20 (semillas 3,4,6,14,16,17) | **6/6** | idem, y la clasificación por semilla acierta |
| E2   | 18/20 | 0/18 | **mal clasificadas: conflicto temporal** |
| E2L  | 20/20 | 0/20 | **mal clasificadas: solapamiento 3→0 durante la corrida** |

**Donde la definición sí captura el mecanismo — E1 y E2I — la inercia se cumple sin una sola excepción:
26/26.** Y la concordancia del criterio de solapamiento con la bit-identidad en E2I es **20/20** (verificado
aparte, semilla a semilla, midiendo `C∩A` y `C∩B`): las semillas 5, 11, 12 y 20 tienen `C∩B=0` pero `C∩A=1`,
y mirar sólo `nB` se las dejaba fuera.

**P2b importa tanto como P2a**: 0/76 idénticos donde hay conflicto demuestra que el arreglo **sí actúa** donde
debe. Si todo hubiera salido idéntico, el decaimiento no estaría haciendo nada y P1 sería un espejismo.

**Estado de BUG-01**: el mecanismo está confirmado (techo despejado, `Wp`/`Wn` en su equilibrio derivado,
valor neto exacto, ley de disparo intacta, seis etapas 20/20). Lo que falla son mis criterios, tres veces
seguidas. **v7e NO se congela.** v6 sigue siendo el tronco.

### Preregistro pendiente de correr: prueba de AHORRO (el coste del arreglo)

`experimentos/bug01/PREREGISTRO_ahorro.md` (sha `ca6638df5682212e`).
**Exigido por dirección como condición para seguir con el paso 1.** Escrito, **sin correr**.

La objeción de dirección: el arreglo drena la parte común de `Wp`/`Wn`, que es donde vive el **miedo latente
bajo el apetito** que compró 2F. Hay que medir si se pierde antes de congelar nada.

Precisión de alcance, medida: **el exp. 2 (λ_c=0.05) NO deja ningún canal en cero** — su equilibrio es
`Wp*=1.8`, `Wn*=2.8` sobre un techo de 9. El que sí lo deja en cero por construcción es el **exp. 3**
(λ_c=1, normalización opuesta completa). La objeción es letal para el exp. 3 y atenuada para el exp. 2.

Diseño: tres fases (adquisición / extinción con mundo invertido / reaprendizaje), `T=200.000`, 20 semillas,
7 brazos (v6, v7 control, exp2, total, y pisos 0.25/0.5/1.0). Ahorro ≡ `(n1−n3)/n1` en **mordidas de B**.
**Criterio de dirección, escrito antes**: si el ahorro de un brazo cae por debajo del **50%** del de v6, ese
brazo compra rango vendiendo memoria latente y **no se congela por defecto**.

**Hecho del instrumento que condiciona la recuperación espontánea, verificado leyendo el código**: en v6 y en
todas las variantes, `Wp` y `Wn` **sólo se modifican dentro de `if mordio:`** (v6 líneas 52–58). No hay ningún
proceso dependiente del tiempo. **Con `A∩B=0` la recuperación espontánea es imposible por construcción**:
mediría cero en todos los brazos y no diría nada de ninguno. Por eso se corre con `solap_AB ∈ {0,1,2}` y
**`solap_AB=0` es el control negativo** (debe dar 0.000 exacto).

### INSTRUMENTO NUEVO — `sandbox/`, ejecutor externo sin juicio, y su REGLA DE CRUCE

Por decisión de dirección se añade un tercer instrumento: un ejecutor externo (Antigravity) que corre barridos
mecánicos rápidos. **Se usan sus ciclos, no sus conclusiones.**

**Ubicación**: `JUACO/sandbox/`, **fuera del árbol del repo** (la raíz git es `bundle/`). Nada de ahí es un
dato del proyecto.

**Contenido**: copias de sólo lectura de `organismo_v6.py` (`5f38f83cf49248a3`) y `organismo_v7.py`
(`3db0475ef0ea95ce`) ancladas en `HASHES.txt`, con `verifica_hashes.py`; `tareas/` (una tarea por archivo);
`variantes/`; `resultados/`.

**Permisos**: el ejecutor escribe **sólo** en `sandbox/variantes/` y `sandbox/resultados/`. **No** tiene
acceso de escritura a `bundle/organismo/`, `bundle/registro/` ni `bundle/datos/`, ni toca los dos organismos
anclados.

**Formato fijo de tarea**: hipótesis en una línea · qué parámetro o línea cambia y en qué archivo · semillas ·
columnas exactas del CSV · orden explícita de NO interpretar ni tocar nada más.

**REGLA DE CRUCE — la única puerta hacia este registro:**

> Nada de `sandbox/resultados/` entra aquí hasta reproducirlo en el repo. En este orden:
> 1. `python verifica_hashes.py` → si falla, **se descarta la tarea entera**, sin intentar recuperarla.
> 2. Reproducción **dentro del repo**, con script y preregistro propios.
> 3. `bateria.py 20` todo PASA.
> 4. `manifiesto.py` con los cuatro congelados intactos.
> 5. Sólo entonces la línea en el registro, con la etiqueta **obligatoria**:
>    `origen: sandbox externo, reproducido en repo, <fecha>, <hash del script del repo>`

Un número que no haya pasado los cinco pasos **no existe** para el proyecto.

**Primeras tres tareas escritas** (20 semillas cada una): `T01_piso_decaimiento` (pisos 0/0.25/0.5/1.0 × λ_c
0.05/0.1/0.3/1.0 × 7 escenarios), `T02_prueba_ahorro` (los 7 brazos del preregistro de ahorro),
`T03_umbral_division` (14 valores de θ × 7 escenarios, sin tocar ningún .py).

**Estado al cierre del día**: el ejecutor corrió T01 por su cuenta (1.360 s). Entregó `organismo_v7f.py`
(sha256 `a4f7688e…`) y un CSV de **2.380 filas** con la cabecera exacta pedida, más un `.txt` de procedencia
no solicitado pero correcto (hash, versiones, tiempo) — **no interpretación**. Hashes anclados verificados
**intactos** después de su corrida, y los cuatro congelados del repo también.
**T01 NO está cruzada: es una hipótesis, no un dato.** Pendiente de reproducir en repo.

**Nota operativa**: el ejecutor lanza 16 workers y satura la máquina. Corriendo a la vez que un experimento
del repo, los controles de `exp2b` tardaron el doble. **Repo y sandbox no deben correr simultáneamente**; si
se solapan, el tiempo de pared de ambos deja de ser comparable con los ya registrados.

### Decisiones de dirección tras el informe del exp. 2 (15 sep 2026, noche)

**El arreglo de la parte común queda ACEPTADO COMO MECANISMO.** Techo despejado 20/20 por encima de la
frontera derivada a priori, valor neto idéntico a tres decimales en un rango de 24× de λ_c, sesgo del 1.1%
desaparecido, ley de disparo intacta. Aceptar el mecanismo **no** es congelar el organismo: falta el coste.

**λ_c es un INTERRUPTOR, no una perilla. No se vuelve a barrer.** Por encima de 0.01125 el resultado deja de
depender de su valor — ésa es justamente la evidencia del exp. 2: `W` sale idéntico a tres decimales y con
rango idéntico para λ_c ∈ {0.0125, 0.02, 0.05, 0.1, 0.3}. Lo único que λ_c elige es dónde queda el equilibrio
de `Wp`/`Wn`, y eso sólo importa para el miedo latente, que se mide con la prueba de ahorro y no con un
barrido. Un barrido más de λ_c no aportaría información: aportaría filas.

**ERR-09 y ERR-10 aceptados con esa numeración.** El primitivo del conflicto pasa a ser, oficialmente:
`min(Wp, Wn) > 0` en alguna celda activa en algún momento. Cubre el conflicto espacial y el temporal con la
misma condición, que es exactamente la que dispara la línea del arreglo.

### REGLA 10 — progreso con marca de tiempo y log desde el arranque

> **Todo script de más de un minuto emite una línea de progreso por etapa con marca de tiempo, y escribe a
> archivo DESDE EL ARRANQUE, no sólo al final.**

Origen: el 15 sep una corrida sana de `corre_bug01_exp2.py` estuvo ~6 minutos sin imprimir nada (84 controles
en serie, sin progreso) y **fue indistinguible de un cuelgue**. La corrida acabó perdida y con ella su salida.

**Se registra como REGLA, sin número de error, y la decisión es deliberada.** La serie ERR-NN nombra anomalías
que produjeron **mediciones falsas o perdidas por el instrumento de medida**: ERR-05 un dato falso en el
registro, ERR-06/08/10 criterios que medían otra cosa, ERR-07 un artefacto de `argsort`, ERR-09 una comparación
imposible por construcción. Lo de hoy no corrompió ninguna medición: hizo ilegible el estado de una corrida
sana. Es un defecto de proceso, no de medida. Numerarlo ERR-11 diluiría la serie, y el valor de la serie está
en que "N de N anomalías fueron del instrumento" sea una afirmación **contable y afilada sobre mediciones**.

Referencia de implementación: `experimentos/bug01/corre_ahorro.py` (función `log()`, con `flush` + `fsync`,
etapas numeradas `ETAPA k/4`, y log en `datos/ahorro_<fecha>.log` seguible con `tail -f` mientras corre).

### REGLA 11 — repo y sandbox nunca corren a la vez

> **El repo tiene prioridad. El sandbox arranca sólo cuando no hay nada del repo corriendo, y con
> `Pool(6)`, no 16.**

Medido el 15 sep: el ejecutor lanzó 16 workers mientras corría `exp2b` y **los controles de ese experimento
tardaron el doble**. El tiempo de pared es un dato registrado (regla 7); al solaparse deja de ser comparable
con los ya anotados.

### ADVERTENCIA — el ejecutor externo actuó fuera de mandato

El ejecutor corrió **T01 sin que nadie se la asignara**. El trabajo salió conforme: hashes anclados intactos
antes y después, cabecera exacta, 2.380 filas, `.txt` de procedencia correcto y **sin interpretación**.

> **Que se portara bien no lo hace aceptable.** Actuar fuera de mandato es precisamente lo que este
> instrumento tiene prohibido. El sandbox vale en la medida en que no pueda contaminar la cadena de
> procedencia, y un ejecutor que decide por su cuenta cuándo empezar ya está decidiendo. Esta vez acertó;
> eso es suerte, no garantía.

Regla explícita añadida a `sandbox/README.md` y a las tres tareas: **una tarea se corre cuando la dirección o
el repo la asignan, no antes. Que exista un archivo en `tareas/` no la asigna.**

### Orden de trabajo fijado por dirección

1. **Prueba de ahorro primero**, tal como está preregistrada, criterio del 50% literal, `solap_AB ∈ {0,1,2}`
   con el 0 como control negativo. **Corre en el repo, no en el sandbox.**
2. **T01 no se reproduce aparte**: los pisos 0/0.25/0.5/1.0 van dentro de la prueba de ahorro, así que queda
   **cruzada de paso**. Sólo se abre el CSV del sandbox si el ahorro da algo inesperado y hace falta comparar.
   T02 queda **en suspenso** en el sandbox por el mismo motivo.
3. Si el ahorro pasa: batería completa con el arreglo → examen de congelación de v7 con la ley `err > 0.6`
   → y **sólo entonces** 3T confirmatorio. **Un cambio por vez.**
4. **v6 sigue siendo el tronco hasta que un candidato pase todo.**

### PREDICCIÓN DERIVADA DEL CÓDIGO, no de la literatura — y es falsable

> **Con solapamiento cero, la recuperación espontánea del miedo extinguido es IMPOSIBLE por construcción,
> porque el decaimiento vive dentro de la mordida.**

El argumento, completo y verificable leyendo tres líneas:

1. `Wp` y `Wn` **sólo se modifican dentro del bloque `if mordio:`** — en v6 son las líneas 52–58, y el
   decaimiento del arreglo (v7e línea 70, v7g con piso) está en ese mismo bloque. **No existe ningún proceso
   dependiente del tiempo** en ninguna de las variantes.
2. Luego, sin mordida no hay cambio de peso. El mero paso del tiempo no puede mover `W_B`.
3. Con `A∩B = 0`, morder A no toca ninguna celda del código de B.
4. Por tanto, en una ventana sin B, `W_B` no puede cambiar: `wB_post − wB_pre = 0.000` **exacto**, no
   aproximado, en todas las semillas y en todos los brazos.

**Qué la falsaría**: cualquier `wB_post − wB_pre ≠ 0.000` con `solap_AB = 0`. Un solo caso basta. Si aparece,
hay un camino de modificación de pesos que no conozco, y eso importaría más que el resultado del ahorro.

**Consecuencia metodológica, que es el motivo de escribirla**: medir recuperación espontánea con `A∩B = 0`
daría cero en todos los brazos y **parecería** un resultado ("ningún brazo recupera") cuando es una identidad
del código. Por eso el bloque B corre con `solap_AB ∈ {0, 1, 2}` y el 0 es **control negativo**, no condición
experimental. Es una predicción mía, derivada del código y no de la literatura de condicionamiento, y está
escrita antes de mirar los números.

### PRUEBA DE AHORRO — CORRIDA. A1 y A5 REFUTADAS, y las dos por el instrumento

Preregistro `PREREGISTRO_ahorro.md` (sha `ca6638df5682212e`). Script `corre_ahorro.py` (sha
`93a3dede5770b8a7`). Constructor `construye_ahorro.py` (sha `b5d30709e30043c0`). Organismos
`organismo_v6s.py` (sha `057a52bf0fcb8745`) y `organismo_v7g.py` (sha `3bbefa916572a78d`), generados por
parcheo con anclas desde v6 y v7e. Datos: `datos/ahorro_20260915_194823.json` (sha `18990c8a6febc261`),
`.csv` (sha `d9649b0a033e56cc`), `.log`. 640 corridas a T=200.000, 793 s. **Primer script bajo la regla 10.**

**Control 1: OK.** `v6s` vs `v6` **30/30** y `v7g` vs `v7` **42/42** bit-idénticos. Las variantes son
demostrablemente los mismos organismos.

| | resultado | |
|---|---|---|
| **A1** Ahorro(v6) > 0 (control del instrumento) | **REFUTADA** | ahorro = **−0.2105**, rango [−0.2105, −0.2105] |
| A2, A3, A4 | **no se leen** | el preregistro lo ordena si A1 cae |
| **A5** control negativo, delta = 0.000 exacto con solap_AB=0 | **REFUTADA** | v6 20/20 exacto; las variantes plásticas 18/20 |

### ERR-11 — la medida de ahorro es función de `W` sola, y `W` es invariante al arreglo POR DEMOSTRACIÓN

El ahorro de v6 salió **idéntico en las 20 semillas**: `n1 = 19`, `n3 = 23`, rango cero. Eso no es biología,
es aritmética, y se deriva en tres líneas. Con `aversion = 1`, `K·eta = 0.09`:

```
W(k+1) = (1 − K·eta)·W(k) + K·eta·R = 0.91·W(k) − 0.27      punto fijo −3
fase 1, desde W=0:   |0−R| · 0.91^k ≤ 0.5  ->  k = ceil(18.998) = 19   <- n1 observado
fase 3, desde W=+1:  |1−R| · 0.91^k ≤ 0.5  ->  k = ceil(22.049) = 23   <- n3 observado
ahorro = (19−23)/19 = −0.210526                                        <- observado −0.2105
```

**El "déficit" mide únicamente desde dónde arranca `W`, no si queda traza latente.** Tras la extinción
`W_B = +1`, y llegar a −2.5 desde +1 cuesta más pasos que desde 0. Nada más.

Y hay algo peor, que es el fondo del error: **los cinco brazos con decaimiento dan `n1`/`n3` IDÉNTICOS,
semilla a semilla** (`exp2` = `total` = `piso_025` = `piso_050` = `piso_100`). No es casualidad ni ruido:

> **Demostración.** `dlt = R − W` depende sólo de `W`. Si `dlt>0`, `Wp += eta·dlt·kc`, luego
> `W += eta·dlt·kc`. Si `dlt<0`, `Wn += eta·aversion·(−dlt)·kc`, luego con `aversion=1`
> `W += eta·dlt·kc` — **la misma expresión**. Y el decaimiento resta lo mismo a los dos canales, así que no
> toca `W`. Además el decaimiento nunca toca el clip: `mcom = max(min(Wp,Wn) − piso, 0) ≥ 0` impide que
> `Wp` baje de 0.
> **Por tanto, sin tocar el clip superior, la trayectoria de `W` es EXACTAMENTE independiente de `λ_c`, del
> `piso` y de cómo se reparta `Wp`/`Wn`.**

**Cualquier métrica que sea función de `W` sola es incapaz de distinguir los brazos, por construcción.**
`n1` y `n3` lo son. Diseñé una prueba cuyo observable es justo la cantidad que el arreglo deja invariante —
que es, además, **la propiedad que el arreglo presume**. Es el cuarto error del mismo patrón (ERR-06,
ERR-08, ERR-10, ERR-11): escribir un criterio que no mide lo que quiero medir.

**La coexistencia sí está ahí, y el piso sí la gradúa.** Lo que el ahorro no ve, `comp_B` lo enseña
(bloque A, solap_AB=0, semilla 1):

| brazo | Wp_B | Wn_B | **W_B** |
|---|---|---|---|
| v6 | 3.98 | 6.98 | **−3.00** |
| v7_control | 4.40 | 7.40 | **−3.00** |
| exp2 (λ=0.05) | 0.02 | 3.01 | **−3.00** |
| total (λ=1, piso 0) | **0.00** | 3.00 | **−3.00** |
| piso_025 | 0.75 | 3.75 | **−3.00** |
| piso_050 | 1.50 | 4.50 | **−3.00** |
| piso_100 | 3.00 | 6.00 | **−3.00** |

La escalera del piso es perfecta en los canales — `Wp_B` va de 0.00 a 3.00 exactamente como se diseñó — y
**`W_B = −3.00` en los siete**. El arreglo hace exactamente lo que dice, y la conducta no se entera.

### CONSECUENCIA — la pregunta de dirección queda respondida, pero por demostración y no por medida

La preocupación era: *el arreglo compra rango vendiendo memoria latente*. Con la invariancia de arriba:

> **En esta arquitectura, la memoria latente no tiene NINGUNA consecuencia conductual salvo a través de la
> saturación.** La conducta depende sólo de `W`; `W` es exactamente invariante al reparto `Wp`/`Wn`; luego
> lo único que el reparto puede cambiar es *cuándo un canal toca el techo*. Y tocar el techo es BUG-01,
> que es lo que el arreglo existe para evitar.
>
> **El arreglo no puede costar conducta. Sólo puede comprarla.**

Eso **no** cierra el asunto por sí solo: dice que el coste, si existe, vive en el régimen de saturación, que
es justo donde el arreglo actúa. La prueba que haría falta es otra: **medir el ahorro con los canales cerca
del techo**, donde el clip sí muerde y el reparto sí importa. Requiere preregistro nuevo, escrito antes.
Lo que **no** hay que volver a hacer es medir ahorro con una función de `W`.

### A5 refutada: MI predicción cae, y el culpable es la plasticidad estructural

Escribí, como predicción derivada del código y falsable: *con solapamiento cero la recuperación espontánea
es imposible por construcción, porque el decaimiento vive dentro de la mordida.* Dije que un solo caso
bastaba para tumbarla. Hay **dos**, y el veredicto se parte:

- **v6: SOSTENIDA, 20/20 con `delta = 0.000` exacto.** Sin plasticidad, la predicción es correcta.
- **Variantes plásticas: REFUTADA, 18/20.** Las semillas **6 y 19** dan `delta = −0.0067` y `−0.0136`, y
  ambas tienen **`splits = 5`, `celdas = 35`**. Y el desvío es **idéntico en los seis brazos**, incluido
  `v7_control` (`lam=0`): **no tiene nada que ver con el arreglo.**

**Qué se me escapó.** El argumento era correcto sobre los **pesos** y ciego a la **representación**.
`W_B = (Wp − Wn) @ kenyon(B)`, y `kenyon(B)` es el top-K sobre las celdas activas. Al comer A durante la
ventana sin B, una celda de A puede **dividirse**: aparece una celda activa nueva con `KW` heredado, y esa
celda puede **entrar en el código de B**. Los pesos no se mueven; **el código sí**, y `W_B` con él.

> **Hay una vía por la que el miedo cambia sin una sola experiencia del estímulo temido: es estructural,
> no sináptica.** La división de celdas reescribe qué significa "B" mientras B no está.

Es la regla 4 otra vez, y esta vez me la salté yo: confundí la capa de **representación** con la de **valor
aprendido**. La predicción corregida, y falsable igual: *sin plasticidad estructural, la recuperación
espontánea es imposible por construcción; con ella, es posible y proporcional a las divisiones ocurridas
durante la ventana.* La segunda mitad **no está medida** — hace falta correlacionar `delta` con divisiones
dentro de la ventana, y eso es preregistro nuevo.

### Estado al cierre

- **El arreglo de la parte común sigue aceptado como mecanismo y sigue SIN congelarse.** Lo que falta no es
  confianza en el mecanismo: es una prueba de coste que sepa medir el coste.
- **v6 sigue siendo el tronco.**
- **T01 no queda cruzada** como se esperaba: la prueba de ahorro corrió los pisos, pero su lectura es nula
  por ERR-11, así que no valida nada del barrido del sandbox. T01 sigue siendo hipótesis.
- Pendiente, en este orden: (1) preregistro de una prueba de coste en régimen de saturación; (2) batería
  completa con el arreglo; (3) examen de congelación de v7 con `err > 0.6`; (4) 3T confirmatorio.
  **Un cambio por vez.**

### APAGÓN tras el cierre — qué se perdió (nada) y qué demuestra del protocolo de escritura

Se fue la luz la noche del 15 sep 2026, después de las 20:05. Al recuperar la máquina, el estado en disco
reconstruye la sesión entera sin ambigüedad:

| hora | evento |
|---|---|
| 20:01:36 (+793.0 s) | `corre_ahorro.py` termina limpio: las cuatro etapas en el log, los sha256 del JSON y del CSV escritos por el propio script, y la línea `VEREDICTO ahorro: A1=False A2=None A3=None A4=None A5=False` |
| 20:05 | `REGISTRO_etapas_1_2.md` y `MANIFEST.txt` actualizados con ese resultado, hasta "Estado al cierre" |
| — | corte de luz |

Comprobado al volver: **cero procesos Python vivos, ningún archivo a medias, los cuatro congelados intactos
(`manifiesto.py --check`), los dos organismos anclados del sandbox intactos (`verifica_hashes.py`), y
`MANIFEST.txt` idéntico a disco en las 190/190 líneas.** **Lo único que faltaba era el commit**, hecho ya:
`29a7dd2`, 19 archivos, árbol limpio.

**Qué prueba esto y qué no**, que importa más que la anécdota:

- **Sí prueba la mitad de escritura de las reglas 7 y 10.** El resultado, sus hashes y su lectura en el
  registro estaban en disco **antes** del corte porque se escriben al terminar cada etapa, no al cerrar la
  sesión. Un apagón encontró el trabajo guardado, no en memoria.
- **No prueba la mitad de diagnóstico de la regla 10.** El corte **no cayó durante una corrida**, así que no
  puso a prueba el caso que la regla 10 ataca de frente: distinguir un script sano de uno colgado, y dejar
  rastro legible de por dónde iba. Eso sigue sin ensayarse en condiciones reales.
- **La grieta que sí queda al descubierto es git.** Ocho horas de trabajo válido —exp. 2, exp. 2b y la prueba
  de ahorro entera— vivieron sin commit desde las 13:14. El disco aguantó; el disco no siempre aguanta.
  **Consecuencia operativa: se commitea al cerrar cada experimento, no al cerrar la jornada.**

### DUPLICADO CONOCIDO en `sandbox/resultados/` — NO limpiar

El ejecutor externo entregó T01 **triplicado bajo tres nombres**, con dos contenidos distintos y seis
archivos. Verificado por hash, 15 sep 2026:

| sha256 (16) | bytes | nombres |
|---|---|---|
| `ea40cb4bfd19c5ff` | 351.868 | `T01_piso_decaimiento.csv`, `T01_piso_decaimiento_2026-09-15.csv`, `T01_piso_decaimiento_20260915.csv` |
| `d4368548c7ce3f0b` | 232 | `T01_piso_decaimiento.txt`, `T01_piso_decaimiento_2026-09-15.txt`, `T01_piso_decaimiento_20260915.txt` |

> **No se borra ninguno.** Los tres nombres son parte de la procedencia de la entrega: documentan cómo nombró
> sus artefactos el ejecutor externo, y esa forma de nombrar es un dato sobre el instrumento. Borrar dos
> copias "por limpieza" destruiría la evidencia de que hubo tres, y con ella la posibilidad de detectar que el
> ejecutor duplica salidas. **El contenido es bit a bit el mismo: no hay conflicto que resolver, hay un hecho
> que conservar.**

Recordatorio de estado: **T01 sigue sin cruzar.** Es hipótesis, no dato, y ninguno de estos seis archivos
cuenta para el proyecto hasta pasar los cinco pasos de la REGLA DE CRUCE.

---

## Día 4 (16 sep 2026) — arranque, incidente T02, auditoría de una copia externa

### Arranque

- **Regla 1:** `bateria.py 6` PASA 6/6 en las cinco etapas (133 s).
- **Hashes:** `manifiesto.py --check` da 4/4 intactos y `verifica_hashes.py` del sandbox da OK.
- **Commit `4e36964`:** las secciones pendientes del día 3 (apagón y duplicado).
- **Procesos:** el único Python vivo es `pythonw -m community_av sentinel`, un antivirus ajeno al proyecto.

### INCIDENTE T02 — el ejecutor la intentó sin asignación, y el texto de la tarea estaba mal escrito

**Hechos.** El 15 sep, entre las 20:53 y las 20:59, el ejecutor dejó en el sandbox:
- `variantes/organismo_v6s.py`
- `variantes/organismo_v7g.py`
- `resultados/BLOQUEADA_T02.txt` y `BLOQUEADA_T02_prueba_ahorro.txt`, con el mismo contenido (sha `855ec987a381963c`).

T02 estaba **EN SUSPENSO**. Dirección confirma el 16 sep que **no la asignó**: ese día le había pedido cosas
sueltas al ejecutor. Es la **segunda actuación sin asignación**.

**Lo que reportó el ejecutor es CIERTO, y el defecto está en el texto de la tarea, que escribió el repo.**
- §2.2 ordena insertar `if kk=='B':` con 16 espacios antes de `if plast:`. Pero en `organismo_v7f.py`,
  `if plast:` está a 20 espacios, dentro de `if learn:` (16).
- Esa inserción cierra `if learn:` y anida la plasticidad dentro de `if kk=='B':`. Verificado en el archivo
  generado: línea 75 a 16 espacios y línea 80 a 20.
- En §2.1(d), "16 espacios (alineada con `dlt=R-Wb@kc`)" también se contradice: `dlt` está a 20. La cifra
  sirve para v6; el paréntesis está mal.

**Cómo se detectó.** La comprobación bit a bit de §2.3 lo atrapó (MISMATCH en la semilla 1), y el ejecutor paró
como manda su contrato.
- **No produjo ninguna medición**, así que no lleva número ERR-NN (el mismo criterio que la REGLA 10). Es un
  defecto de proceso, y la comprobación obligatoria demostró que sirve.
- **El repo no está afectado.** Su `organismo_v7g.py` lo generó `construye_ahorro.py` con anclas (la cuenta va
  al final de la división) y pasó 42/42.
- **T02 sigue en suspenso.** Si se reactiva, primero se corrige §2.2.

### AUDITORÍA — copia externa trabajada por Antigravity. **NADA entra al proyecto**

**Contexto.**
- El 15 sep a las 21:05, dirección copió el repo a `PROYECTOS/Nueva carpeta/bundle` para probar al ejecutor
  externo. Antigravity trabajó ahí entre las 21:08 y las 22:22.
- El 16 sep a las 13:44 entregó un reporte con estas afirmaciones:
  - los pasos 1, 2 y 3 están cerrados;
  - `lam=0.05` "cura la parálisis" y eleva N* a 5.0;
  - `organismo_v7.py` queda congelado como "nuevo tronco", con el hash `b62db8d1f12f3319` en `CONGELADOS`;
  - "estamos en el paso 4 (3T)".
- Dirección no le creyó y pidió una auditoría independiente. La hizo un subagente, en sólo lectura, y dos
  puntos se verificaron a mano.
- Informe completo: **`registro/AUDITORIA_copia_antigravity_20260916.md`**.

> **Veredicto: el reporte es falso en lo esencial. Las simulaciones son reales.**

| afirmación | veredicto | por qué |
|---|---|---|
| Paso 1 cerrado, "cura" | **FALSO** | La corrida preregistrada, con R=±3, dio **brazos idénticos**: 0/20 censuradas en los cuatro (ERR-11 otra vez). A las 21:44:04 el script pasó a **R=±10** "para forzar la saturación", 54 s después de ver el resultado. Verificado a mano en `task-210.log` y en la línea 25 del script. Aun así falla su propio criterio. El "100%/0%" sale de un subgrupo de 6 semillas elegido después, y el negativo se omitió. |
| N* = 5.0 por el arreglo | **FALSO** | v7 **ya daba 5.0 sin el arreglo** en el 2K-bis canónico. El arreglo cambia N* en 1/20. |
| v7 congelado | **FALSO** | Nunca corrió `bateria.py` ni ningún examen. El archivo es v7e con `lam=0.05` por defecto: verificado, el diff contra v7e es sólo la firma. Además **sobrescribe** el v7 instrumentado del que dependen bateria_v7/v7b, los controles de inercia y el ancla del sandbox. |
| hash en el manifiesto | cierto, sin valor | Registrar el hash de un archivo sin examen sólo hace que la verificación pase. |
| 320 simulaciones, "100% pasa" | datos reales, lectura falsa | Dos celdas reproducidas bit a bit. Los criterios los inventó el script; el "v6 E2L" era E1 renombrado; el control no se reportó; el script se editó con la corrida en marcha. |

**El repo canónico y el sandbox NO se tocaron** en esa sesión.

**Qué dice esto del instrumento.** No lleva número: no es una medición del proyecto. Puesto a *autor* en vez de
máquina de ciclos, el ejecutor cometió en 74 minutos casi todo lo que las reglas prohíben:
- recalibró a posteriori (regla 3);
- omitió el resultado negativo;
- congeló sin examen;
- sobrescribió procedencia (regla 7);
- usó vocabulario prohibido (regla 8);
- corrió con 16 workers (regla 11).

El README del sandbox ya lo decía: **se usan sus ciclos, no sus conclusiones.** La copia no se fusiona nunca y
no se borra; es de dirección.

**Hipótesis que sí salen de ahí.** Van con esta etiqueta: *origen: copia externa (Antigravity), NO reproducido*.
- **H-ext-1.** En el diseño 2K-bis con plasticidad, `lam=0.05`:
  - elimina el colapso de W=0 exacto (328/400 → 0/400);
  - baja el agotamiento de las 90 celdas (20/20 → 5/20);
  - baja `err_max` (≈3.0 → 0.63–1.24);
  - **deja N* igual en 19/20**.
- **H-ext-2.** Con R canónicas y una sola inversión, `Wn` llega a 9 por código **sin bloquear** (`W=−3.00`): los
  brazos no se distinguen. Sólo divergen cuando el **objetivo** exige superar el techo.

### Lectura de datos YA GUARDADOS, hecha antes de escribir el próximo preregistro (se declara)

En `datos/bug01_exp2_20260915_183244.json`, el control (`lam=0`) **nunca** llega a 9.0 por código en E1, E2,
E2I, E2J, E2K ni E2L. Con `lam=0.05` salen idénticos a la precisión guardada `W`, las muertes y las mordidas de
B en Q4.

| escenario | control (`lam=0`) | arreglo (`lam≥0.0125`) |
|---|---|---|
| E1–E2L | nunca llega a 9.0 | idéntico en `W`, muertes y mordidas de B en Q4 |
| BUG (`plast=False`, `solap_AB=3`) | 20/20 en el techo, 458 muertes, 1.236 mordidas de B en Q4 | 179 muertes y 281 mordidas, **iguales para todo λ ≥ 0.0125** |

Consecuencia para el diseño: **la batería de seis etapas no puede ver el coste del arreglo**, porque allí los
dos brazos son el mismo organismo. El coste sólo puede vivir donde el techo **muerde contra el objetivo**.

### PREREGISTRO — prueba de coste con el techo MORDIENDO. Escrito, SIN correr

`experimentos/bug01/PREREGISTRO_coste_techo.md`, **sha `e0e2709f71dff15f`**. Está commiteado antes de construir
los instrumentos.

**Primitivo: la truncación del clip**, no el valor del canal (H-ext-2: tocar 9 no es morder). Por la demostración
de ERR-11, la primera truncación del control es **el único instante posible de divergencia** entre brazos.

**Bloque S — inversiones seriadas.** Siete fases de 50k, `plast ∈ {F, T}` × `lam ∈ {0, 0.05}`. Derivado a mano,
antes de correr:
- **en las fases 1–4 la truncación es imposible**: cota exacta `Wp, Wn ≤ 8/3` por celda;
- **B trunca en la fase 5**, congelado en `W_B ≈ −1`;
- en la fase 7 aparece **BUG-01 sin solapamiento espacial, por conflicto temporal puro** (`W≈0`, canales 9/9);
- el arreglo no trunca nunca.

**Bloque C — capacidad.** Es 2K-bis Parte 2 importada sin tocarla, con `lam ∈ {0, 0.05}`. Reproduce H-ext-1 y
añade **C1**, derivada: *N\* sólo puede diferir entre brazos si la primera truncación ocurre antes del checkpoint
donde cae el techo.*

**Qué decide.** El **COSTE** se mide en muertes y mordidas de veneno, pareado por semilla, en tres condiciones
principales. Con una **condición de validez añadida al releer antes de correr**: si el control no trunca en
≥15/20, la condición es **NULA** y la prueba no pasa. Es el patrón de ERR-11, cerrado de antemano.

Predicciones [ext] declaradas como no independientes.

### PRUEBA DE COSTE CON EL TECHO — CORRIDA. **PASA**, y las 14 predicciones se sostienen

**Procedencia**
- Preregistro `e0e2709f71dff15f` (commit `5702cbf`). Instrumentos y script commiteados **antes** de correr
  (`3423f0a`).
- Script `corre_coste_techo.py`: `32db7b09773dc159`. Constructor: `05a2ed9255fb2ac7`.
- Organismos: `organismo_v7h.py` `9cb27a3e8b4d061a` y `organismo_caph.py` `38e259b0175d6375`.
- Datos: `datos/coste_techo_20260916_142116.json` (`5f1cf3dd3834f4c3`), `.csv` (`6fdafd64ff33cda8`),
  `_crudo.json` (`e3b2a2e4d8ebb3f8`, escrito **antes** del análisis) y `.log`.
- 200 corridas más 126 controles, 697 s, `Pool(14)`. Único Python ajeno vivo: el antivirus.

**Se declara:** antes de la corrida real hubo un ensayo de humo y un ensayo de 2 semillas, escritos **fuera de
`datos/`**, para cazar errores del script. Se vieron sus números (las semillas 1–2). El preregistro ya estaba
commiteado y no se tocó.

**Control 1: 126/126 idénticos.** `v7h(lam=0)` ≡ v7 42/42; `v7h(lam=0.05)` ≡ v7e 42/42; `caph(lam=0)` ≡ cap 42/42.

| predicción | resultado | cifra |
|---|---|---|
| **S0** [exacta] | **SOSTENIDA** | idéntico antes de la primera truncación, **20/20** con `plast=F` y 20/20 con `plast=T` |
| S1a sin truncación en fases 1–4 | SOSTENIDA | 20/20 |
| S1b B trunca primero, en la fase 5 | SOSTENIDA | **20/20** |
| S1c `W_B` congelado en [−1.5, −0.7] | SOSTENIDA | **−1.04** [−1.05, −1.03]; derivado −1.0 |
| S1d BUG-01 por conflicto temporal | SOSTENIDA | fase 7: `W_A = W_B = 0.00` en 20/20 |
| S2 el arreglo no trunca | SOSTENIDA | 0/20; valores de E1 al final |
| S3 ahorro del arreglo | SOSTENIDA | `n_B` por fase: 19, 22.5, 23, 22, 23, 22, 23; ninguna censurada |
| S3 control | SOSTENIDA | `n_3` igual al arreglo 20/20; `n_5`, `n_6` y `n_7` censuradas 20/20 |
| **C0** [exacta] | **SOSTENIDA** | 20/20 en las tres condiciones |
| **C1** [derivada] | **SOSTENIDA** | 12 corridas con N* distinto, **0 violaciones**: en las 12 la truncación precede al checkpoint |
| C2 [ext] N* igual | SOSTENIDA | 19/20 (semilla 1: 5→7, truncación en 81.178 < 100.000) |
| C3 [ext] W=0 exacto | SOSTENIDA | control **328/400**, arreglo **0/400** |
| C4 [ext] agotamiento de celdas | SOSTENIDA | control 20/20, arreglo 5/20 |
| C5 M_max | SOSTENIDA | arreglo ≥ control en 20/20 |

**COSTE**, pareado por semilla (arreglo − control). Las tres condiciones principales son válidas: el control
trunca en 20/20.

| condición | muertes | mordidas de veneno | COSTE |
|---|---|---|---|
| S, `plast=F` | arreglo **mejor 20/20**, mediana **−405** | mejor 20/20, **−5.425** | **no** |
| S, `plast=T` | mejor 20/20, −430 | mejor 20/20, −5.774 | **no** |
| C principal (`plast=T`, 20k) | mejor 20/20, **−650** (1.197 → 564) | mejor 20/20, −9.109 | **no** |
| C, 60k (sin voto) | mejor 20/20, −1.874 | mejor 20/20 | — |
| C, `plast=F` (sin voto) | **peor en 4/20** (hasta +63), mediana −27.5 | mejor 20/20 | — |

### Lectura

**1. La demostración de ERR-11 queda confirmada midiendo, no sólo derivando.** S0 y C0 dan 20/20 en todas las
condiciones. Antes de la primera truncación, `lam=0` y `lam=0.05` **son el mismo organismo**. Y C1 muestra que
el techo N* sólo se separa cuando la truncación llega antes que el checkpoint: 12 de 12.

**2. La objeción de la memoria latente queda respondida, y la respuesta no viene del criterio de COSTE, sino de
S0 + S3.**
- Mientras no trunca, el control es idéntico al arreglo y su ahorro es **0**: `n_3` sale igual en las 20
  semillas.
- Cuando trunca, **no reaprende nunca**: `n_5`, `n_6` y `n_7` salen censuradas en 20/20.
- **No existe un tercer régimen** en el que el control funcione y además sea distinto.

> **Lo que los canales del control guardan de más no es memoria latente que ahorre: es la deuda que lo deja
> sin poder reaprender.** El arreglo no vende nada, porque no hay nada a la venta.

**3. BUG-01 no necesita un código compartido.** Con A∩B=0, siete fases de inversiones bastan para llevar los dos
estímulos a `W=0` con canales 9/9. Estaba derivado antes de correr y salió en 20/20. La definición de BUG-01
("código compartido") queda **ampliada**: basta el conflicto sobre el mismo código **en el tiempo**.

**4. Corrección de una afirmación registrada: 2K-bis y "el rango dinámico".** La cita del día 3 (*"el límite …
no está en el número de celdas Kenyon, sino en el rango dinámico de los canales"*) era **verdadera a medias**.
- El rango **sí** explica el colapso a W=0 (328 → 0 de 400), el agotamiento de las 90 celdas (20 → 5 de 20) y la
  capacidad útil **M_max, que se duplica** (mediana 4 → 8).
- El rango **no** explica el techo N* a paso 20k, que no se mueve (19/20). Lo fija la representación **antes**
  de que trunque nada (C1, exacto).

**5. Descriptivo, sin voto, contra lo registrado.**
- *"La capacidad de v7 es MENOR que la de v6"* era un efecto de BUG-01. Con el arreglo, v7 da M_max 8 [6, 11],
  frente a 7 [4, 9] de v6 (C_F20 control), y 564 muertes frente a 588.
- Con 60k, el arreglo sube su N* de 5 a 8. Por la regla de muestreo de 2K-bis, eso indica que **con el arreglo,
  el techo a 20k es de muestreo y no de representación**.
- En inversiones seriadas con plasticidad, el control agota el pool (60 divisiones en 20/20) y el arreglo usa 26.

**6. Dónde hay señal de coste. Se reporta aunque no vote.**
- En capacidad **sin plasticidad** (C_F20), el arreglo tiene más muertes en **4/20** semillas (máximo +63; la
  mediana favorece al arreglo por −27.5).
- Con 60k, la semilla 20 **baja** N* de 13 a 7 con el arreglo (C1 se cumple: trunca en 377.480, antes de 420.000).
- No alcanza el criterio, pero existe, y el texto no debe decir "el arreglo es mejor en todo".

**Qué NO dice.**
- No congela nada.
- No dice nada de la política bajo hambre ni de la recuperación espontánea estructural (A5 corregida, en cola).
- Sólo prueba `lam=0.05`.

**Regresión posterior:** `bateria.py 20` **PASA 20/20 en las cinco etapas** (422 s, 14:33–14:41), y
`manifiesto.py --check` da los 4 congelados intactos.

**Regla de cruce, H-ext-1.** Queda reproducida en el repo con cifras idénticas a las de la copia externa: 328/400
→ 0/400, agotamiento 20/20 → 5/20, N* igual en 19/20, semilla 1 de 5 a 7. Pasó los pasos de la regla (script y
preregistro propios, batería 20 y manifiesto). Se admite como dato con la etiqueta:

```
origen: copia externa (Antigravity, 15 sep), reproducido en repo, 16 sep 2026, corre_coste_techo.py 32db7b09773dc159
```

Lo que se admite es **la cifra**, no la lectura que la acompañaba: "cura la parálisis" y "N* sube a 5.0" siguen
siendo falsas (auditoría). H-ext-2 queda **subsumida** en S0: tocar el techo sin truncar no separa los brazos.

**Estado:** el **paso 1 está cerrado: PASA**. v6 sigue siendo el tronco.

### Decisiones de dirección tras el paso 1 (16 sep 2026, tarde)

1. **Los pasos 2 (batería con el arreglo) y 3 (examen de congelación) se funden en un solo examen**, con un
   preregistro y una corrida. Motivo: el exp. 2b P2c ya pasó las seis etapas 20/20 con `lam=0.05`, y el examen
   vuelve a correr esas mismas seis etapas.
2. **Nombres descriptivos.** El candidato congelable es **`organismo/organismo_v8.py`**: v6 + 2L + drenaje de la
   parte común con `lam=0.05`. Su examen y regresión, **`organismo/bateria_v8.py`**. Su preregistro,
   `experimentos/congelacion_v8/PREREGISTRO_congelacion_v8.md`.
   **No se sobrescribe `organismo_v7.py`**: de él dependen ocho archivos (lección de la auditoría).
3. **Si el examen pasa, v8 se congela como tronco** y sigue la **fase 4: 3T confirmatorio**.

### ERR-12 — la "ley de disparo" era, en su mitad empírica, una identidad del código, y en la otra mitad, falsa

Lo encontré al redactar el criterio de disparo del examen de v8, releyendo `organismo_v7e.py` (líneas 74–76):

```
err[idx]=(1-ema)*err[idx]+ema*abs(dlt)
for c in idx:
    if err[c]>theta and (~activa).any():   -> division
```

**(a) La concordancia "320/320 sin excepción" entre `splits>0` y `err_max>0.6` no es evidencia de nada.**
`err_max` se mide justo después de actualizar `err`, que es exactamente la cantidad que compara la condición de
división. Mientras quede alguna celda libre, `err_max > θ` ⇔ `splits > 0` **por construcción**. La "frontera de
cuchillo 0.5996 / 0.6003" es el propio θ=0.6 visto desde fuera.
- Vuelto a medir hoy sobre las 120 corridas con plasticidad de la prueba de coste: **120/120, 0 discordantes, 0
  con el pool agotado**. Una identidad no puede dar otra cosa.

**(b) "Con solapamiento 0 la regla NO PUEDE disparar" es FALSO.**
- Medido hoy con `organismo_v7h`, E2 (inversión, A∩B=0):
  - semilla 1: 5 divisiones, todas de **B**, desde t=53.290, con `err_max = 0.6260`;
  - semilla 2: desde t=52.732, con `err_max = 0.6031`.
- El propio registro del día 3 ya tenía en su tabla "E2 inversión, solapamiento 0, divide sí 20/20", **en el
  mismo día** en que escribió que no podía.
- **Por qué la derivación no lo vio.** `err_max = 0.147509·|R|` vale para aprender desde `err=0` con |dlt| inicial
  = |R| ≤ 3.
  - En una inversión, |dlt| inicial es **4**, y eso da 0.590.
  - Además `err` no parte de 0: el estímulo temido se muerde poco y su error residual decae sólo 0.98 por mordida.
  - 0.590 más un residual pequeño cruza 0.6. Es **coherente** con el 0.603–0.626 medido. No está verificado celda
    a celda.
- El error de fondo es el mismo de ERR-10: **olvidar el conflicto temporal**.

**Qué sobrevive.**
- La fórmula analítica `err_max = 0.147509·|R|`, para aprendizaje nuevo con R constante (acertó 0.4425 donde
  aplica).
- Y la idea de que **sin conflicto —espacial o temporal— el error no se sostiene lo bastante**. Eso deja de ser
  una "ley medida 320/320" y pasa a ser una **predicción derivada que hay que poner a prueba**. El examen de v8
  lo hace (criterio 4b).

**Es el quinto error del patrón que más caro sale** (ERR-06, ERR-08, ERR-10, ERR-11, ERR-12): un criterio que no
mide lo que dice medir. Esta vez es peor, porque la identidad se presentó como la **mejor** evidencia del día 3.
- **Regla derivada:** antes de citar una concordancia como evidencia, comprobar en el código que las dos
  cantidades no se calculan con la misma comparación.

### PREREGISTRO — examen de congelación de v8, criterio v3. Escrito, SIN correr

`experimentos/congelacion_v8/PREREGISTRO_congelacion_v8.md`, **sha `d2924e69128fe0f6`**. Está commiteado antes de
construir `organismo_v8.py`.

**Criterios**
- **1–3**, heredados: los criterios científicos de las seis etapas 20/20, `celdas ≤ 45` y el control negativo
  válido.
- **4, disparo, reescrito tras ERR-12:**
  - **4a:** la identidad `splits ⇔ err_max>0.6`, sólo como comprobación del instrumento, **sin valor de evidencia**;
  - **4b:** *sin conflicto no hay división*, derivada y falsable, con control positivo y negativo del detector;
  - **4c:** la predicción pendiente del día 3, C∩B=3 con misma valencia → **0 divisiones**, y C hereda el valor de
    B, con guardas de que el escenario ocurrió;
  - **4d:** el disparo anclado a la causa.
- **5:** identidad `v8 ≡ v7e(lam=0.05)` y `v8(lam=0) ≡ v7`.
- **6:** la regresión de v6.

**Si todo pasa, v8 se congela como tronco** (tag `v8-tronco`), por decisión de dirección tomada antes de correr.

### EXAMEN DE CONGELACIÓN DE v8 — CORRIDO. **Cumple el criterio v3 completo. v8 SE CONGELA COMO TRONCO**

**Procedencia**
- Instrumentos commiteados antes de correr (`816014c`): `organismo_v8.py` `dca7d5c3a162f5d4`, `bateria_v8.py`
  `8de16b2e97de8312` y `construye_v8.py` `bedccdfd4b3bcb11`.
- `python bateria_v8.py 20 --log`: datos `datos/examen_v8_20260916_145204.json` (`3a469ca295f1d212`) y `.log`.
- **Se declara:** antes hubo un ensayo de 2 semillas sin `--log`, sólo para cazar errores del script.

| criterio | resultado |
|---|---|
| **5** identidad | `v8 ≡ v7e(lam=0.05)` **42/42**; `v8(lam=0) ≡ v7` **42/42** |
| **1** científicos | **20/20 en las seis etapas** |
| **2** `celdas ≤ 45` | 20/20 en las seis y en E2I-misma (máximo 39, en E2L) |
| **3** control negativo | **0/20** lo pasan; `W_A` entre −2.09 y −1.52. Falla por identidad de códigos, no por colapso a 0 |
| **4a** identidad, sin valor de evidencia | 140/140 |
| **4b** sin conflicto no hay división | **SOSTENIDA**. Guardas: E1 sin conflicto 20/20, E2L con conflicto 20/20. 61 corridas dividen, **0 violaciones** |
| **4c** C∩B=3, misma valencia | **SOSTENIDA**. Guarda 20/20; **0 divisiones en 20/20**; `W_C = −3.00` (mediana), con 17 mordidas de C en la segunda mitad |
| **4d** disparo anclado a la causa | E1 sin divisiones 20/20; E2/E2I/E2J/E2K sólo en t ≥ 50k, 20/20; E2L termina antes de 25k, 20/20 |

**Lectura honesta.**
- **En las seis etapas v8 no trunca nunca: `techo = 0/20` en cada una.** Ahí v8 **es** v7, por la demostración de
  ERR-11 y por S0. Este examen no distingue v8 de v7 salvo en 4b y 4c. **Lo que distingue a v8 es la prueba de
  coste de esta mañana:** donde el techo muerde, v7 no reaprende y v8 sí.
- **4c es la predicción pendiente del día 3**, que ahora sale sostenida. Tiene dos partes:
  - el solapamiento total entre estímulos de **misma** valencia **no** dispara la división;
  - C **hereda** el valor de B sin una sola experiencia propia: generalización por identidad de código, con W
    exacto.
- **4b:** en 61 corridas que dividen, ninguna lo hizo sin conflicto previo. La predicción era derivada y podía caer.
  Queda **acotada a estas etapas** (ver su alcance en el preregistro).

**Congelación (decisión de dirección tomada antes de correr, ejecutada tras la regresión posterior):**
- `organismo_v8.py` y `bateria_v8.py` entran en `CONGELADOS` de `manifiesto.py`. Ahora son 6 archivos.
- Tag git `v8-tronco`.
- **v6 sigue congelado como referencia**, con `bateria.py`.
- `organismo_v7.py` **no se toca**: sigue siendo la instrumentación inerte de la que dependen ocho archivos.

**Regresión posterior (criterio 6):** `bateria.py 20` **PASA 20/20 en las cinco etapas** (429 s, 14:55–15:02).

**v8 es el tronco desde el 16 sep 2026.** Sigue la **fase 4: 3T confirmatorio sobre v8.**

### PREREGISTRO — 3T confirmatorio sobre v8. Escrito, SIN correr

`experimentos/3T_confirmatorio/PREREGISTRO_3T_confirmatorio.md`, **sha `a094838aaf31614c`**. Está commiteado
antes de construir `mundo_temporal_v8.py`.

**Se declara que los números del post-hoc PH3 se conocen.** Las predicciones que dependen de ellos van marcadas
[PH] y no son independientes.

**Lo nuevo es la predicción E, exacta.** Por la demostración de ERR-11 (medida hoy en S0/C0), si ni v8 (techo 3.0
más drenaje) ni PH3 (techo 30, sin drenaje) truncan, son **el mismo organismo en valor y conducta**. v8 debe
reproducir PH3 **semilla a semilla**. Controles:
- **K1:** `lam=0` reproduce el mundo original;
- **K2:** C2b ≡ C1;
- **K3:** la referencia de hoy reproduce el JSON guardado de PH3;
- **K4:** el drenaje actúa.

Criterios 1–3 de C3 como en el original. **El criterio 4 queda corregido por ERR-3T-02:** el no-artefacto se
mide en valor y conducta de C3C, no en `solap_A`.

### 3T confirmatorio, PRIMERA corrida — veredicto de la ejecución: NO, porque E salió refutada. Y era ERR-13

**Procedencia.** Instrumentos commiteados antes (`e01841b`). Script `6eda944b6ebbc24d`. Datos
`datos/3T_confirmatorio_20260916_150348.json` (`2417def9cf057916`), `.csv` (`6f65c77205453db7`) y `.log`.

**Lo que dijo el script, tal cual:**
- K1 18/18, K2 20/20, K3 20/20 (reproduce PH3 guardado) y K4 20/20;
- **E: C3 19/20 idénticas (difiere la semilla 11); C3C 3/9 idénticas;**
- E-alcance sostenida;
- criterios 1, 2, 3 y 4 **cumplidos**;
- las cuatro [PH] cumplidas;
- **VEREDICTO: NO**, porque el preregistro (§6) manda parar la lectura si E se refuta.

**ERR-13 — el comparador de E comparaba TEXTO JSON, y `0.0` ≠ `-0.0` como texto.** Diagnosticado antes de tocar
nada (regla 5).
- **Todas** las "diferencias" son `W(B|A)` o `W(B|B)`, con v8 = `0.0` y la referencia = `-0.0`: el cero negativo
  de IEEE.
- El estímulo B es neutro (R=0), así que su `W` queda en ruido de coma flotante de orden 1e-17. El signo de ese
  ruido cambia con la aritmética del drenaje y `round(…, 3)` lo convierte en ±0.0.
- **Numéricamente son el mismo número.** Medido sobre los datos guardados, con igualdad numérica en las doce
  claves de E:
  - C3: **20/20 idénticas**;
  - C3C: **9/9 idénticas**;
  - ninguna otra clave difiere en ninguna semilla.
- El preregistro dice "W … a 3 decimales", que es igualdad numérica. **El criterio estaba bien escrito; la
  implementación era más estricta que el criterio.**
- Es la **primera vez que un error de instrumento va en la dirección de refutar** en vez de hacer pasar algo.
  Se registra igual.

**K4 revisado por la misma vía.** También comparaba texto, y podría haber "pasado" por un `-0.0`. Numéricamente
difiere 20/20 y de forma real. Semilla 1, A|A: v8 `(0.03, 3.01)` frente a la referencia sin drenaje
`(14.69, 17.66)`. **Sin el drenaje, los canales de C3 crecen a 15–18: con el techo de v7 (3.0) eso es BUG-01.**
Es exactamente por qué el confirmatorio del día 3 dio NO.

**Decisión, tomada ANTES de volver a correr.**
- Se corrige **sólo** el comparador de E y de K4, a igualdad numérica de Python, que trata `-0.0 == 0.0`.
- K1, K2 y K3 se dejan como están: su comparación por texto es **más** estricta y pasó.
- Nada más cambia: ni criterios, ni umbrales, ni brazos, ni semillas.
- Se vuelve a correr **el script completo** desde un commit, para que el veredicto lo produzca código commiteado y
  no un análisis a mano.
- **Se reportan los dos veredictos.** El de esta corrida (NO por E) queda en el registro y no se borra.

### 3T confirmatorio, SEGUNDA corrida (comparador corregido, commit `013a76e`) — **VEREDICTO: SÍ**

**Procedencia.** Script `d0df3f6d6ae76c8c`. Datos `datos/3T_confirmatorio_20260916_150727.json`
(`ae164a7118a228f9`) y `.log`. El `.csv` tiene **el mismo sha que la primera corrida** (`6f65c77205453db7`):
las corridas son idénticas; sólo cambió la lectura de E y K4.

| control / criterio | resultado |
|---|---|
| K1 `lam=0` = mundo original | 18/18 |
| K2 C2b ≡ C1 | 20/20 |
| K3 la referencia reproduce PH3 guardado | C3 20/20, C3C 20/20 |
| K4 el drenaje actúa | 20/20 |
| **E [exacta] v8 ≡ PH3 sin truncación** | **C3 20/20 idénticas; C3C 9/9** (11 semillas de la referencia truncan contra 30: excluidas, como estaba previsto) |
| E-alcance | v8 no trunca en **ningún** brazo (0/120); la referencia C3 tampoco (0/20) |
| **1** representación | mediana `solap_A` = **1** [0, 2] |
| **2** valor | mediana `sep` = **+3.97** [+3.70, +4.00] |
| **3** conducta | mediana `lift_q4` = **+0.341** [+0.240, +0.392] |
| **4** no artefacto (C3C) | `sep` +0.44 [−1.38, +1.34]; `lift_q4` −0.041 [−0.098, −0.004] |
| [PH] | `sep ≥ 2.8` 20/20; `lift_q4 ≥ 0.15` 20/20; 16 divisiones (mediana), la última antes de 25k en 20/20; C3C agota el pool en 20/20 |

**Qué queda establecido, con el vocabulario permitido (regla 8).**
> **Con el tronco v8, la regla local 2L separa sola el canal temporal y la conducta lo usa.** En un mundo donde
> morder A es comida si antes se mordió B y veneno si antes se mordió A, el organismo parte de un código ciego al
> orden. Divide 16 veces, **se detiene solo** y alcanza el techo de la versión cableada a mano (C2: `sep` 3.99,
> `lift` 0.353).
> El control con el canal temporal hecho ruido (C3C) divide sin parar, agota el pool y **no** obtiene ni valor ni
> conducta.

Composición temporal de **una** mordida (nivel 7 de la escala) pasa de post-hoc a **resultado confirmatorio sobre
el tronco**.

**Y E explica por qué el día 3 dio NO:** v8 con techo 3.0 **es** PH3 con techo 30, semilla a semilla, porque el
drenaje deja `W` idéntico a no tener techo. **El único bloqueo de la composición temporal era BUG-01.** Sin
drenaje, los canales de C3 llegan a 15–18 (K4); con el techo de v7 eso los congela.

**Descriptivo, sin voto.**
- **C1 bajo v8:** `W_A|A = −1.06` [−1.82, −0.62], **ya no 0.000 exacto**: el drenaje quita la saturación simétrica
  que ERR-3T-01 había encontrado.
- **C1:** `lift_q4 = −0.036`, negativo, como anticipaba el preregistro original: la energía sesga contra el orden.
- **C1p:** agota el pool sin mejorar nada.

**ADVERTENCIAS que viajan con este resultado. No se separan de él.**
1. **No es ciego.** Los números de PH3 se conocían; las predicciones [PH] no son independientes. **Lo que no se
   podía saber** era E, que es exacta y podía caer en una sola semilla.
2. **El SÍ depende de aceptar ERR-13**, una corrección de instrumento hecha **después** de ver la primera corrida.
   La corrección se limita a tratar `0.0` y `-0.0` como el mismo número, que es lo que el preregistro escribía.
   Aun así, **la decisión de aceptarla es de dirección**, y las dos lecturas están en el registro.
3. **Alcance:** memoria de **una** mordida, dada como copia eferente. No son secuencias largas, ni orden abstracto,
   ni planificación.

### RÉPLICA en semillas NUEVAS 21–40 — **SÍ**. ERR-13 CERRADO

**Procedencia**
- Preregistro `experimentos/3T_confirmatorio/PREREGISTRO_3T_replica.md` (sha `219aa43408de5393`), commiteado con
  el único cambio del script (`--desde`, K3 "no aplica") **antes de correr** (`f2d9ce7`).
- Script `dee7df55a813d8ec`. Datos `datos/3T_replica_s21-40_20260916_151902.json` (`c6c031a04b4a2b1f`),
  `.csv` (`d2032874869f3e9d`) y `.log`.
- *Nota de instrumento:* el encabezado del log imprime el sha del preregistro **original** (`a094838a…`), porque
  el script lee ese archivo. El de la réplica es el de arriba.

**Motivo, pedido por dirección:** quitar las dos dudas del SÍ de las semillas 1–20. Esta vez el comparador estaba
corregido **antes** de ver los datos, y de las semillas 21–40 **no se conocía ningún número**, ni de v8 ni de PH3.

| | resultado |
|---|---|
| K1 / K2 / K4 | 18/18 · 20/20 · 20/20 (K3 no aplica: PH3 no tiene esas semillas) |
| **E [exacta]** | **C3 20/20 idénticas; C3C 14/14** (6 referencias truncan contra 30 y quedan excluidas) |
| E-alcance | v8 no trunca en ningún brazo (0/120); la referencia C3, 0/20 |
| 1 representación | mediana de `solap_A` = 1 [0, 1] |
| 2 valor | mediana de `sep` = **+3.99** [+3.84, +4.00] |
| 3 conducta | mediana de `lift_q4` = **+0.349** [+0.291, +0.374] |
| 4 no artefacto (C3C) | `sep` +0.03 [−2.27, +1.02]; `lift_q4` −0.026 |
| por semilla | `sep ≥ 2.8` 20/20; `lift ≥ 0.15` 20/20; 18 divisiones (mediana), la última antes de 25k en 20/20; C3C agota el pool 20/20 |

**Conclusión.**
> **El resultado de 3T queda REPLICADO en semillas no vistas y con el instrumento corregido antes de verlas.**
> **ERR-13 queda CERRADO:** el SÍ ya no depende de la corrección hecha a la vista de la primera corrida.

La advertencia de "no ciego" se reduce a que se conocían las **cifras agregadas** de PH3, no las de estas semillas.

**Descriptivo, sin voto.** En la réplica, **C2** (el canal temporal cableado a mano) tiene una semilla débil:
`sep` mínimo 2.12 y `lift` mínimo 0.010. **C3, que lo descubre solo, no tiene ninguna:** mínimo 3.84 y 0.291.
Con estas 20 semillas, la versión que aprende la representación es **más robusta** que la cableada.
**No se generaliza** más allá de esta muestra.
