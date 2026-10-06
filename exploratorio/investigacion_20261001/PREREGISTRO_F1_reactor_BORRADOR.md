# PREREGISTRO (BORRADOR v2) — F1 del Reactor: barrido de tamaño en BLOQUES, esc 90 frente a esc 900 (1-oct-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo.

**Estado: BORRADOR v2. No se congela ni se corre hoy: es entrada del plan para el PC nuevo.** No hay runner ni arnés de F1. Lo corrido
por el creador es sólo `f1_nulo.py` (numpy, un proceso; sha `49593c01eb0aac0d`) → `f1_nulo_salida.txt` (sha `9aada750fbda2f61`), que
simula las puertas y LEE JSON ya guardados (BLOQUES y la sonda del coordinador). La v1 queda en `PREREGISTRO_F1_reactor_BORRADOR_v1.md`.

Rutas: `ORG` = `C:\Users\User\Documents\PROYECTOS\JUACO\organelos\`; `OPM` = `ORG\experimentos\organelos\bloques\opusM\`;
`REA` = `ORG\experimentos\organelos\reactor\`; `NUL` = `f1_nulo_salida.txt`.
Marcas: [V] leído o medido de archivos guardados · [S] sonda del coordinador, UNA semilla por escala, T 200 000: calibración, no
resultado · [I] inferencia · [P] proyección o propuesta no medida.

## Cambios v1 → v2

1. **Dos lecturas co-principales en direcciones contrarias**, las dos con el órgano de rechazo (`pixF[AC]->boca+`) excluido:
   L1 = formas funcionales FIJADAS (≥ 50 %), la de la ficha; L2 = **diversidad funcional sostenida** (formas funcionales en ≥ 5 % de los
   vivos). Tabla de desenlaces 3 × 3 (§7f): el experimento informa gane quien gane. La innovación de dos pasos queda descriptiva (§7g).
2. **Comparación a PROFUNDIDAD IGUAL** (reloj A), con el mismo T en los dos tamaños y regla mecánica de lectura (§9c).
3. **Error de v1 corregido: n0 = 900 es imposible** (`ECO_NMAX = 400`, `ORG\experimentos\juaco_eco\motor_eco.py:76`). v2 fija **n0 = 90
   en los dos tamaños** y **tope 3000 en los dos** (v1 decía 900 y 30 000). Es lo que probó la sonda.
4. **Costos llenos** (§12) con la sonda; lo no medido va marcado.
5. **Telemetría: ya existe** en `REA\sonda_reactor.py` (sha `3bd8b95238400f3e`). v2 la cita como instrumento y lista sólo lo que le falta (§9d).
6. **Relojes recalibrados** con lo medido: A ≈ 11.6–15.7 a T 200k y +6 a +10 por 100k; B = 45 por 100k. Los umbrales (≥ 20 y ≥ 150)
   se mantienen; a T 500k serían alcanzables por PROYECCIÓN NO MEDIDA (§9b). El reloj A pasa de "mediana" a "media de los vivos",
   que es lo que calcula la sonda.
7. **Semillas: 49801–49840** (las del coordinador; verificadas en los tres repos, §4). Se dejan las 551xx.
8. **Paso 0: PENDIENTE**, lo corre el coordinador en `REA\paso0_ablacion.py`. Con el rechazo excluido, c pasa de {2, 3} a {1, 2} (§7b).
9. **Reconciliación 14/20 contra 13/20** (§6f): las dos cuentas son correctas para su letra; se conserva la canónica y se dice por qué.
10. Predicción propia actualizada (§7h): la sonda no muestra más diversidad a ≥ 5 % con N grande.

## 1. Hipótesis

Mismo motor, mismas tasas, mismo mundo por cuerpo; población ×10 (esc 900, ≈ 360 vivos, frente a esc 90, ≈ 36 vivos).

- **H-FIJ (la de la ficha):** a esc 900 se fijan más formas funcionales distintas por semilla, sin contar el órgano de rechazo.
- **H-DIV (co-principal, dirección contraria):** a esc 900, a profundidad mutacional igual, se sostienen más formas funcionales
  distintas en ≥ 5 % de los vivos.
- **Lectura de la sonda [S]:** a T 200k hay UNA forma fijada (el rechazo) a esc 300, 900 y 1200, y las formas presentes (`tipo()`, con
  uno o más portadores) suben 26 → 38 → 49 (`REA\sonda_salida.txt:1-3`). N grande parece retardar la fijación y sostener más variantes
  raras. Pero con el umbral del 5 % la misma sonda da 3, 2 y 4 formas, y esc 90 a T 200k da 1 y 2 de mediana [V, `NUL` §F]: el
  aumento visto es casi todo de variantes bajo el 5 %, es decir, muestreo.

## 2. Mecanismo mínimo y memoria nueva

Motor de BLOQUES sin tocar. **Memoria nueva de conducta: cero.** Entre brazos de tamaño sólo cambia `esc` (90 → 900). La telemetría son
ganchos de sólo lectura que no consumen azar del motor (`REA\sonda_reactor.py:11-15`).

## 3. Brazos

| brazo | esc | n0 | tope | donante | papel |
|---|---|---|---|---|---|
| BLOQ_V@90 | 90 | 90 | 3 000 | padre | base (réplica interna de BLOQUES) |
| BLOQ_V@900 | 900 | 90 | 3 000 | padre | hipótesis |
| BLOQ_AZA_V@90 | 90 | 90 | 3 000 | azar | control sin herencia |
| BLOQ_AZA_V@900 | 900 | 90 | 3 000 | azar | control sin herencia (no probado a esc grande) |

**80 corridas por serie** (aceptado por el coordinador), más las ablaciones de §6d.

**Decisiones fijadas:**
- **esc 900, no ≈ 1250.** Es el ×10 exacto de la ficha (36 → 359 vivos [S]); está probado por la sonda; cuesta un 25 % menos. Con
  esc 1250 habría ≈ 500 vivos, pero ese punto no se probó (sí 1200: 480 vivos). El Reactor de 500 cuerpos es otra ficha.
- **n0 = 90 en los dos tamaños.** Idéntico a BLOQUES, probado [S], y deja como única diferencia el tamaño del mundo. n0 = 400 no se probó
  y cambiaría además el número de plazas del vivero. Consecuencia declarada: a esc 900 el vivero siembra el mismo número de plazas en
  un anillo ×10; la población llega a ≈ 0.40 × esc por nacimientos, no por fundadores.
- **"Linaje"** = índice de plaza fundadora `I_LIN` (0–89), como en BLOQUES (`OPM\motor_bloques.py:1280,1331,1361`). Es una etiqueta del
  vivero, NO un clado genético: un refundado toma su genoma del banco, que puede venir de otra plaza (`motor_bloques.py:854-863`).
  Colapsa tras el corte: 90 → 10 / 24 / 27 a 140k → 5 / 12 / 10 a 200k (esc 300 / 900 / 1200) [S]; a esc 90 y T 500k queda 1 en las 38
  semillas viejas que persisten [V, `NUL` §D].
- **"Clado"** (lo que sí mide ascendencia): descendientes genéticos de un mismo cuerpo vivo en t_corte, por la genealogía de la sonda
  (`sonda_reactor.py:148-156`). Se reportan los dos: `linajes_T` y `clados_T`. Ninguno entra en las puertas.

**Idéntico a BLOQUES (cita):**
- Tasas `p_campo 0.10, p_dup 0.02, p_ins 0.02, p_hgt 0.01, p_del 0.05, banco 200`, arranque vacío — `OPM\corre_bloques.py:38`;
  `OPM\PREREGISTRO_bloques.md:25-28,32`.
- Operadores y orden — `OPM\motor_bloques.py:810-833`; `NRMAX = 12` — `:115`; regla al azar — `:805-807`.
- Herencia y banco, donante `padre` / `azar` — `motor_bloques.py:836-863`; brazos `_V`, t_corte 100 000 — `corre_bloques.py:43-46`.
- Mundo w90: `MUNDO = dict(esc=90, n0=90, carro='FABRICA_ECO', tope=3000, muestra=1000)` —
  `ORG\experimentos\juaco_eco\corre_eco.py:31`; entra por `mundo_n=MUNDO['esc']` —
  `ORG\experimentos\organelos\eco_sel_ing\nucleo_eco_sel_ing.py:168`. L = 40·esc, 4·esc objetos — `motor_eco.py:12`.
- **T = 500 000, t_corte = 100 000** — `corre_bloques.py:201-202`.
- K — `corre_bloques.py:111-117`; `persiste` — `nucleo_eco_sel_ing.py:194`; `vivos_T` — `motor_bloques.py:898-902`.
- Órgano de rechazo — `corre_bloques.py:131-142`; P4 de BLOQUES — `:234-236`; registrado 19/20 y 18/20 —
  `ORG\registro\REGISTRO_etapas_1_2.md:7122`.

**Distinto:** sólo `esc` en los brazos @900, puesto como lo hace la sonda (`sonda_reactor.py:193-196`, restaurado en `:205`).
Límites duros: `ECO_NMAX 400`, `ECO_ESC_MAX 2000` (`motor_eco.py:76-77`), `NRMAX 12`. El banco de 200 no escala (§11).

## 4. Semillas (NUEVAS)

- **Serie 49801–49820 · réplica 49821–49840** (propuesta del coordinador). Grep del 1-oct en `organelos`, `o1libre` y `bundle`
  (experimentos y registro; `.md`, `.py`, `.txt`): en 49801–49840 sólo aparece `49835.0`, un valor de tabla en
  `experimentos\organelos\boca_buena\tabla_bb.txt:12`, no una semilla. **Libres en los tres.**
- Las 551xx de v1 se dejan: el Paso 0 ya usa 55151–55155 (`REA\paso0_ablacion.py:27`).
- Práctica y humo de F1: 49841–49846. Ablación de F1 (§6d): 49861–49865. Usadas por la sonda: 49701–49709 (`sonda_reactor.py:17,268`).
- Las mismas 20 semillas en los 4 brazos. Entre tamaños no es diseño pareado: se comparan distribuciones por brazo.

## 5. Medidas (por semilla y brazo; todas al JSON)

`persiste`, K, K_nac, vivos, `linajes_T`, `clados_T`, largo medio, `frac_rechazo`, formas fijadas y D5 (§6), sus versiones funcionales
(§6d), testigos silenciosos, relojes A y B (§9), composición del mundo y llegadas perdidas (`corre_bloques.py:79-83`). Todo en el punto
de lectura de §9c y además en T.

## 6. Definición operativa, letra por código

Código de referencia: `f1_nulo.py` §D y §E–F (corre sobre los JSON guardados). El Paso 0 ya lo copió campo a campo
(`REA\paso0_ablacion.py:7-11`).

```python
PATM = {'A': (1,1,0,1,0,0), 'B': (1,0,1,0,1,0), 'C': (0,1,1,0,0,1), 'D': (0,0,1,0,1,1)}   # corre_bloques.py:128
SENT = ['hambre','sed','cerca','pixF','pixM','Rult']; ACC = ['boca','hacia','quieto','parir']
W_SIL = 0.25; FRAC_FIJ = 0.5; MIN_VIVOS = 12
RECH = (('pixF', (1, 0, 1, 0)), 'boca', '+')            # el organo de rechazo: SE EXCLUYE de L1 y de L2

def condicion(r):                      # r = [sentido, parametro, comparador, theta, accion, peso]
    s, p, c, th = int(r[0]), int(r[1]), (r[2] > 0.5), float(r[3])
    if s in (3, 4):                    # pixel j: tabla de verdad sobre A, B, C, D
        m = tuple(int((PATM[x][p] > th) if c else (PATM[x][p] < th)) for x in 'ABCD')
        if sum(m) in (0, 4): return None                    # nunca / siempre: silenciosa
        if m[0] == 1: return (SENT[s], m), 1                # orientacion canonica: la mascara que contiene a A
        return (SENT[s], tuple(1 - z for z in m)), -1       # complemento, con el signo del peso cambiado
    if (c and th >= 1.0) or ((not c) and th <= 0.0): return None
    return (SENT[s], '>'), (1 if c else -1)                 # theta no cuenta; '<' es '>' con el signo cambiado

def formas_cuerpo(reglas):
    W = {}
    for r in reglas:
        cg = condicion(r)
        if cg is None: continue
        k = (cg[0], ACC[int(r[4])]); W[k] = W.get(k, 0.0) + cg[1] * float(r[5])   # los duplicados SUMAN peso
    return {(k[0], k[1], '+' if w > 0 else '-') for k, w in W.items() if abs(w) >= W_SIL}

def frecs(vivos):
    cnt = {}
    for x in vivos:
        for f in formas_cuerpo(x[3]): cnt[f] = cnt.get(f, 0) + 1
    return cnt

def fijadas(vivos):                    # L1: >= 50 % de los vivos, sin el rechazo
    n = len(vivos)
    return set() if n < MIN_VIVOS else {f for f, c in frecs(vivos).items() if f != RECH and c / n >= FRAC_FIJ}

def sostenidas(vivos):                 # L2 (D5): >= 5 % de los vivos y >= 3 portadores, sin el rechazo
    n = len(vivos)
    return None if n < MIN_VIVOS else {f for f, c in frecs(vivos).items() if f != RECH and c / n >= 0.05 and c >= 3}

def d_rar(vivos, formas_ok, rng, m=24, reps=200):   # L2 rarificada: misma resolucion en los dos tamanos
    if len(vivos) < m: return None
    F = [formas_cuerpo(x[3]) & formas_ok for x in vivos]; tot = 0
    for _ in range(reps):
        cnt = {}
        for i in rng.choice(len(F), m, replace=False):
            for f in F[i]: cnt[f] = cnt.get(f, 0) + 1
        tot += sum(1 for c in cnt.values() if c >= 2)
    return tot / reps
```

**a. Campos.** Forma = (sentido, condición canónica, acción, signo del peso total). En píxeles la condición es la tabla de verdad sobre
A, B, C, D (tres particiones posibles con los 6 píxeles de `PATM`); en sentidos continuos θ no cuenta. Una regla y su complemento con el
signo cambiado son la misma forma. Total: 48 + 32 = **80 formas canónicas**.

**b. Pesos, duplicados, silenciosas.** Las copias de una misma (condición, acción) se suman. La forma cuenta en un cuerpo sólo si
|peso total| ≥ 0.25. Silenciosa = condición constante o peso total bajo ese umbral. Los testigos silenciosos (condición nunca cierta,
clave cruda) se cuentan aparte con las mismas fracciones.

**c. "Fijada" y "sostenida".** Fijada: ≥ 50 % de los vivos. Sostenida: ≥ 5 % de los vivos y ≥ 3 portadores. Las dos piden ≥ 12 vivos;
con menos, L1 cuenta 0 y L2 queda sin dato (se reporta cuántas semillas). A esc 90, 3 portadores de 36 son el 8.3 %: el umbral efectivo
es más duro en la población chica. Por eso la puerta de L2 exige además la versión rarificada (§7c).

**d. "Funcional" — paso del runner, exige motor.** Ablación por trasplante, el instrumento de `REA\paso0_ablacion.py` (sha
`7caff37b6aaeec21`; brazo FORZ_V, tasas 0, `corre_bloques.py:53-60`):
1. Clases a probar, por brazo y serie: toda forma fijada (para L1) o sostenida (para L2) en ≥ 2 semillas. Las de una sola semilla
   cuentan como no funcionales, igual en los dos tamaños.
2. G+ = en la semilla donde la forma tiene mayor fracción (empate: la menor), la lista exacta de reglas más frecuente entre sus
   portadores (empate: mayor `gen`, luego el primero). G− = G+ sin todas las reglas de esa (condición, acción).
3. G+ y G− como `forzada`, t_corte 100 000, T 200 000, **al esc de origen**, semillas 49861–49865. K en [100 000, 200 000].
4. **Funcional** si K(G+) > K(G−) en 5/5 y la mediana de la diferencia ≥ 5 % de la mediana de K(G+). Nulo de signo: 0.031 por clase.
5. `n_fij(semilla)` y `D5(semilla)` cuentan sólo formas de clases funcionales a ese tamaño.

**e. "Distintas".** Tuplas canónicas diferentes después de (a) y (b).

**f. Reconciliación con la cuenta del coordinador (14/20 y 13/20 con `tipo()`; v1 dio 13/20 y 13/20).** Las dos cuentas son correctas
para su letra [V, `NUL` §E]. Con `corre_bloques.tipo` (240 formas, `corre_bloques.py:120-125`) reproduzco 14/20 y 13/20. La única
semilla que cambia de lado es **48426**: `tipo()` le cuenta tres formas, pero dos de ellas (`pixF1>θ -> hacia-`, `pixF4>θ -> parir-`)
tienen θ = 1.0 con comparador `>` en sus copias mayoritarias: "píxel > 1" nunca se cumple. Son reglas muertas que viajan con el linaje.
**Para "formas funcionales" la cuenta correcta es la canónica (13/20).** `tipo()` además cuenta como distintas "píxel 4 > θ" y
"píxel 1 < θ", que son el mismo órgano. Se conserva la canónica; `tipo()` se reporta al lado para enlazar con BLOQUES y con la sonda.

## 7. Nulos y puertas

### 7a. L1 — formas fijadas (puerta de diferencia; nulo de v1, sin cambios)

X = 1 si `n_fij ≥ c`. `k90`, `k900` = semillas con X = 1 en BLOQ_V. **L1+ si `k900 − k90 ≥ 7` y `k900 ≥ 10`; L1− es el espejo
(`k90 − k900 ≥ 7` y `k90 ≥ 10`).** Exacto, binomial [`NUL` §A]:

| puerta | FP máx. serie | FP serie Y réplica | 0.10→0.70 | 0.25→0.75 | 0.25→0.60 | 0.40→0.80 |
|---|---|---|---|---|---|---|
| ficha (≥ 12 vs ≤ 5) | 0.0075 | 5.6e-5 | 0.88 (0.77) | 0.59 (0.35) | 0.37 (0.14) | 0.12 (0.02) |
| **diferencia ≥ 7, k ≥ 10** | **0.019** | **3.7e-4** | 0.97 (0.95) | 0.90 (0.80) | 0.57 (0.32) | 0.71 (0.50) |

Con sobredispersión por lote el FP de una serie sube a 0.015–0.068 (`NUL` §B2): una serie sola no declara.

### 7b. Paso 0 — calibración de c — **PENDIENTE (coordinador)**

Base SIN filtro de función, rechazo excluido, esc 90, T 500k [V, `NUL` §F]: otra forma fijada (c = 1) en **13/20 y 13/20**; dos o más
(c = 2) en 3/20 y 8/20. Regla fija: **c = el menor de {1, 2} cuya base FUNCIONAL agrupada sea ≤ 12/40**; si ninguno, c = 2 y se
declara "potencia baja".

> **PENDIENTE — resultado del Paso 0** (`REA\paso0_ablacion.py`, salida `REA\paso0_salida.txt`):
> clases funcionales = ______ · base funcional c = 1: __/40 · c = 2: __/40 · **c fijado = __**

El creador vio las primeras 19 líneas de `paso0_salida.txt` (el rechazo: K ≈ 38 contra ≈ 1.5; `pixF[AC]->hacia+` a medias). No se usó
para decidir nada de este documento.

### 7c. L2 — diversidad funcional sostenida (nulo nuevo)

Por semilla: **D5** = número de formas funcionales sostenidas (§6c, §6d), en el punto de lectura de §9c. Dos brazos de 20, no pareados.
**L2+ si** (i) Mann–Whitney unilateral de D5(900) > D5(90) con **z ≥ 2.326**, (ii) **diferencia de medianas ≥ 1 forma**, y
(iii) normalización: la versión rarificada `d_rar` (24 vivos, ≥ 2 portadores, 200 submuestras, rng fijo) va en el mismo sentido con
z ≥ 1.645. **L2− es el espejo.** Hacen falta ≥ 15 semillas con dato por brazo.

Simulado [`NUL` §G; D binomial negativa, var = λ·φ; 40 000 series por celda; (iii) no simulada: sólo puede bajar FP y potencia]:

| | φ = 1 | φ = 2 | φ = 4 |
|---|---|---|---|
| **FP máx. por serie** (λ de 0.5 a 6) | 0.0096 | 0.0091 | 0.0092 |
| potencia 1 → 3 | 0.97 (×2: 0.95) | 0.83 (0.69) | 0.62 (0.38) |
| potencia 2 → 4 | 0.86 (0.75) | 0.60 (0.35) | 0.38 (0.14) |
| potencia 4 → 8 | 0.99 (0.99) | 0.89 (0.79) | 0.63 (0.40) |
| potencia 4 → 6 | 0.62 (0.39) | 0.34 (0.12) | 0.19 (0.04) |
| potencia 1.5 → 6 | 1.00 | 1.00 | 0.97 (0.94) |

- **FP ≤ 0.0096 por serie; ≤ 9.2e-5 en serie Y réplica.**
- Base medida sin filtro de función, esc 90, T 500k: D5 media 3.84 y 5.00, mediana 4 y 4, varianza 7.9 y 18.1 → **φ ≈ 2–3.6** [V].
  Con esa dispersión la puerta sólo ve con potencia razonable un efecto de **el doble o más**; un +50 % (4 → 6) casi nunca pasa ×2.
- El filtro de función bajará λ (no medido). Con λ90 ≈ 1, hace falta λ900 ≈ 3.

### 7d. "Más N da más formas sólo por más muestreo": cómo se responde

- La cuenta de formas PRESENTES (≥ 1 portador) sí es muestreo: 15 / 29 / 36 a esc 300 / 900 / 1200 contra 3–8 a esc 90, T 200k
  [V, `NUL` §F]. **No se usa.**
- D5 es una frecuencia (≥ 5 %), no una cuenta de presentes; y la cláusula (iii) repite la lectura con 24 cuerpos por población.
- **Control que puede ganar, "diez pueblos chicos":** se juntan los vivos de 10 semillas de esc 90 (≈ 360 cuerpos; dos grupos por
  serie, semillas 1–10 y 11–20) y se calcula el mismo D5. Si los pueblos juntos igualan o superan la mediana de esc 900, la diversidad
  viene del número total de cuerpos y del aislamiento, no de una población grande. Entonces queda prohibida la frase "una población
  grande sostiene más que la suma de chicas". Descriptivo (n = 2 por serie); recorta el vocabulario, no el veredicto.
- Queda sin normalizar la oferta: esc 900 hace ×10 nacimientos por unidad de tiempo. Eso es la hipótesis, no un artefacto.

### 7e. Deriva, arrastre y BLOQ_AZA_V

- Juguete de Wright–Fisher [`NUL` §C]: N 35 → 0.50–0.68 formas neutras al 50 %; N 350 → 0. La deriva fija más en la población chica.
- **BLOQ_AZA_V se extingue a esc 90** (persiste 1/20 y 0/20) [V]; a esc grande no está probado. Cláusula de control: **P3** = BLOQ_AZA_V@900
  no pasa la misma puerta contra BLOQ_V@90 (ni L1+ ni L2+). Si AZA muere, P3 se cumple por extinción: **control débil, declarado**.
  Se lee además en la foto de t_corte, donde AZA vive (descriptivo, con la cautela de ERR-153).
- **P4 (arrastre):** los testigos silenciosos fijados (para L1) o sostenidos (para L2) no suben de 90 a 900 tanto o más que la medida
  funcional (medianas). Si suben igual, la lectura positiva baja a MODESTO.

### 7f. Tabla de desenlaces (cada celda exige lo mismo en serie Y réplica; si no coinciden, vale la menor)

Validez primero (§9, §10): si falla, NO EVALUABLE. P1 = BLOQ_V persiste ≥ 17/20 en los dos tamaños; si P1 falla a esc 900: **NO**, "el
linaje no se sostiene a esc 900 sin vivero".

| | **L2+** (900 sostiene más) | **L2 0** | **L2−** (90 sostiene más) |
|---|---|---|---|
| **L1+** (900 fija más) | FUNCIONA (H-FIJ y H-DIV): "con N ×10 se fijan y se sostienen más formas funcionales". Habilita F3 | FUNCIONA (H-FIJ): "N ×10 fija más; la diversidad en pie no cambia" | FUNCIONA (H-FIJ) con nota: "fija más y barre la diversidad" |
| **L1 0** | FUNCIONA (H-DIV): "N ×10 sostiene más diversidad funcional a profundidad igual, sin fijarla". Habilita F3 con T largo | **NO**: "con este motor y este reloj, N ×10 no cambia ni lo fijado ni lo sostenido" | NO, signo contrario en diversidad |
| **L1−** (90 fija más) | FUNCIONA (H-DIV) con la lectura de la sonda: "N grande retarda la fijación y sostiene más diversidad" | NO para las dos hipótesis; se declara "N grande retarda la fijación a profundidad igual" | NO fuerte: "N ×10 fija menos y sostiene menos"; revisar estructura espacial |

- FUNCIONA exige además P3 y P4 para la lectura que lo sostiene. Con P4 caída, o con la cláusula (iii) de L2 caída: **MODESTO**.
- MODESTO también si una lectura queda a medio camino: L1 con diferencia 4–6, o L2 con z en [1.645, 2.326) y mediana ≥ +1, ×2.
- **Multiplicidad declarada:** dos lecturas co-principales. FP de "algún FUNCIONA" por serie ≤ 0.019 + 0.0096 ≈ 0.029; en serie Y
  réplica ≤ 3.7e-4 + 9.2e-5 ≈ **4.6e-4**.

### 7g. Lectura secundaria DESCRIPTIVA: innovación de dos pasos (no es puerta)

Por brazo: número de semillas con algún genoma vivo que lleve dos formas funcionales distintas del rechazo, y para el más frecuente de
ellos la ablación triple (G+, sin una, sin la otra, sin las dos) en 5 semillas. "Dos pasos" sólo si quitar cada una baja K y quitar
las dos baja más. El repo no lo ha mostrado nunca (doble regla 0/45, `REGISTRO:7437`). No se elige como principal porque su tasa base
es ≈ 0 en los dos tamaños: con 20 semillas la potencia sería nula salvo efecto enorme, y un 0 contra 0 no informa.

### 7h. Predicciones firmadas del creador (antes de todo dato de F1)

| # | cantidad | predicción | p |
|---|---|---|---|
| F1 | BLOQ_V@900 persiste a T 500k | ≥ 17/20 | 0.80 |
| F2 | `linajes_T` a esc 900 (mediana) | en [1, 6] | 0.65 |
| F3 | L1+ ×2 (H-FIJ) | | **0.05** (la ficha: 0.45; v1: 0.12) |
| F4 | L1− en la serie (esc 90 fija más) | | 0.30 |
| F5 | L2+ ×2 (H-DIV) | | **0.15** |
| F6 | celda central (L1 0, L2 0) ×2 | | 0.40 |
| F7 | D5 funcional, mediana, esc 90 / esc 900 | [0, 2] / [0, 3] | 0.60 |
| F8 | paridad del reloj A en [0.67, 1.5] a T 500k | | 0.70 |
| F9 | BLOQ_AZA_V@900 persiste | ≤ 5/20 | 0.70 |
| F10 | "diez pueblos chicos" ≥ mediana de esc 900 en D5 | en la serie | 0.65 |

## 8. Regla de parada

- **Humo** (49841–49846, un proceso, T ≤ 200 000): cada brazo escribe su JSON con los campos de §5 y §9. Aborta el plan si falta un
  campo, `bloqueados > 0`, `desinc > 0` (`sonda_reactor.py:100`), filas faltantes en la genealogía, o si la identidad no pasa.
- **Identidad:** la sonda ya da esc 90 con ganchos == `corre_bloques.corre` en todas las claves
  (`REA\identidad_reactor_salida.txt:12-13`), pero el arnés cierra **15/16 FALLA** (`:27`) porque la corrida de prueba (49701) se
  extinguió y no es "no trivial" (`:14`). Hay que repetirlo con una semilla que persista antes de usarlo.
- **Práctica de relojes** (una semilla, T completo, los dos tamaños): si A < 30 en T (margen ×1.5), T sube a 750 000 en los dos
  tamaños y se escribe aquí antes de la serie.
- **Si esc 900 no sostiene población:** P1 falla → NO. No se toca t_corte, tope, n0 ni vivero para rescatarla.
- **Tiempo:** tope por corrida = 5 × el costo proyectado de §12 (BLOQ_V@900: 12.5 min). Pasarlo es aborto; con un aborto, NO EVALUABLE.
- **Prohibido mirar parciales para decidir seguir.** La serie se lanza entera (80) y la réplica se lanza SIEMPRE. El log muestra sólo
  `persiste`, `aborto` y segundos. El punto de lectura (§9c) y la lista de clases para la ablación se calculan una vez, con las 80
  cerradas, y se congelan en un archivo antes de lanzar ablaciones.
- `--reanuda`: ver §9d (la genealogía de los ganchos no viaja en el checkpoint).

## 9. Validez: los dos relojes

Nombres de `AUDITORIA_F0.md` (H-2) y de la fe de erratas de `F0_relojes.md`.

### 9a. Definiciones e instrumento (ya existe)

- **Reloj A = profundidad mutacional:** eventos de operador (campo, dup, del, ins, hgt) sumados a lo largo de la ascendencia GENÉTICA
  de un cuerpo; media de los vivos. Instrumento: `sonda_reactor.relojes()` (`REA\sonda_reactor.py:142-185`, campo `prof_eventos`), con
  los eventos de cada parto y cada refundado (`:91-101`, `:103-116`), la fuente del banco (`:106-111`) y las filas de genealogía
  (`:118-126`). Da también `prof_cambios` (pasos con ≥ 1 evento) y `prof_pasos` (pasos genealógicos).
- **Reloj B = reemplazos por cuerpo (reloj de selección):** nacidos (no refundados) en una ventana, divididos por la media de vivos de
  esa ventana (`sonda_reactor.py:180-184,241`). En F1 la ventana es (t_corte, T].
- Comprobado por el arnés de la sonda: ganchos == contadores del motor, banco sincronizado, genealogía sin filas faltantes
  (`identidad_reactor_salida.txt:19-23`).

### 9b. Lo medido y los umbrales

| | esc 300 | esc 900 | esc 1200 | fuente |
|---|---|---|---|---|
| A en t = 100k / 200k | 8.1 / 14.3 | 5.3 / 11.6 | 5.4 / 15.7 | [S] `REA\datos\sonda\R_*.json`, `relojes.prof` |
| A por 100k tras el corte | +6.2 | +6.3 | +10.3 | [S] |
| pasos genealógicos en 200k | 63 | 66 | 68 | [S]; ≈ +30 por 100k |
| fracción de pasos con mutación | 0.20 | 0.17 | 0.20 | [S] (`prof_cambios / prof_pasos`; el coordinador resume 0.2–0.33) |
| B, segunda mitad (100k) | 44.8 | 45.2 | 45.3 | [S] `sonda_salida.txt:1-3` |
| linajes 100k → 140k → 200k | 90 → 10 → 5 | 90 → 24 → 12 | 90 → 27 → 10 | [S] |
| vivos, segunda mitad | 120.6 | 359.0 | 479.5 | [S]; ≈ 0.40 × esc |

A no es monótono (esc 300: 16.0 a 150k, 14.3 a 200k): un barrido puede bajarlo.

**Umbrales (cada tamaño, BLOQ_V, mediana sobre las semillas que persisten, en T):**

| reloj | umbral | T necesario [P] | a T 500k [P] |
|---|---|---|---|
| A, profundidad mutacional media de los vivos | **≥ 20** | ≈ 290 000–340 000 | ≈ 30–47 |
| B, reemplazos por cuerpo en (t_corte, T] | **≥ 150** | ≈ 435 000 | ≈ 180 |
| pasos genealógicos | ≥ 100 (se reporta) | ≈ 320 000 | ≈ 155 |

- **Los dos umbrales siguen teniendo sentido y a T 500 000 serían alcanzables: PROYECCIÓN NO MEDIDA** (una semilla por escala, hasta
  200k, nada a esc 90 con la sonda). A ≥ 20 queda claramente sobre el ≈ 12 de o1_libre (`AUDITORIA_F0.md:10-11`), con margen ×1.5–2.3.
- **B es el que aprieta:** 45 por 100k × 4 = 180, margen ×1.2. No se baja el umbral (la cota de 122 nacimientos por línea no bastó en
  o1_libre, `F0_relojes.md:17`). Si la práctica da B < 165, T sube a 600 000 en los dos tamaños.
- **Corrección a v1:** el "≈ 255–270" de v1 dividía los nacidos de TODA la corrida por la K de la segunda mitad. No es B.
- Si un umbral falla en cualquier tamaño: NO EVALUABLE.
- Límite declarado: ≈ 155 pasos genealógicos están lejos de las ≥ 10³ generaciones del Reactor (`ENTREGA_1_reactor.md:24`).

### 9c. Comparación: mismo T, lectura A PROFUNDIDAD IGUAL

- **Los dos tamaños corren T = 500 000** (pasos iguales). B es igual en todas las escalas [S], así que pasos iguales ≈ reemplazos iguales.
- **La lectura se hace a reloj A igual.** Fotos de los vivos cada 50 000 pasos desde 150 000. Por brazo, Ā(t) = mediana sobre semillas
  del reloj A en la foto t. A* = el menor de Ā_90(T) y Ā_900(T). El brazo de menor Ā se lee en T; el otro, en la foto cuyo Ā esté más
  cerca de A* (empate: la más tardía). Es mecánico y usa sólo el reloj, no las formas.
- Si las tasas son iguales, como sugiere la sonda, los dos se leen en T.
- **Paridad:** tras igualar, Ā_900 / Ā_90 debe quedar en [0.8, 1.25]; si no, el veredicto no pasa de MODESTO. Se reporta también la
  lectura a pasos iguales (los dos en T), sin puerta.
- Por qué no "pasos iguales" como principal: con A no monótono y +6 a +10 por 100k según la escala, a pasos iguales una diferencia de
  formas puede ser sólo reloj.

### 9d. Lo que le falta a la sonda para ser el instrumento de F1

1. `T_MAX = 200000` (`sonda_reactor.py:37,190`): la serie necesita 500 000 y la bandera de serie sólo para el coordinador.
2. Las formas se cuentan con `tipo()` (`:52-64`); falta la letra canónica de §6, D5, `d_rar` y los testigos.
3. No guarda genomas intermedios: faltan las **fotos de vivos cada 50 000** (con reglas, linaje y clave de genealogía) para §9c.
4. `relojes()` da A en T/4, T/2, 3T/4 y T (`:170`): hay que darlo en la rejilla de 50 000 y por cuerpo, no sólo la media.
5. B se calcula en mitades (`:180`): falta la ventana (t_corte, T].
6. **`--reanuda`:** la telemetría vive en `TEL` (`:38,69-70`), fuera del checkpoint. Una corrida reanudada pierde la genealogía. O se
   mete en el blob, o se prohíbe reanudar en F1.
7. `clados_T` (ancestros de t_corte con descendencia viva) no se calcula.
8. El mundo se cambia mutando `NS.MUNDO` en el proceso (`:193-205`): con Pool hay que hacerlo dentro de cada trabajador y guardar
   `mundo` en el JSON (ya lo guarda, `:218`).
9. No probado: BLOQ_AZA_V a esc grande, T > 200k, más de una semilla, y los ganchos con donante `azar` (el arnés corrió sólo BLOQ_V).
10. `veredicto()` con la letra de §7f y el paso de ablación de F1 (el del Paso 0 lee las series viejas).

### 9e. Otras puertas de validez

V0 serie completa (20 × 4, mismas semillas, T y t_corte, sin abortos, `bloqueados == 0`, `desinc == 0`, genealogía sin faltantes) ·
V1 `esc`, `n0`, `tope` y configuración de reglas en cada JSON, conformes a §3 · V2 ancla: BLOQ_V@90 con `frac_rechazo` ≥ 0.5 en ≥ 15/20
(registrado 19 y 18) y BLOQ_AZA_V@90 persiste ≤ 5/20 (registrado 1 y 0).

## 10. Controles que pueden ganar, lecturas alternativas, vocabulario

- **Esc 90 iguala o gana** en cualquiera de las dos lecturas: celdas de la fila y columna centrales y de signo contrario de §7f.
- **Diez pueblos chicos** (§7d) · **BLOQ_AZA_V** (§7e, débil) · **testigos silenciosos** (P4).
- **ERR-153** (`REGISTRO:7137-7139`): con vivero permanente K no es monótono en la calidad. Toda K de puerta es de vivero finito y la
  ablación compara G+ y G− en el mismo mundo. "Funcional" = "sube K en ese mundo". La foto de t_corte sí está subsidiada.
- **Estructura espacial:** anillo de 36 000 celdas a esc 900, HGT del vecino más cercano. "No fijó" puede ser "no hubo tiempo de
  barrer"; por eso la lectura es a profundidad igual y se reportan `linajes_T` y `clados_T`.
- **Las cuatro trampas:** (1) canal simétrico: BLOQ_V y AZA difieren sólo en el donante; entre tamaños sólo `esc` (y el banco relativo).
  (2) Sin clasificación: conteos por semilla. (3) Mundo que se come la comida: composición y llegadas perdidas por tamaño. (4)
  Significado de letras fijo (`PREREGISTRO_bloques.md:82-83`): se miden INSTINTOS.

**Vocabulario.** Permitido: "forma fijada", "forma sostenida", "funcional por ablación en ese mundo", "a profundidad mutacional igual",
"instinto heredable". Prohibido: "aprende", "entiende", "especie", "innovación", "órgano nuevo", "evolución abierta", "el Reactor
funciona", "N era la condición que faltaba"; y "más formas" sin decir el umbral de frecuencia.

## 11. Mini-prueba y debilidades propias

`python f1_nulo.py > f1_nulo_salida.txt` (un proceso; rng 20261001–20261003). Resumen: L1 FP ≤ 0.019; L2 FP ≤ 0.0096; base de esc 90
sin filtro: otra forma fijada en 13/20 ×2, D5 mediana 4 ×2; sonda a 200k: D5 = 3 / 2 / 4 a esc 300 / 900 / 1200.

- La ablación por clase usa un solo genoma portador (no ve epistasis) y descarta las formas de una sola semilla.
- `W_SIL`, `MIN_VIVOS`, el 5 % de la ablación, los umbrales de reloj y la puerta de L2 se eligieron mirando datos VIEJOS de esc 90 y
  la sonda; ninguno con datos de F1.
- θ ignorado en sentidos continuos. Una regla de condición SIEMPRE cierta en un sentido continuo no se trata como silenciosa (el
  Paso 0 trae un control para eso, `paso0_ablacion.py:13`).
- El banco de 200 no escala: en BLOQ_AZA es todo el acervo y a esc 900 gira ×10 más rápido.
- La cláusula (iii) de L2 no entró en la simulación.

## 12. COSTOS

**Medido por la sonda [S]** (`REA\sonda_salida.txt:1-3`; BLOQ_V, T 200k, n0 90, un proceso, con ganchos):

| esc | vivos (2ª mitad) | s por 100k | µs por cuerpo·paso | s de motor en 200k |
|---|---|---|---|---|
| 300 | 120.6 | 12.11 | 0.973 | 24.2 |
| 900 | 359.0 | 26.40 | 0.885 | 52.8 |
| 1200 | 479.5 | 34.73 | 0.833 | 69.5 |

- Lineal en esc: ≈ 0.029–0.040 s por 100k por unidad de esc. El coordinador resume 0.78–0.82 µs y 0.033 s; el archivo dice
  0.83–0.97 µs. La diferencia no cambia el orden; **no la reconcilié**.
- Población ≈ 0.40 × esc. 500 vivos piden esc ≈ 1250. 2M pasos con 500 cuerpos ≈ 14 min por núcleo (coordinador).
- Otros números de hoy: linajes 90 → 10–12 a 200k (5 a esc 300); reloj A +6 a +10 por 100k; reloj B 45 por 100k.

**Por brazo, T 500 000, un núcleo:**

| brazo | s por corrida | × 20 | origen |
|---|---|---|---|
| BLOQ_V@900 | ≈ 150 | 50 min | [P]: 52.8 s hasta 200k + 3 × 31.8 s (0.885 µs × 359 × 100k) |
| BLOQ_V@90 | 63.5 | 21 min | [V] `PREREGISTRO_bloques.md:157` (PC compartido) |
| BLOQ_AZA_V@90 | ≈ 27 (21–48) | 9 min | [V] `:158-159`; se extingue hacia 110–160k |
| BLOQ_AZA_V@900 | 53 a 150 | 18–50 min | **NO MEDIDO**: 53 si se extingue como a esc 90; 150 si persiste |
| **serie (80 corridas)** | | **1.6–2.2 h de núcleo** | |

**Total de reloj:**
- El coordinador da **0.6–1.7 h** para serie + réplica a T 500k con pool 6 y **tres** brazos. El cuarto (BLOQ_AZA_V@90) añade ≈ 18 min
  de núcleo en las dos series, 3–9 min con pool 6: **≈ 0.65–1.85 h con cuatro brazos**. Escalado proporcional (×4/3), como cota:
  0.8–2.3 h.
- Cuenta propia desde la tabla: 3.3–4.3 h de núcleo / 6 × inflación 1–3 = **0.55–2.2 h**. Coincide en orden.
- A T 2M (no es F1): 2.3–7 h con tres brazos (coordinador); ×4/3 ≈ 3–9 h.
- **Ablaciones (§6d), no contadas arriba:** 10 corridas de T 200k por clase. A esc 90 ≈ 10–12 s cada una [V, `REA\paso0_salida.txt`];
  a esc 900 ≈ 53 s [S]. El número de clases no se conoce. Con 10 clases por tamaño y serie: ≈ 1.8 h de núcleo por serie, 0.3–0.9 h
  con pool 6. L2 prueba más clases que L1.

**No medido:** inflación del pool (×1–3, supuesta), BLOQ_AZA_V a esc 900, T > 200k a esc grande, el costo de las fotos cada 50 000 y de
la genealogía a T 500k (≈ 10⁵ filas por corrida a esc 900), más de una semilla.

## 13. Falta construir y no verificado

**Falta construir:** los 10 puntos de §9d · identidad repetida con semilla que persista · runner de serie con `--humo` y entrada campo a
campo contra `corre_bloques.py` (regla 14) · Paso 0 cerrado y c escrito en §7b · práctica de relojes a T 500k en los dos tamaños ·
auditor.

**No verificado:**
- Nada de F1 se corrió. Todo lo de esc ≥ 300 es una semilla por escala hasta 200k.
- Que A y B a esc 90 con el instrumento de la sonda sean los de las otras escalas (la única corrida de esc 90, 49701, se extinguió).
- Que BLOQ_V@900 persista hasta 500k y que BLOQ_AZA_V@900 se extinga.
- El rango de los sentidos continuos y el valor −1 inicial de la memoria de la última mordida (`motor_bloques.py:878`).
- Dónde nace el hijo en el anillo y cuánto tarda un barrido en recorrer 36 000 celdas.
- La diferencia entre los µs del coordinador y los del archivo de la sonda.
- No se releyeron `CLAUDE.md`, `PLAN.md` ni `EQUIPO.md` del bundle.
- El grep de semillas es por texto; no cubre semillas generadas por código.

---

## Anexo: resultado del Paso 0 (1-oct-2026; lo corrió el coordinador; es SONDA, no se declara)

Anotado tal como lo reportó la sesión "JUACO organelos serie y auditoría". Esta sesión NO lo verificó. Archivos: `organelos\experimentos\organelos\reactor\paso0_salida.txt` (sha e8ba05f222e2f259) y `paso0_ablacion.py` (sha 7caff37b6aaeec21).

**c recomendado = 2 contando el órgano de rechazo; base 2/40 (serie 0/20, réplica 2/20).**

| semillas con ≥ c formas funcionales fijadas (de 40) | c = 1 | c = 2 | c = 3 |
|---|---|---|---|
| Con órgano de rechazo | 38 | 2 | 0 |
| Sin órgano de rechazo | 2 | 0 | 0 |
| Sin filtro de función | 38 | 26 | 11 |

- Las dos "segundas funciones" (semillas 48433 y 48439) son el rechazo con otra ropa (píxel 2 > θ → boca −3). Excluyendo la función de rechazo en sentido amplio, la base es 0/40 para todo c. **A esc 90 no hay ninguna segunda función fijada.**
- **Aviso de letra:** `pixF[AC]->boca+` de la canonización de este borrador no equivale a `corre_bloques.rechazo()` (peso negativo sobre B y D exactos); junta "no muerdas veneno" con "muerde comida". El órgano debe definirse por FUNCIÓN (quitarlo extingue), no por forma.
- Órgano: efecto +96 %, G− extinto 5/5. Pasajeras: +0.4 a +2.4 %, todas positivas, una gana 5/5. El umbral del 5 % de la ablación decide y se eligió hoy: declararlo y añadir lectura de sensibilidad a 2 %.
- Testigos "nunca cierta": efecto 0.000 exacto. Testigos silenciosos fijados en 5/40 semillas.
- Semillas 55151–55155 ya gastadas en el Paso 0. (La v2 ya usa 49861–49865 para las ablaciones de F1; no reutilizar las 551xx.)
- Límites del Paso 0: un genoma portador por clase, T 200k sin mutación, 23 formas únicas no ablacionadas, sin arnés propio.

**Pendiente de resolver al congelar (PC nuevo), porque el cuerpo de la v2 y el Paso 0 no coinciden:**
1. La v2 EXCLUYE el órgano de rechazo de L1 y L2 y deja c ∈ {1, 2}; el coordinador recomienda c = 2 CONTANDO el órgano. Son equivalentes a "al menos una función además del rechazo", pero hay que fijar UNA letra. Con cualquiera de las dos, la base a esc 90 es ≈ 0–2/40: L1 pasa a preguntar si esc 900 fija alguna segunda función, y el "espejo" de L1 (esc 90 > esc 900) queda sin sitio.
2. Redefinir el órgano de rechazo por función (ablación que extingue) y rehacer la exclusión en la canonización.
3. Rehacer el nulo de L1 con base 0.05 (2/40) en lugar de 0.25: la puerta `k900 − k90 ≥ 7 y k900 ≥ 10` y su potencia cambian.
4. Umbral de ablación: 5 % declarado, con sensibilidad a 2 %.
