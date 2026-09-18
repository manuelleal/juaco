# Propuesta de v14 = v13 + hija dispersa por relevancia (18 sep 2026, 01:35; coordinador, director ausente)

**No es una decisión: es la propuesta con su evidencia, para que el director decida al volver.** `main` no cambia; el tronco
sigue siendo v13 (cc8b16b492d4d324). La rama `v14-candidato` contiene la copia lista (`organismo/organismo_v14_candidato.py`
= `experimentos/nivel7_hija_dispersa/organismo_v13Don.py`, 1dd131dc0298307d, generada por anclas desde v13 con la perilla ON).

## Qué cambia (una línea del nacimiento de v11)
La hija nace ciega a parte de los píxeles de `P`: `kj = clip(KW[c]·0.95 + paso·dist, 0, 5) · rel`, con `rel ⊊ (P > 0)` por
medias de `P` condicionadas al signo de R (`m̂p`, `m̂n`, EMA 0.05 con normalizador; `del_s`, `del_c` fijos). Memoria: dos
vectores `NIN` y dos escalares por celda. Nada global; nada por patrón.

## Evidencia (todo preregistrado, todo en `registro/REGISTRO_etapas_1_2.md`)
| qué | resultado | datos |
|---|---|---|
| composición a k = 4/5 (3T-k), serie 61–80 | lift 0.251 > v13 18/20; sep 3.09; celdas 48 vs 90; REL > máscara al azar 16/20; inercia k = 1 20/20; **ahorro 16/20** (cayó la letra, 18/20) | hija_dispersa_s61-80_20260918_000202 |
| réplica 81–100 | lift 0.352 > v13 19/20; sep 3.62; celdas 38 vs 90; REL > azar 16/20; **ahorro 19/20 (letra original)**; inercia 20/20 | hija_dispersa_s81-100_20260918_000954 |
| examen v3' completo en 101–120 (v13D, perilla ON) | **8/8** (E1–E2L 20/20; 3'' 20/20; 4a–4d) | baterias_v13D_20260918_012145 |
| generalización (v13D, perilla ON) | K 20/20; G1 px0 0.800 (19/20); G2 0.834 (19/20) | ídem |
| inercia en el tronco (D3) | divisiones 0 → 0, celdas 30 → 30, `W` idéntico 20/20 | ídem |
| identidad de la copia | perilla apagada ≡ v13: 16/16 | identidad_v13D.py |

Auditoría de la madrugada: ERR-26 (la enmienda 1 de la serie 61–80 rebajó un umbral sin ERR; inerte porque 81–100 pasó la
letra original). Muertes: REL 88–102 contra 78–79 de v13 en 3T-k (no era criterio; anotado).

## Qué falta si el director dice sí
1. Gemelo compilado `organismo_v14_rapido.py` con arnés de identidad bit a bit (regla 9).
2. Congelación: `manifiesto.py` (15 archivos), tag `v14-tronco`, `bateria_v14.py` = `bateria_v13D.py` renombrada.
3. Regla 1 (regresión) con v14 en los corredores que importan el tronco; los gemelos de mundo siguen sobre v13 hasta
   compilarse sobre v14.
4. Vocabulario: *"la hija que nace ciega a lo irrelevante compone historias más profundas con menos celdas"*; prohibido
   "aprende a ignorar", "atiende", "selecciona".

## Qué haría cambiar la propuesta
- Si el director prefiere la variante barata AZAR (memoria cero): fue peor que REL en 16/20 × 2; no se recomienda.
- Si quiere ver primero el techo de capacidad con v13D en el mundo grande (60 estímulos): es un bloque de 45 min con el
  montaje de `reverificacion_v13`; no se corrió esta noche.


## Segundo candidato (01:50): "la sorpresa del mundo en la boca" (v13 + predictor de ΔE del bloque 6 con `k_testE = 10`)

| qué | resultado | datos |
|---|---|---|
| recuperación tras la inversión, tres series (41–60, 61–80, 81–100) | **0.143× / 0.144× / 0.141×** de v13, pareado 20/20 × 3 | probar_si_mismo_s41-60_20260918_001756, _s61-80_20260918_003640, _s81-100_20260918_012715 |
| se apaga solo (P4' relativo) | 20/20 × 3 (41–60 retroactivo, ERR-27) | ídem |
| seguridad (veneno post ≤ 4×, muertes ≤ 1.5×) | OK × 3 | ídem |
| retención (seis etapas de `bateria_v13`, 81–100) | 20, 19, 20, 20, 20, 20 | probar_si_mismo_s81-100_20260918_012715 |
| generalización (81–100) | K 20/20; G1 px0 0.90 (azar 0.50); G2 0.85 | ídem |
| latencia del primer sesgo | 202 pasos, 1 bocado (el automodelo: 602, 1.5) | ídem |

Memoria: una lectura lineal `ΔE_pred` (retina + código) + un escalar de estado. Mecanismo: `Vb += k_testE · s̄_E`, con
`s̄_E` la sorpresa de ΔE promediada; no toca `eta` (donde el bloque 6 la puso y no servía: 0.856×). **Examen v3'' completo en
101–120 (v13E, 02:45): retención 8/8, pero G1 px0 0.750 < 0.80 (referencia 0.800) → por el preregistro NO entra tal cual:
coste de 0.05 en generalización de valor a la dosis `k_testE = 10`. Queda FUERA de la propuesta hasta un preregistro de dosis
(k_testE 3–5) que exija a la vez recuperación ≤ 0.60× y G1 ≥ 0.80.**
**Los dos candidatos son componibles** (uno actúa en el nacimiento de las hijas, el otro en la boca); si el director acepta
ambos, se prueba primero la composición (identidad de cada uno con el otro apagado; examen v3' con los dos encendidos).


## Tercer candidato, condicionado (02:40): puerta de familiaridad por evidencia del código exacto (PATC = código ∧ 1 celda)

Capacidad: `N*` 50.5 (= v11) contra 35 de v13 en el paso largo; 41.5 contra 28 en el corto (umbral 45 no alcanzado). Generalización
intacta (px0 1.000, G2 0.96); barajar los contadores destruye la ganancia (20/20). Examen v3': todo pasa salvo **E2 19/20** (una
semilla, subcriterio conductual `come B Q4 ≥ 50`). **Condición CUMPLIDA (02:41):** réplica del examen v3' en 121–140 con la misma letra → **8/8** (E2 20/20; 39/40 en dos
series). Entra a la propuesta como tercer candidato (copia en la rama `v14-candidato`:
`organismo/organismo_v14_candidato_puerta.py` = `experimentos/nivel4_puerta_codigo/organismo_v13Bn5c.py`). Datos `puerta_codigo_s41-60_20260918_013618`. Componible con los otros dos
(actúa en el ruteo, no en el aprendizaje ni en la boca).
