# PREREGISTRO — **v15f bajo el CRITERIO DE TRONCO v2** (siete puertas, semillas nuevas)

CREADOR A, 18-sep-2026 (10:20). Ejecuta `registro/CRITERIO_TRONCO_v2.md` (decisión del director 09:55) sobre v15f: la memoria
de pares con **R crudo, sobrescritura y relevo a la lineal**, cada vía con su propio error. **§1–§6 escritos ANTES de medir;
§7 (humo) después y se dice.** Sin `Pool` por mi parte (sala de agentes activa), sin commits, nada congelado tocado, nada de
v15c/d/e/f sobrescrito. ERR libres desde ERR-45; este preregistro no necesita ninguno.

**Misión (primero):** llegar a la AGI por este camino — un organismo que **generaliza, se desdice y vive**. Bajo el criterio
v1, v15f cayó por un subcriterio de v6 (ERR-44: "veneno Q4 < Q1" 17/20) con W_B ≈ −3 20/20, reversión 20/20, G1 1.000, xor01
1.000. El criterio v2 juzga la **conducta** y la **vida**; v15f es su primer candidato.

## 1. Lo que ya está medido de v15f (no se rejuzga; sirve de predicción)

`v15f_s161-180_20260918_095309`, `examen_v15f_20260918_095443`, `regresion_generaliza_v15f_organismo_v15f_on_20260918_095744`: identidad
32/32 · E1 W_B ≈ −3 20/20, "veneno Q4 < Q1" 17/20 (ERR-44) · E2 reversión 20/20 · E2I W_C ≤ −2.5 17/20 (conducta tasa A 20/20) ·
E2J/K/L 20/20 · G1 1.000 (azar 0.500) · G2 0.998 · xor01 estricta 1.000 [0.25, 1.00] contra 0.500 apagada, gana (0,1) 20/20 · px0
1.000/1.000 · azar 0.500/0.450 · V4 xor01 celdas +7.8 %, splits +16 %.

## 2. Instrumentos (por anclas; congelados sólo leídos; `manifiesto.py --check` 16/16)

- **`construye_vivo_relevo.py` → `organismo_vivo_relevo.py` (3b2cb0ca4c334779)** ← `experimentos/nivel11_mundo_vivo/organismo_vivo_rep2.py`
  (96feb4918dc5d694; cadena `organismo_vivo` 20c0961c79de8825 ← `organismo_v14` feefc88b1fd8d434). **Por qué rep2 y no `organismo_vivo`:**
  T-A (r = descendientes − muertes, brazos VIVO y CUELLO_MIN de `corre_vivo_rep2.py`) exige las perillas de reproducción; con
  `reproduccion=0` rep2 ES `organismo_vivo` bit a bit (identidad (A) del diseñador) y con `vivo=0, n_nec=1` es v14.1: el arnés lo
  comprueba en las cuatro cadenas. **Una tabla por necesidad** (n_nec × 15 × 4, R crudo de la componente de esa necesidad;
  sobrescritura); cada necesidad lee su casilla si conoce la combinación, si no su lineal; la lineal de cada necesidad aprende de
  SU error; la rápida de SU error (sin tocar); `CUELLO_MIN` (lectura pesimista de las dos filas) pasa por `_vnec`, que ya releva.
  Perilla `memoria_pares=None` ≡ rep2 bit a bit sin consumir rng.
- **Brazo exploratorio declarado, NO candidato: `relevo_boca=1` (v15g).** La casilla VISTA manda **antes** que la puerta de v14.1
  (exacto si lo conoce; si no, la puerta). Se mide **pareado** en T-D y en el humo para separar dos cosas: si T-D depende del
  mecanismo de la tabla o del ORDEN de las puertas. **Predicción escrita ahora (§5): v15f (relevo dentro de la lenta) NO pasa T-D
  porque en las semillas ALIAS el código compartido es familiar y la puerta lee la rápida (−1.45), aunque la tabla de hambre
  sepa que la sal vale 0.0 y el veneno −3.0; v15g sí pasa C1/C2.** Si sale así, v15g va a preregistro propio (no es una enmienda
  de v15f: es otro orden de puertas).
- **`invertir_vivo_en`** (T-C en el mundo vivo): `corre_vivo*.py` **no tiene** reversión con cuatro estímulos (`invertir_en` sólo
  reescribe `val` para A/B); en mi copia, en `t` se intercambian los EFECTOS de comida y veneno (A pasa a quitar energía, B a darla).
  Inerte por defecto (None); declarado aquí.
- Baterías ya construidas para v15f (regla 14 verificada): `bateria_v15f.py` (d63f5aee558eb6da), `bateria_generaliza_v15f.py`
  (0cd87d2632e0c66a); tronco de comparación: `organismo/bateria_v14.py` (congelada; se corre o se lee su JSON si ya existe uno
  de v14.1 en 121–140 con `sha_organismo_v13 = feefc88b1fd8d434`).
- `identidad_vivo_relevo.py` (22 comprobaciones: I1 rep2 VIVO ×3 · I2 rep2 CUELLO_MIN ×3 · I3 `organismo_vivo` ×3 · I4 v14.1 ×3 ·
  I5 las 9 ALIAS con `corre_sal.BASE` · I6 rng a T = 100 000). `corre_v15f_v2.py`: identidad → T-B → examen del candidato → examen
  del tronco → T-D (Pool) → T-C vivo (Pool); subprocesos SECUENCIALES, uno a la vez; **lee los JSON de las baterías** (ERR-43);
  `--humo` de un proceso. Reutiliza por import (sin copiar): `corre_vivo_rep2.BRAZOS/resumen2`, `corre_sal.BASE/ALIAS/LIMPIAS/resumen`.

## 3. Las siete puertas (umbrales de CRITERIO_TRONCO_v2.md; instrumento y semillas NUEVAS por puerta)

| puerta | instrumento | semillas | umbral (letra de v2) | estado |
|---|---|---|---|---|
| **T-A sobrevive** | `corre_vivo_rep2` brazos VIVO, VIVO+relevo, CUELLO_MIN+relevo con `organismo_vivo_relevo` (T = 100 000, `costo = 0.001`) | **301–320** | muertes ≤ 1.10 × tronco (mediana); r ≥ tronco − 10; A₁₂ ≥ 0.50 pareado | **se cierra con la síntesis de la sala 2; NO se mide antes** |
| **T-B generaliza** | `bateria_generaliza_v15f.py organismo_v15f_on 20 --desde 121 --log` | **121–140** | G1 ≥ 0.80, G2 ≥ 0.85, azar ∈ [0.35, 0.65] (G2: [0.42, 0.58]), K 20/20 | se mide |
| **T-C se desdice** | (i) examen E2 del candidato, leído por CONDUCTA: "come B Q4 ≥ 50" (la letra de la batería) · (ii) mundo vivo con `invertir_vivo_en = 50 000`, brazo VIVO de `mini_vivo` (sin reproducción), pareado ON/OFF | (i) **121–140** · (ii) **321–340** | (i) ≥ 18/20 · (ii) A₁₂(ON > OFF) ≥ 0.75 en `rev = mord[B][Q4] − mord[A][Q4]` (come la comida nueva, evita el veneno nuevo) | se mide |
| **T-D sin alias** | bloque de la sal con `organismo_vivo_relevo` (`corre_sal.BASE`, sal muda), 9 ALIAS + 9 LIMPIAS, brazos OFF / v15f / v15g | las 9 ALIAS y 9 LIMPIAS del bloque (301–700 estructurales) | C1 ALIAS `|W[sal]| ≤ 0.3` ≥ 8/9 (mediana ≤ 0.1) · C2 ALIAS `W_hambre[veneno] ≤ −2.8` ≥ 8/9 y ≤ −2.5 9/9 · C6 LIMPIAS `|W[sal]| ≤ 0.3` y `W_hambre[veneno] ≤ −2.8` 9/9 y 9/9 | se mide |
| **T-E no regresión conductual** | examen v3′ del candidato (`bateria_v15f.py 20 --desde 121`) contra el del tronco (`bateria_v14.py 20 --desde 121`), pareado por semilla | **121–140** | por escenario ≥ 18/20 (definición en §4) | se mide |
| **T-F coste** | examen: celdas, divisiones, muertes (medianas sobre las seis etapas) contra el tronco; mundo vivo: con T-A | 121–140; 301–320 | ≤ 1.25 × tronco | examen se mide; vivo con T-A |
| **T-G capacidad nueva** | **xor01 estricta con 8 ejemplos** (`corre_v15f.py --desde 181`, kwargs del tronco, pareado ON/OFF) | **181–200** | xor01 estricta ≥ 0.75, azar ∈ [0.35, 0.65], px0 ≥ apagada | **se cierra con la síntesis de la sala 2; NO se mide antes** |

## 4. T-E: la conducta por escenario, definida ahora y por qué

Pareado por semilla con el tronco v14.1 en 121–140; una semilla cuenta si cumple TODAS las cláusulas de su escenario; puerta = ≥ 18/20 en
cada escenario. Tolerancia **1.10** en los conteos (los flujos divergen desde la primera mordida distinta y un conteo de ~50 tiene ±10 %
de ruido; T-F usa 1.25 para el coste).

- **E1:** (a) **mordidas totales de veneno (B, Q1–Q4) ≤ 1.10 × tronco**; (b) comida comida en Q4 (A) ≥ 0.8 × tronco. **Por qué (a) y no
  "tasa Q4 ≤ tronco":** "veneno Q4 < Q1" era un proxy de *deja de morder*; un organismo que aprende el veneno en una mordida tiene Q1 ≈ Q4
  ≈ pequeño por construcción y la tasa Q4 sola dejaría pasar a uno que muerde mucho en Q1–Q3. El total mide lo que la misión pide —
  *aprender sin morder de más* — y contiene a la tasa Q4. Los pesos (W_B ≈ −3) se reportan, no son puerta.
- **E2:** (a) "come B Q4 ≥ 50" (T-C); (b) mordidas de A en Q4 ≤ 1.10 × tronco (evita el veneno nuevo).
- **E2I:** (a) mordidas totales de C (veneno nuevo) ≤ 1.10 × tronco; (b) `tasaA Q4 ≥ 80 % Q2` (la cláusula conductual de la batería).
- **E2J / E2K:** (a) come D (comida nueva) en Q4 ≥ 0.8 × tronco; (b) mordidas totales de B ≤ 1.10 × tronco.
- **E2L:** (a) mordidas totales de B ≤ 1.10 × tronco; (b) come A en Q4 ≥ 0.8 × tronco.

## 5. Predicción numérica (para poder equivocarme)

- **T-B pasa:** G1 1.000 (azar 0.40–0.60), G2 ≥ 0.97, K 20/20 (dos series previas de v15f/v15c con R crudo: 1.000 / 0.997–0.998).
- **T-C (i) pasa 20/20** (v15f: 20/20 en 101–120); **(ii) pasa:** con la tabla, tras el intercambio la primera mordida de B (ahora +1)
  sobrescribe la casilla y la boca lee +1; v14.1 necesita ~4 mordidas de la lineal y la puerta cerrada: A₁₂ **0.80–0.95**.
- **T-D: v15f NO pasa C1/C2** (|W[sal]| ≈ 1.45, W[veneno] ≈ −1.45 en ≥ 7/9 ALIAS: la puerta lee la rápida del código compartido);
  **C6 pasa 9/9** (en limpias la tabla y la rápida coinciden). **v15g (exploratorio) pasa C1 ≥ 8/9 (|W[sal]| 0.0 exacto), C2 ≥ 8/9
  (−3.0 exacto), C6 9/9.** Lo que me refuta aquí: v15f con C1 ≥ 8/9 (entonces la puerta se cierra sola en el alias y no entiendo por
  qué) o v15g con C1 < 8/9 (la casilla ganadora no separa sal de veneno: colisión de casilla en algún par).
- **T-E:** E1 ≥ 18/20 (humo de v15f: 41–45 mordidas de veneno contra 47–51 de v14.1), E2 20/20, E2I 18–20/20 (riesgo: la semilla de
  W_C ≤ −2.5 17/20 era de pesos, la conducta tasa A fue 20/20), E2J/E2K/E2L ≥ 19/20.
- **T-F (examen):** celdas ≤ 1.10 ×, divisiones **≤ 1.20 ×** (v15f xor01 +16 %; declaro que puedo pasar de 1.10 pero no de 1.25),
  muertes ≤ 1.10 ×.
- **T-A y T-G:** no se predicen números hasta la síntesis de la sala 2 (la letra puede cambiar); lo que espero, dicho: T-G como en
  161–180 (1.000 estricta); T-A muertes ≈ tronco (la tabla ahorra mordidas de veneno; la reproducción no se toca).
- **Veredicto esperado:** v15f **cae en T-D** (C1/C2) por el orden de las puertas → **no entra**; v15g queda como candidato con preregistro
  propio si sus C1/C2/C6 salen como predigo. Si v15f pasa T-D, el candidato es v15f y v15g no hace falta.

## 6. Cláusula

Una sola puerta caída → no entra (regla 2 de v2), sin modos intermedios; `mem_alfa = 1.0`, `mem_rho = 0.02`, tolerancias 1.10/0.8 de
§4 y `invertir_vivo_en = 50 000` quedan fijados aquí. T-A y T-G se miden sólo después de la síntesis de la sala 2, con la letra que
ésta fije (si cambia la de aquí, ERR con fecha). Todo cambio de umbral tras ver datos lleva ERR (libres desde ERR-45; los numera
el coordinador). Semillas: 121–140 (T-B, T-C i, T-E, T-F examen), 321–340 (T-C ii), ALIAS/LIMPIAS del bloque de la sal (T-D),
301–320 (T-A), 181–200 (T-G).

## 7. Humo (UN proceso, T ≤ 200 000, ≤ 3 semillas, sin Pool) — medido DESPUÉS de escribir §1–§6

`corre_v15f_v2.py --humo`: (a) identidad corta; (b) semilla ALIAS **326** con sal muda: apagada / v15f / v15g (|W[sal]|, W[veneno],
exposiciones, celdas); (c) mundo vivo brazo VIVO de rep2, semilla **301**: apagada / v15f / v15g (r = descendientes − muertes, muertes,
exposiciones); (d) reversión en el mundo vivo, semilla **321**, `invertir_vivo_en = 50 000`: apagada / v15f (`rev`, mordidas de A y B en
Q4). Los números se pegan aquí abajo cuando existan, con su sha, y en el PUENTE (A18).
