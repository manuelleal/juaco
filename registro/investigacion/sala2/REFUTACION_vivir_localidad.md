# REFUTACIÓN — sala 2, diseño "vivir" (`DISENO_vivir.md`), lente LOCALIDAD Y CONSISTENCIA

**Refutador de la sala 2, 18 sep 2026, ~10:20.** Misión primero: llegar a la AGI por este camino — un organismo mínimo con reglas
locales (sin backprop en el runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada.
Primero la frontera; segundo, que viva. Este archivo es una REFUTACIÓN: no construye nada, no propone tronco. La decisión es del
coordinador; la de tronco, del director.

**Reglas cumplidas.** No edité ningún archivo del repo; éste es el único archivo que creé (en `registro/investigacion/sala2/`). No
ejecuté `Pool` (hay uno vivo). Corrí exactamente **UNA corrida de un proceso, T = 50 000** (§3, declarada con sus números; script y
JSON en mi scratchpad, no en `datos/`): una copia de `organismo/organismo_v14.py` (feefc88b1fd8d434) con un registro de sólo
lectura de `E` y `deaths` por paso. Sin commit. `organismo/` primero en `sys.path`. Leído: `DISENO_vivir.md` entero,
`organismo/organismo_v14.py` entero, `experimentos/nivel11_mundo_vivo/organismo_vivo_rep.py` entero, las anclas de `organismo_vivo_rep2.py`,
`EQUIPO.md`, `CRITERIO_TRONCO_v2.md`, el registro desde ERR-37 hasta la decisión del director (09:55), `PREREGISTRO_reproduccion_2.md` §2,
`DIAG_mundo.md` §3, `DIAG_dinamica.md` (trampa de la herencia de miedo), `dia1_exploracion/poblacion2.py`, `creacion_A/identidad_v15e.py`,
y los JSON registrados `datos/examen_v14_20260918_054720.json`, `datos/examen_v14_20260918_045742.json`,
`datos/vivo_rep2_s261-280_20260918_094126.json`, `datos/vivo_rep2_s281-300_20260918_094323.json`.

---

## 0. Veredicto en una línea

**REFUTADO.** El diseño pasa la lente de localidad (sin backprop, sin aptitud global, estado nuevo mínimo, anclas únicas y
apagado plausible bit a bit), pero **está calibrado con números de otro mundo**: en el anillo del tronco (el mundo de V0) un cuerpo con
la memoria completa consigue ~0.05–0.08 ventanas de 500 pasos por vida (registro: 124–159 muertes por 100 000 en E1; mi corrida: 5
ventanas en 63 vidas, **ninguna en la primera vida**), luego R₀ ≪ 1, el fundador muere sin hijos y **P-V0 cae por el mundo, no por la
herencia** — y la cláusula 4.6.1 cierra la línea entera con ese dato. Además dos casos del arnés (I5, I6) fallan por construcción y
los rng de los hijos colisionan entre semillas vecinas.

---

## 1. Lo que la lente de localidad NO refuta (dicho para no inflar)

| pregunta del encargo | respuesta | evidencia |
|---|---|---|
| ¿regla local sin backprop ni supervisor global? | **Sí.** Nacimiento = copia pagada (`E-=dote`) al cumplir una ventana local; muerte = `break` local; mutación del gen con el rng del hijo; el planificador sólo ordena al azar y aplica el modo de herencia. No hay función de aptitud, ni torneo, ni gradiente | §2.3 del diseño; `meta['stir']=min(id)` es la única "vista global" y es una regla del mundo (quién ejecuta el olvido de objetos), no del organismo |
| ¿apagado ≡ v14.1? | **Plausible y exigible.** Una función con `yield` es generador entera; el `return dict` pasa a `StopIteration.value`; ninguna operación cambia de orden. Las 12 anclas existen y aparecen **exactamente una vez** en `organismo_v14.py` (comprobado con `grep -c`: A2–A11 → 1/1 cada una) y la de CUELLO_MIN en `organismo_vivo_rep.py` línea 185 → 1 | `organismo_v14.py` líneas 38–47, 50, 65, 145, 155–160, 164; `organismo_vivo_rep.py` 185, 255, 289 |
| ¿estado nuevo mínimo o red disfrazada? | **Mínimo.** Por cuerpo: `madre` (90 enteros), 2 genes, un contador; por nacimiento una copia de la memoria de v14.1 (~1 200 flotantes + `ncod`). No entra ninguna capa, ningún peso nuevo con aprendizaje | §2.4 |
| ¿contradice alias / reversión / identificabilidad / ERR-37/38/40? | ERR-37 (A₁₂ sin parear para integrales) y ERR-38 (campo a campo) están **aplicados**; alias reportados al arrancar; reversión (V3) desplaza `invertir_en` al nacer. **Lo que sí contradice son los registros de `deaths` y `vidas`** (§2) | §4 del diseño |

Lo que sigue es lo que sí lo refuta.

---

## 2. Motivos (con evidencia)

### M1 — El mundo de V0 está calibrado con la mortalidad de OTRO mundo; con la registrada, el fundador no se reproduce

El diseño toma sus cifras de mortalidad del mundo vivo (`costo = 0.001`, dos necesidades: "64–100 muertes por 100 000", §0.2 y B4)
y de su corrida a `nobj = 12`. Pero V0 corre en el **anillo del tronco** (`organismo_v16v`, `costo = 0.002`, comida/veneno), cuya
mortalidad **ya está registrada** y el diseño no la cita:

| fuente (registro) | muertes por 100 000 (mediana; n = 6 semillas × 9 escenarios) | vida media ≈ 100 000 / muertes |
|---|---|---|
| `datos/examen_v14_20260918_054720.json` (v14.1, examen), E1 | **129.5** [124–153] | ~770 pasos |
| ídem, E2 / CTRL / E2L | 132 / 146.5 / 141.5 | ~700 |
| `datos/examen_v14_20260918_045742.json`, E1 | 140.5 [127–159] | ~710 |

Es decir: **un cuerpo con la memoria completa y el regalo de 0.6 muere cada ~700 pasos en el mundo del tronco** — más que en el
mundo vivo (600–827 de vida mediana con el mismo regalo, `vivo_rep2` 261–300). Con `costo = 0.002`, una ventana de 500 pasos con
`E ≥ 1.0` exige ≥ 2 comidas bien colocadas (de 1.5 a 1.0 hay 250 pasos) dentro de una vida de ~700. Mi única corrida lo cuantifica (§3):
**5 ventanas en 63 vidas (0.079 por vida; 0.048 sin contar las financiadas por el regalo); la primera vida (E = 1.0, memoria en blanco,
1 355 pasos) no tiene ninguna ventana.** En el diseño el fundador muere en su primera muerte: en la semilla 1, `fundador_sin_hijos`.

Consecuencia sobre el preregistro: P-V0 exige "razón de medianas ≥ 5" y A₁₂ ≥ 0.90 (HEREDA > BLANCO en `t_ext`). Con R₀ (hijos por
vida) ≈ 0.05–0.08 el linaje HEREDA es, en casi todas las semillas, el fundador solo (`t_ext` ≈ vida del fundador), y BLANCO igual: A₁₂
≈ 0.5 y razón ≈ 1. **P-V0 cae por la física del mundo, no por la herencia, y la cláusula 4.6.1 cierra V1–V3.** La guardia del diseño
("el mundo no sostiene nada … los contrastes deciden") no protege a V0 porque su criterio de refutación (A₁₂ < 0.70) se dispara igual
cuando nadie nace. (n = 1 en mi corrida; pero las 12 semillas × 9 escenarios del examen registrado dicen lo mismo sobre la
mortalidad, y la vida mediana registrada del renacido en el mundo vivo, 600–827, es una cota superior de la del hijo con `dote = 0.5`.)

### M2 — P-V4 contradice las `vidas` registradas del bloque 2

`x_viab = 2 000` y "`mort_inf` HEREDA ≤ 0.6" exigen que ≥ 40 % de los hijos vivan ≥ 2 000 pasos. Registrado (`vivo_rep2`, 40 semillas,
cuerpos con memoria completa, regalo 0.6/0.6, posición nueva al azar):

| brazo | vida mediana (mediana de semillas) | vida máxima (mediana) | ventanas financiadas por el regalo (`frac_regalo`) |
|---|---|---|---|
| VIVO | 600 / 600 | 6 133 / 5 096 | 0.44 / 0.42 |
| CUELLO_MIN (el cuerpo de V1) | 827 / 791 | 7 801 / 7 460 | 0.38 / 0.39 |

Con mediana ~800 y máxima ~7 500 sobre ~70 vidas por corrida, la fracción de vidas ≥ 2 000 es de un orden de 0.1–0.2 (en mi corrida
del tronco: 0.081). El hijo del diseño recibe **menos** que el renacido (0.5 contra 0.6) y no cambia de sitio. `mort_inf` ≈ 0.85–0.9 es lo
esperable; el diseño lo pone como umbral de refutación ("≥ 0.8: los hijos nacen para morir") de una predicción que los datos ya
registrados hacen casi segura. Y con `frac_regalo` ≈ 0.4, **el 40 % de las ventanas de CUELLO_MIN las paga el renacer**: quitando el
regalo, CUELLO_MIN queda en ≈ 0.6 ventanas por vida (68 × 0.6 / 66 vidas) → **R₀ < 1 también en el mundo vivo**, y un proceso de
ramificación con media < 1 se extingue con probabilidad 1: tamaño esperado del linaje ≈ 1/(1 − 0.6) = 2.5 cuerpos ≈ 2 000 pasos ≈ 2.5 ×
una vida, no ≥ 5 × (P-V1). El diseño conocía `desc_regalo` (lo cita en B1) y no lo restó al calibrar.

### M3 — El arnés de identidad tiene dos casos que fallan por construcción y una colisión de rng

- **I5** ("`pob=1`, `costo=0`, `rep_X=T+1`: nadie muere, nadie nace → idéntico a `pob=0`"): con `costo = 0` **sí se muere**: el veneno
  resta 0.4 (`E_VAL['veneno'] = −0.4`, `organismo_v14.py` línea 36) y la boca en blanco muerde con `pb = 0.84` (`Vb = 0.5`, línea 103).
  Tres venenos sin comida desde `E = 1.0` → `E ≤ 0` → en `pob=1` el cuerpo hace `break` (A9) y en `pob=0` renace: los dicts difieren
  aunque el planificador sea perfecto. Probabilidad ≥ 1/8 por semilla sólo en las tres primeras mordidas; con semillas 1–3, del
  orden de 1/3–1/2 de que I5 "falle" sin defecto alguno (o pase por suerte con un planificador roto).
- **I6** ("GEN_INERTE ≡ FIJO_05 salvo `genes`"): la mutación de los genes se hace "con el rng del hijo (`seed + 800000 + k`)" y ese
  **mismo** `rng_h` se pasa como `_rng` del cuerpo (`nuevo(k, t+1, est, ev['pos'], rng_h)`, §2.3). En GENES/GEN_INERTE el flujo del hijo
  llega desplazado por los sorteos de la mutación; en FIJO_05 (`genes=0`) no. El primer `rng.normal(0,.3,2)` del movimiento ya difiere
  → las claves de conducta **no pueden** ser idénticas. I6 falla por construcción.
- **Colisión de semillas:** hijo k de la semilla s usa `s + 800000 + k`; hijo k−1 de la semilla s+1 usa el mismo entero (V0: 1301–1320
  son consecutivas). Dos semillas "independientes" comparten los flujos de sus hijos: pseudo-réplica entre semillas, justo lo que la
  regla "toda estadística es entre semillas" quiere evitar.
- **Menor, pero mata la corrida:** el hijo hereda `q=lambda t:min(t//(T//4),3)` (línea 75) con `T = T − t0`; si nace con `T − t0 < 4`,
  `T//4 = 0` → `ZeroDivisionError` en `vis[kk][q(t)]` si pisa un objeto (nace donde está el padre). Raro, pero pierde el JSON entero
  (regla 14 / ERR-42). Y los cuartos `q(t)` del hijo son relativos a su nacimiento: la "tabla 2 × 4 del cuerpo más viejo" no es
  comparable con la del tronco sin decirlo.

### M4 — "Compiten por la misma comida" no es la física de `spawn()`; el acoplamiento real es la trampa 3 bajo una decisión no declarada

`del objs[pos]; spawn()` (línea 112) repone el objeto **en el mismo paso**: el anillo tiene siempre `nobj = 4` objetos, coma quien coma.
N cuerpos no se quitan comida: la densidad de objetos por casilla es 0.1 con 1 o con 16 cuerpos, y el total de comida que sale del mundo
**crece con N**. Lo que sí acopla a los cuerpos es (i) dos cuerpos apuntando al mismo objeto y (ii) la **trampa 3**: lo rechazado se
queda, cada comida comida se repone con 50 % de veneno, y el único desagüe es el olvido a 0.003 por paso, que A8 reserva a **un solo
cuerpo**. Resultado: con N cuerpos el anillo se atasca de veneno N veces más rápido y el desagüe no escala → la capacidad de carga la
fija A8, una decisión de instrumento que el diseño justifica como "artefacto" en una línea y no preregistra como física (con olvido por
objeto —la alternativa igual de local— la capacidad sería otra). `frac_veneno` se reporta "sin umbral"; debería ser la covariable
preregistrada de la selección, porque **es** la selección.

### M5 — "Criterio de emergencia del punto 14, literal" es un error de categoría con `hereda='todo'`

Con copia completa (A7 copia `KW, activa, Wp, Wn, Wps, Wns, ncod, …`), "un linaje que vive más que cualquier cuerpo" es lo que hace un
archivo guardado respecto de un proceso: **programado por construcción**, no ausente en el individuo y presente en el grupo. BLANCO
prueba "reproducirse no basta", cierto; pero HEREDA > BLANCO re-mide en población lo que la Etapa 4 (bloque H1) ya midió en un cuerpo
(heredar el valor ahorra el 80 % del veneno inicial, 6.5 contra 30.5, 20/20). El diseño lo sabe (B5: "predicciones de población, no
resultados") y aun así lo vende como salida de la frontera. Lo genuinamente nuevo y medible del diseño es P-V3 (vector contra token) y
P-V5 (frecuencia alélica), y **ambos dependen de que nazcan hijos** (M1–M2).

### M6 — Inconsistencias de instrumento con lo ya congelado y con el criterio v2

- `organismo_vivo_pob` se ancla en `organismo_vivo_rep.py` (aa823d56c2d4213c), pero las cifras con que se calibra (`vidas`, `desc_regalo`,
  `r`) son de `organismo_vivo_rep2.py` (96feb4918dc5d694), y `CRITERIO_TRONCO_v2.md` T-A juzga por `r = descendientes − muertes` del
  bloque 2. El instrumento propuesto no lleva esas claves → no se puede juzgar con el criterio vigente sin re-anclar.
- P-V7 se evalúa "sólo entre semillas con linaje vivo a 50 000" con umbral "≥ 12/15": el 15 no sale de ningún dato; con M1–M2 el
  subconjunto puede ser de 0–3 semillas (regla 10: subconjunto preregistrado, sí; potencia, ninguna).
- ESCALAR (`Wp = 0`, `Wn = media > 0` en todas las celdas activas) es un cuerpo que teme todo: no es "misma cantidad de memoria" sino un
  hijo que no come; "ESCALAR ≤ 2 × BLANCO" se cumple trivialmente. BARAJA, en cambio, con `ncod` heredado y `Wp/Wn` permutados, rutea
  códigos familiares a valores **equivocados** (no ausentes): mide "memoria mal puesta" contra "ninguna" — sirve, pero hay que decirlo.
- B6 ("+34 % de muertes en N1") está en `CLAUDE.md` día 4: correcto.

---

## 3. La única corrida (declarada): `organismo_v14` seed 1, T = 50 000, un proceso, todo por defecto

Copia `organismo_v14_Elog.py` (scratchpad de esta sesión; sha del origen comprobado feefc88b1fd8d434; tres anclas únicas: `deaths=0; log=[]`,
`if log_cada and …`, `return dict(sobre=sobre,`; sólo se agregan `_EL.append(E); _DL.append(deaths)` al final de cada paso y dos claves
de salida). 2.0 s. Resultado (`corrida_unica_v14_s1_T50000.json`):

```
deaths 62  vidas_n 62  vida_mediana 300  vida_max 3296  vida_primera 1355  vida_final 64
frac_vidas>=2000 0.081  frac_vidas>=1000 0.29  frac_pasos_E>=1 0.36
ventanas_500 5  en la primera vida 0  vidas_con_ventana 5 de 63  ventanas_por_vida 0.079
ventanas que empiezan dentro de los 300 pasos del regalo (0.6/0.002) 2  -> sin regalo 0.048 por vida
W {A 1.0, B -2.92, C -0.5, D -2.5}  celdas 30  splits 0
```

n = 1, semilla vista: **no es evidencia**; sirve para no preregistrar un mundo en el que nadie nace. Es coherente con las 12 × 9 corridas
del examen registrado (124–159 muertes por 100 000).

---

## 4. Qué lo salvaría (en orden; nada de esto se hace mirando datos del bloque)

1. **Calibrar el mundo del linaje ANTES de preregistrar, con lo ya registrado y un humo de un proceso declarado:** medir en el mundo
   del tronco y en el vivo las ventanas por vida **sin regalo** (mi corrida + `desc_regalo`/`vidas` de `vivo_rep2`) y fijar `rep_X`,
   `dote`, `costo` o `nobj` de modo que HEREDA tenga R₀ ≈ 1 y BLANCO R₀ < 1 **por predicción**, con ERR numerado y semillas nuevas. Si
   ningún ajuste de una sola perilla lo consigue, el mundo del tronco no sostiene linajes mortales y se dice así, sin V0.
2. **Arnés:** I5 con semillas en las que `pob=0, costo=0` dé `deaths = 0` (comprobado antes), o comparar el estado del fundador hasta su
   primera muerte; I6 con un rng **propio** para la mutación (`seed + 700000 + k`) que no toque el del cuerpo; semillas de hijo sin
   colisión (`SeedSequence(seed).spawn()` o `seed·1000 + k`); `q` con `max(1, T//4)` o prohibir nacimientos con `T − t0 < 4`, declarado.
3. **Declarar la física del acoplamiento:** reposición instantánea = sin competencia por comida; la densodependencia es la trampa 3 bajo
   olvido de un solo cuerpo. Preregistrar `frac_veneno(N)` como covariable y, si se quiere competencia de verdad, un mundo con
   reposición **por tasa** (un cambio, ERR numerado) en vez de por hueco.
4. **Reescribir la emergencia como algo que ningún cuerpo puede tener:** p. ej. "la tabla 2 × 4 del cuerpo más viejo a T está completa
   (signos en A y B) cuando ningún cuerpo de UN_CUERPO la completa antes de morir en ≥ 18/20" — eso sí es presente en el linaje y ausente
   en el individuo. La persistencia por copia no lo es.
5. **Anclar `organismo_vivo_pob` en `rep2`** para conservar `r`, `vidas`, `desc_regalo` y ser juzgable por `CRITERIO_TRONCO_v2.md` T-A.
6. **Umbrales de P-V4 y P-V7 derivados de las `vidas` registradas** (fracción de vidas ≥ x_viab en 261–300), no de "cuatro ventanas de drenaje".

---

## 5. Lo que este archivo no dice

No dice que la herencia no sirva (H1 de la Etapa 4 dice que sí, en un cuerpo). No dice que el planificador no sea local (lo es). No
dice que el diseño no pueda correr: dice que, tal como está escrito, **V0 se cerraría con el dato equivocado** y el preregistro lo
declararía "línea cerrada" cuando lo que falló es la calibración del mundo — el error de ERR-40 (medida que no mide lo que dice) en
versión de mundo. Refutado; salvable con §4.
