# Revisión de SOLO LECTURA de la rama organelos (4f07e7f0) — 1-oct-2026

Auditor read-only, encargado por la sesión "Juaco revisión" a pedido de "JUACO organelos serie y auditoría".
Sin Pool, sin editar, sin commits. Rutas relativas a `PROYECTOS\JUACO\organelos`.

**VEREDICTO GENERAL: CON HALLAZGOS.** Los cuatro FUNCIONA ×2 de la Escalera (P1, P7, P10) y el NO SUMAN ×2 de "juntos" se
sostienen contra el repo. Los hallazgos son de numeración, texto desactualizado y matices que obliga AUDITORIA_F0. Ninguno
cambia un veredicto registrado.

## 1. Numeración de ERR (154–189)
**Definidos, con texto:**
- 154 y 155: REGISTRO:7206 y :7209.
- 156: REGISTRO:7337 y baldwin_exp/PREREGISTRO_baldwin_exp.md:201.
- 157: o1_evo/grande/PREREGISTRO_grande.md:79 y REGISTRO:7430.
- 158: condiciones/entre_linajes/PREREGISTRO_entre_linajes.md:141 y REGISTRO:7433.
- 159: condiciones/mutacion/PREREGISTRO_mutacion.md:7 y :100, y REGISTRO:7436.
- 160: SOLO en la rama o1-libre (o1_libre/PREREGISTRO_o1_libre.md:253).
- 170 y 171: REGISTRO:7378 y :7380, y escalera/PREREGISTRO_p1.md:155 y :162.
- 172–174: REGISTRO:7396–7397 y PREREGISTRO_p7.md:169–174.
- 175: REGISTRO:7398 y PREREGISTRO_p7.md:182.
- 176: condiciones/moneda_muro/PREREGISTRO_moneda_muro.md:167 y REGISTRO:7440.

**No definidos en ningún archivo ni rama:**
- 161–169: reservados a JUACO 5.
- 177–179: sólo aparecen como "libres".
  - moneda_muro_rep/PREREGISTRO…:7 dice "177–179, ninguno usado aquí".
  - escalera/sondas/PREREGISTRO_sondas.md:5 dice "ERR libre: 179 (no se usa)".
  - escalera/perillas/ no tiene PREREGISTRO.
- 180–189: cero definiciones.

**Hallazgos:**
- **H-1.** No hay ningún número con dos definiciones distintas. Hay una **doble reserva de 179** (perillas 178–179 y sondas 179).
  Hoy no choca, porque sondas no lo usa, pero la reserva es ambigua.
- **H-2.** ESTADO.md:67, HANDOFF.md:1171 y REGISTRO:7449 dicen "siguiente libre ERR-177". No reflejan que 177–179 ya están
  reservados. ESTADO.md:50 dice "JUACO 5: ERR-161" sin decir que 160 sólo existe en o1-libre.
- **Primer número libre:**
  - para esta sesión, **177**: nadie lo ha consumido;
  - sin dueño por reserva, **190**.
  - Recomendación: perillas se queda con 178, sondas con ninguno, y 179 sin reservar.

## 2. Escalera: coherencia contra commits
| Peldaño | (a) preregistro antes | (b) serie y réplica en disco | (c) veredicto por código | (d) vocabulario |
|---|---|---|---|---|
| P1 | OK | OK | OK | OK |
| P7 | OK, con H-3 | OK | OK | OK |
| P10 | OK | OK | OK | OK |
| juntos | OK | OK | OK | OK |

**(a) Preregistro antes de la serie:**
- P1: preregistro 76dc3d11 19:18:31; carpeta de la serie 19:18:42.
- P7: preregistro 61c61ef8 21:07:35; serie 21:07:49.
- P10: preregistro be35c3d2 21:55:56; serie 21:56:06.
- juntos: preregistro 1b5e483f 00:49:44; serie 00:49:48.
- Los preregistros no se modificaron después. Los runners y los carros no cambian entre el preregistro y la réplica.

**(b) Serie y réplica en disco:** las 8 carpetas tienen resumen.json, log.txt y los prueba_*.json, con 20 semillas por brazo y
0 abortos.

**(c) Veredicto por código:** `veredicto` y `letra` salen del runner. Las sumas de `cruzan` por brazo se recalcularon desde los
prueba_*.json y coinciden:
- P1: 79/0/7 y 85/0/7.
- P7: 132/80/49 y 124/81/50.
- P10: 164/82/53 y 163/91/65.
- juntos: todo 159 y 169, preg 163 y 163, sen 129 y 129, lug 88 y 95, todobar 90 y 95.
- preg y sen son idénticos en suma entre serie y réplica, pero con vectores distintos por semilla: es coincidencia.

**(d) Vocabulario:** ESTADO.md:17, HANDOFF.md:1168 y REGISTRO:7364 respetan "diseño, no selección; mundo con oasis".

**Hallazgos:**
- **H-3 (P7, texto).** PREREGISTRO_p7.md:11 dice "Escrito ANTES de… del humo 3. Siguiente ERR libre: ERR-172 (este bloque no abre
  ninguno)". Eso contradice H-9 (:182, "TRAS el humo 3"), y el propio archivo abrió 172–175. El orden "preregistro antes de la
  SERIE" sí se cumple; sólo el encabezado está desactualizado.
- **H-4.** ESTADO.md:3–5 dice "Última reescritura 1-oct ~00:30", pero ya incluye el cierre de "juntos" (≈06:56). HANDOFF.md termina
  en el cierre del 30-sep y no registra "juntos". Ni ESTADO ni HANDOFF mencionan moneda_muro_rep (4f07e7f0), ni perillas/ ni
  sondas/ (untracked).
- **H-5 (menor).** ESTADO.md:12–13: los ítems 1 y 2 no repiten "en el mundo con oasis". Lo cubre la línea 17.
- **H-6 (observación).** PREREGISTRO_juntos dice que SUMAN es "casi inalcanzable por techo", y el runner marca
  `SUMAN_alcanzable: True` en ambas series. El texto y el campo no usan la misma palabra.

## 3. Frases a matizar tras AUDITORIA_F0
El reloj de selección entre linajes NO está medido; n≈12 es un reloj mutacional. "≈150 generaciones" sólo aparece en la rama
o1-libre (o1_libre/PREREGISTRO_o1_libre.md:241), no en organelos.

1. **REGISTRO:7357**
   - Actual: "La selección afina perillas continuas (termostato ×2) pero no inventa combinaciones. / La selección por pasajes
     tampoco encuentra la regla hecha a mano."
   - Propuesto: "Con los montajes corridos (o1_libre ≈ 12 eventos mutacionales por línea; o1_evo y entre_linajes de orden 20–30,
     una serie, genes limitados), la selección afinó perillas continuas (termostato ×2) y no encontró combinaciones. No se midió
     el reloj de selección, de modo que no se concluye que no pueda."
2. **HANDOFF.md:1163**
   - Actual: "la seleccion afina perillas continuas pero no inventa combinaciones".
   - Propuesto: la misma redacción que en el punto 1.
3. **ESTADO.md:20**
   - Actual: "La selección conserva a O1, no lo mejora…".
   - Propuesto: añadir ", con reloj mutacional corto (o1_libre ≈ 12 eventos; o1_evo y entre_linajes orden 20–30, una serie). El
     reloj de selección entre linajes no está medido (F0)".
4. **HANDOFF.md:1169 y REGISTRO:7427–7428** ("la selección NO supera al diseñador…")
   - Propuesto: añadir "(o1_evo: una serie, sin réplica, siembra de vivos, no comparable con o1_libre; n orden 20–30)".
5. **ESTADO.md:23**
   - Actual: "Ne ≈ 9".
   - Propuesto: "Ne de linajes ≈ 9 (1/Σp², máximo 9; no es un Ne genético)".
6. **ESTADO.md:48–49 y REGISTRO:7453** ("la selección sostiene a O1 frente a la deriva y no lo supera")
   - Propuesto: añadir "en ≈ 12 eventos mutacionales por cadena; vale para ese reloj, no para evolución larga. 'Casi neutro' no se
     sostiene como explicación única: PISO se mueve 10/10 ×2; en la serie dos de cuatro definiciones de Ne·s quedan sobre 1".
7. **ESTADO.md:21–22 y REGISTRO:7442** ("la moneda de la selección era un candado del muro")
   - Propuesto: añadir "(exploratorio, 5 cadenas; el reloj de selección no está medido)".
8. **Texto retirado pero vivo** (insinúa que la selección eligió la capacidad de P1).
   - REGISTRO:7444–7447 conserva "HAY ALGO MODESTO… Réplica en curso" y "cuando puede elegir, la selección elige la memoria de
     lugar". La corrección está en :7451–7453.
   - HANDOFF.md:1170 dice "la selección prende sólo la memoria de lugar entre cuatro poderes (modesto; réplica en curso)", sin
     corrección.
   - Propuesto: marcar :7447 como "[RETIRADA 1-oct; ver Corrección]". En HANDOFF:1170 poner "O1 libre con poderes: BLOQUE NO; la
     subida de MEM por selección (10/10) no replicó (6/10, dif 0.047)".

## Verificado a mano
- Los tiempos de commit de preregistros y series.
- git diff de runners y carros entre el preregistro y la réplica.
- Las sumas `cruzan` por brazo desde los prueba_*.json de las 8 series, contra resumen.json y REGISTRO.
- Los veredictos, las puertas, 0 abortos y las semillas.
- Los pareados de P1, P7, P10 y juntos.
- La posición del oasis por semilla.
- El grep de ERR 154–189 en todo el árbol, las ramas y los worktrees.
- La lectura completa de AUDITORIA_F0 y F0_relojes.

## No se pudo verificar
- El contenido de 177–179: no existe definición.
- Los descriptivos secundarios de P10 ("nunca llegan 0/22/35 y 0/27/32").
- Si la réplica de moneda_muro_rep (carpeta untracked serie_20261001_072203) está completa.
- perillas y sondas: sin preregistro commiteado, no auditables.
- La hora exacta de escritura de H-9 en PREREGISTRO_p7 respecto del humo 3.
- La identidad campo a campo de los carros: no se reejecutaron los arneses, porque estaba prohibido correr simulaciones.
