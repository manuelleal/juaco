# PREDICCIONES — mini-LLM con colonia viva (escritas 5-oct-2026 ANTES de correr el experimento principal; después del humo de la base y de calibrar compuerta/λ en la semilla 0, declarado)

Exploración sin preregistro formal; 5 semillas (el flujo de maestros y la colonia cambian con la semilla; la base es una sola, compartida). Umbral de "cumplida": la mediana de las 5 semillas va en el sentido dicho.

1. (p=0.85) La base aprende algo real: pérdida de validación < bigrama (cuenta de pares de letras) y el texto generado tiene palabras del español reconocibles aunque sin sentido.
2. (p=0.7) La colonia (C=200) baja la pérdida EN LÍNEA respecto a la base congelada en los maestros con estructura repetida (hechos, idioma inventado) en ≥ 4/5 semillas; en código (dominio ancho) la mejora es pequeña o nula.
3. (p=0.75) En HECHOS la colonia responde el dígito correcto tras hechos1 en ≥ 0.6 de los 8 hechos (base ≈ 0.1), cambia tras hechos2 (≥ 0.5) y vuelve tras hechos3 (≥ 0.5). El kNN-LM con la misma memoria hace algo parecido en hechos1 pero peor en la VUELTA (lo visto hace 2 400 letras ya salió de su FIFO de 200).
4. (p=0.6) El gradiente en línea aprende cada maestro mejor que la colonia en pérdida en línea (es el techo caro: ~4× ops), pero ROMPE el español original (sonda español cae ≥ 0.05 de acierto) y los hechos vuelven más lento.
5. (p=0.8) La colonia NO rompe lo sabido: sonda español igual a la base (±0.01) en todas las semillas, porque la compuerta sólo pisa donde la base ya falla y el estado se parece.
6. (p=0.8) Controles: barajada peor que colonia en hechos (≥ 4/5); sin compuerta rompe el español (≥ 0.05) y es peor en todo.
7. (p=0.5) Sueño: tras los sueños la base propia responde algunos hechos sin células (liberadas > 0) y el español se mantiene (±0.02) gracias al pseudo-ensayo; con C=40 el sueño mejora a la colonia sola en hechos. Dudoso: 20 pasos de gradiente sobre episodios de última letra pueden no bastar.
8. (p=0.6) Con memoria chica (C=40) la colonia cae en hechos (≤ 0.4) y el kNN también; el ruido y el mentiroso llenan la memoria y matan células útiles.
9. (p=0.6) Maestro mentiroso: la colonia sin cuarentena acepta mentiras (acierto en hechos v1 tras 'mentiroso' cae ≥ 0.3 respecto a tras hechos1); el kNN igual o peor.
10. (p=0.65) CUARENTENA deja fuera la mentira: acierto en v1 tras 'mentiroso' cae < 0.15, y las células nacidas en mentiroso/ruido casi nunca llegan a pisar (< 10 % de las pisadas de la colonia sin cuarentena nacidas ahí). Precio: aprende más lento (en la curva por cuartos de hechos1 el primer cuarto queda por debajo de la colonia) y la verdad dicha UNA vez NO la aprende (unavez ≤ 0.2 frente a colonia ≥ 0.4).
11. (p=0.6) Contradicción (contra): la cuarentena se queda en hipótesis en la mayoría de los hechos (respuesta igual a la base ≥ 0.5) o conserva v1 (la validada); la colonia y el kNN alternan y acaban diciendo lo último (v2).
12. (p=0.5) Reversiones (validada que vuelve a hipótesis) > 0 y concentradas en hechos2/hechos3 (cuando el hecho cambia): es el registro de errores funcionando, no un fallo.
13. (p=0.5) Especialización (6.i): en 'mix' ≥ 70 % de las pisadas las hace una célula nacida en el mismo maestro.
14. (p=0.55) Demanda (6.iii): nacen más células por letra en hechos/inventado que en código, y el ruido produce muchos nacimientos que mueren sin cobrar.
15. (p=0.6) Cadena larga (6.ii, si cabe): con C=40 el sueño mantiene N < C y la pérdida de hechos de cada ciclo mejor que la colonia sin sueño en ≥ 2/3 semillas.

Criterio de veredicto: FUNCIONA si 2, 3, 5, 6 y 10 se cumplen; HAY ALGO MODESTO si 3 y 5 pero no 10 o viceversa; NO si la colonia no mejora a la base en hechos o rompe el español.
