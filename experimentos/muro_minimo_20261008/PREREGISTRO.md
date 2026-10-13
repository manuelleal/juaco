# PREREGISTRO — MURO MÍNIMO (8-oct-2026; escrito ANTES de correr las semillas selladas)

Misión: llegar a la AGI por este camino. Este bloque es consolidación: demostrar que entendemos el muro **reconstruyéndolo a mano**.
La disección de HUMO (6-oct) dio necesidad por ablación: sin RECICLA, sin BANCO o sin CAP, 0/20. Falta la **suficiencia por
reconstrucción**.

## 1. Hipótesis
Si la lectura "el órgano del muro es una decisión de dos modos" es correcta, un carro escrito a mano desde O1 sin limpieza, que añada
**sólo** esa decisión (RECICLA + BANCO + CAP en su forma más simple; sin pizarra y sin nada más del código de HUMO), cruza el muro de
la pista con fundador no limpio como HUMO.

## 2. MINIMO (`programas/MINIMO.py`, sha12 `b9cfbb3bb7cb`; congelado antes del humo)
Parte de la raíz de la que partió HUMO (`openevolve_serie/raiz/programa_inicial.py`, sha 50b2fc3241da510e = O1 sin limpieza). En llano:
- **Lejos de criar** (alguna reserva bajo `rep_umbral`): prueba lo desconocido como la raíz y **limpia**: muerde una letra que ya sabe
  que no sube nada, para que el mundo reponga, siempre que el golpe no deje la reserva golpeada bajo PISO. Si no hay nada bueno ni nada
  por probar, va a la mala más cercana.
- **Cerca de criar** (las dos reservas sobre `rep_umbral`): no prueba ni limpia; sólo come lo que sirve.
- **En los dos modos** lo que sirve se come hasta el tope real de la reserva (1.5), no hasta `rep_umbral` + 0.25.

Diferencia contra la raíz (medida por `identidad.py`, líneas de código): **+27 / −16**, de las que +4/−1 son el docstring; 89 → 100
líneas. Dos parámetros numéricos tocados: **TOPE = 1.5** (reemplaza a MARGEN = 0.25; es el tope físico de la pista, no un ajuste) y
**PISO = 0.35** (nuevo; el valor es el RECICLA_SEGURO de HUMO, tomado sin probar otros). Memoria nueva: cero.

**Lo que MINIMO NO tiene de HUMO (declarado; si el bloque da NO, son los primeros sospechosos de "cuarta pieza"):**
1. la pizarra (SOBRA por la disección, pero quitarla le costó a HUMO 15 % y 35 % de los linajes);
2. el radio de banco: cerca de criar HUMO no persigue nada a más de 45 casillas (RADIO_BANCO) y castiga la distancia (D0_BANCO 0.6).
   La ablación KO_BANCO quitó esto **junto** con "no limpiar ni probar"; la disección no los separa. MINIMO deja sólo "no limpiar ni
   probar", que es lo que dice la lectura;
3. la utilidad de limpiar (RECIC_UTIL 0.6): en HUMO lo malo cercano compite por distancia con lo bueno lejano; en MINIMO limpiar es
   sólo el último recurso como blanco (igual muerde lo malo que le queda de paso);
4. la urgencia 1.3 sobre el umbral (MINIMO deja el 1.0 de la raíz).

No hizo falta una cuarta pieza para **escribir** la decisión; si hace falta para **cruzar**, lo dice este examen.

## 3. Instrumento, anclas e identidad
- `construye.py`: copia sin reemplazos, con sha fijado, `corre_carro.py` (el del examen grande: pista y juez sin tocar, fundador NO
  limpio, ERR-191; 9 copias del carro; pizarra=1, rep_acum=0, escala=1, mundo_n=None) y `evaluador.py` (sólo su filtro de reglas).
  Regla 14: la entrada de la corrida es la misma línea `P.run(...)` del origen, byte a byte (`construye.py --check`).
- `identidad.py`: el instrumento copiado reproduce bit a bit (todos los campos del JSON menos `seg`) O1 s883001, HUMO s276001 y el
  control sin limpieza s883001 ya registrados. Salida en `identidad_consola.txt` e `identidad_salida.json`.
- `corre_examen.py` se niega a correr si un sha o el filtro no coinciden, y fuera de `--humo` sólo acepta las tandas de §5.
- T 100 000. Brazos:

| brazo | qué es | papel |
|---|---|---|
| MINIMO | §2 | el candidato |
| HUMO | sha12 69fcfcb2473f | referencia |
| KO_PIZARRA | HUMO sin pizarra, sha12 965aaec1e366 (de la disección) | referencia justa, sólo descriptiva (ver §4, aviso) |
| O1 | sha 99436afa2715f028 | referencia y cordura |
| O1_SINLIMPIA | la raíz, sha12 50b2fc3241da | **control que debe fallar** |

## 4. LA LETRA (por tanda de 20 semillas; "con mayoría" = cruzan_real ≥ 5/9, del juez)
**Validez:**
- V1: 100/100 corridas.
- V2: shas y filtro de reglas (el script se niega a correr si no).
- V3: O1 con mayoría en ≥ 6/20 (dio 16 y 17).
- V4: HUMO con mayoría en ≥ 15/20 (dio 19 y 20).

**Control:** C1: O1_SINLIMPIA con mayoría en **≤ 3/20** (nulo esperado 0/20: la raíz dio 0/5 y el control 0/9 en cordura). Si C1 cae,
el muro no está en estas semillas y la tanda es NO SE LEE.

**Puertas:**
- **P1:** MINIMO con mayoría en **≥ 15/20** (el umbral de la letra del muro).
- **P2:** linajes que cruzan de MINIMO **≥ 85 %** de los de HUMO (suma de la tanda).

**Veredicto de una tanda:** NO SE LEE si falla V o C1 · **FUNCIONA** = P1 y P2 · **HAY ALGO MODESTO** = MINIMO con mayoría en ≥ 10/20
sin cumplir las dos puertas · **NO** = mayoría en < 10/20.
**Bloque:** se corren serie y réplica (0 USD); si coinciden vale ese veredicto, si no el menor.

**Aviso sobre P2 (dicho antes de correr, regla 15):** el propio HUMO sin pizarra cruzó 0.85 y 0.65 de los linajes de HUMO (67/79 y
54/83). MINIMO no tiene pizarra, así que P2 contra HUMO pide más de lo que dio la mejor reconstrucción posible sin pizarra en una de
dos tandas. Por eso entra KO_PIZARRA y se reporta **P2b = linajes de MINIMO ≥ 85 % de los de KO_PIZARRA**. P2b **no cambia el
veredicto**: la letra es la propuesta base del coordinador (P2 contra HUMO). Si el coordinador prefiere P2b como puerta, se cambia
antes del commit del preregistro, no después.

**Se reporta sin decidir:** pareado MINIMO contra HUMO, KO_PIZARRA y O1; medianas de R0 real, vida, mordidas malas, fracción de pasos sin
nada bueno en el mundo, fundadores tras t = 10 000.

## 5. Semillas (nuevas; grep del 8-oct: `2830[0-4][0-9]` no aparece como semilla en el repo, sólo como dígitos dentro de JSON de datos
de `juaco_eco`)
- Serie **283001–283020**. Réplica **283021–283040**.
- Humo (fuera del bloque, ya usadas por otros brazos, para tener referencia registrada): 276001 y 883001.

## 6. Predicciones (escritas antes del humo)
| # | predicción | p |
|---|---|---|
| M1 | P1: MINIMO con mayoría en ≥ 15/20 en la serie | 0.55 |
| M2 | P2: ≥ 85 % de los linajes de HUMO en la serie | 0.25 |
| M3 | P2b: ≥ 85 % de los linajes de KO_PIZARRA en la serie | 0.40 |
| M4 | C1: el control sin limpieza con mayoría en ≤ 3/20 (espero 0) | 0.97 |
| M5 | HUMO ≥ 18/20 y O1 entre 13 y 19 | 0.75 |
| M6 | mordidas malas de MINIMO (mediana) entre 5 000 y 13 000 (HUMO ~9 000) | 0.50 |
| M7 | MINIMO falla como KO_BANCO si falla: vida mediana > 10 000 y R0 < 0.5 | 0.15 |
| V | bloque FUNCIONA / MODESTO / NO / NO SE LEE | 0.15 / 0.45 / 0.35 / 0.05 |

Razón de la cautela: quité cuatro cosas de HUMO que la disección no midió por separado (§2). La que más temo es el radio de banco: en
un anillo de 360 casillas, un cuerpo que ya cría y sale a buscar comida a 150 pasos puede romper la racha de 500.

## 7. Las cuatro trampas
- Canal simétrico: no hay canal (MINIMO no escribe ni lee la pizarra; el runner reporta `escrituras`).
- Acierto sin balancear: la medida es mayoría de linajes por semilla, con un control que debe dar ~0.
- Mundo que se come la comida: **es el fenómeno** (el muro); se reporta la fracción de pasos sin nada bueno.
- Sitios fijos: los objetos reaparecen al azar; el carro no guarda posiciones.

## 8. Qué NO diría el resultado
- No es aprendizaje ni evolución ni selección: es **diseño explicado**, un carro de la clase de O1.
- FUNCIONA diría: "la decisión de dos modos, escrita a mano en ~25 líneas sobre O1 sin limpieza, basta para cruzar el muro con fundador
  no limpio ×2". No diría que es la única forma (O1 cruza con otra limpieza), ni que MINIMO sea mejor que O1 o que HUMO.
- NO diría: "las tres piezas en su forma más simple no bastan"; **no** diría que la lectura es falsa hasta separar las cuatro
  diferencias de §2 (bloque siguiente, preregistro nuevo, semillas nuevas). No se ajusta MINIMO sobre estas semillas.
- Nada de esto hace a MINIMO tronco ni candidato.

## 9. Costo y parada
0 USD de modelo. 100 corridas por tanda. No hay más tandas tras la réplica. Siguiente ERR libre: ERR-196.

## 10. Identidad y humo (añadido tras correrlos, 8-oct 14:50; §1–§9 no se tocaron y MINIMO no se ajustó)
- Identidad: O1 s883001, HUMO s276001 y O1_SINLIMPIA s883001 dan 33/33 campos iguales al registro (rng del mundo incluido).
- Humo de un proceso, T 100 000, MINIMO sha b9cfbb3bb7cb (`humo/`, `humo_consola.txt`):

| semilla | MINIMO cruzan | R0 real med | vida med | fund > 10k | mordidas malas | sin nada bueno | referencia registrada |
|---|---|---|---|---|---|---|---|
| 276001 | **4/9** (persisten 5) | 0.8966 | 1 815.5 | 18 | 6 982 | 0.197 | HUMO 9/9, O1 7/9 |
| 883001 | **7/9** (persisten 8) | 0.9655 | 2 556.0 | 1 | 7 154 | 0.179 | O1 5/9, sin limpieza 0/9 |

- Una semilla con mayoría y una sin ella (por un linaje). Las predicciones de §6 se dejan como están; M7 (falla como KO_BANCO) ya
  parece falsa: MINIMO cría y muere a ritmo normal.
- Tiempos en esta máquina (un proceso): MINIMO ~400 s, HUMO 211 s, O1 178 s, O1_SINLIMPIA 158 s. MINIMO es ~2× más lento que HUMO
  por cómo está escrito el bucle (no se toca: el sha está congelado). Una tanda de 100 corridas ≈ 2.1–2.6 h con pool 3.

Firmado: Claude (creador, sesión local), 8-oct-2026, antes de correr las selladas.

## 11. Nota del coordinador antes de lanzar (8-oct-2026, tras la auditoría; ningún dato de las semillas selladas visto)
- La letra de §3–§4 queda como estaba escrita antes del humo. P2 (≥ 85 % de los linajes de HUMO) sigue siendo puerta; P2b contra KO_PIZARRA es sólo descriptiva.
- Corrección de §4 (auditoría H-2): en la disección KO_PIZARRA cruzó 67/79 = 0.848 y 54/83 = 0.651 de los linajes de HUMO; habría fallado P2 en las dos tandas, no en una. No cambia la letra.
- Combinación de serie y réplica (auditoría H-3): orden FUNCIONA > MODESTO > NO; el bloque vale el menor de los dos. Si alguna tanda da NO SE LEE, el bloque es NO SE LEE y no se declara nada.
- Vocabulario (auditoría H-5): un FUNCIONA diría "un diseño de dos modos escrito a mano es suficiente para cruzar", no "entendemos el muro" sin más. No es aprendizaje ni evolución.
- Sellado: §1–§9, `MINIMO.py` (sha12 b9cfbb3bb7cb) y `corre_examen.py` (sha16 d202bd621d2eb4ba) son anteriores al humo según el creador; el auditor confirma las fechas de los dos archivos de código, no la de §1–§9 (no había commit). Este commit es el sello verificable.
