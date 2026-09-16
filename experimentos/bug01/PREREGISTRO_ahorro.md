# Prueba de ahorro — el COSTE del arreglo de BUG-01

**Escrito ANTES de correr nada. Fecha: 15 sep 2026, día 3, tarde.**
Dirección: Christiam Puentes — **exigido por él como condición para seguir con el paso 1**. Ejecución: repo.

> "Ese arreglo deja uno de los dos canales en cero, y eso elimina la coexistencia que 2F compró: el miedo
> latente bajo el apetito. Hay que medir si la perdemos." — dirección, 15 sep 2026.

---

## 0. Precisión sobre el alcance, antes de nada

La objeción es correcta, y muerde con fuerza distinta en cada variante:

- **Exp. 2 (`λ_c = 0.05`, sin piso)**: **no** deja ningún canal en cero. Su equilibrio derivado y medido es
  `Wp* = 1.8`, `Wn* = 2.8` (observado 1.77 / 3.04). **Drena** la parte común hacia un equilibrio bajo, no la
  elimina. La coexistencia sobrevive, reducida.
- **Exp. 3 (`λ_c = 1`, normalización opuesta completa)**: sí deja el canal menor **exactamente en 0** tras cada
  evento de aprendizaje, por construcción. Ahí la objeción es letal si el ahorro depende de la coexistencia.

Se miden las dos, y las intermedias con piso. **El coste se preregistra antes de congelar nada**, que es lo
que pidió la dirección.

## 1. Qué prueba

Si el miedo extinguido sobrevive como traza latente en `Wn` bajo un `Wp` que lo cancela, entonces reaprender
ese miedo debe costar **menos mordidas** que aprenderlo la primera vez. Eso es el **ahorro**, y es la firma
conductual de que 2F compró algo real con los canales separados.

El arreglo de BUG-01 drena justamente la parte común de `Wp`/`Wn`, que es donde vive esa traza. **La hipótesis
es que el arreglo compra rango dinámico vendiendo memoria latente.**

## 2. Diseño — tres fases en el mismo organismo

`T = 200.000`, semillas 1..20, tres fases sobre el mismo individuo:

| fase | ventana | mundo | qué se mide |
|------|---------|-------|-------------|
| 1. adquisición | `[0, 60.000)` | A comida, B veneno | `n1` = mordidas de B hasta `W_B ≤ −2.5` |
| 2. extinción | `[60.000, 120.000)` | **invertido**: A veneno, B comida | `wB_ext` = `W_B` al final |
| 3. reaprendizaje | `[120.000, 200.000)` | vuelta al original | `n3` = mordidas de B **desde t=120.000** hasta `W_B ≤ −2.5` |

**Ahorro** ≡ `(n1 − n3) / n1`. Positivo = reaprende más rápido = hay traza latente.

`n1` y `n3` cuentan **mordidas de B**, no pasos de tiempo, porque la tasa de mordida cambia entre fases y
comparar tiempos mezclaría política con aprendizaje (regla 4).

**Censura**: si el criterio no se alcanza en su fase, `n1` o `n3` quedan vacíos y esa semilla **no** entra en
la mediana del ahorro; se reporta el recuento de censuradas por brazo. **No se rebaja `crit_miedo` para que
salgan** (regla 3).

## 3. Brazos

| brazo | organismo | parámetros | qué representa |
|-------|-----------|-----------|----------------|
| `v6` | v6 | — | **el patrón de referencia**: sin decaimiento, coexistencia intacta |
| `v7_control` | v7g | `lam=0` | v7 tal cual; separa el efecto de la plasticidad del efecto del decaimiento |
| `exp2` | v7g | `lam=0.05, piso=0` | el arreglo preregistrado del exp. 2 |
| `total` | v7g | `lam=1.0, piso=0` | exp. 3, normalización opuesta completa |
| `piso_025` | v7g | `lam=1.0, piso=0.25` | |
| `piso_050` | v7g | `lam=1.0, piso=0.5` | el piso que propuso la dirección |
| `piso_100` | v7g | `lam=1.0, piso=1.0` | |

Cada brazo con `solap_AB ∈ {0, 1}`. `v7_control` es imprescindible: sin él, cualquier diferencia contra v6
podría venir de la plasticidad estructural y no del decaimiento.

## 4. Criterio, escrito antes — el que fijó la dirección

> **Si el ahorro mediano de un brazo cae por debajo del 50% del ahorro mediano de `v6`, ese brazo compra
> rango vendiendo memoria latente, y NO se congela por defecto: se lleva a decisión de dirección.**

Formalmente, con `Ahorro(b)` = mediana sobre las semillas no censuradas del brazo `b`:

```
VENDE_MEMORIA(b)  ≡  Ahorro(b) < 0.50 · Ahorro(v6)
```

Predicciones puntuales, para que el resultado pueda equivocarme:

- **A1**: `Ahorro(v6) > 0`, y con margen — si v6 no ahorra, la prueba no mide nada y hay que rediseñarla
  antes de leer ningún otro brazo. **Es el control que valida el instrumento.**
- **A2**: `VENDE_MEMORIA(total)` = **verdadero**. Con `λ_c=1` el canal menor queda en 0 tras cada mordida:
  no puede quedar traza.
- **A3**: `VENDE_MEMORIA(exp2)` = **falso**. `Wp*=1.8` sobre un techo de 9 deja coexistencia de sobra.
  **Si sale verdadero, el arreglo del exp. 2 no se congela**, y la objeción de la dirección se lleva la
  decisión entera.
- **A4**: el ahorro crece monótonamente con el piso: `Ahorro(total) ≤ Ahorro(piso_025) ≤ Ahorro(piso_050)
  ≤ Ahorro(piso_100)`. Es la predicción que hace falsable el mecanismo: si el piso no ordena el ahorro,
  la traza latente no vive donde creemos.

## 5. Recuperación espontánea — y un hecho del instrumento que la condiciona

**Hallazgo previo, verificado leyendo el código, no supuesto**: en v6 y en todas las variantes, `Wp` y `Wn`
**sólo se modifican dentro de `if mordio:`** (v6 líneas 52–58; el decaimiento de v7e/v7f está en el mismo
bloque). No existe ningún proceso dependiente del tiempo.

> **Con `A∩B = 0`, la recuperación espontánea es imposible por construcción**: sin mordidas de B no hay
> cambio, y morder A no toca celdas de B. Mediría cero en todos los brazos y no diría nada de ninguno.

Por eso la prueba se corre con `solap_AB ∈ {0, 1, 2}`, y **`solap_AB = 0` es el control negativo**:

- **A5 (control negativo)**: con `solap_AB = 0`, `wB_post − wB_pre` = **0.000 exacto** en 20/20, en todos los
  brazos. Si no sale exacto, el instrumento está roto y el bloque entero se descarta.
- **A6**: con `solap_AB ∈ {1, 2}`, `wB_post − wB_pre < 0` (el miedo reaparece) en `v6` con más frecuencia que
  en `total`. Predicción **direccional, sin cifra**: no hay base para una puntual y no me la invento.

Diseño del bloque: extinción en `t=60.000`, ventana **sin B** en `[120.000, 160.000)`, medición de `W_B` al
entrar y al salir de la ventana. Sin fase 3.

## 6. Métricas

Por semilla y brazo: `n1`, `n3`, `nB`, `nB3`, `wB_ext`, `wB_pre`, `wB_post`, `W_A`, `W_B` finales,
`Wp_B`/`Wn_B` finales, techo tocado, `splits`, `celdas`, `deaths`. Medianas y rangos (regla 6).

## 7. Controles obligatorios

1. **Inercia de las variantes**: `v6s` con `revertir_en=None, sin_B=None` bit-idéntico a `v6`; `v7g` con
   `lam=0` idem contra `v7`. En los 7 escenarios × 6 semillas.
2. **A1**: `Ahorro(v6) > 0`. Si falla, no se lee ningún otro brazo.
3. **A5**: control negativo de recuperación exacto en 0.000.
4. `bateria.py 20` todo PASA y `manifiesto.py` con los cuatro congelados intactos, antes y después.

## 8. Qué se decide con esto

- Si **A3 se sostiene** (exp. 2 no vende memoria) y el arreglo pasa la batería completa → sigue vivo como
  candidato, y se pasa al **paso 2**: repetir 3T como confirmatorio con preregistro nuevo, **sin mirar los
  números del post-hoc**.
- Si **A3 se refuta** → el arreglo del exp. 2 **no se congela**. Se lleva a dirección la disyuntiva
  rango-contra-memoria, con los brazos de piso como opción intermedia medida.
- En cualquier caso, **v6 sigue siendo el tronco** hasta que un candidato pase todo.

## 9. Procedencia

Los ciclos de barrido los puede producir `sandbox/tareas/T02_prueba_ahorro.md` (ejecutor externo). **Nada de
ahí entra en el registro sin reproducirse en el repo** con la regla de cruce de `sandbox/README.md`. El
análisis, los veredictos y este preregistro son del repo y no se delegan.
