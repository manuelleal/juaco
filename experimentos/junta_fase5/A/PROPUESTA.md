# PROPUESTA A — junta de la fase 5 (creador A: matemática del aprendizaje local)
**Candidato A1: la tabla lee DOS GANADORAS DE DISTINTO TIPO con una lectura conjuntiva.**
19-sep-2026. Instrumento `experimentos/junta_fase5/A/organismo_familias_a1.py` (derivado por anclas de
`organismo_familias_b6.py`, b10cbd4ddd0c32a3). Identidad: `identidad_familias_a1.py`. Humo: `corre_familias_a1.py`.

---

## 0. El diagnóstico matemático (escrito antes de tocar código)

Con **4 casillas por par**, una celda parte los 32 estímulos en ≤ 4 clases. Tres celdas de FORMA dan como mucho
4³ clases, pero su intersección **no puede bajar de la familia**: el token y sus 3 variantes caen siempre en la
misma clase porque los 9 píxeles de forma son idénticos. Eso es `piso_forma` = **4 de 32**, medido sin simular en
las tres semillas del humo (901, 902, 903) — y es exactamente el resultado del bloque 5 (BAR-T baja, BAR-H no).

Para bajar de 4 hace falta una partición que vea la variante. Hay dos maneras:

| | qué hace | resolución | densidad |
|---|---|---|---|
| **(i) sufijo (bloque 6)** | subdivide la dirección DENTRO de una celda: 4 → 32 subcasillas | sube | **÷ 8** |
| **(ii) dos tipos (A1)** | MULTIPLICA dos particiones densas: una celda de FORMA × una celda MIXTA | sube | **intacta** |

**Ésa es mi lectura del precio del bloque 6: no es un precio de referencia, es un precio de DENSIDAD.** Al
repartir la experiencia propia entre 8 veces más casillas, la celda conoce menos combinaciones, la vía lenta
abstiene más y releva a la lineal, que lee la familia por los píxeles de forma: eso sube la base sin mensaje
(CORTADO 0 → 4–6) y con ella BAR-T (5 → 10–11). La resolución que hacía falta **no exige vaciar ninguna casilla**.

## 1. El mecanismo (qué cambia en la tabla y en la lectura)

Cuatro perillas nuevas en la copia del instrumento; **todas inertes en su valor por defecto** (con ellas apagadas
el archivo es `organismo_familias_b6` bit a bit). La ESCRITURA no se toca: las 66 celdas siguen escribiendo R
crudo por sobrescritura en su dirección. El emisor, el canal, el mundo y la boca tampoco.

**(1) `dos_tipos=1` — dos ganadoras de distinto tipo, cada una con sus 4 casillas.** Las 66 celdas se parten por
su soporte: **FORMA** = 36 pares de dos píxeles de forma; **VARIANTE** = 27 pares **mixtos** (un píxel de forma +
uno de variante). Los 3 pares variante-variante quedan fuera de los dos tipos, declarado antes de medir: una
celda que sólo ve variante es ciega a la familia y su casilla guarda la última recompensa de cualquier token de
esa variante (casi siempre comida, porque el organismo muerde lo que come): no puede vetar nada.

**(2) elección por tipo, con COBERTURA (competencia entre ganadoras).** FORMA: las `k_forma`=3 de menor error
propio (el punto del bloque 5). VARIANTE: **la mejor mixta de cada píxel de variante** — una por píxel, 3 en
total. Es local, determinista y sin rng, y **garantiza** la separación: dos variantes distintas difieren en ≥ 1
píxel de variante, luego siempre hay una ganadora que las ve.

**(3) `combina='min'` — la lectura es CONJUNTIVA.** Cada tipo suma sus casillas conocidas (la lectura de b5,
restringida al tipo) y la boca lee **el mínimo de los dos**: *para morder tienen que estar de acuerdo los dos
tipos; para no morder basta uno que diga veneno*. Es la regla pesimista CUELLO_MIN ya declarada en el mundo vivo
(bloque 2 del peldaño 2), aplicada aquí a "familia Y variante". No hay puerta nueva ni umbral nuevo.

**(4) `exige_dir=1` — una casilla desconocida no es "no opino", es "no me consta".** Si alguna ganadora de
cualquiera de los dos tipos no conoce su casilla para el patrón presente, **la tabla calla y releva a la lineal**.
Esto lo añadí *después de medir* (ver §3): sin ello, la casilla que no se conoce desaparece de la suma y el
mensaje de la hermana se cuela por el tipo que no puede saber (la variante v2 nunca se ha visto, así que su
casilla está vacía justo donde tendría que vetar).

**(5) `msg_elige=0` — el mensaje escribe, pero no re-elige quién lee.** El mensaje sigue escribiéndose igual, pero
deja de actualizar el error propio de las celdas y de re-elegir la ganadora. **Un mensaje es una exposición SIN
consecuencia: no es evidencia sobre qué celda predice mejor las consecuencias.** Esta línea toca el bloque del
canal (con `msg_elige=1` es b6 carácter a carácter) y es la que más me gustaría que auditara el coordinador.

En código, el corazón son diez líneas:

```python
_FRM=[c for c in range(_NP) if max(_PARv[c])<_D-_NVA]                 # 36 celdas de FORMA
_VMX=[c for c in range(_NP) if min(_PARv[c])<_D-_NVA<=max(_PARv[c])]  # 27 celdas MIXTAS
def _topk_tipo():                                   # sin rng, desempate por indice
    _f=sorted(_FRM,key=lambda x:(float(_MEv[x]),x))[:k_forma]
    _v=[min([x for x in _VMX if q in _PARv[x]],key=lambda x:(float(_MEv[x]),x))
        for q in range(_D-_NVA,_D)]                 # UNA por pixel de variante: cobertura
    return _f,_v
def _tabla_dos(P):
    _f,_v=_topk_tipo(); _sf,_nf=_suma_tipo(_f,P); _sv,_nv=_suma_tipo(_v,P)
    if _EDv and (_nf<len(_f) or _nv<len(_v)): return (0.0,False)      # direccion completa -> si no, calla
    if not _nf and not _nv: return (0.0,False)
    if not _nf: return (_sv,True)
    if not _nv: return (_sf,True)
    if _CMv: return (min(_sf,_sv),True)             # CONJUNCION: familia Y variante
    return ((_wF*_sf+_wV*_sv)/(_wF+_wV),True)       # (promedio ponderado, con pesos aprendidos)
```

## 2. Por qué debería dar familia Y variante

* **Familia**: las 3 ganadoras de FORMA son las del bloque 5, con sus 4 casillas intactas y su misma elección por
  error propio → BAR-T debería quedarse donde el bloque 5 lo dejó (2–5 de 20), porque el otro token difiere del
  referente en **4 píxeles de forma** (medido, T = 0, en las 3 semillas).
* **Variante**: el referente y su hermana difieren **sólo en los píxeles 9 y 11** (medido, T = 0, en las 3
  semillas: los dos dentro del bloque de variante). Las ganadoras mixtas cubren 9, 10 y 11, así que al menos una
  ve la diferencia → la hermana no alcanza la dirección conjunta del referente.
* **Las dos a la vez**: la conjunción `min` es lo que impide que el tipo ciego (FORMA, que *no puede* distinguir a
  la hermana) decida solo. El grupo de estímulos que comparte TODAS las direcciones del mensaje baja a **1 de 32**
  en las tres semillas (b4b k=1: 16, 16, 4; b5 k=3: 4, 2, 2; b6 sufijo: 2, 1, 1) — y sin vaciar ninguna casilla.
* **El coste no debería ser el de k = 5**: se leen 6 celdas pero no se suman 6 valores (el mínimo entre tipos deja
  la escala en la de k = 3), y la abstención por dirección incompleta devuelve la decisión a la lineal del tronco.

## 3. Qué ERR podría repetir, y cómo lo evito (exoesqueleto, punto 1)

| ERR | riesgo en mi idea | cómo lo evito |
|---|---|---|
| **ERR-54** | el análisis del runner se para en una puerta y no hay números | los crudos se escriben ANTES del análisis; la tabla se calcula desde ellos |
| **ERR-64b / ERR-71** | arnés que pasa por vacuidad | 6 controles que DEBEN diferir, con ≥ 2 de 3 semillas; el caso de la dirección NO pasa por el emisor |
| **ERR-44 / T-E** | medir pesos en vez de conducta | todo se lee de `primera_b2` / `primera_b4` (lo que hizo la boca) |
| **ERR-31** | recopiar el mundo/la letra | el mundo, el canal, el emisor y las medidas son los OBJETOS de b6/b5/b4b, importados |
| **ERR-28** | usar un instrumento que no es el tronco | `organismo/` primero en `sys.path`; el constructor verifica 6 sha de origen y aborta |
| **ERR-38/41/42** | correr la copia en otra configuración que el original | identidad bit a bit en 8 escenarios × k × sufijo, y ancla larga T = 120 000 |
| **ERR-45** | prometer una propiedad estructural que no se cumple | la resolución se REPORTA (`canal_mismo_dos`), no se promete |
| **regla 3 / ERR-37** | recalibrar tras ver datos | cada cambio de la lectura fue por un diagnóstico escrito en la bitácora, con su ablación; nada de mover umbrales |
| **el precedente del bloque 6** | "la predicción acertó en la hermana y falló en el otro token" | **mido BAR-T siempre**, y la ablación A1-c dice qué regla lo sostiene |

**Riesgo que asumo y declaro:** `msg_elige=0` toca el bloque del canal (no lo que se escribe, sino si ese
escrito cuenta como evidencia para elegir lectora). Si el coordinador considera que eso rompe "el canal no se
toca", el candidato se corre con `msg_elige=1` (celda A1-e del humo, que en 3 semillas no se distingue de A1).

## 4. Humo (901–903, T = 30 000, UN proceso; **no es evidencia**, son 3 semillas)

`python experimentos/junta_fase5/A/corre_familias_a1.py --semillas 901,902,903 --T 30000 --celdas b4b,b5k3,b6suf,A1,A1-c,A1-d,A1-e`
(datos `humo_a1_20260919_172151.json`, crudo `..._crudo.json` d2116fedc1bef60e; identidad del humo 6/6)

`com` = mordió en la **primera exposición de la vida** al referente / n. dist = trató distinto a la hermana.

| celda | CANAL | CORTADO | BAR-H | BAR-T | VALOR | dist(PAR) | dist(PAR0) | muertes CANAL (901/902/903) | grupo del mensaje |
|---|---|---|---|---|---|---|---|---|---|
| b4b (k=1, b4b bit a bit) | 3/3 | 0/3 | 2/3 | 1/3 | 0/3 | 1/3 | 0/3 | 3 / 8 / 5 | 16, 16, 4 de 32 |
| b5k3 (bloque 5) | 3/3 | 0/3 | **3/3** | 2/3 | 0/3 | 3/3 | 1/3 | 7 / 296 / 393 | 4, 2, 2 |
| b6suf (bloque 6) | 3/3 | 0/3 | 0/3 | 2/3 | 0/3 | 3/3 | 0/3 | 9 / 11 / 36 | 2, 1, 1 |
| **A1 (candidato)** | **3/3** | **0/3** | **1/3** | **1/3** | 1/3 | 2/3 | 0/3 | 10 / 258 / 20 | **1, 1, 1** |
| A1-c (sin conjunción) | 3/3 | 0/3 | 2/3 | 2/3 | 0/3 | 1/3 | 0/3 | 11 / 29 / 30 | 2, 1, 1 |
| A1-d (sin dirección completa) | 3/3 | 0/3 | 1/3 | 2/3 | 1/3 | 3/3 | 0/3 | 16 / 393 / 87 | 5, 1, 2 |
| A1-e (el mensaje sí re-elige) | 3/3 | 0/3 | 1/3 | 0/3 | 1/3 | 2/3 | 0/3 | 8 / 262 / 20 | 1, 1, 2 |

**Lectura honesta.** (1) A1 es la única celda que baja BAR-H y BAR-T **a la vez** con CANAL 3/3 y CORTADO 0/3;
pero con 3 semillas eso no distingue nada y A1-e hace lo mismo. (2) Los tres fallos de A1 (BAR-H, BAR-T y VALOR,
una semilla cada uno) son **la misma semilla 902**, un mundo hambriento (258–393 muertes en todas las celdas de
la línea k = 3), y **en todos ellos el valor leído era negativo** (−1.0): la tabla no refirió mal, es que −1.0 no
frena a una boca hambrienta (hace falta ≲ −2.1 con `hambre` = 1). (3) El coste del cuerpo es el riesgo real: A1
muere 20/258/20 frente a 3/8/5 de b4b; contra el brazo de su propia línea (b5k3, 7/296/393) **A1 muere menos en
2 de 3 semillas**, pero R6 se mide contra `CANAL-k1v0` y ahí el margen ×1.5 no está garantizado (§6, pregunta 3).
(4) `dist(PAR)` 2/3 con `dist(PAR0)` 0/3: la especificidad entre hermanas está, pero no mejor que b6suf.

## 4bis. Identidad (la nave, antes de medir nada)

`python experimentos/junta_fase5/A/identidad_familias_a1.py` → **77/77** (salida guardada en
`identidad_a1_salida.txt`): apagado ≡ `organismo_familias_b6` **bit a bit** en 8 escenarios × k ∈ {1,3} ×
sufijo ∈ {0,1}, con el canal en sus tres modos, con ancla larga T = 120 000 (el rng no se consume de más), y por
la cadena ≡ b5, b4b, `organismo_familias`, **`organismo_v14` (TRONCO)** y `organismo_v15f_on`. Inercia sin tabla
y sin `dos_tipos`; la partición (36 + 27 + 3 fuera) y la dirección conjunta reimplementadas FUERA del organismo y
comparadas; 13 perillas mal escritas que LANZAN; y **6 controles que DEBEN diferir** (ERR-64b).

## 5. Predicción numérica para 821–860 (dos series de 20; escrita ANTES de correrlas)

Con la celda A1 (`dos_tipos=1, k_forma=3, var_cubre=1, combina='min', exige_dir=1, msg_elige=0`):

| medida | predicción A1 | refuta el mecanismo si |
|---|---|---|
| CANAL (come a la 1.ª lo que evitaba) | **16–19 / 20** en las dos series | < 15 en cualquiera |
| CORTADO (gemelo mudo) | **0–3 / 20** | > 5 |
| **BAR-T (otro token)** | **2–5 / 20** | > 5 en cualquiera de las dos |
| **BAR-H (hermana)** | **3–7 / 20** | > 8 (sería el bloque 5 otra vez) |
| VALOR (sin referencia) | 2–5 / 20 | > 5 |
| **PAR `dist`** | **13–17 / 20** (gemelo PAR0 ≤ 4) | < 12, o `dist(PAR) < dist(PAR0) + 5` |
| muertes(CANAL-A1) / muertes(CANAL-k1v0) | 1.5–4× (mediana) | — (es el punto débil, no el criterio de referencia) |
| `canal_mismo_dos` (resolución) | **1–3 de 32** en ≥ 18/20 semillas | > 4 (entonces la partición no multiplica) |

**LO QUE PIDE EL COORDINADOR, las dos a la vez y con los márgenes del bloque 6, para la celda A1:**

* **BAR-T (R2 del bloque 6: BAR-T ≤ CORTADO + 3)**: predigo **2–5 de 20** con CORTADO **0–3**, es decir **R2 PASA
  en las dos series** (y también el umbral absoluto de la MISIÓN, BAR-T ≤ 5). Refuta: BAR-T > CORTADO + 3, o > 5.
* **PAR (R5: `dist` ≥ 12/20 **y** `dist(PAR)` ≥ `dist(PAR0)` + 5)**: predigo **`dist` 13–17 de 20** con
  `dist(PAR0)` **≤ 4**, es decir **R5 PASA** por la letra del bloque 6; pero **sólo doy 50 % a que llegue al
  umbral de la MISIÓN (≥ 15)**. Refuta: `dist` < 12 o `dist` < `dist(PAR0)` + 5.
* **Las dos a la vez (el objetivo de la junta)**: predigo **R2 y R5 pasan juntos en las dos series** — eso sería
  lo que ningún bloque ha conseguido — y le doy **~50 %** a que además `dist` ≥ 15 en las dos, que es el listón
  estricto de la MISIÓN. **El que se queda en el borde es PAR, no BAR-T.**
* **BAR-H (R3: ≤ CORTADO + 5)**: 3–7 de 20, pasa; **CANAL (R1)**: 16–19 con pareado ≥ 14, pasa.
* **Donde espero caer es R6 (coste del cuerpo)**, no la referencia: ver §6, pregunta 3.

## 5bis. EL COMANDO DE LA CONFIRMACIÓN (lo corre el coordinador)

```bash
cd <bundle>
# Pool configurable por variable de entorno (por defecto 6) o por --pool. BrokenPipe del 17:19: usar 5-6.
JUACO_POOL=6 python -u experimentos/junta_fase5/A/corre_familias_a1.py --serie --desde 821         --celdas b5k3,b6suf,A1,A1-e
JUACO_POOL=6 python -u experimentos/junta_fase5/A/corre_familias_a1.py --serie --desde 841         --celdas b5k3,b6suf,A1,A1-e
```

* **Tiempo estimado por serie: 12–16 min de pared con Pool(6)** (580 corridas de T = 100 000: 20 emisores +
  4 celdas × 7 brazos × 20 semillas, ~7.3 s por corrida medidos en el humo). Con `--celdas b5k3,A1` baja a
  **6–8 min** (300 corridas) si hay prisa; las celdas `b6suf` y `A1-e` son los dos controles que más me importan.
* `--pool N` manda sobre `JUACO_POOL`; `--desde` fija la semilla inicial y `--n` el número de semillas (20).
* Escribe `A/serie_a1_s821-840_*_crudo.json` **antes** de cualquier análisis (ERR-54) y luego la tabla con R1–R5
  y la línea `MISION (BAR-T <= 5 Y PAR >= 15)` por celda. El log va a `A/serie_a1_*.log` desde el arranque
  (regla 10), con una línea de progreso cada 40 corridas.
* Comprobado el *plumbing* del Pool (spawn, tareas picklables, crudo y tabla) con un ensayo corto
  `--serie --desde 901 --n 2 --T 6000 --celdas A1 --pool 2`; **yo no he corrido ninguna serie** (reglas 3 y 11).

## 6. Preguntas al coordinador (exoesqueleto, punto 3: no adivino el criterio)

1. **¿`msg_elige=0` viola "el canal no se toca"?** El mensaje se escribe exactamente igual; lo que quito es que
   ese escrito cuente como error propio y re-elija la lectora. **Lo medí y es una fuga real del bloque 4/4b/5/6:**
   tras un mensaje de +1, la elección se va a las celdas que dicen +1 en todas partes, y por ahí entra la hermana.
   Si esto se considera parte del canal, ¿se corre A1 con `msg_elige=1` (celda A1-e), o se abre un bloque aparte
   para medir la fuga en el propio bloque 5 (celda `b5k3e`, que ya está implementada)?
2. **¿Qué manda cuando la tabla calla?** Con `exige_dir` la tabla abstiene y releva a la lineal; en un mundo
   hambriento la lineal (−1.0) no frena la mordida. ¿Es legítimo que el relevo sea "no sé → la lineal", o el
   criterio de la fase 5 exige que "no sé" sea "no muerdo"? Es una decisión de método, no de parámetro.
3. **R6 con qué referencia.** La puerta está escrita contra `CANAL-k1v0` (b4b). Toda la línea k = 3 (incluido el
   bloque 5, que sí se declaró) muere mucho más que k = 1 en las semillas hambrientas. ¿R6 se mide contra k1v0 o
   contra el brazo de la misma familia (k3v0)? Con 3 semillas mi candidato pasa contra k3v0 y no contra k1v0.
4. **¿Cuántas semillas del humo puedo gastar?** Las 3 que usé (901–903) incluyen dos mundos con 250–400 muertes;
   si el coordinador quiere un humo menos sesgado, pido autorización para 904–906 antes de la confirmatoria.
5. **Occam**: `pesos_tipo` (pesos de tipo aprendidos por consecuencia) y `dentro='min'` quedaron **medidos
   inertes** bajo la lectura pesimista y NO entran en el candidato. ¿Se reportan igual en el registro (yo creo
   que sí: son dos predicciones mías que el instrumento refutó) o se borran?

## 7. Reproducir

```bash
cd <bundle>
python experimentos/junta_fase5/A/construye_familias_a1.py     # anclas sobre b6 (verifica 6 sha de origen)
python experimentos/junta_fase5/A/identidad_familias_a1.py     # arnes completo (~16 min, un proceso)
python experimentos/junta_fase5/A/corre_familias_a1.py --semillas 901,902,903 --T 30000 \
       --celdas b4b,b5k3,b6suf,A1,A1-c,A1-d,A1-e                # el humo de esta propuesta (~5 min)
```
Ficheros: `construye_familias_a1.py` · `organismo_familias_a1.py` · `identidad_familias_a1.py` ·
`corre_familias_a1.py` · `humo_a1_20260919_172151.json` (+ `_crudo.json`, `.log`) · `identidad_a1_salida.txt`.
