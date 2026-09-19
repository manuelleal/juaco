# PROPUESTA — CREADOR C, junta de la fase 5 (19-sep-2026). **La casilla que se divide**

**Misión (primero, siempre): llegar a la AGI por este camino.** Misión de esta junta: cerrar la fase 5 — una
tabla que refiera a la **familia Y a la variante** con `BAR-T ≤ 5/20` y `PAR ≥ 15/20` a la vez, sin subir la base
sin mensaje. Mi ángulo: **sistemas vivos y mente — crecimiento y jerarquía.**

Archivos (sólo en `experimentos/junta_fase5/C/`, sin git):

| archivo | sha256_16 | qué es |
|---|---|---|
| `organismo_familias_c1.py` | `6854bb683a610a68` | copia derivada de `organismo_familias_b6.py` (`b10cbd4ddd0c32a3`, sólo se leyó) + perilla `variante_hija` |
| `identidad_c1.py` | `56a64fd637b66c0b` | arnés de identidad — **61/61** |
| `corre_c1.py` | `a1349fb8bcd0babf` | humo (un proceso) **y** confirmación (`--serie`, con `Pool`, para el coordinador) |
| `PREREGISTRO_oreja.md` | — | candidato **aparte** (E-9, la puerta que se cierra con la competencia): escrito, **no corrido** |
| crudos | `c1_humo_s901-903_20260919_162332_crudo.json`, `c1_humo_s1-2_20260919_163853_crudo.json` | ERR-54: guardados antes del análisis |

Reproducir, exactamente:

```
python experimentos/junta_fase5/C/identidad_c1.py                              # 61/61, ~7.6 min
python experimentos/junta_fase5/C/corre_c1.py --T 100000 --desde 901 --n 3     # humo, ~9.7 min
python experimentos/junta_fase5/C/corre_c1.py --T 100000 --arnes               # diagnóstico en 1-2, ~7.8 min
python experimentos/junta_fase5/C/corre_c1.py --serie --desde 821 --T 100000   # CONFIRMACIÓN (coordinador)
python experimentos/junta_fase5/C/corre_c1.py --serie --desde 841 --T 100000   # réplica       (coordinador)
```

*(El sha de `corre_c1.py` dentro del crudo de 901–903 es `f1c89b2b3c277376`: la bandera `--arnes` se añadió
DESPUÉS de esa corrida y no toca ninguna medida. El instrumento es el mismo `6854bb683a610a68` en las dos.)*

---

## 1. El mecanismo — qué cambia en la tabla y en la lectura

**Diagnóstico de partida (mío, escrito antes de tocar código).** El bloque 6 no perdió la familia por culpa de
la firma de variante: la perdió por **dilución**. El sufijo uniforme parte las 4 casillas de *todas* las 66
celdas en 32 de golpe; cada subcasilla se visita 8 veces menos, y entonces las celdas que **sí** distinguen al
referente de otro token llegan a la lectura **sin datos y se abstienen**. La lectura de b5 es una *suma de las
casillas conocidas de las k ganadoras*: si las que discrepan se callan, **la única que filtra decide sola**. Eso
es BAR-T 5 → 11. Medido en el arnés, caso (w): cobertura de la ganadora **12/32 (37 %) con el sufijo uniforme**
contra **4/4 (100 %) con mi mecanismo**.

**La idea (crecimiento, no decreto).** La distinción de variante no se reparte por toda la tabla: **nace donde la
de familia falla**, casilla a casilla, con la misma regla local con la que nace una celda hija en el tronco
(v11: conflicto de signo contra un valor consolidado; B-5: `R = 0` bajo otra retina), un nivel más abajo. Y
**nace por fisión del valor**: las hijas heredan el valor de la madre, la madre no se mueve, y sólo la firma
presente se lleva el valor nuevo. Por eso la tabla gana resolución **sin perder densidad**: las celdas que
distinguen siguen teniendo qué decir, y siguen pudiendo votar en contra.

```python
def _escribir_c1(_g,_P,_R):   # el ÚNICO sitio donde cambia algo; la lectura sólo baja al nivel vigente
    _bh=_bin4(_g,_P); _fh=_fir_c1(_P)                      # bin de 2 bits (familia) y firma de variante
    if not _FIh[_g,_bh]:                                   # la casilla todavía NO se ha dividido
        _v0=float(_MMv[_g,_bh])
        if _MNv[_g,_bh]>=vh_ev and abs(_v0)>vh_umbral and (_v0*_R<0 or (desambiguar and _R==0)):
            _MFh[_g,_bh,:]=_v0; _NFh_n[_g,_bh,:]=_MNv[_g,_bh]; _FIh[_g,_bh]=True   # DIVISIÓN + FISIÓN DEL VALOR
        else:                                              # ...si no, es b5 literal (sobrescritura de R CRUDO)
            _MMv[_g,_bh]=_R if (_MNv[_g,_bh]==0 or mem_alfa>=1.0) else _MMv[_g,_bh]+mem_alfa*(_R-_MMv[_g,_bh])
            _MNv[_g,_bh]+=1; return
    _MFh[_g,_bh,_fh]=_R if (_NFh_n[_g,_bh,_fh]==0 or mem_alfa>=1.0) else \
        _MFh[_g,_bh,_fh]+mem_alfa*(_R-_MFh[_g,_bh,_fh])
    _NFh_n[_g,_bh,_fh]+=1

def _leer_c1(_g,_P):          # la boca lee el nivel VIGENTE: hija si esa casilla ya se dividió, madre si no
    _bh=_bin4(_g,_P)
    if _FIh[_g,_bh]:
        _fh=_fir_c1(_P)
        return (float(_MFh[_g,_bh,_fh]), True) if _NFh_n[_g,_bh,_fh]>0 else (0.0, False)
    return (float(_MMv[_g,_bh]), True) if _MNv[_g,_bh]>0 else (0.0, False)
```

Perillas: `variante_hija` (0/1, **default 0**), `vh_ev = 2` (escrituras mínimas: la sorpresa contradice una regla
**ya vista**), `vh_umbral = 0.2` (el umbral de consolidación de v11, el mismo número). `variante_hija=1` con
`memoria_variante=1` **lanza**: son dos mecanismos para el mismo cuello y se miden por separado.

**Reglas locales, sin trampa.** La firma se lee de la retina presente; la decisión de dividir usa sólo el valor
guardado en esa casilla, su conteo y la recompensa que llega. Sin estado compartido, sin gradiente, sin
supervisor, sin rng nuevo, sin señal nueva. No cambian el emisor, el canal, el mundo, la selección de la
ganadora `_MGv`, el error propio `_MEv`, la sobrescritura de R CRUDO, la vía lineal, la puerta, la boca ni el
consumo del rng.

## 2. Por qué debería dar familia Y variante

En la dirección (−) el referente `T1v2` es **comida dentro de una familia de veneno**. Entonces:

1. **Variante (PAR, BAR-H).** Las ganadoras son celdas de forma: su casilla en el bin de `T1v2` guarda el valor
   de la familia (−3). El mensaje llega con **+1** → contradice a la madre → **esa casilla se divide**: las 8
   hijas nacen con −3 y la hija de la firma de `v2` se queda con +1. El receptor ante `T1v2` lee **+1** (come);
   ante su hermana `T1v0` lee **−3** (no come). El mensaje sobre `sal rosa` no mueve la boca ante `sal`.
2. **Familia (BAR-T).** Un mensaje sobre **otro token** cae en el bin de *otro* token. Las ganadoras que
   distinguen los dos tokens leen, ante `T1v2`, su propia casilla — que **sigue conociendo su valor**, porque la
   hija heredó el de la madre — y **votan −3** contra el +1 de la que filtra. Es exactamente el voto que el
   sufijo uniforme del bloque 6 silenció.
3. **La base sin mensaje no sube.** Ojo, y lo digo contra mi propio relato: las mordidas propias **sí** dividen
   mucho (131–195 de las 264 casillas en el humo). Lo que mantiene la base baja no es dividir poco, es que
   **dividir no borra nada**: en el instante de la división la lectura de la boca es idéntica a la de antes
   (las hijas nacen con el valor de la madre), mientras que en el bloque 6 la misma casilla pasaba a estar
   vacía. Medido: `CORTADO` 0 y `VALOR` 0 en las 5 semillas, contra 2 y 2 (901–903) del sufijo uniforme.
4. **El cuerpo no se paga.** Medido: muertes 27–29 de mediana contra 42–462 (k3v0) y 18.5–51 (k3v1).

Medido en el arnés, **sin conducta** (caso (x), y sin pasar por el emisor, ERR-71): con la casilla dividida la
hermana **sale** de la dirección vigente del referente (grupo 1–3 de 32) y el referente sigue en la suya, en
3/3 semillas.

## 3. Qué ERR podría repetir, y cómo lo evito

| ERR | cómo lo podría repetir | qué hice |
|---|---|---|
| **ERR-46..49** (recalibrar la medida hasta que pase) | mover `vh_ev`/`vh_umbral` después de ver los brazos | los dos quedan **fijados** aquí (2 y 0.2, el umbral de v11) y sólo cambian con preregistro y semillas nuevas |
| **ERR-44** | declarar el mecanismo mirando la tabla | todo se lee de la **conducta de la boca** (`primera_b2`/`primera_b4`, la lectura de b4b importada) |
| **ERR-54** | un análisis que se cae y tumba el registro | el crudo se escribe **antes** del análisis; el análisis va en `try` |
| **ERR-64b** | arnés que pasa por vacuidad | 4 controles que **DEBEN** diferir, con ≥ 2/3 |
| **ERR-70 / ERR-71** | P-I4 todo-o-nada; el caso de la dirección pasando por el emisor | P-I4 por exclusión de semilla; el caso (x) construye el mensaje del catálogo, no del emisor |
| **ERR-31 / ERR-38 / ERR-41** | recopiar el mundo, o copiar perillas a medias | el mundo, el canal, el **emisor** (`B6R.emisor`, b4b bit a bit), la lectura de la boca y los brazos se **importan** del runner del bloque 6 |
| **ERR-52** | meter OTRO en P-I3 | OTRO no entra en el humo |
| lección del bloque 6 (*"midió bien la hermana y falló el otro token"*) | predecir sólo BAR-H | **BAR-T se mide siempre**, y es el número que más vigilo |
| **ERR-63** | el cruce cod0 del emisor | el emisor es el objeto del bloque 6, sin tocar |

## 4. Identidad (la nave): **61/61**

`variante_hija=0` ≡ `organismo_familias_b6` **bit a bit** en 12 configuraciones de mundo × k ∈ {1,3} × sufijo
∈ {0,1} (incluidos el mundo del bloque 4 emisor/receptor, `voraz`, `par_herm` y los **tres modos del canal**),
ancla de rng a **T = 120 000**, `== organismo_v14` (TRONCO) y `== organismo_v15f_on`; inercia con
`memoria_pares=None`; **8** formas de escribir mal la perilla que lanzan; el mecanismo **reimplementado fuera**
del organismo (fisión del valor y densidad, caso (v)); y **4 controles que DEBEN diferir** (K, C, H, T).
Log: `identidad_c1_salida.log`.

## 5. Humo — lo que se midió y lo que NO prueba

`com` = la boca mordió en su **primera exposición de la vida** al referente, tras la entrega. Un proceso, sin
Pool. **n ≤ 3: no es evidencia.** Las tres celdas corren pareadas en las mismas semillas.

**(a) Semillas 901–903, T = 100 000 (el humo de la nave), 63 corridas de brazo + 3 emisores:**

| celda | CANAL | CORTADO | BAR-H | BAR-T | VALOR | PAR `dist` | PAR0 | muertes | hijas | dir_k/32 | P-I5 (lenta) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `k3v0` (= b5 k=3, bit a bit) | 3/3 | 0 | 2 | 1 | 0 | 1 | 1 | 462 | — | 3 | **3/3** |
| `k3v1` (= b6 sufijo, bit a bit) | 3/3 | 2 | 3 | 3 | 2 | 2 | 2 | 51 | — | 4 | 2/3 |
| **`k3h1` (candidato)** | **1/3** | **0** | **0** | **1** | **0** | **2** | **0** | **29** | 177 | **1** | **1/3** |

**(b) Semillas del arnés 1–2 (las mismas que usó el humo del bloque 6, §9.1), declarado como desviación:**

| celda | CANAL | CORTADO | BAR-H | BAR-T | VALOR | PAR `dist` | PAR0 | muertes | P-I5 |
|---|---|---|---|---|---|---|---|---|---|
| `k3v0` | 2/2 | 0 | **0** | 0 | 0 | 1 | 0 | 42 | 2/2 |
| `k3v1` | 2/2 | 1 | 0 | 1 | 1 | 2 | 0 | 18.5 | 2/2 |
| **`k3h1`** | **2/2** | 0 | 1 | 1 | 0 | 1 | 0 | 27 | **2/2** |

**Lo que el humo SÍ dice.** (1) El montaje está sano: P-I3 (prefijo exacto del gemelo) **15/15 brazos en todas
las semillas**, P-I4 sin exclusiones, emisores 5/5. (2) El mecanismo hace lo que dice, **estructuralmente**: se
divide (131–195 casillas de 264), la hermana sale de la dirección del referente, y la cobertura de la ganadora
se mantiene en 4/4 contra 12/32 del sufijo. (3) **El cuerpo mejora mucho**: 29 muertes de mediana contra 462 de
la línea base en las mismas semillas (R6 sobra por diez).

**Lo que el humo NO dice, y hay que decirlo.** (1) `BAR-H 0` y `BAR-T 1` en 901–903 son **en buena parte
vacuos**: en 2 de 3 semillas la boca leyó la vía **RÁPIDA** (P-I5 cayó), el mensaje quedó escrito y no
consultado, y entonces *todos* los brazos dan 0 — incluido CANAL, que se hunde a 1/3. (2) Igual que en el humo
del bloque 6, **la línea base no se reproduce con n ≤ 3**: `k3v0` da BAR-H 0/2 en las semillas del arnés cuando
la serie midió 13–14/20. El humo sirve para montaje, coste y mecanismo; **no puede pre-validar el contraste**.

**El hallazgo del humo (y es un resultado, no un fallo).** Rastreé la caída de P-I5 en las mismas semillas: mi
tabla acierta más → la boca se contradice menos → hay **menos divisiones de Kenyon** (49 celdas contra 65) → el
código del referente deja de cambiar y acumula evidencia → `puerta_pat` lo declara **familiar** → la boca
consulta la vía rápida y **el mensaje no se lee**. Dicho como principio: *el organismo que aprende mejor el
mundo deja de escuchar*. En las semillas del arnés (1, 2) la vía lenta se mantiene 2/2 en las tres celdas, y
901–902 son mundos donde la línea base muere 936 y 457 veces; así que **no está demostrado** que sea una
propiedad de mi mecanismo — queda como **riesgo declarado** de la serie, y afecta a cualquier candidato que
mejore la vía lenta, no sólo al mío.

**Predictor del mecanismo** (foto al final de la vida del gemelo mudo, declarada como aproximación): el valor
**grueso** de las k ganadoras en el bin del referente es el de la familia (−3) en **12 de 15** celdas-semilla, y
la ganadora comparte bin entre referente y hermana en **13 de 15** (E-8 otra vez). Donde una ganadora ya vale
+1, el mensaje se filtra igual que en b5: eso **acota** cuánto puede bajar BAR-H, y por eso no predigo 0.

## 6. Predicción numérica para 821–860 (celda `k3h1`, mediana y rango sobre 20, en **cada** serie)

| brazo | `k3v0` (referencia medida) | `k3v1` (referencia medida) | **`k3h1` (predigo)** |
|---|---|---|---|
| CANAL | 19 · 17 | 20 · 15 | **17 (15–19)** |
| CORTADO | 0 · 0 | 6 · 4 | **1 (0–3)** |
| BAR-H | 13 · 14 | 6 · 5 | **4 (1–7)** |
| **BAR-T** | 5 · 4 | 11 · 10 | **4 (2–6)** |
| VALOR | 2 · 1 | 4 · 4 | **2 (0–4)** |
| PAR `dist` | 12 · 9 | 15 · 15 | **15 (13–18)** / PAR0 2 |
| muertes (mediana) | 44.5 · 36.5 (bloque 5, k=3) | 45 (predicha en el bloque 6; no publicada) | **35 (25–55)** |
| P-I5 (vía lenta) | 18–20/20 | 18–20/20 | **17 (14–20)** ← el riesgo |

**En una frase:** *la casilla que se divide baja la hermana como el sufijo (BAR-H ≤ 7, PAR ≥ 13) **sin** soltar
al otro token (BAR-T ≤ 6) ni subir la base (CORTADO ≤ 3), porque las celdas que distinguen conservan su valor y
pueden votar.* Contraste medible: **BAR-T(k3h1) ≤ BAR-T(k3v1) − 5** y **PAR(k3h1) ≥ PAR(k3v0) + 3**, las dos en
las dos series. **Qué me refuta:** (i) BAR-T > CORTADO + 3 → la densidad no era la causa del techo del bloque 6
y mi diagnóstico es falso; (ii) BAR-H > CORTADO + 5 con P-I5 sano → la división no llega a las ganadoras (mirar
el predictor del §5: cuántas valían +1); (iii) CANAL < 15/20 con P-I5 sano → la fisión del valor ahoga al
mensaje bajo el valor heredado de la madre; (iv) P-I5 < 18/20 → el candidato mejora el cuerpo y cierra la oreja,
y eso es un resultado del que hay que hablar antes de medir nada más.

## 6-bis. Decisiones del coordinador (19-sep, después del humo) y lo que cambian aquí

1. **P-I5 se queda tal cual**, leída como puerta de **validez** y no de calidad: la semilla vacua (la boca leyó
   la vía rápida; el mensaje quedó escrito y no consultado) **no mide nada**, sale del numerador **y** del
   denominador de **todos** los brazos de esa celda, y se **declara** (cuántas y cuáles), con el **mismo trato
   para la línea base**. Implementado en `corre_c1.py` (`veredicto`: `PI5_por_semilla`, `vacuas_PI5`,
   `validas_por_celda`, `n_comun`) y escrito en `UMBRALES` **antes** de correr. Se reportan las dos lecturas,
   declaradas ahora: **PRINCIPAL** = exclusión por celda (la ruta depende de la vida entera del receptor, así
   que la validez es del montaje de *esa* celda); **SECUNDARIA** = la intersección de semillas válidas en las
   tres celdas, que es la comparación pareada. Los umbrales del bloque 6 se leen como fracción de las válidas:
   `≥ 15/20 → ceil(0.75 n)`, `≤ 5/20 → floor(0.25 n)`, márgenes +3 y +5 sin cambio.
2. **"La oreja" queda como candidato aparte**, con preregistro propio y **sin correr** hasta que C1 esté
   confirmada: `experimentos/junta_fase5/C/PREREGISTRO_oreja.md` (mecanismo exacto en código, identidad
   exigida, predicción numérica, seis refutadores, semillas 861–880 / 881–900). No toca C1 ni una línea, y su
   refutador (6) dice en voz alta cuál es el mejor desenlace: **si C1 pasa O-C sin oreja, la oreja sobra por
   Occam y no se corre nunca.**
3. **Mi hallazgo, convertido en predicción cuantitativa y medible en la misma corrida** (escrita **antes** de
   821–860; vive en `UMBRALES['V1']` y `['V2']` del runner):

   | predicción | umbral | me refuta |
   |---|---|---|
   | **V1** — semillas vacuas por P-I5 | `k3h1` **6/20 (3–11)** contra `k3v0` **1/20 (0–2)** y `k3v1` **2/20 (0–4)**; el contraste que decide: **vacuas(k3h1) − vacuas(k3v0) ≥ +3 en las DOS series** | contraste `≤ +1` en cualquiera de las dos → mi cadena causal (mejor tabla → menos divisiones → código estable → puerta cerrada) es **falsa** |
   | **V2** — el mecanismo de esa vacuidad | en `k3h1`, la mediana de **celdas de Kenyon** de las semillas **vacuas** es **menor** que la de las válidas, en las dos series | igual o mayor → la vacuidad no viene de que el código se estabilice, y hay que buscar otra causa |

   Si V1 pasa, el precio de mi candidato queda **cuantificado** (≈ 6 de 20 semillas no miden) y ése es el
   argumento exacto para abrir o no el bloque de la oreja. Si V1 cae y C1 pasa O-C, mejor: sale barato.

## 7. El comando de la confirmación (lo corre el coordinador)

```
python experimentos/junta_fase5/C/corre_c1.py --serie --desde 821 --T 100000     # serie
python experimentos/junta_fase5/C/corre_c1.py --serie --desde 841 --T 100000     # réplica
```

- Comprobación **en seco** antes de gastar CPU (no simula nada: verifica shas de origen y el plan) —
  `python experimentos/junta_fase5/C/corre_c1.py --serie --desde 821 --plan`. Es lo único que he corrido de
  este modo; devuelve 0 y los tres shas de origen en OK.
- Por serie: guarda de identidad **9 casos × 3 semillas = 27** tareas (P-I1; (K), (C) y (H) **deben** diferir,
  ERR-64b ≥ 2/3; el arnés completo sigue siendo `identidad_c1.py`, 61/61) + **20 emisores** + **540 corridas**
  de brazo (3 celdas × 9 brazos × 20) de 100 000 pasos.
- `Pool(14)` fijado en el script (`N_PARALELO`); el `Pool` es suyo (regla 3). Medido en mi humo: 8–10 s por
  corrida de 100 000 pasos en un proceso → **~8–12 min de pared por serie** (identidad ~2–3 min + brazos ~6–8
  min), **~20 min las dos**. Vía barata si hace falta: quitar `'k3v1'` del dict `CELDAS` deja 360 corridas
  (~6–8 min), pero **recomiendo las tres**: tener las dos líneas base en las mismas semillas es lo que hizo
  legible el humo, y `k3v1` es la única forma de medir BAR-T de b6 y el mío con el mismo mundo y el mismo emisor.
- Salidas en `experimentos/junta_fase5/C/`: `c1_serie_s821-840_<stamp>.log`, `..._crudo.json` (ERR-54: escrito
  **antes** del análisis, el análisis va en `try`) y `..._<stamp>.json` con el veredicto. El log imprime, en
  orden: shas y origen verificado, identidad caso a caso, emisores (P-I2), receptores, **las semillas vacuas
  por celda con sus números**, la tabla PRINCIPAL, la tabla SECUNDARIA y el resultado de V1/V2.
- El instrumento no cambia entre las dos series: `organismo_familias_c1.py` = `6854bb683a610a68` (el mismo del
  humo). `corre_c1.py` = `a1349fb8bcd0babf`; los crudos del humo llevan `f1c89b2b3c277376`, que es este mismo
  runner **antes** de añadirle el modo `--serie` y la letra: lo declaro, y el instrumento medido es idéntico en
  las tres corridas.

## 8. Preguntas al coordinador (las dos primeras ya contestadas el 19-sep)

1. ~~P-I5~~ — **contestada**: puerta de validez, exclusión por semilla declarada, mismo trato para la línea
   base. Implementada y escrita antes de correr (§6-bis).
2. ~~La oreja~~ — **contestada**: candidato aparte, preregistro escrito, **no se corre** hasta confirmar C1.
3. **Coste de la serie.** Las tres celdas (540 corridas) o sólo `k3v0` + `k3h1` (360). Mi recomendación, con su
   razón, está en el §7; la decisión es suya y el cambio es una línea del dict `CELDAS`.
4. **Desviación declarada:** usé las semillas **1 y 2** (las del arnés, y las que usó el humo del bloque 6 en su
   §9.1) para un diagnóstico completo de brazos, porque el humo de 901–903 dejó **una sola** semilla utilizable
   por P-I5. Lo declaro en vez de esconderlo: ¿lo da por bueno, o quiere que en el registro conste el humo sólo
   con 901–903 (y entonces con n = 1 utilizable)?
5. **`vh_ev` y `vh_umbral`** quedan fijados en 2 y 0.2 (el umbral de v11). ¿Los congela así para la serie, o
   quiere un brazo con `vh_ev` mayor (menos divisiones, más conservador) como control de Occam? Si lo quiere,
   entra como celda nueva **antes** de correr, no después.

---

## Resumen en 10 líneas

1. Mi diagnóstico del bloque 6: no fue la firma, fue la **dilución** — el sufijo uniforme dejó sin datos a las
   celdas que sí distinguen, y una sola celda con fuga decidió sola. Por eso BAR-T subió de 5 a 11.
2. Mi mecanismo: **la casilla se divide** por conflicto de signo (la regla de v11 y de B-5, un nivel más abajo),
   sólo donde la familia falla, y **las hijas nacen con el valor de la madre** (fisión del valor).
3. Así la tabla gana resolución de variante **sin perder densidad**: las celdas que distinguen siguen votando.
4. Identidad: **61/61** — con la perilla apagada es `organismo_familias_b6` bit a bit, y por su cadena el TRONCO.
5. Estructura medida: la hermana **sale** de la dirección del referente; cobertura de la ganadora 4/4 contra
   12/32 del sufijo uniforme.
6. Cuerpo: **29 muertes** de mediana contra 462 de la línea base en las mismas semillas; R6 sobra por diez.
7. Humo (901–903, n = 3, **no es evidencia**): CANAL 1/3, CORTADO 0, BAR-H 0, BAR-T 1, VALOR 0, PAR 2/PAR0 0.
8. Y el hallazgo honesto: en 2/3 semillas la boca leyó la **vía rápida** — el mensaje se escribió y no se
   consultó, así que esos ceros son **vacuos**. Causa rastreada: mi tabla acierta más → menos divisiones de
   Kenyon → el código se estabiliza → la puerta lo declara familiar. *El que aprende mejor deja de escuchar.*
9. En las semillas del arnés (1, 2) la vía lenta aguanta 2/2 en las tres celdas: el riesgo está declarado, no
   demostrado. Predigo para 821–860: **BAR-T 4 (2–6) y PAR 15 (13–18) a la vez**, CORTADO 1, CANAL 17.
10. Resueltas las decisiones del coordinador: P-I5 se queda como puerta de **validez** (semillas vacuas
    excluidas y declaradas, mismo trato para la línea base); el hallazgo va ahora como predicción falsable en la
    misma corrida (**V1: vacuas(k3h1) − vacuas(k3v0) ≥ +3**; **V2**: las vacuas tienen menos celdas de Kenyon);
    "la oreja" queda escrita en `PREREGISTRO_oreja.md` y **no se corre**; y la confirmación es
    `corre_c1.py --serie --desde 821` y `--desde 841`, ~8–12 min por serie con `Pool(14)`.
