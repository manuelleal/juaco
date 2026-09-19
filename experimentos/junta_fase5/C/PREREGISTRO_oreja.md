# PREREGISTRO — **LA OREJA**: que la puerta de familiaridad consulte la vía lenta cuando la casilla que tocaría leer **acaba de nacer**

**MISIÓN (primero, siempre): llegar a la AGI por este camino** — un organismo mínimo con reglas locales, sin
retropropagación ni supervisor global, que aprende, desaprende, generaliza, sobrevive y **se comunica con
referencia**. Aquí, exactamente: que un organismo que ya aprendió bien el mundo **no deje de escuchar**.

**Fecha:** 2026-09-19. **Creador:** C (junta de la fase 5). **Estado: ESCRITO Y NO CORRIDO.**
**Orden del coordinador (19-sep, §2 de su mensaje): "la oreja" entra como candidato APARTE, con preregistro
propio, y NO se corre hasta que C1 (`variante_hija`) esté confirmada en 821–840 y 841–860.** Este documento se
escribe ahora precisamente para que no pueda ajustarse después de ver los datos de C1. Los §0–§7 no se editan
una vez corrida su primera serie; lo que cambie va en ERR numerado con fecha, motivo y semillas nuevas.

---

## 0. El error que ataca, con su evidencia

**E-9 — la puerta de familiaridad es una oreja que se cierra con la competencia.**

La boca del tronco (v14.1) consulta la vía rápida si el patrón le resulta **familiar**, y familiar significa
`puerta_pat`: *el código exacto de Kenyon se mordió ≥ 5 veces y tiene ≥ 1 celda consolidada*. Esa puerta mide
**evidencia del código**, no acierto: no puede distinguir "conozco esto" de "creo que conozco esto y me
equivoco". Un mensaje es exactamente el caso en que la vía rápida está **segura y equivocada**.

Evidencia medida en el humo de C1 (`c1_humo_s901-903_20260919_162332_crudo.json`, y el diagnóstico de la
bitácora, prefijo `[C]`):

| hecho | medida |
|---|---|
| en 2 de 3 semillas de humo la boca leyó la vía **RÁPIDA** en la primera exposición al referente (P-I5 cayó) | `fam1 = 1` en s901 y s902, `0` en s903 |
| y entonces **todos** los brazos dan 0: CANAL 1/3, CORTADO 0, BAR-H 0, BAR-T 1 | el mensaje queda escrito y **no consultado** |
| la cadena causal, rastreada en las mismas semillas | tabla mejor → la boca se contradice menos → **menos divisiones de Kenyon** (49 celdas contra 65) → el código deja de cambiar y acumula evidencia → `puerta_pat` lo declara familiar |
| no es una propiedad demostrada del mecanismo | en las semillas del arnés (1, 2) la vía lenta aguanta **2/2** en las tres celdas |

**Por qué esto es un cuello de la misión y no una molestia del montaje:** si cada mejora de la vía lenta cierra
la oreja, entonces **competencia y comunicabilidad se excluyen** en este organismo. Un adulto que ya sabe no
puede recibir un aviso sobre lo que cree saber. Eso bloquea la fase 5 entera, no sólo a C1.

## 1. La pregunta

**¿Basta con que la puerta pregunte también a la tabla — "la casilla que te tocaría leer, ¿acaba de nacer?" —
para que el receptor vuelva a consultar la vía lenta justo donde su regla de familia acaba de fallar, sin que
eso lo vuelva sugestionable (base sin mensaje) ni le cueste el cuerpo?**

## 2. Lo que NO cambia

Se importan, no se recopian (ERR-31): el mundo, el canal, el **emisor** (`B6R.emisor`, b4b bit a bit), la
lectura de la boca (`B4BR.lee_b4`), los nueve brazos y la letra. Dentro del organismo **no** se tocan: la
selección de la ganadora `_MGv`, el error propio `_MEv`, la sobrescritura de R CRUDO, la vía lineal, la boca, el
metabolismo, el consumo del rng, **ni `puerta_pat` ni `pat_min` ni ninguna constante del tronco**. `variante_hija`
queda **exactamente** como se confirmó en C1 (`vh_ev = 2`, `vh_umbral = 0.2`).

## 3. Lo que cambia — una perilla, inerte por defecto

### 3.1 `oreja` (default 0), en `organismo_familias_c2.py` (copia derivada de `organismo_familias_c1.py`)

Cada casilla guarda **el paso en que nació** (`_TNh[g, b]`, −1 si nunca se dividió; se escribe en la misma línea
en que hoy se pone `_FIh[g,b] = True`, sin coste ni rng). La puerta de la boca pasa a ser:

```python
def _recien_c2(P):        # LOCAL: sólo la ganadora, su propia casilla y el paso actual
    if not _ORj: return False
    _bh=_bin4(_MGv,P); _tn=_TNh[_MGv,_bh]
    return bool(_tn>=0 and 0<=t-_tn<=oreja_vent)

def _fam_c2(_k,P):        # la puerta del tronco, intacta, Y la pregunta nueva
    return _fam(_k) and not _recien_c2(P)
```

`_fam` es la función del tronco, **sin tocar una línea**: la oreja sólo puede **abrir** (mandar a la lenta), nunca
cerrar. Con `oreja = 0`, `_fam_c2 ≡ _fam` y el archivo es `organismo_familias_c1.py` bit a bit.

### 3.2 Las constantes, fijadas aquí y no después

- `oreja_vent = 2000` pasos. **Razón declarada, no ajustada:** en el mundo del bloque 4b la entrega ocurre en el
  señalamiento (el receptor está *sobre* el referente) y su primera exposición es ese mismo paso; 2000 pasos son
  ~2 % de la vida y ~1/17 de una ventana de deriva: suficiente para que la entrega y la exposición caigan
  dentro, demasiado poco para dejar la oreja abierta de por vida. **No se recalibra tras ver datos** (ERR-46..49).
- `oreja = 1` exige `variante_hija = 1` (sin divisiones no hay nacimientos que señalar) → si no, **lanza**.

### 3.3 Por qué debería funcionar, y por qué es honesto

La división de una casilla es **la señal local que el organismo ya produce** cuando su regla de familia acaba de
fallar bajo esta retina. La puerta por evidencia de código no puede verla (el código es viejo; el contenido es
nuevo). Con la oreja, el mensaje se lee en **dos pasos**: el código dice *"familia conocida"* y la casilla recién
nacida dice *"esta variante no"*. Es el "mensaje en dos pasos" del encargo, implementado como **crecimiento** y
no como regla de precedencia nueva.

### 3.4 El riesgo que declaro antes de medir (y cómo se controla)

**El mensaje puede abrir su propia oreja**: la entrega divide la casilla, y esa división es la que manda a la
lenta. Es una asimetría real entre `CANAL` y su gemelo mudo `CORTADO` **después** de la entrega (P-I3, que
compara el prefijo **hasta** la entrega, sigue pasando: se verifica, no se supone).

No la escondo: la convierto en el control. **Los brazos barajados (`BAR-H`, `BAR-T`, `VALOR`) también dividen y
también abren la oreja.** Si la especificidad fuera un artefacto de la ruta, los tres subirían con `CANAL`. La
declaración sólo es válida si `BAR-H` y `BAR-T` se quedan abajo **con la oreja abierta**, y eso se mide con el
diagnóstico `oreja_abierta` (en cuántas semillas `_recien_c2` fue cierto en la primera exposición al referente),
que se reporta **por brazo**. Si `oreja_abierta(CANAL) − oreja_abierta(BAR-H) ≥ 3`, la oreja está siendo
selectiva por contenido y **eso mismo refuta el montaje**: se para y se reporta (§6, refutador (v)).

## 4. Identidad que debe pasar ANTES de medir (arnés `identidad_c2.py`)

Nada se mide si esto no da **todo**:

1. `oreja = 0` ≡ `organismo_familias_c1.py` **bit a bit** (todas las claves), para `variante_hija ∈ {0,1}`,
   `k ∈ {1,3}`, sufijo b6 ∈ {0,1}, en mundo `'AB'`, en el mundo de familias y en el del bloque 4 (emisor y
   receptor), con `voraz`, con `par_herm` y en los **tres modos del canal** — y por la cadena de C1 (61/61),
   `== organismo_familias_b6`, `== organismo_v14` (TRONCO) y `== organismo_v15f_on`.
2. **Ancla de rng** a `T = 120 000` con `k = 1` y `k = 3`: la perilla apagada no consume un solo sorteo.
3. **Inercia doble:** con `variante_hija = 0` y con `memoria_pares = None`, `oreja = 1` ≡ `oreja = 0`
   (sin divisiones no hay nacimientos); y con `puerta = None` (las dos vías suman) la perilla **no existe**.
4. **Lanza** con `oreja ∈ {2, −1, 0.5, '1', True}`, con `oreja_vent ≤ 0`, y con `oreja = 1, variante_hija = 0`.
5. **Estructural, reimplementado FUERA del organismo:** en una corrida con divisiones, el conjunto de pasos en
   que `_recien_c2` es cierto coincide **exactamente** con el calculado fuera a partir de `_TNh` y `oreja_vent`.
6. **Controles que DEBEN diferir** (ERR-64b, ≥ 2 de 3): `oreja = 1` ≠ `oreja = 0` con divisiones;
   `CANAL-oreja` ≠ `CORTADO-oreja`; `BAR-H-oreja` ≠ `CANAL-oreja`.
7. La guarda del runner repite el subconjunto crítico **antes** de la etapa de medida (P-I1), y `(d)` **no pasa
   por el emisor** (ERR-71).

## 5. Brazos, celdas y semillas

- Celdas: **`k3h1`** (C1 tal como se confirme, `oreja = 0`) y **`k3o1`** (`oreja = 1`), pareadas en las mismas
  semillas, más **`k3v0`** (= b5 k=3 bit a bit) como control de Occam y referencia de R6.
- Los **nueve** brazos de la dirección (−) del 4b (ERR-53), con sus gemelos: `CANAL`, `CORTADO`, `BAR-H`,
  `BAR-T`, `VALOR`, `INM`, `OTRO`, `PAR`, `PAR0`.
- Semillas: **861–880** y réplica **881–900** (nuevas; 821–860 las gasta C1). T = 100 000. Humo del creador:
  ≤ 3 semillas de 904–906 (901–903 ya están vistas por el humo de C1).
- Puertas de montaje: P-I2, P-I3, P-I4 (exclusión por semilla, ERR-70) y **P-I5 tal como está**, con la lectura
  de validez que fijó el coordinador el 19-sep.

## 6. La letra — predicción numérica y qué me refuta

Umbrales sobre las semillas válidas, leídos como fracción (ceil 0.75 n / floor 0.25 n), en **cada** una de las
dos series:

| # | criterio | pasa |
|---|---|---|
| **O-9** | **el objetivo: la oreja se abre** | `vacuas P-I5 (k3o1) ≤ 2/20` **y** `vacuas(k3o1) ≤ vacuas(k3h1) − 3` |
| R1 | el canal sigue intacto | `CANAL ≥ 15/20`, `CORTADO ≤ 5/20`, pareado `≥ 14/20` |
| R2 | familia | `BAR-T ≤ CORTADO + 3` |
| R3 | variante | `BAR-H ≤ CORTADO + 5` |
| R4 | hace falta el referente | `VALOR ≤ CORTADO + 3` |
| R5 | especificidad entre hermanas | `dist(PAR) ≥ 12/20` y `≥ dist(PAR0) + 5` |
| R6 | no cuesta el cuerpo | muertes `≤ 1.5 ×` `CANAL-k3v0`, `okU ≥ okU(k3v0) − 0.10` |

Predicción por brazo (mediana y rango sobre 20, celda `k3o1`):

| brazo | `k3h1` (lo que C1 haya dado) | **`k3o1` (predigo)** |
|---|---|---|
| vacuas P-I5 | 6 (3–11) | **1 (0–3)** |
| CANAL | 17 | **18 (16–20)** |
| CORTADO | 1 | **1 (0–3)** |
| BAR-H | 4 | **3 (0–6)** |
| BAR-T | 4 | **4 (2–7)** |
| VALOR | 2 | **2 (0–4)** |
| PAR `dist` / PAR0 | 15 / 2 | **16 (14–19) / 2** |
| muertes | 35 | **35 (25–55)** |
| `oreja_abierta` en CANAL / BAR-H | — | **18 / 17** (la oreja NO distingue contenido) |

**En una frase:** *la oreja devuelve las semillas que P-I5 declaraba vacuas sin tocar ningún otro número, porque
sólo cambia POR DÓNDE se lee, no QUÉ se lee.*

**Qué me refuta, escrito ahora:**

1. **`vacuas(k3o1) > 5/20`** → el nacimiento no está donde la boca lee (la ganadora al leer no es la que se
   dividió): la oreja no engancha, y el cuello es la **selección de la ganadora**, no la puerta.
2. **`CORTADO > 5/20` o `VALOR > CORTADO + 3`** → abrir la oreja vuelve al organismo **sugestionable**: la vía
   lenta con valores heredados mueve la boca sin mensaje. Sería la refutación más importante y mataría la línea.
3. **`BAR-H > CORTADO + 5` con la oreja abierta** → la división no llega a las ganadoras, y entonces **toda la
   línea C es falsa**, no sólo la oreja.
4. **R6 cae** → la oreja manda a la lenta tan a menudo que el cuerpo se rompe (como `k = 5` en el bloque 5).
5. **`oreja_abierta(CANAL) − oreja_abierta(BAR-H) ≥ 3`** → la oreja se abre **según el contenido** del mensaje:
   es un artefacto de montaje, se para el bloque y se reporta (§3.4).
6. **C1 pasa O-C sin oreja** → **la oreja sobra por Occam y no se corre nunca**: se cierra como hipótesis con una
   línea en el registro. *Este es el desenlace que prefiero.*

## 7. Qué se podrá declarar, y qué no

Si **O-9** y R1–R6 pasan en las **dos** series, se podrá decir **sólo**:

> *En este mundo, un receptor que ya trataba al referente como familiar volvió a consultar su memoria lenta
> porque una casilla suya acababa de dividirse, y entonces el mensaje cambió su conducta; la conducta siguió
> siendo específica frente a la hermana de variante, frente a otro token y frente a un valor sin referente.*

No autoriza decir atención, sorpresa, metacognición, lenguaje, símbolo ni AGI. Si O-9 pasa en una sola serie, se
reporta como no replicado (regla 12) y se pide un tercer rango.
