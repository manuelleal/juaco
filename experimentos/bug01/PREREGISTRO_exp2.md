# BUG-01 — Experimento 2: decaimiento de la PARTE COMÚN de Wp/Wn

**Escrito ANTES de correr nada. Fecha: 15 sep 2026, cierre del día 3.**
Dirección: Christiam Puentes. Ejecución: pendiente — **lo corre el director**.
Formato del punto 19 del brief: qué prueba · qué cambia · qué esperamos · qué la refuta · métricas · controles.

**Este preregistro está CERRADO.** Si algo falla, se reporta REFUTADO y se registra. No se recalibra
`lam_c` a posteriori (regla 3). Un resultado negativo bien medido vale tanto como uno positivo.

---

## 1. Qué prueba

**BUG-01**: bajo refuerzo contradictorio sobre un código compartido, `Wp` y `Wn` crecen los dos hasta el
techo del clip (3.0/celda = 9.0 por código de K=3) y su diferencia se anula exactamente, congelando el
aprendizaje. Reproducible sin tocar nada: `organismo_v7.run(1, plast=False, solap_AB=3)` → `comp A=(9.0, 9.0)`,
`W=0.0`.

**El experimento 1 (decaimiento uniforme) quedó REFUTADO con demostración**, no por mala calibración:
hace falta `λ > 0.01500` para no saturar y `λ < 0.01000` para no estropear `W_B`. **Ventana vacía.**
El diagnóstico fue: el decaimiento uniforme ataca la **magnitud** de los canales, y la patología no es de
magnitud sino de **redundancia** — que los dos canales codifiquen lo mismo a la vez. Pagar en valor neto
para corregir un exceso que no está en el valor neto es el error de diseño.

Este experimento ataca la redundancia directamente.

## 2. Qué cambia — UN solo cambio

`experimentos/bug01/organismo_v7e.py` (sha256_16 `3118c6d563542da2`) = `organismo_v7.py` + una línea:

```python
if lam: ix = kc>0; mcom = np.minimum(Wp[ix], Wn[ix]); Wp[ix] -= lam*mcom; Wn[ix] -= lam*mcom
```

en el mismo sitio que el experimento 1: justo tras calcular `dlt`, antes de la actualización, sólo en las
celdas del código activo y sólo al morder. Nada más cambia.

**Las dos propiedades que motivan el diseño, y que son consecuencias exactas, no esperanzas:**

1. **`Wp − Wn` queda EXACTAMENTE intacto**, porque se resta lo mismo a los dos canales. El valor neto sigue
   obedeciendo Rescorla-Wagner puro. **Desaparece el sesgo del 1.1% que hundió P2 en el experimento 1, y con
   él la tensión entera entre no saturar y conservar el valor.**
2. **Donde no hay conflicto, la operación es literalmente inerte.** En E1, el código de A tiene `Wn = 0` y el
   de B tiene `Wp = 0`, así que `min(Wp,Wn) = 0` y no se resta nada. El arreglo **sólo actúa donde está la
   patología**.

### λ_c = 0.05, fijado a priori por el siguiente argumento (no por barrido)

Derivación, en unidades de código (suma sobre las K=3 celdas), `eta=0.03`, `K·eta=0.09`, `aversion=1`.
En el escenario del bug, A (comida, R=+1) y B (veneno, R=−3) comparten código, así que tienen el mismo `W`.
Como el decaimiento no toca la diferencia, `W` obedece RW puro y converge a la **media de recompensa**:
con mezcla 50/50, `W_eq = (+1 −3)/2 = −1`.

En ese equilibrio, `|dlt| = |R − W| = 2` para ambos estímulos, luego cada canal crece `K·eta·2 = 0.18` por
mordida de su tipo, y con mezcla 50/50, **0.09 por mordida** de media. El canal menor es `Wp`
(porque `Wn = Wp + 1`), así que `mcom = Wp` y el decaimiento retira `λ_c·Wp` por mordida.

    equilibrio:   0.09 = λ_c · Wp*        ->     Wp* = 0.09/λ_c ,   Wn* = Wp* + 1

    condición de no saturar:  Wn* < 9   ->   0.09/λ_c + 1 < 9   ->   **λ_c > 0.01125**

**Y no hay ninguna condición opuesta**, porque el valor neto no se toca. Se elige λ_c = 0.05, que deja
`Wp* = 1.8` y `Wn* = 2.8` sobre un techo de 9 — un factor **4.4 de margen** sobre la frontera de 0.01125 y
el 31% del rango usado. Barrido de sensibilidad declarado de antemano, λ_c ∈ {0.0125, 0.02, 0.1, 0.3}:
**descriptivo, NO decide.**

## 3. Qué esperamos — predicciones numéricas

**P1 — Desbloqueo (criterio primario).** En `plast=False, solap_AB=3`, donde hoy `Wp = Wn = 9.00` y `W = 0.00`
en 20/20:
- `Wp` y `Wn` **estrictamente por debajo de 9.00** en **20/20**.
- **`Wp ≈ 1.8` y `Wn ≈ 2.8`**, medianas dentro de **±0.5** de esos valores. (Predicción puntual, no rango
  cómodo: si el mecanismo es el que creemos, la cifra tiene que salir.)
- `W ∈ [−1.5, −0.5]` en **≥18/20** — el organismo converge a la media de recompensa en vez de congelarse en 0.

**P2 — No regresión, y esta vez EXACTA.** Las seis etapas (E1, E2, E2I, E2J, E2K, E2L) pasan **20/20** sus
criterios. Además, y es la predicción fuerte: en **E1, E2I y E2J** —donde no hay conflicto de signo sobre un
código— los resultados deben ser **bit-idénticos** a `lam=0`, porque `min(Wp,Wn)=0` hace la operación inerte.
No "parecidos": idénticos.

**P3 — Exactitud del valor recuperada.** `W_A = +1.000` y `W_B = −3.000` **exactos** (mismo valor que v7 con
`lam=0`), sin el sesgo del 1.1% del experimento 1. Criterio: desviación **≤ 0.002**.

**P4 — Ley de disparo.** El patrón de divisiones (`splits>0` sí/no por semilla) no cambia respecto a `lam=0`
en ninguna etapa. Nota: E2 y E2L **sí** pueden cambiar el número de divisiones, porque ahí hay conflicto real
y el arreglo actúa; lo que no debe cambiar es **quién divide y quién no**.

**P5 — Capacidad** (prueba independiente, en el diseño de 2K-bis; no decide P1–P4). Con el arreglo activo:
la fracción de valores finales exactamente 0.000 debe caer **por debajo del 20%** (hoy 82%), y el máximo de
estímulos simultáneamente bien aprendidos debe **subir** respecto al 4 actual de v7.

## 4. Qué lo refuta

- Algún canal **sigue tocando el techo** (≥ 9.00) en el escenario del bug, en cualquier semilla.
- Las medianas de `Wp`/`Wn` se apartan más de **±0.5** de 1.8 y 2.8 → el mecanismo no es el que creemos, y eso
  importa más que si "funciona".
- **Cualquier etapa** de la batería baja de 20/20.
- **E1, E2I o E2J no son bit-idénticas** a `lam=0` → la operación no es inerte donde debería serlo, y hay algo
  en el código que no entendemos.
- `W_A` o `W_B` se apartan de ±R más de 0.002.
- Cambia **quién** divide en alguna etapa.

## 5. Métricas

Por semilla: `Wp` y `Wn` por código, `W` de cada estímulo, canales en el techo, mordidas y visitas por cuarto,
muertes, `splits`, `split_t`, celdas activas, solapamientos. Medianas y rangos siempre (regla 6).
20 semillas (1..20), T = 100.000.

## 6. Controles obligatorios (antes de aceptar cualquier resultado)

1. **Inercia**: `organismo_v7e.run(..., lam=0.0)` debe ser **bit-idéntico** a `organismo_v7.run(...)` en los
   7 escenarios × 6 semillas. Mismo protocolo que se usó para v7 vs v7c, para la sonda de Etapa 3 y para v7d.
2. **Reproducción del bug**: con `lam=0.0`, el escenario debe seguir dando `(9.0, 9.0)` y `W=0.0`.
3. **Regla 1**: `bateria.py 6` todo PASA antes de empezar.
4. **Hashes**: `python manifiesto.py` → los cuatro congelados intactos, antes y después.

## 7. Cómo correrlo

```
cd C:\Users\User\Documents\PROYECTOS\JUACO\bundle
python organismo\..\manifiesto.py                       # control 4
cd organismo && PYTHONIOENCODING=utf-8 python bateria.py 6 && cd ..
python experimentos\bug01\corre_bug01_exp2.py 20        # controles 1 y 2 + experimento
```

Tarda ~4 minutos con 16 núcleos (400 corridas). El script imprime el veredicto de P1–P4, aborta si falla
cualquier control, y escribe `datos/bug01_exp2_<fecha>.json` con cabecera de procedencia completa.
**Si un control falla, el script para y no corre el experimento.** Eso es deliberado.

## 8. Si P1 se sostiene, qué sigue (no es parte de este experimento)

1. Repetir **3T como confirmatorio** con este arreglo en lugar del techo subido a mano. 3T ya mostró post-hoc
   que, quitado el bloqueo, la regla de división **descubre sola la dimensión temporal** (`sep` 3.97,
   `lift` 0.34, 20/20). Con criterio escrito antes, eso sería el **nivel 7** de la escala del punto 6.
2. Repetir el examen de congelación de v7 con la ley de disparo definitiva (`err_max > 0.6`).
3. Rehacer el barrido de capacidad de 2K-bis, donde v7 hoy pierde contra v6.

## 9. Si P1 se refuta — experimento 3, ya nombrado aquí y sin probar

**Normalización opuesta completa**: `m = min(Wp, Wn); Wp -= m; Wn -= m` (es decir, λ_c = 1). Impide **por
construcción** que se acumule redundancia: tras cada evento de aprendizaje, el canal menor queda en 0.
`Wp − Wn` sigue intacto. El clip pasaría a limitar sólo `|W|` mismo, que es el límite legítimo.
Un cambio por experimento: **no mezclar con el 2**. Si el barrido de sensibilidad de λ_c ∈ {…, 0.3} ya insinúa
la respuesta, se registra como indicio y se corre el 3 aparte con su propio preregistro.
