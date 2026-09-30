# PREREGISTRO — EXPLORATORIO DIAGNÓSTICO — CONDICIONES / MUTACIÓN: ¿el muro de "no inventa combinaciones" es carga mutacional? (30-sep-2026, creador)

Misión: llegar a la AGI por este camino. **EXPLORATORIO DIAGNÓSTICO** (5 cadenas). No decide tronco: decide el siguiente paso.
Escrito con el arnés PASADO (`identidad_mut_salida.txt`) y **antes** del humo y de cualquier número de esta réplica.
Carpeta: `experimentos/organelos/condiciones/mutacion/` (sólo archivos nuevos). `moneda/corre_moneda.py` (sha `0441aa7bf5b94316`) se
IMPORTA y no se toca; pista, juez, corre_bp, sentidos_muro y el carro V143_BQ3 van con sha fijado (por `corre_moneda.verifica`).
ERR-158 ya está usado (entre_linajes). **ERR-159** = las enmiendas frente a moneda: la banda de cero pasa a [0.25, 0.75], PURGA ya no exige '<0.10' y entran las puertas nuevas carga_baja y tasas_actuan (sec. 6, advertencia 2; auditoría H-M1).

## 1. Hipótesis (junta Fable, genetista)
La frase "la selección afina perillas pero no inventa combinaciones" puede ser un **artefacto de carga mutacional**. En `moneda` la
pérdida por regla es ~0.11 por generación (p_del 0.07 + p_campo·(campos que sacan de la clase)): cerca del umbral de error (Eigen).
Con esa carga la regla regalada se desarma antes de que la selección la vea. Si se bajan **todas** las tasas ÷10, la regla que paga
debería **subir** frente a la neutra.

## 2. Diseño: `moneda` idéntica, con un solo cambio (las tasas)
Cadena = la de `moneda` (= `bq3_pas` de sentidos_muro con la siembra del pasaje 0 inyectada: 225 × [A] + 225 × [B], intercaladas).
10 pasajes de T 25 000; siembra siguiente = `corre_bp.siembra_de`. **Memoria nueva: cero. Mecanismo nuevo: ninguno.** Las tasas son
configuración del runner (`cfg` explícito en cada tarea; el carro no se toca).

| brazo | siembra inyectada | tasas | papel |
|---|---|---|---|
| **moneda** | A = `[10,0,1,0.5,0,−3]` (la fila de forzada3) + B | **CFG10** | CANDIDATO; prueba a 100k (descriptiva) |
| **neutra** | A0 = `[10,0,1,0.5,0,0]` + B | **CFG10** | CONTROL que puede fallar |
| **cero** | A0 + B | 0 | VALIDEZ (sólo deriva) |

**CFG10** = inicial 2, p_campo **0.01**, p_dup **0.002**, p_del **0.007**, p_ins **0.005**, banco 50 (fábrica: 0.10 / 0.02 / 0.07 / 0.05).
El arnés (A) mide el operador del carro: 20.3 % de hijos cambian a tasas de fábrica y 2.2 % a CFG10 (razón 0.109).

**Medida (la de moneda, sin cambios):** fracción de listas de la siembra con una regla de clase A (sentido 10, j 0, `>`, boca; cualquier
θ y w) a la salida de cada pasaje; **p9** = la siembra final. Nuevo y sólo descriptivo o de validez: **intacta** = fracción de listas de la
siembra que son EXACTAMENTE un genotipo inyectado (mide cuánto mutó); **listas mutadas** = suma de listas no inyectadas.

**Semillas NUEVAS** (grep 30-sep: `634xxx` sólo aparece como cifras de un float en un log de `reunion/`): pasaje p del índice i (1..5) =
**634100 + 10 i + p** (634110–634159), las mismas en los tres brazos (pareado). Humo: 634180–634181 y prueba 634191. Arnés: 634192.
**Prueba descriptiva de la cadena moneda: 59201–59205 a T 100 000** (no son nuevas, a propósito). Así queda pareada con la prueba de
`moneda` a tasas ×1 (16/45) y con forzada3 (23/45) y bq3_pas (13/45) guardados, todos con sha16 fijado. No entra en la letra.

## 3. Instrumento y anclas (arnés `identidad_mut.py`, salida pegada en `identidad_mut_salida.txt`: **ARNES: PASA**, 101 s)
- (K) shas de corre_moneda e identidad_moneda, y por `corre_moneda.verifica` los de sentidos_muro, corre_bp, V143_BQ3, pista y juez.
- (C) CFG10 = fábrica con cada tasa ÷10; inicial y banco iguales. CERO y las filas marcadas son las de corre_moneda.
- (I) La siembra inyectada es la de corre_moneda en los tres brazos.
- (F) **A tasas de fábrica este runner ES corre_moneda bit a bit.** Se prueba así:
  - `tarea` en los tres brazos, campo a campo;
  - `trabajo`: cadena de 2 pasajes más prueba, JSON por JSON;
  - reproducción del pasaje guardado `moneda i1 p0` (s 633110, T 25 000), igual en linajes, pista, R0_pista, tel, tel_termo y bq.
- (A) **Las tasas nuevas actúan.** El mismo pasaje a CFG10 difiere del guardado (intacta 1.0 frente a 0.9). El operador del carro cambia
  al 2.2 % de los hijos frente al 20.3 %. Con tasas 0, al 0 %.
- (E) Regla 14: la entrada se compara campo a campo contra `corre_bp.tarea('V143_BQ3', cfg explícito, siembra)`. La siembra actúa (44/44 fundadores salen del banco).
- (D) determinismo.
- (W) reintento de abortos y reanudación de una cadena.
- (X) el runner niega pool > 2.
- (L) la letra en 14 casos.
- (R) sha16 de las 15 pruebas de referencia y de `lectura_moneda.json`.

## 4. Predicciones (firmadas antes del humo; `lee()` las imprime contra lo medido)
Referencia a tasas ×1 (moneda, 29-sep): la mediana de p9 fue neutra 0.253, moneda 0.247 y cero 0.389 (media 0.353). moneda > neutra en 2/5.
Intacta en p9 a ×1: neutra 0.23–0.61. **Mi modelo:** a ×1 la mutación le quitó a la neutra ~0.10–0.14 frente a cero. A ÷10 le quita ~0.01,
así que la neutra ÷10 ≈ cero. La deriva por cadena es grande (cero de 0.17 a 0.47): con 5 cadenas, sólo un efecto grande de la moneda se verá.

| # | predicción | p |
|---|---|---|
| G1 | (genetista) neutra: mediana de la fracción A en p9 en [0.30, 0.45] | 0.55 (el genetista no dio p; la asigna el creador) |
| K1 | veredicto OTRA MONEDA | 0.65 |
| K2 | veredicto PAGA | 0.20 |
| K3 | veredicto PURGA | 0.10 |
| K4 | la diferencia de medianas en p9 entre neutra y cero es < 0.10 en valor absoluto (la carga desaparece) | 0.65 |
| K5 | intacta de la neutra en p9 (mediana) ≥ 0.85 | 0.75 |
| K6 | prueba de la moneda ÷10: suma de cruzan en [8, 24] de 45 | 0.60 |

Veredicto que espero: **OTRA MONEDA 0.65 · PAGA 0.20 · PURGA 0.10 · NO SE LEE 0.05.**

## 5. Control que puede fallar
La **neutra ÷10**: las mismas semillas, las mismas tasas, el mismo largo y el mismo acceso al banco. Sólo cambia w (0 frente a −3).
Si la moneda sube y la neutra también, no hay pago, y la letra lo exige **pareado**. **cero** comprueba que el instrumento no fabrica tendencia.

## 6. LA LETRA (por código: `corre_mut.letra`; el arnés la prueba en 14 casos). Son las tres lecturas del encargo.
- **PAGA:** la moneda en p9 es **estrictamente mayor** que la neutra en p9, pareado por cadena, en **≥ 4/5**. Lectura: la regla paga y el muro era carga.
- **PURGA:** se cumplen las dos:
  - la moneda es **≤ 0.5 × la neutra** en p9, pareado, en ≥ 4/5;
  - la **mediana de la neutra en p9 es ≥ 0.10** (heredado de moneda H-1a).
- **OTRA MONEDA:** cualquier otro resultado válido (moneda ≈ neutra). Sigue la hipótesis "paga en otra moneda": el muro no era la carga.
- **Validez** (si una falla: NO SE LEE):
  - 0 abortos, las 15 cadenas y las 5 pruebas completas;
  - la fracción de entrada es 0.5 en todas;
  - cero: sólo genotipos inyectados en 5/5;
  - cero: media de p9 en **[0.25, 0.75]**;
  - **carga_baja:** la intacta de la neutra en p9 tiene mediana ≥ 0.80 (si no, las tasas ÷10 no bajaron la carga y la réplica no pregunta lo que dice);
  - **tasas_actúan:** hay ≥ 1 lista mutada en las cadenas ÷10;
  - las 15 referencias y la lectura de moneda con su sha16;
  - el arnés PASA con los shas actuales.
- Descriptivos que no entran en la letra:
  - la cuenta de "moneda − neutra ≥ 0.05";
  - la mediana de la diferencia;
  - las medianas de moneda, neutra y cero;
  - la prueba a 100k frente a moneda ×1, forzada3 y bq3_pas.

**Advertencias declaradas antes de datos:**
1. **Falso positivo de PAGA bajo la nula:** si moneda y neutra son intercambiables, P(≥ 4/5 estrictamente mayor) = 6/32 ≈ **0.19**.
   PAGA es una **señal para replicar**, no un hallazgo. El descriptivo "con margen 0.05" sirve para leerla.
2. **Cambios frente a la letra de moneda (ERR-159):**
   - (a) la banda de cero pasa de [0.30, 0.70] a **[0.25, 0.75]**, porque el cero de moneda dio una media de 0.353 con cadenas de 0.17 a 0.47: la deriva sola casi la saca de la banda;
   - (b) se agregan carga_baja y tasas_actúan;
   - (c) PURGA ya no exige "moneda < 0.10 en ≥ 4/5": el encargo la define sólo por la razón con la neutra.
   Los tres cambios van bajo **ERR-159**: se cambió la letra de un instrumento heredado, antes de datos.

## 7. Qué decide y qué lo refuta
- **PAGA** → la carga mutacional tapaba la selección. Siguiente:
  - réplica en semillas nuevas;
  - bajar tasas en `o1_evo`, `bloques_pista` y `sentidos_muro` antes de volver a concluir "no inventa";
  - la frase queda **en suspenso**.
- **OTRA MONEDA** → a tasas bajas la regla que cruza a mano sigue siendo invisible para el pasaje. La carga no era el muro. Siguiente: el pasaje en la moneda del muro (siembra ponderada por hijos a 100k).
- **PURGA** → el pasaje la saca activamente cuando ya no se desarma sola. Refuerza "paga en otra moneda".
- Con OTRA MONEDA o PURGA en una corrida válida: **no se ve un efecto grande de bajar la carga** (con 5 cadenas y la deriva medida, un efecto chico no es visible; no se escribe "la hipótesis cae"). Un **3/5 a favor de moneda** (±1 del umbral de PAGA) **dispara réplica** (regla 12) antes de cualquier lectura. Si la neutra ÷10 queda ≈ cero (K4) y aun así la moneda no se separa, la carga no explica el muro de esta regla.

**Riesgo de NO SE LEE (declarado; auditoría H-M3):**
- tasas_actuan: casi nulo (el explora tiene ~100 salidas de pasaje a ÷10);
- carga_baja: ~3 %;
- cero_banda: ~5–10 %, casi todo por el borde inferior (la deriva de cero en moneda fue hacia abajo: media 0.353).

## 8. Cuatro trampas
1. **Canal simétrico:**
   - A y B tienen el mismo largo y el mismo consumo de rng;
   - moneda y neutra comparten tasas y semillas;
   - la etiqueta j es muda (arnés N de moneda, heredado: la entrada es la misma, arnés F).
2. **Acierto sin balancear:** todo parte de 0.5 exacto y se lee **pareado** contra la neutra. La tasa nula de PAGA (0.19) está declarada.
3. **Mundo que se come la comida:** A y B conviven en la misma pista. La aptitud depende de la frecuencia (régimen de mezcla 50/50, como en moneda).
4. **Sitios fijos:** las letras tienen significado fijo. Los pasajes son nuevos (6341xx). La prueba reusa 592xx a propósito, sólo como descriptivo pareado.

## 9. Costo y comando
- Humo, un proceso: 6 corridas y 135 000 pasos.
- Explora: 4.25 M pasos. moneda con pool 2 tardó 2 200 s: **≈ 37 min**.
- Comando (lo lanza el coordinador):
  `python experimentos/organelos/condiciones/mutacion/corre_mut.py --explora --pool 2`
- Si se corta: el mismo comando con `--reanuda`.
- Lectura: `--lee datos/explora_<fecha>`.

## 10. Mini-prueba (humo; un proceso; semillas 634180–634181 y prueba 634191; corrida DESPUÉS de firmar las secciones 1–9; no cuenta)
Hubo 6 corridas y 135 000 pasos en 139 s (≈ 1.03 ms por paso). Carpeta `datos/humo_20260930_170849`. Arnés PASA con los shas actuales.

| brazo | fracción A: entrada → p0 → p1 | intacta | listas mutadas | vivos con A | arrastre ≥ | partos |
|---|---|---|---|---|---|---|
| moneda ÷10 | 0.50 → 0.487 → 0.531 | 1.0, 1.0 | 0 | 0.51 → 0.60 | 0.72, 0.72 | 128, 128 |
| neutra ÷10 | 0.50 → 0.469 → 0.513 | 1.0, 1.0 | 0 | 0.47 → 0.60 | 0.71, 0.69 | 132, 138 |
| cero (1 pasaje) | 0.50 → 0.560 | 1.0 | 0 | 0.69 | 0.67 | 148 |

La prueba de 10k da 0/9 (T corta; no dice nada). El humo sale **NO SE LEE**, porque `tasas_actuan` es falso: 0 listas mutadas en 2 pasajes.
Eso es esperable. En el banco sólo entran padres, y cada padre pare ~15 veces, así que las listas de la siembra son copias de pocos padres.
El arnés (A) muestra que a tasas de fábrica un pasaje deja 10 % de listas mutadas (≈ 45 copias de pocos eventos). A ÷10 son ≈ 0.4 eventos
por pasaje, y en 2 pasajes 0 es lo esperable. En el explora habrá ~100 salidas de pasaje ÷10, así que `tasas_actuan` debería cumplirse.
Lo que sí enseña el humo, y lo declaro: **a ÷10 la cadena es casi una cadena sin mutación.** El diagnóstico pregunta, en la práctica,
"¿la selección por pasajes enriquece la regla regalada si nada la desarma?". **No cambio ni la letra ni las predicciones.**

## 11. Cambios por auditoría antes de datos (30-sep; auditor: LISTO CON CAMBIOS; ningún dato del explora existía)
Sólo cambia el texto. `corre_mut.py` e `identidad_mut.py` **no se tocaron**: sus shas siguen siendo los que cita `identidad_mut_salida.txt`.
- **H-M1:** ERR-158 ya está usado (entre_linajes). **ERR-159** = las enmiendas frente a moneda (banda de cero [0.25, 0.75], PURGA sin '<0.10', puertas carga_baja y tasas_actuan). Se anota en la cabecera y en la sec. 6, advertencia 2.
- **H-M2:** "la hipótesis del genetista cae con OTRA MONEDA" pasa a "no se ve un efecto grande de bajar la carga". Un 3/5 a favor de moneda (±1 del umbral de PAGA) dispara réplica (regla 12). Está en la sec. 7.
- **H-M3:** se declara el riesgo de NO SE LEE por cada puerta: tasas_actuan casi nulo; carga_baja ~3 %; cero_banda ~5–10 %, casi unilateral por el borde inferior. Está en la sec. 7.
- Las predicciones G1 y K1–K6 y la letra por código **no cambian**. El humo (sec. 10) no se repitió.
