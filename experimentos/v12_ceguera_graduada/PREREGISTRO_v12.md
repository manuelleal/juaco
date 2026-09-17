# v12 — ceguera GRADUADA de la hija: **el mapa del canje** entre recordar y generalizar

**Escrito ANTES de construir el instrumento y antes de correr. 17 sep 2026, día 5.**
Dirección, textual: *"reportas la superficie completa de la perilla, no el mejor punto; y la predicción escrita es que
ningún valor supera a la vez la retención de v11 (20/20) y la generalización de v9 (0.80). Refutación = un punto que
logre las dos. Es un mapa del canje, no su solución."*

## 0. De dónde sale

- v11 cerró la Etapa 4 (retención 20/20) y **perdió la Etapa 3** (valor sobre patrones nunca vistos 0.60 frente a 0.80
  de v9 y v10; azar 0.50).
- Confirmado en 20 semillas (`PREREGISTRO_fuga.md`, D1–D4): las celdas **hijas** de v9 ocupan **1.00 de cada 3** celdas
  del código de un patrón que nunca las entrenó; en v11, **0.08**. Spearman(fuga, acierto) **+0.601**, y **+0.328
  dentro de v9**. **La generalización de v9 era su interferencia.**
- La única diferencia es una línea: en v11 la hija nace ciega fuera de los píxeles de su patrón (`kj * (P > 0)`).
- **Esto es lo que convierte una correlación en un experimento:** aquí **manipulamos la fuga** y medimos las dos cosas.

## 1. La perilla

En el bloque de división por conflicto de signo, la sintonía de la hija pasa a ser:

```
kj = clip(0.95*KW[c] + paso*dist, 0, 5) * ((P > 0) + beta * (P == 0))
```

- **`beta = 0`** → hija totalmente ciega fuera de su patrón = **v11 exacto** (identidad obligatoria).
- **`beta = 1`** → la hija conserva toda su sintonía fuera del patrón: fuga máxima **dentro de la regla de v11**
  (no es v10: el disparo por signo, la madre fija y la fisión del valor siguen ahí).
- **Valores:** `beta ∈ {0, 0.15, 0.30, 0.50, 0.75, 1.0}` — seis puntos, **todos se reportan**.

## 2. Instrumentos

`organismo_v12.py` desde `organismo_v11.py` (`f69e24063be1b194`) por anclas, con `beta` como único parámetro nuevo
(`beta=0.0` por defecto); `organismo_v12m` (bloque M, anclas de v10m/v11m) y `organismo_v12g` (mundo de regla, anclas
de v9g/v11g), los tres generados por `construye_v12.py`.

**Identidades obligatorias (si fallan, se para):** `v12(beta=0)` ≡ v11; `v12m(beta=0)` ≡ v11m; `v12g(beta=0)` ≡ v11g;
7 escenarios × semillas 1–3 en el primero, E1/E2/M × 1–3 en los otros dos.

## 3. Qué se mide, en los seis puntos (semillas 41–60; nada nuevo, todo ya preregistrado antes)

| eje | medida | referencia |
|---|---|---|
| **Retención** | bloque M: `W_B(100k) ≤ −2` **y** `W_A(100k) ≥ 0.5`, sobre 20 | v11 = **20/20**, v9 = 0/20 |
| guarda | `W_C ≤ −2.5` y `W_D ≥ 0.85` | v11 = 20/20 |
| **Generalización** | acierto de valor, regla `px0`, patrones nunca vistos | v9 = **0.800**, v11 = 0.600, azar 0.50 |
| conducta | `BA_pb` al primer encuentro | v9 = 0.801, v11 = 0.672 |
| **Fuga** | hijas ajenas en el código de un patrón nuevo (de 3) | v9 = 1.00, v11 = 0.08 |
| control | regla `azar` | debe quedarse en 0.50 en todos los puntos |
| sin voto | divisiones, celdas, muertes, examen rápido (`bateria_v12.py 6`) en cada extremo | |

**Se reporta la superficie completa**: una fila por `beta`, con las tres columnas (retención, generalización, fuga) y
sus rangos. **No se elige "el mejor punto"**; si alguien lo quiere elegir después, que lo haga con la tabla delante.

## 4. Predicción (la que pide dirección, escrita antes)

> **Ningún valor de `beta` alcanza a la vez la retención de v11 (20/20) y la generalización de v9 (≥ 0.80).**

Forma cuantitativa que se evalúa:
- **H [el canje existe]:** para todo `beta`, **no** se cumple simultáneamente `retención ≥ 20/20` y `acierto ≥ 0.78`
  (0.80 menos la tolerancia de medida 0.02).
- **Refutación de H:** **un solo punto** que logre las dos cosas. Si aparece, **el canje no es necesario**, v12 pasa a
  candidato a tronco con su confirmatorio propio, y hay que explicar por qué el mecanismo lo evita.
- **Forma esperada de la superficie (predicción secundaria, sin voto):** monótona y cruzada — la retención cae al subir
  `beta` (20/20 en 0, ≤ 10/20 en 1.0) y el acierto sube (0.60 en 0, ≥ 0.75 en 1.0), con el cruce entre 0.30 y 0.75.
- **La fuga debe seguir a `beta`:** correlación Spearman(beta, fuga) ≥ +0.9 sobre los seis puntos. **Si no, la perilla
  no manipula lo que creemos** y todo lo demás queda sin interpretación.

## 5. Qué NO es esto

No es un intento de arreglar el canje. **Es su mapa.** El candidato que podría romperlo —una hija que fuga al nacer y
**deja de aprender al madurar**— queda anotado en la nota de diseño y **no se diseña aquí**.

## 6. Qué se decide

- **H se sostiene:** se registra el canje como **propiedad medida de esta arquitectura**, con su superficie, y se
  publica así: *"en este sistema, separar y generalizar son el mismo parámetro visto por los dos lados"*. v11 sigue
  siendo el tronco; v12 **no** se congela (no aporta un punto mejor en los dos ejes).
- **H se refuta:** v12 con ese `beta` pasa a candidato a tronco, con confirmatorio propio en semillas nuevas, examen
  criterio v3 **y** `bateria_generaliza.py 20` (ERR-20).
- **La fuga no sigue a `beta`:** se para; el instrumento no manipula lo que dice manipular.
