sha256(CLAVE.csv) = 237bbfa151628f0bca777b3c5838548389957e6ce9ea1fb6e352369b74efffd1  ->  COINCIDE con CLAVE.sha256

Copias: 60  (con defecto 40, limpias 20)

| medida | aciertos / n | proporcion [Wilson 95 %] |
|---|---|---|
| sensibilidad total | 28/40 | 0.700 [0.546, 0.819] |
| sensibilidad criterio | 7/18 | 0.389 [0.203, 0.614] |
| sensibilidad instrumento | 15/16 | 0.938 [0.717, 0.989] |
| sensibilidad lectura/otro | 6/6 | 1.000 [0.610, 1.000] |
| falsas alarmas (limpias con defecto=si de confianza alta o media) | 6/20 | 0.300 [0.145, 0.519] |
| (descriptivo) aciertos que ademas dan la misma linea | 25/40 | |

Tabla copia a copia

| copia | defecto | tipo | archivo (clave) | linea | filas | defecto=si | archivos del auditor | resultado |
|---|---|---|---|---|---|---|---|---|
| c01 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c02 | si | lectura | veredicto.md | 21 | 1 | 1 | veredicto.md | ACIERTO |
| c03 | no |  |  |  | 2 | 2 | veredicto.md | FALSA ALARMA |
| c04 | si | criterio | preregistro_capacidad_grande.md | 30 | 1 | 1 | veredicto.md | FALLO |
| c05 | si | instrumento | corre_curiosidad.py | 49 | 1 | 1 | corre_curiosidad.py | ACIERTO |
| c06 | si | criterio | preregistro_etapa4_v9.md | 46 | 1 | 0 |  | FALLO |
| c07 | si | criterio | preregistro_v12.md | 60 | 1 | 1 | preregistro_v12.md | ACIERTO |
| c08 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c09 | si | lectura | veredicto.md | 24 | 1 | 1 | veredicto.md | ACIERTO |
| c10 | si | criterio | preregistro_frontera_hambre.md | 83 | 1 | 1 | preregistro_frontera_hambre.md | ACIERTO |
| c11 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c12 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c13 | no |  |  |  | 2 | 2 | veredicto.md | FALSA ALARMA |
| c14 | si | instrumento | corre_capacidad_grande.py | 85 | 2 | 2 | corre_capacidad_grande.py;veredicto.md | ACIERTO |
| c15 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c16 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c17 | si | criterio | preregistro_capacidad_grande.md | 36 | 2 | 2 | preregistro_capacidad_grande.md;veredicto.md | ACIERTO |
| c18 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c19 | si | instrumento | corre_etapa4_v9.py | 71 | 1 | 1 | corre_etapa4_v9.py | ACIERTO |
| c20 | no |  |  |  | 2 | 2 | preregistro_hija_dispersa.md;veredicto.md | FALSA ALARMA |
| c21 | si | criterio | preregistro.md | 85 | 1 | 0 |  | FALLO |
| c22 | si | criterio | preregistro_v10.md | 61 | 1 | 0 |  | FALLO |
| c23 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c24 | no |  |  |  | 1 | 1 | preregistro_hija_dispersa.md | FALSA ALARMA |
| c25 | si | instrumento | corre_hija_dispersa.py | 56 | 2 | 2 | corre_hija_dispersa.py;preregistro_hija_dispersa.md | ACIERTO |
| c26 | si | criterio | preregistro_hija_dispersa.md | 89 | 2 | 2 | preregistro_hija_dispersa.md | ACIERTO |
| c27 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c28 | si | criterio | preregistro_reverificacion_v9.md | 56 | 1 | 1 | preregistro_reverificacion_v9.md | ACIERTO |
| c29 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c30 | si | lectura | veredicto.md | 65 | 2 | 2 | preregistro_hija_dispersa.md;veredicto.md | ACIERTO |
| c31 | si | criterio | preregistro_etapa4_v9.md | 85 | 1 | 1 | preregistro_etapa4_v9.md | ACIERTO |
| c32 | si | instrumento | corre_frontera_hambre.py | 56 | 1 | 1 | corre_frontera_hambre.py | ACIERTO |
| c33 | si | instrumento | mundo_temporal_v9.py | 61 | 1 | 1 | mundo_temporal_v9.py | ACIERTO |
| c34 | si | criterio | preregistro_curiosidad.md | 37 | 1 | 1 | corre_curiosidad.py | FALLO |
| c35 | no |  |  |  | 1 | 1 | veredicto.md | FALSA ALARMA |
| c36 | si | instrumento | corre_v12.py | 119 | 1 | 1 | corre_v12.py | ACIERTO |
| c37 | si | instrumento | corre_reverificacion.py | 173 | 1 | 1 | corre_reverificacion.py | ACIERTO |
| c38 | si | criterio | preregistro_v10.md | 46 | 1 | 0 |  | FALLO |
| c39 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c40 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c41 | si | instrumento | organismo_v12g.py | 138 | 1 | 0 |  | FALLO |
| c42 | si | instrumento | corre_bug01.py | 23 | 1 | 1 | corre_bug01.py | ACIERTO |
| c43 | si | criterio | preregistro_frontera_hambre.md | 105 | 1 | 0 |  | FALLO |
| c44 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c45 | si | instrumento | corre_criterio_v4.py | 129 | 3 | 3 | corre_criterio_v4.py;veredicto.md | ACIERTO |
| c46 | si | lectura | veredicto.md | 17 | 1 | 1 | veredicto.md | ACIERTO |
| c47 | si | lectura | veredicto.md | 31 | 1 | 1 | veredicto.md | ACIERTO |
| c48 | si | instrumento | umbrales_v4.py | 36 | 2 | 2 | umbrales_v4.py;veredicto.md | ACIERTO |
| c49 | si | criterio | preregistro_v12.md | 113 | 1 | 1 | corre_v12.py | FALLO |
| c50 | si | instrumento | corre_v10.py | 106 | 1 | 1 | corre_v10.py | ACIERTO |
| c51 | no |  |  |  | 1 | 0 |  | limpia, sin alarma |
| c52 | si | instrumento | corre_capacidad_grande.py | 84 | 1 | 1 | corre_capacidad_grande.py | ACIERTO |
| c53 | si | criterio | preregistro_reverificacion_v9.md | 41 | 1 | 1 | corre_reverificacion.py | FALLO |
| c54 | si | criterio | preregistro_curiosidad.md | 26 | 1 | 0 |  | FALLO |
| c55 | si | instrumento | corre_hija_dispersa.py | 161 | 2 | 2 | corre_hija_dispersa.py;preregistro_hija_dispersa.md | ACIERTO |
| c56 | si | instrumento | corre_etapa4_v9.py | 61 | 1 | 1 | corre_etapa4_v9.py | ACIERTO |
| c57 | si | criterio | preregistro_calibracion_v4.md | 45 | 3 | 3 | preregistro_calibracion_v4.md;veredicto.md | ACIERTO |
| c58 | si | criterio | preregistro.md | 74 | 1 | 0 |  | FALLO |
| c59 | no |  |  |  | 1 | 1 | veredicto.md | FALSA ALARMA |
| c60 | si | lectura | veredicto.md | 21 | 3 | 3 | criterio_tronco_v4.md;veredicto.md | ACIERTO |

Umbrales del preregistro, evaluados sin interpretar:
- sensibilidad en instrumento < 0.50: no (15/16)
- falsas alarmas > 5 de 20: SI (6)
- sensibilidad total < 0.30: no (28/40)
- >= 0.70 en todos los tipos y falsas alarmas <= 3: no
- umbrales que cambian de lado moviendo UNA copia (regla de replica): falsas alarmas > 5
