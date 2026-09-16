# BUG-01 exp. 2b — corrección de instrumento (ERR-07) y reejecución de P2

**Escrito ANTES de correr nada. Fecha: 15 sep 2026, día 3, tarde.**
Dirección: Christiam Puentes. Corrige `PREREGISTRO_exp2.md` (sha `8786ad6382e255f5`), que queda vigente en
todo lo demás.

**Los veredictos del exp. 2 ya corridos NO se borran ni se recalculan.** Quedan registrados como salieron
(`datos/bug01_exp2_20260915_183244.json`, sha `1eb82a17119e5447`). Esto es una reejecución con instrumento
corregido, no una reinterpretación de aquélla (regla 3).

---

## 1. ERR-07 — qué falló exactamente

En `corre_bug01_exp2.py` (sha `968b49172c54a16c`), la comprobación de inercia de P2 es:

```python
ident = all(a == b for a, b in zip(R(esc, 0.0), rs))
```

`R(esc, lam)` devuelve los dicts que produce `tarea()`, y esos dicts **contienen la propia clave `lam`**
(línea 41: `return dict(esc=esc, lam=lam, seed=seed, ...)`). Al comparar el brazo `lam=0.0` con el brazo
`lam=0.05`, la clave `lam` difiere **por construcción**.

> **`ident` era estructuralmente `False`. No podía dar `True` bajo ninguna circunstancia, ni aunque el
> organismo fuese literalmente el mismo.** El chequeo no medía inercia: medía que 0.0 ≠ 0.05.

Es el séptimo error de instrumento del proyecto y el séptimo de siete anomalías (regla 5, otra vez).

**Corrección**: comparar ignorando las tres claves de etiqueta, que no son resultado sino índice:

```python
sin_etiquetas = lambda r: {k: v for k, v in r.items() if k not in ('esc', 'lam', 'seed')}
ident = all(sin_etiquetas(a) == sin_etiquetas(b) for a, b in zip(R(esc, 0.0), rs))
```

Aplicada a los datos ya guardados, el resultado real es: **E1 20/20**, E2I 6/20, E2J 0/20.

## 2. ERR-07b — la categoría `SIN_CONFLICTO` estaba mal definida

Error de preregistro, no de código. `PREREGISTRO_exp2.md` §3 declaró `SIN_CONFLICTO = (E1, E2I, E2J)`
razonando "un solo canal activo → `min(Wp,Wn)=0` → inerte". Eso es correcto como mecanismo y falso como
clasificación, por dos motivos distintos:

- **E2J es conflicto por definición.** Su escenario es `nuevo='D', nuevo_val='comida', solap_B=1`: fuerza un
  solapamiento de **una celda** entre D (comida, R=+1) y B (veneno, R=−3). Una celda que recibe premio y
  castigo es la definición exacta de conflicto de signo. Ponerlo en `SIN_CONFLICTO` fue un descuido de
  redacción: el escenario dice en su propio nombre lo contrario.
- **E2I es mixto, semilla a semilla.** El escenario añade C (veneno) y el bucle de rechazo de `run()` sólo
  restringe `A∩B=0`; **no restringe el código de C**. C puede solapar con A (comida, valencia opuesta) o con
  B (veneno, misma valencia pero el conflicto sale de A). Así que cada semilla cae de un lado o del otro.

## 3. Definición nueva, mecánica y por semilla

Un par (escenario, semilla) es **SIN_CONFLICTO** si y sólo si **todos** los solapamientos entre códigos de
estímulos presentes valen 0:

```
solap_cero(esc, seed)  ≡  |code(A) ∩ code(B)| = 0
                      ∧  ( no hay estímulo nuevo N,  ó  |code(N) ∩ code(A)| = 0 ∧ |code(N) ∩ code(B)| = 0 )
```

Se evalúa **midiendo los códigos**, no por escenario y no a mano. Consecuencias, que no se eligen:

| esc | clasificación | por qué |
|-----|---------------|---------|
| E1   | SIN_CONFLICTO, 20/20 | `A∩B=0` impuesto por el bucle de rechazo; no hay más estímulos |
| E2I  | **mixto, se mide por semilla** | el código de C no está restringido |
| E2J  | CON_CONFLICTO, 20/20 | `solap_B=1` fuerza D(comida)∩B(veneno) |
| E2, E2K, E2L | CON_CONFLICTO | inversión de valencia / solapamiento forzado |

**El script clasifica calculando el solapamiento en cada corrida. No lleva ninguna lista de semillas
escrita a mano.** Esto importa: una lista fija sería ajustar la categoría al resultado, que es justo lo que
la regla 3 prohíbe.

## 4. Predicciones de la reejecución — escritas antes de correr

**P2a (inercia donde toca).** En todo par (esc, seed) con `solap_cero`, el resultado con `lam=0.05` es
**bit-idéntico** al de `lam=0.0` en todas las claves de resultado. Criterio: **100%**, sin una excepción.

**P2b (control positivo: el arreglo actúa donde hay conflicto).** En los pares **con** conflicto, el
resultado **NO** debe ser bit-idéntico. Criterio: **0%** de idénticos.
Esta predicción es tan necesaria como P2a: si todo saliera idéntico, el decaimiento no estaría haciendo nada
y P1 sería un espejismo.

**P2c (criterios científicos).** Las seis etapas siguen pasando **20/20** sus criterios de conducta y valor,
como ya pasaron en el exp. 2.

**Qué refuta**: cualquier par `solap_cero` que difiera; cualquier par con conflicto que salga idéntico;
cualquier etapa que baje de 20/20.

## 5. Lo que NO cambia

- `organismo_v7e.py` (sha `3118c6d563542da2`) **no se toca**. El organismo bajo examen es el mismo byte a byte.
- `LAM = 0.05` sigue fijado a priori por la derivación de `PREREGISTRO_exp2.md` §2. **No se recalibra.**
- P1, P3 y P4 conservan sus criterios originales. P1 sigue **REFUTADA** por su tercer subcriterio, y esa
  refutación **no se revisa aquí**: es un fallo de la predicción sobre la dispersión de `W`, no del instrumento.
  Ver §6.

## 6. Nota sobre P1, para que no se confunda con esto

P1 falló **sólo** en `W ∈ [−1.5, −0.5] en ≥18/20`. Los otros dos subcriterios pasaron: techo despejado 20/20 y
`Wp`/`Wn` medianos en 1.77/3.04 contra 1.8/2.8 predichos (±0.5). La predicción `W_eq = −1` supuso mezcla
exacta 50/50 de mordidas A:B; la mezcla real la fija la política y varía por semilla, y el rango observado es
[−2.09, −0.30]. **Es un fallo de la capa de política, no del mecanismo** (regla 4). Se registra como refutada
y punto. Cualquier criterio nuevo sobre la dispersión de `W` exige su propio preregistro, escrito antes.

## 7. La sonda de códigos y su control

Para clasificar hace falta leer los códigos finales, que `organismo_v7e.run()` no devuelve. Se usa
`sonda_codigos.py`: copia de `organismo_v7e.py` con **una sola** línea añadida que exporta
`{estímulo: código}`.

**Control obligatorio, y el script aborta si falla**: la sonda tiene que ser **bit-idéntica** a
`organismo_v7e.py` en todas las claves compartidas, en los 7 escenarios × 6 semillas. Si no lo es, la sonda
no es el mismo organismo y la clasificación no vale.

## 8. Cómo correrlo

```
cd bundle
python experimentos\bug01\corre_bug01_exp2b.py 20
```

Escribe `datos/bug01_exp2b_<fecha>.json`. ~8 minutos con 16 núcleos.
