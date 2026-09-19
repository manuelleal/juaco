# JUNTA FASE 5 — tres creadores Opus con exoesqueleto y nave (19-sep-2026, pedido del director)

Misión de fondo: llegar a la AGI por este camino. Misión de esta junta, concreta y medible: **cerrar la fase 5**.

## El problema (registro: REGISTRO_etapas_1_2.md, BLOQUE 6, línea ~5430)
Comunicación con referencia en el mundo de familias. Hoy, con la misma tabla, el mensaje refiere a la FAMILIA exacta (k = 3)
o a la VARIANTE (sufijo de 3 píxeles), no a las dos: con 4 casillas por par no caben. Falta **una tabla que codifique familia
Y variante (dos ganadoras de distinto tipo, forma + variante)**.
Instrumento base: `experimentos/nivel12_mundo_familias/organismo_familias_b6.py`, runner `corre_familias_b6.py`, identidad
`identidad_familias_b6.py`, preregistro y puertas `PREREGISTRO_bloque6_sufijo.md`.

## Criterio de éxito (el de la tabla del bloque 6, con un solo candidato; dos series de semillas nuevas 821–840 y 841–860)
CANAL ≥ 15/20 · CORTADO ≤ 5/20 · BAR-H (hermana) ≤ 5/20 · **BAR-T (otro token) ≤ 5/20** · PAR (distingue X de su hermana)
≥ 15/20 · VALOR ≤ 5/20 · puertas del bloque 6 (P-I2 incluida) · identidad con el tronco intacta. Hoy: k3 sin sufijo tiene
BAR-T 5/20 pero PAR 12/20; k3 con sufijo tiene PAR 15/20 pero BAR-T 11/20. **Hay que tener las dos a la vez.**

## Exoesqueleto de cada creador (memoria por consecuencia — lo que en alefast bajó los errores 3×)
1. **Antes de proponer**: leer `BITACORA_CONSECUENCIAS.md` y la lista de ERR del registro (ERR-35..ERR-84) y escribir qué
   fallos pasados podría repetir tu idea y cómo los evitas.
2. **Cada prueba que corras** se anota en la bitácora: idea → prueba → resultado → lección (una línea cada una). Lo que
   ya falló no se repite sin una razón nueva escrita.
3. **Calibración**: rápido cuando la prueba es barata y segura (humo ≤ 3 semillas); razonar cuando es nuevo; **preguntar**
   (sección "Preguntas al coordinador" de tu informe) cuando la decisión sea de método o de criterio. No adivines el criterio.

## La nave (lo que protege a todos)
- Sólo trabajas en `experimentos/junta_fase5/<tu letra>/` (copias). Nunca tocas `organismo/`, el tronco ni los archivos de otro.
- Tu instrumento debe pasar una identidad contra `organismo_familias_b6.py` en la configuración que no usa tu mecanismo
  (bit a bit, como `identidad_familias_b6.py`) antes de medir nada.
- Humo sólo con ≤ 3 semillas de 901–910 (nunca 821–860: son de la confirmación). El coordinador corre la serie confirmatoria.
- Sin git commit ni push. Los números que reportes deben poder reproducirse con un comando que escribas.
- Un auditor revisará tu propuesta contra la lista de ERR antes de la confirmación.

## Entregable de la ronda 1 (en `<tu letra>/PROPUESTA.md`)
Mecanismo (qué cambia en la tabla/lectura, en pocas líneas y en código), por qué debería dar familia Y variante, qué ERR
podría repetir, resultado del humo (tabla con los brazos del bloque 6), predicción numérica para 821–860, preguntas al
coordinador. Resumen final de 10 líneas.
