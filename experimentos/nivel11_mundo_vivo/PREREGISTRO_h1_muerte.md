# PREREGISTRO — H-1: `R₀` sin el regalo. ¿Sostiene este mundo un linaje mortal?

**Misión (primero, siempre): llegar a la AGI por este camino** — un organismo mínimo con reglas locales, sin
retropropagación, que aprende, sobrevive, se reproduce y **evoluciona**. Hoy: **que la muerte mate de verdad, para que
el linaje signifique algo.** Sin selección no hay evolución, y sin muerte no hay selección: por eso H-1 va primera y
por eso, si cae, ninguna de las otras hipótesis de la sala 4 significa nada.

**Del diseñador de H-1 para el coordinador, 18 sep 2026, escrito ANTES de correr nada con `Pool` y ANTES del humo**
(las predicciones del humo van en §8, su resultado en §10). **Semillas NUEVAS: 701–720 (primera serie) y 721–740
(réplica).** Nada se recalibra sobre 261–300: sus números aparecen aquí sólo como *origen declarado de los márgenes*
del brazo de control.

---

## 0. El hecho: hoy la muerte no mata, y el renacer es un recurso

`organismo/organismo_v14.py` (v14.1, `feefc88b1fd8d434`, TRONCO CONGELADO) y toda la cadena del mundo vivo mueren así:

```python
if E<=0 or (vivo and Ag<=0):
    deaths+=1; _mnec[...]+=1; E=.6
    if vivo: Ag=.6
    pos=int(rng.integers(L))
```

**Eso no es morir.** El cuerpo conserva `Wp`, `Wn` (valores rápidos), `Wps`, `Wns` (valores lentos), `KW`, `activa`
(la tabla de códigos), `ncod` (la evidencia por código), `mu`, `err`, `mup`, `mun`, `zp`, `zn` (los estadísticos de
plasticidad), `Wpe`, `Wke` (el predictor) y `Wl` (la locomoción): **el individuo es inmortal en memoria**. Y además
**el renacer regala**: renacer en `E = Ag = 0.6` con `costo = costo_a = 0.001` son **600 pasos de drenaje gratis** y un
escape del anillo atascado. Medido (SALA4 §B E-1, bloque 2 `vivo_rep2_s261-280` y réplica): ese regalo financia el
**34–77 %** de las ventanas de reproducción — el 65–77 % en ESCALAR, el 34–36 % en CUELLO_MIN. La calibración del
bloque 4 de `SALA2`, **sin** el regalo, midió **0.048–0.079 ventanas por vida**: *el fundador muere sin hijos*.

**Consecuencia:** el bloque 2 declaró, con dos series y 8/8 predicciones, que la lectura pesimista saciado
(CUELLO_MIN) lleva el linaje "al filo del reemplazo" (`r ≈ 0`; VIVO −73/−75). Con las medianas de ese bloque,
**R₀ = descendientes / vidas** vale **1.02 en CUELLO_MIN (68 / 66.5)** y **0.209 en VIVO (20 / 95.5)** — pero es un
R₀ de un inmortal que además cobra un subsidio. H-1 pregunta lo único que importa para la evolución: **¿queda algo de
eso cuando el individuo muere de verdad y el nacimiento se paga?**

---

## 1. El instrumento: la muerte que borra, el nacimiento que se paga

**`organismo_vivo_h1.py`**, construido POR ANCLAS por **`construye_vivo_h1.py`** (7 inserciones) desde
**`organismo_vivo_rep2.py` (`96feb4918dc5d694`)**, que aquí **sólo se lee**; cadena: `organismo_vivo_rep`
(`aa823d56c2d4213c`) ← `organismo_vivo` (`20c0961c79de8825`) ← TRONCO `organismo_v14` v14.1 (`feefc88b1fd8d434`).
**Ningún archivo existente se toca** (regla 1). Todos los archivos nuevos van en
`experimentos/nivel11_mundo_vivo/` con sufijo `_h1`.

| perilla | qué hace |
|---|---|
| **`muerte_real=0`** | **la ancla: `organismo_vivo_rep2` BIT A BIT**, clave por clave y con el mismo consumo del `rng` del mundo |
| **`muerte_real=1`** | al morir se **borra la memoria del individuo** — `Wp`, `Wn`, `Wps`, `Wns`, `KW`, `activa`, `ncod`, `_ord`, `mu`, `err`, `mup`, `mun`, `zp`, `zn`, `Wpe`, `Wke`, la sorpresa, las trazas `el`/`tr`, la memoria de rechazo y la **locomoción `Wl`** — y el cuerpo siguiente **nace vacío**, con `rng` propio y con la **dote** que su padre pagó |
| **`hereda`** | `'nada'` (BLANCO) · `'M1'` = **el VECTOR**: `Wps`, `Wns`, la lectura lineal sobre los 6 píxeles, que es portable *por construcción* (la retina es la misma en todo cuerpo; los índices de celda no) · `'M1+pares'` = el vector **y el TOKEN**: `KW`, `activa` + los **pares código ↔ valor** (`Wp`, `Wn`, `ncod`, `_ord`) y sus estadísticos · `'baraja'` = M1 con **los 6 píxeles permutados** (misma magnitud, contenido equivocado) |
| **`dote=0.6`** | E y Ag con que nace el hijo, **pagados por el padre** al cerrarse la ventana (`0 < dote < rep_umbral`, por construcción no mata al padre). **Es exactamente el tamaño del regalo de hoy: lo único que cambia es quién lo paga** |
| **`cola_max=200`** | cola FIFO de descendientes por nacer (si desborda, se descarta el más viejo y se cuenta) |
| **`h1=0`** | los diagnósticos de solo lectura del bloque (exige `rep2=1`) |

**El linaje es EN SERIE: un cuerpo a la vez.** Al cerrarse una ventana de `rep_X` pasos saciado, el padre paga la dote
y encola un descendiente **con la memoria congelada en ESE instante** (no en su muerte: la herencia es del momento del
parto, y se declara). Al morir, nace el primero de la cola. **Si la cola está vacía, el linaje se extinguió** y el
mundo pone un **fundador** con la dote regalada: se cuenta (`fundadores`, `t_fund`) y sus ventanas se marcan
(`desc_fund`). *No se dice "generación"*: no hay solapamiento de cuerpos.

**`ERR-60` (escrito al escribir esta línea, regla 11, antes de medir).** El encargo pedía el `rng` del hijo como
`seed + 700000 + k`. Esa fórmula **colisiona entre semillas vecinas** (`seed=701,k=400` y `seed=702,k=399` dan el
mismo número): es el defecto **I6** que `SALA2` §B.1 ya tenía y que la sala 4 recogió en **E-4** ("los `rng` de los
hijos colisionan entre semillas vecinas"). Se corrige **antes de correr nada**:

```
SEM_HIJO(seed, k) = 700000 + 1000000*seed + k      (guarda dura: k < 100000)
SEM_BARAJA(seed)  = 800000 + 1000000*seed          (generador propio; permutación NUEVA en cada parto)
```

Ninguno choca con el `rng` del mundo (`seed`) ni con el del control barajado del mundo vivo (`seed + 900000`).
**El `rng` DEL MUNDO no se consume de más:** el constructor lo comprueba con una expresión regular sobre cada
inserción, y el arnés lo mide (caso D).

**Lo que NO se hereda en ningún brazo, y se declara:** la política de locomoción `Wl` (aproximarse/alejarse). Así los
cuatro brazos MUERE pagan el mismo precio de cuerpo y el único contraste es **la memoria de valor**.

---

## 2. Brazos y semillas

**Principales (5 modos × 2 cuerpos = 10).** Cuerpos: **VIVO** (dos necesidades, cuatro estímulos) y **CM** =
CUELLO_MIN (`rep_cuello=2`: saciado, la boca lee el **mínimo de las dos filas** — la lectura pesimista ya declarada en
el bloque 2). Perillas comunes: `reproduccion=1, rep_mide=1, rep_X=500, rep_umbral=1.0, rep_coste=0, rep2=1,
rep2_regalo=600, h1=1`.

| brazo | modo | papel |
|---|---|---|
| **RENACE_CM · RENACE_VIVO** | `muerte_real=0` | **control con sha**: la muerte de hoy. Tiene que reproducir el bloque 2 o no se lee nada (H1-1) |
| **NADA_CM · NADA_VIVO** | `muerte_real=1, hereda='nada'` | BLANCO: la muerte que mata sin herencia |
| **M1_CM · M1_VIVO** | `hereda='M1'` | el VECTOR de valores |
| **PARES_CM · PARES_VIVO** | `hereda='M1+pares'` | el vector Y el token (H-7 de la sala 4) |
| **BARAJA_CM · BARAJA_VIVO** | `hereda='baraja'` | **la predicción que decide**: BARAJA ≈ NADA |

**Rampa (10 brazos más, sólo sobre CUELLO_MIN, en NADA y M1).** Las cuatro perillas que H-1 nombra: `dote 0.3`,
`dote 0.9`, `rep_X 250`, `nobj 8`, `costo = costo_a = 0.0005` (con `rep2_regalo = 1200`, porque el regalo dura
`A_muerte / costo` pasos). **La rampa es BÚSQUEDA, NO EVIDENCIA** (§6): su único papel es la cláusula de cierre H1-6.

**20 brazos × 20 semillas × 100 000 pasos = 400 corridas por serie.** Semillas **701–720** y réplica **721–740**
(regla 12); **no chocan con nada**: los bloques del 18 sep llegaron hasta 661–680 y ninguno usó las 7xx.
**Alias estructurales** (`diagnostico_codigos.py`, sin simular, calculado antes): **701–720 → [715]** (`|code(D)&code(C)| = 3`:
sal == agua); **721–740 → ninguna**. Se reporta el conjunto completo y al lado las LIMPIAS, mismos umbrales (regla 10).

---

## 3. Medidas

Todas por corrida de 100 000 pasos, todas de solo lectura:

- **`R₀` = descendientes / vidas** = `descendientes / (muertes + 1)` — **ventanas de reproducción por vida.** Es la
  medida de H-1. `R₀ < 1` ⟺ el linaje no se reemplaza.
- **`r` = descendientes − muertes** por 100 000 pasos (la medida validada del bloque 2, ERR-40).
- **vida mediana** — de `vidas_h1` (**sin tope**, no la lista capada a 400 de rep2), y partida por origen:
  `vida_med_fund` (cuerpos fundados por el mundo) contra `vida_med_her` (cuerpos que nacieron de una dote pagada).
- **`frac_regalo` (OBLIGATORIO)** = `desc_regalo / descendientes`, la clave de rep2 tal cual, y su versión limpia
  **`frac_fund` = `desc_fund / descendientes`** = ventanas cuya cuenta empezó dentro de los `rep2_regalo` pasos de un
  nacimiento **NO pagado** (el `t = 0` inicial y cada fundación tras una extinción). Es el único regalo que queda.
- **`fundadores`** (veces que el linaje se extinguió) y **`t_fund1`** (primera extinción).
- **`R0_her`** = descendientes por cuerpo, **contando sólo los cuerpos heredados** — la lectura afilada de si heredar sirve.
- Covariables que se **reportan sin puerta**: `xor01`, celdas estrictas, `sac_tasa`, `exposiciones`. **`xor01` no es
  puerta en los brazos MUERE**: con muerte real la tabla al final de la corrida es de un **mosaico de cuerpos**, no de
  un individuo — usarla como puerta sería vocabulario inflado (regla 6).

**Estadística (ERR-37).** `R₀`, `r`, descendientes, muertes, vidas y fracciones son **integrales de trayectoria** →
**A₁₂ sin parear** (400 pares), medianas y cuartiles. Ningún `max` sobre lecturas; un `None` nunca cuenta como
victoria. **`ERR-61` (escrito aquí, regla 11):** el encargo pedía la puerta de H1-3 como "≥ 15/20 **pareado**". `R₀`
es integral de trayectoria (ERR-37b) y las trayectorias divergen desde la primera mordida, así que **la puerta que
decide es A₁₂ sin parear (≥ 0.80) más la razón de medianas (≥ 1.30)**; el conteo pareado k/20 se calcula, se imprime
y **se reporta al lado sin decidir**.

---

## 4. Predicciones — umbrales escritos ANTES de medir

| # | predicción (701–720) | de dónde sale | refutación |
|---|---|---|---|
| **H1-1** | **ancla del control**: mediana `R₀` **RENACE_CM ∈ [0.70, 1.40]** y **RENACE_VIVO ∈ [0.12, 0.32]**; mediana `r` **RENACE_CM ∈ [−50, +25]** y **RENACE_VIVO ∈ [−115, −45]**; `frac_regalo` RENACE_CM **∈ [0.20, 0.55]** | bloque 2 ×2 series: R₀ 68/66.5 = 1.02 y 20/95.5 = 0.209; r +3/−3 y −73/−75 (intervalos de P2-2, ya acertados dos veces); regalo 0.34–0.36 | **si cae, el instrumento se movió y NO SE LEE NADA MÁS**: se revisan arnés y shas |
| **H1-2** | **la muerte mata**: mediana `R₀`(NADA_CM) **≤ 0.35** y `R₀`(NADA_VIVO) **≤ 0.20**; A₁₂(RENACE_CM > NADA_CM) **≥ 0.90** y A₁₂(RENACE_VIVO > NADA_VIVO) **≥ 0.85**; vida mediana NADA_CM **≤ 0.60 ×** RENACE_CM | `SALA2` bloque 4 sin el regalo: 0.048–0.079 ventanas/vida. Un cuerpo vacío muerde con `pb ≈ 0.99` (su valor es 0) y el veneno le quita 0.4 de 0.6: muere en 2–3 mordidas | **`R₀`(NADA_CM) ≥ 0.90 → borrar la memoria no cambia el linaje**: el regalo del renacer era **energía, no memoria**, y se dice con ERR |
| **H1-3** | **la herencia paga**: `R₀`(M1_CM) **≥ 1.30 ×** `R₀`(NADA_CM) **y** A₁₂(M1_CM > NADA_CM) **≥ 0.80** (esto decide, ERR-61); pareado k/20 **≥ 15** se reporta al lado | con `ncod` vacío la puerta de familiaridad nunca dispara, así que la boca del recién nacido lee **exactamente la vía lenta**: el vector heredado es utilizable **desde la primera mordida** | A₁₂ **≤ 0.60** → heredar el vector de valores no compra nada; el cuello está en otro sitio |
| **H1-4** | **la predicción que decide — BARAJA ≈ NADA**: \|`R₀`(BARAJA_CM) − `R₀`(NADA_CM)\| **≤ 0.10** y **0.35 ≤ A₁₂(BARAJA_CM > NADA_CM) ≤ 0.65** | es la predicción que `SALA2` C.2 bloque 4 dejó escrita (**BARAJA ≈ BLANCO**) y que E-11 reclama: si el contenido del vector es lo que viaja, permutar los píxeles lo destruye | **(a)** BARAJA ≈ M1 (A₁₂(BARAJA > NADA) ≥ 0.80 **y** \|R₀ BARAJA − M1\| ≤ 0.10) → **lo heredable es la MAGNITUD** (una cautela heredada), no el contenido: ERR y se dice. **(b)** A₁₂(BARAJA > NADA) **≤ 0.20** → heredar en los píxeles equivocados es **peor** que no heredar |
| **H1-5** | **¿el vector o el token?** (H-7): A₁₂(PARES_CM > M1_CM) **≥ 0.65** y `R₀`(PARES_CM) ≥ `R₀`(M1_CM) | con el token el hijo puede además usar la vía rápida (los pares código↔valor) desde el primer paso | A₁₂ **≤ 0.50** → **lo portable entre cuerpos es el VECTOR**, no el token. *Las dos direcciones se declaran*: la pregunta de E-11 se contesta gane quien gane |
| **H1-6** | **cláusula de cierre de H-1**: algún brazo con muerte real (principal **o** de rampa) alcanza mediana `R₀` **≥ 0.90** con mediana `fundadores` **≤ 2** y con su NADA pareado por debajo de 1.0 | H-1 nombra cuatro perillas (`rep_X`, `dote`, `costo`, `nobj`): la rampa las recorre una vez cada una | **si NINGUNO lo alcanza → `ERR-62`: este mundo NO SOSTIENE LINAJES MORTALES con estas cuatro perillas**, y la línea de evolución no se corre hasta cambiar el **MUNDO** (no el umbral). Si alguno lo alcanza, **no se declara aquí** (§6) |
| **H1-7** | **sin el regalo (obligatorio)**: mediana `frac_fund` **≤ 0.15** en los cuatro brazos MUERE_CM; `frac_regalo` se reporta en los diez principales | con `dote` el 0.6 lo paga el padre: el único regalo que queda es el de las fundaciones tras una extinción | `frac_fund` **> 0.35** en algún MUERE → el regalo sigue financiando y la medida **no está limpia** |
| **H1-8** | **seguridad y contabilidad**: coherencia contable **20/20** en los veinte brazos (`nacimientos = muertes`, `len(vidas_h1) = len(origen_cuerpo) = len(desc_por_vida) = muertes + 1`, `Σ vidas_h1 = T`, `Σ desc_por_vida = descendientes`, `fundadores + 1 = ceros de origen_cuerpo`); `cola_desborde = 0` en 20/20; `exposiciones[A]` NADA_CM **≥ 0.50 ×** RENACE_CM | arnés 62/62 | coherencia < 20/20 → **instrumento**, se para. Comida < 0.50× → los cuerpos vacíos vacían el anillo y `R₀` se lee neto |

---

## 5. Las cuatro trampas de la noche del 17-sep, y las propias

1. *Canal social simétrico* — n/a (no hay canal aquí). 2. *Acierto sin balancear* — no se usa acierto: `R₀` y tasas
por estímulo. 3. *El mundo que se come la comida* — H1-8 la acota con `exposiciones[A]`; y **la muerte como recurso**
es la trampa propia de este mundo: es exactamente lo que H-1 desmonta, y lo que queda se mide (`frac_fund`).
4. *Sitios fijos* — `spawn()` sortea.

**Propias, declaradas:**
(i) **La dote reintroduce el regalo por la puerta de atrás.** Se controla por construcción (el padre paga lo mismo que
recibe el hijo, y `rep_umbral − dote > 0`) y se mide (`frac_fund`, H1-7).
(ii) **Si `R₀` ≪ 1 en NADA, casi todos los nacimientos son fundaciones y los cuatro brazos MUERE se parecerían por
falta de partos, no por falta de herencia.** Por eso se reportan `heredados` y **`R0_her`** y `vida_med_her` contra
`vida_med_fund`: si `heredados` es mediana < 5 en NADA_CM, H1-3/H1-4/H1-5 **se reportan como de baja potencia** y la
decisión pasa a la rampa (que es donde `R₀` sube) y al bloque nuevo.
(iii) **Elegir el brazo mirando el dato.** La rampa lo haría: por eso la rampa **no puede declarar nada** (§6).
(iv) **`xor01` como puerta** sería vocabulario inflado con muerte real: se reporta, no decide (§3).

---

## 6. Lo que NO se declara

- **Nada nace**: `descendientes` sigue siendo un contador de ventanas; lo que H-1 agrega es que **el cuerpo siguiente
  es otro individuo**. No se dice "población" (hay un cuerpo a la vez), "generación" (no se solapan), "selección",
  "evoluciona", "especie", "quiere".
- **La rampa no declara.** Si algún punto de rampa pasa H1-6, lo único que se escribe es *"hay un ajuste del mundo en
  el que el linaje mortal se reemplaza"*, y **el siguiente paso es un preregistro nuevo con semillas nuevas sobre ese
  punto** — nunca se declara sobre la rampa que lo encontró (ERR-37a y regla 4).
- Un pase de H1-6 con `rep_X = 250` vale **menos** y se dice: la ventana a la mitad hace el descendiente más barato.
- 20 semillas no cierran nada: piden la réplica 721–740 (regla 12).

---

## 7. Entregables

`construye_vivo_h1.py`, `organismo_vivo_h1.py`, `identidad_vivo_h1.py`, `corre_vivo_h1.py` (`--humo` de un proceso;
`Pool` sólo el coordinador: `--desde 701`, réplica `--desde 721`), este preregistro, el humo
(`datos/vivo_h1_humo_*`), el arnés (`datos/vivo_h1_identidad_20260918.log`). **ERR-54:** el runner guarda el JSON
**crudo** antes de analizar nada.

---

## 8. Humo (UN proceso, 4 corridas de T = 100 000: RENACE_CM y NADA_CM × semillas 1, 2) — predicciones ANTES de lanzarlo

- **HH1** `r`(RENACE_CM) > `r`(NADA_CM) en 2/2 (misma semilla).
- **HH2** `R₀`(NADA_CM) < 1 en 2/2 **y** `R₀`(RENACE_CM) > `R₀`(NADA_CM) en 2/2.
- **HH3** coherencia contable en 4/4 (`nacimientos = muertes`; `Σ vidas_h1 = T`; `Σ desc_por_vida = descendientes`;
  `fundaciones + 1 = ceros de origen_cuerpo`).
- **HH4** vida mediana NADA_CM < RENACE_CM en 2/2.
- **HH5** `fundadores`(NADA_CM) ≥ 1 en 2/2 (el linaje se extingue al menos una vez).
- **HH6** (blanda) `frac_fund`(NADA_CM) ≤ 0.35 en 2/2.

**Sólo HH3 bloquea**: si la contabilidad no cierra, el instrumento está roto y no se corre nada. **HH1, HH2, HH4 y
HH5 son la hipótesis, no el instrumento**: si fallan, se escriben aquí y **el bloque corre con esta letra** — un humo
no puede refutar ni confirmar nada (n = 1–2, semillas ya vistas). **No se cambia ningún umbral después del humo.**

---

## 9. Arnés — resultado: **62/62** (`datos/vivo_h1_identidad_20260918.log`; un proceso, T = 20 000, semillas 1–2)

`organismo_vivo_h1.py` **`9e99ff87b5e2db1e`** · `construye_vivo_h1.py` **`07da8128adc82f4e`** · 7 inserciones,
ninguna consume el `rng` del mundo.

- **(A)** apagada (`muerte_real=0, h1=0`) ≡ `organismo_vivo_rep2` en los **7 brazos del bloque 2**, todas las claves: **14/14**
- **(B)** cadena: `reproduccion=0` ≡ `organismo_vivo`; **todas las perillas de H-1 encendidas con la maestra apagada** (inertes);
  `vivo=0, n_nec=1` ≡ `organismo_v14` (TRONCO): **6/6**
- **(C)** `h1=1` con `muerte_real=0`: claves viejas bit a bit + **exactamente 15 nuevas**, y coherencia contable: **8/8**
- **(D)** **antes de la primera muerte**: con `muerte_real=1` y `T` = paso de la primera muerte (349 y 119), **todo
  idéntico a rep2**: ninguna línea nueva consume el `rng` del mundo ni toca el estado antes de que alguien muera: **4/4**
- **(E)** muere de verdad: coherencia contable en los cuatro modos de herencia: **8/8**
- **(F)** determinismo (los `rng` derivados son función de `(seed, k)`, no del reloj): **2/2**
- **(G)** el barajado baraja (permutación nueva por parto; 0 permutaciones identidad, y 0 en los otros modos): **4/4**
- **(H)** **deben fallar**: NADA ≠ RENACE · M1 ≠ NADA · M1+PARES ≠ M1 · BARAJA ≠ M1 · `dote 0.3` ≠ `dote 0.6`: **10/10**
  (si alguno saliera idéntico, la perilla sería inerte y el instrumento estaría roto — ERR-38)
- **(I)** guardias: seis combinaciones prohibidas lanzan `SystemExit`: **6/6**

**Dato lateral del arnés (T = 20 000, semillas 1–2; NO es humo ni evidencia):** con muerte real y `dote = 0.6`,
CUELLO_MIN hace 48–58 cuerpos por corrida con `R₀` **0.074–0.160**, de los cuales **41–51 son fundaciones** (el linaje
se extingue casi en cada muerte). La dirección de H1-2 se ve ya ahí.

---

## 10. Humo — resultado (18 sep 19:17; `datos/vivo_h1_humo_20260918_191715.{log,json}`, sha del JSON `9c5ce2fd6d84667e`; identidad dentro del runner **10/10**; ERR-38 campo a campo OK; 7.4–7.9 s por corrida)

| brazo | s | **R₀** | r | desc | muertes | cuerpos | vida mediana (fund/her) | fundaciones | regalo / fund | coherente |
|---|---|---|---|---|---|---|---|---|---|---|
| RENACE_CM | 1 | **1.031** | **+3** | 67 | 64 | 65 | 756 (756 / —) | 0 | 0.358 / 0.0 | sí |
| NADA_CM | 1 | **0.182** | −188 | 42 | 230 | 231 | 125 (174 / 75) | **188** | 0.690 / **0.571** | sí |
| RENACE_CM | 2 | **0.955** | **−2** | 64 | 66 | 67 | 857 (857 / —) | 0 | 0.344 / 0.0 | sí |
| NADA_CM | 2 | **0.159** | −190 | 36 | 226 | 227 | 119 (102 / 162) | **190** | 0.611 / **0.583** | sí |

**HH1, HH2, HH3, HH4, HH5: SÍ. HH6 (blanda): NO** — 5/6.

- **El control ancla exactamente.** RENACE_CM da `r` **+3 / −2** contra el **+3 / −3** del bloque 2, vida mediana
  **756 / 857** contra 827, `frac_regalo` **0.358 / 0.344** contra 0.34–0.36: el instrumento no se movió.
- **Con la muerte que mata, el linaje se desploma.** `R₀` pasa de **1.03 / 0.96** a **0.18 / 0.16**; la vida mediana de
  **756 / 857** a **125 / 119**; los cuerpos por corrida de 65 / 67 a **231 / 227**; `r` de +3 / −2 a **−188 / −190**.
  La primera extinción llega en `t = 349` y `t = 119` — con la memoria borrada, **el fundador muere sin hijos casi
  siempre**: 188 de 231 y 190 de 227 cuerpos son fundaciones del mundo.
- **HH6 falla, y falla hacia donde importa.** `frac_fund` **0.571 / 0.583**: más de la mitad de las ventanas de
  NADA_CM las financia el regalo de una fundación. *Escrito después del humo, sin tocar ningún umbral:* esto **no
  debilita H1-2, la refuerza** — el `R₀` medido en los brazos MUERE es una **cota SUPERIOR** del `R₀` de un linaje
  mortal, porque el mundo repone gratis al fundador cada vez que el linaje se extingue. H1-7 seguramente caerá en el
  bloque, y su lectura será exactamente ésa. **No se cambia el umbral de H1-7** (regla 4): cae y se dice.
- `heredados` es 42 y 36 por corrida (no < 5), así que la salvaguarda (ii) de §5 no se dispara y H1-3 / H1-4 / H1-5
  tienen potencia en el bloque.
- Ninguna cifra del humo es evidencia (n = 1–2, semillas ya vistas); **no se cambia ningún umbral**. El bloque corre
  con esta letra en 701–720 y réplica 721–740.
