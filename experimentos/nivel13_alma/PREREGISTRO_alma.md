# PREREGISTRO — BLOQUE ALMA (nivel 13): un alma externa que parcha al cuerpo, y un nodo central

**Escrito ANTES de medir nada.** Lo único corrido hasta aquí es `identidad_alma.py` (64/64), que es instrumento,
no medida: no se ha leído ni una vida, ni un R₀, ni una curita del humo. Fecha: 18 sep 2026.

MISIÓN: llegar a la AGI por este camino — un organismo mínimo con reglas locales que aprende, sobrevive, se
comunica y se reproduce, con evidencia preregistrada. Hoy: buscar mecanismos con un "alma" externa (evolución
guiada, como v11/JUACO-EVO) **sin confundir el buscador con el resultado**.

---

## 0. La idea del director (textual) y su traducción medible

> "una célula en un mundo, Haiku de alma del experimento; comienza a interactuar; si muere, Haiku la revive y le
> pone una curita, un puente para que no muera por lo mismo; después se reproduce, tiene hijos, y un nodo central
> de conocimiento como en Avatar: las células que quieren vivir se conectan y reciben los datos, las que no, que
> se mueran solas; cada vez que muera, parcharla, hasta lograr que evolucione."

| la idea | la traducción medible | ya medido antes |
|---|---|---|
| una célula en un mundo | `organismo_vivo_h1.py` con `muerte_real=1`: la muerte BORRA la memoria del individuo | H-1 (18 sep 19:24 y réplica) |
| si muere, la revive | el cuerpo siguiente nace de la cola con la dote que pagó su padre | H-1 |
| le pone una curita | UNA entrada del **menú cerrado** de `MENU_curitas.md` (a–f), elegida por un agente externo | — |
| nodo central de conocimiento | tabla compartida de mensajes `(patrón, R cruda, necesidad)` que se llena con las últimas 20 mordidas **con consecuencia** del que muere | BLOQUE 4/4b: el mensaje cambia la conducta del receptor sin experiencia propia |
| las que se conectan reciben los datos | el cuerpo **conectado** nace leyendo el nodo como **exposiciones sin consecuencia**; el no conectado nace vacío | BLOQUE 4/4b; `NOTA_entrelazamiento_20260918.md` §3 |
| hasta lograr que evolucione | **no se mide aquí**: la palabra "evoluciona" queda prohibida (regla 6). Lo que se mide es *vida por cuerpo* y *R₀ del linaje* | — |

## 1. Hipótesis

**H-A (la del bloque).** Un alma externa que, tras cada muerte, elige una curita de un menú cerrado sube la vida
de los cuerpos sucesivos y el R₀ del linaje por encima del linaje sin alma (H-1: R₀ 0.148, vida mediana ~100), y
lo hace **por el nodo**: la mayor parte del efecto viene de (a) conectar y (b) escribir el miedo, no de (c)/(d)
(perillas del mundo) ni de (e) heredar valores (H-1 ya la midió: paga 10–20 %).

**H-B (la que puede tumbarla).** El efecto es de *tocar perillas*, no de *elegir bien*: un alma que elige al azar
del mismo menú llega igual de lejos. O peor: el efecto entero está en (c)+(d), que abaratan el mundo, y el nodo
no aporta nada — es decir, H-1 sigue en pie y sólo se hizo el mundo más fácil.

## 2. Instrumento

- `organismo_alma.py` (generado por `construye_alma.py` desde `organismo_vivo_h1.py` **9e99ff87b5e2db1e**, que
  sólo se leyó). Con `alma=None` es h1 **bit a bit** en los cinco modos de H-1 (identidad **64/64**).
- Cuerpo: **CUELLO_MIN** (`vivo=1`, `n_nec=2`, `rep_cuello=2`, `costo=costo_a=0.001`, `estims=ABCD`), con
  `reproduccion=1, rep_mide=1, rep_X=500, rep_umbral=1.0, rep_coste=0, rep2=1, rep2_regalo=600, h1=1`,
  `muerte_real=1`, `hereda='nada'`, `dote=0.6`. **Es exactamente el brazo NADA_CM de H-1** (R₀ 0.148 / 0.140).
- El nodo y la exposición sin consecuencia: ver la cabecera de `organismo_alma.py`. **Declaración obligatoria:**
  NO es el canal de b4b bit a bit (b4b escribe en la tabla de pares de v15f, órgano que esta cadena no tiene);
  es su **contrato** ejecutado con el bloque de la vía lenta extraído literalmente de la mordida de h1.
  **Comparar números con b4b es ilegítimo** y no se hará.
- El alma: `corre_alma.py --alma interfaz` (el agente contesta por archivos `alma_pregunta_*.json` /
  `alma_respuesta_*.json`), `alma_aleatoria.py` (control), `alma_ninguna.py` (control).

## 3. Brazos de la serie (10 linajes × 20 muertes; un proceso, sin Pool)

| brazo | alma | nodo | qué prueba |
|---|---|---|---|
| **ALMA** | agente externo, menú a–f | 1 | la hipótesis |
| **AZAR** | curita uniforme del menú, rng propio `850000+10⁶·sem` | 1 | que elegir importa (no sólo tocar) |
| **NADA** | siempre (f) | 0 | la línea base = H-1 NADA_CM |
| **ALMA-SIN-NODO** | agente externo, pero el runner fuerza `nodo=0` (las curitas (a) y (b) quedan inertes) | 0 | que el efecto es **del nodo** y no de (c)/(d)/(e) |
| **NODO-CIEGO** | siempre (a) desde la muerte 1 | 1 | el nodo **solo**, sin alma que elija |
| **BARAJA-NODO** (control de contenido) | siempre (a), pero los 6 píxeles de cada mensaje del nodo se permutan con rng propio `860000+10⁶·sem` | 1 | que lo que paga es el **contenido** del mensaje, no su magnitud (el control que decidió H1-4) |

> BARAJA-NODO exige una perilla más (`nodo_baraja`) que **todavía no está construida**: se construye por anclas
> ANTES de la serie, con su entrada de identidad, o el brazo no se corre y se dice. No se corre la serie sin él:
> sin control de contenido, "el nodo ayuda" no se puede declarar (es la trampa que H1-4 cerró).

## 4. Medidas (fijadas antes)

1. **Principal — la curva de vidas:** `vidas_cuerpo[i]` = pasos que vivió el cuerpo *i* (i = 1..20).
   Resumen: **mediana de los cuerpos 11–20** y **mediana de los cuerpos 1–5**, y su razón (`subida`).
2. **R₀ del linaje** = `descendientes / muertes` acumulado al cierre de la muerte 20 (la medida de H-1).
3. Secundarias (se reportan, no deciden): fundaciones del linaje (`fundadores`), tamaño del nodo, curita elegida
   por muerte, `dote_final` / `umbral_final` / `hereda_final`, `desc_cuerpo`.
4. **Puerta de montaje (si cae, no se lee nada más):** en NADA, mediana de R₀ sobre las 10 semillas en
   **[0.05, 0.35]** y vida mediana en **[60, 220]** — el rango en el que H-1 dejó este brazo. Fuera de ahí el
   instrumento se movió.
   Aviso escrito antes: **los cuerpos 1–5 no son típicos**. El fundador nace del mundo con `E = Ag = 1.0`
   (`A_ini`), no con la dote de 0.6; su vida está inflada. Por eso la razón 11–20 / 1–5 es una medida
   **conservadora** (el denominador juega a favor de la refutación), y por eso **no** se usa 1–5 como "antes".

## 5. Predicción numérica (la letra; se juzga sobre 10 semillas, 801–810)

- **P-1 (la que decide).** ALMA: mediana sobre semillas de `mediana(vidas 11–20) / mediana(vidas 1–5)` **≥ 2.0**;
  y ALMA ≥ **1.5 ×** el mismo cociente en AZAR.
- **P-2 (el nodo es el mecanismo).** `mediana(vidas 11–20)` de ALMA ≥ **1.5 ×** la de ALMA-SIN-NODO; y
  ALMA-SIN-NODO ≤ **1.25 ×** NADA (sin nodo no sube).
- **P-3 (el contenido, no la magnitud).** NODO-CIEGO ≥ **1.5 ×** BARAJA-NODO en `mediana(vidas 11–20)`, y
  BARAJA-NODO ≤ **1.25 ×** NADA. *(Si BARAJA-NODO ≈ NODO-CIEGO, lo que paga es la cautela genérica, no el
  contenido: ERR numerado y se dice, exactamente como H1-4 previó para el vector.)*
- **P-4 (R₀).** ALMA: mediana de R₀ **≥ 0.45** (≥ 3 × el 0.148 de H-1) con mediana de `fundadores` ≤ 3.
  *No se predice R₀ ≥ 1*: sostener el linaje es otro peldaño y H-1 midió lo lejos que está.
- **P-5 (A₁₂, sin parear, ERR-61).** A₁₂(ALMA > NADA) sobre `mediana(vidas 11–20)` **≥ 0.85**;
  A₁₂(ALMA > AZAR) **≥ 0.75**.

**Todas las puertas se juzgan sobre las 10 semillas de la serie, nunca sobre el humo.**

## 6. Qué lo refuta (escrito antes)

- **R-1.** A₁₂(ALMA > AZAR) ≤ 0.60 → *elegir* no aporta: el alma es un generador de perturbaciones y el bloque se
  declara refutado como "alma". Lo que quede es una rampa de perillas, es decir, H-1 otra vez (ERR-62).
- **R-2.** ALMA-SIN-NODO ≥ 0.85 × ALMA → el efecto **no** es del nodo sino de (c)/(d)/(e): el mundo se abarató.
  Entonces se declara eso y sólo eso, y el nodo queda sin evidencia.
- **R-3.** BARAJA-NODO ≥ 0.85 × NODO-CIEGO → el nodo transmite **magnitud**, no contenido (una cautela genérica).
  ERR numerado; el vocabulario permitido pasa a ser "el nodo vuelve al recién nacido más cauto", nunca
  "el nodo transmite lo que el muerto aprendió".
- **R-4.** `mediana(vidas 11–20)` de ALMA ≤ 1.25 × la de NADA → el alma no mueve la vida y el bloque cae entero.
- **R-5 (trampa del mosaico).** Si el efecto entero se explica porque el alma bajó `rep_umbral` (curita (d)) —
  es decir, ALMA con (d) bloqueada ≈ NADA — entonces lo medido es "la ventana de reproducción se hizo más
  barata", no "la célula sobrevive". Se comprueba con un brazo post-hoc **declarado como post-hoc** y no decide.

## 7. Semillas

- **Serie:** 801–810 (10 linajes × 20 muertes cada uno; 6 brazos × 10 = 60 corridas, un proceso).
- **Réplica:** 811–820, misma letra, sin tocar nada. Regla 12: un veredicto que dependa de una semilla en el
  umbral dispara réplica en un rango nuevo con la misma letra.
- **Humo (este entregable):** semilla **801**, **10 muertes**, el diseñador jugando de alma, más los dos
  controles automáticos en la misma semilla. **El humo NO es evidencia** y no entra en ninguna puerta: sólo dice
  si el instrumento se mueve y con qué números escribir la serie.
- Los rng derivados no colisionan (ERR-60): mundo `sem`, hijos `700000+10⁶·sem+k`, baraja de herencia
  `800000+10⁶·sem`, alma al azar `850000+10⁶·sem`, baraja del nodo `860000+10⁶·sem`.

## 8. Cláusula del buscador (manda sobre todo lo anterior)

**Lo que el alma encuentre NO es un resultado: es una hipótesis.** Si la serie pasa, lo que se declara es
*"existe una secuencia de curitas del menú cerrado que sube la vida de los cuerpos sucesivos"*, y el peldaño
siguiente es **obligatorio**: fijar esa configuración (conexión al nodo desde el cuerpo 1, o el nodo con miedo
escrito, o lo que haya salido) como **perillas constantes desde el paso 0**, correrla **sin alma**, con
preregistro nuevo, controles nuevos y semillas nuevas. Sólo eso cuenta como resultado del proyecto.
Es exactamente lo que se hizo con v11/JUACO-EVO: la evolución guiada **encontró** la división por conflicto de
signo; lo que entró al tronco fue la regla fija, medida sin el buscador.

## 9. ERR reservados (regla 11; libres desde ERR-80)

- **ERR-80** — si el menú de `MENU_curitas.md` se amplía o se cambia un paso (`d_dote`, `d_umbral`, `miedo_n`,
  `miedo_R`, `nodo_k`, `nodo_lee`) después de ver cualquier dato.
- **ERR-81** — si `BARAJA-NODO` no llega a construirse y la serie se corre sin control de contenido.
- **ERR-82** — si alguna puerta de §5 se recalibra después de ver la serie.
- **ERR-83** — reservado para la cláusula de cierre: si NINGÚN brazo con alma pasa P-1 ni P-4, se declara que
  **un alma externa con este menú no rescata al linaje mortal de H-1**, y el camino vuelve a "que un cuerpo nuevo
  aprenda en menos de una vida" (v15f, el mensaje del bloque 4), no a más curitas.
