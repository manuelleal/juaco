# v14 CONGELADO (18 sep 2026, 05:05) = v13 + hija dispersa por relevancia + puerta por evidencia del código — este documento fue la propuesta; la decisión está al final y en REGISTRO_etapas_1_2.md

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
`s̄_E` la sorpresa de ΔE promediada; no toca `eta` (donde el bloque 6 la puso y no servía: 0.856×). Examen v3'' completo en
101–120 (v13E, 02:45): retención 8/8, pero G1 px0 0.750 < 0.80 a la dosis `k_testE = 10` → fuera a esa dosis. **Bloque de dosis
(03:32, preregistrado): `k_testE = 5` cumple las seis condiciones a la vez — recuperación 0.267× (20/20, semillas nuevas 121–140),
se apaga 20/20, G1 0.80 (17/20), G2 0.857, K 20/20, examen v3'' 8/8 → REINSTALADO como segundo candidato a dosis 5** (copia
`organismo/organismo_v14_candidato_sorpresa.py` = `organismo_v13E_k5.py` en la rama `v14-candidato`). k = 3 no (G2 0.842, examen 7/8).
**Réplica en 141–160 (04:05): 0.248× (20/20), se apaga 20/20, retención 20/20 × 6, G1 0.80 = v13, G2 0.89 → dos series a dosis 5.**
Falta si se acepta: gemelo, congelación.
**Los dos candidatos son componibles** (uno actúa en el nacimiento de las hijas, el otro en la boca); si el director acepta
ambos, se prueba primero la composición (identidad de cada uno con el otro apagado; examen v3' con los dos encendidos).


## Tercer candidato, condicionado (02:40): puerta de familiaridad por evidencia del código exacto (PATC = código ∧ 1 celda)

Capacidad: `N*` 50.5 (= v11) contra 35 de v13 en el paso largo; 41.5 contra 28 en el corto (umbral 45 no alcanzado). Generalización
intacta (px0 1.000, G2 0.96); barajar los contadores destruye la ganancia (20/20). Examen v3': todo pasa salvo **E2 19/20** (una
semilla, subcriterio conductual `come B Q4 ≥ 50`). **Condición CUMPLIDA (02:41):** réplica del examen v3' en 121–140 con la misma letra → **8/8** (E2 20/20; 39/40 en dos
series). Entra a la propuesta como tercer candidato (copia en la rama `v14-candidato`:
`organismo/organismo_v14_candidato_puerta.py` = `experimentos/nivel4_puerta_codigo/organismo_v13Bn5c.py`). Datos `puerta_codigo_s41-60_20260918_013618`. Componible con los otros dos
(actúa en el ruteo, no en el aprendizaje ni en la boca).


## Composición de los candidatos (03:55): por la letra NO se proponen juntos todavía; réplica del examen compuesto en curso

Con hija dispersa + puerta por código ON a la vez: examen 7/8 (E2 19/20 en 101–120, la misma semilla-subcriterio que PATC solo);
generalización G1 1.000 / G2 0.94 (mejor que cualquiera solo); capacidad `N*` 51 (v13 35); composición 3T-k lift 0.237 (hija sola
0.251; v13 0.137) con 53 celdas. Enmienda 1: réplica del examen compuesto en 121–140 → **8/8 (04:03; E2 20/20). PROPUESTA CONJUNTA: v14 = v13 + hija dispersa +
puerta por evidencia del código** (`organismo/organismo_v14_candidato_conjunto.py` en la rama `v14-candidato`; C3 registrado tal cual:
0.237 con 53 celdas, la puerta resta 0.014 a la hija sola). **Protección extra (04:22): examen 8/8 también en 141–160 y generalización 1.000 / 0.95 en 121–140 → dos series 8/8 propias y dos
de generalización.** La sorpresa en la boca a dosis 5 va aparte hasta medir la composición de los tres (paquete en preparación).
Datos `composicion_v14_20260918_033225`, `examen_v14c_20260918_035946`, `examen_v14c_20260918_041824`,
`regresion_generaliza_organismo_v14c_on_20260918_042128`.


## DECISIÓN (18 sep 2026, 04:55 → 04:50 resultado de los tres): **v14 = v13 + hija dispersa + puerta por código**

Composición de los tres (04:47): T1 8/8 en 101–120 pero 7/8 en la réplica 121–140 (E2, semilla 133, 42 bocados); T2 1.000 / 0.93;
T3 0.24×. Por la cláusula y la decisión del director ("los tres si pasan; si no, los dos"), **v14 lleva los dos primeros**; la
sorpresa del mundo en la boca (dosis 5) es **candidata a v15** con su composición ya medida (T2/T3 OK). Congelación de v14 en curso:
tercer examen en rango virgen 161–180 + generalización 141–160, gemelo compilado, manifiesto, tag.


## Candidato v15c (18 sep 08:06; enmendado 08:46, ERR-38): NO entra — superado por v15d; su G1 0.500 era del instrumento (batería corregida: G1 1.000 / G2 0.997)
Queda como órgano del mundo de regla (xor01 0.81 estricta). Su V1 nunca se midió con la perilla encendida.

## Candidato v15d (18 sep 08:38; V2a corregida 08:46): NO entra — el EXAMEN cae por REVERSIÓN (E2 0/20: la tabla de un golpe no se desdice; E1 0/20: la vía rápida no consolida), aunque conserva la generalización lineal (G1 1.000 / G2 0.999) y cruza XOR con 8 ejemplos (0.875 estricta); coste −18 % en celdas
Vocabulario: "la memoria de pares generaliza y cruza XOR con 8 ejemplos, pero no se desdice". Siguiente candidato con preregistro nuevo: tabla reescribible (v15e). Detalle en `REGISTRO_etapas_1_2.md` (ERR-38 y v15d).
