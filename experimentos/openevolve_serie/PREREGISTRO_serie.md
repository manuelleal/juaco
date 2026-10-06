# PREREGISTRO — SERIE OpenEvolve sobre la pista de JUACO (nube, 6-oct-2026; escrito ANTES de las corridas de búsqueda y del examen)

Misión: llegar a la AGI por este camino. Esto es **evolución de programas guiada por un modelo de lenguaje sobre un juez fijo**: no es
selección natural del organismo, ni "la selección cruzó el muro". Convierte en serie el humo exploratorio del 5-oct
(`exploratorio/openevolve_humo_20261005/`, un solo humo, sin réplica ni controles). Encargo del director del 6-oct, con un presupuesto
duro de 30 USD en total.

## 1. Pregunta
Partiendo del mismo organismo que colapsa (`raiz/programa_inicial.py` = O1 sin limpieza, sha 50b2fc3241da510e, igual al del humo), ¿la
búsqueda de 30 rondas con Sonnet produce **de forma reproducible** (2 corridas independientes con semillas de búsqueda nuevas) un programa
que, en **5 semillas selladas nuevas**, haga cruzar a la mayoría de los linajes? ¿Y la misma búsqueda con el **modelo más pequeño
disponible (Haiku 4.5)**? Lectura del director: si el modelo débil también cruza, el mérito no es de la búsqueda con el modelo grande. El
problema lo resuelve cualquier modelo con este prompt, que ya describe la física.

## 2. Instrumento (fijado antes de correr; commit `c47482c0` de la rama `nube/openevolve-20261006` y este)
- **Pista, juez y revisa_carro sin tocar** (sólo se importan): `pista.py` 9f47c65e438e0ff4, `juez.py` 6a68f640a7832f12, `revisa_carro.py`
  1c8a789f7427ab96 y `carros/O1.py` 99436afa2715f028, comprobados el 6-oct. Fundador NO limpio (`fundador_limpio=0`, ERR-191).
- `evaluador.py` y `corre_carro.py`: copias del humo. Sólo cambian dos cosas:
  - la ruta de Windows pasa a ser relativa al repo;
  - las semillas de búsqueda se leen de `JUACO_OE_SEM`, sin valor por defecto.

  El puntaje, la cascada, los umbrales `[0.04, 0.20]`, la regla de tabla y lo que vuelve al modelo son los del humo
  (`PREREGISTRO_humo.md` §3–4).
- `config_A.yaml`, `config_B.yaml` y `config_H.yaml`: el `config_humo.yaml` con estos cambios:
  - A: `random_seed` 43;
  - B: `random_seed` 44;
  - H: `random_seed` 43 y el modelo `haiku` en lugar de `sonnet`.

  El system prompt, la población, las islas, el diff, `max_tokens` y el timeout no cambian.
- OpenEvolve 0.4.0 (PyPI), Python 3.13.12, numpy 2.4.3. `lanza.py` sin cambios. Cada corrida usa 1 evaluación a la vez; las 3 corridas van en
  paralelo (4 núcleos) porque el tiempo no es medida aquí.
- **`adaptador_claude.py` RECONSTRUIDO** (declarado). El original del humo (sha b1ae88ae6b769bfb) no está en ninguna rama del repo.
  - **Igual que el humo (§2 de su preregistro):**
    - `claude -p`, sin herramientas (`--tools ""`), sin MCP ni skills, sin persistencia de sesión;
    - el system prompt del YAML reemplaza al de Claude Code;
    - corre en una carpeta vacía, así que no ve el repo ni su CLAUDE.md.
  - **Nuevo:**
    - el prompt va por stdin;
    - salida en JSON, para leer el costo de cada llamada;
    - `--max-budget-usd 1.0` por llamada;
    - **tope duro de gasto global de 20 USD** en llamadas al modelo: lo suman las 3 corridas en `gasto/libro_gasto.jsonl`, y al
      cruzarlo toda llamada nueva falla;
    - tope de 33 llamadas por corrida (30 + 3), como en el humo.
  - Lo que no se sabe del original: las banderas exactas y cómo pasaba el prompt. Es una diferencia de instrumento con el humo y se
    reporta como tal.
- **Cordura (corrida antes de este preregistro; `cordura/`):**
  - O1, T 100 000, anclas 883001 y 883002: cruzan **5/9** (R0 0.9032; causas 71/83/25/30) y **8/9** (0.963; 99/60/32/45). Es idéntico
    al registro (ancla del humo, paso A del muro).
  - CTRL_O1_SINLIMPIA: **0/9 y 0/9**.
  - Tramposos: marcos de Python (`sys._getframe`) y `getattr`/dunder, **rechazados por revisa_carro**; tabla escrita a mano,
    **rechazada por la regla de tabla**.
  - El que miente en `salida()` pasa el filtro y da **la misma física que la raíz campo a campo**, con el mismo estado final del rng
    del mundo en T 25 000 ×2: la mentira no cuenta.
- **Humo de tubería** (1 iteración, semillas de práctica 274901–274903, no cuenta): la primera llamada a Sonnet costó 0.065 USD y
  tardó 30 s. Se completa en §9.

## 3. Puntaje
El del humo, sin cambios:
`base = [0.5·persisten/9 + 0.4·cruzan_real/9 + 0.1·min(med R0 real, 1)] × (1 − frac. muertes voluntarias)`, con la cascada
5 000 / 25 000 / 100 000.

## 4. Semillas
**Búsqueda** (las ve el bucle):
| corrida | modelo | `random_seed` | etapa 1 / 2 / 3 |
|---|---|---|---|
| **A** (réplica 1) | Sonnet | 43 | 274101 / 274102 / 274103 |
| **B** (réplica 2) | Sonnet | 44 | 274201 / 274202 / 274203 |
| **H** (CONTROL, modelo débil) | Haiku 4.5 | 43 | 274101 / 274102 / 274103 (pareada con A) |

- Anoche se usaron 271001–271003 y `random_seed` 42.
- Práctica (humo de tubería): 274901–274903.

**Examen SELLADO: 275001, 275002, 275003, 275004, 275005** (T 100 000, fundador no limpio). El bucle y el modelo nunca las ven.
- Ya gastadas, no se usan: 272001 y 272002, el examen del humo. **272003 también se da por gastada**, porque estaba en la lista sellada
  del humo y su examen quedó a medias.
- Comprobación (grep en todo el árbol el 6-oct, ramas incluidas vía `main` actual): 27410x, 27420x, 27490x y 27500x no aparecen como
  semilla en ningún campo `seed`/`semilla`/`--desde` ni en nombres de archivo. Las únicas coincidencias son números dentro de JSON de
  datos de ECO y de n9b, que no son semillas.

## 5. Corridas (en este orden de prioridad)
1. **A y B** (réplicas): 30 iteraciones cada una, con tope de 33 llamadas.
2. **H** (control de modelo débil): 30 iteraciones, con tope de 33 llamadas.
3. **Examen** (`corre_examen.py`, Pool 3) de 6 brazos en las 5 selladas, 30 corridas:
   - el mejor programa de A, de B y de H (el `best` de OpenEvolve al cerrar, congelado);
   - **HUMO**, el mejor del humo (`examen/mejor_programa.py`), fuera de muestra en semillas nuevas;
   - **O1**, como techo;
   - **RAIZ**, como suelo.
- **Presupuesto:** tope de 20 USD en llamadas (adaptador) y ≤ 10 USD estimados para la coordinación, que no se puede medir desde dentro.
  Si la proyección tras 5 iteraciones pasa del tope, **se recorta la réplica B y nunca el control H** (orden del director). El examen no
  gasta en el modelo.

## 6. LA LETRA
Una semilla sellada es **"con mayoría"** para un programa si cruzan_real ≥ 5/9 (juez).

**Un programa "cumple"** si tiene mayoría en **≥ 4 de las 5** selladas.

**Validez (si falla, NO SE LEE):**
- V1: O1 tiene mayoría en ≥ 3/5 selladas. O1 dio 2/9 en una semilla de calibración del humo; el techo se lee en la misma semilla.
- V2: RAIZ no tiene mayoría en ninguna (0/5).
- V3: el examen está completo (30/30 corridas sin fallo).
- V4: todos los programas examinados pasan el filtro de reglas (revisa_carro + regla de tabla).

**Veredicto:**
- **FUNCIONA:** A **y** B cumplen, **y** H NO cumple. Lectura: la búsqueda con el modelo grande reencuentra de forma reproducible un
  programa que cruza, y el modelo débil con el mismo presupuesto no.
- **HAY ALGO MODESTO** en cualquiera de estos casos:
  - (i) A y B cumplen y H también cumple: la tubería reproduce, pero el mérito no es del modelo grande;
  - (ii) sólo uno de A o B cumple;
  - (iii) ninguno cumple, pero el mejor de A y el de B superan a RAIZ en las 5 selladas (más linajes que cruzan).
- **NO:** todo lo demás.
- **Si B se recorta por presupuesto:** el máximo es MODESTO, porque no hay réplica.

**Descriptivo** (no decide): suma de linajes que cruzan en las 5 selladas, de cada mejor contra O1, y pareado por semilla. HUMO fuera
de muestra: ¿cumple?

## 7. Mecanismo (para cada ganador, antes de leer el código se fija cómo se clasifica)
- **"Limpieza redescubierta":** el código tiene una regla explícita que muerde letras ya conocidas como dañinas (valor medio negativo)
  cuando la reserva lo permite. Firma física en el examen: `mordidas_malas` ≥ 10 veces las de RAIZ en la mediana de las selladas.
- **"Trampa del simulador":** cualquier lectura de estado fuera de `obs`, o un efecto que no se explica por la física de la pista. Si
  pasa el filtro pero hay trampa, se anota como ERR.
- **"Otra cosa":** cruza sin la firma de limpieza. Se describe en palabras.

## 8. Predicciones firmadas (antes de las corridas)
| # | predicción | p |
|---|---|---|
| Q1 | A cumple | 0.65 |
| Q2 | B cumple | 0.65 |
| Q3 | H cumple | 0.30 |
| Q4 | HUMO cumple fuera de muestra (≥ 4/5) | 0.60 |
| Q5 | O1 con mayoría en ≥ 4/5 selladas | 0.60 |
| Q6 | los ganadores de Sonnet que cumplan usan limpieza redescubierta | 0.80 |
| Q7 | algún mejor de Sonnet suma más linajes que cruzan que O1 en las 5 selladas | 0.45 |
| Q8 | gasto total en llamadas al modelo ≤ 12 USD | 0.75 |
| V | serie FUNCIONA / MODESTO / NO / NO SE LEE | 0.30 / 0.40 / 0.22 / 0.08 |

**Por qué FUNCIONA sólo tiene 0.30:** el humo halló el programa en la ronda 12–13 de 30, así que una réplica puede no encontrarlo. Y
Haiku, con el prompt que describe la física, puede encontrarlo también: eso da MODESTO (i).

## 9. Humo de tubería (no cuenta; agregado tras el commit 00defd3e y ANTES de lanzar A, B y H)
1 iteración, semillas 274901–274903, 150 s de reloj: OpenEvolve carga, el adaptador llama a Sonnet (`claude-sonnet-5-5`; el CLI usa
además Haiku para una llamada interna mínima), el diff se aplica y la cascada evalúa (etapas 1 y 2; el hijo no pasa a la 3).
Costo: 0.065 USD en una llamada (8 920 tokens de entrada en caché y 2 395 de salida) → ~2–5 USD por corrida de 30 iteraciones.

## 10. Regla de parada
- Cada corrida se detiene a las 30 iteraciones, con 33 llamadas o con 20 USD globales; lo que llegue primero.
- No hay más corridas después del examen. Un veredicto distinto de FUNCIONA no se "arregla" con más rondas sin preregistro nuevo.
- Siguiente ERR libre: **ERR-194**.

Firmado: Claude (sesión nube), 6-oct-2026, antes de lanzar A, B y H.
