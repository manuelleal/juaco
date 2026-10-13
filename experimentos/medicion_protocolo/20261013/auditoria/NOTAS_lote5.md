# NOTAS lote5 (auditor ciego)

## Tiempo aproximado por copia (lectura + recontar contra log/JSON)
c02 ~6 min; c12 ~8; c13 ~12 (la mas larga: runner de 526 lineas, dos series); c24 ~8; c33 ~7; c34 ~4; c47 ~5; c51 ~7; c52 ~4; c58 ~6. Total ~65 min.

## Marcadas con defecto: c02, c13 (2 filas, una de ellas baja), c24, c33, c34, c47, c52. Limpias: c12, c51, c58.

## Que fue dificil
- Los sha de script/instrumento en logs y JSON COINCIDEN con los archivos entregados incluso en copias donde el codigo contradice al log (c33, c34, c52). No sirven para detectar alteraciones; hay que comparar codigo contra preregistro y contra lo que el log imprime.
- Distinguir defecto sembrado de errata original del autor (c13 P-7 "-74.5", c24 "466 corridas" en lugar de 446 o 426, c58 "a 3 decimales" con W redondeado a 2): los dejo sin marcar o con confianza baja.
- c24: la hora de la enmienda (00:50) es el unico indicio; las cifras cuadran con los logs.

## Que no pude verificar sin correr la serie
- c33: que el codigo entregado (memoria_rechazo=0 por defecto) produzca el log; deduzco por contraste con las cifras de v8 del preregistro. Tampoco la logica de memoria de rechazo mas alla de comparar lineas con organismo_caph9.
- c52: igual, no corri el runner; deduzco por el contraste 20k vs 60k.
- c02: la cifra "corr +0.78" del preregistro (Etapa 4 previa) no esta en esta carpeta; no la pude contrastar.
- c12: diagnostico "sin plasticidad" (10/20, +0.837) viene de un script de scratchpad que no esta en la carpeta; solo verifique corr 0.87, semillas sin divisiones y +2.569 desde el JSON.
- c58: Control 1 (lam=0 bit-identico a v7, 42/42) no lo ejecuta este runner ni hay log; sin evidencia en la carpeta. P5 (capacidad) del preregistro no se corrio ni se reporta (el preregistro dice que no decide).
- c24/c51/c13: identidades bit a bit, arneses (identidad_*.py, regla14) y cuerpos de organismos no recorridos linea a linea; me apoye en los logs de identidad (3/3, 21/21, 16/16).
- c51: humo de la Enmienda 2 uso semillas 41-42 que luego entran en la superficie (declarado, lo dejo como nota, no como hallazgo).
- Ningun CLAVE.csv visto ni abierto.
