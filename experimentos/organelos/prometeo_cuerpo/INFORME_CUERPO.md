# EXPLORATORIO, no es dato

# PROMETEO-CUERPO: la cinta puede escribirse partes del cuerpo (Opus, 25-sep-2026, 11:40–13:40)

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).

**Veredicto: HAY ALGO MODESTO.** Una parte del cuerpo aparece de la nada y la selección la fija por su efecto, pero solo donde el efecto es grande.
- **En `niebla`, el OJO pasa la lectura propuesta antes de correr:** se fija en 7/10 semillas de CUERPO y en 0/10 de CUERPO_MUDO.
  - Con él, la población vive sola mejor: persiste en 8/10 contra 4/10, y deja más nacimientos después del corte en 8/10 semillas pareadas.
- **En `veneno`, el ESCUDO no pasa** (0/10). En `quieto` no se fija ninguna parte.
- **Ojo con el borde:** 7/10 es justo el umbral, con 10 semillas y en un mundo que yo armé para que el ojo importe.

## 1. Qué construí (`experimentos/organelos/prometeo_cuerpo/`; solo copias; semillas 31101–31110 y 31901–31902)
- **`construye_cuerpo.py`** construye por anclas de texto (los originales solo se leen):
  - `codigo_cuerpo.py`, desde `prometeo/codigo_prometeo.py`: agrega la instrucción **`PARTE p`**;
  - `motor_cuerpo.py`, desde `prometeo/motor_prometeo.py`: el mundo aplica el efecto y el costo;
  - `carros/FAMB_GRAM_ECO.py`, desde `codigo/carros/`: solo aprende a no reventar cuando no ve nada; con la vista completa es el mismo carro, bit a bit.
- **Cómo aparecen las partes:** nacen **ausentes**. Entran por inserción o cambio entero en la copia, o por HGT. REP, DEF y LLAMA las multiplican como a un gen.
- **Efecto:** con k copias leídas (tope 8), el efecto es `MAX·(1 − 0.5^k)`.
- **Costo:** lineal, en energía por paso. Como referencia, el metabolismo basal gasta 0.001 por paso.
- **El cerebro no sabe qué cuerpo tiene.** El efecto es física del mundo, y el carro recibe las señales nominales de la mordida.

| parte | efecto físico (1 copia) | costo por copia y paso (ronda 2) |
|---|---|---|
| PATA | si se mueve, no muerde y cae en una celda vacía: otro paso con prob 0.30 | 0.0001 |
| ESCUDO | daño de veneno o de sal ×0.70 | 0.0004 |
| ESTÓMAGO | tope de la reserva de E y de Ag: 1.5 → 2.0 | 0.0004 |
| OJO | radio de vista +20. **Sin niebla es INERTE** (el carro ya ve el anillo entero) | 0.0002 |
| MANDÍBULA (mía) | la comida y el agua buenas rinden ×1.25 | 0.0002 |
| LENGUA (mía) | escupe un bocado dañino con prob 0.40; el objeto queda en el mundo | 0.0002 |

- **Brazos:**
  - **CUERPO:** alfabeto v0 + kit de Prometeo (CABLE, HGT) + PARTE. Las partes actúan y cobran.
  - **CUERPO_MUDO:** las mismas partes y el mismo costo, sin efecto.
  - Los dos usan la cinta v0 sin SOS (la de CODIGO_SIN_SOS).
- **Mundos:**
  - `quieto`;
  - `niebla`: `quieto` más vista de radio 12, sobre un anillo de 1 200 celdas;
  - `veneno`: B y D valen −0.8 desde t 0 (el doble que en fábrica).
- **Tiempos:** T 60 000, corte en 44 000 (después nadie repone nada). Es el TL "largo" de Prometeo.
- **Seguridad:** la cinta sigue siendo un lenguaje cerrado de tuplas validadas. No hay `eval` ni `exec`, y no toca archivos ni red.

## 2. Identidad (`identidad_cuerpo_salida.txt`: **14/14 en la primera pasada**, sin cambios de criterio)
- **Sin partes es Prometeo bit a bit:**
  - IC1: PROMETEO con copia prendida;
  - IC2: CODIGO_SIN_SOS;
  - IC3: MUT0 con PARTE en el alfabeto;
  - IC4: niebla 600, que ve todo, da lo mismo que sin niebla.
- **IC5:** la niebla ciega de verdad.
- **Arnés por pieza.** Con una copia en los 30 fundadores y la copia apagada, cada parte mueve su contador físico y en MUDO queda en 0:
  - PATA: 39 297 pasos extra;
  - ESCUDO: 192 de daño evitado;
  - ESTÓMAGO: 371 guardados por encima de 1.5;
  - MANDÍBULA: 438 de ganancia extra;
  - LENGUA: 1 146 escupidas.
- **OJO:** sin niebla, ON == MUDO bit a bit. Con niebla 5, los pasos ciegos bajan de 0.92 a 0.22.
- **Costo:** seis partes sin efecto y sin costo dan MUT0 bit a bit. Con costo se cobra, y los nacimientos bajan de 78 a 27.

## 3. Calibración (declarada antes, en `PREDICCIONES_previas.md`)
- **Ronda 1**, incompleta porque el director paró a las 12:00:
  - condiciones: 15 contra 15, copia apagada, T 16 000, s31901, solo el brazo ON;
  - fracción del banco final con la parte:

    | parte | banco final |
    |---|---|
    | PATA | 0.11 |
    | ESCUDO (en veneno) | 0.94 |
    | ESTÓMAGO | 1.00 |
    | OJO (niebla 5) | 1.00 |
    | MANDÍBULA | 0.58 |
    | LENGUA | 0.885 |

- **Ronda 2**, declarada a las 12:12, antes del exploratorio: PATA con la mitad de costo; ESCUDO y ESTÓMAGO con el doble; niebla de 5 a 12.
  - No la volví a medir con la competencia: fue una sola ronda de ajuste, como se pidió.

## 4. Qué pasó (60 corridas, 0 abortadas, 0 bloqueadas; 5 procesos a la vez, uno por corrida, sin Pool)
**Fijada** = la parte está en ≥ 0.5 del banco (los padres de los 200 nacimientos más recientes) en el corte o al final.
La lectura "elige por efecto" exige ≥ 7/10 en CUERPO y ≤ 3/10 en MUDO.

| mundo | parte | fijada CUERPO | fijada MUDO | banco en el corte C / M (mediana) | banco final C / M (mediana) | lectura |
|---|---|---|---|---|---|---|
| quieto | PATA | 1/10 | 0/10 | 0 / 0 | 0.007 / 0 | – |
| quieto | ESCUDO | 0/10 | 0/10 | 0 / 0 | 0 / 0 | – |
| quieto | ESTÓMAGO | 0/10 | 0/10 | 0 / 0 | 0.005 / 0 | – |
| quieto | OJO (inerte) | 0/10 | 0/10 | 0 / 0.003 | 0 / 0 | – |
| quieto | MANDÍBULA | 0/10 | 0/10 | 0.005 / 0 | 0 / 0 | – |
| quieto | LENGUA | 0/10 | 0/10 | 0.007 / 0.013 | 0 / 0 | – |
| veneno | PATA | 2/10 | 0/10 | 0.083 / 0 | 0.043 / 0 | – |
| veneno | **ESCUDO** | **0/10** | 0/10 | 0 / 0 | 0 / 0 | – |
| veneno | ESTÓMAGO | 3/10 | 0/10 | 0.015 / 0 | 0.028 / 0 | – |
| veneno | OJO (inerte) | 0/10 | **1/10** | 0 / 0 | 0 / 0 | – |
| veneno | MANDÍBULA | 1/10 | 0/10 | 0 / 0 | 0 / 0 | – |
| veneno | LENGUA | 1/10 | 0/10 | 0 / 0 | 0 / 0 | – |
| niebla | PATA | 1/10 | 0/10 | 0.007 / 0.013 | 0.007 / 0.013 | – |
| niebla | ESCUDO | 0/10 | 0/10 | 0.005 / 0.003 | 0.005 / 0.003 | – |
| niebla | ESTÓMAGO | 1/10 | 0/10 | 0.007 / 0 | 0 / 0 | – |
| niebla | **OJO** | **7/10** | **0/10** | **0.43 / 0** | **0.64 / 0** | **ELIGE POR EFECTO** |
| niebla | MANDÍBULA | 1/10 | 0/10 | 0.003 / 0 | 0 / 0 | – |
| niebla | LENGUA | 0/10 | 0/10 | 0.007 / 0 | 0.005 / 0 | – |

"Nac solo" = nacimientos después del corte, sin reponedor.

| mundo | brazo | persiste | nac solo (suma · mediana) | CUERPO > MUDO en nac solo (pareado) | largo del banco final (mediana) | fracción de pasos ciegos |
|---|---|---|---|---|---|---|
| quieto | CUERPO | 10/10 | 1 289 · 124.5 | 5/10 | 33.4 | – |
| quieto | MUDO | 10/10 | 1 363 · 131.5 | | 34.8 | – |
| veneno | CUERPO | 10/10 | 1 141 · 116 | 5/10 | 32.5 | – |
| veneno | MUDO | 10/10 | 1 431 · 112.5 | | 33.8 | – |
| niebla | CUERPO | **8/10** | **817 · 64** | **8/10** | 31.8 | 0.42 |
| niebla | MUDO | **4/10** | 418 · 38.5 | | 32.3 | 0.57 |

**Barridos transitorios** (`barrido_nacidos.py`, `datos/BARRIDOS_largo.txt`; medida agregada DESPUÉS de ver la tabla, así que es descriptiva y no entra en la lectura).
Cuento que una parte "barre" si la llevan ≥ 50 % de los nacidos en alguna ventana de 2 000 pasos con ≥ 20 nacidos. El banco del corte y del final no ve estos barridos.

| mundo | barridos en CUERPO | barridos en MUDO |
|---|---|---|
| niebla | OJO 5, más PATA, MANDÍBULA y ESTÓMAGO 1 cada una (6/10 semillas con alguno) | ninguno (0/10) |
| veneno | ESTÓMAGO 3, PATA 2, ESCUDO 1 (se pierde), LENGUA 1, MANDÍBULA 1 (5/10 semillas) | OJO 1: una parte inerte y con costo, llevada por la deriva |
| quieto | PATA 1, LENGUA 1 | ESCUDO 1, PATA 1 |

- **¿Aparecen donde sirven?**
  - El OJO, sí: en `niebla` supera a su nivel en `quieto` en 7/10 semillas y en `quieto` nunca se fija.
  - El ESCUDO, no. En `veneno` supera a `quieto` solo en 2/10, y la LENGUA en 3/10.
  - En `veneno`, la selección elige otras partes: ESTÓMAGO y PATA.
  - El ESCUDO evitó una mediana de 40 de daño en toda la corrida, contra 16 en `quieto`.
  - **Hipótesis sin verificar:** el carro aprende a no morder B (R = −3), así que el veneno casi no se muerde y el escudo paga costo por un daño raro.

## 5. Tres bichos en humano
1. **`niebla` s31107, CUERPO: el que abrió los ojos.**
   - **Hasta t 20 000:** medio ciego. Nacen unos 30 por ventana y ninguno tiene ojo.
   - **La subida:** el OJO aparece por error de copia hacia t 20 000, en el 6 % de los nacidos. Sube al 18 % en 24 000, al 32 % en 28 000, al 73 % en 32 000 y al 89 % en el corte.
   - **Después del corte:** el 96–100 % lo lleva. Algunos traen dos copias (media 1.3), porque el ojo quedó dentro de un bloque REP 2.
   - **Nacimientos:** pasaron de ~30 a ~70–80 por ventana mientras el ojo se extendía. Después del corte deja **175 nacimientos solos** y persiste.
   - El resto de su cuerpo quedó desnudo: ninguna otra parte pasa del 1 %.
2. **`niebla` s31106, CUERPO: el explorador con mandíbula, que luego se desvistió.**
   - **Arranque:** OJO y MANDÍBULA suben juntos desde t 8 000. En 16 000 los llevan el 36 % y el 51 % de los nacidos.
   - **Auge:** hacia t 28 000 la población explota, de ~70 a **218–250 nacimientos por ventana**, con OJO 0.83–1.0 y MANDÍBULA 0.72–0.94. Después se suman las PATAS: 0.82 en 36 000.
   - **Corte:** la población cae de 68 a unos 16 nacimientos por ventana. **Solo queda el OJO**, en el 100 %; PATA y MANDÍBULA desaparecen de los nacidos.
   - **Lectura:** parece que viajaron de pasajeras en el auge y el ojo es lo único que se sostiene solo. Sin verificar.
   - Lleva además `CABLE(edad→boca, −1)`: cuanto más viejo, menos muerde.
   - Deja 2 756 nacimientos en total y 149 solos, y persiste.
3. **`veneno` s31110, CUERPO: escudo primero, patas después.**
   - **El escudo:** es la única semilla donde el escudo hace lo que predije, y dura poco. Aparece en t 8 000 (42 % de los nacidos) y en 12 000 lo lleva el **93 %**.
   - **El relevo:** desde 16 000 lo desplazan las PATAS. El escudo baja a 0.44, a 0.11 y a 0.03, mientras las patas suben a 0.49, a 0.81 y a **1.00** desde 32 000.
   - **La cinta final (135/200 del banco):** una pata y un cable `la otra reserva → patas, +1` (cuanto más lleno del otro recurso, más camina). El kit contó 30 790 pasos forzados.
   - Deja 146 nacimientos solos y persiste.
   - En la tabla final cuenta como "escudo 0/10", pero el escudo sí apareció donde servía y ganó un tiempo.

## 6. Lectura honesta
- **Lo nuevo.**
  - Los órganos de transmisión de Prometeo se fijaban igual en MUDO, porque manda el azar.
  - Una parte de efecto **grande** (ver en un mundo donde casi no se ve) aparece de novo por error de copia, y **la selección la lleva al banco en 7/10 contra 0/10**, con N chico (w30, 10–80 vivos).
  - Con eso, la población vive sola mejor: 8/10 contra 4/10 en persistencia.
  - Es coherente con la razón del director: si el efecto es grande, la selección le gana al azar aunque N sea chico.
  - En `veneno` pasa algo parecido, más débil: hay barridos con efecto en 5/10 semillas contra 1/10 en MUDO, pero de partes que yo no esperaba.
- **Lo que no es.**
  1. **La niebla la hice yo para que el ojo importe.** Con radio 12, el 57 % de los pasos quedan ciegos sin ojo. El resultado dice que la selección funciona con un efecto así de grande, no que el cuerpo "invente" lo que necesita en un mundo cualquiera.
  2. **El control MUDO no es neutro.** Sus partes cuestan y no hacen nada, así que se espera que no se fijen. Un control de deriva pura (sin efecto y sin costo) no se corrió.
     - Aun así, en `veneno` una parte inerte y con costo (el OJO en MUDO) barrió en 1/10 semillas. La deriva también fija lo costoso, a veces.
  3. **7/10 es el borde exacto del umbral.** Con 10 semillas, una más o una menos cambia la lectura.
  4. **En `quieto`, CUERPO ≈ MUDO en todo.** Donde el mundo no pide nada, el cuerpo no compra nada, y los nacimientos solos no mejoran (5/10).
- **Ganancia neta en nacimientos solos:** solo en `niebla`. En `veneno` y `quieto`, 5/10.

## 7. ¿Merece preregistro? Sí, uno chico, con la pregunta de la escala del efecto
**Pregunta:** ¿la probabilidad de que una parte aparecida de novo se fije por su efecto crece con el tamaño del efecto, en w30? ¿Y la misma parte no se fija donde no sirve?

- **Brazos:**
  - CUERPO;
  - CUERPO_MUDO;
  - **CUERPO_NEUTRO**: sin efecto y sin costo, la deriva pura. Falta hoy;
  - **LESIÓN**: en el corte, se le quita el OJO al banco de CUERPO y se compara la persistencia. Es la prueba causal.
- **Mundos:** niebla de radio 8, 12 y 20 (dosis: efecto grande, medio y chico) y `quieto` (donde el OJO es inerte).
- **Diseño:** 20 semillas, T 60 000, el mismo instrumento, con la calibración de la ronda 2 congelada.
- **Predicciones a escribir:**
  - OJO fijado en ≥ 14/20 en niebla 12;
  - una tendencia monótona con el radio (8 > 12 > 20);
  - ≤ 4/20 en NEUTRO, en MUDO y en `quieto`;
  - LESIÓN: la persistencia baja en ≥ 14/20 pares.
- **Costo:** unas 240 corridas de ~8 min. Con 5 procesos son unas 6.5 h: conviene esperar al gemelo rápido o recortar dosis.

## 8. Predicciones refutadas y lo no verificado
Mis predicciones N1–N6 están en `PREDICCIONES_previas.md` (12:12, antes de correr). Reemplazaron a las 1–7, que eran para el diseño de 3 brazos que no se corrió.

| predicción | resultado |
|---|---|
| **N1:** el OJO pasa en niebla | **se cumplió**, en el borde (7/10 contra 0/10) |
| **N2:** el ESCUDO o la LENGUA pasan en `veneno` | **REFUTADA** (0/10 y 1/10) |
| **N3:** el ESTÓMAGO pasa en `quieto` con costo doble | **REFUTADA** (0/10). La parte "la PATA no pasa" se cumplió |
| **N4:** el OJO es inerte en `quieto` | se cumplió (0 contra 0) |
| **N5:** MUDO nunca pasa de 3/10 | se cumplió (máximo 1/10) |
| **N6:** CUERPO > MUDO en nac solo | en niebla **se cumplió** (8/10); en `veneno` **refutada** (5/10, se pedía 7); en `quieto` **refutada** (5/10, se pedía 6) |

**No verifiqué:**
- la causalidad del OJO en los bichos, porque no hubo lesión ni trasplante;
- si la ronda 2 de calibración deja cada parte en rango, porque no se volvió a medir la competencia;
- el efecto de la HGT sobre las partes. Hubo PARTE transferidas por HGT (kit `hgt_ops`), pero no las separé;
- `onda8k`, que no se corrió;
- si los cuerpos se estabilizan más allá de T 60 000.

## Archivos
- **Instrumento:** `construye_cuerpo.py`, `codigo_cuerpo.py`, `motor_cuerpo.py`, `carros/FAMB_GRAM_ECO.py`.
- **Arnés:** `identidad_cuerpo.py` y `identidad_cuerpo_salida.txt`.
- **Corrida y lectura:** `corre_cuerpo.py`, `lee_cuerpo.py`, `barrido_nacidos.py`.
- **Datos:**
  - `datos/{quieto,veneno,niebla}_largo/*.json`: guardan el banco de cintas en el corte y al final;
  - `datos/LECTURA_largo.txt`, `datos/BARRIDOS_largo.txt`;
  - `datos/cal_r1/`.
- **Notas y predicciones:** `NOTAS_PARA_MUNDO_GRANDE.md`, `PREDICCIONES_previas.md`.
