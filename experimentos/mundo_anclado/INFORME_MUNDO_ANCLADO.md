# INFORME — MUNDO ANCLADO (rama `mundo-anclado`, 22-sep-2026)

**Veredicto: NO.** Con una perilla de dilución de lo malo (quimiostato) no existe un mundo anclado en la rejilla
preregistrada. Diluir sube a NADA y a ORÁCULO **en la misma proporción**: la razón ORÁCULO/NADA se queda en 3.0–3.2,
y las anclas piden ≥ 3.33 (1.0/0.30). Rozamiento en h = 0.0015: ORÁCULO **1.000** (pasa justo) y NADA **0.314**
(fuera por 0.014). Por la regla 5(c)/(d) no se amplía la rejilla y no se corre la confirmación.

## Qué hice
1. `construye_anclado.py` genera `organismo_anclado.py` (sha `e689c2952b1991a4`) por 4 anclas desde `organismo_f9c.py`
   (`9dd1fb91ecec35ae`). No toca el cuerpo. Perilla `olv_mal` = h: cada objeto malo (leído de la tabla del mundo, no de las
   letras) desaparece con probabilidad h por objeto y por paso; usa un rng propio (890000+10⁶·seed), y `spawn()` repone
   como siempre. Placebo `olv_ciego`: mismos sorteos y misma dosis, pero se lleva un objeto al azar. `anc_mide`: presencia
   por tipo, sólo lectura.
2. El arnés `identidad_anclado.py` compara el dict completo con igualdad exacta y recursiva, en los brazos de
   `corre_bloque2.BRAZOS` (el mismo objeto importado) — **TODO PASA** (salida abajo y en `identidad_anclado_salida.txt`).
3. Humo, semilla 1 y 6 corridas (`datos/humo/anclado_humo_20260922_135253.json`), para fijar la rejilla. Después escribí
   `PREREGISTRO_mundo_anclado.md` (sha `ea380602eb25b4af`), con anclas, regla de elección y predicciones firmadas.
4. Calibración 7001–7020 (libres por grep en los 5 worktrees), sólo NADA y ORÁCULO, rejilla ascendente, un proceso:
   120 corridas en 21.4 min de CPU (`datos/anclado_cal_s7001-7020_20260922_135510.json`, sha `2a380d83d1915adc`).
   Regla 14: el runner imprime OK campo a campo en los 7 brazos.

## Calibración (medianas de 20 semillas; rep_acum = 0; T = 100 000)
| h (por objeto y paso) | R0 NADA | R0 ORÁCULO | razón | ORÁCULO ≥ 1 | NADA ≤ 0.30 | f_mala NADA / OR | vida NADA / OR |
|---|---|---|---|---|---|---|---|
| 0 (bloque 2, dos series) | 0.14 | 0.43–0.46 | 3.0–3.3 | 0/20 | — | 0.85 / 0.91 (diag) | 95 / 600 |
| 0.0005 | 0.197 | 0.610 | 3.09 | 0/20 | 20/20 | 0.838 / 0.894 | 94 / 647 |
| 0.001 | 0.253 | 0.752 | 2.97 | 0/20 | 19/20 | 0.831 / 0.882 | 103 / 684 |
| 0.0015 | **0.314** | **1.000** | 3.18 | 11/20 | 7/20 | 0.823 / 0.870 | 128 / 695 |
| 0.002, 0.003 | no se corren (regla 5c: NADA ya > 0.30) | | | | | | |

J (p1 + c1 − 1, acierto balanceado): NADA de 0.18 a 0.20, ORÁCULO 0.98 en todos los puntos. El cuerpo no cambia y la
perilla no toca la discriminación. f_mala baja apenas 2 puntos, así que el mundo **no** se come lo malo. Aun así, R0 se
duplica.

## Predicciones propias
- **REFUTADAS:** P1 (existe un punto; h = 0.001) y P2 (en ese punto, ORÁCULO 1.10–1.80). En h = 0.001 ORÁCULO dio 0.75.
- **No evaluadas** (sin punto elegido no hay confirmación): P3 (REL en 0.55–0.90 del espacio), P4, P5 (BARAJA), P6
  (placebo) y P7 (RENACE).
- **Error de diseño mío:** elegí la perilla porque sube el nivel de R0. Lo que separa las anclas es la **razón**, y
  diluir la mueve poco.

## Controles, trampas y REL
- Placebo ciego: sólo el humo (h = 0.006, semilla 1): selectiva 4.52 frente a ciega 2.22. La selectividad importa,
  pero es una sola semilla y no juzga nada.
- REL no se mide en un mundo anclado porque no hubo punto. Como referencia, en el mundo de hoy REL cae en 0.80–0.84 del
  espacio NADA–ORÁCULO (bloque 2, ×2).
- Trampas: el canal es simétrico (la misma perilla en todos los brazos); J va balanceado; el mundo no se come la comida
  (f_mala ≥ 0.82); los sitios se sortean en cada spawn.

## Qué queda (dato para el próximo preregistro; NO es resultado)
Humo exploratorio de toxicidad, semilla 1 y 6 corridas (`humo_toxicidad.py`,
`datos/humo/anclado_humotox_20260922_141826.json`). Usa el kwarg `tabla`, que ya existe, con lo malo ×2 (−0.8).
Resultado: NADA 0.007 y ORÁCULO 0.129 con h = 0; con h = 0.003, NADA 0.038, ORÁCULO 0.394 y REL 0.348. La razón pasa de
~3 a ~10. La toxicidad castiga la ignorancia y deja casi intacto el conocimiento, aunque el hambre todavía empuja al
oráculo a morder, y con ×2 los recién nacidos mueren al primer bocado malo. **Candidato para el próximo paso:** dos
perillas del mundo, ambas por objeto:
- **toxicidad** de lo malo, que abre la razón;
- **dilución** `olv_mal`, que sube el nivel.

Ese paso pide un preregistro nuevo con una rejilla de 2 dimensiones (p. ej. tox ∈ {1.5, 2} × h ∈ {0.003, 0.006, 0.012}),
unas 240 corridas, y lo corre el coordinador con Pool.
Peldaños biológicos: la dilución es un quimiostato o descomponedores (capacidad de carga). La toxicidad es la presión de
selección de un ambiente con presas venenosas (aposematismo sin señal).

## Arnés de identidad (pegado)
```
IDENTIDAD ANCLADO · organismo_f9c (sha 9dd1fb91ecec35ae) vs organismo_anclado (sha e689c2952b1991a4) · brazos = corre_bloque2.BRAZOS · T=20000
A. perillas apagadas: OK NADA s1/s2 acum0, NADA s1 acum1, REL s1 acum0, REL s2 acum1, ORACULO s1 acum0, ORACULO s2 acum1,
   REL_BAR s1, RENACE s1 acum0/acum1  (difs=[] en los 10; dict completo, igualdad exacta)
B. anc_mide=1: OK NADA, ORACULO, RENACE  extra=['anclado'] difs=[]
A'. T=100000 ORACULO s1: OK difs=[] muertes=144 desc=54
C. ERR-38: OK olv_mal cambia la corrida · OK ciego != selectiva · OK f_mala 0.847 -> 0.793 (ciego 0.803)
   · OK selectiva solo quita B/D · OK ciego quita tambien A/C
TODO PASA en 82.4s
```
CPU total del creador: unos 26 min (arnés 1.4, humos 2.2, calibración 21.4), un proceso, sin Pool. Declarado: el humo 1
corrió con una versión anterior de `corre_anclado.py`; después de él sólo cambiaron `GRID` y la guardia del preregistro.
