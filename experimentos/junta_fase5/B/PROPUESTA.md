# PROPUESTA — CREADOR B (representación y computación) — junta de la fase 5, ronda 1

**Misión de fondo:** llegar a la AGI por este camino. **Hoy:** que el mensaje refiera a la **FAMILIA Y a la
VARIANTE** con la misma tabla — `BAR-T ≤ 5/20` **y** `PAR ≥ 15/20` a la vez, sin subir la base sin mensaje.

**Candidato en una frase:** *la tabla de pares ya guarda las dos referencias — la forma en el bin de cada par y
la variante en la firma de 3 píxeles —; lo que había que cambiar no es la tabla, es el **combinador**: leer las
k celdas como una **CONJUNCIÓN** (todas deben conocer su dirección) en vez de como la suma de las que saben.*

| | archivo | sha256(16) |
|---|---|---|
| constructor por anclas | `experimentos/junta_fase5/B/construye_familias_jb.py` | `ee017b4511a8eb38` |
| instrumento | `experimentos/junta_fase5/B/organismo_familias_jb.py` | `312a68054dbae7f6` |
| arnés de identidad — **88/88** | `experimentos/junta_fase5/B/identidad_familias_jb.py` | `b577f6925af1a655` |
| runner de la serie (coordinador) | `experimentos/junta_fase5/B/corre_jb_serie.py` | `61c0f82379206205` |
| runner del humo | `experimentos/junta_fase5/B/corre_jb_humo.py` | `8a1b0ec9e7cd30f4` |
| origen (sólo lectura) | `experimentos/nivel12_mundo_familias/organismo_familias_b6.py` | `b10cbd4ddd0c32a3` |

---

## 1. El diagnóstico (de los datos del registro, no de una intuición)

El registro dice *"con 4 casillas por par no caben familia y variante a la vez"*. **Los datos dicen otra cosa, y
es una cosa de computación, no de capacidad:**

| | BAR-T | BAR-H | PAR | CORTADO |
|---|---|---|---|---|
| bloque 5 (k = 3, sin sufijo) | **5/20 · 4/18** | 13/20 · 14/18 | 12/20 · 9/18 | **0/20 · 0/18** |
| bloque 6 (k = 3, con sufijo) | 11/20 · 10/18 | **6/20 · 5/18** | **15/20 · 15/18** | 6/20 · 4/18 |

El sufijo hace bien su trabajo (es lo único que puede separar a las hermanas: difieren sólo en los píxeles 9 y
11). Lo que rompió no fue la dirección, fue la **densidad**: con 4 → 32 subcasillas la tabla propia se vuelve 8×
más dispersa y `mem_cobertura` cae de 3.5/4 (88 %) a ~11/32 (34 %), como el propio preregistro del bloque 6
midió en su humo. Mi arnés lo vuelve a medir, ahora sobre **la misma tabla** y con las tres reglas de lectura
(caso (z), semillas 1–3, mundo del receptor, T = 20 000): con la regla de b6, **16 de los 32 estímulos caen en
abstención**; la mitad del mundo deja de tener voz en la lectura.

Y aquí está el mecanismo exacto del daño: la lectura de b5/b6 es
`suma de las casillas CONOCIDAS de las k celdas, abstención si ninguna conoce`. **Eso es una DISYUNCIÓN.** En b5
las celdas que el mensaje no alcanzaba **conocían** su casilla y contestaban su valor propio (negativo): la suma
era un **voto** y la fuga quedaba en minoría. En b6 esas mismas celdas **abstienen** — aportan 0 — y la única
celda que el mensaje alcanzó por azar **decide sola**. Por eso BAR-T sube de 5 a 11 y la base de 0 a 4–6.

> **La referencia del mensaje nunca la fijó el ancho de la dirección: la fija el combinador.** Con disyunción, la
> referencia es la **unión** de las k direcciones (por eso arrastra); con conjunción, es la **intersección**.

## 2. El mecanismo (qué cambia en la lectura, en código)

Una perilla, `mem_conj` (default 0 = `organismo_familias_b6` bit a bit), y **una línea** dentro de
`_tabla_v15f`, la función que ya existía:

```python
    def _tabla_v15f(P):
        _tk=_topk_leer(); _sv=0.0; _nv=0
        for _g5 in _tk:
            _v5,_k5=_lee_celda(_g5,P)
            if _k5: _sv+=_v5; _nv+=1
        if _CJv: return (_sv, True) if _nv==len(_tk) else (0.0, False)   # JB: CONJUNCION
        return (_sv, True) if _nv else (0.0, False)                      # b6: DISYUNCION
```

Si **una** de las k celdas no conoce su dirección, la vía lenta **no contesta** y releva a la lineal — que es
exactamente el relevo que el organismo ya tiene para *"no conozco esta combinación"*, aplicado a la **tupla
entera** en vez de a cada celda por separado. **No cambia una sola línea de la escritura**, ni el mundo, ni el
canal, ni el emisor, ni `_dir_var`, ni la ganadora `_MGv` y su desempate, ni el error propio `_MEv`, ni la
sobrescritura de R CRUDO, ni la lineal, ni la puerta, ni la boca, ni **el consumo del rng**.

## 3. Por qué debería dar familia Y variante

El mensaje escribe en cada celda `g` la subcasilla `(bin_g(P_msg), firma(P_msg))`; la boca lee, para el
referente, `(bin_g(T1v2), firma(v2))`. Con la conjunción, el mensaje sólo cuenta si alcanzó **las k**
direcciones, o sea si el referente está en la **intersección**:

```
   intersección de los bins de FORMA   = LA FAMILIA (el token y sus 3 variantes)     4/32   <- lo que dio k = 3
   intersección con la firma de 3 px   = LA VARIANTE (los *v2 de los 8 tokens)       8/32   <- lo que dio el sufijo
   las dos a la vez                    = 4/32 ∩ 8/32                                 1/32   = EL REFERENTE SOLO
```

Ése es el **código factorizado** que pedía el encargo, y no hace falta más tabla: la FORMA ya vive en el bin de
cada par y la VARIANTE en la firma. **La tupla de las k direcciones ES el código compuesto**; lo que faltaba era
leerlo como intersección. Arma por arma (probe = el referente `T1v2` siempre):

| brazo | el mensaje alcanza… | con conjunción |
|---|---|---|
| CANAL | las k (escribió el patrón del referente) | contesta **+R** → muerde |
| BAR-H (hermana `T1v0`) | ninguna: otra firma | la subcasilla del referente la conoce el propio receptor (familia = veneno) → **negativo**, o abstiene |
| BAR-T (otro token `T3v2`) | sólo donde además coincide el bin | falta al menos una → **abstiene** y releva a la lineal |
| VALOR (ceros) | ninguna | abstiene |
| CORTADO (mudo) | — | lo de b5: la base no sube |
| PAR | `T1v2` las k; `T1v0` ninguna | muerde una y no la otra → `dist` |

## 4. Qué ERR podría repetir mi idea, y cómo lo evito (exoesqueleto §1)

| ERR | riesgo concreto en mi propuesta | qué hago |
|---|---|---|
| **ERR-31** | recopiar el mundo/la letra en vez de importarlos, y leer umbrales de otro sitio | el runner **importa los objetos** de `corre_familias_b5/b4b` (mundo, canal, brazos, `lee_b4`); el instrumento se genera **por anclas** desde b6 con tripwire de sha |
| **ERR-38 / 41 / 42** | una copia por anclas que pierde un parámetro (`eta_s`) o apunta al origen equivocado | el constructor aborta si el sha del origen cambia, y tiene **postcondiciones**: la escritura intacta, `rng.` con el mismo recuento, `_dir_var` y el bin de b4b en su sitio |
| **ERR-44** | medir pesos o tabla en vez de conducta | todo brazo es `com` = **la boca mordió en su primera exposición de la vida** al referente (`primera_b2`/`primera_b4`); la tabla sólo aparece como diagnóstico |
| **ERR-46 / 47 / 48 / 49** | recalibrar la medida hasta que pase | umbrales y refutadores escritos **aquí**, antes de la serie; §6 y §7 |
| **ERR-54** | un análisis que se cae tumba la serie | el runner **guarda el crudo antes de analizar**, corrida a corrida |
| **ERR-64b** | un arnés que pasa por vacuidad | 9 controles que **DEBEN** diferir, con ≥ 2 de 3 semillas |
| **ERR-70** | P-I4 como puerta todo-o-nada | exclusión por semilla, y se reporta cuántas |
| **ERR-71** | comprobar el mecanismo **a través del emisor** (una semilla sin mensaje tumba una guarda de instrumento) | la estructura se comprueba sobre la tabla y el catálogo; el montaje se comprueba aparte |
| **ERR-25 / P-I5** | confundir "no aprendido" con "cancelado" — y, aquí, **"no consultado"** | se reporta `fam1` por semilla (ver §5 y §8, pregunta 3) |
| **bitácora: "medir BAR-T siempre"** | el error del creador del bloque 6: acertó en la hermana y falló en el otro token | BAR-T es el brazo que decide en §6, junto con PAR |

**Y el que ya me mordió, registrado en la bitácora:** mis dos primeras ideas (relevo marginal; dos canales con
relevo por conflicto) cayeron en el humo, las dos por la misma raíz — **ningún agregado ni combinador de
*valores propios* puede vetar al mensaje**: la marginal del bin hereda la subcasilla que el mensaje acaba de
sobrescribir, y el canal de variante, ciego a la forma, tenía valor propio *positivo* para el referente. Lo que
discrimina no es el valor: es **si el mensaje alcanzó la dirección**. La conjunción pregunta exactamente eso.
Las dos perillas refutadas se quedan en el instrumento **como controles** (`mem_marginal`, `mem_canales`).

## 5. Humo — **NO ES EVIDENCIA** (3 semillas de 901–910, T = 30 000, un proceso)

Reproducible con un comando:

```bash
cd C:/Users/User/Documents/PROYECTOS/JUACO/bundle
python experimentos/junta_fase5/B/construye_familias_jb.py        # instrumento por anclas
python experimentos/junta_fase5/B/identidad_familias_jb.py        # identidad
python experimentos/junta_fase5/B/corre_jb_humo.py --T 30000 --semillas 901,902,903
```

Celdas: `k<k>v<sufijo>m<marginal>c<canales>j<conjunción>`. `k3v0m0c0j0` **es b5 bit a bit** y `k3v1m0c0j0` **es
b6 bit a bit** (identidad comprobada), así que la tabla se lee como un factorial dentro de la misma serie.
Montaje: **P-I2 3/3** (los tres emisores avisan de `T1v2` con R = +1), **P-I3 OK** en todas las celdas (cada
brazo comparte el prefijo exacto con su gemelo hasta la entrega), **P-I4 3/3** utilizables.

| brazo | k3v0 (**= b5**) | k3v1 (**= b6**) | **k3v1j1 (CANDIDATO)** | k3v0j1 (conj. sin sufijo) | k3v1m1 (marginal, refutada) |
|---|---|---|---|---|---|
| CANAL | 3/3 | 3/3 | **2/3** (la 3.ª: `fam1 = 1`, P-I5) | 3/3 | 2/3 |
| CORTADO (mudo) | 0/3 | 0/3 | 1/3 | 1/3 | 0/3 |
| BAR-H (hermana) | 3/3 | 0/3 | **0/3** | 1/3 | 2/3 |
| **BAR-T (otro token)** | 2/3 | 2/3 | **0/3** | 1/3 | 1/3 |
| VALOR (sin referencia) | 0/3 | 0/3 | **0/3** | 1/3 | 1/3 |
| PAR `dist` / PAR0 `dist` | 3/3 · 1/3 | 3/3 · 0/3 | **3/3 · 1/3** | 3/3 · 2/3 | 3/3 · 1/3 |
| muertes (mediana) | 296 | 11 | **17** | 14 | 14 |
| okU | 0.722 | 0.778 | **0.778** | 0.722 | 0.778 |

**Precio medido donde más importa:** con la regla de b6, en el mundo del receptor, **16 de 32 estímulos
abstienen**; el candidato exige aún más (las k exactas), así que su coste para el cuerpo es el riesgo real y va
en R6 y en el refutador 3.

**Lo que el humo SÍ decide — el mecanismo, no la conducta.** `canal_lee_post`: qué lee la vía lenta **para el
referente**, en el paso de la entrega (mediana de 3 semillas; `ex` = cuántas de las k contestan exacto):

| brazo | k3v0 (= b5) | k3v1 (= b6) | **k3v1j1 (candidato)** |
|---|---|---|---|
| CANAL | +3.00 ex3/3 | +3.00 ex3/3 | **+3.00 ex3/3** |
| BAR-H | −1.00 ex3/3 | −1.00 ex3/3 | **−9.00 ex3/3** |
| **BAR-T** | **+2.00** ex3/3 | **+2.00** ex3/3 | **−1.00 ex3/3** |
| VALOR | −5.00 ex3/3 | −5.00 ex3/3 | −1.00 ex3/3 |

Ahí está el bloque 6 entero en una fila: con la disyunción, el mensaje de **otro token** deja la lectura del
referente en **+2.00** (y la boca muerde); con la conjunción, en **−1.00**. En las semillas sueltas se ve aún
más crudo: BAR-T y VALOR quedan con **0 de 3 celdas exactas** → la vía lenta abstiene y releva a la lineal.

**Lo que el humo NO puede decir, dicho antes de que alguien lo lea mal:** a T = 30 000 y n = 3 **no reproduce las
líneas base** (b5 da `dist(PAR)` 3/3 donde la serie dio 12/20, y BAR-T 2/3 donde dio 5/20). Los `com` de arriba
**no son evidencia** y no pre-validan ningún contraste: eso lo decide la serie del coordinador.

**Una advertencia honesta:** la única semilla en que CANAL no muerde (902) tiene `fam1 = 1` — el receptor ya leía
por la vía **rápida** y el mensaje quedó escrito y no consultado. Es **P-I5**, el punto ciego conocido del
bloque 4b. El creador C acaba de escribir en la bitácora que su candidato **cayó entero por ahí** (P-I5 2/3), y
su diagnóstico es general: *un candidato que mejora la vía lenta hace que el organismo se contradiga menos, y la
puerta de familiaridad lo declara FAMILIAR antes*. **Mi candidato empuja en la dirección contraria** (la
conjunción hace que la vía lenta conteste **menos**, no más), pero el riesgo es real y compartido: pido que
P-I5 se mida por brazo y se reporte, no que se dé por hecho (§8, pregunta 3).

## 5 bis. PARA EL COORDINADOR — el comando exacto de la confirmación

Runner de la serie: `experimentos/junta_fase5/B/corre_jb_serie.py` (sha `61c0f82379206205`). **Pool configurable**: variable
de entorno `JUACO_POOL` (default 6) y bandera `--pool N`, que gana sobre la variable. Nada más hay que tocar.

```bat
cd C:\Users\User\Documents\PROYECTOS\JUACO\bundle
set JUACO_POOL=6
python experimentos/junta_fase5/B/corre_jb_serie.py --desde 821
python experimentos/junta_fase5/B/corre_jb_serie.py --desde 841
```

- **Coste por serie:** 20 emisores + 4 celdas × 7 brazos × 20 semillas = **580 corridas** de 100 000 pasos.
- **Tiempo estimado (pared):** medí ~4.3 s por corrida a T = 30 000 con la máquina cargada → ~14 s a T = 100 000.
  **Pool(5) ≈ 27 min · Pool(6) ≈ 23 min · Pool(12) ≈ 11 min.** Con `JUACO_POOL=5` o `6` no debería haber
  BrokenPipe: el Pool se abre una sola vez y los crudos los escribe **el proceso padre** tras cada resultado.
- **Salida:** `datos/jb_serie_s821-840_<stamp>_crudo.json` (se escribe **corrida a corrida**, ERR-54), la tabla
  de brazos de las 4 celdas, P-I2/P-I3/P-I4 con sus exclusiones, **P-I5 por brazo** (semillas con `fam1 = 1`) y
  el veredicto contra la letra de §6, calculado por el propio runner.
- Probado de punta a punta (`--desde 901 --n 2 --T 30000 --celdas k3v1m0c0j1`, Pool(3), 36.5 s): emisores, Pool,
  crudos, puertas, tabla y veredicto. **No gasta ninguna semilla de 821–860.**
- Si se cae a mitad, el crudo ya tiene todo lo corrido: el análisis se rehace sin repetir la serie.

## 6. Predicción numérica para 821–860 (escrita antes de la serie)

**Lo que la junta pide, en una línea, y lo firmo: `BAR-T ≤ 5/20` Y `PAR ≥ 15/20` A LA VEZ, en las dos series.**
Con los márgenes del bloque 6 al lado, para que se vea de dónde tiene que moverse cada número:

| | hoy k3 sin sufijo (b5) | hoy k3 con sufijo (b6) | **predicción k3v1j1 (candidato)** | criterio |
|---|---|---|---|---|
| **BAR-T** | 5/20 · 4/18 ✓ | **11/20 · 10/18 ✗** | **2/20** (rango 0–5) | ≤ 5/20 |
| **PAR `dist`** | **12/20 · 9/18 ✗** | 15/20 · 15/18 ✓ | **15/20** (rango 13–18) | ≥ 15/20 |

O sea: **el BAR-T de b5 con el PAR de b6**, en la misma celda y en las dos series. Contrastes pareados dentro de
la serie: `BAR-T(j1) ≤ BAR-T(j0) − 6` y `dist(PAR)(j1) ≥ dist(PAR)(j0) − 2`.


Celda del candidato: **k = 3 + sufijo + conjunción** (`k_ganadoras=3, memoria_variante=1, mem_conj=1`), en
**cada una** de las dos series de 20, dirección (−) sola (ERR-53), con las exclusiones de P-I2 y P-I4:

| brazo | criterio de la junta | predicción (mediana / rango) |
|---|---|---|
| CANAL | ≥ 15/20 | **16** (14–19) |
| CORTADO (mudo) | ≤ 5/20 | **1** (0–3) |
| BAR-H (hermana) | ≤ 5/20 | **2** (0–5) |
| **BAR-T (otro token)** | **≤ 5/20** | **2** (0–5) |
| VALOR | ≤ 5/20 | **2** (0–4) |
| **PAR `dist`** | **≥ 15/20** | **15** (13–18), con PAR0 ≤ 3 |
| muertes | ≤ 1.5 × CANAL-k1v0 | ×1.0–1.4 |
| `okU` | ≥ okU(k1v0) − 0.10 | −0.00 a −0.05 |

**Contrastes medibles, no sólo niveles:** `BAR-T(k3v1j1) ≤ BAR-T(k3v1j0) − 6` (de 10–11 a ≤ 4–5) y
`BAR-H(k3v1j1) ≤ 5` y `dist(PAR)` **no baja** respecto de `k3v1j0` (± 2). Diagnóstico que predigo y que ya se
mide: en BAR-T y VALOR, **0 de las 3 celdas exactas** para el referente en la mayoría de semillas.

**Brazos que pido en la serie (2 × 2, no sólo el candidato):** `k3v1j0` (= b6, la línea base de variante),
`k3v1j1` (candidato), `k3v0j0` (= b5, la línea base de familia) y `k3v0j1` (**conjunción SIN sufijo**: el control
que demuestra que el sufijo sigue haciendo falta — predigo BAR-H alto, 10–16/20, porque la familia entera
comparte los bins de forma). Sin ese control, un BAR-H bajo no se puede atribuir al sufijo.

## 7. Qué me refuta (declarado ahora)

1. **`BAR-T > 5/20` en `k3v1j1`** en cualquiera de las dos series → la disyunción no era la causa; el voto no era
   el problema y el diagnóstico de §1 es falso.
2. **`CANAL < 15/20`** → la conjunción es demasiado exigente y mata el canal. Se mira antes de culpar al
   mecanismo: `fam1` (P-I5: escrito y no consultado) y cuántas de las k contestan exacto en el brazo CANAL. Si
   `fam1` explica las caídas, es montaje; si no, el candidato muere.
3. **`CORTADO > 5/20` o R6 cae** → el precio de abstener más lo paga el cuerpo: el organismo se queda sin tabla
   para vivir. Es el riesgo real de este candidato y lo digo antes.
4. **`dist(PAR) < 15/20`** → la conjunción rompió lo que el sufijo había ganado.
5. **Todo baja a la vez, CANAL incluido** → no hay referencia: hay un organismo que dejó de leer la tabla. Lo
   distinguen el gemelo CORTADO y las celdas `j0` de la misma serie.

## 8. Preguntas al coordinador (decisiones de método/criterio, no las adivino)

1. **¿Cuenta como "una tabla que codifica familia Y variante"?** El cierre del 18-sep pedía *"dos ganadoras de
   distinto tipo (forma + variante), sumadas"*. Lo medí (`mem_canales`) y **no funciona**: sumar canales no veta
   nada (bitácora). Mi candidato cumple el criterio **numérico** de la junta por otro camino (una sola lista de
   k celdas, leída como conjunción). ¿Se acepta el mecanismo por el criterio, o hay que probar además la forma
   literal "dos ganadoras de distinto tipo"?
2. **¿Contra quién se mide R6?** El bloque 6 lo medía contra `CANAL-k1v0`. En mis semillas de humo `k3v0` (b5)
   muere 296 veces y `k3v1` 11: la referencia importa mucho. ¿`k1v0` como en el bloque 6?
3. **P-I5 con un candidato que abstiene más.** ¿Se mantiene "la boca usa la vía LENTA en ≥ 18/20" tal cual?
   Con la conjunción, abstener **es** el mecanismo funcionando (releva a la lineal), y en el gemelo CORTADO va a
   abstener casi siempre. Propongo: P-I5 se mide **en el brazo CANAL** (donde el mensaje sí escribió) y se
   reporta por brazo; las semillas con `fam1 = 1` se **excluyen y se reportan**, como P-I2/P-I4 (ERR-70). Es una
   decisión de criterio y la pido por escrito **antes** de la serie, no después.
4. **¿Factorial o candidato solo?** Recomiendo el 2 × 2 de §6 (28 brazos por serie con los 7 brazos que uso);
   cuesta CPU pero deja el control del sufijo dentro de la misma serie.
5. **El instrumento lleva tres perillas nuevas** (una candidata y dos refutadas, todas inertes por defecto y con
   identidad bit a bit contra b6). ¿El auditor prefiere que la serie corra con este instrumento — con los
   controles dentro — o con uno reducido a `mem_conj`?

---

### Identidad — **88/88** (regla de la nave: antes de medir nada)

`python experimentos/junta_fase5/B/identidad_familias_jb.py` → salida completa en
`experimentos/junta_fase5/B/identidad_jb_salida.txt` (un proceso, semillas 1–3, 1 160 s de pared con otros dos
creadores corriendo a la vez: el tiempo está contaminado y se declara). Comprueba:

- **APAGADO**: con las tres perillas en 0, `jb` es `organismo_familias_b6` **bit a bit** — 7 mundos × k ∈ {1, 3}
  × sufijo ∈ {0, 1} (28 casos), los **tres modos del canal** con sufijo ON y OFF, y T = 120 000 **sin consumir
  rng**; y por su cadena, `b5` (con los tres modos del relevo), `b4b`, `organismo_v14` (**TRONCO**) y
  `organismo_v15f_on`.
- **INERTE donde debe serlo**: con `memoria_variante = 0`, `mem_marginal` no puede hacer nada en sus tres modos
  (la marginal de un bin de una subcasilla es ella misma); con `k_ganadoras = 1`, `mem_conj` no puede hacer nada
  (conjunción y disyunción coinciden); con `memoria_pares = None`, las tres son inertes.
- **ESTRUCTURA**: la lectura reimplementada **fuera** del organismo coincide con la de dentro estímulo a
  estímulo, la dirección exportada coincide con la recalculada fuera, y las tres reglas se comparan **sobre la
  misma tabla** (16/32 → 0/32 de abstención con el relevo; el candidato va en la otra dirección, por eso su
  precio hay que vigilarlo).
- **NO PASA POR VACUIDAD**: 9 formas de escribir mal una perilla **lanzan**, y **9 controles DEBEN diferir**
  (cada perilla cambia la corrida; CANAL ≠ CORTADO, ≠ HERMANA y ≠ OTRO TOKEN), con ≥ 2 de 3 semillas (ERR-64b).
- **MONTAJE**: P-I3 (prefijo exacto contra el gemelo) y P-I4 (el receptor nunca vio el referente antes de la
  entrega) en los tres modos; el mensaje es el **mismo objeto** que en b6 (el emisor no cambia); y el receptor
  **no ve al emisor** (ERR-71: la dirección se comprueba sin pasar por él).
