# INFORME n10b: la familia pasa su TABLA en vida (creador, tanda 2 del nivel 10, 23-sep-2026)

**Veredicto del paquete: listo para serie. Resultado: ninguno** (el humo es una semilla de práctica y no es dato).

## Qué hice
- **Decidí con los datos.** Diagnóstico (`diagnostico_mensaje.py`, práctica 12392, un proceso):
  - el mensaje de PARTO de la tanda 1 lleva sólo un 4 % de R < 0;
  - el 47 % de los mensajes no trae ninguna R < 0 propia.
  - Barajar valores casi iguales no cambia nada, y eso explica por qué PARTO ≈ BAR (11/20).
  - El mundo sí usa contenido: ORÁCULO 0.553 contra NADA 0.110. Los hijos mueren de veneno o sal (100 %) antes de poder aprenderlo solos.
  - Por eso **no cambié el mundo: cambié lo que dice el mensaje.**
- **Mecanismo (memoria nueva cero):** el padre vivo pasa su **tabla**. Es una entrada por (letra, necesidad), a lo sumo 8: la R más reciente que vivió y, para lo que no vivió, lo heredado. El hijo la lee con la misma dosis y la misma regla que el ORÁCULO y la pasa enriquecida.
  - Brazos: NADA, **RES** (candidato), RES1 (sólo lo vivido por el padre: ¿acumula la familia?), BAR (tabla barajada, el control que puede ganar), ORÁCULO y MIX 3+3+3.
- **Calibración del ancla (ERR-116), declarada antes de semillas nuevas.** El arnés prueba que NADA y ORÁCULO son bit a bit los brazos de la serie 12301–12320, así que esa serie los calibra. Las anclas son el intervalo de predicción al 99 % de la mediana de 20 semillas: **NADA [0.085, 0.135]** y **ORÁCULO [0.49, 0.62]**.
- **Arnés `identidad_familia_b.py` (`070e6524f79e3cc4`): 42/42**, en 126 s. Extracto de `identidad_familia_b_salida.txt`:
```
OK  I s12791 T6000 {'solapadas': 1, 'diag': 0, 'reposicion': 'fija'} bca742547501b96a bca742547501b96a nacimientos 28
OK  I FAMB_NADA == FAMILIA_NADA (tanda 1), v2 a4b354febe85aaae a4b354febe85aaae
OK  O s12791 T8000 v2 fija 37d6e53b78d6a5a7 37d6e53b78d6a5a7 nacimientos 49
OK  B2 BAR no consume rng: mismos Wl/KW y mismo estado de rng_hijo que RES y NADA
OK  B3 RES con la tabla COMPLETA == ORACULO: mismo nodo y misma via lenta len 400 400
OK  R subproceso con bandera desconocida: codigo != 0 y no escribe nada codigo 1
RESULTADO: 42/42  (126 s)
```
- **Humo** (un proceso, s12791, T = 20000, 6 brazos, 142 s). JSON: `datos/humo/n10b_humo_todos_s12791_T20000_20260923_170334.json`. Corrido con PREREGISTRO `100f83f74446a973` y runner `b7808bbb83fb038e`.

  | brazo | R0 nacidos | vida nacidos | tamaño |
  |---|---|---|---|
  | NADA | 0.306 | 81 | 9.5 |
  | **RES** | **0.667** | **324** | **16.4** |
  | RES1 | 0.333 | — | — |
  | BAR | 0.174 | — | — |
  | ORÁCULO | 0.705 | 252 | 11.8 |

  - En RES, 2 linajes sin extinción hasta T = 20000.
  - Tablas RES con B|hambre = −3: 90 % (RES1: 47 %; BAR marca mala la comida en el 23 %).
  - MIX, con cohortes de 26 a 35: RES 0.23, BAR 0.36, NADA 0.0.

## Qué falló o está en riesgo (mías, declaradas)
- **P3 (RES en [0.25, 0.55]):** el humo da 0.667, por encima. Mi hipótesis mecánica, no verificada: la tabla de la familia no tiene "B|sed = 0", y el ORÁCULO sí. Ese 0 verdadero borra la generalización de D a B por rasgos compartidos. **Lo incompleto puede ser mejor que la verdad.** No enmiendo: queda como predicción en riesgo.
- **P8 (RES sin persistencia en ≥ 15/20):** en riesgo por el humo. El vocabulario prohíbe "la familia se sostiene" sin una puerta para eso. Si el coordinador quiere leer persistencia, la puerta debe preregistrarse en un bloque propio; agregarla aquí ahora sería **candidato a ERR**.
- **F-4 (MIX RES > BAR):** el humo lo da invertido, con cohortes chicas. P7 (0.80) puede caer.
- **Descarté las propuestas del explorador:**
  - "Mundo monótono": v2 ya tiene la tabla fija.
  - "Ancla [0, 0.12]": sin cálculo.
  - "MIX invertido": era del humo; en la serie, MIX PARTO > NADA fue 17/20.
- **Enmiendas tras el humo:** ninguna.

## Qué queda
- **Serie** (sólo el coordinador): `python experimentos/subida_n10b/corre_n10b.py --serie --desde 12701 --n 20 --pool 6`.
- **Réplica:** `--desde 12721`.
- **Costo:** ≈ 14 000 s de CPU, ≈ 40 min de pared cada una (120 tareas).
- **Puntos si se replica:**

  | resultado | puntos |
  |---|---|
  | FUNCIONA | +8 |
  | ACUMULA | +2 |
  | MODESTO | +4 |
  | sin contenido | +1 |
  | NO | 0 |

  El máximo lleva el nivel 10 a ~20 %.
- **No verificado:**
  - que RES supere al ORÁCULO fuera de una semilla, y su causa (el 0 verdadero);
  - la persistencia a T = 100000;
  - que la réplica repita.
- **Lo que no resuelve este bloque:** el 80 % exige la familia que persiste y el alma que gana al azar.
- **Pista para el bloque siguiente, si el humo se confirma:** "la boca lee las dos filas" (el hijo del ORÁCULO muerde B con sed porque la tabla le dice 0 en esa fila).
