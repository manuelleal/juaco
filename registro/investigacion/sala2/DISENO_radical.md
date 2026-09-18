# SALA 2 — DISEÑO RADICAL: **v16 «TOKEN»** — el organismo como grafo de nodos-retina con valor de un golpe

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales, sin retropropagación en el
runtime, que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada. Primero la frontera; segundo,
que viva. El método manda sobre el cómo: nada de lo de abajo se declara sin identidad, preregistro, controles, semillas nuevas y réplica.

**Creador de la sala 2, ángulo radical, 18 sep 2026 (~10:00).** Encargo del director (09:40): *"la tokenización y la representación:
si sal es sal será número uno, lo guardo, lo vectoriza; después sal rosa lo vectoriza, marca como sal y lo plantea como una variable de
lo mismo — eso es lenguaje; aprender y desaprender"*; y (05:25) *"la palabra es grafo, no vectorización"*. Fuentes leídas: CLAUDE.md
(día 7), PLAN.md (orden del 18), HANDOFF §13 y §15.7–15.8, REGISTRO desde ERR-35 al final (incluidos v15e 09:37, ERR-43, revisor de
literatura, reproducción bloque 2), ENJAMBRE_xor, PUENTE A12–A16 y B-4/B-5, los tres preregistros, `organismo_v14.py` entero,
`bateria_v14.py`, `bateria_generaliza.py`, `organismo_v14g.py`, `corre_sal.py`, `corre_mundo_largo.py`, `construye_codigo.py`,
`identidad_codigo.py`. **Reglas cumplidas:** ningún archivo existente editado; sólo archivos nuevos en `registro/investigacion/sala2/`;
ningún `Pool`; **una** corrida de un proceso con T = 50 000 (§8), medida después de escribir §4; sin commits ni `git add`.

---

## 0. En diez líneas

- **Bloqueo, en una frase:** el valor vive en **direcciones compartidas y con pérdida** (3 celdas de 90 por patrón, delta rule sobre
  ellas) y sólo se escribe **al morder y con tasa**. De ahí salen, con la misma causa, el alias de código (nivel 4), las ~47 mordidas
  de B para llegar a −3 (nivel 3, "la repetición es el enemigo"), el trilema exacto/reversible/generaliza (v15d ↔ v15e), la
  retención de lo ausente 0.67 (interferencia) y la capacidad atada al pool (35–51 de 60).
- **Apuesta:** cambiar el **sustrato de la memoria de casos**: un **grafo de nodos-token** — nodo = retina exacta (la clave),
  nacido en la **primera llegada**, con **valor escrito de un golpe y sobrescrito** (aprender = escribir, desaprender = sobrescribir),
  y **aristas de variante** (Hamming 1) por las que un nodo sin consecuencia propia **lee a sus vecinos** ("sal rosa lee a sal hasta
  que la muerde"). La boca lee el grafo si tiene algo que decir; si no, v14.1 (la regla). Las dos vías de v14.1 **no se tocan**.
- **Estado nuevo:** un diccionario `{retina → [valor, n]}` (≤ 64 nodos en 6 px). **Constantes nuevas: cero.** rng: intacto.
- **Capacidad nueva y medible:** identidad por retina (alias **imposible por construcción**, sin división), asociación en **1 mordida**
  con reversión en **1 mordida** sin tocar la lectura lineal (v15e lo hizo dentro de la vía lenta y perdió XOR; aquí XOR no se toca),
  **transferencia exacta a variantes sin morderlas** (la lineal la diluye a −2: 20–60× más mordidas de veneno-variante), separación
  de una **variante traidora en 1 mordida con abolladura 0** en el padre, retención de lo ausente 1.0, capacidad sin pool.
- **Lo que lo mata:** que el examen v3′ caiga por la letra (predigo que **cae** en «veneno Q4 < Q1»: suelo de inanición, §4 P1);
  que la regla se quede sin mordidas (G1 < 0.95); que las variantes no hereden o que la traidora abolle al padre (§4 P6); y el techo
  del sustrato: claves exactas sólo viven en retinas discretas y pequeñas (2^n nodos; §6).

---

## 1. Qué bloquea, según mi lectura, con evidencia del registro

**1.1 La memoria de valor vive en una dirección compartida y con pérdida.** `code(P)` = las 3 celdas de 90 con mayor `KW@P`
(`organismo_v14.py` L42–43); el valor es `(Wp−Wn)@kenyon(P)` (L63). Dos retinas distintas con el mismo código son **la misma cosa**
para el organismo. Medido: con 4 estímulos algún par comparte código en **18/200** semillas (9 %); en el mundo de regla **170/200**
semillas tienen un par idéntico y 135/200 una fuga a un patrón de test (`negativo_codigo`, B-5). Consecuencia medida: la sal muda hereda
el miedo (|W[sal]| 1.45–1.72), **el veneno paga** (−1.45 en vez de −3.0), la evitación ×7 y nadie corrige (bloque de la sal, 08:16;
S-5: no es la sed, es el código; S-6: la puerta no repara). B-5 lo repara **en un régimen** (R = 0 bajo retina distinta, 18/18) y el
propio B dejó escrito lo que no cubre: *"alias con R ruidoso y alias de magnitud con el mismo signo"*. El síntoma se repara; la causa
(la clave con pérdida) sigue.

**1.2 Sólo se aprende al morder, y con tasa.** Todo aprendizaje está bajo `if mordio:` (L107). v14.1 muerde B **[27, 11, 8, 1]** por
cuarto para consolidar −3 (humo de v15e sobre v14.1, s101) sobre ~**5 000** exposiciones a B por vida (mundo vivo: A 831 / B 5 253); la
vía lenta necesita 150–200 exposiciones para una regla (A-4, A-6). El director (05:10 B): *"la repetición es el enemigo: exposiciones
hasta asociar es la medida"*. Y A midió que sin morder no hay señal (§A12 (a)3): el problema no es la señal, es que **cada mordida se
gasta en mover un promedio** en vez de **escribir un caso**.

**1.3 El trilema exacto / reversible / generaliza.** v15d: exacto a la primera y cruza XOR, **no se desdice** (E2 0/20) y mata de
hambre a la rápida (E1 0/20). v15e: se desdice (E2 20/20) y consolida (E1 W_B 20/20), **hereda el fracaso de la lineal** (XOR 0.500).
v14.1: generaliza (1.000) y se desdice, **no es exacto** (~47 mordidas). Lo que los tres comparten: **la memoria de casos no es un
objeto propio** — vive en celdas compartidas (v14.1) o en una tabla atada a la lectura de la lineal (v15d/e). Cada arreglo mueve el
canje; ninguno lo rompe, exactamente como pasó con v9→v11→v13 hasta que la memoria de casos y la regla se **separaron con una puerta**.

**1.4 Olvido por interferencia y capacidad atada al pool.** Retención de lo ausente **0.67** a 150k (mundo largo: *interferencia,
no inversión*); capacidad N\* **35** (v13) / **51** (v14) de 60 (canje puerta/capacidad, ERR-22). Las dos son consecuencia de 1.1:
lo que se escribe en celdas compartidas se pisa, y lo que exige celdas se agota.

**1.5 Lo que ya se probó en ESTA dirección y falló — y en qué mi diseño no es eso.** **B-4 (06:00)**: ligar lo nuevo al nodo más
cercano y heredar por la arista → NO en el mundo del tronco, con cuatro razones **medidas**: (i) el préstamo caía **en celdas
compartidas** y contaminaba al vecino (W_B −2.97 → −4.2/−5.5); (ii) el código Kenyon **no ordena vecinos** (similitud 0/0/0.333);
(iii) en el mundo del tronco *"el parecido no predice el valor: lo contradice"* (el único par parecido es comida/veneno, sim 0.225);
(iv) *"la señal que enseñaría al grafo (fiabilidad por arista, EMA) es más rara que el problema"*. **B-5 lateral (05:55)**: la
asociación por parecido acelera igual en `azar` que en `px0` → no es el mecanismo. Mi diseño responde a cada una: (i) el valor está
**en el nodo**, nunca en celdas — el vecino no se toca; (ii) la vecindad es **Hamming sobre la retina exacta**, no sobre el código;
(iii) la arista de variante es **Hamming 1**, y en los mundos congelados (patrones de peso 3) **no existe ningún par a Hamming 1** →
la herencia es **inerte por construcción** donde el parecido contradice, y se prueba **sólo** donde hay variantes de verdad (§4 P6),
con la traidora como control que puede fallar; (iv) **no hay fiabilidades que aprender**: la herencia dura hasta la primera mordida
propia (sobrescritura); ninguna EMA, ninguna constante.

**1.6 El bloqueo de método.** De los últimos nueve ERR, cuatro son de instrumento copiado (38, 41, 42, 43). Lo que más nos ha costado
esta madrugada no fue una hipótesis mala: fue una batería con un default distinto. Por eso §5 es campo a campo.

---

## 2. Mecanismo: pseudocódigo por anclas sobre `organismo/organismo_v14.py` (feefc88b1fd8d434)

**Construido y verificado:** `registro/investigacion/sala2/construye_v16.py` → `organismo_v16.py` (**9906cdbb9b533b13**), seis anclas,
cada una exigida exactamente una vez; el constructor aborta si el sha del origen cambia. Perillas: **`token=0`** (maestra; 0 por
defecto) y **`tok_var=1`** (aristas de variante; sólo actúa con `token=1`).

| ancla | línea del tronco (v14.1) | qué se inserta / cambia | estado / rng |
|---|---|---|---|
| **A1** firma | `,pat_shuf=0,pat_min=1):` | `,token=0,tok_var=1):` | — |
| **A2** estado | tras `Wps=np.zeros(6); Wns=np.zeros(6)` (L50) | `_tok={}` y dos ayudantes `_tkey`, `_tlee` (abajo) | dict vacío; **no consume rng** |
| **A3** `valor(P)` (L62–64) | `return _f+_s if puerta is None else (...)` | `_v14=…; if token: _tl=_tlee(P); if _tl is not None: return _tl; return _v14` | sólo lectura: **no crea nodos** |
| **A4** boca (L103) | `Vb=alpha*_wt+…` | `_wm=_wt; if token: nace el nodo si no existe (n=0); _tl=_tlee(PAT[kk]); if _tl is not None: _wm=_tl` y `Vb=alpha*_wm+…` | `_wt/_wf/_ws` **intactos** para el error de cada vía |
| **A5** mordida (tras L108, con `R` conocido) | `R=R_VAL[val[kk]]; …` | `if token: _tok[_tq][0]=R; _tok[_tq][1]+=1` | **un golpe, sobrescritura** |
| **A6** salida (L164) | `return dict(sobre=sobre,` | `+ token, tok_var, n_tok, tok` (sólo lectura) | — |

```python
_tok = {}                                   # retina exacta -> [valor escrito de un golpe, n de consecuencias propias]
def _tkey(P): return frozenset(np.flatnonzero(P > 0).tolist())        # el TOKEN: la clave es la retina, no el código
def _tlee(P):                               # lectura del GRAFO
    q = _tkey(P); e = _tok.get(q)
    if e is not None and e[1] > 0: return e[0]                          # 1) valor propio (ya lo mordió)
    if not tok_var: return None
    v = [x[0] for u, x in _tok.items() if x[1] > 0 and len(q ^ u) == 1] # 2) vecinos a Hamming 1 con consecuencia (aristas de variante)
    return (sum(v) / len(v)) if v else None                             # 3) nada que decir -> None -> v14.1 (la regla)
# boca (A4):  el nodo nace en la primera LLEGADA (n=0); _wm = _tlee(P) si no es None, si no _wt (v14.1)
# mordida (A5): _tok[q] = [R, n+1]        aprender = escribir; desaprender = sobrescribir
```

**Orden de lectura en la boca:** propio (n ≥ 1) → variantes (Hamming 1 con n ≥ 1, media; determinista, sin desempate por índice) →
v14.1 (`_wt`: rápida si familiar, si no la lenta). **Las dos vías de v14.1 siguen aprendiendo de su propio error con sus propias
líneas** (`dlt=R−_wf`, `_ds=R−_ws`, L115–120): el token sólo cambia **qué muerde la boca**, no cómo aprenden las vías.

**Por qué apagado ≡ v14.1 bit a bit:** con `token=0`, A3 devuelve la misma expresión (`_v14`), A4 usa `_wm=_wt` (mismo double), A5 no
se ejecuta, A2 sólo crea un dict vacío y define funciones; ninguna línea nueva llama a `rng`. Con `token=1` **tampoco** se consume rng
(el grafo es determinista): la trayectoria diverge sólo porque `pb` cambia. Exigencia (no predicción): arnés I1–I4 de §5.

**Qué es inerte dónde (y por eso qué montaje mide qué):**

| pieza | tronco A–D / examen | mundo de regla (20 patrones peso 3) | mundo vivo (4 estímulos) | mundo largo (pool pesos 2–4) | mundo de variantes (§4 P6) |
|---|---|---|---|---|---|
| nodo + un golpe + sobrescritura | **actúa** (E1/E2/alias por retina) | actúa en los de tren; los de test **leen v14.1** (sin nodo) | **actúa** (valor vectorial por necesidad) | actúa | actúa |
| arista de variante (Hamming 1) | **inerte**: no hay pares a Hamming 1 entre patrones de peso 3 (dos 3-subconjuntos de 6 difieren en ≥ 2 px) | **inerte** (ídem) | **inerte** (ídem) | **actúa** (peso 2 ↔ 3 ↔ 4): valencias al azar → el **control `azar` de la arista** | **actúa**: es su prueba |

**Copias por las mismas anclas (las construye el implementador; declaradas aquí):** (a) `organismo_v16g.py` ← `organismo_v14g.py`
(mundo de regla; mismas seis anclas; `P_[kk]` en vez de `PAT[kk]`); (b) `organismo_vivo_v16.py` ← `organismo_vivo.py`: el valor del
nodo es un **vector por necesidad** (`_tok[q]=[np.zeros(n_nec),0]`, A5 escribe `_Rv` entero — *un encuentro enseña a todas las
necesidades, de un golpe* —, A3/A4 leen la componente `_nm`; la boca `_wt` de L137); (c) `mundo_largo_v16.py` ← `mundo_largo.py`
(base **v13**: la boca es `_wf if int(...)>=puerta else _ws`, ancla adaptada y declarada); (d) `mundo_variantes_v16.py` ←
`organismo_v16.py`: perilla `ruido_px=0.0` (cada píxel de la vista se voltea con prob. `ruido_px`, `Generator` propio `seed+800000`,
**sin sorteo si `ruido_px=0`** → identidad exacta con `organismo_v16`), la vista ruidosa `_Pv` sustituye a `PAT[kk]` en las siete
apariciones del bloque de la mordida (código `kc`, lectura lenta, actualización lenta, `P` de la división, clave del token, `x` de la
política), y un patrón nuevo **`B1 = [1,0,1,1,1,0]`** (B con el píxel 3 encendido; Hamming 1 de B, ≥ 3 de A/C/D) para la variante
traidora, **fijado aquí, no buscado**. (e) `bateria_v16.py` ← `bateria_v14.py` (sobre `_on`; enmienda de §4 P1). (f)
`bateria_generaliza_v16.py` ← `bateria_generaliza.py` (entrada campo a campo, §5).

**Qué NO hay, y por qué (decidido, no a decidir después):** ni tasa, ni tope, ni EMA, ni fiabilidad por arista (B-4 midió que esa
señal es más rara que el problema; aquí la arista muere con la primera mordida propia del hijo, por sobrescritura); ni **energía ni
muerte de nodos** — el ángulo lo ofrecía, y lo descarto por honestidad: en 6 px hay ≤ 64 retinas, la memoria no puede explotar, y una
muerte por desuso **rompería** "exacta sin experiencia" (Etapa 4) sin que ningún montaje actual pueda medir lo que compra; es el
problema de v17 con retina mayor (§7); ni **n-gramas temporales** (la extensión natural de "sal rosa" como composición; §7).

---

## 3. Por qué sale de la frontera: capacidad NUEVA y MEDIBLE

Traducción exacta de la hipótesis del director: **token = clave/nodo** (`_tkey`: la retina es la clave, no una dirección con
pérdida); **"sal rosa como variable de sal"** = un nodo nuevo a Hamming 1 que **lee al padre hasta que tiene consecuencia propia**;
**grafo, no vector**: el valor está en el nodo, el vector (retina) es sólo la clave; **aprender y desaprender** = escribir y
sobrescribir. Lo que aparece, y con qué se mide:

1. **Identidad por retina → alias imposible por construcción** (nivel 4). Sal y veneno con el mismo código de Kenyon tienen nodos
   distintos: |W[sal]| **0.0**, veneno **−3.0**, sin división, en el **mismo montaje** de B-5 (9 ALIAS + 9 LIMPIAS) — y cubre los
   regímenes que B-5 declaró fuera (magnitud con el mismo signo; R ruidoso).
2. **Exposiciones hasta asociar = 1 mordida; se desdice en 1 mordida; la lectura lineal intacta** (niveles 3–4). v15e ya mostró que
   *cada vía con su error* consolida la rápida y se desdice; lo hizo dentro de la vía lenta y perdió XOR. Aquí la memoria de casos es
   un objeto **fuera** de las vías: XOR no se toca (la línea está cerrada con su prior; el candidato v15f puede coexistir como lector de
   la lenta). Medida: exposiciones hasta |v| ≥ 0.5 con el signo del mundo (la de `organismo_vivo`), `W_B` exacto, `come B Q4`.
3. **Transferencia exacta a variantes sin morderlas** (el enunciado del director, nivel 3 no lineal / robustez). Con B en −3, la
   lineal de v14.1 lee una variante a 1 px en **−2** (2 de 3 píxeles; medido en el humo: D, que comparte 2 px con B, lee −2.50);
   la boca de v14.1 a −2 con hambre 1 muerde con `pb` **0.58** y a −3 con **0.025**; con hambre 0.5, 0.047 contra 0.0009. El grafo
   lee **−3.0 exacto** en la variante sin morderla: **20–60× menos mordidas de veneno-variante**. Es la diferencia entre *"se parece a
   sal"* y *"es una variable de sal"*.
4. **La variante traidora se separa en 1 mordida y el padre no se abolla** (B1 comida a Hamming 1 de B): v16 sobrescribe B1 a +1 y B
   sigue en −3.0 exacto; v14.1 empuja los 3 píxeles compartidos hacia + (0.45·Δ por mordida de B1) y abolla B hasta que la rápida
   divide (E2K permite −2.4). **Precio declarado:** v16 hereda −3 exacto en B1 → la muerde **más tarde** (sólo en inanición) que
   v14.1 (que lee −2): *heredar exacto protege más y explora menos*. Se preregistran las tres medidas (§4 P6d).
5. **Retención de lo ausente 1.0 y capacidad sin pool.** Sin celdas compartidas no hay interferencia (mundo largo: 0.67 → ≥ 0.95) y
   N\* = nº de nodos (60/60). Lo declaro **por construcción** (guardas, no hallazgos).

**Lo que NO es nuevo, dicho antes de que lo diga el revisor:** memoria por instancias / control episódico (MFEC, Blundell 2016; NEC,
Pritzel 2017), tile coding, ART. El revisor de las 09:45 ya dijo *"ningún mecanismo nuevo"* del alias; aquí tampoco lo habrá. Lo que
se mide y no está reportado así es la **composición** con el tronco (grafo delante, regla detrás, cada vía con su error), con identidad
bit a bit y las cinco capacidades de arriba en el mismo organismo y los mismos mundos. Vocabulario permitido si pasa: *"asocia en una
mordida y se desdice en una"*, *"dos retinas nunca comparten valor"*, *"una variante lee a su padre hasta que la muerde"*. Prohibido:
"reconoce", "lenguaje", "entiende".

---

## 4. Preregistro (escrito antes de cualquier serie; el humo de §8 se midió después de este bloque)

**Instrumentos:** los de §2/§5. **T = 100 000** salvo mundo largo (200 000) y mundo de regla (200 000, como la batería). **Semillas:**
examen y generalización **101–120** (las del criterio del tronco; réplica 121–140 si algún subcriterio queda a ±1, regla 12); alias:
las listas **estructurales de B-5** (ALIAS 326, 334, 343, 377, 446, 533, 549, 563, 670 / LIMPIAS 307, 313, 316, 323, 325, 327, 333,
338, 342; réplica ALIAS 779–944 / LIMPIAS 703–764) para comparar 1:1 con D0/D1 — el runner las recalcula con `diagnostico_codigos.py`
y aborta si no coinciden; mundo largo **61–80** (1–60 gastadas en ese montaje); capacidad grande **21–40**; mundo de variantes
**1101–1120**, réplica **1121–1140** (rango virgen: 301–1100 tuvo selección estructural). **Estadística:** lo aprendido (W, exposiciones
hasta criterio, tabla) se parea por semilla; **mordidas, muertes y exposiciones totales son integrales de trayectoria y NO se parean**
(ERR-37b): A₁₂, razón de medianas y cuartiles. Ningún umbral en la mediana esperada del propio efecto (ERR-37a); ningún `max` sobre
lecturas (ERR-37c).

| # | predicción (numérica) | control / de dónde sale | qué me refuta |
|---|---|---|---|
| **P1 examen v3′** (`bateria_v16.py 20 --desde 101 --log`, perilla ON) | **W_B ≈ −3: 20/20 con \|W_B+3\| < 0.05** (exacto); E2 «come B Q4 ≥ 50», «W_B → +1», «W_A → −3» **20/20**; E2I/E2J/E2K/E2L **20/20** (W_C −3.0, W_D +1.0, B intacto); 4c **20/20** (0 divisiones, W_C −3.0); 4d E2L «termina < 25k» **≥ 19/20** (humo: 6 296); 3′ (rápida sola, `token=0`) ≤ 1/20; 3″ ≥ 19/20; **3‴ (nuevo: token solo, `plast=False, eta_s=0, puerta=None, token=1`) ≥ 19/20**. **Y predigo que V1 CAE POR LA LETRA en E1 «veneno Q4 < Q1»: 12–16/20** — las mordidas de B quedan **planas** desde la primera (suelo de inanición `pb` 0.025: humo [6, 2, 2, 5]); v14.1 las tiene [27, 11, 8, 1] porque consolida despacio | 3′/3″/3‴ = desdoble del control como en ERR-21 (un tercer camino rompe el control que asumía dos): **enmienda de instrumento escrita antes de correr, candidata a ERR (numera el coordinador)**; la batería copiada pasa `token=0` sólo en CTRL | E1 W_B < 20/20 o E2 < 20/20 → el un golpe no consolida o no se desdice: **muerto**. Si cae **sólo** «Q4 < Q1» con W_B exacto 20/20 y Q1 ≤ 10, la lectura preregistrada es *"criterio con efecto suelo para un aprendiz de un golpe"* (informativa **V1′: mordidas totales de B en E1 ≤ 0.5 × v14.1**, A₁₂ ≥ 0.8); **por la letra v16 no entra**, y cualquier letra nueva lleva ERR y semillas nuevas, nunca estos datos |
| **P2 generalización** (`bateria_generaliza_v16.py organismo_v16_on 20 --desde 101 --log`) | **G1 ≥ 0.95** (espero 1.000: los de test no tienen nodo ni vecino a Hamming 1 → leen la lineal de v14.1), **G2 ≥ 0.95**, K 20/20, `azar` ∈ [0.35, 0.65]; diagnóstico: mordidas de los venenos de tren ON ≥ 0.5 × OFF (la lineal converge con 15: humo −2.998) | `azar` (regla al azar) y el pareado ON/OFF por semilla que ya imprime la batería | G1 < 0.95 → el grafo **mata de hambre a la regla** (quita las mordidas que la entrenan): no es candidato al tronco; `azar` fuera de banda → fuga |
| **P3 alias por construcción** (`corre_sal`-montaje sobre `organismo_vivo_v16`, NO_INFORMA, n_nec=2 y n_nec=1) | ALIAS: **\|W[sal]\| ≤ 0.05 en 9/9** (mediana 0.0), **W[veneno] −3.0 ± 0.05 en 9/9**, exposiciones a la sal ≤ 1.5 × LIMPIAS en ≥ 8/9, **0 divisiones por R = 0** (B-5 apagado), muertes ≤ 0.8 × D0-ALIAS (A₁₂ ≥ 0.8); LIMPIAS sin regresión 9/9; VIVO (sal informa la sed): tabla 2×4 exacta con **`exp_tabla` ≤ 4** (v14.1: 11) | D0 (v14.1) y D1 (B-5) del registro como referencia numérica; réplica en las ALIAS 779–944 | \|W[sal]\| > 0.3 en ≥ 2/9 → **el instrumento** (primera hipótesis, regla 5): el nodo no indexa lo que digo; `exp_tabla` > 6 → el un golpe no llega a todas las necesidades |
| **P4 retención de lo ausente** (`mundo_largo_v16`, brazos V13-base OFF / ON `tok_var=0` / ON `tok_var=1`; 61–80) | ON: `ret_no_inv` **≥ 0.95 en ≥ 18/20** (v13 0.67); `ret_inv` (invertidos en ausencia) igual a OFF ± 0.1 (nadie puede saberlo); adquisición `adq_hasta30` ON(`tok_var=0`) ≥ OFF − 0.05; **`tok_var=1` ≤ `tok_var=0` en `adq_hasta30`, pareado ≥ 12/20** (aquí el parecido NO predice el valor: heredar cuesta — es el `azar` de la arista) | OFF = v13 dentro del runner; `tok_var=0` aísla nodo de arista | `ret_no_inv` < 0.85 → hay interferencia que no viene de celdas (instrumento); si `tok_var=1` **no** cuesta en adquisición, B-4 y yo estamos equivocados sobre por qué heredar cuesta |
| **P5 capacidad** (`capacidad_grande`, 21–40, paso largo) | N\* **≥ 58 de 60** en ≥ 18/20 (v14 51, v13 35), `celdas` ≤ v14; **por construcción**: guarda, no hallazgo | v14.1 OFF en el mismo runner | N\* < 55 → el mundo grande tiene algo que no es memoria (muestreo, muertes): se reporta |
| **P6 mundo de variantes** (`mundo_variantes_v16`, `ruido_px = 0.05` → 73.5 % vista canónica, 23.2 % 1 px, 3 % 2 px; 1101–1120; brazos OFF=v14.1 / ON / ON `tok_var=0` / BARAJA_VAR / BARAJA_ESC / ESCALAR) | **(a)** mordidas de vistas-variante de veneno por vida: ON ≤ **0.2 ×** OFF (razón de medianas), A₁₂ ≥ 0.9; ON `tok_var=0` ≥ 0.6 × OFF (sin arista, cada variante paga su mordida); **(b)** exposiciones hasta asociar B (canónica): ON ≤ 2 (mediana), OFF ≥ 5; **(c)** `n_tok` ON ≤ 64 (mediana 35–55); **(d) traidora** `B1` comida desde 50 000: **exposiciones hasta la primera mordida de B1: ON ≥ 1.5 × OFF** (pérdida declarada); **mordidas de B1 desde la primera hasta criterio (tasa ≥ 0.5 en ventana de 20 encuentros): ON ≤ 2 en ≥ 18/20, OFF ≥ 5 (mediana)**; **abolladura de B (`W_B_peor` = máximo de W_B tras 50k, log cada 1 000): ON \|W_B+3\| ≤ 0.05 en 20/20; OFF W_B_peor > −2.5 en ≥ 10/20**; muertes ON ≤ 1.2 × OFF (razón de medianas) | BARAJA_VAR: un nodo sin consecuencia lee un nodo con consecuencia **al azar** (rng propio) en vez de sus vecinos → (a) se pierde (≥ 0.8 × OFF); BARAJA_ESC: el nodo escribe el R de la mordida **anterior** → E1/E2 caen; ESCALAR: una sola clave para todo → W_A = W_B; `tok_var=0` aísla la arista; `ruido_px=0` ≡ `organismo_v16` (identidad) | (a) o (d-abolladura) fallan → *"variante como variable de lo mismo"* **refutada en este sustrato**; (d-primera mordida) ON < OFF → mi modelo de la boca está mal (se reporta igual); BARAJA_VAR no destruye (a) → la arista no hace nada y lo hace la lineal: humo |
| **P7 controles de no-vacuidad** | APAGADO: I1–I4 100 % (§5); ESCALAR E1 «W_A ≈ +1 y W_B ≈ −3» **0/20**; BARAJA_ESC E1 W_B **≤ 2/20**, E2 reversión **≤ 2/20**; 3‴ ≥ 19/20 | — | un control que no falla → el grafo no está haciendo el trabajo que digo |
| **P8 coste** | tiempo de pared ON ≤ 1.3 × OFF (humo: 3.2 s / 50k); `celdas` ≤ 45 en las 9 etapas (espero **menos** divisiones que v14.1 en E2/E2L: −10 a −40 %, porque hay menos mordidas de veneno; **la rápida queda de sombra en la boca**: se reporta como coste, no se esconde); `n_tok` = 2–4 en el tronco, 20 en regla, ≤ 64 en variantes; muertes E1 ON ≤ 1.2 × OFF (trampa 3: lo rechazado se queda en el anillo) | — | tiempo > 1.5× o muertes > 1.5× → el precio de la exactitud es el mundo, se reporta |

**Cláusula.** Si P1 cae **sólo** por «Q4 < Q1» (con V1′ y todo lo demás pasando), v16 **no entra al tronco por la letra** y se abre
la discusión de criterio con ERR y semillas nuevas — como ERR-21 → v3′. Si cae P2, P3 o P6(a)/(d-abolladura), la línea se cierra y se
declara lo que se midió. Nada se recalibra; ninguna perilla nueva sobre estos datos.

---

## 5. Coste e instrumentos

**Archivos (todos nuevos; los congelados sólo se leen; `manifiesto.py --check` intacto):** `construye_v16.py` (hecho) →
`organismo_v16.py` (hecho, 9906cdbb9b533b13) · `organismo_v16_on.py` (`token=1` por defecto, lo examinan las baterías) ·
`organismo_v16g.py`/`_on` · `organismo_vivo_v16.py` · `mundo_largo_v16.py` · `mundo_variantes_v16.py` · `bateria_v16.py` ·
`bateria_generaliza_v16.py` · `identidad_v16.py` · `corre_v16.py` (subprocesos **secuenciales**: identidad → V1 → V2a → alias → largo
→ variantes → capacidad; `--humo` de un proceso; **nunca dos `Pool`**; lee los **campos** de las baterías, no el log — ERR-43).

**Identidad (`identidad_v16.py`, un proceso, antes de mirar un número; si no es 100 %, nada corre):** **I1** `organismo_v16(token=0)`
≡ `organismo_v14` en los 12 escenarios de `identidad_codigo.py` × 2 semillas, todas las claves; **I2** rng no consumido con la perilla
apagada, T = 120 000, 2 semillas; **I3** `organismo_v16g(token=0)` ≡ `organismo_v14g`, 3 reglas × 2, con los kwargs EXACTOS de la
entrada del tronco; **I4** `organismo_vivo_v16(token=0)` ≡ `organismo_vivo`, 5 montajes × 2; **I5** `mundo_largo_v16(token=0)` ≡
`mundo_largo`, 2; **I6** `mundo_variantes_v16(ruido_px=0)` ≡ `organismo_v16` (ON y OFF), 4; **I7 (debe fallar)** `token=1` ≠
`token=0` en E1 s1 y `W_B` ON = −3.0 exacto. Predicción adicional, no exigencia: con `token=1` el rng tampoco se consume (I2 con ON).

**Baterías por anclas, campo a campo (regla 14 / ERR-38, 41, 42):** `bateria_v16.py` = `bateria_v14.py` cambiando el import a
`organismo_v16_on` (n = 2), los nombres de salida, `RAIZ`/`sys.path` con `organismo/` PRIMERO (ERR-28), el sha de v11/v10 leído
desde `organismo/` (ERR-42) **y una sola enmienda de letra declarada: `CTRL: dict(solap_AB=3, plast=False, eta_s=0.0, puerta=None,
token=0)` y `CTRL3: dict(solap_AB=3, plast=False, eta_s=0.0, puerta=None, token=1)` con veredicto `3‴ ≥ S−1`**; el resto de etapas,
CRIT y umbrales **intactos**. `bateria_generaliza_v16.py`: entrada `'organismo_v16_on': ('organismo_v16g_on', dict(eta_s=0.15,
clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1))` — **los mismos diez
kwargs que `'organismo_v14'`, copiados del archivo, más ninguno** (el gemelo g tiene `eta_s=0.0, clip_s=3.0` por defecto: la perilla
`token` va en el default del módulo `_on`, no en la entrada); el constructor la compara campo a campo con la del tronco y aborta si
difiere. Toda batería copiada corre un humo que **escribe su JSON** antes de la serie (ERR-42). Los corredores de mundo de regla pasan
los kwargs exactos del tronco (ERR-41).

**Pool (lo corre el coordinador):** V1 9 × 20 = 180 corridas (~2 min); V2a 60 × 200k (~1–2 min); alias 4 brazos × 9 × 2 series + 15
de identidad (~1 min); largo 3 × 20 × 200k (~3 min); variantes 6 × 20 (~3 min); capacidad 2 × 20 (~2 min). **≈ 12–15 min de `Pool(14)`
en total**, en serie, nunca solapado con otro Pool. Tokens: este documento y los constructores; los runners los escribe un implementador
en ≤ 2 h con los patrones de `construye_codigo.py`/`corre_codigo.py`.

---

## 6. Humo y espejos: cómo podría engañarnos, y cómo lo evito

1. **"Es un diccionario."** Sí. Lo digo en §3 y lo dirá el revisor. Lo que no es trivial y se mide: la **composición** (grafo delante,
   regla detrás, cada vía con su error) sin romper G1, alias 0 sin división, y los **precios** (P1 letra, P6 primera mordida, P8
   muertes). Un diccionario que rompiera G1 o matara más sería un hallazgo negativo; lo preregistro igual.
2. **La retina de 6 px sin ruido regala las claves exactas.** El límite es del sustrato, no del organismo: 2^n nodos; una retina
   continua exige un cuantizador y el cuantizador es el código Kenyon, que es justo lo que aliasa. Por eso el mundo de variantes es
   la **prueba mínima honesta** y por eso §7 (retina mayor + muerte de nodos) es la continuación obligada, no un adorno.
3. **La exactitud quita mordidas, y las mordidas entrenan a la rápida y a la lenta.** Riesgos medidos, no supuestos: 4d (E2L < 25k:
   humo 6 296, pero una semilla), G1 (P2 con diagnóstico de mordidas ON/OFF), «Q4 < Q1» (predigo la caída). Nada de esto se esconde
   detrás de un promedio.
4. **Trampa 3 (el mundo que se come la comida):** rechazar exacto desde la primera mordida deja el veneno en el anillo → más inanición
   → más mordidas por hambre y más muertes (humo: 58 muertes en 50k, sin par OFF). P8 lo acota y lo reporta por distribución.
5. **Empates y suelos.** La media de vecinos es determinista (sin índice que gane); los criterios pareados van sólo a lo aprendido;
   «Q4 < Q1» tiene suelo para un aprendiz de un golpe y lo digo antes de correr, con la lectura informativa V1′ separada del veredicto.
6. **El control 3′ deja de medir lo que medía** (un tercer camino, como en ERR-21): desdoblado antes de correr, con ERR candidato.
7. **La traidora no se busca:** `B1` fijado en §2 antes de ver ningún dato; `ruido_px = 0.05` fijado por argumento (1 px en el 23 % de
   las vistas, 2 px en el 3 %: suficiente para que existan variantes y raras las dobles), no por barrido.
8. **"Grafo" como palabra:** en los mundos congelados el grafo **no tiene aristas** (no hay pares a Hamming 1). Lo digo en la tabla de
   §2; el grafo se prueba donde hay variantes, y si allí no compra nada, se declara *"nodos exactos; la arista no aporta"*.
9. **El humo de §8 es una semilla** y se corrió después de escribir §4; no es evidencia de nada; sólo dice que el instrumento arranca y
   que la predicción más incierta (4d) no está muerta de salida.

---

## 7. Lo que sigue si pasa (no se promete; se nombra para que la línea tenga dirección)

**v17-a, retina mayor y muerte de nodos:** mundo de 12 px con `ruido_px` (4 096 retinas): allí los nodos espurios cuestan y la
**energía por uso** (gana en cada llegada, decae por paso, muere en 0) es medible contra "exacta sin experiencia"; el canje
olvido-por-desuso / retención se preregistra con umbrales de tiempo. **v17-b, n-gramas con retroceso:** nodo = (token anterior,
token) — *"sal rosa"* como composición — leído por el contexto más largo conocido y con retroceso al más corto; prueba en 3T-k a
k = 4–5, donde v14.1 agota el pool; el riesgo conocido es la fragmentación de la evidencia por contexto (una mordida por n-grama). **Lo
que NO sigue:** XOR (cerrada), N2 (cerrada con dos mundos).

---

## 8. Humo (UNA corrida de UN proceso, T = 50 000; medida DESPUÉS de fijar §4) — `humo_v16.py` → `humo_v16_E2L_s101.json`

Montaje E2L (`solap_AB=3`), semilla 101, `token=1, tok_var=1`; `organismo_v16` 9906cdbb9b533b13 sobre v14.1 feefc88b1fd8d434; 3.2 s.
**Predicción escrita antes:** W_A +1.00 / W_B −3.00 exactos; B mordida ≈ [3–10, 1–5, 1–5, 1–5] por cuarto de 12.5k; primera división
antes de 25 000; `solap` → 0 probable; `celdas` ≤ 35; `n_tok` = 2.

| medida | resultado | predicción |
|---|---|---|
| W (grafo, lo que lee la boca) | **A +1.0, B −3.0** (exactos); C −0.5, D −2.5 (nunca vistos: leen la lineal) | ✓ |
| W_lenta (sólo lectura) | A +1.000, **B −2.998** con 15 mordidas | (no predicho: la regla converge con pocas mordidas a `eta_s` 0.15) |
| rápida `comp` B | (0.0, 2.24): consolidada, en un código ya separado | — |
| mordidas B por cuarto (12.5k) / llegadas | **[6, 2, 2, 5]** / [1 191, 1 190, 1 465, 1 222] · A [52, 37, 56, 28] | ✓ planas: suelo de inanición |
| divisiones | 3, **todas en t = 6 296** (mordida de B); `t_conflicto` 52; **`solap AB` = 0** | ✓ (< 25 000) |
| celdas / muertes / nodos | **33** / 58 en 50k (sin par OFF: no se corrió) / **`n_tok` 2** {B: (−3.0, n=15), A: (+1.0, n=173)} | ✓ / — / ✓ |

**Lo que dice:** el instrumento arranca; el un golpe es exacto; la división por conflicto se dispara igual con 6 mordidas de B en el
primer cuarto (4d no está muerto de salida); las mordidas de B son planas → **la caída de «Q4 < Q1» que predigo en P1 es real como
riesgo** (aquí Q4 = 5 contra Q1 = 6: a una mordida). **Lo que no dice:** nada sobre 20 semillas, nada sobre OFF pareado, nada sobre
G1, alias, largo ni variantes. No se corrió nada más (tope de una corrida).
