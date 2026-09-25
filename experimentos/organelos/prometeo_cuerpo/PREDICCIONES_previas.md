# EXPLORATORIO, no es dato

# PROMETEO-CUERPO: predicciones escritas ANTES de correr (Opus, 25-sep-2026, 11:50)

Misión: llegar a la AGI por este camino.
Estas predicciones se escriben antes de cualquier humo, calibración o corrida. Si una no se cumple, se declara refutada en el informe.

## Lo que se construye (para que las predicciones tengan sentido)
- Una instrucción nueva de la cinta, `PARTE p`, con seis partes: PATA, ESCUDO, ESTÓMAGO, OJO, MANDÍBULA y LENGUA.
- La cinta inicial no trae ninguna. Solo aparecen por inserción o por cambio entero en la copia, o llegan por HGT.
- Cada copia de una parte cuesta energía por paso (costo lineal). Su efecto crece con rendimiento decreciente: `1 − 0.5^k`.
- **OJO:** en `quieto`, `onda8k` y `veneno` el carro ya ve el anillo entero (ENMIENDA 1, opción A), así que el OJO no tiene qué agregar. Ahí es una parte INERTE por construcción: cuesta y no hace nada. Solo tiene efecto en el mundo `niebla`, que limita la vista.

## Predicciones sobre la ventana exploratoria (6 semillas por brazo y mundo)
1. **Aparición.** En CUERPO y en CUERPO_MUDO aparece al menos una parte en el banco, en algún momento, en todas las semillas.
2. **Fijación con efecto contra sin efecto.** Alguna parte supera el 50 % del banco, en el corte o al final, en al menos 1/3 de las corridas de CUERPO. En CUERPO_MUDO lo hace en a lo sumo 1 de cada 5 corridas: sin efecto, el costo la empuja hacia abajo.
3. **Cuál gana en `quieto`.** El ESCUDO es la parte más frecuente en el banco de CUERPO, porque la población muerde el veneno casi tanto como la comida (lo midió Fable: 0.46 contra 0.48).
4. **Donde sirve (`veneno`).** La fracción del banco con ESCUDO o LENGUA es mayor en `veneno` que en `quieto` en CUERPO, en al menos 4/6 semillas pareadas. Entre las dos, la LENGUA sale más frecuente que el ESCUDO: escupir evita todo el daño.
5. **OJO inerte.** En `quieto` y `onda8k`, la fracción del banco con OJO en CUERPO queda a ±0.10 de la de CUERPO_MUDO (mediana). En `niebla`, el OJO de CUERPO supera al de CUERPO_MUDO en al menos 4/6 semillas.
6. **¿Viven solos mejor?** Casi nada. CUERPO le gana a PROMETEO en nacimientos después del corte en 3 o 4 de 6 semillas por mundo, sin un patrón claro. CUERPO_MUDO pierde contra PROMETEO en al menos 4/6 en `quieto`, porque solo paga el costo.
7. **Largo.** La cinta de CUERPO termina entre 1 y 3 instrucciones más larga que la de PROMETEO (mediana del banco final).

## Criterio de calibración (fijado antes de la calibración; se aplica a lo sumo en 3 rondas)
- **Prueba:** competencia 15 contra 15.
  - Treinta fundadores, con la copia apagada (MUT0).
  - Quince llevan la cinta v0 más UNA copia de la parte; los otros quince, la cinta v0 sola.
  - T 16 000, semilla 31901.
  - Mundo propio de cada parte: `quieto` para PATA, ESTÓMAGO, MANDÍBULA y LENGUA; `veneno` para ESCUDO; `niebla` para OJO.
  - Brazo con efecto (ON) y brazo MUDO.
- **Medida:** fracción del banco final (200 donantes recientes) que lleva la parte.
- **Aceptable:**
  - ON entre 0.25 y 0.90: ni gratis ni dominante;
  - MUDO ≤ ON.
- **Ajustes:**
  - si ON > 0.90, el costo de esa parte se duplica;
  - si ON < 0.25, el costo baja a la mitad.
- Toda regla nueva que invente después de ver un humo será un ERR (desde ERR-145).
