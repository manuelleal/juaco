# PREREGISTRO — pista v2 con generaciones solapadas (22-sep-2026, antes de cualquier serie)

Misión: llegar a la AGI por este camino. Rama `generaciones-conviven` (sale de a170746). Carpeta: `experimentos/generaciones/`.
Instrumento: `pista2.py` (4d2bee16e7961261, construido por anclas desde `carrera_escuderias/pista.py` 9f47c65e438e0ff4),
`motor_convive.py` (d10cb9021f5d0f41), juez `corre_convive.py` (2b04acdff6523b33), control `carros_ctrl/CTRL_O3_SINTERM.py`
(7bb2fff33017e559: O3 0442c2884fcb0e11 con `TERMINAL = False`, una sola línea). Arnés `identidad_convive.py`: **36/36**.

## 1. Hipótesis
**H (coordinador):** con generaciones solapadas, la muerte programada deja de dar ventaja: O2 (sin muerte programada)
persiste igual o mejor que O3 y O4.
**H-b (mecanismo, agregada por el creador):** dentro del mismo carro, apagar la muerte programada no cuesta persistencia
(O3 contra CTRL_O3_SINTERM; O4 contra O1, que es O4 sin M2).

## 2. Mundo (fijado)
- Los mismos objetos, efectos, costos, ventana de 500 pasos y dote 0.6 que la carrera. L = 360, nobj ≤ 36 y 9 sorteos de olvido por paso.
- **P1 parto real:** el hijo nace en el paso del parto, en la celda del padre, con E = Ag = 0.6 pagados por el padre.
- **P2:** cada cuerpo es una instancia del carro: `crea` y luego `nace(memoria = al_parir del padre)`.
- **P3:** fundador limpio solo si muere el último cuerpo del linaje.
- **P5:** `quiere_parir` recibe `cola` = parientes vivos del linaje.
- **P7 reposición fija (quimiostato):** 0.03·9 = 0.27 objetos por paso, con un banco de ≤ 1 objeto pendiente. Así la
  densidad la regula el recurso. Con la regla de v1 (reposición inmediata) no hay capacidad de carga para quien limpia: se midió
  un crecimiento de 9 a 128 O2 en 5000 pasos.
- **Tope de seguridad:** 300 cuerpos en toda la pista. No se alcanzó en ningún humo (máximo 35). Si se alcanza, la corrida queda marcada.

## 3. Series
- Monocultivo de 9 fundadores por carro: FABRICA, O1, O2, O3, O4 y CTRL_O3_SINTERM.
- T = 100000, reposición `fija`.
- **Serie 10101–10120** y **réplica 10121–10140**. Práctica 10001–10040 (humos usados: 10001, 10012, 10013; arnés 10001–10015).
- Verificado con grep: ninguna de las tres ventanas aparece como semilla en el repo, en `carrera` ni en `bundle`.

## 4. Métricas (del juez, solo física)
- **Persiste** (letra de la ENMIENDA 6): un linaje-semilla persiste si tiene 0 fundadores tras t = 10000 y ≥ 5 nacimientos.
  - «Estabiliza en la semilla»: más de la mitad de los 9 linajes persisten.
  - «Persiste el carro en la semilla»: al menos 1 linaje persiste.
- **R0 verdadero (cohorte):** la media de hijos de los individuos nacidos en t ≤ T/2. Los vivos en T cuentan con los hijos que
  llevan (cota inferior) y se reporta la fracción censurada. Al lado van R0 de vidas completas y R0 de todos los muertos
  (este último está sesgado).
- **Tamaño del linaje:** media y mínimo para t ≥ 10000, más el tamaño final. También los cuerpos vivos del carro en la pista.
- **Generaciones:** profundidad máxima de la genealogía.
- **Muertes voluntarias:** las que declara el carro (O3 `cuerpos_term`, O4 `senescentes`). La clasificación física va al lado,
  sin valor (ERR-103).

## 5. Predicciones firmadas (creador, tras el humo 10012 a T = 20000; ver INFORME_CONVIVE.md)
| carro | persisten (de 180) | tamaño medio del linaje (mediana) | semillas con ≥ 1 linaje que persiste (de 20) |
|---|---|---|---|
| FABRICA | 0–5 | 0.9–1.2 | 0–2 |
| O1 | 0–30 | 1.1–2.2 | 8–20 |
| O2 | 5–45 | 1.1–2.2 | 12–20 |
| O3 | 10–60 | 1.2–2.5 | 15–20 |
| O4 | 5–50 | 1.0–2.0 | 12–20 |
| CTRL_O3_SINTERM | 10–60 | 1.2–2.5 | 15–20 |

- **Estructural:** ningún carro «estabiliza» por la letra de la ENMIENDA 6 (> 4.5 de 9 linajes). Probabilidad 0.85.
  Nueve linajes del mismo carro comparten una capacidad de ~15–30 cuerpos, así que se pierden por **deriva y exclusión
  competitiva** (Gause; coalescencia de Wright-Fisher/Moran: con N ≈ 20 y ~45 generaciones en 10⁵ pasos, se espera que
  sobrevivan pocos linajes). Por eso, en este mundo, la persistencia por linaje mide a la vez la deriva y la calidad del carro.
- **Muerte programada rara:** O3 y O4 declaran ≤ 10 % de sus muertes como programadas (humo: 3.5 % y 3.4 %). Probabilidad 0.8.
- **H:** O2 ≥ O3 − 15 **y** O2 ≥ O4 − 15 (persisten, de 180). **La creo REFUTADA con probabilidad 0.55:** en el humo, O2
  tuvo 2/9 contra 4/9 de O3 y O4.
- **H-b:** O3 ≤ CTRL + 15 **y** O4 ≤ O1 + 15. Se cumple con probabilidad 0.55. En el humo, O4 tuvo 4/9 contra 1/9 de O1, pero
  O4 diverge de O1 en cuanto dispara una sola senescencia: puede ser caos de trayectoria y no ventaja.
- **Tolerancia 15:** bajo un modelo binomial por linaje con p = 0.2–0.4, la desviación estándar de la diferencia de sumas en 20
  semillas es ~8–9.
- **No evaluable:** si ningún carro de la comparación llega a 10 linajes persistentes, H o H-b se declara NO EVALUABLE (trampa del piso).

## 6. Controles que pueden fallar
- **FABRICA (piso):** si persiste en ≥ 10 linajes, el mundo es demasiado fácil y H no dice nada.
- **CTRL_O3_SINTERM:** H-b para O3.
- **O1:** H-b para O4.
- **El arnés (S)**, sin partos, es v2 == v1 bit a bit con reposición inmediata. Si falla, no se corre nada.

## 7. Qué refuta
- **H:** O2 < O3 − 15 o O2 < O4 − 15.
- **H-b:** O3 > CTRL + 15 o O4 > O1 + 15, es decir, la muerte programada sigue dando ventaja con generaciones solapadas.
- **El instrumento:** si alguna serie tiene `bloqueados` > 0, la capacidad no la reguló el mundo y la serie no vale para H.
- **La réplica:** debe dar el mismo veredicto de H y H-b. Si no, no se declara.

## 8. Vocabulario
«Linaje» y «tamaño del linaje». «Población» solo en el informe, con la medida al lado (cuerpos vivos del carro). No se dice
«evoluciona» ni «coopera».

## 9. DECISIONES DEL COORDINADOR (22-sep-2026, antes de cualquier serie; el director delegó: "las otras tú decides")

1. **Quimiostato P7: APROBADO** como mundo de esta rama: lo mordido u olvidado desaparece y el mundo repone a un ritmo fijo (0.27/paso con 9
   linajes, hasta 36 objetos; se escala con el número de linajes fundadores). **ERR-104** (lo numera el coordinador): en el mundo de la carrera
   (v1), morder cualquier objeto lo repone al instante con una letra al azar, así que morder lo malo **fabrica comida** (~0.5 buenos por mordida)
   y, con generaciones solapadas, no hay capacidad de carga (9 → 128 cuerpos en 5000 pasos). **Reserva del hito H-1:** la limpieza de O1
   depende en parte de esa regla de reposición instantánea. El cruce vale en ese mundo, con esa letra, y el informe del hito lo tiene que decir.
2. **Unidad de análisis:** con 9 linajes del mismo carro compartiendo 15–30 cuerpos, la extinción por **deriva** entre linajes hermanos es
   esperable y no mide la estrategia. Por eso:
   - **Criterio principal:** *persiste el carro* (≥ 1 linaje vivo sin fundadores puestos por el mundo después de t = 10000) y el **tamaño del
     carro** (cuerpos vivos, media en la segunda mitad de T), en monocultivo, por semilla. **Estabiliza** el carro si persiste en ≥ 15/20 semillas.
   - **La persistencia por linaje** (la de la ENMIENDA 6) se reporta y no decide.
   - **Hipótesis H evaluada en la pista MIXTA** (3 O2 + 3 O3 + 3 O4, mismo quimiostato): gana la estrategia que tiene más cuerpos vivos en la
     segunda mitad de T (mediana por semilla, prueba de signo pareada). H se sostiene si O2 no pierde contra O3 ni contra O4 (no pierde = no
     queda por debajo en ≥ 15/20 semillas). H-b queda como estaba.
3. **T = 100000**, como en toda la carrera, aunque cueste unas 2.5–3 h por serie.
4. **Predicciones firmadas del coordinador:** O2, O3 y O4 persisten como carro en monocultivo en ≥ 15/20 (probabilidad 0.70 cada uno);
   FABRICA persiste como carro en ≥ 15/20 (0.20). En la mixta, H se sostiene (O2 no pierde contra O3 ni contra O4) con probabilidad 0.45.
