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
  **Divisiones en etapas normales: 0 en 6/6** — la regla no dispara sin error crónico.
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
