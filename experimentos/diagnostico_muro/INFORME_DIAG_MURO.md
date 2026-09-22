# INFORME — Diagnóstico del muro (H-MURO, "pastoreo selectivo")

**Veredicto en una línea: H-MURO SE SOSTIENE** (P1, P2 y P3 pasan en 6/6 semillas; P4 pasa 6/6 y con un
margen enorme) — con una corrección importante a la premisa original: **NADA NO "limpia" el mundo** (su
propio mundo ya es ~85 % malo); lo que sostiene la hipótesis es la versión **comparativa**: cuanto mejor
discrimina el cuerpo, más malo es el mundo que hereda.

## Qué hice

1. Leí las reglas del mundo (`organismo_f9c.py`/`organismo_vivo.py`): `spawn()` sortea el tipo del objeto
   nuevo UNIFORME entre A/B/C/D tanto tras una mordida como tras la renovación aleatoria
   (`if rng.random()<.003 and objs: ...` — un objeto al azar, sin mirar el tipo). Deriv é el estado
   estacionario (sec. "Fórmula" abajo).
2. Construí `organismo_f9c_muro.py` por ANCLAS desde `organismo_f9c.py` (sha `9dd1fb91ecec35ae`,
   `construye_muro.py`): 5 inserciones ADITIVAS (prefijo `mu9_`, sin tocar el rng ni ninguna variable
   existente) que miden presencia por tipo, ventana de fracción mala y su valor justo antes de cada muerte.
   Arnés `identidad_muro.py`: bit a bit idéntico en NADA/REL/ORÁCULO/RENACE (T=20000) y en REL a T=100000
   (156/156 muertes registradas) — **PASA, pegado abajo**.
3. Preregistré predicciones y umbrales (`PREREGISTRO_diag_muro.md`) usando un humo (T=5000/20000, semillas
   1-2) ANTES de la serie declarada.
4. Corrí `diag_muro.py` (semillas **2941-2946**, verificadas libres; T=100000; brazos NADA/REL/ORÁCULO con
   los kwargs EXACTOS de `corre_bloque2.BRAZOS`, mismo objeto importado — regla 14 trivial; `rep_acum=0`):
   18 corridas, un solo proceso, sin Pool, **208 s de CPU** (muy por debajo del techo de 25 min).
5. Reconstruí la tabla de vida (edad al primer parto, `l(x)`/`m(x)` agregados) de campos que YA EXISTÍAN
   (`vidas_h1`, `desc_por_vida`, `t_desc`) — cero instrumentación nueva para eso.

## Fórmula del estacionario (sec. 4 del preregistro)

Con `d=0.003` (prob./paso de renovar UN objeto al azar) y `β_X` la tasa de mordida por tiempo de presencia
del tipo X (`bites_X/presencia_X`, medida), y reposición SIEMPRE uniforme (1/4):

**f_X = (1/λ_X) / Σ_Y(1/λ_Y)**, con **λ_X = d/nobj + β_X** (nobj=4)

## P1–P4 (medianas de 6 semillas; 2941–2946, T=100000)

| # | medida | NADA | REL | ORÁCULO | umbral | veredicto |
|---|---|---|---|---|---|---|
| P1 | f_mala medida (presencia) | 0.8458 | 0.9027 | 0.9056 | ORÁCULO/REL > NADA en ≥5/6 sem. | **PASA 6/6 y 6/6** |
| P2 | \|medida − predicha fórmula\| | 0.0033 | 0.0034 | 0.0026 | ≤ 0.10 en las 18 celdas | **PASA 18/18** (máx. 0.0081) |
| P3 | f_mala 200 pasos antes de morir | 0.9225 | 0.9685 | 0.9630 | pre-muerte > global en ≥5/6 | **PASA 6/6 en los tres brazos** |
| P4 | q0 (muere sin parir) vs aporte extra | 0.87 vs ~0.002 | 0.65 vs 0.042 | 0.61 vs 0.060 | q0 domina | **PASA 6/6** |
| — | R0 medido (mediana) | 0.132 | 0.383 | 0.460 | (contexto) | — |
| — | causas de muerte (energía/agua) | 51/49 % | 42/58 % | 41/59 % | (se reporta) | agua algo más letal en los tres |

## Elasticidades (aritméticas sobre la tabla de vida; ORÁCULO, medianas de 6 semillas; sin correr nada nuevo)

| contrafactual | ΔR0 | R0 resultante |
|---|---|---|
| **(a) nadie muere antes del primer parto** (q0→0, cada cuerpo consigue su 1er parto) | **+0.607** | **1.060** |
| (b) el primer parto llega 20 % antes (solo en los que ya paren; tasa agregada post-parto medida) | +0.037 | 0.497 |
| (c) la fracción mala fuera la de NADA (recta de 2 puntos sobre las medianas de los 3 brazos) | **NO INTERPRETABLE**: pendiente positiva (0.132 con f_bad de NADA, es decir *bajaría*) — ver "predicción refutada" |

**La palanca que más movería R0, con enorme margen (~16×), es (a): la supervivencia hasta el primer parto**,
no la velocidad de esa primera reproducción ni "limpiar" el mundo. Mecanismo: el recién nacido arranca con
`E=Ag=0.6` (dote) y necesita 500 pasos **consecutivos** saciado (`rep_X=500`, `rep_acum=0`) para su primer
parto; en un mundo ~90 % malo esas rachas casi no se completan (q0 61-87 %). Esto conecta con un dato que
YA EXISTÍA en el bloque 2: `rep_acum=1` (ventana acumulada, no consecutiva) sube R0 en los tres brazos
(ORÁCULO 0.458→0.557) — la misma palanca, medida por otro lado, sin correr nada nuevo aquí.

## Predicciones propias refutadas / corregidas

- **La premisa "NADA muerde de todo y limpia" (parte (a) del encargo) queda REFUTADA tal cual**: el mundo de
  NADA ya es 84.6 % malo (no ~25 %). Lo que sobrevive es la versión comparativa (P1), no la fuerte.
  Causa medida: incluso un cuerpo sin nodo aprende aversión a B/D DENTRO de su propia vida corta por el
  mecanismo base de v14 (sin nodo ni linaje); el "muro" ya opera con la sola existencia de aprendizaje
  aversivo, el linaje sólo lo profundiza (Δ mediana ORÁCULO−NADA = 0.058 en f_mala, no un salto de 0.25→0.90).
- **Elasticidad (c), tal como la preregistré, es una comparación confundida**: en estos 3 brazos, un f_mala
  bajo (NADA) viene empaquetado con discriminación pésima (p1=0.19), así que la recta de 2 puntos da
  pendiente positiva (más mundo malo → más R0), lo opuesto de lo que H-MURO sugeriría si f_mala variara
  sola. Declarado como diseño insuficiente, no recalibrado a posteriori.

## Qué falló / qué queda

Falló: la elasticidad (c) tal como se diseñó (no hay forma de variar f_mala manteniendo el comportamiento
constante con sólo 3 brazos existentes; haría falta un brazo que fuerce composición del mundo sin tocar la
política). Queda: (i) un bloque que mueva `rep_X`/`rep_acum`/`dote` directamente sobre ORÁCULO para
confirmar que la palanca (a) es explotable de verdad (no sólo aritmética); (ii) instrumentar un control que
mantenga f_mala fija (p.ej. renovación dirigida por tipo) para separar "mundo malo" de "cuerpo bueno" y sí
poder leer (c) limpio.

## Arnés de identidad (pegado)

```
IDENTIDAD MURO · organismo_f9c (sha 9dd1fb91ecec35ae) vs organismo_f9c_muro (sha 72f1e5da62216d23) · T=20000
  OK   NADA     s1  extra=['muro']  falta=[]  dif=[]
  OK   NADA     s2  extra=['muro']  falta=[]  dif=[]
  OK   REL      s1  extra=['muro']  falta=[]  dif=[]
  OK   REL      s2  extra=['muro']  falta=[]  dif=[]
  OK   ORACULO  s1  extra=['muro']  falta=[]  dif=[]
  OK   RENACE   s1  extra=['muro']  falta=[]  dif=[]
T=100000 (REL s1): extra=['muro'] falta=[] dif=[]  muro.pasos=100000  muertes=156 (=b['deaths'])
TODO PASA en 41.3s
```

Datos: `datos/humo/diagmuro_s2941-2946_20260922_132032.json` (crudo, sha `f374daaa92d15379`) ·
`datos/humo/diagmuro_humo_20260922_131335.json` (humo) · script `diag_muro.py` (sha `29bf01d749d1871b`).
