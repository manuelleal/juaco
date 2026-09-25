# INFORME — gemelo compilado de JUACO-ECO con la familia (`motor_eco_rapido_fam.py`), 24-sep-2026 (compilador)

Misión: llegar a la AGI por este camino; el método manda. Un gemelo que no sea bit a bit idéntico sólo explora.

**Arnés `identidad_eco_rapido_fam.py`: RESULTADO 132/132** (salida en `identidad_eco_rapido_fam_salida.txt`, 753 s, un proceso, sin Pool).
- Semillas: sólo de práctica, 19901–19909 y 10001–10011.
- Gemelo `d1f16769a53bb51c`, arnés `2bad9b56014a8dd1`; son los sha que imprime la cabecera de la salida.

## Qué es y cómo se enchufa
- **Qué hace.** `motor_eco_rapido_fam.run_solapadas(...)` tiene la misma firma y la misma salida que `motor_eco.run_solapadas`, `d['carro']` incluido.
  - Cerebros: FABRICA, FABRICA_ECO y **FAMB_RES0_ECO**, mezclables por linaje.
  - Modos: `eco=None` y `eco=dict` (genoma, mutación, banco, sombras, vivero, corte, `refunda=0`, checkpoint, `ind_cb`).
- **Qué no toca.** Es una copia de `motor_eco_rapido.py` más la familia; `motor_eco_rapido.py` no se toca.
- **Cómo se enchufa en un runner.** Es lo que ya hace `corre_eco_v12.usa_gemelo()`, igual que `corre_eco_rapido.py`: `g = types.ModuleType(...)`; `g.__dict__.update(<motor_eco sin dunders>)`; `g.run_solapadas = motor_eco_rapido_fam.run_solapadas`; `CR.ME = g`.
  - La línea corta `CR.ME.run_solapadas = motor_eco_rapido_fam.run_solapadas` también vale. Pero parchea `motor_eco` para todo el proceso.
  - Lo probé por esa ruta con `corre_eco_v12.trabajo` (VIDA_T y AZAR_T, s19902, T 3000, juez con 0 semillas): **idéntico al motor Python**.
- **Checkpoints.** No se mezclan con los del original ni con los de `motor_eco_rapido.py`: la firma es propia y aborta.

## Qué se portó (FAMB_RES0_ECO = FABRICA_ECO + "la familia pasa su tabla")
- **Por cuerpo, lo recibido.** La R de cada (necesidad, letra). El nodo del carro es esa tabla repetida `NODO_LEE` = 50 veces.
- **Por cuerpo, lo vivido.** La R de la mordida más reciente de cada clave, que es lo único que `al_parir` lee de `_mordh`.
- **`al_parir`.** Lo vivido si lo vivió; si no, lo recibido. Va en el orden del `sorted()` del carro (necesidad, letra), con `partos` y `dado[:50]`.
- **`nace`.** Tras Wl y KW:
  - SIN0;
  - instalación de la tabla;
  - 50 lecturas por la vía lenta, en orden de mayor sorpresa y, en empate, el mayor índice original: es `np.lexsort((-indice, -sorpresa))[0]`;
  - LAM, ETA_S, AVERSION y CLIP_S salen del **genoma del hijo**, con los mismos redondeos que `resultado()`.
- **`salida()` de los vivos.** Se calcula con una instancia real del carro: nodo, lecturas, `lect_div`, `n10`.
- **`muere()` no se compila.** En la pista v2 el cerebro del muerto se descarta en ese mismo paso. El arnés (M) lo comprueba: el original con `muere()` anulado da la misma salida (eco=None y eco VIDA).

## Qué se delega a NumPy y por qué (regla 9)
- **Igual que el gemelo viejo.**
  - `np.exp`: el bucle 1-D de NumPy por ctypes, porque el exp de libm difiere en un 4.67 % aquí.
  - BLAS de numba: iguala al de NumPy en ddot 6, 90 y dgemv. El ddot 6 es también el de la lectura del nodo.
  - `Generator`s: se crean en Python y numba extrae sobre su estado.
  - Empates del top-3 de Kenyon: `np.argsort` en `objmode`.
  - Mutación y banco: en `objmode`, con las líneas del original.
- **No se delega la fila de la sorpresa.** Es `((Wps[N] - Wns[N]) * P).sum(1)`, con filas de 6. El `.sum(1)` de NumPy suma de izquierda a derecha desde 0.0: 0 distintos en 163 060 filas, m = 1..400. La asociación "primero + resto" difiere en 8.5 % (control).
- **No se delega el `lexsort`.** La clave (sorpresa, índice) no tiene empates, así que el primero es el máximo lexicográfico sea cual sea el algoritmo.
- Ninguna suma de 8 o más reales en el núcleo. Ninguna función recursiva. **Caché probada en un proceso NUEVO**: 0 compilaciones y 3/3 corridas idénticas.

## Trampas halladas
1. **El desempate de la lectura casi no se ve en la física (hallazgo).** Con el empate al primer índice, la corrida s19906 (T 20 000, 155 partos) da salida, trayectoria y cerebros finales idénticos.
   - Por qué: las filas empatadas son copias de la misma entrada, o son de necesidades distintas y tocan filas distintas de W.
   - Sólo lo delatan `lect_div` en tablas de UNA entrada y algún empate exacto raro.
   - Por eso el arnés compara ahora **cada nacimiento** tras `nace()`: t, linaje, k, recibido, lecturas, `lect_div`, Wps y Wns.
   - Con esa traza, los tres controles de la familia, barridos sobre las 41 corridas FAMB guardadas, fallan exactamente donde se predijo:
     - sin SIN0: 39/39;
     - sin leer el nodo: 39/39;
     - empate al primero: 7/7 corridas con tablas de una entrada. Además cambia 1 de las otras 34 y la física en 0/41.
2. **La referencia de (Z) estaba mal en la primera versión del arnés.** Se había hecho con `ind_cb`, que deja vacío `individuos`. Rehecha sin `ind_cb`, el gemelo cargado de la caché da idéntico.
3. **`corre_eco.trabajo()` llama al juez con `JUEZ['semillas']` (19201…).** En el arnés se cambia, sólo dentro del proceso, a 19907 y 19908. El arnés viejo usaba 19201–19203.

## Aceleración (máquina con otros 3 procesos al 100 %; mismo mundo, en caliente)
| mundo | cuerpos | original | gemelo | factor |
|---|---|---|---|---|
| ECO esc 90, 90 FAMB, VIDA/CEREBRO/AZAR/MUT0, T 4000 | 95–102 | 150–158 pasos/s (64–67 µs por cuerpo y paso) | 6 250–7 540 pasos/s (1.40–1.57 µs) | **×42–48** |
| pista v2, 9 FAMB, T 20 000 | 18.4 | 952 pasos/s | 56 827 pasos/s | ×60 |
| `corre_eco.trabajo()` con FAMB (T 12 000 + juez) | — | 88.7 s | 1.9 s | ×47 |

- Una corrida del gemelo, ECO esc 90 VIDA con FAMB hasta T 200 000 (corte 60 000), tarda 49.7 s: 143 cuerpos de media, 262 como máximo, 64 208 partos.
- Proyección a 1e6: unos 4–5 min por corrida si la población se mantiene; en Python serían unas 3 h.

## Fuera de alcance y riesgos
- **Carros que abortan con `ValueError`:** la variante SIN0 = 0, otros MODO (`res1`, `bar`, `oraculo`), APR, O1–O4. También abortan T < 4 y los checkpoints ajenos.
- **La ruta con `Pool` no la corrí** (regla). Primer paso sugerido, con la caché ya creada: `corre_eco_v12.py --prueba_pool --desde 19902 --n 2 --pool 2`.
- **Validez:** numpy 2.4.3, numba 0.67.0 y estas OpenBLAS. Hay que repetir el arnés tras cualquier cambio. Si cambian los sha fijados (motor_eco, pista2 y los tres carros), el gemelo se niega a correr.
