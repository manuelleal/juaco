# PREREGISTRO: O1 LIBRE CON PODERES (o1_libre, 30-sep-2026, EXPLORATORIO con letra fija; escrito ANTES del humo; cambios de auditoría y de la junta o1_evo ANTES de datos en §11 ter)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).
Encargo del director (30-sep): "corramos nuestro monstruo que pasa el muro, démosle poderes, soltémoslo a ver qué hace; ya evoluciona; no es
tiempo, son condiciones para evolucionar". Rama `o1-libre` (worktree `JUACO/o1libre`, desde `origin/organelos` 166d4be6).
**Numeración de ERR:** ERR-158 y ERR-159 están reservados por la sesión o1_evo; esta rama usa desde ERR-160. Este bloque no abre ninguno
al escribirse.

## 0. Qué es y qué NO es
- **Es EXPLORATORIO** (primer mundo nuevo, primeros poderes); tiene letra fija por código y semillas nuevas. Su lectura propone, o no, un
  confirmatorio. No decide tronco ni nivel.
- No es un intento contra el muro con la letra del muro (O1 ya cruza). Pregunta si **la evolución, soltada con condiciones que pagan,
  sube el uso de capacidades nuevas** (novedad) y si el linaje evolucionado **conquista** a O1 de fábrica en el mismo mundo.
- La lección vigente es "la selección afina perillas continuas pero no inventa combinaciones". Aquí cada poder es **una perilla continua
  que nace en 0**: la selección no tiene que armar una combinación, sólo subir una pendiente. Si ni así se prenden, el resultado no
  contradice la lección. Si se prenden, la selección sube un poder que nadie dejó encendido (los poderes están cableados; lo que se hereda
  es su intensidad).

## 1. Hipótesis
H: con O1 entero como genoma (sus 10 constantes + 4 poderes en 0), en un mundo con parche rico móvil, temporadas suaves y ahorro al quedarse
quieto, y selección por HIJOS en pasajes de 100k, **al menos un poder sube más que por deriva** y **el linaje evolucionado le gana en hijos a
O1 de fábrica en el mismo mundo**, más de lo que le gana un linaje con la misma deriva y sin selección.

## 2. Organismo (`construye_o1_lib.py` → `carros/O1_LIB.py`, por anclas desde `carrera_escuderias/carros/O1.py` sha `99436afa2715f028`)
- **21 anclas**, cada una exactamente una vez; chequeo `ast`: las 5 constantes de módulo de O1 ya no se leen como globales en ningún método
  (salvo la línea de `__init__` que las copia) y `_gana` ya no tiene literales (sólo 0 y 1 de la estructura).
- **Genoma = 14 floats por cuerpo** (toda la memoria heredable nueva):

| gen | fábrica | clip | qué decide |
|---|---|---|---|
| MARGEN | 0.25 | [−0.5, 0.5] | come lo bueno si la necesidad que sube está bajo 1.0 + margen; dispara la limpieza |
| PRUEBA | 0.5 | [0, 1.5] | prueba una letra desconocida sólo si E y Ag > PRUEBA |
| PEN_OTRO | 0.35 | [0, 1.5] | castigo al blanco si otro cuerpo está más cerca |
| D0 | 3.0 | [0.5, 10] | suavizado de la distancia en el puntaje |
| PISO | 0.2 | [0, 1] | la limpieza no baja la necesidad golpeada de aquí |
| U4, U2, U1 | 4, 2, 1 | [0, 10] | pesos de urgencia (antes literales de `_gana`) |
| XURG | 0.3 | [0, 1] | nivel bajo el cual la urgencia es U4 |
| TOPE | 0.5 | [0, 1.5] | tope de la ganancia: min(dS, 1.0 + TOPE − x) |
| **MEM** | **0** | [0, 1] | memoria de LUGAR: sin nada que hacer (O1 iría al hueco) va a la celda de su última mordida BUENA si fue hace ≤ MEM·5000 pasos |
| **SOC** | **0** | [0, 1] | copia SOCIAL: la primera vez que una letra desconocida para el linaje aparece en la pizarra publicada por un vecino que PARIÓ, la copia con prob SOC |
| **RES** | **0** | [0, 1] | sentido de RESERVA: margen efectivo = MARGEN + RES·esc, esc = media móvil (500 pasos) de la fracción de objetos que no son buenos según su tabla |
| **PAU** | **0** | [0, 1] | PAUSA: sin nada que hacer, se queda quieto con prob PAU por paso en vez de ir al hueco |

- **Herencia:** hijo = padre + N(0, σ_j) (arnés d6–d7); σ_j = 0.03·max(1, |fábrica_j|)
  (0.03 como `pasg` y o1_evo; 0.09 D0, 0.12 U4, 0.06 U2). rng propias `[PS_SEMILLA, índice, instancia, 7721]` (mutación, siembra) y `7722`
  (copia, pausa): no tocan el rng del mundo, del cuerpo ni del hijo.
- **Fundador y refundador (cambio antes de datos, junta o1_evo, §11 ter):** el primero de cada linaje sale de la SIEMBRA (o de FÁBRICA en
  el pasaje 0). Un linaje que se extingue DENTRO de un pasaje o de una prueba se refunda por **COLONIZACIÓN**: toma los genes del padre de
  uno de los últimos 50 partos de OTRO linaje de la misma corrida (+ N(0, σ_j)); sólo si todavía no hubo partos de otro linaje, de la
  siembra. El hueco lo llena la descendencia de los que paren, no la siembra vieja. La colonia vive en el módulo del carro: es un canal
  entre linajes de la misma corrida, declarado como regla de mundo; sólo lleva genes al refundar (ninguna decisión la lee; arnés b6, d8, d9).
  En `mix`/`mixn`/`mixA` los O1_LIB colonizan desde partos O1_LIB; O1 de fábrica se refunda como siempre.
- **Publicar** (al parir, la tabla por letra: 8 números, 9.0 = no probada) es una perilla de ESPECIE (`PS_ESCRIBE` = 1 en todos los
  brazos con O1_LIB), no un gen: publicar no le da nada al que publica (altruismo que la selección no ve). O1 de fábrica no publica ni lee.
- **`PS_LEE` 0** (cadena neutra): los genes se heredan, mutan, se anotan y se transfieren igual; ningún cuerpo los lee (O1 de fábrica,
  poderes 0). Con `PS_LEE` 0 el carro es O1 bit a bit con cualquier σ (arnés d1, d4).
- La memoria de lugar y la media de escasez son del LINAJE (como la tabla de O1); el refundador (instancia nueva) nace sin ellas.
- **Vocabulario (auditoría H-7):** los contadores de cada poder se llaman **activaciones** (veces que el poder cambió o pudo cambiar una
  decisión), no "uso".

## 3. Mundo (`pista_libre.py`, por anclas desde `carrera_escuderias/pista.py` sha `9f47c65e438e0ff4`; `juez.py` `6a68f640a7832f12`; 8 anclas)
Con las tres perillas en 0 es `pista.run` bit a bit (arnés a1–a3, incluido FABRICA compat=1 y el estado final del rng del mundo). En el bloque
van las tres en 1. 9 linajes, L 360, 36 objetos, pizarra 1, fundador limpio (ENMIENDA 5), T 100 000: la pista de la carrera.

| condición | regla | por qué (qué poder puede pagar) |
|---|---|---|
| **estación** | s(t) = −sin(2πt/20 000): empieza en abundancia. Lo que nace sortea su letra como siempre y después, con rng propia, una A/C pasa a B/D con prob 0.5·s si s > 0, o una B/D a A/C con prob 0.5·|s| si s < 0. Fracción buena de lo que nace: 0.25–0.75, suave; media = mundo viejo. Las letras NO cambian de significado | RESERVA (llenarse cuando escasea) y ESPERA. Suave y sin inversiones: "el mundo que cambia de golpe mata a todos" (29-sep). Empieza en abundancia: los fundadores se establecen antes de la primera escasez (t 10k) |
| **parche** | arco de 36 celdas (10 %) que avanza 1 celda cada 250 pasos (≈ 1.1 vueltas por 100k; inicio sorteado por semilla). Cada A/C que nace se muda con prob 0.5 a una celda LIBRE del parche. No se anuncia | MEMORIA DE LUGAR: la comida nueva cae donde está el parche; quien espera ahí la toma primero. Se mueve lento: lo recordado vale un rato |
| **quieto** | quien no se movió en la fase A paga 0.7 del costo metabólico | PAUSA / ESPERA |

- **Copia social:** no necesita perilla de mundo; paga en la pista vieja (un refundador con tabla vacía no sabe qué comer y prueba B/D).
- **"Evitar no es gratis":** ya en la pista (lo que nadie muerde TAPA el mundo; por eso O1 limpia) y aquí más: en la escasez nace más B/D.
- rng propia del mundo `[seed, 0, 21, 0]` (pista 11–15; pista_pob 16–17; pista_grande 18): no perturba ninguna corriente de la pista.

## 4. Brazos, semillas, T
Por índice i (10 índices):
| brazo | qué es |
|---|---|
| cadena `lib` | 3 pasajes de T 100 000 de O1_LIB (`PS_LEE` 1). **Siembra del pasaje siguiente = 90 PARTOS al azar de los partos con t ≥ 50 000** (cada parto = los genes del padre): la moneda son los PARTOS (descendientes) a 100k (junta 29-sep). No ve R0, cruce ni nada del juez. Pasaje 0: fábrica + mutación |
| cadena `neu` | LA MISMA cadena (mismas semillas, herencia, mutación, anotación y transferencia) con `PS_LEE` 0: deriva sin selección sobre los genes |
| prueba `lib` / `neu` | 9 × O1_LIB con la siembra final de SU cadena (`PS_LEE` 1) |
| prueba `o1` | 9 × O1 de fábrica (la BASE) |
| prueba `mix` | **CONQUISTA**: O1_LIB (siembra lib) en las casillas pares si i es par (5) o impares si i es impar (4), O1 de fábrica en las demás, en el MISMO mundo (45 casillas de cada lado en 10 índices) |
| prueba `mixn` | CONTROL de la conquista: lo mismo con la siembra neu |
| prueba `mixA` | **SÓLO DESCRIPTIVO (auditoría H-5), NO entra en la letra ni en V1:** lo mismo que `mix` con la siembra lib y los 4 poderes puestos en 0 (vuelven a mutar desde 0 durante la prueba, como en el pasaje 0). Separa "conquista por los poderes" de "conquista por las perillas de O1" |

- Las 6 pruebas de i usan la MISMA semilla (números aleatorios comunes). Monocultivos: `corre_v143.tarea` importada sin tocar, con `pista.run` →
  `pista_libre.run` sólo durante la llamada. Mixtas: `tarea_lista`, copia de `corre_v143.tarea` para una lista (arnés g1: campo a campo, regla 14).
- **Ventana de la siembra (auditoría H-8):** t ≥ 50 000 en un pasaje de 100k con periodo 20k y s(t) = −sin(2πt/20k) cubre **3 medios
  ciclos de escasez** (50–60k, 70–80k, 90–100k) y **2 de abundancia** (60–70k, 80–90k): la moneda pesa un poco más la escasez. Declarado.
- **Revisado contra la junta o1_evo (30-sep):** (a) la siembra NO reparte cuotas: sortea 90 partos del conjunto de TODOS los partos tardíos,
  así que cada linaje aporta en proporción a sus partos (`corre_o1_libre.siembra`; arnés h1–h2); se reportan aportes por linaje, Ne por
  linaje y padres distintos. (b) la refundación dentro del pasaje o de la prueba salía de la siembra vieja: corregido a colonización (§2, §11 ter).
- **Vocabulario (auditoría H-4):** **partos (descendientes)** = hijos que el cuerpo pone en la cola (la moneda de la siembra); **nacimientos
  reales (recambio)** = hijos que llegan a nacer (la medida de la conquista). Son cosas distintas y se reportan por separado.
- **Semillas NUEVAS 734xxx** (grep 30-sep en .py/.md del worktree: no aparecen). Serie: pasaje p de i → 734000 + 10i + p; prueba → 734201 + i.
  Réplica: 734300 + 10i + p; prueba 734501 + i. Práctica 734900–734999 (arnés 734950–734989; humo 734990–734998).
- **Recortes declarados (mejor pequeño y honesto):** (1) sin `pista_pob` (K copias multiplican el costo por K y dio NO el 29-sep): la competencia
  es entre los 9 linajes de un mundo, y la conquista se mide en `mix`; (2) la copia social copia la TABLA, no los genes; (3) sin `o1ctl`: el
  pasaje 0 de cada cadena es el pasaje sin transferencia; (4) sin anclas `v143`/`termo`: en un mundo nuevo no hay banda conocida; la validez
  del mundo es que O1 de fábrica viva (V2, umbral fijado a priori); (5) la visión sigue siendo TOTAL (la pista entrega todos los objetos): la
  memoria de lugar sólo puede pagar cuando no hay nada útil a la vista. Si MEM no se prende, no dice que la memoria no sirva con visión local.

## 5. Medidas
- **Conquista** (por índice, en `mix` y `mixn`): media de **nacimientos reales (recambio)** por linaje O1_LIB − media por linaje O1 (física
  del juez, ERR-100). **PC no se lee como supervivencia:** mide recambio, no quién vive más. Descriptivos por lado (auditoría H-4): partos
  (descendientes), muertes y fundadores de cada lado, y sus diferencias.
- **Poderes:** media de cada gen en la siembra final de cada cadena (`lib` contra `neu`, pareado por índice).
- Descriptivos: trayectoria por pasaje (mediana de cadenas) de los 14 genes en lib y neu; **orden de encendido** (primer pasaje desde el que
  mediana(lib) − mediana(neu) ≥ 0.05 hasta el final); genes de O1 finales; activaciones de cada poder en las pruebas; linajes que cruzan
  (`cruza_real`) por brazo y en `mix` por lado; nacimientos reales; R0 real; A+C del mundo; fracción del tiempo en el parche; **partos por
  pasaje lib contra neu** (auditoría H-3); aportes por linaje, Ne y padres distintos de cada siembra; fundadores de siembra y de colonia;
  `mixA` (conquista, cuántas veces `mix` > `mixA`).

## 6. LA LETRA (`corre_o1_libre.lee_serie`; el arnés la prueba en 13 casos sintéticos, (i))
**Validez (si una falla: NO SE LEE):**
- V1: completa (20 cadenas de 3 pasajes, 50 pruebas de la letra), 0 abortos en ellas, contabilidad coherente y `t_fund` reconstruible
  (`mixA` no entra: un aborto de `mixA` se reporta y no invalida).
- V2: O1 de fábrica vive en el mundo nuevo: mediana (por índice) del R0 real mediano de `o1` ≥ 0.50. Fijado a priori, sin corridas de este
  mundo a la vista (el humo es posterior a este texto).
- V3: el mundo actúa en cada pasaje y en cada prueba (conversiones en los dos sentidos, mudanzas al parche, pasos quietos > 0).
- V4: en `lib`, `neu`, `mix`, `mixn` ningún fundador O1_LIB sale de FÁBRICA y los primeros salen de la siembra (con la colonización, los
  refundadores salen de la colonia); en `o1` no hay fundadores O1_LIB.
- V5: estado escrito por cada corrida: carro correcto; σ 0.03, `PS_LEE` 1, `PS_ESCRIBE` 1 y `PS_COLONIZA` 1 en las pruebas O1_LIB (y colonización en cada pasaje); `PS_LEE` 1 en cada pasaje
  `lib` y 0 en cada pasaje `neu`; el mundo de cada corrida = estación, parche y quieto en 1.
- **V6 (control que puede fallar): el neutro es neutro**: en todos los pasajes `neu`, las activaciones de MEM, PAU, SOC y RES son 0.
**Puertas (n = 10; empates EN CONTRA):**
- **PC (conquista):** conquista de `mix` > 0 en **≥ 8/10** índices. (Bajo azar 50/50, P(≥ 8) = 0.055.)
- **PN (no es sólo deriva: purga de carga):** conquista de `mix` > conquista de `mixn` en **≥ 8/10**. El neutro lleva genes de O1 que
  derivaron sin purga; PN separa "hubo selección" de "sólo deriva", no "poderes" de "perillas" (eso lo mira PP, y descriptivamente `mixA`).
- **PP (un poder se prende):** para al menos un poder: siembra final `lib` > `neu` en **≥ 8/10** cadenas **y** mediana(lib) − mediana(neu) ≥ **0.05**.
  **PP: nulo ≈0.18 por multiplicidad (4 poderes); PP solo nunca pasa de MODESTO ni se cita sin réplica.**
**Veredictos:**
- **FUNCIONA:** validez y PC y PN y PP.
- **HAY ALGO MODESTO:** no FUNCIONA y (PC o PP). Matices: "conquista, pero la deriva sola hace lo mismo" (PC sin PN); "conquista por selección
  sin poderes (afina las perillas de O1)" (PC y PN sin PP); "un poder se prende sin conquista" (PP sin PC).
- **NO:** lo demás.
- **EN EL UMBRAL:** PC en 7–9; **PN en 7–9 sólo si PC ≥ 7** (ERR-160, §11 ter); o un poder con 7–9 cadenas a favor (y diferencia ≥ 0.04),
  o diferencia en [0.04, 0.06] (y ≥ 7 cadenas).
- **Bloque** (serie + réplica): si coinciden vale ése; si no, el menor; NO SE LEE manda.

## 7. Regla de parada y vocabulario
- **Réplica** (semillas 734300–734510) sólo si la serie da FUNCIONA, MODESTO, o NO EN EL UMBRAL. El runner lo exige (candado) y exige el
  mismo sha de runner (arnés k3, k4). **Si la serie da NO fuera del umbral, el bloque se cierra en NO sin réplica.**
- `--reanuda` sólo reintenta trabajos ABORTADOS por el instrumento o la máquina (JSON con `aborto`); un JSON válido nunca se re-corre.
- NO SE LEE no tiene salida por esta letra: no se relee ni se re-corre con las mismas semillas; la causa se registra (ERR-160 en adelante si es
  del instrumento).
- FUNCIONA ×2 → permitido: "soltado en un mundo que paga, O1 prende el poder X por selección (más que por deriva) y su linaje conquista a O1
  de fábrica en el mismo mundo". Prohibido: "O1 inventa un órgano", "la evolución supera al diseñador" sin decir "poderes cableados, apagados,
  con intensidad heredable", "cruza el muro", "aprende". **Prohibido "conquista gracias a X" (un poder) si `mixA` no lo separa** (si `mixA`
  conquista igual que `mix`, la conquista es de las perillas de O1, no del poder). **Prohibido "conquista gracias a X" y "conquista gracias
  a la colonización" cuando `mix` no supera a `mixA`** (la colonización está en los dos: no puede explicar la diferencia).
- Un poder que se prende en lib pero no conquista: "la selección sube el poder X; no alcanza para ganarle a O1".
- NO → "en 3 pasajes de 100k con selección por hijos, ningún poder se separa de la deriva y el linaje no conquista a O1": **no contradice** "la
  selección afina, no inventa combinaciones", en este mundo y con estas dosis (no la "refuerza": un NO de un exploratorio no prueba la lección).
- **Regla de lectura de la carga (R-5b, antes de datos):** si la mediana (de cadenas) del R0 real mediano de `lib` en el ÚLTIMO pasaje (p3)
  cae **≥ 0.15** bajo la del PRIMERO (p1), y la serie da NO, el matiz es **"carga domina; NO no informa sobre poderes"**. El veredicto no
  cambia. (En el runner: `aviso_carga`; se reporta siempre.)
- **Neutro o lib extintos (ERR-160 v):** una cadena sin un solo parto en un pasaje entero se EXTINGUE: es un dato, no un aborto. Se lee así:
  `mixn` de ese índice es pérdida del neutro, `mix` pérdida de lib (conquista −∞), el monocultivo cruza 0, y en PP ese índice no cuenta a
  favor de lib. Esto toca la letra (§6: PC, PN y PP se calculan así con extinciones).

## 8. Predicciones firmadas (creador, ANTES del humo)
Base: O1 cruza ~75 % de los linajes en la pista vieja; los hijos por linaje son del orden de cientos en 100k, así que 3 pasajes son del orden
de 10³ generaciones a lo largo de una línea: con σ 0.03 la deriva sola mueve un gen del orden de 0.5–1 (el neutro no se queda en 0).

| # | predicción | rango | p |
|---|---|---|---|
| Q1 | V2 pasa (O1 de fábrica vive en el mundo nuevo, R0 real mediano ≥ 0.50) | | 0.80 |
| Q2 | `o1`: suma de linajes que cruzan (de 90) | [30, 75] | 0.60 |
| Q3 | en `neu`, la mediana de la siembra final de cada uno de los 4 poderes cae en [0.25, 0.65] (la deriva los sube sola) | | 0.60 |
| Q4 | PP (al menos un poder se prende contra la deriva) | | 0.40 |
| Q5 | el poder MÁS separado (mayor dif. de medianas, si alguno pasa PP): PAU 0.20 · MEM 0.15 · RES 0.15 · SOC 0.10 · ninguno 0.40 | | — |
| Q6 | PC (lib conquista a O1 en ≥ 8/10) | | 0.25 |
| Q7 | `mixn`: conquista < 0 (el neutro pierde contra O1) en ≥ 7/10 | | 0.65 |
| Q8 | PN (lib > neu en conquista en ≥ 8/10) | | 0.35 |
| Q9 | `lib` en monocultivo: suma de linajes que cruzan ≥ la de `o1` | | 0.35 |
| Q10 | MARGEN de la siembra final `lib` (mediana) dentro de ±0.10 de 0.25 | | 0.50 |
| V | veredicto de la SERIE: FUNCIONA / MODESTO / NO / NO SE LEE | | 0.08 / 0.37 / 0.40 / 0.15 |
| Q11 | (R-5b; escrita TRAS los humos v2/v3, antes de la serie) NO SE LEE, o la cadena `neu` extinta en ≥ 1 índice | | 0.25 |

Lo más probable (NO, 0.40): la carga de mutación en 14 genes y la deriva dominan en 3 pasajes; los poderes suben igual en lib y en neu.

## 9. Las cuatro trampas
- **Canal simétrico:** la pizarra es pública y la lee cualquiera con el poder; en `mix` O1 de fábrica no publica ni lee (no tiene el poder):
  la asimetría ES el poder, y se declara. La información de decisión entre linajes pasa sólo por la pizarra de la pista.
- **Canal de GENES por colonización (declarado, R-2):** la colonia (`_COL`, en el módulo del carro) lleva genes de un parto de otro linaje al
  refundador de la misma corrida. No lleva información de decisión. **Asimetría en las mixtas:** un O1_LIB extinto se refunda desde O1_LIB
  reciente (colonia), un O1 de fábrica desde fábrica (la pista). `mixA` tiene la misma colonización y la misma asimetría: la diferencia
  `mix` − `mixA` no la puede explicar la colonización.
- **Acierto sin balancear:** las medidas son físicas del juez (nacimientos reales, `cruza_real`), no un acierto del carro.
- **Mundo que se come la comida:** en `mix` comer más ES competir; se reportan A+C del mundo y fracción en el parche por brazo. Si lib gana
  pelando el mundo, se dice.
- **Sitios fijos:** el parche arranca en un lugar sorteado por semilla (rng propia) y se mueve; semilla nueva por pasaje y por prueba.

## 10. Riesgos
- Carga de mutación con 14 genes: lib puede quedar bajo O1 aunque la selección funcione (por eso PN contra el neutro, no sólo PC).
- Deriva fuerte: con ~10³ generaciones el neutro dispersa los poderes; PP exige separarse de eso, no de 0.
- V2: si el mundo nuevo es muy duro para O1 (la primera escasez en t 10k–20k refunda linajes), NO SE LEE. Sin calibración previa, a propósito.
- La visión total resta valor a la memoria de lugar (sec. 4, recorte 5).
- Costo: si la PC está cargada (otra serie con pool 4), el reloj se alarga.

## 11. Instrumento, arnés, humo, costo
- `corre_o1_libre.py` (`--humo`, `--serie`, `--replica`, `--reanuda`, `--lee`, `--bloque`, `--pool N ≤ 2`); JSON por trabajo y por pasaje
  (ERR-54); `--reanuda` salta lo hecho y reintenta abortos; candados: se niega si ya hay veredicto; réplica sólo por la regla de parada y con
  el mismo sha de runner; `git_limpio` del preregistro, runner, constructor, carro y mundo; `identidad_corta` en cada corrida real.
- Arnés `identidad_o1_libre.py` → `identidad_o1_libre_salida.txt`: **ARNES PASA, 67/67** (265 s) antes del humo. Historia: el primer
  intento dio 66/67 (el "en el umbral" de la diferencia 0.04 fallaba por redondeo de coma flotante en el RUNNER; se corrigió redondeando a 4
  decimales, sin cambiar umbrales). Tras el humo se agregó (k) (ruta Pool con Pool falso, candado, parada): **70/70** (sec. 11 bis).
- Humo (1 proceso cada uno, práctica 734990–734998, NO cuenta): `--humo` = 2 cadenas × 2 pasajes de 12k + `o1` y `mix` de 20k (6 corridas,
  88 000 pasos); `--humo --reanuda` = `lib`, `neu`, `mixn`, `mixA` de 20k (4 corridas, 80 000 pasos) y lee (desde §11 ter; antes 3 corridas).
- **Costo (estimado antes del humo, a ~2.0 ms por paso con 9 cuerpos, medido en el arnés):** por índice 6 pasajes + 5 pruebas = 11 × 100k ≈
  2 200 s de CPU; serie 10 índices ≈ 22 000 s ≈ 3.1 h con pool 2 sin contención. Medido en el humo y recalculado con `mixA`: §11 bis y §11 ter.
  **N_IND = 10 queda fijo** (auditoría H-1).
```
python experimentos/organelos/o1_libre/construye_o1_lib.py --verifica
python experimentos/organelos/o1_libre/identidad_o1_libre.py
python experimentos/organelos/o1_libre/corre_o1_libre.py --humo
python experimentos/organelos/o1_libre/corre_o1_libre.py --humo --reanuda
python experimentos/organelos/o1_libre/corre_o1_libre.py --serie --pool 2 2>&1 | tee experimentos/organelos/o1_libre/serie_pool2.log
python experimentos/organelos/o1_libre/corre_o1_libre.py --replica --pool 2 2>&1 | tee experimentos/organelos/o1_libre/replica_pool2.log   # sólo por §7
python experimentos/organelos/o1_libre/corre_o1_libre.py --bloque <datos/serie_*/resumen.json>,<datos/replica_*/resumen.json>
```

## 12. Shas (antes del humo)
`pista_libre.py` `bf538326a74af8e4` · `construye_o1_lib.py` `5124b76a56b1169d` · `carros/O1_LIB.py` `04992e7de94806fd` · `carros/O1_LIB0.py`
`2ee0b7e8b9b013ad` · `corre_o1_libre.py` y este preregistro: los que registre la cabecera del log del humo.

## 11 bis. Resultado del humo (ESCRITO TRAS EL HUMO, 30-sep 16:31–16:42; NO cuenta; nada de §1–§10 cambia)
La versión de este preregistro que registran las cabeceras de los dos logs del humo es sha `cbc4b7d14585a776` (§1–§12 como arriba, con
"21 anclas" y el arnés 67/67). Lo único agregado después es esta sección y la línea del arnés 70/70 en §11.
- **Humo v1 (16:31, `datos/humo/humo_20260930_163159/`, `humo_salida_v1_FALLA_brazo.txt`, runner `5554214e7c248adc`): 2 abortos** en `o1` y
  `mix`: `trabajo()` armaba el JSON de la prueba con la clave `brazo` dos veces (la de `fila()` y la suya). Las corridas terminaron; falló el
  armado. Arreglo: `fila()` de la prueba sin `brazo` (una línea). No cambia ningún criterio. Queda como historia. **El humo v1 no lleva ERR**
  (falla del instrumento en un humo, antes de datos, sin cambio de criterio; auditoría H-6).
- **Humo v2 (runner `da5780c5031150fa`): `humo_salida.txt` (6 corridas, 88 000 pasos) y `humo_reanuda_salida.txt` (3 corridas, 60 000
  pasos), carpeta `datos/humo/humo_20260930_163543/`, 0 abortos (runner y carro ANTERIORES a los cambios de §11 ter).** V1–V6 True con 1 índice (V6: el neutro no usó ningún poder en sus 2 pasajes).
  A T 20k (práctica 734998): `o1` cruza 6/9 (R0 mediano 0.90); `lib` 5/9; `neu` 3/9; conquista `mix` −2.95 y `mixn` −1.70 hijos por linaje;
  poderes de la siembra tras 2 × 12k: 0.01–0.04 en lib y en neu (ningún separado). El mundo actúa (conversiones, mudanzas, quietos) y los cuatro
  poderes se usan en las pruebas. La letra, con 1 índice, da "NO en el umbral" (no cuenta).
- **La base de §8 era alta:** ~10 nacimientos reales por linaje en 20k (≈ 50 por 100k), no "cientos": 3 pasajes son ≈ 150 generaciones a lo
  largo de una línea y la deriva de un poder es del orden de 0.03·√150 ≈ 0.4 antes del recorte, no 0.5–1. **Las predicciones Q1–Q10 y V NO se
  mueven**; Q3 (neutro en [0.25, 0.65]) queda en riesgo y se declara aquí.
- **Costo medido (un proceso):** pasaje ≈ 2.13 ms/paso (100k ≈ 213 s); prueba ≈ 2.2–2.35 ms/paso (100k ≈ 230 s). Por índice 6 × 213 + 5 × 230 ≈
  **2 430 s de CPU**; serie de 10 índices ≈ 24 300 s → **≈ 3.4 h con pool 2 sin contención; 3.6–4.0 h con la serie o1_evo (pool 4) en la misma
  PC.** Réplica igual. (Costo recalculado con `mixA` y la colonización en §11 ter.)
- Shas al cierre del creador: `corre_o1_libre.py` `da5780c5031150fa` · `identidad_o1_libre.py` `a4b4d7d18cd9b5da` (salida `c7df18066bea2c2f`,
  70/70) · `pista_libre.py` `bf538326a74af8e4` · `construye_o1_lib.py` `5124b76a56b1169d` · `carros/O1_LIB.py` `04992e7de94806fd` ·
  `carros/O1_LIB0.py` `2ee0b7e8b9b013ad`.

## 11 ter. Cambios por auditoría (LISTO CON CAMBIOS) y por la junta o1_evo, ANTES de datos (30-sep, 16:50–17:30); ERR-160
Sólo había humos (no cuentan); ninguna corrida de serie existe. Cada cambio se probó en el arnés y en el humo v3.
- **ERR-160 (letra y mecanismo cambiados después de los humos, antes de datos; auditoría H-2, junta o1_evo y re-auditoría R-1/R-5a). Cinco
  puntos, cada uno con su contrafáctico en el humo v3 (`datos/humo/humo_20260930_172014/`):**
  - **(i) Umbral de PN:** "EN EL UMBRAL" cuenta PN sólo si PC ≥ 7/10. Contrafáctico v3 (PC 0, PN 0, umbral escalado 1): "en el umbral" por
    PC con las dos reglas; igual (también en v2). Arnés: 2 casos (PN 8 con PC 2 → fuera; PN 8 con PC 7 → dentro).
  - **(ii) V4 relajada:** antes "todos los fundadores O1_LIB salen de la siembra"; ahora "ninguno de fábrica y ≥ 1 de la siembra" (los
    refundadores salen de la colonia). **Contrafáctico v3: con la V4 vieja el humo habría salido NO SE LEE** (lib: 9 de siembra y 33 de
    colonia; mix 5 + 37; neu 11 + 148), porque (iv) cambió de dónde salen los refundadores.
  - **(iii) V5 + coloniza:** V5 exige además `PS_COLONIZA` 1 en cada pasaje y prueba O1_LIB. Contrafáctico v3: con la V5 vieja, True igual.
  - **(iv) Mecanismo de refundación:** de "desde la siembra vieja" a colonización (§2). Contrafáctico: no hay uno en la misma corrida; el humo
    v2 (mecanismo viejo) y el v3 (nuevo) tienen la misma letra ("NO en el umbral", con 1 índice; no cuenta) y V1–V6 True. Ningún número de
    la serie existía.
  - **(v) Extinción como dato (R-5a):** una cadena sin un solo parto en un pasaje entero (la siembra ya caía de t ≥ 50k a todo el pasaje)
    ya no aborta: queda `extinto` en su JSON, sus pruebas no se corren y quedan como JSON "extinto" (dato, no aborto). En la letra (**toca la
    letra**): conquista −∞ en la mixta de ese índice (`mixn` = pérdida del neutro; `mix` = pérdida de lib), el monocultivo cruza 0, PP cuenta
    lib > neu sólo con las dos cadenas vivas y las medianas se toman sobre las vivas; la validez se evalúa sobre las corridas que existen.
    Contrafáctico v3: ninguna extinción (105–116 partos por pasaje); igual. Arnés: h4–h6 (una cadena real de T 300 se extingue sin abortar y
    su `mixn` queda "extinto") y 2 casos sintéticos (neutro extinto en 2 y en 3 índices).
- **H-1:** N_IND = 10 fijo; se borró de §11 bis la cláusula que permitía bajar a 8 índices.
- **H-3:** en §6, la multiplicidad de PP (4 poderes, nulo ≈ 0.18); PP solo no pasa de MODESTO ni se cita sin réplica. Descriptivo nuevo: partos por pasaje lib contra neu.
- **H-4:** vocabulario "partos (descendientes)" y "nacimientos reales (recambio)"; en las mixtas, partos, muertes y fundadores por lado (descriptivos).
- **H-5:** PN se llama "no es sólo deriva (purga de carga)". Brazo `mixA` (siembra lib con poderes en 0 contra O1, mismas semillas), sólo
  descriptivo y fuera de V1; prohibido "conquista gracias a X" si `mixA` no lo separa. En §7, un NO "no contradice", no "refuerza".
- **H-6:** arnés k4 (la rama que permite la réplica y el candado de sha_runner); `O1_LIB0.py` en `git_limpio`; §7 aclara `--reanuda`; humo v1 sin ERR.
- **H-7:** "inventa" pasa a "sube"; los contadores se llaman "activaciones" (también en el carro: `_TEL[i]['activaciones']`).
- **H-8:** ventana de la siembra declarada (3 medios ciclos de escasez y 2 de abundancia, §4); arnés d6–d7: herencia directa del gen al hijo con σ > 0.
- **Junta o1_evo (V143_BQ2 sin material: Δ largo 0, carga cerca del umbral de error, refundación desde la siembra vieja con Ne ≈ 9, siembra
  fija de 5 por linaje). Revisión de o1_libre:**
  - (a) Siembra: **bien**, proporcional a los partos de cada linaje, sin cuotas (`corre_o1_libre.siembra`). Se agregan al JSON aportes por linaje, Ne por linaje y padres distintos.
  - (b) Refundación: **estaba mal** (un linaje extinto dentro de un pasaje o de una prueba se refundaba desde la siembra VIEJA). **Corregido
    antes de datos:** colonización desde los últimos 50 partos de OTRO linaje de la misma corrida (§2; arnés b6, d8, d9; V4 y V5 ajustadas).
    Es el punto (iv) de ERR-160.
  - (c) Ne en el humo v3 (T 12k por pasaje): cada siembra toma partos de **9/9 linajes, Ne por linaje 8.5–8.8** (aportes 3–8 por linaje), pero
    de sólo **9–11 padres distintos** (42–53 partos tardíos; ~4.5 partos por padre). En la serie (T 100k, ~300 partos tardíos) estimo
    ~40–65 padres distintos por siembra (extrapolación, no medido). Refundaciones en el humo: 20–63 por pasaje, casi todas ahora por colonia.
  - (d) Carga: ~0.9 partos por vida de cuerpo (13.4 partos y 15.2 muertes por linaje en 20k), no "50 hijos por vida" (50 es por LINAJE en
    100k). Desplazamiento de mutación por generación normalizado al clip: **0.088** (0.065 sólo los 10 genes de O1). Carga sin purga medida en
    el humo v3 (1 índice, ruidoso): el neutro, tras ~15 generaciones de deriva, baja el R0 de 0.90 (o1) a 0.44 → **≈ 4.6 % de R0 por generación**;
    con selección, lib queda en 0.92. Con R0 ≈ 0.9 (reemplazo justo), una carga del ~5 % por generación está **en el mismo orden que el margen
    selectivo: no está lejos del umbral de error**. Se declara como riesgo; σ no se cambia (es el de pasg y o1_evo).
- **Costo recalculado (humo v3, un proceso, con la PC compartida):** pasaje ≈ 2.29 ms/paso (100k ≈ 229 s); prueba ≈ 2.35–2.7 ms/paso (100k ≈
  235–270 s). Por índice 6 pasajes + 6 pruebas ≈ 1 374 + 1 500 ≈ **2 870 s de CPU**. Serie de 10 índices ≈ 28 700 s → **≈ 4.0 h con pool 2
  (3.7 h a los ritmos del humo v2; 4.2–4.6 h con la serie o1_evo en la PC). Réplica: igual.** Sale del objetivo de 2–4 h si la PC está
  cargada: correrlo con la PC libre (por ejemplo de noche). N_IND no se toca (H-1).
- **Humo v3** (runner `619c9e1ff79ee426`, preregistro `5900d5655463b27e` en la cabecera; `humo_salida.txt` 6 corridas / 88 000 pasos y
  `humo_reanuda_salida.txt` 4 corridas / 80 000 pasos; carpeta `datos/humo/humo_20260930_172014/`, resumen `30c8f44716e01cb3`): 0 abortos,
  V1–V6 True. A T 20k: o1 6/9 (R0 0.90); lib 5/9 (0.92); neu 1/9 (0.44); conquista mix −1.3, mixn −0.35, mixA −0.5; poderes 0.01–0.06 en
  lib y en neu. No cuenta. Los humos v2 quedan en `humo_salida_v2.txt` y `humo_reanuda_salida_v2.txt`.
- **Arnés `identidad_o1_libre.py` (`4c24226d8b857fe0`) → `identidad_o1_libre_salida.txt` (`5978895daf163fee`): ARNES PASA, 79/79 (381 s).**
  En el camino falló dos veces y se corrigió antes de datos: un `KeyError` en la lectura si faltaba `mixA` (runner) y la aserción g4
  (con colonización, no todos los fundadores salen de la siembra).
- **Shas finales:** `corre_o1_libre.py` `619c9e1ff79ee426` · `pista_libre.py` `bf538326a74af8e4` · `construye_o1_lib.py` `ec63375ee0b980d0` ·
  `carros/O1_LIB.py` `ff30214f59ed36d8` · `carros/O1_LIB0.py` `7dda8b7f8448b386` · este preregistro: el que quede commiteado.

## 11 quater. Re-auditoría (LISTO CON CAMBIOS), antes de datos (30-sep, 17:30–17:47)
- Aplicados R-1 (ERR-160 en cinco puntos, §11 ter), R-2 (§9 canal de genes por colonización y su asimetría; §7 prohibición con `mixA`),
  R-3 (arnés d1c–d1d), R-5a (extinción como dato, ERR-160 v; arnés h4–h6 y 2 casos sintéticos) y R-5b (§7 regla de carga; §8 Q11).
- **Arnés: ARNES PASA, 88/88** (379 s; `identidad_o1_libre.py` `36ce8613aa8b3520`, salida `630181a6797f14ab`).
- **Humo v4** (runner `98d3a103a1fdde3b`, preregistro `104a298e63f4eb87` en la cabecera; `humo_salida_v4.txt` 6 corridas / 88 000 pasos y
  `humo_reanuda_salida_v4.txt` 4 corridas / 80 000 pasos; carpeta `datos/humo/humo_20260930_174032/`): 0 abortos, V1–V6 True; los mismos números
  que el v3 (mismas semillas; el runner nuevo sólo cambia la lectura). La regla de carga dispara en el humo (R0 de lib 0.20 → 0.00 entre los
  pasajes de 12k), pero con 12k casi ningún linaje llega a 5 muertes y el R0 por pasaje no tiene sentido ahí: el humo no cuenta.
- Shas finales: `corre_o1_libre.py` `98d3a103a1fdde3b` · `pista_libre.py` `bf538326a74af8e4` · `construye_o1_lib.py` `ec63375ee0b980d0` ·
  `carros/O1_LIB.py` `ff30214f59ed36d8` · `carros/O1_LIB0.py` `7dda8b7f8448b386`. Costo: el de §11 ter (≈ 4.0 h por serie con pool 2).
