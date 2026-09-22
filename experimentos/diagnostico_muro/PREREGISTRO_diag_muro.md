# PREREGISTRO — Diagnóstico del muro (H-MURO, "pastoreo selectivo")

Escrito antes de correr la serie declarada (semillas 2941-2946, T=100000). Ya se corrió un HUMO exploratorio
(arnés de identidad + T=20000/T=5000, semillas ya vistas 1-2) para verificar mecánica e instrumento; sus
números son hipótesis-generadores, no la medida. Esta letra se fija ANTES de mirar la serie declarada.

## 1. Hipótesis (firmada por el coordinador antes de medir)

H-MURO: en el mundo de fase 9 bloque 2 (`organismo_f9c.py`, 2 necesidades, 4 estímulos A comida/B veneno/
C agua/D sal), lo bueno (A, C) sale del mundo cuando se come (el organismo lo busca y lo muerde); lo malo
(B, D) sólo sale por renovación aleatoria del mundo (línea `if rng.random()<.003 and objs:`, que borra UN
objeto presente elegido al azar, sin mirar el tipo, y lo repone con `spawn()`, que sortea el tipo NUEVO de
forma UNIFORME entre los 4 — tanto tras una mordida como tras la renovación). Un cuerpo que evita bien lo
malo (ORÁCULO, REL) reduce su propia tasa de remoción de B/D casi a cero, mientras que A/C siguen saliendo
rápido (se comen). Con una tasa de reposición uniforme y una tasa de salida asimétrica, el mundo se llena de
lo malo. NADA (indiscriminado en el diseño, pero que aprende SU PROPIA aversión dentro de su propia vida
corta por el mecanismo base de v14 incluso sin nodo) debería mostrar el mismo sesgo pero MENOR.

## 2. Mecanismo mínimo y memoria nueva

Memoria nueva: CERO. La instrumentación (`organismo_f9c_muro.py`, ver `construye_muro.py`) sólo LEE el
estado que el organismo ya mantiene (`objs`, `mord`, y los campos de H1 `vidas_h1`/`desc_por_vida`/`t_desc`
que ya existían); no se añade ninguna regla de decisión, ningún peso nuevo, ningún canal.

## 3. Instrumento y anclas

- `organismo_f9c_muro.py`, generado por `construye_muro.py` desde
  `experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py` (sha `9dd1fb91ecec35ae`, SOLO LEÍDO). Cinco
  inserciones ADITIVAS (prefijo `mu9_`): presencia acumulada por tipo, ventana deslizante (200 pasos) de
  fracción mala, captura de esa ventana en cada muerte, y una clave nueva `muro` en el `return`. Ninguna
  variable existente, ni el consumo del rng, se toca.
- `identidad_muro.py`: compara `organismo_f9c.run` (origen) contra `organismo_f9c_muro.run` en NADA, REL,
  ORÁCULO, RENACE (semillas 1-2, T=20000, y una corrida T=100000): TODAS las claves existentes deben ser
  bit a bit idénticas (`N()` a los decimales de redondeo del propio proyecto); la única diferencia permitida
  es la clave nueva `muro`. Corre ANTES de mirar cualquier número del diagnóstico.
- Brazos: `corre_bloque2.BRAZOS['NADA']`, `['REL']`, `['ORACULO']` — el MISMO objeto dict importado, no una
  copia a mano (regla 14 trivial por construcción). `rep_acum=0` en las tres.
- Semillas: 2941-2946 (verificadas libres: fuera de los rangos reservados 2441-2940, 3001-3299, 4001-4199,
  5001-5020, 6001-6020; no aparecen como semilla de ninguna corrida previa del repo).
- T=100000 (igual que el bloque 2). Presupuesto: 18 corridas × ~15-20 s ≈ 5-6 min de CPU, un solo proceso,
  sin Pool; muy por debajo del techo de 25 min declarado para esta tarea.

## 4. Derivación analítica del estado estacionario (P2)

Sea `d = 0.003` la probabilidad por PASO (no por objeto) de que el mundo renueve un objeto al azar entre
los `nobj=4` presentes (línea de decaimiento de `organismo_vivo.py`/`organismo_f9c.py`); cada objeto
removido —por mordida o por decaimiento— se repone con un tipo sorteado UNIFORME entre los 4 (`spawn()`).
Tratando cada una de las `nobj` "unidades de presencia" como una cadena semi-Markov con tasa de salida
(hazard) por tipo `λ_X = d/nobj + β_X`, donde `β_X` es la tasa de mordida POR TIEMPO DE PRESENCIA del tipo X
(medida como `bites_X / presencia_X`, con `presencia_X = Σ_t n_X(t)` acumulada paso a paso por el
instrumento), y dado que la reposición es SIEMPRE uniforme (1/4) sin importar qué causó la salida, el
argumento de renovación (renewal-reward) da:

  **f_X = (1/λ_X) / Σ_Y (1/λ_Y)**   (fracción de presencia, en el tiempo, del tipo X)

Esta fórmula usa las tasas de mordida MEDIDAS en la misma corrida (no es una predicción out-of-sample
independiente: es una prueba de bondad de ajuste del MECANISMO propuesto — decaimiento uniforme + mordida
selectiva — contra la composición realmente observada). Si el mecanismo fuera otro (correlación espacial
fuerte, acoplamiento entre el objeto que se muerde y el que decae, etc.) la fórmula podría fallar por más
de ±0.10 pese a usar las tasas medidas de la misma corrida.

## 5. Predicciones (con rango) y umbrales de refutación

- **P1** (world composition): `f_bad = f_B + f_D` (fracción de PRESENCIA, tiempo-promedio) es MAYOR con
  ORÁCULO y REL que con NADA. Umbral: comparación PAREADA por semilla (mismas 6 semillas en los tres
  brazos) — se declara SOSTENIDA si `f_bad(ORACULO) > f_bad(NADA)` en ≥ 5/6 semillas Y
  `f_bad(REL) > f_bad(NADA)` en ≥ 5/6 semillas. Rango esperado (del humo, no vinculante): NADA ≈ 0.82-0.87,
  REL/ORÁCULO ≈ 0.87-0.92.
- **P2**: `|f_bad medido − f_bad predicho por la fórmula de la sec. 4| ≤ 0.10` en cada uno de los 18 pares
  (brazo, semilla).
- **P3**: la fracción mala promedio en los `W=200` pasos previos a cada muerte (`pre_death_bad`) es MAYOR
  que la fracción mala promedio de TODA la corrida (`f_bad medido`), por brazo. Umbral: mediana de
  `pre_death_bad` > mediana de `f_bad` en ≥ 5/6 semillas, para REL y ORÁCULO (NADA se reporta, sin umbral:
  su ventana de vida es tan corta que 200 pasos puede exceder su vida entera y el control es débil ahí).
- **P4** (tabla de vida, predicción DÉBIL declarada al 60 %): el déficit de R0 de ORÁCULO frente al
  reemplazo (1.0) está MÁS en `q0` (fracción de cuerpos que mueren sin parir nunca) que en la fecundidad
  condicional `E[D | D≥1] − 1` de los que sí paren. Operacionalización aritmética: se declara SOSTENIDA si
  `q0 · 1 > (1 − q0) · (E[D|D≥1] − 1)`, es decir, si "regalarle a cada cuerpo su primer parto" (contrafactual
  (a) de la sec. 6) sube R0 más que "regalarle a los que ya paren toda su fecundidad extra de golpe" — con
  ambos evaluados sobre las mismas 6 semillas de ORÁCULO.

## 6. Elasticidades (aritméticas, sobre la tabla de vida reconstruida; SIN correr nada nuevo)

Reconstrucción de la edad al primer parto por cuerpo a partir de campos YA EXISTENTES (`vidas_h1`,
`desc_por_vida`, ambos en orden cronológico H1, y `t_desc`, la lista global de tiempos absolutos de cierre
de ventana): un cuerpo con `desc_por_vida[i]=0` murió sin parir; para los demás, el primer `t_desc` dentro
de su ventana `[nace_i, nace_i+vida_i)` es su primer parto.

- (a) **nadie muere antes del primer parto**: cada cuerpo con `D=0` pasa a `D=1` (consigue exactamente su
  primer parto, nada más). `R0'_a = R0 + q0`.
- (b) **el primer parto llega 20 % antes** (sólo en los cuerpos que ya parieron): se libera
  `0.20 × edad1_i` de vida adicional tras el primer parto, a la tasa de fecundidad post-primer-parto YA
  observada de ese cuerpo (`(D_i−1)/tiempo_restante_i`); los cuerpos con `D=0` NO se tocan (no sabemos su
  edad al primer parto porque nunca ocurrió). Declarado como aproximación de primer orden.
- (c) **la fracción mala fuera la de NADA**: con sólo tres puntos (NADA, REL, ORÁCULO) se ajusta una recta
  `R0 ~ f_bad` sobre las medianas de los tres brazos y se interpola/extrapola el R0 de ORÁCULO si su
  `f_bad` fuera el de NADA. Declarado como una extrapolación lineal de dos puntos, débil por diseño (n=3);
  se reporta como orden de magnitud, no como estimación causal.

## 7. Control que puede fallar

El control es NADA mismo: si NADA (que en el diseño original "muerde de todo") mostrara la MISMA
`f_bad` que ORÁCULO/REL, H-MURO caería (P1 refutada) porque el sesgo del mundo no dependería de cuánto
discrimina el cuerpo. El humo exploratorio (T=20000, semilla 1) ya mostró que NADA también aprende A
EVITAR B/D dentro de su propia vida corta (mecanismo base de v14, sin nodo) y por eso puede no ser un
control "cero": se declara esto ANTES de la serie como limitación conocida, no se recalibra después.

## 8. Qué lo refuta

Si P1 falla (regla de la sec. 5), H-MURO cae como estaba escrita. Si P1 pasa pero P2 falla sistemáticamente
(> 0.10 en la mayoría de las 18 celdas), el sesgo de composición es real pero el MECANISMO propuesto
(decaimiento uniforme + mordida selectiva, sin correlación espacial) no lo explica del todo: H-MURO
queda PARCIALMENTE sostenida (el fenómeno existe, la fórmula no lo captura entero). P3 y P4 son
diagnósticos del CANAL causal (composición → muerte → R0), no de la hipótesis central; su caída no tumba
H-MURO pero limita cuánto explica.

## 9. Mini-prueba de un proceso con números (del humo, semilla 1, YA CORRIDA — no es la serie declarada)

T=20000, brazo REL, semilla 1: presencia `A=4602 B=36052 C=4096 D=35250` (total 80000=4×20000) →
`f_bad=0.891`. NADA (misma semilla, T=20000): `A=5983 B=32675 C=6282 D=35060` → `f_bad=0.847`. ORÁCULO
(semilla 1): `A=3813 B=38134 C=4551 D=33502` → `f_bad=0.895`. Orden ORÁCULO > REL > NADA, como predice
H-MURO, aunque el margen es más chico de lo que la hipótesis literal ("NADA limpia") sugiere — ver sec. 7.

## 10. Semillas

2941, 2942, 2943, 2944, 2945, 2946 — nuevas, verificadas libres por grep contra `datos/` y `registro/`.

Coordinador (creador), 22-sep-2026.
