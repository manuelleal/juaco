# PREREGISTRO — tronco_v14_3: el bicho real (v14.3) en la pista de ayer (creador, 23-sep-2026)

Misión: llegar a la AGI por este camino; el método manda sobre el cómo. Nivel 9 (candidato a tronco v14.3). Escrito **antes** del humo.

## 1. Pregunta y dato que la motiva
Ayer, en la pista escalada de la carrera (L = 360, 36 objetos, 9 linajes, un cuerpo vivo por linaje), sólo cruzaron H-1 carros cuya
**política escribió un LLM** (O1: R0 real 0.941 ×2; con fundador limpio, `r2o1mono` 9101–9120: 20/20 semillas). El organismo no
cruza: FABRICA 0.339, APR 0.375 (R0 de nacimientos reales, recalculado de los crudos sellados). **Dato leído de esos crudos (sin
correr nada):** FABRICA vive **~200 pasos** y muere **>99 % de veneno o sal** (16 105 + 24 897 de 41 009 muertes, 5001–5020); O1 vive
~2 800–3 400 pasos. La boca de FABRICA lee sólo la fila de la necesidad activa: con hambre, la sal vale 0 y se la come (H-BOCA). Y las
patas van al objeto **más cercano**, sea lo que sea. **Hallazgo lateral:** el carro FABRICA es **v14.1** en el mundo vivo (sin B-5):
la carrera de ayer corrió sin el tronco vigente.

## 2. Hipótesis
**H-v143:** v14.2 más tres piezas locales ya medidas por separado, sin política escrita, sube el R0 real del linaje en la misma pista:
1. **FILTRO con META** (port de `subida_n6`, rodea limpio 1.0 / 0.925): lo que el organismo recuerda como malo en **alguna** de sus
   dos filas de valor (y no es meta) no es objetivo de las patas **ni se muerde**, **sólo si hay meta** (algún objeto a la vista con
   valor > 0 en la fila activa).
2. **Boca TD heredada** (APR de `aprende_barrer`, gana a FABRICA 20/20 ×2): corrige la boca donde el filtro no veta.
3. **LIMPIAR no se escribe.** Si aparece, sale de la condición de meta de la pieza 1: sin meta, las patas vuelven a lo más cercano y
   la boca de la fila activa muerde lo que golpea a la **otra** necesidad (la más llena), que es la limpieza costeable de O1.

## 3. Mecanismo mínimo y memoria nueva
`carros_v143/*.py`, construidos **por anclas** (`construye_v143.py`) desde `carros/APR.py` (`4402aa5142065c72`) con B-5 **literal**
de `organismo/organismo_v142.py` (`17528d767fcebaf6`, congelado, sólo se lee) y su port a dos necesidades
(`creacion_B/organismo_vivo_codigo.py`, `839fa71f9c84cb26`); el texto del filtro se verifica en `subida_n6/mundo_subida.py`
(`484e34db8f2150da`). **Memoria nueva: CERO** en B-5, FILTRO, META e INVIERTE (leen las dos filas que ya existen, se recalculan cada
paso, no persisten). La de la pieza 2 es la de APR (Q 2×6 + dS sentido por letra), ya medida y declarada. **Constantes nuevas: cero**
(meta y obstáculo usan el signo, 0). Diferencia declarada con n6: allí la retina era local y el mapa M recordaba sitios; aquí la pista
entrega todos los objetos (opción A de la carrera), así que "M" es lo visible y el port es el filtro, no el campo difundido.

## 4. Instrumento y anclas
- Pista y juez de la carrera **sin tocar** (`pista.py` `9f47c65e438e0ff4`, `juez.py` `6a68f640a7832f12`): monocultivo de 9, pista v1
  escalada, olvido escalado, `T = 100000`, **fundador limpio = 1** (ENMIENDA 5; ERR-101 cerrado por construcción). ERR-118: no se usa la
  pista v2. **Reserva ERR-104 vigente:** morder repone al instante una letra al azar.
- Arnés `identidad_v143.py` (salida en `identidad_v143_salida.txt`): perillas en 0 == FABRICA == monolito `organismo_f9c` REL bit a
  bit; sólo OPCION == APR bit a bit; B-5 sólo divide con R = 0 (tabla verdadera, que lee el arnés y no el carro); el filtro nunca apunta
  ni muerde un obstáculo con meta; regla 14 (`corre_v143.tarea == juez.tarea`); el corredor aborta ante banderas desconocidas (ERR-115).
- **Identidad con v14.2:** no existe un monolito "v14.2 en el mundo vivo con nodo" para comparar bit a bit. Lo que se verifica es
  (a) perillas en 0 == v14.1 del mundo vivo (FABRICA/f9c) bit a bit y (b) B-5 == el literal de `organismo_v142.py` y sólo actúa con
  R = 0. **Declarado como límite**, no como identidad.

## 5. Brazos (9 carros iguales por corrida) y controles
| brazo | carro | qué prueba |
|---|---|---|
| fab | FABRICA (v14.1) | piso y ANCLA 1 |
| v142 | FABRICA + B-5 | el tronco vigente en la pista |
| **v143** | + FILTRO/META + TD | **el candidato** |
| sinfiltro | v143 sin pieza 1 | lesión 1 (= APR + B-5) |
| sintd | v143 sin pieza 2 | lesión 2 — **el control que puede ganar** |
| siempre | filtro también sin meta | lesión 3: no puede limpiar (debe caer: "mundo que se come la comida") |
| invertido | el filtro lee la letra pareja (A↔B, C↔D) | control de contenido (debe caer) |
| o1 | O1 (escrito a mano) | techo y ANCLA 2 |

Cuatro trampas: **canal simétrico** — no hay canal (nadie escribe en la pizarra; el corredor lo cuenta); **acierto sin balancear** —
no se mide acierto, se mide R0 por linaje con pareado por semilla; **mundo que se come la comida** — se reporta la fracción de pasos
sin nada bueno en el mundo y SIEMPRE es su control; **sitios fijos** — objetos y posiciones iniciales sorteados por semilla.

## 6. Predicciones firmadas (medianas; el corredor las evalúa por la letra)
| # | predicción | p |
|---|---|---|
| V-ANCLA-1 | FABRICA: R0 real en [0.22, 0.45] (si no, NO SE LEE) — **enmendada tras el humo a [0.08, 0.20], ver §11** | 0.85 |
| V-ANCLA-2 | O1 gana por la ENMIENDA 5 (si no, NO SE LEE) | 0.90 |
| P1 | V142 ≈ FABRICA: \|dif pareada\| ≤ 0.05 | 0.65 |
| **P2** | **V143 > V142 en ≥ 18/20, dif ≥ 0.10** | 0.75 |
| P3 | V143: R0 real en [0.45, 0.85] | 0.55 |
| **P4** | **V143 NO gana por la ENMIENDA 5 (no cruza)** | 0.80 |
| **P5** | SIEMPRE < V143 en ≥ 15/20 y su mundo sin nada bueno ≥ 0.30 de los pasos | 0.70 |
| P6 | SINFILTRO en [0.30, 0.47] y V143 > SINFILTRO en ≥ 15/20 | 0.70 |
| P7 | SINTD ≈ V143 (\|dif\| ≤ 0.05) | 0.50 |
| P8 | INVERTIDO < V142 en ≥ 15/20 | 0.80 |
| P9 | V143 vive ≥ 3× lo que V142 | 0.70 |
| P10 | V143: veneno + sal ≤ 50 % de las causas de muerte | 0.70 |
| P11 | V143: pasos sin nada bueno en el mundo en [0.01, 0.30] | 0.65 |

Las que pueden fallar de verdad: **P2** (si el filtro no ayuda, el bloque cae), **P4** (predigo que NO cruza) y **P5** (si SIEMPRE
no cae, la limpieza no emerge de la meta y el mecanismo es otro). Probabilidad de cruzar: **0.15–0.20**.

## 7. Criterio (por la letra; `corre_v143.veredicto`)
- **NO SE LEE:** cae V-ANCLA-1 o V-ANCLA-2 en la serie.
- **FUNCIONA:** en la serie **y** en la réplica: V143 gana la ENMIENDA 5 (R0 real ≥ 0.90, 0 fundadores tras 10 000 y ≥ 5 muertes en
  más de la mitad de los linajes, en ≥ 15/20 semillas) **y** estabiliza por la ENMIENDA 6 (≥ 15/20), SIEMPRE e INVERTIDO no ganan, y
  V143 > V142 en ≥ 15/20. Frase permitida: *"en la pista escalada de la carrera (reposición inmediata, ERR-104), un linaje del
  organismo v14.3, sin política escrita, sostiene R0 de nacimientos reales ≥ 0.90 con fundador limpio, replicado; la limpieza aparece
  sin escribirse (su lesión cae)"*. Qué piezas son necesarias lo dicen las lesiones que caen.
- **HAY ALGO MODESTO:** no FUNCIONA, y en las dos: V143 > V142 en ≥ 15/20 con dif ≥ 0.10 **y** V143 > SIEMPRE en ≥ 15/20. Frase:
  *"el organismo con piezas locales cierra parte de la brecha con O1 en la pista de ayer, replicado; no cruza H-1"*.
- **NO:** lo demás. Vocabulario prohibido: "población", "generación", "evoluciona", "coopera", "planifica", "el bicho está resuelto".

## 8. Puntos del nivel (propuesta; decide el director)
| resultado | nivel 9 (hoy 50 %) | nivel 6 (hoy 50 %) |
|---|---|---|
| FUNCIONA | **→ 65 %** (el organismo, no un carro escrito, cruza H-1 en la pista del primer cruce) + candidato al examen de tronco (§10) | +5 si SINFILTRO cae en las dos (el filtro de n6 portado a v14.2 y a otro mundo) |
| HAY ALGO MODESTO | +3 (→ 53 %) | +2 si SINFILTRO cae en las dos |
| NO | 0; queda nombrada la pieza que falta (INFORME) | 0 |

## 9. Semillas (nuevas; `grep` en `bundle` y en todos los worktrees de `PROYECTOS/JUACO/*`: 0 usos como semilla)
Humo/práctica **14281–14290** (el arnés usa 14281–14284) · serie **14301–14320** · réplica **14321–14340**. El corredor se niega a
usar otras.

## 10. Comandos (sólo el coordinador) y costo
```
python experimentos/tronco_v14_3/identidad_v143.py                      # RESULTADO: N/N antes de nada
python experimentos/tronco_v14_3/corre_v143.py --serie fab,v142,v143,sinfiltro,sintd,siempre,invertido,o1 --desde 14301 --n 20 --pool 6
python experimentos/tronco_v14_3/corre_v143.py --serie v143,v142,sinfiltro,sintd,siempre,invertido --desde 14321 --n 20 --pool 6 --con <los 8 crudos _<brazo>.json de la serie, separados por coma>
```
Costo (medido en el humo y el arnés, con la CACHE de §11): ~180 s de CPU por corrida de T = 100 000 (V14x y FABRICA), ~360 s O1. Serie 160 corridas ≈ 9 h de CPU ≈ **1.5–1.8 h de pared con Pool 6**; réplica 120 corridas ≈ 6 h de CPU ≈ **1–1.2 h**. **Examen de tronco (CRITERIO_TRONCO_v4), sólo si FUNCIONA:** el examen corre sobre
`organismo_v3cal` (mundo vivo de un cuerpo), no sobre la pista. Paso 1 (por construir, tanda 2): `construye_v143cal.py` porta FILTRO/META
y la boca TD a `experimentos/criterio_v3/organismo_v3cal.py` (`148014f68cb01785`) por anclas, con arnés "perillas 0 == v3cal". Paso 2:
`python experimentos/criterio_v4/corre_criterio_v4.py --humo` sobre el candidato y luego la serie T-A/T-C(ii) a n = 80 con TRONCO_B y
PLACEBO (~480 corridas, ~20 min con Pool 6, el doble con réplica), `bateria_v142.py` / `bateria_generaliza_v142.py` por anclas (T-B,
T-C i, T-D, T-E). T-G (capacidad nueva) = el cruce de §7 con su lesión SIEMPRE como control. Riesgo declarado: la pieza 2 necesita un
linaje (herencia de Q) que el mundo de T-A sólo tiene con `muerte_real`; si no porta, v14.3 = v14.2 + FILTRO.

## 11. ENMIENDA 1 — **ERR-119** (tras el humo del 23-sep, 18:39; numerado por el coordinador según la regla 11)
1. **V-ANCLA-1 pasa de [0.22, 0.45] a [0.08, 0.20].** Motivo: el rango se escribió con la calibración de fundador **no** limpio
   (sellada 5001–5020: 0.339). Con fundador limpio, FABRICA da 0.113–0.129 en las cinco series `r2fab` de ayer (9101–9140, 600 linajes;
   por semilla 0.098–0.151; leídas de los crudos, no corridas) y 0.145 en el humo. Esos crudos existían y no los leí antes de escribir
   el ancla: es el patrón de ERR-116. Sin la enmienda la serie saldría NO SE LEE por un ancla mal puesta, no por el candidato.
   **Las predicciones P1–P11 NO se tocan**; declaro que P3 y P6 se escribieron pensando en ese mismo piso (0.34–0.38) y espero que P6
   caiga por su rango.
2. **CACHE de las dos filas por letra** (sólo rendimiento): se recalculan al morder o al nacer, no en cada paso. Arnés (7g): con y sin
   cache, bit a bit. Baja la corrida de V143 de ~94 s a ~39 s por 20 000 pasos. No cambia conducta.
3. **Fallo hallado por el arnés ANTES del humo** (no enmienda de diseño): en SIEMPRE todo podía quedar como obstáculo y `_see` devolvía
   nada; se añadió el respaldo "lo más cercano" (inerte en V143: arnés (7f), `todo_obst` 0).
