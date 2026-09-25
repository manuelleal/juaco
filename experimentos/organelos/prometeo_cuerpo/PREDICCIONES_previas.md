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

---

## RECALIBRACIÓN DECLARADA ANTES DE CORRER (25-sep-2026, 12:12; una sola ronda; no se mira el exploratorio para ajustar)
- **Base:** la ronda 1 de calibración quedó incompleta (s31901, solo el brazo ON).
  - Fuera de rango: PATA 0.11, ESCUDO 0.94 (veneno), ESTÓMAGO 1.00, OJO 1.00 (niebla 5).
  - En rango: MANDÍBULA 0.58 y LENGUA 0.885.
- **Ajuste (el que propuse en NOTAS_PARA_MUNDO_GRANDE.md):**
  - costo por copia y por paso: PATA 0.0001 (la mitad), ESCUDO 0.0004 (el doble), ESTÓMAGO 0.0004 (el doble); OJO, MANDÍBULA y LENGUA quedan en 0.0002;
  - niebla: radio **12** (antes 5);
  - las magnitudes de efecto no cambian.
- **No vuelvo a calibrar.** Si con esto alguna parte sigue siendo dominante, se reporta tal cual.
- **No es ERR:** todavía no hay nada juzgado.

## EXPLORATORIO rápido (reabierto por el director, 12:12)
- **Diseño:**
  - 10 semillas (31101–31110);
  - brazos CUERPO y CUERPO_MUDO, pareados por semilla;
  - mundos `quieto`, `niebla` (radio 12) y `veneno` (B y D a −0.8), en ese orden de prioridad;
  - T 60 000, cambio nominal en 8 000, corte en 44 000.
- **Lectura propuesta ANTES de correr (la del coordinador):** "la selección elige la parte por su efecto" si la parte se fija (≥ 0.5 del banco, en el corte o al final) en **≥ 7/10 en CUERPO y ≤ 3/10 en MUDO**, en ese mundo.
- **Predicciones nuevas, que reemplazan las 1–7 para este diseño:**
  - **N1.** En `niebla`, el OJO pasa la lectura: ≥ 7/10 en CUERPO y ≤ 3/10 en MUDO.
  - **N2.** En `veneno`, el ESCUDO o la LENGUA la pasan (al menos una de las dos).
  - **N3.** En `quieto`, el ESTÓMAGO la pasa aun con el doble de costo. La PATA no la pasa.
  - **N4.** El OJO en `quieto` es inerte: se fija igual de poco en CUERPO que en MUDO (diferencia ≤ 2/10).
  - **N5.** En MUDO ninguna parte se fija en más de 3/10, en ningún mundo.
  - **N6.** CUERPO deja más nacimientos solos que MUDO en ≥ 7/10 semillas pareadas en `niebla` y en `veneno`; en `quieto`, en ≥ 6/10.
