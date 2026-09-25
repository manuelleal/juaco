# EXPLORATORIO, no es dato (paquete listo para la serie; todavía no hay datos de serie)

# PROMETEO SERIE: paquete preregistrado (Opus, 25-sep-2026, 10:09–10:50)

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).

**Estado: LISTO PARA LANZAR.**
- Arnés 18/18.
- Humo con JSON en los dos mundos.
- ERR-144 registrado: la guardia de suministro medía el órgano expresado; ahora mide la cinta.
- Se puede auditar antes: el cambio de ERR-144 está en `PREREGISTRO_serie.md` §7.

## Qué hay (`experimentos/organelos/prometeo/serie/`)
| archivo | qué es |
|---|---|
| `PREREGISTRO_serie.md` | preguntas, diseño, letra, predicciones con rango y P, costo, ERR-144 |
| `construye_serie.py` → `motor_serie.py` | `../motor_prometeo.py` por anclas: el control **MUDO**, el rng del kit en el checkpoint y el suministro medido en la cinta (ERR-144) |
| `organos_serie.py` | una sola definición de "órgano armado" (funcional o inerte) para la letra y el motor |
| `corre_serie.py` | runner: `--humo`, `--serie ... --pool N [--reanuda]`, `--lee`. La letra está en `veredicto()` |
| `identidad_serie.py` → `identidad_serie_salida.txt` | **18/18** |
| `datos/humo/humo_{quieto,onda8k}_20260925_103239/` | el humo válido (humo 3, tras ERR-144), con `HUMO.json` y los 4 JSON. Los humos 1 y 2 quedan como historia |

- **La pregunta:** ¿un órgano ARMADO se fija (≥ 50 % del banco en el corte y al final) más en PROMETEO, donde actúa, que en **MUDO**, donde la cinta lo arma igual pero no actúa? La comparación va pareada por semilla, en `quieto` y en `onda8k`.
  **P1:** F(P) > F(M) en ≥ 14/20, y además hay ≥ 4 semillas fijadas de más.
- **P2, aparte:** despegues (≥ 1 000 nacimientos solos) en onda8k ≥ despegues en quieto + 3.
- **El control que puede fallar** es la **guardia de suministro de novo**: PROMETEO/MUDO en [0.5, 2] antes de t 8 000. En el humo dio 0.76. P1 también puede fallar si MUDO fija tanto como PROMETEO.
- **Controles descartados:** AZAR, SIN_HGT y VIVERO_POR_LINAJE. MUDO es el nulo exacto de P1, y los otros tres responden preguntas que hoy no se hacen.

## Costo (medido)
- **Humo** (semilla 30190, T 60 000; 2 procesos míos junto a la otra serie Pool 6): 157–275 s por corrida.
- **Exploración** (14 procesos): 271 s de media, 390 s como máximo.
- **Por ventana:** 80 corridas con Pool 6 ≈ **50–60 min**, peor caso ≈ 87 min. Cabe en ≤ 2 h por ventana, y serie más réplica ≈ 2–3 h. No hizo falta recortar T ni brazos.

## Comandos exactos (SOLO el coordinador lanza `--serie`)
```
cd C:\Users\User\Documents\PROYECTOS\JUACO\organelos\experimentos\organelos\prometeo\serie
python construye_serie.py                       # sha de motor_serie.py: 2e69a885c7148c90
python identidad_serie.py --sin_b1              # 17/17 (≈ 5 min, 1 proceso)
python identidad_serie.py --solo_b1             # 1/1 (banderas, ERR-115)
python corre_serie.py --serie --ventana serie --pool 6
python corre_serie.py --serie --ventana replica --pool 6
#   si se corta:   python corre_serie.py --serie --ventana serie --pool 6 --reanuda
python corre_serie.py --lee datos\prometeo_serie_s30101-30120
python corre_serie.py --lee datos\prometeo_replica_s30121-30140
```
Cada ventana escribe:
- `datos/prometeo_<ventana>_s…/progreso.log`;
- `RESUMEN.json`, con el veredicto P1, P2, lo descriptivo y los shas;
- un JSON por corrida en `<ventana>/<mundo>/<BRAZO>_s<semilla>.json`.

**Shas** (`corre_serie.SHAS()`, 10:45):

| archivo | sha |
|---|---|
| `corre_serie.py` | 95f195db1a32cb6e |
| `motor_serie.py` | 2e69a885c7148c90 |
| `organos_serie.py` | 0e99ab3ff8850744 |
| `codigo_prometeo.py` | aac93f0a43b1c827 |
| `motor_prometeo.py` | d3367e86c45d40ab |

**Nota:** el humo 3 corrió con `corre_serie.py` antes de dos ediciones que no tocan ni la dinámica ni la letra:
- agregar `organos_serie.py` e `identidad_serie.py` a la lista de `SHAS()`;
- una línea descriptiva de suministro en el vivero.
Las dos se verificaron con `--lee` sobre el humo.

## Qué garantiza el nulo (y qué no)
- **Garantiza:**
  - MUDO con un cable o un slot nuevo da la **misma dinámica bit a bit** que la cinta sin ellos (M1–M3);
  - la HGT y la copia siguen iguales (M4);
  - la cinta de MUDO sí arma órganos, y los vivos expresan FILTRA0 (M5).
- **No garantiza:**
  - En MUDO el órgano de fábrica **nunca se pierde en la expresión**, porque siempre se expresa FILTRA0. En PROMETEO la cinta puede perder filtra0, como en la exploración s30002. Es una asimetría declarada.
  - MUDO acumula copias neutras de slots (humo: 82 % de nacidos con órgano armado en la cinta, contra 10 % en PROMETEO). Eso **le da más blancos** para fijar algo por deriva. Es parte de lo que el nulo tiene que vencer.

## Predicciones refutadas y lo que no verifiqué
- **Refutada ya (antes de la serie):** en §5 predije que la guardia de suministro pasaría con una razón entre 0.7 y 1.4 (P 0.85). En el humo 1, con la medida original, dio 2.3.
  - Era un bug de instrumento (ERR-144 a), no un resultado.
  - En el humo 2, con la medida de la cinta sobre el vivero entero, dio 0.56–0.62: MUDO acumula copias neutras de slots, así que ya es selección (ERR-144 b).
  - Tras ERR-144, en la ventana temprana, da 0.76.
  - Con una sola semilla, nada de esto tiene valor.
- **Humo sin valor, pero apunta a mi predicción principal (NO):** en quieto, MUDO llegó a F 0.445 con un solo órgano neutro (vida/neg/hermano/copiar), y PROMETEO a 0.
- **No verifiqué:**
  - el costo con Pool 6 real; lo estimé desde el humo y la exploración;
  - que la ventana temprana tenga nacimientos de novo suficientes en todas las semillas (en el humo fueron unos 150 nacidos antes de t 8 000);
  - una reanudación real de la serie a mitad de camino (sí R1 en el arnés, T 6 000);
  - que el `--serie` con Pool arranque bien en Windows con el monkeypatch: los hijos del Pool importan `corre_serie` y el parche se aplica al importar, como en `corre_fable`/`corre_v01`, pero no lo lancé (contrato: sin Pool).
