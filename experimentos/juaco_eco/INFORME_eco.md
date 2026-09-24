# INFORME — JUACO-ECO v1: diseño e instrumento (23-sep-2026, creador). Sin serie.

**Veredicto de la tanda: el instrumento está LISTO PARA AUDITAR (arnés 41/41, humo con JSON). No hay dato de nivel.**
Lo que más enseñó la tanda:
- **«Soltar el bicho» tal cual muere:** 90 FABRICA en un mundo de 3600 celdas bajan de 90 a 1 cuerpo en 3000 pasos, sin reposición.
- **Mi primer control «sin selección» también seleccionaba.**

## Qué hice
- **Construcción por anclas** (`construye_eco.py`), en dos piezas:
  - `motor_eco.py` desde `motor_convive.py`. Con `eco=None` es la pista v2 bit a bit.
  - `FABRICA_ECO` / `APR_ECO`: sólo cambia `_see`, O(distancia), con salida idéntica.
- **Con `eco`, el motor agrega:**
  - mundo sin tope de 9;
  - un genoma de 18 perillas por cuerpo (memoria nueva en el organismo: cero) y 8 sombras;
  - mutación con rng propios;
  - reposición de fundadores apagable (ERR-118);
  - vivero con banco y corte;
  - checkpoint reanudable con pickle de todo el estado;
  - individuos por flujo.
- **Runner `corre_eco.py`:**
  - modos `--humo` / `--serie` / `--lee` / `--largo`;
  - aborta con banderas desconocidas o abreviadas (ERR-115);
  - sólo acepta las ventanas de semillas declaradas;
  - al final imprime el veredicto por la letra.

## Arnés `identidad_eco.py` (salida completa en `identidad_eco_salida.txt`)
```
(0) 4/4 origen y construcción · (I) 4/4 eco=None == motor_convive BIT A BIT (FABRICA, O2 inmediata, mixta, APR)
(F) 4/4 _see rápido == original en 200000 casos (23641 empates, 1408 'todos rechazados') y en corridas completas FABRICA/APR
(E) 5/5 genoma con perillas apagadas == pista v2 · (M) 4/4 determinismo, tasa 0.192 (p 0.2), rangos, genes no mutables
(R) 3/3 refunda=0: cero fundadores, == refunda=1 hasta el primer fundador, "si todo muere, muere" (t_ext 3624)
(V) 2/2 vivero y corte · (C) 2/2 checkpoint cortado y reanudado == seguido; firma ajena aborta · (S) 1/1 · (G) 9/9 (con ventanas de semillas) · (J) 3/3 juez
RESULTADO: 41/41
```

## Humo `--humo` (un proceso, semilla 19001, VIDA, T = 12 000, corte 8000; 113 s)
- **JSON:** `datos/humo/eco_humo_s19001_20260923_191418.json`.
- **Velocidad:** 113 pasos/s con 70 cuerpos de media, ≈ 116 µs por cuerpo y paso con la máquina cargada.
- **Resultado:**
  - muere en t = 11 686 (3.7 k pasos después del corte);
  - tasa de mutación medida: 0.048;
  - bloqueados: 0.

## Humos exploratorios (5, un proceso cada uno; semillas 10012/10013 de práctica)
| corrida | resultado |
|---|---|
| ECO puro (sin vivero), 90 FABRICA | 90 → 1 en 3000 pasos |
| VIDA 40k/corte 30k (v0: medía a los vivos) | alpha +0.37 fuera de sombras ±0.02; 6 cuerpos vivos 10k después del corte |
| AZAR v0 (donante = un vivo al azar) | alpha **+0.39** también: **no era neutral** |
| MUT0 | extinto en 35 376 (5.4k después del corte) |
| AZAR v1 (banco neutral) | el banco queda dentro de sus sombras salvo NK y tau_e en puntos sueltos; 9 cuerpos 10k después del corte |

## Qué falló (candidatos a ERR; el coordinador numera)
1. **El control «sin selección» v0 era selección por viabilidad.** Copiar el genoma de un cuerpo **vivo** al azar premia al que vive más, y medir la media de los **vivos** tiene el mismo sesgo.
   - Arreglo: en AZAR el genoma de todo cuerpo nuevo sale del banco al azar.
   - La prueba de selección se hace sobre el **banco** contra sus sombras.
2. **El juez v1 comparaba G0 con G0.** Usaba la mediana por gen del banco, que con p = 0.05 es G0; el humo dio supervivencias idénticas.
   - Arreglo: 9 entradas del banco (arnés J). Es **enmienda tras el humo** y el humo **no** la ejercitó.
3. **Mi predicción implícita de diseño quedó refutada:** esperaba que el organismo real viviera lo bastante en el mundo gigante para que la mutación actuara, y no vive.
4. **Dos arneses corrieron a la vez** y mezclaron el archivo de salida. La salida pegada es de una corrida sola.

## Costo y comandos (SÓLO el coordinador; yo no lancé Pool ni --serie)
- **Por trabajo** (semilla × brazo): vivero ~11 min; tras el corte, poco si decae; juez ~2 min.
  - 80 trabajos ≈ 17 h de CPU, es decir **≈ 3–4 h con Pool 6** por serie.
  - Techo ≈ 8 h si VIDA crece hasta cientos de cuerpos tras el corte.
- **Largo:** 1e6 pasos ≈ 3 h de CPU con N = 100, 10 h con 300, 32 h con 1000; 1e7 pasos, ×10.
- Checkpoint cada 10 000 pasos; `--reanuda` retoma tras un corte de luz.

```
python experimentos/juaco_eco/identidad_eco.py                                              # 41/41 antes de todo
python experimentos/juaco_eco/corre_eco.py --serie --prueba_pool --desde 19031 --n 2 --pool 2  # prueba de la ruta del Pool (sin valor)
python experimentos/juaco_eco/corre_eco.py --serie --desde 19101 --n 20 --pool 6            # serie
python experimentos/juaco_eco/corre_eco.py --serie --desde 19121 --n 20 --pool 6            # replica
python experimentos/juaco_eco/corre_eco.py --serie --desde 19101 --n 20 --pool 6 --reanuda  # si se corta
python experimentos/juaco_eco/corre_eco.py --largo --desde 19301 --n 3 --pool 6             # SOLO tras la serie; exploratorio
```

## Qué queda / lo no verificado
- **La ruta `--serie` y `--largo` con Pool NO se ejecutó** (regla). La función de trabajo sí corrió en el humo, con su checkpoint.
- **El juez nuevo** sólo está verificado en el arnés.
- **APR_ECO en v2 pierde su herencia de Q:** su `al_parir` devuelve None, igual que FABRICA pierde el nodo en v2. No se usa en la serie.
- **La cifra del explorador «mutación ~0.01/paso» es de otra unidad:** aquí la mutación es por gen y por nacimiento.
- **Predicción firmada:** NO 0.50 · MODESTO 0.35 · FUNCIONA 0.07. La que puede fallar: alpha seleccionada en el banco de VIDA en ≥ 15/20 (0.55).
