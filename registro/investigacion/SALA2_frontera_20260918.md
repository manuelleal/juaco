# SALA 2 — SÍNTESIS: QUÉ NOS BLOQUEA Y CÓMO LE DARÍA VIDA (18 sep 2026)

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales (sin backprop en el
runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada. **Primero llegar a la
frontera; segundo, que viva.**

**Sintetizador de la sala 2.** La sala corrió el 18 sep 09:40–10:10 (4 diagnósticos, 6 diseños, 12 refutadores); la síntesis
se cayó por límite de sesión y esto la repone.

**Reglas cumplidas.** No edité ningún archivo del repo: este es el único archivo que creé. No corrí el organismo, ningún
`Pool` ni ningún proceso. No hice commits. Todo número lleva su archivo y su entrada. Fuentes: los cuatro `DIAG_*.md` y los
seis `DISENO_*.md` de `registro/investigacion/sala2/`, las dos refutaciones escritas
(`REFUTACION_dos_escalas_medibilidad.md`, `REFUTACION_vivir_localidad.md`), los **ocho veredictos estructurados** de los
refutadores que sí terminaron (journal del workflow `wf_54e95359-0b2`), `CLAUDE.md` (bloque "Estado (día 7)" y la DECISIÓN
DEL DIRECTOR 09:55), `registro/CRITERIO_TRONCO_v2.md` (022059d98ee57bc8, borrador de las 09:58) y
`registro/REGISTRO_etapas_1_2.md` hasta la entrada "Candidato v15f" (10:00) y ERR-44 (10:05).

**Aviso de fecha que importa a la lectura.** Los cuatro diagnósticos se escribieron a las ~09:45 y **sólo conocían hasta
v15e**. A las 10:00 entró **v15f**, que cambia el diagnóstico A3 de abajo: es el primer organismo de la línea que generaliza,
se desdice, consolida **y** cruza XOR con 8 ejemplos en la configuración del tronco. Los diseños de las 09:54–10:03 lo
conocían a medias (sólo por su humo de 2 semillas), y dos refutaciones lo usaron para tumbarlos.

---

## A. QUÉ NOS BLOQUEA (consolidado de los cuatro diagnósticos)

Ordeno por importancia dentro de cada capa. La causa común de A1–A6 es una sola frase, y conviene decirla antes:
**el valor vive en direcciones compartidas con pérdida (3 celdas de 90 por patrón) y sólo se escribe al morder.** De ahí
salen, con la misma causa, el alias, las ~25 mordidas para asociar, el trilema de la memoria de un golpe, la retención 0.67
y la capacidad atada al pool (`DISENO_radical` §0, y las cuatro lentes coinciden).

### A-I. Capacidad (el organismo)

| # | bloqueo | número que lo sostiene | fuente |
|---|---|---|---|
| **A1** | **No existe el nodo: la identidad de un estímulo es "las celdas que comparte".** Lo más parecido a un token es `_key(kc)` (frozenset de 3 celdas en `ncod`): nace al morder, cuenta mordidas, no tiene valor propio ni aristas | "sal" → "sal rosa" por canje de un píxel comparte 0/1/2/3 celdas con p **0.17 / 0.49 / 0.31 / 0.03** (media 1.21 de 3 → hereda ~40 % del valor rápido, y por semilla 0 % o 100 %); por píxel añadido 0.03 / 0.29 / 0.53 / **0.143**; dos estímulos **sin ningún píxel común** comparten una celda el **26 %**. El Kenyon **no ordena vecinos**: similitud 0.000 / 0.000 / 0.333 contra 0.025 / 0.075 / 0.225 del HD (nh 2000, kh 40). 46–55 de 90 celdas activas sin valor legible | `DIAG_representacion` §1, B1; B-4 |
| **A2** | **El código colisiona por diseño (K = 3 de 90) y sólo el conflicto de signo separa.** Con `R = 0` la fisión no actúa | algún par con el mismo código en **18/200** semillas con 4 estímulos (9 %) y **170/200** con 20 patrones; **135/200** con fuga exacta test→train (291 fugas, 115 de valencia opuesta) → parte de lo que mide `bateria_generaliza` es alias. Bloque de la sal: \|W[sal]\| **1.45** contra 0.0, veneno **−1.45** contra −3.0, evitación **×7**, exposiciones 3 835 contra 545, **0 divisiones**. **B-5 lo repara 18/18** (sal 0.0, veneno −3.0, muertes 41 contra 75/77) y es **inerte en el tronco** (examen 8/8, generalización 40/40 idénticos) — y **no está en el tronco** | `DIAG_representacion` B2; `DIAG_dinamica` B5; REGISTRO 08:16, 09:07, 09:12 |
| **A3** | **El canje del estimador: escribir de un golpe ↔ desdecirse ↔ identificar.** *Roto a las 10:00, después de los diagnósticos* | v15d: xor01 0.875 y G1 1.000 **pero E2 0/20 y E1 0/20** (no se desdice, mata de mordidas a la rápida: lee 1.45·R). v15e: **E2 20/20, E1 W_B 20/20, G1 1.000** pero xor01 **0.500** (el residuo hereda el fracaso de la lineal; gana (2,4)). **v15f (10:00): G1 1.000 (azar 0.500) / G2 0.998 (azar 0.549) / K 20/20; E2 reversión 20/20; E1 W_B ≈ −3 20/20; xor01 estricta 1.000 contra 0.500 apagado, gana (0,1) 20/20.** Cae por dos subletras internas del examen (E1 "veneno Q4 < Q1" **17/20**; E2I `W_C ≤ −2.5` **17/20**) y por coste (splits **+16 %**, celdas +7.8 %) | `DIAG_dinamica` B1; REGISTRO 08:38, 09:37, **10:00** |
| **A4** | **La conducta la gobierna la vía más lenta (la puerta), y desaprender depende del hambre, no de la sorpresa** | relojes derivados del código: rápida **0.09** del error por mordida (≈ **24** mordidas al 90 %), lenta **0.45** (≈ **4**), tabla de un golpe **1.0** (1). `_fam` (código mordido ≥ 5 veces y ≥ 1 celda con \|Wb\| > 0.2) entrega la boca a la rápida desde la 5.ª mordida → **la conducta asocia en ≈ 25 mordidas digan lo que digan la lenta o la tabla**: E1 mordidas de B por cuarto, v15e [25.5, 10, 7, 7.5] contra v14.1 [27, 11, 8, 1]. Revertir de −3 a +1 exige muestreo bajo hambre (pb **0.025** con hambre 1; 9·10⁻⁴ con 0.5): **2 000–10 000 pasos**; dE5 lo baja a **0.248–0.267×** (20/20 ×2) y espera desde las 04:47 | `DIAG_dinamica` §1.1–1.2, B2 |
| **A5** | **La estructura sólo nace por conflicto, nunca por novedad.** La fisión exige `Wb[c]·R < 0`; un patrón nuevo lee 3 proyecciones ya existentes | duplicar el pool a 180 **no devuelve nada** (el techo es la evidencia por código, no el pool); `P0·P1` es el par más propuesto por la fisión en **0/20**; aprender `KW` no mejora la generalización (3K, día 3) | `DIAG_representacion` B5; `DIAG_dinamica` B5 |
| **A6** | **Retención de lo ausente 0.67: el valor vive en celdas compartidas y no hay segunda constante de tiempo** | mundo largo 0.67 (0.50 con mapa); A-2 (metaplasticidad por masa de conflicto) **refutada**: 0.667 = base, recupera más lento, **+73 % muertes** | `DIAG_dinamica` B4 |
| **A7** | **Sin morder no hay nada.** Todo aprendizaje está bajo `if mordio:` | **5 740** encuentros con veneno por corrida sin efecto; C-P5 refutado; C-P6 nulo (SOLO_R 0.986); N2 cerrado con **dos** mundos (INNATO 60 contra 278). Lo único "sin morder" que cruza es la **conducta ajena** (N1: 7–8 mordidas contra 19; N3d 0.811–0.822) | `DIAG_metodo` bloqueo 2; `DIAG_mundo` bloqueo 5 |

### A-II. Mundo y medida

| # | bloqueo | número | fuente |
|---|---|---|---|
| **M1** | **El mundo de 6 px ya no puede hacer la pregunta siguiente.** Identificabilidad y alias son **el mismo teorema** | con 8 patrones, **9 de 15** rasgos conjuntivos ajustan con residuo 0 y sólo 1 generaliza (gradiente exacto 0.562, backprop 0.531, estadístico ideal 3/20, fisión 0/20); con **14**, queda 1 de 15 y la regla local llega a 1.000 (n\* 200). Alias: 9 % y 170/200 (arriba) | ERR-35; `DIAG_metodo` bloqueo 1 |
| **M2** | **El mundo es adversario a la herencia por parecido y no tiene grados** | el **único** par lo bastante parecido para heredar (sim 0.225) es **comida/veneno**: heredar **cuesta** (8 → 11–13 exposiciones) y contamina al padre (W_B de −2.97 a **−4.2/−5.5**, porque el préstamo cae en celdas). Con 6 px es alias total o sim 0: **no hay grados** | B-4; `DIAG_mundo` bloqueo 3 |
| **M3** | **Trampa 3: lo mordido desaparece, lo rechazado se queda** | veneno **6.3×** más encuentros que comida en la mini (5 253 contra 831) y **23×** en el ancla V14 (B 7 897.5 contra A 344.5); una semilla ALIAS visita la sal 3 835 veces contra 545. **Toda medida agregada sobre patrones es muestreo** | `DIAG_mundo` bloqueo 3 |
| **M4** | **La muerte no es muerte: el organismo es inmortal en memoria y el renacer es un recurso** | `if E<=0: deaths+=1; E=.6; pos=azar` conserva `Wp, Wn, KW, activa, Wps, Wns, ncod`. El regalo financia el **0.236** del presupuesto en E1 y el **0.457** en E2, y el **34–77 %** de las ventanas del bloque 2 de reproducción. Sobre un inmortal, "sobrevive" no puede ser resultado y "se reproduce" tampoco | `DIAG_mundo` bloqueo 1 |
| **M5** | **Un cero no veta y el impulso tapa el valor: el "propósito" es una lectura, no una conducta** | `Vb = 1.2·W + 2·déficit + 0.5`: con `W = 0` y déficit 0, **pb = 0.841**; saciado, VIVO muerde la sal el **79.7 %**. CUELLO_MIN (mínimo de las dos filas, **sin memoria nueva**) lo lleva a 0.001 y el linaje al filo del reemplazo (**r +3 / −3** contra **−73 / −75** del tronco, 8/8 predicciones ×2) | `DIAG_mundo` bloqueo 4; REGISTRO 09:43/09:45 |
| **M6** | **La medida que manda (exposiciones hasta asociar) no está en ninguna batería del tronco** | V3 "n\*: no medible con los instrumentos de hoy" en v15c/v15d/v15e. Sólo la sala XOR (n\* 7–10 contra 200 contra > 600), B-4 (`exp_hasta` 16 contra 8) y el mundo vivo (`exp_tabla` 11) la reportan, **cada uno con su propia definición**. Es ERR-20 otra vez: lo que no está en una batería no protege ni ordena nada | `DIAG_metodo` bloqueo 5 |
| **M7** | **Sin población no hay señal que no sea la propia mordida, ni nada que transmitir** | N2 cerrado con dos mundos tras 6 diseños; N3d mudo 0.503 ("obedece, no enseña"); un cuerpo por corrida, el descendiente **se cuenta, no se instancia** ("qué se hereda: NADA") | `DIAG_mundo` bloqueos 2 y 5 |

### A-III. Método

| # | bloqueo | número | fuente |
|---|---|---|---|
| **T1** | **No hay regla de entrada al tronco: los candidatos se acumulan y cada uno vuelve a copiar todo** | esperando decisión del director: **dE5** (0.248×/0.267×, 20/20 ×2, se apaga 20/20, G1 0.80, examen 8/8), **B-5** (18/18, tronco idéntico), **A-3** (identidad algebraica 60/60, \|ΔW\| 3e−15). v15c/d/e/B-5 generaron ≈ **24 archivos copiados en 1 h 30** | `DIAG_metodo` bloqueo 3 |
| **T2** | **Instrumentos copiados: la tasa de ERR de instrumento supera a la de hallazgos** | la mañana: **11 bloques, 21 series, ≈ 3 200 corridas, 8 ERR (35–42), 0 entradas al tronco**; de los 8, **4 son instrumento copiado** (36, 38, 41, 42), 3 de medida/criterio, 1 de control, **0 del organismo**; + ERR-43 (regex voraz: el runner leyó `azar 20.000` y marcó NO con la batería en PASA). ERR-38 sostuvo un veredicto falso **38 min** y costó 160 corridas | `DIAG_metodo` §2.1–2.3 |
| **T3** | **20 semillas dan veredictos a ±1 y las réplicas comen el Pool; la letra mezcla "lo que mata" con "lo que reporta"** | v15e 19/20 ×2, **v15f 17/20 ×2**, v14 s117, B-5 C4 7/9 (y 4/9 en la réplica) | `DIAG_metodo` bloqueo 6 |
| **T4** | **El examen es ciego a la capacidad que manda y castiga al que aprende rápido** | un candidato que asocia en 1 mordida y otro en 24 **pasan igual**. **ERR-44 (10:05):** "veneno Q4 < Q1" **no puede distinguir "aprendió en una mordida" de "no aprendió"** — mató a v15f con E1 W_B 20/20 y E2 20/20 | `DIAG_dinamica` B3; REGISTRO 10:05 |

**Respuesta directa a "¿qué nos bloquea?"** (`DIAG_metodo` §4, y lo suscribo): los **instrumentos** bloquean el rendimiento, no
la verdad (ningún error entró al tronco; todos se cazaron); los **criterios** bloquean la lectura, no la verdad; **el tamaño
del mundo es el bloqueo principal**; y el **paradigma** bloquea en un punto preciso y pequeño — un solo canal de aprendizaje
(la boca) y un mundo que se come la comida —, **no** en "las reglas locales".

---

## B. LA HIPÓTESIS DEL DIRECTOR

> *"la tokenización y la representación de algo: si sal es sal será número uno, lo guardo, lo vectoriza; y después sal rosa lo
> vectoriza, marca como sal y lo plantea como una variable de lo mismo — eso es lenguaje. Ahora, si pensamos en el
> aprendizaje, y ya lo hemos visto, que puede aprender y desaprender."* (09:40) · *"la palabra es grafo, no vectorización."* (05:10)

Las cuatro lentes convergen en el mismo veredicto, y es fuerte: **la intuición describe con precisión lo que el organismo ya
hace a medias, y nombra exactamente lo que le falta.** Produjo además los dos resultados más limpios de las últimas horas
(M3 = tokenizar la combinación, el único mecanismo que cruzó XOR con 8 ejemplos; y el alias = "sal rosa marcada como sal" sin
control). **El organismo es un tokenizador con herencia por colisión; lo que le falta no es tokenizar, es gobernar la herencia.**

### B.1 Qué YA hace (medido, con la línea)

| frase | pieza del tronco v14.1 (`organismo/organismo_v14.py`, feefc88b1fd8d434) | ¿lo hace? | número |
|---|---|---|---|
| "sal es sal, número uno, lo guardo" | `code(P)` = top-3 de `KW@P` → `_key(kc)` = frozenset de 3 celdas; `ncod[clave]` cuenta mordidas del código **exacto**; `_ord` el orden de aparición | **a medias**: es una tabla de nodos **sin aristas**; nace al morder; no tiene valor propio | puerta por código: N\* 50.5 contra 35 |
| "lo vectoriza" | dos vectores: el código disperso (90 celdas, K = 3) y la lectura lineal de la retina `Wps−Wns ∈ ℝ⁶` | **sí**, dos veces | G1 **1.000** / G2 0.95–1.00; A-3: los dos canales son **un** vector con signo (60/60) |
| "sal rosa … marca como sal" | rápida: celdas compartidas · lenta: píxeles compartidos | **rápida: al azar** (hereda 0/33/67/100 % con p 0.17/0.49/0.31/0.03) · **lenta: por regla**, y sólo lineal | tabla de A1 |
| "…y es su enfermedad" | cuando el código coincide del todo, la sal **es** el veneno | **sí, medido** | \|W[sal]\| 1.45, veneno −1.45, evitación ×7 |
| "variable de lo mismo" | **fila por necesidad** del mundo vivo (mismo código, otra fila) | **sí para la variable interna**; **no** para un modificador del estímulo | xor necesidad × estímulo **1.0** contra 0.5 escalar (20/20 ×2); tabla 2×4 exacta en **11** exposiciones; barajar el contenido lo destruye (0.25) |
| "sal rosa **deja** de ser sal" | **B-5**: "cuando una celda con valor recibe **nada** bajo una retina distinta, **divide**". La condición `kj@P > KW[c]@P` **es** la prueba local de "misma cosa o no" | **sí, y es local** | 18/18 ALIAS: sal 0.0, veneno −3.0, evitación ×7 → ×1, muertes a la mitad; **tronco idéntico** |
| "tokenizar la combinación" | M3 / **v15f**: 15 celdas (una por par) × 4 casillas, R crudo, sobrescritura, relevo a la lineal, cada vía con su error | **sí, y es lo único que cruzó XOR con 8** | n\* **7–10**; v15f en el tronco: xor01 estricta **1.000** contra 0.500, gana (0,1) **20/20** |
| "aprender y desaprender" | regla delta en las dos vías; fisión por conflicto de signo | **sí** (E1/E2 20/20). La tabla de un golpe **sin sobrescribir no se desdice** (v15d E2 0/20); **con sobrescritura sí** (v15e/v15f, 1 mordida) | relojes de A4 |
| "grafo, no vectorización" | **nada**: la fisión guarda `split_t = (t, kk)` y **no** `padre[j] = c` | **no hay grafo** | — |
| "eso es lenguaje" | N1, N2, N3d | **no declarable** (regla 8) | N2 cerrado ×2 mundos; lo que transfiere es la **conducta** |

### B.2 Qué NO hace (y por qué importa)

1. **No hay aristas explícitas.** La única relación entre tokens es "comparten celdas", y esa relación **es** la
   interferencia (0.67) y el alias. Una arista se corta; una celda compartida no.
2. **No hay lectura por parentesco.** La hija de v11 hereda el valor **copiado** (un número, no una arista) y la de B-5
   hereda 0; después son independientes: si el mundo enseña algo nuevo a "sal", "sal rosa" no se entera.
3. **El valor no vive en el nodo** → interferencia y alias. El mundo vivo ya demostró la mitad de la cura: cuando el valor
   está **indexado** por lo correcto (una fila más), el XOR se disuelve en 11 exposiciones; en celdas compartidas, no.
4. **No hay grados de parecido en 6 px** (0.000 / 0.000 / 0.333) y el parecido **contradice** el valor en el mundo del tronco.
5. **Sin población no hay a quién transmitir** ni nada que no sea la propia mordida.

### B.3 Cómo se operacionaliza con reglas locales (cinco reglas; ninguna mira al futuro, ninguna usa gradiente)

1. **Nacimiento del nodo al VER, no al morder** (`pos in objs`), indexado por **(código, P)**: dos estímulos con el mismo
   código y retina distinta son **dos nodos** — el alias resuelto *en la lectura*; en las celdas sigue haciendo falta B-5.
2. **Arista "es variante de" por imagen** (L1 ≤ 2 en retinas binarias de peso 3 = "un movimiento"), **nunca por código**
   (B-4: el Kenyon no ordena vecinos; la cobertura por imagen es 100 % y por código 32 %). Nace **tentativa**.
3. **Lectura por relevo, con prioridad escrita:** valor propio consolidado → valor del padre por la arista → lo que hoy hace
   v14.1. **El préstamo nunca toca `Wp/Wn`** (prestar en celdas contaminó al padre: W_B −2.97 → −4.2/−5.5).
4. **Escritura al morder con R crudo y sobrescritura, cada vía con su error** (la lección exacta de v15d → v15e → v15f: R
   crudo identifica, la sobrescritura desdice, el error propio deja consolidar a la rápida).
5. **Corte** en la primera mordida que contradice a un padre **estable** (B-4: 1 mordida, 3/3); **confirmación** cuando la
   consecuencia concuerda. Eso es *aprender y desaprender a nivel de relación*, encima del que el tronco ya tiene.

**Cómo se mide** (y esto es la mitad del trabajo): `exp_asoc[k]` = exposiciones hasta signo correcto **y** \|v\| ≥ 0.5, por
patrón y por clase; `colateral` = mordidas de veneno en los **hermanos** tras la primera mordida de una excepción; `w_var` =
\|Wps−Wns\| en los píxeles de variable (¿queda la lenta limpia?); **ruta usada por visita** (exacto / nodo / arista / lenta);
y **el signo leído por la boca en la ÚLTIMA visita** de cada excepción — la medida que **ningún** diseño de la sala traía y
sin la cual "aprende en una" no distingue aprender de olvidar cuatro mordidas después.

### B.4 Dos advertencias que hay que decir antes de construir nada

- **La herencia de miedo se protege a sí misma.** Si "sal rosa" hereda −3, la boca la evita (pb 0.025 con hambre 1) y la
  corrección tarda ~100 encuentros (el bloque de la sal lo midió por otro camino: 3 835 exposiciones); si hereda +1 se
  corrige en 1 mordida. Es la misma asimetría (−3/+1, lo rechazado se queda) que cerró N2. **Por eso la hija de B-5 nace sin
  valor y por eso el grafo necesita el órgano de muestreo (dE5) como compañero, no como alternativa.**
- **En 6 px el grafo casi no compra.** El propio `DISENO_grafo_tokens` lo declara: la vía lenta ya acierta el **signo** de una
  variante nunca vista **10/10 a la primera**; el grafo sólo puede aportar **magnitud exacta** (\|v\| ≥ 0.5 en 10/10 contra
  6/10) "y eso apenas cambia la conducta". La hipótesis del director necesita **un mundo con familias**, no un órgano sobre
  el mundo viejo.

---

## C. SI FUERA MI CREACIÓN

### C.0 El veredicto honesto de la sala, primero

**Ninguna de las seis propuestas, tal como está escrita, sale de la frontera.** Los ocho refutadores que terminaron
**refutaron los cinco diseños que les tocaron**, y por motivos que no son de gusto:

| diseño | refutado por | motivo que lo tumba (el más duro) |
|---|---|---|
| `dos_escalas` (v15f + palabra consolidada + replay) | **medibilidad y localidad** | su puerta P1 **ya estaba caída** por la serie de v15f de las 10:00:43 (E1 17/20, E2I 17/20) que v16 hereda bit a bit en conducta; P4 exige ≥ 16/20 donde **el techo de información de sus propios rasgos da 15/20** en las semillas que eligió (LSQ exacto, 181–200); zonas muertas entre "pasa" y "refuta"; y P6 px0 está mal derivado (la consolidación **ocurrirá** en ~20/20, no en ≤ 3/20) |
| `vivir` (población, muerte real, herencia) | **medibilidad y localidad** | **calibrado con la mortalidad de otro mundo**: en el anillo del tronco un cuerpo con memoria completa logra **0.048–0.079 ventanas por vida** (registro: 124–159 muertes por 100 000; corrida del refutador: 5 ventanas en 63 vidas, **ninguna en la primera**) → R₀ ≪ 1, el fundador muere sin hijos, **P-V0 cae por el mundo y no por la herencia** y su cláusula cierra V1–V3. Además I5 e I6 del arnés **fallan por construcción** y los rng de los hijos **colisionan entre semillas vecinas** |
| `crece_codigo` (v16c) | **medibilidad y localidad** | la compuerta `_GE < _EL` con el nodo naciendo con el error **instantáneo** del padre en la sorpresa contra una **EMA**: **72–73 % de los reclutas nacen muertos** y la poda los mata en la 6.ª mordida sin haber leído nunca (E1: 2.72 contra 0.28) → §2.5 es falso, **el grafo es inerte en el tronco** y P7 8/8 saldría porque no pasa nada. Y P3 pone el umbral de paso en el **suelo estructural** (10 pares co-activos sólo en los venenos) y el de refutación en el **techo** (13): no decide |
| `mundo_grande` (mundo de familias 12 px + perilla `token`) | **medibilidad** (localidad **no terminó**) | **el órgano se apaga solo a la 6.ª mordida** (`_fam` se consulta **antes** de `_tok` y `ncod` cuenta toda mordida) y **ninguna medida lo ve**; P8 exige una identidad G1/G2 **falsa**; P2 pone el umbral (4) **dentro** del rango aritmético del propio efecto ([1, 9]). **Pero su refutador dice lo más importante: "lo que falla no es el mundo — la idea token + variante + excepción + cambio de familia es la que pidió el director — es la letra del preregistro y el órgano"** |
| `radical` (nodos por retina exacta) | **medibilidad** (localidad **no terminó**) | es una **caché episódica** (MFEC/NEC) con cinco capacidades declaradas "por construcción" y **tres predicciones cuya caída ya está pre-atribuida al instrumento**; preregistro con cifras de un humo corrido en la **semilla 101, que es la primera del examen 101–120**; y en el único mundo donde su grafo tiene aristas, **la clave exacta aliasa el 3.87 % por vista** sin ningún control que lo separe |
| `grafo_tokens` | **ninguna de las dos refutaciones terminó** | **no tiene veredicto, y eso no es un mérito** (§F.1). Su propio texto declara que en 6 px la lenta ya acierta el signo 10/10 y que el grafo sólo aporta magnitud |

Y los cinco refutados coinciden en **dos defectos comunes** que valen más que cualquiera de ellos por separado:

- **Cuatro de seis diseños se preregistran contra el criterio v1 que el director retiró a las 09:55**, usan pesos internos
  como puerta (prohibido por T-E) y no traen T-A, T-C, T-D ni T-G del criterio v2.
- **Cinco de seis miden en el mundo que la misma decisión declaró agotado** (6 px, 20 patrones), y cuatro meten la capacidad
  como **perilla diseñada a mano** contra el punto 3 del 09:55 ("ninguna capacidad nueva entra como perilla si puede entrar
  como crecimiento"). Con la lente de la sala: son la quinta, sexta y séptima **reparación** de la línea v15c→d→e→f, no una
  salida de la frontera.

### C.1 La línea elegida

**"El mundo que obliga a representar, y sobre él una estructura que crece" — el mundo de familias de `DISENO_mundo_grande`
desmembrado como manda el director: primero el mundo con v14.1 SIN cambios, después el órgano.**

No elijo un órgano: elijo **el orden**, porque la sala demuestra que el orden es el problema. Los cinco órganos propuestos se
refutan por la misma razón estructural — *un órgano medido en el mundo viejo o es inerte (crece_codigo, grafo_tokens en 6 px,
B-5) o es una tabla con otro índice (radical, mundo_grande, dos_escalas)*. Injertos de los otros diseños, cada uno con su
dueño:

- **de `DISENO_mundo_grande`**: el mundo (D = 12 = 9 de forma + 3 de variable; 8 tokens de peso 3; 3 variantes por token =
  32 estímulos; `n_exc` excepciones; deriva de la variante presente cada 5 000 pasos; cambio de familia en T/2) y sus mundos
  control (`lineal`, `azar`, `barajado`), y las medidas `tasa_tokeniza`, `w_var`, `colateral`, `exp_total`;
- **de `DISENO_grafo_tokens`**: los brazos que deciden (INV = propagación por la familia; FRONTERA = sin hermanos, predicción
  de **igualdad**; SIN_CORTE = control que debe fallar), la elección **estructural y previa** de la variante que cambia, y las
  capacidades C1–C5 (localizar el cambio, propagarlo, `exp_asoc`, no duplicar huella, aprender y desaprender la relación);
- **de `DIAG_mundo` (bloqueo 3)**: **renovación simétrica** — que lo rechazado también desaparezca a una tasa comparable. Sin
  esto, la trampa 3 (6.3× en la mini, **23×** en el ancla) hace de toda medida agregada un muestreo, y es el defecto que
  contaminó el mundo vivo, el bloque de la sal y la reproducción. **Es el único cambio de mundo que propongo y no tiene un
  solo número detrás** (§F.10);
- **de `DIAG_metodo` (bloqueo 1) y B-5**: escalar `NK`/`K` con `negativo_codigo.py` **antes de simular** hasta que el alias
  estructural caiga bajo 1 %. Con D = 12, 32 estímulos y NK = 30 el cálculo de la sala da **199/200 semillas con dos
  estímulos de código idéntico**: el mundo nuevo nacería con la enfermedad del viejo;
- **de `DISENO_crece_codigo`**: el reclutamiento por **sorpresa repetida en la misma pareja co-activa**, con la compuerta
  arreglada según sus dos refutaciones;
- **de `DISENO_radical`, `DIAG_representacion` §4.6 y v15f**: el nodo con valor propio, **R crudo + sobrescritura + relevo**,
  y el préstamo que nunca toca celdas;
- **de `DISENO_vivir`**: la población — al final, y sólo después de calibrar el mundo para que R₀ ≈ 1.

### C.2 Los bloques, en orden (llegar a la frontera = 0, 1, 2, 3 · que viva = 4)

---

#### **BLOQUE 0 — La regla del juego (método; coste ≈ 0 en ciencia)**

*No añade capacidad. Va primero porque sin él ningún candidato puede entrar POR lo que aporta, sólo a pesar del examen.*

| | |
|---|---|
| **qué** | (0a) la **geometría del código por mundo** en cada runner (`negativo_codigo.py`, 0.1 s): pares con el mismo código, pares con 2/3, fugas test→train, celdas con valor legible al final. (0b) **`bateria_exposiciones.py`**: UNA definición de `exp_hasta` (la de B-4), tres escenarios (veneno nuevo · comida nueva parecida al veneno · inversión), referencia fijada **sobre v14.1 antes de correr** (hoy 16 / 8 / ~2 000 pasos). (0c) baterías **parametrizadas** (`--modulo`, kwargs desde UN dict compartido) y runner que **copia el booleano** de la batería (lo que `corre_v15f.py` ya hace: se generaliza). (0d) **juzgar v15f con el criterio v2** completado (semillas ya asignadas: examen 121–140, mundo de regla 181–200, mundo vivo 301–320) |
| **capacidad nueva** | ninguna (es la regla del juego) |
| **predicción** | ninguna: (0a)–(0c) son instrumentos. (0d) sí: v15f cruza T-B, T-C y T-G y se decide en T-A y T-E |
| **controles** | la línea base de v14.1 en las tres etapas de (0b), congelada con su sha |
| **coste (Pool)** | (0a) 0 CPU · (0b) ~4 min una vez · (0c) 0 CPU, 2–3 h de implementador · (0d) ≈ 15 min + réplica |
| **qué lo mata** | nada: no hay hipótesis. El riesgo es no hacerlo — es ERR-20 otra vez, y ya volvió cuatro veces hoy |

---

#### **BLOQUE 1 — EL MUNDO QUE OBLIGA, con v14.1 SIN CAMBIOS (el control base que el director pidió)**

| | |
|---|---|
| **qué** | mundo de familias (arriba), peldaño 2 (cuerpo del mundo vivo: dos necesidades, `costo = costo_a = 0.001`), con **renovación simétrica** y `NK`/`K` escalados a alias < 1 %. **Un solo brazo de organismo: v14.1 tal cual**, en los cuatro mundos (`excepciones`, `lineal`, `azar`, `barajado`). 4 × 20 = 80 corridas, T = 100 000 |
| **capacidad nueva** | ninguna en el organismo. Lo que produce es **la línea base de T-A, T-F y T-G para ese mundo** — hoy inexistente, y sin ella cualquier umbral que escribiéramos sería inventado |
| **predicción clave (la que decide)** | **en `excepciones`, v14.1 paga cada excepción con la vía lenta y contamina a los hermanos**: `colateral` (mordidas de veneno en hermanos en los 10 000 pasos tras la primera mordida de cada excepción) **≥ 2 × el de `lineal`** (razón de medianas, A₁₂ ≥ 0.75), `w_var` **≥ 1.0** en `excepciones` contra **≤ 0.5** en `lineal`, y `exp_total` crece con el número de **estímulos**, no con tokens + excepciones. **Si v14.1 no se distingue de `lineal`, el mundo NO obliga**: se endurece (`n_exc` 4 → 8, una por token) **antes** de tocar el organismo, con ERR numerado |
| **controles** | `lineal` (donde la fuga por píxel basta: predicción nula), `azar` (sin familias), `barajado` (familias falsas por construcción), identidad (con D = 6 y A/B ≡ v14.1 **bit a bit**, 24/24; rng no consumido a T = 120 000), y el subconjunto estructural SEPARABLE/ALIAS/HUÉRFANA calculado **antes** |
| **coste (Pool)** | instrumento por anclas (la cadena `construye_capD.py` + `construye_vivo.py` ya existe): 1–2 h de implementador; 80–180 corridas ≈ **3 min** con `Pool(14)`; réplica igual |
| **qué lo mata** | (i) que el alias estructural no baje de 1 % con ningún `NK`/`K` razonable → la línea pasa **al código**, no al mundo; (ii) que v14.1 se comporte igual en `excepciones` y en `lineal` → el mundo no obliga; (iii) que con renovación simétrica el mundo mate tanto que nadie aprenda nada → se reporta y se baja la tasa **una** vez, con ERR |

---

#### **BLOQUE 2 — CRECIMIENTO POR SORPRESA REPETIDA, medido en el mundo del bloque 1**

| | |
|---|---|
| **qué** | `crece_codigo` con las **tres correcciones exactas** que exigieron sus refutadores: (1) el nodo nace con el error **ACTUAL** del padre (`_GE = _EL`), no con el instantáneo de la sorpresa; (2) la poda cuenta **visitas propias de sus casillas** (`_GV.sum()`), no mordidas globales, y usa `>` en vez de `>=`; (3) el control de Occam es **v15f literal** (ganadora por menor error de la casilla sola, sin compuerta contra la lineal y sin poda), no una variante rota del mismo instrumento |
| **capacidad nueva** | **construir el rasgo conjuntivo sin pre-enumerarlo, donde eso significa algo**: con D = 12, C(n,2) = 66 pares y las sorpresas son pocas. En 6 px esto era "proyección, no medida" (suelo 10, techo 13: el umbral no partía el espacio) |
| **predicción clave** | ocupación (nodos vivos) **≪ 66** y creciente con las sorpresas, no con C(n,2); `exp_asoc` de las variantes ≤ 3 con el nodo correcto entre los reclutados; contra **FIJO-todos** (Occam) y **BARAJADO** (pares al azar en la sorpresa) |
| **controles** | FIJO-todos (= v15f), BARAJADO, ESCALAR, `azar` en banda [0.35, 0.65], apagado bit a bit, desempate por **boleto de nacimiento** (nunca por índice: el índice 0 *es* (0,1), y eso ya produjo un 17/20 falso) |
| **coste (Pool)** | 2–3 h de implementador + ≈ 12 min + réplica |
| **qué lo mata** | que BARAJADO iguale a CRECE en exposiciones **y** ocupación (la co-actividad es decorativa); que la ocupación se acerque a C(n,2) (crecer = pre-enumerar con pasos de más → Occam manda); que el nodo **no lea nunca** — y esto se comprueba **antes de firmar el preregistro** con el replay de la vía lenta que el refutador ya escribió (`sala2/refuta_localidad_crece_codigo.py`), como humo obligatorio |

---

#### **BLOQUE 3 — TOKENS Y VARIABLES: el nodo con valor propio y la arista "es variante de"**

| | |
|---|---|
| **qué** | la fusión de lo que sobrevivió a las refutaciones: nodo indexado por **(código, P)** que nace **al ver**; valor propio con **R crudo y sobrescritura** (v15f); arista por **imagen** (L1 ≤ 2), no por código; **la consulta del nodo va ANTES de `_fam`** (o `ncod` no cuenta las mordidas leídas por nodo) — ésta es exactamente la falla que apagaba al órgano en la 6.ª mordida en `DISENO_mundo_grande`; el préstamo **nunca** toca `Wp/Wn`; corte en la primera mordida que contradice a un padre estable; **B-5 compuesto** para las celdas |
| **capacidad nueva** | leer la variante **por su token sin morderla**; aprender una excepción en **una** mordida y olvidarla en **una**; cuando el token cambia, sus variantes cambian **sin morderlas**; y **retención de la excepción** — el número que ningún diseño de la sala medía |
| **predicción clave** | `exp_asoc` de las variantes no-excepción = **0** y de las excepciones ≤ **1**, con **\|ΔW[padre]\| ≤ 0.1** (lo que distingue "préstamo en el nodo" de "préstamo en celdas": B-4 dañó al padre 1.2–2.5) **y el signo correcto en la ÚLTIMA visita en ≥ 18/20**; `ruta` por visita reportada siempre |
| **controles** | BARAJADO (padre = el creado después del más cercano), ESCALAR (media de raíces), SIN_CORTE (**debe** fallar), FRONTERA (sin hermanos: predicción de **igualdad** — el grafo abstiene), AZAR (la arista no puede ayudar: mide el **coste** de la apuesta equivocada) |
| **coste (Pool)** | 2–3 h + ≈ 12 min + réplica; gemelo numba **después** del veredicto |
| **qué lo mata** | que en AZAR también baje (la arista es una fuga y la retina no discrimina); que el padre se abolle; que el órgano se apague por la puerta; que el nodo acabe teniendo uno por variante (`n_slots` ≈ #variantes = grafo degenerado en tabla, que `barajado` fuerza a propósito) |

---

#### **BLOQUE 4 — QUE VIVA: población con muerte real y herencia** *(ya no es "llegar a la frontera")*

| | |
|---|---|
| **calibración OBLIGATORIA antes del preregistro** | medir **ventanas por vida SIN el regalo del renacer** en el mundo elegido (hoy: 0.048–0.079 por vida en el anillo del tronco; 62 muertes en 50 000 pasos; vida mediana 300; el fundador muere sin hijos) y fijar **UNA** perilla (`rep_X`, `dote`, `costo` o `nobj`) de modo que HEREDA tenga **R₀ ≈ 1** y BLANCO **R₀ < 1** *por predicción*, con ERR numerado. **Si ninguna perilla lo consigue, se declara que el mundo no sostiene linajes mortales y V0 no se corre** |
| **qué** | el `run()` de v14.1 como generador; **la muerte borra al individuo**; nacimiento **pagado** (`dote`, nada se regala); modos de herencia (todo / sólo lenta / sólo rápida / **barajada** / escalar / patas / blanco); `madre[j] = c` (el árbol de fisión como estado heredable: el grafo del director en su forma contable) |
| **capacidad nueva** | **qué memoria es portable entre cuerpos: el vector o el token** — la pregunta "grafo o vector" del director medida con un número (`t_ext`, `viables`) y sin símbolo; y **desaprender a escala de linaje** |
| **predicción clave** | SOLO_LENTA y SOLO_RAPIDA ≥ 0.5 × HEREDA en `t_ext`; **BARAJA ≈ BLANCO** |
| **controles** | BARAJA (contenido roto, misma cantidad), ESCALAR y PATAS, BLANCO, `g_nul` (alelo neutro en la misma corrida), GEN_INERTE, banda binomial [5, 15]/20 para lo neutro, orden de cuerpos al azar |
| **qué lo mata** | la calibración (si el fundador no pare, **todos los brazos empatan bit a bit** y A₁₂ ≈ 0.50); el arnés (I5 e I6 hay que rehacerlos: rng propio para la mutación `seed + 700000 + k`, semillas de hijo sin colisión); y la **emergencia** hay que reescribirla como algo que **ningún cuerpo puede tener** (p. ej. "la tabla 2×4 del cuerpo más viejo está completa a T cuando ningún UN_CUERPO la completa antes de morir en ≥ 18/20") — la persistencia por copia es un operador programado, no emergencia |

---

### C.3 Dónde encaja v15f, y por qué importa

**v15f es hoy lo más cerca de la frontera que tenemos**, y no salió de la sala 2 sino de la línea de la mañana: *generaliza*
(G1 1.000 / G2 0.998, azar en banda), *se desdice* (E2 reversión 20/20), *consolida* (E1 W_B ≈ −3 20/20) **y cruza XOR con 8
ejemplos en la configuración del tronco** (xor01 estricta 1.000 contra 0.500, gana (0,1) 20/20, cobertura 4/4). No entra por
el criterio v1 por **dos subletras internas** que no miden conducta — una de ellas ya numerada como **ERR-44** — y por
`splits +16 %`. Es **el primer candidato del criterio v2** y su juicio va en el bloque 0(d). Dos consecuencias:

1. En los bloques 2 y 3, **v15f es el control de Occam**, no un competidor: si el crecimiento no bate a las 15 celdas
   pre-enumeradas en ocupación y exposiciones, el crecimiento sobra y se dice.
2. La "línea XOR" sigue **cerrada** (ERR-35): con 8 ejemplos hay prior y se declara; con 14 no hace falta. Nada de lo de
   arriba la reabre, y ninguna predicción de esta síntesis depende de ella.

### C.4 Y en paralelo, sin `Pool`: tres decisiones del director que llevan horas esperando

**dE5** (recuperación 0.248×/0.267×, dos series, se apaga 20/20, G1 0.80, examen 8/8) · **B-5** (18/18 ALIAS, tronco
idéntico 8/8 + 40/40) · **A-3** (identidad algebraica 60/60, \|ΔW\| 3e−15). Las tres son gratis en CPU y dos de ellas
(dE5 y B-5) son **compañeras necesarias** del bloque 3: sin muestreo la herencia de miedo no se corrige, y sin B-5 el
alias vuelve en cuanto el mundo tenga más de dos estímulos.

---

## D. CRITERIO v2 — redacción propuesta de T-A y T-G para el mundo elegido

*(Texto propuesto para `registro/CRITERIO_TRONCO_v2.md`. **No he editado ese archivo.** Sustituye a las dos filas actuales;
T-B, T-C, T-D, T-E y T-F quedan como están. La decisión es del director; la numeración del ERR, del coordinador.)*

> | # | puerta | medida | umbral |
> |---|---|---|---|
> | **T-A** | **sobrevive en el mundo que obliga** — mundo de familias, peldaño 2: retina D = 12 (9 de forma + 3 de variable), 8 tokens de peso 3, 3 variantes por token (32 estímulos), `n_exc` excepciones, deriva de la variante presente cada 5 000 pasos, cambio de una familia en T/2, **renovación simétrica** (lo rechazado desaparece a tasa comparable a lo comido), dos necesidades, `costo = costo_a = 0.001`, T = 100 000, `NK`/`K` escalados de modo que el alias estructural quede **< 1 %** (calculado con `negativo_codigo.py` **antes** de simular y reportado con cada serie) | **muertes por 100 000 pasos** y **`r = descendientes − muertes`** (la medida validada del bloque 2 de reproducción), **reportadas también sin el regalo del renacer** (`frac_regalo` obligatorio), en los cuatro mundos (`excepciones`, `lineal`, `azar`, `barajado`) | `muertes ≤ 1.10 × línea base` **y** `r ≥ línea base − 10`, donde **la línea base es v14.1 en ESE mundo, medida en el bloque 1 y congelada con su sha ANTES de que exista ningún candidato** (no un número escrito hoy); pareado por semilla `A₁₂ ≥ 0.50`; medianas y cuartiles, nunca `max`, y `A₁₂` **sin parear** para toda integral de trayectoria (ERR-37b). **Cláusula de validez, heredada de P-R1/ERR-40:** `r` debe ordenar los brazos ya medidos como la supervivencia (`A₁₂ ≥ 0.70`) o la medida se retira por tercera vez. **Cláusula del mundo:** si en el bloque 1 v14.1 no se distingue de `lineal`, **T-A no se aplica** — el mundo no obliga y se endurece (`n_exc` 4 → 8) antes de juzgar a nadie, con ERR y fecha |
> | **T-G** | **capacidad nueva: economía de exposiciones por estructura** en ese mundo | (i) **`exp_asoc[k]`** = exposiciones (llegadas al objeto, nunca encuentros agregados) hasta que el valor que usa la boca tiene el signo del mundo **y** \|v\| ≥ 0.5, **por patrón y por clase**: token · variante no-excepción · excepción · variante nunca vista; (ii) **`colateral`** = mordidas de veneno en los **hermanos** en los 10 000 pasos tras la primera mordida de cada excepción; (iii) **retención de la excepción**: signo leído por la boca en su **ÚLTIMA** visita y en Q4 (no sólo en la primera); (iv) **`ruta` usada por visita** (exacto / nodo / arista / lenta), reportada siempre; (v) `w_var` = \|Wps−Wns\| en los píxeles de variable | contra la **línea base de v14.1 del bloque 1**, pareado por semilla y por patrón para lo aprendido; **el umbral se escribe antes y FUERA del rango aritmético del propio efecto** (ERR-37a: prohibido un "OFF ≥ 4" cuando la aritmética de la vía lenta da [1, 9]), derivándolo de esa línea base y no de una intuición. **Los cuatro controles son obligatorios y ninguno es opcional: barajado** (familias falsas / padre equivocado), **escalar** (la cantidad sin el contenido), **azar** (la relación no puede ayudar: mide el coste de la apuesta equivocada) y **apagado** (identidad bit a bit con el rng no consumido). Sin los cuatro **no hay capacidad declarada**. Una reparación inerte sigue entrando como **v14.x**, no como v15. **Prohibido como puerta:** cualquier peso interno (lo dice T-E) y cualquier subcriterio que no distinga "aprendió de un golpe" de "no aprendió" (**ERR-44**); esos se **reportan** |
>
> **Nota añadida a §2 (Reglas):** la línea base de T-A, T-F y T-G la fija el **bloque 1** (v14.1 sin cambios en el mundo que
> obliga), se congela con su sha y su JSON, y **cambiarla después lleva ERR y fecha**. Ningún candidato se juzga con T-A ni
> T-G antes de que esa línea base exista.

---

## E. QUÉ NO HACER (trampas señaladas por los refutadores, con el ERR que las respalda)

1. **No volver a preguntarle al mundo de 6 px lo que no contiene.** Con 8 ejemplos, 9 de 15 hipótesis empatan — **ERR-35**,
   decisión del director 09:55 §2. Cinco de los seis diseños lo hicieron igual.
2. **No usar el examen v3′ 8/8 como puerta absoluta ni ningún peso interno como puerta** — decisión 09:55 §4 y T-E. En
   particular, **no usar "veneno Q4 < Q1"**: **ERR-44** (10:05) — mató a v15f con E1 W_B 20/20 y E2 reversión 20/20.
3. **No poner umbrales en la mediana esperada del propio efecto (ERR-37a), no parear integrales de trayectoria (ERR-37b),
   no usar `max` sobre lecturas (ERR-37c).** Los refutadores lo cazaron tres veces hoy: `mundo_grande` P2 ("OFF ≥ 4" dentro
   del rango aritmético [1, 9]); `crece_codigo` P3 (paso en el **suelo** 10 y refutación en el **techo** 13); `radical` V1′
   (0.5× sobre un efecto que oscila 0.42–0.64 según T).
4. **No dejar zonas muertas entre "pasa" y "refuta"**, y escribir la **regla de censura** de `n*`: `dos_escalas` P4 no decide
   entre 0.65 y 0.75 ni entre 12 y 15/20, y su P5 no es calculable si `n*_lineal` no existe.
5. **No exigir más de lo que la información permite.** En 181–200 el techo LSQ de {P0..P5, P0·P1} da **15/20** y el diseño
   pedía **≥ 16/20**: el resultado más probable se habría leído como "el mecanismo falla" siendo un límite de información
   (exactamente el error que ERR-35 cerró).
6. **No copiar baterías ni runners a mano** — **ERR-38** (defaults: 160 corridas y 38 min de veredicto falso), **ERR-41**
   (kwargs tipo v13), **ERR-42** (JSON perdido), **ERR-43** (regex voraz: `azar 20.000` con la batería en PASA). Entrada
   **campo a campo**, humo que **escriba su JSON**, runner que **copia el booleano** de la batería.
7. **No contar descendientes sin restar muertes ni declarar lo que financia el renacer** — **ERR-40**: ESCALAR hacía 36
   "descendientes" muriendo 1.5× más, y el regalo paga el **34–77 %** de las ventanas.
8. **No poner controles de paja** — **ERR-39**. ESCALAR con `Wp = 0` es un cuerpo que teme todo y no come: "ESCALAR ≤ 2 ×
   BLANCO" se cumple trivialmente.
9. **No desempatar por índice**: el índice 0 *es* (0,1) y eso ya produjo un **17/20 falso**. Boleto de nacimiento aleatorio,
   o abstención declarada; y reportar la multiplicidad del empate.
10. **No agregar sobre patrones con exposiciones 6.3×–23× desiguales** (trampa 3): todo **por exposición y por patrón**, con
    la tabla de exposiciones al lado. Nada agregado sin ella.
11. **No introducir un órgano que el propio ruteo apaga** y que ninguna medida ve: `_fam` consultado **antes** del nodo
    (`mundo_grande`: se apaga solo en la 6.ª mordida) y `_GE` instantáneo contra `_EL` EMA (`crece_codigo`: 72–73 % de los
    reclutas nacen muertos). **Antes de firmar un preregistro, la aritmética cerrada de la compuerta para los dos órdenes de
    mordida**, como hicieron `refuta_crece_gate.py` y `refuta_localidad_crece_codigo.py`.
12. **No medir "aprende en una" sin medir "lo retiene"**: falta el signo leído por la boca en la **última** visita. Con esa
    medida ausente, `slot_ok` y `n_slots` salen bien mientras el organismo ya volvió al camino de OFF.
13. **No llamar "v16" a tres mecanismos distintos** (`sala2/organismo_v16.py` es el radical, `v16c` es crece_codigo, y
    dos_escalas propone un tercero): es la familia **ERR-28 / ERR-38**, y la identidad 24/24 **no lo detectaría** porque los
    tres declaran "apagado ≡ v14.1".
14. **No preregistrar con cifras de un humo corrido en una semilla del propio conjunto de prueba** (`radical`: humo en s101,
    examen en 101–120) — regla 2 y ERR-37a.
15. **No calibrar un mundo con la mortalidad de otro** (`vivir`: 64–100 muertes del mundo vivo trasplantadas al anillo del
    tronco, que mata **124–159**).
16. **No meter capacidad como perilla diseñada a mano si puede entrar como crecimiento** — decisión 09:55 §3. Es la razón por
    la que `mundo_grande` y `radical` valen como **instrumento** y no como candidato.
17. **No recalibrar tras ver datos (regla 3) ni mover un umbral sin ERR (regla 11)**, y no reabrir veredictos ya dados
    (v15c/v15d/v15e **no se rejuzgan**).
18. **No declarar** "lenguaje", "token", "entiende", "concepto", "razona por analogía", "evoluciona inteligencia" — regla 8 y
    EQUIPO 6. Lo declarable hoy sigue siendo: *asocia, revierte, extingue, generaliza lo lineal, cruza XOR con prior de pares,
    valor por necesidad, alias de código y su reparación*.

---

## F. LO QUE FALTA (y lo que no está verificado)

1. **Cuatro refutaciones no se hicieron** (entradas `failed` del journal `wf_54e95359-0b2`):
   `refuta:grafo_tokens:localidad`, `refuta:grafo_tokens:medibilidad`, `refuta:mundo_grande:localidad`,
   `refuta:radical:localidad`. **`grafo_tokens` es el único diseño sin ninguna refutación**: su falta de veredicto **no es un
   mérito** y no puede leerse como tal. Su propio texto declara lo que más pesa en contra (en 6 px la lenta ya acierta el
   signo 10/10 a la primera y el grafo sólo aporta magnitud, "que apenas cambia la conducta"), y su P3 se escribió como
   decisiva con la cláusula de cierre: *"si ON > OFF en < 10/20, la palabra-grafo no supera a la lectura lineal en 6 px"*.
   `mundo_grande` y `radical` tienen **una sola lente**, la de medibilidad; su localidad está sin auditar.
2. **Nada está verificado por PDF.** El revisor de literatura (09:45) trabajó con **fichas de editor**; ya hay una errata
   detectada (la cita "Milstein et al. 2024" **no existe** con esa autoría; es Wu & Maass 2025, *Nat Commun* 16:342) y el
   propio informe dice que **las demás citas del enjambre quedan sin verificar**.
3. **La prueba decisiva de B-4 sigue sin correr**: mundo de regla `px0` (el parecido predice el valor) contra `azar` (no lo
   predice), con el instrumento listo (`organismo_v14L`, identidad 8/8) y ~10 min de `Pool`. **Condiciona los bloques 2 y 3**:
   si el parecido no predice el valor en ningún mundo, lo declarable es *"lo que falta no es la ligadura sino una relación que
   prediga el valor"* y el grafo espera a un mundo donde exista.
4. **La geometría del código está calculada con celdas UNIFORMES.** En el tronco las celdas 31–90 nacen por fisión
   (`KW[j] = clip(0.95·KW[c] + paso·(P − mu[c]))·_rel`, ciegas fuera de `P`, correlacionadas con la madre): *"el techo baja al
   ganar celdas"* (0.667 → 0.500) **no está calculado sobre la población que el tronco crea**. Y el techo **estricto** (sin
   contar el 25 % de empates) es **0.417**, no 0.667.
5. **Ninguna cifra de los seis diseños está medida en serie.** Lo medido es: tres diagnósticos **estructurales** (T = 0,
   milisegundos, sin simular un paso), dos cálculos LSQ de sólo lectura, y **tres corridas de UN proceso** (`radical` s101
   T = 50 000; `vivir` s1 T = 50 000 y la réplica de su refutador). **n = 1 no es evidencia**, y los propios autores lo dicen.
6. **`bateria_exposiciones.py` no existe**: la medida que manda desde el 05:10 no está en ninguna batería del tronco
   (V3 "no medible" en v15c/d/e). Mientras no exista, un candidato que asocia en 1 exposición y otro en 16 pasan igual.
7. **Ningún instrumento nuevo de hoy tiene gemelo numba** (el tronco sí, ×58–78): cada réplica cuesta minutos donde el tronco
   cuesta segundos. El gemelo del mundo nuevo es lo primero que hay que pagar si el bloque 1 se replica o se barre.
8. **Tres órganos con dos series cada uno siguen esperando decisión del director** (dE5, B-5, A-3) y **v15f está sin juzgar
   con el criterio v2** (semillas ya asignadas por el coordinador: 121–140 examen, 181–200 mundo de regla, 301–320 mundo vivo).
9. **El criterio v2 no tiene línea base para T-A, T-F ni T-G en ningún mundo nuevo.** La fija el bloque 1; hasta entonces
   cualquier umbral escrito sería inventado — por eso §D los escribe **relativos a esa línea base** y no en absoluto.
10. **La renovación simétrica es un cambio de mundo propuesto aquí y no tiene un solo número detrás.** Es mi injerto y es el
    riesgo más grande del bloque 1: cambia la física del muestreo y podría hacer el mundo inhabitable. Va con su cláusula
    (una sola corrección de tasa, con ERR) y se reporta `frac_veneno` del anillo por tramos.
11. **La composición de B-5 con cualquier órgano de tokens está sin medir**: en el peldaño 2 las variantes de agua/sal dan
    `R = 0` a la fila del hambre y **B-5 y el órgano pelearían por las mismas celdas**.
12. **Lo que esta síntesis no pudo hacer:** no corrí nada (ni un proceso), así que todo juicio de arriba es lectura de código,
    registro, JSON y de los ocho veredictos estructurados; y no auditar la localidad de `grafo_tokens`, `mundo_grande` y
    `radical` me deja sin la mitad de la evidencia sobre tres de los seis diseños.

---

## Cierre honesto

La sala 2 no produjo un candidato que salga de la frontera, y decirlo es el resultado. Produjo otras dos cosas que valen más
de lo que parece: (a) **el diagnóstico convergente de que el bloqueo principal es el mundo**, no la regla ni la dimensión —
cuatro lentes independientes llegaron a lo mismo por caminos distintos; y (b) **ocho refutaciones que mataron cinco órganos
antes de gastar una sola corrida de `Pool`**, con la aritmética de cada compuerta escrita. Eso es exactamente lo que el
método debía hacer.

Lo razonable mañana no es un órgano: es **el bloque 0 y el bloque 1**, los dos únicos que no pueden refutarse con "el órgano
es inerte" porque no añaden órgano. Y mientras corren, decidir sobre dE5, B-5, A-3 y v15f, que llevan horas esperando en la
puerta con dos series cada uno.

*Sintetizador de la sala 2, 18 sep 2026.*
