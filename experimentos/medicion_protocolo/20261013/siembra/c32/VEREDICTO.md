# VEREDICTO — entrada del registro

Copiada de `registro/REGISTRO_etapas_1_2.md`, líneas 1675–1716.

---

### FRONTERA HAMBRE–SUPERVIVENCIA — CORRIDA. No pasa como estaba escrita, y cambia el problema de la Etapa 2

**Procedencia.** Instrumentos commiteados antes (`e30ea03`). Script `corre_frontera_hambre.py`. Datos
`datos/frontera_hambre_20260916_153342.json` (`88007765123c94c3`), `.csv` (`348a445324f05521`) y `.log`.
280 corridas más 42 controles.

| hb | muertes E1 | muertes E2 | combinado | E2 revierte | veneno E1, 2ª mitad | comida E1, 2ª mitad |
|---|---|---|---|---|---|---|
| 0.0 | 156 | 208.5 | 364.5 | 0/20 | 2 | 129 |
| 0.5 | 154 | 184 | 338 | 0/20 | 3.5 | 140.5 |
| 1.0 | 151 | 161.5 | 312.5 | **10/20** | 5.5 | 138.5 |
| 1.5 | 149.5 | 155 | 304.5 | 19/20 | 10.5 | 137.5 |
| **2.0 (v8)** | **142** | 146.5 | **288.5** | 20/20 | 27 | 150.5 |
| 2.5 | 148 | 146 | 294 | 20/20 | 59 | 180 |
| 3.0 | 155.5 | 156.5 | 312 | 20/20 | 88.5 | 195.5 |

| criterio | veredicto | cifra |
|---|---|---|
| F0a / F0b instrumento | OK | 42/42 · reproduce el examen de v8 40/40 |
| F1 contador | **REFUTADA** (ERR-14, ver abajo) | 49/51 celdas en banda |
| F2 umbral de reversibilidad | **REFUTADA** | con `hb = 1` revierten **10/20**; predije ≤5 |
| F3 sin exploración se muere en E2 | **REFUTADA** | ×1.10 con `hb = 1`, predije ≥1.5 (con `hb = 0`: ×1.42) |
| F4 en E1 la exploración cuesta poco | **SOSTENIDA, pero por la razón equivocada** | muertes **+9.9%** con `hb = 0`: **suben**, no bajan. Pasó por la banda de ±10% |
| F5 v8 en el óptimo combinado | **SOSTENIDA** | el mínimo está **exactamente** en `hb = 2.0` |
| F6 demasiada exploración mata | **REFUTADA por margen** | ×1.095, predije ≥1.10 |

**Lo que sí se sostiene (lo cualitativo).**
- **Sin exploración no hay reversión:** 0/20 con `hb ≤ 0.5`.
- **v8 está en el óptimo medido** de supervivencia combinada, y también en el de E1 solo.

**Lo que salió mal en mis predicciones.**
- El umbral de reversión es más bajo de lo que estimé (50% con `hb = 1`).
- El efecto de morir de hambre en E2 es más débil. Medido por mitades: la segunda mitad pasa de 74 a 86.5 muertes
  con `hb = 1` (×1.17) y a 129 con `hb = 0` (×1.74).
- **Y en un mundo estable, quitar la exploración NO reduce las muertes: las AUMENTA.** Razoné lo contrario.

**ERR-14 — la banda de validación de F1 era más estrecha que el ruido de Poisson.**
- Con ≥20 mordidas esperadas, la desviación típica de Poisson es ~±22%, y la banda [0.8, 1.25] es ≈ ±1σ.
- Calculado: **1.56 celdas fuera de banda esperadas sólo por azar; observadas 2**. P(fuera | 21.5) = 0.34 y
  P(fuera | 25.3) = 0.28.
- **El contador está bien; el criterio no.** Es un criterio de validación escrito sin el ruido de muestreo. No
  produjo ningún dato falso. Se numera porque decidió un veredicto.
