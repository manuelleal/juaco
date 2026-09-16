# 3T CONFIRMATORIO sobre el tronco v8 — ¿la regla 2L descubre sola la dimensión del orden?

**Escrito ANTES de construir el instrumento y ANTES de correr nada. 16 sep 2026, día 4, fase 4.**

- **Dirección:** Christiam Puentes. Ordenó "comenzar la fase 4" tras congelar v8.
- **Ejecución:** en el repo.
- **Rama original:** `experimentos/ramas/3T_temporal/` (preregistro `7a96acbf3122dce1`). No se modifica nada de ahí.

---

## 0. Qué se sabe antes de escribir (se declara TODO; esto no es un experimento ciego)

1. **Confirmatorio del día 3, con v7 (techo 3.0 sin drenaje): NO.** C3 dio `sep = 0.00` (0/20) y
   `lift_q4 = −0.005`; el pool se agotó en 20/20.
2. **Post-hoc del día 3, sin valor confirmatorio.** PH3, con el pool de v7 (90) y el techo de `Wp`/`Wn` levantado a 30:

   | brazo | sep | lift_q4 | divisiones |
   |---|---|---|---|
   | **C3** | **3.97 (20/20)** | **0.34 (20/20)** | 16 [10, 33], la última en t≈7.418 |
   | **C3C** | 0.53 (0/20) | −0.04 (0/20) | 60 (pool agotado) |
   | C2 | 3.99 | — | — |

   Barrido del techo: 3.0 → 0/20; 4.5 → 12/20; 6.0 → 19/20; 9, 15 y 30 → 20/20.
   **Conozco esas cifras.** Las predicciones que dependen de ellas llevan la marca **[PH]** y **no son independientes**.
3. **ERR-3T-02.** El criterio 4 original (no-artefacto) estaba anclado en `solap_A`, y era insatisfacible: C3C
   separa los códigos igual o más que C3. El discriminador real es **valor y conducta**. Aquí se corrige **antes
   de correr**.
4. **Demostración de ERR-11 y S0/C0, medidas hoy.** El drenaje de la parte común deja `W` idéntico al de un
   organismo **sin techo** mientras nada trunque. Y en la prueba de coste, antes de la primera truncación, los
   dos brazos fueron idénticos 20/20.
5. **Examen de v8 (hoy).** v8 es v7e con `lam=0.05`; con `lam=0` es v7.

## 1. La pregunta, y por qué este confirmatorio no es una repetición

**Pregunta de 3T:** con el tronco corregido, ¿la regla de división 2L produce **sola** composición temporal
(nivel 7)? Es decir: separar A|A (veneno) de A|B (comida) partiendo de un código ciego al orden.

**Lo que añade** es una predicción **exacta y falsable** que el día 3 no podía hacerse.
- PH3 levantó el techo a 30; v8 lo deja en 3.0 y drena la parte común.
- Por §0.4, si ninguno de los dos trunca, **son el mismo organismo en valor y conducta**.
- Por tanto, **v8 debe reproducir PH3 semilla a semilla**.
- Si lo hace, el resultado post-hoc del día 3 no fue una casualidad de un techo arbitrario: es lo que hace el
  tronco congelado.

## 2. Instrumento

`experimentos/3T_confirmatorio/mundo_temporal_v8.py` se genera por anclas desde
`experimentos/ramas/3T_temporal/mundo_temporal.py` (`1f447657faf00ef8`) con `construye_mundo_v8.py`.

**Añade:**
- el parámetro `lam=0.05` con la línea de drenaje **aritméticamente idéntica** a la de `organismo_v8.py`, en el
  mismo sitio (tras `dlt`, antes del clip);
- la **mordida del techo** (truncación contra `wclip`): `t_techo`, `n_techo`;
- las claves nuevas en la salida.

Nada más: mundo, cuerpo, política, 2L (θ=0.6, ema=0.02, paso=0.5, NKMAX=90) y `wclip=3.0` quedan idénticos.

## 3. Brazos

**v8** (`mundo_temporal_v8`, `lam=0.05`, `wclip=3.0`, `nkmax=90`) — los seis del diseño original, 20 semillas,
T=100.000:

| brazo | entrada | plasticidad | papel |
|---|---|---|---|
| C1 | 6 | no | control, ciego al orden por construcción |
| C1p | 6 | sí | dividir sin canal temporal |
| C2 | 12 visibles (rechazo) | no | techo de factibilidad |
| C2b | 12 ciegas | no | control de instrumento: ≡ C1 campo a campo |
| **C3** | 12 ciegas | **sí** | **la pregunta** |
| **C3C** | 12, canal temporal **aleatorio** | sí | control de artefacto |

**Referencia PH3:** C3 y C3C, 20 semillas. Sirve para la predicción exacta.
- Se corre con **`mundo_temporal_v8` con `lam=0`**, `wclip=30.0` y `nkmax=90`, y no con `mundo_temporal`
  directamente, **para poder medir la truncación contra 30**: el original no la instrumenta.
- Es el mismo mundo: con `lam=0` es `mundo_temporal` campo a campo (K1), y **K3** comprueba que reproduce el JSON
  guardado de PH3, generado con el original.

## 4. Criterios — veredicto confirmatorio SÍ si y sólo si se cumplen K, 1, 2, 3 y 4

**K. Controles de instrumento.** Si falla uno, no se lee nada más.
- **K1:** `mundo_temporal_v8(lam=0)` ≡ `mundo_temporal` (ambos con `wclip=3.0`), campo a campo, en los 6 brazos ×
  semillas 1..3.
- **K2:** C2b ≡ C1 bajo v8 en `W`, `sep`, mordidas por cuarto, muertes y `Rtot`, **20/20** (criterio de instrumento
  del preregistro original).
- **K3:** la referencia PH3 recorrida hoy reproduce `sep`, `splits` y `lift` del JSON guardado
  `PH3_20260915_115229.json`, **20/20** en C3 y C3C.
- **K4 (añadido al releer antes de correr: control positivo de que el drenaje actúa).** E pasaría sola si la línea
  de drenaje no se ejecutara nunca. Por eso los canales `comp` de C3 bajo v8 deben **diferir** de los de la
  referencia PH3 en **20/20** semillas. En C3 hay conflicto en todas, así que el drenaje tiene que dejar los
  canales más bajos. Si no difieren, el drenaje no actúa y E no se lee.

**Criterios de C3 bajo v8.** Son los del preregistro original, con el 4 corregido por ERR-3T-02:
1. **Representación:** mediana de `solap_A` final **≤ 1** y **≥15/20** semillas con `solap_A ≤ 1`.
2. **Valor:** mediana de `sep = W(A|B) − W(A|A)` **≥ 1.0**.
3. **Conducta:** mediana de `lift_q4` **≥ 0.15**.
4. **No es artefacto** (corregido): C3C bajo v8 tiene mediana de `sep` **< 1.0** **y** mediana de `lift_q4` **< 0.15**.

**Veredicto NO** si falla 1, 2 o 3, o si C3C cumple 4 a la inversa (valor **o** conducta al nivel de C3).

## 5. Predicciones

- **E [exacta, derivada de §0.4; la más fuerte].** Para C3 y para C3C: en toda semilla en que **ni** el brazo v8
  **ni** la referencia PH3 truncan, las dos corridas coinciden en:
  - `W` de las 4 situaciones (3 decimales), `sep`, `lift` por cuarto, `solap_A` por instantánea;
  - `splits`, `split_t` y `celdas`;
  - `n_AB`/`n_AA`/`n_B` por cuarto, muertes y `Rtot`.
  - **Se refuta con una sola diferencia.** Si se refuta, hay una vía de divergencia sin truncación y se para la
    lectura.
- **E-alcance.** v8 no trunca en ningún brazo con plasticidad ni en C2: **0/20** en C1p, C2, C3 y C3C. El
  equilibrio de la parte común es del orden de `eta·|dlt|/lam`, alrededor de 1.2 por celda, lejos de 3.
  - La referencia C3 con techo 30 no trunca en **≥18/20**: la separación termina pronto y el conflicto cesa.
  - En C3C con techo 30 **no predigo**: el conflicto no cesa y los canales pueden crecer hasta 30. Las semillas
    que trunquen se excluyen de E y se reportan.
- **C3 bajo v8 [PH]:**
  - criterios 1–3 cumplidos;
  - por semilla, `sep ≥ 2.8` en **≥18/20** y `lift_q4 ≥ 0.15` en **≥18/20**;
  - divisiones: mediana **≤ 30**, y la última división antes de t=25.000 en **≥15/20**. Es la firma "se detiene
    sola".
- **C3C bajo v8 [PH]:** criterio 4 cumplido. Además, agota el pool (`celdas = 90`) en **≥15/20**: "no se detiene
  nunca".
- **Sin voto, descriptivas:**
  - C1: `sep = 0` por identidad; `lift_q4 < 0.05`. Derivado: `W_A` **ya no** vale 0.000 exacto, porque el drenaje
    quita la saturación simétrica.
  - C2: `sep ≥ 2.8` en ≥18/20.
  - C1p: divide y no mejora `lift`.

## 6. Qué se decide

- **SÍ:** la composición temporal de una mordida pasa de post-hoc a **resultado confirmatorio sobre el tronco v8**.
  - Vocabulario permitido (regla 8): *"con el tronco v8, la regla local 2L separa sola el canal temporal y la
    conducta lo usa"*.
  - **Nada** de planificación, orden abstracto ni inteligencia general.
- **NO:** se registra, y 3T vuelve a hipótesis. No se recalibra nada (regla 3).
- **Si E se refuta:** se para. Pasa por delante del veredicto.

## 7. Qué NO prueba

- Secuencias de más de una mordida: la memoria es de **una** mordida, dada como copia eferente.
- Que el organismo represente el "orden" en abstracto: representa un par (actual, anterior).
- Que la dirección de división sea inteligente. El día 3 mostró que no lo es: la selección está en el error que
  la dispara y la apaga.
- Un `lift` alto no implica planificación.

## 8. Procedencia

- El sha de este archivo va en el registro antes de construir el instrumento.
- Datos en `datos/3T_confirmatorio_<fecha>.*`, con el sha de `mundo_temporal.py`, `mundo_temporal_v8.py`, el
  constructor, el script, este preregistro y `organismo_v8.py`.
- Regla 10: log desde el arranque. Regla 11: se listan los procesos Python vivos.
