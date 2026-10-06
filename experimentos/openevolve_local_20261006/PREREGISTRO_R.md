# PREREGISTRO — BRAZO R: réplica de la búsqueda con el proponente original (local, 6-oct-2026; escrito ANTES de toda corrida de búsqueda)

Misión: llegar a la AGI por este camino; el método manda. Esto es **evolución de programas guiada por un modelo de lenguaje sobre un juez
fijo**. No es selección natural, ni "el organismo aprendió", ni "la selección cruzó el muro". Encargo del director del 6-oct: "busquemos
llegar con eso otra vez".

## 1. Pregunta e hipótesis
El humo del 5-oct (1 corrida) produjo un programa que cruza (HUMO: mayoría en 19/20 y 20/20 semillas nuevas). La serie de la nube del
6-oct no lo repitió (A, B, H: 0/5), pero su proponente no era el del humo (ERR-194).

**Hipótesis H-R:** desde la misma raíz (O1 sin limpieza, sha 50b2fc3241da), con el adaptador ORIGINAL del humo y el proponente razonando
largo (≥ 10 000 tokens de salida por llamada), 30 iteraciones vuelven a producir un programa que cruza por mayoría en semillas selladas
nuevas. **Nula:** el humo fue suerte de una corrida y la búsqueda no lo repite aunque el proponente sea el mismo.

## 2. Qué difería el adaptador de la nube (medido, no supuesto)
Original: `C:\Users\User\Documents\PROYECTOS\JUACO-OPENEVOLVE\adaptador_claude.py`, sha b1ae88ae6b769bfb (idéntico a
`exploratorio/openevolve_humo_20261005/adaptador_claude.py`). Reconstruido: `experimentos/openevolve_serie/adaptador_claude.py`, sha
65351ea62d0b.

| | ORIGINAL (humo) | RECONSTRUIDO (nube) |
|---|---|---|
| modelo que resolvió el alias `sonnet` | **claude-sonnet-5** (único en `modelUsage`) | **claude-sonnet-5-5**, más una llamada interna a claude-haiku-4-5 |
| `--safe-mode` | **sí** | **no** |
| prompt de sistema | `--system-prompt-file <archivo temporal>` | `--system-prompt <texto por argv>` |
| ejecutable | `claude.exe` por ruta (npm) | `claude` del PATH |
| `--max-budget-usd` por llamada | 2.0 | 1.0 |
| reintentos | 1, con 10 s de espera | ninguno |
| carpeta de trabajo | `JUACO-OPENEVOLVE\cwd_neutro` (vacía, fuera del repo) | carpeta vacía en `/tmp` |
| esfuerzo / razonamiento | **ninguna bandera**: lo que traiga el entorno y `~/.claude/settings.json` (hoy en este PC: `effortLevel: xhigh`; la sesión que lanza trae `CLAUDE_EFFORT=high`) | **ninguna bandera**: `CLAUDE_EFFORT=high`, `MAX_THINKING_TOKENS=31999` del entorno de la nube |
| común | `-p --model sonnet --no-session-persistence --output-format json --tools "" --strict-mcp-config --disable-slash-commands`, prompt por stdin | igual |

Ninguno de los dos fija el esfuerzo ni el razonamiento por bandera. Las diferencias que pueden explicar 15 900 contra 1 800 tokens son
**el modelo** (el alias apuntaba a otro modelo en la nube), **el modo seguro** y **la configuración de la máquina**. No se sabe cuál
de las tres; este brazo no las separa: usa las tres como en el humo y verifica el resultado (§3, G1). Comprobado hoy: en este PC, con
las banderas del original, `sonnet` sigue resolviendo a `claude-sonnet-5`.

## 3. Instrumento (construido por anclas: `construye_instrumento.py`; nada editado a mano)
- **Pista, juez, revisa_carro y O1 sin tocar** (se importan): pista 9f47c65e438e0ff4, juez 6a68f640a7832f12, revisa_carro
  1c8a789f7427ab96, O1 99436afa2715f028. Fundador NO limpio (ERR-191). OpenEvolve 0.4.0, Python 3.14, numpy 2.4.3 (el venv del humo).
- **Proponente:** `adaptador_libro.py` carga por ruta el archivo ORIGINAL (aborta si el sha no es b1ae88ae6b769bfb) y sólo añade
  alrededor un libro de gasto por llamada (`gasto/libro_gasto.jsonl`) y un tope global (40 USD equivalentes; se paga con la
  suscripción). Banderas, ejecutable y carpeta de trabajo: los del humo, literalmente.
- **Config:** `config_R1.yaml` = `config_humo.yaml` con `random_seed` 45 y el párrafo final de "EL OBJETIVO" reescrito para decir la
  verdad sobre las etapas nuevas. Población, islas, diff, `max_tokens`, timeout y el resto del prompt: iguales.

**CAMBIOS DE INSTRUMENTO respecto del humo y de la nube (declarados aquí, antes de correr; hallazgos del auditor del 5-oct; candidato a
ERR-196, lo numera el coordinador):**
- **(a) El ctx ya no trae la tabla.** La pista entrega `ctx['fabrica']` (con `EFECTO` y `VAL_VIVO`) y `ctx['PAT']`. Ahora el carro
  recibe sólo `id, indice, n_linajes, T, L, rng, dote, rep_umbral, costo, costo_a, rep_X, cupo, ancho` (envoltura en `corre_carro.py`;
  la pista no se toca). Además el filtro veta por texto `fabrica`, `PAT`, `EFECTO`, `VAL_VIVO`, `bit_generator`, `np.load`,
  `fromfile`, `memmap` y parientes. Ninguno de los 85 programas evaluados en el humo y en la nube usaba nada de esto (grep).
- **(b) Un módulo por linaje.** Antes los 9 linajes compartían la instancia del módulo (canal oculto por estado de módulo o de clase).
  Ahora cada linaje carga la suya. El filtro veta además toda escritura sobre un módulo importado (`np.x = …`).
- **(c) Varias semillas de búsqueda por etapa:** 1 en la etapa 1, **2** en la 2 y **3** en la 3 (antes 1 / 1 / 1); se promedia.
- **(d) ERR-195: la etapa 2 exige nacimientos reales.** "Cría" = linaje con 0 extinciones tras t 10 000 **y** ≥ 2 nacimientos reales.
  Pasa a la etapa 3 sólo si la media de "cría" es ≥ 5/9. El inmortal que no pare ya no llega al piso 0.30.
- Lo que NO cambia: la fórmula `base` de la etapa 3, los umbrales `[0.04, 0.20]`, la regla de tabla y lo que vuelve al modelo.

**Puntaje (brazo R):**
- etapa 1: filtro y T 5 000 → 0.05 si corre, 0 si no;
- etapa 2: `b2 = media{[0.4·sin_extinción/9 + 0.4·cría/9 + 0.2·min(R0,1)]·(1 − muertes voluntarias)}` → `0.20 + 0.10·b2` si pasa,
  `0.05 + 0.10·b2` si no;
- etapa 3: `0.30 + 0.70·media{base}`, con `base = [0.5·persisten/9 + 0.4·cruzan/9 + 0.1·min(R0,1)]·(1 − muertes voluntarias)`.

**Residuo conocido (no lo cierra el filtro):** mutar por llamada a método un objeto de una librería compartida (por ejemplo
`np.typecodes.update(...)`). Se cubre leyendo el código del mejor antes del examen (§7).

**Identidad (corrida antes de mirar números; `identidad.py`, salida en `identidad_salida.json`):** con las perillas apagadas,
`corre_carro.py` es igual al origen campo a campo (RAIZ y HUMO, T 5 000, incluido el estado del rng del mundo); con las perillas
encendidas RAIZ y HUMO dan la misma física; el evaluador con `BRAZO=ORIGEN` devuelve las mismas métricas y artefactos que el del origen
en 81 resúmenes físicos de la corrida A de la nube.

**Cordura (`cordura.py`, salida en `cordura/cordura_salida.json`; resultados en §10):** C1 filtro, C2 envoltura, C3 ancla de O1 en
883001/883002 con el instrumento nuevo, C4 ERR-195.

**Puertas antes de la serie:**
- **G1 (ERR-194):** en el humo de tubería de R1 (1 iteración, semillas de práctica) la salida del proponente es ≥ 10 000 tokens. Si
  no, la serie no arranca (`corre_brazo.py` lo impide) y se reporta. Aviso: en el humo 8 de 30 llamadas bajaron de 7 000 (mínimo
  4 074), todas tardías; las 5 primeras dieron 15 900–26 600. Una sola llamada es una puerta ruidosa; durante la serie se vigila la
  **mediana** (`avance.py` avisa si baja de 10 000 con ≥ 5 llamadas).
- **G2:** identidad PASA y cordura PASA.

## 4. Semillas (ninguna de 270xxx–277xxx ni 883xxx salvo el ancla; 281xxx y 282xxx no aparecen en el árbol: grep del 6-oct)
| uso | semillas |
|---|---|
| R1, búsqueda (`random_seed` 45) | etapa 1: 281101 · etapa 2: 281111, 281112 · etapa 3: 281121, 281122, 281123 |
| R2, búsqueda (`random_seed` 47) | etapa 1: 281301 · etapa 2: 281311, 281312 · etapa 3: 281321, 281322, 281323 |
| práctica (no cuentan) | 281901–281903 y 281921–281923 (tubería), 281950–281953 (cordura), 281990–281991 (identidad y humo del examen) |
| **EXAMEN SELLADO** | **282001–282020** (serie) · **282021–282040** (réplica del examen) |
| ancla de reproducción (reuso declarado) | 883001, 883002: sólo para comprobar que O1 da su registro |

## 5. Corridas
1. **R1:** 30 iteraciones, tope de 33 llamadas. `corre_brazo.py R1 --desacoplado`.
2. **R2 (réplica de la búsqueda):** igual, con sus semillas. Se lanza después de R1 (o a la vez si el coordinador mide que el PC aguanta).
   Sin R2 no hay "repetible": una corrida más sólo sube la cuenta de 1 de 3 a 2 de 4.
3. **Examen** (`corre_examen.py --desde 282001`, lo corre el coordinador): MEJOR_R1, MEJOR_R2 (si existe), HUMO, O1 y RAIZ en las 20
   selladas, T 100 000. El "mejor" es el `best` de OpenEvolve al cerrar, congelado con su sha antes del examen.

## 6. LA LETRA
"Con mayoría" = cruzan_real ≥ 5 de 9 en una semilla. M(programa) = semillas con mayoría, de 20.

**Validez (si falla, NO SE LEE):** V1 examen completo · V2 M(O1) ≥ 6 (registro: 16 y 17 de 20) · V3 M(RAIZ) ≤ 1 (registro: 0) ·
V4 M(HUMO) ≥ 15 (registro: 19 y 20; ancla del instrumento nuevo en semillas nuevas) · V5 los programas examinados pasan el filtro
ampliado y su código fue leído (§7).

**Una réplica "cumple"** si M(MEJOR_Rk) ≥ 15/20. Nulo de la puerta: RAIZ, 0/20; el umbral queda a 15 semillas del nulo (regla 15).

- **FUNCIONA:** R1 **y** R2 cumplen.
- **HAY ALGO MODESTO:** cumple exactamente una; o ninguna cumple pero las dos tienen M ≥ 5. Con sólo R1 corrida y cumpliendo: MODESTO,
  "falta la réplica".
- **NO:** lo demás.
- Regla 12: si una réplica queda en 14, 15 o 16, su examen se repite en 282021–282040 y vale el menor.

Descriptivo, no decide: suma de linajes que cruzan contra O1 y contra HUMO, pareado por semilla; iteración del primer cruzador;
mecanismo (limpieza redescubierta = mordidas malas ≥ 10 × RAIZ; otra cosa se describe).

## 7. Qué sería "sospechoso de trampa" (entonces PRIMERO se lee el código y el veredicto queda en suspenso)
`corre_examen.py` lo marca solo: cruzan 9/9 en ≥ 18 de 20 semillas · mediana de R0 real > 1.15 en alguna semilla · muertes voluntarias
> 0 · contabilidad del juez no coherente · cruza **sin** la firma de limpieza (mordidas malas < 10 × RAIZ) · cruza con vida mediana
> 20 000 · cruza con el mundo sin comida < 0.01 del tiempo (O1 da 0.04). Además, a mano: puntaje ≥ 0.90 en las iteraciones 1–2;
cualquier lectura del ctx por clave armada (`'fab' + 'rica'`), o llamadas que muten objetos de numpy/math/collections.
En todos los casos el mejor de cada brazo se lee entero antes del examen: es una lectura de ~200 líneas.

## 8. Controles que pueden fallar
- **RAIZ** en el examen (suelo: si cruza, el mundo regala el cruce).
- **HUMO** en el examen con el instrumento nuevo (si cae de 15/20, el ctx limpio o el módulo por linaje le quitaban algo: no se lee).
- **Tramposos** T1–T7 (cordura): si alguno puntúa, el instrumento no está cerrado.
- **INMORTAL_B** en la etapa 2 (cordura): si pasa, ERR-195 no está cerrado.
- **La nube como control histórico del proponente corto:** A y B, 0/5 con ~1 800 tokens. No es un control limpio (otro modelo, otro
  puntaje): si R1 cumple, la lectura "era el proponente" es compatible, no demostrada.

## 9. Predicciones firmadas (antes de correr la búsqueda)
| # | predicción | valor o rango | p |
|---|---|---|---|
| R-1 | G1: primera llamada de la tubería ≥ 10 000 tokens de salida | 12 000–25 000 | 0.80 |
| R-2 | mediana de tokens de salida de R1 en las 30 llamadas | 10 000–20 000 | 0.75 |
| R-3 | R1 escribe limpieza (mordidas malas ≥ 10 × RAIZ en su mejor) | — | 0.85 |
| R-4 | mejor puntaje de búsqueda de R1 | ≥ 0.80 (rango esperado 0.55–0.97) | 0.50 |
| R-5 | R1 cumple (M ≥ 15/20) | M esperado 0–20, bimodal | 0.45 |
| R-6 | R1 y R2 cumplen (FUNCIONA) | — | 0.25 |
| R-7 | iteración del primer programa que llega a la etapa 3 | 6–20 | 0.60 |
| R-8 | gasto equivalente de R1 | 5–9 USD | 0.75 |
| V | bloque FUNCIONA / MODESTO / NO / NO SE LEE | — | 0.25 / 0.40 / 0.30 / 0.05 |

Por qué no más de 0.45 para R-5: el humo es 1 de 1 con este proponente; la etapa 2 nueva quita la meseta de 0.30 donde el humo estuvo
8 rondas antes de añadir el "banco" (ahora ese tramo puntúa 0.09, sin etapa 3), y eso puede ayudar o estorbar: no se sabe.

**Qué refuta H-R:** R1 y R2 con M < 5 teniendo G1 cumplida y mediana de tokens ≥ 10 000. Entonces el humo fue suerte de una corrida y
la línea "la búsqueda lo encuentra" se cierra.

## 10. Cordura y humo de tubería (se completa ANTES de lanzar R1; no cuentan)
Corrido el 6-oct entre 14:34 y 15:09, un proceso de pista a la vez, antes de lanzar ningún brazo:
- **Identidad: PASA.** RAIZ y HUMO, origen contra copia con perillas apagadas: ningún campo difiere; con perillas encendidas, ninguno
  tampoco. Evaluador: 81 resúmenes (30 / 30 / 21 por etapa), 0 distintos.
- **Cordura: PASA** (C1–C4).
  - C1: O1, RAIZ, HUMO e INMORTAL_B pasan el filtro; T1, T2, T4, T5 y T6 rechazados; T3 y T7 pasan el texto, como se esperaba.
  - C2: T3 lee la tabla sin envoltura (`agua, comida, sal, veneno`) y con envoltura da `KeyError 'fabrica'`; T7 queda con un banco por
    linaje (con módulo compartido, uno con los tres).
  - C3: O1 con el instrumento nuevo, 883001: cruzan 5/9, R0 0.9032, causas 71/83/25/30; 883002: 8/9, 0.963, 99/60/32/45. Ningún campo
    difiere del registro.
  - C4: INMORTAL_B en la etapa 2 nueva puntúa 0.0567 y no pasa; HUMO 0.2786 y pasa (cría 6 y 8 de 9). **Aviso:** en estas dos
    semillas INMORTAL_B tampoco habría pasado con la fórmula del origen (0.05 y 0.073): la corrida no distingue las dos puertas.
    Lo distingue `cordura_err195_registros.py` sobre los registros: de los programas que el origen dejó pasar, la puerta nueva
    frena 5 de 13 en el humo, 12 de 12 en A y 5 de 5 en B (ninguno cruzó después), y **0 falsos negativos** (no frena a ninguno que
    luego cruzara con mayoría).
- **Tubería R1** (281901–281903, 1 iteración, 341 s): raíz 0.0533; **proponente 14 763 tokens de salida, modelo claude-sonnet-5 →
  G1 PASA**; el hijo es un inmortal que no pare (vida 25 000, cría 0/9) y queda en 0.09 sin pasar a la etapa 3: ERR-195 cerrado en vivo.
- **Tubería E** (281911–281913, 1 iteración, 567 s): HUMO puntúa **0.7722** en la etapa 3 (cruzan 8/9, sin nada bueno 0.217): dentro
  de 0.55–0.90, hay sitio para mejorar. Proponente 12 635 tokens, claude-sonnet-5.
- **Humo del examen** (`corre_examen.py --humo`): escribe `examen/humo/resumen.json`.
- Gasto de las dos tuberías: 0.35 USD equivalentes (`gasto/libro_gasto.jsonl`).
- Reloj medido hoy con el PC ocupado por procesos ajenos: O1 a T 100 000 tarda ~280 s (ayer ~172 s).

## 11. Las cuatro trampas
- Canal simétrico: la pizarra existe y es legal; los 9 linajes usan el mismo programa, no hay emisor y receptor que confundir. No aplica.
- Acierto sin balancear: no hay tasas de acierto; se cuentan linajes con R0 real ≥ 0.9 (juez, física).
- Mundo que se come la comida: aplica. Se reporta `frac_sin_bueno_mundo` de cada programa junto al cruce (HUMO 0.24, O1 0.04). Es el
  objetivo del brazo E.
- Sitios fijos: los objetos reaparecen en casillas al azar y los cuerpos renacen en casillas al azar. No aplica.

## 12. Regla de parada
30 iteraciones, 33 llamadas o 40 USD equivalentes en el libro común; lo que llegue primero. Un veredicto distinto de FUNCIONA no se
arregla con más rondas sin preregistro nuevo. Siguiente ERR libre: 196.

Firmado: creador (Claude), 6-oct-2026, antes de lanzar R1.
