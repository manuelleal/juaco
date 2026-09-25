# EXPLORATORIO, no es dato

# HALLAZGOS del explorador Fable — mundos que cambian para el CÓDIGO GENÉTICO v0 (24-sep-2026, 20:35–21:35)

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas); el método manda sobre el cómo.

**Veredicto en una línea: HAY ALGO MODESTO, y no es lo que buscábamos.** En 15 mundos (3–6 semillas cada uno, TL corto) el CÓDIGO
vive solo mejor que PERILLAS después del corte (más nacimientos sin reponedor: razón 1.2–2.0 según el mundo), **pero esa ventaja ya
está en el mundo QUIETO (razón 1.54, 6 semillas)**: es una diferencia de BASE entre los dos genomas, no evolucionabilidad ante el
cambio. Ningún mundo hizo que la ventaja del CÓDIGO creciera claramente por encima de la base, salvo una pista débil en `zona_mitad`
(razón 2.0, nadie persiste). Dos cosas sí quedan claras con 6 semillas: **(1) la ventaja de base es de la VARIACIÓN de la cinta, no
del lector** (MUT0, la cinta sin errores, rinde como PERILLAS: 443 vs 492 nacimientos solos en `quieto`, 195 vs 201 en `onda8k`;
CODIGO 757 y 322); **(2) la SOS estorba**: CODIGO_SIN_SOS > CODIGO en 4/6 semillas en los tres mundos donde se midió (`onda8k` 713 vs 322
nacimientos solos; `medio_veneno` persiste 5/6 vs 1/6; `suave` 712 vs 459).

## 0. Qué construí (`experimentos/organelos/codigo/exploracion_fable/`; nada fuera de aquí se tocó; sin git)
| archivo | qué es |
|---|---|
| `construye_fable.py` → `motor_fable.py` | copia de `motor_codigo.py` por 7 anclas de texto. Con `eco['cambio']` = tupla es `motor_codigo` **bit a bit**; con un dict (spec) la tabla letra → (dE, dAg) se recalcula en cada paso (pura, sin rng; `zona` mira la posición). |
| `fable_mundos.py` | el catálogo (§1) y `efecto(spec, t, EF0, L)` → `(letra, pos) → (dE, dAg)`. `reina` es el único con estado (en la copia del spec de la corrida). |
| `identidad_fable.py` → `identidad_fable_salida.txt` | **8/8**: IF1 tupla == `motor_codigo` (CODIGO y PERILLAS, T 6000), IF2 spec `golpe` == tupla, IF3 gradual con dur 1 == golpe en t+1, IF4 tablas de gradual/alterna/zona. |
| `corre_fable.py` | reusa `corre_codigo.trabajo()` sin tocarlo (monkeypatch dentro del proceso: `CC.MC = motor_fable`, `CC.eco_de` agrega el spec). Un proceso por invocación, sin Pool. `--lee`, `--md`. |
| `lee_cintas.py` | órgano (gramática) y cinta de los vivos en T. |
| `PREDICCIONES_previas.md` | mis predicciones firmadas a las 20:50, antes de ver la tanda 1. |
| `datos/<mundo>_corto/*.json` | los crudos, mismo formato que la exploratoria de Opus + `mundo_fable`. `datos/TABLA_MD.txt` es la tabla (a) generada. |

**TL corto** (todo): T 36 000, cambio 8 000, corte 24 000, margen 4 000; w30, banco 200, sin sombras (= `corre_codigo`). **Semillas:** 28001–28003
en los 15 mundos; 28004–28006 en 7 confirmaciones. **Costo medido:** ~87 s por corrida con hasta 15 procesos a la vez (16 núcleos; el
agente de `ohno/` usaba 1). ≈ 135 corridas ≈ 3.3 h de CPU, ~55 min de reloj.

**Medidas por corrida** (de `ventanas_r0`): persistencia en T; **R0 final solo** (hijos medios de los nacidos en [corte, T − margen]; extinto = 0);
**nac solo** = nacimientos después del corte (cuánta vida hubo sin reponedor: la medida con menos ruido; R0 final se calcula sobre
10–50 cuerpos); nac post/pre; t_rec (ERR-141, censurado = 16 001); SOS antes → después.

**Aviso de tamaño:** con 3 semillas, «gana 3/3» pasa por azar 1/8; con 6, «5/6» pasa 0.11. Nada de aquí tiene valor de veredicto.

## 1. Tabla de mundos (a)
Celda por brazo: persisten/n · R0 final mediana · nac solo mediana · t_rec mediana (cens = censurado, 16 001). «Ganador» exige: CODIGO gana R0 final
en todas (n = 3) o en todas menos una (n = 6) las semillas, gana nac solo en ≥ la mitad y no pierde persistencia.

| mundo | parámetros (t0 = 8000) | semillas | CODIGO | PERILLAS | CODIGO_SIN_SOS | CODIGO > PERILLAS en R0 final | en nac solo | persist. dif | ganador |
|---|---|---|---|---|---|---|---|---|---|
| **quieto** (control: no cambia) | fijo, tabla {} | 28001–28006 (6) | 6/6 · R0 0.72 · nac solo 106 · t_rec 0 | 6/6 · R0 0.67 · nac solo 82 · t_rec 0 | — | 4/6 | 5/6 | +0 | empate (**la base**: CODIGO ya vive solo mejor) |
| golpe (el de Opus) | A↔B en t0 | 28001–28006 (6) | 1/6 · R0 0.12 · nac solo 20 · cens | 0/6 · R0 0.16 · nac solo 16 · cens | — | 4/6 | 3/6 | +1 | empate / ruido |
| gradual8k | lineal, dur 8000 | 28001–28003 (3) | 0/3 · R0 0.11 · nac solo 28 · cens | 0/3 · R0 0.21 · nac solo 38 · cens | — | 1/3 | 1/3 | +0 | empate / ruido |
| gradual16k | lineal, dur 16000 | 28001–28006 (6) | 1/6 · R0 0.40 · nac solo 37 · 14000 | 0/6 · R0 0.36 · nac solo 22 · cens | — | 4/6 | 4/6 | +1 | empate / ruido |
| escalera4 | 4 peldaños en 8000 | 28001–28003 (3) | 0/3 · R0 0.14 · nac solo 14 · cens | 0/3 · R0 0.21 · nac solo 27 · cens | — | 1/3 | 0/3 | +0 | PERILLAS |
| alterna2k | cuadrada, período 2000 | 28001–28003 (3) | 0/3 · R0 0.21 · nac solo 13 · cens | 0/3 · R0 0.06 · nac solo 16 · cens | — | 3/3 | 1/3 | +0 | empate / ruido |
| alterna4k | cuadrada, período 4000 | 28001–28003 (3) | 0/3 · R0 0.36 · nac solo 14 · 6000 | 0/3 · R0 0.13 · nac solo 15 · 14000 | — | 2/3 | 2/3 | +0 | empate / ruido |
| alterna8k | cuadrada, período 8000 | 28001–28003 (3) | 0/3 · R0 0.25 · nac solo 17 · 10000 | 1/3 · R0 0.11 · nac solo 19 · 10000 | — | 1/3 | 1/3 | −1 | empate / ruido |
| **onda8k** | coseno, período 8000 | 28001–28006 (6) | 3/6 · R0 0.44 · nac solo 46 · 8000 | 0/6 · R0 0.22 · nac solo 33 · 11000 | 2/6 · R0 0.47 · **nac solo 62** · 8000 | **5/6** | **5/6** | **+3** | **CODIGO** (pero ≈ la base; SIN_SOS mejor) |
| suave | fijo A (0, 0), B (+0.4, 0) | 28001–28006 (6) | 6/6 · R0 0.36 · nac solo 76 · cens | 6/6 · R0 0.32 · nac solo 80 · cens | 3/3 · R0 0.51 · nac solo 80 · 12000 | 4/6 | 3/6 | +0 | empate / ruido |
| bonanza | fijo B (+0.8, 0); A sigue | 28001–28003 (3) | 3/3 · R0 0.78 · nac solo 169 · 0 | 3/3 · R0 0.63 · nac solo 137 · 0 | — | 3/3 | 2/3 | +0 | CODIGO (≈ la base) |
| medio_veneno | fijo A (−0.2, 0), B (+0.8, 0) | 28001–28006 (6) | 1/6 · R0 0.38 · nac solo 44 · 15000 | 3/6 · R0 0.23 · nac solo 45 · cens | 3/3 · R0 0.40 · nac solo 68 · 8000 | 4/6 | 3/6 | **−2** | empate; **SIN_SOS gana a los dos** |
| zona_mitad | A↔B sólo en [0, L/2) | 28001–28006 (6) | 0/6 · R0 0.18 · nac solo 22 · cens | 0/6 · R0 0.16 · nac solo 10 · cens | — | 3/6 (1 empate) | 4/6 | +0 | empate; razón nac solo 2.0 (la mayor) |
| deriva8k | A → (0,0), B → (+0.4,0) en 8000 | 28001–28003 (3) | 3/3 · R0 0.39 · nac solo 107 · 14000 | 3/3 · R0 0.33 · nac solo 86 · 12000 | — | 2/3 | 2/3 | +0 | empate / ruido |
| reina (Reina Roja v2) | A↔B cada vez que las mordidas vuelven al 80 % | 28001–28003 (3) | 1/3 · R0 0.08 · nac solo 14 · cens | 0/3 · R0 0.06 · nac solo 16 · cens | — | 2/3 | 0/3 | +1 | degeneró en alterna2k (§4) |

**La razón CODIGO/PERILLAS en nacimientos solos (suma sobre las semillas comunes), la medida con menos ruido:**

| mundo | n | nac solo CODIGO | nac solo PERILLAS | razón | persiste C vs P | SOS post (CODIGO) | errores/copia post |
|---|---|---|---|---|---|---|---|
| **quieto (base)** | 6 | 757 | 492 | **1.54** | 6 vs 6 | 0.01 | 1.19 |
| onda8k | 6 | 322 | 201 | 1.60 | 3 vs 0 | 0.08 | 1.23 |
| zona_mitad | 6 | 150 | 74 | 2.03 | 0 vs 0 | 0.06 | 1.38 |
| gradual16k | 6 | 218 | 148 | 1.47 | 1 vs 0 | 0.04 | 1.19 |
| medio_veneno | 6 | 424 | 273 | 1.55 | 1 vs 3 | **0.31** | **1.79** |
| bonanza | 3 | 530 | 415 | 1.28 | 3 vs 3 | 0.00 | 1.10 |
| golpe | 6 | 129 | 107 | 1.21 | 1 vs 0 | 0.23 | 1.62 |
| suave | 6 | 459 | 514 | 0.89 | 6 vs 6 | 0.00 | 1.11 |

Lectura: la razón en los mundos que cambian (0.9–2.0) rodea la razón de base (1.54). Donde más se prende la SOS (golpe 0.23,
medio_veneno 0.31) los errores por copia suben a 1.6–1.8 y la razón **baja** (1.21) o la persistencia se pierde (1 vs 3).

## 2. Los mejores mundos, en humano (b)
### 2.1 `onda8k` — estacional suave (coseno, período 8 000): el único donde el CÓDIGO «gana» de verdad, y no por lo que esperaba
El valor de A baja y el de B sube sin saltos; se cruzan a los 2 000 pasos (los dos ≈ +0.2: morder «mal» casi no cuesta), se intercambian
del todo a los 4 000 y vuelven. Hay pasos intermedios siempre.
- Con 6 semillas, CODIGO le gana a PERILLAS en R0 final (0.44 vs 0.22) y en nacimientos solos (46 vs 33 de mediana) en 5/6, y **persiste
  3/6 contra 0/6**. En el vivero los dos brazos siguen la onda igual (nacimientos por ventana 50 → 15 → 50 → 15 → 50); la diferencia
  aparece después del corte.
- **Pero la razón de nacimientos solos (1.60) es la misma que sin cambio (1.54).** La ventaja no la creó la onda: la onda sólo la deja ver
  porque, a diferencia de `quieto`, aquí PERILLAS se extingue y CODIGO no.
- **Y la SOS no ayuda: estorba.** CODIGO_SIN_SOS hizo 713 nacimientos solos contra 322 de CODIGO (mismas 6 semillas); en la semilla 28006
  SIN_SOS llegó a 166–203 nacimientos por ventana en la última vuelta del vivero y persistió con 3 cuerpos.
- Qué eligió la selección en los vivos (`lee_cintas.py`): nada consistente en el órgano (copiar/nacer/sin0 sigue mandando; en 28002 aparece
  `morir/sin0/hermano/olvidar` y en 28003 `vida/sin0/hijo/promediar`, 1 vez cada uno); en la cinta, ejes de «vida lenta» (`EJE 2`) y
  `SUM 9 +1` (eta_s). Es ruido de 1–4 cuerpos.

### 2.2 `zona_mitad` — el mundo parcial: la mayor razón (2.0), pero nadie vive
Sólo la mitad del anillo se intercambia; la otra mitad es el mundo viejo. Nadie persiste (0/6 y 0/6), pero el CÓDIGO deja el doble de
nacimientos solos (150 vs 74) y gana en 4/6. Es la única pista de que un mundo pueda AMPLIFICAR la ventaja de base; con 74 nacimientos
en total del lado de PERILLAS es también la más frágil.

### 2.3 `medio_veneno` y `suave` — donde se ve que la SOS estorba
Con A a −0.2 y B a +0.8 (`medio_veneno`), la SOS se prende en el 31 % de los partos y los errores por copia suben de 1.1 a 1.8:
CODIGO persiste 1/6, PERILLAS 3/6 y **CODIGO_SIN_SOS 3/3** (nac solo 68 de mediana contra 44). En `suave` (nadie se envenena) la SOS no se
prende y CODIGO ≈ PERILLAS ≈ SIN_SOS (todos viven 6/6). Hipótesis: la SOS multiplica ×3 la tasa justo cuando la población está en el
piso, y el 35 % de los errores expresados son dañinos (INFORME de Opus): carga mutacional en el peor momento, sin un peldaño que subir.

## 3. Propuesta v0.1 para preregistrar (c)
**Pregunta honesta, dos partes.** (i) ¿El CÓDIGO vive solo mejor que las PERILLAS **sin que el mundo cambie**, y por qué? (ii) ¿Algún mundo que
cambia AMPLIFICA esa ventaja? Medir (ii) sin (i) fue el hueco de v0: R0 final ya lo gana el código en `quieto`.

- **Mundos:** `quieto` (control obligatorio para los DOS genomas) y `onda8k` (`eco['cambio'] = dict(tipo='onda', t=t_cambio, periodo=8000)`;
  las anclas F4/F5 de `construye_fable.py` son todo lo que hay que meter en `motor_codigo`; la identidad con la tupla ya está probada).
  Opcional, si el costo lo permite: `zona_mitad`.
- **Brazos por mundo:** CODIGO, PERILLAS, CODIGO_SIN_SOS, MUT0, AZAR. TL de serie: T 80 000, cambio 15 000, corte 40 000.
- **Medida principal:** **nac solo** (nacimientos en [corte, T − margen]) y persistencia. R0 final queda descriptivo (10–50 cuerpos).
- **La letra:**
  - **P0 (la base):** en `quieto`, CODIGO > PERILLAS en nac solo en ≥ 14/20. Predigo SÍ (0.75; aquí 5/6 y razón 1.54).
  - **P1 (amplificación):** razón CODIGO/PERILLAS en `onda8k` ≥ 1.5 × la razón en `quieto`, pareado por semilla, en ≥ 14/20. Predigo **NO**
    (0.7; aquí 1.60 vs 1.54).
  - **P2 (persistencia):** en `onda8k`, CODIGO persiste en ≥ 5 semillas más que PERILLAS. Predigo SÍ (0.55; aquí +3 de 6).
  - **P3 (la SOS):** CODIGO > SIN_SOS en nac solo en ≥ 13/20. Predigo **NO** (0.8): espero SIN_SOS > CODIGO en ≥ 13/20 (la SOS estorba). Si sale
    así, la SOS v0 se declara refutada como mecanismo y se rediseña (umbral más alto, o factor < 1: BAJAR la tasa en estrés).
  - **Guardias:** CODIGO > MUT0 (variación) y CODIGO > AZAR (selección) en nac solo ≥ 14/20 en `quieto`. La de MUT0 la predigo SÍ (0.75;
    aquí 5/6 en los dos mundos, §6). **La que puede caer es la de AZAR** (0.5): con n_refund 1 200–2 100 fundadores repuestos del banco por
    corrida, el «donante al azar» y el «padre» se parecen mucho; si AZAR ≈ CODIGO, lo que se ve es la carga mutacional del genoma, no
    selección.
  - **Control extra barato (la robustez):** PERILLAS_ROBUSTA = PERILLAS con p_mut bajado hasta que la fracción de hijos con fenotipo idéntico
    iguale a la del código (~0.65; hoy ~0.40 con p 0.05 × 18). Si PERILLAS_ROBUSTA ≈ CODIGO en `quieto`, la ventaja es «mutar menos el
    fenotipo», y v0 igualó mal la carga (ERR candidato: se igualaron errores por copia, no fenotipos cambiados por copia).
- **Veredicto esperado:** HAY ALGO MODESTO (0.55: P0 y P2 sin P1), NO (0.3), FUNCIONA (0.15).
- **Costo:** 2 mundos × 5 brazos × 20 semillas × ~170 s ≈ 9.4 h de CPU por ventana; Pool 6 ≈ 1.6 h la serie y 1.6 h la réplica.

## 4. Lo que no funcionó y por qué creo que no (d)
- **El cambio gradual no creó peldaños que la variación subiera.** `gradual8k`, `escalera4`, `gradual16k`: los dos brazos siguen la rampa
  (nacimientos en el vivero 50 → 20 → 30) y se extinguen después del corte igual que en `golpe`. Lo que muere no es la genética: es que
  el vivero repone fundadores LIMPIOS sin parar (n_refund 1 200–2 100 por corrida contra 200–300 nacimientos reales), así que la población
  del vivero es casi toda fundadores que aprenden desde cero; la selección casi no ve generaciones encadenadas. El peldaño existe en el
  mundo pero no hay linaje que lo suba.
- **Los mundos que alternan (2k/4k/8k) castigan a los dos igual.** Cada vuelta mata lo aprendido; ninguno guarda nada del período (el genoma no
  tiene reloj ni memoria de estación). La SOS se prende en cada vuelta (0.10–0.20) y no sirve.
- **Reina Roja v1 y v2 no se pudieron construir bien.** v1 (el veneno persigue a la letra que evitan) no tiene señal: la población muerde B casi
  tanto como A (0.46 antes y 0.48 después del cambio, en los datos de Opus): con tantos fundadores limpios nadie «evita». v2 (el mundo cambia
  cuando las mordidas totales vuelven al 80 %) disparó cada 2 000 pasos exactos, porque el total de mordidas no cae (los fundadores repuestos
  siguen mordiendo): degeneró en `alterna2k` (números idénticos). Una Reina Roja de verdad necesita medir a los NACIDOS, no a la población.
- **`bonanza` y `suave` no discriminan:** los dos viven. Sirven de piso, no de prueba.
- **La SOS v0 estorba** (§2.3). No es que «no se demuestre»: en 3 mundos SIN_SOS ≥ CODIGO.

## 5. Predicciones refutadas (de `PREDICCIONES_previas.md`) y lo que no pude verificar
**Refutadas:**
- «`golpe`: CODIGO ≈ PERILLAS (P = 0.45)»: CODIGO ganó R0 final 3/3 y luego 4/6. No lo esperaba, y la explicación (ventaja de base) tampoco.
- «`gradual`: los dos suben a post/pre 0.5–0.9 y persisten 1–3/3»: post/pre 0.7–0.8 sí, persistencia 0–1/6 no.
- «`bonanza`: PERILLAS explota B antes»: no, CODIGO ≥ PERILLAS (3/3 R0, 2/3 nac solo). El «invertir» que yo esperaba ver seleccionado
  aparece en 1 de 10 vivos de PERILLAS en `medio_veneno` y en `quieto` (3 semillas, 1 cuerpo cada una): no es lo que gana.
- «`reina`: 2–4 intercambios»: 9, uno cada 2 000.
- «la ventaja, si la hay, la explica la SOS o el ORG `invertir`/`reciente`»: no; la SOS estorba y el órgano de los vivos es el de fábrica.
- Global «P(2–3 mundos ganados) = 0.35»: salieron 2 con la regla mecánica (`onda8k`, `bonanza`), pero la lectura correcta es que el CÓDIGO gana
  en casi todos los mundos Y en `quieto`: la pregunta estaba mal planteada, no la respuesta.

**Se cumplieron:** `alterna2k` la peor; `suave` los dos viven; en `onda8k` persistencia 1–2/3 de CODIGO (salió 2/3 y 3/6).

**No verifiqué:**
- La guardia de SELECCIÓN (AZAR) en ningún mundo, ni PERILLAS con la carga igualada en fenotipo (§3).
- Nada con T largo (serie): todo es TL corto (T 36 000), y la exploratoria de Opus mostró que el T importa.
- Si la ventaja de base del código en `quieto` sobrevive a 20 semillas: aquí es 5/6 en nac solo y 4/6 en R0 final.
- Qué mutaciones se seleccionan: sólo tengo las cintas de los vivos en T (1–23 cuerpos), no el banco en el corte.

## 6. Últimas corridas (MUT0 y SIN_SOS de confirmación, 6 semillas 28001–28006; leídas a las 21:25)
**La guardia de variación SE SOSTIENE: la ventaja de base es de la VARIACIÓN de la cinta, no del lector.**

| mundo | brazo | nac solo (suma 6 sem.) | gana a CODIGO en nac solo | persiste | lectura |
|---|---|---|---|---|---|
| quieto | MUT0 (cinta sin errores) | **443** vs CODIGO 757 vs PERILLAS 492 | 1/6 | 6 vs 6 vs 6 | MUT0 ≈ PERILLAS; CODIGO > los dos (5/6). La cinta sin errores no explica la base. |
| onda8k | MUT0 | **195** vs CODIGO 322 vs PERILLAS 201 | 1/6 | **0** vs 3 vs 0 | igual: MUT0 ≈ PERILLAS, se extingue como PERILLAS. |
| onda8k | CODIGO_SIN_SOS | **713** vs 322 | 4/6 | 2 vs 3 | la SOS estorba (la semilla 28006 aporta 405 sola; sin ella 308 vs 278, 3/5). |
| medio_veneno | CODIGO_SIN_SOS | 357 vs 424 | 4/6 | **5 vs 1** (PERILLAS 3) | la SOS estorba en persistencia; la suma la tuerce CODIGO 28001 (216). |
| suave | CODIGO_SIN_SOS | **712** vs 459 | 4/6 | 6 vs 6 | la SOS casi no se prende aquí (0.00) y aun así SIN_SOS > CODIGO: parte de la diferencia es ruido de semilla. |

Lo que cambia con esto en la propuesta (§3): la guardia MUT0 la predigo ahora **SÍ se sostiene (0.75)**, y la pregunta (i) se afina:
**los errores de copia de la cinta rinden más que la mutación numérica de las perillas incluso en el mundo quieto.** Candidatos a
mecanismo (para que el Opus elija uno y lo preregistre, no para creerlos): (1) robustez: el 64–67 % de los hijos con código nacen con
el MISMO fenotipo (errores neutros: `SUM j 0` → `SUM j ±1` sobre perillas que no importan, o DEF no llamados), contra ~40 % en
PERILLAS; la variación del código explora sin pagar tanto (Wagner 2008); (2) los pasos discretos de 0.15 log sobre EJES pleiotrópicos
mueven «vida lenta» (`EJE 2`, el más frecuente en los vivos de `quieto`: `EJE 2 −1` en 3 de 6 semillas) de a saltos que la selección
en N_e 10–50 sí ve; (3) simple azar de 6 semillas. La lectura (1) tiene un control barato: PERILLAS con p_mut bajado hasta igualar la
fracción de hijos con fenotipo idéntico (~0.65), en `quieto`.

## 7. Para retomar
```
cd experimentos/organelos/codigo/exploracion_fable
python construye_fable.py && python identidad_fable.py          # 8/8
python corre_fable.py --mundo onda8k --semillas 28007,28008,28009 --brazos CODIGO,PERILLAS,CODIGO_SIN_SOS,MUT0
python corre_fable.py --md ; python corre_fable.py --lee ; python lee_cintas.py datos/onda8k_corto datos/quieto_corto
```
