# PREREGISTRO de las dos SONDAS de ráfaga (1-oct-2026) — EXPLORATORIAS: nada se declara

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).
Escrito ANTES de leer números (el arnés de la sonda 1 ya pasó 12/12; el humo 1 corre mientras se escribe esto y no se ha mirado).
Origen: `investigacion_20261001/ENTREGA_2_planear_componer.md` (fichas 1 y 2). ERR libre: 179 (no se usa: no hay recalibración).

## SONDA 1 — piso y techo de un mundo con llave NO letal

- **Hipótesis:** existe un mundo donde la base vive sin llave y la llave todavía paga (hay espacio entre piso y techo).
- **Mecanismo y memoria nueva:** ninguno; es validez de mundo. El oráculo es una COTA escrita a mano (sabe que K es la llave y cuánto dura), no un candidato.
- **Instrumento y anclas:** `mundo_plus.py` (las 17 anclas de `mundo_tramo_c`, sha fijado, sin tocarlo; sólo cambia la clase del oasis) ·
  `construye_orac.py` (7 anclas sobre el texto de O1_LUGAR de `construye_p1`, sha fijado) · `corre_s1.py` (cada corrida ES `corre_v143.tarea`; fila de `corre_p1.fila`).
  Arnés: `corre_s1.py --identidad` (12 comprobaciones; lo apagado == `mundo_tramo_c` / O1_LUGAR, salida entera).
- **Mundo:** P1b (oasis 1, extra 0.8, pobre 0.5, dens 0.5, vista 20) + K (0, 0) a p_x 0.03, cerrojo 0. Sin llave: P1b tal cual. Con llave
  (K mordida por ese cuerpo hace ≤ d_plus = 600 pasos): el bocado A/C dentro paga +plus en las dos necesidades.
- **Brazos:** piso (O1_LUGAR) · techo (oráculo: K si no lleva llave y aguanta, luego oasis) · azar (va por K por moneda p 0.5 en bloques de 100 pasos, sin
  mirar la llave) · regalo (O1_LUGAR con la llave regalada: cota dura).
- **Medidas:** linajes que cruzan y establecidos (de 18, T 100k, 2 semillas), ganancia EFECTIVA por 1000 pasos de linaje (tras el tope 1.5 de la pista),
  y la parte efectiva del plus (contrafactual en los mismos niveles).
- **Regla de lectura (fijada antes):** ESPACIO SÍ si piso vivo (establecidos ≥ 12/18) Y cota dura − piso ≥ +4 cruces de 18 Y ganancia efectiva
  cota/piso ≥ 1.10. Si no, ESPACIO NO en ese mundo.
- **Predicción numérica (mía):**
  1. Mundo del encargo (extra 0.8 + plus 0.4): piso establecidos 12–17/18, cruzan 6–11/18. **ESPACIO NO**: los niveles saturan (un bocado dentro ya da
     +0.8/+0.8 y O1 muerde con nivel < 1.25; el tope es 1.5): plus efectivo / plus nominal ≤ 0.35; techo − piso entre −3 y +3 cruces; ganancia efectiva
     techo/piso entre 0.95 y 1.08.
  2. Parámetro que abre el espacio: **extra_sin** (lo que el oasis paga SIN llave) bajado a 0.4, con llave 0.8: piso establecidos ≥ 9/18 (vive, peor que P1b),
     regalo − piso ≥ +4 cruces; el oráculo captura ≥ la mitad de regalo − piso; azar queda entre piso y techo.
- **Control que puede fallar:** azar ≥ techo (apetito por K sin estado alcanza: entonces el mundo no exige secuencia y la medida de P9 tiene que ser por
  contraste con ventana corta, no por cruce); regalo ≈ piso (el mundo no paga).
- **Qué lo refuta:** piso muerto (establecidos < 9/18) refuta "la base vive"; regalo − piso < +4 en los dos mundos refuta "hay un parámetro barato que abre el espacio".
- **Trampas:** (3) K neutra que nadie come se acumula y tapa el mundo: se reporta mundo A+C y la fracción de K; el oráculo además LIMPIA K (cada mordida repone):
  parte de su ventaja puede ser limpieza, por eso el azar (misma limpieza, sin orden) y la cota regalo (sin limpieza). (4) el oasis se sortea por semilla.
  (1) y (2) no aplican (no hay canal social ni acierto).
- **Semillas nuevas:** humos 737200–737219 · arnés 737400.

## SONDA 2 — P8 (componer) fuera de la presión de supervivencia, con celda retenida

- **Hipótesis:** letra (E, aprendida sólo FUERA) y lugar (oasis, aprendido con A y C) aprendidos por separado deciden bien el PRIMER E dentro del oasis.
- **Mecanismo y memoria nueva:** COMPONE (el bono de lugar se suma también a letras mixtas; `construye_c.py:122-124`); memoria nueva: cero.
- **Instrumento y anclas:** `mundo_ret.py` (anclas de `mundo_tramo_c` + 1 ancla: la letra nueva nunca nace dentro del oasis; apagada == `mundo_tramo_c` bit a bit) ·
  `corre_s2.py`: (a) CRÍA O1_LUGAR (el mismo carro para los tres brazos) y captura, sin tocar el carro, la tabla por letra (suma, n) y la memoria de lugar
  (lugar, nl) del último cuerpo de cada linaje a precisión completa; (b) PREGUNTA: reconstruye cada brazo con `nace(memoria)` y llama `actua()` con observaciones
  sintéticas, sin `resultado()` y sin mundo. Los tres brazos leen LA MISMA memoria: comp (O1_LUGAR_COMP), lug (O1_LUGAR), compbar (O1_LUGAR_COMP_BAR: lee el antípoda).
- **Preguntas** (el cuerpo a un paso del objeto; rejilla 5×5 de niveles E, Ag ∈ {0.3, 0.5, 0.7, 0.9, 1.1}; 4 celdas dentro del oasis y sus 4 antípodas):
  condición LIMPIA = hay una A a la vista 10 celdas más allá (la limpieza de O1 queda apagada: medida principal) · condición SOLA = sólo el objeto (limpieza posible).
  Objetos: E dentro, E fuera (antípoda), A dentro, B dentro. Y la elección: A y E dentro a igual distancia (5 celdas a cada lado).
- **Medida:** por linaje, P(muerde E dentro) y P(muerde E fuera) sobre rejilla × celdas; D = dentro − fuera. Por brazo: medianas y fracción de linajes con D ≥ 0.6.
  Linajes válidos: conocen E (n[E] ≥ 1), recuerdan el oasis (algún bin del oasis con bono > 0.05) y nunca mordieron E dentro (física del mundo: 0 por construcción).
- **Regla de lectura:** COMPONE SÍ si, en la condición limpia, mediana D(comp) ≥ 0.6 en linajes válidos, D(lug) = 0 exacto, D(compbar) ≤ −0.3 y B dentro (comp) ≤ 0.2.
- **Predicción numérica (mía):** linajes válidos 30–50 de 54. D(comp) mediana 0.5–0.9, y ≥ 0.6 en 55–80 % de los válidos (falla donde el bono del bin en agua
  no supera 0.1: la tabla de A y C absorbe el extra y el bono queda chico); D(lug) = 0 exacto; D(compbar) ≤ −0.5. **B dentro en comp: 0.3–0.8 (falla la segunda
  puerta: el bono también vuelve "buena" a B)**. A dentro ≥ 0.9 en los tres. Elección A contra E: A en ≥ 0.8.
- **Control que puede fallar:** compbar empata con comp (bono difuso por todo el anillo); lug ≠ 0 (el instrumento no apagó la limpieza).
- **Qué lo refuta:** D(comp) mediana < 0.3, o compbar ≥ comp.
- **Trampas:** (2) acierto sin balancear: por eso D (dentro − fuera) y no la tasa dentro; (3) no hay mundo en la pregunta; (4) el oasis se sortea por semilla y
  las celdas de pregunta salen de la física de cada corrida; la celda (E, dentro) está retenida en la crianza (se verifica: mordidas de E dentro = 0).
- **Semillas nuevas:** crianza 737300–737305 (T 60 000, p_x 0.15) · arnés 737401.

## Adenda a la SONDA 1 (07:48, escrita con los humos 1–3 leídos y el humo 4 corriendo, sin mirarlo)

Los humos 1–3 dicen que el plus ENERGÉTICO no abre espacio donde la base vive (mi predicción 2, "extra_sin 0.4 abre", queda REFUTADA: regalo 7 contra piso 7).
Lectura: la ganancia efectiva está acotada por el gasto fijo (2.0 por 1000 pasos) y el tope 1.5; lo que sobra sólo puede ir a partos.
Humo 4, perilla nueva `adelanta` (apagada = bit a bit; arnés E6): con llave, el bocado A/C dentro adelanta 250 pasos la ventana de parto (rep_X 500) si ya corre.
Es un plus REPRODUCTIVO: no pasa por el tope ni por el gasto. Mundo: extra 0.8 siempre, plus energético 0, d 600, K p_x 0.03.
- **Predicción (mía):** piso como en el humo 1 (cruzan 6–10, establecidos 11–14); regalo − piso ≥ +4 cruces y partos regalo/piso ≥ 1.3;
  el oráculo oportunista captura menos de un tercio de regalo − piso (lleva llave en ~15 % de los bocados: K escasa a p_x 0.03 y vista 20).
- **Qué lo refuta:** regalo − piso < +4 cruces: ni pagando en partos el mundo separa; entonces el cruce no sirve de puerta para P9 en ningún mundo de esta familia.

## Adenda 2 a la SONDA 1 (08:01, con el humo 4 leído; humos 5–6 sin correr)

El humo 4 REFUTA mi predicción de la adenda 1: ni el plus reproductivo separa (regalo 6 cruces contra piso 8; partos 476 contra 449, razón 1.06).
Hipótesis nueva: los 9 linajes son CLONES que comparten un oasis y una oferta fija de comida; lo que uno gana lo pierde otro, y el número que cruza lo fija
la capacidad del oasis, no el pago. Si es así, el espacio sólo puede verse en PISTA MIXTA (oráculo y piso en el MISMO mundo, compitiendo).
Humos 5–6: `mixto` / `mixto2` (despachador pasivo; arnés X1–X2): los linajes de índice par (o impar, en `mixto2`) son el oráculo y el resto O1_LUGAR;
2 semillas × 2 paridades = 4 corridas por mundo; se suma por ROL. Humo 5: plus reproductivo (adelanta 250). Humo 6: plus energético del encargo (+0.4).
- **Predicción (mía):** humo 5: fracción que cruza techo − piso ≥ +0.20 (de 18 linajes por rol) y partos por linaje techo/piso ≥ 1.3. Humo 6: diferencia entre −0.10 y +0.15 (el tope se come el plus).
- **Control que puede fallar:** el oráculo también LIMPIA K y viaja más; si gana igual en el humo 6 (donde el plus casi no llega), la ventaja no es de la llave.
- **Qué lo refuta:** techo − piso < +0.10 en el humo 5: ni compitiendo paga la llave; el mundo con llave no letal no sirve para P9 con cruce ni en pista mixta.

## Adenda 3 a la SONDA 1 (08:07, con el humo 5 leído; humo 6 corriendo, humo 7 sin correr)

El humo 5 REFUTA mi predicción de la adenda 2: en pista mixta con plus reproductivo el oráculo cruza MENOS (9/18 contra 12/18), aunque pare más (26.7 contra 20.7 partos por linaje).
Humo 7 (último): el único punto con espacio por cruce fue extra_sin 0.2 (piso 3, regalo 7), con el piso medio muerto. Dos preguntas:
(a) ¿hay un punto intermedio? piso con extra_sin 0.3 (su cota regalo es la misma corrida de 0.4 y 0.2: 7 cruces, 14 establecidos);
(b) en extra_sin 0.2, ¿un oráculo K → oasis captura el espacio? techo y azar, mismas semillas 737200–201.
- **Predicción (mía):** (a) piso 0.3: cruzan 4–7, establecidos 8–12 (entre 0.2 y 0.4; no abre ≥ +4 con piso vivo). (b) el oráculo oportunista lleva llave en 15–30 % de los
  bocados: cruzan 3–5 (captura ≤ la mitad de los +4), ganancia efectiva 2.0–2.3; azar a ±1 cruce del techo (con d 600 el orden no importa).
- **Qué lo refuta:** techo@0.2 ≥ 7 cruces con azar ≤ 4: ahí sí habría mundo para P9 (el orden paga).
