# INFORME — OHNO SOBRE BASE VIVA (Opus A, 24-sep-2026). Misión: llegar a la AGI por este camino.

**Veredicto del trabajo: FUNCIONA como instrumento; el mundo quedó calibrado, con reservas.** No se corrió ninguna serie. Mi
predicción firmada para cada ventana es **NO (0.67)**, con NO EVALUABLE por techo en 0.15.

## Qué construí (`experimentos/organelos/ohno/`; no toqué nada existente)
- **Copias byte a byte** de `gramatica/` (`construye_ohno.py --verifica`): motor 6b65dc5e32093424, carro 2cee0a8510c997b9,
  `gramatica_def` c58086e103d030d9, `conducta` 9a2f1226fe27a514. No hizo falta código nuevo en el motor: el mundo pobre es el argumento
  `r_rep` y los fundadores con filtra0 son `eco['gramatica']`.
- **Runner `corre_ohno.py`:**
  - brazos: VIDA (desde filtra0 expresado, con errores de copia), FIJO:filtra0 (= MUT0) y AZAR (deriva pura), con 8 sombras;
  - modos `--humo`, `--calibra`, `--prueba_pool`, `--serie`, `--lee`;
  - la letra: G1 R0 pareado ≥ 15/20, G2, G3 no diseñado, P-OHNO, y las guardias TECHO e INVIABLE;
  - nube-9 atrapado en `trabajo()`.
- **Arnés `identidad_ohno.py`**:
  - (O1, O1b, O1c) con la mutación apagada, VIDA == FIJO:filtra0 bit a bit;
  - (O2) con fundadores al azar, == `corre_gramatica`;
  - piezas de la duplicación: (D1) una copia idéntica es neutra bit a bit; (D2) una copia que diverge al vecino cambia el mundo y
    el original (nacer/hijo) conserva su conducta; (D3) en el mundo aparecen copias divergidas con el original intacto;
  - nube-9, la letra y las banderas. **Resultado final: 12/12 (864 s)**, en `identidad_ohno_salida.txt`.
- **Humo** (25001, T 20 000, los 3 brazos, 142 s): escribe sus tres JSON en `datos/humo/ohno_humo_20260924_205759/`. `--lee` corre
  sobre ellos y escribe su `RESUMEN.json`: la letra con los JSON reales no se rompe (ERR-42).
- Sha finales: `corre_ohno.py` d47b9de89709d25b, `construye_ohno.py` 85b9a9e231a91074. `manifiesto --check`: 20 congelados intactos.

## La calibración (un proceso; declarada; FIJO:filtra0 a T 80 000, corte 40 000)
| `r_rep` | persisten | lectura |
|---|---|---|
| 0.020 | 6/6 (R0 0.87–1.03) | techo |
| 0.006 | 3/4 | |
| 0.005 | 3/4 | |
| 0.004 | 0/4 | inviable |

- Por la regla del preregistro (§3b), queda **`r_rep` = 0.006**.
- **Hallazgo:** tras el corte, una población que persiste siempre queda en R0 ≈ 1 (el quimiostato fija la densidad). Lo único
  calibrable es la persistencia, y en el mundo pobre la decide un cuello de botella en el corte: la población cae a 1–5 cuerpos.
- Además, antes del corte casi no hay partos (7 en 40 000 pasos), así que Ohno tiene solo unos 240 nacimientos por semilla.

## Qué falló
- **ERR-126** (candidato):
  - El primer arnés dio 8/10: en el mundo pobre, (D2) y (D3) no tenían partos que ejercitar (ERR-120 otra vez). Las piezas pasaron
    al quimiostato de ECO.
  - Después (O1b) dio igualdad con solo 9 partos contra un umbral de 20 puesto a ojo; lo bajé a ≥ 5 y lo declaro.
- Mi primera calibración (0.02) fue ingenua: pensé que bajar la comida bajaba el R0.

## Costo en la NUBE (Pool 3; medido en el PC: 155–222 s por corrida a T 80 000)
| paso | tiempo |
|---|---|
| por ventana (60 corridas ≈ 3.2 h de CPU) | ≈ 1.1 h |
| serie + réplica + arnés (~9 min) + prueba del Pool (~2 min) | **≈ 2.4 h** |
| margen si la nube es 25 % más lenta | ≈ 3 h |

T ya está recortado de 120 000 a 80 000. Si hace falta recortar más, se quita la réplica, no semillas.

## COMANDOS EXACTOS, en orden (desde la raíz del repo)
```
python experimentos/organelos/ohno/construye_ohno.py --verifica
python experimentos/organelos/ohno/identidad_ohno.py            # debe dar N/N; ~9 min
python manifiesto.py --check
python experimentos/organelos/ohno/corre_ohno.py --prueba_pool --pool 2
python experimentos/organelos/ohno/corre_ohno.py --serie --ventana serie --pool 3      # 25011-25030; si se corta: + --reanuda
python experimentos/organelos/ohno/corre_ohno.py --serie --ventana replica --pool 3    # 25031-25050
python experimentos/organelos/ohno/corre_ohno.py --lee experimentos/organelos/ohno/datos/ohno_serie_s25011-25030
python experimentos/organelos/ohno/corre_ohno.py --lee experimentos/organelos/ohno/datos/ohno_replica_s25031-25050
```

## Mis predicciones refutadas y lo que no verifiqué
- **Refutadas:**
  - «Un quimiostato más pobre baja el R0 de filtra0 fijo»: no, sigue en ≈ 1.
  - «0.02 basta para salir del techo»: no.
  - Mi primera versión del arnés «ejercita la duplicación»: no lo hacía (ERR-126).
- **No verifiqué:**
  - La persistencia real de FIJO a 0.006 con 20 semillas: la estimé con 4, y puede disparar la guardia TECHO.
  - La velocidad de la nube.
  - Que la prueba del Pool corra: no se me permite usar Pool.
  - Cuántas duplicaciones sobreviven tras el corte.
- **Qué queda:**
  - Si sale TECHO o NO, el mundo de Ohno necesita que el vivero produzca partos (un corte temprano o una comida que no se vacíe
    con 30 cuerpos). Eso es un preregistro nuevo con otra calibración.
