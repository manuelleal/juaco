# EXPLORATORIO, no es dato

# HALLAZGOS — comité de exploración, EXPLORADOR A: TRASPLANTES sobre v14.3 en la pista (25-sep-2026, 13:15–14:55)

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).

**Veredicto: NO.** Ninguna pieza ganadora, sola ni en combinación, puesta a mano y fija sobre v14.3, acerca el R0 real a 0.90. Lo mejor,
**patas** (ir a lo que le sirve a la necesidad activa en vez de a lo más cercano), da 0.663 contra 0.596 de v14.3 en 10 semillas pareadas
(gana 7/10, dif +0.13), pero sin dosis-respuesta (el doble de dosis da 0.60; sólo la fila activa da 0.58): huele a ruido. O1 sigue en 0.947.
**La regla de parada (≥ 0.85 en ≥ 3/5) no la cumple nadie.** Predicción P11 firmada (p 0.70) se cumple.

**El dato que ordena todo:** en los 21 brazos, el fundador limpio muere igual: vida mediana 43–68 pasos, 98.2–99.1 % sin parir, de sal o
veneno. Y ENSEÑA (el hijo nace con todo lo que sabía el padre) **no cambia** ni la vida del hijo (1400) ni su fracción sin parir (0.47–0.53).
El hijo de v14.3 no muere de ignorancia. El de O1 vive 3271 y deja 2.3 hijos (66 % deja ≥ 1); el de v14.3 deja 1.6 (48 %).

## 1. Qué probé y cómo (todo en `comite/trasplantes/`, sólo copias; motores importados en solo lectura)
- **Pista:** `organelos/cruce/motor_cruce.py` (== `carrera_escuderias/pista.py` bit a bit), 9 carros iguales, L 360, 36 objetos,
  T 100 000, **fundador limpio** (ENMIENDA 5), `juez.resumen_linaje` (sólo física). Métrica: R0 real por linaje-semilla, `cruza_real`,
  persistencia. Medida principal: mediana por semilla de los 9 linajes; mediana sobre semillas.
- **Carro:** `carros/TRASP.py`, construido por anclas (`construye_trasp.py`) desde `cruce/carros/CRUCE.py` (v14.3 + 36 genes de cableado
  señal→boca/patas/parto, que nacen en 0). Agregué la perilla `ENSENA` (0 nada; 1 el hijo nace con las dos filas lentas del padre; 2 con
  todo el cerebro aprendido). **Identidad:** con ENSENA 0 y genoma 0 es V143 en la pista bit a bit (física, `_carrera` y rng del mundo,
  s 33001, T 2000). Los genes se ponen a mano, fijos (p_mut 0, sin banco); el fundador limpio nace con el genotipo del linaje.
- **Genes fuera del rango evolutivo [−4, 4]** (el motor no recorta `genomas_ini`): declarado. La escala del logit de la boca es Vb/0.3 con
  Vb = 1.2·valor + 2·hambre + 0.5 (≈ +4 sobre lo desconocido a E 0.6; ≈ +7 a E 0.2), así que hacen falta desplazamientos de 4 a 20.
- **Semillas** 33001–33005 (todos los brazos), 33006–33010 (v143 y patas). 115 corridas, un proceso cada una, ≤ 6 a la vez, sin Pool,
  ~110–170 s cada una. `corre_trasp.py` (una corrida), `lanza.py` (cola), `lee_trasp.py` (tablas). Crudos en `datos/*.json`.

## 2. Tabla por combinación (mediana sobre semillas de la mediana por semilla del R0 real; pareado con la MISMA semilla)
Columnas: sem>=.85 = semillas con mediana ≥ 0.85 · cruzan = linajes con `cruza_real` · sem may = semillas con mayoría de linajes que cruzan ·
fund/hijos = cuerpos muertos: n / vida mediana / fracción sin parir (/ hijos por hijo).

| brazo | qué es | sem | R0 real med | por semilla | sem>=.85 | cruzan | sem may | persist | vida | fund | fund: n/vida/sin parir | hijos: n/vida/sin parir | vs v143 gana/dif | vs o1 gana/dif |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **o1** | techo (política escrita por un LLM) | 5 | **0.947** | 0.957, 0.952, 0.90, 0.947, 0.947 | 5/5 | 35/45 | 5/5 | 37/45 | 3283 | 0 | 1261/200/0.96 | 761/3271/0.335 | 5/5 +0.305 | – |
| o1genes | O1 escrito en genes (margen+limpia+neofobia+patas) | 5 | 0.768 | 0.943, 0.458, 0.768, 0.786, 0.524 | 1/5 | 14/45 | 1/5 | 27/45 | 600 | 7 | 7390/68/0.986 | 1072/1475/0.476 | 3/5 +0.094 | 0/5 −0.161 |
| patas_neof | patas + neofobia | 5 | 0.735 | 0.776, 0.735, 0.425, 0.59, 0.833 | 0/5 | 12/45 | 0/5 | 29/45 | 600 | 14 | 7985/47/0.986 | 1184/1307/0.502 | 4/5 +0.089 | 0/5 −0.217 |
| neof_fuerte | PRUEBA de O1 con dosis real (sesgo −20, reserva +60) | 5 | 0.714 | 0.587, 0.714, 0.722, 0.745, 0.667 | 0/5 | 18/45 | 0/5 | 29/45 | 1105 | 12 | 8293/47/0.988 | 1116/1401/0.487 | 3/5 +0.048 | 0/5 −0.238 |
| ensena2 | el hijo nace con TODO el cerebro del padre | 5 | 0.675 | 0.447, 0.675, 0.676, 0.585, 0.735 | 0/5 | 10/45 | 0/5 | 30/45 | 600 | 17 | 7965/43/0.989 | 1265/1400/0.474 | 3/5 +0.002 | 0/5 −0.277 |
| patas_limpia | patas + limpieza costeable | 5 | 0.667 | 0.667, 0.733, 0.429, 0.842, 0.492 | 0/5 | 10/45 | 0/5 | 30/45 | 600 | 16 | 7202/68/0.984 | 1089/1400/0.517 | 3/5 +0.017 | 0/5 −0.29 |
| **patas** | pata_act_sesgo +2, pata_otra_sesgo +1 | **10** | **0.663** | 0.795, 0.854, 0.784, 0.696, 0.594, 0.667, 0.636, 0.658, 0.652, 0.424 | 1/10 | 29/90 | 0/10 | 59/90 | 600 | 12 | 15795/46/0.987 | 2423/1400/0.504 | **7/10 +0.129** | 0/5 −0.162 |
| limpia | boca_malo_sesgo −6, boca_malo_otra +8 (O1 costeable) | 5 | 0.656 | 0.656, 0.756, 0.508, 0.727, 0.267 | 0/5 | 12/45 | 0/5 | 27/45 | 600 | 15 | 7585/65/0.983 | 1017/1495/0.48 | 3/5 +0.006 | 0/5 −0.301 |
| ens2_patas | ENSEÑA 2 + patas | 5 | 0.652 | 0.652, 0.867, 0.565, 0.694, 0.561 | 1/5 | 12/45 | 0/5 | 32/45 | 723 | 15 | 7760/46/0.99 | 1183/1519/0.44 | 3/5 +0.002 | 0/5 −0.305 |
| patas_margen | patas + MARGEN | 5 | 0.634 | 0.545, 0.804, 0.634, 0.615, 0.783 | 0/5 | 11/45 | 0/5 | 31/45 | 600 | 11 | 8082/47/0.988 | 1142/1397/0.483 | 3/5 +0.039 | 0/5 −0.266 |
| patas_malosuave | patas + malo −4/otra +4 | 5 | 0.619 | 0.338, 0.778, 0.345, 0.842, 0.619 | 0/5 | 9/45 | 0/5 | 25/45 | 600 | 24 | 7283/68/0.982 | 1114/1320/0.52 | 2/5 −0.125 | 0/5 −0.328 |
| ensena1 | el hijo nace con las dos filas lentas del padre | 5 | 0.612 | 0.612, 0.648, 0.551, 0.441, 0.774 | 0/5 | 11/45 | 0/5 | 31/45 | 600 | 16 | 7867/45/0.988 | 1227/1255/0.514 | 3/5 +0.001 | 0/5 −0.345 |
| margen | O1 MARGEN: no come lo bueno lleno (sesgo +6, reserva −12) | 5 | 0.600 | 0.37, 0.805, 0.944, 0.6, 0.421 | 1/5 | 13/45 | 1/5 | 30/45 | 600 | 19 | 8778/46/0.984 | 960/1490/0.45 | 3/5 +0.158 | 1/5 −0.347 |
| patas4 | patas doble dosis (+4/+2) | 5 | 0.600 | 0.395, 0.5, 0.6, 0.765, 0.6 | 0/5 | 13/45 | 0/5 | 31/45 | 600 | 18 | 8495/49/0.985 | 1030/1401/0.482 | 1/5 −0.144 | 0/5 −0.347 |
| **v143** | el bicho real (genoma 0) | **10** | **0.596** | 0.65, 0.647, 0.674, 0.414, 0.744, 0.432, 0.464, 0.545, 0.676, 0.526 | 0/10 | 21/90 | 0/10 | 58/90 | 431 | 18.5 | 16487/45/0.987 | 2288/1400/0.492 | – | 0/5 −0.305 |
| patas_act | sólo pata_act_sesgo +2 | 5 | 0.581 | 0.776, 0.329, 0.581, 0.703, 0.458 | 0/5 | 16/45 | 0/5 | 28/45 | 600 | 17 | 8344/47/0.985 | 1082/1407/0.488 | 2/5 −0.093 | 0/5 −0.319 |
| sac6 | saciedad fuerte (reserva −6 en las 3 bocas) | 5 | 0.577 | 0.739, 0.24, 0.577, 0.568, 0.706 | 0/5 | 12/45 | 0/5 | 26/45 | 600 | 15 | 5339/49/0.981 | 795/1554/0.501 | 2/5 −0.038 | 0/5 −0.323 |
| sac2 | saciedad literal de Prometeo s30006 (reserva −2) | 5 | 0.576 | 0.667, 0.571, 0.576, 0.302, 0.833 | 0/5 | 11/45 | 0/5 | 31/45 | 600 | 14 | 7072/46/0.985 | 1097/1401/0.501 | 2/5 −0.076 | 0/5 −0.324 |
| patas_neof_fuerte | patas + neofobia fuerte | 5 | 0.561 | 0.588, 0.545, 0.526, 0.561, 0.739 | 0/5 | 15/45 | 0/5 | 30/45 | 600 | 18 | 7913/49/0.986 | 1137/1357/0.49 | 1/5 −0.062 | 0/5 −0.374 |
| neofobia | PRUEBA de O1, dosis débil (sesgo −6, reserva +15) | 5 | 0.545 | 0.833, 0.661, 0.418, 0.478, 0.545 | 0/5 | 11/45 | 0/5 | 32/45 | 452 | 20 | 8747/46/0.988 | 1018/1386/0.482 | 3/5 +0.014 | 0/5 −0.402 |
| nomalo | la boca nunca muerde lo que sabe malo (sesgo −8) | 5 | **0.181** | 0.181, 0.244, 0.489, 0.179, 0.145 | 0/5 | 4/45 | 0/5 | 19/45 | 200 | 86 | 8970/200/0.991 | 618/1438/0.45 | 0/5 −0.403 | 0/5 −0.768 |

Contabilidad física coherente en 100 % de los linajes; 0 escrituras en la pizarra; el mundo nunca se tapa (2.3–3.9 % de pasos sin nada
bueno, O1 3.9 %). Causas de muerte: en todos los brazos v14.3 el 91–94 % es sal/veneno (casi todo fundadores); O1 71 %.

## 3. Lo mejor, en humano
- **Patas (ir a lo que sirve).** El cuerpo de v14.3 va al objeto más cercano, sea lo que sea, y la boca decide al llegar. Con el cable
  `pata_act_sesgo +2`, un objeto que el cuerpo valora positivo para su necesidad activa "se acerca" 16 celdas por unidad de valor: el
  hambriento va a la comida aunque el veneno esté más cerca. Cambia el objetivo en 138 077 de 3.6 millones de decisiones (3.8 %) y muerde
  menos B+D (78 contra 109 por linaje). En 10 semillas pareadas gana 7/10 con +0.13 de mediana. **Pero** la dosis doble (patas4) baja a
  0.60 y sólo la fila activa (patas_act) a 0.58: sin dosis-respuesta no me lo creo como más que ruido de 5–10 semillas.
- **o1genes (O1 escrito en genes)** llegó a 0.943 en s33001 (5/9 linajes cruzan, 1 fundador) y a 0.46 en s33002. Es el brazo con más
  linajes establecidos con R0 alto (mediana de los establecidos 0.909, contra 0.818 de v143 y 0.949 de O1), pero también con más linajes
  que nunca se establecen (18/45). Es la firma de todo v14.3 en esta pista: **bimodal**: el linaje que se establece (0 fundadores tras
  t 10 000) ronda 0.82–0.91; el que no, se queda en 0.05 con cientos de fundadores.
- **Lo que enseña ENSEÑA:** copiarle al hijo todo el cerebro aprendido no mueve nada (0.675 y 0.612 contra 0.596; vida del hijo 1400 en
  los tres). El hijo ya recibe el nodo (últimas 20 mordidas) y con eso basta para saber las letras. El hijo muere a los ~1400 pasos con
  causas repartidas (hambre 30 %, sed 22 %, sal 30 %, veneno 18 %) y deja 1.6 hijos; el de O1 muere a los 3271 casi sólo de hambre y sed
  (70 %) y deja 2.3. **El hijo de v14.3 muerde B/D sabiendo que son malos** (limpieza física de APR, o la boca de FABRICA cuando no hay meta
  y el hambre empuja). Limpia, malo suave y nomalo (tres dosis de "no muerdas lo malo") no lo arreglan: nomalo lo hunde (el fundador se
  queda a 0.2 sin poder recuperarse y vive 200 pasos; 86 fundadores por linaje).

## 4. Lo que no funcionó (predicciones refutadas, `PREDICCIONES_previas.md`)
| # | predicción | resultado |
|---|---|---|
| A1 | v143 en [0.45, 0.70] | se cumple (0.596; por semilla 0.41–0.74) |
| A2 | O1 ≥ 0.85 | se cumple (0.947, 5/5) |
| P1 | sac2 ≈ v143 (dif ≤ 0.05) | **refutada por poco**: −0.076, pierde 3/5 |
| P2 | sac6 < v143 en ≥ 4/5 | refutada: pierde 3/5 (−0.04). La saciedad no hace nada aquí: el cuerpo casi nunca está lleno |
| P3 | margen ≈ v143 | refutada en la forma: dif +0.158 en la mediana pareada pero 3/5 y rango 0.37–0.94: varianza, no efecto |
| P4 | nomalo < v143 en ≥ 4/5 | **se cumple** (0/5, −0.40) |
| P5 | limpia > v143 con dif ≥ 0.05 en 4/5 | **refutada** (3/5, +0.006) |
| P6 | neofobia > v143 con dif ≥ 0.05 en 4/5 | **refutada** (3/5, +0.014); la dosis débil era casi inerte (boca_dif 1 en T 2000). Con dosis fuerte 0.714 (3/5, +0.048): tampoco |
| P7 | patas > v143 con dif ≥ 0.05 en 4/5 | se cumple en 5 (4/5, +0.145) y en 10 (7/10, +0.129); pero sin dosis-respuesta |
| P8 | o1genes el mejor de los genes, en [0.60, 0.80] | se cumple (0.768), con varianza enorme |
| P9 | ensena1 > v143 con dif ≥ 0.10 en 4/5 | **refutada** (3/5, +0.001) |
| P10 | ensena2 el mejor de todos, en [0.70, 0.85] | **refutada** (0.675, cuarto) |
| P11 | nadie llega a ≥ 0.85 en ≥ 3/5 | **se cumple** |
| P12 | nadie llega a ≥ 0.90 en ≥ 3/5 | se cumple |
| P13 | en el mejor brazo el fundador sigue con vida < 100 y > 95 % sin parir | **se cumple en los 21 brazos** (43–68 pasos, 98.2–99.1 %); nomalo lo alarga a 200 sin que pare |

**No probado, y por qué:** vida rápida (dote, rep_X) son costos del mundo (REGLAMENTO §4); ojo/vista es inerte aquí (opción A: el carro ve
el anillo entero); contención (APR) ya está dentro de v14.3 (OPCION 1) y se midió en `tronco_v14_3` (SINTD ≈ V143).

**Fallos míos, declarados:** (a) edité `corre_trasp.py` (brazos nuevos) después de lanzar la cola de la ola 2: 19 corridas abortaron con
"brazo desconocido" y se repitieron con el archivo ya fijo (mismo instrumento, misma semilla: deterministas); (b) el contador
`ensena.hijos` de la telemetría propia sólo refleja la última instancia del linaje (fundador limpio), no cuenta; (c) los pesos fuera
de [−4, 4] no los puede alcanzar la mutación ±1 de `cruce`: lo que aquí se prueba es el trasplante a mano, no su evolucionabilidad.

## 5. Lectura honesta: por qué no cruza y qué le falta
1. **La letra con fundador limpio mide sobre todo la lotería del fundador.** El fundador nace a 0.6/0.6 sin saber nada; la mitad de las
   letras son malas; una mordida mala lo deja a 0.2 y la segunda lo mata. O1 tiene el mismo fundador ciego (vida 200, 96 % sin parir): la
   diferencia entera está en que **una vez establecido, O1 no se extingue** (38/45 linajes con 0 fundadores tras t 10 000 y R0 0.949).
   v14.3 se establece en 29–30/45 y, establecido, ronda 0.82–0.84.
2. **Ningún cable de la boca ni las patas ni enseñar al hijo cambia al fundador** (P13). No hay nada legal en el carro que arregle al
   fundador ciego: sólo la dote (mundo) o que el linaje no lo necesite (que el hijo no se extinga).
3. **El hijo de v14.3 vive la mitad y deja 1.6 en vez de 2.3.** No es ignorancia (ENSEÑA no ayuda): el hijo sabe qué es malo y lo muerde
   igual, y además muere de hambre y sed más que O1 en proporción a lo que vive. La pieza que falta no es un cable lineal de seis
   señales: es *cuándo* muerde lo malo y cómo busca lo bueno cuando no lo hay a la vista (O1 se coloca en el hueco más grande entre
   cuerpos; v14.3 no hace nada con los otros cuerpos).
4. La base de 36 genes lineales **contiene** la política de O1 (o1genes llega a 0.943 en una semilla) pero con la varianza de v14.3
   debajo: los genes sobre un cerebro que aprende dan un fenotipo que depende de lo que el cerebro aprendió en esa semilla.

## 6. ¿Merece preregistro? Uno chico y con otra pregunta; el gordo no
- **Chico (patas):** «¿ir a lo que le sirve a la necesidad activa sube el R0 real de v14.3 fijo en la pista?» 20 semillas, T 100 000,
  fundador limpio. Brazos: v143, patas (+2/+1), patas invertida (−2/−1: va hacia lo que NO le sirve; control de contenido), patas
  desfasada (DESF de `cruce`: el valor lo lee pero la señal de estado viene de un paso pasado; aquí el cable no lee estado, así que
  DESF debería ser inerte y sirve de guardia), O1. Letra: MODESTO si patas > v143 en ≥ 15/20 con dif ≥ 0.05 y la invertida < v143;
  FUNCIONA nunca (no cruza). Mi predicción honesta: MODESTO con p 0.30; NO 0.65. Costo ~80 corridas de 2 min: 30 min con 6 procesos.
- **El que sí importa, y no es de trasplantes:** medir por separado *establecimiento* (fracción de linajes con 0 fundadores tras
  t 10 000) y *R0 del establecido*. Con esa partición, v14.3 ya está en 0.82–0.84 establecido y O1 en 0.95; el muro son los 15/45
  linajes que nunca arrancan. Una pregunta para el director: si la letra con fundador limpio es la que quiere, la pieza a buscar es
  del hijo (que el linaje establecido no se extinga), no del fundador ni de la boca.

## 7. Archivos
`PREDICCIONES_previas.md` (firmadas 13:35, antes de correr) · `construye_trasp.py` → `carros/TRASP.py` (sha b9cf178c7c816398; origen
CRUCE.py 63ac38bac2d0bbcd) · `corre_trasp.py` · `lanza.py` (+ `lanza.log`) · `lee_trasp.py` (`--md` da la tabla de §2) · `datos/*.json`
(115 crudos, uno por corrida, con `telem` por cuerpo) y `datos/*.out`.
