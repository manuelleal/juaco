# Etapa 5, N3 (sentidos complementarios) = experimento 3 del plan: ¿acierta un organismo ciego a la regla usando la conducta de otro que la ve?

**Escrito ANTES de construir el instrumento y ANTES de correr. 17 sep 2026, noche del día 5.** Tercer experimento del
plan del debate (`DEBATE_y_plan_5a10.md` §3, punto 3: "`mundo_social` (nivel5 §7) con un control de saciedad añadido").
Regla 12.

## 0. Qué cambia respecto de la propuesta de nivel 5 §7, y por qué

- La propuesta usa la regla no lineal (XOR) repartida entre dos mitades. **No sirve como primera prueba:** con XOR entre
  un píxel de cada mitad, la conducta de cada uno sobre su media retina es *por construcción* no informativa (para cada
  vista propia, la mitad de los patrones es comida), así que la señal de conducta no puede portar el bit que falta;
  fallaría sin decir nada sobre transferencia. Se empieza por la **regla lineal `px0`** (comida si el píxel 0 está
  activo), con el **emisor viendo los píxeles 0–2** (resuelve la regla solo, como el techo) y el **receptor viendo los
  píxeles 3–5** (ciego al píxel que decide). XOR queda para después, si esto pasa.
- El canal de N1 sólo *entrena* el valor del receptor (Rescorla–Wagner vicario). Un receptor ciego a la regla no puede
  aprender nada útil sobre *su* vista: la información ajena tiene que entrar **en la decisión**, como ya hizo el símbolo
  en N2b (`gamma_sim`). Nuevo knob `gamma_soc`: la última señal honesta oída sobre el patrón `kk` (dentro de `tau_soc`
  pasos) sesga el valor que usa la boca: `_wt += gamma_soc · signo`. Sólo la decisión; el aprendizaje sigue sobre el
  valor propio. Con `gamma_soc = 0` el instrumento es `mundo_social` exacto.
- **Advertencia escrita antes de correr:** con patrones de peso 3, la vista 3–5 del receptor **sí** lleva información
  parcial de `px0` (si ve tres píxeles activos, `px0 = 0`; si ve uno, `px0 = 1` con probabilidad 2/3). Predicción:
  SOLO_R entre 0.55 y 0.70 por ese sesgo estadístico, **no** 0.50. Por eso los criterios son **pareados** contra SOLO_R.
- **Control de saciedad (el que pidió el debate):** SACIEDAD = misma pareja y misma señal, pero el emisor tiene
  `alpha = 0` (su boca ignora el valor: muerde por hambre). Su señal dice "alguien mordió/rechazó aquí" sin saber nada.
  Si el receptor mejora igual con ese emisor, la mejora es un artefacto de saciedad/presencia, no transferencia.

## 1. Instrumento `mundo_social_n3.py` (desde `mundo_social.py` `946ff1c71e375eba`, por anclas)

`Organismo(..., gamma_soc=0.0, tau_soc=400)`; `recibir()` guarda `s_ult[kk] = (±1, t)`; la boca suma
`gamma_soc · signo` si `t − t_oído ≤ tau_soc` (contador `n_sesgo_soc`). `run(..., mascaras=None, kw_por_org=None)`:
cada organismo recibe sus patrones **enmascarados** (`pats · máscara`) y sus kwargs propios. Identidad obligatoria:
`gamma_soc = 0`, sin máscaras ≡ `mundo_social` (n = 1 y n = 2 con señal `conducta`), todas las claves, semillas 1–3.

## 2. Condiciones (semillas 1–20; mundo `regla`, `px0`, T = 200 000, `d_senal = 5`, `f_vicaria = 1/3`, `gamma_soc = 1.5`)

| condición | organismos | señal | qué prueba |
|---|---|---|---|
| TECHO | 1, retina completa | — | la regla se aprende (referencia) |
| SOLO_E | 1, ve 0–2 | — | el emisor la resuelve solo |
| SOLO_R | 1, ve 3–5 | — | el receptor solo (sesgo parcial esperado) |
| N0 | 2 (R ve 3–5, E ve 0–2) | ninguna | presencia sin señal |
| CONV | 2 | `conducta` honesta + `gamma_soc` | **la pregunta** |
| SHUF | 2 | `barajada_conducta` + `gamma_soc` | misma cantidad de señal, sin contenido |
| SACIEDAD | 2, emisor con `alpha = 0` | `conducta` honesta + `gamma_soc` | señal de un emisor que no sabe |

Medida principal, en el receptor (organismo 0) y en el último cuarto: **acierto conductual** = (comida mordida + veneno
rechazado) / visitas; también veneno mordido, muertes, `n_sesgo_soc`, señales recibidas.

## 3. Criterios y predicción

- **S1:** CONV acierto mediana ≥ **0.80** y CONV > SOLO_R pareado en ≥ 15/20. **S2:** CONV > SHUF pareado ≥ 15/20.
  **S3:** CONV > SACIEDAD pareado ≥ 15/20. **S4 (validez):** SOLO_R ≤ 0.75 y TECHO ≥ 0.80 y SOLO_E ≥ 0.80 (si no, el
  montaje no deja sitio para medir). **S5:** N0 no supera a SOLO_R en ≥ 15/20 (la presencia sola no ayuda).
- **Predicción:** S1–S5 pasan → "*transferencia entre sensores por conducta*: el ciego a la regla acierta con la conducta
  reciente del que la ve" (nivel 5; N3 en su forma mínima). Réplica en 21–40 antes de cerrar. **Refutación:** S1, S2 o
  S3 falla. Si S3 falla (SACIEDAD ayuda igual): la mejora no es transferencia de conocimiento, se registra como artefacto
  y no se declara nada. Nada se recalibra después de ver datos.
- Coste: 7 condiciones × 20 semillas = 140 corridas de 200 000 (dos organismos en 4): ~5–6 min.
