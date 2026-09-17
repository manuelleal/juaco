# Capacidad de v11 en un mundo GRANDE — ¿dónde está su límite y quién se lo pone?

**Escrito ANTES de correr. 17 sep 2026, día 5.** Dirección: *"corre un mundo más grande"*, tras la advertencia de que
el instrumento de capacidad se saturó (v11 aprendió los 20 estímulos que existían: `N* = 20` era el **techo de la prueba**).

## 0. Qué se sabe y por qué este diseño

- Ayer, en 2K-bis (20 patrones de peso 3 sobre 6 píxeles), semillas 41–60: **v11 `N*` = 20 y 20** (a 20k y 60k),
  **v10** 5.0 y 8.5, **sin agotar** el pool de 90 celdas (v10 lo agotaba en 12/20 a 60k). El techo del instrumento
  impide saber la capacidad real de v11.
- **Mundo nuevo:** retina de **10 píxeles**, estímulos de **peso 3** (familia C(10,3) = 120), **60 estímulos**,
  valencias alternando comida/veneno, uno nuevo cada `paso_t`. Mismas convenciones y métricas que 2K-bis
  (`N*` = mayor n con mediana |W−R| ≤ 0.3 en todos los checkpoints hasta n; `M_max`; TOL 0.3).
- **El organismo no cambia.** Sigue con `NK = 30` celdas de nacimiento y `NKMAX = 90`: 60 libres. Si cada estímulo
  nuevo en conflicto consume hasta 3 hijas, el pool se agota alrededor de los 20–30 estímulos.
- **Humo declarado** (semilla 41, 40 estímulos, paso 2.000, v11): agota el pool en t = 68.410, 60 divisiones,
  `M_max` 17, `N*` 1 (paso demasiado corto para aprender cada estímulo: por eso el diseño usa 20k y 60k).
- **G0 [instrumento], ya comprobado y declarado:** `mundo_grande(6, 20)` produce patrones, valencias, plan y
  checkpoints **idénticos** a `parte2_capacidad`; y `organismo_capD` con patrones de 6 píxeles es `organismo_caph11`
  **exacto** en todas las claves (semillas 1–3, brazos v9 y v11).

## 1. Diseño

`organismo_capD.py` (`85afad3f0769891f`, generado por anclas desde `organismo_caph11.py` `a34d3309221cc6c7`),
`mundo_grande.py`. Brazos: **v9** (`mu_norm=False, div_signo=False`), **v10** (`True, False`), **v11** (`True, True`),
con `lam=0.05`, `memoria_rechazo=20`, `plast=True`. `paso_t ∈ {20.000, 60.000}`, 60 estímulos, **semillas 41–60**
(las mismas del confirmatorio de v11; se declara). 120 corridas de 1,2 M y 3,6 M pasos.

**Cantidad derivada nueva:** `N_agot` = número de estímulos presentes cuando se agotó el pool = `1 + t_agot/paso_t`
(si no se agota, `N_agot = 60`, censurado). Sirve para preguntar **quién pone el límite**.

## 2. Criterios y predicciones

- **G1 [la capacidad de v11 supera el techo viejo]:** mediana de `N*(v11)` ≥ **20** en 20k **y** en 60k.
  *Predicción: 25–40.*
- **G2 [la ventaja no era del mundo pequeño]:** mediana `N*(v11)` − mediana `N*(v10)` ≥ **+5** en los dos pasos.
  *Predicción: +15 o más.*
- **G3 [mecanismo: a v11 el límite se lo pone el POOL DE CELDAS, no la interferencia]:**
  en v11, `|N* − N_agot| ≤ 5` en ≥ **14/20** semillas; en v10, `N* ≤ N_agot − 5` en ≥ **14/20**.
  *Predicción: se sostiene; v11 agota el pool en ≥ 15/20 semillas y su `N*` cae cerca de ahí.*
- **Sin voto:** `M_max`, celdas, divisiones, muertes, `W = 0` exactos, y la curva de degradación tras el agotamiento.

## 3. Qué se decide

- **G1 y G2 se sostienen:** la capacidad de v11 es **real y mayor**, no un artefacto del mundo de 20. Se registra el
  número medido y el instrumento nuevo queda como referencia.
- **G1 falla (mediana < 20):** la lectura de ayer era del techo del instrumento; se corrige el registro y se dice que
  v11 **no** multiplica la capacidad, sólo aguantaba el mundo pequeño.
- **G3 se sostiene:** se puede escribir que **en v11 el límite de capacidad es estructural (celdas disponibles)**, no
  de rango dinámico. Eso convierte "más celdas" en una predicción comprobable para v12, y es lo que hay que decir en
  vez de "capacidad 20".
- **G3 falla:** el límite es otro (interferencia, energía, muertes); se registra y se investiga.

## 4. Qué NO prueba

No prueba retención con más estímulos **ausentes** que celdas (eso es la Etapa 4 a gran escala, pendiente), ni
generalización a patrones nuevos (Etapa 3 sobre v11, pendiente), ni que 90 celdas sean el número correcto: sólo mide
cuántos estímulos simultáneos sostiene el organismo **congelado** y quién le pone el techo.
