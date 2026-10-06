# PREREGISTRO — EXAMEN GRANDE de HUMO contra O1 (nube, 6-oct-2026; escrito ANTES de correr)

Misión: llegar a la AGI por este camino. Pide el director ("córrelo, a ver si lo logramos") tras el NO de la serie OpenEvolve
(`INFORME.md`).

**Qué se prueba:** el PROGRAMA, no el método de búsqueda. HUMO es el mejor programa del humo del 5-oct (sha 69fcfcb2473f), congelado. Lo
escribió una evolución de programas guiada por un modelo de lenguaje sobre un juez fijo. No es selección natural del organismo ni
aprendizaje del organismo: es un carro diseñado, de la misma clase que O1.

## 1. Pregunta
¿HUMO hace cruzar a la mayoría de los linajes de forma robusta, y mejor que O1, en semillas que nunca vio? El examen chico (5 selladas,
275001–275005) dio 5/5 con mayoría y 37 linajes contra 26. Es descriptivo y tiene pocas semillas.

## 2. Instrumento
- `corre_examen_grande.py`, con el mismo `corre_carro.py` de la serie: pista, juez y revisa_carro sin tocar; fundador NO limpio
  (ERR-191); T 100 000; 9 copias del carro.
- Cordura ya hecha en esta rama (`cordura/`): O1 en 883001/883002 = registro bit a bit.
- El script **se niega a correr** si el sha de HUMO no es 69fcfcb2473f, si el de O1 no es 99436afa2715f028, o si HUMO no pasa el filtro de
  reglas.
- Brazos: **HUMO** y **O1**. RAIZ no entra: ya dio 0/5 y 0 linajes, y su lugar en la letra lo ocupa la cordura de O1.

## 3. Semillas (nuevas; grep del 6-oct: 2760xx no aparece como semilla en el repo, sólo como números dentro de JSON de datos)
- Serie: **276001–276020**.
- Réplica: **276021–276040**. Sólo se corre si la serie no da NO.

## 4. LA LETRA (por tanda de 20 semillas)
Una semilla es "con mayoría" si cruzan_real ≥ 5/9 (juez).

**Validez:**
- V1: 40/40 corridas.
- V2: los shas y el filtro de reglas (el script se niega a correr si no coinciden).
- V3: O1 con mayoría en ≥ 6/20. Es una cordura floja: O1 dio 3/5 en el examen chico y 2/9 en una semilla de calibración.

**Puertas:**
- **P1:** HUMO con mayoría en **≥ 15/20**. Es el umbral de la letra del muro.
- **P2:** HUMO cruza **más linajes que O1** en **≥ 12/20** semillas, pareado por semilla; los empates no cuentan como victoria.

**Veredicto de una tanda:**
- **FUNCIONA:** V y P1 y P2.
- **HAY ALGO MODESTO:** V y P1, sin P2. El carro cruza el muro de forma robusta, pero no mejor que O1.
- **NO:** todo lo demás.
- **NO SE LEE:** falla V.

**Bloque:**
- Si serie y réplica coinciden, vale ese veredicto; si no, el menor.
- FUNCIONA ×2 se declara con este vocabulario: "el mejor carro de la pista con fundador no limpio, escrito por evolución de programas
  guiada por un modelo de lenguaje, cruza el muro en ≥ 15/20 ×2 y gana a O1".

## 5. Predicciones (antes de correr)
| # | predicción | p |
|---|---|---|
| G1 | P1 en la serie | 0.75 |
| G2 | P2 en la serie | 0.60 |
| G3 | O1 con mayoría en 8–15 de 20 | 0.70 |
| G4 | suma de linajes que cruzan, HUMO > O1 en la serie | 0.80 |
| V | bloque FUNCIONA / MODESTO / NO / NO SE LEE | 0.42 / 0.33 / 0.22 / 0.03 |

## 6. Costo y parada
- Costo: 0 USD de modelo (no se llama a ningún modelo). CPU: 40 corridas por tanda, ~1 h con Pool 3.
- No hay más tandas tras la réplica. Un FUNCIONA no hace a HUMO tronco ni candidato: es un carro de la pista, y eso lo decide el
  director.
- Siguiente ERR libre: ERR-196.

Firmado: Claude (sesión nube), 6-oct-2026, antes de correr.
