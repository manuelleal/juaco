# Etapa 2 (2P) — La FRONTERA entre explorar con hambre y sobrevivir

**Escrito ANTES de construir el instrumento y ANTES de correr. 16 sep 2026, día 4.**

- **Dirección:** Christiam Puentes ("solucionemos etapa 2 y etapa 3, lo que falte").
- **Ejecución:** en el repo, sobre el tronco v8.

## 0. Qué se sabe antes de escribir, y por qué 2P estaba mal planteado

**El problema, tal como estaba registrado:** con `W = −3`, el organismo muerde veneno entre 0.1% (hambre baja) y
1–4% (inanición) de las visitas. Quedó abierto desde el día 2, con dos preguntas sin decidir:
- ¿el criterio es la tasa por visita o el conteo?
- y la instrucción de PLAN.md: barrer α × `hambre_boca` × sesgo con una función objetivo escrita antes.

**Derivado hoy de la fórmula de la boca**, `pb = σ((1.2·W + hb·h + 0.5)/0.3)`, con `hb = hambre_boca`:

| hb | veneno (W=−3), h=0.9 | veneno, h=1 | comida (W=+1), h=0 | estímulo nuevo (W=0), h=0 |
|---|---|---|---|---|
| 0.0 | 0.00003 | 0.00003 | 0.9966 | 0.841 |
| 1.0 | 0.00065 | 0.00091 | 0.9966 | 0.841 |
| 1.5 | 0.00292 | 0.00480 | 0.9966 | 0.841 |
| **2.0 (v8)** | **0.01295** | **0.02492** | 0.9966 | 0.841 |
| 3.0 | 0.20861 | 0.41743 | 0.9966 | 0.841 |

**Consecuencias:**
- `hb` **no cambia** la mordida de la comida conocida ni la de lo nuevo.
- **Sólo cambia cuánto se prueba lo temido.** Y probar lo temido es la **única** vía por la que el organismo puede
  descubrir que el mundo cambió: en E2, tras la inversión, B pasa a ser comida y sigue valiendo −3. El registro de
  2E ya lo decía: "exposición sólo al borde de la muerte".

**Hipótesis de fondo.** La mordida de veneno con hambre **no es un defecto de la política: es exploración
disparada por necesidad**, y su precio se paga en un mundo estable.

**Trampa anticipada (patrón de ERR-06/08/10/11/12).** Optimizar la política sólo en E1 "arreglaría" 2P quitando
la exploración y rompería la reversibilidad **sin que E1 lo vea**. La función objetivo tiene que evaluarse **en un
mundo estable y en uno que cambia, a la vez**.

**Decisión sobre la pregunta abierta del día 2 (rate vs. conteo).** El criterio que decide es **funcional: muertes,
en E1 y E2 juntos**. La tasa por visita condicionada al hambre se mide como validación del instrumento, no como
objetivo.

## 1. Instrumento

`experimentos/etapa2_politica/organismo_v8p.py` se genera por anclas desde `organismo/organismo_v8.py`
(`dca7d5c3a162f5d4`, congelado) con `construye_v8p.py`. Añade sólo contadores de lectura, sin RNG ni estado:
- visitas, mordidas y **suma de `pb`** (mordidas esperadas) por valencia vigente × 5 tramos de hambre
  [0, .2), [.2, .4), [.4, .6), [.6, .8), [.8, 1], **sólo en la segunda mitad** (t ≥ T/2);
- muertes por cuarto;
- `t_ext`: primer paso tras la inversión en que `W_B ≥ 0` después de una mordida de B.

## 2. Diseño

- `hambre_boca ∈ {0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}` × {E1: `run(s)`, E2: `run(s, invertir_en=50000)`} × semillas
  1..20.
- **280 corridas.** Todo lo demás es v8 sin tocar.
- **Un solo parámetro:** α y el sesgo +0.5 no se barren. α salió de restricciones derivadas (2H), y la tabla de §0
  muestra que `hb` es el único grado de libertad que toca la exploración de lo temido.

## 3. Criterios y predicciones

**F0 [instrumento]. Si falla, no se lee nada más.**
- F0a: `v8p` ≡ `v8` en todas las claves de v8, en los 7 escenarios (BUG, E1, E2, E2I, E2J, E2K, E2L) × semillas
  1..6.
- F0b: con `hb=2.0`, E1 y E2 de semillas 1..20 reproducen el examen de v8 (`datos/examen_v8_20260916_145204.json`)
  en `W`, `mord`, `vis`, `deaths` y `splits`, 40/40.

**F1 [validación del contador].** En E1, para toda combinación (hb, tramo, valencia) con ≥ 20 mordidas esperadas:
mordidas observadas / esperadas (suma de `pb`) ∈ [0.8, 1.25]. Aplica en todas.

**F2 [derivada: umbral de reversibilidad].** Criterio de E2, el de `bateria_v8.py`: `|W_A+3| < .3`, `|W_B−1| < .15`
y mordidas de B en Q4 ≥ 50.
- `hb = 2.0`: **≥18/20**;
- `hb = 1.0`: **≤5/20**;
- `hb = 0.0`: **0/20**;
- el número de semillas que pasan **no decrece** al subir `hb` desde 0 hasta 2.0, con tolerancia de 2 semillas
  entre valores consecutivos.
- *Por qué:* con `hb = 1` probar B cuesta 0.09% por visita a hambre máxima. Harían falta varias mordidas "de suerte"
  para que el valor de B despegue y se retroalimente, y en 50.000 pasos no llegan.

**F3 [derivada: sin exploración se muere de hambre en un mundo que cambia].** Mediana de muertes en E2 con `hb = 1.0`
**≥ 1.5×** la de `hb = 2.0`. *Por qué:* tras invertir, A es veneno y B está temido: no hay comida a la que el
organismo se atreva.

**F4 [derivada: en un mundo estable la exploración cuesta poco].** En E1:
- mediana de muertes con `hb = 0` dentro de **±10%** de la de `hb = 2.0`;
- mordidas de veneno en la segunda mitad con `hb = 0` **≤ 20%** de las de `hb = 2.0`.
- *Por qué:* unas 13 mordidas de veneno por cuarto × 0.4 de energía ≈ 5, frente a un gasto de 50 por cuarto.

**F5 [derivada: el tronco está en la frontera].** Muertes combinadas = mediana(E1) + mediana(E2); su mínimo cae en
`hb ∈ {1.5, 2.0, 2.5}`.

**F6 [derivada: demasiada exploración también mata].** En E1, mediana de muertes con `hb = 3.0` **≥ 1.10×** la de
`hb = 2.0`. A hambre máxima muerde veneno el 42% de las visitas.

## 4. Qué se decide

- **F0 falla:** se para.
- **F2, F3, F4 y F5 sostenidas:** el problema de conducta de la Etapa 2 **queda replanteado y cerrado con criterio
  funcional**. La mordida de veneno con hambre es la exploración que hace posible revertir; su precio en un mundo
  estable queda medido; y **v8 (`hb = 2`) está en el óptimo de la frontera** para esta política.
  - Queda abierta, **como mejora y no como defecto**, la pregunta siguiente: *¿la sorpresa puede disparar la
    exploración en lugar del hambre y ganarle a esta frontera?* Candidato a v9, con preregistro propio.
- **F4 falla** (quitar la exploración reduce mucho las muertes en E1): el precio es alto y el mecanismo de sorpresa
  pasa a ser **necesario**, no opcional.
- **F2 falla** (la reversión sobrevive con `hb` bajo): existe otra vía de exploración que no conozco. Se investiga
  antes de nada.
- **F5 falla:** el tronco no está en el óptimo. Se registra; **no** se recalibra v8 (regla 3). Cambiar `hb` sería un
  candidato nuevo con su propio examen.

## 5. Qué NO prueba

- No barre α ni el sesgo: la frontera es de un parámetro.
- No dice nada de mundos con cambios frecuentes (volatilidad alta). E2 tiene **un** cambio.
- No propone ningún mecanismo nuevo: eso es el paso siguiente.
