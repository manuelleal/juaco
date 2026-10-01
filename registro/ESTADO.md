> **Ruta de publicación:** ver `registro/RUTA.md` (casilla actual y siguiente paso).

# ESTADO: una página que se reescribe en cada cierre (skill `/juaco-cierre`)

> Última reescritura: **1-oct-2026, ~00:30** (cierre de la jornada del 30-sep), por el coordinador. Rama `organelos`, todo empujado.
> Sin merge a `main` (lo decide el director). Detalle en `REGISTRO_etapas_1_2.md` ("Jornada del 30-sep-2026") y en `experimentos/organelos/escalera/ESCALERA.md`.

## Tronco
**v14.3** (tag `v14.3-tronco`) sigue siendo el tronco. Candidato v14.4: TERMO′ (sólo cae T-E). Sin cambios.

## Lo declarado el 30-sep (serie + réplica)
1. **★★ ESCALERA P1, memoria de lugar: FUNCIONA ×2.** 79 y 85 linajes de 180 contra 0 del control antípoda, 20/20 ×2.
2. **★ ESCALERA P7, señal con significado dado entre linajes clones, con costo: FUNCIONA ×2 con reserva (ERR-175).** 132 y 124 contra 80 del
   mudo y 50 del control; mayorías 18 y 19 de 20.
3. **★★ ESCALERA P10, ir a lo menos visitado cuando el oasis se muda: FUNCIONA ×2.** 164 y 163 de 180; mayoría en 20/20 ×2; R0 0.96.

Los tres son DISEÑO DIRIGIDO (ingeniería genética sobre O1) y valen EN EL MUNDO CON OASIS. No son selección ni el muro de la pista vieja.

## El muro de la pista vieja (H-1): sigue en pie; qué sabemos ahora
- **La selección conserva a O1, no lo mejora** (o1_evo: 128 vs 81 del neutro, pero 128 vs 135 de fábrica; visto también en entre_linajes y en o1_libre).
- **La moneda era un candado:** con pasajes de 25k la selección PURGA la regla que cruza (0.26 vs 0.64); con pasajes de 100k y siembra sólo de
  establecidos la CONSERVA y la sube (0.80 vs 0.14; exploratorio, en el umbral). **Pero conservarla no hizo cruzar más** (17 vs 23): hay otro candado.
- **El montaje tenía defectos medibles:** genoma BQ2 clavado en 2 reglas (Δlargo 0), carga mutacional ~0.11 por regla y generación, Ne ≈ 9.
- Las piezas de O1 sueltas no funcionan; O1 funciona como conjunto (29-sep).

## La Escalera (`experimentos/organelos/escalera/ESCALERA.md`, `BITACORA.md`)
| peldaño | estado |
|---|---|
| P0 unicelular (O1) | hecho |
| P1 memoria de lugar | **FUNCIONA ×2** |
| P7 señal con costo | **FUNCIONA ×2** (reserva ERR-175) |
| P10 ir a lo menos visitado | **FUNCIONA ×2** |
| P8 componer | sin señal por la letra en 2 humos; rediseñar la medida |
| P9 planear | CERRADO en ráfaga (3 humos; el mundo con llave mata a todos) |
| P2 colonia pegada | CERRADO en ráfaga (5 humos) |
| P3–P6 germen/soma, órganos, nervio, cerebro | diseñados, sin correr (dependen de P2 o de ECO grande) |
| Tramo D sexo y familia | instrumentado; sin señal: el mundo de 9 no tiene población para familias |

## Novedad de la madrugada (1-oct): "los tres juntos" — **NO SUMAN ×2** (cerrado)
Serie `f3054b56` y réplica `b1f5f0e6` (preregistro `1b5e483f`). Linajes que cruzan de 180: los tres juntos 159 y 169; memoria + ir a lo menos
visitado 163 y 163; memoria + señal 129 y 129; sólo memoria 88 y 95; los tres con la señal al antípoda 90 y 95. Las tres capacidades no se
estorban, pero la señal NO agrega cruce sobre memoria + ir a lo menos visitado; su contenido sí importa (leída al revés cae a 90–95).
Vocabulario: decir "tres módulos diseñados, cada uno contra un control de contenido equivocado; juntos no suman", no "un organismo que
recuerda, señala y explora" como si los tres aportaran.

## Otra sesión (JUACO 5, rama `o1-libre`, commit `23a6c83d`)
O1 libre con poderes: **BLOQUE NO** (serie MODESTO, réplica NO). La memoria de lugar subió por selección en 10/10 en la serie (dif 0.0596)
pero **no replicó** (6/10, dif 0.047 < 0.05). Conquista 4/10 ×2. Lo que sí se repite ×2: la selección sostiene a O1 frente a la deriva
(R0 0.96–0.98 contra 0.62–0.80 del neutro) y no lo supera. **No decir** "la selección elige la memoria de lugar". Cierre en
`experimentos/organelos/o1_libre/CIERRE_o1_libre.md` (rama o1-libre). JUACO 5: siguiente ERR libre de su bloque, ERR-161.

## PLAN DE LA MAÑANA (el director viaja; prende el PC y lo deja corriendo; poco gasto de tokens)
En orden; cada uno con su preregistro commiteado antes y pool total ≤ 6:
1. **Réplica de moneda_muro** (está en el umbral; 5 cadenas nuevas, ~1 h con pool 2). Comando tras preregistro de réplica:
   `python experimentos/organelos/condiciones/moneda_muro/corre_mm.py --explora --pool 2` con semillas nuevas (necesita un creador: el runner no tiene `--replica`).
2. **P1 + P7 + P10 juntos en un solo organismo** ("recuerda, señala y va a lo menos visitado") en un mundo con oasis que se muda: ¿se suman? Un creador + auditor + serie.
3. **Selección sobre las perillas de los peldaños** (como o1_evo): W de la memoria de lugar, umbral de emisión, ε de exploración como genes; control neutro `PS_LEE 0`.
4. **P8 con medida nueva** (excluir la limpieza de O1) y **P9 en un mundo donde la base viva**.
5. **ECO grande para el tramo D** (familias): es construcción seria, no de una mañana.
No hacer: más vueltas de pasajes de 25k contra el muro; piezas sueltas de O1.

## Niveles (los fija el director)
+2 por el termostato-en-la-pista ×2 (aceptado el 29-sep; total +17–22). Propuesta del coordinador por la Escalera: decidirlo el director al
leer; los tres peldaños son diseño dirigido en un mundo propio, no selección.

## ERR
Esta sesión usó el 30-sep: ERR-157, 158, 159 y 170 a 176. JUACO 5 tiene el bloque 160–169 (usó el 160). **Siguiente libre de esta sesión: ERR-177.**

## Decisiones para el director (máximo 2)
1. ¿Se juntan P1 + P7 + P10 en un solo organismo como siguiente serie, o se replica primero moneda_muro?
2. Merge de `organelos` (y de `o1-libre`) a `main`, y si los tres peldaños entran a `RESULTADOS_VERIFICADOS.md` (lo toca la sesión de publicación).
