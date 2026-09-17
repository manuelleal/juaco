# Etapa 5, N2 — el SIGNIFICADO emerge: juego de señalización entre experto y novato (nadie fija el código)

**Escrito ANTES de modificar el instrumento y ANTES de correr. 17 sep 2026, noche del día 5.** Dirección: *"Dale a la N2"*.
Base: tronco **v13**. Diseño de referencia: `DISENO_comunicacion_simbiotica.md`, peldaño N2, y el punto 14 del brief
(criterio de emergencia): el código **no existe en el individuo, aparece al conectar dos, no está programado, es
reproducible y desaparece al barajar los símbolos**.

## 0. Qué cambia respecto de N1

En N1 el significado venía dado: "+" = muerde, "−" = rechaza, y el receptor lo interpretaba con una escala innata.
En N2 **no hay significado dado**: el emisor dispone de `K = 2` símbolos sin sentido y **aprende** cuál emitir según su
propio estado; el receptor **aprende** qué predice cada símbolo. Lo único compartido es el mundo.

**Por qué el mundo de regla y no A/B.** Con dos patrones, el novato aprende B con ~19 mordidas y después su conducta ya
no depende de ningún símbolo: no queda gradiente para que una convención se forme. Con **20 patrones de valencia
arbitraria** (`regla = 'azar'`: 10 comidas, 10 venenos, sin estructura lineal que la vía lenta pueda atajar), el novato
se enfrenta durante mucho tiempo a cosas que no conoce y el experto sí. Ahí un código paga, y ahí puede emerger.

## 1. Mecanismo (todo local; se declara cada constante)

- **Emisor.** Al pisar un objeto, su **estado** es su propia decisión: `st = 1` si muerde, `0` si rechaza. Emite un
  símbolo `s ∈ {0, 1}` muestreado de `softmax(beta_q · Pq[st])`, con `Pq` una tabla 2×2 de preferencias que **nace al
  azar** en (−0.1, 0.1) (RNG propio, `seed + 500000·i + 7`: no toca el flujo de azar del organismo) y `beta_q = 2`.
- **Refuerzo del emisor ("ganancia compartida", operacionalizada como lo único que puede ver: la conducta del otro).**
  Cuando, dentro de `tau_s = 200` pasos, el receptor visita un objeto **del mismo patrón** y su conducta coincide con el
  estado del emisor (muerde/muerde o rechaza/rechaza), `Pq[st][s] += eta_q · (+1)`; si no coincide, `−1`
  (`eta_q = 0.1`, recorte en ±3). Un refuerzo por emisión; el emisor **nunca ve** lo que el receptor come.
- **Receptor.** Mantiene `M[s]`, el valor que predice cada símbolo (nace en 0). Al oír `s` sobre un objeto de patrón
  `kk` a distancia ≤ `d_senal = 5`: (a) deja una **traza** `(s, kk) → t`; (b) **si ya cree saber qué significa `s`**
  (`|M[s]| ≥ u_m = 0.5`), actualiza su propio valor de `kk` como en N1, con `R̂ = M[s]`, a tasa `f_vicaria = 1/3`, por
  **las dos vías**, sin dividir y sin comer. Cuando después **muerde él mismo** un objeto `kk` con consecuencia `R`, para
  cada símbolo `s` oído sobre `kk` hace ≤ `tau_m = 200` pasos: `M[s] += eta_m · (R − M[s])` (`eta_m = 0.1`). Es la
  única fuente de significado: **sus propias consecuencias**.
- **Ninguna de estas tablas se hereda.** El experto hereda su estado de organismo (valores, códigos, patas, vía lenta),
  no `Pq` ni `M`: el código no existe en el individuo.
- **Con `senal = None` nada de esto se ejecuta y con `n = 1` en el mundo de regla el organismo es `organismo_v13g`
  exacto** (identidad K1).

## 2. Diseño (semillas 1–20; T = 200.000; mundo de regla `azar`, 20 patrones presentes desde el inicio)

Experto = progenitor v13 que vivió 200.000 pasos en ese mismo mundo (`n = 1`, mismo patrón de valencias) y hereda su
estado; novato = nace en blanco. `nobj_por_org = 4`.

| condición | organismos | señal |
|---|---|---|
| SOLO | novato | — |
| N0 | novato + experto | ninguna |
| INNATO (= N1, referencia) | novato + experto | conducta (+ muerde / − rechaza, significado dado) |
| **CONV** | novato + experto | **símbolos aprendidos** |
| SHUF (control del punto 14) | novato + experto | símbolos aprendidos, **barajados en la entrega** (el receptor oye un símbolo al azar) |

**Medidas.** Del novato: mordidas propias de **veneno** en toda la corrida y en Q1; muertes; venenos "conocidos" al final
(`W ≤ −2.5`, de 10). Del experto: `Pq` final, **consistencia** en el último cuarto (fracción de emisiones que usan el
símbolo preferido de su estado), y si los dos estados prefieren **símbolos distintos**. Del novato: `M` final.

## 3. Criterios (escritos antes) y predicciones

- **K1 [instrumento]:** `mundo_social(n=1, mundo='regla', regla='azar')` ≡ `organismo_v13g(mundo='regla', regla='azar',
  fase2_en=0)` en `W`, `mord`, `vis`, `deaths`, `splits`, `split_t`, `celdas`, semillas 1–3. Si falla, se para.
- **K2 [canal]:** en CONV el novato recibe ≥ **1.000** símbolos (mediana).
- **E1 [convención en el emisor]:** en CONV, el experto termina con estados que prefieren **símbolos distintos** y
  consistencia en Q4 ≥ **0.9**, en ≥ **15/20**. *Predicción: 16–19/20.*
- **E2 [decodificación en el receptor]:** en CONV, con `s_rech` y `s_mord` los símbolos preferidos del experto,
  `M[s_rech] ≤ −1.0` **y** `M[s_mord] ≥ +0.3` en ≥ **15/20**. *Predicción: 15–18/20.*
- **E3 [arbitrariedad = no está programado]:** el símbolo que acaba significando "rechazo" es el `0` en **entre 5 y 15**
  de las 20 semillas. *Predicción: ~10/20.*
- **E4 [beneficio]:** mordidas de veneno del novato en CONV ≤ **0.7 ×** N0 (mediana) y CONV < N0 pareado en ≥ **14/20**.
  *Predicción: ≈ 0.5 × N0; INNATO (significado dado) algo mejor que CONV, porque no tiene que aprender el código.*
- **E5 [desaparece al barajar]:** en SHUF, `|M[s]| < 1.0` para los dos símbolos en ≥ **15/20**, y veneno ≥ **0.9 ×** N0.
- **E6 [no existe en el individuo]:** SOLO no tiene símbolos; se reporta y no vota.
- **Reproducible:** si E1–E5 pasan en 1–20, se repite en **21–40** y sólo con eso se escribe "N2 cerrado".

**Refutación:** E1 o E2 fallan (el bucle no cierra: sin gradiente no hay convención), o E4 falla (hay código pero no
sirve), o E5 falla (el "código" no dependía del símbolo). **Riesgo declarado y probable:** el cierre del bucle exige que
la conducta del receptor dependa del símbolo **antes** de que conozca los patrones por su cuenta; si el novato aprende
los 20 por sí mismo antes de que `M` se separe, no emerge nada. Si ocurre, se diagnostica (tiempos de `M`, de `Pq`) y
**no se recalibra**: se registra "no emerge con refuerzo por acuerdo en este mundo" y se propone otro mundo.

## 4. Qué se decide

- **E1–E5 y réplica:** *"entre dos organismos v13 emerge un código de dos símbolos que ninguno tenía, con significado
  arbitrario por semilla, que transmite valor y que muere al barajarlo"*. N2 cerrado. Vocabulario permitido: emerge,
  transmite. **No** se dice "lenguaje".
- **Falla:** se registra qué eslabón no cerró y se vuelve al diseño con otro mundo o con refuerzo distinto, preregistrado.

---

## ENMIENDA 1 (17 sep, noche; tras el humo de instrumentos y ANTES de correr) — el significado es contraste

**Humo declarado (semilla 3, T = 60.000, un solo par CONV):** 11.794 emisiones, 3.165 recibidas, refuerzos del experto
10.621 (+) / 362 (−). El símbolo de **rechazo** emergió (`Pq[0] = [+3.0, −1.18]`, consistencia 0.97) pero el de
**mordida no** (`Pq[1] = [−3.0, −3.0]`: los dos símbolos castigados por igual). Causa, vista en los números: con
símbolos al azar al inicio, cada `M[s]` tiende al **promedio** de consecuencias (10 venenos a −3 y 10 comidas a +1 dan
≈ −1 para los dos símbolos: `M = [−2.69, −0.95]`), el novato **devaluaba todo lo señalado**, rechazaba la comida
señalada, y con eso castigaba al emisor por igual con cualquier símbolo en el estado "muerde": **sin gradiente, la mitad
del código no puede separarse**. Es un fallo de diseño del receptor, no de medida.

**Corrección, antes de correr:** lo que informa de un símbolo es **cuánto se aparta de la media de los símbolos**:
`R̂ = M[s] − media(M)`, con la misma puerta `|R̂| ≥ u_m = 0.5`. Con un código sin información los dos contrastes son ≈ 0 y
el receptor **no actúa** (que es lo correcto); con un código informativo (`M → [−3, +1]`) los contrastes son −2 y +2.
`M` se sigue aprendiendo igual (sólo por las consecuencias propias). **E2 y E5 se evalúan sobre el contraste**
(`C[s] = M[s] − media(M)`): E2 `C[s_rech] ≤ −1.0` y `C[s_mord] ≥ +0.3`; E5 `|C[s]| < 1.0` para los dos en SHUF.
Ninguna constante cambia; K1, K2, E1, E3, E4 y las predicciones se mantienen.

**Corrección de instrumento (K1):** la identidad se comprueba contra `organismo_v13g` **con los defectos del tronco**
(`eta_s = 0.015`, `puerta = 3`); el humo la había comparado contra la copia de exploración con las perillas apagadas.
