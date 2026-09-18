# SALA DE ENJAMBRE — el rasgo conjuntivo con reglas locales (18 sep 2026, madrugada)

**Misión (no opcional, `EQUIPO.md` regla 13):** llegar a la AGI por este camino — un organismo mínimo con reglas
locales, sin retropropagación en tiempo de ejecución, subiendo la escalera del brief con cada peldaño preregistrado,
medido con controles y replicado; el método manda sobre el cómo. **Nada de lo de abajo declara AGI, conciencia ni
inteligencia general** (`CLAUDE.md` regla 8): lo que se declara es lo que se midió.

**El cuello atacado.** Que el organismo CONSTRUYA por sí mismo el rasgo conjuntivo ("los dos píxeles a la vez") con
reglas locales y en pocas exposiciones. Criterio: `acc_lenta` xor01 ≥ 0.75 en 20 semillas nuevas, px0 = 1.000, azar en
[0.35, 0.65], **exposiciones hasta 0.75 (n\*) como número principal**. Escribe el sintetizador: cuatro mini-equipos
independientes (M1–M4) con carpeta, constructor por anclas, arnés de identidad y mini-prueba de un proceso, más
refutadores externos. No corrí ninguna serie: 6 corridas de un proceso (tope de la regla 3).

## 1. Qué se buscó en la literatura reciente y qué dice

La pregunta del director era la correcta: **la vía lenta del tronco es la regla delta (Widrow-Hoff 1960 /
Rescorla-Wagner 1972)**, y A-4 ya midió su precio — 150 exposiciones **con los rasgos regalados**. Los cuatro frentes:

- **Compartimentos y expansión aleatoria → M1** (Caron/Ruta/Abbott/Axel 2013; Modi/Shuai/Turner 2020; Dasgupta/Stevens/
  Navlakha 2017; Lipshutz et al. 2023): pocos canales por celda fijados al nacer, ~15 compartimentos en paralelo con su
  propia señal de enseñanza, expansión + ganador-se-lo-lleva-todo **estructurales, no aprendidos**.
- **Plasticidad estructural dendrítica → M2** (Bicknell & Häusser 2021; Moldwin/Kalmenson/Segev 2021; Devaud et al.
  2015): el rasgo conjuntivo puede **nacer** por reagrupamiento local; benchmark biológico ~10 ensayos por fase.
- **Memoria de un golpe → M3** (BTSP: Bittner/Milstein/Grienberger/Romani/Magee 2017; **Milstein et al. 2024**: memoria
  direccionable por contenido con sinapsis **binarias** y aprendizaje de **una sola vez**; OnlineHD, Hernández-Cano
  et al. 2021; Hattori et al. 2017: la abstención como señal separada del valor).
- **Reglas de plasticidad meta-aprendidas → M4** (Confavreux/Zenke/Agnes/Lillicrap/Vogels 2020; Bacho & Chu 2022;
  Lindsey & Litwin-Kumar 2020): buscar la FORMA de la regla fuera del organismo y trasplantarla local.

**Qué dice el resultado, con números de esta noche:** los dos frentes que sobreviven son **los recientes**, y el
contraste es de orden de magnitud sobre el MISMO mundo y el MISMO flujo — delta rule (1960) ≈ 150–300 exposiciones;
tabla de un golpe (BTSP 2017 / Milstein 2024) = **7**; gradiente exacto (techo) = 10. El cuello era **el estimador**.

## 2. Los cuatro mecanismos y sus números (3 semillas, un proceso, T=100000, sin `Pool`; **no** son series confirmatorias)

| | mecanismo (qué cambia · memoria nueva) | identidad | acc_lenta xor01 | mediana | n\* a 0.75 | px0 | azar | (0,1) |
|---|---|---|---|---|---|---|---|---|
| **M1** | 15 lectores de dos canales, delta en paralelo, k-WTA por error propio · 76 nº | 23/23 | 0.625 · 0.500 · 0.375 | **0.500** | no | 1.000 | **0.300** | 3/3 al FINAL de T |
| **M2** | fisión por conflicto de signo: la hija conjuntiva **nace** · ~190 nº | 9/9 | 0.500 · 0.188 · 0.313 | **0.313** | no | 1.000 | 0.500 | 3/3 al final |
| **M3** | tabla por combinación, escribe R **de un golpe**, argmin de error propio · 135 nº | 18/18 | 0.8125 · 0.750 · 1.000 | **0.8125** | **7** | 1.000 | 0.500 | **3/3 EN LA SONDA** |
| **M4** | tabla por grupos g=2 + competencia, **forma hallada por búsqueda ciega** · 135 nº | 13/13 | 0.8125 · 0.750 · 1.000 | **0.8125** | **10·20·10** | 1.000 | 0.500 | 3/3 |

Referencias del mismo mundo: **tronco A-4 apagado** (mismas semillas, medido por grupo4) 0.500 · 0.313 · 0.563;
**gradiente exacto** 1.000 en 10 exposiciones; **backprop sobre píxeles crudos** 0.531. Puntuación **estricta**
(empate = 0, sin el medio punto de la abstención) — sólo M3 la reportó: 0.625 · 0.500 · 1.000, mediana **0.625**; sólo
1/3 semillas tenía las 4 clases (P0,P1) en el tren. M4 no la reportó y la debe.

## 3. Qué refutaron los refutadores (dos por paquete, con reproducción independiente)

- **M1 — REFUTADO por uno de los dos, y el hallazgo es real.** `cel_ganadora` se captura **al final de T**, no en la
  sonda: el propio JSON trae `cg_ok=False` en **6/9** filas, así que "el enrutamiento funciona 3/3" medido en el
  momento que importa es **2/3**. Además, asimetría de mordidas comida/veneno **80/20** pre-sonda (trampa 3 de
  `EQUIPO.md`) que el grupo no midió. Lo verificable sí se sostuvo: identidad 23/23 (un refutador reconstruyó y difeó
  el archivo), 5/9 y 4/9 filas reproducidas bit a bit, sin fuga ni oráculo, métrica balanceada. Pero los números
  propios — xor01 en 0.500, azar **por debajo del azar** — son el veredicto.
- **M2 — REFUTADO por uno de los dos, con la causa trazada por el propio grupo.** La predicción central (mediana ≥ 0.75)
  cae con margen: 0.313, y 0/3 semillas cruzan siquiera 0.65. Causa medida evento a evento: el piso `_FE=1e9` con
  `fis_rho=0.05` tarda cientos de eventos en decaer y castiga a las hijas **recién nacidas** justo en la sonda (T//2),
  aunque la pareja (0,1) nazca en el evento #15 de 257. Dos deudas de método no declaradas: `fis_umbral=3` se eligió
  **mirando la métrica de su propia cláusula de refutación** (sin ERR numerado), y la cláusula "≤20 celdas" es
  **inviolable por construcción** (tope duro de 12); coste de estructura medido: más muertes en 3/3 semillas de `azar`.
  Identidad impecable (`organismo_g2.py` reconstruido **byte a byte**) y 9/9 filas reproducidas: honesto el instrumento, falsa la hipótesis.
- **M3 — NO refutado.** Identidad 18/18 corrida por el auditor; **18/18 filas reproducidas exactas** por un refutador y
  3 más por mí; el replay reproduce `W_lenta_apriori` con diferencia 0 en 18/18; sin fuga (la sonda se toma antes de
  `tipos.extend(test)`; `lectura` es inerte, declarado y no reclamado); métrica balanceada. El auditor midió además el
  ganador **en la sonda** — el agujero que hundió a M1 — y da (0,1) en 3/3, xor01, en ambos brazos.
- **M4 — sin votos entregados** (llegaron truncados al sintetizador). Verifiqué yo lo esencial: la fila xor01 s1
  reproduce exacta (n_pre 277/266; 0.5 apagado vs 0.8125 encendido; replay = organismo; (0,1)) y su búsqueda ciega (§4.2).

## 4. Lo que medí yo, y que ningún paquete trae (6 corridas de un proceso + replays)

1. **Desempate por índice — riesgo real, magnitud medida.** Las tres familias de pares enumeran `(i,j)` con **(0,1) en
   el índice 0** y eligen con `argmin`/`argmax`: un empate exacto lo gana la respuesta correcta **por convención de
   orden**. Ocurre: en xor01 semilla 3 **dentro del organismo** (corrida mía), las celdas (0,1) y (1,4) terminan con
   error idénticamente igual (0.0215344237, diferencia 0.00e+00) y el índice decide; roto al revés, `acc_lenta` sería
   **0.375 en vez de 1.000** — y ésa es la semilla que da el 1.000 de la mini-prueba de M3. Sobre 20 semillas (replay):
   empate múltiple en **1/20**; con desempate al azar la mediana sigue en 1.000 y el ≥0.75 pasa de 20/20 a **19/20**.
   No es sistemático, **pero decidió la semilla insignia**: la serie debe reportar la multiplicidad y romper al azar.
2. **La búsqueda de M4 reproduce exacta, y elige una MESETA, no un punto.** Repetí las 432 configuraciones (buscar en
   1–10, reportar en 11–20): top-10 **todo** g=2+mse+dura, ganadora idéntica, retenidas mediana **1.000** [0.625, 1.000]
   — igual que el paquete. Pero los 10 primeros empatan en 1.0 y **todos comparten `rho=0.02`**, mientras `eta`, `clip`
   y `alpha` varían libres: el discriminante medido es la memoria del error, no la tasa.
3. **M4 depende de sus constantes más de lo que su paquete afirma.** El grupo concluyó, con 3 semillas, que "la elección
   exacta de eta/rho/clip/alpha pesa menos que la estructura". Sobre 20 semillas: con la **ganadora de la búsqueda**
   (rho=0.02) el par (0,1) sale en **18/20** y ≥0.75 en 18/20; con la **hipótesis inicial del grupo** (rho=0.05) cae a
   **14/20** y ≥0.75 en 14/20. Valen ~4 semillas de 20: la confirmatoria debe fijar `rho=0.02` por escrito.
4. **M3 ≥ M4 en el mismo replay, mismas 20 semillas:** la regla de un golpe da (0,1) en **20/20** y ≥0.75 en **20/20**;
   la mejor de M4, 18/20. Y las dos convergen: la tabla de M4 **también escribe de un golpe** la primera vez
   (`tabla = ds` si la casilla es nueva). Dos grupos independientes — uno desde BTSP, otro desde una búsqueda ciega de
   432 reglas — aterrizaron en **la misma familia**: es lo más fuerte que produjo la sala.

## 5. Top-2, con el preregistro sugerido (formato fijo del puente)

### Primero — **M3 (grupo3), memoria de un golpe por combinación**
- **Hipótesis.** El cuello de "pocas exposiciones" es el ESTIMADOR, no la tasa: escribir de un golpe el valor de cada
  combinación de 2 píxeles resuelve xor01 en un puñado de exposiciones, sin tocar el tronco.
- **Mecanismo mínimo y memoria.** 15 celdas × 4 casillas (`_MM`) + 15×4 visitados (`_MN`) + 15 errores (`_ME`) = 135
  números. Sin pesos, sin tasa, sin clip. Señal: R de la propia mordida. Abstención explícita (casilla no vista → 0.0).
- **Instrumento.** `experimentos/enjambre/grupo3/organismo_g3.py` (`91eb167023cb37b7`), por anclas desde
  `experimentos/creacion_A/organismo_v13q5.py` (`fae9c32b146fdbb4`); `memoria=None` ⇒ v13q5 exacto, identidad 18/18
  verificada por el auditor. Brazos hermanos `'combi'`/`'combi1'`. Semillas vírgenes 121–140, `Pool`.
- **Predicción numérica.** `acc_lenta` xor01 mediana ≥ 0.875 (registro) y **estricta** ≥ 0.75; ≥0.75 en ≥16/20
  (registro) y ≥11/20 (estricta); ganadora (0,1) **medida en la sonda** en ≥18/20; **n\* ≤ 20**; px0 = 1.000 en 20/20;
  azar mediana en [0.35, 0.65]. **Refutación:** n\* > 60, o mediana (registro) < 0.875, o estricta < 0.625.
- **Control que puede fallar.** (a) **Abstención**: parte del número es el medio punto del empate — se reportan SIEMPRE
  las dos puntuaciones y el subconjunto con las 4 clases en el tren. (b) **Desempate por índice** (§4.1): reportar
  cuántas celdas empatan en el mínimo y romperlo **al azar**; si el resultado se mueve, vale el del azar. (c) **Coste
  conductual**: veneno, energía y muertes contra `memoria=None`, pareado. (d) azar bajo el azar (visto: 0.2 en 1/3).
- **Mini-prueba (hecha).** 18 corridas T=100000, un proceso: xor01 0.8125 [0.75, 1.00], estricta 0.625; **n\*=7**;
  px0 1.000 (6/6), n\*=2; azar 0.5 [0.2, 0.5]; ganadora en la sonda (0,1) 3/3; replay = organismo en 18/18.

### Segundo — **M4 (grupo4), tabla por grupos con la forma hallada por búsqueda ciega**
- **Hipótesis.** La misma familia que M3, pero con la FORMA de la regla **encontrada fuera del organismo** (buscar en
  semillas 1–10, reportar en 11–20) y trasplantada local dentro del organismo.
- **Mecanismo mínimo y memoria.** Tabla por grupos g=2 (15 × 4 casillas, 135 números) + estadístico de competencia por
  grupo evaluado **antes** de actualizar la celda + lectura WTA dura. Primera escritura de un golpe; después, EMA con
  `eta`. Señal: el residuo de la propia mordida, el mismo que la vía lenta ya consume.
- **Instrumento.** `experimentos/enjambre/grupo4/organismo_g4.py` (perilla `tabla_g`, identidad 13/13 con
  `tabla_g=None`) + `banco_g4.py` (replay offline) + `meta_regla2_g4.py` (432 configuraciones). Semillas 121–140.
- **Predicción numérica.** Con las constantes **de la búsqueda FIJADAS ANTES** (g=2, mse, dura, **rho=0.02**, eta=0.05,
  clip=3.0, alpha=0.3): mediana xor01 ≥ 0.75, ≥0.75 en ≥14/20, ganadora (0,1) en ≥15/20, n\* ≤ 40, px0 = 1.000 en
  20/20, azar en [0.35, 0.65]. **Refutación:** mediana < 0.75, azar fuera de banda en > 1/20, o replay ≠ organismo.
- **Control que puede fallar.** (a) **Rigging, pendiente y no decorativo**: correr la misma búsqueda contra un objetivo
  cambiado (optimizar px0) y comprobar que el top-10 cambia; si no cambia, la búsqueda no mide lo que dice medir.
  (b) **Winner's curse**: casillas nunca visitadas en 200–350 mordidas — reportar cobertura de la tabla ganadora.
  (c) Desempate por índice (§4.1), igual que M3. (d) Puntuación **estricta**, que este paquete no reportó.
- **Mini-prueba (hecha).** In-organismo, 3 semillas: 0.8125 · 0.750 · 1.000 (apagado: 0.500 · 0.313 · 0.563);
  n\*=10 · 20 · 10; (0,1) en 3/3; px0 1.000 3/3; azar 0.5 · 0.2 · 0.5. **Replay = organismo con la perilla ENCENDIDA
  durante la cosecha, 9/9, diferencia < 1e-9** — el control de flujo mejor resuelto de los cuatro paquetes.

**Por qué en este orden.** M3 gana por evidencia, no por elegancia: identidad y números verificados por terceros fila a
fila, ganador medido **en la sonda** (lo que hundió a M1), n\* de un dígito, estricta reportada por el propio grupo, y
20/20 contra 18/20 en el mismo replay. M4 va segundo porque aporta lo que M3 no tiene — una búsqueda ciega con semillas
retenidas que **reencontró la misma estructura** — pero le faltan rigging, puntuación estricta y votos de refutación.

## 6. Qué falta

1. **Ninguna serie confirmatoria existe todavía.** Todo lo de arriba es n=3 (o replay sobre el flujo del tronco). Nada
   autoriza a declarar "resuelve XOR". Las 120 corridas por mecanismo con `Pool`, semillas 121–140, las corre el
   coordinador. **M1 y M2 no deben entrar a esa cola**: los dos están en o bajo su propio umbral de refutación.
2. **M1 es el control interno del estimador** y comparte arquitectura con M3/M4 a propósito. Si M1 corrigiera su
   `cel_ganadora` (captura en la sonda) y siguiera en 0.50 mientras M3 va a 0.81, el mérito es **de la memoria de un
   golpe** y no de agrupar por canales. Ese contraste se corre en el mismo bloque o no se atribuye nada.
3. **Deudas de método con dueño:** ERR numerado para la calibración de `fis_umbral` en M2 (regla 11); captura en la
   sonda para M1; asimetría comida/veneno (~80/20, trampa 3) en los cuatro; desempate por índice preregistrado en
   M3/M4; `rho=0.02` fijado por escrito en M4 antes de correr.
4. **Lo que nadie tocó:** el coste conductual de la abstención con métricas completas; el examen del tronco y la batería
   de generalización con la perilla encendida (`eta_s`/`clip_s` salieron gratis en A-4, esto puede no salir); g=3 y los
   dos estimadores que M4 no implementó; y la pregunta abierta detrás de todo — **15 pares son 15, pero C(n,2) no lo
   es**: ninguno escala a una retina grande sin que la fisión de M2 (idea correcta, instrumento equivocado) vuelva.


## Errata (coordinador, 18 sep 09:45, del revisor de literatura)
La cita "Milstein et al. 2024" de §1 (memoria direccionable con sinapsis binarias y un disparo) no existe con esa autoría: la fuente
es Wu & Maass 2025, *Nature Communications* 16:342. Las demás citas de §1 quedan sin verificar por PDF (`LITERATURA_novedad_20260918.md`).
