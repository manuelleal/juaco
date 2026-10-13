# VEREDICTO — entrada del registro

Copiada de `registro/REGISTRO_etapas_1_2.md`, líneas 3251–3271.

---

### Bloque 2 (día 6): curiosidad por progreso de error contra el canje del mapa — **REFUTADA: no devuelve la exploración**

Preregistro `experimentos/nivel8_curiosidad/PREREGISTRO_curiosidad.md`; instrumento `mundo_largo_c.py` (`4a24460f504f003e`,
`gamma_C = 0` ≡ `mundo_largo`, identidad 3/3 con el mundo completo); datos `curiosidad_s41-60_20260917_211739`
(`b23a85f7695c6ee8`), semillas 41–60. Dos arranques previos se abortaron sin datos por un `KeyError` de mi runner
(registrado en el commit `d4367e0`).

| brazo | adquisición (≤ 30 vistos) | final | retención nunca invertidos | comida Q4 | muertes | celdas |
|---|---|---|---|---|---|---|
| V13 | **0.900** | 0.800 | 0.67 | 837 | 30 | 90 |
| MAPA | 0.704 | 0.700 | 0.67 | 968 | 26 | 84 |
| **MAPA + curiosidad** | **0.700** | 0.600 | 0.83 | 974 | 22 | 77 |
| MAPA + curiosidad barajada | 0.700 | 0.700 | 0.83 | 968 | 28 | 81 |

P1 NO (0.700; > MAPA en 7/20), P2 OK (comida 974, 19/20), P3 NO (curiosidad = barajada, 6/20). **La curiosidad por
progreso del error no explora**: el sesgo actúa sólo sobre sitios recordados, y lo nuevo entra en sitios cuyo progreso
es cero hasta la primera mordida (la refutación ya escrita en el preregistro). Observación: la retención de lo ausente
sube a 0.83 con curiosidad (0.67 sin) — **la curiosidad aprende qué sitios proteger**: es un efecto del progreso del
error, no del sesgo. **Siguiente candidato, ya escrito antes:** *novedad de sitio* (sesgo hacia el sitio que lleva más
tiempo sin visitarse), no otra perilla de esta. Vocabulario: *el canje exploración / explotación del mapa sigue
abierto*.
