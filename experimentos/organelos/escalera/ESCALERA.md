# LA ESCALERA — ingeniería genética peldaño a peldaño sobre un organismo que ya vive (30-sep-2026, Fable, ingeniero genético)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas). Encargo del director (30-sep): tomar un organismo "alma pura", modificarlo genéticamente peldaño por peldaño
hacia comunicarse, razonar, pensar y preguntarse; ver si la escalera es posible, ir más rápido que la selección sola, y tener cosas
concretas. Ajuste del director (30-sep, tarde): el tramo central son las **transiciones mayores** (Maynard Smith y Szathmáry 1995):
unicelular → colonia clonal pegada → división del trabajo (germen/soma) → organismo con órganos → sistema nervioso simple → cuerpo
animal con cerebro → y de ahí comunicación, razonamiento, planear, preguntarse. Modo ráfaga: humos de un proceso, `BITACORA.md`.

## 0. Lo que ya se hizo una vez (y no se repite)
| intento | dónde | resultado | qué queda de él |
|---|---|---|---|
| BLOQUE ALMA (18-sep): un alma externa (Haiku) que parcha al cuerpo tras cada muerte + nodo central | `experimentos/nivel13_alma/` | **REFUTADO**: A₁₂(ALMA > AZAR) 0.525; lo que paga es el contenido del nodo (0.275 vs barajado 0.175) y abaratar el mundo; ningún linaje mortal llega a R₀ 0.9 | "lo que el alma encuentra es hipótesis, no resultado": lo que entra es la **regla fija**, medida sin el buscador |
| PREREGISTRO_eras (18-sep): "la escalera de niveles con alma" (niveles 5–9 bajo el bucle alma/curita) | ídem | 10–11 bloqueados por **falta de instrumento**, no de alma | la escalera se sube con instrumentos nuevos, no con curitas |
| N1 / N3d social (experto→novato; señal = conducta visible) | `etapa5_comunicacion/` | **replicado ×3**; N2 (significado emergente por refuerzo) **cerrado ×6**; INNATO 60 vs 278: el canal sirve con significado DADO | la comunicación del peldaño 7 nace con significado dado (diseño) y se mide contra la señal barajada |
| curiosidad por progreso, novedad de sitio, saturación (nivel 8) | `nivel8_*` | **refutadas** en el mundo del mapa: no devuelven la exploración | preguntarse (peldaño 10) sólo en un mundo donde explorar PAGA (el oasis se mueve) |
| rodeo (nivel 6) | `nivel6_rodeo`, `subida_n6` | elige y rodea; **un paso, no secuencia** | planear (peldaño 9) exige A→B donde A sola no vale |
| enriquecido (llave→nuez), baldwin, baldwin_exp (29-sep) | `organelos/` | **NO**: la selección fija "evitar"; evitar es más barato que aprender | cada peldaño lleva un mundo donde evitar NO es gratis |
| grande (oasis/pantano, 30-sep, sólo humo) | `o1_evo/grande` | P5 "nadie usa el oasis" se cumple (ratio 1.0): ningún carro tiene memoria de lugar | el oasis es el primer mundo que paga una capacidad que O1 no tiene |
| o1_evo (30-sep): O1 con 4 perillas heredables | `o1_evo/` | **NO** por la letra (128 vs 135), pero la selección **conserva** a O1 frente a la deriva (128 vs 81) | tras instalar cada peldaño, la selección afina su promotor (gen), no lo inventa |

## 1. Reglas de la escalera (valen para todos los peldaños)
1. **Base viva:** O1 (`carrera_escuderias/carros/O1.py`, sha `99436afa2715f028`) en la pista (`pista.py` `9f47c65e438e0ff4`, corrido por
   `corre_v143.tarea`, regla 14). Cruza 136–139/180, mayoría 18–19/20. Reglas locales, sin retropropagación, memoria por letra del linaje.
   Para los peldaños con población (2–6) la base es el mismo O1 puesto en ECO (`juaco_eco/motor_eco.py` = `motor_convive` + E1–E8: parto
   real, cuerpo por instancia, quimiostato), porque la pista tiene UN cuerpo por linaje y las transiciones mayores son de población.
2. **Cada peldaño = un módulo por anclas con un PROMOTOR.** Promotor 0 (o perilla 0.0) ⇒ bit a bit el peldaño anterior (arnés, salida
   entera, antes de mirar números). El módulo se agrega al carro (cerebro) o al mundo (física) por anclas desde el sha del anterior.
3. **El mundo paga la capacidad y evitar no es gratis.** Cada peldaño trae UNA perilla de mundo (`oasis`, `cuello`, ...) que, apagada, deja
   el mundo anterior bit a bit; encendida, hace que la capacidad valga y que "no hacer nada" cueste. Se mide que la perilla actúa (validez).
4. **Prueba operacional + control que puede fallar** en cada peldaño (la capacidad se define por lo que el organismo HACE; el control lleva
   el mismo sesgo con el contenido equivocado: barajado, permutado, mudo). "Pensar" y "preguntarse" son estas conductas medidas, nada más.
5. **Diseño vs evolución, declarado en cada peldaño:** el módulo, su promotor y el mundo los pone el ingeniero (DISEÑO). Después la selección
   por pasajes (esquema o1_evo / termostato) puede afinar el promotor como gen (EVOLUCIÓN): "la selección afina perillas, no inventa
   combinaciones" (ESTADO 29-sep). Lo que se declara es la regla fija medida contra su control, nunca lo que el buscador encontró.
6. **Medida principal común:** en la pista, linajes que cruzan (`cruza_real` del juez) pareado por semilla + suma; en ECO, persistencia
   (0 fundadores tras el corte, K de carga) y partos por recurso. Mecanismo desde la FÍSICA (pasos dentro, mordidas dentro, tamaño de
   colonia...), nunca desde lo que declara el carro (ERR-96).
7. **Las cuatro trampas** se revisan por peldaño: canal simétrico; acierto sin balancear; mundo que se come la comida; sitios fijos.
8. **Vocabulario:** recuerda dónde, se pega, reparte, se especializa, transmite, comunica, compone, planea, explora — sólo cuando la letra
   lo respalde. Prohibido "piensa", "quiere", "entiende", "conciencia", "AGI".

## 2. Los peldaños

### Tramo A — la célula (en la pista: un cuerpo por linaje)

**P0 — Unicelular (HECHO).** O1: vive, aprende letras mordiendo, limpia, se reproduce. Prueba: cruza R₀ ≥ 0.9 (136–139/180). Control: v143,
FABRICA (49–61). Estado: hecho y replicado (22-sep, 28–30-sep).

**P1 — Memoria de lugar (CONSTRUIDO HOY: `construye_p1.py`, `mundo_escalera.py`, `corre_p1.py` (congelado), `identidad_p1.py` 37/37; auditado antes de datos, ERR-170/171).**
- Mundo (`oasis=1`): un arco del 10 % del anillo, sorteado por semilla, invisible; dentro A → (+0.8, +0.8) y C → (+0.8, +0.8);
  fuera A y C valen `pobre` = 0.5 de su efecto. Con `oasis=0` es la pista bit a bit; con `extra 0.8, pobre 1.0` es `pista_grande(G1,rica1)`.
  El mundo PAGA: un bocado recordado vale 4 bocados fuera; evitar (no ir) obliga a morder el doble y repone el doble de B/D.
- Módulo (promotor `LUGAR`, peso `LUGAR_W`): 30 bins × 2 necesidades = lo que ese sitio dio DE MÁS que su letra (EMA local en
  `resultado()`); el valor esperado de un objeto en x = valor(letra) + W·bono(x). Nada más cambia en O1. Memoria nueva: 60 floats + 30 conteos.
- Prueba: `lug` > `o1` en linajes que cruzan, pareado por semilla ≥ 13/20 y suma +10; mecanismo: fracción de pasos dentro del oasis / 0.10 ≥ 2
  en `lug` (O1 ≈ 1.0, como en grande).
- Control que puede fallar: `bar` (O1_LUGAR_BAR): escribe en el bin verdadero y LEE en el bin antípoda fijo (mismo sesgo, siempre el lugar equivocado; ERR-170: la permutación por instancia filtraba el oasis en ~45 %).
  `lug` debe ganarle a `bar` también (≥ 13/20, +10). Validez: O1 en la pista lisa ≥ 16/20 mayorías; el oasis actúa (mordidas dentro > 0).
- Diseño: módulo, bins, EMA, W = 1.0, mundo. Evolución después: `LUGAR_W` como gen (P1-evo, esquema o1_evo).
- Costo: humo 6 corridas T 30k ≈ 8 min; exploración 6 × T 100k ≈ 20 min (1 proceso); serie 20 × 4 brazos × T 100k ≈ 4 h CPU (pool 2: 2 h);
  réplica igual.

### Tramo B — las transiciones mayores (en ECO: población, parto real, cuerpo por instancia)

Por qué ECO y no la pista: la pista tiene UN cuerpo vivo por linaje (el hijo espera en la cola) y toda la contabilidad del juez está escrita
así; "pegarse al dividirse" exige que madre e hija vivan a la vez. ECO (`motor_eco`, P1 parto real: el hijo nace EN LA MISMA CELDA del
padre, sin rng) ya tiene eso, quimiostato (capacidad de carga real) y la selección natural ya armó allí un órgano (BLOQUES ×2). Cada
transición se construye por anclas desde `motor_eco.py` (mundo) y desde el carro de ECO (cerebro), con su promotor.

**P2 — Colonia clonal que se queda pegada (Ratcliff 2012, "snowflake yeast").**
- Mundo (`cuello=1`, el que premia el tamaño): cada `P_CUELLO` pasos (p. ej. 2 000), sedimentación: cada cuerpo SUELTO muere con probabilidad
  `p_suelto` (p. ej. 0.5); un cuerpo pegado a un grupo de tamaño k muere con probabilidad `p_suelto / k` (el grupo grande "sedimenta" y se
  queda). Con `cuello=0`, ECO bit a bit. Evitar no es gratis: no pegarse = pasar el cuello a 0.5 cada vez.
- Módulo (promotor `PEGA`, gen 0/1 heredable): al parir, la hija nace pegada a la madre: el grupo comparte la celda y se mueve como UNO (la
  decisión de movimiento la toma el cuerpo más viejo del grupo; los demás copian el `mov`; cada uno muerde lo que hay bajo el grupo con su
  propia boca, así que el grupo come más rápido lo que pisa y pela más rápido lo que rodea: el costo del tamaño). Memoria nueva: id de grupo
  por cuerpo. Con `PEGA=0`, ECO bit a bit.
- Prueba: linajes con `PEGA=1` persisten y paren más que con `PEGA=0` en el mundo con cuello (pareado por semilla ≥ 13/20 en K de carga
  y en partos); mecanismo: tamaño mediano de grupo ≥ 3 y fracción de muertes en el cuello menor.
- Control que puede fallar: (a) `PEGA=1` en el mundo SIN cuello ⇒ persiste menos o igual que `PEGA=0` (pegarse cuesta: comparte comida);
  (b) `PEGA_SUELTA`: se pega pero el cuello no lo cuenta (el mundo lee tamaño 1 para todos) ⇒ no gana. Si (a) no cae, el mundo no cobraba.
- Evolución después: `PEGA` como gen en ECO_SEL: ¿la selección lo prende sola con cuello y lo apaga sin cuello? (ésa es la réplica de Ratcliff).
- Costo: mundo + carro por anclas ~3 h de construcción; humo ECO T 50k × 4 brazos ≈ 15 min; serie 20 × 4 × T 300k ≈ 6 h CPU.

**P3 — División del trabajo: germen y soma (Volvox; Michod).**
- Mundo: el de P2 (cuello) + `reparto=1`: los cuerpos pegados REPARTEN cada paso E y Ag (promedio local dentro del grupo: regla local, sin
  rng). Con eso la ventana de reproducción (E, Ag ≥ 1.0 durante 500 pasos) es del grupo, y un cuerpo que come sin parir alimenta al que pare.
- Módulo (promotor `SOMA`, gen p_soma ∈ [0, 1]): al nacer pegada, la hija es soma con probabilidad p_soma: nunca abre su ventana
  (`quiere_parir` False), sólo come y reparte; germen = el resto. Memoria nueva: 1 bit por cuerpo.
- Prueba: grupos con `SOMA` (p_soma 0.5) producen más hijos por bocado A+C y persisten más que grupos sin soma (p_soma 0), pareado ≥ 13/20.
  Mecanismo: fracción de partos de células germen ≥ 0.9 y bocados de soma > 0.
- Control que puede fallar: `SOMA` sin `reparto` (el soma come para sí y no pare: puro costo) ⇒ pierde. Y `SOMA_AZAR`: el bit se sortea
  cada paso (no es una especialización estable) ⇒ no gana.
- Evolución: p_soma como gen; ¿la selección lo lleva de 0 a > 0 sólo con reparto y cuello? (la convexidad de Michod, medida).

**P4 — Organismo con órganos: células que comen, se mueven, sienten.**
- Mundo: el de P3 + `vista_parcial=1`: cada cuerpo ve sólo los objetos a distancia ≤ `R` (p. ej. 20); hoy la pista entrega TODOS los objetos
  (percepción global). Con vista parcial un cuerpo solo ve poco; un grupo extendido (ver abajo) ve más. Evitar no es gratis: solo, se muere de
  hambre buscando.
- Módulo (promotor `ORGANO`): el grupo deja de ser un punto: es una CADENA de k celdas contiguas (la cabeza decide el `mov`, los demás siguen
  la celda de adelante). Cada cuerpo del grupo tiene un tipo heredable {boca, pata, sentido}: boca = muerde (los demás no); pata = su `mov`
  cuenta para la cabeza (voto); sentido = aporta lo que ve (su ventana de R) al grupo. Memoria nueva: tipo por cuerpo (2 bits).
- Prueba: grupos con órganos encuentran comida a más distancia (encuentros A+C por paso, desde la física) y persisten más que grupos
  homogéneos (todos boca) con vista parcial. Control: tipos barajados cada paso (sin órganos estables) ⇒ no gana; y sin vista parcial (mundo
  que no paga sentir) ⇒ homogéneo ≥ órganos.

**P5 — Sistema nervioso simple: señales dentro del cuerpo.**
- Mundo: el de P4 con `R` chico (10) y objetos escasos: lo que ve el sentido de la cola no lo ve la cabeza.
- Módulo (promotor `NERVIO`): canal INTERNO del grupo (no la pizarra pública): cada cuerpo escribe ≤ 2 números (dirección y valor esperado
  de lo mejor que ve, con SU memoria de letra+lugar) que sólo leen los pegados; la cabeza integra (suma ponderada, regla fija) y decide. Es
  el N1/N3d (señal con significado dado) dentro de un cuerpo. Memoria nueva: 2 floats por cuerpo por paso (no persiste).
- Prueba: con `NERVIO` el grupo llega a comida que sólo vio la cola (encuentros a distancia > R de la cabeza) y persiste más que sin nervio.
  Control que puede fallar: `NERVIO_BARAJA` (la dirección escrita se permuta) ⇒ igual o peor que sin nervio (el sesgo de moverse más no basta).

**P6 — Cuerpo animal con cerebro.**
- Módulo (promotor `CEREBRO`): la cabeza deja de ser "el más viejo": es una célula de tipo cerebro que lleva la memoria de letra y de lugar
  del GRUPO (una sola tabla, escrita por todas las bocas: lo que muerde cualquiera lo aprende el cerebro) y decide con ella; las demás no
  aprenden (ahorro: una memoria en vez de k). Prueba: con cerebro el grupo aprende el veneno con menos mordidas totales (p1 del juez por
  grupo) y persiste igual o más que con k memorias. Control: cerebro que sólo lee su propia boca ⇒ aprende como una célula sola.
  Aquí el organismo vuelve a ser "uno" (un cerebro, un cuerpo con partes): es O1 con cuerpo. Desde aquí los peldaños son entre organismos.

### Tramo C — entre organismos: comunicar, componer, planear, preguntarse (en la pista o en ECO, según el peldaño)

**P7 — Comunicación con significado dado, que cambia la conducta del receptor y PAGA a ambos.**
- Mundo: oasis (P1) que cada organismo descubre por su cuenta + monocultivo (9 linajes del mismo carro: el receptor es del mismo genotipo,
  el pago es al linaje; en pista mixta el pago sería al rival: se declara). Costo de emitir: escribir cuesta `c_e` E (0.01).
- Módulo (promotor `SEÑAL`): cuando la memoria de lugar de un cuerpo supera un umbral en un bin, escribe en la pizarra pública (canal
  existente, `escribe=(bin, bono)`); un receptor con `SEÑAL` lee la pizarra y siembra su memoria de lugar con lo leído (peso `W_S`).
- Prueba: linajes `SEÑAL` llegan al oasis ANTES de su primera mordida dentro (pasos hasta el primer bocado dentro, desde la física) y cruzan
  más que `o1`+`lug` sin señal; el emisor no pierde (pareado). Control que puede fallar: pizarra BARAJADA (bin permutado al leer) ⇒ igual o
  peor que sin señal; MUDO (lee pero nadie escribe) = `lug`. Trampa del canal simétrico: se reporta quién escribe y quién lee por linaje.
- Ya se sabe (N2): el significado no emerge por refuerzo; aquí es dado por diseño y se dice.

**P8 — Componer / transferencia en frío (lo que el director llama razonar).**
- Mundo: dos reglas aprendidas por separado: (i) el oasis (lugar → bono) y (ii) una letra nueva E ("sal dulce") cuyo valor depende de la
  necesidad (aprendido por letra). Tarea NUEVA nunca entrenada: E dentro del oasis. Predicción componible: valor(E, x) = valor(E) + bono(x).
- Módulo: ninguno nuevo (es lo que P1 ya hace si está bien hecho: la suma letra + lugar es la composición). Prueba operacional: primer
  encuentro con E dentro del oasis: muerde/rechaza según la suma (acierto balanceado J = p1 + c1 − 1 ≥ 0.5 en el primer encuentro, sin
  haber mordido nunca E allí). Control que puede fallar: `bar` (lugar permutado) ⇒ J ≈ 0; y letra E con valor barajado ⇒ J ≈ 0.
- Si P1 no compone así (p. ej. el bono no entra a `_quiere` de una letra nueva), es un módulo pequeño (promotor `COMPONE`) y se dice.

**P9 — Planear: secuencia A→B donde evitar no es gratis.**
- Mundo: `cerrojo=1`: el oasis sólo paga si el cuerpo lleva "llave": haber mordido una letra K (neutra: dS = 0) en los últimos `D` pasos.
  Sin llave, dentro del oasis A y C valen lo pobre. Evitar K es gratis para O1 (K no daña y no da: nunca la vuelve a buscar) — y por eso
  pierde el oasis: evitar cuesta el oasis entero. (Es el `enriquecido` que la selección no armó; aquí se arma por diseño y se mide.)
- Módulo (promotor `PLAN`): crédito de un paso hacia atrás: cuando un bocado da más de lo esperado (bono de lugar positivo), la ÚLTIMA letra
  mordida antes recibe una fracción `λ` de ese extra en una tabla "letra→lo que habilita" (regla local, traza de elegibilidad de longitud 1);
  al valorar K se suma lo que habilita. Memoria nueva: una tabla por letra (2 floats) + la última letra y su t.
- Prueba: `PLAN` muerde K y luego va al oasis (secuencia K→oasis medida desde la física: fracción de bocados dentro con llave ≥ 0.6) y cruza
  más que `lug` sin PLAN en el mundo con cerrojo. Control que puede fallar: `PLAN_BARAJA` (el crédito va a una letra al azar) ⇒ no gana;
  sin cerrojo, `PLAN` = `lug` (no cuesta).

**P10 — Preguntarse: explorar para reducir la propia incertidumbre, y que pague después.**
- Mundo: `mueve=1`: el oasis cambia de sitio cada `P_M` pasos (p. ej. 20 000) a un sitio nuevo sorteado. Lo recordado caduca; quien no
  vuelve a mirar se queda con un mapa viejo (la memoria de lugar se hace mentirosa): evitar explorar no es gratis.
- Módulo (promotor `PREGUNTA`): incertidumbre por bin = pasos desde la última mordida allí (o conteo `nl`); cuando el cuerpo está saciado
  (E, Ag ≥ U: hoy va al "hueco" entre cuerpos) se dirige al bin con MAYOR incertidumbre y menor distancia (el sitio del que menos sabe), y
  la EMA de lugar olvida con `LG_ETA` (ya lo hace). Control que puede fallar: `PREGUNTA_AZAR`: mismo número de excursiones, a un bin al
  azar. Prueba: tras cada mudanza, pasos hasta el primer bocado dentro del oasis nuevo menores con `PREGUNTA` que con AZAR y que sin
  explorar (pareado ≥ 13/20), y cruza más. Esto es "preguntarse" como conducta medida: ir a donde la propia memoria es más vieja, y que
  eso pague. Nada más se afirma.
- Ya se sabe (nivel 8): la curiosidad no devolvió la exploración en el mundo del mapa porque allí explorar no pagaba. Aquí el mundo lo cobra.

### Tramo D — SEXO Y FAMILIA (idea del director, 30-sep noche; en ECO: población, parto real, genoma por cuerpo)

**Instrumento más barato (decisión razonada):** `juaco_eco/motor_eco.py` (sha fijado, por anclas; NO la cámara de `entre_linajes`). Razones:
(1) el tramo exige que DOS padres estén vivos a la vez y cerca: la cámara de entre_linajes vive en la pista v1 (un cuerpo por linaje; los genes
viajan por el depósito entre linajes, no entre dos cuerpos que se encuentran); ECO tiene cuerpos por instancia, parto real en la celda del
padre y el genoma YA en el motor (`b.g`, 18 genes de FABRICA, mutación `muta()` con rng propio por hijo `[seed, i, 16, k]`). (2) La selección ya
actúa en ECO (ECO_SEL ×2: sube K del linaje) y hay una célula nativa que vive allí (FAMB_RES0_ECO, K 31–39 en el mundo de 9); O1 no vive en
v2 (P2, 30-sep). (3) El "nieto" ya está en la salida: `individuos = [k, gen, padre, t_nace, t_muere, hijos, ...]` por linaje: nietos de un
cuerpo = suma de `hijos` de sus hijos, sin instrumento nuevo. Costo: humo (9 fundadores, esc 9, T 50k, 3 brazos × 2 semillas) ≈ 15–25 min
de un proceso (la célula FABRICA es más lenta que O1); serie 20 × 3 × T 200k ≈ 8 h CPU (4 h pool 2). Construcción: `mundo_familia.py` por
anclas sobre `motor_eco.run_solapadas` (el parto: donde hoy `_gh = muta(b.g, ...)`), con `familia=None` ⇒ motor_eco bit a bit (arnés).
**Moneda:** persistencia tras el corte (vivero E9 y `t_corte`, como ECO) y K; y la que pide el director: NIETOS por linaje (de la física).
**Mundo que paga:** el quimiostato de ECO (la comida es fija): la variación genética sólo vale si la selección la puede usar; se mide el
rumbo de los genes (`gen_t`, log(g/G0)) como en ECO_SEL. Todos los brazos llevan el MISMO costo de apareamiento (buscar pareja) salvo que se diga.

**D1 — Reproducción de a dos (recombinación; Fisher 1930, Muller 1932; Weissman et al. 2010 sobre valles).**
- Mundo (`sexo=1`): cada cuerpo nace con un TIPO heredable X/Y (bit; el hijo toma el tipo de uno de los dos padres al azar: X/Y se mantiene
  50/50 sin diseño). Un cuerpo que completa su ventana sólo pare si hay un cuerpo VIVO del mismo carro, del OTRO tipo, a distancia ≤ `R_PAR`
  (p. ej. 10): la pareja. Si no la hay, la ventana se reinicia (cuenta en `sin_pareja`: evitar no es gratis: sin pareja no hay hijo). Genoma del
  hijo = por gen, el de la madre o el del padre con p 0.5 (rng `[seed, i, 20, k]`, nueva etiqueta) y DESPUÉS la mutación de siempre.
- Control que puede fallar (`sexo=1, recombina=0`): la misma pareja obligatoria, el mismo costo, pero el hijo copia SÓLO a la madre (clon con
  pareja). Base (`sexo=0`): ECO. El control PUEDE ganar: en un valle hondo la recombinación rompe mitades co-adaptadas (Weissman 2010), y en
  18 genes con un óptimo cercano a G0 la ventaja de Fisher–Muller puede ser nula.
- Prueba: `sexo` persiste más tras el corte y deja más nietos por linaje que el clon con pareja (pareado por semilla ≥ 13/20); mecanismo: el
  rumbo de los genes que ECO_SEL ya movió es más rápido (|log(g/G0)| mayor en el corte) y la varianza entre vivos menor (la recombinación
  junta mitades). Predicción honesta: p 0.40 de que gane; 0.35 empate; 0.25 el clon.

**D2 — Elección de pareja con inteligencia mínima (selección sexual; Darwin 1871; Zahavi 1975 señal honesta; Andersson 1994).**
- Mundo (`pareja='fuerte'`): entre las parejas posibles (D1), la madre toma la de MAYOR reserva real E+Ag (la señal es honesta porque es el
  estado físico que el mundo ya aplica, no una declaración del carro; ERR-96). Control (`pareja='azar'`): una al azar entre las posibles
  (rng `[seed, i, 21, k]`). Mismo costo, misma recombinación (D1 encendido en ambos).
- Prueba: con `fuerte`, el rumbo de los genes en selección es MÁS RÁPIDO que con `azar` (la selección sexual "aumenta el paso": la mitad
  paterna viene del que mejor come) y la persistencia/nietos no bajan. Control que puede fallar: si la reserva es ruido (el que tiene más E es el
  que acaba de comer, no el mejor genotipo), `fuerte` = `azar`. p 0.35.

**D3 — Inversión parental conjunta (Trivers 1972; Clutton-Brock 1991).**
- Mundo (`dote_doble=1`): los dos padres pagan la dote del hijo por mitades (0.3 + 0.3); el hijo recibe lo mismo (0.6). Control: la madre paga
  todo (ECO). Evitar no es gratis: el padre que paga pierde reserva y puede no llegar a su propia ventana.
- Prueba: más partos por recurso (A+C mordidas) y más nietos; mecanismo: la madre vuelve a la ventana antes (pasos entre partos menores). Si
  el padre deja de parir por pagar, la suma puede ser cero: p 0.50.

**D4 — Reducción de camada (Mock y Parker 1997; Rohwer 1978 huevos tróficos; siblicidio en aves y peces).**
- Mundo (`camada=1`): cuando a un cuerpo con hijos vivos cerca (≤ `R_PAR`) le falta comida (E o Ag < `U_CAM`, p. ej. 0.4) y tiene ≥ 2 hijos
  vivos, el hijo MÁS DÉBIL (menor E+Ag) muere y su reserva pasa al padre (o al hermano más fuerte, perilla `a_quien`). Es física del mundo (regla
  local, sin rng). Control que puede fallar (`camada=0`): todos los hijos reciben igual. Causa de muerte nueva en la salida: `trofico`.
- Prueba: NIETOS por linaje mayores con `camada` (el linaje concentra recurso en los que llegan a parir) y persistencia no menor; mecanismo:
  muertes `trofico` > 0 y vida mediana de los hijos sobrevivientes mayor. Honesto: en quimiostato el recurso del hijo débil ya "vuelve" al
  mundo al morir de hambre (reposición fija: NO vuelve: por eso puede pagar); si el hijo débil se habría recuperado, pierde. p 0.40.

**Lo que no se afirma:** nada de "familia", "cuidado", "elige" en el sentido humano: cada peldaño es una regla física del mundo (D1–D4 son
perillas del motor) medida en nietos/persistencia contra su control; el carro no cambia (la célula nativa no sabe que hay sexo). Orden:
D1 → D2 (necesita D1) → D3 → D4; D3 y D4 son independientes de D1. Trampas: canal (no hay); acierto (no hay); comida (quimiostato: se reporta
`nobj_medio`); sitios fijos (sin sitios). Todo esto es DISEÑO (promotores del mundo); después, `sexo` como gen (D1-evo): ¿la selección lo
conserva o lo apaga? Es la pregunta de Maynard Smith (1978) sobre el costo doble del sexo, medible aquí.

## 3. Orden, costo y qué se declara
| # | peldaño | mundo (perilla) | instrumento | costo humo / serie | estado |
|---|---|---|---|---|---|
| 0 | unicelular | pista | O1 | — | hecho |
| 1 | memoria de lugar | pista + `oasis` (denso, vista parcial) | O1_LUGAR (hecho) | 8 min / 1.4 h pool 2 | **SERIE (20 semillas, 30-sep 20:39): FUNCIONA — cruzan lug 79 / bar 0 / o1 7 (o1f 137), pareado 20/20 contra ambos, establecidos 133 / 0 / 9, razón de pasos en el oasis 7.25 / 0.59 / 1.05; V1–V4 OK, 0 abortos. Réplica en curso (pool 2). Lo lee y declara el coordinador** |
| 2 | colonia pegada | pista v2 (motor_convive) + `cuello` (+ `solo_sueltos`) | mundo_colonia (arnés 6/6; reapertura: `--carro FAMB_RES0_ECO`, `--p_suelto 0.2`, `--solo_sueltos`) | 10 min / 3 h | **CERRADO en ráfaga con las DOS células (5 humos): con O1 (no vive en v2) y con la célula nativa de ECO (cuello suave p 0.2 y cuello sólo sobre sueltos): peg persiste 1/18 y 0/18 vs sue 3/18 y 4/18, partos 311–316 vs 383–420; la pista "pegarse protege al recién nacido" NO se repite con la célula ECO (vida 94 vs 127). Reabrir sólo con recurso en manchas o con reparto (P3) desde el inicio** |
| 3 | germen/soma | ECO + `cuello` + `reparto` | `SOMA` | 15 min / 3 h | diseñado |
| 4 | órganos | ECO + `vista_parcial` | `ORGANO` (cadena, tipos) | 20 min / 4 h | diseñado |
| 5 | sistema nervioso | ECO + `R` chico | `NERVIO` (canal interno) | 20 min / 4 h | diseñado |
| 6 | cerebro | ECO | `CEREBRO` (una memoria por grupo) | 20 min / 4 h | diseñado |
| 7 | señal por pizarra (significado dado, linajes clones, costo) | pista + `oasis` (P1b) + `c_e` 0.01 (mundo_tramo_c) | O1_LUGAR_SENAL (sobre construye_p1 por sha; control antípoda) | 10 min / 1.3 h pool 2 | **PROTOCOLO COMPLETO LISTO PARA EL AUDITOR (tanda 2): PREREGISTRO_p7.md (diseño declarado como visto en exploración), corre_p7 con candados, identidad_p7 36/36. Humo 3 con costo pendiente de CPU** |
| 8 | componer (frío) | `mundo_tramo_c`: letra E (+0.3, −0.1) p_x 0.1 | `COMPONE` (construye_c; control = COMPONE sobre O1_LUGAR_BAR antípoda) | 10 min / 2 h | **SIN SEÑAL en ráfaga (2 humos; el instrumento está confundido con la LIMPIEZA de O1)**: J 0.15 y 0.10 (comp) vs −0.3 / −0.16 (lug); c1 frío comp 0.69–0.71 vs lug 0.34–0.53 vs antípoda 0.30–0.31; cruzan 3/0/0 en el humo 2; pero lug también muerde E dentro en frío (limpieza) y todos muerden E fuera: J no aísla la composición. Humo 3 sólo con medida nueva (excluir limpieza o medir el blanco elegido) |
| 9 | planear | `mundo_tramo_c`: letra K (0, 0) p_x 0.1 + `cerrojo` d_llave 1500 (+ `cerrojo_pobre`, `mundo_k`) | `PLAN` (crédito de un paso; control = crédito a la penúltima) | 10 min / 2 h | **CERRADO en ráfaga (3 humos sin señal)**: los tres brazos colapsan (vida 200–300) en los tres mundos (pobre sin llave; nominal sin llave; nominal + K con vida útil); el control de paso equivocado cruza igual o más (4/6/3 en el humo 3); hab_K ≈ 0. El crédito de un paso no arranca desde fundadores limpios en vidas de 200 pasos. Reabrir sólo con mundo donde la base viva y traza de 3 pasos |
| 10 | preguntarse | `mundo_tramo_c`: `mueve` 10k (humo) / 20k | `PREGUNTA` (olvido por presencia + bin menos visitado; control = antípoda) | 10 min / 1.1 h pool 2 | **SEÑAL CLARA (explora T 100k: cruzan preg 16 / lug 11 / antípoda 5, 2/2 contra ambos; latencia tras la mudanza 408 / 1283 / 1511; fundadores 0.6 / 27.9 / 50.2; trampa 3 declarada: pela el mundo 0.63). PROTOCOLO COMPLETO escrito: PREREGISTRO_p10.md, corre_p10.py con candados, identidad_p10.py (arnés pendiente de CPU)** |
| D1 | reproducción de a dos | ECO + `sexo` (pareja X/Y a ≤ r_par 10, recombinación por gen) | `mundo_familia.py` (12 anclas sobre motor_eco `bca3033878b59622`; `corre_d.py`; arnés `identidad_d` 11/11) | 5 min / 4 h CPU (la célula ECO corre 12 s por 12k pasos) | instrumento listo (30-sep noche); humo pendiente de CPU |
| D2 | elección de pareja | ECO + `sexo` + `pareja` fuerte/azar | ídem | 5 min / 4 h | instrumento listo |
| D3 | inversión parental | ECO + `sexo` + `dote_doble` | ídem | 5 min / 4 h | instrumento listo |
| D4 | reducción de camada | ECO + `camada` (hijo débil → recurso; medido: a T 4k nadie tiene 2 hijos vivos a la vez, a T 12k dispara) | ídem | 5 min / 4 h | instrumento listo |

- Ninguna corrida de ráfaga se declara. Un peldaño se separa y va a protocolo completo (preregistro, arnés entero, auditor, serie + réplica
  con Pool del coordinador) sólo cuando su humo/exploración muestra señal clara contra SU control (candidato > control en las semillas de la
  exploración y mecanismo desde la física).
- Después de cada peldaño declarado: P-evo (el promotor como gen; ¿la selección lo conserva, lo sube o lo apaga cuando el mundo deja de
  pagarlo?). Ése es el segundo objetivo del director ("más rápido que la selección sola"): la escalera pone el módulo; la selección lo afina.
- Lo honesto: 1 y 7–10 se apilan sobre O1 en la pista y son baratos; 2–6 exigen ECO y un cuerpo extendido, y son el tramo caro (semanas,
  no un día). Si el director prefiere subir primero el tramo C (comunicar/planear/preguntarse) sobre P1, la escalera lo permite: los tramos
  B y C son independientes hasta P6.
