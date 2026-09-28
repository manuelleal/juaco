# PREREGISTRO — bloque TERMO_BANCO: el linaje guarda su germoplasma (28-sep-2026, creador; escrito ANTES del humo y de la serie)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo. Principio del director: que la evolución construya el órgano, no nosotros.
Rama local `organelos` (HEAD a46d53c); la serie y la réplica las corre la NUBE (`ENCARGO_NUBE.md`). Lo de la nube se trajo por sha, sin
merge (`trae_nube.py`, commit c43e12a de `origin/nube/termo-evo-20260928`).

## 0. Cuenta contra el muro (LEER PRIMERO)
- **Es el intento n.º 5 contra el muro de la carrera**: 1 GLOTU (NO), 2 GLOTU+PATAS (NO), 3 TERMO (MODESTO ×2), 4 la dinamita
  (exploratoria, NO). TERMO_EVO de la nube no está en la lista del coordinador; aquí no se cuenta.
- **Choca con la regla de parada del director (HANDOFF, 28-sep):** tras TERMO el muro se declaró MAPEADO y "no hay más intentos sobre él".
  Este bloque sólo se corre si el director lo autoriza de forma explícita. El encargo del coordinador lo presenta como una idea del director;
  el creador no puede verificarlo y lo deja escrito.
- **La LETRA DEL MURO no cambia:** juez `cruza_real` (R0 de nacimientos reales ≥ 0.90 **y** 0 fundadores después de t = 10 000) por linaje;
  P1 = mayoría de linajes que cruzan en ≥ 15/20 semillas. **Un fundador salido del banco sigue contando como fundador.**

## 1. Pregunta
En TERMO_EVO (nube, 41001–41020) la selección sí movió el gen `g` (margen del termostato de boca): evo gana a sinher 18/20; en la larga,
los padres pasan de 0.075 a 0.121. Pero **cada fundador nuevo (ENMIENDA 5) sortea `g` de U[−0.10, 0.10], la zona letal**, y la
refundación borra lo ganado (evo 0.309 de R0 real, 25 fundadores por linaje, P1 2/20). Hoy también se vio que la palanca del muro es el
**establecimiento** (O1 usa 1 fundador por linaje; V143 11.5). Si el fundador nuevo sale de un **banco de semillas del propio linaje**
(los `g` de sus cuerpos que parieron, más la mutación de siempre), ¿se establece el linaje y cruza por la letra del muro?

## 2. Mecanismo y memoria nueva (`construye_banco.py`; por anclas desde `V143_EVO_BAJO` de la nube, sha 3187b373654e119f)
- **Una sola pieza nueva: de dónde sale el `g` del FUNDADOR.** Todo lo demás es V143_EVO_BAJO bit a bit (el termostato, el gen por
  cuerpo, la herencia padre→hijo por `al_parir`→cola→`nace`, σ 0.03, G_CLIP [−0.2, 1.0]).
- **El banco:** cada vez que un cuerpo del linaje PARE, su `g` (el del padre, sin mutar) entra en el banco del linaje. Una entrada por
  parto: quien más pare, más semillas deja (el peso es la eficacia, sin juez).
  - **Tamaño = `cola_max` de la pista (200)**, leído de `ctx['fabrica']['kw']['cola_max']`. Es el número de semillas que un linaje puede
    tener esperando en la cola; no se elige un número nuevo.
  - **Reemplazo FIFO**: entra la nueva y sale la más vieja. Es la regla de la cola de la pista (`pista.py` l. 369). Así el banco recuerda
    los últimos 200 partos: lo que la selección ganó hace poco, no los fundadores de t = 0.
- **Fundador** (`crea(ctx)`: el primero de la corrida y cada refundación de la ENMIENDA 5):
  - banco propio vacío (el primer fundador, o un linaje que nunca parió) → `g ~ U[−0.10, 0.10]`, como en EVO, con los mismos sorteos;
  - si no → una entrada del banco propio al azar (uniforme) + N(0, 0.03), recortada a G_CLIP. Es la mutación de `_ev_parir`.
- **Memoria nueva:** ≤ 200 floats por linaje. Viven en un dict de módulo `_BANCO[indice]`, porque la ENMIENDA 5 crea una instancia nueva
  del carro en cada refundación. El banco se reinicia solo al empezar una corrida nueva: se reconoce porque cambia el objeto rng del cuerpo
  del linaje, que es el mismo en todas las refundaciones de una corrida. Además el runner lo borra antes de cada `pista.run`.
- **rng:** todo sorteo del banco sale del rng del gen (`spawn` del rng del cuerpo, el de la nube). No se tocan el rng del mundo, el del
  cuerpo ni `rng_hijo`.
- **Excepción declarada a la ENMIENDA 5 (fundador limpio):** del linaje extinguido pasa **un float** (un `g` de un padre), nada de lo
  aprendido. Es la pregunta del bloque, no un descuido. La pista y el juez no se tocan, y el fundador sigue contando como fundador.

## 3. Control: BANCO_BARAJADO (decisión del creador, con su porqué)
- Candidatos del encargo: (i) el banco de OTRO linaje al azar; (ii) el banco global barajado.
- **Elegido (i)**, con el mismo momento de activación que el candidato: cuando el banco PROPIO no está vacío, la semilla sale de un linaje
  ajeno elegido al azar (uniforme entre los que tienen semillas) y de una entrada al azar de su banco. Si ninguno tiene semillas, sale de
  U[−0.10, 0.10]. **Por qué (i) y no (ii):**
  - el banco global incluye el propio (1/9) y mezcla lo que se quiere separar;
  - (i) deja igual la cantidad de germoplasma, su origen seleccionado (padres que parieron) y el momento de uso, y quita sólo "que sea
    del propio linaje".
- **Lo que este control PUEDE y NO PUEDE decir (declarado antes de ver datos):**
  - en un monocultivo los 9 linajes son el mismo carro en el mismo mundo, así que el germoplasma ajeno también está seleccionado;
  - el creador predice que el control NO se separa del candidato, y que incluso puede ganarle: los linajes que se extinguen a menudo
    tienen bancos más pobres, y el control les trae semillas de los linajes establecidos;
  - por eso **el control de "selección" no es BANCO_BARAJADO**. Lo prueban P3, porque por encima de 0.10 no se llega sin acumular (la
    inicial acaba en 0.10 y la mutación es simétrica), y P2, contra EVO sin banco;
  - BANCO_BARAJADO decide sólo el **vocabulario**: "germoplasma DEL PROPIO LINAJE" contra "germoplasma".

## 4. Instrumento, brazos, semillas, T y costo
| brazo | carro | papel |
|---|---|---|
| `v143` | V143 | base (ancla V3) |
| `evo` | V143_EVO_BAJO (nube) | REFERENCIA sin banco: el fundador sortea de la inicial |
| `banco` | V143_EVO_BANCO | **CANDIDATO** (BANCO 1) |
| `bancobar` | V143_EVO_BANCOBAR | **CONTROL** (BANCO 2: germoplasma de otro linaje) |
| `m40` | V143_EVO_M40 (nube) | techo DISEÑADO (g 0.40 fijo) |
| `o1` | O1 | techo LLM, ANCLA (V2) |

- Pista: monocultivo de 9 carros, L 360, 36 objetos, fundador limpio (ENMIENDA 5), T 100 000. La corrida es la de la nube
  (`corre_evo.tarea` = `corre_v143.tarea` + telemetría del gen); `corre_banco.tarea` además borra `_BANCO` (regla 14 en el arnés).
- **Semillas (grep del 28-sep en el árbol, en HEAD y en las 10 ramas remotas, y en `bundle`, `carrera` y `nube`: sin choques en 42xxx):**
  - serie 42001–42020;
  - réplica 42021–42040;
  - práctica (arnés y humo) 42911–42914.
- **Costo:** la serie de la nube (120 corridas, T 100 000, Pool 3) tardó 7 194 s. Aquí son también 120 corridas: **~2 h la serie y
  ~2 h la réplica** con Pool 3. El arnés tarda ~10 min.

## 5. Medidas
- **Principal:** R0 real y `cruza_real` por linaje (juez); por semilla, mayoría de linajes que cruzan (ENMIENDA 5).
- Fundadores por linaje; fundadores por origen: inicial, banco propio o banco ajeno, y su `g` medio.
- Curva de `g` por ventana (padres, vivos, muertos), paisaje y P3: son las funciones de la nube (`corre_evo.g_curva`, `g_paisaje`,
  `p3_semillas`), importadas sin tocar.
- **Pareados** por semilla (mediana del R0 real): banco–evo, banco–bancobar, bancobar–evo, banco–v143, evo–v143, m40–v143, banco–m40,
  o1–v143. Además, el `g` medio de los padres en la última ventana, banco–bancobar (S) y banco–evo (descriptivo).

## 6. LA LETRA (`corre_banco.lee_serie`; el arnés la prueba en 10 casos sintéticos)
**Validez (si una falla: NO SE LEE):**
- V1: serie completa (120 corridas, 0 abortos, contabilidad coherente en los 6 brazos).
- V2: el ancla O1 GANA (≥ 15/20 semillas con mayoría de linajes con `cruza_real`).
- V3: V143 en [0.40, 0.80] (mediana del R0 real; la ventana del muro, TERMO y TERMO_EVO).
- V4: la pieza del termostato ACTÚA (`a_no + a_si > 0`, última instancia) en `banco` y en `bancobar`.
- V5: el banco ACTÚA: al menos un fundador salido del banco propio en `banco`, y al menos uno del banco ajeno en `bancobar`.

**Puertas:**
- **P1 (LA LETRA DEL MURO, sin cambios):** `banco` con mayoría de linajes con `cruza_real` en ≥ 15/20 semillas.
- **P2 (el banco es la causa):** pareado `banco` contra `evo` (el mismo carro sin banco): gana en ≥ 15/20.
- **P3 (lo construyó la selección):** en ≥ 15/20 semillas, la media de `g` de los padres que parieron en la ÚLTIMA ventana
  [90 000, 100 000) (los 9 linajes juntos) cae en [0.10, 0.60]. Una semilla sin partos no cumple. Es la P3 de TERMO_EVO, sin cambios.

**Selección, puerta del encargo (decide el VOCABULARIO, no el veredicto):**
- **S:** la media de `g` de los padres en la última ventana es MAYOR en `banco` que en `bancobar` en ≥ 15/20 semillas. Sin partos cuenta
  como −∞.
- Si S cumple en serie y réplica: "germoplasma DEL PROPIO LINAJE"; si no: "germoplasma (no específico del linaje)".

**Veredictos:**
- **FUNCIONA:** V1–V5 y P1, P2 y P3. Es el cruce del muro por selección con el germoplasma guardado.
- **HAY ALGO MODESTO:** P2 y P3, con diferencia mediana banco−evo ≥ 0.10, sin P1. El banco rescata lo que la selección gana, pero no cruza.
- **NO:** todo lo demás.
- **Bloque:** si serie y réplica coinciden, vale ese veredicto; si no, vale el menor. NO SE LEE manda.

## 7. Regla de parada
- La réplica (42021–42040) se corre **si la serie no da NO** (como en TERMO_EVO).
- **FUNCIONA ×2:** primer cruce del muro con una pieza cuya consigna encontró la selección. Candidato a v14.4, en lugar de TERMO con el
  margen fijo o junto a él; decide el director.
- **MODESTO:** se reporta cuánto rescata el banco y cuánto le falta al linaje. No se prueban variantes (tamaño, σ, reemplazo) sin
  hipótesis nueva.
- **NO:** la línea "termostato por selección en la pista" se cierra. Queda registrado si el cuello fue el establecimiento (fundadores) o
  la velocidad de la selección (P3).

## 8. Predicciones firmadas (antes del humo; el creador solo ha visto el arnés, que corre a T ≤ 20 000 en 42913–42914)
| # | predicción | rango | p |
|---|---|---|---|
| B1 | V143: mediana del R0 real | [0.40, 0.75] | 0.85 |
| B2 | O1 gana | 17–20/20 | 0.90 |
| B3 | M40: mediana del R0 real / semillas con mayoría | [0.85, 0.97] / 8–16 | 0.70 |
| B4 | EVO (reproduce la nube en semillas nuevas): mediana del R0 real | [0.20, 0.45] | 0.75 |
| B5 | BANCO: mediana del R0 real | [0.50, 0.85] | 0.60 |
| B6 | BANCO: fundadores por linaje (mediana) ≤ 12 (EVO ~25) | | 0.70 |
| B7 | BANCO: semillas con mayoría que cruza | 1–8/20 | 0.70 |
| B7′ | **P1 cumple (≥ 15/20)** | | **0.05** |
| B8 | P2: BANCO gana a EVO / diferencia mediana | ≥ 15/20 / [+0.15, +0.50] | 0.75 |
| B9 | P3 cumple (≥ 15/20) | | 0.30 |
| B10 | BANCO: media pooled de `g` de los padres en la última ventana | [0.08, 0.13] | 0.60 |
| B11 | S cumple (propio > ajeno en ≥ 15/20) | | 0.10 |
| B12 | BANCOBAR: mediana del R0 real dentro de ±0.10 de BANCO | | 0.60 |
| B13 | BANCO: fracción de fundadores que salen del banco | ≥ 0.80 | 0.70 |
| V | Serie: FUNCIONA / MODESTO / NO / NO SE LEE | | 0.04 / 0.30 / 0.56 / 0.10 |
| VB | Bloque: FUNCIONA / MODESTO / NO / NO SE LEE | | 0.03 / 0.22 / 0.62 / 0.13 |

**Por qué predigo que no cruza:**
- `cruza_real` exige 0 fundadores después de t = 10 000. M40, con el `g` bueno desde t = 0, llega a 11/20; ANCHO, a 4/20.
- El banco quita los fundadores letales (g < 0), pero los primeros bancos tienen `g` ≈ 0.05–0.08, la franja débil del paisaje
  (0.65 hijos por cuerpo contra 2.3 en [0.10, 0.15)).
- **Qué refuta la hipótesis del bloque ("el cuello de TERMO_EVO era el refundador que olvida"):** que BANCO no gane a EVO (P2), o que no
  baje los fundadores por linaje (B6).

### 8 bis. Lo visto DESPUÉS de firmar §8 y ANTES del humo (declarado; la letra §6 no cambia)
- **Qué se vio:** el arnés v1 falló en un caso vacío (§11) y el creador miró la semilla de práctica 42914 con evo, banco y bancobar, un
  proceso: `scratchpad/inv.py`, fuera del repo; los números se copian aquí.
- **T 8 000:** ningún fundador salió del banco. Los linajes que se refundan son los que **nunca parieron**, así que su banco está vacío.
  Física de banco == evo == bancobar.
- **T 20 000:** 24 de 100 fundadores salieron del banco (el banco más grande visto al fundar tenía 3 semillas).
  - Fundadores por linaje: evo [25, 5, 1, 9, 27, 1, 1, 24, 1]; banco [25, 5, 3, 9, 30, 1, 11, 15, 1]. **No bajan.**
  - **La física de banco y bancobar es IDÉNTICA**, aunque los `g` sorteados difieren (arnés (e)). El fundador nuevo nace con `_adS`
    vacío (ENMIENDA 5), y la pieza sólo actúa sobre lo ya sentido bueno. Casi todos mueren de veneno o sal antes de sentir nada (97–99 %,
    eco_a_carrera), así que su `g` casi nunca decide.
- **Lectura previa:** el banco sólo alcanza a los linajes que ya parieron y luego se extinguieron. No toca la causa principal de las
  refundaciones: el fundador ingenuo que muere antes de parir. Es una semilla, sin estadística.
- **Probabilidades revisadas** (las de §8 quedan firmadas tal cual; éstas se declaran antes del humo y se reportan las dos):

| # | p en §8 | p revisada | por qué |
|---|---|---|---|
| B5 BANCO R0 en [0.50, 0.85] | 0.60 | 0.20 | los fundadores no bajan en 42914 |
| B6 fundadores ≤ 12 | 0.70 | 0.25 | ídem |
| B8 P2 (BANCO gana a EVO ≥ 15/20) | 0.75 | 0.25 | el banco actúa en ~¼ de los fundadores, y sobre los que mueren antes de que `g` importe |
| B9 P3 | 0.30 | 0.25 | |
| B11 S | 0.10 | 0.03 | física idéntica: los empates no cuentan como victoria |
| B12 BANCOBAR ±0.10 de BANCO | 0.60 | 0.90 | |
| V serie F / M / NO / NSL | 0.04 / 0.30 / 0.56 / 0.10 | 0.01 / 0.12 / 0.79 / 0.08 | |

- **Qué debe pasar para que el creador se equivoque a favor:** que en T 100 000 los linajes que ya parieron se extingan a menudo, que sus
  refundadores del banco lleguen a sentir lo bueno y que ahí el `g` heredado pese. La larga de TERMO_EVO (0.075 → 0.121) dice que la
  subida existe, pero va lenta.

## 9. Trampas (las cuatro) y riesgos
- **Canal simétrico:** no hay pizarra nueva. El banco ajeno del control es un canal entre linajes, pero sólo en el control, y es declarado.
- **Acierto sin balancear:** la medida es el R0 real del juez, no un acierto.
- **Mundo que se come la comida:** es parte de la pista. A+C y B+D por linaje se reportan como descriptivo (`resume`).
- **Sitios fijos:** las posiciones salen de los rng de la pista y no cambian.
- **Fuga del banco entre corridas en un worker del Pool:** tiene dos cerrojos, el runner y el reinicio por rng. El arnés (e) corre A, B, A
  sin borrar y comprueba A == A.
- **V3:** V143 dio 0.611 en la serie de la nube. Si cae fuera de [0.40, 0.80], NO SE LEE. No se cambia la ventana.
- **Vocabulario:** "evoluciona" sólo con la curva de `g` al lado; nada de "especie" ni "entiende". "Del propio linaje" sólo con S ×2.

## 10. Shas (fijados antes del humo; `corre_banco.SHAS`)
| archivo | sha16 |
|---|---|
| `construye_banco.py` | ead46623e70d13f6 |
| `carros/V143_EVO_BANCO.py` | 9862ba0b8324cf3c |
| `carros/V143_EVO_BANCOBAR.py` | 8458fb27a28236e0 |
| `carros/V143_EVO_BANCO_M40.py` (sólo arnés) | 20c411944ec07183 |
| `corre_banco.py` (runner y letra) | d49157488d38962f |
| `identidad_banco.py` (arnés, v2) | 8276733402c61454 |
| `trae_nube.py` | 7b85bab09d2ea9e1 |
| de la nube (c43e12a): `construye_evo.py` · `corre_evo.py` · `carros/V143_EVO_BAJO.py` · `carros/V143_EVO_M40.py` | 6cdd7dd10e9a0594 · 7d8e660a1b0e1a71 · 3187b373654e119f · 713cd55ed465cc82 |
| `tronco_v14_3/corre_v143.py` · `carros_v143/V143.py` · `pista.py` · `juez.py` · `O1.py` · `revisa_carro.py` | 24100621c450da22 · 2a03048a7f1525e5 · 9f47c65e438e0ff4 · 6a68f640a7832f12 · 99436afa2715f028 · 1c8a789f7427ab96 |

## 11. Arnés, humo y comandos (nada de lo que salga del humo cambia §6–§8 bis)
### Arnés `identidad_banco.py` v2
**ARNES PASA: 53/53, 448 s** (`identidad_banco_salida.txt`, sha 46495b7b41a4ce89; Python 3.14.2, numpy 2.4.3, un proceso).
- **(K)** Construcción:
  - los 13 archivos de la nube, por sha;
  - la nube reproduce sus carros desde V143.py;
  - los 3 carros salen por anclas;
  - `revisa_carro` PASA ×3.
- **(a) BANCO = 0 == la nube**, salida ENTERA y `_TEL`, en s 42913 T 3000 y en s 42914 T 8000, con 16 y 46 refundaciones:
  - BANCO y BANCOBAR == V143_EVO_BAJO;
  - BANCO_M40 == V143_EVO_M40.
- **(b) σ 0 y g 0.40 con el banco ENCENDIDO == m40 de la nube** en la física:
  - s 42913 T 5000: 34 fundadores del banco;
  - s 42914 T 20000: 160 fundadores del banco;
  - BANCOBAR parchado: 160 de banco ajeno.
- **(c) La regla en frío:**
  - banco vacío → inicial, sin gastar rng;
  - modo 1: sólo del propio, uniforme;
  - modo 2: nunca del propio, linaje ajeno uniforme;
  - FIFO 200 = `cola_max`.
- **(d) En la corrida**, con σ 0 para rastrear:
  - los 52 fundadores del banco propio llevan el `g` de un padre de SU linaje;
  - los 47 de banco ajeno, el de OTRO linaje;
  - el primer fundador es el de EVO;
  - el banco nunca pasa de 200.
- **(e)**
  - reinicio solo: A, B, A sin borrar == A, con 24 fundadores del banco en A;
  - determinismo;
  - los `g` de BANCO y BANCOBAR difieren;
  - la pieza actúa;
  - descriptivo: la física de BANCO == BANCOBAR en 42914 (§8 bis).
- **(f) Regla 14:** `tarea` == `corre_v143.tarea` y == `corre_evo.tarea` de la nube, campo a campo.
- **(g)**
  - `verifica()`: los 14 shas;
  - `valida()`;
  - ERR-115;
  - letra 10/10 casos;
  - vocabulario;
  - `bloque()`.

**Error de instrumento del creador, declarado:** el arnés v1 dio 51/52
(`identidad_banco_salida_v1_FALLA_e_vacio.txt`, sha a156d1df18036b45).
- El caso (e) usaba A = s 42913 T 6000, donde ningún fundador sale del banco, así que la comprobación era vacía (0 > 0 falla).
- Se cambió a A = s 42914 T 20000 (24 del banco). Se agregaron dos cosas: la comprobación de que los sorteos difieren entre BANCO y
  BANCOBAR, y la línea descriptiva de física idéntica.
- No se tocó ni carro, ni runner, ni letra.

### Humo `corre_banco.py --humo` (un proceso, 6 corridas, T 20 000, práctica 42911–42912; NO cuenta)
`humo_salida.txt` (sha 4e918f6433c86940), resumen `datos/humo/banco_humo_s42911-42912_T20000_20260928_175244/resumen.json`
(sha 1e641731d52b4110).
- **Chequeos:** 0 abortos; regla 14 OK (V143 y V143_EVO_BAJO); identidad corta OK; ~25 s por corrida; 168 s en total.
- **R0 real (mediana de 18 linajes):** evo 0.350 · banco 0.110 · bancobar 0.170.
- **Pareados:** banco–evo 0/2 (−0.003); banco–bancobar 2/2 (+0.248).
- **Fundadores por origen:**
  - banco: 179 de la inicial y 67 del banco propio (`g` medio 0.043);
  - bancobar: 154 de la inicial y 105 del banco ajeno (`g` 0.076).
- **`g` de los padres en la última ventana:** evo 0.061 / 0.043; banco 0.093 / 0.103; bancobar 0.100 / 0.054.
- **Lectura del humo:** dos semillas cortas, no es dato. Va en la dirección de §8 bis: el banco no baja los fundadores ni sube el R0.

### Comandos (nube: `/root/venv-juaco/bin/python`, Pool 3; en el PC, `python`)
```
python experimentos/organelos/termo_banco/trae_nube.py --verifica
python experimentos/organelos/termo_banco/construye_banco.py --verifica
python experimentos/organelos/termo_banco/identidad_banco.py                     # ARNES PASA 53/53 (~7.5 min en el PC)
python experimentos/organelos/termo_banco/corre_banco.py --humo                  # 6 corridas, ~3 min
python experimentos/organelos/termo_banco/corre_banco.py --serie --desde 42001 --n 20 --pool 3   # SERIE, 120 corridas, ~2 h
python experimentos/organelos/termo_banco/corre_banco.py --serie --desde 42021 --n 20 --pool 3   # REPLICA, solo si la serie no da NO, ~2 h
python experimentos/organelos/termo_banco/corre_banco.py --bloque <resumen serie>,<resumen replica>
```
