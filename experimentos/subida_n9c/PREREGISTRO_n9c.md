# PREREGISTRO — nivel 9, tanda 3: ¿persiste un linaje del organismo propio con flujo fijo de comida? (subida_n9c, 23-sep-2026, creador)

Misión: llegar a la AGI por este camino. Escrito DESPUÉS de dos humos de práctica (14191, 14192) y ANTES de cualquier serie.
Carpeta: `experimentos/subida_n9c/`. Sólo se escribe aquí; `generaciones/`, `carrera_escuderias/`, `subida_n10/` y los
congelados sólo se leen. **Recomendación del creador: prioridad BAJA (ver §9). El humo predice NO para la pieza del nivel.**

## 0. Diagnóstico previo (solo lectura de series selladas; no es dato nuevo)
- **Por qué O1 persiste y O3 no** (serie 10101–10120, crudo `6289126525058479`, individuos con t_nace ≥ 10000, mediana por semilla):

| carro | R0 fundadores | vida fundadores | R0 nacidos | vida nacidos | persiste |
|---|---|---|---|---|---|
| O1 | 0.019 | 200 | 0.897 | 1851 | 14/20 |
| O4 | 0.019 | 200 | 0.918 | 2176 | 3/20 |
| O3 | 0.560 | 345 | 0.743 | 2373 | 0/20 |
| O2 | 0.475 | 887 | 0.723 | 1796 | 0/20 |
| FABRICA | 0.167 | 106 | 0.119 | 99 | 0/20 |

  En v2, cuando un linaje se extingue, el mundo pone un fundador limpio (P3). Por eso «persistir» exige que los
  descendientes le ganen el nicho a un flujo continuo de fundadores ingenuos. Los fundadores de O1 no son viables:
  prueban una letra desconocida solo con min(E, Ag) > 0.5 y nacen con 0.6, así que la primera mordida mala los deja en 0.2
  y no pueden volver a probar. Sus descendientes, que heredan la tabla, tienen un R0 de ~0.9.
  Los fundadores de O3 son casi tan buenos como sus hijos: sin esa asimetría, los 9 linajes derivan y todos se extinguen.
  **Limpiar no explica por sí solo la diferencia:** O2 es el que más limpia (11 objetos en el mundo, 67 llegadas perdidas) y persiste en 0/20.
- **El organismo propio en v2** (subida_n10 12301–12320): los nacidos mueren en un 99–100 % por veneno o sal, **aun con la tabla verdadera**
  (ORÁCULO: R0 0.553, 590 de 593 muertes por B/D en una semilla). La boca decide con el valor aprendido de la fila activa
  contra un sesgo de hambre (`Vb = 1.2·w + 2·hambre + 0.5`). Un recién nacido (0.6/0.6) muerde lo malo que ya conoce.

## 1. Hipótesis
- **H-P (la pieza del nivel):** con una boca que **predice su propio estado** tras morder (modelo directo del cuerpo con
  el efecto sentido por letra) y con esa memoria heredada en el parto, un linaje de FABRICA **persiste** con flujo fijo
  de comida: al menos 1 linaje sin fundadores tras t = 10000 y con ≥ 5 nacimientos, en ≥ 15/20 semillas.
- **H-NICHO (mecanismo; la que puede fallar en las dos direcciones):** con el MISMO organismo, la boca que se protege a sí
  misma **tapa el mundo** de objetos malos: se pierden llegadas del quimiostato y queda menos comida. La boca de FABRICA,
  que no se protege, deja el mundo limpio pero muere de lo que muerde. Limpiar es un bien público que la protección
  individual destruye.

## 2. Mecanismo mínimo y memoria nueva (construye_n9c.py v2, 9 anclas sobre FABRICA.py `2ebee3e99ea5a33a`)
- `BOCA='predice'`: si el cuerpo ya mordió la letra, predice su déficit total D = Σ clip(1 − nivel, 0, 1) tras morder,
  usando la media de dS **sentida**, y usa como valor el **código de recompensa del tronco** (+1 si D baja, −3 si sube, 0
  si no cambia). El sesgo de hambre, la temperatura y **el mismo uniforme** no cambian. Si la letra nunca se mordió,
  decide FABRICA. **Sin constantes nuevas y sin rng nuevo.**
- `HER='memoria'`: el padre vivo pasa en el parto su memoria de efectos. `HER='cruz'` pasa la misma memoria con dE y dAg intercambiados.
- **Memoria nueva declarada:** 4 letras × 3 números por cuerpo, la misma forma que la memoria de letras de APR. Los fundadores siguen limpios.
- **Brazos** (monocultivo de 9, L = 360, 36 objetos, T = 100000):

| brazo | papel |
|---|---|
| **NADA** | ancla; == FABRICA bit a bit |
| **PRED** | la boca que predice, sin herencia; control que puede ganar |
| **CAND** | candidato |
| **CRUZ** | control de contenido que puede ganar |

## 3. Instrumento y anclas
- **Mundo:** `generaciones/pista2.py` `4d2bee16e7961261` + `motor_convive.py` `d10cb9021f5d0f41`, sin cambios, con quimiostato r_rep 0.03 y tope 300.
- **Juez:** `resumen_linaje` de `corre_convive.py` `e6dadfdad9c379cd`, importado.
- **Carros:** NADA `d4853da9c6ed9a82`, PRED `4a1ea0844b31c837`, CAND `d5b2b9390e782a70`, CRUZ `822cea5ec7d95b94`.
- **Scripts:** runner `corre_n9c.py` `3a9f66ec33628a50` (el mismo sha que corrió el humo v2), arnés `identidad_n9c.py` `26277f363ed2c82a`,
  lector `lee_nicho.py` `796ab5eecdfae06f`, calibración `calibra_ancla.py` `f25d00698fb0aac8`.
- **Arnés 43/43** (`identidad_n9c_salida.txt`):
  - NADA == FABRICA en 6 configuraciones;
  - la herencia es inerte antes del primer parto;
  - canal y boca por unidad, con el mismo uniforme;
  - determinismo;
  - en marcha;
  - regla 14 campo a campo contra `corre_convive.tarea`;
  - ERR-115 (20 formas malas abortan; `--help` real sale con error sin escribir);
  - la letra del veredicto en 7 casos.
- **Ancla calibrada antes de semillas nuevas (ERR-116)** con `calibra_ancla.py`: bootstrap de dos etapas sobre NADA de
  n10 12301–12320 (`bbc9291c9a1059e6`), IP 99 % de la mediana → **V-ANCLA: mediana R0_nacidos NADA ∈ [0.090, 0.155] y NADA persiste ≤ 2/20.**

## 4. Semillas (NUEVAS)
Práctica 14191–14199 (usadas: 14191 humo v1 y arnés; 14192 humo v2; 14193–14194 arnés). **Serie 14101–14120. Réplica 14121–14140.**
Verificado con grep en `bundle` y en los worktrees `anclado, aprende, carrera, convive, criterio, escuela, exploracion, fanin, respaldo, sandbox`:
- en .py/.md no aparece ningún número de 141xx;
- en .json/.log/.txt no aparece como `"seed": 141xx`, `semilla 141xx`, `_s141xx`, `--desde 141xx` ni `seed=141xx`;
- en los nombres de archivo solo aparecen sellos de hora.

`corre_n9c.py` aborta con cualquier otro rango.

## 5. Predicciones firmadas (creador, tras los humos)
| medida (mediana de 20) | NADA | PRED | CAND | CRUZ |
|---|---|---|---|---|
| persiste (letra estricta, semillas) | 0–1 | 0–2 | **0–2** | 0–2 |
| R0_nacidos | 0.09–0.155 | 0.00–0.30 | 0.00–0.30 | 0.00–0.30 |
| nacimientos por semilla | 350–600 | 5–60 | 5–60 | 5–60 |
| malos_mundo (B+D medios) | 14–19 | 27–33 | 27–33 | 27–33 |
| buenos_mundo (A+C medios) | 5–7.5 | 3–5 | 3–5 | 3–5 |
| perdidas (llegadas perdidas en T) | 0–400 | 6000–14000 | 6000–14000 | 6000–14000 |
| vida_fund | 95–115 | 150–260 | 150–260 | 150–260 |

**Resultados que espero:**
- **G1** (la pieza) **FALLA con probabilidad 0.97.** Es mi predicción central: el humo v2 (CAND, 14192, T = 50000) dio 4 nacimientos, 0 hijos de nacidos, el mundo con 30.7 de 36 objetos malos y 5070 llegadas perdidas.
- **G2 y G3 fallan** (p 0.9): con tan pocos nacimientos la herencia no tiene dónde actuar. Además, `R0_nacidos` es None en las semillas sin nacidos, que el pareado salta.
- **H-NICHO se sostiene** (p 0.85; `lee_nicho.py`, §5b).
- **Veredicto por la letra esperado: NO.**

### 5b. H-NICHO por la letra (`lee_nicho.py`, pareado PRED contra NADA)
| condición | qué exige |
|---|---|
| N1 | malos_mundo mayor en ≥ 15/20, con diferencia mediana ≥ +8 |
| N2 | buenos_mundo menor en ≥ 15/20 |
| N3 | perdidas mayores en ≥ 15/20 |
| N4 | vida_fund mayor; informativa, no decide |

**SE SOSTIENE** si se cumplen N1, N2 y N3. **La refuta** que los malos no suban (diferencia < +8 o < 15/20): en ese caso,
proteger el cuerpo no tapa el mundo y el muro es otro (buscar).

## 6. Criterio por la letra (`corre_n9c.veredicto`, por serie; declarar exige serie Y réplica con el mismo veredicto, `--veredicto`)
**Condiciones de validez** (si alguna falla, la serie **NO SE LEE**):
- **V-ANCLA:** mediana de R0_nacidos de NADA dentro de [0.090, 0.155] y NADA persiste en ≤ 2/20.
- **V-TOPE:** 0 partos bloqueados en CAND.

**Puertas del candidato:**

| puerta | qué exige |
|---|---|
| G1 PERSISTE | CAND persiste (letra estricta) en ≥ 15/20 |
| G2 HERENCIA | CAND > PRED en R0_nacidos en ≥ 15/20 |
| G3 CONTENIDO | CAND > CRUZ en R0_nacidos en ≥ 15/20 |

**Veredicto:**

| veredicto | condición |
|---|---|
| **FUNCIONA** | G1 ∧ G2 ∧ G3 |
| **HAY ALGO MODESTO: PERSISTE SIN ATRIBUCIÓN** | G1 sin G2 o sin G3 |
| **HAY ALGO MODESTO: SUBE SIN PERSISTIR** | G2 ∧ G3 sin G1 |
| **NO** | el resto |

**Controles que pueden ganar** (se imprimen): C-PRED (PRED persiste en ≥ 15/20) y C-CRUZ (CRUZ persiste en ≥ 15/20).

## 7. Vocabulario
- **Permitido si sale NO + H-NICHO:** *"con flujo fijo de comida, el organismo propio no sostiene un linaje: si no se protege, muere de lo que muerde; si se protege prediciendo su propio estado, tapa el mundo y muere de hambre"*.
- **Permitido si sale FUNCIONA:** *"un linaje del organismo propio persiste con flujo fijo de comida, replicado, cuando hereda lo que el linaje sintió y lo usa para predecir su propio estado"*.
- **Prohibido:** «población» sin la medida al lado; «coopera»; «aprende a limpiar» (la limpieza aquí no se aprende; es una consecuencia de la regla); «evoluciona».

## 8. Puntos del nivel 9 que movería cada resultado (propuesta; decide el director)
| resultado (serie + réplica) | puntos |
|---|---|
| FUNCIONA ×2 | 50 → 80 (es la pieza central que el coordinador fijó) |
| MODESTO persiste sin atribución ×2 | +10 |
| MODESTO sube sin persistir | +3 |
| NO | 0 |
| H-NICHO se sostiene ×2 | 0 puntos: cierra con réplica la línea «la boca que se protege sola» y fija el muro del organismo propio (limpiar es un bien público) |

## 9. Historia en práctica (declarada; 6 corridas, 150 000 pasos, un proceso)
- **v1** (`practica_v1/`, humo 14191, T = 20000, 5 brazos, `66b5dd8b785b30ed`).
  - Diseño: boca por gradiente de la deriva (las dos filas pesadas por el déficit) + copia de los pesos del padre.
  - Resultado: R0_nacidos NADA 0.159, deriva 0.218, copia 0.216, las dos 0.255, cruzado 0.189. El 100 % de las muertes de nacidos fue por B/D.
  - **Refutado mi supuesto:** creía que leer las dos filas quitaba el veneno. Los valores aprendidos tras una mordida (−1.35) son chicos frente al sesgo de hambre, y el control cruzado casi empata.
- **v2** (este diseño, humo 14192, T = 50000, solo CAND, `581085983a8ad830`, 55 s).
  - Resultado: 4 nacimientos en 50 000 pasos. Los fundadores mueren a los 200 pasos. El mundo queda en 2.0 A, 15.0 B, 2.0 C y 15.7 D, con 5070 de 13 500 llegadas perdidas. Los nacidos mueren a los 600 pasos (de hambre).
  - **Refutado mi supuesto:** creía que un descendiente informado sería viable. Protegerse tapa el mundo.
- El cambio de v1 a v2 se hizo antes de escribir este preregistro (precedente: aprende_barrer v1→v3). No es enmienda, pero queda declarado.
- **No hay presupuesto de humo para un v3 con limpieza** (el límite de 6 corridas está agotado).
