# INFORME — gemelo compilado de JUACO-ECO (`motor_eco_rapido.py`), 24-sep-2026 (compilador)

Misión: llegar a la AGI por este camino; el método manda. Un gemelo que no sea bit a bit idéntico sólo explora.

**Etapa alcanzada: E1 + E2 + E3. Arnés `identidad_eco_rapido.py`: RESULTADO 120/120** (salida en `identidad_eco_rapido_salida.txt`, 341 s).

## Qué es y cómo se usa
- `motor_eco_rapido.run_solapadas(...)`: misma firma y misma salida (todas las claves) que `motor_eco.run_solapadas`, con el cerebro FABRICA / FABRICA_ECO, con `eco=None` y con `eco=dict(...)`.
- Desde corre_eco **sin cambiar su letra**: `corre_eco_rapido.py`.
  - Importa `corre_eco.py` tal cual y sólo cambia `CR.ME` por una copia de `motor_eco` cuyo `run_solapadas` es el del gemelo.
  - Banderas, `veredicto()`, `juez()` y `trabajo()` son las del original.
  - `ME_SHA()` añade al `RESUMEN.json` los sha del gemelo y del lanzador.
- Diseño:
  - Un núcleo `@njit(cache=True)` corre por tramos entre eventos de Python (muestra de genes, corte, checkpoint, fin).
  - Por ranura, cada cuerpo lleva arrays de física y cerebro y **su** `Generator` en una `numba.typed.List`.
  - El mundo es un `grid` más un árbol de Fenwick, que reproduce el orden de inserción del dict: desempates de `_see` y `list(objs)[i]` del olvido.

## Qué se delega (regla 9) y por qué
| pieza | a dónde | por qué |
|---|---|---|
| `np.exp` | el MISMO bucle 1-D float64 de NumPy, llamado por `ctypes` (se verifica al importar) | en esta máquina (AVX512) NumPy usa su exp vectorial, que **difiere de libm (el exp de numba) en 4.6 % de los argumentos** |
| `@` / `np.dot` | BLAS | el arnés comprueba 0 diferencias entre el BLAS de numba (OpenBLAS de SciPy 0.3.30) y el de NumPy (0.3.31.dev) en 90·90, 6·6, 90×6@6 y 2×9@9 |
| `Generator` | creados en Python; los de cada cuerpo y cada hijo, en `objmode` una vez por parto | numba no tiene `default_rng` / `SeedSequence`; toda extracción la hace numba sobre el estado C real de NumPy |
| banco, donante y mutación de genoma y sombras | `objmode`, con `ME.muta` y la lista `ES['banco']` del original | son las mismas líneas del original |
| empate en la frontera del top-3 de Kenyon | `np.argsort` en `objmode` | 4740 empates forzados en (P); 3 empates reales en la corrida 10071 |
| `_muestra_gen`, foto del corte, `ind_cb`, `salida()` del carro | Python, en las fronteras de tramo; `salida()` se calcula con una instancia real del carro | se usa el código del original |

Otras decisiones:
- Sumas: sólo hay sumas de 6 reales, de izquierda a derecha desde 0.0 como NumPy.
- No hay funciones recursivas.
- La prueba de caché en un proceso NUEVO da 0 compilaciones y 3/3 corridas idénticas al original.

## Qué cubre el arnés
Lo que se comparó:
- **(I) E1: 22 corridas y (E) E2: 34 corridas.** En cada una se comparó:
  - la salida completa;
  - la trayectoria de cada `actua` (hasta 148 157 por corrida);
  - el cerebro entero de cada cuerpo vivo, bit a bit;
  - el estado de su `Generator`;
  - el mundo final en orden;
  - las filas de `ind_cb` con su genoma.
- **Condiciones cubiertas:**
  - pisos, tope y bloqueados, `inmediata`, `rep_acum`;
  - n = 1, `escala=0`, `mundo_n` mayor y menor que n;
  - 40–66 divisiones por corrida, NK = 8 y NK = 90;
  - `memoria_rechazo` 5 y 80, genoma no entero;
  - VIDA, CEREBRO, AZAR y MUT0, `refunda=0`, vivero y corte.
- **(C) Checkpoints.** El estado completo del original coincide con el del gemelo en t = 1000, 2000 y 3000 (cuerpos, cerebros, genomas, sombras, mundo, todos los rng, banco).
  - Cortado y reanudado es igual a seguido.
  - Una firma ajena y los formatos cruzados abortan.
- **(X) El mundo de la serie** (esc 90, 90 fundadores): VIDA, AZAR y MUT0 coinciden.
- **(J) corre_eco:**
  - `juez()` con T_b 20 000 y `trabajo()` (T 12 000, checkpoint en 10 000) dan el mismo JSON que el original;
  - el "corte de luz" más `--reanuda` da lo mismo que la corrida seguida.

## Aceleración (máquina cargada con las series del coordinador; mismo mundo, en caliente)
| mundo | cuerpos | original | gemelo | factor |
|---|---|---|---|---|
| ECO (esc 90), VIDA / AZAR / MUT0 | 74–81 | 194–208 pasos/s (63–68 µs por cuerpo y paso) | 7 700–8 000 pasos/s (1.5–1.7 µs) | **×38–41** |
| pista v2, 9 FABRICA, T = 15 000 | 9.9 | 1 654 pasos/s | 125 062 pasos/s | **×76** |
| `trabajo()` completo | — | 52.1 s | 1.2 s | ×43 |

- La carga de la caché cuesta ~0.5 s por proceso.
- Proyección para el ECO largo (1e6 pasos), sin contar los partos:
  - ~3 min con N = 100;
  - ~8 min con N = 300;
  - ~28 min con N = 1000.
- Hoy el original tarda 3–32 h en esos mismos casos.

## Fuera de alcance / qué falta
- **Otros carros:** APR, O1–O4, … abortan con `ValueError`. También abortan T < 4 y los checkpoints del ORIGINAL.
- **Los checkpoints no se mezclan.** Una serie empezada con un motor se reanuda con el mismo; si no, aborta por firma.
- **No ejecuté la ruta con `Pool`** (`--serie`, `--largo`, `--prueba_pool` de `corre_eco_rapido.py`), por regla. Sólo probé `trabajo()` y `juez()` en proceso.
  - Primer paso sugerido para el coordinador: `corre_eco_rapido.py --serie --prueba_pool --desde 19031 --n 2 --pool 2`, con la caché ya creada por el arnés.
- **Costos que quedan:**
  - dgemv 2×9 de BLAS: ~165 ns por cuerpo y paso;
  - cada parto o refundación en `objmode`: ~70–90 µs. Lo domina `default_rng` en Python (~14 µs por Generator).
- **Validez:** vale para numpy 2.4.3, numba 0.67.0 y estas OpenBLAS. Hay que repetir el arnés tras cualquier cambio. Si cambian los sha fijados, el gemelo se niega a correr.

## Hallazgo (candidato a ERR, no verificado en otros gemelos)
- Con el `exp` de libm (control 97) o con suma ingenua (control 98), a T = 3000 **la salida y la trayectoria salen idénticas y sólo difieren los pesos**. Comparar salidas no detecta derivas de 1 ulp.
- `organismo_f9_rapido.py` y `organismo_v13_rapido.py` usan `np.exp` dentro de numba, es decir libm. En esta máquina eso no es el `np.exp` de NumPy.
- Sus arneses comparan salidas. Conviene revisarlos aquí comparando pesos.
