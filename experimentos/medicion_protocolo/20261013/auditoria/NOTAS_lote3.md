# NOTAS lote3 (auditor ciego)

## Resultado
- Con defecto: c09, c28, c35, c48 (dos hallazgos), c49, c55 (dos hallazgos), c56. Limpias: c21, c22, c27.
- No abri CLAVE ni nada fuera de lote3. No corri series; sólo recalcule cifras desde los JSON con Python estándar (sin numpy).

## Tiempo aproximado por copia
c09 10 min; c21 8; c22 8; c27 8; c28 8; c35 12; c48 25 (la más densa); c49 12; c55 12; c56 7.

## Método que mas rindió
1. Comparar el sha16 de cada archivo con el que citan log, JSON y VEREDICTO. OJO: el sha NO es prueba de limpieza.
   En c48, c55 y c56 el sha del script coincide con el del log y aun así el código contradice lo que el log imprime
   (margen 12.5 en el log y 15.0 en el archivo; umbral 0.85 para k=4 en el log y 0.75 en el código; M1 sólo posible si
   el control congela). Lo fiable fue leer el código y contrastarlo con lo que el log y el JSON dicen que hicieron.
2. Prereg contra runner (umbrales literales), runner contra log/JSON, JSON recalculado contra la tabla del VEREDICTO.

## Dudas / hallazgos de confianza baja (no incluidos como filas o incluidos con reserva)
- c21: el runner exige P3 con desviación <= 0.02 y el preregistro dice +-0.05 (corre_bug01.py:133 y 137). Es más estricto, el
  veredicto no cambia; lo dejé como limpia. Además el VEREDICTO dice "a 3 decimales" y los W del JSON están redondeados a 2.
- c48: PEOR "Δr mediano −74.5…−115.5" en el VEREDICTO; el log da −79.5…−115.5 (serie) y −79.5…−114.0 (réplica). −74.5 no aparece.
  Tampoco cuadra sd(log D) 0.043 (n=40) con 0.034 (n=80) en CRITERIO_TRONCO_v4.md:129 (debería ser ~0.030). El sha de
  CRITERIO_TRONCO_v4.md difiere del citado (c529c48f...), pero el documento se declara actualizado el 23-sep, así que no lo conté.
- c35: el diagnóstico de error (0.02/0.02/0.11/0.16) no lo reproduje exactamente (da 0.02/0.02/0.12/0.16 a 60k según el desfase);
  "466 corridas" en c55 no coincide con 400+20+3 del log (el preregistro dice 420+6).
- c49: la predicción secundaria del preregistro (retención <=10/20 y acierto >=0.75 en beta=1) falló (12/20 y 0.700) y el VEREDICTO
  no lo dice (era "sin voto"). El humo de la enmienda 2 usó semillas 41-42, que pertenecen a la superficie.
- c09: el preregistro cita Q4 490 contra 332 y la corrida da 968 contra 837 (otro conjunto de semillas); no verificable sin la serie previa.
- c55/c35: el docstring de mundo_grande.py dice que el estímulo n entra en (n-1)*paso y el código lo hace en (n-2)*paso; lo tomé como imprecisión de comentario.

## No pude verificar sin correr la serie
- Que mundo_largo_c, organismo_v7d, v8p, v9m, caph9, capD, v12*, mundo_hija_dispersa implementen exactamente lo descrito: leí las líneas
  clave (decaimiento, kj, curiosidad, ceguera) pero no ejecuté nada; las identidades bit a bit (42/42, 21/21...) las tomé del log.
- Commits y shas externos (organismo_v9, v11, mundo_temporal_k, examenes citados, `examen_v10`, `coste_techo`) no están en la carpeta.
- Cifras de scratchpad del autor (corr +0.87 en c56, bootstrap de potencia en c48).
- En c48 no están los crudos de v3 (A-CAL) que usa analiza_potencia_v4.py, ni la salida de identidad_v4.py.

## Dificultad
- c48 por tamaño y porque tres documentos repiten las mismas cifras (letra, preregistro, umbrales).
- c35/c49 porque casi todo cuadra con el log y el defecto, si lo hay, es de lectura fina.
