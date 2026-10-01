# PREREGISTRO (BORRADOR) — F1 del Reactor: barrido de tamaño en BLOQUES, esc 90 frente a esc 900 (1-oct-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo.

**Estado: BORRADOR. No hay runner, ni instrumento, ni arnés, ni humo.** Escrito ANTES de cualquier corrida de F1. Lo único que se corrió
es `f1_nulo.py` (numpy, un proceso, segundos; sha `4cfb76d7e77a99e9`) → `f1_nulo_salida.txt` (sha `fdb54780f7a7a489`), que además LEE los
160 JSON ya registrados de BLOQUES (sección D de la salida). Ningún número de esc 900 existe todavía.

Rutas: `ORG` = `C:\Users\User\Documents\PROYECTOS\JUACO\organelos\`; `OPM` = `ORG\experimentos\organelos\bloques\opusM\`.
Marcas: [V] leído en el repo o medido de JSON guardados · [I] inferencia · [P] propuesta sin construir.

## 0. Tres cosas que este borrador cambia de la ficha, y por qué

1. **La cláusula "≤ 5/20 a esc 90" ya está contradicha por datos guardados.** Con la letra de §6 (sin la prueba de función, que exige
   motor), en las dos series registradas de BLOQ_V a esc 90 hay ≥ 2 formas fijadas en **13/20 y 13/20** semillas, y ≥ 3 en 3/20 y 8/20
   [V, `f1_nulo_salida.txt` §D]. La puerta de la ficha nacería fallada por el lado de esc 90. Se cambia por una puerta de DIFERENCIA (§7).
2. **A esc 90 hay UN linaje vivo en T en las 38 semillas que persisten** (mediana 1, rango 1–1) [V, §D]. "Fijada en ≥ 50 % de los vivos"
   es ahí casi lo mismo que "la lleva el ancestro común": cuenta arrastre. Por eso la prueba de función (ablación) y los testigos
   silenciosos dejan de ser adorno y pasan a decidir (§6, §7c).
3. **BLOQ_AZA_V se extingue** (persiste 1/20 y 0/20; 0 semillas con ≥ 12 vivos en T) [V]. Como control de deriva EN T no puede ganar:
   cuenta 0 por estar muerto, no por no fijar. Se conserva (lo pide la ficha) pero la deriva se estima por otras dos vías (§7c).

## 1. Hipótesis

**H-N:** con el mismo motor, las mismas tasas y el mismo mundo por cuerpo, una población ×10 (esc 900 frente a esc 90) fija más formas
de regla funcionales distintas por semilla.

Lectura contraria con base propia (control que puede ganar): más N NO da más formas fijadas, o da MENOS, porque a esc 90 la fijación es
clonal (un linaje) y a esc 900 conviven muchos linajes que no alcanzan el 50 % en ~115 generaciones.

## 2. Mecanismo mínimo y memoria nueva

- Motor de BLOQUES sin cambios de conducta. **Memoria nueva de conducta: cero.**
- Telemetría nueva (no la lee ningún cuerpo; §9): un entero por cuerpo y por entrada del banco (profundidad mutacional), un contador
  de nacimientos tras el corte, la foto de vivos en t_corte y la tabla de partos encadenados.
- Lo único que cambia entre brazos de tamaño: `esc` (90 → 900), fundadores (90 → 900) y `tope` (3000 → 30 000), todos ×10.

## 3. Brazos

| brazo | esc | fundadores | tope | reglas | donante | papel |
|---|---|---|---|---|---|---|
| BLOQ_V@90 | 90 | 90 | 3 000 | sí | padre | base (réplica interna de BLOQUES) |
| BLOQ_V@900 | 900 | 900 | 30 000 | sí | padre | hipótesis |
| BLOQ_AZA_V@90 | 90 | 90 | 3 000 | sí | azar | control sin herencia |
| BLOQ_AZA_V@900 | 900 | 900 | 30 000 | sí | azar | control sin herencia |

80 corridas por serie (la ficha decía 60: contaba un solo AZA). Más las ablaciones de §6d, que son corridas cortas del runner.

**Idéntico a BLOQUES (cita):**
- Tasas: `p_campo 0.10, p_dup 0.02, p_ins 0.02, p_hgt 0.01, p_del 0.05, banco 200`, arranque vacío — `OPM\corre_bloques.py:38`;
  `OPM\PREREGISTRO_bloques.md:25-28,32`.
- Operadores y su orden (campo → dup → del → ins → hgt → tope NRMAX) — `OPM\motor_bloques.py:810-833`; `NRMAX = 12` — `:115`.
- Regla = [sentido, parámetro, comparador, θ, acción, peso]; sorteo de regla nueva — `motor_bloques.py:805-807`.
- Herencia y banco: donante `padre` / `azar` — `motor_bloques.py:836-863`; brazos `_V` con t_corte 100 000 —
  `corre_bloques.py:43-46`.
- Carro FABRICA_ECO, quimiostato, w90 — `ORG\experimentos\juaco_eco\corre_eco.py:31` (`MUNDO = dict(esc=90, n0=90, ..., tope=3000,
  muestra=1000)`); el mundo entra por `mundo_n=MUNDO['esc']` — `ORG\experimentos\organelos\eco_sel_ing\nucleo_eco_sel_ing.py:168`.
- **T = 500 000, t_corte = 100 000** — `corre_bloques.py:201-202`; `PREREGISTRO_bloques.md:154,157`.
- K = media de `tam_total` en [T/2, T] — `corre_bloques.py:111-117`. `persiste` — `nucleo_eco_sel_ing.py:194`.
- Genoma de los vivos en T: `BQ_OUT['vivos_T'] = [linaje, gen, fund, reglas]` — `motor_bloques.py:898-902`.
- Cómo midió BLOQUES el órgano: `rechazo()` y `frac_rechazo()` — `corre_bloques.py:131-142`; P4 ≥ 0.5 en ≥ 12/20 — `:234-236`.
  Se recalcula igual en F1 como ancla con lo registrado (19/20 y 18/20, `ORG\registro\REGISTRO_etapas_1_2.md:7122`).

**Distinto (declarado):** `esc`, `n0`, `tope` ×10 en los brazos @900. El mundo escala solo: L = 40·esc, 4·esc objetos
(`ORG\experimentos\juaco_eco\motor_eco.py:12`; máximo esc 2000, `:77`). **El banco se queda en 200 en los dos tamaños**: en BLOQ_V sólo lo
usan los refundados antes del corte; en BLOQ_AZA es todo el acervo y a esc 900 gira ×10 más rápido (asimetría declarada, §11).

## 4. Semillas (NUEVAS)

Grep del 1-oct en `organelos`, `o1libre` y `bundle` (experimentos y registro, `.md` y `.py`): **ningún 551xx–554xx aparece**. Los rangos
con prefijo usado son 410, 419, 420, 429–432, 453, 461, 470, 478, 484, 486–491, 498, 499, 501, 526, 530, 531, 537, 564, 566, 583, 584, 592.

- **Serie 55101–55120 · réplica 55121–55140.**
- Ablación (§6d): 55151–55155, las mismas para todas las ablaciones.
- Práctica y humo (costo, relojes, validez; se miran y se declaran): 55191–55196. Nunca entran a la serie.
- Las mismas 20 semillas en los 4 brazos. Entre tamaños NO es un diseño pareado (el mundo de esc 900 no es el de esc 90): la puerta
  compara conteos, no diferencias por semilla.

## 5. Medidas (por semilla y brazo; todas al JSON)

`persiste`, K, K_nac, vivos en T, linajes vivos en T, largo medio, `frac_rechazo` (letra de BLOQUES), `formas_fijadas` y
`formas_silenciosas_fijadas` (§6), `n_func` (§6d), los dos relojes (§9), composición del mundo y llegadas perdidas (`corre_bloques.py:79-83`).

## 6. Definición operativa de "forma de regla fijada", letra por código

El código de referencia es el de `f1_nulo.py` §D (ya corre sobre los JSON de BLOQUES). El runner lo copia campo a campo.

```python
PATM = {'A': (1,1,0,1,0,0), 'B': (1,0,1,0,1,0), 'C': (0,1,1,0,0,1), 'D': (0,0,1,0,1,1)}   # corre_bloques.py:128
SENT = ['hambre','sed','cerca','pixF','pixM','Rult']; ACC = ['boca','hacia','quieto','parir']
W_SIL = 0.25; FRAC_FIJ = 0.5; MIN_VIVOS = 12

def condicion(r):                      # r = [sentido, parametro, comparador, theta, accion, peso]
    s, p, c, th = int(r[0]), int(r[1]), (r[2] > 0.5), float(r[3])
    if s in (3, 4):                    # pixel j: tabla de verdad sobre las letras A, B, C, D
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

def formas_fijadas(vivos):             # vivos = BQ_OUT['vivos_T']
    if len(vivos) < MIN_VIVOS: return {}
    cnt = {}
    for x in vivos:
        for f in formas_cuerpo(x[3]): cnt[f] = cnt.get(f, 0) + 1
    return {f: c / len(vivos) for f, c in cnt.items() if c / len(vivos) >= FRAC_FIJ}
```

**a. Qué campos cuentan.** Forma = (sentido, condición canónica, acción, signo del peso total).
- Píxeles (sentidos 3 y 4): la condición es su tabla de verdad sobre A, B, C, D. El índice del píxel, el comparador y θ NO cuentan por
  separado: "píxel 4 > θ" y "píxel 1 < θ" son la MISMA forma (las dos cumplen en B y D). Con los 6 píxeles de `PATM` sólo existen tres
  particiones: {A,C | B,D}, {A,B | C,D}, {A | B,C,D} [V, enumerado].
- Sentidos continuos (hambre, sed, cercanía, R de la última mordida): cuenta el sentido y el sentido de la desigualdad; **θ no cuenta**
  (la mutación de θ tiene σ 0.15, `motor_bloques.py:820`; partir θ en bandas rompería un mismo cúmulo en dos formas que no llegan al 50 %).
- **Complemento = misma forma.** "Boca − si B/D" y "boca + si A/C" discriminan igual: se canonizan a la máscara que contiene A, con el
  signo cambiado. Por eso el órgano de rechazo de BLOQUES aparece como `pixF[AC]->boca+` (19/20 y 19/20) [V]. Igual `x < θ, w` ≡ `x > θ, −w`.
- Espacio total: 2 × 3 × 4 × 2 = 48 formas de píxel + 4 × 4 × 2 = 32 continuas = **80 formas canónicas**.

**b. Tolerancia en pesos, duplicados y silenciosas.**
- Duplicados: las copias de una misma (condición, acción) en un cuerpo se SUMAN; cuentan como una forma (en BLOQUES la copia es volumen,
  `REGISTRO:7131`).
- Tolerancia: la forma está en un cuerpo sólo si |peso total| ≥ `W_SIL` = 0.25 (medio σ de la mutación del peso, 0.5,
  `motor_bloques.py:822`). Sólo cuenta el signo, no la magnitud.
- Silenciosa: condición constante (nunca o siempre cierta), o |peso total| < 0.25. No entra en `formas_fijadas`.
- **Testigos silenciosos** (para la deriva, §7c): las reglas de condición constante se cuentan aparte con la clave cruda
  (sentido, parámetro, comparador, acción); "fijada" con la misma regla del 50 %. Campo `formas_silenciosas_fijadas`. [P]

**c. "Fijada".** Presente (no silenciosa) en ≥ 50 % de los vivos en T, con **≥ 12 vivos**. Con menos de 12 vivos la semilla cuenta 0
formas y se reporta aparte (no se excluye: excluirla sería mirar). A esc 90 los vivos en T son 36.5 y 32.5 de mediana [V].

**d. "Funcional" — PASO DEL RUNNER, exige motor.** Ablación por trasplante, con el mecanismo que ya existe (`forzada`, tasas 0:
`corre_bloques.py:53-60`, brazos FORZ*_V):
1. Clases a probar: toda forma fijada en **≥ 2 semillas** de BLOQ_V del mismo tamaño y la misma serie. Las fijadas en una sola semilla
   cuentan como NO funcionales, en los dos tamaños por igual (sesgo declarado, §11).
2. Genoma portador G+: en la semilla donde la forma tiene mayor fracción (empate: la semilla menor), la lista exacta de reglas más
   frecuente entre los vivos que la llevan (empate: el de mayor `gen`, luego el primero). G−: G+ sin TODAS las reglas de esa
   (condición, acción).
3. Se corren G+ y G− como `forzada` en los fundadores, tasas 0, t_corte 100 000, **T = 200 000, al mismo esc de origen**, semillas
   55151–55155. K en [100 000, 200 000].
4. **Funcional** si K(G+) > K(G−) en **5/5** semillas **y** la mediana de la diferencia ≥ 5 % de la mediana de K(G+). Nulo de signo: 5/5
   bajo p = 0.5 → 0.031 por clase.
5. `n_func(semilla)` = número de formas fijadas en esa semilla cuya clase es funcional a ese tamaño.

**e. "Distintas".** Dos formas son distintas si su tupla canónica difiere en cualquier campo después de (a) y (b). Dos copias, dos píxeles
con la misma tabla de verdad, dos θ o una regla y su complemento NO son distintas.

## 7. Nulo simulado y puerta

Estadístico por semilla: **X = 1 si n_func ≥ c** (c = 2, salvo §7b). Por brazo: k = suma de X en 20 semillas. `k90`, `k900` de BLOQ_V;
`a90`, `a900` de BLOQ_AZA_V.

### 7a. La puerta de la ficha (G0: k900 ≥ 12 y k90 ≤ 5) frente a una de diferencia (G1: k900 − k90 ≥ d y k900 ≥ m)

Exacto (binomial), H0 = misma p por semilla en los dos tamaños, p de 0.05 a 0.60 (y el máximo sobre 0.01–0.99, que coincide):

| puerta | FP máx. serie sola | FP serie Y réplica | potencia 0.10→0.70 | 0.25→0.75 | 0.25→0.60 | 0.40→0.80 | 0.60→0.95 |
|---|---|---|---|---|---|---|---|
| G0 (ficha) | 0.0075 | 5.6e-5 | 0.88 (×2: 0.77) | 0.59 (0.35) | 0.37 (0.14) | 0.12 (0.02) | 0.00 |
| G1 d = 6, m = 10 | 0.040 | 1.6e-3 | 0.98 (0.96) | 0.94 (0.89) | 0.68 (0.46) | 0.81 (0.66) | 0.73 (0.54) |
| **G1 d = 7, m = 10** | **0.019** | **3.7e-4** | **0.97 (0.95)** | **0.90 (0.80)** | 0.57 (0.32) | 0.71 (0.50) | 0.58 (0.34) |
| G1 d = 8, m = 10 | 0.0083 | 6.9e-5 | 0.96 (0.92) | 0.82 (0.67) | 0.44 (0.19) | 0.58 (0.33) | 0.42 (0.17) |

- **G0 no falla por falso positivo (0.0075): falla por potencia y por el ancla en esc 90.** Si la base es 0.40, su potencia es 0.12 aunque
  esc 900 llegue a 0.80; con la base medida sin filtro (13/20) es ≈ 0.
- **Puerta propuesta: G1 con d = 7 y m = 10.** Falso positivo 0.019 por serie (≤ 0.0192 para toda p), 3.7e-4 en serie Y réplica.
- **Sobredispersión (el nulo que la binomial no ve):** si la p de cada serie varía por lote (Beta con concentración 20), el FP de
  G1(7,10) en una serie sube a 0.015–0.068, y con concentración 8 a 0.04–0.12 (`f1_nulo_salida.txt` §B2). Por eso **una serie sola no
  declara nada**; y el "cuadrado" sólo vale si serie y réplica no comparten el sesgo (semillas nuevas, lanzadas aparte).
- Potencia débil declarada: si el efecto es 0.25 → 0.60, la puerta lo ve en serie Y réplica sólo el 32 % de las veces.

### 7b. Calibración del umbral c (PASO 0, con datos VIEJOS; decide antes de la serie)

La base sin filtro de función es 13/20 ×2 con c = 2 y 3/20, 8/20 con c = 3. Con base ≥ 0.6 no hay sitio para una diferencia de 7.
Regla fija: se aplica §6d a las 40 semillas registradas de BLOQ_V (48411–48450, esc 90) y se toma **el menor c en {2, 3} cuya base
funcional agrupada sea ≤ 12/40**. Si ninguno cumple, c = 3 y se declara "potencia baja" en el veredicto. c se fija y se escribe aquí
ANTES de lanzar F1. Las 40 semillas viejas no entran a la puerta.

### 7c. Nulo de deriva y arrastre: cómo entra en la puerta

- **Qué dice el modelo de juguete** (Wright–Fisher, formas neutras, `f1_nulo_salida.txt` §C; NO es el motor): con N = 35 llegan a
  ≥ 50 % 0.50–0.68 formas neutras por corrida y P(≥ 2) = 0.11–0.17; con N = 350, **0.00 y 0.00** en 100 y 300 generaciones. La deriva
  sola empuja en CONTRA de la hipótesis: fija más formas en la población chica.
- **BLOQ_AZA_V** entra tal como lo pide la ficha: cláusula `k900 − a900 ≥ d`. Con a900 ≈ 0 (extinción esperada) la cláusula es casi
  gratis; el nulo la confirma (FP de la puerta compuesta 0.0033 si no hay efecto de N ni de herencia; 0.019 si más N da más formas
  también sin herencia; 0.019 si la herencia fija pero N no importa). **Se declara control débil en T.**
- **Deriva sin herencia, medida donde AZA aún vive:** foto de vivos en t = t_corte (telemetría nueva `vivos_tc`), mismas funciones de
  §6 en los 4 brazos. Descriptivo; no entra en la puerta.
- **Arrastre dentro del brazo de la hipótesis:** `formas_silenciosas_fijadas` por semilla en BLOQ_V@90 y @900. Regla: si el aumento de
  formas funcionales de 90 a 900 viene con un aumento igual o mayor de testigos silenciosos fijados (medianas), el veredicto baja a
  MODESTO con la lectura "arrastre". La ablación (§6d) es el filtro principal.

### 7d. Puerta final, por serie

- **P1** BLOQ_V@900 persiste ≥ 17/20 y BLOQ_V@90 persiste ≥ 17/20 (base registrada 19/20 ×2).
- **P2** `k900 − k90 ≥ 7` **y** `k900 ≥ 10`.
- **P3** (control) `k900 − a900 ≥ 7`.
- **P4** (arrastre) la mediana de testigos silenciosos fijados no sube de 90 a 900 tanto o más que la de `n_func`.
- **Veredicto:** FUNCIONA = P1 + P2 + P3 + P4 · MODESTO = P1 y `k900 − k90 ≥ 4` sin llegar a FUNCIONA, o P2 + P3 con P4 caída ·
  NO en otro caso · NO EVALUABLE si falla la validez (§9, §10). **El bloque se declara sólo si serie y réplica coinciden; si no, vale
  el menor.**

### 7e. Predicciones firmadas del creador (antes de todo dato de esc 900)

| # | cantidad | predicción | p |
|---|---|---|---|
| F1 | BLOQ_V@900 persiste | ≥ 17/20 | 0.75 |
| F2 | linajes vivos en T a esc 900 (mediana) | en [5, 60] (a esc 90: 1) | 0.70 |
| F3 | formas fijadas sin filtro a esc 900, mediana por semilla | ≤ la de esc 90 (2) | 0.60 |
| F4 | P2 en una serie | se cumple | 0.20 |
| F5 | **FUNCIONA ×2** | | **0.12** (la ficha decía 0.45) |
| F6 | `frac_rechazo` ≥ 0.5 a esc 900 | ≥ 15/20 | 0.70 |
| F7 | BLOQ_AZA_V@900 persiste | ≤ 5/20 | 0.75 |

## 8. Regla de parada

- **Humo (antes de la serie, semillas 55191–55196, un proceso, T ≤ 200 000):** cada brazo escribe su JSON con todos los campos de §5 y
  §9. Aborta el plan si falta un campo, si `bloqueados > 0`, o si el arnés de identidad no da IGUAL (esc 90 con la telemetría nueva
  == `motor_bloques` actual, bit a bit, en todas las claves viejas).
- **Práctica de relojes (una semilla, T completo, los dos tamaños):** si la profundidad mutacional medida queda por debajo de 30
  (margen ×1.5 sobre el umbral de §9), T sube a 750 000 o 1 000 000 **en los dos tamaños** y se escribe aquí antes de la serie.
- **Si esc 900 no sostiene población:** F1 falla P1 → la serie es **NO**, con la frase "a esc 900 el linaje no se sostiene sin vivero".
  No se cambia t_corte, ni tope, ni el vivero para rescatarla. Cambiar eso es otro preregistro.
- **Tiempo:** el tope por corrida y por serie se fija cuando exista la tabla de §12. Una corrida que lo pase se anota como aborto; con
  cualquier aborto la serie es NO EVALUABLE (V0).
- **Prohibido mirar parciales para decidir seguir.** La serie se lanza entera (80 corridas) y la réplica se lanza SIEMPRE, salga lo
  que salga la serie. El log de avance puede mostrar `persiste`, `aborto` y segundos; NO `n_func`, formas ni k. El veredicto se calcula
  una vez, con las 80. Las ablaciones de §6d se lanzan después de cerradas las 80, con la lista de clases congelada en un archivo.
- Si se corta la luz: `--reanuda` (el banco y la telemetría viajan en el checkpoint, `PREREGISTRO_bloques.md:185`; hay que comprobar
  que los campos nuevos también viajan).

## 9. Puertas de validez con los dos relojes

Nombres de `AUDITORIA_F0.md` (H-2) y de la fe de erratas de `F0_relojes.md`.

**(a) Reloj mutacional = profundidad mutacional:** eventos de mutación a lo largo de la ascendencia de un genoma.
- Cómo se mide en BLOQUES [P]: un entero `prof` por cuerpo. Al nacer: `prof(hijo) = prof(base) + eventos`, donde `eventos` es lo que
  suman `n_campo + n_dup + n_del + n_ins + n_hgt` DENTRO de esa llamada a `_muta_reglas` (`motor_bloques.py:810-833`) y `base` es el
  padre (donante padre) o la entrada del banco (donante azar y refundados). Cada entrada del banco guarda su `prof`. Fundadores: 0.
- No consume rng ni cambia el orden de sorteos: el arnés debe dar identidad bit a bit.
- Se guarda por cuerpo vivo en T (quinto campo de `vivos_T`) y resumido: `prof_mut = {mediana, media, max}`.
- El estimador por varianza de un gen neutro (el de F0) NO aplica: BLOQUES no tiene un gen continuo sin leer. El contador es exacto.
- Junto a él se guarda la **profundidad generacional** (`I_GEN`, ya existe: `motor_bloques.py:1331`, segundo campo de `vivos_T`).

**(b) Reemplazos por cuerpo = reloj de selección:** nacimientos que sustituyen a un cuerpo, por cuerpo vivo.
- `reemplazos_por_cuerpo = (nacidos con fund == 0 y t_nac en (t_corte, T]) / (media de cuerpos vivos en (t_corte, T])`.
- Tras el corte no hay refundados: todo cuerpo nuevo es hijo de un vivo, y con población estable cada nacimiento reemplaza una muerte.
- F0 dejó esto SIN MEDIR en o1_libre ("el reloj de selección entre linajes NO está medido", `AUDITORIA_F0.md:24`).

**Lo medido hoy en BLOQUES esc 90, T 500 000** [V, `f1_nulo_salida.txt` §D; son proxies, no los relojes]:
- `I_GEN` mediana de los vivos en T: **115 [100–144]** y **116.5 [103–143]**.
- Eventos de operador por cuerpo nuevo (toda la corrida, incluye refundados): 0.23 y 0.26. Proxy de profundidad mutacional =
  U × generación ≈ **27 y 30** [I].
- `n_nac / K` ≈ **255 [218–316]** y **270 [214–477]** (ventanas distintas: nacidos de toda la corrida, K de la segunda mitad).

**Umbrales para que la corrida cuente (en CADA tamaño, brazo BLOQ_V, mediana sobre las semillas que persisten):**

| reloj | umbral | por qué |
|---|---|---|
| profundidad mutacional (mediana de los vivos en T) | **≥ 20** | ≈ 12 en o1_libre fue insuficiente (11.6 y 11.9, `AUDITORIA_F0.md:10-11`); BLOQUES fijó su órgano con ≈ 27–30 por proxy. 20 queda claramente por encima de 12 y por debajo de lo que BLOQUES ya da |
| reemplazos por cuerpo | **≥ 150** | la cota por nacimientos de o1_libre era 122 por línea (`F0_relojes.md:17`) y no bastó; BLOQUES da ≈ 255–270 por proxy |
| profundidad generacional (`I_GEN`) | ≥ 80 (se reporta; no invalida sola) | BLOQUES da 100–144 |

- **Paridad entre tamaños:** el cociente esc 900 / esc 90 de cada reloj debe quedar en [0.67, 1.5]. Fuera de ahí la comparación mezcla
  tamaño con reloj: el veredicto no pasa de MODESTO y se dice cuál reloj difiere.
- Si un umbral falla en cualquiera de los dos tamaños: **NO EVALUABLE**.
- **Límite declarado:** ~115 generaciones están muy lejos de las ≥ 10³ que pide la ficha del Reactor (`ENTREGA_1_reactor.md:24`). F1
  mide el efecto de N con el reloj de BLOQUES, no con el reloj del Reactor.

**Otras puertas de validez:** V0 serie completa (20 × 4, mismas semillas, mismo T y t_corte, ningún aborto, `bloqueados == 0`,
`n_tope` reportado) · V1 `esc`, `n0`, `tope` y la configuración de reglas guardados en cada JSON y conformes a §3 · V2 ancla con lo
registrado: BLOQ_V@90 con `frac_rechazo` ≥ 0.5 en ≥ 15/20 (registrado 19 y 18) y BLOQ_AZA_V@90 persiste ≤ 5/20 (registrado 1 y 0); si
falla, el instrumento no reproduce BLOQUES.

**Telemetría nueva que hace falta** (F0 mostró que la genealogía encadenada NO ESTÁ en los crudos: `F0_relojes.md:53`,
`AUDITORIA_F0.md:58`):
1. `prof` por cuerpo y por entrada del banco; quinto campo de `vivos_T`.
2. `nac_post_corte` y media de vivos en (t_corte, T] → `reemplazos_por_cuerpo`.
3. `vivos_tc`: la foto de `vivos_T` tomada en t = t_corte.
4. **Tabla de partos encadenados**: por nacimiento (t, id hijo, id padre, linaje, gen, eventos, fund). Permite recalcular los dos
   relojes y contar linajes por coalescencia. A esc 900 son del orden de 10⁵ filas por corrida [I]: archivo aparte (`.npz`), con su
   sha en el JSON.
5. `linajes_vivos_T` y la serie de linajes vivos cada `muestra`.

## 10. Controles que pueden ganar, lecturas alternativas, trampas

- **Control 1, esc 90 iguala o gana** (N no es el límite). Es el desenlace que el creador cree más probable (F3, F5).
- **Control 2, BLOQ_AZA** (sin herencia). Débil en T por extinción (§0.3); se lee además en `vivos_tc`.
- **Control 3, testigos silenciosos** (arrastre): pueden bajar un FUNCIONA a MODESTO (P4).
- **ERR-153** (`REGISTRO:7137-7139`): con vivero permanente K no es monótono en la calidad. Aquí toda K es de vivero finito y la
  ablación compara G+ contra G− en el MISMO mundo. Aun así, el anillo se llena de veneno en los brazos que persisten
  (`PREREGISTRO_bloques.md:183`): "funcional" significa "sube K en ese mundo", no "mejor organismo". Antes del corte (t < 100 000) K
  sigue subsidiada: `vivos_tc` se lee con esa cautela.
- **"Más N sólo da más formas por más muestreo."** La fracción ≥ 50 % no crece con el tamaño de la muestra, así que el estadístico
  principal no se infla por contar más cuerpos. Sí se inflaría una medida de RIQUEZA (formas presentes): por eso la riqueza se reporta
  sólo rarificada (submuestras de 35 vivos, 200 remuestreos con rng fijo, formas funcionales con frecuencia ≥ 10 %) y **no da veredicto**.
  Queda sin normalizar el suministro: esc 900 hace ×10 nacimientos y ×10 inserciones por unidad de tiempo. Eso ES la hipótesis (más
  oferta de variantes con selección más eficaz), no un artefacto; se declara.
- **Estructura espacial:** el anillo de esc 900 mide 36 000 celdas y la HGT es del vecino más cercano. Un barrido puede no recorrerlo
  en 500 000 pasos. Si hay muchos linajes y pocas formas al 50 %, la lectura es "no hubo tiempo de fijar", no "N no ayuda": por eso
  la paridad de relojes y `linajes_vivos_T` van al JSON.
- **Las cuatro trampas:** (1) canal simétrico: BLOQ_V y BLOQ_AZA_V difieren sólo en el donante; entre tamaños difieren `esc`, `n0`,
  `tope` y, de hecho, el banco relativo (200 fijo). (2) Acierto sin balancear: no hay clasificación; conteos por semilla. (3) Mundo que
  se come la comida: llegadas perdidas y composición del anillo al JSON, por tamaño. (4) Sitios fijos: el significado de las letras es
  fijo (`PREREGISTRO_bloques.md:82-83`): se miden INSTINTOS, no aprendizaje.

**Vocabulario.**
- Permitido: "con población ×10, la selección fija más formas de regla funcionales distintas por semilla (instintos heredables)";
  "forma fijada"; "funcional por ablación en ese mundo".
- Prohibido: "aprende", "entiende", "especie", "innovación", "órgano nuevo" (salvo que la ablación y una lectura a mano lo sostengan),
  "evolución abierta", "el Reactor funciona", "N es la condición que faltaba".

**Qué se declara en cada desenlace.**
- **FUNCIONA ×2:** "a esc 900 se fijan más formas funcionales distintas que a esc 90, con herencia y no sin ella". Habilita F3. No dice
  nada de innovaciones de dos pasos.
- **MODESTO:** "hay diferencia a favor de esc 900 pero no pasa la puerta, o no se separa del arrastre o del reloj". No habilita gasto
  mayor sin réplica nueva.
- **NO:** "con este motor y este reloj, ×10 de población no fija más formas; N no era el límite en BLOQUES". Si k900 < k90 por ≥ 7, se
  declara el signo contrario. La lectura de `ENTREGA_1` ("el NO de o1_libre es de tamaño") pierde apoyo, pero no cae: o1_libre es otro
  montaje.
- **NO EVALUABLE:** relojes bajo el umbral, ancla V2 rota o abortos. No se interpreta.

## 11. Mini-prueba de un proceso, con números (lo único corrido)

`python f1_nulo.py > f1_nulo_salida.txt` (un proceso, segundos; rng 20261001):
- G0: FP ≤ 0.0075; potencia 0.59 / 0.37 / 0.12 en 0.25→0.75 / 0.25→0.60 / 0.40→0.80.
- G1(7,10): FP ≤ 0.0192 (×2: 3.7e-4); potencia 0.90 / 0.57 / 0.71; con deriva q900 = 0.25, 0.83 / 0.42 / 0.69.
- Deriva de juguete: N 35 → 0.50–0.68 formas neutras al 50 %; N 350 → 0.
- Base medida en BLOQUES esc 90: formas fijadas por semilla, mediana 2 y 2; ≥ 2 en 13/20 y 13/20; un linaje vivo; `pixF[AC]->boca+`
  en 19/20 y 19/20; segunda forma más común `pixF[AC]->hacia+` (5 y 7 semillas).

**Asimetrías y debilidades propias, declaradas:**
- La ablación por clase usa un solo genoma portador: no ve epistasis con otros fondos.
- Las formas de una sola semilla cuentan como no funcionales. Castiga justo lo que más N podría dar (inventos distintos por semilla).
- `W_SIL`, `MIN_VIVOS`, el 5 % de la ablación y los umbrales de los relojes se eligieron hoy mirando los datos VIEJOS de esc 90.
- θ ignorado en sentidos continuos: dos instintos opuestos en θ sobre el mismo sentido se cuentan como uno.

## 12. COSTOS

**PENDIENTE: tabla de escalado del gemelo a esc 900–1200 (la mide otro agente en `organelos\experimentos\organelos\reactor\`).**

(En blanco a propósito. No se estima aquí.)

## 13. Lo que falta construir y lo que no se pudo verificar

**Falta construir (todo):**
1. Carpeta propia y `construye_*.py` por anclas desde `motor_bloques.py` (sha fijado) con la telemetría de §9.
2. Arnés de identidad: telemetría nueva == motor actual bit a bit a esc 90; determinismo; reanuda == entera con los campos nuevos.
3. Runner con `--humo` que escriba JSON, los 4 brazos con `esc`, `n0`, `tope` por brazo (hoy `MUNDO` es global:
   `nucleo_eco_sel_ing.py:168`), `veredicto()` con la letra de §7d, y el paso de ablación de §6d.
4. Entrada campo a campo contra `corre_bloques.py` (regla 14).
5. Paso 0 de §7b (ablación sobre las 40 semillas viejas) para fijar c.
6. Semillas, T y c finales escritos en este documento antes de la serie; auditor.

**No verificado:**
- Que el motor corra a esc 900 con 900 fundadores y tope 30 000 (sólo se leyó `ECO_ESC_MAX = 2000`). Nada se ejecutó.
- Que el rango de los sentidos continuos sea [0, 1] (de eso depende qué θ hace silenciosa una regla); el valor inicial −1 de la memoria
  de la última mordida (`motor_bloques.py:878`) no se trató.
- Dónde nace el hijo en el anillo y a qué velocidad se propaga un linaje.
- Si el banco de 200 debe escalar en BLOQ_AZA.
- Que `n_nac` cuente sólo nacidos y en qué ventana; el `reemplazos_por_cuerpo` de hoy es un proxy.
- La profundidad mutacional real: 27–30 es U × generación, con U de toda la corrida. Si el contador real da menos de 20 a esc 90, el
  umbral invalida la base y hay que subir T (regla de §8).
- Los 80 estados canónicos se enumeraron desde `PATM`, no desde el motor.
- No se releyeron `CLAUDE.md`, `PLAN.md` ni `EQUIPO.md` del bundle para este borrador.
- La búsqueda de semillas fue por texto en `.md` y `.py`; no cubre semillas generadas por código con otro formato.
