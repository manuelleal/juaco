# PREREGISTRO — EXPLORATORIO — SENTIDOS CONTRA EL MURO (29-sep-2026, creador)

Misión: llegar a la AGI por este camino. Principio del director: que la selección construya el órgano, no nosotros.
**EXPLORATORIO** (5 semillas de prueba). Sólo decide si se escribe una serie. Escrito con el arnés PASADO y el humo (semillas de práctica)
corrido, ANTES de cualquier número del explora. Carpeta: `experimentos/organelos/sentidos_muro/` (sólo archivos nuevos; pista.py, juez.py,
pista_pob.py y los carros existentes sin tocar).

## 0. Lo que YA existía (declarado; cambia la pregunta que me encargaron)
El encargo pedía dar a la gramática BQ2 los sentidos (a) "¿hay algo bueno a la vista?" y (b) "reservas". **BQ2 ya los tiene:**
- sentido 6 con j = 1 = cercanía del objeto más cercano con píxel 1, que es 1 sólo en A y C: "algo bueno a la vista" por IDENTIDAD de letra (instinto);
- sentido 8 = reserva min(E, Ag); sentido 7 = la letra en foco ya fue mordida por el linaje.

Y la gramática BQ2 **ya contiene** una política que cruza la letra del muro: `prueba_forzada` de bloques_pista (dos reglas: "desconocida → boca −3"
y "reserva > 0.5 → boca +3") dio mayoría 3/3 y R0 real 0.957 en 59201–59203. Pero la selección nunca la encontró: bloq2, bloq2_pas y pob_sel
dan 0/45 reglas "prueba" y 17–21 linajes que cruzan de 45. **Diagnóstico:** no falta sentir; falta que la decisión esté a UN paso de mutación.
Esa política exige DOS reglas coordinadas, y cada una por separado no paga.

## 1. Hipótesis
Si un sentido nuevo pone la decisión "limpiar o probar sólo con reservas" a UNA regla de distancia, la selección por pasajes (la que encontró
el termostato ×2) la fija. Con ella, en la pista vieja cruzan más linajes que con la misma selección sin el sentido (bq2_pas) y que con el mismo
carro sin selección (bq3).

## 2. Mecanismo y memoria nueva: **cero**
Carro `V143_BQ3` = `V143_BQ2` (sha 183fb81cf6ad520c) por 4 anclas (`construye_sm.py`), con **perilla SENT3**:
- **sentido 9, "algo BUENO a la vista", aprendido y no por letra:** cercanía `1 − min(d, 20)/20` del objeto más cercano cuya letra el linaje
  SINTIÓ buena. Usa el criterio de TERMO: media dE ≥ 0 y dAg ≥ 0, y alguna > 0 (lee `_adS`, que ya existe desde v14.3). Usa la misma foto del
  anillo que el sentido 6, con el mismo retraso de una celda.
- **sentido 10, "riesgo de morder":** vale `1 − reserva` si la letra en foco NO es sentida buena (desconocida o mala) y 0 si lo es.
  Una sola regla "10 > θ → boca −w" dice: "con reservas bajas no pruebes ni limpies; con reservas altas, sí".
- SENT3 = 0 → NSEN 9 → **V143_BQ2 bit a bit, también con tasas de exploración** (arnés A). SENT3 = 1 → NSEN 11. No cambian los operadores
  ni las tasas (CFG = inicial 2, p_campo 0.10, p_dup 0.02, p_del 0.07, p_ins 0.05, banco 50), ni la herencia ni el banco.
- **Declarado:** con SENT3 = 1 el sorteo de sentidos consume el rng del carro con otro rango, así que bq3 y bq2 divergen en su azar.
- **Trampa 5, sentido a medida:** el sentido 10 está diseñado para que la política de O1 quepa en una regla. Diseñamos media pieza; la
  selección debe encontrar el signo, la acción, el umbral y mantenerla. Lo declaro y lo mide `forzada3`.

## 3. Brazos (prueba: pista vieja, juez, fundador limpio, ENMIENDA 5, T 100 000, semillas 59201–59205 = índices 1..5)
| brazo | qué es | papel |
|---|---|---|
| bq3_pas | V143_BQ3 + 10 pasajes de T 25 000; siembra del siguiente = unión de los bancos finales (sólo entra quien PARIÓ, `corre_bp.siembra_de`); la prueba arranca los bancos con la siembra final | CANDIDATO |
| bq2_pas | lo mismo con V143_BQ2 (sin sentidos 9/10), **mismas semillas de pasaje** | CONTROL que puede fallar (¿es el sentido?) |
| bq3 | V143_BQ3, una corrida, banco vacío | CONTROL que puede fallar (¿es la selección?) |
| forzada3 | V143_BQ3, tasas 0, todo cuerpo con UNA regla "riesgo > 0.5 → boca −3" | DIAGNÓSTICO (no decide): ¿el sentido contiene una política que cruza? |
| v143, termo, o1, bloq2 | JSON GUARDADOS (sha16 por archivo fijado en el runner; el arnés reproduce bloq2 s59201 T 100k BIT A BIT por este runner) | referencias pareadas y validez |

Semillas: pasaje p del índice i = 614000 + 10i + p (614010–614059). 614xxx no aparece como semilla en `.py` ni `.md` de PROYECTOS/JUACO:
grep del 29-sep; en `.json` sólo aparece como cifras de floats. Humo: 614900, 614991. Arnés: 614992.
**Declarado:** las semillas de prueba 59201–59205 ya se usaron y sus tasas base se conocen (cruzan de 45: o1 37, bloq2 21, termo 20,
pob_sel 17); las uso a propósito para parear con los JSON guardados. La siembra se entrena en 614xxx, nunca en 592xx.

## 4. Medida oficial
La letra del muro por linaje es `cruza_real` del juez, y cuenta **cuántos linajes cruzan (de 9) por semilla**. Mayoría = más de 4.5 de 9. R0 real
mediano y fundadores al lado. Mecanismo, descriptivo: fracción de listas de la siembra final y del banco final con la regla de riesgo
(sentido 10, `>`, boca, w < 0).

## 5. Predicciones (firmadas ANTES del explora; `lee()` las imprime con lo medido)
| # | predicción | p |
|---|---|---|
| S1 | forzada3: mayoría que cruza ≥ 3/5 | 0.50 |
| S2 | suma de cruzan bq3_pas en [18, 32] (de 45) | 0.60 |
| S3 | suma de cruzan bq2_pas en [14, 27] | 0.65 |
| S4 | suma de cruzan bq3 en [14, 27] | 0.60 |
| S5 | siembra final de bq3_pas con la regla de riesgo en ≥ 25 % de las listas, en ≥ 3/5 cadenas | 0.35 |
| S6 | mayoría bq3_pas ≥ 3/5 | 0.30 |
| S7 | veredicto NO | 0.62 |

Veredicto que espero: **NO 0.62 · MODESTO 0.28 · FUNCIONA 0.10**.

## 6. Puerta (por código: `corre_sentidos_muro.letra`; el arnés la prueba en 6 casos sintéticos)
- **FUNCIONA (pasa a serie):** se cumplen las tres:
  - mayoría bq3_pas ≥ 4/5;
  - bq3_pas > bq2_pas en cruzan en ≥ 4/5 semillas;
  - bq3_pas > bq3 en ≥ 4/5.
  Un empate no gana.
- **HAY ALGO MODESTO:** bq3_pas > bq2_pas en ≥ 3/5 **y** > bq3 en ≥ 3/5; **o** la suma de cruzan de bq3_pas ≥ max(bq2_pas, bq3) + 5.
- **NO:** cualquier otra cosa.
- **Validez** (si una falla: NO SE LEE):
  - 0 abortos y los 20 trabajos completos;
  - contabilidad coherente;
  - los 20 JSON de referencia con su sha16;
  - v143: mediana del R0 real en [0.40, 0.80];
  - o1: mayoría ≥ 4/5;
  - arnés PASA citando los shas ACTUALES del runner, de V143_BQ3 y de construye_sm (sin eso, `--explora` no arranca).

## 7. Qué lo refuta
- bq3_pas ≤ bq2_pas en ≥ 3/5 semillas y la suma no pasa de +5: el sentido nuevo no le da a la selección nada que la pista premie.
- Si forzada3 NO cruza (mayoría ≤ 2/5) con θ=0.5 y w=−3: no se concluye nada sobre el sentido 10 (es un solo punto de la gramática; el fallo puede ser del umbral). (Cambio por auditoría antes de datos, H-1.)
- Si bq3 ≈ bq3_pas > bq2_pas, lo que ayuda es el sentido, no la selección.
- Si la regla de riesgo es > 25 % de la siembra y aun así bq3_pas no gana, se fijó algo que no sirve en la prueba.

## 8. Cuatro trampas (+1)
1. **Canal simétrico.** bq3_pas y bq2_pas tienen las mismas semillas de pasaje, la misma transferencia, la misma prueba y las mismas tasas;
   sólo cambia SENT3. Los sentidos 9 y 10 leen `_adS` (la experiencia del propio linaje, que se borra con cada fundador limpio) y el anillo que
   la pista ya le da al carro. No abren un canal entre linajes. La siembra une los bancos de los 9 linajes: es igual en los dos brazos con pasajes.
2. **Acierto sin balancear.** Se cuentan linajes que cruzan, pareados por semilla contra controles con la misma maquinaria; las tasas base
   se conocen (sec. 3). Nada se lee en absoluto.
3. **Mundo que se come la comida.** La pista no cambia. El sentido 10 empuja a limpiar con reservas altas, y eso cambia el anillo (A+C
   disponible). No entra en la puerta; se declara.
4. **Sitios fijos.** Las letras tienen significado fijo en la pista (el sentido 6 ya permite el instinto por identidad). Los sentidos 9 y 10 no
   usan la identidad: leen lo sentido. La siembra se entrena en 614xxx y se mide en 592xx.
5. **Sentido a medida** (sec. 2): lo mide `forzada3`.

## 9. Costo y comando
- Humo, un proceso, 6 corridas, 50 000 pasos: 46 s, es decir ~0.93 ms por paso.
- Explora: 10 cadenas (250k + 100k) y 10 pruebas de 100k, ≈ 4.5 M pasos ≈ 4 200 s de CPU → **≈ 35–45 min con `--pool 2`** (la máquina
  corre tres líneas a la vez; el tope es 60 min).
- Comando (lo lanza el coordinador):
  `python experimentos/organelos/sentidos_muro/corre_sentidos_muro.py --explora --pool 2`
  (si se corta: el mismo comando con `--reanuda`).
- Lectura: la imprime el runner al final, o `--lee datos/explora_<fecha>`.

## 10. Opción no construida
Los sentidos 9 y 10 son 4 anclas sobre la maquinaria de reglas. Se podrían portar al carro con patas (`dinamita/carros/TPATAS.py`, brazo pc),
que confirma otro creador en `patas_muro/`. No lo construyo: primero hay que ver si solos le sirven a la selección.

## 11. Cambios antes de datos
- Arnés v1, (A) segunda línea: FALLA por un error del arnés, no del carro. Forzaba la regla de sentido 10 en BQ2, que no tiene ese sentido.
  Se reemplazó por la regla PRUEBA_O1 (sentidos 7 y 8, que están en los dos): OK. Se agregó el control que DEBE diferir (regla 10 en BQ2 ≠ en BQ3): OK.
- POOL_MAX 3 → 2, por ajuste del coordinador. Es la única diferencia entre el runner del humo (ace988ad52a0fcb3) y el final (4776b80e18733079).
  El arnés se volvió a correr con el runner final y PASA.


## 12. Cambios por auditoría antes de datos (29-sep)
- H-1: la sec. 7 ya no dice que un fallo de forzada3 explica de antemano un NO.
- H-2: S5 cuenta como "regla de riesgo" cualquier regla con sentido 10, comparación `>`, efecto sobre la boca y w < 0, **para cualquier θ** (`es_riesgo`, corre_sentidos_muro.py:164). Es descriptivo.
- H-3: tras la corrida, el coordinador comprueba a mano `bq.cfg` y `bq.forzada` de los JSON del explora (el runner no se edita para no cambiar su sha).
