# PREREGISTRO (EXPLORATORIO) — BLOQUES5: olvidar lo que aprendió el cerebro (Opus M, 28-sep-2026, 22:30)

Misión: llegar a la AGI por este camino. Escrito ANTES de ver números (con el arnés y las corridas en marcha, sin mirarlas).

## Mecanismo (`construye_bloques5.py` → `motor_bloques5.py` a727e6aea0fca8da, 10 anclas desde `motor_bloques4.py` ad5bd2eb59f6279d)
- **Acción 8, OLVIDAR EL CEREBRO:** si la condición se cumple, la aversión aprendida del cerebro de fábrica decae hacia su valor de nacimiento
  (0), con λ = min(1, 10^(Σw − 4)) por paso.
  - Afecta Wn (vía rápida) y Wns (vía lenta), de las dos necesidades.
  - Por costo se aplica cada 100 pasos con el factor (1 − λ)^100.
  - Wp y la memoria de rechazo no se tocan: esta última caduca sola en ≤ memoria_rechazo pasos.
- **kit 4** = kit 3 + acción 8.
- **kit 5** = SÓLO el gen: una regla fija "siempre → olvidar el cerebro" en la que sólo muta w. Cada fundador arranca con un w al azar en
  [−3, 3], así que no hay constante a mano.
- Kit 1 a 3: motor_bloques4 bit a bit (arnés).

## Condiciones, brazos y semillas
- Inversión A↔B, C↔D cada 100 000; T 500 000. Condición a = vivero hasta 100 000; condición b = vivero hasta 250 000.
- Brazos:
  - BLOQ3_V (referencia);
  - BLOQ4_V (kit 4);
  - BLOQ4_AZA_V (kit 4 sin herencia);
  - ING_SEL_C_V;
  - SEL_OLV_V (15 genes + el gen de olvido, sin otras reglas).
- Semillas NUEVAS 48621–48626 (grep: libres); arnés 48681–48684.

## Predicciones
| # | predicción | p |
|---|---|---|
| C1 | SEL_OLV_V persiste más que ING_SEL_C_V (suma de a y b) | 0.45 |
| C2 | SEL_OLV_V vive más que ING_SEL_C_V (t_ext pareado) en ≥ 7/12 | 0.55 |
| C3 | λ fijado en SEL_OLV_V (mediana de los vivos o del banco) en [1e-5, 1e-3] por paso (memoria de 1 000 a 100 000 pasos) | 0.45 |
| C4 | BLOQ4_V vive más que BLOQ3_V en ≥ 7/12 | 0.45 |
| C5 | la acción 8 activa fijada (≥ 50 %) en ≥ 3/12 de BLOQ4_V | 0.35 |
| C6 | algún brazo persiste ≥ 3/6 en la condición b | 0.35 |
| C7 | BLOQ4_AZA_V persiste 0/12 | 0.85 |

## Qué lo refuta
"Olvidar lo aprendido rescata al linaje" cae si SEL_OLV_V y BLOQ4_V no viven más que sus referencias (C2 y C4). "La selección elige una tasa"
cae si λ en SEL_OLV_V deriva igual que el valor inicial al azar (sin concentración).

## Números (22:42; `python corre_bloques5.py --lee olvc`; 60 corridas, ningún aborto; arnés 11/11)

Inversión cada 100 000.
| brazo | persiste, vivero 100k | t_ext mediano | persiste, vivero 250k | K mediana (vivero 250k) |
|---|---|---|---|---|
| BLOQ3_V | 0/6 | 116 k | 1/6 | 7.49 |
| BLOQ4_V (+ olvidar el cerebro) | 0/6 | 104 k | 0/6 | 7.07 |
| BLOQ4_AZA_V | 0/6 | 104 k | 0/6 | 0.55 |
| ING_SEL_C_V | 0/6 | 201 k | 0/6 | 2.44 |
| SEL_OLV_V (15 genes + gen de olvido) | 0/6 | 250 k | 0/6 | 3.70 |

Pareados:
- SEL_OLV_V vive más que ING_SEL_C_V en 4/6 (vivero 100k) + 4/6 (vivero 250k) = 8/12 (signo p ≈ 0.19: no se distingue del azar).
- BLOQ4_V vive más que BLOQ3_V en 0/6 + 3/6.

**Qué tasa se fija:** en SEL_OLV_V, el gen está en el 100 % y **λ mediana de 1e-7 a 3e-6 por paso en 11/12 semillas (y 3e-5 en una)**: una memoria de
10^5 a 10^7 pasos, mucho más larga que una vida (~10^3) y que el periodo de inversión (10^5). Los fundadores arrancan con λ al azar entre 1e-7 y
0.1 (mediana ≈ 3e-4). **La selección empuja el olvido del cerebro hacia APAGADO.**
- En BLOQ4_V la acción 8 activa se fija sólo en 2/12: 48622b (95 %, λ 9e-4) y 48624b (77 %, 3e-7).
- Sin herencia, λ se dispersa entre 3e-7 y 0.26.

**Predicciones:**
- Refutadas: C1 (0 contra 0), C3 (λ fijado por debajo de 1e-5), C4 (3/12), C5 (2/12) y C6.
- Aciertan: C2 (8/12, pero no significativo) y C7.

**Lectura: NO.** Con el olvido del cerebro disponible, el linaje tampoco sobrevive a las inversiones, y la selección elige NO olvidar.
Porqué probable (no medido aparte):
- el hijo nace ingenuo, así que cada generación ya aprende de cero;
- olvidar sólo sirve a los adultos vivos en el momento de la inversión (una vez cada 100 000 pasos, unas 30–100 vidas);
- entre inversiones, olvidar cuesta volver a aprender el veneno;
- la selección, que ve vidas y no siglos, no puede pagar ese seguro. El arnés lo muestra en el extremo: con λ = 0.1 los nacimientos caen de 1 411 a 43.

Instrumento (sha a 16): construye_bloques5 f20bbedb7d0a616c · motor_bloques5 a727e6aea0fca8da · corre_bloques5 90a01b9a7ba05f91 ·
identidad_bloques5 01f92da4456c623b → salida 2e2cc7f0f2b6e865 (11/11).
