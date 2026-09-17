# Re-verificación sobre el tronco v13: composición temporal (3T) y capacidad (mundo grande)

**Escrito ANTES de construir los instrumentos y antes de correr. 17 sep 2026, día 5.** Dirección: *"A darle"*.
Obligación declarada al congelar v13: *"3T y capacidad: medidos sólo sobre v11, pendientes sobre v13; obligatorios
antes de decir que todo sobrevive"*.

## 0. Qué se sabe

- Sobre v11: 3T `sep`(C3) +3.96, `lift_q4` +0.388, `solap_A` 0, 6 divisiones; control C3C −0.36. Capacidad en el mundo
  grande (10 px, 60 estímulos): `N*` 43.5 (20k) y 50.0 (60k), `M_max` 28.5 y 32.0.
- v13 añade a v11 una vía lenta **lineal sobre la entrada** y una puerta de familiaridad (3 de 3 celdas consolidadas).
  Ninguna de las dos toca la vía rápida: con `eta_s = 0, puerta = None` es v11 exacto.

## 1. Instrumentos (anclas; orígenes por sha; con las perillas apagadas son sus orígenes EXACTOS)

- `mundo_temporal_v13.py` ← `mundo_temporal_v11.py` (`807f4b357f9eac1a`) + `eta_s`, `puerta`, `clip_s`. La vía lenta lee
  la entrada **completa del mundo temporal** (`NIN` = 6 ó 12 dimensiones: visible + columnas temporales). Toda lectura de
  valor (`W` de las situaciones `A|A`, `A|B`, etc., `sep`, `lift`) pasa a ser el valor total que usa la boca.
- `organismo_capD13.py` ← `organismo_capD.py` (`85afad3f0769891f`) + `eta_s`, `puerta`, `clip_s`. La lenta lee los `D`
  píxeles de la retina. `W` de cada estímulo en cada checkpoint = valor total.
- **Controles de inercia (si fallan, se para):** `mundo_temporal_v13(eta_s=0, puerta=None)` ≡ `mundo_temporal_v11` (6
  brazos × semillas 1–3, todas las claves); `capD13(eta_s=0, puerta=None)` ≡ `capD` (2 semillas × plan corto de 6 y
  mundo grande de 20 estímulos con paso 3.000, todas las claves).

## 2. Criterios

### 3T (semillas 41–60; brazos `v11` = perillas apagadas, `v13` = `eta_s=0.015, puerta=3`, en los 6 arms)
- **KT2:** C2b ≡ C1 bajo v13, 20/20 (las columnas temporales a cero no cambian nada).
- **T1:** `C3`(v13) `solap_A` mediana ≤ 1 y ≤ 1 en ≥ 15/20. **T2:** `sep` mediana ≥ 1.0. **T3:** `lift_q4` ≥ 0.15.
  **T4:** `C3C`(v13) `sep` < 1.0 **y** `lift_q4` < 0.15.
- **T5 [no-inferioridad]:** `sep`(C3, v13) ≥ `sep`(C3, v11) − 1.0.
- **T6 [la lenta no resuelve 3T por otra puerta]:** `C2b`(v13) —columnas temporales a cero, sin plasticidad— tiene
  `sep` < 1.0 (la lenta no puede leer un canal que está a cero). Y **C1p**(v13) (NIN = 6, sin canal temporal, con
  plasticidad) `sep` < 1.0.

### Capacidad (mundo grande: 10 px, 60 estímulos de peso 3; semillas 41–60; `paso_t` ∈ {20k, 60k})
- **K1:** `W = 0.000` exacto en ≤ 5 % de los valores finales (v13, 20k).
- **K2 [no-inferioridad]:** mediana `M_max`(v13) ≥ mediana `M_max`(v11) − 3, en los dos pasos.
- **K3 [no-inferioridad]:** mediana `N*`(v13) ≥ mediana `N*`(v11) − 5, en los dos pasos.
- Sin voto: agotamiento, celdas, divisiones, muertes, y **cuántos estímulos vivos son "no familiares"** al final (van a la
  lenta).

## 3. Predicciones (con número, antes)

- **3T sobrevive:** T1–T5 se sostienen; `sep`(C3, v13) entre 3.0 y 4.5. **T6 se sostiene** (C2b y C1p < 1.0).
  *Razón:* la composición temporal vive en la vía rápida (códigos Kenyon), que v13 no toca; A|A y A|B son familiares y la
  puerta elige la rápida.
- **Capacidad: riesgo real, declarado.** En un mundo con 60 estímulos y 90 celdas, los estímulos tardíos tienen códigos
  con **menos de 3 celdas consolidadas** → la puerta los manda a la **lenta**, que es lineal y **no puede** ajustar 60
  valencias alternadas → su valor será malo → `N*` y `M_max` **caen**. *Predicción:* K1 se sostiene; **K2 y K3 pueden
  fallar** (`N*`(v13) 25–40 frente a 43.5–50 de v11). Si fallan, es el **precio de la puerta en mundos abarrotados**, se
  registra como tal, y se anota la salida obvia (una puerta que exija 2 de 3, o que consulte la lenta sólo cuando la
  rápida esté vacía) para preregistrar después. **No se recalibra aquí.**

## 4. Qué se decide

- **Todo se sostiene:** se escribe "3T y capacidad sobreviven sobre v13"; el tronco queda completo.
- **Falla 3T (T1–T5):** v13 sigue de tronco (se congeló por otros criterios), pero el registro y `CLAUDE.md` llevan la
  advertencia y la composición temporal vuelve a ser pendiente.
- **Falla capacidad (K2/K3):** ídem; se registra el canje nuevo ("puerta contra capacidad") y su magnitud.
- **Falla inercia:** se para y se arregla el instrumento.
