# EXPLORATORIO, no es dato

# FICHAS del explorador — la célula y la evolución temprana como mapa para el bicho (24-sep-2026)

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados
con controles y réplicas); el método manda sobre el cómo.

**Pedido del director (sus palabras):** *"La idea es la multiplicación celular, la célula humana y la evolución de sus organelos;
cada parte cuenta como referencia hacia lo que tenemos. La vida se gesta ahora. No necesitamos crear un organismo perfecto ni
cumplir los benchmarks. No tenemos el tiempo de la evolución: necesitamos ir acelerándola y corrigiéndola, ¡solo selección
natural! Hay que romper el molde: siempre lo limitamos por lo que hay, y no por los errores."*

**Qué es este archivo.** Ideas, no instrumentos. Nada de aquí es dato. Tres juguetes de bolsillo (`juguete_ohno.py`,
`juguete_reina_roja.py`, `juguete_tragar.py`, semillas 23001–23025, un proceso cada uno; 165 s, 131 s y **418 s: el tercero se
pasó del límite de 5 min y no se repitió**) sirvieron sólo para ver si una idea tiene vida; sus 14 predicciones se escribieron
antes de correr y **7 quedaron refutadas** (se declaran una a una en §D).

**Qué leí en el repo (archivo:línea) y qué imagino.** Todo lo que se cita con `archivo:línea` lo leí hoy. Lo demás es imaginación
o literatura (citada). Fuentes del repo: `registro/NUBE_BITACORA_20260924.md` §1g–1k y §4; `registro/ESTADO.md`;
`experimentos/juaco_eco/motor_eco3.py:1-135` y `:415-485`; `experimentos/frankenstein/NOTA_EXPLORATORIA.md` y `organos_frank.py`;
`experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py:143-150` (retina PAT, VAL_VIVO, EFECTO); `registro/investigacion/RONDA1_laboratorio_20260923.md`
(fichas F1–F5 de la ronda 1, para no repetirlas); `registro/investigacion/REPOS_cercanos.md` (Avida, Lenia, POET ya fichados).

---

## (a) MAPA — la célula y la evolución temprana → el bicho de hoy → qué falta

| parte de la célula / de la evolución | equivalente en el bicho HOY (con línea) | qué falta para que aparezca SOLO |
|---|---|---|
| **Membrana / compartimento** (adentro ≠ afuera) | Existe: el cuerpo con E y Ag, costo por paso, muerte real, dote (`motor_eco3.py:12-40`, P1–P4) | Nada esencial. Es la única parte que ya es célula. |
| **Genoma** | Vector FIJO de 25 perillas (`GENES`, `motor_eco3.py:84-92`) + 7 órganos con umbral 1.0 (`ORG_G0`, `UMBRAL_ORG`, `:93-94`) | Largo variable. Hoy el espacio de fenotipos es una caja de 25 dimensiones que nosotros dibujamos; nada puede salirse. |
| **Replicación con error** | `muta()` log-normal por gen, p y sigma constantes (`motor_eco3.py:123-135`) | Errores ESTRUCTURALES: duplicar, borrar, invertir, fusionar (fichas 1, 8). Tasa de mutación como gen (ficha 11). |
| **Traducción genotipo→fenotipo** (ribosoma) | `ctx_genoma()` copia perillas al ctx (`:179-187`); un órgano se expresa si su gen ≥ 1.0 | Una GRAMÁTICA: que los genes CONSTRUYAN el órgano, no que lo prendan (bitácora §4, punto 1; ficha 1). |
| **Mitocondria / cloroplasto (endosimbiosis, Margulis)** | No existe. Los cuerpos no se ven entre sí; sólo compiten por los mismos objetos (`:28-31`, P4) | Que un cuerpo pueda TRAGAR a otro linaje y quedárselo como parte que decide (ficha 2). |
| **Núcleo / germen vs soma (Weismann)** | No hay separación: la tabla VIVIDA del padre pasa al hijo tal cual (`herencia`/`ensena`, modo `res`, `organos_frank.py:145-153`) — lamarckiano | Que el VALOR de una letra pueda escribirse también en el genoma (instinto) y que la selección decida cuánto pasa por cada canal (ficha 10). |
| **División celular** | Existe: parto real, el hijo nace en la celda del padre (P1, `:16-19`) | — |
| **Multicelularidad (dividirse y quedarse juntos)** | No existe. El hijo se va; ningún cuerpo comparte E con otro; el mundo está "bien mezclado" (RONDA1 patrón 1: todos ven todo) | Adhesión: bolsa común de energía entre parientes en la misma celda (ficha 4). Requiere LOCALIDAD (RONDA1 F4/F5). |
| **Diferenciación / división del trabajo** | No existe: todos los cuerpos de un linaje expresan igual el mismo genoma | Expresión CONDICIONADA por una señal local (densidad, k del hijo, dote recibida): mismo genoma, cuerpos distintos (ficha 5). |
| **Apoptosis** (morir por el conjunto) | Existe A MANO: O3 `cuerpos_term` y O4 `senescentes` vía `quiere_parir` (`:44-49`, `VOL_DECL :190`) | Un gen de morir con umbral sobre la densidad de parientes, que la selección prenda sola (ficha 6). |
| **Transferencia horizontal de genes** | No existe (la herencia va SOLO por `al_parir/nace`, `:20-22`) | Tomar un gen del muerto en la celda, o de un vecino vivo (ficha 7). |
| **Duplicación de genes (Ohno 1970)** | No existe (vector fijo) | Copiar un "slot" de órgano y dejar que la copia derive (ficha 1/8). |
| **Reina Roja** (parásitos, depredadores) | No existe. Las 4 letras valen SIEMPRE lo mismo (`organismo_f9c.py:149-150`); el mundo es el mismo de principio a fin | Que el veneno sea un LINAJE que se copia cuando lo muerden (ficha 3); un depredador que come cuerpos (ficha 9). |
| **Sexo / recombinación** | No: herencia clonal (`:466-471`) | Mezclar mitades de dos genomas del mismo linaje en la celda (ficha 12). |
| **Tasa de mutación evolucionable** | No: `p_mut`, `sigma` constantes de la corrida (`ECO_DEF :97`) | p y sigma como genes (ficha 11). |
| **Plasticidad / Baldwin / asimilación genética** | Aprende en vida (dos vías) y hereda lo vivido (lamarck). No hay gen que codifique el valor de una letra → Baldwin imposible por construcción | Ficha 10 (instinto). RONDA1 F8 (Hinton-Nowlan) lo toca de lado. |
| **Ciclo de la materia / cadáver** | No: el muerto desaparece (`:419-421`) | Que el muerto deje su E en la celda como objeto (ficha 13). Cierra el ciclo (Flow-Lenia conserva masa). |
| **Construcción de nicho** | Existe a medias: limpiar (morder lo malo) cambia el mundo, y de eso dependía el cruce de H-1 (ERR-104) | Que lo construido persista y vuelva a quien lo pagó (RONDA1 F4). |
| **Grandes transiciones (Maynard Smith & Szathmáry 1995):** replicadores→cromosomas; genes→células; procariota→eucariota; clonal→sexual; unicelular→multicelular; solitario→colonia; sociedad→lenguaje | El bicho está en el peldaño "célula": UN compartimento con un genoma. Ninguna transición ocurrió ni puede ocurrir con el motor de hoy | Cada ficha de abajo es un candidato a UNA transición: 2 (eucariota), 4–6 (multicelular), 12 (sexual), 7 (cromosoma: genes que viajan juntos o no). |
| **Lo abierto (Tierra, Avida, Lenia, Polyworld, POET)** | El lenguaje de órganos es una LISTA CERRADA de 7 + 2 nombres. Sólo se pueden prender | Que el lenguaje se extienda solo. Lejos; no se promete (bitácora §4, punto 4). Peldaño intermedio: gramática chica (ficha 1). |

**Lectura del mapa en una frase:** ECO ya tiene célula, división, herencia y selección; le faltan TODOS los mecanismos por los que
la biología hizo cosas nuevas (errores estructurales, endosimbiosis, coevolución, adhesión, diferenciación, HGT). Y le falta el
motor externo de novedad: un mundo que cambie porque lo que vive en él cambia.

---

## (b) FICHAS — ordenadas por cuánto rompen el molde (★ = mis tres favoritas)

Formato de cada ficha: idea en una frase · mecanismo mínimo con reglas locales · qué ERROR DE COPIA o EVENTO lo hace posible ·
predicción que podría FALLAR · control que la desmiente · costo · ¿la construyen los Opus del equipo?

### ★ Ficha 1 — El genoma como LISTA con errores de copia sobre una gramática chica (Ohno + gramática)
- **Idea:** dejar de prender órganos escritos y dejar que el genoma sea una lista de largo variable de "piezas" de una gramática
  chica, que la copia puede duplicar, borrar, invertir y fusionar. Lo nuevo nace del error, no del diseño.
- **Mecanismo mínimo:** genoma = lista de tuplas `(cuándo, qué, a quién, cómo)` para la transmisión (bitácora §4, punto 1: parto /
  en vida / al morir × entradas por signo, magnitud, recencia o necesidad × hijo / hermano / vecino × copiar, promediar, invertir,
  olvidar) MÁS tuplas `(patrón ∈ {−1,0,1}^6, peso)` para la boca (un órgano "dispara" si coincide en ≥ 3 píxeles). `ensena`
  y `filtra0` son dos puntos de ese espacio; la selección puede encontrar otros. El carro lee la lista y arma el órgano.
- **Error de copia:** en `muta()` (`motor_eco3.py:123`), además del log-normal por gen: con p_estr, UNA de {duplicar un slot,
  borrar uno, invertir el signo del peso o del "cómo", fusionar dos slots (OR de patrones, suma de pesos)}.
- **Predicción que puede fallar:** en w30 con corte, el banco de VIDA contiene ≥ 1 slot que NO está en la lista diseñada (ni
  `ensena` ni `filtra0`) y que expresa el 60 % de los vivos al final, contra ≤ 20 % en AZAR, en ≥ 15/20. FALLA si la selección sólo
  reencuentra `ensena`, o si el genoma se hincha sin función (ver juguete).
- **Control:** (i) sombras con la misma genealogía (ya existen, `:432-434`); (ii) AZAR (donante al azar); (iii) brazo PUNTO
  (misma gramática, sin errores estructurales: sólo perillas); (iv) el slot ganador, trasplantado a un FABRICA limpio, tiene que
  mejorarlo (que sea función y no pasajero).
- **Costo:** carro nuevo `FAMB_GRAM_ECO` (Python, w30, ~1–2 h por serie); el motor tiene que aceptar genomas de largo variable
  (hoy `np.array` fijo, `:160-171`): el gemelo numba NO lo soporta sin rehacerlo (listas de largo variable). Primero Python.
- **¿Opus?** Sí: creador (carro + gramática) y compilador (después, si la señal lo pide). Riesgo: sobre-diseñar la gramática;
  la regla es que cada primitiva sea una operación de UNA línea sobre la tabla o la retina.
- **Juguete (§D, `juguete_ohno.py`):** REFUTÓ que los errores estructurales aceleren la recuperación tras un cambio del mundo en un
  genoma de 4 slots, y REFUTÓ que la deriva hinche el genoma (con mi mezcla de operadores lo encoge). Lo que quedó: con selección
  el largo se sostiene en ~4 contra una deriva que lo baja a 2–3; la HGT sube el número de órganos distintos (97–119 contra
  61–100) sin subir el acierto. Lección: los errores estructurales dan MATERIAL, no velocidad; hace falta un mundo que lo cobre.

### ★ Ficha 2 — Endosimbiosis: tragar a otro linaje y quedárselo como órgano (Margulis)
- **Idea:** que un órgano nuevo venga de OTRO linaje, no del diseño: un cuerpo grande y torpe traga a uno chico que sabe algo, y
  desde entonces deciden juntos; si eso paga, la selección lo fija y el tragado pasa a heredarse con el que traga.
- **Mecanismo mínimo:** dos carros distintos en el mismo mundo (ECO ya corre varios linajes, `:76-80`). Los cuerpos pasan a ser
  OBJETOS visibles en la celda (hoy no lo son). Si la boca de un cuerpo muerde a un cuerpo de otro carro (una letra que no conoce),
  el mordido queda ADENTRO: su `actua()` se consulta y se suma al del anfitrión; cobra un upkeep fijo por paso; en el parto del
  anfitrión se copia al hijo con sus propios errores de copia (transmisión vertical); si el anfitrión muere, muere.
- **Evento:** un ERROR DE BOCA (morder lo que no se conoce) que no mata sino que incorpora. Es la "digestión fallida" de Margulis.
- **Predicción que puede fallar:** con selección, la fracción de anfitriones con simbionte al final ≥ 0.7 en ≥ 15/20; con deriva
  (muerte y parto al azar) < 0.5. FALLA si el upkeep la tira o si el simbionte libre se extingue antes de ser tragado.
- **Control:** (i) DERIVA (muerte al azar, mismo encuentro); (ii) SIN_TRAGAR; (iii) simbionte "mudo" (se traga pero no decide):
  si se fija igual, lo que se fija es el encuentro y no la función.
- **Costo:** ALTO en el motor (cuerpos como objetos; boca sobre cuerpos; `Cuerpo` con un hijo interno). Carro: bajo. Comparte
  código con la ficha 9 (depredador). Python, w30, ~2 h por serie. Sin gemelo al principio.
- **¿Opus?** Sí, pero es el que más pide un compilador que reescriba `run_solapadas` con cuidado (los rng por cuerpo, `:198-215`).
- **Juguete (§D3, `juguete_tragar.py`):** la función SÍ aparece (el anfitrión con simbionte acierta 0.68–0.89 sobre lo que no
  ve, contra 0.50), pero la fijación NO se puede leer: sin selección el simbionte llega a 1.00 por trinquete (se hereda y nunca
  se pierde). **Corrección obligatoria a esta ficha:** el simbionte debe poder PERDERSE (expulsión en el parto con p, o muerte
  del simbionte por su cuenta); si no, DERIVA y VIDA dan lo mismo y la ficha es ilegible.

### ★ Ficha 3 — Reina Roja: el veneno es un LINAJE que se copia cuando lo muerden
- **Idea:** el mundo de ECO se agota porque las letras valen siempre lo mismo; si el veneno evoluciona a parecerse a la comida,
  la boca no puede dejar de cambiar. Nadie juzga: el veneno que engaña deja más copias; el bicho que no se deja engañar, más hijos.
- **Mecanismo mínimo:** en el quimiostato (P7, `:31-40`), lo que se repone no es una letra al azar sino una COPIA (con 1 píxel
  mutado, p 0.3) de una letra mala que fue MORDIDA recientemente; las letras malas que nadie muerde en 200 pasos desaparecen. Las
  buenas siguen fijas (A y C). Prohibido igualar exactamente a una comida (mimetismo imperfecto).
- **Evento:** la letra deja de ser una constante del mundo y pasa a ser un replicador con error. Es Hillis (1990) y Zaman et al.
  (2014, PLoS Biol 12:e1002023: coevolución anfitrión-parásito en Avida → rasgos más complejos, ~10× más mutaciones de "switch").
- **Predicción que puede fallar:** (i) el número de órganos distintos en el banco sigue creciendo después de que en el mundo fijo se
  estanca (≥ 15/20); (ii) la novedad (fracción de órganos del final que no existían a T/2) es mayor que en el mundo fijo y que en
  el control RUIDO. FALLA si el veneno converge a un mimetismo perfecto y extingue todo, o si el bicho responde sólo con
  neofobia (no morder nada: entonces baja el acierto y no hay órganos nuevos).
- **Control:** RUIDO = el mundo cambia a la misma tasa pero al azar (no depende de quién fue mordido). Separa "el mundo cambia"
  de "el mundo me persigue". Y el mundo FIJO de hoy.
- **Costo:** BAJO-MEDIO: sólo la regla de reposición de `pista2`/`motor` (P7) y guardar qué letras se mordieron. Cabe en el gemelo.
- **¿Opus?** Sí, un creador solo. Es la ficha más barata de las tres favoritas y la que más acelera sin juez.
- **Juguete (§D2, `juguete_reina_roja.py`):** la novedad de órganos (recambio T/2 → T) fue mayor con veneno que evoluciona que con
  mundo fijo Y que con mundo que cambia al azar a la misma tasa, 5/5. El veneno se volvió parecido a la comida sin que nadie lo
  escribiera (mimetismo, 4/5). REFUTADO: no hay MÁS órganos distintos (hay menos: la persecución poda). Se paga con acierto.
  Aviso de instrumento: la primera versión del juguete no cambiaba nada (ver §D2); el control RUIDO fue lo que lo delató.

### Ficha 4 — Multicelularidad por "no soltarse": bolsa común de energía entre parientes
- **Idea:** los hijos ya nacen en la celda del padre (P1); falta que se queden y compartan. Un gen de adhesión hace que los cuerpos
  del mismo linaje en la misma celda (±1) PROMEDIEN su E y Ag al final de cada paso.
- **Mecanismo mínimo:** gen `adhesion` con umbral; tras el paso, para cada celda, los cuerpos del mismo linaje con `adhesion` ≥ 1.0
  ponen su E en una bolsa y la reparten parejo. Regla local: sólo la celda. Sin adhesión = hoy.
- **Evento:** ninguno de copia; es un error de "soltarse": la división que no termina (la hipótesis estándar de la
  multicelularidad, Bonner; Maynard Smith & Szathmáry, transición 5). Requiere que el hijo NO se disperse: hoy el mundo está bien
  mezclado (RONDA1 patrón 1), así que esta ficha depende de RONDA1 F4/F5 (localidad).
- **Predicción que puede fallar:** en quimiostato con parches (F4), `adhesion` se expresa en ≥ 80 % del banco de VIDA contra ≤ 30 %
  de AZAR, en ≥ 15/20; en mundo de comida abundante, neutro. FALLA si la bolsa premia al gorrón (el que no come vive de los otros:
  tragedia de los comunes) y la selección la apaga.
- **Control:** bolsa FORZADA entre linajes DISTINTOS (no parientes): Hamilton dice que no se fija; si se fija igual, la bolsa es un
  regalo del mundo y no cooperación. Sombras.
- **Costo:** BAJO en el motor (un bucle por celda tras el paso). Gemelo: fácil.
- **¿Opus?** Sí. Riesgo de trampa: que la bolsa sea "comida regalada" (ERR-104); hay que medir que la E total no cambie.

### Ficha 5 — Diferenciación: mismo genoma, cuerpos distintos (la expresión condicionada)
- **Idea:** hoy un órgano se prende si su gen ≥ 1.0, para TODOS los cuerpos del linaje igual. Si el umbral se compara con una SEÑAL
  LOCAL en vez de con una constante, el mismo genoma produce cuerpos distintos según dónde y cuándo nacen: división del trabajo.
- **Mecanismo mínimo:** cada gen de órgano lleva un segundo número, la "condición": 0 = constante (hoy), 1 = densidad de parientes
  en la celda al nacer, 2 = dote recibida, 3 = paridad del número de cuerpo k, 4 = E del padre al parir. El órgano se expresa si
  `gen ≥ 1.0` Y la condición se cumple. Un linaje puede así tener hijos "curiosos" y hijos "prudentes".
- **Error de copia:** mutar la condición (un entero) es una mutación puntual más en `muta()`.
- **Predicción que puede fallar:** con bolsa común (ficha 4), la fracción de linajes del banco que expresan un órgano en 20–80 % de
  sus cuerpos (ni todos ni ninguno) es ≥ 2× la de AZAR en ≥ 15/20. FALLA si sin bolsa común la diferenciación no paga (nadie
  quiere ser el prudente que no come) y con bolsa se vuelve gorronería (ficha 4).
- **Control:** condición barajada (la señal es un número al azar): si diferencia igual, es ruido y no división del trabajo.
- **Costo:** BAJO (carro + una línea en `ctx_genoma`). Gemelo: fácil.
- **¿Opus?** Sí. Es la ficha más barata que toca una transición mayor.

### Ficha 6 — Apoptosis que aparece sola: un gen de morir con umbral de densidad
- **Idea:** O3 cruza H-1 con muerte programada escrita por un LLM (`quiere_parir`, `cuerpos_term`). Que en vez de escribirla, la
  selección la PRENDA: un gen `apoptosis` con umbral sobre `vivos_linaje` (P5, `:44-49`): si hay más parientes vivos que el
  umbral, el cuerpo deja de comer (muere en ~200 pasos, como el Frankenstein herido).
- **Mecanismo mínimo:** el gen ya cabe en `GENES` (entero, piso 2, techo 50). El carro lee `info['vivos_linaje']` que la pista ya
  entrega. Nace apagado (techo).
- **Evento:** ninguno de copia; es una mutación puntual del umbral. Lo que lo hace posible es la BOLSA COMÚN (ficha 4) o el
  quimiostato con parches: morir sólo paga si lo que dejo lo come un pariente.
- **Predicción que puede fallar:** con bolsa común + quimiostato, el umbral de `apoptosis` en el banco de VIDA baja del techo en
  ≥ 15/20 contra AZAR; sin bolsa común, no se mueve. FALLA si el ERR-118 se cuela (fundadores repuestos), o si "morir" sólo
  reduce la competencia global y no la del pariente.
- **Control:** linajes MEZCLADOS en la celda (el que muere le deja la comida a un extraño): no debe prenderse. Sombras.
- **Costo:** MUY BAJO (gen + 5 líneas de carro). Gemelo: fácil.
- **¿Opus?** Sí, hasta un Sonnet. Valor: convierte lo que O3 hace a mano en algo que la selección eligió, con control de parentesco.

### Ficha 7 — Transferencia horizontal: tomar un gen del muerto o del vecino
- **Idea:** la herencia va sólo de padre a hijo (`:20-22`). Que un gen (o una entrada de la tabla) pueda saltar entre cuerpos que
  se cruzan: el muerto deja UN gen en su celda; el que nace o pasa por ahí lo toma con p.
- **Mecanismo mínimo:** al morir (`:415-421`), la celda guarda `(gen_j, valor)` de un gen al azar del muerto; al nacer un hijo en
  esa celda (P1: nace donde el padre), con p_hgt reemplaza su gen_j por ese valor. Para la tabla: `ensena` hacia el vecino vivo en
  la misma celda (fase 5 ya tiene señal honesta por conducta).
- **Evento:** el cadáver como plásmido. Es el mecanismo que en bacterias mueve genes más rápido que la descendencia.
- **Predicción que puede fallar:** el tiempo hasta que el 90 % del banco expresa `ensena` (ECO v2.1) baja ≥ 30 % con HGT en
  ≥ 15/20. FALLA si HGT también propaga genes malos y la neta es cero (el juguete sugiere eso: más diversidad, mismo acierto).
- **Control:** HGT BARAJADA: el gen que se toma sale de un cuerpo al azar del mundo, no del muerto de la celda. Si acelera igual,
  no es horizontal, es mezcla global (y eso sí es trampa: un juez implícito).
- **Costo:** BAJO (motor: un dict celda→gen). Gemelo: fácil.
- **¿Opus?** Sí. **Juguete (§D):** el brazo `ESTRUCTURA_HGT` subió los órganos distintos (97–119 contra 61–100) y el largo del
  genoma (5–6 contra 4) sin subir el acierto: material, no función. La predicción P3 del juguete (HGT no mejora) se cumplió.

### Ficha 8 — Duplicación y divergencia como PRIMER paso a un órgano nuevo (Ohno 1970, versión mínima sin gramática)
- **Idea:** antes de la gramática (ficha 1), el caso más chico: permitir que un gen de órgano YA existente se DUPLIQUE con sus
  perillas propias, de modo que un linaje tenga dos copias de `interruptor` con umbrales `PELIGRO` distintos, o dos `herencia`
  con filtros distintos. La copia deriva libre mientras la original conserva la función.
- **Mecanismo mínimo:** el genoma pasa a tener "slots" de órgano `(nombre, umbral, perillas propias)`; `muta()` puede copiar un
  slot (p_dup) o borrarlo (p_del). El carro aplica cada slot expresado en secuencia (dos interruptores = dos vetos).
- **Error de copia:** duplicación en tándem. Avida lo produjo sin que nadie lo pidiera (la copia que sigue de largo; Lehman et al.
  2018, arXiv:1803.03453 §"double-length organisms").
- **Predicción que puede fallar:** en w30, ≥ 15/20 bancos de VIDA tienen ≥ 1 linaje con dos copias de un órgano con perillas que
  difieren > 2 sigma, y las dos expresadas; en AZAR ≤ 5/20. FALLA si la copia siempre se borra (costo) o si las dos copias son
  redundantes (nunca divergen: entonces sólo hay robustez, que también es un resultado de Ohno, pero no novedad).
- **Control:** DUPLICACIÓN SIN DIVERGENCIA (la copia queda ligada a la original: mismas perillas): mide qué da la redundancia sola.
- **Costo:** MEDIO (genoma de largo variable: rompe el gemelo; Python w30 primero).
- **¿Opus?** Sí. Es el peldaño 2 de la bitácora §4 y la mitad de la ficha 1.

### Ficha 9 — Depredador: un linaje que come cuerpos
- **Idea:** Reina Roja versión 2: un carro cuya comida son los otros cuerpos de la celda. Muerde a un cuerpo → le quita 0.4 de E.
  Las presas seleccionan huir, vetar, agruparse; el depredador selecciona reconocer presas. Ecología en vez de mundo.
- **Mecanismo mínimo:** los cuerpos como objetos visibles (comparte código con la ficha 2), letra "cuerpo" con retina propia (p. ej.
  el genoma del otro proyectado a 6 bits: así el depredador puede aprender a reconocer linajes). El depredador no come letras.
- **Evento:** el error de boca de la ficha 2, con el signo contrario: en vez de incorporar, extrae.
- **Predicción que puede fallar:** con depredador, los genomas de presa siguen moviéndose (varianza entre bancos sucesivos) tras
  el punto en que el mundo sin depredador se estanca, en ≥ 15/20. FALLA por extinción total (el clásico Lotka-Volterra roto) o
  porque la presa responde con una sola perilla (más `aversion`) y nada más.
- **Control:** DEPREDADOR CIEGO (muerde cuerpos al azar, sin aprender ni ganar E): mide el efecto de la mortalidad extra sin la
  persecución.
- **Costo:** ALTO (mismo que ficha 2). Después de la ficha 2, BAJO.
- **¿Opus?** Sí, tras la 2.

### Ficha 10 — Instinto: que el valor de una letra pueda escribirse en el genoma (Baldwin visible)
- **Idea:** hoy no hay ningún gen que diga "B es malo": todo se aprende o se hereda por la tabla (lamarck). Ocho genes nuevos
  (`prior_A0..prior_D1`: sesgo innato por letra y necesidad, nacen en 0) dejan que la selección ASIMILE lo que la tabla enseña.
  Predicción de Hinton & Nowlan (1987) y de Waddington: en mundo fijo el instinto sube y `ensena` se apaga; en Reina Roja no.
- **Mecanismo mínimo:** el carro suma el prior al valor leído por la puerta (una línea en `_fk_val`/boca). Los 8 genes van en
  `GENES` con piso −3 y techo +3.
- **Evento:** ninguno de copia. Lo que lo hace posible es tener por primera vez DOS canales de herencia (genoma y tabla) que
  compiten por la misma función.
- **Predicción que puede fallar:** en w30 fijo, `prior_B0` y `prior_D1` del banco de VIDA quedan < −1 en ≥ 15/20 (AZAR ≈ 0) Y la
  expresión de `ensena` baja respecto de ECO v2.1 (97–99 %) a < 70 %. FALLA si `ensena` sigue en 99 % (la tabla es tan buena
  que el instinto es neutro: entonces no hay Baldwin, hay Lamarck estable, y eso también se aprende).
- **Control:** mundo que INVIERTE B y A cada 20 000 pasos: el prior no debe fijarse y `ensena` debe quedarse. Sombras.
- **Costo:** MUY BAJO. Gemelo: trivial (8 floats).
- **¿Opus?** Sí, incluso Sonnet. Es la ficha que más dice sobre "cerebro entrenado" (memoria: efecto Baldwin) con menos costo.

### Ficha 11 — La tasa de mutación como gen (mutador evolucionable)
- **Idea:** `p_mut` y `sigma` son constantes de la corrida. Que sean genes: un linaje puede volverse más o menos mutable.
  Teoría: en mundo fijo baja (reducción de la tasa, Drake); en Reina Roja se mantiene alta (Zaman 2014 lo ve en Avida).
- **Mecanismo mínimo:** dos genes `p_mut_g`, `sigma_g`; `muta()` los lee del genoma del padre (`:471`). Sombras igual.
- **Error de copia:** es el gen que gobierna los demás errores. Sin él, "acelerar" la evolución es siempre una decisión nuestra.
- **Predicción que puede fallar:** mundo fijo → `p_mut_g` del banco cae bajo el inicial en ≥ 15/20; Reina Roja (ficha 3) → no cae.
  FALLA si en mundo fijo sube (los mutadores viajan con las mutaciones buenas: "mutator hitchhiking", que también existe).
- **Control:** sombras (ya calculan la deriva de un gen neutral).
- **Costo:** MUY BAJO. Gemelo: trivial.
- **¿Opus?** Sí. Es la manera más honesta de "acelerar sin juez": que el mundo decida cuánto error conviene.

### Ficha 12 — Recombinación mínima (sexo de bolsillo)
- **Idea:** al parir, con p, el hijo toma la mitad de sus genes de OTRO cuerpo vivo del mismo linaje en la misma celda.
- **Mecanismo mínimo:** máscara aleatoria de 25 bits; genes 1 del padre, 0 del vecino. Sin vecino: clonal.
- **Evento:** fusión de dos genomas (la 4ª transición de MS&S).
- **Predicción que puede fallar:** combinaciones que ECO v3 no juntó (`herencia` + `interruptor` expresados a la vez en el mismo
  cuerpo) aparecen antes en el banco (≥ 15/20). FALLA si rompe paquetes coadaptados (la recombinación deshace lo que junta).
- **Control:** recombinación con un genoma AL AZAR del banco (no del vecino): si mejora igual, es mezcla global, no sexo local.
- **Costo:** BAJO. **¿Opus?** Sí. Rompe poco el molde: la biología tardó mil millones de años y aquí es una máscara.

### Ficha 13 — El cadáver como comida: cerrar el ciclo de la materia
- **Idea:** el muerto desaparece (`:419-421`). Que deje en su celda un objeto con letra nueva `M` (cadáver) que devuelve la E que
  le quedaba (o una fracción). Con eso la materia circula: hay necrofagia, y con la ficha 9, depredación con recompensa real.
- **Mecanismo mínimo:** al morir, `objs[pos] = 'M'` con valor `+0.5*E_restante`; retina de `M` = un quinto patrón de 6 bits.
- **Evento:** ninguno de copia. Lo que cambia es que la energía del sistema deja de escaparse por la muerte.
- **Predicción que puede fallar:** en quimiostato la capacidad de carga sube y los linajes que persisten sin refundación pasan de
  0–3/27 (Frankenstein (b)) a ≥ 6/27. FALLA si el cadáver tapa el mundo como el veneno (ERR-104 al revés) o si aparece un
  "canibalismo" que premia matar parientes.
- **Control:** el cadáver con valor 0 (sólo ocupa celda): mide el efecto de ocupar sin alimentar.
- **Costo:** MUY BAJO. **¿Opus?** Sí. Es lo más raro de la lista y quizá lo más barato de todo.

### Ficha 14 — Errores de copia en el CUERPO, no en el genoma: la tabla se hereda con ruido
- **Idea:** el director dijo "limitamos por lo que hay y no por los errores"; el genoma no es el único lugar donde copiar mal
  crea. `ensena` copia la tabla vivida al hijo SIN ERROR. Que la copie con errores (una entrada borrada, una duplicada con otra
  necesidad, una invertida de signo) con una tasa que sea un GEN. Es la variación de la herencia cultural.
- **Mecanismo mínimo:** en `_fk_parir` (`organos_frank.py:145-153`), antes de devolver `pk['tabla']`, aplicar con p_cult una
  operación de {borrar, duplicar cambiando la necesidad, invertir el signo de R}. `p_cult` es un gen.
- **Error de copia:** el mismo trío que en el genoma, pero sobre la memoria del linaje.
- **Predicción que puede fallar:** en Reina Roja (ficha 3), `p_cult` del banco queda > 0 (la copia imperfecta gana a la perfecta);
  en mundo fijo cae a 0. FALLA si en Reina Roja también cae a 0: el hijo prefiere aprender solo que heredar errores.
- **Control:** ruido barajado (la entrada que se borra no depende de nada): si da lo mismo, no hay selección sobre QUÉ error.
- **Costo:** BAJO (carro). **¿Opus?** Sí. Rompe el molde donde nadie mira: la herencia lamarckiana que ya FUNCIONA (v2.1) hoy
  es una fotocopia; la biología nunca fotocopia.

---

## (c) ¿Qué tan lejos estamos de la evolución darwiniana y abierta? (una página honesta)

**Lo que YA es darwiniano en ECO (leído en el motor, no imaginado).** Hay herencia (el hijo copia el genoma del padre,
`motor_eco3.py:466-471`), variación (mutación log-normal por gen, `:123-135`, con sombras neutrales de la misma genealogía,
`:473-475`), y reproducción diferencial por la energía (ventana de viabilidad, dote, `:440-459`) sin ningún juez que puntúe.
El control AZAR (`donante='azar'`, el banco guarda el genoma NUEVO, `:438,477`) es deriva pura y honesta. Con eso ECO v2.1 mostró
lo que la letra pedía: un rasgo que nace apagado en todos y que sólo sirve al hijo se prende por selección en 97–99 % del banco,
contra 12–47 % por deriva, en tres mundos, serie y réplica (bitácora §1i). **Eso es selección natural de verdad**, a la escala de
una perilla con umbral. No hay que quitarle mérito: la mayoría de los "algoritmos evolutivos" no pasan este control.

**Lo que NO es darwiniano todavía, o lo es a medias.**
1. **El espacio de fenotipos está cerrado por construcción.** El genoma es un vector de 25 números con pisos y techos que nosotros
   escribimos (`GENES :84-92`, `rangos :118`). La selección puede moverse DENTRO de la caja; nada que no esté en la caja puede
   aparecer. Los "órganos" son programas escritos por nosotros con un interruptor. Por eso ECO hasta hoy PRENDE y no CREA
   (bitácora §4). Sin errores estructurales (fichas 1, 8) o sin gramática, esto no cambia por más series que se corran.
2. **El mundo es una constante.** Cuatro letras con valor fijo (`organismo_f9c.py:149-150`), reposición al azar, sin coevolución.
   Un paisaje fijo se sube una vez y se acaba: después sólo hay deriva. La biología nunca tuvo eso: el paisaje lo hacen los otros
   (Reina Roja). Fichas 3, 9, 13.
3. **No hay ecología entre cuerpos.** Los cuerpos sólo se tocan por la comida compartida (P4). No hay depredación, ni simbiosis,
   ni parentesco que importe, ni localidad (RONDA1 patrón 1: "todos ven todo, lo repuesto cae en todo L, el turno se baraja"). Sin
   localidad no hay multicelularidad ni cooperación posibles (fichas 2, 4, 5, 6). Esto es lo más lejano de "la célula humana".
4. **El vivero es una muleta.** E9 (`:19-25`, `:430-439`) refunda linajes extintos desde el banco hasta `t_corte`. No es un juez
   (el genoma sale al azar del banco), pero tampoco es natural: en la naturaleza lo extinto no vuelve. ECO lo declara y lo corta;
   bien. El tope de 300 cuerpos (P4) también es una constante nuestra, declarada.
5. **La tasa de error la ponemos nosotros.** `p_mut = 0.05`, `sigma = 0.15` (RONDA1 F1). Mientras eso sea una constante, "acelerar
   la evolución" es una decisión del coordinador. Ficha 11.
6. **Dos canales de herencia sin competencia.** La tabla (lamarck, `ensena`) FUNCIONA; el genoma no puede codificar valores de
   letras. Así no hay asimilación genética ni Baldwin: ficha 10.

**Qué acelera y qué hace trampa (mi lista, para que el equipo la discuta).**
- *Acelera sin juez:* poblaciones grandes (el gemelo numba ×42–48, bitácora §1g); mundos que cambian PORQUE lo que vive cambia
  (ficha 3, 9); errores estructurales y tasa de error evolucionable (fichas 1, 8, 11); localidad y parches (RONDA1 F4/F5);
  transferencia horizontal (ficha 7); cerrar el ciclo de la materia (ficha 13). Todo esto cambia QUÉ puede pasar, no QUIÉN gana.
- *Zona gris, declararla siempre:* el vivero hasta t_corte; el tope de cuerpos; un mundo que cambia al azar en un reloj nuestro
  (control RUIDO: sirve como control, no como motor); "mundos escalonados" tipo Avida donde nosotros decidimos qué paga (Lenski
  2003): acelera, pero el escalón lo pusimos nosotros.
- *Trampa (juez disfrazado):* elegir el genoma fundador entre los mejores (bitácora §1k lo retiró, bien); mover umbrales tras ver
  el dato (regla 11); pagar con comida algo que sólo el diseñador sabe que conviene (ERR-104); refundar con el MEJOR del banco
  (E9 lo evita: al azar); medir "novedad" con una función que premia lo que queremos ver (Lehman & Stanley: el objetivo engaña).

**Dónde está ECO en la escala de lo abierto.** Tierra y Avida tienen genomas de largo variable que se EJECUTAN en una máquina
virtual: la novedad ocurre a nivel de instrucción (parásitos en la primera corrida de Ray; EQU en Lenski 2003; complejidad por
coevolución en Zaman 2014). Lenia/Flow-Lenia tienen conservación de masa y patrones que nadie escribió. POET genera problemas al
ritmo de las soluciones (con un juez de "aprendible", declarado). ECO hoy es un **algoritmo genético de perillas con interruptores,
sobre un mundo fijo y bien mezclado, con control de deriva honesto**. Está en "microevolución dentro de una caja". Es un peldaño
real y replicado, y es el peldaño 0 de lo abierto. Ninguna transición mayor (MS&S) es posible con el motor de hoy, por
construcción, y eso no lo arregla ninguna serie: lo arregla cambiar QUÉ puede copiarse mal.

**Lo que propondría, en orden, si me tocara a mí (no es una decisión; es la opinión del explorador):** primero lo MUY BARATO que
cambia la pregunta (fichas 11, 10, 13, 6: cuatro genes y tres reglas de una línea, todo cabe en el gemelo); en paralelo la Reina
Roja (ficha 3), que es el motor externo de novedad más barato y con el control más limpio (RUIDO); después la gramática con
errores estructurales (fichas 8 → 1), que es donde de verdad se CREA y donde el gemelo se rompe; y las fichas de ecología (2, 9,
4, 5) sólo cuando haya localidad (RONDA1 F4/F5), porque sin celdas que importen no hay ni simbiosis ni cuerpo multicelular.
La medida que manda en todas: **lo que gana no está en la lista de lo diseñado, y trasplantado a un cuerpo limpio, sirve.**

---

## (D) Los juguetes: predicciones escritas antes, resultados, y lo refutado

Todo lo de esta sección es EXPLORATORIO y de bolsillo (mundo abstracto con la retina del bicho, no el motor de ECO). Sirve para
saber si una idea respira, no para declarar nada. Salidas completas en `salida_ohno.txt`, `salida_reina_roja.txt`,
`salida_tragar.txt`.

### D1. `juguete_ohno.py` — errores de copia estructurales contra perillas (semillas 23001–23005, T 4000, tope 200, 165 s)
Mundo: una letra por paso, morder suma su valor, costo 0.02, parto en E ≥ 2, cambio de mundo en T/2 (4 letras nuevas).
Brazos: PUNTO (4 órganos fijos, sólo perillas), ESTRUCTURA (+ dup/del/inv/fus), ESTRUCTURA_HGT (+ toma un órgano del muerto),
DERIVA (ESTRUCTURA sin selección).

| brazo | acierto antes del cambio | acierto final | recupera ≥ 0.8 (t_rec) | largo final del genoma | órganos distintos |
|---|---|---|---|---|---|
| PUNTO | 0.64–0.80 | 0.63–0.84 | 1/5 (800) | 4.0 (fijo) | 61–99 |
| ESTRUCTURA | 0.69–0.74 | 0.60–0.71 | 1/5 (1600) | 3.7–4.2 | 66–100 |
| ESTRUCTURA_HGT | 0.72–0.77 | 0.59–0.69 | 0/5 | 5.2–6.1 | 97–119 |
| DERIVA | 0.39–0.58 | 0.44–0.51 | 0/5 | 2.1–3.3 | 54–86 |

- **P1 REFUTADA:** ESTRUCTURA no recupera más rápido que PUNTO (1/5 contra 1/5, y más lento). Casi nadie recupera ≥ 0.8: el techo
  del juguete es ~0.7 (la boca de umbral 3 sobre patrones de 3 píxeles es tosca). Lección: los errores estructurales no dan
  velocidad por sí solos; un genoma de 4 slots ya tiene suficiente con mover perillas.
- **P2 REFUTADA en su segunda mitad:** la deriva NO hincha el genoma, lo ENCOGE (2.1–3.3). Causa que veo: mi mezcla de operadores
  tiene dos que acortan (del, fus) y uno que alarga (dup): la deriva estructural tiene una DIRECCIÓN que la fija el operador, no
  la biología. Lo que quedó de interesante: con selección el largo se sostiene en ~4 contra esa deriva → hay selección por
  conservar órganos, débil pero visible. Aviso para la ficha 1: la mezcla de operadores es una decisión de diseño que sesga; hay
  que declararla y hacer el control DERIVA siempre.
- **P3 SE CUMPLE:** HGT no mejora el acierto. Pero sube los órganos distintos (97–119 contra 61–100) y el largo (5–6): material sin
  función. Coincide con lo que la ficha 7 predice como fallo posible.
- **P4 SE CUMPLE:** DERIVA nunca pasa de 0.51.

### D2. `juguete_reina_roja.py` — el veneno que evoluciona (semillas 23011–23015, T 4000, 131 s)
Mundo: 2 comidas fijas (A, C) y una POBLACIÓN de 40 venenos con patrón propio. FIJO: los venenos son B y D y no cambian.
REINA_ROJA: el veneno mordido se copia con error (1 píxel, p 0.3) sobre el veneno menos mordido; no puede igualar a una comida.
RUIDO: la población de venenos cambia a la misma tasa pero al azar. Bichos con genoma ESTRUCTURA (dup/del/inv/fus).

**Error de instrumento, declarado:** la primera versión reemplazaba "un veneno que nadie mordió en 200 pasos"; con ~200 cuerpos
todos los venenos se muerden cada paso y eso nunca ocurría: `cambiosV = 0` y el brazo salió IDÉNTICO a FIJO
(`salida_reina_roja_v0_bug.txt`). Se corrigió (reemplaza al menos mordido, p 0.01 por mordida) y se volvió a correr.

| brazo | acierto final | órganos distintos | novedad (T/2 → T) | cambios del veneno | Hamming veneno→comida | venenos distintos |
|---|---|---|---|---|---|---|
| FIJO | 0.64–0.73 | 108–123 | 0.40–0.46 | 0 | 3.00 | 2 |
| REINA_ROJA | 0.56–0.66 | 73–100 | **0.48–0.55** | 1955–2271 | **1.40–2.10** | 6–15 |
| RUIDO | 0.51–0.70 | 62–115 | 0.35–0.47 | 2387–2427 | 1.93–2.90 | 12–21 |

- **P1 REFUTADA:** REINA_ROJA tiene MENOS órganos distintos que FIJO (73–100 contra 108–123), no más. La persecución poda: el
  bicho que no distingue muere; la diversidad que sobrevive en el mundo fijo es la que nadie castiga.
- **P2 SE CUMPLE 5/5:** la NOVEDAD (fracción de órganos del final que no existían a T/2) es mayor en REINA_ROJA que en FIJO y que
  en RUIDO en las 5 semillas. El mundo que persigue renueva más que el mundo que cambia al azar A LA MISMA TASA. Es lo que la
  ficha 3 necesita que sea cierto, en versión de bolsillo.
- **P3 SE CUMPLE 5/5:** la Reina Roja se paga: acierto menor que en FIJO. Correr para quedarse en el sitio.
- **P4 PARCIAL / REFUTADA:** RUIDO no queda "entre los dos"; queda igual o debajo de FIJO en novedad. Cambiar el mundo al azar no
  renueva al bicho; perseguirlo sí.
- **P5 SE CUMPLE 4/5:** el veneno del final se parece MÁS a la comida (Hamming 1.40–2.10) que en RUIDO (1.93–2.90). **Nadie escribió
  "mimetismo"**: apareció porque el veneno mordido deja copias. Es el único lugar de los tres juguetes donde una estructura que no
  estaba en el diseño apareció sola por selección (del lado del veneno, no del bicho).

### D3. `juguete_tragar.py` — endosimbiosis de bolsillo (semillas 23021–23025, T 4000, **418 s: se pasó de los 5 min**, no se repitió)
Mundo: GRANDES (ven sólo 2 píxeles: no distinguen agua C de sal D) y CHICOS (ven todo, frágiles). En TRAGAR, un grande que muerde
a un chico (retina desconocida) se lo queda adentro: deciden juntos, upkeep 0.01/paso, el chico se copia al hijo del grande.

| brazo | fracción de grandes con simbionte (mitad → final) | tragados | acierto sobre C/D con simbionte | sin simbionte |
|---|---|---|---|---|
| SIN_TRAGAR | 0 → 0 | 0 | — | 0.50 |
| TRAGAR (selección) | 0.23→0.33, 0.59→0.55, 0.11→0.30, 0.25→0.32, 0.84→0.86 | 54–119 | **0.68–0.89** | 0.50 |
| TRAGAR_DERIVA | 1.00 en 5/5 | 47–114 | 0.47–0.53 | — |

- **P1 REFUTADA:** con selección la fracción con simbionte llega a ≥ 0.7 sólo en 1/5.
- **P2 REFUTADA AL REVÉS, y es la lección más útil de los tres juguetes:** sin selección la fracción llega a **1.00 en 5/5**. El
  simbionte se hereda y nunca se pierde: es un estado absorbente, un TRINQUETE. "Fracción con simbionte" no mide selección mientras
  no exista un mecanismo de PÉRDIDA (expulsión en el parto con p). Con la pérdida, la deriva daría un equilibrio encuentro/pérdida y
  la selección tendría que superarlo. Va a la ficha 2 como control obligatorio; sin él, cualquier resultado de endosimbiosis sería
  ilegible (como ERR-118 con los fundadores repuestos).
- **P3 SE CUMPLE 5/5:** los grandes con simbionte aciertan 0.68–0.89 sobre agua/sal contra 0.50 sin él. El tragado sí le presta al
  anfitrión un sentido que no tenía: la función existe.
- **P4 REFUTADA:** el linaje chico libre sigue en su tope (150) en todos los brazos.
- **P5 SE CUMPLE:** el upkeep no purga al simbionte (la fracción no cae; sube despacio).
- Lectura honesta: en TRAGAR la selección mantiene al simbionte en frecuencias intermedias (0.3–0.86) mientras la deriva lo lleva a
  1.0: o sea, la selección está frenando el trinquete en la mayoría de las semillas, aunque el simbionte ayude en C/D. Sospecho que
  los órganos del chico también disparan sobre A/B y estorban la boca del grande (la boca conjunta suma sin ponderar), y que los
  grandes que tragan son los mismos que muerden lo desconocido (y el veneno). No lo verifiqué.

### D4. Cuenta de predicciones y lo que NO pude verificar
**14 predicciones, 7 refutadas:** Ohno P1, P2; Reina Roja P1, P4; Tragar P1, P2, P4. Se cumplen: Ohno P3, P4; Reina Roja P2, P3,
P5; Tragar P3, P5. Dos errores de instrumento míos: la Reina Roja que no cambiaba nada (delatada por el control RUIDO) y la
fijación por trinquete en tragar (delatada por el control DERIVA). Los dos los encontró un control, no yo: ésa es la razón de
que cada ficha lleve el suyo. Y un fallo de presupuesto: `juguete_tragar.py` tardó 418 s (límite 300 s).

- Nada de esto se probó en el motor de ECO ni con los carros reales: los juguetes usan una boca de juguete. El costo de las fichas
  es estimado por lectura del motor, no medido.
- No abrí los PDF: Ohno 1970, Margulis 1970, Maynard Smith & Szathmáry 1995, Hinton & Nowlan 1987 y Hillis 1990 los cito de
  memoria; Zaman et al. 2014 (PLoS Biol 12:e1002023) y Lehman et al. 2018 (arXiv:1803.03453) los verifiqué hoy a nivel de ficha
  por búsqueda web; Symbulation (Vostinar, alife.org/encyclopedia) es la plataforma que ya modela endosimbiosis digital con
  transmisión vertical, y es el precedente más cercano de la ficha 2.
- No medí cuánto rompe el gemelo numba un genoma de largo variable; lo afirmo por leer que el genoma es `np.array` de forma fija
  (`motor_eco3.py:160-171`).

### Fuentes web consultadas hoy (tres búsquedas)
- Zaman, Meyer, Devangam, Bryson, Lenski & Ofria 2014, *Coevolution Drives the Emergence of Complex Traits and Promotes Evolvability*,
  PLoS Biology 12(12):e1002023 — https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1002023
- Lehman et al. 2018, *The Surprising Creativity of Digital Evolution* (anécdota de los organismos de doble largo en Avida) —
  https://arxiv.org/pdf/1803.03453
- Symbulation (plataforma de endosimbiosis digital, Vostinar) — https://alife.org/encyclopedia/software-platforms/symbulation/
- *Gene duplications drive the evolution of complex traits and regulation*, ECAL 2017 — https://direct.mit.edu/isal/proceedings/ecal2017/29/257/99588
- *Gene divergence and pathway duplication in the metabolic network of yeast and digital organisms* — https://pmc.ncbi.nlm.nih.gov/articles/PMC2817152/
