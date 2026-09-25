# INFORME: Darwin y endosimbiosis, escalón 1 (organelos, Opus B, 24-sep-2026)

Misión: llegar a la AGI por este camino.

## Resumen
- **Instrumento LISTO:** arnés 15/15 y humo con los 5 brazos, todo ejercitado. **Sin serie:** la corre el coordinador.
- **Mi apuesta para la serie es NO** (P 0.54). La razón está medida, no es cautela: con FABRICA en w30, tras el corte viven de 1 a 4 cuerpos.

## Qué hice
**1. `DIAGNOSTICO_DARWIN.md`: diez condiciones, citadas con archivo:línea y con números leídos de la serie ECO v2.1 ya registrada.**
- **El Darwin mínimo ya está después del corte:** hay variación, herencia y reproducción que decide el mundo.
- **Antes del corte hay cría asistida:** ≥ 77 % de los cuerpos los pone el vivero, y en el corte la población cae de 74 a 41 y después a 14.
- Veredicto: **estamos a 5 pasos del Darwin que crea formas:**
  1. soltar el vivero;
  2. genoma que crece;
  3. otro que evoluciona enfrente;
  4. mezcla de genomas;
  5. escala sin el techo de ERR-60.

**2. Endosimbiosis.**
- Replicadores libres (g ∈ ℝ⁶) viven pegados a los objetos, sin comérselos, y se copian con error.
- El bicho los traga por contacto: los digiere o se quedan adentro, pagando 10 % del costo basal. Se heredan y mutan, se pierden con p 1e-4 por paso y p 0.05 por parto, y suman tanh(g·P) a la boca.
- Construido por anclas desde `motor_eco3` + `FABRICA_ECO` (`construye_endo.py`), con el código nuevo en `simbiontes.py`.
- Runner: `corre_endo.py` (`--humo`, `--lee`; `--serie` y `--prueba_pool` quedan para el coordinador).
- nube-9 corregido: el motor registra ERR-60 en vez de lanzar y el runner atrapa `BaseException`.

**3. Arnés `identidad_endosimbiosis.py`: 15/15, N/N.** Con `simb=None` es motor_eco3 **bit a bit** en 4 configuraciones. Además comprueba el carro sin canal, que los libres no tocan el mundo del bicho, el canal apagado en INERTE y activo en VIDA_S, el determinismo, ERR-60 con simb y sin él, la contabilidad, el barajado, el anillo y la pérdida. Salida:
```
(F) PASA VERIFICA OK · (A1) PASA VIDA w30 T 6000 corte 3000 · (A2) PASA AZAR w30 · (A3) PASA juez w9 · (A4) PASA eco=None
(B) PASA FABRICA_SIMB sin simb == FABRICA_ECO · (C) PASA bicho == motor_eco3; libres nacidos 1986, vivos 508, tragados 0
(D1) PASA INERTE: tragados 36 quedan 12 herencias 15 canal 0 · (D2) PASA VIDA_S: canal 78 · (E) PASA
(G1) PASA simb=None lanza ERR-60 · (G2) PASA err60 {'t': 406, 'lin': 2, 'donde': 'fundador'} · (H) PASA · (I) PASA barajados 17, sorteos 297
(J) PASA perdidas internas 2, fallas en el parto 2 · RESULTADO: 15/15 · 164 s · N/N
```

**4. Humo final** (22993, T 80 000, corte 50 000, un proceso, 582 s): `datos/humo/endo_humo_20260924_135039/HUMO_endosimbiosis.json`, `todos_ejercitados: true`.

| brazo | tragados | digeridos | quedan | herencias | decisiones de boca con canal | pérdidas internas | fallas en el parto |
|---|---|---|---|---|---|---|---|
| VIDA_S | 1186 | 923 | 263 | 294 | 11 483 | 22 | 11 |
| INERTE | 1397 | 1244 | 153 | 2127 | 0 | 62 | 130 |
| AZAR_S | 1144 | 984 | 160 | 1825 | 40 815 | 63 | 105 |

- BARAJADO baraja 252 veces.
- SIN_TRAGAR no traga nada y aun así nacen 34 038 libres.

## Qué falló (todo antes de preregistrar; declarado en el preregistro)
- **Predicciones mías refutadas:**
  - Los libres con c0 0.003 eran viables: se extinguieron. Con c0 0.001 también se extinguieron, en el humo 1.
  - "El nicho libre no distingue comida de veneno" es falso. El bicho deja B y D en el mundo, y el I de los libres cae a −0.1…−0.3: domesticar es remar contra la vida libre (corregido en el docstring).
  - Mi AZAR_S sesgaba la fracción hacia arriba, porque sólo las adquisiciones entraban al anillo. Ahora las pérdidas empujan "ninguno".
  - El arnés con NAC_MAX 60 no disparaba la guardia.
- **La medida D se rediseñó.** Pasó de "transmisiones tras el corte" a "partos de toda la corrida contra los libres del mismo instante", tras ver que tras el corte hay 1–4 cuerpos (7 portadores).
- **P3 pasó a ser pareada contra AZAR_S e INERTE**, por el sesgo de adquisición: el bicho se para en A y C y traga libres con I alto.
- **Corrección del coordinador aplicada** (trinquete de Fable): la pérdida existe y está probada en el arnés (J). La fracción portadora no decide y la predicción bajo deriva está escrita: 0.40–0.80. Decide la persistencia y el R0 pareados.

## Qué queda
- Coordinador:
  - `--prueba_pool --pool 2` (22991–22992);
  - la serie 22001–22020 y la réplica 22021–22040.
- **No pude verificar:** la ruta del Pool (el contrato me la prohíbe); si la guardia de ERR-60 se dispara a T 120 000 (w30 debería quedar lejos del límite); el tamaño real de los JSON (~0.3 MB por corrida, ~45 MB por ventana).

## Costo de la serie
~3 min por corrida (medido: 80 000 pasos en 112–144 s). 100 corridas por ventana:

| | por ventana | serie + réplica |
|---|---|---|
| **Pool 3** | ≈ 1.7–2.2 h | ≈ 3.5–4.5 h |
| **Pool 6** | ≈ 0.9–1.2 h | ≈ 1.8–2.4 h |

## Riesgos
1. **Poder bajo en w30.** Tras el corte quedan 1–4 cuerpos, así que P1 y P2 casi no pueden pasar. P3 es la pregunta con poder. Un w90 costaría ~3–6× más.
2. La ecología de los libres es de filo: la probé en 3 semillas de práctica.
3. NO EVALUABLE por el trinquete (P 0.08) o por el placebo de D (0.04 nominal).
4. El canal casi no cambia la mordida en el humo final (B: 0.225 con canal contra 0.225 sin él). Puede que el canal sea débil con k = 1.
5. Un solo carro (FABRICA) y un simbionte por cuerpo.

Veredicto predicho por ventana: FUNCIONA 0.01 · MODESTO 0.25 · NO 0.54 · NO EVALUABLE 0.20.
