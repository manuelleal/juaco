# Nivel 6, peldaño siguiente: **dos metas y rodeo** — ¿elige entre dos comidas recordadas la que conviene, y da el rodeo largo cuando el camino corto pasa por veneno recordado?

**Escrito ANTES de correr las semillas 41–60. 17 sep 2026, día 6.** Continúa `experimentos/nivel6_mapa/PREREGISTRO_mapa.md`
(+ enmienda 1) y su resultado replicado (0.81/0.80; INVERTIDO 0.11/0.13; entrada "Nivel 6 (planificación mínima)" de
`registro/REGISTRO_etapas_1_2.md`), que dejó abierto exactamente esto: *"horizonte real (dos metas, rodeo por veneno)"*.
Reglas 4, 5 y 6 de `registro/EQUIPO.md`. **El organismo no cambia**: la hipótesis es que el `_sesgo_M` que ya existe
(suma por dirección del valor descontado de lo recordado) basta.

## 0. Hallazgo de diseño (va al registro, como la "premisa corregida" del mapa)

**Con los tres sitios a `L/3` el rodeo es geométricamente imposible.** Con `sitios=('A','B','A')`, `mundo_mapa` los
pone a `L//3 = 13` (F1 = F0, veneno = F0+13, F2 = F0+26 en un anillo de 40). Llamando `g1` al hueco F1→veneno, `g2` al
hueco veneno→F2 y `dp` a la distancia de S al veneno, un caso de rodeo (el veneno **entre S y la comida cercana**, y la
otra comida más lejos) exige `d2 > d1` con `d1 = g1 + dp` y `d2 = g2 − dp`, es decir **`g2 − g1 > 2·dp`**; y `dp > r_vis`
para que el veneno esté fuera de la vista, o sea `dp ≥ 4`. Con huecos iguales `g2 − g1 = 0`: **ninguna posición S del
anillo pone el veneno en el camino corto**. Comprobado por enumeración de las 40 posiciones: en la disposición L/3 la
comida más cercana siempre está limpia y el lado ganador es siempre el corto (no hay nada que rodear).

Por eso la prueba nueva monta los tres sitios **asimétricos**: `g1 = 5`, `g2 = 20` (y `g3 = L − g1 − g2 = 15`). Es un
cambio del **mundo de la prueba**, no del organismo: los tres sitios siguen siendo fijos, con `regen`, y el mapa `M` se
sigue escribiendo sólo pisándolos. Todo el montaje vive **dentro de `prueba`**, así que sin `modo='rodeo'` el
instrumento es `mundo_mapa` bit a bit.

## 1. Instrumento `mundo_mapa_rodeo.py`

Generado por `construye_rodeo.py` desde `experimentos/nivel6_mapa/mundo_mapa.py` (**sha `207d6a1954336b18`**, fijado en
el constructor) por **anclas con conteo exacto** (2 parches: montaje de sitios y prueba nueva). Añade **sólo**
`prueba=dict(modo='rodeo', ...)`; no toca `_sesgo_M`, ni `valor()`, ni la política, ni el aprendizaje.

**Identidad obligatoria** (la corre `corre_rodeo.py`, etapa 1, y se para si falla): `mundo_mapa_rodeo.run(seed, **kw)`
≡ `mundo_mapa.run(seed, **kw)` en **todas** las claves, semillas **1–3** × **los seis brazos de `corre_mapa.py`**
(MAPA, SINMAPA, CONGELADA, BARAJADO, SINCOMIDA, INVERTIDO) = 18 comparaciones; y con las perillas apagadas
≡ `organismo_v13.run(seed)` en 3 semillas × {base, `invertir_en`, `nuevo='C'`} = 9 comparaciones (v13 no trae las dos
claves que `mundo_mapa` ya añadía, `tel` y `M_llenas`; se comprueba aparte que valgan `None` y `0`). Instrumento
generado: `mundo_mapa_rodeo.py` **`7ab34aed9acffaa0`**, 236 líneas.

*Declaración (regla 4):* antes de escribir este preregistro se corrió el instrumento una vez a `T = 20 000` para ver que
no reventara y que la geometría saliera como dice §0. **Ningún criterio de §4 viene de esos números**: los cuatro son los
del encargo y el umbral de V0 sale de las potencias de `0.9`, no de los datos.

## 2. Mundo y montaje de la prueba (semillas 41–60; `r_vis = 3`, `sitios = ('A','B','A')`, `T = 100 000`)

Entrenamiento normal: dos comidas (`A`) y un veneno (`B`) en sitios fijos, `regen = 50`. `M[pos]` se escribe al pisar un
sitio ⇒ al acabar el entrenamiento `M` tiene **exactamente 3 entradas** (validez V1). Después, **sin aprendizaje y sin
boca**, 40 teletransportes por semilla, alternando caso (par = rodeo, impar = atajo) y recorriendo cuatro distancias:

| caso | S | d1 (comida cercana) | d2 (comida lejana) | dp (veneno) | lado correcto |
|---|---|---|---|---|---|
| **rodeo** (veneno entre S y F1) | veneno + dp | 9, 10, 11, 12 | 16, 15, 14, 13 | **4, 5, 6, 7 (en el camino corto)** | **el largo** (F2 limpia) |
| **atajo** (veneno fuera del camino corto) | F2 + a | 4, 5, 6, 7 | 11, 10, 9, 8 | 16, 15, 14, 13 (detrás de F1, lado largo) | **el corto** (F2 limpia) |

Todo fuera de la vista: la distancia mínima a cualquier sitio en el instante del teletransporte es **4 > r_vis = 3**
(se verifica: `ciego_al_llegar` debe ser 40/40). Cada episodio son **60 iteraciones** de la política: se registra la
dirección del **primer paso** (si en las 60 no se mueve, cuenta en `sin_mover` y no entra en la tasa) y el mismo
episodio sigue andando con el presupuesto que quede, para anotar **a qué comida llega** (`come`) y **si pisa el veneno**
en el camino (`pisa`; pisar es más estricto que morder — no se consulta la boca, así no entra el azar de la mordida). `E_test = 0.3`, traza y memoria de rechazo en cero, sitios repuestos antes de cada
teletransporte (ninguna comida falta nunca: trampa 3).

**El lado correcto del rodeo y el del atajo son opuestos** (en una semilla dada, rodeo = derecha ⇒ atajo = izquierda), y
**la mitad de las semillas corren el mapa en espejo** (`orientacion = ±1` por paridad de la semilla, sin tocar el `rng`).

## 3. Brazos (4; `corre_rodeo.py`)

| brazo | qué es | esperado |
|---|---|---|
| **MAPA** | v13 + `M` (`gamma_M = 0.6`) | la pregunta |
| **SINMAPA** | v13 en el mismo mundo, sin `M` | **0.500 por construcción**: con la retina vacía `x = 0`⁹ ⇒ `V = Wl@x = 0` ⇒ `p` igual en las dos patas ⇒ decide sólo el ruido `N(0,.3)` |
| **INVERTIDO** | MAPA; en la prueba `Wp ↔ Wn`, `Wps ↔ Wns` (`valor → −valor`; la puerta usa \|Wp−Wn\| y no cambia) | debe **ir hacia el veneno**: invierte R1 |
| **CONGELADA** | `M` nunca escrita (`escribe_M = False`) | = SINMAPA **bit a bit** (`_sesgo_M` devuelve [0,0]); se verifica `M_llenas = 0` |

## 4. Criterios (medianas sobre 20 semillas)

- **R1 (rodeo):** en los casos de rodeo esperado, MAPA da el primer paso **por el lado largo ≥ 0.70** y **> SINMAPA
  pareado en ≥ 15/20** semillas.
- **R2 (atajo):** en los casos de atajo esperado, MAPA va **por el lado corto ≥ 0.70**.
- **R3 (control decisivo):** **INVERTIDO ≤ 0.35 en R1** (con el valor del revés, debe meterse por el camino del veneno).
- **R4 (funcional):** MAPA **llega a una comida sin pisar el veneno ≥ 0.60** de los 40 episodios.
- **Validez (no son criterios, pero si caen el resultado no se interpreta):** V0 `v_B < −0.308·v_A` (§5) en ≥ 18/20
  semillas · V1 `M_llenas = 3` en MAPA e INVERTIDO, `0` en CONGELADA · V2 `ciego_al_llegar = 40/40` en los cuatro brazos
  · V3 SINMAPA y CONGELADA idénticos.
- **RODEA** = R1 ∧ R1 pareado ∧ R2 ∧ R3 ∧ R4.

## 5. Predicción numérica de mecanismo (la desigualdad, con las distancias de §2)

`_sesgo_M` suma por dirección `Σ disc^h · valor(M[pos±h])` con `disc = 0.9`, `H = 20`. Con las distancias de §2 y
`v_A = valor(A) > 0`, `v_B = valor(B) < 0`:

- **rodeo:** lado corto `v_A·0.9^d1 + v_B·0.9^dp`, lado largo `v_A·0.9^d2` ⇒ **rodea ⟺ `0.9^d2 > 0.9^d1 − |v_B/v_A|·0.9^dp`**,
  es decir `v_B < v_A·(0.9^d2 − 0.9^d1)/0.9^dp`. Umbral por distancia: `dp=4` → **−0.308·v_A** · `dp=5` → −0.242 ·
  `dp=6` → −0.160 · `dp=7` → −0.059. **El más exigente es `dp = 4`: rodea en los cuatro casos si `v_B < −0.308·v_A`.**
  Con los premios (`v_A = +1`, `v_B = −3`) el margen es **×9.7**; con el valor que el organismo del mapa suele tener
  (`v_B ≈ −1.6`, porque casi no muerde veneno) el margen sigue siendo **×5.2**.
- **atajo:** corto `v_A·0.9^a`, largo `v_A·0.9^(15−a) + v_B·0.9^(20−a)` ⇒ atajo ⟺ `v_B < v_A·(0.9^a − 0.9^(15−a))/0.9^(20−a)`,
  umbral más exigente (`a = 7`) **+0.188·v_A**: se cumple para cualquier `v_B ≤ 0`.
- **Tasas esperadas** (el ruido de la política es `N(0,.3)` por pata, el umbral de movimiento `u.max() > .5`, `p = 0.168`
  con `E_test = 0.3`, y el sesgo entra multiplicado por `gamma_M = 0.6`): **R1 ≈ 0.93–0.99**, **R2 ≈ 0.75–0.90**
  (el atajo tiene menos margen: en `a = 7` las dos comidas están a 7 y 8), **R3 ≈ 0.02–0.15**, **R4 ≈ 0.85–0.95**,
  SINMAPA y CONGELADA **0.500 ± binomial(40)**.
- **Predicción:** R1–R4 pasan → *"con el valor que ya tenía, elige entre dos comidas recordadas fuera de la vista la que
  le conviene, y se desvía por el lado largo cuando el corto pasa por veneno recordado"*. **No se dice "planifica"**
  (sigue siendo un paso de simulación sobre una tabla, sin secuencia de acciones ni horizonte aprendido) ni "rodea a
  propósito": lo que se mide es el primer paso y si llega.

## 6. Refutación (y qué NO se hace después de ver datos)

- **R1 < 0.70** (o pareado < 15/20): el `_sesgo_M` **no** produce el rodeo. Se registra refutado. Candidato siguiente
  (a preregistrar aparte, con semillas nuevas): sesgo con el **mínimo** por dirección en vez de la suma, o un `M` que
  guarde el camino y no sólo el sitio.
- **R3 > 0.35**: la dirección no corre por el valor de lo recordado ⇒ **ERR numerado**, no se declara nada aunque R1 pase.
- **R2 < 0.70 con R1 ≥ 0.70**: no elige, **huye**: siempre se va por el lado largo. Se registra tal cual (`no elige, evita`).
- **V0 falla en > 2/20**: en esas semillas el mecanismo no predice rodeo; se informan aparte, **no** se sustituyen semillas.
- **Nada se recalibra:** si un criterio falla, va ERR numerado + criterio nuevo + **semillas nuevas** (61–80), nunca un
  umbral movido sobre estos datos.

## 7. Las cuatro trampas (regla 5)

1. **Canal social simétrico** — no aplica: aquí no hay segundo organismo ni canal; el único "mensaje" es `M`, escrito y
   leído por el mismo bicho, y los brazos SINMAPA/CONGELADA lo apagan por completo.
2. **Acierto sin balancear** — el peligro real. Tres cierres: (a) **el lado correcto del rodeo y el del atajo son
   opuestos**, así que "siempre a la derecha" da R1 = 1.00 **y R2 = 0.00** (y al revés): ningún sesgo motor constante
   pasa R1 **y** R2; (b) la mitad de las semillas corren el mapa **en espejo**; (c) la línea base SINMAPA es 0.500 *por
   construcción* (demostrado en §3) y se compara **pareada por semilla**.
3. **Mundo que se come la comida (muestreo asimétrico)** — en la prueba no hay boca ni aprendizaje, y antes de cada
   teletransporte se vacía `_pend` y se repone `spawn()`: **los tres sitios están siempre puestos**, ninguna comida
   falta en ningún caso. Las dos comidas son el **mismo patrón `A`**: no hay valencia ni frecuencia que las distinga,
   sólo la geometría.
4. **Sitios fijos que se memorizan (el ciego ya sabe)** — los brazos sin mapa no tienen ninguna memoria de posición:
   la política `Wl` se alimenta de la retina (6 píxeles + lado + contacto), **nunca de `pos`**, así que con la retina
   vacía no puede haber sesgo posicional aprendido (de ahí el 0.500 exacto). Además `F0` es aleatorio por semilla y la
   orientación se invierte en la mitad de las semillas: no hay posición absoluta que memorizar.

Coste: 4 brazos × 20 semillas = 80 corridas de 100 000 + identidad (27 comparaciones). Lo corre el coordinador con `Pool`.


## Enmienda 1 (17 sep 2026, 23:30; escrita DESPUÉS de la serie 41–60 y ANTES de la serie 61–80)

En 41–60 R1–R4 pasaron (R1 0.700, pareado 19/20; R2 0.775; R3 0.25; R4 0.85) pero V0 se cumplió en 15/20 (se exigían 18) y
V1 no en todas: con mapa `v_B` ≈ −0.74 (muerde poco veneno) y en algunas semillas la desigualdad no predice rodeo. Serie
nueva 61–80, mismos criterios, y **análisis adicional preregistrado sobre el subconjunto válido** (semillas con V0 y V1):
válidas ≥ 12; R1 mediana ≥ 0.70 en el subconjunto y pareado (MAPA > SINMAPA) en ≥ 75 % del subconjunto; R2–R4 igual. El
conjunto completo se reporta también. Si el subconjunto pasa y el completo no, el vocabulario es: *rodea cuando el
veneno recordado pesa lo que el mecanismo exige; si no lo conoce, no rodea* (el mecanismo es el que es). Nada se
recalibra sobre 41–60.
