# INFORME — pista v2 con generaciones solapadas (22-sep-2026, creador)

**Veredicto: HAY ALGO MODESTO.** La pista v2 está construida y verificada (arnés **36/36**; con `solapadas=0` es la v1 bit a bit).
Pero **el mundo de v1 no tiene capacidad de carga** cuando las generaciones conviven. Para que la densidad la regule el recurso
hizo falta **cambiar la regla de reposición** (quimiostato), y ese cambio **lo decide el coordinador**. No se corrió ninguna serie.

## Qué hice
- **Construcción:**
  - `construye_pista2.py`: 4 anclas sobre `carrera_escuderias/pista.py` (sha 9f47c65e438e0ff4). Da `pista2.py` (4d2bee16e7961261), con `run(..., solapadas=0)` idéntico y `solapadas=1` que va a `motor_convive.py`.
  - Los carros corren **sin cambios** desde `carrera_escuderias/carros`.
  - `construye_ctrl_o3.py` hace el control `CTRL_O3_SINTERM` (O3 con `TERMINAL = False`; diff de una línea).
- **Reglas del parto:**
  - El hijo nace en el paso del parto, en la celda del padre, con la dote pagada por el padre. No hay cola.
  - Cada cuerpo es una instancia del carro: `crea(ctx)` con su rng `[seed, linaje, 12, k]` y en seguida `nace(memoria = al_parir del padre, rng_hijo [seed, linaje, 13, k])`.
  - Fundador limpio solo cuando muere el último cuerpo del linaje. Ocupa el turno del muerto.
- **Cambios de interfaz (documentados):**
  - `ctx['id']` es único por cuerpo (`O2#3/17`).
  - `quiere_parir` recibe `cola` = parientes vivos del linaje, más `vivos_linaje` y `hijos_vivos`.
  - `nace` recibe `padre`.
  - **FABRICA pierde su nodo REL:** esa herencia viaja por la muerte del padre, y en v2 ningún cuerpo nace de un muerto.
  - No se portan `compat=1`, `diag=1` ni la telemetría F9.
- **Capacidad:**
  - `reposicion='fija'` (por defecto): lo mordido u olvidado desaparece y el mundo repone 0.03·esc objetos por paso (0.27 con 9), con banco ≤ 1 y hasta 36 objetos.
  - El 0.03 es la reposición medida del mundo SOLO de v1 con un FABRICA: 0.0316/paso en 10001–10004.
  - Piso: si el mundo queda vacío, se pone 1 objeto (2 veces en el humo de O2).
  - Biología: quimiostato, flujo fijo de recurso, K ≈ flujo/consumo por cabeza; nacimientos y muertes dependen de la densidad.
  - `reposicion='inmediata'` es la regla de v1.
  - Tope de seguridad: 300 cuerpos, con partos bloqueados contados y marcados.
- **Juez v2** (`corre_convive.py`), solo desde la física. Mide:
  - persistencia (ENMIENDA 6);
  - «persiste el carro» (≥ 1 linaje persistente);
  - R0 de cohorte t ≤ T/2, con los censurados como cota inferior y la fracción censurada, más R0 de vidas completas;
  - tamaño del linaje (media, mínimo y final para t ≥ 10000);
  - generaciones;
  - muertes voluntarias declaradas por el carro.
  Además imprime las predicciones firmadas con SE CUMPLE, NO o NO EVALUABLE.

## Qué falló (y mis predicciones refutadas)
- **Mi supuesto de diseño quedó refutado:** yo daba por hecho que el mismo mundo regularía la densidad.
  - Con reposición inmediata, 9 O2 pasan de 9 a **128 cuerpos en 5000 pasos** y siguen creciendo (s10001; 91 s).
  - La causa: cada mordida repone al instante una letra al azar, así que morder B/D fabrica en promedio ~0.5 objetos buenos. Limpiar se vuelve una bomba de energía y el flujo de comida **crece** con el número de cuerpos. Es la trampa del «mundo que se come la comida», al revés.
  - O1 se frenó en ~20 y FABRICA en ~10, pero sin techo del recurso.
  - Con el quimiostato, O2 queda en 12–24 cuerpos (medido).
- **Resultado estructural que no esperaba:** nueve linajes del mismo carro comparten ~15–30 cuerpos y se extinguen por **deriva y exclusión competitiva**. Además, los fundadores limpios de O1 y O4 mueren enseguida: 400 y 304 fundadores en 20000 pasos, contra 50 de O2 y 25 de O3. Por eso la persistencia por linaje es baja para todos y mezcla deriva con calidad del carro.
- **O3 y O4 casi no usan su muerte programada en v2:** declaran 3/85 y 14/413 muertes. Es raro que tengan ≥ 4 o ≥ 6 parientes vivos.
- **Primer intento del arnés:** falló por un `KeyError` mío (`vetos` está en `_carrera` en v1). Lo corregí y volví a correr.
- **Versiones:** el humo corrió con el motor 942c0cb4 y el juez 2e5f095d; el arnés final, con el motor d10cb902 y el juez de hoy. Lo que cambió después del humo: la entrada `VOL_DECL` del control, la ruta del control en el juez, las predicciones firmadas, la guardia de piso y la tolerancia. La física no cambia (el arnés (S) y el (K) lo cubren).

## Humo (un proceso, semilla de práctica 10012, T = 20000, reposición fija; `datos/convive_humo_cinco_s10012_T20000_fija_20260922_200435*`)
| carro | persisten/9 | R0 cohorte | tamaño medio del linaje | cuerpos del carro (media / máx.) | generaciones (máx., mediana) | vida mediana | muertes voluntarias declaradas | fundadores | s/semilla |
|---|---|---|---|---|---|---|---|---|---|
| FABRICA | 0 | 0.158 | 1.05 | 9.5 / 13 | 1 | 101 | 0/572 | 476 | 24.6 |
| O1 | 1 | 0.133 | 1.49 | 25.3 / 35 | 3 | 200 | 0/527 | 400 | 96.4 |
| O2 | 2 | 0.600 | 1.36 | 16.6 / 24 | 3 | 1398 | 0/142 | 50 | 62.3 |
| O3 | 4 | 1.000 | 1.74 | 15.0 / 22 | 3 | 2256 | 3/85 | 25 | 99.4 |
| O4 | 4 | 0.857 | 1.15 | 20.9 / 29 | 6 | 200 | 14/413 | 304 | 97.7 |

- 0 partos bloqueados en todos. Mundo con 12.5–32.7 objetos de media.
- Semilla sola, a T = 20000: solo sirve de humo.
- Otros humos exploratorios (≤ 6 corridas en total):
  - 10001 T = 5000 inmediata;
  - tasas de v1 a T = 5000;
  - calibración SOLO 10001–10004 a T = 20000;
  - 10001 T = 10000 fija;
  - prueba de la ruta `--serie` con 10013 a T = 2000 (archivos `datos/prueba_ruta_*`).

## Arnés (`identidad_convive_salida.txt`, 36/36, 137 s)
```
(0) origen pista.py sha 9f47c65e438e0ff4 OK · pista2.py == construccion por anclas OK
(I) solapadas=0 == pista v1 (HEAD a170746) en TODA la salida: 7/7 (compat=1; 9 FABRICA diag; rep_acum=1; escala=0; mundo_n=9;
    9 O1 fundador limpio; O2*3+O3*3+O4*3 fundador limpio)
(S) sin partos (todos vetados) v2 == v1 en la fisica y el rng final: 9 FABRICA (76 muertes, 13 vetos), 9 O1, mezcla, 1 FABRICA T=6000 + control no vacio
(D) determinismo fija e inmediata 2/2
(C)/(H) contabilidad (individuos, genealogia, tam, objetos del quimiostato) y herencia (crea = 9 + nac + fund; nace = nac;
    cola == vivos-1; tabla del padre llega en O1/O3; FABRICA memoria None) 12/12
(K) CTRL_O3_SINTERM pasa el chequeo y == O3 bit a bit mientras TERMINAL no puede dispararse 2/2
(T) tope 12 respetado y marcado · (G) 5 guardias
RESULTADO: 36/36
```

## Tiempos y comandos (solo el coordinador; la ruta con Pool NO la corrí, regla 3)
- Por semilla a T = 100000 (humo ×5): FABRICA ~125 s, O2 ~310 s, O1/O3/O4/CTRL ~490 s. Son ~2400 s de CPU por semilla con los 6 carros.
- **Con Pool 6: ~2.2 h de CPU ideal, ~2.5–3 h reales por serie.** La réplica tarda lo mismo.
- Alternativa declarada: `--T 50000`, ~1.2–1.5 h.
- Tope de seguridad sin tocar (máximo 35 de 300).
```
python experimentos/generaciones/identidad_convive.py                       # debe dar 36/36 antes de todo
python experimentos/generaciones/corre_convive.py --serie --desde 10101 --n 20 --pool 6
python experimentos/generaciones/corre_convive.py --serie --desde 10121 --n 20 --pool 6   # replica
# prueba minima del Pool: --serie --desde 10014 --n 2 --T 3000 --pool 2 --carro O2
```

## Qué queda (decisiones del coordinador)
1. **Aprobar o no el quimiostato (P7).** El pedido decía «los mismos objetos y el mismo olvido por objeto»: eso se cumple. La reposición inmediata, en cambio, no regula. Propongo un ERR para el «mundo bomba» de v1: con un cuerpo por linaje era invisible, pero es la misma raíz de «la limpieza compartida es un bien público» (ENMIENDA 4).
2. Con 9 linajes del mismo carro, la persistencia por linaje queda dominada por la deriva. Para la letra de H quizá conviene la mezcla O2*3+O3*3+O4*3 (competencia directa en el mismo mundo). El juez no la corre todavía.
3. O3 y O4 casi no disparan su muerte programada en v2. H se prueba con los carros tal cual; H-b separa el mecanismo.

## v2 (tras la §9 del coordinador) — juez con el criterio principal y la pista mixta
- **Juez `corre_convive.py`** (e6dadfdad9c379cd):
  - **Criterio principal por semilla:** *persiste el carro* = ≥ 1 linaje sin fundadores tras t = 10000 (se reporta también la variante con ≥ 5 nacimientos). *Tamaño del carro* = cuerpos vivos, media de las muestras con t ≥ T/2. El carro *estabiliza* con ≥ 15/20 semillas.
  - La persistencia por linaje se sigue reportando y no decide.
  - Imprime las 4 predicciones de la §9.
  - `--mix`: 3 O2 + 3 O3 + 3 O4 con el quimiostato. Por semilla da el tamaño y la persistencia de cada estrategia. Compara O2−O3 y O2−O4 en pares (gana, pierde, empata, diferencia mediana, prueba de signo bilateral exacta). **H se sostiene** si O2 no queda por debajo en ≥ 15/20 contra ninguna de las dos.
  - Con T ≤ 10000 avisa que «persiste el carro» es trivial.
- **Arnés 37/37:** los 36 de antes + (M), la mixta con `solapadas=1`, determinista y con el tamaño por estrategia igual al total de la pista. La mixta con `solapadas=0` ya estaba en (I).
- **Pool 2** (prueba de ruta, T = 3000, 10014–10015): monocultivo 6 carros en 52 s y mixta en 10 s. Escriben crudo, log, pizarra y resumen (`datos/prueba_pool_*`). Números sin valor.
- **Tiempos a T = 100000:**
  - mixta ≈ 300 s por semilla → **≈ 20–25 min** con Pool 6;
  - monocultivos (6 carros) ≈ 2400 s de CPU por semilla → **≈ 2.5–3 h** con Pool 6.

```
python experimentos/generaciones/identidad_convive.py                                             # 37/37
python experimentos/generaciones/corre_convive.py --serie --desde 10101 --n 20 --pool 6           # monocultivos: FABRICA, O1, O2, O3, O4, CTRL_O3_SINTERM
python experimentos/generaciones/corre_convive.py --serie --mix --desde 10101 --n 20 --pool 6     # mixta (H)
python experimentos/generaciones/corre_convive.py --serie --desde 10121 --n 20 --pool 6           # replica monocultivos
python experimentos/generaciones/corre_convive.py --serie --mix --desde 10121 --n 20 --pool 6     # replica mixta
```
