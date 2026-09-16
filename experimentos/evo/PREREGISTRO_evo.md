# JUACO-EVO — evolución del organismo guiada por LLM, con mutación ciega como control

**Escrito ANTES de construir el evaluador y antes de correr. 16 sep 2026, 18:10, día 4.**

- **Dirección:** Christiam Puentes: *"un sistema evolutivo de auto-crecimiento… que nos deje el código de su evolución…
  multiplicación y evolución… usar técnicas de los LLM para que evolucione más rápido, no creando más órganos"*.
- **Traducción operativa (decisión de Claude):** el **genoma** es el archivo de código del organismo; el **fenotipo**
  es su conducta en el currículo de pruebas; la **mutación** la propone un LLM (subagente) con una hipótesis de una
  línea, **o** un operador ciego (control); la **selección** la hace un evaluador automático con criterios fijados
  aquí; el **archivo** es una rama git donde cada individuo aceptado es un commit y `LINAJE.md` es el árbol.
- **Antecedentes declarados:** AlphaEvolve (DeepMind, 2025), Darwin Gödel Machine (Sakana/UBC, 2025), ShinkaEvolve
  (Sakana, 2025), FunSearch (2023). Todos reportan **el mismo riesgo**: el sistema aprende a engañar al evaluador.
  El protocolo de este proyecto (preregistro, semillas retenidas, auditoría) es el arnés.

## 0. Lo que esto NO es (para no engañarnos)

- **No "crea la evolución"** ni comprime "de bacteria a homo sapiens". Es **búsqueda evolutiva sobre el espacio de
  reglas** de un organismo de 130 líneas, con un prior fuerte (el LLM) frente a un prior nulo (mutación ciega).
- **No sustituye la regla de cruce.** Todo individuo del archivo es **hipótesis**. Sólo se vuelve tronco si pasa el
  confirmatorio en semillas nuevas y el examen criterio v3, como v8, v9 y el intento de v10.
- **No optimiza un número.** Optimiza un vector con restricciones duras; ver §3.

## 1. Genoma, fenotipo, currículo

- **Genoma:** un archivo Python con la interfaz de `organismo_v10m.py` (`run(seed, T, invertir_en, nuevo, nuevo_val,
  solap_B, solap_AB, plast, fases, ...)` devolviendo `W, mord, vis, deaths, splits, split_t, celdas, solap, sondas`).
  **Padre de la generación 0: `organismo_v10m.py`** (v10 con instrumentación de fases; v10 pasó el examen v3 8/8).
- **Currículo (fenotipo), fijo durante todo el experimento:**
  1. Las seis etapas del examen v3 con sus criterios exactos: E1, E2, E2I, E2J, E2K, E2L.
  2. Control negativo CTRL (A∩B=3 sin plasticidad debe fallar).
  3. Bloque M de la Etapa 4 (retención con interferencia): `W_B(100k) ≤ −2` y `W_A(100k) ≥ 0.5`, con guarda
     `W_C ≤ −2.5` y `W_D ≥ 0.85` (no retener por no aprender).
- **Semillas:** entrenamiento **1–10** (las ve la selección); **retenidas 11–20** (sólo se miran al final de cada
  generación para el individuo seleccionado; si el retenido cae, el individuo se marca "sobreajustado" y no se acepta).
- **Coste:** ~80 corridas por individuo, ~1 min de pared con `Pool(14)`.

## 2. Operadores de mutación

- **LLM:** un subagente (Claude Fable 5.1) recibe el genoma padre, el registro de qué falla y qué se ha probado, y
  **propone UN cambio** (≤ 15 líneas), con una hipótesis de una línea y una predicción. Debe declarar el mecanismo y
  no puede tocar el evaluador ni el currículo. Cuatro propuestas por generación.
- **Ciego (control):** `muta_ciega.py`, con RNG propio: elige al azar una constante numérica del cuerpo de `run()` y la
  multiplica por un factor `U(0.5, 2)`, o invierte una comparación `>`/`<`. Cuatro propuestas por generación. Debe
  compilar; si no, se descarta y se sortea otra.
- **Ninguno de los dos operadores ve las semillas retenidas.**

## 3. Evaluación y selección (fijadas aquí)

**Restricciones duras** (un individuo que las viole se descarta, sin puntuación):
- H1: las seis etapas en semillas 1–10 pasan sus criterios en ≥ 9/10 cada una; CTRL falla en ≥ 9/10.
- H2: `celdas ≤ 45` en todas.
- H3: la guarda del bloque M (aprende C y D) en ≥ 8/10.

**Puntuación vectorial** (medianas sobre semillas 1–10):
- `R` = fracción de semillas con retención (`W_B ≤ −2` y `W_A ≥ 0.5`) en el bloque M ∈ [0, 1];
- `S` = 1 − muertes(E1)/200 (0 si muertes ≥ 200);
- `E` = 1 − divisiones(E2L)/9 (economía de la plasticidad; 0 si ≥ 9);
- `C` = coste de complejidad = líneas cambiadas respecto del padre / 15, con signo negativo.

**Regla de selección:** un hijo **reemplaza al padre** sólo si (a) cumple H1–H3, (b) `R_hijo ≥ R_padre + 0.1` **o**
(`R_hijo ≥ R_padre` y `S + E − C` mejora ≥ 0.05), y (c) su `R` en las semillas retenidas 11–20 es ≥ `R_padre` − 0.1.
Si varios hijos cumplen, gana el de mayor `R`; empate por `S + E − C`.

**Lo que se registra de cada individuo, gane o pierda:** genoma (sha), operador, hipótesis, puntuación completa,
diff con el padre. Nada se borra.

## 4. Preguntas falsables (las que hacen ciencia de esto)

- **P1 [aceleración].** A igual número de mutaciones evaluadas (4 por operador por generación, G generaciones), la
  rama LLM alcanza `R ≥ 0.8` (retención en 8/10) en **menos generaciones** que la rama ciega. Predicción: la ciega no
  llega a `R ≥ 0.8` en 6 generaciones; la LLM sí en ≤ 4. Cada rama evoluciona **por separado** desde el mismo padre.
- **P2 [interpretabilidad].** Toda mutación aceptada en la rama LLM tiene una hipótesis mecanicista declarada **antes**
  de evaluarla, y su diff es ≤ 15 líneas. Si una mutación aceptada no se puede explicar, se marca.
- **P3 [sobreajuste].** Al menos una mutación que gane en 1–10 caerá en 11–20 (se predice que la selección sobre pocas
  semillas produce falsos positivos). Se cuenta.
- **P4 [hackeo del evaluador].** Se predice que **al menos una** mutación mejorará `R` por la razón equivocada (p. ej.,
  no dividir, no morder, congelar el aprendizaje). H3 y las seis etapas están para atraparla; **cada aceptación la
  audito yo leyendo el diff** antes de commitear. Se cuentan los intentos de hackeo detectados.

## 5. Qué NO prueba y qué sigue

- No prueba "aprendizaje abierto" ni nivel 8; prueba si la evolución guiada encuentra órganos que yo no diseñé.
- Siguientes dimensiones, si esto funciona (las que dirección llama "aprender por dimensiones"): (i) **población**, no
  individuo (varios genomas coexistiendo, cruce); (ii) **co-evolución del mundo** (el currículo también muta: más
  estímulos, reglas no lineales, novedad procedural); (iii) archivo por **novedad** (MAP-Elites), no sólo por
  puntuación, para no converger a un solo diseño.

## 6. Procedencia

Todo en la rama principal, carpeta `experimentos/evo/`, con una etiqueta git `evo-gen{g}` por generación (decidido antes
de correr; una rama aparte se separaría del registro). Cada generación: `experimentos/evo/gen{g}/` con los ocho
candidatos, sus hipótesis, `puntuaciones.json` y el ganador (si lo hay). `LINAJE.md` acumula el árbol. El sha de este
preregistro va en el commit que lo introduce.

**Precisión del operador ciego (v0, escrita antes de correr):** sólo escala constantes de coma flotante del cuerpo de
`run()` por un factor `U(0.5, 2)`; la inversión de comparaciones queda para una versión posterior. Se declara para que
el control no se lea como más débil o más fuerte de lo que es.
