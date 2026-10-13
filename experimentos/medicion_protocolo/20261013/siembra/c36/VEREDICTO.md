# VEREDICTO — entrada del registro

Copiada de `registro/REGISTRO_etapas_1_2.md`, líneas 2554–2596.

---

### v12 — superficie del canje (seis β) y rama `hija-madura`: **H sostenida, rama REFUTADA**

Preregistro `experimentos/v12_ceguera_graduada/PREREGISTRO_v12.md` con **enmiendas 1 y 2 escritas antes de correr**
(`b89af5f`, `220aa55`). Datos `datos/v12_superficie_20260917_154123.json` (`c57af24accb680fe`). Instrumentos
`organismo_v12` `7f564687ec072da6`, `v12m` `c04a7f32b6eaa539`, `v12g` `b68d918f0db3ca8c`.

**Controles de inercia (pedidos por dirección), verificados ANTES de mirar los puntos intermedios:** `v12(β=0)` ≡ v11
**21/21**, `v12(div_signo=False)` ≡ v10 **21/21**, `v12m` ≡ `v11m` 9/9, `v12g` ≡ `v11g` 6/6. (Enmienda 1: β=1 **no
puede** ser v10 —el disparo por signo, la madre fija y la fisión no se gradúan— y por eso el control correcto es
apagar la regla entera.)

**Guarda del instrumento: Spearman(β, fuga) = +1.000.** La perilla manipula exactamente lo que dice manipular.

| condición | semillas | retención | aprende C y D | acierto en nunca vistos | azar | conducta | fuga | divisiones | muertes |
|---|---|---|---|---|---|---|---|---|---|
| β = 0.00 (= v11) | 41–60 | **20/20** | 20/20 | 0.600 [0.40, 0.90] | 0.500 | 0.672 | 0.08 | 5 | 202 |
| β = 0.15 | 41–60 | **20/20** | 20/20 | 0.575 | 0.500 | 0.657 | 0.13 | 5 | 202 |
| β = 0.30 | 41–60 | **20/20** | 20/20 | 0.600 | 0.500 | 0.689 | 0.18 | 5 | 198 |
| β = 0.50 | 41–60 | 19/20 | 20/20 | 0.600 | 0.500 | 0.664 | 0.22 | 6 | 196 |
| β = 0.75 | 41–60 | 19/20 | 20/20 | 0.700 | 0.500 | 0.716 | 0.37 | 6 | 202 |
| β = 1.00 | 41–60 | 12/20 | 20/20 | 0.700 | 0.500 | 0.692 | 0.57 | 7 | 202 |
| rama u = 1.0 | 71–80 | 5/10 | 10/10 | 0.700 | 0.500 | 0.740 | 0.65 | 7 | 210 |
| rama u = 0.3 | 71–80 | 5/10 | **5/10** | 0.750 | 0.500 | 0.718 | 0.67 | 7 | 222 |

*(referencias: v9 = retención 0/20 y acierto 0.800; v11 = 20/20 y 0.600; azar 0.50)*

- **H [el canje existe]: SOSTENIDA.** Ningún β alcanza a la vez retención 20/20 y acierto ≥ 0.78. La superficie es
  monótona en fuga y **el precio aparece antes que el premio**: la retención empieza a caer en β = 0.50 y se hunde en
  β = 1.00 (12/20), mientras el acierto sólo llega a 0.700.
- **Hallazgo lateral que corrige una simplificación mía:** ni con fuga máxima dentro de la regla de v11 se recupera el
  0.800 de v9. **La ceguera explica parte del costo, no todo**: la fisión del valor y la madre fija también cuestan
  generalización. La fuga a β = 1 es 0.57, no 1.00, porque la regla de signo produce **menos hijas** (7 divisiones
  frente a 28 de v9 en el mismo mundo).
- **Rama `hija-madura`: REFUTADA en los dos umbrales.** Retención 5/10 (se pedía ≥ 8) con acierto 0.700 y 0.750.
  **Las semillas retenidas 81–90 no se tocaron**, por el propio criterio de la rama.
  **Diagnóstico, y es limpio:** con `u = 0.3` la congelación llega tan pronto que **rompe el aprendizaje de lo nuevo**
  (guarda 5/10: ya no aprende C y D); con `u = 1.0` sólo congela hijas de veneno (enmienda 2) y no alcanza a proteger
  A. Congelar lo justo para no olvidar es congelar demasiado para aprender: **la maduración no rompe el canje, lo
  reproduce a otra escala.**

**Lectura:** en esta arquitectura, **recordar y generalizar son el mismo parámetro visto por los dos lados**, y la
superficie lo muestra punto a punto. Es el resultado que pedía dirección: un mapa, no una solución. v11 sigue siendo
el tronco; **v12 no se congela** (ningún punto mejora los dos ejes a la vez).
