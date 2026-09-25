# PREREGISTRO — organelos/cruce: ¿el bicho real cruza R0 real ≥ 0.90 en la pista de la carrera POR SELECCIÓN NATURAL? (Opus C, 24-sep-2026)

Misión: llegar a la AGI por este camino; el método manda sobre el cómo. Escrito **antes** de la serie y después del arnés 30/30 y de
tres humos de práctica (una semilla cada uno, sin valor; §8). Nada commiteado; lo integra el coordinador.

## 1. Hipótesis
El v14.3 en la pista (V143: v14.2 + FILTRO con META + boca TD; R0 real 0.536 / 0.63 en la serie y la réplica de `tronco_v14_3`) sabe
qué es bueno y qué es malo, pero no conecta **cómo está ahora** (reserva, la otra necesidad, ventana de parto, edad, hijos en cola)
con **lo que hace** (morder, a qué ir, parir). Si ese cableado se le da como **genes que nacen apagados** y la **única** selección es
la de la pista (el que vive y pare llena la cola de su linaje y el banco de padres), la cría encuentra un cableado que, **leído
congelado** en carreras nuevas, sube el R0 real por la letra de la carrera, le gana a la deriva (AZAR) y a v14.3 fijo, y se cae si
el cableado lee un estado **desfasado** (subida_n9: O3 cruza porque decide con su estado presente).

## 2. Mecanismo mínimo y memoria nueva
- **Cuerpo:** `carros/CRUCE.py`, construido por anclas desde `tronco_v14_3/carros_v143/V143.py` (sha `2a03048a7f1525e5`). **No se
  toca el cerebro:** con el genoma en 0 ninguna línea nueva corre, y es V143 **bit a bit** (arnés 2a, 2b). N de subida_n7 es inerte
  en la pista porque todas las letras tienen masa 3 (arnés 9c). Por eso v14.3 (v14.2 + N) es aquí el V143 de la pista.
- **Genoma = 36 enteros en [−4, 4], todos en 0 al empezar.** Seis señales internas presentes: s = (1, min(E,Ag)/1.5,
  max(E,Ag)/1.5, ventana de parto recorrida, edad/2000, hijos en cola/4). Tres decisiones que el cuerpo ya tiene:
  - **BOCA** (18 genes = 3 contextos × 6 señales): logit de morder += Σ g·s, con los genes del contexto de la letra que pisa:
    bueno, malo o neutro. El contexto es cómo valora el propio organismo la letra con sus dos filas, la misma lectura que usa el
    FILTRO.
  - **PATAS** (12 genes): objetivo = argmin(distancia − 8·[(g_act·s)·valor en la fila activa + (g_otra·s)·valor en la otra
    fila]). Con los genes en 0 es el más cercano.
  - **PARTO** (6 genes): pare si g·s ≥ 0 (con los genes en 0, siempre).
- **Memoria nueva: CERO en el cerebro.** El genoma no aprende en vida; se hereda. El control DESFASADO guarda las últimas 2000
  señales del linaje (sólo en ese brazo). **Constantes nuevas:** PASO_BOCA 1, PASO_PATA 8, escalas de las señales, p_mut 0.03,
  banco 200, 8 sombras, cría 200 000, lectura 100 000.
- **Por qué no hay regla de O1 ni de O3:** el genoma es un mapa lineal completo de seis señales genéricas en las decisiones que V143
  ya tiene. Nace en 0 y muta ±1 con la misma probabilidad en todos los signos. No aparece ningún umbral de O1 ni de O3 (MARGEN 0.25,
  PRUEBA 0.5, PISO 0.2, COLA_TERM 4). Tampoco hay huecos entre cuerpos, penalización por vecinos, rareza de letras, «no hay nada
  útil» ni muerte programada. Los contextos usan las filas aprendidas del organismo, no la tabla verdadera (arnés 0d). O1 y O3
  **caben** en esta base, pero igual que caben sus contrarios (§6).

## 3. Instrumento y anclas
- **Motor:** `motor_cruce.py`, por anclas desde `carrera_escuderias/pista.py` (`9f47c65e438e0ff4`). Con `cruce=None` es la pista
  **bit a bit**, incluido el rng del mundo (arnés 1). El juez `juez.py` (`6a68f640a7832f12`) sólo se lee.
- **Cría** (semilla s, T = 200 000; declarada como **vivero**): error de copia en cada parto (cada gen ±1 con p = 0.03, rng propio
  [s, i, 16, k]). Si un linaje se extingue, el fundador (instancia nueva) lleva un genoma del banco (los últimos 200 genomas de
  PADRES en un parto), mutado. **Corte en t = 200 000:** el banco se congela.
  - **AZAR:** el genoma de todo cuerpo nuevo sale al azar del banco de genomas NUEVOS, mutado (regla de `motor_eco3`). El genoma
    nunca influye en su propia copia.
  - **MUT0:** p_mut 0.
  - **Sombras:** 8 por cuerpo; mutan igual, viajan por la misma genealogía y nunca se expresan.
- **Lectura** (después del corte nadie repone nada del banco): una carrera **nueva**, semilla s + 500 000, T = 100 000, 9 linajes,
  **letra de la carrera** (ENMIENDA 5 y juez.resumen_linaje). Cada linaje lleva UN genoma de la muestra del banco ([s, 23, k]; 9 sin
  reemplazo). Los hijos lo copian sin error. El fundador que pone la pista es una instancia **nueva**, sin memoria, con el genotipo
  de su linaje (como el fundador de O1 es una instancia nueva del código O1; arnés 4a). Los nacidos de la lectura son «los nacidos
  después del corte».
- **Anclas de lectura** (si alguna falla, NO SE LEE):
  - v14.3 fijo con R0 real mediano en [0.40, 0.75];
  - O1 ≥ 0.85;
  - placebo VIDA contra VIDA_P entre 5 y 15 de 20;
  - lectura mut0 == lectura v143 en la física, 20/20;
  - ≤ 2 tareas con error.
- **Regla 14:** la lectura v143 == `corre_v143.tarea('V143')` campo a campo (arnés 2b).
- **nube-9:** toda tarea atrapa `SystemExit` y devuelve un registro de error (arnés 9a). ERR-60 no se acerca: menos de 10⁴ cuerpos
  por linaje.

| brazo de lectura | genomas | qué prueba |
|---|---|---|
| **vida** | 9 del banco de VIDA | **el candidato** |
| vida_p | otros 9 del mismo banco | placebo: calibra el juez |
| azar | 9 del banco de AZAR | mutación sin selección |
| mut0 | 9 del banco de MUT0 (todo 0) | sin mutación (== v143; instrumento) |
| v143 | v14.3 fijo | la línea de base |
| **desf** | los mismos 9 de vida, con el cableado leyendo las 6 señales de un paso pasado al azar (últimos 2000 del linaje) | **el control que puede fallar** |
| o1 | O1 | techo escrito por un LLM; sólo referencia |

**Cuatro trampas:**
- **Canal simétrico:** no hay canal; nadie escribe en la pizarra, y se cuenta.
- **Acierto sin balancear:** no se mide acierto; se mide R0 por linaje, pareado por semilla, con placebo.
- **Mundo que se come la comida:** se reporta la fracción de pasos sin nada bueno en el mundo. Si la selección apaga la limpieza,
  el mundo se tapa (exploratorio i2) y eso se ve.
- **Sitios fijos:** la lectura corre en otra semilla del mundo, y el genoma no codifica posiciones.

## 4. Pregunta y letra (la aplica `corre_cruce.veredicto`, por serie; el bloque exige serie Y réplica, y si no coinciden vale el menor)
- **F1:** VIDA con R0 real mediano (mediana por semilla de los 9 linajes; mediana de las 20) **≥ 0.90** **y** gana la ENMIENDA 5
  (mayoría de linajes con R0 real ≥ 0.90, 0 fundadores tras 10 000 y ≥ 5 muertes, en ≥ 15/20 semillas).
- **F2:** VIDA > AZAR en ≥ 15/20 semillas pareadas. **F3:** VIDA > V143 en ≥ 15/20. **F4:** VIDA > DESF en ≥ 15/20.
- **FUNCIONA** = F1, F2, F3 y F4.
- **HAY ALGO MODESTO** en cualquiera de estos dos casos:
  - F1, F2 y F3 sin F4 (cruza, pero no se puede decir que lo haga por leer su estado);
  - no F1, pero F2 y F3 con una diferencia mediana VIDA − V143 ≥ 0.05.
- **NO** = lo demás. Bajo la nula, P(≥ 15/20) = 0.021 por comparación, y P(el placebo sale de [5, 15]) = 0.012.
- **Qué eligió la selección (descriptivo, no decide):**
  - Por gen, en cuántas semillas la media del banco de VIDA queda por encima o por debajo de sus 8 sombras. Bajo la nula es 1/9
    por semilla; ≥ 10/20 tiene P = 2·10⁻⁵ por celda. AZAR hace de guardia de falsos positivos.
  - El parecido con O1/O3: cuántas semillas dan el signo que O1/O3 tendrían en esta base (tabla PARECIDO_O del corredor, fijada
    aquí): boca_bueno_reserva −, boca_malo_otra +, boca_neutro_sesgo −, boca_neutro_reserva +, pata_act_sesgo +,
    boca_bueno_cola −, boca_malo_cola +.

## 5. Predicciones firmadas (medianas de 20 semillas; rango del 80 %)
| # | predicción | p |
|---|---|---|
| A1 | v14.3 fijo, R0 real en [0.40, 0.75] (ancla) | 0.85 |
| A2 | O1 ≥ 0.85 (ancla) | 0.90 |
| A3 | placebo VIDA contra VIDA_P dentro de [5, 15] | 0.95 |
| P1 | VIDA, R0 real **0.50–0.72** (puntual ~0.60) | 0.80 |
| P2 | **F1: VIDA ≥ 0.90 y gana la ENMIENDA 5** | **0.05** |
| P3 | F3: VIDA > V143 en ≥ 15/20 | 0.25 |
| P4 | F2: VIDA > AZAR en ≥ 15/20 | 0.55 |
| P5 | AZAR < V143 (mediana pareada < 0): la deriva estropea | 0.70 |
| P6 | F4: DESF < VIDA en ≥ 15/20 | 0.15 |
| P7 | cría: ≥ 1 gen de VIDA fuera de sus sombras en ≥ 10/20 semillas; AZAR ninguno | 0.55 |
| P8 | si hay gen elegido, es de BOCA en contexto malo o neutro (limpiar o contenerse), no de PARTO | 0.60 |
| P9 | ≥ 3 de los 7 signos de PARECIDO_O con ≥ 8/20 semillas en el signo de O1/O3 | 0.20 |

- **Veredicto por serie:** FUNCIONA 0.04 · HAY ALGO MODESTO 0.22 · NO 0.66 · NO SE LEE 0.08.
- **Bloque (serie + réplica):** FUNCIONA 0.03 · MODESTO 0.15 · NO 0.72 · NO SE LEE 0.10.
- **Lectura honesta:** espero NO. En 200 000 pasos, la cría hace ~800–1 000 partos y ~2 000–4 000 refundaciones por semilla, con 36
  genes. El humo largo (§8) no mostró ventaja a los 100 000.

## 6. Control que puede fallar, y qué refuta
- **DESF** (los mismos genomas, las 6 señales de un paso pasado): si VIDA mejora y DESF no cae (F4 falla), lo que la selección
  encontró **no** es leer el estado presente: sesgos constantes o señales lentas como la edad. Eso refuta la hipótesis de trabajo,
  aunque VIDA cruce.
- **Refuta la hipótesis:** VIDA ≤ V143 en ≥ 10/20, o VIDA ≈ AZAR. Querría decir que la selección natural de la pista, en 200 000
  pasos, no encuentra un cableado de estado que transfiera a una carrera nueva.
- **Refuta mi lectura pesimista:** F1.

## 7. Semillas NUEVAS (grep en todos los worktrees de `PROYECTOS/JUACO`: 0 usos; las 24001–24099 las usa el exploratorio de la nube)
- Práctica, humo y arnés: **24401–24420**.
- Serie: **24601–24620**. Réplica: **24701–24720**.
- Las lecturas usan la semilla + 500 000: **524601–524620** y **524701–524720**, sin uso.
- El corredor se niega a usar otras semillas.

## 8. Mini-prueba de un proceso (sin valor; semillas de práctica)
- **Arnés `identidad_cruce.py`: RESULTADO 30/30** (157 s; `identidad_cruce_salida.txt`). Shas:
  - `corre_cruce.py` `0d10b5e3ac033e81`, `construye_cruce.py` `172f67cb1e28678c`, `identidad_cruce.py` `bf227b9427a7f480`;
  - `motor_cruce.py` `6cfff5c04fdc2c8f`, `carros/CRUCE.py` `63ac38bac2d0bbcd`.
- **Humo 1 (diseño VIEJO, lectura en ventana continua;** `cruce_humo_s24401_T20000_tc10000_20260924_132430`). **Encontró el fallo
  de diseño de §9:** tras el corte, los linajes atascados vuelven a v14.3.
- **Humo final** (`cruce_humo_s24405_tc30000_tl20000_final_20260924_135019_resumen.json`, sha `1aa488358d82936f`, 140 s, 6
  corridas, 140 000 pasos):
  - **Cría VIDA:** 687 mutaciones, 109 partos, 523 refundados del banco. El 83 % del banco lleva algún gen ≠ 0. Distancia
    hijo-padre [29, 44, 22, 11, 2, 1].
  - **Cría AZAR:** distancia hijo-padre centrada en 6–11.
  - **Lectura** (T 20 000, una semilla): vida 0.60 · desf 0.50 · azar 0.035 · v143 0.45.
  - **El cableado cambia la conducta:** boca_dif 141, pata_dif 1 575 y 44 vetos de parto en AZAR.
- **Humo largo** (`..._s24406_tc100000_tl50000_largo_...`, 248 s, 200 000 pasos): cría VIDA de 100 000 con 2 594 mutaciones, 417
  partos y 1 978 refundados; lectura (T 50 000) vida 0.233 contra v143 0.250. boca_malo_otra sube sobre sus sombras (1 semilla).
  Es lo que me hace esperar NO.

## 9. Desviaciones declaradas (antes de la serie)
- **Primer diseño retirado tras el humo 1.** Tras el corte, el fundador volvía al genoma 0 y la lectura era una ventana continua.
  Eso hacía la comparación injusta con O1, cuyo fundador limpio es una instancia nueva del mismo código. Además, en los linajes ya
  establecidos el R0 de ventana es ≈ d/(d+1) (ERR-102) y deja a v14.3 fijo cerca de 0.9. Lo reemplacé por cría + lectura con la
  letra de la carrera, antes de mirar ninguna serie.
- **Patas rediseñadas tras el arnés.** Con un bono por contexto cambiaban el objetivo en 12 de 54 000 decisiones: el FILTRO ya
  quita lo malo. Ahora son una ganancia sobre el valor propio de la letra (6 370 de 54 000).
- **Falla del arnés 5c, declarada.** Escribí «≥ 90 % de los partos con 0–2 genes distintos». Con p = 0.03 × 42 genes, el esperado
  es 0.87: el umbral estaba mal calculado. Pasó a «distancia media = p_mut × NG ± 50 %».
- **ERR-124 (coordinador, 24-sep ~14:20, ANTES de la serie; auditoría juaco-auditor: LISTO CON CORRECCIONES).** Las tres
  desviaciones de arriba cambian la forma o un umbral del criterio después de ver un humo o el arnés. Por la regla 11 llevan ERR
  aunque no haya serie; quedan numeradas aquí como ERR-124 (a) diseño de cría + lectura, (b) patas y (c) umbral del arnés 5c.
  Además va (d), el H-2 del auditor: el ancla "mut0 == v143" exige ahora las 20 semillas de lectura (`len(comunes) == ns_lee`
  en `corre_cruce.py`), no la intersección. Con eso `corre_cruce.py` cambia de sha (el de §8 era `0d10b5e3ac033e81`). El arnés se
  vuelve a correr antes de la serie y manda su salida.

## 10. Comandos (sólo el coordinador) y costo
```
python experimentos/organelos/cruce/identidad_cruce.py            # RESULTADO: 30/30 antes de nada (~4 min)
python experimentos/organelos/cruce/corre_cruce.py --serie --desde 24601 --n 20 --pool 6
python experimentos/organelos/cruce/corre_cruce.py --serie --desde 24701 --n 20 --pool 6 --con <..._resumen.json de la serie>
```
- **Costo medido** en un proceso: cría ≈ 1.0–1.25 s por 1 000 pasos; lectura v14.3 ≈ 1.0–1.2 s; O1 ≈ 2.1 s.
- **Por serie:**
  - 60 crías × ~225 s = 13 500 s;
  - 120 lecturas × ~115 s = 13 800 s;
  - 20 O1 × ~210 s = 4 200 s.
  - En total ≈ **8.7 h de CPU ≈ 1.5–2 h de pared con Pool 6**. La réplica cuesta lo mismo.
