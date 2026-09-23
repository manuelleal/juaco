# INFORME — subida del nivel 8, tanda 2 (creador, 23-sep-2026)

**Veredicto de los humos: HAY ALGO MODESTO, por confirmar; no es dato de serie.** El cuello del tronco en un mundo de 500 estímulos no
es sólo de celdas: es de **muestreo**. Muerde 4–8 veces cada comida en toda su vida y la puerta pide 5 mordidas del código exacto. Si
no se fía de su a priori para lo que no reconoce (órgano PRUEBA), aprende la comida temprana casi entera (0.93–1.0 contra 0.33–0.53).
Pero en cuanto se agotan las celdas choca con el muro (−0.48/−0.53). Probar al azar aprende igual o más y muere más. Reciclar
celdas no sostuvo nada de forma consistente. Serie 14801 y réplica 14821 sin correr (necesitan Pool). Manda `PREREGISTRO_n8b.md`
(`68d68cb6e079a5a7`).

## Qué hice
- **Instrumento por anclas:** `construye_n8b.py` (`f06946daadd82a6d`) genera dos archivos.
  - `organismo_n8b.py` (`f9f3b56b498f6fc7`), desde `subida_n8/organismo_flujo.py` (`14afed5aa16e09bf`), con 6 anclas. Añade
    dos perillas apagadas: `recicla` (1 = menor |Wp−Wn|, 3 = menos códigos familiares, 2 = azar) y `prueba` (1 = lectura neutra de
    lo no reconocido, 2 = neutra al azar a la tasa propia).
  - `mundo_n8b.py` (`74e6127ee3e36814`): retina de 13 px, peso 4, 500 estímulos, T = 500 000.
  - Memoria nueva: cero, salvo dos contadores del control PRAZAR. Constantes nuevas: cero.
- **Runner** `corre_n8b.py` (`86e63ec24ee219cf`), con tres modos excluyentes (`--humo`, `--serie`, `--veredicto`).
  - Usa `argparse` con `allow_abbrev=False`: toda bandera desconocida o abreviada aborta con código 2 (ERR-115).
  - `--serie` sólo acepta `--desde` 14801 o 14821, `--n 20` y un `--pool` explícito.
  - `--veredicto` aplica la letra del §6 a los dos JSON y la imprime en la **última línea**.

## Salida del arnés (`identidad_n8b.py` `227e8b9423771926` → `identidad_n8b_salida.txt`, 17:27:24)
```
(0a-0e) origenes, tronco v142 y construidos por sha OK · (A) x2 recicla=0 prueba=0 == organismo_flujo, 31 claves OK
(A1) x2 mundo n8 con pool agotado (fusion 0/1) == organismo_flujo OK · (A2) mundo n8b == organismo_flujo OK
(A3) x3 == organismo_v142 en W, muertes, divisiones, celdas, mordidas, visitas OK · (B) x3 reciclaje inerte con celdas libres OK
(C1-C6) recicla solo con el pool agotado, <= 90 celdas, rel/uso/azar distintos, == base hasta el primer reciclaje OK
(D) x2 determinismo OK · (P1-P5) PRUEBA neutra exactamente en los no reconocidos (243/2999); PRAZAR a su tasa (0.218 vs 0.209);
no lee valencias OK · (E0-E4) mundo: == mundo_n8, balance, 500 de peso 4, prefijo 200 == 500, reciclado OK · (F1-F2) sin rng
nuevo, sin canal OK · (G) regla 14: 175 campos, 0 distintos · (H1-H5) aborta: --bogus, --hum, --semila_humo, sin modo (rc 2),
--humo --pool 6; ningun dato escrito; 6/6 combinaciones malas · (I1-I5) letra sobre sinteticos; --veredicto: ultima linea = letra
TOTAL 50/50 en 94.5s
RESULTADO: 50/50
```

## Humo final (s14893, 200 estímulos, T = 200 000, UN proceso, 124 s; `datos/humo/…_s14893_…json`, `3eac360a371d675a`)
| brazo | comida tarde / a priori | comida temprana | RET40 (comida) | muertes | agota en |
|---|---|---|---|---|---|
| base | 0.56 / 0.20 | 0.53 | 0.575 (0.30) | 338 | 102 |
| prueba | 0.52 / 0.28 | 1.00 | 0.55 (0.35) | 316 | 36 |
| prazar | 0.72 / 0.36 | 0.93 | 0.525 (0.25) | 470 | 35 |
| uso | 0.60 / 0.36 | 0.53 | 0.60 (0.25) | 353 | 102 |
| pruso | 0.44 / 0.28 | 0.93 | 0.70 (0.45) | 316 | 36 |
| pruazar | 0.80 / 0.36 | 0.93 | 0.675 (0.55) | 401 | 36 |
| recic | 0.92 / 0.92 | 0.93 | 0.95 | 274 | — |

## Qué falló (declarado)
- **Predicciones mías que refutaron los humos, antes del preregistro:**
  - «reciclar por relevancia sostiene lo nuevo sin pagar con memoria». Pagó en 3 de 4 (`rel`/`uso`, 14890–14892), así que `rel`
    salió de los brazos.
  - «el cuello es de celdas». El cuello es primero de muestreo, y eso cambió el diseño a un factorial.
- **Tras el preregistro, en el humo 14893 (una semilla; no enmiendo nada):** caen mis P1 (agota en el estímulo 102 > 95), P2
  (0.36 > 0.20), P4, P7 (cociente 0.935), P11, P12 y P15 (PRUSO 0.70/0.45, PRUAZAR 0.675/0.55).
  - PRUAZAR aprende más que PRUSO por 0.36. **Confusión que declaro:** reciclar borra evidencia `ncod`, así que sube la tasa de
    no reconocidos (0.138 contra 0.062) y, con PRUEBA encendida, sube cuánto se prueba. Es probable que G3/G3b midan eso y no la
    elección de la celda.
- **Arnés:** la primera corrida falló en C1 por diseño del propio arnés (un mundo que agotaba el pool demasiado tarde). Se
  corrigió el arnés, no el instrumento.
- **Corridas usadas:** 4 humos de un proceso (14890–14893). Cada organismo corrió ≤ 200 000 pasos; fueron 4 a 7 organismos por
  proceso. Más 6 corridas del arnés.
  - El humo de 14892 usó un conjunto de brazos anterior (`azar` = reciclaje al azar sin PRUEBA).

## Qué queda
- **Serie y réplica** (comandos en el §9; ~3.2 h de CPU en total, ~40 min de pared con Pool 6). Luego `--veredicto`.
- **Puntos en juego** (propuesta; decide el director): pieza 1 +5, pieza 4 +3/+5, pieza 3 +5/+15, pieza 2 +10. Esperable según mis
  p: **+3 a +8**.
- **Fuera de este bloque:** el dominio distinto del anillo (pieza 7) y la curiosidad por progreso.
- **Lectura que se pierde si nadie la dice:** los humos apuntan a que *probar más* vale más que *elegir qué probar* para aprender,
  y que *elegir* sólo ahorra vidas.
- **No verifiqué:**
  - el tiempo a T = 500 000 (extrapolado);
  - la rama `Pool` (prohibida);
  - que las p de P3/P5 aguanten 500 estímulos: el humo no pasa de 200.
