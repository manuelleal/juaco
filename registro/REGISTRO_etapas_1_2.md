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

**Conclusión que sí se sostiene**: en E1 la generalización está determinada por el solapamiento de códigos y por
nada más, y el 15.9% de alcance nulo es una medida real del techo. **Lo que NO se ha probado** es que la fórmula
aguante donde puede romperse. Queda preregistrada la versión dura, para correr:
la fórmula debe fallar de forma medible cuando (a) los códigos se solapan (escenarios 2I/2J/2K, donde las celdas
compartidas reciben actualizaciones mixtas y la uniformidad dentro del código se rompe), (b) el clip de ±3 por celda
está activo, o (c) hay más de dos estímulos. **Predicción: el residuo deja de ser 0 exactamente en esos tres casos,
y crece con el solapamiento.** Si el residuo sigue siendo 0 con códigos solapados, la uniformidad del código es más
robusta de lo que creemos y eso es un hallazgo. Si crece, tenemos la primera medida de cuánto se degrada la
generalización por interferencia, que es lo que 2I y 2J insinuaban sin cuantificar.

### Nota de entorno (Windows)
`bateria.py` aborta en Windows con `UnicodeEncodeError` al imprimir `≈`: la consola es cp1252. Es fallo de impresión,
no de cálculo. Se corre con `PYTHONIOENCODING=utf-8`. Los archivos congelados NO se tocaron; `bateria_v7.py` incluye
`sys.stdout.reconfigure(encoding='utf-8')`.
