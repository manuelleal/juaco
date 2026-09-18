# DIAGNÓSTICO — sala 2, lente MÉTODO Y RENDIMIENTO (18 sep 2026, 09:45)

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales, sin backprop en el
runtime, que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada. Primero la frontera;
segundo, que viva.

**Encargo:** 42 ERR en 7 días, cinco bloques por hora esta mañana y ningún candidato al tronco; ¿nos bloquean los
instrumentos, los criterios, el tamaño de los mundos o el paradigma? Qué cambiar del método para que la frontera se mueva,
sin abandonar el preregistro. Y evaluar la hipótesis del director (tokenización / grafo) desde esta lente.

**Reglas que cumplí:** no edité ningún archivo del repo; sólo creé este. No corrí ningún organismo ni `Pool`; sólo leí
JSON/log/código (dos `python -c` de lectura de `datos/v15e_s141-160_20260918_092921.json`). Sin commit. Todo número de
abajo lleva su archivo/entrada.

---

## 0. Resumen en diez líneas

1. La frontera está donde dice `CLAUDE.md` "Estado (día 7)": **v14.1** (feefc88b1fd8d434) con examen 8/8 ×2, G1 1.000 /
   G2 0.97–1.00, capacidad N\* 51, 3T-k 0.237; XOR cerrada por ERR-35 (14 ejemplos → 1.000; 8 → prior de pares, n\* 7–10);
   mundo vivo replicado ×2 (xor necesidad × estímulo 1.0, 20/20); alias de código hallado y reparado (B-5, 18/18).
2. **Cuatro candidatos con dos series cada uno NO han entrado al tronco** (sorpresa en boca dosis 5; B-5 desambiguar;
   A-3 vector único; y la memoria de pares en tres versiones v15c/d/e que no entran por letra). El cuello de "ningún
   candidato" es en primer lugar de **proceso de integración**, no de ciencia.
3. **Esta mañana (07:37–09:37): 11 bloques, 21 series con `Pool`, 8 ERR (35–42), 0 entradas al tronco.** De los 8 ERR,
   **4 son instrumentos copiados por anclas** (36, 38, 41, 42), 3 son medida/criterio (35, 37, 40) y 1 control mal escrito
   (39). **Cero son errores del organismo.** Encontré un quinto de la misma familia (candidato a ERR-43, §2.3).
4. El mundo de 6 px (C(6,3) = 20 patrones; K = 3 de 90) ya no da información: con 8 patrones **9 de 15 hipótesis
   empatan** (A12) y **dos estímulos comparten código en 9 % de semillas con 4 estímulos y en 170/200 semillas con 20
   patrones** (B-5). Identificabilidad y alias son el mismo teorema: el token colisiona.
5. El único canal de aprendizaje es la boca (`R` sólo al morder, −3/+1), y el mundo se come la comida (veneno 6.3× más
   expuesto que la comida). "Aprender sin morder" cae por construcción (A12 ruta 3, C-P5, B-5 lateral, N2 ×2 mundos).
6. La medida que "manda" desde las 05:10 (exposiciones hasta asociar) **no está en ninguna batería del tronco** (V3 "no
   medible" en v15c/d/e).
7. Con 20 semillas, los veredictos caen a ±1 (v15e E1 19/20 y E2I 19/20; B-5 C4 7/9; v14 s117): la regla 12 dispara
   réplicas que consumen el Pool. Los instrumentos nuevos de la mañana no tienen gemelo compilado; el tronco sí (×58–78).
8. **Qué cambiar (sin abandonar el preregistro):** (a) regla de entrada al tronco escrita de antemano; (b) una batería
   parametrizada en vez de copias; (c) batería de exposiciones obligatoria; (d) runner que codifique "lo que mata" vs "lo
   que reporta"; (e) retina de 12 px con ancla a 6 px; (f) 40 semillas para candidatos, 20 para explorar.
9. **Hipótesis del director:** el organismo YA tokeniza (`code(P)` = frozenset de 3 celdas; `ncod` cuenta evidencia por
   token exacto) y ya hace "sal rosa = variable de sal" — de más: es el alias de código, y la reparación B-5 (división
   por `R = 0` bajo retina distinta) es literalmente "sal rosa nace como hija de sal". Lo que NO tiene: aristas explícitas
   entre tokens que no sean celdas compartidas, ni recorrido. La operacionalización local más barata es el **árbol de
   fisión como grafo** (madre → hija ya ocurre; sólo falta anotar la arista y medir la herencia), no un grafo por parecido
   (B-4 lo refutó en el mundo del tronco: el único par parecido es comida/veneno).
10. "Eso es lenguaje" queda como hipótesis prohibida hasta que un token compartido prediga entre dos organismos (N2 cerrado
    ×2; N3d 0.82 es lo más cercano).

---

## 1. Dónde está exactamente la frontera hoy (con números)

| frente | estado medido | fuente |
|---|---|---|
| tronco | **v14.1** = v13 + hija dispersa + puerta por código + `eta_s` 0.15 / `clip_s` 10; examen v3' 8/8 en 121–140 y 141–160 (7/8 en 101–120: s117 caso conocido); G1 1.000 / G2 0.95–1.00 ×3; capacidad N\* 51; 3T-k 0.237 con 53 celdas; gemelo 196/196 + 42/42 | `CLAUDE.md` día 7; `PROPUESTA_v14.md` |
| etapas del brief | 1, 2, 3, 4, 5-N1, 5-N3d cerradas; N2 cerrado con dos mundos (6 diseños; INNATO 60 contra 278); nivel 6 rodeo 2 series; nivel 7 compone hasta 3 (hija dispersa: lift 0.31–0.35 a k = 4/5) | HANDOFF §13 |
| XOR (nivel 3 no lineal) | **cerrada 07:47 por ERR-35**: 14 ejemplos → 1.000 (n\* 200); 11 → 0.625; 8 → 0.500 sin prior (9/15 empatadas; gradiente exacto 0.562; backprop 0.531); 8 con prior de pares (M3) → 1.000/1.000 ×2 series, n\* 7–10 | REGISTRO "LÍNEA XOR CERRADA"; A12–A15 |
| memoria de pares en el tronco | v15c: sin medida válida (ERR-38); v15d: G1 1.000 pero E2 0/20, E1 0/20 (no se desdice); **v15e (09:36): E2 20/20 y E1 W_B≈−3 20/20 — lo que mataba, arreglado — pero xor01 estricta 0.500 (< 0.75) → no entra**; V1 6/8 por la letra (E1 conducta 19/20; E2I W_C 19/20: ambos a ±1) | `v15e_s141-160_20260918_092921`; `examen_v15e_20260918_093053` |
| mundo vivo (línea F) | xor necesidad × estímulo 1.0 (20/20 ×2), tabla 2×4 en 11 exposiciones, muertes 0.72×/0.64× (A₁₂ 0.90–1.00); alias de código confirmado por P10; peldaño 2: la medida de reproducción SE TIRA (P-R1), la tercera necesidad SOBRA (CUELLO_MIN 65.5 > 55) | `vivo_s181-200`, `vivo_s201-220`, `vivo_rep_s221-240` |
| nivel 4 (alias) | B-5: 18/18 ALIAS reparadas (\|W[sal]\| 0.0; veneno −3.0; evitación ×7 → ×1; muertes 75 → 41), tronco IDÉNTICO a v14.1 (examen 8/8, 40/40); **candidato a v15, sin decisión** | `codigo_alias9`, `codigo_replica_alias9` |
| nivel 8 (sorpresa del mundo en la boca) | dosis 5: 0.267× / 0.248× (20/20 ×2), se apaga 20/20, G1 0.80, examen v3'' 8/8; **candidato a v15, sin decisión** | REGISTRO 03:32 y réplica 141–160 |
| candidatos que ya pasaron todo y esperan | sorpresa dosis 5 (2 series), B-5 (2 series), A-3 vector único (identidad 60/60, \|ΔW\| 3e−15) | `PROPUESTA_v14.md`; PUENTE A-3 |

**La frontera, en una frase con números:** un organismo de 90 celdas y 6 px que recuerda 20/20, generaliza lo lineal 1.000,
compone 3 pasos, aprende valor por necesidad en 11 exposiciones y resuelve XOR con 8 ejemplos sólo si trae un prior de pares —
y **tres órganos con dos series cada uno esperando en la puerta del tronco**.

---

## 2. Rendimiento medido: qué produjo la mañana y qué costó

### 2.1 La mañana (07:37 → 09:37), del listado de `datos/`

| hora | bloque | corridas con `Pool` | veredicto | entra al tronco |
|---|---|---|---|---|
| 07:37–07:44 | XOR bloque 3/3 (M3) + réplica | 360 + 360 | ✅ cruza ×2 → prior estructural declarado | no aplica (instrumento `g3A`) |
| 07:50–07:53 | mundo vivo 181–200 | 140 | núcleo ✅; P4′/P6/P7 ✗ (ERR-37) | no aplica |
| 07:58–08:05 | v15c (examen + generalización + serie) | 180 + 40 + 120 | ✗ (V2a inválida: ERR-38) | **no** |
| 08:06–08:07 | mundo vivo réplica 201–220 | 140 | ✅ replica; P10 ✅ | no aplica |
| 08:12–08:14 | bloque de la sal (alias) | 36 | ✅ alias confirmado | no aplica |
| 08:21–08:37 | v15d (examen + generalización + serie) | 180 + 40 + 120 | ✗ V1 (E2 0/20, E1 0/20) | **no** |
| 08:44–08:46 | ERR-38: V2a repetida para v15c y v15d | 40 + 40 | G1 1.000 los dos | — |
| 08:51–09:07 | B-5 desambiguar (humo, examen, generalización, serie) | 180 + 40 + 63 | 8/9; C4 7/9 → réplica | **candidato, sin decisión** |
| 09:11–09:12 | B-5 réplica | 63 | ✅ DECLARADO | ídem |
| 09:14–09:16 | reproducción como medida | 180 | ✗ la medida se tira (P-R1) | no aplica |
| 09:29–09:36 | v15e (identidad, examen, generalización, serie) | 180 + 40 + 120 | ✗ V2b xor01 0.500 | **no** |

**11 bloques, 21 series, ≈ 3 200 corridas de T = 100 000–200 000 en 2 h, 0 entradas al tronco.** El Pool(14) rinde ≈ 140
corridas / 5 min (`vivo_s181-200`) o 63 corridas / 40 s (`codigo_replica`). El cuello no es la CPU.

### 2.2 Los ERR de la mañana, clasificados

| ERR | hora | tipo | ¿del organismo? | coste medido |
|---|---|---|---|---|
| 35 | 07:10 | **criterio** reformulado tras datos (director) | no | 0 corridas; cambió el enunciado de cierre |
| 36 | 06:37 | **runner** no guardó `curva_rec` | no | N6′ no calculable; serie nula para N6 (240 + 240 corridas) |
| 37 a/b/c | 08:10 | **medida** (umbral en la mediana; pareado no válido; `max` sobre 40) | no | tres predicciones "caídas" que no habían caído; enmienda 2 |
| 38 | 08:44 | **instrumento copiado** (defaults del gemelo `eta_s = 0`) | no | dos V2a anuladas (80 corridas) + 80 de repetición; un veredicto falso de v15c durante 38 min |
| 39 | 09:00 | **control** de paja (CUELLO leía una fila) | no | añadió un brazo (20 corridas) |
| 40 | 09:16 | **medida** no ligada a la supervivencia | no | 180 corridas cuya medida principal se tira |
| 41 | 09:30 | **instrumento copiado** (kwargs tipo v13 en V2b) | no | V2b de v15c/v15d no comparables con el tronco |
| 42 | 09:35 | **instrumento copiado** (ruta del sha) | no | JSON de examen de v15c/v15d perdido |

**8 ERR en 2 h 25 min; 4 de instrumento copiado, 3 de medida/criterio, 1 de control; 0 del organismo.** Contando la
historia (`CLAUDE.md`: "diez de diez anomalías del proyecto han sido del instrumento"), la tasa de error de instrumento no
ha bajado con la experiencia: ha subido con el número de copias.

### 2.3 Hallazgo de lectura de esta sala (candidato a ERR-43; NO corrí nada)

`experimentos/creacion_A/corre_v15e.py`, línea 199:
```
g1az = num(r"G1 valor[^\n]*azar ([0-9.]+)", txt3)
```
Sobre la línea de la batería `PASA  G1 valor en patrones nunca vistos: px0 1.000 (>=0.65), azar 0.450, px0>azar 20/20`, el
`[^\n]*` es voraz y el `azar` que casa es el último: captura **`20`** (de `px0>azar 20/20`), no `0.450`. La línea 203 exige
`0.35 <= g1az <= 0.65` → **`V['V2a'] = False`** aunque la batería dijo PASA (G1 1.000, G2 0.997, K 20/20, azar 0.450 en
banda). El log lo delata: `V2a G1 1.000 >= .80 (azar 20.000) … NO`. El JSON guarda `'V2a': False` con `'V2a_G1': 1.0`.
No cambia el veredicto final de v15e (V2b xor01 0.500 lo tumba solo y la cláusula §7 es "o"), pero **es el tercer defecto de
runner copiado en `creacion_A/` en una hora** (ERR-41, ERR-42, éste) y **el veredicto del runner contradice al de la batería
sin que nadie lo compare**. Regla derivada propuesta (§6, cambio 4): el runner que resume una batería copia el veredicto
booleano de la batería, no lo recalcula con regex; y toda serie compara los dos y aborta si difieren.

### 2.4 Relectura de v15e por la letra de su propio preregistro

`PREREGISTRO_v15e.md` §5: *"Lo que mata al candidato, explícito: E1 'W_B ≈ −3' y E2 reversión … Un 19/20 en el umbral dispara
la regla 12 (réplica en rango nuevo), no una enmienda."* Medido (`examen_v15e_20260918_093053.log`): **E1 W_B≈−3 20/20; E2
reversión 20/20 (las tres); E1 conducta `venenoQ4<Q1` 19/20; E2I `W_C≤−2.5` 19/20.** Es decir: lo que mataba, PASA; lo que
falla está a ±1 semilla en dos subcriterios → por la letra del preregistro, **V1 está en "réplica automática", no en
"cae"**. El runner aplicó 8/8 plano. Y V2b (xor01 0.500 estricta, gana (0,1) 20/20 pero la lectura es residuo + lineal) sí
cae limpio, como A predijo tras el humo. Lo que v15e deja medido y que NO estaba: *la tabla reescribible sin doble cuenta se
desdice en una mordida y la rápida consolida igual que v14.1* (E2 20/20, mordidas de B por trimestre [15, 20, 82, 95]).
El siguiente (v15f, A16: R crudo + sobrescritura + relevo) está propuesto y no construido.

---

## 3. Los bloqueos, ordenados por importancia

### Bloqueo 1 — El mundo de 6 px ya no puede hacer la pregunta siguiente (información, no mecanismo)

- **Evidencia.** (a) A12: con 8 patrones de entrenamiento, **9 de 15** rasgos conjuntivos ajustan con residuo 0 y sólo 1
  generaliza; gradiente exacto 0.562, backprop 0.531, estadístico ideal 3/20 — "con 8 no lo aprende nadie". Con 14, 1 de 15.
  (b) B-5 `negativo_codigo.py` (semillas 1–200, sin simular): con 4 estímulos y K = 3 de 90, algún par comparte código en
  **18/200** semillas (9 %); en el mundo de regla (20 patrones) **170/200** semillas tienen un par idéntico y **135/200** un
  patrón de test que lee exactamente la celda de uno de tren (291 fugas, 115 de valencia opuesta) → parte de lo que
  `bateria_generaliza` mide es alias. (c) B-4: la similitud del código Kenyon por píxeles compartidos (0/1/2 de 3) es
  **0.000 / 0.000 / 0.333** — no ordena vecinos; el código HD (n = 2000, k = 40) sí: 0.025 / 0.075 / 0.225. (d) HANDOFF
  §15.8.7: "el cuello que más importa a la misión (construir el rasgo desde píxeles, sin prior) sigue sin mecanismo".
  (e) El propio registro ya llama a esto "teorema de la retina de 6 px" (C-P6, 06:48).
- **Por qué bloquea.** Los dos resultados de la mañana que más pesan (XOR sólo con prior; alias) son **la misma
  propiedad del mundo**: C(6,3) = 20 patrones con 3 píxeles activos no separan hipótesis ni códigos. Cualquier órgano nuevo
  para "construir el rasgo" se va a medir en un mundo donde la respuesta correcta es indistinguible de ocho incorrectas; y
  cualquier órgano de memoria se va a medir con tokens que colisionan al 9 %. El siguiente peldaño no cabe en la pregunta.
- **Qué lo desbloquearía.** Un instrumento de retina mayor por anclas (p. ej. 12 px con peso 4: C(12,4) = 495 patrones; o
  8 px peso 3: 56), con NK/K escalados para que la tasa de alias caiga < 1 % (calculable con `negativo_codigo.py` antes de
  simular), y **ancla**: con 6 px y las constantes actuales debe ser v14.1 bit a bit (el rng de `KW` cambia de forma; la
  identidad se conserva sólo con un `Generator` aparte para las columnas nuevas, como en `v13s`/`organismo_vivo`). Los
  mundos de regla se redefinen sobre esa retina (px0, xor01, azar) y se declara que **los umbrales 0.75/0.80 se
  recalibran una sola vez, antes de correr nada, sobre v14.1 en 20 semillas** (regla 3: criterio nuevo escrito antes).
- **Coste.** Un diseñador (constructor + arnés + negativo): 2–3 h. Re-línea base de v14.1 en la retina nueva: 3 mundos ×
  20 semillas × 200 000 = 120 corridas ≈ 5 min de Pool. Riesgo: todas las cifras históricas quedan a 6 px; se comparan
  sólo entre sí.

### Bloqueo 2 — La boca es el único canal de aprendizaje: "aprender sin morder" cae por construcción

- **Evidencia.** `organismo_v14.py`: `Wp/Wn/Wps/Wns` sólo cambian dentro de `if mordio:`; `R ∈ {+1, −3}`. A12 ruta 3: "sin
  morder no hay `R`, luego no hay residuo; antes de la sonda los otros 12 patrones no existen en el mundo". C-P5 refutada en
  mini-prueba; B-5 lateral (05:55) "la vía lenta asocia en 2 exposiciones en vez de 4.5 pero también en azar"; N2 cerrado
  con dos mundos; C-P6 nulo (el mundo se aprende solo, SOLO_R 0.986). Trampa 3 medida: exposiciones A 831 / B 5253 / C 843 /
  D 2017 (el veneno se encuentra **6.3×** más que la comida: lo rechazado se queda, lo mordido desaparece). PLAN (3):
  "5 740 encuentros con veneno `00` por corrida donde hoy no se aprende nada".
- **Por qué bloquea.** La medida que manda (exposiciones hasta asociar) tiene un suelo duro: **no puede bajar de "una
  mordida por estímulo"** mientras la única señal sea `R` al morder. Todo lo que se ha llamado "aprender sin morder" ha
  sido un cambio de política (probar antes) o de estimador (escribir de un golpe), no un canal nuevo. Es el bloqueo
  de paradigma real, y es más pequeño de lo que suena: no es "abandonar reglas locales", es **darle al organismo una
  segunda consecuencia observable que no sea comer**.
- **Qué lo desbloquearía.** Tres candidatos, todos con regla local y ancla: (i) **consecuencia de acercarse** (olor/gradiente:
  a distancia d del objeto la retina recibe una señal proporcional que ya predice ΔS; el predictor de ΔE del bloque 6
  existe y "salta al cambio 10/10"); (ii) **la conducta ajena como señal** (N3d 0.82 ya funciona: receptor ciego aprende
  del que ve; es el único "sin morder" medido que cruza); (iii) mundo que **no se come la comida** (`regen` en sitio,
  ya construido en `mundo_social_n3`), para equilibrar exposiciones. El criterio nuevo se escribe antes: exposiciones
  hasta asociar de un estímulo nuevo con 0 mordidas propias ≤ k, control barajado en banda.
- **Coste.** Diseño (1 diseñador, 3–4 h) + bloque de 20 semillas (5 min). Riesgo alto: es el frente donde cayeron
  C-P5, C-P6, N2 ×6; por eso va con ancla y con el mundo, no con un órgano nuevo sobre el mundo viejo.

### Bloqueo 3 — No hay regla de entrada al tronco: los candidatos se acumulan y cada uno vuelve a copiar todo

- **Evidencia.** Esperando decisión: sorpresa dosis 5 (0.267× / 0.248×, 20/20 ×2, G1 0.80, examen 8/8), B-5 (18/18, tronco
  idéntico 8/8 + 40/40), A-3 (identidad algebraica 60/60). `CLAUDE.md`: "la entrada la decide el director" ×3. Mientras
  tanto, cada candidato nuevo se construye por anclas **desde v14.1**, no desde el último candidato aceptado: v15c, v15d,
  v15e y B-5 generaron **4 organismos + 4 gemelos + 4 baterías de examen + 4 de generalización + 4 runners + 4 arneses**
  (≈ 24 archivos copiados en 1 h 30), y de esas copias salieron ERR-38, 41, 42 y el candidato a 43.
- **Por qué bloquea.** "Ningún candidato al tronco" es literal pero engañoso: hay tres que cumplen la letra de la propuesta
  v14 (examen + baterías + réplica). Sin regla de entrada, (a) el director es el paso serial de todo el frente, (b) los
  candidatos no se componen (la composición de v14 fue lo que produjo un tronco), (c) la deuda de copias crece con cada
  candidato y con ella la tasa de ERR de instrumento.
- **Qué lo desbloquearía.** Una **regla de entrada preregistrada** (una línea en `PLAN.md`, decisión del director una
  sola vez): *"un órgano con dos series independientes, examen v3'' 8/8, `bateria_generaliza` intacta e identidad con la
  perilla apagada entra al tronco como perilla APAGADA por defecto (tronco extendido vN.x); la composición de perillas
  encendidas se examina como se hizo para v14"*. Con eso B-5 y la sorpresa dosis 5 entran hoy sin tocar ninguna cifra de
  v14.1 (identidad exacta medida), y el siguiente candidato copia desde v15, no desde v14.1.
- **Coste.** 0 corridas para B-5 (T1/T2 son identidad exacta). Composición sorpresa + B-5 + hija + puerta: un examen
  (180 corridas, 3 min) + generalización (40, 45 s) + réplica en rango virgen (181–200 está usado por vivo; 261–280 libre).

### Bloqueo 4 — Instrumentos copiados por anclas: la tasa de ERR de instrumento supera la de hallazgos

- **Evidencia.** §2.2 y §2.3: de 8 ERR de la mañana, 4 (+1) son copias con defaults distintos, kwargs incompletos, rutas
  mal copiadas o regex de runner. ERR-38 sostuvo un veredicto falso ("v15c rompe la generalización") durante 38 min y
  costó 160 corridas. ERR-28 (madrugada) es el mismo patrón (`experimentos/v13_dos_vias/organismo_v13.py` ≠ tronco).
  `bateria_generaliza.py` ya tiene la solución a medias: un dict `INSTRUMENTOS` con kwargs explícitos por módulo.
- **Por qué bloquea.** Cada copia es una fuente de un ERR a ~1 h de trabajo; y cada ERR obliga a repetir series válidas.
  Además, los instrumentos nuevos de la mañana (`organismo_g3A`, `organismo_vivo`, `organismo_v15c/d/e`,
  `organismo_v14_codigo`) **no tienen gemelo compilado** (HANDOFF §15.8.6), así que cada réplica cuesta minutos donde el
  tronco cuesta segundos (×58–78).
- **Qué lo desbloquearía.** (a) **Una batería parametrizada** en `organismo/`: `bateria_v14.py --modulo X --kwargs-de
  organismo_v14` (y lo mismo para generalización), donde el candidato es una ruta y los kwargs se leen de UN dict
  compartido (`INSTRUMENTOS`) — cero copias de baterías; (b) el runner copia el booleano de la batería (no regex) y
  compara veredictos (aborta si difieren); (c) el humo obligatorio (regla 14) incluye "escribe JSON" **y** "veredicto del
  runner == veredicto de la batería"; (d) un gemelo compilado por familia de candidatos (la familia v15 comparte el 95 %
  del código con v14; el compilador ya hizo 6 gemelos).
- **Coste.** 2–3 h de un implementador, cero ciencia; recupera, por lo medido hoy, ≈ 1 h de cada 2 h de sesión.

### Bloqueo 5 — La medida que manda (exposiciones hasta asociar) no está instrumentada en el tronco

- **Evidencia.** PLAN 05:10 (B): "la medida que manda pasa a ser cuántas exposiciones hacen falta … todo bloque reporta
  exposiciones-hasta-criterio". Medido: v15c/v15d/v15e "**V3 `n*`: no medible con los instrumentos de hoy**"
  (`PREREGISTRO_v15e.md` §5). Sólo la sala XOR (n\* 7–10 contra 200 contra > 600), B-4 (`exp_hasta` 16 contra 8) y el
  mundo vivo (`exp_tabla` 11) la reportan, cada uno con su propia definición. `bateria_v14.py` y `bateria_generaliza.py`
  no la llevan.
- **Por qué bloquea.** Es ERR-20 otra vez: **una medida que no está en una batería no protege nada ni ordena nada**. Sin
  ella, un candidato que asocia en 1 exposición y otro que asocia en 16 pasan el mismo examen 8/8, y el frente único
  ("la repetición es el enemigo") no tiene número con el que decidir.
- **Qué lo desbloquearía.** `bateria_exposiciones.py` (una definición: mordidas/llegadas de un estímulo nuevo hasta que el
  valor que usa la boca queda a ≤ 0.5 del real, la de B-4, ya implementada como `exp_hasta`), tres escenarios (nuevo
  veneno, nuevo comida parecida al veneno, inversión), 20 semillas, umbral escrito una vez sobre v14.1 (hoy 16 / 8 / ~2 000
  pasos) y obligatoria en la regla 1 antes de congelar.
- **Coste.** 1–2 h; con gemelo, 1 min por candidato.

### Bloqueo 6 — 20 semillas dan veredictos a ±1 y las réplicas comen el Pool; los criterios mezclan "lo que mata" con "lo que reporta"

- **Evidencia.** A ±1 del umbral hoy: v15e E1 conducta 19/20 y E2I 19/20; B-5 C4 7/9 (y 4/9 en la réplica: criterio de
  causa mal escrito); v14 examen 7/8 por s117; C-P6 N6 14/20; N1 19/20 → 13/20 entre rangos. ERR-37a: un umbral pareado en
  la mediana del efecto da ~10/20 midas lo que midas. Regla 12 ya dice: "efectos < 0.05 sólo con 40 semillas". Rendimiento:
  140 corridas / 5 min → 40 semillas × 7 brazos = 280 corridas ≈ 10 min con el instrumento en Python; segundos con gemelo.
- **Por qué bloquea.** Cada ±1 dispara una réplica (regla 12) que ocupa el Pool que necesitaría el siguiente bloque; y
  cuando la letra pone diez subcriterios en pie de igualdad, un candidato que arregla lo que mataba (v15e: E1 W_B y E2
  reversión 20/20) aparece como "cae V1" por un subcriterio de conducta a 19/20.
- **Qué lo desbloquearía.** (a) 40 semillas para todo lo que aspire al tronco, 20 para explorar (ya está en la regla 12;
  falta aplicarlo por defecto en los runners); (b) el preregistro declara **dos listas**: "lo que mata" (falla → no entra)
  y "lo que reporta" (falla a ±1 → réplica, falla franca → coste), y el runner las codifica así (v15e ya lo escribió en §5;
  su runner no lo aplicó); (c) ningún umbral pareado se pone en la mediana observada de un humo (ERR-37a como regla).
- **Coste.** ×2 tiempo de pared por serie (10 min en vez de 5); menos réplicas; gemelos lo devuelven con creces.

---

## 4. Respuesta directa a la pregunta del encargo

| ¿nos bloquea…? | veredicto | número que lo sostiene |
|---|---|---|
| **los instrumentos** | **sí, en rendimiento** (no en verdad: ningún error entró al tronco; todos se cazaron) | 4 de 8 ERR de la mañana + 1 hallado aquí; ERR-38 costó 160 corridas y 38 min de veredicto falso |
| **los criterios** | **a medias**: no bloquean la verdad, bloquean la lectura (letra plana de 8/8; umbrales en la mediana) | v15e: lo que mataba 20/20, "cae" por 19/20 en otro subcriterio; ERR-37a 11/20 y 10/20 |
| **el tamaño del mundo** | **sí, y es el principal**: identificabilidad y alias son el mismo teorema de 6 px | 9/15 hipótesis empatadas con 8 patrones; alias 9 % (4 estímulos) y 170/200 (20 patrones); Kenyon no ordena vecinos (0/0/0.333) |
| **el paradigma** | **sí, en un punto preciso y pequeño**: un solo canal de aprendizaje (la boca) y un mundo que se come la comida; no "las reglas locales" | 5 740 encuentros con veneno sin aprender nada por corrida; exposiciones B 6.3× A; todo "sin morder" cae (C-P5, C-P6, N2 ×6) |

---

## 5. La hipótesis del director, desde esta lente

**Texto (09:40):** "la tokenización y la representación de algo: si sal es sal será número uno, lo guardo, lo vectoriza;
después sal rosa lo vectoriza, marca como sal y lo plantea como una variable de lo mismo — eso es lenguaje. Y aprende y
desaprende." **(05:10/05:25):** "la palabra es grafo, no vectorización".

### 5.1 Lo que el organismo YA hace (medido, con la línea de código)

| pieza de la hipótesis | dónde está en v14.1 | medida |
|---|---|---|
| "sal es sal → número uno, lo guardo" (**token**) | `code(P)` = top-3 de `KW@P` → `_key(_k)` = `frozenset` de 3 celdas; `ncod[_ky]` cuenta las mordidas de ese token EXACTO; `_ord` guarda el orden de aparición | puerta por código (PATC): familiar si `ncod ≥ 5` y ≥ 1 celda consolidada; N\* 50.5 contra 35 (B-2) |
| "lo vectoriza" (**vector**) | dos vectores a la vez: el código disperso (90 celdas) y la lectura lineal de la retina (`Wps−Wns ∈ ℝ⁶`) | G1 1.000 / G2 0.97 (la vía lenta generaliza lo lineal) |
| "sal rosa → marca como sal, variable de lo mismo" (**herencia por parecido**) | ocurre **sola y de más**: si `code(sal rosa) = code(sal)` hereda TODO el valor (alias) | bloque de la sal: \|W[sal]\| 1.45 heredado del veneno −1.45; evitación ×7; "cuando dos cosas se parecen tanto que reciben el mismo código, el organismo teme a las dos a medias" |
| "variable de lo mismo" hecha bien (**sub-token**) | **B-5**: una celda consolidada que recibe `R = 0` bajo retina distinta **divide**: la hija nace ciega fuera del patrón nuevo (y con `mask_rel` ciega a lo irrelevante), sin valor; la madre conserva el suyo | 18/18: sal 0.0, veneno −3.0, muertes a la mitad; tronco idéntico. **Es literalmente "sal rosa nace como hija de sal"** |
| "aprende y desaprende" | E2 inversión (20/20 en v14.1), extinción, división por conflicto de signo (fisión del valor: la hija se lleva el signo nuevo) | v15d muestra el negativo: una tabla de un golpe **no se desdice** (E2 0/20); v15e lo arregla (E2 20/20) y pierde XOR |
| "tokenizar la combinación" | M3: 15 celdas (una por par) × 4 casillas (una por combinación): un token por (par, combo) | **el único mecanismo que cruzó XOR con 8 ejemplos** (1.000 ×2, n\* 7–10) — y es exactamente "guardar la combinación como cosa" |

**Conclusión honesta:** la intuición del director ya produjo el resultado más fuerte de la noche (M3 = tokenizar la
combinación) y el hallazgo más limpio de la mañana (alias = "sal rosa marcada como sal" sin control). El organismo es un
tokenizador con herencia por colisión; lo que le falta no es tokenizar, es **gobernar la herencia**.

### 5.2 Lo que NO hace

1. **No tiene aristas explícitas.** La única relación entre tokens es "comparten celdas" (o comparten píxeles en la
   lenta). No hay "sal rosa → sal" como arista consultable: la hija hereda en el instante de nacer y después son dos
   tokens sin vínculo (salvo `split_t = (t, kk)`, que guarda el patrón y no la pareja madre → hija).
2. **No recorre.** Ningún valor se calcula "yendo" de un nodo a otro; el valor es una suma sobre celdas activas.
3. **No liga variables.** "Sal rosa" no se representa como `sal ⊗ rosa` (binding); es otro token. La composición medida
   es temporal (3T-k hasta 3 pasos), no de rasgos.
4. **El parecido no es una arista fiable en este mundo** (B-4, medido): con 4 patrones de peso 3 en 6 px, "el único par lo
   bastante parecido para heredar (sim 0.225) es un par comida/veneno" → heredar por parecido **empeora** (8 → 11–13
   exposiciones) y el grafo con fiabilidad no aprende a tiempo (2–3 episodios por patrón: "la señal que enseñaría al grafo
   es más rara que el problema que debe arreglar"). El código del tronco **no puede ordenar vecinos** (sim 0/0/0.333); el
   HD sí (0.025/0.075/0.225). Esto favorece al director en "grafo, no vectorización" — pero con aristas de **causa**, no
   de distancia.
5. **"Eso es lenguaje"**: prohibido por la regla 8 y EQUIPO 6 hasta medirlo. Lo medible es "un token compartido entre dos
   organismos predice lo que el otro va a sentir": N2 cerrado ×2 mundos (convención sin magnitud), N3d 0.82 (conducta
   ajena informa), C-P6 nulo por el instrumento. No hay hoy un mundo donde se pueda decidir.

### 5.3 Cómo se operacionalizaría con reglas locales (sin abandonar el preregistro)

**G-1. El árbol de fisión ES el grafo (memoria nueva: una lista de aristas; rng intacto).** Cada división (por conflicto
de signo, v11; por `R = 0` bajo retina distinta, B-5) crea la arista `madre → hija` con etiqueta {signo, t, patrón}. Nodo =
código exacto (ya existe como `frozenset`); atributos = `ncod`, valor por celda, `mu`, `mup/mun`. Es lectura pura sobre lo
que ya pasa: **identidad bit a bit garantizada por construcción**. Primer bloque (sólo lectura, 20 semillas, 5 min): medir
en el mundo vivo y en el de regla cuántos tokens tiene el organismo al final, qué fracción del valor de un token nuevo
viene de su madre en la primera mordida, y cuántas mordidas tarda en "desligarse" (v15e mide algo parecido: la lenta se
desdice en una). Predicción a escribir: en las semillas ALIAS con B-5 encendido la sal es hija del veneno en 18/18 y hereda
0.0 (por diseño); en LIMPIAS no hay arista. Es un instrumento, no un órgano: no declara nada.

**G-2. Herencia gobernada por la arista (órgano; la pregunta de B-4 que decide, no corrida).** En la primera mordida de un
token nuevo, préstamo `v0` desde el vecino por **causa** (arista de fisión o co-ocurrencia en el mismo sitio), no por
parecido; una mordida contraria desliga (B-4 lo midió: `n_des = 1`, 3/3). Mundo: el de regla, donde con `px0` el parecido
predice el valor y con `azar` no — el contraste ON/OFF en el mismo instrumento es el control que puede fallar (B-4 lo dejó
preregistrable). Predicción de B: `exp_hasta ≤ 3` contra ≥ 10 con px0; sin ganancia con azar. Coste: 120 corridas.

**G-3. Token de combinación reescribible con relevo (v15f, A16; propuesto, no construido).** Es la versión que junta lo
que sí funcionó: la casilla guarda `R` crudo (identificabilidad de M3), se sobrescribe (se desdice en una, v15e) y la
lineal sólo entra por abstención. Predicción de A: xor01 estricta 0.80–0.88, E1/E2 como v15e. **Escala: C(n,2) no
escala** (ENJAMBRE §6.4) — con 12 px son 66 pares; hay que decidirlo antes de la retina nueva.

**G-4. Lo que la hipótesis exige del mundo (y por qué va después del bloqueo 1).** Para que "sal rosa" exista hace falta
que el mundo tenga *sal rosa*: un estímulo que comparta parte del código con otro y difiera en una consecuencia. Con 6 px
eso es o alias total (mismo código) o nada (sim 0): **no hay grados**. La retina de 12 px (bloqueo 1) es la condición para
que el grafo tenga algo que ligar; el HD (n = 2000, k = 40) de B-4 es la otra vía y cuesta `nh·6` flotantes.

**G-5. Lo que NO se haría.** Un grafo por similitud de vectores (refutado en el mundo del tronco); nodos "conceptuales"
sin celda detrás (no hay regla local que los escriba); y declarar "lenguaje" o "concepto" con cualquier resultado de
un solo organismo.

---

## 6. Qué cambiar del método para que la frontera se mueva (orden propuesto, sin abandonar el preregistro)

| # | cambio | qué desbloquea | coste | quién |
|---|---|---|---|---|
| 1 | **Regla de entrada al tronco escrita una vez** (perilla apagada por defecto tras dos series + examen + baterías + identidad) → B-5 y sorpresa dosis 5 entran como v15; el siguiente candidato copia desde v15 | bloqueo 3 | 0 corridas + 1 examen de composición (3 min) | director (una decisión), coordinador |
| 2 | **Batería parametrizada en `organismo/`** (`--modulo`, kwargs desde `INSTRUMENTOS`), runner que copia el booleano de la batería y aborta si difieren; humo hasta JSON + comparación de veredictos | bloqueo 4 (y el candidato a ERR-43) | 2–3 h de implementador | implementador |
| 3 | **`bateria_exposiciones.py`** obligatoria en la regla 1 (definición única de `exp_hasta`; tres escenarios; umbral fijado sobre v14.1 antes de correr) | bloqueo 5 | 1–2 h; 1 min por candidato con gemelo | diseñador + coordinador |
| 4 | **Preregistros con dos listas** ("lo que mata" / "lo que reporta") codificadas en el runner; umbrales pareados nunca en la mediana observada (ERR-37a como regla); 40 semillas por defecto para candidatos al tronco | bloqueo 6 | ×2 pared por serie; menos réplicas | coordinador |
| 5 | **Gemelo compilado por familia de candidatos** (v15x comparte el 95 % con v14) | bloqueos 4 y 6 | 1 compilador, 1–2 h por familia | compilador |
| 6 | **Retina de 12 px por anclas** (ancla a 6 px = v14.1 bit a bit; tasa de alias calculada antes de simular; umbrales recalibrados UNA vez sobre v14.1 antes de correr) | bloqueo 1 | 2–3 h + 120 corridas | diseñador |
| 7 | **Segundo canal de consecuencia** (acercarse / conducta ajena / mundo que no se come la comida), con ancla y control barajado; criterio de exposiciones con 0 mordidas propias | bloqueo 2 | 3–4 h de diseño + 5 min de Pool; riesgo alto | creador C + diseñador |
| 8 | **Grafo = árbol de fisión** como instrumento de sólo lectura (G-1) y la pregunta decisoria de B-4 en el mundo de regla (G-2) | hipótesis del director | 5 + 2 min de Pool | creador B |

Los cambios 1–5 son de método puro y **no cuestan una sola corrida científica**; con lo medido hoy devuelven ≈ la mitad
del tiempo de sesión (ERR de instrumento + réplicas + veredictos falsos). Los cambios 6–8 son los que mueven la frontera
y **dependen** de 1–5 para no repetir la mañana con una retina más grande.

---

## 7. Límites de este diagnóstico

- No corrí nada: todo es lectura de registro, preregistros, logs y JSON de la mañana y del código congelado de v14.1.
- "Cinco bloques por hora" lo verifico como 11 bloques / 21 series en 2 h (§2.1). "42 ERR en 7 días" lo verifico como
  ERR-03 … ERR-42 numerados en el registro (ERR-01/02/04 con otro formato).
- El encargo dice "16 patrones": el mundo de regla tiene **C(6,3) = 20** (`organismo_v14g.patrones_regla`), 8 de tren y 12
  de test en xor01; `LITERATURA_novedad_20260918.md` §0 dice "8 de 16" y es un desliz de ese informe.
- El candidato a ERR-43 (§2.3) lo verifiqué leyendo la línea 199 del runner y el JSON (`'V2a': False` con `'V2a_G1': 1.0`);
  no cambia ningún veredicto vigente. Lo numera el coordinador.
- Las estimaciones de coste (horas) son juicio; las de corridas y minutos salen de los logs de hoy (140 corridas / 5 min;
  63 / 40 s; 180 / 3 min; 40 / 45 s).
