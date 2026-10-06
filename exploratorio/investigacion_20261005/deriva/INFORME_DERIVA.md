# INFORME DERIVA — la célula de JUACO como aprendizaje en línea con deriva de concepto, contra rivales estándar (5-oct-2026, exploración, predicciones escritas antes, 10 semillas)

**NO.** En las pruebas estándar de flujos con deriva (SEA, hiperplano, STAGGER, RBF; abrupta y gradual, con vuelta del concepto y ruido de etiquetas 10 %), la célula pegada a un modelo congelado **no gana a ningún rival estándar en ningún régimen por mérito propio**: en los tres espacios continuos la perilla que eligió la validación es "no pisar casi nunca" y la célula queda **idéntica al base congelado** (0 pisadas en hiperplano, 13 en RBF, 28 en SEA en 4 000 pasos); cuando se la obliga a pisar, empeora (SEA 0.86 → 0.77–0.83). Donde "gana" al kNN con ventana chica o en la vuelta del concepto, el mérito es del base congelado, no de la célula (célula vs base: 39/17 en 80 pares, mediana +0.000). La única prueba donde la célula hace algo es STAGGER (categórico, 27 combinaciones): ahí es una tabla de búsqueda con olvido y **empata con SGD y SGD+DDM (3/7, −0.005), gana por +0.02–0.03 a kNN, NB, DWM y reentrenar (10/10) con C ≥ 50, y pierde contra todos con C=20** (0.76 vs 0.86). La célula sola (B) es inútil en lo continuo (0.50). Los controles caen sólo donde la célula actúa (barajada en STAGGER 0.71 vs 0.85; sin compuerta 0.61–0.77 en todo): el mecanismo funciona, pero no hay nada que corregir que un SGD o un kNN no corrijan mejor. **Esto le ahorra al director la línea "célula = método de ML para deriva"**: con vecinos continuos y ruido, "corregir donde el base falla, hecho a hecho" no es un algoritmo competitivo; lo del informe 3 valía porque allí los hechos eran puntos sin vecinos y sin ruido.

Misión: llegar a la AGI por este camino (aquí, pregunta del director: ¿la célula sirve para otra cosa, ML?). Carpeta `PROYECTOS\JUACO\investigacion_20261005\deriva\` (fuera de git): `deriva.py` (generadores, 11 métodos, prequential), `analiza.py` (tablas y pareadas), `sensibilidad.py`, `PREDICCIONES.md` (antes de correr), `datos\validacion.{json,txt}`, `datos\deriva.json` (crudo), `datos\tablas.md` (todas las tablas), `datos\sensibilidad.md`. CPU total ≈ 11 min, un proceso, numpy puro, nada instalado ni descargado.

## 1. Diseño
- **Generadores** (de memoria, [M]): SEA (Street & Kim 2001: 3 atributos U[0,10], y = x1+x2 ≤ θ, θ = 8/9/7), hiperplano (Hulten, Spencer & Domingos 2001: d=10, y = Σ wᵢ(xᵢ−½) > 0, cambia w), STAGGER (Schlimmer & Granger 1986: tamaño/color/forma, c1 = small∧red, c2 = green∨circle, c3 = medium∨large), RBF con centros que se mueven (RandomRBF de MOA, Bifet et al. 2010: 6 centros gaussianos, 2 clases, la deriva desplaza los centros). LED y Agrawal no cupieron.
- **Calendario**: 4 000 pasos en 4 tramos: A, B, **A (recurrente)**, C. Abrupto (salto) y gradual (Gama 2004: 300 pasos con probabilidad creciente del concepto nuevo). Ruido de etiquetas 10 % (techo 0.90). Evaluación prequential: predecir, luego aprender. Medidas: acierto global, acierto en los 200 pasos tras cada cambio, pasos hasta que la ventana de 50 vuelve a ≥ 0.80, memoria, ops por ejemplo.
- **Base congelado**: MLP 16 ocultas (Adam, 400 pasos) sobre 600 ejemplos del concepto A; paso 0: 0.873 [0.78–0.95]. **Rivales**: SGD en línea (mismo MLP), SGD + DDM (Gama 2004: reinicio al disparar, calentado con los últimos 30), kNN con ventana (k=5), Naive Bayes gaussiano con olvido (λ=0.995), DWM-NB (Kolter & Maloof 2007: expertos NB, β=0.5, θ=0.01, ≤10), reentrenar el MLP en ventana cada 50 pasos (techo caro). Árbol de Hoeffding: **no cupo**, se dice. **Célula A**: bloque del informe 3 pegado al base (prototipo+valor+energía; compuerta; cobra sólo si pisó y acertó donde el base fallaba; paga por existir; muere la más pobre; suelta la corrección si pisó donde el base acertaba). **Célula B**: sola, el "base" es la clase mayoritaria con olvido. Controles: pago barajado; sin compuerta. Memoria C ∈ {20, 50, 200} para kNN, reentrenar y células.
- **Validación aparte** (semillas 101–103, abrupto y gradual, C=50, una perilla a la vez, sólo el método que la usa): lr 0.03; k 5; λ 0.995; **σ de la célula 0.05·√D (la más estrecha de {0.05, 0.1, 0.2, 0.4}: 0.768 vs 0.721 con 0.4)**; castigo al pisar mal = muerte inmediata (como el original: 0.768 vs 0.753 con castigo gradual); compuerta por evidencia (0.790 vs 0.768 original).

## 2. Tabla 1 — acierto prequential global (mediana de 10; C=50; abrupto / gradual). Completa por C en `datos\tablas.md`
| prueba | base | SGD | SGD+DDM | NB olvido | DWM | kNN-50 | reentrenar-50 | **célula A** | célula B | barajada | sin compuerta |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SEA | 0.86/0.86 | 0.85/0.85 | 0.85/0.85 | **0.86/0.86** | 0.85/0.84 | 0.80/0.80 | 0.82/0.82 | 0.86/0.86 (= base) | 0.66 | 0.85 | 0.77 |
| hiperplano | 0.65/0.67 | 0.73/0.73 | 0.72/0.72 | **0.78/0.78** | 0.76/0.75 | 0.67/0.66 | 0.74/0.73 | 0.65/0.67 (= base) | 0.50 | 0.65 | 0.61 |
| STAGGER | 0.62/0.65 | **0.86/0.84** | 0.86/0.84 | 0.83/0.82 | 0.82/0.80 | 0.83/0.80 | 0.83/0.81 | 0.85/0.84 | 0.84/0.82 | 0.71 | 0.66 |
| RBF | 0.82/0.82 | 0.83/0.83 | 0.80/0.81 | 0.83/0.82 | 0.81/0.81 | **0.85/0.85** | 0.81/0.81 | 0.82/0.83 (= base) | 0.50 | 0.82 | 0.73 |

Con C=20: kNN cae (0.75/0.63/0.78/0.73), reentrenar cae, célula A = base en lo continuo y **0.76 en STAGGER (pierde a todos: necesita 27 celdas)**. Con C=200: kNN 0.84/0.71/0.86/0.87 (gana en RBF y empata en STAGGER), célula A sin cambio (guarda 72/200/50/134).

## 3. Tabla 2 — tras el cambio (C=50, abrupto): acierto en los 200 pasos siguientes al cambio 1 (A→B) / 2 (**vuelve A**) / 3 (A→C), y pasos hasta ventana-50 ≥ 0.80
| prueba | base | SGD+DDM | NB | DWM | kNN-50 | reentrenar | **célula A** |
|---|---|---|---|---|---|---|---|
| hiperplano | 0.47/**0.83**/0.48 · nunca/0/nunca | 0.56/0.57/0.55 · 327/314/371 | 0.61/0.65/0.64 · 236/149/144 | **0.69**/0.71/**0.71** · 100/75/85 | 0.67/0.67/0.67 · 263/116/158 | **0.71**/0.69/0.68 · 72/90/63 | 0.47/0.83/0.48 (= base) |
| STAGGER | 0.40/**0.90**/0.26 | 0.69/0.72/0.72 · 83/57/72 | 0.62/0.55/0.60 | **0.83**/0.42/**0.87** · 27/455/4 | 0.76/0.82/**0.80** · 24/19/29 | 0.75/0.76/0.71 · 43/48/42 | 0.73/0.79/0.69 · 54/62/72 |
| RBF | 0.78/**0.86**/0.75 | 0.80/0.79/0.77 | 0.80/0.76/0.78 | 0.79/0.78/0.76 | **0.85**/0.82/**0.84** · 1/0/0 | 0.80/0.78/0.77 | 0.78/0.86/0.75 (= base) |
| SEA | 0.80/0.88/0.87 | 0.83/0.86/0.86 | 0.84/0.85/0.88 | 0.80/0.83/0.86 | 0.78/0.80/0.82 | 0.80/0.81/0.84 | 0.80/0.87/0.87 |

**Recurrencia**: tras la vuelta de A, la célula A está en 0.83–0.87 en hiperplano/RBF/SEA y gana a todos los rivales (vs SGD+DDM 52/26, kNN 56/23, reentrenar 58/19 en 80 pares) — **pero vs el base congelado es 18/25: es el base el que ya sabía A**; la célula aporta no haber estorbado. En STAGGER (donde sí actúa) la vuelta la hace en 62 pasos a 0.79, contra 19 pasos / 0.82 del kNN y 0 pasos / 0.90 del base; el DWM se derrumba en la vuelta (0.42: sus expertos viejos ya murieron).

## 4. Tabla 3 — "gana en k de 10", célula A vs cada rival, acierto global, suma sobre 8 pruebas (gana/pierde de 80)
| C | base | SGD | SGD+DDM | NB | DWM | kNN | reentrenar | célula B | barajada | sin compuerta |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 | 38/14 (+0.00) | 22/58 | 29/51 | 14/66 | 36/44 | 59/20 | 46/34 | 61/19 | 37/7 | 78/2 |
| 50 | 39/17 (+0.00) | 29/51 | 34/46 | 34/46 | 53/27 | 49/31 | 49/31 | 80/0 | 57/2 | 78/2 |
| 200 | 44/14 (+0.00) | 35/45 | 40/40 | 32/48 | 54/26 | 26/52 | 25/54 | 80/0 | 57/1 | 78/2 |

Lectura honesta: las "victorias" sobre kNN-20, reentrenar-20 y DWM son victorias del base congelado (SEA y RBF: la célula = base, diferencia +0.000); las derrotas contra SGD, SGD+DDM y NB en hiperplano son 0/10 con −0.05 a −0.13 porque la célula no corrige una frontera lineal que cambió globalmente en d=10 con 50 prototipos. STAGGER por separado (C=50): célula A vs SGD 3/7 (−0.005), SGD+DDM 3/7, NB **10/0 (+0.022)**, DWM **10/0 (+0.029)**, kNN **10/0 (+0.026)**, reentrenar **10/0 (+0.026)**; el rival que queda más cerca es SGD en línea (empate).

## 5. Costo y memoria (abrupto, C=50; ops por ejemplo, mediana)
Base 160–384; SGD 640–1 536 (4× base); NB 36–120; DWM 388–1 204; kNN-50 447–1 490; **célula A 727–2 314 (4.5–6× base; con C=200 hasta 5 891)**; reentrenar-50 29 k–70 k (180× base). Memoria final: kNN siempre llena la ventana; célula A con C=200 guarda 72 (SEA), 50 (STAGGER), 134 (RBF), 200 (hiperplano: nace y muere sin cobrar nunca: 1 395 nacimientos, 0 pisadas). La célula es más cara que el kNN con la misma memoria porque además corre el base.

## 6. Sensibilidad: qué pasa cuando la célula SÍ pisa (`datos\sensibilidad.md`, C=50, abrupto, 10 semillas)
| σ·√D | compuerta | SEA | hiperplano | STAGGER | RBF |
|---|---|---|---|---|---|
| 0.05 (validada) | evidencia | 0.857 (28 pisadas) | 0.651 (0) | 0.851 (1 258) | 0.821 (13) |
| 0.1 | evidencia | 0.846 (171) | 0.651 (0) | 0.851 | **0.846 (294)** ← lo único modesto: +0.025 sobre el base; kNN-50 da 0.85 |
| 0.2 | evidencia | 0.828 (228) | 0.657 (137) | 0.851 | 0.819 (458) |
| 0.05 | original (informe 3) | 0.820 (348) | 0.651 | 0.808 (1 494) | 0.809 (165) |
| 0.2 | original | **0.769** (567) | 0.652 (619) | 0.808 | **0.771** (716) |
Cuanto más pisa, peor; la compuerta original del informe 3 pierde 0.04–0.09 contra la de evidencia porque con ruido 10 % cada fallo del base es ambiguo entre deriva y ruido y la célula recién nacida pisa y daña.

## 7. Predicciones (PREDICCIONES.md) contra lo medido
1 (p=.75, NO o modesto) **cumplida: NO**. 2 (p=.6, gana en la vuelta a SGD+DDM/kNN en ≥3/4) cumplida en la letra (4/4 abrupto) **pero por el base, no por la célula** (vs base 18/25). 3 (p=.55, gana a kNN-20 en ≥3/4) cumplida, igual de hueca. 4 (p=.7, célula B pierde) cumplida (0.50 en continuo; 0.84 en STAGGER). 5 (p=.8, controles caen ≥8/10) cumplida donde la célula actúa; donde no actúa barajada = célula (nada que barajar). 6 (p=.6, el ruido le pega y habría que suavizar) cumplida: la validación eligió "casi no pisar". 7 (p=.65, costo 1.2–3× base) parcial: 4.5–6×. 8 (p=.5, DWM el más cercano en recurrencia) **fallida: DWM es el peor en la vuelta** (0.42 en STAGGER); el más cercano es SGD. 9 (p=.7, STAGGER la peor prueba para la célula) **fallida al revés: es la única donde hace algo**. 10 (p=.6, hiperplano gradual sin destacar) cumplida.

## 8. Frases que el director SÍ puede decir a alguien de aprendizaje automático, y las que no
SÍ: (1) "Probamos la célula como corrector en línea pegado a un modelo congelado en los flujos sintéticos estándar (SEA, hiperplano, STAGGER, RBF) con deriva abrupta, gradual y recurrente y 10 % de ruido, contra SGD, SGD+DDM, kNN con ventana, Naive Bayes con olvido, DWM y reentrenar: no gana a ninguno; en los espacios continuos la mejor perilla es no actuar". (2) "En un problema categórico (STAGGER) funciona como una tabla de búsqueda con olvido por energía: empata con SGD y gana por +0.02 a kNN/NB/DWM con memoria ≥ 50, y pierde con memoria 20". (3) "La ventaja en deriva recurrente que medimos es del modelo congelado que ya conocía el concepto viejo, y la célula sólo aporta no romperlo; eso lo da también un detector de deriva con un modelo guardado".
NO: "la célula es un método de aprendizaje en línea competitivo", "gana al kNN con memoria chica" (gana el base), "recupera más rápido tras la vuelta" (el base ya sabía), "sirve con ruido de etiquetas" (hubo que cambiar la compuerta y aun así la mejor opción fue callarse), "generaliza la corrección a vecinos" (en hiperplano con 50 prototipos no corrige nada).

## 9. Qué de esto ya existe con otro nombre
- **IB2/IB3 (Aha, Kibler & Albert 1991)**: aprendizaje basado en instancias que guarda sólo los ejemplos mal clasificados y borra los de mal historial de acierto: es la célula (nace donde falla, muere si no sirve) con contador de aciertos en vez de energía; la célula añade pago por camino y "soltar" al pisar bien al base.
- **Sistemas de clasificadores XCS/LCS (Holland; Wilson 1995)**: reglas con fuerza que cobran por acertar, pagan por existir y mueren por escasez, con cobertura (nace una regla cuando ninguna cubre): es el parecido más fuerte; la célula es una población de reglas-prototipo sin algoritmo genético y pegada a un base.
- **kNN con ventana / olvido por tiempo (SAM-kNN, Losing 2016)**: olvido por antigüedad; la célula olvida por utilidad (energía).
- **Memoria episódica / replay**: guarda episodios para no olvidar; aquí la memoria sólo guarda donde el base falla y se autolimpia.
- **GRACE (Hartvigsen 2023)**: claves de capa con radio que pisan al modelo congelado: la célula A es GRACE con energía y muerte; GRACE tampoco se vendió como método de deriva.
- **Detectores de deriva con modelo guardado (recurrent concept drift: RCD, Gama & Kosina 2014)**: guardan modelos viejos y los reactivan cuando el concepto vuelve: eso es lo que hace aquí el base congelado y lo que explica la "ventaja" en recurrencia.

## 10. Siguiente paso con datos reales (si el director aún quiere)
No lo recomiendo con este resultado. Si se hace: Electricity/Elec2 (45 312 filas, 8 atributos, deriva real recurrente diaria; descargar de MOA/OpenML, ~3 MB), Covertype (581 k × 54, OpenML, ~11 MB), Airlines (539 k × 7, MOA, ~4 MB); haría falta descargar `river` o MOA para los rivales de referencia (árbol de Hoeffding, ADWIN, SAM-kNN) en vez de los míos. Predicción: la célula = base congelado en los tres, y el kNN/SAM-kNN y el árbol adaptativo ganan.

## 11. Lo que ajusté viendo datos (declarado), reproducir, no verificado
- Viendo el humo de 1 semilla (antes de la validación): σ relativa a √D (sin eso en d=10 nunca pisa); DWM con expertos NB (con MLP al azar daba 0.77 en SEA); **compuerta por evidencia** (la célula que oye sin pisar suma si pisar habría servido y resta si habría dañado; pisa sólo con evidencia > 0): con ruido 10 % la original del informe 3 dañaba al base (0.78 vs 0.86 en SEA). Luego la validación en flujo aparte eligió entre original y evidencia, y σ, castigo, lr, k, λ.
- Reproducir: `cd deriva; python deriva.py --valida; python deriva.py --semillas 10; python analiza.py; python sensibilidad.py` (≈ 11 min).
- No verificado: sin preregistro formal (predicciones sí); 10 semillas sin réplica; los rivales son mis implementaciones (kNN sin ponderar, DDM sin usar la ventana de aviso completa, DWM-NB sin período > 1, NB gaussiano sobre one-hot en STAGGER); sin árbol de Hoeffding ni ADWIN; la "recuperación" es ventana-50 ≥ 0.80, que el base cumple de entrada en SEA/RBF (los cambios de SEA y RBF son suaves: el base queda en 0.78–0.82 tras el cambio); 4 generadores, un solo calendario de 4 tramos; perillas de la célula heredadas del informe 3 (existir 0.002, pago 1, castigo 0.5, η 0.3) sin barrido; ops = multiplicaciones-sumas aproximadas.
