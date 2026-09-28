# PREREGISTRO — examen v14.4c: el CRITERIO DE TRONCO v4 con T-C (ii) POR VISITA (ERR-150) sobre v14.4b = v14.3 + TERMO′

**Escrito ANTES del humo** (28-sep-2026, creador). Antes de esto se corrió:
- el análisis del nulo de ERR-150 (`analiza_nulo_err150.py`; sin ningún dato de TERMO′);
- la construcción por anclas;
- la búsqueda de semillas;
- el arnés (144/144).

**No se miró la serie del examen v14.4b.** Corría en el PC mientras se escribía esto.

Misión: llegar a la AGI por este camino. Decisión del director (HANDOFF, 28-sep ~16:30, "A").

## 1. Hipótesis
- **H-v144c:** v14.4b (TERMO′, el mismo organismo del examen v14.4b, sin tocar) **se desdice** en el mundo vivo cuando la reversión
  se mide por visita y contra sí mismo (ERR-150). Además, cruza el resto de la letra v4 sin cambios, en semillas nuevas, con serie y réplica.
- **H-ERR150 (la que este examen pone a prueba por primera vez en un termostato real):** la letra por visita no castiga comer menos.
  Si TERMO′ cae T-C (ii) por visita con C ≈ 0 y S4 bajo el suelo, o con C < −0.125 aunque su memoria de A sea negativa, la
  regla no hace lo que ERR-150 dice.

## 2. Qué cambia respecto del examen v14.4b: SÓLO la letra de T-C (ii)
- **Queda igual:**
  - el organismo (`organismo_v144b*`, las baterías y los carros), que se **reusa** desde `tronco_v14_4b_examen/` con sha fijado; no hay copias aquí;
  - T-A, T-B (ERR-122), T-C (i), T-D, T-E, T-F, T-G y T-H: importadas de `umbrales_examen_v144b` sin un número cambiado.
- **La letra nueva de T-C (ii)** (ERR-150, `ERR_150.md`):
  - `C = S4 − S2`, con `S = p_bueno / (p_bueno + p_malo)` y `p = (mordidas + 1) / (visitas + 2)`;
  - Q2 es antes de la reversión y Q4, después.
  - **Pasa si:** (a) no inferioridad de una cola al 95 % sobre `C_cand − C_tronco`, con margen 0.125 y n = 80, **y** (b) la mediana de S4 es > 0.5.
- **`rev` (la letra vieja) se calcula y se reporta, no decide.**

## 3. Instrumento (por anclas desde el examen v14.4b; `construye_examen_v144c.py`)
| archivo | sha16 | origen |
|---|---|---|
| `corre_examen_v144c.py` | `448b6133f2bc56a0` | `tronco_v14_4b_examen/corre_examen_v144b.py` (`9fb2e22a392590c7`) |
| `identidad_v144cex.py` | `7f2c5ec023a49b2f` | `tronco_v14_4b_examen/identidad_v144bex.py` (`23f5ed70d42399e0`) |
| `umbrales_examen_v144c.py` | (en el log) | **importa** `umbrales_examen_v144b` (`ddc96fa8038c3719`); sólo agrega ERR150, semillas y predicciones |
| organismo, baterías, carros | los de v14.4b | `c8f0c253…`, `19106bea…`, `b9c2cf7b…`, `01e00e0d…`, `3bbd29d3…` (anclas del runner) |

**Qué cambia en el runner:**
- `veredicto_vivo` llama igual a `corre_criterio_v4.juzga` y después sustituye su T-C (ii) por `letra_TC_visita`, guardando la vieja en `rev_absoluto_v4`;
- regla 14 R5: la letra nueva == ERR150 == el JSON del nulo; la vieja == la de v14.3;
- sintéticos con mordidas y visitas por cuarto;
- humo: imprime S2, S4 y C de la corrida del candidato.

**Arnés `identidad_v144cex.py`: RESULTADO 144/144** (170 s; `datos/humo/identidad_v144cex_20260928_162745.json`, `b00db4f809ba2736`; repetido tras fijar las predicciones, 144/144, `identidad_v144cex_20260928_163332.json`, `65d3692492240301`).
Es el de v14.4b, más:
- (0) la construcción de v14.4c y que el organismo se lee de v14.4b;
- (E) 10 casos de ERR-150:
  - la medida del runner == la del análisis, bit a bit, en 1 840 corridas;
  - el juez pasa a TRONCO_B, PLACEBO y PEOR con los mismos LI;
  - en el examen de v14.4 reproduce la letra vieja y **TERMO sigue cayendo** (C LI −0.482, S4 0.342);
  - caen el intercambio A/B y el indiferente (el indiferente, por el suelo);
  - "come menos" pasa la nueva y cae la vieja;
  - una letra mutada deja pasar a TERMO.

Primera corrida del arnés: 143/144. El caso "come menos" leía la clave `rev` sin recalcular tras adelgazar; se corrigió el caso,
sin tocar la letra ni el runner. Salida vieja: `identidad_v144cex_salida_v1_143de144.txt`.

## 4. La letra
- **T-A…T-F, T-H y T-G:** la del examen v14.4b (`PREREGISTRO_examen_v144b.md` sec. 4 y `PREREGISTRO_examen_v144.md` sec. 4), sin cambios.
- **T-C (ii):** ERR-150.
- **Nulo:**
  - P(pasa | nulo) 1.000 en las 5 series;
  - P(pasa | δ = −m) ≤ 0.055;
  - P(pasa | δ = −1.6 m) 0.000.
- **TRONCO_B no pasa la letra (con ERR-150) → la serie no se lee** (4′ de v4), igual que antes.

## 5. Predicciones (antes del humo)
**A la vista:**
- el exploratorio de TERMO′ del examen v14.4b (49001–49002, sin visitas: `rev` 22 y 2; muerde A en Q4 141 y 119);
- los crudos de TERMO (S2 0.820; pA2 0.386, pB2 0.083): antes de la reversión TERMO′ **es** TERMO.

| puerta | predicción | p |
|---|---|---|
| legible | TRONCO_B pasa (P nulo 1.000 en T-C ii) | 0.97 |
| T-A | como en v14.4b | 0.55 |
| T-B | como en v14.4b | 0.90 |
| **T-C** | (i) p 0.85. **(ii) por visita: C mediana en [−0.08, +0.03] (OFF ≈ 0.00), S4 mediana en [0.70, 0.90], LI > −0.125 con p 0.60.** Riesgo: pocas visitas a A en Q4 → pA4 sube → C cae | **0.50** |
| T-C (ii) vieja (informe) | `rev` mediana 0–30 (OFF ≈ 44): sigue cayendo | 0.2 pasa |
| T-D | como en v14.4b | 0.85 |
| T-E | como en v14.4b | 0.60 |
| T-F | como en v14.4b | 0.75 |
| T-G | como en v14.4b (G-1 p 0.25) | 0.25 |
| **serie** | **NO PASA (p ≈ 0.95)**, sobre todo por T-G y T-E; T-C (ii) por visita pasa con p 0.6 | 0.05 |

**Recomendación al coordinador (antes de ver v14.4b):**
- si la serie de v14.4b cae en T-A, T-B, T-D, T-E o T-G (puertas que no cambian), v14.4c caerá con alta probabilidad en la misma puerta;
- en ese caso, correrlo sólo sirve para medir ERR-150 en un termostato real (su sección 6);
- para eso basta `--solo TC,TA` (T-G sale de TA), unas 1 120 corridas en lugar de 1 476, con el veredicto INCOMPLETO declarado.

## 6. Qué refuta
- **Refuta ERR-150 (la regla, no el candidato):** TERMO′ tiene en Q4 la memoria de A negativa y la de B positiva (telemetría `adS`), muere igual o menos que el tronco (T-F), y aun así cae T-C (ii) por visita. En ese caso, la regla sigue midiendo algo que no es desdecirse. Se reporta con S2, S4 y visitas por cuarto.
- **Refuta la predicción del candidato:** C mediana < −0.125 con la memoria de A todavía positiva en Q4. Entonces TERMO′ no se desdice (como TERMO).
- T-G, T-E y el resto: como en v14.4b.

## 7. Riesgos declarados
- Los del examen v14.4b (sec. 7) siguen vigentes.
- ERR-150 se escribió con TERMO (el antagonista) a la vista. La condición anti-TERMO la pidió el director. Nada de TERMO′ entró en la elección de la medida ni del margen.
- La medida cambió de S4 (primer borrador) a C = S4 − S2 **antes** de construir el runner. El motivo: aplicada a Q2 (sin reversión), S4 le quitaba a TERMO −0.106 de 0.125. El borrador está en `datos/descartado_v1/`.
- Las semillas 53xxx están libres al 28-sep 16:10 (sec. 8). Otro creador trabajaba en paralelo; la regla 14 (R6) comprueba los cruces conocidos.

## 8. Semillas NUEVAS (`busca_semillas_v144c.py`: 44 455 archivos de todo PROYECTOS/JUACO)
En 53000–54600 y 153000–154600 sólo aparecen sellos de hora, fragmentos de sha, pasos de un análisis y una URL; ninguna como semilla.
Salida: `busca_semillas_v144c_salida.txt`.

| papel | serie | réplica |
|---|---|---|
| examen v3′ y T-B | 53101–53120 | 53121–53140 |
| mundo vivo T-A (+ CTRL) y T-C (ii) | 53201–53280 (TRONCO_B 153201–) | 53301–53380 (TRONCO_B 153301–) |
| T-D ALIAS | 53567 53569 53574 53580 53591 53597 53609 53675 53682 (de 53501–53999) | 153526 153562 153594 153611 153617 153649 153669 153673 153682 (de 153501–153999) |
| T-D LIMPIAS | 53503 53506 53510 53516 53522 53534 53536 53547 53558 | 153515 153522 153527 153532 153533 153536 153545 153556 153568 |
| reserva | 53401–53480 | |
| humo / identidad | 53951–53953 / 53955–53957 | |

## 9. Comandos (sólo el coordinador)
```
python experimentos/tronco_v14_4c_examen/corre_examen_v144c.py --serie --pool 6
python experimentos/tronco_v14_4c_examen/corre_examen_v144c.py --replica --pool 6 --con experimentos/tronco_v14_4c_examen/datos/examen_v144c_serie_<sello>.json
python experimentos/tronco_v14_4c_examen/corre_examen_v144c.py --bloque <serie.json> <replica.json>
```
Costo: 1 476 corridas por serie, ~30–50 min con Pool 6, igual que v14.4b.

## 10. Humo — escrito DESPUÉS
`python experimentos/tronco_v14_4c_examen/corre_examen_v144c.py --humo` (un proceso; 6 corridas, 200 000 pasos, 16 s):
**VEREDICTO DEL HUMO: OK**. JSON `datos/humo/examen_v144c_humo_20260928_162951.json` (`6e65ff60008a7345`); salida en
`humo_examen_salida.txt`. La etapa 0 dio:
- regla 14: 43/43;
- las anclas y las dos construcciones (`construye_termop --verifica` en v14.4b, `construye_examen_v144c --verifica`) se verificaron;
- sha: runner `448b6133f2bc56a0`, umbrales `13d38cdc72778a5f`, identidad `7f2c5ec023a49b2f`.

**Resultados del humo:**
- **La pieza actúa:** CAND ≠ OFF y ≠ CTRL.
- **Cableado:** el sintético bueno pasa las siete. El MALO (en Q4 muerde A 1100/1700) cae T-C (ii) por visita con C −0.317, LI −0.318; cae también T-A, T-B, T-D y T-G.
- **TRONCO_B y PLACEBO sintéticos pasan.**
- **Una corrida real de TERMO′ en T-C (ii)** (T = 20 000, cuartos de 5 000 pasos; **no es evidencia**):
  - memoria A −0.155, B +0.629 (se desdijo);
  - S2 0.747, S4 0.675, C −0.071;
  - visitas A [62, 99, 132, 208], B [218, 303, 236, 99].
- **Costo:** 1 476 corridas, ~33 min con Pool 6.
