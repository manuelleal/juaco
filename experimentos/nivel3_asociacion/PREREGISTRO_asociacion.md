# PREREGISTRO — asociación en una exposición, en el MUNDO DE REGLA: `px0` (el parecido predice el valor) contra `azar` (no)

**Escrito ANTES de correr, 18 sep 2026.** Convierte en bloque preregistrado la propuesta **B-4** del creador B
(`registro/investigacion/PUENTE_creacion.md`, "Propuestas para el coordinador"; misma propuesta en
`registro/REGISTRO_etapas_1_2.md`, entrada `Frente "dos organismos", creador B (18 sep 06:00)`). La identidad del
instrumento (§9) y el humo (§12, 2 semillas, un proceso, T corto) ya están corridos; la serie de 20 semillas
**no** — la corre el coordinador con `Pool(14)` (regla 3 de `EQUIPO.md`: el implementador no corre Pool).

## 1. De dónde sale

B-4 midió, en el **mundo del tronco** (AB, 4 patrones), que el órgano de asociación (ligar el código nuevo al más
parecido y heredar su valor; desligar con una mordida si la primera evidencia propia lo contradice) **no** baja
`exp_hasta` — lo sube (8 → 11/13 en el escenario de parecido engañoso) — porque en ese mundo **el único par de
patrones bastante parecido para heredar es un par comida/veneno**: el parecido contradice el valor. El diagnóstico
de B-4 (200 sorteos, sin correr el organismo) mide que la representación de alta dimensión (`nh=2000, kh=40`) **sí**
ordena vecinos por parecido de forma graduada donde el código del tronco (Kenyon, `K=3` de `NKMAX=90`) no distingue
nada — así que el fracaso en el mundo AB no es un problema de representación, es que **ese mundo no tiene la
estructura que el órgano necesita**. La pregunta que B-4 pide preregistrar es barata y trae su propio control
incorporado: medir `exp_hasta` en el **mundo de regla** (`organismo_v14g`), con la regla `px0` (la valencia depende
sólo del píxel 0 ⇒ dos patrones que comparten píxeles activos tienden a compartir valencia: **el parecido SÍ
predice el valor**) contra la regla `azar` (valencia asignada al azar por patrón, sin relación con el parecido:
**el parecido NO predice nada**). Si el contraste `px0` vs `azar` no aparece, el propio B-4 ya escribió el
veredicto: *"heredar por parecido no acelera la asociación; lo que falta no es la ligadura sino una relación que
prediga el valor"* — y aquí queda medido en el mundo donde, por construcción, esa relación sí existe.

## 2. Hipótesis

**HB4-regla.** En el mundo de regla con `px0`, al menos uno de los mecanismos de asociación por parecido reduce
`exp_hasta` de forma sustancial frente a v14 sin el órgano, PORQUE ahí el parecido de píxeles predice la valencia;
en `azar`, donde por construcción no la predice, el mismo mecanismo no reduce `exp_hasta` — y heredar un valor
equivocado cuesta.

## 3. Instrumento (por anclas; el original sólo se lee)

| archivo | qué es | origen (sólo lectura) | sha origen | sha generado |
|---|---|---|---|---|
| `construye_v14gL.py` | constructor por anclas (5 anclas, 2 adaptadas — ver su cabecera) | — | — | — |
| `organismo_v14gL.py` | `organismo_v14g` + perilla `sem` + medida `exp_hasta` | `organismo/organismo_v14g.py` **(CONGELADO)** | `1f1318480cd34cde` | `1d3bca2d54b7a064` |

`organismo_v14gL.py` aplica al **mundo de regla** las MISMAS cinco anclas que
`experimentos/creacion_B/construye_B4.py` aplicó a `organismo/organismo_v14.py` para producir
`experimentos/creacion_B/organismo_v14L.py` (`d6d550aec83f775a`). Tres anclas son bit a bit idénticas. Dos se
adaptaron porque el mundo de regla difiere del mundo AB, declaradas en la cabecera de `construye_v14gL.py`:

1. **Firma:** el último default de `organismo_v14g.py` es `pat_min=0` (perillas del tronco apagadas por defecto —
   `organismo_v14g` es `organismo_v13g` con ropa de v14; `bateria_generaliza.py` las enciende con kwargs
   explícitos), no `pat_min=1` como en `organismo_v14.py`. El ancla se adapta a ese texto; los kwargs nuevos
   (`sem=0,nh=2000,kh=40,theta_sim=0.15,sem_min=0.3,tol_sem=0.5`) son exactamente los mismos, con el mismo default.
2. **Ligar/desligar:** el texto de `construye_B4.py` usa `PAT[kk]` (el diccionario GLOBAL de 4 patrones A/B/C/D).
   `organismo_v14g.py` no usa `PAT` dentro de `run()`: usa la variable local `P_` (= `PAT` si `mundo=='AB'`; el
   diccionario de los 20 patrones de `patrones_regla()` si no). Las 5 ocurrencias de `PAT[kk]` se cambiaron a
   `P_[kk]`; con `mundo='AB'` el cambio es transparente (`P_ is PAT`). Sin este cambio, cualquier patrón de la
   regla (claves como `'110100'`) levanta `KeyError` en la primera mordida con `sem≠0` — se comprobó a mano
   (`sem=1,2,4` corridos en T=200000 antes de escribir este preregistro: no revientan y `exp_hasta` se puebla).

**El órgano (perilla `sem`; los valores son los que define `organismo_v14L` — el mini-prueba de B-4 usó los mismos
números, ver la tabla de `PUENTE_creacion.md` §"Propuestas para el coordinador"):**

- `sem=0` — apagado (v14 exacto).
- `sem=1` — **vía lenta**: `v0 = (Wps−Wns)@P` (memoria nueva: **cero**; es el control barato, lee el órgano que v13
  ya tiene).
- `sem=2` — **HD (Kanerva)**: expansión aparte `HW` (`nh=2000 × 6`), código disperso top-`kh=40`; `v0` = valor del
  ítem más parecido ya visto si `similitud ≥ theta_sim=0.15`, si no `0`.
- `sem=4` — **grafo con fiabilidad por tipo de arista** (parecido + co-ocurrencia, EMA 0.3 por tipo; la arista que
  engaña pierde confianza y deja de recorrerse).
- `sem=3` (**no es un brazo de esta serie**) existe en el código —se portó igual que el resto del órgano, por
  fidelidad a B-4— pero es el "control barajado" (prior al azar) que B-4 usó como control **dentro del mundo del
  tronco**; aquí el contraste `px0`/`azar` del mundo de regla hace ese papel de forma más directa (B-4, último
  párrafo), así que no se corre como brazo.

RNG del órgano aparte (`seed+400000` para el canal HD, `seed+500000` para el control barajado que no se usa aquí):
no tocan el flujo de azar del organismo.

**Perillas del tronco:** **ENCENDIDAS** en toda esta serie (medida principal y controles), con los kwargs de
`organismo/bateria_generaliza.py` → `INSTRUMENTOS['organismo_v14']`: `eta_s=0.015, puerta=3, mask_rel=2,
del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1`. La pregunta es si el órgano ayuda **al
tronco v14 tal como está**, no a una versión reducida (`organismo_v13g`-equivalente) de él.

## 4. Diseño

- **Brazos:** `v14` (`sem=0`), `via_lenta` (`sem=1`), `HD` (`sem=2`), `grafo` (`sem=4`).
- **Mundos:** `px0` (el parecido predice el valor) y `azar` (no), con `mundo='regla'`.
- **Semillas:** 101–120 (20) — las del examen de congelación de v14, para poder cruzar los números con
  `bateria_generaliza.py`.
- **T = 200 000** (el de `bateria_generaliza.py`), `fase2_en = T/2 = 100 000` (default: los patrones de **test**
  —los que el parecido nunca vio antes— entran ahí).
- **4 brazos × 2 mundos × 20 semillas = 160 corridas.**

## 5. Medida principal: `exp_hasta` — EXPOSICIONES HASTA ASOCIAR

`exp_hasta[patrón]` (del instrumento, solo lectura): número de MORDIDAS de ese patrón tras las cuales el valor que
usa la boca cae a `≤ tol_sem=0.5` del valor real del mundo, por primera vez.

**Se mide sobre los patrones de TEST** (`r['test']`, los 10 que `split_regla` deja fuera del entrenamiento y que
`organismo_v14g` inyecta en `fase2_en=T/2`): son, por construcción, códigos **nuevos** en el momento en que el
organismo ya aprendió algo de los patrones de entrenamiento — exactamente la situación de "un código nuevo con
estructura previa para asociar" que B-4 propone medir. (Los patrones de entrenamiento no sirven para esto: los
primeros que se muerden no tienen nada previo de qué heredar.)

**Operacionalización exacta (declarada aquí, no después de ver datos):**

- **`exp_hasta` por semilla** = mediana de `exp_hasta[k]` sobre los patrones de test `k` que SÍ asociaron en esa
  semilla (`exp_hasta[k] is not None`). Un patrón de test que nunca cae dentro de `tol_sem` en toda la corrida
  queda **censurado** (excluido de esa mediana) — se reporta aparte, como el "no asocia en 2/3" del mini-prueba de
  B-4.
- Una **semilla totalmente censurada** (ningún patrón de test asoció) no aporta valor a `exp_hasta` por semilla:
  se excluye de la mediana por brazo/mundo y del pareo (ver abajo), y se cuenta aparte.
- **`exp_hasta` por brazo y mundo** = mediana de las (hasta 20) medianas por semilla.
- **Pareo semilla a semilla** ("el brazo le gana a v14"): en la MISMA semilla, `exp_hasta_semilla(brazo) <
  exp_hasta_semilla(v14)` (menos exposiciones = asocia más rápido). Si cualquiera de los dos está censurado en esa
  semilla, esa semilla **no** cuenta como victoria del brazo.

## 6. Predicción numérica (antes de correr)

- **En `px0`:** al menos un brazo con parecido (`via_lenta`, `HD` o `grafo`) tiene `exp_hasta` por brazo/mundo
  **≤ 0.70 × exp_hasta de `v14`** (baja ≥ 30 %), **y** le gana a `v14` en el pareo semilla a semilla en
  **≥ 14/20**.
- **En `azar`:** **ningún** brazo con parecido baja `exp_hasta` por brazo/mundo más de un 10 %
  (`exp_hasta(brazo) ≥ 0.90 × exp_hasta(v14)`), **y** el engaño cuesta: `exp_hasta(brazo) ≥ exp_hasta(v14)` a nivel
  de mediana por brazo/mundo, para los tres brazos.

## 7. Controles (de `bateria_generaliza.py`; fórmula sin tocar, **umbrales de ESTE preregistro — ERR-31**)

`ERR-31` (`registro/REGISTRO_etapas_1_2.md`, 18 sep 02:50) ya documentó el error de fondo: un runner que decide con
los umbrales por defecto de `bateria_generaliza.py` (`G1≥0.65`, `G2≥0.55` — los de la Etapa 3 sobre v9, "NO se
tocan" ahí) en vez de con los del preregistro del candidato que se está probando. Aquí, igual que
`PREREGISTRO_v13E.md` §6 hizo para dE-TEST sobre el tronco, los umbrales de control son los de **este documento**:

- **G1 (valor, fórmula de `bateria_generaliza.py`: 0.5·acierto-comida + 0.5·acierto-veneno sobre los patrones de
  test, leídos en `W_apriori` a `t=fase2_en`, ANTES de que ningún patrón de test se muerda — el órgano de
  asociación todavía no actuó sobre ellos).** Con perilla del tronco **ON**, `sem=0` (`v14`), mundo `px0`: mediana
  en 20 semillas **≥ 0.80**.
- **G2 (conducta, fórmula de `bateria_generaliza.py`: `pb`/`1−pb` en el PRIMER encuentro de cada patrón de test).**
  Con perilla del tronco **ON**, mundo `px0`: mediana en 20 semillas **≥ 0.85**, para **cada uno** de los tres
  brazos con parecido (`via_lenta`, `HD`, `grafo`) — el brazo no debe dañar la generalización que v14 ya tiene.

Los dos controles se calculan de las MISMAS 160 corridas de §4 (`W_apriori` y `primer` ya vienen en la salida del
instrumento): no hacen falta corridas extra.

**Las cuatro trampas de la noche del 17-sep (regla 5 de `EQUIPO.md`), revisadas:** canal social simétrico — no
aplica (no hay comunicación entre organismos aquí); acierto sin balancear — G1/G2 ya ponderan 0.5/0.5
comida/veneno, heredado de `bateria_generaliza.py` sin tocar; mundo que se come la comida (muestreo asimétrico) —
los 4 objetos activos se reparten al azar entre los tipos vigentes en cada `spawn()`, sin cambio de este bloque;
sitios fijos que se memorizan — las posiciones se sortean en cada aparición (`rng.integers(L)`), no hay sitio fijo
que el "ciego" (aquí, el patrón de test antes de `fase2_en`) pueda saber de antemano.

## 8. Cláusula de refutación (escrita antes)

- **Si en `px0` NINGÚN brazo baja `exp_hasta` ≥ 30 % (con el pareo ≥ 14/20), la asociación por parecido queda
  REFUTADA EN LOS DOS MUNDOS.** No se prueba el control de `azar` como si pudiera salvar el resultado, no se
  recalibra ningún umbral, no se corren semillas nuevas para buscarlo. Lo declarable es exactamente lo que B-4 ya
  escribió: *"heredar por parecido no acelera la asociación; lo que falta no es la ligadura sino una relación que
  prediga el valor"* — medido también aquí, donde esa relación sí existe por construcción.
- **Si algún brazo baja ≥ 30 % en `px0` pero el mismo brazo TAMBIÉN baja > 10 % en `azar` (o no cumple
  `exp_hasta(brazo) ≥ exp_hasta(v14)` ahí):** el hallazgo se declara como *"el brazo asocia más rápido en
  general, no específicamente donde el parecido predice el valor"* — **no** confirma HB4-regla (que exige el
  contraste `px0` vs `azar`, no sólo la caída en `px0`).
- **Si G1 < 0.80 o G2 < 0.85 (en cualquiera de los tres brazos) en `px0`:** el brazo que pase `exp_hasta` queda
  con **coste medido** sobre la generalización del tronco y **no se propone tal cual** — mismo patrón que
  `PREREGISTRO_v13E.md` §7 ("se queda como órgano de experimento... nada se recalibra").
- Nada de esto se decide después de ver los números: los tres desenlaces están escritos aquí, antes de correr.

## 9. Identidad (obligatoria; corrida por el implementador antes de este documento)

`identidad_v14gL.py` — `sem=0` ≡ `organismo_v14g` (`1f1318480cd34cde`) en **todas las claves comunes** (las 8
nuevas —`sem, exp_hasta, n_mord, n_sem, n_des, sem_log, rel_arista, n_nodos`— son añadido, no cambio):

- **Bloque A** (perillas del tronco en su propio default, apagadas): `px0`/`xor01`/`azar` × 3 semillas = 9 casos.
- **Bloque B** (perillas del tronco ENCENDIDAS, los kwargs de §3): `px0`/`xor01`/`azar` × 1 semilla = 3 casos.

**Resultado: IDENTIDAD 12/12 (92.6 s)** — A 9/9, B 3/3. `corre_asociacion.py` repite una identidad interna más
ligera (3 casos: los tres mundos a una semilla, T corto) como puerta de arranque de cada corrida (aborta si no es
3/3): no reemplaza este arnés, lo reconfirma con el binario exacto que se va a usar.

## 10. Coste

160 corridas de T=200 000 (medida principal, incluye los controles) + 3 de identidad interna. Un proceso, T=200 000:
≈ 17 s medido (`organismo_v14g`, semilla 101, `px0`, perillas ON). Con `Pool(14)`: ≈ 160/14 ≈ 12 tandas × ~17 s ≈
**3–4 minutos**. La identidad completa (§9, 12 pares a T=40 000, un proceso) ya está corrida: 92.6 s, aparte.

## 11. Qué se declara si pasa / si no

Si HB4-regla se sostiene con los tres desenlaces de §8 en su forma favorable: *"al menos un mecanismo de
asociación por parecido —[el que corresponda]— reduce las exposiciones hasta asociar en el mundo donde el
parecido predice el valor, y no en el mundo donde no lo predice, sin dañar la generalización del tronco"* — y
**sólo entonces** tiene sentido preguntar si migrar el mecanismo (con su propio coste de memoria declarado en
`PUENTE_creacion.md` §B-4) al mundo del tronco con una relación que sí prediga el valor, o proponerlo para un
mundo con esa estructura. Si se refuta (§8, primer desenlace): la línea de "asociación en una exposición por
parecido" queda cerrada en los dos mundos probados hasta ahora (AB y regla), con la misma medida y quien la
propuso puede seguir el vocabulario permitido que B-4 ya fijó: **no** "aprende en una exposición", **no**
"reconoce", **no** "razona por analogía".

## 12. Humo ya corrido (2 semillas, un proceso, sin Pool, T = 20 000)

`python experimentos/nivel3_asociacion/corre_asociacion.py --humo` →
`datos/asociacion_humo_20260918_054317.{log,json}` (log `602378174fd2b04a`, json `24331fc730489909`, 46.1 s).
Identidad interna (3 mundos, semilla 101, perillas ON) **3/3**.

| mundo | brazo | exp_hasta (mediana 2 semillas) | asociaron | acc | ba |
|---|---|---|---|---|---|
| px0  | v14       | 3.2 | 2/2 | 0.750 | 0.771 |
| px0  | via_lenta | 2.5 | 2/2 | 0.800 | 0.784 |
| px0  | HD        | 2.2 | 2/2 | 0.750 | 0.844 |
| px0  | grafo     | 2.0 | 2/2 | 0.700 | 0.833 |
| azar | v14       | 4.0 | 2/2 | 0.600 | 0.597 |
| azar | via_lenta | 4.0 | 1/2 (1 censurada) | 0.650 | 0.651 |
| azar | HD        | 2.2 | 2/2 | 0.550 | 0.683 |
| azar | grafo     | 1.0 | 2/2 | 0.650 | 0.638 |

Con 2 semillas **ningún** criterio de §6-8 vale como evidencia (se preregistraron 20) — esto sólo confirma que el
montaje corre de punta a punta: la identidad interna pasa, las 16 corridas (4 brazos × 2 mundos × 2 semillas)
terminan, `exp_hasta` se puebla (con censura donde se espera, p. ej. `via_lenta`/azar/semilla 101: 0/10 patrones de
test asociaron), G1/G2 se calculan de la misma corrida, y el JSON/log quedan escritos con `fsync`. El propio humo
ya deja ver, sin que cuente, la forma del contraste que preregistra §6: en `px0` los tres brazos con parecido
bajan `exp_hasta` frente a `v14`; en `azar`, `HD` y `grafo` también bajan en estas 2 semillas — exactamente el tipo
de resultado que §8 (segundo desenlace) trata como "no confirma HB4-regla" si se repite en la serie real, y que
sólo la serie de 20 semillas puede decidir.
