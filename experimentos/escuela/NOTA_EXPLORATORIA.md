# Escuela de bacterias: sumar con bits por comida, con y sin sabia

**EXPLORATORIO: no cuenta como dato.** No tiene preregistro, auditoría ni registro oficial. No se hizo arnés de identidad porque es un mini-mundo nuevo y no copia nada del tronco. Fecha: 22-sep-2026, rama `escuela-exploratoria`, sin commit.

## Para el director, en 3 líneas
1. **¿Aprenden a sumar?** SÍ, pero con una condición: la alumna necesita un detector de pares (a,b). Con él aprende el medio sumador en unos 70 a 150 ensayos, y en el examen final sin ayuda saca 100 % (30 de 30). Sin ese detector (alumna LIN) NO aprende el bit de suma, que es un XOR: se queda en 48 %. El acarreo (1+1, que es un AND) y el 0+0 sí los aprende.
2. **¿La sabia ayuda?** Sube el acierto mientras está (sabia más rápida en 24 a 30 de 30 semillas), pero sobre todo porque la alumna la COPIA. Lo que la alumna aprende por su cuenta depende de su regla. Si sus rasgos compiten (RW), aprende lo mismo que sola. Si sus rasgos no compiten (IND), aprende algo más: +0,06 a +0,08 en el examen. Si no tiene detector de pares (LIN), aprende MENOS que sola: la sabia es una muleta que bloquea el aprendizaje propio.
3. **¿Cuánto retienen?** Si la alumna podía aprender sola, retiene casi todo (de 92 a 100 % en el examen al irse la sabia). Si dependía de la sabia (LIN en la tarea de bits), al irse la sabia cae de 92 % a 46 %: falla justo 0+1 y 1+0 (el XOR) y conserva 0+0 y 1+1.
   Extra: una hija que hereda la memoria de su madre sí empieza sabiendo (90 a 93 % en sus primeros 100 ensayos, contra 60 a 78 % si nace en blanco).

## Montaje (mini-mundo propio en Python puro; no se usó la pista de la carrera)
- **Cada ensayo:** llegan a y b (bits al azar). Si acierta, comida (+1); si falla, veneno (-0,2).
- **Dos versiones de la tarea:**
  - CLASES: elige entre 0, 1 y 10.
  - BITS: dos salidas, el bit de suma y el de acarreo. Solo come si acierta las dos. Esta es la suma "con bits" de verdad.
- **Alumna:** aprende por asociación el valor de cada respuesta a partir de sus rasgos: sesgo, a, b, el par (a,b) y la señal de la pizarra si hay sabia. Explora el 10 % de las veces (eps=0,1), así que el techo es 0,93 en CLASES y 0,90 en BITS.
- **Tres reglas de aprendizaje:**
  - RW: Rescorla-Wagner, los rasgos comparten el error y compiten.
  - IND: cada rasgo aprende por separado.
  - LIN: igual que RW pero sin el rasgo de par.
- **Cuatro brazos:**
  - SOLA.
  - SABIA: escribe a+b en la pizarra.
  - MENTIROSA: escribe algo al azar (control).
  - SABIA_RETIRO: la sabia se va en el ensayo 1000 de 2000. Hay versiones extra en las que se va en el 50, el 100 y el 200.
- **Examen:** acierto sin exploración, sin aprender y sin sabia en las 4 combinaciones.

## Tabla (30 semillas, 7001-7030, 2000 ensayos; t85 = ensayos hasta 85 % en una ventana de 50)
| tarea | regla | t85 SOLA | t85 SABIA | sabia más rápida | examen final SOLA | examen al irse la sabia (ensayo 1000) | acierto 100 antes / después del retiro | MENTIROSA acierto final |
|---|---|---|---|---|---|---|---|---|
| CLASES | RW | 69 | 56 | 29/30 | 1.00 | 1.00 | 0.94 / 0.94 | 0.93 |
| CLASES | IND | 247 | 185 | 23/30 | 1.00 | 1.00 | 0.94 / 0.94 | 0.93 |
| CLASES | LIN | 162 | 66 | 30/30 | 0.93 | 0.85 | 0.94 / 0.83 | 0.84 |
| BITS | RW | 153 | 116 | 24/30 | 1.00 | 0.96 | 0.92 / 0.87 | 0.91 |
| BITS | IND | 655 | 258 | 19/30 | 0.89 | 0.92 | 0.85 / 0.82 | 0.71 |
| BITS | LIN | nunca (0/30) | 127 | 30/30 | 0.48 | **0.49** | **0.92 / 0.46** | 0.48 |

**Lo que la alumna sabe POR SU CUENTA** (examen sin sabia en el mismo ensayo; la sabia se fue en ese ensayo, comparada con una alumna SOLA):

| tarea | regla | ensayo 50 | ensayo 100 | ensayo 200 |
|---|---|---|---|---|
| CLASES | RW | 0.99 vs 0.94 | 1.00 vs 0.99 | 1.00 vs 0.99 |
| CLASES | IND | 0.67 vs 0.61 | 0.77 vs 0.73 | 0.88 vs 0.82 |
| CLASES | LIN | 0.65 vs 0.64 | **0.72 vs 0.83** | **0.82 vs 0.93** (la muleta estorba) |
| BITS | RW | 0.67 vs 0.66 | 0.81 vs 0.82 | 0.92 vs 0.94 (sin ganancia) |
| BITS | IND | 0.57 vs 0.50 | 0.66 vs 0.60 | 0.78 vs 0.70 |
| BITS | LIN | 0.47 vs 0.43 | 0.49 vs 0.47 | 0.51 vs 0.53 |

**Por combinación** (BITS, LIN, examen al irse la sabia): 0+0 = 1.00, 0+1 = 0.00, 1+0 = 0.00, 1+1 = 0.97. Falla la parte XOR y conserva la parte AND. En IND BITS pasa al revés: la que falla es 1+1 (0,49 de acierto final en SOLA), o sea, el acarreo.

**Hija que hereda la memoria de una madre SOLA** (acierto en sus primeros 100 ensayos, con semilla de la hija distinta de la de la madre):

| tarea | regla | hereda 0 % | hereda 50 % | hereda 100 % |
|---|---|---|---|---|
| CLASES | RW | 0.78 | 0.93 | 0.93 |
| CLASES | IND | 0.55 | 0.92 | 0.93 |
| BITS | RW | 0.60 | 0.88 | 0.90 |
| BITS | IND | 0.49 | 0.77 | 0.80 |

## Qué tan confiable es
- 30 semillas por celda, emparejadas: SOLA y SABIA usan la misma secuencia de estímulos.
- Las diferencias grandes son robustas: LIN no puede hacer el XOR; la muleta hace caer a LIN de 0,92 a 0,46; la sabia es más rápida en 29-30 de 30 con RW/LIN en CLASES. Las chicas (+0,06 de IND, RW sin ganancia) no tienen prueba formal.
- **Limitaciones serias:**
  - Con solo 4 combinaciones y un rasgo por par, "sumar" aquí es memorizar una tabla de 4 filas. No es generalizar la aritmética.
  - El mini-mundo no tiene cuerpo, espacio ni hambre, y la comida no se agota.
  - La sabia es perfecta y se ve como una entrada más; no se parece a una danza de abejas real.
  - Los parámetros son los primeros que se probaron (eta=0,15, eps=0,1, veneno -0,2), sin barrido.
- Predicción propia que resultó falsa: esperaba que RW mostrara un bloqueo fuerte con la sabia (poca retención). No pasó: RW retiene 0,96-1,00. El bloqueo real aparece solo en LIN.

## Qué queda
- Probar sumas de 2 bits + 2 bits, para ver si generaliza o solo memoriza.
- Llevar la tarea a la pista de la carrera con cuerpo y hambre.
- Hacer que la sabia sea otra bacteria que aprendió (no un oráculo).
- Si algo de esto apunta al tronco, correrlo con el protocolo formal.

## Archivos
- `escuela.py`: brazos, reglas y tabla. Uso: `python escuela.py [--humo] [--bits]`. Escribe `resultados[_humo]_{CLASES|BITS}.json/.txt`.
- `extra.py`: pareado SOLA/SABIA y la sabia que se va temprano. Uso: `python extra.py [--bits]`. Escribe `extra_{CLASES|BITS}.txt`.
