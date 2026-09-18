# SALA 2 — ángulo *mundo_grande*: UN MUNDO QUE OBLIGUE (diseño de v16 desde v14.1, por anclas)

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales, sin backprop en el
runtime, que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada. Primero llegar a la
frontera; segundo, que viva. El método manda sobre el cómo (`registro/EQUIPO.md`, `CLAUDE.md` reglas 1–12).

**Creador de la sala 2, 18 sep 2026, ~10:00.** Nada de esto se corrió con `Pool`; no se editó ningún archivo del repo; no hay
commit. Lo único ejecutado: `diagnostico_familias_sala2.py` (en esta carpeta), un cálculo **estructural con T = 0** — construye
`KW` como el tronco y lee códigos, no simula un paso del organismo; 6 configuraciones, < 2 s; salida en
`diagnostico_familias_sala2_salida.json`. Es la misma clase de instrumento que `negativo_codigo.py` / `diagnostico_codigos.py`.

**Fuentes leídas, en orden:** `CLAUDE.md` (día 7), `PLAN.md` (18 sep), `HANDOFF.md` §13, §15.7–15.8, `REGISTRO_etapas_1_2.md`
desde ERR-35 hasta ERR-42, `ENJAMBRE_xor_20260918.md`, `PUENTE_creacion.md` A12–A16 y B-5, `PREREGISTRO_v15e.md`,
`PREREGISTRO_mundo_vivo.md`, `PREREGISTRO_reproduccion.md` (+ `_2`), `organismo/organismo_v14.py` entero (feefc88b1fd8d434), y
como apoyo `organismo_vivo.py`, `construye_capD.py`, `mundo_grande.py`, `organismo_v14g.py`, `bateria_generaliza.py`.

**Hipótesis del director que integro (09:40, textual):** *"si sal es sal será número uno, lo guardo, lo vectoriza; y después sal rosa
lo vectoriza, marca como sal y lo plantea como una variable de lo mismo — eso es lenguaje. Ahora, si pensamos en el aprendizaje,
[…] puede aprender y desaprender"*; y (05:10) *"la palabra es grafo, no vectorización"*. Traducción operativa que uso: **token** =
el código exacto del tronco cuando acumula evidencia (`ncod ≥ 5` y una celda consolidada: la puerta por código de v14 **ya es** el
"lo guardo, será número uno"); **variable de lo mismo** = un patrón cuyo código comparte K−1 celdas con un token se lee **por el
token**; **excepción** = un nodo aparte, ligado a (token, celda que sobra), con valor propio; **grafo** = nodos (códigos con
evidencia, nodos de excepción) y aristas (pertenencia por K−1 celdas; token → excepción); `KW` y los códigos son el **soporte**
en alta dimensión, no la ruta. **Desaprender** = la excepción se sobrescribe o se borra con la última mordida; el token desaprende
por sus celdas (la dinámica de v14.1) y **todos sus miembros lo siguen sin morder**.

---

## 1. Qué bloquea, según mi lectura (con la evidencia del registro)

| bloqueo | evidencia (registro) | qué exige |
|---|---|---|
| **B1. El mundo no identifica.** Con 6 px y 8 patrones, 9 de 15 hipótesis conjuntivas ajustan con residuo 0; ningún aprendiz (local, gradiente exacto 0.562, MLP 0.531) puede elegir; con 14 ejemplos la regla local llega a 1.000. | ERR-35; A12–A14; bloque 2/3 (A-6) | un mundo que dé **ejemplos distintos del mismo concepto sin pedirlos**: familias token + variantes |
| **B2. El único cruce de XOR es un prior que no escala.** M3 cruza con 8 ejemplos porque enumera los 15 pares de píxeles; "15 pares son 15, pero C(n,2) no lo es". | bloque 3/3, ENJAMBRE §6 | un prior que la **estructura del mundo dé gratis**: (token × variable), no (píxel × píxel) |
| **B3. La memoria de un golpe no se desdice; la reescribible pierde la identificabilidad.** v15d: E2 0/20, E1 0/20. v15e: arregla E1/E2 (lee R exacto tras una mordida, se desdice en una) y pierde XOR (0.25 < 0.375 en el humo; en la serie 141–160, 0.500 contra 0.438). | v15d, v15e, A16, commit 5936893 | que lo reescribible se **indexe por estructura dada** (token, variable), no por competencia entre 15 candidatos |
| **B4. El código K = 3 de 90 no es un tokenizador.** Dos estímulos comparten código en 9 % de las semillas con 4 estímulos y **170/200** con 20; 135/200 tienen una fuga exacta de un patrón nunca visto a uno entrenado. Con 12 px y 32 estímulos (§1.1): alias en 199/200 semillas. | bloque de la sal, B-5 negativo, `diagnostico_familias_sala2` | medir el **techo de tokenización** del código antes de pedirle que tokenice |
| **B5. La generalización del tronco es lineal por píxel y "el olvido de lo ausente" es interferencia (0.67).** Una variante que contradice al token (sal rosa = comida) mueve la vía lenta 0.15·4 = 0.6 por píxel en UNA mordida y arrastra los 3 píxeles de la base. | Etapa 3 (v9), mundo largo 1b, A16 §5 (la lineal oscila sobre XOR) | que la excepción se ate al **token**, no al píxel, y que la mordida de una excepción **no entrene la vía lenta** |
| **B6. La capacidad es por patrón.** N\* 51 a 6 px; en el mundo largo (50 patrones, valencias al azar) la adquisición cae a 0.55–0.70. Un valor por variante no comparte nada con su token salvo por fuga. | capacidad grande, mundo largo | que las **exposiciones escalen con tokens + excepciones, no con estímulos** |
| **B7. Un cero no veta a la boca; la memoria de rechazo y el hambre deciden el muestreo.** `Vb = 1.2·W + 2·hambre + 0.5` | enmienda 1 del mundo vivo | contar **mordidas tras el descubrimiento**, no encuentros: la política es la misma en los dos organismos |

**Lectura de conjunto.** Todo lo que hoy "generaliza" en el tronco es **fuga**: por píxel (vía lenta) o por celdas compartidas
(vía rápida, la interferencia de v9). Funciona mientras el mundo es lineal y se rompe donde el mundo dice "esto es lo mismo, salvo
en este caso". Ningún mundo del repo obliga a representar **la relación** entre dos cosas (sal, sal rosa): con 4 estímulos no hace
falta; con 20 al azar no existe. El bloqueo no es de regla ni de dimensión: **es del mundo, que no castiga la representación
equivocada** salvo en esquinas diseñadas a mano (XOR, alias).

### 1.1 El número que decide el diseño (calculado, T = 0; 200 semillas por configuración; `K = 3`)

Retina `D = 12` = 9 píxeles de *forma* + 3 de *variable* (rosa, azul, verde). 8 tokens de peso 3 sobre los 9 de forma; cada token
tiene 3 variantes = token + 1 píxel de variable → 32 estímulos. `KW` sorteada exactamente como el tronco (`Wl` y luego
`KW ~ U(0,1)`), sin `cond()`.

| celdas activas | variante comparte ≥ K−1 celdas con SU token ("tokeniza") | código exacto = token (alias variante–token) | ≥ K−1 con OTRO token (familia falsa) | ≤ K−2 con todos (huérfana) | semillas con dos tokens de código idéntico | dos estímulos idénticos |
|---|---|---|---|---|---|---|
| 30 (arranque del tronco) | **0.667** (media 0.658) | 0.125 | 0.125 | 0.167 | 38/200 | **199/200** |
| 60 (régimen a mitad de corrida) | 0.542 | 0.083 | 0.083 | 0.375 | 18/200 | 190/200 |
| 90 (pool lleno) | **0.500** | 0.042 | 0.042 | 0.458 | 12/200 | 179/200 |
| 30, píxel variable a intensidad 0.5 | 0.917 | 0.375 | 0.042 | 0.042 | 38/200 | 200/200 |
| `D = 9`, 4 tokens (mundo chico) | 0.667 | 0.167 | 0.083 | 0.250 | 23/200 | 183/200 |

**Consecuencias, escritas antes de correr nada:** (i) un tokenizador que lea el código crudo con tolerancia K−1 **tiene techo
0.50–0.67**, y el techo *baja* a medida que el tronco gana celdas (el código se afina); (ii) el 12 % de las variantes completa a
un token equivocado → **familias falsas** que el organismo no puede distinguir del contenido; (iii) el 8–14 % de las variantes **es**
su token para la vía rápida (código exacto): ésas sólo se separan por fisión (v11), no por un nodo de excepción; (iv) el alias
entre estímulos es la regla (199/200), como midió B-5 con 20 patrones. Por eso el diseño **mide primero el techo por semilla**
(subconjunto estructural, regla 10) y pone la predicción de la tasa de tokenización **dentro** de ese techo: si sale por encima,
es fuga, no capacidad. La intensidad 0.5 no se usa: tunear el mundo a la debilidad del código sería humo (§6).

---

## 2. Mecanismo: v16 = v14.1 + mundo de familias (por anclas) + perilla `token` (por anclas)

Dos capas, cada una con identidad propia y apagada bit a bit:

### 2.1 El mundo (instrumento, no órgano): `organismo_grande.py` ← `organismo/organismo_v14.py` (sólo lectura)

Cadena de anclas ya probadas en el repo: **retina D** (las 4–5 anclas de `construye_capD.py`: `KW (NKMAX,6)`, `rng.uniform(0,1,(NK,6))`,
`mu (NKMAX,6)`, `tr(9)`, `Wl (2,9)`, `Wps/Wns(6)` → `D`, `D+3`; con patrones de 6 px, **mismo consumo del rng**) + **patrones y
valencias del mundo** (`pats`, `val`, `tipos` como en `organismo_vivo`: el único sorteo sensible es `spawn(): rng.integers(len(tipos))`,
así que **con dos estímulos el flujo del rng es el de v14.1**) + **necesidades** (peldaño 2: la cadena de `construye_vivo.py`, 37/37).

```
def mundo_familias(seed, D=12, V=3, F=8, n_exc=4, deriva=5000, cambio=T//2):     # rng PROPIO 30000+seed, como split_regla
    forma = D-V; tokens = F combinaciones distintas de 3 px de forma (sorteadas)      # 'T0'..'T7'
    variantes = token + 1 px de variable -> 'T3v1' = T3 + rosa                        # 32 patrones, todos peso 3 o 4
    val[Tk] = comida/veneno alternando (4 y 4);  val[Tk v] = val[Tk]                   # la variante ES el token...
    exc = n_exc pares (k, v) sorteados, a lo sumo uno por token: val[Tk v] = opuesto   # ...salvo las excepciones
    presentes(t) = los 8 tokens + UNA variante por token, la (t // deriva) mod V       # SECUENCIA: la variante presente rota
    en t == cambio: val[T0] y val[T0 v] no-excepcion se invierten; la excepcion de T0 conserva su valencia absoluta
```
Decisiones tomadas ahora, no después: *deriva* cada 5 000 pasos (20 eventos en T = 100 000; en cada evento los objetos de la variante
que sale pasan a ser la que entra, **sin sorteo**); el cambio a T/2 invierte **una familia** (T0, que por construcción lleva una
excepción); la excepción **conserva su valencia absoluta** ("la sustancia cambió; lo que ya era distinto sigue siendo lo que era"
— la otra semántica, "todo se niega", es OTRO mundo y se escribe como brazo no construido). Mundos-control: `lineal` (`n_exc = 0`),
`excepciones` (`n_exc = 4`), `azar` (valencia sorteada por patrón: no hay familias), `barajado` (cada variante toma la valencia de
OTRO token: familias falsas por construcción). Peldaño 1: una necesidad, dos valencias. Peldaño 2: cuerpo del mundo vivo (dos
recursos que se agotan; 4 valencias comida/veneno/agua/sal, 2 tokens por valencia; filas por necesidad; el cambio = comida ↔ veneno
en T0 y agua ↔ sal en T4). Peldaño 3 (no diseñado aquí, una línea): el estímulo compuesto llega **en dos cuadros** (token, luego
variable) y la complección usa el código del cuadro anterior — el aparato de 3T-k.

### 2.2 La perilla `token` (el órgano candidato), anclas sobre `organismo_v14.py`

Estado nuevo: `nenc = {}` (encuentros por código exacto; sólo lectura hasta la 2.ª visita), `_slot = {}` (nodos de excepción:
`(clave_token, frozenset(celdas_que_sobran)) → R`), contadores de sólo lectura. **Constantes nuevas: `tok_min = K−1 = 2`
(estructural, no se barre) y `umbral_exc = 2.0` = la mitad del salto |R| entre valencias (|+1 − (−3)| = 4); un token consolidado
deja residuos ≤ 0.3 (E1: W_B −2.96…−2.99) y una excepción deja 4.** `rng` intacto: ninguna línea nueva sortea.

```
# A1  firma: ...,pat_min=1):  ->  ...,pat_min=1,token=0,tok_min=2,umbral_exc=2.0):
# A2  estado, tras  ncod={}; _ord=[] :
nenc={}; _slot={}; _tk=[0]*4; _sl=[0]*4                                  # token: encuentros por codigo, nodos de excepcion, lecturas
# A3  tras _fam:  el TOKEN al que pertenece un codigo (grafo: arista por K-1 celdas compartidas)
def _tok(_k):                                                            # None si token=0 -> v14.1 exacto
    if not token: return None
    _q=_key(_k)
    if nenc.get(_q,0)<1: return None                                     # 1er encuentro: se lee como v14.1 (G1/G2 identicos por construccion)
    _c=[(len(_q&_o),ncod[_o],_o) for _o in _ord if _o!=_q and len(_q&_o)>=tok_min and _fam(kenyon_de(_o))]
    return max(_c)[2] if _c else None                                    # empate: mas evidencia; sin rng
def _ruta(_k,P):                                                         # (valor que lee la boca, modo)
    _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)
    if puerta is None: return _f+_s,'suma'
    if _fam(_k): return _f,'exacto'                                      # <- v14.1 tal cual (prioridad: el propio codigo)
    _t=_tok(_k)
    if _t is None: return _s,'lenta'                                     # <- v14.1 tal cual
    _x=(_t,_q-_t)                                                        # la celda que sobra = la VARIABLE
    if _x in _slot: return _slot[_x],'slot'                              # nodo de excepcion: valor propio
    return float((Wp-Wn)@kenyon_de(_t)),'token'                          # variable de lo mismo: lee el token
# A4  valor(P) y la boca (linea _wt=...) llaman a _ruta; con token=0 la expresion evaluada es la de v14.1 bit a bit
# A5  tras vis[kk][q(t)]+=1 :   if token: nenc[_key(kc)]=nenc.get(_key(kc),0)+1     (DESPUES de leer: la 1a visita es v14.1)
# A6  dentro de if mordio: / if learn:, ANTES de dlt=...:
if token and _modo in ('token','slot'):
    _res=R-float((Wp-Wn)@kenyon_de(_t))                                   # residuo respecto del TOKEN, no de la lineal (A16 §5)
    if abs(_res)>umbral_exc: _slot[_x]=R                                  # se escribe/sobrescribe de un golpe (aprende en 1)
    elif _x in _slot: del _slot[_x]                                       # el mundo volvio a "lo mismo": se borra (desaprende en 1)
    if _modo=='slot' or abs(_res)>umbral_exc: continue_sin_aprender()     # el grafo explica la mordida: ni celdas ni via lenta
# A7  salida: claves nuevas (tok_hits, n_slots, slots, tasa_tokeniza) SOLO si token: el dict apagado es el de v14.1
```
**Apagado ≡ v14.1 bit a bit:** todo vive bajo `if token:`; `_fam`, `valor`, la boca y el bloque de aprendizaje evalúan con `token=0`
exactamente las expresiones del tronco; el rng no se toca. **Encendido en el mundo A/B del examen: inerte por construcción**
(`cond()` impone `code(A) ∩ code(B) = ∅` → ningún código comparte K−1 celdas con otro familiar → `_tok` devuelve `None` siempre
→ identidad **medida**, como el I5 de B-5). Donde sí actúa dentro del examen: 4a–4d (`solap_B ∈ {1, 2, 3}`): con `C∩B = 2`, C se lee
por el token B desde su 2.ª visita → conducta distinta a v14.1 → **se declara: el examen ON puede diferir de la identidad en 4a–4d y
debe pasar la letra igual.**

**Qué NO hay:** tasa, clip, decaimiento del nodo, cambio en la rápida, la lenta, la hija dispersa o la puerta exacta; no hay
"núcleo" incremental (la intersección de códigos de una familia): la pertenencia es K−1 celdas con un código exacto familiar, y
punto. Memoria nueva: `n_slots` × 1 float + `nenc` (enteros por código). **Lo que la arquitectura decide sola:** un patrón cuyo
código exacto **es** el del token (alias variante–token, 8–14 %) sigue el camino de v14.1 (`_fam` primero): si es excepción,
sólo la fisión de v11 puede separarlo — se cuenta aparte.

### 2.3 Aprender y desaprender, en el mecanismo

| qué | v14.1 | v16 (`token = 1`) |
|---|---|---|
| variante no-excepción, 2.ª visita | la lenta (fuga por píxel) hasta 5 mordidas de su código exacto | **el token** (sus celdas): sin morderla |
| excepción, 1.ª mordida tras el descubrimiento | `_ds = R − _ws = +4`: la lenta mueve 0.6/px (arrastra la base y a los hermanos); la rápida necesita ≥ 5 mordidas + consolidación; fisión en las celdas compartidas | **nodo de excepción escrito de un golpe**; la mordida no entrena celdas ni lenta |
| la excepción deja de serlo (T0 cambia y su excepción ya vale lo mismo que T0) | nada que borrar: relearn por mordidas | **el nodo se borra en la 1.ª mordida** (`|R − W_tok| ≤ 2`) |
| cambio de familia (T0 invierte) | las celdas de T0 relearn (inversión pura no fisiona: `dist = 0`, B-5); las variantes siguen por fuga parcial | las celdas de T0 relearn **y todos los miembros lo siguen por la arista**, 0 mordidas |

---

## 3. Por qué sale de la frontera: la capacidad NUEVA y MEDIBLE

**Capacidad: economía de exposiciones por estructura.** Suma, sobre los 32 estímulos, de las **mordidas tras el descubrimiento
hasta que el valor leído tiene el signo del mundo** (`exp_total`), y su **escalado**: con v16 debe crecer con `#tokens + #excepciones`
(≈ 8·b + 4·1 + huérfanas·b); con v14.1 en el mundo con excepciones crece con `#estímulos` que la fuga no cubre (≈ 8·b + 4·5 +
hermanos re-aprendidos). Es la medida que manda desde el 05:10 ("exposiciones hasta asociar"), llevada de un patrón a un mundo.
Tres medidas de mecanismo la acompañan y son nuevas (v14.1 las tiene en 0 por definición o no las puede tener):
`tasa_tokeniza` (fracción de encuentros de variantes leídos por token o nodo), `n_slots` y `slot_ok` (nodos de excepción y su
signo contra el mundo), y `w_var` = |Wps − Wns| en los 3 píxeles de variable (la vía lenta limpia). Y una de coste: `colateral` =
mordidas de veneno en **hermanos** (variantes del mismo token y variantes de otros tokens con la misma variable) en los 10 000
pasos que siguen a la primera mordida de cada excepción — es el precio que B5 (§1) predice para la fuga.

**Vocabulario si pasa (y sólo entonces):** *"lee la variante por su token sin morderla; aprende una excepción en una mordida y la
olvida en una; cuando el token cambia, sus variantes cambian sin morderlas; las exposiciones crecen con los tokens y las
excepciones, no con los estímulos"*. **Prohibido:** "entiende", "lenguaje", "concepto", "planifica".

---

## 4. Preregistro (semillas nuevas: **2001–2020**; réplica automática **2021–2040** por regla 12; T = 100 000; peldaño 1)

**Brazos (un cambio por brazo):** `OFF` = v14.1 con el mundo (control base, cuerpo sin cambios) · `ON` = `token = 1` · `ON_SIN_SLOT`
(dosis: complección sin nodos de excepción: `umbral_exc = ∞`; **debe** perder en excepciones y empatar en lo demás) · mundos
`lineal`, `excepciones`, `azar`, `barajado` (§2.1). Total 9 brazos × 20 semillas. **Subconjunto estructural preregistrado (regla
10), calculado ANTES por `diagnostico_familias`:** por semilla, cada excepción se etiqueta SEPARABLE (comparte exactamente K−1
celdas con su token), ALIAS (código exacto = token) o HUÉRFANA; y cada semilla LIMPIA/ALIAS-TOKEN según haya dos tokens con
código idéntico. Se reporta siempre el conjunto completo y al lado las SEPARABLES; **el completo manda** salvo en P2, cuya letra
es sobre las separables (la arquitectura no puede separar un alias exacto con un nodo, §2.2).

Estadística (lecciones de ERR-37): lo aprendido (`exp_*`, signos, `slot_ok`) se parea por semilla; muertes, mordidas de veneno y
`colateral` son integrales de trayectoria → **A₁₂, razón de medianas y cuartiles**, nunca pareado ni `max`; ningún umbral en la
mediana esperada del propio efecto.

| # | predicción (mundo `excepciones` salvo indicación) | umbral | me refuta si… |
|---|---|---|---|
| **P1 techo** | `tasa_tokeniza` de ON, mediana en **[0.40, 0.75]**, y por cuartos **decreciente** (Q1 > Q4) como predice §1.1 (el código se afina al ganar celdas) | banda cerrada, escrita desde el cálculo estructural | > 0.80 → **fuga** (lee por token lo que no debe: revisar familias falsas) · < 0.40 → el código no tokeniza y v16 no puede actuar: la línea pasa al **código**, no al órgano |
| **P2 aprende en una** | mordidas tras el descubrimiento hasta signo correcto, por excepción SEPARABLE: ON mediana **≤ 1**, ≤ 2 en ≥ 16/20; OFF mediana **≥ 4**; pareado ON < OFF en ≥ 16/20 | 1 contra 4: el salto de la puerta por código (5) menos la mordida del descubrimiento | ON > 2 en > 4/20 → el nodo no toma (el token no estaba consolidado al escribir: `umbral_exc` mal derivado) · OFF ≤ 2 → la lenta ya lo hacía (fuga por píxel suficiente): v16 no compra nada |
| **P3 colateral** | `colateral` ON ≤ **0.5 ×** OFF (razón de medianas) y A₁₂(ON < OFF) ≥ 0.80; q75(ON) < q25(OFF) | B5: 0.6/px por mordida de excepción en OFF; ON no entrena la lenta con excepciones | ≥ 0.8 × → el colateral no venía de la vía lenta; buscar la causa antes de seguir |
| **P4 lenta limpia** | `w_var` (mediana de los 3 px de variable al final): ON **≤ 0.5**; OFF **≥ 1.0**; en `lineal` los dos ≤ 0.5 | A16 §5 (la lineal oscila sobre XOR) | OFF ≤ 0.5 en `excepciones` → la lenta no se corrompe con 4 excepciones (el mundo no aprieta: subir `n_exc` en un preregistro nuevo, no aquí) |
| **P5 nulo lineal** | en `lineal`: mordidas de veneno y muertes ON/OFF con razón de medianas en **[0.9, 1.1]** y A₁₂ en [0.35, 0.65]; `n_slots` mediana **≤ 1** | el mecanismo debe ser inerte donde la fuga basta | ON gana en `lineal` → la ganancia **no** es de las excepciones (efecto de la puerta o fuga): se dice y P2/P3 se leen con esa sospecha; ON pierde → reaparece el canje puerta/capacidad de v13 (ERR-22) y se mide |
| **P6 celdas** | `celdas` ON ≤ OFF − 6 (mediana pareada) en `excepciones`; |ON − OFF| ≤ 3 en `lineal` | 3 celdas + fisiones por excepción en OFF; 0 en ON | ON ≥ OFF → los nodos no ahorran celdas: las excepciones se estaban separando por fisión también en ON (alias exacto más frecuente que el 14 % estructural) |
| **P7 cambio de familia (el control que puede ganar)** | mordidas de veneno en las **variantes** de T0 en los 10 000 pasos tras T/2: A₁₂(ON < OFF) ≥ 0.65; la clave del token T0 **sobrevive** al cambio (≤ 2 fisiones en T0, clave intacta) en ≥ 15/20; la excepción de T0 **se borra en su 1.ª mordida** tras el cambio en ≥ 15/20 | la inversión pura no fisiona (B-5: `dist = 0`), pero `mu[c]` mezcla las variantes → puede fisionar | A₁₂ ∈ [0.35, 0.65] → el cambio se propaga por fuga en los dos: **el token no compra el cambio**, se declara; clave rota en > 5/20 → la fisión destruye la identidad del token y los miembros quedan huérfanos: coste real de la arquitectura CLS, se reporta |
| **P8 seguridad** | examen v3′ **8/8** ON (`bateria_v14` copiada por anclas, regla 14; 4a–4d pueden diferir de v14.1, deben pasar la letra); `bateria_generaliza` ON: G1 1.000 / G2 ≥ 0.95, **filas idénticas a v14.1** (identidad por construcción: 1.ª visita = v14.1); `azar`: veneno ON ≤ 1.1 × OFF; `barajado`: `n_slots` ≥ 0.8 × #variantes presentes **y** `exp_total` ON dentro de ±20 % de OFF | lo que protege al tronco y lo que delata al grafo degenerado | examen < 8/8 o G1/G2 no idénticos → no entra; `azar` > 1.1 × → las familias falsas cuestan más de lo que dan; `barajado` con `exp_total` ON < 0.8 × OFF → el grafo hecho tabla generaliza por otra vía: fuga, se busca |

**Controles resumidos:** apagado (`OFF`, el cuerpo v14.1 sin cambios, mismo mundo) · escalar/dosis (`ON_SIN_SLOT`) · azar (sin
familias) · barajado (familias falsas por construcción) · lineal (donde la fuga basta) · identidad (I1 OFF ≡ v14.1 24/24 con `D = 6`
y A/B; I2 ON inerte en A/B, rng no consumido a T = 120 000; I3 cadena ≡ `organismo_vivo` con `vivo = 1`; I4 el control que debe
fallar: ON en `excepciones` ≠ OFF). **Cláusula:** si P2 o P8 caen, v16 no entra; si cae P1 por abajo, la línea cambia de objeto (el
código); nada se recalibra; todo umbral tocado tras ver datos lleva ERR numerado (el siguiente libre lo asigna el coordinador; los
41–42 están tomados). Un veredicto a ±1 semilla dispara la réplica 2021–2040 con la misma letra.

**Predicción global, para poder equivocarme:** en `excepciones`, `exp_total` ON ≈ 0.55 × OFF [0.4, 0.75]; en `lineal` ≈ 1.0. Si ON
≈ OFF en los dos mundos, **el mundo no obligó**: la fuga por píxel cubre 4 excepciones sobre 3 variables, y el siguiente preregistro
sube `n_exc` a 8 (una por token) antes de tocar el órgano.

---

## 5. Coste e instrumentos (todo por anclas; los congelados sólo se leen; `manifiesto.py --check` 16/16 después)

| pieza | origen (sha) | cómo | coste |
|---|---|---|---|
| `construye_grande.py` → `organismo_grande.py` | `organismo/organismo_v14.py` feefc88b1fd8d434 | retina D (anclas de `construye_capD.py`), `pats/val/tipos` (anclas de `construye_vivo.py`), `mundo_familias` (rng propio 30000+seed), deriva y cambio sin sorteo, perilla `token` (A1–A7) | 1–2 h de implementador |
| `identidad_grande.py` | `organismo/identidad_rapido.py` como plantilla | I1–I4 de §4, un proceso, T = 20 000, semillas 1–3; **I2 a T = 120 000** para el rng | 3–5 min de un proceso |
| `diagnostico_familias.py` | `diagnostico_familias_sala2.py` (esta carpeta) | etiqueta SEPARABLE/ALIAS/HUÉRFANA y LIMPIA/ALIAS-TOKEN por semilla **antes** de correr; escribe el subconjunto | < 1 s |
| `bateria_v14_grande.py` | `organismo/bateria_v14.py` 72216f5415de0c86 | examina `organismo_grande_on` (`token = 1`, `D = 6`, A/B); **humo que ESCRIBA su JSON** antes de la serie (ERR-42); sha de v11/v10 leídos desde `organismo/` | 8 min de `Pool` |
| `bateria_generaliza_grande.py` | `organismo/bateria_generaliza.py` 9cf72581ebae7dea + `organismo_v14g.py` 1f1318480cd34cde → `organismo_grandeg.py` | **entrada comparada CAMPO A CAMPO con `'organismo_v14'`** (`eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1` + `token=1`), regla 14 / ERR-38; el gemelo g pone `eta_s=0.0, clip_s=3.0` por defecto | 3 min de `Pool` |
| `corre_grande.py` | `corre_vivo.py` / `corre_v15e.py` | subprocesos SECUENCIALES: identidad → serie 9 brazos → examen → generalización; `--humo` de un proceso (3 semillas, ON/OFF pareados, imprime `tasa_tokeniza`, slots y `w_var`); kwargs EXACTOS del tronco (ERR-41); log desde el arranque (regla 10) | serie: 180 corridas × ~7–9 s (retina 12, máquina cargada) ≈ 2–3 min con `Pool(14)`; réplica igual |
| gemelo numba | después, si entra como candidato | arnés bit a bit (regla 9 de EQUIPO) | no bloquea el bloque |

Total de `Pool` por serie ≈ 15 min; con réplica ≈ 30 min. **Nunca dos `Pool`** (hoy corre v15e). **Ningún archivo de esta carpeta
es instrumento del bloque**: el diagnóstico es un cálculo estructural; los instrumentos nacen en `experimentos/nivel12_mundo_grande/`
cuando el coordinador lo pida.

---

## 6. Humo y espejos: cómo podría engañarnos y cómo lo evito

1. **La fuga hace el trabajo.** La vía lenta ya implementa "variable de lo mismo" para variables no informativas (B5): por eso
   existe el mundo `lineal` (P5, predicho nulo) y el brazo `ON_SIN_SLOT`; una victoria de ON en `lineal` invalida la lectura de P2–P3.
2. **La identidad por construcción disfrazada de generalización.** G1/G2 salen idénticos porque la 1.ª visita se lee como v14.1: **no**
   es evidencia de que el token generalice; se dice así en el registro. Lo que el token compra se mide desde la 2.ª visita.
3. **El grafo que degenera en tabla.** Si cada variante acaba con su nodo (`n_slots` ≈ #variantes), v16 es M3 con otro índice y "aprende"
   por memorización: `barajado` lo fuerza a propósito y P8 exige verlo (`n_slots` ≥ 0.8 × y `exp_total` ≈ OFF). En `excepciones`,
   `n_slots` debe quedar en ≈ `n_exc` (+ familias falsas, ≤ 0.14 × #variantes): se reporta siempre.
4. **La política cuenta como aprendizaje.** El descubrimiento de una excepción depende del hambre (`hambre_boca = 2`), igual en los dos
   organismos: se cuentan **mordidas tras el descubrimiento**, no encuentros, y se reporta el paso del descubrimiento por brazo.
5. **El techo que se mueve.** El código se afina al crecer el pool (0.67 → 0.50): `tasa_tokeniza` se reporta por cuarto (P1); un valor
   plano o creciente sería sospechoso (¿celdas que no nacen?).
6. **El alias como mérito.** Una variante con el código exacto del token "sigue al token" gratis y una excepción con ese código no se
   puede separar con un nodo: la etiqueta ALIAS del subconjunto estructural separa los dos casos antes de ver datos.
7. **La semántica del cambio.** "La excepción conserva su valencia" está decidido y escrito; con la otra semántica P7 se leería al revés.
   No se cambia tras ver datos.
8. **Copias de baterías.** ERR-38/41/42 ya costaron tres veredictos: entrada campo a campo, kwargs del tronco, humo que escribe JSON.
9. **Muertes pareadas y umbrales en la mediana.** Prohibidos aquí (ERR-37a/b/c); A₁₂ y cuartiles para todo lo que sea trayectoria.
10. **Vender.** Si pasa todo, lo que se declara es lo de §3 y nada más; "lenguaje" no aparece en el vocabulario permitido: lo que se
    mide es que un patrón se lee por otro y que un nodo aparte guarda la excepción.

**Tres líneas honestas.** *Predigo:* P1 en banda (~0.6 en Q1, ~0.5 en Q4); P2, P3, P4, P6 pasan en `excepciones`; P5 nulo; **P7 es la
que más probablemente cae** (la fuga propaga el cambio en los dos, o la fisión rompe la clave de T0); P8 pasa por identidad salvo 4a–4d,
donde puede caer una etapa. *Me tumba* de verdad: P2 con OFF ≤ 2 (la lenta ya bastaba) o P1 < 0.40 (el código no tokeniza y el órgano
no tiene sobre qué actuar). *No pude:* correr ni el humo (regla 3 y un `Pool` vivo); medir la interacción con B-5 (`desambiguar`,
candidato v15): en el peldaño 2 las variantes de agua/sal dan `R = 0` a la fila del hambre y B-5 dividiría celdas compartidas con el
token → **B-5 y `token` pueden pelear por las mismas celdas**; se mide con las dos perillas cuando el director decida v15.
