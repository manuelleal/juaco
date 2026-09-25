# RESULTADO del exploratorio H-PLANO en w90 (10:08–11:09, nube). **No es dato.**

**Por la lectura preregistrada: AMBIGUO en M1 y en M2. La manipulación funcionó (M0).**

| Medida | w30 (serie, 20 semillas) | **w90 (25101–25110)** | Lectura preregistrada |
|---|---|---|---|
| M0: nacidos antes del corte (mediana) | 6 | **20** | OK (umbral 18) |
| Nacidos tras el corte (mediana), VIDA / FIJO | 20.5 / 188.5 | **567.5 / 655** | ×30 más cohorte |
| Persisten, VIDA / FIJO | 9/20 / 13/20 | **8/10 / 9/10** | |
| M1: sólo FIJO − sólo VIDA | 4 − 0 (tasa 0.20) | **2 − 1 = 1** | **AMBIGUO** |
| M2: vivos en T pareado, VIDA ≥ FIJO | — | **4/10** | **AMBIGUO** (3 < 4 < 7) |
| Nacidos tras el corte, VIDA/FIJO | 0.11 | **0.87** | descriptivo |
| R0 tras el corte (mediana), VIDA / FIJO | 0.88 / 1.08 | **1.11 / 1.08** | descriptivo (ERR-133) |
| Vivos en T (mediana), VIDA / FIJO | — | **28.5 / 36** | descriptivo |

**Post-hoc, no preregistrado, marcado como tal.** En los pares donde persisten los dos, la razón de vivos VIDA/FIJO sube de **0.67 (w30, 9 pares) a 0.97 (w90, 7 pares)**. La carga se achica con N, pero no desaparece; VIDA ≥ FIJO en 3 pares de los dos lados.

## Lectura
- **Triplicar el mundo cambió mucho el cuadro:**
  - las poblaciones persisten (80–90 %);
  - la cohorte tras el corte se multiplica por 30;
  - VIDA deja de ser "carga pura": sólo FIJO pasa de 0.20 por semilla a 0.10 por semilla.
- **La dirección es la que predice H-PLANO**, pero con 10 semillas no alcanza la letra: D = 1 y M2 4/10.
- **Lo que sigue sin verse:** ninguna señal de que VIDA *supere* a FIJO. Con más N, la variación deja de costar tanto, pero todavía no paga.
  - Eso es exactamente lo que diría H-PLANO en su versión débil.
  - La versión fuerte ("con N suficiente, la variación crea algo mejor") no tiene apoyo todavía.

## Recomendación para el PC
- **Vale la pena escalar**, porque la señal va en la dirección predicha y el instrumento está verificado.
- Se escala como serie preregistrada y no como más de lo mismo:
  - w90 con 20 semillas y réplica, M1 y M2 como aquí;
  - añadir como **primaria** la razón de vivos en pares que persisten, preregistrada ahora antes de ver semillas nuevas;
  - y **w270** (gemelo numba, `ESPEC_GEMELO_anfitrion.md`) para ver si la razón cruza 1.
- **Costo en la nube:** ~530 s por corrida en w90, 3.5× w30. Una serie de 20 semillas × 2 brazos con Pool 3 son ~2 h.
