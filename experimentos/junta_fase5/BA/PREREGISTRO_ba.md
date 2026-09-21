# PREREGISTRO — CANDIDATO **BA** (junta de la fase 5): la lectura CONJUNTIVA de B, aplicada POR TIPO a las dos ganadoras de A

**MISIÓN (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales, sin
retropropagación, que aprende, desaprende, generaliza, sobrevive y **se comunica con referencia**. Hoy, fase 5:
que el mensaje refiera a la **FAMILIA Y a la VARIANTE** con la misma tabla — **`BAR-T ≤ 5/20` Y `PAR ≥ 15/20`**
a la vez, con las puertas del bloque 6, en las dos series.

**Fecha:** 2026-09-21. **Autor:** creador BA (Opus). **Estado:** §0–§8 escritos **antes** de correr el humo y
**antes** de cualquier serie. El humo del §9 se corrió después y **no tocó** los §0–§8. Lo que cambie después
va en ERR numerado, con fecha, motivo y semillas nuevas.

**Carpeta:** `experimentos/junta_fase5/BA/` (nueva; no se toca `A/`, `B/`, `C/`, `organismo/` ni nada congelado).

| | archivo | sha256(16) |
|---|---|---|
| constructor por anclas | `experimentos/junta_fase5/BA/construye_familias_ba.py` | `503ada31c3da9a3b` |
| instrumento | `experimentos/junta_fase5/BA/organismo_familias_ba.py` | `1f196ee786b2040d` |
| arnés de identidad — **56/56** | `experimentos/junta_fase5/BA/identidad_familias_ba.py` | `c01162c2e46d5de2` |
| runner (humo y serie) | `experimentos/junta_fase5/BA/corre_familias_ba.py` | `f511d1bbe34887af` |
| **origen (sólo lectura)** | `experimentos/junta_fase5/A/organismo_familias_a1.py` | `8833e1dcfb62f26d` |
| cadena (sólo lectura) | `experimentos/nivel12_mundo_familias/organismo_familias_b6.py` | `b10cbd4ddd0c32a3` |
| tronco (sólo lectura) | `organismo/organismo_v14.py` | `feefc88b1fd8d434` |

---

## 0. Lo que la junta dejó medido, y lo que esa tabla dice

Series 821–840 / 841–860 (las corrió el coordinador; `com` = la boca mordió en su **primera exposición de la
vida** al referente):

| celda | CORTADO | BAR-H | **BAR-T** | **dist(PAR)** | CANAL | muertes |
|---|---|---|---|---|---|---|
| `b5k3` (k=3 FORMA, denso, DISYUNCIÓN) | **0 / 0** | 13 / 13 | **3 / 2** | 7 / 6 | 18 / 17 | 37 / 95 |
| `k3v0j1` (k=3 FORMA, denso, **CONJUNCIÓN de B**) | 2 / 1 | 13 / 12 | **2 / 2** | 10 / 7 | 17 / 16 | 35 / 34 |
| `b6suf` (sufijo, DISYUNCIÓN) | 1 / 3 | 10 / 4 | 12 / 8 | **15 / 15** | 17 / 16 | 30 / 33.5 |
| `k3v1j1` (sufijo + CONJUNCIÓN de B) | 4 / 2 | 9 / 7 | 7 / 5 | 14 / 14 | 17 / 15 | 27.5 / 31 |
| `A1` (dos tipos + `min` + `exige_dir`) | 4 / 4 | 10 / 7 | 9 / 5 | 13 / 13 | 18 / 17 | 28 / 43.5 |

**Tres hechos que salen de ahí y que nadie usó juntos:**

1. **El mejor BAR-T de toda la junta (2/20 y 2/20), con base baja (CORTADO 2 y 1), lo da la conjunción de B
   sobre las k ganadoras de FORMA SIN sufijo** (`k3v0j1`): densidad intacta, referencia de familia exacta. Lo
   único que le falta es la variante (`dist` 10 y 7).
2. **La separación de la hermana la dan el sufijo (`dist` 15/15) o las ganadoras MIXTAS de A (`dist` 13/13)**,
   y las dos la pagan en la base: CORTADO de 0–1 sube a 4.
3. **En A1 esa base sube por `exige_dir`.** Exigir que las SEIS ganadoras (3 de forma + 3 mixtas) conozcan su
   casilla hace callar a la tabla mucho más; cuando la tabla calla decide la **lineal**, que con `hambre = 1`
   lee ≈ −1.0 y **no frena la mordida** (hace falta ≲ −2.1: la escala que A midió). Por eso en A1 suben **a la
   vez** CORTADO (4), VALOR (7 y 6) y BAR-T (9 y 5): **es la misma fuga, y ninguna de las tres la causa el
   mensaje.** El arnés de este bloque lo vuelve a medir sobre la misma tabla: `exige_dir` hace callar a la
   tabla en **16 de 32** estímulos, y **las 16 son por el tipo VARIANTE: el tipo FORMA nunca estaba incompleto**.

---

## 1. Hipótesis

> **La conjunción de B (la referencia es la INTERSECCIÓN de las direcciones, no la unión) no había que
> aplicarla a una lista de ganadoras, sino a CADA TIPO de ganadora por separado: la FORMA decide si la tabla
> habla, y la VARIANTE decide si lo que dice es del referente o de su hermana. Un tipo incompleto no vota, pero
> tampoco manda callar a la tabla.**

Si es cierta, `BAR-T` y `CORTADO` vuelven al nivel de `k3v0j1` (2 y 1–2) porque la lectura de forma es la
suya, y `dist(PAR)` sube al nivel de A1 (13) o por encima porque el veto de variante sigue ahí — **las dos a la
vez, que es lo que ningún candidato ha conseguido**.

## 2. Mecanismo mínimo y **MEMORIA NUEVA: CERO**

**Una perilla, `conj_tipo` (default 0 = `organismo_familias_a1` bit a bit), y tres líneas dentro de
`_tabla_dos`, la función que A ya tenía.** No hay un array nuevo, ni un contador, ni un bit de procedencia: las
mismas 66 celdas, las mismas 4 casillas por celda, el mismo `_MEv`, la misma escritura, el mismo `_dir_var`.

```python
    def _tabla_dos(P):
        _f7,_v7=_topk_tipo(); _sf7,_nf7=_suma_tipo(_f7,P); _sv7,_nv7=_suma_tipo(_v7,P)
        if _CTv:                                                     # BA: la conjuncion de B, POR TIPO
            if _nf7<len(_f7): return (0.0, False)                    # (1) la FORMA no consta -> la tabla CALLA (releva a la lineal)
            if _nv7<len(_v7) and (_CTv==1 or not _nv7): return (_sf7, True)   # (2) la VARIANTE no consta -> el TIPO NO VOTA (no hace callar)
            return (min(_sf7,_sv7), True) if _CMv else (...)         # (3) los dos tipos enteros -> la conjuncion de VALOR de A
        ...                                                          # de aqui abajo, A1 literal (intacto)
```

- **(1) es exactamente `mem_conj` de B**, restringida al tipo que fija la familia. Es lo que midió BAR-T 2/20 y
  2/20 con CORTADO 2 y 1.
- **(2) es lo que A1 no hacía**, y es lo único que cambia respecto de A: una casilla de variante que no consta
  **no es evidencia contra el mensaje**, y convertirla en abstención es lo que subió la base de A1.
- **(3) es `combina='min'` de A**: para morder tienen que estar de acuerdo los dos tipos; para no morder basta
  uno que diga veneno.
- **Ablación preregistrada en la misma serie, `conj_tipo=2` (celda `BA-v`):** la variante incompleta **sí vota
  con lo que sabe** (la disyunción de b5 dentro del tipo). Se declara **ahora**, antes de los datos, que si
  `BA-v` cumple la misión y `BA` no, **el resultado es `BA-v`** y la lección es que dentro del tipo VARIANTE el
  voto gana a la abstención — lo contrario de lo que B halló para FORMA. No es una salida de emergencia: son
  dos lecturas del mismo mecanismo y la serie las separa.

**`conj_tipo=1` EXIGE `dos_tipos=1` y PROHÍBE `exige_dir=1` (lanza).** Dos reglas de abstención no se componen
y no se elige una en silencio.

**Lo que NO se toca (ni una línea):** el emisor, el canal, el mundo, la ESCRITURA (las 66 celdas siguen
escribiendo R CRUDO por sobrescritura en su dirección), `_dir_var`, `_topk_tipo`, `_suma_tipo`, `_MGv` y su
desempate al azar, `_MEv`, la vía rápida, la puerta, la boca, el metabolismo y **el consumo del rng**.

**Diagnósticos nuevos (no deciden ninguna predicción, no tocan estado ni azar):** `canal_lee_ref` = qué lee la
tabla **para el referente** en el paso exacto de la entrega — `[valor, habla, exactas de FORMA, exactas de
VARIANTE]` (es el diagnóstico que a B le dijo cuál de sus tres ideas era la buena); y `mem_visto` = la matriz
`_MNv > 0`, derivada de un array que ya existía, que permite **reimplementar las tres reglas FUERA del
organismo y compararlas SOBRE LA MISMA TABLA** (la lección de B: dos trayectorias distintas no comparan reglas).

## 3. Instrumento y anclas

`construye_familias_ba.py` construye `organismo_familias_ba.py` **por anclas** sobre
`organismo_familias_a1.py` (sha `8833e1dcfb62f26d`, verificado; aborta si cambia), y verifica además los shas
de `organismo_v14.py` (TRONCO), `b6`, `b5`, `b4b`, `escala_codigo`, `v15f_on`, `construye_familias_a1.py` y
`organismo_familias_jb.py`. Seis anclas y **ocho postcondiciones**: la escritura intacta, `_dir_var` y `_bin4`
intactos, la elección de ganadoras por tipo intacta, `rng.` con el mismo recuento que a1, el desempate de
`_MGv` intacto, la regla `exige_dir` de A intacta, y la lectura nueva exactamente una vez.

**Arnés `identidad_familias_ba.py` (§9.0):** apagado ≡ a1 bit a bit con **todas** las perillas de A encendidas,
en 8 mundos × (k, sufijo), con el canal en sus tres modos y ancla larga a T = 120 000; cadena ≡ b6 ≡ b5 ≡ b4b ≡
`organismo_familias` ≡ **`organismo_v14` (TRONCO)** ≡ `v15f_on`; inercia sin tabla; la regla reimplementada
FUERA comparada con `W_tabla` estímulo a estímulo; las tres reglas comparadas **sobre la misma tabla**; ocho
perillas mal escritas que **lanzan**; y **siete controles que DEBEN diferir** (ERR-64b, ≥ 2 de 3).

**REGLA 14 (ERR-38/41):** el runner reconstruye la entrada del bloque 6 con **sus** objetos
(`corre_familias_b6.tarea`, línea a línea) y la compara **campo a campo** con la suya antes de correr; las
únicas diferencias permitidas son las perillas declaradas de la celda. Si algo más difiere, **se para** — en el
humo y en la serie, antes de gastar una corrida.

## 4. Brazos, celdas, emisor y semillas

- **Brazos:** los 7 de la letra de la misión, dirección (−) sola (ERR-53): `CANAL`, `CORTADO` (gemelo mudo),
  `BAR-H` (hermana), `BAR-T` (otro token), `VALOR` (ceros), `PAR`, `PAR0`. Todo `com`/`dist` por **conducta de
  la boca** (ERR-44).
- **Celdas:** `b5k3` (= bloque 5 bit a bit), `b6suf` (= bloque 6 bit a bit), `A1` (el candidato del creador A,
  el control que más importa), **`BA`** (el candidato) y, si hay CPU, **`BA-v`** (la ablación de §2).
- **Emisor:** el del bloque 6 **sin tocar** (`conj_tipo=0`, `dos_tipos=0`, `memoria_variante=0`,
  `k_ganadoras=1`, `voraz=1.0` = b4b bit a bit). Lo que se mide es **la lectura, no el habla**.
- **Semillas NUEVAS: serie `861–880`, réplica `881–900`.** T = 100 000.
  **Colisión declarada:** `C/PREREGISTRO_oreja.md` reservó 861–900, pero se escribió con la condición
  *"no se corre hasta que C1 esté confirmada en 821–840 y 841–860"* y **C1 quedó refutado ×2**, así que esa
  reserva ya no tiene dueño. Si el coordinador prefiere conservársela, la alternativa preregistrada aquí es
  **`921–940` y `941–960`** (921+ no las ha tocado nadie). La decisión es suya y no cambia ningún umbral.
- **Humo del creador:** **1 semilla (911)**, fuera de 821–900 y fuera de 901–903 (las vio la junta).
  El runner **rechaza** cualquier semilla de 821–900.

**Puertas de montaje (las del bloque 6, sin cambiar):** P-I1 identidad 100 %; P-I2 emisor ≥ 18/20 (las semillas
sin mensaje se excluyen y se reportan); P-I3 prefijo exacto contra el gemelo de la misma celda; P-I4 exclusión
por semilla (ERR-70); P-I5 `fam1 = 1` se reporta por brazo y **la semilla vacua sale del numerador Y del
denominador de todos los brazos de esa celda, con el mismo trato para la línea base** (decisión del coordinador
del 19-sep, aplicada tal cual).

**Vacuidad contra conducta, declarado antes:** es **VACUA** la semilla en que la boca no llegó a consultar la
vía del mensaje — emisor sin mensaje, `evX is None`, `t_X != t_entrega` o `fam1 == 1`. **NO es vacua, es
CONDUCTA**, la abstención de la tabla cuando el tipo FORMA no consta: ahí la vía lenta **sí** fue consultada y
relevó a la lineal, y ese valor entró en la boca. **Predicción de vacuidad:** 0–3/20 semillas con `fam1 = 1` en
`BA` contra 0–3/20 en `b5k3` (el candidato hace que la tabla hable **más** que A1, no menos, así que no espero
el efecto que C describió). Si `vacuas(BA) − vacuas(b5k3) > 4/20` en cualquiera de las dos series, la lectura
principal pasa a la **intersección pareada**, y se declara ahora para no decidirlo después.

## 5. PREDICCIÓN NUMÉRICA, FIRMADA (mediana / rango sobre 20, en **cada** una de las dos series)

| brazo | criterio de la MISIÓN | `b5k3` (medido) | `A1` (medido) | **`BA` (predicción)** | `BA-v` (predicción) |
|---|---|---|---|---|---|
| CANAL | ≥ 15/20 | 18 / 17 | 18 / 17 | **17 (15–19)** | 17 (14–19) |
| CORTADO (mudo) | ≤ 5/20 | 0 / 0 | 4 / 4 | **2 (0–4)** | 1 (0–4) |
| BAR-H (hermana) | ≤ 5/20 | 13 / 13 | 10 / 7 | **6 (3–10)** | 4 (1–8) |
| **BAR-T (otro token)** | **≤ 5/20** | 3 / 2 | 9 / 5 | **3 (0–5)** | 2 (0–5) |
| VALOR (sin referencia) | ≤ 5/20 | 4 / 1 | 7 / 6 | **3 (0–5)** | 2 (0–5) |
| **PAR `dist`** | **≥ 15/20** | 7 / 6 | 13 / 13 | **14 (12–17)**, PAR0 ≤ 3 | 15 (12–18), PAR0 ≤ 3 |
| muertes / CANAL-k1v0 | R6 ≤ 1.5× | — | — | **×1.0–1.8** | ×1.2–3.0 |
| `okU` | ≥ okU(k1v0) − 0.10 | — | — | −0.00 a −0.05 | −0.00 a −0.08 |

**Contrastes pareados dentro de la serie (lo que de verdad firmo, porque no dependen del nivel absoluto):**

1. **`CORTADO(BA) ≤ CORTADO(A1) − 2`** y **`VALOR(BA) ≤ VALOR(A1) − 3`** — la fuga de `exige_dir` es la base, no
   el mensaje. *Si esto falla, mi diagnóstico de §0.3 es falso y el candidato no tiene motivo.*
2. **`BAR-T(BA) ≤ 5`** en las dos series, y `BAR-T(BA) ≤ BAR-T(A1) − 3`.
3. **`dist(PAR)(BA) ≥ dist(PAR)(b5k3) + 5`** — el tipo VARIANTE aporta algo que la forma sola no puede.
4. **`dist(PAR)(BA) ≥ dist(PAR0)(BA) + 5`** (R5 del bloque 6).

**LA MISIÓN, con mi probabilidad honesta escrita antes de los datos:** `BAR-T ≤ 5` **Y** `PAR ≥ 15` en las dos
series. Le doy **~70 %** a que `BAR-T ≤ 5` pase en las dos, **~35 %** a que `PAR ≥ 15` pase en las dos, y
**~25 %** a las dos juntas con `BA`; **~40 %** con `BA-v`; **~50 %** a que lo consiga alguna de las dos celdas.
**El que se queda en el borde es PAR, no BAR-T** — igual que le pasó a A, y lo digo antes de verlo.

**Diagnóstico de mecanismo que predigo y que ya se mide** (`canal_lee_ref` en el paso de la entrega, para el
referente): en `CANAL` **valor > 0 con 3/3 de FORMA y 3/3 de VARIANTE**; en `BAR-T` y `VALOR` **valor ≤ −3 con
3/3 de FORMA** (la forma manda y dice veneno); en `BAR-H` **3/3 de FORMA con valor +R cuando la VARIANTE está
incompleta** y **valor negativo cuando está completa** — ése es exactamente el filo del candidato y por eso va
la ablación `BA-v` en la misma serie.

## 6. Control que puede fallar (y lo digo antes)

- **`CORTADO` y `VALOR` no bajan respecto de A1.** Entonces la base de A1 no era `exige_dir` y el diagnóstico
  entero de §0.3 es falso: el candidato pierde su razón de ser aunque los demás números salgan.
- **`BA` ≡ `BA-v`** (la ablación no difiere): el tipo VARIANTE nunca está incompleto en la serie y la regla (2)
  es inerte — entonces `BA` es sólo "A1 sin `exige_dir` con puerta de forma" y hay que decirlo así.
- **`b5k3` y `b6suf` en la misma serie** tienen que reproducir sus números de 821–860 dentro de ±4. Si no, el
  instrumento o el montaje cambiaron y **no se lee ningún veredicto** (regla 14 y ERR-38: dos organismos
  distintos con filas idénticas, o líneas base que se mueven, son señal de instrumento).
- **R6 (muertes, `okU`)**: el candidato habla más que A1, así que debería morir menos, no más. Si muere más,
  la puerta de seguridad lo mata como mató a k = 5.

## 7. Qué me refuta (declarado ahora)

1. **`BAR-T > 5/20` en `BA`** en cualquiera de las dos series → la conjunción de FORMA no basta para la
   familia cuando hay un segundo tipo leyendo, y §1 es falsa.
2. **`CORTADO(BA) > CORTADO(A1) − 2`** → §0.3 falso (ver §6).
3. **`dist(PAR)(BA) < dist(PAR)(b5k3) + 5`** → el tipo VARIANTE no aporta referencia de variante; lo que A
   medía era otra cosa.
4. **`CANAL < 15/20`** → la conjunción de forma es demasiado exigente y mata el canal. Se mira `fam1` (P-I5) y
   `canal_lee_ref` antes de culpar al mecanismo.
5. **Todo baja a la vez, `CANAL` incluido** → no hay referencia: hay un organismo que dejó de leer la tabla.
   Lo distinguen el gemelo `CORTADO` y las celdas `b5k3`/`b6suf` de la misma serie.
6. **R6 cae** → el candidato muere por coste.

Nada de esto se recalibra después de ver datos. Un cambio de umbral, brazo, mecanismo o criterio exige
preregistro nuevo, semillas nuevas y ERR numerado.

## 8. Las cuatro trampas, revisadas (regla 5 de EQUIPO.md)

1. **Canal simétrico.** No lo es y se comprueba: el emisor es b4b bit a bit y **no cambia** entre celdas; el
   receptor no ve al emisor (el mensaje entra como `(t, ref, P, R)`); `CORTADO` (gemelo mudo) y `PAR0` son los
   controles de simetría, y `BAR-H`/`BAR-T`/`VALOR` prueban que el contenido del campo de referencia importa.
   El arnés incluye `CANAL ≠ CORTADO`, `HERMANA ≠ CANAL` y `OTRO TOKEN ≠ CANAL` como controles que DEBEN diferir.
2. **Acierto sin balancear.** No hay "acierto": la medida es binaria y **pareada** — mordió o no en su primera
   exposición de la vida al referente — y su línea base es el gemelo mudo de **la misma celda**, corrido con el
   mismo prefijo exacto (P-I3). La misión se lee en absoluto (≤ 5, ≥ 15) **y** en la letra relativa del bloque
   6 (≤ CORTADO + 3 / + 5); se reportan las dos.
3. **Mundo que se come la comida.** El mundo es el de familias del bloque 1/2, **importado y no recopiado**,
   con `renov=1.0` y deriva; el muestreo no lo fija el candidato. El coste se vigila con `muertes` y `okU`
   (R6), que son puerta y pueden matar al candidato.
4. **Sitios fijos que se memorizan.** P-I4 exige que la **primera exposición de la vida** al referente sea la
   de después de la entrega (y excluye la semilla si no); los patrones se regeneran con `fam_seed` por semilla;
   el brazo `OTRO` usa otro mundo. El candidato no añade ningún sitio ni índice fijo: la dirección la calcula
   `_dir_var` de la retina presente, como en el bloque 6.

---

## 9. HUMO — resultado (§0–§8 NO se tocaron)

### 9.0 Identidad: **56/56** (`identidad_ba_salida.txt`, un proceso, semillas 1–3, 405 s)
Apagado ≡ `organismo_familias_a1` bit a bit en 16 casos (8 mundos × (k, sufijo)) **y con las cinco
configuraciones de lectura de A encendidas** (A1, A1-d, A1-c, A1-e, `dentro='min'`+`pesos_tipo`), con el canal
en sus tres modos y a T = 120 000 sin consumir rng; cadena ≡ b6 ≡ b5 ≡ b4b ≡ `organismo_familias` ≡
**`organismo_v14` (TRONCO)** ≡ `v15f_on`; inercia sin tabla; **la regla reimplementada FUERA coincide con
`W_tabla` en los 32 estímulos**; las tres reglas comparadas **sobre la misma tabla**; 8 perillas mal escritas
que lanzan; 7 controles que DEBEN diferir, todos 2/2 o 3/3.

**Dato del arnés que fija el diagnóstico de §0.3, y no es conducta:** sobre la misma tabla, `exige_dir` (A1)
hace callar a la tabla en **16 de 32** estímulos en las tres semillas, y **las 16 son por el tipo VARIANTE: el
tipo FORMA nunca estaba incompleto**. Con la regla de BA la tabla habla en 32/32. Ahí está, medido, el origen
de `CORTADO` 4 y `VALOR` 7 de A1.

**HALLAZGO COLATERAL (candidato a ERR, para el coordinador):** la perilla **`dentro` del instrumento del
creador A es código muerto** — `_DMv` se calcula y **no se usa en ninguna parte** (una sola aparición en el
fuente, su definición; comprobado también en la copia BA, que la hereda sin tocarla). A la reportó como
*"predicción propia medida INERTE: las ganadoras de un mismo tipo no discrepan entre sí"*. Lo que está medido
es que **la perilla no está conectada**, no esa propiedad del mecanismo. No afecta a ningún resultado de la
junta (`dentro` no entra en ningún candidato), pero la lección sí: *una perilla que sale idéntica en TODOS los
casos hay que mirarla en el fuente antes de llamarla inerte*. Caso `(s4)` del arnés.

### 9.1 Coste declarado (regla 3)
UN proceso, sin `Pool`. **1 semilla (911) × (1 emisor + 5 brazos) = 6 corridas de 100 000 pasos**, 44.6 s de
pared — dentro del presupuesto de un creador (≤ 6 corridas, ≤ 200 000 pasos); el runner **se para** si el plan
se pasa. Semilla 911: fuera de 821–900 (las series) y de 901–903 (el humo de la junta). Había otro proceso
python ajeno vivo (alefast, pid 5024) y **no se tocó**.

### 9.2 Los números (`humo_ba_20260921_130458.log` / `.json`, crudo `96d61e26386a2041`)

Montaje: emisor 1/1 (`T1v2`, R = +1.0, t = 11 565, tras 16 exposiciones); **regla 14: 33 campos comunes,
IDÉNTICOS campo a campo con la entrada del bloque 6**; entrega en t = 66 700 en los cinco brazos; la boca leyó
la vía **LENTA** en las 5 corridas (P-I5 limpio); `abstiene` 0/32 en las cinco.

`LEE(ref)` = qué lee la tabla **para el referente** en el paso exacto de la entrega = `[valor, habla, exactas
de FORMA, exactas de VARIANTE]`:

| brazo | `LEE(ref)` | comió | esperado en §5 | |
|---|---|---|---|---|
| CANAL | **+3.0, 3/3, 3/3** | 1 | valor > 0 con 3/3 y 3/3 | ✔ |
| CORTADO (mudo) | **−9.0, 3/3, 3/3** | 0 | negativo | ✔ |
| **BAR-T** (otro token) | **−9.0, 3/3, 3/3** | 0 | ≤ −3 con 3/3 de FORMA | ✔ |
| **BAR-H** (hermana) | **+3.0, 3/3, 3/3** | **1** | negativo **cuando la VARIANTE está completa** | **✗ REFUTADO** |
| PAR | +3.0, 3/3, 3/3 · `dist` 0 | 1 | dist 1 | ✗ |

muertes 456–462 en los cinco brazos, `okU` 0.83–1.00. **La 911 es un mundo hambriento** (como la 902 y la 903
de la junta): con n = 1 y sin `b5k3` al lado, ese número **no dice nada** sobre R6.

### 9.3 PREDICCIÓN PROPIA REFUTADA (la declaro yo, antes de la serie)

Escribí en §5: *"en `BAR-H`, valor negativo cuando la VARIANTE está completa"*. **Es falso, y el mecanismo dice
por qué:** con la hermana, las **3/3** ganadoras de variante conocen su casilla y **aun así suman +3**. El
mensaje de la hermana alcanza los bins de FORMA (misma forma) y, donde no los alcanza (las mixtas de los px 9
y 11), la casilla guarda el **valor propio** del receptor para ese bin — y **ese valor propio es POSITIVO**,
porque una celda mixta agrupa por (un px de forma, un px de variante) y recoge la última recompensa de
cualquier token comido en ese bin, que casi siempre es comida. `min(+3, +3) = +3` → muerde.

**Es exactamente la lección que B ya había escrito y que yo no apliqué a fondo:** *"ningún combinador de
VALORES PROPIOS puede vetar al mensaje si el valor propio no lo contradice; lo que discrimina no es el valor,
es si el mensaje alcanzó la DIRECCIÓN de esa celda."* Las ganadoras mixtas densas **no** cambian la dirección
en la que el mensaje escribió para la forma; por eso pueden afinar la resolución (1/32, lo que A midió) y aun
así no vetar.

**Consecuencia, dicha antes de la serie y sin tocar ninguna predicción de §5:** espero que `BA` **pase** la
mitad de la misión que depende de la familia (`BAR-T`, `CORTADO`, `VALOR`, `CANAL`) y **falle** la que depende
de la variante (`BAR-H`, y con ella `PAR ≥ 15`). Bajo mi propia lectura del humo, la probabilidad que firmé en
§5 para la misión completa (~25 % con `BA`, ~40 % con `BA-v`) **es demasiado alta**; la dejo escrita tal cual
porque se firmó antes, y añado aquí mi estimación después del humo: **≈ 10 % `BA`, ≈ 15 % `BA-v`**. La serie
decide; la predicción de §5 es la que cuenta para juzgarme.

### 9.4 Lo que el humo deja señalado para el siguiente preregistro (NO entra en esta serie)

Si la serie confirma §9.3, el hueco queda descrito con precisión y con una sola frase: **la referencia de
FAMILIA se arregla con el combinador (la conjunción de B sobre las ganadoras densas de FORMA: BAR-T 2/20); la
referencia de VARIANTE sólo se puede arreglar con la DIRECCIÓN (el sufijo), porque ningún valor propio
disponible contradice al mensaje.** El candidato natural siguiente — que **no** se mete aquí porque no tiene
humo ni caso estructural propio y meterlo sería recalibrar tras ver datos — es la celda con
`memoria_variante=1` **sobre esta misma perilla** (`conj_tipo=1` + sufijo): el sufijo pone la variante en la
dirección de los dos tipos, y la conjunción POR TIPO con prioridad de forma evita el relevo a la lineal que le
costó a `k3v1j1` su `CORTADO` 4 y su `BAR-T` 7. Se escribe con su preregistro, su humo y semillas nuevas.

**Lo que el humo NO puede decir, dicho antes de que alguien lo lea mal:** con n = 1 y T = 100 000 no se
reproduce ninguna línea base (el bloque 6, B, C y A lo midieron los cuatro). Los `com` del humo **no son
evidencia** y no pre-validan ningún contraste. Lo que el humo sí decide es **el montaje** (P-I2/P-I3/P-I4, la
regla 14) y **el mecanismo** (`canal_lee_ref`).

---

## 10. EL COMANDO DE LA CONFIRMACIÓN (lo corre el coordinador; reglas 3 y 11)

```bat
cd C:\Users\User\Documents\PROYECTOS\JUACO\bundle
python -u experimentos/junta_fase5/BA/corre_familias_ba.py --serie --desde 861 --celdas b5k3,b6suf,A1,BA --pool 5
python -u experimentos/junta_fase5/BA/corre_familias_ba.py --serie --desde 881 --celdas b5k3,b6suf,A1,BA --pool 5
```

- Con la ablación dentro (recomendado si hay CPU): `--celdas b5k3,b6suf,A1,BA,BA-v` (5 celdas).
- **Coste por serie:** 20 emisores + celdas × 7 brazos × 20 semillas = **580** corridas con 4 celdas, **720**
  con 5, de 100 000 pasos. Con `Pool(5)`, ~15–20 min (4 celdas) y ~19–25 min (5), por la medida de las series
  de A (853 s y 806 s con 532 y 504 corridas).
- `--pool N` manda sobre `JUACO_POOL` (ERR-86; en PowerShell la variable de entorno no pasa al hijo).
- Escribe `serie_ba_s861-880_*_crudo.json` **antes** de cualquier análisis (ERR-54), el log desde el arranque
  (regla 10) con una línea cada 40 corridas, la comprobación **campo a campo** de la regla 14, P-I5 por brazo y
  la tabla con R1–R5 y la línea `MISION (BAR-T <= 5 Y PAR >= 15)` por celda.
- La serie **se para sola** antes de gastar una corrida si un sha de origen cambió o si la entrada difiere del
  bloque 6 en algo que no sea una perilla de celda.
