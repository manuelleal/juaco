# VEREDICTO — entrada del registro

Copiada de `registro/REGISTRO_etapas_1_2.md`, líneas 2003–2041.

---

### RE-VERIFICACIÓN sobre v9 — 3T y 2K-bis: **los dos sobreviven**

**Procedencia**
- Preregistro `experimentos/v9_reverificacion/PREREGISTRO_reverificacion_v9.md` (`2708cb73ab8531e8`, commit
  `fb8a155`). Instrumentos commiteados antes de correr (`dd08056`): `mundo_temporal_v9.py` `18d96a1c79863bb0` y
  `organismo_caph9.py` `1b113605dc803435`.
- Datos: `datos/reverificacion_v9_20260916_165658.json` (`111e25284b7b0e6d`) y `.log`.

**Controles:** KT1 18/18 (`memoria=0` ≡ `mundo_temporal_v8`); KK1 12/12 (`memoria=0` ≡ `caph`); KT2 C2b ≡ C1 20/20;
**KK2 reproduce N\* y M_max de v8 guardados, 20/20**.

**3T sobre v9 — T1–T4 SOSTENIDAS.**

| brazo | sep | lift_q4 | solap_A | divisiones |
|---|---|---|---|---|
| **C3** | **+3.93** [3.72, 3.97] | **+0.383** | 1 | 17 |
| C3C | −0.37 [−1.84, +1.11] | −0.043 | 0 | 60 (agota el pool 20/20) |

- En v8, C3 daba `lift_q4` +0.341; con v9 la conducta de composición **mejora ligeramente** (sin voto).
- 0 truncaciones en todos los brazos.

**2K-bis sobre v9 — K1–K3 SOSTENIDAS.**

| | N\* | M_max | W=0 exacto | agotan | muertes |
|---|---|---|---|---|---|
| 20k v8 | 5.0 | 8.0 | 0/400 | 5/20 | 564 |
| 20k **v9** | 5.0 | 8.0 | 0/400 | 4/20 | **514** |
| 60k v8 | 8.0 | 12.0 | 0/400 | 15/20 | 1.650 |
| 60k **v9** | 8.0 | 11.5 | 0/400 | 11/20 | **1.521** |

**Dicho con honestidad (sin voto):** pareado, M_max baja algo con v9.
- a 20k: mediana −0.5 (sube en 6 semillas, baja en 10);
- a 60k: mediana −1.0 (sube en 7, baja en 12).

Queda **dentro** de la tolerancia preregistrada (−1), pero la dirección es de coste pequeño. A cambio, **muere menos**:
−50 (bajan 16/20) y −131.5 (bajan 17/20).

**Lectura.** La composición temporal y la corrección de 2K-bis **valen sobre el tronco v9**. La memoria de rechazo
cambia a dónde van las patas y cuesta, quizá, una fracción de estímulo en capacidad útil, a cambio de supervivencia.
