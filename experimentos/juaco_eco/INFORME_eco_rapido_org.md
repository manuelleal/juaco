# INFORME — gemelo compilado de ECO v2, órganos como genes (`motor_eco_rapido_org.py`), 24-sep-2026 (compilador)

Misión: llegar a la AGI por este camino. Un gemelo que no sea bit a bit idéntico sólo explora.

**Arnés `identidad_eco_rapido_org.py`: RESULTADO 99/99** (salida en `identidad_eco_rapido_org_salida.txt`, 459 s, un proceso, sin Pool).
- Semillas: sólo de práctica (19901–19909, 20091–20099, 10001–10011).
- Gemelo `024f0a8ea5e12c7d`, arnés `aa188b564b8d831e`; son los sha de la cabecera de la salida.

## Qué es y cómo se enchufa
- **Qué hace.** `motor_eco_rapido_org.run_solapadas(...)` equivale a `motor_eco2.run_solapadas` bit a bit, con la misma firma y la misma salida.
  - Genoma de 20 genes.
  - Cerebros FAMB_ORG_ECO (órganos por cuerpo), FAMB_RES0_ECO, FABRICA_ECO y FABRICA, mezclables por linaje.
- **Cómo se enchufa.** `corre_eco_v2.usa_gemelo()` ya lo hace (como `corre_eco_rapido.py`): una copia de `motor_eco2` con `run_solapadas` = el del gemelo.
  - El arnés lo prueba por esa ruta: `corre_eco_v2.trabajo` (w30, VIDA, T 12 000) da lo mismo que Python.
  - El corte de luz tras el checkpoint de 10 000, reanudado, da lo mismo que la corrida seguida.
- **Qué no toca.** Es una copia de `motor_eco_rapido_fam.py` (132/132, que no se tocó tras entregarse) con dos cambios:
  - el motor de referencia es `motor_eco2`: la mutación en `objmode` usa `ME2.muta`, que consume 2 × 20 números por genoma;
  - hay dos órganos por cuerpo, sacados de su genoma en `_consts` con el umbral literal del carro (`>= 1.0`):
    - `ensena`, del **padre**: sin él no hay tabla, el hijo nace con `recibido` −1 y el parto no se cuenta en `_n10`;
    - `filtra0`, del **hijo**: hace el papel de SIN0.
  - Sin eco, los dos órganos están apagados.
- **Checkpoints.** No se mezclan con el original ni con los otros gemelos (firma).

## Qué cubre el arnés
- **(N) Nacimiento aislado.**
  - 2500 genomas de 20 genes al azar, 346 de ellos con un órgano en el umbral EXACTO 1.0, con memoria None o una tabla. Coincide todo: Wps/Wns, nodo, lecturas, `lect_div`, `recibido`, órganos expresados y los dos Generators.
  - `al_parir` con y sin `ensena`: 2000 casos.
- **(I) y (E) Corridas enteras.** Se comparan salida, trayectoria, cada nacimiento, cerebro + familia + órganos de los vivos, mundo y filas `ind_cb`. Casos:
  - eco=None;
  - los brazos VIDA, AZAR y MUT0 en esc 30 y 90, y VIDA en esc 270 (T 1200);
  - órganos prendidos, apagados, sólo uno, mezclados por linaje, en el umbral exacto y un ulp por debajo;
  - mutación con p 0.3 y 0.4, que prende y apaga órganos;
  - refunda=0, tope, divisiones, y la mezcla de los tres cerebros de la familia.
- **(C) Checkpoints.** El estado completo, órganos incluidos, coincide en t = 1000, 2000 y 3000. Cortado y reanudado es igual a seguido.
- **(J) El juez** (refunda=0, genoma=): G0, órganos prendidos y un banco real del corte (30 de 36 con `ensena`).
- **(R) Regresión.** FABRICA_ECO y FAMB_RES0_ECO con 20 genes, contra `motor_eco2`. Con eco=None, gemelo de órganos == gemelo de la familia a T 40 000.
- **(K) Controles**, barridos sobre las 30 corridas guardadas. Cada uno falla exactamente donde se predice:

  | control | corridas donde difiere | física distinta |
  |---|---|---|
  | órganos siempre expresados | 22/22 | 22/30 |
  | `filtra0` leído del PADRE | 6/6 | 4/30 |
  | sin leer el nodo | 17/17 | 17/30 |
  | empate al primero (sólo lo delata `lect_div`) | 2/2 | 0/30 |

  Además fallan: exp de libm, suma ingenua, turno fijo, VIDA contra MUT0 y órganos prendidos contra apagados.
- **(Z) Caché.** Un proceso NUEVO hace 0 compilaciones y reproduce 3/3 corridas del original, esc 270 incluida.

## Delegado a NumPy y trampas
- **Delegado.** Lo mismo que el gemelo de la familia (ver `INFORME_eco_rapido_fam.md`): `np.exp` por su bucle 1-D, BLAS, Generators creados en Python, empates del top-3 a `np.argsort`, y mutación y banco en `objmode`. No hay nada nuevo que delegar.
- **Trampas propias de v2:**
  - el umbral es `>=`: 1.0 exacto expresa y un ulp por debajo no, probado en corridas enteras;
  - `ensena` se lee en el padre y `filtra0` en el hijo. El control con el `filtra0` del padre sólo se ve en partos con neutras donde los dos órganos difieren (6 corridas).

## Aceleración (máquina con otros procesos; mismo mundo, en caliente)
| mundo | cuerpos | original | gemelo | factor |
|---|---|---|---|---|
| esc 90, 90 FAMB_ORG_ECO, VIDA/AZAR/MUT0, T 4000 | 79–82 | 181–192 pasos/s (66–68 µs por cuerpo y paso) | 7 560–9 310 pasos/s (1.3–1.6 µs) | **×42–50** |
| esc 270, 270 FAMB_ORG_ECO, VIDA, T 1500 | 229 | 58 pasos/s (75 µs) | 1 846 pasos/s (2.4 µs) | ×32 |
| `corre_eco_v2.trabajo` (w30, T 12 000) | — | 18.2 s | 0.4 s | ×45 |

Corridas completas de la serie v2 con el gemelo (VIDA, T 120 000, corte 60 000, semilla de práctica 20096):

| mundo | tiempo | cuerpos de media | máximo |
|---|---|---|---|
| w90 | 20 s | 119 | 290 |
| w270 | 62 s | 347 | 775 |

En Python serían unos 16 y 49 min.

## Fuera de alcance y riesgos
- **Carros que abortan con `ValueError`:** otros carros y otros MODO. También abortan un genoma de 18 genes (con el mismo mensaje que `motor_eco2`) y los checkpoints ajenos.
- **La ruta con `Pool` no la corrí** (regla). Primer paso sugerido, con la caché ya creada por el arnés: `corre_eco_v2.py --prueba_pool --pool 2`.
- **Validez:** numpy 2.4.3, numba 0.67.0 y estas OpenBLAS. Hay que repetir el arnés tras cualquier cambio. Si cambian los sha fijados (`motor_eco2`, `pista2` y los cuatro carros), el gemelo se niega a correr.
