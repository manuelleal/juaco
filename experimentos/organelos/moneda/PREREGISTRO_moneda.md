# PREREGISTRO — DIAGNÓSTICO EXPLORATORIO — LA MONEDA (29-sep-2026, creador)

Misión: llegar a la AGI por este camino. **EXPLORATORIO** (5 cadenas). No decide tronco: decide el siguiente paso.
Escrito con el arnés PASADO y **antes** del humo y de cualquier número del explora. Carpeta: `experimentos/organelos/moneda/`
(sólo archivos nuevos). Pista, juez, corre_bp, sentidos_muro y sus carros se importan con sha fijado; no se tocan.

## 1. Hipótesis (junta Fable, investigador 1)
La selección por pasajes (siembra = bancos finales a 25k) no sólo no **encuentra** la regla de riesgo de `forzada3`
("riesgo (sentido 10) > 0.5 → boca −3"; en sentidos_muro: 0 % de la siembra final en 5/5). Además la **purga**, aunque
esa regla cruce a 100k (forzada3: 23 de 45 cruzan, mayoría 3/5). La razón propuesta: la regla paga en la moneda de la letra
(establecerse, pocos fundadores a 100k) y no en la del pasaje (partos: sólo entra al banco quien pare).
**Dato previo, no es de esta prueba:** en los JSON guardados a 100k, forzada3 suma 1 728 descendientes, bq3 2 477 y termo 2 675.
Tiene menos partos y más cruces.

## 2. Diseño: la cadena bq3_pas, con un solo cambio (la siembra inyectada del pasaje 0)
Cadena = `bq3_pas` de sentidos_muro. Carro `V143_BQ3` (sha dd527e3c627e77fb), `CFG` = inicial 2, p_campo 0.10, p_dup 0.02,
p_del 0.07, p_ins 0.05, banco 50. Son 10 pasajes de T 25 000. La siembra siguiente es `corre_bp.siembra_de` (unión de los 9 bancos finales).
**Memoria nueva: cero. Mecanismo nuevo: ninguno.** Sólo cambia la siembra del pasaje 0 (450 listas de una regla, intercaladas):

| brazo | siembra inyectada | papel |
|---|---|---|
| **moneda** | 225 × `[10,0,1,0.5,0,−3]` (A = LA fila de forzada3) + 225 × `[10,5,1,0.5,0,0]` (B) | CANDIDATO; además prueba a 100k |
| **neutra** | 225 × `[10,0,1,0.5,0,0]` (A0 = la misma fila con w 0) + 225 × B | CONTROL que puede fallar (mutación + deriva) |
| **cero** | A0 + B como en neutra, **tasas 0** | VALIDEZ (sólo deriva) |

**Cambio declarado frente al encargo, antes de datos: "listas vacías" → B.** Una lista vacía **nunca entra al banco**
(`_bq_banco`: `if not R: return`, y `siembra_de` exige `if R`). Así, la mitad vacía desaparece de la siembra por construcción,
sin selección. El arnés (V) lo mide: 50 % `[]` + 50 % `[B]` dan una salida de 210 listas y 0 vacías. La comparación
quedaría regalada; es la trampa 1. B es la misma fila con **w 0** y **j 5**. Para el sentido 10, j **no se lee** (`_bq_s3`),
así que funciona como una **etiqueta muda**. El arnés (N) prueba que `[B]` = `[A0]` = genoma vacío = V143_TERMO, bit a bit, con
tasas 0. A y B tienen el mismo largo, la misma exposición a la mutación y el mismo acceso al banco. Sólo difieren en w.

**Medida (igual en los tres brazos).** Es la fracción de listas de la siembra con una regla de **clase A** (sentido 10, j 0, `>`,
boca; cualquier θ y cualquier w), a la **salida** de cada pasaje p0..p9. **p9** = la siembra que entra a la prueba. La entrada
vale 0.5 exacto (arnés I). Descriptivos: la clase A con w < 0, los "vivos con A" (muestras del cuerpo vivo cada 5k), los partos
por pasaje y el **arrastre**. El arrastre es la cota inferior de las listas de la siembra que no pasaron por ningún parto: Σ max(0, 50 − partos)/listas.
**Aviso medido antes de datos:** en sentidos_muro cada linaje pare 5–25 veces por pasaje. Con banco 50, ~70 % de la siembra
se **arrastra sin selección**, y la cota más fuerte posible a p9 es 0.5·0.7¹⁰ ≈ 0.014.

Semillas NUEVAS (grep del 29-sep: 6331xx no aparece en `.py/.md/.txt` de PROYECTOS/JUACO): el pasaje p de la cadena i (1..5) usa
**633100 + 10 i + p** (633110–633159), **las mismas en los tres brazos** (pareado). Prueba de la cadena moneda: pista vieja,
T 100 000, **59201–59205** (índice i), pareada con los JSON guardados `forzada3_s592xx` y `bq3_pas_s592xx` de sentidos_muro
(sha16 fijado en el runner). Humo: 633180–633181 y prueba 633191. Arnés: 633192.

## 3. Instrumento y anclas
`corre_moneda.tarea` ES `sentidos_muro.corre_sentidos_muro.tarea(seed, 'bq3', T, siembra)`, con cfg CERO en el brazo cero
(= `corre_bp.tarea`). Arnés: `identidad_moneda.py`, cuya salida se pega en `identidad_moneda_salida.txt`. Comprueba lo siguiente:
- (K) shas;
- (I) la siembra inyectada es la declarada, y los bancos de prepara salen de ella;
- (N) la etiqueta es muda y la neutra es nula;
- (Z) con tasas 0, la etiqueta es invisible (cero 50/50 = todo B, bit a bit) y no nace ningún genotipo;
- (V) el porqué de B;
- (E) regla 14: la entrada se compara campo a campo contra sentidos_muro.tarea y corre_bp.tarea;
- (D) determinismo;
- (W) reintento de abortos y reanudación de una cadena;
- (X) el runner niega pool > 2;
- (L) la letra en 9 casos;
- (R) los shas de las referencias y la reproducción BIT A BIT de **forzada3 s59201 T 100k** con el JSON guardado.

## 4. Predicciones (firmadas antes del humo y del explora; `lee()` las imprime contra lo medido)
Mi modelo previo es el siguiente. Por generación, una regla sale de la clase A con probabilidad ≈ 0.07 (p_del) + 0.1·(1/6)·(10/11 + 1 + 2/3) ≈ 0.11.
Con ~15 partos por linaje y por pasaje, la mitad de la clase A de la parte parida se pierde por **mutación**, también en la neutra.
Entonces la neutra cae hacia ~0.1–0.25 sin ninguna selección. El discriminante es el **pareado** contra la neutra.

| # | predicción | p |
|---|---|---|
| M1 | neutra: mediana de la fracción A en p9 en [0.05, 0.30] | 0.60 |
| M2 | moneda: mediana de la fracción A en p9 ≤ 0.15 | 0.60 |
| M3 | moneda < neutra en p9 en ≥ 4/5 cadenas | 0.55 |
| M4 | veredicto PURGA | 0.45 |
| M5 | cero: media de p9 en [0.35, 0.65] | 0.80 |
| M6 | arrastre mediano por pasaje en [0.55, 0.80] | 0.80 |
| M7 | prueba moneda: suma de cruzan en [8, 22] de 45 | 0.60 |
| INV1 | (investigador 1) veredicto PURGA | 0.60 |

Veredicto que espero: **PURGA 0.45 · INDETERMINADO 0.50 · CONSERVA 0.05.**

## 5. Control que puede fallar
La **neutra**, con las mismas semillas de pasaje, la misma mutación, el mismo largo y el mismo acceso al banco. Si la neutra cae
igual que la moneda, la pérdida es **carga mutacional o deriva, no moneda**, y el veredicto no puede ser PURGA. **cero** comprueba
que el instrumento no fabrica tendencia.

## 6. LA LETRA (por código: `corre_moneda.letra`; el arnés la prueba en 13 casos; enmendada por auditoría H-1, sec. 12)
- **PURGA:** se cumplen las tres:
  - la fracción A de la moneda en p9 es < 0.10 en ≥ 4/5 cadenas;
  - la moneda en p9 es **≤ 0.5 × la neutra** en p9, pareado por cadena, en ≥ 4/5 (H-1b; antes decía "estrictamente menor");
  - la **mediana de la neutra en p9 es ≥ 0.10** (H-1a). Si no, el veredicto es INDETERMINADO: el pasaje no conserva nada, pague o no pague (sec. 7).
- **CONSERVA:** la fracción A de la moneda en p9 es ≥ 0.40 en ≥ 3/5.
- **INDETERMINADO:** cualquier otra cosa.
- **Validez** (si una falla: NO SE LEE):
  - 0 abortos, las 15 cadenas y las 5 pruebas completas;
  - fracción de entrada 0.5 en todas;
  - cero: la siembra final sólo contiene genotipos inyectados, en 5/5;
  - cero: media de p9 en [0.30, 0.70];
  - los 10 JSON de referencia con su sha16;
  - arnés PASA con los shas actuales del runner y del arnés.

"Purga" significa aquí, y sólo esto: **baja la fracción de listas de clase A en la siembra** (no se mide la conducta de los cuerpos).
El alcance es el **régimen de mezcla 50/50** de la siembra inyectada (A y B en la misma pista); no se extiende a otras mezclas ni a forzada3 (100 % A).

**Qué decide (acotado al régimen de mezcla 50/50).** PURGA → el problema es la moneda. Siguiente: pasajes ponderados por hijos a 100k, o siembra por la letra.
CONSERVA → el problema es encontrarla. Siguiente: andamio o escalera.

## 7. Qué lo refuta
- La hipótesis cae si la neutra cae igual o más rápido que la moneda en ≥ 2/5 cadenas (sin PURGA), o si la moneda conserva
  ≥ 0.40 en ≥ 3/5 (CONSERVA).
- Si el veredicto es INDETERMINADO con la neutra ya en < 0.10: el pasaje no conserva **nada**, pague o no pague. El muro sería la carga
  mutacional o el arrastre, no la moneda. Se escribe así; no se reinterpreta como PURGA.
- La prueba a 100k es **descriptiva**. Si la siembra purgada sigue cruzando como forzada3 (~23), la regla no hacía falta en la siembra.

## 8. Cuatro trampas
1. **Canal simétrico:**
   - A y B tienen el mismo largo (una regla) y el mismo consumo de rng en la mutación;
   - los tres brazos usan las mismas semillas de pasaje;
   - la etiqueta j es muda (arnés N);
   - las vacías se reemplazaron por B porque la vacía no tiene acceso al banco (sec. 2).
2. **Acierto sin balancear:** cada brazo arranca en 0.5 exacto y se compara pareado contra una neutra con la misma maquinaria. No se lee ninguna fracción en absoluto.
3. **Mundo que se come la comida:** A y B conviven en la **misma** pista (los 9 linajes comparten el anillo). La aptitud depende de la frecuencia.
   Por eso forzada3 (100 % A) no es el mismo régimen que la moneda (mezcla). Se declara; no entra en la letra.
4. **Sitios fijos:** las letras tienen significado fijo en la pista. Los pasajes se entrenan en 6331xx y la prueba es en 592xx, pareada.
   El sentido 10 lee lo sentido, no la identidad.
5. **Clase A por etiqueta, no por función (H-2).** La clase A se mide por la etiqueta (sentido 10, j 0, `>`, boca), con cualquier θ y w. Un
   descendiente de A que ya no es "riesgo" (por ejemplo, w ≥ 0) sigue contando como A, y un descendiente de B con w < 0 no cuenta. El sesgo es
   **simétrico** (misma regla de medida en los tres brazos) y **conservador para PURGA** (retiene como A mutantes que ya no pagan como riesgo).
   La clase A con w < 0 (`f_neg`) queda como **descriptivo**; no entra en la letra.

## 9. Costo y comando
- Humo, un proceso: 6 corridas y 135 000 pasos.
- Explora: 15 cadenas × 250k + 5 pruebas × 100k = **4.25 M pasos**. A la tasa medida en sentidos_muro con pool 2
  (4.5 M en 2 159 s), son **≈ 34 min**.
- Comando (lo lanza el coordinador):
  `python experimentos/organelos/moneda/corre_moneda.py --explora --pool 2`
- Si se corta: el mismo comando con `--reanuda`.
- Lectura: `--lee datos/explora_<fecha>`.

## 10. Cambios antes de datos
Ninguno en la letra. El reemplazo de las vacías por B se decidió antes del arnés (sec. 2).

## 11. Mini-prueba (humo, un proceso, semillas de práctica 633180–633181 / 633191; corrida DESPUÉS de firmar las secs. 1–10; no cuenta)
Hubo 6 corridas y 135 000 pasos en 127 s (≈ 0.94 ms por paso). Carpeta `datos/humo_20260929_120821`.

| brazo | fracción A: entrada → p0 → p1 | vivos con A | arrastre ≥ | partos por pasaje |
|---|---|---|---|---|
| moneda | 0.50 → 0.536 → **0.633** | 0.67 → 0.80 | 0.75, 0.74 | 112, 119 |
| neutra | 0.50 → 0.433 → **0.344** | 0.33 → 0.16 | 0.67, 0.72 | 147, 127 |
| cero (1 pasaje) | 0.50 → 0.538 | 0.67 | 0.72 | 125 |

Prueba de 10k: 0/9 cruzan (T corta; no dice nada). En **una** cadena y **dos** pasajes, la regla de riesgo **sube** en la siembra,
mientras la neutra cae por mutación, como predije. La moneda pare **menos** (112–119 frente a 127–147) y aun así gana en
fracción: sus fundadores se establecen y ocupan los linajes (vivos con A de 0.67 a 0.80). Si esto se repite, M2, M3, M4 e INV1
caen. **No cambio ninguna predicción ni la letra:** quedan como se firmaron.

## 12. Cambios por auditoría antes de datos (29-sep; auditor: LISTO CON CAMBIOS; ningún dato del explora existía)
- **H-1 (obligatorio), en `letra()` y en la sec. 6.** PURGA exige ahora dos condiciones nuevas:
  - (a) la mediana de la neutra en p9 es ≥ 0.10; si no, INDETERMINADO;
  - (b) la moneda es ≤ 0.5 × la neutra, pareado, en ≥ 4/5, en lugar de "estrictamente menor".
  - Constantes `MITAD = 0.5`, `NEUTRA_MIN = 0.10`. La cuenta "estrictamente menor" queda como descriptivo (`moneda_mas_rapida_que_neutra`) porque la predicción M3 se firmó con ella. `lee()` imprime `moneda_le_mitad_neutra` y `neutra_mediana_p9`.
  - Arnés (L): el caso PURGA base se ajustó a la nueva regla. Se agregaron 4 casos:
    - neutra < 0.10 → INDETERMINADO;
    - neutra con mediana 0.10 exacta basta;
    - menor pero > 0.5 × neutra → INDETERMINADO;
    - = 0.5 × neutra cuenta.
  - Quedan 13 casos de letra.
- **H-2, en la sec. 8, punto 5.** La clase A se mide por etiqueta, no por función. El sesgo es simétrico y conservador; `f_neg` es descriptivo.
- **H-4, en la sec. 6.** La conclusión se acota al régimen de mezcla 50/50. "Purga" = "baja la fracción de clase A en la siembra".
- Las predicciones M1–M7 e INV1 **no cambian**. El humo (sec. 11) no se repitió. El arnés se volvió a correr entero con los shas nuevos.
