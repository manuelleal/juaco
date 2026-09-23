# INFORME N7-NL (creador del nivel 7, 23-sep-2026): una página

**Veredicto de lo hecho hoy: HAY ALGO MODESTO, sin serie.** Encontré una regresión que no estaba registrada y dejé
listo un candidato para repararla, con el arnés en verde. Nada de esto es dato todavía: la serie y la réplica
las corre el coordinador.

## Qué hice
1. Revisé la base del 70 %. Todo lo medido en 3T-k (v13 "hasta 3", la hija dispersa a k = 4/5 y v14c a k = 5)
   se corrió con **eta_s 0.015 y clip_s 3**. El tronco vigente v14.2 usa **eta_s 0.15, clip_s 10** (A-4) más
   B-5, y **nunca se midió en 3T-k**. Ninguna batería del tronco tiene 3T-k.
2. Mini-prueba (semillas 7798–7799, no son dato): el tronco tal cual **deja de morder** en 3T-k con k ≥ 3.
   Hace 6–15 mordidas en 100 000 pasos, muere 327–331 veces y el lift es 0 o None. Con k = 2 depende de la
   semilla (lift 0.0 en una, 0.395 en otra). La causa es la vía lenta sin normalizar: la masa de la entrada es
   3(k+1), y un solo veneno hunde el valor lento de todos los patrones.
3. Mecanismo mínimo **norm_lenta**: el paso de la vía lenta se multiplica por 3/(P·P). No añade memoria. La
   única constante es M0 = 3, y la fija el tronco. Es **inerte por construcción en los mundos del tronco**, y
   eso está verificado bit a bit.
4. Instrumentos construidos por anclas en `experimentos/subida_n7/`: `construye_n7.py`, `mundo_n7.py`,
   `organismo_v142N.py`, `organismo_v142gN.py`, `identidad_n7.py`, `corre_n7.py` y `PREREGISTRO_n7.md`.

## Arnés de identidad (`identidad_n7_salida.txt`), corrido antes de cualquier número
`(A) mundo_n7 apagado == mundo_composicion_v14 26/26 · (B) v142N(0) == v142 24/24 · (C) v142gN(0) == v142g 6/6 ·
(I) inercia con la perilla ENCENDIDA en los mundos del tronco 30/30 · (K) kwargs campo a campo 28/28 → PASA 114/114`

## Humo (1 proceso, semilla 7799, k = 2/5/8, 164 s)
`python experimentos/subida_n7/corre_n7.py --humo` → `experimentos/subida_n7/datos/humo/n7_humo_s7799-7799_T100000_20260923_154527.json`
(sha 5429ba421fc9bd86)

| k | T142 lift / muertes / mordidas | N lift / celdas | L015 | NAZAR | NSH | NC3C sep |
|---|---|---|---|---|---|---|
| 2 | 0.395 / 201 / 879 | 0.379 / 43 | 0.385 | 0.393 | 0.403 | **1.25** |
| 5 | **0.000 / 330 / 6** | **0.361 / 50** | 0.396 | 0.264 | 0.365 (90 celdas) | −0.43 |
| 8 | **0.000 / 331 / 2** | 0.090 / 90 | 0.132 | 0.218 | 0.153 | 0.05 |

## Qué falló o amenaza
- En el humo, el canal falso separa a k = 2 (sep 1.25 > 1.0). Si en la serie la mediana también pasa de 1.0,
  T4 cae y K_max(N) = 0 por la letra. Está declarado como riesgo de P6.
- L015 (el paso chico fijo de v14.0) **iguala a N** en 3T-k. En este mundo la normalización no se distingue de
  "paso chico". Lo que la distingue es fuera de 3T-k: N conserva A-4 en los mundos del tronco (inerte) y L015
  lo pierde.
- A k = 8, N no compone (0.090, pool 90/90). Los controles sí pasan en esa semilla. Es un techo a verificar,
  no un resultado.
- Candidato a ERR: A-4 entró al tronco (v14.1) sin volver a medir 3T-k. Es el mismo patrón de ERR-20. Propuesta:
  meter 3T-k (k = 3) en la batería del tronco.

## Qué queda (para el coordinador)
Serie `python experimentos/subida_n7/corre_n7.py --desde 7701 --n 20 --pool 6` y réplica `--desde 7721`, en ese
orden. Cada una son 8 k × 7 brazos × 20 semillas = 1 120 corridas × ~8.5 s ≈ **2.6 h de CPU (~27 min de pared
con Pool 6)**. Las dos juntas suman ≈ 5.3 h de CPU. Después, si FUNCIONA: v14.3 como reparación inerte bajo el
criterio v4, con T-A..T-H en semillas nuevas. Sin verificar: la transcripción de B-5 dentro de 3T-k (no hay
referencia con la que compararla bit a bit), la inercia en el mundo vivo (lo argumento por construcción, no lo
corrí) y el mundo grande de T-H, donde las masas varían y la perilla sí actúa.
