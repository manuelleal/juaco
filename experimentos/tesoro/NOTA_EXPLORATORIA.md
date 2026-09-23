# Búsqueda del tesoro: bacterias en un plano, estaciones con pruebas de bits y una pizarra común

**EXPLORATORIO: no es dato.** No tiene preregistro, auditoría, arnés de identidad ni registro oficial. Es un mini-mundo nuevo en Python puro y no copia nada del tronco. Fecha: 22-sep-2026. Rama `escuela-exploratoria`, sin commit. Hubo 4 corridas de un solo proceso, cada una de menos de 1 segundo.

## Para el director, en 3 líneas
1. **¿Llegó alguna?** SÍ. Sin canal llega alguna en 18 de 20 semillas, pero pocas: la mediana es 2 de 12. Con canal llegan casi todas: la mediana es 12 de 12, y hubo llegadas en 20 de 20 semillas.
2. **¿El canal ayudó?** SÍ, y mucho. Con canal llegan más bacterias en 20 de 20 semillas, tanto contra el brazo sin canal como contra el canal ruidoso. La primera llega antes (paso 101 contra 131). Las que llegan tarde siguen la pizarra el 79 % de las veces que tienen un mensaje. Hay una salvedad: el canal ruidoso también ayuda un poco (4 de 12 contra 2 de 12). Parece que los mensajes al azar sirven como exploración extra. Aun así, el contenido correcto explica casi toda la ganancia.
3. **¿Qué las detuvo?** El hambre en las pruebas difíciles. Ninguna quedó viva sin llegar: todas las que no llegaron murieron sin energía. La prueba que más mata es el medio sumador (SUMA, 4 respuestas posibles), después XOR y XNOR. AND y OR matan poco.

## Montaje
- **Plano:** 20×20 con 5 estaciones en cadena. Los sitios cambian con cada semilla y las estaciones quedan separadas al menos 6 casillas.
- **Pruebas:** AND, XOR, OR, SUMA (medio sumador) y XNOR. El orden de las pruebas también cambia con la semilla.
- **Bacterias:** 12, con energía inicial de 30. Moverse cuesta 0,25 por paso y cada intento cuesta 0,3.
- **Recompensa por intento:** si acierta, recibe +0,15; si falla, pierde 0,4. Así, intentar siempre cuesta energía: no se puede vivir haciendo la prueba.
- **Resolver una estación:** hacen falta 4 aciertos seguidos con entradas al azar. Al resolverla, la bacteria recibe +6 de comida y el mundo le muestra la dirección hacia la siguiente estación. Al resolver la última, tiene comida infinita.
- **Aprendiz:** es asociativo, de tipo IND como en la escuela, y tiene detector de pares. Sus rasgos son el sesgo, a, b y el par (a,b), por separado para cada estación. Explora el 10 % de las veces.
- **Canal:** cuando una bacteria acierta, escribe en la pizarra "estación k, entrada (a,b) → respuesta r". Solo se guarda el primer mensaje de cada entrada.
- **Cómo se usa el canal:** la que lee suma un peso de "confianza" a la respuesta sugerida. Esa confianza se aprende por recompensa y es la misma para todas las estaciones, así que la bacteria puede ignorar la pizarra si no le sirve.
- **RUIDO (control):** cuando existe un mensaje, lo que se lee es una respuesta al azar.
- **Semillas:** 7101 a 7120 (20 por brazo). Los brazos se comparan pareados por semilla.

## Tabla por brazo (energía inicial 30; 20 semillas; EXPLORATORIO)

| brazo | semillas con ≥1 llegada | llegan (mediana, rango) de 12 | paso de la 1ª llegada (mediana) | estación mediana alcanzada (de 5) | intentos por bacteria (mediana) | tardías siguen la pizarra | confianza aprendida |
|---|---|---|---|---|---|---|---|
| SIN | 18/20 | 2 (0–5) | 131,5 | 2,5 | 71 | n/a | 0 |
| CANAL | 20/20 | 12 (11–12) | 101 | 5 | 46,5 | 0,79 | 0,997 |
| RUIDO | 20/20 | 4 (2–8) | 128 | 3,5 | 77 | 0,56 (azar) | 0,51 |

**Confiabilidad (comparación pareada por semilla, n=20):**
- CANAL tiene más llegadas que SIN en 20/20 semillas, con 0 empates.
- CANAL tiene más llegadas que RUIDO en 20/20 semillas, con 0 empates.
- RUIDO contra SIN: 4 contra 2 de mediana. No hice la prueba pareada.

**Muertes por prueba (suma de las 20 semillas):**

| brazo | SUMA | XOR | XNOR | OR | AND |
|---|---|---|---|---|---|
| SIN | 93 | 36 | 35 | 18 | 17 |
| CANAL | 2 | 1 | 1 | 1 | 0 |
| RUIDO | 74 | 28 | 34 | 5 | 9 |

**Sensibilidad (energía inicial 45):** SIN llega a una mediana de 5 de 12, RUIDO a 9 de 12 y CANAL a 12 de 12, sin ninguna muerta. El orden entre brazos no cambia.

## Qué no dice esto (honestidad)
- **Copiar no es aprender.** No medí si las que usaron la pizarra retienen la regla sin ella, porque no hubo examen sin pizarra. En la escuela, la sabia servía de muleta para el aprendiz LIN. Aquí puede pasar lo mismo.
- **El mundo ayuda mucho.** Da la dirección hacia la siguiente estación, así que moverse no se aprende. La ganancia está entera en las pruebas.
- **Las constantes las elegí yo** en el primer intento, sin ajustarlas. No probé otras combinaciones, salvo la energía inicial.
- **La RUIDO que salió mejor que SIN** no la había anticipado. Mi lectura es que los mensajes al azar funcionan como exploración extra, pero no está verificado.
- **No hice predicción escrita antes de correr**, así que no hay predicciones propias que declarar refutadas.

## Archivos
- `tesoro.py`: el mundo y los brazos (`--humo` corre 2 semillas).
- `resultados.json` y `resultados.txt`.
- `diagnostico.py`, `diagnostico.json` y `diagnostico.txt`: causas de muerte y sensibilidad a la energía inicial.
