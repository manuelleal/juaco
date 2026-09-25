# EXPLORATORIO, no es dato

# PROMETEO-CUERPO: notas para cuando exista el mundo grande (Opus, 25-sep-2026, 12:05)

Misión: llegar a la AGI por este camino.

**Estado: DETENIDO por el director a las 12:00.** La serie de Prometeo dio que los órganos armados no se fijan más que en MUDO y hubo 0 despegues. Este ejercicio usa la misma base y el mismo mundo (w30), así que no se lanzó la ventana exploratoria.
Queda: el instrumento construido, el arnés 14/14 y media ronda de calibración (1 semilla, solo el brazo ON).

## Archivos (todo en `prometeo_cuerpo/`, solo copias)
- **`construye_cuerpo.py`**: construye por anclas de texto, sin tocar los originales:
  - `codigo_cuerpo.py`, desde `prometeo/codigo_prometeo.py`;
  - `motor_cuerpo.py`, desde `prometeo/motor_prometeo.py`;
  - `carros/FAMB_GRAM_ECO.py`, desde `codigo/carros/FAMB_GRAM_ECO.py`. Este solo cambia en una cosa: si no ve ningún objeto (niebla), no revienta.
- **`identidad_cuerpo.py`** → `identidad_cuerpo_salida.txt`: **14/14 en la primera pasada**, sin cambios de criterio.
- **`corre_cuerpo.py`**: runner de un proceso, sin Pool. Tiene los brazos CUERPO, CUERPO_MUDO y PROMETEO y el modo `--cal` (competencia 15 contra 15).
- **`lee_cuerpo.py`**: lectura descriptiva. No se llegó a usar sobre datos de la ventana.
- **`PREDICCIONES_previas.md`**: predicciones y criterio de calibración, escritos antes de correr. Quedan sin evaluar.

## Las partes (instrucción nueva de la cinta: `PARTE p`)
- **Cómo aparecen:** nacen ausentes. Entran por inserción, por cambio entero en la copia o por HGT. REP, DEF y LLAMA las multiplican como a cualquier gen.
- **Efecto:** con k copias leídas (tope 8), el efecto es `MAX × (1 − 0.5^k)`, con rendimiento decreciente.
- **Costo:** lineal, `k × 0.0002` de E por paso. Como referencia, el metabolismo basal gasta 0.001 por paso: cada copia cuesta un 20 % del basal.
- **Quién aplica el efecto:** el mundo, como física. El carro no sabe qué partes tiene y recibe las señales nominales de la mordida.

| parte | efecto físico (MAX) | 1 copia |
|---|---|---|
| PATA | si se mueve, no muerde y cae en una celda vacía: otro paso en la misma dirección con prob 0.6·R | p = 0.30 |
| ESCUDO | cada componente negativa de una mordida (veneno B en E, sal D en Ag) × (1 − 0.6·R) | −30 % de daño |
| ESTÓMAGO | tope de la reserva de E y de Ag: 1.5 → 1.5 + 1.0·R | tope 2.0 |
| OJO | radio de vista = niebla + 40·R. **Sin niebla es INERTE** (el carro ya ve el anillo entero, ENMIENDA 1 opción A) | +20 celdas |
| MANDÍBULA (nueva) | cada componente positiva × (1 + 0.5·R) | +25 % de comida |
| LENGUA (nueva) | si el bocado daña, lo escupe con prob 0.8·R: no hay efecto ni aprendizaje, y el objeto queda | p = 0.40 |

- **CUERPO_MUDO:** las partes cobran y no actúan (`partes_on=False`).
- **Mundo `niebla`:** eco `niebla=r`. El cuerpo solo ve los objetos a distancia ≤ r, más lo que agregue su OJO.
- **Mundo `veneno`:** B y D valen −0.8 desde t 0 (en fábrica valen −0.4).
- **Rng propio:** `random.Random(seed·7919+31)`. Solo se consume con PATA o LENGUA activas.

## Identidad (14/14; onda8k, T 6000)
- **Sin partes es Prometeo bit a bit:**
  - IC1: PROMETEO con copia prendida;
  - IC2: CODIGO_SIN_SOS;
  - IC3: MUT0 con PARTE en el alfabeto;
  - IC4: niebla 600, que ve todo, da lo mismo que sin niebla.
- **Arnés por pieza.** Con 1 copia en los 30 fundadores y la copia apagada, cada parte actúa y en MUDO su contador queda en 0:

  | caso | contador de la parte | nacimientos |
  |---|---|---|
  | PATA | 39 297 pasos extra | 67 |
  | ESCUDO | 192 de daño evitado | 89 |
  | ESTÓMAGO | 371 guardados por encima de 1.5 | **146** |
  | MANDÍBULA | 438 de ganancia extra | 81 |
  | LENGUA | 1 146 escupidas | 72 |
  | MUT0 (sin partes) | — | 78 |
  | MUDO de 1 parte | — | 64 |

- **OJO sin niebla:** ON == MUDO bit a bit, así que es inerte, como se diseñó.
- **Niebla 5:** el 92 % de los pasos quedan ciegos y nacen 9 (contra 69 sin niebla). Con un OJO baja a 22 % de pasos ciegos, 66 nacimientos contra 2 en MUDO.
- **Seis partes sin efecto y sin costo:** == MUT0 bit a bit. Con costo (0.0012 por paso) nacen 27 contra 78.

## Calibración (ronda 1, INCOMPLETA: 1 de 2 semillas, solo ON; no se ajustó nada)
- **Condiciones:** competencia 15 contra 15, copia apagada, T 16 000, s31901.
- **Medida:** fracción del banco final con la parte. Criterio fijado antes: aceptable entre 0.25 y 0.90.

| parte (mundo) | banco final | lectura por el criterio |
|---|---|---|
| PATA (quieto) | **0.11** | sale cara: tocaría bajar el costo a la mitad |
| ESCUDO (veneno) | **0.94** | dominante: tocaría duplicar el costo |
| ESTÓMAGO (quieto) | **1.00** | dominante: tocaría duplicar el costo |
| OJO (niebla 5) | **1.00** | dominante; con niebla 5 el mundo casi mata al que no ve |

- Faltan MANDÍBULA, LENGUA, todos los MUDO y la semilla 31902. El único proceso que quedó vivo (bloque 0/4) termina solo MANDÍBULA_ON y LENGUA_ON en `datos/cal_r1/`.
- **Lectura provisional:**
  - las magnitudes de ESTÓMAGO, ESCUDO y OJO son demasiado buenas para su costo;
  - la PATA es demasiado cara;
  - la niebla 5 es demasiado dura.

  Para el mundo grande, recalibrar desde aquí:
  - ESTÓMAGO y ESCUDO a ×2 de costo;
  - PATA a ×0.5;
  - niebla entre 10 y 15.

## Para reusarlo en el mundo grande con el gemelo rápido
- Las partes tocan cuatro puntos del motor:
  1. la vista, al construir `obs['objs']`;
  2. el movimiento, después de `b.pos += mov`;
  3. la mordida: LENGUA antes de morder; ESCUDO, MANDÍBULA y ESTÓMAGO al sumar dS;
  4. el costo, en el bucle de costos.
  Todo sale de un solo vector por cuerpo, `pt` (7 números más las copias), que se calcula al nacer y queda en caché por cinta. Portarlo a numba es directo.
- La pregunta que se quería hacer sigue abierta: ¿se fija la parte con efecto por encima de su MUDO, y aparece donde sirve (ESCUDO o LENGUA en `veneno`, OJO en `niebla`)?
  - La lección de H-PLANO y de la serie de Prometeo es que con w30 el azar manda. Esto solo tiene sentido con una población grande.
  - El OJO sin niebla es un control neutro interno gratis: sirve para medir la deriva.
