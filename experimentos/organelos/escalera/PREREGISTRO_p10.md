# PREREGISTRO — PELDAÑO 10 DE LA ESCALERA: IR AL LUGAR DEL QUE HACE MÁS TIEMPO NO TIENE DATO, EN UN MUNDO DONDE EL OASIS SE MUDA (O1_LUGAR_PREG), CONFIRMATORIO (30-sep-2026, noche)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y
réplicas). Encargo del director (30-sep, "LA ESCALERA", modo ráfaga). Ingeniero genético: Fable. Plan: `ESCALERA.md` (P10).
**DECLARACIÓN (sesgo del diseñador):** este diseño VIENE DE UNA EXPLORACIÓN VISTA: un humo (739890–739891, T 30k, mueve 10k) y una
exploración (739801–739802, T 100k, mueve 20k) de un proceso (sec. 11, `BITACORA.md`). Con ellos se eligió medir el cruce a T 100k (a T 30k
el juez no evalúa a los linajes que viven 3 600 pasos) y se vio la trampa 3 (el candidato pela el mundo), que aquí se declara y se reporta.
Las semillas de la serie son NUEVAS y disjuntas de las vistas. Escrito ANTES de cualquier dato de serie. ERR-175 queda asignado a P7 H-9; este
bloque no abre ninguno.

## 0. Qué es y qué no es
Es DISEÑO dirigido: el ingeniero pone en O1_LUGAR (P1, serie FUNCIONA 30-sep) un módulo (PREGUNTA) con dos piezas locales y pone en el mundo
una perilla (`mueve`) que hace que lo recordado caduque. NO es selección natural y NO es "curiosidad": el nivel 8 (18-sep) refutó la curiosidad
por progreso/novedad/saturación en un mundo donde explorar no pagaba; aquí explorar paga porque el oasis se muda. Lo que se afirma, si FUNCIONA,
es una conducta medida: el CONJUNTO de las dos piezas del módulo —(a) olvidar el sitio donde tiene hambre y no ve nada y (b), sin blanco a la
vista y sin recuerdo, ir al lugar del que hace más tiempo no tiene dato— hace que el linaje dé su primer bocado dentro del oasis nuevo antes
que la base y que el control, y cruce más. No hay brazo "sólo olvido": el efecto se atribuye al conjunto, no a una pieza (H-2). Nada más.

## 1. Pregunta
En el mundo de P1b donde el oasis se muda cada 20 000 pasos (4 veces en T 100k), ¿O1_LUGAR + PREGUNTA (`preg`) cruza más y se refunda menos
que O1_LUGAR (`lug`) y que O1_LUGAR + PREGUNTA con destino antípoda (`pregbar`), y lo hace encontrando ANTES el oasis nuevo (latencia desde
cada mudanza hasta el primer bocado dentro, física)?

## 2. Mecanismo y memoria nueva (carro `O1_LUGAR_PREG`, `construye_c.py`, por anclas sobre el texto de O1_LUGAR de `construye_p1.py` sha `90dc1b6f848fac80`)
- **(a) Olvido por presencia:** cada paso con necesidad (min(E, Ag) < U + MARGEN = 1.25) y sin nada útil a la vista, el bin donde está pierde
  `PG_OLVIDO` = 1 % de su memoria de lugar ("estar aquí con hambre y no ver nada = este sitio ya no da"). Sin esto la memoria de P1 sólo se
  corrige al morder, y en el oasis viejo ya no hay qué morder: el linaje volvería para siempre.
- **(b) Pregunta:** cuando O1 no tiene blanco a la vista NI sitio recordado (en P1 iba al "hueco" entre los otros cuerpos), va al centro del bin
  que hace MÁS tiempo no visita, ponderado por distancia (edad / (d + D0)). Memoria nueva: `visto` = 30 enteros (último paso de visita por bin),
  del linaje (viaja en `al_parir`/`nace`; el fundador limpio nace sin nada). Promotor `PREGUNTA` (0 ⇒ O1_LUGAR bit a bit, arnés).
- Nada más cambia: urgencia, blancos, limpieza, partos, memoria de lugar y de letra son los de P1/O1.
- **Control `O1_LUGAR_PREG_BAR`** (`PG_BARAJA` = 1): (a) igual; (b) va al ANTÍPODA (b + 15 mod 30) del bin elegido. Como el bin se recalcula en
  cada paso, el antípoda queda siempre lejos: es un control PESIMISTA ("destino lejano sin información"), no de igual costo (el número de
  excursiones difiere: humo 2 24.6k vs 16.5k; exploración 378k vs 462k). PB se lee como "destino informado frente a destino lejano sin
  información" (H-1). El mismo tipo de antípoda que P1 y P7 (ERR-170), con esta diferencia declarada.
- Los tres carros pasan `revisa_carro`.

## 3. Mundo (`mundo_tramo_c.py` sha `4a1044a4e0e1d5c9`: `pista.py` `9f47c65e438e0ff4` + 9 anclas de `mundo_escalera.py` `4f28b372207ba0a6` + 8 propias)
El de P1b (`oasis 1, extra 0.8, pobre 0.5, dens 0.5, vista_r 20`; T 100 000; monocultivo de 9; fundador limpio) con UNA perilla nueva:
- `mueve` = 20 000: cada 20k pasos el oasis se muda a un arco nuevo (misma corriente rng de la zona `[seed, 0, 18, 0]`; se re-sortea hasta que
  no se solape con el anterior: el oasis nuevo NUNCA se solapa con el anterior, así que "ir al lugar del que hace más tiempo no tiene dato"
  coincide con la regla del mundo; no se probó un mundo donde el oasis pueda volver al mismo sitio, y eso se declara, H-5). La reposición
  densa (`dens`) sigue al oasis nuevo; los objetos del viejo se quedan. Con `mueve` = 0 es
  `mundo_escalera` bit a bit (arnés M). Las demás perillas del tramo C (`c_e`, `letra_x`, `cerrojo`, `cerrojo_pobre`) van apagadas.
- Por qué paga y por qué evitar no es gratis: lo recordado caduca; quien no vuelve a mirar se queda con un mapa viejo y vaga por el hueco (O1).
- Física nueva por linaje: `latencias` = pasos desde cada mudanza hasta el primer bocado A+C dentro del oasis nuevo (None = nunca).

## 4. Brazos
| brazo | carro | mundo | qué es |
|---|---|---|---|
| `preg` | O1_LUGAR_PREG (`4e12a5708ecb5dea`) | P1b + `mueve` 20k | CANDIDATO |
| `pregbar` | O1_LUGAR_PREG_BAR (`27489bd5d4431b85`) | P1b + `mueve` 20k | control PESIMISTA de contenido: destino lejano sin información (el antípoda del bin elegido, recalculado cada paso, queda lejos); NO es de igual costo: excursiones 24.6k vs 16.5k en el humo 2 y 378k vs 462k en la exploración (H-1) |
| `lug` | O1_LUGAR (`49eee6bb278ea097`) | P1b + `mueve` 20k | la BASE (P1) |

## 5. Medidas
- **Principal:** linajes que cruzan (`cruza_real`), por semilla y suma (de 180); pareado por semilla, empates en contra.
- **Co-principal:** fundadores por linaje (media de 9) por semilla, pareado `preg` < `lug`.
- **Mecanismo (física):** latencia mediana por corrida (sobre linajes × mudanzas; nunca = T) desde la mudanza hasta el primer bocado A+C
  dentro del oasis nuevo, por linaje (incluye las vidas nuevas del linaje): `preg` < `lug` y `preg` < `pregbar`, pareado. **Sesgos declarados
  (H-3):** PM NO tiene el sesgo de exclusión de P7 (el denominador es fijo, 9 linajes × 4 mudanzas = 36 por corrida, y "nunca" cuenta como T);
  pero comparte variable con PF: un fundador limpio no conoce A/C y tarda en morder, así que un linaje que se refunda mucho tiene latencias
  largas por las dos razones (menos refundaciones y encontrar antes van juntas). PM y PF no son evidencias independientes.
  **H-4:** la comparación `preg` vs `pregbar` de latencia (pmc) se lee de `lat_med` en los `prueba_*.json` de la carpeta (el runner la calcula
  dentro de PM pero no la guarda como pareado aparte ni la incluye en `en_umbral`; sólo `preg` vs `lug` entra en `en_umbral`).
- **Trampa 3 (declarada, se reporta, NO puntúa):** mundo A+C del candidato sobre la base. En la exploración `preg` pela el mundo (4.3 vs 6.8:
  razón 0.63) porque pasa más tiempo en el oasis (6.9× el azar); en monocultivo los 9 linajes son el mismo brazo, así que lo que se pela lo
  pelan todos por igual: no es un candidato que gana quitándole la comida a un rival. Se reporta la razón y el tiempo en el oasis.
- Descriptivos: R0, establecidos, vida mediana, nunca-llegan, excursiones (pg_exc) y olvidos (pg_olv) del carro (no puntúan; V5 los usa como
  validez del instrumento), razón de pasos en el oasis.

## 6. LA LETRA (`corre_p10.lee_serie`; casos sintéticos en el arnés (f), 8 casos)
**Validez (si una falla: NO SE LEE):**
- V1: serie completa (20 × 3), 0 abortos, contabilidad coherente.
- V2: el mundo se muda: 4 mudanzas en TODA corrida y `mueve` 20 000 escrito.
- V3: el mundo actúa: mordidas A+C dentro > 0, `extra` 0.8, `pobre` 0.5.
- V4: estado por worker: carro y `mueve` correctos; `PREGUNTA` 1 en `preg`/`pregbar`, `PG_BARAJA` 1 sólo en `pregbar`; `LUGAR_BARAJA` 0.
- V5: el módulo actúa: excursiones > 0 y olvidos > 0 en toda corrida de `preg` y `pregbar`; 0 en `lug`.
**Puertas (n 20):**
- PA-par: `preg` > `lug` en linajes que cruzan en ≥ 13/20. PA-suma: suma(`preg`) ≥ suma(`lug`) + 10.
- PB-par: `preg` > `pregbar` en ≥ 13/20. PB-suma: suma(`preg`) ≥ suma(`pregbar`) + 10. (PB = "destino informado frente a destino lejano sin
  información": control pesimista, no de igual costo; H-1.)
- PF: fundadores de `preg` < `lug` en ≥ 13/20.
- PM: latencia de `preg` < `lug` en ≥ 13/20 Y `preg` < `pregbar` en ≥ 13/20.
**Veredictos:** FUNCIONA = V1–V5 y SEIS condiciones: PA-par, PA-suma, PB-par, PB-suma, PF, PM. HAY ALGO MODESTO = no FUNCIONA, y (PA-par o
PA-suma o PF) y (PB-par o PB-suma) y PM. NO = lo demás; si gana sin PM → "NO (gana sin encontrar antes el oasis nuevo: instrumento)". EN EL
UMBRAL: cualquier pareado a ±1 de 13 o suma a ±1 de 10. Serie + réplica: si coinciden vale ése; si no, el menor; NO SE LEE manda.
PB es NECESARIA (signo del contenido: sin ella lo que paga es "salir de excursión", no "ir a donde menos se sabe"); PA mide superar a O1_LUGAR.
**Nulos:** cada pareada bajo p = 0.5: P(≥ 13/20) = 0.132; las sumas: media 0 bajo el nulo, dispersión no calibrada (se reporta); FUNCIONA exige
las seis a la vez (nulo entre 0.0003 y 0.132 según la dependencia); MODESTO ≤ 0.132.

## 7. Regla de parada y vocabulario
- Réplica (739851–739870) sólo si la serie da FUNCIONA, MODESTO o NO en el umbral; candado con el mismo sha del runner.
- FUNCIONA ×2 → "O1 con memoria de lugar más el conjunto de dos piezas —olvida el sitio donde tiene hambre y no ve nada y, sin blanco y sin
  recuerdo, va al lugar del que hace más tiempo no tiene dato— en un mundo donde el oasis se muda, da su primer bocado A+C dentro tras la
  mudanza antes que la base (por linaje, incluye vidas nuevas) y cruza más que la base (O1_LUGAR, que sin blanco va al hueco entre los otros
  cuerpos) y que el control con destino lejano sin información". No se atribuye el efecto a una pieza sola (H-2). PERMITIDO: "ir al lugar del que hace más tiempo no tiene dato", "en un mundo donde el oasis se muda", "lo recordado
  caduca". PROHIBIDO: "se pregunta" o "preguntarse" como experiencia interna, "curiosidad", "sabe que no sabe", "explora por explorar",
  "piensa", "planifica", "entiende". (El nombre del peldaño en ESCALERA.md es un rótulo; la frase que se declara es la permitida.)
- Depende de P1 (serie FUNCIONA 30-sep; réplica en curso): si la réplica de P1 lo baja a NO, P10 se lee igual pero no sube a declarado.
- Si PB cae, el código da NO: se dice "lo que paga es la excursión, no el destino".

## 8. Predicciones firmadas (antes de la serie; calibradas con la exploración de 2 semillas, declarado)
| # | predicción | rango | p |
|---|---|---|---|
| Q1 | `lug`: suma de linajes que cruzan | [60, 120] de 180 | 0.70 |
| Q2 | `preg`: suma | [100, 160] | 0.65 |
| Q3 | `pregbar`: suma | [20, 80]; < `lug` (ir al antípoda cuesta) | 0.70 |
| Q4 | V2 y V5 (el mundo se muda 4 veces; el módulo actúa en toda corrida) | | 0.90 |
| Q5 | PA (par ≥ 13/20 y +10) | | 0.70 |
| Q6 | PB (par ≥ 13/20 y +10) | | 0.80 |
| Q7 | PF (fundadores `preg` < `lug` ≥ 13/20); medianas `preg` ≤ 5, `lug` ≥ 15 | | 0.80 |
| Q8 | PM (latencia `preg` < ambos ≥ 13/20); medianas `preg` ≤ 700, `lug` ≥ 1000, `pregbar` ≥ 1200 | | 0.75 |
| Q9 | trampa 3: mundo A+C `preg` / `lug` en [0.5, 0.8] (pela; se reporta) | | 0.70 |
| Q10 | nunca-llegan: `preg` ≤ 5 de 720, `lug` ≥ 20, `pregbar` ≥ 30 | | 0.65 |
| V | veredicto de la SERIE: FUNCIONA / MODESTO / NO / NO SE LEE | | 0.50 / 0.20 / 0.20 / 0.10 |

## 9. Las cuatro trampas
- **Canal simétrico:** no hay canal. **Acierto sin balancear:** la medida es `cruza_real`, fundadores y latencia (física).
- **Mundo que se come la comida:** SÍ ocurre (Q9) y se declara: `preg` pasa más tiempo en el oasis y lo pela; en monocultivo lo pelan los 9 por
  igual; se reporta la razón A+C y la razón de pasos. Si `preg` ganara sólo por comer más donde ya estaba, PM no pasaría (la latencia es por
  mudanza, no por tiempo en el oasis).
- **Sitios fijos:** el oasis se sortea por semilla y se muda 4 veces por corrida; semillas nuevas 739821–739840.

## 10. Instrumento, semillas, costo, comandos
- Runner `corre_p10.py` (`--humo`, `--explora`, `--serie --pool ≤ 2`, `--replica`, `--lee`, `--reanuda`); usa `corre_c.tarea`/`fila_c` y
  `corre_p1.fila` (congelado `392b71186cf49b60`); JSON por trabajo; estado por worker (V4); candados como P7 (git limpio de preregistro,
  runner, los seis archivos de `SHAS_P10` y los carros; veredicto previo; réplica sólo por la regla de parada y con el mismo sha del runner;
  pool ≤ 2). `SHAS_P10` fijados al cerrar: corre_p1 `392b71186cf49b60`, construye_p1 `90dc1b6f848fac80`, mundo_escalera `4f28b372207ba0a6`,
  mundo_tramo_c `4a1044a4e0e1d5c9`, construye_c `024a89476109b997`, corre_c `01e4ad94dd06e133` (si alguno cambia, el runner no corre).
- Arnés `identidad_p10.py` → `identidad_p10_salida.txt`: **ARNES PASA 29/29** (T 4500, 84 s, con los shas fijados): mueve 0 == mundo_escalera
  BIT A BIT (salida entera y rng); PREG0 == O1_LUGAR (salida entera, con mudanza); el oasis se muda y los objetos nacen en el nuevo; módulo y
  control actúan; pieza (a) muda; regla 14 a nivel de fila contra `corre_p1.trabajo`; JSON/reanuda/nube-9; letra sintética 8 casos; guardas.
- **ERR-42 (main() ejercitado antes de la serie):** `corre_p10.py --humo --n 1 --T 10000 --mueve 3000 --desde 739892` con el runner final y
  los shas fijados, un proceso (`humo_p10_2_salida.txt`: V1–V5 True, 0 abortos; veredicto a T 10k "NO", no cuenta) y `--lee` sobre su carpeta
  (`humo_p10_2_lee_salida.txt`). Una línea en `BITACORA.md`.
- **Semillas NUEVAS 7398xx:** serie 739821–739840; réplica 739851–739870; humo 739890–739891 (usados); exploración 739801–739802 (usados);
  arnés 739880–739889.
- **Costo medido** (exploración, un proceso, T 100k): `preg` 112–136 s, `pregbar` 125–133 s, `lug` 111–136 s → por semilla ≈ 380 s → serie ≈
  2.1 h CPU → **≈ 1.1 h con pool 2**; réplica igual.
```
python experimentos/organelos/escalera/construye_c.py --verifica
python experimentos/organelos/escalera/identidad_p10.py
python experimentos/organelos/escalera/corre_p10.py --serie --pool 2 2>&1 | tee experimentos/organelos/escalera/p10_serie_pool2.log   # coordinador
python experimentos/organelos/escalera/corre_p10.py --replica --pool 2 2>&1 | tee experimentos/organelos/escalera/p10_replica_pool2.log
```

## 11. Historia honesta (ráfaga; NADA de esto cuenta; `BITACORA.md`)
1. **Humo 1** (739890–739891, T 30k, mueve 10k, `corre_c`): latencia tras la mudanza preg 498 / lug 1118 / antípoda 1652; nunca 0 / 3 / 5;
   fundadores 0.9 / 18.3 / 22.6; establecidos 18 / 14 / 10; vida 3656 / 1020 / 600; PERO cruzan 1 / 2 / 5: a T 30k el juez no evalúa a los que
   viven 3 600 pasos (< 5 muertes) y el antípoda cruza porque muere y pare rápido. Lectura: señal de establecimiento, cruce no leído → exploración.
2. **Exploración 1** (739801–739802, T 100k, mueve 20k): cruzan **preg 16 / lug 11 / pregbar 5** (pareado 2/2 contra ambos; pregbar < lug 2/2);
   latencia 408 / 1283 / 1511; nunca 0 / 3 / 5; fundadores 0.6 / 27.9 / 50.2; establecidos 18 / 15 / 9; vida 1782 / 801 / 600; R0 0.96 / 0.96 /
   0.77; excursiones 378k (preg) vs 462k (pregbar): el control sale igual o más y le va peor. Mundo A+C 4.3 / 6.8 / 7.5 (trampa 3, Q9).
3. Lo que NO se sabe: si con 20 semillas `lug` se acerca a `preg` (en P1 `lug` cruzó 79/180 sin mudanzas; con mudanzas la base pierde el mapa 4
   veces); si la pieza (a) sola (olvido) explica parte del efecto (no hay brazo de lesión: se declara; P10-lesión sería otro preregistro).

## 12bis. Cambios por auditoría antes de datos (30-sep) — auditor: LISTO CON CAMBIOS, sólo texto
- H-1: el control NO es de igual costo: el antípoda se recalcula cada paso y queda lejos (control pesimista; excursiones humo 2 24.6k vs
  16.5k, exploración 378k vs 462k). PB reescrita como "destino informado frente a destino lejano sin información" (secs. 2, 4, 6).
- H-2: el efecto es del conjunto (a) olvido + (b) ir al menos visitado; no hay brazo "sólo olvido". Retirado "en vez de al hueco (O1)" de la
  sec. 0; la aclaración va en la frase de FUNCIONA ×2 (sec. 7).
- H-3: PM no tiene el sesgo de exclusión de P7 (denominador fijo 36; "nunca" = T) pero comparte variable con PF (el fundador limpio no conoce
  A/C). "Encuentra antes el oasis que se mudó" → "primer bocado A+C dentro tras la mudanza, por linaje, incluye vidas nuevas" (secs. 5, 7).
- H-4 (opción A): pmc (latencia `preg` vs `pregbar`) se lee de `lat_med` en los `prueba_*.json`; el runner no la incluye en `en_umbral` (sec. 5).
- H-5: el oasis nuevo nunca se solapa con el anterior; "ir al menos visitado" coincide con la regla del mundo; no se probó un mundo donde el
  oasis pueda volver (sec. 3).
- H-6: línea de ERR: "ERR-175 queda asignado a P7 H-9; este bloque no abre ninguno". Números del humo 2 pegados abajo (sec. 12).
Ningún .py cambió; la letra por código (sec. 6) no cambió.

## 12. Cierre antes de datos (30-sep, 22:40)
- **Humo 2 (ERR-42; 739892, T 10k, mueve 3000, 3 mudanzas; NO cuenta):** cruzan 0 / 0 / 0 (T corto); fundadores por linaje preg 0.0 / pregbar
  8.8 / lug 10.1; latencia tras la mudanza 560 / 10000 (nunca) / 2450; nunca-llegan 1 / 15 / 12 de 27; excursiones 24 571 / 16 543 / 0; mundo
  A+C 4.4 / 9.4 / 8.9; V1–V5 True, 0 abortos; veredicto a n 1 "NO" (PA/PB no se leen con 0 cruces).
- Humo 1 y exploración 1 corrieron con `corre_c.py` (runner de ráfaga, mismas `tarea`/`fila_c` que importa `corre_p10`). Para ERR-42 el
  `main()` de `corre_p10.py` se ejercita de punta a punta con un humo corto (sec. 10) con el runner final y los shas fijados: los números de ese
  humo (T 10k) no cuentan ni calibran nada; se pegan abajo al cerrar.
- Sesgo del ganador declarado: la letra, los brazos y las predicciones se escribieron DESPUÉS de ver el humo 1 y la exploración 1 (dos semillas,
  739890–739891 y 739801–739802); las semillas de la serie (739821–739840) y la réplica (739851–739870) son nuevas y disjuntas.
- Nada de P1/P7 se tocó: `mundo_tramo_c` es el mismo sha fijado en P7 (`4a1044a4e0e1d5c9`).
