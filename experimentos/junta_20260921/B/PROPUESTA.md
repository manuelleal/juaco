# PROPUESTA — CREADOR **B** (representación y computación) · JUNTA DEL 21-sep-2026

**Misión de fondo:** llegar a la AGI por este camino (organismo mínimo, reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas). **Mi foco hoy:** Q2 (fase 5). Voto también Q1 y Q3.

| | archivo (todos en `experimentos/junta_20260921/B/`) | sha256(16) |
|---|---|---|
| diagnóstico sobre los crudos ya registrados (no simula) | `analiza_q2_bav.py` → `salida_analiza_q2.txt` | `c4d358a6e3666c79` |
| cálculo estructural T = 0 (no simula) | `estructura_q2.py` → `salida_estructura_q2.txt` | `eaa6473e05302873` |
| modelo de un parámetro + potencia de A₁₂ (no simula) | `modelo_q1_q2.py` → `salida_modelo_q1_q2.txt` | `3b90f226c8a38440` |
| **mini-prueba de UN proceso, con `--humo` que ESCRIBE su JSON** | `corre_b21_lectura.py` → `humo_b21_salida.txt` | `be29d936d467499e` |
| instrumento: **copia BYTE A BYTE** de `nivel05_familia_variante_BAv/organismo_familias_bav.py` | `organismo_bav_b21.py` | **`2dca0a3e239481f0`** = origen |

> **Arnés de identidad.** No añadí ninguna perilla: mi copia es **idéntica bit a bit al origen preregistrado** (mismo sha, verificado por el
> propio runner antes de gastar una corrida). El control de vacuidad que sí corrí es el que importa aquí: **mi reimplementación FUERA de la
> regla de lectura coincide con `W_tabla` de DENTRO en los 32 estímulos, 32/32 en las 2 semillas** (`humo_b21_salida.txt`).

---

## 1. Porcentaje por nivel del brief (justificación de una frase + entrada del registro)

| nivel | % | por qué |
|---|---|---|
| 1–4 asociación / desaprender / generalizar / capacidad | **100 %** | cerrados; el negativo del alias quedó reparado por B-5 dentro del tronco (v14.2, 18-sep 21:25, `REGISTRO` «TRONCO v14.2») |
| 5 comunicación con referencia | **75 %** (sin cambio) | N1 cerrado; con la **réplica 981–1000 entrada hoy**, `BA-v` cae P6 por segunda vez (14/18 < 15) y la línea BA/BA-v se cierra por su propio §7 (HANDOFF 15.17) |
| 6 mapa, dos metas, rodeo | **50 %** | elige entre dos comidas recordadas y rodea el veneno recordado, replicado; no planifica (17-sep, `rodeo_s41-60/61-80`) |
| 7 composición / XOR | **70 %** | 3T-k compone hasta 3 y XOR cruza con 8 ejemplos **sólo con prior de pares declarado**; la línea de memoria de pares en la vía lenta quedó CERRADA sin que entrara ningún candidato (HANDOFF 15.16) |
| 8 aprendizaje abierto | **40 %** | curiosidad por progreso refutada; el mundo vivo de dos necesidades es el primer mundo con más de una dimensión de valor (18-sep) |
| 9 autonomía / modelo de sí mismo | **30 %** | fase 9 bloque 1: 8/10 puertas, caen F9-4 y F9-7, **sin réplica**; H-1 y ERR-62 en pie (HANDOFF 15.18) |
| 10–13 alma / familias / vivo | **10 %** | exploratorio: el alma razonada no gana al azar; el mundo de familias existe y mide (18-sep) |

## 2. Voto y predicción en las tres preguntas

**Q1 — T-A y T-C (ii) pareadas: NO-REGRESIÓN, y además la letra está mal calibrada.** No es una opinión: `A₁₂ ≥ 0.50` pareado pone el umbral
**exactamente en la media de la hipótesis nula**. Con n = 20 y sin empates, n·A₁₂ ~ Bin(20, 0.5): un candidato **indistinguible del tronco**
pasa un brazo el **58.8 %** de las veces, y T-A (dos brazos) **falla el 65 %** de las veces (`salida_modelo_q1_q2.txt`). Eso explica sin
mecanismo la observación transversal del director (v15f y dE5 con A₁₂ 0.4–0.55): **la puerta es una moneda al aire para lo inerte**, y una
puerta que rechaza dos de cada tres candidatos inertes no mide capacidad ni no-regresión: mide ruido de muestreo.
*Voto:* no-regresión, con **banda de la nula**: `A₁₂ ≥ 0.50 − 1.645·0.5/√n` (**≥ 0.32** con n = 20), y **la capacidad vive SÓLO en T-G**, que es
donde el candidato declara qué compra. Esto **exige ERR nuevo, semillas nuevas y no rejuzga a NADIE** (regla 3): ni v15c/d/e/f, ni dE5, ni B-5.
*Predicción firmada:* con la banda, **el primer candidato que cruce T-G volverá a caer en T-E (no regresión conductual), no en T-A** — T-E es la
puerta que de verdad selecciona, y ninguna relajación de T-A la toca.

**Q2 — La fase 5 se cierra en 75 % con lo medido, PERO hay un candidato con mecanismo que nadie probó.** Ver §3. Lo nuevo de hoy es que **ya
sé por qué falla `BA-v`, con una cuenta exacta**, y no es lo que la fase 5 creía:
1. **La dirección ya es perfecta.** En las 19 semillas de 961–980 el mensaje alcanza **1 de los 32 estímulos** (`n_mismo_dos` mediana 1, máx 3)
   y **la hermana está FUERA del grupo en 19/19** (`herm_en_grupo` False). El código factorizado que pedía la fase 5 **existe y está medido**.
2. **Lo que falla es el VALOR, y por una colisión estructural.** Con `var_cubre=1` el tipo VARIANTE son **tres** pares mixtos, uno por píxel de
   variante. El referente `T1v2` y su hermana `T1v0` difieren en **2 de 12 píxeles**, los dos de variante → **exactamente UNA de las tres
   ganadoras de variante les da LA MISMA casilla**: la que cubre el píxel en que coinciden. Medido a T = 0 en **37/37 semillas** de las dos
   series (`salida_estructura_q2.txt`). Es decir: **el mensaje escribe su +R dentro del propio canal que tenía que vetarlo.**
3. **La cuenta cierra con UN parámetro.** Para la hermana: `s_FORMA = +3` (las 36 celdas de forma colisionan las 36) y
   `s_VARIANTE = (+1 del mensaje) + v9 + v11`, con `v ∈ {+1, −3}`. La boca con hambre = 1 muerde si la lectura > −2.083 → **sólo veta el caso
   (−5)**, o sea que hagan falta **las dos** casillas propias en veneno. Con `p` = P(una casilla propia vale −3) ajustado sobre `dist(PAR)`,
   el modelo **predice `BAR-H` sin tocarlo**: 6.0 predicho / **7 medido** en 961–980, y 4.0 predicho / **4 medido** en 981–1000.
*Predicción firmada:* con la regla pesimista dentro del tipo (§3), `dist(PAR)` sube a **17–18 de 19** y `BAR-H` baja a **0–2**; y **R6 (coste)
es lo que lo mata** (le doy 35 %).

**Q3 — La letra de F9-4 NO mide lo que quería medir, y es la trampa 2 aplicada al CONTROL.** F9-4 compara candidato y nodo barajado sobre una
medida **de un solo lado** (vive más), y el barajado gana esa medida produciendo **cautela genérica** (c1 0.598: deja de comer lo bueno).
Un control con la misma información y la correspondencia destruida tiene que juzgarse con **la misma medida de dos lados que el candidato**:
`p1` (rechaza lo malo al primer encuentro) **y** `c1` (come lo bueno al primer encuentro), o su diferencia pareada. *Voto:* reescribir F9-4 como
puerta balanceada (`p1 − (1 − c1)` del candidato ≥ barajado + margen), con **ERR nuevo y semillas nuevas**; **F9-4 de 1501–1520 no se rejuzga**.
*Bloque 2 de la fase 9:* población con herencia y muerte real **sobre el cuerpo nuevo con nodo**, con R₀ ≥ 0.9 como puerta y **H-1 como control
negativo obligatorio en la misma serie** (sin él, un R₀ alto no se distingue de un mundo más blando). Es línea de C; no la diseño yo.

---

## 3. MI BLOQUE SIGUIENTE — **BA-vm: «la variante vota con su PEOR casilla, no con la suma»**

**Hipótesis.** *Dentro del tipo VARIANTE, la suma deja que el propio mensaje —que se cuela por la única ganadora estructuralmente ciega a la
variante— compre el voto de las dos que sí separan. Con el mínimo, la casilla contaminada ya no puede outvotar a ninguna: basta UNA casilla
propia en veneno para vetar la hermana, y el referente sigue leyendo +R porque el mensaje escribió en las tres.*

**Mecanismo mínimo · MEMORIA NUEVA: CERO.** Una línea dentro de `_suma_tipo`, la función que ya existe:
```python
    def _suma_tipo(_gs,P):
        _vs=[float(_MMv[_g7,_dir_var(_g7,P)]) for _g7 in _gs if _MNv[_g7,_dir_var(_g7,P)]>0]
        if not _vs: return 0.0,0
        if _DMv and (_MINV==0 or _gs is _vtipo): return float(len(_vs)*min(_vs)), len(_vs)   # NUEVO: min ESCALADO a k
        return float(sum(_vs)), len(_vs)                                                     # BA-v: la suma, literal
```
Ni un array, ni un contador, ni un bit: las mismas 66 celdas, las mismas 4 casillas, el mismo `_MEv`, la **misma escritura**, el mismo
`_dir_var`, el mismo `_topk_tipo`, el mismo consumo de rng. El mínimo va **escalado por el número de casillas conocidas** para que el valor siga
en la escala de k = 3 y **`CANAL` no pierda margen** (con las tres casillas del mensaje, `3·min(+1,+1,+1) = +3` = lo de hoy, exactamente).
**Celda candidata `BA-vm` = `BA-v` + `dentro='minv'`** (el mínimo **sólo en el tipo VARIANTE**, que es el que veta: es lo más barato para R6).
**Ablación preregistrada AHORA, antes de los datos:** `BA-vM` = `dentro='min'` (los dos tipos, la intención literal de A). **Si pasa `BA-vM` y no
`BA-vm`, el resultado es `BA-vM`** y la lección es que el pesimismo también hacía falta en la forma. No es una salida de emergencia: la serie las separa.

**Instrumento y anclas.** `construye_familias_bavm.py` por anclas sobre `organismo_familias_bav.py` (sha `2dca0a3e239481f0`, aborta si cambia),
con tripwire de `organismo_familias_ba` (`1f196ee786b2040d`), `a1`, `b6`, `b5`, `b4b` y `organismo_v14` (`feefc88b1fd8d434`), y postcondiciones:
escritura intacta, `_dir_var`/`_bin4` intactos, `_topk_tipo` intacto, `rng.` con el mismo recuento, la línea nueva exactamente una vez.
**Arnés:** apagado (`dentro='suma'`) ≡ `organismo_familias_bav` **bit a bit** con las seis configuraciones de lectura (incluida `conj_tipo=2`) y
la cadena hasta `organismo_v14`; **controles que DEBEN diferir (≥ 2 de 3 semillas, ERR-64b): `BA-vm ≠ BA-v`, `BA-vM ≠ BA-v`, `BA-vm ≠ BA-vM`** —
esto es lo que ERR-88 exige y lo que A no tuvo. **Perilla mal escrita LANZA.** **Regla 14:** entrada campo a campo contra el bloque 6 (33 campos).
**Runner:** `corre_familias_bavm.py --humo` (escribe su JSON en `datos/humo/`) y `--serie`; celdas
`b4b,b5k3,b6suf,A1,BA-v,BA-vm,BA-vM,BA-vm-sh`; `b4b` obligatoria (**ERR-89**); crudo antes de analizar (**ERR-54**).
**Criterio:** **las puertas ABSOLUTAS P0–P7 y la MISIÓN de `PREREGISTRO_bav.md` §3, sin tocar una letra** (ERR-90 ya escrito; no recalibro nada).

**Predicción numérica firmada (mediana y rango, en CADA una de las dos series).**

| puerta | predicción | P(pasa las dos) |
|---|---|---|
| P1 CANAL ≥ 15 | **18** (15–19) | 85 % |
| P2 CORTADO ≤ 5 | 0 (0–2) | 92 % |
| P3 BAR-T ≤ 5 | 2 (0–5) | 80 % |
| P4 VALOR ≤ 5 | 2 (0–5) | 82 % |
| P5 BAR-H ≤ 10 | **1** (0–4) | 92 % |
| **P6 dist ≥ 15 y PAR0 ≤ 5** | **dist 17 (15–19)**, PAR0 1 (0–3) | **70 %** |
| **P7 R6 muertes ≤ 1.5×(b4b)** | **1.6× (1.1–2.4×)** | **35 %** |
| P7 R6 okU | −0.08 (−0.17 a 0.00) | 65 % |
| MISIÓN (BAR-T ≤ 5 **y** dist ≥ 15) | BAR-T 2, dist 17 | 65 % |
| **TODO (candidato declarado)** | — | **18 %** |

**Contrastes pareados que firmo aparte** (no dependen del nivel absoluto): (1) `dist(BA-vm) ≥ dist(BA-v) + 3` en las dos series;
(2) `BAR-H(BA-vm) ≤ BAR-H(BA-v)` en las dos; (3) `abstiene(BA-vm)` mediana **0**, igual que `BA-v` (mi regla **no calla más**: no repite a A1);
(4) `CANAL(BA-vm-sh) ≤ CORTADO(BA-vm-sh) + 3` (memoria barajada).

**El control que puede fallar, y lo digo antes: R6.** `BA-v` ya está en **1.46×** y **1.50×** contra `b4b` (el lector más permisivo, k = 1). Mi
regla hace la tabla **más pesimista**, y el mecanismo del coste ya está medido: `BA-v` no se envenena más, **come menos** (mordidas de comida
3 494 contra 4 950 de `b4b` en la réplica; veneno 13.5 contra 80.5). **Le doy 35 % y no voy a discutir la mediana si cae.** Segundo control:
`b5k3`/`b6suf` tienen que reproducir sus números de las cuatro series dentro de ±4 o no se lee ningún veredicto (regla 14, ERR-38).

**Qué me refuta.** (1) `dist(PAR) < 15` en cualquiera de las dos → el modelo de un parámetro es falso y **la fase 5 se cierra en 75 %** con la
frase «la referencia exacta está, y cuesta comida». (2) `CANAL < 15` → el mínimo escalado sí quita margen y mi razonamiento de escala es falso.
(3) `abstiene > 0` de mediana → mi regla calla y estoy repitiendo `exige_dir` de A1 sin darme cuenta. (4) `BA-vm ≡ BA-v` hasta el último decimal
→ la perilla no está conectada: **ERR-88 otra vez**, y el arnés tiene que haberlo cazado antes. (5) Todo baja a la vez, `CANAL` incluido → no
hay referencia; lo distinguen `CORTADO`, `BA-vm-sh` y las celdas de instrumento de la misma serie.

**Semillas NUEVAS (verificadas libres con grep sobre `*.py`/`*.md` de `experimentos/`, `registro/` y `organismo/`): serie `1541–1560`, réplica
`1561–1580`.** Única aparición en el rango 1541–1580: ninguna; `1540` aparece sólo como fin de la réplica de la fase 9 en `ESTADO.md`.
**Humo: `918–920`** (banda 901–920; 901–903 la junta, 912 el humo de BA-v, 913–915 las mías de hoy, 916–917 el bloque del alias de `creacion_B`).

**Las cuatro trampas.** (1) *Canal simétrico:* no lo es y se comprueba — emisor `b4b` bit a bit y sin tocar, el receptor no ve al emisor,
`CORTADO`/`PAR0` son los gemelos mudos, y `BA-vm-sh` (memoria barajada, misma información y misma trayectoria) prueba que importa la
**dirección** en que se escribe. (2) *Acierto sin balancear:* la medida es binaria y pareada (mordió o no en su **primera exposición de la vida**)
y las puertas van en los dos sentidos: P1 obliga a comer cuando el mensaje lo dice, P2–P6 obligan a no comer cuando no; el que no come nunca
falla P1 y P7. (3) *Mundo que se come la comida:* mundo del bloque 1/2 **importado, no recopiado**, `renov=1.0`, el muestreo no lo fija el
candidato, y el coste es puerta (P7) con diagnóstico de mordidas/veneno/`frac_regalo`. (4) *Sitios fijos:* P-I4 exige que la primera exposición al
referente sea la de después de la entrega; los patrones se regeneran con `fam_seed` por semilla; mi regla no añade ningún índice fijo.

## 4. ERR que mi idea podría repetir, y cómo los evito

**ERR-88** (declarar «inerte» lo que no estaba conectado) — es *exactamente* mi perilla: el arnés exige **tres controles que DEBEN diferir** y el
runner imprime el contraste `BA-vm − BA-v` por brazo. **ERR-38/41/42** (copia por anclas que pierde un parámetro) — tripwire de shas +
postcondiciones + regla 14 campo a campo + humo que escribe su JSON. **ERR-31** (leer umbrales de la batería y no del preregistro) — las puertas
son las de `PREREGISTRO_bav.md` §3 copiadas sin tocar. **ERR-44** (medir pesos en vez de conducta) — todo `com`/`dist` por conducta de la boca.
**ERR-46..49** (recalibrar tras ver datos) — umbrales, refutadores y probabilidades escritos arriba. **ERR-54** — crudo antes del análisis.
**ERR-70 / P-I5** — vacuidad declarada antes: espero **1–3 de 20** semillas con `fam1 = 1` en `BA-vm` contra 1–2 en `BA-v`; si la diferencia pasa
de 4/20, la lectura principal pasa a la **intersección pareada**. **ERR-89** — `b4b` obligatoria en `--celdas`. **ERR-90** — puertas absolutas, y
**no** normalizo por `CORTADO`. **ERR-62/H-1** — no aplica (no toco población).
**Y el fallo del que vengo:** mi antecesor B dio con la conjunción y creyó que la referencia la fijaba **la dirección**; hoy se mide que la
dirección ya era única (1/32) y que lo que sobra es **valor prestado dentro del propio canal de veto**. La lección de la bitácora («ningún
combinador de *valores* puede vetar al mensaje, sólo la dirección») **es falsa en su forma general**: sí puede, si el combinador es el mínimo y
el mensaje no está en todas las casillas del tipo. Lo declaro como corrección de mi propia línea.

## 5. Predicciones propias refutadas hoy · lo que NO pude verificar

- **REFUTADA (mía, hoy):** escribí, antes de correr la mini-prueba, que comparar las reglas de lectura **al final de la vida** separaría el
  candidato. **Es falso:** a T = 33 000 el mensaje ya está sobrescrito y las tres reglas leen **−9, −3, −9 para el referente Y para la hermana**
  (`humo_b21_salida.txt`): la tabla del final de la vida **no distingue nada**. Lo único que ese humo decide es (a) que mi reimplementación es
  exacta (32/32 contra `W_tabla`), (b) que la colisión 1/3 aparece también en la corrida, y (c) que el pesimismo **encoge el conjunto de
  estímulos que la tabla licencia** de 12 a 9 y de 8 a 6 de 32 — que es justo el riesgo de R6 que declaro. La separación del mecanismo se apoya
  en el cálculo estructural y en el modelo de un parámetro, **no** en ese humo.
- **REFUTADA (de la línea, la declaro yo porque es mía):** la lección «lo que discrimina no es el valor sino si el mensaje alcanzó la dirección»
  (bitácora de la junta de la fase 5, firmada por B). Con la dirección ya única, el que decide es el valor.
- **NO PUDE VERIFICAR:** (a) qué lee la tabla **para la hermana en el paso exacto de la entrega** — el instrumento sólo exporta `canal_lee_ref`
  para el referente; mi bloque lo añade como diagnóstico (`canal_lee_herm`, sin tocar estado ni rng). (b) El valor de `p` medido directamente
  sobre las casillas (lo obtengo por ajuste, no por lectura). (c) La conducta de `BA-vm`: con ≤ 6 corridas y ≤ 200 000 pasos no se reproduce
  ninguna línea base — el humo decide mecanismo y montaje, nunca brazos.
- **Dato entrado mientras escribía (no lo cambia):** la réplica **981–1000 terminó a las 15:57** y `BA-v` **vuelve a caer P6** (dist 14/18, una
  semilla), pasando P0–P5 y P7 (R6 exactamente 1.50×). Por su propio §7, **la línea BA/BA-v se cierra**; el nivel 5 sigue en 75 %.

---

### Salida pegada del arnés / control de identidad (`humo_b21_salida.txt`, un proceso, 21.6 s)

**Coste real declarado (regla 3):** el presupuesto planificado e impreso por el runner es **6 corridas × 33 000 = 198 000 pasos**; el gasto
**real fue de 5 corridas = 165 000 pasos** (3 emisores + 2 receptores: la semilla 914 no emitió y su receptor no se corrió, P-I2). El JSON del
humo guarda el **plan** en `meta.corridas`/`meta.pasos`; esta línea es la corrección honesta y no se edita el script después de correrlo.

```
MINI-PRUEBA B (Q2, junta 21-sep): las reglas de lectura comparadas SOBRE LA MISMA TABLA.
  copia del instrumento  2dca0a3e239481f0   origen 2dca0a3e239481f0   esperado 2dca0a3e239481f0   -> IDENTICA
  runner BA-v (solo lectura) 4453754a9921e349   corre_familias_b6 88253f352d921c42
  presupuesto: 6 corridas x T = 33000  ->  198000 pasos
  celda BA-v = {'k_ganadoras': 3, 'memoria_variante': 0, 'dos_tipos': 1, 'k_forma': 3, 'var_cubre': 1,
                'combina': 'min', 'msg_elige': 0, 'conj_tipo': 2}
  s913     8.6s  entrega t=22040  muertes 293  control SUMA==W_tabla 32/32  ganadoras VARIANTE que COLISIONAN entre T1v2 y T1v0: 1/3
  s914: el emisor NO emitio a T=33000 -> semilla sin mensaje, se reporta y se sigue        (P-I2)
  s915     8.9s  entrega t=25840  muertes  10  control SUMA==W_tabla 32/32  ganadoras VARIANTE que COLISIONAN entre T1v2 y T1v0: 1/3
--- RESUMEN (mecanismo, NO conducta) ---
  SUMA      muerde X 0/2   muerde HERMANA 0/2   muerde OTRO TOKEN 0/2   mediana muerde/32 12
  MIN       muerde X 0/2   muerde HERMANA 0/2   muerde OTRO TOKEN 0/2   mediana muerde/32  9
  MINESC    muerde X 0/2   muerde HERMANA 0/2   muerde OTRO TOKEN 0/2   mediana muerde/32  9
HUMO -> datos/humo/humo_b21_lectura_20260921_155927.json
```

```
--- ESTRUCTURA (T = 0, sin simular; 19 semillas de 961-980, idéntico en las 18 de 981-1000) ---
Referente X = T1v2   Hermana H = T1v0   Otro token TK = T3v2
pares de FORMA: 36   pares MIXTOS (tipo VARIANTE): 27   px de variante: [9, 10, 11]
seed 961..980: dHam(X,H) = 2 en 19/19 · px de variante IGUAL = 10 en 19/19 · forma_col 36/36 en 19/19
   ganadoras VARIANTE: (i,9) separa · (i,10) COLISIONA · (i,11) separa      -> 1 de 3 COLISIONA en 37/37 semillas
semillas donde el SUFIJO tampoco separaria (firma de 3 px igual): 0/19
```

```
--- MODELO DE UN PARAMETRO: se AJUSTA con dist(PAR), se PREDICE BAR-H ---
serie      dist(PAR)   p       BAR-H predicho   BAR-H medido   dist con min (predicho)
961-980    13/19       0.827   6.0              7              18.4/19
981-1000   14/18       0.882   4.0              4              17.7/18
--- Q1: POTENCIA DE A12 >= 0.50 PAREADA, candidato INDISTINGUIBLE del tronco ---
n=20: P(pasa un brazo) 0.588 · P(falla un brazo) 0.412 · P(falla T-A, dos brazos) 0.654
banda de la nula (sd de A12) 0.112 ·  umbral que deja pasar al 95 % de lo inerte: A12 >= 0.32
```
