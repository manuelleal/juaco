# PREREGISTRO — EXPLORATORIO — MUNDO ENRIQUECIDO: nuez con secuencia, canal social y memoria (29-sep-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo. Encargo aprobado por el director: plan 3b de `registro/ESTADO.md` (idea del 28-sep, a partir
de chimpancés en cautiverio: sin estímulo no desarrollan nada; aprenden de otros; hacen tareas con orden).

**EXPLORATORIO.** 5 semillas, T 500 000, pool ≤ 2. §1–§8 se escriben ANTES de la explora. Los únicos números vistos antes de escribir
§7 son los del arnés y de la calibración de viabilidad (§9a, semilla de práctica 50195, declarados). El humo final (§9b) se corre DESPUÉS
de escribir §7.

## 1. Hipótesis
- **H-SEC (secuencia):** en un mundo donde parte de la comida sólo se abre con un orden (morder la llave C y, como mordida siguiente,
  la nuez), la selección arma, con el genoma de reglas de BLOQUES, un órgano secuencial: morder la nuez cuando se tiene la llave y no
  cuando no se tiene. Firma: SI = P(llave | intento de nuez) − P(llave | mordida de A común) > 0.
- **H-SOC (social):** si hay un canal local para copiar una regla del vecino que ACABA de abrir una nuez, el linaje adquiere la
  secuencia más (fracción de aperturas correctas mayor) que sin canal y que con un canal que muestra a un vecino al azar.

## 2. Mecanismo mínimo y memoria nueva
Motor `motor_enriquecido.py`, construido por 30 anclas desde `bloques/opusM/motor_bloques.py` (ff782697e54585a5, el de BLOQUES ×2).
Todo nuevo va apagado por defecto; apagado == motor_bloques bit a bit (arnés).
- **Nuez:** cada A que llega por el quimiostato llega cerrada con prob f = 0.5 (rng propio [seed, 0, 7705, 0]); capa NZ sobre la celda;
  la retina y el cerebro de fábrica la ven como A. Se abre sólo si la mordida inmediatamente anterior del cuerpo fue C (la llave).
  Abrir = A de siempre + bonus 0.8 en E y en Ag (recortado a 1.5, como todo), se consume. Morder la nuez sin llave (suelta o en orden
  inverso) = no abre, no se consume, cuesta c_fallo 0.005 de E, **borra la llave** y el cuerpo **la deja** (la celda entra a su memoria
  de rechazo de fábrica, `memoria_rechazo` pasos; calibración §9a).
- **Sentido 6 de las reglas:** "el foco es una nuez cerrada" (0/1). Sólo lo leen las reglas.
- **Acción 4 de las reglas:** impulso de copiar (suma de w de las reglas que se cumplen en el paso).
- **Canal social** (después de la fase A de cada paso; rng propio [seed, 0, 7706, 0]). Disparo: impulso > 0 y un vecino a ≤ 10 celdas
  abrió una nuez en ESTE paso. Moneda: prob min(1, impulso/3). Fuente: SOC = el que abrió (el más cercano); DESF = un vecino al azar a
  ≤ 10 celdas que NO abrió (si no hay, un vivo al azar); OFF = ninguna (se cuentan disparos y monedas). Se copia UNA regla al azar de la
  fuente (se agrega; con la lista llena reemplaza una al azar). La lista se hereda al hijo como en BLOQUES: lo copiado en vida viaja.
- **Kit:** 7 sentidos (0 hambre, 1 sed, 2 cercanía, 3 píxel del foco, 4 píxel de la última mordida, 5 R de la última, **6 nuez**) y
  5 acciones (boca, hacia, quieto, parir, **copiar**). Mismos operadores y tasas de BLOQUES (mutar 0.10, duplicar 0.02, insertar 0.02,
  HGT 0.01, borrar 0.05; tope 12 reglas; arranque VACÍO; banco 200; donante padre).
- **Memoria nueva:** por cuerpo 2 números (impulso de copiar del paso, t de la última nuez abierta); del mundo, la capa NZ. La memoria
  de la secuencia ("¿mi última mordida fue la llave?") es la de BLOQUES (sentido 4): **cero memoria nueva para la secuencia**.

## 3. Brazos (ECO w90, esc 90, 90 fundadores, quimiostato, tope 3000, FABRICA_ECO, MUT0, vivero finito t_corte 100 000)
| brazo | nueces | canal | papel |
|---|---|---|---|
| NUEZ_SOC | sí | SOC (copia al que abrió) | hipótesis |
| NUEZ_OFF | sí | apagado (mismo disparo y moneda, no copia) | sin social |
| NUEZ_DESF | sí | desfasado (mismo disparo y moneda, copia a un vecino al azar que no abrió) | control que puede fallar |
| REF | no (sin tarea secuencial) | SOC (inerte: nadie abre) | referencia, mismo kit |

**Brazo O1 (pedido del coordinador, 10:50): NO CABE sin forzarlo.** El gemelo numba sólo compila FABRICA / FABRICA_ECO / FAMB_RES0_ECO /
BAR0 (aborta con O1..O4, ver docstring de motor_bloques) y toda la capa nueva (reglas, nuez, canal) vive en el gemelo. Poner O1 exige
un gemelo nuevo de O1 con su arnés, o el motor Python (sin reglas ni nueces, y ~50× más lento). No se hace aquí.

## 4. Instrumento y anclas
- `construye_enriquecido.py` (E0–E29) → `motor_enriquecido.py`; `--verifica` IGUAL.
- `identidad_enriquecido.py` → `identidad_enriquecido_salida.txt` (salida entera): (K) anclas y shas; (A) todo apagado == motor_bloques
  (BLOQ_V y ING_F1_V: todas las claves de trabajo() y BQ_OUT); (B) nuez con f 0 y canal OFF, kit 1 == motor_bloques; (B2) canal OFF ==
  sin canal (nueces f 0.5, kit enriquecido, copia forzada) salvo los contadores de disparo/moneda; (C) controles que deben fallar
  (f 0.5 ≠ f 0; SOC ≠ OFF y copia; DESF ≠ SOC y copia; llave imposible → 0 aperturas); (S) mecánica (intentos = abre + falla; f 1 →
  toda A es nuez; el sentido nuez ACTÚA); (D) determinismo; (Q) corte de luz en 20 000 + reanuda == entera (claves, BQ_OUT, NZ_OUT);
  (R) reanudar con otra cfg (NZ o BQ) ABORTA; (L) la letra y medidas() en entradas sintéticas; banderas.
- `corre_enriquecido.py`: `--humo` (1 proceso), `--explora --pool N` (N ≤ 2), `--reanuda`, `--lee <carpeta>` (imprime y escribe
  `VEREDICTO.json` con la letra). **La cfg (BQ_CFG y NZ_CFG) se fija dentro del trabajador en cada llamada** y el motor comprueba al
  reanudar que el checkpoint es de la misma cfg (lección de pista_pob). Cada trabajo escribe `M_<brazo>_s<semilla>.json` antes de volver
  (también si aborta).

## 5. Semillas NUEVAS
grep del 29-sep en `registro/` y `experimentos/` (.py, .md): 501xx sin usos. **Explora 50101–50105.** Arnés 50181–50184. Práctica y humo
50191–50199 (usada: 50195). El otro creador (sentidos_muro) usa 592xx.

## 6. Medidas (por corrida; ventana [T/2, T] = [250 000, 500 000])
- **frac_ok** (medida principal) = aperturas / intentos de nuez en la ventana (= P(llave | intento de nuez)); con < 20 intentos → 0
  (no adquirida; el que evita las nueces no hizo la secuencia).
- **SI** = frac_ok − P(llave | mordida de A común) (con ≥ 20 de cada; si no, None → no cuenta). Balancea el azar (trampa 2): morder
  mucha agua sube las dos; sólo el control condicional sube SI.
- K (media de tam_total en la ventana), persiste, aperturas por cuerpo y 1000 pasos, copias, disparos, fracción de vivos con
  "copiar+" y con alguna regla sobre el sentido nuez en T; t_adq (primera t con frac_ok ≥ 0.6 en 20 000 pasos; descriptivo).

## 7. Predicciones firmadas (ANTES de la explora; vistos sólo el arnés y la calibración §9a)
| # | cantidad | predicción | p |
|---|---|---|---|
| E1 | validez V0–V3 (§8) | se cumple | 0.85 |
| E2 | frac_ok(NUEZ_OFF) mediana | en [0.05, 0.25] | 0.70 |
| E3 | SI(NUEZ_OFF) mediana | en [−0.35, 0.00] (sin secuencia) | 0.65 |
| E4 | P3: SI(SOC) ≥ 0.10 en ≥ 3/5 | se cumple | 0.15 |
| E5 | PS: SI(OFF) ≥ 0.10 en ≥ 3/5 | se cumple | 0.12 |
| E6 | P1: frac_ok(SOC) > frac_ok(OFF) pareado ≥ 4/5 y mediana ≥ +0.05 | se cumple | 0.15 |
| E7 | P2: frac_ok(SOC) > frac_ok(DESF) pareado ≥ 4/5 y mediana ≥ +0.05 | se cumple | 0.12 |
| E8 | copias en SOC en la ventana, mediana | < 500 (el canal casi no se usa) | 0.65 |
| E9 | K(NUEZ_OFF) > K(REF) pareado (el mundo con nueces sostiene más) | ≥ 4/5 | 0.55 |
| E10 | veredicto | NO 0.80 · HAY ALGO MODESTO 0.13 · FUNCIONA 0.07 | — |

Razón del pesimismo (declarada): en la calibración (50195, 200 000) el linaje fija "no muerdas B/D" y "ve hacia A/C" pero no la
secuencia (SI −0.22), y en la segunda mitad hubo 267 disparos y 38 monedas en todo el mundo: el canal apenas se usa.

## 8. La letra (código: `corre_enriquecido.veredicto`)
- **Validez (si algo falla: NO EVALUABLE):** V0 5 semillas × 4 brazos, T 500 000, t_corte 100 000, sin abortos, bloqueados 0 ·
  V1 cfg declarada por brazo (BQ y NZ) y carro FABRICA_ECO en cada JSON · V2 el mundo con nueces es vivible: NUEZ_SOC, NUEZ_OFF **y NUEZ_DESF**
  persisten ≥ 3/5 cada uno (enmienda H-1 del auditor, antes de datos) · V3 sanidad: hay nueces en los NUEZ_* que persisten; REF sin nueces ni copias; OFF sin copias.
- **Pares válidos (enmienda H-1 del auditor, antes de datos):** en P1 y P2 cuentan SÓLO las semillas en que los DOS brazos del par
  persisten y tienen ≥ 20 intentos de nuez en la ventana; se exigen ≥ 4 pares válidos (con menos, la puerta NO se cumple). Así un control
  extinto (frac_ok 0) no regala la victoria.
- **P1** frac_ok(SOC) > frac_ok(OFF) en ≥ 4 pares válidos **y** mediana de la diferencia (sobre los válidos) ≥ +0.05.
- **P2** (control que puede fallar) frac_ok(SOC) > frac_ok(DESF) en ≥ 4 pares válidos **y** mediana (sobre los válidos) ≥ +0.05.
- **P3** (la secuencia es real) SI(SOC) ≥ 0.10 en ≥ 3/5.
- **FUNCIONA** = P1 ∧ P2 ∧ P3 · **HAY ALGO MODESTO** = (P1 ∧ P2) ∨ (P3 ∧ (P1 ∨ P2)), sin ser FUNCIONA · **NO** en otro caso.
- **Sub-veredicto PS** (¿la selección arma la secuencia sin social?): SI(OFF) ≥ 0.10 en ≥ 3/5 → SÍ / NO. Se informa aparte.
- **P4** (firma, no entra al veredicto): fracción de vivos con "copiar+" en T, SOC > DESF pareado ≥ 4/5.
- Nulos: 4/5 bajo p = 0.5 → 0.19 (una puerta sola es débil; por eso FUNCIONA pide las tres y esto es exploratorio: si da señal, serie
  n = 20 + réplica con semillas nuevas y la misma letra con umbral 15/20).
- **Qué refuta:** H-SEC cae si P3 y PS caen con la validez intacta. H-SOC cae si P1 cae; "es copiar al que sabe" (y no más variación)
  cae si P1 pasa y P2 cae.

**Trampas revisadas:**
1. *Canal simétrico:* SOC, DESF y OFF tienen el MISMO disparo y la MISMA moneda (rng dedicado, sin tocar el resto del azar); sólo cambia
   la fuente. Arnés B2: OFF == sin canal bit a bit salvo los contadores. El kit es el mismo en los 4 brazos (REF incluido).
2. *Acierto sin balancear:* frac_ok tiene una base de azar (P(llave) por morder agua); por eso P3 usa SI contra las mordidas de A común,
   y las comparaciones son pareadas en el mismo mundo.
3. *Mundo que se come la comida:* medido y corregido ANTES de datos (§9a): sin "dejar la nuez" el linaje se quedaba pegado mordiendo
   nueces cerradas (~1/3 de los pasos) y se extinguía al cerrar el vivero. V2 lo vigila. Las nueces no abiertas ocupan cupo del mundo
   (tope 360); se registra `nueces_T`.
4. *Sitios fijos:* las nueces llegan en celdas al azar; pero la LLAVE es una letra fija (C): lo que se arma es un instinto de secuencia
   (heredable y, con el canal, cultural), no aprendizaje de la regla dentro de la vida. Declarado.

**Límite declarado del canal:** se copia una REGLA del vecino, no su conducta observada (es imitación de "memes", no inferencia del
acto). Es la versión local mínima; la versión por observación (ver A→B del vecino y armar la regla) queda para después.

## 9. Mini-prueba, calibración y números (§1–§8 no se tocan)

### 9a. Calibración de viabilidad (ANTES de §7; semilla de práctica 50195, T 200 000, 1 proceso cada una)
| corrida | motor | resultado |
|---|---|---|
| humo v0 NUEZ_SOC y NUEZ_OFF (c_fallo 0.005) | e11a4134f3daaada | extinción en t 104 341 (al cerrar el vivero): K 1.29; ~33 intentos de nuez por paso en todo el mundo (≈ 0.35 por cuerpo y paso), frac_ok 0.06; 0 disparos; SOC == OFF |
| REF (sin nueces) | e11a4134f3daaada | persiste, K 36.69; fija "píxel 4 del foco → boca −" en el 100 % (= BLOQ_V): el kit enriquecido no estorba |
| NUEZ_OFF con c_fallo 0 | e11a4134f3daaada | extinción igual (K 1.98): no es el costo, es el TIEMPO pegado a la nuez |
| NUEZ_OFF con "la deja" (memoria de rechazo tras el fallo) | **09f1f2f4d85b2368** | persiste, K 49.06; frac_ok 0.113, SI −0.223; fija "píxel 4 → boca −" y "píxel 1 → hacia +" (100 %); 267 disparos, 38 monedas; 52 s |
Decisión (antes de §7): el fallo usa la memoria de rechazo de fábrica ("la deja"); c_fallo queda en 0.005. Datos en `datos/humo_v0_motor_e11a4134/`,
`datos/practica/`, `datos/practica_c_fallo0.0/`; salidas `humo_v0_salida.txt`, `practica1_salida.txt`, `practica2_salida.txt`, `practica3_salida.txt`.

### 9b. Humo final y arnés (se completa después de §7)
- Instrumento final (sha a 16): construye_enriquecido f802e38ab5171210 · motor_enriquecido 09f1f2f4d85b2368 (`--verifica` IGUAL) ·
  corre_enriquecido a7a1eb655c9899b8 · identidad_enriquecido 6632e1a3af38f8dd → `identidad_enriquecido_salida.txt`: **40/40 OK** (33 s).
- **Humo final** (escrito DESPUÉS de §7; `humo_salida.txt`, JSON en `datos/humo/M_NUEZ_SOC_s50195.json`): NUEZ_SOC 50195, T 200 000:
  **se extingue** (t_ext 151 109; cae de ~100 a 5 al cerrar el vivero), K 5.35; frac_ok 0.087, SI −0.221; 13 disparos, 9 copias; 15 s.
  El mismo mundo con canal OFF (§9a, práctica 3) persistió con K 49: las 9 copias cambiaron la historia y el establecimiento tras el
  vivero resultó una lotería (1 de 2 corridas con nueces persiste). **Riesgo declarado, sin tocar §7:** V2 (NUEZ_OFF y NUEZ_SOC
  persisten ≥ 3/5) puede caer y dejar la explora NO EVALUABLE; mi E1 (p 0.85) queda expuesta. No me quedan corridas (6/6) para
  recalibrar; si V2 cae, la lectura es "el mundo enriquecido está en el borde de lo vivible con vivero de 100 000", y el siguiente
  paso sería alargar el vivero (t_corte 250 000, como BLOQUES2 §6a) con semillas nuevas.
- Costo: una corrida que persiste ≈ 52 s a T 200 000 (práctica 3) → ≈ 130–170 s a T 500 000; extintas 15–40 s. 20 trabajos con pool 2:
  ≈ 15–25 min; ×2 por PC compartido: **≤ 50 min**.
- **Comando (sólo el coordinador), desde la raíz del repo:**
  `python experimentos/organelos/enriquecido/corre_enriquecido.py --explora --pool 2`
  (si se corta: el mismo con `--reanuda`; leer: `python experimentos/organelos/enriquecido/corre_enriquecido.py --lee explora`).
  Datos en `experimentos/organelos/enriquecido/datos/explora/` (M_*.json y VEREDICTO.json).

## 10. Enmiendas del auditor (LISTO CON CAMBIOS), firmadas ANTES de datos de la explora (29-sep-2026)
- **H-1 (letra):** pares válidos en P1/P2 (los dos brazos persisten y ≥ 20 intentos; ≥ 4 pares exigidos) y V2 también para DESF. Hecho en
  §8, en `corre_enriquecido.veredicto` y en el arnés (L): casos sintéticos de extinción del control (DESF 2/5 → NO EVALUABLE; un par con
  DESF extinto no cuenta; 3 pares válidos < 4 → P2 no se cumple; par con < 20 intentos no cuenta).
- **H-2 (si V2 cae):** la explora se lee SÓLO como descriptiva de persistencia por brazo (cuántas semillas persisten en SOC, OFF, DESF y
  REF, y K), sin veredicto sobre secuencia ni social. La contingencia ya fijada es repetir con **vivero más largo (t_corte 250 000),
  semillas nuevas y la misma letra**. **La p 0.85 de E1 quedó descalibrada por el humo final** (NUEZ_SOC 50195 extinto); E1 no se reescribe.
- **H-3 (reanuda):** con `--reanuda`, un `M_*.json` con `aborto` se REINTENTA (se borra y se corre de nuevo, desde el checkpoint si lo
  hay); uno sin aborto se salta. Arnés (L3).
- **H-4:** `.gitignore` local en esta carpeta: `__pycache__/`, `*.pyc`, `*.nbi`, `*.nbc`, `datos/*/ckpt/`, `*.pkl`, `*.pkl.tmp`,
  `*.json.tmp`, `datos/arnes/`.
- Arnés entero repetido: **46/46 OK** (`identidad_enriquecido_salida.txt`). El motor no cambió (09f1f2f4d85b2368).
