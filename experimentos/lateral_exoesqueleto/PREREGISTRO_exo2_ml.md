# PREREGISTRO EXO-2 — la capa JUACO decide QUÉ entra a entrenar (ML clásico, imágenes 8×8)
Escrito el 18-sep-2026 ~22:25, ANTES de correr. Línea lateral (§6 de la hipótesis). Pedido del director: "lo mismo con
machine learning, entrenamiento de imágenes, algo muy sencillo".

## Mundo
Dígitos de sklearn (1797 imágenes 8×8, 10 clases). Por semilla: 1200 de flujo, 597 de prueba. Flujo en lotes de 50.
Fase 1: 600 imágenes. Fase 2 (CAMBIO no avisado): las etiquetas 3 y 8 se intercambian en el flujo y en la prueba.
Modelo: regresión softmax en NumPy, SGD (lr 0.1), mismo para todos. Semillas 1–10 (serie) y 11–20 (réplica).

## Brazos
- **TODO**: entrena con cada imagen del flujo.
- **J (JUACO)**: sólo escribe lo que SORPRENDE (p de la etiqueta verdadera < 0.5) → entra al lote y a un buffer (200 máx.);
  cada lote repasa hasta 50 del buffer; **sobrescritura**: un ejemplo nuevo sorprendente borra del buffer a sus vecinos
  (coseno > 0.9) con etiqueta distinta; **olvido**: sale del buffer lo que el modelo ya predice con p > 0.95.
- **R (control de presupuesto)**: elige al azar EXACTAMENTE tantas imágenes por lote como J escribió, y con el mismo buffer
  y repaso (sin sobrescritura ni olvido por valor: FIFO). Es el "J barajado": mismo gasto, selección sin valor.
## Métricas
Acierto en prueba al final de la fase 1 y de la fase 2; acierto en 3/8 tras 100 y 200 imágenes del cambio (desdecirse);
fracción de imágenes usadas.
## Predicciones
- Q1 J usa ≤ 40 % de las imágenes y queda a ≤ 0.03 de TODO al final de la fase 1.
- Q2 J > R en ≥ 0.03 al final de la fase 1 (la selección por sorpresa paga, no sólo el presupuesto).
- Q3 en 3/8 tras 100 imágenes del cambio, J > R en ≥ 0.10 (sobrescritura).
## Refuta
J ≈ R (|Δ| < 0.03 en Q2 y < 0.10 en Q3) → la capa no aporta sobre el azar con igual gasto. Nota: seleccionar por
incertidumbre es aprendizaje activo conocido; el aporte posible es la combinación local (escribir/sobrescribir/olvidar).

## RESULTADO (22:20, series 1–10 y 11–20; `datos/exo2_s1-10_*`, `exo2_s11-20_*`)
| | fase 1 | 3/8 tras 100 | fase 2 final | usa |
|---|---|---|---|---|
| TODO | 0.856 / 0.866 | 0.12 / 0.14 | 0.873 / 0.875 | 100 % |
| J | 0.882 / 0.886 | 0.10 / 0.06 | 0.907 / 0.910 | 65 % |
| R | 0.867 / 0.872 | 0.05 / 0.05 | 0.828 / 0.834 | 65 % |
Q1 CAE (usa 65 %, no ≤ 40 %; eso sí, supera a TODO). Q2 CAE (+0.015). Q3 CAE (+0.04 / +0.01). **Refutada por la letra en las dos
series.** Exploratorio, NO preregistrado: al final de la fase 2, J supera a R por +0.08 en las dos series y a TODO por +0.03.
Candidato a un preregistro nuevo (métrica: acierto final tras el cambio). Instrumento: nadie se desdice en 3/8 a los 200
(< 0.25): el cambio es demasiado lento de revertir con este lr; revisar antes de rejuzgar Q3.

## EXO-2b — réplica corta de la señal exploratoria (preregistrada 22:40, ANTES de correr)
Mismo código sin tocar. Semillas NUEVAS 21–30 y 31–40. Predicción: acierto final de la fase 2, J − R ≥ 0.05 y J − TODO ≥ 0.02,
en las dos series. Refuta: J − R < 0.03 en cualquiera de las dos.
