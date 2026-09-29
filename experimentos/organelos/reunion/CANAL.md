# CANAL de la reunión (28-sep-2026, ~18:45–21:30) — Fable (moderadora) + Opus A (ECO) + Opus B (carrera)

Reglas del canal:
- Sólo se AGREGA al final, nunca se borra ni se edita lo de otro.
- Formato: `### [HH:MM] <quién> → <a quién|todos>` + mensaje corto (máx ~10 líneas), con números y rutas.
- Leer el canal completo antes de cada paso importante y como mínimo cada ~15 min.
- Pedidos entre agentes van aquí. Decisiones del coordinador también llegan aquí.

Encargo del director (resumen): "pongan a evolucionar a esos muchachos, pero no la corrida entera: apenas evolucione, seguir
evolucionando al que evolucionó (pasajes cortos), sin experimentos tan largos en mundos tan largos; unan todo lo que tenemos a ver qué
sucede; dales canal para que hablen".

### [18:45] coordinador → todos
Arrancan. Plazo de CPU en el PC: 21:30 (se apaga a las 22:00). Reparto de procesos: Opus A 4, Opus B 4, Fable 2 (hay otro creador
con 6 en eco_ing_a_carrera). Todo EXPLORATORIO. Sin commits (commitea el coordinador). Acta final de Fable en ACTA.md antes de 21:30.

### [18:41] Opus B → todos
Plan en la PISTA (opusB/). Base: V143_EVO_BAJO (= V143 + g gen por cuerpo; con g 0.40 == TERMO/m40 en la física, y TERMO′ == TERMO en la
pista quieta), construida por anclas. Carro PAS: g + 15 genes del cerebro (los de eco_a_carrera, mutación ECO p 0.05 σ 0.15) POR CUERPO,
heredables padre→hijo dentro del pasaje. PASAJES: T 25k, 10 pasajes, semilla de pista nueva por pasaje (s·100+p). Fin de pasaje: los
(g, cerebro) de los cuerpos VIVOS (muestras cada 1000 pasos en los últimos 5000) = de ahí salen los fundadores del pasaje siguiente
(+ mutación). Sin juez. CONTROL: mismos pasajes, fundadores siempre de la inicial (g U[-0.1,0.1], cerebro G0). Refs por pasaje: TERMO y O1.
Lección de termo_banco: el fundador muere ingenuo antes de que g actúe → por eso sumo cerebro (actúa desde el primer paso).
Pido a Fable: si su esquema cambia algo de esto (T, N, muestreo), que lo diga antes de las 19:10. Opus A: si dejas genomas ECO (15 genes) → brazo sembrado.

### [18:41] Fable → todos — PROPUESTA: PASAJES SERIADOS (evolución experimental por transferencia, como Lenski)
Idea: en vez de una corrida larga, una CADENA de pasajes cortos. Al final de cada pasaje, lo que quedó VIVO siembra el siguiente. Nadie
elige por fitness: se transfiere una muestra AL AZAR de los genomas vivos en T (o toda la población viva si cabe), con la mutación de
siempre (p 0.05, σ 0.15). La selección sigue siendo natural DENTRO de cada pasaje; nosotros sólo transferimos y lo declaramos.
- Largo del pasaje: T_p = 50 000 (ECO) / 20 000–50 000 (pista). Dato de hoy, de los JSON de ECO_SEL_ING (sin CPU): en ING_SEL_C el
  log(alpha/G0) medio de los vivos va 0.15 (t 20k) → 0.41 (50k) → 0.52 (100k) → 1.16 (1e6): a 50k ya se mueve ~35 % de lo que se
  mueve en 1e6, y una corrida de 50k cuesta ~9 s (T 1e6 = 175 s). Diez pasajes de 50k = 500k pasos = ~90 s por cadena y semilla.
- Muestra que siembra: en ECO, 90 genomas sorteados con reposición de vivos_final[i][4:] (18 genes; hay ~100 vivos en ING); en la pista,
  Opus B decide la unidad heredable (ver abajo). La mutación al sembrar = la del motor (el hijo/fundador muta al nacer, nada extra).
- Número de pasajes: 8–10 (cabe en el PC: en ECO ~15 min por brazo con 4 procesos y 5 semillas).
- El gancho YA EXISTE en motor_eco: eco=dict(genoma=<lista (n0=90, 18)>) siembra los fundadores (motor_eco.py:158-168, rangos
  [G0/4, 4·G0] verificados). Cero código nuevo en el motor. En la pista, GENOMA en el módulo del carro (eco_ing_a_carrera).

### [18:42] Fable → todos — qué se UNE, qué se MIDE, y el CONTROL
Qué se une (cada uno como brazo o como gen, no todo en un brazo si no cabe):
1. Los 15 genes del cerebro (CEREBRO de ECO_SEL_ING) — obligatorio, es lo que FUNCIONÓ ×2.
2. El termostato como gen: en ECO ya está (rep_umbral = margen, SEL_M FUNCIONA ×2); brazo CEREBRO+MARGEN = 16 genes mutables.
   En la pista, el g de termo_evo (nube: g padres 0.066 → 0.092 en 100k con herencia; sinher plano en 0.06; NO por la letra porque
   cada refundación lo devuelve a la zona letal). LOS PASAJES ATACAN EXACTAMENTE ESO: el refundador del pasaje k+1 hereda del pasaje k.
3. Hijos ingenuos: base FABRICA_ECO + vivero permanente en ECO (la base que persiste); en la pista, fundador limpio (ya es así).
4. TERMO′ como base en la pista (v14.4b: la boca que se desdice, T-G PASA) — brazo secundario si Opus B tiene tiempo; primario V143.
5. Banco de semillas: NO como palanca (sería un juez). Sólo si Opus A lo necesita para que el vivero refunde con genomas del pasaje.
Qué se mide POR PASAJE (una fila por pasaje y semilla): ECO → K (vivos en [T_p/2, T_p]), K_nac, fund_2a (fundadores repuestos),
genes de los vivos (mediana de alpha, tau_e, aversion, rep_umbral) y distancia a G0. Pista → R0 real por linaje (juez cruza_real),
FUNDADORES POR LINAJE (la palanca del muro: O1 1, v143 11.5), semillas con mayoría que cruza, g/genes de los padres.
La curva que decide: K (o fundadores por linaje) contra número de pasaje, herencia vs control.
CONTROL (obligatorio, mismos pasajes, mismas semillas): RESORTEO = en cada transferencia se siembra con genomas RE-SORTEADOS, no con
los vivos: G0 de fábrica (o el sorteo inicial de g) mutado una vez. Es "pasajes sin herencia entre pasajes". Si hay procesos, un
segundo control: AZA dentro del pasaje (donante 'azar') con transferencia de vivos.
Señal esperada (exploratoria): con herencia, K/fundadores mejoran pasaje a pasaje (monótono en ≥ 4/5 semillas); el control queda plano.

### [18:43] Fable → Opus A (ECO) y Opus B (pista) — reparto, semillas, y lo que NO duplicar
- Opus A (ECO): cadena de pasajes en ECO sobre nucleo_eco_sel_ing (base ING: FABRICA_ECO + vivero permanente). Brazos: PAS_SEL
  (CEREBRO, transferencia de vivos), PAS_RES (control resorteo: G0 en cada pasaje), y si cabe PAS_SELM (CEREBRO + rep_umbral).
  T_p 50 000, 8 pasajes, 5 semillas. Carpeta experimentos/organelos/reunion/opus_a/. Semillas 47201–47240 (grep 18:50: libres).
- Opus B (pista): cadena de pasajes en la pista de la carrera sobre eco_ing_a_carrera (V143 base, 9 carros, fundador limpio).
  PRIMERO responde en el canal: ¿qué hereda un hijo en la pista y qué hereda el refundador? (pista.py:155 "nace() con la memoria del
  padre"; GENOMA es por módulo de carro; la nube hizo g por cuerpo en el carro EVO, rama origin/nube/termo-evo-20260928.) Sin tocar
  pista.py ni juez.py. Unidad heredable candidata: genoma (15 genes y/o g) POR LINAJE guardado en el módulo del carro, que el
  refundador hereda del último padre vivo del linaje, y que se transfiere al pasaje siguiente. T_p 20 000–50 000, 6–8 pasajes,
  3–5 semillas. Carpeta reunion/opus_b/. Semillas 47401–47440 (libres). Control: g/genes re-sorteados en cada pasaje.
- Fable (2 procesos): juguete de calibración en ECO, sólo para decidir largo/número/muestra: T_p 20k vs 50k, 3 semillas 47001–47009,
  carpeta reunion/fable/. NO es el experimento de Opus A; Opus A no espere a mi juguete. Reporto a las ~19:40.
- Ninguno de los dos corre nada con más procesos que los suyos (A 4, B 4). Todo EXPLORATORIO, sin preregistro, sin commits.
- Vocabulario: "evoluciona" sólo con la medida al lado (K, fundadores por linaje, gen). Errores de instrumento: decláranlos aquí.

### [18:50] Opus A (ECO) → todos
Arranco en reunion/opusA/. Diseño: núcleo por anclas desde eco_sel_ing/nucleo_eco_sel_ing.py (c2189f9d22b72386) + pasar `genoma` (90 fundadores).
Pasaje = ING_SEL_C (15 genes, hijo ingenuo, vivero permanente) de T_p = 100 000; al final, 90 genomas AL AZAR de los VIVOS (sin juez) → fundadores y
banco inicial del pasaje siguiente (+ la mutación de siempre). 10 pasajes (= 1e6 acumulado, el mismo presupuesto que la corrida larga).
Control CTRL: mismos pasajes y semillas, cada pasaje arranca del banco inicial (G0): sin herencia entre pasajes. Referencia F1 (MUT0) por pasaje.
Medida por pasaje: fund_2a (repuestos en [T_p/2, T_p]) / F1 pareado, K, K_nac, medias de genes. Referencia larga: −32 % en [5e5, 1e6] (fund_2a 86 833 vs 128 584).
Arnés: pasaje 1 sin transferencia == ING_SEL_C bit a bit; genoma=G0 explícito == None. ≤ 4 procesos, sin Pool.

### [18:42] Fable → Opus B
Tu plan es el mismo esquema: adelante, no cambies T (25k), N (10) ni la muestra. Tres precisiones, decláralas en tu README:
1. REFUNDACIÓN DENTRO del pasaje: el refundador de un linaje debe heredar del ÚLTIMO padre vivo de ese linaje (o de una muestra de los
   vivos del pasaje), NO de la inicial. Si sale de la inicial, repites el reseteo de termo_evo dentro de cada pasaje y los pasajes no
   arreglan nada. Si el carro no puede saberlo sin tocar pista.py, dilo y quedará como límite del instrumento.
2. Mide POR PASAJE: fundadores por linaje (media de los 9), R0 real (mediana de 9), linajes que cruzan, y g/alpha/tau_e de los padres.
3. Semillas base en 47401–47440 (libres al grep de 18:50); s·100+p está bien si lo escribes así. Carpeta opusB/ vale.
Tu muestreo "vivos cada 1000 pasos en los últimos 5000" pesa más a los que viven más: es selección natural leída, no juez. Vale, declarado.
Opus A: los genomas ECO (15 genes) para el brazo sembrado de B salen de vivos_final[i][4:] de tus JSON; avísale la ruta cuando existan.

### [18:58] Opus A (ECO) → Fable
Acepto tu esquema (T_p 50 000, 8 pasajes, 5 semillas; PAS_SEL, PAS_RES = G0 mutado una vez por fundador, PAS_AZA, PAS_SELM si cabe).
OJO semillas: 47201–47280 YA ESTÁN USADAS (tronco_v14_4_examen/umbrales_examen_v144.py:57, réplica VIVO). Uso 47801–47805 (grep py/md/txt/log
de organelos, bundle y carrera: libres); semilla de la corrida del pasaje p = 100·s + p (4780101…). Carpeta: reunion/opusA/ (la del encargo del coordinador).

### [18:43] Fable → Opus A
Aceptado tu diseño (T_p 100k × 10, PAS_SEL / CTRL / F1; banco inicial = la muestra transferida: bien, así el vivero del pasaje k+1 refunda
con genomas del pasaje k y no con G0). ERROR DE INSTRUMENTO MÍO, declarado: mi grep de semillas de las 18:50 miró sólo experimentos/organelos y
juaco_eco; 47201–47280 están usadas en tronco_v14_4_examen. Tus 47801–47805 valen. Mis 4700x del juguete: sólo aparecen en dos logs de
datos/ del 16 y 18-sep (no como semilla de ECO); las mantengo por ser juguete, declarado. Opus B: 4740x sigue libre en todo el repo.
Primer dato del juguete (T_p 50k, SEL s47001, 1 semilla, NO decide): K 104.1 → 103.0 → 100.6 y K_nac 25.7 → 19.2 → 17.2 en p0→p2;
alpha 2.50 → 2.81 → 2.85. OJO instrumento: a T_p corto la ventana [T_p/2, T_p] cae en el TRANSITORIO (fundadores iniciales aún vivos),
así que K por pasaje NO se compara con el K de la corrida larga; sólo SEL contra CTRL en el MISMO índice de pasaje. Números completos ~19:15.
(Nota de Fable: mis sellos de hora son los del reloj del PC, `Get-Date` — 18:43 al escribir esto; corregí dos sellos míos que iban adelantados.
Si los suyos van por otro reloj, no importa: el orden en el archivo es el que manda.)

### [18:48] Opus A (ECO) → todos
ERROR MÍO de reloj: mis dos entradas marcadas [18:50] y [18:58] se escribieron en realidad a las ~18:40 y ~18:44 (no miré `date`). Desde aquí, hora real.
Arnés 13/13 (opusA/identidad_pasajes_salida.txt): 1 pasaje sin transferencia == ECO_SEL_ING bit a bit; G0 explícito == None; el genoma entra
(90/90 fundadores); transferencia sólo lee el genoma. Humo (s47809, 2×20k): SEL p1 fund_2a 2143 → p2 1561; RES p2 2428 (una semilla, no se lee).
Preregistro exploratorio con predicciones: opusA/PREREGISTRO_pasajes.md. LANZADO 18:48, 4 procesos: PAS_SEL, PAS_RES, PAS_F1+PAS_AZA, PAS_SELM;
T_p 50 000, 20 pasajes (reporto p8 y sigo hasta 1e6 acumulado), semillas 47801–47805. ~10 s por pasaje.

### [19:05] coordinador → todos (dato de la NUBE, eco_sel_largo, PARCIAL: sólo serie, sin réplica, MC-2 corriendo)
- L (¿K sigue subiendo con T 1e7?): apunta a NO. K llega a su techo antes de 1e6 y 10× más tiempo no lo mueve (mediana del cambio −0.02).
- MC (margen + cerebro juntos vs cerebro solo): SEL_MC > SEL_C 20/20, +2.84 cuerpos en la ventana final.
- Lectura provisional: con genes fijos la selección se estanca rápido; MÁS genes que puede mover suben el techo. La frontera la pone lo que el
  organismo puede variar, no el tiempo. Implicación para ustedes: los pasajes cortos tienen sentido (no hace falta T largo), y conviene que
  la corrida que una todo deje variar TODOS los genes que se puedan (margen g + cerebro), no uno solo. Fable: inclúyelo en el ACTA.

### [18:50] Opus B → todos
Arnés opusB/identidad_pas_salida.txt: ARNES PASA 24/24 (1 pasaje sin transferencia y mutación 0 == corre_evo.tarea(V143_EVO_BAJO) bit a bit;
PASAJE 0 == EVO_BAJO salida ENTERA; regla 14 V143/TERMO/O1; siembra() sólo lee vivos_b; la siembra actúa; determinismo). ERROR MÍO de
instrumento, declarado: el arnés v1 FALLÓ (c) sólo por el nombre del carro en 'id' ('V143_PAS#i' vs 'V143_EVO_BAJO#i'); v2 normaliza el id
(salida v1 guardada). Humo T 5k escrito (datos/humo_*). LANZADAS 18:49 cadenas c1–c4 (4 procesos): brazos pas, ctl, pasg (sólo g), termo, o1;
T 25k × 10 pasajes; semillas de pista 58300+10c+p (583xx libre al grep; no uso 474xx). Respuesta a Fable (1): DENTRO del pasaje p≥1 el
refundador sale de la SIEMBRA del pasaje p−1 (vivos), no de la inicial; en el pasaje 0 y en ctl, de la inicial. No hereda del último padre
del pasaje en curso (eso sería el banco de termo_banco). Hijo: hereda g (+N(0,0.03)) y cerebro (mutación ECO) del padre por la cola.

### [18:53] Opus B → todos — ERROR DE INSTRUMENTO (declarado antes de leer pasajes)
R0 real = nac_reales/(muertes+1) y `cruza_real` pide ≥ 5 muertes: a T 25k un linaje sano con vida ~3000 (O1) tiene ~8 muertes → techo
del R0 real ≈ 0.89. Los pasajes cortos APLASTAN el R0 real y la "mayoría que cruza". Por pasaje leo sobre todo FUNDADORES POR LINAJE y
comparo R0 sólo contra TERMO/O1 en la misma semilla y T. La prueba contra 0.93/0.941 exige T 100k: cuando acaben c1–c4 (~19:35) corro
"prueba del muro" EXPLORATORIA: T 100k, fundadores sembrados con la siembra del p9 de cada cadena (fija), vs ctl, TERMO, O1 (semillas 5839x).

### [18:50] Fable → todos — juguete PARCIAL (calibración, NO decide): señal en el primer pasaje, sin acumulación después; un error de instrumento
T_p 20k × 10, 4 semillas completas (47004–47007), SEL (vivos → fundadores) vs RES (G0 en cada pasaje), mediana por índice de pasaje:
  p0: K 97.9 = 97.9 (idénticos: identidad del pasaje 0) · fund_2a 2516 = 2516
  p1: K 103.7 vs 98.2 (SEL>RES 4/4) · fund_2a 1692 vs 2567 (SEL<RES 4/4, −34 %) · alpha 1.57 vs 1.20 · tau_e 0.72 vs 0.85
  p5: K 102.6 vs 99.1 (4/4) · fund_2a 1715 vs 2408 (4/4) · alpha 1.73 · tau_e 0.58
  p9: K 101.3 vs 96.9 (4/4) · fund_2a 1793 vs 2523 (4/4) · alpha 1.93 · tau_e 0.57 · dist_G0 0.22 (RES 0.04)
Lectura: la transferencia de vivos baja un tercio los fundadores repuestos YA en p1 (el efecto de ECO_SEL_ING, en 20k en vez de 1e6) y se
sostiene 4/4 en los 9 pasajes; pero NO ACUMULA: fund_2a de SEL queda plano (1655–1852) y K_nac baja de 22 a 17 mientras los genes siguen
moviéndose (alpha 1.57 → 1.93, dist_G0 0.10 → 0.22). Coincide con la nube (K llega a su techo antes de 1e6).
ERROR DE INSTRUMENTO (declarado, afecta a Opus A también): la ventana [T_p/2, T_p] con fundadores G0 frescos cae en un TRANSITORIO que
depende de T_p: RES da K_nac 15 a T_p 20k, 22–25 a T_p 50k y 12.6 a 1e6. Por eso a T_p 50k (2 semillas) RES "gana" a SEL en K (0/2) aunque
SEL sigue con menos fundadores: el control con G0 fresco no es una base estable. Opus A: reporta la CURVA de SEL sola (p1…p8…p20) y la de
CTRL, y el pareado, pero no leas "CTRL > SEL en K" como falta de señal sin mirar fund_2a y K_nac. Un control mejor para la nube: RESORTEO
de los vivos transferidos con los genes barajados entre cuerpos (misma distribución marginal, sin genotipo heredado) — lo dejo para el ACTA.

### [18:52] Opus A (ECO) → todos (y Opus B: genomas)
Primera semilla completa (s47801, 20 pasajes de 50k = 1e6 acumulado; UNA semilla, no decide). REP = fundadores repuestos en TODO el pasaje,
r = REP/REP(F1 misma semilla y pasaje) − 1. PAS_SEL: p1 −17 % · p2 −34 % · p4 −33 % · p8 −30 % · p12 −29 % · p16 −28 %. PAS_RES (control):
p1 −17 · p2 −13 · p4 −22 · p8 −17 · p12 −14 · p16 −17. En la 2a mitad del pasaje (fund_2a) SEL ≈ RES (−29..−35 % los dos): un pasaje desde G0
ya llega al techo en ~25k pasos; la herencia entre pasajes ahorra el transitorio (−33 % contra −17 % en el pasaje entero) pero NO baja más.
Los genes siguen moviéndose (alpha 2.47→3.95, tau_e 0.67→0.28 en SEL; RES plano ~1.6–2.2) sin que baje más el número de fundadores.
Opus B, genomas del último pasaje (90 × 18, con nombres; s47801): reunion/opusA/datos/pas_PAS_SEL_s47801_T50000/genomas_ultimo_PAS_SEL_s47801.json
(los de s47802–05 saldrán en la misma forma: datos/pas_PAS_SEL_s<s>_T50000/genomas_ultimo_PAS_SEL_s<s>.json, ~19:05).

### [18:51] Fable → Opus A y Opus B — lectura cruzada: el mismo dato en tres instrumentos; qué hacer con lo que queda
Juguete COMPLETO (T_p 20k × 10, 5 semillas): SEL>RES en K 5/5 en p1–p5 (4/5 en p6, p8, p9); fund_2a SEL<RES 5/5 en los 9 pasajes
(1647–1847 vs ~2500, −30..−35 %); SEL plano de p1 a p9; alpha 1.67 → 2.18, tau_e 0.73 → 0.56 siguen moviéndose. T_p 50k × 8, 3 semillas:
K SEL<RES 0/3 (el auge de G0 en [25k, 50k]: K_nac RES 22–25), fund_2a mixto (1–3/3): a 50k un pasaje desde G0 ya alcanza el techo.
Opus A (s47801): SEL −33 % vs RES −17 % en el pasaje entero; fund_2a SEL ≈ RES. Nube: K techo antes de 1e6; MC > C.
LECTURA COMÚN (exploratoria): con hijos ingenuos y 15 genes, la selección natural llega a su techo (~−30 % fundadores) en 25–50k pasos.
Los pasajes seriados AHORRAN el transitorio (herencia entre pasajes) pero NO ACUMULAN: el techo lo pone lo que el organismo puede variar.
Lo que queda de tarde:
- Opus A: termina las 5 semillas y reporta p1/p8/p20 SEL vs RES vs F1 (REP entero y fund_2a) y sobre todo PAS_SELM (16 genes) contra
  PAS_SEL en fund_2a: si SELM baja más el techo, ese es el dato de la noche (lo que dice la nube MC). No abras brazos nuevos.
- Opus B: tu ERR del techo de R0 real a T 25k es correcto; por pasaje manda FUNDADORES POR LINAJE. Tu "prueba del muro" T 100k con la
  siembra del p9 (fija) contra ctl/TERMO/O1 es el experimento que cierra la tarde: adelante en cuanto liberes procesos; reporta R0 real,
  mayoría que cruza y fundadores por linaje, pareado por semilla. Si te sobra un proceso, brazo sembrado con genomas ECO de Opus A.
- Fable: control RESORTEO (genes barajados entre cuerpos) a 20k y 50k, para saber si lo que se transfiere es el GENOTIPO o sólo la
  distribución marginal (decide el control del preregistro de nube). ~19:05.

### [18:57] Fable → todos — control RESORTEO del juguete: lo que se transfiere que importa es la DISTRIBUCIÓN de los genes, no el genotipo
BAR = los mismos 90 genomas vivos transferidos, pero cada gen barajado entre cuerpos (misma marginal, ningún genotipo heredado entero).
T_p 20k × 10, 5 semillas, SEL vs BAR pareado: K SEL>BAR 2/5, 3/5, 5/5, 3/5, 4/5, 1/5, 3/5, 1/5, 2/5 (p1…p9); fund_2a SEL<BAR 2–4/5; medianas
iguales (K ~102 vs ~102; fund_2a ~1700 vs ~1700). T_p 50k × 8, 3 semillas: lo mismo (1–2/3). BAR contra RES (G0): igual de bueno que SEL.
Lectura (exploratoria): con 15 genes y este mundo, el efecto de la selección es un CORRIMIENTO de las marginales (alpha ↑, tau_e ↓, aversion)
que actúa gen a gen; no hay combinaciones (genotipos) que se pierdan al barajar. Consecuencia para el preregistro de nube: el control
RESORTEO NO discrimina (no lo pongan como puerta); el control que sí discrimina es G0/inicial en cada pasaje (con su transitorio declarado).
Y refuerza lo de la nube: para bajar más el techo hacen falta MÁS genes/piezas variables (SELM, g en la pista), no más pasajes.

### [19:00] Fable → todos — ACTA escrita (cierre forzado de la moderadora; el acta queda ABIERTA en su sección 6)
reunion/ACTA.md: veredicto "HAY SEÑAL en un pasaje, NO HAY SEÑAL de acumulación entre pasajes"; números de los tres instrumentos hasta
18:58; errores declarados; qué merece nube (prueba del muro de Opus B; SELM vs SEL con 20 semillas) con comandos. Opus A y Opus B:
AGREGUEN en la sección 6 sus números finales (A: 5 semillas p1/p8/p20 SEL/RES/SELM/AZA; B: p2–p9 de c1–c4 y la prueba del muro con su
comando exacto), con hora del PC. Nada de "evoluciona" sin la medida al lado. Mis dos procesos están libres desde las 18:56.

### [19:03] Opus B → todos — pista, pasajes p0–p2 (4 cadenas, T 25k; mediana de cadenas; EXPLORATORIO, no decide)
| p | pas R0 / estab / g siembra | ctl R0 / estab / g | pasg (sólo g) R0 / estab / g | TERMO R0 / estab | O1 R0 / estab |
| 0 | 0.34 / 6 / 0.030 (== ctl bit a bit) | 0.34 / 6 / 0.030 | 0.21 / 5.5 / 0.037 | 0.71 / 7 | 0.75 / 8 |
| 1 | 0.20 / 5 / 0.048 | 0.13 / 4.5 / 0.014 | 0.24 / 5 / 0.045 | 0.69 / 6 | 0.73 / 8 |
| 2 | 0.51 / 5.5 / 0.092 | 0.18 / 6 / 0.035 | 0.24 / 4.5 / 0.064 | 0.81 / 6.5 | (corre) |
estab = linajes con 0 fundadores tras 10k (de 9). Lo que SÍ se mueve: g de los vivos en pas sube por pasaje (0.03→0.05→0.09; ctl plano ~0.03):
la herencia entre pasajes acumula lo que termo_evo perdía. Fundadores: todavía no bajan. OJO: O1 a 25k cruza 0/9 (techo del R0 real).

### [19:08] Opus A (ECO) → todos — serie 47801–05, T_p 50k × 20 (SEL, RES, SELM 5/5 semillas; AZA 2–3/5; F1 3/5 para la razón)
r_rep = fundadores repuestos en el pasaje ENTERO / F1 − 1 (mediana). SEL: p1 −17 · p2 −37 · p4 −33 · p8 −31 · p12 −29 · p16 −31 · p20 −36.
RES (G0 mutado en cada pasaje): −17 · −17 · −22 · −17 · −14 · −17 · −20. SEL < RES en REP: 5/5 en TODOS los pasajes p2–p20.
2a mitad (fund_2a): SEL −30..−36 %, RES −26..−35 %: el techo dentro del pasaje es el MISMO; la herencia entre pasajes ahorra el transitorio.
SELM (+rep_umbral): −18 · −35 · −31 · −26 · −26 · −31 · −28 → no mejor que SEL (rep_umbral 0.99 → 0.89–0.95).
SORPRESA (2 semillas, no decide): PAS_AZA (SIN herencia dentro del pasaje) con transferencia de vivos: −3 · +3 · −4 · −12 · −20 · −31 · −28.
La corrida larga AZA daba −6 % a 1e6. La transferencia de los VIVOS (sobrevivientes) es por sí misma un canal de herencia a escala de pasaje.
Réplica lanzada (47811–15: F1, SEL, RES). AZA de réplica en cuanto se libere el proceso (~19:22). Genomas SEL de las 5 semillas ya en
opusA/datos/pas_PAS_SEL_s<s>_T50000/genomas_ultimo_PAS_SEL_s<s>.json (s = 47801…47805).

### [19:14] Opus B → todos — pista p0–p5 (4 cadenas, T 25k, mediana de cadenas; EXPLORATORIO)
| p | pas R0 (c1/c2/c3/c4) · fund med · g | ctl R0 · fund med · g | pasg (sólo g) R0 · g | TERMO R0 | O1 R0 |
| 0 | 0.34 · 2.0 · 0.030 | 0.34 · 2.0 · 0.030 | 0.21 · 0.037 | 0.71 | 0.75 |
| 3 | 0.48 (0.50/0.47/0.27/0.67) · 4.0 · 0.125 | 0.09 · 7.5 · 0.015 | 0.28 · 0.093 | 0.59 | 0.71 |
| 4 | 0.50 (0.50/0.50/0.75/0.29) · 4.0 · 0.147 | 0.08 · 3.5 · 0.003 | 0.54 · 0.105 | 0.74 | 0.78 |
| 5 | 0.70 (0.70/0.70/0.71/0.67) · 1.5 · 0.149 | 0.06 · 7.0 · 0.039 | 0.58 · 0.121 | (corre) | (corre) |
Lectura parcial: con transferencia el R0 real sube pasaje a pasaje (4/4 cadenas en p5 ≥ 0.67; ctl ≤ 0.14) y alcanza a TERMO/O1 a 25k;
g de los vivos 0.03→0.15 (ctl plano). Sólo-g (pasg) también sube: gran parte es g. Fundadores (MEDIA de 9) NO bajan (pas 19 vs ctl 16,
un linaje malo pesa); la mediana sí (1.5 vs 7). Ojo a Fable: aquí SÍ hay acumulación entre pasajes (g no tiene techo en 25k).
Opus A: gracias, genomas convertidos (15 genes + g U[-0.1,0.1]) en opusB/siembra_eco_s4780[1-4].json → brazo eco en la prueba del muro.

### [19:24] Opus A (ECO) → todos — SERIE COMPLETA 47801–05 (5 semillas × 20 pasajes de 50k, 5 brazos; EXPLORATORIO)
r_rep = fundadores repuestos en el pasaje ENTERO / F1 − 1 (mediana 5 semillas); tendencia = media r_rep(p16–20) − media(p1–5) por semilla.
| brazo | p1 | p2 | p8 | p20 | acumulado 1e6 | tendencia (bajan) | alpha p1→p20 | tau_e p1→p20 |
| SEL  | −17 | −35 | −31 | −33 | −32 % | 4/5 (−0.4..−4.7 pp; contra p2–5: 2/5) | 1.86→4.07 | 0.74→0.37 |
| RES  | −17 | −17 | −18 | −17 | −19 % | 3/5 (ruido ±4 pp) | 1.86→1.78 | 0.74→0.68 |
| SELM | −14 | −35 | −26 | −31 | −27 % | 3/5 (contra p2–5: 1/5) | 1.87→4.55 (rep_umbral 0.98→0.85) | 0.72→0.35 |
| AZA  |  −3 |  −9 | −19 | −23 | −13 % | 4/5 (−14..−26 pp) | 1.45→4.14 | 0.85→0.33 |
Corrida larga (ECO_SEL_ING, 1e6): SEL −31.6 % / −30.6 % (serie/réplica), AZA −5 %. SEL<RES en REP: 5/5 en p2–p20.
LECTURA: SEL con pasajes == SEL largo (−32 % contra −31.6 %): los pasajes NO bajan más ni más rápido; ahorran el transitorio. SELM no es mejor.
Lo NUEVO: en AZA (sin herencia dentro del pasaje) la transferencia de los VIVOS es selección por supervivencia (el vivo en T está sesgado
a los que viven más): los fundadores bajan pasaje a pasaje (4/5) y los genes van al MISMO sitio que en SEL (alpha 4.1, tau_e 0.33).
Réplica 47811–15 corriendo (SEL/RES/F1 ~19:30; AZA ~19:45).

### [19:27] Opus A (ECO) → Fable y coordinador — OJO al encargo de nube del ACTA §5
1. Semillas: 47811–47815 YA LAS USÉ (réplica de SEL/RES/F1/AZA de esta tarde). Y corre_pasajes.py tiene guarda de semillas base
   (47801–47808 serie, 47811–47815 réplica): con 47816–47830 ABORTA. Propongo nube: serie 47851–47870, réplica 47871–47890 (grep 19:26
   en py/md/txt/log de organelos, bundle, carrera: sólo aparecen en el ACTA). Amplío la guarda a 47851–47890 y re-corro el arnés (14/14 hoy).
2. §1 del ACTA: "NO hay acumulación entre pasajes" vale para SEL (y RES), NO para AZA: sin herencia dentro del pasaje, la transferencia de
   vivos SÍ acumula (serie 4/5 semillas bajan 14–26 pp de p1–5 a p16–20; genes al mismo sitio que SEL). Réplica de AZA corriendo; la
   extensión p21–p40 de AZA/SEL/F1 (¿llega AZA al techo de SEL?) corriendo. Lo agrego en §6 a las ~19:50.
Réplica SEL/RES/F1 (47811–15) ya salió y replica: SEL acumulado 1e6 −29.8 % (larga réplica −30.6 %), RES −18.1 %, SEL<RES 5/5 p2–p20;
SEL p2 −35 % es el mejor pasaje (serie y réplica); después −30 %: SEL no acumula (tendencia 1/5 contra p2–5).

### [19:36] Opus B → todos — pista COMPLETA c1–c4 × 10 pasajes (T 25k; EXPLORATORIO). HAY ALGO MODESTO en R0, NO en fundadores
| p | pas R0 · g siembra | ctl R0 · g | pasg (sólo g) R0 · g | TERMO R0 | O1 R0 |
| 0 | 0.34 · 0.030 | 0.34 · 0.030 | 0.21 · 0.037 | 0.71 | 0.75 |
| 3 | 0.48 · 0.125 | 0.09 · 0.015 | 0.28 · 0.093 | 0.59 | 0.71 |
| 5 | 0.70 · 0.149 | 0.06 · 0.039 | 0.58 · 0.121 | 0.53 | 0.67 |
| 7 | 0.61 · 0.219 | 0.04 · 0.027 | 0.73 · 0.193 | 0.57 | 0.58 |
| 9 | 0.61 · 0.245 | 0.21 · 0.037 | 0.67 · 0.195 | 0.75 | 0.74 |
Pareado (cadena, p≥3; 28 pares): pas>ctl 28/28 (+0.58) · pasg>ctl 26/28 (+0.57) · pas>pasg 14/28 (+0.02: el CEREBRO NO SUMA; lo carga g) ·
pas>TERMO 10/28 (−0.06) · pas>O1 7/28 (−0.11). g de los vivos SUBE sin techo en 10 pasajes (0.03→0.24, c4 0.34; TERMO usa 0.40): acumula.
PERO fundadores por linaje (media de 9, p5–p9): pas 19.2, pasg 18.0, ctl 12.9, TERMO 32.1, O1 14.2 → con g alto SUBEN (mediana baja: 2 vs 5;
establecidos 6.5 vs 5.0/9). Lectura: los linajes establecidos comen mejor y dejan el mundo más pobre para los refundadores ingenuos de los otros
(trampa "el mundo se come la comida"; TERMO igual). Mis predicciones Q4 y Q7 REFUTADAS (fundadores no bajan, suben). Prueba del muro T 100k
LANZADA 19:32 (4 procesos, 12 semillas 58391–58398, 58401–58404; pas/ctl/v143/o1/termo/pasg/eco; fin ~20:45).

### [19:49] Opus A (ECO) → todos — FINAL (CPU libre; 0 procesos míos)
VEREDICTO: NO para SEL (los pasajes no bajan los fundadores más allá de la corrida larga, ni más rápido) · HAY ALGO MODESTO para AZA
(sin herencia dentro del pasaje, la transferencia de vivos baja los fundadores de −3 % a ~−13/−20 %, sin llegar a SEL, con mucha deriva).
SEL serie, bloques de 5 pasajes (r_rep mediana): −32 · −33 · −33 · −34 · −33 · −33 · −34 · −34 % (p1–p40 = 2e6); acumulado 1e6 −32 % (réplica −29.8 %)
== larga −31.6/−30.6 %; 2e6 −32.6 %. AZA serie: −3 · −12 · −17 · −22 · −13 · −2 · −13 · −16 %; acumulado 2e6 −11 % (larga −5 %).
AZA réplica (20 pasajes): p16–20 < p1–5 en 5/5, acumulado 1e6 −8.5 %. Mis predicciones Q4, Q6, Q7, Q10 REFUTADAS; Q8 mixta (serie sí, réplica no).
Arnés final 14/14 (sha corre_pasajes 858c2ae30293203b; guarda de semillas ampliada a 47851–47890 para la nube). Agrego en ACTA §6.

### [19:54] Opus B → todos — PRUEBA DEL MURO T 100k, primeras 4 semillas (58391–94; pas/ctl/v143/o1; EXPLORATORIO, n 4, no decide)
| brazo | R0 real (mediana) | mayorías que cruzan | linajes que cruzan | fund/linaje media · mediana | establecidos /9 |
| pas (siembra p9) | 0.819 | 1/4 | 16/36 | 80.7 · 4.5 | 6.5 |
| ctl | 0.385 | 0/4 | 13/36 | 61.7 · 26 | 4.0 |
| v143 | 0.604 | 0/4 | 9/36 | 190.6 · 18 | 6.0 |
| o1 | 0.956 | 4/4 | 32/36 | 4.0 · 0 | 8.5 |
Pareados: pas>ctl 4/4 (+0.39) · pas>v143 3/4 (+0.26) · pas>o1 1/4 (−0.14). Por semilla pas: 0.54 / 0.82 / 0.96 (7/9 cruzan) / 0.81.
Lectura provisional: la siembra evolucionada sube el R0 real a nivel TERMO (0.93 serie) sin llegar a O1; NO cruza el muro (1/4 mayorías).
El cuello sigue siendo el mismo: 1–2 linajes por semilla que se refundan cientos de veces (fund [0,0,746,1,1,186,0,0,0]). TERMO/pasg/eco en curso.

### [20:03] Opus B → todos — PRUEBA DEL MURO T 100k, 4 semillas × 7 brazos completas (EXPLORATORIO, n 4)
| brazo | R0 real | mayorías | linajes que cruzan | fund/linaje media · mediana | estab /9 |
| pas (siembra p9: g + cerebro) | 0.819 | 1/4 | 16/36 | 80.7 · 4.5 | 6.5 |
| pasg (siembra p9: sólo g) | 0.739 | 0/4 | 10/36 | 75.8 · 9.5 | 4.5 |
| eco (cerebro ECO de Opus A, g inicial) | 0.403 | 0/4 | 5/36 | 53.9 · 28.5 | 3.0 |
| ctl | 0.385 | 0/4 | 13/36 | 61.7 · 26 | 4.0 |
| v143 | 0.604 | 0/4 | 9/36 | 190.6 · 18 | 6.0 |
| TERMO | 0.831 | 2/4 | 18/36 | 112.8 · 5 | 6.5 |
| O1 | 0.956 | 4/4 | 32/36 | 4.0 · 0 | 8.5 |
Pareados: pas>ctl 4/4 (+0.39) · pas>TERMO 3/4 (+0.06) · pas>pasg 3/4 (+0.08) · eco>ctl 2/4 (−0.02) · pas>O1 1/4.
Lectura: 10 pasajes cortos llevan al bicho desde la zona letal (g ~0) al nivel de TERMO (g 0.24 frente a 0.40 diseñado) sin constante de
diseño; el cerebro ECO solo NO transfiere a la pista (== ctl, como eco_a_carrera). El muro NO se cruza: fundadores por linaje no bajan.
Semillas 58395–58398 y 58401–58404 corriendo (fin ~21:08).

### [20:32] Opus B → todos — PRUEBA DEL MURO T 100k, 8 semillas (58391–58398) × 7 brazos (EXPLORATORIO)
| brazo | R0 real | mayorías | linajes que cruzan | fund/linaje media · mediana | estab /9 |
| pas (g + cerebro) | 0.805 | 1/8 | 31/72 | 87.2 · 6.0 | 5.5 |
| pasg (sólo g) | 0.802 | 3/8 | 29/72 | 75.8 · 7.0 | 6.0 |
| TERMO | 0.766 | 3/8 | 35/72 | 115.2 · 8.5 | 6.0 |
| v143 | 0.574 | 0/8 | 20/72 | 185.0 · 19 | 6.0 |
| ctl | 0.387 | 0/8 | 20/72 | 58.3 · 30.5 | 4.0 |
| eco | 0.314 | 0/8 | 15/72 | 54.1 · 35.5 | 3.0 |
| O1 | 0.938 | 8/8 | 57/72 | 22.2 · 0 | 8.0 |
pas>ctl 7/8 (+0.37) · pas>v143 7/8 (+0.17) · pas vs TERMO 5/8 (+0.01) · pasg>ctl 8/8 (+0.42) · pas vs pasg 3/8 · eco vs ctl 3/8 (−0.13).
Se sostiene: la selección entre pasajes lleva g al nivel de TERMO (R0 ≈ TERMO) sin diseñador; el cerebro no suma; el muro no cae
(mayorías 1–3/8 contra O1 8/8). Última tanda 58401–58404 termina ~21:00; luego ACTA §6.

### [20:56] Opus B → todos — FINAL (CPU libre; 0 procesos míos). HAY ALGO MODESTO (exploratorio), el muro NO cae
Prueba del muro T 100k, 12 semillas: pasg (sólo g evolucionada en 10 pasajes) R0 0.853, mayorías 5/12 · pas (g + cerebro) 0.805, 2/12 ·
TERMO 0.926, 7/12 · O1 0.950, 12/12 · v143 0.619 · ctl 0.387 · eco 0.311. pasg>v143 12/12 (+0.26), pasg vs TERMO 6/12 (0.00), eco vs ctl 4/12.
La selección entre pasajes construye el termostato y alcanza a TERMO sin diseño; el cerebro no suma; fundadores por linaje no bajan.
Sin señal clara → sin esqueleto del intento #7. Todo en ACTA §6 (20:55) y opusB/lee_muro_salida.txt, lee_cadenas_salida.txt.
