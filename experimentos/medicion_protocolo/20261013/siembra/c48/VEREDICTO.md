# VEREDICTO — entrada del registro

Copiada de `registro/REGISTRO_etapas_1_2.md`, líneas 6217–6239.

---

### CRITERIO DE TRONCO v4 — calibración y réplica (ERR-94) (22-sep-2026, 13:25–14:30; semillas 2841–2920, réplica 2361–2440, Pool 5): **v4 CUMPLE sus cinco condiciones de validación (V4-1..V4-5) en la serie Y en la réplica — UTILIZABLE; v3 queda RETIRADO (sobre el mismo nulo da 0.709 / 0.732, confirma ERR-94); P-1..P-7 acertadas ×2**

Preregistro `experimentos/criterio_v4/PREREGISTRO_calibracion_v4.md` (sha `2646dd7a8c42891b`). Letra en `registro/CRITERIO_TRONCO_v4.md` (sha `c529c48f63734426`). Instrumento: `corre_criterio_v4.py` (`c70d1c643e78ee88`), `umbrales_v4.py` (`4210e4384c2aecd5`), `identidad_v4.py` (`ab3bf0453c23a8c8`, arnés **16/16**), `regla14_v4.py` (`d31958b997a763aa`); reusa por import `organismo_v3cal.py` (`148014f68cb01785`, arnés v3 **54/54**). Crudos: serie `datos/critv4_20260922_132544.json` (sha `302a713f31719872`); réplica `datos/critv4_rep_20260922_135746.json` (sha `f986ef2787d334a8`). 960 corridas por serie (640 T-A + 320 T-C ii). Commits `038ff0d` (preregistro/letra), `cc52105` (calibración+réplica), `319a93b` (integración a main, v3 retirado).

| condición | serie 2841–2920 | réplica 2361–2440 |
|---|---|---|
| V4-1 (reparto del nulo, las dos puertas juntas ≥ 0.95) | **0.9952** | **0.9962** |
| V4-2 (TRONCO_B pasa T-A, T-C ii, T-F en la realización) | PASA | PASA |
| V4-3 (PLACEBO pasa las tres) | PASA | PASA |
| V4-4 (PEOR cae) | CAE (correcto) | CAE (correcto) |
| V4-5 (δ=−20 pasa ≤ 0.05; δ=−margen ≤ 0.15) | TA 0.0 / TC 0.0; margen TA 0.0027 / TC 0.058 | TA 0.0 / TC 0.0; margen TA 0.0027 / TC 0.0558 |
| v3 sobre el mismo nulo (juntas) | 0.7088 | 0.7321 |
| v2 (T-A, n=20) sobre el mismo nulo | 0.323 | 0.3147 |

**Nota declarada:** T-C (ii) sola no atrapa a PEOR en la serie (v4 marca PASA con rev PEOR 47.0/43.0, LI −3.478 > −12.5); es T-A quien lo atrapa (LI −83.457 y −118.218). En la réplica, T-C (ii) sí atrapa a PEOR (LI −14.518 < −12.5): las dos puertas juntas son necesarias, ninguna sola basta siempre.

**Predicciones firmadas (P-1..P-7), acertadas en las dos series:** P-1 reparto conjunto 0.9952/0.9962 (banda 0.965–1.0); P-2 T-C sola 0.996/0.998 (0.97–1.0); P-3 T-A sola 0.9992/0.9982 (0.985–1.0); P-4 v2 sigue rechazando 0.323/0.3147 (0.20–0.45); P-5 v3 0.7088/0.7321 (0.55–0.80); P-6 marginales TRONCO_B 6/6 y PLACEBO 6/6 dentro de Bonferroni las dos veces; P-7 PEOR Δr mediano −74.5…−115.5 (≤ −60).

**Lectura honesta.** v4 no es un candidato al tronco: es el instrumento con el que se van a juzgar los candidatos de aquí en adelante. Pasa exactamente lo que tenía que pasar (el propio tronco contra sí mismo, y un candidato inerte) y rechaza exactamente lo que tenía que rechazar (un coste de vida ×1.5 conocido malo, y un desplazamiento exacto de −20), en dos series independientes. v3 se retira porque, con el mismo nulo, su probabilidad de dejar pasar al tronco (0.71–0.73) es demasiado baja para ser el criterio de aceptación de un candidato honesto.

**Vocabulario permitido:** *"el criterio v4, calibrado con n=80 y margen 12.5 en T-C (ii), deja pasar al propio tronco y a un candidato inerte con probabilidad mayor a 0.99 sobre el nulo, y rechaza con probabilidad 1.0 a un candidato desplazado −20 y a un coste de vida conocido malo, replicado en dos series independientes; v3, sobre el mismo nulo, sólo llega a 0.71–0.73: se retira"*. Prohibido: "v4 declara un candidato"; usar v4 para rejuzgar algo evaluado con v2/v3 sin decirlo.

**Qué queda.** De aquí en adelante, cualquier candidato a tronco se juzga con v4. No toca ningún nivel del brief directamente (es infraestructura de juicio).
