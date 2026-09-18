# N3b — sentidos complementarios, segundo intento tras ERR-23 (escrito ANTES de correr; semillas NUEVAS 21–40)

**17 sep 2026, noche del día 5.** N3 (`PREREGISTRO_N3.md`, `N3_s1-20_20260917_193532`) cayó y sus datos mostraron dos
fallos del **instrumento y de la medida**, no del organismo. Se registran como **ERR-23** y se corrige aquí sin
recalibrar sobre las mismas semillas: criterio nuevo, semillas nuevas.

## ERR-23 (dos partes)

1. **Canal simétrico con sesgo de decisión en los dos.** `gamma_soc` entró por `kw_org` a ambos organismos: el emisor
   (que ve la regla) también escuchaba la conducta del receptor ciego y se dejaba sesgar por ella. Emisor solo: 0.994;
   emisor en CONV: **0.681**. La señal que recibía el receptor venía ya contaminada. Además el emisor aprendía
   vicariamente (`f_vicaria`) de la conducta del ciego. Corrección: knob `escucha` por organismo; **sólo el receptor
   escucha** (`kw_por_org = [dict(gamma_soc=1.5), dict(escucha=False)]`).
2. **Acierto no balanceado.** `acierto = (comida mordida + veneno rechazado) / visitas` premia rechazarlo todo cuando el
   mundo se llena de veneno: en la pareja sin señal (N0) el emisor se come la comida en cuanto aparece, el receptor
   visita casi sólo veneno, lo rechaza (y se muere de hambre: 667 muertes) y "acierta" **0.978** sin saber nada.
   Corrección: **acierto balanceado** = ½ · (comida mordida / visitas a comida + veneno rechazado / visitas a veneno),
   en el último cuarto; rechazarlo todo o morderlo todo da 0.50.

Lo demás del montaje no cambia (regla `px0`, emisor ve 0–2, receptor ve 3–5, `gamma_soc = 1.5`, `tau_soc = 400`,
`d_senal = 5`, `f_vicaria = 1/3`, T = 200 000; identidad con `mundo_social`).

## Criterios (medianas, acierto balanceado del receptor en Q4) y predicción

- **S1:** CONV ≥ **0.80** y CONV > SOLO_R pareado ≥ 15/20. **S2:** CONV > SHUF ≥ 15/20. **S3:** CONV > SACIEDAD ≥ 15/20.
  **S4 (validez):** SOLO_R ≤ 0.75, TECHO ≥ 0.80, SOLO_E ≥ 0.80, y **emisor en CONV ≥ 0.90** (si el emisor se degrada,
  el montaje sigue roto). **S5:** N0 no supera a SOLO_R en ≥ 15/20.
- **Predicción:** S1–S5 pasan. Riesgo escrito: el mundo señala el veneno muchas veces y la comida pocas (desaparece al
  comerla; la misma asimetría que cerró N2), así que el receptor puede quedar **sesgado a rechazar** comida de la que
  no oyó nada; si S1 falla sólo por el umbral absoluto con los pareados en ≥ 15/20, se registra "transfiere, menos de
  lo predicho" y **no** se declara cerrado. **Refutación:** S1, S2 o S3 falla. Sin recalibrar después.
