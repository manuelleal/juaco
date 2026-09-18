# PREREGISTRO — A-3: la vía lenta de v13 es, exactamente, UN vector con signo

**Borrador del CREADOR A. Escrito el 18-sep-2026, ANTES de la serie de 20 semillas.** El humo (1 semilla, un proceso)
ya está corrido y sus números están en §6; la serie **no**.

## 1. De dónde sale (álgebra, no intuición)

Por celda o rasgo, con `W = Wp − Wn` y `m = min(Wp, Wn)`, la aplicación `(Wp,Wn) ↔ (W,m)` es una **biyección** del
cuadrante (`Wp = m + W⁺`, `Wn = m + W⁻`). En esas coordenadas la regla de v13 es exactamente:

- **drenaje** `Wp,Wn −= lam·min(Wp,Wn)` ⟺ `m ← (1−lam)·m`, **`W` sin cambio** → *el drenaje no toca el valor*;
- **refuerzo/castigo** ⟺ `W ← W ± min(η·|g(δ)|, C − m − W^∓)` → *el tope actúa sobre `W` como `|W| ≤ C − m`*;
- **fisión de v11** ⟺ la hija se lleva exactamente `m` y la madre queda con `W ∓ m`.

**Consecuencia:** con `aversion = 1.0` (el valor de todos los experimentos del tronco) y mientras **ningún canal
toque `clip_s`**, la vía lenta de dos canales con drenaje **es** la regla delta sobre un solo vector con signo. La vía
**rápida** no: su fisión lee `m`, y ahí el segundo número por celda tiene trabajo.
Comprobación previa (`dos_canales_es_valor_mas_conflicto.py`): conduciendo las dos parametrizaciones con la misma
secuencia de 200 000 deltas, `max|ΔW| = 2.5e−14`. En 9 corridas reales del mundo de regla, `n_techo = 0`,
`max(Wps) ≤ 2.55`, `max(Wns) ≤ 2.30`, `m ≤ 0.24`.

## 2. Hipótesis

**HA3.** En el montaje de generalización del tronco, `DOS_CANALES` y `VECTOR_UNICO` dan resultados **idénticos**
semilla a semilla, y la vía lenta del tronco puede escribirse con **la mitad de estado** sin perder nada.

## 3. Mundo, instrumento, brazos

- Instrumento: `organismo_v13q3.py` (`aaebe073308a40c2`), **sin tocarlo** — las dos parametrizaciones ya son perillas.
- Montaje: el de `organismo/bateria_generaliza.py` (mundo de regla, `lectura='lineal'`, T = 200 000, sonda a priori
  en T/2, reglas `px0` y `azar`, criterios **G1/G2/K con sus umbrales sin tocar**), más `xor01` como lectura extra.
- Brazos (único cambio entre ellos):

| brazo | perillas | qué es |
|---|---|---|
| `DOS_CANALES` | `regla_lenta='dos_canales'`, `constante=False` | la vía lenta del tronco v13, sin tocar |
| `VECTOR_UNICO` | `regla_lenta='delta_signo'`, `lam_lenta=0.0`, `constante=False` | un solo vector con signo, sin decaimiento |

- Semillas **101–120** (las mismas de la batería de congelación de v13, para poder cruzar los números).
- **ETAPA 1 obligatoria, se para si falla:** `organismo_v13q3(dos_canales, lineal)` == `organismo_v13q` en todas las
  claves del original (2 reglas × 3 semillas, T = 60 000).

## 4. Predicciones numéricas (antes de correr)

- **A1.** `acc` (G1) **idéntica semilla a semilla** en los dos brazos: 60/60 pareos (3 reglas × 20 semillas).
- **A2.** `max|ΔW_lenta|` (valor de la vía lenta en la sonda, sin redondear) **< 1e−9** en todos los pareos donde el
  tope no aprieta.
- **A3.** El tope **no aprieta nunca** en la vía lenta: `max(Wps, Wns) < clip_s = 3` en 60/60.
- **A4.** `n_techo` (tope de la vía **rápida**) **= 0** en las 120 corridas.
- **A5.** `VECTOR_UNICO` pasa **G1, G2 y K** exactamente igual que `DOS_CANALES` (los de v13: G1 px0 ≈ 0.80,
  G2 ≈ 0.89), y `celdas` y `splits` coinciden semilla a semilla.

## 5. Criterio de refutación y controles que pueden fallar

- **Se refuta** si A1 falla en cualquier pareo con el tope sin apretar: significaría que hay otra diferencia entre las
  dos parametrizaciones que el álgebra no ve.
- **Control 1 (el que más puede fallar): el tope.** Si en alguna semilla un canal alcanza `clip_s`, A2 y A3 caen y la
  equivalencia deja de valer **en esa semilla**. Entonces la predicción cambia de signo: el vector único tiene **más**
  rango (`|W| ≤ C` en vez de `C − m`), no menos, y **hay que medir la generalización, no suponerla**. Se reporta
  aparte, sin recalibrar.
- **Control 2: `aversion ≠ 1`.** Fuera del alcance de esta serie (todo el tronco usa 1.0), pero se declara: con
  `aversion ≠ 1` la equivalencia exige una ganancia asimétrica explícita en el vector único.
- **Control 3: la vía rápida.** Esta propuesta **no** toca los dos canales de la vía rápida. Si alguien los sustituye
  por un vector único, la fisión de v11 pierde `m` y la retención 20/20 puede caerse: no está probado aquí.

## 6. Humo ya corrido (1 semilla, un proceso, sin Pool, T = 60 000)

`python experimentos/creacion_A/corre_vector_unico.py --humo` → `datos/vector_unico_humo_20260918_000816.{log,json}`
(`0689e674666bbdfa`). Identidad del instrumento **2/2**.

| regla | acc `DOS_CANALES` | acc `VECTOR_UNICO` | `max\|ΔW_lenta\|` | `max\|ΔWs\|` | tope toca | celdas/splits |
|---|---|---|---|---|---|---|
| px0 | 0.600 | 0.600 | 8.9e−16 | 6.7e−16 | no | iguales |
| azar | 0.700 | 0.700 | 1.1e−15 | 6.7e−16 | no | iguales |
| xor01 | 0.312 | 0.312 | 2.2e−16 | 2.2e−16 | no | iguales |

`acc` igual 3/3; `max(Wps,Wns)` 0.49–2.07 < 3; `m` ≤ 0.23; `n_techo = 0` en las 6 corridas.

## 7. Coste

2 brazos × 3 reglas × 20 semillas = **120 corridas** de T = 200 000 + 6 de identidad. Con `Pool(14)`, minutos.

## 8. Qué se declara si pasa

*"El drenaje `lam` de la vía lenta no toca el valor: es la tasa de olvido de una masa de conflicto. La vía lenta del
tronco puede escribirse con un solo vector con signo, con la mitad del estado y sin cambiar ningún número. La vía
rápida no, porque la fisión de v11 lee esa masa de conflicto."* Y como corolario ya verificado: **queda demostrada
la ablación del Agente B en `PUENTE_xor`** (`lam_lenta=0` y `clip_s=10` no movían ni un decimal) — no fue casualidad.
