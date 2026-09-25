# PREREGISTRO — muro, SEGUNDO INTENTO: GLOTU + PATAS (creador, 25-sep-2026, escrito ~16:55, ANTES del humo2 y antes de ver el control)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo.

**Tiro largo, igual que el primero.** Espero NO (p 0.72).

## 0. Qué es y de dónde sale
- **Candidato:** `V143_GLOTUPATAS`, v14.3 con dos piezas locales, las dos nacidas inertes:
  - **GLOTU** (boca), la del primer intento: no morder lo que sólo sube la necesidad MÁS llena cuando esa ya está en `rep_umbral` o encima;
  - **PATAS** (patas): con META (hay a la vista algo con valor > 0 en la fila activa, la misma lectura del FILTRO de v14.3), el objetivo
    es el más cercano de ESOS, lo que sirve a la necesidad que hoy más falta. Sin meta, v14.3 tal cual.
- **Memoria nueva: cero. Constantes a mano: ninguna.** Ni MARGEN ni PRUEBA ni el hueco ni la penalización por el otro cuerpo de O1.
- **Sale del exploratorio de hoy** (37901–37905, T 100 000, `PREREGISTRO_muro.md` §8, no es dato):
  - GLOTU + PATAS le ganó a V143 en 4/5, con +0.030 (0.688, 0.816, 0.789, 0.875, 0.750);
  - GLOTU sola, 3/5 y +0.016; PATAS sola, 1/5 y −0.020.

## 1. La regla de "una pieza" se rompe A PROPÓSITO (justificación)
- **El puenteo** (`comite2/puenteo/HALLAZGOS.md`, `lee_puenteo.py`, 4 semillas 36001–36004, exploratorio) muestra que en V143 la brecha
  está en DOS decisiones de acción distintas: a qué objeto ir (patas) y si morder lo bueno que hay bajo el cuerpo (boca).
  - Cada una, en su versión O1, cierra la brecha sola: patas 0.949 (4/4); boca_buena 0.907 (4/4); V143 0.651; O1 0.935.
  - La memoria (0.136) y la limpieza (0.209) hunden.
- GLOTU actúa sólo en la boca y PATAS sólo en las patas. El arnés verifica que el veto de la boca no cambia el objetivo de las patas.
- **Lo que se pregunta:** ¿las traducciones genéricas de esas dos decisiones, juntas, cruzan?
- **Lo que NO se puede declarar si gana:** cuál de las dos pesa. Para eso está el control (§3): desfasa la pieza nueva.

## 2. Lo que dice el puenteo contra esta combinación (declarado antes de correr)
**El puenteo NO contradice la DIRECCIÓN, pero sí contradice la DOSIS.**
- Las piezas de O1, solas, suben +0.25 a +0.31. Mis traducciones solas suben +0.016 (GLOTU) y −0.02 (PATAS).
- **Mis traducciones no capturan lo que hace fuertes a las piezas de O1.** Las diferencias:
  - **PATAS.** Sin meta sigue yendo a lo más cercano, malo incluido, que es justo lo que el puenteo dice que falta arreglar ("el cuerpo de
    V143 se pone encima de lo malo"). Además ignora la competencia con otros cuerpos, y en s37908 es físicamente == V143 hasta T 3000.
  - **GLOTU.** Veta sólo la comida de la necesidad más llena ya sobre el umbral; O1 no come lo bueno bajo 1.25 si no le sirve. Y no tiene
    neofobia con reserva.
  - Acercarlas más a O1 sería copiar sus umbrales, y eso está prohibido.
- **Por eso espero NO.** Si la serie da NO, la lectura correcta es "las traducciones genéricas se quedan cortas", no "patas y boca no importan".

## 3. Brazos, semillas, costo
- **Brazos:**
  - `v143`: la base;
  - `glotupatas`: el CANDIDATO;
  - `glotupatasdesf`: el CONTROL;
  - `o1`: techo y ancla.
- **El CONTROL que PUEDE fallar:** `V143_GLOTUPATASDESF` es GLOTU más PATAS AL REVÉS (con meta, el objetivo es el más cercano que sirve a
  la OTRA necesidad; si no hay ninguno, v14.3).
  - Desfasa la pieza nueva y deja idéntica la boca.
  - Elegí este y no GLOTUINV + PATAS porque GLOTUINV ya se mide en la serie 1 y en el exploratorio da 0.000: con él, P3 no podría fallar.
  - Este sí puede cruzar si las patas no importan.
- **Semillas nuevas:** serie 37101–37120; réplica 37121–37140. No chocan con la serie 1 (37001–37040) ni con la práctica
  (37901–37919: humo2 37911–37912, arnés2 37913–37914).
- **Costo:** 80 corridas por serie, 35–45 min con Pool 6; la réplica igual.

## 4. Instrumento
- `construye_muro2.py` (642cd37565bc14ee) genera SÓLO `V143_GLOTUPATASDESF` (d82a7bb5bdf821b4).
  - Importa `construye_muro.construye`, las mismas nueve anclas desde V143.py (2a03048a7f1525e5).
  - El candidato `V143_GLOTUPATAS` (dec2d8ceb004e541) sale de `construye_muro.py` (ad607c6ad4f9ced9), sin tocar.
- `corre_muro2.py` IMPORTA `corre_muro.py` (503b531ea1213c59, el de la serie 1, sin tocar) y cambia EN MEMORIA sólo brazos, candidato,
  control, semillas, humo y carpeta (`datos/muro2`). También agrega a `verifica()` el carro nuevo y las identidades cortas.
  - Corrida, letra, resumen, pareados, nube-9, `--reanuda` y ERR-115 son los de corre_muro.
- `identidad_muro2.py`: **66/66** (`identidad_muro2_salida.txt`). Verifica, entre otras cosas, que corre_muro, recién importado, conserva
  la configuración de la serie 1.

## 5. Predicciones firmadas (antes del humo2 y del exploratorio del control)
| # | predicción | rango | p |
|---|---|---|---|
| A1 | V143: mediana del R0 real | [0.45, 0.78] | 0.85 |
| A2 | O1 cruza | 18–20/20 | 0.95 |
| Q1 | GLOTU+PATAS: mediana del R0 real | [0.60, 0.85] | 0.70 |
| Q2 | GLOTU+PATAS contra V143 pareado | gana 10–15/20, dif [−0.02, +0.10] | 0.65 |
| Q3 | GLOTU+PATAS: semillas con mayoría que cruza | 0–5/20 | 0.85 |
| Q4 | Control ≈ candidato: \|dif mediana\| < 0.05; el candidato le gana en 8–13/20 | | 0.60 |
| Q5 | Control: semillas con mayoría que cruza | 0–5/20 | 0.85 |
| V | NO / HAY ALGO MODESTO / FUNCIONA / NO SE LEE | | 0.72 / 0.10 / 0.03 / 0.15 |

## 6. LA LETRA: la MISMA que la serie 1 (`corre_muro.lee_serie`)
- **Validez:** V1 completa; V2 O1 gana; V3 V143 en [0.40, 0.80]; V4 la pieza actúa en candidato y control (`veto_glot` o `patas_meta` > 0).
- **P1:** el candidato cruza, ≥ 15/20 semillas con mayoría de linajes con `cruza_real`.
- **P2:** le gana a V143 pareado en ≥ 15/20.
- **P3:** el control NO cruza.
- **FUNCIONA:** todo. **HAY ALGO MODESTO:** P2, más dif mediana ≥ 0.10, más ganarle al control en > 10/20. **NO:** lo demás.
- **Bloque:** vale el menor. NO SE LEE manda.

## 7. Nulos declarados (regla 15)
- N1: candidato ≈ V143 (lo más probable).
- N2: candidato ≈ control. Las patas no aportan; lo que haya es GLOTU.
- N3: el candidato gana ≥ 15/20 con dif < 0.10. Es NO por la letra.
- N4: el control cruza y el candidato no, o los dos cruzan. P3 cae; se reporta sin declarar.
- **Qué lo refuta:** P2 < 15/20, en serie o en réplica.

## 8. Comandos (el coordinador)
```
python experimentos/organelos/muro/construye_muro2.py --verifica
python experimentos/organelos/muro/identidad_muro2.py                                     # 66/66, ~2 min
python experimentos/organelos/muro/corre_muro2.py --serie --desde 37101 --n 20 --pool 6
python experimentos/organelos/muro/corre_muro2.py --serie --desde 37121 --n 20 --pool 6     # replica
python experimentos/organelos/muro/corre_muro2.py --bloque <resumen serie>,<resumen replica>
```

## ADENDA (16:57, DESPUÉS de firmar: §0–§8 tenían sha 4098ff690c556ee5). No cambia la letra ni las predicciones.
- **Humo2** (1 proceso, 6 corridas, T 20 000, 376 s; `humo2_salida.txt`, `datos/muro2/humo/`):
  - regla 14 OK; identidades cortas OK (candidato y control con perillas en 0 == V143);
  - shas de corre_muro y construye_muro intactos; V4 True;
  - GLOTU+PATAS le gana a V143 2/2 (+0.05); el control 0.29 (1 semilla); no se lee.
- **Exploratorio del control** (37901–37905, T 100 000; corrido en paralelo a la firma):
  - GLOTU + PATASDESF: 0.596, 0.743, 0.724, 0.792, 0.575; le gana a V143 2/5 (−0.036);
  - **el candidato le gana al control 5/5, con dif mediana ≈ +0.07.**
  - Eso apunta a que **Q4 (control ≈ candidato) será refutada**: las patas "a lo que sirve a la activa" sí aportan algo contra su
    versión desfasada, aunque poco contra V143. Lo dejo escrito sin tocar Q4.
