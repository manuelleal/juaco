# INFORME — F1 ARRANQUE EN FRÍO (creador, 25-sep-2026, ~13:30–14:10). Paquete LISTO PARA SERIE; sin serie, sin Pool, sin git.

Misión: llegar a la AGI por este camino. Meta: mantener el linaje sin andamio. Preregistro: `PREREGISTRO_frio.md`.

**Qué hice**
- `construye_frio.py` construye por anclas, desde los sha de la serie v1.2, dos archivos:
  - `carros/BAR0_ECO.py` (a4b899611bd71197) = FAMB_RES0_ECO con `MODO = 'bar'`, que es el BAR_SIN0 de n10c con el `_see` de ECO;
  - `motor_frio_rapido.py` (ff9d890a5cce9dec) = el gemelo 132/132, más BAR0 (la permutación en `objmode`, con las líneas del carro) y la
    guardia ERR-60 subida a 1e9 (**ERR-146**).
- `corre_frio.py` (3ba8b0f5cf1fbbfa) es el envoltorio de `corre_eco_v12`. Lleva los 5 brazos, cada uno con su carro y su `t_corte`, y la
  genética MUT0 en todos. Atrapa todo `SystemExit` (nube-9). Implementa la letra, con sus nulos declarados.
- `ancla_1e6.py` es para el coordinador: una corrida de 1e6 (RES0_60k s19701) comparada campo a campo con el JSON guardado de MUT0_T.

**Arnés `identidad_frio.py` (salida completa en `identidad_frio_salida.txt`), 14:04, 84 s**
```
(K) 2/2 · (A) motor copiado == gemelo original, salida entera: 5/5 · (B) envoltorio RES0_60k == corre_eco_v12 MUT0_T: 2/2
(C) motor copiado == motor Python en los 5 brazos (BAR0 incluido): 5/5 · (D) frío limpio + control que puede fallar: 6/6
(E) BAR permuta de verdad: 3/3 (173/200 partos con otra asignación) · (Q) corte + --reanuda: 2/2 · (F) nube-9: 3/3
(V) la letra: 15/15 · (R) banderas: 3/3                                                        RESULTADO: 46/46
(B) ... distintas [], faltan [] (persiste 1, vivos_T 22, n_nac 4615, refundados 21050; 13.8 s contra 14.4 s)
(D) control: con vivero SÍ refunda (t_corte 1500: 334 refundados); con t_corte 1 y linajes extinguiéndose (quedan 3): 0 refundados
```

**Humo** (`--humo`, 35905, T 200 000, 1 proceso, 33.6 s; JSON escrito). No se lee.
- Persisten RES0_FRIO (32 vivos, 0 refundados), RES0_10k (37), RES0_60k (34) y **BAR0_FRIO (11)**.
- FAB_FRIO se extingue en t 2 792.

**Lo que el investigador no verificó**
- `t_corte = 1` funciona sin efectos laterales. El vivero sólo podría refundar en t = 0, y ahí nadie muere. La foto del corte es de t = 1
  (90 fundadores) y `sel_corte` queda en None. El gemelo parte el tramo en t = 1 y da lo mismo que el motor Python (C).
- Los JSON de MUT0_T existen: 20/20 persisten a 1e6, R0 tras el corte 0.9945–0.9970, 1 linaje, 21 400–21 900 nacimientos. Descriptivo
  nuevo: en el corte hay ~225 cuerpos en 90 linajes, y 2 000 pasos después quedan ~67 en 10–14 linajes. El vivero sí es un andamio.
- Dato que la ficha no tenía: FABRICA + MUT0 con vivero da 0/20 en ECO v1 (×2) y 0/20 en v1.1 a 1e6. Por eso subí P3 a 0.97.
- La guardia ERR-60 era un resto de la fórmula escalar de H-1. Aquí la semilla es una lista y no colisiona. Los brazos MUT0 hacen ~20 000
  nacimientos por corrida, así que no se espera que dispare ni la guardia vieja.

**Costo, medido en 1 proceso (a 200 000 pasos) y extrapolado a 1e6**

| brazo | segundos por corrida |
|---|---|
| RES0_FRIO | ~32 |
| RES0_10k | ~33 |
| RES0_60k | ~44 (la nube midió 47–49) |
| BAR0 vivo | ~10 |
| FAB | < 1 |

- Serie con Pool 6: ≤ 2 400 s de CPU, unos **7 min**. Con los exploradores ocupando núcleos serán **10–25 min por serie**.
- No es 0.6–1.7 h como estimó la ficha.

**Comandos (el coordinador, en este orden)**
```
python experimentos/organelos/frio/construye_frio.py --verifica
python experimentos/organelos/frio/identidad_frio.py                                   # 46/46, ~1.5 min
python experimentos/organelos/frio/ancla_1e6.py                                        # IGUAL, ~1 min (1e6: no lo corrí)
python experimentos/organelos/frio/corre_frio.py --serie --desde 35001 --n 20 --pool 6
python experimentos/organelos/frio/corre_frio.py --serie --desde 35021 --n 20 --pool 6  # réplica
```

**Qué falló / ERR**
- **ERR-146:** guardia a 1e9, declarado antes del humo.
- **ERR-147:** el caso (Q) se añadió tras el humo. Su primera versión daba 45/46 porque BAR0 en 35904 moría antes del corte. Era el diseño
  del caso, no el instrumento. Runner y letra sin cambios.

**Predicciones**
- No hay ninguna refutada todavía: no corrí la serie.
- Riesgo visible: BAR0_FRIO sobrevivió al humo. P4 (≤ 5/20, firmada con 0.90) es mi predicción más expuesta; no la toco.

**Qué queda / no verificado**
- La ruta con Pool en Windows (spawn) no la ejecuté: el patrón es el de `corre_eco_v12`.
- `ancla_1e6.py` no lo corrí, por la regla de 200 000 pasos.
- Una semilla que llegue exactamente a 100 000 cuerpos: sin probar en real, sólo con un `SystemExit` simulado.
