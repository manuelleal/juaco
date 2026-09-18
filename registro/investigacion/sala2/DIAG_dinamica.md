# DIAG — Sala 2, lente DINÁMICA DE APRENDIZAJE (aprender y desaprender)

**Diagnosticador de la sala 2, 18 sep 2026, ~09:45.** Misión primero: llegar a la AGI por este camino — un organismo mínimo
con reglas locales (sin backprop en el runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia
preregistrada. Primero llegar a la frontera; segundo, que viva.

**Alcance y reglas cumplidas.** No edité ningún archivo del repo; este es el único archivo que creé. No corrí ningún organismo ni
ningún `Pool` (hay uno vivo: `corre_vivo_rep2.py --desde 261`, pid 16896, con 14 workers). Toda la evidencia sale de (a) el
código del tronco `organismo/organismo_v14.py` (feefc88b1fd8d434), (b) los JSON/logs ya guardados en `datos/` (en particular
la serie de **v15e**, que terminó a las 09:36:56 mientras se escribía esto: `v15e_s141-160_20260918_092921`,
`examen_v15e_20260918_093053`, `regresion_generaliza_v15e_organismo_v15e_on_20260918_093352`), y (c) el registro. Cuando doy
una cifra derivada del código (no medida), lo digo.

---

## 1. Dónde está la frontera hoy, desde esta lente

### 1.1 Las tres escalas de tiempo del tronco v14.1 (derivadas del código y confirmadas con datos)

En `organismo_v14.py` la única línea donde cambia un valor es dentro de `if mordio:` (L107–129). **Nada aprende sin morder, por
construcción** (la capa política `Wl` sí recibe `Rp = 0.2` por acercarse, L158, pero eso no es valor). De ahí salen tres relojes:

| vía | regla (línea) | cuánto se mueve la lectura por mordida | mordidas hasta el 90 % de R (derivado) | medido |
|---|---|---|---|---|
| **rápida** (Kenyon, 3 celdas) | `Wn += eta·(−dlt)·kc`, `eta = 0.03` (L128–129) | 3 celdas × 0.03 = **0.09** del error | **≈ 24** (0.91ⁿ ≤ 0.1) | 47–51 mordidas de B → W_B −2.96/−2.98 (humo v15e, v14.1 apagado, s101/s102: 0.91⁴⁷ = 0.012 ✓) |
| **lenta** (lineal de la retina) | `Wns += eta_s·(−ds)·P`, `eta_s = 0.15` (L119–120) | 3 píxeles × 0.15 = **0.45** del error | **≈ 4** (0.55ⁿ ≤ 0.1) | v13 tenía 0.015 → 0.045/mordida → ≈ 51; A-4 midió 400 → 150 exposiciones con rasgos dados |
| **tabla de pares** (M3 / v15c / v15d / v15e, fuera del tronco) | casilla ← R de un golpe | **1.0** del error | **1** | n\* = 7–10 exposiciones en xor01 (dos series, 121–140 y 141–160) |

Y una cuarta pieza que **decide cuál de las tres gobierna la boca**: la puerta por evidencia del código (`_fam`, L58–60): el
patrón es "familiar" cuando su código exacto se mordió ≥ 5 veces **y** tiene ≥ 1 celda con `|Wp−Wn| > 0.2`. Tras 3–5 mordidas
de B cada celda lleva `Wn ≈ 0.27–0.45` → familiar → **la boca deja de leer la lenta (ya en −3.00) y pasa a leer la rápida (≈ −1.2),
que tarda ≈ 20 mordidas más en llegar a −3**. Consecuencia medida: la memoria de un golpe de v15e (la lenta lee −3.00 exacto tras
UNA mordida) **no cambia la conducta**: mordidas de B por cuarto en E1, mediana de 20 semillas, v15e **[25.5, 10, 7, 7.5]** contra
v14.1 **[27, 11, 8, 1] / [27, 9, 7, 8]** (mismas semillas 101/102, humo). *La velocidad de asociación de la boca del tronco está
acotada por la puerta a ≈ 25 mordidas, digan lo que digan la lenta o una tabla.*

### 1.2 Cómo desaprende el tronco, y cuánto cuesta

- **Cambio de signo sobre el mismo código** (E2, A: +1 → −3): error −4, la rápida se mueve 0.36/mordida → el signo cruza 0 en
  **≈ 3 mordidas**; en la primera mordida contradictoria con `|Wb[c]| > 0.2` la división por conflicto de signo (L144–149) manda
  el signo nuevo a una hija ciega fuera de P y la madre conserva el viejo (creador A: "la fisión es consolidación"). Pasa 20/20 en
  todos los exámenes de v14/v14.1.
- **Cambio de −3 a +1 (B: veneno → comida)**: la boca lee −3 → `Vb = 1.2·(−3) + 2·hambre + 0.5` → **pb = 0.025 con hambre 1**
  (`1/(1+e^{1.1/0.3})`), **9·10⁻⁴ con hambre 0.5, 3·10⁻⁵ saciado**. Desaprender lo temido **exige muestreo bajo hambre**: es la
  frontera de la Etapa 2 (`hb = 2` óptimo). Medido en pasos: recuperación tras la inversión **2 000–4 000** pasos en el mundo largo
  (18/20 ≤ 10 000; `largo_s1-20`, `largo_s21-40`) y **7 931 / 9 076 / 10 126** pasos en el mundo de recuperación de C-P1
  (V13, tres series). La "sorpresa del mundo en la boca" a dosis 5 (dE5) baja eso a **2 249–2 700 pasos (0.25×, 20/20 × 2)** con
  retención 20/20 × 6 y G1 = base; en compañía de los órganos de v14: T1 8/8 + 7/8 (semilla 133, 42 bocados), T2 1.000/0.93,
  T3 0.24×. **Candidata a v15 desde las 04:47; no está en el tronco.**
- **Olvido no querido (retención de lo ausente)**: patrones nunca invertidos, ausentes ≥ 150 000 pasos mientras se aprenden otros
  40 con las mismas celdas: **0.67** (V13; `largo_s21-40`). A-2 (metaplasticidad por masa de conflicto) refutada: 0.667 = base,
  recupera más lento, **+73 % muertes** (`metaplasticidad_s41-60`). No hay mecanismo. El valor vive en celdas compartidas; la
  interferencia es el precio de la generalización (hallazgo del día 5: "la generalización de v9 era su interferencia").
- **Memoria de un golpe y desaprender**: v15d (tabla con R crudo, EMA 0.3, error de la suma) **no se desdice**: E2 0/20 (come B
  Q4: 1/20), y mata de hambre a la rápida (E1 W_B ≈ −3: 0/20, W_B −4.35 = 1.45·R). v15e (cada vía su error, la tabla guarda el
  residuo de la lineal por sobrescritura) **sí se desdice**: E2 **20/20** (B Q4 63–112 mordidas; W_A −2.84…−2.94; W_B +1.00 en 20/20)
  y E1 W_B ≈ −3 20/20 — **pero pierde la identificabilidad de XOR** (abajo, §1.4).

### 1.3 Identificabilidad de XOR con 8 ejemplos (cerrada, y por qué no es un problema de dinámica)

Con 8 patrones de tren, **9 de 15 rasgos conjuntivos ajustan con residuo 0** y sólo 1 generaliza (creador A, A12); gradiente
exacto 0.562, retropropagación 0.531, estadístico ideal 3/20, fisión de v11 0/20 (criba). Con 14 patrones queda 1 de 15 y la
regla local con competencia da **1.000 con n\* = 200** (A-6). Con 8, sólo un **prior de pares** cruza: M3 **1.000 / 1.000
estricta, n\* = 7 y 10, gana (0,1) 40/40, azar 0.50, px0 1.000** (dos series). ERR-35 (firmado por el director): la línea se
cierra declarando el mínimo de ejemplos. **Desde esta lente: el cuello de "pocas exposiciones" era el estimador (150–300 para la
regla delta contra 7 para escribir de un golpe), y el de "8 ejemplos" es información, no regla**: ningún reloj lo arregla.

### 1.4 Lo que la mañana dejó (07:43 → 09:36): tres candidatos de la línea XOR, ninguno entra; dos candidatos que pasan todo, esperan

| candidato | qué arregla | qué rompe | datos |
|---|---|---|---|
| v15c (08:06) | xor01 0.812 estricta (config v13, ERR-41) | V1 nunca medido ON; G1 anulado por ERR-38 (corregido: 1.000) | `v15c_s121-140` |
| v15d (08:38) | generaliza (G1 1.000 / G2 0.999) y cruza XOR (0.875, config v13) | **no se desdice** (E2 0/20) y **no consolida** (E1 0/20: 1.45·R) | `v15d_s121-140`, `examen_v15d_…083108` |
| **v15e (09:36)** | **se desdice en una mordida** (E2 20/20), consolida (E1 W_B 20/20), generaliza (**G1 1.000, azar 0.450; G2 0.997; K 20/20 — la batería imprime PASA**) | **xor01 estricta 0.500** [0.06, 0.88] contra 0.438 apagado [0.06, 0.75]; gana (0,1) **20/20** pero el residuo es ruido; celdas +9 %, splits +18 % en xor01 | `v15e_s141-160`, `examen_v15e_…093053` |
| B-5 desambiguar códigos (09:12) | alias de código: sal 0.0, veneno −3.0, exposiciones 517/475 contra 3 835/3 718, muertes 41 contra 75/77 (18/18) | nada (inerte en el tronco: examen 8/8 y generalización 40/40 **idénticos**) | `codigo_alias9`, `codigo_replica_alias9` |
| dE5 sorpresa en la boca (04:05) | recupera 0.25× (20/20 × 2), se apaga 20/20 | una semilla en E2 en compañía (133, 42 bocados) | `probar_si_mismo_s141-160`, `composicion_tres` |

**Detalle de v15e que importa a esta lente (leído del JSON del examen, no del log):** V1 cae **19/20 en dos subcriterios**: E1
"veneno Q4 < Q1" en la semilla **110** con mordidas de B **[14, 13, 10, 14]** (Q4 = Q1: empate de dos conteos pequeños, el criterio
es `<` estricto, `bateria_v14.py` L67) y E2I "W_C ≤ −2.5" en la semilla **102** (−2.41). Los dos están a **una semilla del
umbral → regla 12 de EQUIPO (réplica automática en rango nuevo)**, no son un fallo del mecanismo. Y una firma del residuo dentro
de los mundos del tronco: en E2I, **W_D = −4.0 en 18/20 semillas** para un patrón que nunca estuvo presente (v14.1 en E1: −2.5 en
19/20): la casilla ganadora guarda `R − lineal(C_última)` y la lectura de D es `lineal(D) + ese residuo` = −2.5 − 3 + 1.5. No lo
mira ningún criterio, pero es exactamente el mecanismo por el que xor01 cae: *la tabla de residuos hereda el error de la lineal*
(A16). El veredicto "NO ENTRA" se sostiene por V2b (0.500 < 0.75), como A predijo tras el humo.

### 1.5 Nota de instrumento (candidata a ERR; lo numera el coordinador)

`corre_v15e.py` L200: `g1az = num(r"G1 valor[^\n]*azar ([0-9.]+)", txt3)`. El `[^\n]*` es voraz y sobre la línea real del log
(`… px0 1.000 (>=0.65), azar 0.450, px0>azar 20/20`) captura el **último** "azar" → **20.000** (lo comprobé con el regex sobre la
línea: voraz → `20`; no voraz `[^\n]*?` → `0.450`). Por eso el runner imprime `V2a … (azar 20.000) … NO` y marca V2a como caída
cuando **la batería la declara PASA** (G1 1.000, azar 0.450, G2 0.997, azar 0.469, K 20/20). No cambia el veredicto final (V2b
decide), pero cambia la lectura: **v15e no cae por generalización ni por reversión; cae sólo por XOR**. Cuarto defecto de
instrumento en tres candidatos en 90 minutos (ERR-38, ERR-41, ERR-42 y éste), todos en baterías/runners copiados a mano.

### 1.6 La frontera, en un párrafo

El tronco v14.1 (06:05) aprende un valor en ≈ 4 mordidas (lenta) y lo consolida en ≈ 25 (rápida), pero la puerta entrega la boca a
la vía lenta de consolidar desde la mordida 5, así que la **conducta** asocia en ≈ 25 mordidas; desaprende lo temido sólo mordiendo
bajo hambre (pb 0.025 a −3) en 2 000–10 000 pasos, y el único órgano que lo acorta 4× (dE5) lleva 5 h como candidato; retiene 20/20
lo que ve y **0.67** lo que deja de ver; generaliza lineal 1.000 / 0.95–0.97; resuelve XOR sólo con un prior de pares (n\* = 7–10)
o con 14 ejemplos (n\* = 200); no aprende nada sin morder (5 740 encuentros con veneno por corrida sin efecto). La memoria de un
golpe traída al tronco **o no se desdice (v15d) o se desdice y pierde la identificabilidad (v15e)**; y los dos candidatos que
pasan todo (B-5, dE5) esperan una decisión. Ningún órgano ha entrado desde las 06:05, y la última entrada fue un cambio de dos
constantes, no un órgano.

---

## 2. Qué nos bloquea, ordenado por importancia (con evidencia, coste y desbloqueo)

### B1 — El canje del estimador: escribir de un golpe ↔ desdecirse ↔ identificar (el bloqueo de la columna vertebral)

- **Evidencia.** v15d: guarda R crudo → cruza XOR (0.875) y generaliza (1.000/0.999) pero **E2 0/20, E1 0/20** (`examen_v15d_…083108`,
  registro 08:38): una casilla escrita una vez no se corrige porque, al leer 1.45·R, la boca deja de morder (pb 1.1·10⁻⁴) y sin
  mordidas no hay error. v15e: cada vía su error + sobrescritura del residuo → **E2 20/20, E1 W_B 20/20, G1 1.000**, pero **xor01
  0.500** (gana (0,1) 20/20 y la casilla es ruido de ±1.6 porque la lineal oscila sobre XOR; `v15e_s141-160`, A16 §5).
- **Por qué bloquea.** Es el frente único del director (aprender sin morder / pocas exposiciones): la única familia que cruza XOR
  con 8 ejemplos (M3/M4, sala de 19 agentes) no sabe todavía **desdecirse sin perder lo que la identifica**. Cada versión arregla
  una mitad: R crudo identifica y no se desdice; residuo se desdice y no identifica.
- **Qué lo desbloquearía.** La propuesta v15f de A (A16, no construida): **R crudo + sobrescritura + relevo** (la tabla si la casilla
  ganadora se vio, si no la lineal; cada vía con su error; ganadora por error de la casilla sola). Predicción de A: E1/E2 como v15e,
  xor01 0.80–0.88, px0 ≥ OFF; riesgo declarado: px0 < OFF si la ganadora no contiene el píxel 0 (el relevo tapa a la lineal).
  Desde esta lente añado un control que puede tumbarla: **n\* de reversión en la tabla** (mordidas desde el cambio hasta que la
  casilla cambia de signo) debe ser **1**, y el coste conductual de leer R exacto a la primera (menos mordidas de veneno → menos
  conflictos → menos divisiones: v15e −18 %/+18 %) se reporta pareado.
- **Coste.** ~1 h de construcción por anclas + identidad 32/32 + 10 min de `Pool` (V1 3 min, V2a 1 min, V2b 5 min); semillas
  101–120 y 141–160 ya "gastadas" por v15e con la misma letra → **rango nuevo** (161–180 / 181–200 o los siguientes libres).

### B2 — La conducta la gobierna la vía más lenta (la puerta) y desaprender depende del hambre, no de la sorpresa

- **Evidencia.** `_fam` (L58–60): familiar = código mordido ≥ 5 veces y ≥ 1 celda consolidada → la boca lee la rápida (0.09/mordida,
  ≈ 24 mordidas) aunque la lenta ya esté en −3.00 (E1 v15e: mordidas de B por cuarto **25.5** contra 27 de v14.1). Reversión de
  −3 → +1: pb = 0.025 con hambre 1 → 2 000–10 000 pasos; dE5 lo baja a 0.25× (dos series) y espera desde las 04:47.
- **Por qué bloquea.** La medida que manda desde las 05:10 es *exposiciones hasta asociar*; con esta puerta, **ninguna mejora en el
  estimador se ve en la conducta** después de la quinta mordida, y ninguna aparece en la reversión sin un órgano que decida *probar*.
  El organismo tiene el reloj rápido (lenta 4 mordidas, tabla 1) y no lo usa para actuar.
- **Qué lo desbloquearía.** (a) Decisión del director sobre dE5 (ya cumple examen 8/8, retención 20/20 × 6, G1 = base, dos series;
  falta gemelo + tag ≈ 30 min; su semilla 133 dispara la regla 12: réplica del examen compuesto en un rango nuevo, 3 min).
  (b) Preregistro nuevo, un cambio: **puerta por confianza** en vez de por familiaridad — la boca lee la vía con **menor error propio**
  (EMA del error de cada vía, memoria: 2 escalares; la tabla M3 ya lleva ese error por celda). Predicción: mordidas de B en Q1 de E1
  bajan de ≈ 25 a ≈ 5–8 sin perder E1 W_B ≈ −3 (la rápida sigue recibiendo mordidas bajo hambre) ni la retención; refutación: E1
  W_B < 20/20 (la rápida se muere de hambre, el canje "el que acierta a la primera no repite" de A §6a).
- **Coste.** (a) 30–40 min; (b) 1 h + 10 min de `Pool`.

### B3 — El examen del tronco no mide la capacidad que manda y castiga por una semilla al que aprende rápido

- **Evidencia.** `bateria_v14.py` (copia de v13, criterio v3'): E1 "veneno Q4 < Q1" y E2 "come B Q4 ≥ 50" son conteos por cuartos de
  25 000 pasos; no existe **n\*** (mordidas o exposiciones hasta criterio) en ninguna batería del tronco, ni "retención de lo ausente",
  ni "aprender sin morder". Decisiones por una semilla en el umbral: E2 42 bocados (117, 133), E1 empate 14 = 14 (110 en v15e),
  E2I −2.41 (102). Cuatro veredictos de la noche se decidieron por una semilla (registro 04:45).
- **Por qué bloquea.** Un candidato que asocia en 1 mordida y otro en 24 **pasan igual**; uno que se desdice en 1 mordida y otro en
  3 + espera de hambre, **pasan igual**; el que retiene lo ausente al 0.67 y el que lo retendría al 0.9, **pasan igual**. La puerta al
  tronco protege lo viejo y es ciega a lo nuevo: por eso ningún candidato puede entrar *gracias* a la capacidad que buscamos, sólo
  *a pesar* del examen.
- **Qué lo desbloquearía.** `bateria_v15.py` por anclas (la congelada no se toca) con tres etapas nuevas, umbrales fijados con los
  números de v14.1 antes de correr (regla 11: ERR numerado por cambio de forma): **n\*_adq** (mordidas de B hasta |W_B + 3| < 0.3 y
  hasta que la boca lo rechace: v14.1 ≈ 24 / 5), **n\*_rev** (mordidas de A y de B desde `invertir_en` hasta el cambio de signo:
  v14.1 ≈ 3, y pasos hasta la primera mordida de B), **retención de lo ausente** (etapa del mundo largo: 0.67). Se corre sobre v14.1
  para fijar la referencia (3–4 min de `Pool`, una vez) y desde ahí todo candidato reporta exposiciones, como ordena el PLAN.
- **Coste.** Diseñador 1 h; 4 min de `Pool`; ningún riesgo para el tronco (sólo se mide).

### B4 — Retención de lo ausente 0.67: el valor vive en celdas compartidas y no hay segunda constante de tiempo

- **Evidencia.** `largo_s21-40`: 0.67 (V13), 0.50 con mapa; A-2 refutada (0.667 = base, +73 % muertes). Creador A y explorador: la
  masa de conflicto `m` tiene semivida ≈ 14 mordidas; hacen falta ≥ 2 constantes de tiempo propias (cascada de Fusi), no una prótesis.
- **Por qué bloquea.** "Desaprender" hoy incluye un olvido que nadie pidió: aprender 40 cosas nuevas borra un tercio de lo que no se
  ve. Para "que viva" (mundo vivo, población, reproducción) el organismo tiene que llevar lo aprendido a mundos donde lo viejo
  vuelve; con 0.67 no lo lleva.
- **Qué lo desbloquearía.** Un slot de valor **por nodo** (código exacto, la clave de `ncod` que ya existe) al lado del valor por
  celda, escrito de un golpe y leído cuando el nodo es conocido: no comparte celdas → no interfiere. Es el "grafo" del director en su
  forma mínima (§5–6). Predicción falsable: retención de lo ausente ≥ 0.80 con G1 ≥ 0.80 intacta (la generalización la sigue dando
  la lineal); refutación: G1 < 0.80 (vuelve el canje de v11) o muertes +50 %. Alternativa: dos constantes de tiempo en la rápida
  (Fusi), memoria +90 floats.
- **Coste.** Preregistro + constructor 1–2 h; `Pool` 5 min (mundo largo 20 semillas + baterías).

### B5 — Identidad del token y creación de nodos: el alias de código está reparado pero no entra; los nodos conjuntivos no nacen solos

- **Evidencia.** Alias (K = 3 de 90): algún par con el mismo código en **18/200** semillas del mundo de 4 estímulos (9 %) y en
  **170/200** del mundo de regla (135/200 con fuga a un patrón nunca visto); cuando ocurre, el que no informa hereda el valor y el
  veneno pierde la mitad del miedo (−1.45 contra −3.0; muertes 75 contra 35). B-5 lo repara 18/18 con una regla inerte en el tronco
  (identidad exacta): **candidato a v15 desde las 09:12, decisión del director**. Creación de rasgos conjuntivos por fisión: `P0·P1`
  el par más propuesto en **0/20** (criba); M2 refutado (0.313); el prior de M3 son **15 pares fijos** (C(6,2)) y "C(n,2) no lo es"
  (sala §6).
- **Por qué bloquea.** Sin identidad de token no hay nodo estable ("sal" y "veneno" son la misma cosa en 1 de 11 semillas), y sin
  creación de nodos a demanda el prior de pares no escala a una retina mayor: es un techo del "grafo" antes de construirlo.
- **Qué lo desbloquearía.** (a) B-5 al tronco: coste ≈ 0 (gemelo + tag; C4 reescrito como criterio de causa: "la división de la
  celda compartida precede a la caída de |W[sal]|"). (b) Para los nodos conjuntivos, honestidad: no hay mecanismo local que pase la
  criba con 8 ejemplos; lo que sí se puede preregistrar es el **disparador**: un nodo-par nace sólo cuando dos tokens co-activos
  reciben un R que contradice el valor de **los dos** padres (la fisión con el gatillo de M2 y la memoria de M3), y se mide en el
  mundo de 14 ejemplos (donde la información existe) antes que en el de 8.
- **Coste.** (a) 30 min. (b) 2 h + 10 min de `Pool`; probabilidad de cruzar con 8 ejemplos: baja (todo lo medido dice azar).

### B6 — Método: cada candidato al tronco corre sobre baterías y runners copiados a mano, y cada copia trajo un defecto

- **Evidencia.** ERR-38 (kwargs omitidos → vía lenta apagada, dos G1 anulados), ERR-41 (mundo de regla en config v13), ERR-42 (JSON
  del examen perdido), y el regex voraz de `corre_v15e.py` (§1.5: V2a "NO" con G1 1.000). Cuatro defectos, tres candidatos, 90 min.
- **Por qué bloquea.** Cada veredicto de la mañana necesitó una corrección después de correr; la regla 14 ya cubre las entradas de
  batería, no los runners. El coste no es sólo tiempo: el registro de las 08:06 dijo "rompe la generalización" y era falso.
- **Qué lo desbloquearía.** Un módulo compartido (`experimentos/comun/`: `KW14`, rutas de sha, parsers de las líneas de las
  baterías con tests de una línea, la etapa de umbrales) que los runners importen en vez de copiar; y un humo obligatorio que
  ejercite el parser sobre un log real. **Coste:** 1 h de un implementador; beneficio: deja de perderse una serie por un regex.

---

## 3. Por qué el tronco no cambia desde las 06:05 (v14.1)

1. **Lo que se intentó meter era la columna vertebral (XOR / un golpe) y choca con el examen por B1**: tres candidatos en 90 min,
   ninguno cumple V1 + V2a + V2b a la vez, y el fallo cambia de sitio en cada versión (v15d: E1/E2; v15e: xor01). No es mala suerte:
   es un canje real entre escribir de un golpe, corregir y identificar, que todavía no tiene el mecanismo que lo rompa (v15f es la
   primera propuesta que ataca las tres a la vez y está sin construir).
2. **Los candidatos que sí pasan todo son laterales y esperan al director**: dE5 (04:47; el director decidió a las 04:55 "los tres si
   pasan; si no, los dos" y lo dejó como candidato a v15), B-5 (09:12, "la entrada la decide el director"), A-3 vector único (00:36,
   simplificación). El tronco sólo cambia por decisión del director y esa decisión no se ha tomado en las últimas 3.5 h de mañana.
3. **El examen es ciego a la capacidad nueva (B3)**: aunque v15f cruzara, entraría por no romper nada, no por asociar en 1 mordida;
   y cualquier candidato rápido corre el riesgo de un empate de conteo (semilla 110) que dispara réplicas, no entradas.
4. **La instrumentación copiada a mano (B6) convirtió cada bloque en dos** (correr, corregir, releer): v15c quedó sin medir de verdad,
   v15d midió el mundo de regla en configuración v13, v15e tiene un V2a mal leído.
5. Lo que **no** es la causa: ni el `Pool` (cada serie tarda 5–10 min), ni la falta de ideas (A16, B-5, dE5, mundo vivo), ni la
   literatura (M3 salió de BTSP 2017/Milstein 2024 y de una búsqueda ciega, y convergieron).

---

## 4. Qué capacidad medible falta (desde esta lente)

- **n\* de reversión por patrón** (mordidas y pasos desde el cambio del mundo hasta que la boca cambia de signo). Hoy sólo existe
  como "recuperación en pasos" en un mundo aparte (C-P1) y como "come B Q4 ≥ 50" en el examen. Es la medida que distingue a un
  organismo que "puede aprender y desaprender" (hipótesis del director) de uno que sólo aprende.
- **n\* de adquisición en la conducta** (no en el valor): mordidas hasta que la boca rechaza el veneno con hambre 0.5. Hoy ≈ 25 por
  la puerta; con la lenta sola sería ≈ 4; con tabla, 1. Nadie lo mide en el tronco.
- **Retención de lo ausente** como etapa de batería (0.67 hoy) — sin ella, "recuerda" significa "recuerda lo que sigue viendo".
- **Aprender sin morder = 0 por construcción**: número de encuentros sin mordida que mueven un valor. Hoy es 0 (L107). La
  medida existe conceptualmente (A-1: 5 740 encuentros con veneno `00` por corrida) y ningún instrumento la reporta.
- **Exposiciones hasta asociar en un hijo** (nodo nacido por fisión/B-5): hoy la hija nace con el valor copiado (v11) o con 0 (B-5)
  y nadie mide cuántas mordidas necesita para tener valor propio. Es la medida natural del "sal rosa" del director.

---

## 5. La hipótesis del director, desde la dinámica

> *"si sal es sal será número uno, lo guardo, lo vectoriza; después sal rosa lo vectoriza, marca como sal y lo plantea como una
> variable de lo mismo — eso es lenguaje. Ahora, si pensamos en el aprendizaje, y ya lo hemos visto, que puede aprender y desaprender."*
> (09:40) · *"la palabra es grafo, no vectorización"* (05:10).

**Qué ya hace el organismo (y con qué línea):**
- **"Sal es sal, número uno, lo guardo"** = el código de Kenyon (`code(P)`, L42–43: 3 celdas de 90) es el **token**, y `ncod`
  (L51, L109–111) es el **registro de tokens exactos** con su evidencia (la puerta por código cuenta cuántas veces se mordió cada
  código exacto). El tronco ya tokeniza y ya guarda por token; lo que **no** guarda por token es el **valor** (vive en las celdas).
- **"Lo vectoriza"** = la vía lenta (`Wps−Wns ∈ ℝ⁶`, L50, L119–120): la lectura lineal de la retina, que es lo que generaliza
  (G1 1.000). El vector existe y es "sólo soporte", como pide el director: la boca lo consulta cuando el token no es familiar.
- **"Sal rosa … variable de lo mismo"** = dos operaciones locales que ya crean un token nuevo a partir de otro: la **fisión por
  conflicto de signo** de v11 (L144–149: la hija nace ciega fuera del patrón nuevo, hereda el signo nuevo, la madre conserva el
  viejo) y la **división por R = 0 bajo retina distinta** de B-5 (la hija nace sin valor). La condición `kj@P > KW[c]@P` **es la
  prueba local de "esto es una variable de lo mismo o es otra cosa"** (misma retina → no divide; retina distinta → divide).
  El caso literal de la sal ya está medido: con K = 3, "sal" y "veneno" reciben el mismo token en 2/20 semillas; B-5 hace de la
  sal un token propio y el veneno recupera −3.0 (18/18).
- **"Puede aprender y desaprender"**: sí, con los relojes de §1.1–1.2 — 4 mordidas para aprender un valor, 3 para cambiarle el
  signo si lo muerde, 2 000–10 000 pasos hasta morderlo si lo teme.
- **Nodos conjuntivos** = la tabla de pares de M3 (15 nodos, 4 casillas): es un grafo de pares con valor por nodo, escrito de un
  golpe y con competencia local por error propio — y es lo único que cruzó XOR con 8 ejemplos.

**Qué NO hace (y por qué importa para "aprender y desaprender"):**
- **No hay aristas explícitas.** La fisión sólo deja `split_t = (t, kk)`; no se guarda `padre[j] = c`. La hija y la madre son
  independientes desde el nacimiento: si el mundo enseña algo nuevo a "sal", "sal rosa" no se entera, y viceversa. La única relación
  entre tokens es **implícita** (celdas compartidas), y esa relación es exactamente la interferencia (0.67) y el alias.
- **No hay lectura por parentesco.** Un token sin evidencia lee la lineal (vector), no a su madre. La "variable de lo mismo" del
  director es una **lectura por defecto desde el padre**; hoy la hija de v11 hereda el valor **copiado** (un número, no una arista) y
  la de B-5 hereda 0.
- **El valor no vive en el nodo.** Por eso hay interferencia (B4) y por eso el mundo vivo tuvo que poner el valor "por necesidad"
  (indexar la memoria) para resolver su XOR: cuando el valor está indexado por lo correcto, el XOR se disuelve en 11 exposiciones;
  cuando está en celdas compartidas, no.
- **Desaprender en un grafo exige una regla para decidir entre sobrescribir y dividir**, y hoy sólo existe para dos casos: conflicto
  de signo (v11 → divide) y R = 0 (B-5 → divide). Para "el mismo nodo cambió de valor" el tronco usa EMA (lento) y v15e usa
  sobrescritura (1 mordida, E2 20/20). Lo que v15d/v15e enseñan: **un nodo escrito de un golpe que no se sobrescribe no se desdice;
  y si guarda residuos en vez de R, se desdice pero deja de identificar.** La regla que falta es local y ya tiene sus piezas: error
  propio del nodo (EMA, M3 lo lleva) + prueba de retina (`kj@P > KW[c]@P`).
- **La identificabilidad no la arregla el grafo.** Con 8 ejemplos, 9/15 hipótesis empatan; un grafo sólo ayuda si sus aristas
  codifican el prior ("los nodos que importan son pares de tokens co-activos"), y eso ya está medido como prior, no como aprendizaje.
- **Una trampa dinámica propia de "heredar el valor"**, que hay que decir antes de construir nada: si "sal rosa" hereda −3 de
  "sal", la boca la evita (pb 0.025 con hambre 1) y **la corrección tarda ≈ 100 encuentros** (el bloque de la sal lo midió por otro
  camino: evitación ×7, 3 835 exposiciones); si hereda +1, se corrige en 1 mordida. La herencia de miedo se protege a sí misma
  contra la corrección. Es la misma asimetría (−3/+1, lo rechazado se queda en el anillo) que cerró N2. Por eso B-5 hace nacer a la
  hija **sin** valor, y por eso el grafo necesita el órgano de muestreo (dE5) como compañero, no como alternativa.
- **"Eso es lenguaje"**: vocabulario prohibido por la regla 6/8 hasta que haya prueba; lo que se puede declarar es *tokeniza,
  divide tokens, hereda valor al nacer, generaliza por el vector*.

**Cómo se operacionalizaría con reglas locales (esbozo preregistrable, un cambio por bloque; no construido, no medido):**
1. **Nodo con valor** (bloque 1, ataca B4): `V[key]` y `e[key]` (valor y error propio EMA) por clave de `ncod`; escritura de un
   golpe con **R crudo y sobrescritura** (lo que v15e demostró que se desdice en 1 mordida) sobre el nodo **exacto** (no por pares:
   sin prior, sin identificabilidad que perder); lectura: nodo si `ncod[key] ≥ 1`, si no la lineal. Memoria: 2 floats por token
   visto (≈ 30–60). Predicción: retención de lo ausente ≥ 0.80 (0.67), n\*_adq del valor en la boca = 1, E1/E2 como v15e, G1 ≥ 0.80
   por la lineal; refutación: G1 < 0.80, muertes +50 %, o E1 W_B < 20/20 (la rápida se muere de hambre).
2. **Arista y lectura por parentesco** (bloque 2, el "sal rosa"): `padre[j] = c` al nacer (90 ints); un nodo hijo sin evidencia lee
   `V[padre]` **sólo si el valor del padre es ≥ 0** (la trampa de arriba, declarada) y, si es negativo, lee 0 y deja que la sorpresa
   en la boca (dE5) decida probar. Medida principal: exposiciones hasta asociar en el hijo (predicción: 0–1 donde el padre acierta).
3. **Sobrescribir o dividir** (bloque 3, el "desaprender"): sobre el nodo conocido, si `|R − V[key]| > θ` y la retina es la misma
   (`kj@P ≤ KW[c]@P`) → sobrescribir (el mundo cambió); si la retina es distinta → dividir (v11/B-5: es otra cosa). Medida: n\*_rev = 1
   en E2 para el nodo; 0 divisiones espurias en E1 (4b/4c intactos).
4. **Nodos conjuntivos a demanda** (bloque 4, sólo en el mundo de 14 ejemplos primero): nace un nodo-par cuando dos tokens co-activos
   reciben un R que contradice el valor de ambos padres; competencia por error propio (M3). Con 8 ejemplos se predice honestamente
   que **no cruza** (todo lo medido dice azar); con 14, que iguala a la regla local (1.000) con n\* ≪ 200.
   Todo con identidad bit a bit con las perillas apagadas, exposiciones como número principal, `azar` en [0.35, 0.65], px0 = 1.000.

---

## 6. Si fuera mi creación: cómo le daría vida (orden, en una sesión)

1. **Primero la regla del juego (B3, 1 h + 4 min):** `bateria_v15.py` por anclas con n\*_adq, n\*_rev y retención de lo ausente,
   referencia fijada sobre v14.1. Sin esto ningún candidato de velocidad puede entrar por lo que aporta.
2. **Cerrar lo que ya pasó (B2a, B5a, 40 min):** dE5 y B-5 al tronco por decisión del director (réplica del examen compuesto de dE5
   en un rango nuevo por la semilla 133, regla 12). Desde esta lente, dE5 es el único órgano medido que acorta el desaprender.
3. **v15f (B1, 1 h + 10 min)** con el control de n\*_rev = 1 añadido; rango de semillas nuevo.
4. **Nodo con valor (B4/§5-1)** en el mundo largo: la primera prueba del grafo que puede fallar limpio (retención 0.67 → ≥ 0.80 sin
   perder G1).
5. **Parentesco y sobrescribir/dividir (§5-2/3)** en el mundo vivo (la sal es el caso natural).
6. **El módulo común de runners (B6, 1 h)** antes del punto 3, o cada bloque volverá a costar dos.

Lo que no haría: buscar otra regla para 8 ejemplos (está demostrado que no hay información), ni meter nada al tronco por
exposiciones sin la batería de exposiciones (sería recalibrar por el resultado).

---

## 7. Fuentes

`organismo/organismo_v14.py` (L42–60, L101–129, L144–149, L158) · `organismo/bateria_v14.py` (L67–75) ·
`experimentos/creacion_A/corre_v15e.py` (L198–204, L241–247) · `datos/examen_v15e_20260918_093053.{log,json}` ·
`datos/v15e_s141-160_20260918_092921.{log,json}` · `datos/regresion_generaliza_v15e_organismo_v15e_on_20260918_093352.log` ·
`datos/v15e_humo_20260918_091900` · `experimentos/creacion_A/PREREGISTRO_v15e.md` · `registro/investigacion/PUENTE_creacion.md`
(A12–A16, B-5) · `registro/investigacion/ENJAMBRE_xor_20260918.md` · `registro/REGISTRO_etapas_1_2.md` (mundo largo 3152/3226;
A-2 3760; C-P1 3839–4200; composición 4241; A-4 4407; v14.1 4456; A-6 4466; ERR-35 4559; XOR 4617/4652; mundo vivo 4671/4761;
ERR-37 4706; v15c 4730; sal 4784; ERR-38 4811; v15d 4835; B-5 4865/4916; reproducción 4944; ERR-41/42 4986) ·
`registro/HANDOFF.md` §13, §15.7–15.8 · `registro/PLAN.md` · `CLAUDE.md` (día 7) ·
`experimentos/nivel11_mundo_vivo/PREREGISTRO_mundo_vivo.md`, `PREREGISTRO_reproduccion.md`.
