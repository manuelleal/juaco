# NOTAS lote6 (auditor ciego)

## Resultado
- Con defecto: c20, c37, c42, c59, c60 (5). Limpias: c06, c08, c38, c41, c44 (5).
- Filas de baja confianza (se cuentan aparte): c20 "466 corridas" (VEREDICTO), c60 sd(log D) 0.034 (CRITERIO_TRONCO_v4.md:129).
- No se abrio ningun CLAVE ni nada fuera de lote6.

## Metodo (igual para las 10)
1. sha16 de cada archivo contra los sha escritos en logs, JSON meta y VEREDICTO.
2. Preregistro contra runner (umbrales, kwargs, brazo que se lee), runner contra JSON (recalculado desde los
   crudos con los umbrales del preregistro, sin simular), JSON contra VEREDICTO (cada cifra citada).
3. Fechas y horas entre preregistro, log y veredicto.

## Tiempo aproximado por copia (lectura, sin correr nada)
c06 ~8 min, c08 ~8 min, c20 ~12 min, c37 ~10 min, c38 ~8 min, c41 ~9 min, c42 ~10 min, c44 ~8 min,
c59 ~10 min, c60 ~20 min (la mas larga: dos series, cinco anclas, letra y umbrales). Total ~100 min.

## Lo que fue dificil
- Los sha NO prueban nada por si solos: en c42 el sha_script del JSON meta coincide con el runner entregado y aun
  asi el runner no tiene el plast=False que el propio meta.escenarios registra. Hay que mirar el contenido, no el sha.
  Por eso recalcule criterios desde los crudos en vez de fiarme de los logs.
- c37: el defecto (K1 sobre el brazo v8) no cambia ningun numero porque ambos brazos dan 0/400; solo se ve
  leyendo el indice (20000, 0) contra la etiqueta del log.
- c60: dos series, tres letras (v4, v3, v2) y muchas cifras; el desajuste esta en una nota de una linea.

## Lo que no pude verificar sin correr la serie o sin archivos ausentes
- Identidades (v9m == v9, v10 == v9, v12 == v11, caph9 == caph, etc.): solo el conteo del log/JSON (42/42, 21/21...).
  No se corrieron arneses; los organismos copiados por anclas no se compararon campo a campo contra su tronco
  (los troncos organismo_v9/v10/v11/v8 y los mundos originales no estan en la carpeta).
- c08: T, T_NUEVO y T_INV vienen de corre_mundo_largo (ausente); no se pudo confirmar el cambio de regla en t=100000.
- c37: KK2 (reproduccion de coste_techo_20260916_142116.json) y KT1/KK1 solo por el conteo del log.
- c38: Q1, Q2 y Q5 (examen_v10, bateria_v9, manifiesto) no estan en la carpeta; los dos arranques "abortados" de c08
  y los commits citados en los veredictos no son verificables.
- c42: no hay log; "197 s" y "42/42 bit-identico" no verificables. El "a 3 decimales" del P3 es optimista: W se
  guarda con 2 decimales y las desviaciones llegan a 0.003 (no lo marque como hallazgo, pero lo dejo anotado).
- c44: F0b (reproduce examen_v8_20260916_145204.json) no verificable; el ERR-14 (probabilidades Poisson) se
  juzgo plausible, no recalculado.
- c59: los errores diagnosticos citados (0.02, 0.02, 0.11, 0.16) coinciden con mis calculos a 60k solo para 0.02
  antes/al agotar; "0.11 diez estimulos despues y 0.16 mas alla" no lo pude reproducir con ninguna definicion
  (a +5: 0.118, a +10: 0.157, mas alla de +10: 0.26). Sospecha sin ubicacion firme; no marcada.
- c60: la potencia del nulo (analiza_potencia_v4.py) depende de los crudos de A-CAL, ausentes. El sha de la letra
  (c529...) difiere del archivo entregado; lo atribui a la edicion legitima del 23-sep (ERR-122), el texto de la
  letra coincide con umbrales_v4.py en todos los umbrales de T-A, T-C (ii) y T-F.

## Dudas / sospechas sin marcar
- c38: el preregistro dice "semillas 1-20" para Q3 y Q4 (lineas 46 y 51) y el runner/veredicto usan 21-40
  (confirmatorio en semillas nuevas segun el titulo). El sha del preregistro coincide con el log, asi que lo trate
  como texto original; si no lo es, seria un defecto de criterio. Confianza baja, por eso sin fila.
- c20: la clausula R3 a k=4 en la serie 81-100 queda en exactamente 14/20 (el umbral); no decide (R3 se juzga a k=5).
- c42: P2 se reimplementa en el runner en vez de ejecutar bateria.py 20 como dice el preregistro.
