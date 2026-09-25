# PREREGISTRO — OHNO SOBRE BASE VIVA: ¿la selección MEJORA el órgano ganador (filtra0) duplicándolo y dejando divergir la copia? (24-sep-2026, Opus A del equipo organelos; antes de cualquier serie)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/organelos/ohno/`. Principio del director (24-sep noche): **la evolución
arranca desde lo más evolucionado que tengamos.** Viene de GRAMÁTICA (serie 21011–21030 = NO; commit 48f99b8): desde un slot al azar,
la selección no encontró el órgano que el diseño fijo ya da (FIJO:filtra0 persiste 20/20 con R0 0.94; VIDA 8/20 con 0.59).

## 0. Instrumento
- **Copias BYTE A BYTE** de `gramatica/` (`construye_ohno.py --verifica`):

| archivo | sha |
|---|---|
| `motor_gramatica.py` | 6b65dc5e32093424 |
| `carros/FAMB_GRAM_ECO.py` | 2cee0a8510c997b9 |
| `gramatica_def.py` | c58086e103d030d9 |
| `conducta.py` | 9a2f1226fe27a514 |

  OHNO no necesita código nuevo en el motor: el mundo pobre es el argumento `r_rep` del quimiostato (P7) y los fundadores con
  filtra0 son un valor de `eco['gramatica']`. Todo lo nuevo está en `corre_ohno.py`.
- **Arnés `identidad_ohno.py`** (N/N en `identidad_ohno_salida.txt`):
  - (O1) con la mutación de la gramática apagada, VIDA == FIJO:filtra0 bit a bit;
  - (O2) con fundadores al azar y quimiostato 0.03, corre_ohno == corre_gramatica (en subprocesos);
  - (W) el quimiostato llega al motor;
  - piezas de la duplicación: (D1) una copia idéntica es neutra, (D2) una copia que diverge cambia el mundo y el original sigue
    trabajando, (D3) en el mundo aparecen copias divergidas con el original intacto;
  - (N9) nube-9 atrapado; (V) la letra; (R) banderas.

## 1. Pregunta y nombre honesto
Con selección natural sola tras el corte, **¿aparece un órgano de 2 o más slots (o un slot cambiado), conductualmente distinto de
filtra0 según `conducta.py`, que le GANE a filtra0 fijo?**
- «La selección MEJORA el órgano ganador» se declara solo si VIDA le gana a FIJO:filtra0 pareado (G1, G2) con un órgano no diseñado (G3).
- «... con un duplicado que diverge (Ohno)» exige además P-OHNO.
- Prohibido: «evoluciona», «inventa», «cultura».

## 2. Brazos, semillas, errores de copia (DECLARADOS)
- **Brazos** (MUT0 = FIJO):
  - **VIDA:** los 30 fundadores con filtra0 = nacer/sin0/hijo/copiar EXPRESADO en el slot 1; errores de copia y selección.
  - **FIJO:filtra0:** sin errores de copia de la gramática.
  - **AZAR:** desde filtra0, deriva pura; todo cuerpo nuevo copia una entrada al azar del banco.
  - En los tres hay mutación numérica de los mismos 18 genes (p 0.05, σ 0.15) y **8 sombras** de gramática por cuerpo.
- **Errores de copia** (los de GRAMÁTICA, sin cambio):
  - cambio de campo p 0.05 por slot y campo;
  - **duplicación p 0.02** por copia (en tándem, la copia con origen 1);
  - **borrado p 0.02** por copia (el vacío es absorbente);
  - tope 4 slots; alfabeto sin «olvidar».
  - Mecánicamente, original y copia sufren los mismos errores. Que el original se conserve lo decide la selección (es la hipótesis
    de Ohno), no el operador. Arnés (D1)–(D3).
- **Semillas NUEVAS** (grep: 25000–25999 sin usos):

| uso | semillas |
|---|---|
| humo | 25001 |
| arnés | 25002–25003 |
| **serie** | **25011–25030** |
| **réplica** | **25031–25050** |
| calibración (un proceso, declaradas) | 25901–25918 |
| prueba del Pool | 25991–25992 |

## 3. El mundo: CALIBRADO antes de la serie (riesgo principal: el techo)
- En w30 de ECO (`r_rep` 0.03), filtra0 fijo persiste 20/20 con R0 0.94: no hay margen para ganarle.
- Objetivo del coordinador: filtra0 fijo persiste 8–14/20 o tiene R0 entre 0.6 y 0.85.
- Palanca: el quimiostato (`r_rep`; objetos por paso = 30·`r_rep`). «Más veneno» exigiría cambiar el motor (las letras salen
  uniformes) y se descartó.
- **T 80 000, corte 40 000, margen de R0 15 000** (recortado de 120 000/60 000 por el costo en la nube, §8).
- **Calibración** (FIJO:filtra0, un proceso, `--calibra`; datos en `datos/calibra_rrep*/`):

| `r_rep` | semillas | persisten | R0 de nacidos tras el corte | lectura |
|---|---|---|---|---|
| 0.020 | 25901–25906 | 6/6 | 0.87–1.03 (mediana 0.95) | **TECHO** |
| 0.006 | 25907–25910 | 3/4 | 1.11, 0.99, 1.09 y 0 (extinta en 41 920) | |
| 0.004 | 25911–25914 | 0/4 | — | **INVIABLE**: todas mueren entre 40 593 y 41 829 |
| 0.005 | 25915–25918 | 3/4 | 1.32, 1.23, 1.09 y — (extinta en 40 621) | |

- **Lo que enseñó la calibración** (dato; cambia la lectura):
  - Tras el corte, una población que persiste queda en **R0 ≈ 1** con cualquier `r_rep` viable: el quimiostato fija la densidad.
    El R0 de 0.6–0.85 no se alcanza bajando la comida. **Lo que se calibra es la persistencia.**
  - En el mundo pobre casi no hay partos antes del corte (7 nacimientos en 40 000 pasos a 0.006, contra ~500 a 0.02): 30 cuerpos
    vacían el mundo y el vivero solo recicla fundadores. Al corte la población cae a 1–5 cuerpos. O se extingue ahí (el cuello de
    botella) o se rehace hasta 8–15 con R0 ≈ 1.
  - Por eso, **en este mundo la selección de la gramática ocurre casi toda DESPUÉS del corte, en unos 240 nacimientos por
    semilla**. Es poco material para Ohno; declarado como riesgo (§7).

## 3b. Elección del mundo
- **Regla**, escrita mientras corría 0.005 y antes de verlo: se elige el `r_rep` calibrado cuya persistencia medida quede más cerca
  del 55 % (el centro de 8–14/20); en empate, el más rico; si 0.005 da 0/4 o 4/4, queda 0.006.
- 0.005 y 0.006 dieron 3/4 cada uno (empate), así que **el mundo de OHNO es `r_rep` = 0.006** (0.18 objetos por paso, contra 0.9 en el w30 de ECO). Queda en `corre_ohno.R_REP`.
- Juntando 0.005 y 0.006 da 6/8 (75 %): el centro estimado queda ARRIBA del rango pedido (40–70 %). No se recalibra: las guardias
  TECHO (≥ 18/20) e INVIABLE (≤ 2/20) deciden en la serie.
- El cuello de botella es empinado: de 0/4 a 0.004 se pasa a 3/4 a 0.005.

## 4. Medidas
Todas sobre VIDA contra FIJO:filtra0, pareadas por semilla. R0 = media de hijos de los nacidos en [corte, T − 15 000]; sin cohorte = 0.
- **G1 (la medida que manda):** R0 de VIDA > R0 de FIJO (estricto) en **≥ 15/20**. Nula: intercambiables, con empates 0–0 que
  cuentan en contra; P(≥ 15/20) ≤ 0.021.
- **G2:** persistencia en T de VIDA ≥ la de FIJO (conteos).
- **G3:** en las semillas de VIDA que persisten, la conducta MODAL del banco final no es igual a ningún diseñado (nulo, ensena,
  filtra0), en **≥ 10/20**.
- **P-OHNO (descriptivo con umbral):** la modal de VIDA tiene ≥ 2 slots activos, y uno nació por duplicación (origen 1) con una
  conducta de un slot que no es la de ningún diseñado ni la de los otros slots. La gramática sin ese slot tiene otra conducta, y la
  entera no es filtra0. Umbral: **≥ 5/20**. También se informa, por semilla, la fracción del banco final con genomas OHNO en el real
  contra la media de sus 8 sombras.
- Descriptivas: AZAR contra FIJO en R0, persistencia por brazo y `max_nac_linaje`.

## 5. La letra (`corre_ohno.veredicto`), por ventana
- **NO EVALUABLE:**
  - ventana incompleta, alguna corrida abortada (nube-9) o bloqueados > 0;
  - **TECHO:** FIJO:filtra0 persiste ≥ 18/20 con mediana de R0 ≥ 0.9;
  - **INVIABLE:** FIJO persiste ≤ 2/20.
- **FUNCIONA — LA SELECCIÓN MEJORA EL ÓRGANO GANADOR CON UN DUPLICADO QUE DIVERGE (Ohno):** G1, G2, G3 y P-OHNO.
- **FUNCIONA — ... CON UN ÓRGANO NO DISEÑADO:** G1, G2 y G3.
- **HAY ALGO MODESTO:** G1 y G2 sin G3; o bien P-OHNO sin perder (VIDA < FIJO en menos de 15/20).
- **NO:** otro caso.
- El bloque exige serie y réplica con el mismo veredicto; si no, vale el menor. La regla 12 aplica (a ±1 del umbral → réplica nueva).

## 6. Predicciones firmadas
**Revisión declarada** (20:45, después de ver 0.005 y antes de cualquier serie): la persistencia de FIJO pasa de 7–16 a 10–18,
P(techo) de 0.05 a 0.15, y el veredicto se reparte de nuevo. La versión anterior estaba escrita con 0.004 y 0.006 vistos.
| cantidad | rango | probabilidad |
|---|---|---|
| FIJO:filtra0 persiste en la serie | 10–18 /20 | 0.75 (P(techo) 0.15; P(inviable) 0.02) |
| G1 VIDA > FIJO en R0 — **la que puede fallar** | 4–12 /20 | P(≥ 15) = 0.05 |
| VIDA < FIJO en R0 | 4–12 /20 | — |
| persistencia VIDA − FIJO | −4 a +3 | — |
| G3 modal no diseñada | 0–4 /20 | P(≥ 10) = 0.04 |
| P-OHNO | 0–2 /20 | P(≥ 5) = 0.03 |
| fracción OHNO real > sombras | 3–12 /20 | — |
| AZAR > FIJO en R0 | 3–10 /20 | — |
| **veredicto por ventana** | FUNCIONA-Ohno 0.02 · FUNCIONA-no diseñado 0.03 · MODESTO 0.08 · **NO 0.67** · NO EVALUABLE 0.20 (techo 0.15) | — |

Por qué predigo NO:
- El mundo que saca a filtra0 del techo lo hace con un cuello de botella al corte, y ahí la persistencia es mayormente suerte.
- Antes del corte casi no hay partos, así que VIDA llega al corte con su banco casi igual a FIJO.
- Después quedan unos 240 nacimientos: con p_dup 0.02, unas 5 duplicaciones por semilla, y la mayoría se pierde por deriva.
- La carga de errores (~18 % por slot y parto) juega contra VIDA.

## 7. Riesgos declarados (las cuatro trampas y otros)
1. **Techo y cuello de botella:** la persistencia depende del azar del cuello de botella del corte. Por eso se pareó por semilla (la
   misma semilla da el mismo mundo inicial y los mismos fundadores en VIDA y FIJO hasta que la gramática diverge).
2. **Canal simétrico:** una copia que diverge hacia «vecino» beneficia a otros linajes. Tras el corte suele quedar uno o dos linajes,
   así que casi todo vecino es pariente.
3. **Acierto sin balancear:** no hay tasas de acierto; las comparaciones son pareadas.
4. **Mundo que se come la comida:** ES la palanca (quimiostato pobre), declarada y calibrada.
5. **Sitios fijos:** no hay.
6. **Poco material para Ohno** (§3); T recortado a 80 000 por costo (§8).
7. La calibración usó 4–6 semillas por nivel: la persistencia real de FIJO en la serie puede caer fuera de 8–14/20. Para eso están
   las guardias TECHO/INVIABLE, sin recalibrar después.

## 8. Costo y comandos (ver INFORME.md)
Medido en la calibración (PC, con otros procesos corriendo): 155–222 s por corrida a T 80 000 (unos 190 s de media a 0.005–0.006).
- Por ventana: 60 corridas ≈ 3.2 h de CPU, **≈ 1.1 h con Pool 3**.
- Serie + réplica + arnés + prueba del Pool ≈ **2.4 h con Pool 3** si un núcleo de la nube rinde como el del PC.

## 9. ERR (candidato) de este paquete
- **ERR-126** (instrumento, 24-sep 20:35–20:44): la primera corrida de `identidad_ohno.py` dio 8/10. En el mundo pobre, a T 10 000,
  hay ~3 nacimientos, así que (D2) y (D3) no ejercitaban la duplicación: es la trampa de ERR-120 otra vez.
  - Arreglo: las piezas (D1)–(D3) corren con el quimiostato de ECO (mismo código, cientos de partos). Se agregan (O1b), VIDA ==
    FIJO pasado el corte en el mundo pobre, y (O1c), lo mismo con 0.03.
  - La segunda corrida dio 11/12: (O1b) daba igualdad bit a bit, pero con 9 partos contra un umbral puesto a ojo de 20. Se bajó
    a ≥ 5 y se declara.
  - Nada de esto toca la física ni la letra.
