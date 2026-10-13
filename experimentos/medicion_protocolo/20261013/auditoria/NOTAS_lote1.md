# NOTAS lote1 (auditor ciego)

Metodo por copia: (1) sha de cada archivo contra los sha que el propio log y el veredicto declaran; (2) preregistro contra runner (umbrales, kwargs, controles); (3) recalculo desde el JSON con python estandar (sin numpy: no estaba instalado) de las cifras de la tabla y de las frases con numeros del VEREDICTO; (4) fechas y horas del preregistro contra las marcas de los logs. No abri nada fuera de lote1 ni busqué CLAVE.

## Tiempo aproximado por copia
- c01 ~10 min. c07 ~12. c10 ~10. c11 ~12. c14 ~15 (recalculo de N_agot y de N*). c15 ~10. c16 ~8. c30 ~15. c54 ~8. c57 ~25 (el mas largo: 8 JSON, tres letras, recalculo de LI).
- Total ~2 h.

## Resultado en una linea
Con defecto: c07 (confianza media), c10 (alta), c14 (alta, dos hallazgos), c30 (media/alta, dos hallazgos), c57 (alta, mas dos de menor peso). Limpias: c01, c11, c15, c16, c54.
Si se cuentan solo hallazgos con confianza alta o media-alta: c10, c14, c30, c57 = 4 copias; c07 es media y la tercera fila de c57 es baja.

## Que fue dificil
- Los sha no discriminan solos: en c10, c57 y c30 el preregistro actual no coincide con el sha que registra el log, pero en el proyecto original los preregistros se anotaron despues (enmiendas, asignacion de replica, resultados). Hay que leer el contenido para saber si el cambio es legitimo.
- En c14 el sha del script coincide con el del log y aun asi las cifras del log no salen del codigo entregado (N_agot). Es decir, "sha coincide" no prueba que el log venga de ese codigo; solo recalculando se ve.
- c57: tres letras superpuestas (v2, v3, v4), 8 JSON; el pareo de semillas y la funcion no_inferior viven en un archivo que no esta en la carpeta.

## Lo que NO pude verificar sin correr la serie o sin archivos que no estan
- Identidades bit a bit (v9m vs v9, v10 vs v9, v12 vs v11, v8p vs v8, caph9 vs caph, mundo_largo_c vs mundo_largo, etc.): los origenes (organismo_v8/v9/v10/v11, mundo_temporal_v8, mundo_temporal_k, mundo_largo, parte2_capacidad, corre_criterio_v3 con no_inferior) no estan en la carpeta; solo comprobe que el codigo generado coincide con las anclas de su construye_*.py en lo que pude leer.
- c11: Q1/Q2 (examen_v10, bateria_v10) y Q5 (bateria_v9, manifiesto) no estan; c15: la tabla "sin plasticidad" (+0.837, 10/20) viene de un script de scratchpad que no esta; c07: "28 divisiones de v9", humo de enmienda 2 (t_cong 52.218 y 74.131), el examen rapido bateria_v12; c16: control 1 (42/42) y bateria_v7b; c30: "466 corridas" (el JSON trae 400 + 20 de P4 + 3 de identidad; no me cuadra con 466 ni con las 420+6 del preregistro); c14: el diagnostico post-hoc de |W-R| (0.02 / 0.02 / 0.11 / 0.16): con mi calculo a 60k sale 0.021 / 0.021 / 0.157 (+10) / 0.252 (+20), asi que "0.11 a diez estimulos" no lo reproduje (podria ser otra definicion de distancia); no lo marque por ser explicitamente exploratorio.
- Commits y sha de commit citados en los veredictos.
- c07: la humo de enmienda 2 se hizo en las semillas 41-42, que luego forman parte de la serie 41-60; esta declarado, lo anoto como reserva menor (punto 5).
- c16: la adenda P5 (capacidad, "NO decide") esta preregistrada pero ni el runner ni el veredicto la reportan; lo trate como no defecto porque el propio texto dice que P5 se prueba en el diseno de 2K-bis, pero es una laguna de completitud (punto 8).
- c54: el control "barajado" permuta el progreso entre las 90 celdas, no entre las 3 celdas de cada patron como dice el preregistro (permutar dentro de las 3 daria la misma media); es una desviacion de redaccion sin efecto, no la marque.
- c57: la frase de la letra sobre sd(log D) 0.034 a n=80 no me cuadra con 0.043/sqrt(2)=0.030; es texto de borrador de T-H (no eliminatoria), no la marque.

## Sospechas sin ubicacion firme (cuentan aparte)
- Ninguna adicional. La fila baja de c57 (PREREGISTRO:45) tiene ubicacion pero es la de menor confianza: puede ser una anotacion posterior legitima.
