# ETAPA 3 sobre el tronco v9 — versión dura y generalización EN CONDUCTA al primer encuentro

**Escrito ANTES de construir el instrumento y ANTES de correr. 16 sep 2026, día 4.**

- **Dirección:** Christiam Puentes ("dale hasta que lo logres").
- **Ejecución:** en el repo, sobre v9 (`d3b72fb8819fbe8e`, congelado).
- **Si algo falla, no se recalibra** (regla 3).

## 0. Qué se sabe antes de escribir (se declara)

1. **Etapa 3, día 3 (v6), mundo E1:** `W_X = 0.333·nA − 1.0·nB` se cumple con residuo máximo 5.9e-3, y el valor a
   priori sigue al solapamiento de códigos (R² 0.999999), no a la similitud visual (R² 0.33). El propio registro dice
   **"el diseño era demasiado fácil"** y deja preregistrada una **versión dura**: la fórmula debe fallar de forma
   medible cuando los códigos se solapan (2I/2J/2K), con el techo activo o con más de dos estímulos, y el residuo
   debe crecer con el solapamiento.
2. **El registro también dice que la Etapa 3 "no prueba que el organismo ACTÚE según él".** Nunca se midió la
   conducta.
3. **Rama 3K (día 3, sobre v6):** mundo de 20 patrones de peso 3, con la valencia decidida por el píxel 0, 10 de
   entrenamiento y 10 de test que entran en t=100.000.
   - Su "precisión 0.683" es la tasa de mordida **por visita a lo largo de toda la fase 2**, así que **mezcla** la
     generalización con lo aprendido después y usa la métrica "por paso" que ERR-15 mostró diluida.
   - **Nadie ha medido la conducta al primer encuentro.**
4. **Sobre v9:** en las seis etapas el techo no trunca (0/120), así que la condición "(b) techo activo" del día 3 **no
   aplica** en esos escenarios. Se reporta cuántas truncaciones hay en cada mundo, sin voto.
5. **No se ha corrido nada de este diseño sobre v9 con ninguna semilla.**

## 1. Instrumento

`experimentos/etapa3_v9/organismo_v9g.py` se genera desde `organismo/organismo_v9.py` por anclas con
`construye_v9g.py`. Añade tres cosas.
- **`mundo='regla'`** (por defecto `'AB'`, que es v9 exacto):
  - los 20 patrones de peso 3;
  - `regla ∈ {'px0', 'xor01', 'azar'}`;
  - partición de entrenamiento y test con un RNG propio (`10000 + semilla`);
  - sin muestreo por rechazo de KW, como en 3K;
  - en `fase2_en = T/2` entran los patrones de test.
- **Sonda de lectura** en `fase2_en`: valor a priori `W_X` y código de los 20 patrones.
- **Registro del PRIMER ENCUENTRO** de cada patrón de test: paso, `W`, `pb` (probabilidad de morder que calcula la
  boca), hambre y si mordió. Todo sin RNG.
- **`sonda_final=True`** (sólo en `'AB'`): valor y código de los 64 patrones de 6 píxeles al final, para la versión
  dura en E1/E2J/E2K.

**Reglas de valencia:**

| regla | comida si… | train (comida + veneno) | test | notas |
|---|---|---|---|---|
| `px0` (lineal) | píxel 0 = 1 | 5 + 5 | 5 + 5 | como 3K |
| `xor01` (no lineal) | píxel 0 ≠ píxel 1 | 4 + 4 | 8 + 4 | 12 comida / 8 veneno |
| `azar` (control) | valencia sorteada por semilla (RNG `30000 + semilla`) | 5 + 5 | 5 + 5 | balanceada 10/10 |

`T = 200.000`.

## 2. Diseño

| bloque | escenarios | semillas | corridas |
|---|---|---|---|
| **Versión dura (VD)** | v9 en E1 = `run(s)`; E2J = `run(s, nuevo='D', nuevo_val='comida', solap_B=1)`; E2K = `…solap_B=2`, con `sonda_final=True` | 1..20 | 60 |
| **Generalización (G)** | v9 en `mundo='regla'` con `px0`, `azar` y `xor01` | 1..20 | 60 |

## 3. Métricas

**Residuo nominal (VD).** Para cada patrón X con al menos una celda en común con algún estímulo aprendido S:
`res = |W_X − Σ_S (|code(X)∩code(S)|/3)·R_S|`, con R = +1 (comida) / −3 (veneno).
- En VD: S ∈ {A, B} en E1 y S ∈ {A, B, D} en E2J/E2K, con los códigos finales.
- En G: S = los 10 de entrenamiento, con los códigos de `fase2_en`.
- Se excluye el patrón nulo `000000` (ERR-07).

**Generalización de valor (sobre los patrones de test).** Exactitud balanceada del signo de `W_X` a priori:
`0.5·frac(W>0 | comida) + 0.5·frac(W<0 | veneno)`. `W = 0` exacto cuenta 0.5.

**Generalización en conducta al primer encuentro.** Exactitud balanceada de la probabilidad de morder:
`BA_pb = 0.5·media(pb | comida) + 0.5·media(1−pb | veneno)`. Además se reportan las mordidas reales al primer
encuentro por clase, sin voto.

**Alcance.** Fracción de patrones de test con `W_X = 0` exacto.

## 4. Predicciones y criterios

**K [instrumento]. Si falla, no se lee nada más.**
- `v9g(mundo='AB')` ≡ v9 en todas las claves de v9, en los 7 escenarios × semillas 1..3.
- Con `sonda_final=True`, las claves de v9 siguen idénticas (E1, semillas 1..3).
- En `mundo='regla'`, **20/20** corridas registran primer encuentro para ≥ 8 de sus 10 patrones de test (en `xor01`,
  ≥ 10 de 12). Si no, la métrica de conducta no es evaluable.

**VD [versión dura del día 3, adaptada].**
- **VD1:** en E1, residuo máximo < 0.01 en 20/20. Es el control: con códigos disjuntos la fórmula es exacta, como
  el día 3.
- **VD2:** la mediana por corrida del residuo **crece con el solapamiento**: E1 < E2J < E2K, pareado por semilla, en
  ≥ 15/20 para cada desigualdad.
- **VD3:** en el mundo `px0` (10 estímulos, códigos que se pisan), la mediana del residuo es > la de E2K en ≥ 15/20.

**G [generalización]. Deciden el cierre de la Etapa 3.**
- **G1, valor:** mediana de la exactitud de signo `px0` ≥ **0.65**; mediana en `azar` ∈ [0.35, 0.65]; `px0` > `azar`
  (estricto, pareado) en **≥ 14/20**.
- **G2, conducta al primer encuentro:** mediana de `BA_pb` en `px0` ≥ **0.55**; en `azar` ∈ [0.42, 0.58]; `px0` >
  `azar` pareado en **≥ 14/20**.
- **G3, frontera no lineal (sin voto):** mediana de la exactitud de signo en `xor01` ≤ 0.60, y `xor01` < `px0`
  pareado en ≥ 14/20.

**¿Qué lo haría pasar por la razón equivocada? Respondido antes de correr.**
- **Diferencia de brillo:** controlada, todos los patrones tienen peso 3.
- **Que la partición favorezca por azar a una clase:** el control `azar` usa el mismo sorteo de KW y otra valencia.
  Si G1/G2 salen igual en `azar`, no hay generalización por la regla.
- **Que "primer encuentro" incluya experiencia previa:** imposible, porque los patrones de test no existen antes de
  `fase2_en`.
- **Que `pb` alto para todo lo nuevo esconda la diferencia:** por eso G2 es pareado contra `azar`, y la BA de la
  conducta tiene un umbral más bajo que la del valor (la boca muerde lo nuevo con p ≈ 0.84 aunque `W = 0`).

## 5. Qué se decide

- **K falla:** se para.
- **G1 y G2 sostenidas:** **la Etapa 3 se cierra**, en valor y en conducta. Con una característica lineal, v9 le
  asigna valor a patrones nunca vistos **y actúa según ese valor en el primer encuentro**, por encima del control.
  - VD cuantifica cuánto se degrada la fórmula por interferencia, que es lo que el día 3 dejó preregistrado.
  - G3 marca la frontera no lineal.
- **G1 sostenida y G2 no:** generaliza en valor pero la política no lo expresa al primer encuentro. **No se cierra.**
  Se registra como problema de la capa de política.
- **G1 falla:** no se cierra. Se registra.
- **VD falla:** se registra; no bloquea el cierre de G, que es la parte de la etapa que faltaba.

## 6. Qué NO prueba

- Características no lineales, fuera de la frontera reportada.
- Transferencia entre dominios.
- Memoria entre vidas (eso es la Etapa 4).
- No re-corre 3T ni 2K-bis sobre v9.
