# Resumen de errores ERR-1 … ERR-153 (generado por `informe/construye_errores.py`; no editar a mano)

Generado: 2026-09-29. Fuente de verdad: `informe/errores.csv` (definiciones en `definiciones_errores.json`, clasificación en `clasificacion_errores.json`).

## Inventario
- Números 1..153: **126 con definición**, **27 "no encontrado"**: 55, 56, 57, 58, 59, 65, 66, 67, 68, 69, 72, 73, 74, 75, 76, 77, 78, 79, 127, 128, 129, 135, 136, 137, 138, 139, 145.
  Ninguno de esos números aparece en ninguna rama local ni remota (git grep sobre todas las refs). `REGISTRO_etapas_1_2.md:6750` declara sin uso 127–129 y 135–139; ERR-145 sólo aparece como "desde ERR-145" en `experimentos/organelos/prometeo_cuerpo/PREDICCIONES_previas.md:37`.
- ERR-1..4 no llevan número escrito: se reconstruyen por el ordinal del registro (`REGISTRO_etapas_1_2.md:192` y `:333`: "unidades 2H, disponibilidad 2I, aliasing ANOM-01, aritmética del techo 2K"). `registro/investigacion/sala2/DIAG_metodo.md:361` ya lo notaba ("ERR-01/02/04 con otro formato").
- ERR-151 vive sólo en la rama `origin/nube/eco-sel-largo-20260928` (allí se llama "ERR-150"); leído con `git show`.
- Números por encima de 153 citados en el árbol: [154] (sólo como "siguiente libre").
- Entradas numeradas que NO describen un error cometido (reservas condicionales, cláusulas de cierre): 6 → ERR-50, ERR-62, ERR-80, ERR-81, ERR-82, ERR-83.
- Duplicados e inconsistencias de numeración: ERR-07 dos veces (los artefactos del exp. 2b llaman "ERR-07" al ERR-09, `REGISTRO_etapas_1_2.md:737-743`); "ERR-150" dos veces (main = T-C ii; rama nube = ERR-151, `experimentos/organelos/eco_sel_largo/ENCARGO_NUBE.md:78-80`); ERR-151 y ERR-152 son el mismo defecto de fondo (σ = 0 no apaga los genes enteros); ERR-50 y ERR-51 son el mismo suceso (parada del bloque 4); ERR-64 tiene variante "ERR-64b" y ERR-37 tiene a/b/c; "ERR-3" se cita como "recalibrar tras ver datos" (es la regla 3) en `experimentos/criterio_v3/PREREGISTRO_calibracion_v3.md:181`, `experimentos/criterio_v4/PREREGISTRO_calibracion_v4.md:82` y `experimentos/junta_20260921/A/PROPUESTA.md:91,190`.

## Vocabulario y convenciones de la clasificación (decididas antes de contar)
- **tipo**
  - `instrumento`: el código, la copia, el runner, el arnés o el montaje del mundo producen números falsos, perdidos o
    vacíos (comparadores, claves, rutas, kwargs perdidos, casos de arnés mal hechos, mundos que no hacen la prueba).
  - `criterio`: la letra escrita (umbral, banda, puerta, control, medida) no mide lo que dice o no puede fallar o pasar;
    incluye los cambios de letra tras ver datos que se numeraron por la regla 11.
  - `generalizacion_indebida_del_criterio`: un criterio, control o calibración válido en un organismo, etapa o
    instrumento se aplica a otro donde su premisa ya no vale. Nombre tomado del registro (`REGISTRO_etapas_1_2.md:333`).
  - `fabricacion_o_fuera_de_mandato`: afirmación sin la medición que la respalde, o agente que actúa fuera de su mandato
    (matar procesos, lanzar una serie, cambiar la letra por su cuenta).
  - `concurrencia`: choque de procesos o recursos compartidos (Pool, CPU).
  - `otro`: aritmética de una predicción, erratas, omisiones de informe, defecto del organismo (no del método), y los
    números usados para reservas o cláusulas de cierre (`no_es_error`).
- **quien_lo_cometio / quien_lo_atrapo**: sólo se llenan si el texto lo dice ("mío", "creador A", "auditor",
  "cronista", "director"...). `coordinador` = la sesión principal de Claude, incluidos los días 1–4, antes de que
  existieran los roles; cuando el registro habla en primera persona ("mío", "lo encontré"), se asigna a ella.
  `arnes` / `humo` = el fallo lo destapó la corrida de identidad o el humo. Todo lo demás, `no_determinable`.
- **tiempo_hasta_detectarlo**: `antes_de_la_serie` (antes de la serie cuyo resultado habría tocado),
  `despues_de_la_serie` (tras correrla, el mismo día), `dias` (uno o más días después), `misma_sesion` (sin serie de
  por medio: afirmaciones, procedimiento, procesos).
- **altero_conclusion**: `si` sólo si un veredicto o una lectura ya declarada tuvo que corregirse (incluye magnitudes
  y reservas sobre un resultado ya declarado). Las entradas `no_es_error` llevan `no_determinable`: no aplica.

## Por tipo (n = 126)
| valor | n |
|---|---|
| criterio | 53 |
| instrumento | 47 |
| otro | 12 |
| generalizacion_indebida_del_criterio | 9 |
| fabricacion_o_fuera_de_mandato | 4 |
| concurrencia | 1 |

## Por quien_lo_cometio (n = 126)
| valor | n |
|---|---|
| no_determinable | 66 |
| creador | 38 |
| coordinador | 13 |
| agente_externo | 7 |
| auditor | 1 |
| nube | 1 |

## Por quien_lo_atrapo (n = 126)
| valor | n |
|---|---|
| no_determinable | 37 |
| creador | 32 |
| auditor | 22 |
| coordinador | 15 |
| arnes | 8 |
| humo | 8 |
| cronista | 2 |
| director | 1 |
| agente_externo | 1 |

## Por altero_conclusion (n = 126)
| valor | n |
|---|---|
| no | 105 |
| si | 14 |
| no_determinable | 7 |

## Por tiempo_hasta_detectarlo (n = 126)
| valor | n |
|---|---|
| despues_de_la_serie | 53 |
| antes_de_la_serie | 49 |
| dias | 11 |
| misma_sesion | 7 |
| no_determinable | 6 |

## La X de la tesis
**Cómo se calcula.** X = número de ERR con definición que describen un error (se excluyen las 6 reservas/cláusulas marcadas `no_es_error`) y cuyo `altero_conclusion` es "no": el error se atrapó (en el arnés, el humo, la auditoría, el registro o una revisión posterior) antes de que un veredicto o una lectura ya declarada tuviera que corregirse. "si" = hubo que corregir un veredicto o una lectura declarada. "no_determinable" = el texto no permite decidirlo; no cuenta en X.

| universo | n | X (no alteró) | alteró | no determinable |
|---|---|---|---|---|
| **errores (sin reservas/cláusulas)** | 120 | **105** | 14 | 1 |
| todos los números con definición | 126 | 105 | 14 | 7 |

**X = 105 de 120 errores** (88 %; 105 de 119 con altero determinable). Sensibilidad a los casos con `dudoso_altero`: X entre 104 (si ERR-35 fueran "si") y 110 (si ERR-27, ERR-88, ERR-97, ERR-100, ERR-104 fueran "no"). Sin los ERR-1..4 reconstruidos: X = 101 de 116. Versión estricta (atrapados antes de correr la serie que habrían tocado): 49.

**Aviso para la tesis:** "153 errores registrados" no es exacto: hay 126 números con definición, de los cuales 120 son errores; 27 números no se usaron.

ERR que alteraron una conclusión: ERR-5, ERR-9, ERR-12, ERR-13, ERR-15, ERR-20, ERR-27, ERR-38, ERR-41, ERR-88, ERR-97, ERR-100, ERR-104, ERR-117.

ERR no determinables: ERR-50, ERR-62, ERR-80, ERR-81, ERR-82, ERR-83, ERR-118.

### Cruces (sólo errores, n = 120)
| tiempo_hasta_detectarlo / altero_conclusion | no | no_determinable | si |
|---|---|---|---|
| antes_de_la_serie | 49 | 0 | 0 |
| despues_de_la_serie | 45 | 1 | 7 |
| dias | 6 | 0 | 5 |
| misma_sesion | 5 | 0 | 2 |

| tipo / altero_conclusion | no | no_determinable | si |
|---|---|---|---|
| concurrencia | 1 | 0 | 0 |
| criterio | 47 | 1 | 5 |
| fabricacion_o_fuera_de_mandato | 4 | 0 | 0 |
| generalizacion_indebida_del_criterio | 9 | 0 | 0 |
| instrumento | 39 | 0 | 8 |
| otro | 5 | 0 | 1 |

| quien_lo_atrapo / altero_conclusion | no | no_determinable | si |
|---|---|---|---|
| agente_externo | 1 | 0 | 0 |
| arnes | 8 | 0 | 0 |
| auditor | 20 | 0 | 2 |
| coordinador | 9 | 0 | 6 |
| creador | 28 | 0 | 4 |
| cronista | 2 | 0 | 0 |
| director | 0 | 0 | 1 |
| humo | 8 | 0 | 0 |
| no_determinable | 29 | 1 | 1 |

## Casos dudosos (marcados en `clasificacion_errores.json`)
- ERR-1 (criterio, altero no): Sin número escrito: reconstruido del ordinal (REGISTRO:192 y :333).
- ERR-2 (criterio, altero no): Sin número escrito: reconstruido del ordinal (REGISTRO:192 y :333).
- ERR-3 (instrumento, altero no): Sin número escrito; además "ERR-3" se cita en otros archivos como "recalibrar tras ver datos" (confusión con la regla 3).
- ERR-4 (otro, altero no): Sin número escrito. El cuarto también podría ser el import equivocado de la batería v7 (REGISTRO:138, "Cuarta vez").
- ERR-5 (instrumento, altero si): Podría leerse como afirmación sin medición (fabricación); el registro lo atribuye al instrumento.
- ERR-7 (instrumento, altero no): Número duplicado: los artefactos del exp. 2b llaman "ERR-07" a lo que el registro numera ERR-09.
- ERR-11 (criterio, altero no): El registro lo agrupa con ERR-06/08/10 ("mismo patrón").
- ERR-18 (criterio, altero no): "Atrapado por la auditoría": el texto no dice qué agente auditó.
- ERR-23 (instrumento, altero no): Mezcla montaje (instrumento) y medida sin balancear (criterio).
- ERR-25 (otro, altero no): Es defecto del organismo, no del método; podría excluirse del recuento.
- ERR-26 (criterio, altero no): También admite fuera de mandato (se cambió el criterio sin el procedimiento).
- ERR-27 (criterio, altero si): "si": la serie 41–60 quedó como retroactiva y se rebajó el vocabulario del candidato.
- ERR-35 (criterio, altero no): "no": se reformuló antes de declarar fracaso la línea XOR; pudo haber lecturas previas.
- ERR-43 (instrumento, altero no): La sala 2 (DIAG_metodo §2.3) también lo encontró; el registro lo firma el coordinador.
- ERR-47 (otro, altero no): Podría ser criterio (banda E1) o instrumento (mundo).
- ERR-50 (otro, altero no_determinable): Mismo suceso que ERR-51.
- ERR-51 (instrumento, altero no): El humo lo señaló (1 de 2) pero se corrigió después de la serie.
- ERR-85 (fabricacion_o_fuera_de_mandato, altero no): También admite concurrencia.
- ERR-88 (instrumento, altero si): "si": la lectura "inerte y retirado" pasó a "no medida" (ningún veredicto cambió).
- ERR-97 (otro, altero si): Justificación, no veredicto: "si" por lectura causal corregida.
- ERR-100 (criterio, altero si): El cruce se mantiene; "si" por la magnitud declarada (1.565) corregida.
- ERR-104 (instrumento, altero si): "si": reserva sobre un cruce ya declarado.
- ERR-115 (fabricacion_o_fuera_de_mandato, altero no): Causa raíz mixta: agente fuera de mandato y runner sin validar banderas.
- ERR-118 (criterio, altero no_determinable): No consta si la lectura "O1 persiste 14/20" se había declarado antes.
- ERR-122 (criterio, altero no): Corrección decidida por el director; el texto no dice quién halló el fallo.
- ERR-131 (fabricacion_o_fuera_de_mandato, altero no): Sobre-afirmación; podría ser "otro".
- ERR-142 (fabricacion_o_fuera_de_mandato, altero no): La cláusula sólo puede rebajar el veredicto; también admite criterio.
- ERR-146 (instrumento, altero no): Es un cambio preventivo; la guardia ya había detenido ECO v1.2 en la nube.
- ERR-151 (instrumento, altero no): En la rama nube se llama ERR-150; mismo defecto de fondo que ERR-152.

## Muestra para el director
`informe/muestra_20.csv`: random.Random(20260929).sample(existentes, 20) sobre los 126 números con definición, en ese orden: 49, 85, 113, 38, 104, 70, 19, 61, 31, 95, 47, 80, 123, 9, 83, 2, 40, 93, 94, 60.

