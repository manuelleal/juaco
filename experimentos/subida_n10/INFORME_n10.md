# INFORME n10: la familia que hereda en vida (creador del nivel 10, 23-sep-2026)

**Veredicto del paquete: listo para serie. Resultado: ninguno, porque no hay serie.** El humo es de una semilla de práctica y no es dato.

## Qué hice
- **Bloque elegido: C (familias/vivo).** En la pista v2 (generaciones que conviven, quimiostato), el organismo real del proyecto (FABRICA, el cerebro REL de `organismo_f9c`) no tiene ningún canal de herencia: su nodo se llenaba al morir el padre, y en v2 nadie nace de un muerto.
- **Por qué este y no ALMA o transmisión F1:** es la pieza de la brecha donde el organismo propio (no un carro de Opus escrito a mano) puede mostrar que la familia hereda contenido en vida y compite con él. Además no duplica lo que corre ahora (los monocultivos de `generaciones` y la réplica de `aprende_barrer`).
- **Mecanismo, con memoria nueva cero:** el padre vivo entrega en el parto lo que heredó más sus últimas 20 mordidas, y el hijo lo lee con la regla de F9, que no se toca. Se construyen cuatro carros por anclas desde `FABRICA.py`, y entre ellos cambia una línea:
  - NADA (== FABRICA);
  - PARTO (candidato);
  - BAR (control de contenido que puede ganar);
  - ORÁCULO (techo).
  - Más un brazo MIX: 3 + 3 + 3 carros en el mismo mundo.
- **Arnés `identidad_familia.py`: 26/26** (`identidad_familia_salida.txt`). NADA == FABRICA en toda la salida en 6 configuraciones (v1 y v2); el canal verificado por unidad (BAR no consume ningún rng).
- **Humo:** un proceso, 5 brazos, s12391, T = 20000, 142 s. JSON en `datos/humo/n10_humo_todos_s12391_T20000_20260923_153432.json`.

  | brazo | R0 de los nacidos | vida de los nacidos |
  |---|---|---|
  | NADA | 0.020 | 92 |
  | PARTO | 0.213 | 152.5 |
  | BAR | 0.068 | 87 |
  | ORÁCULO | 0.544 | 200 |

  - Ningún linaje sin extinción.
  - `gen_max`: 2 / 3 / 2 / 6.
  - En MIX se invierte: NADA 0.25, PARTO 0.059, con cohortes de 12–17.
- **Preregistro:** `PREREGISTRO_n10.md`, con 9 predicciones, criterio por la letra, vocabulario y puntos. Semillas nuevas: serie 12301–12320, réplica 12321–12340 (verificadas con grep en `bundle` y en los 8 worktrees).

## Qué falló (mis errores, declarados)
1. **La primera corrida del arnés dio 25/26.** La comprobación (P) comparaba salidas con etiquetas distintas (`FAMILIA_NADA` contra `FAMILIA_PARTO`), y la pista copia la etiqueta a la salida. La corregí con la misma etiqueta para los cuatro; no cambia la física. Resultado final: 26/26.
2. **Bug en la telemetría del humo:** `frac_mala_nacidos` salió 0.0 porque la pista guarda la causa como índice, no como texto. Está corregido en el runner y verificado con un humo de ruta (MIX, T = 3000, 1 corrida). Las cifras del humo principal para esa clave no valen.
3. **Mi medida de diseño original (`tam_carro`) no separa:** en v2, el fundador repone el linaje extinto, así que el tamaño es ≥ 9 por construcción. Humo: 9.48 / 9.64 / 9.50 / 11.11. La medida que decide pasó a ser el R0 de los nacidos (cambio escrito antes de la serie).
4. **El runner cambió después del humo** (sha `b570b18f…` → `db8dfdcb57cc0bc0`): causa, `exceso`, veredicto y contador P4b. No cambió la llamada a la física. Verifiqué la agregación final sin simular, sobre el crudo del humo.

## Qué queda
- **Serie y réplica** (coordinador, Pool ≤ 6), ≈ 45–60 min cada una:
  - `python experimentos/subida_n10/corre_n10.py --serie --desde 12301 --n 20 --pool 6`
  - y `--desde 12321`.
- **Lo que no resuelve este bloque:**
  - la familia que persiste (predigo que no: P7);
  - el alma que le gana al azar;
  - el evaluador de novedad (JUACO-ECO).
- **Puntos si se replica:** FUNCIONA +8, MODESTO +4, sin contenido +1, NO 0. Decide el director.
