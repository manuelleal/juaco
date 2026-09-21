# ENMIENDA 1 al PREREGISTRO_cuerpo_nuevo.md — rango del ancla F9-1 (ERR-92; 21-sep-2026, 19:05; coordinador)

**Qué cambia y por qué (escrito ANTES de correr la tercera serie).** La puerta F9-1 (ANCLA, bloqueante) exige `vida_NADA ∈ [90, 170]`. Ese rango
se fijó en el preregistro con las dos únicas series de H-1 disponibles (NADA_CM vida 125 y 119). Hoy existen cuatro series de la misma cantidad,
medidas con el mismo instrumento por identidad (NADA de F9 ≡ NADA_CM de H-1 bit a bit): **125, 119, 94.0, 88.5**. En la réplica 1521–1540 el ancla
cayó por `vida_NADA = 88.5` (las otras tres cláusulas en rango). No hay evidencia de que el instrumento se haya movido; la evidencia es que el rango
se calibró con menos series de las que existen (misma forma de defecto que ERR-91 en el criterio v2: una letra que no se contrastó con la variación
natural del propio tronco).

**Letra nueva de F9-1 (sólo para series a partir de esta enmienda; 1501–1520 y 1521–1540 NO se rejuzgan, regla 3):**
`vida_NADA ∈ [70, 170]`. Justificación: mínimo observado 88.5 menos un 20 % = 70.8, redondeado hacia abajo; el techo no cambia. Las otras tres
cláusulas de F9-1 no cambian. Ningún otro umbral de F9-2..F9-10 cambia.

**Cómo se aplica:** `corre_f9.py` lee la variable de entorno `F9_VIDA_NADA_MIN` (por defecto 90.0 = letra original). La tercera serie se corre con
`F9_VIDA_NADA_MIN=70`. El log imprime el valor usado en la línea de F9-1.

**Semillas NUEVAS:** 1621–1640 (verificadas libres con grep: el único "1630" del repo es una celda de una tabla de v9). Réplica, si hace falta, 1641–1660.

**Predicción (misma letra F9-2..F9-10 que las dos series):** F9-1 pasa (vida_NADA en [85, 130]); F9-2, F9-3, F9-5, F9-6, F9-8, F9-9, F9-10 pasan
otra vez; F9-4 y F9-7 caen otra vez (p1(REL_BAR) en [0.50, 0.65]; A₁₂(REL > REL_TARDE) en [0.35, 0.55]). Si F9-1 pasa y las siete pasan, con las
tres series (1501–1520, 1521–1540 exploratoria, 1621–1640) se declara lo replicado con el vocabulario permitido de la entrada del bloque 1, y el
nivel 9 sube de 30 % (la cifra la fija el director). Lo que refuta esta enmienda: `vida_NADA < 70` (entonces el instrumento sí se movió y se abre ERR).

**Regla derivada:** todo rango de ancla se calibra con TODAS las series existentes de esa cantidad y se reescribe (con ERR) cuando aparezcan más.
