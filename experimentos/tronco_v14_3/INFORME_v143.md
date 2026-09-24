# INFORME — tronco_v14_3: el bicho real en la pista de ayer (creador, 23-sep-2026). Una página

**Estado: LISTO PARA SERIE (lo corre el coordinador).** El humo, de una semilla y con T = 20 000, no es dato. Misión: llegar a la AGI
por este camino.

## Qué hice
1. **Leí los crudos de ayer antes de diseñar.** FABRICA vive ~200 pasos y muere de veneno o sal en más del 99 % de los casos: la boca
   lee sólo la fila activa y las patas van a lo más cercano. **FABRICA es v14.1**: la carrera corrió sin B-5.
2. **v14.3 = v14.2 + dos piezas medidas, y la limpieza sin escribirla.** Los carros salen por anclas desde `carros/APR.py`, con B-5
   literal de `organismo_v142.py` (congelado, sólo se lee). Las piezas son:
   - **FILTRO con META**, de `subida_n6`: lo recordado como malo en alguna fila no es objetivo ni se muerde, sólo si hay meta.
   - **La boca TD de APR.**
   - **Limpiar:** debería salir sola de la condición de meta. Su lesión es `SIEMPRE`.
   Memoria nueva: cero, fuera de la de APR, que ya está declarada. Constantes nuevas: cero.
3. **Arnés `identidad_v143.py`: RESULTADO 36/36** (`identidad_v143_salida.txt`, JSON `datos/humo/identidad_v143_20260923_185646.json`):
   ```
   (0a/0b) shas de los orígenes OK; carros en disco == construye · (1) revisa_carro PASA x6; no nombran VAL_VIVO/EFECTO
   (2) perillas 0 == FABRICA, N1 compat1 T20000 s1-3 (rng incluido) x3 · (3) == monolito organismo_f9c REL, 76 claves, dif []
   (4) las 6 variantes con perillas 0 == 9 FABRICA (fundador limpio) x6 · (5) sólo OPCION == APR bit a bit
   (6) B-5: 14 divisiones, todas con efecto 0 en la necesidad activa; texto == organismo_v142 · (7a-g) el filtro con meta nunca apunta
   ni muerde un obstáculo (pasa por encima 4122 veces); sin meta no hay obstáculos; SIEMPRE sí; CACHE == sin CACHE
   (8) variantes distintas, determinismo · (9) aborta ante banderas desconocidas o abreviadas; rechaza semillas ajenas; regla 14 OK
   ```
4. **Humo** (`--humo`, semilla 14281, T 20 000, 6 corridas, 428 s; `datos/humo/v143_humo_…_183935_*.json`, resumen `05c9512b8f91f725`):

| brazo | R0 real (mediana) | linajes sin fundadores tras 10 000 | vida mediana | veneno + sal en las causas | notas |
|---|---|---|---|---|---|
| FABRICA | 0.145 | 0/9 | 68 | 100 % | 70 muertes por linaje |
| V142 | 0.159 | 0/9 | 68 | 100 % | 29 divisiones B-5 |
| **V143** | **0.044** | **6/9** | 113 | 94 % | es bimodal: 2 linajes a 0.86/0.875 (vida ~2000, sin fundadores); 3 atascados (114–139 fundadores) |
| SINTD | 0.154 | 7/9 | 74 | 95 % | 1 linaje casi inmortal |
| SIEMPRE | 0.000 | 1/9 | 200 | 83 % | 0 nacimientos reales en 8/9 |
| O1 | 0.500 | 8/9 | 4354 | 87 % | 7/9 casi inmortales a T = 20 000 |

## Qué falló (declarado)
- **El ancla V-ANCLA-1 estaba mal calibrada: candidato a ERR.** La escribí con fundador no limpio (0.34). Con fundador limpio, FABRICA da
  0.113–0.129 en las cinco series `r2fab` de ayer. Esos crudos ya existían y no los leí. Tras el humo quedó enmendada a [0.08, 0.20]
  (PREREGISTRO §11). Las predicciones no se tocaron.
- **Predicciones que el humo contradice** (no cuentan, pero las declaro):
  - P2: V143 < V142.
  - P3 y P9–P11 fuera de rango.
  - La segunda cláusula de P5: el mundo de SIEMPRE no se ensucia, porque sus cuerpos mueren antes.
  - P6: espero que caiga por su rango, escrito para el piso de fundador no limpio.
- **El arnés halló un fallo antes del humo.** En SIEMPRE, `_see` podía no devolver nada. Lo reparé con un respaldo, que en V143 es
  inerte.
- **El humo tardó 7 min, no 5.** Luego añadí una CACHE que da lo mismo bit a bit y baja el costo 2.4 veces.

## Qué queda
- **Serie y réplica** (sólo el coordinador; ~1.5–1.8 h y ~1–1.2 h de pared con Pool 6; ~15 h de CPU en total):
  - Serie: `python experimentos/tronco_v14_3/corre_v143.py --serie fab,v142,v143,sinfiltro,sintd,siempre,invertido,o1 --desde 14301 --n 20 --pool 6`
  - Réplica: `python experimentos/tronco_v14_3/corre_v143.py --serie v143,v142,sinfiltro,sintd,siempre,invertido --desde 14321 --n 20 --pool 6 --con <8 crudos de la serie>`
  - Al final, cada corrida imprime `VEREDICTO:` por la letra.
- **Mi lectura antes de la serie: probablemente NO cruza** (P4, p 0.80). El humo sugiere por qué, y eso apunta a **la pieza que falta**.
  - Con fundador limpio, el ENMIENDA 5 cuenta cada fundador ingenuo que muere antes de establecerse. Los linajes de V143 que se
    establecen se parecen a O1: sin fundadores y con cola de hijos.
  - Los que no se establecen muerden letras desconocidas con dote 0.6 y mueren en ~50 pasos. O1 no lo hace: sólo prueba una letra
    desconocida si E y Ag > 0.5 (`PRUEBA`).
  - **Pieza candidata, local y biológica: neofobia regulada por la reserva.** La boca se contiene ante un código poco familiar
    (`ncod` bajo y valor lento ≈ 0) cuando min(E, Ag) es bajo. Cero memoria nueva, un umbral. Va a otro paquete, no a éste.
- **Examen de tronco** (sólo si FUNCIONA): hay que portar FILTRO y la boca TD a `organismo_v3cal` por anclas y correr `criterio_v4`
  (PREREGISTRO §10). Los comandos están ahí; el paquete no está construido.
- **Puntos:** FUNCIONA sube el nivel 9 a 65 % (y +5 al nivel 6 si SINFILTRO cae); HAY ALGO MODESTO, +3; NO, 0.
- **No verificado:**
  - la calibración del ancla en monocultivo FABRICA con fundador limpio a T = 100 000 (sólo en pista mixta);
  - INVERTIDO y SINFILTRO sin humo;
  - la identidad bit a bit con un v14.2 del mundo vivo, que no existe como monolito;
  - si la condición de fundador limpio es la que el director quiere para "lo de ayer". El primer cruce de O1 fue sin fundador limpio,
    y su réplica S-FUNDBORRA también cruzó.
