# PREREGISTRO (EXPLORATORIO) — BLOQUES4: olvidar / volver a probar en el mundo que cambia (Opus M, 28-sep-2026, 22:12)

Misión: llegar a la AGI por este camino. Escrito ANTES de ver números (con el arnés corriendo).

## Pregunta
Con la pieza de olvidar, ¿la selección arma "memoria que se actualiza" y el linaje sobrevive a las inversiones? ¿Qué tasa de olvido se fija?

## Mecanismo (`construye_bloques4.py` → `motor_bloques4.py`, 8 anclas desde `motor_bloques3.py` 21b5ee28d086b3be)
- **Kit 3 = kit 2 + dos acciones.**
  - **Acción 6, OLVIDAR:** si la condición se cumple, la memoria por letra y la R de la última mordida decaen hacia 0 en ese paso, con
    λ = min(1, 10^(Σw − 4)); λ va de 1e-7 a 0.1 por paso.
  - **Acción 7, REPROBAR:** si lo que tiene en la celda es una letra recordada mala, muerde igual con p = min(1, 10^(Σw − 3)).
- La tasa λ y la probabilidad p SON el peso de la regla: heredable y mutable, nadie la fija a mano. Las reglas son condicionales, así que
  también se puede olvidar sólo con hambre, sólo con sed, etc.
- El azar de reprobar es un hash de (t, ranura, letra): no toca ningún rng.
- Con kit 1 o kit 2, motor_bloques4 == motor_bloques3 bit a bit (arnés).

## Condiciones, brazos y semillas
Inversión A↔B y C↔D. T = 500 000.
| condición | inversión cada | vivero hasta |
|---|---|---|
| a | 100 000 | 100 000 |
| b | 100 000 | 250 000 |
| c | 50 000 | 250 000 |

- Brazos: BLOQ2_V (kit 2, sin olvido, referencia) · BLOQ3_V (kit 3) · BLOQ3_AZA_V (kit 3 sin herencia) · ING_SEL_C_V.
- Semillas NUEVAS 48611–48616 (grep del 28-sep: 486[1-9]x libre salvo 48675); arnés 48691–48694.

## Predicciones (antes de números)
| # | predicción | p |
|---|---|---|
| O1 | en (a), BLOQ3_V persiste ≥ 2/6 | 0.30 |
| O2 | BLOQ3_V vive más que BLOQ2_V (t_ext pareado) en ≥ 4/6, en (a) y en (b) | 0.50 |
| O3 | una regla de OLVIDO activa fijada (≥ 50 %) en ≥ 3/6 semillas de BLOQ3_V en alguna condición | 0.45 |
| O4 | λ mediano fijado en [1e-4, 1e-2] por paso (memoria de 100 a 10 000 pasos) | 0.40 |
| O5 | REPROBAR activo fijado en ≥ 2/6 | 0.35 |
| O6 | en (b) o (c), BLOQ3_V persiste ≥ ING_SEL_C_V | 0.35 |
| O7 | BLOQ3_AZA_V persiste 0/6 en las tres condiciones | 0.85 |

## Qué lo refuta
"Olvidar rescata al linaje" cae si BLOQ3_V no vive más que BLOQ2_V (O2) ni persiste más (O1, O6). "La selección elige una tasa" cae si
no se fija olvido (O3) o si lo fijado aparece igual en AZA.

## Números (22:27; `python corre_bloques4.py --lee olv`; 72 corridas, ningún aborto)

Persistencia (/6) y t_ext por semilla:
| condición | BLOQ2_V (sin olvido) | BLOQ3_V (con olvido) | BLOQ3_AZA_V | ING_SEL_C_V |
|---|---|---|---|---|
| a: cada 100k, vivero 100k | 1/6 | 0/6 | 0/6 | 2/6 |
| b: cada 100k, vivero 250k | 0/6 (K 7.6, muere en 300k) | 0/6 (K 6.9, muere en 300k) | 0/6 | 1/6 |
| c: cada 50k, vivero 250k | 0/6 | 1/6 | 0/6 | 0/6 |

BLOQ3_V vive más que BLOQ2_V (pareado): a 1/6 · b 4/6 · c 4/6.

**Qué se fijó** (≥ 50 % de los vivos o del banco de padres al extinguirse):
- **Olvido:** activo en ≥ 50 % sólo en 1/18 (48611 c: 52 %, λ 2.6e-2 por paso, memoria de ~40 pasos). En las demás está en 0–21 %; en
  BLOQ3_AZA_V, 0–84 % (deriva).
- **Reprobar:**
  - activo sólo en 48615 b (93 %, p 0.05 por encuentro, condicionado a "el vecino no mordió");
  - donde se fija en las otras semillas, lo hace con p ≈ 1e-6 a 5e-9: la selección lo deja APAGADO.
- **Lo que sí se fijó:**
  - el instinto de la retina (o su versión invertida de la fase nueva);
  - el órgano SOCIAL "si el vecino no mordió, no muerdas" en 3 semillas (48616 a, 48615 b, 48616 b; 94–100 %);
  - "no muerdas justo después de parir" (tParto → boca −) en 48615 c y 48616 c; esta última es la única de BLOQ3 que persiste.
- No se fijó "memoria que se actualiza".

**Predicciones:**
- Refutadas: O1 (0/6), O2 (a 1/6), O3 (olvido fijado en 1/18), O4 (λ 2.6e-2, fuera de [1e-4, 1e-2]) y O5 (reprobar activo en 1/18).
- Aciertan: O6 (en c, 1/6 ≥ 0/6) y O7.

**Lectura: NO.**
- Con la pieza de olvidar, la selección NO arma "memoria que se actualiza": casi no fija olvido, y la reprueba la deja apagada.
- El linaje sigue muriendo justo después de las inversiones (t_ext en 300k), igual que sin la pieza y que el cerebro de 15 genes.
- **Causa probable (de instrumento, no medida):** el olvido de las reglas sólo borra la memoria de las reglas. La aversión aprendida del CEREBRO
  DE FÁBRICA (Wp/Wn, la memoria de rechazo) no se olvida, y ING_SEL_C_V, que no tiene reglas, muere en las mismas inversiones. Olvidar lo que
  aprendió el cerebro no está entre las piezas.
- Instrumento (sha a 16): construye_bloques4 c41408ec7def3c5a · motor_bloques4 ad5bd2eb59f6279d · corre_bloques4 1a7b1ffcb5baee17 · identidad_bloques4 fff245d158a1d765 → salida 6f6548772e709514 (10/10).
