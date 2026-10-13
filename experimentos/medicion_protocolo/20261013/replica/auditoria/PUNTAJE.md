sha256(CLAVE.csv) = 370fb5ad39561e19d937b3061a6988fa235beba452ff585401d5df2fa8bbcf11  ->  *** NO COINCIDE con CLAVE.sha256 (237bbfa151628f0bca777b3c5838548389957e6ce9ea1fb6e352369b74efffd1) ***

Copias: 20  (con defecto 13, limpias 7)

| medida | aciertos / n | proporcion [Wilson 95 %] |
|---|---|---|
| sensibilidad total | 7/13 | 0.538 [0.291, 0.768] |
| sensibilidad criterio | 2/6 | 0.333 [0.097, 0.700] |
| sensibilidad instrumento | 3/5 | 0.600 [0.231, 0.882] |
| sensibilidad lectura/otro | 2/2 | 1.000 [0.342, 1.000] |
| falsas alarmas (limpias con defecto=si de confianza alta o media) | 3/7 | 0.429 [0.158, 0.750] |
| (descriptivo) aciertos que ademas dan la misma linea | 4/13 | |

Tabla copia a copia

| copia | defecto | tipo | archivo (clave) | linea | filas | defecto=si | archivos del auditor | resultado |
|---|---|---|---|---|---|---|---|---|
| c01 | no |  |  |  | 1 | 1 | veredicto.md | FALSA ALARMA |
| c02 | si | instrumento | corre_frontera_hambre.py | 176 | 1 | 0 |  | FALLO |
| c03 | no |  |  |  | 3 | 3 | veredicto.md | FALSA ALARMA |
| c04 | si | criterio | preregistro_reverificacion_v9.md | 65 | 1 | 0 |  | FALLO |
| c05 | si | criterio | preregistro_v12.md | 119 | 1 | 0 |  | FALLO |
| c06 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c07 | si | lectura | veredicto.md | 35 | 1 | 1 | veredicto.md | ACIERTO |
| c08 | si | instrumento | corre_reverificacion.py | 83 | 1 | 0 |  | FALLO |
| c09 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c10 | si | criterio | preregistro_calibracion_v4.md | 57 | 2 | 2 | veredicto.md | FALLO |
| c11 | no |  |  |  | 1 | 1 | preregistro_hija_dispersa.md | FALSA ALARMA |
| c12 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c13 | si | criterio | preregistro_hija_dispersa.md | 57 | 3 | 3 | preregistro_hija_dispersa.md;veredicto.md | ACIERTO |
| c14 | si | lectura | veredicto.md | 40 | 2 | 2 | veredicto.md | ACIERTO |
| c15 | si | instrumento | corre_etapa4_v9.py | 73 | 1 | 1 | corre_etapa4_v9.py | ACIERTO |
| c16 | si | instrumento | organismo_v7d.py | 69 | 2 | 2 | organismo_v7d.py;veredicto.md | ACIERTO |
| c17 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c18 | si | criterio | preregistro_v10.md | 39 | 1 | 0 |  | FALLO |
| c19 | si | criterio | preregistro_curiosidad.md | 10 | 2 | 2 | preregistro_curiosidad.md | ACIERTO |
| c20 | si | instrumento | mundo_largo_c.py | 48 | 1 | 1 | mundo_largo_c.py | ACIERTO |

Umbrales del preregistro, evaluados sin interpretar:
- sensibilidad en instrumento < 0.50: no (3/5)
- falsas alarmas > 5 de 7: no (3)
- sensibilidad total < 0.30: no (7/13)
- >= 0.70 en todos los tipos y falsas alarmas <= 3: no
- umbrales que cambian de lado moviendo UNA copia (regla de replica): instrumento < 0.50, falsas alarmas <= 3, instrumento >= 0.70, lectura >= 0.70
