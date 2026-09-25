# PREREGISTRO — CÓDIGO GENÉTICO v0: ¿una cinta que se lee, se copia y regula su propia copia es más EVOLUCIONABLE que las perillas? (24-sep-2026, Opus del equipo organelos)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/organelos/codigo/`. Todo es nuevo. No se tocó nada existente.
**Escrito a las ~20:00, con la ventana EXPLORATORIA corriendo y ANTES de ver cualquiera de sus números** (§9 dice qué se vio y cuándo).
La serie y la réplica quedan RESERVADAS para el coordinador (Pool).

## 0. Instrumento (sha a 16; los recalcula `corre_codigo.SHAS()`)
- `motor_codigo.py` dd0051a348f93c6e. Lo CONSTRUYE `construye_codigo.py` (258b14b05160c8e3) por 25 anclas desde
  `organelos/gramatica/motor_gramatica.py` (6b65dc5e32093424).
- `codigo_def.py` 1096202c8afaa3d1: la cinta, el lector y el copiador.
- `carros/FAMB_GRAM_ECO.py` 2cee0a8510c997b9 y `gramatica_def.py` c58086e103d030d9: copias byte a byte de las de la gramática (arnés I0).
- Runner: `corre_codigo.py`. Versiones: c79e161c4a027acf en el humo 2 y en la exploratoria; **6aca7526849d67b9** después de ERR-141, que es la de la SERIE. El arnés se re-corrió con él y con I5 (reanudar desde el checkpoint después del cambio): 26/26.
- **Arnés `identidad_codigo.py`: 26/26** (25/25 antes de agregar I5) (`identidad_codigo_salida.txt`, `datos/identidad_codigo.json`).

## 1. Pregunta
Pregunta del director: el problema es el código genético. Hoy el genoma es un VECTOR (una perilla por rasgo), no hay lector ni desarrollo
y nada en el genoma dice dónde variar.
**Pregunta v0, pequeña y que puede fallar.** Todos arrancan desde lo mismo, lo más evolucionado (FIJO:filtra0), y viven en el mismo mundo
w30. El mundo CAMBIA: A (comida) y B (veneno) intercambian su valor. ¿El linaje con CÓDIGO recupera la reproducción más rápido y vive solo
más lejos en el mundo nuevo que el linaje de PERILLAS de hoy?
- Nombre honesto si sale bien: «**la cinta con copia regulada es más evolucionable que las perillas ante UN cambio del mundo**».
- Vocabulario prohibido: «código de la vida», «evoluciona sola», «inventa».

## 2. El código v0 (`codigo_def.py`)
- **La cinta** es una cadena de instrucciones de 9 operaciones:
  - `SUM j d`: una perilla, efecto directo.
  - `EJE k d`: uno de 3 ejes; mueve 4 rasgos a la vez (pleiotropía): aprender (eta, eta_s, paso, ema), cautela (alpha, aversion,
    −hambre_boca, memoria_rechazo) y vida lenta (dote, rep_umbral, rep_X, tau_e).
  - `ORG c q w m`: un slot del órgano de transmisión de la gramática.
  - `REP n … FIN`: repetición.
  - `DEF m … FIN` y `LLAMA m`: el gen MAESTRO; cambiar el DEF cambia todas sus llamadas.
  - `TASA r`: la tasa de error de copia del tramo que sigue, en niveles 0, 0.002, 0.01, 0.04 y 0.1.
  - `SOS u f`: si la fracción de mordidas MALAS (dS < 0) entre las últimas 20 del PADRE es ≥ U, toda la copia usa la tasa × F.
- **El lector** (al nacer) interpreta la cinta y produce las 18 perillas de `motor_gramatica` (en log, con paso 0.15 = la σ de hoy,
  relativas a G0, con los rangos de hoy) y el órgano (hasta 4 slots).
  - Es indirecto: una instrucción toca varios rasgos (EJE), hay repetición y llamada, y duplicar un tramo duplica una estructura
    (arnés P4).
- **El copiador** (en el parto y en el fundador del vivero que sale del banco) copia la cinta SIN interpretarla. Lee de ella la tasa por
  tramo y la regla SOS (von Neumann: la cinta describe también al copiador).
  - Tipos de error: cambio 0.55 (un argumento ±1 o a otro valor; en el 30 % de los casos, la instrucción entera al azar), borrado 0.20,
    inserción 0.15, duplicación en tándem de 1 a 4 instrucciones 0.10. Tope de 200 instrucciones.
  - Usa un rng propio por parto, `[seed, linaje, 23, k]` (arnés I2b: no toca el mundo).
  - «Lee lo vivido»: el cuerpo lleva el registro físico de sus últimas 20 mordidas (del mundo, no del carro).
- **Alfabeto del órgano CON «olvidar»**, en los dos brazos (CÓDIGO y PERILLAS). En la gramática se quitó por inerte en un mundo quieto;
  este mundo cambia. Decidido antes de correr nada.

## 3. Desde lo más evolucionado: la cinta inicial y la identidad
- `CINTA0 = compila()` tiene 30 instrucciones:
  `TASA(1) SOS(2,2) | TASA(3) DEF(0) EJE(0,0) EJE(1,0) EJE(2,0) FIN LLAMA(0) SUM(0..17, 0) REP(1) ORG(1,3,0,0) FIN`.
  - Zona del copiador: tasa 0.002. Zona del cuerpo: 0.04 × 28 ≈ **1.12 errores por copia**, parecido a PERILLAS: 18 × 0.05 = 0.9
    numéricos más ≈ 0.24 de la gramática.
  - SOS(2,2) = umbral 0.3 y factor ×3. **Calibración declarada:** el umbral se eligió con la corrida de identidad I2 (mundo viejo, sin
    errores, T 6000). La fracción de mordidas malas del padre al parir fue: media 0.087, p90 0.20, p99 0.35. Con 0.3 la SOS casi no se
    prende en el mundo viejo. No se miró ningún brazo ni el mundo nuevo para elegirlo.
- **Identidad (la pedida, I2):** la cinta inicial desarrollada, con copia SIN errores, da BIT A BIT la misma corrida (salida entera) que
  `motor_gramatica` con la gramática FIJA en filtra0, sin mutación numérica y sin sombras (T 6000, 314 desarrollos).
  - I2b: con el copiador PRENDIDO en todos los partos pero la cinta en TASA 0, también es idéntica.
  - I1: sin código y sin cambio, `motor_codigo` == `motor_gramatica` bit a bit (PERILLAS con sombras; silenciosos con AZAR).
  - I3: antes del cambio, idéntica a la corrida sin cambio; después, A da dS < 0 y B dS > 0.
  - P0–P12: cada instrucción cambia algo medible. La SOS multiplica la tasa ×3.0 sólo con frac_mal ≥ 0.3, no con el brazo sin SOS y no
    en fundadores. Los 4 tipos de error salen en la proporción declarada.

## 4. El mundo que cambia
- `eco['cambio'] = (t_cambio, 'A', 'B')`: en ese paso se intercambia `VAL_VIVO` de A y B, **el cambio mínimo que el motor permite**.
  Nada más cambia: patrones, llegadas, costos y letras son iguales.
- Lo que queda viejo: la tabla heredada (filtra0 dice A = +1, B = −3), lo aprendido y las perillas.
- La etiqueta de causa de muerte («veneno» si mordió B) queda mal rotulada después del cambio. Es telemetría y no se usa.
- **ERR-140 (tras el humo 1, antes de cualquier dato de semillas de serie ni de la exploratoria).**
  - El diseño inicial ponía el cambio DESPUÉS del corte y medía la recuperación por el tamaño.
  - El humo 1 (27001, T 8000, corte 3000) extinguió todo antes del cambio: el vivero corto no deja una población que viva sola. Con
    ~15 cuerpos solos no hay generaciones para que la variación haga nada antes de extinguirse, así que la pregunta mediría el piso.
  - **Cambio:** el mundo cambia DENTRO del vivero (t_cambio < t_corte). La recuperación se mide en NACIMIENTOS reales por ventana de 2000
    pasos, porque el tamaño en el vivero lo sostiene el reponedor. La prueba final es vivir SOLO en el mundo nuevo después del corte.
  - Riesgo que trae: en el vivero, el fundador repuesto nace sin tabla heredada (limpio) y aprende el mundo nuevo desde cero. Eso ayuda a
    todos los brazos por igual y puede tapar la diferencia (se declara; ver §7).

## 5. Brazos (w30: esc 30, 30 fundadores, quimiostato; banco 200; sin sombras)
| brazo | genoma | variación | donante |
|---|---|---|---|
| **CODIGO** | CINTA0 | copia con errores (TASA de la cinta) + SOS | padre |
| **PERILLAS** | vector de hoy desde filtra0 + G0 | numérica p 0.05, σ 0.15, 18 genes + gramática (campo 0.05, dup 0.02, del 0.02, tope 4) | padre |
| **CODIGO_SIN_SOS** | CINTA0 | copia con errores; la SOS no se lee | padre |
| **AZAR** | CINTA0 | como CODIGO | entrada al azar del banco (deriva) |
| **MUT0** | CINTA0 | ninguna | padre |

- Serie: **T 80 000, cambio en 15 000, corte en 40 000, margen 10 000.**
- Exploratoria: T 40 000, cambio en 10 000, corte en 25 000, margen 5 000.

## 6. Medidas y la letra (`corre_codigo.veredicto`)
- **t_rec:**
  - B_pre = nacimientos medios por ventana de 2000 pasos en las 3 ventanas antes del cambio.
  - Después del cambio se toma la ventana con el mínimo de nacimientos. t_rec = pasos desde el cambio hasta la primera ventana, a partir
    de esa, con ≥ 0.8 × B_pre.
  - Si nunca cayó por debajo, t_rec = 0. Si no vuelve antes de T − margen, se censura en T − margen − t_cambio + 1.
- **R0 final:** hijos medios de los nacidos en [corte, T − margen], viviendo SOLOS en el mundo nuevo (extinto o sin nacidos = 0).
- **Persistencia en T.**
- **Descriptivas:**
  - Robustez: entre los hijos con ≥ 1 error de copia, la fracción NEUTRA (fenotipo idéntico al del donante), la que CAMBIA y deja
    hijos, y la que CAMBIA y deja 0 hijos, frente a la tasa con hijos de los copiados sin error.
  - Largo de la cinta.
  - Fracción de partos con la SOS prendida antes del cambio y en los 5000 pasos después.
  - Mordidas por letra y signo.

| prueba | criterio (pareado por semilla) |
|---|---|
| **P1** | CODIGO t_rec < PERILLAS en ≥ 14/20 **y** persistencia(CODIGO) ≥ persistencia(PERILLAS) |
| **P2** | CODIGO R0 final > PERILLAS en ≥ 14/20 |
| **P3** (la SOS sirve) | CODIGO R0 final > SIN_SOS en ≥ 13/20 **y** la SOS SE PRENDE: frac SOS en los 5000 pasos tras el cambio ≥ 2 × la de antes, en ≥ 15/20 semillas de CODIGO |
| **Guardia de selección** | CODIGO R0 final > AZAR en ≥ 14/20 |
| **Guardia de variación** | CODIGO R0 final > MUT0 en ≥ 14/20 |

**Veredicto, en orden:**
1. **NO EVALUABLE**: ventana incompleta, corridas abortadas o tope de cuerpos.
2. **FUNCIONA + la SOS aporta**: (P1 o P2) y las dos guardias y P3.
3. **FUNCIONA**: (P1 o P2) y las dos guardias.
4. **HAY ALGO MODESTO**, si se da una de estas:
   - (P1 o P2) con una guardia caída: el código gana, pero no se atribuye a la selección o a la variación;
   - P3 sola;
   - las dos guardias sin P1 ni P2: el código evoluciona, pero no le gana a las perillas.
5. **NO**: todo lo demás.

El bloque exige serie + réplica con el mismo veredicto.

## 7. Predicciones firmadas (antes de ver la exploratoria)
| medida | predicción (rango) |
|---|---|
| persistencia en T, cada brazo | 6–16/20; MUT0 la más baja o empatada |
| t_rec mediana | 2 000–16 000 pasos en todos los brazos; diferencia CODIGO − PERILLAS dentro de ±4 000 |
| R0 final mediana | 0.4–0.95 en todos los brazos |
| la SOS se prende tras el cambio (≥ 2×) | sí, en ≥ 15/20 (P = 0.70) |
| robustez CODIGO: fracción neutra | 0.45–0.70 |
| largo de la cinta en T (mediana) | 29–36 |

**Probabilidad de cada veredicto:**
| veredicto | P |
|---|---|
| NO | **0.55** |
| HAY ALGO MODESTO | 0.28 |
| FUNCIONA (cualquiera) | 0.10 |
| NO EVALUABLE | 0.07 |

- P1: 0.15 · P2: 0.20 · P3 completa: 0.15 · guardia de variación: 0.30 · guardia de selección: 0.35.
- **Por qué NO es lo más probable:**
  - La diferencia está en la FORMA del genoma, y la carga de mutación se igualó (≈ 1.1 errores por copia en los dos).
  - En el vivero el fundador limpio reaprende el mundo nuevo sin genes (§4, riesgo).
  - En w30 la selección sólo ve efectos fuertes (N_e 10–50, DIAGNOSTICO_DARWIN).
  - Lo que más ayudaría ante el cambio es apagar o invertir la tabla heredada. Eso lo pueden hacer los dos brazos: en PERILLAS por
    mutación de campo y en CODIGO por mutación del ORG.

## 8. Semillas (27000–27999, asignadas por el coordinador; grep del 24-sep en `experimentos/**/*.py`: sin usos como semilla. Aparece un «27006» en `subida_n9`, pero son pasos, no una semilla)
| uso | semillas |
|---|---|
| humos | 27001 |
| identidad | 27002 |
| arnés por pieza | 27003 |
| **serie** | **27011–27030** |
| **réplica** | **27031–27050** |
| práctica / exploratoria | 27901–27903 (y 27904–27999 libres para práctica) |

## 8b. ERR-141 (DESPUÉS de ver la exploratoria; antes de cualquier semilla de serie o réplica)
El texto de §0 a §8 quedó con sha 3a7fdec10124627f a las 19:58, antes del primer resultado de la exploratoria.
- **(a) Error de instrumento en t_rec.** El mínimo de nacimientos se buscaba hasta T − margen. Después del corte el vivero deja de reponer,
  la población se desploma en TODOS los brazos y ese mínimo (0 o 1 nacimientos) se comía la medida: t_rec quedaba censurado 15/15.
  - Eso pasó incluso en CODIGO 27903, que en el vivero volvió a 40–63 nacimientos por ventana, por encima de B_pre = 45.
  - **Arreglo:** la recuperación se mide DENTRO del vivero, en ventanas de [t_cambio, t_corte). El censurado pasa a ser
    t_corte − t_cambio + 1.
  - Para los JSON ya escritos, `relee_trec()` recalcula desde `ventanas_r0`, que están alineadas cuando t_cambio es múltiplo de 2000.
- **(b) Brazo DESCRIPTIVO nuevo, QUIETO:** CODIGO en el mundo que NO cambia, medido en el mismo t_cambio nominal. Queda fuera de la letra.
  - Motivo: en la exploratoria casi todo se extingue después del corte, en todos los brazos. Sin QUIETO no se sabe cuánto de eso es el
    cambio del mundo y cuánto es el corte.
  - Suma 1/5 al costo.
- **Lo que NO cambia:** la letra (P1, P2, P3, las guardias y sus umbrales), las predicciones de §7, TL de la serie, las semillas y los
  brazos de la letra.

## 9. Lo que se vio antes de la serie (se completa en `INFORME.md`)
- **Humo 1** (27001, cambio después del corte) → ERR-140.
- **Humo 2** (27001, T 8000, cambio 3000, corte 5000): escribe los 5 JSON y el `HUMO.json`. Números sin valor. En CODIGO la SOS pasó de
  0.049 a 0.125 de los partos tras el cambio.
- **EXPLORATORIA** 27901–27903 (T 40 000, cambio 10 000, corte 25 000). Números EXPLORATORIOS: no cambian ni la letra ni las
  predicciones. Lectura completa en `datos/EXPLORATORIO_s27901-27903_T40000/LECTURA_EXPLORATORIA.txt`.
  - Cómo se corrió: 5 brazos en 3 bloques de un proceso (~85 s por corrida), más QUIETO en un proceso (~141 s por corrida).
  - **El cambio golpea igual a todos.** Los nacimientos caen de ~50 a 9–17 por ventana y dentro del vivero no vuelven a 0.8 × B_pre
    (t_rec censurado 14/15). La excepción es CODIGO 27903: 40–63 por ventana desde t ≈ 16 000.
  - **Solo, después del corte, todo muere:** persisten 2/15 con 1 cuerpo (PERILLAS 27903 y AZAR 27901). R0 final mediano: CODIGO 0.22,
    PERILLAS 0.23, SIN_SOS 0.15, AZAR 0.00, MUT0 0.24.
  - **QUIETO (sin cambio) persiste 3/3**, con R0 final 0.74–0.79 y 7 a 13 cuerpos. Lo que mata es el cambio del mundo, no el corte.
  - **La SOS SE PRENDE** en 3/3: la fracción de partos con SOS pasó de 0.015–0.037 a 0.20–0.35 tras el cambio y siguió en 0.17–0.42.
  - Robustez de CODIGO (mediana): de los hijos con ≥ 1 error, 0.50 salen neutros (el mismo fenotipo), 0.13 cambian y dejan hijos, 0.35
    cambian y no dejan. Con 0 errores dejan hijos 0.36 de los hijos.
  - Largo de la cinta: 30–33.5 de media en los partos tardíos; máximo 40.
  - La letra, en 3 semillas y sin valor de veredicto, dice NO. P1 1/3 · P2 0/3 · P3 2/3 con la SOS encendida 3/3 · guardia de selección
    3/3 · guardia de variación 2/3.

## 10. Costo y comandos (el coordinador)
- `python experimentos/organelos/codigo/corre_codigo.py --serie --ventana serie --pool 3` y luego `--ventana replica`.
- Estimación en `INFORME.md`, medida en la exploratoria.
