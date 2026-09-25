# PREREGISTRO: CONTROL DEL ANFITRIÓN (organelos, Opus B, 24-sep-2026; antes de cualquier serie)

Misión: llegar a la AGI por este camino. Frente 2 (ECO). Carpeta: `experimentos/organelos/anfitrion/`. Sólo copias; ningún archivo existente se modificó.

**De dónde viene.** Endosimbiosis dio **HAY ALGO MODESTO ×2** (commit f464ae0):
- el simbionte heredado se domestica por selección: P3, 18 y 16/20 en la serie, 17 y 17/20 en la réplica;
- **portarlo cuesta**: P1 cae ×2, porque SIN_TRAGAR e INERTE persisten más;
- P2 casi no fue evaluable.

**Principio del director:** *"la evolución arranca DESDE LO MÁS EVOLUCIONADO que tengamos, no desde cero".*

**Pregunta:** con control del anfitrión, ¿portar pasa a ser buen negocio?

## 0. Instrumento (sha a 16; `corre_anf.py` los imprime en cada log)

**Orígenes (sólo se leen):**
- `darwin/motor_endo.py`, 7e10329cf0cb9fd0;
- `darwin/simbiontes.py`, 72f8829defe3e69f;
- `darwin/corre_endo.py`, 078734369e9721c5 (sus `medidas`);
- `darwin/carros/FABRICA_SIMB.py`, 38ac0ddba8829c88;
- `juaco_eco/corre_eco.py`, 47d9cee4d6462116.

**Construido por anclas:** `construye_anf.py` (16980240f186aa25) produce `motor_anf.py` (**8d46795ec2b645b8**). Son 4 anclas:
- importa `control_anfitrion` como SIM;
- busca los carros en darwin;
- agrega la ranura `ctl`;
- agrega el gancho `siembra` después de `banco_ini`.

**Siembras:** `construye_siembras.py` (c29334d3bd395457) produce `siembras.json` (**8ff067ba6ace9f37**), con la ruta y el sha de cada fuente adentro.

**Código nuevo:**
- `control_anfitrion.py` (**b26bb3efd78834a3**);
- `corre_anf.py` (**191e9050e086b3bd**);
- `identidad_anfitrion.py` (**7006b880b8b7fa2f**).

**Arnés `identidad_anfitrion.py`: 16/16, N/N** (218 s, un proceso, semilla 26994; salida en `identidad_anfitrion_salida.txt`).

| caso | qué comprueba |
|---|---|
| (F) | anclas y siembras |
| (A1) | simb=None == motor_endo bit a bit |
| (A2, A3) | VIDA_S y AZAR_S de hoy == motor_endo bit a bit |
| **(A4)** | **control APAGADO (SIN_CONTROL sin siembra) == motor_endo VIDA_S bit a bit** |
| (A5) | CONTROL con mutación 0 == motor_endo |
| (S) | siembra: 30 portadores en t = 0; SIN_TRAGAR no siembra |
| (K1a, K1b) | pieza tx: tx 0 no transmite en ningún parto; tx 1 no toca el rng del control |
| (K2a, K2b) | pieza san: san 1 sanciona a todo candidato; san 0 a ninguno; sin canal no hay candidatos |
| (M) | CONTROL mueve el control; SIN_CONTROL no |
| (Z) | AZAR sortea |
| (E) | determinismo |
| (H) | contabilidad y bancos alineados |
| **(N9)** | un trabajo con error NO lanza: devuelve `error` y escribe su JSON |

**nube-9:** con simb, ERR-60 se registra y no lanza (motor_endo G5); `trabajo` atrapa `BaseException`.

## 1. Hipótesis
**H-C.** Dos genes del bicho que regulan al simbionte hacen rentable la fusión:
- transmisión regulada (tx);
- sanción por consecuencia (san).

Con ellos, los linajes portadores persisten más y tienen más R0 que los que no tragan y que los de simbionte inerte, y el control le gana a no tenerlo.

## 2. Mecanismo mínimo (detalle en el docstring de `control_anfitrion.py`)

**Dos genes nucleares nuevos del bicho.** Viven en la ranura `Cuerpo.ctl`, se heredan del padre y mutan; el vector GENES del motor no cambia.
- **tx ∈ [0, 1]:** en cada parto el padre portador transmite su simbionte con probabilidad tx. Se aplica antes de la falla de siempre (p_falla 0.05).
- **san ∈ [0, 1]:** si el cuerpo muerde una letra que le hace daño y el canal del simbionte empujaba a morderla (su término en la boca era > 0), el cuerpo lo digiere con probabilidad san.
  - "Le hace daño" significa que el efecto físico de la letra tiene una componente negativa, que es la misma señal con la que aprende su cerebro.
  - Sin canal no hay empuje y no hay sanción.
  - La regla no dice qué letra es mala: la lee de la consecuencia.
- Nacen **apagados**: tx = 1 y san = 0, que es el mundo de hoy.
- Mutan en cada parto y en cada fundador del vivero: cada gen con p 0.1 se mueve N(0, 0.1), con reflexión en [0, 1].
- RNG propio: [seed, 0, 32, 0].

**Memoria nueva:** 2 números por cuerpo. En el cerebro, 0.

**Arrancar desde lo más evolucionado (siembras):**
- **Huéspedes:** los 30 fundadores salen del banco de VIDA en el corte de ECO v1.1 (19401–19440; 8000 genomas de FABRICA en w90). Es la colonia que vive 3.2–3.3× la de AZAR con el juez v2 calibrado. Se muestrean con [seed, 0, 33, 0], sin reemplazo. Los 7 órganos de motor_eco3 van en 0.9 (apagados), con 0 recortes de rango.
- **Simbiontes:** cada fundador, salvo en SIN_TRAGAR, nace con uno DOMESTICADO, muestreado con [seed, 0, 31, 0].
  - Salen de 2428 vectores: el g medio de los simbiontes de adentro de VIDA_S en cada muestra con t ≥ 10 000 y ≥ 1 portador, en la serie 22001–22020 y la réplica 22021–22040 de endosimbiosis.
  - **Declarado:** los genomas individuales transmitidos no se guardaron (`don` sólo tiene I; `dentro_final` tiene 1 genoma en 40 corridas). Por eso se siembran medias de 1 a ~5 portadores.
  - El banco del vivero y el anillo de AZAR arrancan con esos simbiontes.

**Brazos:**

| brazo | qué es |
|---|---|
| **CONTROL** | VIDA_S + siembra + tx y san que evolucionan |
| **SIN_CONTROL** | lo mismo con tx 1 y san 0 fijos. **Es el control que puede fallar** |
| **INERTE** | sin canal + siembra + control que evoluciona; en la práctica sólo tx, porque sin canal no hay sanción |
| **SIN_TRAGAR** | el bicho sembrado, sin simbiontes ni tragar |
| **AZAR** | deriva: el simbionte sale del anillo de AZAR_S y el control de cada cuerpo nuevo de un anillo de estados nuevos, mutado |

**Mundo:**
- w30, que es el de endosimbiosis: 30 fundadores FABRICA_SIMB, quimiostato r 0.03, tope de 3000 cuerpos.
- **T 100 000 y corte 40 000.** El vivero es más corto porque los fundadores ya vienen evolucionados.
- La ecología de los libres es la de endosimbiosis, sin cambios.

## 3. PODER: qué se calibró y qué se cambió (declarado, antes de la serie)
- **Calibración** (`calibra_poder.py` → `calibra_poder_salida.json`): SIN_TRAGAR con los huéspedes sembrados, semillas de práctica 26991–26992, corte 40 000, T 100 000.

  | comida | cuerpos tras el corte (mediana) | area_post |
  |---|---|---|
  | r 0.03 | 3 y 2 | 230 y 244 |
  | r 0.045 | 4 y 3 | 324 y 244 |

  - Registrado en ECO v1.1 (FABRICA en w90): ~6 cuerpos tras el corte.
  - **Lectura:** ni más comida ni un mundo más grande arreglan el poder. El mundo tiene objetos de sobra (nobj ≈ 96 de 120): lo que falla es el R0 < 1 de FABRICA tras el corte, que es estructural en este carro.
  - **Se queda r 0.03**, para que siga siendo comparable con endosimbiosis.
- **La medida sí cambia, para que P2 se pueda leer.**
  - La cohorte de P2 son TODOS los **NACIDOS** (no los fundadores del vivero) con t_nace en [10 000, T_ef − 20 000], vivero incluido.
  - Nacer es reproducción real; el vivero sólo agrega competidores, y lo hace igual en todos los brazos.
  - En el humo (T 60 000) salieron 99–324 nacidos por grupo, cuando antes eran 0–7.
- **P1 sigue siendo `area_post`.** Sí tuvo poder: en endosimbiosis cayó 15/20 y 18/20 en contra.
- **Si hiciera falta más** (no en esta serie), el siguiente paso es el gemelo numba en w270: ver `ESPEC_GEMELO_anfitrion.md`.

## 4. Predicciones firmadas

Dato visto antes, declarado. Es el humo 26990 (T 60 000, corte 30 000), una semilla y sin valor:
- area_post: CONTROL 99, SIN_CONTROL 94, INERTE 105, SIN_TRAGAR 69, AZAR 145;
- r0 de nacidos portadores: CONTROL 0.237 (266 cuerpos), SIN_CONTROL 0.168, INERTE 0.146, AZAR 0.354; SIN_TRAGAR, todos, 0.190;
- tx del banco: CONTROL 0.97, INERTE 0.93, AZAR 0.84; san del banco: CONTROL 0.07, AZAR 0.16;
- fracción con simbionte tras el corte: INERTE 0.76.

| cantidad (por ventana de 20) | rango | P(≥ 15/20) |
|---|---|---|
| **PC** area_post CONTROL > SIN_CONTROL | 8–14 | 0.15 |
| P1a area_post CONTROL > SIN_TRAGAR | 5–14 | 0.15 |
| P1b area_post CONTROL > INERTE | 5–13 | 0.10 |
| P2a r0 de nacidos portadores CONTROL > r0 de todos en SIN_TRAGAR (evaluables 18–20) | 8–16 | 0.30 |
| P2b r0 de nacidos portadores CONTROL > INERTE (evaluables 18–20) | 9–17 | 0.35 |
| descriptivo: tx del banco CONTROL > AZAR | 11–18 | — |
| descriptivo: san del banco CONTROL < AZAR | 10–17 | — |
| fracción con simbionte bajo DERIVA (AZAR, mediana) | 0.15–0.50 | — |
| INERTE con fracción ≥ 0.9 (trinquete) | 1–8 semillas | P(≥ 10) = 0.12 |

**Veredicto por ventana:** FUNCIONA 0.02 · HAY ALGO MODESTO 0.38 · NO 0.45 · NO EVALUABLE 0.15. Mi apuesta es **NO**.
- En endosimbiosis, portar perdió 18/20 contra SIN_TRAGAR.
- tx y san parten apagados y mutan lento; en el humo, tx del banco sólo bajó a 0.97.
- P2 es la que más puede pasar, porque los simbiontes sembrados ya están domesticados.

## 5. Controles, y cómo puede fallar cada uno
- **SIN_CONTROL** (PC). Si CONTROL no le gana en ≥ 15/20, **el control no sirve**. Es la pregunta propia del paquete.
- **SIN_TRAGAR** (P1a, P2a). Si portar no supera a no tragar, portar sigue sin ser negocio.
- **INERTE** (P1b, P2b). Si el portador con canal no supera al portador inerte, lo que paga es el tragar o la digestión, no la función del simbionte.
- **AZAR** (descriptivo y trinquete). Deriva del control y del simbionte. Si AZAR o INERTE tienen fracción ≥ 0.9 en ≥ 10/20: NO EVALUABLE.
- **Instrumento.** Si en SIN_CONTROL o en SIN_TRAGAR el control se mueve de (1, 0) en alguna corrida: NO EVALUABLE.

## 6. La letra (`corre_anf.veredicto`)
Todas las comparaciones son pareadas por semilla y estrictas; una semilla sin dato no cuenta a favor. Umbral: ≥ 15/20 (P = 0.021 bajo p = 0.5).
- **PC:** CONTROL > SIN_CONTROL en area_post.
- **P1:** CONTROL > SIN_TRAGAR **y** CONTROL > INERTE en area_post.
- **P2:** r0 de nacidos portadores de CONTROL > r0 de todos los nacidos de SIN_TRAGAR **y** > r0 de nacidos portadores de INERTE. Cada grupo necesita ≥ 5 cuerpos.

**NO EVALUABLE**, por cualquiera de estas causas:
- errores o ventana incompleta;
- bloqueados > 0;
- tope de libres en ≥ 5 corridas;
- libres extintos antes del corte en ≥ 5 semillas de CONTROL;
- trinquete;
- control fijo que se movió.

**Veredictos:**
- **FUNCIONA — CON CONTROL DEL ANFITRIÓN, PORTAR ES BUEN NEGOCIO:** PC, P1 y P2.
- **HAY ALGO MODESTO:** 1 o 2 de las tres.
- **NO:** ninguna.

El bloque se declara con serie y réplica iguales; si no, vale el menor. Vocabulario: «portar paga», «el anfitrión regula al simbionte»; prohibido «organelo» como hecho.

## 7. Qué refuta
- **H-C:** PC cae en las dos ventanas.
- **"Portar paga":** P1 y P2 caen en las dos ventanas, o SIN_TRAGAR > CONTROL en area_post en ≥ 15/20 las dos veces.

## 8. Semillas NUEVAS (26001–26999; grep del 24-sep: sin uso como semilla)
- **Serie 26001–26020; réplica 26021–26040.** RESERVADAS, sin correr.
- Práctica:
  - 26990, humo;
  - 26991–26992, calibración;
  - 26993–26994, prueba del Pool (coordinador);
  - 26994, arnés.

## 9. Siguiente escalón, escrito y no construido: TRANSFERENCIA AL NÚCLEO
- Un tercer gen del bicho, `nuc` ∈ [0, 1].
- En cada parto de un padre portador, con probabilidad `nuc` el hijo recibe una COPIA del término de canal del simbionte en su propio genoma nuclear: un vector de 4 números que suma a Vb sin costo de alojar, que se hereda y muta como un gen y que no se pierde con el simbionte.
- Pregunta: ¿la función migra al núcleo y el simbionte se vuelve prescindible? Es la firma de la reducción del genoma mitocondrial.
- Control: NUC_BARAJADO, donde la copia nuclear sale de un libre al azar.
- Va después de este paquete, si PC o P2 pasan.
