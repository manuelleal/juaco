# gen1 / llm_2 — operador LLM, clase REGLA ESTRUCTURAL

**Padre:** `experimentos/v10_direccion_division/organismo_v10m.py`. **Hijo:** `organismo.py` (esta carpeta). Diff: 12 líneas
(métrica de `evalua.py`), sin parámetro de apagado, misma interfaz `run(...)` y mismas claves devueltas.

## Diagnóstico previo (lo que vi antes de proponer)

Leí `datos/v10_confirmatorio_20260916_175557.json` (bloque M del padre en semillas 21–40; no son las retenidas 11–20,
pero lo declaro). Retención con ambos criterios: 4/20. Los modos de fallo, por semilla:

- `W_A(100k) < 0.5` en 16/20, y en la mayoría **el código de A no cambia**: la celda que A comparte con C (A·C comparten el
  píxel 1) es arrastrada por RW + drenaje `lam` hasta ≈ −1 mientras A no está. El error EMA de esa celda nunca llega a
  `theta`, porque C converge en ~10 mordidas y `err` acumula a tasa 0.02: la regla 2L del padre **no dispara** ahí.
- `W_B(100k) > −2` en 10/20: hijas nacidas por C/D que entran en el código de B (22, 24, 25, 32, 38, 39) o **madres**
  empujadas hacia su `mu` (= hacia B) que entran en el código de B o de A con el valor arrastrado (26, 27, 33; A en 22 y 38).
- Las hijas de celdas vírgenes (`mu`=0) reciben el empuje completo `+paso·P`, que en D pisa los dos píxeles que B comparte.

## Mecanismo (qué cambia y dónde)

Sólo el bloque `if plast:` dentro de la mordida (líneas 100–107 del padre). Cuatro decisiones, una regla:

1. **Cuándo se divide:** por **conflicto de signo**, no por error acumulado. La celda `c` del código de P se divide si su
   valor previo a la mordida `Wb[c] = Wp[c]−Wn[c]` tiene signo contrario al refuerzo `R` y `|Wb[c]| > 0.2` (valor
   consolidado: una celda de comida vale +0.33, una de veneno −1). Dispara en la **primera** mordida contraria, antes
   del arrastre. La regla `err[c] > theta` desaparece (`err`, `theta`, `ema`, `err_max` quedan como instrumentación).
2. **Hacia dónde y qué hereda:** la hija es `kj = clip(0.95·KW[c] + paso·dist, 0, 5)·(P>0)`, con `dist` la de v10
   (mu normalizada). Nace **ciega fuera de los píxeles de P** (no puede entrar en códigos ajenos por los píxeles de la
   madre) y con **5 % menos de la sintonía heredada** dentro de P. Su historia es P: `mu[j] = P·masa(mu[c])`.
3. **División estéril = no ocurre:** sólo se divide si `kj·P > KW[c]·P` (la hija le gana a la madre en P). Con
   `mu ≈ P` (`dist ≈ 0`, p. ej. la inversión de E2) la hija sería un clon 5 % más débil y no se divide: E2 se resuelve
   reescribiendo el valor por RW, como en v7. Esto acota las divisiones: cada hija entra al código de P por encima de la
   madre, así que la madre sale del código de P tras ≤ 3 hijas.
4. **La madre no se mueve** (su `KW` queda intacto: ninguna celda consolidada cambia nunca de sintonía) y el valor se
   **fisiona**: si `R>0` la hija se lleva `Wp[c]` y la madre queda con `Wn[c]` (y `Wp[c]=0`); si `R<0`, al revés. La
   madre conserva exacto el valor del patrón viejo; el drenaje `lam` no la toca porque `min(Wp,Wn)=0`.

Por qué la madre fija no repite K1: K1 fallaba E2L por **empate** (madre `[5,0,0,0,0,0]` e hija `[5,.25,0,.25,0,0]`
leen 5 para B). Aquí la hija lee 4.75 para B y 5.45 para A: A → hijas, B → madres, solapamiento 0 en una sola ronda.

## Hipótesis (una línea)

El olvido del bloque M es arrastre de valor en celdas compartidas más captura de códigos por hijas y madres movidas; si la
división dispara al primer refuerzo contrario, fisiona el valor y sólo mueve a una hija ciega fuera de P, A y B conservan
código y valor mientras C y D se aprenden en hijas nuevas.

## Predicción numérica

- **R (semillas 1–10): 0.8–0.9** (8–9/10), frente a ~0.3–0.5 del padre. Medianas: `W_B(100k) ≈ −3.0`, `W_A(100k) ≈ +1.0`.
  Fallos residuales esperables: hija de una madre entrenada por C que nace para D gana +0.5 en el píxel 4 (de B) y puede
  entrar en el código de B si la tercera celda de B es débil; hija para C desde madre de B/D gana +0.5 en el píxel 1
  (de A). Ambas raras (leen ≈ 1–1.8 frente a ≈ 2.3 de la tercera celda).
- **Guarda H3:** `W_C ≤ −2.5` y `W_D ≥ 0.85` en ≥ 9/10 (C y D se aprenden en hijas propias; en la corrida de humo, −2.61 y +0.99).
- **E1:** idéntico al padre (sin conflicto no hay división y el flujo del RNG no cambia) → `S` igual.
- **E2:** 0 divisiones (padre: 3 clones); pasa por reescritura RW. Es el riesgo principal de H1: si la regla bloquea la
  revaloración, cae aquí.
- **E2L:** exactamente 3 divisiones, en una ronda, antes de t=25.000 (humo: t=183) → `E = 0.67`, igual al padre.
- **E2I/E2J/E2K:** 1–2 celdas compartidas se dividen en la primera mordida contraria (≤ 3 hijas por celda); celdas ≤ 36.
- **CTRL:** falla como debe (la regla está detrás de `plast`).
- **Divisiones en el bloque M:** mediana 3–6 (padre: ~4), todas en la primera mordida contraria de cada fase; celdas ≤ 45.
- **C = 12/15 = 0.8.**

## Estado nuevo añadido

Ninguno. Usa `Wb`, `R`, `mu`, `KW`, `Wp`, `Wn`, `activa` que ya existen; `kj` es temporal. Dos constantes nuevas en el
cuerpo: `0.2` (valor mínimo para contar como consolidado) y `0.05` (merma hereditaria de la hija).

## Qué lo haría pasar por la razón equivocada

- **Retener por no aprender:** la guarda H3 (W_C, W_D en 100k) lo atrapa; auditar además mordidas de C y D hasta criterio.
- **Retener por no dividir (congelar códigos):** E2L exige solapamiento 0 con divisiones; auditar `splits == 3` en E2L y
  que el bloque M tenga divisiones (si `splits_M == 0` en la mayoría, la retención sería la de `plast=False`, no la de
  esta regla). Distingue de K0s: aquí `W_viejo(B)` (valor sobre el código de 50k) debe quedar ≈ −3, no ≈ −2.1.
- **La madre fija como congelación encubierta:** la madre sólo fija su sintonía, no su valor; sigue siendo re-entrenable
  por patrones del mismo signo y, si `mu ≈ P`, se reescribe sin dividir. Si E2 falla, esa es la señal.
- **La merma del 5 % como truco para E2L:** rompe el empate en el caso degenerado `[5,0,0,0,0,0]`; si E2L pasara sólo
  con `paso/merma` en una ventana estrecha, sería frágil. Auditar que E2L divide una sola ronda en las 10 semillas.
- **Identidad 4a de la batería (`splits>0 ⇔ err_max>0.6`) deja de valer por construcción:** ya no es evidencia de nada
  en este genoma; no debe citarse ni a favor ni en contra.
- **Sobreajuste:** el diagnóstico usó las semillas 21–40 del padre; la predicción se juzga en 1–10 y se confirma en 11–20.

## Corridas de humo (las dos prescritas, sobre el genoma entregado)

- `run(1, T=20000, solap_AB=3)`: W_A=+1.00, W_B=−2.82, solap 0, 3 divisiones (t=183, 'A'), celdas 33, muertes 29.
- `run(1, T=30000, fases={10000: C veneno + D comida, 20000: vuelven A y B})`: sonda 20k → A +0.99, B −3.20, C −2.61,
  D +0.99; códigos de A y B **iguales** a los de 10k; D leído por hijas [30,32,33]; 4 divisiones (3 en t=10075, 1 en
  t=10100), celdas 34.

Nota de procedencia: un primer borrador (madre empujada como en el padre, sin merma) pasó por las mismas dos corridas de
humo; en la segunda, la madre 25 (celda de B y C) fue empujada hacia el píxel 1 y entró al código de A con −1
(W_A = −0.79). Ese resultado motivó fijar la madre; las dos corridas se repitieron sobre la versión final. Total:
cuatro corridas cortas de humo, ninguna otra.
