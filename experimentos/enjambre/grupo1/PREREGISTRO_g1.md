# PREREGISTRO (borrador) — enjambre/grupo1, mecanismo M1: compartimentos de dos canales

MINI-EQUIPO 1 de la sala enjambre. Instrumento: `organismo_g1.py`, construido POR ANCLAS desde
`experimentos/creacion_A/organismo_v13q5.py` (`fae9c32b146fdbb4`, solo lectura) por
`experimentos/enjambre/grupo1/construye_grupo1.py`. Identidad `celdas=None` == original: **23/23** (ver
`identidad_g1.py`). Este documento es un BORRADOR de preregistro para la serie confirmatoria (semillas vírgenes,
pendiente de asignar por el coordinador) — **no** es el preregistro final, y ya incorpora lo que salió del
`mini_g1.py` (semillas 1–3, un proceso, T=100000), que por regla del proyecto NO cuenta como la serie.

## 1. Hipótesis

Partir la lectura de la vía lenta en **15 lectores lineales pequeños** — uno por cada par de píxeles
`(i,j)`, `i<j`, fijos al nacer, cada uno con 4 entradas `[P_i, P_j, P_i·P_j, 1]` — que aprenden EN PARALELO
con la regla delta que el tronco ya usa y compiten por su **propio** error de predicción (k-WTA, k=1; la vía
lenta lee solo al ganador), basta para que el organismo **enrute** el crédito hacia el par correcto de
píxeles en la regla XOR, sin construir ni destruir estructura y sin que ninguna señal nueva cruce entre
celdas (ninguna backprop en tiempo de ejecución: solo el refuerzo escalar `R` de cada mordida, el mismo que
la vía lenta ya usa).

Fundamento (dado por el jefe de investigación, no verificado por mí más allá de lo citado):
Caron, Ruta, Abbott & Axel (2013, *Nature* 497:113-117); Modi, Shuai & Turner (2020, *Annu. Rev. Neurosci.*
43:465-484); Dasgupta, Stevens & Navlakha (2017, *Science* 358:793-796); Lipshutz, Kashalikar, Farashahi &
Chklovskii (2023, PMC9934445).

## 2. Mecanismo y memoria (recordatorio técnico exacto)

Estado nuevo, nace con el organismo, nunca cambia de canales: `_PAR` (los 15 pares `(i,j)`), `_CW` (15×4,
peso de cada celda), `_CE` (15, error EMA propio de cada celda, `cel_rho=0.02`), `_CG` (índice de la celda
ganadora vigente). 76 números en total — la MISMA información que el brazo `seleccion='wta'` actual, repartida
en 15 lectores independientes en vez de uno solo. Por mordida, con `R` el refuerzo y `P` el patrón:

```
a_c = [P_i, P_j, P_i·P_j, 1]              (por cada celda c=(i,j), i<j)
d_c = R − W_c·a_c                         (residuo PROPIO de cada celda)
E_c ← (1−cel_rho)·E_c + cel_rho·d_c²      (primera vez: E_c = d_c², vía centinela E_c ≥ 1e9 del nacimiento)
W_c ← clip(W_c + eta_s·d_c·a_c, −clip_s, +clip_s)
ganadora = argmin_c E_c                   (la vía lenta lee SOLO esta celda)
```

Constantes fijadas antes de correr: `eta_s=0.15`, `clip_s=10` (v14.1 / A-4), `cel_rho=0.02` (A-4).

**Corrección mía al mecanismo, encontrada al construirlo (no cambia la regla, solo el nombre de una clave de
salida):** el ancla 5 propuesta por el jefe agregaba `celdas=celdas` al `return dict(...)`, pero
`organismo_v13q5` YA devuelve una clave `celdas=int(activa.sum())` (número de células de Kenyon activas —
capacidad/splits, nada que ver con el knob nuevo). Eso es `SyntaxError: keyword argument repeated` en Python,
no un fallo silencioso. Renombré el eco del knob a `cel_modo` (prefijo `cel_` ya usado por
`cel_rho`/`cel_ganadora`/`cel_E`); la `celdas` original (Kenyon) queda intacta. Ver
`construye_grupo1.py`, ancla 5, comentario en el código.

## 3. Instrumentos y arnés

- `construye_grupo1.py` — construye `organismo_g1.py` por 5 anclas desde `organismo_v13q5.py`.
- `identidad_g1.py` — `celdas=None` == original, TODAS las claves de `organismo_v13q5` (más `cel_modo=None,
  cel_ganadora=None, cel_E=[1e9]*15` siempre presentes y sin efecto). 6 configuraciones (BASE de la serie ×
  una config ALTERNA con las perillas viejas en su default) × 3 reglas × 3 semillas = 18, más mundo 'AB' × 3
  semillas y el chequeo de claves del brazo apagado = **23/23**, T=30000.
- `mini_g1.py` — un proceso, sin Pool, semillas 1–3, T=100000, `mundo='regla'`, `puerta=3`,
  `lectura='cuadratica'`, `regla_lenta='delta_signo'`, `constante=True`, `lam_lenta=0`, `eta_s=0.15`,
  `clip_s=10`, `celdas='par2'`, `cel_rho=0.02`, `lab=True`. `acc_lenta` = acierto balanceado por signo
  (`signo_acc`, la fórmula del registro) de `W_lenta_apriori` sobre los patrones de TEST nunca vistos.
  EXPOSICIONES: se recosechó `lab=True` **con la perilla encendida** (no se reusó el replay viejo cosechado
  bajo `delta_signo` estándar — riesgo #1 del mecanismo); el replay offline de mi propia `regla_local` sobre
  los eventos `(t,patrón,R)` pre-sonda se autocomprobó contra el `W_lenta_apriori` real del organismo: **9/9
  autocomprobaciones exactas (maxdif=0.0)**.

## 4. Predicción numérica del jefe (para la serie confirmatoria, semillas vírgenes 121–140 — NO corrida aquí)

`acc_lenta` xor01 mediana ≥ 0.75 y ≥0.75 en ≥ 9/20; `n*` ≤ 300; celda ganadora (0,1) en ≥ 15/20; px0 = 1.000
en 20/20; azar mediana en [0.35, 0.65].

## 5. Lo que salió en el mini_g1 (semillas 1–3, T=100000) — NO es la serie, y esto es lo importante

| regla | s1 | s2 | s3 | mediana | ganadora (0,1)/(0,j)/otro |
|---|---|---|---|---|---|
| xor01 | acc_lenta 0.625, cel (0,1) | 0.500, cel (0,1) | 0.375, cel (0,1) | **0.500** | **3/3 (0,1)** |
| px0 | 1.000, cel (0,2) | 1.000, cel (0,5) | 1.000, cel (0,3) | **1.000** | 0/3 (0,1); las 3 contienen el píxel 0 |
| azar | 0.300, cel (2,4) | 0.200, cel (2,5) | 0.500, cel (0,3) | **0.300** | 0/3 |

`n*(≥0.75)`: px0 en n=10–40 en las 3 semillas; xor01 y azar **no alcanzan 0.75** dentro de lo corrido
(hasta n_pre≈245–307 eventos pre-sonda por semilla).

Dos resultados que van en DIRECCIONES OPUESTAS y hay que reportar por separado:

1. **El enrutamiento funciona**: la celda (0,1) — el par P0,P1 correcto para XOR — gana en **3/3** semillas de
   xor01 (el criterio del jefe pedía ≥15/20 = 75%; 3/3 = 100% en esta muestra chica). k-WTA sobre 15 canales
   fijos SÍ encuentra el compartimento correcto.
2. **La calibración dentro de la celda NO alcanza el criterio**: aun ganando el par correcto, `acc_lenta`
   mediana = 0.500 (nivel de azar), por debajo del umbral de refutación declarado para la serie completa
   (`mediana < 0.625` ⇒ "M1 cae"). Con las MISMAS 4 entradas `[P0,P1,P0·P1,1]`, el control positivo de la
   sesión anterior (mínimos cuadrados exactos) llega a 1.000 en 10 exposiciones; la regla delta online de
   esta celda, con ~250-300 exposiciones, no. La diferencia no es el rasgo (ya está, y ya gana) — es la
   REGLA dentro de la celda: `eta_s=0.15`/`clip_s=10` se afinaron para el lector único de 21/22 rasgos
   (A-4), no para una celda de 4 entradas con recompensa asimétrica (`R_VAL`: comida +1.0, veneno −3.0) y
   pocas repeticiones por patrón.
3. **azar por debajo de lo predicho**: mediana 0.300, con 2/3 semillas en 0.2–0.3 (fuera de [0.35,0.65] y
   por debajo del azar puro). Esto es exactamente el riesgo #2 que el jefe anticipó ("con 15 hipótesis
   compitiendo el sobreajuste puede dar por debajo del azar de forma sistemática"): elegir la celda de MENOR
   error de tren entre 15 candidatas, con pocos patrones y etiquetas verdaderamente aleatorias, selecciona
   para sobreajuste al ruido del tren, que anticorrelaciona con el test. Con solo 3 semillas no se puede
   separar señal de ruido aquí — hace falta la serie completa.

Nota aparte (no bloquea nada): en mis 3 semillas, `split_regla` siempre deja ambas clases en tren (comida y
veneno, `ntr=(4,4)` fijo por construcción — estructuralmente no puede quedar una clase entera fuera del
`tren` de xor01). Esto no calza obviamente con la nota del jefe sobre "una clase XOR ausente del tren" en
6/20 semillas 1–20 (incluidas semillas 1 y 2) — puede que esa nota se refiera a mordidas/exposición real y no
a la partición `tren`/`test` en sí. Lo dejo señalado para que el coordinador lo revise contra su propia
medición; no lo investigué más a fondo.

## 6. Mi predicción corregida para la serie confirmatoria (121–140), con las MISMAS constantes

Con `eta_s=0.15`/`clip_s=10` sin cambios: espero que la mediana de `acc_lenta` en xor01 NO llegue a 0.75 (mi
estimación puntual, de solo 3 semillas: entre 0.45 y 0.65), que la celda ganadora sea (0,1) en una fracción
alta (≥15/20 me parece alcanzable — 3/3 en la mini-prueba), y que azar necesite las 20 semillas para saber si
0.300 fue ruido de muestra chica o un sesgo sistemático por debajo del azar. **No** recomiendo correr la
serie de 121–140 todavía con estas constantes tal cual: antes valdría la pena una barrida chica (3 semillas,
un proceso) de `eta_s`/`clip_s` DENTRO de la celda ganadora sola (o `cel_rho`), ya que el cuello parece estar
ahí y no en el enrutamiento.

## 7. Refutación y cláusulas

Cláusula del jefe (para la serie de 20): si la mediana de xor01 < 0.625, o la ganadora es (0,1) en < 12/20,
M1 cae. **Con 3 semillas la mediana ya está en 0.500 (< 0.625)** — no es la serie y no cuenta como
refutación formal, pero es una señal de alerta real, no humo: hay que decidir si la serie corre igual (para
tener el número real con n=20) o si primero se ajustan las constantes de la celda. Ganadora (0,1) 3/3 NO
refuta la parte de enrutamiento del mecanismo.

## 8. Coste

`identidad_g1.py`: T=30000 × 23 corridas, interpretado, ≈ decenas de segundos. `mini_g1.py`: T=100000 × 9
corridas (celdas='par2', interpretado, ~8-9s cada una) + replay offline (barato) ≈ 77s en total, un proceso,
sin Pool. Sin `--rapido` (el gemelo compilado `organismo_v13q5_rapido.py` no tiene la perilla `celdas`).
