# PREREGISTRO — Rama 3K: ¿hace falta APRENDER la expansión Kenyon, o basta el azar?

**Escrito el 15 sep 2026 ANTES de correr una sola condición de la hipótesis.**
Rama exploratoria. NO es tronco. No toca `organismo/`, `registro/`, ni ficheros existentes de `datos/`.
Regla 2 del proyecto: hipótesis, predicción numérica, criterio de refutación y métricas, escritos antes.
Regla 3: no se recalibra nada a posteriori. Si un criterio sale mal escrito, se registra el error y se
decide uno nuevo ANTES de volver a correr.

---

## 0. La pregunta

La capa Kenyon de v6 es un sorteo congelado: `KW = rng.uniform(0,1,(30,6))` se saca una vez al nacer y no
aprende nunca. De ahí cuelgan la generalización (Etapa 3), la interferencia de 2I, el conflicto de 2J, el
techo de 2K y el umbral de división de 2L. La mosca tiene el cuerpo fungiforme cableado de forma casi
aleatoria y le funciona. **¿Cuándo basta el azar y cuándo hace falta aprender las características?**

El PREREGISTRO de Etapa 3 predice `W_X = (nA/3)·W_A + (nB/3)·W_B`: el valor a priori de un patrón nunca
visto lo decide el solapamiento de códigos, es decir, un sorteo anterior a la experiencia. Esta rama
construye la tarea donde esa propiedad debería ser un defecto medible, y mide si una regla local de
aprendizaje de KW lo corrige.

---

## 1. Mundo diseñado para separar azar de aprendizaje

Lo relevante es **una regla sobre los píxeles**, no un patrón concreto.

- Universo: los **20 patrones binarios de 6 px con exactamente 3 px activos** (`C(6,3)=20`).
- **La valencia la decide el píxel 0**: `px0=1` → comida (R=+1.0), `px0=0` → veneno (R=−3.0).
  Hay 10 de cada clase. Los otros 5 píxeles son irrelevantes por diseño.
- **Entrenamiento**: 10 patrones (5 comida + 5 veneno). **Test**: los otros 10 (5 + 5), que el organismo
  **no ve jamás** durante la fase 1.
- `T = 200000`. Fase 1 = pasos 0–99.999 (sólo patrones de entrenamiento). En `t = 100.000` se sondea el
  valor a priori de los 20 patrones y **acto seguido** entran los 10 de test al mundo. Fase 2 = 100.000–199.999.

**Justificación de la desviación respecto al ejemplo del brief (16+16 de los 64):** fijar `px0=1` quita un
grado de libertad, de modo que cualquier subconjunto de los 64 balanceado en clase queda **desbalanceado en
luminancia** (la clase comida tendría más píxeles activos en media). Eso daría una pista trivial —"brilla
más, es comida"— que un sistema puede explotar sin aprender nada de la característica. Con luminancia fija
en 3 px activos el desbalance desaparece por construcción y la **única** señal utilizable es el píxel 0.
Precio: 20 patrones en vez de 32, 10+10 en vez de 16+16. Se acepta: el control vale más que los 12 patrones.

**Partición**: sorteada con un RNG propio (`default_rng(10000+semilla)`), **idéntica en todas las
condiciones de la misma semilla**, distinta entre semillas. Así el resultado no depende de una partición
arbitraria y la comparación entre condiciones es pareada.

**Desviación obligada:** v6 rechaza sorteos de KW hasta que `code(A)∩code(B)=0`. Con 20 patrones × 3 celdas
sobre 30 celdas eso es imposible (principio del palomar) y además el solapamiento accidental es el objeto de
estudio. En `mundo='regla'` **no hay muestreo por rechazo**. En `mundo='AB'` se conserva intacto.

**Instrumento verificado antes (regla 5):** `equivalencia_3k.py` → `organismo_3k.run(mundo='AB',
kenyon_mode='fijo')` es **bit-idéntico a `organismo_v6.run()`, 24/24** escenarios × semillas (E1, E1 sin
aprender, E2 inversión, E2I, E2J, E2K; semillas 1–4). Cero llamadas nuevas al RNG.

**Piloto de dimensionado (instrumento, no hipótesis), 3 semillas, condición 1**, declarado aquí: se miró
**sólo** muertes, visitas por patrón de ENTRENAMIENTO, valor final de los patrones de ENTRENAMIENTO y número
de celdas usadas. **No se miró ninguna métrica de los patrones de test.** Resultado: la tarea es aprendible
(W comida ≈ +0.6/+1.0, W veneno ≈ −3.2/−3.4), muertes 150–162 a T=100k, y **sólo 16–21 de las 30 celdas
participan en algún código, con una celda presente en hasta 19 de los 20 códigos**. Fija T=200k y fase2=100k.

---

## 2. Las tres condiciones (un cambio entre cada par)

Regla local común, sin gradiente y sin backpropagation. Cuando una celda gana (está en el top-3 del patrón
actual), su vector de entrada se acerca al patrón y la fila se renormaliza a **su norma de nacimiento**:

```
KW[i] <- KW[i] + lr*(P - KW[i])
KW[i] <- KW[i] * n0[i]/||KW[i]||
```

Conservar `n0[i]` garantiza que en `t=0` los códigos de las cuatro condiciones son **idénticos**: sólo se
aprende la *dirección* de cada celda, nunca la *ganancia* que le tocó en el sorteo. No hay confusión en t=0.

| Cond. | `kenyon_mode` | Qué cambia respecto a la anterior |
|---|---|---|
| **1** | `fijo` | — (es v6: KW aleatorio y congelado) |
| **2** | `hebb_visita` | KW aprende, en **cada visita**, con lr constante. Competitivo puro, sin recompensa. |
| **2b** | `hebb_mordida` | Igual que 2 pero sólo **al morder**. Control para aislar la modulación. |
| **3** | `error` | Igual que 2b pero el lr va **modulado por \|error de predicción\|**: `lr·min(\|δ\|/3, 1)`, con `δ = R − (Wp−Wn)·kc`. Misma señal que usa 2L para decidir cuándo dividir. |

`2 → 2b` aísla "cuándo se actualiza"; `2b → 3` aísla **la modulación por error**, que es el único cambio que
importa para la hipótesis. Los tres comparten el mismo `k_lr`.

**Tasa de aprendizaje `k_lr`: fijada A PRIORI, no ajustada.** Primaria `k_lr = 0.01` (≈ convergencia completa
del prototipo en ~300 actualizaciones, y tres veces más lenta que `eta=0.03` del valor: la representación se
mueve más despacio que el valor que sostiene). Se declara además un barrido de sensibilidad
`k_lr ∈ {0.003, 0.01, 0.03}` para 2, 2b y 3, que se reporta pero **no decide**. `error@0.03` funciona además
como "condición 3 con tasa de pico igualada a 2b@0.01" (la modulación media es ≈1/3), y se reporta como
robustez, nunca como primaria.

**Confusión conocida y declarada:** la condición 3 mueve KW **menos** en total que 2b con el mismo `k_lr`
(la modulación es ≤1 y decae a 0 al converger). La dirección de esa confusión es **conservadora contra la
hipótesis**: si 3 gana, no es por moverse más.

**Dos variantes de la fase 2, ambas corridas para todas las condiciones:**
- **`congelado`**: toda la plasticidad (Wp, Wn, Wl, KW) se apaga en `t=100.000`. La conducta en fase 2 es
  **generalización pura de tiro cero**, sin una gota de aprendizaje nuevo. **Es la variante primaria.**
- **`aprende`**: la plasticidad sigue. Da la trayectoria por cuarto. Es secundaria.

---

## 3. Métricas

Sea, sobre los 10 patrones de TEST y un bin temporal dado:
`tasa_comida` = media **macro** sobre los 5 patrones de test-comida de `mordidas/visitas`;
`tasa_veneno` = ídem sobre los 5 de test-veneno.

> **PRECISIÓN = exactitud balanceada** `= 0.5·tasa_comida + 0.5·(1 − tasa_veneno)`.
> Se usa la forma balanceada y macro porque el veneno rechazado **permanece en el mundo y acumula visitas**
> (el piloto lo muestra: hasta 5.700 visitas de un patrón frente a 63 de otro). Una precisión ponderada por
> visitas premiaría a un organismo que no muerde nada. Con la balanceada, **toda política ciega a la clase
> vale exactamente 0.50**: morder todo, no morder nada, o morder al azar. 0.50 es el azar exacto.
> Se reportan SIEMPRE las dos componentes por separado.

1. **Precisión en patrones nuevos** (primaria: variante `congelado`, toda la fase 2; secundaria: variante
   `aprende`, por cuarto de fase 2).
2. **Valor a priori** `W_X` de cada patrón de test leído en `t=100.000`, **antes de su primera mordida**
   (los patrones de test no existen en el mundo antes de ese instante). De ahí:
   `acc_signo` = fracción de los 10 patrones de test con el signo correcto (empate `|W_X|<0.02` cuenta 0.5).
3. **Estructura de KW** (ratios, sobre KW final):
   - `ratio_disp = std(KW[:,0]) / media_{j≠0} std(KW[:,j])` — **el ratio titular**: ¿se despega el peso del
     píxel relevante respecto a los otros 5? Vale 1 por construcción en la condición 1.
   - `ratio_media = media(KW[:,0]) / media(KW[:,1:])` — se espera ≈1 en todas (tarea balanceada); control.
   - `sel_clase` = media sobre celdas usadas de `|f_i − p_i|`, con `f_i`/`p_i` = fracción de los 10 patrones
     de comida / de veneno (de los 20) cuyo código contiene la celda `i`. Selectividad de clase del código.
   - `ratio_solap` = solapamiento medio de códigos **intra-clase** / **inter-clase** sobre los 20 patrones.
   - `celdas_usadas` = celdas presentes en al menos uno de los 20 códigos.
4. **Correlaciones** (sobre los 10 patrones de test de cada semilla, códigos y pesos en `t=100.000`):
   - `r_clase` = Pearson(`W_X`, clase) con clase = +1 comida / −1 veneno.
   - `r_solap` = Pearson(`W_X`, `O_X`) con `O_X = Σ_{Y∈entrenamiento} signo(Y)·|code(X)∩code(Y)|`.
5. **Supervivencia**: muertes, mordidas de comida, mordidas de veneno.

---

## 4. Predicciones numéricas

- **Condición 1 (azar fijo).** El valor a priori de los patrones nuevos lo predice el solapamiento de
  códigos y NO la característica relevante: **`|r_solap| > |r_clase|`** en mediana sobre 20 semillas.
  Precisión en patrones nuevos claramente por encima de 0.50 sólo en la medida en que el solapamiento
  accidental correlacione con el píxel 0. Predicción puntual: **precisión mediana en (0.50, 0.70)**.
- **Condición 2 (Hebb puro).** Los códigos se agrupan por similitud visual, que **no basta**: el píxel
  relevante es 1 de 6 y la similitud visual lo diluye. **Mejora pequeña o nula**: predicción puntual
  **< +5 pp** sobre la condición 1.
- **Condición 3 (modulada por error).** Los códigos se organizan alrededor de lo que importa para el valor.
  **Predicción: precisión mediana ≥ +10 pp sobre la condición 1**, y `ratio_disp > 1.3`.

## 5. CRITERIO DE ÉXITO — el margen, fijado antes de correr

**La condición 3 (`error`, `k_lr = 0.01`, variante `congelado`) supera a la condición 1 si y sólo si se
cumplen LAS TRES cosas:**

**(C-1) Margen.** `mediana_20semillas(precisión_3) − mediana_20semillas(precisión_1) ≥ +0.10`
(diez puntos porcentuales; el 20 % del recorrido útil 0.50→1.00).

**(C-2) Consistencia pareada.** La diferencia por semilla `precisión_3(s) − precisión_1(s)` es **> 0 en
≥ 15 de las 20 semillas**.

**(C-3) No se rompe nada.**
 (a) `bateria_3k.py` con la tarea A/B original y 20 semillas: **E1 pasa 20/20 en las condiciones 1, 2, 2b y 3**
     (criterios idénticos a los de `organismo/bateria.py`: veneno Q4 < Q1, W_A ≈ +1 ±0.15, W_B ≈ −3 ±0.3).
 (b) En el mundo-regla, `mediana(muertes_3) ≤ 1.5 × mediana(muertes_1)`.

**Confirmación mecanística (co-primaria, se reporta siempre, no anula C-1..C-3):**
`mediana(acc_signo_3) − mediana(acc_signo_1) ≥ +0.10`. Si el margen conductual se cumple pero éste no, se
reporta como "conducta sí, valor a priori no" y se investiga el instrumento antes de concluir.

## 6. REFUTACIÓN

**Si (C-1) o (C-2) no se cumplen, la hipótesis queda refutada: para esta tarea el azar basta y la expansión
aleatoria no es el cuello de botella.** Se reporta sin suavizar, sin barrer el `k_lr` a posteriori para
rescatarla y sin reinterpretar el criterio. El barrido `k_lr ∈ {0.003, 0.03}` se reporta como sensibilidad;
si el criterio falla en 0.01 y pasa en otro `k_lr`, **el resultado sigue siendo "falla"** y el otro valor se
reporta como observación abierta para un experimento futuro, no como éxito.

Refutación adicional, independiente: si la condición 3 sube la precisión **degradando la supervivencia**
(C-3b incumplido) o rompiendo E1 (C-3a), el resultado no cuenta como generalización sino como cambio de
política, y se reporta así.

## 7. Qué NO prueba este experimento

Nada sobre otras tareas: la característica relevante aquí es un único píxel, linealmente separable en la
retina. No dice si el azar basta para características conjuntivas (XOR de dos píxeles) ni para más de dos
clases. No dice nada sobre AGI, conciencia ni inteligencia general (regla 8). El vocabulario permitido es
"generaliza" y sólo si (C-1) y (C-2) lo respaldan.

## 8. Plan de corrida

20 semillas (1..20). `multiprocessing.Pool` con `spawn` y guard `__main__`.
Malla: `fijo` + {`hebb_visita`, `hebb_mordida`, `error`} × `k_lr ∈ {0.003, 0.01, 0.03}` = 10 celdas,
× 2 variantes de fase 2 (`congelado`, `aprende`) × 20 semillas = **400 corridas** de 200k pasos.
Salida a `datos/3K_*.csv` y `datos/3K_*.json` con cabecera de procedencia (fecha, sha256 corto de los
scripts, versiones, kwargs). Nunca se sobrescribe nada. Medianas y rangos siempre (regla 6).
