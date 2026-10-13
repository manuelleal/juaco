# ETAPA 4 sobre v9 — Memoria persistente: ausencia con interferencia, y herencia cero / parcial / completa

**Escrito ANTES de construir el instrumento y ANTES de correr. 16 sep 2026, día 4.**

- **Dirección:** Christiam Puentes ("pasa a 4").
- **Ejecución:** en el repo, sobre v9 (`d3b72fb8819fbe8e`).
- **Brief:** punto 11 ("borrar mundo, matar cuerpo, reproducir, cambiar entorno") y punto 8F (memoria heredada).

## 0. Lo que es propiedad de la arquitectura y NO se "prueba" (se declara)

- **Muerte del cuerpo.** En v9 (y desde v4) morir sólo reinicia la energía (0.6) y la posición. Los pesos no se tocan.
  **La memoria sobrevive a la muerte por construcción.** No se corre un experimento para eso.
- **Ausencia sin experiencia.** `Wp`, `Wn`, `KW` y las divisiones sólo cambian dentro de `if mordio:` (y las patas,
  con aprendizaje activo). **Sin aprendizaje durante la ausencia, la retención es exacta por construcción.** Se usa
  como **control** (M1), no como resultado.
- **Lo que sí se mide:** retención cuando durante la ausencia **se aprende otra cosa** (interferencia por celdas
  compartidas y por divisiones; lección de A5), y el valor de **heredar** memoria según si el mundo cambió.

## 1. Instrumento

`experimentos/etapa4_v9/organismo_v9m.py` se genera por anclas desde `organismo/organismo_v9.py` con
`construye_v9m.py`. Todo apagado por defecto, y en ese caso es v9 exacto.
- **`fases={t: (tipos, valencias)}`:** en el paso t cambia qué estímulos existen. Se retiran los objetos de tipos que
  ya no existen y se repone. Se sondea `W` de A, B, C y D en ese instante.
- **`congelar=(t0, t1)`:** sin aprendizaje (boca, canales, divisiones y patas) en [t0, t1).
- **`estado_inicial` y `heredar_patas`:** la cría arranca con copia de `KW`, `activa`, `Wp`, `Wn`, `err` y `mu` del
  progenitor, y con `Wl` sólo si `heredar_patas=True`. Los contadores empiezan en cero.
- **`devolver_estado=True`:** devuelve ese estado al final.
- **Lectura, sin RNG:** muertes por cuarto; primer encuentro con cada estímulo tras cada cambio de fase (paso, `W`,
  `pb`, si mordió).

## 2. Bloque M — ausencia con interferencia

- **Diseño.** Fases, con T = 150.000:
  - [0, 50k): A comida, B veneno;
  - [50k, 100k): **sólo C (veneno) y D (comida)**, con A y B retirados;
  - [100k, 150k): vuelven A y B, y se retiran C y D.
- **Condiciones:** `con_aprendizaje` y `control` (`congelar=(50000, 100000)`). Semillas 1..20.
- **Métricas:** `W_A` y `W_B` en 50k y en 100k (sonda, antes de ninguna mordida nueva); cambio `ΔW`; `pb` al primer
  reencuentro con A y B, sin voto.

**Predicciones:**
- **M1 [control, por construcción]:** en `control`, `W_A` y `W_B` en 100k son **idénticos** a 50k (numéricamente), 20/20.
- **M2 [recuerda pese a la interferencia]:** en `con_aprendizaje`, `W_B(100k) ≤ −2.0` en ≥ 15/20 **y**
  `W_A(100k) ≥ +0.5` en ≥ 15/20.
- **M3 [la interferencia existe y se mide]:** en `con_aprendizaje`, `|ΔW_A| + |ΔW_B| > 0.01` en ≥ 10/20 semillas.
  Los códigos de C y D se sortean libres, así que la mayoría comparte alguna celda con A o B.

## 3. Bloque H — herencia

- **Progenitor:** v9, E1, semilla s, T = 100.000, `devolver_estado=True`.
- **Cría:** semilla `1000 + s` (otro cuerpo y otro mundo), T = 100.000, en seis condiciones:

  | | cero | parcial | completa |
  |---|---|---|---|
  | qué hereda | nada (v9 nuevo) | `KW`, `activa`, `Wp`, `Wn`, `err`, `mu`, **sin** patas | todo, **con** patas |
  | mundo | `igual` (A comida, B veneno) o `invertido` (`invertir_en=0`: A veneno, B comida desde el primer paso) | | |

**Predicciones, derivadas de lo medido en el proyecto:**
- **H1 [mundo igual, ventaja]:**
  - mediana de mordidas de veneno de `completa` en Q1 ≤ **0.5 ×** la de `cero`;
  - `completa` < `cero`, pareado, en ≥ 15/20.
  - *Por qué:* nacer con `W_B = −3` evita las ~19 mordidas de aprendizaje y la exploración inicial.
- **H3 [mundo igual]:** muertes en Q1, `completa` < `cero`, pareado, en ≥ 15/20.
- **H4 [mundo invertido, desventaja]:** muertes en Q1 + Q2, `completa` > `cero`, pareado, en ≥ 15/20.
  - *Por qué:* la cría completa teme a B, que ahora es comida, y ese miedo sólo se extingue probando con hambre (≈2.5%
    por visita a hambre máxima). La cría `cero` muerde lo nuevo con p ≈ 0.84.
- **H5 [la herencia no impide adaptarse]:** en el mundo invertido, `completa` termina con `|W_A+3| < .3` y
  `|W_B−1| < .15` en ≥ 15/20.
- **H2 (sin voto):** mundo igual, veneno en Q1 de `parcial` ≤ 0.6 × `cero`. Las patas nuevas cambian las visitas y
  no hay base para una cifra firme.

**¿Qué lo haría pasar por la razón equivocada? Respondido antes de correr.**
- **Que la cría `completa` muera menos sólo por heredar patas que ya saben forrajear, y no por la memoria de valor:**
  `parcial` lo separa (H2, descriptivo).
- **Que el mundo de la cría fuera el mismo sorteo que el del progenitor:** se usa una semilla distinta (`1000 + s`).
- **Que M2 pase porque C y D no comparten nada con A y B:** M3 lo vigila. Si M3 falla, M2 no dice nada sobre
  interferencia y se declara así.

## 4. Qué se decide

- **Instrumento** (se comprueba antes de correr; si falla, se para):
  - `v9m` con los valores por defecto ≡ v9 en los 7 escenarios × semillas 1..3;
  - `v9m(estado_inicial=estado de una cría cero recién nacida)` produce una corrida válida.
- **M1, M2, M3, H1, H3, H4 y H5 sostenidas:** **la Etapa 4 se cierra.**
  - Recuerda sin experiencia (exacto) y recuerda pese a aprender otra cosa (medido).
  - La memoria heredada **es ventaja en un mundo que no cambió y desventaja en uno que cambió**, sin impedir la
    adaptación.
- **Cualquier otra combinación:** no se cierra; se registra lo que falló, y el rediseño va con preregistro nuevo.

## 5. Qué NO prueba

- Herencia con selección, a lo largo de varias generaciones o en poblaciones (punto 8F completo).
- Transmisión horizontal entre individuos: eso es la Etapa 5, y es lo que motiva este resultado.
- Memoria episódica.
