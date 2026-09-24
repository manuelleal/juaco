EXPLORATORIO — no es dato

# Frankenstein de JUACO (creador, 23-sep-2026, pedido del director: "haz un Frankenstein con todo… y lo sueltas en el mundo")

**Veredicto: HAY ALGO MODESTO.** El bicho del tronco con los seis órganos vive unas tres veces más que FABRICA y algunos linajes
duran (7/27 contra 0/27). No cruza H-1. O1, con su regla escrita a mano, sigue muy por encima. No sube ningún nivel.

## Qué es
- `organismo_frankenstein.py` (`baff124177d44e90`) se construye por anclas (`construye_frankenstein.py`) desde FABRICA (`2ebee3e99ea5a33a`), el cerebro del mundo vivo
  del linaje v14.1. APR (`4402aa5142065c72`) se pega sin tocar.
- Tiene 7 perillas: `b5` (B-5 de v14.2) y seis órganos:
  1. mapa: campo de valor con el veneno recordado como pared;
  2. curiosidad: lee como neutro lo no reconocido y no probado, 2 veces por cuerpo;
  3. modelo de sí: la opción de APR con `post`, aprendida por TD;
  4. memoria lenta: `Wc` del linaje, que consolida repasando cada 10 pasos lo que dice la memoria rápida (prototipo propio);
  5. herencia: la tabla vivida del padre, portada sin cambios de n10b `res`;
  6. interruptor: en peligro (u<0.3) veta lo que sintió malo; con hambre arriesga; saciado explora.
- **Memoria nueva por cuerpo:** Q 12 + lo sentido 12 + `Wc` 12 + ~5 escalares de TD + 2 contadores, **≈ 43 números**. Trabajo: caché de 8 valores y blanco.
  Herencia: 0 nuevos (reusa el nodo; el mensaje lleva ≤ 8 entradas).
- **"Todo off == v14.2":** todo en 0 da **FABRICA bit a bit** (v14.1 en el mundo vivo). `V142` = off + B-5 (portado de `organismo_v142.py:162-166`).
  No se compara bit a bit con `organismo_v142` porque el mundo es otro. Lo declaro.

## Arnés `identidad_frankenstein.py`: **RESULTADO 33/33** (97 s, `identidad_frankenstein_salida.txt`)
```
(A1) OFF == FABRICA N1 compat s1,s2 salida entera · (A2) == monolito organismo_f9c(REL) 76 claves dif [] · (A3) N9 escalada · (A4) pista v2 quimiostato
(B1) SOLO_MODELO == APR (física + telemetría de la opción) · (B2) SOLO_HERENCIA == FAMB_RES (n10b) en pista v2
(C) V142 y cada órgano solo difieren de OFF; B-5 divide con R==0 (33) · (D) determinismo · (E) revisa_carro, sin tabla verdadera, sin rng propio
(F) corre_frankenstein aborta 8 formas malas (código 2) sin escribir datos · RESULTADO: 33/33
```

## Números (N = 9 del mismo brazo; mediana de las 3 semillas del R0 de nacimientos reales; "persisten" = 0 fundadores tras 10000 y ≥ 5 nacimientos)
**(a) Pista escalada de la carrera, fundador limpio, T 30000, semillas 17001–17003**
(`python experimentos/frankenstein/corre_frankenstein.py --mundo carrera --brazos X,Y --semillas 17001,17002,17003 --T 30000 --etiqueta a`; tabla `datos/tabla_carrera_T30000.txt`)

| brazo | R0 real (3 semillas) | persisten | muertes/linaje | vida mediana | % mordidas B+D | muere de veneno/sal |
|---|---|---|---|---|---|---|
| TODO | 0.181 / 0.118 / 0.174 | 7/27 | 63 | 200 | 45 % | 99 % |
| OFF = FABRICA | 0.122 / 0.150 / 0.116 | 0/27 | 112 | 67.5 | 47 % | 100 % |
| V142 (solo B-5) | 0.143 / 0.113 / 0.176 | 1/27 | 115 | 69 | 48 % | 100 % |
| SIN mapa / curiosidad / modelo / lenta | 0.217 / 0.233 / 0.204 / 0.200 (3/3 > TODO) | 5 / 6 / 5 / 7 | 52–63 | 200 | 45–46 % | 99 % |
| SIN herencia | 0.226 (3/3 > TODO) | **1/27** | 54 | 200 | 47 % | 99.8 % |
| SIN interruptor | **0.145** (TODO gana 2/3) | 5/27 | **106** | **64** | 47 % | 100 % |
| O1 (referencia) | 0.833 / 0.500 / 0.833 | 13/27 | 5 | 3565 | 36 % | 86 % |

Una semilla larga (17004, T = 100000, `--etiqueta largo`): TODO 0.249 (2/9 persisten; cruzan 2/9), OFF 0.150 (0/9), **O1 0.933 (8/9)**.
**El Frankenstein no cruza H-1. O1 sí cruza en esta semilla.**

**(b) Pista v2 con quimiostato (flujo fijo), T 20000, semillas 17101–17103** (`--mundo convive … --T 20000 --etiqueta b`; `datos/tabla_convive_T20000.txt`)

| brazo | linajes sin extinción | carro persiste | R0 fundadores (n) | R0 nacidos (n) | cuerpos | gen. máx. |
|---|---|---|---|---|---|---|
| TODO | 3/27 | 2/3 | 0.10–0.16 (596) | **0.44–0.94** (129) | 11–16 | 5–11 |
| OFF = FABRICA | 0/27 | 0/3 | 0.17–0.20 (751) | 0.04–0.18 (125) | 9.5 | 2–3 |
| SIN herencia | 0/27 | 0/3 | 0.18–0.21 (512) | 0.04–0.26 (95) | 10 | 2–3 |
| SIN modelo | 2/27 | 2/3 | 0.16–0.18 | 0.57–0.81 | 11–15 | 7–9 |
| SIN interruptor | 1/27 | 1/3 | 0.12–0.17 | 0.30–0.64 | 10–12 | 4–5 |
| O1 | 9/27 | 3/3 | 0.14–0.19 (443) | **0.97–1.02** (199) | 22–24 | 7–8 |

ERR-118 se ve aquí: los fundadores repuestos son malos en todos los brazos. Lo que separa a los brazos es el R0 de los **nacidos**.

## Qué hace el bicho (en palabras llanas)
- Nace con 0.6 en un mundo donde **~30 de los 36 objetos son veneno o sal**.
- Sabe lo que es malo porque se lo pasa el padre, pero lo bueno escasea y se lo comen los otros 8.
- Muerde una cosa mala temprano (sal casi siempre), queda con 0.2 y **muere justo 200 pasos después**: 44/178 vidas exactas en `diagnostico_frank.py`, s17001.
- El interruptor le impide seguir mordiendo lo malo: por eso vive 200 pasos y no 67 como FABRICA. Pero no le alcanza para llegar al agua.
- **El mapa casi no trabaja:** con 29 paredes de media, la meta más cercana está tapada el 49 % del tiempo, y solo en el 11 % de los pasos elige una meta.
  **Nunca rodea** (0 rodeos en (a)): en un mundo sucio, "el veneno es pared" deja al bicho encerrado.
- Curiosidad: 131 pruebas en 27 linajes × 30000 pasos, casi nada. Limpia (muerde lo malo con la necesidad más llena) unas 2600 veces por corrida, como FABRICA (2800).
  O1 limpia 930 veces y vive 18 veces más: limpia **cuando conviene**, no más.

## Qué órgano pesa más (ablaciones descriptivas; 3 semillas)
- **Interruptor** (el veto en peligro): quitarlo duplica las muertes (63 → 106) y la vida vuelve a ~64 pasos. Es el único órgano cuya ausencia baja el R0 real.
  Ojo: es el órgano **más escrito a mano**, lo más parecido a la regla de O1.
- **Herencia:** quitarla deja la persistencia en (a) de 7 a 1 de 27, y en (b) de 3 a 0 linajes, con los nacidos de 0.44–0.94 a 0.04–0.26.
  En el mundo con quimiostato es el órgano que decide, porque es la única vía entre cerebros.
- Mapa, curiosidad, modelo y memoria lenta: quitar cualquiera de ellos **sube** el R0 real (3/3 cada uno), sin cambio claro en la persistencia.
  O estorban juntos, o la métrica premia morir (ERR-102). Con 3 semillas no se separa una cosa de la otra.

## Predicciones propias (escritas antes, `predicciones_antes.txt`)
- **REFUTADA P-a1:** la mediana de TODO es 0.174, fuera de 0.25–0.50.
- Se cumplen P-a2 (TODO > OFF 2/3), P-a3 (O1 > TODO 3/3), P-a4 (el interruptor es el que más pesa), P-a5 y P-a6, P-b1 (2/3 y 0/3) y P-b2.
- P-a5 se cumple pero no es específica: quitar cualquier órgano sube el R0.

## Qué sorprendió
1. Que el todo sea peor que casi cualquier "todo menos uno" en R0 real.
2. Que lo que más pesa sea la regla más a mano.
3. Que el mapa con filtro quede ciego justo en el mundo donde más haría falta.

## Qué no se hizo
- (c) el mundo partido de subida_n6 y el flujo de n8: son monolitos v13 en otro mundo y portar el carro no cabía.
- Con 3 semillas no hay intervalos. En v2, los contadores de órganos son solo del último cuerpo de cada linaje.

## Qué valdría la pena rehacer con protocolo
1. **Herencia (n10b `res`) + interruptor** como par mínimo, en la pista v2 con quimiostato, con semillas selladas, BAR como control de contenido
   y el R0 de nacidos (ERR-118) como métrica.
2. **Un mapa que distinga "pared" de "puerta":** que pueda cruzar lo malo sin morder. Hoy la pared solo aparta el blanco.
3. Separar "órganos que estorban juntos" de "la métrica premia morir": repetir las ablaciones con la **persistencia** como métrica y 20 semillas.

Archivos (todos en `experimentos/frankenstein/`): `organos_frank.py`, `construye_frankenstein.py`, `organismo_frankenstein.py`, `comun_frank.py`, `identidad_frankenstein.py` (+ `_salida.txt`), `corre_frankenstein.py` (`--humo`),
`tabla_frank.py`, `diagnostico_frank.py`, `predicciones_antes.txt`, `datos/` (JSON por invocación, logs y tablas).
