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

---

## Día 4, tarde — cerrar lo que falta de las Etapas 2 y 3 (orden de dirección)

### Replanteamiento, escrito antes de diseñar nada

Pensado antes de actuar, como pidió dirección. **Las dos etapas estaban planteadas de forma que podían "cerrarse"
sin probar lo que importa.**

**Etapa 2, 2P.** La fórmula de la boca, `σ((1.2·W + hb·h + 0.5)/0.3)`, muestra que `hambre_boca` **no cambia** la
mordida de la comida conocida (0.9966) ni la de lo nuevo (0.841). **Sólo cambia cuánto se prueba lo temido**, y
probar lo temido es la única vía para descubrir que el mundo cambió.
- **Hipótesis:** la mordida de veneno con hambre es **exploración disparada por necesidad**, no un defecto.
- **Riesgo:** optimizar sólo en E1 la "arreglaría" rompiendo la reversibilidad sin que E1 lo vea.
- **Decisión:** el criterio es funcional, **muertes en E1 y E2 a la vez**. Con eso se cierra la pregunta abierta del
  día 2 (tasa frente a conteo).

**Etapa 3.**
- La versión dura del día 3 prueba si la fórmula nominal se rompe con solapamiento. Eso es casi seguro y mide el
  instrumento más que al organismo.
- **Lo que falta de verdad lo dice el propio registro:** *"no prueba que el organismo ACTÚE según él"*. La
  generalización demostrada es de valor, nunca de conducta.

**Plan, un experimento por vez y cada uno preregistrado:**
1. Frontera hambre–supervivencia en E1 y E2.
2. Sólo si hace falta: la sorpresa como disparador de la exploración (candidato a v9).
3. Etapa 3 versión dura sobre v8.
4. Generalización **en conducta** al primer encuentro, con regla lineal y no lineal.

### PREREGISTRO — frontera hambre–supervivencia (Etapa 2). Escrito, SIN correr

`experimentos/etapa2_politica/PREREGISTRO_frontera_hambre.md`, **sha `902f1f0223ef597b`**. Está commiteado antes
de construir `organismo_v8p.py`.

**Diseño:** `hambre_boca ∈ {0, .5, 1, 1.5, 2, 2.5, 3}` × {E1, E2} × 20 semillas.

**Predicciones derivadas:**
- **F2:** la reversión cae con `hb = 1` (≤5/20) y se sostiene con `hb = 2` (≥18/20);
- **F3:** sin exploración, en E2 se muere de hambre (≥1.5× muertes);
- **F4:** en E1 la exploración cuesta poco (muertes ±10%);
- **F5:** v8 está en el óptimo combinado;
- **F6:** demasiada exploración también mata.

### FRONTERA HAMBRE–SUPERVIVENCIA — CORRIDA. No pasa como estaba escrita, y cambia el problema de la Etapa 2

**Procedencia.** Instrumentos commiteados antes (`e30ea03`). Script `corre_frontera_hambre.py`. Datos
`datos/frontera_hambre_20260916_153342.json` (`d1c34dfa94d594dd`), `.csv` (`348a445324f05521`) y `.log`.
280 corridas más 42 controles.

| hb | muertes E1 | muertes E2 | combinado | E2 revierte | veneno E1, 2ª mitad | comida E1, 2ª mitad |
|---|---|---|---|---|---|---|
| 0.0 | 156 | 208.5 | 364.5 | 0/20 | 2 | 129 |
| 0.5 | 154 | 184 | 338 | 0/20 | 3.5 | 140.5 |
| 1.0 | 151 | 161.5 | 312.5 | **10/20** | 5.5 | 138.5 |
| 1.5 | 149.5 | 155 | 304.5 | 19/20 | 10.5 | 137.5 |
| **2.0 (v8)** | **142** | 146.5 | **288.5** | 20/20 | 27 | 150.5 |
| 2.5 | 148 | 146 | 294 | 20/20 | 59 | 180 |
| 3.0 | 155.5 | 156.5 | 312 | 20/20 | 88.5 | 195.5 |

| criterio | veredicto | cifra |
|---|---|---|
| F0a / F0b instrumento | OK | 42/42 · reproduce el examen de v8 40/40 |
| F1 contador | **REFUTADA** (ERR-14, ver abajo) | 49/51 celdas en banda |
| F2 umbral de reversibilidad | **REFUTADA** | con `hb = 1` revierten **10/20**; predije ≤5 |
| F3 sin exploración se muere en E2 | **REFUTADA** | ×1.10 con `hb = 1`, predije ≥1.5 (con `hb = 0`: ×1.42) |
| F4 en E1 la exploración cuesta poco | **SOSTENIDA, pero por la razón equivocada** | muertes **+9.9%** con `hb = 0`: **suben**, no bajan. Pasó por la banda de ±10% |
| F5 v8 en el óptimo combinado | **SOSTENIDA** | el mínimo está **exactamente** en `hb = 2.0` |
| F6 demasiada exploración mata | **REFUTADA por margen** | ×1.095, predije ≥1.10 |

**Lo que sí se sostiene (lo cualitativo).**
- **Sin exploración no hay reversión:** 0/20 con `hb ≤ 0.5`.
- **v8 está en el óptimo medido** de supervivencia combinada, y también en el de E1 solo.

**Lo que salió mal en mis predicciones.**
- El umbral de reversión es más bajo de lo que estimé (50% con `hb = 1`).
- El efecto de morir de hambre en E2 es más débil. Medido por mitades: la segunda mitad pasa de 74 a 86.5 muertes
  con `hb = 1` (×1.17) y a 129 con `hb = 0` (×1.74).
- **Y en un mundo estable, quitar la exploración NO reduce las muertes: las AUMENTA.** Razoné lo contrario.

**ERR-14 — la banda de validación de F1 era más estrecha que el ruido de Poisson.**
- Con ≥20 mordidas esperadas, la desviación típica de Poisson es ~±22%, y la banda [0.8, 1.25] es ≈ ±1σ.
- Calculado: **1.56 celdas fuera de banda esperadas sólo por azar; observadas 2**. P(fuera | 21.5) = 0.34 y
  P(fuera | 25.3) = 0.28.
- **El contador está bien; el criterio no.** Es un criterio de validación escrito sin el ruido de muestreo. No
  produjo ningún dato falso. Se numera porque decidió un veredicto.

### HALLAZGO del diagnóstico — **el organismo pasa ~20% de su vida parado sobre el veneno**

Salió al preguntar por qué, con menos exploración, se come **menos** comida (129 frente a 150), si la boca no
cambia la mordida de comida.

- **Pasos sobre objetos veneno en la 2ª mitad de E1:**

  | hb | pasos | % del tiempo | pasos por mordida de veneno |
  |---|---|---|---|
  | 0 | 9.940 | 19.9% | 4.970 |
  | 1 | 10.296 | 20.6% | 1.872 |
  | 2 | 10.040 | 20.1% | 372 |
  | 3 | 11.626 | 23.3% | 131 |

  Con 4 objetos en un anillo de 40 y la mitad veneno, **al azar** estaría encima de un veneno ~5% del tiempo.
  Observado: **~4× más, y casi igual para todo hb**.
- **Mecanismo probable, NO verificado.** Las patas aprenden a acercarse al objeto más cercano: hay premio por
  acercarse y la comida se come en `d = 0`. Por diseño del día 1 ("miedo sólo en la boca"), **no tienen ninguna
  razón para irse** del objeto que la boca rechaza. Se estacionan hasta que el mundo lo retira (p = 0.003 por paso,
  repartido entre 4 objetos).
- **La U de muertes en E1 se explica, como hipótesis, por la renovación del mundo.** Cada veneno mordido desaparece
  y reaparece un objeto al azar (50% comida). Se observan ~0.5–0.8 mordidas de comida extra por cada mordida de
  veneno extra, compatible con esa vía. **Morder veneno con hambre limpia el mundo.** Es la trampa del punto 15
  del brief ("explotar el entorno"), encontrada esta vez en el organismo y no en el diseño del experimento.

**Consecuencia para la Etapa 2.**
- El problema de conducta **no es** "muerde veneno el 1–4% con hambre": eso resultó ser exploración útil, y v8 está
  en su óptimo.
- **El problema real es que las patas no saben alejarse de lo temido**, y eso cuesta ~20% del tiempo de vida.
- **La Etapa 2 NO se cierra con este experimento.** Su regla de cierre exigía F2–F5 y no se cumplió. Queda
  replanteada con un problema medido y un mecanismo candidato.

### EXPLORACIÓN — "órganos" que faltan: dimensionados y probados (subagente, SIN valor confirmatorio)

**Encargo de dirección:** un loop de variantes medidas con varianza para saber qué órganos funcionales le faltan
al organismo para explorar y decidir.

**Procedencia**
- Lo ejecutó un subagente (modelo Fable) **fuera del repo**, en `JUACO/exploracion/organos_20260916/`.
- Informe `INFORME.md` (`f7a3ff032a9d2ec0`), constructor `construye_v8x.py` (`92cccc24fa24f302`), variante
  `organismo_v8x.py` (`976bfe7061456b04`), datos `corridas_20260916_160957.csv` (`0324bdd418400838`).
- 864 corridas, 20 semillas (1–20), E1 y E2. Cada variante con el órgano apagado es idéntica a v8 (8/8 por
  construcción).
- `bundle/` y `sandbox/` sin tocar, verificado.
- **Las cifras clave de O3 y D0 las recalculé yo desde el CSV, y coinciden.**

**Todo lo que sigue es hipótesis con evidencia exploratoria.** Las semillas 1–20 quedan vistas: la confirmación se
hará en semillas nuevas.

**Ronda 0: diagnóstico del atasco. Corrige lo que escribí esta tarde.**
- **No está "parado" encima: oscila atado al objeto más cercano.** En E1, segunda mitad, hay 7.142 llegadas a
  veneno con **1.42 pasos por llegada**.
- **La línea de azar que usé (5%) estaba mal.** El 92% de los objetos vivos son veneno, porque la comida se come al
  llegar. Un paseo uniforme daría **9.2%**, así que el exceso es **×2.2, no ×4**.
- **El atasco se aprende.** Con las patas sin aprendizaje (D1) baja a 9.73%, exactamente el azar corregido (exceso
  1.10), en 20/20.
- **Mi mecanismo sospechado era falso.** Quitar la señal "estoy encima" (D2) no cambia nada: esa entrada no puede
  frenar, sólo empujar. El vehículo es la **política de objetivo** (`see()` elige siempre el objeto más cercano) más
  las entradas de dirección.
- **Las tasas "por visita" (por paso) del registro están diluidas ×1.42** frente a "por llegada" (0.251% frente a
  0.370%). Afecta a las cifras del día 2–3 y a la frontera de hoy; **ninguna cambia de signo**.

**ERR-15 — dos afirmaciones mías de esta tarde, falsas por el instrumento de comparación.**
1. **"Al azar estaría encima ~5%":** supuse que la mitad de los objetos eran veneno. La composición real del mundo
   vivo es 92% veneno.
2. **"Se estaciona":** interpreté pasos como estancia. Eran llegadas repetidas.

El hallazgo cualitativo (se aprende un exceso de tiempo sobre el veneno) **se sostiene**; su magnitud y su mecanismo
no. Es otra vez el patrón de **la línea base mal puesta**.

**Ronda 1–2: un órgano por variante, pareado frente a v8.**

| órgano | efecto | veredicto exploratorio |
|---|---|---|
| O1 valor→movimiento (señal "encima" con valor) | ≈ 0; actúa sobre una entrada inerte | descartar |
| O2 habituación | ≈ 0; misma entrada inerte | descartar |
| O4 sorpresa como disparador de exploración | 0 mordidas de veneno en E1, pero **rompe E1 (7/20) y E2 (8/20)**, come menos y no muere menos | descartar tal cual: es `hb = 0` con otro nombre |
| **O3 memoria de trabajo de rechazo** (ignorar como objetivo un objeto rechazado durante τ = 20 pasos) | **veneno 20.1% → 9.8%** (exceso 1.01; 20/20 bajan, en E1 y en E2); llegadas a veneno 7.142 → 3.969; comida +7.5; **muertes −8.5 en E1 (16↓ 3↑), −17.5 combinadas (17↓ 3↑)**; criterios de E1 y E2 20/20 | **candidato a preregistrar** |

**La varianza del mecanismo (ronda 2) importa.** O3 **no es monótona en τ**:

| τ | % del tiempo sobre veneno |
|---|---|
| 20 | 9.8% |
| 50 | 12.9% |
| 150 | 16.9% |

Con τ largo se rechazan los cuatro objetos, no queda objetivo y vuelve la política original (fallback: 1.8% → 57%
→ 75%). **El parámetro importa por lo que pasa cuando no hay objetivo.** El agente señala un órgano que nadie pidió:
**O7, "qué hacer sin objetivo"**.

**O5 (mapa de lugares) y O6 (consolidación/fusión)** quedan dimensionados por escrito, sin implementar.
- O5 no tiene nada que mapear en este mundo.
- O6 exige medir antes si hay fragmentación.

**Lectura.** El órgano que falta para decidir dónde ir no está en el valor ni en la habituación: es **memoria de
trabajo** ("acabo de rechazar esto, busca otra cosa"). Encaja con la tabla de mecanismos del HANDOFF, donde cada
órgano lo pidió una falla medible.

### PREREGISTRO — v9 = v8 + memoria de trabajo de rechazo. Escrito, SIN correr

`experimentos/v9_memoria_rechazo/PREREGISTRO_v9.md`, **sha `f68841597adb55d8`**. Está commiteado antes de construir
`organismo_v9.py`. **τ = 20 queda fijado y no se barre.**

**Confirmatorio en semillas nuevas 21–40**, con cuatro brazos: v8, v9, C1 (memoria sobre un objeto al azar) y C2
(τ = 1).
- **M0:** identidades, incluida la de v9 con la variante del agente.
- **M1:** el tiempo sobre veneno baja ≥6 pp en ≥18/20.
- **M2:** las muertes combinadas no suben.
- **M3:** no come menos.
- **M4:** el fallback es < 5%.
- **M5:** no-regresión de E1 y E2.
- **M6:** C1 y C2 no reproducen el efecto.

**Después, examen de congelación** con el criterio v3 sin cambiar un umbral.

**Si pasa todo:** v9 es el tronco y **la conducta de la Etapa 2 se cierra**.

### v9 — CONFIRMATORIO (semillas 21–40) PASA M0–M6 · EXAMEN criterio v3 PASA 20/20 · **v9 SE CONGELA COMO TRONCO**

**Procedencia**
- Instrumentos commiteados antes de correr (`b7c4a82`): `organismo_v9.py` `d3b72fb8819fbe8e`, `bateria_v9.py`
  `c6496196990f6774` (generada desde `bateria_v8.py` con sustituciones contadas; el diff demuestra que no cambia
  ningún criterio ni umbral) y `organismo_v9c.py` `8495dbe81e8b5749`.
- Confirmatorio: `datos/v9_confirmatorio_20260916_162904.json` (`e7a4aaffeb40ab0c`), `.csv` (`be479b0cdcf0340a`)
  y `.log`.
- Examen: `datos/examen_v9_20260916_163138.json` (`9a2c0797bde6d0a5`) y `.log`.
- Humo declarado: semilla 2, T=20000, fuera de las semillas confirmatorias.

**Confirmatorio, semillas nuevas 21–40:**

| | v8 | **v9** | C1 (memoria al azar) | C2 (τ=1) |
|---|---|---|---|---|
| veneno E1, 2ª mitad | 21.50% [16.3, 25.1] | **9.60%** [9.2, 11.0] | 26.43% | 21.50% |
| veneno E2 | 21.22% | **9.21%** [8.2, 9.8] | 25.18% | 21.22% |
| sin objetivo | 0% | 1.9% | 1.8% | 0% |
| muertes E1 / E2 | 143.5 / 148 | **133.5 / 132.5** | 149 / 150 | 143.5 / 148 |
| criterios E1 / E2 | 20 / 19 | **20 / 20** | 20 / 19 | 20 / 19 |

| | veredicto | cifra |
|---|---|---|
| M0 identidades | ✅ | `v9(0)` ≡ v8 42/42; `v9c` ≡ v9 6/6; **v9 ≡ variante exploratoria del agente 6/6** |
| M1 efecto | ✅ | pareado **−11.7 pp (E1) y −12.1 pp (E2)**; ≤ −6 pp en **20/20** en los dos |
| M2 muertes combinadas | ✅ | mediana **−24**, ≤ 0 en 18/20 |
| M3 comida | ✅ | +3 |
| M4 fallback | ✅ | 1.9% |
| M5 no-regresión | ✅ | E1 20/20, E2 20/20 (v8 hace 19/20 en E2 con estas semillas) |
| M6 controles | ✅ (C2 no informativo, ver ERR-16) | v9 −11.70 pp; **C1 +5.35 pp**; C2 +0.00 |

**Examen de congelación de v9** (criterio v3, semillas 1–20): **8/8**.
- identidad `v9(0)` ≡ v8 42/42;
- científicos **20/20 en las seis etapas**;
- `celdas ≤ 45`;
- control negativo 0/20;
- 4a 140/140;
- **4b sostenida** (63 corridas dividen, 0 sin conflicto previo);
- **4c sostenida** (0 divisiones, `W_C = −2.99`);
- 4d 20/20.

**Regresión:** `bateria_v8.py 6` cumple y `manifiesto.py --check` da los 6 congelados intactos.

**ERR-16 — el control C2 (τ=1) era un no-op por construcción.**
- La memoria se guarda como `_rech[pos] = t + τ` y se consulta como `_rech[x] > t` en el paso siguiente. Con τ = 1,
  en `t+1` la condición es `t+1 > t+1`, falsa: **nunca filtra nada**.
- C2 salió idéntico a v8 número por número. Por eso "pasó" su parte de M6: **por construcción, no por evidencia.**
- **Qué queda en pie:** la conclusión se sostiene con M1 y con **C1**, que sí discrimina. Recordar un objeto al azar
  en lugar del rechazado **empeora** el atasco (+5.35 pp).
- **Qué no queda probado:** "la duración mínima necesaria". La dependencia de τ sólo tiene evidencia exploratoria
  (20 → 9.8%, 50 → 12.9%, 150 → 16.9%, semillas 1–20).
- Mismo patrón de siempre, en un control: **releer que el control pueda hacer algo antes de fiarse de que no lo haga.**

**Congelación** (decisión de dirección tomada antes de correr):
- `organismo_v9.py` y `bateria_v9.py` entran en `CONGELADOS`; ahora son 8 archivos.
- Tag **`v9-tronco`**.
- v8 y v6 quedan congelados como referencia.

### ETAPA 2 — CONDUCTA: **CERRADA** con v9

Las dos piezas que faltaban están ahora medidas y preregistradas:
1. **Explora lo temido con hambre, y eso es lo que le permite revertir.**
   - Sin esa exploración, 0/20 revierten.
   - v8, y v9 que conserva la boca, está exactamente en el **óptimo medido** de supervivencia en un mundo estable y
     en uno que cambia (frontera, `hb = 2.0`).
2. **Ya no se queda atado a lo que rechaza.**
   - Memoria de trabajo de rechazo: el tiempo sobre veneno pasa de ~21% a ~9.5%, en torno al azar corregido.
   - Muere menos y revierte igual o mejor, confirmado en semillas no vistas.

Etapa 2: **valor cerrado (día 2, 2G), conducta cerrada (día 4, v9).**

**Pendiente, dicho explícitamente:**
- 3T y 2K-bis eran sobre v8 y **no se han re-corrido sobre v9**.
- ERR-16 deja sin probar la duración mínima de la memoria.
- El órgano O7 ("qué hacer sin objetivo") queda abierto.

### PREREGISTRO — Etapa 3 sobre v9: versión dura y generalización EN CONDUCTA. Escrito, SIN correr

`experimentos/etapa3_v9/PREREGISTRO_etapa3_v9.md`, **sha `5a2af284ee73ae76`**. Está commiteado antes de construir
`organismo_v9g.py`.

**Lo que se detectó al diseñar.** La "precisión 0.683" de 3K mezcla la generalización con lo aprendido después, a
lo largo de 100.000 pasos, y la mide "por visita". **La conducta al primer encuentro nunca se midió.**

**Diseño**
- **Versión dura (VD):** residuo de la fórmula nominal en E1 (control), E2J, E2K y el mundo de 20 patrones.
  Predicción: crece con el solapamiento.
- **Generalización (G):** mundo de 20 patrones de peso 3 con reglas `px0` (lineal), `azar` (control) y `xor01`
  (frontera). Se mide el valor a priori y la **probabilidad de morder al primer encuentro** con los patrones de
  test.

**Decide el cierre:**
- **G1:** valor `px0` ≥ 0.65 y por encima de `azar` en ≥ 14/20.
- **G2:** conducta `px0` ≥ 0.55 y por encima de `azar` en ≥ 14/20.

G3 (XOR) y VD se reportan sin bloquear el cierre.

### ETAPA 3 sobre v9 — CORRIDA. **G1 y G2 SOSTENIDAS: LA ETAPA 3 SE CIERRA** (en valor y en conducta)

**Procedencia**
- Instrumentos commiteados antes de correr (`eac1727`): `organismo_v9g.py` `e7021992c857d244`, derivado de v9
  congelado.
- Datos `datos/etapa3_v9_20260916_164240.json` (`526e6c0cac66975c`), `.csv` (`cf6ad4072b6c9114`) y `.log`.
- 120 corridas más 24 controles.
- Humo declarado: semilla 4, T=20000, fuera del diseño.

**K (instrumento):** `v9g('AB')` ≡ v9 21/21; con sonda final 3/3; cobertura del primer encuentro 20/20 en los tres
mundos.

**Generalización, sobre los patrones de test, nunca vistos antes del primer encuentro:**

| mundo | valor a priori (exactitud de signo) | **conducta al primer encuentro** (`BA_pb`) | mordidas reales al primer encuentro | pareado frente a `azar` |
|---|---|---|---|---|
| **`px0` (lineal)** | **0.800** [0.60, 1.00] | **0.798** [0.54, 0.99] | **comida 70% · veneno 15%** (n = 100 + 100) | valor **19/20**, conducta **18/20** |
| `azar` (control) | 0.500 [0.30, 1.00] | 0.497 | comida 48% · veneno 47% | — |
| `xor01` (no lineal) | **0.438** [0.19, 0.69] | 0.450 | comida 38% · veneno 49% | por debajo de `px0` en 19/20 |

- **G1 SOSTENIDA:** 0.800 ≥ 0.65; `azar` 0.500 dentro de [0.35, 0.65]; 19/20.
- **G2 SOSTENIDA:** 0.798 ≥ 0.55; `azar` 0.497 dentro de [0.42, 0.58]; 18/20.
- **G3 (sin voto) SOSTENIDA:** XOR 0.438 ≤ 0.60 y por debajo de `px0` en 19/20.
  - Además queda **por debajo del azar**: los vecinos por código de un patrón XOR tienden a tener la valencia
    contraria. Es anti-generalización medible, no sólo ausencia.
- Alcance (W = 0 exacto en test): 0 en los tres mundos. Truncaciones: 0 en todos.

**Versión dura (preregistrada el día 3, adaptada a v9):**

| escenario | residuo nominal mediano |
|---|---|
| E1 | 0.0067 |
| E2J (D∩B = 1) | **0.203** |
| E2K (D∩B = 2) | **0.634** |
| mundo `px0` (10 estímulos) | **1.406** |

- **VD2 SOSTENIDA:** E1 < E2J en 20/20 y E2J < E2K en 20/20.
- **VD3 SOSTENIDA:** `px0` > E2K en 18/20.

**Primera medida de cuánto degrada la interferencia la regla nominal de generalización:** crece ~×3 por cada celda
compartida y ~×2 más con 10 estímulos.

**VD1 REFUTADA (residuo máximo en E1 < 0.01: sólo 1/20), con la causa diagnosticada.**
- En E1, el residuo máximo por semilla es **exactamente** `|W_B + 3|` (0.0095 a 0.0392). Con los `W` reales, la
  fórmula es exacta (residuo máximo **4.4e-16**, la identidad del día 3).
- La diferencia con el día 3 (v6: 5.9e-3) es que **en v9 `W_B` converge menos**: −2.96 a −2.99, mediana
  `|W_B+3|` = 0.020. La memoria de rechazo hace que v9 muerda menos veneno, y hay menos muestras de B.
- **Error de predicción mío:** arrastré el umbral de v6 sin considerar que el órgano nuevo cambia la exposición al
  veneno. Es el patrón de ERR-06/08 ("asumir que todo se comporta igual"). No produjo ninguna medición falsa.
- **No bloquea el cierre**, porque VD no decidía; VD2 y VD3, que miden la degradación, se sostienen.

### ETAPA 3 — **CERRADA** con v9

> **Con una característica lineal (un píxel), v9 asigna valor a patrones que nunca ha visto (acierto 0.80 frente
> a 0.50 del control) y ACTÚA según ese valor en el primer encuentro: muerde la comida nueva el 70% de las veces y
> el veneno nuevo el 15%, frente a 48% y 47% en el control.**
> **Con una característica no lineal (XOR) no generaliza.** La generalización vive en el solapamiento de códigos
> de una proyección aleatoria, y la interferencia la degrada de forma medible.

Vocabulario (regla 8): "generaliza" con criterio preregistrado sostenido. **No** es abstracción, ni transferencia
entre dominios, ni aprendizaje de reglas no lineales.

**Etapas del brief:** 1 cerrada · **2 cerrada** (valor y conducta) · **3 cerrada** (valor y conducta, característica
lineal) · 4 memoria persistente, parcial · 5 en adelante, pendientes.

**Pendiente, dicho explícitamente:**
- 3T y 2K-bis sobre v9;
- la frontera no lineal (XOR) como problema abierto de representación;
- O7.

### RE-VERIFICACIÓN sobre v9 — 3T y 2K-bis: **los dos sobreviven**

**Procedencia**
- Preregistro `experimentos/v9_reverificacion/PREREGISTRO_reverificacion_v9.md` (`2708cb73ab8531e8`, commit
  `fb8a155`). Instrumentos commiteados antes de correr (`dd08056`): `mundo_temporal_v9.py` `18d96a1c79863bb0` y
  `organismo_caph9.py` `1b113605dc803435`.
- Datos: `datos/reverificacion_v9_20260916_165658.json` (`111e25284b7b0e6d`) y `.log`.

**Controles:** KT1 18/18 (`memoria=0` ≡ `mundo_temporal_v8`); KK1 12/12 (`memoria=0` ≡ `caph`); KT2 C2b ≡ C1 20/20;
**KK2 reproduce N\* y M_max de v8 guardados, 20/20**.

**3T sobre v9 — T1–T4 SOSTENIDAS.**

| brazo | sep | lift_q4 | solap_A | divisiones |
|---|---|---|---|---|
| **C3** | **+3.93** [3.72, 3.97] | **+0.383** | 1 | 17 |
| C3C | −0.37 [−1.84, +1.11] | −0.043 | 0 | 60 (agota el pool 20/20) |

- En v8, C3 daba `lift_q4` +0.341; con v9 la conducta de composición **mejora ligeramente** (sin voto).
- 0 truncaciones en todos los brazos.

**2K-bis sobre v9 — K1–K3 SOSTENIDAS.**

| | N\* | M_max | W=0 exacto | agotan | muertes |
|---|---|---|---|---|---|
| 20k v8 | 5.0 | 8.0 | 0/400 | 5/20 | 564 |
| 20k **v9** | 5.0 | 8.0 | 0/400 | 4/20 | **514** |
| 60k v8 | 8.0 | 12.0 | 0/400 | 15/20 | 1.650 |
| 60k **v9** | 8.0 | 11.5 | 0/400 | 11/20 | **1.521** |

**Dicho con honestidad (sin voto):** pareado, M_max baja algo con v9.
- a 20k: mediana −0.5 (sube en 6 semillas, baja en 10);
- a 60k: mediana −1.0 (sube en 7, baja en 12).

Queda **dentro** de la tolerancia preregistrada (−1), pero la dirección es de coste pequeño. A cambio, **muere menos**:
−50 (bajan 16/20) y −131.5 (bajan 17/20).

**Lectura.** La composición temporal y la corrección de 2K-bis **valen sobre el tronco v9**. La memoria de rechazo
cambia a dónde van las patas y cuesta, quizá, una fracción de estímulo en capacidad útil, a cambio de supervivencia.

### PREREGISTRO — Etapa 4 sobre v9 (memoria persistente). Escrito, SIN correr

`experimentos/etapa4_v9/PREREGISTRO_etapa4_v9.md`, commiteado antes de construir `organismo_v9m.py`.

**Propiedades de arquitectura declaradas y NO "probadas":**
- la memoria sobrevive a la muerte por construcción;
- sin aprendizaje durante la ausencia, la retención es exacta (se usa como control).

**Se mide:**
- **Bloque M:** ausencia de A y B mientras se aprenden C y D.
  - M1: control exacto;
  - M2: recuerda (`W_B ≤ −2`, `W_A ≥ 0.5`);
  - M3: la interferencia es medible.
- **Bloque H:** herencia **cero / parcial (valor sin patas) / completa** en mundo **igual** o **invertido**.
  - H1/H3: ventaja en mundo igual;
  - **H4: desventaja en mundo invertido**;
  - H5: aun así se adapta.

### DISEÑO (no preregistro) — comunicación y aprendizaje simbiótico

Pedido de dirección. Queda en `experimentos/etapa5_comunicacion/DISENO_comunicacion_simbiotica.md`.
- **Definición operativa** de comunicación: 5 condiciones, y **no** copiar pesos.
- **Escalera:**
  - N0, control ecológico (dos organismos sin señal);
  - **N1, señal innata honesta de placer/asco con aprendizaje vicario**;
  - N2, significado aprendido (juego de señalización, criterio de emergencia del punto 14);
  - **N3, simbiosis complementaria:** dos organismos con sentidos distintos que juntos resuelven lo que ninguno puede
    solo, como la frontera XOR de la Etapa 3.
- Trampas y controles, y el primer experimento propuesto (N1).

### ETAPA 4 sobre v9 — CORRIDA. **NO se cierra: v9 sufre OLVIDO CATASTRÓFICO por interferencia**

**Procedencia**
- Preregistro `9f14cd3b1b1150b3` (commit `b930c9e`). Instrumentos commiteados antes de correr (`1bdc080`):
  `organismo_v9m.py` `8afa74b805ba2102`.
- Datos: `datos/etapa4_v9_20260916_170519.json` (`d15df10103ebb5a1`) y `.log`.
- Instrumento: `v9m` ≡ v9 21/21; herencia corre 3/3.
- **Humo declarado**, con fases cortas: en una corrida la interferencia ya se veía grande.

**Bloque M — ausencia con interferencia** (A y B fuera en [50k, 100k); se aprenden C veneno y D comida):

| | resultado |
|---|---|
| **M1** control sin aprendizaje en la ausencia | **SOSTENIDA**: `W_A` y `W_B` en 100k idénticos a 50k, 20/20 |
| **M2** recuerda | **REFUTADA**: `W_B` de −2.924 a **−0.344** [−3.80, +2.26], conserva el miedo en **7/20**; `W_A` de +1.000 a +0.572, en 10/20 |
| **M3** la interferencia es medible | **SOSTENIDA**: cambio > 0.01 en 18/20, mediana **3.92** |
| (sin voto) primer reencuentro con B | `pb` mediana **0.60**; **muerde B en 10/20**. Olvido también en la conducta |

**Bloque H — herencia** (cría con semilla 1000 + s):

| mundo | modo | veneno en Q1 | muertes Q1 | muertes Q1+Q2 | muertes totales |
|---|---|---|---|---|---|
| igual | cero | 30.5 | 32.0 | 66.0 | 135.0 |
| igual | parcial | **7.0** | 35.0 | 66.5 | 137.0 |
| igual | completa | **6.5** | 29.5 | 64.5 | 132.5 |
| invertido | cero | 32.0 | 34.5 | 66.5 | 137.5 |
| invertido | parcial | 33.0 | 36.5 | 68.5 | 136.0 |
| invertido | completa | 36.5 | 40.0 | **74.0** | **146.0** |

- **H1 SOSTENIDA:** heredar el valor ahorra ~80% del veneno inicial en un mundo igual (6.5 frente a 30.5, 20/20).
  Lo explica el valor heredado, no las patas: `parcial` también da 7.0.
- **H3 REFUTADA por margen:** muertes en Q1, `completa` < `cero` en **14/20**; se pedían 15.
- **H4 REFUTADA:** en el mundo invertido, `completa` > `cero` en **12/20**. La dirección de las medianas es la
  predicha (74 frente a 66.5 en Q1+Q2, 146 frente a 137.5 en total), pero sin la consistencia exigida.
- **H5 SOSTENIDA:** aun heredando la memoria equivocada, revierte al final en 20/20.

### DIAGNÓSTICO del olvido (sin valor confirmatorio): **dos vías, y las divisiones lo triplican**

**Qué se corrió.** Brazo `sin_plast`: igual que el bloque M con aprendizaje, pero con `plast=False` en toda la
corrida. En E1, v9 no divide nunca, así que la fase 1 no cambia; sólo se quitan las divisiones de la ausencia.
Script en el scratchpad de la sesión, 20 corridas.

| | ΔW_B mediana | ΔW_A mediana | conserva el miedo a B |
|---|---|---|---|
| con plasticidad (bloque M) | **+2.569** | −0.428 | 7/20 |
| sin plasticidad | **+0.837** | 0.000 | 10/20 |

- **corr(|ΔA| + |ΔB|, divisiones durante la ausencia) = +0.87.**
- **Control interno:** en las 6 semillas sin divisiones (4, 6, 10, 12, 17, 19), los dos brazos dan **exactamente el
  mismo** Δ.

**Lectura.**
1. **Interferencia de valor:** D (comida) comparte celdas con B y empuja su valor hacia arriba; C (veneno) comparte
   celdas con A y lo empuja hacia abajo. Como **A y B no están**, nadie lo corrige. Es la deriva sin re-muestreo que
   2I ya había medido ("misma valencia: deriva no corregida"), aquí sin el estímulo presente y durante 50.000 pasos.
2. **Interferencia estructural:** las divisiones provocadas por C y D **reescriben los códigos** de A y B, la vía de
   A5, y **triplican** el olvido.

**Consecuencia.** La memoria de v9 es exacta si no aprende nada, pero **no protege lo aprendido de lo que se aprende
después**. Falta un órgano de **consolidación** (O6, dimensionado por escrito en la exploración de órganos): que lo
consolidado resista la sobrescritura, y que lo nuevo reclute celdas en vez de pisar las de otros.

**La Etapa 4 NO se cierra.** Sostenido: M1, M3, H1, H5. Refutado: M2, H3 (por margen), H4.

### EXPLORACIÓN — órgano de consolidación (subagente Fable, SIN valor confirmatorio)

**Procedencia**
- Carpeta `JUACO/exploracion/consolidacion_20260916/`: `INFORME.md` (`9d2e4b47c4df39c9`), `organismo_v9k.py`
  (`846641af7297714d`) y datos R1 (`8aa6e1fc5b1ba8f2`), R2 (`90f5fe8c8a6316be`) y R3 (`09402c382b7e3f3d`).
- ~1.020 corridas, semillas 1–20, bloque M de la Etapa 4. Identidad 21/21. `bundle/` y `sandbox/` sin tocar.
- **Verificado por mí desde los JSON:** el control reproduce `W_B(100k)` del registro 20/20; K4 r=200 da 17/20
  (`W_B`) y 20/20 (`W_A`); K4 r=100, 20/20 y 20/20; K4c r=200, 9/20 y 11/20; K5, 10/20 y 11/20.
- El agente paró a mitad de la ronda 1 esperando un aviso que no llegó. Se lo reanudó sin tocar nada.

**1. Diagnóstico refinado. Corrige lo que registré.**
- La vía estructural es la catastrófica, y **no es "la madre se mueve": son las HIJAS las que toman el código de B**.
  En 11 semillas, las 3 celdas del código de B en 100k son hijas, y B lee el valor de D (+0.99).
- **Causa:** B·D = 2, y `mu` (EMA con tasa 0.02 que arranca en 0) **subestima** el patrón viejo. La hija no se aleja
  de B.
- **Predicción mía refutada:** "fijar la madre recupera la retención". K1 queda igual al control (7/20), **y rompe
  E2L** (1/20). El agente la había refutado **por derivación, antes de correr**.

**2. Variantes**

| variante | retención (B / A) | aprende C y D | no-regresión | veredicto exploratorio |
|---|---|---|---|---|
| K1 madre fija | 7 / 11 | sí | **rompe E2L** | descartar |
| K2 metaplasticidad (κ=50) | 4 / 10 | frena lo nuevo | E2 más lento | descartar sola |
| K3 reclutamiento temprano | 3 / 12 | sí | 22 divisiones | descartar así |
| **K4 repaso** (almacén episódico patrón → último R, repaso cada r pasos) | **17–20 / 20** | sí (r=100: `W_D` 20/20) | E1/E2/E2L 20/20 | **retiene, pero la memoria vive en el almacén** |
| K4c (almacén borrado en cada fase) | 9 / 11 | sí | — | **control:** sin A y B en el almacén, cae al nivel del control |
| **K5 `mu` normalizada** (1 línea, 0 parámetros) | 10 / 11 | sí | **E2 y E2L en 3 divisiones exactas, 20/20** | arregla la mitad de la vía estructural; ninguna vía **sin** almacén supera 11/20 |

**3. Lectura (con cuidado; es la trampa "memoria escondida" del punto 15 del brief)**
- **K4 es "memoria episódica de pocas casillas + repaso"**, no un endurecimiento de `Wp/Wn`.
  - Funciona, tiene análogo biológico (el repaso del hipocampo) y el agente lo documentó con sus controles.
  - Pero **cambia la naturaleza del organismo**: añade un almacén explícito. En un mundo con 4 estímulos, 4 casillas lo
    guardan todo.
  - Probarlo en serio exige un mundo con **más estímulos que casillas**.
- **K5 es la corrección de un defecto de la regla 2L:** la dirección de división usaba una media que no había
  convergido, algo que el preregistro de 3T ya había anticipado como modo de fallo.
  - Es un cambio de una línea, sin parámetros, que además hace la plasticidad más económica.
  - Por sí sola no cierra la Etapa 4.
- **Propuesta del agente para v10:** K4 con r=100 y n=8, con cinco controles de artefacto, y K5 como brazo secundario.
  **La decisión de cuál entra primero, o si van los dos, es de dirección.**

### ETAPA 5, N1 — señal innata honesta y aprendizaje vicario. **NO se demuestra**

**Procedencia**
- Preregistro `experimentos/etapa5_comunicacion/PREREGISTRO_N1.md` (`ed4c995020f9ff4a`, commit `ee6f3c9`).
- Instrumento `mundo_social.py`, escrito antes del preregistro y sin ejecutar hasta después. Script commiteado antes de
  correr (`74decdf`).
- Datos: `datos/N1_20260916_174236.json` (`cd15946bc4b2395f`) y `.log`.
- Humo declarado (semilla 7, T=20k): ya sugería que S1 podía caer.

**Instrumento:**
- K1: `mundo_social(n=1)` ≡ v9, 6/6.
- K2: señales recibidas: N0 0; N1, mediana 156 por semilla.
- K3: BAR, mediana 190, dentro de ±50%.

**E1** (mediana por organismo):

| condición | veneno propio hasta el criterio | veneno Q1 | muertes | aprendizajes vicarios sobre B |
|---|---|---|---|---|
| SOLO | 19 | 30 | **132** | 0 |
| N0 (dos, sin señal) | 19 | 39 | **177.5** | 0 |
| **N1** (señal honesta) | **18** | 37 | 179 | 22 |
| BAR (barajada) | 20 | 43 | 167 | 31 |

| criterio | veredicto | cifra |
|---|---|---|
| **S1** aprende del asco del otro | **REFUTADA** | N1 18 frente a N0 19; se pedía ≤ 13.3 |
| **S2** simbiosis (ganan los dos) | **REFUTADA** | 9/20; se pedían ≥ 15 |
| **S3** importa el contenido | **SOSTENIDA** | BAR 20 ≥ N0 19; la señal barajada empeora |
| S4 (E2, sin voto) | "verdadera", pero **no informativa** | `t_ext_B`: N1 52.466 < N0 52.860, **pero BAR 52.162 es aún más rápida**. La extinción más rápida no es contenido: las señales "placer" al azar sobre B también la empujan |

**Lectura (qué dice el fallo).**
1. **Dos aprendices igual de ignorantes a la vez no tienen nada que enseñarse.**
   - Cada uno aprende que B es veneno en sus primeras ~19 mordidas, muy al principio.
   - Las señales útiles del otro llegan a la vez o después, y de a pocas: ~30% dentro del alcance, tasa 1/3.
   - **La comunicación sólo puede valer donde hay asimetría de información:** uno sabe y el otro no (experto y
     novato, o un mundo que cambió para uno). Ese es el rediseño; va con preregistro nuevo, sin recalibrar
     `d_senal` ni `f_vicaria` (regla 3).
2. **Ser dos cuesta mucho: +34% de muertes por organismo** (177.5 frente a 132), aun con 4 objetos por cabeza.
   - Hay competencia por la comida en un anillo compartido.
   - BAR muere **menos** que N0 aunque muerde **más** veneno: otra vez la renovación del mundo al morder veneno
     (frontera de la Etapa 2).
3. **Lo que sí queda:** el contenido de la señal importa (S3). La vía de transmisión existe; lo que falta es una
   situación en la que valga la pena.

**Etapa 5, N1: NO demostrado.** Queda el diseño y un problema bien planteado.

### DECISIÓN DELEGADA (dirección: "decide tú") — v10 = v9 + dirección de división con `mu` normalizada

Preregistro `experimentos/v10_direccion_division/PREREGISTRO_v10.md` (`0e035dc12f3fffd3`, commit `296d1ac`).
Instrumentos commiteados antes de correr (`51de86d`): `organismo_v10.py` `219d5033fe15b5b9` (diff funcional con v9:
la firma y **una** línea), `bateria_v10.py` `d354813d3fa9d0f1` (23 líneas de nombres, ningún criterio), `v10m`
`c33253b850570308`. Datos: `datos/v10_confirmatorio_20260916_175557.json` (`ea0fd051edf61d0a`),
`datos/examen_v10_20260916_175716.json` (`d2f6de7350514291`) y sus `.log`.

| criterio | veredicto | cifra |
|---|---|---|
| Q0 identidad | ✅ | `v10(mu_norm=False)` ≡ v9 42/42; `v10m` ≡ v10 6/6 |
| **Q1** examen criterio v3 | ✅ **8/8**, seis etapas 20/20 | |
| **Q2** economía de la plasticidad | ✅ | **E2 y E2L terminan con exactamente 3 divisiones en 20/20** (v9: medianas 5 y 6) |
| **Q3** vía estructural (semillas 21–40) | ❌ **REFUTADA como está escrita** | hijas en B: v9 14/20 ✅, **v10 6/20 (pedía ≤ 5)**; ΔW_B v10 < v9 en **11/20 (pedía ≥ 12)**; v10 peor por > 0.5 en **1 semilla (pedía 0)** |
| Q4 retención, con guarda | ✅ | `W_B ≤ −2`: v9 7/20 → v10 **10/20**; `W_C`, `W_D` aprendidos 20/20 |
| Q5 regresión | ✅ | `bateria_v9.py 6` cumple; 8 congelados intactos |

**Por la letra del preregistro, v10 NO se congela.** Nada se recalibra.

**Descriptivo, que importa:** ΔW_B mediana +2.24 (v9) → **+0.86** (v10); `W_B` al volver −0.69 → **−2.06**; celdas hijas en
el código de B: 32 → **8**; muerde B al reencuentro 9 → 5; divisiones en la corrida 6 → 3.

### ERR-17 — los tres subcriterios de Q3 estaban mal escritos, cada uno por una razón distinta

Diagnóstico desde el JSON (`scratchpad`, sin simular), regla 5:
1. **Los empates contaban como fallo.** `mu_norm` sólo actúa **al dividir**. En **6/20** semillas ninguno de los dos
   brazos dividió durante la ausencia, así que ΔW_B es **idéntico por construcción** (v10 = v9 exacto). Entre los 14
   pares no empatados, v10 es menor en **11/14**. El criterio "≥ 12/20" exigía que v10 ganara también donde no
   podía diferir. Es la familia de ERR-11/16: un criterio que no puede cumplirse por construcción en parte de la
   muestra.
2. **El umbral de hijas contradecía la evidencia declarada.** Escribí "v10 ≤ 5/20" habiendo declarado en §0 que la
   exploración daba "0 hijas en 11/20", es decir, **hijas en 9/20**. El umbral era inconsistente con mi propio prior.
3. **Tolerancia cero sobre una diferencia pareada estocástica** ("nunca > v9 + 0.5"). Con 20 pares y una cola larga
   de divisiones (v9 llega a 19 divisiones en una semilla), un caso al revés no refuta nada. Es ERR-14 otra vez (banda
   más estrecha que el ruido).

**Qué se decide, antes de volver a correr (regla 3):**
- v10 sigue **sin congelar**. El examen (Q1, Q2) y Q4 valen y no se repiten.
- Criterio Q3 corregido, para una **réplica en semillas nuevas 41–60**, escrito desde el mecanismo y no desde las
  cifras de 21–40: (a) entre los pares **no empatados**, v10 < v9 en ≥ **70%**; (b) semillas con ≥ 1 hija en el código
  de B: v10 ≤ **la mitad** de v9 (pareado en recuento) y ≤ 9/20; (c) v10 peor por > 0.5 en ≤ **2/20**. Se corre sólo
  si dirección decide seguir; si pasa, v10 se congela.
- Se declara que los datos de 21–40 se vieron antes de escribir (a)–(c).

### JUACO-EVO — evolución del organismo guiada por LLM, con control ciego. GENERACIÓN 1

**Origen.** Dirección pidió liberar al organismo: *"un sistema evolutivo de auto-crecimiento que nos deje el código de su
evolución… usar técnicas de los LLM para que evolucione más rápido"*. Traducción operativa (decisión de Claude, delegada):
el genoma es el código; un LLM propone mutaciones con hipótesis; un evaluador automático con currículo fijo y semillas
retenidas selecciona; una rama ciega es el control. Antecedentes declarados: AlphaEvolve, Darwin Gödel Machine,
ShinkaEvolve. Preregistro `experimentos/evo/PREREGISTRO_evo.md` (`684e5da82227e04d`, commit `e057b3a`), instrumentos
commiteados antes de seleccionar (`1a6d177`), candidatos con hipótesis commiteados antes de evaluar (`d233b80`).

**Padre (gen 0), `organismo_v10m`:** válido; retención R = 0.3 (semillas 1–10) y 0.4 (retenidas 11–20).

**Generación 1** (4 mutaciones LLM en clases distintas + 4 ciegas; `experimentos/evo/LINAJE.md`):
- **Ganador: `llm_2` (regla estructural).** Sustituye el disparo `err > θ` por **conflicto de signo** (una celda con
  valor consolidado recibe refuerzo contrario), la hija nace **ciega fuera de los píxeles del patrón nuevo**, **la madre
  no se mueve** y el valor se **fisiona** (la hija se lleva el signo nuevo, la madre conserva el viejo).
  **R = 1.0 en 1–10 y 1.0 en 11–20** (padre 0.3 / 0.4), con E1 bit-idéntico al padre, E2 10/10, E2L en 3 divisiones,
  C y D aprendidos 10/10, y sigue dividiendo en la ausencia (3–5). Predijo 0.8–0.9. Auditoría del diff: retiene por el
  mecanismo declarado. **Es hipótesis del archivo, no tronco.**
- `llm_3` (repaso por celda con puerta de edad) también R = 1.0, con estado nuevo declarado; perdió el empate por muertes.
- `llm_1` retuvo 0.5 **a costa de no aprender D** (H3 la invalidó; su autor lo había declarado como razón equivocada).
- `llm_4` sin efecto. Ciegas: 0.3–0.4.

**ERR-18 — el evaluador podía ser explotado por constantes de constitución.** `ciega_4` subió la energía tras morir de
0.6 a 1.06: muertes 127 → 96 (S 0.36 → 0.52) sin aprender nada distinto, y con R = 0.4 la regla mecánica lo aceptaba.
Corregido antes de continuar (enmienda 1 del preregistro): operador ciego v1 con constitución y mundo protegidos,
misma prohibición a los LLM, linaje ciego rehecho desde el padre original. Es el patrón del punto 15 del brief ("explotar
el entorno"), esta vez atrapado por la auditoría y no por el criterio.

**Lo que ya dice la generación 1 sobre las preguntas preregistradas:**
- **P1 (aceleración):** el linaje LLM alcanzó R ≥ 0.8 en **una** generación; el linaje ciego se está corriendo (v1).
- **P2 (interpretabilidad):** el ganador tenía mecanismo e hipótesis escritos antes; 12 líneas.
- **P4 (hackeo):** dos razones equivocadas detectadas (una por criterio, una por auditoría).

**Advertencia que viaja con esto:** que `llm_2` retenga 10/10 en un mundo de cuatro estímulos **no** dice qué pasa con
veinte. Cada conflicto de signo fabrica una hija ciega; el pool de 90 celdas puede agotarse. Es la primera pregunta de
la generación 2 y del futuro confirmatorio.

### JUACO-EVO — linaje CIEGO terminado (control de P1) y corte de la generación 2

**Linaje ciego** (`muta_ciega` v1, constitución protegida, desde `organismo_v10m`, 24 mutaciones en 6 generaciones,
16 sep 18:54–19:14; `experimentos/evo/gen{1..6}c/`, `linaje_ciego.log`): termina en **R 0.5 (1–10) / 0.4 (11–20)**. No
alcanza R ≥ 0.8. Aceptó tres cambios: recompensa de acercamiento de las patas, una mutación nula (ERR-19) y el umbral de
las patas; ninguno mejora la retención en semillas retenidas. Hubo un sobreajuste atrapado por las retenidas (P3) y dos
candidatos que subían R rompiendo la reversión (H1).

| pregunta | veredicto | cifra |
|---|---|---|
| **P1** aceleración | **SOSTENIDA** | LLM: R ≥ 0.8 en **1** generación (4 mutaciones). Ciego: no llega en **6** (24 mutaciones) |
| P2 interpretabilidad | sostenida (gen 1) | el ganador LLM tenía mecanismo e hipótesis escritos antes; 12 líneas |
| P3 sobreajuste | **observado** | 1 caso (ciego gen1c) atrapado por las semillas retenidas |
| P4 hackeo | **observado, 3 casos** | llm_1 (retiene sin aprender D, H3), ciega_4 v0 (energía tras morir, ERR-18), mutación nula (ERR-19) |

**Límite honesto de P1.** El operador ciego sólo escala constantes: **no puede crear un mecanismo nuevo por
construcción**. P1 demuestra que un LLM explora el espacio de *reglas* y el ciego sólo el de *parámetros*; no demuestra
que el LLM gane a una búsqueda ciega sobre reglas (programación genética). Esa comparación queda pendiente.

**ERR-19.** `selecciona.py` comparaba el `S+E−C` del hijo (C respecto de su padre) con el guardado del padre (C respecto
del abuelo): una mutación `0.0 → 0.0` ganó en gen4c. Corregido: SEC del padre con C = 0. No altera R ni P1.

**Generación 2 LLM: no se ejecutó.** Los cuatro operadores lanzados desde `gen1/llm_2` se cortaron por el **límite de uso de
la sesión** (HTTP 429, 16 sep ~19:10) antes de escribir nada; `gen2/` no existe. No hay datos parciales que descartar.

**Pendiente antes de cualquier tronco:** `gen1/llm_2` es hipótesis del archivo. Necesita (1) confirmatorio en semillas nuevas
21–40 con preregistro propio, (2) examen criterio v3 con 20 semillas, y (3) la prueba de capacidad (más estímulos que
celdas), porque cada conflicto de signo fabrica una hija y el pool de 90 puede agotarse.

## DÍA 5 (17 sep 2026) — v11: el primer órgano del tronco NACIDO POR EVOLUCIÓN GUIADA

Preregistro `experimentos/v11_evo_division/PREREGISTRO_v11.md` (`a7c6a485718dab46`), commiteado con los instrumentos
ANTES de correr (`210e821`). Datos: `datos/v11_confirmatorio_20260917_070339.json` (`497ec7075e304be2`) y
`datos/examen_v11_20260917_071012.json` (`6a63bec1f637e35a`), con sus `.log`.

**Semillas.** 1–20 las usó la selección de EVO; 21–40 las leyó el autor de la mutación para diagnosticar al padre (lo
declaró). **Todo esto corre en 41–60, que nadie había visto.**

**Q0 instrumentos:** `v11m` ≡ genoma evolucionado 12/12; `v11m(div_signo=False)` ≡ `v10m` 9/9; `caph11` ≡ `caph9` 12/12;
`caph11(T,T)` ≡ v11 3/3. En la batería: `v11(mu_norm=False, div_signo=False)` ≡ v9 42/42 y `v11(div_signo=False)` ≡ v10 42/42.

### Retención con interferencia (bloque M, semillas 41–60)

| brazo | retención conjunta | W_B(100k) | W_A(100k) | aprende C y D | muerde B al volver | divisiones | celdas |
|---|---|---|---|---|---|---|---|
| v9 | **0/20** | +0.43 | −0.09 | sí | 15/20 | 8 | 38 |
| v10 | **2/20** | −1.79 | −0.09 | sí | 7/20 | 4 | 34 |
| **v11** | **20/20** | **−3.00** | **+1.00** | sí (20/20) | **0/20** | 5 | 35 |

R1 (≥16/20) ✅ · R2 (v11−v10 ≥ +6): **+18** ✅ · R3 guarda (≥18/20): **20/20** ✅ · R4 mecanismo (códigos de A y B
intactos de 50k a 100k, ≥14/20): **20/20** ✅. **La retención ocurre por el mecanismo declarado**, no por otra vía.

### Capacidad (2K-bis, 20 estímulos, semillas 41–60)

| paso | brazo | N\* | M_max | agotan el pool | celdas | divisiones |
|---|---|---|---|---|---|---|
| 20k | v10 | 5.0 [3, 8] | 7.0 | 1/20 | 78 | 48 |
| 20k | **v11** | **20.0 [17, 20]** | **14.0** | **0/20** | **61** | 31 |
| 60k | v10 | 8.5 [5, 16] | 11.0 | **12/20** | 90 | 60 |
| 60k | **v11** | **20.0 [20, 20]** | **16.0** | **0/20** | **62** | 32 |

K1 ✅ K2 ✅ K3 ✅. **No sólo no pierde capacidad: la multiplica**, con menos celdas y sin agotar el pool, mientras v10
lo agota en 12 de 20 semillas a 60k. Muertes iguales (512 y ~1.555 en ambos brazos).

**ADVERTENCIA, y es importante: el instrumento de capacidad se saturó.** `N* = 20` es el **techo de la prueba** (sólo
existen 20 estímulos de peso 3 sobre 6 píxeles). No sabemos cuál es la capacidad real de v11, sólo que es ≥ 20. Hace
falta un mundo con más estímulos (píxeles o pesos distintos) para encontrar su límite. Hasta entonces, **no se puede
escribir "capacidad 20"; se escribe "≥ 20, techo del instrumento"**.

### Examen y regresión
`bateria_v11.py 20 --desde 41 --log`: criterio v3 **8/8**, seis etapas 20/20, control negativo 0/20, 4a' (identidad de
contabilidad, declarada antes de correr en sustitución de la 4a de la regla `err>θ`), 4b, 4c y 4d pasan.
`bateria_v9.py 6` cumple; 12 congelados intactos.

### Réplica de v10 (ERR-17, criterio corregido escrito antes): **(b) FALLA**
(a) v10 < v9 en 13/18 pares no empatados (≥70 %) ✅ · **(b) semillas con hija en el código de B: v9 17, v10 11; se pedía
≤ la mitad y ≤ 9: ❌** · (c) peor por >0.5 en 2/20 ✅. **v10 no se congela como tronco**: se congela como **instrumento**
(la identidad de v11 lo necesita). Su corrección de `mu` es real pero insuficiente por sí sola; **v11 la incluye**.

### Decisión (por el preregistro, sin recalibrar nada)
**v11 SE CONGELA COMO TRONCO** (tag `v11-tronco`; `organismo_v11.py` y `bateria_v11.py` a CONGELADOS, con v10 y
`bateria_v10.py` como instrumentos). **Etapa 4 (memoria persistente): CERRADA en el mundo de 4 estímulos.**

### Lo que esto significa, dicho con cuidado
1. **Un órgano propuesto por un LLM, seleccionado por un evaluador automático y auditado por el protocolo, sobrevive en
   semillas que nadie vio y mejora dos cosas a la vez** (retención y capacidad) sin romper ninguna de las seis etapas.
2. **No es magia ni es inédito**: fisionar una traza ante un conflicto de signo tiene parientes en la literatura
   (asignación de engramas, separación de patrones). Lo nuestro es que **apareció por búsqueda guiada** y está medido.
3. **Riesgo abierto y no medido:** la hija nace **ciega fuera del patrón** que la dispara. Eso separa códigos… y podría
   **destruir la generalización a patrones nuevos** (Etapa 3) y la composición temporal (3T), que se midieron sobre v9.
   **Hasta re-verificarlas, v11 es mejor sólo en lo medido.** Es lo siguiente que se corre.

### Capacidad de v11 en un mundo GRANDE (retina de 10 píxeles, 60 estímulos) — G1 y G2 sostenidas, **G3 refutada**

Preregistro `experimentos/capacidad_grande/PREREGISTRO_capacidad_grande.md` (`c98776664cb80377`), commiteado con los
instrumentos antes de correr (`13101f7`). Datos `datos/capacidad_grande_20260917_142455.json` (`da01ae07dc73a73d`).
Instrumento `organismo_capD.py` (`85afad3f0769891f`): la retina pasa a ser parámetro. **G0 comprobado:** con 6 píxeles
es `caph11` **exacto** (semillas 1–3, brazos v9 y v11) y `mundo_grande(6, 20)` reproduce `parte2_capacidad`.
120 corridas, semillas 41–60, 1,2 M y 3,6 M pasos. El organismo **no cambia**: 30 celdas de nacimiento, tope 90.

| paso | brazo | N\* (mediana [min, máx]) | M_max | estímulos al agotarse el pool | muertes |
|---|---|---|---|---|---|
| 20k | v9 | 4.0 [2, 6] | 16.5 | 21 | 1630 |
| 20k | v10 | 6.0 [3, 9] | 21.0 | 28 | 1686 |
| 20k | **v11** | **43.5 [6, 60]** | **28.5** | 33.5 | 1617 |
| 60k | v9 | 8.0 [5, 27] | 20.0 | 19.5 | 5119 |
| 60k | v10 | 9.0 [7, 18] | 24.0 | 28 | 5204 |
| 60k | **v11** | **50.0 [31, 60]** | **32.0** | 32.5 | 4849 |

- **G1 [N\*(v11) ≥ 20]: SOSTENIDA** (43.5 y 50.0). La lectura de ayer era el techo del instrumento; la capacidad real
  es mucho mayor. **En 3 semillas a 60k aprende los 60 estímulos**, así que el instrumento nuevo también se satura
  en parte: lo honesto es "mediana 50 de 60, rango 31–60".
- **G2 [ventaja sobre v10 ≥ +5]: SOSTENIDA** (+37.5 y +41.0). No era un artefacto del mundo pequeño.
- **G3 [el límite lo pone el pool de celdas]: REFUTADA.** Los **tres** brazos agotan las 90 celdas en 20/20 semillas
  (60 divisiones), v11 hacia el estímulo ~32. Pero v11 **sigue aprendiendo después de quedarse sin celdas** hasta ~50,
  mientras v10 se queda en 9. Mi predicción de mecanismo era falsa.

**Diagnóstico post-hoc (exploratorio, desde el JSON; no decide nada):** el error mediano |W−R| de v11 es **0.02** justo
antes de agotar el pool, **0.02** al agotarlo, **0.11** diez estímulos después y **0.16** más allá. No hay precipicio:
hay **degradación suave**. Es decir, **el pool marca el final de la fase barata** (separación casi perfecta mientras hay
celdas libres), **no el techo**: después, los códigos comparten celdas y el error crece poco a poco. Lo que distingue a
v11 de v10 no es tener más celdas —las gastan igual— sino **con qué se queda cuando se acaban**: madres de un solo
signo, sin la mezcla que arrastra a v10 (su error final es 0.59–0.63 frente a 0.30–0.41).

**Qué se puede escribir ahora:** *"en este mundo, v11 sostiene una mediana de 50 estímulos de 60 con 90 celdas, frente a
9 de v10; agota las celdas hacia el estímulo 32 y a partir de ahí se degrada suavemente en vez de colapsar"*. **No** se
puede escribir que el límite sea el número de celdas: eso quedó refutado.

**Pendiente:** encontrar el techo real de v11 (hace falta un mundo de más de 60 estímulos), y las dos re-verificaciones
que siguen abiertas sobre v11: generalización (Etapa 3) y composición temporal (3T).

### Re-verificación sobre v11: **3T sobrevive, la GENERALIZACIÓN NO.** v11 es un canje, y el canje tiene mecanismo

Preregistro `experimentos/v11_generaliza/PREREGISTRO_v11_generaliza.md` (`f51cfd0f1f8a01c6`), commiteado con los
instrumentos e hipótesis **antes** de correr (`9d55c44`). Marco de lectura fijado antes por dirección en
`registro/NOTA_v11_pattern_separation_20260917.md` (CLS 1995 frente a Sahay 2011 / Clelland 2009).
Datos `datos/v11_generaliza_20260917_151145.json` (`e3576c31509d51c1`). 420 corridas, semillas **41–60**, los tres
brazos con **el mismo instrumento** (`organismo_v11g` `6c6b5eecc177c181`, `mundo_temporal_v11` `807f4b357f9eac1a`);
identidades 33/33.

#### Etapa 3 — generalización a patrones NUNCA VISTOS (regla `px0`)

| brazo | valor (acierto de signo) | conducta al primer encuentro | control azar (valor) |
|---|---|---|---|
| v9 | **0.800** | 0.801 | 0.500 |
| v10 | **0.800** | 0.760 | 0.500 |
| **v11** | **0.600** | 0.672 | 0.500 |

- **G1 REFUTADA** (0.600 < 0.65; `px0` > azar sólo en 12/20). **G3 (XOR) REFUTADA.** **G2 sostenida** (la conducta
  sigue por encima del azar). **G4, no-inferioridad frente a v9: REFUTADA** (valor 0.600 frente a 0.800; conducta
  0.672 frente a 0.801).
- **La pérdida es atribuible a UNA línea:** v10 (con `mu` normalizada, sin la regla de signo) conserva 0.800. Lo que
  cuesta generalización es **exactamente** la división por conflicto de signo con hija ciega.
- **Mi predicción preregistrada (0.72–0.88 y "sobrevive con ventaja") queda REFUTADA.** Escribí que un patrón nuevo
  caería en las celdas de los entrenados parecidos. Es falso, y el diagnóstico dice por qué.

#### Diagnóstico (post-hoc, exploratorio, 5 semillas; declarado como tal)

| | celdas hijas en el código de un patrón NUEVO (de 3) | celdas compartidas con el entrenamiento | \|W\| a priori | acierto |
|---|---|---|---|---|
| v9 | **1.00** | 2.90 | 1.96 | 0.76 |
| v11 | **0.07** | 2.44 | 1.52 | 0.50 |

**La explicación, y es el hallazgo de fondo:** en v9 las hijas **se metían en el código de casi todos los patrones**
(una de cada tres celdas de un patrón nunca visto era una hija ajena). Esa **fuga** era la que llevaba valor aprendido
a lo nuevo: **la generalización de v9 ERA la interferencia de v9**. v11 tapa la fuga —la hija nace ciega fuera de su
patrón— y con ella desaparecen **las dos cosas a la vez**: el olvido catastrófico **y** la generalización.
**No son dos propiedades: son la misma, vista desde los dos lados.**

#### 3T — composición temporal: **SOBREVIVE, y mejora**

| brazo | `sep` (C3) | `lift_q4` | `solap_A` | divisiones | control C3C |
|---|---|---|---|---|---|
| v9 | +3.91 | +0.382 | 1 | 16 | −0.35 |
| **v11** | **+3.96** | **+0.388** | **0** | **6** | −0.36 |

T1, T2, T3, T4 y T5 (no-inferioridad) **sostenidas**; KT2 20/20. v11 compone el paso de historia igual de bien con
**menos de la mitad de divisiones** y separa el canal temporal por completo.

#### Veredicto y lectura según el marco preregistrado

**`ETAPA3_SOBREVIVE = False`; `3T_SOBREVIVE = True`.** Por el preregistro: **v11 es un canje, no una mejora
universal**, y el resultado va **a favor de la predicción de McClelland, McNaughton y O'Reilly (1995)**: separar para
no interferir **cuesta** generalización. Sahay/Clelland describen mejoras de separación sin ese costo; **aquí el costo
existe y está medido**, con la ventaja de que podemos señalar la línea exacta que lo produce y el mecanismo (la fuga
de las hijas).

**v11 sigue siendo el tronco** (su congelación se decidió con otros criterios, ya cumplidos), **con esta advertencia
en grande**: v11 recuerda y tiene capacidad, pero **generaliza al nivel del azar** en valor sobre patrones nuevos.

**Lo que abre, y es lo interesante:** CLS propone exactamente la salida — **dos sistemas**, uno rápido y separado y
otro lento y entrelazado. Nuestro sistema lo plantea con una perilla: la ceguera de la hija es hoy **total**
(`kj * (P > 0)`). Una ceguera **graduada** debería recorrer el canje entre recordar y generalizar. Es el candidato
natural a v12 y se preregistrará como tal.

### Confirmación de "generalización = interferencia" en 20 semillas: **D1–D4 SOSTENIDAS**

Preregistro `experimentos/v11_generaliza/PREREGISTRO_fuga.md` (`b8932958e3480afa`), commiteado antes de correr
(`f630bf6`). Datos `datos/fuga_20260917_152707.json` (`e9278cce6320f9f5`). Regla `px0`, T = 200.000, semillas 41–60,
tres brazos con el mismo instrumento. Contaminación declarada en el preregistro: la hipótesis salió de las semillas
41–45; por eso D4 repite todo sólo con las 15 no miradas.

| brazo | fuga (hijas ajenas en el código de un patrón nuevo, de 3) | fuga en los entrenados | acierto | divisiones |
|---|---|---|---|---|
| v9 | **1.00** [0.97, 1.00] | 1.00 | 0.800 | 28 |
| v10 | 0.65 [0.20, 0.93] | 0.73 | 0.800 | 16 |
| **v11** | **0.08** [0.00, 0.33] | 0.40 | 0.600 | 28 |

- **D1 SOSTENIDA** (1.00 ≥ 0.8 y 0.08 ≤ 0.3).
- **D2 SOSTENIDA:** Spearman(fuga, acierto) = **+0.601** sobre las 60 corridas.
- **D3 SOSTENIDA, y era la que podía fallar:** dentro de v9, sin el brazo como confusor, **+0.328** (se pedía ≥ +0.30).
  Sin voto: v10 +0.466; v11 −0.104 (con la fuga en el suelo no hay varianza que correlacionar).
- **D4 SOSTENIDA** en las semillas limpias 46–60: fuga 1.00 y 0.10, Spearman +0.579.

**Por el preregistro, la frase entra al HANDOFF** (sección 11.3): *"la generalización de v9 era su interferencia"*.
Queda anotado lo que **no** prueba: la relación es correlacional dentro de una arquitectura; la prueba causal es
manipular la fuga y medir, que es exactamente lo que hará v12 con la ceguera graduada.

### ERR-20 — una etapa cerrada que no está en ninguna batería no está protegida

**Qué pasó.** La Etapa 3 (generalización) se cerró el 16 sep con v9 y **no quedó en ninguna batería**. El criterio v3
—el examen que decide si un tronco se congela— cubre aprender, revertir, interferencia, control negativo y las
identidades de la plasticidad, pero **no cubre generalización a patrones nunca vistos**. Resultado: **v11 pasó el examen
8/8, se congeló como tronco el 17 sep, y la Etapa 3 quedó reabierta sin que ninguna prueba lo dijera**. Nos enteramos
sólo porque la nota de dirección pidió re-verificarla a mano.

**Por qué importa más que un fallo de número.** Los otros 19 errores eran de medición o de criterio: se veían corriendo
algo. Éste es **de cobertura**: el sistema de protección tenía un agujero con forma de etapa entera. Un agente futuro
(o yo mismo) podía congelar v12, v13 y v14 sin volver a mirar la generalización nunca más.

**Familia:** la misma de ERR-11 y ERR-16 (un control que no puede fallar, un criterio que no mide lo que dice), pero a
nivel del **conjunto de pruebas**, no de una prueba.

**Corrección, hecha hoy.**
1. **`organismo/bateria_generaliza.py`** (`105ce314d643cd08`): regresión de generalización para cualquier tronco.
   Mide G1 (valor sobre patrones nunca vistos, regla `px0` contra control `azar`), G2 (conducta al primer encuentro) y
   la cobertura, con **los umbrales del preregistro de la Etapa 3, sin tocar ninguno**. Cada tronco necesita su
   instrumento de mundo de regla registrado en `INSTRUMENTOS` (mismas anclas para todos).
2. **Entra a la regla 1 y a la lista de congelación:** ningún tronco nuevo se congela sin correrla con 20 semillas, y
   el resultado se registra aunque falle.
3. **Comprobada sobre v11 en semillas nuevas (61–66):** `G1 FALLA` (0.550), `G2 PASA`, cobertura 6/6 →
   *"v11 NO CONSERVA la generalización de la Etapa 3"*. La batería hace visible, en dos minutos, lo que nos costó una
   re-verificación entera descubrir.

**Regla derivada, para el proyecto:** *cuando una etapa se declare cerrada, la prueba que la cerró entra a una batería
el mismo día, o la etapa no está cerrada.* Pendiente: revisar si las Etapas 1 y 2 tienen la misma deuda (la 2 sí está
en el criterio v3 vía E2/E2L; la 1 también vía E1).

### v12 — superficie del canje (seis β) y rama `hija-madura`: **H sostenida, rama REFUTADA**

Preregistro `experimentos/v12_ceguera_graduada/PREREGISTRO_v12.md` con **enmiendas 1 y 2 escritas antes de correr**
(`b89af5f`, `220aa55`). Datos `datos/v12_superficie_20260917_154123.json` (`9cc6c639405f7016`). Instrumentos
`organismo_v12` `7f564687ec072da6`, `v12m` `c04a7f32b6eaa539`, `v12g` `b68d918f0db3ca8c`.

**Controles de inercia (pedidos por dirección), verificados ANTES de mirar los puntos intermedios:** `v12(β=0)` ≡ v11
**21/21**, `v12(div_signo=False)` ≡ v10 **21/21**, `v12m` ≡ `v11m` 9/9, `v12g` ≡ `v11g` 6/6. (Enmienda 1: β=1 **no
puede** ser v10 —el disparo por signo, la madre fija y la fisión no se gradúan— y por eso el control correcto es
apagar la regla entera.)

**Guarda del instrumento: Spearman(β, fuga) = +1.000.** La perilla manipula exactamente lo que dice manipular.

| condición | semillas | retención | aprende C y D | acierto en nunca vistos | azar | conducta | fuga | divisiones | muertes |
|---|---|---|---|---|---|---|---|---|---|
| β = 0.00 (= v11) | 41–60 | **20/20** | 20/20 | 0.600 [0.40, 0.90] | 0.500 | 0.672 | 0.08 | 5 | 202 |
| β = 0.15 | 41–60 | **20/20** | 20/20 | 0.575 | 0.500 | 0.657 | 0.13 | 5 | 202 |
| β = 0.30 | 41–60 | **20/20** | 20/20 | 0.600 | 0.500 | 0.689 | 0.18 | 5 | 198 |
| β = 0.50 | 41–60 | 19/20 | 20/20 | 0.600 | 0.500 | 0.664 | 0.22 | 6 | 196 |
| β = 0.75 | 41–60 | 19/20 | 20/20 | 0.700 | 0.500 | 0.716 | 0.37 | 6 | 202 |
| β = 1.00 | 41–60 | 12/20 | 20/20 | 0.700 | 0.500 | 0.692 | 0.57 | 7 | 202 |
| rama u = 1.0 | 71–80 | 5/10 | 10/10 | 0.700 | 0.500 | 0.740 | 0.65 | 7 | 210 |
| rama u = 0.3 | 71–80 | 5/10 | **5/10** | 0.750 | 0.500 | 0.718 | 0.67 | 7 | 222 |

*(referencias: v9 = retención 0/20 y acierto 0.800; v11 = 20/20 y 0.600; azar 0.50)*

- **H [el canje existe]: SOSTENIDA.** Ningún β alcanza a la vez retención 20/20 y acierto ≥ 0.78. La superficie es
  monótona en fuga y **el precio aparece antes que el premio**: la retención empieza a caer en β = 0.50 y se hunde en
  β = 1.00 (12/20), mientras el acierto sólo llega a 0.700.
- **Hallazgo lateral que corrige una simplificación mía:** ni con fuga máxima dentro de la regla de v11 se recupera el
  0.800 de v9. **La ceguera explica parte del costo, no todo**: la fisión del valor y la madre fija también cuestan
  generalización. La fuga a β = 1 es 0.57, no 1.00, porque la regla de signo produce **menos hijas** (7 divisiones
  frente a 28 de v9 en el mismo mundo).
- **Rama `hija-madura`: REFUTADA en los dos umbrales.** Retención 5/10 (se pedía ≥ 8) con acierto 0.700 y 0.750.
  **Las semillas retenidas 81–90 no se tocaron**, por el propio criterio de la rama.
  **Diagnóstico, y es limpio:** con `u = 0.3` la congelación llega tan pronto que **rompe el aprendizaje de lo nuevo**
  (guarda 5/10: ya no aprende C y D); con `u = 1.0` sólo congela hijas de veneno (enmienda 2) y no alcanza a proteger
  A. Congelar lo justo para no olvidar es congelar demasiado para aprender: **la maduración no rompe el canje, lo
  reproduce a otra escala.**

**Lectura:** en esta arquitectura, **recordar y generalizar son el mismo parámetro visto por los dos lados**, y la
superficie lo muestra punto a punto. Es el resultado que pedía dirección: un mapa, no una solución. v11 sigue siendo
el tronco; **v12 no se congela** (ningún punto mejora los dos ejes a la vez).

**Lo que queda, con lo aprendido:** la salida ya no puede ser una perilla dentro de una sola vía. La propone la propia
literatura (McClelland y otros, 1995) y ahora también nuestros datos: **dos vías** —una rápida y separada que recuerde,
otra lenta y con fuga que generalice— y un modo de consultarlas. Es un cambio de arquitectura, no un parámetro.

### v13 — DOS VÍAS: **el canje se rompe** (P4 confirmado en semillas 61–80, P5 sostenida)

Preregistro `experimentos/v13_dos_vias/PREREGISTRO_v13.md` (`e9568fc0542d493e`) con **enmienda 1 escrita antes de
correr** (`57ec024`). Datos `datos/v13_dos_vias_20260917_160541.json` (`01d1cdf0d4c1dbe5`). Instrumentos por anclas:
`organismo_v13` `88c3574cf9cf38bf`, `v13m` `8b134cfd335e78e2`, `v13g` `2a80e125f8593bf2`. 2.100 corridas de superficie
+ 140 de confirmatorio.

**Mecanismo.** Vía rápida = v11 sin tocar. Vía lenta = lectura **lineal directa de la retina** (dos canales `Wps`/`Wns`
∈ ℝ⁶, tasa `eta_s`, mismo drenaje). Tres modos de combinarlas: `suma` (un solo error compartido, lo preregistrado),
`puerta2` y `puerta3` (cada vía aprende de **su propio** error; la boca consulta la rápida sólo si ≥ K de las 3 celdas
del código tienen valor consolidado —`|Wp−Wn| > 0.2`, el umbral que ya usa v11— y si no, la lenta).

**P1 inercia:** `v13(eta_s=0)` ≡ v11 21/21; `v13m` ≡ `v11m` 9/9; `v13g` ≡ `v11g` 6/6.

**Superficie completa (semillas 41–60; referencias: v11 = 20/20 y 0.600; v9 = 0/20 y 0.800; azar 0.50):**

| brazo | eta_s | retención | aprende C,D | acierto nunca vistos | xor | conducta | E1 / E2 / E2L |
|---|---|---|---|---|---|---|---|
| suma | 0 (=v11) | 20/20 | 20/20 | 0.600 | 0.500 | 0.672 | 20 / 20 / 20 |
| suma | 0.003 | 20/20 | 20/20 | 0.600 | 0.500 | 0.640 | 20 / 20 / 20 |
| suma | 0.006 | 20/20 | 20/20 | 0.600 | 0.500 | 0.698 | 20 / 20 / 20 |
| suma | 0.015 | 19/20 | 20/20 | 0.600 | 0.500 | 0.719 | 20 / 18 / 20 |
| suma | 0.03 | **0/20** | 20/20 | 0.700 | 0.500 | 0.849 | 20 / 16 / 19 |
| puerta2 | 0 | 20/20 | 20/20 | 0.600 | 0.500 | 0.682 | 20 / 20 / 20 |
| puerta2 | 0.003 | 20/20 | 20/20 | 0.600 | 0.438 | 0.690 | 20 / 20 / 20 |
| puerta2 | 0.006 | 20/20 | 20/20 | 0.650 | 0.438 | 0.728 | 20 / 20 / 20 |
| puerta2 | 0.015 | 20/20 | 20/20 | 0.600 | 0.500 | 0.730 | 20 / 20 / 20 |
| puerta2 | 0.03 | 19/20 | 14/20 | 0.600 | 0.500 | 0.712 | 20 / 20 / 20 |
| puerta3 | 0 | 20/20 | 17/20 | 0.550 | 0.500 | 0.573 | 20 / 20 / 20 |
| puerta3 | 0.003 | 20/20 | 15/20 | 0.750 | 0.438 | 0.697 | 20 / 20 / 20 |
| puerta3 | 0.006 | 20/20 | 15/20 | 0.750 | 0.375 | 0.760 | 20 / 20 / 20 |
| **puerta3** | **0.015** | **20/20** | 19/20 | **0.800** | 0.406 | 0.798 | 20 / 20 / 20 |
| puerta3 | 0.03 | 20/20 | 11/20 | 0.800 | 0.406 | 0.883 | 20 / 20 / 20 |

- **El brazo `suma` (un error compartido) NO rompe el canje**, como anticipó el humo: la rápida deja sin error a la
  lenta; y con `eta_s = 0.03` la lenta se lleva tanto valor que **se pierde la retención por completo** (0/20). La
  predicción P2 original falla por esa razón, declarada antes de correr.
- **El brazo `puerta3` sí lo rompe.** Dos puntos cumplen en 41–60 (`eta_s` 0.015 y 0.03); por la regla escrita se lleva
  **uno solo** (0.015: mejor guarda) al confirmatorio.

**CONFIRMATORIO en semillas 61–80 (nunca usadas; el único que decide):**

| condición | retención | guarda | W_B | acierto nunca vistos | xor | conducta | fuga | E1 / E2 / E2L | muerde B al volver |
|---|---|---|---|---|---|---|---|---|---|
| **puerta3, eta_s = 0.015** | **20/20** | 19/20 | −3.05 | **0.850** [0.60, 1.00] | 0.438 | **0.852** | 0.03 | **20 / 20 / 20** | 0 |

**P4 [el canje se rompe]: CONFIRMADO. P5 [nada se rompe]: SOSTENIDA. XOR ≤ 0.60: sí (0.438).**

**Lectura.** Por primera vez el organismo **recuerda como v11 (20/20) y generaliza mejor que v9 (0.85 frente a 0.80)**,
sin romper aprender, revertir ni separar. El mecanismo es el que propone la teoría de sistemas complementarios y el que
nuestros propios datos pedían: **dos vías**, una que separa (y recuerda) y otra que solapa (y generaliza), con **una
puerta de familiaridad** que decide a cuál se le cree. Cuando la rápida "reconoce" el patrón (tres celdas consolidadas)
manda ella; cuando no, manda la lenta, que ha aprendido la **regla** y no los casos.

**Cautelas, escritas con el resultado caliente:**
1. La vía lenta es **lineal**: generaliza lo lineal (`px0`) y **no** XOR (0.44, como se predijo). No es "la corteza";
   es la vía lenta mínima.
2. El punto se **eligió** entre 15 en 41–60 y se **confirmó** en 61–80: es un confirmatorio limpio, pero de **un** punto.
3. Falta el confirmatorio completo de tronco: examen criterio v3 en 20 semillas nuevas, `bateria_generaliza.py 20`
   (ERR-20) y la re-verificación 3T. **v13 es candidato, no tronco.**
4. La guarda queda en 19/20 (una semilla no aprende del todo lo nuevo): por debajo del 20/20 de v11. Se vigila.

### Confirmatorio de congelación de v13: **X2 y X3 pasan; X1 falla en el control negativo → v13 NO se congela (por la letra)**

Preregistro `experimentos/v13_dos_vias/PREREGISTRO_tronco_v13.md` (`ee204f281d04a329`, `9195f18`), instrumentos
`organismo/organismo_v13.py` (`cc8b16b492d4d324`: el genoma explorado con `eta_s = 0.015`, `puerta = 3`) y
`organismo/bateria_v13.py` (`38f07f95f76c31ae`), commiteados antes de correr (`7415536`). Datos
`examen_v13_20260917_164031` (`f4fea3e841facfc8`), `regresion_generaliza_organismo_v13_20260917_164314`
(`4bd6ce4221db5c8d`). Semillas **81–100**, nunca usadas.

| bloque | resultado |
|---|---|
| Q0 identidades | `v13(eta_s=0, puerta=None)` ≡ v11 **42/42**; con `div_signo=False` ≡ v10 **42/42**; tronco ≡ genoma explorado 9/9 |
| X1 examen criterio v3 | **7/8**: E1, E2, E2I, E2J, E2K, E2L **20/20**; celdas ≤ 45; 4a', 4b, 4c, 4d pasan. **Criterio 3 (control negativo) FALLA: 20/20 lo pasan** (`W_A` 0.99–1.00) |
| **X2** `bateria_generaliza.py 20 --desde 81` | **G1 PASA 0.900** (azar 0.500, px0 > azar 20/20); **G2 PASA 0.916**; cobertura 20/20 → *"v13 CONSERVA la generalización de la Etapa 3"* |
| X3 regresión | `bateria_v11.py 6` y `bateria_v9.py 6` cumplen; 12 congelados intactos |

**Diagnóstico del control 3.** El control negativo dice: *con A∩B = 3 y sin plasticidad, el organismo no debe separar
A de B* (así se demuestra que la separación de E2L la causa la división de celdas). Vale para v6–v11, que **sólo**
leen el mundo a través de las celdas Kenyon: si A y B comparten las tres, son indistinguibles. **v13 tiene otra vía:**
la lectura lineal de la retina, y A = `110100` y B = `101010` **difieren en cuatro píxeles**. Sin plasticidad, la vía
rápida sigue sin poder separarlos, pero la lenta los separa sola, y la boca —al no reconocerlos como familiares en la
rápida— consulta a la lenta. **El control no fue burlado; su premisa ("no hay otra vía") dejó de ser cierta.**

**Decisión, por la letra del preregistro (regla 3): v13 NO se congela hoy. v11 sigue de tronco.** Nada se recalibra.

### ERR-21 — un control negativo con la premisa de una sola vía

**Qué pasó.** El criterio 3 del examen v3 asume que separar A∩B=3 exige plasticidad estructural porque la única lectura
del mundo son las celdas Kenyon. Un organismo con **dos vías** puede separar por la otra. El criterio, tal como está
escrito, **no puede fallar honestamente ni pasar honestamente** para v13: no distingue "burló el control" de "tiene
otra vía". Es la familia de ERR-16 y ERR-20 (controles y coberturas cuya premisa no se revisó al cambiar la
arquitectura), y **no se anticipó** al preregistrar (a diferencia de 4a', que sí se corrigió antes de correr).

**Qué NO se hace:** no se quita el criterio 3 ni se relaja para que v13 pase.

**Qué se propone, y se corre AHORA como diagnóstico (no decide nada):**
- **3' [la vía rápida sigue necesitando plasticidad]:** `v13(plast=False, solap_AB=3, eta_s=0)` —la vía rápida sola—
  debe **fallar** E2L en ≥ 19/20, exactamente como v11. Es el control 3 heredado, aplicado a la vía que lo motivó.
- **3'' [la vía lenta separa por píxeles, y eso es lo que se espera de ella]:** `v13(plast=False, solap_AB=3)` con la
  lenta activa **pasa** E2L en ≥ 19/20. Ya medido: 20/20. Deja de ser un "fallo" y pasa a ser una **propiedad medida**.
- **Decisión sobre la congelación: la toma dirección**, porque cambiar un criterio de congelación después de ver el
  resultado es exactamente lo que la regla 3 vigila, aunque aquí la razón sea estructural y esté a la vista. Se le
  presenta con 3' medido.

**Diagnóstico 3' / 3'' medido (semillas 81–100, `datos/control3_v13_20260917_164836.json`):**
- **3' [vía rápida sola, sin plasticidad]: pasan E2L 0/20** (`W_A` −1.12, `W_B` −1.12: indistinguibles, como en v11).
  **SOSTENIDA.** La vía rápida sigue necesitando la división para separar; el control heredado se cumple.
- **3'' [vía lenta activa, sin plasticidad]: pasan 20/20** (`lenta_A` +1.00, `lenta_B` −2.97). **SOSTENIDA.** La lenta
  separa por píxeles, que es exactamente lo que se le pide.

**Lectura:** el criterio 3 original mezclaba dos preguntas que en v13 tienen respuestas distintas. Separadas, las dos
salen como deben. **La congelación queda en manos de dirección**: aceptar 3'+3'' como criterio 3 del examen **v3'**
(y con ello v13 pasa 8/8 con todo lo demás ya medido en 81–100), o mantener la letra y dejar v13 como candidato.


### v13 CONGELADO COMO TRONCO — confirmatorio en semillas NUEVAS 101–120 con el criterio v3' fijado antes

Enmienda 1 del preregistro de congelación (`6fc9873`), escrita **antes** de correr: criterio **v3'** (control 3
desdoblado, ERR-21) y examen completo en 101–120. `bateria_v13.py` pasa a `1a027bcb37eb536e`. Datos
`examen_v13_20260917_165859` (`4c12053554354f80`) y `regresion_generaliza_organismo_v13_20260917_170148`
(`9483fb6f50af24c7`).

| bloque (semillas 101–120) | resultado |
|---|---|
| identidades | 42/42 y 42/42 |
| seis etapas | **20/20 las seis** |
| 3' vía rápida sola sin plasticidad | **0/20** pasan (≤ 1) ✅ |
| 3'' vía lenta sin plasticidad | **20/20** pasan (≥ 19) ✅ |
| 2, 4a', 4b, 4c, 4d | ✅ |
| **X2 generalización** | G1 **0.800** (azar 0.500, px0 > azar 18/20) ✅; G2 **0.892** ✅ |
| X3 regresión | v11 y v9 cumplen; 12 congelados intactos |

**Nota honesta sobre la predicción:** G1 dio 0.800, **por debajo** de lo que predije (0.85–0.90) y por debajo del 0.900
de 81–100. Pasa el criterio (≥ 0.65) con margen, y es igual al v9 histórico; la variación entre lotes de semillas
(0.85, 0.90, 0.80) es la que hay. Se anota para no vender 0.90 como el número.

**Por el preregistro: v13 SE CONGELA COMO TRONCO** (tag `v13-tronco`; CONGELADOS pasa a 14). **Etapa 3 y Etapa 4
quedan cerradas a la vez sobre el mismo organismo.** v11 pasa a tronco anterior.

**Pendientes declarados, obligatorios antes de decir "todo sobrevive":** 3T (composición temporal) y capacidad sobre v13.


### Re-verificación sobre v13: **3T sobrevive (T1–T6); la capacidad cae, como se predijo; KT2 no aplica (ERR-22)**

Preregistro `experimentos/v13_reverificacion/PREREGISTRO_reverificacion_v13.md` (`e874add677bbb67b`, `01c47dc`);
instrumentos `mundo_temporal_v13` (`f9c3169b32f393d4`; el `bd3c64c0799ed8ce` que decía aquí era el sha anterior al renombre `valor_tot`, corregido el 17-sep noche) y `organismo_capD13` (`c93ba572bc783a05`), commiteados antes.
Datos `datos/reverificacion_v13_20260917_171603.json` (`9c9f52afffa36c79`). Inercia: 18/18 y 4/4. Semillas 41–60.
(Un primer lanzamiento se cayó en la etapa de inercia por un choque de nombres del instrumento —mi `valor(P)` pisó la
`valor(kk, last)` del mundo temporal—; se renombró y se relanzó sin medir nada en medio.)

#### 3T — composición temporal

| brazo | C3 `sep` | C3 `lift_q4` | C3 `solap_A` | divisiones | C3C (control) | C2b | C1p |
|---|---|---|---|---|---|---|---|
| v11 | +3.96 | +0.388 | 0 | 6 | −0.36 | +0.00 | +0.00 |
| **v13** | **+3.96** [+1.89, +3.98] | **+0.376** | 0 | 6 | −0.04 | +0.00 | +0.00 |

**T1, T2, T3, T4, T5 (no-inferioridad) y T6 SOSTENIDAS.** T6 era el control nuevo para v13: con las columnas temporales
a cero (C2b) o sin canal temporal (C1p), la vía lenta **no** resuelve 3T por otra puerta (`sep` 0.00 en ambos). La
composición temporal vive en la vía rápida, que v13 no toca. Cautela: el rango de v13 en C3 baja a +1.89 en la peor
semilla (v11: +3.88); mediana igual.

**KT2 falla: C2b ≡ C1 bajo v13 en 0/20.** KT2 era el control **de instrumento** que garantizaba que "columnas
temporales a cero = entrada temporal invisible". En v13 la vía lenta lee la entrada **directamente**, así que la
entrada temporal existe para ella aunque las columnas de Kenyon estén a cero; C2b (12 entradas) y C1 (6) dejan de ser
el mismo organismo (muertes 121 frente a 104, `lift` −0.163 frente a −0.030), **aunque ninguno resuelva 3T** (T6). Por la
letra del preregistro, `3T_SOBREVIVE = False` porque incluía KT2. **Lectura honesta:** los seis criterios científicos
pasan y el que falla es una identidad cuya premisa (una sola vía) v13 rompe por construcción.

### ERR-22 — la identidad C2b ≡ C1 tiene la premisa de una sola vía (misma familia que ERR-21)

Igual que el control negativo del examen: un control escrito para un organismo que sólo ve el mundo por Kenyon. Para
un organismo de dos vías, la garantía que daba KT2 ("la lenta no ve el canal temporal") **es falsa y debe serlo**; lo que
hay que garantizar es que **no lo usa para resolver la tarea**, y eso es T6, que se preregistró y pasa. No se anticipó
al escribir el preregistro (se anticipó T6, no la caída de KT2). **Regla derivada, ya la segunda vez:** *al cambiar la
arquitectura, revisar TODAS las identidades de instrumento, no sólo los criterios científicos.* Pendiente: KT2' para
organismos de dos vías = C2b(`eta_s=0`) ≡ C1(`eta_s=0`) (la vía rápida sola), más T6.

**Veredicto de 3T sobre v13, con la salvedad escrita: SOBREVIVE (T1–T6); KT2 no aplicable (ERR-22).**

#### Capacidad — mundo grande (10 px, 60 estímulos)

| paso | brazo | N\* | M_max | agotan el pool | no familiares al final |
|---|---|---|---|---|---|
| 20k | v11 | 43.5 [6, 60] | 28.5 | 20/20 | 16/60 |
| 20k | **v13** | **28.0** [3, 45] | **25.0** | 20/20 | 16/60 |
| 60k | v11 | 50.0 [31, 60] | 32.0 | 20/20 | 14/60 |
| 60k | **v13** | **35.0** [9, 46] | **29.5** | 20/20 | 11/60 |

**K1 sostenida; K2 y K3 (no-inferioridad) REFUTADAS**, exactamente en la dirección y magnitud predichas (se predijo
`N*` 25–40): en un mundo abarrotado, los estímulos cuyo código no tiene las 3 celdas consolidadas (11–16 de 60 al
final) van a la vía lenta, que es lineal y **no puede** ajustar 60 valencias alternadas. **Es el precio de la puerta en
mundos abarrotados.** v13 sigue **muy por encima** de v10 (6 y 9) y conserva la degradación suave, pero **pierde ~15
estímulos** frente a v11. Se registra como **canje nuevo: puerta contra capacidad**.

**Salida anotada para preregistrar después (NO se recalibra aquí):** que la puerta consulte la lenta sólo cuando la
rápida esté **vacía** (0 celdas consolidadas), y no cuando esté a medias; o una puerta graduada por número de celdas.
Riesgo conocido: `puerta = 2` costó generalización (0.60–0.65) en la superficie de v13.

**Estado del tronco v13, completo y honesto:** aprende, revierte, recuerda (20/20), generaliza (0.80–0.85), compone un
paso de historia (3T 3.96) y sostiene 28–35 estímulos de 60 (v11: 43–50; v10: 6–9). Su costo conocido es la
capacidad en mundos abarrotados, y su límite conocido es que la vía lenta es lineal.


## ETAPA 5 — N1-ASIMÉTRICO sobre v13: **transmisión por conducta visible y simbiosis en el tiempo, DEMOSTRADAS (semillas 1–20)**

Preregistro `experimentos/etapa5_comunicacion/PREREGISTRO_N1_asimetrico.md` (`df387ef8ca41d3f9`; enmienda 1 escrita
antes de correr: base v13, vicario en las dos vías). `mundo_social.py` (`562293565b239821`) replica v13 línea a línea;
**K1**: con un organismo ≡ `organismo_v13` 6/6 (y con las perillas apagadas ≡ v11 y ≡ v9, en el humo). Datos
`datos/N1asim_20260917_175433.json` (`84469d93cf1891b0`). Semillas 1–20, T = 100.000, experto = progenitor v13 que vivió
E1 100.000 pasos (`W_A` +1.00, `W_B` −2.98) y hereda todo su estado; novato = nace en blanco.

**Instrumento:** K2, el novato recibe avisos "−" sobre B **antes** de su propio criterio: mediana 38, ≥ 5 en 20/20 (el
canal llega a tiempo). K3, la señal barajada llega en la misma cantidad (5057 frente a 5168).

**Mundo estable (E1): el experto enseña**

| condición | veneno propio hasta el criterio (novato) | veneno Q1 | muertes | W_B final | experto |
|---|---|---|---|---|---|
| NOV-SOLO | 19 | 29.5 | 137 | −2.98 | — |
| PAR-N0 (dos, sin señal) | 19 | 40 | 181.5 | −3.00 | −3.00 |
| **PAR-N1 (señal de conducta)** | **7** | **21** | 181 | −3.00 | −3.00 (20/20 intacto) |
| PAR-BAR (barajada) | **704.5** | 178.5 | 255.5 | −1.75 | −1.65 |

- **A1 SOSTENIDA:** 7 ≤ 0.7 × 19 = 13.3. **El novato aprende que B es veneno con un tercio de las mordidas**, mirando
  cómo el experto lo rechaza. **A2 SOSTENIDA: 20/20 pareado.**
- **A3 SOSTENIDA, y de forma brutal:** la señal barajada no es neutra, es **destructiva** (704 mordidas de veneno, 255
  muertes, `W_B` −1.75): la mitad de los avisos al azar dicen "+" sobre B y el novato lo come. **El contenido lo es
  todo**; "cualquier señal acelera" queda refutado en su forma más fuerte.
- **A3b:** el experto no se degrada: `W_B` −3.00 en 20/20.

**Mundo invertido (INV): el experto está equivocado y el novato lo corrige**

| condición | novato `t_B_ok` (descubre que B es comida) | veneno Q1 (A) | experto `t_ext_B` (extingue su miedo a B) | mordidas de B del experto |
|---|---|---|---|---|
| PAR-N0 | 93 | 31 | **70.142** | 94 |
| **PAR-N1** | 168 | 19 | **21.902** | 182 |
| PAR-BAR | 104 | 168 | 9.657 | 788 |

- **A4 SOSTENIDA (18/20):** el novato que escucha a un experto equivocado tarda **más** en descubrir que B es comida
  (168 frente a 93 pasos): **el coste de la confianza**, pequeño y medido.
- **A5 SOSTENIDA (19/20):** el experto que ve al novato morder B **extingue su miedo tres veces antes** (21.902 frente
  a 70.142): **el que descubre corrige al que sabe.** (BAR extingue aún antes, 9.657, pero por la razón equivocada: los
  "+" al azar le hacen morder B 788 veces; su `W_B` final queda en +0.88 y muere 292 veces.)

**Veredicto: `TRANSMISION = True`, `SIMBIOSIS = True`.** Vocabulario permitido: *el novato **aprende** del rechazo
visible del experto; el experto **revierte** antes gracias al novato.* Nada de "lenguaje": la señal es un reflejo de
la conducta, honesta por construcción, y el receptor la trata como una experiencia propia atenuada.

**Antes de escribir "Etapa 5 cerrada": réplica en semillas nuevas 21–40** con los mismos criterios (se corre a
continuación; preregistrada por este mismo párrafo antes de correr, predicción: los seis criterios se sostienen).


### Réplica de N1-asimétrico en semillas NUEVAS 21–40: **los seis criterios se sostienen. ETAPA 5 (transmisión N1) CERRADA**

Datos `datos/N1asim_s21-40_20260917_175924.json` (`c7be2a06df98f52f`). K1 6/6; K2 mediana 35 (20/20); K3 OK.

| criterio | semillas 1–20 | **semillas 21–40** |
|---|---|---|
| A1 veneno propio hasta el criterio, N1 frente a N0 | 7 frente a 19 | **8 frente a 19** |
| A2 pareado N1 < N0 | 20/20 | **20/20** |
| A3 la barajada no ayuda (es destructiva) | 704 | **715** |
| A3b el experto no se degrada | 20/20 | **20/20** |
| A4 coste de la confianza (novato N1 tarda más en INV) | 18/20 | **19/20** |
| A5 simbiosis inversa (experto N1 extingue antes: 21.124 frente a 65.936) | 19/20 | **20/20** |

**Etapa 5, peldaño N1 (transmisión por conducta visible, con asimetría de información): CERRADA sobre v13.**
Vocabulario: *el novato aprende del rechazo visible del experto; el experto revierte antes gracias al novato.*
Por ERR-20, la prueba entra a la regresión el mismo día: `corre_N1_asim.py --n 6 --desde 41` es la batería rápida de la
Etapa 5 (K1 + A1–A5 en 6 semillas), y `--desde 21` (20 semillas) la completa. Queda escrito en `CLAUDE.md`.

**Peldaños abiertos de la Etapa 5:** N2 (que el **significado** de la señal emerja, juego de señalización) y N3 (dos
cuerpos con sentidos distintos resuelven lo que ninguno puede solo). Diseño en
`experimentos/etapa5_comunicacion/DISENO_comunicacion_simbiotica.md`.


## ETAPA 5, N2 (significado emergente) — **REFUTADO en el primer intento**, con diagnóstico limpio

Preregistro `experimentos/etapa5_comunicacion/PREREGISTRO_N2.md` (`8286eb96e843a84d`; enmienda 1 —el significado es
contraste— escrita tras el humo y antes de correr, `29ef4e5`). Datos `datos/N2_s1-20_20260917_181950.json`
(`b201d7424b4855f5`). K1: `mundo_social(n=1, regla)` ≡ `organismo_v13g` (tronco, `fase2_en=0`) 3/3. Progenitores
expertos: conocen 8 de 10 venenos (mediana). K2: 10.597 símbolos recibidos por el novato.

| condición | veneno del novato (200k) | veneno Q1 | muertes | venenos conocidos /10 | comidas conocidas /10 | decodificados |
|---|---|---|---|---|---|---|
| SOLO | 319 | 128 | 266 | 8 | 9 | — |
| N0 (dos, sin señal) | 318 | 140 | 440 | 8 | 6 | — |
| INNATO (conducta, = N1) | **194** | 93 | 361 | **10** | **0** | — |
| CONV (símbolos aprendidos) | **375** [235, 1805] | 190 | 429 | 9 | 7 | 149 |
| SHUF (barajados) | 328 | 147 | 434 | 9 | 6 | 32 |

| criterio | veredicto | cifra |
|---|---|---|
| E1 convención en el emisor | **REFUTADA** | 1/20; consistencia Q4 mediana **0.50** (azar); estados con símbolos distintos 6/20 |
| E2 decodificación en el receptor | **REFUTADA** | 1/20; contraste mediana **+0.00 / +0.03** (M crudo −2.69 / −2.63: los dos símbolos predicen el promedio) |
| E3 arbitrariedad | **REFUTADA** | "rechazo" = símbolo 0 en 19/20: no es convención, es el desempate del argmax con `Pq` empatado |
| E4 beneficio | **REFUTADA** | CONV 375 frente a N0 318; CONV mejor en sólo 3/20. **Peor con símbolos que sin ellos** |
| E5 barajar destruye | sostenida, **vacía** | no había código que destruir |

**Diagnóstico (desde los números; no se recalibra nada):**
1. **El emisor no recibe gradiente.** Refuerzos +37.088 / −692: el "acuerdo" del receptor es casi siempre positivo y,
   sobre todo, **ciego al símbolo**: como la conducta del receptor no depende del símbolo, los dos símbolos de un mismo
   estado reciben la misma corriente de refuerzo y saturan juntos (`|Pq|` mediana 3.00, empatados). Sin diferencia
   entre símbolos no hay convención.
2. **El receptor no actúa hasta tener significado, y no hay significado hasta que actúe.** `M` aprende el promedio de
   consecuencias por símbolo; con emisiones al azar los dos promedios son iguales (−2.7), el contraste es 0 y la puerta
   (`|C| ≥ 0.5`) casi nunca abre (149 decodificaciones en 200.000 pasos). Es el círculo que el preregistro declaró como
   riesgo principal. En los juegos de señalización de Lewis/Skyrms el círculo se rompe porque el receptor **sólo** tiene
   la señal para decidir; aquí el receptor ve el objeto y aprende su valor por su cuenta, así que el símbolo es
   redundante hasta que ya no hace falta.
3. **Por qué CONV es PEOR que N0:** las pocas veces que la puerta abre lo hace por ruido de muestreo (un símbolo que
   por azar precedió a más venenos), con el signo que toque; en una semilla el novato terminó con 1.805 mordidas de
   veneno. Un código a medio formar **hace daño**: es información con el signo al azar.

**Observación lateral, importante para N1 (sin voto):** INNATO reduce el veneno un 39 % pero el novato termina con
**0 de 10 comidas conocidas** (frente a 9/10 solo). La señal de conducta "−" (rechazo) también se emite cuando el experto
rechaza **comida por saciedad**, y el novato la devalúa. En el mundo A/B no se notó; con 20 patrones sí. **La conducta
visible no es una señal pura de valor: mezcla valor y hambre.** Queda anotado para el diseño de N2b y para el registro
de N1 (no cambia su veredicto: allí se midió veneno y retención, y ambos pasaron).

**Decisión:** N2 tal como se diseñó **no emerge**. Se registra como refutación de esta forma de refuerzo ("por
acuerdo") con este receptor ("actúa sólo cuando ya sabe"). Siguiente intento, preregistrado aparte (`PREREGISTRO_N2b.md`):
(a) el símbolo entra en la **decisión** del receptor desde el primer día, como un sesgo proporcional al contraste
(sin puerta), para que la conducta dependa del símbolo aunque sea poco; (b) el emisor se refuerza por la **ventaja**
sobre su promedio por estado (refuerzo menos línea base), para que la corriente ciega al símbolo se cancele y sólo
mueva `Pq` la parte que depende del símbolo. Si tampoco emerge, la conclusión honesta es que **con percepción directa
el código no paga lo bastante**, y el mundo que lo haría pagar es el de la Etapa 6 (novatos sucesivos, transmisión en
cadena).


### N2b — el bucle cierra a medias: **convención sí (14/20, arbitraria), significado débil (contraste ±0.4), beneficio −23 %**

Preregistro `PREREGISTRO_N2b.md` (`3f73782a5d4c2812`, commit `77f5b3e`, escrito antes de correr). Datos
`datos/N2b_s1-20_20260917_183004.json` (`7096226a18e31584`). K1 3/3 (con las perillas de N2b encendidas y sin señal, el
organismo sigue siendo v13). K2: 10.823 símbolos.

| condición | veneno del novato | veneno Q1 | muertes | venenos conocidos /10 | comidas /10 |
|---|---|---|---|---|---|
| SOLO | 319 | 128 | 266 | 8 | 9 |
| N0 | 318 | 140 | 440 | 8 | 6 |
| INNATO | 194 | 93 | 361 | 10 | 0 |
| **CONV** | **246** [162, 1171] | 125 | 434 | 8 | 7 |
| SHUF | **334** | 151 | 446 | 8 | 6 |

| criterio | N2 | **N2b** | umbral |
|---|---|---|---|
| E1 convención en el emisor | 1/20 | **13/20** (consistencia Q4 0.99; símbolos distintos 14/20) | ≥ 15 → **refutada por 2** |
| E2 decodificación (contraste) | 0.00 | **−0.42 / +0.36**, signo correcto; 2/20 | ≥ 15 con \|C\| ≥ 1 → **refutada** |
| E3 arbitrariedad | desempate | **10/20** | 5–15 → **sostenida** |
| E4 beneficio | 375 (peor) | **246 = 0.77 × N0**; pareado 12/20 | ≤ 0.70 y ≥ 14 → **refutada por poco** |
| E5 barajar destruye | vacío | **real**: SHUF 334 frente a CONV 246; \|C\| < 1 en 20/20 | **sostenida** |

Refuerzos del experto +37.916 / −444 pero `|Pq|` mediana **0.79** (no 3.00): la línea base cancela la corriente ciega y
sólo queda la parte que depende del símbolo. Decodificaciones por la vía de valor: **0** (la puerta 1.0 nunca abrió):
**todo el beneficio vino del sesgo del símbolo en la decisión** (`gamma · C ≈ ±0.5` sobre `Vb`).

**Lectura.** Las dos correcciones de N2b hicieron exactamente lo que se predijo: hay gradiente y el código se forma.
Lo que falta es **magnitud** en el receptor, y los datos señalan dos contaminaciones de `M`: (a) el estado del emisor
es su **conducta**, y rechaza comida **por saciedad** → el símbolo de rechazo precede a comida a veces; (b) el experto
**no conoce 2 de 10 venenos** y los muerde emitiendo "muerde" → el símbolo de mordida precede a veneno. **Es un fallo de
pureza de la señal, no del bucle.** Por la letra del preregistro: **refutado**; el siguiente diseño (N2c: el estado del
emisor es su valor y calla cuando no sabe; experto con 400k) va preregistrado aparte y se corre en la misma sesión
(regla 12).


### N2c — la pureza de la señal NO era el cuello: **refutado, y el eslabón real queda a la vista**

Preregistro `PREREGISTRO_N2c.md` (commit `77f5b3e`+), datos `datos/N2c_s1-20_20260917_183901.json` (`c6a276d0a7bbe258`).
K1 3/3 (perillas de N2c encendidas y sin señal: sigue siendo v13). Experto con 400k: conoce **7–8 de 10** venenos
(criterio estricto), igual que a 200k.

| criterio | N2b | **N2c** |
|---|---|---|
| E1 convención | 13/20 | **11/20** (consistencia 0.99; distintos 13/20) |
| E2 contraste | −0.42 / +0.36 | **−0.35 / +0.20** (M crudo −2.70 / −1.85); 3/20 |
| E3 arbitrariedad | 10/20 ✅ | **13/20 ✅** |
| E4 veneno CONV / N0 | 0.77 | **0.92** (290 / 316) |
| E5 barajar destruye | ✅ | ✅ (342 frente a 290) |

**Mi predicción (que la pureza de la señal subiría la magnitud) queda REFUTADA.** Cláusula cumplida: el cuello está en
el receptor. Y los números dicen cuál: aun con convención limpia en 13/20 semillas, **`M["positivo"]` = −1.85**: el
símbolo positivo precede a mordidas de veneno. Fuente: los 2–3 venenos que el experto **no tiene consolidados en su vía
rápida** los lee por la **vía lenta lineal**, que en el mundo `azar` devuelve valores arbitrarios; cuando el valor sale
≥ +0.5 el experto dice "positivo" sobre un veneno **con confianza**, el novato (sesgado por el símbolo) lo muerde más, y
el símbolo se envenena. **El canje puerta/capacidad de v13 reaparece como extrapolación confiada del emisor.** Es el
mismo fenómeno de la re-verificación (35 de 60) visto desde la comunicación.

**Decisión (regla 12):** N2d, preregistrado aparte: el emisor **habla sólo de lo que su vía rápida conoce por
experiencia** (la misma prueba de familiaridad de la puerta, sin constante nueva) y calla de lo que sólo extrapola.
Mismos umbrales. Si tampoco emerge en magnitud, **se cierra la línea N2 por hoy** con "emerge en signo, no en magnitud" y
se sigue el plan del debate de niveles 5–10.

### N2d — habla sólo de lo consolidado: **refutado en magnitud**, y un diagnóstico instrumentado encuentra la causa en el MUNDO

Datos `datos/N2d_s1-20_20260917_184830.json` (`3ebd203bf1594284`). E1 13/20 (consistencia 0.99), E2 **1/20** (contraste
−0.34 / +0.27), E3 12/20 ✅, **E4 pareado 15/20** (CONV 249 frente a N0 316; mediana 0.79 × N0, se pedía 0.70), E5 ✅.
Mi hipótesis (extrapolación confiada del experto) queda **refutada**: hablar sólo de lo consolidado no subió la magnitud.

**Diagnóstico instrumentado (semilla 4, `scratchpad/diag_n2d.py`, contadores sin tocar el mecanismo):** el experto
emite **36.365** símbolos en estado "negativo" y **564** en "positivo"; el novato oye "negativo" sobre veneno 10.092 veces
y "positivo" sobre comida **88**; y sólo muerde después de un "positivo" **8 veces** en 200.000 pasos (6 de ellas veneno,
por sus propios errores). Con 8 muestras `M[positivo]` no converge. **Causa: el muestreo del mundo.** La comida se come y
desaparece (una visita, una emisión); el veneno se rechaza y se queda, y se vuelve a pisar miles de veces. La
convención es perfecta (1.00) y el receptor no tiene con qué aprenderla por consecuencias. Ninguno de los cuatro
intentos podía verlo sin instrumentar.

**Decisión (regla 12):** se **anula** la cláusula de cierre de N2d (escrita sin conocer esta causa) y se preregistra N2e:
el significado también se aprende **por alineación con lo que el receptor ya conoce** (al oír `s` sobre un patrón
familiar a su vía rápida, `M[s]` se acerca al valor propio de ese patrón). Miles de oídas en vez de 8 mordidas. Si N2e
no sube E2, la línea se cierra con "emerge en signo, no en magnitud, por asimetría del muestreo del mundo".


### N2e — alineación con lo conocido: **también cae. LÍNEA N2 CERRADA POR HOY: emerge en signo, no en magnitud**

Preregistro `PREREGISTRO_N2e.md`; datos `datos/N2e_s1-20_20260917_185950.json` (`c03f3603c83eaeea`). E1 **7/20**
(consistencia 0.97; distintos 13/20), E2 2/20 (contraste **−0.11 / +0.05**; M crudo −3.15 / −2.96), E3 7/20 ✅, E4 CONV
320 ≈ N0 316 (pareado 13/20), E5 ✅. Alineaciones: miles; no sirvieron.

**Por qué (humo instrumentado de la semilla 4 y los cinco intentos juntos):** la alineación multiplica las muestras,
pero cada "positivo" equivocado sobre un veneno se alinea a **−3** y cada acierto sobre comida a **+1**; con una
convención imperfecta (0.70–0.97) bastan pocos errores para hundir `M[positivo]`. Es la misma asimetría de N2d:
**recompensa asimétrica (−3 / +1) y muestreo asimétrico del mundo (la comida desaparece al comerla; el veneno se queda
y se vuelve a señalar 36.000 veces)**. Con eso, ningún receptor razonable acumula significado positivo.

**Balance de la línea N2 (cinco diseños preregistrados, 500 corridas):**

| diseño | convención (E1) | arbitrariedad (E3) | contraste (E2) | beneficio (E4) | barajar destruye (E5) |
|---|---|---|---|---|---|
| N2 (refuerzo por acuerdo, puerta de valor) | 1/20 | no | 0.00 | peor | vacío |
| N2b (+ sesgo en la decisión, ventaja) | **13/20** | **10/20** | ±0.42 | 0.77 × N0 | **real** |
| N2c (+ estado = valor, experto 400k) | 11/20 | 13/20 | ±0.35 | 0.92 | real |
| N2d (+ habla sólo de lo consolidado) | 13/20 | 12/20 | ±0.34 | 0.79, **pareado 15/20** | real |
| N2e (+ alineación) | 7/20 | 7/20 | ±0.11 | 1.01 | real |

**Lo que sí quedó demostrado (y se puede escribir):** con refuerzo por ventaja y el símbolo en la decisión, **entre dos
organismos v13 emerge una convención de dos símbolos que ninguno tenía, arbitraria por semilla (el símbolo de rechazo
es el 0 en ~la mitad de las semillas) y que muere al barajar** (E1 ≈ 13/20, E3, E5). Lo que **no**: que el receptor le
asigne una magnitud útil (E2) ni que el beneficio llegue al 30 % (E4; llegó al 21–23 %, pareado 15/20 en N2d).
**Vocabulario permitido:** *emerge una convención; transmite poco.* No "significado" a secas, no "lenguaje".

**Lo que hay que cambiar para reabrirla (no hoy):** el **mundo**, no el receptor: equilibrar el muestreo (comida que
no desaparezca al morderla, o veneno que sí) y/o la escala (+1/−3 → simétrica en la señal social). El debate de niveles
5–10 la saca del camino crítico y propone volver a ella sólo si la composición social (N3) la necesita.


### Nivel 7 (composición temporal), experimento 1 del plan del debate: **v13 COMPONE historias de 1, 2 y 3 pasos — replicado**

Preregistro `experimentos/nivel7_3T_k/PREREGISTRO_3T_k.md` (sha `cf38dfab9c90645d` al correr); instrumento
`mundo_temporal_k.py` (`68736baafe7c8cdb`, desde `mundo_temporal_v13.py` `f9c3169b32f393d4`; **k = 1 idéntico bit a bit,
18/18 claves × brazos**). El mundo pone en la entrada el estímulo actual y los k anteriores; **manda el más profundo**
(A es comida si `h_k = B`); los intermedios son distractores. El organismo no cambia.

| k | C3 `sep` (mediana [mín, máx]) | `lift_q4` | C3C (canal falso) `sep` | C3 − C3C ≥ 1 | divisiones C3 | veredicto |
|---|---|---|---|---|---|---|
| 1 | **3.97** [1.55, 3.98] · réplica 3.96 | 0.374 · 0.372 | −0.24 · +0.03 | 20/20 · 20/20 | 5 · 4 | compone |
| 2 | **3.74** [1.47, 3.97] · réplica 3.81 | 0.375 · 0.379 | +0.08 · +0.29 | 20/20 · 19/20 | 11 · 10 | compone (predicho ≥ 3.0) |
| 3 | **2.24** [1.48, 3.38] · réplica 2.56 | 0.161 · 0.202 | +0.11 · +0.04 | 20/20 · 20/20 | 28 · 24 | compone (predicho ≥ 2.0; T3 al filo: 0.161 vs 0.15) |

Semillas 1–20 (`3T_k_s1-20_20260917_191732`, `767bd661747cf568`) y réplica 21–40 (`3T_k_s21-40_20260917_192053`,
`2000670ed82ede42`). C1/C1p/C2b `sep` 0 en todos los k (sin canal o sin plasticidad no hay composición). **Lectura:** la
división por conflicto de signo aprende a mirar el slot que importa e ignorar los distractores; cuesta más divisiones
(5 → 11 → 28) y la separación baja con la profundidad (3.97 → 3.74 → 2.24), pero el control barajado se queda en cero.
El canal falso divide más (60 con k = 3) sin separar: divide por ruido. **Vocabulario:** *compone hasta 3 pasos de
historia con distractores*; no "planifica", no "razona". Abierto: k = 4, 5 (¿dónde se agota?), y si las divisiones extra
cuestan capacidad (no se midió aquí: el organismo no cambió).


### Nivel 6 (planificación mínima), experimento 2 del plan: **v13 + tabla M elige la dirección hacia comida recordada que no ve — replicado**

Preregistro `experimentos/nivel6_mapa/PREREGISTRO_mapa.md` + enmienda 1 (control INVERTIDO, escrita tras el humo y antes
de las 20 semillas); instrumento `mundo_mapa.py` (`207d6a1954336b18`, desde `organismo_v13.py` por anclas; **perillas
apagadas ≡ v13, 9/9**). **Hallazgo de diseño (va contra el informe de nivel 6):** la retina del tronco **no es una
ventana**: `see()` devuelve el objeto más cercano de todo el anillo con su lado; la prueba de "meta fuera de la vista"
exige un mundo con visión limitada (`r_vis = 3`). Mundo: sitios fijos (comida en F, veneno enfrente) que reaparecen 50
pasos después de morderlos. `M[pos]` = último patrón visto ahí; con la retina vacía la boca suma por dirección el valor
descontado (`0.9^h`, `H = 20`) de lo recordado, con su propio `valor()` (dos vías y puerta, sin tocar); `gamma_M = 0.6`.
Prueba: 40 teletransportes por semilla con la comida a 4–12 casillas (invisible) por un lado; dirección del **primer paso**.

| brazo | acierto 1–20 (mediana; > 0.60) | acierto 21–40 | comida Q4 | muertes | lectura |
|---|---|---|---|---|---|
| **MAPA** | **0.812** (19/20) | **0.800** (20/20) | 490 | 3 | elige el lado de la comida recordada |
| SINMAPA | 0.475 (2/20) | 0.500 (2/20) | 332 · 346 | 42 · 46 | azar; y muere 14 veces más |
| CONGELADA (M nunca escrita) | 0.475 = SINMAPA **bit a bit** | 0.500 = SINMAPA | | | 0.50 por construcción, verificado |
| BARAJADO (Wp/Wn permutados) | 0.675 | 0.550 | | | **no decisivo**: la masa positiva de la vía lenta sobrevive a la permutación (enmienda 1) |
| SINCOMIDA (meta virtual) | 0.534 | 0.500 | 0 | 355 | sin sesgo motor |
| **INVERTIDO** (`Wp ↔ Wn`, `Wps ↔ Wns` en la prueba) | **0.114** (0/20) | **0.128** (0/20) | | | **huye** de la comida recordada: la dirección corre por el valor |

F1 (comida en Q4, MAPA > SINMAPA) **20/20 y 20/20**. Datos `mapa_s1-20_20260917_192813` (`ca8657637e8c2292`) y
`mapa_s21-40_20260917_193133` (`82a31af5259389ba`). **Vocabulario:** *elige la dirección hacia comida recordada fuera de
la vista, con el valor que ya tenía; y eso le da de comer*. No "planifica" (un paso de simulación, sin secuencia de
acciones ni horizonte aprendido). Abierto: horizonte real (dos metas, rodeo por veneno), `M` que se degrade, y si el
mismo mecanismo hacia ADELANTE (tabla) y hacia ATRÁS (3T-k) son la misma traza (nivel 6 ↔ 7, como propone el debate).


### Etapa 5 N3 (sentidos complementarios), experimento 3 del plan: **cae tal como se diseñó, y destapa ERR-23 (instrumento y medida)**

Preregistro `PREREGISTRO_N3.md` (regla `px0`; emisor ve píxeles 0–2, receptor ve 3–5; la conducta ajena reciente sesga
la decisión del receptor, `gamma_soc = 1.5`; control de saciedad = emisor con `alpha = 0`). Instrumento
`mundo_social_n3.py` (`1bc6dd2fb0a00224`, identidad con `mundo_social` 6/6). Datos `N3_s1-20_20260917_193532`
(`ef73dcc2a1347581`). Receptor, último cuarto: TECHO 0.996 · SOLO_E 0.994 · SOLO_R **0.697** (el sesgo parcial de la
vista 3–5 que la predicción ya anunciaba: 0.55–0.70) · **N0 0.978** · CONV 0.696 · SHUF 0.704 · SACIEDAD 0.564. S1 NO
(10/20), S2 NO (10/20), S3 OK (16/20), S5 NO. **Refutado como estaba escrito.**

**ERR-23 — dos fallos míos, visibles en los datos:**
1. *Canal simétrico con sesgo en los dos.* `gamma_soc` fue por `kw_org` a ambos: el emisor que ve la regla escuchaba
   al ciego (y aprendía vicariamente de él). Emisor solo 0.994 → emisor en CONV **0.681**; la señal que llegaba al
   receptor ya venía contaminada. La pregunta ("¿le sirve al ciego la conducta del que ve?") no se llegó a hacer.
2. *Acierto no balanceado.* Con "comida mordida + veneno rechazado / visitas", N0 dio 0.978 sin señal alguna: el emisor
   se come la comida en cuanto aparece, el receptor visita casi sólo veneno, lo rechaza y **se muere de hambre (667
   muertes)** "acertando". La medida premiaba no comer.

Corrección preregistrada (`PREREGISTRO_N3b.md`, semillas nuevas 21–40): knob `escucha` (sólo el receptor escucha),
**acierto balanceado** (½ · comida mordida/visitas a comida + ½ · veneno rechazado/visitas a veneno; rechazarlo todo
= 0.50) y validez añadida: el emisor en CONV debe seguir ≥ 0.90. Sin recalibrar sobre 1–20.


### N3b (tras ERR-23, semillas 21–40): **cae con la medida honesta; la señal cambia la conducta pero el mundo no deja probar comida**

Preregistro `PREREGISTRO_N3b.md`; instrumento `mundo_social_n3.py` (`c0bcedd4f8c12e43`, knob `escucha`; identidad 6/6);
datos `N3b_s21-40_20260917_194339` (`501d45749330eb13`). Acierto **balanceado** del receptor, último cuarto: TECHO 0.998 ·
SOLO_E 0.994 · **SOLO_R 0.539** (con la medida balanceada, el ciego a la regla está en el azar, como debía) · N0 0.545 ·
**CONV 0.561** · SHUF 0.533 · SACIEDAD 0.560. **Emisor en CONV 0.987** (ERR-23.1 corregido). S1 NO (13/20), S2 NO (14/20),
S3 NO (10/20). **Refutado.**

**Lo que sí muestran los datos (sin declararlo cerrado):** la conducta ajena **sí gobierna** al receptor: veneno mordido
en Q4 = **21** con señal honesta, **1 542** con la señal barajada (2 530 muertes), 162 solo, 2 552 con el emisor que no
sabe. La señal honesta le quita el veneno; lo que no le da es la comida, porque **casi no la encuentra**: en el humo de
la semilla 22, 210 visitas a comida contra 9 617 a veneno (el emisor se la come en cuanto reaparece al azar; el veneno
se queda). Es la asimetría de muestreo que cerró N2, por tercera vez. `PREREGISTRO_N3c.md` (escrito antes de ver este
veredicto): mismo montaje en un mundo donde lo mordido **reaparece en el mismo sitio** (`regen = 50`), semillas 41–60.


### N3c (mundo con reaparición en el mismo sitio, semillas 41–60): **montaje inválido, e informativo**

Preregistro `PREREGISTRO_N3c.md` (escrito antes del veredicto de N3b); instrumento `mundo_social_n3.py`
(`79e777ea57c649b4`, knob `regen`, mundo nunca vacío; identidad 6/6); datos `N3c_s41-60_20260917_195528`
(`a1c447c45fdbadd2`). Con `regen = 50` las visitas se equilibran (semilla 42: 1 671 comida / 3 558 veneno contra 210 /
9 617 en N3b) y las muertes caen de cientos a 2–4. Pero **S4 (validez) cae: SOLO_R = 0.997**. Con 8 objetos fijos que
reaparecen donde estaban, el receptor que ve sólo 3–5 **memoriza las 8 vistas** y ya no necesita la regla (la vista 3–5
lleva información parcial de `px0` y con 8 objetos casi siempre alcanza). No había nada que transferir.

Lo que sí mide: la conducta ajena **gobierna** al receptor: CONV 0.957 contra SHUF **0.683** (888 venenos, 727 muertes)
y SACIEDAD **0.689** (936 venenos), 20/20 pareados en ambos; N0 0.832 (la presencia del otro sin señal le quita comida).
CONV no supera a SOLO_R (8/20): con un receptor que ya sabe, la señal sólo puede estorbar o empatar.

Siguiente y último de hoy en esta línea: `PREREGISTRO_N3d.md` — los 8 objetos en **4 parejas con la misma vista 3–5 y
valencia opuesta** (ciego por construcción; SOLO_R ≈ 0.50 por diseño, no por resultado), semillas 61–80.


### Niveles 8 + 9, experimento 4 del plan (mundo largo con novedad y cambio de regla): **veredicto compuesto NO; tres hallazgos limpios**

Preregistro `experimentos/nivel8_mundo_largo/PREREGISTRO_mundo_largo.md`; instrumento `mundo_largo.py`
(`9f74ff6b5941e5a5`, desde `mundo_mapa.py`; **pool = None ≡ mapa, 3/3**). Mundo: `r_vis = 3`, 8 sitios fijos que
reaparecen; 50 patrones (peso 2, 3 y 4; valencias al azar 25/25 por semilla); uno nuevo cada 4 000 pasos en el sitio más
viejo (46 inyecciones, los 50 pasan); en t = 100 000 se invierte sin aviso la valencia de los 4 iniciales y de los
presentes. Datos `largo_s1-20_20260917_200026` (`8301d0d3f1b343a9`), semillas 1–20.

| brazo | adquisición (últimos 10, ≤ 30 vistos) | adquisición al final (50) | retención (10 primeros) | recuperación tras la inversión | muertes |
|---|---|---|---|---|---|
| V13 | **0.880** | **0.800** | 0.50 | **2 000 pasos** (≤ 10 000 en 18/20) | 30 |
| V13 + mapa | 0.700 | 0.700 | 0.50 | 0 (19/20 hallada; 13/20 antes que V13) | 31 |
| reciclado (V13 / mapa) | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 3 000 / 1 000 | 9 / 12 |

Curva de V13 por patrones vistos: 5: 1.00 · 10: 0.90 · 20: 0.90 · 30: 0.70 · 40: 0.80 · 50: 0.80. Mapa: 10: 0.80 · 30: 0.60 · 50: 0.60.
A1 NO (por el mapa), **A2 NO en la dirección buena** (predije caída a 0.55–0.70; se quedó en 0.80), A3 OK, R1 NO, C1 OK,
C2 NO.

**Hallazgos:** (1) **v13 sigue aprendiendo lo nuevo** con presupuesto fijo, hasta agotar los 50 patrones que caben en
la retina, en ~0.8 (con sólo 8 presentes a la vez no hay que saber 50 a la vez; la "capacidad" 35/60 era otro mundo).
(2) **Se recupera de un cambio de regla sin aviso** en ~2 000 pasos (nivel 9 en su forma mínima: viabilidad ante cambio).
(3) **El mapa daña la adquisición** (0.70 contra 0.88 a ≤ 30 vistos y 0.60 contra 0.80 al final) y no acelera la
recuperación: el organismo con mapa vuelve a los sitios que recuerda y **explora menos**; es el canje
explotación/exploración del nivel 8, medido. **Caveat de la medida R1:** "retención" mezcla olvido con la inversión de
patrones ya ausentes (los 4 iniciales se invirtieron sin poder verse): 0.50 no separa las dos cosas; para separarlas
hay que guardar `W` por patrón (no se guardó) — pendiente, no urgente. **Vocabulario:** *sigue aprendiendo hasta el
techo de la retina y se recupera del cambio; el mapa cobra la comida en exploración*. No "abierto", no "autónomo".


### N3d (receptor ciego por construcción, semillas 61–80): **TRANSFIERE entre sensores por conducta** — réplica 81–100 igual: 0.811 contra 0.516 solo, barajada 0.487, emisor que no sabe 0.515, 20/20 en los tres (N3d_s81-100_20260917_201205, 454fb54abddb2146)

Preregistro `PREREGISTRO_N3d.md`; instrumento `mundo_social_n3.py` (`42a7797c2dbccea7`, knob `tipos_fijos`; identidad
6/6); datos `N3d_s61-80_20260917_200706` (`88261db047ba8129`). Mundo: 8 objetos = 4 parejas de patrones de peso 3 con la
**misma vista en los píxeles 3–5 y valencia opuesta** (`px0` decide), reaparecen en su sitio a los 50 pasos. Receptor ve
3–5 (ciego a `px0` por construcción), emisor ve 0–2 y no escucha; la conducta ajena reciente (≤ 400 pasos) sesga la
boca del receptor (`gamma_soc = 1.5`). Acierto balanceado del receptor, último cuarto:

| condición | acierto | veneno Q4 | muertes | lectura |
|---|---|---|---|---|
| TECHO / SOLO_E | 0.998 / 0.998 | 1 / 2 | 1 / 0 | la regla se aprende con `px0` a la vista |
| **SOLO_R** | **0.515** [0.50, 0.53] | 332 | 86 | ciego por construcción: azar, como debía |
| N0 (pareja sin señal) | 0.503 | 244 | 534 | la presencia sola no ayuda (y le quita comida) |
| **CONV** (conducta honesta) | **0.822** [0.77, 0.85] | 331 | 80 | **acierta con la conducta del que ve** |
| SHUF (conducta barajada) | 0.484 | 1 128 | 1 176 | sin contenido, sólo daño |
| SACIEDAD (emisor con `alpha = 0`) | 0.508 | 1 270 | 308 | un emisor que no sabe no transfiere nada |

S1 (≥ 0.80 y > SOLO_R **20/20**), S2 (> SHUF **20/20**), S3 (> SACIEDAD **20/20**), S4 (validez: emisor en CONV 0.998),
S5 (N0 > SOLO_R 1/20): **todos pasan.** Es el nivel 5 del brief en su forma mínima: *un organismo que no puede saber usa
la conducta reciente de otro que sí sabe, sobre el mismo objeto, y acierta*. Cuatro intentos hicieron falta (N3, N3b,
N3c, N3d), y los tres fallos fueron **del instrumento, la medida o el mundo**, no del organismo: canal simétrico, acierto
sin balancear, mundo que se come la comida, receptor que memoriza sitios. Cada uno está registrado.
**Vocabulario:** *transfiere por conducta; no "comunica", no "entiende"*. Abierto: cuánto dura la transferencia sin el
emisor presente (¿aprende algo propio o sólo obedece?: `W` del receptor), y XOR entre dos (composición social real).


### Bloque 1a (día 6): 3T-k con k = 4 y 5 — **compone hasta 4; a 5 se agota el pool de celdas y la ventaja conductual cae al filo**

Preregistro: `PREREGISTRO_3T_k.md` enmienda 2 (predicción: k = 4 compone, k = 5 no por agotamiento del pool de 90).
Datos `3T_k45_s1-20_20260917_204451` (`66e4291b9b91f5a4`), semillas 1–20, identidad k = 1 18/18.

| k | C3 `sep` | `lift_q4` | C3C `sep` | C3 − C3C ≥ 1 | divisiones | **celdas** | veredicto |
|---|---|---|---|---|---|---|---|
| 4 | **1.99** [1.71, 3.24] | 0.152 | +0.01 | **20/20** | 42 | **72** | **compone** (predicho: sep 1.5–2.2, divisiones 40–55 ✓) |
| 5 | 1.94 [1.15, 2.23] | **0.144** | 0.00 | 19/20 | 60 | **90 / 90** | **NO** por T3 (0.144 < 0.15), con el pool agotado |

**Lectura precisa:** a k = 5 el organismo ya no tiene celdas (60 divisiones = las 60 libres; 90/90), y la refutación
que había escrito ("sep < 1.0 o pareado < 15/20") **no** ocurrió: la separación sobrevive (1.94, 19/20 pareado); lo que
cae es la ventaja conductual en el último cuarto (0.144, al filo del 0.15). El control barajado divide igual (60) sin
separar. **Vocabulario:** *compone hasta 4 pasos de historia con distractores; a 5 se agota el pool y la ventaja se
diluye*. La causa del techo es el **presupuesto de celdas** (el criterio de parada del debate: "si el límite es el pool,
la salida es crecer celdas o cambiar la lectura", no otra regla). Serie completa k = 1…5: sep 3.97 / 3.74 / 2.24 / 1.99 /
1.94; celdas ~35 / 41 / 58 / 72 / 90.


### Bloque 1b (día 6): mundo largo, semillas 21–40, `W` por patrón — **réplica de los hallazgos; la retención de lo ausente es mala (interferencia), no inversión**

Enmienda 1 de `PREREGISTRO_mundo_largo.md`; datos `largo_s21-40_20260917_204840` (`5738e6062d583294`); identidad 3/3.
Réplica: V13 adquisición 0.90 (≤ 30 vistos) / 0.80 (final); MAPA 0.70 / 0.70; reciclado 1.00; V13 recupera en 4 000
pasos (18/20 ≤ 10 000); MAPA recupera antes (16/20) y **muere menos** (2 contra 8 en los 20 000 pasos posteriores; mi
predicción decía "muere más": refutada en la dirección buena — el mapa usa el valor vivo, muerde una vez lo que ya no es
comida y deja de ir).

**Retención separada (lo nuevo de la enmienda):** patrones 5–10 vistos, **nunca invertidos**, ausentes ≥ 150 000 pasos:
V13 **0.67**, MAPA **0.50** (predije ≥ 0.70: NO). Los 4 iniciales invertidos en ausencia: 0.38 / 0.25 (predije ≤ 0.25 por
construcción: NO en V13 — sus valores se acercaron a cero y el signo es ruido). **Lectura:** v13 **no retiene** lo que
deja de ver mientras aprende otras 40 cosas con las mismas celdas: interferencia por códigos compartidos (la misma
causa de "generalización = interferencia"), peor con mapa (menos exploración, celdas 78 contra 90). No es la
inversión. Queda como límite medido de nivel 8 (retención en ausencia) y del nivel 4.

### Bloque 1c (día 6): N3d mudo — **la conducta ajena gobierna la decisión; no enseña**

`PREREGISTRO_N3d_mudo.md`; instrumento `mundo_social_n3.py` (`e6b3ee1ef5b8a4be`, knob `mudo_desde`; identidad 6/6); datos
`N3dmudo_s61-80_20260917_205345` (`ae5c451879848d1e`), mismas semillas 61–80 de N3d (los primeros 150 000 pasos son la
misma trayectoria). Último cuarto sin señal: CONV_MUDO **0.503** [0.50, 0.51] contra CONV 0.822 (20/20 pareado) y SOLO_R
0.515 (|Δ| = 0.012). **Predicción cumplida:** el receptor ciego por construcción obedece, no aprende (no puede: su vista
no lleva la regla). Dato extra: muere **189** veces en el cuarto mudo contra 86 el que nunca escuchó: la obediencia
crea **dependencia** (sin la señal está peor que solo). Vocabulario: *la conducta ajena gobierna la decisión; no enseña*.


### Bloque 2 (día 6): curiosidad por progreso de error contra el canje del mapa — **REFUTADA: no devuelve la exploración**

Preregistro `experimentos/nivel8_curiosidad/PREREGISTRO_curiosidad.md`; instrumento `mundo_largo_c.py` (`4a24460f504f003e`,
`gamma_C = 0` ≡ `mundo_largo`, identidad 3/3 con el mundo completo); datos `curiosidad_s41-60_20260917_211739`
(`b23a85f7695c6ee8`), semillas 41–60. Dos arranques previos se abortaron sin datos por un `KeyError` de mi runner
(registrado en el commit `d4367e0`).

| brazo | adquisición (≤ 30 vistos) | final | retención nunca invertidos | comida Q4 | muertes | celdas |
|---|---|---|---|---|---|---|
| V13 | **0.900** | 0.800 | 0.67 | 837 | 30 | 90 |
| MAPA | 0.704 | 0.700 | 0.67 | 968 | 26 | 84 |
| **MAPA + curiosidad** | **0.700** | 0.600 | 0.83 | 974 | 22 | 77 |
| MAPA + curiosidad barajada | 0.700 | 0.700 | 0.83 | 968 | 28 | 81 |

P1 NO (0.700; > MAPA en 7/20), P2 OK (comida 974, 19/20), P3 NO (curiosidad = barajada, 6/20). **La curiosidad por progreso
del error no explora**: el sesgo actúa sólo sobre sitios recordados, y lo nuevo entra en sitios cuyo progreso es cero
hasta la primera mordida (la refutación ya escrita en el preregistro). Observación no preregistrada (sólo se anota): la
retención de lo ausente sube a 0.83 con curiosidad y con su control (0.67 sin) — el sesgo extra reduce visitas, no es
un efecto del progreso (el barajado lo comparte). **Siguiente candidato, ya escrito antes:** *novedad de sitio* (sesgo
hacia el sitio que lleva más tiempo sin visitarse), no otra perilla de esta. Vocabulario: *el canje exploración /
explotación del mapa sigue abierto*.


### Bloque 3 (día 6): XOR como límite de lectura — **refutado como estaba escrito; la lectura cuadrática SÍ aprende XOR y la puerta la esconde (hipótesis, se prueba en 3b)**

Preregistro `experimentos/nivel7_xor_lectura/PREREGISTRO_xor_lectura.md`; instrumento `organismo_v13q.py` (`f1c70d646f1820e7`,
`lectura='lineal'` ≡ `organismo_v13g`, identidad 6/6); datos `xor_lectura_s1-20_20260917_213124` (`b056086985dd26fc`).

| lectura | `xor01` acc (nunca vistos, a priori) | `xor01` ba (conducta) | `px0` acc | `azar` acc |
|---|---|---|---|---|
| lineal (v13) | **0.438** [0.12, 0.62] | 0.301 | 0.850 | 0.500 |
| **cuadrática** | **0.438** [0.19, 0.62] · `W_lenta(P0·P1)` = **−2.65** | 0.415 | 0.800 | 0.500 |
| random15 (control) | 0.500 | 0.402 | 0.700 | 0.500 |

X0 OK, X1 **NO** (0.438; > lineal 8/20), X2 OK, X3 OK (la regresión lineal no cae), X4 NO. **Refutado como estaba escrito.**
Pero el dato que no estaba previsto manda: la vía lenta cuadrática **aprendió la estructura de XOR** (el peso neto del
producto `P0·P1` es −2.65, grande y del signo correcto) y el acierto total no se movió. Hipótesis escrita antes de
probarla (`PREREGISTRO_xor_lectura_3b.md`): **la puerta de familiaridad esconde la vía lenta**: un patrón nunca visto
cuyo código Kenyon comparte ≥ 3 celdas consolidadas con los entrenados cuenta como "familiar" y la boca lee la vía
rápida (memoria de casos, engañosa en XOR porque el solapamiento de códigos no sigue la regla). En `px0` no se nota
porque el solapamiento sí correlaciona con la regla. Nota de diseño: `phi` no tiene término constante; los patrones con
`P0 = P1 = 0` (4 de 20) sólo pueden clasificarse por ruido → techo esperado de la lectura cuadrática ≈ 0.85–0.90.
Vocabulario: *XOR no se generaliza en v13; la lectura cuadrática lo representa; falta saber si la puerta lo tapa*.


### Bloque 3b (día 6): ¿la puerta esconde la vía lenta? — **NO: la vía lenta cuadrática sola tampoco sabe XOR (0.50). El límite es la regla de aprendizaje**

Preregistro `PREREGISTRO_xor_lectura_3b.md`; instrumento `organismo_v13q.py` (`0b59eb03858df3a8`, lecturas puras
`W_lenta_apriori` y `familiar_apriori`; identidad 6/6); datos `xor_3b_s21-40_20260917_213752` (`f2fb5920aba1231b`).

| brazo | `xor01` acc | `xor01` **acc de la vía lenta sola** | familiar (puerta lee la rápida) | `px0` acc / lenta | `W_lenta(P0·P1)` |
|---|---|---|---|---|---|
| cuadrática, puerta 3 | 0.500 | **0.500** [0.31, 0.75] | 0.33 | 0.900 / 1.000 | −2.68 |
| cuadrática, sin puerta | 0.500 | 0.438 | — | 0.700 / 0.950 | −0.93 |
| lineal, puerta 3 | 0.438 | 0.375 | 0.33 | 0.900 / 1.000 | — |

Y1 NO, Y2 NO (0/20), Y3 NO. **Mi hipótesis de la puerta queda refutada** (y bien: la puerta sólo lee la rápida en un
tercio de los nunca vistos). La vía lenta cuadrática **representa** el producto (−2.68) pero **no clasifica** XOR: sus
**marginales** de `P0` y `P1` quedan en cero. Diagnóstico (escrito después de ver los datos, así que es hipótesis para 3c,
no resultado): la regla de la vía lenta reparte cada error por igual entre TODAS las entradas activas del patrón (dos
canales no negativos `Wps/Wns` + drenaje de la parte común); cuando muerde `(1,1)` (veneno) empuja `Wns` en `P0`, `P1`
y `P0·P1` a la vez, y el drenaje se lleva luego lo que `P0` y `P1` habían ganado como comida en `(1,0)` y `(0,1)`. Una
regla delta con signo (LMS: un solo vector de pesos, error residual) pondría lo negativo sólo donde distingue, en el
producto. **XOR es un límite de la REGLA de la vía lenta**, no de la dimensión (random15 = cuadrática = lineal) ni de la
puerta. Vocabulario: *v13 no generaliza XOR; la lectura cuadrática lo representa pero su regla no lo separa*. Siguiente
(bloque 3c, lo diseña un trío de agentes con puente, `registro/investigacion/PUENTE_xor.md`): vía lenta con regla delta
con signo, controles: la misma regla con lectura lineal (debe seguir en ≤ 0.6) y `px0`/`azar` sin caer.


### Auditoría del equipo (agente auditor, Sonnet) sobre bloques 2, 3 y N3d mudo — `registro/investigacion/AUDITORIA_bloques_2_3_20260917.md`

Sin hallazgos bloqueantes. Decisiones del coordinador sobre cada uno: **(1)** "la puerta enmascara la vía lenta" — el
auditor leyó antes del bloque 3b, que ya lo **refutó** (familiar 0.33; vía lenta sola 0.50): superado. **(2)**
`n_sesgo_soc` no tiene índice de cuarto, así que el chequeo secundario de N3d mudo ("≈ 0 en Q4") no es verificable desde
el JSON: **aceptado**; se añadirá `n_sesgo_soc_q` (4 posiciones) al instrumento social antes de reusarlo; el veredicto
M1/M2 no depende de eso. **(3)** el control de prioridad barajada permutaba sobre las 90 celdas, incluidas las inactivas
(progreso 0): diluye el control (no lo infla); **aceptado** y transmitido al diseñador de "novedad de sitio" para que su
control permute sólo sobre celdas/sitios activos. **(4)** aceptado como práctica: listar en cada preregistro la
puerta como causa candidata cuando el resultado depende del readout. **(5)** `None → 0.0/0.5` sin guardia y `med([])`
en los runners: **aceptado**; se corrige en los runners nuevos. Las cuatro trampas: sin hallazgos nuevos.


### Bloque 5 (N2f, diseño del agente diseñador): humo de un proceso antes de correr — **dos hallazgos que cambian el diseño; no se corre como estaba**

Diseño entregado (en el worktree del agente; se integra con la versión 2): N2b letra por letra sobre `mundo_social_n3`
con `regen = 50`, E1–E6 sin suavizar, puertas de validez nuevas K3 ("queda algo que enseñar": veneno Q4 del novato solo
≥ 20) y K4 ("las visitas se equilibran": emisiones muerde ≥ 1/5 de rechaza). Humo (semilla 81, progenitor + N0 + CONV,
identidades K1a/K1b idénticas con `regen = None`):
1. **Por primera vez en la línea N2 hay magnitud:** contraste **−1.28 / +1.28** (serie N2 0.00 · N2b ±0.42 · N2c ±0.35 ·
   N2d ±0.34 · N2e ±0.11), consistencia 0.9994, 6 272 decodificaciones. Las emisiones se equilibran ×18 (rechaza 19 335 /
   muerde 5 524 = 0.29 contra 0.016 en N2d), aunque por objeto sigue ~7:1.
2. **Pero el símbolo "desenseña" al que sabe:** el novato de CONV muerde **135** venenos contra **34** el de N0: sus
   valores de veneno se quedan en −1.29/−1.36 (el valor del símbolo) en vez de −2.45/−2.34 (lo que aprende solo). El
   empujón vicario arrastra el valor propio hacia la magnitud del símbolo, más grosera que lo ya sabido.
3. **Fallo de validez del mundo con `regen`:** al reaparecer siempre el mismo tipo en el mismo sitio, los 8 objetos
   iniciales se repiten 200 000 pasos y **los patrones de test nunca aparecen** (5 patrones presentes de 20) → K3 caería
   (el mismo fallo S4 de N3c). En N3c/N3d era intencional (`tipos_fijos`); en N2 no.

**Decisión (coordinador):** no correr; versión 2 con dos cambios en brazos separables: `regen_rota` (al regenerar, el
tipo se vuelve a sortear: reaparición en sitio + flujo de patrones) y `escucha_si_no_sabe` (el empujón vicario sólo si
|valor propio| < |valor del símbolo|). Brazos CONV (ambos), CONV_MUNDO (sólo el mundo), N0, SOLO, INNATO, SHUF.
Predicción escrita: E2 pasa en CONV y CONV_MUNDO (la magnitud viene del mundo); E4 sólo en CONV. Vocabulario por
ahora: *en el mundo con reaparición el símbolo adquiere magnitud; enseña al que no sabe y desenseña al que sabe*.


### Bloque 2 bis (día 6): novedad de sitio (diseño del agente diseñador) — **refutada a dosis 0.6; la dosis 1.8 (lectura) casi recupera la exploración sin cobrar la comida → serie confirmatoria**

Preregistro `experimentos/nivel8_novedad_sitio/PREREGISTRO_novedad_sitio.md`; instrumento `mundo_largo_n.py`
(`f3e9ad0118f1d6c5`, `gamma_N = 0` ≡ `mundo_largo` con el mundo completo, 3/3; reconstruido en la copia principal con el
mismo sha); datos `novedad_s61-80_20260917_215405` (`6ccb7e1133333cd9`). Mecanismo: `t_visita[pos]` al pisar un sitio y,
con la retina vacía, sesgo `gamma_N · Σ disc^h · min(1, (t − t_visita)/tau_N)` sobre los sitios que `M` conoce.

| brazo | adquisición (≤ 30) | comida Q4 | muertes | visitas / equidad | celdas |
|---|---|---|---|---|---|
| V13 | 0.900 | 836 | 32 | 13 559 / 0.615 | 90 |
| MAPA | 0.704 | 963 | 34 | 5 664 / 0.120 | 86 |
| MAPA + novedad 0.6 (criterio) | **0.800** | 946 | 28 | 7 982 / 0.292 | 90 |
| + novedad barajada | 0.741 | 974 | 26 | 6 633 / 0.145 | 88 |
| + novedad constante (lectura) | 0.700 | 1 158 | 19 | 7 288 / 0.133 | 86 |
| **+ novedad 1.8 (lectura, dosis)** | **0.874** | 929 | 36 | 13 515 / 0.518 | 90 |

P1 NO (0.800; > MAPA 14g/5e/1p), P2 NO (14/20), P3 OK (13g/4e/3p; barajada no supera a MAPA), P4 OK (> constante 15/20).
**Refutada como estaba escrita**, pero con la lectura que el preregistro reservaba: el mecanismo va en la dirección
correcta y la diferencia con la barajada y con la constante es real; lo que no alcanza es la **escala** (novedad
máxima +0.6 contra recuerdo de veneno −3). La dosis 1.8 recupera la equidad de visitas de V13 (0.518 contra 0.615) y casi
su adquisición (0.874 contra 0.900) conservando la comida del mapa (929 contra 963). **Decisión (regla 12, cláusula (a)
del preregistro):** serie confirmatoria con la dosis 1.8 en semillas nuevas 81–100, mismos criterios (enmienda 1). Nada
se ajusta sobre 61–80. Vocabulario si pasa: *vuelve a los sitios que lleva tiempo sin pisar y por eso encuentra lo nuevo*.

### N2f v2 (agente diseñador): la rotación de tipos arregla K3 y **destruye K4** — balance y flujo son incompatibles con retirada sólo al morder

Humo v2 (semilla 81; `regen_rota`: al regenerar un sitio se vuelve a sortear el tipo): patrones presentes 20 ✅ (K3 ok),
pero la razón rechaza/muerde vuelve a **36 201 / 794 = 0.022** (v1: 0.286; N2d: 0.016) y las visitas comida/veneno
**decaen por cuarto** (0.037 → 0.018): **el mundo se absorbe en veneno**, porque un objeto sólo se retira al morderlo:
la comida se muerde, rota y puede volver veneno; el veneno se rechaza y nunca sale. Contraste ±0.30, `decodificados = 0`
→ la puerta vicaria nunca abre y la segunda perilla (`escucha_si_no_sabe`) no tiene ocasión (CONV ≡ CONV_MUNDO bit a
bit). **Reinterpretación de la v1:** el reequilibrio ×18 lo daba la **congelación** del mundo (5 patrones), no la
reaparición. Identidad con las dos perillas apagadas 8/8 (N3c/N3d protegidos). **Decisión:** no se corre; tercera
perilla `vida` (caducidad por objeto: el veneno también sale) con puerta de validez propia, la construye el mismo agente;
se corre el día 7. Sonda de dinámica sin organismos (razón comida/veneno): v1 0.366 · v2 0.015 · `vida = 200` 0.14 ·
`vida = 50` **1.01**. Fallo de predicción del agente registrado por él mismo: acertó K3, falló K4.

### Trío XOR (agentes A, B, C con puente `registro/investigacion/PUENTE_xor.md`): **propuesta única firmada, hipótesis para preregistrar (3d), no resultado**

A (regla delta con signo, sin drenaje): **refutada** — `acc_lenta` en `xor01` 0.250 (peor que 0.50 de dos canales) aunque
el producto aprende −2.2: sin regularizador las otras 20 entradas absorben correlación espuria de 8 patrones (sistema
subdeterminado). B (drenaje `lam` y tope `clip_s`): **refutada por ablación** — ninguno mueve nada (24 corridas); el
tope nunca actúa. C (lectura y muestreo): sin término constante el patrón `(0,0)` vale exactamente 0 (prueba algebraica);
la constante sola sube la mediana de 0.25 a 0.375; **en 3 de 10 semillas una clase XOR entera no recibe ninguna
mordida antes de la sonda** (límite del muestreo del mundo, no de la regla); ~331 actualizaciones de la vía lenta antes
de la sonda. Propuesta fusionada (firmada por los tres): `phi' = phi + [1]`, vector con signo `Ws`, decaimiento
multiplicativo `Ws·(1 − lam_lenta)` con `lam_lenta` ∈ [0.001, 0.003]; prueba exploratoria de C: 0.50 y 0.31 — no llega a
0.75. **Decisión:** 3d se preregistra el día 7 con instrumento único por anclas (no tres copias), sonda `Ws_apriori`,
controles lineal/random15/azar, y con la cota de muestreo escrita (mediana sobre 20 semillas, no 0.75 por semilla).
Vocabulario: *XOR sigue sin generalizarse; tres mecanismos aislados refutados; la fusión es hipótesis*.

### Gemelos compilados de los mundos (compiladores Opus) y revisión independiente del gemelo del tronco

- `mundo_temporal_k_rapido.py` (3T-k): **146/146** idéntico (6 brazos × k = 1…5 × 3 semillas + 7 variantes), ×74; suma por
  pares de NumPy reproducida bit a bit; **trampa hallada:** función recursiva + `cache=True` → el proceso que carga el
  cache segmenta sin traza (habría matado a cada worker de `Pool`); resuelta con pila explícita; regla 9 de `EQUIPO.md`.
- `organismo_v13q_rapido.py` (mundo de regla / XOR): **81/81 + 243/243 + 81/81** idéntico, ×67–77; pendiente añadir las
  lecturas `W_lenta_apriori`/`familiar_apriori` del 3b (el gemelo se construyó sobre la versión previa).
- `mundo_mapa_rapido.py`: **90/90** idéntico (los seis brazos de `corre_mapa` + 18 caminos de cobertura), ×30–38 con mapa
  y ×52–120 sin mapa; regla 9 comprobada (proceso nuevo leyendo el cache).
- Revisión del gemelo del tronco (Sonnet): **apto para confirmar**; 257/257 nuevas corridas idénticas (rejilla ampliada de
  18 configuraciones × 10 semillas, 200k × 5, `learn=False` × 5); H1: `puerta` negativa explícita divergía del tronco (que la
  trata como 0) → el gemelo ahora la **rechaza** con `ValueError` (ningún experimento la usa); H4: `nuevo_val` inválido
  ahora falla en vez de callar. Cada gemelo queda integrado sólo tras repetir su arnés en la copia principal (en curso).


### Novedad de sitio, dosis 1.8, semillas 81–100 (enmienda 1): **cae otra vez; línea cerrada en dos dosis, como estaba escrito**

Datos `novedad_alta_s81-100_20260917_221523` (`20a8d18cdfd55406`); identidad 3/3. V13 0.887 · MAPA 0.700 · **MAPA + novedad
1.8: 0.841** (> MAPA 17g/2e/1p; equidad de visitas 0.455 contra 0.139 del mapa y 0.710 de V13) · barajada 0.800 (10g/4e/6p
contra MAPA: no supera) · constante 0.681. P1 **NO** (0.841 < 0.85), P2 **NO** (comida 918 contra 971: ≥ 0.9 × MAPA sólo en
9/20), P3 OK, P4 OK. **Lectura honesta:** el mecanismo hace lo que dice (devuelve visitas y sube la adquisición 0.70 →
0.84, distinguible del control barajado y del constante), pero **no llega al criterio y cobra comida en la mitad de las
semillas**: el canje exploración/explotación se **desplaza**, no se rompe. Por el preregistro (enmienda 1: "si P1
vuelve a fallar, refutada en dos dosis y no se prueba una tercera") la línea queda cerrada. Vocabulario: *la novedad de
sitio mueve el canje; no lo resuelve*. El canje del mapa sigue abierto (nivel 8) y ya lleva dos candidatos refutados
(curiosidad por progreso, novedad de sitio); el siguiente, si lo hay, debe atacar la **escala del recuerdo de veneno**
(−3 pesa más que cualquier atracción de +0.6…+1.8), no otra atracción.


### Bloque 5 — N2f v3 (semillas 81–100): **montaje VÁLIDO por primera vez, y N2 cae por sexta vez → N2 cerrado con dos mundos**

Preregistro `PREREGISTRO_N2f.md` (v3 + enmiendas 1–2, del agente diseñador); instrumento `mundo_social_n3.py`
(`ef227f833c5bf46a`: `regen = 50`, `regen_rota`, `vida = 100` fijado por las puertas K3/K4/K5 en el humo,
`escucha_si_no_sabe`; identidad con las tres perillas apagadas **8/8** en mi copia contra la versión anterior
`e6b3ee1ef5b8a4be`, N3c/N3d protegidos); datos `N2f_s81-100_20260917_222744` (`56902998e66b714e`).

**Validez (todas pasan):** K2 símbolos recibidos 6 108; K3 queda algo que enseñar (veneno Q4 del novato solo 50 ≥ 20);
K5 el mundo se aprende solo (veneno Q1 → Q4: 123 → 50, 19/20); **K4 equilibrio de emisiones: rechaza 18 216 / muerde
4 198 = 0.23** (N2d: 0.016; ×14), 1 156 "muerde" oídas. Es el mundo que la clausura de N2 pedía.

| condición | veneno total | veneno Q4 | muertes | símbolos recibidos | decodificados |
|---|---|---|---|---|---|
| SOLO | 278 | 50 | 10 | — | — |
| N0 | 340 | 68 | 20 | 0 | 0 |
| **INNATO** (mapa correcto dado) | **60** | 0 | 16 | 7 568 | — |
| CONV (mundo + no desenseñar) | 314 | 57 | 18 | 6 108 | 50 |
| CONV_MUNDO (sólo mundo) | 311 | 66 | 19 | 6 040 | 334 |
| SHUF (símbolo barajado) | 177 | 28 | 12 | 6 021 | 0 |

E1 convención 11/20 (consistencia 0.99, distintos 14/20) · **E2 contraste −0.29 / +0.32** (4/20) · E3 sostenida · **E4 sin
beneficio** (314 contra 340; pareado 12/20) · **E5 barajar no destruye** (el receptor con símbolo barajado muerde *menos*
veneno, 177) · A1/A2 no atribuibles. `N2f_EMERGE = False`.

**Lectura:** ya no vale la excusa del mundo. Con visitas equilibradas y patrones que fluyen, el canal de dos símbolos
sigue sin adquirir magnitud ni beneficio; y el brazo INNATO (60 venenos contra 278 solo) muestra que **el canal sí
podría servir si el significado estuviera dado**: lo que no funciona es **aprender el significado** con refuerzo por
ventaja y símbolo como sesgo. El barajado que "ayuda" (177) es el aviso de que el sesgo del símbolo actúa como ruido que
frena la boca, no como información. **Cierre:** *N2 cerrado con dos mundos* (cláusula de refutación del preregistro).
Seis diseños (N2, N2b–e, N2f) y ~750 corridas. Vocabulario: *emerge una convención débil; no adquiere significado; el
canal serviría con significado dado*. Reabrir sólo con un mecanismo de significado distinto (p. ej. que el receptor
aprenda el símbolo por **predicción** de lo que va a sentir, no por refuerzo del emisor) — apunta al bloque 6.


### 3T-k k = 4 y 5, réplica en semillas 41–60 con el gemelo compilado (día 7, 22:45): **k = 4 NO replica en la ventaja conductual → lo declarable es "compone hasta 3"**

Datos `3T_k45_s41-60_20260917_224306` (`f06b95f81b49f5ca`); identidad k = 1 18/18 y gemelo ≡ original 3/3 (primera corrida
confirmatoria con `--rapido`: 300 corridas en ~1 min). k = 4: `sep` **1.94** [1.54, 2.92] (T2 ≥ 1.5 ✅), C3 − C3C ≥ 1 en
**20/20** ✅, `solap_A` 0.06 ✅, pero `lift_q4` **0.140 < 0.15** (T3 ❌; en 1–20 fue 0.152) → NO compone por el criterio
conductual. k = 5: sep 1.87, T5 20/20, lift 0.133, celdas 90/90 → NO (como en 1–20).

**Corrección de vocabulario (la réplica manda):** *compone hasta 3 pasos de historia con distractores (replicado); a 4 y 5
la separación sobrevive en las dos series (≥ 1.9, 20/20 pareado) pero la ventaja conductual del último cuarto queda al
filo del umbral (0.152 / 0.140 en k = 4; 0.144 / 0.133 en k = 5) con el pool de celdas agotándose (78–90/90)*. La
composición representacional llega más lejos que la conductual; el umbral 0.15 de `lift_q4` es el de 3T (v8) y no se toca.
Lección: sin la réplica habríamos escrito "hasta 4". El gemelo hace la réplica gratis: **toda serie confirmatoria se
replica desde ahora**.


### Mapa, tercera serie (41–60, gemelo compilado `--rapido`, identidad 9/9 + 3/3): **lo esencial replica por tercera vez; el control de sesgo motor es ruidoso → ERR-24**

Datos `mapa_s41-60_20260917_224442` (`71ab7d3f6640c030`). MAPA **0.800** [0.65, 0.93], > 0.60 en **20/20** · SINMAPA 0.475 ·
CONGELADA = SINMAPA bit a bit · BARAJADO 0.600 · **INVERTIDO 0.150** (huye) · comida Q4 491 contra 345, **F1 20/20** · muertes 2
contra 41. P1, C1, C2, C4, C5, F1 pasan. **C3 (SINCOMIDA) cae: 0.621** (series anteriores 0.534 y 0.500) con **28/40
teletransportes sin moverse** y 32/40 ciegos al llegar: el control cuenta sólo primeros pasos (~12 por semilla) y la meta
virtual cae a veces dentro de la vista del veneno; la mediana salta entre series por ruido de muestreo, no por sesgo
motor (SINMAPA, que sí tiene el mismo cuerpo y las mismas patas, se queda en 0.475–0.500 en las tres series).

**ERR-24 (control, no organismo):** el control SINCOMIDA tal como está escrito no fija su n efectivo (no fuerza el
movimiento ni excluye llegadas con veneno a la vista) y puede fallar o pasar por azar. Corrección para la próxima serie
del mapa (protocolo, no organismo): en la prueba, contar sólo teletransportes ciegos al llegar y exigir ≥ 30 primeros
pasos por semilla (subir `max_pasos` o bajar `E_test`), o sustituir el control por SINMAPA (mismo cuerpo, sin mapa),
que es el que realmente mide el sesgo motor. El veredicto compuesto de esta serie es NO por C3; **lo que replica tres
veces es la afirmación**: *elige la dirección hacia comida recordada fuera de la vista con el valor que ya tenía, y eso
le da de comer*. Nada se recalibra: la corrección aplica a series nuevas.


### Gemelo compilado del mundo de regla en la batería de generalización: **reproduce la batería registrada de v13 40/40 (semillas 101–120)**

`bateria_generaliza.py organismo_v13_rapido 20 --desde 101 --log` → `regresion_generaliza_organismo_v13_rapido_20260917_224731`:
K 20/20, G1 px0 0.800 / azar 0.500 / px0 > azar 18/20, G2 px0 0.892 / azar 0.458 / 20/20 — **idéntico semilla a semilla**
(acc, ba, divisiones, celdas, muertes: 0 de 40 difieren) a la batería de congelación de v13
(`regresion_generaliza_organismo_v13_20260917_170148`, semillas 101–120). Tiempo: **3.6 s** contra ~40 min·CPU. Nota de
método: mi primera comparación (semillas 41–60 contra el registro de 101–120) parecía una divergencia y no lo era —
comparar siempre las mismas semillas antes de sospechar del gemelo. La batería acepta ahora el módulo
`organismo_v13_rapido`; la regla 1 de `CLAUDE.md` puede correrse con él en segundos (con la identidad verificada).


### Bloque 3d (día 7, 22:55): regla fusionada del trío (constante + vector con signo + decaimiento) — **REFUTADA (0.500); lo que queda es un problema de identificabilidad**

Preregistro `experimentos/nivel7_xor_lectura/PREREGISTRO_xor_3d.md` (agente diseñador; `lam_lenta = 0.002` atado a T = 100 000 por
~331 actualizaciones pre-sonda); instrumento `organismo_v13q3.py` (`b71bbe41a7326aaf`, knobs apagados ≡ `organismo_v13q`
12/12); datos `xor_3d_s41-60_20260917_225535` (`3e2489b1b02d4f19`), 360 corridas.

| brazo (xor01, nunca vistos) | `acc` | **`acc_lenta`** | `Ws(P0)` | `Ws(P1)` | `Ws(P0·P1)` |
|---|---|---|---|---|---|
| lineal (v13) | 0.375 | 0.344 | +0.03 | −0.45 | — |
| cuadrática, dos canales (3b) | 0.562 | 0.500 | −0.11 | −0.39 | −1.16 |
| **cuadrática + constante + delta con signo + decaimiento** | 0.500 | **0.500** [0.25, 0.81] | −0.00 | −0.29 | −0.83 |
| lo mismo sin constante | 0.531 | 0.500 | −0.00 | −0.27 | −0.91 |
| lineal + delta (control) | 0.406 | 0.406 | — | — | — |
| random15 + delta (control) | 0.500 | 0.469 | — | — | — |

Z1 **NO** (> dos canales sólo 5/20), Z2 OK, Z3 OK (px0 1.000 / azar 0.500 en todas las lecturas: la regla nueva no rompe lo
lineal), Z4 1/20. Curva preregistrada: sin clases XOR sin morder (n = 17) la mediana sigue en 0.500 → **la cota de
muestreo no es la causa principal**. Los marginales de P0 y P1 quedan en cero también con la regla delta con signo.

**Lectura (con el informe del investigador `registro/investigacion/xor_mecanismos_locales_20260917.md`, mecanismo 3):**
con 8–10 patrones de entrenamiento y 21–22 rasgos, la partición XOR está **indeterminada**: existen muchas soluciones que
separan lo visto usando los otros píxeles y sus productos (rasgos espurios), y ninguna regla local que sólo ve el error
puede preferir la que usa P0, P1 y P0·P1. No es la dimensión (random15), ni la puerta (3b), ni el reparto del error
(3d): es **identificabilidad**. Diagnóstico decisivo, preregistrado como 3e: darle a la vía lenta sólo {P0, P1, P0·P1, 1}
("oráculo"); si generaliza ≥ 0.80, el límite es de **selección de rasgos** (sesgo inductivo), no de la regla; si no,
la regla tampoco puede con 4 rasgos y el problema es otro. Vocabulario: *XOR sigue sin generalizarse; tres reglas y tres
lecturas refutadas; el candidato a causa es la identificabilidad, pendiente de 3e*.

### Investigación del equipo (dos informes, Sonnet), integrados como dato

- `registro/investigacion/xor_mecanismos_locales_20260917.md`: negative patterning en abejas/moscas resuelto por el cuerpo
  fungiforme vía celdas conjuntivas ("unique cue", Deisig–Lachnit–Giurfa 2001; Devaud 2015) — sugiere probar la vía
  RÁPIDA sola (`eta_s = 0`) y K = 5 en vez de 3; leaky-LMS (Widrow) da λ ≈ ln 2 / n_actualizaciones ≈ 0.0021, la misma
  banda que el trío halló a tanteo; paridad es dura para expansiones aleatorias (Bengio–Delalleau–Le Roux 2006;
  Daniely–Malach 2020): random15 = 0.50 no es accidente; currículo local por cuenta de mordidas por celda.
- `registro/investigacion/exploracion_sin_atraccion_20260917.md`: cinco mecanismos sin atracción extra; el más limpio,
  **olvido de `M` en ausencia** (`_Mset[pos] = False` si `t − t_visita > 4000`) combinado con la dosis barata de novedad
  0.6; normalización divisiva (Louie–Khaw–Glimcher 2013) como control barato; "paradoja de exposición" (confirmar que un
  sitio ya no es veneno exige acercarse, y el mapa lo impide) como límite compartido de 3 y 5. Dato de arquitectura
  subrayado: `valor()` sólo cambia al morder; pisar sin morder no toca lo aprendido.


### Bloque 2 ter (día 7, 23:10): escala del recuerdo (valor recordado saturado en la brújula del mapa) — **REFUTADA → el canje exploración/explotación del mapa se registra como ESTRUCTURAL; v14 no lleva el mapa**

Preregistro `experimentos/nivel8_escala_mapa/PREREGISTRO_escala_mapa.md` (agente diseñador; `sat_M = 1.0 = R_VAL['comida']`, fijado
antes de correr por la escala del mundo); instrumento `mundo_largo_e.py` (`d1398f0428b1739b`, perillas apagadas ≡ `mundo_largo`
3/3 con el mundo completo); datos `escala_s81-100_20260917_230039` (`05a712ef734aba56`), semillas 81–100 (las mismas de la
serie de novedad 1.8: la puerta K0 reprodujo MAPA 0.700 / comida 971 exactamente y V13 **0.8875** contra un ancla escrita
como 0.887 — el runner imprimió "NO: instrumento sospechoso" porque el ancla se transcribió de la impresión a tres
decimales del log anterior en vez del JSON de precisión completa. **Corrección (auditoría del día 7, hallazgo 1):** el
diagnóstico que quedó escrito aquí primero ("comparación de flotantes mal escrita") era erróneo; los valores son
idénticos, no hay sospecha; `corre_escala.py` lleva ahora el ancla 0.8875 (cambio posterior a la corrida, sin tocar datos;
el JSON conserva `K0_esperado = 0.887`). Lección: las anclas de reproducción se copian del JSON, nunca de un log).

| brazo | adquisición (≤ 30) | comida Q4 | visitas / equidad | celdas |
|---|---|---|---|---|
| V13 | 0.887 | 834 | 12 115 / 0.710 | 90 |
| MAPA | 0.700 | 971 | 5 064 / 0.139 | 79 |
| **MAPA + saturación [−1, +1]** | **0.716** | 973 | 5 660 / 0.212 | 84 |
| + saturación barajada por sitios (control) | 0.723 | 958 | 5 680 / 0.199 | 85 |
| + atenuación κ = 0.5 (lectura) | 0.700 | 954 | 5 998 / 0.226 | 90 |

P1 **NO** (0.716; > MAPA 11g/4e/5p), P2 OK (la comida no cae), P3 **NO** (saturación = barajada), P4 NO. **Lectura:** quitarle
al veneno recordado su peso ×3 no redistribuye las visitas (equidad 0.21 contra 0.71 de V13): la brújula sigue diciendo
"ve a la comida recordada", y el organismo acampa en los sitios de comida aunque el veneno ya no lo repela. La causa del
canje **no es la escala del veneno**: es la **atracción de la comida recordada** misma — con mapa, el organismo deja de
explorar porque ya sabe dónde comer. **Tres candidatos refutados** (curiosidad por progreso, novedad de sitio en dos
dosis, saturación): por la cláusula (a) del preregistro, **el canje se registra como estructural**: *el mapa cobra
exploración por construcción; v14 no lo lleva*. El mapa queda como órgano de experimento (nivel 6) con su canje escrito.
Vocabulario: *el mapa da de comer y quita exploración; no hay perilla que lo arregle sin quitarle el mapa*. Si algún día
se reabre, será por un mecanismo que haga que **la comida recordada deje de atraer** cuando el cuerpo no la necesita
(saciedad como temperatura de la brújula: informe de exploración, mecanismo 4 y "paradoja de exposición"), en rama.


### Bloque 3e (día 7, 23:15): oráculo de rasgos — **con los rasgos exactos {P0, P1, P0·P1, 1} la vía lenta TAMPOCO generaliza XOR (0.625) → el cuello es la DINÁMICA, no la representación, la lectura, la regla ni la identificabilidad**

Preregistro `experimentos/nivel7_xor_lectura/PREREGISTRO_xor_3e.md`; instrumento `organismo_v13q3.py` (`aaebe073308a40c2`; knobs
apagados ≡ v13q 12/12; inercia contra los datos publicados del 3d: idéntico en 3 semillas); datos `xor_3e_s61-80_20260917_231444`
(`9d1c5071fd2a97b6`), 200 corridas.

| brazo (xor01, nunca vistos) | `acc_lenta` | `Ws(P0)` | `Ws(P1)` | `Ws(P0·P1)` |
|---|---|---|---|---|
| oráculo, dos canales | 0.562 [0.50, 0.94] | +0.26 | +0.39 | −1.32 |
| oráculo, dos canales + constante | 0.625 [0.31, 1.00] | +0.19 | +0.33 | −1.23 |
| **oráculo + delta con signo + constante** | **0.625** [0.31, 0.88] | +0.05 | +0.23 | −0.91 |
| ruido (P2·P3) + delta (control) | 0.375 | +0.01 | +0.08 | (P2·P3 +0.12) |
| cuadrática + delta (referencia 3d) | 0.438 | −0.11 | +0.01 | −0.78 |

O1 **NO** (0.625 < 0.80; > ruido sólo 13/20); R1 (px0) 1.000 en todos (P0 es px0: lectura, no control). **Lectura:** con los
rasgos regalados la estructura aparece (marginales positivos, producto negativo: es la forma de XOR) pero la magnitud no
alcanza para clasificar en ~330 actualizaciones con refuerzo sólo al morder, recompensa −3/+1 y clases desigualmente
muestreadas (hasta 82 % de las mordidas de una sola clase). Serie completa de la línea XOR: 3 (dimensión: no), 3b (puerta:
no), 3d (regla: no), trío (tres mecanismos aislados: no), 3e (identificabilidad: no) → **XOR es representable y legible
pero no aprendible con la dinámica actual de muestreo y refuerzo**. Vocabulario: *XOR no se generaliza; el cuello está
en cuántas veces y con qué error se actualiza la vía lenta, no en qué ve*. La línea pasa a la célula de creación
(creador A: reglas y dinámica; creador C: aprender también sin morder, por predicción). No se corre 3f hoy.


### Bloque 6 (día 7, 23:25; RAMA, 10 semillas, no cierra nada): modelo de sí mismo mínimo — **la sorpresa no acelera la recuperación; el predictor sí mide**

Preregistro `experimentos/nivel9_allostasis/PREREGISTRO_allostasis.md` (+ enmiendas 1–2, del agente diseñador); instrumentos
`organismo_v13a.py` (`cada8cd34539d15f`) y `organismo_v13ag.py` (`c0faac23d8a56c0e`), identidades I1 (`eta_pred = 0` ≡ v13) e
I2 (`eta_pred > 0, k_sorpresa = 0` ≡ v13 **bit a bit**: el predictor no decide nada) 6/6; datos `allostasis_s1-10_20260917_231652`
(`edb069ba16367139`). Mecanismo: tercera lectura lineal `ΔE_pred(P)` (retina + código) con regla delta a `eta_pred`;
`sorpresa = |ΔE − ΔE_pred|` modula la vía rápida `eta_ef = eta·(1 + k·sorpresa)`; control RUIDO con la sorpresa barajada.

| brazo | recuperación tras la inversión (pasos) | veneno post | comida post | `eta` medio Q3 | sorpresa pre / post |
|---|---|---|---|---|---|
| V13 | 8 360 | 55.5 | 317 | 1.00 | — |
| V13 + predictor (sólo mide) | 8 360 (≡ V13) | 55.5 | 317 | 1.00 | 0.0 / 0.76 |
| **V13 + sorpresa** | **7 159** | 51.0 | 309.5 | 1.085 | 0.0 / 0.83 |
| V13 + ruido (control) | 8 317 | 52.0 | 311.5 | 1.081 | 0.0 / 0.71 |

P1 **NO** (0.856 del tiempo de V13; pareado 6/10), P2 NO (exceso de `eta` casi igual en ruido: contraste inconcluso, escrito
antes), **P3 OK** (la sorpresa es 0 en régimen y salta ≥ 0.20 justo al cambio, 10/10), P4 retención intacta (E1–E2L 10/10 en
los cuatro brazos), P5 generalización intacta (px0 0.80–0.90, azar 0.50), P6 no gana por pasividad. **Lectura:** el
predictor de la propia energía aprende exacto (error 0 en régimen) y detecta el cambio de mundo; usar esa sorpresa para
acelerar el aprendizaje **no** ayuda aquí (la recuperación la limita cuántas veces muerde, no la tasa). Vocabulario:
*el organismo predice su energía y se sorprende cuando el mundo cambia; esa sorpresa no le sirve todavía*. Queda como
instrumento para la célula de creación (significado por predicción; modelo de sí mismo). No se declara nada.


### Nivel 6, dos metas y rodeo (día 7, 23:25; semillas 41–60): **los cuatro criterios pasan, las puertas de validez del preregistro caen → no se declara; enmienda 1 y serie nueva**

Preregistro `experimentos/nivel6_rodeo/PREREGISTRO_rodeo.md` (agente diseñador; hallazgo de diseño: con tres sitios equidistantes
el rodeo es geométricamente imposible — la prueba usa sitios asimétricos g1 = 5, g2 = 20, g3 = 15 y la desigualdad de
mecanismo `0.9^d2 > 0.9^d1 − |v_B/v_A|·0.9^dp`, exigente en dp = 4: `v_B < −0.308·v_A`); instrumento `mundo_mapa_rodeo.py`
(`7ab34aed9acffaa0`; sin `modo='rodeo'` ≡ `mundo_mapa`, 27/27); datos `rodeo_s41-60_20260917_232338` (`53b0b62d68da4ffe`).

| brazo | R1 rodeo (lado largo cuando el veneno está en el corto) | R2 atajo | llega sin pisar veneno | `v_B` |
|---|---|---|---|---|
| **MAPA** | **0.700** [0.45, 1.00], pareado contra SINMAPA **19/20** | 0.775 | 0.850 | −0.74 |
| SINMAPA (= CONGELADA bit a bit) | 0.500 | 0.500 | 0.263 | −2.66 |
| INVERTIDO | 0.250 | 0.150 | 0.025 | +0.74 |

R1–R4 **pasan**. Validez: V0 (`v_B < −0.308·v_A`, mecanismo predice rodeo) sólo en **15/20** (se exigía 18): con mapa el
organismo casi no muerde veneno y `v_B` queda en −0.74 (solo: −2.66), y en 5 semillas el veneno recordado no pesa lo
bastante para que la suma descontada elija el lado largo; V1 (`M` con los 3 sitios) tampoco en todas. Por la letra del
preregistro, **no se interpreta**. Lectura honesta: donde el mecanismo predice rodeo, rodea; donde no lo predice (veneno
apenas conocido), no. **Enmienda 1 (escrita antes de la serie nueva):** semillas 61–80 con los mismos criterios y, además,
análisis preregistrado sobre el **subconjunto válido** (semillas con V0 y V1): se exigen ≥ 12 semillas válidas, R1 ≥ 0.70 en
mediana del subconjunto y pareado ≥ 75 % del subconjunto; el conjunto completo se reporta igual. Sin recalibrar nada
sobre 41–60. Vocabulario provisional: *elige entre dos comidas recordadas y se desvía por el lado largo cuando el veneno
recordado pesa; no "planifica"*.


### Nivel 6, dos metas y rodeo, serie 61–80 + análisis preregistrado del subconjunto válido (enmienda 1): **REPLICADO — elige entre dos comidas recordadas y se desvía por el lado largo cuando el veneno recordado pesa**

Datos `rodeo_s61-80_20260917_232711` (`6e64975c0c14172c`), identidad 27/27. Conjunto completo: R1 **0.750** [0.40, 0.90] (pareado
contra SINMAPA **19/20**), R2 0.700, R3 INVERTIDO 0.25, R4 llega sin pisar veneno 0.825; V0 16/20, V1 no en todas (como en 41–60).
**Análisis del subconjunto válido (escrito en la enmienda 1 antes de esta serie; V0 = el mecanismo predice rodeo,
V1 = `M` con los tres sitios):**

| serie | válidas | R1 rodeo (mediana) | pareado MAPA > SINMAPA | R2 atajo | llega limpio | R1 en las NO válidas |
|---|---|---|---|---|---|---|
| 41–60 | 14/20 | **0.725** | **14/14** | 0.750 | 0.875 | 0.600 |
| 61–80 | 16/20 | **0.750** | **16/16** | 0.700 | 0.850 | 0.800 |

Las dos series pasan la enmienda (≥ 12 válidas, R1 ≥ 0.70, pareado ≥ 75 %, R2 ≥ 0.70, llega ≥ 0.60) y también los cuatro
criterios sobre el conjunto completo. Donde el mecanismo no predice rodeo (veneno recordado débil, 4–6 semillas) el
resultado es más bajo en una serie (0.600) y alto en la otra (0.800; 4–6 semillas, sin potencia): consistente con que el rodeo lo produce la suma
descontada del valor recordado, no otra cosa (INVERTIDO 0.25 en ambas; SINMAPA = CONGELADA bit a bit 0.45–0.50).

**Declarable (nivel 6, segundo peldaño):** *con dos comidas recordadas fuera de la vista, elige la más cercana cuando el
camino está limpio y se desvía por el lado largo cuando el veneno recordado está en el corto, sin pisarlo (llega limpio
0.83–0.88), con el mismo mecanismo del mapa (suma descontada por dirección del valor recordado) y sin ningún parámetro
nuevo*. No "planifica" (un paso de simulación, sin secuencia). Diseño: agente diseñador (hallazgo: con sitios
equidistantes el rodeo es geométricamente imposible; sitios asimétricos g = 5/20/15; desigualdad `v_B < −0.308·v_A`).
Abierto: rodeo falso (veneno detrás de la comida corta: el mecanismo se desvía sin motivo) y secuencias de dos metas.


### N3d, tercera serie (semillas 101–120) con el gemelo social compilado en producción: **TRANSFIERE (0.811); tres series 0.822 / 0.811 / 0.811**

Datos `N3d_s101-120_20260917_233033` (`cc5ca17e2e4bbf21`). Etapa de identidad dentro del corredor: gemelo compilado ==
original en CONV (T = 30 000, 3 semillas) **3/3** e identidades de montaje 6/6 antes de correr. CONV **0.811** [0.76, 0.84]
(> SOLO_R 20/20; > SHUF 20/20; > SACIEDAD 20/20; N0 > SOLO_R 2/20, validez OK). SHUF 0.488, SACIEDAD 0.507, N0 0.504,
SOLO_R 0.512, TECHO 0.998. `corre_N3d.py --rapido` queda enganchado (la serie con gemelo tarda minutos, no horas).
Vocabulario sin cambio: *transfiere entre sensores por conducta*. Tres series independientes: se declara replicado ×3.


### Auditoría del día 7 (agente auditor, Sonnet; `registro/investigacion/AUDITORIA_dia7_20260917.md`): **sin hallazgos bloqueantes; dos importantes corregidos**

Revisó 3d/3e, escala del mapa, allostasis, rodeo y las réplicas con gemelos contra preregistro + instrumento + runner +
JSON/log (no la prosa). Identidades 100 % en sus JSON, anclas con conteo exacto, acierto balanceado, ningún `humo()` con
`Pool`, defensas contra las cuatro trampas implementadas de verdad, sin vocabulario inflado.
**Hallazgo 1 (importante) — K0 del bloque 2 ter:** la causa real del "NO: instrumento sospechoso" fue un ancla transcrita
a tres decimales (0.887 contra 0.8875 medido), no una comparación de flotantes; entrada corregida arriba y ancla
corregida en `corre_escala.py`. **Hallazgo 2 (importante) — rodeo:** la enmienda 1 nunca entró en `corre_rodeo.py`; el
análisis del subconjunto se hizo en línea. **Acción:** `experimentos/nivel6_rodeo/analiza_subconjunto.py` (lee los JSON,
aplica la enmienda tal cual) reproduce los números registrados: 41–60 válidas 14/20, R1 0.725, pareado 14/14, R2 0.750,
llega 0.875; 61–80 válidas 16/20, R1 0.750, pareado 16/16, R2 0.700, llega 0.850 → PASA en las dos. **Menores:** ERR-24
(control SINCOMIDA con n efectivo bajo) debilita también las dos series anteriores del mapa (1–20 y 21–40), no sólo la de
41–60 — queda anotado aquí: las dos "confirmaciones" previas de C3 no cuentan como replicación independiente de ese
control; la comparación fuerte del mapa es MAPA contra SINMAPA/CONGELADA e INVERTIDO, no contra SINCOMIDA; y las "enmiendas de subconjunto" pasan a regla estándar (`EQUIPO.md`, regla 10).


### ERR-25 (18 sep, 00:35; hallazgo colateral del creador C, verificado por el auditor en sólo lectura): **la puerta de familiaridad no distingue "no aprendido" de "cancelado"**

`organismo_v13.py:34`: la puerta manda a la vía lenta cualquier celda con `|Wp − Wn| ≤ 0.2`, sea porque nunca aprendió o
porque los dos canales subieron juntos y se cancelaron (el mecanismo de BUG-01, cerrado desde v7e/v8 por el drenaje de la
parte común, `organismo_v13.py:88`, que sigue activo). En el examen de congelación (`examen_v13_20260917_165859`, semillas
101–120) `n_techo = 0` en los seis escenarios, así que el caso literal no se disparó ahí; pero el riesgo **no se discutió
al diseñar v13** y es la misma confusión que el creador B midió por otro lado (B4: el 100 % de los estímulos que la puerta
declara desconocidos habían sido mordidos ≥ 5 veces — la puerta pregunta "¿tengo su valor sin repartir?" y no "¿lo he
visto?"). Consecuencia medida: el canje puerta contra capacidad (v13 28/35 contra v11 43/50). Propuesta B-2 (puerta por
evidencia del código exacto) lo ataca desacoplando las dos preguntas; se corre esta madrugada. **Regla derivada:** los
runners del mundo de regla y las baterías deben **guardar `n_techo`** en el JSON (hoy se calcula y no se imprime ni se
guarda: `corre_xor_3d.py`, `bateria_generaliza.py`), y todo preregistro que use la puerta declara qué pasa con las celdas
canceladas. Verificación: `registro/investigacion/AUDITORIA_dia7_20260917.md`, sección "Verificación adicional".


### Bloque B-1 (célula de creación, creador B; 18 sep 00:07): hija dispersa en 3T-k, semillas 61–80 — **REFUTADA por la letra (R1: el ahorro de celdas 16/20, se exigían 18/20); la conducta pasa y la relevancia gana a la máscara al azar**

Preregistro `experimentos/nivel7_hija_dispersa/PREREGISTRO_hija_dispersa.md` (a3c7af91453598ad, escrito antes de correr);
instrumento `mundo_hija_dispersa.py` (d305d53186fcbcd6, por anclas desde `mundo_temporal_k` 68736baafe7c8cdb; identidad
7/7 en la copia principal y 3/3 dentro del runner); datos `hija_dispersa_s61-80_20260918_000202` (dd86cdbb45041c37),
466 corridas, 4.9 min. Mecanismo: una línea del nacimiento de v11 — la hija nace ciega a parte de los píxeles de `P`
(REL: por relevancia, con medias de `P` condicionadas al signo de R; AZAR: subconjunto al azar de la misma cardinalidad;
SLOT: máscara con el slot profundo intercambiado, control de artefacto; RELD: REL + división diferida n_cf = 4).

| k = 5, C3 | `sep` mediana | `lift_q4` | divisiones | celdas | muertes | C3C (canal falso) |
|---|---|---|---|---|---|---|
| V13 | 1.87 | 0.137 | 60 | 90 | 78 | sep 0.07 |
| **REL** | **3.09** | **0.251** | **18** | **48** | 88 | 0.14 |
| RELD | 2.42 | 0.255 | 16 | 46 | 88 | 0.03 |
| AZAR | 2.02 | 0.191 | 42 | 72 | 70 | −0.00 |
| SLOT | 2.17 | 0.172 | 60 | 90 | 72 | −0.02 |

Criterios: **P1 (celdas ≤ 0.75 × V13 en ≥ 18/20) NO: 16/20** (a k = 4, ≤ 0.85 ×: también 16/20) → **R1, refutación por
la letra, sin reajustar umbrales**. P2 (lift ≥ 0.18 y > V13 en ≥ 15/20): **0.251 y 18/20 OK** (k = 4: 0.329 y 17/20).
P3 (sep ≥ 2.2 y C3 − C3C ≥ 1 en ≥ 18/20): **3.09 y 20/20 OK** (k = 4: 3.51 y 20/20). P4 inercia a k = 1: REL ≡ V13
semilla a semilla **20/20**. **R3 (REL > AZAR en ≥ 14/20): 16/20 a k = 5 y 15/20 a k = 4 → la relevancia SÍ pesa** (lo
contrario de lo que el propio creador esperaba). R4 (SLOT > REL): 4/20 y 5/20 → sin artefacto. Canal falso limpio en
los cinco brazos. Muertes: REL 88 contra 78 (no era criterio; se anota).

**Lectura honesta.** El mecanismo mejora la composición a k = 4 y k = 5 (18/20 pareado), separa mejor, gana al control al
azar y al del slot equivocado, y usa la mitad de las celdas en la mediana — pero la predicción numérica del ahorro (18/20)
no se cumplió (16/20) y la cláusula R1 la escribió el creador como refutación entera. Se registra REFUTADA tal como
estaba escrita. **Enmienda 1 (escrita ahora, ANTES de la serie nueva, criterio nuevo en semillas nuevas, sin tocar 61–80):**
serie 81–100 con los mismos brazos y umbrales, salvo P1 que pasa a **≥ 14/20** (mayoría, derivado de lo visto en 61–80 y
declarado como tal); si P1–P3 y R3 se repiten en 81–100, el vocabulario permitido es el preregistrado: *"la hija que nace
ciega a lo irrelevante compone historias más profundas con menos celdas"*; si P1 vuelve a caer, el mecanismo queda como
*"compone mejor; el ahorro de celdas es mayoritario, no general"*. Nada toca el tronco (§6 del preregistro: baterías
antes). Vocabulario prohibido sigue: "aprende a ignorar", "atiende", "selecciona".


### Bloque A-2 (célula de creación, creador A; 18 sep 00:09): metaplasticidad por masa de conflicto en el mundo largo, semillas 41–60 — **REFUTADA (la retención de lo ausente no se mueve: 0.667 = base; recupera más lento y muere más)**

Preregistro `experimentos/nivel8_metaplasticidad/PREREGISTRO_metaplasticidad.md` (1b528822724bf553, escrito antes de correr);
instrumento `experimentos/creacion_A/mundo_largo_A.py` (a3ded739a46b1c97, por anclas desde `mundo_largo` 9f74ff6b5941e5a5;
identidad 9/9 del creador y 3/3 dentro del runner, 29 claves); datos `metaplasticidad_s41-60_20260918_000740`
(6f9b82ae2f300ad9), 60 corridas, 1.5 min. Mecanismo: `g_c = 1/(1 + beta_m·m_c)` sobre la tasa de la vía rápida, con
`m_c = min(Wp, Wn)` (la masa de conflicto que el tronco ya tiene; memoria nueva cero).

| brazo | `ret_no_inv` | `ret_inv` | `adq_final` | `rec` | muertes | celdas / divisiones |
|---|---|---|---|---|---|---|
| BASE | 0.667 | 0.250 | 0.800 | 2 500 | 30 | 90 / 60 |
| B10 | 0.667 | 0.250 | 0.800 | 4 000 | 37 | 90 / 60 |
| **B50** | **0.667** | 0.250 | 0.800 | **4 000** | **52** | 90 / 60 |

P1 **NO** (mediana 0.667 < 0.80; pareado > BASE 7/20), P2 OK (adquisición intacta), P3 **NO** (recupera más lento),
P4 OK (B10 ≈ BASE), **C1 NO** (muertes +73 %, límite +50 %: el mecanismo cobra supervivencia), C2 OK. La mini-prueba de
3 semillas (0.833) no replica en 20. **Lectura:** volver lentas las celdas con evidencia contradictoria no protege lo
ausente aquí — `m` tiene semivida ≈ 14 mordidas y vale 0.02–0.05 de media (lo dijo el propio creador y lo confirmó el
explorador con la cascada de Fusi: hacen falta ≥ 2 constantes de tiempo propias, no una prótesis con β grande). Queda
refutado el mecanismo con estado existente; una variable lenta nueva sería otra propuesta (con su memoria declarada).
Vocabulario: *la masa de conflicto no sirve como freno de olvido*. Nada toca el tronco.


### Paquetes A-1 y A-3 del creador A (18 sep 00:25): instrumento de selección por competencia listo con identidad; **3f NO se corre todavía** (la selección online no abre el conjuntivo correcto); vector único listo para correr

- **A-1.** `experimentos/creacion_A/organismo_v13q4.py` (3cc732dd2b2519cd; por anclas desde `organismo_v13q3` aaebe073308a40c2,
  constructor `construye_v13q4.py` c6faffcd21eaaf47): perilla `seleccion='wta'` — elementales siempre plásticos, cada conjuntivo
  lleva un escalar `e_i` (correlación con el residuo) y un bit; se abre uno solo si `|e_i| > sel_theta`; la vía lenta
  aprende sólo en lo abierto. **Identidad `seleccion=None` ≡ v13q3: 16/16** (8 escenarios × 2 semillas, 38 claves).
  **Mini-prueba** (xor01, cuadrática, constante, delta con signo, `clip_s = 10`, T = 200 000, s1–3): sin selección 0.500;
  COND **0.625** (abre `P0·P1` 1/3); COV 0.438 (abre 2/3); reajustar los elementales al abrir (γ ∈ {1, 0.5, 0.25, 0}) da
  0.625 en los cuatro; px0 1.000/1.000/1.000, azar 0.500. **Decisión del coordinador (PLAN, orden de la madrugada, punto 4):
  3f no se corre** hasta que exista la pieza (i) — aprender también sin morder (frente del creador C; A lo dimensiona:
  5 740 encuentros con veneno `00` por corrida donde hoy no se aprende nada). Borrador `PREREGISTRO_xor_3f.md` guardado
  (7 brazos × 3 reglas × 20 semillas; techo de muestreo 0.75 escrito como resultado posible). Errata corregida por el
  propio creador en su banco: la tabla A2 decía "6 px + constante" y era "6 px + `P0·P1` dado"; con el rasgo correcto
  abierto la regla delta online alcanza residuo 0.000 y acierto 1.000 con η = 0.015 → **el ajuste no es cuello; lo son la
  selección y el muestreo**.
- **A-3.** `corre_vector_unico.py` (ee25f9ce9c3193b6) + `PREREGISTRO_vector_unico.md`: brazos DOS_CANALES (v13q3) y
  VECTOR_UNICO (`regla_lenta='delta_signo'`, `lam_lenta = 0`), semillas 101–120, montaje y umbrales de `bateria_generaliza`
  sin tocar (px0, azar) + xor01; predicción: `acc` idéntica semilla a semilla y `|ΔW_lenta| < 1e−9` mientras ningún canal
  toque `clip_s`; guarda `n_techo` (regla de ERR-25). Humo `vector_unico_humo_20260918_000816` (0689e674666bbdfa): acc
  idéntica 3/3, `max|ΔW_lenta| = 1.1e−15`, `n_techo = 0` en 6/6. Se corre después de la réplica de B-1.


### Bloque B-1, réplica 81–100 bajo la enmienda 1 (18 sep 00:15): **PASA — y pasa también por la letra ORIGINAL (P1 19/20 a k = 5, 18/20 a k = 4)**

Datos `hija_dispersa_s81-100_20260918_000954` (bdc705609bac2633), 466 corridas, identidad 3/3 dentro del runner.

| k | brazo | `sep` mediana | `lift_q4` | divisiones | celdas | muertes |
|---|---|---|---|---|---|---|
| 5 | V13 | 1.85 | 0.128 | 60 | 90 | 79 |
| 5 | **REL** | **3.62** | **0.352** | **8** | **38** | 102 |
| 5 | RELD | 3.40 | 0.358 | 10 | 40 | 94 |
| 5 | AZAR | 2.16 | 0.201 | 40 | 70 | 72 |
| 5 | SLOT | 2.12 | 0.205 | 58 | 88 | 72 |
| 4 | V13 | 2.11 | 0.135 | 45 | 75 | 86 |
| 4 | **REL** | **3.10** | **0.314** | **13** | **43** | 92 |
| 4 | AZAR | 2.35 | 0.205 | 32 | 62 | 76 |
| 4 | SLOT | 2.30 | 0.217 | 32 | 62 | 81 |

P1 celdas ≤ 0.75 × V13: **19/20** a k = 5 (≤ 0.85 ×: **18/20** a k = 4) — cumple P1' (≥ 14) **y** el umbral original (≥ 18).
P2 lift 0.352 y > V13 **19/20**. P3 sep 3.62 y C3 − C3C ≥ 1 en **20/20**. P4 inercia a k = 1: **20/20**. R3 REL > AZAR
**16/20** (k = 4: 14/20). R4 SLOT > REL 4/20 (k = 4: 6/20). Canal falso limpio. Muertes REL 102 contra 79 (se anota; no es
criterio). **Dos series:** conducta > V13 en 18/20 y 19/20; relevancia > azar en 16/20 y 16/20; ahorro de celdas 16/20 y
19/20; inercia 20/20 y 20/20.

**Declarable (nivel 7, vocabulario preregistrado):** *la hija que nace ciega a lo irrelevante compone historias más
profundas con menos celdas* — a k = 4 y k = 5 compone mejor que v13 (lift 0.31–0.35 contra 0.13; separación 3.1–3.6
contra 1.9–2.1) con **la mitad de las celdas y una décima parte de las divisiones**, y qué píxeles conserva **sí** importa
(gana a la máscara al azar de la misma cardinalidad en 16/20 dos veces; el slot equivocado no gana). Mecanismo: una línea
del nacimiento de v11 (`rel ⊊ (P > 0)` por medias de `P` condicionadas al signo de R; memoria: dos vectores `NIN` y dos
escalares por celda). Prohibido: "aprende a ignorar", "atiende", "selecciona". **Antes de tocar el tronco (§6 del
preregistro):** `bateria_v13.py` 8/8 y `bateria_generaliza.py` G1 ≥ 0.80 / G2 ≥ 0.85 sobre un `organismo_v13` con la misma
perilla (copia por anclas, identidad con la perilla apagada); la decisión de v14 es del director. Convergencia con B1/A5:
el techo de la composición no era el pool de celdas (duplicarlo no devuelve nada) sino la evidencia por código; la hija
dispersa cierra el conflicto de la madre con una sola hija por familia de rellenos.


### Bloque C-P1 (célula de creación, creador C; 18 sep 00:28): "probar cuando no me reconozco" — la sorpresa sobre la propia acción entra en la boca, semillas 41–60 — **ACELERA LA RECUPERACIÓN 0.26× (20/20) y los controles de cantidad y de momento no; retención y generalización intactas; el sesgo no se apaga del todo (P4 15/20, se exigían 16/20) → réplica antes de declarar**

Preregistro `experimentos/nivel9_probar_si_mismo/PREREGISTRO_probar_si_mismo.md` (escrito antes de correr); instrumentos
`organismo_v13p.py` (0dbc2495efe44e60; linaje v13 cc8b16b492d4d324 → `creacion_C/organismo_v13s` 2eaba8dde27f05bd → v13p, por
anclas) y `organismo_v13pg.py` (7ab4767d446ba797, mundo de regla); identidades J1–J4 18/18, 18/18, 18/18, 6/6 en la copia
principal y 11/11 dentro del runner; datos `probar_si_mismo_s41-60_20260918_001756` (69651ffff5ea2abd), 120 corridas +
baterías, 9.7 min. Mecanismo: una lectura logística por encuentro predice la propia acción (98 escalares + un escalar de
estado `s̄_a`, EMA 0.05); `Vb += k_test·s̄_a` — la sorpresa sobre sí mismo decide **si prueba**, no la tasa de aprendizaje.

| brazo | recuperación tras la inversión (pasos) | sesgo de boca por cuarto | veneno post | comida post | muertes post |
|---|---|---|---|---|---|
| V13 | 7 931 | 0 / 0 / 0 / 0 | 54.5 | 328 | 271 |
| **SELF-TEST** | **2 089** (0.263×; pareado **20/20**) | 0.29 / 0.07 / 0.31 / 0.07 | 159.5 | 441.5 | 295.5 |
| CONST-a (sesgo fijo 0.173) | 6 364 | 0.17 × 4 | 68 | 343 | 265.5 |
| CONST-b (sesgo fijo 0.31) | 6 720 | 0.31 × 4 | 82.5 | 354 | 264.5 |
| MOMENTO (misma traza rotada un cuarto) | 8 417 | 0.06 / 0.32 / 0.07 / 0.30 | 175.5 | 454 | 295.5 |
| dE-TEST (sorpresa de ΔE en la boca; exploratorio) | **1 136** | 0.10 / 0.00 / 0.13 / 0.00 | 62.5 | 350.5 | 271.5 |

P1 **OK** (0.263 ≤ 0.60; 20/20). P2 no es la cantidad **OK** (< CONST-a 19/20, < CONST-b 20/20; CONST-b iguala el sesgo de
Q3: razón 1.011, control limpio). P3 es el momento **OK** (< MOMENTO 20/20; masa de la traza idéntica, G-d 0.0). **P4 NO:
se apaga solo en 15/20** (Q2/Q4 ≤ 0.10 y Q3 ≥ 0.20; se exigían 16/20): el lazo sorpresa → morder → sorpresa deja un suelo
(Q2/Q4 ≈ 0.07). P5 retención **20/20 en las seis etapas** (V13, SELF-TEST, CONST-b). P6 generalización **OK** (px0 G1 0.80
= V13, G2 0.854; azar 0.50). P7 probar no es envenenarse **OK** (veneno post 159.5 ≤ 4 × 54.5; muertes 295.5 ≤ 1.5 × 271).
Exploratorio, sin criterio: **la sorpresa del mundo (ΔE) en la boca recupera aún más rápido (1 136) con un sesgo tres
veces menor y que sí se apaga** — el bloque 6 la había puesto en `eta` y no servía: lo que importa es DÓNDE entra.

**Lectura honesta.** Es el primer mecanismo de la noche que gana con todos los controles de fondo (cantidad, momento,
retención, generalización, seguridad) en 20 semillas; cae por una semilla en el criterio de apagado. No se declara órgano:
**enmienda 1** (escrita ahora, antes de la serie nueva): réplica 61–80 con los mismos criterios (P4 sigue en 16/20) y
**dE-TEST promovido a brazo con criterio**: P1' recuperación ≤ 0.60 × V13 y pareado ≥ 14/20, P7' igual que P7, calculado
con un script sobre el JSON (regla 10). Vocabulario provisional (del preregistro): *cuando no se reconoce, prueba; y por
eso se recupera antes de un cambio no avisado del mundo*. Prohibido: "curiosidad", "conciencia", "se conoce".


### Bloque A-3 (célula de creación, creador A; 18 sep 00:36): la vía lenta de dos canales ES un vector con signo — **CONFIRMADO con identidad numérica (60/60 corridas, |ΔW| 3.3e−15)**

Preregistro `experimentos/creacion_A/PREREGISTRO_vector_unico.md` (81a8919252313b73); runner `corre_vector_unico.py`
(ee25f9ce9c3193b6); instrumento `organismo_v13q3` (aaebe073308a40c2; identidad v13q3 dos canales lineal ≡ v13q 6/6 dentro
del runner); datos `vector_unico_s101-120_20260918_003352` (b9b82486b2224480), 120 corridas (2 brazos × 3 reglas × 20
semillas, T = 200 000). Álgebra (A3 del puente): `(Wp, Wn) ↔ (W = Wp − Wn, m = min(Wp, Wn))` es biyección; el drenaje `lam`
sólo olvida `m`; mientras ningún canal toque `clip_s`, la regla delta con signo sobre un solo vector es la misma
función.

| brazo | G1 px0 / azar | px0 > azar | G2 px0 / azar | K |
|---|---|---|---|---|
| DOS_CANALES (v13) | 0.800 / 0.500 | 18/20 | 0.892 / 0.458 (20/20) | 20/20 |
| VECTOR_UNICO | 0.800 / 0.500 | 18/20 | 0.892 / 0.458 (20/20) | 20/20 |

A1 `acc` idéntica semilla a semilla **60/60**; A2 `max|ΔW_lenta| = 3.3e−15`; A3 el tope nunca aprieta en la vía lenta (máximo
por canal 2.81 < 3.0; masa de conflicto máxima 0.34); A4 `n_techo` (vía rápida) = 0 en todas (regla de ERR-25: ya se
guarda). **Consecuencias:** (1) la vía lenta puede llevar **la mitad de memoria** (un número por rasgo) sin cambiar ni un
bit de conducta — simplificación candidata para v14 (decisión del director; no es capacidad nueva); (2) queda demostrada
la ablación del Agente B del puente XOR (`lam_lenta = 0` y `clip_s = 10` no movían nada: identidad, no casualidad);
(3) la vía RÁPIDA no admite la misma simplificación: la fisión de v11 lee `m`. Vocabulario: *la vía lenta es un vector con
signo; el drenaje es el olvido de la evidencia contradictoria*.


### Bloque C-P1, réplica 61–80 con la enmienda 1 (18 sep 00:44): **REPLICADO — SELF-TEST acelera 0.22× (20/20) con todos los controles; P4 vuelve a caer (15/20); dE-TEST ("la sorpresa del mundo en la boca") pasa P1', P4' y P7' en las DOS series → candidato por derecho propio**

Datos `probar_si_mismo_s61-80_20260918_003640` (6eedf29fc48ac580), 120 corridas + baterías; identidades 11/11.

| brazo | recuperación (pasos) | sesgo Q3 | veneno post | muertes | 41–60 (para comparar) |
|---|---|---|---|---|---|
| V13 | 7 969 | 0 | 56 | 265 | 7 931 |
| **SELF-TEST** | **1 761** (0.221×; pareado 20/20) | 0.27 | 147 | 303.5 | 2 089 (0.263×) |
| CONST-a / CONST-b | 6 278 / 5 697 | 0.17 / 0.31 | 71.5 / 86 | 268.5 / 258.5 | 6 364 / 6 720 |
| MOMENTO | 9 305 | 0.08 (rotado) | 198 | 285 | 8 417 |
| **dE-TEST** | **1 152** (0.144×; pareado 20/20) | 0.13 | 66.5 | 284 | 1 136 (0.143×) |

SELF-TEST: P1 OK, P2 OK (20/20 y 20/20), P3 OK (20/20), **P4 NO (15/20 por segunda vez)**, P5 retención 20/20 × 6, P6 px0 G1 0.80
(V13 0.85), azar 0.40, P7 OK. **dE-TEST con los criterios de la enmienda 1 (`analiza_dE.py`, forma relativa de P4'):**
41–60 P1' 0.143× y 20/20, P4' se apaga **20/20**, P7' OK; 61–80 P1' 0.144× y 20/20, P4' **20/20**, P7' OK.

**Declarable (vocabulario de la enmienda):** SELF-TEST → *cuando no se reconoce, prueba, y se recupera antes de un cambio no
avisado del mundo; el impulso de probar no se apaga del todo* (límite medido: el suelo es la cota de oráculo de su propia
política, C7 del puente). dE-TEST → *la sorpresa del mundo puesta en la boca* recupera 7× más rápido que v13, con un sesgo
tres veces menor que se apaga solo y sin más veneno ni más muertes: **candidato a órgano**. Lo que falta antes de
proponerlo al director para v14: retención y generalización medidas en dE-TEST (las baterías corrieron sólo para V13,
SELF-TEST y CONST-b) — serie 81–100 (enmienda 2, en preparación por el creador C) con `--baterias` para dE-TEST, la variante
`resta_cota` del automodelo (P4′) y la prueba de latencia. Hallazgo de la línea: **el predictor de ΔE del bloque 6 nunca fue el
problema; lo era dónde entraba** (en `eta`: 0.856×, refutado; en la boca: 0.14×).


### Auditoría de la madrugada del 18 (agente auditor, Sonnet; `registro/investigacion/AUDITORIA_madrugada18_20260918.md`): **sin bloqueantes; dos ERR numerados a posteriori (regla 4) y una rebaja de vocabulario**

Identidades 100 % en los cuatro JSON, ningún humo con `Pool`, fuga de identidad J2 limpia en código y en datos, ERR-25
transcrito con exactitud. **ERR-26 (B-1, enmienda 1):** la enmienda que bajó P1 a ≥ 14/20 no es un análisis de subconjunto
(regla 10) sino una rebaja lisa del umbral de aprobación escrita entre dos series; fue inerte (81–100 pasó el umbral
original, 19/20) y nunca se implementó en el runner (`corre_hija_dispersa.py:163` sigue en 18), pero **cambió un criterio
sin ERR numerado**. Queda numerada aquí; la declaración de B-1 se apoya en la letra original en 81–100 y en la conducta en
las dos series. **ERR-27 (C-P1, adenda a la enmienda 1):** la forma relativa de P4' se decidió al ver, con `analiza_dE.py`,
que la copia literal de P4 fallaba sobre los datos ya corridos de 41–60 — transparente y motivado (el criterio literal no
podía medir el apagado de un sesgo pequeño por construcción), pero es un criterio escrito mirando datos de esa misma
serie. **Consecuencia:** para dE-TEST valen como prueba limpia los criterios P1' y P7' en las dos series y P4' sólo en
61–80 (20/20); 41–60 se reporta como retroactivo. **Vocabulario rebajado:** dE-TEST es *candidato pendiente de baterías*
(retención y generalización no medidas: M5/M6 corrieron sólo para V13, SELF-TEST y CONST-b), no "candidato a órgano".
Menores: la guarda G-b etiqueta a MOMENTO como "inconcluso" por comparar sólo Q3 cuando el control desplaza el pico a Q4
por diseño (la cantidad total la certifica G-d, limpia); el criterio A1 de A-3 es casi tautológico una vez que A3 (el
tope nunca aprieta) se cumple — A-3 vale como identidad demostrada, no como prueba empírica independiente. **Regla
derivada (se añade a EQUIPO.md, regla 4 bis):** toda enmienda que cambie un umbral o la forma de un criterio lleva ERR
numerado en el momento de escribirla, aunque sea antes de la serie nueva.


### Nivel 6 en 2D (diseñador; 18 sep 01:30; semillas 21–40): **no rodea, se aleja (refutación en la forma predicha); el rodeo falso queda confirmado y cuantificado; encadena dos metas mejor si borra el sitio comido; horizonte 2 sin potencia**

Preregistro `experimentos/nivel6_2d/PREREGISTRO_2d.md` (+ enmienda 0 del coordinador, P3b pareado, escrita antes de correr);
instrumento `mundo_2d.py` (24da4ab1644eb92a; por anclas desde `mundo_mapa_rodeo` 7ab34aed9acffaa0 ← `mundo_mapa`
207d6a1954336b18; **identidad 60/60 en la copia principal**: `alto = 1` ≡ mundo_mapa 36/36, modo rodeo 9/9, perillas apagadas
≡ v13 9/9, perilla barajar apagada ≡ ausente 6/6; 8/8 dentro del runner); datos `2d_s21-40_20260918_010836`
(94a82d9e25a66e57), 480 corridas (4 mundos × 6 brazos × 20 semillas, T = 100 000), 20 min. Rejilla toroidal 17 × 13, 4
direcciones, retina del objeto más cercano en distancia Manhattan, tabla `M` en 2D, el organismo sin cambios.

| prueba | MAPA | SINMAPA (= CONGELADA en conducta) | INVERTIDO | lectura |
|---|---|---|---|---|
| T1 rodeo verdadero, `R1` (primer paso por el camino limpio) | **0.000** (pareado 0/20) | 0.525 | 1.000 | se aleja 1.000; distingue el flanco barato 1.000 |
| T4 rodeo falso, `R4` (comida con veneno detrás frente a comida limpia) | **0.05** | 0.24 | 0.58 | indiferente sería 0.50: **se desvía sin motivo** |
| T3 secuencia, `come2` (alcanza A y luego B) | 0.500 (MAPA) / **0.950** (MAPA_borra) | 0.225 | 0.000 | P3b dif ≥ 0.15 en **18/20**; llega_A 1.00 |
| T2 horizonte 2, `R2` | 0.575 (H1) / 0.875 (H2) | 0.26 | 0.000 | ventana V-T2 **6/20** (se exigían 8): sin potencia; en las 6, H2 − H1 = +0.475 (6/6) |

**C1 INVERTIDO decisivo OK** (T1b 0.000, R4 1.000: con el valor del revés va hacia el veneno), **C2 OK** (CONGELADA ≡
SINMAPA en conducta, `M_llenas` = 0), C3 BARAJADO se reporta (0.31–0.54). Validez: V2, V3, V4 OK; **V1 cae en T2 (5/20 sin
un sitio en `M`) y T4 (2/20)** → por la letra el bloque "no se interpreta"; **regla 10** (análisis automático del
subconjunto válido con los umbrales originales, `analiza_2d.py`): T1 20/20 válidas, T3 20/20, T4 18/18 → R4 0.062,
T2 15/15 → mismas medianas; nada cambia.

**Lecturas (vocabulario del preregistro):** (1) *con el veneno recordado entre él y la comida no rodea: se aleja; el
mecanismo distingue el flanco barato y no lo usa* — en 2D el sesgo de `M` es un voto global y el veneno no repele el
camino, repele el acercamiento. Es la refutación predicha por el diseñador; ahora está medida. (2) **Rodeo falso
confirmado**: con dos comidas limpias a la misma distancia elige en 0.05 la que tiene veneno detrás (indiferente = 0.50):
*se desvía sin motivo*. (3) *Borrar el sitio comido de la tabla ayuda a encadenar dos metas (0.95 contra 0.50); sin
borrarlo vuelve al sitio vacío la mitad de las veces* (P3 por la letra cae en el umbral de MAPA ≤ 0.20; P3b pasa 18/20).
(4) Horizonte 2: sin potencia (6/20 en la ventana); lo que hay (6/6 a favor, +0.475) coincide con lo predicho y pide un
mundo con más semillas dentro de la ventana antes de decir nada. **No se corre réplica ahora**: los resultados de T1 y T4
son 0/20 y 0/18 (no hay ambigüedad que replicar); T2 necesita rediseño del mundo (declarado). Nivel 6 queda así: *el
mecanismo actual del mapa elige direcciones por valor recordado descontado; no planifica en 2D, y en 2D esa carencia se
ve* — la planificación real exige otro mecanismo (simular con `M`, H2, mostró +0.475 donde discrimina).


### ERR-28 (18 sep 01:15; aviso del creador B, verificado por el auditor): **trampa latente — `experimentos/v13_dos_vias/organismo_v13.py` (88c3574cf9cf38bf) no es el tronco (cc8b16b492d4d324)**

Diff real: docstring y dos valores por defecto (`eta_s` 0.015 → 0.0, `puerta` 3 → None). Empírico (scratchpad, 3 semillas):
con los kwargs por defecto **difieren** en valor y conducta; con `eta_s`/`puerta` explícitos son idénticos 3/3. De los 24
sitios que importan `organismo_v13` a secas, ninguno tiene esa carpeta delante de `organismo/`; los que sí la anteponen
(XOR, N3*, `bateria_generaliza*`) nunca importan ese nombre ambiguo; en `datos/` el sha de la copia sólo aparece en la
corrida histórica que congeló v13, cuyo runner pasa `eta_s`/`puerta` explícitos. **Sin consecuencia medida en 70+
archivos.** Al creador B le costó un humo (identidad 3/6) hasta poner `organismo/` primero. **Regla derivada:** todo runner
pone `organismo/` primero en `sys.path`; nunca se importa `organismo_v13` a secas con `experimentos/v13_dos_vias` delante;
la copia histórica no se edita (documenta la congelación) pero queda señalada aquí.


### v13D — la hija dispersa en la copia del tronco: **NO REGRESIONA** (examen v3' 8/8 en 101–120, generalización G1 0.80 / G2 0.83, inercia total en la retina de 6 px) → **candidata a v14; la decisión es del director**

Preregistro `experimentos/nivel7_hija_dispersa/PREREGISTRO_v13D.md` (b476d4ce8dbe8a04; prueba de NO regresión: en una retina de
6 px con un solo objeto no hay nada irrelevante que ignorar, se predijo máscara inerte); instrumentos por anclas desde el
tronco congelado: `organismo_v13D.py` (dd380dada0b72bac; perilla apagada ≡ v13, **identidad 16/16** en la copia principal),
`organismo_v13Don.py` (1dd131dc0298307d, perilla fija ON), `organismo_v13gD.py`, `bateria_v13D.py` y `bateria_generaliza_D.py`
(seis etapas, CRIT, G1/G2/K intactos); datos `baterias_v13D_20260918_012145` (cd35bca589962fcb), 5.2 min.

| prueba (perilla ENCENDIDA) | resultado |
|---|---|
| D3 inercia (3 escenarios × 20 semillas) | divisiones 0 → 0, celdas 30 → 30, `W` idéntico 20/20 |
| D1 retención, examen v3' completo (101–120) | E1, E2, E2I, E2J, E2K, E2L **20/20**; celdas ≤ 45; 3' 0/20 (≤ 1); 3'' **20/20**; 4a–4d OK → **8/8** |
| D2 generalización | K 20/20; G1 px0 **0.800** (azar 0.500; 19/20); G2 px0 **0.834** (azar 0.427; 19/20) — con la perilla apagada 0.800 / 0.892 |

**Lectura:** la hija dispersa no daña nada del tronco donde no hay nada que ignorar (inerte por construcción, D3) y compone
historias más profundas con la mitad de celdas donde sí lo hay (B-1, dos series). Cumple lo que el método exige para un
órgano: mecanismo de una línea con memoria declarada (dos vectores `NIN` y dos escalares por celda), preregistrado,
replicado, controles de cantidad/forma (máscara al azar, slot equivocado), inercia, examen v3' y batería de
generalización intactos. **Propuesta de v14 en `registro/PROPUESTA_v14.md` y rama `v14-candidato`** (copia, no toca `main`
ni el tronco congelado). Faltan, si el director la acepta: gemelo compilado con arnés, congelación (manifiesto), tag.


### Bloque C-P1, serie 3 (81–100) con la enmienda 2 (18 sep 01:48): **SELF-TEST pasa TODO, incluido el apagado (P4 17/20); dE-TEST pasa sus baterías (retención ≥ 19/20 × 6, G1 0.90) → "la sorpresa del mundo en la boca" es CANDIDATO A ÓRGANO con tres series; las variantes del automodelo (restar la cota, línea base lenta) quedan refutadas como el creador predijo**

Datos `probar_si_mismo_s81-100_20260918_012715` (207c83061567ba45), 160 corridas + baterías para V13, SELF-TEST y dE-TEST;
identidades J1–J6 (18/18 × 5, 6/6) en la copia principal y 11/11 dentro del runner.

| brazo | recuperación | sesgo Q3 · razón Q2/Q3 | latencia del primer sesgo | veneno post | muertes | retención (6 etapas) | G1 px0 / G2 |
|---|---|---|---|---|---|---|---|
| V13 | 7 578 | 0 | — | 57.5 | 275 | 20/20 × 6 | 0.90 / 0.92 |
| **SELF-TEST** | **2 492** (0.329×; 20/20) | 0.25 · 0.21 | 602 pasos (1.5 bocados) | 126.5 | 294.5 | 20/20 × 6 | 0.90 / 0.84 |
| CONST-a / CONST-b | 6 589 / 5 178 | 0.17 / 0.31 · 1.0 | 8–10 | 71.5 / 87 | 270 / 263.5 | — | — |
| MOMENTO | 7 836 | 0.07 · 3.9 | 614 | 150.5 | 293.5 | — | — |
| **dE-TEST** | **1 071** (0.141×; 20/20) | 0.13 · **0.001** | **202 pasos (1 bocado)** | 62.5 | 280.5 | **20, 19, 20, 20, 20, 20** | **0.90 / 0.85** |
| SELF-TEST-R (resta la cota) | 3 210 | 0.05 · 0.40 | 1 041 | 62 | 276.5 | — | — |
| SELF-TEST-L (línea base lenta) | 3 617 | 0.08 · 0.29 | 1 604 | 73 | 294.5 | — | — |

SELF-TEST: P1 OK, P2 OK (19/20, 19/20), P3 OK (20/20), **P4 OK (17/20)**, P5 OK, P6 OK, P7 OK. **Tres series:** P1 0.26× /
0.22× / 0.33× (20/20 × 3); P2–P3 y P5–P7 en las tres; P4 15, 15, 17 de 20. dE-TEST (`analiza_dE.py`): P1' 0.141× 20/20, P4'
20/20, P7' OK — **tres series** (0.143× / 0.144× / 0.141×; apagado 20/20 × 3; seguridad × 3) y **Q1' (enmienda 2) OK:
retención ≥ 18/20 en las seis etapas y px0 ≥ 0.80**. Q2' (variantes): refutadas como estaba predicho (recuperan peor y no
apagan mejor). Q3' (latencia): dE-TEST arranca en 202 pasos con un bocado; el automodelo tarda 602 y 1.5 bocados — la
ventaja de densidad del automodelo no se cobra (el error de ΔE salta 1.2 en un solo bocado).

**Declarable (vocabulario del preregistro y enmiendas):** (1) *cuando no se reconoce, prueba, y por eso se recupera antes de un
cambio no avisado del mundo* — tres series, todos los controles; el apagado pasa en la tercera y queda 15–17/20 (límite
conocido: la cota de oráculo de su propia política). (2) **"La sorpresa del mundo puesta en la boca"** (el predictor de ΔE
del bloque 6 decidiendo si prueba, `k_testE = 10`): recupera **7× más rápido que v13** (0.14× en tres series, 20/20 × 3),
sesgo tres veces menor que se apaga solo, sin más veneno ni muertes, y **no cobra retención ni generalización** → **candidato
a órgano** (`registro/PROPUESTA_v14.md`, segundo candidato). Falta, si el director lo quiere en v14: el examen v3' completo
(3', 3'', 4a–4d) sobre una copia del tronco con la perilla fija (como se hizo con v13D), gemelo y congelación. Lección de
la línea: *el predictor de ΔE nunca fue el problema; lo era dónde entraba*.


### ERR-29 (18 sep 02:05; hallazgo del implementador del paquete v13E): **`corre_baterias_v13D.py` guardaba la generalización ON y la referencia OFF bajo la misma clave** — el veredicto registrado no cambia

La corrida OFF (posterior) pisó en el JSON la entrada de la corrida ON antes de leerla; el veredicto `D2_generalizacion = True`
se mantiene porque **las dos pasan** y los números ON están en el log registrado (`baterias_v13D_20260918_012145.log`:
K 20/20, G1 px0 0.800 / azar 0.500, 19/20; G2 0.834 / 0.427, 19/20). Corrección: claves explícitas `D2` / `D2_ref` en el runner
(sin volver a correr). Lección (regla 9 de los runners): cada etapa escribe bajo una clave propia; el veredicto se lee del
JSON, no del recuerdo del proceso.

### ERR-30 — examen v3' y órganos que actúan en la boca (02:05): **el criterio 5 (identidad: reducción a v11 apagando `eta_s` y `puerta`) no puede medir a v13E** → criterio 5 adaptado (v3'' para órganos en la boca), declarado antes de correr

En el humo de `bateria_v13E` (2 semillas) el criterio 5 dio 0/84 y el examen abortó por su guarda: `k_testE·s̄_E` entra en la boca
sin pasar por `eta_s` ni `puerta`, así que apagar esas dos perillas no reduce v13E a v11. Precedente ERR-21 → v3': el criterio
se reescribe (la reducción a v11 apaga también la perilla nueva), se justifica en `PREREGISTRO_v13E.md` y el examen entero
se corre en semillas nuevas; si con las tres perillas apagadas v13E no es v11 bit a bit, el instrumento está mal y no se
interpreta nada. Se anota aquí antes de correr el examen.


### Bloque B-2 (célula de creación, creador B; 18 sep 02:32): puerta de familiaridad por evidencia del código exacto, semillas 41–60 — **recupera la capacidad en el paso largo (PATC `N*` 50.5 = v11, contra 35 de v13) con la generalización INTACTA (px0 1.000 / 0.96); en el paso corto mejora sin cruzar el umbral (41.5 contra 28; se exigía 45); el examen de retención cae por UNA semilla en E2 (19/20) → no entra al tronco tal como está**

Preregistro `experimentos/nivel4_puerta_codigo/PREREGISTRO_puerta_codigo.md` (+ enmienda 1 escrita tras el humo y antes de
la serie: brazo **PATC** = evidencia del código **y** ≥ 1 celda consolidada, porque la puerta de v13 también detecta
conflicto y contar mordidas del código pierde el criterio 3''); instrumentos por anclas desde el tronco y los congelados:
`organismo_v13B` (59075fa17f034112), `organismo_v13gB`, `organismo_capB` (desde `organismo_capD13`), `bateria_v13B/Bc`,
`bateria_generaliza_B`; **identidad 21/21** en la copia principal y 6/6 (inercia) dentro del runner; datos
`puerta_codigo_s41-60_20260918_013618` (d6fa9e0c7bec62cf), 200 corridas largas + 4 baterías, 56 min. Montaje exacto de
`reverificacion_v13` (D = 10, 60 estímulos, pasos 20 000 y 60 000, semillas 41–60).

| paso | v11 | v13 | PAT (código, n0 = 5) | **PATC** (código ∧ 1 celda) | PATSHUF (contadores barajados) |
|---|---|---|---|---|---|
| 60 000: `N*` mediana | 50.0 | 35.0 | 49.5 | **50.5** | 9.0 |
| 20 000: `N*` mediana | 43.5 | 28.0 | 41.0 | **41.5** | 3.0 |
| a la lenta / mal ruteados (60 000) | 0 / 0 | 11 / 11 | 0 / 0 | 0 / 0 | 26 / 0 |

Q1 a 60 000 **OK** (≥ 48 y > v13 en 19/20) para PAT y PATC; **Q1 a 20 000 NO** (41–41.5 < 45, aunque > v13 en 19/20); Q2 celdas y
divisiones sin cambio (90 / 60) **OK**; Q3 nada mal ruteado **OK**; **S2 barajar los contadores destruye la ganancia (20/20)**
→ lo que actúa es la evidencia, no "abrir la puerta". **S1 generalización (`bateria_generaliza`, 101–120): PAT y PATC
CONSERVAN la generalización** (K 20/20; G1 px0 1.000 / azar 0.500, 19/20; G2 0.960, 20/20): el canje puerta–capacidad **se
rompe** en el paso largo sin pagar la generalización. **Retención (examen v3' completo):** PAT **falla 3''** (0/20; la
predicción de la enmienda 1) y E2 19/20; PATC pasa 3' (0/20), **3'' (20/20)**, celdas, 4a–4d, E1/E2I–E2L 20/20 y **falla E2 por
una semilla** (`come B Q4 ≥ 50`: 19/20; los pesos `W_A → −3`, `W_B → +1` 20/20). Por la cláusula del preregistro (retención
8/8) **no entra al tronco**. Lectura honesta: el mecanismo hace lo que dice (desacopla "¿lo he visto?" de "¿tengo su valor
sin repartir?", ERR-25) y cierra el canje en 60 000 sin tocar la generalización; el fallo de E2 es una semilla en un
subcriterio conductual, con los pesos correctos en las 20 — puede ser muestreo o un coste real de reabrir la rápida antes
de tiempo. **Sin recalibrar: réplica del examen v3' de PATC en semillas nuevas (121–140), misma letra**; si vuelve a caer
E2, la puerta por código queda como órgano de experimento; si pasa 8/8, es el tercer candidato a v14. Vocabulario: *la
puerta pregunta si lo ha visto, no si tiene el valor entero; con eso recuerda tanto como v11 y generaliza como v13*.


### v13E — "la sorpresa del mundo en la boca" en la copia del tronco, examen v3'' completo (101–120; 18 sep 02:45): **retención 8/8 con el criterio 5 adaptado; la generalización de VALOR cae por debajo de la letra (G1 px0 0.750 < 0.80; referencia apagada 0.800) → por el preregistro NO entra al tronco tal cual; coste medido, dosis a preregistrar**

Preregistro `experimentos/nivel9_probar_si_mismo/PREREGISTRO_v13E.md` (fe50ccb6ffde9427; E1 examen v3' completo 8/8, **E2 G1 ≥ 0.80
y G2 ≥ 0.85 y K 20/20**, E3 diagnóstico; criterio 5 adaptado por ERR-30: la reducción a v11 apaga también `k_testE`/`eta_pred`);
instrumentos por anclas `organismo_v13E` (ab8e3b0579edfc29; = `organismo_v13p` con `eta_pred = 0.03, ema_pred = 0.05, k_testE = 10`
fijos), `organismo_v13gE`, `bateria_v13E` (bed81b870faf5da5), `bateria_generaliza_E`; **identidad 28/28** en la copia principal
(incluida la reducción a v11 con las cuatro perillas apagadas, 3/3); datos `baterias_v13E_20260918_023210` (973c306b44f7f87b), 13 min.

| prueba (perilla ENCENDIDA) | resultado |
|---|---|
| E1 examen v3' completo | E1–E2L **20/20 × 6**; celdas ≤ 45; 3' 0/20; 3'' 20/20; 4a–4d OK; criterio 5 (v3'') OK → **8/8** |
| E2 generalización | K 20/20; **G1 px0 0.750** (azar 0.500; 18/20) — **< 0.80**; G2 0.870 (18/20) ≥ 0.85; referencia apagada G1 0.800 / G2 0.892 |
| E3 inercia sin inversión | divisiones 0 → 0, celdas 30 → 30; sesgo de boca Q1 0.20 (transitorio del predictor) → Q2–Q4 ≈ 0; `W` no idéntico (actúa en Q1) |

**Veredicto por la letra del preregistro: E2 cae (G1 0.750 < 0.80)** → *"se queda como órgano de experimento y no entra al
tronco; nada se recalibra"*. El runner imprimió "NO REGRESIONA" porque su E2 leyó los umbrales de la batería (0.65 / 0.55) en
vez de los preregistrados (**ERR-31**, defecto del runner; el registro sigue al preregistro). **Lectura:** con `k_testE = 10`
el órgano recupera 7× más rápido de un cambio no avisado y conserva la retención entera, pero **cuesta 0.05 en la
generalización de valor** (0.80 → 0.75; la conducta al primer encuentro se mantiene, 0.87) — el mismo mecanismo que hace
probar cuando el mundo sorprende hace probar un poco en lo nunca visto. Es una **dosis**: `k_testE` se fijó por la
mini-prueba de C, no por barrido. Camino declarado: preregistro nuevo con dosis menor (p. ej. `k_testE ∈ {3, 5}`) en semillas
nuevas, exigiendo a la vez recuperación ≤ 0.60× y G1 ≥ 0.80; hasta entonces el segundo candidato queda **fuera de la
propuesta de v14** con su coste anotado. Vocabulario: *la sorpresa del mundo en la boca acelera la recuperación a costa de
una parte de la generalización de valor a la dosis probada*.

### ERR-31 (02:50): el runner `corre_baterias_v13E.py` decidía E2 con los umbrales de `bateria_generaliza` (0.65 / 0.55), no con los preregistrados (0.80 / 0.85)
Consecuencia: veredicto impreso "NO REGRESIONA" contra un preregistro que dice lo contrario. Sin efecto en el registro (se
sigue la letra); regla: el runner codifica los umbrales del preregistro, no los de la batería que reutiliza.


### B-2, réplica del examen v3' de PATC en semillas nuevas 121–140 (enmienda 2; 18 sep 02:41): **8/8 — E2 20/20** → la puerta por evidencia del código (código ∧ 1 celda consolidada) es el **tercer candidato a v14**

`bateria_v13Bc.py 20 --desde 121 --log`, misma letra; datos `examen_v13Bc_20260918_023737` (e1b50852bbf07fea), 3.1 min. E1–E2L
**20/20 × 6** (E2 `come B Q4 ≥ 50` 20/20; en 101–120 había sido 19/20 → 39/40 en dos series), celdas ≤ 45, 3' 0/20, 3'' 20/20,
4a–4d OK, identidad 5 OK. Con esto PATC tiene: capacidad de v11 en el paso largo (`N*` 50.5 contra 35 de v13; 20 000: 41.5
contra 28, umbral 45 no alcanzado — se registra como no alcanzado), generalización intacta (px0 1.000 / G2 0.96, 101–120),
contadores barajados destruyen la ganancia (20/20), examen v3' 8/8 en 121–140 (39/40 en E2 sobre dos series), identidad de la
copia 21/21. Mecanismo: `familiar(P) ⟺ ncod[código(P)] ≥ 5 ∧ ≥ 1 celda consolidada`; memoria: un entero por código visto; no
toca el aprendizaje, sólo el ruteo. **Entra a `registro/PROPUESTA_v14.md` como tercer candidato (condición cumplida); la
decisión es del director.** Vocabulario: *la puerta pregunta si lo ha visto y si tiene al menos una celda que lo sostenga; con
eso recuerda tanto como v11 y generaliza como v13*. Abierto: el paso corto (41.5 < 45) y la composición con los otros
candidatos.


### Bloque de dosis de "la sorpresa del mundo en la boca" (`k_testE` ∈ {3, 5}; 18 sep 03:32): **k = 5 cumple las seis condiciones a la vez — recupera 0.27× (20/20), se apaga (20/20), G1 0.80, G2 0.857, K 20/20 y examen v3'' 8/8 → vuelve a la propuesta de v14 como segundo candidato, a dosis 5**

Preregistro `experimentos/nivel9_probar_si_mismo/PREREGISTRO_dosis_dE.md` (e58b9525eb0ee575; escrito antes de correr; las seis
condiciones deben cumplirse a la vez; predicción: dE5 cumple, dE3 recupera ≈ 0.40× con G1 = referencia); instrumentos por
anclas `organismo_v13E_k3/k5` (+ mundo de regla y baterías por dosis, criterio 5 adaptado por ERR-30), **identidad 36/36** en la
copia principal; orquestador `corre_dosis_dE.py` con los umbrales del preregistro (ERR-31); datos `dosis_dE_20260918_031724`
(1c7c45a42a79e4a0) con `probar_si_mismo_s121-140_20260918_031725` (recuperación, semillas nuevas 121–140),
`regresion_generaliza_organismo_v13E_k3/k5_20260918_0324xx` y `examen_v13E_k3/k5_20260918_032604/032913` (101–120); 15 min.

| dosis | recuperación (V13 10 126) | pareado | se apaga (P4') | G1 px0 (pareado) | G2 | K | examen v3'' | veredicto |
|---|---|---|---|---|---|---|---|---|
| k = 3 | 4 219 (0.417×) | 17/20 | 20/20 | 0.85 (19/20) | **0.842 < 0.85** | 20/20 | **7/8** (una etapa científica) | no candidata |
| **k = 5** | **2 700 (0.267×)** | **20/20** | **20/20** | **0.80 (17/20)** | **0.857** | **20/20** | **8/8** | **CANDIDATA** |
| k = 10 (v13E, ya medido) | 0.14× ×3 | 20/20 ×3 | 20/20 ×3 | **0.75** | 0.87 | 20/20 | 8/8 | fuera (G1) |

**Lectura:** es una dosis. A `k_testE = 5` el órgano conserva la recuperación rápida (0.27× de v13, 20/20 en semillas nuevas) y
recupera la generalización de valor de v13 (0.80) con el examen completo 8/8; a 3 la ganancia de recuperación baja (0.42×) y
cae otra cosa (G2 y una etapa del examen: no es monotónico, se anota sin interpretar); a 10 cuesta 0.05 de G1. La predicción
del preregistro se cumple para dE5 y falla en el detalle de dE3 (G1 sí, G2 no). **Segundo candidato reinstalado en
`registro/PROPUESTA_v14.md` a dosis 5** (copia `organismo_v14_candidato_sorpresa.py` en la rama `v14-candidato`); faltan, si el
director lo acepta: réplica de la recuperación en otra serie a dosis 5 (hoy: una serie a 5 y tres a 10), gemelo y congelación.
Vocabulario: *la sorpresa del mundo puesta en la boca, a dosis 5, hace probar cuando el mundo cambia sin cobrar
retención ni generalización*.


### Composición de los dos candidatos aceptados (hija dispersa + puerta por código PATC) sobre el tronco (18 sep 03:55): **por la letra, "los órganos interfieren, no se proponen juntos" — C1 cae por UNA semilla en E2 (19/20, la misma fragilidad que PATC solo en 101–120), C2 y C4 pasan, C3 queda 0.013 por debajo de la hija sola**

Preregistro `experimentos/nivel10_composicion_v14/PREREGISTRO_composicion_v14.md` (47e9bdee00afc5c9; escrito antes de correr);
instrumentos por anclas sobre el tronco con los dos parches (colisión de la firma resuelta y declarada): `organismo_v14c`
(649851c0f10c3cd6; perillas apagadas ≡ v13), `organismo_v14c_on` (00e941c861896455), `organismo_v14gc`, `organismo_capBD`,
`mundo_composicion_v14`, `bateria_v14c`, `bateria_generaliza_v14c`; **identidad 30/30** en la copia principal (cada perilla sola
≡ su candidato: v13Don 3/3, v13Bn5c 3/3); datos `composicion_v14_20260918_033225` (f9de95cb542342f7), 22 min.

| medida (las dos perillas ON) | resultado | umbral | veredicto |
|---|---|---|---|
| C1 examen v3' completo (101–120) | E1, E2I–E2L 20/20; **E2 19/20** (`come B Q4 ≥ 50`); celdas ≤ 45; 3' 0/20; 3'' 20/20; 4a–4d OK → 7/8 | 8/8 | **NO** |
| C2 generalización (101–120) | K 20/20; G1 px0 **1.000** (20/20); G2 **0.940** (20/20) | ≥ 0.80 / ≥ 0.85 | OK |
| C3 composición 3T-k, k = 5 (61–80) | lift **0.237** (> V13 18/20; V13 0.137); sep 2.90 (V13 1.87); celdas **53** (V13 90; 19/20) | lift ≥ 0.25 y ≥ hija sola (0.251) | **NO** por 0.013 |
| C4 capacidad, mundo grande (41–60) | `N*` **51.0** a 60 000 (v13 35.0); 44.0 a 20 000 (v13 28.0) | ≥ 48 | OK |

**Lectura honesta.** El único fallo del examen es la misma semilla-subcriterio que PATC solo dio en 101–120 (19/20) y que pasó en la
réplica 121–140 (8/8): con la letra del preregistro no se pueden proponer juntos; con los datos, no hay señal de interferencia
más allá de esa fragilidad conocida de PATC, y la composición **suma**: generaliza mejor que cualquiera solo (1.000 / 0.94),
recupera la capacidad (51) y compone historias profundas con la mitad de celdas (53), aunque la puerta le resta un poco de
ventaja conductual a la hija dispersa (0.237 contra 0.251). **Enmienda 1 (escrita ahora, antes de correr, semillas nuevas):
réplica del examen compuesto (C1) en 121–140 con la misma letra** (`bateria_v14c.py 20 --desde 121 --log`); si 8/8, la
composición pasa a la propuesta como opción conjunta (C3 se reporta como está: no alcanza 0.25); si vuelve a caer E2, quedan
como candidatos separados y el director elige. Vocabulario: *juntos generalizan y recuerdan como el mejor de los dos y componen
casi como la hija sola; la puerta cuesta una semilla de conducta en el examen de 101–120*.


### Dosis 5 de "la sorpresa del mundo en la boca", réplica de la recuperación en semillas nuevas 141–160 (enmienda 1; 18 sep 04:05): **REPLICA — 0.248× (20/20), se apaga 20/20, retención 20/20 × 6, G1 0.80 = v13, G2 0.89, sin más veneno ni muertes**

`corre_probar_si_mismo.py --desde 141 --brazos V13,dE5 --baterias V13,dE5`; datos `probar_si_mismo_s141-160_20260918_035504`
(c51d159b83d9ec38); identidades 33/33 dentro del runner; 10 min.

| brazo | recuperación | pareado | se apaga (P4') | veneno post | muertes | retención (6 etapas) | G1 px0 / G2 |
|---|---|---|---|---|---|---|---|
| V13 | 9 076 | — | — | 56 | 275 | 20/20 × 6 | 0.80 / 0.85 |
| **dE5** | **2 249 (0.248×)** | **20/20** | **20/20** | 61 | 278.5 | **20/20 × 6** | **0.80 / 0.89** |

Con esto el segundo candidato tiene, a dosis 5: dos series de recuperación (0.267× en 121–140 y 0.248× en 141–160, 20/20 × 2),
apagado 20/20 × 2, generalización de valor igual a v13 en las dos (0.80), retención de las seis etapas 20/20 × 2 y el examen v3''
completo 8/8 (101–120); y a dosis 10, tres series más de recuperación (0.14×). Vocabulario: *la sorpresa del mundo puesta en la
boca, a dosis 5, hace probar cuando el mundo cambia y por eso se recupera cuatro veces antes, sin cobrar retención ni
generalización*. Falta sólo lo administrativo (gemelo, congelación) y la decisión del director.


### Composición hija dispersa + puerta por código, réplica del examen compuesto en 121–140 (enmienda 1; 18 sep 04:03): **8/8 (E2 20/20) → los dos órganos NO interfieren: la composición entra a la propuesta como opción conjunta**

`bateria_v14c.py 20 --desde 121 --log` (las dos perillas ON), misma letra; datos `examen_v14c_20260918_035946` (47bb21f5e8e3c06c),
3.2 min. E1–E2L **20/20 × 6** (E2 `come B Q4 ≥ 50` 20/20; en 101–120 había sido 19/20 → 39/40 en dos series, exactamente el
patrón de PATC solo), celdas ≤ 45, 3' 0/20, 3'' 20/20, 4a–4d OK, identidad 5 OK. Con esto la composición tiene: examen 8/8 en
121–140 (7/8 en 101–120 por la semilla conocida), generalización **G1 1.000 / G2 0.94** (mejor que cualquiera solo), capacidad
`N*` **51** (v13 35), composición temporal lift **0.237** con **53 celdas** (v13 0.137 / 90; hija sola 0.251 / 48: la puerta resta
0.014 de ventaja conductual, registrado tal cual, no alcanza el 0.25 preregistrado). **Propuesta conjunta: v14 = v13 + hija
dispersa + puerta por evidencia del código** (copia `organismo/organismo_v14_candidato_conjunto.py` = `organismo_v14c_on.py` en la
rama `v14-candidato`). La sorpresa del mundo en la boca (dosis 5) sigue como candidato aparte: su composición con los otros dos
no se ha medido (paquete en preparación). La decisión es del director.


### Propuesta conjunta v14 (v13 + hija dispersa + puerta por código), protección extra antes de congelar (enmienda 2; 18 sep 04:22, con el director de vuelta: "prueba los dos"): **segunda serie limpia del examen 8/8 en 141–160 y generalización 1.000 / 0.95 en 121–140**

`bateria_v14c.py 20 --desde 141 --log` → `examen_v14c_20260918_041824` (db6344e0f7982574): E1–E2L 20/20 × 6, celdas ≤ 45, 3' 0/20, 3''
20/20, 4a–4d OK, identidad 5 OK → **8/8**. `bateria_generaliza_v14c.py organismo_v14c_on 20 --desde 121 --log` →
`regresion_generaliza_organismo_v14c_on_20260918_042128` (b16214bb8cd00b56): K 20/20; G1 px0 **1.000** (azar 0.500; 20/20); G2 **0.950**
(azar 0.464; 20/20). **Estado de la propuesta conjunta:** examen 7/8 (101–120, la semilla conocida de PATC), **8/8 (121–140), 8/8
(141–160)**; generalización 1.000 / 0.94 (101–120) y 1.000 / 0.95 (121–140); capacidad `N*` 51 (41–60); composición 3T-k 0.237 con 53
celdas (61–80); identidad 30/30. Cumple la regla de tronco (examen + baterías + réplica). Falta: gemelo compilado (en construcción),
congelación (manifiesto, tag), regresión de la regla 1. **La decisión de congelar sigue siendo del director.**


### Caso conocido — semilla 117 del rango 101–120 (18 sep 04:45; a petición del director: "¿cómo ves las semillas?")

En los exámenes de 101–120 el único subcriterio que cae con la puerta por código es E2 `come B Q4 ≥ 50`, y cae **en la misma
semilla y con el mismo valor** en dos organismos distintos: PATC solo (`examen_v13Bc_20260918_022843`: semilla **117**, 42 bocados de
B en el último cuarto) y la composición hija + puerta (`examen_v14c_20260918_033226`: semilla **117**, 42). En 121–140 y 141–160
(`examen_v14c_..._035946`, `_041824`) ninguna semilla baja de 50. No es azar: es un mundo concreto donde reabrir la vía rápida a
un patrón ya visto (lo que la puerta por código hace por diseño) cuesta comida en el cuarto final. Queda como **caso conocido**
del candidato v14, no como ruido; los pesos (`W_A → −3`, `W_B → +1`) están bien en esa semilla. **Lección de semillas (lo
honesto):** 20 semillas es una resolución de un 5 % por semilla; cuatro veredictos de la noche se decidieron por una semilla en
el umbral (ahorro 16/20 vs 18, E2 19/20 ×2, apagado 15/20 vs 16). El método los salvó con réplicas en rangos nuevos; la regla
12 de EQUIPO.md lo hace automático. Los efectos pequeños (composición 0.237 vs 0.251; G1 0.75 vs 0.80) están en el límite de lo
que 20 semillas distinguen: con el gemelo compilado, las series de efectos < 0.05 pasan a 40 semillas.


### Composición de los TRES órganos (hija dispersa + puerta por código + sorpresa del mundo en la boca a dosis 5; 18 sep 04:47): **por la letra NO van juntos (T1 réplica 7/8: E2 19/20 en 121–140, semilla 133 con 42 bocados); T1 101–120 8/8, T2 1.000 / 0.93, T3 recuperación 0.24× (19/20) → v14 = los DOS primeros; la sorpresa sigue como candidata a v15 con su composición ya medida**

Preregistro `experimentos/nivel10_composicion_v14/PREREGISTRO_composicion_tres.md` (0558a198017794f9; escrito antes de correr);
instrumentos por anclas `organismo_v14t` (fc4a803019116a88; tres perillas apagadas ≡ v13), `organismo_v14t_on`, `organismo_v14gt`,
`bateria_v14t` (criterio 5 con las cuatro perillas apagadas ≡ v11, ERR-30), `bateria_generaliza_v14t`; **identidad 25/25** en la
copia principal (cada órgano solo ≡ su candidato); datos `composicion_tres_20260918_043921` (99faae2f9bb50b90) con
`examen_v14t_20260918_043922` (101–120), `examen_v14t_20260918_044233` (121–140), `regresion_generaliza_organismo_v14t_on_20260918_044543`,
`recuperacion_tres_20260918_044630` (8b4ed6ca25aeaa16); 8 min.

| medida (las tres ON) | resultado | umbral | veredicto |
|---|---|---|---|
| T1 examen v3'' 101–120 | **8/8** (la semilla 117 pasa con las tres) | 8/8 | OK |
| T1 réplica 121–140 | **7/8**: E2 19/20 (`come B Q4 ≥ 50`: semilla **133**, 42 bocados) | 8/8 | **NO** |
| T2 generalización 101–120 | K 20/20; G1 **1.000** (20/20); G2 **0.930** (20/20) | ≥ 0.80 / ≥ 0.85 | OK |
| T3 recuperación 161–180 | TRES 1 958 contra V13 8 136 (**0.241×**; pareado 19/20); se apaga 20/20; veneno 60 ≤ 228; muertes 267.5 ≤ 398 | ≤ 0.60×, ≥ 14/20, ≥ 16/20 | OK |
| T4 composición 3T-k | no medible sin un cuarto constructor | — | — |

**Lectura honesta.** La tercera pieza conserva su efecto en compañía (0.24×, el mismo que sola) y no toca la generalización
(1.000 / 0.93); el único fallo es otra vez **una semilla en E2 con 42 bocados de B**, ahora la 133 (antes la 117 con la puerta sola y
con las dos): el valor idéntico (42) en tres exámenes distintos apunta a un mundo-tipo donde la puerta reabre la vía rápida en
el cuarto final, no a azar — se pasa al auditor como pregunta (¿por qué siempre 42?). Por la cláusula del preregistro y la
decisión del director ("los tres si pasan; si no, los dos"): **v14 = v13 + hija dispersa + puerta por código**; la sorpresa
del mundo en la boca a dosis 5 queda como **candidata a v15**, con dos series sola, examen 8/8 sola, y en compañía T2/T3 OK y
T1 8/8 + 7/8. Vocabulario: *las tres piezas no se estorban en lo que cada una hace; la puerta sigue costando una semilla de
conducta en el examen en algunos mundos*.


### v14 (dos órganos), tercer examen en rango virgen 161–180 y generalización en 141–160 (18 sep 04:52; decisión del director): **8/8 y 1.000 / 0.951 → tres exámenes 8/8 en rangos distintos y tres baterías de generalización**

`bateria_v14c.py 20 --desde 161 --log` → `examen_v14c_20260918_044752` (7c18dc86a6168eba): E1–E2L 20/20 × 6, celdas ≤ 45, 3' 0/20, 3'' 20/20,
4a–4d OK, identidad 5 OK → **8/8**. `bateria_generaliza_v14c.py organismo_v14c_on 20 --desde 141 --log` →
`regresion_generaliza_organismo_v14c_on_20260918_045101` (7304564adde75dbd): K 20/20; G1 px0 **1.000** (20/20); G2 **0.951** (19/20).
**Evidencia final de v14 = v13 + hija dispersa + puerta por código:** examen v3' 8/8 en 121–140, 141–160 y 161–180 (7/8 en 101–120
por la semilla 117, caso conocido); generalización 1.000 / 0.94 (101–120), 1.000 / 0.95 (121–140), 1.000 / 0.95 (141–160); capacidad
`N*` 51 (v13 35); composición 3T-k 0.237 con 53 celdas (v13 0.137 / 90); identidad de la copia 30/30; gemelo compilado 196/196
(×52–82). Cumple con exceso la regla de tronco. **Se congela** (entrada de congelación a continuación).


### v14 CONGELADO COMO TRONCO (18 sep 2026, 05:05; decisión del director "sí a todo", 04:55): **v14 = v13 + hija dispersa por relevancia + puerta de familiaridad por evidencia del código exacto**

Archivos: `organismo/organismo_v14.py` (9bab8ac0685b1f21; = `organismo_v14c_on` 00e941c861896455, generado por anclas desde v13 con
`construye_v14c.py`; con `mask_rel=0, puerta_pat=0` es v13 exacto), `organismo/organismo_v14g.py` (1f1318480cd34cde, mundo de regla),
`organismo/bateria_v14.py` (101cba9177e8e5af; examen v3' completo, copia por anclas de `bateria_v13`), `bateria_generaliza.py` con el
instrumento `organismo_v14` (perillas ON); `manifiesto.py` pasa a **16 congelados**; tag `v14-tronco`. Gemelo compilado
`organismo_v14c_rapido.py` (196/196, ×52–82; el módulo con defaults ON `organismo_v14_rapido.py` en integración).

| evidencia | resultado |
|---|---|
| examen v3' completo (criterio 5 intacto: apagando `eta_s`/`puerta` ≡ v11) | **8/8 en 121–140, 141–160 y 161–180**; 7/8 en 101–120 (semilla 117, `come B Q4` 42: caso conocido) |
| generalización (K, G1, G2) | **1.000 / 0.94** (101–120), **1.000 / 0.95** (121–140), **1.000 / 0.95** (141–160); v13: 0.80 / 0.89 |
| capacidad (mundo grande, 60 estímulos, paso 60 000) | `N*` **51** (v13 35; v11 50) |
| composición temporal 3T-k, k = 5 | lift **0.237** con **53** celdas (v13 0.137 con 90; hija sola 0.251 con 48) |
| identidades | copia ≡ v13 con perillas apagadas 30/30; cada órgano solo ≡ su candidato; gemelo 196/196 |
| regresión regla 1 sobre las copias congeladas | examen 8/8 con 6 semillas (examen_v14_20260918_045742, 4c4e45d2dcf8f8f7); generalización K 20/20, G1 1.000 / G2 0.940 en 101–120 (regresion_generaliza_organismo_v14_20260918_045939, 0ae8fd144d801d93); gemelo organismo_v14_rapido ≡ organismo_v14 42/42 desde organismo/ |

**Lo que v14 hace de más que v13:** compone historias de 4–5 pasos con distractores gastando la mitad de las celdas; recuerda
50 de 60 patrones con valor (como v11) sin perder la generalización de v13 (y generaliza mejor: 1.000 / 0.95). **Lo que no
cambia:** XOR, significado emergente (N2) y planificación en 2D siguen sin mecanismo. **Coste conocido:** en algunos mundos
(semillas 117 y 133) la puerta reabre la vía rápida en el cuarto final y E2 queda en 42 bocados (< 50); registrado, no
recalibrado. **Candidata a v15:** la sorpresa del mundo en la boca a dosis 5 (dos series sola; en compañía T2/T3 OK, examen
8/8 + 7/8). Regla 1 (regresión) pasa a: `cd organismo && python bateria_v14.py 6 && python bateria_generaliza.py organismo_v14 20 --desde 101`
(con 10 semillas 41–50 el control azar quedó en 0.40, fuera de la banda 0.42–0.58: n = 10 no basta para el control);
`bateria_v13.py 6`, `bateria_v11.py 6` y `bateria_v9.py 6` como regresión histórica. v13 pasa a tronco anterior.


### Frente "dos organismos", creador A (18 sep 05:40): **CONTROL POSITIVO — con el mismo flujo de encuentros, los mismos rasgos y el mismo muestreo real, el gradiente exacto llega a 1.000 en XOR con los rasgos correctos → el cuello es la REGLA (y los rasgos), no el mundo; la predicción del techo 0.75 queda refutada y corregida por su autor**

Instrumento `experimentos/creacion_A/organismo_v13q5.py` (fae9c32b146fdbb4; por anclas desde v13q4 ← v13q3; perilla `lab` que sólo graba
la secuencia (t, patrón, R, residuo) de cada actualización de la vía lenta; identidad 16/16 con `lab` apagado y encendido; replay
≡ organismo en 20/20 semillas, 0 diferencias). Sobre ese flujo, 20 semillas, T = 100 000:

| lectura | DELTA (regla local del tronco) | **LSQ (gradiente exacto, mismos datos)** | MLP 6px→8→1 (retropropagación sobre píxeles) |
|---|---|---|---|
| cuadrática (21 + 1 rasgos) | 0.438 | **0.562** | 0.531 |
| oráculo {P0, P1, P0·P1, 1} | 0.625 | **1.000** (14/20 semillas con las cuatro clases) | 0.531 |

**Lecturas:** (1) con los rasgos correctos la información está en los datos (LSQ 1.000 con **10 exposiciones**; el tronco no llega
con 600): **repetir no es la palanca**; (2) la retropropagación sobre píxeles crudos NO gana (0.531): más capacidad no compra nada,
los rasgos correctos lo compran todo; (3) por qué la delta no llega: `clip_s = 3` no deja caber la solución (`|w| = 8`) y
`eta_s = 0.015` no la recorre en ~290 mordidas desalineadas; barrido sobre el mismo flujo: (0.015, 3) 0.656 · (0.15, 3) 0.750 ·
**(0.15, 10) 1.000** · (1.0, ·) 0.500; (4) la predicción del propio creador (techo de muestreo 0.75) estaba mal: la midió con un
perfil sintético; con los flujos reales 14/20 semillas muerden las cuatro clases (errata corregida en el puente).
**Meta-aprendizaje de la regla** (888 configuraciones, búsqueda en 1–10, retenidas 11–20): ganadora `eta_s = 0.15, clip_s = 10,
WTA(θ = 0.3, ρ = 0.02, cupo 1)`, 0.625 en búsqueda → **0.531 en retenidas** (justo el techo del gradiente exacto con rasgos
cuadráticos); implantada en el organismo (3 semillas) 0.375 → 0.500 y abre `P0·P1` en 3/3. **Propuestas A-4 (dos números de la
vía lenta; control que puede fallar: la generalización y la retención del tronco con `eta_s` ×10) y A-5 (este control positivo)**;
paquete A-4 en preparación. Lo que esto dice del frente: el organismo CON (gradiente) sólo gana cuando le dan los rasgos; el
siguiente cuello real es **construir los rasgos** (selección conjuntiva en pocas exposiciones), y eso es del organismo SIN.


### Frente "dos organismos", creador C (18 sep 05:50): **aprender sin morder por codificación predictiva sobre la vía lenta — REFUTADO como estaba escrito (no baja exposiciones ni mordidas); el retorno ALEATORIO daña en una capa (feedback alignment sólo tiene sitio donde hay capa oculta: las celdas KW); la única fuente de información del organismo son sus propias mordidas**

Instrumento `experimentos/creacion_C/organismo_v14pc.py` (edfcb77a9ca91682; por anclas desde `organismo/organismo_v14g.py`), identidades K1
(apagado ≡ v14g) 12/12, K2 (el predictor sólo mide) 12/12, K3 (la sonda de exposiciones sólo lee) 12/12. Mini-prueba (24 corridas
de 100 000, semillas 1–3, criterio 0.90 en px0, `eta_c = eta_s = 0.015` no buscado; el humo de la semilla 1 declarado antes de las
predicciones):

| brazo | exposiciones hasta criterio (mediana; s1/s2/s3) | mordidas | `acc_lenta` fase 2 |
|---|---|---|---|
| sólo bocados (el actual) | **995** (2 298 / 995 / 555) | 104 | 1.00 |
| consolidación por predicción, crédito directo | 1 703 (1 703 / 3 507 / 226) | 165 | — |
| consolidación, retorno transpuesto | 631 | — | 1.00 (no daña) |
| consolidación, retorno aleatorio (feedback alignment) | censurada / 1 878 / censurada | — | **0.70 (daña)** |
| retorno aleatorio barajado (control) | 399 / censurada / 1 221 | — | — |

MP-K1 (exposiciones ≤ 0.80×) **refutada** (1.71×); MP-K2 (mordidas ≤ 0.80×) **refutada** (1.59×, como el creador había predicho); MP-K3
sostenida y más fuerte: el retorno aleatorio es peor que la base en 3/3 e indistinguible de su control barajado; MP-K4 (xor01 no
se mueve) refutada en dirección contraria: 0.25 → 0.56 con `fa` (n = 3, cabo abierto). ERR propio corregido antes de publicar
(las corridas censuradas se contaban saltándolas). **Mecánica:** en una lectura lineal de una capa el crédito exacto es la
propia entrada, así que un retorno aleatorio no tiene nada que comprar y rompe la estructura por píxeles; la consolidación
redistribuye lo que las mordidas ya enseñaron, no crea información. **Consecuencia para el frente:** "aprender sin morder"
exige otra fuente de información — otro organismo (N2 por predicción, instrumento aprobado) o el mundo (predecir el estímulo
siguiente, no sólo la energía) — y el retorno asimétrico, si sirve, es sobre las celdas KW (C-P5, sin mini-prueba).


### Frente "dos organismos", creador B (18 sep 06:00): **órgano de asociación en una exposición (grafo con soporte de alta dimensión) — NO en el mundo del tronco, con la razón medida: aquí el parecido contradice el valor; la alta dimensión sí hace falta para que el grafo tenga aristas legibles**

Instrumento `experimentos/creacion_B/organismo_v14L.py` (d6d550aec83f775a; por anclas desde el tronco congelado `organismo_v14`), identidad
8/8 con la perilla apagada; medida nueva de sólo lectura `exp_hasta[patrón]` = exposiciones hasta asociar. Mini-prueba (semillas 1–3,
T = 100 000, un proceso):

| escenario | v14 | vía lenta (memoria 0) | HD (Kanerva) | azar | grafo con fiabilidad por arista |
|---|---|---|---|---|---|
| C veneno, parecido débil | 16 | **13** (mejor 3/3) | 16 | no asocia 2/3 | 17 |
| D comida con 2 px de veneno (parecido engañoso) | **8** | 11 (peor 3/3) | 13 (peor 3/3) | — | 13 (peor 3/3) |

Desligar cuesta una mordida (3/3), pero el préstamo cae en celdas compartidas y contamina al vecino (`W_B` −2.97 → −4.2/−5.5).
**Diagnóstico estructural (200 sorteos, sin correr el organismo):** similitud del código por píxeles compartidos 0/1/2 → HD (n = 2 000,
k = 40): 0.025 / 0.075 / 0.225 (graduada); Kenyon del tronco (K = 3 de 90): 0.000 / 0.000 / 0.333 (no distingue). Es decir, la
alta dimensión hace falta para que un grafo de parecidos tenga aristas legibles — pero en el mundo del tronco (4 patrones de
peso 3 sobre 6 px) el único par lo bastante parecido para heredar es comida/veneno: **el parecido no predice el valor, lo
contradice**, y la señal que enseñaría al grafo (acierto/fallo por episodio de ligadura, 2–3 por patrón nuevo) es más rara que el
problema que debe arreglar. **Lo que pide preregistrar (formato fijo en el puente):** no el órgano, sino la pregunta que lo decide:
`exp_hasta` en el mundo de regla con `px0` (donde el parecido SÍ predice el valor) contra `azar` (donde no), mismo instrumento y
semillas; si el contraste no aparece, refutado en los dos mundos. Coste en generalización y capacidad no medido (no es candidato).
Pregunta B-4 al explorador (umbral de similitud n/k en HD; ensayos hasta asociar en abeja/Drosophila; animales que aprenden qué
relación predice el valor).


### Frente "dos organismos", creador C (18 sep 06:40): **N2 por predicción — el significado se aprende con la magnitud exacta del mundo (u = +0.80 / −0.38; controles ≈ 0), pero el mudo lo delata: es obediencia en línea, y en el montaje de N3d NO PUEDE ser otra cosa (los dos miembros de cada pareja tienen la misma retina para el receptor) → ERR-32 de montaje, hallado antes de gastar 20 semillas**

Instrumento `experimentos/creacion_C/mundo_social_pred.py` (fc306b8fcddabe15; por anclas desde `mundo_social_n3` ef227f833c5bf46a; perillas
`eta_sym`/`gamma_pred`/`theta_a` y contador de exposiciones); identidad **63/63** (las siete condiciones de N3d × 3 semillas; L1 apagado ≡
original, L2 el contador sólo lee, L3 `u[c]` se aprende sin usarse). Mecanismo, dos escalares: `u[c] ← u[c] + eta_sym·(E_VAL − u[c])` al
morder un patrón del que oyó la conducta `c`; al oírla sin morder, `R̂ = (R_VAL/E_VAL)·u[c]·gamma_pred` (constantes del mundo, sin
parámetro libre). Mini-prueba (21 corridas de 100 000, semillas 1–3, montaje N3d):

| brazo | `u[1]` / `u[0]` (mundo: +0.8 / −0.4) | mordidas hasta criterio 0.75 | acierto Q4 | mudo desde T/2 |
|---|---|---|---|---|
| PRED (significado aprendido por predicción) | **0.800 / −0.38** en 3/3 | 117 / 159 / 153 | 0.805 | **0.502** |
| INNATO (significado dado) | — | 230 / 126 / 92 | 0.821 | 0.511 |
| SOLO_R | — | nunca (censurado 1 347–2 437) | 0.52 | — |
| barajado / emisor que no sabe (controles) | ≈ 0 (−0.07…+0.18) | — | — | — |

**Lectura:** por primera vez en la línea N2 el significado aparece con la magnitud del mundo y no en ±0.3, y cuesta ≈ 27 mordidas
más que recibirlo dado. Pero el control que decide es negativo: con el emisor mudo PRED e INNATO caen a 0.50 (como el 0.503
registrado de N3d): **obediencia en línea, no valor propio**. Y no es fallo del mecanismo sino del montaje: `parejas()` agrupa por
los píxeles 3–5 y la máscara del receptor es [0,0,0,1,1,1] → los dos miembros de cada pareja tienen la misma retina para el
receptor, el mismo código de Kenyon y el mismo `valor(kk)`: **ninguna regla local puede escribir una distinción en un código
idéntico**. N3d mide obediencia, no retención (pariente del ERR de N3c). **ERR-32 (montaje):** los receptores "ciegos" de N3d no
pueden aprender nada propio por construcción; toda lectura anterior de N3d como "transferencia" queda como *obediencia en
línea al que ve* (ya era el vocabulario declarado; ahora con la causa). **Aprobado:** mundo mínimo decidible — parejas con vista
PARCIALMENTE distinta para el receptor, puertas de validez de N3d, y el mudo (N6) como predicción principal (C-P6). Regla
nueva del creador (anotada): toda predicción "≤ k × la base" necesita cláusula para cuando la base no alcanza el criterio.


### Bloque A-4 = BLOQUE 1 de 3 del criterio de parada (XOR; 18 sep 05:35; semillas 81–100): **las dos constantes de la vía lenta (eta_s 0.15, clip_s 10) hacen que la regla local llegue a 1.000 con los rasgos correctos (150 exposiciones contra 400) sin dañar el tronco (examen 8/8, generalización 1.000 / 0.967) — pero con los rasgos propios del organismo XOR sigue en 0.50–0.63: el cuello que queda es CONSTRUIR el rasgo conjuntivo (V3 cae: 11/20)**

Preregistro `experimentos/creacion_A/PREREGISTRO_xor_4.md` (b8f3a148041753cc; anula el borrador 3f); instrumento `organismo_v13q5`
(fae9c32b146fdbb4; identidad 16/16 + 3/3 en el runner); datos `xor_4_s81-100_20260918_053016` (0e5722530398e651), 480 corridas, 4.6 min.

| lectura | brazo | `acc_lenta` xor01 (mediana) | abre `P0·P1` | eventos | n* (≥ 0.75) |
|---|---|---|---|---|---|
| oráculo {P0,P1,P0·P1,1} | TRONCO (0.015, 3) | 0.625 | — | ~290 | 400 |
| oráculo | **DOS_NUM (0.15, 10)** | **1.000** (> TRONCO 16/20) | — | 270 | **150** |
| oráculo | DOS_NUM + WTA | 0.875 | 20/20 | 264 | 200 |
| cuadrática (rasgos propios) | TRONCO | 0.500 | 0/20 | 292 | > 600 |
| cuadrática | DOS_NUM | 0.500 | 0/20 | 231 | > 600 |
| cuadrática | **DOS_NUM + WTA** | **0.625** | **11/20** | 214 | > 600 |
| cualquiera | ETA_1 (1.0, 10) | 0.500 | — | **2–16** | — |

V1 **OK** (oráculo 1.000, > TRONCO 16/20), V2 **OK** (cuadrática 0.500 ≤ 0.65: el techo son los rasgos), **V3 NO** (WTA abre `P0·P1` 11/20 < 15;
`acc` 0.625), V4 OK por la letra pero **no comparable** (ETA_1 cambia la conducta: 2–16 eventos; cláusula §7 del preregistro escrita
antes), V5 NO por ETA_1 (px0 0.500, misma causa). Veredicto del runner: *"las dos constantes no bastan"*. **Controles del tronco
(§6):** `organismo_v14` con (0.15, 10): examen v3' **8/8** en 101–120 (`examen_v14_e015c10_*`), generalización **K 20/20, G1 1.000, G2 0.967**
(`regresion_generaliza_organismo_v14_e015c10_*`) → las constantes no cuestan nada al tronco (identidad con las originales 16/16).
**Lectura:** el cuello de la regla queda resuelto y medido (la regla local llega donde llega el gradiente exacto cuando le dan los
rasgos, y aprende 2.7× más rápido en exposiciones); **el cuello que queda es construir el rasgo conjuntivo en pocas exposiciones**:
la selección meta-aprendida lo abre en 11/20 y sube a 0.625, no a 0.75. **Bloque 1 de 3: XOR 0.625 (no cruza 0.75).** Propuesta
derivada, sin ejecutar: v14.1 = v14 con (0.15, 10) (cambio de dos constantes del tronco congelado; decisión del director). Siguiente
bloque (A-6): mecanismo local de construcción/selección de rasgos conjuntivos con `n*` como número principal.


### Bloque B-5 (lateral, un bloque; 18 sep 05:55; semillas 101–120): asociación por parecido en el mundo de regla — **NO CONFIRMA como estaba escrito: la variante barata (vía lenta, memoria cero) baja las exposiciones hasta asociar de 4.5 a 2.0 en px0 (pareado 14/20) sin dañar la generalización, pero en azar no cuesta (7.8 contra 8.0): asocia más rápido en general, no sólo donde el parecido predice el valor**

Preregistro `experimentos/nivel3_asociacion/PREREGISTRO_asociacion.md` (af37ac512d999d21); instrumento `organismo_v14gL` (1d3bca2d54b7a064; por
anclas desde `organismo_v14g`, 2 anclas adaptadas y declaradas; identidad 12/12 en la copia y 3/3 en el runner); datos
`asociacion_s101-120_20260918_055214` (39bec0c57104b953), 160 corridas, 3.3 min.

| brazo | px0: exposiciones hasta asociar (mediana) | pareado < v14 | azar: exposiciones | G2 (px0) |
|---|---|---|---|---|
| v14 | 4.5 | — | 8.0 | 0.940 |
| **vía lenta (memoria cero)** | **2.0** (−56 %) | **14/20** | 7.8 | 0.917 |
| HD (Kanerva) | 2.8 (−38 %) | 12/20 | 7.2 | 0.893 |
| grafo | 4.0 | 10/20 | 9.0 | 0.897 |

Criterio: en px0 al menos un brazo baja ≥ 30 % con pareado ≥ 14/20 → **vía lenta cumple**; en azar ninguno baja > 10 % → cumple; **pero "el
engaño cuesta" (exposiciones en azar ≥ v14) falla** para vía lenta y HD (7.8 y 7.2 contra 8.0): el contraste que decidía la hipótesis
del creador B (que la asociación sirve sólo donde el parecido predice el valor) no aparece. G1 1.000 y G2 ≥ 0.89 en todos. **Lectura:**
la asociación por parecido acelera un poco en todos los mundos y no cuesta nada donde el parecido engaña; no es el mecanismo que la
hipótesis decía, y con 2–4 exposiciones de base no hay margen que valga un órgano. **Línea lateral cerrada** (revisión de rumbo de
las 06:45): el hallazgo que queda es de representación (la alta dimensión da aristas legibles; el código de 3 celdas no), útil
para el mundo vivo y para A-6, no un órgano.


### v14.1 CONGELADO (18 sep 2026, 06:05; decisión del director "sí, mételas"): **v14 con `eta_s = 0.15` y `clip_s = 10` en la vía lenta**

Cambio: dos constantes de `organismo/organismo_v14.py` (ahora feefc88b1fd8d434), el instrumento `organismo_v14` de `bateria_generaliza.py` (mismos
valores) y los defaults del gemelo `organismo_v14_rapido.py`; manifiesto actualizado; tag `v14.1-tronco`. Evidencia (bloque A-4 y su
control §6): con rasgos dados la regla local pasa de 0.625 a 1.000 y de 400 a 150 exposiciones; examen v3' **8/8 en 101–120 y 8/8 en
121–140**; generalización **K 20/20, G1 1.000 / G2 0.967 (101–120) y 1.000 / 0.998 (121–140)**; identidad de la copia con las constantes
originales 16/16. Regresión de la regla 1 sobre el tronco v14.1: examen 8/8 con 6 semillas (examen_v14_20260918_054720, c2331c253bab1681); generalización K 20/20, G1 1.000 / G2 0.967 en 101–120 (regresion_generaliza_organismo_v14_20260918_054926, 6452fdf50352607e); arnés del gemelo 42/42 (el bloque que compara con v13 pasa ahora también las constantes viejas). Lo que NO cambia: XOR con rasgos propios sigue en
0.50–0.63 (el cuello son los rasgos; bloque A-6 en curso). v14 (05:05) queda como tronco anterior.


### Bloque A-6 = BLOQUE 2 de 3 del criterio de parada (XOR; 18 sep 06:05; semillas 101–120): **quitar la constante NO desbloquea (0.500, > REF 4/20); con 8 patrones de entrenamiento no hay información para seleccionar el rasgo ni con el estadístico ideal (3/20); si el mundo muestra 14 patrones, la misma regla local llega a 1.000 en los 6 nunca vistos (200 exposiciones) — XOR con rasgos propios sigue en 0.50 en el mundo original**

Preregistro `experimentos/creacion_A/PREREGISTRO_xor_6.md` (0d6e368d820996f2); instrumento `organismo_v13q6` (b37aa8124c89cc5f; perilla `ntr`;
identidad 8/8 + 5/5 en el runner; gemelo `organismo_v13q5_rapido` en los brazos sin `ntr`); datos `xor_6_s101-120_20260918_055928`
(25dd85e56c19ecc0), 360 corridas, 6 min. Constantes del tronco v14.1 (eta_s 0.15, clip_s 10), lectura cuadrática (rasgos propios),
selección WTA meta-aprendida (θ 0.3, ρ 0.02, cupo 1).

| brazo (xor01) | tren / test | `acc_lenta` (mediana) | abre `P0·P1` antes de la sonda | n* (≥ 0.75) |
|---|---|---|---|---|
| REF (8 patrones, con constante) | 8 / 12 | 0.500 | 11/20 | > 600 |
| **SIN_CTE** (decide: no toca el mundo) | 8 / 12 | **0.500** (> REF 4/20) | 12/20 | > 600 |
| NTR11 (cambia el mundo) | 11 / 9 | 0.625 | 15/20 | 300 |
| **NTR14 (cambia el mundo)** | 14 / 6 | **1.000** | 17/20 | **200** |
| SIN_CTE_NTR11 | 11 / 9 | 0.667 | 16/20 | 300 |
| SIN_SEL (sin competencia) | 8 / 12 | 0.438 | 0/20 | > 600 |

W1 **NO** (la sobredeterminación no explica el techo), W2 NO (NTR11 0.625 < 0.75), W3 OK, W4 NO (11–12/20 en el mundo original), W5 NO
(px0 de SIN_SEL 0.900). Cláusula de muestreo: 2/20 semillas sin una clase XOR en el mundo original, 0/20 con `ntr`. Análisis
previo del creador (banco, sin organismo): el estadístico IDEAL de selección — el residuo del ajuste elemental exacto — pone `P0·P1`
primero sólo en 3/20 semillas con 8 patrones, 7/20 con 11 y 12/20 con 14: **la información no está en 8 patrones**, y con el
conjuntivo abierto son 8 rasgos contra 8 patrones (sistema exactamente determinado, signo frágil).
**Lectura honesta:** (1) bloque 2/3: **XOR con rasgos propios en el mundo original sigue en 0.50** — no cruza 0.75; (2) pero la
misma regla local, con competencia, **sí aprende XOR y generaliza a los nunca vistos cuando el mundo muestra 14 de los 20
patrones** (1.000 en 6 nunca vistos, 200 exposiciones): el organismo no está incapacitado para la no linealidad; lo que le
falta en el mundo original es información suficiente para seleccionar el rasgo con 8 ejemplos — y un mecanismo que la cree sin
más ejemplos es precisamente lo que el tercer bloque tiene que aportar (la sala de agentes trabaja en eso); (3) el mundo de
regla de 20 patrones con 8 de entrenamiento es un instrumento al límite de la identificabilidad: se anota como propiedad del
instrumento, no se cambia el criterio (ERR-33 candidato: mundo con poca información para el rasgo — lo decide el auditor).


### Creador C (18 sep 06:30): el mundo social decidible NO existe todavía — teorema del instrumento y dos ERR candidatos en `mundo_social_n3` (ERR-33, ERR-34; verificación del auditor en curso)

Construido `experimentos/creacion_C/mundo_vd.py` (d670fd65c53e4310): 8 objetos con las 8 vistas del receptor distintas, parejas a
distancia de Hamming 1, 4 comida / 4 veneno; sin perilla nueva (es otra elección de `tipos_fijos` sobre `mundo_social_pred`, cuya
identidad L1/L2/L3 sigue 21/21 cada una). Humos (T = 100 000, semillas 1–3): VD sin rotación → SOLO_R 0.998 (techo: la base lo
resuelve sola); 20 patrones sin rotación → K3 falla (4 de 20 presentes); 20 patrones con flujo → SOLO_R 0.572 (suelo: 18 de 20 en
vistas ambiguas, ERR-32 otra vez); VD con flujo → el flujo descarta `tipos_fijos` y el montaje se destruye. **Teorema (derivable):**
con peso 3, regla `px0` y máscara [0,0,0,1,1,1] hay 8 vistas para 20 patrones, 6 ambiguas; el techo de un lector que sólo ve la
vista es 14/20 = 0.700: **la vista del receptor no puede ser a la vez no informativa sobre la valencia e identificadora del objeto**
— no informativa ⇒ código compartido ⇒ nada que escribir (ERR-32); identificadora ⇒ lo aprende solo ⇒ el canal no aporta.
Enmascarar una retina de 6 píxeles no puede producir el mundo que N3d necesita. En el mundo más duro, PRED 0.708 contra INNATO
0.637 y SOLO_R 0.559 (el canal de significado sigue funcionando; falta el mundo donde medir si retiene).
**ERR-33 (candidato, instrumento):** `Mundo._reaparece` sortea de `self.tipos` (los 20) y no de `fijos` → `regen_rota=True` descarta
`tipos_fijos`: flujo y conjunto controlado son incompatibles (arreglo de una línea, en copia). **ERR-34 (candidato, toca un resultado
registrado):** `nobj = nobj_por_org · n` y `spawn()` consume `fijos` en orden → con 8 nombres, SOLO_R (n = 1) recibe sólo los 4 primeros
y CONV/PRED (n = 2) los 8: **el 0.515 de SOLO_R y el 0.822 de CONV de N3d están medidos sobre conjuntos de objetos distintos**;
probablemente no cambia el veredicto (el receptor es ciego en los dos) pero invalida comparaciones de exposiciones entre brazos con
`n` distinto. Pasa al auditor. Aprobado a C: los dos arreglos como perillas en `mundo_social_pred` (apagadas ≡ actual), tres
humos con SOLO_R en banda y, sólo entonces, el preregistro con el mudo como predicción principal.


### Mundo vivo (línea F; diseñador; 18 sep 06:55): **diseño e instrumento listos con ancla fuerte (37/37: con una necesidad y dos estímulos, TODA la maquinaria encendida es v14.1 bit a bit); mini-prueba: el organismo aprende la tabla exacta necesidad × estímulo (2 × 4) en 7/2/9/3 exposiciones y resuelve el "XOR natural" (1.00 contra 0.50 con una necesidad o con valor escalar) — NO se corre hasta el veredicto de XOR (revisión de rumbo de las 06:45)**

`experimentos/nivel11_mundo_vivo/`: `construye_vivo.py` (03c83de17e34d9a0; 20 sustituciones por anclas desde `organismo/organismo_v14.py`
v14.1 feefc88b1fd8d434), `organismo_vivo.py` (20c0961c79de8825), `identidad_vivo.py` (37/37; el control que debe fallar, falla),
`mini_vivo.py`, `PREREGISTRO_mundo_vivo.md` (borrador + enmienda 1), informe `registro/investigacion/DISENO_mundo_vivo_20260918.md`.
Diseño mínimo: dos necesidades (hambre, sed) con dos muertes, cuatro estímulos (los cuatro patrones que ya existen: comida,
veneno, agua, sal), consecuencia vectorial, sorpresa específica por necesidad, valor por estímulo y necesidad. Mini-prueba (3
semillas, T = 100 000): VIVO xor01(necesidad × estímulo) **1.00** 3/3, tabla exacta {hambre: A +1, B −3, C 0, D 0; sed: A 0, B 0,
C +1, D −3} en 7/2/9/3 exposiciones, muertes 89 [52 energía, 37 agua]; UNA_NEC 0.50 (141 muertes, 97 de sed); ESCALAR 0.50 (160):
**el valor escalar promedia lo que el mundo separa y le va peor que no tener la segunda necesidad**; BARAJA_CON 0.25; NO_INFORMA
1.00 con sal que nunca cruza. Cuatro fallos declarados por el propio diseñador y corregidos antes de proponer (control barajado
mal escrito; P4 refutada: un valor 0 no veta a la boca frente al impulso, fallo de política; trampa 3 confirmada: veneno 6.3×
más encontrado que comida; primera cruzada transitoria). **Lectura del diseñador, que comparto:** el mundo vivo compra
ESTRUCTURA, no regla — disuelve el XOR necesidad × estímulo porque lo mete en la forma de la memoria; el cuello de construir el
rasgo desde píxeles sigue intacto; su valor es un criterio de éxito que no es un acierto sino estar vivo. Semillas cuando toque:
181–200 (réplica 201–220). Queda en diseño hasta el veredicto de XOR.


### Creador A (18 sep 07:00): criba previa al bloque 3 — **la fisión de v11 como creadora de rasgos está en el azar (P0·P1 nunca es el par más propuesto, 0/20; rango mediano 8 de 15); el estadístico de pureza (unique cue) también cae (mejor honesto 10/20, 0.625), tras un artefacto propio detectado y declarado** → no se gasta el bloque 3/3 en eso; los cuatro mecanismos de la sala pasarán por la criba (proponer P0·P1 en ≥ 15/20; 1.6 s con el gemelo) antes de preregistrar

Criba con instrumento existente + gemelo (20 corridas, 1.6 s): de cada fisión salen los 3 pares del patrón que causó el conflicto;
`P0·P1` es el par más propuesto en **0/20** semillas. Pureza del refuerzo bajo el par: primera medida 17/20 y 1.000 era un **artefacto**
(con `nmin = 4` sólo 3 de 300 pares eran elegibles y el empate en −∞ daba la victoria al índice 0 = `0x1`; regla 5 en acto);
con desempate al azar: pureza 0/20 (0.469), media de R 10/20 (0.625). **Mapa completo del mundo de 8 patrones, todo medido:**
correlación con el residuo (estadístico ideal) 3/20 · fisión 0/20 · pureza/media 10/20 · normas ≤ 0.625 · gradiente exacto 0.562 ·
retropropagación 0.531; razón estructural: 9 de 15 candidatos ajustan el tren con residuo 0. Recomendación del creador (pendiente
de la decisión del director sobre el criterio, opción A/B): criba a los mecanismos del enjambre; si ninguno la pasa, cerrar con el
mínimo `ntr` con el que el organismo generaliza (1.000 con 14 patrones, n* = 200).


### ERR-33 y ERR-34 confirmados por el auditor (18 sep 07:05): **reales en código; ERR-34 con consecuencia medida CERO sobre N3d (CONV restringido a los 4 objetos comunes: 0.826 contra 0.512 de SOLO_R, gana 8/8) — el veredicto "transfiere entre sensores por conducta" sobrevive intacto; nota en N3d, no reescritura**

`mundo_social_n3.py:44-45` (`_reaparece` sortea de `self.tipos`, no de `fijos`: `regen_rota` descarta `tipos_fijos`; **no toca N3d**, que nunca
activa `regen_rota`) y `:47-51` (`nobj = nobj_por_org·n` y `spawn()` consume `fijos` en orden: SOLO_R con n = 1 recibe 4 de los 8 objetos
que reciben CONV/SHUF/SACIEDAD con n = 2). El auditor reprodujo 8 semillas en el scratchpad (acierto idéntico dígito a dígito al JSON
registrado) y recalculó CONV sólo sobre los 4 objetos comunes: mediana 0.826 contra 0.512 de SOLO_R, gana 8/8, como sin restringir.
**Nota a las tres series de N3d (61–80, 81–100, 101–120):** los brazos con n distinto vieron conjuntos de objetos distintos (4 contra 8);
el acierto compara bien (el receptor es ciego en los dos y el resultado se mantiene sobre los comunes); **las comparaciones de
EXPOSICIONES entre brazos con n distinto quedan inválidas** hasta fijar `nobj_por_org` por brazo (perilla en `mundo_social_pred`, en
curso por el creador C). Verificación: `AUDITORIA_madrugada18_20260918.md`, sección "mundo_social_n3 (ERR-33/34)".


### ERR-35 — DECISIÓN DEL DIRECTOR (18 sep 2026, 07:10): **el criterio de parada de XOR se reformula después de ver datos (por eso lleva número): la línea XOR se cierra declarando el MÍNIMO de ejemplos con el que el organismo generaliza, no como fracaso**

Motivo (medido, creador A, §A12–A13): con 8 patrones de entrenamiento, **9 de los 15 rasgos conjuntivos posibles ajustan los datos con
residuo cero y sólo uno generaliza** — ningún aprendiz (local, con retropropagación o con gradiente exacto: 0.562 / 0.531 medidos) puede
elegir entre nueve hipótesis empatadas salvo por un prior; con 14 patrones queda una sola. El criterio original (0.75 en xor01 con 8
patrones) exigía adivinar una moneda; mantenerlo habría llevado a concluir "techo de la arquitectura" cuando el techo es del examen.
Palabras del director: *"es esperar que mi hijo haga pan solo con haberme visto dos veces"*.

**Criterio nuevo (firmado por el director):** la línea XOR se cierra declarando el mínimo número de ejemplos distintos con el que el
organismo aprende XOR con reglas locales y lo generaliza a los nunca vistos. **Ya medido:** con **14** patrones de entrenamiento la
regla local con competencia llega a **1.000** en los 6 nunca vistos con n* = **200** exposiciones (`xor_6_s101-120`); con 11, 0.625; con 8,
0.500 (nadie puede). **Vocabulario:** *"XOR se aprende con reglas locales cuando el mundo da 14 ejemplos distintos; con 8 no lo aprende
nadie, porque 9 de 15 hipótesis explican los datos igual de bien."* **El bloque 3/3 se corre igual**, con el mejor mecanismo de la sala
de agentes que pase la criba (proponer `P0·P1` en ≥ 15/20), y con `ntr = 14` como control obligatorio: si cruza 0.75 con 8 patrones,
se declara **prior estructural** (con el control `azar` ∈ [0.35, 0.65] y `px0` = 1.000), no "aprende XOR"; si sube con 8 y no con 14,
es un ajuste al régimen y se dice. Nada más se recalibra. Siguiente peldaño tras el bloque 3: el mundo vivo (línea F), donde el
significado por necesidad da ejemplos distintos sin pedirlos.


### Bloque C-P6 (lateral, un bloque; 18 sep 06:37; semillas 121–140): N2 por predicción en el mundo "decidible" — **NULO para la pregunta principal (N6) por la propia cláusula del creador: la banda G-c se leyó en N0 (0.835) cuando había que leerla en el brazo sin canal y sin competidor, SOLO_R = 0.986, fuera de banda por arriba: el mundo se aprende solo y el canal sólo ahorra mordidas (109 contra 188.5); N6′ (emparejada por mordidas) no calculable porque el runner no guardó `curva_rec` (ERR-36). Sobreviven N1 y N4. Línea lateral cerrada.**

Preregistro `experimentos/creacion_C/PREREGISTRO_n2pred.md` (36e077f8871dbbe6); instrumento `mundo_social_pred` (277b6978ad47a492; perillas
`regen_en_fijos`/`nobj_total` apagadas ≡ actual, identidad L1/L2/L3 63/63 en la copia principal y en el runner) + `mundo_vd`; datos
`n2pred_s121-140_20260918_062737` (68f3b18377730b44), 240 corridas, 9.6 min; réplica 141–160 lanzada por la regla 12 (N6 cruda con pareado
14/20 en el umbral) antes de conocer la nulidad: vale sólo como dato de N1/N4.

| brazo | acierto hablando | acierto MUDO | mordidas hasta criterio |
|---|---|---|---|
| N0 (dos forrajeadores, sin canal) | 0.835 | 0.835 | 129.5 |
| **SOLO_R (uno, sin canal)** | **0.986** | 0.986 | 188.5 |
| INNATO | 0.968 | 0.976 | 107.5 |
| PRED | 0.955 | 0.988 | **109.0** |
| SHUF (control) | 0.728 | 0.983 | 850 (2 censuradas) |
| SACIEDAD (control) | 0.800 | 0.997 | 541 (1) |

Lo que el runner imprimió: N6 cruda OK (0.988 ≥ 0.835 + 0.10; 14/20), N6b INNATO 0.976, N1 **19/20**, N2′ NO (109 contra 129.5, ≤ 0.70× no;
12/20), N3 OK, N4 **SHUF 19/20 y SACIEDAD 18/20**, N5 OK, G-e 1.20 ≤ 1.5 (el confuso del humo no se sostiene). **Lo que decide (`analiza_n6prima.py`,
63aeb82daf5f0a83, escrito por el creador contra su propio bloque):** (1) N6′ no es calculable: `corre_n2pred.py` no devolvía `curva_rec`
(**ERR-36**, instrumento; runner parcheado a 286a5bb2d71962b4 para el futuro; la réplica en curso tampoco la lleva); (2) SOLO_R 0.986 supera
a N0 y a PRED (−0.031): el mundo se aprende solo; el canal sólo ahorra mordidas (−42 % frente al receptor solo, −16 % frente a N0);
(3) N0 < SOLO_R sin canal en ninguno porque en N0 hay dos forrajeadores sobre 8 objetos (`nobj_total` arregló ERR-34 y creó "objetos
distintos por organismo": dilema estructural, no ajuste); (4) G-c mal leída → **serie nula para N6**: con el receptor resolviendo solo,
"retiene tras el silencio" no distingue aprender del canal de aprender solo. **Sobrevive:** N1 (el significado se aprende por predicción
con la magnitud del mundo: u = +0.80 / −0.38, 19/20) y N4 (el canal sólo enseña cuando la conducta ajena informa). **Qué haría falta
(no hoy):** bajar el techo de SOLO_R a la banda (más objetos que vistas-tiempo o menos pasos), leer G-c en SOLO_R y guardar `curva_rec`.
Línea lateral cerrada (revisión de rumbo 06:45): N2 sigue sin mundo donde medir retención sin morder; lo que queda es el
resultado de significado por predicción (N1) y el diseño del mundo que lo haría decidible.


### C-P6, réplica automática 141–160 (regla 12; 18 sep 06:48): **lo que sobrevivía tampoco replica — N1 (significado) 13/20 (se exigían 15), N4 SACIEDAD 15/20 (se exigían 18); SOLO_R 0.983 otra vez fuera de banda → N2 por predicción queda SIN resultado firme en este mundo**

Datos `n2pred_s141-160_20260918_063750` (301e5c4359382aca). N1 19/20 en 121–140 contra 13/20 en 141–160: la magnitud del significado
(`u ≈ +0.80 / −0.38`) no es robusta entre rangos de semillas; N4 SHUF 18/20 se sostiene, SACIEDAD cae a 15/20. Veredicto del runner:
*"refutado en la raíz: el receptor no aprende el significado"*. **Lectura honesta:** con el mundo fuera de banda (el receptor aprende solo) ni
siquiera el aprendizaje del significado se puede afirmar; la línea N2 vuelve al estado de antes de la noche — cerrada con dos mundos —
más lo aprendido sobre el instrumento (ERR-32, ERR-33, ERR-34, ERR-36 y el teorema de la retina de 6 px). Nada se declara.


### BLOQUE 3 de 3 del criterio de parada (XOR; 18 sep 07:43; semillas 121–140): **M3 "memoria de un golpe por combinación" CRUZA con 8 ejemplos — 1.000 en los 12 nunca vistos (puntuación del registro Y estricta), abre (P0, P1) en la sonda 20/20, n* = 7 exposiciones, con desempate al azar (X4: índice 1.000 = azar 1.000), px0 = 1.000, azar 0.500, y con 14 patrones también 1.000 → se declara PRIOR ESTRUCTURAL (candidatos = pares de píxeles), no aprendizaje de la estructura. Réplica 141–160 en curso.**

Preregistro `experimentos/creacion_A/PREREGISTRO_xor_7.md` (3ebde4f9d433b477; escrito antes de correr por el creador A sobre el ganador de
la sala); instrumento `organismo_g3A` (6e7d80db210b1950; por anclas desde `organismo_g3` del mini-equipo 3 de la sala, 91eb167023cb37b7;
perillas `mem_apriori` —lectura en la sonda— y `mem_desempate='azar'`; identidad 10/10 + 3/3 en el runner); datos
`xor_7_s121-140_20260918_073918` (a7f65e09b47b25ae), 360 corridas, 4 min. Mecanismo: 15 celdas de dos canales, una por par de píxeles,
con 4 casillas de valor (una por combinación de los dos píxeles); la primera mordida de una combinación escribe R de un golpe (sin
tasa, sin tope); cada celda lleva su error propio (EMA); la vía lenta lee sólo la celda de menor error; abstención (0) en combinaciones
nunca vistas. Memoria: 15 × (4 + 1) escalares. Señal: el refuerzo de la propia mordida y nada más. Constantes del tronco v14.1.

| brazo (xor01, 8 tren / 12 nunca vistos) | registro | ESTRICTA (abstención = fallo) | gana (0,1) en la sonda | n* (≥ 0.75) | px0 / azar |
|---|---|---|---|---|---|
| M3 (desempate por índice, como la sala) | 1.000 | 1.000 | 20/20 | 10 | 1.000 / 0.500 |
| **M3_AZAR (decide)** | **1.000** [0.81, 1.00] | **1.000** | **20/20** | **7** | 1.000 / 0.500 |
| M3_NTR14 (control de prior: 14 tren / 6 test) | 1.000 | 1.000 | 20/20 | 7 | 1.000 / 0.500 |
| M4 (tabla por grupos, búsqueda ciega) | 1.000 | 1.000 | — | — | 1.000 / 0.550 |
| REF (v13q6 + WTA, el mejor local anterior) | 0.500 | 0.500 | 14/20 | > 600 | 1.000 / 0.500 |
| SIN_SEL | 0.469 | 0.469 | 0/20 | > 600 | 1.000 / 0.500 |

X1 OK (1.000 ≥ 0.75; > REF 20/20), X2 OK (estricta 1.000 ≥ 0.60), X3 OK (20/20), **X4 rigging OK** (|índice − azar| = 0), X5 OK (con 14: 1.000
≥ 0.90), X6 OK (px0 1.000; azar 0.500 en banda). Cláusula de muestreo: 2/20 semillas sin una clase mordida (iguales en todos los brazos).
Cobertura de la celda ganadora 4/4. La predicción del creador (≥ 0.94 registro, ≥ 0.75 estricta) se cumple con exceso.

**Lectura (ERR-35, letra acordada):** con 8 ejemplos no se puede *seleccionar* el rasgo (9 de 15 hipótesis empatan); lo que M3 hace es
**no elegir**: guarda el valor de cada combinación de cada par la primera vez que la muerde y responde con el par que menos se equivoca.
Es un **prior estructural** (los rasgos que importan son pares de píxeles co-activos), declarado como tal, no "aprende XOR": los
nunca vistos se aciertan porque comparten la combinación (P0, P1) con los vistos. Con ese prior bastan **7 exposiciones** (el gradiente
exacto necesitaba 10 con los rasgos dados; el tronco, > 600). Dos grupos independientes de la sala (uno desde la plasticidad de un
disparo, BTSP; otro desde una búsqueda ciega de 432 reglas con semillas retenidas) convergieron en "escribir de un golpe la primera
vez". **Vocabulario:** *"con 8 ejemplos XOR exige un prior de pares, y con él bastan 7 exposiciones; con 14 ejemplos no hace falta
prior (1.000 con la regla local y competencia, 200 exposiciones)"*. Los dos enunciados son compatibles y los dos son resultados.
**Qué falta:** réplica 141–160 (en curso); llevar la memoria por pares a la vía lenta del tronco (copia por anclas de `organismo_v14`)
con examen v3'' completo, generalización y recuperación intactas → candidato a **v15**, decisión del director.


### LÍNEA XOR CERRADA (18 sep 2026, 07:47) — réplica del bloque 3 en 141–160: **X1–X6 OK otra vez (1.000 registro y estricta; gana (0,1) 20/20; rigging 0; con 14, 1.000; px0 1.000; azar en banda; n* = 10)** → dos series independientes. Declaración final con la letra de ERR-35

Datos `xor_7_s141-160_20260918_074208` (025029d3ea223a36). Cláusula de muestreo: 4/20 semillas sin una clase mordida en todos los brazos
de M3 (5–6 en REF/SIN_SEL); no altera los criterios (se reporta).

| enunciado (nivel 3, no lineal) | evidencia |
|---|---|
| **Con 8 ejemplos XOR exige un prior de pares, y con él bastan 7–10 exposiciones** | M3 (memoria de un golpe por combinación, desempate al azar): 1.000 / 1.000 en 121–140 y 141–160; n* = 7 y 10; abre (P0, P1) en la sonda 40/40; rigging 0; azar 0.50 |
| **Con 14 ejemplos no hace falta prior: la regla local con competencia llega a 1.000 en los nunca vistos** | A-6: 1.000, n* = 200 (bloque 2); M3 con 14: 1.000, n* = 7–10 |
| **Con 8 ejemplos no lo aprende nadie sin prior** | 9 de 15 hipótesis con residuo 0; estadístico ideal 3/20; gradiente exacto 0.562; retropropagación 0.531; fisión 0/20 (bloques 1–2 y criba) |
| Las dos constantes de la vía lenta ya están en el tronco (v14.1) | 0.625 → 1.000 con rasgos dados; sin coste (examen 8/8 ×2, G1 1.000) |

Vocabulario permitido: *"con 8 ejemplos XOR exige un prior de pares (candidatos = pares de píxeles co-activos), y con él bastan 7–10
exposiciones; con 14 ejemplos no hace falta prior"*. Prohibido: "aprende XOR", "entiende la combinación". Lo que sigue: candidato a
**v15** (la memoria por pares en la vía lenta del tronco: examen, generalización y recuperación intactas; paquete en preparación)
y el **mundo vivo** (línea F). Bloques de la línea XOR esta noche: 3, 3b, 3d, trío, 3e (día 7) · A-4, A-6, bloque 3 (madrugada) ·
control positivo, criba y sala de 19 agentes. ERR de la línea: 30, 31, 35.


### MUNDO VIVO (línea F; primer bloque; 18 sep 07:58; semillas 181–200): **el núcleo se sostiene — el organismo aprende un VALOR POR NECESIDAD que resuelve el XOR necesidad × estímulo (1.0, 20/20), un valor escalar no lo hace (0.5, 20/20) y barajar el contenido lo destruye (20/20); la tabla 2 × 4 se aprende con error 0 en ~11 exposiciones — pero las predicciones de supervivencia (P4′, P7) y la del estímulo que no informa (P6) NO se cumplen como estaban escritas**

Preregistro `experimentos/nivel11_mundo_vivo/PREREGISTRO_mundo_vivo.md` (+ enmienda 1 del diseñador y aclaración del coordinador antes de
correr: P5 se lee sobre la celda más lenta real de v14); instrumento `organismo_vivo` (20c0961c79de8825; por anclas desde v14.1 con 20
sustituciones; **identidad 37/37** en la copia principal y 15/15 dentro del runner, incluido el control que debe fallar); runner
`corre_vivo.py` (0bce2ae090fcb0a7; umbrales con la frase literal del preregistro); datos `vivo_s181-200_20260918_075215`
(3d9a7d3b7c8a9c54), 140 corridas, T = 100 000, 5 min. Diseño: dos necesidades (hambre, sed) con dos muertes, cuatro estímulos
(comida, veneno, agua, sal), consecuencia vectorial, sorpresa específica por necesidad, valor por estímulo y necesidad.

| brazo | xor01 (necesidad × estímulo) | celdas estrictas | exposiciones hasta la tabla | peor error de casilla | muertes [energía, agua] |
|---|---|---|---|---|---|
| V14 (ancla: una necesidad) | 0.5 | 2/4 | — | 2.5 | 139 [139, 0] |
| **VIVO** | **1.0** | **4/4** | **11** | **0.00** | **97 [53.5, 48]** |
| UNA_NEC | 0.5 | 2/4 | — | 0.13 | 135.5 [43.5, 89] |
| ESCALAR (valor promedio) | 0.5 | 2/4 | — | 1.90 | 152.5 [70, 83] |
| BARAJA_CON (contenido barajado) | 0.5 | 3/4 | 10 | 1.72 | 157 [79.5, 78] |
| BARAJA_POL (política barajada) | 1.0 | 4/4 | 7.5 | 0.00 | 364.5 [176.5, 186.5] |
| NO_INFORMA (sal nunca informa) | 1.0 | 3/4 | — | 0.00 | 39.5 [39.5, 0] |

P1 **PASA** (20/20, mediana 1.0); P2 **PASA** (ESCALAR 0.5, pareado 20/20); P3a **PASA** (contenido barajado 0.5, 20/20); P3b **PASA** (política
barajada: muertes ×3.76, 18/20; xor intacto); P9 **PASA** (VIVO no paga en exposiciones: 4.0 = 4.0). **P5 PASA con la lectura aclarada**
(celda más lenta real de v14 = A, 4 exposiciones → umbral 12; exp_tabla 11; 20/20 con las 4) y **falla con la letra** ("(B)" = 2 → umbral 6):
error de redacción declarado antes de correr, no de criterio. **P4′ NO:** VIVO muere menos que UNA_NEC (0.72×) y que ESCALAR (0.64×) y la
mitad por agua (0.54×) — las medianas cumplen, pero el pareado exige ≥ 16/20 en los tres y da 11 / 17 / 20. **P7 NO:** las muertes por agua
de UNA_NEC son 1.85× las de VIVO (se exigía ≥ 2×; pareado 10/20). **P6 NO:** la sal nunca cruza criterio (censurada 20/20, como se
predijo) pero |W| llega a 1.83 (se exigía ≤ 0.3): **el organismo asigna valor a un estímulo que nunca informa** — hallazgo, no ruido
(superstición por co-ocurrencia con la necesidad activa; se estudia aparte). **Lectura honesta (regla 12: P4′ y P7 no están a ±1
semilla; no hay réplica automática):** el mundo vivo hace lo que prometía en lo cognitivo — valor por necesidad, XOR natural, tabla
exacta, en pocas exposiciones — y sus predicciones de supervivencia eran demasiado finas para 20 semillas (direcciones correctas,
márgenes no). Lo que sigue: réplica del núcleo en 201–220 con la misma letra, y un preregistro nuevo para la supervivencia y la
superstición de la sal (no una enmienda sobre estos datos). El organismo v14.1 no cambia; el mundo vivo queda como instrumento y
peldaño (línea F) para la siguiente sesión. Vocabulario: *"en un mundo con dos necesidades el organismo aprende qué vale cada cosa
para cada necesidad, y con eso resuelve el XOR necesidad × estímulo en 11 exposiciones; un valor único no puede"*.


### ERR-37 (diseñador del mundo vivo, 18 sep 08:10) y hallazgo de ALIAS DE CÓDIGO: **las tres predicciones caídas eran errores de medida (umbral pareado puesto en la mediana del efecto; muertes no pareables por semilla; `max` sobre 40 lecturas) y la "superstición de la sal" no es superstición: con K = 3 la sal y el veneno tienen el MISMO código en 2/20 semillas y el veneno paga el precio (−1.83 en vez de −3.00)**

**ERR-37a:** P4′ exigía ≤ 0.75 y la mediana pareada es 0.739; P7 exigía ≥ 2× y la mediana pareada es 1.99: un umbral en la mediana parte la
muestra por la mitad por construcción (11/20, 10/20 no miden nada). El efecto es grande: A₁₂ = 0.90 (VIVO contra UNA_NEC), 0.935 (contra
ESCALAR), 0.955 (muertes por agua); q75(VIVO) 106 < q25(UNA_NEC) 125 < q25(ESCALAR) 143. **ERR-37b:** las muertes son la integral de una
trayectoria que diverge desde el primer paso: la semilla fija KW y el flujo, no la supervivencia — pareado válido para lo aprendido,
no para las muertes. **ERR-37c:** `|W| ≤ 0.3` con `max` sobre 40 lecturas es un estadístico de extremos (mediana 0.0; 18/20 semillas 0.0
exacto). **Enmienda 2** (`PREREGISTRO_mundo_vivo.md` f87cafa631a6b31c; escrita después de 181–200 y antes de 201–220, declarándolo): P4″
por medianas, A₁₂ y cuartiles; P7′ con umbral por debajo de la mediana observada; P6′ ≥ 18/20; y **P10, la que puede fallar limpio**: en
201–220 no hay ninguna semilla con alias de código (calculado antes de correr con `diagnostico_codigos.py`), luego `err_peor` de VIVO debe
ser 0.00 en 20/20.
**Alias de código (hallazgo, `PREREGISTRO_supersticion_sal.md` b803b20128ade9ea):** las dos semillas con valor en la sal (182, 188) son
exactamente las dos con `|code(sal) ∩ code(veneno)| = 3`: el mismo código de Kenyon; y el valor es el mismo número (`W_hambre[veneno] =
W_hambre[sal] = −1.83` y −1.34). La puerta presta la evidencia por código, la división por conflicto no repara (exige `R ≠ 0` y la sal
da `R = 0`; sal muda → 0 divisiones), la evitación cierra el bucle (exposiciones ×8). **Consecuencia:** un estímulo que no informa le
quita al organismo el 40–55 % del miedo a lo que sí lo mata cuando comparten código. Las tres hipótesis del coordinador (co-ocurrencia
con la necesidad, sorpresa específica, drenaje) quedan refutadas con el mismo dato (`W_sed[sal] = 0.0`; `eta_pred = 0`; `lam` sólo actúa al
morder). Bloque aparte preregistrado: 9 semillas ALIAS y 9 LIMPIAS elegidas estructuralmente en 301–700, seis predicciones (S-5 es la
del coordinador y puede tumbar la del diseñador: sin sed la superstición debe seguir igual). **Nivel del brief:** no cierra ninguno; nivel
8 recibe el primer mundo con más de una dimensión de valor; **nivel 9 sube a 30 %** (allostasis mínima medida; el organismo puede
equivocarse de objetivo); nivel 4 recibe el negativo del alias de código; el XOR necesidad × estímulo no toca el nivel 3 (se resuelve
indexando la memoria, no leyendo mejor los píxeles). Réplica 201–220 con la enmienda 2 → en cola tras v15c.


### Candidato v15c — la memoria de un golpe por combinación en la vía lenta del TRONCO (18 sep 08:06): **NO ENTRA AL TRONCO — sustituye la lectura lineal y rompe la generalización lineal del tronco (batería de generalización con la memoria ON: G1 px0 0.500, G2 0.513; se exigían ≥ 0.80 / ≥ 0.85); en el mundo de regla sí hace lo suyo (xor01 0.812 estricta contra 0.438 sin memoria) → queda como ÓRGANO DEL MUNDO DE REGLA (cláusula §5), como A avisó antes de correr**

**ENMIENDA (18 sep 08:46, ERR-38):** la V2a que sostenía "rompe la generalización lineal" corrió con la vía lenta lineal APAGADA
(la batería copiada omitió `eta_s`/`clip_s`); repetida con la batería corregida: **G1 1.000 / G2 0.997 — v15c NO rompe la
generalización lineal**. Su V1 nunca se midió con la perilla encendida (defecto 1 de A). Queda SUPERADO por v15d, cuyo examen
encendido sí se midió y cae por reversión. El "no entra" se mantiene, pero por falta de medida válida, no por G1.

Preregistro `experimentos/creacion_A/PREREGISTRO_v15c.md` (d6904b21e19905e3); instrumentos por anclas desde v14.1 `organismo_v15c` (0d2ae9c54a3a8c53;
perilla `memoria_pares`; identidad 32/32 en la copia principal: 24/24 ≡ v14.1, el rng no se consume con la perilla apagada, 6/6 mundo
de regla ≡ v14g), `organismo_v15c_on`, `organismo_v15gc`, `bateria_v15c`, `bateria_generaliza_v15c`; datos `v15c_s121-140_20260918_075817`
(91091a293dd66192) con `regresion_generaliza_organismo_v15c_on_20260918_080307` (a634d0a770ff6401), 8 min.

| medida | con memoria (ON) | sin memoria (v14.1) | umbral |
|---|---|---|---|
| V2a generalización del tronco (`bateria_generaliza`, 101–120): G1 px0 / G2 | **0.500 / 0.513** (px0 > azar 4/20) | 1.000 / 0.967 | ≥ 0.80 / ≥ 0.85 → **NO** |
| V2b mundo de regla (121–140): xor01 registro / estricta | **0.812 / 0.812** (gana (0,1) 20/20) | 0.438 / 0.438 | ≥ 0.75 → sí |
| V2b px0 | 0.900 | 0.900 | = 1.000 → NO (también sin memoria: umbral mal puesto para v15gc) |
| V2b azar | 0.500 | 0.500 | en banda |
| V4 celdas / divisiones | 62 | 68 | ±10 % → OK |
| V1 examen v3' (corrido con la perilla apagada por el runner: sólo re-verifica v14.1) | — | 8/8 | no mide al candidato (defecto del runner, se anota) |

**Lectura:** la memoria por pares responde con la casilla del par ganador y **abandona la lectura lineal**: en el mundo del tronco, donde
las reglas son de un píxel, eso destruye la generalización (0.500 = azar). Es exactamente lo que A avisó en el humo (px0 0.90 → 0.80 con
una semilla) y por la cláusula del preregistro **no entra al tronco**. El órgano vale en el mundo de regla (xor01 0.81 estricta en el
tronco extendido; 1.000 en el instrumento de la sala). **La variante honesta es OTRO mecanismo, para un preregistro nuevo:** que la vía
lenta SUME lineal + memoria, o enrute por cuál tiene menos error (con abstención de la memoria en combinaciones no vistas) — así el
tronco conserva la lectura lineal donde basta y usa la tabla de pares donde no. También se anota: el runner corrió V1 con la perilla
apagada (no mide al candidato) y el umbral px0 = 1.000 de V2b no lo cumple ni v14.1 en ese mundo (0.900): dos defectos de runner/umbral
que no cambian el veredicto (V2a decide). v14.1 sigue de tronco.


### MUNDO VIVO, réplica 201–220 con la enmienda 2 (18 sep 08:20): **el núcleo REPLICA (P1 20/20, P2 20/20, P3a 20/20, P3b ×3.9, P5 20/20, P9) y las predicciones de supervivencia corregidas (ERR-37) PASAN en las DOS series; P10 —la que podía fallar limpio— se cumple: sin semillas con alias de código, la sal vale 0 en 20/20 y el error de casilla es 0.00 en 20/20 → la explicación por alias de código queda confirmada por predicción**

Datos `vivo_s201-220_20260918_080619` (e1e932387b411a3e), 140 corridas, 5 min; análisis `analiza_vivo_enm2.py` (ef7588acfa19535e; regla 10:
lee los JSON de las dos series; salida `analiza_vivo_enm2_salida.json`).

| predicción (enmienda 2) | 181–200 | 201–220 |
|---|---|---|
| P4″a muertes VIVO / UNA_NEC ≤ 0.85 y / ESCALAR ≤ 0.80 (razón de medianas) | 0.716 / 0.636 ✅ | 0.718 / 0.588 ✅ |
| P4″b A₁₂ (probabilidad de que VIVO muera menos) ≥ 0.75 / 0.80 | 0.900 / 0.935 ✅ | 1.000 / 1.000 ✅ |
| P4″c q75(VIVO) < q25 de los dos | 106 < 125 < 143 ✅ | 99.8 < 125.8 / 149.2 ✅ |
| P7′a muertes por agua UNA_NEC / VIVO ≥ 1.6 y ≥ 1.5 en ≥ 16/20 | 1.854; 18/20 ✅ | 2.047; 19/20 ✅ |
| P7′b cuartiles de agua | 50 < 84 ✅ | 50.2 < 79.2 ✅ |
| P6′ sal sin valor en ≥ 18/20 (mediana ≤ 0.1; censurada 20/20) | 18/20 (máx 1.83 en las 2 alias) ✅ | **20/20, máx 0.0** ✅ |
| P10 sin alias → err_peor 0.00 en 20/20 | n/a (2 alias) | **PASA** ✅ |

Ambigüedades de la letra resueltas reportando las dos lecturas (razón de medianas y mediana de razones; cuartiles exclusive e
inclusive): todas pasan. Los pareados de la letra vieja (14/18/20; 11/20) siguen siendo la moneda de ERR-37a, no una medida.
**Declarable (línea F, nivel 8/9):** *en un mundo con dos necesidades el organismo aprende qué vale cada cosa para cada necesidad y con
eso resuelve el XOR necesidad × estímulo en 11 exposiciones (dos series, 20/20); un valor único no puede; sobrevive más (muere un 28–41 %
menos y la mitad por sed) y no atribuye valor a lo que no informa salvo cuando el código de tres celdas lo confunde con el veneno
(alias)*. Instrumento y peldaño para la siguiente sesión (propósito y reproducción como medida). Bloque de la sal: corre ahora.


### Bloque de la sal — ALIAS DE CÓDIGO (nivel 4; 18 sep 08:16; 9 semillas ALIAS y 9 LIMPIAS elegidas estructuralmente en 301–700): **CONFIRMADO — el valor espurio de un estímulo que no informa aparece sólo cuando su código de tres celdas coincide con el de un estímulo con valor consolidado (|W[sal]| 1.45 contra 0.0), el veneno paga (−1.45 contra −3.0), la evitación multiplica ×7 las exposiciones y no hay divisiones; NO depende de la sed (S-5: persiste sin sed, 1.62) y la puerta de v13 NO lo repara (S-6: 1.48)**

Preregistro `experimentos/nivel11_mundo_vivo/PREREGISTRO_supersticion_sal.md` (b803b20128ade9ea; selección de semillas por diagnóstico estructural
recalculada dentro del runner: coincide 9/9 y 9/9); runner `corre_sal.py` (bfdc00bb48656337; identidad 5/5); datos `sal_alias9_20260918_081346`
(d521f569205ebcfd), 36 corridas, 2 min.

| brazo (9 semillas) | |W[sal]| mediana | W[veneno] mediana | exposiciones a la sal | divisiones | muertes |
|---|---|---|---|---|---|
| S1-ALIAS (sal y veneno con el mismo código) | **1.45** | **−1.45** | 3 835 | 0 | 75 |
| S1-LIMPIA (códigos distintos) | **0.0** | **−3.0** | 545 | 0 | 35 |
| S2-SIN-SED (alias, una sola necesidad) | 1.62 | −1.62 | 3 814 | 0 | 75 |
| S3-PUERTA (alias, puerta de v13 por celdas) | 1.48 | −1.71 | 2 895 | 0 | 69 |

S-1 PASA (9/9 y 9/9), S-2 PASA (el veneno paga: 9/9 y 9/9), S-3 PASA (evitación ×7, 9/9), S-4 PASA (0 divisiones 9/9: la división por conflicto
no puede actuar con R = 0). **S-5 NO por la letra** (±0.3 en 5/9; medianas 1.62 contra 1.45) **pero en la dirección que refuta la hipótesis del
coordinador**: sin sed la superstición persiste igual o mayor — no es la necesidad, es el código. **S-6 NO:** la puerta por celdas de v13 no lo
reduce (1/9) — la puerta por evidencia del código no es parte del bucle; basta el alias. **Lectura:** con K = 3 celdas de 90, dos estímulos
pueden recibir el mismo código (2 de 20 semillas con cuatro estímulos); entonces el que no informa hereda el valor del que sí, y el que sí
lo mata pierde la mitad del miedo, y como el organismo evita el código, nunca corrige. Es una **propiedad estructural del código del
tronco** (v9–v14.1), invisible con dos estímulos y visible con cuatro: cabo abierto del nivel 4 (memoria/capacidad) para la siguiente sesión
(desambiguar códigos: más celdas por código, K mayor, o un tercer canal que distinga estímulos con el mismo código). Nada entra al tronco.
Vocabulario: *"cuando dos cosas se parecen tanto que reciben el mismo código, el organismo teme a las dos a medias"*.


### Nota a v15c (18 sep 08:25): defecto latente corregido — colisión de nombre `_ev` en `organismo_v15c` (con `puerta_pat > 0` y la memoria encendida lanzaría `TypeError`); la batería V2a de v15c completó sus 40 corridas con salida completa (acc, celdas, divisiones) y sin excepciones: su veredicto (G1 0.500) se mantiene. Constructores v15c/v15d reconstruidos con el arreglo (`_ev` → `_erv`). v15d (perilla `memoria_pares` = 'suma' | 'ruta'): examen CON la perilla encendida (corrige el segundo defecto de v15c); identidad 32/32 del creador; humo: 'suma' devuelve px0 a 1.000 (v15c 0.70–0.90) y xor01 0.875 estricta; avisos escritos antes de correr: `azar` con 'suma' 0.700 en una semilla (control que puede tumbarlo) y celdas 33 contra 62 (V4 probablemente cae).


### ERR-38 (coordinador, 18 sep 08:44): **la batería de generalización copiada por anclas para v15c y v15d omitió `eta_s=0.15` y `clip_s=10` — V2a corrió con la vía lenta lineal APAGADA; los G1/G2 de v15c y de v15d (0.500/0.513 los dos) se ANULAN; con la batería corregida los dos generalizan (G1 1.000)**

La entrada nueva `'organismo_v15c_on'` / `'organismo_v15d_on'` de `bateria_generaliza_v15c/v15d.py` llevaba `dict(puerta=3, mask_rel=2, …)`
con el comentario "eta_s/clip_s por defecto = v14.1"; pero el gemelo de generalización (`organismo_v14g` y sus copias `organismo_v15gc_on`,
`organismo_v15gd_on`) tiene `eta_s=0.0, clip_s=3.0` por defecto — la entrada del tronco `'organismo_v14'` los pasa explícitos (0.15 / 10).
Con `eta_s=0` la lectura lineal no aprende y el valor a priori en los nunca vistos queda al azar. **Cómo se detectó:** 6/40 filas de la
V2a de v15d idénticas hasta el 16.º decimal a las de v15c (dos organismos distintos no dan lo mismo si la lineal contribuye) → revisión de
las kw. **Corrección:** `construye_v15c.py` / `construye_v15d.py` (la entrada lleva `eta_s=0.15, clip_s=10.0`), baterías regeneradas
(`bateria_generaliza_v15d` 2a36df3ac43b49bf → ee4c9214310de717; `bateria_generaliza_v15c` 644843ae9e3b625b → e28932bfbcb92eab; organismos y
baterías de examen con el mismo sha). Datos anulados: `regresion_generaliza_organismo_v15c_on_20260918_080307`,
`regresion_generaliza_organismo_v15d_on_20260918_083404` (se conservan como evidencia del error). Repetición (101–120, 20 semillas):

| candidato (memoria ON) | G1 px0 | azar | px0 > azar | G2 px0 | azar | K | datos |
|---|---|---|---|---|---|---|---|
| v15d `suma` | **1.000** | 0.600 | 19/20 | **0.999** | 0.557 | 20/20 | `regresion_generaliza_organismo_v15d_on_20260918_084412` (4b9a36a127a2c2ea) |
| v15c `sustituye` | **1.000** | 0.400 | 19/20 | **0.997** | 0.502 | 20/20 | `regresion_generaliza_organismo_v15c_on_20260918_084524` (820369ed5555ee73) |

**Verificación independiente (creador B, 08:50, con los kwargs exactos de la batería, semilla 101, px0):** `Wps = [0, …, 0]` y
`mem_vistas = 0` — con `eta_s = 0` ni la lineal aprende NI la tabla de pares se escribe: las V2a anuladas midieron la vía rápida sola.
**Consecuencia:** la memoria de pares NO rompe la generalización lineal del tronco (cualquier par que contenga el píxel de la regla la
generaliza); el veredicto de v15c queda enmendado (arriba) y superado por v15d. **Regla derivada (EQUIPO 14):** una entrada nueva en una
batería copiada por anclas se compara campo a campo con la entrada del tronco; "por defecto" no existe cuando el módulo es un gemelo
con sus propios defaults.

### Candidato v15d — la memoria de pares que SUMA o ENRUTA (18 sep 08:38; V2a corregida 08:46): **NO ENTRA AL TRONCO — conserva la generalización lineal (V2a 1.000 / 0.999) y cruza XOR con 8 ejemplos (V2b 0.875 estricta), pero el EXAMEN cae: la tabla escrita de un golpe no se desdice cuando la regla cambia (E2 0/20: come B en Q4 en 1/20) y, al explicar la recompensa desde la primera mordida, deja a la vía rápida sin consolidar (E1 W_B ≈ −3 en 0/20 con conducta 17/20; E2L 10/20)**

Preregistro `experimentos/creacion_A/PREREGISTRO_v15d.md` (87b18228df6cd222; enmienda 1 = ERR-38, sólo instrumento, umbrales intactos);
instrumentos por anclas desde v14.1: `organismo_v15d` (f2f0b06e31877e96; perilla `memoria_pares = None | 'suma' | 'ruta'`, apagada ≡ v14.1
bit a bit sin consumir rng), `organismo_v15d_on` (e57d0677cdff3906), `organismo_v15gd` (4720721d775eec29), `organismo_v15gd_on`
(a1863e095fb5d1b5), `bateria_v15d` (707299a585572ce9; examina al candidato ENCENDIDO — corrige el defecto 1 de v15c),
`bateria_generaliza_v15d` (ee4c9214310de717 tras ERR-38); runner `corre_v15d.py` (78d0a04c39c27a76); identidad **32/32** (I1 24/24, I2 rng
no consumido 2/2, I3 6/6); datos `v15d_s121-140_20260918_082846` (e1ad17cfdb97512b), examen `examen_v15d_20260918_083108.log` (sólo log: **ERR-42**, la batería copiada calculaba el sha de `organismo_v11.py` con la ruta de
`creacion_A/` y lanzaba excepción después de escribir el veredicto; los conteos del log son válidos, el JSON por corrida se perdió), V2a `regresion_generaliza_organismo_v15d_on_20260918_084412` (4b9a36a127a2c2ea).

| criterio (escrito antes) | resultado | veredicto |
|---|---|---|
| V1 examen v3′ 8/8 en 101–120, perilla ON (`suma`) | E1 0/20 (W_B ≈ −3: 0/20; veneno Q4 < Q1: 17/20) · E2 0/20 (W_A → −3: 0/20; W_B → +1: 1/20; come B Q4 ≥ 50: 1/20) · E2L 10/20 · E2I/E2J/E2K 20/20 · 2, 3′, 3″, 4a–4d pasan | **FALLA** |
| V2a generalización ON: G1 ≥ 0.80, G2 ≥ 0.85, K 20/20 | G1 1.000 (azar 0.600, 19/20) · G2 0.999 (azar 0.557, 20/20) · K 20/20 (tras ERR-38) | PASA |
| V2b mundo de regla 121–140: xor01 estricta ≥ 0.75; px0 ≥ apagada; azar ∈ [0.35, 0.65] | xor01 `suma` 0.875 / `ruta` 0.844 / apagada 0.438 (gana (0,1) 20/20) · px0 1.000 / 0.900 / 0.900 · azar 0.500 / 0.450 / 0.500 | PASA |
| V3 `n*` | no medible con los instrumentos de hoy (declarado en el runner) | — |
| V4 coste ±10 % | celdas xor01 56 (`suma`) contra 68 (apagada): −18 %; muertes 246 contra 280 | NO (A lo avisó antes) |

Cláusula §5/§6: si V1 o V2a caen, no entra → **no entra**. **Lectura honesta:** A acertó en lo que predijo (sumar conserva la lineal: V2a
pasa una vez corregido el instrumento; `ruta` queda por debajo de `suma` en xor01) y su aviso de coste se cumplió; lo que nadie había
escrito es la REVERSIÓN: una memoria de un golpe por combinación guarda la primera recompensa y no la corrige cuando el mundo cambia,
y como explica la recompensa desde la primera mordida, la vía rápida deja de recibir error y no consolida (E1). Vocabulario permitido:
*"la memoria de pares generaliza y cruza XOR con 8 ejemplos, pero no se desdice"*. Prohibido: buscar modos intermedios sobre estos
datos (§6). Siguiente candidato legítimo, con preregistro NUEVO: **tabla reescribible** (la casilla sigue a la última recompensa, o se
borra cuando su error propio sube) — v15e, creador A. Notas de instrumento (sin ERR: no cambian ningún umbral): la etiqueta "perilla
APAGADA" de la ETAPA 2/5 en el log del runner es texto heredado del runner de v15c (`bateria_v15d` importa `organismo_v15d_on`, líneas
98 y 111); el JSON del examen no se escribió por ERR-42 (ruta de `organismo_v11.py` en la batería copiada, corregida en
`bateria_v15e`), no por la batería congelada — corrección del 18 sep 09:35 a la nota escrita a las 08:46.


### Bloque B-5 — DESAMBIGUAR CÓDIGOS (nivel 4; creador B; 18 sep 09:07; ALIAS 326–670 y LIMPIAS 307–342 del bloque de la sal): **8 de 9 criterios pasan — el alias se repara sin tocar el tronco (examen 8/8 y generalización IDÉNTICOS a v14.1); C4 (dónde cae la primera división) queda a una semilla del umbral (7/9) → réplica automática en semillas nuevas (regla 12)**

Mecanismo (uno, local, sin memoria ni constantes nuevas, rng intacto): la división por conflicto de v11 se dispara también cuando una
celda consolidada (`|Wb[c]| > 0.2`), bajo una retina distinta (`kj@P > KW[c]@P`), recibe `R = 0`; la hija nace sin valor y la madre
conserva el suyo. En los mundos del tronco `R ∈ {+1, −3}` → inerte por construcción. Perilla `desambiguar = 0 | 1`. Preregistro
`experimentos/creacion_B/PREREGISTRO_codigo.md` (218b5eefbf2d552f); instrumentos por anclas (`construye_codigo.py` f94aa0a2f714c28d):
`organismo_v14_codigo` (a4eeca90fb605c78) / `_on` (2f7794d92e68cc89), `organismo_v14g_codigo` (ae9231070a95c801) / `_on` (7a1628b6e6a37f86),
`organismo_vivo_codigo` (839fa71f9c84cb26), `bateria_v14_codigo` (875727174447b01a; examina al `_on`), `bateria_generaliza_codigo`
(8669053f71fa76ef; entrada campo a campo igual a la del tronco, regla 14); runner `corre_codigo.py` (cb91371b77c079d3); identidad
**42/42** (I1 24/24 ≡ v14.1, I2 rng 2/2, I3 6/6 ≡ v14g, I4 10/10 ≡ `organismo_vivo`) + **I5 inercia con la perilla ON 30/30** + I6 (debe
fallar) falla. Negativo estructural (`negativo_codigo.py`, semillas 1–200, sin simular): en el mundo de 4 estímulos algún par de
estímulos comparte código en **18/200** semillas (9 %; B–D 5 %, C–D 4 %); en el mundo de regla (20 patrones) **170/200** semillas tienen
algún par idéntico y en 135/200 un patrón nunca visto lee exactamente la celda de uno entrenado (291 fugas, 115 de valencia opuesta).
Datos `codigo_alias9_20260918_085958` (369d784c65e036b1; 63 corridas, T = 100 000), examen `examen_codigo_20260918_090300`
(1c9aa3a3d87173d6), generalización `regresion_generaliza_codigo_organismo_v14_codigo_on_20260918_090557` (ed4d5d25e9eb2ad7).

| brazo (n = 9) | \|W[sal]\| | W[veneno] | exposiciones a la sal | divisiones (por R = 0) | celdas | muertes |
|---|---|---|---|---|---|---|
| D0-ALIAS (v14.1) | 1.45 | −1.45 | 3 835 | 0 | 30 | 75 |
| **D1-ALIAS** | **0.0** | **−3.0** | **517** | 7 (7) | 37 | **41** |
| D0-LIMPIA / D1-LIMPIA | 0.0 / 0.0 | −3.0 / −3.0 | 545 / 545 | 0 / 3 | 30 / 33 | 35 / 35 |
| D1-SINSED (tronco, 4 estímulos) | 0.0 | −2.9 | 414 | 7 | 37 | 42 |
| D0-VIVO / D1-VIVO (la sal informa la sed) | 1.69 / 3.0 (W_s) | −1.61 / −3.0 | 3 833 / 1 936 | 3 / 10 | 33 / 40 | 146 / 90 |

| criterio | resultado | veredicto |
|---|---|---|
| G guardas: D0 ≡ JSON del bloque de la sal | 18/18 | PASA |
| C1 D1-ALIAS \|W[sal]\| ≤ 0.3 en ≥ 8/9, mediana ≤ 0.1 | 9/9, mediana 0.0 | PASA |
| C2 W_hambre[veneno] ≤ −2.8 en ≥ 8/9 y ≤ −2.5 en 9/9 | 9/9 y 9/9 (mediana −3.0) | PASA |
| C3 evitación: exposiciones ≤ 1.5 × limpias en ≥ 8/9 | 517 contra 545, 9/9 (v14.1: ×7) | PASA |
| C4 causa: `des_splits ≥ 1` 9/9 y primera división por R = 0 en una mordida de D en ≥ 8/9 | 9/9 y **7/9** | **NO (a una semilla)** |
| C5 coste: celdas ≤ 45 en 18/18, mediana ≤ 40 | 18/18, mediana 35, máx. 39 | PASA |
| C6 limpias sin regresión | 9/9 y 9/9 (3 divisiones por R = 0 de agua/sal, sin daño) | PASA |
| C7 sin sed (tronco con 4 estímulos) | 9/9 y 9/9 | PASA |
| C8 tabla 2×2 exacta con la perilla; falla sin ella | ON 9/9; OFF falla 9/9 | PASA |
| C9 muertes ≤ 0.8 × D0-ALIAS | 41 contra 75 (0.547; A₁₂ 1.0) | PASA |
| T1 examen v3′ 8/8 ON y `splits` por etapa idénticos a v14.1 | 8/8; 6/6 idénticas | PASA |
| T2 generalización ON: G1 1.000, G2 0.967, K 20/20; filas idénticas a v14.1 | 40/40 idénticas | PASA |
| T3 coste en el tronco | 0 % exacto (T1 y T2 son identidad) | PASA |

**Lectura:** el alias se repara con una sola regla local que en el tronco no actúa nunca (inercia medida, no supuesta): el estímulo que
no informa se queda sin valor, el veneno conserva el miedo, la evitación desaparece (×7 → ×1) y las muertes bajan a la mitad; en el
mundo vivo con la sal informando la sed, la tabla 2×2 sale exacta 9/9. Lo que falla es sólo la LETRA de la causa: en 2/9 semillas la
primera división por R = 0 ocurre en una mordida de agua/sal antes que en la de D. Por la regla 12 (a una semilla del umbral) se corre
**réplica en semillas nuevas** elegidas estructuralmente antes de correr (enmienda 1: ALIAS 779, 796, 822, 852, 895, 916, 917, 926, 944;
LIMPIAS 703, 712, 717, 725, 728, 744, 746, 751, 764; mismos umbrales; T1/T2 no se repiten por inercia exacta; guarda G′ en vez de G).
**Nada se declara hasta la réplica.** Vocabulario provisional: *"cuando una celda con valor recibe nada bajo una retina distinta,
divide: el código deja de prestar valor"*. Predicción de B cumplida en 8/9 (predijo C1–C2 9/9, C3 400–700, C6 9/9, C9 40–50, T1–T3
identidad); C4 no como se escribió.


### Bloque B-5, RÉPLICA en semillas nuevas (18 sep 09:12; ALIAS 779–944 y LIMPIAS 703–764 elegidas estructuralmente antes de correr): **PASA — DECLARADO (nivel 4): "cuando una celda con valor recibe nada bajo una retina distinta, divide: el código deja de prestar valor". El alias de código se repara con una regla local que en el tronco no actúa nunca. C4 (dónde cae la primera división) 4/9: ese criterio estaba mal escrito como marca de causa**

Runner `corre_codigo_replica.py` (reutiliza las funciones y umbrales de `corre_codigo.py`; enmienda 1 del preregistro, escrita antes);
guarda estructural: las 9 primeras ALIAS y LIMPIAS del rango 701–1100 recalculadas coinciden; datos `codigo_replica_alias9_20260918_091133`
(83577dbe1323bfbe; 63 corridas, T = 100 000, 40 s con Pool(14)). T1/T2 no se repiten (inercia exacta medida en la serie 1).

| brazo (n = 9) | \|W[sal]\| serie 1 → réplica | W[veneno] | exposiciones a la sal | divisiones por R = 0 | celdas | muertes |
|---|---|---|---|---|---|---|
| D0-ALIAS (v14.1) | 1.45 → **1.72** | −1.45 → −1.72 | 3 835 → 3 718 | 0 → 0 | 30 → 30 | 75 → 77 |
| **D1-ALIAS** | **0.0 → 0.0** | **−3.0 → −3.0** | **517 → 475** | 7 → 7 | 37 → 37 | **41 → 41** |
| D1-LIMPIA | 0.0 → 0.0 | −3.0 → −3.0 | 545 → 522 | 3 → 4 | 33 → 34 | 35 → 43 |
| D1-SINSED | 0.0 → 0.0 | −2.9 → −2.92 | 414 → 397 | 7 → 7 | 37 → 37 | 42 → 47 |
| D0-VIVO / D1-VIVO | 1.69 / 3.0 (W_s) → 1.85 / 3.0 | −1.61 / −3.0 → −1.79 / −3.0 | 3 833 / 1 936 → 3 685 / 1 994 | 3 / 10 → 2 / 8 | 33 / 40 → 32 / 38 | 146 / 90 → 141 / 91 |

Criterios en la réplica: G′ 9/9 y 9/9 · C1 9/9 (mediana 0.0) · C2 9/9 y 9/9 · C3 9/9 (475 contra 522) · **C4 9/9 y 4/9 (NO)** · C5 18/18
(mediana 35, máx. 39) · C6 9/9 y 9/9 · C7 9/9 y 9/9 · C8 ON 9/9, OFF falla 9/9 · C9 41 contra 77 (0.532; A₁₂ 1.0). Veredicto por la
letra de la enmienda 1: **PASA** (G′ y C1–C3, C5–C9). **Lectura de C4:** la primera división por `R = 0` cae en una mordida de agua o
de sal indistintamente (4/9 en D; 7/9 en la serie 1): el criterio marcaba *dónde* cae la primera división, no *si* la división de la
celda de la sal ocurre y deja el valor en 0 — eso sí ocurre 18/18 (C1). Queda anotado para reescribirlo como criterio de causa en el
siguiente preregistro de esta línea (la división de la celda compartida por D precede a la caída de `|W[sal]|`). **Declarable:**
*con K = 3 dos estímulos pueden compartir código; cuando una celda con valor consolidado recibe R = 0 bajo una retina distinta,
divide, la hija nace sin valor y el código deja de prestar valor: el estímulo que no informa queda en 0.0, el veneno conserva −3.0,
la evitación cae de ×7 a ×1 y las muertes a la mitad (18/18 semillas ALIAS en dos series); en el tronco la regla no actúa nunca
(examen y generalización idénticos a v14.1)*. Nivel 4 → 75 %. **Candidato a v15 ("división por R = 0", perilla `desambiguar`):
la entrada al tronco la decide el director** (`registro/PROPUESTA_v14.md`). Pendiente de la línea: réplica con `R = 0` ruidoso
y alias de magnitud (regímenes que hoy no existen), y el gemelo compilado.


### Mundo vivo, peldaño 2 — PROPÓSITO Y REPRODUCCIÓN COMO MEDIDA (diseñador; 18 sep 09:16; semillas 221–240): **LA MEDIDA SE TIRA — `descendientes_viables` (ventana de 500 pasos con energía y agua ≥ 1) no ordena los brazos como la supervivencia: ESCALAR y BARAJA_CON hacen más "descendientes" que VIVO muriendo 1.5× más (P-R1 < 0.50, cláusula escrita antes). Nada más se declara. Lo reportado sin interpretar: la tercera necesidad ("reproducirse") cambia UNA conducta — saciado, deja de morder la sal (0.80 → 0.007) — y leer el mínimo de las dos filas existentes (CUELLO_MIN, sin memoria nueva) lo hace igual o mejor → la tercera fila SOBRA (Occam)**

Preregistro `experimentos/nivel11_mundo_vivo/PREREGISTRO_reproduccion.md` (§1–10 antes del humo; enmienda 1 = **ERR-39**: el control de Occam
CUELLO leía UNA fila y dejaba invisible el veneno — control de paja — y se añadió CUELLO_MIN antes del bloque, sin cambiar umbrales);
instrumento por anclas `organismo_vivo_rep.py` (aa823d56c2d4213c; perilla maestra `reproduccion=0` ≡ `organismo_vivo` bit a bit; medida de
sólo lectura; `rep_nec` = tercera fila de valor cuyo cuerpo es `min(E, Ag)`; `rep_coste` paga E y Ag por descendiente); arnés
`identidad_vivo_rep.py` **52/52** (+ 15/15 dentro del runner); runner `corre_vivo_rep.py` (d8ff689c6dd544d0); datos
`vivo_rep_s221-240_20260918_091428` (4a3096492a1ddcfc; 180 corridas, T = 100 000, 2 min con Pool(14)); subconjunto limpio n = 19 (alias
estructural 236 excluido): mismo cuadro.

| brazo (n = 20) | descendientes (mediana) | viable | muertes [E, agua] | xor01 | sac_tasa[D] (sal, saciado) |
|---|---|---|---|---|---|
| VIVO (organismo_vivo) | 20.0 | 0.356 | 100 [53.5, 49.5] | 1.0 | 0.797 |
| REP_SIN_COSTE (tercera necesidad) | 55.0 | 0.549 | 75 [30, 44] | 1.0 | **0.007** |
| REP (paga 0.4 / 0.4) | 54.5 | 0.495 | 107 [47, 60.5] | 1.0 | 0.007 |
| CUELLO (una fila: control de paja, ERR-39) | 6.5 | 0.328 | 96.5 | 1.0 | 0.269 |
| **CUELLO_MIN (mínimo de las dos filas, sin memoria nueva)** | **65.5** | 0.555 | 76 [32.5, 39] | 1.0 | **0.001** |
| UNA_NEC | 13.0 | 0.231 | 137.5 | 0.5 | — |
| ESCALAR | **36.0** | 0.468 | **149.5** | 0.5 | — |
| BARAJA_CON | **39.5** | 0.486 | **159.5** | 0.5 | — |
| BARAJA_POL | 1.0 | 0.378 | 372.5 | 1.0 | — |

| predicción (escrita antes) | resultado | veredicto |
|---|---|---|
| P-R1 la medida ordena como la supervivencia (A₁₂ ≥ 0.70 en cuatro pares; < 0.50 → se tira) | VIVO > UNA_NEC 0.93 · UNA_NEC > BARAJA_POL 1.0 · **VIVO > ESCALAR 0.007** · **VIVO > BARAJA_CON 0.0** | **SE TIRA LA MEDIDA** |
| P-R2 saciado veta la sal | VIVO 0.797 → REP 0.007 (A₁₂ 1.0) | pasa (reportado) |
| P-R3 rinde sin pagar / P-R4 pagando | 55 contra 20 (A₁₂ 1.0; ×2.75); REP 0.99 × REP_SIN_COSTE | pasan (reportado) |
| P-R5 / **P-R5b** Occam | CUELLO 6.5; **CUELLO_MIN 65.5 > 55 (A₁₂ 0.146)**, veta la sal 0.001, comida y agua A₁₂ 1.0 | **la tercera fila sobra** |
| P-R6 seguridad (xor01, celdas, exposiciones, muertes) | 20/20, 20/20, ×1.0; muertes A₁₂ 0.966 | pasa (reportado) |
| P-R7 tabla de la fila 2 | 12/20 y 16/20 (se exigían 18/20) | NO |
| P-R8 coste en el mundo | sal ×1.9, comida ×0.69 | NO |

**Lectura honesta:** la ventana de viabilidad cuenta "cuerpo lleno 500 pasos seguidos" y un organismo que se atraca y muere más la
cumple más veces: no es una medida de reproducción ligada a la supervivencia, y el preregistro la mató solo (P-R1). Lo que sí se vio
(sin declarar): valor por el cuello de botella `min(E, Ag)` = *saciado, no muerdas lo que no informa* (la sal cae de 0.80 a 0.00) — y
no hace falta una necesidad nueva para tenerlo: CUELLO_MIN lo saca de las dos filas que ya existen. Siguiente (preregistro nuevo,
semillas 261–280, **ERR-40**: medida no ligada a la supervivencia): medida que no pueda premiar morir (descendientes por vida, o
descendientes con coste contados sólo si el cuerpo sigue vivo Y pasos después), CUELLO_MIN contra tercera necesidad contra VIVO,
mismos controles. Nivel 9 sigue en 30 % (propósito medido como conducta, no como medida de reproducción). Sin ERR nuevo por el
resultado (es una refutación, no un defecto).


### ERR-41 (creador A, 18 sep 09:30) y ERR-42 (creador A, verificado por el coordinador 09:35): dos defectos de los instrumentos copiados de v15c/v15d

**ERR-41 — el mundo de regla (V2b) de v15c y v15d corrió en configuración tipo v13, no v14.1:** `corre_v15c.py`/`corre_v15d.py` pasaban
`eta_s=0.15, puerta=3` solos, y el gemelo g pone por defecto `clip_s=3.0, mask_rel=0, puerta_pat=0` (v14.1: 10, 2, 5). Los veredictos V2b
(v15c 0.812; v15d `suma` 0.875 / `ruta` 0.844 estricta) valen como "mundo de regla en configuración v13 + memoria de pares", no como
"tronco v14.1 + memoria". No se repiten: v15c y v15d ya no entran por V1. `corre_v15e.py` pasa los kwargs exactos del tronco (`KW14`).
**ERR-42 — el JSON del examen de v15c/v15d no se escribió:** `bateria_v15c.py`/`bateria_v15d.py` (copias por anclas de `bateria_v14`)
calculaban `h16(AQUI/organismo_v11.py)` con `AQUI = creacion_A/`, donde ese archivo no existe → excepción **después** de escribir las
líneas del veredicto; los conteos del log (`examen_v15d_20260918_083108.log`) son válidos y el JSON por corrida se perdió. La nota del
registro de las 08:46 que lo atribuía a la batería congelada queda corregida. `bateria_v15e` lee los sha desde `organismo/`. Regla 14
ampliada: toda batería copiada pasa un humo que llegue a ESCRIBIR su JSON antes de la serie.


### Candidato v15e — la tabla de pares REESCRIBIBLE, cada vía con su error (creador A; 18 sep 09:37; V1/V2a 101–120, V2b 141–160 con los kwargs exactos del tronco): **NO ENTRA (cláusula §7) — arregla lo que mató a v15d: se DESDICE (E2 reversión 20/20) y la vía rápida CONSOLIDA (E1 W_B ≈ −3 20/20), conserva la generalización lineal (G1 1.000 / G2 0.997), pero PIERDE XOR (0.500 estricta contra 0.438 apagada; se exigía ≥ 0.75), como A dejó escrito como refutación posible: una tabla que guarda lo que a la lineal le falta hereda el fracaso de la lineal**

Diagnóstico de v15d (A, líneas de `organismo_v15d.py`): la lineal aprendía de `R − (lineal + tabla)` calculado ANTES de que la tabla
escribiera `R` de un golpe → tras UNA mordida la vía lenta leía 1.45·R (−4.35; medido −4.22/−3.72), la probabilidad de morder caía 220×,
no había más mordidas, el exceso no se corregía (E1) y tras el cambio nadie mordía B (E2); `mem_alfa = 1` sobre v15d da los mismos
números — la reescritura sola no toca la primera escritura. **v15e:** rápida con su error; lineal con su error `R − lineal`; la tabla
escribe DESPUÉS del paso de la lineal el residuo `R − lineal_después` por sobrescritura; abstención; ganadora por menor error propio.
Preregistro `experimentos/creacion_A/PREREGISTRO_v15e.md` (8fb7ddcdeb086089; §1–§7 antes de medir); instrumentos por anclas
`organismo_v15e` (5930c5ed2df1be1d) / `_on` (c576d0de467d7cca), `organismo_v15ge` / `_on`, `bateria_v15e` (d5039d16ce21920d), `bateria_generaliza_v15e`
(b01142827847c7d7; entrada campo a campo = tronco, regla 14), runner `corre_v15e.py` (18a588dcba5cf547; kwargs del tronco en V2b: ERR-41);
identidad **32/32**; datos `v15e_s141-160_20260918_092921` (90e851dff9cafeca), examen `examen_v15e_20260918_093053` (91c2127c0958781a; JSON
escrito: ERR-42 corregido), V2a `regresion_generaliza_v15e_organismo_v15e_on_20260918_093352` (b9300ad10f01694b).

| criterio | resultado | veredicto |
|---|---|---|
| V1 examen v3′ 8/8 ON | **E1 19/20** (venenoQ4<Q1 19/20; **W_B ≈ −3: 20/20**), **E2 20/20** (W_A → −3, W_B → +1, come B Q4 ≥ 50: 20/20 — la REVERSIÓN que v15d tenía en 0/20), **E2I 19/20** (W_C ≤ −2.5 19/20), E2J/E2K/E2L 20/20; 2, 3′, 3″, 4a–4d pasan | 6/8: **NO** (dos escenarios a una semilla) |
| V2a G1 ≥ 0.80, G2 ≥ 0.85, K 20/20 | G1 1.000 (azar 0.450, 20/20) · G2 0.997 (azar 0.469, 20/20) · K 20/20 | PASA (veredicto de la batería; ver ERR-43) |
| V2b mundo de regla 141–160 (kwargs del tronco): xor01 estricta ≥ 0.75; px0 ON ≥ OFF; azar en banda | **xor01 0.500 [0.06, 0.88] contra 0.438 apagada** (gana (0,1) 20/20, cobertura 4/4) · px0 1.000 / 1.000 · azar 0.500 / 0.500 | **NO** |
| V4 ±10 % | xor01 celdas +9 %, splits +18 %; px0 −2 % / −5 % | NO (por arriba en xor01; A esperaba incumplir por abajo) |

**Lectura:** v15e resuelve la reversión y la consolidación en 20 semillas — lo que ninguna memoria de pares había hecho — y lo hace
exactamente por la razón que A escribió: cada vía con su error. Y pierde XOR por la razón que también escribió (§6c): con residuos,
el error propio de la celda buena (0,1) ya no es 0 sino la deriva de una lineal que no puede con XOR, del mismo orden que la
confusión de las celdas malas → el prior de pares pierde su identificabilidad. Vocabulario: *"una tabla que guarda lo que a la lineal
le falta se desdice, pero hereda el fracaso de la lineal"*. Los dos escenarios a una semilla (E1, E2I 19/20) no se replican: v15e
cae por V2b de todos modos. **Siguiente candidato legítimo (preregistro nuevo, A16 del PUENTE): v15f — R crudo en la tabla (no el
residuo), sobrescritura, relevo a la lineal por abstención, cada vía con su error.** Encargado 09:45.

**ERR-43 (coordinador, 09:40):** la ETAPA 5 de `corre_v15e.py` leyó el conteo K (20) como mediana de `azar` y declaró "V2a NO"; el
veredicto de la batería (`K_cobertura=True G1_valor=True G2_conducta=True`, azar 0.450/0.469) es el que vale. Ningún umbral cambia; el
runner de v15f debe leer los campos de la batería, no reconstruirlos del log.

### Revisor de literatura (18 sep 09:45; `registro/investigacion/LITERATURA_novedad_20260918.md`): **ningún mecanismo nuevo; lo publicable es una nota técnica con código y datos**

Veredictos, citas verificadas por ficha de editor (no por PDF): alias de código = colisión de un hash sensible a la localidad
(Dasgupta, Stevens & Navlakha 2017) + generalización de la extinción (Rescorla 1976) + aliasing perceptual (Whitehead & Ballard 1991)
+ protección por evitación (Lovibond 2009) → **ya existe**; reparación por R = 0 = distinción útil (McCallum 1993) / match tracking
de ARTMAP (Carpenter, Grossberg & Reynolds 1991) / neurogénesis → **ya existe**; identificabilidad de XOR con 8 = necesidad de sesgo
(Mitchell 1980) → **ya existe**; prior de pares = unique cue / configural cue / tile coding → **ya existe**; memoria de un golpe por
combinación = control episódico sobre BTSP (Bittner 2017; Wu & Maass 2025) → **existe en parte** (el ensamblaje con n* medido en un
organismo con consecuencias no está reportado así); no desdecirse = tabla de máximos de MFEC (Blundell 2016) corregida por NEC
(Pritzel 2017) → **ya existe**; valor por necesidad = RL homeostático (Keramati & Gutkin 2014), Cañamero 1997/2004, Senapati 2019 →
**ya existe** (y recomienda no llamarlo "XOR": infla). **Aporte publicable:** nota técnica reproducible sobre la línea del alias
(necesidad medida + reparación con identidad bit a bit en el tronco) y un benchmark de método "ejemplos y exposiciones hasta asociar".
**Errata:** la cita "Milstein et al. 2024" de `ENJAMBRE_xor_20260918.md` §1 no existe con esa autoría; es Wu & Maass 2025 (*Nat Commun*
16:342); anotado al final del informe. Las demás citas del enjambre quedan sin verificar.


### Mundo vivo, peldaño 2, BLOQUE 2 — crecimiento neto del linaje y lectura pesimista saciado (diseñador; 18 sep 09:43 y réplica 09:45; semillas 261–280 y 281–300): **8/8 predicciones en las dos series — DECLARADO: la medida `r = descendientes − muertes` ordena los brazos como la supervivencia (ERR-40 resuelto), y leer el MÍNIMO de las dos filas de valor cuando el cuerpo está saciado (CUELLO_MIN, sin memoria nueva) lleva el linaje al filo del reemplazo (r ≈ 0 en 9–11/20; VIVO −73/−75) por menos muertes y más ventanas; la "tercera necesidad" no aporta nada sobre eso y SE RETIRA (Occam)**

Preregistro `experimentos/nivel11_mundo_vivo/PREREGISTRO_reproduccion_2.md` (1b18b471ee06397e; ERR-40: la ventana de viabilidad premiaba
atracones que mueren más; candidatas comparadas por escrito — `desc/(muertes+1)` falla con el propio dato de 221–240; exclusión tras la
muerte y coste no quitan el atracón — elegida `r = descendientes − muertes` por 100 000 pasos: una muerte financia a lo sumo una ventana,
morir nunca suma; umbral con significado r = 0 = tasa de reemplazo); instrumento por anclas `organismo_vivo_rep2.py` (96feb4918dc5d694;
perilla `rep2` de sólo lectura; apagada ≡ `organismo_vivo`); arnés `identidad_vivo_rep2.py` **60/60** (+ 15/15 en cada runner); runner
`corre_vivo_rep2.py` (10ab45355883d98d); datos `vivo_rep2_s261-280_20260918_094126` (b557dc80e77a43e7) y réplica `vivo_rep2_s281-300_20260918_094323` (3674a46f92a26e9c);
140 corridas de 100 000 pasos por serie; subconjunto limpio (alias estructurales 278 y 286 excluidos) con el mismo cuadro.

| brazo (n = 20) | r serie 1 → réplica | descendientes | muertes | vida mediana | r ≥ 0 |
|---|---|---|---|---|---|
| VIVO (organismo_vivo) | −73 → −75 | 20 | 94.5 | 600 | 0/20, 0/20 |
| **CUELLO_MIN (mínimo de las dos filas, saciado)** | **+3 → −3** | **68** | **65.5** | **827** | **11/20, 9/20** |
| REP_SIN_COSTE (tercera necesidad) | −21.5 → −30.5 | 53.5 | 76 | 755 | 1/20, 0/20 |
| UNA_NEC | −130 → −123 | 12 | 140.5 | 489 | 0 |
| ESCALAR | −121 → −116 | 33.5 | 153 | 284 | 0 |
| BARAJA_CON | −127 → −117.5 | 40 | 164.5 | 281 | 0 |
| BARAJA_POL | −360.5 → −372.5 | 0 | 361.5 | 150 | 0 |

| predicción (escrita antes) | serie 1 | réplica | veredicto |
|---|---|---|---|
| P2-1 r ordena como la supervivencia (A₁₂ ≥ 0.80 / 0.95) | 0.983 · 0.975 · 0.988 · 1.0 | 0.968 · 0.97 · 0.981 · 0.998 | PASA ×2 |
| P2-2 medianas de r dentro del intervalo predicho (≥ 6/7) | 7/7 | 7/7 | PASA ×2 |
| P2-3 mecanismo: r A₁₂(CUELLO_MIN > VIVO) ≥ 0.90, Δ ≥ 40; muertes; descendientes | 1.0, +76; 0.976; 1.0 | 0.965, +72; 0.917; 1.0 | PASA ×2 |
| P2-4 Occam: A₁₂(REP_SIN_COSTE > CUELLO_MIN) ≤ 0.50 | 0.064 | 0.145 | PASA ×2 → la tercera fila se retira |
| P2-5 reemplazo: CUELLO_MIN r ≥ 0 en 2–14/20; los demás 0/20 | 11/20; 0 | 9/20; 0 | PASA ×2 |
| P2-6 saciado: sal VIVO ≥ 0.60; CUELLO_MIN sal y veneno ≤ 0.05 | 0.776; 0.001 / 0.001 | 0.795; 0.001 / 0.0 | PASA ×2 |
| P2-7 diagnóstico de ERR-40: el regalo del renacer financia más ventanas en ESCALAR/BARAJA_CON | 1.0 / 1.0 | 0.968 / 0.983 | PASA ×2 |
| P2-8 seguridad: xor01 1.0 y celdas 4/4 ≥ 18/20; exposiciones | 20/20; sal ×1.65, comida ×0.64 | 20/20; ×1.72, ×0.63 | PASA ×2 |

**Declarable (nivel 9, propósito medido):** *con dos necesidades, el organismo que saciado lee la peor de sus dos filas de valor deja de
morder lo que no informa y lo que envenena (sal 0.80 → 0.00), muere un tercio menos y triplica las ventanas de cuerpo lleno: su linaje,
contado como descendientes menos muertes, queda en el filo del reemplazo (r ≈ 0) donde el tronco pierde 73–75 por cada 100 000 pasos;
ninguna necesidad nueva hace falta para eso*. Lo que NO se declara: "quiere reproducirse", "tiene propósito" (es una lectura, no un
impulso), ni herencia (no nace nadie todavía: la ventana es una medida). La medida r está validada por su propia cláusula en dos
series y sustituye a la ventana de viabilidad (ERR-40). Nivel 9 → 45 %. Siguiente peldaño (preregistro nuevo): población con
herencia (código/valor) y muerte real, con r como medida — exige mundo con varios cuerpos y Pool. Predicciones del diseñador
cumplidas 8/8 ×2 (sus intervalos de P2-2 acertaron las siete medianas dos veces).


### **DECISIÓN DEL DIRECTOR (18 sep 2026, 09:55) — CAMBIO DE RUMBO.** Tras la mañana (cinco bloques preregistrados por hora, dos
resultados declarados, ningún candidato de capacidad al tronco; revisor de literatura: ningún mecanismo nuevo), el coordinador
diagnosticó cuatro cosas mal planteadas y el director decidió: *"Perfecto, hagamos esa modificación y registra todo"*.
Lo que cambia, y lo que no:
1. **Se conserva el método** (preregistro → commit → correr → registrar; ERR numerados; réplica antes de cerrar; regla 12; reglas 1–14 de
   EQUIPO). Es lo que nos salvó cinco veces hoy (ERR-38, 41, 42, 43; la medida de reproducción).
2. **El mundo cambia por uno que obligue a representar:** estímulos compuestos (una "sal" y una "sal rosa": la variante como variable
   del mismo token), más píxeles que 6, recursos que se agotan, veneno que cambia — un mundo donde 16 patrones no basten y donde
   la tokenización, la variable y el desaprender sean necesarios para sobrevivir (ERR-35: el mundo de 16 patrones no contiene la
   información para elegir XOR; no se le vuelve a preguntar lo que no puede responder).
3. **La estructura crece por reglas locales:** el organismo recluta y divide celdas cuando la sorpresa se repite en la misma
   combinación (conjunción por coactividad) y cuando un código con valor recibe otra consecuencia (B-5); ninguna capacidad nueva
   entra como perilla diseñada a mano si puede entrar como crecimiento.
4. **El criterio de tronco cambia:** el examen v3′ 8/8 deja de ser la puerta absoluta (selecciona "no cambies nada": v15d/v15e
   murieron por detalles internos; sólo entró lo inerte). Un candidato nuevo se juzga por **sobrevivir y generalizar en el mundo
   vivo** (muertes, r = descendientes − muertes, nunca vistos, reversión: se desdice, sin alias) con **no regresión CONDUCTUAL** del
   examen (la conducta de cada escenario se conserva; los pesos internos no son puertas). El criterio v2 se escribe en
   `registro/CRITERIO_TRONCO_v2.md` ANTES de juzgar a ningún candidato con él; **v15c/v15d/v15e no se rejuzgan** (regla: no
   recalibrar después de ver datos); v14.1 sigue siendo el tronco hasta que un candidato cruce el criterio v2 en semillas nuevas.
5. **Ejecución:** la SALA 2 (4 diagnósticos, 6 diseños, 12 refutadores, síntesis) entrega el diseño concreto del mundo y del
   crecimiento; de ahí salen los bloques preregistrados, en este orden: (a) `CRITERIO_TRONCO_v2.md`; (b) el mundo que obliga (mundo
   nuevo con v14.1 SIN cambios como control base: si el tronco ya sobrevive ahí, el mundo no obliga); (c) crecimiento estructural
   por sorpresa repetida (crece_codigo) medido en ese mundo; (d) tokens y variables ("sal rosa" cuelga de "sal"; separación cuando
   deja de comportarse igual); (e) población con herencia y muerte real (que viva). Una cosa a la vez en el Pool; réplica antes de
   declarar; "llegar a la frontera es lo primero, que viva lo segundo".

Registro de la conversación (para el cronista): el director dijo *"me fractura la mente lo que decimos … no sé en qué estamos mal, no
sé qué estamos planteando mal, no sé qué debemos cambiar"*; el coordinador respondió con cuatro puntos (mundo demasiado pequeño;
capacidades diseñadas a mano; el examen selecciona "no cambies nada"; medimos una tarea, no una vida) y una recomendación
(conservar el método, cambiar el mundo, dejar crecer la estructura, juzgar por sobrevivir y generalizar); el director: *"Perfecto,
hagamos esa modificación y registra todo"*. Nada de lo medido hasta aquí cambia de veredicto.


### Candidato v15f — tabla de pares con R CRUDO, sobrescritura y RELEVO a la lineal, cada vía con su error (creador A; 18 sep 10:00; V1/V2a 101–120, V2b 161–180 con los kwargs del tronco): **NO ENTRA por la letra del criterio v1 (cláusula §7) — pero es el primer organismo de la línea que GENERALIZA (G1 1.000 / G2 0.998), SE DESDICE (E2 reversión 20/20), CONSOLIDA (E1 W_B ≈ −3 20/20) y CRUZA XOR CON 8 EJEMPLOS EN LA CONFIGURACIÓN DEL TRONCO (xor01 estricta 1.000 contra 0.500 apagado, gana (0,1) 20/20, azar 0.500 en banda). Cae en dos subletras internas del examen (E1 "veneno Q4 < Q1" 17/20; E2I `W_C ≤ −2.5` 17/20) y en el coste de divisiones (+16 %). ERR-44 abajo. Candidato para el CRITERIO DE TRONCO v2 con preregistro nuevo y semillas nuevas**

Preregistro `experimentos/creacion_A/PREREGISTRO_v15f.md` (df7348599aa68333; §1–§7 antes de medir); instrumentos por anclas `organismo_v15f`
(96fc5c5262107850; perilla `memoria_pares = None | 'relevo'`, `mem_alfa = 1.0`; apagada ≡ v14.1 bit a bit) / `_on` (54d6efe0b564113c),
`organismo_v15gf` / `_on`, `bateria_v15f` (d63f5aee558eb6da; sha desde `organismo/`: JSON siempre escrito), `bateria_generaliza_v15f`
(0cd87d2632e0c66a; entrada campo a campo = tronco), runner `corre_v15f.py` (8eae63dc22913e2b; lee `meta.veredictos` de los JSON: ERR-43
cerrado; kwargs del tronco en V2b: ERR-41 cerrado); identidad **32/32**; datos `v15f_s161-180_20260918_095309` (b0c5e28e04c6f3e5), examen
`examen_v15f_20260918_095443` (c72c6ab10186fc7e), V2a `regresion_generaliza_v15f_organismo_v15f_on_20260918_095744` (df042c2c27ce374f).
Mecanismo: tabla 15 pares × 4 casillas con R crudo, sobrescritura en cada mordida; la lenta lee la casilla de la celda ganadora si conoce
la combinación y si no la lineal (relevo); rápida y lineal con su propio error; ganadora por menor error propio; desempate con el rng.

| criterio (v1, escrito antes) | resultado | veredicto |
|---|---|---|
| V1 examen v3′ 8/8 ON | **E1 17/20** (W_A ≈ +1 20/20, **W_B ≈ −3 20/20**; "veneno Q4 < Q1" 17/20) · **E2 20/20** (reversión: W_A → −3, W_B → +1, come B Q4 ≥ 50) · **E2I 17/20** (`W_C ≤ −2.5` 17/20; conducta "tasa A Q4 ≥ 80 % Q2" 20/20) · E2J/E2K/E2L 20/20 · 2, 3′, 3″, 4a–4d pasan | 6/8: **NO** |
| V2a G1 ≥ 0.80, G2 ≥ 0.85, K | G1 1.000 (azar 0.500, 20/20) · G2 0.998 (azar 0.549, 20/20) · K 20/20 | PASA |
| V2b (kwargs del tronco, 161–180): xor01 estricta ≥ 0.75; px0 ON ≥ OFF; azar en banda | **xor01 1.000 [0.25, 1.00] contra 0.500** (gana (0,1) 20/20, cobertura 4/4) · px0 1.000 / 1.000 · azar 0.500 / 0.450 | **PASA** |
| V4 ±10 % | xor01 celdas +7.8 %, **splits +16 %**; px0 −5.6 % / −? | NO (declarado por abajo; salió por arriba) |

**Lectura:** la línea v15c → v15d → v15e → v15f cerró en cuatro pasos exactamente lo que cada refutación pedía: sustituir rompía la
lineal (v15c, mal medido: ERR-38), el error compartido dejaba sin consolidar y sin desdecir (v15d), el residuo perdía la
identificabilidad (v15e), y el R crudo con relevo lo junta todo: **el organismo que aprende una combinación de un golpe, la corrige de
un golpe y sigue leyendo la lineal donde la tabla calla**. Lo que lo tumba en v1 son dos letras que no miden conducta: (a) *"veneno
Q4 < Q1"* presupone aprendizaje gradual — un organismo que aprende el veneno en UNA mordida apenas muerde en Q1 (2 mordidas), la puerta
se abre en Q2 y la rápida consolida después; el total de mordidas de veneno es MENOR que en v14.1 (41–45 contra 47–51 en el humo) pero la
letra mide dónde caen; (b) `W_C ≤ −2.5` es un peso interno con la conducta intacta 20/20. Ninguna se recalibra aquí (regla 3): v15f NO
entra por v1. **ERR-44 (coordinador, 10:05):** el subcriterio E1 "veneno Q4 < Q1" de la batería v3′ no puede distinguir "aprendió en una
mordida" de "no aprendió": para candidatos que aprenden de un golpe hay que medir el total (o la tasa por trimestre contra el tronco),
como hará el criterio v2 (T-E: conducta conservada; pesos internos reportados). **Siguiente:** v15f es el primer candidato que se juzga
con `registro/CRITERIO_TRONCO_v2.md` — completado con la síntesis de la sala 2 — con preregistro nuevo, semillas nuevas y réplica
(examen y generalización en 121–140, mundo vivo 301–320, mundo de regla 181–200). Vocabulario permitido hoy: *"la memoria de pares con
R crudo y relevo generaliza, se desdice y cruza XOR con 8 ejemplos en el tronco"*; prohibido: "entra al tronco" (todavía no).


### BLOQUE 0 — escalar el código (nivel 12, mundo de familias; 18 sep ~14:30; cálculo estructural, 200 semillas por celda, sin simular): **NINGÚN (NK, K) con D = 12 deja el alias exacto por debajo del 1 % — el mejor es 8.5 % (NK 360, K 5), 4× por encima de NKMAX; a NK = 5 760 baja a 0.5 % pero el código ya no agrupa familias. ERR-45: la cláusula "NK/K escalados a alias < 1 %" del bloque 1 y del T-A propuesto es insatisfacible → la línea del alias pasa al ORGANISMO (B-5 y nodo indexado por código y retina), y el mundo de familias declara el alias por semilla en vez de prometer que no existe**

Preregistro `experimentos/nivel12_mundo_familias/PREREGISTRO_bloque0_codigo.md` (§1–7 antes de calcular); `escala_codigo.py` (importa `organismo_v14` para NK/NKMAX/K; verificación P2 15/15 campos contra `DISENO_mundo_grande` §1.1); `escala_codigo_salida.json`. Rejilla NK ∈ {30, 60, 90, 180, 360} × K ∈ {2, 3, 4, 5}, catálogo 8 tokens × 3 variantes (32 estímulos): U1 (alias exacto < 1 %) 0/20 celdas; U2 (alias 2/3 acotado) 6/20; U3 (sim intra − inter ≥ 0.20) 20/20 — la estructura de familias SÍ se lee en el código (+0.31 en el tronco, 200/200). D = 6 tampoco (mejor 5.0 %). Cota optimista (celdas uniformes, sin `cond()`): con las celdas reales el alias sólo puede ser mayor. Predicciones del diseñador: 4/7 en pie, 2 refutadas (U3 no cayó; la similitud cayó 0.059, no 0.10), 1 acertada por la razón equivocada. Consecuencia para el bloque 1: brazos v14.1 y v14.1 + B-5 (`organismo_v14_codigo_on`), alias estructural declarado por semilla; la decisión pendiente del director sobre B-5 (v14.2) pasa a ser necesaria para la línea.


### BLOQUE 1 — el mundo de familias con v14.1 sin cambios (nivel 12; 18 sep 14:52; semillas 401–420; 9 brazos × 20): **INDECISO en la predicción que decide y el INSTRUMENTO cae — nada se declara; ERR-46: las medidas se revisan antes de endurecer el mundo**

Preregistro `experimentos/nivel12_mundo_familias/PREREGISTRO_bloque1_familias.md` (§1–10 congeladas a9d87b87f07b4826); instrumento por anclas
`organismo_familias.py` (b9dd561a0cf056b8; `mundo='AB'` ≡ v14.1 + claves de B-5, valores bit a bit; D = 12, NK 30, K 3, alias declarado por
semilla con el código del bloque 0); identidad 43/43 (+24/24 en el runner); runner `corre_familias.py` (c21b3c38f36cb4c9); datos
`familias_s401-420_20260918_144946` (028e7b39f5461356; 180 corridas, T = 100 000, 2 min).

| brazo | muertes | colateral | omisión | w_var | exp. total | celdas |
|---|---|---|---|---|---|---|
| EXC (v14.1, 4 excepciones) | 2 | 6.0 | 22.5 | 0.000 | 95 | 52 |
| LIN (lector lineal de referencia) | 1 | 2.0 | 4.0 | 0.000 | 62 | 46.5 |
| AZA (control: consecuencias al azar) | 2 | 19.5 | 75.5 | 0.14 | 319 | 61 |
| BAR (barajado) | 4 | 17.0 | 146.5 | 2.79 | 702 | 61.5 |
| EXC-B5 / LIN-B5 | = EXC / = LIN (B-5 inerte sin estímulos neutros: P7a pasa) | | | | | |
| NEU / NEU-B5 (2 estímulos que no informan) | 2 / 2 | 7.5 / 9.0 | 14 / 12.5 | 0.0 / 0.001 | 135 / 170 | 53 / 71.5 |
| V14 (anillo del tronco, referencia) | 133.5 | — | — | — | — | 30 |

P2 (colateral EXC ≥ 2 × LIN y A₁₂ ≥ 0.75): razón **3.0** pero A₁₂ **0.68** → **INDECISO** (zona declarada: endurecer `n_exc` 4 → 8 en 441–460). P3
(`w_var` ≥ 1.0): **NO** (0.000: la vía lenta drena los píxeles de variable, como el diseñador predijo). **P5 cae:** las medidas no ordenan
los cuatro mundos (AZA y BAR tienen más colateral que EXC) → por la letra, primero el instrumento, nada se declara. P7a pasa (B-5
inerte sin R = 0); P7b: con estímulos neutros B-5 no repara (`|W|` de los neutros no baja; celdas 71.5). Lo limpio: la renovación
simétrica quita la trampa 3 (razón de exposiciones veneno/comida 0.99–1.02); el mundo casi no mata (1–2 muertes contra 133.5 del anillo):
**T-A tendrá efecto suelo aquí** (avisado antes de correr). **ERR-46 (coordinador, 14:55):** las medidas `colateral`/`omision`/`w_var` no
separan "aprender la excepción a costa de los hermanos" de "no aprender nada" (AZA/BAR puntúan más colateral que EXC): se rediseñan y
preregistran de nuevo (medida que ordene EXC > LIN y AZA/BAR abajo por construcción), con `n_exc = 8` y semillas 441–460. Ningún umbral
de esta serie se recalibra.


### BLOQUE 1, ENMIENDA 1 (18 sep 15:08; semillas 441–460; `n_exc` 8, `dureza` 4, medida `colateral_n` con ERR-46/47/48/49): **E3 CAE otra vez — nada se declara; la línea del "colateral" se CIERRA como instrumento: tres correcciones seguidas de la medida sin que separe familia real de familia falsa es recalibrar hasta que pase**

Datos `familias_enm1_s441-460_20260918_150719` (507e3ee556e0d593; 100 corridas, 1.4 min); identidad 24/24. EXC: muertes 53, `colateral_n` 0.089
(mediana; E2b exigía ≥ 0.20, refutaba ≤ 0.05: INDECISO), `n_valida` 2.0 (E3 exigía ≥ 4), `apr` 0.59; LIN: 33, 0.000, 3.5, 1.00; AZA: 58.5, 0.125,
1.0; BAR: 83.5, 0.030, 0.0. Lectura honesta: v14.1 aprende sólo el 59 % de las excepciones y con 2 ventanas válidas por corrida la medida
es ruido; el daño a los hermanos existe (0.089 contra 0.000 en LIN) pero pequeño y sin poder. **Decisión del coordinador (15:12):** no se
corrige la medida una cuarta vez. La pregunta "¿el mundo obliga?" se reformula como CAPACIDAD directa (la hipótesis del director): *¿el
organismo generaliza a una variante nunca vista de un token conocido, y separa la variante cuando deja de comportarse igual?* —
preregistro nuevo, medidas C1–C5 de `DISENO_grafo_tokens`, brazos v14.1 / lineal / azar / barajado, semillas 461–480. La renovación
simétrica y `dureza = 4` (31–53 muertes) se conservan como mundo. ERR-46..49 quedan como historial del instrumento fallido.


### BLOQUE 2 — la hipótesis del director medida por conducta: variante nunca vista y variante que deja de comportarse igual (nivel 12; 18 sep 15:49 y réplica 15:52; semillas 461–480 y 481–500; 11 brazos × 20): **REPLICADO — (1) v14.1 sin cambios lee la variante nunca vista desde su token (0.875 en las dos series; lector lineal 1.000; azar 0.5; barajado 0.25–0.31): "sal rosa se marca como sal" es LINEALIDAD, no capacidad nueva; (2) cuando una variante deja de comportarse igual, la separa sólo a medias (4 de 8, y sólo las que ya mordía como comida) y SIN dañar a sus hermanas (daño 0.0 en 14/20 ×2: P-S4 refutada — no hay colateral que medir, el bloque 1 buscaba un fantasma)**

Preregistro `experimentos/nivel12_mundo_familias/PREREGISTRO_bloque2_variante.md` (412538a907d802a0); instrumento por anclas `organismo_familias_b2.py`
(30200bea6a41c3c8; perillas `vira`, `exc_evita`, `reg_b2`; apagadas ≡ `organismo_familias` ≡ v14.1 bit a bit; identidad **63/63** + 18/18 en cada
runner; gemelo `vira=8` ≡ `vira=−8` bit a bit hasta el cambio: el control no puede ser de paja); runner `corre_familias_b2.py` (c8fa05abaec88dac);
datos `familias_b2_s461-480_20260918_154635` (fc3c00b1532cc7bb) y `familias_b2_s481-500_20260918_154930` (0b8565c93055e78c); 220 corridas por
serie, T = 100 000, 2.7 min; alias estructural declarado (19–20/20 semillas con algún par alias; covariable, no puerta).

| predicción (escrita antes) | serie 1 | réplica | veredicto |
|---|---|---|---|
| P-G2 puerta: azar en [0.35, 0.65] | 0.5 | 0.5 | ok |
| P-G1: LIN ≥ 0.75 en ≥ 15/20 | 1.0 (19/20) | 1.0 (20/20) | PASA ×2 |
| P-G3: barajado ≤ 0.35 (la variante lleva la valencia del token siguiente) | 0.25 | 0.31 | PASA ×2 |
| P-G4: v14.1 < LIN en ≥ 14/20 | 0.875 (8/20) | 0.875 (11/20) | INDECISO ×2 |
| P-S1 gemelo idéntico hasta el cambio | 3/3 | 3/3 | ok |
| P-S2: separa ≤ 5/8 y sep ≥ 2 × apr | 4/8, 2.0 | 4/8, 2.0 | PASA / INDECISO (en el borde exacto, avisado) |
| P-S3: separa las que eran comida, no las que eran veneno | 1.0 contra 0.0 | 1.0 contra 0.0 | PASA ×2 |
| P-S4: daño a las hermanas ≥ 0.10 | 0.0 (6/20 > 0) | 0.0 (6/20 > 0) | **REFUTA ×2** |
| P-S5: daño específico de familia | NO | NO | NO ×2 |

**Lectura honesta:** la primera mitad de la hipótesis del director ya la cumple el tronco, y por la razón más barata: el píxel de la
variante nueva pesa cero en la vía lenta y la lectura sale del token (el barajado lo demuestra: 0.25). La segunda mitad —
desaprender la variante que cambió — es donde v14.1 falla a medias: separa 4 de 8, sólo las que ya mordía como comida (la puerta sólo
se abre con mordidas), y retiene la virada al final 0.5. Y no hay daño colateral: aprender que "sal rosa envenena" no estropea a "sal"
ni a "sal gruesa" (daño 0.0). **El bloque 1 buscaba medir un colateral que no existe**; ERR-46..49 quedan explicados por eso. Lo que el
mundo de familias SÍ obliga y v14.1 no hace: separar la variante que vira cuando era veneno (0/8) y desaprender de un golpe. Eso es
exactamente lo que v15f trae (se desdice en una mordida, E2 20/20): **siguiente bloque: v15f en este mundo, brazos S-EXC con
`memoria_pares='relevo'` contra v14.1, misma letra P-S2/P-S3/P-S6, semillas 501–520 y réplica**; predicción del coordinador escrita
aquí antes: v15f separa ≥ 6/8 incluidas las que eran veneno, `sep/apr` ≤ 1.0, retención de la virada ≥ 0.8. Regla 12: P-G4 y P-S2 en el
borde se resuelven con la réplica siguiente, no con más análisis.


### BLOQUE 3 — v15f (memoria de pares con relevo) en el mundo de familias (18 sep 16:12 y réplica 16:16; semillas 501–520 y 521–540; 14 brazos × 20): **REPLICADO — v15f separa la variante que deja de comportarse igual en 7–7.5 de 8 (v14.1: 4 de 8), incluidas las que eran veneno (0.75–0.875 contra 0.0–0.125 de v14.1), y lee la variante nunca vista sin morderla (1.0 / 0.875; los 32 estímulos leen la TABLA, cobertura 4/4 en 17/20). Precio medido: un daño pequeño a las hermanas (0.042 contra 0.000) y retención de la virada 0.625–0.75 (ni la predicción del coordinador ≥ 0.8 ni la del diseñador ≤ 0.5). Nada se declara como capacidad cerrada: los tres puntos quedan en INDECISO/REFUTA por la letra y piden un candidato con más de una ganadora**

Preregistro `experimentos/nivel12_mundo_familias/PREREGISTRO_bloque3_v15f.md` (7178e4479bf26a35); instrumento por dos cadenas de anclas
`organismo_familias_b3.py` (62a1e53b452b078e; identidad **71/71**: apagado ≡ `organismo_familias_b2` 30/30, cadena hasta el tronco 9/9, `relevo`
ON en `mundo='AB'` ≡ `organismo_v15f_on` 17/17 incluido el rng, 8 controles que deben fallar) + 21/21 en cada runner; runner
`corre_familias_b3.py` (8ad387790f145bab; importa los umbrales del bloque 2, no los copia); datos `familias_b3_s501-520_20260918_160841`
(dbe20b7bbb99c950) y `familias_b3_s521-540_20260918_161228` (cf655980b21c429f); 280 corridas por serie, 3.8 min.

| medida | v14.1 (bloque 2, ×2) | **v15f** serie 1 | **v15f** réplica | letra |
|---|---|---|---|---|
| g1 variante nunca vista (1.ª exposición) | 0.875 / 0.875 | **1.0** | 0.875 | P-G1 pasa ×2 |
| separa la variante que vira (de 8) | 4 / 4 | **7.5** (sep/apr 3.0) | **7.0** (3.0) | P-S2 INDECISO ×2 (separa más, no en menos exposiciones) |
| de las que eran veneno | 0.0 / 0.0 | **0.875** | **0.75** | P-S3 REFUTA / pasa (la asimetría desaparece: eso era lo que se buscaba) |
| daño a las hermanas (Δ 10 000) | 0.0 / 0.0 | 0.042 | 0.042 | P-S4 REFUTA ×2 (pequeño pero > 0) |
| retención de la virada al final | 0.5 / 0.5 | 0.75 | 0.625 | ni ≥ 0.8 (coordinador) ni ≤ 0.5 (diseñador) |

**Lectura honesta:** en el mundo de familias la tabla de pares SÍ comprime: los 32 estímulos se agrupan por familia en las 4 casillas de
un par que parte los tokens por valencia, así que v15f lee la variante nunca vista con el R crudo exacto sin morderla y desaprende la
que cambia casi siempre, también cuando era veneno — la mitad de la hipótesis del director que v14.1 no cumplía. El precio: una sola
ganadora de 4 casillas para 32 estímulos deja un daño pequeño a las hermanas y una retención parcial. Predicciones: la del diseñador
sobre velocidad acertó y sobre retención no; la del coordinador sobre cobertura acertó y sobre `sep/apr` y retención no. Por regla 3
nada se recalibra: el siguiente candidato (preregistro nuevo) necesita **varias ganadoras o compuerta contra la lineal** (el nodo por
familia), y el bloque 4 (canal con referencia por señalamiento) puede montarse sobre v15f tal cual, porque ya lee sin morder.


### BLOQUE 4 — canal con referencia por señalamiento, dos organismos v15f (18 sep 17:33 y 17:38; semillas 541–560 y 561–580; 14 brazos × 20): **NADA SE DECLARA por la letra (P-I2: el emisor tenía que anotar el referente en ≥ 18/20 y lo hizo en 15/20 y 16/20 en la dirección irreemplazable: el emisor comparte el punto ciego del receptor — lo que evita no lo muerde y no puede avisarlo) — pero LO REPORTADO, en las semillas con mensaje, es la señal más fuerte del día: el receptor come a la primera el alimento que evitaba SÓLO por el mensaje (15/15 y 16/16 contra 0/15 y 0/16 sin mensaje) y evita a la primera el veneno nunca mordido (16/20 y 18/20 contra 1/20 y 2/20); la referencia llega al nivel de la FAMILIA, no de la variante (barajado con la hermana funciona igual: 15–18/20; con otro token no: 6–8/20; valor solo no: 1/20)**

Preregistro `experimentos/nivel12_mundo_familias/PREREGISTRO_bloque4_canal.md` (07bef3347a28866e; protocolo de la sala 3 incorporado: emisor
simétrico, entrega por señalamiento, escritura en la tabla de pares como exposición sin consecuencia); instrumento `organismo_familias_b4.py`
(ff9946ee2ffe27e6; identidad 92/92 + 21/21 en cada runner; gemelo mudo con prefijo idéntico); datos `familias_b4_s541-560_20260918_172836`
(5fabb1518ee630d0) y `familias_b4_s561-580_20260918_173313` (8e65c7631b9ad377); 300 corridas por serie, 4.6 min.

| brazo (semillas con mensaje) | + veneno nunca mordido: evita a la 1.ª | − alimento que evitaba: come a la 1.ª |
|---|---|---|
| **CANAL** (patrón de X + R cruda) | **16/20 · 18/20** | **15/15 · 16/16** |
| CORTADO (gemelo mudo) | 1/20 · 2/20 | 0/15 · 0/16 |
| BAR-H (patrón de una hermana) | 15/20 · 18/20 | 12/15 · 12/16 |
| BAR-T (patrón de otro token) | 8/20 · 6/20 | 1/15 · 4/16 |
| VALOR (sin referencia) | 1/20 · 1/20 | 1/15 · 2/16 |
| INM (entrega inmediata) / OTRO | 3/20 · 3/20 / 4/20 · 3/20 | 4/15 · 3/16 / 5/15 · 4/16 |

Precio: `comH` 1.0 en CANAL− (se come también a las hermanas venenosas: la referencia es de familia); muertes iguales. **Puerta P-I2:** emisores
sin mensaje 5/20 y 4/20 en la dirección (−); el preregistro (ERR-50 reservado) manda PARAR y no corregir: es el montaje. Predicción del
diseñador (P-D: llega el valor y la familia, no la variante; BAR-H ≈ CANAL) acertada; la del coordinador (`comH` ≥ 0.9, BAR ≈ CORTADO)
refutada. **Lectura honesta:** el canal transmite "esta familia, este valor" y el receptor actúa sin experiencia propia — eso es
comunicación con referencia en su forma mínima — pero con una sola ganadora de 2 bits la referencia no baja a la variante, y el
emisor no puede avisar de lo que él mismo evita. **Siguiente (preregistro nuevo, ERR-51 = montaje del emisor):** bloque 4b con un emisor
que sí descubre (por ejemplo, un emisor "voraz" o que recibió a su vez el aviso de un tercero: la cadena), misma letra en el receptor y
en los controles, semillas 581–600 y réplica; y para la variante, el candidato de varias ganadoras (nodo por familia). Nivel 5 sigue en
50 % hasta la serie válida.


### BLOQUE 4b — el emisor que sí descubre (voraz = 1.0; ERR-51); tres series (18 sep 18:10, 18:15, 18:22; semillas 581–600, 601–620, 621–640): **NADA SE DECLARA por la letra — cada serie cayó en una puerta de montaje distinta (P-I3 por el brazo R-SIN-SAL, ERR-52; P-I5 en la dirección + por la puerta de familiaridad: 6/20 receptores ya leían por la vía rápida) — pero LA DIRECCIÓN IRREEMPLAZABLE (−: el receptor come a la primera el alimento que evitaba, sólo por el mensaje) pasa TODAS sus puertas en la tercera serie y replica en las tres: CANAL− 19/20, 17/18, 19/19 contra CORTADO− 3/20, 0/18, 2/19; emisor voraz avisa 20/20, 18/20, 19/20**

Preregistro `PREREGISTRO_bloque4b_emisor.md` (86c08ed4e0ba9821 + ERR-52); instrumento `organismo_familias_b4b.py` (b3dd1d7e66a2d147; identidad 95/95 +
18/18 por runner); datos `familias_b4b_s581-600_20260918_181001` (541f57d7711ae3e7), `familias_b4b_s601-620_20260918_181548` (e42c6a5e99dd5a86),
`familias_b4b_s621-640_20260918_182209` (206665f9bd674335); 340 corridas por serie.

| brazo (semillas con mensaje) | − come a la 1.ª lo que evitaba (3 series) | + evita a la 1.ª el veneno nunca mordido (3 series) |
|---|---|---|
| **CANAL** | **19/20 · 17/18 · 19/19** | 18/20 · 18/19 · 14/20 |
| CORTADO (gemelo mudo) | 3/20 · 0/18 · 2/19 | 4/20 · 2/19 · 2/20 |
| BAR-H (patrón de una hermana) | 12/18 · 14/19 (serie 2, 3) | 18/20 · 14/20 |
| BAR-T (otro token) | 5/18 · 7/19 | 11/20 (serie 3) |
| VALOR (sin referencia) | 3/18 · 3/19 | 1/20 |
| PAR (dos variantes tras el mensaje) / PAR0 | 18/18 · 19/19 / 3/18 · 1/19 | — |

Puertas: P-I2 (emisor avisa ≥ 18/20) pasa en las tres (+) y en la 1.ª y 3.ª (−) (18/20 en la 2.ª: regla 12); P-I3 cae en las series 1–2 sólo por
OTRO (ERR-52) y pasa en la 3.ª; P-I4 pasa; **P-I5 (la boca lee la vía lenta ≥ 18/20): (−) 19/19 pasa, (+) 14/20 cae** — en 6 semillas el receptor
ya tenía ≥ 5 mordidas del código del referente y leyó la vía rápida: el mensaje quedó escrito y no consultado (el segundo punto ciego, previsto
en el protocolo de la sala 3 §2.7). Precio: `comH` 1.0 (la referencia es de familia; `n_H = 1`, errata del 4 §9.3). **Lectura honesta:** la
comunicación con referencia de familia existe y es robusta en la única dirección donde el receptor no puede aprender solo; la dirección (+)
compite con la vía rápida cuando el receptor ya conoce el referente. Por la letra del 4b (puertas conjuntas para las dos direcciones) nada se
declara; **la declaración exige un preregistro con puertas POR DIRECCIÓN (ERR-53: montaje — las dos direcciones tienen puntos ciegos
distintos y no pueden compartir puerta), semillas nuevas 641–660 y réplica 661–680, sólo brazos (−).** Escrito antes de correrlo (18:30).
Nivel 5: 50 % → **65 %** (mensaje con referencia actuado sin experiencia propia, tres series; sin declarar).


### BLOQUE 4b, DIRECCIÓN (−) SOLA con puertas por dirección (ERR-53; 18 sep 18:38 y 18:42; semillas 641–660 y 661–680; 9 brazos): **NO SE DECLARA por la letra — el control BAR-T (mensaje con el patrón de OTRO token) queda por encima de CORTADO + 3 en las dos series (9/18 y 6/19 contra 2/18 y 0/19): la referencia del mensaje es PARCIAL. Reportado: el receptor come a la primera lo que evitaba, sólo por el mensaje, 17/18 y 16/19 contra 2/18 y 0/19 (quinta y sexta serie consecutivas); con el patrón de una hermana 15/18 y 13/19 (referencia de familia); sin referencia 5/18 y 4/19 (≈ CORTADO)**

Runner `corre_familias_b4b.py --brazos` sólo (−) (con ERR-54: los datos crudos se guardan antes del análisis; el análisis cayó por KeyError 'CANAL+'
con brazos de una sola dirección y el veredicto se calculó fuera del runner desde `familias_b4b_s641-660_20260918_183839_crudo.json` y
`familias_b4b_s661-680_20260918_184155_crudo.json`, campos `B4`). Puertas (−): P-I2 emisor voraz avisa 18/20 y 19/20 (pasa; la primera en el
borde, regla 12); P-I3 prefijo idéntico al gemelo 18/18 y 19/19 (pasa, OTRO excluido por ERR-52); P-I5 lee la vía lenta 17/18 (cae por una
semilla) y 18/19 (pasa). Receptor: CANAL− 17/18 · 16/19 (≥ 15 ✓); CORTADO− 2/18 · 0/19 (≤ 5 ✓); VALOR− 5/18 · 4/19 (≤ CORTADO + 3: ✓ · ✗ por
una); **BAR-T− 9/18 · 6/19 (✗ ✗)**; BAR-H− 15/18 · 13/19; PAR− 18/18 · 17/19 contra PAR0− 3/18 · 1/19; muertes iguales. **Lectura honesta:**
seis series seguidas dicen lo mismo — un organismo actúa sin experiencia propia porque otro se lo dijo — y también dicen que la referencia
no es limpia: el patrón de otro token arrastra la mitad del efecto (una sola ganadora de 2 bits reparte el mensaje entre familias que
comparten casilla). No se declara "comunicación con referencia"; se declara, con vocabulario estricto: *"el mensaje (patrón + recompensa)
cambia la conducta del receptor sin experiencia propia; la referencia es de familia y parcial"*. Nivel 5 se queda en 65 %. **Siguiente
(H-4 de la sala 4): varias ganadoras — el nodo por familia — para que BAR-T caiga a CORTADO y BAR-H también; entonces sí se declara.**
Cierre del día 18 sep a las 18:45: 15 bloques, 27 series, ERR-35..54, 0 entradas al tronco, dos declaraciones (desambiguar códigos;
crecimiento del linaje con lectura pesimista) y una comunicación mínima medida seis veces sin poder firmarla.


### Simulación EXTERNA (ChatGPT, entregada por el director 18 sep 19:05): `registro/investigacion/externo/JUACO_MEMORY_FRONTIER_v3/` — **no es evidencia; lectura del coordinador: no discrimina nada, y confirma por otro camino la H-1 (sin calibrar la mortalidad, ninguna arquitectura de memoria se puede comparar)**

Contenido: barrido de 7 arquitecturas de memoria (S resumen, E episodios, W trabajo, R replay, X sorpresa) en tres mundos, un "loop
evolutivo" de 40 generaciones y una validación de 60 réplicas. Hechos: (1) en el primer barrido las SIETE arquitecturas dan números
IDÉNTICOS (linaje medio 0.267 / 0.233 / 0.533; extinción 100 %): los módulos de memoria no tocaron la dinámica; (2) tras recalibrar el
metabolismo (energía inicial 8 → 20, coste 0.7 → 0.35; declarado en `CALIBRATION_NOTE.md`), las diferencias son pequeñas (supervivencia
media 4.5–8.3; linaje medio 0.15–0.43) y la extinción sigue en 100 % en todos; (3) el candidato final "S+E" valida con linaje mediano 0.0 y
extinción 100 %; (4) las citas del texto son marcadores sin resolver ("citeturn0search0"). El propio documento dice "simulación
hipotética". **Qué sirve:** llega, independiente de nosotros, a lo mismo que E-1/H-1 de la sala 4: si la población se extingue siempre,
la memoria no se puede comparar; primero R₀ ≈ 1. **Qué no sirve:** ninguna conclusión sobre qué memoria es mejor. Se archiva como
punto de vista externo; H-1 (la muerte que mata, con R₀ calibrado) ya está en diseño.


### LÍNEA EXTERNA — mundo mínimo (protocolo de ChatGPT) reproducido en el repo (18 sep 19:40; `experimentos/externo_mundo_minimo/`; un proceso; ZIP reproducibles byte a byte): **calibración reproducida (0.32 → R₀ 0.9415 ± 0.023, extinción 0.078, población 2.98; referencia externa 0.9665 / 0.082 / 3.03, dentro del ruido); A0 ≡ E semilla a semilla (0 discrepancias en 1000 semillas, 12 métricas, 1000/1000 genealogías): la predicción del coordinador se cumplió — ese mundo no puede probar ninguna memoria porque no hay acción; con dos parches (0.42 / 0.22, media 0.32) y una acción por ronda, la memoria episódica sube R₀ de 0.96 a 1.86, baja la extinción de 8.7 % a 0.8 %, pareado 70.8 % (réplica 74.8 %); la memoria BARAJADA (etiquetas de acción permutadas) ≈ A0 (p 0.16), como estaba predicho**

Calibración: barrido 0.29–0.34 (R₀ 0.53 → 1.31; extinción 0.41 → 0.02); mundo congelado en 0.32 con sha del motor. Decisiones no fijadas por
el protocolo declaradas (D1–D4). Lectura honesta del implementador (Opus): la variante de parches era predecible con aritmética (un bandido
de dos brazos con dos medias), el pareado es por semilla y no por trayectoria, el tope de 12 satura (R₀ censurado por arriba), y NADA de
esto entra en la escalera de JUACO. Lo que sí sirve: (1) la memoria es exactamente inerte sin acción y paga con una acción cuya contingencia
se pueda registrar, y quien lo sostiene es el control barajado; (2) R₀ ≈ 1 se calibra con una sola perilla (comida) en un mundo de juguete;
en el mundo vivo real, H-1 (corriendo) dirá si el organismo mortal se sostiene. SHA de los ZIP en `experimentos/externo_mundo_minimo/*/SHA256.txt`.


### H-1 — QUE LA MUERTE MATE (mundo vivo; 18 sep 19:24 y réplica 19:28; semillas 701–720 y 721–740; 20 brazos × 20): **REPLICADO — con la muerte que borra la memoria del individuo, el linaje NO se reemplaza: R₀ cae de 0.87–0.98 (control inmortal, idéntico al bloque 2 campo a campo) a 0.14–0.17 en TODOS los modos de herencia (nada 0.148/0.140; valores 0.160/0.170; valores + tabla 0.153/0.165; barajado 0.146/0.139); la vida mediana cae de ~700–800 a ~100–130 pasos. ERR-62 (cláusula de cierre escrita antes): ESTE MUNDO NO SOSTIENE LINAJES MORTALES con ninguna herencia ni con las rampas de dote, umbral, objetos o coste. El "filo del reemplazo" del bloque 2 era el de un inmortal subsidiado**

Preregistro `experimentos/nivel11_mundo_vivo/PREREGISTRO_h1_muerte.md` (f35f6d061b023d38; ERR-60 semillas de hijos sin colisión; ERR-61 A₁₂ sin
parear; ERR-62 reservado y ejecutado); instrumento `organismo_vivo_h1.py` (9e99ff87b5e2db1e; `muerte_real=0` ≡ rep2 bit a bit; identidad
62/62); runner `corre_vivo_h1.py` (34c8cd4d264a7a66); datos `vivo_h1_s701-720_20260918_191939` (bfaca3d00f58eecd) y `vivo_h1_s721-740_20260918_192423`
(1a6561be332aec0d); 400 corridas por serie, T = 100 000.

| brazo (CUELLO_MIN) | R₀ serie 1 / réplica | r | muertes | vida mediana |
|---|---|---|---|---|
| RENACE (control, como hoy) | 0.874 / 0.976 | −8.5 / −0.5 | 74.5 / 68.5 | 711 / 798 |
| MUERE, hereda nada | 0.148 / 0.140 | −210 / −205 | 249 / 239.5 | 96.5 / 102.5 |
| MUERE, hereda valores (M1) | 0.160 / 0.170 | −201 / −190.5 | 237 / 231.5 | 126.5 / 132 |
| MUERE, hereda valores + tabla | 0.153 / 0.165 | −202.5 / −201.5 | 238 / 240.5 | 121 / 112 |
| MUERE, hereda barajado | 0.146 / 0.139 | −203 / −210.5 | 242 / 246 | 104.5 / 102 |

H1-1 ancla del control: pasa (idéntico al bloque 2). **H1-2 la muerte mata: PASA ×2** (A₁₂ 1.0). H1-3 la herencia paga (≥ 1.30 × nada): NO (×1.08–1.21). **H1-4
barajado ≈ nada: pasa** (el control es limpio: la pequeña ventaja de heredar valores es real pero no alcanza). H1-5 el token no aporta sobre el
vector. **H1-6 → ERR-62.** H1-7: más de la mitad de las ventanas de los mortales las paga todavía el regalo de la fundación (R₀ medido es cota
superior). **Lectura honesta:** el organismo actual no puede reemplazarse a sí mismo si de verdad muere: aprende demasiado despacio (≈ 25
mordidas para consolidar; el hijo nace vacío y muere antes de aprender), y heredar los valores le da un 10–20 %, no el 500 % que le falta.
Esto reordena la escalera: **antes de población y evolución, hace falta que un cuerpo nuevo aprenda en menos de una vida** (aprender de un
golpe — v15f — y el mensaje del bloque 4 son exactamente eso), o un mundo menos letal para el recién nacido (dote, cuidado parental: mecanismos
nuevos, preregistro nuevo). Coincide con la simulación externa (extinción 100 % en todas las memorias hasta calibrar el metabolismo). Nivel 9:
45 % → **40 %** (la declaración del bloque 2 queda acotada: "al filo del reemplazo" sólo con renacer).


### BLOQUE 5 — VARIAS GANADORAS (H-4; k ∈ {1, 3, 5}; 18 sep 19:42 y 19:50; semillas 681–700 y 701–720; 27 brazos): **NADA SE DECLARA por la letra (puerta P-I2: el emisor avisó en 20/20 y 18/20, pero la subcondición "el mensaje llega ANTES de que el receptor vea el referente" dio 19/20 y 16/20 con ≥ 20 exigido; y R3 cae: la hermana sigue arrastrando), pero el RESULTADO es nítido y replica: con k = 3 el mensaje con el patrón de OTRO token cae de 7/20 a 2/20 y 4/18 (≤ CORTADO + 3 en las dos series) con el canal intacto (19/20, 16/18) y "sin referencia" ≈ mudo (4/20, 3/18): la referencia pasa de "alguna familia" a EXACTAMENTE ESTA FAMILIA; la hermana no baja (15/20, 13/18) porque el 100 % de las celdas de forma son ciegas a los 3 píxeles de variante (cálculo estructural del creador, escrito antes); k = 5 no mejora la referencia (7/20, 7/18) y rompe el cuerpo (muertes 199 y 152 contra 32–38)**

Preregistro `experimentos/nivel12_mundo_familias/PREREGISTRO_bloque5_ganadoras.md` (b53d7eb0603d82d2 + ERR-63 cruce cod0 del emisor que no comparaba
en b4/b4b + ERR-64/64b controles de no-vacuidad del arnés a T 60 000 y ≥ 2/3); instrumento `organismo_familias_b5.py` (e0b6b90f6f92d5c1; `k_ganadoras`
= 1 ≡ b4b bit a bit; lectura = SUMA de las casillas conocidas de las k celdas de menor error propio, relevo por abstención; identidad 106/106 +
26/27 en cada runner con el control (C) en 2/3 por ERR-64b); runner `corre_familias_b5.py` (27826d0d6eda0827); datos `familias_b5_s681-700_20260918_193337`
(253e8ca83a72c114) y `familias_b5_s701-720_20260918_194259` (1119b2600eae25e0); 540 corridas por serie.

| brazo (receptor come a la 1.ª lo que evitaba) | k = 1 (serie / réplica) | **k = 3** | k = 5 |
|---|---|---|---|
| CANAL (patrón de X + R) | 18/20 · 16/18 | **19/20 · 16/18** | 19/20 · 16/18 |
| CORTADO (mudo) | 1/20 · 0/18 | 0/20 · 1/18 | 0/20 · 1/18 |
| BAR-H (patrón de una hermana) | 13/20 · 12/18 | 15/20 · 13/18 | 16/20 · 13/18 |
| **BAR-T (patrón de otro token)** | 7/20 · 4/18 | **2/20 · 4/18** | 7/20 · 7/18 |
| VALOR (sin referencia) | 3/20 · 4/18 | 4/20 · 3/18 | 3/20 · 3/18 |
| PAR / PAR0 | 19/20 · 15/18 / 3/20 · 0/18 | 19/20 · 16/18 / 1/20 · 0/18 | 19/20 · 16/18 / 0/20 · 1/18 |
| muertes | 32.5 · 38.5 | 44.5 · 36.5 | **199.5 · 152** |

R1 pasa ×2 (k = 3); **R2 (BAR-T ≤ CORTADO + 3) pasa ×2 con k = 3**, no con k = 5; R3 (BAR-H ≤ CORTADO + 5) NO ×2; R4 pasa; R6 coste ≤ 1.5× pasa con k = 3
(×1.37, ×0.95), no con k = 5. Predicciones del creador cumplidas en todo (BAR-T cae, BAR-H no, k = 5 destruye): *"el techo no era sólo de bits:
la referencia de variante está en la retina de 3 píxeles, no en cuántas celdas se leen"*. **Lectura honesta:** la comunicación con referencia
de familia ya es exacta (k = 3: otro token no arrastra; sin referencia no arrastra; la familia correcta sí), en ocho series; lo que falta —
distinguir "sal rosa" de "sal" en el mensaje — exige celdas que vean el píxel de variante (nodo con subíndice de variante: cuello A del encargo
externo a Codex; H-4 cerrada como "no es k"). Por la letra (P-I2 en el borde y R3) no se declara; **vocabulario permitido: "el mensaje cambia la
conducta del receptor sin experiencia propia y refiere a esta familia y no a otra (k = 3); no distingue la variante"**. Nivel 5: 65 % → **70 %**.
Nota para el siguiente preregistro: la puerta P-I2 (emisor voraz ≥ 18/20) queda en el borde en cuatro de seis series; regla 12 la manda replicar
o rebajarla con ERR, y se decidirá antes de la serie siguiente, no después.


### BLOQUE ALMA — curitas guiadas por 20 almas Haiku y nodo central (18 sep 21:20; semillas 802–811; 6 brazos × 10 linajes × 20 muertes, muerte real): **EL ALMA RAZONADA NO LE GANA A LAS CURITAS AL AZAR (R-1 refuta: A₁₂(ALMA > AZAR) 0.525, se exigía > 0.60) — lo que paga es el CONTENIDO DEL NODO (nodo bien emparejado contra nodo barajado: R₀ 0.275 contra 0.175, A₁₂ 0.88, P-3 pasa) y abaratar el mundo (dote y umbral); ningún linaje mortal llega a R₀ 0.9 (mejor mediana 0.40; H-1 sigue en pie)**

Preregistro `experimentos/nivel13_alma/PREREGISTRO_alma.md` (a5a397330c314e21); instrumentos `organismo_alma.py` (7c09cec391daa879) y `organismo_alma2.py`
(4fd616aeaf535e61; identidad 114/114); runner `corre_alma.py` (77803beb86756ed8); almas = 20 agentes Haiku por la interfaz de archivos (`alma_io/`),
un linaje cada uno; controles automáticos; crudos por linaje en `experimentos/nivel13_alma/alma_<brazo>_s<sem>_*.json`.

| brazo | R₀ mediana (10 linajes) | vida mediana | A₁₂ contra ALMA |
|---|---|---|---|
| **ALMA** (alma Haiku, menú completo, nodo) | **0.40** [0.15, 0.55] | — | — |
| AZAR (curita al azar, nodo) | 0.35 | 470 | 0.525 (ALMA no gana) |
| CIEGO (nodo bien emparejado, curitas al azar sin conectar) | 0.275 | 594 | 0.52 |
| BARAJA (nodo con recompensas permutadas) | 0.175 | 226 | 0.835 |
| SIN_NODO (alma Haiku sin nodo; 7 de 10 reportados) | 0.30 | — | 0.65 |
| NINGUNA (= H-1 hereda nada) | 0.225 | 125 | 0.75 |

**Lectura honesta:** (1) el alma que razona no aporta sobre elegir curitas al azar del mismo menú: P-5 (A₁₂ ≥ 0.85 contra NADA, ≥ 0.75 contra
AZAR) cae; lo que las almas hicieron bien fue lo que el azar también hace: bajar el umbral y subir la dote (abaratar el mundo) y conectar al
nodo. (2) El nodo transmite CONTENIDO, no cautela genérica: el barajado es el peor brazo (0.175, vidas 226) y el nodo ciego lo dobla en vida
(594). (3) Con muerte real ningún brazo se acerca al reemplazo (0.9): H-1 y ERR-62 siguen en pie; el alma no encontró la curita que falta,
porque no está en el menú: el hijo nace vacío y muere a los ~100 pasos si no está conectado; conectado vive 5×, pero se reproduce poco
(saciedad y umbral). (4) Defecto de instrumento en 1 linaje (810): respuestas con caracteres no ASCII no aplicaron (a)/(b): ERR-84, tolerancia
de codificación en el buzón, para la próxima serie. **Hipótesis que deja para el método (sin alma, preregistro nuevo):** nodo central leído por
relevancia y no por recencia (las lecciones expiraban); conexión al nodo desde el nacimiento como mecanismo (no como curita) contra barajado;
y la reproducción desacoplada de la saciedad. Nivel 9 sigue en 40 %.


### BLOQUE 6 — SUFIJO DE VARIANTE (mecanismo de Codex completado; factorial k × sufijo; 18 sep 21:07 y réplica 21:20; semillas 721–740 y 741–760; 36 brazos): **REPLICADO — la firma de los 3 píxeles de variante en la tabla de pares lleva la referencia del mensaje hasta la VARIANTE (el receptor distingue "sal rosa" de "sal": 15/20 y 15/18 contra 12/20 y 9/18 sin sufijo; la hermana cae de 13–14 a 5–6 de 20) al precio de perder parte de la especificidad de familia (otro token sube de 4–5 a 10–11) y subir la base sin mensaje (0 → 4–6): con 4 casillas por par no caben familia y variante a la vez. NADA SE DECLARA por la letra (puerta P-I2 en el borde, R2 cae) — pero la fase 5 queda con dos lecturas replicadas: k = 3 da familia exacta; el sufijo da variante; el organismo necesita las dos y hoy sólo puede una**

Preregistro `experimentos/nivel12_mundo_familias/PREREGISTRO_bloque6_sufijo.md` (ERR-70 P-I4 por exclusión; ERR-64b heredado; ERR-71 el caso (d)
del arnés pasaba por el emisor); instrumento `organismo_familias_b6.py` (b10cbd4ddd0c32a3; identidad 59/59, cadena hasta el tronco); runner
`corre_familias_b6.py` (88253f352d921c42); crudos `familias_b6_s721-740_20260918_205401_crudo` (31f01bf3f16bb09b) y `familias_b6_s741-760_20260918_210716_crudo`
(7522e085744c46cc); 720 corridas por serie; los brazos se calcularon desde los crudos (ERR-54) porque el análisis del runner se detuvo en la puerta P-I2.

| receptor come a la 1.ª lo que evitaba (serie / réplica) | k1 sin sufijo | k3 sin sufijo | k1 con sufijo | **k3 con sufijo** |
|---|---|---|---|---|
| CANAL | 19/20 · 18/18 | 19/20 · 17/18 | 19/20 · 17/18 | **20/20 · 15/18** |
| CORTADO (mudo) | 2/20 · 5/18 | 0/20 · 0/18 | 1/20 · 2/18 | 6/20 · 4/18 |
| BAR-H (hermana) | 14/20 · 15/18 | 13/20 · 14/18 | 9/20 · 10/18 | **6/20 · 5/18** |
| BAR-T (otro token) | 12/20 · 8/18 | **5/20 · 4/18** | 11/20 · 9/18 | 11/20 · 10/18 |
| VALOR (sin referencia) | 5/20 · 8/18 | 2/20 · 1/18 | 3/20 · 4/18 | 4/20 · 4/18 |
| PAR: distingue X de su hermana | 5/20 · 6/18 | 12/20 · 9/18 | 16/20 · 15/18 | **15/20 · 15/18** |

**Lectura honesta:** el mecanismo de Codex funciona para lo que se diseñó (la variante entra en la dirección: PAR 15/18 contra 6/18; la hermana
deja de arrastrar) y cobra exactamente el precio que el creador calculó antes (tabla 8× más dispersa; una sola ganadora reparte entre familias:
BAR-T vuelve a 10/18). La predicción del creador (BAR-H 0–5, BAR-T 0–4 con k3v1) acertó en la hermana y falló en el otro token. Lo que la fase
5 necesita ahora es una tabla que codifique familia Y variante (dos ganadoras de distinto tipo: una de forma y una de variante, sumadas), y
eso es un candidato nuevo con preregistro nuevo. Vocabulario permitido: *"el mensaje puede referir a la familia exacta (k = 3) o a la
variante (sufijo), no a las dos con la misma tabla"*. Nivel 5: 70 % → **75 %**.

### CIERRE DEL 18 SEP (21:30). Estado para el siguiente chat
Corrido y registrado hoy: 18 bloques, 33 series, ERR-35..ERR-84, dos declaraciones (desambiguar códigos; crecimiento del linaje con lectura
pesimista), la comunicación mínima medida en diez series (familia exacta con k = 3; variante con sufijo), H-1 (la muerte mata: el mundo no
sostiene linajes mortales), la serie ALMA (el alma razonada no gana al azar; el nodo transmite contenido). Preparado y pendiente: v14.2 (=
v14.1 + B-5) con identidad 62/62 y humo, a la espera de la regla 1 completa, manifiesto y tag; v15f bajo el criterio v2 (paquete verificado,
33/33) a la espera de su serie; la línea lateral del exoesqueleto (`HIPOTESIS_exoesqueleto_20260918.md`). Decisiones del director: B-5 → v14.2
(sí), v15f con v2 (sí), dE5 después (sí). Próximo candidato de la fase 5: tabla con dos ganadoras de tipo distinto (forma + variante).


### CONGELACIÓN v14.2 (18 sep 21:25; decisión del director ~20:40: "córrelas recomendaciones") — **TRONCO = v14.1 + B-5 (división por R = 0)**
Archivos nuevos (por anclas, `experimentos/creacion_B/construye_v142.py`, tripwire de sha en los orígenes): `organismo/organismo_v142.py` (17528d767fcebaf6;
única diferencia con `organismo_v14_codigo.py`: `desambiguar=1` por defecto), `organismo_v142g.py` (9e5f566cd6a7a4d2), `bateria_v142.py`
(6375d90e531b06e6), `bateria_generaliza_v142.py` (e5929942647756a5; entrada campo a campo = tronco). Identidad `organismo/identidad_v142.py` **62/62**
(apagada ≡ v14.1 24/24; rng 2/2; ON ≡ `organismo_v14_codigo_on` 24/24; gemelos 12/12; inercia ON 30/30). **Regla 1 completa (21:20, Pool):** examen
`bateria_v142.py 6`: 8/8 True; `bateria_generaliza_v142.py organismo_v142 20 --desde 101`: G1 1.000 (azar 0.450, 20/20), G2 0.967 (azar 0.437,
20/20), K 20/20. Evidencia heredada de B-5 (bit a bit el mismo módulo): examen con `splits` idénticos a v14.1 6/6, generalización 40/40 idéntica,
alias reparado 18/18 en dos series, coste 0 % exacto. Lo que v14.2 NO es: un candidato del criterio v2 (no mejora el tronco; le quita un defecto
que sólo aparece fuera de él). Tag `v14.2-tronco`. v14.1 pasa a regresión histórica. 20 congelados.

### JUNTA DE LA FASE 5 (19-sep-2026, 16:00 → 19:35; tres creadores Opus con exoesqueleto y nave; el coordinador corrió las series)
Objetivo: una tabla que refiera a FAMILIA Y VARIANTE a la vez (BAR-T ≤ 5/20 **y** PAR ≥ 15/20), con las puertas del bloque 6.
Confirmaciones en semillas nuevas 821–840 y 841–860, corridas por el coordinador (Pool 5, `JUACO_POOL`/`--pool` tras ERR-86).

| candidato | identidad | serie 821–840 | serie 841–860 | misión |
|---|---|---|---|---|
| **C** división por conflicto donde falla la familia | 61/61 | BAR-T 3 ✅ · BAR-H 12 ✗ · PAR 8 ✗ | BAR-T 3 ✅ · BAR-H 9 ✗ · PAR 9 ✗ | **NO (refutado ×2)** |
| **B** lectura CONJUNTIVA (intersección en vez de unión) | 88/88 | BAR-H 9 ✗ · BAR-T 7 ✗ · (5 de 7 puertas) | BAR-H 7 ✗ · BAR-T 5 ✗ · PAR 14 · CANAL 15 | **NO (cae ×2, el más cerca en variante)** |
| **A** dos ganadoras de distinto tipo + mínimo entre tipos | 77/77 | R2 BAR-T 9 CAE · R3 BAR-H 10 CAE · PAR 13 | **R1–R5 TODAS pasan** (BAR-T 5, BAR-H 7, VALOR 6, dist 13) | **NO (sin réplica; PAR 13 < 15)** |

**Lectura honesta:** ninguno cierra la fase 5. El canje sigue vivo, pero se movió: C recupera la familia y pierde la variante;
B recupera la variante y casi la familia; A pasa todas las puertas preregistradas en UNA de las dos series. La fase 5 queda en
75 % y el siguiente candidato debería combinar la conjunción de B con las dos ganadoras de A (nadie lo probó junto).
**Hallazgos del bloque, medidos y registrados aunque el candidato caiga:** (1) la lectura de b5/b6 es una DISYUNCIÓN —la unión
de las k direcciones—, por eso una celda alcanzada por azar decide sola (B); (2) el precio del sufijo es de DENSIDAD, no de
bits: subdivide en vez de multiplicar particiones (A y C coinciden); (3) fuga del mensaje re-eligiendo la ganadora hacia celdas
"+1 en todas partes", presente en b4/b4b/b5/b6 y no medida hasta hoy (A, `msg_elige`); (4) predicciones propias refutadas y
registradas por sus autores: pesos de tipo y mínimo dentro del tipo inertes (A), relevo marginal y dos canales con veto (B),
"el que aprende mejor deja de escuchar" V1/V2 (C, cae en las dos series).
**ERR-85** (agente mató procesos sin verificar cmdline) y **ERR-86** (Pool(14) con otras corridas → BrokenPipe) en HANDOFF 15.12.

### ERR-87 (21-sep-2026, 13:30; hallado el 18 sep por un auditor externo, verificado hoy por el coordinador y un segundo auditor Sonnet)
**Qué se observó:** en `experimentos/nivel7_hija_dispersa/corre_baterias_v13D.py` y `experimentos/nivel9_probar_si_mismo/corre_baterias_v13E.py`,
`lee_json(pref)` elegía el último `datos/<pref>*.json` por `startswith` + orden de nombre. Como `regresion_generaliza_organismo_v13D_` es
prefijo literal de `..._v13D_on_` (y `..._v13E_` lo es de `..._v13E_k3_`/`_k5_`) y `'o'`/`'k'` > dígito, la etapa de referencia (OFF) releía
el JSON de la ON. Es un segundo defecto en la misma línea que ERR-29 (1e2d7a6), no cubierto por aquella corrección.
**Causa:** instrumento (lectura de resultados). **Veredictos registrados que toca: NINGUNO** — verificado contra los JSON, no asumido:
v13D `regresion_generaliza_organismo_v13D_on_20260918_012533` y `..._v13D_20260918_012617` dan `{K,G1,G2}=True` los dos lados, así que
`D2_generalizacion=True` en `baterias_v13D_20260918_012145` es correcto sea cual sea el archivo leído; v13E `baterias_v13E_20260918_023210`
(02:37) es anterior a los archivos k3/k5 (03:09/03:24), así que no pudo leerlos.
**Corrección:** `lee_json` exige `prefijo + AAAAMMDD_HHMMSS.json` exacto (regex) en los dos runners; en v13D cada etapa guarda además el
archivo y el módulo leídos y avisa si el JSON es anterior al arranque de la etapa. Verificación mecánica (sin Pool): la función nueva sobre
`datos/` real devuelve `012533` para el prefijo ON y `012617` para el OFF; `py_compile` limpio en los dos. No se vuelve a correr nada.
**Regla derivada (para creadores e implementadores):** todo runner que lea "el último JSON de un prefijo" lo hace con prefijo + sello de
tiempo exacto, nunca con `startswith`; y registra en su JSON qué archivo leyó cada etapa.
También se corrige `experimentos/creacion_A/PREREGISTRO_v15f_v2.md:120`, que decía "los ERR libres siguen desde ERR-100": cifra inventada
por el agente; el último real era ERR-86. Crudos de la junta de la fase 5 (`jb_serie_s821-840_20260919_181958`, `jb_serie_s841-860_20260919_183515`)
añadidos al repo en este commit; el segundo auditor recalculó desde ellos BAR-H 9/18 · BAR-T 7/18 · PAR 14/18 y BAR-H 7/17 · BAR-T 5/17 · PAR 14/17 ·
CANAL 15/17, idénticos a la tabla registrada. Siete archivos de humo sin dueño en el registro (b4b, enm1 ×3, b5 ×2 con guarda fallida,
jb 901-902) se mueven a `datos/humo_no_registrado/` y NO entran a git.

### Candidato v15f bajo el CRITERIO DE TRONCO v2 — veredicto final de las siete puertas, semillas nuevas (creador A / RELEVO; serie corrida por el coordinador 21-sep-2026 12:37–12:54, 1002 s, Pool 10 vía `JUACO_POOL`, commit del runner `930f6fb`): **NO ENTRA — cae T-A (sobrevive), T-C (se desdice), T-D (sin alias) y T-E (no regresión conductual); pasan T-B (generaliza), T-F (coste) y T-G (capacidad nueva: xor01 estricta 1.000 ON contra 0.531 OFF, pareado 18/20). Una sola puerta caída basta (regla 2 de v2, sin modos intermedios) — v15f queda fuera del tronco; el tronco sigue siendo v14.2**

Preregistro `experimentos/creacion_A/PREREGISTRO_v15f_v2.md` (sha impreso por el log de hoy: `f3ad71467197a531`; §1–§6 antes de medir del creador A, 18-sep; ENMIENDA 1 del 18-sep 20:40 añadió T-A y T-G sin tocar ningún umbral). Runner `corre_v15f_v2.py` (`c2d118ec603d01c6`; único cambio desde el paquete verificado: Pool por `JUACO_POOL`, ERR-86). Instrumentos por anclas (shas que imprime el log): `construye_vivo_relevo` `6942d42461832404` → `organismo_vivo_relevo` `3b2cb0ca4c334779`; `identidad_vivo_relevo` `90187f3c114500c1` (**ARNÉS TOTAL 33/33**: 28 identidades + 5 controles M1–M5 que fallan como deben); `bateria_v15f` `d63f5aee558eb6da`; `bateria_generaliza_v15f` `0cd87d2632e0c66a`; `organismo_v15f_on` `54d6efe0b564113c`; orígenes `organismo_vivo_rep2` `96feb4918dc5d694`, `organismo_vivo` `20c0961c79de8825`, `organismo_v14` `feefc88b1fd8d434`, `bateria_v14` `72216f5415de0c86`. Crudos: `datos/v15f_v2_20260921_123755.log` / `.json` (sha256_16 `58538f00d49d0f8e`) con los volcados por etapa `..._crudo_TA.json` (`193d8009af2a9d2c`), `..._crudo_TCii.json` (`33100bee7a14d904`), `..._crudo_TD.json` (`bb8549a18b892983`), `..._crudo_TG.json` (`609c1727d1d7c858`), y los JSON de subproceso `regresion_generaliza_v15f_organismo_v15f_on_20260921_123920.json` (T-B), `examen_v15f_20260921_124008.json` (examen candidato) y `examen_v14_20260921_124347.json` (examen tronco, corrido fresco). Los números salen de `v15f_v2_20260921_123755.json` con precisión completa donde el log trunca. Sin ERR ni violación de regla: al arranque el runner reportó 3 procesos python vivos (regla 11): este y dos ajenos de un proceso (alefast), ninguno con Pool.

| puerta | letra del umbral | medido v15f (ON) | medido OFF / tronco | pasa/cae |
|---|---|---|---|---|
| **T-A sobrevive** | muertes ≤ 1.10 × tronco (mediana) y r ≥ tronco − 10; pareado por semilla A₁₂(r) ≥ 0.50 | VIVO: muertes 92.5 (razón 0.974), r −73.5 (Δ −0.5), A₁₂(r) 0.425 · CUELLO_MIN: muertes 78.5 (razón 1.09), r −11.5 (Δ −3.0), A₁₂(r) 0.45 | VIVO: muertes 95.0, r −73.0 · CUELLO_MIN: muertes 72.0, r −8.5 | **CAE** — medianas y Δr cumplen en los dos brazos; A₁₂(r) < 0.50 en los dos |
| **T-B generaliza** | G1 ≥ 0.80, G2 ≥ 0.85, azar ∈ [0.35, 0.65], K 20/20 | G1 1.0, G2 0.998568713657896, K 20/20 | azar G1 0.5, azar G2 0.43623750833855923 | **PASA** |
| **T-C se desdice** | (i) conducta E2 ≥ 18/20 ("come B Q4 ≥ 50") · (ii) A₁₂(rev ON>OFF) ≥ 0.75 | (i) comeB_Q4 20/20 · (ii) A₁₂(rev) 0.55, rev 44.5 | (ii) rev OFF 37.5 | **CAE** — (i) pasa; (ii) 0.55 < 0.75 tumba la puerta |
| **T-D sin alias** | C1 \|W[sal]\| ≤ 0.3 en ≥ 8/9 (mediana ≤ 0.1) · C2 W_hambre[veneno] ≤ −2.8 en ≥ 8/9 y ≤ −2.5 en 9/9 · C6 (LIMPIAS) 9/9 y 9/9 | C1 0/9 (mediana 1.56) · C2 0/9 (mediana −1.56) · C6 9/9 y 9/9 | OFF: C1 0/9 (mediana 1.45) · C2 0/9 (mediana −1.45) · C6 9/9 y 9/9 | **CAE** (C1/C2 en ALIAS; C6 pasa) |
| **T-E no regresión conductual** | por escenario ≥ 18/20 (conducta conservada; los pesos sólo se reportan) | E1 13/20 · E2 3/20 · E2I 19/20 · E2J 16/20 · E2K 14/20 · E2L 16/20 | — | **CAE** — 5 de 6 escenarios caen; sólo E2I pasa |
| **T-F coste** | ≤ 1.25 × tronco | celdas razón 1.0 · splits razón 1.0 · muertes razón 1.019 | tronco: celdas 32.0, splits 2.0, muertes 129.5 | **PASA** |
| **T-G capacidad nueva** | xor01 estricta ≥ 0.75 con 8 ejemplos; azar ∈ [0.35, 0.65]; px0 ON ≥ OFF | xor01 estricta ON 1.0 (pareado ON>OFF 18/20, gana(0,1) 20/20) · px0 ON 1.0 (pareado 17/20) · azar 0.6 | xor01 estricta OFF 0.53125 · px0 OFF 1.0 | **PASA** |

Brazo exploratorio `v15g` (`relevo_boca=1`, la casilla decide antes que la puerta; NO candidato, declarado así en el preregistro §2): **T-D PASA** (C1 9/9 mediana 0.0, C2 9/9 mediana −3.0, C6 9/9 y 9/9) · **T-C (ii) CAE** (A₁₂(rev) 0.55, rev 43.0 contra OFF 37.5, igual que v15f).

**Lectura honesta:** v15f generaliza (T-B), no encarece el examen (T-F) y sigue cruzando XOR con 8 ejemplos en la configuración del tronco (T-G), pero no sobrevive de forma pareada (T-A cae por A₁₂(r) < 0.50 en los dos brazos aunque las medianas de muertes y el delta de r cumplan: no le gana semilla a semilla a su propio apagado), no se desdice en el mundo vivo (T-C ii, 0.55 contra 0.75) y no conserva la conducta del examen (T-E: sólo E2I; E2 se derrumba a 3/20 porque "muerde A Q4 ≤ 1.10 × tronco" casi no se cumple tras la reversión). En T-D la tabla de hambre sabe la combinación exacta (0.0 en la sal, −3.0 en el veneno) pero la puerta de v14.1 lee la vía rápida en el código compartido de las ALIAS antes de consultarla, exactamente el mecanismo que predijo el creador A; `v15g`, que mueve la casilla antes de esa puerta, sí cruza C1/C2: el orden de las puertas, no la tabla, es la causa. Una sola puerta caída basta: v15f no entra. **Patrón de la línea:** v15d, v15e y v15f (tres mecanismos distintos de memoria de pares en la vía lenta) caen los tres por reversión o por conducta del examen; el coordinador lo lee como patrón, no como ruido, y recomienda cerrar la línea salvo decisión del director.

**Predicciones del creador A (§5 del preregistro, escritas antes de medir):** T-B (G1 1.000, G2 ≥ 0.97) acertada. T-C (i) 20/20 acertada; T-C (ii) A₁₂ 0.80–0.95 **refutada** (0.55). **T-D, la predicción central ("v15f NO pasa T-D porque la puerta lee la rápida; v15g sí pasa C1/C2"): acertada** (v15f 0/9, v15g 9/9). T-E: E1 ≥ 18 refutada (13); E2 20/20 refutada (3); E2I acertada (19); E2J/E2K/E2L ≥ 19 refutadas (16, 14, 16). T-F acertada, mejor de lo esperado. T-A y T-G sin número fijado; T-G cualitativa ("1.000 estricta") se cumple; T-A "muertes ≈ tronco" se cumple en medianas pero no anticipó el criterio pareado A₁₂(r), que es lo que tumba la puerta. **Veredicto esperado del creador ("cae sólo en T-D") parcialmente refutado:** el "no entra" es correcto, pero cae en cuatro puertas.

Vocabulario permitido: *"la memoria de pares con relevo generaliza y no encarece el examen, pero bajo el criterio v2 no sobrevive de forma pareada, no se desdice en el mundo vivo ni conserva la conducta del examen; en el alias la puerta de v14.1 lee la vía rápida antes que la tabla, y v15g, que invierte ese orden, cruza el alias pero no la reversión"*. Prohibido: "v15f entra"; "cae sólo por el orden de las puertas"; llamar a v15g "candidato".

**Qué queda:** v14.2 sigue siendo el tronco; nada se rejuzga. `v15g` entra como candidato aparte únicamente si alguien escribe su preregistro con las siete puertas y semillas nuevas. Decisión pendiente del director: cerrar la línea de memoria de pares en la vía lenta (recomendado) o preregistrar v15g.
