# BUG-01 — Experimento 1: decaimiento local en Wp/Wn

**Escrito ANTES de tocar una línea de código y ANTES de correr nada. Fecha: 15 sep 2026 (día 3).**
Dirección: Christiam Puentes ("arregla BUG-01, empieza por el decaimiento"). Ejecución: Claude.
Trabajo dirigido al TRONCO, no es rama. Formato según el punto 19 del brief:
qué prueba · qué cambia · qué esperamos · qué la refuta · qué métricas · qué controles.

---

## 1. Qué prueba

**BUG-01, diagnosticado hoy (registro, día 3).** Bajo refuerzo contradictorio sobre un código compartido,
`Wp` y `Wn` crecen **los dos** hasta el techo del clip (3.0 por celda = 9.0 por código de 3 celdas) y su
diferencia se anula **exactamente**. A partir de ahí no se puede aprender nada más en esas celdas: con
`Wp = Wn = 3.0`, un error positivo no puede subir `Wp` y uno negativo no puede subir `Wn`. El aprendizaje
queda congelado, no lento: congelado.

Reproducible sobre el organismo congelado, sin modificarlo:

    organismo_v7.run(1, plast=False, solap_AB=3)
      -> comp = {'A': (9.0, 9.0), 'B': (9.0, 9.0)},  W = {'A': 0.0, 'B': 0.0}
    control E1 normal:  A=(1.0, 0.0),  B=(0.0, 3.0)   <- sin inflar

Es el mismo fenómeno que el registro anotó tres veces sin nombrarlo: *"v6 colapsa: W=0"* (2L),
*"ambos canales saturan en 9, sin freno al apetitivo"* (2F), *"canales inflados"* (2J/2K).

## 2. Qué cambia — UN solo cambio

En el bloque de aprendizaje de la boca, un **decaimiento multiplicativo local** aplicado a `Wp` y `Wn`
**sólo en las celdas del código activo** y **sólo en el momento de morder** (es decir, sólo cuando esas
celdas participan en un evento de aprendizaje):

```python
if lam: idx = kc > 0; Wp[idx] *= (1-lam); Wn[idx] *= (1-lam)
```

insertado justo después de calcular `dlt` y antes de la actualización, de modo que `dlt` se sigue
calculando con los valores previos. **Nada más cambia.** `eta`, `aversion`, el clip, `theta`, `ema`,
`paso`, la política y el mundo quedan intactos.

**Dos decisiones de diseño, justificadas por principio y no por conveniencia:**

- **Local, no global.** El decaimiento toca sólo las celdas del código que se está mordiendo. Un
  decaimiento global (cada paso, todas las celdas) destruiría el valor de los estímulos que el organismo
  no está visitando y rompería E2I ("aprende C sin degradar A/B"), que es un resultado establecido.
  Con 100k pasos, incluso un decaimiento global de 1e-5 por paso dejaría el valor en el 37% de su magnitud.
- **Simétrico.** Decae en los dos canales por igual. No se elige a mano cuál frenar.

**λ = 0.001, fijado a priori por el siguiente argumento, no por barrido.** El equilibrio analítico se deriva
abajo y vale `W* = 3·eta·R / (3·eta + λ)`. λ = 0.001 es el valor para el que ese equilibrio queda dentro
del **1.1%** de la recompensa. Se declara un barrido de sensibilidad λ ∈ {0.0003, 0.003, 0.01} que
**NO decide** el veredicto, sólo describe la forma de la curva.

## 3. Qué esperamos — predicción numérica derivada

Por mordida, con `W` = valor neto del código (suma de sus 3 celdas), el orden es: decaer, luego actualizar.

    W_nuevo = (1-λ)·W + 3·eta·(R − W)

Equilibrio (`W_nuevo = W`):   **W\* = 3·eta·R / (3·eta + λ)**

Con `eta = 0.03` (3·eta = 0.09) y `λ = 0.001`:

| | sin decaimiento | con λ = 0.001 | criterio de la batería |
|---|---|---|---|
| W_A (R = +1) | +1.000 | **+0.989** | \|W_A − 1\| < 0.15 → pasa |
| W_B (R = −3) | −3.000 | **−2.967** | \|W_B + 3\| < 0.3 → pasa |

Constante de tiempo ≈ 1/(3·eta+λ) ≈ **11 mordidas**: el equilibrio se alcanza rápido y no cambia la
dinámica observable de aprendizaje.

**P1 — Desbloqueo (criterio primario).** En el escenario del bug (`plast=False, solap_AB=3`), donde hoy
`Wp = Wn = 9.00` y `W = 0.00` en 20/20:
- `max(Wp)` y `max(Wn)` por código quedan **estrictamente por debajo de 9.00** en **20/20** semillas.
- `W` deja de estar congelado en 0 y converge al **promedio de recompensa**. Con A y B compartiendo código
  al 50/50, ese promedio es (+1 −3)/2 = −1. Predicción: **W ∈ [−1.5, −0.5] en ≥18/20**.
  (Con códigos idénticos y sin plasticidad, W_A = W_B por fuerza: la representación es degenerada y
  converger a la media es la conducta CORRECTA. Lo que se arregla no es la representación, es el bloqueo.)

**P2 — No regresión.** `bateria.py 20` sigue pasando **5/5 etapas 20/20**, y `bateria_v7b.py 20` da
**los mismos veredictos** que hoy (seis etapas 20/20 en criterios científicos, control negativo 0/20,
E2I 18/20 en disparo).

**P3 — Precisión del valor.** Las medianas de W_A y W_B coinciden con el equilibrio analítico
(+0.989 y −2.967) dentro de **±0.02**. Es la prueba de que entendemos el mecanismo y no sólo de que
"funciona".

**P4 — La ley de valencia se conserva.** El decaimiento no debe cambiar el patrón de disparo medido hoy
(divide con ≥2 celdas compartidas entre valencias opuestas; no divide con misma valencia).

## 4. Qué lo refuta

El experimento queda **REFUTADO** si ocurre cualquiera de estas:
- Los canales **siguen clavándose** en el techo (max ≥ 9.00 en alguna semilla del escenario del bug) → el
  decaimiento no ataca el mecanismo.
- **Cualquier etapa** de `bateria.py 20` deja de pasar 20/20 → el arreglo cuesta más de lo que vale.
- W_A se aleja de +1 más de 0.15, o W_B de −3 más de 0.3.
- Las medianas observadas **no** coinciden con el equilibrio analítico dentro de ±0.02 → hay algo en el
  mecanismo que no entendemos, y eso es más importante que el arreglo.
- `bateria_v7b.py` cambia algún veredicto respecto a hoy.

**No se recalibrará λ a posteriori.** Si λ = 0.001 falla, se registra el fallo y se decide un λ o un
mecanismo nuevo antes de volver a correr (regla 3).

## 5. Qué métricas

Por semilla: `Wp` y `Wn` por código (máximo y por celda), `W` de cada estímulo, nº de celdas en el techo,
paso en que se alcanza el techo si se alcanza, mordidas, muertes, tasas por visita por cuarto, `splits`,
`split_t`, celdas activas. Medianas y rangos siempre (regla 6). 20 semillas, T = 100.000.

## 6. Qué controles

1. **Inercia del código nuevo**: `organismo_v7d.py` con `lam = 0.0` debe ser **bit-idéntico** a
   `organismo_v7.py` en todos los campos, sobre los 7 escenarios × 6 semillas. Si no lo es, el
   instrumento está sucio y se para (regla 5, y es el mismo protocolo usado para v7 vs v7c y para la sonda
   de Etapa 3).
2. **Control negativo**: `lam = 0.0` en el escenario del bug debe seguir dando `(9.0, 9.0)` y `W = 0.0`.
   Si el bug no se reproduce con el decaimiento apagado, el escenario está mal montado.
3. **Barrido de sensibilidad** λ ∈ {0.0003, 0.003, 0.01}, declarado de antemano como descriptivo:
   **no decide el veredicto**.

## 6-bis. ADENDA — añadida a las 12:5x del 15 sep, DESPUÉS de que cayera la rama 2K-bis y ANTES de correr nada de este experimento

2K-bis terminó mientras se escribía este preregistro y llega **por su cuenta** a BUG-01 como causa raíz de su
resultado principal: el 82% de los valores finales de v7 valen 0.000 exacto, y en **169/169** de esos casos
`Wp·kc = Wn·kc = 9.000`. Su conclusión, textual: *"el límite de esta arquitectura no está en el número de celdas
Kenyon, sino en el rango dinámico de los canales de valor. Dividir compra separación; no compra rango."*

Eso convierte la capacidad en una **prueba independiente y más exigente** del mismo arreglo. Se añade como
predicción NUEVA (no se modifica ninguna de las anteriores; se deja constancia de que se añade antes de correr):

**P5 — Capacidad.** Con el decaimiento activo, en el diseño de capacidad de 2K-bis (familia completa de los 20
patrones de peso 3, un estímulo nuevo cada 60.000 pasos, 20 semillas):
- la fracción de valores finales exactamente 0.000 debe caer **por debajo del 20%** (hoy 82%);
- el máximo de estímulos simultáneamente bien aprendidos (|W−R| ≤ 0.3) debe **subir respecto a v7 (hoy 4)**;
- y debe **dejar de cumplirse** que v7 sea peor que v6 en capacidad (hoy v7 gana sólo en 6/20).

**Refuta P5**: que la fracción de ceros siga por encima del 50%, o que el máximo de estímulos bien aprendidos
no suba. P5 **no** decide el veredicto de P1–P4; es una prueba adicional del mismo mecanismo en otro terreno.

**Nota sobre la ley de disparo**, que 2K-bis también refuta y que NO es objeto de este experimento: el umbral no
está en el número de celdas compartidas sino en `err > 0.6`, con concordancia 320/320 y derivación analítica
(`err_max = 0.147509·|R|`, que exige `|R| efectivo > 4.068` — imposible sin recompensas de signo opuesto sobre
la misma celda). Mi "ley de valencia" de esta mañana es una **consecuencia** de eso, no el primitivo, y también
es falsa como enunciado general (con A∩B=1 co-aprendido desde t=0 dividen 8/20). Se corrige en el registro.

## 7. Coste conocido y aceptado de antemano

El decaimiento **rompe la convergencia exacta a la recompensa**, que es un resultado destacado de 2G
("los valores convergen exactamente a la recompensa, W_A→+1.00 y W_B→−3.00"). Pasa a +0.989 y −2.967:
un **1.1% de sesgo hacia cero**, sistemático y predicho por la fórmula. Los criterios de la batería lo
absorben, pero la afirmación de exactitud habría que reescribirla como "converge al valor predicho por
`3·eta·R/(3·eta+λ)`". Se anota ahora, antes de ver resultados, para que no parezca un descubrimiento a
posteriori.

**Candidato para el experimento 2, anotado aquí y NO probado en éste** (un cambio por experimento):
decaer sólo la **parte común** de los dos canales — `m = min(Wp, Wn); Wp -= λ·m; Wn -= λ·m` — que ataca
exactamente la patología (los dos canales inflados a la vez) **sin tocar la diferencia**, y por tanto
preservaría la convergencia exacta. Si el experimento 1 sale bien pero el coste del 1.1% molesta, ése es
el siguiente paso. No se prueba aquí para no mezclar dos cambios.
