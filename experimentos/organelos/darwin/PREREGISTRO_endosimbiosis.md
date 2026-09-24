# PREREGISTRO: ENDOSIMBIOSIS, escalón 1 (organelos, Opus B, 24-sep-2026; antes de cualquier serie)

Misión: llegar a la AGI por este camino. Frente 2 (ECO). Carpeta: `experimentos/organelos/darwin/`. No se modificó ningún archivo existente.

Palabras del director: *"la célula humana y la evolución de sus organelos… ¡solo selección natural! Hay que romper el molde."*

Lo que se busca: órganos que llegan de AFUERA y que nadie diseña como órganos.
- En el mundo de ECO viven, además del bicho, replicadores libres: proto-organelos con genoma propio.
- El bicho puede tragarse uno.
- Si el tragado sobrevive adentro, se hereda, sigue mutando y actúa sobre su anfitrión por un canal genérico.
- Sólo la selección natural decide si la fusión se queda.

## 0. Instrumento (sha a 16; los verifica `corre_endo.py` en cada log)

**Orígenes (sólo se leen):**
- `juaco_eco/motor_eco3.py`, 2eec9830792d9822.
- `juaco_eco/carros/FABRICA_ECO.py`, f1163009cb5193a2.
- `juaco_eco/corre_eco.py`, 47d9cee4d6462116 (de aquí sale `eco_cfg('VIDA')` para el bicho).

**Construido por anclas:** `construye_endo.py` (750c9ced2c3d7631) produce:
- `motor_endo.py` (7e10329cf0cb9fd0): motor_eco3 con ganchos G1–G5;
- `carros/FABRICA_SIMB.py` (38ac0ddba8829c88): FABRICA_ECO con UNA línea, `Vb += obs['simb'][letra]`.

**Código nuevo:**
- `simbiontes.py`: la ecología de los libres, tragar, herencia, canal y los brazos;
- `corre_endo.py`: el runner y la letra.

Sha del código nuevo: `simbiontes.py` **72f8829defe3e69f**, `corre_endo.py` **078734369e9721c5**, `identidad_endosimbiosis.py` **42f458cbbfbe3bc8** (los del humo 5; los imprime cada log).

**Arnés `identidad_endosimbiosis.py`: 15/15**, un proceso, 123–133 s. Salida en `identidad_endosimbiosis_salida.txt`.

| caso | qué comprueba |
|---|---|
| (F) | las anclas reproducen los archivos |
| (A1–A4) | con `simb=None`, motor_endo == motor_eco3 **bit a bit**: eco VIDA con vivero y corte, eco AZAR, eco del juez y eco=None |
| (B) | FABRICA_SIMB sin canal == FABRICA_ECO |
| (C) | con libres vivos y sin tragar, el bicho == motor_eco3 bit a bit: los libres **no se comen la comida** (trampa 3) |
| (D1) | en INERTE el canal está apagado de verdad |
| (D2) | en VIDA_S el canal actúa |
| (E) | determinismo |
| (G1/G2) | guardia de ERR-60 |
| (H) | contabilidad de eventos |
| (I) | BARAJADO baraja y AZAR_S sortea |
| (J) | la pérdida ocurre |

**nube-9, corregido en dos capas:**
- en el motor, con `simb` la guardia de 100 000 cuerpos por linaje NO lanza: se registra (`err60`, `t_trunc`) y la corrida termina ahí (arnés G2). Con `simb=None` lanza lo mismo que motor_eco3 (G1);
- en el runner, cada trabajo atrapa `BaseException` (SystemExit incluido) y escribe su JSON con `error`, así que el Pool no se cuelga. Una corrida truncada por ERR-60 se informa en las guardias.

## 1. Hipótesis
- **H-F (la fusión se queda por selección):** tras el corte, los linajes cuyo simbionte ACTÚA:
  - persisten más que los de simbionte inerte y que los que no tragan;
  - y los que nacen con simbionte tienen más hijos que los que nacen sin él, más de lo que pasa con un simbionte inerte o con uno libre al azar.
- **H-D (el simbionte se domestica):** el genoma que el bicho transmite en sus partos diverge de sus parientes libres (del mismo instante) en la dirección que le sirve al anfitrión. Diverge más que bajo herencia sin selección y más que sin canal.

## 2. Mecanismo mínimo y memoria nueva (detalle en el docstring de `simbiontes.py`)

**Libres.**
- Genoma g ∈ ℝ⁶, en el espacio de la retina del mundo (los 4 patrones de 6 píxeles).
- Se pegan a un objeto con afinidad a = σ(g·P) y comen el exudado sin quitar el objeto: F·a/m, con m = libres en la celda.
- Pagan c0 + c2·|g|² por paso.
- Se parten con e ≥ 1 y el hijo muta (p 0.25 por componente, N(0, 0.3)). Mueren con e ≤ 0 o con p 0.001 por paso.
- Tope computacional: 60·esc.

**Tragar.** Por contacto en la misma celda, con p_trag 0.005 por paso. Con p_queda 0.25 el tragado sigue vivo adentro (un solo simbionte por cuerpo). Si no, se digiere: E += 0.02.

**Alojar.** Cuesta 0.0001 de E por paso, el 10 % del costo basal: la fusión tiene que pagarse sola.

**Pérdida** (pedido del coordinador, trinquete de Fable D3). El simbionte muere adentro con p_pierde 1e-4 por paso y no pasa al hijo con p_falla 0.05 por parto.

**Herencia vertical.** El hijo recibe una copia mutada con la misma regla de los libres. En el vivero, el banco de donantes del motor guarda, alineado con cada genoma de padre, el simbionte de ese padre.

**Canal** (genérico y simétrico en signo). El simbionte lee la letra que el cuerpo tiene en la boca y suma k·tanh(g·P[letra]), con k = 1, a Vb (la entrada de la boca, antes de la sigmoide). El signo y la letra salen del genoma del libre. **No codifica la respuesta.**

**Memoria nueva.**
- **En el cerebro, cero:** un término aditivo.
- En el cuerpo, un genoma de 6 números más su caché de 4 números.
- Por libre, 6 números, la energía y la posición.

**El bicho** es FABRICA_ECO y evoluciona como VIDA de ECO en los 5 brazos: 25 genes, p_mut 0.05, banco 200, 8 sombras.

**Mundo:** w30 (esc 30, 30 fundadores, L 1200), quimiostato de ECO, tope de 3000 cuerpos. T 120 000, corte 60 000; sin checkpoints.

**Brazos:**

| brazo | qué cambia |
|---|---|
| **VIDA_S** | todo lo de arriba |
| **INERTE** | tragado, costo y herencia iguales; el canal no actúa |
| **BARAJADO** | en cada parto y en cada fundador, el genoma heredado se sustituye por el de un libre al azar (la presencia sí se hereda) |
| **SIN_TRAGAR** | p_trag = 0 |
| **AZAR_S** | herencia sin selección: el estado del simbionte de cada cuerpo nuevo sale al azar de un anillo de 200 estados NUEVOS. Esos estados son el de cada cuerpo nuevo, el de cada adquisición y un "ninguno" por cada pérdida interna, y la entrada sale mutada |

## 3. Medidas (`corre_endo.medidas`)
- **area_post:** suma de los cuerpos vivos en las muestras (cada 1000 pasos) con t ≥ corte. Es la persistencia de la población de anfitriones, continua y sin empates por extinción.
- **delta_r0:** hijos medios de la cohorte nacida en [corte, T_ef − 20 000] **con** simbionte al nacer, menos los de la cohorte **sin** él. Exige ≥ 5 cuerpos por grupo; si no, la semilla no es evaluable.
- **D:** media, sobre cada transmisión en un PARTO con t ≥ 10 000 (vivero incluido; los fundadores del vivero no cuentan), de I(genoma transmitido antes de mutar) − I medio de los libres en la muestra de ese mismo instante.
  - I(g) = [tanh(g·A) + tanh(g·C) − tanh(g·B) − tanh(g·D)]/4. Es balanceado: 2 letras buenas y 2 malas, y llegan en mezcla uniforme.
  - D compara con los libres **del mismo instante**, así que no se contamina con la deriva de los libres.
- **Descriptivas, no deciden** (trinquete): la fracción con simbionte tras el corte (`prev_post`), D sólo tras el corte, la distancia de genomas adentro contra libres en T y la tasa de mordida por letra con canal y sin él.

## 4. Predicciones firmadas (antes de la serie)

**ERR-123 (coordinador, 24-sep ~14:20, ANTES de la serie; auditoría juaco-auditor: LISTO CON CORRECCIONES, H-1).**
- La medida D cambió de forma después de ver los humos de práctica: pasó de "transmisiones tras el corte" a "partos de toda la
  corrida contra los libres del mismo instante", pareada contra AZAR_S e INERTE. Por la regla 11 lleva ERR aunque no haya serie.
- Los humos usaron sólo semillas de práctica (22990–22999). El auditor verificó que no se solapan con la serie ni con la réplica.
  No encontró sesgo hacia FUNCIONA.
- H-2 del auditor (identidad sólo a T ≤ 6000): el coordinador corre `identidad_escala_endo.py` (A1 y C a T 120 000, corte
  60 000, semilla 22995) antes de la serie. Si no da 2/2, no hay serie.

Dato visto antes de escribir esto, declarado. Todo es de UNA semilla de práctica y sin valor:
- humo 1 (22990, ecología v1, T 40 000): los libres se extinguieron;
- humos 2–5 (22993, ecología final, T 80 000, corte 50 000; la dinámica es idéntica en los cuatro, sólo cambió la medida D):
  - tras el corte viven de 1 a 4 cuerpos;
  - area_post: VIDA_S 108, INERTE 82, BARAJADO 56, SIN_TRAGAR 99, AZAR_S 47;
  - prev_post: VIDA_S 0.62, INERTE 0.37, AZAR_S 0.62;
  - D: VIDA_S −0.021, INERTE −0.029, BARAJADO +0.025, AZAR_S +0.113;
  - delta_r0 VIDA_S −0.43 (7 contra 47 cuerpos).

| cantidad (por ventana de 20) | rango predicho | P(pasa ≥ 15/20) |
|---|---|---|
| P1a area_post VIDA_S > INERTE | 8–14 | 0.15 |
| P1b area_post VIDA_S > SIN_TRAGAR | 8–15 | 0.20 |
| P2a delta_r0 VIDA_S > INERTE (pareado, evaluables 4–14) | 2–9 | 0.03 |
| P2b delta_r0 VIDA_S > BARAJADO | 2–9 | 0.03 |
| P3a D VIDA_S > AZAR_S | 7–14 | 0.20 |
| P3b D VIDA_S > INERTE | 8–15 | 0.25 |
| **fracción bajo DERIVA** (AZAR_S prev_post, mediana; pedido 3 del coordinador) | **0.40–0.80** | — |
| fracción INERTE (mediana) | 0.15–0.55 | — |
| fracción VIDA_S (mediana) | 0.25–0.75 | — |
| semillas de AZAR_S o INERTE con fracción ≥ 0.9 (trinquete residual) | 0–4 | P(≥ 10) = 0.08 |
| placebo BARAJADO: D de un solo signo | 6–14 | P(≥ 15) = 0.04 (nominal) |

**La fracción bajo DERIVA, en cuentas.** Tomo el equilibrio de encuentro y pérdida sin selección: π\* ≈ λ/(λ + p_pierde + p_falla/τ).
- λ es la adquisición por cuerpo y paso, medida en los humos: ~1.3e-4.
- τ es el tiempo de generación, ~2000 pasos.
- Queda π\* ≈ 1.3/(1.3 + 1.0 + 0.25) ≈ 0.51. La copia desde el anillo la sube un poco: el humo dio 0.62.
- Una fracción ≥ 0.9 en AZAR_S delataría que la pérdida no alcanza.

**Veredicto por ventana:** FUNCIONA 0.01 · HAY ALGO MODESTO 0.25 · NO 0.54 · NO EVALUABLE 0.20. Mi apuesta es **NO**.

La razón está en los humos: FABRICA en w30 queda en 1 a 4 cuerpos tras el corte, así que P1 y P2 tienen poco poder. P3 usa los partos de toda la corrida y es la pregunta con poder.

## 5. Controles, y cómo puede fallar cada uno
- **INERTE** (P1a, P2a, P3b). Falla si el simbionte sin canal da la misma persistencia, el mismo delta o el mismo D que VIDA_S. En ese caso el efecto sería de la digestión, del costo o del sesgo de adquisición, no del canal.
- **BARAJADO** (P2b y placebo de D). Falla P2b si un libre al azar sirve igual que el linaje propio. Como placebo, si D sale de un solo signo en ≥ 15/20 el instrumento de D está sesgado: NO EVALUABLE.
- **SIN_TRAGAR** (P1b). Falla si sin tragar la población persiste igual.
- **AZAR_S** (P3a, trinquete). Falla P3a si la herencia sin selección da el mismo D. En particular, el **sesgo de adquisición** (el bicho se para sobre A y C, así que traga libres con I alto) sube D sin selección, y AZAR_S y INERTE lo llevan igual. Si AZAR_S o INERTE llegan a una fracción ≥ 0.9 en ≥ 10/20 semillas: NO EVALUABLE (trinquete).

## 6. La letra (`corre_endo.veredicto`)
Todas las comparaciones son pareadas por semilla y estrictas. Una semilla sin dato en cualquiera de los dos brazos no cuenta a favor. Umbral: ≥ 15/20 (P = 0.021 bajo p = 0.5).
- **P1:** P1a **y** P1b.
- **P2:** P2a **y** P2b.
- **P3:** P3a **y** P3b.

**NO EVALUABLE**, por cualquiera de estas causas:
- serie incompleta o con `error`;
- bloqueados > 0;
- tope de los libres en ≥ 5 corridas;
- libres extintos antes del corte en ≥ 5 semillas de VIDA_S;
- trinquete (arriba);
- placebo de D de un solo signo en ≥ 15/20;
- en INERTE, delta_r0 > 0 en ≥ 15/20 (el estado "con simbionte al nacer" estaría confundido).

**Veredictos:**
- **FUNCIONA — LA FUSIÓN SE QUEDA POR SELECCIÓN Y EL SIMBIONTE SE DOMESTICA:** P1, P2 y P3.
- **HAY ALGO MODESTO:** 1 o 2 de las tres.
- **NO:** ninguna.

El bloque se declara si serie y réplica dan el mismo veredicto; si no, vale el menor. Vocabulario: «la fusión se queda», «el simbionte diverge de sus parientes libres»; prohibido «evoluciona un órgano», «organelo» como hecho y «especie».

## 7. Qué refuta
- **H-F:** P1 y P2 caen en las dos ventanas; o area_post de VIDA_S queda por debajo de INERTE en ≥ 15/20 (el canal daña).
- **H-D:** P3 cae en las dos ventanas; o D de VIDA_S queda por debajo de AZAR_S en ≥ 15/20 (el anfitrión arrastra al simbionte hacia su vida libre).
- **El instrumento:** cualquier NO EVALUABLE de §6.

## 8. Semillas NUEVAS (grep del 24-sep: 22001–22040 sin uso como semilla en el repo)
- **Serie 22001–22020; réplica 22021–22040.** RESERVADAS, sin correr.
- Práctica 22990–22999:
  - 22990, humo 1;
  - 22991–22992, prueba del Pool (coordinador);
  - 22993, humos 2–5;
  - 22994, arnés;
  - 22996–22997, exploración de viabilidad de los libres.

## 9. Costo y comandos (sólo el coordinador lanza `--serie` y `--prueba_pool`)
- **Por corrida:** ~2.5 min de vivero y ~0.5 min después del corte (medido: 80 000 pasos en 126–144 s).
- **Por ventana:** 100 corridas ≈ 5 h de CPU, es decir **Pool 3 ≈ 1.7–2.2 h** y **Pool 6 ≈ 0.9–1.2 h**.
- **Serie + réplica:** Pool 3 ≈ 3.5–4.5 h; Pool 6 ≈ 1.8–2.4 h.
- Comandos:
  - `python experimentos/organelos/darwin/identidad_endosimbiosis.py` (15/15 antes de lanzar);
  - `python experimentos/organelos/darwin/corre_endo.py --prueba_pool --pool 2`;
  - `python experimentos/organelos/darwin/corre_endo.py --serie --ventana serie --pool 3`, y después `--ventana replica`.
- Humo 5 (final, shas de §0): `datos/humo/endo_humo_20260924_135039/HUMO_endosimbiosis.json`, 582 s, los 5 brazos, todo ejercitado.
