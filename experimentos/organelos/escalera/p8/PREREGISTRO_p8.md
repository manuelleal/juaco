# PREREGISTRO P8 — "componer en celda retenida" (protocolo completo, 1-oct-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).
Escrito ANTES de correr el humo y de ver un solo número de COMP2 (sólo el arnés 20/20 y `nulo_p8.py`, que usa la sonda). DISEÑO, no selección.

## 1. Qué se afirma (y qué no)
En el mundo con oasis, en celda retenida: un linaje que aprendió la letra E sólo FUERA del oasis y el lugar sólo con A y C decide morder el PRIMER E
dentro del oasis, sin haberlo vivido nunca, y no lo muerde fuera. El mecanismo es una **suma cableada** (valor de la letra + bono del sitio) que
generaliza a un caso no vivido. No se afirma que "razona" ni que "compone conceptos"; no se mide supervivencia ni cruce (la celda está retenida: la
conducta no puede pagar en la crianza).

## 2. Sesgo declarado
Los umbrales se fijaron DESPUÉS de la sonda 2 (semillas 737300–737305, que NO entran): allí COMP sobre memoria de O1_LUGAR dio D por semilla
0.25, 0.25, 0.5, 0.5, 0.5, 0.625 (mediana 0.50; 6/6 > 0). La serie usa semillas nuevas y la letra es por código (`corre_p8.lee_letra`).
Diferencia con la sonda, declarada: aquí COMP se CRÍA como COMP (brazo propio); el instrumento exacto de la sonda queda como `comp_s` (descriptivo).
Linaje válido aquí = establecido + conoce E y A + 0 mordidas de E dentro (la sonda además pedía "recuerda el oasis"; se quita porque filtra por el mecanismo).

## 3. Mundo e instrumento (anclas y shas)
- Mundo: `sondas/mundo_ret.py` (sha 0b0d84552d176569; 18 anclas = las 17 de `mundo_tramo_c` + 1): P1b (oasis 1, extra 0.8, pobre 0.5, dens 0.5, vista 20)
  + E (+0.3, −0.1) a p_x 0.15 que nunca nace dentro del oasis. T 60 000, 9 linajes del mismo carro, fundador limpio.
- Pregunta: `sondas/corre_s2.py` (sha 6977e4869261f3da): `nace(memoria)` + `actua()` con observaciones sintéticas, sin `resultado()` ni mundo. Cuerpo a un paso
  del objeto; rejilla 5×5 de niveles {0.3 … 1.1}; 4 celdas dentro del oasis y sus antípodas; una A a la vista 10 celdas más allá (limpieza apagada).
  D del linaje = P(muerde E dentro) − P(muerde E fuera). D de la SEMILLA = mediana sobre sus linajes válidos (mínimo 3; si no, la semilla cuenta 0).
- Carros: `construye_p8.py` sobre el texto de O1_LUGAR_COMP de `construye_c` (shas fijados). Runner `corre_p8.py`. Arnés: `corre_p8.py --identidad` (20 comprobaciones).

## 4. Brazos
Crianza (20 semillas pareadas, cada brazo con SU memoria; nadie comparte memoria en la letra):
| brazo | carro | qué es |
|---|---|---|
| comp | O1_LUGAR_COMP | la composición de la ráfaga (el bono se suma a toda letra mixta) |
| lug | O1_LUGAR | sin composición |
| comp2 | O1_LUGAR_COMP2 | el candidato |

**COMP2 — qué cambia exactamente respecto de COMP (0 floats nuevos, 0 memoria nueva; arnés M5–M6):**
1. `LG2 = 1` (aprendizaje, una línea en `resultado`): una mordida en un bin que ya recuerda bono (algún componente > LG_MIN, leído después de aprender el lugar)
   NO actualiza la tabla por letra, si la letra ya es conocida. La tabla aprende sólo donde el sitio no da de más: tiende al valor de la letra fuera y deja
   de absorber el extra del oasis (en la sonda v_A = (0.67, 0.54) y el bono mediano en agua 0.065).
2. `COMPONE = 2` (compuerta, una línea en `_lg_v`): el bono se suma a una letra mixta sólo si la letra alimenta algo (algún componente > 0). Motivo, escrito
   antes de correr: con el bono entero, la suma sin compuerta volvería "buenas" a B y D dentro (B = (−0.4, 0) + (≈0.6, ≈0.6)). Es conocimiento puesto a mano
   y se declara como tal. La variante sin compuerta (`comp2sg`) se pregunta sobre la misma memoria y se reporta.
Con LG2 = 0 y COMPONE = 1 el carro ES O1_LUGAR_COMP bit a bit (arnés M2, M3, M8).

Preguntas descriptivas (no entran en la letra): `comp_s` (COMP sobre memoria de lug: la sonda), `comp2sg`, `lug2` (O1_LUGAR sobre memoria de comp2).

## 5. Controles que pueden ganar
- **Memoria de lugar PERMUTADA entre bins** (`comp_perm`, `comp2_perm`; media de 8 permutaciones por linaje, rng [semilla, linaje, 7]): la composición sin
  contenido de lugar. Debe dar D ≈ 0. (El antípoda se descarta: es espejo por construcción.)
- **Sin composición** (lug): D = 0 exacto en todo linaje válido. **Fuera general** (4 celdas fuera que no son antípodas): ≤ 0.05.
- **Segunda puerta:** B dentro rechazada (mordida ≤ 0.1) y, con A y E dentro a igual distancia y EN EL MISMO BIN, elige A (≥ 0.75; Enmienda 1).

## 6. La letra (por código; unidad = semilla; empates en contra; n = 20)
**NO SE LEE** (antes que todo) si falla alguna: V1 60 corridas sin aborto y coherentes · V2 celda retenida (0 mordidas de E dentro, composición de E dentro = 0,
re-sorteos > 0 en toda corrida) · V3 preguntar no cambia la memoria · V4 estado (carro, LG2, COMPONE, mundo, retenida) · V5 ≥ 17/20 semillas con ≥ 3 linajes
válidos en cada brazo de crianza.
Para cada candidato X ∈ {comp, comp2}, por separado:
- P1: D de la semilla > 0 en ≥ 15/20 · P2: mediana de D sobre las 20 semillas ≥ 0.40 (MODESTO: ≥ 0.25)
- P3: |mediana de D permutada| ≤ 0.10 · P4: sin composición D = 0 exacto · P5: fuera general ≤ 0.05 · P6: B dentro ≤ 0.10 · P7: elige A ≥ 0.75 en el MISMO bin, balanceada (Enmienda 1, sec. 11; antes ≥ 0.90 entre bins distintos)
  (P5–P7: mediana sobre semillas de la media por linajes válidos)
- **FUNCIONA** = P1 y P2 y P3–P7. **HAY ALGO MODESTO** = P1 y mediana ≥ 0.25 y P3–P7. Si no, **NO**.
Lectura separada, preregistrada: **COMP2 MEJORA** si D(comp2) > D(comp) en ≥ 14/20 semillas pareadas (estricto) Y mediana de la diferencia ≥ +0.20.
Réplica (737520–737539) sólo si la serie da FUNCIONA o MODESTO en algún candidato, o NO en el umbral (P1 o el pareado a ±1); mismo sha del runner.

## 7. Nulo, falso positivo y potencia (`nulo_p8.py`, salida en `nulo_p8_salida.txt`)
Nulo = memoria de lugar permutada, sobre la sonda (600 semillas-permutación): P(D de la semilla > 0) = 0.015; media −0.001; P(|D| > 0.1) = 0.037.
Falso positivo de P1 (≥ 15/20) bajo el nulo: 6e-24 (1e-13 con p0 × 5). Bajo el nulo, P(P1 y mediana ≥ 0.25) = 0.0000 en 20 000 simulaciones.
Potencia cruda si la serie se parece a la sonda (remuestreo de 6 semillas): FUNCIONA 0.90, al menos MODESTO 1.00. Ningún umbral es el valor del nulo (0).
Aviso: 0.40 queda a 0.10 de lo visto (0.50) y D por semilla sale en escalones de 0.125: el veredicto de COMP entre FUNCIONA y MODESTO es incierto.

## 8. Trampas (se reportan por código en `trampas`)
- (5a) Que la crianza de COMP2 difiera de la base de modo que explique D: cruzan, establecidos, mundo A+C, vida, mordidas, razón de pasos en el oasis por brazo,
  y pareado de cruce comp2 contra lug y comp. LG2 SÍ cambia la tabla en la crianza (valor de A y C más bajo): se espera diferencia; se mide, no se corrige.
- (5b) Que D dependa del nº de linajes válidos: correlación de rangos D de la semilla contra válidos, por brazo.
- (2) Acierto sin balancear: por eso D (dentro − fuera). (3) No hay mundo en la pregunta. (4) El oasis se sortea por semilla. (1) No aplica.
- Debilidad conocida del instrumento: en "A contra E" con niveles (1.1, 1.1) las dos ganancias saturan y el empate lo resuelve el orden del diccionario (A primero): 1 de 25 celdas.

## 9. Predicciones firmadas (antes de correr)
- **COMP:** k_pos 17–20/20; mediana de D 0.375–0.50; B dentro 0.00; elige A 1.00; permutada 0.00. Veredicto: FUNCIONA 0.55 · MODESTO 0.40 · NO 0.05.
- **COMP2:** CORRIJO mi predicción de la sonda (mediana ≥ 0.8) a **mediana 0.75 (rango 0.60–1.00)**: una de las 4 celdas de pregunta suele caer en un bin de
  borde con 1–4 celdas de oasis, que casi no se muerde. k_pos 19–20/20; B dentro 0.00 (por la compuerta); permutada |·| ≤ 0.05; fuera general 0.00.
  Veredicto FUNCIONA 0.75. **COMP2 MEJORA: sí** (diferencia mediana +0.25 a +0.40; ≥ 15/20), probabilidad 0.65.
- `comp2sg` (sin compuerta): B dentro mordida ≥ 0.3 (falla P6). `comp_s`: como la sonda (mediana 0.4–0.5). `lug2`: D = 0 exacto.
- Trampa 5a: comp ≈ lug en crianza (cruce a ±3 de 180, casi la misma corrida); comp2 establecidos dentro de ±15 % de lug.
- **Qué me refuta:** COMP2 mediana < 0.5 (la tabla sigue absorbiendo o LG2 rompe la crianza); permutada > 0.1 (el bono es difuso); comp2 no mejora a comp.

## 10. Costo y comandos
Medido en los humos 1 y 2 (un proceso, con otras series en la máquina): 58–92 s por corrida (media ~75 s, crianza + pregunta), arnés ~70 s. Serie: 60 corridas (20 × 3):
~75 min en un proceso, ~40 min con pool 2; serie + réplica ~80 min. La ruta con Pool NO se probó (un creador no corre Pool): `trabajo` es de nivel de módulo, como en `corre_p1`.
```
python experimentos/organelos/escalera/p8/corre_p8.py --serie   --pool 2      (cortada: agregar --reanuda)
python experimentos/organelos/escalera/p8/corre_p8.py --replica --pool 2
python experimentos/organelos/escalera/p8/corre_p8.py --lee <carpeta>
```
`--serie/--replica` exigen todo commiteado (preregistro, runner, constructor, nulo, `sondas/mundo_ret.py`, `sondas/corre_s2.py`, carros).
Semillas: serie 737500–737519 · réplica 737520–737539 · humo 737490–737491 · arnés 737402 (grep: 7375xx y 7374xx sin uso previo fuera de las sondas).

## 11. Enmienda 1 — ERR-179 (08:55, tras el humo 1 de `main`, semillas 737490–491 que no entran; ANTES de la serie y del humo 2)
**Qué pasó.** El humo 1 corrió de punta a punta (ERR-42 cumplido) y mostró que la puerta P7 heredada de la sonda (`S2.elige`: A a +5 y E a −5 del cuerpo)
pone las dos letras en BINS DISTINTOS. En COMP el bono es chico y A gana siempre (1.00); en COMP2 el bono es grande y ruidoso entre bins vecinos (EMA 0.5:
el último bocado manda), y el carro elige el bin con más bono aunque tenga la E: elige A 0.72 y 0.60. Eso mide el lugar, no la letra: el instrumento
confunde las dos cosas. También refuta mi lectura previa ("A gana por orden de diccionario en los empates").
**Criterio nuevo (por código, `corre_p8.elige_bin`):** A contra E dentro del oasis EN EL MISMO BIN (bins de 12 celdas enteros dentro del oasis; cuerpo en el
centro, una letra a +5 y la otra a −5: mismo bono para las dos) y BALANCEADA en lado y en orden de diccionario (las dos disposiciones): una preferencia de
lado o un empate dan 0.5. **P7: fracción que elige A ≥ 0.75** (nulo sin preferencia de letra = 0.50; margen 0.25; el 0.90 anterior no estaba calibrado para
una medida donde los empates por saturación cuentan 0.5). La medida vieja se sigue reportando como descriptiva ("entre bins distintos"). Arnés B1–B2.
**Lo que NO cambia:** D, P1–P6, validez, brazos, semillas de serie y réplica. Los números del humo 1 (n = 2, no cuentan) quedan en `humo_p8_1_salida.txt`:
D por semilla comp 0.0 y 0.25; comp2 0.75 y 0.75; permutadas ≈ 0; B dentro 0.00 con compuerta y 0.38 sin ella; mundo A+C comp2 8.2 contra lug 6.4.
**Predicción firmada para la P7 nueva:** COMP 1.00; COMP2 0.85–1.00 (empates por saturación en 0–6 de 25 celdas de la rejilla, que cuentan 0.5).
**Sesgo:** la enmienda se escribe después de ver P7 en 2 semillas de humo. Mis predicciones de la sec. 9 NO se tocan (la de COMP, mediana 0.375–0.50, ya
pinta mal en el humo: 0.0 y 0.25; queda firmada como está).

## Correcciones de la auditoría previa (1-oct-2026, antes del commit y de cualquier dato de serie; no cambian la letra, los umbrales, los brazos ni las semillas; mandan sobre el texto anterior donde lo contradigan)
- **H-1 (qué mide D).** D se mide con una A a la vista (condición L). NO mide "muerde E dentro y no la muerde fuera" a secas: con E sola (condición S, descriptiva, se imprime) el brazo sin composición ya muerde E 0.56 dentro y fuera, y comp2 en el humo 2 dio 0.936 dentro / 0.572 fuera. D mide "E le gana a una A visible dentro del oasis y no fuera". Además, en "dentro" la A de +10 puede caer en un bin con bono y en "fuera" no: el instrumento sintético no difiere sólo en el bin.
- **H-2 (qué está garantizado por el código y qué puede fallar).** Garantizado por construcción, y por tanto control del instrumento y no resultado: sin composición = 0 exacto (P4); B dentro = 0 en comp2 (P6: la compuerta se escribió para eso; sin compuerta da 0.43). Hecho empírico que puede fallar: (1) que la memoria de lugar aprendida sólo con A y C supere el −0.1 de E en ambos componentes en los bins del oasis y no fuera; (2) que con la memoria de lugar permutada D dé 0; (3) fuera general ≤ 0.05; (4) que ocurra en ≥ 15/20 semillas.
- **Afirmación máxima que sostiene un FUNCIONA:** "en el mundo con oasis, en celda retenida, con una suma cableada letra+bono y una compuerta cableada, un linaje que sólo vivió E fuera la muerde dentro del oasis aun con A a la vista, porque su memoria de lugar (aprendida sólo con A y C) tiene bono ahí; con la memoria de lugar permutada, no". NO sostiene: que aprendió o descubrió la composición, que la compuerta o LG2 se descubrieron, "razona", ni "no la muerde fuera" en general.
- **H-3 (ERR-179, efecto contrafáctico, regla 11).** Sin la enmienda (puerta vieja: A sobre E entre bins distintos, umbral 0.90) COMP2 = NO por P7: el humo 1 dio 0.72 y 0.60 y el humo 2 agrupa 0.73. La enmienda se acepta porque el mismo bin mide letra con el lugar constante, pero la medida vieja captura un efecto real que no se corrige: COMP2 elige E sobre A ~27 % de las veces cuando la E está en un bin con más bono. Todo veredicto de COMP2 se declara con "A sobre E sólo a igual lugar". El umbral 0.75 se fijó habiendo visto 0.978 (nulo 0.5 + 0.25).
- **H-4.** Semillas de humo: humo 1 = 737490–491, humo 2 = 737492–493.
- **H-5/H-6 (trampas obligatorias junto al veredicto, no entran en la letra).** vida_med, mundo A+C y rho(D, válidos) por brazo. En los humos la vida mediana de comp es ≈ 500 contra 1100–2100 de lug y comp2: un D bajo de comp puede venir de vida corta y no sólo del mecanismo. COMP2 deja más comida (A+C 7.9 contra 6.3).
- **H-8.** El falso positivo 6e-24 es del nulo de memoria permutada con semillas independientes, no de "sin composición". La potencia 0.90 se calculó con COMP sobre memoria de O1_LUGAR; **la potencia de COMP2 no está calculada**.
