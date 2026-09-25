# ERR-133..134: correcciones antes de la serie de Ohno (nube, 25-sep-2026, ~03:20)

Salen de la auditoría de sólo lectura (`juaco-auditor`), cuyo veredicto fue LISTO CON CORRECCIONES. Se escriben ANTES de correr cualquier semilla de 25011–25050.
No cambian la letra, los umbrales, el mundo ni el código. `PREREGISTRO_ohno.md` no se edita, porque el runner registra su sha.

## ERR-133 [fondo, sólo interpretación]: G1 compara dos series que oscilan alrededor del mismo punto fijo
**Qué pasa**
- En la calibración, toda población que persiste tras el corte queda en R0 ≈ 1, sea cual sea `r_rep`: el quimiostato fija la densidad.
  - 0.02: R0 entre 0.87 y 1.03.
  - 0.006: 0.99 / 1.09 / 1.11.
  - 0.005: 1.09 / 1.23 / 1.32.
- G1 (R0 pareado VIDA > FIJO, ≥ 15/20) compara entonces dos series alrededor del mismo punto fijo homeostático.

**Cómo se lee lo que salga**
- **Un NO en G1** no distingue "VIDA no tiene ventaja" de "la ventaja existe y el quimiostato la borra antes de llegar a R0".
- **Un SÍ** es más creíble, porque es más difícil de obtener por azar.
- La letra no cambia; se aplica tal cual.

**Descriptivo añadido, que no es letra**
- Junto al conteo pareado se reportan la mediana y el rango de R0 por brazo.
- También la persistencia y los nacimientos tras el corte.

## ERR-134 [protocolo]: la duplicación no se ejercita en el mundo exacto de la serie
- Las piezas D1–D3 del arnés corren con el quimiostato de ECO (0.03, mundo rico).
- Los casos del mundo pobre (O1, O1b) corren con la mutación de gramática apagada.
- Ninguna prueba ejercita la duplicación o la divergencia con `r_rep` = 0.006, el valor de la serie.
- **Riesgo residual:** un fallo de la duplicación que sólo aparezca con escasez extrema. Es una brecha de cobertura, no un error activo.
- **Mitigación sin construir nada:** en la lectura se reporta cuántas duplicaciones ocurren y sobreviven en VIDA.

(El umbral de O1b, bajado de ≥ 20 a ≥ 5 partos, ya está numerado como ERR-126 por el creador. Es un ajuste del arnés y no toca la letra: se acepta.)
