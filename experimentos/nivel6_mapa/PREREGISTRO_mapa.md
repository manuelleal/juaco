# Nivel 6 (planificación), experimento 2 del plan: ¿elige v13 la dirección hacia comida recordada que no ve?

**Escrito ANTES de construir el instrumento y ANTES de correr. 17 sep 2026, noche del día 5.** Segundo experimento del
plan del debate (`registro/investigacion/DEBATE_y_plan_5a10.md` §3, punto 2), condicionado a que 3T-k no refutara la
composición de más de un paso: **no la refutó** (k = 1, 2, 3 componen, 20/20 en cada k, `3T_k_s1-20_20260917_191732`).
Regla 12.

## 0. Premisa corregida (hallazgo de diseño, va al registro)

El informe de nivel 6 (`nivel6_planificacion.md` §2) parte de que "la retina sólo informa la ventana de 6 píxeles
actual". **Es falso en el tronco:** `see()` de `organismo_v13.py` devuelve el objeto **más cercano de todo el anillo**
con su lado (`left`) y su distancia; el organismo siempre sabe hacia dónde está el objeto más próximo. Por eso el
"teletransporte con la meta fuera de la ventana" no mide nada sobre v13 tal cual: la meta nunca está fuera de la vista.
La prueba de planificación necesita un **mundo con visión limitada** (`r_vis`): más allá de `r_vis` casillas no se ve
nada (retina en cero, sin bit de lado ni de contacto). En ese mundo, v13 sin mapa es la línea base justa.

## 1. Mundo `mundo_mapa.py` (desde `organismo_v13.py` `cc8b16b492d4d324`, por anclas; con perillas apagadas es v13 exacto)

- `r_vis` (None = tronco): objetos a distancia > `r_vis` son invisibles. Sin nada visible: `pat = 0`, lado = 0, contacto = 0.
- `sitios` (None = tronco): objetos en **sitios fijos** por semilla: `F` al azar y los demás a `L/n` casillas; cada sitio
  tiene tipo fijo; al morderlo (o al "olvido" de v9) desaparece y **reaparece en el mismo sitio** `regen = 50` pasos después.
- **Tabla `M`** (`usa_M`): `M[pos] = último patrón visto en pos` (6 píxeles; se escribe sólo al estar sobre un objeto).
  Con la retina vacía, por dirección `dir ∈ {izq, der}`: `B_dir = Σ_{h=1..H} disc^h · valor(M[pos ± h])` sobre las
  entradas escritas, con el `valor()` de la boca (las dos vías y la puerta, sin tocar); `u += gamma_M · [B_izq, B_der]`
  sobre la política de patas. `H = 20`, `disc = 0.9`, `gamma_M = 0.6`. Nada de valor nuevo: sólo lee lo que ya sabe.
- **Prueba de teletransporte** (sin aprendizaje, tras T = 100 000): 40 teletransportes por semilla, alternando lado; la
  comida queda a `d_n ∈ [r_vis+1, 12]` casillas por un lado (invisible) y a `40 − d_n ≥ 28` por el otro; el veneno
  (sitio opuesto a F) queda a ≥ 8 casillas; `E = 0.3`; traza y memoria de rechazo en cero. Se registra la dirección del
  **primer paso** (hasta 30 pasos sin moverse cuenta como "no se movió", aparte). `acierto` = primeros pasos hacia el
  lado de la comida / primeros pasos.

## 2. Brazos (semillas 1–20; `r_vis = 3`, `sitios = (A=comida, B=veneno)`, T = 100 000)

| brazo | qué es | esperado |
|---|---|---|
| MAPA | v13 + `M` (`gamma_M = 0.6`) | la pregunta |
| SINMAPA | v13 en el mismo mundo, sin `M` | línea base; sesgo motor |
| CONGELADA | `M` nunca escrita | 0.50 **por construcción** (sesgo idéntico a cero; se verifica `M_llenas = 0`) |
| BARAJADO | MAPA entrenado; en la prueba, `Wp/Wn` permutados entre celdas y `Wps/Wns` entre píxeles | ≤ 0.60: si acierta igual, la dirección **no** viene del valor de lo recordado (memoria escondida, K4) |
| SINCOMIDA | dos sitios de veneno, meta virtual | 0.50 (control de sesgo motor puro) |

Identidad obligatoria: `mundo_mapa.run(seed)` con perillas apagadas ≡ `organismo_v13.run(seed)`, todas las claves,
semillas 1–3 × {base, `invertir_en=50000`, `nuevo='C'`} = 9 comparaciones.

## 3. Criterios (medianas sobre 20 semillas) y predicción

- **P1:** MAPA `acierto` ≥ **0.75** y ≥ 15/20 semillas > 0.60. **C1:** CONGELADA en [0.40, 0.60] y `M_llenas = 0` en todas.
  **C2:** BARAJADO ≤ 0.60. **C3:** SINCOMIDA en [0.40, 0.60]. **C4:** SINMAPA en [0.40, 0.60].
  **F1 (funcional):** comida mordida en el último cuarto, MAPA > SINMAPA pareado en ≥ 15/20.
- **Predicción:** P1, C1–C4 y F1 pasan → "v13 + `M` elige la dirección hacia comida recordada fuera de la vista y come
  más" (no se dice "planifica" sin réplica en 21–40). **Refutación:** P1 falla (o C2 falla: acierta barajado → ERR, la
  medida no mide lo que dice). Si P1 falla y F1 pasa: `M` ayuda a sobrevivir sin dirigir el primer paso; se registra
  tal cual. Nada se recalibra después de ver datos: se registra y se escribe criterio nuevo para semillas nuevas.
- Coste: 5 brazos × 20 semillas = 100 corridas de 100 000 + pruebas cortas.

## Enmienda 1 (escrita tras el humo del instrumento en la semilla 2, ANTES de correr las 20 semillas)

El humo (identidad 3/3; MAPA 0.825, SINMAPA = CONGELADA 0.525, SINCOMIDA 0.52) mostró que **BARAJADO dio 0.75**: al
permutar `Wp/Wn` entre celdas, la puerta manda a la vía lenta, y la vía lenta permutada entre píxeles conserva el
**signo** (la masa positiva domina porque el organismo con mapa casi no muerde veneno: `W[B] = 0.1`). Cualquier sitio
recordado sigue atrayendo, y el más cercano suele ser la comida. C2 se deja como está (se reporta) pero **no es
decisivo**. Se añade el control decisivo **INVERTIDO**: en la prueba, `Wp ↔ Wn` y `Wps ↔ Wns` (el valor cambia de
signo; la puerta, que usa |Wp − Wn|, no cambia). **C5: INVERTIDO ≤ 0.40** (debe *huir* del sitio de la comida
recordada). `ELIGE` = P1 ∧ C1 ∧ C3 ∧ C4 ∧ C5. Predicción: C5 pasa. Si INVERTIDO se queda cerca de 0.5 o arriba, la
dirección no corre por el valor de lo recordado y no se declara nada.
