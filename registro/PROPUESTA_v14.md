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
